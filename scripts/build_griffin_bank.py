import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

# Griffin Bank Limited (FRN 970920) is a very young UK challenger bank -
# renamed from Griffin Financial Technology Limited on 12 April 2023, held
# only an Authorisation-with-Restrictions (AWR/mobilisation) banking licence
# until 29 February 2024, and changed its fiscal year-end from 30 June to
# 30 September during the process (making its first published period a
# 15-month period rather than 12). Only 3 Annual Reports have ever been
# published (periods ended 30 Sep 2023, 2024, 2025) - there is no FY2021/
# FY2022 history for this entity as a bank at all, so only 3 years are
# included here rather than padding to 5.
YEARS = ["FY2025", "FY2024", "FY2023"]  # most recent first
YEAR_LABEL = {
    "FY2025": "FY2025",
    "FY2024": "FY2024",
    "FY2023": "FY2023 (15mo)",
}

AR2023_URL = "https://cms.griffin.com/griffin-assets/Griffin_Bank_Ltd_2023_Annual_Report_and_Financial_Statements_9c92dd2876.pdf"
AR2024_URL = "https://cms.griffin.com/griffin-assets/Griffin_Bank_Ltd_Annual_Report_2024_b98c8d4c38.pdf"
AR2025_URL = "https://cms.griffin.com/griffin-assets/Griffin_Bank_Ltd_Annual_Report_2025_edeb37eca7.pdf"
P3_2023_URL = "https://cms.griffin.com/griffin-assets/Griffin_Bank_Ltd_Pillar_3_30_Sept_2023_df3ca44acc.pdf"

ENTITY_NOTE = (
    "Griffin Bank Limited (Companies House 10842931) was renamed from Griffin Financial Technology "
    "Limited on 12 April 2023 and held only an Authorisation-with-Restrictions (mobilisation) banking "
    "licence - granted in February 2023, per its own 2023 Pillar 3 Report, which is why that year's LCR and "
    "NSFR are eight-month post-authorisation averages - until it obtained a full unrestricted licence on "
    "29 February 2024. During the mobilisation "
    "period the Company also changed its financial year-end from 30 June to 30 September, so its first "
    "published period (FY2023) is a 15-month period from 1 July 2022 to 30 September 2023, not a "
    "standard 12-month year - both figures are as originally reported, not annualised. FY2023's cash "
    "flow statement is itself labelled 'Unaudited' in the source Annual Report. Only 3 Annual Reports "
    "have ever been published for this entity (FY2023/FY2024/FY2025) - no FY2021/FY2022 data exists."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are Griffin Bank Limited's own Statement of Cash Flows:\n"
    "FY2025: Annual Report and Financial Statements 2025, p.53-54 (Statement of cash flows) - " + AR2025_URL + "\n"
    "FY2024: Annual Report and Financial Statements 2024, p.61 (Statement of cash flows; cross-checked "
    "against its own restated comparative in the 2025 Annual Report, p.53-54 - figures match exactly, "
    "no restatement) - " + AR2024_URL + "\n"
    "FY2023 (15mo): Annual Report and Financial Statements 2023, p.47 (Statement of cash flows, "
    "unaudited, 15 months ended 30 September 2023) - " + AR2023_URL + "\n"
    + ENTITY_NOTE
)


def p3_sources():
    return (
        "Sources - Griffin Bank Limited Pillar 3 basis:\n"
        "FY2023: 2023 Pillar 3 Report (30 September 2023), p.21 (4.1 Disclosure of key metrics - KM1) - "
        + P3_2023_URL + "\n"
        "FY2025 CET1 ratio (112%): Annual Report and Financial Statements 2025, p.3 (Chief Executive's "
        "review) and p.13 (Financial review), both stating 112% (2024: 64%) - " + AR2025_URL + "\n"
        "FY2024 CET1 ratio (64%): Annual Report and Financial Statements 2024, p.4 (Chief Executive's "
        "review) and p.13 (Financial review), both stating 64% (2023: 456%), and independently confirmed "
        "by the FY2025 report's own comparative - " + AR2024_URL + "\n"
        "FY2024/FY2025 (all other metrics): no Pillar 3 disclosure document has been published for either "
        "period - only the 2023 Pillar 3 Report exists on the Bank's own site (re-checked 2026-09-12: "
        "https://griffin.com/reports still lists exactly 6 PDFs across FY2023-FY2025, of which only one is "
        "a Pillar 3 report). Not a data-access gap - confirmed genuinely unpublished, not guessed. Both "
        "Annual Reports were read in full for this re-verification: they disclose the CET1 ratio in "
        "narrative form (captured above) but give no CET1/Tier 1/Total Capital amount, no RWA figure, no "
        "leverage ratio and no numeric LCR - the LCR is described only qualitatively ('materially in "
        "excess of internal risk appetite and regulatory requirements', FY2025 p.92 / FY2024 p.104), which "
        "is not a disclosed value, so those sheets stay blank rather than being inferred. The Bank's own "
        "FY2023 KM1 table notes it does not provide comparative information for the prior "
        "(pre-authorisation) period either, since it was first authorised as a bank (with restrictions) "
        "only in 2023.\n"
        "INDEPENDENTLY RE-VERIFIED 2026-09-15 (multi-year trailing-gap investigation), and the finding above "
        "stands. What was checked this time, and what it rules out:\n"
        "  (a) griffin.com/reports was re-fetched and every PDF link on it enumerated. It still carries "
        "exactly six documents, and the complete list is: Annual Report 2025, Annual Impact Report 2025/2026, "
        "Annual Report 2024, Annual Impact Report 2024/2025, 2023 Annual Report & Financial Statements, and "
        "'Griffin Bank Ltd Pillar 3 30 Sept 2023'. There is no FY2024 or FY2025 Pillar 3 report. griffin.com's "
        "own sitemap.xml contains no other reports/disclosures page, and /pillar-3, /disclosures, /legal and "
        "/regulatory-disclosures all return 404 - so there is no second location to look in.\n"
        "  (b) The FY2024 and FY2025 Annual Reports were re-downloaded and full-text searched again. The only "
        "regulatory-capital number in either is the CET1 ratio already captured above (FY2025 p.3/p.13: '112% "
        "(2024: 64%)'; FY2024 p.4/p.13: '64% (2023: 456%)'). Searching both for 'risk weighted'/'RWA'/'own "
        "funds'/'total capital'/'Tier 2'/'leverage'/'MREL'/'NSFR' returns no figure at all, and the LCR "
        "passage is verbatim identical in both years and purely qualitative.\n"
        "  (c) IT IS A REGULATORY EXEMPTION AFTER ALL - this paragraph CORRECTS the earlier conclusion "
        "recorded here, which read 'NOT a regulatory exemption' on the strength of Griffin's own 2023 Pillar 3 "
        "Report describing it as a 'small and non-complex institution'. That earlier reading conflated two "
        "different reliefs and mis-dated the evidence. Corrected 2026-09-15 (cross-bank SDDT date-fit pass) "
        "against the PRA's own firm-level register.\n"
        "      THE REGISTER ROW: Bank of England consolidated list of waivers and modifications granted to "
        "PRA-authorised firms (downloaded 2026-09-15, "
        "https://www.bankofengland.co.uk/-/media/boe/files/prudential-regulation/authorisations/"
        "waivers-and-modifications-of-rules/consolidated-waivers-pra-firms.csv) carries a row for FRN 970920, "
        "'Griffin Bank Ltd': 'Modification by Consent - PRA Rulebook - CRR Firms - Rule 3.1 of the SDDT Regime "
        "- General Application Part', rule 'SDDT Regime - General Application', sub rule 'Ru 3.1', waiver ref "
        "'A00007614P.pdf', START DATE 05/03/2024, NO END DATE. Rule 3.1 is the actual opt-in by which a firm "
        "becomes a Small Domestic Deposit Taker; it is the operative rule, not one of the eligibility-criteria "
        "modifications (rules 1.2 / 2.1(9) / 2.6) that some firms hold without being SDDTs. Griffin holds no "
        "such criteria-only row - the 3.1 row is the only SDDT entry against FRN 970920. The register's dating "
        "was validated on two independent controls in the same pass (Cynergy's 3.1 row starts 17/01/2025, "
        "matching its annual report's stated approval date to the day; Vanquis's starts 13/03/2024, matching "
        "its recorded 'March 2024').\n"
        "      WHY BOTH FACTS ARE TRUE AT ONCE - it is a matter of dates, not a contradiction. The SNCI "
        "statement is real but it is dated: the 2023 Pillar 3 Report is explicitly 'the Pillar 3 disclosures "
        "for Griffin Bank Ltd (we or Griffin) as of 30 September 2023' (Introduction, p.2) and says at section "
        "1.2 'As a small and non-complex institution, we have prepared these disclosures in line with the "
        "relevant guidance in the Disclosure (CRR) part of the PRA Rulebook'. That report covers the period "
        "ended 30 SEPTEMBER 2023 and therefore PREDATES the 5 March 2024 modification by roughly five months. "
        "Griffin published as an SNCI for FY2023 because on that reference date it was one and had not yet "
        "opted in; it then took the SDDT modification on 5 March 2024. The two routes are NOT the same and "
        "must not be conflated in this workbook: Article 433b (small and non-complex institution) REDUCES "
        "disclosure to an annual subset, so an SNCI still owes a Pillar 3 report; Rule 3.1 of the SDDT Regime "
        "REMOVES the Pillar 3 disclosure obligation outright. Only the second explains a total absence.\n"
        "      DATE FIT - the modification covers BOTH outstanding gap years, on either reading of when SDDT "
        "disclosure relief bites. Griffin's accounting reference date is 30 SEPTEMBER, confirmed at Companies "
        "House (company 10842931, accounts filed for periods ended 30 June 2021, 30 June 2022, then 30 "
        "September 2023, 2024 and 2025 - the year-end moved mid-history, which is why FY2023 is a 15-month "
        "period). So FY2024 ended 30 September 2024 and FY2025 ended 30 September 2025, both AFTER the "
        "05/03/2024 start date, and both also after 1 July 2024, the date PS15/23 made the SDDT disclosure "
        "requirements effective. (RE-DOWNLOADED AND RE-CHECKED 2026-09-15 under a maximum-effort sweep that "
        "treated every prior 'unavailable' verdict in this project as unproven: the register was pulled fresh "
        "from the Bank of England - 2,919 rows, 135 of them SDDT Rule 3.1 modifications - and Griffin's row "
        "reproduces the citation above to the character, including waiver ref A00007614P.pdf and start date "
        "05/03/2024 with no end date. The register is a living document, so this confirms the row has not "
        "been withdrawn or re-dated since the original check.) FY2024 and FY2025 are therefore an EVIDENCED "
        "STRUCTURAL ABSENCE, not a "
        "sourcing failure and not merely the Bank neglecting to publish.\n"
        "      WHAT THE EXEMPTION DOES NOT EXPLAIN: nothing is read back onto FY2023. FY2023 predates the "
        "modification, Griffin did publish a full Pillar 3 report for it, and this workbook's FY2023 KM1 "
        "figures are transcribed from that report in the normal way. There is no earlier gap year to consider "
        "- see (e), no reporting period exists for this entity before the 15 months ended 30 September 2023.\n"
        "      Consistent with the register, neither the FY2024 nor the FY2025 Annual Report mentions 'SDDT', "
        "'Small Domestic Deposit Taker', 'Strong and Simple' or a modification by consent - both were "
        "re-downloaded and full-text searched again on 2026-09-15 (text-native, 306k and 258k extracted "
        "characters respectively, so not scanned images producing a false negative), and neither contains the "
        "string 'Pillar 3' even once. A firm that has opted out has nothing to say about Pillar 3, so silence "
        "in the Annual Reports corroborates the register rather than undercutting it - but note that the "
        "register, not the Annual Report, is the evidence here; Griffin does not state the opt-in in its own "
        "words anywhere this pass could find. Separately, do not confuse this SDDT DISCLOSURE exemption, which "
        "is in force now, with the SDDT CAPITAL regime that starts 1 January 2027.\n"
        "  (d) NOT an entity cessation either. Griffin Bank Ltd (FRN 970920) appears in the Bank of England's "
        "own 'List of banks' as at 30 September 2026, and its FY2024 and FY2025 Annual Reports were both "
        "published normally - the bank is trading and its balance sheet grew from £18.7m to £119.6m over "
        "FY2025.\n"
        "  (e) The early years are genuinely outside any disclosure obligation: Griffin was authorised as a "
        "bank by the PRA (with restrictions) in FEBRUARY 2023 and exited mobilisation with a full unrestricted "
        "licence on 29 February 2024. Its FY2023 Pillar 3 report says so directly ('our liquidity levels ... "
        "have remained comfortably above the minimum regulatory and internal requirements since authorisation "
        "(with restrictions) in February 2023') and footnotes its KM1/OV1 tables 'We were authorised as a bank "
        "by the PRA (with restrictions) in 2023, and so we do not provide comparative information for the "
        "prior period'; its FY2023 LCR and NSFR are explicitly eight-month post-authorisation averages "
        "(Feb-Sep 2023). The 15-month period ended 30 September 2023 is therefore the first reporting period "
        "for which any Pillar 3 metric can exist for this entity.\n"
        "CELL CONVENTION (introduced 2026-09-15): FY2024 and FY2025 now read 'Not required (SDDT)' on every "
        "Pillar 3 metric sheet rather than being left blank. A blank cell is indistinguishable from an "
        "unresearched gap and had caused this bank to be re-chased repeatedly; the explicit marker records "
        "that the obligation itself does not exist for those years. The sole exception is the CET1 Ratio "
        "sheet, which does carry FY2024/FY2025 values - not from a Pillar 3 document (none exists) but from "
        "the Annual Report narrative, which continues to state the ratio voluntarily.\n"
        "SOURCE-DATE RESTATEMENT of the 30 September 2023 Pillar 3, checked against the document's own text "
        "on 2026-09-15 because the file is dated to a SEPTEMBER reference date rather than a December "
        "year-end and could otherwise be mis-mapped: its Introduction (p.2) reads 'Griffin) as of 30 "
        "September 2023' and 'This Pillar 3 document should be read in conjunction with the 2023 Annual "
        "Report and Financial Statements for the period ended 30th September 2023'. Griffin's accounting "
        "reference date IS 30 September (moved from 30 June during mobilisation, which is why FY2023 spans "
        "15 months from 1 July 2022). The document therefore maps to FY2023 in this workbook - the same "
        "reference date as the FY2023 Annual Report - and is not a stub or interim period.\n"
        "USER-ACTIONABLE: there is nothing further to fetch online. FY2024/FY2025 KM1 figures would have to be "
        "requested from Griffin directly (or read from PRA regulatory returns, which are not public).\n"
        + ENTITY_NOTE
    )


STATEMENTS_SOURCES = (
    "Sources - all figures are Griffin Bank Limited's own primary financial statements:\n"
    "FY2025: Annual Report and Financial Statements 2025, p.51 (Statement of Financial Position), "
    "p.50 (Statement of comprehensive income), p.52 (Statement of changes in equity) - " + AR2025_URL + "\n"
    "FY2024: Annual Report and Financial Statements 2024, p.59 (Statement of financial position), "
    "p.58 (Statement of comprehensive income), p.60-61 (Statement of changes in equity) - " + AR2024_URL + "\n"
    "FY2023 (15mo, unaudited): Annual Report and Financial Statements 2023, p.45 (Statement of "
    "financial position), p.44 (Statement of comprehensive income), p.46 (Statement of changes in "
    "equity) - " + AR2023_URL + "\n"
    "All 3 documents are text-native (no scanned/image-only pages) - transcribed directly from "
    "extracted text, cross-checked against each later report's own comparative column where "
    "available (all agree exactly, no restatements found).\n"
    + ENTITY_NOTE
)

bw = BankWorkbook(bank_name="Griffin Bank Limited", years=YEARS, year_label=YEAR_LABEL, header_color="3480C7")

# ---------------------------------------------------------------
# Balance Sheet - built first per the equity reconciliation ladder, so
# each year's own Total equity figure is an independent check value for
# the Statement of Changes in Equity sheet below.
# ---------------------------------------------------------------
balance_sheet_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and cash equivalents", {"FY2025": 7326998, "FY2024": 2364540, "FY2023": 270150}),
    ("TOTAL", "Total debt securities", {"FY2025": 106511170, "FY2024": 12709240, "FY2023": 8551308}),
    ("DATA", "Money market funds, FVTPL (UK gilts/sovereign-backed)", {"FY2025": 100587287, "FY2024": 12709240, "FY2023": 8551308}),
    ("DATA", "UK Treasury bills, FVTPL", {"FY2025": 5923883, "FY2024": 0, "FY2023": 0}),
    ("DATA", "Trade and other receivables", {"FY2025": 1380080, "FY2024": 1430220, "FY2023": 1085821}),
    ("DATA", "Intangible assets", {"FY2025": 4194662, "FY2024": 2073199, "FY2023": 197614}),
    ("DATA", "Property, plant and equipment", {"FY2025": 138510, "FY2024": 148461, "FY2023": 126821}),
    ("TOTAL", "Total assets", {"FY2025": 119551420, "FY2024": 18725660, "FY2023": 10231714}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Customer deposits", {"FY2025": 101783429, "FY2024": 2070144}),
    ("DATA", "Trade and other payables", {"FY2025": 1121665, "FY2024": 1372107, "FY2023": 776298}),
    ("DATA", "Contract liabilities", {"FY2025": 138627, "FY2024": 108984, "FY2023": 115000}),
    ("DATA", "Borrowings", {"FY2025": 0, "FY2024": 0, "FY2023": 579173}),
    ("TOTAL", "Total liabilities", {"FY2025": 103043721, "FY2024": 3551235, "FY2023": 1470471}),
    ("SECTION", "Equity", {}),
    ("DATA", "Share capital", {"FY2025": 23, "FY2024": 16, "FY2023": 13}),
    ("DATA", "Share premium account", {"FY2025": 60901935, "FY2024": 49559702, "FY2023": 30877722}),
    ("DATA", "Employee share option reserve", {"FY2025": 3701831, "FY2024": 1653057, "FY2023": 1039179}),
    ("DATA", "Warrant reserve", {"FY2025": 101283, "FY2024": 101283, "FY2023": 101283}),
    ("DATA", "Accumulated losses", {"FY2025": -48197373, "FY2024": -36139633, "FY2023": -23256954}),
    ("TOTAL", "Total equity", {"FY2025": 16507699, "FY2024": 15174425, "FY2023": 8761243}),
    ("TOTAL", "Total liabilities and equity", {"FY2025": 119551420, "FY2024": 18725660, "FY2023": 10231714}),
]

bw.add_balance_sheet_sheet(
    title="Griffin Bank Limited — Balance Sheet",
    subtitle="Bank-only (no group); FY2023 covers a 15-month period ended 30 September 2023 and is "
              "labelled unaudited in the source. £.",
    rows=balance_sheet_rows,
    sources_text=STATEMENTS_SOURCES + (
        "\n\nPRESENTATION NOTE: Customer deposits first appear as a Balance Sheet line in FY2024 - the Bank "
        "held no customer deposits at all as at 30 September 2023, its first full period as an authorised "
        "bank (confirmed by that year's own Balance Sheet having no such line) - genuinely nil, not a gap.\n\n"
        "DEBT SECURITIES BREAKDOWN (Note 12, 'Investments in financial assets'): FY2025: Annual Report and "
        "Financial Statements 2025, p.73-74 - " + AR2025_URL + " - splits the FY2025/FY2024 comparative "
        "into 'Debt securities (solely Money Market Funds)' 100,587,287 / 12,709,240 and 'Treasury bills' "
        "5,923,883 / 0, both classified as 'Financial assets recorded as FVTPL', reconciling exactly to the "
        "Total investments row (106,511,170 / 12,709,240). The note explains the Money Market Funds invest "
        "in government bonds, notes and bills issued or guaranteed by the UK government (or another "
        "sovereign government), and that Treasury bills are issued by the UK government via the Debt "
        "Management Office - both sub-rows are UK government/sovereign-backed, all FVTPL. FY2024: Annual "
        "Report and Financial Statements 2024, p.77-78 - " + AR2024_URL + " - shows the FY2024/FY2023 "
        "comparative as 100% 'Debt securities (solely Money Market Funds)' (12,709,240 / 8,551,308, no "
        "Treasury bills held in either year - genuinely nil, not a gap), describing the fund as a 'UK "
        "Sovereign Gilt Money Market Fund'. FY2023 (15mo): Annual Report and Financial Statements 2023, "
        "p.65-66 - " + AR2023_URL + " - confirms the same, 100% in a single 'UK Sovereign Gilt Money "
        "Market Fund' (8,551,308), also described elsewhere in that report (p.66/4184) as valued at an "
        "active quoted market price. No amortised-cost or held-to-maturity/AFS portion is disclosed in any "
        "year - the entire debt securities book is FVTPL in every published Annual Report."
    ),
    first_col_width=64,
    source_height=340,
    unit_suffix=" (£)",
)

# ---------------------------------------------------------------
# Profit & Loss
# ---------------------------------------------------------------
income_statement_rows = [
    ("SECTION", "Revenue", {}),
    ("DATA", "Net interest income", {"FY2025": 787929, "FY2024": 661153, "FY2023": 207121}),
    ("DATA", "Net fees and commissions", {"FY2025": 1137886, "FY2024": 83480, "FY2023": 84335}),
    ("TOTAL", "Total net revenue", {"FY2025": 1925815, "FY2024": 744633, "FY2023": 291456}),
    ("SECTION", "Operating costs", {}),
    ("DATA", "Administrative expenses", {"FY2025": -13467508, "FY2024": -13477876, "FY2023": -12906136}),
    ("DATA", "Other expenses", {"FY2025": -516456, "FY2024": -156686, "FY2023": -104904}),
    ("TOTAL", "Total operating costs", {"FY2025": -13983964, "FY2024": -13634562, "FY2023": -13011040}),
    ("TOTAL", "Loss before tax", {"FY2025": -12058149, "FY2024": -12889929, "FY2023": -12719584}),
    ("DATA", "Tax", {"FY2025": 0, "FY2024": 0, "FY2023": 0}),
    ("TOTAL", "Loss for the year/period after taxation", {"FY2025": -12058149, "FY2024": -12889929, "FY2023": -12719584}),
    ("SECTION", "Other comprehensive income", {}),
    ("DATA", "Other gains and losses", {"FY2025": 409, "FY2024": 7250, "FY2023": -1108}),
    ("TOTAL", "Total comprehensive income/(loss) for the year/period", {"FY2025": -12057740, "FY2024": -12882679, "FY2023": -12720692}),
]

bw.add_income_statement_sheet(
    title="Griffin Bank Limited — Profit & Loss",
    subtitle="Bank-only (no group); FY2023 covers a 15-month period ended 30 September 2023 and is "
              "labelled unaudited in the source. All results are from continuing operations. £.",
    rows=income_statement_rows,
    sources_text=STATEMENTS_SOURCES + (
        "\n\nTax was £nil in all 3 periods (no tax charge or credit disclosed - confirmed by reading each "
        "year's own P&L in full)."
    ),
    first_col_width=64,
    source_height=260,
    unit_suffix=" (£)",
)

# ---------------------------------------------------------------
# Statement of Changes in Equity (chronological) - built using the per-year
# reconciliation ladder: Balance Sheet built first (above), then each
# year's closing balance checked against both the next year's own opening
# balance and that year's own Balance Sheet Total equity. Ties exactly at
# every boundary - zero plug rows needed.
# ---------------------------------------------------------------
equity_changes_rows = [
    ("TOTAL", "Balance at 1 July 2022", (10, 20122137, None, None, -10536262, 9585885)),
    ("DATA", "Loss for the period (FY2023, 15mo)", (None, None, None, None, -12719584, -12719584)),
    ("DATA", "Other comprehensive loss for the period (FY2023)", (None, None, None, None, -1108, -1108)),
    ("DATA", "Net issue of share capital (FY2023)", (3, 10755585, None, None, None, 10755588)),
    ("DATA", "Issue of employee share options (FY2023)", (None, None, 1039179, None, None, 1039179)),
    ("DATA", "Net issue/(release) of warrants (FY2023)", (None, None, None, 101283, None, 101283)),
    ("TOTAL", "Balance at 30 September 2023", (13, 30877722, 1039179, 101283, -23256954, 8761243)),
    ("DATA", "Loss for the year (FY2024)", (None, None, None, None, -12889929, -12889929)),
    ("DATA", "Other comprehensive income for the year (FY2024)", (None, None, None, None, 7250, 7250)),
    ("DATA", "Net issue of share capital (FY2024)", (3, 18681980, None, None, None, 18681983)),
    ("DATA", "Issue of employee share options (FY2024)", (None, None, 613878, None, None, 613878)),
    ("TOTAL", "Balance at 30 September 2024", (16, 49559702, 1653057, 101283, -36139633, 15174425)),
    ("DATA", "Loss for the year (FY2025)", (None, None, None, None, -12058149, -12058149)),
    ("DATA", "Other comprehensive income for the year (FY2025)", (None, None, None, None, 409, 409)),
    ("DATA", "Net issue of share capital (FY2025)", (7, 11342233, None, None, None, 11342240)),
    ("DATA", "Issue of employee share options (FY2025)", (None, None, 2048774, None, None, 2048774)),
    ("TOTAL", "Balance at 30 September 2025", (23, 60901935, 3701831, 101283, -48197373, 16507699)),
]

bw.add_equity_changes_sheet(
    title="Griffin Bank Limited — Statement of Changes in Equity",
    subtitle="Bank-only (no group); FY2023 opening/period figures cover the 15 months ended 30 September "
              "2023 and are labelled unaudited in the source. £. Ties exactly to the Balance Sheet's own "
              "Total equity at every year-end - no plug rows needed.",
    headers=["Share capital", "Share premium account", "Employee share option reserve", "Warrant reserve", "Accumulated losses", "Total equity"],
    rows=equity_changes_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=76,
    source_height=260,
)

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Loss for the year/period after taxation", {
        "FY2025": -12058149, "FY2024": -12889929, "FY2023": -12719584,
    }),
    ("DATA", "Finance income", {"FY2025": -787929, "FY2024": -661153, "FY2023": -207121}),
    ("DATA", "Fair value on warrants expense", {"FY2025": 0, "FY2024": 0, "FY2023": 101283}),
    ("DATA", "Depreciation of property, plant and equipment", {"FY2025": 89059, "FY2024": 87363, "FY2023": 82107}),
    ("DATA", "Loss on disposal of property, plant and equipment", {"FY2023": 0}),
    ("DATA", "Amortisation of intangible assets", {"FY2025": 427397, "FY2024": 69323, "FY2023": 22797}),
    ("DATA", "Share-based payment expense", {"FY2025": 2048775, "FY2024": 613878, "FY2023": 1039179}),
    ("TOTAL", "Operating cash flows before movements in working capital", {
        "FY2025": -10280847, "FY2024": -12780518, "FY2023": -11681339,
    }),
    ("DATA", "Change/(increase) in trade and other receivables", {"FY2025": 50140, "FY2024": -344399, "FY2023": -337582}),
    ("DATA", "Change/(increase) in customer deposits", {"FY2025": 99713285, "FY2024": 2070144}),
    ("DATA", "Change/(increase) in trade and other payables", {"FY2025": -250442, "FY2024": 595809, "FY2023": -160031}),
    ("DATA", "Change in contract liabilities", {"FY2025": 29643, "FY2024": -6016, "FY2023": 115000}),
    ("TOTAL", "Net cash from/(used in) operating activities", {
        "FY2025": 89261779, "FY2024": -10464980, "FY2023": -12063952,
    }),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Interest received", {"FY2025": 2385325, "FY2024": 670900, "FY2023": 370741}),
    ("DATA", "Purchases of debt securities", {"FY2025": -297626768, "FY2024": -37188716, "FY2023": -14891308}),
    ("DATA", "Proceeds on disposal of debt securities", {"FY2025": 209748720, "FY2024": 33030785, "FY2023": 6340000}),
    ("DATA", "Purchases of Treasury bills", {"FY2025": -20713633}),
    ("DATA", "Proceeds on disposal and maturity of Treasury bills", {"FY2025": 14789751}),
    ("DATA", "Purchases of supranational bonds", {"FY2025": -3122866}),
    ("DATA", "Proceeds on disposal and maturity of supranational bonds", {"FY2025": 3122866}),
    ("DATA", "Proceeds on disposal of property, plant and equipment", {"FY2025": 5011, "FY2024": 1107}),
    ("DATA", "Purchases of property, plant and equipment", {"FY2025": -84119, "FY2024": -110110, "FY2023": -144868}),
    ("DATA", "Capitalisation of intangible assets / purchases of patents and trademarks", {
        "FY2025": -2548860, "FY2024": -1944908, "FY2023": -202536,
    }),
    ("TOTAL", "Net cash from/(used in) investing activities", {
        "FY2025": -94044573, "FY2024": -5540942, "FY2023": -8527971,
    }),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Interest paid", {"FY2025": -1597396, "FY2024": -9747, "FY2023": -163620}),
    ("DATA", "Repayments of loans and borrowings", {"FY2024": -579173, "FY2023": -777435}),
    ("DATA", "Transaction costs related to issuing shares", {"FY2025": -213963, "FY2024": -454668, "FY2023": -411555}),
    ("DATA", "Proceeds on issue of shares", {"FY2025": 11556203, "FY2024": 19136651, "FY2023": 11167143}),
    ("TOTAL", "Net cash from/(used in) financing activities", {
        "FY2025": 9744844, "FY2024": 18093063, "FY2023": 9814533,
    }),
    ("TOTAL", "Net increase/(decrease) in cash and cash equivalents", {
        "FY2025": 4962049, "FY2024": 2087140, "FY2023": -10777390,
    }),
    ("DATA", "Cash and cash equivalents at the beginning of the year/period", {
        "FY2025": 2364540, "FY2024": 270150, "FY2023": 11048648,
    }),
    ("DATA", "Effect of foreign exchange rate changes", {"FY2025": 409, "FY2024": 7250, "FY2023": -1108}),
    ("TOTAL", "Cash and cash equivalents at the end of the year/period", {
        "FY2025": 7326998, "FY2024": 2364540, "FY2023": 270150,
    }),
]

bw.add_cash_flow_sheet(
    title="Griffin Bank Limited — Statement of Cash Flows",
    subtitle="Bank-only (no group); FY2023 covers a 15-month period ended 30 September 2023 and is "
              "labelled unaudited in the source; see the source note below",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=70,
    source_height=170,
    unit_suffix=" (£)",
)

# ---------------------------------------------------------------
# Asset Quality: the Bank has no customer lending at all in any of the 3
# published years - confirmed explicitly in its own Financial risk
# management note ("As the Bank has no customer lending at this stage, the
# main credit risk to which the Bank is exposed is counterparty risk
# associated with its placements at banks and its investments" - AR2025
# p.93, Note 28 Financial risk management, Credit risk) and by all 3
# years' own Balance Sheets having no "Loans and advances to customers"
# line at all - genuinely nil, not a data gap.
# ---------------------------------------------------------------
asset_quality_rows = [
    ("DATA", "Not publicly disclosed - the Bank has no customer lending in any of the 3 published years "
             "(confirmed explicitly in its own Note 28 'Financial risk management, Credit risk' and by the "
             "absence of any loan line on the Balance Sheet) - see source note.", {}),
]

bw.add_asset_quality_sheet(
    title="Griffin Bank Limited — Asset Quality / Credit Risk Disclosures",
    subtitle="No customer lending exists at all in FY2023-FY2025 - see source note.",
    rows=asset_quality_rows,
    sources_text=(
        "Sources - Griffin Bank Limited's own Note 28 'Financial risk management' (Annual Report and "
        "Financial Statements 2025, p.93, Credit risk section) - " + AR2025_URL + " - states: \"As the "
        "Bank has no customer lending at this stage, the main credit risk to which the Bank is exposed is "
        "counterparty risk associated with its placements at banks and its investments.\" Confirmed against "
        "all 3 years' own Balance Sheets (FY2023-FY2025), none of which show a Loans and advances to "
        "customers line at all - the Bank's only interest-bearing assets are cash/bank placements and debt "
        "securities/Treasury bills/supranational bonds (see Balance Sheet sheet).\n\n" + ENTITY_NOTE
    ),
    first_col_width=90,
    source_height=200,
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
# FY2024 and FY2025 are STRUCTURALLY EXEMPT, not unresearched. Griffin Bank Ltd
# (FRN 970920) holds a Modification by Consent of Rule 3.1 of the SDDT Regime -
# General Application Part (waiver ref A00007614P.pdf, start date 05/03/2024, no
# end date) on the Bank of England's consolidated register of waivers and
# modifications granted to PRA-authorised firms. Rule 3.1 is the Small Domestic
# Deposit Taker opt-in and it REMOVES the Pillar 3 disclosure obligation outright
# (unlike Article 433b / small-and-non-complex status, which merely REDUCES it,
# and unlike the eligibility-criteria rules 1.2 / 2.1(9) / 2.6, which have no
# disclosure effect at all). Griffin's accounting reference date is 30 September,
# so FY2024 (30 Sep 2024) and FY2025 (30 Sep 2025) both end after that start date.
# Independently re-confirmed 2026-09-15 by enumerating every PDF link on
# https://griffin.com/reports: six documents, exactly one of which is a Pillar 3
# report, and it is dated 30 September 2023.
#
# These cells are written explicitly rather than left blank because an empty cell
# is indistinguishable from an unresearched gap and gets re-chased indefinitely.
SDDT_EXEMPT_YEARS = ["FY2025", "FY2024"]
SDDT_CELL = "Not required (SDDT)"


def metric(name, unit, rows_data, sources_text, note=None):
    rows_data = [(label, {**{y: SDDT_CELL for y in SDDT_EXEMPT_YEARS}, **values})
                 for label, values in rows_data]
    bw.add_metric_sheet(name, f"{unit}" if unit else None,
                         rows_data, sources_text, note=note, first_col_width=44, source_height=130)


metric(
    "CET1 Capital", "£'000",
    [("Common Equity Tier 1 (CET1) capital", {"FY2023": 8564})],
    p3_sources(),
)
metric(
    "CET1 Ratio", "%",
    [("CET1 ratio", {"FY2025": "112%", "FY2024": "64%", "FY2023": "456%"})],
    p3_sources(),
    note="An extreme FY2023 ratio reflecting the Bank's genuine early-mobilisation position (capital "
         "raised ahead of loan-book/RWA growth, per the Bank's own FY2023 Pillar 3 report), not a "
         "transcription error - the KM1 table's own RWA figure (£1,879k) against £8,564k of CET1 capital "
         "is internally consistent. The ratio falls to 64% (FY2024) and rises to 112% (FY2025) as the "
         "balance sheet grows; FY2024/FY2025 come from the Annual Report narrative (no Pillar 3 document "
         "exists for those years), which discloses the CET1 ratio only - no CET1 capital amount, RWA "
         "figure or other KM1 line is given, so those sheets stay blank for FY2024/FY2025.",
)
metric(
    "Tier 1 Capital", "£'000",
    [("Tier 1 capital", {"FY2023": 8564})],
    p3_sources(),
    note="No Additional Tier 1 instruments - Tier 1 capital equals CET1 capital in the source.",
)
metric(
    "Tier 1 Ratio", "%",
    [("Tier 1 ratio", {"FY2023": "456%"})],
    p3_sources(),
)
metric(
    "Total Capital", "£'000",
    [("Total capital", {"FY2023": 8564})],
    p3_sources(),
    note="No Tier 2 instruments - Total capital equals CET1/Tier 1 capital in the source.",
)
metric(
    "Total Capital Ratio", "%",
    [("Total capital ratio", {"FY2023": "456%"})],
    p3_sources(),
)
metric(
    "Total RWAs", "£'000",
    [("Total risk-weighted exposure amount", {"FY2023": 1879})],
    p3_sources(),
)

# ---------------------------------------------------------------
# RWA Breakdown - only FY2023 has a Pillar 3 report at all (see p3_sources'
# note - no Pillar 3 disclosure has been published for FY2024/FY2025).
# Sourced from the FY2023 Pillar 3 Report's own OV1 table.
# ---------------------------------------------------------------
rwa_breakdown_rows = [
    ("DATA", "Credit risk (excluding counterparty credit risk)",
     {"FY2023": 706, "FY2024": SDDT_CELL, "FY2025": SDDT_CELL}),
    ("DATA", "Operational risk",
     {"FY2023": 1174, "FY2024": SDDT_CELL, "FY2025": SDDT_CELL}),
    ("TOTAL", "Total risk-weighted exposure amount",
     {"FY2023": 1879, "FY2024": SDDT_CELL, "FY2025": SDDT_CELL}),
]

bw.add_rwa_breakdown_sheet(
    title="Griffin Bank Limited — RWA Breakdown",
    subtitle="Only FY2023 has a published Pillar 3 report - see source note.",
    rows=rwa_breakdown_rows,
    sources_text=p3_sources() + (
        "\n\nGENUINE £1k ROUNDING GAP, not force-reconciled: the OV1 table's own category figures (Credit "
        "risk £706k + Operational risk £1,174k = £1,880k) sum to £1k more than the same document's own KM1 "
        "table Total risk-weighted exposure amount (£1,879k) - both reproduced as disclosed; the KM1 total "
        "is used on the Total RWAs sheet per project convention."
    ),
    first_col_width=64,
    source_height=200,
)

metric(
    "Leverage Ratio", "%",
    [("Leverage ratio excluding claims on central banks", {"FY2023": "91%"})],
    p3_sources(),
)
metric(
    "LCR", "%",
    [("Liquidity coverage ratio (average of 8 months reported LCR post-authorisation)", {"FY2023": "2,675%"})],
    p3_sources(),
    note="An extreme ratio for the same genuine early-mobilisation reason as the capital ratios above - "
         "the Bank held far more high-quality liquid assets (£10,387k weighted) than its tiny net cash "
         "outflow (£388k) required this early in its life.",
)
metric(
    "NSFR", "%",
    [("Net stable funding ratio (average of 8 months reported NSFR post-authorisation)", {"FY2023": "1,034%"})],
    p3_sources(),
)

bw.add_not_disclosed_metric_sheets(["MREL Ratio"], sources_text=p3_sources())

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {"FY2025": 119551420, "FY2024": 18725660, "FY2023": 10231714}),
        ("Debt securities", {"FY2025": 106511170, "FY2024": 12709240, "FY2023": 8551308}),
        ("Customer deposits", {"FY2025": 101783429, "FY2024": 2070144}),
        ("Total equity", {"FY2025": 16507699, "FY2024": 15174425, "FY2023": 8761243}),
    ],
    balance_sheet_unit="£",
    income_statement_totals=[
        ("Total net revenue", {"FY2025": 1925815, "FY2024": 744633, "FY2023": 291456}),
        ("Total operating costs", {"FY2025": -13983964, "FY2024": -13634562, "FY2023": -13011040}),
        ("Loss for the year/period after taxation", {"FY2025": -12058149, "FY2024": -12889929, "FY2023": -12719584}),
    ],
    income_statement_unit="£",
    equity_changes_totals=[
        ("Opening equity", {"FY2025": 15174425, "FY2024": 8761243, "FY2023": 9585885}),
        ("Loss for the year/period", {"FY2025": -12058149, "FY2024": -12889929, "FY2023": -12719584}),
        ("Other movements, net", {"FY2025": 13391423, "FY2024": 19303111, "FY2023": 11894942}),
        ("Closing equity", {"FY2025": 16507699, "FY2024": 15174425, "FY2023": 8761243}),
    ],
    equity_changes_unit="£",
    cash_flow_totals=[
        ("Net cash from/(used in) operating activities", {
            "FY2025": 89261779, "FY2024": -10464980, "FY2023": -12063952,
        }),
        ("Net cash from/(used in) investing activities", {
            "FY2025": -94044573, "FY2024": -5540942, "FY2023": -8527971,
        }),
        ("Net cash from/(used in) financing activities", {
            "FY2025": 9744844, "FY2024": 18093063, "FY2023": 9814533,
        }),
        ("Cash and cash equivalents at end of year/period", {
            "FY2025": 7326998, "FY2024": 2364540, "FY2023": 270150,
        }),
    ],
    cash_flow_unit="£",
    ratios=[
        ("CET1 Ratio", {"FY2025": "112%", "FY2024": "64%", "FY2023": "456%"}),
        ("Tier 1 Ratio", {"FY2025": SDDT_CELL, "FY2024": SDDT_CELL, "FY2023": "456%"}),
        ("Total Capital Ratio", {"FY2025": SDDT_CELL, "FY2024": SDDT_CELL, "FY2023": "456%"}),
        ("Leverage Ratio", {"FY2025": SDDT_CELL, "FY2024": SDDT_CELL, "FY2023": "91%"}),
        ("LCR", {"FY2025": SDDT_CELL, "FY2024": SDDT_CELL, "FY2023": "2,675%"}),
        ("NSFR", {"FY2025": SDDT_CELL, "FY2024": SDDT_CELL, "FY2023": "1,034%"}),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own "
         "source citation for the underlying document/page. Only FY2023 has any Pillar 3 data - no "
         "Pillar 3 report has been published for FY2024 or FY2025 (re-confirmed 2026-09-15 by enumerating "
         "every PDF on griffin.com/reports: six documents, of which one Pillar 3 report, dated 30 Sept 2023). "
         "That absence is a REGULATORY EXEMPTION, not an access gap and not mere non-publication - a "
         "correction, made 2026-09-15, to the previous note here. Griffin Bank Ltd (FRN 970920) holds a "
         "Modification by Consent of Rule 3.1 of the SDDT Regime - General Application Part (waiver ref "
         "A00007614P.pdf, start date 05/03/2024, no end date) on the Bank of England's consolidated register "
         "of waivers and modifications granted to PRA-authorised firms. Rule 3.1 is the Small Domestic Deposit "
         "Taker opt-in, and it removes the Pillar 3 disclosure obligation outright. Griffin's year-end is 30 "
         "September (Companies House 10842931), so FY2024 (30 Sep 2024) and FY2025 (30 Sep 2025) both fall "
         "after that 5 March 2024 start date and are structurally exempt. This does NOT extend back to FY2023: "
         "that period ended 30 September 2023, before the modification, and Griffin duly published a full "
         "Pillar 3 report for it as a 'small and non-complex institution' under Article 433b - a route that "
         "REDUCES disclosure, unlike Rule 3.1 which REMOVES it. The two must not be conflated; see the Pillar "
         "3 sheets' own source note for the full reasoning. Griffin "
         "Bank Ltd (FRN 970920) is still on the Bank of England's List of banks as at 30 September 2026. The "
         "only FY2024/FY2025 regulatory figure disclosed anywhere is the CET1 ratio, in the Annual Report "
         "narrative (64% / 112%). The Bank "
         "has no customer lending at all in any of the 3 published years - Asset Quality is 'Not publicly "
         "disclosed' for this genuine reason (see that sheet's own source note).",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/GRIFFIN BANK FINANCIALS.xlsx")
