import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first, y/e 30 September

CH_FY2025_URL = "https://find-and-update.company-information.service.gov.uk/company/07454474/filing-history/MzUwMDY5OTYyMGFkaXF6a2N4/document?format=pdf&download=0"
CH_FY2024_URL = "https://find-and-update.company-information.service.gov.uk/company/07454474/filing-history/MzQ1MzY3NTE2MGFkaXF6a2N4/document?format=pdf&download=0"
CH_FY2023_URL = "https://find-and-update.company-information.service.gov.uk/company/07454474/filing-history/MzQxNTc2MDk1NGFkaXF6a2N4/document?format=pdf&download=0"
CH_FY2022_URL = "https://find-and-update.company-information.service.gov.uk/company/07454474/filing-history/MzM2MzAyNjk5NGFkaXF6a2N4/document?format=pdf&download=0"
CH_FY2021_URL = "https://find-and-update.company-information.service.gov.uk/company/07454474/filing-history/MzMzNDg3NzA5MWFkaXF6a2N4/document?format=pdf&download=0"

P3_2025_URL = "https://www.castletrust.co.uk/wp-content/uploads/fy-30_sept-2025-ctb-pillar-3-disclosures.pdf"
P3_2024_URL = "https://www.castletrust.co.uk/wp-content/uploads/fy-30_sept-2024-ctb-pillar-3-disclosures.pdf"
P3_2023_URL = "https://www.castletrust.co.uk/wp-content/uploads/fy-30-sept-2023-ctb-pillar-3-disclosures.pdf"
P3_2022_URL = "https://www.castletrust.co.uk/wp-content/uploads/fy-30-sept-2022-ctb-pillar-3-disclosures.pdf"
P3_2021_URL = "https://www.castletrust.co.uk/wp-content/uploads/fy-30-sept-2021-ctb-pillar-3-disclosures.pdf"
# Sixth live edition. Outside this workbook's FY2021-FY2025 window, so it supplies no column here;
# recorded because it is the earliest edition published and because its Appendix 4 independently
# confirms the FY2020 comparatives printed in the FY2021 edition (CET1/Total capital GBP72,042k,
# total RWA GBP372,306k, CET1 ratio 19.35%, leverage 9.86%).
P3_2020_URL = "https://www.castletrust.co.uk/wp-content/uploads/fy-30-sept-2020-ctb-pillar-3-disclosures.pdf"
# A byte-identical copy of the FY2024 document (verified 2026-09-15: same MD5, 1,434,534 bytes),
# NOT a separate edition. Recorded so it is never counted or cited as one.
P3_2024_DUPLICATE_URL = "https://www.castletrust.co.uk/wp-content/uploads/2025/05/Pillar-3-Document.pdf"

URL_PROVENANCE_NOTE = (
    "PILLAR 3 URL PROVENANCE (re-verified 2026-09-15 - every URL above and below was fetched and confirmed to "
    "return real PDF content, i.e. '%PDF' magic bytes and a readable text layer, not a soft-404 HTML page):\n"
    "  * Castle Trust's filename separator is INCONSISTENT between years and must not be permuted or "
    "'corrected'. FY2020-FY2023 use 'fy-30-sept-<year>-...' (hyphen); FY2024 and FY2025 use "
    "'fy-30_sept-<year>-...' (UNDERSCORE between '30' and 'sept'). Six editions are live in total, one per "
    "financial year FY2020 through FY2025, all under https://www.castletrust.co.uk/wp-content/uploads/ .\n"
    f"  * {P3_2024_DUPLICATE_URL} is byte-identical to the FY2024 edition (same MD5) and is a duplicate copy, "
    "not a seventh edition or a separate reporting period.\n"
    "  * Period dates were taken from each document's own cover and scope paragraph, not from its filename; "
    "all six agree with their filenames."
)

ENTITY_NOTE = (
    "Castle Trust Capital plc (company 07454474, FRN 541910, trading as 'Castle Trust Bank') is a "
    "wholly-owned subsidiary of Castle Trust Holdings Limited ('CTH', company 12161224) and has availed "
    "itself of the exemption under s.400 Companies Act 2006 to not prepare group accounts - its own "
    "statutory accounts (sourced here) are solo/Company-only, not consolidated, and are a genuinely "
    "different document from CTH's own consolidated 'Annual report and financial statements' (also "
    "published on the bank's website) which cover the wider Group. Cash flow figures on this sheet are "
    "Castle Trust Capital plc solo, matching the Pillar 3 sheets' 'Bank' (not 'Group') columns - kept "
    "consistent throughout to avoid a cash-flow-vs-Pillar-3 basis mismatch. All 5 Companies House filings "
    "for this entity are fully scanned/image-only; figures were transcribed via page rendering and "
    "cross-checked against each year's own report where it appears again as the following year's "
    "comparative column.\n"
    "One genuine cross-vintage discrepancy found, not silently resolved: the FY2022 Annual Report's own "
    "note states 'Certain items in operating activities have been reclassified in the prior year "
    "comparatives for presentational purposes. The changes had no impact on the net cashflows from "
    "operating activities' - but its FY2021 comparative operating-activities total is stated as "
    "£(57,981)k, which does NOT match FY2021's own originally-published total of £(62,617)k (a £4,636k "
    "difference), despite the note's claim of no impact. FY2021's own originally-published figure is used "
    "in the FY2021 column here, per project convention; the discrepancy itself is flagged here rather than "
    "silently reconciled either way. All other tail-chain closing/opening balances tie exactly year to "
    "year with no gap."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are Castle Trust Capital plc's own Company-only (solo) Statement of Cash Flows, £'000:\n"
    f"FY2025 (& FY2024 comparative): Castle Trust Capital plc Annual financial statements, y/e 30 Sept 2025, p.59 - {CH_FY2025_URL}\n"
    f"FY2024 (& FY2023 comparative): Castle Trust Capital plc Annual financial statements, y/e 30 Sept 2024, p.58 - {CH_FY2024_URL}\n"
    f"FY2023 (& FY2022 comparative): Castle Trust Capital plc Annual financial statements, y/e 30 Sept 2023, p.55 - {CH_FY2023_URL}\n"
    f"FY2022 (& FY2021 comparative): Castle Trust Capital plc Annual financial statements, y/e 30 Sept 2022, p.48 - {CH_FY2022_URL}\n"
    f"FY2021 (& FY2020 comparative): Castle Trust Capital plc Annual financial statements, y/e 30 Sept 2021, p.41 - {CH_FY2021_URL}\n"
    + ENTITY_NOTE
)


ENTITY_BASIS_NOTE = (
    "ENTITY BASIS - determined 2026-09-15 by reading the scope/basis section of all SIX live editions.\n"
    "Every edition is PUBLISHED BY the holding company and carries 'Registered No: 12161224' on its cover - "
    "that is Castle Trust Holdings Limited, NOT the bank. It is not the basis of the figures used here, and the\n"
    "cover number must not be read as one. Each document nonetheless presents the Bank separately from the\n"
    "Group, and every figure in this workbook is taken from the BANK presentation.\n"
    "Verbatim, from each edition's own Scope section:\n"
    "  FY2020: 'This document sets out the consolidated Pillar 3 disclosures of Castle Trust Holdings Limited\n"
    "    (\"the Group\") which includes Castle Trust Capital plc (\"the Bank\") and its directly owned\n"
    "    subsidiaries as at 30 September 2020.'\n"
    "  FY2021: identical wording, '...as at 30 September 2021.'\n"
    "  FY2022: identical wording, '...as at 30 September 2022.'\n"
    "  FY2023: 'Castle Trust Holdings Limited (the \"Group\") was incorporated on 16 August 2019 to act as a\n"
    "    holding company of the Castle Trust Capital (CTC) group... This document sets out the consolidated\n"
    "    Pillar 3 disclosures of the Group which includes Castle Trust Capital plc (\"the Bank\") and its\n"
    "    directly owned subsidiaries as at 30 September 2023.'\n"
    "  FY2024 and FY2025: same two-paragraph wording as FY2023, with their own year.\n"
    "All six also state that Castle Trust Capital plc is the PRA/FCA-authorised firm, 'registered number\n"
    "541910', and the FY2021, FY2022, FY2024 and FY2025 editions carry a closing legal line reading 'Castle\n"
    "Trust Bank means Castle Trust Capital plc, a company incorporated in England and Wales with company\n"
    "number 07454474' - i.e. the document's own definition of 'the Bank' is this workbook's entity.\n"
    "\n"
    "SINGLE CONSOLIDATED SET, OR SEPARATE BANK AND GROUP COLUMNS? Separate, in every edition, but in two\n"
    "different formats:\n"
    "  FY2022-FY2025 (KM1-era): each document has TWO full key-metrics tables, headed 'Key Metrics for the\n"
    "    Group' and 'Key Metrics for the Bank' (pp.5 and 6; the FY2025 edition adds 'Overview of RWEAs for\n"
    "    Group' and 'Overview of RWEAs for Bank' on p.7). The FY2024 edition's basis section says so directly:\n"
    "    'These disclosures are based upon the Group's Financial Statements... Both the Group and the Bank\n"
    "    calculate capital resources and requirements using the Basel III framework'; the FY2022 edition says\n"
    "    'The key metrics disclosures have been prepared for both the Group and the Bank as required per\n"
    "    Article 18 of the CRR.'\n"
    "  FY2020-FY2021 (pre-KM1): the MAIN BODY is Group-only and its headline table is captioned 'Key Metrics\n"
    "    for the Business... for the Group'. The Bank appears only in 'Appendix 4. Bank Disclosures'. Both\n"
    "    editions' basis sections say: 'These disclosures have been prepared for the Group with the exception\n"
    "    of Appendix 4 which shows the required disclosures for the Bank as per Article 18 of the Capital\n"
    "    Requirements Regulation EU 575/2013 (\"CRR\").' The FY2021 Appendix 4 opens: 'The following tables\n"
    "    detail the capital reporting disclosures for Castle Trust Capital plc (\"the Bank\") as a standalone\n"
    "    solo legal entity.'\n"
    "\n"
    "WHICH COLUMN THIS WORKBOOK USES: the Bank column, in every year and on every sheet - FY2022-FY2025 from\n"
    "'Key Metrics for the Bank', FY2021 from 'Appendix 4. Bank Disclosures'. Confirmed 2026-09-15 against all\n"
    "six primary documents. The divergence is large enough that the two bases could never be blended: FY2023\n"
    "Bank CET1 83,177 / RWA 413,907 / CET1 ratio 20.10% against Group 99,699 / 592,678 / 16.82%; FY2022 Bank\n"
    "357,870 against Group 530,968. NO Holdings-basis figure is written into any sheet of this workbook.\n"
    "\n"
    "ONE BASIS CAVEAT INSIDE THE BANK COLUMN ITSELF, flagged not smoothed over. The FY2021 Appendix 4 defines\n"
    "the Bank as 'a standalone solo legal entity', and adds: 'In the prior year the Bank's disclosures also\n"
    "incorporated the financial performance and balances of Castle Trust Capital Management Limited and Castle\n"
    "Trust Direct plc.' The FY2020 edition confirms this from the other side: 'For capital reporting purposes,\n"
    "Castle Trust Capital plc's (\"the Bank\") disclosures also incorporate the financial performance and\n"
    "balances of Castle Trust Capital Management Limited and Castle Trust Direct plc.' So the FY2020 Bank\n"
    "column is Castle Trust Capital plc plus two of its own subsidiaries, while FY2021 onward is CTC plc solo.\n"
    "This affects no cell here - FY2020 is outside this workbook's five-year window - but it is the reason\n"
    "FY2020 is not backfilled from that edition without a basis label."
)


def p3_sources(page="6"):
    return (
        "Sources - Castle Trust Bank Pillar 3 Disclosures, 'Key Metrics for the Bank' table (Castle Trust "
        "Capital plc solo basis, not the wider CTH Group):\n"
        f"FY2025: Pillar 3 Disclosures FY ended 30 Sept 2025, p.{page} - {P3_2025_URL}\n"
        f"FY2024: Pillar 3 Disclosures FY ended 30 Sept 2024, p.{page} - {P3_2024_URL}\n"
        f"FY2023: Pillar 3 Disclosures FY ended 30 Sept 2023, p.{page} - {P3_2023_URL}\n"
        f"FY2022: Pillar 3 Disclosures FY ended 30 Sept 2022, p.{page} - {P3_2022_URL}\n"
        "FY2021: Pillar 3 Disclosures FY ended 30 Sept 2021 (pre-KM1 template - 'Appendix 4. Bank "
        f"Disclosures'), p.40-43 - {P3_2021_URL}\n\n"
        + ENTITY_BASIS_NOTE + "\n\n" + URL_PROVENANCE_NOTE + "\n\n"
        "SDDT - EXPLICIT NEGATIVE, recorded 2026-09-15 (cross-bank SDDT date-fit pass) so that a future pass "
        "does not wrongly apply the Small Domestic Deposit Taker exemption to this workbook's gap year. Castle "
        "Trust DOES hold the SDDT opt-in, but it is far too recent to explain anything here. The Bank of England "
        "consolidated list of waivers and modifications granted to PRA-authorised firms (downloaded 2026-09-15, "
        "https://www.bankofengland.co.uk/-/media/boe/files/prudential-regulation/authorisations/"
        "waivers-and-modifications-of-rules/consolidated-waivers-pra-firms.csv) carries three SDDT rows for FRN "
        "541910, 'Castle Trust Capital PLC': (a) Rule 3.1 of the SDDT Regime - General Application Part, sub "
        "rule 'Ru 3.1', waiver ref 'A00011417P.pdf', START DATE 06/01/2026, no end date; (b) Rule 3.2, ref "
        "'A00011424P.pdf', same start date; and (c) 'CRR firms: SDDT Regime - General Application Part 1.2 & "
        "2.1(9)', ref 'A00011283P.pdf', start 01/12/2025, end 01/12/2028. Only row (a) is the opt-in that "
        "removes the Pillar 3 disclosure obligation; row (c) modifies ELIGIBILITY CRITERIA only and would not by "
        "itself make the firm a confirmed SDDT.\n"
        "DATE FIT - IT DOES NOT FIT. Castle Trust's accounting reference date is 30 SEPTEMBER, confirmed at "
        "Companies House (company 07454474, an unbroken run of accounts to 30 September from 2015 to 2025) - "
        "note this is NOT a December year-end. The outstanding gap year is FY2021, which ended 30 SEPTEMBER "
        "2021. The Rule 3.1 modification began 6 JANUARY 2026 - more than four years later. A modification "
        "cannot explain a gap that predates it, so the SDDT regime explains NONE of the FY2021 blanks.\n"
        "FY2021's gap keeps its existing and entirely separate explanation, unchanged: Castle Trust published a "
        "full Pillar 3 document for FY2021, but on the PRE-KM1 template ('Appendix 4. Bank Disclosures'), which "
        "simply does not carry every line the later KM1 tables do. That is a template-vintage gap in a document "
        "that exists, which is the opposite of an exemption from publishing one. The register finding changes no "
        "cell in this workbook. Note too that the Bank published a Pillar 3 document for FY2025, whose 30 "
        "September 2025 year-end precedes the 6 January 2026 modification - consistent with the dates, and a "
        "reminder that the exemption bites only from FY2026 onward. This is the SDDT DISCLOSURE exemption, in "
        "force now - not the separate SDDT CAPITAL regime beginning 1 January 2027."
    )


NOT_DISCLOSED_NOTE = "Not found in any of the 5 Pillar 3 Disclosures documents reviewed - no MREL figure or exemption statement given at any point."


bw = BankWorkbook(bank_name="Castle Trust Capital plc", years=YEARS, header_color="6A4C93")

STATEMENTS_SOURCES = (
    "Sources - Castle Trust Capital plc's own Statement of Financial Position / Statement of Comprehensive "
    "Income / Statement of Changes in Equity, each year's own originally-published figures (not a later year's "
    "comparative column), £'000:\n"
    f"FY2025: Annual financial statements, y/e 30 Sept 2025, pp.56-58 - {CH_FY2025_URL}\n"
    f"FY2024: Annual financial statements, y/e 30 Sept 2024, pp.55-57 - {CH_FY2024_URL}\n"
    f"FY2023: Annual financial statements, y/e 30 Sept 2023, pp.52-54 - {CH_FY2023_URL}\n"
    f"FY2022: Annual financial statements, y/e 30 Sept 2022, pp.45-47 - {CH_FY2022_URL}\n"
    f"FY2021: Annual financial statements, y/e 30 Sept 2021, pp.38-40 - {CH_FY2021_URL}\n"
    + ENTITY_NOTE
)

PL_PRESENTATION_NOTE = (
    "PRESENTATION NOTE: the P&L's line-item structure changed across years - FY2021/FY2022 use a "
    "Net-interest-income/Net-operating-income structure with a distinct 'Other income - dividends received' "
    "line (only populated FY2021: £18,001k, reflecting a dividend from a subsidiary, alongside a matching "
    "£(18,001)k 'Impairment charge on investments in subsidiaries' line that year) and 'Profit/(loss) before "
    "tax'; FY2023-FY2025 drop both the dividend-income and investment-impairment lines (nil in every "
    "subsequent year) and FY2025 additionally renames 'Total operating (expense)/income' to 'Total operating "
    "income'. 'Realised/unrealised (loss)/gain on financial instruments at fair value through profit or loss' "
    "is the one line materially comparable across all 5 years. OCI detail (fair value of own credit risk "
    "changes) is nil or near-nil throughout - a genuine feature of this Bank's balance sheet, not a disclosure "
    "gap."
)

BS_PRESENTATION_NOTE = (
    "PRESENTATION NOTE: 'Loans to customers, designated at fair value through profit or loss' (one legacy "
    "mortgage - see the Bank's own Note 13/12) only appears FY2021-FY2023, fully run off by FY2024; "
    "'Fair value adjustment on hedged assets/liabilities' and 'Derivative financial instruments' as assets "
    "only appear from FY2023 onward (hedge accounting on interest rate swaps commenced 1 July 2023); "
    "'Corporation tax receivable/payable' and 'Amounts due to credit institutions'/'group companies' are "
    "populated only in the years the Bank actually had a balance on that line, per its own report - blank "
    "cells elsewhere reflect a genuine nil/not-applicable balance, not a missing figure."
)

# ---------------------------------------------------------------
# Sheet: Balance Sheet (Statement of Financial Position, Company/solo basis)
# ---------------------------------------------------------------
balance_sheet_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and cash equivalents", {"FY2025": 326895, "FY2024": 117053, "FY2023": 100292, "FY2022": 143706, "FY2021": 54544}),
    ("DATA", "Due from credit institutions", {"FY2025": 15053, "FY2024": 12254, "FY2023": 3900, "FY2022": 1970}),
    ("DATA", "Debt instruments", {"FY2025": 20301, "FY2024": 63810, "FY2023": 40495, "FY2022": 5000, "FY2021": 19999}),
    ("DATA", "Trade and other receivables", {"FY2025": 996, "FY2024": 738, "FY2023": 750, "FY2022": 1003, "FY2021": 817}),
    ("DATA", "Corporation tax receivable", {"FY2025": 1506, "FY2024": 276}),
    ("DATA", "Loans to customers, at amortised cost", {"FY2025": 1082504, "FY2024": 668338, "FY2023": 546990, "FY2022": 453815, "FY2021": 394523}),
    ("DATA", "Loans to customers, designated at fair value through profit or loss", {"FY2023": 4083, "FY2022": 4094, "FY2021": 4474}),
    ("DATA", "Fair value adjustment on hedged assets", {"FY2025": 4016, "FY2024": 6499}),
    ("DATA", "Derivative financial instruments", {"FY2025": 1742, "FY2024": 1637, "FY2023": 3119, "FY2022": 3123}),
    ("DATA", "Prepayments", {"FY2025": 2196, "FY2024": 2019, "FY2023": 1670, "FY2022": 1589, "FY2021": 1575}),
    ("DATA", "Deferred tax", {"FY2025": 5519, "FY2024": 5695, "FY2023": 5907, "FY2022": 6898, "FY2021": 9043}),
    ("DATA", "Amounts due from group companies", {"FY2025": 154496, "FY2024": 211327, "FY2023": 209527, "FY2022": 189221, "FY2021": 152451}),
    ("DATA", "Property and equipment", {"FY2025": 1247, "FY2024": 518, "FY2023": 1001, "FY2022": 1593, "FY2021": 1450}),
    ("DATA", "Investment in subsidiaries", {"FY2025": 16206, "FY2024": 16206, "FY2023": 16206, "FY2022": 16206, "FY2021": 16206}),
    ("DATA", "Intangible assets", {"FY2025": 5365, "FY2024": 5793, "FY2023": 5451, "FY2022": 4679, "FY2021": 4186}),
    ("TOTAL", "Total assets", {"FY2025": 1638042, "FY2024": 1112163, "FY2023": 939391, "FY2022": 832897, "FY2021": 659268}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Trade and other payables", {"FY2025": 13305, "FY2024": 5930, "FY2023": 5145, "FY2022": 8815, "FY2021": 8033}),
    ("DATA", "Corporation tax payable", {"FY2023": 599}),
    ("DATA", "Amounts due to credit institutions", {"FY2025": 1733, "FY2024": 1614, "FY2023": 2940, "FY2022": 4100}),
    ("DATA", "Amounts due to customers, at amortised cost", {"FY2025": 1495438, "FY2024": 957770, "FY2023": 827055, "FY2022": 724595, "FY2021": 557956}),
    ("DATA", "Amounts due to customers, at fair value through profit or loss", {"FY2025": 53, "FY2024": 128, "FY2023": 831, "FY2022": 1433, "FY2021": 1317}),
    ("DATA", "Fair value adjustment on hedged liabilities", {"FY2025": 515, "FY2024": 567}),
    ("DATA", "Derivative financial instruments (liability)", {"FY2025": 5026, "FY2024": 4691, "FY2023": 442}),
    ("DATA", "Subordinated liabilities", {"FY2025": 15759, "FY2024": 7632}),
    ("DATA", "Amounts due to group companies", {"FY2025": 3072, "FY2024": 31216}),
    ("TOTAL", "Total liabilities", {"FY2025": 1534901, "FY2024": 1009548, "FY2023": 837012, "FY2022": 738943, "FY2021": 567306}),
    ("SECTION", "Equity", {}),
    ("DATA", "Share capital", {"FY2025": 15217, "FY2024": 15217, "FY2023": 15217, "FY2022": 15217, "FY2021": 15217}),
    ("DATA", "Share premium", {"FY2025": 124195, "FY2024": 124195, "FY2023": 124195, "FY2022": 124195, "FY2021": 124195}),
    ("DATA", "Equity settled share based payment reserve", {"FY2025": 301, "FY2024": 301, "FY2023": 300, "FY2022": 207, "FY2021": 171}),
    ("DATA", "Own credit revaluation reserves", {"FY2025": 8, "FY2024": 8, "FY2023": 8, "FY2022": 8, "FY2021": 33}),
    ("DATA", "Retained earnings", {"FY2025": -36580, "FY2024": -37106, "FY2023": -37341, "FY2022": -45673, "FY2021": -47654}),
    ("TOTAL", "Total equity", {"FY2025": 103141, "FY2024": 102615, "FY2023": 102379, "FY2022": 93954, "FY2021": 91962}),
    ("TOTAL", "Total liabilities and equity", {"FY2025": 1638042, "FY2024": 1112163, "FY2023": 939391, "FY2022": 832897, "FY2021": 659268}),
]

bw.add_balance_sheet_sheet(
    title="Castle Trust Capital plc — Statement of Financial Position",
    subtitle="Company (solo) basis, £'000. Not the wider Castle Trust Holdings Limited Group. See source note at bottom.",
    rows=balance_sheet_rows,
    sources_text=STATEMENTS_SOURCES + "\n\n" + BS_PRESENTATION_NOTE,
    first_col_width=68,
    source_height=340,
)

# ---------------------------------------------------------------
# Sheet: Profit & Loss (Statement of Comprehensive Income, Company/solo basis)
# ---------------------------------------------------------------
income_statement_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest and similar income", {"FY2025": 88928, "FY2024": 66464, "FY2023": 49763, "FY2022": 34047, "FY2021": 35127}),
    ("DATA", "Interest and similar expense", {"FY2025": -55919, "FY2024": -40056, "FY2023": -20137, "FY2022": -8508, "FY2021": -10873}),
    ("TOTAL", "Net interest income", {"FY2025": 33009, "FY2024": 26408, "FY2023": 29626, "FY2022": 25539, "FY2021": 24254}),
    ("DATA", "Other income", {"FY2025": 3712, "FY2024": 4509, "FY2023": 5126}),
    ("DATA", "Fees and commission income", {"FY2025": 1486, "FY2024": 1351, "FY2023": 1088, "FY2022": 812, "FY2021": 643}),
    ("DATA", "Fees and commission expense", {"FY2025": -64, "FY2024": -18, "FY2023": -20, "FY2021": -48}),
    ("DATA", "Realised/unrealised (loss)/gain on financial instruments at fair value through profit or loss", {"FY2025": -1749, "FY2024": -2776, "FY2023": 988, "FY2022": 2680, "FY2021": -1328}),
    ("TOTAL", "Total operating income", {"FY2025": 36394, "FY2024": 29474, "FY2023": 36808, "FY2022": 29031, "FY2021": 23521}),
    ("SECTION", "Expenses", {}),
    ("DATA", "Administrative expenses", {"FY2025": -23526, "FY2024": -21751, "FY2023": -21144, "FY2022": -21001, "FY2021": -22281}),
    ("DATA", "Impairment losses", {"FY2025": -8911, "FY2024": -4715, "FY2023": -3298, "FY2022": -1530, "FY2021": -1892}),
    ("DATA", "Impairment charge on investments in subsidiaries", {"FY2021": -18001}),
    ("DATA", "Depreciation and amortisation", {"FY2025": -2754, "FY2024": -2464, "FY2023": -2219, "FY2022": -2040, "FY2021": -1613}),
    ("TOTAL", "Total operating expenses", {"FY2025": -35191, "FY2024": -28930, "FY2023": -26661, "FY2022": -24571, "FY2021": -43787}),
    ("DATA", "Other income - dividends received", {"FY2021": 18001}),
    ("TOTAL", "Profit/(loss) before tax", {"FY2025": 1203, "FY2024": 544, "FY2023": 10147, "FY2022": 4460, "FY2021": -2265}),
    ("DATA", "Corporation tax charge/credit", {"FY2025": -677, "FY2024": -309, "FY2023": -1815, "FY2022": -2479, "FY2021": 9018}),
    ("TOTAL", "Total profit/(loss)", {"FY2025": 526, "FY2024": 235, "FY2023": 8332, "FY2022": 1981, "FY2021": 6753}),
    ("SECTION", "Other comprehensive income", {}),
    ("DATA", "Fair value of own credit risk changes of financial liabilities at FVPL", {"FY2022": -25, "FY2021": -4}),
    ("TOTAL", "Total other comprehensive income/(expense) for the year", {"FY2025": 0, "FY2024": 0, "FY2023": 0, "FY2022": -25, "FY2021": -4}),
    ("TOTAL", "Total comprehensive income/(loss) for the year", {"FY2025": 526, "FY2024": 235, "FY2023": 8332, "FY2022": 1956, "FY2021": 6749}),
]

bw.add_income_statement_sheet(
    title="Castle Trust Capital plc — Statement of Comprehensive Income",
    subtitle="Company (solo) basis, £'000. Not the wider Castle Trust Holdings Limited Group. See source note at bottom.",
    rows=income_statement_rows,
    sources_text=STATEMENTS_SOURCES + "\n\n" + PL_PRESENTATION_NOTE,
    first_col_width=88,
    source_height=340,
)

# ---------------------------------------------------------------
# Sheet: Statement of Changes in Equity (chronological, oldest to newest)
# ---------------------------------------------------------------
EQUITY_HEADERS = ["Share capital", "Share premium", "Equity settled share based payment reserve", "Own credit revaluation reserves", "Retained earnings", "Total"]
equity_changes_rows = [
    ("TOTAL", "At 1 October 2020", (15217, 124195, 155, 37, -54407, 85197)),
    ("DATA", "Total profit for the year (FY2021)", (None, None, None, None, 6753, 6753)),
    ("DATA", "Fair value of own credit risk changes of financial liabilities at FVPL (FY2021)", (None, None, None, -4, None, -4)),
    ("DATA", "Equity settled share based payment reserve (FY2021)", (None, None, 16, None, None, 16)),
    ("TOTAL", "At 30 September 2021", (15217, 124195, 171, 33, -47654, 91962)),
    ("DATA", "Total profit for the year (FY2022)", (None, None, None, None, 1981, 1981)),
    ("DATA", "Fair value of own credit risk changes of financial liabilities at FVPL (FY2022)", (None, None, None, -25, None, -25)),
    ("DATA", "Equity settled share based payment reserve (FY2022)", (None, None, 36, None, None, 36)),
    ("TOTAL", "At 30 September 2022", (15217, 124195, 207, 8, -45673, 93954)),
    ("DATA", "Total comprehensive income for the year (FY2023)", (None, None, None, None, 8332, 8332)),
    ("DATA", "Equity settled share based payment reserve (FY2023)", (None, None, 93, None, None, 93)),
    ("TOTAL", "At 30 September 2023", (15217, 124195, 300, 8, -37341, 102379)),
    ("DATA", "Total comprehensive income for the year (FY2024)", (None, None, None, None, 235, 235)),
    ("DATA", "Equity settled share based payment reserve (FY2024)", (None, None, 1, None, None, 1)),
    ("TOTAL", "At 30 September 2024", (15217, 124195, 301, 8, -37106, 102615)),
    ("DATA", "Total comprehensive income for the year (FY2025)", (None, None, None, None, 526, 526)),
    ("TOTAL", "At 30 September 2025", (15217, 124195, 301, 8, -36580, 103141)),
]

bw.add_equity_changes_sheet(
    title="Castle Trust Capital plc — Statement of Changes in Equity",
    subtitle="Company (solo) basis, £'000. Not the wider Castle Trust Holdings Limited Group. Chronological, "
             "oldest to newest. No plug row needed - GBP-native, chain ties exactly year to year.",
    headers=EQUITY_HEADERS,
    rows=equity_changes_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=52,
    source_height=280,
)

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement (Company/solo basis)
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Cash flows from operating activities", {}),
    ("DATA", "Profit/(loss) before tax", {"FY2025": 1203, "FY2024": 544, "FY2023": 10147, "FY2022": 4460, "FY2021": -2265}),
    ("DATA", "Depreciation and amortisation", {"FY2025": 2754, "FY2024": 2464, "FY2023": 2219, "FY2022": 2040, "FY2021": 1617}),
    ("DATA", "Loss on disposal of property, plant and equipment", {"FY2025": 63}),
    ("DATA", "Write off of intangible assets", {"FY2024": 80}),
    ("DATA", "Loss on disposal of intangibles and property, plant and equipment", {"FY2022": 78, "FY2021": 78}),
    ("DATA", "Dividends received", {"FY2022": -18001, "FY2021": -18001}),
    ("DATA", "Impairment charge/(reversal) on investments in subsidiaries", {"FY2022": 18001, "FY2021": 18001}),
    ("DATA", "Share based payment expense", {"FY2025": 0, "FY2024": 1, "FY2023": 93, "FY2022": 36, "FY2021": 16}),
    ("DATA", "Net interest income", {"FY2025": -33009, "FY2024": -26408, "FY2023": -29626, "FY2022": -25436}),
    ("DATA", "Interest income - MILA", {"FY2021": -4687}),
    ("DATA", "Interest on lease liabilities", {"FY2021": 52}),
    ("DATA", "Impairment losses", {"FY2025": 8911, "FY2024": 4715, "FY2023": 3298, "FY2022": 1530, "FY2021": 1892}),
    ("DATA", "Other income on R&D tax credits", {"FY2025": -255, "FY2024": -417}),
    ("DATA", "R&D tax credits released against tax charge", {"FY2023": -120, "FY2022": -220}),
    ("DATA", "Tax charge transferred from subsidiary", {"FY2024": 0, "FY2023": -225}),
    ("DATA", "Fair value losses/(gains) on loans to customers at fair value", {"FY2025": 0, "FY2024": 319, "FY2023": 278, "FY2022": 427, "FY2021": 1032}),
    ("DATA", "Fair value (gains)/losses on amounts due to customers at fair value", {"FY2025": -4, "FY2024": 51, "FY2023": -41, "FY2022": 112, "FY2021": 158}),
    ("DATA", "Net unrealised (gain)/loss on derivative(s) assets", {"FY2025": 1753, "FY2024": 2406, "FY2023": -1225, "FY2022": -3219}),
    ("TOTAL", "Cash flows from operating activities before changes in operating assets and liabilities", {"FY2025": -18584, "FY2024": -16245, "FY2023": -15202}),
    ("SECTION", "Changes in operating assets and liabilities", {}),
    ("DATA", "(Increase)/decrease in trade and other receivables (excluding corporation tax receivable)", {"FY2025": -258, "FY2024": 12, "FY2023": 253, "FY2022": -186, "FY2021": 201}),
    ("DATA", "Increase/(decrease) in loans to customers at amortised cost", {"FY2025": -390164, "FY2024": -107177, "FY2023": -79742, "FY2022": -47624, "FY2021": 48663}),
    ("DATA", "Increase in amounts due to customers at amortised cost (and related hedged asset)", {"FY2025": 546293, "FY2024": 139599, "FY2023": 108862, "FY2022": 168780}),
    ("DATA", "Increase in amounts due to customers at amortised cost / Borrower Loan Agreement", {"FY2021": -93538}),
    ("DATA", "Increase/(decrease) in prepayments (and related hedge liability)", {"FY2025": -177, "FY2024": -350, "FY2023": -81, "FY2022": -14, "FY2021": 466}),
    ("DATA", "Increase/(decrease) in trade and other payables (excl. corporation tax payable and lease liability)", {"FY2025": 6547, "FY2024": 1281, "FY2023": -3074, "FY2022": 772, "FY2021": -16013}),
    ("DATA", "Decrease/(increase) in loans to customers at fair value", {"FY2025": 0, "FY2024": 3764, "FY2023": -267, "FY2022": -47, "FY2021": 0}),
    ("DATA", "Decrease in amounts due to customers at fair value", {"FY2025": -71, "FY2024": -754, "FY2023": -561, "FY2022": -21}),
    ("DATA", "Increase/(decrease) in derivative financial instruments/assets", {"FY2025": -1523, "FY2024": -2605, "FY2023": 1671, "FY2022": 96}),
    ("DATA", "Increase in amounts due to customers at fair value / group companies (inter-company swap)", {"FY2021": -289}),
    ("DATA", "Increase in amounts due from credit institutions", {"FY2025": -2799, "FY2024": -8354, "FY2023": -1930}),
    ("DATA", "Increase/(decrease) in amounts due to credit institutions", {"FY2025": 119, "FY2024": -1326, "FY2023": -1160, "FY2022": 4100}),
    ("DATA", "Tax refunds", {"FY2025": 0, "FY2024": 118}),
    ("DATA", "Tax paid", {"FY2025": -1188, "FY2022": -26}),
    ("DATA", "Tax refunded/(paid)", {"FY2023": -13}),
    ("DATA", "Interest received", {"FY2025": 60879, "FY2024": 46245, "FY2023": 30986, "FY2022": 20746}),
    ("DATA", "Interest paid (excluding interest on lease liabilities and MILA loan)", {"FY2025": -64410}),
    ("DATA", "Interest paid on lease liabilities", {"FY2025": -59}),
    ("DATA", "Interest paid (including interest on lease liabilities and MILA loan)", {"FY2024": -48308, "FY2023": -26760, "FY2022": -10649}),
    ("TOTAL", "Net cash generated from/(used in) operating activities", {"FY2025": 134605, "FY2024": 5222, "FY2023": 12982, "FY2022": 113687, "FY2021": -62617}),
    ("SECTION", "Cash flows from investing activities", {}),
    ("DATA", "Purchase of intangible assets", {"FY2025": -1781, "FY2024": -2237, "FY2023": -2352, "FY2022": -1862, "FY2021": -1027}),
    ("DATA", "Purchase of debt instruments", {"FY2025": -19838, "FY2024": -53000}),
    ("DATA", "Proceeds from sale of debt instruments", {"FY2025": 63347, "FY2024": 29685, "FY2022": 14999}),
    ("DATA", "(Purchase)/sale of debt instruments (net, as reported)", {"FY2023": -35495}),
    ("DATA", "Sale/(purchase) of debt instruments (net, as reported)", {"FY2021": 96919}),
    ("DATA", "Purchase of property, plant and equipment", {"FY2025": -97, "FY2024": -123, "FY2023": -11, "FY2022": -493, "FY2021": -73}),
    ("DATA", "Disposals of property, plant and equipment", {"FY2025": 0, "FY2024": 22}),
    ("DATA", "Purchase of leased asset on transfer", {"FY2021": -17}),
    ("DATA", "Proceeds from maturities of fixed deposits", {"FY2021": 0}),
    ("TOTAL", "Net cash generated from/(used in) investing activities", {"FY2025": 41631, "FY2024": -25653, "FY2023": -37858, "FY2022": 12644, "FY2021": 95802}),
    ("SECTION", "Cash flows from financing activities", {}),
    ("DATA", "Principal receipts of intercompany loans", {"FY2025": 127105, "FY2024": 35952}),
    ("DATA", "Principal repayment of intercompany loans", {"FY2025": -101088, "FY2024": -5199, "FY2023": -18021}),
    ("DATA", "Principal repayment of MILA loan", {"FY2022": -36770}),
    ("DATA", "Proceeds from issue of share capital", {"FY2021": 0}),
    ("DATA", "Interest received on MILA", {"FY2021": 4687}),
    ("DATA", "Principal (repayment)/receipt of MILA", {"FY2021": -14813}),
    ("DATA", "Lease payments of principal", {"FY2025": -411, "FY2024": -561, "FY2023": -517, "FY2022": -399, "FY2021": -293}),
    ("DATA", "Lease interest paid", {"FY2021": -52}),
    ("DATA", "Receipts from issuance of subordinated liability", {"FY2025": 8000, "FY2024": 7000}),
    ("TOTAL", "Net cash generated from/(used in) financing activities", {"FY2025": 33606, "FY2024": 37192, "FY2023": -18538, "FY2022": -37169, "FY2021": -10471}),
    ("TOTAL", "Net increase/(decrease) in cash and cash equivalents", {"FY2025": 209842, "FY2024": 16761, "FY2023": -43414, "FY2022": 89162, "FY2021": 22714}),
    ("DATA", "Cash and cash equivalents at the beginning of the year", {"FY2025": 117053, "FY2024": 100292, "FY2023": 143706, "FY2022": 54544, "FY2021": 31830}),
    ("TOTAL", "Cash and cash equivalents at the end of the year", {"FY2025": 326895, "FY2024": 117053, "FY2023": 100292, "FY2022": 143706, "FY2021": 54544}),
]

bw.add_cash_flow_sheet(
    title="Castle Trust Capital plc — Statement of Cash Flows",
    subtitle="Company (solo) basis, £'000. Not the wider Castle Trust Holdings Limited Group. See source note at bottom.",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=88,
    source_height=280,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Sheet: Asset Quality / Credit Risk Disclosures
# ---------------------------------------------------------------
STAGE1_GROSS = {"FY2025": 968725, "FY2024": 532712, "FY2023": 440613, "FY2022": 335067, "FY2021": 224629}
STAGE1_ECL = {"FY2025": -969, "FY2024": -765, "FY2023": -929, "FY2022": -291, "FY2021": -684}
STAGE2_GROSS = {"FY2025": 44952, "FY2024": 57136, "FY2023": 48080, "FY2022": 65347, "FY2021": 116924}
STAGE2_ECL = {"FY2025": -498, "FY2024": -842, "FY2023": -986, "FY2022": -1105, "FY2021": -1034}
STAGE3_GROSS = {"FY2025": 87888, "FY2024": 90833, "FY2023": 70394, "FY2022": 63269, "FY2021": 61643}
STAGE3_ECL = {"FY2025": -17594, "FY2024": -10736, "FY2023": -10182, "FY2022": -8472, "FY2021": -6955}
TOTAL_GROSS_LOANS = {"FY2025": 1101565, "FY2024": 680681, "FY2023": 559087, "FY2022": 463683, "FY2021": 403196}
TOTAL_ECL = {"FY2025": -19061, "FY2024": -12343, "FY2023": -12097, "FY2022": -9868, "FY2021": -8673}

def _pct(numer, denom):
    return {y: f"{abs(numer[y]) / denom[y] * 100:.2f}%" for y in YEARS}

STAGE3_NPL_RATIO = _pct(STAGE3_GROSS, TOTAL_GROSS_LOANS)
STAGE3_COVERAGE = {y: f"{abs(STAGE3_ECL[y]) / STAGE3_GROSS[y] * 100:.2f}%" for y in YEARS}
TOTAL_ECL_COVERAGE = _pct(TOTAL_ECL, TOTAL_GROSS_LOANS)

asset_quality_rows = [
    ("SECTION", "Loans and advances to customers at amortised cost, by IFRS 9 stage (gross carrying amount)", {}),
    ("DATA", "Stage 1", STAGE1_GROSS),
    ("DATA", "Stage 2", STAGE2_GROSS),
    ("DATA", "Stage 3", STAGE3_GROSS),
    ("TOTAL", "Total gross carrying amount", TOTAL_GROSS_LOANS),
    ("SECTION", "Expected credit loss (ECL) allowance, by IFRS 9 stage", {}),
    ("DATA", "Stage 1 allowance", STAGE1_ECL),
    ("DATA", "Stage 2 allowance", STAGE2_ECL),
    ("DATA", "Stage 3 allowance", STAGE3_ECL),
    ("TOTAL", "Total ECL allowance", TOTAL_ECL),
    ("SECTION", "Derived ratios", {}),
    ("DATA", "Stage 3 / NPL ratio (Stage 3 gross / total gross)", STAGE3_NPL_RATIO),
    ("DATA", "Stage 3 coverage (Stage 3 ECL / Stage 3 gross)", STAGE3_COVERAGE),
    ("DATA", "Total ECL coverage (total ECL / total gross)", TOTAL_ECL_COVERAGE),
]

bw.add_asset_quality_sheet(
    title="Castle Trust Capital plc — Asset Quality / Credit Risk Disclosures",
    subtitle="Company (solo) basis, £'000. Loans to customers at amortised cost only (excludes the small "
             "fair-value-designated legacy mortgage book, run off by FY2024). All 5 years genuinely disclosed - "
             "no not-disclosed fallback needed.",
    rows=asset_quality_rows,
    sources_text=(
        "Sources - Castle Trust Capital plc's own 'Reconciliation of gross loan and ECL movements in the year' "
        "note (Property loans table, the entity's sole loan product), each year's own originally-published "
        "figures:\n"
        f"FY2025: Annual financial statements, y/e 30 Sept 2025, p.85 - {CH_FY2025_URL}\n"
        f"FY2024: Annual financial statements, y/e 30 Sept 2024, p.85 - {CH_FY2024_URL}\n"
        f"FY2023: Annual financial statements, y/e 30 Sept 2023, p.78 - {CH_FY2023_URL}\n"
        f"FY2022: Annual financial statements, y/e 30 Sept 2022, p.70 - {CH_FY2022_URL}\n"
        f"FY2021: Annual financial statements, y/e 30 Sept 2021, p.62 - {CH_FY2021_URL}\n\n"
        "All 5 years' Total gross carrying amount ties exactly to the Balance Sheet's 'Loans to customers, at "
        "amortised cost' net figure once the Total ECL allowance is deducted (e.g. FY2025: £1,101,565k - "
        "£19,061k = £1,082,504k). Derived ratios (Stage 3/NPL ratio, Stage 3 coverage, total ECL coverage) are "
        "calculated here, not disclosed as standalone percentages by the Bank itself."
    ),
    first_col_width=64,
    source_height=280,
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets (all "Key Metrics for the Bank" - Castle Trust Capital plc solo)
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, unit, rows_data, sources_text, note=note, first_col_width=50, source_height=170)


CET1_TIER1 = {"FY2025": 84719, "FY2024": 83107, "FY2023": 83177, "FY2022": 75267, "FY2021": 71677}
TOTAL_CAPITAL = {"FY2025": 99719, "FY2024": 90107, "FY2023": 83177, "FY2022": 75267, "FY2021": 71677}
RWA = {"FY2025": 634489, "FY2024": 499532, "FY2023": 413907, "FY2022": 357870, "FY2021": 359249}
CET1_RATIO = {"FY2025": "13.35%", "FY2024": "16.64%", "FY2023": "20.10%", "FY2022": "21.03%", "FY2021": "20.0%"}
TOTAL_CAP_RATIO = {"FY2025": "15.72%", "FY2024": "18.04%", "FY2023": "20.10%", "FY2022": "21.03%", "FY2021": "20.0%"}
LEV_EXPOSURE = {"FY2025": 1173013, "FY2024": 860147, "FY2023": 930371, "FY2022": 821174, "FY2021": 647358}
LEV_RATIO = {"FY2025": "7.22%", "FY2024": "9.66%", "FY2023": "8.94%", "FY2022": "9.17%", "FY2021": "11.1%"}
LCR_RATIO = {"FY2025": "189.07%", "FY2024": "296.84%", "FY2023": "324.90%", "FY2022": "401.68%", "FY2021": "575.71%"}
NSFR_RATIO = {"FY2025": "178.27%", "FY2024": "156.44%", "FY2023": "171.97%", "FY2022": "169.82%"}

# FY2021 is the one year for which two Bank-basis sources exist and disagree, found 2026-09-15 when all
# six editions were read side by side. Row 1 of each affected sheet is the FY2021 Pillar 3's own
# Appendix 4 (the same-year original, this workbook's convention); these are the FY2022 edition's
# restated FY2021 comparative, carried on their own labelled row rather than overwriting it.
FY2021_ALT = {"FY2021": 71644}
FY2021_ALT_RATIO = {"FY2021": "19.94%"}
FY2021_ALT_LEV = {"FY2021": "11.07%"}
FY2021_ALT_NOTE = (
    "FY2021 CROSS-EDITION DIVERGENCE (recorded 2026-09-15). Two Bank-basis sources cover FY2021 and they do "
    "not agree, so both are shown and neither overwrites the other:\n"
    "  (a) the FY2021 Pillar 3 Disclosures' own 'Appendix 4. Bank Disclosures' (p.40-43), which states CET1 = "
    "Tier 1 = Total capital of GBP71,677k and a CET1/Tier 1/Total capital ratio of 20.0%, and shows its own "
    "build-up (share capital 15,217 + share premium 124,195 - retained earnings 47,654 + other reserves 205 - "
    "prudent valuation 6 - intangibles 4,186 - DTA 8,743 - significant investments 8,217 + IFRS 9 transitional "
    "867 = 71,677); and\n"
    "  (b) the FY2022 Pillar 3 Disclosures' 'Key Metrics for the Bank' FY2021 comparative column, which "
    "restates the same three capital figures to GBP71,644k and the ratio to 19.94%.\n"
    "The gap is GBP33k of capital, 6bp of ratio - immaterial in size but a real restatement, and the later "
    "edition gives no reconciliation for it. Everything else about FY2021 is IDENTICAL between the two "
    "editions, which is why only these rows are duplicated: total RWA GBP359,249k and leverage exposure "
    "measure GBP647,358k both appear unchanged in both. The leverage ratio differs only by rounding "
    "(Appendix 4 prints one decimal, 11.1%; the KM1 comparative prints two, 11.07%) - 71,677 / 647,358 and "
    "71,644 / 647,358 both round to 11.07%, so that pair is a precision difference, not a restatement."
)

metric(
    "CET1 Capital", "£'000",
    [("Common Equity Tier 1 (CET1) capital", CET1_TIER1),
     ("FY2021 as restated in the FY2022 Pillar 3 'Key Metrics for the Bank' comparative", FY2021_ALT)],
    p3_sources(),
    note="No AT1 instruments in issue in any year to date, so CET1 = Tier 1 capital throughout.\n\n"
         + FY2021_ALT_NOTE,
)

metric(
    "CET1 Ratio", "% of RWA",
    [("Common Equity Tier 1 (CET1) ratio", CET1_RATIO),
     ("FY2021 as restated in the FY2022 Pillar 3 'Key Metrics for the Bank' comparative", FY2021_ALT_RATIO)],
    p3_sources(),
    note="FY2021 sourced from the pre-KM1-template 'Appendix 4. Bank Disclosures' section of the FY2021 "
         "Pillar 3 document (own funds/RWA breakdown, not a KM1 template - this format was only introduced "
         "from 1 Jan 2022).\n\n" + FY2021_ALT_NOTE,
)

metric(
    "Tier 1 Capital", "£'000",
    [("Tier 1 capital", CET1_TIER1),
     ("FY2021 as restated in the FY2022 Pillar 3 'Key Metrics for the Bank' comparative", FY2021_ALT)],
    p3_sources(),
    note="= CET1 capital (no AT1 instruments in issue in any year to date).\n\n" + FY2021_ALT_NOTE,
)

metric(
    "Tier 1 Ratio", "% of RWA",
    [("Tier 1 ratio", CET1_RATIO),
     ("FY2021 as restated in the FY2022 Pillar 3 'Key Metrics for the Bank' comparative", FY2021_ALT_RATIO)],
    p3_sources(),
    note=FY2021_ALT_NOTE,
)

metric(
    "Total Capital", "£'000",
    [("Total capital", TOTAL_CAPITAL),
     ("FY2021 as restated in the FY2022 Pillar 3 'Key Metrics for the Bank' comparative", FY2021_ALT)],
    p3_sources(),
    note="Total capital exceeds Tier 1 capital from FY2024 onward (Tier 2 instruments: £7.0m FY2024, "
         "£15.0m FY2025) - no Tier 2 in issue FY2021-FY2023, when Total Capital = CET1 = Tier 1.\n\n"
         + FY2021_ALT_NOTE,
)

metric(
    "Total Capital Ratio", "% of RWA",
    [("Total capital ratio", TOTAL_CAP_RATIO),
     ("FY2021 as restated in the FY2022 Pillar 3 'Key Metrics for the Bank' comparative", FY2021_ALT_RATIO)],
    p3_sources(),
    note=FY2021_ALT_NOTE,
)

metric(
    "Total RWAs", "£'000",
    [("Total risk-weighted exposure amount", RWA)],
    p3_sources(),
)

rwa_breakdown_rows = [
    ("SECTION", "RWA by risk category (UK OV1, Bank basis)", {}),
    ("DATA", "Credit risk (excluding CCR)", {"FY2025": 566610, "FY2024": 439883}),
    ("DATA", "Counterparty credit risk (CCR)", {"FY2025": 6560, "FY2024": 3412}),
    ("DATA", "  of which: credit valuation adjustment (CVA)", {"FY2025": 2755, "FY2024": 1465}),
    ("DATA", "Operational risk", {"FY2025": 61318, "FY2024": 56237}),
    ("TOTAL", "Total", {"FY2025": 634489, "FY2024": 499532}),
    ("SECTION", "Breakdown of Risk Weighted Assets (pre-KM1/OV1 format, Bank/solo basis, as disclosed)", {}),
    ("DATA", "Credit risk", {"FY2021": 311424}),
    ("DATA", "Market risk", {"FY2021": 0}),
    ("DATA", "Operational risk", {"FY2021": 47825}),
    ("TOTAL", "Total", {"FY2021": 359249}),
    ("SECTION", "FY2022-FY2023", {}),
    ("TOTAL", "Total", {"FY2023": "Not publicly disclosed", "FY2022": "Not publicly disclosed"}),
]

bw.add_rwa_breakdown_sheet(
    title="Castle Trust Capital plc — RWA Breakdown",
    subtitle="£'000, Bank basis. UK OV1-format breakdown only from FY2024-FY2025; FY2021 uses an earlier, "
             "coarser-grained 'Breakdown of Risk Weighted Assets' table from the same Bank/solo entity (no "
             "OV1 template existed pre-2022) - see note below for FY2022-FY2023, where nothing usable was found.",
    rows=rwa_breakdown_rows,
    sources_text=(
        f"Sources - Castle Trust Bank Pillar 3 Disclosures, 'Overview of RWEAs for Bank' table (Bank, not "
        f"Group, basis):\nFY2025: Pillar 3 Disclosures FY ended 30 Sept 2025, p.6 - {P3_2025_URL} (also carries "
        f"FY2024 as its own comparative column, used here since FY2024's own Pillar 3 Disclosures document "
        f"predates the OV1 template and doesn't carry this breakdown itself - flagged, not a same-year "
        f"original disclosure for FY2024)\n\n"
        f"FY2021: Pillar 3 Disclosures FY ended 30 Sept 2021, Appendix 4 'Bank Disclosures' (Castle Trust "
        f"Capital plc standalone solo legal entity), 'Capital Adequacy - Breakdown of Risk Weighted Assets' "
        f"table, p.40 - {P3_2021_URL}. Directly disclosed RWA by risk type (Credit Risk £311,424k, Market Risk "
        f"£0k, Operational Risk £47,825k, Total £359,249k) - reconciles exactly to the Total RWAs sheet's own "
        f"FY2021 figure (£359,249k, same document's Appendix 4 Capital Adequacy table). Not an OV1-format "
        f"disclosure (no CCR/CVA sub-lines existed in this pre-2022 table format) and on a different granularity "
        f"from the FY2024-FY2025 OV1 section above - kept in a separate section rather than blended in.\n\n"
        "FY2023/FY2022: not publicly disclosed. Confirmed by reading both years' Pillar 3 Disclosures documents "
        "in full - they contain only the 7-page 'Key Metrics' (KM1) template, with no RWA-by-category "
        "breakdown. Also checked the FY2023 Annual Report (Companies House filing, same document already cited "
        "for the cash-flow statement) in full: its Notes to the Financial Statements run straight from Note "
        "23.1 (credit risk) to 23.2 (liquidity risk) to Note 25 (share capital) with no capital-risk/RWA note "
        "in between - no risk-type RWA breakdown exists in that document either.\n\n"
        "RE-VERIFIED (2026-09-12, independent re-check): re-downloaded both FY2022 and FY2023 Pillar 3 "
        "Disclosures directly from the Bank's own site and re-read them page by page (both are exactly 8 "
        "pages) - each contains only the Group and Bank 'Key Metrics' (KM1) tables (Total RWA £530,968k/"
        "£357,870k Bank basis FY2022; £592,678k Group/£413,907k Bank basis FY2023), with no OV1 or any other "
        "category-level RWA table present in either document. Confirms the gap is genuine, not a prior "
        "session's access failure.\n\n"
        "THIRD INDEPENDENT CHECK (2026-09-15, RWA-backfill sweep - this bank was flagged because its FY2022/"
        "FY2023 gap sits BETWEEN disclosed years, which usually indicates a sourcing miss rather than a real "
        "absence; here it does not). Both documents re-downloaded and machine-read again: each has a real text "
        "layer (no OCR needed) and its own table of contents settles the question without relying on a page-by-"
        "page search - both list exactly Scope / Background / Business Overview / Basis for this Requirement / "
        "Frequency of Disclosure / Verification / Location of Document / Key Metrics for the Group / Key Metrics "
        "for the Bank / Additional Information. There is no OV1 section to have been missed. The Bank's "
        "disclosure format simply changed twice: a pre-2022 'Breakdown of Risk Weighted Assets' table through "
        "FY2021, a minimal KM1-only document for FY2022-FY2023, then the full UK OV1 template from FY2024. "
        "Treat this gap as closed - it does not need chasing again."
    ),
    first_col_width=58,
    source_height=310,
)

metric(
    "Leverage Ratio", "£'000 / %",
    [
        ("Total exposure measure excluding claims on central banks (£'000)", LEV_EXPOSURE),
        ("Leverage ratio excluding claims on central banks (%)", LEV_RATIO),
        ("FY2021 leverage ratio as printed in the FY2022 Pillar 3 'Key Metrics for the Bank' comparative (%)",
         FY2021_ALT_LEV),
    ],
    p3_sources(),
    note="FY2021 figure/basis from the FY2021 Pillar 3 document's own 'Leverage Ratio' appendix table "
         "(pre-KM1 template, same underlying 'excluding claims on central banks' concept), which shows its "
         "own reconciliation: total assets per the published financial statements £659,269k, plus £2,515k of "
         "off-balance-sheet items converted to credit equivalent amounts, less £14,426k of other adjustments, "
         "giving the £647,358k exposure measure used above.\n\n" + FY2021_ALT_NOTE,
)

metric(
    "LCR", "£'000 / %",
    [
        ("Total high-quality liquid assets (HQLA), weighted value - average (£'000)",
         {"FY2025": 264609, "FY2024": 107626, "FY2023": 91141, "FY2022": 89542}),
        ("Total net cash outflows, adjusted value (£'000)",
         {"FY2025": 139955, "FY2024": 36257, "FY2023": 28052, "FY2022": 22292}),
        ("Liquidity Coverage Ratio (%)", LCR_RATIO),
    ],
    p3_sources(),
    note="FY2021's own Pillar 3 document (pre-KM1 template) discloses no LCR figure for the Bank at all - "
         "the 575.71% shown here is FY2021's comparative column as it appears in the FY2022 Pillar 3 "
         "document's KM1 table (HQLA £77,922k, net cash outflows £13,535k), the earliest source in which "
         "it's disclosed. Flagged, not a same-year original disclosure.",
)

metric(
    "NSFR", "£'000 / %",
    [
        ("Total available stable funding (£'000)",
         {"FY2025": 1473649, "FY2024": 943517, "FY2023": 810485, "FY2022": 715551}),
        ("Total required stable funding (£'000)",
         {"FY2025": 826660, "FY2024": 603108, "FY2023": 471300, "FY2022": 421346}),
        ("Net Stable Funding Ratio (%)", NSFR_RATIO),
    ],
    p3_sources(),
    note="Not disclosed for FY2021 in any source reviewed (marked 'N/A' even in the FY2022 Pillar 3 "
         "document's FY2021 comparative column) - the UK NSFR regime only took effect from 1 Jan 2022, "
         "partway through this entity's FY2021 (y/e 30 Sept 2021).",
)

bw.add_not_disclosed_metric_sheets(
    ["MREL Ratio"], p3_sources(page="n/a"), per_note={"MREL Ratio": NOT_DISCLOSED_NOTE},
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {"FY2025": 1638042, "FY2024": 1112163, "FY2023": 939391, "FY2022": 832897, "FY2021": 659268}),
        ("Loans to customers, at amortised cost", {"FY2025": 1082504, "FY2024": 668338, "FY2023": 546990, "FY2022": 453815, "FY2021": 394523}),
        ("Amounts due to customers, at amortised cost", {"FY2025": 1495438, "FY2024": 957770, "FY2023": 827055, "FY2022": 724595, "FY2021": 557956}),
        ("Total equity", {"FY2025": 103141, "FY2024": 102615, "FY2023": 102379, "FY2022": 93954, "FY2021": 91962}),
    ],
    balance_sheet_unit="£'000",
    income_statement_totals=[
        ("Net interest income", {"FY2025": 33009, "FY2024": 26408, "FY2023": 29626, "FY2022": 25539, "FY2021": 24254}),
        ("Administrative expenses", {"FY2025": -23526, "FY2024": -21751, "FY2023": -21144, "FY2022": -21001, "FY2021": -22281}),
        ("Total profit/(loss)", {"FY2025": 526, "FY2024": 235, "FY2023": 8332, "FY2022": 1981, "FY2021": 6753}),
    ],
    income_statement_unit="£'000",
    equity_changes_totals=[
        ("Opening equity", {"FY2025": 102615, "FY2024": 102379, "FY2023": 93954, "FY2022": 91962, "FY2021": 85197}),
        ("Total comprehensive income for the year", {"FY2025": 526, "FY2024": 235, "FY2023": 8332, "FY2022": 1956, "FY2021": 6749}),
        ("Other movements, net", {"FY2025": 0, "FY2024": 1, "FY2023": 93, "FY2022": 36, "FY2021": 16}),
        ("Closing equity", {"FY2025": 103141, "FY2024": 102615, "FY2023": 102379, "FY2022": 93954, "FY2021": 91962}),
    ],
    equity_changes_unit="£'000",
    cash_flow_totals=[
        ("Net cash generated from/(used in) operating activities", {"FY2025": 134605, "FY2024": 5222, "FY2023": 12982, "FY2022": 113687, "FY2021": -62617}),
        ("Net cash generated from/(used in) investing activities", {"FY2025": 41631, "FY2024": -25653, "FY2023": -37858, "FY2022": 12644, "FY2021": 95802}),
        ("Net cash generated from/(used in) financing activities", {"FY2025": 33606, "FY2024": 37192, "FY2023": -18538, "FY2022": -37169, "FY2021": -10471}),
        ("Cash and cash equivalents at end of year", {"FY2025": 326895, "FY2024": 117053, "FY2023": 100292, "FY2022": 143706, "FY2021": 54544}),
    ],
    cash_flow_unit="£'000",
    ratios=[
        ("CET1 Ratio", CET1_RATIO),
        ("Tier 1 Ratio", CET1_RATIO),
        ("Total Capital Ratio", TOTAL_CAP_RATIO),
        ("Leverage Ratio", LEV_RATIO),
        ("LCR", LCR_RATIO),
        ("NSFR", NSFR_RATIO),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own "
         "source citation for the underlying document/page. All figures are Castle Trust Capital plc's own "
         "solo ('Bank') basis, not the wider Castle Trust Holdings Limited Group.",
)

bw.save("/Users/armaan/code/katalysis/banks/CASTLE TRUST CAPITAL FINANCIALS.xlsx")
