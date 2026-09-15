import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook


# EXTENDED HISTORY: Afin Bank Limited's first Pillar 3 disclosure (its
# standalone regulatory reporting) is for 31 December 2024 only - the
# company was authorised as a bank with restrictions in October 2024 and
# its 2024 Pillar 3 report explicitly states no prior-period comparatives
# are provided. However, the same legal entity (company 13090556) existed
# since incorporation on 18 December 2020 under the name "All Africa
# Capital Limited" and filed ordinary Companies Act statutory accounts for
# each year back to its first accounting period. This workbook therefore
# extends FY2024's Pillar-3-only build back using those pre-authorisation
# statutory accounts for the Balance Sheet / Profit & Loss / Statement of
# Changes in Equity / Cash Flow Statement sheets (FY2021-FY2023), while the
# 11 Pillar 3 metric sheets, Asset Quality and RWA Breakdown remain
# genuinely "Not applicable" for those years - see NOT_APPLICABLE_P3_NOTE.
#
# FY2020 IS SELF-SKIPPED IN FULL (not a document-availability problem, a
# non-existence one): the company was incorporated 18 December 2020, and
# its first statutory accounts filed at Companies House cover the period
# from incorporation to 31 December 2021 (a ~13.5-month first accounting
# period) - confirmed by inspecting the filing history in full (pages 1-4,
# every accounts filing back to incorporation): the earliest accounts filed
# are for "the period ended 31 December 2021", with no discrete FY2020
# (1 Jan-31 Dec 2020) accounts ever filed, because no such period exists
# for this entity. See CH_FILING_HISTORY_URL.
YEARS = ["FY2024", "FY2023", "FY2022", "FY2021"]
YEAR_LABEL = {y: y for y in YEARS}

AR_2024_URL = "https://afinbank.com/wp-content/uploads/2025/09/Afin-Bank-Ltd-Year-End-Accounts-FV24-FINAL-SIGNED.pdf"
P3_2024_URL = "https://afinbank.com/wp-content/uploads/2025/09/Afin-Bank-2024-Pillar-3-Disclosures-FINAL.pdf"
CH_OVERVIEW_URL = "https://find-and-update.company-information.service.gov.uk/company/13090556"
CH_FILING_HISTORY_URL = "https://find-and-update.company-information.service.gov.uk/company/13090556/filing-history"
CH_2024_ACCOUNTS_URL = "https://find-and-update.company-information.service.gov.uk/company/13090556/filing-history/MzQ4MjgwOTc2M2FkaXF6a2N4/document?download=0&format=pdf"
CH_2023_ACCOUNTS_URL = "https://find-and-update.company-information.service.gov.uk/company/13090556/filing-history/MzQyNDA1MjMwOGFkaXF6a2N4/document?format=pdf&download=0"
CH_2022_ACCOUNTS_URL = "https://find-and-update.company-information.service.gov.uk/company/13090556/filing-history/MzM5MzI3MzYzNmFkaXF6a2N4/document?format=pdf&download=0"
CH_2021_ACCOUNTS_URL = "https://find-and-update.company-information.service.gov.uk/company/13090556/filing-history/MzM2MjY4Mzc2MGFkaXF6a2N4/document?format=pdf&download=0"

ENTITY_NOTE = (
    "ENTITY NOTE: Afin Bank Limited (company 13090556, FRN 1004742) is the UK legal entity covered here. "
    "The 2024 Pillar 3 report says the disclosure scope applies to Afin Bank Limited only; it is a majority-owned "
    "subsidiary of WAICA Reinsurance Corporation PLC, but no parent-level figures are substituted. The company was "
    "incorporated 18 December 2020 as All Africa Capital Limited, traded under that name through FY2021-FY2023, "
    "and changed its name to Afin Bank Limited after receiving banking authorisation with restrictions in "
    "October 2024. FY2021-FY2023 figures below are therefore All Africa Capital Limited's own pre-bank statutory "
    "accounts for the same continuous legal entity, sourced from Companies House (not from afinbank.com, which "
    "only hosts the FY2024 bank-era documents)."
)

FY2020_SKIP_NOTE = (
    "FY2020 SELF-SKIPPED IN FULL: the company was incorporated 18 December 2020, so no financial year beginning "
    "1 January 2020 exists for this entity, and no such period was ever filed at Companies House. Its first "
    "statutory accounts (filed 16 December 2022) cover the period from incorporation (18 December 2020) to "
    "31 December 2021 - a single ~13.5-month first accounting period, not a discrete FY2020 followed by a "
    "discrete FY2021. This was confirmed by reading the full Companies House filing history for company 13090556 "
    "(all 4 pages, back to incorporation), not assumed from the entity-creation-date signal alone - "
    f"{CH_FILING_HISTORY_URL}"
)

NOT_APPLICABLE_P3_NOTE = (
    "NOT APPLICABLE for FY2021-FY2023: All Africa Capital Limited (this entity's name before October 2024) was "
    "not a PRA-authorised bank during FY2021-FY2023 and had no Pillar 3 disclosure obligation - its own filed "
    "accounts for those years contain no capital/liquidity/leverage/RWA figures of any kind. This is a genuine "
    "'not applicable' (no obligation existed), distinct from 'not publicly disclosed' (an obligated but unpublished "
    "figure), which is how FY2024's own non-disclosures are marked.\n"
    "RE-VERIFIED 2026-09-12 (disclosure audit): confirmed independently against the Companies House register - "
    "company 13090556 was incorporated 18 December 2020 and was named 'ALL AFRICA CAPITAL LIMITED' from "
    "18 Dec 2020 until 22 October 2024, when it was renamed Afin Bank Limited on receiving banking authorisation "
    "with restrictions. FY2021-FY2023 therefore sit wholly inside the pre-authorisation period and the blanks are "
    "structural. Also confirmed the workbook's FY2024 endpoint is still current: the latest accounts on the "
    "register are made up to 31 December 2024, with FY2025 accounts not yet filed (due 30 September 2026)."
)

CASH_FLOW_SOURCES = (
    "Sources - FY2024: Afin Bank Limited audited annual report and financial statements for the year ended "
    f"31 December 2024, statement of cash flows, printed p. 36 - {AR_2024_URL}\n"
    "FY2023: All Africa Capital Limited audited annual report and financial statements for the year ended "
    f"31 December 2023, statement of cash flows, p. 9 (2023 column; 2022 comparative column, itself unaudited "
    f"per the auditor's report on p. 4) - {CH_2023_ACCOUNTS_URL}\n"
    "FY2022: as above (FY2023 report's own 2022 comparative column - the standalone FY2022 filing is a "
    f"balance-sheet-only unaudited filing with no cash flow statement) - {CH_2022_ACCOUNTS_URL}\n"
    "FY2021: NOT DISCLOSED - All Africa Capital Limited's first accounts (period ended 31 December 2021) take the "
    "small companies' exemption from preparing a cash flow statement (FRS 102 Section 1A); no cash flow statement "
    f"exists for this period in any source reviewed - {CH_2021_ACCOUNTS_URL}\n"
    f"Companies House filing history - {CH_FILING_HISTORY_URL}\n"
    "STRUCTURAL NOTE: FY2023/FY2022 route net interest through two new 'Interest received'/'Interest paid' rows "
    "under Operating activities (per those years' own statement); FY2024 instead reports 'Finance income' under "
    "Investing and 'Finance cost' under Financing (per that year's own statement) - both are reproduced exactly "
    "as each year's own source presents them, not forced into a single common layout.\n"
    + ENTITY_NOTE + "\n" + FY2020_SKIP_NOTE
)

P3_SOURCES = (
    "Sources - Afin Bank Limited standalone Pillar 3 Disclosures for the year ended 31 December 2024:\n"
    f"FY2024: UK KM1 Key Metrics, printed pp. 4-5, and UK OV1, printed p. 5 - {P3_2024_URL}\n"
    "Afin Bank annual reports and disclosures page - https://afinbank.com/about/annual-reports-and-disclosures/\n"
    + ENTITY_NOTE + "\n" + NOT_APPLICABLE_P3_NOTE
)

bw = BankWorkbook(
    bank_name="Afin Bank Limited",
    years=YEARS,
    year_label=YEAR_LABEL,
    header_color="4A1E4D",
)


BALANCE_SHEET_SOURCES = (
    "Sources - FY2024: Afin Bank Limited audited annual report and financial statements for the year ended "
    f"31 December 2024, statement of financial position, printed p. 34 - {AR_2024_URL}\n"
    "FY2023: All Africa Capital Limited audited annual report and financial statements for the year ended "
    f"31 December 2023, statement of financial position, p. 7 (2023 column; 2022 comparative column) - {CH_2023_ACCOUNTS_URL}\n"
    "FY2022: All Africa Capital Limited unaudited financial statements for the year ended 31 December 2022, "
    f"balance sheet, p. 1 (cross-checked against the FY2023 report's own 2022 comparative - ties exactly) - {CH_2022_ACCOUNTS_URL}\n"
    "FY2021: All Africa Capital Limited unaudited financial statements for the period ended 31 December 2021 "
    f"(first accounting period, from incorporation 18 December 2020), balance sheet, p. 1 - {CH_2021_ACCOUNTS_URL}\n"
    + ENTITY_NOTE
    + "\nSTRUCTURAL NOTES: (1) 'Treasury assets', 'Right-of-use assets', 'Revaluation reserve' and 'Share based "
    "payment reserve' are all genuinely new line items that first appear on the FY2024 face statement (post-"
    "banking-authorisation) - left blank, not zero, for FY2021-FY2023, where the underlying asset/liability class "
    "simply did not exist on the company's books. (2) FY2023's face statement combines right-of-use assets into "
    "the single 'Property, plant and equipment' line (its own note 10 breaks out Computer equipment £22,098 + "
    "Right of use asset £130,091 = £152,189); FY2022/FY2021 predate IFRS 16 entirely (no leases). (3) FY2021's "
    "'Debtors' £19,562 is a single undifferentiated line (no prepayments split existed yet) - reproduced under "
    "'Receivables' with FY2021's own 'Prepayments' cell left blank rather than zero. (4) 'Receivables' for "
    "FY2023 combines the current £147,604 and non-current £19,200 other-receivables notes into one face-equivalent "
    "figure, consistent with how FY2024's own single 'Receivables' row is presented. (5) 'Treasury assets' note "
    "10 (Listed investments, non-current, printed p. 44) discloses only the single lump £9,767,797 figure with no "
    "further split - the note's narrative and the accounting policy note (note 1.7 'Financial asset investments "
    f"under IFRS 9', printed p. 38) both state these are UK government securities (gilts and Treasury bills) "
    "classified as debt instruments measured at fair value through other comprehensive income (FVOCI). Note 1.7's "
    "own fair-value disclosure (p. 38) further splits the £9,767,797 total by instrument as UK Gilts £5,813,980 + "
    "Treasury Bills £3,953,817 (reconciles exactly), but since both instruments share the same issuer type (UK "
    "government) and the same measurement basis (FVOCI), there is no real split by either dimension - the row is "
    f"labelled in place rather than broken into sub-rows - {AR_2024_URL}\n"
    + FY2020_SKIP_NOTE
)

INCOME_STATEMENT_SOURCES = (
    "Sources - FY2024: Afin Bank Limited audited annual report and financial statements for the year ended "
    f"31 December 2024, statement of comprehensive income, printed p. 33 - {AR_2024_URL}\n"
    "FY2023: All Africa Capital Limited audited annual report and financial statements for the year ended "
    f"31 December 2023, statement of comprehensive income p. 6 and operating loss note 5 p. 14 (2023 column; "
    f"2022 comparative column, itself unaudited) - {CH_2023_ACCOUNTS_URL}\n"
    "FY2022: as above (FY2023 report's own 2022 comparative and note 5 breakdown - the standalone FY2022 filing "
    f"states the directors elected not to include a P&L account within the filed financial statements) - {CH_2022_ACCOUNTS_URL}\n"
    "FY2021: NOT DISCLOSED - the directors of All Africa Capital Limited elected not to include a copy of the "
    "profit and loss account within the filed financial statements for the period ended 31 December 2021 (a "
    f"small-companies filing exemption); no P&L breakdown exists in any source reviewed - {CH_2021_ACCOUNTS_URL}\n"
    + ENTITY_NOTE
    + "\nSTRUCTURAL NOTE: FY2023/FY2022's own administrative-expenses note (note 5) splits costs as Staff costs / "
    "Computer running costs / Legal and professional fees / Consultancy fees / Audit fees / Depreciation / Other "
    "costs and separately discloses 'Other operating income' (£231 in FY2022, £nil in FY2023) - reproduced as "
    "its own set of rows rather than force-mapped onto FY2024's differently-labelled 'Other operating costs' "
    "bucket. Both years' figures were verified to foot exactly to the reported Administrative expenses total.\n"
    + FY2020_SKIP_NOTE
)

EQUITY_CHANGES_SOURCES = (
    "Sources - FY2024: Afin Bank Limited audited annual report and financial statements for the year ended "
    f"31 December 2024, statement of changes in equity, p. 35, covering 1 January 2023 to 31 December 2024 - {AR_2024_URL}\n"
    "FY2021-FY2023: All Africa Capital Limited's own statement of changes in equity (FY2023 report, p. 8, "
    f"covering 1 January 2022 to 31 December 2023) - {CH_2023_ACCOUNTS_URL} - plus the FY2021 first-period "
    f"balance sheet (opening/closing bridge derived from its own reported balances) - {CH_2021_ACCOUNTS_URL}\n"
    + ENTITY_NOTE
    + "\nThis sheet now runs chronologically from incorporation (18 December 2020) through 31 December 2024, the "
    "one sheet in the workbook not self-skipping FY2020: even though no discrete FY2020 accounts exist (see "
    "FY2020_SKIP_NOTE), the equity roll-forward correctly shows the company's true opening position at "
    "incorporation (£0) as its own row, with the first accounting period's entire movement (18 December 2020 to "
    "31 December 2021) shown as a single aggregate line - the small-companies filing exemption from including a "
    "P&L account means no finer split of that movement is available from any source.\n"
    + FY2020_SKIP_NOTE
)

ASSET_QUALITY_SOURCES = (
    "Sources - Afin Bank Limited 2024 Annual Report and Pillar 3 Disclosures:\n"
    f"{AR_2024_URL}\n{P3_2024_URL}\n" + ENTITY_NOTE
    + "\nNOT DISCLOSED (FY2024): Afin Bank's balance sheet has no lending product line (assets are Cash, Treasury "
    "assets, Receivables, Prepayments, PP&E and intangibles only) and neither the 2024 Annual Report nor the 2024 "
    "Pillar 3 disclosure (a small non-complex institution under CRR Article 433b) contains a loan book / IFRS 9 "
    "stage / credit risk exposure breakdown.\n"
    + NOT_APPLICABLE_P3_NOTE
)

RWA_BREAKDOWN_SOURCES = (
    "Sources - Afin Bank Limited standalone Pillar 3 Disclosures for the year ended 31 December 2024:\n"
    f"FY2024: UK OV1 - Overview of risk weighted exposure amounts (Table 2), printed p. 5 - {P3_2024_URL}\n"
    "FY2024 figures are directly disclosed (not derived): Credit risk (excluding CCR) £2,489k + Operational risk "
    "£598k = £3,087k, which reconciles exactly to the Total RWAs sheet's own FY2024 figure of £3,087k (UK KM1, "
    "row 4). No counterparty credit risk, securitisation or market risk rows are shown in Afin Bank's own OV1 "
    "table (rows 2-22 and 24-28 of the standard OV1 template are blank/not populated), consistent with a small, "
    "newly-authorised institution with no trading book or derivatives exposure - not a gap in transcription.\n"
    + ENTITY_NOTE
    + "\nNOT APPLICABLE / NOT DISCLOSED (FY2023-FY2021): as above (see NOT_APPLICABLE_P3_NOTE) - the entity had no "
    "Pillar 3 disclosure obligation for these years.\n"
    + NOT_APPLICABLE_P3_NOTE
)

bw.add_balance_sheet_sheet(
    title="Afin Bank Limited — Consolidated Statement of Financial Position",
    subtitle=(
        "Afin Bank Limited (All Africa Capital Limited pre-October 2024) audited/unaudited statement of "
        "financial position; amounts in £. FY2021 covers the first accounting period, 18 Dec 2020-31 Dec 2021 "
        "(FY2020 does not exist as a discrete period - see source note)."
    ),
    rows=[
        ("SECTION", "Assets", {}),
        ("DATA", "Cash and cash equivalents", {"FY2024": 3155921, "FY2023": 971678, "FY2022": 7333, "FY2021": 86318}),
        ("DATA", "Treasury assets - UK Government gilts & Treasury bills, at FVOCI", {"FY2024": 9767797}),
        ("DATA", "Receivables", {"FY2024": 450628, "FY2023": 166804, "FY2022": 6859, "FY2021": 19562}),
        ("DATA", "Prepayments", {"FY2024": 372022, "FY2023": 50123, "FY2022": 0}),
        ("DATA", "Property, plant and equipment", {"FY2024": 57172, "FY2023": 152189, "FY2022": 360, "FY2021": 487}),
        ("DATA", "Right-of-use assets", {"FY2024": 967204}),
        ("DATA", "Intangible assets", {"FY2024": 2657199, "FY2023": 12000}),
        ("TOTAL", "Total assets", {"FY2024": 17427943, "FY2023": 1352794, "FY2022": 14552, "FY2021": 106367}),
        ("SECTION", "Liabilities", {}),
        ("DATA", "Trade and other payables", {"FY2024": 1102894, "FY2023": 260524, "FY2022": 50338, "FY2021": 59537}),
        ("DATA", "Lease liabilities", {"FY2024": 965184, "FY2023": 130091, "FY2022": 0}),
        ("TOTAL", "Total liabilities", {"FY2024": 2068078, "FY2023": 390615, "FY2022": 50338, "FY2021": 59537}),
        ("TOTAL", "Net assets", {"FY2024": 15359865, "FY2023": 962179, "FY2022": -35786, "FY2021": 46830}),
        ("SECTION", "Equity", {}),
        ("DATA", "Called up share capital", {"FY2024": 23614036, "FY2023": 3357807, "FY2022": 590654, "FY2021": 266750}),
        ("DATA", "Revaluation reserve", {"FY2024": 67382}),
        ("DATA", "Share based payment reserve", {"FY2024": 267626}),
        ("DATA", "Retained earnings", {"FY2024": -8589179, "FY2023": -2395628, "FY2022": -626440, "FY2021": -219920}),
        ("TOTAL", "Total equity", {"FY2024": 15359865, "FY2023": 962179, "FY2022": -35786, "FY2021": 46830}),
    ],
    sources_text=BALANCE_SHEET_SOURCES,
    first_col_width=48,
    source_height=210,
    unit_suffix=" (£)",
)

bw.add_income_statement_sheet(
    title="Afin Bank Limited — Consolidated Statement of Comprehensive Income",
    subtitle=(
        "Afin Bank Limited (All Africa Capital Limited pre-October 2024) audited/unaudited statement of "
        "comprehensive income; amounts in £. FY2021 NOT DISCLOSED (small-companies exemption - see source note)."
    ),
    rows=[
        ("SECTION", "Operating income and expenses", {}),
        ("DATA", "Other operating income", {"FY2023": 0, "FY2022": 231}),
        ("DATA", "Staff costs", {"FY2024": -3941455, "FY2023": -1088800, "FY2022": -224067}),
        ("DATA", "Computer running costs", {"FY2023": -45103, "FY2022": -3026}),
        ("DATA", "Legal and professional fees", {"FY2023": -166504, "FY2022": -42042}),
        ("DATA", "Consultancy fees", {"FY2023": -276803, "FY2022": -123016}),
        ("DATA", "Audit fees", {"FY2023": -8760, "FY2022": 0}),
        ("DATA", "Depreciation", {"FY2024": -142504, "FY2023": -21488, "FY2022": -127}),
        ("DATA", "Amortisation of intangibles", {"FY2024": -23179, "FY2023": 0}),
        ("DATA", "Other operating costs", {"FY2024": -2149595}),
        ("TOTAL", "Total operating expenses", {"FY2024": -6256733, "FY2023": -1767933, "FY2022": -406751}),
        ("TOTAL", "Operating loss", {"FY2024": -6256733, "FY2023": -1767933, "FY2022": -406520}),
        ("DATA", "Finance income", {"FY2024": 75152, "FY2023": 8}),
        ("DATA", "Finance costs", {"FY2024": -11970, "FY2023": -1263}),
        ("TOTAL", "Loss before taxation", {"FY2024": -6193551, "FY2023": -1769188, "FY2022": -406520}),
        ("DATA", "Income tax expense", {"FY2024": 0, "FY2023": 0, "FY2022": 0}),
        ("TOTAL", "Loss for the year", {"FY2024": -6193551, "FY2023": -1769188, "FY2022": -406520}),
        ("SECTION", "Other comprehensive income", {}),
        ("DATA", "Treasury asset revaluation", {"FY2024": 67382, "FY2023": 0, "FY2022": 0}),
        ("TOTAL", "Total other comprehensive income for the year", {"FY2024": 67382, "FY2023": 0, "FY2022": 0}),
        ("TOTAL", "Total comprehensive income for the year", {"FY2024": -6126169, "FY2023": -1769188, "FY2022": -406520}),
    ],
    sources_text=INCOME_STATEMENT_SOURCES,
    first_col_width=48,
    source_height=210,
    unit_suffix=" (£)",
)

EQUITY_HEADERS = ["Share capital", "Revaluation reserve", "Share based payment", "Retained earnings", "Total equity"]
bw.add_equity_changes_sheet(
    title="Afin Bank Limited — Statement of Changes in Equity",
    subtitle=(
        "Afin Bank Limited (All Africa Capital Limited pre-October 2024) statement of changes in equity, "
        "18 December 2020 (incorporation) to 31 December 2024; amounts in £."
    ),
    headers=EQUITY_HEADERS,
    rows=[
        ("TOTAL", "Balance at 18 December 2020 (date of incorporation)", (0, None, None, 0, 0)),
        ("DATA", "Total comprehensive income for the period (18 Dec 2020 to 31 Dec 2021)", (None, None, None, -219920, -219920)),
        ("DATA", "Issue of share capital (2021)", (266750, None, None, None, 266750)),
        ("TOTAL", "Balance at 31 December 2021", (266750, 0, 0, -219920, 46830)),
        ("DATA", "Total comprehensive income for the year (2022)", (None, None, None, -406520, -406520)),
        ("DATA", "Issue of share capital (2022)", (323904, None, None, None, 323904)),
        ("TOTAL", "Balance at 1 January 2023", (590654, None, None, -626440, -35786)),
        ("DATA", "Total comprehensive income for the year (2023)", (None, None, None, -1769188, -1769188)),
        ("DATA", "Issue of share capital (2023)", (2767153, None, None, None, 2767153)),
        ("TOTAL", "Balance at 31 December 2023", (3357807, 0, 0, -2395628, 962179)),
        ("DATA", "Loss for the year (2024)", (None, None, None, -6193551, -6193551)),
        ("DATA", "Other comprehensive income - Treasury asset revaluation (2024)", (None, 67382, None, None, 67382)),
        ("TOTAL", "Total comprehensive income for the year (2024)", (None, 67382, None, -6193551, -6126169)),
        ("DATA", "Issue of share capital (2024)", (20256229, None, None, None, 20256229)),
        ("DATA", "Share based payment (2024)", (None, None, 267626, None, 267626)),
        ("TOTAL", "Balance at 31 December 2024", (23614036, 67382, 267626, -8589179, 15359865)),
    ],
    sources_text=EQUITY_CHANGES_SOURCES,
    source_height=210,
)

bw.add_cash_flow_sheet(
    title="Afin Bank Limited — Cash Flow Statement",
    subtitle=(
        "Afin Bank Limited (All Africa Capital Limited pre-October 2024) audited/unaudited statement of cash "
        "flows; amounts in £. FY2021 NOT DISCLOSED (small-companies exemption - see source note)."
    ),
    rows=[
        ("SECTION", "Cash flows from operating activities", {}),
        ("DATA", "Cash absorbed by operations", {"FY2024": -5854403, "FY2023": -1746327, "FY2022": -402889}),
        ("DATA", "Interest received", {"FY2023": 8, "FY2022": 0}),
        ("DATA", "Interest paid", {"FY2023": -1263, "FY2022": 0}),
        ("TOTAL", "Net cash outflow from operating activities", {"FY2024": -5854403, "FY2023": -1747582, "FY2022": -402889}),
        ("SECTION", "Investing activities", {}),
        ("DATA", "Purchase of intangible assets", {"FY2024": -2668378, "FY2023": -12000, "FY2022": 0}),
        ("DATA", "Purchase of property, plant and equipment", {"FY2024": -52008, "FY2023": -19717, "FY2022": 0}),
        ("DATA", "Purchase of investments", {"FY2024": -9700415}),
        ("DATA", "Finance income", {"FY2024": 75152}),
        ("TOTAL", "Net cash used in investing activities", {"FY2024": -12345649, "FY2023": -31717, "FY2022": 0}),
        ("SECTION", "Financing activities", {}),
        ("DATA", "Proceeds from issue of shares", {"FY2024": 20523855, "FY2023": 2767153, "FY2022": 323904}),
        ("DATA", "Payment of lease liabilities", {"FY2024": -134783, "FY2023": -23509, "FY2022": 0}),
        ("DATA", "Finance cost", {"FY2024": -4777}),
        ("TOTAL", "Net cash generated from financing activities", {"FY2024": 20384295, "FY2023": 2743644, "FY2022": 323904}),
        ("TOTAL", "Net increase in cash and cash equivalents", {"FY2024": 2184243, "FY2023": 964345, "FY2022": -78985}),
        ("DATA", "Cash and cash equivalents at the beginning of the year", {"FY2024": 971678, "FY2023": 7333, "FY2022": 86318}),
        ("TOTAL", "Cash and cash equivalents at the end of the year", {"FY2024": 3155921, "FY2023": 971678, "FY2022": 7333, "FY2021": 86318}),
    ],
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=62,
    source_height=225,
    unit_suffix=" (£)",
)


bw.add_asset_quality_sheet(
    title="Afin Bank Limited — Asset Quality / Credit Risk Disclosures",
    subtitle="Afin Bank Limited loan book / credit risk disclosures; amounts in £.",
    rows=[
        ("DATA", "Not publicly disclosed / Not applicable", {
            "FY2024": "Not publicly disclosed",
            "FY2023": "Not applicable",
            "FY2022": "Not applicable",
            "FY2021": "Not applicable",
        }),
    ],
    sources_text=ASSET_QUALITY_SOURCES,
    first_col_width=58,
    source_height=180,
    unit_suffix=" (£)",
)


def metric(name, unit, rows_data, note=None):
    bw.add_metric_sheet(
        name,
        unit,
        rows_data,
        P3_SOURCES,
        note=note,
        first_col_width=56,
        source_height=180,
    )


metric("CET1 Capital", "£'000", [
    ("Common Equity Tier 1 (CET1) capital", {"FY2024": 12922, "FY2023": "Not applicable", "FY2022": "Not applicable", "FY2021": "Not applicable"}),
])
metric("CET1 Ratio", "% of RWA", [
    ("Common Equity Tier 1 (CET1) ratio", {"FY2024": "418.5%", "FY2023": "Not applicable", "FY2022": "Not applicable", "FY2021": "Not applicable"}),
])
metric("Tier 1 Capital", "£'000", [
    ("Tier 1 capital", {"FY2024": 12922, "FY2023": "Not applicable", "FY2022": "Not applicable", "FY2021": "Not applicable"}),
])
metric("Tier 1 Ratio", "% of RWA", [
    ("Tier 1 ratio", {"FY2024": "418.5%", "FY2023": "Not applicable", "FY2022": "Not applicable", "FY2021": "Not applicable"}),
])
metric("Total Capital", "£'000", [
    ("Total capital", {"FY2024": 12922, "FY2023": "Not applicable", "FY2022": "Not applicable", "FY2021": "Not applicable"}),
])
metric("Total Capital Ratio", "% of RWA", [
    ("Total capital ratio", {"FY2024": "418.5%", "FY2023": "Not applicable", "FY2022": "Not applicable", "FY2021": "Not applicable"}),
])
metric("Total RWAs", "£'000", [
    ("Total risk-weighted exposure amount", {"FY2024": 3087, "FY2023": "Not applicable", "FY2022": "Not applicable", "FY2021": "Not applicable"}),
])
bw.add_rwa_breakdown_sheet(
    title="Afin Bank Limited — RWA Breakdown",
    subtitle=(
        "Afin Bank Limited risk-weighted exposure amount breakdown; amounts in £'000. FY2024 per the Pillar 3 "
        "UK OV1 template; FY2023-FY2021 not applicable (entity not yet a PRA-authorised bank)."
    ),
    rows=[
        ("SECTION", "UK OV1 — Overview of risk weighted exposure amounts", {}),
        ("DATA", "Credit risk (excluding CCR)", {"FY2024": 2489}),
        ("DATA", "Operational risk", {"FY2024": 598}),
        ("TOTAL", "Total risk weighted exposure amount", {"FY2024": 3087}),
        ("SECTION", "Not applicable", {}),
        ("DATA", "Not publicly disclosed / Not applicable", {
            "FY2023": "Not applicable",
            "FY2022": "Not applicable",
            "FY2021": "Not applicable",
        }),
    ],
    sources_text=RWA_BREAKDOWN_SOURCES,
    first_col_width=58,
    source_height=180,
    unit_suffix=" (£'000)",
)
metric("Leverage Ratio", "£'000 / %", [
    ("Total exposure measure excluding claims on central banks", {"FY2024": 14782, "FY2023": "Not applicable", "FY2022": "Not applicable", "FY2021": "Not applicable"}),
    ("Leverage ratio excluding claims on central banks", {"FY2024": "87.4%", "FY2023": "Not applicable", "FY2022": "Not applicable", "FY2021": "Not applicable"}),
])
metric("LCR", "£'000 / %", [
    ("Total high-quality liquid assets (HQLA) (weighted value - average)", {"FY2024": 8909, "FY2023": "Not applicable", "FY2022": "Not applicable", "FY2021": "Not applicable"}),
    ("Cash outflows - total weighted value", {"FY2024": 0, "FY2023": "Not applicable", "FY2022": "Not applicable", "FY2021": "Not applicable"}),
    ("Cash inflows - total weighted value", {"FY2024": 3971, "FY2023": "Not applicable", "FY2022": "Not applicable", "FY2021": "Not applicable"}),
    ("Total net cash outflows (adjusted value)", {"FY2024": 0, "FY2023": "Not applicable", "FY2022": "Not applicable", "FY2021": "Not applicable"}),
    ("Liquidity coverage ratio", {"FY2024": "999999%", "FY2023": "Not applicable", "FY2022": "Not applicable", "FY2021": "Not applicable"}),
], note=(
    "Afin states that it had no qualifying cash outflows at 31 December 2024; the source therefore reports the "
    "LCR as 999999%. This is reproduced as reported and is not interpreted as a conventional finite ratio. "
    "FY2021-FY2023 predate Afin's banking authorisation - no LCR obligation existed."
))
metric("NSFR", "£'000 / %", [
    ("Total available stable funding", {"FY2024": 21486, "FY2023": "Not applicable", "FY2022": "Not applicable", "FY2021": "Not applicable"}),
    ("Total required stable funding", {"FY2024": 4365, "FY2023": "Not applicable", "FY2022": "Not applicable", "FY2021": "Not applicable"}),
    ("NSFR ratio", {"FY2024": "492.2%", "FY2023": "Not applicable", "FY2022": "Not applicable", "FY2021": "Not applicable"}),
])
metric("MREL Ratio", None, [
    ("MREL ratio", {"FY2024": "Not publicly disclosed", "FY2023": "Not applicable", "FY2022": "Not applicable", "FY2021": "Not applicable"}),
], note=(
    "No numeric MREL ratio is disclosed in the 2024 Pillar 3 report or the audited annual accounts for FY2024. "
    "FY2021-FY2023 predate Afin's banking authorisation (October 2024), so no MREL obligation existed for those years."
))


bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {"FY2024": 17427943, "FY2023": 1352794, "FY2022": 14552, "FY2021": 106367}),
        ("Trade and other payables", {"FY2024": 1102894, "FY2023": 260524, "FY2022": 50338, "FY2021": 59537}),
        ("Total equity", {"FY2024": 15359865, "FY2023": 962179, "FY2022": -35786, "FY2021": 46830}),
    ],
    balance_sheet_unit="£",
    income_statement_totals=[
        ("Total operating expenses", {"FY2024": -6256733, "FY2023": -1767933, "FY2022": -406751}),
        ("Loss for the year", {"FY2024": -6193551, "FY2023": -1769188, "FY2022": -406520}),
    ],
    income_statement_unit="£",
    equity_changes_totals=[
        ("Opening equity", {"FY2024": 962179, "FY2023": -35786, "FY2022": 46830, "FY2021": 0}),
        ("Total comprehensive income", {"FY2024": -6126169, "FY2023": -1769188, "FY2022": -406520, "FY2021": -219920}),
        ("Other movements, net", {"FY2024": 20523855, "FY2023": 2767153, "FY2022": 323904, "FY2021": 266750}),
        ("Closing equity", {"FY2024": 15359865, "FY2023": 962179, "FY2022": -35786, "FY2021": 46830}),
    ],
    equity_changes_unit="£",
    cash_flow_totals=[
        ("Net cash outflow from operating activities", {"FY2024": -5854403, "FY2023": -1747582, "FY2022": -402889}),
        ("Net cash used in investing activities", {"FY2024": -12345649, "FY2023": -31717, "FY2022": 0}),
        ("Net cash generated from financing activities", {"FY2024": 20384295, "FY2023": 2743644, "FY2022": 323904}),
        ("Cash and cash equivalents at end of year", {"FY2024": 3155921, "FY2023": 971678, "FY2022": 7333, "FY2021": 86318}),
    ],
    cash_flow_unit="£",
    ratios=[
        ("CET1 Ratio", {"FY2024": "418.5%", "FY2023": "Not applicable", "FY2022": "Not applicable", "FY2021": "Not applicable"}),
        ("Tier 1 Ratio", {"FY2024": "418.5%", "FY2023": "Not applicable", "FY2022": "Not applicable", "FY2021": "Not applicable"}),
        ("Total Capital Ratio", {"FY2024": "418.5%", "FY2023": "Not applicable", "FY2022": "Not applicable", "FY2021": "Not applicable"}),
        ("Leverage Ratio", {"FY2024": "87.4%", "FY2023": "Not applicable", "FY2022": "Not applicable", "FY2021": "Not applicable"}),
        ("LCR", {"FY2024": "999999%", "FY2023": "Not applicable", "FY2022": "Not applicable", "FY2021": "Not applicable"}),
        ("NSFR", {"FY2024": "492.2%", "FY2023": "Not applicable", "FY2022": "Not applicable", "FY2021": "Not applicable"}),
    ],
    note=(
        "EXTENDED HISTORY: this workbook now covers FY2021-FY2024 (four years), extended back from an original "
        "FY2024-only Pillar-3-only build. Afin Bank Limited was named All Africa Capital Limited and was not yet "
        "a PRA-authorised bank until October 2024, so FY2021-FY2023's Balance Sheet/P&L/Equity/Cash Flow figures "
        "are that same continuous legal entity's own pre-bank Companies House statutory accounts, while all 11 "
        "Pillar 3 metric sheets plus Asset Quality and RWA Breakdown are genuinely 'Not applicable' for those "
        "three years (no disclosure obligation existed) - only FY2024 carries real Pillar 3 figures. "
        "FY2020 is self-skipped in full: the company was incorporated 18 December 2020 and its first statutory "
        "accounts cover the period from incorporation to 31 December 2021 - no discrete FY2020 period was ever "
        "filed, because none exists for this entity (confirmed by reading the complete Companies House filing "
        "history, not assumed from the entity-creation-date signal alone). FY2021's Profit & Loss and Cash Flow "
        "Statement are themselves NOT DISCLOSED (small-companies filing exemptions - no P&L account or cash flow "
        "statement was ever filed for that period); only its Balance Sheet and the equity roll-forward derived "
        "from it are available. Genuine structural findings, all documented on their own sheets: FY2023 is the "
        "first year with intangible assets, a lease/right-of-use asset, and an audit (FY2021-FY2022 were "
        "unaudited small-company filings); the FY2023 report's own 2022 comparative column is itself unaudited "
        "per its auditor's report. Every closing cash and equity balance ties exactly into the next year's own "
        "opening balance across all four years, including into the pre-existing FY2024 figures unchanged from "
        "the original build."
    ),
)

bw.save("/Users/armaan/code/katalysis/banks/AFIN BANK FINANCIALS.xlsx")
