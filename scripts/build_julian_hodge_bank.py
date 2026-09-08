import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

# PILLAR-3-ONLY WORKBOOK: Julian Hodge Bank Limited (company 00743437, FRN 204439)
# takes the FRS 101 cash-flow-statement disclosure exemption in every one of its FY2021-FY2025
# Annual Reports - explicitly stated each year in Note 1 (Basis of preparation): "the Bank has
# applied the exemptions available under FRS 101 in respect of the following disclosures: A Cash
# Flow Statement and related notes; ..." No Statement of Cash Flows exists in any year's accounts.
# Pillar 3 / capital disclosures are rich for FY2021-FY2023 (full UK KM1-format Key Regulatory
# Metrics tables, standalone Pillar 3 documents), but FY2024-FY2025 have no standalone Pillar 3
# document published - only a brief unaudited "Capital risk management" note inside each year's
# own Annual Report giving CET1/RWA/ratios (no Leverage/LCR/NSFR for those two years). Follows the
# BNY Mellon International / ABC International Bank precedent: standard 13-sheet structure, but
# the Cash Flow Statement sheet documents the exemption instead of line items, and the Overview
# sheet omits the cash-flow chart.

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021", "FY2020", "FY2019", "FY2018", "FY2017", "FY2016",
         "FY2015", "FY2014", "FY2013", "FY2012", "FY2011", "FY2010", "FY2009"]  # most recent first. FY2021-FY2025
# fiscal year-end 30 September; FY2020 is an 11-month transition PERIOD ended 30 September 2020 (the year the
# fiscal year-end changed from 31 October to 30 September - the Bank's own Annual Report 2020 explicitly covers
# "the 11-month period ended 30 September 2020" with its FY2019 comparative column covering the full prior year
# ended 31 October 2019); FY2009-FY2019 fiscal year-end is 31 October.
YEAR_LABEL = {y: y for y in YEARS}

# HD-074 (2026-09-07): Pillar 3 (all 11 metric sheets), Asset Quality, and RWA Breakdown stay out of scope for
# this statutory-statement-only extension - pin them to the original project-wide FY2014-FY2025 window via this
# override. FY2010-FY2013 is HD-004's confirmed real statutory floor for this entity; FY2009 is a bonus beyond
# that floor (found readily as a genuine comparative in the FY2010 Annual Report's own Balance Sheet/Profit and
# Loss Account - see HD074_NOTE below), not force-searched further per the ticket's "don't force it" guidance.
PILLAR3_YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021", "FY2020", "FY2019", "FY2018", "FY2017", "FY2016",
                 "FY2015", "FY2014"]

AR2025_URL = "https://hodgebank.co.uk/wp-content/uploads/2026/02/Hodge-AR-28.01.26.pdf"
AR2024_URL = "https://hodgebank.co.uk/wp-content/uploads/2025/02/Hodge-annual-report-21.02.25.pdf"
AR2023_URL = "https://hodgebank.co.uk/wp-content/uploads/2024/07/Annual-report-Jan-25.01.24.pdf"
AR2022_URL = "https://hodgebank.co.uk/wp-content/uploads/2024/07/Hodge-Annual-Report-April-04.04.23-optimised.pdf"
AR2021_URL = "https://hodgebank.co.uk/wp-content/uploads/2024/07/Hodge-Annual-Report-2020_2021.pdf"
P3_2023_URL = "https://hodgebank.co.uk/wp-content/uploads/2024/07/Hodge-pillar-3-11.03.24.pdf"
P3_2022_URL = "https://hodgebank.co.uk/wp-content/uploads/2024/07/Hodge-pillar-3-19.06.23.pdf"
P3_2021_URL = "https://hodgebank.co.uk/wp-content/uploads/2024/07/Hodge-Pillar-3-Document-2020_2021.pdf"

# HD-049 (historical-depth extension, capped at FY2014): FY2014-FY2020 source documents. The bank's own site no
# longer hosts these live; all retrieved from the Wayback Machine, which held a full historical archive at
# /wp-content/uploads/2019/01/jhb-financial-statements-YYYY1031.pdf and jhb-pillar3-YYYY.pdf (as crawled
# 2019-2022) plus the FY2018/FY2019/FY2020 originals at /wp-content/uploads/2020/02/ and /2021/02/. FY2018
# annual report cross-checked against the Companies House filing history (company 00743437) - both copies agree.
AR2020_URL = "https://web.archive.org/web/20210517011507id_/https://hodgebank.co.uk/wp-content/uploads/2021/02/1.-JHB-Financial-Statements.pdf"
P3_2020_URL = "https://web.archive.org/web/20220620025450id_/https://hodgebank.co.uk/wp-content/uploads/2021/02/2.-JHB-Pillar-III.pdf"
AR2019_URL = "https://web.archive.org/web/20220620025335id_/https://hodgebank.co.uk/wp-content/uploads/2020/02/Julian-Hodge-Bank-Limited-Master-FINAL-EY-Signed-FY19.pdf"
P3_2019_URL = "https://web.archive.org/web/20210517002419id_/https://hodgebank.co.uk/wp-content/uploads/2020/02/Pillar-3-Disclosure-FY19-FINAL.pdf"
AR2018_URL = "https://web.archive.org/web/20210517014628id_/https://hodgebank.co.uk/wp-content/uploads/2020/02/FINAL-Julian-Hodge-Bank-Limited-FY18.pdf"
P3_2018_URL = "https://web.archive.org/web/20210517004624id_/https://hodgebank.co.uk/wp-content/uploads/2019/04/jhb-pillar3-2018.pdf"
AR2017_URL = "https://web.archive.org/web/20220620025318id_/https://hodgebank.co.uk/wp-content/uploads/2019/01/jhb-financial-statements-20171031-1.pdf"
P3_2017_URL = "https://web.archive.org/web/20220620025310id_/https://hodgebank.co.uk/wp-content/uploads/2019/01/jhb-pillar3-2017.pdf"
AR2016_URL = "https://web.archive.org/web/20220620025318id_/https://hodgebank.co.uk/wp-content/uploads/2019/01/jhb-financial-statements-20161031-1.pdf"
P3_2016_URL = "https://web.archive.org/web/20220620025406id_/https://hodgebank.co.uk/wp-content/uploads/2019/01/jhb-pillar3-2016.pdf"
AR2015_URL = "https://web.archive.org/web/20220620025258id_/https://hodgebank.co.uk/wp-content/uploads/2019/01/jhb-financial-statements-20151031.pdf"
P3_2015_URL = "https://web.archive.org/web/20220620025429id_/https://hodgebank.co.uk/wp-content/uploads/2019/01/jhb-pillar3-2015.pdf"
AR2014_URL = "https://web.archive.org/web/20220620025529id_/https://hodgebank.co.uk/wp-content/uploads/2019/01/jhb-financial-statements-20141031.pdf"
P3_2014_URL = "https://web.archive.org/web/20220620025434id_/https://hodgebank.co.uk/wp-content/uploads/2019/01/jhb-pillar3-2014.pdf"

# HD-074 (2026-09-07): FY2010-FY2013 extension, down to this entity's real statutory floor (HD-004/HD-002).
# Same Wayback archive as HD-049's FY2014-FY2020 batch, at the same /wp-content/uploads/2019/01/ path - all 3
# are text-native PDFs (no OCR needed). FY2012's own standalone Annual Report is NOT present anywhere in this
# archive (confirmed via the Wayback CDX API - a genuine gap, not a search failure) - FY2012 figures are instead
# sourced from the FY2013 Annual Report's own FY2012 comparative column (a document-level self-skip of the
# FY2012 standalone report only, not of the year itself, following this project's established convention for
# this kind of gap - see e.g. Vanquis Bank's FY2016 Pillar 3 treatment). FY2009 is a bonus year beyond the
# HD-004 floor, likewise sourced from the FY2010 Annual Report's own FY2009 comparative column (no standalone
# FY2009 report found in this archive either - not force-searched further per the ticket's guidance).
AR2013_URL_HD074 = "https://web.archive.org/web/20220620025323id_/https://hodgebank.co.uk/wp-content/uploads/2019/01/jhb-financial-statements-20131031.pdf"
AR2011_URL_HD074 = "https://web.archive.org/web/20220620025317id_/https://hodgebank.co.uk/wp-content/uploads/2019/01/jhb-financial-statements-20111031.pdf"
AR2010_URL_HD074 = "https://web.archive.org/web/20220620025334id_/https://hodgebank.co.uk/wp-content/uploads/2019/01/jhb-financial-statements-20101031.pdf"

HD074_NOTE = (
    "HISTORICAL-DEPTH NOTE (HD-074, added 2026-09-07): extends Balance Sheet, Profit & Loss and Statement of "
    "Changes in Equity back to FY2009 (one year beyond HD-004's confirmed FY2010 statutory floor) - Pillar 3, "
    "Asset Quality and RWA Breakdown remain capped at FY2014 as a deliberate project-wide scope decision, not a "
    "sourcing gap. This entity has no Cash Flow Statement in any year (see EXEMPTION_NOTE on the Cash Flow "
    "Statement sheet) - the FRS1 predecessor exemption (identical grounds: a parent undertaking includes the "
    "Bank in its own published consolidated accounts) is confirmed explicitly stated in each of the FY2013/"
    "FY2011/FY2010 Annual Reports too, so this extension adds no Cash Flow Statement columns. "
    f"FY2013 (and its own FY2012 comparative): Directors' report and financial statements 2013 - {AR2013_URL_HD074}\n"
    f"FY2011 (and its own FY2010 comparative): Directors' report and financial statements 2011 - {AR2011_URL_HD074}\n"
    f"FY2010 (and its own FY2009 comparative): Directors' report and financial statements 2010 - {AR2010_URL_HD074}\n"
    "All 3 new filings are old UK GAAP (pre-FRS101), consistent with the existing FY2014/FY2015 treatment "
    "already on this sheet - no basis-transition gap exists at the FY2013/FY2014 boundary (FY2013's own closing "
    "Total equity of GBP128.2m ties exactly to FY2014's own opening position). 'Equity shares' is a genuine "
    "small distinct holding line disclosed in the FY2010-FY2012 Balance Sheets (nil in FY2013) - not folded into "
    "Debt securities or another line, since it is its own numbered note in the source accounts. FY2012's own "
    "Profit and Loss Account (per the FY2013 Annual Report's own comparative) reclassified certain cost/income "
    "sub-lines from how they were originally presented (a reclassification only, explained in that report's own "
    "Note 1 - profit for the year and net assets are unaffected). Every one of the 5 new years' Balance Sheet "
    "ties exactly (Total assets = Total liabilities + Total equity, verified to the exact £000) and every new "
    "year's disclosed Profit on ordinary activities before taxation and Total recognised gains and losses in the "
    "financial year are reproduced exactly by the rows on this sheet and the Profit & Loss sheet."
)

ENTITY_NOTE = (
    "ENTITY NOTE: Julian Hodge Bank Limited (company 00743437, FRN 204439, incorporated 1962) is a "
    "privately-owned Cardiff-based bank; immediate parent Hodge Limited, ultimate parent The Carlyle Trust "
    "(Jersey) Limited. Fiscal year-end is 30 September from FY2021 onward (FY2020 was an 11-month transition "
    "period covering the change from the prior 31 October year-end used FY2014-FY2019). All 12 years' source "
    "documents are text-native PDFs, no OCR required."
)

EXEMPTION_NOTE = (
    "FRS 101 / FRS 1 CASH-FLOW EXEMPTION: every Annual Report FY2016-FY2025 states in Note 1 (Basis of "
    "preparation) that the Bank \"has applied the exemptions available under FRS 101 in respect of the following "
    "disclosures: A Cash Flow Statement and related notes; ...\" - e.g. Julian Hodge Bank Limited Annual Report "
    f"2025, Note 1.1, p.42 - {AR2025_URL}. FY2014-FY2015 (pre-FRS101, old UK GAAP) rely on the equivalent "
    "predecessor exemption under FRS 1 ('the Bank is exempt from the requirement to prepare a cash flow statement "
    "on the grounds that a parent undertaking includes the Bank in its own published consolidated financial "
    f"statements') - e.g. Julian Hodge Bank Limited Directors' report and financial statements 2015, p.19 - "
    f"{AR2015_URL}. The same FRS 1 exemption wording is confirmed present in each of the FY2009-FY2013 Directors' "
    "report and financial statements sourced for HD-074 (e.g. FY2010, FY2011, FY2013 reports, each Note 1) - see "
    "HD074_NOTE below. No Statement of Cash Flows exists in any of the entity's published accounts for any year "
    "FY2009-FY2025 - a standing structural feature spanning both the old-UK-GAAP and FRS101 eras, not a one-off or "
    "data gap. Per the project's established policy for this exemption (see The Bank of New York Mellon "
    "(International) Limited / ABC International Bank plc), this workbook is built as a PILLAR-3-ONLY variant: "
    "all 11 Pillar 3 metric sheets are populated below, but no cash flow figures exist to show. See the Overview "
    "sheet for the equivalent treatment there."
)

CASH_FLOW_SOURCES = ENTITY_NOTE + "\n\n" + EXEMPTION_NOTE + "\n\n" + HD074_NOTE

BASIS_NOTE = (
    "FY2021-FY2023: full UK KM1-format 'Key Regulatory Metrics' table from each year's own standalone Pillar 3 "
    "Disclosures document. FY2024-FY2025: no standalone Pillar 3 document was located on the bank's site (financial "
    "information page lists a Pillar 3 disclosure link for FY2018-FY2023 only) - CET1/RWA/ratio figures instead "
    "come from each year's own Annual Report 'Capital risk management (unaudited)' note, which does not include "
    "Leverage Ratio, LCR, or NSFR - those 3 metrics are genuinely unavailable for FY2024/FY2025 this session, not "
    "assumed absent."
)


def p3_sources(extra=""):
    return (
        "Sources - Julian Hodge Bank Limited:\n"
        f"FY2023: Hodge Bank Pillar 3 Disclosures - Period ended 30 September 2023, Table \"3 Key Regulatory "
        f"Metrics\", p.9 - {P3_2023_URL}\n"
        f"FY2022: Hodge Bank Pillar 3 Disclosures - Period ended 30 September 2022, Table \"3 Key Regulatory "
        f"Metrics\", p.12 - {P3_2022_URL}\n"
        f"FY2021: Hodge Bank Pillar 3 Disclosures - Period ended 30 September 2021, Table \"Key Metrics\", p.16 - "
        f"{P3_2021_URL}\n"
        f"FY2020: Julian Hodge Bank Limited Pillar 3 Disclosures - Period ended 30 September 2020, Summary of Key Regulatory Metrics, p.8 - {P3_2020_URL}\n"
        f"FY2019: Julian Hodge Bank Limited Pillar 3 Disclosures - Period ended 31 October 2019, Key Regulatory Metrics, p.10-11 - {P3_2019_URL}\n"
        f"FY2018: Julian Hodge Bank Limited Pillar 3 Disclosures - Period ended 31 October 2018, Key Regulatory Metrics, p.10-11 - {P3_2018_URL}\n"
        f"FY2017: Julian Hodge Bank Limited Pillar 3 Disclosures - Period ended 31 October 2017, Summary of Key Capital Ratios/Capital Resources, p.6/15 - {P3_2017_URL}\n"
        f"FY2016: Julian Hodge Bank Limited Pillar 3 Disclosures - Period ended 31 October 2016, Summary of Key Capital Ratios/Capital Resources, p.6/15 - {P3_2016_URL}\n"
        f"FY2015: Julian Hodge Bank Limited Pillar 3 Disclosures - Period ended 31 October 2015, Capital Resources, p.12-13 - {P3_2015_URL}\n"
        f"FY2014: Julian Hodge Bank Limited Pillar 3 Disclosures - period ended 31 October 2014, Capital Resources, p.12-13 - {P3_2014_URL}\n"
        f"FY2024: Julian Hodge Bank Limited Annual Report 2024, Note 32 'Capital risk management (unaudited)', "
        f"p.73 - {AR2024_URL}\n"
        f"FY2025: Julian Hodge Bank Limited Annual Report 2025, Note 34 'Capital risk management (unaudited)', "
        f"p.76 - {AR2025_URL}\n"
        + (extra + "\n" if extra else "") + BASIS_NOTE
    )


bw = BankWorkbook(bank_name="Julian Hodge Bank Limited", years=YEARS, year_label=YEAR_LABEL, header_color="8B4513")

STATEMENTS_SOURCES = (
    "Sources - Julian Hodge Bank Limited Annual Reports:\n"
    f"FY2025: Annual Report 2025, Balance Sheet/Income Statement/Statement of Changes in Equity, p.40-41, "
    f"Note 12 'Loans and advances to customers'/Note 13 'Impairment provisions', p.49-50 - {AR2025_URL}\n"
    f"FY2024: Annual Report 2024, Balance Sheet/Income Statement/Statement of Changes in Equity, p.40-42, "
    f"Note 12/13, p.48-49 - {AR2024_URL}\n"
    f"FY2023: Annual Report 2023, Balance Sheet/Income Statement/Statement of Changes in Equity, p.40-42, "
    f"Note 13/14, p.49-50 - {AR2023_URL}\n"
    f"FY2022: Annual Report 2022, Balance Sheet/Income Statement/Statement of Changes in Equity, p.37-39, "
    f"Note 13/14, p.46-47 - {AR2022_URL}\n"
    f"FY2021: Annual Report 2021, Balance Sheet/Income Statement/Statement of Other Comprehensive Income/"
    f"Statement of Changes in Equity, p.62-65 (printed pages 67-70) - {AR2021_URL}\n"
    f"FY2020: Julian Hodge Bank Limited Annual Report (11-month period ended 30 September 2020), Income "
    f"Statement/Balance Sheet/Statement of Changes in Equity p.26-28, Note 14 'Impairment provisions', p.44-45 - "
    f"{AR2020_URL}\n"
    f"FY2019: Julian Hodge Bank Limited Annual Report and Financial Statements 2019 (Master FINAL EY Signed), "
    f"Income Statement/Balance Sheet/Statement of Changes in Equity p.20-23, Note 15 'Impairment provisions', "
    f"p.42-43 - {AR2019_URL}\n"
    f"FY2018: Julian Hodge Bank Limited Annual Report and Financial Statements 2018, Income Statement/Balance "
    f"Sheet/Statement of Changes in Equity p.24-26, Note 16 'Loans and advances to customers', p.42-44 - "
    f"{AR2018_URL} (cross-checked against the Companies House filing for the period made up to 31 October 2018)\n"
    f"FY2017: Julian Hodge Bank Limited Annual report and financial statements 2017, Income Statement/Balance "
    f"Sheet/Statement of Changes in Equity p.24-26, Note 16 'Loans and advances to customers', p.42-43 - "
    f"{AR2017_URL}\n"
    f"FY2016: Julian Hodge Bank Limited Financial Statements 2016 (FRS 101, first year of transition from UK "
    f"GAAP), Income Statement/Balance Sheet/Statement of Changes in Equity p.16-19, Note 16 'Loans and advances "
    f"to customers', p.34 - {AR2016_URL}\n"
    f"FY2015: Julian Hodge Bank Limited Directors' report and financial statements 2015 (UK GAAP), Profit and "
    f"loss account/Balance sheet p.13-15, Note 22 'reconciliation of movements in shareholder's funds', p.28, "
    f"Note 12 'Provisions for bad and doubtful debts', p.24 - {AR2015_URL}\n"
    f"FY2014: Julian Hodge Bank Limited Directors' report and financial statements 2014 (UK GAAP), Profit and "
    f"loss account/Balance sheet p.14-16, Note 12 'Provisions for bad and doubtful debts', p.24 - {AR2014_URL}\n\n"
    + ENTITY_NOTE + "\n\n"
    "HISTORICAL-DEPTH NOTE (HD-049): FY2016 is this entity's first year of FRS 101 reporting (transitioning from "
    "old UK GAAP used in FY2014-FY2015) - its own report's FY2015 comparative column is FRS101-restated and does "
    "NOT tie to FY2015's own contemporaneous UK GAAP report (e.g. FY2015 closing shareholder's funds/equity: "
    "GBP133.7m as originally reported in the FY2015 Annual Report vs GBP133.3m as restated in the FY2016 Annual "
    "Report's FY2015 comparative - a real GAAP-transition adjustment, not a transcription error). Per this "
    "project's convention, each year's own originally-published figures are used throughout (FY2014/FY2015 in "
    "UK GAAP format; FY2016 onward in FRS101 format), so the equity ladder has one genuine, documented break at "
    "the FY2015/FY2016 boundary rather than a forced tie-out. Separately, FY2017's own report restates FY2016's "
    "shareholder's funds from GBP146.3m (as FY2016's own report showed) to GBP153.5m, citing a 'prior period "
    "error' corrected in Note 36 (GBP6.8m addition to opening retained earnings, GBP0.3m to FY2016's own profit) - "
    "again, FY2016's own originally-published figures are used here, with this restatement documented rather than "
    "applied. IFRS 9 was adopted 1 November 2018 (start of FY2019), so IFRS 9 Stage 1/2/3 impairment staging "
    "exists only from FY2019 onward; FY2014-FY2018 show only the (unstaged) IAS 39/UK GAAP total impairment "
    "provision. FY2014-FY2015 Income Statement rows follow the old UK GAAP layout (interest receivable/payable, "
    "fees, 'other operating income' components including reversionary interest/stock profits, then a single "
    "'profit on ordinary activities before taxation' line) rather than the FRS101 Net interest income / Net "
    "operating income / Operating profit structure used FY2016 onward - both shown on their own basis, not forced "
    "into one template, consistent with how this same script already treats the FY2025 structural change."
)

# ---------------------------------------------------------------
# Balance Sheet
# ---------------------------------------------------------------
bs_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and balances held at central banks", {"FY2025": 69.5, "FY2024": 151.3, "FY2023": 93.7, "FY2022": 118.1, "FY2021": 412.2, "FY2020": 147.9, "FY2019": 321.9, "FY2018": 153.2, "FY2017": 87.0, "FY2016": 168.0, "FY2015": 101.6, "FY2014": 18.5, "FY2013": 35.6, "FY2012": 37.0}),
    ("DATA", "Loans and advances to credit institutions", {"FY2025": 7.9, "FY2024": 4.5, "FY2023": 11.2, "FY2022": 0.2, "FY2021": 45.9, "FY2020": 105.2, "FY2019": 86.1, "FY2018": 96.2, "FY2017": 107.6, "FY2016": 128.3, "FY2015": 20.5, "FY2014": 28.8, "FY2013": 25.6, "FY2012": 90.6, "FY2011": 78.4, "FY2010": 188.5, "FY2009": 91.8}),
    ("DATA", "Derivative financial instruments (asset)", {"FY2025": 16.8, "FY2024": 27.9, "FY2023": 58.5, "FY2022": 75.8}),
    ("DATA", "Government bonds (called 'Treasury bills' in FY2009-FY2019 reports)", {"FY2025": 27.9, "FY2024": 27.7, "FY2023": 61.7, "FY2022": 111.2, "FY2021": 29.8, "FY2020": 48.6, "FY2019": 25.1, "FY2018": 81.2, "FY2017": 87.3, "FY2016": 84.7, "FY2015": 81.0, "FY2014": 75.5, "FY2013": 78.1, "FY2012": 81.3, "FY2011": 35.3, "FY2010": 42.5, "FY2009": 17.9}),
    ("DATA", "Debt securities", {"FY2025": 135.8, "FY2024": 70.7, "FY2023": 82.0, "FY2022": 116.2, "FY2021": 42.3, "FY2020": 50.7, "FY2019": 57.0, "FY2018": 87.5, "FY2017": 77.0, "FY2016": 89.1, "FY2015": 81.5, "FY2014": 85.1, "FY2013": 87.6, "FY2012": 89.5, "FY2011": 67.4, "FY2010": 54.2, "FY2009": 31.6}),
    ("DATA", "Loans and advances to customers", {"FY2025": 1839.7, "FY2024": 1699.3, "FY2023": 1488.5, "FY2022": 1404.6, "FY2021": 1061.5, "FY2020": 930.8, "FY2019": 766.9, "FY2018": 827.9, "FY2017": 757.9, "FY2016": 706.9, "FY2015": 557.5, "FY2014": 440.8, "FY2013": 384.0, "FY2012": 358.8, "FY2011": 362.8, "FY2010": 398.4, "FY2009": 470.2}),
    ("DATA", "Shares in group undertakings and participating interests (Hodge Life Assurance Company - sold/reclassified out by FY2018)", {"FY2017": 16.0, "FY2016": 16.0, "FY2015": 16.0, "FY2014": 16.0, "FY2013": 16.0, "FY2012": 16.1, "FY2011": 16.1, "FY2010": 16.1, "FY2009": 16.1}),
    ("DATA", "Equity shares (a small distinct holding, genuinely nil/absent in some years - not a residual)", {"FY2012": 0.8, "FY2011": 0.8, "FY2010": 0.4, "FY2009": 0.4}),
    ("DATA", "Stock and work in progress (UK GAAP line, folded into other line items after the FY2016 FRS101 transition)", {"FY2015": 3.4, "FY2014": 3.2, "FY2013": 4.5, "FY2012": 5.2}),
    ("DATA", "Reversionary interests in properties (UK GAAP line, folded into Investment properties after the FY2016 FRS101 transition)", {"FY2015": 55.0, "FY2014": 57.4, "FY2013": 59.4, "FY2012": 61.2, "FY2011": 62.6, "FY2010": 63.3, "FY2009": 57.3}),
    ("DATA", "Intangible assets", {"FY2025": 14.5, "FY2024": 15.1, "FY2023": 12.7, "FY2022": 9.7, "FY2021": 7.4, "FY2020": 7.3, "FY2019": 5.8, "FY2018": 3.1, "FY2017": 1.7, "FY2016": 1.2}),
    ("DATA", "Property and equipment", {"FY2025": 0.6, "FY2024": 1.0, "FY2023": 1.2, "FY2022": 1.5, "FY2021": 1.6, "FY2020": 1.9, "FY2019": 1.9, "FY2018": 2.2, "FY2017": 2.0, "FY2016": 2.1, "FY2015": 1.3, "FY2014": 0.6, "FY2013": 0.1, "FY2012": 0.1, "FY2011": 0.0, "FY2010": 0.0, "FY2009": 0.1}),
    ("DATA", "Investment properties", {"FY2025": 0.2, "FY2024": 1.5, "FY2023": 2.6, "FY2022": 9.2, "FY2021": 94.6, "FY2020": 97.4, "FY2019": 97.3, "FY2018": 100.3, "FY2017": 118.6, "FY2016": 107.8, "FY2015": 7.7, "FY2014": 9.2, "FY2013": 8.9, "FY2012": 8.9, "FY2011": 9.3, "FY2010": 10.3, "FY2009": 10.3}),
    ("DATA", "Deferred tax assets", {"FY2025": 2.2, "FY2024": 3.7, "FY2023": 5.6, "FY2022": 6.3, "FY2021": 11.5, "FY2020": 9.5, "FY2019": 6.6, "FY2018": 6.5, "FY2017": 7.3, "FY2016": 8.3}),
    ("DATA", "Other assets (includes prepayments/accrued income in FY2009-FY2015)", {"FY2025": 6.6, "FY2024": 5.9, "FY2023": 5.4, "FY2022": 8.0, "FY2021": 6.6, "FY2020": 9.9, "FY2019": 10.1, "FY2018": 5.3, "FY2017": 5.0, "FY2016": 4.4, "FY2015": 73.5, "FY2014": 49.7, "FY2013": 26.7, "FY2012": 53.0, "FY2011": 78.2, "FY2010": 51.7, "FY2009": 42.4}),
    ("DATA", "Pension asset", {"FY2025": 0.9, "FY2024": 0.2}),
    ("TOTAL", "Total assets", {"FY2025": 2122.6, "FY2024": 2008.8, "FY2023": 1823.1, "FY2022": 1860.8, "FY2021": 1713.4, "FY2020": 1409.2, "FY2019": 1378.7, "FY2018": 1363.4, "FY2017": 1267.4, "FY2016": 1316.8, "FY2015": 999.0, "FY2014": 784.7, "FY2013": 726.5, "FY2012": 802.5, "FY2011": 710.9, "FY2010": 825.3, "FY2009": 738.0}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Deposits from banks (called 'amounts owed to credit institutions and central banks' in FY2014-FY2015)", {"FY2025": 67.0, "FY2024": 167.7, "FY2023": 240.7, "FY2022": 221.0, "FY2021": 145.0, "FY2020": 87.5, "FY2019": 72.5, "FY2018": 72.5, "FY2017": 2.8, "FY2016": 2.8, "FY2015": 2.8, "FY2014": 10.0, "FY2013": 5.0, "FY2012": 8.9, "FY2011": 1.1, "FY2010": 0.5}),
    ("DATA", "Deposits from customers (called 'customer accounts' in FY2014-FY2015)", {"FY2025": 1860.3, "FY2024": 1639.4, "FY2023": 1368.1, "FY2022": 1425.0, "FY2021": 1381.0, "FY2020": 1071.4, "FY2019": 1042.8, "FY2018": 994.6, "FY2017": 947.7, "FY2016": 991.7, "FY2015": 848.6, "FY2014": 633.2, "FY2013": 583.6, "FY2012": 658.9, "FY2011": 579.6, "FY2010": 696.2, "FY2009": 610.5}),
    ("DATA", "Derivative financial instruments (liability)", {"FY2025": 5.1, "FY2024": 5.6, "FY2023": 9.7, "FY2022": 11.4, "FY2021": 14.7, "FY2020": 82.0, "FY2019": 80.4, "FY2018": 107.8, "FY2017": 131.1, "FY2016": 150.6}),
    ("DATA", "Other liabilities (includes accruals/deferred income and other provisions in FY2009-FY2020)", {"FY2025": 10.4, "FY2024": 12.9, "FY2023": 16.5, "FY2022": 13.9, "FY2021": 9.9, "FY2020": 6.3, "FY2019": 6.1, "FY2018": 4.0, "FY2017": 5.5, "FY2016": 11.9, "FY2015": 10.3, "FY2014": 6.6, "FY2013": 7.5, "FY2012": 7.7, "FY2011": 4.9, "FY2010": 4.3, "FY2009": 4.5}),
    ("DATA", "Pension liabilities", {"FY2023": 4.3, "FY2022": 4.5, "FY2021": 14.2, "FY2020": 21.0, "FY2019": 16.6, "FY2018": 12.8, "FY2017": 13.0, "FY2016": 13.5, "FY2015": 3.6, "FY2014": 2.9, "FY2013": 2.2, "FY2012": 1.4, "FY2011": 0.6, "FY2010": 0.1, "FY2009": 0.9}),
    ("TOTAL", "Total liabilities", {"FY2025": 1942.8, "FY2024": 1825.6, "FY2023": 1639.3, "FY2022": 1675.8, "FY2021": 1564.8, "FY2020": 1268.2, "FY2019": 1218.4, "FY2018": 1191.7, "FY2017": 1100.1, "FY2016": 1170.5, "FY2015": 865.3, "FY2014": 652.7, "FY2013": 598.3, "FY2012": 676.9, "FY2011": 586.2, "FY2010": 701.1, "FY2009": 615.9}),
    ("SECTION", "Equity", {}),
    ("DATA", "Called up share capital", {"FY2025": 130.0, "FY2024": 130.0, "FY2023": 130.0, "FY2022": 130.0, "FY2021": 105.0, "FY2020": 105.0, "FY2019": 105.0, "FY2018": 105.0, "FY2017": 105.0, "FY2016": 100.0, "FY2015": 100.0, "FY2014": 100.0, "FY2013": 100.0, "FY2012": 100.0, "FY2011": 100.0, "FY2010": 100.0, "FY2009": 100.0}),
    ("DATA", "Other reserves (retained earnings + pension reserve; profit and loss account + revaluation reserve in FY2009-FY2015 UK GAAP)", {"FY2025": 49.8, "FY2024": 53.2, "FY2023": 53.8, "FY2022": 55.0, "FY2021": 43.6, "FY2020": 36.0, "FY2019": 55.3, "FY2018": 66.7, "FY2017": 62.3, "FY2016": 46.3, "FY2015": 33.7, "FY2014": 32.0, "FY2013": 28.2, "FY2012": 25.6, "FY2011": 24.7, "FY2010": 24.1, "FY2009": 22.1}),
    ("TOTAL", "Total equity", {"FY2025": 179.8, "FY2024": 183.2, "FY2023": 183.8, "FY2022": 185.0, "FY2021": 148.6, "FY2020": 141.0, "FY2019": 160.3, "FY2018": 171.7, "FY2017": 167.3, "FY2016": 146.3, "FY2015": 133.7, "FY2014": 132.0, "FY2013": 128.2, "FY2012": 125.6, "FY2011": 124.7, "FY2010": 124.1, "FY2009": 122.1}),
    ("TOTAL", "Total equity and liabilities", {"FY2025": 2122.6, "FY2024": 2008.8, "FY2023": 1823.1, "FY2022": 1860.8, "FY2021": 1713.4, "FY2020": 1409.2, "FY2019": 1378.7, "FY2018": 1363.4, "FY2017": 1267.4, "FY2016": 1316.8, "FY2015": 999.0, "FY2014": 784.7, "FY2013": 726.5, "FY2012": 802.5, "FY2011": 710.9, "FY2010": 825.3, "FY2009": 738.0}),
]

bw.add_balance_sheet_sheet(
    title="Julian Hodge Bank Limited — Balance Sheet",
    subtitle="Entity-level (Company-only, FRS 101). £m.",
    rows=bs_rows,
    sources_text=STATEMENTS_SOURCES + "\n\n" + HD074_NOTE,
    first_col_width=64,
    source_height=280,
    unit_suffix=" (£m)",
)

# ---------------------------------------------------------------
# Profit & Loss
# ---------------------------------------------------------------
pl_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest revenue calculated using the EIR method (FY2014-FY2015: UK GAAP interest receivable, not EIR-method - same row for comparability, see note)",
     {"FY2025": 122.9, "FY2024": 92.1, "FY2023": 67.3, "FY2022": 50.5, "FY2021": 39.6, "FY2020": 38.4, "FY2019": 48.3, "FY2018": 46.0, "FY2017": 41.3, "FY2016": 42.2, "FY2015": 33.3, "FY2014": 28.9,
      "FY2013": 27.5, "FY2012": 26.9, "FY2011": 28.4, "FY2010": 33.5, "FY2009": 32.6}),
    ("DATA", "Interest expense calculated using the EIR method (FY2014-FY2015: UK GAAP interest payable)",
     {"FY2025": -81.1, "FY2024": -52.4, "FY2023": -27.9, "FY2022": -21.1, "FY2021": -22.0, "FY2020": -22.8, "FY2019": -28.1, "FY2018": -27.7, "FY2017": -27.4, "FY2016": -29.0, "FY2015": -27.7, "FY2014": -26.0,
      "FY2013": -29.4, "FY2012": -28.7, "FY2011": -28.3, "FY2010": -31.0, "FY2009": -25.3}),
    ("TOTAL", "Net interest income", {"FY2025": 41.8, "FY2024": 39.7, "FY2023": 39.4, "FY2022": 29.4, "FY2021": 17.6, "FY2020": 15.6, "FY2019": 20.2, "FY2018": 18.3, "FY2017": 13.9, "FY2016": 13.2, "FY2015": 5.6, "FY2014": 2.9,
      "FY2013": -1.9, "FY2012": -1.8, "FY2011": 0.2, "FY2010": 2.4, "FY2009": 7.4}),
    ("DATA", "Fees and commission income", {"FY2025": 1.0, "FY2024": 2.9, "FY2023": 2.5, "FY2022": 2.6, "FY2021": 2.5, "FY2020": 1.8, "FY2019": 0.7, "FY2018": 2.5, "FY2017": 0.5, "FY2016": 1.1, "FY2015": 2.8, "FY2014": 2.2,
      "FY2013": 1.1, "FY2012": 1.2, "FY2011": 1.3, "FY2010": 1.6, "FY2009": 2.6}),
    ("DATA", "Fees and commission expense", {"FY2025": -3.6, "FY2024": -1.2, "FY2023": -0.1, "FY2022": -0.1, "FY2019": -0.1, "FY2018": -1.1, "FY2017": -1.2, "FY2016": -0.7, "FY2015": -0.8, "FY2014": -1.5,
      "FY2013": -0.3, "FY2011": -0.1, "FY2010": -0.4, "FY2009": -1.0}),
    ("TOTAL", "Net fee and commission income/(expense)", {"FY2025": -2.6, "FY2024": 1.7, "FY2023": 2.4, "FY2022": 2.5, "FY2021": 2.5, "FY2020": 1.8, "FY2019": 0.6, "FY2018": 1.4, "FY2017": -0.7, "FY2016": 0.4, "FY2015": 2.0, "FY2014": 0.7,
      "FY2013": 0.8, "FY2012": 1.2, "FY2011": 1.3, "FY2010": 1.2, "FY2009": 1.6}),
    ("DATA", "Investment income (FY2014-FY2015: 'Other finance income')", {"FY2025": 0.6, "FY2024": 0.5, "FY2023": 4.6, "FY2022": 6.7, "FY2021": 6.0, "FY2020": 3.5, "FY2019": 7.2, "FY2018": 6.4, "FY2017": 4.8, "FY2015": 0.4, "FY2014": 0.8,
      "FY2013": 0.3, "FY2012": 0.4, "FY2011": -0.1, "FY2010": 0.1, "FY2009": 0.2}),
    ("DATA", "Dividend income from listed equity shares and subsidiary companies (FY2009-FY2013 only)",
     {"FY2012": 0.2, "FY2011": 0.2, "FY2010": 0.1, "FY2009": 0.4}),
    ("DATA", "Other operating income", {"FY2023": 0.2, "FY2021": 0.1, "FY2018": 0.1, "FY2017": 1.0, "FY2016": 0.8, "FY2015": 5.0, "FY2014": 4.9,
      "FY2013": 9.0, "FY2012": 8.2, "FY2011": 7.5, "FY2010": 12.2, "FY2009": 3.4}),
    ("DATA", "Bad debt recovery", {"FY2022": 0.4}),
    ("TOTAL", "Net operating income", {"FY2025": 39.8, "FY2024": 41.9, "FY2023": 46.6, "FY2022": 38.6, "FY2021": 26.2, "FY2020": 20.9, "FY2019": 28.0, "FY2018": 18.2, "FY2017": 19.3, "FY2016": 33.5, "FY2015": 13.0, "FY2014": 9.3,
      "FY2013": 8.2, "FY2012": 8.1, "FY2011": 9.0, "FY2010": 16.1, "FY2009": 13.0}),
    ("DATA", "Administrative expenses", {"FY2025": -33.7, "FY2024": -36.4, "FY2023": -35.3, "FY2022": -34.2, "FY2021": -25.9, "FY2020": -22.3, "FY2019": -16.4, "FY2018": -12.0, "FY2017": -9.9, "FY2016": -8.1, "FY2015": -6.7, "FY2014": -5.4,
      "FY2013": -4.5, "FY2012": -4.9, "FY2011": -4.9, "FY2010": -5.7, "FY2009": -7.5}),
    ("DATA", "Depreciation and amortisation", {"FY2025": -3.1, "FY2024": -2.9, "FY2023": -2.9, "FY2022": -2.5, "FY2021": -2.4, "FY2020": -1.8, "FY2019": -1.2, "FY2018": -0.9, "FY2017": -0.5, "FY2016": -0.2,
      "FY2013": 0.0, "FY2012": 0.0, "FY2011": 0.0, "FY2010": 0.0, "FY2009": -0.2}),
    ("DATA", "Impairment (losses)/gains on loans and advances to customers", {"FY2025": -6.5, "FY2024": -2.2, "FY2023": -1.6, "FY2020": -5.4, "FY2019": -3.9, "FY2018": 1.0, "FY2017": 1.6, "FY2016": -2.4, "FY2015": -2.1, "FY2014": -0.7,
      "FY2013": -0.1, "FY2012": 0.8, "FY2011": -1.5, "FY2010": -8.2, "FY2009": -4.2}),
    ("DATA", "Movement in valuation of stock/work-in-progress (UK GAAP line, FY2009-FY2015 only)", {"FY2015": 0.9, "FY2014": 1.1, "FY2013": -0.1, "FY2012": -0.9}),
    ("TOTAL", "Operating profit/(loss) (FY2021-FY2024 subtotal; see Net operating (loss)/income for FY2025's own equivalent line)",
     {"FY2024": 0.4, "FY2023": 6.8, "FY2022": 2.3, "FY2021": -2.1, "FY2020": -8.6, "FY2019": 6.5}),
    ("TOTAL", "Net operating (loss)/income (FY2025's own subtotal, structured differently from FY2021-FY2024's 'Operating profit')",
     {"FY2025": -3.5}),
    ("DATA", "(Loss)/gain arising from the derecognition of financial assets managed at amortised cost", {"FY2024": -1.0, "FY2021": 0.0, "FY2020": 4.2, "FY2019": 3.1}),
    ("DATA", "Other fair value gains/(losses)", {"FY2025": -2.3, "FY2024": -1.5, "FY2023": -7.0, "FY2022": 4.3, "FY2021": 11.3, "FY2020": -16.7, "FY2019": -12.8, "FY2018": -8.0, "FY2017": 0.3, "FY2016": 19.2}),
    ("DATA", "Loss on disposal of loans and advances to customers held at fair value", {"FY2021": -5.5, "FY2019": -4.6}),
    ("TOTAL", "Profit/(loss) before taxation (FY2014-FY2015: 'Profit on ordinary activities before taxation')",
     {"FY2025": -5.8, "FY2024": -2.1, "FY2023": -0.2, "FY2022": 6.6, "FY2021": 3.7, "FY2020": -21.1, "FY2019": -7.8, "FY2018": 6.3, "FY2017": 10.5, "FY2016": 22.8, "FY2015": 5.0, "FY2014": 4.3,
      "FY2013": 3.5, "FY2012": 3.1, "FY2011": 2.6, "FY2010": 2.1, "FY2009": 1.2}),
    ("DATA", "Tax credit/(charge) on profit/(loss) before taxation", {"FY2025": 1.9, "FY2024": 0.4, "FY2022": -1.8, "FY2021": 2.1, "FY2020": 5.2, "FY2019": 2.1, "FY2018": -0.8, "FY2017": -0.3, "FY2016": -5.2, "FY2015": -0.8, "FY2014": -0.2,
      "FY2013": 0.1, "FY2012": -0.5, "FY2011": -0.6, "FY2010": -0.8, "FY2009": -0.4}),
    ("TOTAL", "Profit/(loss) for the financial year", {"FY2025": -3.9, "FY2024": -1.7, "FY2023": -0.2, "FY2022": 4.8, "FY2021": 5.8, "FY2020": -15.9, "FY2019": -5.7, "FY2018": 5.5, "FY2017": 10.2, "FY2016": 17.6, "FY2015": 4.3, "FY2014": 4.1,
      "FY2013": 3.5, "FY2012": 2.6, "FY2011": 2.0, "FY2010": 1.3, "FY2009": 0.7}),
    ("SECTION", "Other comprehensive income", {}),
    ("DATA", "Re-measurement of defined benefit pension plan (FY2014-FY2015: 'Actuarial loss recognised in the pension scheme')",
     {"FY2025": 0.7, "FY2024": 1.7, "FY2023": -1.7, "FY2022": 9.0, "FY2021": 2.6, "FY2020": -4.4, "FY2019": -3.3, "FY2018": 0.6, "FY2017": 0.4, "FY2016": -9.1, "FY2015": -1.1, "FY2014": -1.4,
      "FY2013": -1.2, "FY2012": -1.4, "FY2011": -0.5, "FY2010": 0.7, "FY2009": -2.8}),
    ("DATA", "Deferred tax on pension plan re-measurement", {"FY2025": -0.2, "FY2024": -0.4, "FY2023": 0.4, "FY2022": -2.2, "FY2021": -0.4, "FY2020": 0.7, "FY2019": 0.6, "FY2018": -0.1, "FY2017": -0.1, "FY2016": 1.5,
      "FY2013": 0.2, "FY2012": 0.2, "FY2011": 0.1}),
    ("DATA", "Deficit on revaluation of investment properties (FY2011-FY2012 only)", {"FY2012": -0.4, "FY2011": -1.0}),
    ("DATA", "Movement of pension scheme reimbursement asset/(liability) (FY2014-FY2015: net of deferred tax)",
     {"FY2024": -0.3, "FY2023": 0.4, "FY2022": -0.2, "FY2021": -1.0, "FY2020": 0.4, "FY2019": 0.5, "FY2018": -0.1, "FY2017": -0.9, "FY2016": 2.3, "FY2015": 0.1, "FY2014": 0.7}),
    ("DATA", "Deferred tax on pension reimbursement movement", {"FY2024": 0.1, "FY2023": -0.1, "FY2021": 0.6, "FY2020": -0.1, "FY2019": -0.1, "FY2017": 0.1, "FY2016": -0.4}),
    ("DATA", "Fair value movements on available-for-sale investments (AFS reserve; discontinued after IFRS 9 replaced it FY2019)",
     {"FY2018": -1.8, "FY2017": -0.1, "FY2016": 1.1}),
    ("DATA", "Deferred tax on available-for-sale fair value movements", {"FY2018": 0.3, "FY2017": -0.8}),
    ("DATA", "Revaluation of investment properties (UK GAAP line, FY2014-FY2015 only, net of deferred tax)", {"FY2015": -1.5, "FY2014": 0.3}),
    ("TOTAL", "Total other comprehensive income/(loss)", {"FY2025": 0.5, "FY2024": 1.1, "FY2023": -1.0, "FY2022": 6.6, "FY2021": 1.8, "FY2020": -3.4, "FY2019": -2.3, "FY2018": -1.1, "FY2017": -1.4, "FY2016": -4.6, "FY2015": -2.5, "FY2014": -0.3,
      "FY2013": -1.0, "FY2012": -1.6, "FY2011": -1.4, "FY2010": 0.7, "FY2009": -2.8}),
    ("TOTAL", "Total comprehensive (loss)/income for the year", {"FY2025": -3.4, "FY2024": -0.6, "FY2023": -1.2, "FY2022": 11.4, "FY2021": 7.6, "FY2020": -19.3, "FY2019": -8.0, "FY2018": 4.4, "FY2017": 8.8, "FY2016": 13.0, "FY2015": 1.8, "FY2014": 3.8,
      "FY2013": 2.6, "FY2012": 1.0, "FY2011": 0.5, "FY2010": 2.0, "FY2009": -2.1}),
]

bw.add_income_statement_sheet(
    title="Julian Hodge Bank Limited — Profit & Loss",
    subtitle="Entity-level (Company-only, FRS 101). £m. Structure genuinely changes FY2025 (Net operating (loss)/income "
              "subtotal replaces the FY2021-FY2024 'Operating profit' subtotal) - both shown on their own basis, not forced "
              "into one template. Each year's own originally-published figures used throughout; note AR2025's own FY2024 "
              "comparative column is separately labelled 'Restated' (Note 33 interest revenue/expense reclassification) - "
              "that restated column is NOT used here, FY2024's own contemporaneous report is used instead, per project convention.",
    rows=pl_rows,
    sources_text=STATEMENTS_SOURCES + "\n\n" + HD074_NOTE,
    first_col_width=90,
    source_height=280,
    unit_suffix=" (£m)",
)

# ---------------------------------------------------------------
# Statement of Changes in Equity - per-year reconciliation ladder. FY2021-FY2025 confirmed: every year's own
# closing balance ties exactly to both the next year's own opening balance and that year's own Balance Sheet
# Total equity - zero plug rows needed. FY2014-FY2020 (HD-049 extension) also ties exactly year-to-year once the
# "Other reserves" column is read as: Revaluation reserve (FY2014-FY2015, UK GAAP) -> Available-for-sale reserve
# + Pension reserve combined (FY2016-FY2019, FRS101/IAS 39) -> Pension reserve only (FY2020 onward, post-IFRS 9 -
# the AFS reserve was extinguished on IFRS 9 adoption 1 November 2018). One genuine, documented break exists at
# the FY2016/FY2017 boundary: FY2016's own Annual Report reported its own closing equity at GBP146.3m, but
# FY2017's Annual Report (Note 36) restates FY2016's opening/closing position for a "prior period error"
# (+GBP7.2m, entirely in retained earnings) - both the originally-published FY2016 closing balance and the
# subsequent restatement are shown explicitly below, rather than silently using one or the other.
# ---------------------------------------------------------------
equity_headers = ["Called up share capital", "Retained earnings", "Other reserves (see sheet note)", "Total"]
equity_rows = [
    ("TOTAL", "Opening balance at 1 November 2009 (FY2010 opening, per the FY2010 Annual Report; FY2009's own "
     "1 November 2008 opening and component movement are not available from the sourced documents - see HD074_NOTE - "
     "so the ladder begins here, one year later than the Balance Sheet/P&L sheets)", (100.0, 22.1, None, 122.1)),
    ("DATA", "Profit for the financial year", (None, 1.3, None, 1.3)),
    ("TOTAL", "At 31 October 2010 (FY2010 closing)", (100.0, 24.1, None, 124.1)),
    ("DATA", "Profit for the financial year", (None, 2.0, None, 2.0)),
    ("DATA", "Deficit on revaluation of investment properties", (None, None, -1.0, -1.0)),
    ("DATA", "Actuarial loss recognised in the pension scheme (net of deferred tax)", (None, -0.4, None, -0.4)),
    ("TOTAL", "At 31 October 2011 (FY2011 closing)", (100.0, 25.7, -1.0, 124.7)),
    ("DATA", "Profit for the financial year", (None, 2.6, None, 2.6)),
    ("DATA", "Deficit on revaluation of investment properties", (None, None, -0.4, -0.4)),
    ("DATA", "Actuarial loss recognised in the pension scheme (net of deferred tax)", (None, -1.2, None, -1.2)),
    ("TOTAL", "At 31 October 2012 (FY2012 closing, per the FY2013 Annual Report's own comparative - see HD074_NOTE "
     "on the FY2012 standalone-document gap)", (100.0, 27.1, -1.4, 125.6)),
    ("DATA", "Profit for the financial year", (None, 3.5, None, 3.5)),
    ("DATA", "Actuarial loss recognised in the pension scheme (net of deferred tax)", (None, -1.0, None, -1.0)),
    ("TOTAL", "Opening balance at 1 November 2013 (FY2014 opening)", (100.0, 29.7, -1.4, 128.2)),
    ("DATA", "Profit for the financial year", (None, 4.1, None, 4.1)),
    ("DATA", "Actuarial loss recognised in the pension scheme (net of deferred tax)", (None, -1.4, None, -1.4)),
    ("DATA", "Recognition of pension scheme reimbursement asset (net of deferred tax)", (None, 0.7, None, 0.7)),
    ("DATA", "Revaluation of investment properties", (None, None, 0.3, 0.3)),
    ("TOTAL", "At 31 October 2014 (FY2014 closing)", (100.0, 33.1, -1.1, 132.0)),
    ("DATA", "Profit for the financial year", (None, 4.3, None, 4.3)),
    ("DATA", "Actuarial loss recognised in the pension scheme (net of deferred tax)", (None, -1.1, None, -1.1)),
    ("DATA", "Recognition of pension scheme reimbursement asset (net of deferred tax)", (None, 0.1, None, 0.1)),
    ("DATA", "Revaluation of investment properties", (None, None, -1.5, -1.5)),
    ("TOTAL", "At 31 October 2015 (FY2015 closing)", (100.0, 36.4, -2.6, 133.7)),
    ("DATA", "Profit for the financial year", (None, 17.6, None, 17.6)),
    ("DATA", "Other comprehensive income (AFS + pension, FRS101 first-year transition)", (None, None, -4.6, -4.6)),
    ("TOTAL", "At 31 October 2016 (FY2016 closing, as originally reported in the FY2016 Annual Report)", (100.0, 49.4, -3.1, 146.3)),
    ("DATA", "Prior period error restatement (FY2017 Annual Report, Note 36 - not reflected in FY2016's own original report)",
     (None, 7.2, None, 7.2)),
    ("TOTAL", "At 31 October 2016 (restated, per the FY2017 Annual Report's own comparative)", (100.0, 56.6, -3.1, 153.5)),
    ("DATA", "Profit for the financial year", (None, 10.2, None, 10.2)),
    ("DATA", "Other comprehensive income (AFS + pension)", (None, None, -1.4, -1.4)),
    ("DATA", "Issue of share capital", (5.0, None, None, 5.0)),
    ("TOTAL", "At 31 October 2017 (FY2017 closing)", (105.0, 66.8, -4.5, 167.3)),
    ("DATA", "Profit for the financial year", (None, 5.9, -0.4, 5.5)),
    ("DATA", "Other comprehensive income (AFS + pension)", (None, None, -1.1, -1.1)),
    ("TOTAL", "At 31 October 2018 (FY2018 closing)", (105.0, 72.7, -6.0, 171.7)),
    ("DATA", "Impact of adoption of IFRS 9 (extinguishes the AFS reserve)", (None, -0.7, -2.7, -3.4)),
    ("DATA", "Loss for the financial year", (None, -5.3, -0.4, -5.7)),
    ("DATA", "Other comprehensive income (pension only - AFS reserve extinguished)", (None, None, -2.3, -2.3)),
    ("TOTAL", "At 31 October 2019 (FY2019 closing)", (105.0, 66.7, -11.4, 160.3)),
    ("DATA", "Loss for the financial year", (None, -16.3, 0.4, -15.9)),
    ("DATA", "Other comprehensive income", (None, None, -3.4, -3.4)),
    ("TOTAL", "At 30 September 2020 (FY2020 closing - 11-month transition period; opening balance below = FY2021 opening)",
     (105.0, 50.4, -14.4, 141.0)),
    ("TOTAL", "Opening balance at 1 October 2020 (FY2021 opening)", (105.0, 50.4, -14.4, 141.0)),
    ("DATA", "Profit for the financial year", (None, 5.5, 0.3, 5.8)),
    ("DATA", "Other comprehensive income", (None, None, 1.8, 1.8)),
    ("TOTAL", "At 30 September 2021 (FY2021 closing)", (105.0, 54.3, -10.7, 148.6)),
    ("DATA", "Issue of share capital", (25.0, None, None, 25.0)),
    ("DATA", "Profit for the financial year", (None, 5.2, -0.4, 4.8)),
    ("DATA", "Other comprehensive income", (None, None, 6.6, 6.6)),
    ("DATA", "Pension additional contribution", (None, -1.2, 1.2, None)),
    ("TOTAL", "At 30 September 2022 (FY2022 closing)", (130.0, 58.3, -3.3, 185.0)),
    ("DATA", "Loss for the financial year", (None, 0.1, -0.3, -0.2)),
    ("DATA", "Other comprehensive loss", (None, None, -1.0, -1.0)),
    ("DATA", "Pension additional contribution", (None, -1.8, 1.8, None)),
    ("TOTAL", "At 30 September 2023 (FY2023 closing)", (130.0, 56.6, -2.8, 183.8)),
    ("DATA", "Loss for the financial year", (None, -1.5, -0.2, -1.7)),
    ("DATA", "Other comprehensive income", (None, None, 1.1, 1.1)),
    ("DATA", "Pension additional contribution", (None, -3.0, 3.0, None)),
    ("TOTAL", "At 30 September 2024 (FY2024 closing)", (130.0, 52.1, 1.1, 183.2)),
    ("DATA", "Loss for the financial year", (None, -3.9, None, -3.9)),
    ("DATA", "Other comprehensive income", (None, None, 0.5, 0.5)),
    ("TOTAL", "At 30 September 2025 (FY2025 closing)", (130.0, 48.2, 1.6, 179.8)),
]

bw.add_equity_changes_sheet(
    title="Julian Hodge Bank Limited — Statement of Changes in Equity",
    subtitle="Chronological roll-forward, oldest to newest, FY2014-FY2025. Reconciliation ladder ties exactly year-to-year "
              "and to each year's own Balance Sheet Total equity throughout, with one documented exception: the FY2016/"
              "FY2017 boundary carries an explicit prior-period-error restatement row (see sheet note). 'Other reserves' "
              "column is Revaluation reserve (FY2014-FY2015, UK GAAP) / Available-for-sale + Pension reserve combined "
              "(FY2016-FY2019) / Pension reserve only (FY2020 onward, post-IFRS 9). £m.",
    headers=equity_headers,
    rows=equity_rows,
    sources_text=STATEMENTS_SOURCES + "\n\n" + HD074_NOTE,
)

# ---------------------------------------------------------------
# Asset Quality - Note 12/13's own IFRS 9 Stage 1/2/3/PMA provision
# roll-forward (portfolio-wide, all loans and advances to customers at
# amortised cost combined - no gross-exposure-by-stage table exists at
# portfolio level, only per-product segment tables for Commercial/PBTL/
# Motor separately, which don't sum to the full book since Retail's own
# stage split isn't separately disclosed).
# ---------------------------------------------------------------
asset_quality_rows = [
    ("SECTION", "Loans and advances to customers at amortised cost", {}),
    ("DATA", "Gross balances", {"FY2025": 1811.1, "FY2024": 1671.4, "FY2023": 1483.1, "FY2022": 1403.6, "FY2021": 989.9, "FY2020": 709.3, "FY2019": 526.4, "FY2018": 562.3, "FY2017": 469.9, "FY2016": 386.5, "FY2015": 335.3}),
    ("DATA", "Net loan fee deferral", {"FY2025": 13.0, "FY2024": 8.5, "FY2023": 2.9, "FY2022": 3.7, "FY2021": 1.9, "FY2020": -0.8, "FY2019": -1.7, "FY2018": -2.3, "FY2017": -2.5, "FY2016": -2.3, "FY2015": -1.9}),
    ("DATA", "Provision for impairment", {"FY2025": -13.8, "FY2024": -7.7, "FY2023": -6.0, "FY2022": -8.6, "FY2021": -8.4, "FY2020": -7.9, "FY2019": -9.8, "FY2018": -3.7, "FY2017": -6.4, "FY2016": -10.0, "FY2015": -7.6, "FY2014": -5.8}),
    ("TOTAL", "Net balance (amortised cost)", {"FY2025": 1810.3, "FY2024": 1672.2, "FY2023": 1480.0, "FY2022": 1398.7, "FY2021": 983.4, "FY2020": 700.6, "FY2019": 514.9, "FY2018": 556.3, "FY2017": 461.0, "FY2016": 374.2, "FY2015": 325.8}),
    ("DATA", "Impairment provision coverage (%)", {
        "FY2025": "0.76%", "FY2024": "0.46%", "FY2023": "0.40%", "FY2022": "0.61%", "FY2021": "0.85%",
        "FY2020": "1.11%", "FY2019": "1.86%", "FY2018": "0.66%", "FY2017": "1.36%", "FY2016": "2.59%", "FY2015": "2.27%",
    }),
    ("SECTION", "Impairment provision, by IFRS 9 stage (IFRS 9 adopted 1 November 2018 - stage data only exists FY2019 onward; "
               "FY2014-FY2018 show only the unstaged IAS 39/UK GAAP total provision above)", {}),
    ("DATA", "Stage 1 (12-month ECL)", {"FY2025": 3.6, "FY2024": 2.4, "FY2023": 1.3, "FY2022": 1.7, "FY2021": 1.3, "FY2020": 1.5, "FY2019": 2.4}),
    ("DATA", "Stage 2 (lifetime ECL, not credit-impaired)", {"FY2025": 1.7, "FY2024": 1.2, "FY2023": 3.1, "FY2022": 1.3, "FY2021": 2.0, "FY2020": 1.6, "FY2019": 0.1}),
    ("DATA", "Stage 3 (lifetime ECL, credit-impaired)", {"FY2025": 8.3, "FY2024": 4.2, "FY2023": 1.2, "FY2022": 4.8, "FY2021": 5.1, "FY2020": 4.8, "FY2019": 7.3}),
    ("DATA", "Post Model Adjustment", {"FY2025": 0.2, "FY2024": -0.1, "FY2023": 0.4, "FY2022": 0.8}),
    ("TOTAL", "Total provision for impairment", {"FY2025": 13.8, "FY2024": 7.7, "FY2023": 6.0, "FY2022": 8.6, "FY2021": 8.4, "FY2020": 7.9, "FY2019": 9.8, "FY2018": 3.7, "FY2017": 6.4, "FY2016": 10.0, "FY2015": 7.6, "FY2014": 5.8}),
    ("SECTION", "Loans and advances by product, at amortised cost (before hedge FV adjustment / retirement mortgages FVTPL)", {}),
    ("DATA", "Retail", {"FY2025": 1371.8, "FY2024": 1315.9, "FY2023": 1234.9, "FY2022": 1140.0, "FY2021": 679.0}),
    ("DATA", "Commercial (real estate)", {"FY2025": 218.1, "FY2024": 189.7, "FY2023": 170.4, "FY2022": 182.2, "FY2021": 233.9}),
    ("DATA", "Portfolio Buy-to-Let", {"FY2025": 37.3, "FY2024": 70.3, "FY2023": 74.7, "FY2022": 76.5, "FY2021": 70.5}),
    ("DATA", "Motor receivables", {"FY2025": 183.1, "FY2024": 96.3}),
    ("DATA", "Amounts owed from parent and fellow subsidiaries", {"FY2021": 0.4}),
]

# ---------------------------------------------------------------
# Sheet: Cash Flow Statement (exemption note in place of line items)
# ---------------------------------------------------------------
rows = [
    ("SECTION", "No Statement of Cash Flows is published by this entity in any year", {}),
    ("DATA", "See the note below for the FRS 101 exemption this entity relies on every year, and why this "
             "workbook is built as a Pillar-3-only variant.", {}),
]

bw.add_cash_flow_sheet(
    title="Julian Hodge Bank Limited — Cash Flow Statement",
    subtitle="Not applicable — this entity takes the FRS 101 cash-flow-statement disclosure exemption every year. See source note below.",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=90,
    source_height=260,
    unit_suffix="",
)

bw.add_asset_quality_sheet(
    title="Julian Hodge Bank Limited — Asset Quality",
    subtitle="Portfolio-wide IFRS 9 Stage 1/2/3 impairment provision roll-forward (Note 13/14). £m.",
    rows=asset_quality_rows,
    sources_text=STATEMENTS_SOURCES + (
        "\n\nDATA QUALITY FLAG: AR2025's own Note 13 table prints its 2025-year closing row as \"At 30 September 2024\" "
        "and its 2024-year closing row as \"At 30 September 2023\" - both appear to be an off-by-one-year label carried "
        "over from an earlier template (each closing row's own figures follow arithmetically from that block's own "
        "opening row and match the FOLLOWING year's contemporaneous report exactly), so the closing rows are treated "
        "here as FY2025 and FY2024 respectively, not as literally labelled. No gross-exposure-by-IFRS-9-stage table "
        "exists at portfolio level in any year - only the impairment PROVISION is broken out by stage portfolio-wide; "
        "gross exposure by stage is only disclosed for the Commercial/PBTL/Motor segments separately (not for Retail, "
        "the largest segment), so a full gross-by-stage table is not reconstructable without assuming Retail's split."
    ),
    first_col_width=76,
    source_height=380,
    unit_suffix=" (£m)",
    years=PILLAR3_YEARS,
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, unit, rows_data, sources_text, note=note, first_col_width=52, source_height=170, years=PILLAR3_YEARS)


metric(
    "CET1 Capital", "£m",
    [("Common Equity Tier 1 (CET1) capital", {"FY2025": 162.8, "FY2024": 166.2, "FY2023": 172.9, "FY2022": 177, "FY2021": 143.8, "FY2020": 136.4, "FY2019": 156.6, "FY2018": 168.0, "FY2017": 149.3, "FY2016": 129.1})],
    p3_sources(),
    note="FY2021's own report (P3 2021) shows CET1 = 143.8; the following year's Pillar 3 document (P3 2022) "
         "restates the FY2021 comparative to 144 (rounding to whole £m from that document's own precision) - "
         "each year's own originally-published figure is used per this project's convention. FY2014/FY2015 not "
         "shown: this bank's own Pillar 3 documents for those two years pre-date the CET1 concept (still reporting "
         "under Basel II Pillar 1 - 'Tier 1 capital' and 'Total capital resources' only, no CRD IV capital tiers). "
         "See the Total Capital sheet for the FY2014/FY2015 Basel II 'Total capital resources' figures instead.",
)

metric(
    "CET1 Ratio", "% of RWA",
    [("Common Equity Tier 1 (CET1) ratio", {"FY2025": "17.5%", "FY2024": "19.8%", "FY2023": "24.5%", "FY2022": "25.2%", "FY2021": "20.2%", "FY2020": "19.7%", "FY2019": "23.0%", "FY2018": "22.3%", "FY2017": "21.1%", "FY2016": "19.2%"})],
    p3_sources(),
)

metric(
    "Tier 1 Capital", "£m",
    [("Tier 1 capital", {"FY2025": 162.8, "FY2024": 166.2, "FY2023": 172.9, "FY2022": 177, "FY2021": 143.8, "FY2020": 136.4, "FY2019": 156.6, "FY2018": 168.0, "FY2017": 149.3, "FY2016": 129.1})],
    p3_sources(),
    note="Tier 1 = CET1 every year (no AT1 instruments in issue - 'Hold all its capital in the form of Common "
         "Equity Tier 1 and Tier 2 capital', and Tier 2 = nil every year per the Pillar 3 documents). FY2024/FY2025 "
         "not separately labelled 'Tier 1' in the Annual Report's brief capital note but equal to CET1 by the same "
         "pattern confirmed directly in FY2021-FY2023. FY2014/FY2015: pre-CRD IV Basel II regime - see CET1 Capital "
         "sheet note; for those two years 'Total Tier 1 capital' as reported was GBP117.1m (FY2014) and GBP118.6m "
         "(FY2015), which differs from the 'Total capital resources' shown on the Total Capital sheet because those "
         "two years DID hold a small amount of Tier 2 (general provisions less revaluation reserve deduction) - "
         "shown here only for completeness, not populated as a data column to avoid conflating Basel II Tier 1 with "
         "CRD IV Tier 1.",
)

metric(
    "Tier 1 Ratio", "% of RWA",
    [("Tier 1 ratio", {"FY2025": "17.5%", "FY2024": "19.8%", "FY2023": "24.5%", "FY2022": "25.2%", "FY2021": "20.2%", "FY2020": "19.7%", "FY2019": "23.0%", "FY2018": "22.3%", "FY2017": "21.1%", "FY2016": "19.2%"})],
    p3_sources(),
    note="Equal to CET1 ratio every year - see Tier 1 Capital sheet note.",
)

metric(
    "Total Capital", "£m",
    [("Total capital", {"FY2025": 162.8, "FY2024": 166.2, "FY2023": 172.9, "FY2022": 177, "FY2021": 143.8, "FY2020": 136.4, "FY2019": 156.6, "FY2018": 168.0, "FY2017": 149.5, "FY2016": 129.3, "FY2015": 122.4, "FY2014": 118.8})],
    p3_sources(),
    note="Equal to CET1/Tier 1 FY2016-FY2025 - the Bank holds no Tier 2 capital in those years. FY2014/FY2015: "
         "these figures are Basel II Pillar 1 'Total capital resources' (Tier 1 + a small Tier 2 add-back for "
         "eligible general provisions, net of a revaluation reserve deduction) - not directly comparable to the "
         "CRD IV 'Total capital' figures shown FY2016 onward, though presented on the same row per this project's "
         "convention of showing each year's own headline total-capital figure.",
)

metric(
    "Total Capital Ratio", "% of RWA",
    [("Total capital ratio", {"FY2025": "17.5%", "FY2024": "19.8%", "FY2023": "24.5%", "FY2022": "25.2%", "FY2021": "20.2%", "FY2020": "19.7%", "FY2019": "23.0%", "FY2018": "22.3%", "FY2017": "21.2%", "FY2016": "19.2%"})],
    p3_sources(),
)

metric(
    "Total RWAs", "£m",
    [("Total risk-weighted assets / exposure amount", {"FY2025": 930.2, "FY2024": 841.1, "FY2023": 704.7, "FY2022": 705, "FY2021": 711.0, "FY2020": 693.8, "FY2019": 681.9, "FY2018": 754.6, "FY2017": 706.3, "FY2016": 672.8})],
    p3_sources(),
    note="FY2021's own report (P3 2021) shows RWA = 711.0; the FY2022 Pillar 3 document's FY2021 comparative "
         "restates this to 711 (rounding only, immaterial) - each year's own originally-published figure is used. "
         "FY2014/FY2015 not available: those years' Pillar 3 documents pre-date CRD IV Pillar 3 RWA disclosure for "
         "this bank - only a Basel II 'Pillar 1 capital requirement' figure is given (FY2014: GBP36.3m; FY2015: "
         "GBP42.6m), not a risk-weighted-assets figure, so no RWA is shown for those two years rather than backing "
         "one out via an assumed 8% minimum ratio (which the source document itself does not state).",
)

# ---------------------------------------------------------------
# RWA Breakdown - FY2023/FY2022/FY2021 sourced from each year's own
# standalone Pillar 3 document's "Risk Type Breakdown" (UK OV1-style)
# table; FY2025/FY2024 have no standalone Pillar 3 document (see
# BASIS_NOTE) so no category-level split exists, only the aggregate
# Total RWAs figure already shown on that sheet.
# ---------------------------------------------------------------
rwa_breakdown_rows = [
    ("DATA", "Credit risk (excluding CCR)", {"FY2023": 629.2, "FY2022": 644, "FY2021": 639.9}),
    ("DATA", "Counterparty credit risk (CCR) - includes CVA memo below for FY2023/FY2022 (this year's own template "
             "shows CVA as a memo item within CCR, not a separately additive line); FY2021's own template shows CVA "
             "as its own separately additive line instead (see next row)",
     {"FY2023": 2.7, "FY2022": 1, "FY2021": 4.6}),
    ("DATA", "Of which: Credit valuation adjustment (CVA) - memo only for FY2023/FY2022, already included in CCR above, not separately additive",
     {"FY2023": 0.2, "FY2022": 0}),
    ("DATA", "Credit valuation adjustment (CVA) - shown as its own separately additive risk type in FY2021's own Pillar 3 template only",
     {"FY2021": 0.8}),
    ("DATA", "Operational risk", {"FY2023": 58.9, "FY2022": 44, "FY2021": 36.5}),
    ("DATA", "Amounts below the threshold for deduction (250% risk weight)", {"FY2023": 13.9, "FY2022": 16, "FY2021": 29.2}),
    ("TOTAL", "Total risk-weighted exposure amount", {"FY2023": 704.7, "FY2022": 705, "FY2021": 711.0}),
]

bw.add_rwa_breakdown_sheet(
    title="Julian Hodge Bank Limited — RWA Breakdown",
    subtitle="FY2023-FY2021 only (see source note - no category-level RWA breakdown was located for any other year). £m.",
    rows=rwa_breakdown_rows,
    sources_text=p3_sources(
        "\nFY2025/FY2024: Not publicly disclosed at category level - no standalone Pillar 3 document is published for "
        "these years (see BASIS_NOTE above); only the aggregate Total RWAs figure exists, already shown on the Total "
        "RWAs sheet, sourced from each year's own Annual Report 'Capital risk management' note instead.\n"
        "FY2020-FY2016: each year's own standalone Pillar 3 document was reviewed in full but none contains a "
        "risk-type RWA breakdown table (no OV1-equivalent) - only the aggregate Total RWAs figure, already shown "
        "on the Total RWAs sheet.\n"
        "FY2015/FY2014: no RWA figure of any kind is disclosed for these two years (pre-CRD IV regime) - see the "
        "Total RWAs sheet note."
    ),
    first_col_width=90,
    source_height=280,
    unit_suffix=" (£m)",
    years=PILLAR3_YEARS,
)

metric(
    "Leverage Ratio", "£m / %",
    [
        ("Total Basel III/leverage ratio exposure measure (£m)", {"FY2023": 1649.9, "FY2022": 1624, "FY2021": 1732.2, "FY2020": 1423.5, "FY2019": 1393.2, "FY2018": 1412.2, "FY2017": 1309.5, "FY2016": 1359.3}),
        ("Leverage Ratio (%)", {"FY2023": "10.5%", "FY2022": "10.9%", "FY2021": "8.3%", "FY2020": "9.6%", "FY2019": "11.2%", "FY2018": "11.9%", "FY2017": "11.4%", "FY2016": "9.5%"}),
    ],
    p3_sources(),
    note="FY2024/FY2025 not available - no standalone Pillar 3 document exists for those years and the Annual "
         "Report's brief 'Capital risk management' note does not include a leverage ratio. DATA QUALITY FLAG: the "
         "FY2022 Pillar 3 document's own FY2021 comparative column shows a materially different leverage exposure "
         "(£1,320m) and ratio (10.9%) than FY2021's own contemporaneous report (£1,732.2m / 8.3%) - a genuine "
         "cross-vintage restatement in the bank's own documents, not a transcription error. Per this project's "
         "convention, each year's own originally-published figure is used (FY2021 = 8.3%, not the later-restated "
         "10.9%) - worth double-checking if this workbook is relied on for leverage-ratio trend analysis. FY2015/"
         "FY2014 not available - no leverage ratio concept existed under the Basel II regime those years used.",
)

metric(
    "LCR", "£m / %",
    [
        ("Total HQLA after haircuts (£m)", {"FY2023": 230.4, "FY2022": 334, "FY2021": 479.5, "FY2020": 196.4, "FY2019": 346.4, "FY2018": 245.2}),
        ("Total net cash outflow, adjusted value (£m)", {"FY2023": 130.2, "FY2022": 133, "FY2021": 137.1, "FY2020": 72.0, "FY2019": 67.0, "FY2018": 103.5}),
        ("Liquidity Coverage Ratio (%)", {"FY2023": "176.9%", "FY2022": "252%", "FY2021": "349.6%", "FY2020": "272.9%", "FY2019": "516.9%", "FY2018": "236.9%"}),
    ],
    p3_sources(),
    note="FY2024/FY2025 not available - see Leverage Ratio sheet note. Year-end (point-in-time) values shown, "
         "per each source document's own basis ('year end value for LCR related metrics'). FY2017/FY2016 Pillar 3 "
         "documents were reviewed in full but contain no LCR disclosure (UK LCR reporting for this class of firm "
         "phased in gradually; FY2018 is this bank's first year showing it). FY2015/FY2014 not available - see "
         "Leverage Ratio sheet note on the pre-CRD IV regime.",
)

metric(
    "NSFR", "£m / %",
    [
        ("Total available stable funding (£m)", {"FY2023": 1721.9, "FY2022": 1549, "FY2021": 1551.0, "FY2020": 1226.2}),
        ("Total required stable funding (£m)", {"FY2023": 1144.2, "FY2022": 1085, "FY2021": 922.7, "FY2020": 793.3}),
        ("Net Stable Funding Ratio (%)", {"FY2023": "150.5%", "FY2022": "143%", "FY2021": "168.1%", "FY2020": "154.6%", "FY2019": "217.6%"}),
    ],
    p3_sources(),
    note="FY2024/FY2025 not available - see Leverage Ratio sheet note. FY2019's own Pillar 3 document gives the "
         "ratio only (217.6%), with no ASF/RSF breakdown; the breakdown shown for FY2020 comes from FY2020's own "
         "report. FY2018/FY2017/FY2016 Pillar 3 documents were reviewed in full but contain no NSFR disclosure "
         "(UK NSFR reporting phased in later than LCR for this class of firm - FY2019 is this bank's first year "
         "showing it). FY2015/FY2014 not available - see Leverage Ratio sheet note on the pre-CRD IV regime.",
)

metric(
    "MREL Ratio", "£m / %",
    [("MREL ratio", {y: "Not publicly disclosed" for y in YEARS})],
    p3_sources(),
    note="No MREL figure (numeric or qualitative) appears in any of the Pillar 3 documents reviewed (FY2014-"
         "FY2023), nor in any Annual Report's brief capital note - no reason is stated. Consistent with this small "
         "private bank not being set an independent MREL requirement by the Bank of England, the same pattern "
         "seen at other small UK banks in this project (e.g. Cynergy Bank, DF Capital Bank).",
)

# ---------------------------------------------------------------
# Overview sheet (Pillar-3-only: no cash-flow chart)
# ---------------------------------------------------------------
bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {"FY2025": 2122.6, "FY2024": 2008.8, "FY2023": 1823.1, "FY2022": 1860.8, "FY2021": 1713.4, "FY2020": 1409.2, "FY2019": 1378.7, "FY2018": 1363.4, "FY2017": 1267.4, "FY2016": 1316.8, "FY2015": 999.0, "FY2014": 784.7}),
        ("Loans and advances to customers", {"FY2025": 1839.7, "FY2024": 1699.3, "FY2023": 1488.5, "FY2022": 1404.6, "FY2021": 1061.5, "FY2020": 930.8, "FY2019": 766.9, "FY2018": 827.9, "FY2017": 757.9, "FY2016": 706.9, "FY2015": 557.5, "FY2014": 440.8}),
        ("Deposits from customers", {"FY2025": 1860.3, "FY2024": 1639.4, "FY2023": 1368.1, "FY2022": 1425.0, "FY2021": 1381.0, "FY2020": 1071.4, "FY2019": 1042.8, "FY2018": 994.6, "FY2017": 947.7, "FY2016": 991.7, "FY2015": 848.6, "FY2014": 633.2}),
        ("Total equity", {"FY2025": 179.8, "FY2024": 183.2, "FY2023": 183.8, "FY2022": 185.0, "FY2021": 148.6, "FY2020": 141.0, "FY2019": 160.3, "FY2018": 171.7, "FY2017": 167.3, "FY2016": 146.3, "FY2015": 133.7, "FY2014": 132.0}),
    ],
    balance_sheet_unit="£m",
    income_statement_totals=[
        ("Net interest income", {"FY2025": 41.8, "FY2024": 39.7, "FY2023": 39.4, "FY2022": 29.4, "FY2021": 17.6, "FY2020": 15.6, "FY2019": 20.2, "FY2018": 18.3, "FY2017": 13.9, "FY2016": 13.2, "FY2015": 5.6, "FY2014": 2.9}),
        ("Net operating income", {"FY2025": 39.8, "FY2024": 41.9, "FY2023": 46.6, "FY2022": 38.6, "FY2021": 26.2, "FY2020": 20.9, "FY2019": 28.0, "FY2018": 18.2, "FY2017": 19.3, "FY2016": 33.5, "FY2015": 13.0, "FY2014": 9.3}),
        ("Profit/(loss) for the financial year", {"FY2025": -3.9, "FY2024": -1.7, "FY2023": -0.2, "FY2022": 4.8, "FY2021": 5.8, "FY2020": -15.9, "FY2019": -5.7, "FY2018": 5.5, "FY2017": 10.2, "FY2016": 17.6, "FY2015": 4.3, "FY2014": 4.1}),
    ],
    income_statement_unit="£m",
    equity_changes_totals=[
        ("Opening equity", {"FY2025": 183.2, "FY2024": 183.8, "FY2023": 185.0, "FY2022": 148.6, "FY2021": 141.0, "FY2020": 160.3, "FY2019": 171.7, "FY2018": 167.3, "FY2017": 153.5, "FY2016": 133.3, "FY2015": 132.0, "FY2014": 128.2}),
        ("Total comprehensive income/(loss) for the year", {"FY2025": -3.4, "FY2024": -0.6, "FY2023": -1.2, "FY2022": 11.4, "FY2021": 7.6, "FY2020": -19.3, "FY2019": -8.0, "FY2018": 4.4, "FY2017": 8.8, "FY2016": 13.0, "FY2015": 1.8, "FY2014": 3.8}),
        ("Other equity movements, net", {"FY2025": 0, "FY2024": 0, "FY2023": 0, "FY2022": 25.0, "FY2021": 0, "FY2020": 0, "FY2019": -3.4, "FY2018": 0, "FY2017": 5.0, "FY2016": 0, "FY2015": 0, "FY2014": 0}),
        ("Closing equity", {"FY2025": 179.8, "FY2024": 183.2, "FY2023": 183.8, "FY2022": 185.0, "FY2021": 148.6, "FY2020": 141.0, "FY2019": 160.3, "FY2018": 171.7, "FY2017": 167.3, "FY2016": 146.3, "FY2015": 133.7, "FY2014": 132.0}),
    ],
    equity_changes_unit="£m",
    cash_flow_totals=[],
    cash_flow_unit=None,
    ratios=[
        ("CET1 Ratio", {"FY2025": "17.5%", "FY2024": "19.8%", "FY2023": "24.5%", "FY2022": "25.2%", "FY2021": "20.2%", "FY2020": "19.7%", "FY2019": "23.0%", "FY2018": "22.3%", "FY2017": "21.1%", "FY2016": "19.2%"}),
        ("Tier 1 Ratio", {"FY2025": "17.5%", "FY2024": "19.8%", "FY2023": "24.5%", "FY2022": "25.2%", "FY2021": "20.2%", "FY2020": "19.7%", "FY2019": "23.0%", "FY2018": "22.3%", "FY2017": "21.1%", "FY2016": "19.2%"}),
        ("Total Capital Ratio", {"FY2025": "17.5%", "FY2024": "19.8%", "FY2023": "24.5%", "FY2022": "25.2%", "FY2021": "20.2%", "FY2020": "19.7%", "FY2019": "23.0%", "FY2018": "22.3%", "FY2017": "21.2%", "FY2016": "19.2%"}),
        ("Leverage Ratio", {"FY2023": "10.5%", "FY2022": "10.9%", "FY2021": "8.3%", "FY2020": "9.6%", "FY2019": "11.2%", "FY2018": "11.9%", "FY2017": "11.4%", "FY2016": "9.5%"}),
        ("LCR", {"FY2023": "176.9%", "FY2022": "252%", "FY2021": "349.6%", "FY2020": "272.9%", "FY2019": "516.9%", "FY2018": "236.9%"}),
        ("NSFR", {"FY2023": "150.5%", "FY2022": "143%", "FY2021": "168.1%", "FY2020": "154.6%", "FY2019": "217.6%"}),
    ],
    note="This entity takes the FRS 101/FRS 1 cash-flow-statement exemption every year FY2014-FY2025 (see the Cash "
         "Flow Statement sheet), so no cash flow summary or chart is shown here - Balance Sheet/Profit & Loss/"
         "Statement of Changes in Equity summaries and the Pillar 3 Key Metrics trend chart are shown instead. "
         "Leverage/LCR/NSFR availability varies by year - see each Pillar 3 sheet's own source citation for detail "
         "(pre-CRD IV FY2014/FY2015 have none of the three; LCR/NSFR were phased in for this bank in FY2018/FY2019 "
         "respectively). The FY2022 and FY2017 'Other equity movements' figures (£25.0m and £5.0m) are real share "
         "capital issuances those years, not plugs; the FY2019 figure (-£3.4m) is the IFRS 9 transition adjustment "
         "on adoption. Note FY2017's own 'Opening equity' (£153.5m) is the FY2017 Annual Report's RESTATED FY2016 "
         "closing position (Note 36 prior-period error, +£7.2m vs. the £146.3m FY2016 originally reported as its "
         "own closing figure) - both figures are shown, and this discontinuity, on the Statement of Changes in "
         "Equity sheet.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/JULIAN HODGE BANK FINANCIALS.xlsx")
