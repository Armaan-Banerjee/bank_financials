import os
import sys
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021", "FY2020", "FY2019", "FY2018", "FY2017", "FY2016", "FY2015", "FY2014"]
YEAR_LABEL = {y: y for y in YEARS}
CH = "https://find-and-update.company-information.service.gov.uk/company/04656003/filing-history"
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
# P3 declarations for FY2014-FY2018 are an appendix bundled inside that year's own Annual Report
# (same PDF as AR[y], "Appendix: QIB (UK) Pillar 3 Declaration"). QIB (UK) stopped including the
# Pillar 3 appendix in the AR from FY2019 onward and began publishing a standalone Pillar 3
# document from FY2020. FY2019 has no standalone Pillar 3 document of its own on the Bank's site
# or in Wayback Machine snapshots of qib-uk.com (checked 2014-2022) - its KM1-style figures are
# sourced from FY2020's own standalone document's FY2019 comparative column, the same convention
# already used for FY2021 in this file (comparative column of the following year's own document).
P3 = {"FY2025": "https://www.qib-uk.com/-/media/project/uk/files/finance-reports/pillar-3-disclosure-document--2025-approved.pdf", "FY2024": "https://www.qib-uk.com/-/media/project/uk/files/finance-reports/pillar-3-disclosure-document-31-december-2024.pdf", "FY2023": "https://www.qib-uk.com/-/media/project/uk/files/finance-reports/pillar-3-disclosure-document-31-december-2023.pdf", "FY2022": "https://www.qib-uk.com/-/media/project/uk/files/finance-reports/pillar-3-disclosure-document-2023.pdf", "FY2021": "https://www.qib-uk.com/-/media/project/uk/files/finance-reports/pillar-3-disclosure-document-2023.pdf",
      "FY2020": "https://www.qib-uk.com/-/media/project/uk/files/finance-reports/pillar-3-disclosure-document-2020-board-approved-final.pdf",
      "FY2019": "https://www.qib-uk.com/-/media/project/uk/files/finance-reports/pillar-3-disclosure-document-2020-board-approved-final.pdf",
      "FY2018": AR["FY2018"], "FY2017": AR["FY2017"], "FY2016": AR["FY2017"], "FY2015": AR["FY2015"], "FY2014": AR["FY2014"]}

ENTITY = ("ENTITY NOTE: QIB (UK) plc (Companies House 04656003, FRN 466577) is the UK bank subsidiary of Qatar Islamic Bank S.A.Q. The Bank states that it had no active subsidiaries or joint ventures at 31 December 2023 and does not prepare group accounts; these are entity-only GBP accounts. Companies House shows the entity Active with accounts filed through FY2025.")
CASH_SOURCES = ("Sources - QIB (UK) plc's own entity Statement of Cash Flows, converted from £ to £m (divide by 1,000,000 and round to 2 decimals):\n" + "\n".join(f"{y}: Annual Report, p.{p} - {AR[y]}" for y,p in {"FY2025":24,"FY2024":25,"FY2023":24,"FY2022":25,"FY2021":22,"FY2020":21,"FY2019":14,"FY2018":16,"FY2017":17,"FY2016":13,"FY2015":14,"FY2014":14}.items()) + "\nFY2025/FY2024 reports label the FY2024 comparative restated and FY2023 labels the FY2022 comparative restated. Each year's own report column is used here, preserving the project convention and avoiding blended reclassifications. FY2024 and FY2023 each contain a source presentation difference between the printed operating line items and the printed operating subtotal; explicit reconciliation rows preserve both.\nFY2014-FY2020 own-year cash flow statements were sourced from QIB (UK)'s qib-uk.com Annual Report PDFs (native text). FY2018/FY2019/FY2020's own 'cash and cash equivalents at end of year' figure (37,017,161 / 40,777,075 / 41,708,427) is a few hundred pounds above that same year's own Balance Sheet 'Cash and balances with banks' line (37,016,753 / 40,776,701 / 41,708,029) - an immaterial gross-vs-net-of-ECL presentation difference within the Bank's own report, not a transcription error.\n\n" +
    "DATA QUALITY FLAG - FY2015: the Bank's own AR2015 prints 'Net cash inflow / (outflow) from operating activities' as a positive 23,588,646, but that figure does not reconcile two different ways: (1) it is not the sum of that same table's own 14 printed adjustment lines, which sum to exactly -23,588,647 (verified independently); and (2) using +23,588,646 for operating activities together with the Bank's own printed investing (-2,658,626) and financing (+26,500,000) subtotals gives 47,430,020, not the Bank's own printed 'Net increase in cash and cash equivalents' of 252,728 - whereas using -23,588,647 gives -23,588,647-2,658,626+26,500,000=252,727, matching (within £1 rounding) both the printed net-change figure and the independently-verifiable cash-at-start/cash-at-end tie-out (5,844,014 -> 6,096,742). This sheet therefore carries -23,588,647 (a net outflow) for FY2015 operating activities - the value consistent with the rest of the Bank's own statement and with actual cash movement - rather than the Bank's own headline positive figure, which appears to be missing a negative sign/bracket in the published PDF. All 14 individual adjustment-line figures are transcribed exactly as printed either way.\n\n" + ENTITY)
def p3_sources():
    return ("Sources - QIB (UK) plc's own Pillar 3 disclosures (amounts in £m unless noted; ratios as reported):\n" + "\n".join(f"{y}: {P3_LABEL.get(y, 'own-year disclosure')}, {P3_PAGES.get(y,'pp.6-7')} - {P3[y]}" for y in YEARS) + "\nFY2014/FY2015: the Bank's own Pillar 3 Declaration for these years is narrative-only - it discloses total Tier 1 and Tier 2 capital in round £m terms but no Total RWA figure and no CET1/Total Capital ratio percentage; those cells are left blank rather than estimated. FY2016's own Pillar 3 Declaration is likewise narrative-only; its numeric capital/RWA/ratio figures here are read from FY2017's own Annual Report Note 4 comparative ('2016') column instead.\nLeverage Ratio, LCR and NSFR are not numerically disclosed anywhere in the reviewed QIB UK documents before FY2019 (LCR)/FY2019 (Leverage) - both first appear as a % figure in FY2020's own standalone Pillar 3 document's FY2019 comparative column. NSFR is not disclosed in any reviewed QIB UK document through FY2020 (the FY2020 document states the Bank was still 'monitoring' NSFR ahead of implementation).\nMREL is not disclosed in the reviewed QIB UK Pillar 3 documents.\n\n" + ENTITY)
P3_LABEL = {
    "FY2021": "FY2022 comparative column of FY2022 disclosure",
    "FY2019": "FY2019 comparative column of FY2020 disclosure",
    "FY2016": "FY2016 comparative column of FY2017 Annual Report Note 4",
    "FY2017": "own-year disclosure, Annual Report Note 4",
    "FY2018": "own-year disclosure, Annual Report Note 4",
    "FY2015": "own-year disclosure (narrative only, no RWA/ratio)",
    "FY2014": "own-year disclosure (narrative only, no RWA/ratio)",
}
P3_PAGES = {"FY2017": "pp.47-48", "FY2018": "pp.49-50", "FY2016": "pp.47-48 (FY2017 AR)", "FY2015": "pp.46", "FY2014": "p.55", "FY2020": "p.6 / Note 6.2", "FY2019": "p.6 (FY2020 doc)"}
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
    "comparative column, a native-text PDF): Annual Report 2014, pp.11-14 - " + AR["FY2014"] + "\n\n"
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
    ("DATA", "Cash and balances with banks", m({"FY2025": 132462261, "FY2024": 27223411, "FY2023": 49246616, "FY2022": 59103924, "FY2021": 56338957, "FY2020": 41708029, "FY2019": 40776701, "FY2018": 37016753, "FY2017": 30751631, "FY2016": 16662446, "FY2015": 6096742, "FY2014": 5844014})),
    ("DATA", "Due from banks", m({"FY2016": 90861366, "FY2015": 69597214, "FY2014": 23576325})),
    ("DATA", "Financing arrangements", m({"FY2025": 954683460, "FY2024": 884059958, "FY2023": 826875369, "FY2022": 777848982, "FY2021": 726026105, "FY2020": 593879089, "FY2019": 530994682, "FY2018": 482374737, "FY2017": 403270277, "FY2016": 293012707, "FY2015": 227801665, "FY2014": 88981407})),
    ("DATA", "Less: impairment on financing arrangements", m({"FY2017": -4997014, "FY2016": -2750372, "FY2015": -625495, "FY2014": -679495})),
    ("DATA", "Financial assets held to maturity", m({"FY2017": 0, "FY2016": 2422970, "FY2015": 4067521, "FY2014": 6808055})),
    ("DATA", "Financial assets available for sale", m({"FY2017": 69064158, "FY2016": 77665869, "FY2015": 87735905, "FY2014": 70549731})),
    ("DATA", "Financial assets at amortised cost", m({"FY2025": 141472045, "FY2024": 192903927, "FY2023": 172313444, "FY2022": 149784049, "FY2021": 81553810, "FY2020": 67271228, "FY2019": 74814453, "FY2018": 66832272})),
    ("DATA", "Derivative financial instruments", m({"FY2025": 1122065, "FY2024": 1597563, "FY2023": 617042, "FY2022": 989055, "FY2021": 1429382, "FY2020": 94702, "FY2019": 93764, "FY2018": 5371224, "FY2017": 0, "FY2016": 8127029, "FY2015": 923845, "FY2014": 650176})),
    ("DATA", "Fair value adjustment for portfolio hedged risk", m({"FY2025": -1031227, "FY2024": -898730})),
    ("DATA", "Property and equipment", m({"FY2025": 15289209, "FY2024": 12810372, "FY2023": 12674423, "FY2022": 14126933, "FY2021": 12995170, "FY2020": 13545102, "FY2019": 14434772, "FY2018": 14836478, "FY2017": 15353959, "FY2016": 15826909, "FY2015": 16248792, "FY2014": 14724851})),
    ("DATA", "Intangible assets", m({"FY2025": 384806, "FY2023": 23300, "FY2022": 72221, "FY2021": 231069, "FY2020": 250722, "FY2019": 0, "FY2018": 11389, "FY2017": 80970, "FY2016": 200542, "FY2015": 295064, "FY2014": 61555})),
    ("DATA", "Investment property", m({"FY2025": 3100000, "FY2024": 6225000, "FY2023": 6225000, "FY2022": 7665000, "FY2021": 10240000, "FY2020": 10240000, "FY2019": 10240000, "FY2018": 10240000, "FY2017": 10240000, "FY2016": 9176071, "FY2015": 9511839, "FY2014": 9511839})),
    ("DATA", "Other assets", m({"FY2025": 2766848, "FY2024": 1527850, "FY2023": 1003932, "FY2022": 7105411, "FY2021": 4124393, "FY2020": 3926789, "FY2019": 3780006, "FY2018": 3651433, "FY2017": 3729134, "FY2016": 3033107, "FY2015": 3224444, "FY2014": 3153260})),
    ("DATA", "Deferred tax asset", m({"FY2023": 1500052, "FY2022": 2212189, "FY2021": 1792307, "FY2020": 1148521, "FY2019": 1031743, "FY2018": 1478710, "FY2017": 2274425, "FY2016": 2696072, "FY2015": 3316970, "FY2014": 3194647})),
    ("TOTAL", "Total assets", m({"FY2025": 1250249467, "FY2024": 1125449351, "FY2023": 1070479178, "FY2022": 1018907764, "FY2021": 894731193, "FY2020": 732064182, "FY2019": 676166121, "FY2018": 621812996, "FY2017": 529767540, "FY2016": 516934716, "FY2015": 428194506, "FY2014": 226376365})),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Due to banks", m({"FY2025": 108416644, "FY2024": 83641722, "FY2023": 103985098, "FY2022": 105266168, "FY2021": 120257356, "FY2020": 125332937, "FY2019": 85169482, "FY2018": 91504145, "FY2017": 72566143, "FY2016": 49438510, "FY2015": 134128955, "FY2014": 27358165})),
    ("DATA", "Due to customers", m({"FY2025": 969400662, "FY2024": 886390965, "FY2023": 827374599, "FY2022": 780208856, "FY2021": 657768467, "FY2020": 495173550, "FY2019": 480142212, "FY2018": 434542830, "FY2017": 366604600, "FY2016": 388377883, "FY2015": 216017303, "FY2014": 153139947})),
    ("DATA", "Other liabilities", m({"FY2025": 31877296, "FY2024": 27424980, "FY2023": 23695160, "FY2022": 29976993, "FY2021": 22889306, "FY2020": 18567055, "FY2019": 24281037, "FY2018": 17001377, "FY2017": 12851817, "FY2016": 11028773, "FY2015": 6213727, "FY2014": 2615160})),
    ("DATA", "Derivative financial instruments", m({"FY2025": 1646782, "FY2024": 593378, "FY2023": 816802, "FY2022": 1345231, "FY2021": 1289353, "FY2020": 5107456, "FY2019": 3406473, "FY2018": 0, "FY2017": 1694241})),
    ("DATA", "Deferred tax liability", m({"FY2025": 163967, "FY2024": 163136})),
    ("DATA", "Subordinated Wakala", m({"FY2025": 14097755, "FY2024": 14133099, "FY2023": 14166072, "FY2022": 13700000, "FY2021": 13700000, "FY2020": 15950000, "FY2019": 15950000, "FY2018": 15950000, "FY2017": 15950000, "FY2016": 16200000, "FY2015": 16200000, "FY2014": 12757834})),
    ("TOTAL", "Total liabilities", m({"FY2025": 1125603106, "FY2024": 1012347280, "FY2023": 970037731, "FY2022": 930497248, "FY2021": 815904482, "FY2020": 660130998, "FY2019": 608949204, "FY2018": 558998352, "FY2017": 469666801, "FY2016": 465045166, "FY2015": 372559985, "FY2014": 195871106})),
    ("SECTION", "Equity", {}),
    ("DATA", "Share capital", m({"FY2025": 60864221, "FY2024": 60864221, "FY2023": 60864221, "FY2022": 60864221, "FY2021": 60864221, "FY2020": 60864221, "FY2019": 60864221, "FY2018": 60864221, "FY2017": 85807834, "FY2016": 79557834, "FY2015": 79557834, "FY2014": 56500000})),
    ("DATA", "Fair value reserve on AFS financial assets", m({"FY2017": -457745, "FY2016": -598538, "FY2015": -309485, "FY2014": 166916})),
    ("DATA", "Cash flow hedge reserve", m({"FY2025": -470073, "FY2024": -206240, "FY2023": -283405, "FY2022": -309566, "FY2021": -202208, "FY2020": -283898, "FY2019": -256373, "FY2018": -253137, "FY2017": -305737, "FY2016": -366086})),
    ("DATA", "Retained earnings", m({"FY2025": 64252213, "FY2024": 52444090, "FY2023": 39860631, "FY2022": 27855861, "FY2021": 18164698, "FY2020": 11352861, "FY2019": 6609069, "FY2018": 2203560, "FY2017": -24943613, "FY2016": -26703660, "FY2015": -23613828, "FY2014": -26161657})),
    ("TOTAL", "Total equity", m({"FY2025": 124646361, "FY2024": 113102071, "FY2023": 100441447, "FY2022": 88410516, "FY2021": 78826711, "FY2020": 71933184, "FY2019": 67216917, "FY2018": 62814644, "FY2017": 60100739, "FY2016": 51889550, "FY2015": 55634521, "FY2014": 30505259})),
    ("TOTAL", "Total liabilities and equity", m({"FY2025": 1250249467, "FY2024": 1125449351, "FY2023": 1070479178, "FY2022": 1018907764, "FY2021": 894731193, "FY2020": 732064182, "FY2019": 676166121, "FY2018": 621812996, "FY2017": 529767540, "FY2016": 516934716, "FY2015": 428194506, "FY2014": 226376365})),
]
bw.add_balance_sheet_sheet(
    title="QIB (UK) plc — Balance Sheet",
    subtitle="Entity basis, £m, converted from the Bank's reported £ amounts; FY2014-FY2025. Each year's "
              "own originally-published figures are used - see RESTATEMENT NOTE / PRE-2018 PRESENTATION "
              "note at bottom.",
    rows=bs_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=66,
    source_height=520,
    unit_suffix=" (£m)",
)

pl_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Income from financing and investing activities", m({"FY2017": 17391144, "FY2016": 13599099, "FY2015": 11089315, "FY2014": 5786005})),
    ("DATA", "Income from financing activities", m({"FY2025": 65547275, "FY2024": 69270359, "FY2023": 60989079, "FY2022": 31605685, "FY2021": 21439036, "FY2020": 19808578, "FY2019": 20567967, "FY2018": 17726668})),
    ("DATA", "Income from investing activities", m({"FY2025": 7726355, "FY2024": 6228539, "FY2023": 4899705, "FY2022": 2535344, "FY2021": 1622287, "FY2020": 1807057, "FY2019": 1756532, "FY2018": 1143463})),
    ("DATA", "Returns to banks and customers", m({"FY2025": -45712749, "FY2024": -47998896, "FY2023": -37367914, "FY2022": -14860836, "FY2021": -7938424, "FY2020": -9690817, "FY2019": -10922693, "FY2018": -8503736, "FY2017": -7241968, "FY2016": -5712849, "FY2015": -3045370, "FY2014": -2496257})),
    ("TOTAL", "Net income from financing and investing activities", m({"FY2025": 27560881, "FY2024": 27500002, "FY2023": 28520870, "FY2022": 19280193, "FY2021": 15122899, "FY2020": 11924818, "FY2019": 11401806, "FY2018": 10366395, "FY2017": 10149176, "FY2016": 7886250, "FY2015": 8043945, "FY2014": 3289748})),
    ("DATA", "Fees and commissions income", m({"FY2025": 2489591, "FY2024": 2208209, "FY2023": 1823107, "FY2022": 1842222, "FY2021": 1611384, "FY2020": 1728470, "FY2019": 1816439, "FY2018": 1798526, "FY2017": 1378813, "FY2016": 1214184, "FY2015": 1113357, "FY2014": 1845823})),
    ("DATA", "Fees and commissions expense", m({"FY2025": -719061, "FY2024": -633508, "FY2023": -667574, "FY2022": -556172, "FY2021": -491526, "FY2020": -289355, "FY2019": -132005, "FY2018": -57746, "FY2017": -189859, "FY2016": -1190589, "FY2015": -880560, "FY2014": -450948})),
    ("TOTAL", "Net fees and commissions income", m({"FY2025": 1770530, "FY2024": 1574701, "FY2023": 1155533, "FY2022": 1286050, "FY2021": 1119858, "FY2020": 1439115, "FY2019": 1684434, "FY2018": 1740780, "FY2017": 1188954, "FY2016": 23595, "FY2015": 232797, "FY2014": 1394875})),
    ("DATA", "Net gain/(loss) on financial assets at fair value", m({"FY2025": -323866, "FY2024": 28013})),
    ("DATA", "Net gain/(loss) on financial assets at amortised cost", m({"FY2025": 103987, "FY2024": 25681, "FY2021": 25475, "FY2020": 149745, "FY2019": 27132, "FY2018": -2190})),
    ("DATA", "Net gain/(loss) on financial assets at FVPL", m({"FY2021": 95289})),
    ("DATA", "Net gain/(loss) on financial assets classified as AFS", m({"FY2017": -145408, "FY2016": 712361, "FY2015": 664505, "FY2014": 232643})),
    ("DATA", "Gain/(loss) on foreign exchange", m({"FY2025": 330256, "FY2024": 198849, "FY2023": 251062, "FY2022": 248560, "FY2021": 83629, "FY2020": 206809, "FY2019": 96171, "FY2018": 29050, "FY2017": 33803, "FY2016": -9405, "FY2015": -144845, "FY2014": -845914})),
    ("DATA", "Fair value gain on forward foreign exchange", m({"FY2015": 142127, "FY2014": 838599})),
    ("DATA", "Rental income", m({"FY2018": 283557, "FY2017": 109922, "FY2016": 17950})),
    ("DATA", "Other income", m({"FY2025": 120181, "FY2024": 477869, "FY2023": 172981, "FY2022": 124170, "FY2021": 91934, "FY2020": 177986, "FY2019": 257577, "FY2015": 389300, "FY2014": 339647})),
    ("DATA", "FV loss on investment property", m({"FY2023": -1440000, "FY2022": -905000})),
    ("TOTAL", "Total operating income", m({"FY2025": 29561969, "FY2024": 29805115, "FY2023": 28660446, "FY2022": 20033973, "FY2021": 16539084, "FY2020": 13898473, "FY2019": 13467120, "FY2018": 12417592, "FY2017": 11336448, "FY2016": 8630751, "FY2015": 9327829, "FY2014": 5249598})),
    ("SECTION", "Expenses", {}),
    ("DATA", "Personnel expenses", m({"FY2025": -7814270, "FY2024": -7645092, "FY2023": -7169597, "FY2022": -6410143, "FY2021": -5758494, "FY2020": -5032706, "FY2019": -4875912, "FY2018": -4631460, "FY2017": -4568984, "FY2016": -3977155, "FY2015": -3714599, "FY2014": -3098242})),
    ("DATA", "Depreciation and amortisation", m({"FY2025": -376722, "FY2024": -569224, "FY2023": -608256, "FY2022": -692789, "FY2021": -695265, "FY2020": -665641, "FY2019": -637414, "FY2018": -762582, "FY2017": -769185, "FY2016": -747329, "FY2015": -901176, "FY2014": -133409})),
    ("DATA", "Other expenses", m({"FY2025": -3944957, "FY2024": -3334767, "FY2023": -2857395, "FY2022": -2558521, "FY2021": -2192538, "FY2020": -1925466, "FY2019": -2043621, "FY2018": -2262508, "FY2017": -2111124, "FY2016": -3143654, "FY2015": -2216100, "FY2014": -2499332})),
    ("DATA", "Exceptional item", m({"FY2016": -1384950})),
    ("TOTAL", "Total operating expenses", m({"FY2025": -12135949, "FY2024": -11549083, "FY2023": -10635248, "FY2022": -9661453, "FY2021": -8646297, "FY2020": -7623813, "FY2019": -7556947, "FY2018": -7656550, "FY2017": -7449293, "FY2016": -7868138, "FY2015": -6831875, "FY2014": -5730983})),
    ("TOTAL", "Profit/(loss) before provisions for impairment", m({"FY2025": 17426020, "FY2024": 18256032, "FY2023": 18025198, "FY2022": 10372520, "FY2021": 7892787, "FY2020": 6274660, "FY2019": 5910173, "FY2018": 4761042, "FY2017": 3887155, "FY2016": -622337, "FY2015": 2495954, "FY2014": -481385})),
    ("DATA", "Credit (loss)/reversal expense on financial assets", m({"FY2025": -1650686, "FY2024": -735091, "FY2023": -1048140, "FY2022": 638445, "FY2021": -661700, "FY2020": -831513, "FY2019": -563480, "FY2018": -1940})),
    ("DATA", "Provisions for impairment", m({"FY2017": -1724839, "FY2016": -1824275, "FY2015": 51000, "FY2014": 1727092})),
    ("DATA", "Impairment on building", m({"FY2023": -945738})),
    ("TOTAL", "Profit/(loss) before taxation", m({"FY2025": 15775334, "FY2024": 17520941, "FY2023": 16031320, "FY2022": 11010965, "FY2021": 7231087, "FY2020": 5443147, "FY2019": 5346693, "FY2018": 4759102, "FY2017": 2162316, "FY2016": -2446612, "FY2015": 2546954, "FY2014": 1245707})),
    ("DATA", "Taxation", m({"FY2025": -4043683, "FY2024": -4918191, "FY2023": -4081371, "FY2022": -1318592, "FY2021": -375560, "FY2020": -699355, "FY2019": -920146, "FY2018": -1046242, "FY2017": -402269, "FY2016": -643220, "FY2015": 875, "FY2014": 71725})),
    ("TOTAL", "Profit/(loss) for the year", m({"FY2025": 11731651, "FY2024": 12602750, "FY2023": 11949949, "FY2022": 9692373, "FY2021": 6855527, "FY2020": 4743792, "FY2019": 4426547, "FY2018": 3712860, "FY2017": 1760047, "FY2016": -3089832, "FY2015": 2547829, "FY2014": 1317432})),
    ("SECTION", "Other comprehensive income", {}),
    ("DATA", "Change in fair value of AFS financial assets net of tax", m({"FY2017": 140793, "FY2016": -289054, "FY2015": -476401, "FY2014": 274825})),
    ("DATA", "Change in fair value of cash flow hedge", m({"FY2025": -263833, "FY2024": 77165, "FY2023": 26161, "FY2022": -107358, "FY2021": 81691, "FY2020": -27525, "FY2019": -3236, "FY2018": 52600, "FY2017": 60349, "FY2016": -366086})),
    ("TOTAL", "Total comprehensive profit/(loss) for the year", m({"FY2025": 11467818, "FY2024": 12679915, "FY2023": 11976110, "FY2022": 9585015, "FY2021": 6937218, "FY2020": 4716267, "FY2019": 4423311, "FY2018": 3765460, "FY2017": 1961189, "FY2016": -3744972, "FY2015": 2071428, "FY2014": 1592257})),
]
bw.add_income_statement_sheet(
    title="QIB (UK) plc — Profit & Loss",
    subtitle="Entity basis, £m, converted from the Bank's reported £ amounts; FY2014-FY2025. Each year's "
              "own originally-published figures are used - see PRESENTATION NOTE / PRE-2018 PRESENTATION "
              "note at bottom.",
    rows=pl_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=66,
    source_height=520,
    unit_suffix=" (£m)",
)

equity_headers = ["Share Capital", "Fair Value Reserve on AFS Financial Assets", "Cash Flow Hedge", "Retained Earnings", "Total"]
equity_rows = [
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
    subtitle="Chronological roll-forward oldest to newest, entity basis, £m, FY2014-FY2025. Equity "
              "reconciliation ladder confirmed: every year's own closing balance ties exactly to both the "
              "next year's own opening balance and that year's own Balance Sheet Total equity, with one "
              "exception - a single explicit £21,038 restatement row is carried between FY2018's own "
              "closing balance and FY2019's own opening balance (see RESTATEMENT NOTE on the Balance "
              "Sheet/P&L sheets); no other plug rows are needed anywhere across all 12 years. The Fair "
              "Value Reserve on AFS Financial Assets column is only populated FY2014-FY2018 (blank "
              "thereafter, once the FY2018 IFRS 9 capital restructuring eliminated the AFS category); the "
              "Cash Flow Hedge column only exists from FY2016 onward. The deferred-tax movement row's "
              "label changes across years (the Bank's own wording); all years' rows represent the same "
              "underlying deferred tax adjustment on the relevant reserve/retained earnings.",
    headers=equity_headers,
    rows=equity_rows,
    sources_text=STATEMENTS_SOURCES,
)

rows = [
 ("SECTION", "Operating activities", {}),
 ("DATA", "Profit/(loss) for the year", m({"FY2025":11731651,"FY2024":12602750,"FY2023":11949949,"FY2022":9692373,"FY2021":6855527,"FY2020":4743792,"FY2019":4426546,"FY2018":3712860,"FY2017":1760047,"FY2016":-3089832,"FY2015":2547829,"FY2014":1317432})),
 ("DATA", "Depreciation", m({"FY2025":365521,"FY2024":545924,"FY2023":559334,"FY2022":533941,"FY2021":559611,"FY2020":555383,"FY2019":626025,"FY2018":688272,"FY2017":637431,"FY2016":603046,"FY2015":861601,"FY2014":105777})),
 ("DATA", "Amortisation", m({"FY2025":11201,"FY2024":23300,"FY2023":48921,"FY2022":158848,"FY2021":135654,"FY2020":110258,"FY2019":11389,"FY2018":74311,"FY2017":131754,"FY2016":142719,"FY2015":39575,"FY2014":27632})),
 ("DATA", "Fair Value on Building", m({"FY2017":-1063929,"FY2016":335768})),
 ("DATA", "ECL loss allowance and write-offs", m({"FY2020":877573,"FY2019":620430,"FY2018":-37271})),
 ("DATA", "Taxation", m({"FY2025":4043683,"FY2024":4918194,"FY2023":4081371,"FY2022":1318592,"FY2021":375560,"FY2020":699355,"FY2019":920146,"FY2018":1046242,"FY2017":402269,"FY2016":643220,"FY2015":-875,"FY2014":-71725})),
 ("DATA", "Fair value / impairment adjustments", m({"FY2025":1783183,"FY2024":898730,"FY2023":2383878,"FY2022":1490529,"FY2021":760690})),
 ("DATA", "Increase/(decrease) in impairments on financing arrangements", m({"FY2019":-56950,"FY2018":-87867,"FY2017":2246642,"FY2016":2124876,"FY2015":-54000,"FY2014":-1727092})),
 ("DATA", "(Increase)/decrease in amounts due from banks", m({"FY2017":90861366,"FY2016":-21264152,"FY2015":-46020889,"FY2014":54532317})),
 ("DATA", "Increase/(decrease) in financing arrangements", m({"FY2025":-72273531,"FY2024":-57921880,"FY2023":-44846764,"FY2022":-51177541,"FY2021":-133182070,"FY2020":-63502402,"FY2019":-49113784,"FY2018":-85674969,"FY2017":-110257569,"FY2016":-65211042,"FY2015":-138820258,"FY2014":-52303240})),
 ("DATA", "Stage 3 ECL recoveries", m({"FY2024":0,"FY2023":-3750,"FY2022":-1223974,"FY2021":-3700,"FY2020":-46061})),
 ("DATA", "Increase/(decrease) in other assets", m({"FY2025":-1238998,"FY2024":-523919,"FY2023":-53161,"FY2022":-2981020,"FY2021":-183119,"FY2020":-146783,"FY2019":-128572,"FY2018":77700,"FY2017":-696030,"FY2016":191339,"FY2015":-71184,"FY2014":-183765})),
 ("DATA", "Increase/(decrease) in amounts due to banks", m({"FY2025":24774922,"FY2024":-20343376,"FY2023":-2185645,"FY2022":-14991188,"FY2021":-5075581,"FY2020":40163454,"FY2019":-6334662,"FY2018":18938002,"FY2017":23127632,"FY2016":-84690446,"FY2015":106770791,"FY2014":-26374538})),
 ("DATA", "Increase/(decrease) in amounts due to customers", m({"FY2025":83009697,"FY2024":59016367,"FY2023":41134935,"FY2022":122440389,"FY2021":162594916,"FY2020":15031338,"FY2019":45599382,"FY2018":67938230,"FY2017":-21773283,"FY2016":172360580,"FY2015":62877356,"FY2014":85233707})),
 ("DATA", "Increase/(decrease) in other liabilities", m({"FY2025":539841,"FY2024":458933,"FY2023":-2293547,"FY2022":5356669,"FY2021":3613140,"FY2020":-6738617,"FY2019":6658681,"FY2018":4059147,"FY2017":1823046,"FY2016":4815047,"FY2015":3581353,"FY2014":-777303})),
 ("DATA", "(Increase)/decrease in financial assets held to maturity", m({"FY2017":2422970,"FY2016":1644551,"FY2015":2740534,"FY2014":536654})),
 ("DATA", "Increase/(decrease) in financial assets available for sale", m({"FY2017":8822231,"FY2016":9392574,"FY2015":-17766811,"FY2014":-48125848})),
 ("DATA", "Increase/(decrease) in financial assets at amortised cost", m({"FY2025":-3660555,"FY2024":-20589713,"FY2023":-21599498,"FY2022":-68236950,"FY2021":-14259831,"FY2020":7544997,"FY2019":-7998849,"FY2018":2771857})),
 ("DATA", "Increase/(decrease) in derivative financial instruments", m({"FY2025":1265068,"FY2024":-1126779,"FY2023":-130255,"FY2022":388846,"FY2021":-5152783,"FY2020":1700045,"FY2019":8683933,"FY2018":-7065464,"FY2017":9821270,"FY2016":-7203184,"FY2015":-273669,"FY2014":-650218})),
 ("DATA", "Source operating subtotal reconciliation (see source note)", m({"FY2024":735088,"FY2023":1050000})),
 ("TOTAL", "Net cash inflow/(outflow) from operating activities", m({"FY2025":50351683,"FY2024":-21306381,"FY2023":-9904232,"FY2022":2769514,"FY2021":17038014,"FY2020":992332,"FY2019":3913714,"FY2018":6441050,"FY2017":8265847,"FY2016":10795064,"FY2015":-23588647,"FY2014":11539790})),
 ("SECTION", "Investing activities", {}),
 ("DATA", "Purchase of property, plant and equipment", m({"FY2025":-65532,"FY2024":-685282,"FY2023":-54715,"FY2022":-4369,"FY2021":-37762,"FY2020":0,"FY2019":-153801,"FY2018":-170791,"FY2017":-164480,"FY2016":-181163,"FY2015":-2385542,"FY2014":-23974159})),
 ("DATA", "Purchase of intangible assets", m({"FY2025":-103738,"FY2021":-116000,"FY2020":-60980,"FY2019":0,"FY2018":-4729,"FY2017":-12182,"FY2016":-48197,"FY2015":-273084,"FY2014":-50973})),
 ("TOTAL", "Net cash outflow from investing activities", m({"FY2025":-169270,"FY2024":-685282,"FY2023":-54715,"FY2022":-4369,"FY2021":-153762,"FY2020":-60980,"FY2019":-153801,"FY2018":-175520,"FY2017":-176662,"FY2016":-229360,"FY2015":-2658626,"FY2014":-24025132})),
 ("SECTION", "Financing activities", {}),
 ("DATA", "Repayment/(increase) of subordinated Wakala", m({"FY2025":-35344,"FY2024":-32973,"FY2023":100909,"FY2021":-2250000,"FY2017":-250000})),
 ("DATA", "Proceeds from issuance of ordinary shares", m({"FY2017":6250000,"FY2016":0,"FY2015":23057834,"FY2014":12500000})),
 ("DATA", "Proceeds from subordinated loans/Wakala", m({"FY2016":0,"FY2015":3442166,"FY2014":3000000})),
 ("TOTAL", "Net cash (outflow)/inflow from financing activities", m({"FY2025":-35344,"FY2024":-32973,"FY2023":100909,"FY2022":0,"FY2021":-2250000,"FY2020":0,"FY2019":0,"FY2018":0,"FY2017":6000000,"FY2016":0,"FY2015":26500000,"FY2014":15500000})),
 ("TOTAL", "Net increase/(decrease) in cash and cash equivalents", m({"FY2025":50147069,"FY2024":-22024636,"FY2023":-9858038,"FY2022":2765145,"FY2021":14634252,"FY2020":931352,"FY2019":3759913,"FY2018":6265530,"FY2017":14089185,"FY2016":10565704,"FY2015":252728,"FY2014":3014658})),
 ("DATA", "Cash and cash equivalents at start of year", m({"FY2025":82318198,"FY2024":49249786,"FY2023":59107824,"FY2022":56342679,"FY2021":41708427,"FY2020":40777075,"FY2019":37017161,"FY2018":30751631,"FY2017":16662446,"FY2016":6096742,"FY2015":5844014,"FY2014":2829356})),
 ("TOTAL", "Cash and cash equivalents at end of year", m({"FY2025":132465267,"FY2024":27225150,"FY2023":49249786,"FY2022":59107824,"FY2021":56342679,"FY2020":41708427,"FY2019":40777075,"FY2018":37017161,"FY2017":30751631,"FY2016":16662446,"FY2015":6096742,"FY2014":5844014})),
]
bw.add_cash_flow_sheet(title="QIB (UK) plc — Statement of Cash Flows", subtitle="Entity basis, £m, converted from the Bank's reported £ amounts; FY2014-FY2025.", rows=rows, sources_text=CASH_SOURCES, first_col_width=66, source_height=340, unit_suffix=" (£m)")

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
)

def metric(name, unit, data, note=None): bw.add_metric_sheet(name, unit, data, p3_sources(), note=note, first_col_width=50, source_height=340)
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
metric("CET1 Capital","£m",[("Common Equity Tier 1 (CET1) capital",cap)],"FY2014/FY2015 are the Bank's own narrative-disclosed round figures (£25.9m/£49.1m), not from a numeric capital table; FY2016 is FY2017's own comparative column.")
metric("CET1 Ratio","% of RWA",[("Common Equity Tier 1 ratio",ratios["CET1 Ratio"])],"FY2014/FY2015: no CET1 ratio is disclosed in the reviewed QIB UK Pillar 3 documents (narrative capital amounts only, no RWA denominator given).")
metric("Tier 1 Capital","£m",[("Tier 1 capital",cap)],"KM1/Note 4 report Tier 1 equal to CET1; no AT1 capital is reported in any reviewed year.")
metric("Tier 1 Ratio","% of RWA",[("Tier 1 ratio",ratios["CET1 Ratio"])],"Tier 1 ratio equals the CET1 ratio in every reviewed year (no AT1 capital).")
metric("Total Capital","£m",[("Total capital",total)],"FY2014/FY2015 total capital is derived as Tier 1 + Tier 2 from the Bank's own narrative figures (not itself a single disclosed line for those two years).")
metric("Total Capital Ratio","% of RWA",[("Total capital ratio",ratios["Total Capital Ratio"])],"FY2014/FY2015: no Total Capital ratio is disclosed (no RWA denominator given).")
metric("Total RWAs","£m",[("Total risk-weighted exposure amount",rwa)],"FY2014/FY2015: no RWA figure is disclosed in the reviewed QIB UK Pillar 3 documents for these two years.")

rwa_breakdown_rows = [
    ("DATA", "Credit risk (excluding CCR)", {"FY2025": 634.742, "FY2024": 548.789, "FY2023": 500.902, "FY2022": 465.681, "FY2021": 432.383}),
    ("DATA", "Counterparty credit risk (CCR, including CVA)", {"FY2025": 3.345, "FY2024": 4.023, "FY2023": 1.390, "FY2022": 1.852, "FY2021": 2.166}),
    ("DATA", "Position, foreign exchange and commodities risk (market risk)", {"FY2025": 0.049, "FY2024": 0.053, "FY2023": 0.122, "FY2022": 0.044, "FY2021": 0.031}),
    ("DATA", "Credit and counterparty credit risk, combined (pre-2021 template)", {"FY2020": 392.457, "FY2018": 336, "FY2017": 316, "FY2016": 249}),
    ("DATA", "Market risk (pre-2021 template)", {"FY2020": 0.026, "FY2018": 0, "FY2017": 1, "FY2016": 1}),
    ("DATA", "Credit valuation adjustment (CVA) (pre-2021 template)", {"FY2020": 0.736}),
    ("DATA", "Operational risk", {"FY2025": 55.017, "FY2024": 49.062, "FY2023": 40.771, "FY2022": 31.545, "FY2021": 27.440, "FY2020": 24.864, "FY2018": 18, "FY2017": 18, "FY2016": 14}),
    ("TOTAL", "Total risk-weighted exposure amount", {"FY2025": 693.154, "FY2024": 601.927, "FY2023": 543.185, "FY2022": 499.122, "FY2021": 462.020, "FY2020": 418.084, "FY2019": 375.285, "FY2018": 354, "FY2017": 335, "FY2016": 264}),
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
)

metric("Leverage Ratio","%",[("Leverage ratio excluding claims on central banks",ratios["Leverage Ratio"])],"Not numerically disclosed in the reviewed QIB UK documents before FY2019 (FY2019 figure is FY2020's own comparative column).")
metric("LCR","%",[("Liquidity coverage ratio",ratios["LCR"])],"Not numerically disclosed in the reviewed QIB UK documents before FY2019 (FY2019 figure is FY2020's own comparative column); narrative mentions of the LCR regime starting 1 October 2015 appear from the FY2015 Pillar 3 Declaration onward, but with no percentage given.")
metric("NSFR","%",[("Net stable funding ratio",ratios["NSFR"])],"No NSFR is disclosed in the reviewed QIB UK Pillar 3 documents through FY2020; the FY2020 document states the Bank was still 'monitoring' NSFR ahead of implementation.")
metric("MREL Ratio","%",[("MREL ratio",{y:"Not publicly disclosed" for y in YEARS})],"No MREL ratio or requirement is disclosed in the reviewed QIB UK Pillar 3 documents.")

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
