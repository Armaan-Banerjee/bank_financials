import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = [
    "FY2025", "FY2024", "FY2023", "FY2022", "FY2021",
    "FY2020", "FY2019", "FY2018", "FY2017", "FY2016", "FY2015", "FY2014",
    "FY2013", "FY2012", "FY2011", "FY2010", "FY2009", "FY2008",
]
Y_CORE = YEARS[:YEARS.index('FY2014') + 1]  # HD-072/075/079: FY2014-floor default for Pillar 3/Asset Quality/RWA Breakdown/Overview
  # most recent first

AR2021_URL = "https://pic.bankofchina.com/bocappd/uk/202303/P020230331590070165221.pdf"
AR2022_URL = "https://pic.bankofchina.com/bocappd/uk/202403/P020240315379765805794.pdf"
AR2023_URL = "https://pic.bankofchina.com/bocappd/uk/202405/P020240508355110735895.pdf"
AR2024_URL = "https://pic.bankofchina.com/bocappd/uk/202507/P020250718380377744220.pdf"
AR2025_URL = "https://pic.bankofchina.com/bocappd/uk/202605/P020260506389809417235.pdf"

P3_2021_URL = "https://www.bankofchina.com/uk/aboutus/ab5/202303/P020230315381669571541.pdf"
P3_2022_URL = "https://www.bankofchina.com/uk/aboutus/ab5/202310/P020231026347190320350.pdf"
P3_2023_URL = "https://www.bankofchina.com/uk/aboutus/ab5/202410/P020241008402737321677.pdf"
P3_2024_URL = "https://www.bankofchina.com/uk/aboutus/ab5/202507/P020250718380587744231.pdf"
P3_2025_URL = "https://pic.bankofchina.com/bocappd/uk/202607/P020260716391457618567.pdf"

# --- HD-046 (2026-09-05): FY2014-FY2020 extension, capped at FY2014 by explicit
# user decision even though the entity's own archive genuinely runs to FY2008
# (HD-001's reference finding). All 14 documents below are still live on
# bankofchina.com/pic.bankofchina.com (confirmed via direct HTTP fetch, no
# Wayback fallback needed) - the deepest, cleanest self-hosted archive found
# across the whole HD- effort so far.
AR2020_URL = "https://pic.bankofchina.com/bocappd/uk/202109/P020210902654360894172.pdf"
AR2019_URL = "https://pic.bankofchina.com/bocappd/uk/202007/P020200727323473194461.pdf"
AR2018_URL = "https://pic.bankofchina.com/bocappd/uk/201904/P020190410506087628158.pdf"
AR2017_URL = "https://pic.bankofchina.com/bocappd/uk/201805/P020180517534275167127.pdf"
AR2016_URL = "https://pic.bankofchina.com/bocappd/uk/201706/P020170627373089457851.pdf"
AR2015_URL = "https://pic.bankofchina.com/bocappd/uk/201606/P020160620504225340480.pdf"
AR2014_URL = "https://pic.bankofchina.com/bocappd/uk/201505/P020150504352614441641.pdf"

P3_2020_URL = "https://pic.bankofchina.com/bocappd/uk/202110/P020211027537761891740.pdf"
P3_2019_URL = "https://pic.bankofchina.com/bocappd/uk/202009/P020200909535865685853.pdf"
P3_2018_URL = "https://pic.bankofchina.com/bocappd/uk/201904/P020190410408108385209.pdf"
P3_2017_URL = "https://pic.bankofchina.com/bocappd/uk/201803/P020180328577372288229.pdf"
P3_2016_URL = "https://pic.bankofchina.com/bocappd/uk/201706/P020170627381103226068.pdf"
P3_2015_URL = "https://pic.bankofchina.com/bocappd/uk/201606/P020160620504436264971.pdf"
P3_2014_URL = "https://pic.bankofchina.com/bocappd/uk/201509/P020150910375228515274.pdf"

AR2014_SCAN_NOTE = (
    "AR2014_URL note: the Bank's own FY2014 Annual Report PDF is a scanned/photocopied "
    "document (Canon iR-ADV C5045 scanner output) with no extractable text layer - "
    "pdftotext and qpdf both confirm zero recoverable text after a repair pass. FY2014 "
    "figures on every sheet are therefore taken from the FY2015 Annual Report's own "
    "FY2014 comparative column instead (a real, live, text-searchable document), the "
    "same each-year's-own-report methodology used everywhere else in this workbook, "
    "just one year removed since FY2014's own PDF cannot be read as text."
)

# --- HD-075 (2026-09-06): FY2013-FY2008 extension of the four statutory-statement
# sheets only (Balance Sheet, Profit & Loss, Statement of Changes in Equity, Cash Flow
# Statement) - Pillar 3, Asset Quality and RWA Breakdown are untouched and simply gain
# no new-year entries. All 6 documents below are confirmed live on bankofchina.com's
# own "Annual Reports" archive page (uk/aboutus/ab4/), continuing the same self-hosted
# archive HD-046 found for FY2014-FY2020.
AR2013_URL = "https://pic.bankofchina.com/bocappd/uk/201505/P020150504339499661074.pdf"
AR2012_URL = "https://pic.bankofchina.com/bocappd/uk/201312/P020131213310466908739.pdf"
AR2011_URL = "https://pic.bankofchina.com/bocappd/uk/201301/P020130110394685934112.pdf"
AR2010_URL = "https://pic.bankofchina.com/bocappd/uk/201206/P020120618317067419492.pdf"
AR2009_URL = "https://pic.bankofchina.com/bocappd/uk/201109/P020110901339600023124.pdf"
AR2008_URL = "https://pic.bankofchina.com/bocappd/uk/201109/P020110901339400504145.pdf"

AR2013_SCAN_NOTE = (
    "AR2013_URL note: the Bank's own FY2013 Annual Report PDF is a scanned/photocopied "
    "document (Xerox WorkCentre 5665 scanner output) with no extractable text layer, the "
    "same pattern HD-046 found on FY2014's own PDF. Unlike FY2014 (where a later year's "
    "clean comparative column exists), FY2014's own PDF is itself unreadable, so no clean "
    "comparative source exists for FY2013 either - FY2013 figures here were instead OCR'd "
    "directly off this scanned PDF (ocrmypdf --force-ocr + tesseract), then cross-checked "
    "two ways: (1) the resulting FY2013 closing equity/balance-sheet/cash-flow figures tie "
    "out internally (assets = liabilities + equity; operating + investing + financing cash "
    "flows = the disclosed net movement; opening + net movement = closing cash) and (2) the "
    "OCR'd FY2013 closing Statement of Changes in Equity figures match this workbook's own "
    "pre-existing FY2014 opening balance exactly (250,000 / 56,831 / 843 / 307,674), which "
    "was itself sourced independently via AR2015's FY2014 comparative column under HD-046. "
    "Several individual OCR digit errors were caught and corrected via these tie-outs (e.g. "
    "'Interest income from financial investments' misread as 4,294 instead of 1,294, 'Total "
    "assets' misread as 4,050,075 instead of 1,050,075 - a recurring 1-to-4 OCR confusion in "
    "this particular scan)."
)

AR2010_SCAN_NOTE = (
    "AR2010_URL note: the Bank's own FY2010 Annual Report PDF is a scanned/photocopied "
    "document (Canon iR-ADV C5045 scanner output, the same scanner/pattern as FY2014's own "
    "PDF) with no extractable text layer. FY2010 figures on every sheet are therefore taken "
    "from the FY2011 Annual Report's own FY2010 comparative column instead (a real, live, "
    "text-searchable document), the same each-year's-own-report-one-year-removed "
    "methodology used for FY2014 via AR2015."
)

FY2008_PERIOD_NOTE = (
    "FY2008 period note: Bank of China (UK) Limited's first accounting period ran 1 April "
    "2007 - 30 September 2007 (a 6-month stub, outside this workbook's scope), and its "
    "second and only 'FY2008' statutory period is genuinely a 15-month period from 1 "
    "October 2007 to 31 December 2008 (the year-end was moved to December during this "
    "period) - not a standard 12-month year. Both the Bank's own FY2008 Report and "
    "Financial Statements (AR2008_URL) and the FY2009 Report's own FY2008 comparative "
    "column (AR2009_URL) show this identical 15-month figure set, cross-checked and tying "
    "exactly. Shown here as 'FY2008' per this workbook's year-labelling convention, but "
    "flagged as non-comparable in length to every other year in this workbook - growth "
    "trends spanning the FY2008/FY2009 boundary should be read with that caveat."
)

ENTITY_NOTE = (
    "Entity note: Bank of China (UK) Limited (company 06193060, FRN 467410) is a wholly-owned UK subsidiary of "
    "Bank of China Limited (state-owned). It does not take the FRS 101/102 cash-flow-statement exemption - a full "
    "Statement of Cash Flows is published every year. All figures are the Bank's own solo entity basis throughout."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are Bank of China (UK) Limited's own Statement of Cash Flows, £'000, as published on "
    "the Bank's own site (each year's own originally-published report, not a later restated comparative):\n"
    f"FY2025: Annual Report and Financial Statements for the year ended 31 December 2025, p.51-52 - {AR2025_URL}\n"
    f"FY2024: Annual Report and Financial Statements for the year ended 31 December 2024, p.52-53 - {AR2024_URL}\n"
    f"FY2023: Annual Report and Financial Statements for the year ended 31 December 2023, p.52-53 - {AR2023_URL}\n"
    f"FY2022: Financial Statements for the year ended 31 December 2022, p.40 - {AR2022_URL}\n"
    f"FY2021: Financial Statements for the year ended 31 December 2021, p.37 - {AR2021_URL}\n"
    f"FY2020: Financial Statements for the year ended 31 December 2020, p.34-35 - {AR2020_URL}\n"
    f"FY2019: Financial Statements for the year ended 31 December 2019, p.33-34 - {AR2019_URL}\n"
    f"FY2018: Financial Statements for the year ended 31 December 2018, p.28-29 - {AR2018_URL}\n"
    f"FY2017: Financial Statements for the year ended 31 December 2017, p.26-27 - {AR2017_URL}\n"
    f"FY2016: Financial Statements for the year ended 31 December 2016, p.21-22 - {AR2016_URL}\n"
    f"FY2015: Financial Statements for the year ended 31 December 2015, p.20-21 - {AR2015_URL}\n"
    f"FY2014: Financial Statements 2015's own FY2014 comparative column, p.20-21 - {AR2015_URL} ({AR2014_SCAN_NOTE})\n"
    f"FY2013: Annual Report and Financial Statements 2013, p.18-19 - {AR2013_URL} ({AR2013_SCAN_NOTE})\n"
    f"FY2012: Annual Report 2012, p.26 - {AR2012_URL}\n"
    f"FY2011: Annual Report 2011, p.26 - {AR2011_URL}\n"
    f"FY2010: Annual Report 2011's own FY2010 comparative column, p.26 - {AR2011_URL} ({AR2010_SCAN_NOTE})\n"
    f"FY2009: 2009 Report and Financial Statements, p.33 - {AR2009_URL}\n"
    f"FY2008: 2009 Report's own FY2008 comparative column, p.33 - {AR2009_URL}, cross-checked against the Bank's "
    f"own 2008 Report and Financial Statements (Statement of Cash Flows, p.31) - {AR2008_URL} (figures identical). "
    + FY2008_PERIOD_NOTE + "\n"
    "FY2008-FY2020 presentation note: through FY2020's own report, 'Dividend paid' and 'Interest paid' sit inside "
    "the operating-activities 'Adjustment for cash items' subsection (own rows here, labelled '...FY2008-FY2020 "
    "presentation' to distinguish them from the FY2021-onward financing-section rows of the same name, which are "
    "left blank for FY2008-FY2020 rather than merged into a single row spanning two different statement "
    "sections); 'Cash flows from financing activities' is genuinely nil every year FY2008-FY2019 and, in FY2020's "
    "own report, contains only the new lease-liability repayment line. FY2014's cash flow figure (£199,854k) was "
    "confirmed against the Balance Sheet's own internal subtotal arithmetic (see the Balance Sheet sheet's own "
    "source note, HD-081 2026-09-07) - the Balance Sheet's originally-transcribed £199,954k was a single-digit "
    "misread that broke its own 'Total assets' subtotal by £100k; every year's cash-flow closing balance ties "
    "exactly to that year's own Balance Sheet cash figure. Individual "
    "reconciling items were independently verified by summing each year's disclosed components back to that "
    "year's own reported 'Net cash generated from operating activities' total (all matched exactly), used as a "
    "correction check against several PDFs' garbled OCR text (e.g. FY2014's 'Acquisition of intangible assets' "
    "printed without its minus sign was resolved to -£426k this way).\n"
    "HD-075 extension presentation notes (FY2008-FY2013): FY2008-FY2009's own statements separately disclose "
    "'Change in derivative assets/liabilities held for risk management' (folded into the FY2014+ 'Change in "
    "derivative financial instruments assets/liabilities' rows here); FY2010-FY2012 combine both into a single "
    "'Change in derivatives held for risk management' line instead (its own row, not force-split). FY2012's own "
    "statement presents 'Proceeds from the issue of ordinary shares' (£110,000k, the same capital raise recorded "
    "on the Statement of Changes in Equity sheet) and 'Investment in subsidiaries' (£62,210k, the same-year "
    "subsidiary disposal) both under investing activities rather than financing (own rows, noting this year's "
    "presentation); FY2013's own restated FY2012 comparative instead splits the ordinary-share proceeds into "
    "financing activities - this workbook uses each year's own originally-published presentation throughout, per "
    "project convention, so FY2012's own figures stay under investing here. FY2013's own statement has no "
    "corresponding 'Loss/(gain) on disposal of subsidiary' cash-flow addback despite the Income Statement's "
    "one-off £1,632k gain that year - confirmed absent by full-text reading of the OCR'd document and by the "
    "fact that FY2013's own operating/investing/financing subtotals already tie exactly to its own disclosed "
    "opening/closing cash balances without one (see AR2013_SCAN_NOTE). FY2009's own statement includes a "
    "standalone 'Effects of exchange-rate changes on cash and cash equivalents' line (-£2,477k) between the net "
    "movement and closing balance, not present in any other year (own row). Every FY2008-FY2013 year's cash-flow "
    "closing balance ties exactly to that year's own Balance Sheet cash figure, and every operating/investing/"
    "financing subtotal for these 6 years was independently verified by full-component summation against each "
    "year's own disclosed net-movement and opening/closing balances (all matched exactly, including through the "
    "FY2013 OCR reconstruction).\n"
    "Restatement note: FY2023's own report marks its FY2022 comparative column 'Restated' and shows different "
    "figures (e.g. operating activities -£17,138k, closing cash £687,013k) to FY2022's own originally-published "
    "report (operating activities +£22,570k, closing cash £657,656k). This workbook uses each year's own "
    "originally-published figures as the primary column (project convention), which creates a genuine, disclosed "
    "£29,357k gap between FY2022's own closing balance and FY2023's own opening balance - flagged here rather "
    "than silently blended or force-reconciled. The underlying cause of the restatement is not explained in "
    "either source.\n"
    "Presentation notes: FY2021-FY2023 include small 'Exchange rate movements on plant and equipment/on equity' "
    "lines not present in FY2024/FY2025's statements. FY2022 alone shows a one-off Tier 2-to-AT1 capital "
    "replacement (subordinated debt of £60,000k repaid, an equal Additional Tier 1 instrument issued, both under "
    "financing activities). FY2025's own report split 'Change in financial assets at amortised cost/fair value' "
    "into two lines (the government-bond component shown separately) and separated lease-liability cash flows "
    "into principal and interest portions for the first time - both are FY2025-only presentational changes with "
    "no net impact on any section total. FY2025's own supplementary 'cash and cash equivalents comprise' note "
    "totals £1,073,245k (£157k less than the statement's own £1,073,402k closing balance), a gap matching the "
    "same page's separately-shown expected-credit-loss allowance of £157k - the statement's own total is used as "
    "the primary closing-balance figure here. FY2022's own report does not break out a separate 'Interest paid "
    "on Additional Tier 1 instrument' line (the AT1 instrument was only issued in June 2022); FY2023's restated "
    "FY2022 comparative does show one (£1,759k), consistent with the broader FY2022 restatement noted above - "
    "not included here since it wasn't part of FY2022's own originally-published statement.\n"
    + ENTITY_NOTE
)


def p3_sources():
    return (
        "Sources - Bank of China (UK) Limited Pillar 3 disclosures (UK KM1 Key Metrics template from FY2022 "
        "onward; FY2021's own document is narrative/ratio-only and predates the KM1 template; FY2014-FY2020 use "
        "the pre-KM1 CRD IV 'Table 1: Total capital resources and risk asset ratios' / 'Table 2: Leverage ratio' "
        "narrative-table format), £'000 unless stated:\n"
        f"FY2025 & FY2024 comparative: Pillar 3 Disclosure 31 December 2025, p.15 (UK KM1) - {P3_2025_URL}\n"
        f"FY2024 (own year) & FY2023 comparative: Pillar 3 Disclosures 31 December 2024, p.16 (UK KM1) - {P3_2024_URL}\n"
        f"FY2023 (own year) & FY2022 comparative: Pillar 3 disclosures 31 December 2023, p.14 (UK KM1) - {P3_2023_URL}\n"
        f"FY2022 (own year) & FY2021 comparative: Pillar 3 Disclosures 2022, p.14 (UK KM1) - {P3_2022_URL}\n"
        f"FY2021 (own year, narrative/ratio-only - no KM1 template yet): Pillar 3 Disclosures 2021, p.12-14, 24 - {P3_2021_URL}\n"
        "FY2021 note: the Bank's own FY2021 Pillar 3 document states CET1/Total Capital as rounded £275m/£335m "
        "and gives no £-breakdown for leverage exposure, LCR HQLA/outflow, or NSFR (NSFR was not yet a formal "
        "disclosure). The precise FY2021 figures used on those sheets (CET1/Tier 1 £275,164k, Total Capital "
        "£335,164k, leverage exposure £2,431,869k, LCR HQLA £527,697k/outflow £294,774k, NSFR £1,438,026k/"
        "£950,742k) are taken from the FY2022 Pillar 3 document's FY2021 comparative column instead, since it is "
        "the more complete disclosure - all overlapping ratios (CET1 24.6%, Total Capital 29.9%, Leverage 11.3%, "
        "LCR 179.0%) match the FY2021 document's own narrative figures exactly.\n"
        f"FY2020 (own year) & FY2019 comparative: Pillar 3 Disclosures 31 December 2020, Table 9 'Overview of "
        f"risk weighted assets', p.20-22, Table 31 'Liquidity coverage ratio' - {P3_2020_URL}\n"
        f"FY2019 (own year) & FY2018 comparative: Pillar 3 Disclosures 31 December 2019, p.16-19, 33 - {P3_2019_URL}\n"
        f"FY2018 (own year) & FY2017 comparative: Pillar 3 Disclosures 31 December 2018, p.15-18, 31 - {P3_2018_URL}\n"
        f"FY2017 (own year) & FY2016 comparative: Pillar 3 Disclosures 2017, Table 1/Table 2, p.9-10 - {P3_2017_URL}\n"
        f"FY2016 (own year) & FY2015 comparative: Pillar 3 Disclosures 2016, Table 1/Table 2, p.10-11 - {P3_2016_URL}\n"
        f"FY2015 (own year) & FY2014 comparative: Pillar III Disclosures 2015, Table 1/Table 2, p.9-10 - {P3_2015_URL}\n"
        f"FY2014 (own year) & FY2013 comparative: Pillar III Disclosure 2014, Table 1/Table 2, p.8-9 - {P3_2014_URL}\n"
        "FY2014-FY2017 note: 'Tier 1 capital' equals 'CET1 capital' every year (£274,958k throughout - the Bank "
        "issued no AT1 instruments until far later) and 'Total capital' equals CET1 capital plus the £60,000k "
        "Tier 2 subordinated debt facility, both stated directly in each year's own Table 1. LCR and NSFR are "
        "genuinely undisclosed for FY2014-FY2016 (no LCR/HQLA/NSFR concept appears anywhere in those 3 documents, "
        "confirmed by reading each in full); FY2017's LCR ratio (167%) is not in FY2017's own document at all "
        "(confirmed absent) but appears as the FY2018 Pillar 3 document's own FY2017 comparative column, the "
        "earliest point any LCR figure for this bank exists - shown here with no £-breakdown since none is given "
        "for that comparative year. RWA breakdown by risk category (credit/market/operational/CVA) is genuinely "
        "undisclosed for FY2014-FY2018 (only the single aggregate RWA figure appears in each Table 1); the FY2020 "
        "Pillar 3 document introduces a full 'Table 9: Overview of risk weighted assets' (its own year plus its "
        "own FY2019 comparative column), the first and only such breakdown found across all 12 years covered.\n"
        + ENTITY_NOTE
    )


bw = BankWorkbook(bank_name="Bank of China (UK) Limited", years=Y_CORE, year_label={y: y for y in YEARS}, header_color="B22222")

# ---------------------------------------------------------------
# Sheet: Balance Sheet
# ---------------------------------------------------------------
AR2024_OWN_NOTE = (
    "FY2024's own primary source is its own report (AR2024_URL), not AR2025's comparative column - both are "
    "identical figures (verified), no restatement."
)

balance_sheet_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and balances at central banks", {"FY2025": 982512, "FY2024": 975201, "FY2023": 687070, "FY2022": 657656, "FY2021": 716133, "FY2020": 481379, "FY2019": 332542, "FY2018": 333275, "FY2017": 281944, "FY2016": 311917, "FY2015": 344019, "FY2014": 199854, "FY2013": 159219, "FY2012": 197622, "FY2011": 275821, "FY2010": 215155, "FY2009": 127812, "FY2008": 40069}),
    ("DATA", "Government bonds", {"FY2025": 142529, "FY2024": 144495, "FY2023": 118328, "FY2022": 44264}),
    ("DATA", "Loans and advances to banks", {"FY2025": 90733, "FY2024": 73658, "FY2023": 86477, "FY2022": 29357, "FY2021": 69065, "FY2020": 110446, "FY2019": 85247, "FY2018": 61391, "FY2017": 83706, "FY2016": 24270, "FY2015": 62633, "FY2014": 207026, "FY2013": 168898, "FY2012": 48779, "FY2011": 12865, "FY2010": 12817, "FY2009": 36933, "FY2008": 67272}),
    ("DATA", "Loans and advances to customers", {"FY2025": 810985, "FY2024": 941507, "FY2023": 990763, "FY2022": 1122459, "FY2021": 1194653, "FY2020": 1138583, "FY2019": 1064347, "FY2018": 1044570, "FY2017": 1054454, "FY2016": 1159696, "FY2015": 810776, "FY2014": 722307, "FY2013": 581030, "FY2012": 464479, "FY2011": 290752, "FY2010": 214623, "FY2009": 504743, "FY2008": 551148}),
    ("DATA", "Derivative financial instruments", {"FY2025": 2504, "FY2024": 4667, "FY2023": 5506, "FY2022": 7702, "FY2021": 11, "FY2020": 48163, "FY2019": 4614, "FY2018": 1344, "FY2017": 1717, "FY2016": 4577, "FY2015": 8173, "FY2014": 16173, "FY2013": 41502, "FY2012": 1949, "FY2011": 72, "FY2010": 505, "FY2009": 1375, "FY2008": 5554}),
    ("DATA", "Prepayments, accrued income and other assets", {"FY2025": 156554, "FY2024": 138246, "FY2023": 130581, "FY2022": 351967, "FY2021": 87868, "FY2020": 78769, "FY2019": 58405, "FY2018": 6273, "FY2017": 5204, "FY2016": 4762, "FY2015": 25831, "FY2014": 27820, "FY2013": 66602, "FY2012": 64084, "FY2011": 37692, "FY2010": 46427, "FY2009": 29780, "FY2008": 21197}),
    ("DATA", "Financial assets at fair value through profit and loss", {"FY2025": 71293, "FY2024": 30150, "FY2023": 47445, "FY2022": 60514, "FY2021": 64659, "FY2020": 77482, "FY2019": 83928, "FY2018": 76171}),
    ("DATA", "Available for sale financial investments", {"FY2017": 12, "FY2016": 40716, "FY2015": 35859, "FY2014": 37469, "FY2013": 28754, "FY2012": 46270, "FY2011": 95671, "FY2010": 149677, "FY2009": 249004, "FY2008": 330093}),
    ("DATA", "Held to maturity / debt instruments at amortised cost", {"FY2019": 50431, "FY2018": 103189, "FY2017": 107478}),
    ("DATA", "Investment in subsidiary/group companies", {"FY2011": 63285, "FY2010": 94357, "FY2009": 29945, "FY2008": 32128}),
    ("DATA", "Current tax asset", {"FY2025": 4582, "FY2024": 2934, "FY2023": 637, "FY2022": 2351, "FY2021": 5979}),
    ("DATA", "Deferred tax assets", {"FY2025": 289, "FY2024": 406, "FY2023": 359, "FY2022": 1280, "FY2021": 1283, "FY2020": 1227, "FY2019": 787, "FY2018": 1546, "FY2017": 1462, "FY2016": 562, "FY2015": 425, "FY2014": 751, "FY2013": 276, "FY2012": 206, "FY2011": 30, "FY2010": 4, "FY2009": 16, "FY2008": 5656}),
    ("DATA", "Property, plant and equipment", {"FY2025": 11573, "FY2024": 11419, "FY2023": 11902, "FY2022": 12769, "FY2021": 11167, "FY2020": 4527, "FY2019": 6328, "FY2018": 2761, "FY2017": 3149, "FY2016": 3276, "FY2015": 3514, "FY2014": 3390, "FY2013": 3765, "FY2012": 4032, "FY2011": 1374, "FY2010": 1612, "FY2009": 2025, "FY2008": 2371}),
    ("DATA", "Intangible assets", {"FY2025": 887, "FY2024": 636, "FY2023": 305, "FY2022": 274, "FY2021": 362, "FY2020": 529, "FY2019": 759, "FY2018": 462, "FY2017": 95, "FY2016": 122, "FY2015": 180, "FY2014": 326, "FY2013": 29, "FY2012": 106, "FY2011": 163, "FY2010": 317, "FY2009": 440, "FY2008": 321}),
    ("TOTAL", "Total assets", {"FY2025": 2274441, "FY2024": 2323319, "FY2023": 2079373, "FY2022": 2290593, "FY2021": 2151180, "FY2020": 1941105, "FY2019": 1687388, "FY2018": 1630982, "FY2017": 1539221, "FY2016": 1549898, "FY2015": 1291410, "FY2014": 1215116, "FY2013": 1050075, "FY2012": 827527, "FY2011": 777725, "FY2010": 735494, "FY2009": 982073, "FY2008": 1055809}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Deposits from banks", {"FY2025": 511961, "FY2024": 493256, "FY2023": 369590, "FY2022": 539387, "FY2021": 396254, "FY2020": 219378, "FY2019": 128590, "FY2018": 102919, "FY2017": 123122, "FY2016": 164849, "FY2015": 136736, "FY2014": 40270, "FY2013": 72132, "FY2012": 62384, "FY2011": 202684, "FY2010": 176070, "FY2009": 366763, "FY2008": 560116}),
    ("DATA", "Deposits from customers", {"FY2025": 1304816, "FY2024": 1355529, "FY2023": 1223068, "FY2022": 1291150, "FY2021": 1333523, "FY2020": 1215647, "FY2019": 1132193, "FY2018": 1107439, "FY2017": 1019007, "FY2016": 982361, "FY2015": 737724, "FY2014": 765899, "FY2013": 537699, "FY2012": 398239, "FY2011": 352176, "FY2010": 296289, "FY2009": 378219, "FY2008": 290289}),
    ("DATA", "Derivative financial instruments", {"FY2025": 289, "FY2024": 2, "FY2023": 3, "FY2022": 13, "FY2021": 5280, "FY2020": 56924, "FY2019": 8771, "FY2018": 1977, "FY2017": 257, "FY2016": 4150, "FY2015": 11505, "FY2014": 21499, "FY2013": 42505, "FY2012": 3435, "FY2011": 4416, "FY2010": 5956, "FY2009": 5766, "FY2008": 5390}),
    ("DATA", "Other liabilities", {"FY2025": 39574, "FY2024": 37473, "FY2023": 38352, "FY2022": 50379, "FY2021": 43571, "FY2020": 36086, "FY2019": 43609, "FY2018": 21359, "FY2017": 20158, "FY2016": 13620, "FY2015": 17145, "FY2014": 18089, "FY2013": 23787, "FY2012": 19123, "FY2011": 15290, "FY2010": 14205, "FY2009": 13404, "FY2008": 10601}),
    ("DATA", "Accruals and deferred income", {"FY2025": 18650, "FY2024": 23257, "FY2023": 15017, "FY2022": 7720, "FY2021": 5657, "FY2020": 5705, "FY2019": 6390, "FY2018": 6207, "FY2017": 4176, "FY2016": 5874, "FY2015": 4512, "FY2014": 4016, "FY2013": 3729, "FY2012": 4828, "FY2011": 3602, "FY2010": 3137, "FY2009": 2166, "FY2008": 4099}),
    ("DATA", "Current tax liabilities", {"FY2020": 4891, "FY2019": 675, "FY2018": 4908, "FY2017": 5447, "FY2016": 8680, "FY2015": 3520, "FY2014": 3873, "FY2013": 2521, "FY2012": 3715, "FY2010": 14184, "FY2009": 4106, "FY2008": 195}),
    ("DATA", "Deferred tax liabilities", {"FY2013": 28, "FY2008": 14}),
    ("DATA", "Impairment provision on off balance sheet products", {"FY2025": 138, "FY2024": 58, "FY2023": 54, "FY2022": 51, "FY2021": 119, "FY2020": 310, "FY2019": 102, "FY2018": 97}),
    ("DATA", "Subordinated liabilities", {"FY2021": 60000, "FY2020": 60000, "FY2019": 60000, "FY2018": 60000, "FY2017": 60000, "FY2016": 60000, "FY2015": 60000, "FY2014": 60000, "FY2013": 60000, "FY2012": 60000, "FY2011": 60000, "FY2010": 60000, "FY2009": 60000, "FY2008": 60000}),
    ("TOTAL", "Total liabilities", {"FY2025": 1875428, "FY2024": 1909575, "FY2023": 1646084, "FY2022": 1888700, "FY2021": 1844404, "FY2020": 1598941, "FY2019": 1380330, "FY2018": 1304906, "FY2017": 1232167, "FY2016": 1239534, "FY2015": 971142, "FY2014": 913636, "FY2013": 742401, "FY2012": 551724, "FY2011": 638168, "FY2010": 569841, "FY2009": 830424, "FY2008": 930704}),
    ("SECTION", "Equity", {}),
    ("DATA", "Authorised and called up share capital", {"FY2025": 250000, "FY2024": 250000, "FY2023": 250000, "FY2022": 250000, "FY2021": 250000, "FY2020": 250000, "FY2019": 250000, "FY2018": 250000, "FY2017": 250000, "FY2016": 250000, "FY2015": 250000, "FY2014": 250000, "FY2013": 250000, "FY2012": 250000, "FY2011": 140000, "FY2010": 140000, "FY2009": 140000, "FY2008": 140000}),
    ("DATA", "Other equity instruments (Additional Tier 1)", {"FY2025": 60000, "FY2024": 60000, "FY2023": 60000, "FY2022": 60000}),
    ("DATA", "Retained earnings", {"FY2025": 89013, "FY2024": 103744, "FY2023": 123289, "FY2022": 91893, "FY2021": 56776, "FY2020": 92164, "FY2019": 57058, "FY2018": 76076, "FY2017": 57022, "FY2016": 60648, "FY2015": 70408, "FY2014": 50913, "FY2013": 56831, "FY2012": 24958, "FY2011": 528, "FY2010": 26598, "FY2009": 15819, "FY2008": 3259}),
    ("DATA", "Available for sale reserve", {"FY2017": 32, "FY2016": -284, "FY2015": -140, "FY2014": 567, "FY2013": 843, "FY2012": 845, "FY2011": -971, "FY2010": -945, "FY2009": -4170, "FY2008": -18154}),
    ("TOTAL", "Total shareholders' equity", {"FY2025": 399013, "FY2024": 413744, "FY2023": 433289, "FY2022": 401893, "FY2021": 306776, "FY2020": 342164, "FY2019": 307058, "FY2018": 326076, "FY2017": 307054, "FY2016": 310364, "FY2015": 320268, "FY2014": 301480, "FY2013": 307674, "FY2012": 275803, "FY2011": 139557, "FY2010": 165653, "FY2009": 151649, "FY2008": 125105}),
    ("TOTAL", "Total liabilities and equity", {"FY2025": 2274441, "FY2024": 2323319, "FY2023": 2079373, "FY2022": 2290593, "FY2021": 2151180, "FY2020": 1941105, "FY2019": 1687388, "FY2018": 1630982, "FY2017": 1539221, "FY2016": 1549898, "FY2015": 1291410, "FY2014": 1215116, "FY2013": 1050075, "FY2012": 827527, "FY2011": 777725, "FY2010": 735494, "FY2009": 982073, "FY2008": 1055809}),
]

BALANCE_SHEET_SOURCES = (
    "Sources - Bank of China (UK) Limited's own Statement of Financial Position (Bank/solo basis - no group "
    "accounts prepared, Companies Act 2006 s.401 exemption), £'000, each year's own originally-published report:\n"
    f"FY2025: Annual Report 2025, p.49 - {AR2025_URL}\n"
    f"FY2024: Annual Report 2024, p.49 - {AR2024_URL} ({AR2024_OWN_NOTE})\n"
    f"FY2023: Annual Report 2023, p.50 - {AR2023_URL}\n"
    f"FY2022: Financial Statements 2022, p.38 - {AR2022_URL}\n"
    f"FY2021: Financial Statements 2021, p.35 - {AR2021_URL}\n"
    f"FY2020: Financial Statements 2020, p.33 - {AR2020_URL}\n"
    f"FY2019: Financial Statements 2019, p.32 - {AR2019_URL}\n"
    f"FY2018: Financial Statements 2018, p.27 - {AR2018_URL}\n"
    f"FY2017: Financial Statements 2017, p.25 - {AR2017_URL}\n"
    f"FY2016: Financial Statements 2016, p.20 - {AR2016_URL}\n"
    f"FY2015: Financial Statements 2015, p.19 - {AR2015_URL}\n"
    f"FY2014: Financial Statements 2015's own FY2014 comparative column, p.19 - {AR2015_URL} ({AR2014_SCAN_NOTE})\n"
    f"FY2013: Annual Report and Financial Statements 2013, p.17 - {AR2013_URL} ({AR2013_SCAN_NOTE})\n"
    f"FY2012: Annual Report 2012, p.24 - {AR2012_URL}\n"
    f"FY2011: Annual Report 2011, p.24 - {AR2011_URL}\n"
    f"FY2010: Annual Report 2011's own FY2010 comparative column, p.24 - {AR2011_URL} ({AR2010_SCAN_NOTE})\n"
    f"FY2009: 2009 Report and Financial Statements, p.31 - {AR2009_URL}\n"
    f"FY2008: 2009 Report's own FY2008 comparative column, p.31 - {AR2009_URL}, cross-checked against the Bank's "
    f"own 2008 Report and Financial Statements (Balance Sheet, p.29) - {AR2008_URL} (figures identical). "
    + FY2008_PERIOD_NOTE + "\n"
    "HD-075 extension presentation notes (FY2008-FY2013): 'Investment in subsidiary/group companies' is its own "
    "row for these 6 years only (a real, non-nil balance - the subsidiary was disposed of during FY2012, hence "
    "nil/omitted from FY2014 onward). 'Deferred tax liabilities' is its own row for FY2008 (£14k) and FY2013 "
    "(£28k) only - nil/not disclosed as a separate line in every other year shown. 'Authorised and called up "
    "share capital' rose from £140,000k to £250,000k during FY2012 via a £110,000k ordinary share issue (see the "
    "Statement of Changes in Equity sheet). FY2013's Balance Sheet total assets/liabilities were affected by two "
    "OCR digit corrections cross-checked against the statement's own subtotals - see AR2013_SCAN_NOTE.\n"
    "Presentation notes: 'Government bonds' only appears as its own line from FY2022 onward. 'Subordinated "
    "liabilities' (£60,000k every year FY2014-FY2021) was repaid and replaced by an equal £60,000k Additional "
    "Tier 1 instrument in June 2022 - both nil/blank in the years they don't apply. 'Investment in subsidiary "
    "companies' is nil every year and omitted as a row. 'Available for sale financial investments' and its "
    "matching equity 'Available for sale reserve' existed under IAS 39 through FY2017 and were replaced by "
    "'Financial assets at fair value through profit and loss' / 'Debt instruments at amortised cost' at the "
    "1 January 2018 IFRS 9 transition (a £495k opening-equity charge that year, see the Statement of Changes "
    "in Equity sheet) - both pairs of rows are blank/zero in the years they don't apply, not force-matched. "
    "FY2021's own report's Statement of Changes in Equity states closing retained earnings as £56,706k, £70k "
    "less than the Balance Sheet's own £56,776k for the same date - the Balance Sheet's single 'Retained "
    "earnings' line appears to combine the SOCE's separate retained-earnings and FX-translation-reserve columns "
    "(£56,706k + £70k = £56,776k); the same pattern recurs one year earlier at FY2020 (SOCE retained earnings "
    "£92,228k + FX reserve -£64k = Balance Sheet's own £92,164k); total equity ties out exactly either way in "
    "both years. FY2014 cash resolved (HD-081, 2026-09-07): FY2015's own filing originally appeared to show two "
    "different FY2014 cash figures - £199,954k on the Balance Sheet's comparative column vs. £199,854k on the "
    "Cash Flow Statement's own comparative closing balance. Re-summing FY2014's own 9 asset line items as "
    "originally transcribed (199,954 + 207,026 + 722,307 + 16,173 + 27,820 + 37,469 + 751 + 3,390 + 326) gives "
    "£1,215,216k, £100k more than the Balance Sheet's own stated 'Total assets' of £1,215,116k for that column; "
    "substituting £199,854k for the cash line instead sums to exactly £1,215,116k. The Balance Sheet's own "
    "internal subtotal therefore only ties out with £199,854k, confirming £199,954k was a single-digit "
    "transcription/OCR misread of the FY2015 filing's FY2014 comparative column (a 9 misread for an 8 in the "
    "thousands place) and that £199,854k, matching the Cash Flow Statement, is the correct figure. Corrected "
    "here to £199,854k; FY2014's own primary report remains unreadable as text (see AR2014_SCAN_NOTE), so this "
    "arithmetic cross-check within FY2015's own filing is the resolving evidence.\n"
    + ENTITY_NOTE
)

bw.add_balance_sheet_sheet(
    title="Bank of China (UK) Limited — Statement of Financial Position",
    subtitle="Bank of China (UK) Limited (solo entity basis), £'000",
    rows=balance_sheet_rows,
    sources_text=BALANCE_SHEET_SOURCES,
    first_col_width=68,
    source_height=200,
    unit_suffix=" (£'000)",
    years=YEARS,
)

# ---------------------------------------------------------------
# Sheet: Profit & Loss
# ---------------------------------------------------------------
income_statement_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest income", {"FY2025": 110123, "FY2024": 128817, "FY2023": 121217, "FY2022": 62661, "FY2021": 36936, "FY2020": 40327, "FY2019": 45693, "FY2018": 40759, "FY2017": 38234, "FY2016": 34591, "FY2015": 25645, "FY2014": 26082, "FY2013": 18724, "FY2012": 14523, "FY2011": 12956, "FY2010": 16182, "FY2009": 20622, "FY2008": 54071}),
    ("DATA", "Interest expense", {"FY2025": -53024, "FY2024": -57415, "FY2023": -40422, "FY2022": -13239, "FY2021": -3650, "FY2020": -6276, "FY2019": -9313, "FY2018": -6553, "FY2017": -5788, "FY2016": -4629, "FY2015": -3095, "FY2014": -3635, "FY2013": -2800, "FY2012": -2828, "FY2011": -2828, "FY2010": -3858, "FY2009": -7677, "FY2008": -35584}),
    ("TOTAL", "Net interest income", {"FY2025": 57099, "FY2024": 71402, "FY2023": 80795, "FY2022": 49422, "FY2021": 33286, "FY2020": 34051, "FY2019": 36380, "FY2018": 34206, "FY2017": 32446, "FY2016": 29962, "FY2015": 22550, "FY2014": 22447, "FY2013": 15924, "FY2012": 11695, "FY2011": 10128, "FY2010": 12324, "FY2009": 12945, "FY2008": 18487}),
    ("DATA", "Fee and commission income", {"FY2025": 3399, "FY2024": 3228, "FY2023": 3378, "FY2022": 3955, "FY2021": 4294, "FY2020": 3627, "FY2019": 4674, "FY2018": 4850, "FY2017": 5502, "FY2016": 4029, "FY2015": 8906, "FY2014": 7109, "FY2013": 9445, "FY2012": 7448, "FY2011": 6353, "FY2010": 6317, "FY2009": 3689, "FY2008": 3886}),
    ("DATA", "Fee and commission expense", {"FY2025": -1462, "FY2024": -1481, "FY2023": -1692, "FY2022": -1694, "FY2021": -1319, "FY2020": -1549, "FY2019": -1170, "FY2018": -886, "FY2017": -813, "FY2016": -776, "FY2015": -582, "FY2014": -1022, "FY2013": -580, "FY2012": -783, "FY2011": -507, "FY2010": -170, "FY2009": -135, "FY2008": -238}),
    ("TOTAL", "Net fee and commission income", {"FY2025": 1937, "FY2024": 1747, "FY2023": 1686, "FY2022": 2261, "FY2021": 2975, "FY2020": 2078, "FY2019": 3504, "FY2018": 3964, "FY2017": 4689, "FY2016": 3253, "FY2015": 8324, "FY2014": 6087, "FY2013": 8865, "FY2012": 6665, "FY2011": 5846, "FY2010": 6147, "FY2009": 3554, "FY2008": 3648}),
    ("DATA", "Net fair value gain/(loss) on financial instruments", {"FY2025": 3431, "FY2024": 4711, "FY2023": 9119, "FY2022": 148, "FY2021": 1923, "FY2020": -3151, "FY2019": -1165, "FY2018": -331, "FY2017": 51, "FY2016": 241, "FY2015": 511, "FY2014": -1413, "FY2013": 826}),
    ("DATA", "Net gain/(loss) on derivative financial instruments (FY2008-FY2012 presentation)", {"FY2012": -1478, "FY2011": -927, "FY2010": -2312, "FY2009": -2181, "FY2008": -3314}),
    ("DATA", "Foreign exchange gain", {"FY2025": 2388, "FY2024": 2295, "FY2023": 386, "FY2022": 4916, "FY2021": 2590, "FY2020": 1489, "FY2019": 4767, "FY2018": 3167, "FY2017": 2593, "FY2016": 2827, "FY2015": 2492, "FY2014": 2100, "FY2013": 554, "FY2012": 1688, "FY2011": -2080, "FY2010": 262, "FY2009": 303, "FY2008": 915}),
    ("DATA", "Net other operating income", {"FY2025": 123435, "FY2024": 107108, "FY2023": 114199, "FY2022": 93633, "FY2021": 83274, "FY2020": 85636, "FY2019": 71751, "FY2018": 73555, "FY2017": 54704, "FY2016": 54899, "FY2015": 61054, "FY2014": 42403, "FY2013": 42508, "FY2012": 45390, "FY2011": 25698, "FY2010": 30331, "FY2009": 19368, "FY2008": 9501}),
    ("DATA", "Gain/(loss) on sale of debt securities", {"FY2014": -3, "FY2013": -436, "FY2012": -23, "FY2011": -1298, "FY2010": -190, "FY2009": 534, "FY2008": 2495}),
    ("DATA", "Profit on sale of impaired loan", {"FY2013": 2158}),
    ("TOTAL", "Non-interest income", {"FY2025": 129254, "FY2024": 114114, "FY2023": 123704, "FY2022": 98697, "FY2021": 87787, "FY2020": 83974, "FY2019": 75353, "FY2018": 76391, "FY2017": 57348, "FY2016": 57967, "FY2015": 64047, "FY2014": 43087, "FY2013": 45610, "FY2012": 45577, "FY2011": 21393, "FY2010": 28091, "FY2009": 18024, "FY2008": 9597}),
    ("TOTAL", "Total income", {"FY2025": 188290, "FY2024": 187263, "FY2023": 206185, "FY2022": 150380, "FY2021": 124048, "FY2020": 120103, "FY2019": 115237, "FY2018": 114561, "FY2017": 94483, "FY2016": 91182, "FY2015": 94921, "FY2014": 71621, "FY2013": 70399, "FY2012": 63937, "FY2011": 37367, "FY2010": 46562, "FY2009": 34523, "FY2008": 31732}),
    ("SECTION", "Expenses", {}),
    ("DATA", "Staff costs", {"FY2025": -86079, "FY2024": -72194, "FY2023": -68058, "FY2022": -59208, "FY2021": -50154, "FY2020": -47607, "FY2019": -47279, "FY2018": -41868, "FY2017": -41365, "FY2016": -32821, "FY2015": -29500, "FY2014": -30178, "FY2013": -24489, "FY2012": -19227, "FY2011": -16203, "FY2010": -13759, "FY2009": -11761, "FY2008": -11629}),
    ("DATA", "Other expenses", {"FY2025": -10029, "FY2024": -9735, "FY2023": -9543, "FY2022": -9818, "FY2021": -8924, "FY2020": -18816, "FY2019": -23048, "FY2018": -7857, "FY2017": -7870, "FY2016": -6914, "FY2015": -6544, "FY2014": -6402, "FY2013": -4987, "FY2012": -5779, "FY2011": -4657, "FY2010": -4044, "FY2009": -3702, "FY2008": -5767}),
    ("DATA", "Depreciation of plant and equipment", {"FY2025": -1870, "FY2024": -1540, "FY2023": -1572, "FY2022": -1462, "FY2021": -1802, "FY2020": -2342, "FY2019": -2498, "FY2018": -691, "FY2017": -794, "FY2016": -918, "FY2015": -965, "FY2014": -859, "FY2013": -831, "FY2012": -589, "FY2011": -507, "FY2010": -516, "FY2009": -496, "FY2008": -292}),
    ("DATA", "Amortisation of intangible assets", {"FY2025": -161, "FY2024": -104, "FY2023": -52, "FY2022": -271, "FY2021": -237, "FY2020": -256, "FY2019": -100, "FY2018": -53, "FY2017": -45, "FY2016": -144, "FY2015": -146, "FY2014": -129, "FY2013": -47, "FY2012": -105, "FY2011": -160, "FY2010": -161, "FY2009": -106, "FY2008": -84}),
    # Derived subtotal, not itself a printed AR line - sum of the four genuine operating-cost
    # rows above (Staff costs + Other expenses + Depreciation + Amortisation). Deliberately
    # excludes "Credit/(provision) for expected credit losses", "Impairment of investment in
    # subsidiary", and "Gain/(loss) on disposal of subsidiary" below, since those are credit-risk
    # / one-off items rather than operating expenses under standard cost-to-income convention.
    # Added so the cross-bank insights cost-to-income-ratio pipeline (in041_spend_metrics.py) has
    # a TOTAL-tagged opex row to divide into "Total income" above.
    ("TOTAL", "Total operating expenses (sum of Staff costs + Other expenses + Depreciation + Amortisation - excludes credit loss provisions and subsidiary items per standard cost-to-income convention, not itself a printed AR subtotal)", {"FY2025": -98139, "FY2024": -83573, "FY2023": -79225, "FY2022": -70759, "FY2021": -61117, "FY2020": -69021, "FY2019": -72925, "FY2018": -50469, "FY2017": -50074, "FY2016": -40797, "FY2015": -37155, "FY2014": -37568, "FY2013": -30354, "FY2012": -25700, "FY2011": -21527, "FY2010": -18480, "FY2009": -16065, "FY2008": -17772}),
    ("DATA", "Credit/(provision) for expected credit losses", {"FY2025": 217, "FY2024": 3953, "FY2023": 11235, "FY2022": 11526, "FY2021": -23665, "FY2020": -3172, "FY2019": -377, "FY2018": 458, "FY2017": 187, "FY2016": -527, "FY2015": 155, "FY2014": -722, "FY2013": -60, "FY2012": -4455, "FY2011": -8272, "FY2010": -35, "FY2009": -1827, "FY2008": -9386}),
    ("DATA", "Impairment of investment in subsidiary", {"FY2011": -31432, "FY2010": -8432}),
    ("DATA", "Gain/(loss) on disposal of subsidiary", {"FY2015": -1707, "FY2013": 1632, "FY2012": -1074}),
    ("TOTAL", "Profit before income tax", {"FY2025": 90368, "FY2024": 107643, "FY2023": 138195, "FY2022": 91147, "FY2021": 39266, "FY2020": 47910, "FY2019": 41935, "FY2018": 64550, "FY2017": 44596, "FY2016": 49858, "FY2015": 56214, "FY2014": 33331, "FY2013": 41617, "FY2012": 32708, "FY2011": -23864, "FY2010": 19615, "FY2009": 16631, "FY2008": 4574}),
    ("DATA", "Income tax expense", {"FY2025": -21437, "FY2024": -23726, "FY2023": -34982, "FY2022": -22583, "FY2021": -7788, "FY2020": -12745, "FY2019": -9830, "FY2018": -13427, "FY2017": -12532, "FY2016": -14168, "FY2015": -10764, "FY2014": -7376, "FY2013": -9744, "FY2012": -8278, "FY2011": -2206, "FY2010": -8836, "FY2009": -4071, "FY2008": -1562}),
    ("TOTAL", "Profit/(loss) for the year", {"FY2025": 68931, "FY2024": 83917, "FY2023": 103213, "FY2022": 68564, "FY2021": 31478, "FY2020": 35165, "FY2019": 32105, "FY2018": 51123, "FY2017": 32064, "FY2016": 35690, "FY2015": 45450, "FY2014": 25955, "FY2013": 31873, "FY2012": 24430, "FY2011": -26070, "FY2010": 10779, "FY2009": 12560, "FY2008": 3012}),
    ("SECTION", "Other comprehensive income", {}),
    ("DATA", "Foreign currency translation", {"FY2025": 80, "FY2023": -2, "FY2022": 12, "FY2021": 134, "FY2020": -59}),
    ("DATA", "Net change in fair value of available-for-sale financial assets (net of tax)", {"FY2017": 316, "FY2016": -144, "FY2015": -707, "FY2014": -276, "FY2013": -2, "FY2012": 1816, "FY2011": -26, "FY2010": 3225, "FY2009": 13984, "FY2008": -18154}),
    ("TOTAL", "Other comprehensive income/(expense) for the year", {"FY2025": 80, "FY2024": 0, "FY2023": -2, "FY2022": 12, "FY2021": 134, "FY2020": -59, "FY2019": 0, "FY2018": 0, "FY2017": 316, "FY2016": -144, "FY2015": -707, "FY2014": -276, "FY2013": -2, "FY2012": 1816, "FY2011": -26, "FY2010": 3225, "FY2009": 13984, "FY2008": -18154}),
    ("TOTAL", "Total comprehensive income/(expense) for the year", {"FY2025": 69011, "FY2024": 83917, "FY2023": 103211, "FY2022": 68576, "FY2021": 31612, "FY2020": 35106, "FY2019": 32105, "FY2018": 51123, "FY2017": 32380, "FY2016": 35546, "FY2015": 44743, "FY2014": 25679, "FY2013": 31871, "FY2012": 26246, "FY2011": -26096, "FY2010": 14004, "FY2009": 26544, "FY2008": -15142}),
]

INCOME_STATEMENT_SOURCES = (
    "Sources - Bank of China (UK) Limited's own Income Statement / Statement of Comprehensive Income (Bank/solo "
    "basis), £'000, each year's own originally-published report:\n"
    f"FY2025: Annual Report 2025, p.47-48 - {AR2025_URL}\n"
    f"FY2024: Annual Report 2024, p.48-49 - {AR2024_URL} ({AR2024_OWN_NOTE})\n"
    f"FY2023: Annual Report 2023, p.48-49 - {AR2023_URL}\n"
    f"FY2022: Financial Statements 2022, p.36-37 - {AR2022_URL}\n"
    f"FY2021: Financial Statements 2021, p.33-34 - {AR2021_URL}\n"
    f"FY2020: Financial Statements 2020, p.31-32 - {AR2020_URL}\n"
    f"FY2019: Financial Statements 2019, p.30-31 - {AR2019_URL}\n"
    f"FY2018: Financial Statements 2018, p.24-26 - {AR2018_URL}\n"
    f"FY2017: Financial Statements 2017, p.23-24 - {AR2017_URL}\n"
    f"FY2016: Financial Statements 2016, p.18-19 - {AR2016_URL}\n"
    f"FY2015: Financial Statements 2015, p.16-18 - {AR2015_URL}\n"
    f"FY2014: Financial Statements 2015's own FY2014 comparative column, p.16-18 - {AR2015_URL} ({AR2014_SCAN_NOTE})\n"
    f"FY2013: Annual Report and Financial Statements 2013, p.15-16 - {AR2013_URL} ({AR2013_SCAN_NOTE})\n"
    f"FY2012: Annual Report 2012, p.22-23 - {AR2012_URL}\n"
    f"FY2011: Annual Report 2011, p.22-23 - {AR2011_URL}\n"
    f"FY2010: Annual Report 2011's own FY2010 comparative column, p.22-23 - {AR2011_URL} ({AR2010_SCAN_NOTE})\n"
    f"FY2009: 2009 Report and Financial Statements, p.28-29 - {AR2009_URL}\n"
    f"FY2008: 2009 Report's own FY2008 comparative column, p.28-29 - {AR2009_URL}, cross-checked against the "
    f"Bank's own 2008 Report and Financial Statements (Income Statement, p.28) - {AR2008_URL} (figures identical). "
    + FY2008_PERIOD_NOTE + "\n"
    "HD-075 extension presentation notes (FY2008-FY2013): FY2008-FY2012 present a single 'Net gain/(loss) on "
    "derivative financial instruments' line (its own row here) instead of the 'Net fair value gain/(loss) on "
    "financial instruments' concept first used from FY2013 onward - both blank in the years the other applies, "
    "not force-mapped together. FY2013's own P&L shows one-off 'Loss on sale of debt securities' (-£436k) and "
    "'Profit on sale of impaired loan' (+£2,158k) as separate lines; FY2012's 'Loss on disposal of subsidiary' "
    "(-£1,074k) reverses to a one-off '+£1,632k' gain in FY2013 (own row, renamed 'Gain/(loss) on disposal of "
    "subsidiary' to accommodate both signs across the years it appears). FY2010-FY2011 show a one-off "
    "'Impairment of investment in subsidiary' expense (£8,432k / £31,432k respectively, its own row) relating to "
    "the same UK subsidiary later disposed of in FY2012. FY2009-FY2008's 'Other expenses' row is labelled "
    "'Administration and general expenses' in both years' own reports (same concept, folded into this row for "
    "consistency with FY2010 onward). Every FY2008-FY2013 year's Other Comprehensive Income is a single combined "
    "available-for-sale fair-value movement (net of tax), consistent with the existing FY2014-FY2017 row.\n"
    "Profit before income tax ties exactly to the Cash Flow Statement's own 'Profit before income tax' row for "
    "every year, cross-checked as a reconciliation. Presentation notes: FY2014's Income Statement splits "
    "'Interest income' into 'Interest income from financial investments' + 'Other interest income' sub-lines "
    "through FY2020 (summed into the single 'Interest income' row here to match FY2021 onward's presentation - "
    "e.g. FY2014's £654k + £25,428k = £26,082k). FY2014's own P&L shows a one-off £3k 'Loss on sale of debt "
    "securities' (its own row here, income section); FY2015's own P&L shows a separate one-off £1,707k 'Loss on "
    "disposal of subsidiary' (its own row here, expenses section, immediately before Profit before income tax) - "
    "neither recurs in any other year. Other comprehensive income was governed by IAS 39's 'available for sale "
    "financial assets' fair-value reserve through FY2017 (its own row here) before the 1 January 2018 IFRS 9 "
    "transition removed the AFS category entirely (FY2018/FY2019 OCI is genuinely nil); the 'Foreign currency "
    "translation' OCI item used FY2021 onward first appears at FY2020 (a different, unrelated OCI component, not "
    "a renamed AFS reserve) - both rows are blank in the years the other applies, not force-matched.\n"
    + ENTITY_NOTE
)

bw.add_income_statement_sheet(
    title="Bank of China (UK) Limited — Income Statement and Statement of Comprehensive Income",
    subtitle="Bank of China (UK) Limited (solo entity basis), £'000",
    rows=income_statement_rows,
    sources_text=INCOME_STATEMENT_SOURCES,
    first_col_width=68,
    source_height=180,
    unit_suffix=" (£'000)",
    years=YEARS,
)

# ---------------------------------------------------------------
# Sheet: Statement of Changes in Equity
# ---------------------------------------------------------------
EQUITY_HEADERS = ["Issued share capital", "Other equity instruments", "Retained earnings", "Available for sale reserve", "Foreign currency translation reserve", "Total"]

equity_changes_rows = [
    ("DATA", "As at 1 October 2007", (140000, 0, 247, None, None, 140247)),
    ("DATA", "Unrealised loss on available for sale investments, net of tax", (0, 0, 0, -18154, None, -18154)),
    ("DATA", "Profit for the financial period (15 months to 31 December 2008)", (0, 0, 3012, 0, None, 3012)),
    ("TOTAL", "Total comprehensive income/(expense) for the period", (0, 0, 3012, -18154, None, -15142)),
    ("TOTAL", "As at 31 December 2008", (140000, 0, 3259, -18154, None, 125105)),
    ("DATA", "Unrealised profit on available for sale investments, net of tax", (0, 0, 0, 13984, None, 13984)),
    ("DATA", "Profit for the financial year", (0, 0, 12560, 0, None, 12560)),
    ("TOTAL", "Total comprehensive income", (0, 0, 12560, 13984, None, 26544)),
    ("TOTAL", "As at 31 December 2009", (140000, 0, 15819, -4170, None, 151649)),
    ("DATA", "Unrealised profit on available for sale investments, net of tax", (0, 0, 0, 3225, None, 3225)),
    ("DATA", "Profit for the financial year", (0, 0, 10779, 0, None, 10779)),
    ("TOTAL", "Total comprehensive income", (0, 0, 10779, 3225, None, 14004)),
    ("TOTAL", "As at 31 December 2010", (140000, 0, 26598, -945, None, 165653)),
    ("DATA", "Unrealised loss on available for sale investments, net of tax", (0, 0, 0, -26, None, -26)),
    ("DATA", "Loss for the financial year", (0, 0, -26070, 0, None, -26070)),
    ("TOTAL", "Total comprehensive expense", (0, 0, -26070, -26, None, -26096)),
    ("TOTAL", "As at 31 December 2011", (140000, 0, 528, -971, None, 139557)),
    ("DATA", "Unrealised gain on available for sale investments, net of tax", (0, 0, 0, 1816, None, 1816)),
    ("DATA", "Profit for the financial year", (0, 0, 24430, 0, None, 24430)),
    ("TOTAL", "Total comprehensive income", (0, 0, 24430, 1816, None, 26246)),
    ("DATA", "Issue of ordinary shares", (110000, 0, 0, 0, None, 110000)),
    ("TOTAL", "As at 31 December 2012", (250000, 0, 24958, 845, None, 275803)),
    ("DATA", "Unrealised loss on available for sale investments, net of tax", (0, 0, 0, -2, None, -2)),
    ("DATA", "Profit for the financial year", (0, 0, 31873, 0, None, 31873)),
    ("TOTAL", "Total comprehensive income", (0, 0, 31873, -2, None, 31871)),
    ("TOTAL", "As at 31 December 2013", (250000, 0, 56831, 843, None, 307674)),
    ("DATA", "Unrealised loss on available for sale investments, net of tax", (0, 0, 0, -276, None, -276)),
    ("DATA", "Profit for the financial year", (0, 0, 25955, 0, None, 25955)),
    ("TOTAL", "Total comprehensive income", (0, 0, 25955, -276, None, 25679)),
    ("DATA", "Dividend paid", (0, 0, -31873, 0, None, -31873)),
    ("TOTAL", "As at 31 December 2014", (250000, 0, 50913, 567, None, 301480)),
    ("DATA", "Unrealised loss on available for sale investments, net of tax", (0, 0, 0, -707, None, -707)),
    ("DATA", "Profit for the financial year", (0, 0, 45450, 0, None, 45450)),
    ("TOTAL", "Total comprehensive income", (0, 0, 45450, -707, None, 44743)),
    ("DATA", "Dividend paid", (0, 0, -25955, 0, None, -25955)),
    ("TOTAL", "As at 31 December 2015", (250000, 0, 70408, -140, None, 320268)),
    ("DATA", "Unrealised loss on available for sale investments, net of tax", (0, 0, 0, -144, None, -144)),
    ("DATA", "Profit for the financial year", (0, 0, 35690, 0, None, 35690)),
    ("TOTAL", "Total comprehensive income", (0, 0, 35690, -144, None, 35546)),
    ("DATA", "Dividend paid", (0, 0, -45450, 0, None, -45450)),
    ("TOTAL", "As at 31 December 2016", (250000, 0, 60648, -284, None, 310364)),
    ("DATA", "Unrealised gain on available for sale investments, net of tax", (0, 0, 0, 316, None, 316)),
    ("DATA", "Profit for the financial year", (0, 0, 32064, 0, None, 32064)),
    ("TOTAL", "Total comprehensive income", (0, 0, 32064, 316, None, 32380)),
    ("DATA", "Dividend paid", (0, 0, -35690, 0, None, -35690)),
    ("TOTAL", "As at 31 December 2017", (250000, 0, 57022, 32, None, 307054)),
    ("DATA", "Impact of adopting IFRS 9 (1 January 2018)", (0, 0, -463, -32, None, -495)),
    ("TOTAL", "Restated opening balance under IFRS 9", (250000, 0, 56559, 0, None, 306559)),
    ("DATA", "Profit for the financial year", (0, 0, 51123, None, None, 51123)),
    ("TOTAL", "Total comprehensive income", (0, 0, 51123, None, None, 51123)),
    ("DATA", "Dividend paid", (0, 0, -31606, None, None, -31606)),
    ("TOTAL", "As at 31 December 2018", (250000, 0, 76076, None, None, 326076)),
    ("DATA", "Profit for the financial year", (0, 0, 32105, None, None, 32105)),
    ("TOTAL", "Total comprehensive income", (0, 0, 32105, None, None, 32105)),
    ("DATA", "Foreign exchange and other", (0, 0, -5, None, None, -5)),
    ("DATA", "Dividend paid", (0, 0, -51118, None, None, -51118)),
    ("TOTAL", "As at 31 December 2019", (250000, 0, 57058, None, None, 307058)),
    ("DATA", "FY2020 report's re-split of the FY2019 closing balance (retained earnings/FX reserve)", (0, 0, 5, None, -5, 0)),
    ("DATA", "Profit for the financial year", (0, 0, 35165, None, 0, 35165)),
    ("DATA", "Foreign exchange and other", (0, 0, 0, None, -59, -59)),
    ("TOTAL", "Total comprehensive income", (0, 0, 35165, None, -59, 35106)),
    ("TOTAL", "As at 31 December 2020", (250000, 0, 92228, None, -64, 342164)),
    ("DATA", "Profit for the financial year", (0, 0, 31478, None, 0, 31478)),
    ("DATA", "Foreign exchange and other", (0, 0, 0, None, 134, 134)),
    ("TOTAL", "Total comprehensive income", (0, 0, 31478, None, 134, 31612)),
    ("DATA", "Dividend paid", (0, 0, -67000, None, 0, -67000)),
    ("TOTAL", "As at 31 December 2021", (250000, 0, 56706, None, 70, 306776)),
    ("DATA", "Additional Tier 1 capital issued", (0, 60000, 0, None, 0, 60000)),
    ("DATA", "Profit for the financial year", (0, 0, 68564, None, 0, 68564)),
    ("DATA", "Foreign exchange and other", (0, 0, 0, None, 12, 12)),
    ("TOTAL", "Total comprehensive income", (0, 0, 68564, None, 12, 68576)),
    ("DATA", "Dividend paid", (0, 0, -33459, None, 0, -33459)),
    ("TOTAL", "As at 31 December 2022", (250000, 60000, 91811, None, 82, 401893)),
    ("DATA", "Profit for the financial year", (0, 0, 103213, None, 0, 103213)),
    ("DATA", "Foreign exchange and other", (0, 0, 0, None, -2, -2)),
    ("TOTAL", "Total comprehensive income", (0, 0, 103213, None, -2, 103211)),
    ("DATA", "Dividend paid", (0, 0, -71815, None, 0, -71815)),
    ("TOTAL", "As at 31 December 2023", (250000, 60000, 123209, None, 80, 433289)),
    ("DATA", "Profit for the financial year", (0, 0, 83917, None, 0, 83917)),
    ("TOTAL", "Total comprehensive income", (0, 0, 83917, None, 0, 83917)),
    ("DATA", "Dividend paid", (0, 0, -103462, None, 0, -103462)),
    ("TOTAL", "As at 31 December 2024", (250000, 60000, 103664, None, 80, 413744)),
    ("DATA", "Profit for the financial year", (0, 0, 68931, None, 0, 68931)),
    ("DATA", "Transfer", (0, 0, 80, None, -80, 0)),
    ("TOTAL", "Total comprehensive income", (0, 0, 69011, None, 0, 69011)),
    ("DATA", "Dividend paid", (0, 0, -83662, None, 0, -83662)),
    ("TOTAL", "As at 31 December 2025", (250000, 60000, 89013, None, 0, 399013)),
]

EQUITY_CHANGES_SOURCES = (
    "Sources - Bank of China (UK) Limited's own Statement of Changes in Equity (Bank/solo basis), £'000, "
    "chronological roll-forward reconstructed from each year's own originally-published report:\n"
    f"2008 movements (15-month period): Financial Statements 2009's own FY2008 comparative (Statement of "
    f"Changes in Equity), p.32 - {AR2009_URL}, cross-checked against the Bank's own 2008 Report and Financial "
    f"Statements, which uses the older 'Statement of Recognised Income and Expenses' format instead (no roll-"
    f"forward table) but shows an identical opening (£140,247k, 'As of 1 October 2007') and closing (£125,105k) "
    f"position - {AR2008_URL}. " + FY2008_PERIOD_NOTE + "\n"
    f"2009 movements: 2009 Report and Financial Statements, p.32 - {AR2009_URL}\n"
    f"2010 movements: Annual Report 2011's own FY2010 comparative, p.25 - {AR2011_URL} ({AR2010_SCAN_NOTE})\n"
    f"2011 movements: Annual Report 2011, p.25 - {AR2011_URL}\n"
    f"2012 movements: Annual Report 2012, p.25 (includes the £110,000k ordinary share issue that took share "
    f"capital from £140,000k to £250,000k) - {AR2012_URL}\n"
    f"2013 movements: Annual Report and Financial Statements 2013, p.18 - {AR2013_URL} ({AR2013_SCAN_NOTE})\n"
    f"2014 movements: Financial Statements 2015's own FY2014 comparative, p.17 - {AR2015_URL} ({AR2014_SCAN_NOTE})\n"
    f"2015 movements: Financial Statements 2015, p.17 - {AR2015_URL}\n"
    f"2016 movements: Financial Statements 2016, p.20 - {AR2016_URL}\n"
    f"2017 movements: Financial Statements 2017, p.25 - {AR2017_URL}\n"
    f"2018 movements: Financial Statements 2018, p.27 - {AR2018_URL}\n"
    f"2019 movements: Financial Statements 2019, p.32 - {AR2019_URL}\n"
    f"2020 movements: Financial Statements 2020, p.33 - {AR2020_URL}\n"
    f"2021 movements: Financial Statements 2021, p.36 - {AR2021_URL}\n"
    f"2022 movements: Financial Statements 2022, p.39 - {AR2022_URL}\n"
    f"2023 movements: Annual Report 2023, p.51 - {AR2023_URL}\n"
    f"2024 movements: Annual Report 2024, p.50 - {AR2024_URL} ({AR2024_OWN_NOTE})\n"
    f"2025 movements: Annual Report 2025, p.50 - {AR2025_URL}\n"
    "Note: the 'Dividend paid' row in this statement (which includes both ordinary share dividends and Additional "
    "Tier 1 coupon/interest payments to the parent) differs from the Cash Flow Statement's separately-split "
    "'Dividend paid'/'Interest paid on Additional Tier 1 instrument' lines - e.g. FY2025's £83,662k here vs "
    "£78,700k + £4,962k = £83,662k on the Cash Flow Statement (ties out exactly once combined; genuinely two "
    "different presentations of the same total, not a discrepancy). "
    "The 'Available for sale reserve' column applied under IAS 39 through the FY2018 IFRS 9 transition (a "
    "£495k opening-equity charge, split £463k retained earnings / £32k AFS reserve per the Bank's own FY2018 and "
    "FY2019 reports); the 'Foreign currency translation reserve' column is a separate, later, unrelated OCI "
    "component that first appears at FY2020 - both are blank in the years the other applies, not force-matched, "
    "and there is a genuine one-year gap (FY2019) where neither column is populated (OCI was nil that year). A "
    "restatement-split quirk is flagged rather than silently resolved: the FY2019 closing balance is shown twice "
    "with a different retained-earnings/FX-reserve split - £57,058k/blank per FY2019's own report (its own "
    "presentation had no separate FX column yet) as 'As at 31 December 2019', and £57,063k/-£5k per FY2020's own "
    "report's FY2019 opening comparative (which introduced the new column and re-split the same £57,058k total); "
    "the FY2020 movement rows that follow use this second, FY2020-report split as their starting point. The "
    "FY2021 opening balance is likewise stated directly from FY2021's own report rather than carried forward "
    "arithmetically, and ties out exactly to the FY2020 closing row above it.\n"
    + ENTITY_NOTE
)

bw.add_equity_changes_sheet(
    title="Bank of China (UK) Limited — Statement of Changes in Equity",
    subtitle="Bank of China (UK) Limited (solo entity basis), £'000, chronological",
    headers=EQUITY_HEADERS,
    rows=equity_changes_rows,
    sources_text=EQUITY_CHANGES_SOURCES,
    first_col_width=42,
    source_height=190,
)

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Cash flows from operating activities", {}),
    ("DATA", "Profit before income tax", {"FY2025": 90368, "FY2024": 107644, "FY2023": 138195, "FY2022": 91147, "FY2021": 39266, "FY2020": 47910, "FY2019": 41935, "FY2018": 64550, "FY2017": 44596, "FY2016": 49858, "FY2015": 56214, "FY2014": 33331, "FY2013": 41617, "FY2012": 32708, "FY2011": -23864, "FY2010": 19615, "FY2009": 16631, "FY2008": 4574}),
    ("DATA", "Depreciation and amortisation of plant and equipment and intangible assets", {"FY2025": 2031, "FY2024": 1644, "FY2023": 1624, "FY2022": 1733, "FY2021": 2039, "FY2020": 2601, "FY2019": 2599, "FY2018": 744, "FY2017": 839, "FY2016": 1062, "FY2015": 1111, "FY2014": 988, "FY2013": 908, "FY2012": 694, "FY2011": 667, "FY2010": 677, "FY2009": 602, "FY2008": 376}),
    ("DATA", "Net (credit)/loss for expected credit losses", {"FY2025": -297, "FY2024": -3958, "FY2023": -11237, "FY2022": -11526, "FY2021": 23665, "FY2020": 3172, "FY2019": 377, "FY2018": -458, "FY2017": -187, "FY2016": 527, "FY2015": -155, "FY2014": 722, "FY2013": 60, "FY2012": 5223, "FY2011": 7167, "FY2010": -115, "FY2009": 5033, "FY2008": 421}),
    ("DATA", "Net impairment (profit)/loss on investment securities", {"FY2012": -768, "FY2011": 1105, "FY2010": 150, "FY2009": -3206, "FY2008": 8965}),
    ("DATA", "Impairment of investment in subsidiary (non-cash addback)", {"FY2011": 31432, "FY2010": 8432}),
    ("DATA", "(Gain)/loss on disposal of subsidiary (non-cash addback)", {"FY2012": 1074}),
    ("DATA", "Interest receivable from financial investments", {"FY2020": 13, "FY2019": 93, "FY2018": 0, "FY2017": -692, "FY2016": -1216, "FY2015": -1134, "FY2014": -654, "FY2013": -1294, "FY2012": -2279, "FY2011": -3425, "FY2010": -6117, "FY2009": -9761, "FY2008": -17202}),
    ("DATA", "Other interest receivable (from loans and advances)", {"FY2020": -40326, "FY2019": -46357, "FY2018": -41792, "FY2017": -38599, "FY2016": -33375, "FY2015": -24511, "FY2014": -25428, "FY2013": -17430, "FY2012": -12243, "FY2011": -9531, "FY2010": -10065, "FY2009": -10861, "FY2008": -36869}),
    ("DATA", "Interest payable (non-cash addback)", {"FY2019": 9313, "FY2018": 6553, "FY2017": 5788, "FY2016": 4629, "FY2015": 3095, "FY2014": 3635, "FY2013": 2800, "FY2012": 2828, "FY2011": 2828, "FY2010": 3858, "FY2009": 7677, "FY2008": 35584}),
    ("DATA", "(Gain)/loss on disposal of fixed assets", {"FY2018": -1, "FY2017": 1, "FY2014": 3, "FY2011": 6}),
    ("DATA", "Loss on disposal of intangible assets", {"FY2012": 4}),
    ("DATA", "Net loss on sale of available-for-sale investments / debt securities", {"FY2017": 45, "FY2014": 3, "FY2013": 436, "FY2012": 23, "FY2011": 1298, "FY2010": 190}),
    ("DATA", "Net (profit) on sale of available-for-sale investments", {"FY2009": -569, "FY2008": -2657}),
    ("DATA", "Amortisation of premiums on debt instruments at amortised cost / held-to-maturity investments", {"FY2018": 116, "FY2017": 96, "FY2009": 35, "FY2008": 162}),
    ("DATA", "Other income receivable", {"FY2017": -504}),
    ("DATA", "Fee income receivable", {"FY2020": 283}),
    ("DATA", "Exchange rate movements on plant and equipment", {"FY2021": -1, "FY2020": -79}),
    ("DATA", "Exchange rate movements on equity", {"FY2023": -1, "FY2022": 12, "FY2021": 135, "FY2020": -59}),
    ("DATA", "Exchange-rate movements on available-for-sale investments", {"FY2016": -4958, "FY2015": 704, "FY2014": 1721, "FY2013": -487, "FY2012": 4642, "FY2011": 489, "FY2010": 797, "FY2009": 23990, "FY2008": -59563}),
    ("DATA", "Other exchange-rate movements", {"FY2009": 2301}),
    ("DATA", "Net fair value (gain)/loss on financial instruments", {"FY2025": -1895, "FY2024": -1310, "FY2023": -7446, "FY2022": 10358, "FY2021": 2656}),
    ("SECTION", "Changes in operating assets and liabilities", {}),
    ("DATA", "Change in derivative financial instruments assets", {"FY2025": 2163, "FY2024": 839, "FY2023": 2196, "FY2022": -7691, "FY2021": -8, "FY2020": -43549, "FY2019": -3270, "FY2018": 372, "FY2017": 2860, "FY2016": 3596, "FY2015": 8000, "FY2014": 25329, "FY2013": -39553, "FY2009": 4179, "FY2008": -5554}),
    ("DATA", "Change in derivatives held for risk management (FY2010-FY2012 presentation)", {"FY2012": -2858, "FY2011": -1107, "FY2010": 1060}),
    ("DATA", "Change in loans and advances to banks", {"FY2022": 39708, "FY2021": 41381, "FY2020": -25199, "FY2019": -23856, "FY2018": 22315, "FY2017": -59436, "FY2016": 37836, "FY2015": 144643, "FY2014": -38459, "FY2013": -120119, "FY2012": -35913, "FY2011": -48, "FY2010": 24116, "FY2009": 30339, "FY2008": -67272}),
    ("DATA", "Change in loans and advances to customers", {"FY2025": 130992, "FY2024": 53197, "FY2023": 142977, "FY2022": 83721, "FY2021": -79736, "FY2020": -77438, "FY2019": -20154, "FY2018": -31910, "FY2017": 105429, "FY2016": -348920, "FY2015": -88564, "FY2014": -141927, "FY2013": -116611, "FY2012": -178951, "FY2011": -83295, "FY2010": 290235, "FY2009": 41372, "FY2008": -551569}),
    ("DATA", "Change in financial assets at amortised cost/fair value", {"FY2025": -39251, "FY2024": 16787, "FY2023": 20515, "FY2022": -6213, "FY2021": 10167, "FY2020": 6877, "FY2019": -4241, "FY2018": -30262}),
    ("DATA", "Change in financial assets at amortised cost - Government bonds", {"FY2025": 2147}),
    ("DATA", "Change in other assets", {"FY2025": -18315, "FY2024": -7665, "FY2023": 221384, "FY2022": -264099, "FY2021": -9099, "FY2020": -20489, "FY2019": -57250, "FY2018": 2055, "FY2017": 574, "FY2016": 20998, "FY2015": 1918, "FY2014": 38117, "FY2013": -1637, "FY2012": -27419, "FY2011": 792, "FY2010": -9397, "FY2009": -10407, "FY2008": -16295}),
    ("DATA", "Change in derivative financial instruments liabilities", {"FY2025": 287, "FY2024": 1, "FY2023": -10, "FY2022": -5267, "FY2021": -3484, "FY2020": 48153, "FY2019": 6794, "FY2018": 1720, "FY2017": -3893, "FY2016": -7355, "FY2015": -9984, "FY2014": -21016, "FY2013": 39070, "FY2009": 376, "FY2008": 5390}),
    ("DATA", "Change in deposits from banks", {"FY2025": 18705, "FY2024": 123666, "FY2023": -169797, "FY2022": 143133, "FY2021": 176876, "FY2020": 90788, "FY2019": 25671, "FY2018": -20203, "FY2017": -41727, "FY2016": 28113, "FY2015": 96466, "FY2014": -31862, "FY2013": 9748, "FY2012": -140301, "FY2011": 26254, "FY2010": -201627, "FY2009": -191170, "FY2008": 560116}),
    ("DATA", "Change in deposits from customers", {"FY2025": -50713, "FY2024": 132461, "FY2023": -68081, "FY2022": -42374, "FY2021": 117876, "FY2020": 83454, "FY2019": 24754, "FY2018": 88432, "FY2017": 36646, "FY2016": 244637, "FY2015": -28175, "FY2014": 228200, "FY2013": 139460, "FY2012": 46063, "FY2011": 55887, "FY2010": -81930, "FY2009": 87930, "FY2008": 290289}),
    ("DATA", "Change in other liabilities and provisions", {"FY2025": -2001, "FY2024": 7855, "FY2023": -4681, "FY2022": 8883, "FY2021": 1456, "FY2020": -6246, "FY2019": 22251, "FY2018": -793, "FY2017": 6672, "FY2016": -3584, "FY2015": -466, "FY2014": -5499, "FY2013": 3226, "FY2012": 5651, "FY2011": 1174, "FY2010": 1724, "FY2009": 3438, "FY2008": 11254}),
    ("DATA", "Interest and coupon received (operating, FY2008-FY2020 presentation)", {"FY2020": 40314, "FY2019": 45600, "FY2018": 40643, "FY2017": 37848, "FY2016": 34582, "FY2015": 25736, "FY2014": 28126, "FY2013": 18671, "FY2012": 14354, "FY2011": 16421, "FY2010": 15426, "FY2009": 25680, "FY2008": 43862}),
    ("DATA", "Dividend paid (operating activities, FY2008-FY2020 presentation)", {"FY2020": 0, "FY2019": -51118, "FY2018": -31606, "FY2017": -35690, "FY2016": -45450, "FY2015": -25955, "FY2014": -31873}),
    ("DATA", "Interest paid (operating activities, FY2008-FY2020 presentation)", {"FY2020": -7121, "FY2019": -9313, "FY2018": -4522, "FY2017": -7487, "FY2016": -4527, "FY2015": -2994, "FY2014": -3895, "FY2013": -2461, "FY2012": -3418, "FY2011": -2451, "FY2010": -3810, "FY2009": -10244, "FY2008": -32258}),
    ("DATA", "Income taxes paid", {"FY2025": -22969, "FY2024": -26070, "FY2023": -32346, "FY2022": -18955, "FY2021": -18895, "FY2020": -8430, "FY2019": -13293, "FY2018": -13859, "FY2017": -16749, "FY2016": -7780, "FY2015": -10695, "FY2014": -6670, "FY2013": -10980, "FY2012": -3729, "FY2011": -11131, "FY2010": -5059, "FY2008": -1815}),
    ("TOTAL", "Net cash generated from operating activities", {"FY2025": 111252, "FY2024": 405091, "FY2023": 233292, "FY2022": 22570, "FY2021": 304294, "FY2020": 100905, "FY2019": -49465, "FY2018": 52094, "FY2017": 36430, "FY2016": -31327, "FY2015": 145254, "FY2014": 52892, "FY2013": -54577, "FY2012": -294615, "FY2011": 10668, "FY2010": 48160, "FY2009": 13365, "FY2008": 169939}),
    ("SECTION", "Cash flows from investing activities", {}),
    ("DATA", "Acquisition of government bonds", {"FY2025": -78477, "FY2024": -36107, "FY2023": -74108, "FY2022": -44264}),
    ("DATA", "Proceeds from government bonds", {"FY2025": 78289, "FY2024": 11775}),
    ("DATA", "Acquisition of investment securities", {"FY2017": -106425, "FY2016": -8, "FY2014": -26932, "FY2008": -471210}),
    ("DATA", "Proceeds from sale of investment securities", {"FY2014": 15590, "FY2013": 16739, "FY2012": 47505, "FY2011": 50279, "FY2010": 101235, "FY2009": 77230, "FY2008": 176536}),
    ("DATA", "Proceeds from maturity of investment securities", {"FY2020": 50000, "FY2019": 50000, "FY2017": 40708}),
    ("DATA", "Proceeds from the issue of ordinary shares (investing, FY2012 presentation)", {"FY2012": 110000}),
    ("DATA", "Investment in subsidiaries/group companies", {"FY2012": 62210, "FY2010": -61911, "FY2008": -32128}),
    ("DATA", "Acquisition of property, plant and equipment", {"FY2025": -2120, "FY2024": -1086, "FY2023": -745, "FY2022": -3086, "FY2021": -1349, "FY2020": -519, "FY2019": -870, "FY2018": -318, "FY2017": -668, "FY2016": -681, "FY2015": -1089, "FY2014": -489, "FY2013": -565, "FY2012": -3247, "FY2011": -275, "FY2010": -102, "FY2009": -150, "FY2008": -2663}),
    ("DATA", "Acquisition of intangible assets", {"FY2025": -412, "FY2024": -435, "FY2023": -83, "FY2022": -183, "FY2021": -86, "FY2020": -52, "FY2019": -398, "FY2018": -419, "FY2017": -18, "FY2016": -86, "FY2014": -426, "FY2012": -52, "FY2011": -6, "FY2010": -39, "FY2009": -225, "FY2008": -405}),
    ("DATA", "Proceeds from disposal of property, plant and equipment", {"FY2025": 97, "FY2024": 27, "FY2023": 40, "FY2022": 22, "FY2021": 272, "FY2020": 82}),
    ("DATA", "Proceeds from disposal of intangible assets", {"FY2021": 16}),
    ("TOTAL", "Net cash from/(used in) investing activities", {"FY2025": -2623, "FY2024": -25826, "FY2023": -74896, "FY2022": -47511, "FY2021": -1147, "FY2020": 49511, "FY2019": 48732, "FY2018": -737, "FY2017": -66403, "FY2016": -775, "FY2015": -1089, "FY2014": -12257, "FY2013": 16174, "FY2012": 216416, "FY2011": 49998, "FY2010": 39183, "FY2009": 76855, "FY2008": -329870}),
    ("SECTION", "Cash flows from financing activities", {}),
    ("DATA", "Repayment of subordinated debt", {"FY2022": -60000}),
    ("DATA", "Issuance of Additional Tier 1 instrument", {"FY2022": 60000}),
    ("DATA", "Dividend paid", {"FY2025": -78700, "FY2024": -98100, "FY2023": -66800, "FY2022": -33459, "FY2021": -67000}),
    ("DATA", "Interest paid on Additional Tier 1 instrument", {"FY2025": -4962, "FY2024": -5362, "FY2023": -5015}),
    ("DATA", "Repayment of principal portion of lease liabilities", {"FY2025": -722, "FY2024": -491, "FY2023": -47, "FY2022": -77, "FY2021": -1393, "FY2020": -1578}),
    ("DATA", "Repayment of interest portion of lease liabilities", {"FY2025": 298}),
    ("TOTAL", "Net cash used in financing activities", {"FY2025": -84086, "FY2024": -103953, "FY2023": -71862, "FY2022": -33536, "FY2021": -68393, "FY2020": -1578, "FY2019": 0, "FY2018": 0, "FY2017": 0, "FY2016": 0, "FY2015": 0, "FY2014": 0, "FY2013": 0, "FY2012": 0, "FY2011": 0, "FY2010": 0, "FY2009": 0, "FY2008": 0}),
    ("TOTAL", "Net increase/(decrease) in cash and cash equivalents", {"FY2025": 24543, "FY2024": 275312, "FY2023": 86534, "FY2022": -58477, "FY2021": 234754, "FY2020": 148837, "FY2019": -733, "FY2018": 51357, "FY2017": -29973, "FY2016": -32102, "FY2015": 144165, "FY2014": 40635, "FY2013": -38403, "FY2012": -78199, "FY2011": 60666, "FY2010": 87343, "FY2009": 90220, "FY2008": -159931}),
    ("DATA", "Current/prior year reclassification adjustments", {"FY2018": -26}),
    ("DATA", "Effects of exchange-rate changes on cash and cash equivalents", {"FY2009": -2477}),
    ("DATA", "Cash and cash equivalents at beginning of period", {"FY2025": 1048859, "FY2024": 773547, "FY2023": 687013, "FY2022": 716133, "FY2021": 481379, "FY2020": 332542, "FY2019": 333275, "FY2018": 281944, "FY2017": 311917, "FY2016": 344019, "FY2015": 199854, "FY2014": 159219, "FY2013": 197622, "FY2012": 275821, "FY2011": 215155, "FY2010": 127812, "FY2009": 40069, "FY2008": 200000}),
    ("TOTAL", "Cash and cash equivalents at end of period", {"FY2025": 1073402, "FY2024": 1048859, "FY2023": 773547, "FY2022": 657656, "FY2021": 716133, "FY2020": 481379, "FY2019": 332542, "FY2018": 333275, "FY2017": 281944, "FY2016": 311917, "FY2015": 344019, "FY2014": 199854, "FY2013": 159219, "FY2012": 197622, "FY2011": 275821, "FY2010": 215155, "FY2009": 127812, "FY2008": 40069}),
]

bw.add_cash_flow_sheet(
    title="Bank of China (UK) Limited — Statement of Cash Flows",
    subtitle="Bank of China (UK) Limited (solo entity basis), £'000",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=72,
    source_height=210,
    unit_suffix=" (£'000)",
    years=YEARS,
)

# ---------------------------------------------------------------
# Sheet: Asset Quality
# ---------------------------------------------------------------
asset_quality_rows = [
    ("SECTION", "Gross carrying amount by product", {}),
    ("DATA", "Wholesale loans", {"FY2025": 2162, "FY2024": 2242, "FY2023": 2352, "FY2022": 2535, "FY2021": 4806, "FY2020": 4987, "FY2019": 2629, "FY2018": 5222}),
    ("DATA", "Housing loans", {"FY2025": 895, "FY2024": 1117, "FY2023": 2279, "FY2022": 2417, "FY2021": 2607, "FY2020": 3398, "FY2019": 4519, "FY2018": 5894}),
    ("DATA", "Syndicated loans", {"FY2025": 194775, "FY2024": 238983, "FY2023": 173584, "FY2022": 155931, "FY2021": 183604, "FY2020": 215270, "FY2019": 229152, "FY2018": 263321}),
    ("DATA", "Factoring financing", {"FY2025": 1898, "FY2024": 2185, "FY2023": 4840, "FY2022": 4219, "FY2021": 7892, "FY2020": 4097, "FY2019": 686, "FY2018": 1043}),
    ("DATA", "Overdraft corporate accounts", {"FY2020": 1, "FY2019": 1, "FY2018": 258}),
    ("DATA", "Overdraft personal accounts", {"FY2019": 2, "FY2018": 2}),
    ("DATA", "Credit cards", {"FY2025": 343, "FY2024": 382, "FY2023": 501, "FY2022": 401, "FY2021": 449, "FY2020": 460, "FY2019": 778, "FY2018": 784}),
    ("DATA", "Mortgage loans", {"FY2025": 611782, "FY2024": 697619, "FY2023": 812348, "FY2022": 973424, "FY2021": 1035418, "FY2020": 913853, "FY2019": 827596, "FY2018": 767860}),
    ("DATA", "Financing order", {"FY2024": 319, "FY2023": 140, "FY2022": 92, "FY2021": 1960, "FY2020": 655, "FY2019": 93, "FY2018": 1009}),
    ("TOTAL", "Total gross carrying amount", {"FY2025": 811855, "FY2024": 942847, "FY2023": 996044, "FY2022": 1139019, "FY2021": 1236736, "FY2020": 1142721, "FY2019": 1065456, "FY2018": 1045393}),
    ("SECTION", "Gross carrying amount by IFRS 9 stage", {}),
    ("DATA", "Stage 1: 12-month ECL", {"FY2025": 755256, "FY2024": 838850, "FY2023": 875144, "FY2022": 932381, "FY2021": 1161138, "FY2020": 1502398, "FY2019": 1429872, "FY2018": 1136718}),
    ("DATA", "Stage 2: Lifetime ECL, not credit-impaired", {"FY2025": 52230, "FY2024": 99518, "FY2023": 117365, "FY2022": 133805, "FY2021": 23529, "FY2020": 143650, "FY2019": 22324, "FY2018": 29296}),
    ("DATA", "Stage 3: Lifetime ECL, credit-impaired", {"FY2025": 4369, "FY2024": 4479, "FY2023": 3535, "FY2022": 72833, "FY2021": 52069, "FY2020": 3939, "FY2019": 1776, "FY2018": 686}),
    ("TOTAL", "Total gross carrying amount (by stage)", {"FY2025": 811855, "FY2024": 942847, "FY2023": 996044, "FY2022": 1139019, "FY2021": 1236736, "FY2020": 1649987, "FY2019": 1453972, "FY2018": 1166700}),
    ("SECTION", "Reconciliation to Balance Sheet", {}),
    ("DATA", "Net carrying value (Balance Sheet's Loans and advances to customers)", {"FY2025": 810985, "FY2024": 941507, "FY2023": 990763, "FY2022": 1122459, "FY2021": 1194653, "FY2020": 1138583, "FY2019": 1064347, "FY2018": 1044570}),
    ("DATA", "Implied total ECL allowance (gross − net)", {"FY2025": 870, "FY2024": 1340, "FY2023": 5281, "FY2022": 16560, "FY2021": 42083, "FY2020": 4138, "FY2019": 1109, "FY2018": 823}),
    ("SECTION", "Asset quality ratios", {}),
    ("DATA", "ECL coverage ratio (implied allowance / gross carrying amount)", {"FY2025": "0.11%", "FY2024": "0.14%", "FY2023": "0.53%", "FY2022": "1.45%", "FY2021": "3.40%", "FY2020": "0.36%", "FY2019": "0.10%", "FY2018": "0.08%"}),
    ("DATA", "Stage 3 / NPL ratio (Stage 3 gross / total gross carrying amount)", {"FY2025": "0.54%", "FY2024": "0.48%", "FY2023": "0.35%", "FY2022": "6.39%", "FY2021": "4.21%", "FY2020": "0.24%", "FY2019": "0.12%", "FY2018": "0.06%"}),
    ("SECTION", "Loans and advances to customers - credit quality (IAS 39, pre-IFRS 9, FY2014-FY2017)", {}),
    ("DATA", "Gross exposure", {"FY2017": 1055142, "FY2016": 1160589, "FY2015": 811185, "FY2014": 722717}),
    ("DATA", "Allowance for impairment", {"FY2017": -688, "FY2016": -893, "FY2015": -409, "FY2014": -410}),
    ("TOTAL", "Carrying amount", {"FY2017": 1054454, "FY2016": 1159696, "FY2015": 810776, "FY2014": 722307}),
    ("DATA", "Individually impaired (gross)", {"FY2017": 1, "FY2016": 3, "FY2015": 33, "FY2014": 5}),
    ("DATA", "Neither past due nor impaired", {"FY2017": 1041377, "FY2016": 1147306, "FY2015": 800575, "FY2014": 710358}),
    ("DATA", "Past due but not impaired", {"FY2017": 13077, "FY2016": 12390, "FY2015": 10201, "FY2014": 11949}),
    ("SECTION", "Credit quality categories (IAS 39, pre-IFRS 9, FY2014-FY2017)", {}),
    ("DATA", "Performing", {"FY2017": 1013454, "FY2016": 1110954}),
    ("DATA", "Special mention (unrated)", {"FY2017": 40645, "FY2016": 46426, "FY2015": 26740, "FY2014": 17106}),
    ("DATA", "Substandard (unrated)", {"FY2016": 2209, "FY2014": 740}),
    ("DATA", "Loss (unrated)", {"FY2016": 108}),
    ("SECTION", "Asset quality ratios (IAS 39 basis, FY2014-FY2017)", {}),
    ("DATA", "Individually impaired ratio (individually impaired / gross exposure)", {"FY2017": "0.00%", "FY2016": "0.00%", "FY2015": "0.00%", "FY2014": "0.00%"}),
    ("DATA", "Special mention ratio (special mention / gross exposure)", {"FY2017": "3.85%", "FY2016": "4.00%", "FY2015": "3.30%", "FY2014": "2.37%"}),
]

ASSET_QUALITY_SOURCES = (
    "Sources - Note 6(a) 'Analysis of risk concentration in the financial position' (Global/Europe/US/UK/UK "
    "Retail x Stage 1/2/3 geographic table), Bank/solo basis, £'000. By-product figures here are summed from "
    "that table's 'Loans and advances to customers' product rows (Wholesale/Housing/Syndicated/Factoring/"
    "Overdraft/Credit Cards/Mortgage/Financing Order) across all geography columns:\n"
    f"FY2025: Annual Report 2025, p.77 - {AR2025_URL}\n"
    f"FY2024: Annual Report 2025's own FY2024 comparative column, p.78 (figures independently cross-checked "
    "against AR2024's own Balance Sheet net-loans figure) - {AR2025_URL}\n"
    f"FY2023: Annual Report 2023, p.80 - {AR2023_URL}\n"
    f"FY2022: Annual Report 2023's own FY2022 comparative column, p.81 - {AR2023_URL}\n"
    f"FY2021: Financial Statements 2021, p.67 - {AR2021_URL}\n"
    f"FY2020: Financial Statements 2020, note 6(a)(x) 'Analysis of risk concentration', p.61-62 - {AR2020_URL}\n"
    f"FY2019: Financial Statements 2019, note 6(a)(x), p.62-63 (own-year table; FY2018 by-product Totals taken "
    "from this same table's own FY2018 comparative column since FY2018's own report's equivalent table has "
    "unreliable OCR alignment) - {AR2019_URL}\n"
    f"FY2018 by-stage totals: Financial Statements 2018, note 6(a)(xii) 'Impairment allowance analysis', p.54 "
    "- {AR2018_URL}\n"
    f"FY2019/FY2020 by-stage totals: Financial Statements 2019/2020, note 6(a)(xi)/(xii) 'Impairment allowance "
    "analysis' - {AR2019_URL}, {AR2020_URL}\n"
    "'Implied total ECL allowance' is not separately disclosed by product/stage anywhere in these documents - it "
    "is the residual gap between the by-product gross carrying total and the Balance Sheet's own net carrying "
    "value, so it captures the whole-portfolio allowance only (not split by stage), hence no separate Stage 3 "
    "coverage ratio is shown here (would require a stage-level allowance split that isn't disclosed). FY2021's "
    "large ECL gap (£42,083k, 3.40% coverage) is consistent with that year's Cash Flow Statement, which shows "
    "the largest single-year 'Net loss for expected credit losses' charge (£23,665k) in the whole 5-year series. "
    "FY2022's elevated Stage 3/NPL ratio (6.39%, mostly Syndicated loans) fell sharply by FY2023 (0.35%) - both "
    "years' own source tables, not smoothed or averaged. "
    "Scope caveat for FY2018-FY2020: unlike FY2021-2025 (where the by-product and by-stage groupings tie exactly "
    "to each other, both restricted to customer loans only), the FY2018-FY2020 by-stage totals are the note's "
    "broader 'On Balance Sheet' Impairment allowance analysis figures, which also include cash balances and debt "
    "instruments at amortised cost alongside customer loans - they do NOT tie to the by-product (loans-only) "
    "total for these three years (e.g. FY2020: £1,649,987k by-stage vs £1,142,721k by-product), because a clean "
    "stage-level split restricted to customer loans only could not be reliably read off the geography-table's "
    "column layout in these three PDFs' extracted text. The FY2018-FY2020 Stage 3/NPL ratio is therefore computed "
    "against the broader by-stage total, not the narrower by-product total used FY2021 onward - not directly "
    "comparable across that boundary, shown as each year's own disclosed figures rather than force-aligned.\n"
    "FY2014-FY2017 pre-IFRS 9 section: the Bank's own 'Loans and advances to customers' credit-risk note used "
    "IAS 39's incurred-loss classification (gross exposure/individually impaired/past due but not "
    "impaired/neither past due nor impaired, plus an internal-rating-based Performing/Special mention/"
    "Substandard/Doubtful/Loss category split) before the 1 January 2018 IFRS 9 transition replaced it with the "
    "Stage 1/2/3 model used from FY2018 onward - shown here as its own section rather than force-mapped onto the "
    "IFRS 9 rows above, per the same regime-change convention used elsewhere in this project:\n"
    f"FY2017: Financial Statements 2017, p.39-40 - {AR2017_URL}\n"
    f"FY2016: Financial Statements 2016, p.33-34 - {AR2016_URL}\n"
    f"FY2015: Financial Statements 2015, p.32-33 - {AR2015_URL}\n"
    f"FY2014: Financial Statements 2015's own FY2014 comparative, p.32-33 - {AR2015_URL} ({AR2014_SCAN_NOTE})\n"
    "'Performing' is left blank for FY2014/FY2015 where the source table's OCR text was too garbled to read "
    "reliably (rather than transcribe a guessed figure); 'Individually impaired' is negligible in all four years "
    "under IAS 39's incurred-loss model (rounds to 0.00% of gross exposure every year) - 'Special mention "
    "(unrated)', an internal early-warning watchlist category, is shown alongside it as a more informative "
    "leading indicator of the period's credit quality.\n"
    + ENTITY_NOTE
)

bw.add_asset_quality_sheet(
    title="Bank of China (UK) Limited — Asset Quality / Credit Risk Disclosures",
    subtitle="Bank of China (UK) Limited (solo entity basis), £'000 (ratios as calculated)",
    rows=asset_quality_rows,
    sources_text=ASSET_QUALITY_SOURCES,
    first_col_width=68,
    source_height=430,
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, f"{unit}" if unit else None,
                         rows_data, sources_text, note=note, first_col_width=46, source_height=170)


# ---------------------------------------------------------------
# KM1 Key Metrics - the Bank's own table, headed "UK KM1 - Key Metrics",
# reproduced exactly as printed. Four things about this bank's version:
#
#   1. IT IS THE BASEL/BCBS KM1 ROW SET UNDER A UK KM1 HEADING. Despite the
#      "UK KM1" title, rows 8-11 are the BCBS buffer block ("Capital
#      conservation buffer requirement", "Countercyclical buffer
#      requirement", "Bank G-SIB and/or D-SIB additional requirements",
#      "Total of bank CET1 specific buffer requirements") and rows 13-14 are
#      captioned "Basel III leverage ratio exposure measure"/"Basel III
#      leverage ratio". The PRA template's UK 7a-7d, UK 8a, UK 9a, UK 10a,
#      UK 11a and UK 16a/16b rows appear in NO edition. The bank's row set is
#      reproduced; the PRA rows are not added back as blanks, because this
#      bank's table does not contain them.
#
#   2. ROW 16 IS PRINTED AS "6" IN EVERY EDITION. "6 Total net cash outflow"
#      sits between rows 15 and 17 in the FY2022, FY2023, FY2024 and FY2025
#      documents alike - a persistent typo in the Bank's own template, not an
#      extraction artefact (it was checked in all four). Reproduced as
#      printed and flagged in the citation, per the map's rule 7 (record a
#      source defect, do not correct it).
#
#   3. ROW 12'S CAPTION AND BASIS CHANGED IN THE FY2025 EDITION, from "CET1
#      available after meeting the bank's minimum Cap Req (%)" to "CET1
#      available after meeting the total SREP own funds requirements (%)",
#      and the FY2024 figure was restated with it: 20.3% as its own edition
#      printed it, 19.5% as the FY2025 edition's comparative restates it.
#      Per the map's rule 1 the cell carries each year's OWN edition, so
#      FY2024 shows 20.3%; the restatement is recorded in the citation. This
#      is the only row in the whole table where the editions disagree.
#
#   4. ROW 10 PRINTS "0%", NOT A DASH, in every year. That is a measured
#      zero (the Bank is neither a G-SIB nor a D-SIB and the requirement is
#      nil), so the zero is kept rather than blanked.
#
# FY2020 and earlier are blank: the FY2021 document and every edition before
# it predate the KM1 template and are narrative/ratio-only. The pre-KM1
# figures those documents do carry are on the individual metric sheets below.
# ---------------------------------------------------------------
km1_rows = [
    ("SECTION", "Available capital (£'000)", {}),
    ("DATA", "1    Common equity tier 1 capital (CET1)",
     {"FY2025": 274521, "FY2024": 274294, "FY2023": 275056, "FY2022": 275000, "FY2021": 275164}),
    ("DATA", "2    Tier 1 capital",
     {"FY2025": 334521, "FY2024": 334294, "FY2023": 335056, "FY2022": 335000, "FY2021": 275164}),
    ("DATA", "3    Total regulatory capital",
     {"FY2025": 334521, "FY2024": 334294, "FY2023": 335056, "FY2022": 335000, "FY2021": 335164}),
    ("SECTION", "Risk-weighted assets ('RWAs') (£'000)", {}),
    ("DATA", "4    Total risk-weighted assets (RWA)",
     {"FY2025": 1008110, "FY2024": 1106898, "FY2023": 1024452, "FY2022": 1176625, "FY2021": 1119380}),
    ("SECTION", "Risk-based capital ratios as a percentage of RWA (%)", {}),
    ("DATA", "5    Common Equity Tier 1 ratio (%)",
     {"FY2025": "27.2%", "FY2024": "24.8%", "FY2023": "26.8%", "FY2022": "23.4%", "FY2021": "24.6%"}),
    ("DATA", "6    Tier 1 ratio (%)",
     {"FY2025": "33.2%", "FY2024": "30.2%", "FY2023": "32.7%", "FY2022": "28.5%", "FY2021": "24.6%"}),
    ("DATA", "7    Total capital ratio (%)",
     {"FY2025": "33.2%", "FY2024": "30.2%", "FY2023": "32.7%", "FY2022": "28.5%", "FY2021": "29.9%"}),
    ("SECTION", "Additional CET1 buffer requirements as a percentage of RWA (%)", {}),
    ("DATA", "8    Capital conservation buffer requirement (%)",
     {"FY2025": "2.5%", "FY2024": "2.5%", "FY2023": "2.5%", "FY2022": "2.5%", "FY2021": "2.5%"}),
    ("DATA", "9    Countercyclical buffer requirement (%)",
     {"FY2025": "0.3%", "FY2024": "0.4%", "FY2023": "0.5%", "FY2022": "0.3%", "FY2021": "0.1%"}),
    ("DATA", "10    Bank G-SIB and/or D-SIB additional requirements (%)",
     {"FY2025": "0%", "FY2024": "0%", "FY2023": "0%", "FY2022": "0%", "FY2021": "0%"}),
    ("DATA", "11    Total of bank CET1 specific buffer requirements (%)",
     {"FY2025": "2.8%", "FY2024": "2.9%", "FY2023": "3.0%", "FY2022": "2.8%", "FY2021": "2.6%"}),
    ("DATA", "12    CET1 available after meeting the total SREP own funds requirements (%)",
     {"FY2025": "21.9%", "FY2024": "20.3%", "FY2023": "22.3%", "FY2022": "18.9%", "FY2021": "20.1%"}),
    ("SECTION", "Basel III leverage Ratio", {}),
    ("DATA", "13    Total Basel III leverage ratio exposure measure (£'000)",
     {"FY2025": 1373968, "FY2024": 1462346, "FY2023": 1473437, "FY2022": 1814024, "FY2021": 2431869}),
    ("DATA", "14    Basel III leverage ratio (%)",
     {"FY2025": "24.4%", "FY2024": "22.9%", "FY2023": "22.7%", "FY2022": "18.5%", "FY2021": "11.3%"}),
    ("SECTION", "Liquidity Coverage Ratio (£'000 / %)", {}),
    ("DATA", "15    Total HQLA",
     {"FY2025": 1007375, "FY2024": 1014087, "FY2023": 677646, "FY2022": 545654, "FY2021": 527697}),
    ("DATA", "6    Total net cash outflow   [printed \"6\" by the Bank; this is template row 16]",
     {"FY2025": 310866, "FY2024": 272240, "FY2023": 174967, "FY2022": 299877, "FY2021": 294774}),
    ("DATA", "17    LCR ratio (%)",
     {"FY2025": "324.1%", "FY2024": "372.5%", "FY2023": "387.3%", "FY2022": "182.0%", "FY2021": "179.0%"}),
    ("SECTION", "Net Stable Funding Ratio (£'000 / %)", {}),
    ("DATA", "18    Total available stable funding",
     {"FY2025": 1389486, "FY2024": 1630136, "FY2023": 1289845, "FY2022": 1463448, "FY2021": 1438026}),
    ("DATA", "19    Total required stable funding",
     {"FY2025": 714820, "FY2024": 752941, "FY2023": 959234, "FY2022": 1209361, "FY2021": 950742}),
    ("DATA", "20    NSFR ratio (%)",
     {"FY2025": "194.4%", "FY2024": "216.5%", "FY2023": "134.5%", "FY2022": "121.0%", "FY2021": "151.3%"}),
]

KM1_SOURCES = p3_sources() + (
    "\nKM1 presentation notes:\n"
    "• LATEST-EDITION CHECK 2026-09-16: the Bank's own disclosure index at "
    "https://www.bankofchina.com/uk/aboutus/ab5/ lists 'Pillar 3 Disclosure 31 December 2025' as its newest "
    "document, which is the one cited above. Checked, none newer.\n"
    "• A BASEL ROW SET UNDER A UK KM1 HEADING. The table is headed 'UK KM1 - Key Metrics' (FY2022's edition: "
    "'UK KM1 - Key metrics template'), but rows 8-11 are the BCBS buffer block and rows 13-14 are captioned "
    "'Basel III leverage ratio exposure measure' / 'Basel III leverage ratio'. The PRA template's UK 7a-7d, "
    "UK 8a, UK 9a, UK 10a, UK 11a and UK 16a/16b rows appear in no edition. This sheet reproduces the Bank's "
    "row set and does not add the PRA rows back as blanks, because the Bank's table does not contain them.\n"
    "• ROW 16 IS PRINTED AS '6'. '6 Total net cash outflow' sits between rows 15 and 17 in the FY2022, "
    "FY2023, FY2024 and FY2025 documents alike. It is a persistent typo in the Bank's own template, checked "
    "in all four editions, and is reproduced rather than corrected.\n"
    "• ROW 12 CHANGED BASIS AND CAPTION IN FY2025, from 'CET1 available after meeting the bank's minimum "
    "Cap Req (%)' to 'CET1 available after meeting the total SREP own funds requirements (%)'. The FY2025 "
    "edition restates FY2024 as 19.5% on the new basis; the FY2024 edition printed 20.3% on the old one. The "
    "cell here carries 20.3%, that year's own edition, per this project's rule that each year comes from its "
    "own edition rather than a later comparative. Both figures are the Bank's; they are not reconciled. Every "
    "other row agrees exactly across overlapping editions.\n"
    "• ROW 10 PRINTS '0%', NOT A DASH, in every year - a measured zero (the Bank is neither a G-SIB nor a "
    "D-SIB), so the zero is kept rather than blanked.\n"
    "• The FY2023 edition prints its own year-column header as '20232', where the trailing 2 is a footnote "
    "marker rather than part of the year.\n"
    "• FY2020 and earlier are blank. The FY2021 Pillar 3 document and every edition before it predate the "
    "KM1 template and are narrative/ratio-only; FY2021 above is the comparative column of the FY2022 "
    "edition, which is the first to print the template. Nothing has been back-filled from the pre-KM1 CRD IV "
    "tables - those figures are on the individual metric sheets, with their basis stated there."
)

bw.add_km1_sheet(
    title="Bank of China (UK) Limited — KM1 Key Metrics",
    subtitle="The Bank's own published table, headed 'UK KM1 - Key Metrics', reproduced in its row order with "
             "its own row numbers, captions and precision — including the Basel III buffer/leverage row set it "
             "uses in place of the PRA template's, and its own mis-numbering of row 16 as '6'. Amounts in "
             "£'000, ratios as printed. FY2020 and earlier predate the template and are intentionally blank.",
    rows=km1_rows,
    sources_text=KM1_SOURCES,
    source_height=300,
)


metric(
    "CET1 Capital", "£'000",
    [("Common Equity Tier 1 (CET1) capital", {"FY2025": 274521, "FY2024": 274294, "FY2023": 275056, "FY2022": 275000, "FY2021": 275164, "FY2020": 307058, "FY2019": 274958, "FY2018": 274958, "FY2017": 274958, "FY2016": 274958, "FY2015": 274958, "FY2014": 274958})],
    p3_sources(),
)

metric(
    "CET1 Ratio", "% of RWA",
    [("Common Equity Tier 1 ratio", {"FY2025": "27.2%", "FY2024": "24.8%", "FY2023": "26.8%", "FY2022": "23.4%", "FY2021": "24.6%", "FY2020": "26.7%", "FY2019": "27.8%", "FY2018": "29.2%", "FY2017": "30%", "FY2016": "27%", "FY2015": "31%", "FY2014": "34%"})],
    p3_sources(),
)

metric(
    "Tier 1 Capital", "£'000",
    [("Tier 1 capital", {"FY2025": 334521, "FY2024": 334294, "FY2023": 335056, "FY2022": 335000, "FY2021": 275164, "FY2020": 307058, "FY2019": 274958, "FY2018": 274958, "FY2017": 274958, "FY2016": 274958, "FY2015": 274958, "FY2014": 274958})],
    p3_sources(),
    note="Equal to CET1 capital every year FY2014-FY2021 (no AT1 instruments in issue until June 2022). A £60m "
         "Additional Tier 1 instrument was issued in June 2022, replacing an equal amount of Tier 2 subordinated "
         "debt.",
)

metric(
    "Tier 1 Ratio", "% of RWA",
    [("Tier 1 ratio", {"FY2025": "33.2%", "FY2024": "30.2%", "FY2023": "32.7%", "FY2022": "28.5%", "FY2021": "24.6%", "FY2020": "26.7%", "FY2019": "27.8%", "FY2018": "29.2%", "FY2017": "30%", "FY2016": "27%", "FY2015": "31%", "FY2014": "34%"})],
    p3_sources(),
    note="Numerically equal to the CET1 ratio every year FY2014-FY2021 since Tier 1 capital equalled CET1 capital "
         "exactly (no AT1 in issue until June 2022); each year's own Table 1/KM1 document states this explicitly "
         "as its own 'Tier 1 capital ratio' line, not just inferred.",
)

metric(
    "Total Capital", "£'000",
    [("Total regulatory capital", {"FY2025": 334521, "FY2024": 334294, "FY2023": 335056, "FY2022": 335000, "FY2021": 335164, "FY2020": 367058, "FY2019": 334958, "FY2018": 334958, "FY2017": 334958, "FY2016": 334958, "FY2015": 334958, "FY2014": 334958})],
    p3_sources(),
)

metric(
    "Total Capital Ratio", "% of RWA",
    [("Total capital ratio", {"FY2025": "33.2%", "FY2024": "30.2%", "FY2023": "32.7%", "FY2022": "28.5%", "FY2021": "29.9%", "FY2020": "31.9%", "FY2019": "33.9%", "FY2018": "35.6%", "FY2017": "36%", "FY2016": "33%", "FY2015": "37%", "FY2014": "42%"})],
    p3_sources(),
)

metric(
    "Total RWAs", "£'000",
    [("Total risk-weighted assets (RWA)", {"FY2025": 1008110, "FY2024": 1106898, "FY2023": 1024452, "FY2022": 1176625, "FY2021": 1119380, "FY2020": 1151516, "FY2019": 988901, "FY2018": 941052, "FY2017": 931206, "FY2016": 1003913, "FY2015": 895473, "FY2014": 800993})],
    p3_sources(),
    note="FY2016's own Table 1 states RWA as £1,003,913k; the FY2017 Pillar 3 document's own FY2016 comparative "
         "column shows a slightly different £1,002,116k (a ~£1.8k/0.2% difference, not explained in either "
         "document) - each year's own originally-published figure is used as the primary value throughout, per "
         "project convention.",
)

GA020_OV1_NOTE = (
    "\n\nFY2014-FY2018 BREAKDOWN FOUND 2026-09-19 (GA-020). These years previously read 'Not publicly "
    "disclosed - category breakdown'. That was wrong: each edition prints an 'Overview of RWA' table. "
    "Sources, each year's own edition, read from the page image: FY2018 - Pillar 3 Disclosures 2018, Table 6, "
    f"printed p.28 - {P3_2018_URL}; FY2017 - Pillar 3 Disclosures 2017, Table 3, printed p.13 - {P3_2017_URL}; "
    f"FY2016 - Capital and Risk Management Pillar 3 Disclosures 2016, Table 3, printed p.13 - {P3_2016_URL}; "
    f"FY2015 - Capital and Risk Management Pillar 3 Disclosures 2015, Table 3, printed p.12 - {P3_2015_URL}; "
    f"FY2014 - Pillar 3 Disclosures 2014, Table 3, printed p.11 - {P3_2014_URL}. "
    "ROW DEFINITIONS: FY2014-FY2016 print credit risk EXCLUDING CCR plus a separate CCR line (the same "
    "editions' Pillar 1 table labels that line 'Counterparty Credit Risk (including CVA)', so there is no "
    "separate CVA row for those years); FY2017 prints credit risk INCLUDING counterparty credit and dilution "
    "risks and free deliveries, plus a CVA line, so it has its own row; FY2018 returns to the "
    "excluding-CCR layout, printing a dash for CCR and a separate CVA line. "
    "SOURCE ARITHMETIC, recorded not corrected: FY2014's rows sum to 924,802 against the printed Total "
    "924,791 (an 11k gap inside the table); FY2017's sum to 931,205 against 931,206 (the FY2018 edition's "
    "comparative prints 931,205). FY2015, FY2016 and FY2018 foot exactly. "
    "FY2014 BASIS DIVERGENCE, recorded not reconciled: the SAME FY2014 edition prints TWO different 'RWA' "
    "figures - Table 1 'Total capital resources and risk asset ratios' gives 'Risk-weighted assets (RWA) "
    "800,993' (the figure carried on the Total RWAs sheet, and the denominator of its printed 34%/42% ratios), "
    "while Table 3 totals 924,791, and 800,993 is exactly Table 3's credit-risk-excluding-CCR line. This "
    "sheet's FY2014 Total is Table 3's printed total; the Total RWAs sheet keeps Table 1's figure. Neither "
    "is adjusted. FY2016: the FY2017 edition's comparative Total is 1,002,116 against the FY2016 edition's "
    "own 1,003,913 (already noted on the Total RWAs sheet); own-edition figures are used."
)

RWA_BREAKDOWN_SOURCES = (
    "Sources - Bank of China (UK) Limited's own UK OV1/EU OV1 'Overview of risk weighted exposure amounts' "
    "tables (same 5 Pillar 3 documents as the Total RWAs sheet), each year's own originally-published figures "
    "used as primary (not a later restated comparative), per project convention:\n"
    f"FY2025: Pillar 3 Disclosure 2025, Table 'UK OV1' - {P3_2025_URL}\n"
    f"FY2024: Pillar 3 Disclosure 2024, Table 'UK OV1' - {P3_2024_URL}\n"
    f"FY2023: Pillar 3 Disclosure 2023, Table 'UK OV1', p.15 - {P3_2023_URL}\n"
    f"FY2022: Pillar 3 Disclosure 2022, Table 'UK OV1', p.16 - {P3_2022_URL}\n"
    f"FY2021: Pillar 3 Disclosure 2021, Table 1 'Template EU OV1', p.14 - {P3_2021_URL}\n"
    f"FY2020 (own year) & FY2019 comparative: the FY2020 Pillar 3 document's own Table 9 'Overview of risk "
    f"weighted assets' (UK OV1 template), p.20-22 - {P3_2020_URL}\n\n"
    "CORRECTION (fresh re-verification, 2026-09-12): the prior version of this sheet claimed FY2021-FY2025 (and "
    "FY2014-FY2018) had no category-level breakdown disclosed. That was wrong for FY2021-FY2025 - every one of "
    "those 5 Pillar 3 documents was re-read directly and each contains a full OV1/EU OV1 table, with every "
    "year's Total tying exactly to the Total RWAs sheet's own figure. FY2014-FY2018 were not re-checked in this "
    "pass (out of scope - this re-verification targeted the last-5-years gap) and remain as previously "
    "documented pending a future check.\n"
    "TEMPLATE FORMAT CHANGE: FY2021's own document does not carry a separate 'Counterparty credit risk (CCR)' "
    "line (only Credit risk, CVA, Market risk, Operational risk) - the following year's own document's FY2021 "
    "comparative column DOES split out a CCR figure (£16,535k) with a correspondingly smaller credit-risk figure "
    "(£776,521k vs £793,055k as FY2021's own document states it, a difference of £16,534k), confirming the CCR "
    "amount was folded into the 'credit risk' line in FY2021's own original publication rather than omitted "
    "entirely. FY2021's own originally-published split is used here per project convention, with the later "
    "restatement noted rather than silently substituted. FY2022 onward carries CCR as its own explicit line "
    "every year."
    + GA020_OV1_NOTE
)

bw.add_rwa_breakdown_sheet(
    title="Bank of China (UK) Limited — RWA Breakdown",
    subtitle="Bank of China (UK) Limited (solo entity basis), £'000",
    rows=[
        ("SECTION", "UK OV1 'Overview of risk weighted exposure amounts' — each year's own Pillar 3 Disclosure for FY2025-FY2022, and the FY2020 Pillar 3 Disclosure's Table 9 for FY2020 with FY2019 as its comparative", {}),
        ("DATA", "Credit risk (excluding counterparty credit risk, standardised approach)", {
            "FY2025": 606687, "FY2024": 662567, "FY2023": 641596, "FY2022": 730027,
            "FY2020": 822496, "FY2019": 783214,
        }),
        ("DATA", "Counterparty credit risk (CCR, standardised approach)", {
            "FY2025": 5053, "FY2024": 8763, "FY2023": 6946, "FY2022": 19086,
        }),
        ("DATA", "Credit valuation adjustment (CVA)", {
            "FY2025": 31552, "FY2024": 94533, "FY2023": 74760, "FY2022": 198501,
            "FY2020": 114722, "FY2019": 12598,
        }),
        ("DATA", "Market risk (standardised approach)", {
            "FY2025": 1231, "FY2024": 1143, "FY2023": 766, "FY2022": 4394,
            "FY2020": 11621, "FY2019": 5448,
        }),
        ("DATA", "Operational risk", {
            "FY2025": 363586, "FY2024": 339893, "FY2023": 300383, "FY2022": 224618,
            "FY2020": 202676, "FY2019": 187641,
        }),
        ("TOTAL", "Total risk exposure amount", {"FY2025": 1008110, "FY2024": 1106898, "FY2023": 1024452, "FY2022": 1176625, "FY2020": 1151516, "FY2019": 988901}),
        ("SECTION", "Template EU OV1 — Pillar 3 Disclosure 2021, Table 1, p.14 (FY2021). This edition carries no separate counterparty-credit-risk line: CCR is folded into its credit-risk figure, so that row is NOT the same measure as the 'excluding CCR' row above — see sources note", {}),
        ("DATA", "Credit risk (standardised approach, CCR included as published)", {"FY2021": 793055}),
        ("DATA", "Credit valuation adjustment (CVA)", {"FY2021": 93581}),
        ("DATA", "Market risk (standardised approach)", {"FY2021": 14056}),
        ("DATA", "Operational risk", {"FY2021": 218688}),
        ("TOTAL", "Total risk exposure amount", {"FY2021": 1119380}),
        # GA-020 (2026-09-19): FY2014-FY2018 FOUND. This section previously read "Not publicly
        # disclosed - category breakdown". Every one of those five Pillar 3 editions prints an
        # 'Overview of RWA' table (the Basel/EBA OV1 layout); each figure below is from that
        # year's OWN edition, read from the page image: FY2014 Table 3, printed p.11 (PDF p.12);
        # FY2015 Table 3, p.12 (PDF p.13); FY2016 Table 3, p.13 (PDF p.14); FY2017 Table 3, p.13
        # (PDF p.14); FY2018 Table 6, p.28 (PDF p.29). See GA020_OV1_NOTE in the sources.
        ("SECTION", "'Overview of RWA' (Basel/EBA OV1 layout) — each year's own Pillar 3 Disclosure, FY2018-FY2014. Row definitions change in FY2017 (credit risk printed INCLUDING CCR); see sources note", {}),
        ("DATA", "Credit risk (excluding counterparty credit risk, standardised approach)", {"FY2018": 754002, "FY2016": 840455, "FY2015": 754715, "FY2014": 800993}),
        ("DATA", "Credit risk (including counterparty credit and dilution risks and free deliveries, as published)", {"FY2017": 757906}),
        ("DATA", "Counterparty credit risk (standardised approach; includes CVA per the same editions' Pillar 1 table)", {"FY2018": "-", "FY2016": 4164, "FY2015": 2062, "FY2014": 3251}),
        ("DATA", "Credit valuation adjustment (CVA)", {"FY2018": 2757, "FY2017": 2526}),
        ("DATA", "Market risk (standardised approach)", {"FY2018": 8927, "FY2017": 9694, "FY2016": 11206, "FY2015": 9973, "FY2014": 13244}),
        ("DATA", "Operational risk (Basic Indicator Approach)", {"FY2018": 175366, "FY2017": 161079, "FY2016": 148088, "FY2015": 128723, "FY2014": 107314}),
        ("TOTAL", "Total (as printed in the Overview of RWA table)", {"FY2018": 941052, "FY2017": 931206, "FY2016": 1003913, "FY2015": 895473, "FY2014": 924791}),
    ],
    sources_text=RWA_BREAKDOWN_SOURCES,
    first_col_width=58,
    source_height=280,
)

metric(
    "Leverage Ratio", "£'000 / %",
    [
        ("Total Basel III leverage ratio exposure measure", {"FY2025": 1373968, "FY2024": 1462346, "FY2023": 1473437, "FY2022": 1814024, "FY2021": 2431869, "FY2020": 2147455, "FY2019": 1894456, "FY2018": 1860587, "FY2017": 1794647, "FY2016": 1801366, "FY2015": 1593203, "FY2014": 1582346}),
        ("Basel III leverage ratio (%)", {"FY2025": "24.4%", "FY2024": "22.9%", "FY2023": "22.7%", "FY2022": "18.5%", "FY2021": "11.3%", "FY2020": "14.3%", "FY2019": "14.5%", "FY2018": "14.8%", "FY2017": "15%", "FY2016": "15%", "FY2015": "17%", "FY2014": "17%"}),
    ],
    p3_sources(),
    note="FY2021's 11.3% is on an older/broader exposure-measure basis (pre-dates the KM1 'excluding claims on "
         "central banks' framework used from FY2022 onward) - not directly comparable to later years, kept on "
         "its own row per project convention. FY2014-FY2020 use the pre-KM1 CRD IV leverage framework (Table 2 "
         "in each year's own document) - broadly the same 'Tier 1 capital / total exposure measure' concept "
         "throughout, but methodology details (e.g. treatment of off-balance-sheet items, central bank claims) "
         "evolved gradually across this whole span, so a smooth-looking multi-year trend should be read with "
         "that caveat rather than as a single unbroken methodology.",
)

metric(
    "LCR", "£'000 / %",
    [
        ("Total high-quality liquid assets (HQLA)", {"FY2025": 1007375, "FY2024": 1014087, "FY2023": 677646, "FY2022": 545654, "FY2021": 527697, "FY2020": 360820, "FY2019": 302154, "FY2018": 381928}),
        ("Total net cash outflow", {"FY2025": 310866, "FY2024": 272240, "FY2023": 174967, "FY2022": 299877, "FY2021": 294774, "FY2020": 148715, "FY2019": 139559, "FY2018": 164459}),
        ("LCR ratio (%)", {"FY2025": "324.1%", "FY2024": "372.5%", "FY2023": "387.3%", "FY2022": "182.0%", "FY2021": "179.0%", "FY2020": "243%", "FY2019": "217%", "FY2018": "232%", "FY2017": "167%"}),
    ],
    p3_sources(),
    note="FY2017's 167% ratio is the only FY2017 LCR figure available anywhere (from the FY2018 Pillar 3 "
         "document's own FY2017 comparative column - FY2017's own document predates LCR disclosure entirely) and "
         "has no accompanying HQLA/outflow £-breakdown, hence the blank cells on those two rows. LCR is "
         "genuinely undisclosed for FY2014-FY2016 (confirmed absent from all three years' own Pillar 3 "
         "documents, read in full).",
)

metric(
    "NSFR", "£'000 / %",
    [
        ("Total available stable funding", {"FY2025": 1389486, "FY2024": 1630136, "FY2023": 1289845, "FY2022": 1463448, "FY2021": 1438026, "FY2020": 1429700, "FY2019": 1263428, "FY2018": 1219968}),
        ("Total required stable funding", {"FY2025": 714820, "FY2024": 752941, "FY2023": 959234, "FY2022": 1209361, "FY2021": 950742, "FY2020": 884460, "FY2019": 797680, "FY2018": 843948}),
        ("NSFR ratio (%)", {"FY2025": "194.4%", "FY2024": "216.5%", "FY2023": "134.5%", "FY2022": "121.0%", "FY2021": "151.3%", "FY2020": "162%", "FY2019": "158%", "FY2018": "145%"}),
    ],
    p3_sources(),
    note="FY2021's own Pillar 3 document does not disclose an NSFR figure at all (the UK NSFR regime's formal KM1 "
         "disclosure only started from FY2022) - the FY2021 figures here are taken from the FY2022 Pillar 3 "
         "document's FY2021 comparative column instead, the only source where they appear. NSFR is genuinely "
         "undisclosed for FY2014-FY2017 (confirmed absent from all four years' own Pillar 3 documents, read in "
         "full) - FY2018 is the earliest year any NSFR figure exists for this bank.",
)

metric(
    "MREL Ratio", None,
    [("MREL ratio", {y: (f"Not published – BoC (UK) {y} Pillar 3 has no MREL figure, KM2 or eligible-"
                          "liabilities disclosure (text probe 0 hits, 2026-09-19)") for y in YEARS})],
    p3_sources(),
    note="No MREL disclosure found in any of the 12 available Pillar 3 documents (FY2014-FY2025) - each was read "
         "in full (table of contents plus a full-text search for 'MREL') and none contains one. Re-checked 2026-09-19 "
         "(GA-020): all 12 editions re-downloaded (%PDF, text-native); 0 hits for 'MREL', 'KM2' and 'eligible "
         "liabilities' in each, against 93-223 'capital' hits; the only 'loss-absorbing' hits are the generic "
         "countercyclical-buffer description.",
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {"FY2025": 2274441, "FY2024": 2323319, "FY2023": 2079373, "FY2022": 2290593, "FY2021": 2151180, "FY2020": 1941105, "FY2019": 1687388, "FY2018": 1630982, "FY2017": 1539221, "FY2016": 1549898, "FY2015": 1291410, "FY2014": 1215116}),
        ("Loans and advances to customers", {"FY2025": 810985, "FY2024": 941507, "FY2023": 990763, "FY2022": 1122459, "FY2021": 1194653, "FY2020": 1138583, "FY2019": 1064347, "FY2018": 1044570, "FY2017": 1054454, "FY2016": 1159696, "FY2015": 810776, "FY2014": 722307}),
        ("Deposits from customers", {"FY2025": 1304816, "FY2024": 1355529, "FY2023": 1223068, "FY2022": 1291150, "FY2021": 1333523, "FY2020": 1215647, "FY2019": 1132193, "FY2018": 1107439, "FY2017": 1019007, "FY2016": 982361, "FY2015": 737724, "FY2014": 765899}),
        ("Total shareholders' equity", {"FY2025": 399013, "FY2024": 413744, "FY2023": 433289, "FY2022": 401893, "FY2021": 306776, "FY2020": 342164, "FY2019": 307058, "FY2018": 326076, "FY2017": 307054, "FY2016": 310364, "FY2015": 320268, "FY2014": 301480}),
    ],
    balance_sheet_unit="£'000",
    income_statement_totals=[
        ("Total income", {"FY2025": 188290, "FY2024": 187263, "FY2023": 206185, "FY2022": 150380, "FY2021": 124048, "FY2020": 120103, "FY2019": 115237, "FY2018": 114561, "FY2017": 94483, "FY2016": 91182, "FY2015": 94921, "FY2014": 71621}),
        ("Staff costs", {"FY2025": -86079, "FY2024": -72194, "FY2023": -68058, "FY2022": -59208, "FY2021": -50154, "FY2020": -47607, "FY2019": -47279, "FY2018": -41868, "FY2017": -41365, "FY2016": -32821, "FY2015": -29500, "FY2014": -30178}),
        ("Profit for the year", {"FY2025": 68931, "FY2024": 83917, "FY2023": 103213, "FY2022": 68564, "FY2021": 31478, "FY2020": 35165, "FY2019": 32105, "FY2018": 51123, "FY2017": 32064, "FY2016": 35690, "FY2015": 45450, "FY2014": 25955}),
    ],
    income_statement_unit="£'000",
    equity_changes_totals=[
        ("Opening equity", {"FY2025": 413744, "FY2024": 433289, "FY2023": 401893, "FY2022": 306776, "FY2021": 342164, "FY2020": 307058, "FY2019": 326076, "FY2018": 307054, "FY2017": 310364, "FY2016": 320268, "FY2015": 301480, "FY2014": 307674}),
        ("Total comprehensive income", {"FY2025": 69011, "FY2024": 83917, "FY2023": 103211, "FY2022": 68576, "FY2021": 31612, "FY2020": 35106, "FY2019": 32105, "FY2018": 51123, "FY2017": 32380, "FY2016": 35546, "FY2015": 44743, "FY2014": 25679}),
        ("Other movements, net (AT1 issued / dividends / IFRS 9 transition)", {"FY2025": -83662, "FY2024": -103462, "FY2023": -71815, "FY2022": 26541, "FY2021": -67000, "FY2020": 0, "FY2019": -51123, "FY2018": -32101, "FY2017": -35690, "FY2016": -45450, "FY2015": -25955, "FY2014": -31873}),
        ("Closing equity", {"FY2025": 399013, "FY2024": 413744, "FY2023": 433289, "FY2022": 401893, "FY2021": 306776, "FY2020": 342164, "FY2019": 307058, "FY2018": 326076, "FY2017": 307054, "FY2016": 310364, "FY2015": 320268, "FY2014": 301480}),
    ],
    equity_changes_unit="£'000",
    cash_flow_totals=[
        ("Net cash generated from operating activities", {"FY2025": 111252, "FY2024": 405091, "FY2023": 233292, "FY2022": 22570, "FY2021": 304294, "FY2020": 100905, "FY2019": -49465, "FY2018": 52094, "FY2017": 36430, "FY2016": -31327, "FY2015": 145254, "FY2014": 52892}),
        ("Net cash from/(used in) investing activities", {"FY2025": -2623, "FY2024": -25826, "FY2023": -74896, "FY2022": -47511, "FY2021": -1147, "FY2020": 49511, "FY2019": 48732, "FY2018": -737, "FY2017": -66403, "FY2016": -775, "FY2015": -1089, "FY2014": -12257}),
        ("Net cash used in financing activities", {"FY2025": -84086, "FY2024": -103953, "FY2023": -71862, "FY2022": -33536, "FY2021": -68393, "FY2020": -1578, "FY2019": 0, "FY2018": 0, "FY2017": 0, "FY2016": 0, "FY2015": 0, "FY2014": 0}),
        ("Cash and cash equivalents at end of period", {"FY2025": 1073402, "FY2024": 1048859, "FY2023": 773547, "FY2022": 657656, "FY2021": 716133, "FY2020": 481379, "FY2019": 332542, "FY2018": 333275, "FY2017": 281944, "FY2016": 311917, "FY2015": 344019, "FY2014": 199854}),
    ],
    cash_flow_unit="£'000",
    ratios=[
        ("CET1 Ratio", {"FY2025": "27.2%", "FY2024": "24.8%", "FY2023": "26.8%", "FY2022": "23.4%", "FY2021": "24.6%", "FY2020": "26.7%", "FY2019": "27.8%", "FY2018": "29.2%", "FY2017": "30%", "FY2016": "27%", "FY2015": "31%", "FY2014": "34%"}),
        ("Tier 1 Ratio", {"FY2025": "33.2%", "FY2024": "30.2%", "FY2023": "32.7%", "FY2022": "28.5%", "FY2021": "24.6%", "FY2020": "26.7%", "FY2019": "27.8%", "FY2018": "29.2%", "FY2017": "30%", "FY2016": "27%", "FY2015": "31%", "FY2014": "34%"}),
        ("Total Capital Ratio", {"FY2025": "33.2%", "FY2024": "30.2%", "FY2023": "32.7%", "FY2022": "28.5%", "FY2021": "29.9%", "FY2020": "31.9%", "FY2019": "33.9%", "FY2018": "35.6%", "FY2017": "36%", "FY2016": "33%", "FY2015": "37%", "FY2014": "42%"}),
        ("Leverage Ratio", {"FY2025": "24.4%", "FY2024": "22.9%", "FY2023": "22.7%", "FY2022": "18.5%", "FY2021": "11.3%", "FY2020": "14.3%", "FY2019": "14.5%", "FY2018": "14.8%", "FY2017": "15%", "FY2016": "15%", "FY2015": "17%", "FY2014": "17%"}),
        ("LCR", {"FY2025": "324.1%", "FY2024": "372.5%", "FY2023": "387.3%", "FY2022": "182.0%", "FY2021": "179.0%", "FY2020": "243%", "FY2019": "217%", "FY2018": "232%", "FY2017": "167%"}),
        ("NSFR", {"FY2025": "194.4%", "FY2024": "216.5%", "FY2023": "134.5%", "FY2022": "121.0%", "FY2021": "151.3%", "FY2020": "162%", "FY2019": "158%", "FY2018": "145%"}),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own "
         "source citation for the underlying document/page. See the Cash Flow Statement sheet's source note for "
         "a disclosed restatement gap between FY2022's and FY2023's own reports. FY2014's own Annual Report PDF "
         "is a scanned document with no extractable text layer - its figures are taken from FY2015's own report's "
         "FY2014 comparative column instead (see AR2014_SCAN_NOTE on the Balance Sheet sheet). LCR and NSFR are "
         "genuinely undisclosed before FY2017/FY2018 respectively (blank, not zero).",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/BANK OF CHINA UK FINANCIALS.xlsx")
