import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2026", "FY2025", "FY2024", "FY2023", "FY2022", "FY2021", "FY2020", "FY2019", "FY2018"]
AR26_URL = "https://recognisebank.co.uk/wp-content/uploads/274107-Recognise-Bank-Annual-Report-WEB.pdf"
AR24_URL = "https://recognisebank.co.uk/wp-content/uploads/2024-Annual-Report-Accounts.pdf"
AR23_URL = "https://recognisebank.co.uk/wp-content/uploads/2023/10/230821-Recognise-Bank-2023-Annual-Report-WEB.pdf"
AR22_URL = "https://recognisebank.co.uk/wp-content/uploads/2023/10/2022-Annual-Report-Recognise-Bank-Limited.pdf"
P3_26_URL = "https://recognisebank.co.uk/wp-content/uploads/Pillar-3-disclosure-March-2026-RBL-v1.1-To-BAC-updated_-1-1.pdf"
P3_24_URL = "https://recognisebank.co.uk/wp-content/uploads/Pillar-3-disclosure-March-2024-RBL.pdf"
P3_23_URL = "http://web.archive.org/web/20231210004904/https://www.recognisebank.co.uk/wp-content/uploads/2023/10/Pillar-3-disclosures-March-2023-RBL.pdf"

# Historical years FY2018-FY2021: sourced from Companies House filing history for
# Recognise Bank Limited (co. no. 10603119; filed under its earlier names Echo
# Financial Services Limited / Recognise Financial Services Limited), re-verified
# directly from the filed PDFs (not merely the earlier GLEIF/domain-creation-date
# scan that first flagged FY2017 as a historical-floor signal - see ENTITY_NOTE).
CH21_URL = "https://find-and-update.company-information.service.gov.uk/company/10603119/filing-history/MzMyMTE3NDk3NmFkaXF6a2N4/document?format=pdf&download=0"
CH20_URL = "https://find-and-update.company-information.service.gov.uk/company/10603119/filing-history/MzI4NDMzNTMxOGFkaXF6a2N4/document?format=pdf&download=0"
CH19_URL = "https://find-and-update.company-information.service.gov.uk/company/10603119/filing-history/MzI0MjQ2NzU0OGFkaXF6a2N4/document?format=pdf&download=0"
CH18_URL = "https://find-and-update.company-information.service.gov.uk/company/10603119/filing-history/MzIxODY1MTA1NGFkaXF6a2N4/document?format=pdf&download=0"

ENTITY_NOTE = (
    "ENTITY/BASIS NOTE: Recognise Bank Limited (Companies House 10603119; FRN 849404; LEI "
    "213800ZFTXJC7RV9UQ92) is the matched authorised bank entity. Cash flows are presented on "
    "the Company/standalone basis in £'000 throughout. The 2022-2024 reports also show Group "
    "columns, but the Company column is used consistently here. Recognise's sole remaining "
    "subsidiary, Credit Asset Management Limited (CAML), entered members' voluntary liquidation "
    "on 24 March 2025; the 2025 accounts therefore were not consolidated, and the 2026 report is "
    "standalone. FY2025 is taken from the clean comparative in the 2026 report because the bank's "
    "published 2025 PDF has an extraction/encoding problem; no figure is inferred. Blank cells "
    "mean not publicly disclosed, not zero."
)
HISTORICAL_NOTE = (
    "HISTORICAL DEPTH NOTE (FY2018-FY2021, added per HD-053): the entity's confirmed historical "
    "floor is FY2017 per its Companies House incorporation date (6 Feb 2017, then named Biz "
    "Financial Services Limited); however that date signal is a domain/creation-date scan, not a "
    "read of an actual filed document. Re-verified directly against Companies House filing "
    "history: there is no separate FY2017 accounts filing. The company's FIRST statutory accounts "
    "cover the 14-month period from incorporation (6 Feb 2017) to 31 March 2018 (filed 6 Nov 2018, "
    "as Echo Financial Services Limited) - FY2017 is therefore self-skipped as a distinct year "
    "(there is no document for it to be sourced from; it is already folded into the FY2018 period "
    "shown here). FY2018-FY2020: the company had not yet obtained a UK banking licence (only "
    "Authorised with Restrictions from 10 Nov 2020, full licence Sept 2021) - it held no loan book "
    "and took no deposits in these years, so the Asset Quality sheet, all 11 Pillar 3 key-metric "
    "sheets, and the RWA Breakdown sheet are self-skipped for FY2018-FY2020 (genuinely not "
    "applicable, not merely undisclosed). FY2021: lending began in Nov 2020 and the Asset Quality "
    "sheet is populated; however no standalone Pillar 3 document was published for FY2021 (the "
    "Bank was still under Authorised-with-Restrictions status, not yet fully mobilised) - CET1/"
    "Tier 1/Total Capital and their ratios are sourced instead from a capital-adequacy note in the "
    "FY2021 Annual Report itself (Group basis, no separate Company figure disclosed) and Total "
    "RWAs/Leverage Ratio/LCR/NSFR/MREL Ratio are self-skipped for FY2021 as not disclosed anywhere "
    "in that report. Company-only Income Statements were not separately presented for FY2021 either "
    "(s.408 Companies Act 2006 exemption, once the PFS subsidiary existed) - see PL_SOURCES."
)
CH_SOURCES_NOTE = (
    "Sources for FY2018-FY2021 (Companies House filing history, co. no. 10603119):\n"
    f"FY2021: Annual Report and Financial Statements for the year ended 31 March 2021 (filed 24 Nov "
    f"2021, as Recognise Bank Limited) - {CH21_URL}\n"
    f"FY2020: Annual Report and Financial Statements for the year ended 31 March 2020 (filed 25 Nov "
    f"2020, as Recognise Financial Services Limited) - {CH20_URL}\n"
    f"FY2019: Annual Report and Financial Statements for the year ended 31 March 2019 (filed 23 Aug "
    f"2019, as Recognise Financial Services Limited) - {CH19_URL}\n"
    f"FY2018: Report and Financial Statements for the 14-month period ended 31 March 2018, the "
    f"company's first statutory accounts (filed 6 Nov 2018, as Echo Financial Services Limited, "
    f"formerly Biz Financial Services Limited) - {CH18_URL}\n\n"
    + HISTORICAL_NOTE
)
CASH_SOURCES = (
    "Sources - Recognise Bank Limited Company/standalone cash flows, £'000:\n"
    f"FY2026 & FY2025: Annual Report 2026, printed p.52 - {AR26_URL}\n"
    f"FY2024 & FY2023: Annual Report 2024, printed p.46 (Company statement) - {AR24_URL}\n"
    f"FY2023 & FY2022: Annual Report 2023, printed p.42 (Company statement) - {AR23_URL}\n"
    f"FY2022 & FY2021 comparative: Annual Report 2022, printed p.44 (Company statement) - {AR22_URL}\n"
    f"FY2021: Company Statement of Cash Flows, p.33 of the FY2021 accounts - {CH21_URL}\n"
    f"FY2020 & FY2019: Statement of Cash Flows, p.15 of the FY2020 accounts (incl. FY2019 comparative) - "
    f"{CH20_URL}\n"
    f"FY2018: Statement of Cash Flows, p.9 of the FY2018 (first-period) accounts - {CH18_URL}\n\n"
    + ENTITY_NOTE
    + "\n\n" + CH_SOURCES_NOTE
)
BS_SOURCES = (
    "Sources - Recognise Bank Limited Company/standalone balance sheet, £'000:\n"
    f"FY2026 & FY2025: Annual Report 2026, printed p.50, Balance sheet - {AR26_URL}\n"
    f"FY2024 & FY2023: Annual Report 2024, printed p.42, Company balance sheet - {AR24_URL}\n"
    f"FY2023 & FY2022: Annual Report 2023, printed p.38, Company balance sheet - {AR23_URL}\n"
    f"FY2021: Company Statement of Financial Position, p.29 of the FY2021 accounts - {CH21_URL}\n"
    f"FY2020 & FY2019: Statement of Financial Position, p.13 of the FY2020 accounts (incl. FY2019 "
    f"comparative) - {CH20_URL}\n"
    f"FY2018: Statement of Financial Position, p.7 of the FY2018 (first-period) accounts - {CH18_URL}\n\n"
    + ENTITY_NOTE
    + "\n\nPRESENTATION NOTE: Debt securities and Deferred tax asset only appear as separate lines from FY2025 and "
    "FY2026 respectively (not disclosed pre-FY2025; blank means not applicable/not disclosed, not zero, except "
    "where a report explicitly showed a nil dash, which is recorded as 0 - e.g. Lease liabilities FY2025 and "
    "Borrowings FY2026). Investment in subsidiaries appears only FY2023-FY2024 (Credit Asset Management Limited, "
    "CAML, was a subsidiary until its liquidation in March 2025). Borrowings appears only FY2025 (£503k). Company "
    "balance sheets pre-FY2025 also showed Group columns; the Company column is used consistently, matching the "
    "existing Cash Flow Statement convention.\n\n"
    + CH_SOURCES_NOTE
    + "\n\nFY2018-FY2020 BALANCE SHEET NOTE: pre-licence, the balance sheet is a simple shell (cash, "
    "receivables, PP&E, intangibles from FY2020, and trade payables) with no Loans/Deposits lines - those "
    "rows are blank for FY2018-FY2020, genuinely not applicable rather than undisclosed. Share capital for "
    "FY2018-FY2020 combines Ordinary and Deferred share classes (no separate Share premium account existed "
    "until FY2021); see the Statement of Changes in Equity sheet for the full roll-forward. FY2021 introduces "
    "a new 'Loans and advances to subsidiary' asset row (the Bank lent TO its PFS subsidiary that year); "
    "this reverses direction from FY2022 onward, where 'Loans and advances from subsidiary' is a liability "
    "(the subsidiary lending to the Bank) - a genuine change in the intercompany funding relationship, not an "
    "error.\n\n"
    "DEBT SECURITIES: in every year disclosed, the balance is 100% UK Government Treasury Bills and Gilts - "
    "there is no supranational/corporate/other-issuer component to split out, and no note-level split by "
    "issuer type is possible or needed. The measurement basis, however, genuinely changed over time: FY2021 "
    "Note 13 'Debt Securities' (Company Statement of Financial Position, p.29, and the Fair Value note, p.47-"
    "48 of the FY2021 accounts - " + CH21_URL + ") states the balance is 'Debt securities at FVOCI' (fair "
    "value through other comprehensive income, Level 1 fair value hierarchy), consistent with the FY2021 "
    "accounting-policy note 2.7 (p.36) that the Bank's debt securities were held under a Hold-to-Collect-and-"
    "Sell business model. By FY2026, Note 17 'Debt securities' (Annual Report 2026, printed p.74 - " + AR26_URL + ") "
    "instead states 'UK Government Treasury Bills and Gilts - at amortised cost', consistent with the FY2026 "
    "accounting-policy note 2.7.2(b) (p.56) that debt securities are now held under a Hold-to-Collect business "
    "model. No note discloses the exact year this reclassification took effect (no debt securities were held "
    "at all in FY2022-FY2024); the FY2025 balance in Note 17 is disclosed only under the amortised-cost "
    "heading, so the same balance is shown there. Because the entire balance is one issuer/bucket in every "
    "year, the row is labelled by issuer type only, not renamed to a 'Total ...' line (no sub-rows apply)."
)
PL_SOURCES = (
    "Sources - Recognise Bank Limited Statement of Comprehensive Income, £'000:\n"
    f"FY2026 & FY2025: Annual Report 2026, printed p.49, Statement of comprehensive income (Company/standalone "
    f"basis) - {AR26_URL}\n"
    f"FY2024 & FY2023: Annual Report 2024, printed p.40, Consolidated statement of comprehensive income - {AR24_URL}\n"
    f"FY2023 & FY2022: Annual Report 2023, printed p.36, Consolidated statement of comprehensive income - {AR23_URL}\n"
    f"FY2021: Consolidated Income Statement and Statement of Comprehensive Income, p.27, plus operating-expense "
    f"breakdown note 7, p.49, of the FY2021 accounts - {CH21_URL}\n"
    f"FY2020 & FY2019: Income Statement and Statement of Comprehensive Income, p.12 of the FY2020 accounts "
    f"(incl. FY2019 comparative) - {CH20_URL}\n"
    f"FY2018: Statement of Comprehensive Income, p.6 of the FY2018 (first-period) accounts - {CH18_URL}\n\n"
    + ENTITY_NOTE
    + "\n\nPRESENTATION NOTE: Recognise Bank took advantage of s.408 Companies Act 2006 and did not present a "
    "standalone Company income statement for FY2021-FY2024 (only the Group/consolidated income statement was "
    "published in those years, once the PFS/CAML subsidiary existed); the detail rows above for FY2021-FY2024 are "
    "therefore Group-level, not Company-level. The 'Profit/(loss) for the year' TOTAL row uses the Company-level "
    "bottom line for all years, consistent with the Balance Sheet, Cash Flow Statement, and Statement of Changes "
    "in Equity elsewhere in this workbook (per the Company balance sheet's / Company statement of changes in "
    "equity's own disclosure of the Company's loss after tax). For FY2021-FY2024 this Company bottom line does "
    "not foot exactly from the Group-level 'Profit/(loss) before tax' row above it (differs by roughly £160k-"
    "£370k) - a genuine, documented Group-vs-Company basis difference, not a calculation error. Restructuring "
    "costs only appear as a separate line from FY2025. FY2018-FY2020 predate the PFS subsidiary and any banking "
    "activity: there was no consolidation issue (a single, non-trading applicant company) and no interest income/"
    "expense, fee income, or impairment lines - just administrative expenses while the banking-licence application "
    "was in progress."
)
EQ_SOURCES = (
    "Sources - Recognise Bank Limited Company Statement of Changes in Equity, £'000:\n"
    f"FY2025-FY2026 movements & FY2024 closing balance: Annual Report 2026, printed p.51, Statement of changes in "
    f"equity - {AR26_URL}\n"
    f"FY2023-FY2024 movements: Annual Report 2024, printed p.44, Company statement of changes in equity - {AR24_URL}\n"
    f"FY2022-FY2023 movements & FY2021 opening balance: Annual Report 2023, printed p.40, Company statement of "
    f"changes in equity - {AR23_URL}\n"
    f"FY2021 movements: Company Statement of Changes in Equity, p.31 of the FY2021 accounts - {CH21_URL}\n"
    f"FY2020 movements & FY2019 movements: Statement of Changes in Equity, p.14 of the FY2020 accounts (incl. "
    f"FY2019 comparative) - {CH20_URL}\n"
    f"FY2018 movements (period from incorporation): Statement of Changes in Equity, p.8 of the FY2018 (first-"
    f"period) accounts - {CH18_URL}\n\n"
    + ENTITY_NOTE
    + "\n\nEvery year ties almost exactly to both the next year's opening balance and that year's own Company "
    "balance sheet Total equity - the handful of single-£'000-unit gaps that appear (e.g. FY2018, FY2021) are "
    "independent-rounding artifacts of converting whole-pound source figures to £'000 at different levels of "
    "aggregation, not undocumented plug rows. FY2018-FY2020 combine Ordinary and Deferred share capital into the "
    "single 'Share capital' column (no separate Share premium account existed yet); FY2021 is the first year with "
    "a genuine Share premium account, following an in-year reclassification of £8,145,000 of Deferred shares to "
    "Ordinary share capital (a net-nil internal reclass, not shown as a separate row here).\n\n" + CH_SOURCES_NOTE
)
AQ_SOURCES = (
    "Sources - Recognise Bank Limited Company loan book by IFRS 9 stage, £'000:\n"
    f"FY2026 & FY2025: Annual Report 2026, printed p.67 (portfolio analysis by credit risk grade) and p.74 (note "
    f"18, loan movements) - {AR26_URL}\n"
    f"FY2024 & FY2023: Annual Report 2024, printed p.57 (Company portfolio analysis) - {AR24_URL}\n"
    f"FY2023 & FY2022: Annual Report 2023, printed p.62 (Company note 17, loan movements, incl. the FY2022 Group-"
    f"and-Company combined comparative) - {AR23_URL}\n\n"
    + ENTITY_NOTE
    + "\n\nAll years' Net loans and advances to customers ties exactly to the Balance Sheet's own Loans and "
    "advances to customers line. Stage 2 and Stage 3 were both nil in FY2021, FY2022 and FY2023 (100% Stage 1) - "
    "a young, still-small loan book at that point, not an omission. Stage 3 (NPL) and coverage ratios are left "
    "blank for FY2021/FY2022/FY2023 as not meaningful (zero Stage 3 exposure), not because they were undisclosed.\n\n"
    "FY2021: Company loan book (net of ECL), note 14, p.52 of the FY2021 accounts - " + CH21_URL + ". FY2018-"
    "FY2020 have no Asset Quality sheet entries at all (self-skipped): Recognise had no banking licence and no "
    "loan book in those years - see HISTORICAL_NOTE in the Balance Sheet source text."
)
RWA_SOURCES = (
    "Sources - Recognise Bank Limited UK OV1 Overview of RWAs, £'000:\n"
    f"FY2026 & FY2025: Pillar 3 Disclosure March 2026, Table 2 UK OV1, printed p.4 - {P3_26_URL}\n"
    f"FY2024 & FY2023: Pillar 3 Disclosure March 2024, Table 2 UK OV1, printed p.4 - {P3_24_URL}\n"
    f"FY2023 & FY2022: Pillar 3 Disclosure March 2023, Table 2 UK OV1, printed p.4 (Wayback Machine archive, "
    f"capture 2023-12-10; not linked from the bank's current site) - {P3_23_URL}\n\n"
    "Counterparty credit risk (CCR) is only disclosed as a separate category from FY2025 (Recognise did not have "
    "material CCR exposure, or did not break it out, in FY2022-FY2024's OV1 tables - blank, not zero, for those "
    "years). All years shown tie exactly to the Total risk-weighted exposure amount already on file in the "
    "CET1/Total RWAs metric sheets. FY2018-FY2021 have no RWA Breakdown entries (self-skipped): no standalone "
    "Pillar 3 disclosure (with a UK OV1 table) was published for any of those years - Recognise had no banking "
    "licence at all until Nov 2020 (Authorised with Restrictions) and had not yet reached full mobilisation by "
    "its FY2021 year-end (31 March 2021); see HISTORICAL_NOTE in the Balance Sheet source text."
)
P3_SOURCES = (
    f"Source - Recognise Bank Limited Pillar 3 Disclosure 2026, Table 1 UK KM1, printed p.3 "
    f"(Mar-26 through Mar-22 comparatives) - {P3_26_URL}\n"
    "The 2026 KM1 table supplies all five most recent year-ends on a bank/entity basis."
)
# FY2018-FY2020 are structurally pre-authorisation, not undisclosed - see
# PRE_AUTHORISATION_NOTE. Injected as explicit "Not applicable" defaults by the local
# metric() wrapper, following the build_vida.py / build_afin_bank.py convention, so an
# empty cell is never mistaken for an unresearched gap.
PRE_AUTHORISATION_YEARS = ["FY2020", "FY2019", "FY2018"]

PRE_AUTHORISATION_NOTE = (
    "FY2018-FY2020 READ 'Not applicable', NOT BLANK AND NOT 'Not disclosed' (set 2026-09-15). Recognise Bank Limited held no PRA "
    "authorisation of any kind at the 31 March 2018, 2019 or 2020 year-ends, so no Pillar 3 disclosure obligation existed and there is no "
    "capital, RWA, leverage or liquidity figure that could exist to be found. The entity's own FY2022 Annual Report states the timeline in "
    "its own words - 'After receiving its Authorisation with Restrictions (AwR) in November 2020, Recognise Bank became fully authorised in "
    "September 2021 and was able to accept savings deposits' (PDF p.23, going-concern note) - and note 1 repeats it: the Bank 'became fully "
    "authorised in September 2021 when restrictions set by the PRA were lifted after all mobilisation conditions were met' (PDF p.45). "
    "Source: Recognise Bank Limited Annual Report and Financial Statements 2022 - " + AR22_URL + "\n"
    "FY2021 IS DIFFERENT AND IS DELIBERATELY NOT MARKED 'Not applicable'. Authorisation with Restrictions was already in force at the "
    "31 March 2021 year-end (granted November 2020), so the Bank was a PRA-authorised firm for that whole year-end even though it was still "
    "in mobilisation. Its FY2021 blanks (Total RWAs, Leverage Ratio, LCR, NSFR, MREL) are therefore genuine non-disclosure, not structural "
    "inapplicability, and stay distinguishable from the FY2018-FY2020 cells above."
)

ENUMERATED_NEGATIVE_NOTE = (
    "ENUMERATED NEGATIVE for FY2018-FY2021 (re-verified 2026-09-15). The bank's own investor index at "
    "https://recognisebank.co.uk/investors/ was fetched and its document list read in full. It offers Pillar 3 Disclosures for 2023, 2024, "
    "2025 and 2026 only, and Annual Report & Accounts for 2022, 2023, 2024, 2025 and 2026 only. There is no FY2018, FY2019, FY2020 or FY2021 "
    "Pillar 3 document listed, linked or hosted - the four PDF hrefs on that page for Pillar 3 are the March 2023, March 2024, March 2025 and "
    "March 2026 editions and nothing else. This is enumeration of the publisher's own index, not a failed URL guess, so it proves absence "
    "rather than merely failing to find. The pre-2023 annual reports used in this workbook for FY2018-FY2021 come from Companies House "
    "instead (see CH_SOURCES_NOTE); they are statutory accounts, not Pillar 3 disclosures.\n"
    "The March 2026 Pillar 3 was also downloaded and read in full on 2026-09-15 to check for backfill: its UK KM1 (Table 1, printed p.4) "
    "carries five columns, Mar-26 through Mar-22, and every one of those values already matches what is recorded in this workbook. It reaches "
    "no further back than Mar-22 and contains no MREL row, so it yields nothing new for FY2018-FY2021."
)

P3_21_SOURCES = (
    f"Source - Recognise Bank Limited FY2021 Annual Report, Strategic Report, 'Capital' section capital-"
    f"adequacy note, printed p.43 - {CH21_URL}\n"
    "No standalone Pillar 3 document was published for FY2021 (Recognise was Authorised with Restrictions, not "
    "yet fully mobilised, at its 31 March 2021 year-end); this note is a Group-basis capital-adequacy disclosure "
    "in the Annual Report itself, not a UK KM1 table, and only CET1/Tier 1/Total Capital and their ratios were "
    "given (Total RWAs, Leverage Ratio, LCR, NSFR and MREL Ratio were not disclosed anywhere in the FY2021 "
    "report - self-skipped for FY2021). The note states CET1 Capital after deductions = Own Funds = "
    "£26,395,924, and CET1 Capital Ratio = Total Capital Ratio = 78.92%, implying no AT1/T2 instruments beyond "
    "CET1 at that stage (Tier 1 Capital, Tier 1 Ratio, and Total Capital/Total Capital Ratio are therefore the "
    "same figures)."
)

bw = BankWorkbook(bank_name="Recognise Bank Limited", years=YEARS, header_color="51158C")

BS_ROWS = [
        ("SECTION", "Assets", {}),
        ("DATA", "Cash and cash equivalents", {"FY2026": 160949, "FY2025": 238732, "FY2024": 164292, "FY2023": 138354, "FY2022": 36233, "FY2021": 11225, "FY2020": 533, "FY2019": 511, "FY2018": 874}),
        ("DATA", "Debt securities - UK government (gilts and Treasury bills)", {"FY2026": 29999, "FY2025": 9932, "FY2021": 6500}),
        ("DATA", "Investment in subsidiaries", {"FY2024": 349, "FY2023": 3349, "FY2021": 0}),
        ("DATA", "Loans and advances to customers", {"FY2026": 461863, "FY2025": 305596, "FY2024": 302710, "FY2023": 121441, "FY2022": 98941, "FY2021": 6485}),
        ("DATA", "Loans and advances to subsidiary", {"FY2021": 4572}),
        ("DATA", "Other assets", {"FY2026": 1603, "FY2025": 1418, "FY2024": 970, "FY2023": 3221, "FY2022": 516, "FY2021": 240, "FY2020": 123, "FY2019": 0, "FY2018": 29}),
        ("DATA", "Property, plant and equipment", {"FY2026": 89, "FY2025": 62, "FY2024": 165, "FY2023": 230, "FY2022": 70, "FY2021": 57, "FY2020": 39, "FY2019": 8, "FY2018": 4}),
        ("DATA", "Intangible assets", {"FY2026": 980, "FY2025": 1813, "FY2024": 1832, "FY2023": 1095, "FY2022": 980, "FY2021": 1028, "FY2020": 544}),
        ("DATA", "Right-of-use assets", {"FY2026": 307, "FY2025": 3, "FY2024": 171, "FY2023": 372, "FY2022": 100, "FY2021": 25}),
        ("DATA", "Deferred tax asset", {"FY2026": 7060}),
        ("TOTAL", "Total assets", {"FY2026": 662850, "FY2025": 557556, "FY2024": 470489, "FY2023": 268062, "FY2022": 136840, "FY2021": 30132, "FY2020": 1240, "FY2019": 519, "FY2018": 906}),
        ("SECTION", "Liabilities", {}),
        ("DATA", "Deposits from customers", {"FY2026": 575545, "FY2025": 484311, "FY2024": 411667, "FY2023": 200251, "FY2022": 94994, "FY2021": 2}),
        ("DATA", "Loans and advances from subsidiary", {"FY2024": 517, "FY2023": 5000, "FY2022": 468}),
        ("DATA", "Borrowings", {"FY2026": 0, "FY2025": 503}),
        ("DATA", "Lease liabilities", {"FY2026": 293, "FY2025": 0, "FY2024": 188, "FY2023": 413, "FY2022": 103, "FY2021": 25}),
        ("DATA", "Other liabilities", {"FY2026": 4355, "FY2025": 3941, "FY2024": 3985, "FY2023": 4097, "FY2022": 3352, "FY2021": 2859, "FY2020": 824, "FY2019": 297, "FY2018": 93}),
        ("TOTAL", "Total liabilities", {"FY2026": 580193, "FY2025": 488755, "FY2024": 416357, "FY2023": 209761, "FY2022": 98917, "FY2021": 2887, "FY2020": 824, "FY2019": 297, "FY2018": 93}),
        ("SECTION", "Equity", {}),
        ("DATA", "Share capital", {"FY2026": 87531, "FY2025": 82531, "FY2024": 62530, "FY2023": 57530, "FY2022": 30578, "FY2021": 21210, "FY2020": 5555, "FY2019": 2010, "FY2018": 1010}),
        ("DATA", "Share premium", {"FY2026": 38722, "FY2025": 38722, "FY2024": 38722, "FY2023": 38722, "FY2022": 32513, "FY2021": 18931}),
        ("DATA", "Other reserves", {"FY2026": 90, "FY2025": 90, "FY2024": 90, "FY2023": 0, "FY2022": 226, "FY2021": 55}),
        ("DATA", "Accumulated losses", {"FY2026": -43686, "FY2025": -52542, "FY2024": -47210, "FY2023": -37951, "FY2022": -25394, "FY2021": -12950, "FY2020": -5139, "FY2019": -1788, "FY2018": -196}),
        ("TOTAL", "Total equity", {"FY2026": 82657, "FY2025": 68801, "FY2024": 54132, "FY2023": 58301, "FY2022": 37923, "FY2021": 27246, "FY2020": 416, "FY2019": 222, "FY2018": 813}),
        ("TOTAL", "Total liabilities and equity", {"FY2026": 662850, "FY2025": 557556, "FY2024": 470489, "FY2023": 268062, "FY2022": 136840, "FY2021": 30132, "FY2020": 1240, "FY2019": 519, "FY2018": 906}),
]
bw.add_balance_sheet_sheet(
    title="Recognise Bank Limited - Company Balance Sheet",
    subtitle="Company/standalone basis, £'000; FY2018-FY2026 (31 March year-end; FY2018 is a 14-month first period from incorporation).",
    rows=BS_ROWS,
    sources_text=BS_SOURCES,
    first_col_width=60,
    source_height=330,
    unit_suffix=" (£'000)",
)

PL_ROWS = [
        ("SECTION", "Income", {}),
        ("DATA", "Interest income", {"FY2026": 42754, "FY2025": 36294, "FY2024": 25554, "FY2023": 9206, "FY2022": 2380, "FY2021": 439}),
        ("DATA", "Interest expense", {"FY2026": -22398, "FY2025": -20832, "FY2024": -13153, "FY2023": -3007, "FY2022": -824, "FY2021": -75}),
        ("TOTAL", "Net interest income", {"FY2026": 20356, "FY2025": 15462, "FY2024": 12401, "FY2023": 6199, "FY2022": 1556, "FY2021": 364}),
        ("DATA", "Fee and commission income", {"FY2026": 557, "FY2025": 412, "FY2024": 408, "FY2023": 175, "FY2022": 16, "FY2021": 0}),
        ("DATA", "Fee and commission expense", {"FY2026": -34, "FY2025": -61, "FY2024": -102, "FY2023": -7, "FY2022": -16, "FY2021": -4}),
        ("TOTAL", "Net operating income", {"FY2026": 20879, "FY2025": 15813, "FY2024": 12707, "FY2023": 6367, "FY2022": 1556, "FY2021": 360}),
        ("DATA", "Other income", {"FY2026": 432, "FY2025": 1420, "FY2024": 777, "FY2023": 1, "FY2022": 0}),
        ("SECTION", "Operating expenses", {}),
        ("DATA", "Staff costs", {"FY2026": -10333, "FY2025": -10346, "FY2024": -10453, "FY2023": -11914, "FY2022": -8405, "FY2021": -5373}),
        ("DATA", "Other operating expenses", {"FY2026": -7759, "FY2025": -6884, "FY2024": -8277, "FY2023": -6802, "FY2022": -4831, "FY2021": -2565, "FY2020": -3351, "FY2019": -1591, "FY2018": -196}),
        ("DATA", "Restructuring costs", {"FY2026": -910, "FY2025": -2325}),
        ("DATA", "Depreciation and amortisation", {"FY2026": -559, "FY2025": -699, "FY2024": -635, "FY2023": -789, "FY2022": -307, "FY2021": -68}),
        ("DATA", "Net impairment gain/(loss) on financial assets", {"FY2026": 46, "FY2025": -2311, "FY2024": -3126, "FY2023": 162, "FY2022": -149, "FY2021": -5}),
        ("TOTAL", "Total operating expense", {"FY2026": -19515, "FY2025": -22565, "FY2024": -22491, "FY2023": -19343, "FY2022": -13692, "FY2021": -8006, "FY2020": -3351, "FY2019": -1591, "FY2018": -196}),
        ("TOTAL", "Profit/(loss) before tax", {"FY2026": 1796, "FY2025": -5332, "FY2024": -9007, "FY2023": -12975, "FY2022": -12136, "FY2021": -7651, "FY2020": -3351, "FY2019": -1591, "FY2018": -196}),
        ("DATA", "Taxation credit/(expense) for the year", {"FY2026": 7060, "FY2025": 0, "FY2024": 0, "FY2023": 0, "FY2022": 0, "FY2021": 0, "FY2020": 0, "FY2019": 0, "FY2018": 0}),
        ("TOTAL", "Profit/(loss) for the year", {"FY2026": 8856, "FY2025": -5332, "FY2024": -9259, "FY2023": -12783, "FY2022": -12444, "FY2021": -7811, "FY2020": -3351, "FY2019": -1591, "FY2018": -196}),
]
bw.add_income_statement_sheet(
    title="Recognise Bank Limited - Statement of Comprehensive Income",
    subtitle="FY2025-FY2026 Company/standalone basis; FY2021-FY2024 detail rows Group-level (see sources); FY2018-FY2020 pre-banking-licence Company basis, £'000.",
    rows=PL_ROWS,
    sources_text=PL_SOURCES,
    first_col_width=62,
    source_height=280,
    unit_suffix=" (£'000)",
)

EQ_ROWS = [
        ("TOTAL", "Balance at 6 February 2017 (incorporation)", (0, 0, 0, 0, 0)),
        ("DATA", "Issue of ordinary and deferred shares (FY2018)", (1010, None, None, None, 1010)),
        ("TOTAL", "Total comprehensive loss for the period (FY2018)", (None, None, -196, None, -196)),
        ("TOTAL", "Balance at 31 March 2018", (1010, 0, -196, 0, 813)),
        ("TOTAL", "Total comprehensive loss for the year (FY2019)", (None, None, -1591, None, -1591)),
        ("DATA", "Issue of deferred shares (FY2019)", (1000, None, None, None, 1000)),
        ("TOTAL", "Balance at 31 March 2019", (2010, 0, -1788, 0, 222)),
        ("TOTAL", "Total comprehensive loss for the year (FY2020)", (None, None, -3351, None, -3351)),
        ("DATA", "Issue of deferred shares (FY2020)", (3545, None, None, None, 3545)),
        ("TOTAL", "Balance at 31 March 2020", (5555, 0, -5139, 0, 416)),
        ("DATA", "Issue of deferred shares (FY2021)", (2600, None, None, None, 2600)),
        ("DATA", "Issue of ordinary shares and share premium (FY2021)", (13056, 18931, None, None, 31987)),
        ("TOTAL", "Total comprehensive loss for the year (FY2021)", (None, None, -7811, None, -7811)),
        ("DATA", "Share-based payments and other reserves movement (FY2021)", (None, None, None, 55, 55)),
        ("TOTAL", "Balance at 31 March 2021", (21210, 18931, -12950, 55, 27246)),
        ("DATA", "Issue of ordinary shares (FY2022)", (9368, 13582, None, None, 22950)),
        ("DATA", "Share-based payments (FY2022)", (None, None, None, 171, 171)),
        ("TOTAL", "Total comprehensive loss for the year (FY2022)", (None, None, -12444, None, -12444)),
        ("TOTAL", "Balance at 31 March 2022", (30578, 32513, -25394, 226, 37923)),
        ("TOTAL", "Total comprehensive loss for the year (FY2023)", (None, None, -12783, None, -12783)),
        ("DATA", "Transfer from Other reserves (FY2023)", (None, None, 226, -226, 0)),
        ("DATA", "Issue of ordinary shares (FY2023)", (26952, 6209, None, None, 33161)),
        ("TOTAL", "Balance at 31 March 2023", (57530, 38722, -37951, 0, 58301)),
        ("TOTAL", "Total comprehensive loss for the year (FY2024)", (None, None, -9259, None, -9259)),
        ("DATA", "Share-based payments (FY2024)", (None, None, None, 90, 90)),
        ("DATA", "Issue of ordinary shares (FY2024)", (5000, None, None, None, 5000)),
        ("TOTAL", "Balance at 31 March 2024", (62530, 38722, -47210, 90, 54132)),
        ("TOTAL", "Total comprehensive loss for the year (FY2025)", (None, None, -5332, None, -5332)),
        ("DATA", "Issue of ordinary shares (FY2025)", (20001, None, None, None, 20001)),
        ("TOTAL", "Balance at 31 March 2025", (82531, 38722, -52542, 90, 68801)),
        ("TOTAL", "Total comprehensive income for the year (FY2026)", (None, None, 8856, None, 8856)),
        ("DATA", "Issue of ordinary shares (FY2026)", (5000, None, None, None, 5000)),
        ("TOTAL", "Balance at 31 March 2026", (87531, 38722, -43686, 90, 82657)),
]
bw.add_equity_changes_sheet(
    title="Recognise Bank Limited - Company Statement of Changes in Equity",
    subtitle="Company/standalone basis, £'000; FY2018-FY2026 (31 March year-end; FY2018 from incorporation), read chronologically.",
    headers=["Share capital", "Share premium", "Accumulated losses", "Other reserves", "Total equity"],
    rows=EQ_ROWS,
    sources_text=EQ_SOURCES,
    first_col_width=46,
    source_height=220,
)

rows = [
    ("SECTION", "Cash flow from operating activities", {}),
    ("DATA", "Profit/(loss) for the year", {"FY2026": 8856, "FY2025": -5332, "FY2024": -9259, "FY2023": -12783, "FY2022": -12444, "FY2021": -7811, "FY2020": -3351, "FY2019": -1591, "FY2018": -196}),
    ("DATA", "Depreciation and amortisation", {"FY2026": 559, "FY2025": 699, "FY2024": 635, "FY2023": 789, "FY2022": 305, "FY2021": 142, "FY2020": 12, "FY2019": 3, "FY2018": 0}),
    ("DATA", "Intangible assets impairment", {"FY2026": 928}),
    ("DATA", "Recognition of deferred tax asset", {"FY2026": -7060}),
    ("DATA", "Interest earned during the year", {"FY2026": -42754, "FY2025": -36294, "FY2024": -25487, "FY2023": -9112, "FY2022": -2136, "FY2021": -186}),
    ("DATA", "Interest expense during the year", {"FY2026": 22398, "FY2025": 20832, "FY2024": 13153, "FY2023": 2970, "FY2022": 803, "FY2021": 28}),
    ("DATA", "Interest expense on leases", {"FY2026": 5, "FY2025": 10, "FY2024": 22, "FY2023": 29}),
    ("DATA", "Impairment (gain)/loss", {"FY2026": -46, "FY2025": 2311, "FY2024": 3339, "FY2023": 76, "FY2022": 148, "FY2021": 5}),
    ("DATA", "Share-based incentive plan", {"FY2022": 171, "FY2021": 55}),
    ("DATA", "Dividend income from CAML", {"FY2025": -400, "FY2024": 0, "FY2023": -468}),
    ("DATA", "Other income", {"FY2026": -431}),
    ("DATA", "Interest received", {"FY2026": 41682, "FY2025": 36170, "FY2024": 24429, "FY2023": 9210, "FY2022": 3608, "FY2021": 43}),
    ("DATA", "Interest paid", {"FY2026": -11971, "FY2025": -11997, "FY2024": -4824, "FY2023": -2245, "FY2022": -457, "FY2021": 0}),
    ("DATA", "Increase in debt securities", {"FY2026": -19928, "FY2025": -9656, "FY2021": -6500}),
    ("DATA", "Decrease/(increase) in debt securities", {"FY2022": 6500}),
    ("DATA", "Increase in loans and advances", {"FY2026": -155239, "FY2025": -5307, "FY2024": -183505, "FY2023": -22804, "FY2022": -93780, "FY2021": -11269}),
    ("DATA", "Increase in deposits from customers", {"FY2026": 80807, "FY2025": 63808, "FY2024": 203087, "FY2023": 104533, "FY2022": 94646, "FY2021": 2}),
    ("DATA", "Increase/(decrease) in other assets", {"FY2026": -271, "FY2025": -78, "FY2024": -77, "FY2023": -248, "FY2022": -276}),
    ("DATA", "Increase/(decrease) in other liabilities", {"FY2026": 368, "FY2025": -60, "FY2024": -22, "FY2023": 745, "FY2022": 492}),
    ("DATA", "(Increase)/decrease in trade and other receivables", {"FY2021": 69, "FY2020": -110, "FY2019": 28, "FY2018": -29}),
    ("DATA", "Increase/(decrease) in trade and other payables", {"FY2021": 2172, "FY2020": 527, "FY2019": 204, "FY2018": 70}),
    ("DATA", "Amount advanced for rental property", {"FY2020": -12}),
    ("TOTAL", "Net cash (used in)/generated from operating activities", {"FY2026": -82097, "FY2025": 54706, "FY2024": 21491, "FY2023": 70692, "FY2022": -2420, "FY2021": -23251, "FY2020": -2935, "FY2019": -1356, "FY2018": -155}),
    ("SECTION", "Cash flow from investing activities", {}),
    ("DATA", "Purchase of property, plant and equipment", {"FY2026": -90, "FY2025": -7, "FY2024": -52, "FY2023": -259, "FY2022": -53, "FY2021": -41, "FY2020": -43, "FY2019": -7, "FY2018": -4}),
    ("DATA", "Disposal of property, plant and equipment", {"FY2022": 1, "FY2020": 1}),
    ("DATA", "Distribution/dividend received from CAML", {"FY2026": 11, "FY2025": 60}),
    ("DATA", "Surplus funds sent from CAML", {"FY2025": 280, "FY2024": 800, "FY2023": 1000}),
    ("DATA", "Loans repaid by group companies", {"FY2022": 5017}),
    ("DATA", "Loans advanced to group companies", {"FY2022": -271}),
    ("DATA", "Purchase of intangible assets", {"FY2026": -562, "FY2025": -402, "FY2024": -1054, "FY2023": -571, "FY2022": -156, "FY2021": -535, "FY2020": -545}),
    ("DATA", "Investment in subsidiary", {"FY2021": 0}),
    ("TOTAL", "Net cash (used in)/generated from investing activities", {"FY2026": -641, "FY2025": -69, "FY2024": -306, "FY2023": 170, "FY2022": 4538, "FY2021": -576, "FY2020": -588, "FY2019": -7, "FY2018": -4}),
    ("SECTION", "Cash flow from financing activities", {}),
    ("DATA", "Interest paid on customer deposits", {"FY2022": 6}),
    ("DATA", "Finance lease payments", {"FY2026": -45, "FY2025": -198, "FY2024": -247, "FY2023": -225, "FY2022": -66, "FY2021": -68}),
    ("DATA", "Gross proceeds from the issue of ordinary shares", {"FY2026": 5000, "FY2025": 20001, "FY2024": 5000, "FY2023": 31504, "FY2022": 22950, "FY2021": 34587, "FY2018": 10}),
    ("DATA", "Costs of share issue", {"FY2023": -20}),
    ("DATA", "Proceeds from the issue of deferred shares", {"FY2020": 3545, "FY2019": 1000, "FY2018": 1000}),
    ("DATA", "Amount advanced by director", {"FY2018": 23}),
    ("TOTAL", "Net cash generated from financing activities", {"FY2026": 4955, "FY2025": 19803, "FY2024": 4753, "FY2023": 31259, "FY2022": 22890, "FY2021": 34519, "FY2020": 3545, "FY2019": 1000, "FY2018": 1033}),
    ("TOTAL", "Net (decrease)/increase in cash and cash equivalents", {"FY2026": -77783, "FY2025": 74440, "FY2024": 25938, "FY2023": 102121, "FY2022": 25008, "FY2021": 10692, "FY2020": 22, "FY2019": -363, "FY2018": 874}),
    ("DATA", "Cash and cash equivalents brought forward", {"FY2026": 238732, "FY2025": 164292, "FY2024": 138354, "FY2023": 36233, "FY2022": 11225, "FY2021": 533, "FY2020": 511, "FY2019": 874, "FY2018": 0}),
    ("TOTAL", "Cash and cash equivalents at end of year", {"FY2026": 160949, "FY2025": 238732, "FY2024": 164292, "FY2023": 138354, "FY2022": 36233, "FY2021": 11225, "FY2020": 533, "FY2019": 511, "FY2018": 874}),
]
bw.add_cash_flow_sheet(title="Recognise Bank Limited - Company Cash Flow Statement", subtitle="Company/standalone basis, £'000; FY2018-FY2026 (31 March year-end; FY2018 is a 14-month first period from incorporation).", rows=rows, sources_text=CASH_SOURCES, first_col_width=66, source_height=230, unit_suffix=" (£'000)")

bw.add_asset_quality_sheet(
    title="Recognise Bank Limited - Asset Quality",
    subtitle="Company/standalone basis, loan book by IFRS 9 stage, £'000; FY2021-FY2026 (31 March year-end). No loan book existed pre-FY2021 (self-skipped).",
    rows=[
        ("SECTION", "Gross loans and advances by IFRS 9 stage", {}),
        ("DATA", "Stage 1 (12-month ECL)", {"FY2026": 416693, "FY2025": 284884, "FY2024": 284104, "FY2023": 121660, "FY2022": 99094, "FY2021": 6490}),
        ("DATA", "Stage 2 (lifetime ECL, not credit-impaired)", {"FY2026": 23895, "FY2025": 15458, "FY2024": 17405, "FY2023": 0, "FY2022": 0, "FY2021": 0}),
        ("DATA", "Stage 3 (credit-impaired)", {"FY2026": 25835, "FY2025": 11094, "FY2024": 4748, "FY2023": 0, "FY2022": 0, "FY2021": 0}),
        ("TOTAL", "Gross loans and advances to customers", {"FY2026": 466423, "FY2025": 311436, "FY2024": 306257, "FY2023": 121660, "FY2022": 99094, "FY2021": 6490}),
        ("SECTION", "Allowances for expected credit losses (ECL)", {}),
        ("DATA", "Stage 1 allowance", {"FY2026": -357, "FY2025": -526, "FY2024": -335, "FY2023": -219, "FY2022": -153, "FY2021": -5}),
        ("DATA", "Stage 2 allowance", {"FY2026": -29, "FY2025": -265, "FY2024": -15, "FY2023": 0, "FY2022": 0, "FY2021": 0}),
        ("DATA", "Stage 3 allowance", {"FY2026": -4174, "FY2025": -5049, "FY2024": -3197, "FY2023": 0, "FY2022": 0, "FY2021": 0}),
        ("TOTAL", "Total allowances for ECLs", {"FY2026": -4560, "FY2025": -5840, "FY2024": -3547, "FY2023": -219, "FY2022": -153, "FY2021": -5}),
        ("TOTAL", "Net loans and advances to customers", {"FY2026": 461863, "FY2025": 305596, "FY2024": 302710, "FY2023": 121441, "FY2022": 98941, "FY2021": 6485}),
        ("SECTION", "Asset quality ratios", {}),
        ("DATA", "Stage 3 (NPL) ratio, gross", {"FY2026": "5.54%", "FY2025": "3.56%", "FY2024": "1.55%", "FY2023": "0.00%", "FY2022": "0.00%", "FY2021": "0.00%"}),
        ("DATA", "Stage 3 coverage ratio (Stage 3 ECL / Stage 3 gross)", {"FY2026": "16.16%", "FY2025": "45.51%", "FY2024": "67.35%"}),
    ],
    sources_text=AQ_SOURCES,
    first_col_width=58,
    source_height=230,
    unit_suffix=" (£'000)",
)

def metric(name, unit, data, note=None, sources=None):
    # Pre-authorisation years are written as an explicit "Not applicable" default and
    # only overridden if a real figure exists for them (none does, by construction).
    rows_data = [
        (label, {**{y: "Not applicable" for y in PRE_AUTHORISATION_YEARS}, **{k: v for k, v in values.items() if v is not None}})
        for label, values in data
    ]
    full_note = PRE_AUTHORISATION_NOTE + "\n\n" + ENUMERATED_NEGATIVE_NOTE
    if note:
        full_note = note + "\n\n" + full_note
    bw.add_metric_sheet(name, unit, rows_data, sources or P3_SOURCES, note=full_note, first_col_width=54, source_height=200)

km1 = {
    "FY2026": (74617, 356376, "20.9%", 509006, "14.7%", 220955, 82309, 8630, 73679, "299.9%", 520393, 295089, "176.4%"),
    "FY2025": (66988, 220421, "30.4%", 329206, "20.3%", 212180, 44148, 5456, 38692, "548.4%", 480437, 211608, "227.0%"),
    "FY2024": (52617, 200213, "26.3%", 316246, "16.6%", 149255, 39271, 10380, 28891, "516.6%", 440424, 213351, "206.4%"),
    "FY2023": (57482, 88249, "65.1%", 134402, "42.8%", 71930, 18358, 9363, 8996, "799.6%", 247010, 93289, "264.8%"),
    "FY2022": (37411, 87216, "42.9%", 109158, "34.3%", 20648, 13379, 8079, 5300, "389.6%", 128630, 78103, "164.7%"),
    "FY2021": (26396, None, "78.92%", None, None, None, None, None, None, None, None, None, None),
}
_NO_KM1 = (None,) * 13
def col(i): return {y: km1.get(y, _NO_KM1)[i] for y in YEARS}
P3_SOURCES_WITH_FY2021 = P3_SOURCES + "\n\n" + P3_21_SOURCES
metric("CET1 Capital", "£'000", [("Common Equity Tier 1 (CET1) capital", col(0))], sources=P3_SOURCES_WITH_FY2021)
metric("CET1 Ratio", "%", [("Common Equity Tier 1 (CET1) ratio", col(2))], sources=P3_SOURCES_WITH_FY2021)
metric("Tier 1 Capital", "£'000", [("Tier 1 capital", col(0))], sources=P3_SOURCES_WITH_FY2021)
metric("Tier 1 Ratio", "%", [("Tier 1 ratio", col(2))], sources=P3_SOURCES_WITH_FY2021)
metric("Total Capital", "£'000", [("Total capital", col(0))], sources=P3_SOURCES_WITH_FY2021)
metric("Total Capital Ratio", "%", [("Total capital ratio", col(2))], sources=P3_SOURCES_WITH_FY2021)
metric("Total RWAs", "£'000", [("Total risk-weighted exposure amount", col(1))])

bw.add_rwa_breakdown_sheet(
    title="Recognise Bank Limited - RWA Breakdown",
    subtitle="UK OV1 Overview of risk-weighted exposure amounts, £'000; FY2022-FY2026 (31 March year-end). No standalone Pillar 3 OV1 disclosure exists for FY2018-FY2021 (self-skipped).",
    rows=[
        ("SECTION", "Risk-weighted exposure amounts by category", {}),
        ("DATA", "Credit risk (excluding CCR)", {"FY2026": 325441, "FY2025": 198530, "FY2024": 187320, "FY2023": 83185, "FY2022": 81924}),
        ("DATA", "Counterparty credit risk (CCR)", {"FY2026": 61, "FY2025": 91}),
        ("DATA", "Operational risk", {"FY2026": 30874, "FY2025": 21800, "FY2024": 12893, "FY2023": 5065, "FY2022": 5292}),
        ("TOTAL", "Total risk-weighted exposure amount", {"FY2026": 356376, "FY2025": 220421, "FY2024": 200213, "FY2023": 88249, "FY2022": 87216}),
        ("SECTION", "Not applicable - entity held no PRA authorisation in these years", {}),
        ("DATA", "Not applicable (no banking licence, and no authorisation of any kind, held at these year-ends)", {
            "FY2020": "Not applicable",
            "FY2019": "Not applicable",
            "FY2018": "Not applicable",
        }),
    ],
    sources_text=RWA_SOURCES + "\n\n" + PRE_AUTHORISATION_NOTE + "\n\n" + ENUMERATED_NEGATIVE_NOTE,
    first_col_width=54,
    source_height=220,
    unit_suffix=" (£'000)",
)

metric("Leverage Ratio", "£'000 / %", [("Total exposure measure excluding claims on central banks", col(3)), ("Leverage ratio excluding claims on central banks", col(4))])
metric("LCR", "£'000 / %", [("Total high-quality liquid assets (HQLA), weighted value - average", col(5)), ("Cash outflows - total weighted value", col(6)), ("Cash inflows - total weighted value", col(7)), ("Total net cash outflows (adjusted value)", col(8)), ("Liquidity coverage ratio", col(9))])
metric("NSFR", "£'000 / %", [("Total available stable funding", col(10)), ("Total required stable funding", col(11)), ("NSFR ratio", col(12))])
metric("MREL Ratio", None, [("MREL ratio", {y: "Not publicly disclosed" for y in YEARS if y not in PRE_AUTHORISATION_YEARS})], "No quantitative MREL ratio was located in the official Recognise Bank annual reports or Pillar 3 disclosures reviewed. The March 2023, 2024, 2025 and 2026 Pillar 3 disclosures contain no MREL row in their UK KM1 tables at all (the 2026 edition was re-read in full on 2026-09-15 to confirm). FY2018-FY2020 read 'Not applicable' rather than 'Not publicly disclosed' because the entity was not PRA-authorised in those years.")

def row_values(label, rows_list=rows):
    return next(values for kind, name, values in rows_list if name == label)

equity_opening = {"FY2026": 68801, "FY2025": 54132, "FY2024": 58301, "FY2023": 37923, "FY2022": 27246, "FY2021": 416, "FY2020": 222, "FY2019": 813, "FY2018": 0}
equity_other_movements = {"FY2026": 5000, "FY2025": 20001, "FY2024": 5090, "FY2023": 33161, "FY2022": 23121, "FY2021": 34642, "FY2020": 3545, "FY2019": 1000, "FY2018": 1009}

bw.add_overview_sheet(
    cash_flow_totals=[(label, row_values(label)) for label in ["Net cash (used in)/generated from operating activities", "Net cash (used in)/generated from investing activities", "Net cash generated from financing activities", "Cash and cash equivalents at end of year"]],
    cash_flow_unit="£'000",
    ratios=[
        ("CET1 Ratio", {**{y: "Not applicable" for y in PRE_AUTHORISATION_YEARS}, **{k: v for k, v in col(2).items() if v is not None}}),
        ("Total Capital Ratio", {**{y: "Not applicable" for y in PRE_AUTHORISATION_YEARS}, **{k: v for k, v in col(2).items() if v is not None}}),
        ("Leverage Ratio", {**{y: "Not applicable" for y in PRE_AUTHORISATION_YEARS}, **{k: v for k, v in col(4).items() if v is not None}}),
        ("LCR", {**{y: "Not applicable" for y in PRE_AUTHORISATION_YEARS}, **{k: v for k, v in col(9).items() if v is not None}}),
        ("NSFR", {**{y: "Not applicable" for y in PRE_AUTHORISATION_YEARS}, **{k: v for k, v in col(12).items() if v is not None}}),
    ],
    balance_sheet_totals=[
        ("Total assets", row_values("Total assets", BS_ROWS)),
        ("Loans and advances to customers", row_values("Loans and advances to customers", BS_ROWS)),
        ("Deposits from customers", row_values("Deposits from customers", BS_ROWS)),
        ("Total equity", row_values("Total equity", BS_ROWS)),
    ],
    balance_sheet_unit="£'000",
    income_statement_totals=[
        ("Net operating income", row_values("Net operating income", PL_ROWS)),
        ("Total operating expense", row_values("Total operating expense", PL_ROWS)),
        ("Profit/(loss) for the year", row_values("Profit/(loss) for the year", PL_ROWS)),
    ],
    income_statement_unit="£'000",
    equity_changes_totals=[
        ("Opening equity", equity_opening),
        ("Total comprehensive income/(loss) for the year", {"FY2026": 8856, "FY2025": -5332, "FY2024": -9259, "FY2023": -12783, "FY2022": -12444, "FY2021": -7811, "FY2020": -3351, "FY2019": -1591, "FY2018": -196}),
        ("Other equity movements (share issuances etc.), net", equity_other_movements),
        ("Closing equity", row_values("Total equity", BS_ROWS)),
    ],
    equity_changes_unit="£'000",
    note="Cash flows and Balance Sheet are Company/standalone figures. P&L detail rows are Group-level for FY2021-FY2024 (Company P&L not separately presented under s.408 exemption); 'Profit/(loss) for the year' is the Company-level figure throughout, consistent with the rest of the workbook. Pillar 3 metrics are Recognise Bank Limited UK KM1 figures, except FY2021's CET1/Tier 1/Total Capital figures, which come from an Annual Report capital-adequacy note (no standalone Pillar 3 document existed yet). FY2025 accounts were not consolidated after CAML entered liquidation; the 2026 report supplies the FY2025 comparative. FY2018-FY2020 predate any banking licence: no loan book, no deposits, no Pillar 3 metrics, and no Asset Quality/RWA Breakdown sheets exist for those years (genuinely not applicable, not merely undisclosed) - see HISTORICAL_NOTE on the Balance Sheet sheet for the full account of what was self-skipped and why. FY2017 itself has no separate accounts at all (folded into the first, 14-month FY2018 period). Blank cells mean not disclosed, not zero. UPDATED 2026-09-15: FY2018-FY2020 regulatory cells now read 'Not applicable' explicitly rather than sitting blank, because the Bank held no PRA authorisation of any kind at those year-ends (Authorisation with Restrictions was granted only in November 2020, full authorisation in September 2021, per the FY2022 Annual Report's own going-concern note and note 1) - a blank cell was indistinguishable from an unresearched gap and was being re-chased. FY2021 is deliberately NOT marked 'Not applicable': the Bank was authorised-with-restrictions for that whole year-end, so its remaining blanks are genuine non-disclosure. The bank's own investor index was re-enumerated on 2026-09-15 and lists Pillar 3 only for 2023-2026 and annual reports only for 2022-2026, confirming that no FY2018-FY2021 Pillar 3 document exists to be found; the March 2026 Pillar 3 was re-read in full and its KM1 reaches back only to Mar-22, every value of which already matches this workbook.",
)
bw.save("/Users/armaan/code/katalysis/banks/RECOGNISE BANK FINANCIALS.xlsx")
