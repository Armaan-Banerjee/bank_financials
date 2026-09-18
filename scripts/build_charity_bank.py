import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

# Calendar year-end (31 December), full 5 years FY2021-FY2025.
YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first
YEAR_LABEL = {y: y for y in YEARS}

AR2025_URL = "https://www.charitybank.org/wp-content/uploads/2026/06/Charity-Bank-2025-Annual-Report-signed.pdf"
AR2024_URL = "https://www.charitybank.org/wp-content/uploads/2025/06/Charity-Bank-2024-Annual-Report-signed.pdf"
AR2023_URL = "https://www.charitybank.org/wp-content/uploads/2024/10/Charity-Bank-Annual-Accounts-2023.pdf"
AR2022_CH_URL = ("https://find-and-update.company-information.service.gov.uk/company/04330018/filing-history/"
                  "MzM4MjU0NDA3NWFkaXF6a2N4/document?format=pdf&download=0")
AR2021_CH_URL = ("https://find-and-update.company-information.service.gov.uk/company/04330018/filing-history/"
                  "MzM0MTk3OTg0MGFkaXF6a2N4/document?format=pdf&download=0")

P3_2023_URL = ("https://web.archive.org/web/20250809165738/https://www.charitybank.org/wp-content/uploads/2024/10/"
               "PILLAR-3-disclosures-2023.pdf")
P3_2022_URL = ("https://web.archive.org/web/20250805161700/https://www.charitybank.org/wp-content/uploads/2024/10/"
               "PILLAR-3-disclosures-2022-FINAL.pdf")
P3_2021_URL = ("https://web.archive.org/web/20250726224104/https://www.charitybank.org/wp-content/uploads/2024/10/"
               "PILLAR-3-disclosures-2021-Final.pdf")

ENTITY_NOTE = (
    "ENTITY NOTE: The Charity Bank Limited (Companies House 04330018, FRN 207701) matches Banks List 2608.xlsx "
    "exactly - a wholly UK-owned, standalone entity with no parent-subsidiary complications. Charity Bank "
    "publishes a full Statement of Cash Flows every year (no FRS 101/102 exemption). Its FY2021 and FY2022 "
    "Companies House filings are fully scanned/image-only PDFs (no text layer) - OCR'd with tesseract and every "
    "figure visually cross-checked against a rendered page image at 400dpi (one apparently ambiguous OCR read, "
    "'depreciation of property and equipment' for FY2021, was confirmed as 59 by direct visual inspection, not "
    "the alternative misreading). All 5 years' own primary figures were cross-checked against their appearance "
    "as the following year's comparative column and match exactly - no source-document arithmetic errors found."
)

PRA_WAIVERS_CSV = (
    "https://www.bankofengland.co.uk/-/media/boe/files/prudential-regulation/authorisations/"
    "waivers-and-modifications-of-rules/consolidated-waivers-pra-firms.csv"
)

PILLAR3_NOTE = (
    "PILLAR 3 NOTE: Charity Bank published an annual standalone Pillar 3 disclosure document every year through "
    "the FY2023 edition (retrieved via the Wayback Machine - the current live site no longer links to any Pillar "
    "3 document, only Annual Reports). No FY2024 or FY2025 edition has been published anywhere as of the "
    "research date.\n"
    "CAUSAL LINK NOW ESTABLISHED, 2026-09-15 (cross-bank SDDT pass) - this supersedes the earlier hedged "
    "wording, which said SDDT status was 'noted as context' but 'not asserted as a confirmed causal link'. "
    "The absence of a FY2024 and FY2025 Pillar 3 document is an EVIDENCED STRUCTURAL EXEMPTION, not a "
    "sourcing failure: becoming a Small Domestic Deposit Taker removes the Pillar 3 disclosure obligation "
    "outright, so no such document will ever exist for those years.\n"
    "Evidence 1 - the PRA's own firm-level register. Bank of England consolidated list of waivers and "
    "modifications granted to PRA-authorised firms (downloaded 2026-09-15) carries the row: FRN 207701, 'The "
    "Charity Bank Limited', 'Modification by Consent - PRA Rulebook - CRR Firms - Rule 3.1 of the SDDT Regime "
    "- General Application Part', rule 'SDDT Regime - General Application', sub rule 'Ru 3.1', waiver ref "
    f"'A00007506P.pdf', start date '01/02/2024', no end date - {PRA_WAIVERS_CSV}\n"
    "Evidence 2 - Charity Bank in its own words, in both recent Annual Reports, under the heading 'Capital "
    "regulatory framework': 'In 2024, Charity Bank opted-in to the PRA's Small Domestic Deposit-Takers "
    "('SDDT') regime, also known as 'Strong & Simple'.' - Charity Bank 2024 Annual Report p.32 "
    f"({AR2024_URL}) and, repeated verbatim, Charity Bank 2025 Annual Report p.30 ({AR2025_URL}). This "
    "corroborates the register's 01/02/2024 start date and the FY2023 Annual Report's (p.35) 'was accepted "
    f"into the Small Domestic Deposit Taker (SDDT) regime in January 2024' ({AR2023_URL}).\n"
    "Evidence 3 - what the Rule 3.1 modification does to Pillar 3, stated by a peer holding the identical "
    "register row: Cynergy Bank plc Annual Report & Accounts 2024, p.71 - 'The Bank applied for the "
    "Modification by Consent to become an SDDT and received approval on 17 January 2025. As a result, we are "
    "not required to publish Pillar 3 disclosures as at 31 December 2024 and will submit only a simplified "
    "retail deposit ratio instead of a full Net Stable Funding Ratio (NSFR) going forward.'\n"
    "DATE FIT: the modification took effect 1 February 2024, i.e. before the 31 December 2024 year-end, so it "
    "covers FY2024 and FY2025 - exactly the two years with no Pillar 3 document. It covers NEITHER FY2021, "
    "FY2022 nor FY2023, all of which have their own published Pillar 3 editions in any case. Do not read the "
    "exemption back onto FY2023 or earlier. Note also that the Annual Reports' statement that the SDDT regime "
    "'takes full effect from 1 January 2027' refers to the SDDT simplified CAPITAL regime, which is a "
    "separate and later matter from the disclosure exemption that already applies. Charity Bank does not "
    "disclose a Simplified Retail Deposit Ratio value, so nothing replaces the NSFR series here.\n"
    "For FY2024 and FY2025, "
    "capital amounts (Tier 1/Tier 2/Total capital, £), RWAs, leverage exposure, and CET1/Total Capital/Leverage "
    "ratios were instead sourced from the 'Capital risk' section of each year's own Annual Report (Strategic "
    "Report and Note 28) - the Annual Reports do not disclose LCR, NSFR, or MREL at all, so those sheets are "
    "blank for FY2024-FY2025 (not a transcription gap - genuinely not published anywhere)."
)

LEVERAGE_BASIS_NOTE = (
    "LEVERAGE RATIO BASIS NOTE: the FY2021 Pillar 3 disclosure's own leverage ratio calculation (Tier 1 capital "
    "÷ [total balance sheet assets + addbacks - intangibles + 10% of off-balance-sheet commitments]) does not "
    "show an explicit deduction for claims on central banks, whereas the FY2022-FY2025 figures are explicitly "
    "computed on a 'total exposure measure excluding claims on central banks' basis (per the UK KM1 Pillar 3 "
    "template / each Annual Report's own definition). FY2021 (7.72%) is therefore likely not on a directly "
    "comparable basis to FY2022 onward (8.39%-10.39%) - shown exactly as each year's own source states it, not "
    "blended or recalculated."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are The Charity Bank Limited's own Cash Flow Statement, £'000:\n"
    f"FY2025: Charity Bank 2025 Annual Report, p.54 (Cash Flow Statement) - {AR2025_URL}\n"
    f"FY2024: Charity Bank 2024 Annual Report, p.52 (Cash Flow Statement) - {AR2024_URL}\n"
    f"FY2023: Charity Bank Annual Report 2023, p.54 (Cash Flow Statement) - {AR2023_URL}\n"
    f"FY2022: The Charity Bank Limited Annual Report for the year ended 31 December 2022 (Companies House filing, "
    f"17 Jun 2023), p.42 (Cash Flow Statement) - scanned/image-only, OCR'd and visually cross-checked - {AR2022_CH_URL}\n"
    f"FY2021: The Charity Bank Limited Annual Report for the year ended 31 December 2021 (Companies House filing), "
    f"p.38 (Cash Flow Statement) - scanned/image-only, OCR'd and visually cross-checked - {AR2021_CH_URL}\n"
    "All 5 years' own primary figures cross-checked and tie exactly against their appearance as the following "
    "year's comparative column (e.g. FY2021's own £2,878k operating-adjustments subtotal matches the FY2022 "
    "report's own FY2021 comparative exactly).\n\n"
    + ENTITY_NOTE
)


def p3_sources(page_2025="93 (Note 28) / 32 (Strategic Report)", page_2024="91 (Note 28) / 34 (Strategic Report)",
               page_2023="14 (Template UK KM1)", page_2022="14-15 (Template UK KM1, FY2022 column)",
               page_2021="15 (Own Funds / Key CRD IV Ratios)"):
    return (
        "Sources - The Charity Bank Limited entity-level Pillar 3 / regulatory capital basis:\n"
        f"FY2025: Charity Bank 2025 Annual Report, p.{page_2025} - {AR2025_URL}\n"
        f"FY2024: Charity Bank 2024 Annual Report, p.{page_2024} - {AR2024_URL}\n"
        f"FY2023: Charity Bank Pillar 3 Disclosures 2023, p.{page_2023} - {P3_2023_URL}\n"
        f"FY2022: Charity Bank Pillar 3 Disclosures 2022, p.{page_2022} - {P3_2022_URL}\n"
        f"FY2021: Charity Bank Pillar 3 Disclosures 2021, p.{page_2021} - {P3_2021_URL}; FY2021 LCR cross-check: FY2022 Pillar 3 Disclosure, FY2021 comparative column - {P3_2022_URL}\n\n"
        + PILLAR3_NOTE
    )


bw = BankWorkbook(bank_name="The Charity Bank Limited", years=YEARS, year_label=YEAR_LABEL, header_color="285943")

STATEMENTS_SOURCES = (
    "Sources - all figures are The Charity Bank Limited's own Statement of Comprehensive Income / Balance Sheet / "
    "Statement of Changes in Equity, transcribed from each year's own annual report/filing (not a later year's "
    "comparative column):\n"
    f"FY2025: Charity Bank 2025 Annual Report, pp.51,52,53 - {AR2025_URL}\n"
    f"FY2024: Charity Bank 2024 Annual Report, pp.49,50,51 - {AR2024_URL}\n"
    f"FY2023: Charity Bank Annual Report 2023, pp.51,52,53 - {AR2023_URL}\n"
    f"FY2022: The Charity Bank Limited Annual Report for the year ended 31 December 2022 (Companies House filing), "
    f"pp.39,40,41 - scanned/image-only, visually transcribed - {AR2022_CH_URL}\n"
    f"FY2021: The Charity Bank Limited Annual Report for the year ended 31 December 2021 (Companies House filing), "
    f"pp.35,36,37 - scanned/image-only, visually transcribed - {AR2021_CH_URL}\n"
    "All 5 years' own primary figures cross-checked and tie exactly against their appearance as the following "
    "year's comparative column.\n\n"
    + ENTITY_NOTE
    + "\n\nPRESENTATION NOTE: 'Financial assets at fair value through profit & loss' (FVPL) and a separate "
    "'Profit on financial assets at fair value through profit & loss' P&L line appear only in FY2021 (as a nil "
    "balance/small profit) - the Bank held no such assets from FY2022 onward. 'Deferred tax asset' (Balance Sheet) "
    "and 'Current tax liability' only appear as distinct lines from FY2022/FY2023 onward respectively - blank "
    "cells indicate that year's own report did not disclose that specific line, not a transcription gap. No OCI "
    "in any year - 'Total comprehensive income/(loss) for the year' equals 'Profit/(loss) after taxation' exactly, "
    "per the Bank's own disclosure that all income and expenses are derived from continuing operations."
)

ASSET_QUALITY_SOURCES = (
    "Sources - The Charity Bank Limited's own Note 28 (Financial Risk Management), 'Maximum exposure to credit "
    "risk' / 'Credit risk by asset class' IFRS 9 stage tables for 'Loans and advances to customers at amortised "
    "cost':\n"
    f"FY2025: Charity Bank 2025 Annual Report, p.81 - {AR2025_URL}\n"
    f"FY2024: Charity Bank 2024 Annual Report, p.85 - {AR2024_URL}\n"
    f"FY2023: Charity Bank Annual Report 2023, p.83 - {AR2023_URL}\n"
    f"FY2022: The Charity Bank Limited Annual Report for the year ended 31 December 2022 (Companies House filing), "
    f"p.74 - scanned/image-only, visually transcribed - {AR2022_CH_URL}\n"
    f"FY2021: The Charity Bank Limited Annual Report for the year ended 31 December 2021 (Companies House filing), "
    f"p.70 - scanned/image-only, visually transcribed - {AR2021_CH_URL}\n"
    "Every year's own 'Carrying amount' total ties exactly to the Balance Sheet's own 'Loans and advances to "
    "customers' line for that year.\n\n"
    + ENTITY_NOTE
)

RWA_BREAKDOWN_SOURCES = (
    "Sources - The Charity Bank Limited entity-level Pillar 3 / regulatory capital basis, UK OV1 template (RWAs by "
    "category):\n"
    f"FY2025/FY2024: Charity Bank 2025 Annual Report, p.32 (Strategic Report, aggregate Total RWA only - no "
    "category split published; standalone Pillar 3 disclosure ceased after the FY2023 edition, see PILLAR3_NOTE "
    f"on the Pillar 3 metric sheets) - {AR2025_URL}\n"
    f"FY2023: Charity Bank Pillar 3 Disclosures 2023, p.15 (Template UK OV1) - {P3_2023_URL}\n"
    f"FY2022: Charity Bank Pillar 3 Disclosures 2022, p.15 (Template UK OV1) - {P3_2022_URL}\n"
    f"FY2021: Charity Bank Pillar 3 Disclosures 2022, p.15 (Template UK OV1, FY2021 comparative column) - "
    f"{P3_2022_URL}\n\n"
    + PILLAR3_NOTE
    + "\n\nFY2021 SOURCING NOTE: FY2021's own Pillar 3 Disclosures 2021 document uses an older format (a single "
    "'Credit and operational risk RWAs' combined total of £153,193k plus a separate 'Total Credit Risk Capital "
    "Component' £'000 figure at an 8% weighting, not a UK OV1-style RWA-by-category table) - so the FY2021 "
    "category split shown here (Credit risk £143,316k / Operational risk £9,877k) is instead taken from the "
    "following year's own Pillar 3 Disclosures 2022 document, which states it as its own FY2021 comparative "
    "column. The combined Total (£153,193k) is independently corroborated by FY2021's own document and ties "
    "exactly to the existing Total RWAs metric sheet."
)

# ---------------------------------------------------------------
# Sheet: Balance Sheet
# ---------------------------------------------------------------
balance_sheet_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and balances at banks", {"FY2025": 82700, "FY2024": 97352, "FY2023": 91420, "FY2022": 63198, "FY2021": 45934}),
    ("DATA", "Financial assets at fair value through profit & loss", {"FY2021": 0}),
    ("DATA", "Financial assets at amortised cost", {"FY2025": 33160, "FY2024": 14859, "FY2023": 16661, "FY2022": 18776, "FY2021": 24888}),
    ("DATA", "Loans and advances to customers", {"FY2025": 363058, "FY2024": 331101, "FY2023": 285315, "FY2022": 273700, "FY2021": 238695}),
    ("DATA", "Prepayments", {"FY2025": 770, "FY2024": 577, "FY2023": 407, "FY2022": 361, "FY2021": 256}),
    ("DATA", "Other assets", {"FY2025": 325, "FY2024": 407, "FY2023": 497, "FY2022": 358, "FY2021": 215}),
    ("DATA", "Deferred tax asset", {"FY2025": 264, "FY2024": 252, "FY2023": 393}),
    ("DATA", "Property and equipment", {"FY2025": 177, "FY2024": 232, "FY2023": 41, "FY2022": 63, "FY2021": 110}),
    ("DATA", "Right-of-use asset", {"FY2025": 638, "FY2024": 16, "FY2023": 208, "FY2022": 406, "FY2021": 622}),
    ("DATA", "Intangible fixed assets", {"FY2025": 720, "FY2024": 871, "FY2023": 1025, "FY2022": 1188, "FY2021": 1352}),
    ("TOTAL", "Total assets", {"FY2025": 481812, "FY2024": 445667, "FY2023": 395967, "FY2022": 358050, "FY2021": 312072}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Customer accounts", {"FY2025": 421741, "FY2024": 387175, "FY2023": 342963, "FY2022": 313835, "FY2021": 272571}),
    ("DATA", "Deferred income", {"FY2025": 236, "FY2024": 341, "FY2023": 337, "FY2022": 316, "FY2021": 374}),
    ("DATA", "Other liabilities", {"FY2025": 3322, "FY2024": 3609, "FY2023": 2563, "FY2022": 4771, "FY2021": 4079}),
    ("DATA", "Current tax liability", {"FY2025": 521, "FY2024": 781, "FY2023": 1546, "FY2022": 0}),
    ("DATA", "Accruals", {"FY2025": 627, "FY2024": 1052, "FY2023": 675, "FY2022": 638, "FY2021": 662}),
    ("DATA", "Lease liability", {"FY2025": 656, "FY2024": 11, "FY2023": 179, "FY2022": 335, "FY2021": 501}),
    ("DATA", "Subordinated debt", {"FY2025": 9555, "FY2024": 9346, "FY2023": 8141, "FY2022": 8141, "FY2021": 7137}),
    ("TOTAL", "Total liabilities", {"FY2025": 436658, "FY2024": 402315, "FY2023": 356404, "FY2022": 328036, "FY2021": 285324}),
    ("SECTION", "Shareholders' equity", {}),
    ("DATA", "Called up share capital", {"FY2025": 16810, "FY2024": 16810, "FY2023": 16621, "FY2022": 15743, "FY2021": 15437}),
    ("DATA", "Retained earnings", {"FY2025": 20412, "FY2024": 18610, "FY2023": 15235, "FY2022": 7398, "FY2021": 4682}),
    ("DATA", "Share premium", {"FY2025": 7932, "FY2024": 7932, "FY2023": 7707, "FY2022": 6873, "FY2021": 6629}),
    ("TOTAL", "Total equity", {"FY2025": 45154, "FY2024": 43352, "FY2023": 39563, "FY2022": 30014, "FY2021": 26748}),
    ("TOTAL", "Total liabilities and equity", {"FY2025": 481812, "FY2024": 445667, "FY2023": 395967, "FY2022": 358050, "FY2021": 312072}),
]

bw.add_balance_sheet_sheet(
    title="The Charity Bank Limited — Balance Sheet",
    subtitle="Entity-level basis, £'000. See source note at bottom.",
    rows=balance_sheet_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=74,
    source_height=260,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Sheet: Profit & Loss
# ---------------------------------------------------------------
income_statement_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest income", {"FY2025": 27885, "FY2024": 28476, "FY2023": 24041, "FY2022": 12218, "FY2021": 7116}),
    ("DATA", "Interest expense", {"FY2025": -13398, "FY2024": -12537, "FY2023": -8026, "FY2022": -2822, "FY2021": -1602}),
    ("TOTAL", "Net interest income", {"FY2025": 14487, "FY2024": 15939, "FY2023": 16015, "FY2022": 9396, "FY2021": 5514}),
    ("DATA", "Fee income", {"FY2025": 526, "FY2024": 561, "FY2023": 596, "FY2022": 724, "FY2021": 780}),
    ("DATA", "Profit on financial assets at fair value through profit & loss", {"FY2022": 0, "FY2021": 12}),
    ("DATA", "Other operating income", {"FY2025": 115, "FY2024": 260, "FY2023": 144, "FY2022": 52, "FY2021": 98}),
    ("TOTAL", "Net total income", {"FY2025": 15128, "FY2024": 16760, "FY2023": 16755, "FY2022": 10172, "FY2021": 6404}),
    ("SECTION", "Expenses", {}),
    ("DATA", "Administrative expenses", {"FY2025": -11066, "FY2024": -9775, "FY2023": -7818, "FY2022": -6010, "FY2021": -5141}),
    ("DATA", "Depreciation and amortisation", {"FY2025": -396, "FY2024": -391, "FY2023": -412, "FY2022": -424, "FY2021": -423}),
    ("DATA", "Impairment reversal/(charge)", {"FY2025": 58, "FY2024": -4, "FY2023": 465, "FY2022": -1022, "FY2021": 104}),
    ("TOTAL", "Profit before taxation", {"FY2025": 3724, "FY2024": 6590, "FY2023": 8990, "FY2022": 2716, "FY2021": 944}),
    ("DATA", "Tax expense", {"FY2025": -934, "FY2024": -1649, "FY2023": -1153, "FY2022": 0, "FY2021": 0}),
    ("TOTAL", "Profit after taxation and total comprehensive income for the year", {"FY2025": 2790, "FY2024": 4941, "FY2023": 7837, "FY2022": 2716, "FY2021": 944}),
]

bw.add_income_statement_sheet(
    title="The Charity Bank Limited — Profit & Loss",
    subtitle="Entity-level basis, £'000. No OCI in any year - see source note at bottom.",
    rows=income_statement_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=74,
    source_height=260,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Sheet: Statement of Changes in Equity
# ---------------------------------------------------------------
equity_headers = ["Share capital", "Retained earnings", "Share premium", "Total equity"]
equity_rows = [
    ("TOTAL", "At 1 January 2021", (12509, 3738, 4657, 20904)),
    ("DATA", "Profit for the year", (None, 944, None, 944)),
    ("DATA", "Capital received", (2928, None, 1972, 4900)),
    ("TOTAL", "At 31 December 2021", (15437, 4682, 6629, 26748)),
    ("DATA", "Profit for the year", (None, 2716, None, 2716)),
    ("DATA", "Capital received", (306, None, 244, 550)),
    ("TOTAL", "At 31 December 2022", (15743, 7398, 6873, 30014)),
    ("DATA", "Profit for the year", (None, 7837, None, 7837)),
    ("DATA", "Capital received", (878, None, 834, 1712)),
    ("TOTAL", "At 31 December 2023", (16621, 15235, 7707, 39563)),
    ("DATA", "Profit for the year", (None, 4941, None, 4941)),
    ("DATA", "Dividends paid", (None, -1566, None, -1566)),
    ("DATA", "Capital received", (189, None, 225, 414)),
    ("TOTAL", "At 31 December 2024", (16810, 18610, 7932, 43352)),
    ("DATA", "Profit for the year", (None, 2790, None, 2790)),
    ("DATA", "Dividends paid", (None, -988, None, -988)),
    ("TOTAL", "At 31 December 2025", (16810, 20412, 7932, 45154)),
]

bw.add_equity_changes_sheet(
    title="The Charity Bank Limited — Statement of Changes in Equity",
    subtitle="Entity-level basis, £'000, chronological (oldest to newest). See source note at bottom.",
    headers=equity_headers,
    rows=equity_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=54,
    source_height=260,
)

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Profit/(loss) before tax", {
        "FY2025": 3724, "FY2024": 6590, "FY2023": 8990, "FY2022": 2716, "FY2021": 944,
    }),
    ("DATA", "Interest expense", {
        "FY2025": 13398, "FY2024": 12537, "FY2023": 8026, "FY2022": 2822, "FY2021": 1602,
    }),
    ("DATA", "Depreciation of property and equipment", {
        "FY2025": 102, "FY2024": 45, "FY2023": 56, "FY2022": 61, "FY2021": 59,
    }),
    ("DATA", "Amortisation of intangible assets", {
        "FY2025": 151, "FY2024": 154, "FY2023": 163, "FY2022": 164, "FY2021": 166,
    }),
    ("DATA", "Depreciation of right-of-use asset", {
        "FY2025": 143, "FY2024": 192, "FY2023": 193, "FY2022": 199, "FY2021": 198,
    }),
    ("DATA", "Movement in impairment", {
        "FY2025": -106, "FY2024": -227, "FY2023": -367, "FY2022": 1057, "FY2021": -91,
    }),
    ("DATA", "Corporation tax paid", {
        "FY2025": -1206, "FY2024": -2274,
    }),
    ("TOTAL", "Adjustments to reconcile net profit to cash flow generated from operating activities", {
        "FY2025": 16206, "FY2024": 17017, "FY2023": 17061, "FY2022": 7019, "FY2021": 2878,
    }),

    ("SECTION", "Net increase in assets relating to operating activities", {}),
    ("DATA", "Loans and advances to customers", {
        "FY2025": -32043, "FY2024": -45526, "FY2023": -11550, "FY2022": -35715, "FY2021": -31665,
    }),
    ("DATA", "Financial assets", {
        "FY2025": -18309, "FY2024": 1811, "FY2023": 2113, "FY2022": 6103, "FY2021": 4723,
    }),
    ("DATA", "Other assets", {
        "FY2025": 78, "FY2024": 93, "FY2023": -139, "FY2022": -145, "FY2021": 526,
    }),
    ("DATA", "Movement in prepayments", {
        "FY2025": -193, "FY2024": -170, "FY2023": -46, "FY2022": -105, "FY2021": 12,
    }),
    ("TOTAL", "Net increase in assets relating to operating activities", {
        "FY2025": -50467, "FY2024": -43792, "FY2023": -9622, "FY2022": -29862, "FY2021": -26404,
    }),

    ("SECTION", "Net increase in liabilities relating to operating activities", {}),
    ("DATA", "Due to customers", {
        "FY2025": 34566, "FY2024": 44212, "FY2023": 29128, "FY2022": 41264, "FY2021": 31312,
    }),
    ("DATA", "Interest paid", {
        "FY2025": -13201, "FY2024": -12422, "FY2023": -7961, "FY2022": -2744, "FY2021": -1531,
    }),
    ("DATA", "Deferred income", {
        "FY2025": -105, "FY2024": 4, "FY2023": 21, "FY2022": -58, "FY2021": -45,
    }),
    ("DATA", "Movement in accruals and accrued interest", {
        "FY2025": -425, "FY2024": 377, "FY2023": 37, "FY2022": -24, "FY2021": 118,
    }),
    ("DATA", "Other liabilities", {
        "FY2025": -84, "FY2024": 1001, "FY2023": -1903, "FY2022": 358, "FY2021": 1586,
    }),
    ("TOTAL", "Net increase in liabilities relating to operating activities", {
        "FY2025": 20751, "FY2024": 33172, "FY2023": 19322, "FY2022": 38796, "FY2021": 31440,
    }),

    ("TOTAL", "Net cash (outflow)/inflow from operating activities", {
        "FY2025": -13510, "FY2024": 6397, "FY2023": 26761, "FY2022": 15953, "FY2021": 7914,
    }),

    ("SECTION", "Investing activities", {}),
    ("DATA", "Acquisition of fixed assets", {
        "FY2025": -47, "FY2024": -236, "FY2023": -34, "FY2022": -14, "FY2021": -66,
    }),
    ("DATA", "Proceeds from sale of fixed assets", {
        "FY2022": 0, "FY2021": 1,
    }),
    ("TOTAL", "Net cash outflow from investing activities", {
        "FY2025": -47, "FY2024": -236, "FY2023": -34, "FY2022": -14, "FY2021": -65,
    }),

    ("SECTION", "Financing activities", {}),
    ("DATA", "Principal elements of lease payment", {
        "FY2025": -119, "FY2024": -167, "FY2023": -152, "FY2022": -147, "FY2021": -164,
    }),
    ("DATA", "Proceeds from issue of share capital", {
        "FY2025": 0, "FY2024": 400, "FY2023": 1712, "FY2022": 550, "FY2021": 4900,
    }),
    ("DATA", "Proceeds from issue of subordinated loan stock", {
        "FY2025": 200, "FY2024": 1170, "FY2023": 0, "FY2022": 1000, "FY2021": 1310,
    }),
    ("DATA", "Interest on subordinated loan stock", {
        "FY2025": -188, "FY2024": -80, "FY2023": -65, "FY2022": -78, "FY2021": -71,
    }),
    ("DATA", "Dividends paid to shareholders", {
        "FY2025": -988, "FY2024": -1552,
    }),
    ("TOTAL", "Net cash (outflow)/inflow from financing activities", {
        "FY2025": -1095, "FY2024": -229, "FY2023": 1495, "FY2022": 1325, "FY2021": 5975,
    }),

    ("TOTAL", "Net (decrease)/increase in cash and cash equivalents", {
        "FY2025": -14652, "FY2024": 5932, "FY2023": 28222, "FY2022": 17264, "FY2021": 13824,
    }),
    ("DATA", "Cash and cash equivalents at the beginning of the year", {
        "FY2025": 97352, "FY2024": 91420, "FY2023": 63198, "FY2022": 45934, "FY2021": 32110,
    }),
    ("TOTAL", "Cash and cash equivalents at the end of the year", {
        "FY2025": 82700, "FY2024": 97352, "FY2023": 91420, "FY2022": 63198, "FY2021": 45934,
    }),
]

bw.add_cash_flow_sheet(
    title="The Charity Bank Limited — Cash Flow Statement",
    subtitle="Entity-level basis, £'000",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=70,
    source_height=160,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Sheet: Asset Quality
# ---------------------------------------------------------------
asset_quality_rows = [
    ("SECTION", "Loans and advances to customers at amortised cost, by IFRS 9 stage", {}),
    ("DATA", "Stage 1 (12-month ECL), gross carrying amount", {"FY2025": 311418, "FY2024": 199922, "FY2023": 172112, "FY2022": 177047, "FY2021": 212641}),
    ("DATA", "Stage 2 (lifetime ECL), gross carrying amount", {"FY2025": 41592, "FY2024": 122844, "FY2023": 113183, "FY2022": 96664, "FY2021": 25429}),
    ("DATA", "Stage 3 (lifetime ECL), gross carrying amount", {"FY2025": 11526, "FY2024": 9727, "FY2023": 1672, "FY2022": 1706, "FY2021": 1632}),
    ("TOTAL", "Total gross carrying amount", {"FY2025": 364536, "FY2024": 332493, "FY2023": 286967, "FY2022": 275417, "FY2021": 239702}),
    ("SECTION", "Expected credit loss (ECL) allowance, by IFRS 9 stage", {}),
    ("DATA", "Stage 1 allowance", {"FY2025": -94, "FY2024": -102, "FY2023": -82, "FY2022": -227, "FY2021": -240}),
    ("DATA", "Stage 2 allowance", {"FY2025": -452, "FY2024": -870, "FY2023": -1204, "FY2022": -952, "FY2021": -353}),
    ("DATA", "Stage 3 allowance", {"FY2025": -932, "FY2024": -420, "FY2023": -366, "FY2022": -538, "FY2021": -414}),
    ("TOTAL", "Total ECL allowance", {"FY2025": -1478, "FY2024": -1392, "FY2023": -1652, "FY2022": -1717, "FY2021": -1007}),
    ("TOTAL", "Carrying amount (net of ECL)", {"FY2025": 363058, "FY2024": 331101, "FY2023": 285315, "FY2022": 273700, "FY2021": 238695}),
]

bw.add_asset_quality_sheet(
    title="The Charity Bank Limited — Asset Quality",
    subtitle="Loans and advances to customers at amortised cost, £'000, IFRS 9 basis. See source note at bottom.",
    rows=asset_quality_rows,
    sources_text=ASSET_QUALITY_SOURCES,
    first_col_width=88,
    source_height=220,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, f"{unit}" if unit else None,
                         rows_data, sources_text, note=note, first_col_width=48, source_height=140)


KM1_YEARS = ["FY2023", "FY2022", "FY2021"]

KM1_SOURCES = (
    "Sources - The Charity Bank Limited, 'Template UK KM1' under heading '3.4 Consolidated View of Key "
    "Ratios', GBP'000. Each year is transcribed from the edition in which it is the REPORTING year, never "
    "from a later edition's comparative column (map rule 1):\n"
    f"FY2023: Pillar 3 Disclosures 2023, p.14, 'Template UK KM1' (31 Dec 2023 column) - {P3_2023_URL}\n"
    f"FY2022: Pillar 3 Disclosures 2022, p.14-15, 'Template UK KM1' (31 Dec 2022 column) - {P3_2022_URL}\n\n"
    "UNNUMBERED TEMPLATE. Charity Bank prints the UK KM1 row set with its section headers and row labels but "
    "WITHOUT the template's row numbers, and it heads the section '3.4 Consolidated View of Key Ratios' rather "
    "than 'KM1'. It is still the template (map rule 8 - the row-set test): every row of the UK KM1 is present, "
    "including the three NSFR rows and the four buffer rows, and the table itself is captioned 'Template UK "
    "KM1'. Row labels are reproduced exactly as the Bank prints them, unnumbered.\n\n"
    "FY2021 IS THE FY2022 EDITION'S COMPARATIVE COLUMN, not an own-edition year - filled under map rule 28. "
    "Charity Bank's FY2021 Pillar 3 Disclosures (35 pages) contain NO KM1 template at all: zero occurrences of "
    "'KM1' and zero of 'LCR', against a richness control on the same extraction of 'capital' 148, 'ratio' 92, "
    "'own funds' 14, 'leverage' 14, 'liquidity' 13 - so that zero is a fact about the document, not a failed "
    "extraction (map rule 15). The template took effect 1 January 2022 and FY2021 ended 31 December 2021, so no "
    "own-edition KM1 can exist and rule 1 has no original to protect. This is rule 28's whole-missing-table "
    "case, NOT rule 20 (which governs a single row dashed in an own edition that does exist, and is "
    "untouched): every FY2021 figure on this sheet is taken from the 31 Dec 2021 comparative column printed in "
    f"the Pillar 3 Disclosures 2022, p.14-15 - {P3_2022_URL} .\n"
    "Where that comparative column itself prints nothing, the cell stays blank: the three NSFR rows are empty "
    "for 31 Dec 2021 under the edition's own footnote, 'Note that NSFR became a reportable regulatory "
    "requirement from Jan 1st 2022, therefore no results for 2021 have been included'. Filling a column from a "
    "comparative does not license inventing the cells the comparative leaves empty.\n"
    "The single-metric sheets carry FY2021 from this same comparative, so the two agree by construction.\n\n"
    "FY2024 AND FY2025 - BLANK, WITH AN AFFIRMATIVE AND DATE-FITTED EXPLANATION. Charity Bank stopped "
    "publishing Pillar 3 after the FY2023 edition, and says so itself in that edition's section 7: 'On 5th "
    "December 2023 the PRA released PS15/23 ... the PRA confirmed that Small Domestic Deposit Takers (SDDT's) "
    "without listed instruments would be excluded from the requirement to disclose a Pillar 3 report. Charity "
    "Bank falls into this category of firm; as such, management anticipate this will be the last publicly "
    "disclosed Pillar 3 report (unless and until regulatory requirements change).' The Bank of England "
    "consolidated waivers register (downloaded 2026-09-16) corroborates it with an exact date: FRN 207701, 'The "
    "Charity Bank Limited', 'Modification by Consent - PRA Rulebook - CRR Firms - Rule 3.1 of the SDDT Regime - "
    "General Application Part', sub rule 'Ru 3.1', ref A00007506P.pdf, START DATE 01/02/2024, no end date. DATE "
    "FIT: Charity Bank's year-end is 31 December, so the opt-in precedes the whole of FY2024 and FY2025 and "
    "explains both; it does NOT reach back to FY2023 or earlier, which is why those years carry a full "
    "template. Only a Rule 3.1 row removes the disclosure obligation - this is the SDDT DISCLOSURE exemption in "
    "force now, not the separate SDDT CAPITAL regime beginning 1 January 2027.\n\n"
    "PRECISION IS THE BANK'S OWN (map rule 3), including where it drifts between editions: the FY2022 edition "
    "prints 'Additional CET1 SREP requirements 0.330%' and 'Total SREP own funds requirements 8.590%', while "
    "the FY2023 edition restates the same FY2022 figures as 0.332% and prints 8.59% to two decimals. Each "
    "column here shows what its own edition printed, so 0.330%/8.590% stand for FY2022. Within the FY2023 "
    "column the Bank mixes precisions in the same table (9.64% beside 8.385%, 2.000% beside 2.500%); that is "
    "house style and is reproduced, not normalised. ONE CONSEQUENCE IS VISIBLE TO THE WORKBOOK'S OWN CHECKER: "
    "this sheet prints the FY2022 leverage ratio excluding claims on central banks as 8.385%, while the "
    "Leverage Ratio sheet carries the same disclosed figure as the Bank printed it elsewhere, 8.39%. These are "
    "the SAME figure at two printed precisions, not two measurements, and neither has been altered to match the "
    "other. The pair is recorded here because it is real and a reader comparing the two sheets will notice it, not "
    "because anything is wrong with either figure. (It briefly surfaced as a checker disagreement: the "
    "difference is exactly half a unit of the coarser printing, so it sat precisely on verify_workbook.py's "
    "tolerance boundary and was tipped over by binary floating point. The checker gained an epsilon on "
    "2026-09-17 and no longer reports it. Neither figure was altered at any point.)\n\n"
    "LATEST-EDITION CHECK, 16 September 2026: charitybank.org's own '/reports-and-publications/' page lists "
    "Annual Reports for 2025 and 2024 and NO Pillar 3 document of any year. The WordPress media API returned "
    "HTTP 403 on every query including the empty control, so that route proves nothing either way (map rule 9 - "
    "a blocked fetch is not an absence); the page listing above was reached instead via the site's own "
    "robots.txt sitemap index. Newest Pillar 3 edition published: FY2023. The three Pillar 3 URLs cited by this "
    "workbook are Wayback captures because the live copies have since been withdrawn from the site."
)

km1_rows = [
    ("SECTION", "Available own funds (£000)", {}),
    ("DATA", "Common Equity Tier 1 (CET1) capital (£'000)", {"FY2023": 30701, "FY2022": 26146, "FY2021": 24522}),
    ("DATA", "Tier 1 capital (£'000)", {"FY2023": 30701, "FY2022": 26146, "FY2021": 24522}),
    ("DATA", "Total capital (£'000)", {"FY2023": 33541, "FY2022": 29878, "FY2021": 27812}),
    ("SECTION", "Risk-weighted exposure amounts (£000)", {}),
    ("DATA", "Total risk-weighted exposure amount (£'000)", {"FY2023": 190056, "FY2022": 173774, "FY2021": 153193}),
    ("SECTION", "Capital ratios (as a percentage of risk-weighted exposure amount)", {}),
    ("DATA", "Common Equity Tier 1 ratio (%)", {"FY2023": "16.15%", "FY2022": "15.05%", "FY2021": "16.01%"}),
    ("DATA", "Tier 1 ratio (%)", {"FY2023": "16.15%", "FY2022": "15.05%", "FY2021": "16.01%"}),
    ("DATA", "Total capital ratio (%)", {"FY2023": "17.65%", "FY2022": "17.19%", "FY2021": "18.15%"}),
    ("SECTION", "Additional own funds requirements based on SREP (as a percentage of risk-weighted exposure amount)", {}),
    ("DATA", "Additional CET1 SREP requirements (%)", {"FY2023": "0.332%", "FY2022": "0.330%", "FY2021": "0.330%"}),
    ("DATA", "Additional AT1 SREP requirements (%)", {"FY2023": "0.111%", "FY2022": "0.112%", "FY2021": "0.112%"}),
    ("DATA", "Additional T2 SREP requirements (%)", {"FY2023": "0.148%", "FY2022": "0.148%", "FY2021": "0.148%"}),
    ("DATA", "Total SREP own funds requirements (%)", {"FY2023": "8.59%", "FY2022": "8.590%", "FY2021": "8.590%"}),
    ("SECTION", "Combined buffer requirement (as a percentage of risk-weighted exposure amount)", {}),
    ("DATA", "Capital conservation buffer (%)", {"FY2023": "2.500%", "FY2022": "2.500%", "FY2021": "2.500%"}),
    ("DATA", "Conservation buffer due to macro-prudential or systemic risk identified at the level of a Member State (%)", {"FY2023": "0%", "FY2022": "0%", "FY2021": "0%"}),
    ("DATA", "Institution specific countercyclical capital buffer (%)", {"FY2023": "2.000%", "FY2022": "1.000%", "FY2021": "0%"}),
    ("DATA", "Systemic risk buffer (%)", {"FY2023": "0%", "FY2022": "0%", "FY2021": "0%"}),
    ("DATA", "Global Systemically Important Institution buffer (%)", {"FY2023": "0%", "FY2022": "0%", "FY2021": "0%"}),
    ("DATA", "Other Systemically Important Institution buffer", {"FY2023": "0%", "FY2022": "0%", "FY2021": "0%"}),
    ("DATA", "Combined buffer requirement (%)", {"FY2023": "4.500%", "FY2022": "3.500%", "FY2021": "2.500%"}),
    ("DATA", "Overall capital requirements (%)", {"FY2023": "13.09%", "FY2022": "12.09%", "FY2021": "11.09%"}),
    ("DATA", "CET1 available after meeting the total SREP own funds requirements (%)", {"FY2023": "11.32%", "FY2022": "10.24%", "FY2021": "11.2%"}),
    ("SECTION", "Leverage ratio", {}),
    ("DATA", "Total exposure measure excluding claims on central banks (£'000)", {"FY2023": 318506, "FY2022": 311813, "FY2021": 317557}),
    ("DATA", "Leverage ratio excluding claims on central banks (%)", {"FY2023": "9.64%", "FY2022": "8.385%", "FY2021": "7.722%"}),
    ("SECTION", "Liquidity Coverage Ratio", {}),
    ("DATA", "Total high-quality liquid assets (HQLA) (Weighted value -average) (£'000)", {"FY2023": 80628, "FY2022": 60685, "FY2021": 67018}),
    ("DATA", "Cash outflows - Total weighted value (£'000)", {"FY2023": 53461, "FY2022": 45791, "FY2021": 39841}),
    ("DATA", "Cash inflows - Total weighted value (£'000)", {"FY2023": 13724, "FY2022": 12126, "FY2021": 9498}),
    ("DATA", "Total net cash outflows (adjusted value) (£'000)", {"FY2023": 39737, "FY2022": 33665, "FY2021": 30343}),
    ("DATA", "Liquidity coverage ratio (%)", {"FY2023": "206.0%", "FY2022": "182.2%", "FY2021": "222.4%"}),
    ("SECTION", "Net Stable Funding Ratio (FY2021 blank in the source: the requirement took effect 1 Jan 2022)", {}),
    ("DATA", "Total available stable funding (£'000)", {"FY2023": 308698, "FY2022": 277789}),
    ("DATA", "Total required stable funding (£'000)", {"FY2023": 220941, "FY2022": 204829}),
    ("DATA", "NSFR ratio (%)", {"FY2023": "139.7%", "FY2022": "135.6%"}),
]

bw.add_km1_sheet(
    title="The Charity Bank Limited - KM1 Key Metrics",
    subtitle="'Template UK KM1' as published, GBP'000, unnumbered rows as the Bank prints them. FY2023 and "
             "FY2022 are own-edition years; FY2021 is the FY2022 edition's comparative column (map rule 28), "
             "the template postdating that year. FY2024-FY2025 have no Pillar 3 at all - the Bank ceased "
             "disclosure under the SDDT exemption (PRA Rule 3.1, from 01/02/2024) - see source note",
    rows=km1_rows,
    sources_text=KM1_SOURCES,
    first_col_width=88,
    source_height=680,
    years=KM1_YEARS,
)

metric(
    "CET1 Capital", "£'000",
    [("Common Equity Tier 1 (CET1) capital", {
        "FY2025": 41644, "FY2024": 37540, "FY2023": 30701, "FY2022": 26146, "FY2021": 24522,
    })],
    p3_sources(),
)

metric(
    "CET1 Ratio", "%",
    [("Common Equity Tier 1 (CET1) ratio", {
        "FY2025": "17.33%", "FY2024": "16.67%", "FY2023": "16.15%", "FY2022": "15.05%", "FY2021": "16.01%",
    })],
    p3_sources(),
)

metric(
    "Tier 1 Capital", "£'000",
    [("Tier 1 capital", {
        "FY2025": 41644, "FY2024": 37540, "FY2023": 30701, "FY2022": 26146, "FY2021": 24522,
    })],
    p3_sources(),
    note="Tier 1 capital equals CET1 capital in every year shown - Charity Bank has no Additional Tier 1 (AT1) "
         "instruments.",
)

metric(
    "Tier 1 Ratio", "%",
    [("Tier 1 ratio", {
        "FY2025": "17.33%", "FY2024": "16.67%", "FY2023": "16.15%", "FY2022": "15.05%", "FY2021": "16.01%",
    })],
    p3_sources(),
    note="Equal to the CET1 ratio every year shown - no Additional Tier 1 (AT1) instruments.",
)

metric(
    "Total Capital", "£'000",
    [("Total capital", {
        "FY2025": 47044, "FY2024": 42376, "FY2023": 33541, "FY2022": 29878, "FY2021": 27812,
    })],
    p3_sources(),
)

metric(
    "Total Capital Ratio", "%",
    [("Total capital ratio", {
        "FY2025": "19.58%", "FY2024": "18.82%", "FY2023": "17.65%", "FY2022": "17.19%", "FY2021": "18.15%",
    })],
    p3_sources(),
)

metric(
    "Total RWAs", "£'000",
    [("Total risk-weighted exposure amount", {
        "FY2025": 240287, "FY2024": 225196, "FY2023": 190056, "FY2022": 173774, "FY2021": 153193,
    })],
    p3_sources(),
)

rwa_breakdown_rows = [
    ("SECTION", "RWA by risk category", {}),
    ("DATA", "Credit risk (excluding CCR)", {"FY2023": 169233, "FY2022": 160312, "FY2021": 143316}),
    ("DATA", "Operational risk", {"FY2023": 20823, "FY2022": 13462, "FY2021": 9877}),
    ("TOTAL", "Total RWAs", {"FY2025": 240287, "FY2024": 225196, "FY2023": 190056, "FY2022": 173774, "FY2021": 153193}),
]

bw.add_rwa_breakdown_sheet(
    title="The Charity Bank Limited — RWA Breakdown",
    subtitle="£'000. No market risk or counterparty credit risk exposure (Charity Bank holds no trading book) - "
              "category split not published for FY2025/FY2024 (standalone Pillar 3 disclosure ceased after the "
              "FY2023 edition; re-confirmed 2026-09-12, Wayback CDX shows no Pillar 3 filename crawled on "
              "charitybank.org past the 2023 edition). See source note at bottom.",
    rows=rwa_breakdown_rows,
    sources_text=RWA_BREAKDOWN_SOURCES,
    first_col_width=54,
    source_height=280,
    unit_suffix=" (£'000)",
)

metric(
    "Leverage Ratio", "%",
    [("Leverage ratio", {
        "FY2025": "10.13%", "FY2024": "10.39%", "FY2023": "9.64%", "FY2022": "8.39%", "FY2021": "7.72%",
    })],
    p3_sources(),
    note=LEVERAGE_BASIS_NOTE,
)

# GAP-FILL (2026-09-18): FY2024 and FY2025 previously carried NO cell on the LCR
# and NSFR sheets, so four sheet-years read as blank to audit_gaps.py even though
# the finding was complete. The finding is now stated IN the columns.
# EVIDENCE RE-VERIFIED 2026-09-18, three independent ways:
#   (1) No Pillar 3 edition exists for either year. Wayback CDX for every
#       charitybank.org Pillar 3 PDF ever captured ends at
#       PILLAR-3-disclosures-2023.pdf; there is no 2024 or 2025 file. Charity Bank
#       has since removed the whole Pillar 3 series from its live site - the
#       verbatim 2023 URL used by this script now returns HTTP 404 - so a live-site
#       search cannot settle the question either way and the archive is the
#       instrument that can.
#   (2) The Annual Reports disclose neither ratio. Both editions have genuine text
#       layers (2024: 228,666 chars over 98pp; 2025: 229,517 over 100pp), and both
#       return ZERO hits for 'LCR', 'liquidity coverage', 'NSFR' and 'net stable
#       funding' against a richness control of 329/317 hits for 'Charity Bank' on
#       the same extraction. Neither report mentions Pillar 3 AT ALL: all 17
#       'pillar' hits in each are Pillar 1 / Pillar 2A / Pillar 2B CAPITAL
#       requirements, which are a different regime from Pillar 3 DISCLOSURE.
#   (3) The PRA register carries the opt-in that removes the duty - see
#       PILLAR3_NOTE. Charity Bank's year end is 31 December (confirmed in both
#       reports), so a modification effective 01/02/2024 covers FY2024 and FY2025
#       and neither FY2023 nor earlier.
SDDT_NO_P3 = ("Not published - SDDT regime, no Pillar 3 disclosure required from FY2024; "
              "not disclosed in the Annual Report either")

metric(
    "LCR", "%",
    [("Liquidity Coverage Ratio (LCR)", {
        "FY2025": SDDT_NO_P3, "FY2024": SDDT_NO_P3,
        "FY2023": "206.0%", "FY2022": "182.2%", "FY2021": "222.4%",
    })],
    p3_sources(),
    note="FY2021 is disclosed in the FY2022 Pillar 3 document's comparative column (222.4%). FY2024-FY2025 are "
         "NOT a transcription gap: no standalone Pillar 3 document has been published for either year (the "
         "archived series ends at the 2023 edition) and the Annual Reports do not disclose LCR at all - zero "
         "hits for 'LCR' or 'liquidity coverage' in either, against a 329/317-hit control for 'Charity Bank' on "
         "the same text extraction. See the Pillar 3 note on this sheet's source citation for the PRA "
         "modification that removes the duty.",
)

metric(
    "NSFR", "%",
    [("Net Stable Funding Ratio (NSFR)", {
        "FY2025": SDDT_NO_P3, "FY2024": SDDT_NO_P3,
        "FY2023": "139.7%", "FY2022": "135.6%",
    })],
    p3_sources(),
    note="Blank FY2021 (not disclosed in that year's Pillar 3 document, and predates the UK NSFR requirement in "
         "any case - PS22/21). FY2024-FY2025 are a regulatory absence, not a search miss: no standalone Pillar 3 "
         "document was published for either year and the Annual Reports do not disclose NSFR at all (zero hits "
         "for 'NSFR' and 'net stable funding' in both, same controls as the LCR sheet). Becoming an SDDT also "
         "replaces the full NSFR with a Simplified Retail Deposit Ratio, and Charity Bank publishes no value for "
         "that either, so nothing replaces the series here.",
)

bw.add_not_disclosed_metric_sheets(
    ["MREL Ratio"],
    p3_sources(),
    per_note={
        "MREL Ratio": "Not disclosed in any Pillar 3 document or Annual Report found for any year FY2021-FY2025 "
                      "- no explicit exemption stated, simply absent from every source.",
    },
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {"FY2025": 481812, "FY2024": 445667, "FY2023": 395967, "FY2022": 358050, "FY2021": 312072}),
        ("Loans and advances to customers", {"FY2025": 363058, "FY2024": 331101, "FY2023": 285315, "FY2022": 273700, "FY2021": 238695}),
        ("Customer accounts", {"FY2025": 421741, "FY2024": 387175, "FY2023": 342963, "FY2022": 313835, "FY2021": 272571}),
        ("Total equity", {"FY2025": 45154, "FY2024": 43352, "FY2023": 39563, "FY2022": 30014, "FY2021": 26748}),
    ],
    balance_sheet_unit="£'000",
    income_statement_totals=[
        ("Net total income", {"FY2025": 15128, "FY2024": 16760, "FY2023": 16755, "FY2022": 10172, "FY2021": 6404}),
        ("Administrative expenses", {"FY2025": -11066, "FY2024": -9775, "FY2023": -7818, "FY2022": -6010, "FY2021": -5141}),
        ("Profit after taxation and total comprehensive income for the year", {"FY2025": 2790, "FY2024": 4941, "FY2023": 7837, "FY2022": 2716, "FY2021": 944}),
    ],
    income_statement_unit="£'000",
    equity_changes_totals=[
        ("Opening equity", {"FY2025": 43352, "FY2024": 39563, "FY2023": 30014, "FY2022": 26748}),
        ("Total comprehensive income for the year", {"FY2025": 2790, "FY2024": 4941, "FY2023": 7837, "FY2022": 2716, "FY2021": 944}),
        ("Other equity movements, net", {"FY2025": -988, "FY2024": -1152, "FY2023": 1712, "FY2022": 550, "FY2021": 4900}),
        ("Closing equity", {"FY2025": 45154, "FY2024": 43352, "FY2023": 39563, "FY2022": 30014, "FY2021": 26748}),
    ],
    equity_changes_unit="£'000",
    cash_flow_totals=[
        ("Net cash (outflow)/inflow from operating activities", {
            "FY2025": -13510, "FY2024": 6397, "FY2023": 26761, "FY2022": 15953, "FY2021": 7914,
        }),
        ("Net cash outflow from investing activities", {
            "FY2025": -47, "FY2024": -236, "FY2023": -34, "FY2022": -14, "FY2021": -65,
        }),
        ("Net cash (outflow)/inflow from financing activities", {
            "FY2025": -1095, "FY2024": -229, "FY2023": 1495, "FY2022": 1325, "FY2021": 5975,
        }),
        ("Cash and cash equivalents at end of year", {
            "FY2025": 82700, "FY2024": 97352, "FY2023": 91420, "FY2022": 63198, "FY2021": 45934,
        }),
    ],
    cash_flow_unit="£'000",
    ratios=[
        ("CET1 Ratio", {
            "FY2025": 17.33, "FY2024": 16.67, "FY2023": 16.15, "FY2022": 15.05, "FY2021": 16.01,
        }),
        ("Tier 1 Ratio", {
            "FY2025": 17.33, "FY2024": 16.67, "FY2023": 16.15, "FY2022": 15.05, "FY2021": 16.01,
        }),
        ("Total Capital Ratio", {
            "FY2025": 19.58, "FY2024": 18.82, "FY2023": 17.65, "FY2022": 17.19, "FY2021": 18.15,
        }),
        ("Leverage Ratio", {
            "FY2025": 10.13, "FY2024": 10.39, "FY2023": 9.64, "FY2022": 8.39, "FY2021": 7.72,
        }),
        ("LCR", {
            "FY2023": 206.0, "FY2022": 182.2,
        }),
        ("NSFR", {
            "FY2023": 139.7, "FY2022": 135.6,
        }),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own "
         "source citation for the underlying document/page. " + ENTITY_NOTE + "\n\n" + PILLAR3_NOTE,
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/CHARITY BANK FINANCIALS.xlsx")
print("Saved CHARITY BANK FINANCIALS.xlsx")
