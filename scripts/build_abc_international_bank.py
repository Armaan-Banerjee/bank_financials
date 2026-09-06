import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

# PILLAR-3-ONLY WORKBOOK: ABC International Bank plc (company 02564490, FRN 149025)
# is a qualifying entity under FRS 101 and takes the "requirements of IAS 7 Statement
# of Cash Flows" exemption every year - explicitly stated in note 1.2 of its FY2024
# Annual Report: "there is no requirement to prepare a statement of cash flows in
# accordance with Financial Reporting Standard 101." No Statement of Cash Flows
# exists in any year's accounts. Pillar 3 / capital disclosures are available for all
# 12 years - FY2025's Total RWA/Capital/ratios come from the FY2025 Annual Report's own
# Financial Highlights table (same table used for FY2021-FY2022; visually transcribed,
# see AR2025_URL note below), not a separate Pillar 3 report - no FY2025 Pillar 3 OV1/
# leverage/LCR/NSFR breakdown could be located, so those 4 sheets stay FY2021-FY2024
# only. This follows the BNY Mellon International precedent: standard 13-sheet
# structure, but the Cash Flow Statement sheet documents the exemption instead of line
# items, and the Overview sheet omits the cash-flow chart.
#
# HD-018 EXTENSION (2026-09-05): back-extended from FY2021-FY2025 to FY2014-FY2025.
# Balance Sheet/P&L/Equity/Asset Quality for FY2014-FY2020 are sourced from ABCIB's
# own Annual Report each year (FY2014 and FY2019/FY2020 have a text layer; FY2015-
# FY2017 are scanned Companies House filings, visually transcribed page-by-page same
# as the existing FY2025 convention). Dedicated ABCIB-entity Pillar 3 reports exist for
# FY2017-FY2020 (all SOLO basis, matching FY2021/FY2022/FY2025); FY2014-FY2016 Pillar 3
# figures come from each year's own Annual Report "Financial Highlights" table (same
# solo-basis convention already used for FY2021/FY2022/FY2025) - no FY2014-2016
# ABCIB-entity Pillar 3 document could be located on the bank's site or via Wayback
# Machine (only Bank ABC GROUP-level "30 June" Basel III disclosures exist for those
# years, a different entity - confirmed by opening them and checking the cover page -
# not used here). FY2014-FY2016 report Tier 1/Total capital ratios only (Basel
# II/early-CRD IV era terminology - no separate CET1 concept is disclosed), consistent
# with this project's convention of treating CET1 = Tier 1 where ABCIB has no AT1
# instruments in issue (confirmed still true in every FY2017-2020 Pillar 3 report).
# Leverage Ratio/LCR are newly populated for FY2017-FY2020 (from the dedicated Pillar 3
# reports); NSFR and MREL remain undisclosed for every year 2014-2020, same as
# 2021-2025. RWA Breakdown (OV1 format) does not exist for any year outside
# FY2023-FY2024 - not a gap introduced by this extension.

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021", "FY2020", "FY2019", "FY2018",
         "FY2017", "FY2016", "FY2015", "FY2014"]  # most recent first, calendar year-end (31 December)
YEAR_LABEL = {y: y for y in YEARS}

AR2024_URL = "https://www.bank-abc.com/en/ShareholderRelations/Annual%20Reports/ABC%20IB%20Annual%20Report%202024%20_%20Spreads%20for%20web.pdf"
AR2022_URL = "https://www.bank-abc.com/en/ShareholderRelations/Annual%20Reports/ABCIB%20Annual%20Report%202022.pdf"
P3_2024_URL = "https://www.bank-abc.com/en/CountrySites/Europe/London/Financial-Info/Basel%20Pillars/ABCIB%20Pillar%203%20final%20Board%202024%20.pdf"
P3_2023_URL = "https://www.bank-abc.com/en/CountrySites/Europe/London/Financial-Info/Basel%20Pillars/BH2407109%20-%20Bank%20ABC%20Pillar%203%20Disclosures%202023%20-%20Final%20website%20version.pdf"
# FY2025 Companies House filing (accounts made up to 31 December 2025, filed 2026) IS available - it is
# scanned/image-only (no text layer), so figures below were transcribed by rendering each page to PNG and
# reading it visually (pdf_tools.py render + Read) rather than by text extraction. No separate FY2025 Pillar 3
# report or updated Financial Highlights-format Pillar 3 breakdown (OV1/leverage/LCR/NSFR) could be located on
# ABCIB's website - only the Annual Report's own "Financial Highlights" table (same table used for FY2021/
# FY2022), which gives Total RWA/Capital base/ratios but no category breakdown, leverage, LCR or NSFR.
AR2025_URL = "https://find-and-update.company-information.service.gov.uk/company/02564490/filing-history"  # Companies House filing history (2026 accounts filing, scanned/image-only PDF)

# HD-018 extension sources (FY2014-FY2020)
AR2020_URL = "https://www.bank-abc.com/en/ShareholderRelations/Annual%20Reports/ABCIB_Annual_Report_2020.pdf"
AR2019_URL = "https://www.bank-abc.com/en/ShareholderRelations/Annual%20Reports/ABCIB%20Annual%20Report%202019.pdf"
AR2018_URL = "https://www.bank-abc.com/en/ShareholderRelations/Annual%20Reports/Bank%20ABC%20Europe%202018%20Annual%20Report.pdf"
AR2014_URL = "https://www.bank-abc.com/en/ShareholderRelations/Annual%20Reports/ABCIB%20Annual%20Report%202014.pdf"
# FY2016/FY2017 Companies House filings (accounts made up to 31 Dec 2016 / 31 Dec 2017) are
# scanned/image-only (no text layer) - transcribed by rendering each page to PNG and reading it
# visually (pdf_tools.py render + Read), same convention as FY2025 above. FY2016's filing also
# carries FY2015 as its comparative column (no separate FY2015 filing was opened).
CH2016_URL = "https://find-and-update.company-information.service.gov.uk/company/02564490/filing-history/MzE3MDg4MzM5M2FkaXF6a2N4/document?format=pdf&download=0"
CH2017_URL = "https://find-and-update.company-information.service.gov.uk/company/02564490/filing-history/MzE5OTA1ODc1MWFkaXF6a2N4/document?format=pdf&download=0"

P3_2020_URL = "https://www.bank-abc.com/en/CountrySites/Europe/London/Financial-Info/Basel%20Pillars/ABCIB-Pillar3Disclosure-2020.pdf"
P3_2019_URL = "https://www.bank-abc.com/en/CountrySites/Europe/London/Financial-Info/Basel%20Pillars/ABCIB-Pillar3Disclosure2019-postBRC.pdf"
P3_2017_URL = "https://www.bank-abc.com/en/CountrySites/Europe/London/Financial-Info/Basel%20Pillars/Pillar-3-Disclosure-2018.pdf"  # filename says "2018" but the document's own title page and content are "Pillar 3 Report 2017" (FY2017 figures) - confirmed by opening it, not a mistaken re-use of the FY2018 file (a separate Pillar-3-Disclosure_2018.pdf exists with FY2018 figures, cited as P3_2018_URL)
P3_2018_URL = "https://www.bank-abc.com/en/CountrySites/Europe/London/Financial-Info/Basel%20Pillars/Pillar-3-Disclosure_2018.pdf"

ENTITY_NOTE = (
    "ENTITY NOTE: ABC International Bank plc (company 02564490, FRN 149025, incorporated 3 December 1990) is a "
    "wholly-owned subsidiary within the Bank ABC (Arab Banking Corporation B.S.C., Bahrain) group. FY2023 and FY2024 "
    "figures are on a CONSOLIDATED basis (ABCIB's own subsidiaries, e.g. Alphabet Nominees Limited - a nominee "
    "company, not a trading entity), taken from ABCIB's own UK KM1 Pillar 3 template. FY2021 and FY2022 figures are "
    "on a SOLO (entity-only) basis, taken from the Annual Report's 'Financial Highlights' table - no consolidated "
    "Pillar 3 KM1-format disclosure could be located for those two years (only the modern KM1 template, introduced "
    "for the FY2023 report onward, publishes a full metrics breakdown; earlier years' Pillar 3 documents could not "
    "be located on the bank's website or via Wayback Machine). This is a genuine basis break within the series, not "
    "a data-entry choice - flagged on every affected sheet."
)

EXEMPTION_NOTE = (
    "FRS 101 CASH-FLOW EXEMPTION: ABCIB's FY2024 Annual Report states (Note 1.2, Basis of preparation): \"ABCIB is "
    "not required to prepare group accounts since it qualifies for the exemptions available under Section 401 of "
    "the Companies Act 2006. In addition, there is no requirement to prepare a statement of cash flows in "
    "accordance with Financial Reporting Standard 101,\" and lists among the FRS 101 exemptions taken: \"The "
    f"requirements of IAS 7 Statement of Cash Flows.\" - ABC International Bank plc Annual Report 2024, p.55 - "
    f"{AR2024_URL}. No Statement of Cash Flows exists in any of the entity's published accounts for any year - this "
    "is a standing structural feature of the entity, not a one-off or a data gap - confirmed as far back as FY2014 "
    "(same FRS 101 exemption language, ABC International Bank plc Annual Report 2014, note 1.2). Per the project's "
    "established policy for this exemption (see The Bank of New York Mellon (International) Limited), this "
    "workbook is built as a PILLAR-3-ONLY variant: all 11 Pillar 3 metric sheets are populated below (all 12 years "
    "for the capital/RWA total and ratio sheets; only FY2017-FY2020 and FY2023-FY2024 for Leverage Ratio/LCR, "
    "which aren't in the Financial Highlights table used for every other year; NSFR and MREL are not disclosed in "
    "any year), but no cash flow figures exist to show. See the Overview sheet for the equivalent treatment there."
)

CASH_FLOW_SOURCES = ENTITY_NOTE + "\n\n" + EXEMPTION_NOTE

BASIS_NOTE = (
    "FY2023-FY2024 shown on a CONSOLIDATED basis (ABCIB Pillar 3 Disclosures, UK KM1 template); every other year "
    "(FY2014-FY2022, FY2025) is shown on a SOLO basis - FY2017-FY2020 from ABCIB's own dedicated Pillar 3 report "
    "(which itself states its basis explicitly - only FY2020/FY2021's reports carry a Consolidated column "
    "alongside Solo, and the Solo column is used throughout for continuity with the other years - see below), "
    "FY2014-FY2016 and FY2021/FY2022/FY2025 from the Annual Report's own Financial Highlights table (no "
    "consolidated Pillar 3 KM1-format disclosure exists for those years). See the Cash Flow Statement sheet's "
    "entity note for detail. FY2025's Financial Highlights table (Total RWA £3,132m, Capital base £517m, Tier 1 "
    "ratio 15.0%, Total ratio 16.5%) does not split CET1 from Tier 1, so CET1/Tier 1 capital £m figures for FY2025 "
    "are CALCULATED (RWA x Tier 1 ratio), same convention as FY2014-FY2016/FY2021/FY2022 - see the CET1 Capital "
    "sheet note. No Leverage Ratio, LCR or NSFR figure appears in any Financial-Highlights-sourced year "
    "(FY2014-FY2016, FY2021/FY2022, FY2025) - those metrics are only available for FY2017-FY2020 (dedicated "
    "Pillar 3 reports) and FY2023-FY2024. NSFR and MREL are not disclosed in ANY year 2014-2025, including the "
    "dedicated FY2017-FY2020 Pillar 3 reports (which discuss NSFR only in qualitative/narrative terms, never as a "
    "figure).\n\n"
    "BASEL II/EARLY-CRD IV TERMINOLOGY CAVEAT: FY2014-FY2016's Financial Highlights tables report 'Risk asset "
    "ratio - Tier 1' and 'Risk asset ratio - Total' only - no separate CET1 concept is disclosed for those years "
    "(CET1 as a defined capital tier is a CRD IV/Basel III introduction phased in in the UK from 2014). Per this "
    "project's existing convention (assumes CET1 = Tier 1 where ABCIB has no AT1 instruments in issue - confirmed "
    "true in every FY2017-FY2024 Pillar 3 report reviewed), FY2014-FY2016's 'Risk asset ratio - Tier 1' is used "
    "for both the CET1 Ratio and Tier 1 Ratio sheets."
)


def p3_sources(extra=""):
    return (
        "Sources - ABC International Bank plc:\n"
        f"FY2024 & FY2023 (consolidated): ABC International Bank plc Pillar 3 Report 2024, Table \"UK KM1 - Key "
        f"metrics template\", p.14 - {P3_2024_URL}\n"
        f"FY2023 (consolidated, as originally reported): ABC International Bank plc Pillar 3 Disclosures 2023, "
        f"Table 3: Key Regulatory Metrics, p.13 - {P3_2023_URL}\n"
        f"FY2022 & FY2021 (solo): ABC International Bank plc Annual Report 2022, Financial Highlights, p.31 - "
        f"{AR2022_URL}\n"
        f"FY2025 (solo): ABC International Bank plc Annual Report 2025, Financial Highlights, p.20 (scanned "
        f"Companies House filing, visually transcribed) - {AR2025_URL}\n"
        f"FY2020 (solo): ABC International Bank plc Pillar 3 Disclosures 2020, Table 3 \"Key Regulatory Metrics\", "
        f"p.8 - {P3_2020_URL}\n"
        f"FY2019 (solo): ABC International Bank plc Pillar 3 Disclosures 2019, p.7-8 - {P3_2019_URL}\n"
        f"FY2018 (solo): ABC International Bank plc Pillar 3 Report 2018, p.8-9 (Table 3, 'IFRS9 Transitional "
        f"arrangements applied' column used for continuity with FY2019/FY2020) - {P3_2018_URL}\n"
        f"FY2017 (solo): ABC International Bank plc Pillar 3 Report 2017, Table 4 'RWAs and Capital ratio' and "
        f"Appendix 2 Own Funds disclosure, p.8/p.24 - {P3_2017_URL}\n"
        f"FY2016 (solo): ABC International Bank plc Annual Report 2016 (Companies House filing, scanned, visually "
        f"transcribed), Financial Highlights, p.17 - {CH2016_URL}\n"
        f"FY2015 (solo): as FY2016's own comparative column (no separate FY2015 filing opened) - {CH2016_URL}\n"
        f"FY2014 (solo): ABC International Bank plc Annual Report 2014, Financial Highlights, p.13 - {AR2014_URL}\n"
        + (extra + "\n" if extra else "") + BASIS_NOTE
    )


AR2023_URL = AR2024_URL  # FY2023/2024 primary statements both live in the 2024 Annual Report (comparative column)
AR2022B_URL = AR2022_URL  # FY2021/2022 primary statements both live in the 2022 Annual Report (comparative column)

STATEMENTS_ENTITY_NOTE = (
    "ENTITY NOTE: Balance Sheet, Profit & Loss and Statement of Changes in Equity are all prepared on ABCIB's own "
    "SOLO (entity, non-consolidated) FRS 101 basis for every year shown - ABCIB does not prepare group accounts "
    "(Companies Act 2006, Section 401 exemption; the 'Investment in subsidiary' line, where disclosed, is the only "
    "trace of ABCIB's subsidiaries on these statements - it is not disclosed at all for FY2014-FY2017, and grows "
    "from a nominal £33k in FY2018 to £163.8m in FY2020 once ABCIB's new Paris subsidiary, Arab Banking "
    "Corporation S.A. ('ABCSA'), is opened in October 2020 as part of the bank's post-Brexit restructuring - a "
    "real change in the underlying business, not a data gap). This is a different basis to the Pillar 3 sheets, "
    "which are CONSOLIDATED for FY2023-FY2024 and SOLO for every other year (see the Cash Flow Statement sheet's "
    "entity note) - flagged here so the two blocks of sheets aren't assumed to be on the same basis. FY2025 "
    "figures were transcribed by rendering the scanned FY2025 Companies House filing to PNG and reading it "
    "visually (pdf_tools.py render + Read), not from a text layer - see AR2025_URL; the same method was used for "
    "FY2015-FY2017 (scanned Companies House filings for those years - CH2016_URL/CH2017_URL), while FY2014 and "
    "FY2018-FY2020 have a text layer and were extracted directly.\n\n"
    "ACCOUNTING STANDARD NOTE: ABCIB adopted IFRS 9 (replacing IAS 39) from 1 January 2018, restating the opening "
    "1 January 2018 equity balance by -£6,549k (recognised as a separate roll-forward line on the Statement of "
    "Changes in Equity, not netted into 'profit for the year'). Two presentational consequences follow, both "
    "flagged rather than silently smoothed over: (1) the 'Financial investments - available-for-sale' balance "
    "sheet line (FY2014-FY2017, IAS 39) and the 'Debt investments - FVOCI' line (FY2018 onward, IFRS 9) are the "
    "same underlying asset class under different standards - shown on the SAME balance sheet row for continuity; "
    "(2) the equivalent OCI line on the Profit & Loss sheet is labelled 'Change in fair value of debt investments "
    "at FVOCI' throughout, though FY2014-FY2017's own statements label it 'Change in fair value of available for "
    "sale investments and loans and advances' (IAS 39 terminology) - again the same underlying item, relabelled "
    "for one consistent row across the full FY2014-FY2025 series."
)

BALANCE_SHEET_SOURCES = (
    "Sources - ABC International Bank plc:\n"
    f"FY2025: ABC International Bank plc Annual Report 2025, Statement of Financial Position, p.46 (scanned "
    f"filing, visually transcribed) - {AR2025_URL}\n"
    f"FY2024 & FY2023: ABC International Bank plc Annual Report 2024, Statement of Financial Position, p.53 (FY2023 "
    f"restated - see Note 37) - {AR2024_URL}\n"
    f"FY2022 & FY2021: ABC International Bank plc Annual Report 2022, Statement of Financial Position, p.62 - "
    f"{AR2022_URL}\n"
    f"FY2020 & FY2019: ABC International Bank plc Annual Report 2020, Statement of Financial Position, p.58 - "
    f"{AR2020_URL}\n"
    f"FY2019 & FY2018 (as originally reported): ABC International Bank plc Annual Report 2019, Statement of "
    f"Financial Position, p.51 - {AR2019_URL}\n"
    f"FY2017 & FY2016 (as originally reported): ABC International Bank plc Annual Report 2017 (Companies House "
    f"filing, scanned, visually transcribed), Statement of Financial Position, p.40 - {CH2017_URL}\n"
    f"FY2016 & FY2015 (as originally reported): ABC International Bank plc Annual Report 2016 (Companies House "
    f"filing, scanned, visually transcribed), Statement of Financial Position, p.33 - {CH2016_URL}\n"
    f"FY2014: ABC International Bank plc Annual Report 2014, Statement of Financial Position, p.26 - {AR2014_URL}\n"
    + STATEMENTS_ENTITY_NOTE + "\n\n"
    "PRESENTATION NOTE: FY2025 introduces two lines not present in earlier years - 'Investment property' (£5,973k) "
    "and a 'Pension scheme liability' of £163k (FY2024 instead showed a net 'Pension scheme asset' of £1,347k, "
    "now nil) - both are new/changed, not omissions, and are shown as disclosed. 'Investment in subsidiary' is not "
    "disclosed at all for FY2014-FY2017 (blank, not zero) - see the entity note above."
)

INCOME_STATEMENT_SOURCES = (
    "Sources - ABC International Bank plc:\n"
    f"FY2025: ABC International Bank plc Annual Report 2025, Statement of Comprehensive Income, p.45 (scanned "
    f"filing, visually transcribed) - {AR2025_URL}\n"
    f"FY2024 & FY2023: ABC International Bank plc Annual Report 2024, Statement of Comprehensive Income, p.52 "
    f"(FY2023 restated - see Note 37) - {AR2024_URL}\n"
    f"FY2022 & FY2021: ABC International Bank plc Annual Report 2022, Statement of Comprehensive Income, p.61 - "
    f"{AR2022_URL}\n"
    f"FY2020 & FY2019: ABC International Bank plc Annual Report 2020, Statement of Comprehensive Income, p.57 - "
    f"{AR2020_URL}\n"
    f"FY2019 & FY2018 (as originally reported): ABC International Bank plc Annual Report 2019, Statement of "
    f"Comprehensive Income, p.51 - {AR2019_URL}\n"
    f"FY2017 & FY2016 (as originally reported): ABC International Bank plc Annual Report 2017 (Companies House "
    f"filing, scanned, visually transcribed), Statement of Comprehensive Income, p.39 - {CH2017_URL}\n"
    f"FY2016 & FY2015 (as originally reported): ABC International Bank plc Annual Report 2016 (Companies House "
    f"filing, scanned, visually transcribed), Income Statement + Statement of Comprehensive Income, p.31-32 - "
    f"{CH2016_URL}\n"
    f"FY2014: ABC International Bank plc Annual Report 2014, Statement of Comprehensive Income, p.25 - "
    f"{AR2014_URL}\n"
    + STATEMENTS_ENTITY_NOTE + "\n\n"
    "PRESENTATION NOTE: ABCIB's statement of comprehensive income is presented net of interest/fee income and "
    "expense from the top (\"Profit for the year attributable to owners\" is the first disclosed line, with "
    "expense items not broken out above it) - there is no Revenue/Net operating income subtotal structure "
    "disclosed for any year, unlike Monzo's workbook. \"Total comprehensive income for the year\" is the one row "
    "comparable and populated across all 12 years. FY2014-FY2020's own primary statements actually DO disclose a "
    "full Income Statement above this point (net interest income, fees, G&A expenses, impairment, profit before "
    "tax) - not reproduced here, to keep this sheet's row set identical across all 12 years matching the "
    "FY2021-FY2025 disclosure shape already established; the full income statement for those years is available "
    "in the cited primary sources for a human who wants it.\n\n"
    "DISCREPANCY FLAGGED (found while sourcing FY2025, not fixed - out of scope for this pass): AR2024's own OCI "
    "line items for FY2024 (as directly re-verified against the source PDF: Foreign exchange movement 155, "
    "Actuarial gain 36, tax (69), FVOCI tax (333), FVOCI change (1,044), reclassification 1,954, ECL 4, fair "
    "value hedging 423) sum to +1,126, but AR2024's own disclosed 'Total comprehensive income' row implies a "
    "total OCI of only +35 (34,148 - 34,113 profit) - the components do not reconcile to AR2024's own total, "
    "which is a defect in the primary source, not a transcription error (both re-verified directly against the "
    "PDF text). AR2025's FY2024 comparative column uses a different item set (no separate FX line; Actuarial "
    "(1,055) not 36; fair value hedging 578 not 423) that DOES reconcile to 35 exactly. The FY2024 figures below "
    "are left as originally sourced from AR2024 (each year sourced from its own primary report, per this "
    "project's convention) rather than silently swapped to AR2025's restated figures - a genuine unresolved "
    "reconciliation gap in ABCIB's own disclosures, flagged here for a human to judge. FY2021-FY2023 were not "
    "re-checked for the same issue (out of scope for this pass)."
)

EQUITY_CHANGES_SOURCES = (
    "Sources - ABC International Bank plc:\n"
    f"FY2021-FY2022 roll-forward: ABC International Bank plc Annual Report 2022, Statement of Changes in Equity, "
    f"p.62 - {AR2022_URL}\n"
    f"FY2023-FY2024 roll-forward: ABC International Bank plc Annual Report 2024, Statement of Changes in Equity, "
    f"p.54 (FY2023 restated - see Note 37; opening 1 Jan 2023 balance not materially affected) - {AR2024_URL}\n"
    f"FY2025 roll-forward: ABC International Bank plc Annual Report 2025, Statement of Changes in Equity, p.47 "
    f"(scanned filing, visually transcribed) - {AR2025_URL}\n"
    f"FY2019-FY2020 roll-forward: ABC International Bank plc Annual Report 2020, Statement of Changes in Equity, "
    f"p.59 - {AR2020_URL}\n"
    f"FY2018-FY2019 roll-forward (incl. the IFRS 9 transition adjustment at 1 Jan 2018): ABC International Bank "
    f"plc Annual Report 2019, Statement of Changes in Equity, p.52 - {AR2019_URL}\n"
    f"FY2016-FY2017 roll-forward: ABC International Bank plc Annual Report 2017 (Companies House filing, scanned, "
    f"visually transcribed), Statement of Changes in Equity, p.41 - {CH2017_URL}\n"
    f"FY2014-FY2016 roll-forward: ABC International Bank plc Annual Report 2016 (Companies House filing, scanned, "
    f"visually transcribed), Statement of Changes in Equity, p.34 - {CH2016_URL}; FY2014 opening/closing balances "
    f"cross-checked against ABC International Bank plc Annual Report 2014, Statement of Changes in Equity, p.27 - "
    f"{AR2014_URL}\n"
    + STATEMENTS_ENTITY_NOTE + "\n\n"
    "RECONCILIATION GAP FLAGGED (found while sourcing this extension, not fixed - out of scope for this pass): "
    "ABCIB's own FY2020 Annual Report discloses a 31 December 2020 closing 'Total equity' of £501,167k (Share "
    "capital 212,296 / Retained earnings 287,834 / Fair value reserve 1,037), but the already-shipped FY2021-2025 "
    "columns on this sheet (sourced from AR2022) open FY2021 at £503,157k (Retained earnings 289,824) - a £1,990k "
    "gap in the opening balance that neither AR2020 nor AR2022 explains (no restatement note found in AR2022 for "
    "the FY2021 opening position). Left as originally sourced in each affected year per this project's convention; "
    "flagged here for a human to judge."
)

ASSET_QUALITY_SOURCES = (
    "Sources - ABC International Bank plc:\n"
    f"FY2025 IFRS 9 stage roll-forward: ABC International Bank plc Annual Report 2025, Note 11 (Loans and advances "
    f"to customers), p.62 (scanned filing, visually transcribed) - {AR2025_URL}\n"
    f"FY2023-FY2024 IFRS 9 stage roll-forward: ABC International Bank plc Annual Report 2024, Note 11 (Loans and "
    f"advances to customers), p.76-77 - {AR2024_URL}\n"
    f"FY2021-FY2022 IFRS 9 stage roll-forward: ABC International Bank plc Annual Report 2022, Note 11, p.87-89 - "
    f"{AR2022_URL}\n"
    f"FY2020 IFRS 9 stage roll-forward: ABC International Bank plc Annual Report 2020, Note 11, p.84-85 - "
    f"{AR2020_URL}\n"
    f"FY2019 & FY2018 IFRS 9 stage roll-forward (as originally reported): ABC International Bank plc Annual Report "
    f"2019, Note 11, p.76-77 - {AR2019_URL}\n"
    f"FY2017 & FY2016 (as originally reported): ABC International Bank plc Annual Report 2017 (Companies House "
    f"filing, scanned, visually transcribed), Notes 11-13, p.52-53 - {CH2017_URL}\n"
    f"FY2016 & FY2015 (as originally reported): ABC International Bank plc Annual Report 2016 (Companies House "
    f"filing, scanned, visually transcribed), Notes 11-13, p.47 - {CH2016_URL}\n"
    f"FY2014: ABC International Bank plc Annual Report 2014, Notes 14-15 (Loans and advances by credit quality; "
    f"Movements in allowance for impairment losses), p.44 - {AR2014_URL}\n"
    + STATEMENTS_ENTITY_NOTE + "\n\n"
    "PRESENTATION NOTE: No by-product breakdown of the loan book is disclosed (a single 'Loans and advances to "
    "customers' line only) - only the IFRS 9 stage 1/2/3 breakdown, shown here. Ratios are calculated from the "
    "disclosed gross carrying amount and ECL allowance figures. FY2025's Stage 1/Stage 3 gross figures include "
    "£60.5m/£1.5m of credit enhancements via export credit agency guarantee respectively (per the Annual Report's "
    "own footnote) - shown gross, as disclosed, not netted down.\n\n"
    "IAS 39 / PRE-IFRS 9 CAVEAT: FY2014-FY2017 report loans and advances to customers on an IAS 39 two-category "
    "'impaired' / 'neither past due nor impaired' basis, not the three-stage IFRS 9 expected-credit-loss model "
    "(adopted 1 January 2018 - see the entity note above) - the IFRS 9 'Stage 2' concept (a meaningful rise in "
    "credit risk without the loan yet being credit-impaired) simply does not exist pre-2018. For continuity of "
    "this sheet's row layout across all 12 years, FY2014-FY2017's 'neither past due nor impaired' balance is shown "
    "under 'Stage 1', 'Stage 2' is left blank (not zero - a concept that did not exist, not a disclosed nil), and "
    "'impaired' is shown under 'Stage 3'. Likewise the ECL allowance split shown under 'Stage 1 ECL allowance' / "
    "'Stage 3 ECL allowance' for FY2014-FY2017 is actually ABCIB's own 'collectively assessed' / 'individually "
    "assessed' provision split (IAS 39 terminology) - a reasonable but approximate analogy (collective provisions "
    "broadly correspond to the performing/under-performing book, individual provisions to the impaired book), not "
    "an exact IFRS 9 equivalence. The NPL and coverage ratios below are calculated on the CUSTOMER loan book only "
    "throughout, in every year - this is a narrower denominator than the combined banks+customers ratios ABCIB's "
    "own Financial Highlights table reports (e.g. FY2016: this sheet's 2.29% vs the Financial Highlights table's "
    "0.7%, which divides by the combined loans-to-banks-and-customers book), so the two should not be compared "
    "directly."
)

RWA_BREAKDOWN_SOURCES = (
    "Sources - ABC International Bank plc (CONSOLIDATED basis, matching the Total RWAs sheet):\n"
    f"FY2024 & FY2023 (FY2023 as originally reported by the FY2024 report's own comparative column - no separate "
    f"OV1 breakdown exists in ABCIB's own FY2023 Pillar 3 Disclosures document, which only carries Table 3's "
    f"single Total RWA figure, not a category breakdown): ABC International Bank plc Pillar 3 Report 2024, Table "
    f"\"UK OV1 - Overview of risk weighted exposure amounts\", ABCIB CONSOLIDATED, p.14 - {P3_2024_URL}\n"
    "Every other year (FY2014-FY2022, FY2025): not available - no OV1-format RWA category breakdown exists for "
    "these years, only the single Total RWA figure (either the Annual Report's Financial Highlights table, or - "
    "for FY2017-FY2020 - the dedicated Pillar 3 report's Table 3/Table 4, neither of which carries a category "
    "breakdown; see the Total RWAs sheet). No separate FY2025 Pillar 3 report could be located on ABCIB's website, "
    "and no FY2014-FY2016 ABCIB-entity Pillar 3 document could be located at all (see p3_sources note)."
)


bw = BankWorkbook(bank_name="ABC International Bank plc", years=YEARS, year_label=YEAR_LABEL, header_color="0D7377")

# ---------------------------------------------------------------
# Sheet: Balance Sheet (Consolidated -> actually SOLO, see entity note)
# ---------------------------------------------------------------
balance_sheet_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and cash equivalents", {"FY2025": 103934, "FY2024": 373606, "FY2023": 535241, "FY2022": 133298, "FY2021": 8395, "FY2020": 47646, "FY2019": 32683, "FY2018": 70763, "FY2017": 21379, "FY2016": 26269, "FY2015": 83226, "FY2014": 81076}),
    ("DATA", "Debt investments - FVOCI", {"FY2025": 562145, "FY2024": 550345, "FY2023": 494318, "FY2022": 574839, "FY2021": 466103, "FY2020": 333872, "FY2019": 277909, "FY2018": 265129, "FY2017": 277687, "FY2016": 321055, "FY2015": 219030, "FY2014": 259769}),
    ("DATA", "Loans and advances to banks", {"FY2025": 1164047, "FY2024": 896970, "FY2023": 604546, "FY2022": 1036596, "FY2021": 1002776, "FY2020": 975054, "FY2019": 1186006, "FY2018": 1855187, "FY2017": 1441263, "FY2016": 2350215, "FY2015": 1519663, "FY2014": 1086342}),
    ("DATA", "Loans and advances to customers", {"FY2025": 1540521, "FY2024": 1368632, "FY2023": 1290334, "FY2022": 1101772, "FY2021": 1094131, "FY2020": 1105423, "FY2019": 1435262, "FY2018": 1414678, "FY2017": 1121735, "FY2016": 909592, "FY2015": 983414, "FY2014": 1170920}),
    ("DATA", "Derivative financial assets", {"FY2025": 4859, "FY2024": 20825, "FY2023": 4038, "FY2022": 3704, "FY2021": 3606, "FY2020": 490, "FY2019": 336, "FY2018": 1905, "FY2017": 874, "FY2016": 16438, "FY2015": 1843, "FY2014": 39487}),
    ("DATA", "Tangible fixed assets", {"FY2025": 29127, "FY2024": 35131, "FY2023": 35215, "FY2022": 35409, "FY2021": 36270, "FY2020": 37386, "FY2019": 39303, "FY2018": 39561, "FY2017": 39885, "FY2016": 40290, "FY2015": 2113, "FY2014": 1098}),
    ("DATA", "Investment property", {"FY2025": 5973}),
    ("DATA", "Current tax asset", {"FY2025": 1104, "FY2024": 889, "FY2022": 0, "FY2021": 127, "FY2020": 923, "FY2019": 730, "FY2018": 322, "FY2017": 0, "FY2016": 315, "FY2015": 1493, "FY2014": 67}),
    ("DATA", "Deferred tax asset", {"FY2022": 2149, "FY2021": 1574, "FY2020": 3159, "FY2019": 2041, "FY2018": 2314, "FY2017": 2915, "FY2016": 4119, "FY2015": 3154, "FY2014": 7245}),
    ("DATA", "Prepayments, accrued income and other debtors", {"FY2025": 44993, "FY2024": 75609, "FY2023": 62556, "FY2022": 88821, "FY2021": 27093, "FY2020": 63630, "FY2019": 49163, "FY2018": 46246, "FY2017": 26396, "FY2016": 21214, "FY2015": 20579, "FY2014": 50703}),
    ("DATA", "Pension scheme asset", {"FY2025": 0, "FY2024": 1347}),
    ("DATA", "Investment in subsidiary", {"FY2025": 171713, "FY2024": 163776, "FY2023": 171043, "FY2022": 174302, "FY2021": 165804, "FY2020": 163814, "FY2019": 4253, "FY2018": 33}),
    ("TOTAL", "Total assets", {"FY2025": 3628416, "FY2024": 3487130, "FY2023": 3197291, "FY2022": 3150890, "FY2021": 2805879, "FY2020": 2731397, "FY2019": 3027686, "FY2018": 3696138, "FY2017": 2932134, "FY2016": 3689507, "FY2015": 2834515, "FY2014": 2696707}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Deposits from banks", {"FY2025": 1801577, "FY2024": 1793118, "FY2023": 1719290, "FY2022": 1604268, "FY2021": 1711980, "FY2020": 1650452, "FY2019": 1875147, "FY2018": 2382938, "FY2017": 1725984, "FY2016": 2599892, "FY2015": 1824418, "FY2014": 1753585}),
    ("DATA", "Customer deposits", {"FY2025": 796992, "FY2024": 588657, "FY2023": 460063, "FY2022": 517193, "FY2021": 238737, "FY2020": 224299, "FY2019": 243923, "FY2018": 432416, "FY2017": 399274, "FY2016": 267883, "FY2015": 235152, "FY2014": 196351}),
    ("DATA", "Derivative financial liabilities", {"FY2025": 1644, "FY2024": 1190, "FY2023": 13647, "FY2022": 10516, "FY2021": 635, "FY2020": 5501, "FY2019": 3975, "FY2018": 2533, "FY2017": 2280, "FY2016": 1720, "FY2015": 5604, "FY2014": 2087}),
    ("DATA", "Other liabilities, accruals and deferred income", {"FY2025": 61776, "FY2024": 208793, "FY2023": 168234, "FY2022": 195399, "FY2021": 102982, "FY2020": 56740, "FY2019": 56166, "FY2018": 51162, "FY2017": 21798, "FY2016": 22691, "FY2015": 22997, "FY2014": 55491}),
    ("DATA", "Current tax liability", {"FY2023": 491, "FY2022": 2286, "FY2020": 0, "FY2019": 1746, "FY2018": 2369, "FY2017": 2077, "FY2016": 1475, "FY2015": 185, "FY2014": 891}),
    ("DATA", "Term borrowing", {"FY2025": 315538, "FY2024": 256013, "FY2023": 216093, "FY2022": 224794, "FY2021": 164793, "FY2020": 230665, "FY2019": 288149, "FY2018": 275634, "FY2017": 245827, "FY2016": 278033, "FY2015": 245582, "FY2014": 170463}),
    ("DATA", "Pension scheme liability", {"FY2025": 163, "FY2023": 209, "FY2022": 2733, "FY2021": 2621, "FY2020": 12573, "FY2019": 11718, "FY2018": 11550, "FY2017": 15202, "FY2016": 18086, "FY2015": 8581, "FY2014": 9732}),
    ("DATA", "Subordinated liabilities", {"FY2025": 48263, "FY2024": 51869, "FY2023": 51121, "FY2022": 50000, "FY2021": 50000, "FY2020": 50000, "FY2019": 50000, "FY2018": 50000, "FY2017": 50000, "FY2016": 50000, "FY2015": 50000, "FY2014": 80813}),
    ("DATA", "Deferred tax liability", {"FY2025": 1409, "FY2024": 1016, "FY2023": 11}),
    ("TOTAL", "Total liabilities", {"FY2025": 3027362, "FY2024": 2900656, "FY2023": 2629159, "FY2022": 2607189, "FY2021": 2271748, "FY2020": 2230230, "FY2019": 2530824, "FY2018": 3208602, "FY2017": 2462442, "FY2016": 3239780, "FY2015": 2392519, "FY2014": 2269413}),
    ("SECTION", "Equity", {}),
    ("DATA", "Share capital", {"FY2025": 212296, "FY2024": 212296, "FY2023": 212296, "FY2022": 212296, "FY2021": 212296, "FY2020": 212296, "FY2019": 212296, "FY2018": 212296, "FY2017": 212296, "FY2016": 212296, "FY2015": 212296, "FY2014": 212296}),
    ("DATA", "Retained earnings", {"FY2025": 385710, "FY2024": 372922, "FY2023": 355584, "FY2022": 334086, "FY2021": 321493, "FY2020": 287834, "FY2019": 284231, "FY2018": 275816, "FY2017": 257372, "FY2016": 237409, "FY2015": 229682, "FY2014": 215018}),
    ("DATA", "Fair value reserve", {"FY2025": 3048, "FY2024": 1256, "FY2023": 252, "FY2022": -2681, "FY2021": 342, "FY2020": 1037, "FY2019": 335, "FY2018": -576, "FY2017": 24, "FY2016": 22, "FY2015": 18, "FY2014": -20}),
    ("TOTAL", "Total equity", {"FY2025": 601054, "FY2024": 586474, "FY2023": 568132, "FY2022": 543701, "FY2021": 534131, "FY2020": 501167, "FY2019": 496862, "FY2018": 487536, "FY2017": 469692, "FY2016": 449727, "FY2015": 441996, "FY2014": 427294}),
    ("TOTAL", "Total equity and liabilities", {"FY2025": 3628416, "FY2024": 3487130, "FY2023": 3197291, "FY2022": 3150890, "FY2021": 2805879, "FY2020": 2731397, "FY2019": 3027686, "FY2018": 3696138, "FY2017": 2932134, "FY2016": 3689507, "FY2015": 2834515, "FY2014": 2696707}),
]

bw.add_balance_sheet_sheet(
    title="ABC International Bank plc — Statement of Financial Position",
    subtitle="Entity (solo) basis, all figures in £'000. Blank cells indicate that year's report did not disclose that specific line.",
    rows=balance_sheet_rows,
    sources_text=BALANCE_SHEET_SOURCES,
)

# ---------------------------------------------------------------
# Sheet: Profit & Loss
# ---------------------------------------------------------------
income_statement_rows = [
    ("SECTION", "Comprehensive income", {}),
    ("TOTAL", "Profit for the year attributable to owners", {"FY2025": 32616, "FY2024": 34113, "FY2023": 28022, "FY2022": 22069, "FY2021": 25344, "FY2020": 8001, "FY2019": 16031, "FY2018": 23085, "FY2017": 18521, "FY2016": 16227, "FY2015": 14025, "FY2014": 23684}),
    ("SECTION", "Items that cannot be reclassified to income statement", {}),
    ("DATA", "Foreign exchange movement", {"FY2024": 155, "FY2023": 22, "FY2022": -10, "FY2020": -47, "FY2019": -119, "FY2018": -14, "FY2017": 38, "FY2016": 28, "FY2015": -67, "FY2014": -142}),
    ("DATA", "Actuarial gain / (loss) recognised on defined benefit pension scheme", {"FY2025": -3431, "FY2024": 36, "FY2023": -1055, "FY2022": -2676, "FY2021": 7756, "FY2020": -5366, "FY2019": -2075, "FY2018": 2527, "FY2017": 1733, "FY2016": -10529, "FY2015": 326, "FY2014": -4350}),
    ("DATA", "Current and Deferred tax (charge) / credit relating to defined benefit pension scheme", {"FY2025": 703, "FY2024": -69, "FY2023": -37, "FY2022": 480, "FY2021": -1431, "FY2020": 1149, "FY2019": 391, "FY2018": -605, "FY2017": -329, "FY2016": 2001, "FY2015": 380, "FY2014": 599}),
    ("SECTION", "Items that can be reclassified to income statement", {}),
    ("DATA", "Deferred tax (charge) / credit relating to change in fair value of debt investments at FVOCI", {"FY2025": -420, "FY2024": -333, "FY2023": -988, "FY2022": 964, "FY2021": 205, "FY2020": -134, "FY2019": -43, "FY2018": 0, "FY2014": -70}),
    ("DATA", "Change in fair value of debt investments at FVOCI", {"FY2025": 4060, "FY2024": -1044, "FY2023": 2406, "FY2022": -6637, "FY2021": -765, "FY2020": 929, "FY2019": 831, "FY2018": -600, "FY2017": 2, "FY2016": 4, "FY2015": 38, "FY2014": 511}),
    ("DATA", "Reclassification to income statement: debt investments at FVOCI", {"FY2025": 549, "FY2024": 1954, "FY2023": 3421, "FY2022": -85, "FY2021": -282, "FY2020": -248}),
    ("DATA", "Change in ECL allowance for debt investments at FVOCI", {"FY2025": 6, "FY2024": 4, "FY2023": -33, "FY2022": 12, "FY2021": 2, "FY2020": 21, "FY2019": 80, "FY2018": 0}),
    ("DATA", "Net gain / (loss) due to fair value hedging", {"FY2025": -2403, "FY2024": 423, "FY2023": -1873, "FY2022": 2723, "FY2021": 145}),
    ("TOTAL", "Total comprehensive income for the year attributable to owners", {"FY2025": 31680, "FY2024": 34148, "FY2023": 31051, "FY2022": 16840, "FY2021": 30974, "FY2020": 4305, "FY2019": 15096, "FY2018": 24393, "FY2017": 19965, "FY2016": 7731, "FY2015": 14702, "FY2014": 20232}),
]

bw.add_income_statement_sheet(
    title="ABC International Bank plc — Statement of Comprehensive Income",
    subtitle="Entity (solo) basis, all figures in £'000. Blank cells indicate that year's report did not disclose that specific line.",
    rows=income_statement_rows,
    sources_text=INCOME_STATEMENT_SOURCES,
)

# ---------------------------------------------------------------
# Sheet: Statement of Changes in Equity (chronological, oldest -> newest)
# ---------------------------------------------------------------
EQUITY_HEADERS = ["Share capital", "Retained earnings", "Fair value reserve", "Total equity"]
equity_changes_rows = [
    ("TOTAL", "Balance at 1 January 2014", (212296, 195227, -461, 407062)),
    ("DATA", "Profit for the year", (None, 23684, None, 23684)),
    ("DATA", "Other comprehensive income / (loss)", (None, -3893, 441, -3452)),
    ("TOTAL", "Balance at 31 December 2014", (212296, 215018, -20, 427294)),
    ("DATA", "Profit for the year", (None, 14025, None, 14025)),
    ("DATA", "Other comprehensive income / (loss)", (None, 639, 38, 677)),
    ("TOTAL", "Balance at 31 December 2015", (212296, 229682, 18, 441996)),
    ("DATA", "Profit for the year", (None, 16227, None, 16227)),
    ("DATA", "Other comprehensive income / (loss)", (None, -8500, 4, -8496)),
    ("TOTAL", "Balance at 31 December 2016", (212296, 237409, 22, 449727)),
    ("DATA", "Profit for the year", (None, 18521, None, 18521)),
    ("DATA", "Other comprehensive income / (loss)", (None, 1442, 2, 1444)),
    ("TOTAL", "Balance at 31 December 2017", (212296, 257372, 24, 469692)),
    ("DATA", "Impact of adopting IFRS 9, net of tax (1 January 2018)", (None, -6549, None, -6549)),
    ("DATA", "Profit for the year", (None, 23085, None, 23085)),
    ("DATA", "Other comprehensive income / (loss)", (None, 1908, -600, 1308)),
    ("TOTAL", "Balance at 31 December 2018", (212296, 275816, -576, 487536)),
    ("DATA", "Dividend paid", (None, -5770, None, -5770)),
    ("DATA", "Profit for the year", (None, 16031, None, 16031)),
    ("DATA", "Other comprehensive income / (loss)", (None, -1846, 911, -935)),
    ("TOTAL", "Balance at 31 December 2019", (212296, 284231, 335, 496862)),
    ("DATA", "Dividend paid", (None, 0, None, 0)),
    ("DATA", "Profit for the year", (None, 8001, None, 8001)),
    ("DATA", "Other comprehensive income / (loss)", (None, -4398, 702, -3696)),
    ("TOTAL", "Balance at 31 December 2020", (212296, 287834, 1037, 501167)),
    ("TOTAL", "Balance at 1 January 2021", (212296, 289824, 1037, 503157)),
    ("DATA", "Profit for the year", (None, 25344, None, 25344)),
    ("DATA", "Other comprehensive income / (loss)", (None, 6325, -695, 5630)),
    ("TOTAL", "Balance at 31 December 2021", (212296, 321493, 342, 534131)),
    ("DATA", "Dividend paid", (None, -7270, None, -7270)),
    ("DATA", "Profit for the year", (None, 22069, None, 22069)),
    ("DATA", "Other comprehensive income / (loss)", (None, -2206, -3023, -5229)),
    ("TOTAL", "Balance at 31 December 2022", (212296, 334086, -2681, 543701)),
    ("DATA", "Dividend paid", (None, -6620, None, -6620)),
    ("DATA", "Profit for the year", (None, 28022, None, 28022)),
    ("DATA", "Other comprehensive income / (loss)", (None, 96, 2933, 3029)),
    ("TOTAL", "Balance at 31 December 2023", (212296, 355584, 252, 568132)),
    ("DATA", "Dividend paid", (None, -15806, None, -15806)),
    ("DATA", "Profit for the year", (None, 34113, None, 34113)),
    ("DATA", "Other comprehensive income / (loss)", (None, -969, 1004, 35)),
    ("TOTAL", "Balance at 31 December 2024", (212296, 372922, 1256, 586474)),
    ("DATA", "Dividend paid", (None, -17100, None, -17100)),
    ("DATA", "Profit for the year", (None, 32616, None, 32616)),
    ("DATA", "Other comprehensive income / (loss)", (None, -2728, 1792, -936)),
    ("TOTAL", "Balance at 31 December 2025", (212296, 385710, 3048, 601054)),
]

bw.add_equity_changes_sheet(
    title="ABC International Bank plc — Statement of Changes in Equity",
    subtitle="Entity (solo) basis, chronological, all figures in £'000.",
    headers=EQUITY_HEADERS,
    rows=equity_changes_rows,
    sources_text=EQUITY_CHANGES_SOURCES,
)

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement (exemption note in place of line items)
# ---------------------------------------------------------------
rows = [
    ("SECTION", "No Statement of Cash Flows is published by this entity in any year", {}),
    ("DATA", "See the note below for the FRS 101 exemption this entity relies on every year, and why this "
             "workbook is built as a Pillar-3-only variant.", {}),
]

bw.add_cash_flow_sheet(
    title="ABC International Bank plc — Cash Flow Statement",
    subtitle="Not applicable — this entity takes the FRS 101 cash-flow-statement disclosure exemption every year. See source note below.",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=90,
    source_height=280,
    unit_suffix="",
)

# ---------------------------------------------------------------
# Sheet: Asset Quality / Credit Risk Disclosures
# ---------------------------------------------------------------
asset_quality_rows = [
    ("SECTION", "Loans and advances to customers - gross carrying amount by IFRS 9 stage", {}),
    ("DATA", "Stage 1 (performing)", {"FY2025": 1508403, "FY2024": 1332380, "FY2023": 1225745, "FY2022": 979678, "FY2021": 944168, "FY2020": 941585, "FY2019": 1312947, "FY2018": 1292777, "FY2017": 1127006, "FY2016": 914584, "FY2015": 984581, "FY2014": 1169552}),
    ("DATA", "Stage 2 (underperforming / SICR)", {"FY2025": 5752, "FY2024": 6075, "FY2023": 41723, "FY2022": 108221, "FY2021": 160564, "FY2020": 174184, "FY2019": 128434, "FY2018": 126344}),
    ("DATA", "Stage 3 (credit-impaired / non-performing)", {"FY2025": 45704, "FY2024": 46882, "FY2023": 39868, "FY2022": 25547, "FY2021": 1311, "FY2020": 2247, "FY2019": 2729, "FY2018": 14626, "FY2017": 17713, "FY2016": 21433, "FY2015": 19133, "FY2014": 20260}),
    ("TOTAL", "Total gross carrying amount", {"FY2025": 1559859, "FY2024": 1385337, "FY2023": 1307336, "FY2022": 1113446, "FY2021": 1106043, "FY2020": 1118016, "FY2019": 1444109, "FY2018": 1433747, "FY2017": 1144719, "FY2016": 936017, "FY2015": 1003714, "FY2014": 1189812}),
    ("SECTION", "Loans and advances to customers - ECL allowance by IFRS 9 stage", {}),
    ("DATA", "Stage 1 ECL allowance", {"FY2025": 1164, "FY2024": 1524, "FY2023": 1096, "FY2022": 1569, "FY2021": 464, "FY2020": 914, "FY2019": 1750, "FY2018": 1932, "FY2017": 5700, "FY2016": 5900, "FY2015": 3135, "FY2014": 2200}),
    ("DATA", "Stage 2 ECL allowance", {"FY2025": 33, "FY2024": 9, "FY2023": 31, "FY2022": 3636, "FY2021": 10137, "FY2020": 9520, "FY2019": 4897, "FY2018": 3131}),
    ("DATA", "Stage 3 ECL allowance", {"FY2025": 18141, "FY2024": 15172, "FY2023": 15875, "FY2022": 6469, "FY2021": 1311, "FY2020": 2159, "FY2019": 2201, "FY2018": 14006, "FY2017": 17284, "FY2016": 20525, "FY2015": 17165, "FY2014": 16692}),
    ("TOTAL", "Total ECL allowance", {"FY2025": 19338, "FY2024": 16705, "FY2023": 17002, "FY2022": 11674, "FY2021": 11912, "FY2020": 12593, "FY2019": 8847, "FY2018": 19069, "FY2017": 22984, "FY2016": 26425, "FY2015": 20300, "FY2014": 18892}),
    ("SECTION", "Loans and advances to customers - net carrying amount", {}),
    ("TOTAL", "Net carrying amount", {"FY2025": 1540521, "FY2024": 1368632, "FY2023": 1290334, "FY2022": 1101772, "FY2021": 1094131, "FY2020": 1105423, "FY2019": 1435262, "FY2018": 1414678, "FY2017": 1121735, "FY2016": 909592, "FY2015": 983414, "FY2014": 1170920}),
    ("SECTION", "Derived ratios", {}),
    ("DATA", "Stage 3 / NPL ratio (Stage 3 gross / total gross)", {"FY2025": "2.93%", "FY2024": "3.38%", "FY2023": "3.05%", "FY2022": "2.29%", "FY2021": "0.12%", "FY2020": "0.20%", "FY2019": "0.19%", "FY2018": "1.02%", "FY2017": "1.55%", "FY2016": "2.29%", "FY2015": "1.91%", "FY2014": "1.70%"}),
    ("DATA", "Stage 3 coverage ratio (Stage 3 ECL / Stage 3 gross)", {"FY2025": "39.69%", "FY2024": "32.36%", "FY2023": "39.82%", "FY2022": "25.32%", "FY2021": "100.00%", "FY2020": "96.08%", "FY2019": "80.65%", "FY2018": "95.76%", "FY2017": "97.58%", "FY2016": "95.76%", "FY2015": "89.71%", "FY2014": "82.39%"}),
    ("DATA", "Overall ECL coverage ratio (Total ECL / Total gross)", {"FY2025": "1.24%", "FY2024": "1.21%", "FY2023": "1.30%", "FY2022": "1.05%", "FY2021": "1.08%", "FY2020": "1.13%", "FY2019": "0.61%", "FY2018": "1.33%", "FY2017": "2.01%", "FY2016": "2.82%", "FY2015": "2.02%", "FY2014": "1.59%"}),
]

bw.add_asset_quality_sheet(
    title="ABC International Bank plc — Asset Quality / Credit Risk Disclosures",
    subtitle="Loans and advances to customers only, entity (solo) basis, all figures in £'000. IFRS 9 stage breakdown; no by-product split disclosed.",
    rows=asset_quality_rows,
    sources_text=ASSET_QUALITY_SOURCES,
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, unit, rows_data, sources_text, note=note, first_col_width=52, source_height=150)


metric(
    "CET1 Capital", "£m",
    [("Common Equity Tier 1 (CET1) capital", {"FY2025": 469.8, "FY2024": 564.579, "FY2023": 547.665, "FY2022": 416.5, "FY2021": 418.8, "FY2020": 393.198, "FY2019": 495.422, "FY2018": 487.265, "FY2017": 469.029, "FY2016": 449.664, "FY2015": 439.008, "FY2014": 421.08})],
    p3_sources(),
    note="FY2025/FY2022/FY2021/FY2016/FY2015/FY2014 are calculated (RWA x Tier 1 ratio, all solo basis) - no "
         "separate CET1/Tier 1 £m figure is disclosed for those years, only the ratio and total 'Capital base'. "
         "Assumes CET1 = Tier 1 (no AT1 instruments in issue), consistent with the pattern directly confirmed in "
         "every FY2017-FY2024 Pillar 3 report reviewed. FY2017-FY2020 are directly disclosed (Appendix 2 Own "
         "Funds / Table 3 Key Regulatory Metrics of each year's dedicated Pillar 3 report); FY2018/FY2019 use the "
         "'IFRS9 Transitional arrangements applied' column for continuity with FY2020's single reported figure.",
)

metric(
    "CET1 Ratio", "% of RWA",
    [("Common Equity Tier 1 (CET1) ratio", {"FY2025": "15.0%", "FY2024": "16.2%", "FY2023": "17.6%", "FY2022": "17.0%", "FY2021": "16.7%", "FY2020": "16.4%", "FY2019": "17.5%", "FY2018": "16.6%", "FY2017": "18.2%", "FY2016": "19.2%", "FY2015": "20.4%", "FY2014": "22.0%"})],
    p3_sources(),
    note="FY2023 shown as originally reported (17.6%, consolidated); the FY2024 Pillar 3 Report's FY2023 "
         "comparative column restates this to 17.7% alongside a small RWA restatement (see Total RWAs sheet) - "
         "immaterial, but shown as originally reported per this project's convention. FY2022/FY2021/FY2025 and "
         "FY2014-FY2020 all labelled 'Tier 1 Capital Ratio' (a.k.a. 'Risk asset ratio - Tier 1') in the source "
         "(solo basis) - assumed equal to CET1 ratio, see CET1 Capital sheet note. FY2014-FY2016 predate the "
         "CET1 concept entirely (Basel II/early-CRD IV terminology) - see BASIS_NOTE's caveat.",
)

metric(
    "Tier 1 Capital", "£m",
    [("Tier 1 capital", {"FY2025": 469.8, "FY2024": 564.579, "FY2023": 547.665, "FY2022": 416.5, "FY2021": 418.8, "FY2020": 393.198, "FY2019": 495.422, "FY2018": 487.265, "FY2017": 469.029, "FY2016": 449.664, "FY2015": 439.008, "FY2014": 421.08})],
    p3_sources(),
    note="Tier 1 = CET1 every year (no AT1 instruments in issue). FY2025/FY2022/FY2021/FY2016/FY2015/FY2014 "
         "calculated - see CET1 Capital sheet note.",
)

metric(
    "Tier 1 Ratio", "% of RWA",
    [("Tier 1 ratio", {"FY2025": "15.0%", "FY2024": "16.2%", "FY2023": "17.6%", "FY2022": "17.0%", "FY2021": "16.7%", "FY2020": "16.4%", "FY2019": "17.5%", "FY2018": "16.6%", "FY2017": "18.2%", "FY2016": "19.2%", "FY2015": "20.4%", "FY2014": "22.0%"})],
    p3_sources(),
    note="FY2023 shown as originally reported (consolidated) - see CET1 Ratio sheet note.",
)

metric(
    "Total Capital", "£m",
    [("Total capital", {"FY2025": 517, "FY2024": 616.448, "FY2023": 598.786, "FY2022": 447, "FY2021": 460, "FY2020": 443.198, "FY2019": 545.422, "FY2018": 537.265, "FY2017": 524.729, "FY2016": 506, "FY2015": 493, "FY2014": 423})],
    p3_sources(),
    note="FY2022/FY2021/FY2025 ('Capital base'), FY2014-FY2016 ('Capital base', Financial Highlights table) and "
         "FY2023-FY2024/FY2017-FY2020 ('Total capital'/'Total regulatory capital') are directly disclosed, not "
         "calculated. FY2020's solo Total capital (443.198m) is genuinely lower than FY2019's (545.422m) - "
         "reflects the new investment in ABCSA (the Paris subsidiary) reducing solo-basis capital resources, per "
         "the FY2020 Pillar 3 report's own footnote ('The solo capital base reflect the new investment in "
         "ABSA') - a real basis effect, not a data error.",
)

metric(
    "Total Capital Ratio", "% of RWA",
    [("Total capital ratio", {"FY2025": "16.5%", "FY2024": "17.7%", "FY2023": "19.3%", "FY2022": "18.2%", "FY2021": "18.3%", "FY2020": "18.5%", "FY2019": "19.3%", "FY2018": "18.3%", "FY2017": "20.4%", "FY2016": "21.5%", "FY2015": "22.9%", "FY2014": "22.1%"})],
    p3_sources(),
    note="FY2025 labelled 'Risk asset ratio - Total' in the Financial Highlights table; same for FY2014-FY2016.",
)

metric(
    "Total RWAs", "£m",
    [("Total risk-weighted exposure amount", {"FY2025": 3132, "FY2024": 3486.256, "FY2023": 3104.763, "FY2022": 2450, "FY2021": 2508, "FY2020": 2397.973, "FY2019": 2824.811, "FY2018": 2940.867, "FY2017": 2574.027, "FY2016": 2342, "FY2015": 2152, "FY2014": 1914})],
    p3_sources(),
    note="FY2023 shown as originally reported (consolidated, 3,104.763m); the FY2024 Pillar 3 Report's FY2023 "
         "comparative column restates this to 3,101.197m - immaterial (~0.1%), shown as originally reported per "
         "this project's convention. FY2025 (3,132m, solo basis, Financial Highlights table 'Risk weighted "
         "assets') is genuinely lower than FY2024's consolidated 3,486.256m - a basis effect (solo excludes "
         "Alphabet Nominees Limited), not a real risk reduction; see BASIS_NOTE. FY2016 (2,342m, own-year Annual "
         "Report figure) differs immaterially (~0.2%) from the FY2018 Annual Report's restated FY2016 comparative "
         "(2,347m) - shown as originally reported, same convention as the FY2023 restatement above.",
)

rwa_breakdown_rows = [
    ("SECTION", "UK OV1 — Overview of risk weighted exposure amounts (CONSOLIDATED)", {}),
    ("DATA", "Credit risk (excluding CCR)", {"FY2024": 3198514, "FY2023": 2842771}),
    ("DATA", "Counterparty credit risk (CCR)", {"FY2024": 45144, "FY2023": 55407}),
    ("DATA", "Of which: credit valuation adjustment (CVA)", {"FY2024": 10131, "FY2023": 11788}),
    ("DATA", "Position, foreign exchange and commodities risks (Market risk)", {"FY2024": 14469, "FY2023": 5670}),
    ("DATA", "Operational risk", {"FY2024": 217998, "FY2023": 185561}),
    ("TOTAL", "Total risk weighted exposure amount", {"FY2024": 3486256, "FY2023": 3101197}),
]

bw.add_rwa_breakdown_sheet(
    title="ABC International Bank plc — RWA Breakdown",
    subtitle="CONSOLIDATED basis, all figures in £'000. Matches the Total RWAs sheet.",
    rows=rwa_breakdown_rows,
    sources_text=RWA_BREAKDOWN_SOURCES,
)

metric(
    "Leverage Ratio", "£m / %",
    [
        ("Total exposure measure excluding claims on central banks (£m)", {"FY2024": 5540.164, "FY2023": 5155.039, "FY2020": 2937.195, "FY2019": 3683.204, "FY2018": 4738.858, "FY2017": 3726.262}),
        ("Leverage ratio excluding claims on central banks (%)", {"FY2024": "10.2%", "FY2023": "10.62%", "FY2020": "13.39%", "FY2019": "13.45%", "FY2018": "10.28%", "FY2017": "12.59%"}),
    ],
    p3_sources(),
    note="FY2022/FY2021/FY2025/FY2014-FY2016 not available - the Annual Report Financial Highlights table (the "
         "only source located for those years) does not include a leverage ratio. FY2017-FY2020 are from each "
         "year's dedicated Pillar 3 report (solo basis; FY2018/FY2019 use the 'IFRS9 Transitional arrangements "
         "applied' column, same convention as the CET1 Capital sheet).",
)

metric(
    "LCR", "£m / %",
    [
        ("Total high-quality liquid assets (HQLA), weighted value - average (£m)", {"FY2024": 854.893, "FY2023": 699.862, "FY2020": 362.315, "FY2019": 634.602, "FY2018": 566.611, "FY2017": 1002.101}),
        ("Total net cash outflows, adjusted value (£m)", {"FY2024": 252.133, "FY2023": 189.675, "FY2020": 127.560, "FY2019": 168.941, "FY2018": 192.084, "FY2017": 405.144}),
        ("Liquidity Coverage Ratio (%)", {"FY2024": "339.1%", "FY2023": "369.0%", "FY2020": "281%", "FY2019": "391%", "FY2018": "325%", "FY2017": "281%"}),
    ],
    p3_sources(),
    note="FY2023 LCR is sourced from the FY2024 Pillar 3 Report's comparative column - ABCIB's own FY2023 Pillar 3 "
         "Disclosures document (Table 3) does not include LCR at all (only capital and leverage metrics). "
         "FY2022/FY2021/FY2025/FY2014-FY2016 not available. FY2017-FY2020 are from each year's dedicated Pillar 3 "
         "report (solo basis).",
)

metric(
    "NSFR", "£m / %",
    [
        ("Total available stable funding (£m)", {"FY2024": 2339.367, "FY2023": 2053.004}),
        ("Total required stable funding (£m)", {"FY2024": 1802.627, "FY2023": 1504.583}),
        ("Net Stable Funding Ratio (%)", {"FY2024": "129.8%", "FY2023": "136.4%"}),
    ],
    p3_sources(),
    note="FY2023 NSFR is sourced from the FY2024 Pillar 3 Report's comparative column - same reason as the LCR "
         "sheet. Every other year (FY2014-FY2022, FY2025) not available - NSFR is discussed only in qualitative/"
         "narrative terms (e.g. 'well on the way to becoming fully compliant') in ABCIB's FY2016-FY2020 Pillar 3 "
         "reports, never disclosed as a figure.",
)

metric(
    "MREL Ratio", "£m / %",
    [("MREL ratio", {y: "Not publicly disclosed" for y in YEARS})],
    p3_sources(),
    note="No MREL figure (numeric or qualitative) appears in any Pillar 3 Report reviewed for this entity across "
         "FY2014-FY2025 - no reason is stated. ABCIB's balance sheet size (~£2.7-4.3bn across this whole period) "
         "is well below the thresholds at which the Bank of England typically sets an independent MREL "
         "requirement, consistent with no disclosure existing.",
)

# ---------------------------------------------------------------
# Overview sheet (Pillar-3-only: no cash-flow chart)
# ---------------------------------------------------------------
bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {"FY2025": 3628416, "FY2024": 3487130, "FY2023": 3197291, "FY2022": 3150890, "FY2021": 2805879, "FY2020": 2731397, "FY2019": 3027686, "FY2018": 3696138, "FY2017": 2932134, "FY2016": 3689507, "FY2015": 2834515, "FY2014": 2696707}),
        ("Loans and advances to customers", {"FY2025": 1540521, "FY2024": 1368632, "FY2023": 1290334, "FY2022": 1101772, "FY2021": 1094131, "FY2020": 1105423, "FY2019": 1435262, "FY2018": 1414678, "FY2017": 1121735, "FY2016": 909592, "FY2015": 983414, "FY2014": 1170920}),
        ("Customer deposits", {"FY2025": 796992, "FY2024": 588657, "FY2023": 460063, "FY2022": 517193, "FY2021": 238737, "FY2020": 224299, "FY2019": 243923, "FY2018": 432416, "FY2017": 399274, "FY2016": 267883, "FY2015": 235152, "FY2014": 196351}),
        ("Total equity", {"FY2025": 601054, "FY2024": 586474, "FY2023": 568132, "FY2022": 543701, "FY2021": 534131, "FY2020": 501167, "FY2019": 496862, "FY2018": 487536, "FY2017": 469692, "FY2016": 449727, "FY2015": 441996, "FY2014": 427294}),
    ],
    balance_sheet_unit="£'000",
    income_statement_totals=[
        ("Profit for the year attributable to owners", {"FY2025": 32616, "FY2024": 34113, "FY2023": 28022, "FY2022": 22069, "FY2021": 25344, "FY2020": 8001, "FY2019": 16031, "FY2018": 23085, "FY2017": 18521, "FY2016": 16227, "FY2015": 14025, "FY2014": 23684}),
        ("Total comprehensive income for the year", {"FY2025": 31680, "FY2024": 34148, "FY2023": 31051, "FY2022": 16840, "FY2021": 30974, "FY2020": 4305, "FY2019": 15096, "FY2018": 24393, "FY2017": 19965, "FY2016": 7731, "FY2015": 14702, "FY2014": 20232}),
    ],
    income_statement_unit="£'000",
    equity_changes_totals=[
        ("Opening equity", {"FY2025": 586474, "FY2024": 568132, "FY2023": 543701, "FY2022": 534131, "FY2021": 503157, "FY2020": 496862, "FY2019": 487536, "FY2018": 469692, "FY2017": 449727, "FY2016": 441996, "FY2015": 427294, "FY2014": 407062}),
        ("Total comprehensive income for the year", {"FY2025": 31680, "FY2024": 34148, "FY2023": 31051, "FY2022": 16840, "FY2021": 30974, "FY2020": 4305, "FY2019": 15096, "FY2018": 24393, "FY2017": 19965, "FY2016": 7731, "FY2015": 14702, "FY2014": 20232}),
        ("Other equity movements, net (dividends)", {"FY2025": -17100, "FY2024": -15806, "FY2023": -6620, "FY2022": -7270, "FY2021": 0, "FY2020": 0, "FY2019": -5770, "FY2018": -6549, "FY2017": 0, "FY2016": 0, "FY2015": 0, "FY2014": 0}),
        ("Closing equity", {"FY2025": 601054, "FY2024": 586474, "FY2023": 568132, "FY2022": 543701, "FY2021": 534131, "FY2020": 501167, "FY2019": 496862, "FY2018": 487536, "FY2017": 469692, "FY2016": 449727, "FY2015": 441996, "FY2014": 427294}),
    ],
    equity_changes_unit="£'000",
    cash_flow_totals=[],
    cash_flow_unit=None,
    ratios=[
        ("CET1 Ratio", {"FY2025": "15.0%", "FY2024": "16.2%", "FY2023": "17.6%", "FY2022": "17.0%", "FY2021": "16.7%", "FY2020": "16.4%", "FY2019": "17.5%", "FY2018": "16.6%", "FY2017": "18.2%", "FY2016": "19.2%", "FY2015": "20.4%", "FY2014": "22.0%"}),
        ("Tier 1 Ratio", {"FY2025": "15.0%", "FY2024": "16.2%", "FY2023": "17.6%", "FY2022": "17.0%", "FY2021": "16.7%", "FY2020": "16.4%", "FY2019": "17.5%", "FY2018": "16.6%", "FY2017": "18.2%", "FY2016": "19.2%", "FY2015": "20.4%", "FY2014": "22.0%"}),
        ("Total Capital Ratio", {"FY2025": "16.5%", "FY2024": "17.7%", "FY2023": "19.3%", "FY2022": "18.2%", "FY2021": "18.3%", "FY2020": "18.5%", "FY2019": "19.3%", "FY2018": "18.3%", "FY2017": "20.4%", "FY2016": "21.5%", "FY2015": "22.9%", "FY2014": "22.1%"}),
        ("Leverage Ratio (excl. central bank claims)", {"FY2024": "10.2%", "FY2023": "10.62%", "FY2020": "13.39%", "FY2019": "13.45%", "FY2018": "10.28%", "FY2017": "12.59%"}),
        ("LCR", {"FY2024": "339.1%", "FY2023": "369.0%", "FY2020": "281%", "FY2019": "391%", "FY2018": "325%", "FY2017": "281%"}),
        ("NSFR", {"FY2024": "129.8%", "FY2023": "136.4%"}),
    ],
    note="ABC International Bank plc takes the FRS 101 cash-flow-statement exemption every year (see the Cash Flow "
         "Statement sheet), so no cash flow summary or chart is shown here - only the Balance Sheet / P&L / Equity "
         "blocks (all entity/solo basis) and the Pillar 3 Key Metrics trend chart below. Pillar 3 ratios are "
         "consolidated basis for FY2023-FY2024 and solo basis for every other year - a different basis to the "
         "statement blocks above, see the Cash Flow Statement sheet's entity note. FY2025's statement/asset-"
         "quality figures were transcribed from a scanned Companies House filing via visual reading (OCR-style); "
         "FY2025 Leverage Ratio/LCR/NSFR remain unavailable (not in the Annual Report's Financial Highlights "
         "table, and no separate FY2025 Pillar 3 report could be located) - see each sheet's own source citation. "
         "HD-018 extended this workbook's window from FY2021-FY2025 back to FY2014-FY2025 (2026-09-05); FY2018's "
         "'Other equity movements' figure (-£6,549k) is the IFRS 9 transition adjustment recognised on 1 January "
         "2018, not a dividend - see the Statement of Changes in Equity sheet.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/ABC INTERNATIONAL BANK FINANCIALS.xlsx")
