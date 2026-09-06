import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook


# HD-049: extended back to FY2014 (capped project-wide at FY2014 - see ticket).
# HD-074 (2026-09-06): further extended to FY2010, Metro Bank's real statutory
# floor (Companies House incorporation 2007, but the entity only began trading
# as a bank in July 2010) - Balance Sheet/P&L/Statement of Changes in
# Equity/Cash Flow ONLY, per HD-074's scope; Pillar 3/Asset Quality/RWA
# Breakdown are untouched and still start at FY2014.
# FY2014-FY2020 sourcing/transcription in progress; blank dict keys = not yet
# sourced/transcribed for that year (not a zero).
YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021", "FY2020", "FY2019", "FY2018", "FY2017", "FY2016", "FY2015", "FY2014",
         "FY2013", "FY2012", "FY2011", "FY2010"]
YEAR_LABEL = {y: y for y in YEARS}
YEAR_LABEL["FY2010"] = "FY2010 (16m)"

# HD-074: Pillar 3 (all 11 metric sheets), Asset Quality, and RWA Breakdown
# stay out of scope for this statutory-statement-only extension - pin them
# to the original project-wide FY2014-FY2025 window via this override.
PILLAR3_YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021", "FY2020", "FY2019", "FY2018", "FY2017", "FY2016", "FY2015", "FY2014"]

AR_2014 = "https://www.metrobankonline.co.uk/globalassets/documents/investor_documents/annual-report-2015.pdf"  # FY2014 restated comparative column (see DATA QUALITY note)
AR_2015 = "https://www.metrobankonline.co.uk/globalassets/documents/investor_documents/annual-report-2015.pdf"
AR_2016 = "https://www.metrobankonline.co.uk/globalassets/documents/investor_documents/metro-bank-annual-report-2016.pdf"
AR_2017 = "https://www.metrobankonline.co.uk/globalassets/documents/investor_documents/2017-annual-report.pdf"
AR_2018 = "https://www.metrobankonline.co.uk/globalassets/documents/investor_documents/annual-report-2018.pdf"
AR_2019 = "https://www.metrobankonline.co.uk/globalassets/documents/investor_documents/metro-bank-annual-report-2019.pdf"
AR_2020 = "https://www.metrobankonline.co.uk/globalassets/investor-relations/metro-bank-annual-report-2020.pdf"
P3_2016 = "https://www.metrobankonline.co.uk/globalassets/legal-information/pillar-3-disclosure-2016.pdf"
P3_2017_HIST = "https://www.metrobankonline.co.uk/globalassets/documents/investor_documents/metro-bank-2017-pillar-3-disclosure.pdf"
P3_2018_HIST = "https://www.metrobankonline.co.uk/globalassets/documents/investor_documents/pillar-3-disclosure-2018.pdf"
P3_2019_HIST = "https://www.metrobankonline.co.uk/globalassets/documents/investor_documents/metro-bank-pillar-3-2019.pdf"
P3_2020_HIST = "https://www.metrobankonline.co.uk/globalassets/investor-relations/metro-bank-plc-pillar-3-2020.pdf"
AR_2021 = "https://www.metrobankonline.co.uk/globalassets/documents/customer_documents/intermediaries/metro-bank-annual-report-2021.pdf"
AR_2022 = "https://www.metrobankonline.co.uk/globalassets/documents/customer_documents/business-and-commercial/metro-bank-annual-report-and-accounts-2022.pdf.pdf"
AR_2023 = "https://www.metrobankonline.co.uk/globalassets/documents/customer_documents/business-and-commercial/metro-bank-plc-annual-report-2023.pdf"
AR_2024 = "https://www.metrobankonline.co.uk/globalassets/documents/customer_documents/personal/metro-bank-annual-report-2024.pdf"
AR_2025 = "https://www.metrobankonline.co.uk/globalassets/documents/investor_documents/metro-bank---annual-report-2025.pdf"
P3_2021 = "https://www.metrobankonline.co.uk/globalassets/documents/customer_documents/intermediaries/metro-bank-pillar-3-disclosure-2021.pdf"
P3_H1_2022 = "https://www.metrobankonline.co.uk/globalassets/documents/customer_documents/business-and-commercial/pillar-3-disclosure---h1-2022.pdf"
P3_H1_2023 = "https://www.metrobankonline.co.uk/globalassets/documents/customer_documents/personal/pillar-3-disclosure-h1-2023.pdf"
P3_H1_2024 = "https://www.metrobankonline.co.uk/globalassets/documents/customer_documents/intermediaries/pillar-3-disclosure-h1-2024.pdf"
P3_H1_2025 = "https://www.metrobankonline.co.uk/globalassets/h1-2025-pillar-3-final.pdf"
P3_2022 = "https://www.metrobankonline.co.uk/globalassets/documents/customer_documents/business-and-commercial/pillar-3-disclosure-2022.pdf"
P3_2023 = "https://www.metrobankonline.co.uk/globalassets/pillar-3-disclosure-2023.pdf"
P3_2024 = "https://www.metrobankonline.co.uk/globalassets/pillar-3-2024.pdf"
P3_2025 = "https://www.metrobankonline.co.uk/globalassets/documents/investor_documents/pillar-3---2025-final.pdf"

# HD-074: Metro Bank's own IR site does not host reports this old; Companies
# House is the only located source for FY2010-FY2013 (Metro Bank PLC,
# Companies House 06419578). These are the stable filing-history document
# permalinks (each redirects to a freshly-signed download on access).
CH_FY2010 = "https://find-and-update.company-information.service.gov.uk/company/06419578/filing-history/MzAzOTgzODAwMGFkaXF6a2N4/document?format=pdf&download=0"
CH_FY2011 = "https://find-and-update.company-information.service.gov.uk/company/06419578/filing-history/MzA2MDE4MDA3NWFkaXF6a2N4/document?format=pdf&download=0"
CH_FY2012 = "https://find-and-update.company-information.service.gov.uk/company/06419578/filing-history/MzA3OTE2MjcwMGFkaXF6a2N4/document?format=pdf&download=0"
CH_FY2013 = "https://find-and-update.company-information.service.gov.uk/company/06419578/filing-history/MzEwMzEwOTEwMGFkaXF6a2N4/document?format=pdf&download=0"

ENTITY_NOTE = (
    "ENTITY/BASIS NOTE: Metro Bank PLC (Companies House 06419578; FRN 488982; LEI "
    "213800X5WU57YL9GPK89) is the matched legal entity in Banks List 2608.xlsx. "
    "FY2021-FY2023 cash flows are the Company/standalone figures from Metro Bank PLC "
    "accounts. Metro Bank PLC used an individual consolidation method for prudential "
    "reporting in 2021-2022. On 19 May 2023 Metro Bank Holdings PLC became the ultimate "
    "holding company; FY2023-FY2025 Pillar 3 disclosures are subsequently for Holdings "
    "and its subsidiaries, not standalone Metro Bank PLC. FY2024-FY2025 standalone Metro "
    "Bank PLC accounts/cash flows were not located in the reviewed official archive and "
    "are left blank rather than substituted with Holdings figures."
    "\n\nHD-049 EXTENSION (2026-09-06): FY2014-FY2020 added, capped at FY2014 by explicit project-wide user "
    "decision (real Metro Bank archive extends to FY2010, but pre-CRD IV/Basel III Pillar 3 disclosures aren't "
    "comparable). Balance Sheet/Cash Flow/Statement of Changes in Equity for FY2014-FY2020 are shown on a "
    "Consolidated/Group basis (Metro Bank PLC did not have a materially different standalone Company balance "
    "sheet/cash flow in these years, and re-extracting the separate Company statements for 7 more years was not "
    "attempted this session) - this differs from the Company/standalone basis used for FY2021-FY2023, so there is "
    "a genuine basis change at the FY2020/FY2021 boundary in addition to the FY2023 basis change already noted "
    "above; both are flagged rather than silently blended. DATA QUALITY FLAG: FY2014 figures are the 'restated' "
    "comparative column as published in the Annual Report and Accounts 2015 (Metro Bank's own FY2014 Annual "
    "Report, if one was published as a standalone document pre-IPO, was not located in the company's live IR "
    "site, Wayback Machine snapshots 2014-2016, or a quick Companies House filing-history check within this "
    "session's effort - only the 2015 AR's restated FY2014 comparative was found); note 36 of the 2015 AR "
    "references undisclosed prior-period adjustments behind the 'restated' label. No dedicated Pillar 3 disclosure "
    "document for FY2014 or FY2015 was located (Metro Bank's Pillar 3 archive appears to begin with FY2016, the "
    "year of its LSE listing); FY2014/FY2015 capital figures below are instead sourced from the Capital "
    "management note in the FY2015 Annual Report and the FY2016 Annual Report's own capital-structure table "
    "(both audited, both citing Tier 1/Total capital resources), not a Pillar 3 report - Total RWAs and LCR were "
    "not disclosed in either document for FY2014/FY2015 and are left blank rather than estimated."
)

# HD-074 (2026-09-06): kept separate from ENTITY_NOTE, deliberately, so it is
# appended ONLY to the in-scope statutory-statement sources (Balance Sheet/P&L/
# Statement of Changes in Equity/Cash Flow) - never to P3_SOURCES/ASSET_QUALITY_
# SOURCES, which must stay byte-for-byte unchanged for this out-of-scope extension.
HD074_EXTENSION_NOTE = (
    f"FY2013 (Group): Metro Bank PLC Full Accounts, year ended 31 December 2013, Consolidated Statement of comprehensive income/Consolidated Balance Sheet/Consolidated Statement of changes in equity, p.10-11 and p.15 - {CH_FY2013}\n"
    f"FY2012: Metro Bank PLC Full Accounts, year ended 31 December 2012, Statement of comprehensive income/Balance Sheet/Statement of changes in equity, p.9-10 and p.12 - {CH_FY2012}\n"
    f"FY2011: Metro Bank PLC Full Accounts, year ended 31 December 2011, Statement of comprehensive income/Balance Sheet/Statement of changes in equity, p.9-10 and p.12 - {CH_FY2011}\n"
    f"FY2010 (16m): Metro Bank PLC Financial Statements, period ended 31 December 2010, Statement of comprehensive income/Balance Sheet/Statement of changes in equity, p.8-9 and p.11 - {CH_FY2010}\n\n"
    "HD-074 EXTENSION (2026-09-06): Balance Sheet/P&L/Statement of Changes in Equity/Cash Flow further extended "
    "to FY2010 - Metro Bank PLC's real statutory floor. Pillar 3/Asset Quality/RWA Breakdown are explicitly out of "
    "scope for this extension and remain unchanged, still starting at FY2014. Sourced entirely from Companies House "
    "(06419578) full accounts filings - Metro Bank's own IR site does not host reports this old. ENTITY HISTORY: "
    "the company was incorporated 6 November 2007 as a shelf company, converted to a PLC and changed its accounting "
    "reference date to 31 December on 18 September 2009, then began trading as a bank on 29 July 2010 (its first "
    "branch, Holborn). FY2010's first accounts therefore cover a genuine 16-month period (19 September 2009 to 31 "
    "December 2010), not a clean 12-month year - labelled 'FY2010 (16m)' in the column header for this reason "
    "(same convention as this project's other non-12-month periods, e.g. StreamBank PLC's 'FY2023 (15m)'). BASIS: "
    "FY2010-FY2012 are Company-only (Metro Bank had no subsidiaries yet, so 'Balance Sheet'/'Statement of "
    "comprehensive income' as filed are already the whole entity); FY2013 is Group/Consolidated (Metro Bank "
    "acquired 100% of SME Invoice Finance Limited on 31 July 2013, its first subsidiary, so a Company/Group split "
    "first appears in the FY2013 accounts - Group figures are used for consistency with the Group/Consolidated "
    "basis already used for FY2014-FY2020 above). INVESTMENT SECURITIES: the FY2011-FY2013 balance sheets disclose "
    "a single combined 'Investment securities' line without an available-for-sale/held-to-maturity note-level split "
    "(unlike FY2010, which explicitly labels its £40.3m holding 'held to maturity', and FY2014-FY2017, which do "
    "split) - carried under a dedicated 'Investment securities (undifferentiated basis)' row rather than forced "
    "into the HTM/AFS split used elsewhere, to avoid a false precision this session didn't verify. CASH FLOW: "
    "FY2011 and FY2012 disclose only a net investment-securities purchase figure (no separate gross sale/purchase "
    "lines), while FY2010 and FY2013 disclose true gross purchases (and, for FY2013, a true gross sale) - both "
    "presentations are as-reported, not reclassified by this workbook. ROUNDING: source figures are in £'000, "
    "converted here to whole £m to one decimal place; summing independently-rounded component rows can be off by "
    "up to £0.1m from the stated Total in a few places - the same rounding-artifact pattern already documented "
    "above for FY2014-FY2017, not a data error."
)

CASH_SOURCES = (
    "ROUNDING NOTE (HD-049): FY2014-FY2017 source figures were originally reported in £'000 and are converted here "
    "to whole £m per line item; the reconciliation totals use each year's own as-reported £m-equivalent total, so "
    "summing the independently-rounded component rows can be off by £1m from the total in a few years (FY2014, "
    "FY2016, FY2017) - this is a rounding artifact of the conversion, not a data error.\n\n"
    "Sources - Metro Bank PLC Company/standalone cash flows, £m:\n"
    f"FY2023 & FY2022: Metro Bank PLC Annual Report 2023, p.147 (Company cash flow statement) - {AR_2023}\n"
    f"FY2022 & FY2021: Metro Bank PLC Annual Report and Accounts 2022, p.185 (Company column) - {AR_2022}\n"
    f"FY2021: Metro Bank PLC Annual Report and Accounts 2021, p.165 (Company column) - {AR_2021}\n"
    f"FY2013: Metro Bank PLC Full Accounts, year ended 31 December 2013, Consolidated Cash flow statement, p.13 - {CH_FY2013}\n"
    f"FY2012: Metro Bank PLC Full Accounts, year ended 31 December 2012, Cash flow statement, p.11 - {CH_FY2012}\n"
    f"FY2011: Metro Bank PLC Full Accounts, year ended 31 December 2011, Cash flow statement, p.11 - {CH_FY2011}\n"
    f"FY2010 (16m): Metro Bank PLC Financial Statements, period ended 31 December 2010, Cash flow statement, p.10 - {CH_FY2010}\n\n"
    + ENTITY_NOTE
    + "\n\n" + HD074_EXTENSION_NOTE
)

P3_SOURCES = (
    "Sources - Metro Bank regulatory key metrics:\n"
    f"FY2020: Metro Bank PLC Pillar 3 Disclosure 2020, Table 6/KM1 and Table 8 EU OV1 - {P3_2020_HIST}\n"
    f"FY2019: Metro Bank PLC Pillar 3 Disclosure 2019, Table 2 Key Ratios, KM1 and Table 8 EU OV1 - {P3_2019_HIST}\n"
    f"FY2018: Metro Bank PLC Pillar 3 Disclosure 2018, Key Ratios table, KM1 and Table 10 EU OV1 - {P3_2018_HIST}\n"
    f"FY2017: Metro Bank PLC 2017 Pillar 3 Disclosure, Capital Adequacy/Leverage Ratio Common Disclosure tables - {P3_2017_HIST}\n"
    f"FY2016: Metro Bank PLC Pillar 3 Disclosure 2016, Tier 1 capital/Leverage Ratio Common Disclosure tables - {P3_2016}\n"
    f"FY2014/FY2015: no dedicated Pillar 3 disclosure located (see HD-049 note) - capital resources/ratio from Metro "
    f"Bank PLC Annual Report Year Ended 31 December 2015 (Capital management note, p.76) - {AR_2015} - and Risk "
    f"weighted assets/CET1 ratio/leverage ratio for FY2015 from Metro Bank PLC Annual Report and Accounts 2016 "
    f"(Capital structure table) - {AR_2016}\n"
    f"FY2025: Metro Bank Holdings PLC Pillar 3 Disclosure 2025, p.10 - {P3_2025}\n"
    f"FY2024: Metro Bank Holdings PLC Pillar 3 Disclosure 2024, p.12 - {P3_2024}\n"
    f"FY2023: Metro Bank Holdings PLC Pillar 3 Disclosure 2023, p.12 - {P3_2023}\n"
    f"FY2022: Metro Bank PLC Pillar 3 Disclosure 2022, p.10 - {P3_2022}\n"
    f"FY2021: Metro Bank PLC Pillar 3 Disclosure 2021, p.4 - {P3_2021}\n\n"
    + ENTITY_NOTE
)

bw = BankWorkbook(bank_name="Metro Bank PLC", years=YEARS, year_label=YEAR_LABEL, header_color="00695C")

STATEMENTS_SOURCES = (
    "Sources - Metro Bank PLC statements, £m:\n"
    f"FY2020: Metro Bank PLC Annual Report and Accounts 2020, Consolidated statement of comprehensive income/balance sheet/statement of changes in equity/cash flow statement, p.163-167 - {AR_2020}\n"
    f"FY2019: Metro Bank PLC Annual Report and Accounts 2019, same statements, p.119-123 - {AR_2019}\n"
    f"FY2018: Metro Bank Plc Annual report and accounts 2018, same statements, p.104-107 - {AR_2018}\n"
    f"FY2017: Metro Bank PLC Annual Report and Accounts 2017, same statements, p.87-90 - {AR_2017}\n"
    f"FY2016: Metro Bank PLC Annual Report and Accounts 2016, same statements, p.73-76 - {AR_2016}\n"
    f"FY2015: Metro Bank PLC Annual Report, Year Ended 31 December 2015, Consolidated statement of comprehensive income/balance sheet/cash flow statement/statement of changes in equity, p.27-30 - {AR_2015}\n"
    f"FY2014 (restated): same FY2015 Annual Report's FY2014 comparative column, p.27-30 (own FY2014 Annual Report not located - see HD-049 note) - {AR_2014}\n"
    f"FY2025: Metro Bank Holdings PLC Annual Report and Accounts 2025, Consolidated income statement/balance sheet/statement of changes in equity, p.147-151 - {AR_2025}\n"
    f"FY2024: Metro Bank Holdings PLC Annual Report and Accounts 2024, Consolidated statement of comprehensive income/balance sheet/statement of changes in equity, p.161-164 - {AR_2024}\n"
    f"FY2023: Metro Bank PLC Annual Report 2023, Consolidated and Company statement of comprehensive income/balance sheet/statement of changes in equity, p.92-95 and p.144-146 - {AR_2023}\n"
    f"FY2022: Metro Bank PLC Annual Report and Accounts 2022, Consolidated and company statement of comprehensive income/balance sheets/statements of changes in equity, p.181-184 - {AR_2022}\n"
    f"FY2021: Metro Bank PLC Annual Report & Accounts 2021, Consolidated statement of comprehensive income/Consolidated and company balance sheets/statements of changes in equity, p.162-165 - {AR_2021}\n\n"
    + ENTITY_NOTE
    + "\n\nBASIS NOTE: Balance Sheet and Statement of Changes in Equity are shown on the same Company/standalone Metro "
    "Bank PLC basis as the Cash Flow Statement for FY2021-FY2023, and left blank for FY2024-FY2025 for the same reason "
    "(no standalone Metro Bank PLC accounts were located for those years - the 'Company' balance sheet published in the "
    "FY2024/FY2025 Annual Reports is Metro Bank Holdings PLC's own shell-company balance sheet, an investment-holding "
    "entity with ~£1.8bn/£1.9bn total assets dominated by 'Investment in subsidiaries', a fundamentally different entity "
    "from the ~£17-22bn banking entity Metro Bank PLC and not a defensible substitute; confirmed via Companies House "
    "filing history for Metro Bank PLC (06419578), which lists only 'Group of companies' accounts' for FY2024/FY2025, "
    "no standalone individual accounts). Profit & Loss is shown on a Group/consolidated basis for all 5 years, because "
    "Metro Bank PLC does not publish its own standalone income statement in any year reviewed (s.408 Companies Act 2006 "
    "exemption, available where consolidated accounts are also presented) - only a Company balance sheet, statement of "
    "changes in equity, and cash flow statement.\n\n"
    "DATA QUALITY FLAG: the FY2024 Annual Report's own FY2023 comparative column restates several FY2023 P&L and "
    "Balance Sheet figures from what AR2023 itself originally reported (e.g. Total operating expenses (585.2) vs "
    "AR2023's own (566.4); Total assets 22,245 vs AR2023's own 22,267; Total equity 1,134 vs AR2023's own 1,153) - this "
    "workbook uses each year's own contemporaneous figures (as AR2023 itself reported FY2023) rather than the later "
    "restated comparative, consistent with this project's standing convention.\n\n"
    "P&L PRESENTATION NOTE (HD-049): FY2015-FY2017 include a 'Costs associated with Listing / Listing Share Awards' "
    "expense line and a pre-IFRS 9 'Credit impairment charges' line (incurred-loss model) that have no FY2018+ "
    "equivalent row (from FY2018, IFRS 9 folds these into 'Impairment...' and 'Expected credit loss expense' "
    "respectively) - both are additive components of Total operating expenses/Profit before tax for those years "
    "only, not separately continued afterwards. The FY2014 comparative in the audited FY2015 Annual Report, p.28, "
    "shows explicit dashes for both listing fees and impairment/write-offs; these are recorded as £0m, not left as "
    "unknowns.\n\n"
    "ROUNDING NOTE (HD-049): as with the Cash Flow Statement, FY2014-FY2017 Balance Sheet/P&L/Equity source figures "
    "were originally reported in £'000 and converted here to whole £m per line item; summing independently-rounded "
    "component rows can be up to £1m off the reported Total in a few years (FY2016/FY2017 Total assets, FY2014/"
    "FY2017 Total liabilities, FY2017 Total equity) - a rounding artifact of the conversion, not a data error."
)

cash_rows = [
    ("SECTION", "Reconciliation of profit/(loss) before tax to net cash flows from operating activities", {}),
    ("DATA", "Profit/(loss) before tax", {"FY2023": 46, "FY2022": -71, "FY2021": -245,
        "FY2020": -311, "FY2019": -131, "FY2018": 41, "FY2017": 19, "FY2016": -17, "FY2015": -57, "FY2014": -49,
        "FY2013": -52.2, "FY2012": -45.7, "FY2011": -33.1, "FY2010": -23.4}),
    ("DATA", "Impairment and write-offs of property, plant, equipment and intangible assets", {
        "FY2020": 41, "FY2019": 78, "FY2018": 5, "FY2017": 1, "FY2016": 1, "FY2015": 9}),
    ("DATA", "Interest on lease liabilities", {"FY2020": 19, "FY2019": 18}),
    ("DATA", "Depreciation and amortisation (cash flow add-back)", {
        "FY2020": 74, "FY2019": 76, "FY2018": 45, "FY2017": 33, "FY2016": 22, "FY2015": 18, "FY2014": 14,
        "FY2013": 10.4, "FY2012": 6.2, "FY2011": 3.7, "FY2010": 1.5}),
    ("DATA", "Share option charge", {
        "FY2020": 2, "FY2019": 4, "FY2018": 5, "FY2017": 3, "FY2016": 2, "FY2015": 1, "FY2014": 1,
        "FY2013": 0.4, "FY2012": 0.3, "FY2011": 0.1}),
    ("DATA", "Grant income recognised in the income statement", {"FY2020": -24, "FY2019": -16}),
    ("DATA", "Amounts provided for (net of amounts released)", {"FY2020": 8, "FY2019": 12}),
    ("DATA", "Gain on sale of securities and fair value gains on derivatives", {
        "FY2020": -73, "FY2019": -2, "FY2018": -11, "FY2017": -4, "FY2016": -5, "FY2015": -6, "FY2014": -5,
        "FY2013": -6.5, "FY2012": -1.7, "FY2011": -2.3}),
    ("DATA", "Accrued interest on and amortisation of investment securities", {
        "FY2020": 3, "FY2019": -8, "FY2018": -7, "FY2017": 2, "FY2016": -4, "FY2015": 9, "FY2014": -4,
        "FY2013": -4.4, "FY2012": -4.1}),
    ("DATA", "Adjustments for non-cash items", {"FY2023": -376, "FY2022": -259, "FY2021": -132}),
    ("DATA", "Interest received", {"FY2023": 834, "FY2022": 538, "FY2021": 394}),
    ("DATA", "Interest paid", {"FY2023": -370, "FY2022": -124, "FY2021": -126}),
    ("DATA", "Changes in loans and advances to customers", {"FY2020": 2591, "FY2019": -445}),
    ("DATA", "Changes in deposits from customers", {"FY2020": 1595, "FY2019": -1184}),
    ("DATA", "Changes in other operating assets", {"FY2023": 729, "FY2022": -842, "FY2021": 2613,
        "FY2020": -2820, "FY2019": -26, "FY2018": -4651, "FY2017": -3755, "FY2016": -2341, "FY2015": -1971, "FY2014": -856,
        "FY2013": -591.9, "FY2012": -129.9, "FY2011": -44.6, "FY2010": -1.6}),
    ("DATA", "Changes in other operating liabilities", {"FY2023": -251, "FY2022": -409, "FY2021": 370,
        "FY2020": -64, "FY2019": -31, "FY2018": 4726, "FY2017": 5994, "FY2016": 3512, "FY2015": 2543, "FY2014": 1709,
        "FY2013": 893.6, "FY2012": 430.6, "FY2011": 140.0, "FY2010": 17.0}),
    ("TOTAL", "Net cash inflows/(outflows) from operating activities", {"FY2023": 612, "FY2022": -1167, "FY2021": 2874,
        "FY2020": 1041, "FY2019": -1655, "FY2018": 153, "FY2017": 2294, "FY2016": 1169, "FY2015": 546, "FY2014": 810,
        "FY2013": 249.3, "FY2012": 255.8, "FY2011": 63.7, "FY2010": -6.5}),
    ("SECTION", "Cash flows from investing activities", {}),
    ("DATA", "Sales of investment securities", {"FY2023": 1870, "FY2022": 857, "FY2021": 1269,
        "FY2020": 615, "FY2019": 2193, "FY2018": 1522, "FY2017": 309, "FY2016": 2197, "FY2015": 911, "FY2014": 474,
        "FY2013": 368.1}),
    ("DATA", "Purchase of investment securities", {"FY2023": -816, "FY2022": -1206, "FY2021": -3438,
        "FY2020": -1460, "FY2019": -618, "FY2018": -1740, "FY2017": -997, "FY2016": -3403, "FY2015": -1311, "FY2014": -1376,
        "FY2013": -638.5, "FY2012": -335.7, "FY2011": -38.7, "FY2010": -40.3}),
    ("DATA", "Purchase of property, plant and equipment", {"FY2023": -12, "FY2022": -29, "FY2021": -41,
        "FY2020": -29, "FY2019": -120, "FY2018": -150, "FY2017": -100, "FY2016": -98, "FY2015": -50, "FY2014": -41,
        "FY2013": -60.0, "FY2012": -26.8, "FY2011": -17.8, "FY2010": -15.3}),
    ("DATA", "Proceeds from sale of property, plant and equipment and intangible assets", {"FY2017": 0, "FY2016": 0}),
    ("DATA", "Purchase and development of intangible assets", {"FY2023": -26, "FY2022": -24, "FY2021": -64,
        "FY2020": -81, "FY2019": -79, "FY2018": -75, "FY2017": -70, "FY2016": -45, "FY2015": -30, "FY2014": -13,
        "FY2013": -14.2, "FY2012": -2.9, "FY2011": -2.7, "FY2010": -6.4}),
    ("DATA", "Acquisition of subsidiary, net of cash acquired", {"FY2020": -1}),
    ("DATA", "Dividends received from subsidiaries", {"FY2023": 12}),
    ("TOTAL", "Net cash inflows/(outflows) from investing activities", {"FY2023": 1028, "FY2022": -402, "FY2021": -2274,
        "FY2020": -956, "FY2019": 1376, "FY2018": -443, "FY2017": -858, "FY2016": -1349, "FY2015": -480, "FY2014": -957,
        "FY2013": -344.6, "FY2012": -365.3, "FY2011": -59.1, "FY2010": -62.0}),
    ("SECTION", "Cash flows from financing activities", {}),
    ("DATA", "Repayment of preference shares", {"FY2010": -0.1}),
    ("DATA", "Repayment of capital elements of leases", {"FY2023": -23, "FY2022": -25, "FY2021": -27,
        "FY2020": -31, "FY2019": -25}),
    ("DATA", "Issuance of new shares", {"FY2023": 144,
        "FY2019": 375, "FY2018": 304, "FY2017": 279, "FY2016": 404, "FY2014": 99,
        "FY2013": 284.3, "FY2012": 126.0, "FY2010": 120.1}),
    ("DATA", "Cost of share/debt issues", {
        "FY2019": -16, "FY2018": -3, "FY2017": -3, "FY2016": -5, "FY2014": -1}),
    ("DATA", "Issuance of medium-term notes/subordinated debt (net of costs)", {"FY2023": 175, "FY2019": 350, "FY2018": 250}),
    ("DATA", "Cost of debt issued", {"FY2019": -8, "FY2018": -1}),
    ("DATA", "Grant (repaid)/received", {"FY2020": -50, "FY2019": 120}),
    ("TOTAL", "Net cash inflows/(outflows) from financing activities", {"FY2023": 296, "FY2022": -25, "FY2021": -27,
        "FY2020": -81, "FY2019": 796, "FY2018": 550, "FY2017": 276, "FY2016": 398, "FY2015": 0, "FY2014": 99,
        "FY2013": 284.3, "FY2012": 126.0, "FY2011": 0, "FY2010": 120.1}),
    ("TOTAL", "Net increase/(decrease) in cash and cash equivalents", {"FY2023": 1936, "FY2022": -1594, "FY2021": 573,
        "FY2020": 4, "FY2019": 517, "FY2018": 260, "FY2017": 1712, "FY2016": 218, "FY2015": 66, "FY2014": -47,
        "FY2013": 189.1, "FY2012": 16.5, "FY2011": 4.7, "FY2010": 51.6}),
    ("DATA", "Cash and cash equivalents at start of year", {"FY2023": 1953, "FY2022": 3547, "FY2021": 2974,
        "FY2020": 2989, "FY2019": 2472, "FY2018": 2212, "FY2017": 500, "FY2016": 282, "FY2015": 216, "FY2014": 263,
        "FY2013": 74.1, "FY2012": 57.6, "FY2011": 52.9, "FY2010": 1.3}),
    ("TOTAL", "Cash and cash equivalents at end of year", {"FY2023": 3889, "FY2022": 1953, "FY2021": 3547,
        "FY2020": 2993, "FY2019": 2989, "FY2018": 2472, "FY2017": 2212, "FY2016": 500, "FY2015": 282, "FY2014": 216,
        "FY2013": 263.2, "FY2012": 74.1, "FY2011": 57.6, "FY2010": 52.9}),
]

bs_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and balances with the Bank of England", {"FY2023": 3889, "FY2022": 1953, "FY2021": 3547,
        "FY2020": 2993, "FY2019": 2989, "FY2018": 2286, "FY2017": 2112, "FY2016": 435, "FY2015": 218, "FY2014": 181,
        "FY2013": 239.0, "FY2012": 46.7, "FY2011": 35.3, "FY2010": 48.4}),
    ("DATA", "Loans and advances to banks", {"FY2018": 186, "FY2017": 100, "FY2016": 66, "FY2015": 64, "FY2014": 35,
        "FY2013": 24.2, "FY2012": 27.4, "FY2011": 22.2, "FY2010": 4.5}),
    ("DATA", "Loans and advances to customers", {"FY2023": 11844, "FY2022": 12698, "FY2021": 11976,
        "FY2020": 12090, "FY2019": 14681, "FY2018": 14235, "FY2017": 9620, "FY2016": 5865, "FY2015": 3543, "FY2014": 1590,
        "FY2013": 751.1, "FY2012": 167.8, "FY2011": 42.1, "FY2010": 0.1}),
    ("DATA", "Investment securities held at FVOCI", {"FY2023": 476, "FY2022": 571, "FY2021": 798,
        "FY2020": 773, "FY2019": 411, "FY2018": 674}),
    ("DATA", "Investment securities held at amortised cost", {"FY2023": 4403, "FY2022": 5343, "FY2021": 4776,
        "FY2020": 2640, "FY2019": 2154, "FY2018": 3458}),
    ("DATA", "Available-for-sale investment securities (pre-IFRS 9)", {"FY2017": 361, "FY2016": 604, "FY2015": 364, "FY2014": 1304}),
    ("DATA", "Held-to-maturity investment securities (pre-IFRS 9)", {"FY2017": 3554, "FY2016": 2623, "FY2015": 1636, "FY2014": 307,
        "FY2010": 40.3}),
    ("DATA", "Investment securities (undifferentiated basis, HD-074: FY2011-FY2013 note-level AFS/HTM split not sourced this session)", {
        "FY2013": 696.4, "FY2012": 431.2, "FY2011": 81.3}),
    ("DATA", "Financial assets held at fair value through profit and loss", {"FY2022": 1, "FY2021": 3, "FY2020": 30}),
    ("DATA", "Derivative financial assets", {"FY2023": 36, "FY2022": 23}),
    ("DATA", "Property, plant and equipment", {"FY2023": 723, "FY2022": 748, "FY2021": 765,
        "FY2020": 806, "FY2019": 856, "FY2018": 454, "FY2017": 328, "FY2016": 247, "FY2015": 165, "FY2014": 132,
        "FY2013": 104.5, "FY2012": 53.6, "FY2011": 32.3, "FY2010": 17.3}),
    ("DATA", "Investment in subsidiaries", {"FY2023": 15, "FY2022": 31, "FY2021": 31}),
    ("DATA", "Intangible assets", {"FY2023": 188, "FY2022": 204, "FY2021": 231,
        "FY2020": 254, "FY2019": 168, "FY2018": 197, "FY2017": 148, "FY2016": 93, "FY2015": 54, "FY2014": 35,
        "FY2013": 23.8, "FY2012": 10.9, "FY2011": 8.8, "FY2010": 7.0}),
    ("DATA", "Deferred tax asset", {"FY2018": 41, "FY2017": 54, "FY2016": 56, "FY2015": 53, "FY2014": 44,
        "FY2013": 35.8, "FY2012": 25.3, "FY2011": 14.1}),
    ("DATA", "Prepayments and accrued income", {"FY2023": 111, "FY2022": 80, "FY2021": 64,
        "FY2020": 77, "FY2019": 66, "FY2018": 66, "FY2017": 53, "FY2016": 43, "FY2015": 30, "FY2014": 19,
        "FY2013": 5.0, "FY2012": 1.9, "FY2011": 0.8, "FY2010": 0.4}),
    ("DATA", "Assets classified as held for sale", {"FY2022": 1, "FY2020": 295}),
    ("DATA", "Other assets", {"FY2023": 572, "FY2022": 473, "FY2021": 392,
        "FY2020": 2621, "FY2019": 75, "FY2018": 50, "FY2017": 26, "FY2016": 26, "FY2015": 21, "FY2014": 14,
        "FY2013": 11.8, "FY2012": 6.4, "FY2011": 3.3, "FY2010": 1.0}),
    ("TOTAL", "Total assets", {"FY2023": 22257, "FY2022": 22126, "FY2021": 22583,
        "FY2020": 22579, "FY2019": 21400, "FY2018": 21647, "FY2017": 16355, "FY2016": 10057, "FY2015": 6148, "FY2014": 3661,
        "FY2013": 1891.6, "FY2012": 771.2, "FY2011": 240.3, "FY2010": 119.1}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Deposits from customers", {"FY2023": 15623, "FY2022": 16014, "FY2021": 16448,
        "FY2020": 16072, "FY2019": 14477, "FY2018": 15661, "FY2017": 11669, "FY2016": 7951, "FY2015": 5108, "FY2014": 2867,
        "FY2013": 1315.4, "FY2012": 576.3, "FY2011": 151.6, "FY2010": 17.9}),
    ("DATA", "Deposits from central banks", {"FY2023": 3050, "FY2022": 3800, "FY2021": 3800,
        "FY2020": 3808, "FY2019": 3801, "FY2018": 3801, "FY2017": 3321, "FY2016": 543}),
    ("DATA", "Debt securities", {"FY2023": 699, "FY2022": 571, "FY2021": 588,
        "FY2020": 600, "FY2019": 591, "FY2018": 249}),
    ("DATA", "Financial liabilities held at fair value through profit and loss", {"FY2020": 30}),
    ("DATA", "Repurchase agreements", {"FY2023": 1191, "FY2022": 238, "FY2021": 169,
        "FY2020": 196, "FY2019": 250, "FY2018": 344, "FY2017": 122, "FY2016": 653, "FY2015": 562, "FY2014": 283}),
    ("DATA", "Derivative financial liabilities", {"FY2022": 26, "FY2021": 10, "FY2020": 8, "FY2019": 8}),
    ("DATA", "Lease liabilities", {"FY2023": 234, "FY2022": 248, "FY2021": 269, "FY2020": 327, "FY2019": 341}),
    ("DATA", "Deferred grants", {"FY2023": 16, "FY2022": 17, "FY2021": 19, "FY2020": 28, "FY2019": 50}),
    ("DATA", "Provisions", {"FY2023": 23, "FY2022": 7, "FY2021": 15, "FY2020": 11, "FY2019": 17}),
    ("DATA", "Deferred tax liability", {"FY2023": 13, "FY2022": 12, "FY2021": 12, "FY2020": 12, "FY2019": 15}),
    ("DATA", "Other liabilities", {"FY2023": 256, "FY2022": 236, "FY2021": 217,
        "FY2020": 198, "FY2019": 267, "FY2018": 189, "FY2017": 148, "FY2016": 106, "FY2015": 71, "FY2014": 49,
        "FY2013": 171.2, "FY2012": 16.7, "FY2011": 10.7, "FY2010": 4.5}),
    ("TOTAL", "Total liabilities", {"FY2023": 21105, "FY2022": 21169, "FY2021": 21547,
        "FY2020": 21290, "FY2019": 19817, "FY2018": 20244, "FY2017": 15259, "FY2016": 9253, "FY2015": 5741, "FY2014": 3198,
        "FY2013": 1486.6, "FY2012": 593.0, "FY2011": 162.3, "FY2010": 22.3}),
    ("SECTION", "Equity", {}),
    ("DATA", "Called-up share capital", {}),
    ("DATA", "Share premium", {"FY2023": 144, "FY2022": 1964, "FY2021": 1964,
        "FY2020": 1964, "FY2019": 1964, "FY2018": 1605, "FY2017": 1304, "FY2016": 1028, "FY2015": 629, "FY2014": 629,
        "FY2013": 530.5, "FY2012": 246.2, "FY2011": 120.1, "FY2010": 120.1}),
    ("DATA", "Retained earnings/(losses)", {"FY2023": 996, "FY2022": -1014, "FY2021": -941,
        "FY2020": -694, "FY2019": -392, "FY2018": -209, "FY2017": -219, "FY2016": -230, "FY2015": -213, "FY2014": -164,
        "FY2013": -118.7, "FY2012": -76.9, "FY2011": -42.3, "FY2010": -23.3}),
    ("DATA", "Other reserves", {"FY2023": 12, "FY2022": 7, "FY2021": 13,
        "FY2020": 19, "FY2019": 11, "FY2018": 7, "FY2017": 12, "FY2016": 7, "FY2015": -9, "FY2014": -3,
        "FY2013": -6.8, "FY2012": 8.9, "FY2011": 0.2}),
    ("TOTAL", "Total equity", {"FY2023": 1152, "FY2022": 957, "FY2021": 1036,
        "FY2020": 1289, "FY2019": 1583, "FY2018": 1403, "FY2017": 1096, "FY2016": 805, "FY2015": 407, "FY2014": 462,
        "FY2013": 405.0, "FY2012": 178.2, "FY2011": 78.0, "FY2010": 96.8}),
    ("TOTAL", "Total equity and liabilities", {"FY2023": 22257, "FY2022": 22126, "FY2021": 22583,
        "FY2020": 22579, "FY2019": 21400, "FY2018": 21647, "FY2017": 16355, "FY2016": 10057, "FY2015": 6148, "FY2014": 3661,
        "FY2013": 1891.6, "FY2012": 771.2, "FY2011": 240.3, "FY2010": 119.1}),
]

bw.add_balance_sheet_sheet(
    title="Metro Bank PLC - Balance Sheet",
    subtitle="Company/standalone basis, £m; 31 December year-end (FY2013-FY2020 shown on a Group/consolidated "
              "basis instead - see HD-049/HD-074 notes). FY2010 is a 16-month first accounting period. "
              "FY2024-FY2025 not located (see source note) - same basis and gap as the Cash Flow Statement.",
    rows=bs_rows, sources_text=STATEMENTS_SOURCES + "\n\n" + HD074_EXTENSION_NOTE, first_col_width=72, source_height=340, unit_suffix=" (£m)",
)

pl_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest income", {"FY2025": 725.4, "FY2024": 935.4, "FY2023": 855.7, "FY2022": 563.7, "FY2021": 405.7, "FY2020": 426.3, "FY2019": 496.2, "FY2018": 444.4,
        "FY2017": 301.9, "FY2016": 213.5, "FY2015": 125.2, "FY2014": 74.0,
        "FY2013": 27.7, "FY2012": 10.7, "FY2011": 2.0, "FY2010": 0.2}),
    ("DATA", "Interest expense", {"FY2025": -265.1, "FY2024": -557.5, "FY2023": -443.8, "FY2022": -159.6, "FY2021": -110.4, "FY2020": -176.6, "FY2019": -188.1, "FY2018": -114.3,
        "FY2017": -61.0, "FY2016": -59.2, "FY2015": -36.3, "FY2014": -20.6,
        "FY2013": -11.5, "FY2012": -4.7, "FY2011": -0.6, "FY2010": 0.0}),
    ("TOTAL", "Net interest income", {"FY2025": 460.3, "FY2024": 377.9, "FY2023": 411.9, "FY2022": 404.1, "FY2021": 295.3, "FY2020": 249.7, "FY2019": 308.1, "FY2018": 330.1,
        "FY2017": 241.0, "FY2016": 154.2, "FY2015": 88.9, "FY2014": 53.4,
        "FY2013": 16.2, "FY2012": 6.0, "FY2011": 1.4, "FY2010": 0.2}),
    ("DATA", "Fee and commission income", {"FY2025": 96.7, "FY2024": 98.0, "FY2023": 95.0, "FY2022": 84.4, "FY2021": 71.2, "FY2020": 61.1, "FY2019": 67.4, "FY2018": 42.5,
        "FY2017": 29.7, "FY2016": 22.2, "FY2015": 15.7, "FY2014": 12.1,
        "FY2013": 5.7, "FY2012": 2.4, "FY2011": 0.6, "FY2010": 0.0}),
    ("DATA", "Fee and commission expense", {"FY2025": -5.6, "FY2024": -4.8, "FY2023": -4.6, "FY2022": -2.6, "FY2021": -1.6, "FY2020": -1.2, "FY2019": -6.4, "FY2018": -4.9,
        "FY2013": -0.2, "FY2012": -0.2, "FY2011": -0.1}),
    ("TOTAL", "Net fee and commission income", {"FY2025": 91.1, "FY2024": 93.2, "FY2023": 90.4, "FY2022": 81.8, "FY2021": 69.6, "FY2020": 59.9, "FY2019": 61.0, "FY2018": 37.6,
        "FY2017": 29.7, "FY2016": 22.2, "FY2015": 15.7, "FY2014": 12.1,
        "FY2013": 5.5, "FY2012": 2.2, "FY2011": 0.5, "FY2010": 0.0}),
    ("DATA", "Net gain/(loss) on sale of assets", {"FY2025": 5.2, "FY2024": -101.4, "FY2023": 2.7, "FY2021": 9.4, "FY2020": 73.3, "FY2019": 1.6, "FY2018": 10.7,
        "FY2017": 3.7, "FY2016": 5.4, "FY2015": 6.4, "FY2014": 5.1,
        "FY2013": 6.5, "FY2012": 1.7, "FY2011": 2.3}),
    ("DATA", "Other income", {"FY2025": 36.7, "FY2024": 35.6, "FY2023": 143.9, "FY2022": 37.6, "FY2021": 44.2, "FY2020": 49.7, "FY2019": 44.9, "FY2018": 25.7,
        "FY2017": 19.4, "FY2016": 13.3, "FY2015": 9.2, "FY2014": 4.8,
        "FY2013": 3.3, "FY2012": 1.1, "FY2011": 0.2, "FY2010": 0}),
    # FY2014 is an explicit dash in the audited FY2015 consolidated income
    # statement (p.28), i.e. no listing cost was reported in that year.
    ("DATA", "Costs associated with Listing / Listing Share Awards", {"FY2017": -1.4, "FY2016": -5.1, "FY2015": -1.5, "FY2014": 0}),
    ("TOTAL", "Total income", {"FY2025": 593.3, "FY2024": 405.3, "FY2023": 648.9, "FY2022": 523.5, "FY2021": 418.5, "FY2020": 432.6, "FY2019": 415.6, "FY2018": 404.1,
        "FY2017": 293.8, "FY2016": 195.1, "FY2015": 120.2, "FY2014": 75.4,
        "FY2013": 31.5, "FY2012": 11.0, "FY2011": 4.5, "FY2010": 0.2}),
    ("DATA", "General operating expenses", {"FY2025": -429.4, "FY2024": -489.0, "FY2023": -484.1, "FY2022": -467.6, "FY2021": -536.1, "FY2020": -502.3, "FY2019": -380.6, "FY2018": -305.6,
        "FY2017": -231.4, "FY2016": -179.8, "FY2015": -141.6, "FY2014": -107.9,
        "FY2013": -72.3, "FY2012": -50.3, "FY2011": -33.7, "FY2010": -22.0}),
    ("DATA", "Depreciation and amortisation", {"FY2025": -61.7, "FY2024": -77.3, "FY2023": -77.7, "FY2022": -77.0, "FY2021": -80.2, "FY2020": -74.4, "FY2019": -76.4, "FY2018": -45.1,
        "FY2017": -33.4, "FY2016": -22.4, "FY2015": -18.2, "FY2014": -14.2,
        "FY2013": -10.4, "FY2012": -6.2, "FY2011": -3.7, "FY2010": -1.5}),
    ("DATA", "Impairment and write-offs of property, plant, equipment and intangible assets", {"FY2025": -0.7, "FY2024": -44.0, "FY2023": -4.6, "FY2022": -9.7, "FY2021": -24.9, "FY2020": -40.6, "FY2019": -77.7, "FY2018": -4.8,
        "FY2017": -0.6, "FY2016": -0.3, "FY2015": -8.7, "FY2014": 0}),
    ("TOTAL", "Total operating expenses", {"FY2025": -491.8, "FY2024": -610.3, "FY2023": -566.4, "FY2022": -554.3, "FY2021": -641.2, "FY2020": -617.3, "FY2019": -534.7, "FY2018": -355.5,
        "FY2017": -266.9, "FY2016": -207.6, "FY2015": -170.0, "FY2014": -122.2,
        "FY2013": -82.7, "FY2012": -56.6, "FY2011": -37.4, "FY2010": -23.6}),
    ("DATA", "Expected credit loss expense", {"FY2025": -14.3, "FY2024": -7.1, "FY2023": -33.2, "FY2022": -39.9, "FY2021": -22.4, "FY2020": -126.7, "FY2019": -11.7, "FY2018": -8.0}),
    ("DATA", "Credit impairment charges (pre-IFRS 9)", {"FY2017": -8.2, "FY2016": -4.7, "FY2015": -7.0, "FY2014": -2.2,
        "FY2013": -1.0, "FY2012": -0.2, "FY2011": -0.2}),
    ("TOTAL", "Profit/(loss) before tax", {"FY2025": 87.2, "FY2024": -212.1, "FY2023": 49.3, "FY2022": -70.7, "FY2021": -245.1, "FY2020": -311.4, "FY2019": -130.8, "FY2018": 40.6,
        "FY2017": 18.7, "FY2016": -17.2, "FY2015": -56.8, "FY2014": -48.9,
        "FY2013": -52.2, "FY2012": -45.7, "FY2011": -33.1, "FY2010": -23.4}),
    ("DATA", "Taxation credit/(expense)", {"FY2025": -17.5, "FY2024": 254.6, "FY2023": -1.0, "FY2022": -2.0, "FY2021": -3.1, "FY2020": 9.7, "FY2019": -51.8, "FY2018": -13.5,
        "FY2017": -7.9, "FY2016": 0.4, "FY2015": 7.6, "FY2014": 7.8,
        "FY2013": 10.4, "FY2012": 11.2, "FY2011": 14.1, "FY2010": 0}),
    ("TOTAL", "Profit/(loss) for the year", {"FY2025": 69.7, "FY2024": 42.5, "FY2023": 48.3, "FY2022": -72.7, "FY2021": -248.2, "FY2020": -301.7, "FY2019": -182.6, "FY2018": 27.1,
        "FY2017": 10.8, "FY2016": -16.8, "FY2015": -49.2, "FY2014": -41.1,
        "FY2013": -41.8, "FY2012": -34.6, "FY2011": -19.0, "FY2010": -23.4}),
    ("SECTION", "Other comprehensive income/(expense) for the year", {}),
    ("DATA", "Movement in investment securities held at FVOCI - changes in fair value (net of tax)", {"FY2025": 4.2, "FY2024": 3.4, "FY2023": 2.4, "FY2022": -7.6, "FY2021": -8.1, "FY2020": 5.6, "FY2019": 2.7, "FY2018": -2.4,
        "FY2017": 2.7, "FY2016": 13.9, "FY2015": -1.3, "FY2014": 8.3,
        "FY2013": -16.1, "FY2012": 8.5, "FY2011": 0.1}),
    ("DATA", "FV changes transferred to the income statement on disposal (net of tax)", {"FY2021": -0.3, "FY2020": -0.1, "FY2019": -2.4, "FY2018": -1.5,
        "FY2017": -3.7, "FY2016": -5.4, "FY2015": -6.4, "FY2014": -5.1}),
    ("TOTAL", "Total other comprehensive income/(expense)", {"FY2025": 4.2, "FY2024": 3.4, "FY2023": 2.4, "FY2022": -7.6, "FY2021": -8.4, "FY2020": 5.5, "FY2019": 0.3, "FY2018": -3.9,
        "FY2017": -0.9, "FY2016": 8.5, "FY2015": -7.7, "FY2014": 3.2,
        "FY2013": -16.1, "FY2012": 8.5, "FY2011": 0.1, "FY2010": 0}),
    ("TOTAL", "Total comprehensive income/(loss) for the year", {"FY2025": 73.9, "FY2024": 45.9, "FY2023": 50.7, "FY2022": -80.3, "FY2021": -256.6, "FY2020": -296.2, "FY2019": -182.3, "FY2018": 23.2,
        "FY2017": 9.8, "FY2016": -8.2, "FY2015": -56.9, "FY2014": -37.9,
        "FY2013": -57.9, "FY2012": -26.1, "FY2011": -18.9, "FY2010": -23.4}),
]

bw.add_income_statement_sheet(
    title="Metro Bank PLC - Profit & Loss",
    subtitle="Group/consolidated basis, £m (Metro Bank PLC does not publish its own standalone income statement in "
              "any year reviewed - see source note). FY2010-FY2012 had no subsidiaries yet, so Company and Group "
              "are identical for those years; FY2010 is a 16-month first accounting period (see HD-074 note).",
    rows=pl_rows, sources_text=STATEMENTS_SOURCES + "\n\n" + HD074_EXTENSION_NOTE, first_col_width=78, source_height=340, unit_suffix=" (£m)",
)

equity_headers = ["Called-up share capital", "Share premium", "Retained earnings/(losses)", "FVOCI reserve",
                   "Share option reserve", "Deemed capital contribution", "Total equity"]
equity_rows = [
    ("TOTAL", "Balance at 19 September 2009 (opening, Company basis - conversion to PLC)", (0.1, 0, 0.0, None, None, None, 0.1)),
    ("DATA", "Net loss for the period (16 months to 31 December 2010)", (None, None, -23.4, None, None, None, -23.4)),
    ("DATA", "Issue of new ordinary shares", (None, 120.1, None, None, None, None, 120.1)),
    ("DATA", "Repayment of preference shares", (-0.1, None, None, None, None, None, -0.1)),
    ("TOTAL", "Balance as at 31 December 2010 (FY2010 closing, 16-month first accounts, Company basis)", (0, 120.1, -23.3, None, None, None, 96.8)),
    ("DATA", "Net loss for the year", (None, None, -19.0, None, None, None, -19.0)),
    ("DATA", "Other comprehensive income relating to available-for-sale investments, net of tax", (None, None, None, 0.1, None, None, 0.1)),
    ("DATA", "Share options at fair value", (None, None, None, None, 0.1, None, 0.1)),
    ("TOTAL", "Balance as at 31 December 2011 (FY2011 closing, Company basis)", (0, 120.1, -42.3, 0.1, 0.1, None, 78.0)),
    ("DATA", "Share issue", (None, 126.0, None, None, None, None, 126.0)),
    ("DATA", "Net loss for the year", (None, None, -34.6, None, None, None, -34.6)),
    ("DATA", "Other comprehensive income relating to available-for-sale investments, net of tax", (None, None, None, 8.5, None, None, 8.5)),
    ("DATA", "Share options at fair value", (None, None, None, None, 0.3, None, 0.3)),
    ("TOTAL", "Balance as at 31 December 2012 (FY2012 closing, Company basis)", (0, 246.2, -76.9, 8.6, 0.4, None, 178.2)),
    ("DATA", "Share issue", (None, 284.3, None, None, None, None, 284.3)),
    ("DATA", "Net loss for the year", (None, None, -41.8, None, None, None, -41.8)),
    ("DATA", "Other comprehensive expense relating to available-for-sale investments, net of tax", (None, None, None, -16.1, None, None, -16.1)),
    ("DATA", "Share options at fair value", (None, None, None, None, 0.4, None, 0.4)),
    # HD-074: this genuine FY2013 closing (Group basis, own contemporaneous
    # figures) does not tie to the pre-existing "FY2014 opening, restated"
    # row immediately below (share premium 530.5 vs 530, retained earnings
    # -118.7 vs -123) - the FY2014 opening figure was already sourced from
    # the FY2015 Annual Report's own "restated" FY2014 comparative column
    # (see HD-049's DATA QUALITY FLAG above; note 36 of the 2015 AR
    # references undisclosed prior-period adjustments behind that label).
    # This is a genuine restatement discontinuity at the FY2013/FY2014
    # boundary, flagged rather than silently blended - consistent with how
    # this sheet already flags the FY2020/FY2021 Group/Company basis change.
    ("TOTAL", "Balance as at 31 December 2013 (FY2013 closing, own contemporaneous figures, Group basis)", (0, 530.5, -118.7, -7.5, 0.8, None, 405.0)),
    ("TOTAL", "At 1 January 2014 (FY2014 opening, restated, Group basis)", (0, 530, -123, -8, 1, None, 401)),
    ("DATA", "Loss for the year", (None, None, -41, None, None, None, -41)),
    ("DATA", "Other comprehensive income relating to available-for-sale investments, net of tax", (None, None, None, 3, None, None, 3)),
    ("DATA", "Share issue", (None, 99, None, None, None, None, 99)),
    ("DATA", "Share options at fair value", (None, None, None, None, 1, None, 1)),
    ("TOTAL", "At 31 December 2014 (FY2014 closing, restated)", (0, 629, -164, -4, 2, None, 462)),
    ("DATA", "Loss for the year", (None, None, -49, None, None, None, -49)),
    ("DATA", "Other comprehensive expense relating to available-for-sale investments, net of tax", (None, None, None, -8, None, None, -8)),
    ("DATA", "Share options at fair value", (None, None, None, None, 2, None, 2)),
    ("TOTAL", "At 31 December 2015 (FY2015 closing)", (0, 629, -213, -12, 3, None, 407)),
    ("DATA", "Loss for the year", (None, None, -17, None, None, None, -17)),
    ("DATA", "Other comprehensive income relating to available-for-sale investments, net of tax", (None, None, None, 9, None, None, 9)),
    ("DATA", "Share issue", (None, 404, None, None, None, None, 404)),
    ("DATA", "Cost of share issue", (None, -5, None, None, None, None, -5)),
    ("DATA", "Share options at fair value", (None, None, None, None, 7, None, 7)),
    ("TOTAL", "At 31 December 2016 (FY2016 closing)", (0, 1028, -230, -3, 11, None, 805)),
    ("DATA", "Profit for the year", (None, None, 11, None, None, None, 11)),
    ("DATA", "Other comprehensive expense relating to available-for-sale investments, net of tax", (None, None, None, -1, None, None, -1)),
    ("DATA", "Share issue", (None, 279, None, None, None, None, 279)),
    ("DATA", "Cost of share issue", (None, -3, None, None, None, None, -3)),
    ("DATA", "Net share option movements", (None, None, None, None, 6, None, 6)),
    ("TOTAL", "At 31 December 2017 (FY2017 closing)", (0, 1304, -219, -4, 16, None, 1096)),
    ("DATA", "IFRS 9 transition adjustment, net of tax (AFS reserve replaced by FVOCI reserve)", (None, None, -17, 5, None, None, -12)),
    ("DATA", "Profit for the year", (None, None, 27, None, None, None, 27)),
    ("DATA", "Other comprehensive expense relating to investment securities designated at FVOCI, net of tax", (None, None, None, -4, None, None, -4)),
    ("DATA", "Shares issued", (None, 304, None, None, None, None, 304)),
    ("DATA", "Cost of shares issued", (None, -3, None, None, None, None, -3)),
    ("DATA", "Net share option movements", (None, None, None, None, -6, None, -6)),
    ("TOTAL", "At 31 December 2018 (FY2018 closing)", (0, 1605, -209, -3, 10, None, 1403)),
    ("DATA", "Loss for the year", (None, None, -183, None, None, None, -183)),
    ("DATA", "Shares issued", (None, 375, None, None, None, None, 375)),
    ("DATA", "Cost of shares issued", (None, -16, None, None, None, None, -16)),
    ("DATA", "Net share option movements", (None, None, None, None, 4, None, 4)),
    ("TOTAL", "At 31 December 2019 (FY2019 closing)", (0, 1964, -392, -3, 14, None, 1583)),
    ("DATA", "Loss for the year", (None, None, -302, None, None, None, -302)),
    ("DATA", "Other comprehensive income relating to investment securities designated at FVOCI, net of tax", (None, None, None, 6, None, None, 6)),
    ("DATA", "Net share option movements", (None, None, None, None, 2, None, 2)),
    ("TOTAL", "At 31 December 2020 (FY2020 closing, Group basis)", (0, 1964, -694, 3, 16, None, 1289)),
    ("TOTAL", "At 1 January 2021 (FY2021 opening)", (0, 1964, -689, 3, 16, None, 1294)),
    ("DATA", "Loss for the year", (None, None, -252, None, None, None, -252)),
    ("DATA", "Other comprehensive expense relating to investment securities designated at FVOCI, net of tax", (None, None, None, -8, None, None, -8)),
    ("DATA", "Net share option movements", (None, None, None, None, 2, None, 2)),
    ("TOTAL", "At 31 December 2021 (FY2021 closing)", (0, 1964, -941, -5, 18, None, 1036)),
    ("DATA", "Loss for the year", (None, None, -73, None, None, None, -73)),
    ("DATA", "Other comprehensive expense relating to investment securities designated at FVOCI, net of tax", (None, None, None, -8, None, None, -8)),
    ("DATA", "Net share option movements", (None, None, None, None, 2, None, 2)),
    ("TOTAL", "At 31 December 2022 (FY2022 closing)", (0, 1964, -1014, -13, 20, None, 957)),
    ("DATA", "Profit for the year", (None, None, 46, None, None, None, 46)),
    ("DATA", "Other comprehensive income relating to investment securities designated at FVOCI, net of tax", (None, None, None, 2, None, None, 2)),
    ("DATA", "Net share option movements", (None, None, None, None, 3, None, 3)),
    ("DATA", "Transfer of share option reserve upon insertion of new holding company", (None, None, None, None, -23, 23, 0)),
    ("DATA", "Cancellation of Metro Bank PLC share capital and share premium", (None, -1964, 1964, None, None, None, 0)),
    ("DATA", "Shares issued", (None, 144, None, None, None, None, 144)),
    ("TOTAL", "At 31 December 2023 (FY2023 closing)", (0, 144, 996, -11, 0, 23, 1152)),
]

bw.add_equity_changes_sheet(
    title="Metro Bank PLC - Statement of Changes in Equity",
    subtitle="Chronological roll-forward, oldest to newest, £m. FY2010-FY2013 are Company basis (HD-074; FY2010 "
              "is a 16-month first accounting period); FY2013's closing is nonetheless Group/consolidated, Metro "
              "Bank's first subsidiary having been acquired that July - see HD-074 note. FY2014-FY2020 are "
              "Group/consolidated basis; FY2021-FY2023 are Company/standalone basis (see HD-049 basis note); "
              "FY2024-FY2025 not located - same gap as the Balance Sheet and Cash Flow Statement. Equity "
              "reconciliation ladder confirmed: each year's own closing balance ties exactly to both the next "
              "year's own opening balance and that year's own Balance Sheet Total equity within each basis, EXCEPT "
              "at the FY2013/FY2014 boundary, where the pre-existing FY2014 opening row uses the FY2015 Annual "
              "Report's own 'restated' FY2014 comparative rather than FY2013's own contemporaneous closing figures "
              "- a genuine restatement discontinuity, flagged in place rather than silently blended (see the note "
              "on that row). The ladder's mandated scan caught the insertion "
              "of Metro Bank Holdings PLC as new ultimate parent in 2023 - a genuine cancellation of Metro Bank "
              "PLC's £1,964m share capital/premium (offset into retained earnings) and £144m of new shares issued, "
              "not a plug - and also the genuine Company/Group basis discontinuity at 31 Dec 2020/1 Jan 2021 "
              "(£1,289m Group closing vs £1,294m Company opening), which is a basis change, not an error. The "
              "'FVOCI reserve' column holds the pre-2018 'Available-for-sale reserve' for FY2010-FY2017 (same "
              "underlying reserve, renamed on IFRS 9 adoption 1 January 2018 - see the transition adjustment row).",
    headers=equity_headers,
    rows=equity_rows,
    sources_text=STATEMENTS_SOURCES + "\n\n" + HD074_EXTENSION_NOTE,
    first_col_width=46,
)

bw.add_cash_flow_sheet(
    title="Metro Bank PLC - Cash Flow Statement",
    subtitle="£m; 31 December year-end. FY2010-FY2012 are Company (own, pre-subsidiary); FY2013 is Group "
              "(HD-074); FY2014-FY2020 are Group/consolidated (as reported, itemized adjustments); "
              "FY2021-FY2023 are Company/standalone (as reported, collapsed to 'Adjustments for non-cash items' "
              "plus memo interest received/paid) - see HD-049 basis note. FY2024-FY2025 standalone accounts not "
              "located.",
    rows=cash_rows, sources_text=CASH_SOURCES + (
        "\n\nHD-049: FY2014-FY2020 reproduce each year's own Consolidated Cash Flow Statement line items "
        "(impairment/write-offs, D&A, share option charge, gain on sale, accrued interest, lease interest, grant "
        "income, amounts provided for) rather than collapsing them into 'Adjustments for non-cash items' as the "
        "Company statement does for FY2021-FY2023 - both presentations are as-reported, not reclassified by this "
        "workbook.\n\nHD-074: FY2010-FY2013 similarly reproduce each year's own reported line items - see the "
        "HD-074 note above for the net-vs-gross investment-securities purchase distinction across these years."
    ), first_col_width=72, source_height=260, unit_suffix=" (£m)",
)

asset_quality_rows = [
    ("SECTION", "Gross carrying amount by portfolio, Group basis", {}),
    ("DATA", "Retail mortgages", {"FY2025": 4940, "FY2024": 5145, "FY2023": 7817, "FY2022": 7649, "FY2021": 6723}),
    ("DATA", "Consumer lending", {"FY2025": 114, "FY2024": 745, "FY2023": 1297, "FY2022": 1480, "FY2021": 890}),
    ("DATA", "Commercial / corporate and commercial lending", {"FY2025": 3939, "FY2024": 3314, "FY2023": 3382, "FY2022": 4160, "FY2021": 4846}),
    ("TOTAL", "Total loans and advances to customers, gross", {"FY2025": 8993, "FY2024": 9204, "FY2023": 12496, "FY2022": 13289, "FY2021": 12459}),
    ("DATA", "ECL allowance - retail mortgages", {"FY2025": -16, "FY2024": -15, "FY2023": -19, "FY2022": -20, "FY2021": -19}),
    ("DATA", "ECL allowance - consumer lending", {"FY2025": -67, "FY2024": -108, "FY2023": -108, "FY2022": -75, "FY2021": -42}),
    ("DATA", "ECL allowance - commercial / corporate and commercial lending", {"FY2025": -87, "FY2024": -68, "FY2023": -72, "FY2022": -92, "FY2021": -108}),
    ("TOTAL", "Total ECL allowance", {"FY2025": -170, "FY2024": -191, "FY2023": -199, "FY2022": -187, "FY2021": -169}),
    ("TOTAL", "Total loans and advances to customers, net", {"FY2025": 8823, "FY2024": 9013, "FY2023": 12297, "FY2022": 13102, "FY2021": 12290}),
    ("SECTION", "IFRS 9 stage split and coverage, portfolio-total level", {}),
    ("DATA", "Stage 1, gross carrying amount", {"FY2025": 7819, "FY2024": 7723}),
    ("DATA", "Stage 2, gross carrying amount", {"FY2025": 713, "FY2024": 978}),
    ("DATA", "Stage 3, gross carrying amount", {"FY2025": 462, "FY2024": 504}),
    ("DATA", "% loans in Stage 2", {"FY2025": "7.9%", "FY2024": "11%", "FY2023": "12%", "FY2022": "16%", "FY2021": "15%"}),
    ("DATA", "% loans in Stage 3", {"FY2025": "5.1%", "FY2024": "5%", "FY2023": "3%", "FY2022": "3%", "FY2021": "4%"}),
    ("DATA", "Coverage ratio (ECL allowance / gross lending, including Stage 3)", {"FY2025": "1.89%", "FY2024": "2.07%", "FY2023": "1.59%", "FY2022": "1.41%", "FY2021": "1.36%"}),
    ("DATA", "90+ days past due", {"FY2024": "3%", "FY2023": "2%", "FY2022": "1%", "FY2021": "2%"}),
    ("SECTION", "Non-performing loans (NPLs) by portfolio", {}),
    ("DATA", "Retail mortgages NPLs", {"FY2025": 220, "FY2024": 203, "FY2023": 146, "FY2022": 111, "FY2021": 114,
        "FY2020": 118, "FY2019": 25, "FY2018": 9}),
    ("DATA", "Consumer NPLs", {"FY2025": 74, "FY2024": 97, "FY2023": 77, "FY2022": 50, "FY2021": 21,
        "FY2020": 13, "FY2019": 10, "FY2018": 5}),
    ("DATA", "Commercial / corporate and commercial NPLs", {"FY2025": 168, "FY2024": 204, "FY2023": 166, "FY2022": 191, "FY2021": 327,
        "FY2020": 127, "FY2019": 42, "FY2018": 7}),
    ("TOTAL", "Total NPLs", {"FY2025": 462, "FY2024": 504, "FY2023": 389, "FY2022": 352, "FY2021": 462,
        "FY2020": 258, "FY2019": 77, "FY2018": 21}),
    ("DATA", "Total NPL ratio", {"FY2025": "5.14%", "FY2024": "5.48%", "FY2023": "3.11%", "FY2022": "2.65%", "FY2021": "3.71%",
        "FY2020": "2.10%", "FY2019": "0.53%", "FY2018": "0.15%", "FY2017": "0.27%"}),
]

bw.add_asset_quality_sheet(
    title="Metro Bank PLC - Asset Quality",
    subtitle="Group/consolidated basis, £m (Group loans and advances to customers ties exactly to the Consolidated "
              "Balance Sheet, not the Company balance sheet above - see source note).",
    rows=asset_quality_rows,
    sources_text=STATEMENTS_SOURCES + (
        "\n\nAsset Quality tables: FY2025 - AR2025 'Table 1' (Financial review, p.17) and Note 30 Expected credit "
        "loss (p.185-186); FY2024 - AR2024 'Table 1'/'Table 2'/'Table 3' (Financial risks, p.126-127) and Note 30; "
        "FY2023 - AR2023 'Table 1'/'Table 2'/'Table 3' (Financial risks, p.62-63); FY2022 - AR2022 'Table 1'/'Table "
        "2' (Risk report, p.72-74) and AR2023's FY2022 comparative for 'Table 3' NPLs by portfolio; FY2021 - AR2022's "
        "FY2021 comparative for 'Table 1'/'Table 2', and AR2021's own 'Table 1: Non-performing loans' (p.69).\n\n"
        "DATA QUALITY NOTE: FY2025's % Stage 2/% Stage 3 are computed here from Note 30's absolute Stage 1/2/3 gross "
        "carrying amounts (713/8,993 and 462/8,993) rather than a disclosed percentage - AR2025 stopped disclosing "
        "the FY2021-FY2024 'Table 2: Total portfolio credit performance' percentage table in that exact form. FY2025's "
        "90+ days past due percentage was not located in the reviewed disclosure and is left blank rather than "
        "estimated. 'Commercial lending' (FY2021-FY2024 label) and 'Corporate and commercial' (FY2025 label) are the "
        "same portfolio, simply relabelled between years.\n\n"
        "HD-049: FY2018-FY2020 NPLs by portfolio and Total NPL ratio are from each AR's own 'Table 9: Non-performing "
        "loans' (labelled 'Retail-residential mortgages'/'Retail-consumer and other'/'Commercial (including asset "
        "and invoice finance)' - the same three portfolios as the FY2021+ rows above, under earlier labels). FY2017's "
        "Total NPL ratio (0.27%) is a prior-year comparator quoted in AR2018's own narrative; no portfolio breakdown "
        "or FY2014-FY2016 NPL/stage data was located within this session's effort. Gross carrying amount by "
        "portfolio, ECL allowance by portfolio, and IFRS 9 stage split are not populated for FY2014-FY2020: FY2014-"
        "FY2017 pre-date IFRS 9 (incurred-loss model, no stage concept, and portfolio-level gross/ECL tables in a "
        "comparable format were not located), and FY2018-FY2020's portfolio-level gross/ECL tables were not "
        "extracted this session (only the Group Balance Sheet's single net loans and advances to customers figure "
        "and the NPL table above were sourced) - left blank rather than estimated."
    ),
    first_col_width=76,
    source_height=340,
    unit_suffix=" (£m)",
    years=PILLAR3_YEARS,
)


def vals(data):
    return {y: data.get(y) for y in PILLAR3_YEARS}


def metric(name, unit, rows_data, note=None):
    bw.add_metric_sheet(name, unit, rows_data, P3_SOURCES, note=note, first_col_width=56, source_height=190, years=PILLAR3_YEARS)


metric("CET1 Capital", "£m", [("Common Equity Tier 1 (CET1) capital", vals({"FY2025": 840, "FY2024": 808, "FY2023": 985, "FY2022": 819, "FY2021": 936,
       "FY2020": 1192, "FY2019": 1427, "FY2018": 1171, "FY2017": 897, "FY2016": 651, "FY2015": 300, "FY2014": 384}))],
       "FY2023-FY2025 are Holdings Group figures following the May 2023 holding-company insertion; FY2021-FY2022 are Metro Bank PLC consolidated prudential figures. CORRECTED 2026-09-03 (ST-026): FY2023-FY2025 previously showed the 30 June interim KM1 column instead of the 31 December year-end column (e.g. FY2024 was 937, the 30 June 2024 figure - the year-end figure is 808); found while cross-checking against the RWA Breakdown sheet's own OV1/KM1 source tables. FY2021-FY2022 were already correct. HD-049: FY2014/FY2015 are Total regulatory capital (=CET1=Tier1=Total capital, no AT1/Tier 2 disclosed in either year) from the Annual Report's own Capital management note/capital structure table, not a Pillar 3 disclosure - see P3_SOURCES note.")
metric("CET1 Ratio", "%", [("Common Equity Tier 1 ratio", vals({"FY2025": "12.5%", "FY2024": "12.5%", "FY2023": "13.1%", "FY2022": "10.3%", "FY2021": "12.6%",
       "FY2020": "15.0%", "FY2019": "15.6%", "FY2018": "13.1%", "FY2017": "15.25%", "FY2016": "18.16%", "FY2015": "13%", "FY2014": "28%"}))],
       "CORRECTED 2026-09-03 (ST-026): FY2023-FY2025 previously showed the 30 June interim column instead of 31 December year-end (see CET1 Capital sheet's note). HD-049: FY2014/FY2015 from the Annual Report (not Pillar 3) - see CET1 Capital sheet's note.")
metric("Tier 1 Capital", "£m", [("Tier 1 capital", vals({"FY2025": 1082, "FY2024": 808, "FY2023": 985, "FY2022": 819, "FY2021": 936,
       "FY2020": 1192, "FY2019": 1427, "FY2018": 1171, "FY2017": 897, "FY2016": 651, "FY2015": 300, "FY2014": 384}))],
       "CORRECTED 2026-09-03 (ST-026): FY2023-FY2025 previously showed the 30 June interim column instead of 31 December year-end (see CET1 Capital sheet's note). HD-049: FY2014-FY2017 Tier 1 = CET1 (no AT1 disclosed) - see CET1 Capital sheet's note.")
metric("Tier 1 Ratio", "%", [("Tier 1 ratio", vals({"FY2025": "16.1%", "FY2024": "12.5%", "FY2023": "13.1%", "FY2022": "10.3%", "FY2021": "12.6%",
       "FY2020": "15.0%", "FY2019": "15.6%", "FY2018": "13.1%", "FY2017": "15.25%", "FY2016": "18.16%", "FY2015": "13%", "FY2014": "28%"}))],
       "CORRECTED 2026-09-03 (ST-026): FY2023-FY2025 previously showed the 30 June interim column instead of 31 December year-end (see CET1 Capital sheet's note). HD-049: FY2014-FY2017 Tier 1 ratio = CET1 ratio (no AT1 disclosed).")
metric("Total Capital", "£m", [("Total capital", vals({"FY2025": 1232, "FY2024": 958, "FY2023": 1135, "FY2022": 1069, "FY2021": 1184,
       "FY2020": 1441, "FY2019": 1676, "FY2018": 1420, "FY2017": 897, "FY2016": 651, "FY2015": 300, "FY2014": 384}))],
       "CORRECTED 2026-09-03 (ST-026): FY2023-FY2025 previously showed the 30 June interim column instead of 31 December year-end (see CET1 Capital sheet's note). HD-049: FY2014-FY2017 Total capital = Tier 1 (no Tier 2 disclosed until FY2018's £249m debt securities). FY2014/FY2015 from the Annual Report, not Pillar 3.")
metric("Total Capital Ratio", "%", [("Total capital ratio", vals({"FY2025": "18.4%", "FY2024": "14.9%", "FY2023": "15.1%", "FY2022": "13.4%", "FY2021": "15.9%",
       "FY2020": "18.1%", "FY2019": "18.3%", "FY2018": "15.9%", "FY2017": "15.25%", "FY2016": "18.16%", "FY2015": "13%", "FY2014": "28%"}))],
       "CORRECTED 2026-09-03 (ST-026): FY2023-FY2025 previously showed the 30 June interim column instead of 31 December year-end (see CET1 Capital sheet's note). HD-049: FY2014-FY2017 Total capital ratio = CET1 ratio (no Tier 2 disclosed).")
metric("Total RWAs", "£m", [("Total risk-weighted exposure amount", vals({"FY2025": 6711, "FY2024": 6442, "FY2023": 7533, "FY2022": 7990, "FY2021": 7454,
       "FY2020": 7957, "FY2019": 9147, "FY2018": 8936, "FY2017": 5882, "FY2016": 3590}))],
       "CORRECTED 2026-09-03 (ST-026): FY2023-FY2025 previously showed the 30 June interim column instead of 31 December year-end (e.g. FY2024 was 7239, the 30 June 2024 figure - the year-end figure is 6442, confirmed against both the KM1 Key metrics table and the OV1 RWA-by-risk-type table, and against the RWA Breakdown sheet's own total). FY2021-FY2022 were already correct. HD-049: FY2014/FY2015 RWAs were not disclosed in the Annual Report (only capital and ratios) and are left blank rather than derived by dividing capital by the ratio.")

rwa_breakdown_rows = [
    ("DATA", "Credit risk (excluding counterparty credit risk)", vals({"FY2025": 5793, "FY2024": 5572, "FY2023": 6667, "FY2022": 7071, "FY2021": 6444,
        "FY2020": 7251, "FY2019": 8591, "FY2018": 8560, "FY2017": 5020, "FY2016": 2959})),
    ("DATA", "Counterparty credit risk", vals({"FY2025": 5, "FY2024": 19, "FY2023": 26, "FY2022": 9, "FY2021": 6,
        "FY2020": 7, "FY2019": 5, "FY2018": 2, "FY2017": 0, "FY2016": 0})),
    ("DATA", "Securitisation exposures in the banking book (after the cap)", vals({"FY2025": 138, "FY2024": 124, "FY2023": 129, "FY2022": 166, "FY2021": 261,
        "FY2017": 626, "FY2016": 494})),
    ("DATA", "Market risk", vals({"FY2022": 0, "FY2021": 9, "FY2020": 14, "FY2019": 5, "FY2018": 4, "FY2017": 2, "FY2016": 1})),
    ("DATA", "Operational risk", vals({"FY2025": 759, "FY2024": 720, "FY2023": 703, "FY2022": 739, "FY2021": 729,
        "FY2020": 686, "FY2019": 546, "FY2018": 370, "FY2017": 234, "FY2016": 136})),
    ("DATA", "Amounts below the thresholds for deduction (subject to 250% risk weight)", vals({"FY2025": 16, "FY2024": 7, "FY2023": 8, "FY2022": 5, "FY2021": 5})),
    ("TOTAL", "Total", vals({"FY2025": 6711, "FY2024": 6442, "FY2023": 7533, "FY2022": 7990, "FY2021": 7454,
        "FY2020": 7957, "FY2019": 9147, "FY2018": 8936, "FY2017": 5882, "FY2016": 3590})),
]
bw.add_rwa_breakdown_sheet(
    title="Metro Bank PLC - RWA Breakdown",
    subtitle="Pillar 3 UK/EU OV1 template. FY2023-FY2025 are Holdings Group figures; FY2021-FY2022 are the Metro "
              "Bank PLC prudential perimeter (same basis split as the other Pillar 3 sheets).",
    rows=rwa_breakdown_rows,
    sources_text=P3_SOURCES + (
        "\n\nRWA Breakdown table: FY2025 - Pillar 3 Disclosure 2025, Table 6 UK OV1, p.12. FY2024 - Pillar 3 "
        "Disclosure 2024, Table 6 UK OV1, p.14. FY2023 - Pillar 3 Disclosure 2023, Table 6 UK OV1, p.14. FY2022 - "
        "Pillar 3 Disclosure 2022, Table 5 UK OV1, p.12. FY2021 - Pillar 3 Disclosure 2021, Table 10 EU OV1, p.52. "
        "All 5 years' totals tie exactly to the (corrected) Total RWAs sheet.\n\n"
        "HD-049: FY2020/FY2019/FY2018 - Pillar 3 2020/2019/2018 EU OV1 tables (no separate securitisation line - "
        "embedded within credit risk under the post-2018 template, hence blank). FY2017/FY2016 - each year's own "
        "'Risk Weighted Assets - Pillar 1' table in the 2017 Pillar 3 Disclosure (Credit risk shown standardised "
        "approach, securitisation broken out separately under the pre-2018 template)."
    ),
    first_col_width=68,
    source_height=250,
    years=PILLAR3_YEARS,
    unit_suffix=" (£m)",
)

metric("Leverage Ratio", "£m / %", [
    ("Total exposure measure excluding claims on central banks", vals({"FY2025": 13837, "FY2024": 14417, "FY2023": 18420, "FY2022": 19348, "FY2021": 17869})),
    ("Leverage ratio excluding claims on central banks", vals({"FY2025": "7.8%", "FY2024": "5.6%", "FY2023": "5.3%", "FY2022": "4.2%", "FY2021": "5.2%"})),
    ("Total exposure measure (as originally disclosed, including central bank claims)", vals({
        "FY2020": None, "FY2019": 21506, "FY2018": 21704, "FY2017": 16450, "FY2016": 10004})),
    ("Regulatory leverage ratio (as originally disclosed, including central bank claims)", vals({
        "FY2020": "5.6%", "FY2019": "6.6%", "FY2018": "5.4%", "FY2017": "5.5%", "FY2016": "6.5%", "FY2015": "4.9%", "FY2014": "10%"})),
], note="The 2023-2025 figures are Holdings Group figures; 2021-2022 are the Metro Bank PLC prudential perimeter. The 2021-2022 disclosures restate the leverage measure to exclude central-bank claims for comparability. CORRECTED 2026-09-03 (ST-026): FY2023-FY2025 previously showed the 30 June interim column instead of 31 December year-end. HD-049: FY2014-FY2020 predate the 2021-2022 central-bank-claims exclusion methodology entirely, so a separate pair of rows is used for the as-originally-disclosed 'Regulatory leverage ratio' (including central bank claims) rather than conflating the two definitions; FY2020's total exposure measure was not located (only the ratio) and is left blank.")
metric("LCR", "£m / %", [
    ("Total high-quality liquid assets (HQLA), weighted value - average", vals({"FY2025": 5552, "FY2024": 7189, "FY2023": 5056, "FY2022": 6051, "FY2021": 6900,
        "FY2019": 3356, "FY2018": 3489})),
    ("Total net cash outflows, adjusted value", vals({"FY2025": 1773, "FY2024": 1854, "FY2023": 2079, "FY2022": 2465, "FY2021": 2169,
        "FY2019": 1708, "FY2018": 2506})),
    ("Liquidity Coverage Ratio", vals({"FY2025": "314%", "FY2024": "444%", "FY2023": "244%", "FY2022": "246%", "FY2021": "281%",
        "FY2020": "187%", "FY2019": "197%", "FY2018": "139%", "FY2017": "141%", "FY2016": "136%"})),
], note="The source tables disclose HQLA/net outflow components on different reporting bases across years; the headline ratios are reproduced as reported. Basis changes after the holding-company insertion are described on the Cash Flow Statement and source note. CORRECTED 2026-09-03 (ST-026): FY2023-FY2025 previously showed the 30 June interim column instead of 31 December year-end. HD-049: FY2020 and FY2014/FY2015 absolute HQLA/net outflow £m were not located (Pillar 3 2020 discloses only the ratio in the executive summary reviewed this session; FY2014/FY2015 have no LCR disclosure at all) and are left blank rather than estimated.")
metric("NSFR", "£m / %", [
    ("Total available stable funding", vals({"FY2025": 13965, "FY2024": 16676, "FY2023": 18277, "FY2022": 18903})),
    ("Total required stable funding", vals({"FY2025": 8448, "FY2024": 10475, "FY2023": 13442, "FY2022": 13225})),
    ("Net stable funding ratio", vals({"FY2025": "165%", "FY2024": "160%", "FY2023": "136%", "FY2022": "143%"})),
], note="NSFR disclosures were required from 1 January 2023; FY2014-FY2021 are blank (not yet a UK/EU disclosure requirement). FY2023-FY2025 are Holdings Group figures after the restructure. CORRECTED 2026-09-03 (ST-026): FY2023-FY2025 previously showed the 30 June interim column instead of 31 December year-end.")
metric("MREL Ratio", "%", [("MREL ratio", vals({"FY2021": "20.5%", "FY2022": "Not disclosed", "FY2023": "Not disclosed", "FY2024": "Not disclosed", "FY2025": "Not disclosed",
       "FY2020": "22.4% (total capital plus MREL ratio)", "FY2019": "22.1% (total capital plus MREL ratio)", "FY2018": "Not disclosed (pre-dates MREL requirement)", "FY2017": "Not disclosed (pre-dates MREL requirement)", "FY2016": "Not disclosed (pre-dates MREL requirement)", "FY2015": "Not disclosed (pre-dates MREL requirement)", "FY2014": "Not disclosed (pre-dates MREL requirement)"}))],
       "The 2021 Pillar 3 report discloses 20.5%. No quantitative MREL ratio was located in the later KM1 tables reviewed; the 2022-2025 cells are therefore not publicly disclosed rather than zero. HD-049: FY2019/FY2020 Pillar 3 disclosures report a 'Total capital plus MREL ratio' (22.1%/22.4%) rather than a standalone MREL ratio - a different (broader) metric than the FY2021 '20.5%', reproduced as-disclosed and labelled accordingly rather than treated as directly comparable. FY2014-FY2018 pre-date the interim MREL requirement referenced in the FY2019 disclosure.")


INTERIM_HEADERS = ["Period", "Disclosure type", "Metric", "Value", "Unit", "Basis", "Source document", "Page / table"]
INTERIM_METRICS = [
    ("CET1 capital", [1052, 816], "£m"),
    ("Tier 1 capital", [1052, 816], "£m"),
    ("Total capital", [1301, 1065], "£m"),
    ("Total risk-weighted exposure amount", [7563, 7702], "£m"),
    ("CET1 ratio", ["13.9%", "10.6%"], "%"),
    ("Tier 1 ratio", ["13.9%", "10.6%"], "%"),
    ("Total capital ratio", ["17.2%", "13.8%"], "%"),
    ("Total exposure measure excluding claims on central banks", [16909, 18809], "£m"),
    ("Leverage ratio excluding claims on central banks", ["6.2%", "4.3%"], "%"),
    ("Total HQLA, weighted value - average", [None, 6687], "£m"),
    ("Total net cash outflows, adjusted value", [None, 2374], "£m"),
    ("Liquidity coverage ratio", [None, "282%"], "%"),
    ("Total available stable funding", ["Not yet required", "Not disclosed"], "£m"),
    ("Total required stable funding", ["Not yet required", "Not disclosed"], "£m"),
    ("NSFR ratio", ["Not yet required", "Not disclosed"], "%"),
    ("MREL ratio", ["Not disclosed", "Not disclosed"], "%"),
]
interim_rows = []
for period, values, source, page in [
    ("30 Jun 2021", 0, P3_H1_2022, "3, UK KM1"),
    ("30 Jun 2022", 1, P3_H1_2022, "3, UK KM1"),
]:
    for metric_name, metric_values, unit in INTERIM_METRICS:
        interim_rows.append([period, "H1 Pillar 3 disclosure", metric_name, metric_values[values], unit, "Metro Bank PLC consolidated basis", source, page])
for period, source in [("30 Jun 2023", P3_H1_2023), ("30 Jun 2024", P3_H1_2024), ("30 Jun 2025", P3_H1_2025)]:
    interim_rows.append([period, "H1 Pillar 3 disclosure", "All Metro Bank PLC entity-level interim metrics", "Not separately disclosed", "n/a", "Metro Bank Holdings PLC group disclosure after 19 May 2023 restructure", source, "Basis note"])

bw.add_wide_interim_sheet(
    "Interim Pillar 3", rows=interim_rows,
    hyperlink_cells={(i, 6): row[6] for i, row in enumerate(interim_rows)},
    title="Metro Bank PLC - Interim Pillar 3 Disclosures",
    subtitle="Entity-level Metro Bank PLC basis where available; later Holdings Group disclosures are not substituted.",
    note="H1 2021 and H1 2022 use the official Metro Bank PLC consolidated UK KM1 table. From 19 May 2023 the ultimate holding company changed to Metro Bank Holdings PLC; H1 2023-H1 2025 official disclosures are Holdings Group figures and do not provide a defensible standalone Metro Bank PLC series, so those periods are explicitly recorded as not separately disclosed.",
)


def cash_value(label):
    return next(v for kind, name, v in cash_rows if name == label)


def bs_value(label):
    return next(v for kind, name, v in bs_rows if name == label)


def pl_value(label):
    return next(v for kind, name, v in pl_rows if name == label)


equity_summary = {
    "FY2014": {"Opening equity": 401, "Total comprehensive loss for the year": -38, "Other equity movements, net": 100, "Closing equity": 462},
    "FY2015": {"Opening equity": 462, "Total comprehensive loss for the year": -57, "Other equity movements, net": 2, "Closing equity": 407},
    "FY2016": {"Opening equity": 407, "Total comprehensive loss for the year": -8, "Other equity movements, net": 406, "Closing equity": 805},
    "FY2017": {"Opening equity": 805, "Total comprehensive income for the year": 10, "Other equity movements, net": 282, "Closing equity": 1096},
    "FY2018": {"Opening equity": 1096, "Total comprehensive income for the year": 23, "Other equity movements, net": 283, "Closing equity": 1403},
    "FY2019": {"Opening equity": 1403, "Total comprehensive loss for the year": -183, "Other equity movements, net": 363, "Closing equity": 1583},
    "FY2020": {"Opening equity": 1583, "Total comprehensive loss for the year": -296, "Other equity movements, net": 2, "Closing equity": 1289},
    "FY2021": {"Opening equity": 1294, "Total comprehensive loss for the year": -260, "Other equity movements, net": 2, "Closing equity": 1036},
    "FY2022": {"Opening equity": 1036, "Total comprehensive loss for the year": -81, "Other equity movements, net": 2, "Closing equity": 957},
    "FY2023": {"Opening equity": 957, "Total comprehensive income for the year": 48, "Other equity movements, net": 147, "Closing equity": 1152},
}

bw.add_overview_sheet(
    cash_flow_totals=[(label, cash_value(label)) for label in [
        "Net cash inflows/(outflows) from operating activities",
        "Net cash inflows/(outflows) from investing activities",
        "Net cash inflows/(outflows) from financing activities",
        "Cash and cash equivalents at end of year",
    ]],
    cash_flow_unit="£m",
    balance_sheet_totals=[(label, bs_value(label)) for label in [
        "Total assets",
        "Loans and advances to customers",
        "Deposits from customers",
        "Total equity",
    ]],
    balance_sheet_unit="£m",
    income_statement_totals=[(label, pl_value(label)) for label in [
        "Total income",
        "Total operating expenses",
        "Profit/(loss) before tax",
        "Profit/(loss) for the year",
    ]],
    income_statement_unit="£m",
    equity_changes_totals=[
        (label, {y: equity_summary[y].get(label) for y in equity_summary})
        for label in ["Opening equity", "Total comprehensive income for the year", "Total comprehensive loss for the year", "Other equity movements, net", "Closing equity"]
    ],
    equity_changes_unit="£m",
    ratios=[
        ("CET1 Ratio", vals({"FY2025": "12.5%", "FY2024": "12.5%", "FY2023": "13.1%", "FY2022": "10.3%", "FY2021": "12.6%",
            "FY2020": "15.0%", "FY2019": "15.6%", "FY2018": "13.1%", "FY2017": "15.25%", "FY2016": "18.16%", "FY2015": "13%", "FY2014": "28%"})),
        ("Total Capital Ratio", vals({"FY2025": "18.4%", "FY2024": "14.9%", "FY2023": "15.1%", "FY2022": "13.4%", "FY2021": "15.9%",
            "FY2020": "18.1%", "FY2019": "18.3%", "FY2018": "15.9%", "FY2017": "15.25%", "FY2016": "18.16%", "FY2015": "13%", "FY2014": "28%"})),
        ("Leverage Ratio", vals({"FY2025": "7.8%", "FY2024": "5.6%", "FY2023": "5.3%", "FY2022": "4.2%", "FY2021": "5.2%",
            "FY2020": "5.6%", "FY2019": "6.6%", "FY2018": "5.4%", "FY2017": "5.5%", "FY2016": "6.5%", "FY2015": "4.9%", "FY2014": "10%"})),
        ("LCR", vals({"FY2025": "314%", "FY2024": "444%", "FY2023": "244%", "FY2022": "246%", "FY2021": "281%",
            "FY2020": "187%", "FY2019": "197%", "FY2018": "139%", "FY2017": "141%", "FY2016": "136%"})),
        ("NSFR", vals({"FY2025": "165%", "FY2024": "160%", "FY2023": "136%", "FY2022": "143%"})),
    ],
    note="Metro Bank PLC entity basis. Balance Sheet/Equity Changes summaries are Company/standalone (FY2024-FY2025 "
         "blank - no standalone Metro Bank PLC accounts located); Profit & Loss summary is Group/consolidated "
         "(Metro Bank PLC does not publish its own income statement); cash-flow is Company/standalone with the same "
         "FY2024-FY2025 gap. Regulatory ratios change from Metro Bank PLC consolidated basis to Holdings Group basis "
         "after the 19 May 2023 restructure; see the metric and interim-sheet notes. Regulatory figures for "
         "FY2023-FY2025 were corrected 2026-09-03 (ST-026) - see the Total RWAs sheet's note. HD-049: FY2014-FY2020 "
         "added, capped at FY2014 (see ENTITY/BASIS NOTE on the Balance Sheet/Cash Flow/Equity sheets for the "
         "Group-vs-Company basis change at FY2020/FY2021). This Overview's 'Leverage Ratio' row uses the FY2014-"
         "FY2020 'regulatory leverage ratio including central bank claims' as originally disclosed for those years, "
         "and the FY2021-FY2025 'excluding central bank claims' measure for those years (the two are not the same "
         "definition - see the Leverage Ratio sheet's own two-row breakdown for both series in full).",
)

bw.save("/Users/armaan/code/katalysis/banks/METRO BANK FINANCIALS.xlsx")
