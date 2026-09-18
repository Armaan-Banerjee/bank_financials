import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook


YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021", "FY2020", "FY2019", "FY2018", "FY2017", "FY2016", "FY2015"]
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
# FY2015-FY2020 accounts were not retained on weatherbys.bank's own site (only ~5 years are kept
# live there); Companies House's filing history for company 02943300 holds the originally-filed
# Group accounts for every one of these years (HD-022 re-verification: each PDF below was
# downloaded, OCR'd — the CH copies are unindexed scanned images with no text layer — and the
# extracted Consolidated Balance Sheet/Income Statement/Statement of Changes in Equity/Cash Flow
# figures were cross-checked against the following year's comparative column, which agreed to the
# penny in every case bar isolated £1 OCR/rounding artefacts noted inline below).
CH_AR_URLS = {
    "FY2020": "https://find-and-update.company-information.service.gov.uk/company/02943300/filing-history/MzMxMjkxNjk5MmFkaXF6a2N4/document?format=pdf&download=0",
    "FY2019": "https://find-and-update.company-information.service.gov.uk/company/02943300/filing-history/MzI4MTYxMTM3NWFkaXF6a2N4/document?format=pdf&download=0",
    "FY2018": "https://find-and-update.company-information.service.gov.uk/company/02943300/filing-history/MzIzODIyOTM2NWFkaXF6a2N4/document?format=pdf&download=0",
    "FY2017": "https://find-and-update.company-information.service.gov.uk/company/02943300/filing-history/MzIwNzgwNDQ3MGFkaXF6a2N4/document?format=pdf&download=0",
    "FY2016": "https://find-and-update.company-information.service.gov.uk/company/02943300/filing-history/MzE3NTA2MDU3MmFkaXF6a2N4/document?format=pdf&download=0",
    "FY2015": "https://find-and-update.company-information.service.gov.uk/company/02943300/filing-history/MzE1MDMxNDcxNGFkaXF6a2N4/document?format=pdf&download=0",
}
# The FY2025 annual report is served from weatherbys.bank as a 301 redirect from the
# AR_URLS["FY2025"] page slug to this direct PDF; cited explicitly where FY2025 Pillar 3-style
# metrics are sourced from it, since no FY2025 Pillar 3 document exists (see FY2025_P3_NOTE).
AR2025_PDF_URL = "https://www.weatherbys.bank/app/uploads/2026/05/Weatherbys-Banking-Group-Annual-report-2025.pdf"
P3_URLS = {
    "FY2024": "https://www.weatherbys.bank/app/uploads/2025/04/Weatherbys-Bank-Pillar-3-Disclosures-2024.pdf",
    "FY2023": "https://weatherbys.bank/app/uploads/2024/05/Weatherbys-Bank-Pillar-3-Dislcosures-2023.pdf",
    "FY2022": "https://weatherbys.bank/app/uploads/2023/05/Weatherbys-Bank-Pillar-3-Dislcosures-2022.pdf",
    "FY2021": "https://www.weatherbys.bank/app/uploads/2022/05/Pillar-3-2021-v2.0-Weatherbys-Bank.pdf",
    "FY2020": "https://www.weatherbys.bank/app/uploads/2021/08/Pillar3-2020.pdf",
}
CH_URL = f"https://find-and-update.company-information.service.gov.uk/company/{COMPANY_NO}"
PRA_URL = "https://www.bankofengland.co.uk/prudential-regulation/authorisations/which-firms-does-the-pra-regulate"

PRE2021_NOTE = (
    "FY2015-FY2020 figures are sourced from Weatherbys Bank Limited's Companies-House-filed Group "
    "accounts (CH_AR_URLS above), not from weatherbys.bank (which retains only ~5 years of annual "
    "reports); no separate Pillar 3 disclosure document was located for FY2015-FY2019 (a single "
    "pre-2021 Pillar 3 PDF was found via the Wayback Machine, archived 2020-09-21, but the archive's "
    "own capture is truncated mid-file - 1,048,576 of 1,264,248 original bytes - and unrecoverable; "
    "this is a genuine access gap, not a disclosure gap, so those years' capital/RWA metric sheets are "
    "left blank rather than estimated. The intact FY2020 document does, however, include FY2019 "
    "comparative LCR (586%) and NSFR (207.6%), which are populated. FY2020's own Pillar 3 Disclosures document (Weatherbys Bank, "
    "Pillar3-2020.pdf) was independently located and is intact, so FY2020's Pillar 3 metrics ARE "
    "populated. Terminology note: Weatherbys' FY2020 Pillar 3 disclosure already reports capital under "
    "CRD IV/Basel III (CET1/Tier 1/Tier 2), not Basel II Tier 1/Total Capital-only terminology, so no "
    "Basel-II-era caveat applies to any extended year in this workbook."
)

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
    f"FY2022/FY2021: Annual Report & Accounts 2022, p.46 - {AR_URLS['FY2022']}; "
    f"FY2020/FY2019: Group accounts made up to 31 Dec 2020, p.34 (Consolidated statement of cash flows) - {CH_AR_URLS['FY2020']}; "
    f"FY2018/FY2017: Group accounts made up to 31 Dec 2018, pp.25-26 - {CH_AR_URLS['FY2018']}; "
    f"FY2016/FY2015: Group accounts made up to 31 Dec 2016, p.15 - {CH_AR_URLS['FY2016']}.\n\n"
    + ENTITY_NOTE
    + " The 2024 statement labels the financing section's subtotal as investing activities, but its placement and figures are the financing cash flows; the source presentation is retained with a corrected descriptive label."
    + " " + PRE2021_NOTE
    + " FY2015's own cash flow statement combines fixed-asset and debt-securities depreciation/amortisation "
    "into one line (GBP259k); it is placed in this workbook's 'Depreciation, impairment and amortisation of "
    "fixed assets' row, with 'Amortisation of debt securities' left blank for FY2015 only (all other years "
    "split the two). FY2016-FY2018 disclose a one-off 'Gain on Visa convertible preferred stock' adjustment "
    "(Visa Inc.'s 2016 acquisition of Visa Europe, which several UK banks including Weatherbys held preferred "
    "stock in) not present before or after those years. FY2020's own filed 'Cash from operations' subtotal "
    "(GBP104,053,076) exceeds the sum of its own listed adjustment lines (GBP104,043,076) by GBP10,000 - a "
    "small internal footing discrepancy in the source document, reproduced as-stated rather than forced to tie "
    "(all other years' subtotals reconcile to their component lines to within normal independent-rounding "
    "tolerance, +/-GBP2k)."
)

rows = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Profit for the financial year before exceptional items", {"FY2025": 19244, "FY2024": 18270, "FY2023": 24735, "FY2022": 11909, "FY2021": 5206, "FY2020": 1931, "FY2019": 6146, "FY2018": 6084, "FY2017": 4428, "FY2016": 4242, "FY2015": 5942}),
    ("DATA", "Exceptional items", {"FY2016": 1079}),
    ("DATA", "Depreciation, impairment and amortisation of fixed assets", {"FY2025": 7065, "FY2024": 4506, "FY2023": 2758, "FY2022": 2786, "FY2021": 2402, "FY2020": 1794, "FY2019": 1204, "FY2018": 1060, "FY2017": 805, "FY2016": 434, "FY2015": 259}),
    ("DATA", "Amortisation of debt securities", {"FY2025": -1870, "FY2024": -1138, "FY2023": 413, "FY2022": 443, "FY2021": 133, "FY2020": 63, "FY2019": 21, "FY2018": 51, "FY2017": 328, "FY2016": 379}),
    ("DATA", "Taxation expense", {"FY2025": 3830, "FY2024": 6306, "FY2023": 8348, "FY2022": 3504, "FY2021": 1596, "FY2020": 642, "FY2019": 1855, "FY2018": 1550, "FY2017": 1313, "FY2016": 1463, "FY2015": 1587}),
    ("DATA", "Increase in prepayments and accrued income", {"FY2025": -1508, "FY2024": -4032, "FY2023": -4930, "FY2022": -6282, "FY2021": -1055, "FY2020": -2, "FY2019": -450, "FY2018": -381, "FY2017": -900, "FY2016": 748, "FY2015": -157}),
    ("DATA", "Decrease/(increase) in trade and other debtors", {"FY2025": -678, "FY2024": 38, "FY2023": -201, "FY2022": -364, "FY2021": 20, "FY2020": -161, "FY2019": 39, "FY2018": 3283, "FY2017": -1142, "FY2016": -424, "FY2015": -39}),
    ("DATA", "Change in fair value of financial instruments", {"FY2025": 6430, "FY2024": -1624, "FY2023": 7216, "FY2022": -8619, "FY2021": -3069, "FY2020": 1355, "FY2019": 822, "FY2018": -136, "FY2017": -150, "FY2016": 252, "FY2015": -29}),
    ("DATA", "Movement in margin call", {"FY2025": -6550}),
    ("DATA", "Loss/(gain) on investments", {"FY2025": 20, "FY2024": 71, "FY2023": -17, "FY2022": 104, "FY2021": 3, "FY2020": 171, "FY2019": -386}),
    ("DATA", "Gain on Visa convertible preferred stock", {"FY2018": -51, "FY2017": -45, "FY2016": -185}),
    ("DATA", "Loss/(gain) on disposal of subsidiary/tangible fixed assets", {"FY2025": -10235}),
    ("DATA", "Change in trade and other creditors", {"FY2025": 2299, "FY2024": -2982, "FY2023": 11753, "FY2022": 2607, "FY2021": -496, "FY2020": -753, "FY2019": 428, "FY2018": -3665, "FY2017": -715, "FY2016": 367, "FY2015": 1166}),
    ("DATA", "Net decrease/(increase) in provisions", {"FY2025": -64, "FY2024": -1366, "FY2023": 5968, "FY2022": 2623, "FY2021": 1123, "FY2020": -766, "FY2019": 623, "FY2018": 613, "FY2017": 337, "FY2016": -241, "FY2015": 907}),
    ("DATA", "Increase/(decrease) in provision for bad and doubtful debts", {"FY2025": 1074, "FY2024": 46, "FY2023": 184, "FY2022": -25, "FY2021": -518, "FY2020": 2202, "FY2019": -80, "FY2018": 154, "FY2017": 539, "FY2016": 105, "FY2015": -27}),
    ("DATA", "Loss on sale of assets", {"FY2016": 1}),
    ("DATA", "(Loss)/gain on investment property", {"FY2016": 149, "FY2015": -1055}),
    ("DATA", "Net increase/(decrease) in deposits from customers", {"FY2025": 193121, "FY2024": 203231, "FY2023": -16626, "FY2022": 116590, "FY2021": 315834, "FY2020": 189410, "FY2019": 82977, "FY2018": 107417, "FY2017": 121483, "FY2016": 103297, "FY2015": 27022}),
    ("DATA", "Net increase in loans and advances to customers", {"FY2025": -138623, "FY2024": -38018, "FY2023": -46309, "FY2022": -30957, "FY2021": -65508, "FY2020": -91843, "FY2019": -114115, "FY2018": -87378, "FY2017": -60659, "FY2016": -50867, "FY2015": -43264}),
    ("TOTAL", "Cash from operations", {"FY2025": 73555, "FY2024": 183308, "FY2023": -6708, "FY2022": 94319, "FY2021": 255671, "FY2020": 104053, "FY2019": -20915, "FY2018": 28602, "FY2017": 65620, "FY2016": 60798, "FY2015": -7687}),
    ("DATA", "Taxation paid", {"FY2025": -4301, "FY2024": -5721, "FY2023": -5421, "FY2022": -2320, "FY2021": -678, "FY2020": -1389, "FY2019": -1621, "FY2018": -906, "FY2017": -983, "FY2016": -1694, "FY2015": -1166}),
    ("TOTAL", "Net cash generated/(used) from operating activities", {"FY2025": 69254, "FY2024": 177587, "FY2023": -12129, "FY2022": 91999, "FY2021": 254993, "FY2020": 102664, "FY2019": -22536, "FY2018": 27696, "FY2017": 64637, "FY2016": 59103, "FY2015": -8852}),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Sale of subsidiary undertaking", {"FY2025": 10552}),
    ("DATA", "Income from joint venture", {"FY2025": 400}),
    ("DATA", "Investment in joint venture", {"FY2023": -60, "FY2022": -280, "FY2021": -12, "FY2020": 2, "FY2019": -30, "FY2018": -60, "FY2017": 10, "FY2016": -6, "FY2015": -125}),
    ("DATA", "Loan repayment from joint venture", {"FY2017": 50, "FY2015": 50}),
    ("DATA", "Investment in unlisted equities", {"FY2016": -50}),
    ("DATA", "Purchase of investment securities", {"FY2025": -361092, "FY2024": -173844, "FY2023": -66857, "FY2022": -136837, "FY2021": -22148, "FY2020": -46838, "FY2019": -54873, "FY2018": -36761, "FY2017": -49361, "FY2016": -22097, "FY2015": -45893}),
    ("DATA", "Sale and maturities of investment securities", {"FY2025": 190722, "FY2024": 72330, "FY2023": 127951, "FY2022": 46415, "FY2021": 38649, "FY2020": 10610, "FY2019": 46304, "FY2018": 28430, "FY2017": 43790, "FY2016": 46600, "FY2015": 38000}),
    ("DATA", "Purchase of tangible fixed assets", {"FY2025": -4139, "FY2024": -2103, "FY2021": -3939, "FY2020": -1150, "FY2019": -3539, "FY2016": -2186, "FY2015": -3189}),
    ("DATA", "Purchase of intangible fixed assets", {"FY2025": -13123, "FY2024": -6502}),
    ("DATA", "Purchase of intangible/tangible fixed assets", {"FY2023": -7251, "FY2022": -6456, "FY2018": -1773, "FY2017": -1672}),
    ("TOTAL", "Net cash (used)/generated from investing activities", {"FY2025": -176680, "FY2024": -110119, "FY2023": 53783, "FY2022": -97158, "FY2021": 12550, "FY2020": -37377, "FY2019": -12138, "FY2018": -10165, "FY2017": -7183, "FY2016": 22261, "FY2015": -11156}),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Issue of contingent convertible securities", {"FY2023": 3000}),
    ("DATA", "Subordinated loan", {"FY2018": 10000}),
    ("DATA", "Equity dividends paid", {"FY2025": -11100, "FY2024": -5000, "FY2023": -5000, "FY2022": -2000, "FY2021": -1250, "FY2020": -250, "FY2019": -2050, "FY2018": -1750, "FY2017": -1250, "FY2016": -1520, "FY2015": -1140}),
    ("TOTAL", "Net cash (used)/generated from financing activities", {"FY2025": -11100, "FY2024": -5000, "FY2023": -2000, "FY2022": -2000, "FY2021": -1250, "FY2020": -250, "FY2019": -2050, "FY2018": 8250, "FY2017": -1250, "FY2016": -1520, "FY2015": -1140}),
    ("TOTAL", "Net increase/(decrease) in cash and cash equivalents", {"FY2025": -118526, "FY2024": 62468, "FY2023": 39654, "FY2022": -7159, "FY2021": 266293, "FY2020": 65038, "FY2019": -36724, "FY2018": 25781, "FY2017": 56204, "FY2016": 79844, "FY2015": -21148}),
    ("DATA", "Cash and cash equivalents at beginning of year", {"FY2025": 687343, "FY2024": 624875, "FY2023": 585221, "FY2022": 592380, "FY2021": 326087, "FY2020": 261050, "FY2019": 297773, "FY2018": 271992, "FY2017": 215788, "FY2016": 135944, "FY2015": 157092}),
    ("TOTAL", "Cash and cash equivalents at end of year", {"FY2025": 568817, "FY2024": 687343, "FY2023": 624875, "FY2022": 585221, "FY2021": 592380, "FY2020": 326087, "FY2019": 261050, "FY2018": 297773, "FY2017": 271992, "FY2016": 215788, "FY2015": 135944}),
]

AR2024_OWN_URL = AR_URLS["FY2024"]

DEBT_SECURITIES_NOTE = (
    "DEBT SECURITIES MEASUREMENT BASIS: Note 32 'Financial instruments' of each Annual Report (the "
    "table of financial assets/liabilities by IFRS 9 measurement category) states 'Debt Securities' is "
    "entirely within 'Instruments measured at amortised cost' - not fair value through OCI or fair value "
    "through profit or loss - confirmed identically in AR2024 (p.71, FY2024/FY2023 columns: GBP248,749k/"
    f"GBP146,097k - {AR_URLS['FY2024']}) and AR2022 (Note 32, FY2022/FY2021 columns: GBP207,605k/GBP117,625k "
    f"- {AR_URLS['FY2022']}). No note discloses a further split of the balance by issuer type (UK "
    "government gilts/treasury bills/sovereign vs supranational/corporate/other) in any year reviewed - "
    "Note 17 'Debt securities' only reconciles cost, premiums/discounts and book value, and the maturity-"
    "gap table (Note 33) breaks the balance down by remaining term, not issuer, so the label below is a "
    "relabel of the existing single line (measurement basis only), not a multi-row split. FY2015-FY2020 "
    "are Companies House scanned-image filings with no machine-readable Note 32 equivalent to verify "
    "against; given the consistent 'amortised cost' classification across every machine-readable year "
    "(FY2021-FY2025) and no indication of a change in accounting policy, the same measurement basis is "
    "assumed - not independently re-verified - for FY2015-FY2020."
)

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
    f"FY2022/FY2021: Annual Report & Accounts 2022, p.42 - {AR_URLS['FY2022']}; "
    f"FY2020/FY2019: Group accounts made up to 31 Dec 2020, p.28 (Consolidated balance sheet) - {CH_AR_URLS['FY2020']}; "
    f"FY2018/FY2017: Group accounts made up to 31 Dec 2018, p.20 - {CH_AR_URLS['FY2018']}; "
    f"FY2016/FY2015: Group accounts made up to 31 Dec 2016, p.10 (2015 shown restated per note 34; "
    f"the FY2015 filing's own p.10 reports the same total, see BS_RESTATEMENT_NOTE) - {CH_AR_URLS['FY2016']} "
    f"and (FY2015's own filing) {CH_AR_URLS['FY2015']}.\n\n"
    + ENTITY_NOTE
    + " " + BS_RESTATEMENT_NOTE
    + " " + PRE2021_NOTE
    + " FY2016's Group accounts restate FY2015's comparative balance sheet (note 34) splitting the "
    "single 'Tangible fixed assets' line (GBP7,942,105k combined, as FY2015's own filing shows it, net "
    "of the GBP50k Subordinated term loan asset) into separate Intangible/Tangible fixed asset lines "
    "(GBP3,079,139/GBP4,812,966) with an identical combined total and no equity impact; this workbook "
    "uses that split for FY2015 for structural consistency with all other years' Balance Sheet rows. "
    "'Subordinated term loan' (an asset, GBP50k, FY2015-FY2016 only) is a small third-party loan note "
    "the Group held, unrelated to the GBP10m Tier 2 'Subordinated loan' liability the Bank itself issued "
    "in 2018 (see FY2018's Cash Flow Statement). 'Provisions for liabilities' (a small liability-side "
    "balance, FY2015-FY2018 only) was not separately disclosed on the Balance Sheet from FY2019 onward."
    + " " + DEBT_SECURITIES_NOTE
)

bs_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash at banks / Loans and advances to banks", {"FY2025": 575367, "FY2024": 687343, "FY2023": 624875, "FY2022": 585221, "FY2021": 592380, "FY2020": 326087, "FY2019": 261050, "FY2018": 297773, "FY2017": 271992, "FY2016": 215788, "FY2015": 135944}),
    ("DATA", "Derivative financial assets", {"FY2025": 1394, "FY2024": 5018, "FY2023": 5194, "FY2022": 9813, "FY2021": 961, "FY2020": 30, "FY2019": 265, "FY2018": 377, "FY2017": 81, "FY2016": 37, "FY2015": 16}),
    ("DATA", "Loans and advances to customers", {"FY2025": 1006160, "FY2024": 859672, "FY2023": 821700, "FY2022": 775573, "FY2021": 744591, "FY2020": 678564, "FY2019": 588924, "FY2018": 474728, "FY2017": 387504, "FY2016": 327384, "FY2015": 276621}),
    ("DATA", "Debt securities (measured at amortised cost)", {"FY2025": 420989, "FY2024": 248749, "FY2023": 146097, "FY2022": 207605, "FY2021": 117625, "FY2020": 134258, "FY2019": 98093, "FY2018": 89545, "FY2017": 81265, "FY2016": 76021, "FY2015": 100903}),
    ("DATA", "Investment in joint venture", {"FY2024": 670, "FY2023": 670, "FY2022": 610, "FY2021": 330, "FY2020": 318, "FY2019": 320, "FY2018": 290, "FY2017": 230, "FY2016": 240, "FY2015": 234}),
    ("DATA", "Subordinated term loan (Group's own asset, unrelated to the Tier 2 liability below)", {"FY2016": 50, "FY2015": 50}),
    ("DATA", "Investments", {"FY2025": 364, "FY2024": 384, "FY2023": 455, "FY2022": 438, "FY2021": 542, "FY2020": 546, "FY2019": 717, "FY2018": 331, "FY2017": 280, "FY2016": 235}),
    ("DATA", "Intangible fixed assets", {"FY2025": 24676, "FY2024": 16194, "FY2023": 12327, "FY2022": 6145, "FY2021": 3154, "FY2020": 1822, "FY2019": 1827, "FY2018": 2134, "FY2017": 2436, "FY2016": 4621, "FY2015": 3079}),
    ("DATA", "Tangible fixed assets", {"FY2025": 10936, "FY2024": 9397, "FY2023": 9283, "FY2022": 11216, "FY2021": 10747, "FY2020": 10085, "FY2019": 11341, "FY2018": 9035, "FY2017": 7993, "FY2016": 4930, "FY2015": 4813}),
    ("DATA", "Other assets", {"FY2025": 2753, "FY2024": 1875, "FY2023": 1913, "FY2022": 1711, "FY2021": 1803, "FY2020": 1823, "FY2019": 1672, "FY2018": 1711, "FY2017": 4994, "FY2016": 4090, "FY2015": 3791}),
    ("DATA", "Prepayments and accrued income", {"FY2025": 10808, "FY2024": 19192, "FY2023": 15160, "FY2022": 10232, "FY2021": 3950, "FY2020": 2896, "FY2019": 2894, "FY2018": 2443, "FY2017": 2063, "FY2016": 1163, "FY2015": 1911}),
    ("TOTAL", "Total assets", {"FY2025": 2053447, "FY2024": 1848494, "FY2023": 1637674, "FY2022": 1608564, "FY2021": 1476083, "FY2020": 1156429, "FY2019": 967101, "FY2018": 878368, "FY2017": 758839, "FY2016": 634559, "FY2015": 527361}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Derivative financial liabilities", {"FY2025": 4075, "FY2024": 1269, "FY2023": 3069, "FY2022": 472, "FY2021": 238, "FY2020": 2377, "FY2019": 1258, "FY2018": 547, "FY2017": 387, "FY2016": 493, "FY2015": 220}),
    ("DATA", "Customer accounts", {"FY2025": 1905431, "FY2024": 1707796, "FY2023": 1504566, "FY2022": 1521191, "FY2021": 1404601, "FY2020": 1088767, "FY2019": 899358, "FY2018": 816380, "FY2017": 708964, "FY2016": 587481, "FY2015": 484184}),
    ("DATA", "Other liabilities", {"FY2025": 12734, "FY2024": 18287, "FY2023": 22583, "FY2022": 7903, "FY2021": 4568, "FY2020": 4147, "FY2019": 5646, "FY2018": 4984, "FY2017": 8006, "FY2016": 8629, "FY2015": 8617}),
    ("DATA", "Accruals and deferred income", {"FY2025": 10093, "FY2024": 11099, "FY2023": 12465, "FY2022": 6498, "FY2021": 3876, "FY2020": 2752, "FY2019": 3518, "FY2018": 2887, "FY2017": 2266, "FY2016": 1912, "FY2015": 2133}),
    ("DATA", "Subordinated loan", {"FY2025": 10000, "FY2024": 10000, "FY2023": 10000, "FY2022": 10000, "FY2021": 10000, "FY2020": 10000, "FY2019": 10000, "FY2018": 10000}),
    ("DATA", "Provisions for liabilities", {"FY2018": 8, "FY2017": 16, "FY2016": 32, "FY2015": 53}),
    ("TOTAL", "Total liabilities", {"FY2025": 1942333, "FY2024": 1748451, "FY2023": 1552683, "FY2022": 1546064, "FY2021": 1423283, "FY2020": 1108043, "FY2019": 919779, "FY2018": 834806, "FY2017": 719637, "FY2016": 598547, "FY2015": 495207}),
    ("SECTION", "Shareholders' funds", {}),
    ("DATA", "Called up share capital", {"FY2025": 7000, "FY2024": 7000, "FY2023": 7000, "FY2022": 7000, "FY2021": 7000, "FY2020": 7000, "FY2019": 7000, "FY2018": 7000, "FY2017": 7000, "FY2016": 7000, "FY2015": 7000}),
    ("DATA", "Contingent convertible securities", {"FY2025": 3000, "FY2024": 3000, "FY2023": 3000}),
    ("DATA", "Revaluation reserve", {"FY2025": 231, "FY2024": 404, "FY2023": 522, "FY2022": 766, "FY2021": 975, "FY2020": 517, "FY2019": 1133, "FY2018": 1470, "FY2017": 1443, "FY2016": 1432, "FY2015": 1374}),
    ("DATA", "Profit and loss account", {"FY2025": 100883, "FY2024": 89639, "FY2023": 74469, "FY2022": 54734, "FY2021": 44825, "FY2020": 40869, "FY2019": 39188, "FY2018": 35092, "FY2017": 30758, "FY2016": 27581, "FY2015": 23780}),
    ("TOTAL", "Total equity", {"FY2025": 111114, "FY2024": 100043, "FY2023": 84991, "FY2022": 62500, "FY2021": 52800, "FY2020": 48386, "FY2019": 47322, "FY2018": 43562, "FY2017": 39201, "FY2016": 36012, "FY2015": 32154}),
    ("TOTAL", "Total liabilities and equity", {"FY2025": 2053447, "FY2024": 1848494, "FY2023": 1637674, "FY2022": 1608564, "FY2021": 1476083, "FY2020": 1156429, "FY2019": 967101, "FY2018": 878368, "FY2017": 758839, "FY2016": 634559, "FY2015": 527361}),
]

PL_SOURCES = (
    "Sources - Weatherbys Banking Group consolidated income statement, GBP'000: "
    f"FY2025: Annual Report and Financial Accounts 2025, p.58 - {AR_URLS['FY2025']}; "
    f"FY2024: Annual Report & Accounts 2024, p.39 - {AR2024_OWN_URL}; "
    f"FY2023: Annual Report & Accounts 2023, pp.44-45 - {AR_URLS['FY2023']}; "
    f"FY2022/FY2021: Annual Report & Accounts 2022, p.40 - {AR_URLS['FY2022']}; "
    f"FY2020/FY2019: Group accounts made up to 31 Dec 2020, p.26 (Consolidated income statement) - {CH_AR_URLS['FY2020']}; "
    f"FY2018/FY2017: Group accounts made up to 31 Dec 2018, p.18 - {CH_AR_URLS['FY2018']}; "
    f"FY2016/FY2015: Group accounts made up to 31 Dec 2016, p.8 - {CH_AR_URLS['FY2016']}.\n\n"
    + ENTITY_NOTE
    + " FY2025's exceptional item is a £10,238k gain (sale of subsidiary/tangible fixed assets, matching the "
    "Cash Flow Statement's disposal line); FY2024's exceptional item is a £2,128k charge; FY2016's exceptional "
    "item is a £1,079k gain (per its own income statement, no further breakdown given); FY2023/FY2022/FY2021/"
    "FY2020/FY2019/FY2018/FY2017/FY2015 had no exceptional item line. FY2023 additionally discloses a small "
    "Rent Receivable line (£84k); FY2015-FY2020 all disclose a Rent Receivable line too (this stopped being "
    "separately reported FY2021-FY2022, briefly resumed FY2023, then stopped again). "
    + PRE2021_NOTE
    + " FY2015-FY2020's income statements break Fees and commissions receivable into a gross 'Group and share "
    "of joint venture' figure less a 'Less: share of joint venture' deduction, arriving at the net Fees and "
    "commissions receivable figure this workbook's row of that name always shows (FY2021 onward's income "
    "statement no longer discloses that gross/deduction split, only the net-equivalent figure - the JV's "
    "operating-profit share is instead only shown via the separate 'Share of operating profit in joint venture' "
    "line, present in all years). FY2015/FY2016 uniquely disclose a '(Loss)/Gain on investment property' line "
    "(the Bank held an investment property in those years); FY2015-FY2019 uniquely disclose an 'Other "
    "provisions for liabilities' line (a small non-loan provision movement) that is nil/not separately shown "
    "from FY2020 onward."
)

pl_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest receivable - arising from debt securities", {"FY2025": 12442, "FY2024": 12235, "FY2023": 8846, "FY2022": 2642, "FY2021": 655, "FY2020": 766, "FY2019": 1147, "FY2018": 804, "FY2017": 758, "FY2016": 762, "FY2015": 974}),
    ("DATA", "Interest receivable - other interest and similar income", {"FY2025": 102751, "FY2024": 104058, "FY2023": 93591, "FY2022": 51278, "FY2021": 35361, "FY2020": 33377, "FY2019": 30938, "FY2018": 25935, "FY2017": 21645, "FY2016": 18852, "FY2015": 17024}),
    ("DATA", "Interest payable", {"FY2025": -36240, "FY2024": -37279, "FY2023": -24283, "FY2022": -4733, "FY2021": -3996, "FY2020": -4706, "FY2019": -3564, "FY2018": -2788, "FY2017": -2559, "FY2016": -2377, "FY2015": -2923}),
    ("TOTAL", "Net interest income", {"FY2025": 78953, "FY2024": 79014, "FY2023": 78154, "FY2022": 49187, "FY2021": 32020, "FY2020": 29437, "FY2019": 28521, "FY2018": 23951, "FY2017": 19845, "FY2016": 17237, "FY2015": 15074}),
    ("DATA", "Fees and commissions receivable: Group and share of joint venture (gross, FY2015-FY2020 only)", {"FY2020": 5770, "FY2019": 6826, "FY2018": 6079, "FY2017": 5670, "FY2016": 4944, "FY2015": 4562}),
    ("DATA", "Less: share of joint venture (fees, FY2015-FY2020 only)", {"FY2020": -1493, "FY2019": -1698, "FY2018": -1453, "FY2017": -1274, "FY2016": -1149, "FY2015": -923}),
    ("DATA", "Fees and commissions receivable", {"FY2025": 8973, "FY2024": 7852, "FY2023": 6796, "FY2022": 5862, "FY2021": 5118, "FY2020": 4278, "FY2019": 5127, "FY2018": 4627, "FY2017": 4396, "FY2016": 3795, "FY2015": 3639}),
    ("DATA", "Fees and commissions payable", {"FY2025": -1130, "FY2024": -942, "FY2023": -615, "FY2022": -546, "FY2021": -493, "FY2020": -673, "FY2019": -685, "FY2018": -539, "FY2017": -380, "FY2016": -385, "FY2015": -518}),
    ("DATA", "Rent receivable", {"FY2023": 84, "FY2020": 130, "FY2019": 310, "FY2018": 310, "FY2017": 310, "FY2016": 310, "FY2015": 363}),
    ("DATA", "Other operating income", {"FY2025": 4299, "FY2024": 4502, "FY2023": 4007, "FY2022": 3526, "FY2021": 3130, "FY2020": 2523, "FY2019": 2697, "FY2018": 2440, "FY2017": 2211, "FY2016": 2064, "FY2015": 1944}),
    ("TOTAL", "Operating income", {"FY2025": 91095, "FY2024": 90426, "FY2023": 88426, "FY2022": 58029, "FY2021": 39775, "FY2020": 35695, "FY2019": 35970, "FY2018": 30789, "FY2017": 26382, "FY2016": 23021, "FY2015": 20502}),
    ("SECTION", "Operating expenses", {}),
    ("DATA", "(Loss)/gain on value of derivatives", {"FY2025": -673, "FY2024": 117, "FY2023": 75, "FY2022": 76, "FY2021": 2362, "FY2020": -1355, "FY2019": -822, "FY2018": 136, "FY2017": 150, "FY2016": -252, "FY2015": 29}),
    ("DATA", "(Loss)/Gain on investment property", {"FY2016": -149, "FY2015": 1055}),
    ("DATA", "Administrative expenses", {"FY2025": -65873, "FY2024": -55163, "FY2023": -50274, "FY2022": -39014, "FY2021": -31654, "FY2020": -26942, "FY2019": -25426, "FY2018": -21661, "FY2017": -19315, "FY2016": -16391, "FY2015": -13534}),
    ("DATA", "Depreciation and amortisation", {"FY2025": -7065, "FY2024": -4505, "FY2023": -2758, "FY2022": -2786, "FY2021": -2402, "FY2020": -1794, "FY2019": -1204, "FY2018": -1060, "FY2017": -805, "FY2016": -434, "FY2015": -115}),
    # Not itself a printed AR subtotal - the sum of Administrative expenses +
    # Depreciation and amortisation above. Excludes the derivative/investment
    # property valuation movements, credit impairment charge, and joint
    # venture share above/below per standard cost-to-income convention
    # (operating costs only, not credit risk or valuation items).
    ("TOTAL", "Total operating expenses (sum of Administrative expenses + Depreciation and amortisation - excludes derivative/property valuation movements, credit impairment, and joint venture share)", {"FY2025": -72938, "FY2024": -59668, "FY2023": -53032, "FY2022": -41800, "FY2021": -34056, "FY2020": -28736, "FY2019": -26630, "FY2018": -22721, "FY2017": -20120, "FY2016": -16825, "FY2015": -13649}),
    ("DATA", "Impairment charge on loans and advances", {"FY2025": -4648, "FY2024": -4571, "FY2023": -2784, "FY2022": -1400, "FY2021": -1559, "FY2020": -3298, "FY2019": -795, "FY2018": -809, "FY2017": -836, "FY2016": -250, "FY2015": -497}),
    ("DATA", "Other provisions for liabilities", {"FY2019": 8, "FY2018": 0, "FY2017": -15, "FY2016": -30, "FY2015": -95}),
    ("DATA", "Share of operating profit in joint venture", {"FY2024": 400, "FY2023": 400, "FY2022": 340, "FY2021": 280, "FY2020": 268, "FY2019": 270, "FY2018": 240, "FY2017": 180, "FY2016": 190, "FY2015": 184}),
    ("TOTAL", "Operating profit before exceptional items and tax", {"FY2025": 12836, "FY2024": 26704, "FY2023": 33085, "FY2022": 15245, "FY2021": 6802, "FY2020": 2573, "FY2019": 8001, "FY2018": 7634, "FY2017": 5740, "FY2016": 5705, "FY2015": 7529}),
    ("DATA", "Exceptional item", {"FY2025": 10238, "FY2024": -2128, "FY2016": 1079}),
    ("TOTAL", "Operating profit before tax", {"FY2025": 23074, "FY2024": 24576, "FY2023": 33085, "FY2022": 15245, "FY2021": 6802, "FY2020": 2573, "FY2019": 8001, "FY2018": 7634, "FY2017": 5740, "FY2016": 6784, "FY2015": 7529}),
    ("DATA", "Taxation on profit", {"FY2025": -3830, "FY2024": -6306, "FY2023": -8350, "FY2022": -3336, "FY2021": -1596, "FY2020": -642, "FY2019": -1855, "FY2018": -1550, "FY2017": -1313, "FY2016": -1463, "FY2015": -1587}),
    ("TOTAL", "Profit for the financial year", {"FY2025": 19244, "FY2024": 18270, "FY2023": 24735, "FY2022": 11909, "FY2021": 5206, "FY2020": 1931, "FY2019": 6146, "FY2018": 6084, "FY2017": 4428, "FY2016": 5321, "FY2015": 5942}),
    ("SECTION", "Other comprehensive income", {}),
    ("DATA", "Revaluation of tangible fixed assets", {"FY2025": -173, "FY2024": -118, "FY2023": -244, "FY2022": -209, "FY2021": 458, "FY2020": -617, "FY2019": -336, "FY2018": 27, "FY2017": 11, "FY2016": 58, "FY2015": 338}),
    ("TOTAL", "Total comprehensive income for the year", {"FY2025": 19071, "FY2024": 18152, "FY2023": 24491, "FY2022": 11700, "FY2021": 5664, "FY2020": 1314, "FY2019": 5810, "FY2018": 6111, "FY2017": 4439, "FY2016": 5379, "FY2015": 6280}),
]

EQ_SOURCES = (
    "Sources - Weatherbys Banking Group consolidated statement of changes in equity, GBP'000: "
    f"AR2025, p.62 - {AR_URLS['FY2025']}; AR2024, p.43 - {AR2024_OWN_URL}; AR2023, p.48 - {AR_URLS['FY2023']}; "
    f"AR2022, p.44 - {AR_URLS['FY2022']}; "
    f"FY2020/FY2019: Group accounts made up to 31 Dec 2020, pp.29-30 - {CH_AR_URLS['FY2020']}; "
    f"FY2018/FY2017: Group accounts made up to 31 Dec 2018, pp.22-23 - {CH_AR_URLS['FY2018']}; "
    f"FY2016/FY2015: Group accounts made up to 31 Dec 2016, pp.12-13 - {CH_AR_URLS['FY2016']}.\n\n"
    + ENTITY_NOTE
    + " Every year's closing balance ties exactly to the next year's opening balance and to that year's own "
    "Balance Sheet Total equity - zero undocumented plug rows, all the way back to 1 January 2015 (which "
    "itself ties to FY2014's own closing balance, one year beyond this workbook's floor, per the FY2015 Group "
    "accounts' own comparative column). Contingent Convertible Securities first appear in FY2023 (a £3,000k "
    "issuance). " + PRE2021_NOTE
)

eq_headers = ["Share capital", "Contingent Convertible Securities", "Revaluation reserve", "Profit & loss account", "Total equity"]
eq_rows = [
    ("DATA", "1 January 2015", (7000, None, 1036, 18978, 27014)),
    ("DATA", "Profit for the year", (None, None, None, 5942, 5942)),
    ("DATA", "Revaluation of non-investment property", (None, None, 338, None, 338)),
    ("TOTAL", "Total comprehensive income for the year", (None, None, 338, 5942, 6280)),
    ("DATA", "Dividends", (None, None, None, -1140, -1140)),
    ("TOTAL", "31 December 2015", (7000, None, 1374, 23780, 32154)),
    ("DATA", "Profit for the year", (None, None, None, 5321, 5321)),
    ("DATA", "Revaluation of non-investment property", (None, None, 58, None, 58)),
    ("TOTAL", "Total comprehensive income for the year", (None, None, 58, 5321, 5379)),
    ("DATA", "Dividends", (None, None, None, -1520, -1520)),
    ("TOTAL", "31 December 2016", (7000, None, 1432, 27581, 36012)),
    ("DATA", "Profit for the year", (None, None, None, 4428, 4428)),
    ("DATA", "Revaluation of tangible fixed assets", (None, None, 11, None, 11)),
    ("TOTAL", "Total comprehensive income for the year", (None, None, 11, 4428, 4439)),
    ("DATA", "Dividends", (None, None, None, -1250, -1250)),
    ("TOTAL", "31 December 2017", (7000, None, 1443, 30758, 39201)),
    ("DATA", "Profit for the year", (None, None, None, 6084, 6084)),
    ("DATA", "Revaluation of tangible fixed assets", (None, None, 27, None, 27)),
    ("TOTAL", "Total comprehensive income for the year", (None, None, 27, 6084, 6111)),
    ("DATA", "Dividends", (None, None, None, -1750, -1750)),
    ("TOTAL", "31 December 2018", (7000, None, 1470, 35092, 43562)),
    ("DATA", "Profit for the year", (None, None, None, 6146, 6146)),
    ("DATA", "Revaluation of tangible fixed assets", (None, None, -336, None, -336)),
    ("TOTAL", "Total comprehensive income for the year", (None, None, -336, 6146, 5810)),
    ("DATA", "Dividends", (None, None, None, -2050, -2050)),
    ("TOTAL", "31 December 2019", (7000, None, 1133, 39188, 47322)),
    ("DATA", "Profit for the year", (None, None, None, 1931, 1931)),
    ("DATA", "Revaluation of tangible fixed assets", (None, None, -617, None, -617)),
    ("TOTAL", "Total comprehensive income for the year", (None, None, -617, 1931, 1314)),
    ("DATA", "Dividends", (None, None, None, -250, -250)),
    ("TOTAL", "31 December 2020", (7000, None, 517, 40869, 48386)),
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
    f"Disclosures 2021, pp.7-8 - {AR_URLS['FY2022']} and {P3_URLS['FY2021']}; "
    f"FY2020 impairment/NPL from Group accounts made up to 31 Dec 2020, p.34 (Note 15/16) and Pillar 3 Disclosures "
    f"2020, Table 6, p.8 - {CH_AR_URLS['FY2020']} and {P3_URLS['FY2020']}; "
    f"FY2019 impairment/NPL from the same Group accounts' FY2019 comparative column - {CH_AR_URLS['FY2020']}; "
    f"FY2018/FY2017 impairment/NPL from Group accounts made up to 31 Dec 2018, p.33 (Note 15/16) - {CH_AR_URLS['FY2018']}; "
    f"FY2016/FY2015 impairment/NPL from Group accounts made up to 31 Dec 2016, p.25 (Note 15/16) - {CH_AR_URLS['FY2016']}.\n\n"
    + ENTITY_NOTE
    + " Gross loans and advances to customers is derived as the Balance Sheet's net Loans and advances to "
    "customers plus the Loan loss provision balance from each year's own Note 15/16 (Banking Group basis); "
    "this ties exactly to the Balance Sheet's net figure every year. FY2025's Note 15 Balance Sheet loan loss "
    "provision (£5,333k) differs by £5k from Note 16's cumulative provision total (£5,338k) - a small internal "
    "document discrepancy, reproduced as-stated rather than forced to tie; both figures are shown. The "
    "regulatory credit risk exposure table (Pillar 3 Table 6) is a broader Pillar 1 exposure-class measure "
    "before credit risk mitigation (includes central bank/financial institution/covered bond exposures, not "
    "just customer loans) and does not tie to the narrower Balance Sheet loans line - shown as supplementary "
    "risk categorisation, not forced to reconcile. " + PRE2021_NOTE
    + " FY2015-FY2019's loan loss provision (used for both the 'Balance Sheet' and 'Note 16 cumulative' rows, "
    "since the Companies House Group accounts for those years give only the single Note 16 movement table, "
    "not a separate Balance Sheet-note split) and NPL figures are Group accounts Note 15/16 disclosures, not "
    "Pillar 3 figures (no pre-FY2020 Pillar 3 document was recoverable - see PRE2021_NOTE); the regulatory "
    "credit risk exposure section (Pillar 3 Table 6) is therefore populated for FY2020 only and left blank for "
    "FY2015-FY2019, a genuine access gap rather than a non-disclosure."
)

def npl_ratio(npl, gross):
    return f"{npl / gross * 100:.2f}%"

def coverage_ratio(prov, npl):
    return f"{prov / npl * 100:.2f}%"

aq_gross = {"FY2025": 1011493, "FY2024": 863936, "FY2023": 825925, "FY2022": 779193, "FY2021": 748236, "FY2020": 682727, "FY2019": 590885, "FY2018": 476770, "FY2017": 389398, "FY2016": 328735, "FY2015": 277870}
aq_prov_bs = {"FY2025": -5333, "FY2024": -4264, "FY2023": -4225, "FY2022": -3620, "FY2021": -3645, "FY2020": -4163, "FY2019": -1961, "FY2018": -2042, "FY2017": -1894, "FY2016": -1351, "FY2015": -1249}
aq_prov_total = {"FY2025": 5338, "FY2024": 4264, "FY2023": 4225, "FY2022": 3620, "FY2021": 3645, "FY2020": 4163, "FY2019": 1961, "FY2018": 2042, "FY2017": 1894, "FY2016": 1351, "FY2015": 1249}
aq_npl = {"FY2025": 11193, "FY2024": 10452, "FY2023": 9628, "FY2022": 6847, "FY2021": 6372, "FY2020": 6102, "FY2019": 3593, "FY2018": 2435, "FY2017": 2461, "FY2016": 891, "FY2015": 716}

aq_rows = [
    ("SECTION", "Loans and advances to customers - credit quality (Banking Group)", {}),
    ("DATA", "Gross loans and advances to customers", aq_gross),
    ("DATA", "Loan loss provision (Balance Sheet, Note 15)", aq_prov_bs),
    ("TOTAL", "Net loans and advances to customers", {"FY2025": 1006160, "FY2024": 859672, "FY2023": 821700, "FY2022": 775573, "FY2021": 744591, "FY2020": 678564, "FY2019": 588924, "FY2018": 474728, "FY2017": 387504, "FY2016": 327384, "FY2015": 276621}),
    ("DATA", "Total provisions for bad and doubtful debts (Note 16 cumulative)", aq_prov_total),
    ("DATA", "Non-performing loans and advances to customers (before provisions)", aq_npl),
    ("DATA", "NPL ratio (non-performing loans / gross loans)", {y: npl_ratio(aq_npl[y], aq_gross[y]) for y in YEARS}),
    ("DATA", "Coverage ratio (total provisions / non-performing loans)", {y: coverage_ratio(aq_prov_total[y], aq_npl[y]) for y in YEARS}),
    ("SECTION", "Regulatory credit risk exposure by class (Pillar 3 Table 6, before credit risk mitigation)", {}),
    ("DATA", "Central Government and Central Banks", {"FY2025": None, "FY2024": 760594, "FY2023": 645464, "FY2022": 646149, "FY2021": 577637, "FY2020": 287639}),
    ("DATA", "Financial institutions", {"FY2024": 65986, "FY2023": 40329, "FY2022": 48477, "FY2021": 38362, "FY2020": 56136}),
    ("DATA", "Covered Bonds", {"FY2024": 86742, "FY2023": 60875, "FY2022": 67566, "FY2021": 51916, "FY2020": 69489}),
    ("DATA", "Multilateral Development Banks", {"FY2024": 38424, "FY2023": 29455, "FY2022": 37092, "FY2021": 43634, "FY2020": 48783}),
    ("DATA", "Corporates", {"FY2024": 0, "FY2023": 0, "FY2022": 15, "FY2021": 99, "FY2020": 232}),
    ("DATA", "Retail", {"FY2024": 273745, "FY2023": 239489, "FY2022": 196497, "FY2021": 131874, "FY2020": 150260}),
    ("DATA", "CBILs - Government Guaranteed", {"FY2024": 15644, "FY2023": 10628, "FY2022": 12793, "FY2021": 13240}),
    ("DATA", "Secured on real estate property", {"FY2024": 578244, "FY2023": 571853, "FY2022": 568369, "FY2021": 581162, "FY2020": 528553}),
    ("DATA", "Other items", {"FY2024": 42329, "FY2023": 35556, "FY2022": 22514, "FY2021": 34363, "FY2020": 29989}),
    ("DATA", "Exposures In Default", {"FY2024": 12703, "FY2023": 14760, "FY2022": 9269, "FY2021": 7139, "FY2020": 4403}),
    ("DATA", "Credit Value Adjustment", {"FY2024": 6164, "FY2023": 1784, "FY2021": 1549, "FY2020": 598}),
    ("TOTAL", "Total regulatory credit risk exposure", {"FY2024": 1880575, "FY2023": 1650193, "FY2022": 1608741, "FY2021": 1480975, "FY2020": 1176082}),
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
    "already noted on the other Pillar 3 sheets). "
    "FY2020 uses the same 8% conversion rate as FY2021 (its own Table 3 header states 'Minimum Capital "
    "Requirement 8%', predating the PRA's September-2022 9%-TCR determination); it reconciles to the directly "
    "disclosed Total RWAs figure (401,130) to within 0.01% (FY2020: GBP40k/0.01%). FY2015-FY2019 are blank - "
    "no Pillar 3 document was recoverable for those years (see PRE2021_NOTE)."
)

rwa_rows = [
    ("DATA", "Pillar 3 edition status for this year (see source note)",
     {"FY2025": "Not published - SDDT Rule 3.1 opt-in from 02/04/2025; AR 2025 prints no RWA figure"}),
    ("SECTION", "Credit risk, by exposure class (derived, see sources)", {}),
    ("DATA", "Financial institutions", {"FY2024": 14667, "FY2023": 8811, "FY2022": 10256, "FY2021": 8450, "FY2020": 11413}),
    ("DATA", "Covered bonds", {"FY2024": 8678, "FY2023": 6089, "FY2022": 6756, "FY2021": 5188, "FY2020": 6950}),
    ("DATA", "Corporates", {"FY2024": 0, "FY2023": 0, "FY2022": 11, "FY2021": 100, "FY2020": 238}),
    ("DATA", "Retail", {"FY2024": 149878, "FY2023": 131600, "FY2022": 106233, "FY2021": 81438, "FY2020": 90825}),
    ("DATA", "Secured by mortgages on immovable property", {"FY2024": 216322, "FY2023": 213678, "FY2022": 212289, "FY2021": 218838, "FY2020": 197013}),
    ("DATA", "Exposures in default", {"FY2024": 16278, "FY2023": 18400, "FY2022": 12456, "FY2021": 8888, "FY2020": 5525}),
    ("DATA", "Other items", {"FY2024": 52400, "FY2023": 46544, "FY2022": 43689, "FY2021": 32050, "FY2020": 30913}),
    ("DATA", "Credit Value Adjustment", {"FY2024": 6167, "FY2023": 1778}),
    ("TOTAL", "Credit risk (subtotal)", {"FY2024": 464390, "FY2023": 426900, "FY2022": 391690, "FY2021": 354952, "FY2020": 342877}),
    ("SECTION", "Other risk categories", {}),
    ("DATA", "Market risk", {"FY2021": 975}),
    ("DATA", "Operational risk", {"FY2024": 148056, "FY2023": 116389, "FY2022": 83433, "FY2021": 69650, "FY2020": 58213}),
    ("TOTAL", "Total RWAs (derived - see sources for reconciliation to the directly disclosed Total RWAs sheet)", {"FY2024": 612446, "FY2023": 543289, "FY2022": 475123, "FY2021": 425577, "FY2020": 401090}),
]

bw = BankWorkbook(bank_name=COMPANY, years=YEARS, year_label=None, header_color="7030A0")
bw.add_balance_sheet_sheet(
    title=f"{COMPANY} — Balance Sheet",
    subtitle="Weatherbys Banking Group consolidated statement of financial position, GBP'000. FY2015-FY2025.",
    rows=bs_rows,
    sources_text=BS_SOURCES,
    first_col_width=64,
    source_height=280,
    unit_suffix=" (GBP'000)",
)
bw.add_income_statement_sheet(
    title=f"{COMPANY} — Profit & Loss",
    subtitle="Weatherbys Banking Group consolidated income statement, GBP'000. FY2015-FY2025.",
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
    subtitle="Weatherbys Banking Group consolidated basis, GBP'000. FY2015-FY2025.",
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

# KM1 Key Metrics — not applicable. Weatherbys publishes annual Pillar 3
# disclosures, but none of the editions in scope prints the prescribed KM1
# row set. Their numbered tables are bespoke leverage, liquidity, own-funds
# and capital-requirements tables; their row numbers must not be remapped onto
# the template (wayfinder KM1 rule 8).
KM1_SOURCES = (
    "Sources — Weatherbys Bank Limited's own Pillar 3 disclosures, checked against the Bank's live "
    "annual-reporting page on 17 September 2026. The newest listed Pillar 3 remains the year ended "
    "31 December 2024; the same page lists the Banking Group Annual Report and Accounts 2025, so the "
    "annual-report side of this workbook is current but no FY2025 Pillar 3 edition is published.\n\n"
    f"FY2024: Pillar 3 Disclosures 2024, printed pp.6 and 20-24 — {P3_URLS['FY2024']}\n"
    f"FY2023: Pillar 3 Disclosures 2023, printed pp.6 and 20-25 — {P3_URLS['FY2023']}\n"
    f"FY2022: Pillar 3 Disclosures 2022, printed pp.7 and 21-25 — {P3_URLS['FY2022']}\n"
    f"FY2021: Pillar 3 Disclosures 2021, printed pp.6 and 14-20 — {P3_URLS['FY2021']}\n\n"
    "Every edition was read through the end of its regulatory-template section. Each publishes capital, "
    "leverage and liquidity information, including CC1-style own-funds rows, but none publishes UK KM1: "
    "there is no single table carrying the template's own-funds, SREP/buffer, leverage, LCR and NSFR row "
    "set. The apparent bare row numbers in the documents belong to separate tables (for example the CC1 "
    "own-funds build-up) and are not KM1 row references. No later-edition comparative has been reshaped into "
    "a template, and no wider-group KM1 has been substituted. This is 'Pillar 3 is published but the "
    "template is not used', not a failed fetch or a claim that no Pillar 3 exists."
)

bw.add_km1_sheet(
    title=f"{COMPANY} — KM1 Key Metrics",
    subtitle="Not applicable — Weatherbys Bank publishes Pillar 3 disclosures, but none of its FY2021–FY2024 "
             "editions uses the UK KM1 key-metrics template. The newest live edition is FY2024; FY2025 is "
             "covered by an Annual Report but no Pillar 3 publication. See the source note for the row-set test.",
    rows=[
        ("DATA", "UK KM1 key-metrics template", {y: "Not used in any published edition" for y in YEARS}),
    ],
    sources_text=KM1_SOURCES,
    first_col_width=48,
    source_height=260,
)

FY2025_P3_NOTE = (
    "FY2025: NO Weatherbys Pillar 3 disclosure document for 2025 exists as at 15 September 2026 - the "
    "Bank's own annual-reporting page (https://www.weatherbys.bank/about-us/corporate-information/"
    "annual-reporting/) still lists the 2024 edition as the latest Pillar 3 document, and every 2026 "
    "upload-folder permutation of the FY2024 filename returns 404. Independently re-confirmed the same "
    "date by a Wayback CDX sweep of the whole weatherbys.bank domain for 'pillar' URLs, which returns no "
    "Pillar 3 document later than Weatherbys-Bank-Pillar-3-Disclosures-2024.pdf (first archived 20 July "
    "2025).\n"
    "SDDT DATE TEST (checked 2026-09-15) - IMPORTANT, this SUPERSEDES the publication-lag reading of that "
    "absence. An earlier pass on 2026-09-15 reasoned that because Weatherbys publishes its Pillar 3 alongside "
    "the April/May annual report, an FY2025 edition would be expected around April-May 2027 and the blank was "
    "merely a document not yet due. The PRA register shows that is wrong: no FY2025 edition is expected at all. "
    "The 'Consolidated Waivers list for PRA-regulated firms - as of 1 July 2026' (bankofengland.co.uk/"
    "prudential-regulation/authorisations/waivers-and-modifications-of-rules) records that Weatherbys Bank "
    "Limited (FRN 204571) holds a 'Modification by Consent - PRA Rulebook - CRR Firms - Rule 3.1 of the SDDT "
    "Regime - General Application Part', sub-rule 'Ru 3.1', starting 02/04/2025 with no end date (still in "
    "force). That modification removes the Pillar 3 disclosure obligation outright - a stronger relief than UK "
    "CRR Article 433b, which only reduces frequency and content for small and non-complex institutions. The "
    "Bank's year-end is 31 December, stable across its Companies House accounts filing history (company "
    "02943300). FY2025 (y/e 31 December 2025) therefore falls AFTER the modification took effect, so no FY2025 "
    "Pillar 3 was ever required. Consistent with that, FY2024 (y/e 31 December 2024) PREDATES the modification - "
    "which is exactly why the 2024 edition exists and is the last one. The FY2025 blanks here are structural and "
    "permanent unless the Bank opts back in; they should NOT be re-chased in April-May 2027 or at any later "
    "date. By the same logic the FY2025 Annual-Report-sourced figures below will NOT be restated onto a Pillar 3 "
    "basis later, because no such document is coming - see the precision caveat on Total Capital.\n"
    "The FY2025 figures that ARE populated "
    "below therefore come from the Bank's own Annual Report and Financial Accounts 2025, NOT from a "
    "Pillar 3 document - and on the CONSOLIDATED (Banking Group) basis, matching the basis of the "
    f"FY2020-FY2024 Pillar 3 figures in this sheet ({AR2025_PDF_URL}):\n"
    "  - CET1 Ratio 13.1%, Total Capital Ratio 15.3%, LCR 1,080%, NSFR 252%, Leverage Ratio 6.05%: "
    "Annual Report and Financial Accounts 2025, '3. Financial key performance indicators', p.19 (the "
    "five-KPI panel, each figure shown with its 2024 comparative), corroborated for CET1/total capital/"
    "leverage by '2. Business review: the Group', p.19-20 ('a Common Equity Tier 1 ratio of 13.1% (2024: "
    "13.8%)... the Group's total capital ratio at the year end was 15.3% (2024: 16.3%). The leverage "
    "ratio at the year end was 6.05% (2024: 7.08%)').\n"
    "  - Total Capital GBP105.5m: Annual Report and Financial Accounts 2025, Report of the Directors, "
    "section 4.1 'Capital and leverage ratios', p.45 ('On a consolidated basis total regulatory capital "
    "and the total capital ratio were GBP105.5 million and 15.3% respectively (2024: GBP99.8 million and "
    "16.3%)'). Stated only to GBP0.1m, so FY2025's 105,500 carries less precision than the exact "
    "Pillar 3-sourced figures for FY2020-FY2024. This is now a PERMANENT precision limit, not a temporary one: "
    "per the SDDT date test above, no FY2025 Pillar 3 will be published, so there is no future document to "
    "restate this figure against.\n"
    "  - BASIS CHECK: the Annual Report and Pillar 3 bases agree for this bank. Every FY2024 comparative "
    "printed alongside the FY2025 figures above reproduces this workbook's Pillar 3-sourced FY2024 values "
    "- total capital GBP99.8m vs 99,753; total capital ratio 16.3% vs 16.26%; CET1 ratio 13.8% vs 13.84%; "
    "leverage 7.08% vs 7.08%; LCR 1,017% vs 1017%; NSFR 266% vs 266% - so the FY2025 figures sit on the "
    "same consolidated basis as the rest of the series, not a different one.\n"
    "  - CET1 Capital, Tier 1 Capital, Tier 1 Ratio and Total RWAs now STATE the absence in the FY2025 "
    "cell rather than sitting blank (changed 2026-09-18, because an empty cell is indistinguishable from a "
    "year nobody searched): the FY2025 "
    "Annual Report states no CET1 or Tier 1 capital amount, no Tier 1 ratio and no risk-weighted-assets "
    "figure anywhere (it confirms the Bank holds Additional Tier 1 securities and Tier 2 subordinated "
    "notes, so CET1/Tier 1/Total Capital are genuinely different numbers and neither may be inferred from "
    "the other). Total RWAs has deliberately NOT been back-solved from GBP105.5m / 15.3%, since both "
    "inputs are rounded."
)

P3_SOURCES = (
    "Sources - Weatherbys Bank 3 Pillar Disclosures, Group/Solo columns, GBP'000 except ratios: "
    f"FY2024, pp.5-6 and 20-26 - {P3_URLS['FY2024']}; "
    f"FY2023, pp.5-6 and 20-27 - {P3_URLS['FY2023']}; "
    f"FY2022, pp.6-7 and 21-27 - {P3_URLS['FY2022']}; "
    f"FY2021, pp.5-6 and 14, 18-22 - {P3_URLS['FY2021']}; "
    f"FY2020, Pillar 3 Disclosures - Year Ended 31st December 2020, Tables 1-2 and 10 (pp.5-6, 13-14) - {P3_URLS['FY2020']}.\n\n"
    + ENTITY_NOTE
    + " " + FY2025_P3_NOTE
    + " " + PRE2021_NOTE
    + " FY2020's Table 1 mislabels its Total Capital Ratio row as 'Tier 2 Ratio' (14.53% Group/14.32% Solo) - "
    "verified as Total Capital / RWAs (58,286/401,130 = 14.53%), reproduced here under 'Total Capital Ratio' "
    "with the source's own mislabel noted rather than propagated."
)

# THE FOUR ABSENT FY2025 METRICS NOW SAY SO IN THE CELL (2026-09-18, remaining-gap
# round). They previously sat as None, and an empty cell is indistinguishable from a
# year nobody searched - `audit_gaps.py` scored all four, plus the RWA Breakdown
# column, as unexplained gaps. Two separate findings are compressed into the cell
# text and both were RE-VERIFIED independently on 2026-09-18 rather than carried on
# trust:
#   (1) NO FY2025 PILLAR 3 EXISTS AND NONE IS COMING. The PRA consolidated waivers
#       register was re-downloaded that day (2,899 rows) and matched on BOTH
#       conjuncts - Rule Description 'SDDT Regime - General Application' AND Sub Rule
#       Number 'Ru 3.1'; either column alone gives a wrong answer. The row: FRN
#       204571, 'Weatherbys Bank Limited', ref A00010140P.pdf, start 02/04/2025, NO
#       end date. The Bank's year-end is 31 December, so the FY2025 reporting date of
#       31 December 2025 falls AFTER the opt-in and no FY2025 edition was ever owed.
#       FY2024 (31 December 2024) PRECEDES it, which is why the 2024 edition exists
#       and is the last one. (The Bank's other register row, a Capital Requirements
#       Regulation Ar 9 permission running 09/12/2024-09/12/2027, is not a disclosure
#       exemption and is not relied on.) The Bank's own annual-reporting index was
#       fetched live the same day with a browser UA over HTTP/1.1 (HTTP 200,
#       text/html, 67,417 bytes - not a block): its newest Pillar 3 link is still
#       Weatherbys-Bank-Pillar-3-Disclosures-2024.pdf, alongside a 2025 Annual Report
#       and a 2025 gender-pay report, so the Bank kept publishing into the window and
#       added no Pillar 3.
#   (2) THE FY2025 ANNUAL REPORT WAS READ AND PRINTS NO SUCH FIGURE. The PDF was
#       re-downloaded 2026-09-18 (HTTP 200, application/pdf, 4,899,892 bytes, begins
#       `%PDF-1.6`) and text-extracted to 403,150 characters. RICHNESS CONTROL FIRST,
#       so the zeros indict the document and not the instrument: 2,967 hits for
#       'the', 132 for 'Weatherbys', 177 for 'ratio', 94 for 'capital'. Against that,
#       every 'RWA' hit (17) is a false positive inside 'forward'/'Forward-looking',
#       and the only two 'risk-weighted' hits are the glossary DEFINITIONS of the
#       CET1 and total capital ratios. The report prints the total capital AMOUNT
#       (£105.5m, section 4.1 p.45) and four ratios, and no CET1 capital amount, no
#       Tier 1 capital amount, no Tier 1 ratio and no RWA amount anywhere.
# Nothing is back-solved: £105.5m / 15.3% would invent an RWA from two rounded
# inputs, and the Bank holds AT1 securities and Tier 2 notes (p.2443-2446), so CET1,
# Tier 1 and Total Capital are genuinely three different numbers here.
# This is outcome 2 (never published), not outcome 3 (unreached today).
WB_FY2025_ABSENT = "Not disclosed - AR 2025 states no such figure; no Pillar 3 (SDDT Rule 3.1 from 02/04/2025)"

capital = {
    # FY2025 is sourced from the Annual Report and Financial Accounts 2025 (consolidated basis), NOT
    # from a Pillar 3 document - none exists for 2025. CET1 Capital, Tier 1 Capital, Tier 1 Ratio and
    # Total RWAs are genuinely absent from that report and carry the stated negative above.
    "FY2025": {"cet1": WB_FY2025_ABSENT, "tier1": WB_FY2025_ABSENT, "total": 105500, "rwa": WB_FY2025_ABSENT, "cet1r": "13.1%", "tier1r": WB_FY2025_ABSENT, "totalr": "15.3%", "lev": "6.05%", "lcr": "1080%", "nsfr": "252%"},
    "FY2024": {"cet1": 84898, "tier1": 87898, "total": 99753, "rwa": 613559, "cet1r": "13.84%", "tier1r": "14.33%", "totalr": "16.26%", "lev": "7.08%", "lcr": "1017%", "nsfr": "266%"},
    "FY2023": {"cet1": 73192, "tier1": 76192, "total": 87815, "rwa": 543090, "cet1r": "13.48%", "tier1r": "14.03%", "totalr": "16.17%", "lev": "7.13%", "lcr": "896%", "nsfr": "254%"},
    "FY2022": {"cet1": 57524, "tier1": 57524, "total": 69108, "rwa": 476472, "cet1r": "12.07%", "tier1r": "12.07%", "totalr": "14.50%", "lev": "5.30%", "lcr": "650%", "nsfr": "259.7%"},
    "FY2021": {"cet1": 50247, "tier1": 50247, "total": 61634, "rwa": 425582, "cet1r": "11.81%", "tier1r": "11.81%", "totalr": "14.48%", "lev": "3.37%", "lcr": "531%", "nsfr": "268.2%"},
    "FY2020": {"cet1": 46910, "tier1": 46910, "total": 58286, "rwa": 401130, "cet1r": "11.69%", "tier1r": "11.69%", "totalr": "14.53%", "lev": "3.92%", "lcr": "683%", "nsfr": "227.8%"},
    # The intact FY2020 disclosure also reports the prior-year liquidity comparatives (Table 10).
    # No other FY2019 regulatory metrics were available in that document.
    "FY2019": {"cet1": None, "tier1": None, "total": None, "rwa": None, "cet1r": None, "tier1r": None, "totalr": None, "lev": None, "lcr": "586%", "nsfr": "207.6%"},
}
# FY2015-FY2019: no capital/RWA metrics. FY2019's LCR and NSFR are disclosed as comparatives in the intact
# FY2020 document (Table 10). The only pre-2021 Weatherbys Pillar 3 document located (a Wayback Machine
# capture of the pre-wp-uploads "WBL-Pillar3-Disclosures.pdf", archived 2020-09-21, timed to be the FY2019
# disclosure) is truncated mid-file by the Wayback Machine's own capture (1,048,576 of 1,264,248 original bytes)
# and unrecoverable by qpdf/pdftotext repair; no other pre-2021 Pillar 3 PDF for this bank was found via
# web/CDX search. This is a genuine access gap (self-skip), not a non-disclosure - see PRE2021_NOTE.

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
    subtitle="Weatherbys Bank risk-weighted assets by category, GBP'000 — derived from Pillar 3 capital requirement tables (see sources). "
             "The FY2025 column stays visible and now carries an explicit stated negative on the status row rather than sitting blank: "
             "the Bank holds a PRA SDDT Rule 3.1 modification effective 2 April 2025 with no end date, preceding its 31 December 2025 "
             "year-end, so no FY2025 Pillar 3 exists, and the FY2025 Annual Report prints no risk-weighted-assets figure of any kind.",
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
        ("Total equity (year-end)", {"FY2015": 32154, "FY2016": 36012, "FY2017": 39201, "FY2018": 43562, "FY2019": 47322, "FY2020": 48386, "FY2021": 52800, "FY2022": 62500, "FY2023": 84991, "FY2024": 100043, "FY2025": 111114}),
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
    note=(
        "FY2025 has no Weatherbys Pillar 3 disclosure document (none published as at 15 September 2026), so "
        "its CET1 Ratio, Total Capital, Total Capital Ratio, Leverage Ratio, LCR and NSFR are taken from the "
        "Annual Report and Financial Accounts 2025 instead (consolidated basis, same basis as the Pillar 3 "
        "series - every FY2024 comparative printed there reproduces this workbook's Pillar 3-sourced FY2024 "
        "value); FY2025 CET1 Capital, Tier 1 Capital, Tier 1 Ratio and Total RWAs stay blank because that "
        "report states no such figure - all four now carry that statement in the cell rather than sitting blank "
        "(2026-09-18). FY2021-FY2024 "
        "values are the official Weatherbys Group/Solo disclosures. FY2020's Pillar 3 metrics are populated "
        "from Weatherbys' own FY2020 Pillar 3 Disclosures document (already reported under CRD IV/Basel III "
        "CET1/Tier 1/Tier 2 terminology - no Basel-II-era Tier-1/Total-Capital-only caveat applies). FY2015-"
        "FY2019 Pillar 3 metrics are blank: the only pre-2021 Pillar 3 document found for this bank is an "
        "unrecoverable, truncated Wayback Machine capture, a genuine access gap rather than a non-disclosure "
        "(see the Balance Sheet/Cash Flow/Asset Quality sheets' source notes). All other statements (Balance "
        "Sheet, Profit & Loss, Statement of Changes in Equity, Cash Flow Statement, and the Asset Quality "
        "sheet's loan-book credit-quality rows) are populated back to FY2015, this bank's confirmed historical "
        "floor, sourced from Weatherbys' Companies-House-filed Group accounts."
    ),
)

bw.save("/Users/armaan/code/katalysis/banks/WEATHERBYS FINANCIALS.xlsx")
