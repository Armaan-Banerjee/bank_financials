import os
import sys
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021", "FY2020", "FY2019", "FY2018", "FY2017", "FY2016", "FY2015", "FY2014",
         "FY2013", "FY2012", "FY2011", "FY2010"]
YEAR_LABEL = {y: y for y in YEARS}
# HD-074: Pillar 3 (all 11 metric sheets), Asset Quality, and RWA Breakdown
# stay out of scope for this statutory-statement-only extension - pin them
# to the original project-wide FY2014-FY2025 window via this override.
PILLAR3_YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021", "FY2020", "FY2019", "FY2018", "FY2017", "FY2016", "FY2015", "FY2014"]
CH = "https://find-and-update.company-information.service.gov.uk/company/04656003/filing-history"
# HD-074 (2026-09-06): FY2010-FY2013 own-year Companies House statutory accounts
# (entity-only, same basis as FY2014+). Real statutory floor for QIB (UK): the
# Bank (formerly European Finance House Limited) received FSA authorisation and
# commenced trading 29 January 2008, so FY2008/FY2009 accounts exist too, but
# the ticket's confirmed floor is FY2010 - not extended further this session.
CH_FY2013 = CH + "/MzA5NDQ2NjU5MmFkaXF6a2N4/document?format=pdf&download=0"
CH_FY2012 = CH + "/MzA3ODk3MTMzNGFkaXF6a2N4/document?format=pdf&download=0"
CH_FY2011 = CH + "/MzA2MDE2OTYyNGFkaXF6a2N4/document?format=pdf&download=0"
CH_FY2010 = CH + "/MzAzOTkwNDQxN2FkaXF6a2N4/document?format=pdf&download=0"
# HD-049 note: FY2014-FY2020 sourced from QIB (UK)'s own qib-uk.com "Financial Reports" library
# (native-text PDFs, not scans) except FY2014, whose own AR was not found live on the site and is
# instead sourced from its Companies House filing (a scanned tiff2pdf image; cross-validated
# digit-for-digit against FY2015's own AR comparative column, which is native text and agrees
# exactly). Capped at FY2014 per the historical-depth map's project-wide decision even though
# Companies House shows filings back to FY2013 (pre-CRD IV/Basel III, not comparable).
AR = {"FY2025": CH+"/MzUyNzI4MTM5OGFkaXF6a2N4/document?format=pdf&download=0", "FY2024": CH+"/MzQ2NzkwMzQ0MmFkaXF6a2N4/document?format=pdf&download=0", "FY2023": CH+"/MzQyNDU4NzQ0OGFkaXF6a2N4/document?format=pdf&download=0", "FY2022": CH+"/MzM4MDQ4MTUzN2FkaXF6a2N4/document?format=pdf&download=0", "FY2021": CH+"/MzMzOTk2ODIxNmFkaXF6a2N4/document?format=pdf&download=0",
      "FY2020": "https://www.qib-uk.com/wp-content/uploads/sites/2/2021/09/QIB-UK-Annual-Report-31-December-2020-v6-Signed.pdf",
      "FY2019": "https://www.qib-uk.com/wp-content/uploads/sites/2/2020/08/QIB-Annual-Report-UK-2019.pdf",
      "FY2018": "https://www.qib-uk.com/wp-content/uploads/sites/2/2019/12/QIB-UK-Annual-Report-2018-edited.pdf",
      "FY2017": "https://www.qib-uk.com/wp-content/uploads/sites/2/2019/12/QIB-UK-Annual-Report-2017_Eng-.pdf",
      "FY2016": "https://www.qib-uk.com/-/media/project/uk/files/finance-reports/qib-uk-annual-report-2016-eng-.pdf",
      "FY2015": "https://www.qib-uk.com/-/media/project/uk/files/finance-reports/qib-uk-annual-report-2015.pdf",
      "FY2014": CH+"/MzEyMDQzMzk0OWFkaXF6a2N4/document?format=pdf&download=0"}
# BLOCKED, WITH NO ARCHIVED FALLBACK - an unresolved state, explicitly NOT a negative
# (checked 2026-09-16). The four qib-uk.com Annual Report URLs above for FY2017-FY2020 are
# refused by the host's WAF. NOTE THE TRAP: they return HTTP **200**, not an error code, but
# the body is a 247-byte text/html page reading "Request Rejected - The requested URL was
# rejected. Please consult with your administrator. Your support ID is: ..." - an F5-style
# WAF rejection wearing a success status. A status-code check alone would mis-read these as
# working; only the Content-Type and body reveal the block, which is why a PDF must always be
# confirmed by its %PDF magic bytes rather than by HTTP 200.
# This is a BLOCK, i.e. an UNKNOWN: it records that the host declined to serve THIS fetcher,
# NOT that the documents were withdrawn - a human browser or another network may retrieve them
# normally. No substitute can be offered either: a Wayback CDX query was run against each of
# the four exact URLs on 2026-09-16 and every one returned successfully with an EMPTY result
# set, so the absence of an ARCHIVE is enumerated rather than assumed, while the documents
# themselves remain unexamined rather than absent. They are left cited at the publisher's live
# URLs deliberately, there being nothing verified to replace them with. Do not downgrade these
# to "dead", and do not record them as evidence that QIB (UK) failed to publish.
# P3 declarations for FY2014-FY2018 are an appendix bundled inside that year's own Annual Report
# (same PDF as AR[y], "Appendix: QIB (UK) Pillar 3 Declaration"). QIB (UK) stopped including the
# Pillar 3 appendix in the AR from FY2019 onward and began publishing a standalone Pillar 3
# document from FY2020. FY2019 has no standalone Pillar 3 document of its own on the Bank's site
# or in Wayback Machine snapshots of qib-uk.com (checked 2014-2022) - its KM1-style figures are
# sourced from FY2020's own standalone document's FY2019 comparative column.
#
# KM1-024 (16 September 2026) CORRECTION TO FY2021'S CITATION. qib-uk.com's own financial-reports
# library was listed directly and carries a standalone "pillar-3-disclosure-document-2021-board-
# approved.pdf" - the Bank's OWN 31 December 2021 edition - which this script had not cited; FY2021
# was pointed at the FY2022 edition's comparative column instead. FY2021 now cites its own edition.
# The FY2021 edition's key-metrics table (printed p.3, an EMBEDDED IMAGE in an otherwise text-native
# PDF, read at 300dpi) gives CET1 78,028, total capital 91,081, RWA 462,020, CET1/Tier 1 ratio
# 16.89%, total capital ratio 19.71%, leverage exposure 892,228, leverage ratio 8.75% and LCR
# 555.60% - every FY2021 figure on the metric sheets below except NSFR, which that table does not
# carry at all and which therefore still comes from the FY2022 edition's comparative column.
P3 = {"FY2025": "https://www.qib-uk.com/-/media/project/uk/files/finance-reports/pillar-3-disclosure-document--2025-approved.pdf", "FY2024": "https://www.qib-uk.com/-/media/project/uk/files/finance-reports/pillar-3-disclosure-document-31-december-2024.pdf", "FY2023": "https://www.qib-uk.com/-/media/project/uk/files/finance-reports/pillar-3-disclosure-document-31-december-2023.pdf", "FY2022": "https://www.qib-uk.com/-/media/project/uk/files/finance-reports/pillar-3-disclosure-document-2023.pdf", "FY2021": "https://www.qib-uk.com/-/media/project/uk/files/finance-reports/pillar-3-disclosure-document-2021-board-approved.pdf",
      "FY2020": "https://www.qib-uk.com/-/media/project/uk/files/finance-reports/pillar-3-disclosure-document-2020-board-approved-final.pdf",
      "FY2019": "https://www.qib-uk.com/-/media/project/uk/files/finance-reports/pillar-3-disclosure-document-2020-board-approved-final.pdf",
      "FY2018": AR["FY2018"], "FY2017": AR["FY2017"], "FY2016": AR["FY2017"], "FY2015": AR["FY2015"], "FY2014": AR["FY2014"]}

ENTITY = ("ENTITY NOTE: QIB (UK) plc (Companies House 04656003, FRN 466577) is the UK bank subsidiary of Qatar Islamic Bank S.A.Q. The Bank states that it had no active subsidiaries or joint ventures at 31 December 2023 and does not prepare group accounts; these are entity-only GBP accounts. Companies House shows the entity Active with accounts filed through FY2025.")
CASH_SOURCES = ("Sources - QIB (UK) plc's own entity Statement of Cash Flows, converted from £ to £m (divide by 1,000,000 and round to 2 decimals):\n" + "\n".join(f"{y}: Annual Report, p.{p} - {AR[y]}" for y,p in {"FY2025":24,"FY2024":25,"FY2023":24,"FY2022":25,"FY2021":22,"FY2020":21,"FY2019":14,"FY2018":16,"FY2017":17,"FY2016":13,"FY2015":14,"FY2014":14}.items()) + "\nFY2025/FY2024 reports label the FY2024 comparative restated and FY2023 labels the FY2022 comparative restated. Each year's own report column is used here, preserving the project convention and avoiding blended reclassifications. FY2024 and FY2023 each contain a source presentation difference between the printed operating line items and the printed operating subtotal; explicit reconciliation rows preserve both.\nFY2014-FY2020 own-year cash flow statements were sourced from QIB (UK)'s qib-uk.com Annual Report PDFs (native text). FY2018/FY2019/FY2020's own 'cash and cash equivalents at end of year' figure (37,017,161 / 40,777,075 / 41,708,427) is a few hundred pounds above that same year's own Balance Sheet 'Cash and balances with banks' line (37,016,753 / 40,776,701 / 41,708,029) - an immaterial gross-vs-net-of-ECL presentation difference within the Bank's own report, not a transcription error.\n\n" +
    "DATA QUALITY FLAG - FY2015: the Bank's own AR2015 prints 'Net cash inflow / (outflow) from operating activities' as a positive 23,588,646, but that figure does not reconcile two different ways: (1) it is not the sum of that same table's own 14 printed adjustment lines, which sum to exactly -23,588,647 (verified independently); and (2) using +23,588,646 for operating activities together with the Bank's own printed investing (-2,658,626) and financing (+26,500,000) subtotals gives 47,430,020, not the Bank's own printed 'Net increase in cash and cash equivalents' of 252,728 - whereas using -23,588,647 gives -23,588,647-2,658,626+26,500,000=252,727, matching (within £1 rounding) both the printed net-change figure and the independently-verifiable cash-at-start/cash-at-end tie-out (5,844,014 -> 6,096,742). This sheet therefore carries -23,588,647 (a net outflow) for FY2015 operating activities - the value consistent with the rest of the Bank's own statement and with actual cash movement - rather than the Bank's own headline positive figure, which appears to be missing a negative sign/bracket in the published PDF. All 14 individual adjustment-line figures are transcribed exactly as printed either way.\n\n" + ENTITY)
def p3_sources():
    return ("Sources - QIB (UK) plc's own Pillar 3 disclosures (amounts in £m unless noted; ratios as reported):\n" + "\n".join(f"{y}: {P3_LABEL.get(y, 'own-year disclosure')}, {P3_PAGES.get(y,'pp.6-7')} - {P3[y]}" for y in PILLAR3_YEARS) + "\nFY2014/FY2015: the Bank's own Pillar 3 Declaration for these years is narrative-only - it discloses total Tier 1 and Tier 2 capital in round £m terms but no Total RWA figure and no CET1/Total Capital ratio percentage; those cells are left blank rather than estimated. FY2016's own Pillar 3 Declaration is likewise narrative-only; its numeric capital/RWA/ratio figures here are read from FY2017's own Annual Report Note 4 comparative ('2016') column instead.\nLeverage Ratio, LCR and NSFR are not numerically disclosed anywhere in the reviewed QIB UK documents before FY2019 (LCR)/FY2019 (Leverage) - both first appear as a % figure in FY2020's own standalone Pillar 3 document's FY2019 comparative column. NSFR is not disclosed in any reviewed QIB UK document through FY2020 (the FY2020 document states the Bank was still 'monitoring' NSFR ahead of implementation).\nMREL is not disclosed in the reviewed QIB UK Pillar 3 documents.\n\n" + ENTITY)
P3_LABEL = {
    "FY2022": "own-year disclosure (scanned PDF, no text layer - read from a 300dpi rendering)",
    "FY2021": "own-year disclosure, bespoke key-metrics table printed as an image (NSFR only: FY2021 comparative column of the FY2022 disclosure)",
    "FY2019": "FY2019 comparative column of FY2020 disclosure",
    "FY2016": "FY2016 comparative column of FY2017 Annual Report Note 4",
    "FY2017": "own-year disclosure, Annual Report Note 4",
    "FY2018": "own-year disclosure, Annual Report Note 4",
    "FY2015": "own-year disclosure (narrative only, no RWA/ratio)",
    "FY2014": "own-year disclosure (narrative only, no RWA/ratio)",
}
P3_PAGES = {"FY2017": "pp.47-48", "FY2018": "pp.49-50", "FY2016": "pp.47-48 (FY2017 AR)", "FY2015": "pp.46", "FY2014": "p.55", "FY2020": "p.3 key-metrics summary (page corrected from p.6 on 2026-09-16) / section 6.2 Pillar 1, p.30", "FY2019": "p.3 of the FY2020 doc, comparative column (page corrected from p.6 on 2026-09-16)", "FY2021": "p.3"}
def m(d): return {y: round(v/1_000_000, 2) for y,v in d.items()}

bw = BankWorkbook(bank_name="QIB (UK) plc", years=YEARS, year_label=YEAR_LABEL, header_color="0B4F6C")

STATEMENTS_SOURCES = (
    "Sources - QIB (UK) plc's own entity Statement of Financial Position / Statement of Comprehensive "
    "Income / Statement of Changes in Equity, converted from £ to £m (divide by 1,000,000, round to 3 "
    "decimals):\n"
    "FY2025/FY2024 (own): Annual Report and Accounts 2025, pp.21-23 - " + AR["FY2025"] + "\n"
    "FY2023 (own): Annual Report and Accounts 2023, pp.20-22 - " + AR["FY2023"] + "\n"
    "FY2022 (own): Annual Report and Accounts 2022, pp.21-23 - " + AR["FY2022"] + "\n"
    "FY2021 (own): Annual Report and Accounts 2021, pp.18-20 - " + AR["FY2021"] + "\n"
    "FY2020 (own): Annual Report 2020, pp.19-22 - " + AR["FY2020"] + "\n"
    "FY2019 (own): Annual Report 2019, pp.13-15 - " + AR["FY2019"] + "\n"
    "FY2018 (own): Annual Report 2018, pp.15-17 - " + AR["FY2018"] + "\n"
    "FY2017 (own): Annual Report 2017, pp.15-17 - " + AR["FY2017"] + "\n"
    "FY2016 (own): Annual Report 2016, pp.11-13 - " + AR["FY2016"] + "\n"
    "FY2015 (own): Annual Report 2015, pp.11-13 - " + AR["FY2015"] + "\n"
    "FY2014 (own, Companies House scanned filing; cross-validated against FY2015 AR's own FY2014 "
    "comparative column, a native-text PDF): Annual Report 2014, pp.11-14 - " + AR["FY2014"] + "\n"
    "FY2013 (own, Companies House filing): Annual Report 2013, pp.10-13 - " + CH_FY2013 + "\n"
    "FY2012 (own, Companies House filing): Annual Report 2012, pp.11-14 - " + CH_FY2012 + "\n"
    "FY2011 (own, Companies House filing): Annual Report 2011, pp.11-14 - " + CH_FY2011 + "\n"
    "FY2010 (own, Companies House filing): Annual Report 2010, pp.10-13 - " + CH_FY2010 + "\n\n"
    "HD-074 (2026-09-06): FY2010-FY2013 figures are each independently cross-checked against the following "
    "year's own report's comparative column (e.g. FY2010's own figures tie exactly to FY2011 AR's own '2010' "
    "column; FY2012's own figures as originally published tie exactly to FY2011 AR's own equity roll-forward "
    "opening balance) - all four years reconcile without adjustment. FY2012 was later restated in FY2013's "
    "own AR (an additional £362,716 loss relating to a UK company financing exposure that entered "
    "administration after FY2012's accounts were approved); per this file's RESTATEMENT NOTE convention, "
    "FY2012's own originally-published figures are used here, not the later restatement.\n\n"
    + ENTITY + "\n\n"
    "RESTATEMENT NOTE: each year's own originally-published Balance Sheet figures are used throughout "
    "(project convention), not later restated comparatives. FY2024's Balance Sheet was later restated in "
    "AR2025 (Cash and balances with banks 82,316,418 vs FY2024's own 27,223,411; Financial assets at "
    "amortised cost 137,810,920 vs FY2024's own 192,903,927) - Note 2g attributes this to a reclassification "
    "of the Alternative Liquidity Facility from 'Financial assets at amortised cost' into 'Cash and balances "
    "with banks'; Total assets/equity are unaffected. FY2022's Balance Sheet was similarly restated in "
    "AR2023 (Financing arrangements 783,073,152 vs FY2022's own 777,848,982; Financial assets at amortised "
    "cost 150,714,519 vs FY2022's own 149,784,049; Other assets 950,771 vs FY2022's own 7,105,411) - a "
    "reclassification across three asset lines, net-zero on Total assets. FY2018's Balance Sheet was also "
    "restated in AR2019 (Derivative financial instruments asset 5,728,697 vs FY2018's own 5,371,224, plus a "
    "new 357,473 derivative financial instruments liability line not present in FY2018's own Balance Sheet; "
    "Other liabilities 17,022,415 vs FY2018's own 17,001,377) - a gross-up of derivative asset/liability "
    "presentation plus a small other-liabilities adjustment, net effect of £21,038 on Total equity (carried "
    "as an explicit restatement row on the Statement of Changes in Equity sheet rather than silently folded "
    "in). All of the above are genuine, Bank-disclosed reclassifications/restatements, not transcription "
    "errors.\n\n"
    "PRESENTATION NOTE: the Balance Sheet's 'Fair value adjustment for portfolio hedged risk' line and "
    "'Deferred tax liability' line only appear from FY2024 onward (FY2021-FY2023 instead carry a 'Deferred "
    "tax asset' line - a genuine sign flip in the Bank's net deferred tax position, not an omission). The "
    "P&L's 'Net gain/(loss) on financial assets at fair value' / 'at amortised cost' lines and the 'FV loss "
    "on investment property' line each appear only in some years, reflecting genuine year-on-year changes "
    "in what the Bank's own income statement discloses as a separate line - blank cells indicate a line "
    "not disclosed that year, not a zero.\n\n"
    "PRE-2018 PRESENTATION: FY2014-FY2017 report 'Financing arrangements' gross with a separate 'Less: "
    "impairment on financing arrangements' line, and hold treasury assets as 'Due from banks' plus "
    "'Financial assets held to maturity'/'available for sale' (IAS 39 categories); IFRS 9 adoption at "
    "FY2018 nets financing arrangements and reclassifies AFS/HTM into 'Financial assets at amortised "
    "cost'. The P&L's 'Income from financing and investing activities' is one combined line FY2014-FY2017, "
    "split into 'Income from financing activities'/'Income from investing activities' from FY2018. 'Rental "
    "income' (FY2016-FY2018) and 'Other income' (FY2014-FY2015, FY2019 onward) are the Bank's own labels "
    "for the same investment-property income line."
)

bs_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and balances with banks", m({"FY2025": 132462261, "FY2024": 27223411, "FY2023": 49246616, "FY2022": 59103924, "FY2021": 56338957, "FY2020": 41708029, "FY2019": 40776701, "FY2018": 37016753, "FY2017": 30751631, "FY2016": 16662446, "FY2015": 6096742, "FY2014": 5844014, "FY2013": 2829356, "FY2012": 4626245, "FY2011": 1455093, "FY2010": 2032596})),
    ("DATA", "Due from banks", m({"FY2016": 90861366, "FY2015": 69597214, "FY2014": 23576325, "FY2013": 78108642, "FY2012": 71412705, "FY2011": 52361914, "FY2010": 15305544})),
    ("DATA", "Financing arrangements", m({"FY2025": 954683460, "FY2024": 884059958, "FY2023": 826875369, "FY2022": 777848982, "FY2021": 726026105, "FY2020": 593879089, "FY2019": 530994682, "FY2018": 482374737, "FY2017": 403270277, "FY2016": 293012707, "FY2015": 227801665, "FY2014": 88981407, "FY2013": 36678167, "FY2012": 52464110, "FY2011": 36735640, "FY2010": 24611076})),
    ("DATA", "Less: impairment on financing arrangements", m({"FY2017": -4997014, "FY2016": -2750372, "FY2015": -625495, "FY2014": -679495, "FY2013": -2406587, "FY2012": -5279916, "FY2011": -1600661, "FY2010": -1487056})),
    ("DATA", "Financial assets held to maturity", m({"FY2017": 0, "FY2016": 2422970, "FY2015": 4067521, "FY2014": 6808055, "FY2013": 7344709, "FY2012": 7446552, "FY2011": 4210887})),
    ("DATA", "Financial assets available for sale", m({"FY2017": 69064158, "FY2016": 77665869, "FY2015": 87735905, "FY2014": 70549731, "FY2013": 22073787, "FY2012": 4242993, "FY2011": 1900693})),
    ("DATA", "Financial assets at amortised cost", m({"FY2025": 141472045, "FY2024": 192903927, "FY2023": 172313444, "FY2022": 149784049, "FY2021": 81553810, "FY2020": 67271228, "FY2019": 74814453, "FY2018": 66832272})),
    ("DATA", "Financial assets held for trading", m({"FY2013": 0, "FY2012": 25827202, "FY2011": 27006222})),
    ("DATA", "Derivative financial instruments", m({"FY2025": 1122065, "FY2024": 1597563, "FY2023": 617042, "FY2022": 989055, "FY2021": 1429382, "FY2020": 94702, "FY2019": 93764, "FY2018": 5371224, "FY2017": 0, "FY2016": 8127029, "FY2015": 923845, "FY2014": 650176, "FY2013": -42, "FY2012": -309, "FY2011": 2324368})),
    ("DATA", "Fair value adjustment for portfolio hedged risk", m({"FY2025": -1031227, "FY2024": -898730})),
    ("DATA", "Property and equipment", m({"FY2025": 15289209, "FY2024": 12810372, "FY2023": 12674423, "FY2022": 14126933, "FY2021": 12995170, "FY2020": 13545102, "FY2019": 14434772, "FY2018": 14836478, "FY2017": 15353959, "FY2016": 15826909, "FY2015": 16248792, "FY2014": 14724851, "FY2013": 368308, "FY2012": 467184, "FY2011": 600158, "FY2010": 744201})),
    ("DATA", "Intangible assets", m({"FY2025": 384806, "FY2023": 23300, "FY2022": 72221, "FY2021": 231069, "FY2020": 250722, "FY2019": 0, "FY2018": 11389, "FY2017": 80970, "FY2016": 200542, "FY2015": 295064, "FY2014": 61555, "FY2013": 38214, "FY2012": 63651, "FY2011": 49195, "FY2010": 130360})),
    ("DATA", "Investment property", m({"FY2025": 3100000, "FY2024": 6225000, "FY2023": 6225000, "FY2022": 7665000, "FY2021": 10240000, "FY2020": 10240000, "FY2019": 10240000, "FY2018": 10240000, "FY2017": 10240000, "FY2016": 9176071, "FY2015": 9511839, "FY2014": 9511839})),
    ("DATA", "Other assets", m({"FY2025": 2766848, "FY2024": 1527850, "FY2023": 1003932, "FY2022": 7105411, "FY2021": 4124393, "FY2020": 3926789, "FY2019": 3780006, "FY2018": 3651433, "FY2017": 3729134, "FY2016": 3033107, "FY2015": 3224444, "FY2014": 3153260, "FY2013": 2969495, "FY2012": 4279507, "FY2011": 3638142, "FY2010": 5061781})),
    ("DATA", "Deferred tax asset", m({"FY2023": 1500052, "FY2022": 2212189, "FY2021": 1792307, "FY2020": 1148521, "FY2019": 1031743, "FY2018": 1478710, "FY2017": 2274425, "FY2016": 2696072, "FY2015": 3316970, "FY2014": 3194647, "FY2013": 3198193, "FY2012": 3037095, "FY2011": 2366298, "FY2010": 2538899})),
    ("TOTAL", "Total assets", m({"FY2025": 1250249467, "FY2024": 1125449351, "FY2023": 1070479178, "FY2022": 1018907764, "FY2021": 894731193, "FY2020": 732064182, "FY2019": 676166121, "FY2018": 621812996, "FY2017": 529767540, "FY2016": 516934716, "FY2015": 428194506, "FY2014": 226376365, "FY2013": 151202242, "FY2012": 168587019, "FY2011": 131047949, "FY2010": 60143956})),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Due to banks", m({"FY2025": 108416644, "FY2024": 83641722, "FY2023": 103985098, "FY2022": 105266168, "FY2021": 120257356, "FY2020": 125332937, "FY2019": 85169482, "FY2018": 91504145, "FY2017": 72566143, "FY2016": 49438510, "FY2015": 134128955, "FY2014": 27358165, "FY2013": 53732703, "FY2012": 43528523, "FY2011": 25901549, "FY2010": 25875553})),
    ("DATA", "Due to customers", m({"FY2025": 969400662, "FY2024": 886390965, "FY2023": 827374599, "FY2022": 780208856, "FY2021": 657768467, "FY2020": 495173550, "FY2019": 480142212, "FY2018": 434542830, "FY2017": 366604600, "FY2016": 388377883, "FY2015": 216017303, "FY2014": 153139947, "FY2013": 67906240, "FY2012": 102819363, "FY2011": 81119886, "FY2010": 11433313})),
    ("DATA", "Other liabilities", m({"FY2025": 31877296, "FY2024": 27424980, "FY2023": 23695160, "FY2022": 29976993, "FY2021": 22889306, "FY2020": 18567055, "FY2019": 24281037, "FY2018": 17001377, "FY2017": 12851817, "FY2016": 11028773, "FY2015": 6213727, "FY2014": 2615160, "FY2013": 3392463, "FY2012": 3540475, "FY2011": 2194460, "FY2010": 1094374})),
    ("DATA", "Derivative financial instruments", m({"FY2025": 1646782, "FY2024": 593378, "FY2023": 816802, "FY2022": 1345231, "FY2021": 1289353, "FY2020": 5107456, "FY2019": 3406473, "FY2018": 0, "FY2017": 1694241})),
    ("DATA", "Deferred tax liability", m({"FY2025": 163967, "FY2024": 163136})),
    ("DATA", "Subordinated Wakala (FY2010/FY2011: 'Loan from related party', an unsubordinated related-party facility later formalised as a subordinated loan/Wakala - same underlying facility, continuous balance)", m({"FY2025": 14097755, "FY2024": 14133099, "FY2023": 14166072, "FY2022": 13700000, "FY2021": 13700000, "FY2020": 15950000, "FY2019": 15950000, "FY2018": 15950000, "FY2017": 15950000, "FY2016": 16200000, "FY2015": 16200000, "FY2014": 12757834, "FY2013": 9757834, "FY2012": 4757834, "FY2011": 4757834, "FY2010": 4757834})),
    ("TOTAL", "Total liabilities", m({"FY2025": 1125603106, "FY2024": 1012347280, "FY2023": 970037731, "FY2022": 930497248, "FY2021": 815904482, "FY2020": 660130998, "FY2019": 608949204, "FY2018": 558998352, "FY2017": 469666801, "FY2016": 465045166, "FY2015": 372559985, "FY2014": 195871106, "FY2013": 134789240, "FY2012": 154646195, "FY2011": 113973729, "FY2010": 43161074})),
    ("SECTION", "Equity", {}),
    ("DATA", "Share capital", m({"FY2025": 60864221, "FY2024": 60864221, "FY2023": 60864221, "FY2022": 60864221, "FY2021": 60864221, "FY2020": 60864221, "FY2019": 60864221, "FY2018": 60864221, "FY2017": 85807834, "FY2016": 79557834, "FY2015": 79557834, "FY2014": 56500000, "FY2013": 44000000, "FY2012": 25000001, "FY2011": 25000001, "FY2010": 25000001})),
    ("DATA", "Fair value reserve on AFS financial assets", m({"FY2017": -457745, "FY2016": -598538, "FY2015": -309485, "FY2014": 166916, "FY2013": -107909, "FY2012": 305549})),
    ("DATA", "Cash flow hedge reserve", m({"FY2025": -470073, "FY2024": -206240, "FY2023": -283405, "FY2022": -309566, "FY2021": -202208, "FY2020": -283898, "FY2019": -256373, "FY2018": -253137, "FY2017": -305737, "FY2016": -366086})),
    ("DATA", "Retained earnings", m({"FY2025": 64252213, "FY2024": 52444090, "FY2023": 39860631, "FY2022": 27855861, "FY2021": 18164698, "FY2020": 11352861, "FY2019": 6609069, "FY2018": 2203560, "FY2017": -24943613, "FY2016": -26703660, "FY2015": -23613828, "FY2014": -26161657, "FY2013": -27479089, "FY2012": -11364726, "FY2011": -7925781, "FY2010": -8017119})),
    ("TOTAL", "Total equity", m({"FY2025": 124646361, "FY2024": 113102071, "FY2023": 100441447, "FY2022": 88410516, "FY2021": 78826711, "FY2020": 71933184, "FY2019": 67216917, "FY2018": 62814644, "FY2017": 60100739, "FY2016": 51889550, "FY2015": 55634521, "FY2014": 30505259, "FY2013": 16413002, "FY2012": 13940824, "FY2011": 17074220, "FY2010": 16982882})),
    ("TOTAL", "Total liabilities and equity", m({"FY2025": 1250249467, "FY2024": 1125449351, "FY2023": 1070479178, "FY2022": 1018907764, "FY2021": 894731193, "FY2020": 732064182, "FY2019": 676166121, "FY2018": 621812996, "FY2017": 529767540, "FY2016": 516934716, "FY2015": 428194506, "FY2014": 226376365, "FY2013": 151202242, "FY2012": 168587019, "FY2011": 131047949, "FY2010": 60143956})),
]
bw.add_balance_sheet_sheet(
    title="QIB (UK) plc — Balance Sheet",
    subtitle="Entity basis, £m, converted from the Bank's reported £ amounts; FY2010-FY2025. Each year's "
              "own originally-published figures are used - see RESTATEMENT NOTE / PRE-2018 PRESENTATION "
              "note at bottom. HD-074: FY2010-FY2013 added from the Bank's own Companies House statutory "
              "accounts (each year's own figures, cross-verified against the next year's own comparative "
              "column) - real statutory floor confirmed FY2010; every year's own Total equity ties exactly "
              "to both its own Statement of Changes in Equity closing balance and the next year's opening "
              "balance across the whole FY2010-FY2025 chain, no restatement gaps.",
    rows=bs_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=66,
    source_height=520,
    unit_suffix=" (£m)",
)

pl_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Income from financing and investing activities", m({"FY2017": 17391144, "FY2016": 13599099, "FY2015": 11089315, "FY2014": 5786005, "FY2013": 5139758, "FY2012": 5540799, "FY2011": 2644263, "FY2010": 1081938})),
    ("DATA", "Income from financing activities", m({"FY2025": 65547275, "FY2024": 69270359, "FY2023": 60989079, "FY2022": 31605685, "FY2021": 21439036, "FY2020": 19808578, "FY2019": 20567967, "FY2018": 17726668})),
    ("DATA", "Income from investing activities", m({"FY2025": 7726355, "FY2024": 6228539, "FY2023": 4899705, "FY2022": 2535344, "FY2021": 1622287, "FY2020": 1807057, "FY2019": 1756532, "FY2018": 1143463})),
    ("DATA", "Returns to banks and customers", m({"FY2025": -45712749, "FY2024": -47998896, "FY2023": -37367914, "FY2022": -14860836, "FY2021": -7938424, "FY2020": -9690817, "FY2019": -10922693, "FY2018": -8503736, "FY2017": -7241968, "FY2016": -5712849, "FY2015": -3045370, "FY2014": -2496257, "FY2013": -3614608, "FY2012": -3299437, "FY2011": -1187821, "FY2010": -346682})),
    ("TOTAL", "Net income from financing and investing activities", m({"FY2025": 27560881, "FY2024": 27500002, "FY2023": 28520870, "FY2022": 19280193, "FY2021": 15122899, "FY2020": 11924818, "FY2019": 11401806, "FY2018": 10366395, "FY2017": 10149176, "FY2016": 7886250, "FY2015": 8043945, "FY2014": 3289748, "FY2013": 1525150, "FY2012": 2241362, "FY2011": 1456442, "FY2010": 735256})),
    ("DATA", "Fees and commissions income", m({"FY2025": 2489591, "FY2024": 2208209, "FY2023": 1823107, "FY2022": 1842222, "FY2021": 1611384, "FY2020": 1728470, "FY2019": 1816439, "FY2018": 1798526, "FY2017": 1378813, "FY2016": 1214184, "FY2015": 1113357, "FY2014": 1845823, "FY2013": 1210522, "FY2012": 4420906, "FY2011": 5797976, "FY2010": 4335075})),
    ("DATA", "Fees and commissions expense", m({"FY2025": -719061, "FY2024": -633508, "FY2023": -667574, "FY2022": -556172, "FY2021": -491526, "FY2020": -289355, "FY2019": -132005, "FY2018": -57746, "FY2017": -189859, "FY2016": -1190589, "FY2015": -880560, "FY2014": -450948, "FY2013": -228882, "FY2012": -316825, "FY2011": -538322, "FY2010": -137095})),
    ("TOTAL", "Net fees and commissions income", m({"FY2025": 1770530, "FY2024": 1574701, "FY2023": 1155533, "FY2022": 1286050, "FY2021": 1119858, "FY2020": 1439115, "FY2019": 1684434, "FY2018": 1740780, "FY2017": 1188954, "FY2016": 23595, "FY2015": 232797, "FY2014": 1394875, "FY2013": 981640, "FY2012": 4104081, "FY2011": 5259654, "FY2010": 4197980})),
    ("DATA", "Net gain/(loss) on financial assets at fair value", m({"FY2025": -323866, "FY2024": 28013})),
    ("DATA", "Net gain/(loss) on financial assets at amortised cost", m({"FY2025": 103987, "FY2024": 25681, "FY2021": 25475, "FY2020": 149745, "FY2019": 27132, "FY2018": -2190})),
    ("DATA", "Net gain/(loss) on financial assets at FVPL", m({"FY2021": 95289})),
    ("DATA", "Net gains/(losses) on financial assets classified as held for trading", m({"FY2012": 1472227, "FY2011": 730919, "FY2010": 235540})),
    ("DATA", "Net gain/(loss) on financial assets classified as AFS", m({"FY2017": -145408, "FY2016": 712361, "FY2015": 664505, "FY2014": 232643, "FY2013": -195062})),
    ("DATA", "Gain/(loss) on foreign exchange", m({"FY2025": 330256, "FY2024": 198849, "FY2023": 251062, "FY2022": 248560, "FY2021": 83629, "FY2020": 206809, "FY2019": 96171, "FY2018": 29050, "FY2017": 33803, "FY2016": -9405, "FY2015": -144845, "FY2014": -845914, "FY2013": -52714})),
    ("DATA", "Fair value gain on forward foreign exchange", m({"FY2015": 142127, "FY2014": 838599, "FY2013": 267, "FY2012": -824677, "FY2011": 824368})),
    ("DATA", "Rental income", m({"FY2018": 283557, "FY2017": 109922, "FY2016": 17950})),
    ("DATA", "Other income", m({"FY2025": 120181, "FY2024": 477869, "FY2023": 172981, "FY2022": 124170, "FY2021": 91934, "FY2020": 177986, "FY2019": 257577, "FY2015": 389300, "FY2014": 339647})),
    ("DATA", "FV loss on investment property", m({"FY2023": -1440000, "FY2022": -905000})),
    ("TOTAL", "Total operating income", m({"FY2025": 29561969, "FY2024": 29805115, "FY2023": 28660446, "FY2022": 20033973, "FY2021": 16539084, "FY2020": 13898473, "FY2019": 13467120, "FY2018": 12417592, "FY2017": 11336448, "FY2016": 8630751, "FY2015": 9327829, "FY2014": 5249598, "FY2013": 2259281, "FY2012": 8001119, "FY2011": 8271383, "FY2010": 5168776})),
    ("SECTION", "Expenses", {}),
    ("DATA", "Personnel expenses", m({"FY2025": -7814270, "FY2024": -7645092, "FY2023": -7169597, "FY2022": -6410143, "FY2021": -5758494, "FY2020": -5032706, "FY2019": -4875912, "FY2018": -4631460, "FY2017": -4568984, "FY2016": -3977155, "FY2015": -3714599, "FY2014": -3098242, "FY2013": -3347697, "FY2012": -3990183, "FY2011": -3936964, "FY2010": -3564158})),
    ("DATA", "Depreciation and amortisation", m({"FY2025": -376722, "FY2024": -569224, "FY2023": -608256, "FY2022": -692789, "FY2021": -695265, "FY2020": -665641, "FY2019": -637414, "FY2018": -762582, "FY2017": -769185, "FY2016": -747329, "FY2015": -901176, "FY2014": -133409, "FY2013": -142958, "FY2012": -199111, "FY2011": -286996, "FY2010": -529274})),
    ("DATA", "Other expenses", m({"FY2025": -3944957, "FY2024": -3334767, "FY2023": -2857395, "FY2022": -2558521, "FY2021": -2192538, "FY2020": -1925466, "FY2019": -2043621, "FY2018": -2262508, "FY2017": -2111124, "FY2016": -3143654, "FY2015": -2216100, "FY2014": -2499332, "FY2013": -3080026, "FY2012": -2742312, "FY2011": -3669879, "FY2010": -2018824})),
    ("DATA", "Exceptional item", m({"FY2016": -1384950})),
    ("TOTAL", "Total operating expenses", m({"FY2025": -12135949, "FY2024": -11549083, "FY2023": -10635248, "FY2022": -9661453, "FY2021": -8646297, "FY2020": -7623813, "FY2019": -7556947, "FY2018": -7656550, "FY2017": -7449293, "FY2016": -7868138, "FY2015": -6831875, "FY2014": -5730983, "FY2013": -6570681, "FY2012": -6931606, "FY2011": -7893839, "FY2010": -6112256})),
    ("TOTAL", "Profit/(loss) before provisions for impairment", m({"FY2025": 17426020, "FY2024": 18256032, "FY2023": 18025198, "FY2022": 10372520, "FY2021": 7892787, "FY2020": 6274660, "FY2019": 5910173, "FY2018": 4761042, "FY2017": 3887155, "FY2016": -622337, "FY2015": 2495954, "FY2014": -481385, "FY2013": -4311400, "FY2012": 1069513, "FY2011": 377544, "FY2010": -943480})),
    ("DATA", "Credit (loss)/reversal expense on financial assets", m({"FY2025": -1650686, "FY2024": -735091, "FY2023": -1048140, "FY2022": 638445, "FY2021": -661700, "FY2020": -831513, "FY2019": -563480, "FY2018": -1940})),
    ("DATA", "Provisions for impairment", m({"FY2017": -1724839, "FY2016": -1824275, "FY2015": 51000, "FY2014": 1727092, "FY2013": -7652242, "FY2012": -3679255, "FY2011": -113605, "FY2010": -562272})),
    ("DATA", "Impairment on building", m({"FY2023": -945738})),
    ("DATA", "Fair value loss related to impaired/wa'ad assets", m({"FY2013": -3949103, "FY2012": -1500000})),
    ("TOTAL", "Profit/(loss) before taxation", m({"FY2025": 15775334, "FY2024": 17520941, "FY2023": 16031320, "FY2022": 11010965, "FY2021": 7231087, "FY2020": 5443147, "FY2019": 5346693, "FY2018": 4759102, "FY2017": 2162316, "FY2016": -2446612, "FY2015": 2546954, "FY2014": 1245707, "FY2013": -15912745, "FY2012": -4109742, "FY2011": 263939, "FY2010": -1505752})),
    ("DATA", "Taxation", m({"FY2025": -4043683, "FY2024": -4918191, "FY2023": -4081371, "FY2022": -1318592, "FY2021": -375560, "FY2020": -699355, "FY2019": -920146, "FY2018": -1046242, "FY2017": -402269, "FY2016": -643220, "FY2015": 875, "FY2014": 71725, "FY2013": 161098, "FY2012": 670797, "FY2011": -172601, "FY2010": 298514})),
    ("TOTAL", "Profit/(loss) for the year", m({"FY2025": 11731651, "FY2024": 12602750, "FY2023": 11949949, "FY2022": 9692373, "FY2021": 6855527, "FY2020": 4743792, "FY2019": 4426547, "FY2018": 3712860, "FY2017": 1760047, "FY2016": -3089832, "FY2015": 2547829, "FY2014": 1317432, "FY2013": -15751647, "FY2012": -3438945, "FY2011": 91338, "FY2010": -1207238})),
    ("SECTION", "Other comprehensive income", {}),
    ("DATA", "Change in fair value of AFS financial assets net of tax", m({"FY2017": 140793, "FY2016": -289054, "FY2015": -476401, "FY2014": 274825, "FY2013": -413458, "FY2012": 305549})),
    ("DATA", "Change in fair value of cash flow hedge", m({"FY2025": -263833, "FY2024": 77165, "FY2023": 26161, "FY2022": -107358, "FY2021": 81691, "FY2020": -27525, "FY2019": -3236, "FY2018": 52600, "FY2017": 60349, "FY2016": -366086})),
    ("TOTAL", "Total comprehensive profit/(loss) for the year", m({"FY2025": 11467818, "FY2024": 12679915, "FY2023": 11976110, "FY2022": 9585015, "FY2021": 6937218, "FY2020": 4716267, "FY2019": 4423311, "FY2018": 3765460, "FY2017": 1961189, "FY2016": -3744972, "FY2015": 2071428, "FY2014": 1592257, "FY2013": -16165105, "FY2012": -3133396, "FY2011": 91338, "FY2010": -1207238})),
]
bw.add_income_statement_sheet(
    title="QIB (UK) plc — Profit & Loss",
    subtitle="Entity basis, £m, converted from the Bank's reported £ amounts; FY2010-FY2025. Each year's "
              "own originally-published figures are used - see PRESENTATION NOTE / PRE-2018 PRESENTATION "
              "note at bottom. HD-074: FY2010-FY2013 added (real statutory floor FY2010). DATA QUALITY "
              "NOTE: FY2012's own printed Statement of Comprehensive Income has no Other Comprehensive "
              "Income section at all (ends at 'Profit/(loss) for the year') even though FY2012's own "
              "Statement of Changes in Equity discloses a £305,549 'Net Change in fair value of AFS "
              "financial assets' equity movement that year - a genuine presentation gap in the Bank's own "
              "FY2012 AR, not a transcription omission here; that £305,549 is carried on this sheet's OCI "
              "section so the Total comprehensive income row ties to the Statement of Changes in Equity.",
    rows=pl_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=66,
    source_height=520,
    unit_suffix=" (£m)",
)

equity_headers = ["Share Capital", "Fair Value Reserve on AFS Financial Assets", "Cash Flow Hedge", "Retained Earnings", "Total"]
equity_rows = [
    ("DATA", "At 1 January 2010 (FY2010 opening, per FY2011 AR's own FY2010 comparative)", (25.000, None, None, -6.810, 18.190)),
    ("DATA", "Loss for the year", (None, None, None, -1.207, -1.207)),
    ("TOTAL", "At 31 December 2010", (25.000, None, None, -8.017, 16.983)),
    ("DATA", "Profit for the year", (None, None, None, 0.091, 0.091)),
    ("TOTAL", "At 31 December 2011", (25.000, None, None, -7.926, 17.074)),
    ("DATA", "Net Change in fair value of AFS financial assets (see DATA QUALITY NOTE on Profit & Loss sheet - not separately presented as OCI in FY2012's own printed Statement of Comprehensive Income)", (None, 0.306, None, None, 0.306)),
    ("DATA", "Loss for the year (own, as originally published - see RESTATEMENT NOTE)", (None, None, None, -3.439, -3.439)),
    ("TOTAL", "At 31 December 2012 (own, as originally published)", (25.000, 0.306, None, -11.365, 13.941)),
    ("DATA", "Share issuance", (19.000, None, None, None, 19.000)),
    ("DATA", "Net Change in fair value of AFS financial assets", (None, -0.413, None, None, -0.413)),
    ("DATA", "Loss for the year", (None, None, None, -15.752, -15.752)),
    ("TOTAL", "At 31 December 2013", (44.000, -0.108, None, -27.479, 16.413)),
    ("DATA", "At 1 January 2014 (FY2014 opening)", (44.000, -0.108, None, -27.479, 16.413)),
    ("DATA", "Share issuance", (12.500, None, None, None, 12.500)),
    ("DATA", "Change in fair value of AFS financial assets net of tax", (None, 0.275, None, None, 0.275)),
    ("DATA", "Profit for the year", (None, None, None, 1.317, 1.317)),
    ("TOTAL", "At 31 December 2014", (56.500, 0.167, None, -26.162, 30.505)),
    ("DATA", "Share issuance", (23.058, None, None, None, 23.058)),
    ("DATA", "Change in fair value of AFS financial assets net of tax", (None, -0.476, None, None, -0.476)),
    ("DATA", "Profit for the year", (None, None, None, 2.548, 2.548)),
    ("TOTAL", "At 31 December 2015", (79.558, -0.309, None, -23.614, 55.635)),
    ("DATA", "Change in fair value of AFS financial assets net of tax", (None, -0.289, None, None, -0.289)),
    ("DATA", "Changes in fair value of cash flow hedge foreign exchange", (None, None, -0.366, None, -0.366)),
    ("DATA", "Profit/(loss) for the year", (None, None, None, -3.090, -3.090)),
    ("TOTAL", "At 31 December 2016", (79.558, -0.599, -0.366, -26.704, 51.890)),
    ("DATA", "Share issuance", (6.250, None, None, None, 6.250)),
    ("DATA", "Change in fair value of AFS financial assets net of tax", (None, 0.141, None, None, 0.141)),
    ("DATA", "Changes in fair value of cash flow hedge foreign exchange", (None, None, 0.060, None, 0.060)),
    ("DATA", "Profit for the year", (None, None, None, 1.760, 1.760)),
    ("TOTAL", "At 31 December 2017", (85.808, -0.458, -0.306, -24.944, 60.101)),
    ("DATA", "IFRS 9 ECL allowance (transition)", (None, None, None, -1.809, -1.809)),
    ("DATA", "Movement in deferred tax related to AFS reserve", (None, -0.049, None, 0.049, None)),
    ("DATA", "Reclassification of AFS financial assets to amortised cost under IFRS 9", (None, 0.507, None, None, 0.507)),
    ("DATA", "Changes in deferred tax", (None, None, None, 0.251, 0.251)),
    ("DATA", "Capital restructuring", (-24.944, None, None, 24.944, None)),
    ("DATA", "Changes in fair value of cash flow hedge foreign exchange", (None, None, 0.053, None, 0.053)),
    ("DATA", "Profit for the year", (None, None, None, 3.713, 3.713)),
    ("TOTAL", "At 31 December 2018", (60.864, None, -0.253, 2.204, 62.815)),
    ("DATA", "Restatement of FY2018 opening balance (per FY2019 Annual Report Note 2 - see RESTATEMENT NOTE)", (None, None, None, -0.021, -0.021)),
    ("DATA", "Changes in fair value of cash flow hedge foreign exchange", (None, None, -0.003, None, -0.003)),
    ("DATA", "Profit for the year", (None, None, None, 4.427, 4.427)),
    ("TOTAL", "At 31 December 2019", (60.864, None, -0.256, 6.609, 67.217)),
    ("DATA", "Changes in fair value of cash flow hedge foreign exchange", (None, None, -0.028, None, -0.028)),
    ("DATA", "Profit for the year", (None, None, None, 4.744, 4.744)),
    ("TOTAL", "At 31 December 2020", (60.864, None, -0.284, 11.353, 71.933)),
    ("DATA", "At 1 January 2021 (FY2021 opening)", (60.864, None, -0.284, 11.353, 71.933)),
    ("DATA", "Changes in FV of cash flow hedge", (None, None, 0.082, None, 0.082)),
    ("DATA", "Movement in deferred tax relating to change in tax rate", (None, None, None, -0.044, -0.044)),
    ("DATA", "Profit for the year", (None, None, None, 6.856, 6.856)),
    ("TOTAL", "At 31 December 2021", (60.864, None, -0.202, 18.165, 78.827)),
    ("DATA", "Changes in FV of cash flow hedge", (None, None, -0.107, None, -0.107)),
    ("DATA", "Movement in deferred tax relating to change in tax rate", (None, None, None, -0.001, -0.001)),
    ("DATA", "Profit for the year", (None, None, None, 9.692, 9.692)),
    ("TOTAL", "At 31 December 2022", (60.864, None, -0.310, 27.856, 88.411)),
    ("DATA", "Changes in FV of cash flow hedge", (None, None, 0.026, None, 0.026)),
    ("DATA", "Movement in deferred tax relating to recognition or change in tax rate", (None, None, None, 0.055, 0.055)),
    ("DATA", "Profit for the year", (None, None, None, 11.950, 11.950)),
    ("TOTAL", "At 31 December 2023", (60.864, None, -0.283, 39.861, 100.441)),
    ("DATA", "Changes in FV of cash flow hedge", (None, None, 0.077, None, 0.077)),
    ("DATA", "Movement in deferred tax relating to recognition or change in tax rate", (None, None, None, -0.019, -0.019)),
    ("DATA", "Profit for the year", (None, None, None, 12.603, 12.603)),
    ("TOTAL", "At 31 December 2024", (60.864, None, -0.206, 52.444, 113.102)),
    ("DATA", "Changes in FV of cash flow hedge", (None, None, -0.264, None, -0.264)),
    ("DATA", "Movement in deferred tax on cash flow hedge", (None, None, None, 0.076, 0.076)),
    ("DATA", "Profit for the year", (None, None, None, 11.732, 11.732)),
    ("TOTAL", "At 31 December 2025", (60.864, None, -0.470, 64.252, 124.646)),
]
bw.add_equity_changes_sheet(
    title="QIB (UK) plc — Statement of Changes in Equity",
    subtitle="Chronological roll-forward oldest to newest, entity basis, £m, FY2010-FY2025. Equity "
              "reconciliation ladder confirmed: every year's own closing balance ties exactly to both the "
              "next year's own opening balance and that year's own Balance Sheet Total equity, with one "
              "exception - a single explicit £21,038 restatement row is carried between FY2018's own "
              "closing balance and FY2019's own opening balance (see RESTATEMENT NOTE on the Balance "
              "Sheet/P&L sheets); no other plug rows are needed anywhere across all 16 years - HD-074's "
              "FY2010-FY2013 extension ties exactly into the pre-existing FY2014 opening row with no gap. "
              "The Fair Value Reserve on AFS Financial Assets column is populated FY2012-FY2018 (blank "
              "before FY2012 and after FY2018, once the FY2018 IFRS 9 capital restructuring eliminated the "
              "AFS category); the Cash Flow Hedge column only exists from FY2016 onward. The deferred-tax "
              "movement row's label changes across years (the Bank's own wording); all years' rows "
              "represent the same underlying deferred tax adjustment on the relevant reserve/retained "
              "earnings.",
    headers=equity_headers,
    rows=equity_rows,
    sources_text=STATEMENTS_SOURCES,
)

rows = [
 ("SECTION", "Operating activities", {}),
 ("DATA", "Profit/(loss) for the year", m({"FY2025":11731651,"FY2024":12602750,"FY2023":11949949,"FY2022":9692373,"FY2021":6855527,"FY2020":4743792,"FY2019":4426546,"FY2018":3712860,"FY2017":1760047,"FY2016":-3089832,"FY2015":2547829,"FY2014":1317432,"FY2013":-15751647,"FY2012":-3438945,"FY2011":91338,"FY2010":-1207238})),
 ("DATA", "Depreciation", m({"FY2025":365521,"FY2024":545924,"FY2023":559334,"FY2022":533941,"FY2021":559611,"FY2020":555383,"FY2019":626025,"FY2018":688272,"FY2017":637431,"FY2016":603046,"FY2015":861601,"FY2014":105777,"FY2013":111359,"FY2012":164489,"FY2011":183157,"FY2010":218908})),
 ("DATA", "Amortisation", m({"FY2025":11201,"FY2024":23300,"FY2023":48921,"FY2022":158848,"FY2021":135654,"FY2020":110258,"FY2019":11389,"FY2018":74311,"FY2017":131754,"FY2016":142719,"FY2015":39575,"FY2014":27632,"FY2013":31599,"FY2012":34622,"FY2011":103839,"FY2010":310366})),
 ("DATA", "Fair Value on Building", m({"FY2017":-1063929,"FY2016":335768})),
 ("DATA", "ECL loss allowance and write-offs", m({"FY2020":877573,"FY2019":620430,"FY2018":-37271})),
 ("DATA", "Taxation", m({"FY2025":4043683,"FY2024":4918194,"FY2023":4081371,"FY2022":1318592,"FY2021":375560,"FY2020":699355,"FY2019":920146,"FY2018":1046242,"FY2017":402269,"FY2016":643220,"FY2015":-875,"FY2014":-71725,"FY2013":-161098,"FY2012":-670797,"FY2011":172601,"FY2010":-298514})),
 ("DATA", "Fair value / impairment adjustments", m({"FY2025":1783183,"FY2024":898730,"FY2023":2383878,"FY2022":1490529,"FY2021":760690})),
 ("DATA", "Increase/(decrease) in impairments on financing arrangements", m({"FY2019":-56950,"FY2018":-87867,"FY2017":2246642,"FY2016":2124876,"FY2015":-54000,"FY2014":-1727092,"FY2013":-3869545,"FY2012":3679255,"FY2011":113605,"FY2010":562272})),
 ("DATA", "(Increase)/decrease in amounts due from banks", m({"FY2017":90861366,"FY2016":-21264152,"FY2015":-46020889,"FY2014":54532317,"FY2013":-6695937,"FY2012":-19050791,"FY2011":-37056370,"FY2010":3864195})),
 ("DATA", "Increase/(decrease) in financing arrangements", m({"FY2025":-72273531,"FY2024":-57921880,"FY2023":-44846764,"FY2022":-51177541,"FY2021":-133182070,"FY2020":-63502402,"FY2019":-49113784,"FY2018":-85674969,"FY2017":-110257569,"FY2016":-65211042,"FY2015":-138820258,"FY2014":-52303240,"FY2013":16419443,"FY2012":-15728470,"FY2011":-12124564,"FY2010":-2135767})),
 ("DATA", "Stage 3 ECL recoveries", m({"FY2024":0,"FY2023":-3750,"FY2022":-1223974,"FY2021":-3700,"FY2020":-46061})),
 ("DATA", "Increase/(decrease) in other assets", m({"FY2025":-1238998,"FY2024":-523919,"FY2023":-53161,"FY2022":-2981020,"FY2021":-183119,"FY2020":-146783,"FY2019":-128572,"FY2018":77700,"FY2017":-696030,"FY2016":191339,"FY2015":-71184,"FY2014":-183765,"FY2013":1310012,"FY2012":-641365,"FY2011":1423639,"FY2010":-2711066})),
 ("DATA", "Increase/(decrease) in amounts due to banks", m({"FY2025":24774922,"FY2024":-20343376,"FY2023":-2185645,"FY2022":-14991188,"FY2021":-5075581,"FY2020":40163454,"FY2019":-6334662,"FY2018":18938002,"FY2017":23127632,"FY2016":-84690446,"FY2015":106770791,"FY2014":-26374538,"FY2013":10204180,"FY2012":17626974,"FY2011":25996,"FY2010":7348801})),
 ("DATA", "Increase/(decrease) in amounts due to customers", m({"FY2025":83009697,"FY2024":59016367,"FY2023":41134935,"FY2022":122440389,"FY2021":162594916,"FY2020":15031338,"FY2019":45599382,"FY2018":67938230,"FY2017":-21773283,"FY2016":172360580,"FY2015":62877356,"FY2014":85233707,"FY2013":-34913123,"FY2012":21699477,"FY2011":69686573,"FY2010":3757028})),
 ("DATA", "Increase/(decrease) in other liabilities", m({"FY2025":539841,"FY2024":458933,"FY2023":-2293547,"FY2022":5356669,"FY2021":3613140,"FY2020":-6738617,"FY2019":6658681,"FY2018":4059147,"FY2017":1823046,"FY2016":4815047,"FY2015":3581353,"FY2014":-777303,"FY2013":-148012,"FY2012":1346015,"FY2011":1100086,"FY2010":322289})),
 ("DATA", "(Increase)/decrease in financial assets held to maturity", m({"FY2017":2422970,"FY2016":1644551,"FY2015":2740534,"FY2014":536654,"FY2013":101843,"FY2012":-3235665,"FY2011":-4210887})),
 ("DATA", "Increase/(decrease) in financial assets available for sale", m({"FY2017":8822231,"FY2016":9392574,"FY2015":-17766811,"FY2014":-48125848,"FY2013":-18244252,"FY2012":-2036751,"FY2011":-1900693})),
 ("DATA", "Increase/(decrease) in financial assets at amortised cost", m({"FY2025":-3660555,"FY2024":-20589713,"FY2023":-21599498,"FY2022":-68236950,"FY2021":-14259831,"FY2020":7544997,"FY2019":-7998849,"FY2018":2771857})),
 ("DATA", "(Increase)/decrease in financial assets held for trading", m({"FY2013":25827202,"FY2012":1179020,"FY2011":-15799667,"FY2010":-11206555})),
 ("DATA", "Increase/(decrease) in derivative financial instruments", m({"FY2025":1265068,"FY2024":-1126779,"FY2023":-130255,"FY2022":388846,"FY2021":-5152783,"FY2020":1700045,"FY2019":8683933,"FY2018":-7065464,"FY2017":9821270,"FY2016":-7203184,"FY2015":-273669,"FY2014":-650218,"FY2013":-267,"FY2012":2324677,"FY2011":-2324368})),
 ("DATA", "Source operating subtotal reconciliation (see source note)", m({"FY2024":735088,"FY2023":1050000})),
 ("TOTAL", "Net cash inflow/(outflow) from operating activities", m({"FY2025":50351683,"FY2024":-21306381,"FY2023":-9904232,"FY2022":2769514,"FY2021":17038014,"FY2020":992332,"FY2019":3913714,"FY2018":6441050,"FY2017":8265847,"FY2016":10795064,"FY2015":-23588647,"FY2014":11539790,"FY2013":-25778243,"FY2012":3251745,"FY2011":-515715,"FY2010":-1175281})),
 ("SECTION", "Investing activities", {}),
 ("DATA", "Purchase of property, plant and equipment", m({"FY2025":-65532,"FY2024":-685282,"FY2023":-54715,"FY2022":-4369,"FY2021":-37762,"FY2020":0,"FY2019":-153801,"FY2018":-170791,"FY2017":-164480,"FY2016":-181163,"FY2015":-2385542,"FY2014":-23974159,"FY2013":-12483,"FY2012":-31515,"FY2011":-39114,"FY2010":-21782})),
 ("DATA", "Purchase of intangible assets", m({"FY2025":-103738,"FY2021":-116000,"FY2020":-60980,"FY2019":0,"FY2018":-4729,"FY2017":-12182,"FY2016":-48197,"FY2015":-273084,"FY2014":-50973,"FY2013":-6162,"FY2012":-49078,"FY2011":-22674,"FY2010":-50864})),
 ("TOTAL", "Net cash outflow from investing activities", m({"FY2025":-169270,"FY2024":-685282,"FY2023":-54715,"FY2022":-4369,"FY2021":-153762,"FY2020":-60980,"FY2019":-153801,"FY2018":-175520,"FY2017":-176662,"FY2016":-229360,"FY2015":-2658626,"FY2014":-24025132,"FY2013":-18645,"FY2012":-80593,"FY2011":-61788,"FY2010":-72646})),
 ("SECTION", "Financing activities", {}),
 ("DATA", "Repayment/(increase) of subordinated Wakala", m({"FY2025":-35344,"FY2024":-32973,"FY2023":100909,"FY2021":-2250000,"FY2017":-250000})),
 ("DATA", "Proceeds from issuance of ordinary shares", m({"FY2017":6250000,"FY2016":0,"FY2015":23057834,"FY2014":12500000,"FY2013":18999999})),
 ("DATA", "Proceeds from subordinated loans/Wakala", m({"FY2016":0,"FY2015":3442166,"FY2014":3000000,"FY2013":5000000})),
 ("TOTAL", "Net cash (outflow)/inflow from financing activities", m({"FY2025":-35344,"FY2024":-32973,"FY2023":100909,"FY2022":0,"FY2021":-2250000,"FY2020":0,"FY2019":0,"FY2018":0,"FY2017":6000000,"FY2016":0,"FY2015":26500000,"FY2014":15500000,"FY2013":23999999,"FY2012":0,"FY2011":0,"FY2010":0})),
 ("TOTAL", "Net increase/(decrease) in cash and cash equivalents", m({"FY2025":50147069,"FY2024":-22024636,"FY2023":-9858038,"FY2022":2765145,"FY2021":14634252,"FY2020":931352,"FY2019":3759913,"FY2018":6265530,"FY2017":14089185,"FY2016":10565704,"FY2015":252728,"FY2014":3014658,"FY2013":-1796889,"FY2012":3171152,"FY2011":-577503,"FY2010":-1247927})),
 ("DATA", "Cash and cash equivalents at start of year", m({"FY2025":82318198,"FY2024":49249786,"FY2023":59107824,"FY2022":56342679,"FY2021":41708427,"FY2020":40777075,"FY2019":37017161,"FY2018":30751631,"FY2017":16662446,"FY2016":6096742,"FY2015":5844014,"FY2014":2829356,"FY2013":4626245,"FY2012":1455093,"FY2011":2032596,"FY2010":3280523})),
 ("TOTAL", "Cash and cash equivalents at end of year", m({"FY2025":132465267,"FY2024":27225150,"FY2023":49249786,"FY2022":59107824,"FY2021":56342679,"FY2020":41708427,"FY2019":40777075,"FY2018":37017161,"FY2017":30751631,"FY2016":16662446,"FY2015":6096742,"FY2014":5844014,"FY2013":2829356,"FY2012":4626245,"FY2011":1455093,"FY2010":2032596})),
]
bw.add_cash_flow_sheet(title="QIB (UK) plc — Statement of Cash Flows", subtitle="Entity basis, £m, converted from the Bank's reported £ amounts; FY2010-FY2025. HD-074: FY2010-FY2013 added (real statutory floor FY2010); the FY2013 closing cash figure ties exactly to the pre-existing FY2014 opening cash figure.", rows=rows, sources_text=CASH_SOURCES, first_col_width=66, source_height=340, unit_suffix=" (£m)")

ASSET_QUALITY_SOURCES = (
    "Sources - QIB (UK) plc's own Annual Report, 'ECL breakdown' / 'Credit Quality' IFRS 9 stage 1/2/3 "
    "table for Financing Arrangements (Murabaha financing):\n"
    "FY2025 (own): Annual Report and Accounts 2025, p.55 - " + AR["FY2025"] + "\n"
    "FY2024 (own): Annual Report and Accounts 2024, p.56 - " + AR["FY2024"] + "\n"
    "FY2023 (own): Annual Report and Accounts 2023, p.54 - " + AR["FY2023"] + "\n"
    "FY2022 (own): Annual Report and Accounts 2022, p.55 - " + AR["FY2022"] + "\n"
    "FY2021 (own): Annual Report and Accounts 2021, p.51 - " + AR["FY2021"] + "\n"
    "FY2020 (own): Annual Report 2020, p.51 - " + AR["FY2020"] + "\n"
    "FY2019 (own): Annual Report 2019, p.34 - " + AR["FY2019"] + "\n"
    "FY2018 (own): Annual Report 2018, p.39 - " + AR["FY2018"] + "\n\n"
    + ENTITY + "\n\n"
    "DATA QUALITY FLAG: the Bank's own note states these are the 'maximum credit exposure, including "
    "accrued profit' - for FY2019/FY2020/FY2021/FY2022 this note's own Total financing arrangements net "
    "figure (533,463,912 / 596,343,819 / 728,703,868 / 783,073,152) does NOT tie to that same year's own "
    "Balance Sheet 'Financing arrangements' line (530,994,682 / 593,879,089 / 726,026,105 / 777,848,982) - "
    "a genuine internal inconsistency within each of those Annual Reports (the accrued-profit basis "
    "difference the note itself flags), not a transcription error here. FY2018's own note ties exactly to "
    "the Balance Sheet (482,374,737 both); FY2023 onward this note's total also ties exactly to the "
    "Balance Sheet.\n\n"
    "FY2014-FY2017: QIB (UK) had not yet adopted IFRS 9 (effective FY2018) and its Annual Reports for "
    "these years report impairment under IAS 39 ('individually assessed'/'collectively assessed' "
    "provisions on the aggregate financing book), not the IFRS 9 Stage 1/2/3 categorisation used in this "
    "sheet - cells are left blank for FY2014-FY2017 rather than force-mapped onto a staging basis the "
    "Bank itself did not use that year."
)
asset_quality_rows = [
    ("SECTION", "Financing arrangements (Murabaha financing), gross carrying amount by IFRS 9 stage", {}),
    ("DATA", "Stage 1", m({"FY2025": 849001016, "FY2024": 768728253, "FY2023": 768684249, "FY2022": 761510966, "FY2021": 719077654, "FY2020": 587129363, "FY2019": 524063374, "FY2018": 479180025})),
    ("DATA", "Stage 2", m({"FY2025": 94122611, "FY2024": 109923252, "FY2023": 60853408, "FY2022": 23168677, "FY2021": 5856639, "FY2020": 5100718, "FY2019": 11718362, "FY2018": 4961747})),
    ("DATA", "Stage 3", m({"FY2025": 16609442, "FY2024": 8808032, "FY2023": 0, "FY2022": 7500, "FY2021": 7810910, "FY2020": 10962407, "FY2019": 4746525, "FY2018": 4803475})),
    ("TOTAL", "Total gross carrying amount", m({"FY2025": 959733069, "FY2024": 887459537, "FY2023": 829537657, "FY2022": 784687143, "FY2021": 732745203, "FY2020": 603192488, "FY2019": 540528261, "FY2018": 488945247})),
    ("SECTION", "ECL allowance by IFRS 9 stage", {}),
    ("DATA", "Stage 1", m({"FY2025": -832670, "FY2024": -933355, "FY2023": -1079806, "FY2022": -890540, "FY2021": -746630, "FY2020": -1707802, "FY2019": -552018, "FY2018": -1289498})),
    ("DATA", "Stage 2", m({"FY2025": -553439, "FY2024": -2455724, "FY2023": -1582482, "FY2022": -715951, "FY2021": -281223, "FY2020": -80840, "FY2019": -1765807, "FY2018": -477537})),
    ("DATA", "Stage 3", m({"FY2025": -3663500, "FY2024": -10500, "FY2023": 0, "FY2022": -7500, "FY2021": -3013482, "FY2020": -5060027, "FY2019": -4746525, "FY2018": -4803475})),
    ("TOTAL", "Total ECL allowance", m({"FY2025": -5049609, "FY2024": -3399579, "FY2023": -2662288, "FY2022": -1613991, "FY2021": -4041335, "FY2020": -6848669, "FY2019": -7064349, "FY2018": -6570510})),
    ("TOTAL", "Net financing arrangements (per this note)", m({"FY2025": 954683460, "FY2024": 884059958, "FY2023": 826875369, "FY2022": 783073152, "FY2021": 728703868, "FY2020": 596343819, "FY2019": 533463912, "FY2018": 482374737})),
    ("SECTION", "Asset quality ratios (derived)", {}),
    ("DATA", "Stage 3 as % of total gross carrying amount (NPL ratio)",
     {"FY2025": "1.73%", "FY2024": "0.99%", "FY2023": "0.00%", "FY2022": "0.00%", "FY2021": "1.07%", "FY2020": "1.82%", "FY2019": "0.88%", "FY2018": "0.98%"}),
    ("DATA", "Total ECL allowance as % of total gross carrying amount (coverage)",
     {"FY2025": "0.53%", "FY2024": "0.38%", "FY2023": "0.32%", "FY2022": "0.21%", "FY2021": "0.55%", "FY2020": "1.14%", "FY2019": "1.31%", "FY2018": "1.34%"}),
]
bw.add_asset_quality_sheet(
    title="QIB (UK) plc — Asset Quality",
    subtitle="Financing arrangements (Murabaha financing), IFRS 9 stage 1/2/3 gross carrying amount and "
              "ECL allowance. Entity basis, £m, FY2018-FY2025 (FY2014-FY2017 blank - pre-IFRS 9, see "
              "source note). See DATA QUALITY FLAG at bottom for several years' own internal "
              "note-vs-Balance Sheet basis difference.",
    rows=asset_quality_rows,
    sources_text=ASSET_QUALITY_SOURCES,
    first_col_width=76,
    source_height=440,
    unit_suffix=" (£m)",
    years=PILLAR3_YEARS,
)

def metric(name, unit, data, note=None): bw.add_metric_sheet(name, unit, data, p3_sources(), note=note, first_col_width=50, source_height=340, years=PILLAR3_YEARS)
cap={"FY2025":124.259,"FY2024":113.099,"FY2023":98.878,"FY2022":86.739,"FY2021":78.028,"FY2020":72.249,"FY2019":68.279,"FY2018":63,"FY2017":58,"FY2016":49,"FY2015":49.1,"FY2014":25.9}
total={"FY2025":137.959,"FY2024":126.799,"FY2023":112.578,"FY2022":96.585,"FY2021":91.081,"FY2020":85.440,"FY2019":80.129,"FY2018":79,"FY2017":74,"FY2016":65,"FY2015":65.3,"FY2014":38.7}
rwa={"FY2025":693.154,"FY2024":601.928,"FY2023":543.184,"FY2022":499.121,"FY2021":462.020,"FY2020":418.084,"FY2019":375.285,"FY2018":354,"FY2017":335,"FY2016":264}
ratios={
 "CET1 Ratio":{"FY2025":"17.93%","FY2024":"18.79%","FY2023":"18.20%","FY2022":"17.38%","FY2021":"16.89%","FY2020":"17.28%","FY2019":"18.19%","FY2018":"18%","FY2017":"17%","FY2016":"19%"},
 "Total Capital Ratio":{"FY2025":"19.90%","FY2024":"21.07%","FY2023":"20.73%","FY2022":"19.35%","FY2021":"19.71%","FY2020":"20.44%","FY2019":"21.35%","FY2018":"22%","FY2017":"22%","FY2016":"25%"},
 "Leverage Ratio":{"FY2025":"10.67%","FY2024":"10.53%","FY2023":"9.61%","FY2022":"8.50%","FY2021":"8.75%","FY2020":"9.85%","FY2019":"10.00%"},
 "LCR":{"FY2025":"345.59%","FY2024":"322.05%","FY2023":"1153.62%","FY2022":"1236.14%","FY2021":"555.60%","FY2020":"242.03%","FY2019":"683.74%"},
 "NSFR":{"FY2025":"127.95%","FY2024":"128.20%","FY2023":"130.56%","FY2022":"129.18%","FY2021":"119.68%"},
}

# ---------------------------------------------------------------
# KM1 Key Metrics - QIB (UK)'s own "Template UK KM1 - Key metrics template",
# reproduced as printed. KM1-024, 16 September 2026.
#
# UNIT: £'000, NOT the £m used by every other sheet in this workbook. Each of
# the FY2023/FY2024/FY2025 editions states it in terms on its own p.4 ("All
# figures in tables are in thousands of pounds, unless stated otherwise"), and
# the FY2022 edition's figures agree digit-for-digit with the FY2023 edition's
# comparative column, which is explicitly £'000. The template is reproduced in
# the Bank's own unit rather than restated into £m - the £m figures on the 11
# metric sheets are this project's conversion, not QIB's printing.
#
# WHICH EDITIONS CARRY THE TEMPLATE. Only FY2022 onward:
#   FY2025/FY2024/FY2023 - text-native PDFs, "Template UK KM1" at printed p.6.
#   FY2022 - the SAME template, but the whole document is a Konica Minolta
#     SCAN with no text layer at all, which is why an earlier text-only survey
#     recorded it as absent. Located by reading the document's OWN contents
#     page (printed p.6, KM1; p.8, OV1 - so the table spans pp.6-7), not by any
#     page-density heuristic, then rendered and read by eye. Transcribed TWICE
#     from two independent renderings - the full page at 300dpi (pdftoppm) and
#     the embedded 2056x2960 CCITT stencil at native resolution (pdfimages) -
#     with digit-for-digit agreement before use.
#   FY2021/FY2020 - Pillar 3 IS published, and each carries a table headed
#     "As at 31 December 20XX, the Bank's key metrics were:", but that is a
#     BESPOKE 12-line summary of the Bank's own design (its own headings
#     "Available Capital (£'000s)" / "Capital Ratios as a percentage of RWA" /
#     "Leverage Ratio" / "Liquidity Coverage Ratio", no template row numbers,
#     no SREP rows, no buffer rows, no cash in/outflow rows, no NSFR, and a
#     "Profit/(Loss) after taxation" line that is not a KM1 row at all). It
#     fails the row-set test, so it is NOT the template and is not mapped onto
#     template row numbers here. NOTE the FY2021 edition prints that table as
#     an EMBEDDED IMAGE inside an otherwise text-native PDF, so text extraction
#     returns the heading and then nothing; it was rendered at 300dpi and read.
#   FY2020 and earlier - see the metric sheets; no template.
#
# FY2021 IS FILLED FROM THE FY2022 EDITION'S COMPARATIVE; FY2020-FY2014 ARE
# BLANK. Revised 17 September 2026 under KM1-035 / map rule 28, superseding
# this script's previous treatment, which left FY2021 blank and quoted the
# comparative in prose instead. FY2021's own edition prints NO KM1 template at
# all, so there is no own-edition disclosure for a comparative to displace -
# which is what distinguishes this from rule 20, where a bank's own table
# exists and dashes a row. The FY2022 edition's column b (31/12/2021) carries
# the full template and is not a restatement: it agrees with the FY2021
# edition's own bespoke table on every one of the ten overlapping lines.
# FY2020 and earlier stay blank because NO edition anywhere prints them in
# template form - the FY2021 edition's 31/12/20 comparative is the same bespoke
# 12-line shape, not the template (rule 28 condition (c)).
#
# ROWS 14a-14e ARE A STATED EXCLUSION, not a gap: every edition prints, under
# the table, "Rows 14a-14e have been removed as only LREQ firms are required to
# disclose this information". They are therefore not printed and not shown.
#
# TWO CROSS-EDITION DIVERGENCES, recorded and NOT reconciled (each cell below
# comes from the edition in which that year is the reporting year):
#   row 4 FY2024 - FY2024 edition prints 601,928; FY2025 edition's comparative
#     prints 601,927.
#   row 14 FY2022 - FY2022 edition prints 8.50%; FY2023 edition's comparative
#     prints 8.57%.
# ---------------------------------------------------------------
# KM1-035 (17 September 2026), map rule 28: FY2021 is FILLED from the FY2022
# edition's comparative column b (31/12/2021), because FY2021's OWN edition
# prints no KM1 template at all - see the sheet note for the positive evidence.
# This is rule 28, NOT rule 20: rule 20 governs a row dashed inside a table the
# bank did print, and there is no FY2021 table here to have dashed anything.
# Every one of the 28 values below was read off a 300dpi rendering of the
# scanned FY2022 edition (printed pp.6-7) rather than copied from this script's
# own prior quotation of them.
km1_rows = [
    ("SECTION", "Available own funds (amounts, £'000)", {}),
    ("DATA", "1    Common Equity Tier 1 (CET1) capital",
     {"FY2025": 124259, "FY2024": 113099, "FY2023": 98878, "FY2022": 86739, "FY2021": 78028}),
    ("DATA", "2    Tier 1 capital",
     {"FY2025": 124259, "FY2024": 113099, "FY2023": 98878, "FY2022": 86739, "FY2021": 78028}),
    ("DATA", "3    Total capital",
     {"FY2025": 137959, "FY2024": 126799, "FY2023": 112578, "FY2022": 96585, "FY2021": 91081}),
    ("SECTION", "Risk-weighted exposure amounts (£'000)", {}),
    ("DATA", "4    Total risk-weighted exposure amount",
     {"FY2025": 693154, "FY2024": 601928, "FY2023": 543184, "FY2022": 499121, "FY2021": 462020}),
    ("SECTION", "Capital ratios (as a percentage of risk-weighted exposure amount)", {}),
    ("DATA", "5    Common Equity Tier 1 ratio (%)",
     {"FY2025": "17.93%", "FY2024": "18.79%", "FY2023": "18.20%", "FY2022": "17.38%", "FY2021": "16.89%"}),
    ("DATA", "6    Tier 1 ratio (%)",
     {"FY2025": "17.93%", "FY2024": "18.79%", "FY2023": "18.20%", "FY2022": "17.38%", "FY2021": "16.89%"}),
    ("DATA", "7    Total capital ratio (%)",
     {"FY2025": "19.90%", "FY2024": "21.07%", "FY2023": "20.73%", "FY2022": "19.35%", "FY2021": "19.71%"}),
    ("SECTION", "Additional own funds requirements based on SREP (as a percentage of risk-weighted exposure amount)", {}),
    ("DATA", "UK 7a    Additional CET1 SREP requirements (%)",
     {"FY2025": "2.56%", "FY2024": "2.56%", "FY2023": "1.86%", "FY2022": "1.86%", "FY2021": "1.86%"}),
    ("DATA", "UK 7b    Additional AT1 SREP requirements (%)",
     {"FY2025": "N/A", "FY2024": "N/A", "FY2023": "N/A", "FY2022": "N/A", "FY2021": "N/A"}),
    ("DATA", "UK 7c    Additional T2 SREP requirements (%)",
     {"FY2025": "1.14%", "FY2024": "1.14%", "FY2023": "0.83%", "FY2022": "0.83%", "FY2021": "0.83%"}),
    ("DATA", "UK 7d    Total SREP own funds requirements (%)",
     {"FY2025": "12.55%", "FY2024": "12.55%", "FY2023": "11.30%", "FY2022": "11.30%", "FY2021": "11.30%"}),
    ("SECTION", "Combined buffer requirement (as a percentage of risk-weighted exposure amount)", {}),
    ("DATA", "8    Capital conservation buffer (%)",
     {"FY2025": "2.50%", "FY2024": "2.50%", "FY2023": "2.50%", "FY2022": "2.50%", "FY2021": "2.50%"}),
    ("DATA", "UK 8a    Conservation buffer due to macro-prudential or systemic risk identified at the level of a Member State (%)",
     {"FY2025": "N/A", "FY2024": "N/A", "FY2023": "N/A", "FY2022": "N/A", "FY2021": "N/A"}),
    # FY2021's 0.00% is a PRINTED ZERO, not a dash (map rule 2) - recorded as the zero.
    ("DATA", "9    Institution specific countercyclical capital buffer (%)",
     {"FY2025": "1.18%", "FY2024": "1.14%", "FY2023": "0.98%", "FY2022": "1.00%", "FY2021": "0.00%"}),
    ("DATA", "UK 9a    Systemic risk buffer (%)",
     {"FY2025": "N/A", "FY2024": "N/A", "FY2023": "N/A", "FY2022": "N/A", "FY2021": "N/A"}),
    ("DATA", "10    Global Systemically Important Institution buffer (%)",
     {"FY2025": "N/A", "FY2024": "N/A", "FY2023": "N/A", "FY2022": "N/A", "FY2021": "N/A"}),
    ("DATA", "UK 10a    Other Systemically Important Institution buffer",
     {"FY2025": "N/A", "FY2024": "N/A", "FY2023": "N/A", "FY2022": "N/A", "FY2021": "N/A"}),
    ("DATA", "11    Combined buffer requirement (%)",
     {"FY2025": "3.68%", "FY2024": "3.64%", "FY2023": "3.48%", "FY2022": "3.50%", "FY2021": "2.50%"}),
    ("DATA", "UK 11a    Overall capital requirements (%)",
     {"FY2025": "16.23%", "FY2024": "16.19%", "FY2023": "14.78%", "FY2022": "14.80%", "FY2021": "13.80%"}),
    ("DATA", "12    CET1 available after meeting the total SREP own funds requirements (%)",
     {"FY2025": "5.38%", "FY2024": "6.24%", "FY2023": "6.90%", "FY2022": "6.08%", "FY2021": "5.59%"}),
    ("SECTION", "Leverage ratio (£'000 / %)", {}),
    ("DATA", "13    Total exposure measure excluding claims on central banks",
     {"FY2025": 1164862, "FY2024": 1074467, "FY2023": 1028395, "FY2022": 1012682, "FY2021": 892228}),
    ("DATA", "14    Leverage ratio excluding claims on central banks (%)",
     {"FY2025": "10.67%", "FY2024": "10.53%", "FY2023": "9.61%", "FY2022": "8.50%", "FY2021": "8.75%"}),
    ("SECTION", "Liquidity Coverage Ratio (£'000 / %)", {}),
    ("DATA", "15    Total high-quality liquid assets (HQLA) (Weighted value -average)",
     {"FY2025": 208659, "FY2024": 169312, "FY2023": 158061, "FY2022": 143649, "FY2021": 81115}),
    ("DATA", "UK 16a    Cash outflows - Total weighted value",
     {"FY2025": 94465, "FY2024": 83702, "FY2023": 54805, "FY2022": 46483, "FY2021": 58398}),
    ("DATA", "UK 16b    Cash inflows - Total weighted value",
     {"FY2025": 34237, "FY2024": 31128, "FY2023": 43597, "FY2022": 58766, "FY2021": 55899}),
    ("DATA", "16    Total net cash outflows (adjusted value)",
     {"FY2025": 60378, "FY2024": 52574, "FY2023": 13701, "FY2022": 11621, "FY2021": 14600}),
    ("DATA", "17    Liquidity coverage ratio (%)",
     {"FY2025": "345.59%", "FY2024": "322.05%", "FY2023": "1153.62%", "FY2022": "1236.14%", "FY2021": "555.60%"}),
    ("SECTION", "Net Stable Funding Ratio (£'000 / %)", {}),
    ("DATA", "18    Total available stable funding",
     {"FY2025": 881099, "FY2024": 794507, "FY2023": 770756, "FY2022": 728399, "FY2021": 615108}),
    ("DATA", "19    Total required stable funding",
     {"FY2025": 688511, "FY2024": 619756, "FY2023": 590277, "FY2022": 563857, "FY2021": 513950}),
    ("DATA", "20    NSFR ratio (%)",
     {"FY2025": "127.95%", "FY2024": "128.20%", "FY2023": "130.56%", "FY2022": "129.18%", "FY2021": "119.68%"}),
]

KM1_SOURCES = (
    "Sources - QIB (UK) plc's own 'Template UK KM1 - Key metrics template'. FY2022-FY2025 are taken from "
    "EACH YEAR'S OWN edition (column a of that edition). FY2021 IS THE ONE EXCEPTION AND IS FLAGGED AS SUCH "
    "BELOW: it is the FY2022 edition's comparative column, used because QIB (UK)'s own 31 December 2021 "
    "edition prints no KM1 template at all. Amounts in £'000 as the Bank prints them; ratios exactly as "
    "printed, to the Bank's own 2 decimal places.\n"
    "FY2025: Pillar 3 Disclosures 31 December 2025, section 3.1, printed p.6 - " + P3["FY2025"] + "\n"
    "FY2024: Pillar 3 Disclosures 31 December 2024, section 3.1, printed pp.6-7 (rows 18-20 run over to p.7) - "
    + P3["FY2024"] + "\n"
    "FY2023: Pillar 3 Disclosures 31 December 2023, section 3.1, printed pp.6-7 (rows UK 16a-20 run over to "
    "p.7) - " + P3["FY2023"] + "\n"
    "FY2022: Pillar 3 Disclosures 31 December 2022, section 3.1, printed pp.6-7 (rows 18-20 on p.7) - "
    + P3["FY2022"] + "\n"
    "FY2021 (NOT AN OWN-EDITION COLUMN): the SAME Pillar 3 Disclosures 31 December 2022 document, section "
    "3.1, printed pp.6-7, COMPARATIVE COLUMN b headed 31/12/2021 - " + P3["FY2022"] + "\n\n"
    "LATEST-EDITION CHECK, 16 September 2026. qib-uk.com's own financial-reports library "
    "(https://www.qib-uk.com/en/qibs-financial-reports) was listed directly rather than relying on the URLs "
    "already cited here. The NEWEST Pillar 3 on it is the 31 December 2025 edition already cited above, and "
    "the newest Annual Report on it is 31 December 2024 (this workbook already carries FY2025 from the "
    "Companies House filing). Nothing newer exists to transcribe, so YEARS is unchanged. Every document read "
    "for this sheet was verified by HTTP status, Content-Type AND %PDF magic bytes.\n"
    "That listing also surfaced a Pillar 3 edition this script had not cited - 'pillar-3-disclosure-document-"
    "2021-board-approved.pdf', the Bank's own 31 December 2021 edition - which is now examined here (see "
    "below) rather than FY2021 being read only from the FY2022 edition's comparative.\n\n"
    "UNIT: £'000, NOT the £m used elsewhere in this workbook. The FY2023, FY2024 and FY2025 editions each "
    "state on their own p.4 that 'All figures in tables are in thousands of pounds, unless stated otherwise'. "
    "The template is reproduced in the Bank's own unit; it is not restated into £m, which would be "
    "normalising. The £m on the 11 metric sheets is this project's conversion of these same figures.\n\n"
    "WHICH EDITIONS CARRY THE TEMPLATE, and what the others carry instead:\n"
    "• FY2022-FY2025: the UK KM1 template, identical row set in all four editions.\n"
    "• FY2022's edition is a SCANNED document (Konica Minolta bizhub) with NO text layer anywhere, which is "
    "why a text-only survey of this corpus recorded it as having no KM1. It does have one. The table was "
    "located by reading the document's OWN contents page (3.1 Template UK KM1 at printed p.6; 3.2 UK OV1 at "
    "p.8, so the table spans pp.6-7), then transcribed TWICE from two independent renderings - the full page "
    "at 300dpi and the page's embedded 2056x2960 CCITT stencil at native resolution - and required to agree "
    "digit-for-digit before use. It also agrees with the FY2023 edition's comparative column on every row.\n"
    "• THIRD CORROBORATION FOR THAT BITMAP-READ COLUMN, from a second table in the SAME document: the "
    "FY2022 edition's own Template UK CC1 (section 5.1, printed pp.16-17) builds CET1 up from components "
    "and prints row 29 'Common Equity Tier 1 (CET1) capital' as 86,739 - exactly the KM1 row 1 figure read "
    "off the page image. Its row 6 (CET1 before regulatory adjustments) is 88,411 and row 28 (total "
    "regulatory adjustments) is -1,672. Two source defects fall out of adding that column up, recorded and "
    "NOT corrected: the CC1 components 60,864 + 27,622 - 76 sum to 88,410 against the printed 88,411, and "
    "the adjustments -72 - 2,212 + 613 sum to -1,671 against the printed -1,672. Both are £1k roundings "
    "inside QIB (UK)'s own printing; the two errors cancel, so row 29 still lands on 86,739.\n"
    "• FY2021 and FY2020: Pillar 3 IS published (31 December 2021 and 31 December 2020 editions), and each "
    "opens with 'As at 31 December 20XX, the Bank's key metrics were:' - but what follows is a BESPOKE "
    "12-line summary of the Bank's own design, not the template. Its headings are the Bank's own ('Available "
    "Capital (£'000s)', 'Capital Ratios as a percentage of RWA', 'Leverage Ratio', 'Liquidity Coverage "
    "Ratio'); it carries no template row numbers, no SREP rows, no buffer rows, no cash-inflow/outflow rows "
    "and no NSFR, and it ends with a 'Profit/(Loss) after taxation' line that is not a KM1 row at all. That "
    "is a different and shorter table, so it is NOT mapped onto template row numbers here. THIS IS A "
    "'THE TEMPLATE IS NOT USED' FINDING, which is a different and weaker thing than 'no Pillar 3 is "
    "published' - QIB (UK) publishes one every year.\n"
    "• The absence of a FY2021 template was re-established from the document on 17 September 2026, three "
    "independent ways, before FY2021 was filled from the comparative. (i) The FY2021 edition's OWN CONTENTS "
    "PAGE runs sections 1-9 and contains no 'Annex I: Disclosure of key metric' section - the section the "
    "FY2022 edition numbers 3 - so there is no template to have been missed. (ii) Text extraction from the "
    "35-page FY2021 PDF is RICH (117 hits for 'capital', 104 for 'ratio', 64 for 'liquidity', 7 for "
    "'leverage'), which is what makes its ZERO hits meaningful rather than an extraction failure; against "
    "that richness it returns zero hits for 'KM1', 'Template UK', 'combined buffer requirement', 'overall "
    "capital requirement', 'available after meeting' and 'total exposure measure'. (iii) The page-3 bitmap "
    "was re-rendered and re-read. This matters because it is the difference between two rules: a year whose "
    "own edition prints the template and dashes a row keeps that row BLANK, whereas a year whose own edition "
    "prints NO template is filled from a later comparative. This is the second case.\n"
    "• A TRAP WORTH RECORDING for anyone re-checking: in the FY2021 edition that bespoke table is an "
    "EMBEDDED IMAGE inside an otherwise text-native PDF, so text extraction returns the heading 'the Bank's "
    "key metrics were:' and then nothing at all before '2. Background'. The page was rendered at 300dpi and "
    "read by eye; the figures are CET1 78,028 / Total capital 91,081 / RWA 462,020 / CET1 and Tier 1 ratio "
    "16.89% / total capital ratio 19.71% / leverage exposure 892,228 / leverage ratio 8.75% / liquid buffer "
    "81,115 / net liquidity outflow 14,600 / LCR 555.60%, all £'000.\n\n"
    "WHY FY2021 IS FILLED FROM THE FY2022 EDITION, AND FY2020 AND EARLIER ARE NOT (revised 17 September "
    "2026). FY2021's own edition prints no KM1 template at all - not a template with rows left blank, but no "
    "template - so there is no own-edition disclosure for this year to displace. The FY2022 edition's "
    "comparative column b (31/12/2021) carries the complete FY2021 template, and it is NOT a restatement: it "
    "agrees with the FY2021 edition's own bespoke table on every one of the ten lines the two have in "
    "common. THAT COLUMN IS THEREFORE WHAT THIS SHEET'S FY2021 CARRIES, in the row structure the FY2022 "
    "edition prints it in. A reader can tell it apart from an own-edition column by the citation above, "
    "which names it.\n"
    "This reverses the treatment this sheet carried until 17 September 2026, which left FY2021 blank and "
    "quoted the comparative in this note instead. The evidence behind that decision is unchanged and is "
    "still set out above - what changed is the conclusion drawn from it, so that a BLANK on this sheet now "
    "means one thing only: QIB (UK) has never published that figure, in any edition, on any basis.\n"
    "FY2020 AND EARLIER REMAIN BLANK for exactly that reason. No edition anywhere prints them in template "
    "form. The FY2021 edition does carry a 31/12/20 comparative, but it is the same bespoke 12-line shape as "
    "its own-year column (RWA 418,084; CET1 72,249; total capital 85,440; ratios 17.28% / 17.28% / 20.44%; "
    "leverage exposure 733,305 and 9.85%; liquid buffer 68,358; net outflow 28,318; LCR 242.03%; profit "
    "after tax 4,744) - a different and shorter table, not the template, so it cannot fill a template "
    "column.\n\n"
    "ROWS 14a-14e ARE A STATED EXCLUSION, NOT A GAP. Every edition prints beneath the table: 'Rows 14a-14e "
    "have been removed as only LREQ firms are required to disclose this information.' They are not printed by "
    "the Bank, so they are not shown here; the reason is recorded instead.\n\n"
    "'N/A' IS REPRODUCED AS THE BANK PRINTS IT. QIB (UK) writes the literal string 'N/A' in rows UK 7b, UK "
    "8a, UK 9a, 10 and UK 10a - not a dash and not an empty cell - so 'N/A' is what this sheet carries. Row 9 "
    "for FY2021 is a printed '0.00%', which is a disclosed zero and is carried as the zero, not as a "
    "blank.\n\n"
    "TWO CROSS-EDITION DIVERGENCES, RECORDED AND NOT RECONCILED (each cell above is from the edition in which "
    "that year is the reporting year):\n"
    "• Row 4, FY2024: the FY2024 edition prints 601,928; the FY2025 edition's comparative column prints "
    "601,927. This sheet carries 601,928.\n"
    "• Row 14, FY2022: the FY2022 edition prints 8.50%; the FY2023 edition's comparative column prints 8.57%. "
    "This sheet carries 8.50%, which is also what the Leverage Ratio metric sheet carries.\n\n"
    "COLUMN LETTERS DO NOT TRANSFER. Each QIB edition prints two columns lettered a (its own reporting date) "
    "and b (the prior year). This sheet is one column per YEAR: FY2022-FY2025 are drawn from that year's own "
    "edition's column a, and FY2021 from the FY2022 edition's column b as set out above, so the Bank's a/b "
    "lettering is not reproduced.\n\n"
    + ENTITY
)

bw.add_km1_sheet(
    title="QIB (UK) plc — KM1 Key Metrics",
    subtitle="The Bank's own published 'Template UK KM1 - Key metrics template', reproduced in QIB (UK)'s row "
             "order with its own template row numbers, labels, 'N/A' glyphs and printed precision. AMOUNTS ARE "
             "IN £'000 as the Bank prints them - not the £m used on the other sheets in this workbook. Entity "
             "basis (the Bank prepares no group accounts). FY2022-FY2025 come from each year's own edition; "
             "FY2021 is the FY2022 edition's comparative column, because the Bank's own FY2021 edition "
             "publishes a bespoke key-metrics summary of its own design and no template at all. FY2020 and "
             "earlier are blank because no edition prints them in template form. See the source note.",
    rows=km1_rows,
    sources_text=KM1_SOURCES,
    years=PILLAR3_YEARS,
    first_col_width=76,
    source_height=520,
)

metric("CET1 Capital","£m",[("Common Equity Tier 1 (CET1) capital",cap)],"FY2014/FY2015 are the Bank's own narrative-disclosed round figures (£25.9m/£49.1m), not from a numeric capital table; FY2016 is FY2017's own comparative column.")
metric("CET1 Ratio","% of RWA",[("Common Equity Tier 1 ratio",ratios["CET1 Ratio"])],"FY2014/FY2015: no CET1 ratio is disclosed in the reviewed QIB UK Pillar 3 documents (narrative capital amounts only, no RWA denominator given).")
metric("Tier 1 Capital","£m",[("Tier 1 capital",cap)],"KM1/Note 4 report Tier 1 equal to CET1; no AT1 capital is reported in any reviewed year.")
metric("Tier 1 Ratio","% of RWA",[("Tier 1 ratio",ratios["CET1 Ratio"])],"Tier 1 ratio equals the CET1 ratio in every reviewed year (no AT1 capital).")
metric("Total Capital","£m",[("Total capital",total)],"FY2014/FY2015 total capital is derived as Tier 1 + Tier 2 from the Bank's own narrative figures (not itself a single disclosed line for those two years).")
metric("Total Capital Ratio","% of RWA",[("Total capital ratio",ratios["Total Capital Ratio"])],"FY2014/FY2015: no Total Capital ratio is disclosed (no RWA denominator given).")
metric("Total RWAs","£m",[("Total risk-weighted exposure amount",rwa)],"FY2014/FY2015: no RWA figure is disclosed in the reviewed QIB UK Pillar 3 documents for these two years.")

rwa_breakdown_rows = [
    ("SECTION", "Template UK OV1 'Overview of risk weighted exposure amounts' — p.7 of each year's own Pillar 3 document (FY2025-FY2021; FY2021 read from the FY2022 document's own comparative column)", {}),
    ("DATA", "Credit risk (excluding CCR)", {"FY2025": 634.742, "FY2024": 548.789, "FY2023": 500.902, "FY2022": 465.681, "FY2021": 432.383}),
    ("DATA", "Counterparty credit risk (CCR, including CVA)", {"FY2025": 3.345, "FY2024": 4.023, "FY2023": 1.390, "FY2022": 1.852, "FY2021": 2.166}),
    ("DATA", "Position, foreign exchange and commodities risk (market risk)", {"FY2025": 0.049, "FY2024": 0.053, "FY2023": 0.122, "FY2022": 0.044, "FY2021": 0.031}),
    ("DATA", "Operational risk", {"FY2025": 55.017, "FY2024": 49.062, "FY2023": 40.771, "FY2022": 31.545, "FY2021": 27.440}),
    ("TOTAL", "Total risk-weighted exposure amount", {"FY2025": 693.154, "FY2024": 601.927, "FY2023": 543.185, "FY2022": 499.122, "FY2021": 462.020}),
    ("SECTION", "Pillar 1 minimum-capital-requirement table by exposure class — the Bank's own standalone Pillar 3 document, p.30 (FY2020). This table BUNDLES credit and counterparty credit risk into a single line and discloses CVA separately, so its rows are not the UK OV1 rows above", {}),
    ("DATA", "Credit and counterparty credit risk, combined", {"FY2020": 392.457}),
    ("DATA", "Market risk", {"FY2020": 0.026}),
    ("DATA", "Credit valuation adjustment (CVA)", {"FY2020": 0.736}),
    ("DATA", "Operational risk", {"FY2020": 24.864}),
    ("TOTAL", "Total risk-weighted exposure amount", {"FY2020": 418.084}),
    ("SECTION", "Annual Report Note 4.2 'Regulatory capital required' — each year's own Annual Report, FY2016 taken from the FY2017 report's own comparative column (FY2018-FY2016). THREE categories only: this table has no separate counterparty-credit-risk or CVA line at all", {}),
    ("DATA", "Credit and counterparty credit risk, combined", {"FY2018": 336, "FY2017": 316, "FY2016": 249}),
    ("DATA", "Market risk", {"FY2018": 0, "FY2017": 1, "FY2016": 1}),
    ("DATA", "Operational risk", {"FY2018": 18, "FY2017": 18, "FY2016": 14}),
    ("TOTAL", "Total risk-weighted exposure amount", {"FY2018": 354, "FY2017": 335, "FY2016": 264}),
    ("SECTION", "No risk-type breakdown disclosed (FY2019) — total risk-weighted exposure amount only; see the Total RWAs sheet", {}),
    ("TOTAL", "Total risk-weighted exposure amount", {"FY2019": 375.285}),
]
bw.add_rwa_breakdown_sheet(
    title="QIB (UK) plc — RWA Breakdown",
    subtitle="Pillar 3 UK OV1 template (top-level risk-type categories), £m, FY2021-FY2025; FY2016-FY2020 "
              "use the Bank's own earlier, differently-categorised Pillar 1 tables (see rows below) - "
              "FY2014/FY2015/FY2019 have no risk-type breakdown disclosed, only (for FY2019) a Total RWA "
              "figure on the Total RWAs sheet.",
    rows=rwa_breakdown_rows,
    sources_text=p3_sources() + (
        "\n\nRWA BREAKDOWN: FY2021-FY2025 sourced from Template UK OV1 - Overview of risk weighted exposure "
        "amounts (p.7 of each year's own Pillar 3 document). Each year's own OV1 table gives that year's own "
        "column plus the prior year's comparative column; FY2021's figures are read from the FY2022 Pillar 3 "
        "document's own comparative column (its own standalone OV1 table not being available this session). "
        "This sheet's totals (693.154 / 601.927 / 543.185 / 499.122 / 462.020) are within £1k of the "
        "pre-existing Total RWAs sheet's figures (693.154 / 601.928 / 543.184 / 499.121 / 462.020) - an "
        "immaterial rounding difference between the two Pillar 3 tables, not an error.\n\n"
        "FY2016-FY2018 sourced from each year's own Annual Report Note 4.2 'Regulatory capital required' "
        "table (FY2016 from FY2017's own comparative column), which uses three categories only (Credit "
        "risk / Market risk / Operational risk, no separate CCR or CVA line). FY2020 sourced from the "
        "Bank's own standalone Pillar 3 document's Pillar 1 minimum-capital-requirement table by exposure "
        "class (p.30), which bundles credit risk and counterparty credit risk into one 'Credit and "
        "Counterparty Credit Risk (Standardised)' line and discloses CVA separately; FY2020's four rows "
        "here sum to 418.083, within £1k of the Total RWAs sheet's 418.084."
    ),
    first_col_width=64,
    source_height=360,
    unit_suffix=" (£m)",
    years=PILLAR3_YEARS,
)

metric("Leverage Ratio","%",[("Leverage ratio excluding claims on central banks",ratios["Leverage Ratio"])],"Not numerically disclosed in the reviewed QIB UK documents before FY2019 (FY2019 figure is FY2020's own comparative column).")
metric("LCR","%",[("Liquidity coverage ratio",ratios["LCR"])],"Not numerically disclosed in the reviewed QIB UK documents before FY2019 (FY2019 figure is FY2020's own comparative column); narrative mentions of the LCR regime starting 1 October 2015 appear from the FY2015 Pillar 3 Declaration onward, but with no percentage given. BASIS CHECKED 2026-09-15: this series swings widely (FY2022 1236.14% -> FY2023 1153.62% -> FY2024 322.05%, an 831pp fall in one year), which elsewhere in this project has indicated a silent mix of KM1 12-month-average and point-in-time year-end figures. It is NOT that here: every year from FY2019 onward is taken from a QIB (UK) Pillar 3 disclosure (see sources note), so the row is single-basis and the movement is as the Bank reported it. Recorded so the discontinuity is not re-investigated as a basis error.")
metric("NSFR","%",[("Net stable funding ratio",ratios["NSFR"])],"No NSFR is disclosed in the reviewed QIB UK Pillar 3 documents through FY2020; the FY2020 document states the Bank was still 'monitoring' NSFR ahead of implementation.")
metric("MREL Ratio","%",[("MREL ratio",{y:"Not publicly disclosed" for y in PILLAR3_YEARS})],"No MREL ratio or requirement is disclosed in the reviewed QIB UK Pillar 3 documents.")

bs_totals = {r[1]: r[2] for r in bs_rows}
pl_totals = {r[1]: r[2] for r in pl_rows}
cf_totals = {r[1]: r[2] for r in rows}
bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", bs_totals["Total assets"]),
        ("Financing arrangements", bs_totals["Financing arrangements"]),
        ("Due to customers", bs_totals["Due to customers"]),
        ("Total equity", bs_totals["Total equity"]),
    ],
    balance_sheet_unit="£m",
    income_statement_totals=[
        ("Total operating income", pl_totals["Total operating income"]),
        ("Total operating expenses", pl_totals["Total operating expenses"]),
        ("Profit/(loss) for the year", pl_totals["Profit/(loss) for the year"]),
    ],
    income_statement_unit="£m",
    equity_changes_totals=[
        ("Opening equity", {"FY2025": 113.102, "FY2024": 100.441, "FY2023": 88.411, "FY2022": 78.827, "FY2021": 71.933, "FY2020": 67.217, "FY2019": 62.815, "FY2018": 60.101, "FY2017": 51.890, "FY2016": 55.635, "FY2015": 30.505, "FY2014": 16.413}),
        ("Profit for the year", {"FY2025": 11.732, "FY2024": 12.603, "FY2023": 11.950, "FY2022": 9.692, "FY2021": 6.856, "FY2020": 4.744, "FY2019": 4.427, "FY2018": 3.713, "FY2017": 1.760, "FY2016": -3.090, "FY2015": 2.548, "FY2014": 1.317}),
        ("Other equity movements, net", {"FY2025": -0.188, "FY2024": 0.058, "FY2023": 0.081, "FY2022": -0.108, "FY2021": 0.038, "FY2020": -0.028, "FY2019": -0.024, "FY2018": -0.999, "FY2017": 6.451, "FY2016": -0.655, "FY2015": 22.582, "FY2014": 12.775}),
        ("Closing equity", {"FY2025": 124.646, "FY2024": 113.102, "FY2023": 100.441, "FY2022": 88.411, "FY2021": 78.827, "FY2020": 71.933, "FY2019": 67.217, "FY2018": 62.815, "FY2017": 60.101, "FY2016": 51.890, "FY2015": 55.635, "FY2014": 30.505}),
    ],
    equity_changes_unit="£m",
    cash_flow_totals=[
        ("Net cash inflow/(outflow) from operating activities", cf_totals["Net cash inflow/(outflow) from operating activities"]),
        ("Net cash outflow from investing activities", cf_totals["Net cash outflow from investing activities"]),
        ("Net cash (outflow)/inflow from financing activities", cf_totals["Net cash (outflow)/inflow from financing activities"]),
        ("Cash and cash equivalents at end of year", cf_totals["Cash and cash equivalents at end of year"]),
    ],
    cash_flow_unit="£m",
    ratios=list(ratios.items()),
    note="Figures are duplicated from detail sheets; see each detail sheet's source citation.",
)
bw.save("/Users/armaan/code/katalysis/banks/QIB UK FINANCIALS.xlsx")
