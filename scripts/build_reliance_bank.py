import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2026", "FY2025", "FY2024", "FY2023", "FY2022", "FY2021", "FY2020", "FY2019"]
AR_URLS = {
    "FY2026": "https://find-and-update.company-information.service.gov.uk/company/00068835/filing-history/MzUzNTUyMDU0NWFkaXF6a2N4/document?format=pdf&download=0",
    "FY2025": "https://find-and-update.company-information.service.gov.uk/company/00068835/filing-history/MzQ3NTMwMjc2NGFkaXF6a2N4/document?format=pdf&download=0",
    "FY2024": "https://find-and-update.company-information.service.gov.uk/company/00068835/filing-history/MzQzMDIwODk2MGFkaXF6a2N4/document?format=pdf&download=0",
    "FY2023": "https://find-and-update.company-information.service.gov.uk/company/00068835/filing-history/MzM5NDkwNzg3NmFkaXF6a2N4/document?format=pdf&download=0",
    "FY2022": "https://find-and-update.company-information.service.gov.uk/company/00068835/filing-history/MzM1MjMwMDYyNWFkaXF6a2N4/document?format=pdf&download=0",
    "FY2021": "https://www.reliancebankltd.com/wp-content/uploads/2021/11/Reliance-Bank-Report-and-Accounts-for-the-year-ending-31March2021.pdf",
    "FY2020": "https://www.reliancebankltd.com/wp-content/uploads/2021/09/Reliance-Bank-Ltd-Annual-Accounts-for-the-year-ending-31March2020-1-1.pdf",
    "FY2019": "https://www.reliancebankltd.com/wp-content/uploads/2021/09/Reliance-Bank-Ltd-Annual-Accounts-for-the-year-ending-31March2020-1-1.pdf",
}
P3_2023_URL = "https://www.reliancebankltd.com/wp-content/uploads/2023/10/RBL-Pillar-3-Disclosures-31-March-2023-for-website-30Oct2023.pdf"
P3_2022_URL = "https://www.reliancebankltd.com/wp-content/uploads/2023/04/RBL-Pillar-3-Disclosures-31-March-2022-final-post-Board.pdf"

# The Bank's own website copies, found by enumerating its WordPress media library
# (/wp-json/wp/v2/media?mime_type=application/pdf) rather than guessing filenames:
# FY2024-FY2026 found 2026-09-15, FY2022-FY2023 found 2026-09-16 on a re-enumeration
# (6 pages, 600 PDFs). These matter because the Companies House copies used above are
# image-only scans (Producer "libtiff / tiff2pdf", ~1 character of text per page) that
# had to be OCR'd, whereas all five of these carry a real text layer - so findings for
# those years rest on exact text extraction instead of OCR. Kept alongside, not in
# place of, the Companies House URLs, which remain the filed-of-record source.
AR_WEBSITE_URLS = {
    "FY2026": "https://www.reliancebankltd.com/wp-content/uploads/2026/08/RBL-Annual-Accounts-31st-March-2026.pdf",
    "FY2025": "https://www.reliancebankltd.com/wp-content/uploads/2025/07/Reliance-Bank-Report-and-Accounts-FINAL.pdf",
    "FY2024": "https://www.reliancebankltd.com/wp-content/uploads/2024/08/2024-07-23-Reliance-Bank-Report-and-Accounts-2024-Final_20-Aug.pdf",
    "FY2023": "https://www.reliancebankltd.com/wp-content/uploads/2023/10/Reliance-Bank-Report-and-Accounts-2023-Final-for-website-30Oct2023.pdf",
    "FY2022": "https://www.reliancebankltd.com/wp-content/uploads/2023/04/Reliance-Bank-Report-and-Accounts-31-March-2022.pdf",
}

ENTITY_NOTE = (
    "Reliance Bank Limited (Companies House 00068835; FRN 204537) is the bank in the supplied bank list. "
    "The statements are the Bank's own entity accounts in £. The available years are FY2019-FY2026 "
    "(31 March year ends). All Companies House reports were image-only scans and were transcribed after rendering/OCR. "
    "The 2024 accounts restate the 2023 cash-flow comparative (operating cash £(27,740,745) versus £(28,182,841) "
    "reported in the 2023 accounts), following a money-market-fund reclassification. Per project convention, each "
    "year uses its own originally published figures; the restatement is documented rather than silently applied. "
    "The FY2026 operating subtotal is £67,891 higher than its listed adjustments and its reported operating total "
    "is £67,891 lower than subtotal plus listed changes; FY2022 has £1 differences in both places. These are shown "
    "as source arithmetic differences, not estimates."
)
CASH_SOURCES = "Sources - Reliance Bank Limited entity cash flows, £:\n" + "\n".join(
    f"{y}: Annual Report and Accounts for year ended 31 March {y[-4:]}, cash-flow statement and notes 23-25, {AR_URLS[y]}"
    for y in YEARS
) + "\n\n" + ENTITY_NOTE

BS_RESTATEMENT_NOTE = (
    "The FY2024 Annual Report's FY2023 comparative balance sheet reclassifies figures relative to the FY2023 "
    "Annual Report's own originally published FY2023 balance sheet: Investment Property (£603,774) was folded "
    "into Other Assets, part of Loans and Advances to Banks was reclassified into Other Assets, and Other "
    "Liabilities/Accruals and Deferred Income were regrouped. Per project convention, each year's own "
    "originally published figures are used rather than a later restated comparative."
)
DEBT_SECURITIES_NOTE = (
    "DEBT SECURITIES COMPOSITION: the 'Debt Securities' note (numbered variously 10, 11 or 9 across years - "
    "FY2019/FY2020 Report and Accounts p.38, FY2021 p.43, FY2023 p.43, FY2024 p.49, FY2025 p.52, FY2026 p.62) "
    "discloses a single line, '[Sterling Certificates of Deposit/Securities] Issued by [Commercial] Banks/Building "
    "Societies' (wording varies slightly by year), for every year FY2019-FY2026: 100% of the balance in every year "
    "is issued by banks/building societies (no UK government/gilts/sovereign or corporate/supranational/ABS "
    "component disclosed) and valued at amortised cost less impairment (the note states securities are 'generally "
    "held to maturity and valued at amortised cost'; the FY2026 accounting-policy note confirms subsequent "
    "measurement at amortised cost using the effective interest method - no FVOCI/FVTPL portion is disclosed in "
    "any year). Each year's note gives only a maturity-band breakdown (e.g. <3 months, 3-6 months, etc.), not a "
    "further measurement-basis or issuer-type split - there is nothing to sub-divide against, so the row is "
    "relabelled in place rather than split into sub-rows."
)
BS_SOURCES = "Sources - Reliance Bank Limited entity balance sheet, £:\n" + "\n".join(
    f"{y}: Annual Report and Accounts for year ended 31 March {y[-4:]}, Balance Sheet, {AR_URLS[y]}"
    for y in YEARS
) + "\n\n" + ENTITY_NOTE + "\n\n" + BS_RESTATEMENT_NOTE + "\n\n" + DEBT_SECURITIES_NOTE

bs_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and balances at central bank", {"FY2026": 65404792, "FY2025": 68150991, "FY2024": 99657428, "FY2023": 83261986, "FY2022": 91287306, "FY2021": 73927250, "FY2020": 51769502, "FY2019": 36565164}),
    ("DATA", "Loans and advances to banks / Balances at banks", {"FY2026": 8415747, "FY2025": 5729293, "FY2024": 9342232, "FY2023": 12342225, "FY2022": 23726132, "FY2021": 46802990, "FY2020": 29850667, "FY2019": 32119504}),
    ("DATA", "Loans and advances to customers", {"FY2026": 146696075, "FY2025": 142039997, "FY2024": 125748749, "FY2023": 118818336, "FY2022": 96522411, "FY2021": 77505973, "FY2020": 53204878, "FY2019": 47220230}),
    ("DATA", "Debt securities (amortised cost, issued by banks/building societies)", {"FY2026": 47845043, "FY2025": 31152108, "FY2024": 25735400, "FY2023": 32981508, "FY2022": 34201068, "FY2021": 40540011, "FY2020": 60210153, "FY2019": 65285621}),
    ("DATA", "Intangible fixed assets", {"FY2026": 126970, "FY2025": 175064, "FY2024": 147533, "FY2023": 284207, "FY2022": 443170, "FY2021": 392501, "FY2020": 394287, "FY2019": 301903}),
    ("DATA", "Tangible fixed assets", {"FY2026": 4845723, "FY2025": 4745873, "FY2024": 4035112, "FY2023": 3620828, "FY2022": 3153335, "FY2021": 3282956, "FY2020": 2599924, "FY2019": 2450094}),
    ("DATA", "Investment property", {"FY2023": 603774, "FY2022": 1573962, "FY2021": 1573962}),
    ("DATA", "Other assets", {"FY2026": 11828905, "FY2025": 14247232, "FY2024": 11959308, "FY2023": 8250, "FY2022": 17750, "FY2021": 13081, "FY2020": 12476, "FY2019": 18577}),
    ("DATA", "Prepayments and accrued income", {"FY2026": 299078, "FY2025": 410388, "FY2024": 267423, "FY2023": 267150, "FY2022": 321998, "FY2021": 287516, "FY2020": 408722, "FY2019": 284598}),
    ("TOTAL", "Total assets", {"FY2026": 285462333, "FY2025": 266650946, "FY2024": 276893185, "FY2023": 252188264, "FY2022": 251247132, "FY2021": 244326240, "FY2020": 198450609, "FY2019": 184245691}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Customer accounts", {"FY2026": 254118275, "FY2025": 241237545, "FY2024": 252228935, "FY2023": 230049991, "FY2022": 236212051, "FY2021": 231503315, "FY2020": 186411063, "FY2019": 171635444}),
    ("DATA", "Other liabilities", {"FY2026": 557347, "FY2025": 689476, "FY2024": 681122, "FY2023": 131819, "FY2022": 139116, "FY2021": 112920, "FY2020": 11864, "FY2019": 12868}),
    ("DATA", "Accruals and deferred income", {"FY2025": 0, "FY2024": 915795, "FY2023": 756801, "FY2022": 453172, "FY2021": 517568, "FY2020": 361945, "FY2019": 443315}),
    ("DATA", "Current tax liability", {"FY2026": 185893}),
    ("DATA", "Deferred tax liability", {"FY2026": 44631, "FY2025": 2303, "FY2024": 67671, "FY2023": 0, "FY2022": 0, "FY2021": 0, "FY2020": 13529, "FY2019": 11092}),
    ("TOTAL", "Total liabilities", {"FY2026": 254906146, "FY2025": 241929324, "FY2024": 253893523, "FY2023": 230938611, "FY2022": 236804339, "FY2021": 232133803, "FY2020": 186798401, "FY2019": 172102719}),
    ("SECTION", "Equity", {}),
    ("DATA", "Called up share capital", {"FY2026": 25000000, "FY2025": 20000000, "FY2024": 20000000, "FY2023": 20000000, "FY2022": 13000000, "FY2021": 10000000, "FY2020": 10000000, "FY2019": 9000000}),
    ("DATA", "Revaluation reserve", {"FY2026": 1777644, "FY2025": 1412663, "FY2024": 811847, "FY2023": 811847, "FY2022": 1132160, "FY2021": 1258277, "FY2020": 0, "FY2019": 0}),
    ("DATA", "Profit and loss account", {"FY2026": 3778543, "FY2025": 3308959, "FY2024": 2187815, "FY2023": 437806, "FY2022": 310633, "FY2021": 934160, "FY2020": 1652208, "FY2019": 3142972}),
    ("TOTAL", "Equity shareholder's funds", {"FY2026": 30556187, "FY2025": 24721622, "FY2024": 22999662, "FY2023": 21249653, "FY2022": 14442793, "FY2021": 12192437, "FY2020": 11652208, "FY2019": 12142972}),
    ("TOTAL", "Total liabilities and equity", {"FY2026": 285462333, "FY2025": 266650946, "FY2024": 276893185, "FY2023": 252188264, "FY2022": 251247132, "FY2021": 244326240, "FY2020": 198450609, "FY2019": 184245691}),
]
bw_bs_sources = BS_SOURCES

PL_SOURCES = "Sources - Reliance Bank Limited entity income statement, £:\n" + "\n".join(
    f"{y}: Annual Report and Accounts for year ended 31 March {y[-4:]}, Income Statement and Statement of Comprehensive Income, {AR_URLS[y]}"
    for y in YEARS
) + "\n\n" + ENTITY_NOTE + (
    "\n\nPresentation notes: FY2026 relabelled the third interest-income line \"Bank and Discount Market "
    "Deposits\" (previously \"Other\") and combined fee income/expense into a single \"Net Fees and Commission "
    "Income\" row without a separate \"Other Operating Income\" line - blank cells reflect that year's own "
    "published structure. \"Revaluation of Investment Property\" was a charge only in FY2023. \"Impairment "
    "Charge on Loans and Advances\" was a credit (income) in FY2022, shown as a positive value here matching "
    "the report's own sign."
)

pl_rows = [
    ("SECTION", "Interest income", {}),
    ("DATA", "On debt securities", {"FY2026": 617560, "FY2025": 616711, "FY2024": 906012, "FY2023": 422427, "FY2022": 87111, "FY2021": 351962, "FY2020": 594066, "FY2019": 641280}),
    ("DATA", "On loans and advances to customers", {"FY2026": 9112271, "FY2025": 8061008, "FY2024": 6720038, "FY2023": 4295434, "FY2022": 3007940}),
    ("DATA", "Bank and discount market deposits / Other", {"FY2026": 4105052, "FY2025": 5673987, "FY2024": 4004050, "FY2023": 2059797, "FY2022": 247053, "FY2021": 2231261, "FY2020": 2368407, "FY2019": 2114057}),
    ("TOTAL", "Total interest income", {"FY2026": 13834883, "FY2025": 14351706, "FY2024": 11630100, "FY2023": 6777658, "FY2022": 3342104, "FY2021": 2583223, "FY2020": 2962473, "FY2019": 2755337}),
    ("DATA", "Interest expense", {"FY2026": -4230881, "FY2025": -4871055, "FY2024": -2908023, "FY2023": -1048467, "FY2022": -226523, "FY2021": -339335, "FY2020": -888263, "FY2019": -822418}),
    ("TOTAL", "Net interest income", {"FY2026": 9604002, "FY2025": 9480651, "FY2024": 8722077, "FY2023": 5729191, "FY2022": 3115581, "FY2021": 2243888, "FY2020": 2074210, "FY2019": 1932919}),
    ("SECTION", "Fees, commissions and other operating income", {}),
    ("DATA", "Fees and commissions income", {"FY2026": 609353, "FY2025": 617013, "FY2024": 844088, "FY2023": 777631, "FY2022": 741012, "FY2021": 538562, "FY2020": 765852, "FY2019": 700492}),
    ("DATA", "Other operating income", {"FY2025": 0, "FY2024": 30214, "FY2023": 76718, "FY2022": 111614, "FY2021": 109094, "FY2020": 96892, "FY2019": 62245}),
    ("DATA", "Fees and commissions expense", {"FY2026": -513096, "FY2025": -519874, "FY2024": -506137, "FY2023": -468192, "FY2022": -466297, "FY2021": -203075, "FY2020": -256682, "FY2019": -186947}),
    ("TOTAL", "Net fees and commission income", {"FY2026": 96257, "FY2025": 97139, "FY2024": 368165, "FY2023": 386157, "FY2022": 386329}),
    ("TOTAL", "Operating income", {"FY2026": 9700259, "FY2025": 9577790, "FY2024": 9090242, "FY2023": 6115348, "FY2022": 3501910, "FY2021": 2688469, "FY2020": 2680272, "FY2019": 2508709}),
    ("SECTION", "Operating expenses", {}),
    ("DATA", "Administrative expenses", {"FY2026": -7929596, "FY2025": -7563544, "FY2024": -6724210, "FY2023": -5166893, "FY2022": -3907710, "FY2021": -3667941, "FY2020": -2998818, "FY2019": -1971987}),
    ("DATA", "Amortisation", {"FY2026": -71120, "FY2025": -116162, "FY2024": -175719, "FY2023": -202157, "FY2022": -203839, "FY2021": -178797, "FY2020": -160986, "FY2019": -146267}),
    ("DATA", "Depreciation", {"FY2026": -370918, "FY2025": -373648, "FY2024": -262446, "FY2023": -163034, "FY2022": -156387, "FY2021": -158545, "FY2020": -101758, "FY2019": -91616}),
    ("DATA", "Revaluation of investment property", {"FY2023": -128301}),
    ("DATA", "Impairment (charge)/credit on loans and advances", {"FY2026": -230821, "FY2025": -93310, "FY2024": -9455, "FY2023": -221018, "FY2022": 16382, "FY2021": 38829, "FY2020": -90466, "FY2019": -105205}),
    ("TOTAL", "Operating expenses", {"FY2026": -8602455, "FY2025": -8146664, "FY2024": -7171830, "FY2023": -5881403, "FY2022": -4251554, "FY2021": -4508727, "FY2020": -4168599, "FY2019": -3194202}),
    ("TOTAL", "Profit/(loss) before tax", {"FY2026": 1097804, "FY2025": 1431126, "FY2024": 1918412, "FY2023": 233945, "FY2022": -749644, "FY2021": -1820258, "FY2020": -1488327, "FY2019": -685493}),
    ("DATA", "Taxation charge/(credit)", {"FY2026": -228220, "FY2025": -209982, "FY2024": -67671, "FY2023": -106772, "FY2022": 140817, "FY2021": 459451, "FY2020": -2437, "FY2019": 37634}),
    ("TOTAL", "Profit/(loss) on activities after tax", {"FY2026": 869584, "FY2025": 1221144, "FY2024": 1850741, "FY2023": 127173, "FY2022": -608827, "FY2021": -1360807, "FY2020": -1490764, "FY2019": -647859}),
    ("SECTION", "Other comprehensive income", {}),
    ("DATA", "Revaluation of tangible fixed assets, net of deferred tax", {"FY2026": 364981, "FY2025": 600816, "FY2023": -320312}),
    ("DATA", "Deferred tax rate change related to OCI items", {"FY2022": -95118}),
    ("TOTAL", "Total comprehensive income/(loss) for the year", {"FY2026": 1234565, "FY2025": 1821960, "FY2024": 1850741, "FY2023": -193139, "FY2022": -703945}),
]

EQUITY_SOURCES = "Sources - Reliance Bank Limited entity Statement of Changes in Equity, £:\n" + "\n".join(
    f"{y}: Annual Report and Accounts for year ended 31 March {y[-4:]}, Statement of Changes in Equity, {AR_URLS[y]}"
    for y in YEARS
) + "\n\n" + ENTITY_NOTE
equity_headers = ["Called up share capital", "Revaluation reserve", "Profit and loss reserve", "Total shareholder funds"]
equity_rows = [
    ("TOTAL", "At 31 March 2021 (opening balance)", (10000000, 1258277, 934160, 12192437)),
    ("DATA", "Loss for the year (FY2022)", (None, None, -608827, -608827)),
    ("DATA", "Reserve - depreciation on revaluation", (None, -30999, 30999, 0)),
    ("DATA", "Reserve - deferred tax rate change", (None, -95118, -45699, -140817)),
    ("DATA", "New shares issued", (3000000, None, None, 3000000)),
    ("TOTAL", "At 31 March 2022", (13000000, 1132160, 310633, 14442793)),
    ("DATA", "Revaluation, net of deferred tax (FY2023)", (None, -320313, None, -320313)),
    ("DATA", "Profit for the year (FY2023)", (None, None, 127173, 127173)),
    ("DATA", "New shares issued", (7000000, None, None, 7000000)),
    ("TOTAL", "At 31 March 2023", (20000000, 811847, 437806, 21249653)),
    ("DATA", "Profit for the year (FY2024)", (None, None, 1850741, 1850741)),
    ("DATA", "Distributions to Salvation Army", (None, None, -100000, -100000)),
    ("DATA", "Adjustment", (None, None, -732, -732)),
    ("TOTAL", "At 31 March 2024", (20000000, 811847, 2187815, 22999662)),
    ("DATA", "Revaluation of property, net of deferred tax (FY2025)", (None, 600816, None, 600816)),
    ("DATA", "Profit for the year (FY2025)", (None, None, 1221144, 1221144)),
    ("DATA", "Distributions to Salvation Army", (None, None, -100000, -100000)),
    ("TOTAL", "At 31 March 2025", (20000000, 1412663, 3308959, 24721622)),
    ("DATA", "New shares issued", (5000000, None, None, 5000000)),
    ("DATA", "Revaluation of property (FY2026)", (None, 364981, None, 364981)),
    ("DATA", "Profit for the year (FY2026)", (None, None, 869584, 869584)),
    ("DATA", "Distributions to Salvation Army", (None, None, -400000, -400000)),
    ("TOTAL", "At 31 March 2026 (Total Equity)", (25000000, 1777644, 3778543, 30556187)),
]

AQ_SOURCES = "Sources - Reliance Bank Limited entity loan book, £:\n" + "\n".join(
    f"{y}: Annual Report and Accounts for year ended 31 March {y[-4:]}, Loans and Advances to Customers and Loan Loss Provisioning notes, {AR_URLS[y]}"
    for y in YEARS
) + "\n\n" + ENTITY_NOTE + (
    "\n\nNPL ratio = non-performing loans and advances before provisions / total loans and advances to "
    "customers (gross of impairment provision, i.e. before the deduction shown on the Balance Sheet). Coverage "
    "ratio = impairment provision / non-performing loans and advances before provisions. Both are derived from "
    "disclosed figures, not themselves separately labelled ratios in the source. \"Loans\" was relabelled \"SME "
    "Loans\" in the FY2026 Annual Report - same underlying product line."
)
aq_rows = [
    ("SECTION", "Loan book by product", {}),
    ("DATA", "Overdrafts (recoverable on demand)", {"FY2026": 15167, "FY2025": 1591, "FY2024": 446798, "FY2023": 327417, "FY2022": 458905}),
    ("DATA", "Mortgages", {"FY2026": 44833297, "FY2025": 61413123, "FY2024": 63859773, "FY2023": 60906781, "FY2022": 47009328}),
    ("DATA", "Loans / SME Loans", {"FY2026": 101847611, "FY2025": 80625283, "FY2024": 61442178, "FY2023": 57584138, "FY2022": 49054178}),
    ("DATA", "Impairment provision", {"FY2026": -692585, "FY2025": -461764, "FY2024": -368454, "FY2023": -358999, "FY2022": -137981}),
    ("TOTAL", "Total loans and advances to customers", {"FY2026": 146696075, "FY2025": 142039997, "FY2024": 125748749, "FY2023": 118818336, "FY2022": 96522411}),
    ("SECTION", "Impairment provision roll-forward", {}),
    ("DATA", "Provision at 1 April", {"FY2026": 461764, "FY2025": 368454, "FY2024": 358999, "FY2023": 137981, "FY2022": 154363}),
    ("DATA", "Increase in impairment provision", {"FY2026": 230821, "FY2025": 93310, "FY2024": 9455, "FY2023": 221018}),
    ("DATA", "Release of impairment provision", {"FY2022": -16382}),
    ("TOTAL", "Provision at 31 March", {"FY2026": 692585, "FY2025": 461764, "FY2024": 368454, "FY2023": 358999, "FY2022": 137981}),
    ("SECTION", "Non-performing loans and advances to customers", {}),
    ("DATA", "Before provisions", {"FY2026": 2906004, "FY2025": 614575, "FY2024": 2153227, "FY2023": 1857399, "FY2022": 277279}),
    ("DATA", "Specific provision applied", {"FY2026": -543921, "FY2025": -361305, "FY2024": -168000, "FY2023": -106376, "FY2022": -2289}),
    ("TOTAL", "After provisions", {"FY2026": 2362083, "FY2025": 253270, "FY2024": 1985227, "FY2023": 1751023, "FY2022": 274990}),
    ("SECTION", "Derived ratios", {}),
    ("DATA", "NPL ratio (before provisions / gross loans)", {"FY2026": "1.98%", "FY2025": "0.43%", "FY2024": "1.71%", "FY2023": "1.56%", "FY2022": "0.29%"}),
    ("DATA", "Coverage ratio (provision / NPL before provisions)", {"FY2026": "23.84%", "FY2025": "75.13%", "FY2024": "17.11%", "FY2023": "19.33%", "FY2022": "49.76%"}),
]

RWA_SOURCES = (
    f"Reliance Bank Pillar 3 Disclosures 31 March 2023 (section 7.1, Standardised Approach to Credit Risk), {P3_2023_URL}\n"
    f"Reliance Bank Pillar 3 Disclosures 31 March 2022 (section 7.1, Standardised Approach to Credit Risk), {P3_2022_URL}\n"
    "No standalone Pillar 3 disclosure document for 31 March 2024, 2025 or 2026 was found on the Bank's website, "
    "in Companies House filings, or via the Wayback Machine (URL guesses against the FY2023 document's naming "
    "pattern also failed) - FY2024-FY2026 are left as an honest access gap, not a confirmed non-disclosure, "
    "queued for follow-up.\n"
    "SDDT DATE TEST (checked 2026-09-15) - this SPLITS those three years into two different categories. The "
    "PRA's 'Consolidated Waivers list for PRA-regulated firms - as of 1 July 2026' (bankofengland.co.uk/"
    "prudential-regulation/authorisations/waivers-and-modifications-of-rules) records that RELIANCE BANK LIMITED "
    "(FRN 204537) holds a 'Modification by Consent - PRA Rulebook - CRR Firms - Rule 3.1 of the SDDT Regime - "
    "General Application Part 3.1', sub-rule 'Ru 3.1', starting 05/04/2024 with no end date. That modification "
    "removes the Pillar 3 obligation outright - a stronger relief than UK CRR Article 433b, which only reduces "
    "frequency/content for small and non-complex institutions. The Bank's year-end is 31 March, stable across its "
    "Companies House accounts filing history (company 00068835). Therefore:\n"
    "  - FY2025 (y/e 31 March 2025) and FY2026 (y/e 31 March 2026) fall AFTER the modification took effect and "
    "are STRUCTURALLY EXEMPT. The absence of a Pillar 3 document for those years is expected rather than a "
    "sourcing failure, and is consistent with the FY2026 Annual Report's own reference to the simplified SDDT "
    "regime.\n"
    "  - FY2024 (y/e 31 March 2024) ends FIVE DAYS BEFORE the 05/04/2024 start date, so it PREDATES the relief "
    "and remains a GENUINE gap - the Bank was still subject to the disclosure obligation for that year. FY2024 is "
    "the only one of the three still worth chasing.\n"
    "Re-checked 2026-09-04 (ST-031 follow-up): a full Wayback Machine CDX crawl of every "
    "reliancebankltd.com/wp-content/uploads/* URL ever archived (2021-2026, 640+ files) turned up no Pillar 3 "
    "document later than 31 March 2023, and the FY2024, FY2025 and FY2026 Annual Report and Accounts (both the "
    "bank's own website PDFs and the Companies House filings, the latter OCR'd) were searched for risk-weighted-asset "
    "amounts and found to disclose none - the Strategic Report gives only the total capital requirement/TCR as a "
    "percentage, not an RWA or capital amount in £. Figures converted from the source's £'000 to £ for consistency "
    "with the rest of this workbook. Standardised approach to credit risk only - the Bank does not disclose market "
    "or operational risk RWA components separately, consistent with its stated minimal market risk exposure."
)
rwa_rows = [
    ("SECTION", "Standardised approach to credit risk - exposure and risk-weighted exposure", {}),
    ("DATA", "Central governments or central banks", {"FY2023": 0, "FY2022": 0}),
    ("DATA", "Financial institutions", {"FY2023": 6693000, "FY2022": 7008000}),
    ("DATA", "Covered bonds", {"FY2023": 1824000, "FY2022": 2432000}),
    ("DATA", "Corporates", {"FY2023": 0, "FY2022": 0}),
    ("DATA", "Retail", {"FY2023": 20000, "FY2022": 28000}),
    ("DATA", "Secured on real estate property", {"FY2023": 62925000, "FY2022": 50630000}),
    ("DATA", "Past due items", {"FY2023": 2627000, "FY2022": 243000}),
    ("DATA", "Other items", {"FY2023": 5736000, "FY2022": 6012000}),
    ("DATA", "Particularly high risk items (development loans)", {"FY2023": 3321000, "FY2022": 5429000}),
    ("TOTAL", "Total risk-weighted assets", {"FY2023": 83146000, "FY2022": 71782000}),
]

bw = BankWorkbook(bank_name="Reliance Bank Limited", years=YEARS, header_color="0F5B78")
bw.add_balance_sheet_sheet(
    title="Reliance Bank Limited - Entity Balance Sheet",
    subtitle="Entity basis, £; five latest available financial years FY2026-FY2022. See source note.",
    rows=bs_rows, sources_text=bw_bs_sources, first_col_width=70, source_height=220, unit_suffix=" (£)",
)
bw.add_income_statement_sheet(
    title="Reliance Bank Limited - Entity Income Statement",
    subtitle="Entity basis, £; five latest available financial years FY2026-FY2022. See source note.",
    rows=pl_rows, sources_text=PL_SOURCES, first_col_width=70, source_height=240, unit_suffix=" (£)",
)
bw.add_equity_changes_sheet(
    title="Reliance Bank Limited - Statement of Changes in Equity",
    subtitle="Entity basis, £; chronological roll-forward FY2022-FY2026. See source note.",
    headers=equity_headers, rows=equity_rows, sources_text=EQUITY_SOURCES, first_col_width=46, source_height=150,
)
rows = [
    ("SECTION", "Cash flows from operating activities", {}),
    ("DATA", "Profit/(loss) before tax / operating loss", {"FY2026": 1097804, "FY2025": 1431126, "FY2024": 1918412, "FY2023": 233945, "FY2022": -749645}),
    ("DATA", "Add back revaluation of investment property", {"FY2023": 128301}),
    ("DATA", "Movement in provision for bad debts", {"FY2026": 230821, "FY2025": 83855, "FY2024": 9455, "FY2023": -221048, "FY2022": 16412}),
    ("DATA", "Movement in value of debt securities/investments", {"FY2026": 169844, "FY2025": 372879, "FY2024": 386849, "FY2023": -813173, "FY2022": 179932}),
    ("DATA", "Amortisation of intangible fixed assets", {"FY2026": 71120, "FY2025": 116162, "FY2024": 175719, "FY2023": 202157, "FY2022": 203839}),
    ("DATA", "Depreciation of tangible fixed assets", {"FY2026": 370918, "FY2025": 373648, "FY2024": 262446, "FY2023": 163234, "FY2022": 156387}),
    ("DATA", "Other operating items included in reported subtotal (source arithmetic difference)", {"FY2026": 67891, "FY2022": 1}),
    ("DATA", "(Decrease)/increase in prepayments and accrued income", {"FY2026": 111310, "FY2025": -142965, "FY2024": -274, "FY2023": 54848, "FY2022": -34482}),
    ("DATA", "(Decrease)/increase in accruals and deferred income", {"FY2026": 0, "FY2025": -915795, "FY2024": 722273, "FY2023": 303630, "FY2022": -64396}),
    ("DATA", "(Decrease)/increase in other liabilities", {"FY2026": -132129, "FY2025": 8354, "FY2024": -13969, "FY2023": -7297, "FY2022": 26197}),
    ("DATA", "(Increase)/decrease in other assets", {"FY2026": -47072, "FY2025": -11150, "FY2024": -524, "FY2023": 9499, "FY2022": -4671}),
    ("TOTAL", "Cash flows from operating activities before changes in operating assets and liabilities", {"FY2026": 1940507, "FY2025": 1316114, "FY2024": 3460387, "FY2023": 54096, "FY2022": -270426}),
    ("DATA", "Increase in loans and advances to customers", {"FY2026": -4886899, "FY2025": -16375104, "FY2024": -6940602, "FY2023": -22074877, "FY2022": -19032850}),
    ("DATA", "Increase/(decrease) in customer accounts", {"FY2026": 12880730, "FY2025": -10991390, "FY2024": 22178943, "FY2023": -6162060, "FY2022": 4708736}),
    ("DATA", "Other operating items included in reported operating cash total (source arithmetic difference)", {"FY2026": -67891, "FY2022": 1}),
    ("TOTAL", "Net cash from/(used in) operating activities", {"FY2026": 9866447, "FY2025": -26050380, "FY2024": 18698728, "FY2023": -28182841, "FY2022": -14594539, "FY2021": 19788171, "FY2020": 7440459, "FY2019": -27420769}),
    ("SECTION", "Cash flows from investing activities", {}),
    ("DATA", "Sale and maturity of debt securities", {"FY2026": 66320081, "FY2025": 74717939, "FY2024": 54372721, "FY2023": 49694094, "FY2022": 33000000}),
    ("DATA", "Purchase of debt securities", {"FY2026": -83182860, "FY2025": -80507526, "FY2024": -47513462, "FY2023": -47661362, "FY2022": -26840989}),
    ("DATA", "Purchase of intangible fixed assets", {"FY2026": -23026, "FY2025": -143693, "FY2024": -39045, "FY2023": -43194, "FY2022": -254508}),
    ("DATA", "Purchase of tangible fixed assets", {"FY2026": -105786, "FY2025": -758943, "FY2024": -72957, "FY2023": -215926, "FY2022": -26765}),
    ("DATA", "Movement in interest on security deposit", {"FY2026": 840758, "FY2025": 4899, "FY2024": -23038, "FY2023": -7249}),
    ("DATA", "Net movement in loans and advances to banks not recoverable on demand", {"FY2022": 14498971}),
    ("TOTAL", "Net cash from/(used in) investing activities", {"FY2026": -16150833, "FY2025": -6687324, "FY2024": 6724219, "FY2023": 1766363, "FY2022": 20376709, "FY2021": 15545473, "FY2020": 12855842, "FY2019": 36459741}),
    ("SECTION", "Cash flows from financing activities", {}),
    ("DATA", "Issue of ordinary shares", {"FY2026": 5000000, "FY2023": 7000000, "FY2022": 3000000}),
    ("DATA", "Distribution to parent company/Salvation Army", {"FY2026": -400000, "FY2025": -100000, "FY2024": -100000}),
    ("TOTAL", "Net cash from/(used in) financing activities", {"FY2026": 4600000, "FY2025": -100000, "FY2024": -100000, "FY2023": 7000000, "FY2022": 3000000, "FY2021": 0, "FY2020": 1000000, "FY2019": 1500000}),
    ("TOTAL", "Increase/(decrease) in cash and cash equivalents", {"FY2026": -1684386, "FY2025": -32837704, "FY2024": 25322947, "FY2023": -19416478, "FY2022": 8782169, "FY2021": 35333644, "FY2020": 21296301, "FY2019": 10538972}),
    ("DATA", "Cash and cash equivalents at 1 April/beginning of reporting period", {"FY2026": 87080370, "FY2025": 119918074, "FY2024": 94595127, "FY2023": 114011605, "FY2022": 105229436, "FY2021": 69895792, "FY2020": 48599491, "FY2019": 38060520}),
    ("TOTAL", "Cash and cash equivalents at 31 March/end of reporting period", {"FY2026": 85395984, "FY2025": 87080370, "FY2024": 119918074, "FY2023": 94595127, "FY2022": 114011606, "FY2021": 105229436, "FY2020": 69895792, "FY2019": 48599492}),
]
bw.add_cash_flow_sheet(
    title="Reliance Bank Limited - Entity Cash Flow Statement",
    subtitle="Entity basis, £; five latest available financial years FY2026-FY2022. See source note.",
    rows=rows, sources_text=CASH_SOURCES, first_col_width=70, source_height=220, unit_suffix=" (£)",
)
bw.add_asset_quality_sheet(
    title="Reliance Bank Limited - Asset Quality",
    subtitle="Entity basis, £; five latest available financial years FY2026-FY2022. See source note.",
    rows=aq_rows, sources_text=AQ_SOURCES, first_col_width=64, source_height=200, unit_suffix=" (£)",
)

P3_SOURCES = (
    f"Reliance Bank Pillar 3 Disclosure for 31 March 2023, KM1/capital and risk disclosures, {P3_2023_URL}\n"
    f"Reliance Bank Pillar 3 Disclosure for 31 March 2022, KM1/capital and risk disclosures, {P3_2022_URL}\n"
    "Reliance Bank Annual Reports and Accounts FY2019-FY2026, Strategic Report capital/liquidity sections and KPI tables, "
    + "; ".join(AR_URLS[y] for y in YEARS) + "\n"
    "Text-layer copies on the Bank's own website, used for exact extraction where the Companies House filing is an "
    "image-only scan (the Companies House URLs above remain the filed-of-record source): "
    + "; ".join(f"{y} {AR_WEBSITE_URLS[y]}" for y in ["FY2026", "FY2025", "FY2024", "FY2023", "FY2022"]) + "\n"
    "Blank cells mean the metric was not explicitly disclosed; no capital amount, RWA, NSFR or MREL figure has been inferred. "
    "No standalone Pillar 3 disclosure document for 31 March 2024, 2025 or 2026 was found (Bank website, Companies House, "
    "Wayback Machine, and URL-pattern guesses all came up empty) - CET1 Capital/Total Capital/Total RWAs for those years are "
    "an honest access gap, not confirmed non-disclosure. Re-checked 2026-09-04 (ST-031 follow-up): a full Wayback Machine "
    "CDX crawl of the Bank's entire wp-content/uploads history (2021-2026) found no later Pillar 3 document, and the FY2024, "
    "FY2025 and FY2026 Annual Reports (website copies with a text layer for FY2024/FY2025; the FY2026 Companies House scan "
    "OCR'd) were checked directly for Tier 1 Capital, Total Capital, Total RWAs, NSFR and MREL Ratio figures - none of these "
    "five are given a £ amount or % in any of the three years' Annual Reports, only CET1 Ratio, Leverage Ratio, LCR and the "
    "TCR/OCR percentages (already captured on their own metric sheets or in the Strategic Report narrative).\n"
    "RE-CONFIRMED 2026-09-15 ON A CLEAN TEXT LAYER, not OCR. The 2026-09-04 negative above rested on OCR of the "
    "Companies House scan, which leaves room for a missed table. The Bank's own website copy of the FY2026 Annual "
    f"Report ({AR_WEBSITE_URLS['FY2026']}) was located by enumerating the site's WordPress media library and DOES "
    "carry a text layer (71 pages, 229,728 characters extracted). Searching that extraction for 'risk weighted', "
    "'risk-weighted', 'own funds', 'capital resources', 'Tier 1 capital', 'Tier 2', 'NSFR' and 'net stable' returns "
    "only narrative: the Strategic Report's CET1 ratio (21.8%, 2025: 19.9%), leverage ratio (13.3%, 2025: 11.4%), "
    "LCR, and the statement that 'the Bank's total capital requirement is currently 11.74% of risk weighted assets' "
    "- a REQUIREMENT expressed as a percentage, with no RWA amount anywhere to apply it to. The 'Capital' section "
    "of the Strategic Report (p.11) is entirely qualitative, describing 'a simple and high-quality capital "
    "structure, with the majority of its capital resources comprising CET1' without quantifying any of it. There is "
    "no capital-resources note in the financial statements: Note 17 is 'Called up share capital' only. The website "
    f"copies of FY2025 ({AR_WEBSITE_URLS['FY2025']}) and FY2024 ({AR_WEBSITE_URLS['FY2024']}) were extracted the "
    "same way (187,503 and 197,464 characters respectively) and give the same result even more starkly: across "
    "both entire documents the string 'risk weighted' occurs exactly ONCE each, and neither occurrence is an "
    "amount - FY2025's is 'the Bank's updated total capital requirement is now 11.74% of risk weighted assets' and "
    "FY2024's is the bullet 'Core Tier 1 Capital as a % of total risk weighted assets' defining what the ratio "
    "means. Neither report contains 'own funds', 'capital resources of', 'NSFR' or 'net stable funding' at all. So "
    "for ALL THREE of FY2024, FY2025 and FY2026 this is now a CONFIRMED NON-DISCLOSURE rather than an access gap - "
    "the documents exist, are fully machine-readable, and do not contain the figures. Deriving Total RWAs from CET1 capital / CET1 ratio is "
    "possible in principle but is the back-solve this project forbids (see build_alpha_bank_london.py and "
    "build_bank_mandiri_europe.py, where such values were withdrawn), and in any case CET1 capital itself is "
    "undisclosed for the year, so there is nothing to divide.\n"
    "FY2021 FIGURES SOURCED FROM THE FOLLOWING YEAR'S EDITION (added 2026-09-16, comparative-column sweep). "
    "The Bank published no Pillar 3 disclosure as at 31 March 2021, but the 31 March 2022 edition prints a full "
    "prior-year comparative column headed '2021' - section 2 'Summary of Key Metrics' (p.3) and section 3 "
    "'Capital Resources' (p.3, column headed '31 March 2021'). The FY2021 values on the CET1 Capital, Tier 1 "
    "Capital, Tier 1 Ratio, Total Capital and Total RWAs sheets are read from that comparative column, NOT from a "
    "FY2021 document, and each sheet's note says so. The edition was dated from its own cover ('Pillar 3 "
    "Disclosures / As at 31 March 2022') and running page footer, not from its filename or upload path (the URL "
    "carries a 2023 upload date). Document verified before reading: HTTP 200, Content-Type application/pdf, %PDF "
    "magic bytes, 524,698 bytes, 14 pages, clean text layer. Column alignment cross-checked rather than assumed: "
    "the 2022 edition's '2022' column and the 2023 edition's '2022' comparative column agree digit-for-digit on "
    "every line (CET1 Resources 13,952; RWAs 71,782; CET1 ratio 18.05%; leverage exposure 274,521 and 5.08%; "
    "HQLA 115,575; net cash outflow 18,809; LCR 605%; Capital Resources 14,443/(306)/14,137), so the headers are "
    "not off by one and NO RESTATEMENT of any kind was found between the two editions. Nothing was derived or "
    "back-solved: the FY2021 comparative column prints no NSFR, no MREL and no separate Tier 1 or Tier 2 line, so "
    "those sheets stay blank for FY2021."
)
def metric(name, unit, data, note=None, first_col_width=54, source_height=200):
    bw.add_metric_sheet(name, unit, data, P3_SOURCES, note=note, first_col_width=first_col_width,
                        source_height=source_height)

metric("CET1 Capital", "£", [("CET1 capital", {"FY2023": 20965000, "FY2022": 13952000, "FY2021": 11799000})], "£20,965,000 (FY2023) and £13,952,000 (FY2022) per the Pillar 3 Summary of Key Metrics table. FY2021 £11,799,000 added 2026-09-16: the Bank published no Pillar 3 as at 31 March 2021, and this figure is the 'Common Equity Tier 1 (CET1) Resources' line in the PRIOR-YEAR COMPARATIVE COLUMN (headed '2021', £'000s) of the FOLLOWING year's edition - Pillar 3 Disclosures as at 31 March 2022, section 2 'Summary of Key Metrics', p.3. A printed figure, not a derivation. FY2024-FY2026: not found - see RWA Breakdown sheet's access-gap note.")
metric("CET1 Ratio", "% of RWA", [("CET1 ratio", {"FY2026": "21.8%", "FY2025": "19.9%", "FY2024": "20.7%", "FY2023": "23.1%", "FY2022": "18.2%", "FY2021": "15.7%", "FY2020": "17.7%", "FY2019": "20.2%"})])
metric("Tier 1 Capital", "£", [("Tier 1 capital", {"FY2023": 20965000, "FY2022": 13952000, "FY2021": 11799000})],
       "Added 2026-09-12. Not labelled 'Tier 1' anywhere in the source: Reliance Bank's Pillar 3 uses its own "
       "'Summary of Key Metrics' table rather than the UK KM1 template, and that table has no Tier 1 row. The "
       "figure shown is the disclosed CET1 Resources amount, carried across because the Bank's own Pillar 3 "
       "states explicitly that it holds no other capital tier: 'The Bank has a very simple capital structure and "
       "all capital resources qualify as Common Equity Tier 1 capital (CET1)' (FY2023 disclosure, section 3, "
       "p.2) and 'All of Reliance Bank's capital resources are currently Common Equity Tier 1 capital' (section "
       "on TCR composition, p.6). With no AT1 in issue, Tier 1 = CET1 by definition - the same treatment applied "
       "to other all-CET1 banks in this workbook set, and a disclosed fact rather than an estimate. FY2024-FY2026: "
       "not found - see RWA Breakdown sheet's access-gap note. "
       "FY2021 £11,799,000 added 2026-09-16 from the PRIOR-YEAR COMPARATIVE COLUMN of the FOLLOWING year's edition "
       "(Pillar 3 Disclosures as at 31 March 2022, section 2 'Summary of Key Metrics', p.3, column headed '2021'), "
       "there being no 31 March 2021 edition. The no-AT1 basis is evidenced for FY2021 by that same document's "
       "section 3 Capital Resources table, whose '31 March 2021' column lists only CET1 components (Ordinary Share "
       "Capital 10,000 + Revaluation Reserve 1,258 + P&L Reserves 934 = 12,192 'CET1 capital prior to "
       "adjustments', less CRR adjustments (239) = Total Capital 11,953) with no Additional Tier 1 or Tier 2 line "
       "at all, and by section 6 (p.8), 'All of Reliance Bank's capital resources are currently Common Equity Tier "
       "1 capital'.")
metric("Tier 1 Ratio", "% of RWA", [("Tier 1 ratio", {"FY2026": "21.8%", "FY2025": "19.9%", "FY2024": "20.7%", "FY2023": "23.07%", "FY2022": "18.05%", "FY2021": "15.45%"})],
       "Added 2026-09-12 on the same basis as the Tier 1 Capital sheet (no AT1 in issue, so Tier 1 = CET1). "
       "These are the Pillar 3 'Summary of Key Metrics' table's own CET1 ratio figures (23.07% / 18.05%). Note "
       "they differ marginally from the CET1 Ratio sheet's FY2023/FY2022 values (23.1% / 18.2%), which come from "
       "the Annual Report's Strategic Report KPI table - the two documents state the same ratio to different "
       "precision and, for FY2022, on a slightly different year-end capital basis. Each sheet keeps its own "
       "source's figure rather than being force-reconciled. "
       "FY2024-FY2026 added 2026-09-15: no Pillar 3 disclosure exists for those years (the Bank's last published "
       "edition is the one as at 31 March 2023 - see the RWA Breakdown sheet's access-gap note, and note the "
       "FY2026 Annual Report's reference to the simplified SDDT regime), so these three years mirror the CET1 "
       "Ratio sheet's Annual-Report figures on the no-AT1 basis set out on the Tier 1 Capital sheet: with no AT1 "
       "in issue, Tier 1 Ratio is CET1 Ratio by definition. They are therefore Annual-Report-sourced and stated "
       "to 1 d.p., unlike the 2 d.p. Pillar 3 figures for FY2023/FY2022 above. "
       "FY2021 15.45% added 2026-09-16, superseding the previous 'blank before FY2022' note: it is the 'Common "
       "Equity Tier 1 ratio (%)' line in the PRIOR-YEAR COMPARATIVE COLUMN (headed '2021') of the FOLLOWING "
       "year's edition - Pillar 3 Disclosures as at 31 March 2022, section 2 'Summary of Key Metrics', p.3 - not "
       "from a FY2021 document, there being none. The no-AT1 basis for FY2021 is evidenced from the same "
       "document's section 3 comparative column, which lists CET1 components only (see the Tier 1 Capital sheet). "
       "It sits on this sheet's Pillar 3 series at 2 d.p. and is deliberately NOT reconciled with the CET1 Ratio "
       "sheet's Annual-Report FY2021 value of 15.7%.")
metric("Total Capital", "£", [("Total capital", {"FY2023": 21218000, "FY2022": 14137000, "FY2021": 11953000})], "£21,218,000 (FY2023) and £14,137,000 (FY2022) per the Pillar 3 Capital Resources table (CET1 capital prior to adjustments less CRR adjustments). FY2021 £11,953,000 added 2026-09-16: printed as the 'Total Capital' line in the PRIOR-YEAR COMPARATIVE COLUMN headed '31 March 2021' of the FOLLOWING year's edition - Pillar 3 Disclosures as at 31 March 2022, section 3 'Capital Resources', p.3 (12,192 CET1 capital prior to adjustments less (239) CRR adjustments). There is no 31 March 2021 edition; this is a printed figure in the 2022 edition, not a derivation. It exceeds the FY2021 CET1 Resources figure of £11,799,000 on the CET1 Capital sheet by £154,000, mirroring the same £185,000 gap in FY2022 between the Bank's two tables - the two are kept on separate sheets and deliberately not reconciled. FY2024-FY2026: not found - see RWA Breakdown sheet's access-gap note.")
metric("Total Capital Ratio", "% of RWA", [("Total capital ratio", {"FY2023": "25.5%", "FY2022": "19.7%", "FY2021": "15.9%", "FY2020": "17.9%", "FY2019": "20.2%"})], "FY2023/FY2022 are derived from disclosed Pillar 3 capital and RWAs; FY2021-FY2019 are directly disclosed in the annual-report Strategic Report (FY2021: 15.9%; FY2020: 17.9%; FY2019: 20.2%). The accounts also disclose total capital requirement (TCR), a distinct figure not substituted here. FY2024-FY2026: not found.")
metric("Total RWAs", "£", [("Total risk-weighted assets", {"FY2023": 83146000, "FY2022": 71782000, "FY2021": 71451000})], "£83,146,000 (FY2023) and £71,782,000 (FY2022) per the Pillar 3 Summary of Key Metrics table; ties to the RWA Breakdown sheet's standardised-approach total. FY2021 £71,451,000 added 2026-09-16: the 'Risk Weighted Assets' line in the PRIOR-YEAR COMPARATIVE COLUMN headed '2021' of the FOLLOWING year's edition - Pillar 3 Disclosures as at 31 March 2022, section 2 'Summary of Key Metrics', p.3. No 31 March 2021 edition exists. BASIS CAVEAT, checked explicitly rather than assumed: the Bank's 'Risk Weighted Assets' line is the STANDARDISED CREDIT-RISK total only. The FY2022 edition's section 7.1 credit-risk table (p.9) totals exactly 71,782 for 31 March 2022, matching the section 2 line digit for digit, and the same edition discloses market risk (section 8) and operational risk outside it. Consistent with that, the Bank's own printed CET1 ratios do NOT reproduce from these figures - 13,952/71,782 = 19.44% against a printed 18.05%, and 11,799/71,451 = 16.51% against a printed 15.45% - because the ratio denominator includes operational and market risk (implied roughly 5,514 and 4,918 respectively). Those implied amounts are NOT recorded anywhere in this workbook: they are back-solved and the Bank does not print them. FY2021 is placed on the same credit-risk-total basis as FY2022/FY2023 so the series is internally consistent. FY2024-FY2026: not found - see RWA Breakdown sheet's access-gap note.")
bw.add_rwa_breakdown_sheet(
    title="Reliance Bank Limited - RWA Breakdown",
    subtitle="Entity basis, £; standardised approach to credit risk, FY2023 and FY2022 only. See source note.",
    rows=rwa_rows, sources_text=RWA_SOURCES, first_col_width=58, source_height=200, unit_suffix=" (£)",
)
metric(
    "Leverage Ratio", "£'000 / %",
    [
        ("Leverage ratio EXCLUDING claims on central banks - Annual Report basis (FY2022 onward)",
         {"FY2026": "13.3%", "FY2025": "11.0%", "FY2024": "10.8%", "FY2023": "11.5%", "FY2022": "7.6%"}),
        ("Leverage ratio INCLUDING claims on central banks - Annual Report basis, 'capital as a % of total "
         "exposures' (pre-2022 UK framework; not comparable with the row above)",
         {"FY2021": "4.50%", "FY2020": "5.45%", "FY2019": "6.12%"}),
        ("Basel III leverage ratio INCLUDING claims on central banks - Pillar 3 basis",
         {"FY2023": "7.90%", "FY2022": "5.08%", "FY2021": "4.45%"}),
        ("Total Basel III leverage ratio exposure measure (£'000) - Pillar 3 basis",
         {"FY2023": 267687, "FY2022": 274521, "FY2021": 265321}),
    ],
    "RESOLVED 2026-09-16 BY A DEDICATED SOURCING PASS. A cross-bank leverage-basis sweep the same day had "
    "flagged this sheet twice - that the row label 'excluding claims on central banks' appeared in neither "
    "Pillar 3 edition, and that the figures 4.50% / 7.6% / 11.5% appeared in neither Pillar 3 edition either - "
    "and had withdrawn the label while leaving the figures alone. Both observations were correct about the "
    "PILLAR 3 documents and wrong about where the figures come from. THE FIGURES ARE THE BANK'S OWN ANNUAL "
    "REPORT DISCLOSURES, and the withdrawn label was the Bank's own wording for FY2022 onward. It was wrong "
    "only in having been applied to the whole row, pre-2022 years included. The row is now split by basis.\n"
    "TWO SERIES ON TWO BASES, BOTH SOURCED, NEITHER RECONCILED INTO THE OTHER.\n"
    "(A) ANNUAL REPORT SERIES, rows 1-2. Every figure was read this session from a text-layer PDF, and the two "
    "boundary figures were additionally read VISUALLY from the Companies House scans rendered at 170 dpi (not "
    "OCR'd) and match digit for digit. FY2019/FY2020: FY2020 Annual Report, KPI table p.10 (commentary 'Capital "
    "as a % of total exposures') and Strategic Report narrative p.11, 'As at 31 March 2020, the Bank's Leverage "
    "Ratio (capital as a percentage of total exposures) was 5.45% (2019: 6.12%)'. FY2021: FY2021 Annual Report, "
    "KPI table p.11 ('Capital as a % of total assets (not risk weighted)') and narrative p.12. FY2022: FY2022 "
    "Annual Report, Strategic Report CAPITAL section p.10. FY2023: FY2023 Annual Report, CAPITAL p.10, 'the "
    "Bank's Leverage Ratio (excluding claims on central banks) increased to 11.5% (2022: 7.6%)'. FY2024: FY2024 "
    "Annual Report p.11, same 'excluding claims on central banks' wording. FY2025: FY2025 Annual Report p.14. "
    "FY2026: FY2026 Annual Report p.15.\n"
    "(B) PILLAR 3 SERIES, rows 3-4, from the 'Summary of Key Metrics' table (section 2, p.3) of each of the two "
    "editions that exist. Reliance does not use the UK KM1 template, so there is no row 14b and no "
    "central-bank-exclusion line anywhere in either document; the template prints 'Basel III Leverage Ratio' "
    "and 'Total Basel III leverage ratio exposure measure' only.\n"
    "WHY THE FY2022 FIGURE SITS ON THE 'EXCLUDING' ROW, AND THE ONE CONFLICT IN THE SOURCES. The FY2022 Annual "
    "Report's own parenthetical still reads 'capital as a percentage of total exposures' - the pre-2022 "
    "wording - yet the FY2023 Annual Report re-presents that IDENTICAL 7.6% as its 2022 comparative directly "
    "under the heading 'excluding claims on central banks'. The Bank therefore carries one figure under two "
    "different basis labels, and the later, explicit statement is followed here. Both labels are recorded above "
    "rather than one being suppressed. The supporting evidence is the denominator, not the ratio: the Pillar 3 "
    "exposure measure (row 4) is 265,321 / 274,521 / 267,687 against total assets of 244,326 / 251,247 / 252,188 "
    "- it EXCEEDS total assets every year (off-balance-sheet commitments) and never falls, whereas excluding the "
    "Bank's central-bank balances of £73.9m / £91.3m / £83.3m would have cut it to roughly £191m / £183m / "
    "£184m. So the Pillar 3 denominator includes claims on central banks throughout, on one unbroken basis. "
    "Consistent with that, the two series AGREE at FY2021 (Annual Report 4.50% vs Pillar 3 4.45%, both "
    "including central banks) and diverge sharply from FY2022 onward (7.6% vs 5.08%, 11.5% vs 7.90%) - the "
    "signature of the UK framework's exclusion of central-bank claims from 1 January 2022 entering the Annual "
    "Report series but not the Pillar 3 one.\n"
    "YEAR ALIGNMENT WAS CHECKED, AND ONE SOURCE-SIDE TRAP WAS FOUND. The Pillar 3 columns are explicitly headed "
    "('2022 | 2021' and '2023 | 2022') and the shared 5.08% confirms the overlap, so that series is aligned. "
    "BUT THE FY2020 ANNUAL REPORT'S KPI TABLE HEADERS ARE OFF BY ONE YEAR: the table on p.10 is headed '2019' "
    "and '2018 (as stated)' while holding the FY2020 and FY2019 figures. Proof from the same document - the "
    "Capital narrative below it reads 'as at 31 March 2020 ... 17.7% (2019: 20.2%)' while the table's '2019' "
    "column shows 17.7% and its '2018 (as stated)' column 20.2%, and the p.11 narrative gives 5.45% for 31 "
    "March 2020 against 6.12% for 2019. Independently corroborated by the FY2021 Annual Report's KPI table, "
    "correctly headed '2021 | 2020', showing 4.50% / 5.45%. The assignment above is therefore correct; do NOT "
    "shift this series by a year to match that table's printed headers.\n"
    "FY2025 RESTATEMENT: the FY2025 Annual Report states 11% for its own year; the FY2026 Annual Report labels "
    "its 2025 comparative 11.4%. Both are on the 'excluding claims on central banks' basis. The own-year figure "
    "is retained per project convention and the cross-report difference is documented rather than applied.",
)
metric("LCR", "%", [("Liquidity Coverage Ratio", {"FY2026": "228%", "FY2025": "247%", "FY2024": "408%", "FY2023": "315%", "FY2022": "605%", "FY2021": "986%", "FY2020": "690%", "FY2019": "1100%"})],
       "Ratios are the Bank's year-end disclosures; FY2021-FY2019 are directly disclosed in the annual reports.\n"
       "FY2026 - THE SOURCE DOCUMENT CONTRADICTS ITSELF, and 228% is the right figure. Recorded here 2026-09-15 so "
       "that a future pass does not 'correct' this cell to 247%. The FY2026 Annual Report states the LCR twice and "
       "disagrees with itself: the Strategic Report (p.5) says it 'stood at 228% at year-end (2025: 247%)', while "
       "the Liquidity Risk note (p.68) says 'The Bank's LCR at 31 March 2026 was 247% (2025: 247%), this has "
       "decreased vs. last year'. The note is stale, and it is provably so on three independent grounds. (1) It "
       "contradicts itself in the same sentence - it prints an unchanged 247% while asserting the ratio "
       "'decreased'. (2) The same paragraph makes the identical mistake with a second figure: it says HQLA 'equates "
       "to 34.3% of total assets (2025: 34.3%)', but £82.5m of HQLA against the audited FY2026 total assets of "
       "£285,462,333 is 28.9%, not 34.3% - whereas £91.3m against FY2025's £266,650,946 is 34.2%, i.e. the FY2025 "
       "percentage has simply been repeated in the current-year slot. (3) The one number in that paragraph that "
       "WAS updated, HQLA falling from £91.3m to £82.5m, moves in the direction of a lower LCR, matching the "
       "Strategic Report and the note's own narrative. The Strategic Report figure is therefore used, and the note "
       "is treated as a current-year-column update failure affecting both its LCR and its HQLA percentage.")
metric("NSFR", "%", [("Net Stable Funding Ratio", {})], "Not publicly disclosed in the reviewed annual reports or 31 March 2023 Pillar 3 disclosure.")
metric("MREL Ratio", "%", [("MREL ratio", {})], "The reports describe the Bank as subject to an MREL requirement equal to its TCR/Pillar 1 and Pillar 2 requirements, but disclose no quantitative MREL ratio; no value is inferred.")

bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {"FY2026": 285462333, "FY2025": 266650946, "FY2024": 276893185, "FY2023": 252188264, "FY2022": 251247132, "FY2021": 244326240, "FY2020": 198450609, "FY2019": 184245691}),
        ("Loans and advances to customers", {"FY2026": 146696075, "FY2025": 142039997, "FY2024": 125748749, "FY2023": 118818336, "FY2022": 96522411, "FY2021": 77505973, "FY2020": 53204878, "FY2019": 47220230}),
        ("Customer accounts", {"FY2026": 254118275, "FY2025": 241237545, "FY2024": 252228935, "FY2023": 230049991, "FY2022": 236212051, "FY2021": 231503315, "FY2020": 186411063, "FY2019": 171635444}),
        ("Total equity", {"FY2026": 30556187, "FY2025": 24721622, "FY2024": 22999662, "FY2023": 21249653, "FY2022": 14442793, "FY2021": 12192437, "FY2020": 11652208, "FY2019": 12142972}),
    ],
    balance_sheet_unit="£",
    income_statement_totals=[
        ("Total interest income", {"FY2026": 13834883, "FY2025": 14351706, "FY2024": 11630100, "FY2023": 6777658, "FY2022": 3342104}),
        ("Operating income", {"FY2026": 9700259, "FY2025": 9577790, "FY2024": 9090242, "FY2023": 6115348, "FY2022": 3501910}),
        ("Total operating expense", {"FY2026": -8602455, "FY2025": -8146664, "FY2024": -7171830, "FY2023": -5881403, "FY2022": -4251554}),
        ("Profit/(loss) on activities after tax", {"FY2026": 869584, "FY2025": 1221144, "FY2024": 1850741, "FY2023": 127173, "FY2022": -608827, "FY2021": -1360807, "FY2020": -1490764, "FY2019": -647859}),
    ],
    income_statement_unit="£",
    equity_changes_totals=[
        ("Opening equity", {"FY2026": 24721622, "FY2025": 22999662, "FY2024": 21249653, "FY2023": 14442793, "FY2022": 12192437}),
        ("Total comprehensive income/(loss) for the year", {"FY2026": 1234565, "FY2025": 1821960, "FY2024": 1850741, "FY2023": -193139, "FY2022": -703945}),
        ("Other equity movements, net", {"FY2026": 4600000, "FY2025": -100000, "FY2024": -100732, "FY2023": 7000000, "FY2022": 2954301}),
        ("Closing equity", {"FY2026": 30556187, "FY2025": 24721622, "FY2024": 22999662, "FY2023": 21249653, "FY2022": 14442793}),
    ],
    equity_changes_unit="£",
    cash_flow_totals=[
        ("Net cash from/(used in) operating activities", {"FY2026": 9866447, "FY2025": -26050380, "FY2024": 18698728, "FY2023": -28182841, "FY2022": -14594539}),
        ("Net cash from/(used in) investing activities", {"FY2026": -16150833, "FY2025": -6687324, "FY2024": 6724219, "FY2023": 1766363, "FY2022": 20376709}),
        ("Net cash from/(used in) financing activities", {"FY2026": 4600000, "FY2025": -100000, "FY2024": -100000, "FY2023": 7000000, "FY2022": 3000000}),
        ("Cash and cash equivalents at end of reporting period", {"FY2026": 85395984, "FY2025": 87080370, "FY2024": 119918074, "FY2023": 94595127, "FY2022": 114011606, "FY2021": 105229436, "FY2020": 69895792, "FY2019": 48599492}),
    ],
    cash_flow_unit="£",
    ratios=[
        ("CET1 Ratio", {"FY2026": "21.8%", "FY2025": "19.9%", "FY2024": "20.7%", "FY2023": "23.1%", "FY2022": "18.2%"}),
        ("Leverage Ratio (excluding claims on central banks; Annual Report basis - see Leverage Ratio sheet)", {"FY2026": "13.3%", "FY2025": "11.0%", "FY2024": "10.8%", "FY2023": "11.5%", "FY2022": "7.6%"}),
        ("LCR", {"FY2026": "228%", "FY2025": "247%", "FY2024": "408%", "FY2023": "315%", "FY2022": "605%", "FY2021": "986%", "FY2020": "690%", "FY2019": "1100%"}),
    ],
    note="Entity-only cash flows. Regulatory ratios are disclosed on the Bank's regulatory basis. Blank cells mean "
         "not disclosed, not zero. The 2023 cash-flow comparative restatement is explained on the cash-flow sheet. "
         "The Leverage Ratio row above is shown on the 'excluding claims on central banks' basis only, for "
         "comparability: FY2021 and earlier were disclosed on the pre-2022 'capital as a % of total exposures' basis "
         "and are deliberately NOT carried here, and the Bank's Pillar 3 disclosures give a separate, lower Basel III "
         "leverage series on the including-central-banks basis. All three series, with their sources and the evidence "
         "for each basis, are on the Leverage Ratio sheet.",
)
bw.save("/Users/armaan/code/katalysis/banks/RELIANCE BANK FINANCIALS.xlsx")
