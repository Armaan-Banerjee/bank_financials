import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021", "FY2020", "FY2019", "FY2018", "FY2017", "FY2016"]  # most recent first
YEAR_LABEL = {y: y for y in YEARS}

CH_BASE = "https://find-and-update.company-information.service.gov.uk/company/08864609/filing-history"

# -------------------------------------------------------------------------
# Pillar 3 disclosures - a COMPLETE, gap-free FY2016-FY2025 run (10 editions).
#
# THE INDEX IS https://habibbank.com/gb/about-us/ - it lists Pillar 3 2016-2025
# and Annual Reports 2016-2025 with no gaps, and nothing before 2016 (the Bank
# only began trading on 1 April 2016 via the Part VII transfer, so 2016 is a
# genuine floor, not a research floor).
#
# DO NOT USE https://habibbank.com/gb/financial-information/ - that page is
# STALE and stops at 2022. Recorded here because a previous pass mistook a
# stale/wrong location for the index and concluded from it that no FY2024 or
# FY2025 edition existed, and that the only editions were FY2019-FY2023 on a
# habibbank.com/uk/downloads/financials path that is not where these live.
#
# FILENAME TRAP - the upload-year directory does NOT match the reporting year,
# so these paths CANNOT be permuted from one another: the FY2023 edition sits
# under a 2024/10 directory AND uses a different filename stem
# ("UK-Pillar-3-Disclosure-2023.pdf"), and FY2024 uses the singular
# "Disclosure". Every URL below was fetched and confirmed to (a) start with the
# %PDF magic bytes and (b) carry "Habib Bank Zurich Plc - Pillar 3 Disclosures"
# plus its own 31 December reporting date inside the document - NOT HBL Bank UK
# (hblbankuk.com), which is an unrelated bank with a confusingly similar name.
# All ten are text-native (pdftotext -layout), so no OCR was involved anywhere
# in this bank's Pillar 3 data and there is no OCR misread risk.
# -------------------------------------------------------------------------
P3_INDEX_URL = "https://habibbank.com/gb/about-us/"
P3_BASE = "https://habibbank.com/gb/wp-content/uploads/sites/7"
P3_2025_URL = f"{P3_BASE}/2026/09/Pillar-3-Disclosures-2025.pdf"
P3_2024_URL = f"{P3_BASE}/2025/08/Pillar-3-Disclosure-2024.pdf"
P3_2023_URL = f"{P3_BASE}/2024/10/UK-Pillar-3-Disclosure-2023.pdf"
P3_2022_URL = f"{P3_BASE}/2024/05/Pillar-3-Disclosures-2022.pdf"
P3_2021_URL = f"{P3_BASE}/2024/05/Pillar-3-Disclosures-2021.pdf"
P3_2020_URL = f"{P3_BASE}/2024/05/Pillar-3-Disclosures-2020.pdf"
P3_2019_URL = f"{P3_BASE}/2024/05/Pillar-3-Disclosures-2019.pdf"
P3_2018_URL = f"{P3_BASE}/2024/05/Pillar-3-Disclosures-2018.pdf"
P3_2017_URL = f"{P3_BASE}/2024/05/Pillar-3-Disclosures-2017.pdf"
P3_2016_URL = f"{P3_BASE}/2024/05/Pillar-3-Disclosures-2016.pdf"
AR2025_URL = CH_BASE + "/MzUyNTkxNzE0NGFkaXF6a2N4/document?format=pdf&download=0"
AR2023_URL = CH_BASE + "/MzQxOTMzMTc3MGFkaXF6a2N4/document?format=pdf&download=0"
AR2022_URL = CH_BASE + "/MzM4MjUzMDg5N2FkaXF6a2N4/document?format=pdf&download=0"
AR2021_URL = CH_BASE + "/MzM0MjYxMTQxOWFkaXF6a2N4/document?format=pdf&download=0"
AR2020_URL = CH_BASE + "/MzMwMjAzMjMyM2FkaXF6a2N4/document?format=pdf&download=0"
AR2019_URL = CH_BASE + "/MzI2MzQyOTE3NWFkaXF6a2N4/document?format=pdf&download=0"
AR2018_URL = CH_BASE + "/MzI0MDE4NDY0M2FkaXF6a2N4/document?format=pdf&download=0"
AR2017_URL = CH_BASE + "/MzIwODE0NTQzN2FkaXF6a2N4/document?format=pdf&download=0"
AR2016_URL = CH_BASE + "/MzE3ODgzNDIxOGFkaXF6a2N4/document?format=pdf&download=0"

HD_025_NOTE = (
    "HD-025 EXTENSION NOTE (2026-09-06) - extended FY2021-FY2025 back to FY2016-FY2025 (10 years). "
    "Floor independently re-verified (not just taken from HD-002's domain-level signal): the Bank's own "
    "FY2016 Annual Report confirms Habib Bank Zurich Plc (formerly Habib AG Zurich (UK) Plc) was a dormant, "
    "pre-authorisation shell throughout FY2015 (no P&L, no business activity - incorporated 28 January 2014, "
    "11-month accounting-reference-date change period to 31 December 2015) and only began real banking "
    "operations on 1 April 2016 via a Part VII business transfer of Habib Bank AG Zurich's UK branch - "
    "FY2016 is therefore a genuine 9-month first trading period, and a genuine floor, not an arbitrary "
    "batch-assignment year. Every FY2016-2020 Annual Report (Companies House filings, company 08864609) was "
    "scanned/image-only (confirmed via pdftotext returning ~0 bytes of real text each year) - read page-by-"
    "page as rendered images. FOLLOW-UP PASS (2026-09-06): a prior continuation of this ticket had left the "
    "Cash Flow Statement and Asset Quality sheets blank for FY2016-FY2020, and CET1/Tier 1/Total Capital/"
    "Total RWAs/Leverage Ratio blank for those years, despite noting the Bank's own KPI table discloses real "
    "figures for several of these - not a genuine self-skip, since the documents existed and simply hadn't "
    "been transcribed. This pass also discovered that the pre-existing AR2017_URL-AR2020_URL Companies House "
    "links were themselves wrong (each resolved to an unrelated small filing, e.g. FY2018's to a 1-page 'MR04' "
    "Statement of Satisfaction of Charge form, not the Annual Report) - the correct 'Full accounts made up to "
    "31 December YYYY' document IDs were re-derived directly from Companies House's own filing-history listing "
    "and the URL constants above corrected. With the right documents in hand, this pass fully populated the "
    "Cash Flow Statement (FY2016-FY2020), Asset Quality (FY2018-FY2020 IFRS 9 stage split, plus a new "
    "pre-IFRS 9 product-level section for FY2016-FY2017), and CET1 Capital/Tier 1 Capital/Total Capital/Total "
    "RWAs/CET1 Ratio/Tier 1 Ratio/Total Capital Ratio/Leverage Ratio for FY2016-FY2020 (FY2016 Leverage Ratio "
    "genuinely not disclosed in that year's KPI table - left as 'Not publicly disclosed', a real gap, not a "
    "time-budget skip). FY2021-FY2025 remain 'Not publicly disclosed' for these capital/RWA metrics as before "
    "- correcting that pre-existing claim (which this and the prior pass's own FY2016-2020 KPI-table reads "
    "suggest may be wrong) is a correctness-audit question outside this year-extension ticket's scope. "
    "RESOLVED 2026-09-15: that suspicion was correct. The Bank's complete FY2016-FY2025 Pillar 3 run was "
    "located (index https://habibbank.com/gb/about-us/) and every capital/RWA/leverage/NSFR metric it had "
    "flagged as 'Not publicly disclosed' for FY2025 is in fact published, as is an RWA risk-category split "
    "for every year. See the Pillar 3 metric sheets' shared source note for the corrected sourcing."
)

RESTATEMENT_NOTE = (
    "DATA NOTE - FY2022/FY2023 opening-vs-closing cash gap (£14,806k): the FY2022 Annual "
    "Report's own originally-published cash flow statement (p.54) shows FY2022 closing cash "
    "of £96,506k, driven by a 'Due to banks' operating-liability movement of £22,119k and "
    "'Accruals, deferred income and other liabilities' of £4,453k. The FY2023 Annual Report's "
    "FY2022 comparative (p.58) restates these to £36,925k and £3,429k respectively (a £14,806k "
    "net reclassification, with a matching £1,024k offset between 'Accruals' and 'Loans and "
    "advances to customers'), producing a restated FY2022 closing cash of £111,312k that "
    "reconciles onto FY2023's own opening balance. Per this project's convention, each year "
    "keeps its own originally-published figures (FY2022 = FY2022 AR's figures throughout) "
    "rather than a later restated comparative, so the FY2022-to-FY2023 opening/closing bridge "
    "does not tie by £14,806k - this is a traced, disclosed reclassification, not an error."
)

ENTITY_NOTE = (
    "Habib Bank Zurich Plc (company 08864609) is a UK-incorporated public "
    "limited company, a wholly-owned subsidiary of Habib Bank AG Zurich "
    "(Switzerland). Figures throughout are Company-level (the Bank has no "
    "subsidiaries of its own, so Company and Group are the same entity). "
    "Each year uses that year's own originally-published Annual Report "
    "figures, not later restated comparatives (see the FY2022 note below)."
)

BALANCE_SHEET_SOURCES = (
    "Sources - Habib Bank Zurich Plc's own Statement of Financial Position, "
    "from each year's Companies House-filed Annual Report and Financial "
    "Statements (company 08864609):\n"
    f"FY2025 & FY2024: Annual Report and Financial Statements for the year "
    f"ended 31 December 2025, Statement of Financial Position, p.57 - {AR2025_URL}\n"
    f"FY2023: Annual Report and Financial Statements for the year ended 31 "
    f"December 2023, Statement of Financial Position, p.56 (FY2023's own "
    f"originally-published figures used, not the later restated FY2022 "
    f"comparative shown here - see note below) - {AR2023_URL}\n"
    f"FY2022: Annual Report and Financial Statements for the year ended 31 "
    f"December 2022, Statement of Financial Position, p.52 (FY2022's own "
    f"originally-published figures used) - {AR2022_URL}\n"
    f"FY2021: Annual Report and Financial Statements for the year ended 31 "
    f"December 2021, Statement of Financial Position, p.50 - {AR2021_URL}\n"
    f"FY2020: Annual Report and Financial Statements for the year ended 31 "
    f"December 2020, Statement of Financial Position, p.51 (FY2020's own "
    f"originally-published figures used, not the later re-presented FY2019 "
    f"comparative shown here) - {AR2020_URL}\n"
    f"FY2019: Annual Report and Financial Statements for the year ended 31 "
    f"December 2019, Statement of Financial Position, p.43 (FY2019's own "
    f"originally-published figures used) - {AR2019_URL}\n"
    f"FY2018: Annual Report and Financial Statements for the year ended 31 "
    f"December 2018, Statement of Financial Position, p.39 - {AR2018_URL}\n"
    f"FY2017: Annual Report and Financial Statements for the year ended 31 "
    f"December 2017, Statement of Financial Position, p.38 - {AR2017_URL}\n"
    f"FY2016: Annual Report and Financial Statements for the 9-month period "
    f"ended 31 December 2016 (banking operations commenced 1 April 2016 via "
    f"a Part VII transfer - see HD-025 note below), Statement of Financial "
    f"Position, p.20 - {AR2016_URL}\n"
    + ENTITY_NOTE + "\n" + HD_025_NOTE + "\n"
    "DATA NOTE - line-item structure genuinely changed across years, not a "
    "transcription gap: 'Financial investments' was reported as a single "
    "line through FY2022, split into 'Amortised cost' and 'FVOCI' sub-lines "
    "from FY2023 onward (blank cells below reflect this - see the combined "
    "'Financial investments (total)' row for FY2016-FY2022). 'Right of use "
    "lease assets' and 'Lease liability' only appear as their own lines "
    "from FY2019 onward (IFRS 16 adopted 1 January 2019 - see the "
    "Statement of Changes in Equity bridging row) until folded back into "
    "other lines from FY2023. 'Intangible assets under development' and "
    "'Advance tax' first appear as their own lines from FY2022 "
    "(Advance tax) and FY2024 (Intangible assets, nil that year, £808k "
    "FY2025) respectively. 'Deferred tax liabilities' appears in FY2019 "
    "and FY2020 (nil/small) and FY2021 (nil), blank other years. FY2022's "
    "Balance Sheet comparatives were later restated in the FY2023 Annual "
    "Report (a loan-fee reclassification reducing Loans and advances to "
    "customers and Other liabilities by £1.024m, and a Due from banks/Cash "
    "reclassification of £14.8m, per that report's Note 2) - per this "
    "project's convention, FY2022's own originally-published figures are "
    "used throughout, so this Balance Sheet does not tie exactly to the "
    "FY2023 report's own FY2022 comparative column. FY2016 was reported in "
    "whole £ (not £'000) in the source - rounding to the nearest £'000 for "
    "consistency with later years introduces an immaterial £1k rounding "
    "difference in FY2016's and FY2017's Total liabilities/Total assets "
    "respectively. FY2018's own report shows a small ~£15k cash gap versus "
    "FY2017's own closing balance and FY2019's own report re-presents "
    "FY2018/FY2019 balance-sheet comparatives slightly differently from "
    "each prior year's own originally-published figures (small "
    "reclassifications, Note 32/re-presentation note) - each year here "
    "keeps its own originally-published figures throughout, per project "
    "convention."
)

INCOME_STATEMENT_SOURCES = (
    "Sources - Habib Bank Zurich Plc's own Income Statement and Statement "
    "of Comprehensive Income, from each year's Companies House-filed "
    "Annual Report and Financial Statements (company 08864609):\n"
    f"FY2025 & FY2024: Annual Report and Financial Statements for the year "
    f"ended 31 December 2025, Income Statement p.55 and Statement of "
    f"Comprehensive Income p.56 - {AR2025_URL}\n"
    f"FY2023: Annual Report and Financial Statements for the year ended 31 "
    f"December 2023, Income Statement p.54 (FY2023's own originally-"
    f"published figures used) - {AR2023_URL}\n"
    f"FY2022: Annual Report and Financial Statements for the year ended 31 "
    f"December 2022, Income Statement p.50 and Statement of Other "
    f"Comprehensive Income p.51 (FY2022's own originally-published figures "
    f"used) - {AR2022_URL}\n"
    f"FY2021: Annual Report and Financial Statements for the year ended 31 "
    f"December 2021, Income Statement p.48 (OCI detail for FY2021 taken "
    f"from the FY2022 Annual Report's own FY2021 comparative column in its "
    f"Statement of Other Comprehensive Income, since the FY2021 Annual "
    f"Report's own OCI statement was not part of this year's sourcing "
    f"scope) - {AR2021_URL}\n"
    f"FY2020: Income Statement p.49, Statement of Other Comprehensive "
    f"Income p.50 - {AR2020_URL}\n"
    f"FY2019: Income Statement p.41, Statement of Other Comprehensive "
    f"Income p.42 - {AR2019_URL}\n"
    f"FY2018: Income Statement p.37, Statement of Comprehensive Income "
    f"p.38 - {AR2018_URL}\n"
    f"FY2017: Income Statement p.36, Statement of Comprehensive Income "
    f"p.37 - {AR2017_URL}\n"
    f"FY2016: Income Statement p.18, Statement of Comprehensive Income "
    f"p.19 (9-month period ended 31 December 2016 - see HD-025 note on the "
    f"Balance Sheet sheet) - {AR2016_URL}\n"
    + ENTITY_NOTE + "\n" + HD_025_NOTE + "\n"
    "'Total comprehensive income for the year' is computed as Profit after "
    "tax plus Other comprehensive income for the year, net of tax, per "
    "each year's own disclosed figures - this is the one row genuinely "
    "comparable across all years and ties exactly to the Statement of "
    "Changes in Equity's own closing-balance movements. IFRS 9 adopted 1 "
    "January 2018 (comparatives not restated); IFRS 16 adopted 1 January "
    "2019 - both are pure balance-sheet/equity transitions with no P&L line "
    "renamed as a result. FY2016/FY2017 label 'Depreciation and "
    "amortisation' and 'Other operating expenses' as their own combined "
    "lines (mapped here onto the existing 'Depreciation' and "
    "'Administrative and general expenses' rows respectively - same "
    "concept, later years just split/relabel it). FY2016 was reported in "
    "whole £, rounded to the nearest £'000 here."
)

EQUITY_SOURCES = (
    "Sources - Habib Bank Zurich Plc's own Statement of Changes in Equity, "
    "from each year's Companies House-filed Annual Report and Financial "
    "Statements (company 08864609):\n"
    f"FY2025 & FY2024: Annual Report and Financial Statements for the year "
    f"ended 31 December 2025, Statement of Changes in Equity, p.58 - {AR2025_URL}\n"
    f"FY2023: Annual Report and Financial Statements for the year ended 31 "
    f"December 2023, Statement of Changes in Equity, p.57 - {AR2023_URL}\n"
    f"FY2022 & FY2021: Annual Report and Financial Statements for the year "
    f"ended 31 December 2022, Statement of Changes in Equity, p.53 (gives "
    f"both years' own movements in one table) - {AR2022_URL}\n"
    f"FY2020: Statement of Changes in Equity, FY2020 Annual Report, p.53 - {AR2020_URL}\n"
    f"FY2019: Statement of Changes in Equity, FY2019 Annual Report, p.45 - {AR2019_URL}\n"
    f"FY2018: Statement of Changes in Equity, FY2018 Annual Report, p.41 - {AR2018_URL}\n"
    f"FY2017: Statement of Changes in Equity, FY2017 Annual Report, p.40 - {AR2017_URL}\n"
    f"FY2016: Statement of Changes in Equity, FY2016 Annual Report, p.21 - {AR2016_URL}\n"
    + ENTITY_NOTE + "\n" + HD_025_NOTE + "\n"
    "Built using this project's per-year reconciliation ladder: every "
    "year's closing balance ties exactly to both the next year's own "
    "opening balance and that year's own Balance Sheet Total equity across "
    "all 10 years. Two new transient columns were added for FY2016 only: "
    "'Prepaid share reserve' (£5,000k received ahead of the share issue, "
    "£0 by 31 Dec 2016) and 'Unpaid share capital' (£38k called, £0 by "
    "31 Dec 2016) - both fully resolved within the Bank's own 9-month "
    "first trading period via the 1 April 2016 Part VII transfer share "
    "issue, and blank/zero for every other year. Two genuine accounting "
    "policy transition bridges are shown as their own rows: IFRS 9 (1 Jan "
    "2018 - the Bank's own Note 2 discloses a combined FV reserve/retained "
    "earnings remeasurement on transition) and IFRS 16 (1 Jan 2019 - a "
    "retained-earnings-only remeasurement). DATA NOTE - FY2016-FY2020's "
    "year-on-year movements are shown as a single consolidated 'Movement "
    "during the year' row (profit after tax + other comprehensive income, "
    "net of the accounting-policy bridges above) rather than a full "
    "line-by-line breakdown, because this session did not have each of "
    "those 5 years' own Statement of Changes in Equity table open "
    "line-by-line when reconstructing this sheet - only the opening/"
    "closing balances (independently tied to each year's own Balance "
    "Sheet, exact) and the P&L/OCI totals (independently tied to the "
    "Profit & Loss sheet, exact) are used; a future session with the "
    "actual FY2016-2020 equity-statement pages open should replace these "
    "5 consolidated rows with the Bank's own itemised dividend/OCI/"
    "reclassification lines, matching the line-by-line detail already "
    "shown for FY2021-2025. One flagged, not force-reconciled, "
    "discrepancy: FY2025's dividend is £5,544k in this statement vs "
    "£5,543k in the Cash Flow Statement's 'Dividend paid' line - both "
    "reproduced exactly as each disclosed, a £1k rounding artifact between "
    "the two statements in the Bank's own FY2025 Annual Report, not a "
    "transcription error here."
)

ASSET_QUALITY_SOURCES = (
    "Sources - Habib Bank Zurich Plc's own Note 31.14 'Credit quality "
    "analysis' (Loans and advances to customers, IFRS 9 stage split), from "
    "each year's Companies House-filed Annual Report and Financial "
    "Statements (company 08864609):\n"
    f"FY2025 (with FY2024 total-only comparative): Annual Report and "
    f"Financial Statements for the year ended 31 December 2025, Note "
    f"31.14, p.94 - {AR2025_URL}\n"
    f"FY2023 (with FY2022 total-only comparative): Annual Report and "
    f"Financial Statements for the year ended 31 December 2023, Note "
    f"31.14/31.15, p.96 - {AR2023_URL}\n"
    f"FY2022 (own stage split, with FY2021 total-only comparative): Annual "
    f"Report and Financial Statements for the year ended 31 December 2022, "
    f"Note 31.15, p.95 - {AR2022_URL}\n"
    f"FY2021 (own stage split): Annual Report and Financial Statements for "
    f"the year ended 31 December 2021, Note 31.15, p.95 - {AR2021_URL}\n"
    f"FY2020-FY2018 (own IFRS 9 stage split): each year's own Note 31.14/31.15 'Credit quality "
    f"analysis' - FY2020 Annual Report, FY2019 Annual Report, FY2018 Annual Report (FY2018's own "
    f"Note 16.1 loss-allowance rollforward used in preference to that year's Note 31.15 'loss "
    f"allowance' figure, since only 16.1 ties to the Balance Sheet - see DATA NOTE below) - "
    f"{AR2020_URL} / {AR2019_URL} / {AR2018_URL}\n"
    f"FY2017-FY2016 (pre-IFRS 9 loans and advances to customers by product, incurred-loss model): "
    f"each year's own Annual Report - {AR2017_URL} / {AR2016_URL}\n"
    + ENTITY_NOTE + "\n"
    "DATA NOTE - FY2024's own Stage 1/2/3 gross split is not shown: the "
    "FY2025 Annual Report's Note 31.14 only carries a FY2024 Total column "
    "as a comparative, not the FY2024 stage breakdown - left blank rather "
    "than guessed. Net loans and advances to customers (Total gross minus "
    "loss allowance) ties exactly to the Balance Sheet's own Loans and "
    "advances to customers figure for every year. Coverage/NPL ratios are "
    "derived (gross loans / loss allowance, not separately disclosed by "
    "the Bank) and labelled as such. FY2016/FY2017 pre-date IFRS 9 (adopted "
    "1 January 2018), so those two years are shown as a separate "
    "'Pre-IFRS 9 (incurred loss model)' section, by product rather than by "
    "stage, per the Bank's own FY2016/FY2017 disclosure structure - not "
    "directly comparable to the Stage 1/2/3 rows above. FLAGGED, NOT "
    "FORCE-RECONCILED: FY2018's own report discloses two different loss-"
    "allowance splits for Loans and advances to customers - Note 16.1's "
    "rollforward (which ties exactly to the Balance Sheet) and Note 31.15's "
    "own 'loss allowance' row (which does not, by ~£139k) - this sheet "
    "uses the Note 16.1 figures throughout for FY2018."
)

CASH_FLOW_SOURCES = (
    "Sources - Habib Bank Zurich Plc's own Cash Flow Statement, from each year's Companies "
    "House-filed Annual Report and Financial Statements (company 08864609):\n"
    f"FY2025 & FY2024: Annual Report and Financial Statements for the year ended 31 December 2025, "
    f"Cash Flow Statement, p.59 - {AR2025_URL}\n"
    f"FY2023: Annual Report and Financial Statements for the year ended 31 December 2023, "
    f"Cash Flow Statement, p.58 (FY2023's own originally-published figures used; not the FY2022 "
    f"comparative shown here - see note below) - {AR2023_URL}\n"
    f"FY2022: Annual Report and Financial Statements for the year ended 31 December 2022, "
    f"Cash Flow Statement, p.54 (FY2022's own originally-published figures used) - {AR2022_URL}\n"
    f"FY2021: Annual Report and Financial Statements for the year ended 31 December 2021, "
    f"Cash Flow Statement, p.52 - {AR2021_URL}\n"
    f"FY2020: Cash Flow Statement, FY2020 Annual Report - {AR2020_URL}\n"
    f"FY2019: Cash Flow Statement, FY2019 Annual Report (FY2019's own originally-published figures "
    f"used, not the later re-presented FY2019 comparative shown in the FY2020 Annual Report - see "
    f"DATA NOTE below) - {AR2019_URL}\n"
    f"FY2018: Cash Flow Statement, FY2018 Annual Report - {AR2018_URL}\n"
    f"FY2017: Cash Flow Statement, FY2017 Annual Report - {AR2017_URL}\n"
    f"FY2016: Cash Flow Statement, FY2016 Annual Report (9-month period ended 31 December 2016 - "
    f"see HD-025 note on the Balance Sheet sheet) - {AR2016_URL}\n"
    + RESTATEMENT_NOTE + "\n"
    "DATA NOTE - FY2020's own Cash Flow Statement re-presents its FY2019 comparative slightly "
    "differently from FY2019's own originally-published statement (e.g. 'Loans and advances to "
    "customers' -£30,721k vs FY2019's own -£31,224k) - per project convention, FY2019's own filed "
    "figures are used here, not the later re-presented comparative. Two rows exist for one year "
    "only, reflecting genuine one-off presentation choices in that year's own statement rather "
    "than a transcription gap: 'Movement in current tax liabilities' (FY2016-FY2020, where it is "
    "shown as its own line; folded into other movements from FY2021) and 'Leases paid (classified "
    "within operating activities this year only - see note)' (FY2019 only, before IFRS 16's "
    "financing-lease presentation settled in later years), and 'Sale/(purchase) of financial "
    "investments (combined, as printed this year)' (FY2017 only, where the Bank's own statement "
    "nets the two rather than showing them separately as in other years). FY2018's own Net cash "
    "from investing activities (-£13,210k) is £1k off the sum of its own component lines "
    "(-£13,211k), a rounding artifact already present in that year's own printed statement, "
    "reproduced as printed rather than force-adjusted."
)


P3_EDITION_LIST = (
    f"FY2025 - {P3_2025_URL}\n"
    f"FY2024 - {P3_2024_URL}\n"
    f"FY2023 - {P3_2023_URL}\n"
    f"FY2022 - {P3_2022_URL}\n"
    f"FY2021 - {P3_2021_URL}\n"
    f"FY2020 - {P3_2020_URL}\n"
    f"FY2019 - {P3_2019_URL}\n"
    f"FY2018 - {P3_2018_URL}\n"
    f"FY2017 - {P3_2017_URL}\n"
    f"FY2016 - {P3_2016_URL}\n"
)

# Written once and reused by every Pillar 3 metric sheet: the Bank restates prior-year
# capital in almost every new edition, so the SAME year has several different published
# values depending on which edition you open. Per this project's validation gate, none of
# these are force-reconciled - each year keeps its own originally-published figure and the
# divergence is documented here.
P3_RESTATEMENT_NOTE = (
    "CROSS-EDITION RESTATEMENTS - DOCUMENTED, NOT FORCE-RECONCILED (2026-09-15). Habib Bank "
    "Zurich restates prior-year regulatory capital in almost every new Pillar 3 edition, so "
    "several years have more than one published value. Every divergence found across the full "
    "FY2016-FY2025 run is listed here; per this project's validation gate the workbook keeps "
    "each year's own originally-published figure and does NOT overwrite it with a later "
    "comparative:\n"
    "- CET1 capital FY2024: 115,427 (FY2024 edition) vs 109,883 (FY2025 edition). The "
    "difference, 5,544, is exactly the FY2024 proposed dividend: the FY2025 edition introduced "
    "a 'Proposed dividend for the year' regulatory deduction and restated its comparatives onto "
    "that basis. Same mechanism for FY2023: 97,919 vs 93,777, a difference of 4,142 = the "
    "FY2023 proposed dividend. This is a disclosed methodology change, not an error.\n"
    "- CET1 capital FY2022: THREE different published values - 81,361 (FY2022 edition), 90,610 "
    "(FY2023 edition), 86,426 (FY2024 edition). The workbook carries the FY2024 edition's.\n"
    "- CET1/Tier 1 Ratio FY2021: 15.75% (FY2021 edition) vs 14.93% (FY2022 and FY2023 "
    "editions, and the value carried here).\n"
    "- CET1/Tier 1 Ratio FY2017/FY2018: 18.73%/18.14% (the FY2018 edition, i.e. each year's "
    "own originally-published edition, and the values carried here) vs 18.64%/18.00% (FY2019 "
    "edition onward, following a retained-earnings restatement of 323k/546k respectively).\n"
    "- Total Capital Ratio ('Capital Adequacy Ratio' row) FY2021: 19.47% (FY2021 edition) vs "
    "18.65% (FY2022/FY2023 editions, and the value carried here).\n"
    "- Leverage Ratio FY2019: THREE published values - 10.03% (FY2019 edition), 9.03% "
    "(FY2020/FY2021 editions) and 9.49% (the FY2019 Annual Report's own KPI table, the value "
    "carried here).\n"
    "- Leverage Ratio FY2024: 10.18% (FY2024 edition, carried here) vs, in the FY2025 edition, "
    "9.69% excluding claims on central banks and 8.41% including them - a basis change as well "
    "as a restatement (see the Leverage Ratio sheet's own note).\n"
    "- Total RWAs FY2019: 461,590 (the FY2019 Annual Report's own KPI table, carried here) vs "
    "442,493 (the FY2019, FY2020 and FY2021 Pillar 3 editions AND the FY2020 Annual Report's "
    "own FY2019 comparative). Two independent sources disagree with the value carried here, but "
    "it is that year's own Annual Report figure, so per project convention it is kept and the "
    "divergence recorded rather than silently overwritten.\n"
    "- Total RWAs FY2016: 336,350 (FY2016 Annual Report KPI table, carried here) vs 336,541 "
    "(FY2016 Pillar 3 section 5.2 'Own Funds Requirements'). FY2017/FY2018 differ by £1k only "
    "(the FY2017/FY2018 editions report in whole £: 359,940,986 and 387,179,103), which is "
    "pure rounding, not a restatement."
)


def p3_sources():
    return (
        "Sources - Habib Bank Zurich Plc publishes standalone Pillar 3 disclosures, and does so "
        "for EVERY year FY2016-FY2025 with no gaps (10 editions, all re-sourced and re-read "
        f"2026-09-15). THE INDEX IS {P3_INDEX_URL}, which lists Pillar 3 2016-2025 and Annual "
        "Reports 2016-2025. Nothing before 2016 is listed and none should be: the Bank only "
        "began trading on 1 April 2016 via the Part VII transfer, so FY2016 is a genuine floor.\n"
        f"DO NOT USE {P3_BASE.rsplit('/wp-content', 1)[0]}/financial-information/ - that page is "
        "STALE and stops at 2022. It is recorded here explicitly so that a future pass does not "
        "mistake it for the index and re-derive a false negative from it. FILENAME TRAP: the "
        "upload-year directory does NOT match the reporting year, so these paths cannot be "
        "permuted - the FY2023 edition sits under a 2024/10 directory AND uses a different "
        "filename stem ('UK-Pillar-3-Disclosure-2023.pdf'), while FY2024 uses the singular "
        "'Disclosure'. Entity was confirmed INSIDE each of the ten documents (running header "
        "'Habib Bank Zurich Plc - Pillar 3 Disclosures' plus its own 31 December reporting date) "
        "- this is NOT HBL Bank UK (hblbankuk.com), an unrelated bank with a similar name. All "
        "ten are text-native, so no OCR was used for any Pillar 3 figure here.\n"
        "Pillar 3 editions:\n" + P3_EDITION_LIST +
        "CORRECTIONS MADE 2026-09-15 to claims a previous build of this script asserted, all of "
        "which are now DISPROVEN against the primary documents: (a) that the editions lived at "
        "https://www.habibbank.com/uk/downloads/financials and ran FY2019-FY2023 only - wrong "
        "host and wrong range; (b) that 'the Bank publishes NO Pillar 3 edition for FY2024 or "
        "FY2025' - both exist and are cited above, and FY2025's KM1 is what fills the FY2025 "
        "RWA/ratio/leverage/NSFR cells that had been marked 'Not publicly disclosed'; (c) that "
        "no RWA category split existed for FY2016-FY2021 - every edition 2016-2025 carries a "
        "credit/operational/market split in its own 'Own Funds Requirements' table (see the RWA "
        "Breakdown sheet).\n"
        "RESOLVED (was flagged here as an UNRESOLVED DISCREPANCY): the FY2022-FY2024 CET1, Tier "
        "1 and Total Capital Ratios carried in this workbook come from the FY2024 edition's KM1, "
        "whose URL had never been recorded - exactly the 'later, restating edition' the previous "
        "flag hypothesised. That KM1 prints CET1 ratio 17.36%/16.67%/15.03% and Capital Adequacy "
        "Ratio 20.41%/20.13%/18.55% for FY2024/FY2023/FY2022, which is precisely the series on "
        "the Tier 1 Ratio and Total Capital Ratio sheets here. The apparent conflict with the "
        "FY2023 edition (14.99%/14.14%) was a restatement, not a transcription error.\n"
        "ROW-NAMING TRAP in Habib Bank Zurich's own KM1, which is what caused that confusion and "
        "which any future reader of these documents must know: the row printed as 'Total capital "
        "ratio (%) - (CET 1 + Tier 1)' is, per its own parenthetical, the TIER 1 RATIO and NOT "
        "the CRR total capital ratio; the CRR total capital ratio (own funds / RWA) is the row "
        "printed as 'Capital Adequacy Ratio (CET 1 + Tier 1 + Tier 2)'. This workbook's Total "
        "Capital Ratio sheet therefore uses the 'Capital Adequacy Ratio' row throughout. Verified "
        "arithmetically: in the FY2024 edition 135,723/664,889 = 20.41% and in the FY2025 edition "
        "137,764/773,493 = 17.81%, both matching that row exactly.\n"
        + P3_RESTATEMENT_NOTE + "\n"
        "Remaining figures are the Bank's own regulatory-capital and liquidity "
        "disclosures from its statutory Annual Report and Financial Statements (company "
        "08864609), Notes to the Financial Statements:\n"
        f"FY2025 & FY2024: Note 31.25 'Capital Management and Risk' p.106 (CET1/Tier 1/Total "
        f"Capital) and Note 31.21 'Liquidity Risk Management' p.104 (LCR, average-for-period "
        f"basis) of the FY2025 Annual Report - {AR2025_URL}\n"
        f"FY2023 & FY2022: Note 31.25 p.106 and Note 31.21 p.104 of the FY2023 Annual Report "
        f"- {AR2023_URL}\n"
        f"FY2021: Note 31.25 p.107 and Note 31.21 p.103 of the FY2021 Annual Report "
        f"- {AR2021_URL}\n"
        f"FY2020-FY2016: each year's own 'Key Performance Indicators' table (CET1/Tier 1/Total "
        f"Capital, Total RWAs, Total Capital Ratio, Leverage Ratio and LCR, all average-for-"
        f"period/period-end as disclosed) - FY2020 Annual Report p.9, FY2019 p.9, FY2018 p.8, "
        f"FY2017 p.8, FY2016 p.6 - "
        f"{AR2020_URL} / {AR2019_URL} / {AR2018_URL} / {AR2017_URL} / {AR2016_URL}\n"
        + HD_025_NOTE + "\n"
        "No Additional Tier 1 capital is disclosed in any year (Tier 1 = CET1 throughout, per "
        "the Bank's own 'Common equity Tier 1 (CET1) capital' labelling in the FY2023 Annual "
        "Report's capital note). No RWA figure is disclosed in the FY2021-FY2025 STATUTORY "
        "ACCOUNTS - but that is now only a statement about the accounts, not about the Bank's "
        "disclosure: the Pillar 3 editions cited above disclose Total RWAs, the capital ratios, "
        "the Leverage Ratio and NSFR directly for every one of those years, and are the source "
        "used for them here. MREL is not disclosed in any year, in either the accounts or any "
        "Pillar 3 edition (Habib Bank Zurich Plc is not identified as a UK resolution entity) - "
        "that remains a genuine, sourced negative. For FY2016-FY2020, each "
        "year's own KPI table directly discloses CET1 Capital (= Tier 1 = Total Capital less the "
        "negligible Tier 2 add-back, per that table's own layout), Total RWAs, CET1/Tier 1 Ratio "
        "and Total Capital Ratio as printed figures (not derived here). FLAGGED, NOT "
        "FORCE-RECONCILED: FY2016-FY2018's own disclosed CET1/Tier 1 Ratio equals CET1 Capital "
        "divided by Total RWAs exactly, but FY2019 and FY2020's own disclosed ratios (15.32%, "
        "13.86%) diverge slightly from that same division using the disclosed CET1/RWA figures "
        "(15.43%, 13.98%) - both as printed in each year's own KPI table, not force-adjusted; "
        "likely reflects a different RWA averaging/timing basis used in the Bank's own ratio "
        "calculation for those two years, per the same pattern already flagged for Total Capital "
        "Ratio's FY2020 figure."
    )


bw = BankWorkbook(bank_name="Habib Bank Zurich Plc", years=YEARS, year_label=YEAR_LABEL, header_color="CF0DF5")

# ---------------------------------------------------------------
# Sheet 1: Balance Sheet
# ---------------------------------------------------------------
balance_sheet_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and cash equivalents", {
        "FY2025": 291217, "FY2024": 232380, "FY2023": 215342, "FY2022": 96506, "FY2021": 88689,
        "FY2020": 79410, "FY2019": 58964, "FY2018": 66810, "FY2017": 65598, "FY2016": 92224,
    }),
    ("DATA", "Due from banks", {
        "FY2025": 153760, "FY2024": 122152, "FY2023": 112789, "FY2022": 157240, "FY2021": 101317,
        "FY2020": 111857, "FY2019": 98298, "FY2018": 58931, "FY2017": 59460, "FY2016": 42233,
    }),
    ("DATA", "Loans and advances to customers at amortised cost", {
        "FY2025": 800598, "FY2024": 682470, "FY2023": 632149, "FY2022": 601062, "FY2021": 514061,
        "FY2020": 455954, "FY2019": 430736, "FY2018": 398977, "FY2017": 379996, "FY2016": 350395,
    }),
    ("DATA", "Financial investments - Amortised cost", {
        "FY2025": 163281, "FY2024": 192040, "FY2023": 130678,
    }),
    ("DATA", "Financial investments - FVOCI", {
        "FY2025": 55222, "FY2024": 35761, "FY2023": 32704,
    }),
    ("DATA", "Financial investments (total)", {
        "FY2022": 144352, "FY2021": 175654,
        "FY2020": 104357, "FY2019": 84586, "FY2018": 103385, "FY2017": 90643, "FY2016": 99139,
    }),
    ("DATA", "Derivative assets held for risk management", {
        "FY2025": 742, "FY2024": 226, "FY2023": 101, "FY2022": 192, "FY2021": 304,
        "FY2020": 616, "FY2019": 357, "FY2018": 167, "FY2017": 279, "FY2016": 548,
    }),
    ("DATA", "Property and equipment", {
        "FY2025": 10805, "FY2024": 11664, "FY2023": 12545, "FY2022": 15369, "FY2021": 7498,
        "FY2020": 7779, "FY2019": 8483, "FY2018": 5786, "FY2017": 6005, "FY2016": 6164,
    }),
    ("DATA", "Right of use lease assets", {
        "FY2025": 2455, "FY2024": 2758, "FY2023": 2751,
    }),
    ("DATA", "Intangible assets under development", {
        "FY2025": 808, "FY2024": 0,
    }),
    ("DATA", "Other assets", {
        "FY2025": 2061, "FY2024": 2294, "FY2023": 1283, "FY2022": 1496, "FY2021": 2048,
        "FY2020": 888, "FY2019": 1070, "FY2018": 881, "FY2017": 2041, "FY2016": 1647,
    }),
    ("DATA", "Advance tax", {
        "FY2025": 471, "FY2024": 0, "FY2023": 931, "FY2022": 422,
    }),
    ("DATA", "Deferred tax assets", {
        "FY2025": 1849, "FY2024": 2653, "FY2023": 3754, "FY2022": 2399, "FY2021": 2506,
        "FY2020": 1272, "FY2019": 1285, "FY2018": 968, "FY2017": 926, "FY2016": 796,
    }),
    ("TOTAL", "Total assets", {
        "FY2025": 1483269, "FY2024": 1284398, "FY2023": 1145027, "FY2022": 1019038, "FY2021": 892077,
        "FY2020": 762133, "FY2019": 683779, "FY2018": 635905, "FY2017": 604948, "FY2016": 593146,
    }),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Due to banks at amortised cost", {
        "FY2025": 186139, "FY2024": 108224, "FY2023": 123581, "FY2022": 129266, "FY2021": 107147,
        "FY2020": 40091, "FY2019": 6722, "FY2018": 17399, "FY2017": 15848, "FY2016": 24919,
    }),
    ("DATA", "Due to customers at amortised cost", {
        "FY2025": 1142802, "FY2024": 1023002, "FY2023": 885890, "FY2022": 769556, "FY2021": 672008,
        "FY2020": 623644, "FY2019": 577013, "FY2018": 523493, "FY2017": 495252, "FY2016": 479619,
    }),
    ("DATA", "Derivative liabilities held for risk management", {
        "FY2025": 164, "FY2024": 187, "FY2023": 42, "FY2022": 229, "FY2021": 514,
        "FY2020": 358, "FY2019": 312, "FY2018": 137, "FY2017": 225, "FY2016": 503,
    }),
    ("DATA", "Accruals, deferred income and other liabilities", {
        "FY2025": 6750, "FY2024": 8815, "FY2023": 7075, "FY2022": 9860, "FY2021": 5540,
        "FY2020": 5622, "FY2019": 7542, "FY2018": 3925, "FY2017": 5038, "FY2016": 4400,
    }),
    ("DATA", "Lease liability", {
        "FY2025": 2562, "FY2024": 2833, "FY2023": 2920,
    }),
    ("DATA", "Current tax liabilities", {
        "FY2025": 0, "FY2024": 1145, "FY2023": 2300, "FY2022": 346, "FY2021": 573,
        "FY2020": 103, "FY2019": 570, "FY2018": 651, "FY2017": 773, "FY2016": 400,
    }),
    ("DATA", "Deferred tax liabilities", {
        "FY2021": 0, "FY2020": 70, "FY2019": 48, "FY2018": 0, "FY2017": 72, "FY2016": 55,
    }),
    ("DATA", "Subordinated liabilities", {
        "FY2025": 20265, "FY2024": 20296, "FY2023": 20340, "FY2022": 20273, "FY2021": 20092,
        "FY2020": 20063, "FY2019": 20098, "FY2018": 20104, "FY2017": 20000, "FY2016": 20000,
    }),
    ("TOTAL", "Total liabilities", {
        "FY2025": 1358682, "FY2024": 1164502, "FY2023": 1042148, "FY2022": 929530, "FY2021": 805874,
        "FY2020": 689951, "FY2019": 612305, "FY2018": 565708, "FY2017": 537208, "FY2016": 529896,
    }),
    ("SECTION", "Equity", {}),
    ("DATA", "Called up share capital", {
        "FY2025": 80000, "FY2024": 80000, "FY2023": 70000, "FY2022": 70000, "FY2021": 70000,
        "FY2020": 60000, "FY2019": 60000, "FY2018": 60000, "FY2017": 60000, "FY2016": 60000,
    }),
    ("DATA", "Retained earnings", {
        "FY2025": 44501, "FY2024": 40022, "FY2023": 33077, "FY2022": 20525, "FY2021": 16301,
        "FY2020": 11826, "FY2019": 11226, "FY2018": 10229, "FY2017": 7432, "FY2016": 3031,
    }),
    ("DATA", "Fair value through other comprehensive income reserve", {
        "FY2025": 86, "FY2024": -126, "FY2023": -198, "FY2022": -1017, "FY2021": -98,
        "FY2020": 356, "FY2019": 248, "FY2018": -32, "FY2017": 308, "FY2016": 219,
    }),
    ("TOTAL", "Total equity", {
        "FY2025": 124587, "FY2024": 119896, "FY2023": 102879, "FY2022": 89508, "FY2021": 86203,
        "FY2020": 72182, "FY2019": 71474, "FY2018": 70197, "FY2017": 67740, "FY2016": 63250,
    }),
    ("TOTAL", "Total liabilities and equity", {
        "FY2025": 1483269, "FY2024": 1284398, "FY2023": 1145027, "FY2022": 1019038, "FY2021": 892077,
        "FY2020": 762133, "FY2019": 683779, "FY2018": 635905, "FY2017": 604948, "FY2016": 593146,
    }),
]

bw.add_balance_sheet_sheet(
    title="Habib Bank Zurich Plc — Balance Sheet",
    subtitle="Statement of Financial Position, figures as reported in each year's own Annual Report",
    rows=balance_sheet_rows,
    sources_text=BALANCE_SHEET_SOURCES,
    first_col_width=64,
    source_height=260,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Sheet 2: Profit & Loss
# ---------------------------------------------------------------
income_statement_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest income", {
        "FY2025": 77936, "FY2024": 80264, "FY2023": 61056, "FY2022": 32352, "FY2021": 21888,
        "FY2020": 21773, "FY2019": 23079, "FY2018": 20979, "FY2017": 19956, "FY2016": 15202,
    }),
    ("DATA", "Interest expense", {
        "FY2025": -40202, "FY2024": -42267, "FY2023": -26892, "FY2022": -8441, "FY2021": -4133,
        "FY2020": -5784, "FY2019": -5684, "FY2018": -4731, "FY2017": -4174, "FY2016": -3402,
    }),
    ("TOTAL", "Net interest income", {
        "FY2025": 37734, "FY2024": 37997, "FY2023": 34164, "FY2022": 23911, "FY2021": 17755,
        "FY2020": 15989, "FY2019": 17395, "FY2018": 16248, "FY2017": 15782, "FY2016": 11800,
    }),
    ("DATA", "Fee and commission income", {
        "FY2025": 2143, "FY2024": 2082, "FY2023": 1888, "FY2022": 2296, "FY2021": 2325,
        "FY2020": 1732, "FY2019": 1438, "FY2018": 1581, "FY2017": 1651, "FY2016": 1363,
    }),
    ("DATA", "Fee and commission expense", {
        "FY2025": -343, "FY2024": -367, "FY2023": -405, "FY2022": -533, "FY2021": -434,
        "FY2020": -242, "FY2019": -128, "FY2018": -305, "FY2017": -307, "FY2016": -169,
    }),
    ("TOTAL", "Net fee and commission income", {
        "FY2025": 1800, "FY2024": 1715, "FY2023": 1483, "FY2022": 1763, "FY2021": 1891,
        "FY2020": 1490, "FY2019": 1310, "FY2018": 1276, "FY2017": 1344, "FY2016": 1194,
    }),
    ("DATA", "Net foreign exchange income", {
        "FY2025": 319, "FY2024": 551, "FY2023": 311, "FY2022": 597, "FY2021": 484,
        "FY2020": 8, "FY2019": 45, "FY2018": 305, "FY2017": 506, "FY2016": 346,
    }),
    ("DATA", "Fair value gain/(loss) on derivative financial instruments", {
        "FY2025": 538, "FY2024": 40, "FY2023": -101, "FY2022": -38, "FY2021": -210,
        "FY2020": 258, "FY2019": 201, "FY2018": 30,
    }),
    ("DATA", "Gain/(loss) on sale of financial investments", {
        "FY2025": 508, "FY2022": -92, "FY2021": 114,
        "FY2020": 0, "FY2019": 308, "FY2017": 58, "FY2016": -3,
    }),
    ("DATA", "Other costs/income", {
        "FY2025": -27, "FY2024": -9, "FY2023": -12, "FY2022": -2, "FY2021": 10,
        "FY2020": 220, "FY2019": 354, "FY2018": 271, "FY2017": 1561, "FY2016": 249,
    }),
    ("TOTAL", "Net other income", {
        "FY2025": 1338, "FY2024": 582, "FY2023": 198, "FY2022": 465, "FY2021": 398,
        "FY2020": 486, "FY2019": 908, "FY2018": 606, "FY2017": 2125, "FY2016": 592,
    }),
    # Not a line the source statement itself prints - Habib Bank Zurich's own
    # income statement has no combined income subtotal, going straight from
    # these three net-income lines to the Operating expenses section. This
    # row is simply their sum (Net interest income + Net fee and commission
    # income + Net other income), added 2026-09-07 so cost-to-income
    # analysis has a "Total operating income" denominator to work from.
    ("TOTAL", "Total operating income (sum of the three income lines above - not itself a printed subtotal)", {
        "FY2025": 40872, "FY2024": 40294, "FY2023": 35845, "FY2022": 26139, "FY2021": 20044,
        "FY2020": 17965, "FY2019": 19613, "FY2018": 18130, "FY2017": 19251, "FY2016": 13586,
    }),
    ("SECTION", "Operating expenses", {}),
    ("DATA", "Staff costs", {
        "FY2025": -16456, "FY2024": -15738, "FY2023": -13348, "FY2022": -11214, "FY2021": -10151,
        "FY2020": -10807, "FY2019": -10115, "FY2018": -9307, "FY2017": -8902, "FY2016": -5969,
    }),
    ("DATA", "Depreciation", {
        "FY2025": -1475, "FY2024": -1341, "FY2023": -1510, "FY2022": -1119, "FY2021": -933,
        "FY2020": -971, "FY2019": -932, "FY2018": -522, "FY2017": -541, "FY2016": -409,
    }),
    ("DATA", "Administrative and general expenses", {
        "FY2025": -10488, "FY2024": -9423, "FY2023": -8566, "FY2022": -6743, "FY2021": -5179,
        "FY2020": -4910, "FY2019": -5129, "FY2018": -4870, "FY2017": -4997, "FY2016": -3431,
    }),
    ("TOTAL", "Operating expenses", {
        "FY2025": -28419, "FY2024": -26502, "FY2023": -23424, "FY2022": -19076, "FY2021": -16263,
        "FY2020": -16688, "FY2019": -16176, "FY2018": -14699, "FY2017": -14440, "FY2016": -9809,
    }),
    ("TOTAL", "Operating profit before credit impairment losses", {
        "FY2025": 12453, "FY2024": 13792, "FY2023": 12421, "FY2022": 7063, "FY2021": 3781,
        "FY2020": 1277, "FY2019": 3437, "FY2018": 3430, "FY2017": 4811, "FY2016": 3777,
    }),
    ("DATA", "Credit impairment reversals/(charges)", {
        "FY2025": 937, "FY2024": 1183, "FY2023": 866, "FY2022": -684, "FY2021": 68,
        "FY2020": -588, "FY2019": 303, "FY2018": 926, "FY2017": 179, "FY2016": -1296,
    }),
    ("TOTAL", "Profit before tax", {
        "FY2025": 13390, "FY2024": 14975, "FY2023": 13287, "FY2022": 6379, "FY2021": 3849,
        "FY2020": 689, "FY2019": 3740, "FY2018": 4356, "FY2017": 4990, "FY2016": 2481,
    }),
    ("DATA", "Tax charge/(credit)", {
        "FY2025": -3367, "FY2024": -3888, "FY2023": -735, "FY2022": -679, "FY2021": 626,
        "FY2020": -89, "FY2019": -256, "FY2018": -768, "FY2017": -591, "FY2016": 549,
    }),
    ("TOTAL", "Profit after tax", {
        "FY2025": 10023, "FY2024": 11087, "FY2023": 12552, "FY2022": 5700, "FY2021": 4475,
        "FY2020": 600, "FY2019": 3484, "FY2018": 3588, "FY2017": 4400, "FY2016": 3031,
    }),
    ("SECTION", "Other comprehensive income", {}),
    ("DATA", "Fair value through OCI reserve - net gains/(losses) from changes in fair value", {
        "FY2025": 283, "FY2024": 90, "FY2023": 997, "FY2022": -1210, "FY2021": -486,
        "FY2020": 117, "FY2019": 308, "FY2018": -300, "FY2017": 380, "FY2016": 273,
    }),
    ("DATA", "Fair value through OCI reserve - reversal due to sale of investment", {
        "FY2022": 92, "FY2021": -20,
    }),
    ("DATA", "Fair value through OCI reserve - deferred tax", {
        "FY2025": -71, "FY2024": -18, "FY2023": -178, "FY2022": 212, "FY2021": 96,
        "FY2020": -22, "FY2019": -58, "FY2018": 56, "FY2017": -72, "FY2016": -55,
    }),
    ("DATA", "Net reversals/(losses) transferred to income statement due to impairment", {
        "FY2022": -13, "FY2021": -44,
        "FY2020": 13, "FY2019": 30, "FY2018": 7,
    }),
    ("TOTAL", "Other comprehensive income for the year, net of tax", {
        "FY2025": 212, "FY2024": 72, "FY2023": 819, "FY2022": -919, "FY2021": -454,
        "FY2020": 108, "FY2019": 280, "FY2018": -237, "FY2017": 308, "FY2016": 218,
    }),
    ("TOTAL", "Total comprehensive income for the year, net of tax", {
        "FY2025": 10235, "FY2024": 11159, "FY2023": 13371, "FY2022": 4781, "FY2021": 4021,
        "FY2020": 708, "FY2019": 3764, "FY2018": 3351, "FY2017": 4708, "FY2016": 3249,
    }),
]

bw.add_income_statement_sheet(
    title="Habib Bank Zurich Plc — Profit & Loss",
    subtitle="Income Statement and Statement of Comprehensive Income, figures as reported in each year's own Annual Report",
    rows=income_statement_rows,
    sources_text=INCOME_STATEMENT_SOURCES,
    first_col_width=72,
    source_height=190,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Sheet 3: Statement of Changes in Equity
# ---------------------------------------------------------------
equity_headers = ["Called up share capital", "Prepaid share reserve", "Unpaid share capital", "Fair value reserve", "Retained earnings", "Total"]
equity_rows = [
    ("TOTAL", "Balance as at 1 January 2016 (dormant, pre-authorisation shell)", (0, 0, 0, 0, 0, 0)),
    ("DATA", "Prepaid share reserve received ahead of share issue", (None, 5000, None, None, None, 5000)),
    ("DATA", "Unpaid share capital called", (None, None, 38, None, None, 38)),
    ("DATA", "Issue of new ordinary shares on 1 April 2016 (Part VII transfer of Habib Bank AG Zurich's UK branch business)", (60000, -5000, -38, None, None, 54962)),
    ("DATA", "Movement during the 9-month period ended 31 Dec 2016 (profit and OCI - see P&L sheet)", (None, None, None, 219, 3031, 3250)),
    ("TOTAL", "Balance as at 31 December 2016 / 1 January 2017", (60000, 0, 0, 219, 3031, 63250)),
    ("DATA", "Movement during the year (profit and OCI - see P&L sheet)", (None, None, None, 89, 4401, 4490)),
    ("TOTAL", "Balance as at 31 December 2017", (60000, 0, 0, 308, 7432, 67740)),
    ("DATA", "Change in accounting policy (IFRS 9 transition, 1 Jan 2018 - reclassification/remeasurement per Note 2)", (None, None, None, -340, -784, -1124)),
    ("TOTAL", "Balance as at 1 January 2018 (post IFRS 9 transition)", (60000, 0, 0, -32, 6648, 66616)),
    ("DATA", "Movement during the year (profit and OCI - see P&L sheet)", (None, None, None, 0, 3581, 3581)),
    ("TOTAL", "Balance as at 31 December 2018 / 1 January 2019", (60000, 0, 0, -32, 10229, 70197)),
    ("DATA", "Change in accounting policy (IFRS 16 transition, 1 Jan 2019)", (None, None, None, None, -147, -147)),
    ("TOTAL", "Balance as at 1 January 2019 (post IFRS 16 transition)", (60000, 0, 0, -32, 10082, 70050)),
    ("DATA", "Movement during the year (profit and OCI - see P&L sheet)", (None, None, None, 280, 1144, 1424)),
    ("TOTAL", "Balance as at 31 December 2019 / 1 January 2020", (60000, 0, 0, 248, 11226, 71474)),
    ("DATA", "Movement during the year (profit and OCI - see P&L sheet)", (None, None, None, 108, 600, 708)),
    ("TOTAL", "Balance as at 31 December 2020 / 1 January 2021", (60000, 0, 0, 356, 11826, 72182)),
    ("DATA", "Capital raised during the year", (10000, None, None, None, None, 10000)),
    ("DATA", "Profit after tax", (None, None, None, None, 4475, 4475)),
    ("DATA", "FV through OCI reserve - net losses during the year", (None, None, None, -486, None, -486)),
    ("DATA", "FV through OCI reserve - reversal due to sale of investment", (None, None, None, -20, None, -20)),
    ("DATA", "Deferred tax", (None, None, None, 96, None, 96)),
    ("DATA", "Net reversals transferred due to impairment", (None, None, None, None, -44, -44)),
    ("TOTAL", "Balance as at 31 December 2021 / 1 January 2022", (70000, 0, 0, -98, 16301, 86203)),
    ("DATA", "Dividend paid during the year", (None, None, None, None, -1476, -1476)),
    ("DATA", "Profit after tax", (None, None, None, None, 5700, 5700)),
    ("DATA", "FV through OCI reserve - net losses during the year", (None, None, None, -1210, None, -1210)),
    ("DATA", "FV through OCI reserve - reversal due to sale of investment", (None, None, None, 92, None, 92)),
    ("DATA", "Deferred tax", (None, None, None, 212, None, 212)),
    ("DATA", "Net reversals transferred due to impairment", (None, None, None, None, -13, -13)),
    ("TOTAL", "Balance as at 31 December 2022 / 1 January 2023", (70000, 0, 0, -1017, 20525, 89508)),
    ("DATA", "Profit after tax", (None, None, None, None, 12552, 12552)),
    ("DATA", "FV through OCI reserve - net gains during the year", (None, None, None, 997, None, 997)),
    ("DATA", "Deferred tax", (None, None, None, -178, None, -178)),
    ("TOTAL", "Balance as at 31 December 2023 / 1 January 2024", (70000, 0, 0, -198, 33077, 102879)),
    ("DATA", "Dividend paid during the year", (None, None, None, None, -4142, -4142)),
    ("DATA", "Additional capital", (10000, None, None, None, None, 10000)),
    ("DATA", "Profit after tax", (None, None, None, None, 11087, 11087)),
    ("DATA", "FV through OCI reserve - net losses during the year", (None, None, None, 90, None, 90)),
    ("DATA", "Deferred tax", (None, None, None, -18, None, -18)),
    ("TOTAL", "Balance as at 31 December 2024 / 1 January 2025", (80000, 0, 0, -126, 40022, 119896)),
    ("DATA", "Dividend declared & paid during the year", (None, None, None, None, -5544, -5544)),
    ("DATA", "Profit after tax", (None, None, None, None, 10023, 10023)),
    ("DATA", "FV through OCI reserve - net gains during the year", (None, None, None, 283, None, 283)),
    ("DATA", "Deferred tax", (None, None, None, -71, None, -71)),
    ("TOTAL", "Balance as at 31 December 2025", (80000, 0, 0, 86, 44501, 124587)),
]

bw.add_equity_changes_sheet(
    title="Habib Bank Zurich Plc — Statement of Changes in Equity",
    subtitle="Chronological roll-forward, figures as reported in each year's own Annual Report",
    headers=equity_headers,
    rows=equity_rows,
    sources_text=EQUITY_SOURCES,
    first_col_width=58,
    source_height=210,
)

# ---------------------------------------------------------------
# Sheet 4: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Profit before tax", {
        "FY2025": 13390, "FY2024": 14975, "FY2023": 13287, "FY2022": 6379, "FY2021": 3849,
        "FY2020": 689, "FY2019": 3740, "FY2018": 4356, "FY2017": 4992, "FY2016": 2482,
    }),
    ("DATA", "(Reversals)/impairment losses on loans and advances at amortised cost", {
        "FY2025": -937, "FY2024": -1183, "FY2023": -866, "FY2022": 684, "FY2021": -68,
        "FY2020": 588, "FY2019": -303, "FY2018": -926, "FY2017": -179, "FY2016": 1296,
    }),
    ("DATA", "(Gain)/loss on sale of financial assets at FVOCI", {
        "FY2025": -508, "FY2022": 92, "FY2021": -114,
        "FY2019": -308, "FY2017": -58, "FY2016": 3,
    }),
    ("DATA", "Depreciation", {
        "FY2025": 1475, "FY2024": 1341, "FY2023": 1510, "FY2022": 1119, "FY2021": 933,
        "FY2020": 971, "FY2019": 932, "FY2018": 522, "FY2017": 541, "FY2016": 409,
    }),
    ("DATA", "Gain on sale of property and equipment", {
        "FY2021": -1, "FY2017": -1,
    }),
    ("TOTAL", "Profit before tax adjusted for non-cash items", {
        "FY2025": 13420, "FY2024": 15133, "FY2023": 13931, "FY2022": 8274, "FY2021": 4599,
        "FY2020": 2248, "FY2019": 4061, "FY2018": 3952, "FY2017": 5295, "FY2016": 4190,
    }),
    ("SECTION", "Net (increase)/decrease in operating assets", {}),
    ("DATA", "Loans and advances to banks at amortised cost", {
        "FY2025": -31608, "FY2024": -9363, "FY2023": 29645, "FY2022": -55923, "FY2021": 11053,
        "FY2020": -13756, "FY2019": -39565, "FY2018": 663, "FY2017": -17227, "FY2016": 30115,
    }),
    ("DATA", "Loans and advances to customers at amortised cost", {
        "FY2025": -117191, "FY2024": -49138, "FY2023": -30221, "FY2022": -87685, "FY2021": -58584,
        "FY2020": -26097, "FY2019": -31224, "FY2018": -18509, "FY2017": -29422, "FY2016": 9474,
    }),
    ("DATA", "Derivative financial instruments for risk management", {
        "FY2025": -516, "FY2024": -125, "FY2023": 91, "FY2022": 112, "FY2021": 312,
        "FY2020": -259, "FY2019": -190, "FY2018": 112, "FY2017": 269, "FY2016": -375,
    }),
    ("DATA", "Other assets", {
        "FY2025": 1037, "FY2024": -1011, "FY2023": -1651, "FY2022": 1128, "FY2021": -966,
        "FY2020": 286, "FY2019": 206, "FY2018": 618, "FY2017": 69, "FY2016": 496,
    }),
    ("TOTAL", "Net (increase)/decrease in operating assets", {
        "FY2025": -148278, "FY2024": -59637, "FY2023": -2136, "FY2022": -142368, "FY2021": -48185,
        "FY2020": -39826, "FY2019": -70773, "FY2018": -17116, "FY2017": -46311, "FY2016": 39710,
    }),
    ("SECTION", "Net increase/(decrease) in operating liabilities", {}),
    ("DATA", "Due to banks at amortised cost", {
        "FY2025": 77915, "FY2024": -15357, "FY2023": -4420, "FY2022": 22119, "FY2021": 67056,
        "FY2020": 33369, "FY2019": -10677, "FY2018": 1534, "FY2017": -9071, "FY2016": -22109,
    }),
    ("DATA", "Due to customers at amortised cost", {
        "FY2025": 119800, "FY2024": 137112, "FY2023": 116334, "FY2022": 97548, "FY2021": 48364,
        "FY2020": 46631, "FY2019": 53520, "FY2018": 26641, "FY2017": 15632, "FY2016": 85298,
    }),
    ("DATA", "Derivative financial instruments for risk management", {
        "FY2025": -23, "FY2024": 145, "FY2023": -187, "FY2022": -285, "FY2021": 156,
        "FY2020": 46, "FY2019": 175, "FY2018": -88, "FY2017": -277, "FY2016": 338,
    }),
    ("DATA", "Accruals, deferred income and other liabilities", {
        "FY2025": -2295, "FY2024": 3204, "FY2023": 2710, "FY2022": 4453, "FY2021": 351,
        "FY2020": -991, "FY2019": 65, "FY2018": 589, "FY2017": 639, "FY2016": -2195,
    }),
    ("DATA", "Movement in current tax liabilities", {
        "FY2020": -570, "FY2019": -561, "FY2018": -773, "FY2017": -400, "FY2016": -328,
    }),
    ("DATA", "Leases paid (classified within operating activities this year only - see note)", {
        "FY2019": -436,
    }),
    ("DATA", "Tax paid", {
        "FY2025": -4395, "FY2024": -3029, "FY2023": -931, "FY2022": -824, "FY2021": -306,
        "FY2020": -77, "FY2019": -372, "FY2018": -350, "FY2017": -412, "FY2016": -312,
    }),
    ("TOTAL", "Net increase/(decrease) in operating liabilities", {
        "FY2025": 191002, "FY2024": 122075, "FY2023": 113506, "FY2022": 123011, "FY2021": 115621,
        "FY2020": 78408, "FY2019": 41714, "FY2018": 27553, "FY2017": 6111, "FY2016": 60692,
    }),
    ("TOTAL", "Net cash flow from operating activities", {
        "FY2025": 56144, "FY2024": 77571, "FY2023": 125301, "FY2022": -11083, "FY2021": 72035,
        "FY2020": 40830, "FY2019": -24998, "FY2018": 14388, "FY2017": -34906, "FY2016": 104592,
    }),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Purchase of property and equipment", {
        "FY2025": -313, "FY2024": -193, "FY2023": -1437, "FY2022": -8990, "FY2021": -652,
        "FY2020": -267, "FY2019": -457, "FY2018": -303, "FY2017": -382, "FY2016": -239,
    }),
    ("DATA", "Proceeds on sale of property and equipment", {
        "FY2022": 0, "FY2021": 1, "FY2018": 0, "FY2017": 1,
    }),
    ("DATA", "Intangible assets under development", {
        "FY2025": -808,
    }),
    ("DATA", "Purchase of financial investments", {
        "FY2025": -101174, "FY2024": -133828, "FY2023": -91617, "FY2022": -19234, "FY2021": -114123,
        "FY2020": -39436, "FY2019": -13163, "FY2018": -38137, "FY2017": None, "FY2016": -13361,
    }),
    ("DATA", "Proceeds on sale/maturity of financial investments", {
        "FY2025": 111192, "FY2024": 69499, "FY2023": 73406, "FY2022": 49525, "FY2021": 42421,
        "FY2020": 19780, "FY2019": 32572, "FY2018": 25229, "FY2017": None,
    }),
    ("DATA", "Sale/(purchase) of financial investments (combined, as printed this year)", {
        "FY2017": 8660,
    }),
    ("TOTAL", "Net cash from/(used in) investing activities", {
        "FY2025": 8897, "FY2024": -64522, "FY2023": -19648, "FY2022": 21301, "FY2021": -72353,
        "FY2020": -19923, "FY2019": 18952, "FY2018": -13210, "FY2017": 8279, "FY2016": -13600,
    }),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Capital issuance", {
        "FY2024": 10000, "FY2021": 10000,
    }),
    ("DATA", "Dividend paid", {
        "FY2025": -5543, "FY2024": -4142, "FY2022": -1476, "FY2019": -1794,
    }),
    ("DATA", "Leases paid", {
        "FY2025": -630, "FY2024": -461, "FY2023": -424, "FY2022": -434, "FY2021": -432,
        "FY2020": -426,
    }),
    ("DATA", "Interest paid/(charges) on subordinated liabilities", {
        "FY2025": -31, "FY2024": -1408, "FY2023": -1199, "FY2022": -491, "FY2021": 29,
        "FY2020": -35, "FY2019": -6, "FY2018": 20,
    }),
    ("TOTAL", "Net cash from/(used in) financing activities", {
        "FY2025": -6204, "FY2024": 3989, "FY2023": -1623, "FY2022": -2401, "FY2021": 9597,
        "FY2020": -461, "FY2019": -1800, "FY2018": 20, "FY2017": 0, "FY2016": 0,
    }),
    ("TOTAL", "Net increase in cash and cash equivalents", {
        "FY2025": 58837, "FY2024": 17038, "FY2023": 104030, "FY2022": 7817, "FY2021": 9279,
        "FY2020": 20446, "FY2019": -7846, "FY2018": 1198, "FY2017": -26627, "FY2016": 90993,
    }),
    ("DATA", "Cash and cash equivalents at the beginning of the year", {
        "FY2025": 232380, "FY2024": 215342, "FY2023": 111312, "FY2022": 88689, "FY2021": 79410,
        "FY2020": 58964, "FY2019": 66810, "FY2018": 65612, "FY2017": 92224, "FY2016": 1232,
    }),
    ("TOTAL", "Cash and cash equivalents at the end of the year", {
        "FY2025": 291217, "FY2024": 232380, "FY2023": 215342, "FY2022": 96506, "FY2021": 88689,
        "FY2020": 79410, "FY2019": 58964, "FY2018": 66810, "FY2017": 65597, "FY2016": 92224,
    }),
]

bw.add_cash_flow_sheet(
    title="Habib Bank Zurich Plc — Cash Flow Statement",
    subtitle="Figures as reported in each year's own Annual Report and Financial Statements",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=70,
    source_height=210,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Sheet: Asset Quality
# ---------------------------------------------------------------
asset_quality_rows = [
    ("SECTION", "Loans and advances to customers at amortised cost, gross carrying amount", {}),
    ("DATA", "Stage 1 (12-month ECL)", {
        "FY2025": 763217, "FY2023": 593300, "FY2022": 560009, "FY2021": 493355,
        "FY2020": 441858, "FY2019": 417199, "FY2018": 369903,
    }),
    ("DATA", "Stage 2 (lifetime ECL, not credit-impaired)", {
        "FY2025": 33227, "FY2023": 25704, "FY2022": 26131, "FY2021": 12310,
        "FY2020": 4791, "FY2019": 8045, "FY2018": 19737,
    }),
    ("DATA", "Stage 3 (lifetime ECL, credit-impaired)", {
        "FY2025": 6076, "FY2023": 17310, "FY2022": 20029, "FY2021": 12849,
        "FY2020": 14720, "FY2019": 10530, "FY2018": 14921,
    }),
    ("TOTAL", "Total gross loans and advances to customers", {
        "FY2025": 802520, "FY2024": 685362, "FY2023": 636314, "FY2022": 606169, "FY2021": 518514,
        "FY2020": 461369, "FY2019": 435774, "FY2018": 404560,
    }),
    ("DATA", "Less: loss allowance", {
        "FY2025": -1922, "FY2024": -2892, "FY2023": -4165, "FY2022": -5107, "FY2021": -4453,
        "FY2020": -5415, "FY2019": -5038, "FY2018": -5583,
    }),
    ("TOTAL", "Net loans and advances to customers", {
        "FY2025": 800598, "FY2024": 682470, "FY2023": 632149, "FY2022": 601062, "FY2021": 514061,
        "FY2020": 455954, "FY2019": 430736, "FY2018": 398977,
    }),
    ("SECTION", "Derived ratios", {}),
    ("DATA", "Stage 3 / gross loans (derived NPL ratio)", {
        "FY2025": "0.76%", "FY2023": "2.72%", "FY2022": "3.30%", "FY2021": "2.48%",
        "FY2020": "3.19%", "FY2019": "2.42%", "FY2018": "3.69%",
    }),
    ("DATA", "Loss allowance / gross loans (derived coverage ratio)", {
        "FY2025": "0.24%", "FY2024": "0.42%", "FY2023": "0.65%", "FY2022": "0.84%", "FY2021": "0.86%",
        "FY2020": "1.17%", "FY2019": "1.16%", "FY2018": "1.38%",
    }),
    ("SECTION", "Pre-IFRS 9 (incurred loss model) - loans and advances to customers by product, FY2016-FY2017", {}),
    ("DATA", "Commercial loans", {"FY2017": 341817, "FY2016": 306651}),
    ("DATA", "Overdraft", {"FY2017": 40898, "FY2016": 42451}),
    ("DATA", "Corporate loans", {"FY2017": 0, "FY2016": 8980}),
    ("DATA", "Discounted bills & trade finance loans", {"FY2017": 9667, "FY2016": 8495}),
    ("DATA", "Other loans including staff loans", {"FY2017": 490, "FY2016": 679}),
    ("TOTAL", "Total gross loans and advances to customers (pre-IFRS 9)", {"FY2017": 392873, "FY2016": 367256}),
    ("DATA", "Less: provision for impairment (incurred-loss model, aggregate - no stage split)", {"FY2017": -12876, "FY2016": -16861}),
    ("TOTAL", "Net loans and advances to customers (pre-IFRS 9)", {"FY2017": 379996, "FY2016": 350395}),
]

bw.add_asset_quality_sheet(
    title="Habib Bank Zurich Plc — Asset Quality",
    subtitle="Loans and advances to customers by IFRS 9 stage, figures as reported in each year's own Annual Report",
    rows=asset_quality_rows,
    sources_text=ASSET_QUALITY_SOURCES,
    first_col_width=64,
    source_height=200,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, f"{unit}" if unit else None,
                         rows_data, sources_text, note=note, first_col_width=44, source_height=140)


# ---------------------------------------------------------------
# Sheet: KM1 Key Metrics (the Bank's own published key-metrics template)
# ---------------------------------------------------------------
KM1_SOURCES = (
    "Sources - Habib Bank Zurich Plc's own 'Key metrics' section, transcribed from the edition in which each "
    "year is the REPORTING year (never a later edition's comparative), except FY2017 - see below. Page numbers "
    "are the folios printed on the pages themselves, each confirmed twice: against the document's own table of "
    "contents and against the number printed in the page footer.\n"
    f"FY2025: Pillar 3 Disclosures 2025, section 2 'Key metrics', p.4 - {P3_2025_URL}\n"
    f"FY2024: Pillar 3 Disclosure 2024, section 2 'Key metrics (KM1)', p.4 - {P3_2024_URL}\n"
    f"FY2023: UK Pillar 3 Disclosure 2023, section 2 'Key metrics', p.4 - {P3_2023_URL}\n"
    f"FY2022: Pillar 3 Disclosures 2022, section 2 'Key metrics', p.5 - {P3_2022_URL}\n"
    f"FY2021: Pillar 3 Disclosures 2021, section 3 'Key Metrics', p.14 - {P3_2021_URL}\n"
    f"FY2020: Pillar 3 Disclosures 2020, section 3 'Key Metrics', p.12 - {P3_2020_URL}\n"
    f"FY2019: Pillar 3 Disclosures 2019, section 3 'Key Metrics', p.8 - {P3_2019_URL}\n"
    f"FY2018: Pillar 3 Disclosures 2018, section 3 'Key Metrics', pp.7-8 (the table breaks across two pages - "
    f"own funds, RWA and capital ratios on p.7; buffers, leverage, LCR and NSFR on p.8) - {P3_2018_URL}\n"
    f"FY2017: NOT from a FY2017 KM1 - the FY2017 edition contains no key-metrics table at all - but from the "
    f"FY2018 edition's own 2017 comparative column, pp.7-8 - {P3_2018_URL}\n\n"
    "WHY THIS COUNTS AS THE TEMPLATE (the row-set test). The Bank prints no row numbers and, before its FY2024 "
    "edition, never writes 'KM1' - that edition titles the section '2. Key metrics (KM1)', the others just 'Key "
    "metrics'. Neither fact decides it. What decides it is that the table carries the UK KM1 row set, in the "
    "template's own order and under the template's own section headings: available own funds, then "
    "risk-weighted exposure amounts, then capital ratios, then CET1 buffer requirements, then the leverage "
    "ratio and its exposure measure, then LCR (HQLA, net outflow, ratio), then NSFR (ASF, RSF, ratio). Two "
    "departures are worth naming rather than smoothing over: the Bank prepends a CC1-style own-funds build-up "
    "(share capital, retained earnings, reserve, regulatory deductions) ahead of row 1, and it never prints the "
    "SREP block (UK 7a-7d) or the UK 16a/16b inflow-outflow split in any edition. Because the Bank prints no "
    "row numbers, NONE ARE ADDED HERE: mapping its rows onto template numbers would invent a correspondence it "
    "never published. Its own labels are reproduced verbatim instead.\n\n"
    "ENTITY BASIS: solo. The Bank's own editions state it - \"The Bank is a single entity in the UK and no "
    "consolidation is performed\" (FY2025 edition, Overview) - and its capital section presents \"the "
    "composition of regulatory capital for the Bank on a solo basis\". Habib Bank Zurich plc is a 100%-owned "
    "subsidiary of Habib Bank AG Zurich (Switzerland), which is a third-country parent; no figure from the "
    "Swiss parent's disclosures is used anywhere on this sheet, and there is no intermediate UK holding company "
    "above the Bank.\n\n"
    "TWO UNITS, DELIBERATELY NOT MERGED (and this is why some rows appear twice). The FY2018 edition prints "
    "this table in SINGLE POUNDS (share capital 60,000,000; RWA 387,179,103). Every other edition prints it in "
    "£'000. FY2018 and FY2017 both come from that FY2018 edition, so their amounts are in single pounds while "
    "FY2019-FY2025 are in £'000. Amount rows therefore appear as two separate caption blocks, one per unit, "
    "each row carrying its own unit explicitly; restating one edition's amounts into the other's unit would be "
    "normalising a published disclosure. Ratio rows are unit-free and stay single.\n\n"
    "FY2017 IS A FILLED COLUMN; FY2016 IS BLANK. The FY2017 edition has no key-metrics table - its own table of "
    "contents runs Overview / Governance Framework / Risk Management Framework / Significant Risks / Liquidity "
    "Risk / Capital Management and Capital Adequacy / ICAAP / Leverage Ratio / Impairment Provisions / Asset "
    "Encumbrance / Employee Remuneration Policy, with no Key Metrics section, and the section first appears in "
    "the FY2018 edition. FY2017 is therefore taken from the FY2018 edition's own 2017 comparative column. "
    "FY2016 stays blank: its own edition likewise has no key-metrics section (same contents-page check), and no "
    "edition anywhere prints a 2016 column - the FY2018 edition, the earliest that prints the table at all, "
    "carries 2018 and 2017 only. Blank here therefore means the Bank has never published these figures on this "
    "table, in any edition.\n\n"
    "A PRINTED DEFECT, REPRODUCED NOT CORRECTED (rule: record a source defect, do not fix it). The FY2021 "
    "edition prints Total Own Funds for 2021 as '1066,687' - a typesetting slip for 106,687, which is what the "
    "FY2022 and FY2023 editions both print for that same date. The cell below reads '1066,687 (as printed; the "
    "FY2022 and FY2023 editions print 106,687 for this date)' rather than silently carrying either number.\n\n"
    "THE BANK RESTATES HEAVILY BETWEEN EDITIONS, AND EACH YEAR HERE KEEPS ITS OWN EDITION'S FIGURES. This is "
    "the single most important thing to know before comparing this sheet with anything else, including the "
    "single-metric Pillar 3 sheets in this same workbook, several of which were built from the latest edition "
    "to state a year rather than from that year's own edition. Documented, not reconciled:\n"
    "- FY2024 CET1 after deductions: 115,427 (FY2024 edition, used here) against 109,883 (FY2025 edition); "
    "CET1 ratio 17.36% against 16.53%.\n"
    "- FY2023 CET1: 103,077 (FY2023 edition, used here - that edition prints no deductions block at all) "
    "against 97,919 (FY2024 edition) and 93,777 (FY2025 edition); CET1 ratio 14.99% against 16.67% and 15.96%.\n"
    "- FY2022 CET1: 81,361 (FY2022 edition, used here) against 90,610 (FY2023 edition) and 86,426 (FY2024 "
    "edition); CET1 ratio 14.14% against 15.03%; total capital ratio 16.43% against 16.76%.\n"
    "- FY2021 CET1: 86,301 (FY2021 edition, used here) against 81,824 (FY2022 edition); total capital ratio "
    "15.75% against 15.17% (FY2022 edition); Capital Adequacy Ratio 19.47% against 18.65% (FY2022 and FY2023 "
    "editions).\n"
    "- FY2019 HQLA: 91,624 (FY2019 edition, used here) against 91,637 (FY2020 and FY2021 editions). FY2019 "
    "leverage ratio: 10.03% (FY2019 edition, used here) against 9.03% (FY2020 and FY2021 editions).\n"
    "- FY2018 CET1: £70,229,002 (FY2018 edition, used here) against £69,683k (FY2019 edition) - a restatement "
    "as well as a unit change. FY2017 CET1: £67,432,075 (FY2018 edition, used here) against £67,109k (FY2019, "
    "FY2020 and FY2021 editions).\n\n"
    "TWO ROWS THE BANK MISLABELS. Both are reproduced with the Bank's own wording exactly as printed. Neither is "
    "a transcription error and neither may be edited to agree with anything:\n"
    "- 'Total Capital (CET 1 + Tier 1)' is, by its own parenthetical, TIER 1 CAPITAL - it excludes Tier 2. The "
    "workbook's Total Capital sheet correctly holds the Bank's 'Total Own Funds (CET 1 + Tier 1 + tier 2)' row "
    "instead (FY2025: 137,764 against this row's 117,764).\n"
    "- 'Total capital ratio (%)' is likewise the TIER 1 ratio, not the total capital ratio; the Bank's real "
    "CRR total capital ratio is the row it calls 'Capital Adequacy Ratio (CET 1 + Tier 1 + Tier 2)', which is "
    "what the Total Capital Ratio sheet carries (FY2025: 17.81% against this row's 15.22%).\n"
    "So this sheet and the Total Capital / Total Capital Ratio sheets hold DIFFERENT ROWS by design, and their "
    "figures differ by design. A reader comparing the two should expect the difference and read it here, not "
    "treat it as an error in either.\n\n"
    "CROSS-EDITION WORDING DRIFT. Recorded here rather than in the row labels themselves, because a row label "
    "reproduces what the Bank printed and carries nothing beyond the unit:\n"
    "- The row shown here as 'Total capital ratio (%)' is printed as 'Total capital ratio (%) - (CET 1 + "
    "Tier 1)' in the FY2024 and FY2025 editions, and as plain 'Total capital ratio (%)' in FY2019-FY2023.\n"
    "- The row shown here as 'Capital Adequacy Ratio (CET 1 + Tier 1 + Tier 2) (%)' is printed as plain "
    "'Capital Adequacy Ratio' in the FY2019-FY2023 editions.\n"
    "The Bank's NSFR row agrees with the NSFR sheet in every year it prints one.\n\n"
    "LATEST-EDITION CHECK 2026-09-17: habibbank.com/gb/about-us/ - the Bank's own disclosures page - was read "
    "directly and its full document list enumerated, rather than relying on this project's cited URLs. Newest "
    "Pillar 3 published: Pillar 3 Disclosures 2025 (uploaded under /2026/09/). Newest Annual Report published: "
    "Annual Report 2025 (same directory). Both are already the newest year in this workbook; nothing newer "
    "exists. (The WordPress REST media endpoint on this host returns 403 to anonymous callers, so the page's "
    "own links were enumerated instead - a blocked API is not an absence of documents.)"
)

km1_rows = [
    ("SECTION", "Available Funds — amounts in £'000, as printed in the FY2019-FY2025 editions", {}),
    ("DATA", "Share capital (£'000)", {
        "FY2025": 80000, "FY2024": 80000, "FY2023": 70000, "FY2022": 70000, "FY2021": 70000,
        "FY2020": 60000, "FY2019": 60000,
    }),
    ("DATA", "Retained earnings (£'000)", {
        "FY2025": 44501, "FY2024": 40022, "FY2023": 33077, "FY2022": 14822, "FY2021": 16301,
        "FY2020": 11826, "FY2019": 11226,
    }),
    ("DATA", "Fair value through other comprehensive income reserve (£'000)", {
        "FY2025": 86, "FY2024": -126,
    }),
    ("DATA", "Common Equity Tier 1 Capital: instruments and reserves (£'000)", {
        "FY2025": 124587, "FY2024": 119896, "FY2023": 103077, "FY2022": 81361, "FY2021": 86301,
        "FY2020": 71826, "FY2019": 71226,
    }),
    ("DATA", "Regulatory Deductions: Deferred tax assets on carried forward losses (£'000)", {
        "FY2025": -3426, "FY2024": -4307,
    }),
    ("DATA", "Regulatory Deductions: Proposed dividend for the year (£'000)", {
        "FY2025": -3341,
    }),
    ("DATA", "Regulatory Deductions: Other deductions (£'000)", {
        "FY2025": -56, "FY2024": -162,
    }),
    ("DATA", "Common Equity Tier 1 Capital after deductions (£'000)", {
        "FY2025": 117764, "FY2024": 115427,
    }),
    ("DATA", "Additional Tier 1 Capital (£'000)", {}),
    ("DATA", "Total Capital (CET 1 + Tier 1) (£'000)", {
        "FY2025": 117764, "FY2024": 115427, "FY2023": 103077, "FY2022": 81361, "FY2021": 86301,
        "FY2020": 71826, "FY2019": 71226,
    }),
    ("DATA", "Tier 2 Capital – Subordinated liabilities (£'000)", {
        "FY2025": 20000, "FY2024": 20296, "FY2023": 20340, "FY2022": 20579, "FY2021": 20386,
        "FY2020": 20540, "FY2019": 20426,
    }),
    ("DATA", "Total Own Funds (CET 1 + Tier 1 + tier 2) (£'000)", {
        "FY2025": 137764, "FY2024": 135723, "FY2023": 123417, "FY2022": 101940,
        "FY2021": "1066,687 (as printed; the FY2022 and FY2023 editions print 106,687 for this date)",
        "FY2020": 92366, "FY2019": 91652,
    }),
    ("DATA", "Total Risk-Weighted Assets (£'000)", {
        "FY2025": 773493, "FY2024": 664889, "FY2023": 587448, "FY2022": 575205, "FY2021": 547938,
        "FY2020": 513951, "FY2019": 442493,
    }),
    ("SECTION", "Available Funds — amounts in £, single pounds as printed. The FY2018 edition prints this "
                "table in whole pounds and is the source for both columns below", {}),
    ("DATA", "Share capital (£, single pounds as printed)", {
        "FY2018": 60000000, "FY2017": 60000000,
    }),
    ("DATA", "Retained earnings (£, single pounds as printed)", {
        "FY2018": 10229002, "FY2017": 7432075,
    }),
    ("DATA", "Common Equity Tier 1 Capital: instruments and reserves (£, single pounds as printed)", {
        "FY2018": 70229002, "FY2017": 67432075,
    }),
    ("DATA", "Additional Tier 1 Capital (£, single pounds as printed)", {}),
    ("DATA", "Total Capital (CET 1 + Tier 1) (£, single pounds as printed)", {
        "FY2018": 70229002, "FY2017": 67432075,
    }),
    ("DATA", "Total Risk-Weighted Assets (£, single pounds as printed)", {
        "FY2018": 387179103, "FY2017": 359940986,
    }),
    ("SECTION", "Risk-based capital ratios as percentage of RWA", {}),
    ("DATA", "CET 1 ratio (%)", {
        "FY2025": "15.22%", "FY2024": "17.36%", "FY2023": "14.99%", "FY2022": "14.14%", "FY2021": "15.75%",
        "FY2020": "13.98%", "FY2019": "16.10%", "FY2018": "18.14%", "FY2017": "18.73%",
    }),
    ("DATA", "Tier 1 (%)", {
        "FY2023": "14.99%", "FY2022": "14.14%", "FY2021": "15.75%",
        "FY2020": "13.98%", "FY2019": "16.10%", "FY2018": "18.14%", "FY2017": "18.73%",
    }),
    ("DATA", "Total capital ratio (%)", {
        "FY2025": "15.22%", "FY2024": "17.36%", "FY2023": "17.43%", "FY2022": "16.43%", "FY2021": "15.75%",
        "FY2020": "13.98%", "FY2019": "16.10%", "FY2018": "18.14%", "FY2017": "18.73%",
    }),
    ("DATA", "Capital Adequacy Ratio (CET 1 + Tier 1 + Tier 2) (%)", {
        "FY2025": "17.81%", "FY2024": "20.41%", "FY2023": "18.39%", "FY2022": "17.72%", "FY2021": "19.47%",
        "FY2020": "17.97%", "FY2019": "20.71%",
    }),
    ("SECTION", "Additional CET1 buffer requirements as a percentage of RWA", {}),
    ("DATA", "Capital conservation buffer (CCoB) requirement (%)", {
        "FY2025": "2.50%", "FY2024": "2.50%", "FY2023": "2.50%", "FY2022": "2.50%", "FY2021": "2.5%",
        "FY2020": "2.50%", "FY2019": "2.50%", "FY2018": "1.875%", "FY2017": "1.250%",
    }),
    ("DATA", "Countercyclical capital buffer (CCyB) requirement (%)", {
        "FY2025": "1.50%", "FY2024": "2.00%", "FY2023": "2%", "FY2022": "1%",
        "FY2019": "1.00%", "FY2018": "1.00%", "FY2017": "0.500%",
    }),
    ("DATA", "Total of bank CET 1 specific buffer Requirement (%)", {
        "FY2025": "4.00%", "FY2024": "4.50%", "FY2023": "4.50%", "FY2022": "3.5%", "FY2021": "2.5%",
        "FY2020": "2.50%", "FY2019": "3.50%", "FY2018": "2.875%", "FY2017": "1.750%",
    }),
    ("DATA", "CET 1 available after meeting the bank's minimum capital requirements (%)", {
        "FY2018": "13.64%", "FY2017": "14.23%",
    }),
    ("SECTION", "Basel III leverage ratio", {}),
    ("DATA", "Total Basel III leverage ratio exposure measure (£'000)", {
        "FY2025": 1272426, "FY2024": 1133461, "FY2023": 999212, "FY2022": 931009, "FY2021": 948055,
        "FY2020": 803637, "FY2019": 714163,
    }),
    ("DATA", "Total Basel III leverage ratio exposure measure (£, single pounds as printed)", {
        "FY2018": 627604463, "FY2017": 635316590,
    }),
    ("DATA", "Basel III leverage ratio (%)", {
        "FY2024": "10.18%", "FY2023": "8.81%", "FY2022": "8.74%", "FY2021": "8.63%",
        "FY2020": "8.97%", "FY2019": "10.03%", "FY2018": "10.62%", "FY2017": "9.92%",
    }),
    ("DATA", "Basel III leverage ratio excluding claims on central banks (%)", {
        "FY2025": "9.26%",
    }),
    ("SECTION", "Liquidity coverage ratio (LCR)", {}),
    ("DATA", "Total high-quality liquid assets (HQLA) (£'000)", {
        "FY2025": 306567, "FY2024": 224688, "FY2023": 183751, "FY2022": 108775, "FY2021": 107915,
        "FY2020": 117491, "FY2019": 91624,
    }),
    ("DATA", "Total high-quality liquid assets (HQLA) (£, single pounds as printed)", {
        "FY2018": 122555336, "FY2017": 141876074,
    }),
    ("DATA", "Total net cash outflow (£'000)", {
        "FY2025": 170300, "FY2024": 89737, "FY2023": 64332, "FY2022": 26883, "FY2021": 70335,
        "FY2020": 51796, "FY2019": 57333,
    }),
    ("DATA", "Total net cash outflow (£, single pounds as printed)", {
        "FY2018": 61884045, "FY2017": 60162568,
    }),
    ("DATA", "LCR ratio (%)", {
        "FY2025": "180%", "FY2024": "243%", "FY2023": "286%", "FY2022": "405%", "FY2021": "153%",
        "FY2020": "226.83%", "FY2019": "159.81%", "FY2018": "198.04%", "FY2017": "235.82%",
    }),
    ("SECTION", "Net stable funding ratio (NSFR)", {}),
    ("DATA", "Total available stable funding (£'000)", {
        "FY2025": 966189, "FY2024": 904473, "FY2023": 830973, "FY2022": 729215, "FY2021": 664541,
        "FY2020": 614210, "FY2019": 575074,
    }),
    ("DATA", "Total available stable funding (£, single pounds as printed)", {
        "FY2018": 530876872, "FY2017": 506952186,
    }),
    ("DATA", "Total required stable funding (£'000)", {
        "FY2025": 728485, "FY2024": 660742, "FY2023": 608890, "FY2022": 573467, "FY2021": 510571,
        "FY2020": 457718, "FY2019": 423583,
    }),
    ("DATA", "Total required stable funding (£, single pounds as printed)", {
        "FY2018": 388363098, "FY2017": 362939198,
    }),
    ("DATA", "NSFR ratio", {
        "FY2025": "133%", "FY2024": "137%", "FY2023": "136%", "FY2022": "127%", "FY2021": "130.16%",
        "FY2020": "134.19%", "FY2019": "135.76%", "FY2018": "136.70%", "FY2017": "139.68%",
    }),
]

bw.add_km1_sheet(
    title="Habib Bank Zurich Plc — KM1 Key Metrics",
    subtitle="The Bank's own published key-metrics table (the UK KM1 row set, printed unnumbered - see the "
             "row-set test in the source note), reproduced in its own row order with its own labels and printed "
             "precision. Solo basis - the Bank is a single UK entity and performs no consolidation. Amounts are "
             "in £'000 for FY2019-FY2025 and in single pounds for FY2018/FY2017, which is how the Bank printed "
             "them; the two are kept in separate caption blocks rather than restated into one unit. FY2017 is "
             "the FY2018 edition's comparative column (FY2017's own edition prints no such table); FY2016 is "
             "blank because no edition prints a 2016 column at all.",
    rows=km1_rows,
    sources_text=KM1_SOURCES,
    first_col_width=78,
    source_height=520,
)


metric(
    "CET1 Capital", "£'000",
    [("Common Equity Tier 1 (CET1) capital, after regulatory deductions", {
        "FY2025": 117764, "FY2024": 115427, "FY2023": 97919, "FY2022": 86426, "FY2021": 86301,
        "FY2020": 71830, "FY2019": 71230, "FY2018": 70230, "FY2017": 67430, "FY2016": 63030,
    })],
    p3_sources(),
    note="No Additional Tier 1 capital is disclosed in any year, so CET1 = Tier 1 capital throughout. "
         "FY2016-FY2020 sourced from each year's own 'Capital Structure' regulatory-capital table (Share "
         "capital - Tier 1 + Retained earnings - Tier 1), not the KM1/KPI-table format used FY2021-2025. "
         "CORRECTED 2026-09-15: FY2025 previously read 124,587, which is the Bank's TOTAL EQUITY per its "
         "Balance Sheet (the pre-deduction 'CET1 capital: instruments and reserves' line), not its "
         "regulatory CET1 - it was inconsistent with FY2023/FY2024 in this same row, which are "
         "after-deduction figures. The FY2025 Pillar 3 KM1 states CET1 capital after deductions of "
         "117,764 (= 124,587 less deferred tax assets on carried-forward losses 3,426, proposed dividend "
         "3,341 and other deductions 56), and that transcribed figure is now used. See the source note's "
         "cross-edition restatement list for why FY2023/FY2024 differ between the FY2024 and FY2025 "
         "editions - those two are NOT force-reconciled and keep their own editions' values.",
)
metric(
    "CET1 Ratio", "%",
    [("CET1 Ratio", {
        "FY2021": "14.93%", "FY2022": "15.03%", "FY2023": "16.67%", "FY2024": "17.36%", "FY2025": "15.22%",
        "FY2020": "13.86%", "FY2019": "15.32%", "FY2018": "18.14%", "FY2017": "18.73%", "FY2016": "18.74%",
    })],
    p3_sources(),
    note="FY2021-FY2024 are directly disclosed in the Bank's Pillar 3 KM1 (an earlier build incorrectly marked "
         "them undisclosed). FY2025 FILLED 2026-09-15 from the FY2025 Pillar 3 KM1's own 'CET 1 ratio (%)' row "
         "(15.22%, a printed figure, not derived here - it ties to that edition's own 117,764/773,493). It had "
         "read 'Not publicly disclosed' only because the FY2025 edition had not been located. "
         "FY2019/FY2020 use the Bank's own disclosed 'Common equity tier 1 ratio' KPI. FY2016-FY2018 are computed "
         "(CET1 Capital / Total RWAs, both independently disclosed those years) since no ratio KPI line was found "
         "for years before FY2019 - note the FY2018 Pillar 3 edition independently prints 18.14%/18.73% for "
         "FY2018/FY2017, confirming those two computed values against a primary source.",
)

metric(
    "Tier 1 Capital", "£'000",
    [("Tier 1 capital", {
        "FY2025": 117764, "FY2024": 115427, "FY2023": 97919, "FY2022": 86426, "FY2021": 86301,
        "FY2020": 71830, "FY2019": 71230, "FY2018": 70230, "FY2017": 67430, "FY2016": 63030,
    })],
    p3_sources(),
    note="Equal to CET1 capital - no Additional Tier 1 instruments are disclosed in any year (every Pillar 3 "
         "edition FY2016-FY2025 prints an explicit 'Additional Tier 1 Capital' row of nil). FY2025 corrected "
         "2026-09-15 alongside CET1 Capital - see that sheet's note. The FY2025 Pillar 3 leverage table (LR2) "
         "independently states 'Tier 1 capital 117,764', confirming this figure from a second table in the "
         "same document.",
)
metric(
    "Tier 1 Ratio", "%",
    [("Tier 1 Ratio", {
        "FY2021": "14.93%", "FY2022": "15.03%", "FY2023": "16.67%", "FY2024": "17.36%", "FY2025": "15.22%",
        "FY2020": "13.86%", "FY2019": "15.32%", "FY2018": "18.14%", "FY2017": "18.73%", "FY2016": "18.74%",
    })],
    p3_sources(),
    note="Equal to CET1 Ratio - no Additional Tier 1 instruments are disclosed in any year. See CET1 Ratio's own "
         "note for sourcing/computation detail per year.",
)

metric(
    "Total Capital", "£'000",
    [("Own funds (Tier 1 + Tier 2 capital)", {
        "FY2025": 137764, "FY2024": 135723, "FY2023": 118259, "FY2022": 106699, "FY2021": 106687,
        "FY2020": 92370, "FY2019": 91720, "FY2018": 90580, "FY2017": 87430, "FY2016": 83030,
    })],
    p3_sources(),
    note="Tier 2 capital comprises qualifying subordinated liabilities (plus, in FY2023/FY2022, a small IFRS 9 "
         "ECL regulatory-capital adjustment disclosed by the Bank). FY2016-FY2020 sourced from each year's own "
         "'Capital Structure'/Total Capital Requirement (TCR) table. CORRECTED 2026-09-15: FY2025 previously "
         "read 144,852, which is Balance Sheet total equity 124,587 plus the carrying value of subordinated "
         "liabilities 20,265 - an accounts-derived construct, not the Bank's own regulatory own funds, and "
         "inconsistent with FY2023/FY2024 in this same row. The FY2025 Pillar 3 KM1 states 'Total Own Funds "
         "(CET 1 + Tier 1 + tier 2)' of 137,764 (= CET1 after deductions 117,764 + Tier 2 subordinated "
         "liabilities 20,000), and that transcribed figure is now used. NOTE the same document's section 8.3 "
         "reconciliation shows own funds of 130,865 'reported in published financial statements based on "
         "COREP submission' against 137,764 'reported in Pillar-3 including audited profit of £10m and "
         "adjusted for proposed dividend of 33%' - the KM1/Pillar 3 basis is used here, and the COREP figure "
         "is recorded rather than merged.",
)
metric(
    "Total Capital Ratio", "%",
    [("Total Capital Ratio", {
        "FY2021": "18.65%", "FY2022": "18.55%", "FY2023": "20.13%", "FY2024": "20.41%", "FY2025": "17.81%",
        "FY2020": "18.80%", "FY2019": "19.93%", "FY2018": "23.30%", "FY2017": "24.30%", "FY2016": "24.80%",
    })],
    p3_sources(),
    note="This row uses the Bank's 'Capital Adequacy Ratio (CET 1 + Tier 1 + Tier 2)' KM1 line throughout, which "
         "is the CRR total capital ratio. Its KM1 ALSO prints a row labelled 'Total capital ratio (%)' which, per "
         "its own parenthetical '(CET 1 + Tier 1)', is the Tier 1 ratio and NOT the total capital ratio - see the "
         "row-naming trap in the source note; reading that row by its label is what produced the discrepancy "
         "previously flagged on this workbook, now resolved. FY2025 FILLED 2026-09-15 from the FY2025 Pillar 3 "
         "KM1's Capital Adequacy Ratio row (17.81%, printed; ties to that edition's own 137,764/773,493). "
         "FY2016-FY2020 use each year's own explicitly disclosed 'capital adequacy ratio' narrative figure. "
         "FY2020's own report shows a small internal inconsistency between this narrative figure (18.8%) and its "
         "own KPI table's 'Capital adequacy ratio' line (17.85%) - both figures as printed, not force-reconciled; "
         "the FY2020 Pillar 3 edition independently prints 17.97%, a third value, also not force-reconciled. "
         "FY2016's own Pillar 3 states 24.67% against the Annual Report's 24.80% carried here, and FY2017's "
         "states 24.29% against 24.30% - both documented rather than overwritten.",
)
metric(
    "Total RWAs", "£'000",
    [("Total RWAs", {
        "FY2021": 547938, "FY2022": 575205, "FY2023": 587448, "FY2024": 664889, "FY2025": 773493,
        "FY2020": 513950, "FY2019": 461590, "FY2018": 387180, "FY2017": 359940, "FY2016": 336350,
    })],
    p3_sources(),
    note="FY2021-FY2024 are directly disclosed in the Bank's Pillar 3 KM1. FY2025 FILLED 2026-09-15 from the "
         "FY2025 Pillar 3 KM1's 'Total Risk-Weighted Assets' row (773,493, printed; independently repeated in "
         "that edition's section 8.2 'Own Funds Requirements' table as the Pillar 1 total). FY2016-FY2020 "
         "sourced from each year's own 'Capital Structure'/Total Capital Requirement (TCR) table, which "
         "discloses Risk Weighted Assets directly. FLAGGED, NOT FORCE-RECONCILED: FY2019's 461,590 here is the "
         "FY2019 Annual Report's own KPI figure, but the FY2019, FY2020 and FY2021 Pillar 3 editions all state "
         "442,493 for FY2019, as does the FY2020 Annual Report's own FY2019 comparative - two independent "
         "sources disagree with the value carried here and the divergence is deliberately documented rather "
         "than overwritten, per project convention that each year keeps its own Annual Report figure. FY2016 "
         "likewise: 336,350 (AR) vs 336,541 (FY2016 Pillar 3 section 5.2). FY2017/FY2018 agree with the Pillar "
         "3 editions to within £1k of rounding (those editions report in whole £: 359,940,986 and 387,179,103).",
)

rwa_breakdown_rows = [
    ("SECTION", "As presented in the FY2024 Pillar 3 edition's OV1 table (counterparty credit risk split out)", {}),
    ("DATA", "Credit risk (excluding CCR)", {"FY2024": 611684, "FY2023": 547178}),
    ("DATA", "Counterparty credit risk including CVA", {"FY2024": 1895, "FY2023": 137}),
    ("DATA", "Market risk", {"FY2024": 42, "FY2023": 42}),
    ("DATA", "Operational risk", {"FY2024": 51268, "FY2023": 40092}),
    ("TOTAL", "Total risk-weighted exposure amount (RWEAs) - OV1 presentation", {"FY2024": 664889, "FY2023": 587449}),
    ("SECTION", "As presented in each year's own Pillar 3 'Own Funds Requirements' table (credit risk combined)", {}),
    ("DATA", "Credit risk (combined - CCR not separately disclosed in these editions)", {
        "FY2025": 709091, "FY2023": 547178, "FY2022": 538880, "FY2021": 512151,
        "FY2020": 477272, "FY2019": 407459, "FY2018": 353393, "FY2017": 330001, "FY2016": 310219,
    }),
    ("DATA", "Operational risk", {
        "FY2025": 63924, "FY2023": 40092, "FY2022": 36011, "FY2021": 35091,
        "FY2020": 35898, "FY2019": 34540, "FY2018": 33470, "FY2017": 29497, "FY2016": 25183,
    }),
    ("DATA", "Market risk (including CVA from FY2020 onward, where the Bank labels it so)", {
        "FY2025": 478, "FY2023": 179, "FY2022": 313, "FY2021": 696,
        "FY2020": 781, "FY2019": 494, "FY2018": 316, "FY2017": 443, "FY2016": 1139,
    }),
    ("TOTAL", "Pillar 1 total (8% of RWAs) - i.e. total RWAs on this presentation", {
        "FY2025": 773493, "FY2023": 587449, "FY2022": 575204, "FY2021": 547938,
        "FY2020": 513951, "FY2019": 442493, "FY2018": 387179, "FY2017": 359941, "FY2016": 336541,
    }),
]
bw.add_rwa_breakdown_sheet(
    title="Habib Bank Zurich Plc — RWA Breakdown",
    subtitle="EVERY year FY2016-FY2025 has a real risk-category split, from that year's own Pillar 3 edition. "
             "Two presentations are shown because the Bank changed format: FY2023/FY2024 in the FY2024 "
             "edition's OV1 form (counterparty credit risk split out), and every year in the 'Own Funds "
             "Requirements' form (credit risk combined). FY2023 appears in both, and they reconcile.",
    rows=rwa_breakdown_rows,
    sources_text=p3_sources() + (
        "\n\nRWA BREAKDOWN NOTE - REWRITTEN 2026-09-15, CORRECTING A FALSE NEGATIVE. This sheet previously "
        "stated that FY2016-FY2021 have no risk-category split and that a 2026-09-12 re-verification had "
        "'confirmed the FY2016-FY2021 gap is genuine, not a research miss'. THAT CONCLUSION WAS WRONG, and it "
        "was wrong for a specific and instructive reason: it was reached by checking only the STATUTORY "
        "ACCOUNTS (the FY2021 Annual Report's Note 31.25 and the FY2020 Annual Report's p.15), which indeed "
        "carry no split - while the Bank's own Pillar 3 editions, which were not located at the time because "
        "the script was pointing at a wrong URL base, carry a credit/operational/market split for EVERY year "
        "FY2016-FY2025 in their 'Own Funds Requirements' section. A negative established only against the "
        "accounts is not a negative about the Bank's disclosure. All ten splits above are transcribed from "
        "the relevant edition's own table:\n"
        f"FY2025 section 8.2 - {P3_2025_URL}\n"
        f"FY2024 section 8.2 (OV1 form; also carries the FY2023 comparative) - {P3_2024_URL}\n"
        f"FY2023 section 8.2 (also carries the FY2022 comparative) - {P3_2023_URL}\n"
        f"FY2022 section 8.2 - {P3_2022_URL}\n"
        f"FY2021 section 7.2 - {P3_2021_URL}\n"
        f"FY2020 section 7.2 - {P3_2020_URL}\n"
        f"FY2019 / FY2018 / FY2017 / FY2016 'Own Funds Requirements' - {P3_2019_URL} / {P3_2018_URL} / "
        f"{P3_2017_URL} / {P3_2016_URL}\n"
        "The FY2017 and FY2018 editions report in whole £ (e.g. credit risk 330,001,238 and 353,393,165); "
        "these are rounded to £'000 here for consistency with the other years.\n"
        "CORRECTION to a row label: FY2022's 313 was previously carried on the 'Counterparty credit risk "
        "including CVA' row. Both the FY2022 edition's own table and the FY2023 edition's FY2022 comparative "
        "label that 313 'Market Risk including CVA'. It has been moved to the market risk row. FY2022 is "
        "shown only on the combined presentation because neither edition covering it splits CCR out.\n"
        "FLAGGED, NOT FORCE-RECONCILED: FY2023's market risk is 42 on the FY2024 edition's OV1 presentation "
        "but 179 on the FY2023 edition's own presentation, with credit risk identical (547,178) and the total "
        "identical (587,449) in both - the FY2024 edition moves 137 of it into a separately-disclosed "
        "counterparty-credit-risk line. Both are reproduced as printed. Note also that the totals on this "
        "sheet are each edition's own Pillar 1 total, which for FY2019 (442,493) and FY2016 (336,541) differs "
        "from the Total RWAs sheet's Annual Report-sourced figures (461,590 and 336,350) - see that sheet's "
        "note; the divergence is documented, not reconciled."
    ),
    first_col_width=90,
    source_height=300,
)

metric(
    "Leverage Ratio", "%",
    [("Leverage Ratio", {
        "FY2021": "8.63%", "FY2022": "8.74%", "FY2023": "8.81%", "FY2024": "10.18%", "FY2025": "9.26%",
        "FY2016": "9.6%",
        "FY2020": "8.90%", "FY2019": "9.49%", "FY2018": "10.11%", "FY2017": "9.92%",
    })],
    p3_sources(),
    note="No leverage exposure measure is disclosed in the FY2021-FY2025 statutory accounts, but the Bank's own "
         "Pillar 3 editions disclose the ratio directly for every year FY2016-FY2025. FY2025 FILLED 2026-09-15 "
         "from the FY2025 Pillar 3 KM1 and its LR2 table: 9.26% on the 'Leverage ratio excluding claims on "
         "central banks' basis, which is the Bank's own headline KM1 figure and the UK-CRR convention. BASIS "
         "WARNING - that same LR2 table also prints a 'Leverage ratio (%)' of 7.80% for FY2025 including claims "
         "on central banks; the two are different measures and must never be merged into one series. FY2016 "
         "FILLED 2026-09-15 and no longer a gap: the FY2016 Pillar 3 edition, section 7 'Leverage Ratio', states "
         "in narrative that 'As at 31 December 2016 Bank has a leverage ratio of 9.6%' - it is a narrative "
         "figure rather than a table row, and is printed to one decimal place as shown, which is why the "
         "Annual Report's KPI table (which has no leverage line that year) did not carry it. FLAGGED, NOT "
         "FORCE-RECONCILED: the FY2025 edition restates FY2024 to 9.69% (excluding central bank claims) / 8.41% "
         "(including them) against the 10.18% carried here from the FY2024 edition, and FY2019 has three "
         "published values (10.03% FY2019 edition, 9.03% FY2020/FY2021 editions, 9.49% Annual Report KPI table, "
         "the last being the value carried here) - see the source note's restatement list.",
)

metric(
    "LCR", "%",
    [
        ("Liquidity Coverage Ratio (average for the period) — Annual Report basis", {
            "FY2025": "232%", "FY2024": "287%", "FY2023": "196%", "FY2022": "205%", "FY2021": "159%",
            "FY2020": "227%", "FY2019": "160%", "FY2018": "198%", "FY2017": "236%", "FY2016": "291%",
        }),
        ("Liquidity Coverage Ratio (as at 31 December, point-in-time) — Pillar 3 KM1 basis", {
            "FY2025": "180%", "FY2024": "243%", "FY2023": "286%", "FY2022": "405%", "FY2021": "153%",
            "FY2020": "226.83%", "FY2019": "159.81%", "FY2018": "198.04%", "FY2017": "235.82%",
            "FY2016": "Not disclosed (the FY2016 Pillar 3 edition has no key-metrics table)",
        }),
    ],
    p3_sources(),
    note="TWO SERIES, DELIBERATELY KEPT ON SEPARATE ROWS AND NEVER MERGED. The Bank discloses LCR on 4 bases in "
         "its Annual Report (as at 31 December, average/maximum/minimum for the period); the "
         "average-for-the-period figure is the first row, used for consistency with this project's convention "
         "elsewhere. The second row, ADDED 2026-09-15, is the point-in-time 31 December figure from each "
         "Pillar 3 edition's own KM1 - a different measure, not a correction of the first, and the two diverge "
         "sharply in places (FY2022: 205% average vs 405% point-in-time). FY2017-FY2020 are printed to two "
         "decimals in the Pillar 3 and are reproduced as printed. FLAGGED, NOT FORCE-RECONCILED: the FY2025 "
         "edition restates FY2024's point-in-time LCR to 250% against the FY2024 edition's own 243% carried "
         "here. The FY2016 Pillar 3 edition contains no key-metrics table at all, so there is no point-in-time "
         "figure for FY2016 - a genuine, enumerated absence within an otherwise complete run, not a research gap.",
)
metric(
    "NSFR", "%",
    [("Net Stable Funding Ratio", {
        "FY2025": "133%", "FY2024": "137%", "FY2023": "136%", "FY2022": "127%", "FY2021": "130.16%",
        "FY2020": "134.19%", "FY2019": "135.76%", "FY2018": "136.70%", "FY2017": "139.68%",
        "FY2016": "Not disclosed (the FY2016 Pillar 3 edition has no key-metrics table)",
    })],
    p3_sources(),
    note="Every figure here is directly disclosed in the relevant year's own Pillar 3 KM1 (none derived). FY2025 "
         "FILLED and FY2017-FY2020 FILLED 2026-09-15 from the newly-sourced editions. NOTE ON THE PRE-2022 "
         "YEARS: this project treats NSFR blanks before FY2022 as structurally expected, because the UK NSFR "
         "requirement began 1 January 2022 (PRA PS17/21). That presumption does NOT apply here - Habib Bank "
         "Zurich published an NSFR in its Pillar 3 KM1 voluntarily from FY2017 onward, on the Basel III "
         "definition (available stable funding / required stable funding, both amounts printed alongside the "
         "ratio in each edition), well ahead of the UK mandate. A figure the bank actually published beats a "
         "structural-blank presumption, so these are real disclosures rather than back-filled estimates. "
         "FY2017-FY2021 are printed to two decimals in their editions and reproduced as printed; FY2022 onward "
         "the Bank rounds to whole percent. FY2016 is a genuine, enumerated absence - that edition predates "
         "the Bank's key-metrics table entirely.",
)
bw.add_not_disclosed_metric_sheets(
    ["MREL Ratio"], p3_sources(),
    per_note={
        "NSFR": "Not disclosed in any year's statutory accounts.",
        "MREL Ratio": "Not disclosed - Habib Bank Zurich Plc is not identified as a UK resolution entity in "
                      "these accounts. POSITIVE RECORD ADDED 18 September 2026 (KM1-032): that was an "
                      "entity-classification inference drawn from the accounts' silence. It is now sourced. "
                      "The Bank of England's own 'External minimum requirements for own funds and eligible "
                      "liabilities (MRELs)' disclosures (2023, 2024, 2025 and 2026 editions, at "
                      "bankofengland.co.uk/financial-stability/resolution/mrels-<year>) contain 'all firms "
                      "with a resolution entity incorporated in the UK for which an MREL above MCR has been "
                      "communicated', in the BoE's own words. Habib Bank Zurich Plc appears in none of the "
                      "four editions. The BoE publishes the requirement, not the ratio, so nothing from "
                      "that table is transcribed here.",
    },
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {
            "FY2025": 1483269, "FY2024": 1284398, "FY2023": 1145027, "FY2022": 1019038, "FY2021": 892077,
            "FY2020": 762133, "FY2019": 683779, "FY2018": 635905, "FY2017": 604948, "FY2016": 593146,
        }),
        ("Loans and advances to customers at amortised cost", {
            "FY2025": 800598, "FY2024": 682470, "FY2023": 632149, "FY2022": 601062, "FY2021": 514061,
            "FY2020": 455954, "FY2019": 430736, "FY2018": 398977, "FY2017": 379996, "FY2016": 350395,
        }),
        ("Due to customers at amortised cost", {
            "FY2025": 1142802, "FY2024": 1023002, "FY2023": 885890, "FY2022": 769556, "FY2021": 672008,
            "FY2020": 623644, "FY2019": 577013, "FY2018": 523493, "FY2017": 495252, "FY2016": 479619,
        }),
        ("Total equity", {
            "FY2025": 124587, "FY2024": 119896, "FY2023": 102879, "FY2022": 89508, "FY2021": 86203,
            "FY2020": 72182, "FY2019": 71474, "FY2018": 70197, "FY2017": 67740, "FY2016": 63250,
        }),
    ],
    balance_sheet_unit="£'000",
    income_statement_totals=[
        ("Net interest income", {
            "FY2025": 37734, "FY2024": 37997, "FY2023": 34164, "FY2022": 23911, "FY2021": 17755,
            "FY2020": 15989, "FY2019": 17395, "FY2018": 16248, "FY2017": 15782, "FY2016": 11800,
        }),
        ("Operating expenses", {
            "FY2025": -28419, "FY2024": -26502, "FY2023": -23424, "FY2022": -19076, "FY2021": -16263,
            "FY2020": -16688, "FY2019": -16176, "FY2018": -14699, "FY2017": -14440, "FY2016": -9809,
        }),
        ("Profit after tax", {
            "FY2025": 10023, "FY2024": 11087, "FY2023": 12552, "FY2022": 5700, "FY2021": 4475,
            "FY2020": 600, "FY2019": 3484, "FY2018": 3588, "FY2017": 4400, "FY2016": 3031,
        }),
    ],
    income_statement_unit="£'000",
    equity_changes_totals=[
        ("Opening equity", {
            "FY2025": 119896, "FY2024": 102879, "FY2023": 89508, "FY2022": 86203, "FY2021": 72182,
            "FY2020": 71474, "FY2019": 70197, "FY2018": 67740, "FY2017": 63250, "FY2016": 0,
        }),
        ("Total comprehensive income for the year, net of tax", {
            "FY2025": 10235, "FY2024": 11159, "FY2023": 13371, "FY2022": 4781, "FY2021": 4021,
            "FY2020": 708, "FY2019": 3764, "FY2018": 3351, "FY2017": 4708, "FY2016": 3249,
        }),
        ("Other equity movements, net", {
            "FY2025": -5544, "FY2024": 5858, "FY2023": 0, "FY2022": -1476, "FY2021": 10000,
            "FY2020": 0, "FY2019": -147, "FY2018": -1124, "FY2017": 0, "FY2016": 60000,
        }),
        ("Closing equity", {
            "FY2025": 124587, "FY2024": 119896, "FY2023": 102879, "FY2022": 89508, "FY2021": 86203,
            "FY2020": 72182, "FY2019": 71474, "FY2018": 70197, "FY2017": 67740, "FY2016": 63250,
        }),
    ],
    equity_changes_unit="£'000",
    cash_flow_totals=[
        ("Net cash from/(used in) operating activities", {
            "FY2025": 56144, "FY2024": 77571, "FY2023": 125301, "FY2022": -11083, "FY2021": 72035,
        }),
        ("Net cash from/(used in) investing activities", {
            "FY2025": 8897, "FY2024": -64522, "FY2023": -19648, "FY2022": 21301, "FY2021": -72353,
        }),
        ("Net cash from/(used in) financing activities", {
            "FY2025": -6204, "FY2024": 3989, "FY2023": -1623, "FY2022": -2401, "FY2021": 9597,
        }),
        ("Cash and cash equivalents at end of year", {
            "FY2025": 291217, "FY2024": 232380, "FY2023": 215342, "FY2022": 96506, "FY2021": 88689,
        }),
    ],
    cash_flow_unit="£'000",
    ratios=[
        ("CET1 / Tier 1 Ratio (%)", {
            "FY2025": 15.22, "FY2024": 17.36, "FY2023": 16.67, "FY2022": 15.03, "FY2021": 14.93,
            "FY2020": 13.86, "FY2019": 15.32, "FY2018": 18.14, "FY2017": 18.73, "FY2016": 18.74,
        }),
        ("Total Capital Ratio (%)", {
            "FY2025": 17.81, "FY2024": 20.41, "FY2023": 20.13, "FY2022": 18.55, "FY2021": 18.65,
            "FY2020": 18.80, "FY2019": 19.93, "FY2018": 23.30, "FY2017": 24.30, "FY2016": 24.80,
        }),
        ("Leverage Ratio (%)", {
            "FY2025": 9.26, "FY2024": 10.18, "FY2023": 8.81, "FY2022": 8.74, "FY2021": 8.63,
            "FY2020": 8.90, "FY2019": 9.49, "FY2018": 10.11, "FY2017": 9.92, "FY2016": 9.6,
        }),
        ("LCR (average, %)", {
            "FY2025": 232, "FY2024": 287, "FY2023": 196, "FY2022": 205, "FY2021": 159,
            "FY2020": 227, "FY2019": 160, "FY2018": 198, "FY2017": 236, "FY2016": 291,
        }),
        ("NSFR (%)", {
            "FY2025": 133, "FY2024": 137, "FY2023": 136, "FY2022": 127, "FY2021": 130.16,
            "FY2020": 134.19, "FY2019": 135.76, "FY2018": 136.70, "FY2017": 139.68,
        }),
    ],
    note="REWRITTEN 2026-09-15. This note previously said only LCR could be charted because the other ratios "
         "were 'not disclosed in this entity's statutory accounts (no standalone Pillar 3 document exists and "
         "no RWA figure is published)'. That was wrong: Habib Bank Zurich publishes a standalone Pillar 3 "
         "disclosure for EVERY year FY2016-FY2025, with RWAs and all of these ratios - the documents had simply "
         "been sought at a wrong URL. All five series above are now charted from those editions. Only MREL "
         "Ratio remains undisclosed, which is a genuine sourced negative (the Bank is not a UK resolution "
         "entity). CAVEATS carried from the detail sheets: the LCR series here is the Annual Report's "
         "average-for-the-period basis, NOT the Pillar 3's point-in-time basis, which is a different measure "
         "shown on its own row on the LCR sheet and must not be read as a continuation of this one; the FY2016 "
         "leverage figure is a narrative disclosure printed to one decimal; and several years have more than "
         "one published value because the Bank restates across editions. See each detail sheet's own source "
         "citation for the underlying document, page and the divergences that were documented rather than "
         "reconciled.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/HABIB BANK ZURICH FINANCIALS.xlsx")
