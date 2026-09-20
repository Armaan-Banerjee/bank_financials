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

# HD-074 pinned Pillar 3 (all 11 metric sheets), Asset Quality and RWA
# Breakdown to FY2014-FY2025, because no Pillar 3 disclosure older than FY2016
# had been located at that point and the statutory-statement extension to
# FY2010 was explicitly statements-only.
#
# 2026-09-15 (historical Pillar 3 recovery): that pin is now lifted to the full
# YEARS range. Four genuine Metro Bank PLC Pillar 3 editions - FY2010, FY2011,
# FY2013 and FY2014 - were recovered from the Wayback Machine and read cover to
# cover this session (see HIST_P3_NOTE). They are Basel II documents and their
# figures are NOT continuous with the CRR series, so they are carried on their
# own separate, explicitly-labelled rows rather than extending the existing
# ones. FY2012's edition was published (named on the Feb-2014 legal page) but never
# archived, so its cells read 'Unreached today' (corrected 2026-09-19; this said 'genuinely absent').
PILLAR3_YEARS = list(YEARS)

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
CH_FY2024 = "https://find-and-update.company-information.service.gov.uk/company/06419578/filing-history/MzQ2NzY4OTg1OGFkaXF6a2N4/document?format=pdf&download=0"
CH_FY2025 = "https://find-and-update.company-information.service.gov.uk/company/06419578/filing-history/MzUzODAzNTg0NWFkaXF6a2N4/document?format=pdf&download=0"

# 2026-09-15: historical Pillar 3 editions recovered from the Wayback Machine.
# Metro Bank's own live IR site hosts nothing older than the FY2016 edition, so
# these timestamped `id_` captures are the only located source for them.
#
# CITATION TRAP - DO NOT SHORTEN THESE: the FY2013 and FY2014 editions were
# published at the SAME original URL
# (metrobankonline.co.uk/Global/Legal Information/Pillar 3 Disclosure.pdf) and
# are distinguishable ONLY by Wayback capture timestamp. Citing the bare
# original URL would be ambiguous between two different documents. Each was
# opened and its cover date read before being mapped to a year: the
# 2014-09-15 capture's cover reads "31st December 2013" (20 pages) and the
# 2015-12-30 capture's reads "31st December 2014" (21 pages).
P3_2010_HIST = "https://web.archive.org/web/20120717023649id_/https://www.metrobankonline.co.uk/Global/NEW%20WEBSITE%20FILES/Pillar%203%20Disclosures%202010%2031%20December.pdf"
P3_2011_HIST = "https://web.archive.org/web/20130625053953id_/https://www.metrobankonline.co.uk/Global/Legal%20Information/Pillar%203%20Disclosure%20-%202011.pdf"
P3_2013_HIST = "https://web.archive.org/web/20140915151355id_/https://www.metrobankonline.co.uk/Global/Legal%20Information/Pillar%203%20Disclosure.pdf"
P3_2014_HIST = "https://web.archive.org/web/20151230210842id_/https://www.metrobankonline.co.uk/Global/Legal%20Information/Pillar%203%20Disclosure.pdf"

ENTITY_NOTE = (
    "ENTITY/BASIS NOTE: Metro Bank PLC (Companies House 06419578; FRN 488982; LEI "
    "213800X5WU57YL9GPK89) is the matched legal entity in Banks List 2608.xlsx. "
    "FY2021-FY2023 cash flows are the Company/standalone figures from Metro Bank PLC "
    "accounts. Metro Bank PLC used an individual consolidation method for prudential "
    "reporting in 2021-2022. On 19 May 2023 Metro Bank Holdings PLC became the ultimate "
    "holding company; FY2023-FY2025 Pillar 3 disclosures are subsequently for Holdings "
    "and its subsidiaries, not standalone Metro Bank PLC. "
    "\n\nREPORTING-ENTITY BOUNDARY, ESTABLISHED FROM THE DOCUMENTS THEMSELVES (2026-09-15). The change of "
    "reporting entity happens at exactly the FY2022/FY2023 Pillar 3 boundary - not earlier, not later - and the "
    "later documents ARE a holding-company consolidated basis, not Metro Bank PLC. Evidence, in document order: "
    "the FY2010, FY2011, FY2013 and FY2014 Pillar 3 covers all read 'METRO BANK PLC'; the FY2021 edition's "
    "executive summary describes itself as complementing \"Metro Bank PLC's (Metro Bank or the Bank) 2021 Annual "
    "Report and Accounts\"; every page header of the FY2022 edition reads 'Metro Bank PLC Pillar 3 2022'; the "
    "FY2023 edition's cover and every page header read 'Metro Bank Holdings PLC | Pillar 3 2023', its section 1 "
    "states \"In May 2023, Metro Bank completed the implementation of its holding company marking an important "
    "milestone in meeting the requirements of the Bank of England's resolution framework\", and its Table 3 (UK "
    "LI3) enumerates the regulatory consolidation group entity by entity - Metro Bank Holdings PLC (holding "
    "company), Metro Bank PLC (banking), RDM Factors Limited (dormant), SME Invoice Finance Limited (invoice "
    "financing) and SME Asset Finance Limited (asset financing), all under full consolidation. This is therefore "
    "a genuine basis change WITHIN this workbook's Pillar 3 series and is labelled on every affected sheet rather "
    "than being presented as one continuous entity. It is also why the FY2023 regulatory total assets of 22,245 "
    "differ from Metro Bank PLC's own AR2023 balance sheet total of 22,257. "
    "\n\nFY2024-FY2025 Metro Bank PLC Company/standalone balance sheets and cash flows are "
    "taken from the Bank's own statutory accounts filed at Companies House, rather than "
    "substituting Metro Bank Holdings PLC figures."
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
    f"FY2025 & FY2024: Metro Bank PLC Annual Report and Accounts 2025, Company cash flow statement, p.155 - {CH_FY2025}\n"
    f"FY2024: Metro Bank PLC Annual Report and Accounts 2024, Company cash flow statement, p.147 - {CH_FY2024}\n"
    f"FY2023 & FY2022: Metro Bank PLC Annual Report 2023, p.147 (Company cash flow statement) - {AR_2023}\n"
    f"FY2022 & FY2021: Metro Bank PLC Annual Report and Accounts 2022, p.185 (Company column) - {AR_2022}\n"
    f"FY2021: Metro Bank PLC Annual Report and Accounts 2021, p.165 (Company column) - {AR_2021}\n"
    f"FY2013: Metro Bank PLC Full Accounts, year ended 31 December 2013, Consolidated Cash flow statement, p.13 - {CH_FY2013}\n"
    f"FY2012: Metro Bank PLC Full Accounts, year ended 31 December 2012, Cash flow statement, p.11 - {CH_FY2012}\n"
    f"FY2011: Metro Bank PLC Full Accounts, year ended 31 December 2011, Cash flow statement, p.11 - {CH_FY2011}\n"
    f"FY2010 (16m): Metro Bank PLC Financial Statements, period ended 31 December 2010, Cash flow statement, p.10 - {CH_FY2010}\n\n"
    + ENTITY_NOTE
    + "\n\n" + HD074_EXTENSION_NOTE
    + "\n\nFY2024 SOURCE-QUALITY NOTE: the filed Company statement gives the exact net operating total (\u00a31,383m), "
    "but the accessible text rendition dropped the six FY2024 operating-reconciliation component values. Those "
    "cells remain blank; no consolidated figures were substituted. The FY2024 investing, financing and cash "
    "reconciliation figures are directly reported and populated."
)

HIST_P3_NOTE = (
    "HISTORICAL PILLAR 3 RECOVERY (2026-09-15) - FY2010, FY2011, FY2013, FY2014\n"
    f"FY2014: Metro Bank PLC Pillar 3 Disclosure, 31st December 2014 (21pp), section 4 Capital Resources (p.11) "
    f"and section 5.1 Credit Risk Exposures (p.13) - {P3_2014_HIST}\n"
    f"FY2013: Metro Bank PLC Pillar 3 Disclosure, 31st December 2013 (20pp), section 4 Capital Resources (p.13) "
    f"and section 5.1 Credit Risk Exposures (p.14-15) - {P3_2013_HIST}\n"
    f"FY2011: Metro Bank PLC Pillar 3 Disclosures, 31st December 2011 (18pp), section 4 Capital Resources (p.10) "
    f"and section 5.1 Credit Risk Exposures (p.12) - {P3_2011_HIST}\n"
    f"FY2010: Metro Bank PLC Pillar 3 Disclosures, 31st December 2010 (18pp), section 4 Capital Resources (p.10) "
    f"and section 5.1 Credit Risk Exposures (p.12) - {P3_2010_HIST}\n\n"
    "WHY THESE ARE ON SEPARATE ROWS - BASIS. All four editions are explicitly Basel II documents ('The Capital "
    "Requirements Directive (Basel II) came into force from January 1st 2007'), computed under the FSA's/PRA's "
    "GENPRU 2.2 definition of Tier 1 capital, using the Standardised Approach for credit risk and (from FY2011) "
    "the Basic Indicator Approach for operational risk. A full-text search of all four documents returns ZERO "
    "occurrences of 'CET1', 'Common Equity', 'Tier 2', 'leverage', 'LCR', 'NSFR' and 'MREL' - none of those "
    "concepts existed in Metro Bank's disclosure at the time. The CRR/CRD IV series that runs from FY2016 on the "
    "sheets above is therefore NOT continuous with these figures, and they are carried on their own separate rows "
    "rather than extending the existing ones.\n\n"
    "WHAT EACH EDITION ACTUALLY DISCLOSES, and nothing more: (a) a 'Tier 1 capital based on the [year] audited "
    "accounts' table whose bottom line is Total (Regulatory) Capital; (b) a credit-risk exposure table with an RWA "
    "column; (c) a single narrative sentence giving the doubtful-debt provision. NO capital ratio of any kind is "
    "stated in any of the four - the ratio cells for FY2010/FY2011/FY2013 are therefore 'Not publicly disclosed', "
    "and are deliberately NOT computed from the capital and RWA figures on these same sheets, which would be "
    "back-solving. Likewise NO total RWA is stated: operational risk RWA under the Basic Indicator Approach is "
    "never quantified, so the disclosed RWA figure is a credit-risk-only subtotal and is labelled as such.\n\n"
    "Transcribed figures (source tables are in GBP'000; these sheets are in GBP'm):\n"
    "FY2014 - Total Regulatory Capital 387,261 (narrative: 'capital base was made up of GBP 388m of Tier 1 "
    "capital'); components Share Capital 629,304, Profit and loss reserve (157,549), Other Reserves (4,314), "
    "Intangible Assets and Reserves (80,810). Credit risk table 'TOTAL' row: exposures 3,896,820, RWA 1,415,881.\n"
    "FY2013 - Total Regulatory Capital 381,530 (narrative: 'GBP 382m of Tier 1 capital'); components Share Capital "
    "531,011, Profit and loss reserve (118,608), Other Reserves (7,520), Intangible Assets and Reserves (23,353). "
    "Credit risk table 'TOTAL Risk Weighted Assets' row: exposures 2,076,992, RWA 775,310.\n"
    "FY2011 - Total Regulatory Capital 69,090 (narrative: 'GBP 69.090m of Tier 1 capital'); components Share "
    "Capital 120,131, Profit and loss reserve (42,179), Intangible Assets and Reserves (8,862). Credit risk table "
    "'TOTAL Risk Weighted Assets' row: RWA 93,152 (this table prints no exposure total).\n"
    "FY2010 - Total Capital 89,811 (narrative: 'GBP 89.8m of Tier 1 capital'); components Share capital 0, Share "
    "premium 120,131, Profit and loss reserve (23,341), Intangible Assets (6,979). Credit risk table 'Total "
    "assets' row: exposures 119,117, RWA 18,950.\n\n"
    "SOURCE-DOCUMENT DEFECTS, recorded rather than corrected:\n"
    "- The FY2014 capital table DOES NOT FOOT. 629,304 - 157,549 - 4,314 - 80,810 = 386,631, but the printed "
    "Total Regulatory Capital is 387,261 - a GBP 630k discrepancy inside the source document itself. The printed "
    "total (387,261) is what is transcribed, because it is what the document states and it is the figure the "
    "narrative rounds to ('GBP 388m'). The components are recorded above so the defect stays visible. It is NOT "
    "reconciled or 'fixed' here.\n"
    "- The FY2010 and FY2011 credit-risk tables are headed 'GBP m' but their values are plainly GBP'000 (FY2010's "
    "'Total assets 119,117' is the GBP 119.1m total assets on the Balance Sheet sheet of this workbook, to the "
    "pound). The FY2014 edition corrects the heading to 'GBP 000'. Treated as GBP'000 throughout.\n"
    "- The FY2011/FY2013/FY2014 capital tables label the GBP 120,131 / 531,011 / 629,304 line 'Share Capital', but "
    "the FY2010 edition splits the identical GBP 120,131 into 'Share capital 0' and 'Share premium 120,131'. The "
    "later label is a shorthand for share capital plus share premium, not a different figure.\n\n"
    "VALIDATION GATE against figures already in this workbook - divergences documented, nothing overwritten:\n"
    "- FY2010 ties exactly: 120,131 - 23,341 - 6,979 = 89,811, and share premium 120.1 / retained earnings (23.3) "
    "/ intangibles 7.0 are the Balance Sheet sheet's own FY2010 figures.\n"
    "- FY2011 Profit and loss reserve (42,179) vs this workbook's FY2011 retained earnings (42.3): GBP ~0.1m "
    "apart. FY2013 'Share Capital' 531,011 vs share premium 530.5: GBP ~0.5m apart. Both are small, both are "
    "left as each source reports them.\n"
    "- FY2014 is the material one, TWICE OVER. (1) CAPITAL: this workbook's FY2014 CET1/Tier 1/Total capital of "
    "384 comes from the FY2015 Annual Report's Capital management note, whereas the FY2014 Pillar 3 states 387,261 "
    "('GBP 388m') - GBP 3.3m apart, two different documents on two different bases (CRD IV-era annual report note "
    "vs contemporaneous Basel II Pillar 3). Per the project's validation-gate rule the pre-existing row is NOT "
    "overwritten; the Pillar 3 figure is carried alongside it on its own Basel II row. (2) RETAINED EARNINGS: the "
    "FY2014 Pillar 3's Profit and loss reserve of (157,549) is the CONTEMPORANEOUS figure, against this workbook's "
    "(164), which is the FY2015 Annual Report's 'restated' FY2014 comparative - GBP 6.5m apart. That independently "
    "corroborates the restatement flagged in the DATA QUALITY FLAG above (note 36 of the 2015 AR references "
    "undisclosed prior-period adjustments), and is the first contemporaneous FY2014 figure located for it.\n\n"
    "FY2012 - PUBLISHED BUT NOT ARCHIVED (corrected 2026-09-19; this previously read 'genuinely absent, closed'). "
    "The FY2012 edition existed: the bank's Legal Information page as archived on 2014-02-14 (Wayback "
    "20140214085420 of metrobankonline.co.uk/Footer/LegalInformation/) links 'Pillar 3 Disclosures' to "
    "/Global/Legal Information/Pillar 3 Disclosure update - December 2012.pdf, between the FY2011 file it "
    "replaced (still linked on the 2013-05-14, 2013-08-12 and 2013-11-14 captures) and the undated 'Pillar 3 "
    "Disclosure.pdf' that carried FY2013 by 2014-07-06. That file has no Wayback capture (CDX exact and prefix "
    "on the name), is 404 live, and archive.ph has none. The FY2013 edition (Wayback 20140915151355) prints no "
    "2012 comparative anywhere (0 occurrences of '2012' in its text layer), so it cannot fill the year. The "
    "FY2012 statutory accounts (Companies House scan, page images read 2026-09-19) print only the Directors' "
    "report KPI 'Capital as %age of risk weighted assets 55%' (PDF p.7, carried on the Total Capital Ratio "
    "sheet); note 25 'Capital management' refers back to that KPI table and gives no capital amount, RWA or "
    "provision on the Pillar 3 basis. The FY2012 cells that depend on the Pillar 3 therefore stay 'Unreached "
    "today' - a limit on our reach, not a statement that the bank published nothing. Note that the structurally "
    "inapplicable FY2012 metrics (CET1, leverage, LCR, NSFR, MREL) are marked 'Not applicable (Basel II)' like "
    "their neighbours - those would not have been disclosed in an FY2012 edition even if one were found.\n\n"
    "CDN/HOST SWEEP (GA-020 cdn-sweep, 2026-09-19), all negative, so FY2012 stays UNREACHED: (i) link and host "
    "extraction from the archived 2013-2014 Legal Information, homepage, About-us and Press-releases pages - "
    "every PDF was served same-origin from the EPiServer /Global/ tree; the only other hosts are the bank's own "
    "subdomains (personal., corporate., commercial., selfservice.) and metrobankmore.co.uk, no CDN or document "
    "host; (ii) Wayback CDX matchType=domain on metrobankonline.co.uk to 2017 without a mimetype filter (2,823 "
    "URL keys over 20 host variants): no FY2012 file, and the undated 'Pillar 3 Disclosure.pdf' digests are "
    "FY2013 (2014-09) and FY2014 (2015-12), never FY2012; (iii) the post-2015 EPiServer /globalassets/ tree, "
    "where the 2015/2016 editions were re-hosted (/globalassets/legal-information/pillar-3-disclosure-2015.pdf "
    "and -2016.pdf are live %PDF): CDX of all 7,632 URL keys has no pre-2015 Pillar 3, and slug guesses for "
    "the Dec-2012 update and the 2011 file 404; (iv) Common Crawl URL index, every crawl 2012-2016, for "
    "www.metrobankonline.co.uk/Global/*, metrobankonline.co.uk/Global/* and *.metrobankonline.co.uk: no "
    "capture of any /Global/ PDF; (v) web search for the title: 2019+ editions only; (vi) UK Web Archive CDX "
    "endpoint unavailable, Memento TimeTravel unreachable - neither is evidence.\n\n"
    "H1 interim editions for 2019-2021 were checked and are absent: 404 live with no Wayback capture."
)

P3_SOURCES = (
    "Sources - Metro Bank regulatory key metrics:\n"
    f"FY2020: Metro Bank PLC Pillar 3 Disclosure 2020, Table 6/KM1 and Table 8 EU OV1 - {P3_2020_HIST}\n"
    f"FY2019: Metro Bank PLC Pillar 3 2019 (31 December 2019), Table 1 RWA Summary and Table 2 Key Ratios (p.4), "
    f"Table 3 Capital Composition (p.25), Table 5 LRSum / Table 6 LRCom (p.28), Table 8 EU OV1 (p.30), Table 26 EU "
    f"LIQ1 (p.46) - {P3_2019_HIST}\n"
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
    "FY2019 VERIFICATION (2026-09-15): every FY2019 Pillar 3 cell in this workbook was re-checked line by line "
    "against the Pillar 3 2019 PDF itself and all reproduce exactly (CET1 and Tier 1 capital 1,427; CET1/Tier 1 "
    "ratio 15.6%; Total capital 1,676; Total capital ratio 18.3%; Total RWAs 9,147; leverage exposure 21,506 and "
    "ratio 6.6%; LCR HQLA 3,356 / net outflows 1,708 / ratio 197%; OV1 credit 8,591, CCR 5, market 5, operational "
    "546). The document's own FY2018 comparative column also reproduces every FY2018 figure already held here, so "
    "the validation gate passed with no conflicting basis to document. NSFR is not disclosed anywhere in the 2019 "
    "document (the UK NSFR disclosure requirement began 1 January 2023) and is left blank, not zeroed.\n\n"
    "RETRIEVAL METHOD NOTE (2026-09-15) - reusable, recorded because it generalises beyond Metro Bank: the FY2019 "
    "Pillar 3 disclosure EXISTS and is a genuine 54-page PDF, but it is MISSING from Metro Bank's own "
    "investor-relations document index. Nine candidate URLs built by permuting the neighbouring years' filename "
    "patterns all returned 404 - including paths under the same /globalassets/documents/investor_documents/ folder "
    "that demonstrably serves the 2017 and 2018 Pillar 3 files, and which in fact also serves the 2019 file under a "
    "name none of the permutations guessed. Only a search on the filename and bank name, independent of the bank's "
    "own site and index, located metro-bank-pillar-3-2019.pdf. RULE: a year missing from a bank's own document "
    "index is NOT closed until BOTH a direct fetch AND a name search have failed. Permutation can only fail to "
    "find; it can never prove absence.\n\n"
    "URL RE-CHECK (2026-09-15): all ten live metrobankonline.co.uk Pillar 3 URLs cited on this sheet (FY2016-"
    "FY2025) were re-fetched and every one returned HTTP 200 with a non-trivial PDF body. No cell on this sheet "
    "is left without a working source URL.\n\n"
    + HIST_P3_NOTE
    + "\n\n"
    + ENTITY_NOTE
)

bw = BankWorkbook(bank_name="Metro Bank PLC", years=YEARS, year_label=YEAR_LABEL, header_color="00695C")

STATEMENTS_SOURCES = (
    "Sources - Metro Bank PLC statements, £m:\n"
    f"FY2025 & FY2024 (Company/standalone balance sheet): Metro Bank PLC Annual Report and Accounts 2025, p.153 - {CH_FY2025}\n"
    f"FY2024 (Company/standalone statements): Metro Bank PLC Annual Report and Accounts 2024, p.145-147 - {CH_FY2024}\n"
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
    + "\n\nBASIS NOTE: Balance Sheet and Cash Flow Statement are shown on a Company/standalone Metro Bank PLC basis "
    "for FY2021-FY2025. The FY2024/FY2025 Bank company statements were located inside Metro Bank PLC's own 'Group of "
    "companies' statutory accounts filings at Companies House; that filing label does not mean the document lacks "
    "separate Company statements. Metro Bank Holdings PLC's shell-company balance sheet is not used. Profit & Loss is "
    "shown on a Group/consolidated basis for all 5 years, because "
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
    ("DATA", "Profit/(loss) before tax", {"FY2025": 94, "FY2023": 46, "FY2022": -71, "FY2021": -245,
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
    ("DATA", "Adjustments for non-cash items", {"FY2025": -401, "FY2023": -376, "FY2022": -259, "FY2021": -132}),
    ("DATA", "Interest received", {"FY2025": 748, "FY2023": 834, "FY2022": 538, "FY2021": 394}),
    ("DATA", "Interest paid", {"FY2025": -319, "FY2023": -370, "FY2022": -124, "FY2021": -126}),
    ("DATA", "Changes in loans and advances to customers", {"FY2020": 2591, "FY2019": -445}),
    ("DATA", "Changes in deposits from customers", {"FY2020": 1595, "FY2019": -1184}),
    ("DATA", "Changes in other operating assets", {"FY2025": 96, "FY2023": 729, "FY2022": -842, "FY2021": 2613,
        "FY2020": -2820, "FY2019": -26, "FY2018": -4651, "FY2017": -3755, "FY2016": -2341, "FY2015": -1971, "FY2014": -856,
        "FY2013": -591.9, "FY2012": -129.9, "FY2011": -44.6, "FY2010": -1.6}),
    ("DATA", "Changes in other operating liabilities", {"FY2025": -1323, "FY2023": -251, "FY2022": -409, "FY2021": 370,
        "FY2020": -64, "FY2019": -31, "FY2018": 4726, "FY2017": 5994, "FY2016": 3512, "FY2015": 2543, "FY2014": 1709,
        "FY2013": 893.6, "FY2012": 430.6, "FY2011": 140.0, "FY2010": 17.0}),
    ("TOTAL", "Net cash inflows/(outflows) from operating activities", {"FY2025": -1105, "FY2024": -1383, "FY2023": 612, "FY2022": -1167, "FY2021": 2874,
        "FY2020": 1041, "FY2019": -1655, "FY2018": 153, "FY2017": 2294, "FY2016": 1169, "FY2015": 546, "FY2014": 810,
        "FY2013": 249.3, "FY2012": 255.8, "FY2011": 63.7, "FY2010": -6.5}),
    ("SECTION", "Cash flows from investing activities", {}),
    ("DATA", "Sales of investment securities", {"FY2025": 1154, "FY2024": 1017, "FY2023": 1870, "FY2022": 857, "FY2021": 1269,
        "FY2020": 615, "FY2019": 2193, "FY2018": 1522, "FY2017": 309, "FY2016": 2197, "FY2015": 911, "FY2014": 474,
        "FY2013": 368.1}),
    ("DATA", "Purchase of investment securities", {"FY2025": -816, "FY2024": -630, "FY2023": -816, "FY2022": -1206, "FY2021": -3438,
        "FY2020": -1460, "FY2019": -618, "FY2018": -1740, "FY2017": -997, "FY2016": -3403, "FY2015": -1311, "FY2014": -1376,
        "FY2013": -638.5, "FY2012": -335.7, "FY2011": -38.7, "FY2010": -40.3}),
    ("DATA", "Purchase of property, plant and equipment", {"FY2025": -34, "FY2024": -41, "FY2023": -12, "FY2022": -29, "FY2021": -41,
        "FY2020": -29, "FY2019": -120, "FY2018": -150, "FY2017": -100, "FY2016": -98, "FY2015": -50, "FY2014": -41,
        "FY2013": -60.0, "FY2012": -26.8, "FY2011": -17.8, "FY2010": -15.3}),
    ("DATA", "Proceeds from sale of property, plant and equipment and intangible assets", {"FY2017": 0, "FY2016": 0}),
    ("DATA", "Purchase and development of intangible assets", {"FY2025": -48, "FY2024": -19, "FY2023": -26, "FY2022": -24, "FY2021": -64,
        "FY2020": -81, "FY2019": -79, "FY2018": -75, "FY2017": -70, "FY2016": -45, "FY2015": -30, "FY2014": -13,
        "FY2013": -14.2, "FY2012": -2.9, "FY2011": -2.7, "FY2010": -6.4}),
    ("DATA", "Acquisition of subsidiary, net of cash acquired", {"FY2020": -1}),
    ("DATA", "Dividends received from subsidiaries", {"FY2023": 12}),
    ("TOTAL", "Net cash inflows/(outflows) from investing activities", {"FY2025": 256, "FY2024": 327, "FY2023": 1028, "FY2022": -402, "FY2021": -2274,
        "FY2020": -956, "FY2019": 1376, "FY2018": -443, "FY2017": -858, "FY2016": -1349, "FY2015": -480, "FY2014": -957,
        "FY2013": -344.6, "FY2012": -365.3, "FY2011": -59.1, "FY2010": -62.0}),
    ("SECTION", "Cash flows from financing activities", {}),
    ("DATA", "Repayment of preference shares", {"FY2010": -0.1}),
    ("DATA", "Repayment of capital elements of leases", {"FY2025": -19, "FY2024": -22, "FY2023": -23, "FY2022": -25, "FY2021": -27,
        "FY2020": -31, "FY2019": -25}),
    ("DATA", "Issuance of new shares", {"FY2023": 144,
        "FY2019": 375, "FY2018": 304, "FY2017": 279, "FY2016": 404, "FY2014": 99,
        "FY2013": 284.3, "FY2012": 126.0, "FY2010": 120.1}),
    ("DATA", "Cost of share/debt issues", {
        "FY2019": -16, "FY2018": -3, "FY2017": -3, "FY2016": -5, "FY2014": -1}),
    ("DATA", "Issuance of shares and other equity instruments", {"FY2025": 250, "FY2024": "-"}),
    ("DATA", "Distributions on other equity instruments", {"FY2025": -17, "FY2024": "-"}),
    ("DATA", "Issuance of medium-term notes/subordinated debt (net of costs)", {"FY2023": 175, "FY2019": 350, "FY2018": 250}),
    ("DATA", "Cost of debt issued", {"FY2019": -8, "FY2018": -1}),
    ("DATA", "Grant (repaid)/received", {"FY2020": -50, "FY2019": 120}),
    ("TOTAL", "Net cash inflows/(outflows) from financing activities", {"FY2025": 214, "FY2024": -22, "FY2023": 296, "FY2022": -25, "FY2021": -27,
        "FY2020": -81, "FY2019": 796, "FY2018": 550, "FY2017": 276, "FY2016": 398, "FY2015": 0, "FY2014": 99,
        "FY2013": 284.3, "FY2012": 126.0, "FY2011": 0, "FY2010": 120.1}),
    ("TOTAL", "Net increase/(decrease) in cash and cash equivalents", {"FY2025": -635, "FY2024": -1078, "FY2023": 1936, "FY2022": -1594, "FY2021": 573,
        "FY2020": 4, "FY2019": 517, "FY2018": 260, "FY2017": 1712, "FY2016": 218, "FY2015": 66, "FY2014": -47,
        "FY2013": 189.1, "FY2012": 16.5, "FY2011": 4.7, "FY2010": 51.6}),
    ("DATA", "Cash and cash equivalents at start of year", {"FY2025": 2811, "FY2024": 3889, "FY2023": 1953, "FY2022": 3547, "FY2021": 2974,
        "FY2020": 2989, "FY2019": 2472, "FY2018": 2212, "FY2017": 500, "FY2016": 282, "FY2015": 216, "FY2014": 263,
        "FY2013": 74.1, "FY2012": 57.6, "FY2011": 52.9, "FY2010": 1.3}),
    ("TOTAL", "Cash and cash equivalents at end of year", {"FY2025": 2176, "FY2024": 2811, "FY2023": 3889, "FY2022": 1953, "FY2021": 3547,
        "FY2020": 2993, "FY2019": 2989, "FY2018": 2472, "FY2017": 2212, "FY2016": 500, "FY2015": 282, "FY2014": 216,
        "FY2013": 263.2, "FY2012": 74.1, "FY2011": 57.6, "FY2010": 52.9}),
]

bs_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and balances with the Bank of England", {"FY2025": 2176, "FY2024": 2811, "FY2023": 3889, "FY2022": 1953, "FY2021": 3547,
        "FY2020": 2993, "FY2019": 2989, "FY2018": 2286, "FY2017": 2112, "FY2016": 435, "FY2015": 218, "FY2014": 181,
        "FY2013": 239.0, "FY2012": 46.7, "FY2011": 35.3, "FY2010": 48.4}),
    ("DATA", "Loans and advances to banks", {"FY2018": 186, "FY2017": 100, "FY2016": 66, "FY2015": 64, "FY2014": 35,
        "FY2013": 24.2, "FY2012": 27.4, "FY2011": 22.2, "FY2010": 4.5}),
    ("DATA", "Loans and advances to customers", {"FY2025": 8040, "FY2024": 8472, "FY2023": 11844, "FY2022": 12698, "FY2021": 11976,
        "FY2020": 12090, "FY2019": 14681, "FY2018": 14235, "FY2017": 9620, "FY2016": 5865, "FY2015": 3543, "FY2014": 1590,
        "FY2013": 751.1, "FY2012": 167.8, "FY2011": 42.1, "FY2010": 0.1}),
    ("DATA", "Investment securities held at FVOCI", {"FY2025": 218, "FY2024": 377, "FY2023": 476, "FY2022": 571, "FY2021": 798,
        "FY2020": 773, "FY2019": 411, "FY2018": 674}),
    ("DATA", "Investment securities held at amortised cost", {"FY2025": 3942, "FY2024": 4113, "FY2023": 4403, "FY2022": 5343, "FY2021": 4776,
        "FY2020": 2640, "FY2019": 2154, "FY2018": 3458}),
    ("DATA", "Available-for-sale investment securities (pre-IFRS 9)", {"FY2017": 361, "FY2016": 604, "FY2015": 364, "FY2014": 1304}),
    ("DATA", "Held-to-maturity investment securities (pre-IFRS 9)", {"FY2017": 3554, "FY2016": 2623, "FY2015": 1636, "FY2014": 307,
        "FY2010": 40.3}),
    ("DATA", "Investment securities (undifferentiated basis, HD-074: FY2011-FY2013 note-level AFS/HTM split not sourced this session)", {
        "FY2013": 696.4, "FY2012": 431.2, "FY2011": 81.3}),
    ("DATA", "Financial assets held at fair value through profit and loss", {"FY2022": 1, "FY2021": 3, "FY2020": 30}),
    ("DATA", "Derivative financial assets", {"FY2025": 23, "FY2024": 16, "FY2023": 36, "FY2022": 23}),
    ("DATA", "Property, plant and equipment", {"FY2025": 705, "FY2024": 711, "FY2023": 723, "FY2022": 748, "FY2021": 765,
        "FY2020": 806, "FY2019": 856, "FY2018": 454, "FY2017": 328, "FY2016": 247, "FY2015": 165, "FY2014": 132,
        "FY2013": 104.5, "FY2012": 53.6, "FY2011": 32.3, "FY2010": 17.3}),
    ("DATA", "Investment in subsidiaries", {"FY2025": 15, "FY2024": 15, "FY2023": 15, "FY2022": 31, "FY2021": 31}),
    ("DATA", "Intangible assets", {"FY2025": 138, "FY2024": 121, "FY2023": 188, "FY2022": 204, "FY2021": 231,
        "FY2020": 254, "FY2019": 168, "FY2018": 197, "FY2017": 148, "FY2016": 93, "FY2015": 54, "FY2014": 35,
        "FY2013": 23.8, "FY2012": 10.9, "FY2011": 8.8, "FY2010": 7.0}),
    ("DATA", "Deferred tax asset", {"FY2025": 225, "FY2024": 237, "FY2018": 41, "FY2017": 54, "FY2016": 56, "FY2015": 53, "FY2014": 44,
        "FY2013": 35.8, "FY2012": 25.3, "FY2011": 14.1}),
    ("DATA", "Prepayments and accrued income", {"FY2025": 70, "FY2024": 84, "FY2023": 111, "FY2022": 80, "FY2021": 64,
        "FY2020": 77, "FY2019": 66, "FY2018": 66, "FY2017": 53, "FY2016": 43, "FY2015": 30, "FY2014": 19,
        "FY2013": 5.0, "FY2012": 1.9, "FY2011": 0.8, "FY2010": 0.4}),
    ("DATA", "Assets classified as held for sale", {"FY2022": 1, "FY2020": 295}),
    ("DATA", "Other assets", {"FY2025": 949, "FY2024": 640, "FY2023": 572, "FY2022": 473, "FY2021": 392,
        "FY2020": 2621, "FY2019": 75, "FY2018": 50, "FY2017": 26, "FY2016": 26, "FY2015": 21, "FY2014": 14,
        "FY2013": 11.8, "FY2012": 6.4, "FY2011": 3.3, "FY2010": 1.0}),
    ("TOTAL", "Total assets", {"FY2025": 16501, "FY2024": 17597, "FY2023": 22257, "FY2022": 22126, "FY2021": 22583,
        "FY2020": 22579, "FY2019": 21400, "FY2018": 21647, "FY2017": 16355, "FY2016": 10057, "FY2015": 6148, "FY2014": 3661,
        "FY2013": 1891.6, "FY2012": 771.2, "FY2011": 240.3, "FY2010": 119.1}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Deposits from customers", {"FY2025": 13445, "FY2024": 14458, "FY2023": 15623, "FY2022": 16014, "FY2021": 16448,
        "FY2020": 16072, "FY2019": 14477, "FY2018": 15661, "FY2017": 11669, "FY2016": 7951, "FY2015": 5108, "FY2014": 2867,
        "FY2013": 1315.4, "FY2012": 576.3, "FY2011": 151.6, "FY2010": 17.9}),
    ("DATA", "Deposits from central banks", {"FY2025": 400, "FY2024": 400, "FY2023": 3050, "FY2022": 3800, "FY2021": 3800,
        "FY2020": 3808, "FY2019": 3801, "FY2018": 3801, "FY2017": 3321, "FY2016": 543}),
    ("DATA", "Debt securities", {"FY2025": 688, "FY2024": 679, "FY2023": 699, "FY2022": 571, "FY2021": 588,
        "FY2020": 600, "FY2019": 591, "FY2018": 249}),
    ("DATA", "Financial liabilities held at fair value through profit and loss", {"FY2020": 30}),
    ("DATA", "Repurchase agreements", {"FY2025": 73, "FY2024": 391, "FY2023": 1191, "FY2022": 238, "FY2021": 169,
        "FY2020": 196, "FY2019": 250, "FY2018": 344, "FY2017": 122, "FY2016": 653, "FY2015": 562, "FY2014": 283}),
    ("DATA", "Derivative financial liabilities", {"FY2025": 0, "FY2024": 1, "FY2022": 26, "FY2021": 10, "FY2020": 8, "FY2019": 8}),
    ("DATA", "Lease liabilities", {"FY2025": 185, "FY2024": 205, "FY2023": 234, "FY2022": 248, "FY2021": 269, "FY2020": 327, "FY2019": 341}),
    ("DATA", "Deferred grants", {"FY2025": 10, "FY2024": 13, "FY2023": 16, "FY2022": 17, "FY2021": 19, "FY2020": 28, "FY2019": 50}),
    ("DATA", "Provisions", {"FY2025": 6, "FY2024": 11, "FY2023": 23, "FY2022": 7, "FY2021": 15, "FY2020": 11, "FY2019": 17}),
    ("DATA", "Deferred tax liability", {"FY2023": 13, "FY2022": 12, "FY2021": 12, "FY2020": 12, "FY2019": 15}),
    ("DATA", "Other liabilities", {"FY2025": 181, "FY2024": 237, "FY2023": 256, "FY2022": 236, "FY2021": 217,
        "FY2020": 198, "FY2019": 267, "FY2018": 189, "FY2017": 148, "FY2016": 106, "FY2015": 71, "FY2014": 49,
        "FY2013": 171.2, "FY2012": 16.7, "FY2011": 10.7, "FY2010": 4.5}),
    ("TOTAL", "Total liabilities", {"FY2025": 14988, "FY2024": 16395, "FY2023": 21105, "FY2022": 21169, "FY2021": 21547,
        "FY2020": 21290, "FY2019": 19817, "FY2018": 20244, "FY2017": 15259, "FY2016": 9253, "FY2015": 5741, "FY2014": 3198,
        "FY2013": 1486.6, "FY2012": 593.0, "FY2011": 162.3, "FY2010": 22.3}),
    ("SECTION", "Equity", {}),
    ("DATA", "Called-up share capital", {"FY2025": 0, "FY2024": 0}),
    ("DATA", "Share premium", {"FY2025": 144, "FY2024": 144, "FY2023": 144, "FY2022": 1964, "FY2021": 1964,
        "FY2020": 1964, "FY2019": 1964, "FY2018": 1605, "FY2017": 1304, "FY2016": 1028, "FY2015": 629, "FY2014": 629,
        "FY2013": 530.5, "FY2012": 246.2, "FY2011": 120.1, "FY2010": 120.1}),
    ("DATA", "Retained earnings/(losses)", {"FY2025": 1096, "FY2024": 1040, "FY2023": 996, "FY2022": -1014, "FY2021": -941,
        "FY2020": -694, "FY2019": -392, "FY2018": -209, "FY2017": -219, "FY2016": -230, "FY2015": -213, "FY2014": -164,
        "FY2013": -118.7, "FY2012": -76.9, "FY2011": -42.3, "FY2010": -23.3}),
    ("DATA", "Other equity instruments", {"FY2025": 250, "FY2024": "-"}),
    ("DATA", "Other reserves", {"FY2025": 23, "FY2024": 18, "FY2023": 12, "FY2022": 7, "FY2021": 13,
        "FY2020": 19, "FY2019": 11, "FY2018": 7, "FY2017": 12, "FY2016": 7, "FY2015": -9, "FY2014": -3,
        "FY2013": -6.8, "FY2012": 8.9, "FY2011": 0.2}),
    ("TOTAL", "Total equity", {"FY2025": 1513, "FY2024": 1202, "FY2023": 1152, "FY2022": 957, "FY2021": 1036,
        "FY2020": 1289, "FY2019": 1583, "FY2018": 1403, "FY2017": 1096, "FY2016": 805, "FY2015": 407, "FY2014": 462,
        "FY2013": 405.0, "FY2012": 178.2, "FY2011": 78.0, "FY2010": 96.8}),
    ("TOTAL", "Total equity and liabilities", {"FY2025": 16501, "FY2024": 17597, "FY2023": 22257, "FY2022": 22126, "FY2021": 22583,
        "FY2020": 22579, "FY2019": 21400, "FY2018": 21647, "FY2017": 16355, "FY2016": 10057, "FY2015": 6148, "FY2014": 3661,
        "FY2013": 1891.6, "FY2012": 771.2, "FY2011": 240.3, "FY2010": 119.1}),
]

bw.add_balance_sheet_sheet(
    title="Metro Bank PLC - Balance Sheet",
    subtitle="Company/standalone basis, £m; 31 December year-end (FY2013-FY2020 shown on a Group/consolidated "
              "basis instead - see HD-049/HD-074 notes). FY2010 is a 16-month first accounting period. "
              "FY2024-FY2025 are from Metro Bank PLC's filed Company statements. 'Other equity instruments' is "
              "a row Metro Bank PLC first printed in its FY2025 Company balance sheet (£250m of AT1 securities, "
              "FY2024 nil); it is reproduced here in the bank's own position, between Retained earnings and Other "
              "reserves. Note that Metro Bank Holdings PLC's consolidated balance sheet carries the same "
              "instrument at £242m, net of issuance costs borne at the holding-company level - the two figures "
              "are different entities' presentations, not a discrepancy.",
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
                   "Share option reserve", "Deemed capital contribution", "Other equity instruments",
                   "Total equity"]
equity_rows = [
    ("TOTAL", "Balance at 19 September 2009 (opening, Company basis - conversion to PLC)", (0.1, 0, 0.0, None, None, None, None, 0.1)),
    ("DATA", "Net loss for the period (16 months to 31 December 2010)", (None, None, -23.4, None, None, None, None, -23.4)),
    ("DATA", "Issue of new ordinary shares", (None, 120.1, None, None, None, None, None, 120.1)),
    ("DATA", "Repayment of preference shares", (-0.1, None, None, None, None, None, None, -0.1)),
    ("TOTAL", "Balance as at 31 December 2010 (FY2010 closing, 16-month first accounts, Company basis)", (0, 120.1, -23.3, None, None, None, None, 96.8)),
    ("DATA", "Net loss for the year", (None, None, -19.0, None, None, None, None, -19.0)),
    ("DATA", "Other comprehensive income relating to available-for-sale investments, net of tax", (None, None, None, 0.1, None, None, None, 0.1)),
    ("DATA", "Share options at fair value", (None, None, None, None, 0.1, None, None, 0.1)),
    ("TOTAL", "Balance as at 31 December 2011 (FY2011 closing, Company basis)", (0, 120.1, -42.3, 0.1, 0.1, None, None, 78.0)),
    ("DATA", "Share issue", (None, 126.0, None, None, None, None, None, 126.0)),
    ("DATA", "Net loss for the year", (None, None, -34.6, None, None, None, None, -34.6)),
    ("DATA", "Other comprehensive income relating to available-for-sale investments, net of tax", (None, None, None, 8.5, None, None, None, 8.5)),
    ("DATA", "Share options at fair value", (None, None, None, None, 0.3, None, None, 0.3)),
    ("TOTAL", "Balance as at 31 December 2012 (FY2012 closing, Company basis)", (0, 246.2, -76.9, 8.6, 0.4, None, None, 178.2)),
    ("DATA", "Share issue", (None, 284.3, None, None, None, None, None, 284.3)),
    ("DATA", "Net loss for the year", (None, None, -41.8, None, None, None, None, -41.8)),
    ("DATA", "Other comprehensive expense relating to available-for-sale investments, net of tax", (None, None, None, -16.1, None, None, None, -16.1)),
    ("DATA", "Share options at fair value", (None, None, None, None, 0.4, None, None, 0.4)),
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
    ("TOTAL", "Balance as at 31 December 2013 (FY2013 closing, own contemporaneous figures, Group basis)", (0, 530.5, -118.7, -7.5, 0.8, None, None, 405.0)),
    ("TOTAL", "At 1 January 2014 (FY2014 opening, restated, Group basis)", (0, 530, -123, -8, 1, None, None, 401)),
    ("DATA", "Loss for the year", (None, None, -41, None, None, None, None, -41)),
    ("DATA", "Other comprehensive income relating to available-for-sale investments, net of tax", (None, None, None, 3, None, None, None, 3)),
    ("DATA", "Share issue", (None, 99, None, None, None, None, None, 99)),
    ("DATA", "Share options at fair value", (None, None, None, None, 1, None, None, 1)),
    ("TOTAL", "At 31 December 2014 (FY2014 closing, restated)", (0, 629, -164, -4, 2, None, None, 462)),
    ("DATA", "Loss for the year", (None, None, -49, None, None, None, None, -49)),
    ("DATA", "Other comprehensive expense relating to available-for-sale investments, net of tax", (None, None, None, -8, None, None, None, -8)),
    ("DATA", "Share options at fair value", (None, None, None, None, 2, None, None, 2)),
    ("TOTAL", "At 31 December 2015 (FY2015 closing)", (0, 629, -213, -12, 3, None, None, 407)),
    ("DATA", "Loss for the year", (None, None, -17, None, None, None, None, -17)),
    ("DATA", "Other comprehensive income relating to available-for-sale investments, net of tax", (None, None, None, 9, None, None, None, 9)),
    ("DATA", "Share issue", (None, 404, None, None, None, None, None, 404)),
    ("DATA", "Cost of share issue", (None, -5, None, None, None, None, None, -5)),
    ("DATA", "Share options at fair value", (None, None, None, None, 7, None, None, 7)),
    ("TOTAL", "At 31 December 2016 (FY2016 closing)", (0, 1028, -230, -3, 11, None, None, 805)),
    ("DATA", "Profit for the year", (None, None, 11, None, None, None, None, 11)),
    ("DATA", "Other comprehensive expense relating to available-for-sale investments, net of tax", (None, None, None, -1, None, None, None, -1)),
    ("DATA", "Share issue", (None, 279, None, None, None, None, None, 279)),
    ("DATA", "Cost of share issue", (None, -3, None, None, None, None, None, -3)),
    ("DATA", "Net share option movements", (None, None, None, None, 6, None, None, 6)),
    ("TOTAL", "At 31 December 2017 (FY2017 closing)", (0, 1304, -219, -4, 16, None, None, 1096)),
    ("DATA", "IFRS 9 transition adjustment, net of tax (AFS reserve replaced by FVOCI reserve)", (None, None, -17, 5, None, None, None, -12)),
    ("DATA", "Profit for the year", (None, None, 27, None, None, None, None, 27)),
    ("DATA", "Other comprehensive expense relating to investment securities designated at FVOCI, net of tax", (None, None, None, -4, None, None, None, -4)),
    ("DATA", "Shares issued", (None, 304, None, None, None, None, None, 304)),
    ("DATA", "Cost of shares issued", (None, -3, None, None, None, None, None, -3)),
    ("DATA", "Net share option movements", (None, None, None, None, -6, None, None, -6)),
    ("TOTAL", "At 31 December 2018 (FY2018 closing)", (0, 1605, -209, -3, 10, None, None, 1403)),
    ("DATA", "Loss for the year", (None, None, -183, None, None, None, None, -183)),
    ("DATA", "Shares issued", (None, 375, None, None, None, None, None, 375)),
    ("DATA", "Cost of shares issued", (None, -16, None, None, None, None, None, -16)),
    ("DATA", "Net share option movements", (None, None, None, None, 4, None, None, 4)),
    ("TOTAL", "At 31 December 2019 (FY2019 closing)", (0, 1964, -392, -3, 14, None, None, 1583)),
    ("DATA", "Loss for the year", (None, None, -302, None, None, None, None, -302)),
    ("DATA", "Other comprehensive income relating to investment securities designated at FVOCI, net of tax", (None, None, None, 6, None, None, None, 6)),
    ("DATA", "Net share option movements", (None, None, None, None, 2, None, None, 2)),
    ("TOTAL", "At 31 December 2020 (FY2020 closing, Group basis)", (0, 1964, -694, 3, 16, None, None, 1289)),
    ("TOTAL", "At 1 January 2021 (FY2021 opening)", (0, 1964, -689, 3, 16, None, None, 1294)),
    ("DATA", "Loss for the year", (None, None, -252, None, None, None, None, -252)),
    ("DATA", "Other comprehensive expense relating to investment securities designated at FVOCI, net of tax", (None, None, None, -8, None, None, None, -8)),
    ("DATA", "Net share option movements", (None, None, None, None, 2, None, None, 2)),
    ("TOTAL", "At 31 December 2021 (FY2021 closing)", (0, 1964, -941, -5, 18, None, None, 1036)),
    ("DATA", "Loss for the year", (None, None, -73, None, None, None, None, -73)),
    ("DATA", "Other comprehensive expense relating to investment securities designated at FVOCI, net of tax", (None, None, None, -8, None, None, None, -8)),
    ("DATA", "Net share option movements", (None, None, None, None, 2, None, None, 2)),
    ("TOTAL", "At 31 December 2022 (FY2022 closing)", (0, 1964, -1014, -13, 20, None, None, 957)),
    ("DATA", "Profit for the year", (None, None, 46, None, None, None, None, 46)),
    ("DATA", "Other comprehensive income relating to investment securities designated at FVOCI, net of tax", (None, None, None, 2, None, None, None, 2)),
    ("DATA", "Net share option movements", (None, None, None, None, 3, None, None, 3)),
    ("DATA", "Transfer of share option reserve upon insertion of new holding company", (None, None, None, None, -23, 23, None, 0)),
    ("DATA", "Cancellation of Metro Bank PLC share capital and share premium", (None, -1964, 1964, None, None, None, None, 0)),
    ("DATA", "Shares issued", (None, 144, None, None, None, None, None, 144)),
    ("TOTAL", "At 31 December 2023 (FY2023 closing)", (0, 144, 996, -11, 0, 23, None, 1152)),
    ("DATA", "Profit for the year", (None, None, 44, None, None, None, None, 44)),
    ("DATA", "Other comprehensive income relating to investment securities designated at FVOCI, net of tax", (None, None, None, 4, None, None, None, 4)),
    ("DATA", "Equity-settled share-based payment charges", (None, None, None, None, None, 2, None, 2)),
    ("TOTAL", "At 31 December 2024 (FY2024 closing)", (0, 144, 1040, -7, 0, 25, None, 1202)),
    ("DATA", "Profit for the year", (None, None, 55, None, None, None, 17, 72)),
    ("DATA", "Other comprehensive income relating to investment securities designated at FVOCI, net of tax", (None, None, None, 4, None, None, None, 4)),
    ("DATA", "Issuance of other equity instruments", (None, None, None, None, None, None, 250, 250)),
    ("DATA", "Equity-settled share-based payment charges", (None, None, None, None, None, 3, None, 3)),
    ("DATA", "Distributions on other equity instruments", (None, None, None, None, None, None, -17, -17)),
    ("DATA", "Other movements in share option charges", (None, None, 1, None, None, -2, None, -1)),
    ("TOTAL", "At 31 December 2025 (FY2025 closing)", (0, 144, 1096, -3, 0, 26, 250, 1513)),
]

bw.add_equity_changes_sheet(
    title="Metro Bank PLC - Statement of Changes in Equity",
    subtitle="Chronological roll-forward, oldest to newest, £m. FY2010-FY2013 are Company basis (HD-074; FY2010 "
              "is a 16-month first accounting period); FY2013's closing is nonetheless Group/consolidated, Metro "
              "Bank's first subsidiary having been acquired that July - see HD-074 note. FY2014-FY2020 are "
              "Group/consolidated basis; FY2021-FY2025 are Company/standalone basis (see HD-049 basis note). "
              "FY2024 and FY2025 were added 2026-09-18 (GA-006) from Metro Bank PLC's own FY2025 Company "
              "statement of changes in equity, which is also the source of the new 'Other equity instruments' "
              "column - a component the bank first reported in FY2025 and which is blank, not zero, for every "
              "earlier year because it did not exist. Equity "
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
    sources_text=STATEMENTS_SOURCES + "\n\n" + HD074_EXTENSION_NOTE + (
        "\n\nFY2024/FY2025 SOURCE-QUALITY NOTE: Metro Bank PLC's FY2025 Companies House filing (06419578) is a "
        "scanned image PDF with no text layer, so its Company statement of changes in equity (printed p.154) was "
        "read from rendered page images. Two cells were read inconsistently across two independent renderings - "
        "FY2025 profit for the year attributable to ordinary shareholders, and the retained-earnings element of "
        "total comprehensive income. Both were settled against figures that do not depend on that page at all: "
        "retained earnings of 1,040 opening + 55 + 1 = 1,096 closing, the closing figure being independently "
        "printed on the Company balance sheet (p.153), and 55 + 17 attributable to other equity holders = the "
        "72 total. Every other column ties the same way (deemed capital contribution 25 + 3 - 2 = 26; FVOCI (7) "
        "+ 4 = (3); other equity instruments 17 + 250 - 17 = 250), so the block is arithmetically closed on its "
        "own closing balances rather than on the image read alone."
    ),
    first_col_width=46,
)

bw.add_cash_flow_sheet(
    title="Metro Bank PLC - Cash Flow Statement",
    subtitle="£m; 31 December year-end. FY2010-FY2012 are Company (own, pre-subsidiary); FY2013 is Group "
              "(HD-074); FY2014-FY2020 are Group/consolidated (as reported, itemized adjustments); "
              "FY2021-FY2023 are Company/standalone (as reported, collapsed to 'Adjustments for non-cash items' "
              "plus memo interest received/paid) - see HD-049 basis note. FY2024-FY2025 are Company/standalone "
              "figures from Metro Bank PLC's statutory accounts.",
    rows=cash_rows, sources_text=CASH_SOURCES + (
        "\n\nHD-049: FY2014-FY2020 reproduce each year's own Consolidated Cash Flow Statement line items "
        "(impairment/write-offs, D&A, share option charge, gain on sale, accrued interest, lease interest, grant "
        "income, amounts provided for) rather than collapsing them into 'Adjustments for non-cash items' as the "
        "Company statement does for FY2021-FY2023 - both presentations are as-reported, not reclassified by this "
        "workbook.\n\nHD-074: FY2010-FY2013 similarly reproduce each year's own reported line items - see the "
        "HD-074 note above for the net-vs-gross investment-securities purchase distinction across these years."
        "\n\nFY2025 FINANCING ROWS: the FY2025 Company cash flow statement prints two rows no earlier edition "
        "carries - 'Issuance of shares and other equity instruments' (£250m) and 'Distributions on other equity "
        "instruments' (£17m outflow) - and both are reproduced here under the bank's own FY2025 captions rather "
        "than folded into the 'Issuance of new shares' row that earlier editions use for share issuances. "
        "FY2025's £250m is entirely the AT1 issuance: the Company statement of changes in equity shows nil "
        "issuance of shares under existing employee schemes that year. With these rows present the section foots "
        "as published: -19 + 250 - 17 = 214."
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
    # FY2019/FY2018: Pillar 3 2019, narrative under Table 16 (p.39) - "At the end of
    # 2019 we held an ECL provision of GBP 34 million (31 December 2018: GBP 34
    # million)" - corroborated by Table 18's 31 December total row (p.41).
    ("TOTAL", "Total ECL allowance", {"FY2025": -170, "FY2024": -191, "FY2023": -199, "FY2022": -187, "FY2021": -169,
        "FY2019": -34, "FY2018": -34}),
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
    # FY2016/FY2015 recovered 2026-09-18 (interior-gap pass). These two years were
    # an interior hole - FY2017's NPL ratio above them, the Basel II block below.
    # They are IAS 39 INCURRED-loss figures, so they get their own section and must
    # never be read as a continuation of the IFRS 9 ECL rows above; equally they are
    # NOT the same measure as the Basel II Pillar 3 general doubtful-debt provision
    # in the block below, which is a regulatory rather than an accounting number.
    # Group basis throughout, matching the rest of this sheet. Source: Metro Bank PLC
    # Annual Report and Accounts 2016, Note 10 "Loans and advances to customers and
    # banks", printed pp.91-92, which prints Group 2016 and Group 2015 side by side.
    ("SECTION", "IAS 39 incurred-loss loan book and impairment allowance (FY2016-FY2015) - separate basis, NOT comparable with the IFRS 9 ECL rows above and NOT the same measure as the Basel II Pillar 3 provision rows below. Group basis, from Note 10 of the Annual Report and Accounts 2016 (printed pp.91-92), which prints Group 2016 and Group 2015 side by side", {}),
    ("DATA", "Gross loans and advances to customers (IAS 39)", {"FY2016": 5872.9, "FY2015": 3549.3}),
    ("DATA", "Allowance for impairment (IAS 39)", {"FY2016": -7.5, "FY2015": -6.8}),
    ("TOTAL", "Net loans and advances to customers (IAS 39)", {"FY2016": 5865.4, "FY2015": 3542.5}),
    ("DATA", "Credit quality - neither past due nor impaired", {"FY2016": 5762.7, "FY2015": 3473.9}),
    ("DATA", "Credit quality - past due but not impaired", {"FY2016": 88.8, "FY2015": 60.0}),
    ("DATA", "Credit quality - individually impaired", {"FY2016": 6.6, "FY2015": 4.6}),
    ("DATA", "Credit quality - portfolio impaired (predominantly retail loans 90 days or more past due)", {"FY2016": 14.8, "FY2015": 10.9}),
    ("DATA", "Allowance for impairment held against individually impaired loans", {"FY2016": -1.8, "FY2015": -3.3}),
    ("DATA", "Allowance for impairment held collectively", {"FY2016": -5.7, "FY2015": -3.5}),
    # 2026-09-15 historical Pillar 3 recovery. Kept in its own section because
    # a Basel II general doubtful-debt provision is an INCURRED-loss measure and
    # is not the same thing as the IFRS 9 expected-credit-loss allowance rows
    # above - the two must never be read as one series.
    ("SECTION", "Basel II incurred-loss provisioning (FY2010-FY2014) - separate basis, NOT comparable with the IFRS 9 ECL rows above", {}),
    ("DATA", "General doubtful debt provision, as stated in that year's Pillar 3", {
        "FY2014": 3.5, "FY2013": 1.09, "FY2012": "Unreached today – FY2012 Pillar 3 ('Pillar 3 Disclosure update - December 2012.pdf', linked Feb 2014): not in Wayback, archive.ph or Common Crawl; live 404 incl. globalassets slugs (2026-09-19); FY2013 edition has no 2012 column", "FY2011": 0.186, "FY2010": 0}),
    ("DATA", "Past due >20% impaired secured exposure (Basel II credit risk table)", {"FY2014": 2.2, "FY2013": 1.1}),
]

bw.add_asset_quality_sheet(
    title="Metro Bank PLC - Asset Quality",
    subtitle="Group/consolidated basis, £m (Group loans and advances to customers ties exactly to the Consolidated "
              "Balance Sheet, not the Company balance sheet above - see source note). The FY2010-FY2014 block at "
              "the bottom is pre-IFRS 9 incurred-loss provisioning on a separate basis - see its section header.",
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
        "and the NPL table above were sourced) - left blank rather than estimated.\n\n"
        "FY2016/FY2015 BLOCK ADDED 2026-09-18 (interior-gap pass). These two years were an interior hole on this "
        "sheet - FY2017's Total NPL ratio sat above them and the FY2010-FY2014 Basel II block below them - so the "
        "blanks could not be explained by the data not yet existing. Source: Metro Bank PLC Annual Report and "
        "Accounts 2016, Note 10 'Loans and advances to customers and banks', printed pp.91-92 (PDF pp.95-96) - "
        + AR_2016 + " - which prints Group 2016, Group 2015, Company 2016 and Company 2015 as four columns. The "
        "GROUP columns are used, consistent with the rest of this sheet, and no Company figure appears here (they "
        "differ materially: the Company allowance for impairment is 6,610 for 2016 and 3,580 for 2015 against the "
        "Group's 7,494 and 6,783). Converted from the source GBP'000 to GBP'm at one decimal place. FY2015 is a "
        "COMPARATIVE COLUMN, taken from the following year's edition; it is used because the FY2015 Annual Report's "
        "own Note 33 was read this pass and carries a Tier 1 capital build-up only, with no loan-book credit-quality "
        "table of this shape. WHY THIS BLOCK IS SEPARATE, three ways: (i) these are IAS 39 INCURRED-loss figures, so "
        "'allowance for impairment' is not the IFRS 9 expected-credit-loss allowance in the rows above and the two "
        "must never be read as one series; (ii) equally they are not the Basel II Pillar 3 general doubtful-debt "
        "provision in the block below, which is a regulatory measure - though note the two agree for FY2016: the "
        "Pillar 3 Disclosure 2016 states 'the group held a collective impairment provision of GBP 5.7 million, and "
        "provision of GBP 1.8 million against individual loan exposures', reproducing Note 10's 5,669 and 1,825 to "
        "the GBP 0.1m; (iii) IAS 39's credit-quality categories (neither past due nor impaired / past due but not "
        "impaired / individually impaired / portfolio impaired) are not IFRS 9 stages and are not mapped onto them. "
        "ROUNDING: the four FY2015 credit-quality rows sum to 3,549.4 as displayed against the 3,549.3 gross figure "
        "above them, because the source's GBP'000 components (3,473,856 + 60,033 + 4,562 + 10,880 = 3,549,331) foot "
        "exactly but round independently - a display artefact of the GBP'm conversion, not a data error, and the "
        "reason those four rows are deliberately left without a TOTAL row of their own. The FY2016 equivalents "
        "(5,762,719 + 88,811 + 6,555 + 14,779 = 5,872,864) foot exactly at one decimal place.\n\n"
        "2026-09-15 (Pillar 3 2019 pass): FY2019/FY2018 Total ECL allowance (-34 both years) is now sourced from the "
        "Pillar 3 2019's own narrative under Table 16 (p.39) and Table 18 Loss allowance under IFRS 9 (p.41). The "
        "FY2019/FY2018 Stage 1/2/3 gross carrying amounts remain blank on purpose: Table 18 discloses loss allowance "
        "BY STAGE (FY2019: Stage 1 -9, Stage 2 -5, Stage 3 -20, POCI 0) but the document contains no gross carrying "
        "amount by stage, and the coverage ratio is likewise not stated - both would have to be back-solved, which "
        "this project does not do. Separately, Table 17 EU CR1-A reports a regulatory defaulted exposure of GBP 92m "
        "(FY2018: GBP 59m); that is a different definition from the Annual Report's non-performing loan measure of "
        "GBP 77m (FY2018: GBP 21m) already recorded above, so the two are NOT merged and the NPL rows are left as "
        "the Annual Report reported them.\n\n"
        "2026-09-15 BASEL II BLOCK (FY2010-FY2014): the general doubtful-debt provision figures are the single "
        "narrative sentence each recovered Pillar 3 edition devotes to provisioning, in its section 5.4 "
        "'Non-performing Loans and Provisioning' - verbatim: FY2014 'At the end of 2014 there was a general "
        "doubtful debt provision of GBP 3.5m'; FY2013 'a general doubtful debt provision of GBP 1.09m'; FY2011 'a "
        "general doubtful debt provision of GBP 186k'; FY2010 'At the end of 2010 there were no specific and "
        "general doubtful debt provisions required', which is an explicitly stated nil and is recorded as 0, not "
        "left blank. BASIS WARNING: these are INCURRED-LOSS provisions under the pre-IFRS 9 regime described in "
        "those documents ('A general provision is raised against performing balances and a specific provision is "
        "raised against non-performing or defaulted agreements'), which is a fundamentally different measurement "
        "basis from the IFRS 9 expected-credit-loss allowance in the rows above. They are on their own labelled "
        "rows and must not be spliced onto the ECL series. The past-due row is the 'Past Due >20% Impaired "
        "Secured' exposure line in the FY2013/FY2014 credit-risk tables (FY2013 1,093.08 GBP'000, FY2014 2,165 "
        "GBP'000); FY2010 and FY2011 have no such line. Note that the FY2013 general provision (GBP 1.09m) and "
        "the FY2013 past-due exposure (GBP 1.09m) are the same number - that is what both places in the source "
        "document say, and it is reproduced rather than treated as a transcription error. No NPL, stage or "
        "coverage data of any kind exists in the Basel II editions, so those rows stay blank for FY2010-FY2014.\n\n"
        + HIST_P3_NOTE
    ),
    first_col_width=76,
    source_height=340,
    unit_suffix=" (£m)",
    years=PILLAR3_YEARS,
)


def vals(data):
    return {y: data.get(y) for y in PILLAR3_YEARS}


# 2026-09-15 historical Pillar 3 recovery. FY2010-FY2013 are covered by Basel II
# editions (FY2012's is genuinely absent - see HIST_P3_NOTE). Explicit markers,
# not blanks: a blank cell is indistinguishable from an unresearched gap and
# gets re-chased forever.
HIST_P3_YEARS = ["FY2013", "FY2012", "FY2011", "FY2010"]
NA_BASEL2 = "Not applicable (Basel II)"
ND_BASEL2 = "Not publicly disclosed"
# GA-020 (2026-09-19): "FY2012 Pillar 3 not located" is a limit on OUR reach and now carries
# the reserved phrase. Tried today: Wayback CDX of metrobankonline.co.uk/Global/* (every
# pre-2016 Pillar 3 lived there) lists the FY2010, FY2011, FY2013 and FY2014 editions and no
# FY2012 one; the FY2011-pattern path "Pillar 3 Disclosure - 2012.pdf" 301s to a 404 live.
# Companies House "Full accounts made up to 31 December 2012" (filed 04 Jun 2013, 45pp scan)
# was OCR'd and its pages viewed: its Note 25 'Capital management' gives no capital amount and
# points to the Directors' report KPI table, which prints only 'Capital as %age of risk
# weighted assets 55%' (carried on the Total Capital Ratio sheet).
NOT_LOCATED_2012 = "Unreached today – FY2012 Pillar 3 ('Pillar 3 Disclosure update - December 2012.pdf', linked Feb 2014): not in Wayback, archive.ph or Common Crawl; live 404 incl. globalassets slugs (2026-09-19); FY2013 edition has no 2012 column"


def hist_na():
    """Structurally inapplicable across FY2010-FY2013: the metric did not exist
    in Metro Bank's Basel II disclosure regime at all, so an FY2012 edition
    would not have carried it either - hence FY2012 is marked the same way."""
    return {y: NA_BASEL2 for y in HIST_P3_YEARS}


# GA-020 (2026-09-19): the bare "Not publicly disclosed" cells for FY2010/FY2011/FY2013 were
# re-checked against each year's STATUTORY ACCOUNTS as well as the Pillar 3 (Companies House
# 06419578 scans, OCR'd 2026-09-19 and the KPI tables viewed as page images):
#   FY2010 accounts (16 months to 31 Dec 2010), Directors' report KPI table (PDF p.6):
#     'Tier 1 capital £89.8m / Risk weighted assets £19.0m / Tier 1 ratio 474%'.
#   FY2011 accounts, KPI table (PDF p.5): 'Capital as %age of risk weighted assets 74%'.
#   FY2012 accounts, KPI table (PDF p.7): 55% (2011: 74%).
#   FY2013 accounts, KPI table (PDF p.7): 50% (2012: 55%).
#   FY2014 group accounts, Financial Highlights (PDF p.4): 28% (2013: 50%).
# These are FOUND figures and are written as printed. The bank does not say which RWA it
# divides by; FY2010's £19.0m equals the Pillar 3 credit-risk-only RWA (18,950k), so the KPI
# ratios are almost certainly over credit-risk RWA only - flagged in the cells, not adjusted.
# 69.1/93.2 = 74.2% ties FY2011; 381.5/775.3 = 49.2% against a printed 50% for FY2013 does
# not tie exactly - recorded, not reconciled. "Capital" is the whole capital base, which the
# Pillar 3 editions state is entirely Tier 1, so the ratio is carried on the Total Capital
# Ratio sheet (capital / RWA); only FY2010's explicitly labelled 'Tier 1 ratio' goes on the
# Tier 1 Ratio sheet. No total RWA (incl. operational risk) is printed in any document.
_KPI_TCR = {
    "FY2013": "50% (FY2013 accounts KPI 'Capital as %age of risk weighted assets'; Basel II, RWA basis unstated)",
    "FY2012": "55% (FY2012 accounts KPI 'Capital as %age of risk weighted assets'; Basel II, RWA basis unstated)",
    "FY2011": "74% (FY2011 accounts KPI 'Capital as %age of risk weighted assets'; Basel II, RWA basis unstated)",
    "FY2010": ("Not published – FY2010 accounts and Pillar 3 print no total capital ratio; accounts print "
               "'Tier 1 ratio 474%' (no Tier 2 held) - on Tier 1 Ratio sheet"),
}
_KPI_T1R = {
    "FY2013": ("Not published – FY2013 Pillar 3 and accounts print no Tier 1 ratio; accounts KPI "
               "'Capital as %age of RWA' 50% is on Total Capital Ratio sheet"),
    "FY2012": NOT_LOCATED_2012,
    "FY2011": ("Not published – FY2011 Pillar 3 and accounts print no Tier 1 ratio; accounts KPI "
               "'Capital as %age of RWA' 74% is on Total Capital Ratio sheet"),
    "FY2010": "474% (FY2010 accounts KPI 'Tier 1 ratio', CH filing PDF p.6; over RWA £19.0m = credit-risk RWA)",
}
_NO_TOTAL_RWA = {
    y: (f"Not published – {y} Pillar 3 prints credit-risk RWA only (row below) and {y} accounts print no "
        "RWA amount; no total incl. operational risk anywhere")
    for y in ("FY2014", "FY2013", "FY2011")}
_NO_TOTAL_RWA["FY2010"] = ("Not published – FY2010 accounts' 'Risk weighted assets £19.0m' equals the Pillar 3 "
                           "credit-risk-only RWA (18,950k, row below); no total incl. op risk printed")
_NO_TOTAL_RWA["FY2012"] = NOT_LOCATED_2012


def hist_nd():
    """Existed as a concept under Basel II but is stated nowhere in any of the
    three recovered editions; FY2012's edition was never located."""
    return {y: (NOT_LOCATED_2012 if y == "FY2012" else ND_BASEL2) for y in HIST_P3_YEARS}


# Basel II / GENPRU Total Regulatory Capital (= Tier 1; no Tier 2 held), GBP'm,
# as printed on the bottom line of each edition's own capital table. FY2012's
# edition was published but never archived (unreached).
BASEL2_TOTAL_CAPITAL = {"FY2014": 387.3, "FY2012": NOT_LOCATED_2012, "FY2013": 381.5, "FY2011": 69.1, "FY2010": 89.8}
# Credit-risk-only RWA, Basel II standardised approach, GBP'm. Operational risk
# under the Basic Indicator Approach is never quantified in any edition, so no
# total RWA figure exists to transcribe.
BASEL2_CREDIT_RWA = {"FY2014": 1415.9, "FY2012": NOT_LOCATED_2012, "FY2013": 775.3, "FY2011": 93.2, "FY2010": 19.0}


# ---------------------------------------------------------------------------
# KM1 Key Metrics (wayfinder KM1-020, 2026-09-16)
#
# Placed BEFORE the first add_metric_sheet() call so the sheet lands
# immediately after Asset Quality and immediately before CET1 Capital, per the
# locked sheet order in wayfinder/km1/map.md.
#
# YEARS COVERED - FY2021 to FY2025 ONLY, and this is a fact about the source
# documents, not a gap. Metro Bank's Pillar 3 editions for FY2016-FY2021 were
# each read cover to cover for this ticket and NONE of them prints the KM1
# template. Their index of tables runs "Table 1: RWA Summary / Table 2: Key
# Ratios / Table 3: Capital Composition / ... / Table 7 (or 9): Comparison of
# institutions' own funds ... IFRS 9 ... / EU OV1 / EU LIQ1 ...". "Table 2: Key
# Ratios" is a four-to-six line summary (CET1 / Tier 1 / Total capital / CRR
# leverage / LCR, with a prior-year comparison), with no row numbers, no SREP
# rows, no buffer rows, no HQLA/net-outflow build-up and no NSFR block. That
# fails the row-set test (map rule 8) the same way ABC International Bank's
# "Table 3 Key Regulatory Metrics" does, so it is NOT transcribed onto KM1 row
# numbers. The UK KM1 template arrived with the Disclosure (CRR) Part of the
# PRA Rulebook, applying from 1 January 2022, which is exactly where Metro
# Bank's first KM1 appears. The sheet therefore uses a years= override rather
# than PILLAR3_YEARS: a KM1 column for FY2010-FY2020 would be 11 blank columns
# asserting nothing.
#
# FY2021 comes from the FY2022 edition's 31 December 2021 comparative column,
# because the FY2021 edition prints no KM1 at all. Stated on the sheet.
#
# ENTITY (map rule 6 - check the entity of every column, not just its year):
# each edition prints the template exactly once, so there is no rule-11 double
# printing here, but the REPORTING ENTITY CHANGES MID-SERIES. The FY2022
# edition's every page header reads "Metro Bank PLC Pillar 3 2022"; the FY2023,
# FY2024 and FY2025 editions' every page header reads "Metro Bank Holdings PLC
# | Pillar 3 20XX". FY2021/FY2022 are therefore Metro Bank PLC and
# FY2023-FY2025 are Metro Bank Holdings PLC consolidated - the same basis split
# already labelled on every other Pillar 3 sheet in this workbook (see
# ENTITY_NOTE). At the 31 December 2022 column the two editions agree exactly
# (819 / 1,069 / 7,990 in both the FY2022 and the FY2023 edition), because the
# holding company was not inserted until 19 May 2023.
KM1_YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]

km1_rows = [
    ("SECTION", "Available own funds (amounts) (£'million)", {}),
    ("DATA", "1    Common Equity Tier 1 (CET1) capital",
     {"FY2025": 840, "FY2024": 808, "FY2023": 985, "FY2022": 819, "FY2021": 936}),
    ("DATA", "2    Tier 1 capital",
     {"FY2025": 1082, "FY2024": 808, "FY2023": 985, "FY2022": 819, "FY2021": 936}),
    ("DATA", "3    Total capital",
     {"FY2025": 1232, "FY2024": 958, "FY2023": 1135, "FY2022": 1069, "FY2021": 1184}),
    ("SECTION", "Risk-weighted exposure amounts (£'million)", {}),
    ("DATA", "4    Total risk-weighted exposure amount",
     {"FY2025": 6711, "FY2024": 6442, "FY2023": 7533, "FY2022": 7990, "FY2021": 7454}),
    ("SECTION", "Capital ratios (as a percentage of risk-weighted exposure amount)", {}),
    ("DATA", "5    Common Equity Tier 1 ratio (%)",
     {"FY2025": "12.5%", "FY2024": "12.5%", "FY2023": "13.1%", "FY2022": "10.3%", "FY2021": "12.6%"}),
    ("DATA", "6    Tier 1 ratio (%)",
     {"FY2025": "16.1%", "FY2024": "12.5%", "FY2023": "13.1%", "FY2022": "10.3%", "FY2021": "12.6%"}),
    ("DATA", "7    Total capital ratio (%)",
     {"FY2025": "18.4%", "FY2024": "14.9%", "FY2023": "15.1%", "FY2022": "13.4%", "FY2021": "15.9%"}),
    ("SECTION", "Additional own funds requirements based on SREP (as a percentage of risk-weighted exposure amount)", {}),
    # FY2021 blank on UK 7a-7d, 12, UK 16a/16b and 18-20: the FY2022 edition
    # SHADES OUT those cells in its 31 December 2021 column (verified on the
    # rendered page, not just the text layer). They are empty cells, not
    # dashes and not zeros - map rule 2.
    ("DATA", "UK 7a    Additional CET1 SREP requirements (%)",
     {"FY2025": "0.7%", "FY2024": "0.2%", "FY2023": "0.2%", "FY2022": "0.3%"}),
    ("DATA", "UK 7b    Additional AT1 SREP requirements (%)",
     {"FY2025": "0.2%", "FY2024": "0.1%", "FY2023": "0.1%", "FY2022": "0.1%"}),
    ("DATA", "UK 7c    Additional T2 SREP requirements (%)",
     {"FY2025": "0.3%", "FY2024": "0.1%", "FY2023": "0.1%", "FY2022": "0.1%"}),
    ("DATA", "UK 7d    Total SREP own funds requirements (%)",
     {"FY2025": "9.2%", "FY2024": "8.4%", "FY2023": "8.4%", "FY2022": "8.5%"}),
    ("SECTION", "Combined buffer requirement (as a percentage of risk-weighted exposure amount)", {}),
    ("DATA", "8    Capital conservation buffer (%)",
     {"FY2025": "2.5%", "FY2024": "2.5%", "FY2023": "2.5%", "FY2022": "2.5%", "FY2021": "2.5%"}),
    # FY2021 is a PRINTED ZERO ("0.0%") in the FY2022 edition, not a dash and
    # not an empty cell - recorded as the zero it is (map rule 2).
    ("DATA", "9    Institution specific countercyclical capital buffer (%)",
     {"FY2025": "2.0%", "FY2024": "2.0%", "FY2023": "2.0%", "FY2022": "1.0%", "FY2021": "0.0%"}),
    ("DATA", "11    Combined buffer requirement (%)",
     {"FY2025": "4.5%", "FY2024": "4.5%", "FY2023": "4.5%", "FY2022": "3.5%", "FY2021": "2.5%"}),
    ("DATA", "UK 11a    Overall capital requirements (%)",
     {"FY2025": "13.7%", "FY2024": "12.9%", "FY2023": "12.9%", "FY2022": "12.0%", "FY2021": "11.6%"}),
    ("DATA", "12    CET1 available after meeting the total SREP own funds requirements (%)",
     {"FY2025": "7.3%", "FY2024": "7.8%", "FY2023": "8.4%", "FY2022": "5.5%"}),
    ("SECTION", "Leverage ratio", {}),
    ("DATA", "13    Total exposure measure excluding claims on central banks (£'million)",
     {"FY2025": 13837, "FY2024": 14417, "FY2023": 18420, "FY2022": 19348, "FY2021": 17869}),
    ("DATA", "14    Leverage ratio excluding claims on central banks (%)",
     {"FY2025": "7.8%", "FY2024": "5.6%", "FY2023": "5.3%", "FY2022": "4.2%", "FY2021": "5.2%"}),
    ("SECTION", "Liquidity Coverage Ratio", {}),
    ("DATA", "15    Total high-quality liquid assets (HQLA) (Weighted value - average) (£'million)",
     {"FY2025": 5552, "FY2024": 7189, "FY2023": 5056, "FY2022": 6051, "FY2021": 6900}),
    ("DATA", "UK 16a    Cash outflows - Total weighted value (£'million)",
     {"FY2025": 1962, "FY2024": 2184, "FY2023": 2335, "FY2022": 2729}),
    ("DATA", "UK 16b    Cash inflows - Total weighted value (£'million)",
     {"FY2025": 189, "FY2024": 413, "FY2023": 256, "FY2022": 264}),
    ("DATA", "16    Total net cash outflows (adjusted value) (£'million)",
     {"FY2025": 1773, "FY2024": 1854, "FY2023": 2079, "FY2022": 2465, "FY2021": 2169}),
    ("DATA", "17    Liquidity coverage ratio (%)",
     {"FY2025": "314%", "FY2024": "444%", "FY2023": "244%", "FY2022": "246%", "FY2021": "318%"}),
    ("SECTION", "Net Stable Funding Ratio", {}),
    ("DATA", "18    Total available stable funding (£'million)",
     {"FY2025": 13965, "FY2024": 16676, "FY2023": 18277, "FY2022": 18903}),
    ("DATA", "19    Total required stable funding (£'million)",
     {"FY2025": 8448, "FY2024": 10475, "FY2023": 13442, "FY2022": 13225}),
    ("DATA", "20    NSFR ratio (%)",
     {"FY2025": "165%", "FY2024": "160%", "FY2023": "136%", "FY2022": "143%"}),
]

KM1_SOURCES = (
    "KM1 Key Metrics sheet - each year transcribed from the 31 December column of THAT YEAR'S OWN Pillar 3 "
    "edition (map rule 1), with one stated exception (FY2021, below). Every edition prints the template as a "
    "three-column table - 31 December of the reporting year, 30 June of the reporting year, and 31 December of "
    "the prior year - and ONLY the 31 December reporting-year column is taken. (This workbook has been bitten by "
    "that before: ST-026 corrected six Pillar 3 metric sheets in which FY2023-FY2025 had been read off the 30 "
    "June interim column.)\n\n"
    "FY2025 - Metro Bank Holdings PLC Pillar 3 2025, 'Table 4: UK KM1 - Key metrics', printed p.10 (PDF p.10), "
    + P3_2025 + "\n"
    "FY2024 - Metro Bank Holdings PLC Pillar 3 2024, 'Table 4: UK KM1 - Key metrics', printed p.12 (PDF p.12), "
    + P3_2024 + "\n"
    "FY2023 - Metro Bank Holdings PLC Pillar 3 2023, 'Table 4: UK KM1 - Key metrics', printed p.12 (PDF p.12), "
    + P3_2023 + "\n"
    "FY2022 - Metro Bank PLC Pillar 3 2022, 'Table 3: UK KM1 - Key metrics', printed p.10 (PDF p.11), "
    + P3_2022 + "\n"
    "FY2021 - THE FY2021 EDITION PRINTS NO KM1, so this column is the FY2022 edition's own 31 December 2021 "
    "comparative, taken from the same Table 3 cited above and labelled as such rather than presented as a "
    "FY2021-edition figure. All five FY2022-edition URLs re-fetched 2026-09-16 with a browser User-Agent and "
    "verified HTTP 200 / Content-Type application/pdf / %PDF magic bytes.\n\n"
    "WHY THERE IS NO KM1 BEFORE FY2021. Metro Bank's FY2016-FY2021 Pillar 3 editions were read for this ticket "
    "and none contains the template. Each one's index of tables offers 'Table 2: Key Ratios' - a short summary "
    "of CET1 / Tier 1 / Total capital / CRR leverage / LCR against the prior year, with no row numbers, no SREP "
    "rows, no combined-buffer rows, no HQLA and net-cash-outflow build-up and no NSFR block. That is a different "
    "and shorter table, not an unnumbered KM1, so it is NOT mapped onto KM1 row numbers; doing so would invent a "
    "correspondence Metro Bank never published. The UK KM1 template arrived with the Disclosure (CRR) Part of "
    "the PRA Rulebook, applying from 1 January 2022, which is precisely when Metro Bank's first KM1 appears. The "
    "capital, leverage and liquidity figures those earlier editions DO publish already populate the eleven "
    "single-metric sheets in this workbook and are not duplicated here.\n\n"
    "REPORTING ENTITY CHANGES MID-SERIES, and the columns are labelled accordingly. FY2021 and FY2022 are Metro "
    "Bank PLC (every page header of the FY2022 edition reads 'Metro Bank PLC Pillar 3 2022'). FY2023, FY2024 and "
    "FY2025 are Metro Bank Holdings PLC and its subsidiaries (every page header reads 'Metro Bank Holdings PLC | "
    "Pillar 3 20XX'), following the insertion of the holding company on 19 May 2023. The two editions agree "
    "exactly at 31 December 2022 (CET1 819, total capital 1,069, RWAs 7,990 in both the FY2022 and the FY2023 "
    "edition), because the restructure post-dates that balance-sheet date. The series is NOT presented as one "
    "continuous entity - see the workbook's entity/basis note.\n\n"
    "BLANK CELLS, each one a row the bank printed and left empty rather than a row we failed to find. In the "
    "FY2022 edition the 31 December 2021 column is SHADED OUT for UK 7a, UK 7b, UK 7c, UK 7d, 12, UK 16a, UK "
    "16b, 18, 19 and 20 - confirmed by rendering the page at 200 dpi and looking, not only from the text layer. "
    "Those cells are empty, not dashes and not zeros, so they are left blank. By contrast row 9 (institution "
    "specific countercyclical capital buffer) prints '0.0%' in that same 31 December 2021 column, and a printed "
    "zero is recorded as a zero.\n\n"
    "ROWS 10 AND UK 10a ARE ABSENT FROM EVERY EDITION. Metro Bank's combined-buffer block runs 8, 9, 11, UK 11a, "
    "12 in all four editions; it never prints a row 10 (systemic risk buffer) or UK 10a (O-SII buffer). They are "
    "not shown as blank rows because the bank does not print them at all - which is a different statement from a "
    "printed-but-empty cell.\n\n"
    "THE BANK'S OWN FOOTNOTES, reproduced because they carry the basis: (i) the FY2022 edition footnotes its "
    "leverage block 'Restated UK Leverage Ratio for comparison. Recalculated based on changes in PRA Policy "
    "Statement 21/21 to exclude claims on central banks' - i.e. the 1 January 2022 basis break (map rule 5) is "
    "handled by the bank restating the earlier column onto the new 'excluding claims on central banks' caption, "
    "so rows 13/14 carry one caption throughout and the pre-2022 'including central bank claims' series is kept "
    "SEPARATELY, on its own two rows of the Leverage Ratio sheet, never merged into this one; (ii) 'LCR is based "
    "on 12-month average'; (iii) 'NSFR is based on 4-quarter average'.\n\n"
    "PRECISION AND TYPOGRAPHY kept as printed: all percentages to one decimal place except rows 17 and 20, which "
    "the bank prints as whole percentages. The FY2023-FY2025 editions typeset their section headings with an "
    "en-dash ('Risk-weighted exposure amounts' is printed 'Risk–weighted exposure amounts') where the FY2022 "
    "edition uses a hyphen; a plain hyphen is used on this sheet and the drift is recorded here rather than "
    "reproduced glyph-for-glyph.\n\n"
    "ONE DELIBERATE DIVERGENCE FROM THE LCR SHEET, DOCUMENTED RATHER THAN SILENCED. KM1 row 17 for FY2021 is "
    "318%, while the LCR sheet's headline Liquidity Coverage Ratio row for FY2021 is 281%. Both are Metro Bank's "
    "own published figures for 31 December 2021 on DIFFERENT BASES, and the FY2021 Pillar 3 edition says so "
    "itself in section 8.2: 'Table 29 has been updated to align to the EBA/GL/2017/01 Guidelines and therefore "
    "shows the amount of high-quality liquid assets, total net cash outflows and the LCR, averaged over a "
    "12-month period. The ratio at the period end was 281%.' Its Table 29 (EU LIQ1) then prints HQLA 6,900, net "
    "cash outflow 2,169 and a liquidity coverage ratio of 318% - the same three figures the FY2022 edition's KM1 "
    "carries in its 31 December 2021 column, which independently corroborates that comparative. So 318% is the "
    "12-month average and 281% is the point-in-time ratio at the balance-sheet date. Neither figure has been "
    "edited to agree with the other. (Note in passing that 6,900 / 2,169 = 318%, so the LCR sheet's own HQLA and "
    "net-outflow rows for FY2021 are the average-basis figures; only its headline ratio cell is the point-in-time "
    "one.)\n\n"
    "NEWER THAN THIS WORKBOOK, FLAGGED NOT TRANSCRIBED: the IR page also carries an H1 2026 edition, 'Metro Bank "
    "Pillar 3 30 June 2026' (metro-bank-pillar-3-30-june-2026.pdf), and interim financial statements to 30 June "
    "2026. They add no financial YEAR - Metro Bank's year-end is 31 December and FY2026 has not occurred - so "
    "they are outside this workbook's annual series, but a later interim-focused ticket should pick them up.\n\n"
    + ENTITY_NOTE
)

bw.add_km1_sheet(
    title="Metro Bank - KM1 Key Metrics",
    subtitle="Metro Bank's own \"UK KM1 - Key metrics\" table, reproduced in the bank's own row order, row "
             "numbers, labels and printed precision. £'million and % exactly as published. FY2021-FY2022 are "
             "Metro Bank PLC; FY2023-FY2025 are Metro Bank Holdings PLC consolidated, following the 19 May 2023 "
             "holding-company insertion. FY2021 is the FY2022 edition's 31 December 2021 comparative, because "
             "the FY2021 edition prints no KM1. No KM1 exists for FY2010-FY2020: the template post-dates those "
             "editions, whose 'Table 2: Key Ratios' is a short summary, not an unnumbered KM1. Blank cells are "
             "rows the bank printed and left empty; each is explained in the source note below.",
    rows=km1_rows,
    sources_text=KM1_SOURCES,
    first_col_width=86,
    source_height=620,
    years=KM1_YEARS,
)


def metric(name, unit, rows_data, note=None):
    bw.add_metric_sheet(name, unit, rows_data, P3_SOURCES, note=note, first_col_width=56, source_height=190, years=PILLAR3_YEARS)


metric("CET1 Capital", "£m", [("Common Equity Tier 1 (CET1) capital", vals(dict({"FY2025": 840, "FY2024": 808, "FY2023": 985, "FY2022": 819, "FY2021": 936,
       "FY2020": 1192, "FY2019": 1427, "FY2018": 1171, "FY2017": 897, "FY2016": 651, "FY2015": 300, "FY2014": 384}, **hist_na())))],
       "FY2010-FY2013 are marked 'Not applicable (Basel II)': Metro Bank's Pillar 3 disclosures for those years pre-date CRD IV entirely and contain no CET1 concept at all (a full-text search of the FY2010/FY2011/FY2013 editions returns zero hits for 'CET1' and 'Common Equity'). The Basel II Tier 1 / Total Regulatory Capital those editions DO disclose is carried on the Tier 1 Capital and Total Capital sheets, on its own separate row. "
       "FY2023-FY2025 are Holdings Group figures following the May 2023 holding-company insertion; FY2021-FY2022 are Metro Bank PLC consolidated prudential figures. CORRECTED 2026-09-03 (ST-026): FY2023-FY2025 previously showed the 30 June interim KM1 column instead of the 31 December year-end column (e.g. FY2024 was 937, the 30 June 2024 figure - the year-end figure is 808); found while cross-checking against the RWA Breakdown sheet's own OV1/KM1 source tables. FY2021-FY2022 were already correct. HD-049: FY2014/FY2015 are Total regulatory capital (=CET1=Tier1=Total capital, no AT1/Tier 2 disclosed in either year) from the Annual Report's own Capital management note/capital structure table, not a Pillar 3 disclosure - see P3_SOURCES note.")
metric("CET1 Ratio", "%", [("Common Equity Tier 1 ratio", vals(dict({"FY2025": "12.5%", "FY2024": "12.5%", "FY2023": "13.1%", "FY2022": "10.3%", "FY2021": "12.6%",
       "FY2020": "15.0%", "FY2019": "15.6%", "FY2018": "13.1%", "FY2017": "15.25%", "FY2016": "18.16%", "FY2015": "13%", "FY2014": "28%"}, **hist_na())))],
       "FY2010-FY2013 'Not applicable (Basel II)' - no CET1 concept existed in those editions (see CET1 Capital sheet's note). "
       "CORRECTED 2026-09-03 (ST-026): FY2023-FY2025 previously showed the 30 June interim column instead of 31 December year-end (see CET1 Capital sheet's note). HD-049: FY2014/FY2015 from the Annual Report (not Pillar 3) - see CET1 Capital sheet's note.")
metric("Tier 1 Capital", "£m", [
    ("Tier 1 capital (CRR/CRD IV basis)", vals({"FY2025": 1082, "FY2024": 808, "FY2023": 985, "FY2022": 819, "FY2021": 936,
       "FY2020": 1192, "FY2019": 1427, "FY2018": 1171, "FY2017": 897, "FY2016": 651, "FY2015": 300, "FY2014": 384})),
    ("Tier 1 capital, Basel II / GENPRU 2.2 basis - as disclosed in that year's own Pillar 3 (NOT continuous with the CRR row above)", vals(BASEL2_TOTAL_CAPITAL)),
], note="SECOND ROW ADDED 2026-09-15 (historical Pillar 3 recovery). The four recovered Metro Bank PLC Pillar 3 editions (FY2010, FY2011, FY2013, FY2014) each state a single 'Tier 1 capital based on the [year] audited accounts' figure computed under the FSA's/PRA's GENPRU 2.2 definition, i.e. Basel II. That is a different definition from the CRR/CRD IV Tier 1 capital on the first row and the two are deliberately NOT merged into one series. "
       "FY2014 APPEARS ON BOTH ROWS AND THE TWO DISAGREE, ON PURPOSE: 384 on the CRR row is the FY2015 Annual Report's Capital management note; 387.3 on the Basel II row is the FY2014 Pillar 3's own printed Total Regulatory Capital of 387,261 (its narrative rounds this to 'GBP 388m'). The GBP 3.3m gap between two different documents on two different bases is documented, not reconciled, and the pre-existing figure was not overwritten. See the source note for the FY2014 table's own GBP 630k internal footing error. "
       "CORRECTED 2026-09-03 (ST-026): FY2023-FY2025 previously showed the 30 June interim column instead of 31 December year-end (see CET1 Capital sheet's note). HD-049: FY2014-FY2017 Tier 1 = CET1 (no AT1 disclosed) - see CET1 Capital sheet's note.")
metric("Tier 1 Ratio", "%", [("Tier 1 ratio", vals(dict({"FY2025": "16.1%", "FY2024": "12.5%", "FY2023": "13.1%", "FY2022": "10.3%", "FY2021": "12.6%",
       "FY2020": "15.0%", "FY2019": "15.6%", "FY2018": "13.1%", "FY2017": "15.25%", "FY2016": "18.16%", "FY2015": "13%", "FY2014": "28%"}, **_KPI_T1R)))],
       "GA-020 2026-09-19: FY2010 FOUND - 474% is the 'Tier 1 ratio' printed in the FY2010 statutory accounts' Directors' report KPI table (Companies House filing, PDF p.6), beside 'Tier 1 capital £89.8m' and 'Risk weighted assets £19.0m'; the £19.0m is the Pillar 3's credit-risk-only RWA, so this ratio is on a credit-risk denominator and is NOT comparable with the CRR series. FY2011/FY2013 remain unpublished as a Tier 1 ratio; the accounts' 'Capital as %age of risk weighted assets' KPI for those years is on the Total Capital Ratio sheet. See the GA-020 comment above hist_nd() in the build script. "
       "FY2010/FY2011/FY2013 'Not publicly disclosed' (2026-09-15, SUPERSEDED for FY2010 by the accounts KPI above): a Tier 1 ratio was a Basel II concept and could in principle have been disclosed, but none of the three recovered editions states one anywhere. It is deliberately NOT computed from the Basel II capital and credit-risk RWA figures elsewhere in this workbook - that would be back-solving, and the denominator would in any case be a credit-risk-only subtotal. FY2012's edition was never located. "
       "CORRECTED 2026-09-03 (ST-026): FY2023-FY2025 previously showed the 30 June interim column instead of 31 December year-end (see CET1 Capital sheet's note). HD-049: FY2014-FY2017 Tier 1 ratio = CET1 ratio (no AT1 disclosed).")
metric("Total Capital", "£m", [
    ("Total capital (CRR/CRD IV basis)", vals({"FY2025": 1232, "FY2024": 958, "FY2023": 1135, "FY2022": 1069, "FY2021": 1184,
       "FY2020": 1441, "FY2019": 1676, "FY2018": 1420, "FY2017": 897, "FY2016": 651, "FY2015": 300, "FY2014": 384})),
    ("Total Regulatory Capital, Basel II / GENPRU 2.2 basis - equals Tier 1, no Tier 2 held (NOT continuous with the CRR row above)", vals(BASEL2_TOTAL_CAPITAL)),
], note="SECOND ROW ADDED 2026-09-15: the Basel II bottom line printed in each recovered Pillar 3 edition's capital table. These editions describe the entire capital base as Tier 1 ('the Bank's capital base was made up of GBP Xm of Tier 1 capital') and contain no occurrence of 'Tier 2' at all, so Total Regulatory Capital equals Tier 1 for FY2010-FY2014 as a matter of what the documents state, not by inference. The FY2014 disagreement between the two rows (384 vs 387.3) is explained on the Tier 1 Capital sheet. "
       "CORRECTED 2026-09-03 (ST-026): FY2023-FY2025 previously showed the 30 June interim column instead of 31 December year-end (see CET1 Capital sheet's note). HD-049: FY2014-FY2017 Total capital = Tier 1 (no Tier 2 disclosed until FY2018's £249m debt securities). FY2014/FY2015 from the Annual Report, not Pillar 3.")
metric("Total Capital Ratio", "%", [("Total capital ratio", vals(dict({"FY2025": "18.4%", "FY2024": "14.9%", "FY2023": "15.1%", "FY2022": "13.4%", "FY2021": "15.9%",
       "FY2020": "18.1%", "FY2019": "18.3%", "FY2018": "15.9%", "FY2017": "15.25%", "FY2016": "18.16%", "FY2015": "13%", "FY2014": "28%"}, **_KPI_TCR)))],
       "GA-020 2026-09-19: FY2011 74%, FY2012 55% and FY2013 50% FOUND - each is the 'Capital as %age of risk weighted assets' KPI printed in that year's own statutory accounts (Companies House scans, Directors' report KPI table; each read from the page image, and each confirmed by the next year's comparative column). The capital base was wholly Tier 1 with no Tier 2 (the Pillar 3 editions say so), so capital/RWA is the total capital ratio; the RWA denominator is not stated and FY2010's shows it was credit-risk RWA only. Basel II basis, NOT continuous with the CRR series above. RATIO TIE: FY2011 69.1/93.2 = 74.2% ties; FY2013 381.5/775.3 = 49.2% vs 50% printed - recorded, not reconciled. The earlier text below saying no ratio appears is right about the Pillar 3 editions only. "
       "FY2010/FY2011/FY2013 'Not publicly disclosed' - no capital ratio of any kind appears in the recovered Basel II editions, and none is back-solved here (see the Tier 1 Ratio sheet's note). FY2012's edition was never located. "
       "CORRECTED 2026-09-03 (ST-026): FY2023-FY2025 previously showed the 30 June interim column instead of 31 December year-end (see CET1 Capital sheet's note). HD-049: FY2014-FY2017 Total capital ratio = CET1 ratio (no Tier 2 disclosed).")
metric("Total RWAs", "£m", [
    ("Total risk-weighted exposure amount", vals(dict({"FY2025": 6711, "FY2024": 6442, "FY2023": 7533, "FY2022": 7990, "FY2021": 7454,
       "FY2020": 7957, "FY2019": 9147, "FY2018": 8936, "FY2017": 5882, "FY2016": 3590, "FY2015": 2261.2},
       **_NO_TOTAL_RWA))),
    ("Credit risk RWA only, Basel II standardised approach - the sole RWA figure these editions disclose (NOT a total RWA)", vals(BASEL2_CREDIT_RWA)),
], note="SECOND ROW ADDED 2026-09-15. The recovered Basel II editions each print an RWA column in their credit-risk exposure table, totalled on the bottom row (captioned 'TOTAL Risk Weighted Assets' in FY2011/FY2013, 'TOTAL' in FY2014, and sitting on the 'Total assets' row in FY2010). Despite the FY2011/FY2013 caption, that figure is NOT a total RWA: the table covers credit-risk exposures only, and each edition states that operational risk is measured under the Basic Indicator Approach without ever quantifying the resulting RWA. It is therefore carried on its own row and never added to, or continued into, the CRR total above. "
       "FY2010-FY2013 read 'Not publicly disclosed' on the first row rather than 'Not applicable': a total Pillar 1 RWA (credit plus market plus operational) WAS a defined Basel II concept, so this is a genuine disclosure gap in those editions, not a structurally inapplicable metric. "
       "FY2014's cell now reads 'Not publicly disclosed' rather than being left blank: the FY2014 Pillar 3 has now been read cover to cover and confirms no total RWA exists to find, which closes that cell instead of leaving it to be re-chased. "
       "FY2015 POPULATED 2026-09-18 (interior-gap pass) AT 2,261.2 - and the sentence it replaces, which said 'FY2015 stays blank', was correct only about the Pillar 3. FY2015 was an interior hole with FY2016 above it and FY2014 below it settled, so it could not be explained by the metric not yet existing. It does exist, in a document already cited on this sheet: Metro Bank PLC's own ANNUAL REPORT AND ACCOUNTS 2016, Strategic Report, 'Capital structure' table, printed p.23, which prints a two-column comparison headed 2016 and 2015 and gives 'Risk weighted assets (RWAs)' as 3,590.4 (2016) and 2,261.2 (2015), alongside the CET1 capital, CET1 ratio and leverage ratio figures this workbook ALREADY takes from that same table for FY2015. The RWA row was simply not transcribed when the others were. The note lower down on this sheet previously asserted that 'FY2014/FY2015 RWAs were not disclosed in the Annual Report (only capital and ratios)'; that is wrong for FY2015 and has been corrected. FY2015 is therefore a COMPARATIVE-COLUMN figure, from the following year's edition, because FY2015's own Annual Report (Note 33 Capital management, printed p.76, read this pass) discloses only the Tier 1 capital build-up - no RWA, no ratio - and no FY2015 Pillar 3 edition exists to check: a Wayback CDX enumeration of the whole metrobankonline.co.uk domain returned 1,078 archived PDFs, whose only Pillar 3 editions are FY2010, FY2011, FY2013, FY2014 and FY2016 onward, and the recurring 'Pillar 3 Disclosure.pdf' URL has exactly three captures (2014-09-15 = the FY2013 edition, a 2015-06-26 revisit of the identical digest, and 2015-12-30 = the FY2014 edition) with nothing in 2016 that could be the FY2015 edition. "
       "RATIO TIE, RECORDED NOT RECONCILED: the same table's FY2015 CET1 ratio of 13.1% does not tie to its own FY2015 CET1 capital and RWAs - 299.9 / 2,261.2 = 13.26%, a 0.2pp break - whereas the FY2016 column ties exactly (651.4 / 3,590.4 = 18.14% against the printed 18.1%). Both FY2015 figures are reproduced as printed and neither is adjusted to make the ratio tie. "
       "CORRECTED 2026-09-03 (ST-026): FY2023-FY2025 previously showed the 30 June interim column instead of 31 December year-end (e.g. FY2024 was 7239, the 30 June 2024 figure - the year-end figure is 6442, confirmed against both the KM1 Key metrics table and the OV1 RWA-by-risk-type table, and against the RWA Breakdown sheet's own total). FY2021-FY2022 were already correct. HD-049, PARTLY SUPERSEDED 2026-09-18: this read 'FY2014/FY2015 RWAs were not disclosed in the Annual Report (only capital and ratios) and are left blank rather than derived by dividing capital by the ratio.' That is still true of FY2014 but was WRONG for FY2015 - the Annual Report and Accounts 2016's 'Capital structure' table (printed p.23) discloses the FY2015 RWA directly, as 2,261.2, and it is now carried. Nothing has been derived by dividing capital by a ratio here or anywhere else on this sheet.")

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
    # FY2019/FY2018: Table 8 EU OV1 row 27 in the Pillar 3 2019 prints an explicit
    # en-dash for both years, i.e. a stated nil - recorded as 0, not left blank.
    ("DATA", "Amounts below the thresholds for deduction (subject to 250% risk weight)", vals({"FY2025": 16, "FY2024": 7, "FY2023": 8, "FY2022": 5, "FY2021": 5,
        "FY2019": 0, "FY2018": 0})),
    ("TOTAL", "Total", vals({"FY2025": 6711, "FY2024": 6442, "FY2023": 7533, "FY2022": 7990, "FY2021": 7454,
        "FY2020": 7957, "FY2019": 9147, "FY2018": 8936, "FY2017": 5882, "FY2016": 3590})),
    # 2026-09-15 historical Pillar 3 recovery. Kept in its own section, below
    # the OV1 total, because these are Basel II standardised-approach exposure
    # classes, not UK/EU OV1 risk types - the two must not be read as one
    # series. Every figure below is printed in the source; none is derived.
    # FY2015 recovered 2026-09-18 (interior-gap pass). It sits in its own section
    # because it is the CRD IV-era "Standardised Credit Risk" exposure-class table
    # the FY2016 Pillar 3 prints with a 2015 comparative column - a different
    # template from both the UK/EU OV1 rows above and the Basel II block below, and
    # credit risk only. No FY2015 Pillar 3 edition exists to take it from directly.
    ("SECTION", "CRD IV standardised credit-risk exposure classes, credit risk only (FY2015) - the 2015 COMPARATIVE COLUMN of the Pillar 3 Disclosure 2016's 'Standardised Credit Risk' table (section 7.1, p.16 of the PDF). A third, separate template: neither a UK/EU OV1 breakdown nor the Basel II table below, and it excludes operational risk entirely. Its rows sum to 2,262 against the 2,261 the table itself prints on its Total line - a GBP 1m rounding break in the bank's own arithmetic, present in its 2016 column too (rows sum to 3,455 against a printed 3,454), reproduced rather than smoothed", {}),
    ("DATA", "Cash and balances with the Bank of England (0% risk weight)", vals({"FY2015": 0})),
    ("DATA", "Loans and advances to banks (20% risk weight)", vals({"FY2015": 13})),
    ("DATA", "Investments (10%-100% risk weight)", vals({"FY2015": 601})),
    ("DATA", "Retail and Business Lending (35%-150% risk weight)", vals({"FY2015": 1362})),
    ("DATA", "Fixed and other assets (100% risk weight)", vals({"FY2015": 219})),
    ("DATA", "Past Due >20% impaired secured (50% risk weight)", vals({"FY2015": 4})),
    ("DATA", "Secured and unsecured lending facilities (20%-100% risk weight)", vals({"FY2015": 63})),
    ("TOTAL", "Total credit risk RWA, CRD IV standardised approach (as printed; excludes operational risk)", vals({"FY2015": 2261})),

    ("SECTION", "Basel II standardised approach, credit risk only (FY2010-FY2014) - separate basis, NOT part of the UK/EU OV1 total above", {}),
    ("DATA", "Loans and advances to banks (20% risk weight)", vals({"FY2014": 6.8, "FY2013": 5.0, "FY2011": 5.7, "FY2010": 1.1})),
    ("DATA", "Investments (10%-100% risk weight)", vals({"FY2014": 406.3, "FY2013": 155.3, "FY2011": 7.8})),
    ("DATA", "Secured residential lending (35%-75% risk weight)", vals({"FY2013": 138.2, "FY2011": 8.7})),
    ("DATA", "Retail lending (35%-75% risk weight; FY2014 label)", vals({"FY2014": 344.8})),
    ("DATA", "Retail and commercial lending (75%-100% risk weight; FY2011/FY2013 label)", vals({"FY2013": 285.5, "FY2011": 17.6})),
    ("DATA", "SME and commercial (35%-100% risk weight; FY2014 label)", vals({"FY2014": 426.0})),
    ("DATA", "Loans and advances to customers (75% risk weight; FY2010 label)", vals({"FY2010": 0.1})),
    ("DATA", "Fixed and other assets (100% risk weight)", vals({"FY2014": 166.6, "FY2013": 160.3, "FY2011": 50.3})),
    ("DATA", "Tangible fixed assets (100% risk weight; FY2010 label)", vals({"FY2010": 17.3})),
    ("DATA", "Prepayments and accrued income (100% risk weight; FY2010 label)", vals({"FY2010": 0.4})),
    ("DATA", "Past due >20% impaired secured (50% risk weight)", vals({"FY2014": 1.1, "FY2013": 0.5})),
    ("DATA", "Contingent assets - secured and unsecured lending facilities", vals({"FY2014": 64.3, "FY2013": 30.5, "FY2011": 3.2})),
    ("DATA", "Cash and balances with the Bank of England, and UK government bonds (0% risk weight)", vals({"FY2014": 0, "FY2013": 0, "FY2011": 0, "FY2010": 0})),
    ("TOTAL", "Total credit risk RWA, Basel II standardised approach (excludes operational risk, which is never quantified)", vals(BASEL2_CREDIT_RWA)),
]
bw.add_rwa_breakdown_sheet(
    title="Metro Bank PLC - RWA Breakdown",
    subtitle="Pillar 3 UK/EU OV1 template. FY2023-FY2025 are Holdings Group figures; FY2021-FY2022 are the Metro "
              "Bank PLC prudential perimeter (same basis split as the other Pillar 3 sheets). The FY2010-FY2014 "
              "block at the bottom is a SEPARATE Basel II standardised-approach credit-risk table on a different "
              "basis - read it on its own, never as a continuation of the OV1 rows above.",
    rows=rwa_breakdown_rows,
    sources_text=P3_SOURCES + (
        "\n\nRWA Breakdown table: FY2025 - Pillar 3 Disclosure 2025, Table 6 UK OV1, p.12. FY2024 - Pillar 3 "
        "Disclosure 2024, Table 6 UK OV1, p.14. FY2023 - Pillar 3 Disclosure 2023, Table 6 UK OV1, p.14. FY2022 - "
        "Pillar 3 Disclosure 2022, Table 5 UK OV1, p.12. FY2021 - Pillar 3 Disclosure 2021, Table 10 EU OV1, p.52. "
        "All 5 years' totals tie exactly to the (corrected) Total RWAs sheet.\n\n"
        "HD-049: FY2020/FY2019/FY2018 - Pillar 3 2020/2019/2018 EU OV1 tables (no separate securitisation line - "
        "embedded within credit risk under the post-2018 template, hence blank). FY2017/FY2016 - each year's own "
        "'Risk Weighted Assets - Pillar 1' table in the 2017 Pillar 3 Disclosure (Credit risk shown standardised "
        "approach, securitisation broken out separately under the pre-2018 template).\n\n"
        "2026-09-15 (FY2019 re-verification against the Pillar 3 2019 PDF, Table 8 EU OV1, p.30): the FY2019/FY2018 "
        "securitisation cells are blank because that template contains NO securitisation row at all - its rows run "
        "1, 2, 6, 7, 12, 19, 20, 23, 24, 27, 29, with securitisation exposures folded into credit risk. The blank is "
        "therefore correct and is deliberately NOT filled with 0, which would falsely assert nil securitisation RWA. "
        "'Amounts below the thresholds for deduction' IS present as row 27 and prints an explicit en-dash for both "
        "FY2019 and FY2018, so those two cells are recorded as a stated 0. All other FY2019/FY2018 lines on this "
        "sheet reproduce Table 8 exactly.\n\n"
        "2026-09-15 BASEL II BLOCK (FY2010-FY2014): these rows reproduce the 'Credit Risk Exposures' table in "
        "each recovered Pillar 3 edition (FY2014 p.13, FY2013 p.14-15, FY2011 p.12, FY2010 p.12), converted from "
        "the source GBP'000 to GBP'm. They are a different template on a different regulatory basis from the UK/EU "
        "OV1 rows above and are placed in their own section for that reason. EXPOSURE CLASS LABELS CHANGED BETWEEN "
        "EDITIONS and are NOT silently merged: FY2010 uses 'Loans and advances to customers'/'Tangible fixed "
        "assets'/'Prepayments and accrued income'; FY2011 and FY2013 use 'Secured residential lending'/'Retail and "
        "commercial lending'/'Fixed and other assets'; FY2014 re-cuts the lending split into 'Retail lending' and "
        "'SME and Commercial'. Each label therefore gets its own row and populates only the years that actually "
        "used it. FY2010's table has no securities/investments RWA line because its gilt and held-to-maturity "
        "holdings are 0% risk weighted; the 0% rows are recorded as a stated 0, since the source prints an "
        "explicit zero or dash for them.\n\n"
        "2026-09-18 FY2015 BLOCK (interior-gap pass): FY2015 had been blank on this sheet while FY2016 above and "
        "FY2014 below were populated - an interior hole, which cannot be explained by the template not yet "
        "existing. No FY2015 Pillar 3 edition exists (see the Total RWAs sheet note for the Wayback enumeration "
        "that establishes this), but the FY2016 edition prints its 'Standardised Credit Risk' exposure table with "
        "a full 2015 comparative column of exposure values and RWAs - section 7.1, p.16 of "
        + P3_2016 + " - and that column is what the FY2015 rows reproduce. It is kept in its own section because "
        "it is a THIRD template, distinct from both the UK/EU OV1 rows and the Basel II rows: CRD IV-era exposure "
        "classes, credit risk only, no operational-risk line at all. Consequently FY2015's 2,261 here is NOT the "
        "same quantity as FY2015's 2,261.2 on the Total RWAs sheet, which comes from the Annual Report and "
        "Accounts 2016's 'Capital structure' table - they happen to be equal to the nearest GBP 0.1m, and that "
        "coincidence is left standing as each document states it rather than being asserted as an identity. "
        "SOURCE-FOOTING BREAK, REPRODUCED NOT SMOOTHED: the seven FY2015 rows sum to 2,262 against the 2,261 the "
        "table prints on its own Total line. The same table's 2016 column has the same GBP 1m break (rows sum to "
        "3,455 against a printed 3,454), so this is the bank's own rounding, not a transcription slip. The printed "
        "total is what the TOTAL row carries and no row has been adjusted to close the gap; the workbook "
        "verifier's reconciliation check reports this block as a mismatch for exactly that reason, and that report "
        "is correct and expected.\n\n"
        "ROUNDING AND SOURCE-FOOTING NOTE for that block: converting independently-rounded GBP'000 components to "
        "GBP'm makes the displayed rows sum to up to GBP 0.1m away from the stated total (FY2010 18.9 vs 19.0; "
        "FY2011 93.3 vs 93.2) - a conversion artifact, not a data error. Separately, the FY2011 and FY2014 source "
        "tables are themselves off by GBP 1k in their own units (FY2011 components sum to 93,153 against a printed "
        "93,152; FY2014 to 1,415,880 against a printed 1,415,881). The printed totals are what is carried on the "
        "TOTAL row, as stated, and the source's own arithmetic is not corrected."
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
    ("Regulatory leverage ratio (as originally disclosed, including central bank claims)", vals(dict({
        "FY2020": "5.6%", "FY2019": "6.6%", "FY2018": "5.4%", "FY2017": "5.5%", "FY2016": "6.5%", "FY2015": "4.9%", "FY2014": "10%"}, **hist_na()))),
], note="FY2010-FY2013 'Not applicable (Basel II)' (2026-09-15): the regulatory leverage ratio is a CRD IV construct with no Basel II counterpart, and the word 'leverage' does not appear anywhere in any of the recovered FY2010/FY2011/FY2013 Pillar 3 editions. Marked structurally inapplicable rather than left blank. "
       "The 2023-2025 figures are Holdings Group figures; 2021-2022 are the Metro Bank PLC prudential perimeter. The 2021-2022 disclosures restate the leverage measure to exclude central-bank claims for comparability. CORRECTED 2026-09-03 (ST-026): FY2023-FY2025 previously showed the 30 June interim column instead of 31 December year-end. HD-049: FY2014-FY2020 predate the 2021-2022 central-bank-claims exclusion methodology entirely, so a separate pair of rows is used for the as-originally-disclosed 'Regulatory leverage ratio' (including central bank claims) rather than conflating the two definitions; FY2020's total exposure measure was not located (only the ratio) and is left blank.")
metric("LCR", "£m / %", [
    ("Total high-quality liquid assets (HQLA), weighted value - average", vals({"FY2025": 5552, "FY2024": 7189, "FY2023": 5056, "FY2022": 6051, "FY2021": 6900,
        "FY2019": 3356, "FY2018": 3489})),
    ("Total net cash outflows, adjusted value", vals({"FY2025": 1773, "FY2024": 1854, "FY2023": 2079, "FY2022": 2465, "FY2021": 2169,
        "FY2019": 1708, "FY2018": 2506})),
    ("Liquidity Coverage Ratio", vals(dict({"FY2025": "314%", "FY2024": "444%", "FY2023": "244%", "FY2022": "246%", "FY2021": "281%",
        "FY2020": "187%", "FY2019": "197%", "FY2018": "139%", "FY2017": "141%", "FY2016": "136%",
        "FY2015": "Not disclosed in any located FY2015/FY2016 document",
        "FY2014": "Not applicable (pre-dates the 1 October 2015 UK LCR requirement)"}, **hist_na()))),
], note="FY2010-FY2013 'Not applicable (Basel II)' (2026-09-15): the LCR only became a UK requirement on 1 October 2015. The recovered FY2010/FY2011/FY2013 Pillar 3 editions discuss liquidity risk qualitatively under the pre-LCR Individual Liquidity Adequacy Assessment (ILAA) regime and contain no occurrence of 'LCR' or 'liquidity coverage'; they disclose no quantitative liquidity metric of any kind. "
       "The source tables disclose HQLA/net outflow components on different reporting bases across years; the headline ratios are reproduced as reported. Basis changes after the holding-company insertion are described on the Cash Flow Statement and source note. CORRECTED 2026-09-03 (ST-026): FY2023-FY2025 previously showed the 30 June interim column instead of 31 December year-end. FY2015 AND FY2014 CLOSED 2026-09-18 (interior-gap pass) - the ratio cells now carry an explicit statement instead of a blank, so the two years read as settled rather than as outstanding gaps, and the HQLA/net-outflow rows stay blank because no such figures exist to put in them. FY2014 is marked STRUCTURALLY INAPPLICABLE for the same reason FY2010-FY2013 are: the LCR only became a UK requirement on 1 October 2015, nine months after that year-end, and the FY2014 Pillar 3 edition contains no occurrence of 'LCR' or 'liquidity coverage' anywhere in its 21 pages. FY2015 is a different finding and is deliberately worded differently: its year-end falls three months AFTER the LCR took effect, so a disclosure was possible - it simply was not made in anything that can be read. Enumerated rather than assumed, on 2026-09-18: 'LCR'/'liquidity coverage' appears ZERO times in the Annual Report and Accounts 2015 (86pp), ZERO times in the Annual Report and Accounts 2016 (118pp) and ZERO times in the Pillar 3 Disclosure 2016 (25pp) - and the earliest Metro LCR figure that exists anywhere is 136% for FY2016, which appears only as a prior-year comparative inside the FY2017 documents ('remaining strong at 141% (2016: 136%)', Pillar 3 Disclosure 2017 and Annual Report and Accounts 2017). No FY2015 Pillar 3 edition exists to check (see the Total RWAs sheet note for the Wayback enumeration), and the FY2016 edition states 'There have been no material changes in disclosure since the Pillar 3 report for 2015' while itself disclosing no LCR - consistent with the FY2015 edition having disclosed none either, though that last step is an inference and is flagged as one. The same grep run over the Pillar 3 Disclosure 2022 returns many LCR hits, so the search instrument is known to work on these documents. HD-049: FY2020 absolute HQLA/net outflow £m were not located (Pillar 3 2020 discloses only the ratio in the executive summary reviewed this session) and are left blank rather than estimated. BASIS FLAG (2026-09-15): the FY2019/FY2018 HQLA, net-outflow and ratio figures come from Table 26 EU LIQ1 of the Pillar 3 2019 (p.46), which is captioned 'as at 31 December' - a POINT-IN-TIME figure, not the 12-month average that the later UK KM1 rows on this sheet report. The 'average' wording in the first two row labels therefore does not apply to FY2018/FY2019. Flagged rather than merged: the two bases are different series and are not directly comparable year-on-year across the FY2019/FY2021 boundary.")
metric("NSFR", "£m / %", [
    ("Total available stable funding", vals({"FY2025": 13965, "FY2024": 16676, "FY2023": 18277, "FY2022": 18903})),
    ("Total required stable funding", vals({"FY2025": 8448, "FY2024": 10475, "FY2023": 13442, "FY2022": 13225})),
    ("Net stable funding ratio", vals(dict({"FY2025": "165%", "FY2024": "160%", "FY2023": "136%", "FY2022": "143%"},
        **{y: "Not applicable (pre-dates the UK NSFR requirement)"
           for y in ["FY2021", "FY2020", "FY2019", "FY2018", "FY2017", "FY2016", "FY2015", "FY2014"]},
        **{y: ("Not applicable – no UK NSFR requirement before 1 Jan 2022 (PRA PS17/21); the FY2010/11/13 "
               "Basel II Pillar 3s contain no 'NSFR'") for y in HIST_P3_YEARS}))),
], note="FY2010-FY2013 marked 'Not applicable' (2026-09-15): the NSFR did not exist as a UK requirement until 2022, so those years are structurally inapplicable, not gaps. (They are marked 'Not applicable' rather than 'Not applicable (Basel II)' used elsewhere on these sheets, because the NSFR post-dates CRD IV as well as Basel II.) "
       "FY2014-FY2021 CLOSED 2026-09-18 (interior-gap pass): these eight years previously stood BLANK with the prose note alone saying they were not yet a requirement, which made them read as eight outstanding gaps sitting between a populated FY2022 and eight 'Not applicable' cells below. They are now marked on the face of the sheet, on the same footing as FY2010-FY2013 and for the same reason - the NSFR became a binding UK requirement only on 1 January 2022, so no year ending on or before 31 December 2021 could have one. THIS IS ENUMERATED, NOT ASSUMED. Every Metro Bank Pillar 3 edition that exists for those years was fetched on 2026-09-18 and searched for 'NSFR' and 'net stable funding': FY2014 (21pp), FY2016 (25pp), FY2017, FY2018, FY2019, FY2020 and FY2021 (80pp) return ZERO occurrences each; so do the Annual Report and Accounts for 2015, 2016 and 2017. FY2015 has no Pillar 3 edition at all (see the Total RWAs sheet note for the Wayback enumeration), and its own Annual Report likewise has none. POSITIVE CONTROL, so that the zeros are known to mean something: the identical search over the Pillar 3 Disclosure 2022 returns 12 occurrences, including 'Table 16 UK LIQ2 Net Stable Funding Ratio' and the quantitative row this sheet's FY2022 column is taken from. The instrument works; these years genuinely have no NSFR. "
       "FY2023-FY2025 are Holdings Group figures after the restructure. CORRECTED 2026-09-03 (ST-026): FY2023-FY2025 previously showed the 30 June interim column instead of 31 December year-end.")
metric("MREL Ratio", "%", [("MREL ratio", vals({"FY2021": "20.5%", "FY2022": "17.7%", "FY2023": "22.0%", "FY2024": "23.0%", "FY2025": "26.1%",
       "FY2020": "22.4% (total capital plus MREL ratio)", "FY2019": "22.1% (total capital plus MREL ratio)", "FY2018": "Not disclosed (pre-dates MREL requirement)", "FY2017": "Not disclosed (pre-dates MREL requirement)", "FY2016": "Not disclosed (pre-dates MREL requirement)", "FY2015": "Not disclosed (pre-dates MREL requirement)", "FY2014": "Not disclosed (pre-dates MREL requirement)",
       **{y: "Not applicable (pre-dates MREL requirement)" for y in HIST_P3_YEARS}}))],
       "FY2010-FY2013 marked 'Not applicable (pre-dates MREL requirement)' (2026-09-15): MREL was introduced by BRRD and did not exist as a UK requirement in those years; the recovered Basel II Pillar 3 editions contain no occurrence of 'MREL'. This is the same reasoning already applied to FY2014-FY2018 above, simply extended back over the newly-covered years. "
       "FY2022-FY2025 CORRECTED 18 September 2026 (KM1-032). These four cells previously read 'Not disclosed', on the recorded ground that 'no quantitative MREL ratio was located in the later KM1 tables reviewed'. THE CLAIM WAS FALSE, and the sentence names its own error: the search was of KM1, and Metro does not publish MREL in KM1. It publishes it in UK KM2 - Key metrics: MREL, a separate template, present as Table 4 or Table 5 of every edition from FY2022 on. "
       "A SECOND failure compounded the first and is worth recording, because a text search cannot detect it: in the FY2023, FY2024 and FY2025 editions the KM2 table's VALUE COLUMNS DO NOT EXTRACT under pdftotext at all - the row labels come out, the numbers come out empty, and the table renders perfectly on screen. So a text-based sweep of those documents sees the table caption and no figures, and reports 'searched, found nothing' with complete confidence. Every figure below was read from a 150-160dpi page render of the printed table, and each was then cross-checked against the adjacent edition's comparative column, which reproduces it exactly. "
       "Sources, each year from its OWN edition (rows 5 of UK KM2, Total MREL resources as a percentage of total risk-weighted assets): FY2025 26.1% - Pillar 3 2025, printed p.11, Table 5, column '31 December 2025' (MREL resources GBP 1,754m / RWAs GBP 6,711m). FY2024 23.0% - Pillar 3 2024, printed p.13, Table 5, column '31 December 2024' (1,479 / 6,442). FY2023 22.0% - Pillar 3 2023, printed p.13, Table 5, column '31 December 2023' (1,655 / 7,533). FY2022 17.7% - Pillar 3 2022, printed p.12, Table 4, column '31 December 2022' (1,416 / 7,990). FY2021 20.5% - Pillar 3 2022, printed p.12, Table 4, comparative column '31 December 2021' (1,527 / 7,454), which independently confirms the figure already carried here. The corresponding leverage-exposure-basis ratios (KM2 row 7), recorded but not used on this sheet because this sheet reports the RWA basis: 12.7% / 10.3% / 9.0% / 7.3% / 8.5%. "
       "ENTITY AND BASIS BREAK AT FY2023, recorded rather than merged: the FY2022 edition's running head reads 'Metro Bank PLC Pillar 3 2022', while the FY2023, FY2024 and FY2025 editions read 'Metro Bank Holdings PLC | Pillar 3 20XX'. FY2021 and FY2022 are therefore Metro Bank PLC and FY2023 onwards are Metro Bank Holdings PLC consolidated - the holding-company insertion of 19 May 2023 already described on the Cash Flow Statement sheet. The FY2023 edition confirms the holdco is the resolution entity ('MREL-eligible debt is exclusively provided from Metro Bank Holdings PLC'). "
       "The FY2021 cell's 20.5% is a standalone UK KM2 MREL ratio on the RWA basis, so the 'total capital plus MREL ratio' caveat recorded below for FY2019/FY2020 does NOT apply to it. "
       "WHY THE SERIES STOPS AFTER FY2025, stated in the Bank's own words (Pillar 3 2025, section 8, printed p.28): 'In December, the Bank of England confirmed that the Bank will be treated as a transfer firm under its MREL-related resolution framework, effective 1 January 2026.' Metro's external MREL consequently falls to its minimum capital requirement, which is also why it appears in the Bank of England's published external-MREL tables for 2023, 2024 and 2025 and not in the 2026 edition. HD-049: FY2019/FY2020 Pillar 3 disclosures report a 'Total capital plus MREL ratio' (22.1%/22.4%) rather than a standalone MREL ratio - a different (broader) metric than the FY2021 '20.5%', reproduced as-disclosed and labelled accordingly rather than treated as directly comparable. FY2014-FY2018 pre-date the interim MREL requirement referenced in the FY2019 disclosure. LABEL NOTE (2026-09-15): the FY2019 document uses two captions for the same 22.1% - 'Total capital plus MREL ratio' in Table 2 Key Ratios (p.4), and 'Metro Bank's interim MREL ratio' in section 3 (p.25), against a Bank of England interim MREL requirement of 18% of RWAs plus buffers effective 1 January 2020. Both captions are recorded here; the cell keeps the broader Table 2 wording so it is never silently treated as equivalent to the FY2021 standalone 20.5%.")


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
    note="Metro Bank PLC entity basis. Balance Sheet and cash-flow summaries are Company/standalone through FY2025; "
         "Profit & Loss summary is Group/consolidated (Metro Bank PLC does not publish its own income statement). "
         "The Equity Changes summary remains through FY2023 because adding FY2024-FY2025 roll-forward rows would "
         "change the existing worksheet structure. Regulatory ratios change from Metro Bank PLC consolidated basis to Holdings Group basis "
         "after the 19 May 2023 restructure; see the metric and interim-sheet notes. Regulatory figures for "
         "FY2023-FY2025 were corrected 2026-09-03 (ST-026) - see the Total RWAs sheet's note. HD-049: FY2014-FY2020 "
         "added, capped at FY2014 (see ENTITY/BASIS NOTE on the Balance Sheet/Cash Flow/Equity sheets for the "
         "Group-vs-Company basis change at FY2020/FY2021). This Overview's 'Leverage Ratio' row uses the FY2014-"
         "FY2020 'regulatory leverage ratio including central bank claims' as originally disclosed for those years, "
         "and the FY2021-FY2025 'excluding central bank claims' measure for those years (the two are not the same "
         "definition - see the Leverage Ratio sheet's own two-row breakdown for both series in full). "
         "2026-09-15 HISTORICAL PILLAR 3: four Metro Bank PLC Basel II Pillar 3 editions (FY2010, FY2011, FY2013, "
         "FY2014) were recovered and transcribed, so the Pillar 3, Asset Quality and RWA Breakdown sheets now run "
         "to FY2010 alongside the statutory statements. NOTHING FROM THOSE EDITIONS APPEARS ON THIS OVERVIEW: they "
         "disclose no capital ratio, no leverage ratio and no liquidity metric of any kind, and their Basel II "
         "capital and credit-risk RWA figures sit on their own separate rows on the detail sheets precisely "
         "because they are not continuous with the CRR series summarised here. The FY2010-FY2013 ratio cells above "
         "are therefore blank by design. FY2012 is recorded on the detail sheets as a genuinely absent edition, "
         "not an open gap.",
)

bw.save("/Users/armaan/code/katalysis/banks/METRO BANK FINANCIALS.xlsx")
