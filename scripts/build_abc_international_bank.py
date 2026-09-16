import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

# PILLAR-3-ONLY WORKBOOK: ABC International Bank plc (company 02564490, FRN 149025)
# is a qualifying entity under FRS 101 and takes the "requirements of IAS 7 Statement
# of Cash Flows" exemption every year - explicitly stated in note 1.2 of its FY2024
# Annual Report: "there is no requirement to prepare a statement of cash flows in
# accordance with Financial Reporting Standard 101." No Statement of Cash Flows
# exists in any year's accounts. Pillar 3 / capital disclosures are available for all
# 12 years. FY2025 is sourced from the ABCIB Pillar 3 Report 2025 on the CONSOLIDATED
# basis (restated from solo on 2026-09-15 - see BASIS_NOTE), and FY2021/FY2022 from
# each year's own dedicated Pillar 3 report (located 2026-09-15; an earlier pass had
# wrongly recorded those as non-existent and used the Annual Report Financial
# Highlights table instead). This follows the BNY Mellon International precedent: standard 13-sheet
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
# NOTE ON FINDING THIS FILE: the FY2025 edition abandons every previous naming
# convention ("Bank-ABC-IB-Pillar-Report-2025.pdf", dropping both the "ABCIB"
# prefix and the "3" from "Pillar 3"), so no filename permutation of the FY2024
# URL locates it. It is linked only from the disclosures index at
# https://www.bank-abc.com/en/CountrySites/Europe/London/Financial-Info/basel-pillar-3-disclosures
# (note: the older .../Pages/Basel-Pillar-3-Disclosure.aspx path now 404s).
P3_2025_URL = "https://www.bank-abc.com/en/CountrySites/Europe/London/Financial-Info/Basel%20Pillars/Bank-ABC-IB-Pillar-Report-2025.pdf"
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

# FY2021/FY2022 dedicated Pillar 3 reports, located 2026-09-15 on the disclosures
# index. An earlier pass recorded these years as having "no Pillar 3 document" and
# sourced them from the Annual Report's Financial Highlights table instead; that was
# wrong. Both documents exist, have a real text layer, and print a two-column
# "Solo | Consolidated" Key Regulatory Metrics table (NOT a year-comparative table -
# the single date column is Dec-21 / Dec-22 respectively). The Solo column is used
# here, matching the basis of every other FY2014-FY2022 year in this workbook, and
# its Tier 1 / Total capital ratios reproduce the existing Financial-Highlights
# figures exactly (FY2021 16.7%/18.3%, FY2022 17.0%/18.2%) - the validation gate
# that confirms the two sources describe the same basis.
P3_2021_URL = "https://www.bank-abc.com/en/CountrySites/Europe/London/Financial-Info/Basel%20Pillars/ABCIB-Pillar3Disclosure-2021.pdf"
P3_2022_URL = "https://www.bank-abc.com/en/CountrySites/Europe/London/Financial-Info/Basel%20Pillars/ABCIB-Pillar3Disclosure-2022.pdf"
P3_2020_URL = "https://www.bank-abc.com/en/CountrySites/Europe/London/Financial-Info/Basel%20Pillars/ABCIB-Pillar3Disclosure-2020.pdf"
P3_2019_URL = "https://www.bank-abc.com/en/CountrySites/Europe/London/Financial-Info/Basel%20Pillars/ABCIB-Pillar3Disclosure2019-postBRC.pdf"
P3_2017_URL = "https://www.bank-abc.com/en/CountrySites/Europe/London/Financial-Info/Basel%20Pillars/Pillar-3-Disclosure-2018.pdf"  # filename says "2018" but the document's own title page and content are "Pillar 3 Report 2017" (FY2017 figures) - confirmed by opening it, not a mistaken re-use of the FY2018 file (a separate Pillar-3-Disclosure_2018.pdf exists with FY2018 figures, cited as P3_2018_URL)
P3_2018_URL = "https://www.bank-abc.com/en/CountrySites/Europe/London/Financial-Info/Basel%20Pillars/Pillar-3-Disclosure_2018.pdf"

ENTITY_NOTE = (
    "ENTITY NOTE: ABC International Bank plc (company 02564490, FRN 149025, incorporated 3 December 1990) is a "
    "wholly-owned subsidiary within the Bank ABC (Arab Banking Corporation B.S.C., Bahrain) group. FY2023, FY2024 "
    "and FY2025 figures are on a CONSOLIDATED basis (ABCIB's own subsidiaries, e.g. Alphabet Nominees Limited - a "
    "nominee company, not a trading entity). FY2014-FY2022 are on a SOLO (entity-only) basis. This is a genuine "
    "basis break within the series, not a data-entry choice - flagged on every affected sheet.\n\n"
    "TWO CLAIMS CORRECTED HERE (2026-09-16), both of which had been recorded more confidently than their evidence "
    "supported. (1) This note previously said the UK KM1 template was 'introduced for the FY2023 report onward'. It "
    "was not: the FY2023 edition prints a 10-row 'Table 3 Key Regulatory Metrics' summary and contains no "
    "occurrence of 'KM1' or 'SREP' anywhere. ABCIB first published the template in its Pillar 3 Report 2024, and "
    "FY2023's consolidated figures come from that 2023 Table 3, not from a KM1. (2) This note previously said "
    "FY2021/FY2022 were taken from the Annual Report's Financial Highlights because 'earlier years' Pillar 3 "
    "documents could not be located on the bank's website or via Wayback Machine'. Both documents do exist on the "
    "disclosures index and were located on 2026-09-15 (see P3_2021_URL / P3_2022_URL); those two years are now "
    "sourced from their own Pillar 3 reports. A document that a fetch failed to reach is not a document that does "
    "not exist, and the original wording did not preserve that distinction."
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
    "FY2023-FY2025 shown on a CONSOLIDATED basis (ABCIB Pillar 3 Disclosures, UK KM1 template); FY2014-FY2022 on "
    "a SOLO basis - FY2017-FY2022 from ABCIB's own dedicated Pillar 3 report for each year (which itself states "
    "its basis explicitly; the FY2020/FY2021/FY2022 reports carry a Consolidated column alongside Solo, and the "
    "Solo column is used throughout for continuity with the other years), FY2014-FY2016 from the Annual Report's "
    "own Financial Highlights table (no Pillar 3 report exists for those years). See the Cash Flow Statement "
    "sheet's entity note for detail.\n\n"
    "FY2025 BASIS RESTATEMENT (2026-09-15): FY2025's capital sheets originally used the Annual Report's solo "
    "Financial Highlights table (Total RWA £3,132m, Capital base £517m, Tier 1 ratio 15.0%, Total ratio 16.5%), "
    "which left the FY2025 column internally mixed once the Pillar 3 Report 2025 supplied consolidated "
    "leverage/LCR/NSFR. On the user's explicit instruction the whole FY2025 column was moved onto the "
    "CONSOLIDATED basis (CET1/Tier 1 £579.993m, Total capital £628.255m, RWAs £3,880.104m, CET1/Tier 1 ratio "
    "14.9%, total capital ratio 16.2%), giving a clean consolidated run FY2023-FY2025. The superseded solo "
    "figures are preserved: quoted in each capital sheet's note, and kept as a full risk-type split in the RWA "
    "Breakdown sheet's SOLO block. Note this removes a presentational artefact - the old mixed column made RWAs "
    "appear to FALL from FY2024 to FY2025, whereas like-for-like they rose.\n\n"
    "FY2021/FY2022 SOURCE CORRECTION (2026-09-15): an earlier pass recorded these years as having no Pillar 3 "
    "document and sourced them from the Annual Report Financial Highlights table. That was wrong - "
    "ABCIB-Pillar3Disclosure-2021.pdf and -2022.pdf both exist on the disclosures index. Mining them added "
    "Leverage Ratio and LCR for both years and NSFR for FY2022, and upgraded CET1/Tier 1 capital from CALCULATED "
    "(RWA x Tier 1 ratio) to DIRECTLY DISCLOSED. Their ratio columns reproduce the previously-held Financial "
    "Highlights figures exactly, confirming the two sources share a basis. CET1/Tier 1 capital £m remain "
    "CALCULATED only for FY2014-FY2016, whose Financial Highlights tables do not split CET1 from Tier 1 - see "
    "the CET1 Capital sheet note.\n\n"
    "No Leverage Ratio or LCR figure is available for FY2014-FY2016 (no Pillar 3 report exists and the Financial "
    "Highlights table carries neither metric). NSFR is disclosed from FY2022 onward only; FY2021 and earlier are "
    "structurally absent because the UK had no NSFR requirement or disclosure template before 1 January 2022 "
    "(PRA PS17/21 / PS22/21) - see the NSFR sheet note. MREL is not disclosed in any year.\n\n"
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
        f"FY2022 (solo): ABC International Bank plc Pillar 3 Disclosures 2022, Table 3 'Key Regulatory Metrics' "
        f"(Solo column), Table 17 'LCR components (Average)' and Table 18 'NSFR components (Average)' - "
        f"{P3_2022_URL}\n"
        f"FY2021 (solo): ABC International Bank plc Pillar 3 disclosures 2021, Table 3 'Key Regulatory Metrics' "
        f"(Solo column), p.8, Table 6 'RWAs and Capital ratio', p.10, and Table 17 'LCR components (Average)', "
        f"p.17 - {P3_2021_URL}\n"
        f"FY2022 & FY2021 (solo, Total Capital/RWA cross-check only): ABC International Bank plc Annual Report "
        f"2022, Financial Highlights, p.31 - {AR2022_URL}\n"
        f"FY2025 (CONSOLIDATED - all capital, RWA, leverage, LCR and NSFR sheets): ABC International Bank plc "
        f"Pillar 3 Report 2025, Table 3 'Key Regulatory Metrics', 'ABCIB CONSOLIDATED' UK KM1 table, p.16, and "
        f"'ABCIB CONSOLIDATED' UK OV1 table, p.17 - {P3_2025_URL}\n"
        f"FY2024 (consolidated): as the FY2025 report's own comparative column (validation gate - reproduces this "
        f"workbook's existing FY2024 figures exactly) - {P3_2025_URL}\n"
        f"FY2025 (solo - superseded 2026-09-15, retained in the RWA Breakdown sheet's SOLO block and quoted in "
        f"each capital sheet's note): ABC International Bank plc Pillar 3 Report 2025, 'ABCIB SOLO' UK KM1 table, "
        f"p.15, and 'ABCIB SOLO' UK OV1 table, p.17 - {P3_2025_URL}; ABC International Bank plc Annual Report "
        f"2025, Financial Highlights, p.20 (scanned Companies House filing, visually transcribed) - "
        f"{AR2025_URL}\n"
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
    "Sources - ABC International Bank plc:\n"
    f"FY2025 (CONSOLIDATED basis, matching the Total RWAs sheet's restated FY2025 figure of 3,880,104; added "
    f"2026-09-15): ABC International Bank plc Pillar 3 Report 2025, Table \"UK OV1 - Overview of risk weighted "
    f"exposure amounts\", ABCIB CONSOLIDATED, p.17 - {P3_2025_URL}\n"
    f"FY2024 & FY2023 (CONSOLIDATED basis, matching the Total RWAs sheet's FY2024/FY2023 figures; FY2023 as "
    f"originally reported by the FY2024 report's own comparative column - no separate OV1 breakdown exists in "
    f"ABCIB's own FY2023 Pillar 3 Disclosures document, which only carries Table 3's single Total RWA figure, not "
    f"a category breakdown): ABC International Bank plc Pillar 3 Report 2024, Table \"UK OV1 - Overview of risk "
    f"weighted exposure amounts\", ABCIB CONSOLIDATED, p.14 - {P3_2024_URL}\n"
    f"NOTE ON THE 'Of which: CVA' ROW: the UK OV1 template labels CVA as an 'of which' subset of counterparty "
    f"credit risk, and this sheet copies that label verbatim, but in ABCIB's own tables the CVA figure is "
    f"ADDITIVE, not a subset - FY2025 consolidated foots only as 3,554,768 + 45,144 + 13,124 + 23,741 + 243,327 "
    f"= 3,880,104, and FY2024 likewise needs its 10,131 CVA added to reach 3,486,256. The source's label is "
    f"therefore internally inconsistent with its own arithmetic; the figures are transcribed as printed and each "
    f"block's TOTAL row is the document's own stated total, so no derived value is affected.\n"
    f"FY2025 (SOLO basis - SUPERSEDED as the Total RWAs sheet's basis on 2026-09-15 but retained here so the solo "
    f"split stays legible), FY2022 & FY2021 (SOLO basis, matching the Total RWAs sheet's own figures for those "
    f"years - a "
    f"coarser 3-category split than the OV1 template above, not a separate CCR/CVA breakout; DIRECTLY DISCLOSED "
    f"as risk-weighted assets, not derived): ABC International Bank plc Annual Report 2025, Note 26 'Regulatory "
    f"capital', 'Risk-weighted assets (unaudited)' table, p.66 (scanned Companies House filing, visually "
    f"transcribed) - {AR2025_URL}; ABC International Bank plc Annual Report 2022, Note 25 'Regulatory capital', "
    f"'Risk-weighted assets (unaudited)' table, p.66 - {AR2022_URL}. The FY2025 solo split also appears as a "
    f"true UK OV1 table in the Pillar 3 Report 2025 ('ABCIB SOLO', p.17: credit 2,862,420 + CCR 47,494 + CVA "
    f"13,252 + market 24,739 + operational 183,713 = 3,131,618), which reconciles exactly to the Annual Report's "
    f"coarser 3-category figures used here - {P3_2025_URL}\n"
    f"FY2020, FY2019, FY2018 & FY2017 (SOLO basis, matching the Total RWAs sheet's own figures for those years - "
    f"DERIVED, not directly disclosed as RWA: each dedicated Pillar 3 report only discloses the Pillar 1 MINIMUM "
    f"CAPITAL REQUIREMENT by risk type, i.e. 8% of RWA per CRR Article 92 - so each category figure below is that "
    f"report's own capital-requirement figure divided by 8% (multiplied by 12.5), the standard, exact Basel/CRR "
    f"identity, not an estimate. Verified against each year's own Total RWA figure (already in the Total RWAs "
    f"sheet) to within a few £'000 - the residual gap is the source table's own £'000 rounding of the capital-"
    f"requirement figures before this multiplication, not a data-quality issue here. FY2020's report additionally "
    f"discloses a Consolidated column alongside Solo - Solo is used throughout for continuity with every other "
    f"year, per the Total RWAs sheet's own basis note): ABC International Bank plc Pillar 3 Disclosures 2020, "
    f"Table 5 'Pillar 1 Capital Requirements', p.10 - {P3_2020_URL}; ABC International Bank plc Pillar 3 "
    f"Disclosures 2019, Table 4 'Pillar 1 Capital Requirements', p.10 - {P3_2019_URL}; ABC International Bank plc "
    f"Pillar 3 Report 2018, Table 4 'Pillar 1 Capital Requirements', p.10 - {P3_2018_URL}; ABC International Bank "
    f"plc Pillar 3 Report 2017, Table 3 'Pillar 1 Capital Requirements', p.9 - {P3_2017_URL}\n"
    "FY2014-FY2016: not available in the credit/market/operational risk-TYPE split used above. Their Annual "
    "Reports' own 'Regulatory capital'/'Called up share capital' notes DO carry a risk-weighted-assets breakdown "
    "(checked directly), but only by BOOK type (Banking book / Trading book) - a different, non-comparable "
    "dimension to the risk-type categories used in every other year on this sheet, so deliberately not added "
    "here rather than mixed in under misleading category labels. No FY2014-FY2016 ABCIB-entity Pillar 3 document "
    "could be located at all (see p3_sources note)."
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


# ---------------------------------------------------------------
# Sheet: KM1 Key Metrics (KM1-003)
# ---------------------------------------------------------------
# WHY ONLY TWO YEARS CARRY A COLUMN.
# ABCIB printed the UK KM1 template for the FIRST time in its Pillar 3 Report
# 2024. The 2023, 2022 and 2021 editions each print "Table 3 Key Regulatory
# Metrics" instead: a 10-row Solo|Consolidated summary at a SINGLE date
# (Dec-23 / Dec-22 / Dec-21), with no SREP rows, no buffer rows, no LCR and no
# NSFR, captioning leverage as "Total Leverage ratio exposure measure" rather
# than "...excluding claims on central banks". The 2023 document contains ZERO
# occurrences of "KM1" and zero of "SREP" - re-read in full on 2026-09-16.
#
# That is NOT the same thing as a bank printing the template without numbering
# it (map rule KM1-004(a) - Aldermore, Allica, Europe Arab Bank), which is why
# those banks get full columns and these years do not. The test is the ROW SET,
# not the "KM1" token: an unnumbered table carrying the template's own row set
# is the template; a 10-row summary is a different table, and mapping it onto
# template row numbers would invent a correspondence the bank never published.
#
# FY2023 is therefore BLANK here and is NOT filled from the FY2024 edition's
# comparative column (map rule 1). Those figures are not lost - they are on the
# single-metric sheets, captioned and sourced as that year's own edition printed
# them. The two sources genuinely disagree, which is why the rule exists: the
# FY2023 edition prints consolidated RWAs of 3,104,763 while the FY2024
# edition's FY2023 comparative prints 3,101,197.
#
# ENTITY: both columns are ABCIB CONSOLIDATED. Each edition prints the template
# TWICE - once "ABCIB SOLO", once "ABCIB CONSOLIDATED" - so the entity call is
# made INSIDE one document, and taking the first table encountered would put
# solo figures into a consolidated series. Consolidated is used because this
# workbook runs FY2023-FY2025 on that basis (BASIS_NOTE); the solo table gives
# materially different figures (FY2025 CET1 469,209 against 579,993). ABCIB
# CONSOLIDATED is the UK entity's OWN consolidation (its own subsidiaries, e.g.
# Alphabet Nominees Limited), never the Bahraini parent's group consolidation.
#
# CROSS-EDITION CHECK (map rule 6): every one of the 26 rows in the FY2024
# column was read from the FY2024 edition's own consolidated table and
# independently reproduces the FY2025 edition's FY2024 comparative column
# exactly. Amounts are in £'000 as published - this sheet is NOT converted to
# the £m used by the single-metric sheets.
km1_rows = [
    ("SECTION", "Available own funds (amounts)", {}),
    ("DATA", "1  Common Equity Tier 1 (CET1) capital (£'000)", {"FY2025": 579993, "FY2024": 564579}),
    ("DATA", "2  Tier 1 capital (£'000)", {"FY2025": 579993, "FY2024": 564579}),
    ("DATA", "3  Total capital (£'000)", {"FY2025": 628255, "FY2024": 616448}),
    ("SECTION", "Risk-weighted exposure amounts", {}),
    ("DATA", "4  Total risk-weighted exposure amount (£'000)", {"FY2025": 3880104, "FY2024": 3486256}),
    ("SECTION", "Capital ratios (as a percentage of risk-weighted exposure amount)", {}),
    ("DATA", "5  Common Equity Tier 1 ratio (%)", {"FY2025": "14.9%", "FY2024": "16.2%"}),
    ("DATA", "6  Tier 1 ratio (%)", {"FY2025": "14.9%", "FY2024": "16.2%"}),
    ("DATA", "7  Total capital ratio (%)", {"FY2025": "16.2%", "FY2024": "17.7%"}),
    ("SECTION", "Additional own funds requirements based on SREP (as a percentage of risk-weighted exposure amount)", {}),
    ("DATA", "UK 7a  Additional CET1 SREP requirements (%)", {"FY2025": "2.1%", "FY2024": "2.1%"}),
    ("DATA", "UK 7b  Additional AT1 SREP requirements (%)", {"FY2025": "0.0%", "FY2024": "0.0%"}),
    ("DATA", "UK 7c  Additional T2 SREP requirements (%)", {"FY2025": "0.0%", "FY2024": "0.0%"}),
    ("DATA", "UK 7d  Total SREP own funds requirements (%)", {"FY2025": "10.1%", "FY2024": "10.1%"}),
    ("SECTION", "Combined buffer requirement (as a percentage of risk-weighted exposure amount)", {}),
    ("DATA", "8  Capital conservation buffer (%)", {"FY2025": "2.5%", "FY2024": "2.5%"}),
    ("DATA", "9  Institution specific countercyclical capital buffer (%)", {"FY2025": "0.6%", "FY2024": "0.7%"}),
    ("DATA", "11  Combined buffer requirement (%)", {"FY2025": "3.1%", "FY2024": "3.2%"}),
    ("DATA", "UK 11a  Overall capital requirements (%)", {"FY2025": "13.2%", "FY2024": "13.3%"}),
    ("DATA", "12  CET1 available after meeting the total SREP own funds requirements (%)",
     {"FY2025": "4.8%", "FY2024": "6.0%"}),
    ("SECTION", "Leverage ratio", {}),
    ("DATA", "13  Total exposure measure excluding claims on central banks (£'000)",
     {"FY2025": 5990509, "FY2024": 5540164}),
    ("DATA", "14  Leverage ratio excluding claims on central banks (%)", {"FY2025": "9.7%", "FY2024": "10.2%"}),
    ("SECTION", "Liquidity Coverage Ratio", {}),
    ("DATA", "15  Total high-quality liquid assets (HQLA) (Weighted value - average) (£'000)",
     {"FY2025": 748628, "FY2024": 854893}),
    ("DATA", "UK 16a  Cash outflows - Total weighted value (£'000)", {"FY2025": 878001, "FY2024": 839225}),
    ("DATA", "UK 16b  Cash inflows - Total weighted value (£'000)", {"FY2025": 578631, "FY2024": 587092}),
    ("DATA", "16  Total net cash outflows (adjusted value) (£'000)", {"FY2025": 299370, "FY2024": 252133}),
    ("DATA", "17  Liquidity coverage ratio (%)", {"FY2025": "250.1%", "FY2024": "339.1%"}),
    ("SECTION", "Net Stable Funding Ratio", {}),
    ("DATA", "18  Total available stable funding (£'000)", {"FY2025": 2391315, "FY2024": 2339367}),
    ("DATA", "19  Total required stable funding (£'000)", {"FY2025": 1902311, "FY2024": 1802627}),
    ("DATA", "20  NSFR ratio (%)", {"FY2025": "125.7%", "FY2024": "129.8%"}),
]

KM1_SOURCES = (
    "Sources - the 'ABCIB CONSOLIDATED' UK KM1 table in each year's OWN Pillar 3 edition. Every edition prints "
    "this template twice, once for ABCIB SOLO and once for ABCIB CONSOLIDATED; the consolidated table is used "
    "here, matching this workbook's FY2023-FY2025 basis (see the Cash Flow Statement sheet's entity note). "
    "ABCIB CONSOLIDATED is ABC International Bank plc's own consolidation of its own subsidiaries - it is NOT "
    "the Bahraini parent group's consolidation. Amounts are in £'000 exactly as published, not converted to the "
    "£m used by the single-metric sheets.\n"
    f"FY2025: ABC International Bank plc Pillar 3 Report 2025, p.16, Table 3 'Key Regulatory Metrics', "
    f"'ABCIB CONSOLIDATED' UK KM1 - Key metrics template, 2025 column - {P3_2025_URL}\n"
    f"FY2024: ABC International Bank plc Pillar 3 Report 2024, p.14, Table 3 'Key Regulatory Metrics', "
    f"'ABCIB CONSOLIDATED' UK KM1 - Key metrics template, 2024 column - {P3_2024_URL}\n"
    "\n"
    "WHY FY2023, FY2022 AND FY2021 ARE BLANK - NOT DISCLOSED, NOT 'NOT FOUND'.\n"
    "ABCIB first published the UK KM1 template in its Pillar 3 Report 2024. The 2023, 2022 and 2021 editions "
    "each print 'Table 3 Key Regulatory Metrics' instead: a 10-row Solo|Consolidated summary at a single date, "
    "carrying capital, RWAs, two ratios and leverage only - no SREP rows, no buffer rows, no LCR and no NSFR - "
    "and captioning leverage as 'Total Leverage ratio exposure measure' rather than '...excluding claims on "
    "central banks'. The 2023 document was re-read in full on 2026-09-16 and contains no occurrence of 'KM1' "
    "or 'SREP' anywhere. A 10-row summary is a different table from the 26-row template, so its figures are "
    "not mapped onto template row numbers here; they appear on the single-metric sheets instead, captioned as "
    "their own edition printed them.\n"
    "A full FY2023 KM1 column DOES exist - as the FY2024 edition's comparative - and is deliberately not used, "
    "because each column on this sheet comes from the edition in which that year is the reporting year. The "
    "two sources disagree, which is precisely why: the FY2023 edition prints consolidated RWAs of 3,104,763 "
    "while the FY2024 edition's FY2023 comparative prints 3,101,197.\n"
    "\n"
    "SOURCE DEFECT, REPRODUCED AND FLAGGED RATHER THAN CORRECTED.\n"
    "Row 3 of the FY2025 consolidated table prints total capital as '628.255' - a DECIMAL POINT where the "
    "thousands separator belongs, while every other figure in the same column uses a comma. It is carried here "
    "as 628,255 £'000: the printed digits are unchanged and only the separator is wrong. This is corroborated "
    "inside the same document rather than derived - 'Table 2 Regulatory Capital' on the preceding page prints "
    "total regulatory capital of 628,255 for the consolidated basis. A literal 628.255 (£628k) would sit below "
    "that table's own CET1 of £580m.\n"
    "\n"
    "LABEL DRIFT: the FY2024 edition captions row 12 'CET1 available after meeting the total SREP own funds "
    "requirements (%)'; the FY2025 edition drops the '(%)'. The FY2024 wording is used for the row label and "
    "both years' figures are percentages as printed.\n"
    "\n"
    "CROSS-EDITION VALIDATION (map rule 6): all 26 rows of the FY2024 column were taken from the FY2024 "
    "edition's own consolidated table and independently reproduce the FY2025 edition's FY2024 comparative "
    "column exactly, which is what confirms both columns are on the consolidated basis and not the solo one.\n"
    "\n"
    "UNIT IS £'000 AS PUBLISHED, WHILE THE SINGLE-METRIC SHEETS ARE £m.\n"
    "ABCIB publishes this template in £'000, so it is reproduced in £'000, matching the RWA Breakdown sheet in "
    "this same workbook. The eleven single-metric Pillar 3 sheets are in £m. The two are therefore the same "
    "figures at a different scale - 579,993 here against 579.993 there, 564,579 against 564.579, 628,255 "
    "against 628.255, 3,880,104 against 3,880.104 - identical digits, factor of 1,000, no digit slip anywhere. "
    "Each row label on this sheet carries its own unit token ((£'000) on amount rows, (%) on ratio rows), which "
    "is how the cross-check resolves the scale: a KM1 sheet cannot declare one sheet-level unit, because the "
    "map requires it to mix £'000 amounts and % ratios down a single column.\n"
    "HISTORY, so the earlier note is not mistaken for a live defect: until 2026-09-16 "
    "scripts/verify_workbook.py inferred scale from the COLUMN HEADER only, and neither this sheet's headers "
    "('FY2025') nor a metric sheet's carries a unit token, so both sides were read as scale 1 and compared raw "
    "- which made rows 1-4 report as disagreeing in both years. That was a gap in the checker, not in these "
    "figures. It was fixed the same day (_unit_scale() now returns None rather than 1.0 when a label carries no "
    "unit, with _km1_row_scale() preferring the ROW LABEL, then the header, then the sheet), and this workbook "
    "now cross-checks 20 of 20 KM1 cells clean. Do not rescale these cells to £m: they are right as printed, "
    "and this sheet is deliberately not normalised away from the unit the bank published.\n"
    "\n"
    "LATEST-EDITION CHECK: ABCIB's own disclosures index "
    "(https://www.bank-abc.com/en/CountrySites/Europe/London/Financial-Info/Basel Pillars/) checked 2026-09-16 "
    "- newest Pillar 3 is the Pillar 3 Report 2025 (year ended 31 December 2025), already carried here and "
    "already cited by this script. None newer."
)

bw.add_km1_sheet(
    title="ABC International Bank plc - KM1 Key Metrics",
    subtitle="The 'ABCIB CONSOLIDATED' UK KM1 - Key metrics template, reproduced in the bank's own row order, "
             "row numbers, labels and precision. Amounts in £'000 as published; ratios as printed. FY2023 and "
             "earlier are blank because ABCIB did not publish this template before its FY2024 report - see the "
             "sources note, which also records a printed-separator defect in FY2025 row 3.",
    rows=km1_rows,
    sources_text=KM1_SOURCES,
    first_col_width=64,
    source_height=300,
    years=["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"],
)

metric(
    "CET1 Capital", "£m",
    [("Common Equity Tier 1 (CET1) capital", {"FY2025": 579.993, "FY2024": 564.579, "FY2023": 547.665, "FY2022": 416.914, "FY2021": 419.517, "FY2020": 393.198, "FY2019": 495.422, "FY2018": 487.265, "FY2017": 469.029, "FY2016": 449.664, "FY2015": 439.008, "FY2014": 421.08})],
    p3_sources(),
    note="FY2025 RESTATED 2026-09-15 from SOLO to CONSOLIDATED basis (469.8 -> 579.993), on the user's explicit "
         "instruction, so that the whole FY2025 column sits on one basis: its Leverage/LCR/NSFR rows were already "
         "consolidated, while the capital rows were still solo. Superseded solo value: 469.8 (itself calculated as "
         "RWA x Tier 1 ratio); the Pillar 3 Report 2025's own SOLO column gives a directly-disclosed 469.209. "
         "Now directly disclosed, not calculated - ABCIB CONSOLIDATED UK KM1 row 1, p.16. FY2022/FY2021 UPGRADED "
         "2026-09-15 from calculated to DIRECTLY DISCLOSED (416.5 -> 416.914, 418.8 -> 419.517) using each year's "
         "own dedicated Pillar 3 report (solo column), located that day - see P3_2021_URL/P3_2022_URL. "
         "FY2016/FY2015/FY2014 remain calculated (RWA x Tier 1 ratio, solo basis) - no separate CET1/Tier 1 £m "
         "figure is disclosed for those years, only the ratio and total 'Capital base'. Assumes CET1 = Tier 1 (no "
         "AT1 instruments in issue), consistent with the pattern directly confirmed in every FY2017-FY2025 Pillar "
         "3 report reviewed. FY2017-FY2020 are directly disclosed (Appendix 2 Own Funds / Table 3 Key Regulatory "
         "Metrics of each year's dedicated Pillar 3 report); FY2018/FY2019 use the 'IFRS9 Transitional "
         "arrangements applied' column for continuity with FY2020's single reported figure.",
)

metric(
    "CET1 Ratio", "% of RWA",
    [("Common Equity Tier 1 (CET1) ratio", {"FY2025": "14.9%", "FY2024": "16.2%", "FY2023": "17.6%", "FY2022": "17.0%", "FY2021": "16.7%", "FY2020": "16.4%", "FY2019": "17.5%", "FY2018": "16.6%", "FY2017": "18.2%", "FY2016": "19.2%", "FY2015": "20.4%", "FY2014": "22.0%"})],
    p3_sources(),
    note="FY2025 RESTATED 2026-09-15 from SOLO to CONSOLIDATED basis (15.0% -> 14.9%) - see the CET1 Capital "
         "sheet note for the reason. Superseded solo value: 15.0% (ABCIB SOLO UK KM1 row 5, p.15, and the Annual "
         "Report's Financial Highlights table). FY2025 now matches FY2023/FY2024's consolidated basis, giving a "
         "clean consolidated run FY2023-FY2025. "
         "FY2023 shown as originally reported (17.6%, consolidated); the FY2024 Pillar 3 Report's FY2023 "
         "comparative column restates this to 17.7% alongside a small RWA restatement (see Total RWAs sheet) - "
         "immaterial, but shown as originally reported per this project's convention. FY2022/FY2021 and "
         "FY2014-FY2020 all labelled 'Tier 1 Capital Ratio' (a.k.a. 'Risk asset ratio - Tier 1') in the source "
         "(solo basis) - assumed equal to CET1 ratio, see CET1 Capital sheet note. FY2025's consolidated figure "
         "is labelled 'Common Equity Tier 1 ratio' outright (UK KM1 row 5), so no such assumption is needed for "
         "that year. FY2014-FY2016 predate the "
         "CET1 concept entirely (Basel II/early-CRD IV terminology) - see BASIS_NOTE's caveat.",
)

metric(
    "Tier 1 Capital", "£m",
    [("Tier 1 capital", {"FY2025": 579.993, "FY2024": 564.579, "FY2023": 547.665, "FY2022": 416.914, "FY2021": 419.517, "FY2020": 393.198, "FY2019": 495.422, "FY2018": 487.265, "FY2017": 469.029, "FY2016": 449.664, "FY2015": 439.008, "FY2014": 421.08})],
    p3_sources(),
    note="Tier 1 = CET1 every year (no AT1 instruments in issue) - the FY2021/FY2022/FY2025 Pillar 3 reports each "
         "print identical CET1 and Tier 1 rows, confirming this directly rather than by assumption. FY2025 "
         "RESTATED 2026-09-15 from SOLO to CONSOLIDATED (469.8 -> 579.993); FY2022/FY2021 upgraded from "
         "calculated to directly disclosed (416.5 -> 416.914, 418.8 -> 419.517) - see CET1 Capital sheet note for "
         "both. FY2016/FY2015/FY2014 remain calculated - see CET1 Capital sheet note.",
)

metric(
    "Tier 1 Ratio", "% of RWA",
    [("Tier 1 ratio", {"FY2025": "14.9%", "FY2024": "16.2%", "FY2023": "17.6%", "FY2022": "17.0%", "FY2021": "16.7%", "FY2020": "16.4%", "FY2019": "17.5%", "FY2018": "16.6%", "FY2017": "18.2%", "FY2016": "19.2%", "FY2015": "20.4%", "FY2014": "22.0%"})],
    p3_sources(),
    note="FY2025 RESTATED 2026-09-15 from SOLO to CONSOLIDATED basis (15.0% -> 14.9%); superseded solo value "
         "15.0%. FY2023 shown as originally reported (consolidated) - see CET1 Ratio sheet note.",
)

metric(
    "Total Capital", "£m",
    [("Total capital", {"FY2025": 628.255, "FY2024": 616.448, "FY2023": 598.786, "FY2022": 446.942, "FY2021": 459.544, "FY2020": 443.198, "FY2019": 545.422, "FY2018": 537.265, "FY2017": 524.729, "FY2016": 506, "FY2015": 493, "FY2014": 423})],
    p3_sources(),
    note="FY2025 RESTATED 2026-09-15 from SOLO to CONSOLIDATED basis (517 -> 628.255) - see the CET1 Capital "
         "sheet note for the reason. Superseded solo value: 517 (Annual Report 'Capital base'); the Pillar 3 "
         "Report 2025's own SOLO column gives a more precise 517.472. "
         "SOURCE TYPO, verified visually at 8x zoom on p.16: the FY2025 consolidated KM1 prints Total capital as "
         "'628.255' with a DECIMAL POINT where the thousands separator belongs (every other figure in the same "
         "column uses a comma). Read as 628,255 £'000: the printed digits are unchanged, only the separator is "
         "wrong, and 628,255 / 3,880,104 = 16.19% reproduces the same table's printed 16.2% total capital ratio, "
         "whereas a literal 628.255 (£628k) would be absurd against CET1 of £580m. Not a derived figure. "
         "FY2022/FY2021 UPGRADED 2026-09-15 to each year's own Pillar 3 report ('Total regulatory capital', solo "
         "column): 447 -> 446.942 and 460 -> 459.544. Same measure and same basis as the Annual Report 'Capital "
         "base' figures they replace - the AR simply rounds to £m - so this is a precision gain, not a "
         "restatement. FY2014-FY2016 ('Capital base', Financial Highlights table) and "
         "FY2023-FY2024/FY2017-FY2020 ('Total capital'/'Total regulatory capital') are directly disclosed, not "
         "calculated. FY2020's solo Total capital (443.198m) is genuinely lower than FY2019's (545.422m) - "
         "reflects the new investment in ABCSA (the Paris subsidiary) reducing solo-basis capital resources, per "
         "the FY2020 Pillar 3 report's own footnote ('The solo capital base reflect the new investment in "
         "ABSA') - a real basis effect, not a data error.",
)

metric(
    "Total Capital Ratio", "% of RWA",
    [("Total capital ratio", {"FY2025": "16.2%", "FY2024": "17.7%", "FY2023": "19.3%", "FY2022": "18.2%", "FY2021": "18.3%", "FY2020": "18.5%", "FY2019": "19.3%", "FY2018": "18.3%", "FY2017": "20.4%", "FY2016": "21.5%", "FY2015": "22.9%", "FY2014": "22.1%"})],
    p3_sources(),
    note="FY2025 RESTATED 2026-09-15 from SOLO to CONSOLIDATED basis (16.5% -> 16.2%) - see the CET1 Capital "
         "sheet note for the reason. Superseded solo value: 16.5% (ABCIB SOLO UK KM1 row 7, p.15, and the Annual "
         "Report's 'Risk asset ratio - Total'). FY2022/FY2021 are confirmed unchanged against each year's own "
         "Pillar 3 report ('Total Capital' ratio, solo column: 18.2% and 18.3%) - the validation gate for the "
         "FY2021/FY2022 documents located 2026-09-15. FY2014-FY2016 labelled 'Risk asset ratio - Total' in the "
         "Financial Highlights table.",
)

metric(
    "Total RWAs", "£m",
    [("Total risk-weighted exposure amount", {"FY2025": 3880.104, "FY2024": 3486.256, "FY2023": 3104.763, "FY2022": 2450.11, "FY2021": 2507.675, "FY2020": 2397.973, "FY2019": 2824.811, "FY2018": 2940.867, "FY2017": 2574.027, "FY2016": 2342, "FY2015": 2152, "FY2014": 1914})],
    p3_sources(),
    note="FY2025 RESTATED 2026-09-15 from SOLO to CONSOLIDATED basis (3,132m -> 3,880.104m) - see the CET1 "
         "Capital sheet note for the reason. Superseded solo value: 3,132m (Annual Report Financial Highlights); "
         "the Pillar 3 Report 2025's own SOLO column gives a more precise 3,131.618m, which is retained in the "
         "RWA Breakdown sheet's SOLO block so the solo basis stays visible. This removes the apparent FY2024 -> "
         "FY2025 fall that the old mixed presentation created: on a like-for-like consolidated basis RWAs ROSE "
         "from 3,486.256m to 3,880.104m. "
         "FY2022/FY2021 refined 2026-09-15 to each year's own Pillar 3 report (solo, Table 6 'RWAs and Capital "
         "ratio' / Key Regulatory Metrics): 2,450m -> 2,450.110m and 2,508m -> 2,507.675m - the same figures the "
         "Annual Report rounds to £m. "
         "FY2023 shown as originally reported (consolidated, 3,104.763m); the FY2024 Pillar 3 Report's FY2023 "
         "comparative column restates this to 3,101.197m - immaterial (~0.1%), shown as originally reported per "
         "this project's convention. FY2016 (2,342m, own-year Annual "
         "Report figure) differs immaterially (~0.2%) from the FY2018 Annual Report's restated FY2016 comparative "
         "(2,347m) - shown as originally reported, same convention as the FY2023 restatement above.",
)

rwa_breakdown_rows = [
    ("SECTION", "UK OV1 — Overview of risk weighted exposure amounts (CONSOLIDATED)", {}),
    ("DATA", "Credit risk (excluding CCR)", {"FY2025": 3554768, "FY2024": 3198514, "FY2023": 2842771}),
    ("DATA", "Counterparty credit risk (CCR)", {"FY2025": 45144, "FY2024": 45144, "FY2023": 55407}),
    ("DATA", "Of which: credit valuation adjustment (CVA)", {"FY2025": 13124, "FY2024": 10131, "FY2023": 11788}),
    ("DATA", "Position, foreign exchange and commodities risks (Market risk)", {"FY2025": 23741, "FY2024": 14469, "FY2023": 5670}),
    ("DATA", "Operational risk", {"FY2025": 243327, "FY2024": 217998, "FY2023": 185561}),
    ("TOTAL", "Total risk weighted exposure amount", {"FY2025": 3880104, "FY2024": 3486256, "FY2023": 3101197}),
    # Own SECTION block, not folded into the OV1 block above: this source
    # (the Annual Report's own "Regulatory capital" note, not a Pillar 3
    # report) is a coarser 3-category split on a different basis (SOLO,
    # matching the Total RWAs sheet's own figures for these years) - it
    # doesn't separate CCR/CVA out of credit risk, so its "Credit and
    # counterparty credit risk" row isn't directly comparable to the OV1
    # block's "Credit risk (excluding CCR)" row above. Directly disclosed
    # as risk-weighted assets (not derived), unlike the Pillar 1 block below.
    # FY2025 deliberately appears in BOTH this SOLO block and the CONSOLIDATED
    # block above. The Total RWAs sheet now carries FY2025 on the consolidated
    # basis (restated 2026-09-15), and keeping the solo split here is how the
    # superseded solo basis stays legible rather than being silently dropped -
    # the Pillar 3 Report 2025 prints both tables in full (pp.16-17).
    ("SECTION", "Regulatory capital note — risk-weighted assets (SOLO, unaudited, as disclosed)", {}),
    ("DATA", "Credit and counterparty credit risk", {"FY2025": 2923166, "FY2022": 2311968, "FY2021": 2362339}),
    ("DATA", "Market risk", {"FY2025": 24739, "FY2022": 3197, "FY2021": 1121}),
    ("DATA", "Operational risk", {"FY2025": 183713, "FY2022": 134945, "FY2021": 144216}),
    ("TOTAL", "Total risk weighted exposure amount", {"FY2025": 3131618, "FY2022": 2450110, "FY2021": 2507676}),
    # Third SECTION block, own basis note: these 4 years' dedicated Pillar 3
    # reports never disclose RWA by risk type directly - only the Pillar 1
    # MINIMUM CAPITAL REQUIREMENT by risk type (8% of RWA, per CRR Article
    # 92). Each figure below is that report's own capital-requirement figure
    # multiplied by 12.5 (= divided by 8%) - an exact regulatory identity,
    # not an estimate. Each year's Total below reconciles to within a few
    # £'000 of the Total RWAs sheet's own figure for that year (the residual
    # is the source table's own £'000 rounding before this multiplication).
    ("SECTION", "Pillar 1 capital requirement × 12.5 (SOLO, derived from disclosed capital requirement)", {}),
    ("DATA", "Credit risk", {"FY2020": 2245800, "FY2019": 2664138, "FY2018": 2794500, "FY2017": 2440150}),
    ("DATA", "Market risk", {"FY2020": 2100, "FY2019": 8988, "FY2018": 5250, "FY2017": 7425}),
    ("DATA", "Credit valuation adjustment (CVA)", {"FY2020": 613, "FY2019": 475, "FY2018": 513, "FY2017": 525}),
    ("DATA", "Operational risk", {"FY2020": 149463, "FY2019": 151213, "FY2018": 140613, "FY2017": 125925}),
    ("TOTAL", "Total risk weighted exposure amount (derived)", {"FY2020": 2397976, "FY2019": 2824814, "FY2018": 2940876, "FY2017": 2574025}),
]

bw.add_rwa_breakdown_sheet(
    title="ABC International Bank plc — RWA Breakdown",
    subtitle="All figures in £'000. FY2025/FY2024/FY2023 CONSOLIDATED basis (UK OV1); FY2025 ALSO shown in the "
             "SOLO block below, since the Pillar 3 Report 2025 prints both tables in full and the solo basis is "
             "retained there for continuity after FY2025's restatement onto the consolidated basis (2026-09-15); "
             "FY2022/FY2021 SOLO basis, as disclosed; FY2020-FY2017 SOLO basis, derived from disclosed Pillar 1 "
             "capital requirement x 12.5 - see the three SECTION blocks below and the sources note. Each year's "
             "TOTAL matches (within rounding) the Total RWAs sheet's figure for that year, on that year's own "
             "basis - FY2025's Total RWAs figure is now the CONSOLIDATED 3,880,104. FY2016-FY2014: no "
             "risk-type breakdown available - see sources note.",
    rows=rwa_breakdown_rows,
    sources_text=RWA_BREAKDOWN_SOURCES,
)

metric(
    "Leverage Ratio", "£m / %",
    [
        ("Total exposure measure excluding claims on central banks (£m)", {"FY2025": 5990.509, "FY2024": 5540.164, "FY2023": 5155.039, "FY2022": 3393.925, "FY2021": 3047.344, "FY2020": 2937.195, "FY2019": 3683.204, "FY2018": 4738.858, "FY2017": 3726.262}),
        ("Leverage ratio excluding claims on central banks (%)", {"FY2025": "9.7%", "FY2024": "10.2%", "FY2023": "10.62%", "FY2022": "12.28%", "FY2021": "13.77%", "FY2020": "13.39%", "FY2019": "13.45%", "FY2018": "10.28%", "FY2017": "12.59%"}),
    ],
    p3_sources(),
    note="FY2025 added 15 September 2026 from the ABCIB Pillar 3 Report 2025, which was located only via the "
         "bank's disclosures index (its filename abandons every prior naming convention - see the P3_2025_URL "
         "comment). CONSOLIDATED basis, matching FY2023/FY2024: that report prints separate 'ABCIB SOLO' and "
         "'ABCIB CONSOLIDATED' UK KM1 tables, and its consolidated FY2024 comparative column reproduces this "
         "workbook's existing FY2024 figures exactly (exposure 5,540,164k; ratio 10.2%), which is what identifies "
         "the basis. The solo table gives a materially different FY2025 (exposure 4,352,399k; ratio 10.8%) and is "
         "deliberately NOT used here. "
         "FY2022/FY2021 ADDED 2026-09-15 from each year's own dedicated Pillar 3 report, located that day on the "
         "disclosures index - the 'live lead' this note previously flagged is now closed. Both are SOLO basis "
         "(each report's Key Regulatory Metrics table prints a 'Solo | Consolidated' pair for a single date; the "
         "solo column is used, matching FY2017-FY2020 and this workbook's basis for every FY2014-FY2022 year). "
         "Their consolidated columns, NOT used, give FY2021 exposure 3,843,784k / 13.56% and FY2022 exposure "
         "4,509,683k / 11.69%. BASIS CAVEAT: FY2017-FY2022 are therefore solo and FY2023-FY2025 consolidated, so "
         "the two portions of this row are not strictly like-for-like - the step down from FY2022's 12.28% to "
         "FY2023's 10.62% is partly that basis change, not solely a real leverage increase. "
         "FY2014-FY2016 remain unavailable (the Annual Report Financial Highlights table carries no leverage "
         "metric and no dedicated Pillar 3 report exists for those years).",
)

metric(
    "LCR", "£m / %",
    [
        ("Total high-quality liquid assets (HQLA), weighted value - average (£m)", {"FY2025": 748.628, "FY2024": 854.893, "FY2023": 699.862, "FY2022": 427.736, "FY2021": 362.210, "FY2020": 362.315, "FY2019": 634.602, "FY2018": 566.611, "FY2017": 1002.101}),
        ("Total net cash outflows, adjusted value (£m)", {"FY2025": 299.370, "FY2024": 252.133, "FY2023": 189.675, "FY2022": 139.904, "FY2021": 133.186, "FY2020": 127.560, "FY2019": 168.941, "FY2018": 192.084, "FY2017": 405.144}),
        ("Liquidity Coverage Ratio (%)", {"FY2025": "250.1%", "FY2024": "339.1%", "FY2023": "369.0%", "FY2022": "310%", "FY2021": "276%", "FY2020": "281%", "FY2019": "391%", "FY2018": "325%", "FY2017": "281%"}),
    ],
    p3_sources(),
    note="FY2025 added 15 September 2026 from the ABCIB Pillar 3 Report 2025, 'ABCIB CONSOLIDATED' UK KM1 table - "
         "same consolidated basis as FY2023/FY2024, confirmed by that table's FY2024 comparative column "
         "reproducing this workbook's existing HQLA 854,893k / outflows 252,133k / 339.1% exactly. Internal "
         "cross-check: 748,628 / 299,370 = 250.07%, consistent with the printed 250.1%. The report's separate "
         "solo table gives a different FY2025 LCR (231.0%) and is not used. FY2023 LCR is sourced from the FY2024 "
         "Pillar 3 Report's comparative column - ABCIB's own FY2023 Pillar 3 Disclosures document (Table 3) does "
         "not include LCR at all (only capital and leverage metrics). "
         "FY2022/FY2021 ADDED 2026-09-15 from each year's own dedicated Pillar 3 report (Table 17 'LCR components "
         "(Average)'), located that day - closing the 'live lead' this note previously flagged. SOLO column used, "
         "matching FY2017-FY2020; the consolidated columns, NOT used, give FY2021 327% and FY2022 330%. Both "
         "years' reports state the components are 'based on the average of the twelve monthly reported data "
         "items', i.e. the same 12-month-average basis as the UK KM1 years - NOT a point-in-time year-end ratio. "
         "NOTE the component rows do not divide to the printed ratio (FY2021 362,210/133,186 = 272.0% vs 276% "
         "printed; FY2022 427,736/139,904 = 305.7% vs 310% printed): the disclosed ratio is the average of the "
         "twelve monthly LCRs, whereas the components are averaged separately, so a ratio-of-averages does not "
         "reproduce an average-of-ratios. The printed ratio is carried as disclosed; nothing is derived. "
         "'Liquidity Buffer' is that table's label for the HQLA row. FY2014-FY2016 not available. "
         "FY2017-FY2022 are all SOLO basis, "
         "so they are not strictly like-for-like with the consolidated FY2023-FY2025 figures.",
)

metric(
    "NSFR", "£m / %",
    [
        ("Total available stable funding (£m)", {"FY2025": 2391.315, "FY2024": 2339.367, "FY2023": 2053.004, "FY2022": 1660.479}),
        ("Total required stable funding (£m)", {"FY2025": 1902.311, "FY2024": 1802.627, "FY2023": 1504.583, "FY2022": 1325.875}),
        ("Net Stable Funding Ratio (%)", {"FY2025": "125.7%", "FY2024": "129.8%", "FY2023": "136.4%", "FY2022": "125.24%"}),
    ],
    p3_sources(),
    note="FY2025 added 15 September 2026 from the ABCIB Pillar 3 Report 2025, 'ABCIB CONSOLIDATED' UK KM1 table - "
         "same consolidated basis as FY2023/FY2024, confirmed by that table's FY2024 comparative column "
         "reproducing this workbook's existing ASF 2,339,367k / RSF 1,802,627k / 129.8% exactly. Internal "
         "cross-check: 2,391,315 / 1,902,311 = 125.7%, matching the printed ratio. FY2023 NSFR is sourced from the "
         "FY2024 Pillar 3 Report's comparative column - same reason as the LCR sheet. "
         "FY2022 ADDED 2026-09-15 from the ABCIB Pillar 3 Disclosures 2022, Table 18 'NSFR components (Average)', "
         "located that day - SOLO basis ('Solo Avg 2022' column; the consolidated column, NOT used, gives "
         "123.91%). Internal cross-check: 1,660,479 / 1,325,875 = 125.24%, matching the printed ratio exactly. "
         "This is ABCIB's FIRST disclosed NSFR and it correctly falls in the first year the UK requirement "
         "applied. "
         "FY2021 and earlier are STRUCTURALLY absent, not an oversight: the FY2021 Pillar 3 report was re-read in "
         "full on 2026-09-15 and contains zero occurrences of 'stable funding' anywhere, and NSFR is discussed "
         "only in qualitative/narrative terms (e.g. 'well on the way to becoming fully compliant') in ABCIB's "
         "FY2016-FY2020 reports, never as a figure. That is exactly what PRA PS17/21 / PS22/21 require: the UK "
         "had no NSFR requirement and no NSFR disclosure template before 1 January 2022, and firms were not "
         "required to disclose comparatives for periods before the rule bit. Blank rather than derived. "
         "FY2014-FY2016 likewise unavailable.",
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
        ("CET1 Ratio", {"FY2025": "14.9%", "FY2024": "16.2%", "FY2023": "17.6%", "FY2022": "17.0%", "FY2021": "16.7%", "FY2020": "16.4%", "FY2019": "17.5%", "FY2018": "16.6%", "FY2017": "18.2%", "FY2016": "19.2%", "FY2015": "20.4%", "FY2014": "22.0%"}),
        ("Tier 1 Ratio", {"FY2025": "14.9%", "FY2024": "16.2%", "FY2023": "17.6%", "FY2022": "17.0%", "FY2021": "16.7%", "FY2020": "16.4%", "FY2019": "17.5%", "FY2018": "16.6%", "FY2017": "18.2%", "FY2016": "19.2%", "FY2015": "20.4%", "FY2014": "22.0%"}),
        ("Total Capital Ratio", {"FY2025": "16.2%", "FY2024": "17.7%", "FY2023": "19.3%", "FY2022": "18.2%", "FY2021": "18.3%", "FY2020": "18.5%", "FY2019": "19.3%", "FY2018": "18.3%", "FY2017": "20.4%", "FY2016": "21.5%", "FY2015": "22.9%", "FY2014": "22.1%"}),
        ("Leverage Ratio (excl. central bank claims)", {"FY2025": "9.7%", "FY2024": "10.2%", "FY2023": "10.62%", "FY2022": "12.28%", "FY2021": "13.77%", "FY2020": "13.39%", "FY2019": "13.45%", "FY2018": "10.28%", "FY2017": "12.59%"}),
        ("LCR", {"FY2025": "250.1%", "FY2024": "339.1%", "FY2023": "369.0%", "FY2022": "310%", "FY2021": "276%", "FY2020": "281%", "FY2019": "391%", "FY2018": "325%", "FY2017": "281%"}),
        ("NSFR", {"FY2025": "125.7%", "FY2024": "129.8%", "FY2023": "136.4%", "FY2022": "125.24%"}),
    ],
    note="ABC International Bank plc takes the FRS 101 cash-flow-statement exemption every year (see the Cash Flow "
         "Statement sheet), so no cash flow summary or chart is shown here - only the Balance Sheet / P&L / Equity "
         "blocks (all entity/solo basis) and the Pillar 3 Key Metrics trend chart below. Pillar 3 ratios are "
         "consolidated basis for FY2023-FY2025 and solo basis for FY2014-FY2022 - a different basis to the "
         "statement blocks above, see the Cash Flow Statement sheet's entity note. "
         "FY2025 BASIS MIX RESOLVED (2026-09-15): the FY2025 column previously held CONSOLIDATED "
         "Leverage/LCR/NSFR alongside SOLO capital ratios. On the user's explicit instruction the capital ratios "
         "were restated onto the consolidated basis (CET1/Tier 1 15.0% -> 14.9%, total capital 16.5% -> 16.2%, "
         "RWAs £3,132m -> £3,880.104m), so the whole FY2025 column is now one basis. Superseded solo figures are "
         "preserved in each capital sheet's note and as a full risk-type split in the RWA Breakdown sheet's SOLO "
         "block. "
         "FY2022/FY2021 Leverage Ratio and LCR, and FY2022 NSFR, were ADDED the same day from each year's own "
         "dedicated Pillar 3 report (ABCIB-Pillar3Disclosure-2021.pdf / -2022.pdf), which an earlier pass had "
         "wrongly recorded as non-existent. Note the resulting FY2022 -> FY2023 step in the Leverage/LCR rows is "
         "partly the solo-to-consolidated basis change, not solely a real movement - see those sheets' notes. "
         "FY2025's statement/asset-"
         "quality figures were transcribed from a scanned Companies House filing via visual reading (OCR-style). "
         "HD-018 extended this workbook's window from FY2021-FY2025 back to FY2014-FY2025 (2026-09-05); FY2018's "
         "'Other equity movements' figure (-£6,549k) is the IFRS 9 transition adjustment recognised on 1 January "
         "2018, not a dividend - see the Statement of Changes in Equity sheet.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/ABC INTERNATIONAL BANK FINANCIALS.xlsx")
