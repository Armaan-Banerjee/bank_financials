import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021", "FY2020", "FY2019", "FY2018", "FY2017", "FY2016"]  # most recent first
YEAR_LABEL = {y: y for y in YEARS}

AR2021_URL = "https://cdn.craft.cloud/019db931-b985-7148-ac09-8f1d1e20d1a6/assets/content/hampden/content/Hampden-Co-Annual-Report-2021.pdf"
AR2022_URL = "https://cdn.craft.cloud/019db931-b985-7148-ac09-8f1d1e20d1a6/assets/content/hampden/content/Hampden-Co-2022-Annual-Report-and-Financial-Statements.pdf"
AR2023_URL = "https://cdn.craft.cloud/019db931-b985-7148-ac09-8f1d1e20d1a6/assets/content/hampden/content/Hampden-Co-Annual-Report-and-Financial-Statements-2023.pdf"
AR2024_URL = "https://cdn.craft.cloud/019db931-b985-7148-ac09-8f1d1e20d1a6/assets/content/hampden/content/Hampden-Bank-Annual-Report-and-Financial-Statements-2024.pdf"
AR2025_URL = "https://cdn.craft.cloud/019db931-b985-7148-ac09-8f1d1e20d1a6/assets/content/hampden/content/Hampden_Bank_Annual_Report_2025_2026-06-09-100801_cggc.pdf"

# FY2016-FY2020 Annual Reports: Companies House-filed scanned copies (image-only PDFs, no
# text layer - transcribed by reading each page as an image). Bank's own domain was checked
# via a full Wayback Machine CDX listing and carries no PDFs at all from before 2019 other than
# fscs_awareness.pdf, so Companies House is the only obtainable source for these 5 years.
AR2016_URL = "https://find-and-update.company-information.service.gov.uk/company/SC386922/filing-history/MzE3OTE1MzI3NmFkaXF6a2N4/document?format=pdf&download=0"
AR2017_URL = "https://find-and-update.company-information.service.gov.uk/company/SC386922/filing-history/MzIwNjc3MTg4N2FkaXF6a2N4/document?format=pdf&download=0"
AR2018_URL = "https://find-and-update.company-information.service.gov.uk/company/SC386922/filing-history/MzIzNjE3NTE0NmFkaXF6a2N4/document?format=pdf&download=0"
AR2019_URL = "https://find-and-update.company-information.service.gov.uk/company/SC386922/filing-history/MzI2NzQzODEwNWFkaXF6a2N4/document?format=pdf&download=0"
AR2020_URL = "https://find-and-update.company-information.service.gov.uk/company/SC386922/filing-history/MzMwNTYzNTA1MmFkaXF6a2N4/document?format=pdf&download=0"

P3_2021_URL = "https://hampdenandco.com/content/hampden/content/Hampden-Co-plc-2021-Pillar-3-Disclosures-FINAL.pdf"
P3_2022_URL = "https://hampdenandco.com/content/hampden/content/Hampden-Co-2022-Pillar-3-Disclosures.pdf"
P3_2023_URL = "https://cdn.craft.cloud/019db931-b985-7148-ac09-8f1d1e20d1a6/assets/content/hampden/content/Hampden-Co-plc-2023-Pillar-3-Disclosures.pdf"
# FY2019 Pillar 3 document is still live on the Bank's own domain; it also carries a full FY2018
# comparative column (used below for FY2018's metrics, since no standalone FY2018 Pillar 3 PDF
# was found anywhere - confirmed via a full Wayback CDX domain search of hampdenandco.com).
P3_2019_URL = "https://hampdenandco.com/content/hampden/content/Hampden-Co-plc-2019-Pillar-3-Disclosures-FINAL.pdf"
# FY2020 Pillar 3 document 404s on the live domain today; retrieved via its own Wayback Machine
# snapshot instead. It carries a full UK KM1-format Own Funds/Leverage Ratio appendix with an
# FY2019 comparative column (more precise than the FY2019 document's own rounded whole-percent
# figures), used below where noted.
P3_2020_URL = "https://web.archive.org/web/20220518033330/https://hampdenandco.com/content/hampden/content/Hampden-Co-Pillar-3-disclosures-2020-for-Web.pdf"

ENTITY_NOTE = (
    "Hampden & Co Plc (Companies House SC386922, FRN 606934) is a small Edinburgh-based private/relationship "
    "banking group; it began trading as 'Hampden Bank' during 2025/2026 but the legal entity name and company "
    "number are unchanged - confirmed via the entity's own 'about us' page. Incorporated 12 October 2010, but its "
    "own Annual Report FY2016 describes 2016 as still an early growth year for a 'fledgling bank' (deposits grew "
    "from GBP30m to GBP143m that year) - this ticket's confirmed floor of FY2016 (per HD-004) is used as instructed "
    "rather than reaching further back toward incorporation. The cash flow statement's presentation structure "
    "genuinely changes several times across this window rather than moving in one direction: FY2016-FY2019 and "
    "FY2021-FY2022 present operating activities as a single reconciliation block ending directly at 'Net cash "
    "from/(used in) operating activities'; FY2020 is a one-year exception with its own subtotal/tax split ('Cash "
    "(used in)/generated from operations', then 'Income tax received', then the final net total). "
    "FY2023 onward split it into a 'Cash generated from operations' subtotal followed by a separate 'Changes in "
    "operating assets and liabilities' block and a final operating subtotal (with 'Tax paid' appearing as its own "
    "line from FY2024). Each year is kept on its own as-disclosed structure rather than forced into a single row "
    "set. All comparative-year figures cross-checked against each year's own originally-published report - no "
    "restatements found anywhere in the FY2021-FY2025 window.\n"
    "FY2016-FY2020 sourced from scanned (image-only, no text layer) Companies House filings, read page-by-page. "
    "IFRS 9 was adopted 1 January 2018 (a GBP14k transition adjustment to opening retained earnings, no restatement "
    "of the FY2017 comparative); FY2016 and FY2017 are presented on the pre-IFRS 9 (IAS 39) basis, with no IFRS 9 "
    "stage split and no impairment provision recognised in either year ('No impairment provision has been "
    "recognised against the loans and advances to clients in the current or prior year'). IFRS 16 was adopted for "
    "FY2019 (Right-of-use assets/Lease liabilities lines appear for the first time that year; no restatement of "
    "the FY2018 comparative). A 'Deposits from banks' balance sheet liability line existed FY2016-FY2018 (GBP681k/"
    "GBP686k/nil) and was dropped from the statement entirely from FY2019 onward once it fell to nil - left blank "
    "for FY2019/FY2020 rather than assumed nil, since the line is no longer presented at all (distinct from an "
    "explicit disclosed '-', which is transcribed as 0). 'Current tax liabilities' did not exist as its own balance "
    "sheet line before FY2022. A standalone 'Provisions' line first appears in FY2018 (GBP118k) - FY2017's own "
    "balance sheet instead prints a single combined 'Other liabilities and provision' line (GBP158k), split here "
    "using that year's own Note 15/Note 24 detail (Other liabilities GBP39k, Provisions GBP119k, as separately "
    "confirmed via the FY2018 Annual Report's own FY2017 comparative note); FY2016 has no such combined line or "
    "provision of any kind (a plain 'Other liabilities' balance sheet line of GBP7k only). An 'Other reserves' "
    "equity line (a GBP19k capital redemption "
    "reserve, created 2016) existed FY2016-FY2018 and was cancelled to nil as part of the November-December 2019 "
    "share capital restructure (see Statement of Changes in Equity) - shown as 0 from FY2019 onward rather than "
    "omitted, since the underlying reserve genuinely still exists as a zero balance post-cancellation.\n"
    "A share capital restructure was approved by shareholders on 19 November 2019 and by the Court of Session on "
    "17 December 2019: a 20:1 share consolidation, a reduction of the GBP1.00 nominal value to GBP0.05 (with "
    "GBP63.1m of cancelled capital credited to retained earnings), and cancellation of the share premium account "
    "and capital redemption reserve (GBP18.1m, also credited to retained earnings) - this is the source of the "
    "sharp share capital/share premium level shift visible in the Statement of Changes in Equity between FY2018 "
    "and FY2019; it had no impact on cash, net assets or regulatory capital other than GBP0.1m of implementation "
    "costs. Two genuine source-internal inconsistencies are transcribed as printed rather than silently corrected: "
    "(1) the FY2016 Annual Report's own 'Cash and cash equivalents at end of year' (GBP108,931k) differs by GBP7k "
    "from the same balance shown as the FY2017 Annual Report's own 'beginning of year' comparative (GBP108,938k) - "
    "a reclassification between the cash/loans-to-banks split, not a cash movement; (2) the FY2017 Annual Report's "
    "Statement of Cash Flows opens with 'Loss before tax (6,359)', one thousand pounds different from the "
    "Statement of Comprehensive Income's own Loss before tax of (6,360) for the same year - the printed cash flow "
    "figure is used as-is since the statement's own arithmetic (to Net cash from operating activities) foots "
    "correctly from it. Similarly the FY2018 Annual Report's Statement of Cash Flows opens with a row labelled "
    "'Loss before tax' but printing (5,577) - which is actually that year's after-tax Loss for the year (the "
    "Statement of Comprehensive Income's own Loss before tax is (5,796)) - an apparent source mislabelling, "
    "transcribed as printed since the statement's own arithmetic foots correctly from the printed figure."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are Hampden & Co Plc's own Statement of Cash Flows, as filed with Companies House:\n"
    f"FY2025: Hampden Bank Annual Report and Financial Statements 2025, p.49 (Statement of cash flows) - {AR2025_URL}\n"
    f"FY2024: Hampden Bank Annual Report and Financial Statements 2024, p.51 (Statement of cash flows) - {AR2024_URL}\n"
    f"FY2023: Hampden & Co Plc Annual Report and Financial Statements 2023, p.44 (Statement of cash flows) - {AR2023_URL}\n"
    f"FY2022: Hampden & Co Plc Annual Report and Financial Statements 2022, p.45 (Statement of cash flows) - {AR2022_URL}\n"
    f"FY2021: Hampden & Co Plc Annual Report and Financial Statements 2021, p.56 (Statement of cash flows) - {AR2021_URL}\n"
    f"FY2020: Hampden & Co Plc Annual Report and Financial Statements 2020, p.54 (Statement of cash flows) - {AR2020_URL}\n"
    f"FY2019: Hampden & Co Plc Annual Report and Financial Statements 2019, p.31 (Statement of cash flows) - {AR2019_URL}\n"
    f"FY2018: Hampden & Co Plc Annual Report and Financial Statements 2018, p.22 (Statement of cash flows) - {AR2018_URL}\n"
    f"FY2017: Hampden & Co Plc Annual Report and Financial Statements 2017, p.25 (Statement of cash flows) - {AR2017_URL}\n"
    f"FY2016: Hampden & Co Plc Annual Report and Financial Statements 2016, p.18 (Statement of cash flows) - {AR2016_URL}\n"
    + ENTITY_NOTE
)


def p3_sources():
    return (
        "Sources - Hampden & Co Plc Pillar 3 Disclosures (Article 447/UK KM1 Key Metrics table unless noted):\n"
        f"FY2023/FY2022: Pillar 3 Disclosures for the year ended 31 December 2023, p.5-6 (UK KM1 Key metrics table) - {P3_2023_URL}\n"
        f"FY2021: Pillar 3 Disclosures for the year ended 31 December 2021 (pre-KM1 format), p.15 'Table 4: Capital resources' "
        f"and p.18 leverage ratio and p.26 'Table 15: Liquidity coverage ratio' - {P3_2021_URL}\n"
        f"FY2020: Pillar 3 disclosures for the year ended 31 December 2020, p.15 'Table 4: Capital resources', p.16 'Table 6: "
        f"Pillar 1 capital requirement', p.26 'Table 15: Liquidity coverage ratio', and Appendix 1/2 (UK KM1-style Own Funds and "
        f"Leverage Ratio templates, p.34-35) - {P3_2020_URL}\n"
        f"FY2019: Pillar 3 Disclosures for the year ended 31 December 2019, p.14-16 'Section 3.1 Composition of regulatory "
        f"capital and key ratios' and 'Table 6: Pillar 1 capital requirement', p.13 LCR - {P3_2019_URL}. More precise ratio/"
        f"leverage figures for FY2019 (26.1%/8.6% vs this document's own rounded 26%/9%) are instead taken from the FY2020 "
        f"Pillar 3 document's own FY2019 comparative KM1/leverage appendix columns, which are more granular.\n"
        "FY2018: no standalone Pillar 3 document was found published for FY2018 (confirmed via a full Wayback Machine CDX "
        "domain search of hampdenandco.com, which carries no PDF of any kind from before 2019 other than fscs_awareness.pdf) "
        f"- sourced instead from the FY2019 Pillar 3 document's own FY2018 comparative column ('Dec-18'), p.14-16 - {P3_2019_URL}. "
        "Only the whole-percent ratios and leverage ratio are available for FY2018 (that document does not carry a KM1-style "
        "appendix for its comparative year).\n"
        "FY2017/FY2016: not publicly disclosed - no Pillar 3 document exists for either year (same full domain Wayback CDX "
        "search as above; the FY2016/FY2017 Annual Reports' own Note 24/Note 20 'Capital management policy' state only that "
        "Pillar 3 disclosures 'are published annually and are available on the Bank's website', without giving any figures "
        "in the statutory accounts themselves, and no such document was ever crawled by the Wayback Machine for those years).\n"
        "FY2024/FY2025: no standalone Pillar 3 document was found published for either year (last located Pillar 3 disclosure "
        "covers FY2023) - Total Capital Ratio only is sourced from each year's own Annual Report Key Performance Indicators "
        f"table instead (FY2024 AR p.7, FY2025 AR p.11) - {AR2024_URL} / {AR2025_URL}. All other metrics are not publicly "
        "disclosed for FY2024/FY2025."
    )


bw = BankWorkbook(bank_name="Hampden & Co Plc", years=YEARS, year_label=YEAR_LABEL, header_color="32ADB6")

STATEMENTS_SOURCES = (
    "Sources - all figures are Hampden & Co Plc's own Statement of Financial Position / Statement of "
    "Comprehensive Income / Statement of Changes in Equity, as filed with Companies House:\n"
    f"FY2025: Hampden Bank Annual Report and Financial Statements 2025, p.46-48 - {AR2025_URL}\n"
    f"FY2024: Hampden Bank Annual Report and Financial Statements 2024, p.48-50 - {AR2024_URL}\n"
    f"FY2023: Hampden & Co Plc Annual Report and Financial Statements 2023, p.41-43 - {AR2023_URL}\n"
    f"FY2022: Hampden & Co Plc Annual Report and Financial Statements 2022, p.42-44 - {AR2022_URL}\n"
    f"FY2021: Hampden & Co Plc Annual Report and Financial Statements 2021, p.53-55 - {AR2021_URL}\n"
    f"FY2020: Hampden & Co Plc Annual Report and Financial Statements 2020, p.51-53 - {AR2020_URL}\n"
    f"FY2019: Hampden & Co Plc Annual Report and Financial Statements 2019, p.28-30 - {AR2019_URL}\n"
    f"FY2018: Hampden & Co Plc Annual Report and Financial Statements 2018, p.19-21 - {AR2018_URL}\n"
    f"FY2017: Hampden & Co Plc Annual Report and Financial Statements 2017, p.22-24 - {AR2017_URL}\n"
    f"FY2016: Hampden & Co Plc Annual Report and Financial Statements 2016, p.15-17 - {AR2016_URL}\n"
    + ENTITY_NOTE
    + " Debt securities and the FY2022 hedge-accounting-related lines (Fair value adjustment for hedged risk, "
    "Derivative financial instruments, Deferred tax asset, Current tax liabilities) genuinely did not exist as "
    "separate balance sheet lines before FY2022 (the Bank started using interest rate hedges and holding debt "
    "securities that year) - left blank for FY2021 rather than assumed nil, except where that year's own report "
    "explicitly shows a dash ('-'), which is transcribed as a disclosed nil (0).\n"
    "DEBT SECURITIES COMPOSITION: checked each year's own Note 19 'Financial instruments' ('Categories of financial "
    "instruments' table) for a measurement-basis / issuer-type breakdown. No numeric split exists in any year - the "
    "table shows the entire balance in a single 'Amortised cost' column with £nil in the 'Fair value through profit "
    "or loss' column every year (no FVOCI column at all), so the row is relabelled in place rather than split into "
    "sub-rows. Issuer-type composition (100% sovereign government debt throughout, narrative-only, no per-country "
    f"split of the total is disclosed): FY2023: 'All debt securities held are UK Government debt securities' - "
    f"Hampden & Co Plc Annual Report and Financial Statements 2023, Note 19, p.65 - {AR2023_URL}. FY2024: 'All debt "
    "securities held are UK Government or US Department of Treasury debt securities' per that year's own Note 19 "
    "(p.69), though the same report's Note 21 credit-risk section (p.74) instead states 'Debt securities are all "
    "issued by the UK Government' - an internal inconsistency in the FY2024 Annual Report itself, transcribed as "
    f"printed rather than resolved - Hampden Bank Annual Report and Financial Statements 2024, Note 19, p.69 - "
    f"{AR2024_URL}. FY2025: 'All debt securities held are issued by the UK, US and Australian governments' - "
    f"Hampden Bank Annual Report and Financial Statements 2025, Note 19, p.69 (also carries the FY2024 comparative "
    f"column) - {AR2025_URL}. FY2022: nil balance, no securities held. No supranational, corporate or ABS holdings "
    "are disclosed in any year."
)

# ---------------------------------------------------------------
# Sheet: Balance Sheet
# ---------------------------------------------------------------
bs_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and balances at central banks", {
        "FY2025": 60397, "FY2024": 52771, "FY2023": 104956, "FY2022": 172477, "FY2021": 139948,
        "FY2020": 117058, "FY2019": 119691, "FY2018": 91135, "FY2017": 83278, "FY2016": 101954,
    }),
    ("DATA", "Loans and advances to banks", {
        "FY2025": 137120, "FY2024": 203664, "FY2023": 274523, "FY2022": 241254, "FY2021": 189686,
        "FY2020": 108358, "FY2019": 129085, "FY2018": 81759, "FY2017": 58618, "FY2016": 26499,
    }),
    ("DATA", "Debt securities (sovereign government debt, amortised cost)", {
        "FY2025": 362399, "FY2024": 224751, "FY2023": 67066, "FY2022": 0,
    }),
    ("DATA", "Loans and advances to clients", {
        "FY2025": 639581, "FY2024": 585893, "FY2023": 487624, "FY2022": 447675, "FY2021": 422160,
        "FY2020": 326254, "FY2019": 203807, "FY2018": 132488, "FY2017": 94198, "FY2016": 48137,
    }),
    ("DATA", "Fair value adjustment for hedged risk on loans and advances to clients", {
        "FY2025": 607, "FY2024": -175, "FY2023": 759, "FY2022": -256, "FY2021": 0,
    }),
    ("DATA", "Derivative financial instruments", {
        "FY2025": 413, "FY2024": 1016, "FY2023": 1083, "FY2022": 1867, "FY2021": 0,
    }),
    ("DATA", "Deferred tax asset", {
        "FY2025": 3823, "FY2024": 5605, "FY2023": 4315, "FY2022": 4819, "FY2021": 0,
    }),
    ("DATA", "Prepayments and accrued income", {
        "FY2025": 2334, "FY2024": 1063, "FY2023": 623, "FY2022": 1118, "FY2021": 913,
        "FY2020": 727, "FY2019": 714, "FY2018": 503, "FY2017": 417, "FY2016": 555,
    }),
    ("DATA", "Other assets", {
        "FY2025": 558, "FY2024": 508, "FY2023": 513, "FY2022": 2372, "FY2021": 212,
        "FY2020": 215, "FY2019": 233, "FY2018": 220, "FY2017": 186, "FY2016": 168,
    }),
    ("DATA", "Property, plant and equipment", {
        "FY2025": 1370, "FY2024": 570, "FY2023": 176, "FY2022": 143, "FY2021": 85,
        "FY2020": 111, "FY2019": 141, "FY2018": 195, "FY2017": 258, "FY2016": 312,
    }),
    ("DATA", "Right-of-use assets", {
        "FY2025": 8051, "FY2024": 4439, "FY2023": 589, "FY2022": 714, "FY2021": 1139,
        "FY2020": 1650, "FY2019": 2093,
    }),
    ("DATA", "Intangible assets", {
        "FY2025": 10396, "FY2024": 9197, "FY2023": 3936, "FY2022": 2302, "FY2021": 2038,
        "FY2020": 1752, "FY2019": 2342, "FY2018": 2910, "FY2017": 3241, "FY2016": 2948,
    }),
    ("TOTAL", "Total assets", {
        "FY2025": 1227049, "FY2024": 1089302, "FY2023": 946163, "FY2022": 874485, "FY2021": 756181,
        "FY2020": 556125, "FY2019": 458106, "FY2018": 309210, "FY2017": 240196, "FY2016": 180573,
    }),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Deposits from banks", {
        "FY2018": 0, "FY2017": 686, "FY2016": 681,
    }),
    ("DATA", "Deposits from clients", {
        "FY2025": 1123743, "FY2024": 990720, "FY2023": 857506, "FY2022": 796049, "FY2021": 695590,
        "FY2020": 501163, "FY2019": 409374, "FY2018": 267483, "FY2017": 193926, "FY2016": 143415,
    }),
    ("DATA", "Derivative financial instruments (liability)", {
        "FY2025": 788, "FY2024": 436, "FY2023": 1194, "FY2022": 838, "FY2021": 0,
    }),
    ("DATA", "Current tax liabilities", {
        "FY2025": 72, "FY2024": 22, "FY2023": 532, "FY2022": 0,
    }),
    ("DATA", "Accruals and deferred income", {
        "FY2025": 2530, "FY2024": 3472, "FY2023": 3447, "FY2022": 3440, "FY2021": 2014,
        "FY2020": 1795, "FY2019": 1662, "FY2018": 1756, "FY2017": 1703, "FY2016": 1574,
    }),
    ("DATA", "Lease liabilities", {
        "FY2025": 7565, "FY2024": 3940, "FY2023": 574, "FY2022": 756, "FY2021": 1134,
        "FY2020": 1665, "FY2019": 2076,
    }),
    ("DATA", "Other liabilities", {
        "FY2025": 24, "FY2024": 87, "FY2023": 21, "FY2022": 174, "FY2021": 18,
        "FY2020": 38, "FY2019": 14, "FY2018": 1, "FY2017": 39, "FY2016": 7,
    }),
    ("DATA", "Provisions", {
        "FY2025": 291, "FY2024": 517, "FY2023": 465, "FY2022": 376, "FY2021": 123,
        "FY2020": 125, "FY2019": 116, "FY2018": 118, "FY2017": 119,
    }),
    ("TOTAL", "Total liabilities", {
        "FY2025": 1135013, "FY2024": 999194, "FY2023": 863739, "FY2022": 801633, "FY2021": 698879,
        "FY2020": 504786, "FY2019": 413242, "FY2018": 269358, "FY2017": 196473, "FY2016": 145677,
    }),
    ("SECTION", "Equity", {}),
    ("DATA", "Share capital", {
        "FY2025": 4726, "FY2024": 4726, "FY2023": 4726, "FY2022": 4623, "FY2021": 4223,
        "FY2020": 3823, "FY2019": 3322, "FY2018": 59902, "FY2017": 59369, "FY2016": 49282,
    }),
    ("DATA", "Share premium account", {
        "FY2025": 25865, "FY2024": 25865, "FY2023": 25865, "FY2022": 24001, "FY2021": 16555,
        "FY2020": 9064, "FY2019": 0, "FY2018": 15066, "FY2017": 14812, "FY2016": 9939,
    }),
    ("DATA", "Other reserves", {
        "FY2020": 0, "FY2019": 0, "FY2018": 19, "FY2017": 19, "FY2016": 19,
    }),
    ("DATA", "Retained earnings", {
        "FY2025": 61445, "FY2024": 59517, "FY2023": 51833, "FY2022": 44228, "FY2021": 36524,
        "FY2020": 38452, "FY2019": 41542, "FY2018": -35135, "FY2017": -30477, "FY2016": -24344,
    }),
    ("TOTAL", "Total equity", {
        "FY2025": 92036, "FY2024": 90108, "FY2023": 82424, "FY2022": 72852, "FY2021": 57302,
        "FY2020": 51339, "FY2019": 44864, "FY2018": 39852, "FY2017": 43723, "FY2016": 34896,
    }),
    ("TOTAL", "Total liabilities and equity", {
        "FY2025": 1227049, "FY2024": 1089302, "FY2023": 946163, "FY2022": 874485, "FY2021": 756181,
        "FY2020": 556125, "FY2019": 458106, "FY2018": 309210, "FY2017": 240196, "FY2016": 180573,
    }),
]

bw.add_balance_sheet_sheet(
    title="Hampden & Co Plc — Statement of Financial Position",
    subtitle="Company-only statement, as filed with Companies House",
    rows=bs_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=70,
    source_height=190,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Sheet: Profit & Loss
# ---------------------------------------------------------------
is_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest receivable and similar income", {
        "FY2025": 54016, "FY2024": 53961, "FY2023": 45265, "FY2022": 22882, "FY2021": 12542,
        "FY2020": 10144, "FY2019": 9241, "FY2018": 6022, "FY2017": 3389, "FY2016": 1502,
    }),
    ("DATA", "Interest payable and similar charges", {
        "FY2025": -24738, "FY2024": -25613, "FY2023": -16096, "FY2022": -2821, "FY2021": -868,
        "FY2020": -1233, "FY2019": -1661, "FY2018": -561, "FY2017": -200, "FY2016": -214,
    }),
    ("TOTAL", "Net interest income", {
        "FY2025": 29278, "FY2024": 28348, "FY2023": 29169, "FY2022": 20061, "FY2021": 11674,
        "FY2020": 8911, "FY2019": 7580, "FY2018": 5461, "FY2017": 3189, "FY2016": 1288,
    }),
    ("DATA", "Non-interest income", {
        "FY2025": 1152, "FY2024": 1055, "FY2023": 1043, "FY2022": 906, "FY2021": 758,
        "FY2020": 631, "FY2019": 627, "FY2018": 577, "FY2017": 465, "FY2016": 172,
    }),
    ("DATA", "Income from currency operations", {
        "FY2025": 1144, "FY2024": 1124, "FY2023": 1278, "FY2022": 1069, "FY2021": 775,
        "FY2020": 695, "FY2019": 476, "FY2018": 326, "FY2017": 251, "FY2016": 179,
    }),
    ("DATA", "Net (losses)/gains from derivatives and hedge accounting", {
        "FY2025": -111, "FY2024": -203, "FY2023": -303, "FY2022": 820, "FY2021": 0,
    }),
    ("TOTAL", "Total income", {
        "FY2025": 31463, "FY2024": 30324, "FY2023": 31187, "FY2022": 22856, "FY2021": 13207,
        "FY2020": 10237, "FY2019": 8683, "FY2018": 6364, "FY2017": 3905, "FY2016": 1639,
    }),
    ("SECTION", "Operating expenses", {}),
    ("DATA", "Administrative expenses", {
        "FY2025": -21945, "FY2024": -20873, "FY2023": -20903, "FY2022": -19837, "FY2021": -15006,
        "FY2020": -13007, "FY2019": -13028, "FY2018": -11502, "FY2017": -9638, "FY2016": -7282,
    }),
    ("DATA", "Depreciation and amortisation", {
        "FY2025": -2672, "FY2024": -1258, "FY2023": -1038, "FY2022": -945, "FY2021": -1176,
        "FY2020": -1193, "FY2019": -1211, "FY2018": -641, "FY2017": -627, "FY2016": -616,
    }),
    ("TOTAL", "Operating expenses", {
        "FY2025": -24617, "FY2024": -22131, "FY2023": -21941, "FY2022": -20782, "FY2021": -16182,
        "FY2020": -14200, "FY2019": -14239, "FY2018": -12143, "FY2017": -10265, "FY2016": -7898,
    }),
    ("TOTAL", "Operating profit/(loss) before impairment losses", {
        "FY2025": 6846, "FY2024": 8193, "FY2023": 9246, "FY2022": 2074, "FY2021": -2975,
        "FY2020": -3963, "FY2019": -5556, "FY2018": -5779, "FY2017": -6360, "FY2016": -6259,
    }),
    ("DATA", "Impairment credit/(charge) on loans and advances to clients", {
        "FY2025": 107, "FY2024": -12, "FY2023": -103, "FY2022": -29, "FY2021": 5,
        "FY2020": -173, "FY2019": 23, "FY2018": -17, "FY2017": 0, "FY2016": 0,
    }),
    ("TOTAL", "Profit/(loss) before tax", {
        "FY2025": 6953, "FY2024": 8181, "FY2023": 9143, "FY2022": 2045, "FY2021": -2970,
        "FY2020": -4136, "FY2019": -5533, "FY2018": -5796, "FY2017": -6360, "FY2016": -6259,
    }),
    ("DATA", "Tax (expense)/income", {
        "FY2025": -1964, "FY2024": 930, "FY2023": -1036, "FY2022": 4819, "FY2021": 0,
        "FY2020": 57, "FY2019": 0, "FY2018": 219, "FY2017": 0, "FY2016": 0,
    }),
    ("TOTAL", "Profit/(loss) for the year and total comprehensive profit/(loss)", {
        "FY2025": 4989, "FY2024": 9111, "FY2023": 8107, "FY2022": 6864, "FY2021": -2970,
        "FY2020": -4079, "FY2019": -5533, "FY2018": -5577, "FY2017": -6360, "FY2016": -6259,
    }),
]

bw.add_income_statement_sheet(
    title="Hampden & Co Plc — Statement of Comprehensive Income",
    subtitle="Company-only statement, as filed with Companies House",
    rows=is_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=70,
    source_height=190,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Sheet: Statement of Changes in Equity
# ---------------------------------------------------------------
eq_headers = ["Share capital", "Share premium account", "Other reserves", "Retained earnings", "Total equity"]
eq_rows = [
    ("TOTAL", "At 1 January 2016", (46090, 9048, 0, -18085, 37053)),
    ("DATA", "Loss for the year and total comprehensive loss", (None, None, None, -6259, -6259)),
    ("DATA", "Issue of share capital", (3211, 963, None, None, 4174)),
    ("DATA", "Direct share issue costs", (None, -72, None, None, -72)),
    ("DATA", "Cancellation of ordinary B and C shares", (-19, None, 19, None, 0)),
    ("TOTAL", "At 31 December 2016", (49282, 9939, 19, -24344, 34896)),
    ("DATA", "Loss for the year and total comprehensive loss", (None, None, None, -6360, -6360)),
    ("DATA", "Issue of share capital", (10087, 5043, None, None, 15130)),
    ("DATA", "Direct share issue costs", (None, -170, None, None, -170)),
    ("DATA", "Equity settled share-based payments", (None, None, None, 227, 227)),
    ("TOTAL", "At 31 December 2017", (59369, 14812, 19, -30477, 43723)),
    ("DATA", "Impact of initial application of IFRS 9", (None, None, None, -14, -14)),
    ("TOTAL", "At 1 January 2018 after adopting IFRS 9", (59369, 14812, 19, -30491, 43709)),
    ("DATA", "Loss for the year and total comprehensive loss", (None, None, None, -5577, -5577)),
    ("DATA", "Issue of share capital", (533, 268, None, None, 801)),
    ("DATA", "Direct share issue costs", (None, -14, None, None, -14)),
    ("DATA", "Equity settled share-based payments", (None, None, None, 933, 933)),
    ("TOTAL", "At 31 December 2018", (59902, 15066, 19, -35135, 39852)),
    ("DATA", "Loss for the year and total comprehensive loss", (None, None, None, -5533, -5533)),
    ("DATA", "Issue of share capital", (6543, 3271, None, None, 9814)),
    ("DATA", "Direct share issue costs", (None, -145, None, None, -145)),
    ("DATA", "Share capital restructure", (-63123, -18083, -19, 81225, 0)),
    ("DATA", "Direct share capital restructure costs", (None, -109, None, None, -109)),
    ("DATA", "Equity settled share-based payments", (None, None, None, 985, 985)),
    ("TOTAL", "At 31 December 2019", (3322, 0, 0, 41542, 44864)),
    ("DATA", "Loss for the year and total comprehensive loss", (None, None, None, -4079, -4079)),
    ("DATA", "Issue of share capital", (501, 9514, None, None, 10015)),
    ("DATA", "Direct share issue costs", (None, -450, None, None, -450)),
    ("DATA", "Equity settled share-based payments", (None, None, None, 989, 989)),
    ("TOTAL", "At 31 December 2020", (3823, 9064, 0, 38452, 51339)),
    ("DATA", "Loss for the year and total comprehensive loss", (None, None, None, -2970, -2970)),
    ("DATA", "Issue of share capital", (400, 7600, None, None, 8000)),
    ("DATA", "Direct share issue costs", (None, -109, None, None, -109)),
    ("DATA", "Equity settled share-based payments", (None, None, None, 1042, 1042)),
    ("TOTAL", "At 31 December 2021", (4223, 16555, 0, 36524, 57302)),
    ("DATA", "Profit for the year and total comprehensive profit", (None, None, None, 6864, 6864)),
    ("DATA", "Issue of share capital", (400, 7600, None, None, 8000)),
    ("DATA", "Direct share issue costs", (None, -154, None, None, -154)),
    ("DATA", "Equity settled share-based payments", (None, None, None, 840, 840)),
    ("TOTAL", "At 31 December 2022", (4623, 24001, 0, 44228, 72852)),
    ("DATA", "Profit for the year and total comprehensive profit", (None, None, None, 8107, 8107)),
    ("DATA", "Issue of share capital", (103, 1956, None, None, 2059)),
    ("DATA", "Direct share issue costs", (None, -92, None, None, -92)),
    ("DATA", "Equity settled share-based payments", (None, None, None, 186, 186)),
    ("DATA", "Cancellation of share options", (None, None, None, -688, -688)),
    ("TOTAL", "At 31 December 2023", (4726, 25865, 0, 51833, 82424)),
    ("DATA", "Profit for the year and total comprehensive profit", (None, None, None, 9111, 9111)),
    ("DATA", "Dividends", (None, None, None, -1512, -1512)),
    ("DATA", "Equity settled share-based payments", (None, None, None, 176, 176)),
    ("DATA", "Dividend equivalent on share options", (None, None, None, -91, -91)),
    ("TOTAL", "At 31 December 2024", (4726, 25865, 0, 59517, 90108)),
    ("DATA", "Profit for the year and total comprehensive profit", (None, None, None, 4989, 4989)),
    ("DATA", "Dividends", (None, None, None, -3024, -3024)),
    ("DATA", "Equity settled share-based payments", (None, None, None, 145, 145)),
    ("DATA", "Dividend equivalent on share options", (None, None, None, -182, -182)),
    ("TOTAL", "At 31 December 2025", (4726, 25865, 0, 61445, 92036)),
]

bw.add_equity_changes_sheet(
    title="Hampden & Co Plc — Statement of Changes in Equity",
    subtitle="Company-only statement, as filed with Companies House — read chronologically, oldest to newest",
    headers=eq_headers,
    rows=eq_rows,
    sources_text=(
        STATEMENTS_SOURCES
        + " Equity reconciliation ladder: every year's closing balance ties exactly to both the next year's own "
        "reported opening balance and that year's own Balance Sheet Total equity - zero plug rows needed anywhere "
        "in this FY2016-FY2025 window, including through the November-December 2019 share capital restructure "
        "(net nil impact on Total equity) and the FY2017/FY2018 IFRS 9 transition adjustment."
    ),
    first_col_width=52,
    source_height=190,
)

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Profit/(loss) before tax", {
        "FY2025": 6953, "FY2024": 8181, "FY2023": 9143, "FY2022": 2045, "FY2021": -2970,
        "FY2020": -4136, "FY2019": -5533, "FY2018": -5577, "FY2017": -6359, "FY2016": -6259,
    }),
    ("DATA", "Net losses/(gains) from derivatives and hedge accounting", {
        "FY2025": 111, "FY2024": 203, "FY2023": 303, "FY2022": -820,
    }),
    ("DATA", "Depreciation and amortisation", {
        "FY2025": 2672, "FY2024": 1258, "FY2023": 1038, "FY2022": 945, "FY2021": 1176,
        "FY2020": 1193, "FY2019": 1211, "FY2018": 641, "FY2017": 627, "FY2016": 616,
    }),
    ("DATA", "Equity settled share-based payments", {
        "FY2025": 145, "FY2024": 176, "FY2023": 186, "FY2022": 840, "FY2021": 1042,
        "FY2020": 989, "FY2019": 985, "FY2018": 933, "FY2017": 227,
    }),
    ("DATA", "Dividend equivalent on share options", {
        "FY2025": -182, "FY2024": -91,
    }),
    ("DATA", "Cancellation of share options", {
        "FY2023": -688,
    }),
    ("DATA", "Impairment (credit)/charge for the year", {
        "FY2025": -107, "FY2024": 12, "FY2023": 103, "FY2022": 29, "FY2021": -5,
        "FY2020": 173, "FY2019": -23, "FY2018": 17,
    }),
    ("DATA", "(Increase) in prepayments and accrued income", {
        "FY2021": -185, "FY2020": -13, "FY2019": -328, "FY2018": -86, "FY2017": -29, "FY2016": -322,
    }),
    ("DATA", "Increase/(decrease) in accruals and deferred income", {
        "FY2021": 353, "FY2020": -14, "FY2019": 189, "FY2018": 53, "FY2017": 394, "FY2016": -250,
    }),
    ("DATA", "(Increase) in loans and advances to clients and banks", {
        "FY2021": -132311, "FY2020": -139270, "FY2019": -95184, "FY2018": -45597, "FY2017": -43213, "FY2016": -45258,
    }),
    ("DATA", "Increase in deposits by clients and banks", {
        "FY2021": 194668, "FY2020": 91418, "FY2019": 144772, "FY2018": 70424, "FY2017": 55429, "FY2016": 110608,
    }),
    ("DATA", "Decrease in other assets", {
        "FY2021": 3, "FY2020": 17,
    }),
    ("DATA", "(Increase) in other assets", {
        "FY2019": -11, "FY2018": -36, "FY2017": -19, "FY2016": -20,
    }),
    ("DATA", "(Decrease)/increase in other liabilities and provisions", {
        "FY2021": -22, "FY2020": 34, "FY2019": 11, "FY2018": -38, "FY2017": 151, "FY2016": 3,
    }),
    ("DATA", "Elimination of foreign exchange differences", {
        "FY2022": 8, "FY2021": -9, "FY2020": 7, "FY2019": 8, "FY2018": 1, "FY2016": 1,
    }),
    ("TOTAL", "Cash generated from/(used in) operations", {
        "FY2025": 9592, "FY2024": 9739, "FY2023": 10085,
    }),
    ("TOTAL", "Cash (used in)/generated from operations", {
        "FY2020": -49602,
    }),
    ("SECTION", "Changes in operating assets and liabilities", {}),
    ("DATA", "Increase/(decrease) in prepayments and accrued income", {
        "FY2025": -1271, "FY2024": -441, "FY2023": 421, "FY2022": -205,
    }),
    ("DATA", "Increase/(decrease) in accruals and deferred income", {
        "FY2025": -942, "FY2024": 25, "FY2023": 6, "FY2022": 1560,
    }),
    ("DATA", "Decrease/(increase) in loans and advances to clients and banks", {
        "FY2025": 34430, "FY2024": -57243, "FY2023": -93474, "FY2022": -43506,
    }),
    ("DATA", "Increase in deposits from clients/by clients and banks", {
        "FY2025": 133690, "FY2024": 134544, "FY2023": 67050, "FY2022": 90941,
    }),
    ("DATA", "(Increase)/decrease in other assets", {
        "FY2025": -49, "FY2024": 5, "FY2023": 1859, "FY2022": -2160,
    }),
    ("DATA", "(Decrease)/increase in other liabilities and provisions", {
        "FY2025": -285, "FY2024": 117, "FY2023": -56, "FY2022": 405,
    }),
    ("TOTAL", "Cash generated from/(used in) operating activities", {
        "FY2025": 175165, "FY2024": 86746, "FY2023": -14109,
    }),
    ("DATA", "Tax paid/(income tax received)", {
        "FY2025": -131, "FY2024": -870, "FY2021": 0, "FY2020": 57,
    }),
    ("TOTAL", "Net cash from/(used in) operating activities", {
        "FY2025": 175034, "FY2024": 85876, "FY2023": -14109, "FY2022": 50082, "FY2021": 61740,
        "FY2020": -49545, "FY2019": 46097, "FY2018": 20701, "FY2017": 7208, "FY2016": 59119,
    }),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Purchase of debt securities", {
        "FY2025": -853557, "FY2024": -414862, "FY2023": -67066,
    }),
    ("DATA", "Sales and maturities of debt securities", {
        "FY2025": 715908, "FY2024": 257177,
    }),
    ("DATA", "Purchase of property, plant and equipment", {
        "FY2025": -1848, "FY2024": -902, "FY2023": -77, "FY2022": -86,
        "FY2020": -2, "FY2018": -3, "FY2017": -11, "FY2016": -25,
    }),
    ("DATA", "Purchases/development of intangible assets", {
        "FY2025": -2736, "FY2024": -5995, "FY2023": -2184, "FY2022": -891, "FY2021": -1145,
        "FY2020": -158, "FY2019": -457, "FY2018": -245, "FY2017": -855,
    }),
    ("TOTAL", "Net cash from/(used in) investing activities", {
        "FY2025": -142233, "FY2024": -164582, "FY2023": -69327, "FY2022": -977, "FY2021": -1145,
        "FY2020": -160, "FY2019": -457, "FY2018": -248, "FY2017": -866, "FY2016": -25,
    }),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Repayment of lease liabilities", {
        "FY2025": -74, "FY2024": -500, "FY2023": -427, "FY2022": -378, "FY2021": -445,
        "FY2020": -412, "FY2019": -385,
    }),
    ("DATA", "Proceeds from issue of shares", {
        "FY2023": 2059, "FY2022": 8000, "FY2021": 8000,
        "FY2020": 10015, "FY2019": 9814, "FY2018": 801, "FY2017": 15130, "FY2016": 4050,
    }),
    ("DATA", "Direct costs of share issuance", {
        "FY2023": -92, "FY2022": -154, "FY2021": -109,
        "FY2018": -14, "FY2017": -170, "FY2016": -72,
    }),
    ("DATA", "Direct costs of share issuance and share capital restructure", {
        "FY2020": -272, "FY2019": -184,
    }),
    ("DATA", "Equity dividends paid", {
        "FY2025": -3024, "FY2024": -1512,
    }),
    ("TOTAL", "Net cash from/(used in) financing activities", {
        "FY2025": -3098, "FY2024": -2012, "FY2023": 1540, "FY2022": 7468, "FY2021": 7446,
        "FY2020": 9331, "FY2019": 9245, "FY2018": 787, "FY2017": 14960, "FY2016": 3978,
    }),
    ("TOTAL", "Net increase/(decrease) in cash and cash equivalents", {
        "FY2025": 29703, "FY2024": -80718, "FY2023": -81896, "FY2022": 56573, "FY2021": 68041,
        "FY2020": -40374, "FY2019": 54885, "FY2018": 21240, "FY2017": 21301, "FY2016": 63072,
    }),
    ("DATA", "Cash and cash equivalents at the beginning of the year", {
        "FY2025": 125315, "FY2024": 207363, "FY2023": 294851, "FY2022": 228768, "FY2021": 160960,
        "FY2020": 200970, "FY2019": 148975, "FY2018": 125284, "FY2017": 108938, "FY2016": 43290,
    }),
    ("DATA", "Effects of foreign exchange rate changes on cash and cash equivalents", {
        "FY2025": -667, "FY2024": -1330, "FY2023": -5592, "FY2022": 9510, "FY2021": -233,
        "FY2020": 364, "FY2019": -2890, "FY2018": 2451, "FY2017": -4955, "FY2016": 2569,
    }),
    ("TOTAL", "Cash and cash equivalents at the end of the year", {
        "FY2025": 154351, "FY2024": 125315, "FY2023": 207363, "FY2022": 294851, "FY2021": 228768,
        "FY2020": 160960, "FY2019": 200970, "FY2018": 148975, "FY2017": 125284, "FY2016": 108931,
    }),
]

bw.add_cash_flow_sheet(
    title="Hampden & Co Plc — Statement of Cash Flows",
    subtitle="Company-only statement, as filed with Companies House",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=70,
    source_height=170,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Sheet: Asset Quality
# ---------------------------------------------------------------
aq_rows = [
    ("SECTION", "Loans and advances to clients, gross carrying amount by IFRS 9 stage", {}),
    ("DATA", "Stage 1", {
        "FY2025": 609002, "FY2024": 562580, "FY2023": 471836, "FY2022": 432518, "FY2021": 402514,
        "FY2020": 313209, "FY2019": 194573, "FY2018": 125408,
    }),
    ("DATA", "Stage 2", {
        "FY2025": 12202, "FY2024": 17094, "FY2023": 13154, "FY2022": 15223, "FY2021": 19690,
        "FY2020": 13216, "FY2019": 8869, "FY2018": 7090,
    }),
    ("DATA", "Stage 3", {
        "FY2025": 18589, "FY2024": 6534, "FY2023": 2939, "FY2022": 128, "FY2021": 124,
        "FY2020": 0, "FY2019": 372, "FY2018": 19,
    }),
    ("TOTAL", "Gross loans and advances to clients", {
        "FY2025": 639793, "FY2024": 586208, "FY2023": 487929, "FY2022": 447869, "FY2021": 422328,
        "FY2020": 326425, "FY2019": 203814, "FY2018": 132517, "FY2017": 94198, "FY2016": 48137,
    }),
    ("SECTION", "Impairment allowances by IFRS 9 stage", {}),
    ("DATA", "Stage 1", {
        "FY2025": -115, "FY2024": -102, "FY2023": -67, "FY2022": -111, "FY2021": -106,
        "FY2020": -94, "FY2019": -7, "FY2018": -10,
    }),
    ("DATA", "Stage 2", {
        "FY2025": -56, "FY2024": -164, "FY2023": -218, "FY2022": -67, "FY2021": -56,
        "FY2020": -77, "FY2019": 0, "FY2018": 0,
    }),
    ("DATA", "Stage 3", {
        "FY2025": -41, "FY2024": -49, "FY2023": -20, "FY2022": -16, "FY2021": -6,
        "FY2020": 0, "FY2019": 0, "FY2018": -19,
    }),
    ("TOTAL", "Total impairment allowances", {
        "FY2025": -212, "FY2024": -315, "FY2023": -305, "FY2022": -194, "FY2021": -168,
        "FY2020": -171, "FY2019": -7, "FY2018": -29, "FY2017": 0, "FY2016": 0,
    }),
    ("SECTION", "Loans and advances to clients, net carrying amount by IFRS 9 stage", {}),
    ("DATA", "Stage 1", {
        "FY2025": 608887, "FY2024": 562478, "FY2023": 471769, "FY2022": 432407, "FY2021": 402408,
        "FY2020": 313115, "FY2019": 194566, "FY2018": 125398,
    }),
    ("DATA", "Stage 2", {
        "FY2025": 12146, "FY2024": 16930, "FY2023": 12936, "FY2022": 15156, "FY2021": 19634,
        "FY2020": 13139, "FY2019": 8869, "FY2018": 7090,
    }),
    ("DATA", "Stage 3", {
        "FY2025": 18548, "FY2024": 6485, "FY2023": 2919, "FY2022": 112, "FY2021": 118,
        "FY2020": 0, "FY2019": 372, "FY2018": 0,
    }),
    ("TOTAL", "Net loans and advances to clients", {
        "FY2025": 639581, "FY2024": 585893, "FY2023": 487624, "FY2022": 447675, "FY2021": 422160,
        "FY2020": 326254, "FY2019": 203807, "FY2018": 132488, "FY2017": 94198, "FY2016": 48137,
    }),
    ("SECTION", "Coverage ratios (each year's own disclosed figure)", {}),
    ("DATA", "Stage 3 coverage ratio", {
        "FY2025": "0.221%", "FY2024": "0.750%", "FY2023": "0.680%", "FY2022": "12.500%", "FY2021": "4.839%",
        "FY2019": "0.000%", "FY2018": "100.000%",
    }),
    ("DATA", "Total coverage ratio", {
        "FY2025": "0.033%", "FY2024": "0.054%", "FY2023": "0.063%", "FY2022": "0.043%", "FY2021": "0.040%",
        "FY2020": "0.052%", "FY2019": "0.003%", "FY2018": "0.022%", "FY2017": "0.000%", "FY2016": "0.000%",
    }),
]

bw.add_asset_quality_sheet(
    title="Hampden & Co Plc — Asset Quality",
    subtitle="Loans and advances to clients by IFRS 9 stage, as disclosed in the Bank's own impairment note",
    rows=aq_rows,
    sources_text=(
        "Sources - Hampden & Co Plc's own impairment note ('Note 12: Impairment of loans and advances to clients' "
        "from FY2020 onward; 'Note 18: Financial risk management' pre-2020), 'Impairments by stage' table:\n"
        f"FY2025/FY2024: Hampden Bank Annual Report and Financial Statements 2025, p.61 - {AR2025_URL}\n"
        f"FY2023/FY2022: Hampden & Co Plc Annual Report and Financial Statements 2023, p.57 - {AR2023_URL}\n"
        f"FY2021: Hampden & Co Plc Annual Report and Financial Statements 2021, p.72 - {AR2021_URL}\n"
        f"FY2020/FY2019: Hampden & Co Plc Annual Report and Financial Statements 2020, p.70-72 (Note 12.1, carries "
        f"both years' own stage-level figures) - {AR2020_URL}\n"
        f"FY2018: Hampden & Co Plc Annual Report and Financial Statements 2019, p.55-56 (Note 18, FY2018 comparative "
        f"column) - {AR2019_URL}. The FY2018 Annual Report's own Note 18 (p.47-48) prints a materially different, "
        "internally-inconsistent gross carrying amount rollforward for this same balance (closing total GBP159,564k, "
        "which does not reconcile to that year's own GBP132,488k Balance Sheet net loans and advances figure even "
        "after adding back the disclosed GBP29k impairment allowance) - apparently blending drawn balances with "
        "undrawn loan commitments despite its own row label. The FY2019 report's own FY2018 comparative column "
        "(used here) is internally consistent and ties exactly to the FY2018 Balance Sheet, so it is used in "
        "preference to the FY2018 report's own figure.\n"
        f"FY2017: Hampden & Co Plc Annual Report and Financial Statements 2017, p.40-41 (Note 16, 'No impairment "
        f"provision has been recognised against the loans and advances to clients in the current or prior year') - {AR2017_URL}\n"
        f"FY2016: Hampden & Co Plc Annual Report and Financial Statements 2016, p.31-32 (Note 15, same 'no impairment "
        f"provision' statement) - {AR2016_URL}\n"
        "FY2016 and FY2017 pre-date the Bank's 1 January 2018 IFRS 9 adoption (IAS 39 basis) - no stage split exists "
        "for either year and no impairment provision was ever recognised in either year, so gross equals net exactly "
        "and no Stage 1/2/3 breakdown is shown for those two years. "
        "Net loans and advances to clients ties exactly to the Balance Sheet's own 'Loans and advances to clients' "
        "line for every year. The Bank does not disclose gross/net exposure by product type separately from this "
        "IFRS 9 stage split - all lending is presented as a single 'loans and advances to clients' category."
    ),
    first_col_width=56,
    source_height=190,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, f"{unit}" if unit else None,
                         rows_data, sources_text, note=note, first_col_width=44, source_height=130)


metric(
    "CET1 Capital", "£'000",
    [("Common Equity Tier 1 (CET1) capital", {
        "FY2023": 74173, "FY2022": 65731, "FY2021": 55264,
        "FY2020": 49587, "FY2019": 42522, "FY2018": 36942,
    })],
    p3_sources(),
    note="No Additional Tier 1 or Tier 2 capital any year - CET1 = Tier 1 = Total Capital throughout. FY2018 sourced "
         "from the FY2019 Pillar 3 document's own comparative column (no standalone FY2018 document exists). "
         "Not disclosed for FY2024/FY2025 (no standalone Pillar 3 document located for either year) or FY2016/FY2017 "
         "(no Pillar 3 document exists at all for either year, confirmed via a full domain Wayback CDX search).",
)

metric(
    "CET1 Ratio", "%",
    [("Common Equity Tier 1 (CET1) ratio", {
        "FY2023": "20.53%", "FY2022": "20.77%", "FY2021": "19%",
        "FY2020": "20.2%", "FY2019": "26.1%", "FY2018": "41%",
    })],
    p3_sources(),
    note="FY2018 sourced from the FY2019 Pillar 3 document's own comparative column as a rounded whole percentage "
         "(that document does not carry a KM1-style appendix for its comparative year). Not disclosed for "
         "FY2024/FY2025 (no standalone Pillar 3 document located for either year) or FY2016/FY2017 (no Pillar 3 "
         "document exists at all for either year).",
)

metric(
    "Tier 1 Capital", "£'000",
    [("Tier 1 capital", {
        "FY2023": 74173, "FY2022": 65731, "FY2021": 55264,
        "FY2020": 49587, "FY2019": 42522, "FY2018": 36942,
    })],
    p3_sources(),
    note="No AT1 capital any year - Tier 1 = CET1 = Total Capital throughout. FY2018 sourced from the FY2019 Pillar 3 "
         "document's own comparative column. Not disclosed for FY2024/FY2025 or FY2016/FY2017.",
)

metric(
    "Tier 1 Ratio", "%",
    [("Tier 1 ratio", {
        "FY2023": "20.53%", "FY2022": "20.77%", "FY2021": "19%",
        "FY2020": "20.2%", "FY2019": "26.1%", "FY2018": "41%",
    })],
    p3_sources(),
    note="Not disclosed for FY2024/FY2025 (no standalone Pillar 3 document located for either year) or FY2016/FY2017 "
         "(no Pillar 3 document exists at all for either year).",
)

metric(
    "Total Capital", "£'000",
    [("Total capital", {
        "FY2023": 74173, "FY2022": 65731, "FY2021": 55264,
        "FY2020": 49587, "FY2019": 42522, "FY2018": 36942,
    })],
    p3_sources(),
    note="Not disclosed in £'000 terms for FY2024/FY2025 - only the ratio (below) is given. Not disclosed at all for "
         "FY2016/FY2017.",
)

metric(
    "Total Capital Ratio", "%",
    [("Total capital ratio", {
        "FY2025": "17%", "FY2024": "17%", "FY2023": "20.53%", "FY2022": "20.77%", "FY2021": "19%",
        "FY2020": "20.2%", "FY2019": "26.1%", "FY2018": "41%",
    })],
    p3_sources(),
    note="FY2024/FY2025 sourced from each year's own Annual Report Key Performance Indicators table (the only "
         "capital metric given there) rather than a standalone Pillar 3 document - none was found published for "
         "either year. FY2018 sourced from the FY2019 Pillar 3 document's own comparative column. Not disclosed at "
         "all for FY2016/FY2017.",
)

metric(
    "Total RWAs", "£'000",
    [("Total risk-weighted exposure amount", {
        "FY2023": 361317, "FY2022": 316422, "FY2021": 285422,
        "FY2020": 245595, "FY2019": 163065, "FY2018": 91188,
    })],
    p3_sources(),
    note="FY2020/FY2019 figures are directly disclosed (the FY2020 Pillar 3 document's own KM1-style appendix). "
         "FY2018 is derived (not directly disclosed) as that year's own disclosed Pillar 1 capital requirement "
         "(GBP7,295k, per the FY2019 Pillar 3 document's comparative column) divided by 8%, since only the capital "
         "requirement - not the RWA total itself - is stated under that document's pre-KM1 format for its "
         "comparative year. Not disclosed for FY2024/FY2025 or FY2016/FY2017.",
)

rwa_rows = [
    ("DATA", "Credit risk (excluding CCR)", {
        "FY2023": 317736, "FY2022": 284658, "FY2021": 269622,
        "FY2020": 233745, "FY2019": 155627, "FY2018": 87630,
    }),
    ("DATA", "Counterparty credit risk (CCR)", {
        "FY2023": 1549, "FY2022": 2826,
    }),
    ("DATA", "Of which credit valuation adjustment (CVA)", {
        "FY2023": 738, "FY2022": 1750,
    }),
    ("DATA", "Of which other CCR", {
        "FY2023": 811, "FY2022": 1076,
    }),
    ("DATA", "Market risk (FX)", {
        "FY2021": 0, "FY2020": 0, "FY2019": 0,
    }),
    ("DATA", "Operational risk", {
        "FY2023": 42032, "FY2022": 28938, "FY2021": 15800,
        "FY2020": 11850, "FY2019": 7438, "FY2018": 3562,
    }),
    ("TOTAL", "Total risk-weighted exposure amount", {
        "FY2023": 361317, "FY2022": 316422, "FY2021": 285422,
        "FY2020": 245595, "FY2019": 163065, "FY2018": 91192,
    }),
]

bw.add_rwa_breakdown_sheet(
    title="Hampden & Co Plc — RWA Breakdown",
    subtitle="Pillar 1 risk weighted exposure amounts by risk category",
    rows=rwa_rows,
    sources_text=(
        "Sources - Hampden & Co Plc Pillar 3 Disclosures:\n"
        f"FY2023/FY2022: Table UK OV1 'Overview of risk weighted exposure amounts', Pillar 3 Disclosures for the "
        f"year ended 31 December 2023, p.16 - {P3_2023_URL}\n"
        f"FY2021: Table 6 'Pillar 1 capital requirement' and Table 7 'Risk weighted assets and Pillar 1 credit "
        f"risk capital requirement by exposure class', Pillar 3 Disclosures for the year ended 31 December 2021, "
        f"p.16 - {P3_2021_URL}. FY2021's Operational risk RWA (15,800) is derived from the disclosed capital "
        "requirement (1,264) divided by 8%, since only the capital requirement (not the RWA itself) is stated "
        "under this pre-UK-KM1-format disclosure; FY2021 also does not separately disclose a CCR/CVA split (not "
        "itemised in this basis) - left blank rather than assumed zero, unlike Market risk which the document "
        "explicitly states is nil.\n"
        f"FY2020/FY2019: Table 7 'Risk weighted assets and Pillar 1 credit risk capital requirement by exposure "
        f"class' (directly discloses Credit risk RWA), Pillar 3 disclosures for the year ended 31 December 2020, "
        f"p.16 - {P3_2020_URL}. Operational risk RWA is derived (capital requirement divided by 8%: GBP948k/GBP595k "
        "respectively) since only the capital requirement is separately stated. Market risk explicitly stated as "
        "nil both years (the Bank has no material FX position risk exposure). No CCR/CVA split itemised in this "
        "pre-KM1 basis - left blank rather than assumed zero.\n"
        f"FY2018: Table 6 'Pillar 1 capital requirement' and Table 7 credit risk breakdown, Pillar 3 Disclosures "
        f"for the year ended 31 December 2019 (FY2018 comparative column), p.15-16 - {P3_2019_URL}. Credit risk RWA "
        "(87,630) is directly disclosed; Operational risk RWA (3,562) is derived from the disclosed capital "
        "requirement (285) divided by 8%. This breakdown's own component sum (91,192) differs by GBP4k from the "
        "Total RWAs metric sheet's own FY2018 figure (91,188, derived from the aggregate Pillar 1 capital "
        "requirement of 7,295 divided by 8%) - both are derivations from disclosed capital requirements rounded at "
        "different stages, and the GBP4k gap is not forced to reconcile.\n"
        "Not disclosed for FY2024/FY2025 (no standalone Pillar 3 document located for either year, consistent "
        "with the pre-existing Total RWAs sheet) or FY2016/FY2017 (no Pillar 3 document exists at all for either "
        "year). Every year's Total ties exactly to the pre-existing Total RWAs metric sheet, except FY2018 as "
        "noted above."
    ),
    first_col_width=52,
    source_height=190,
    unit_suffix=" (£'000)",
)

metric(
    "Leverage Ratio", "%",
    [("Leverage ratio (excluding claims on central banks, FY2022-FY2023)", {
        "FY2023": "8.36%", "FY2022": "8.72%",
    }),
     ("Leverage ratio (FY2021 basis, as originally disclosed)", {
        "FY2021": "7%",
    }),
     ("Leverage ratio (FY2019-FY2020, UK leverage ratio exempt basis)", {
        "FY2020": "8.2%", "FY2019": "8.6%",
    }),
     ("Leverage ratio (FY2018, as originally disclosed)", {
        "FY2018": "11%",
    })],
    p3_sources(),
    note="FY2021's pre-UK-KM1-format disclosure does not specify whether central-bank claims are excluded - shown "
         "on its own row rather than merged with the later, explicitly-labelled basis. FY2020/FY2019 figures "
         "(8.2%/8.6%) are the more granular KM1-style-appendix figures from the FY2020 Pillar 3 document; that "
         "document's own main-text narrative rounds these to 8%/9%, and the FY2019 Pillar 3 document's own contemporaneous "
         "figure for FY2019 was also rounded to 9% - the more precise comparative figure is preferred here. FY2018 is "
         "only available as a rounded whole percentage (11%), from the FY2019 Pillar 3 document's own comparative "
         "column (no KM1-style appendix exists for that comparative year). Not disclosed for FY2024/FY2025 or "
         "FY2016/FY2017.",
)

metric(
    "LCR", "%",
    [("Liquidity Coverage Ratio (12-month average)", {
        "FY2023": "262%", "FY2022": "213%",
    }),
     ("Liquidity Coverage Ratio (point-in-time, FY2018-FY2021 basis)", {
        "FY2021": "180%", "FY2020": "286%", "FY2019": "467%", "FY2018": "509%",
    })],
    p3_sources(),
    note="FY2018-FY2021's disclosures predate the UK KM1 format and do not state an averaging basis (later years "
         "use a 12-month average per KM1) - shown on its own row rather than assumed equivalent. FY2018 sourced "
         "from the FY2019 Pillar 3 document's own comparative column. Not disclosed for FY2024/FY2025 or "
         "FY2016/FY2017.",
)

metric(
    "NSFR", "%",
    [("Net Stable Funding Ratio (4-quarter average)", {
        "FY2023": "186%", "FY2022": "186%",
    })],
    p3_sources(),
    note="Not disclosed for FY2021 or earlier - none of the Bank's Pillar 3 reports back to and including FY2019 "
         "contain an NSFR section at all, consistent with the UK's NSFR reporting requirement only commencing "
         "during 2022 for firms of this size (the same commencement pattern already seen at Ghana International "
         "Bank). Not disclosed for FY2024/FY2025 or FY2016-FY2018 (no Pillar 3 document exists at all for "
         "FY2016/FY2017; the FY2019 document's own FY2018 comparative column likewise carries no NSFR section).",
)

bw.add_not_disclosed_metric_sheets(
    ["MREL Ratio"],
    p3_sources(),
    per_note={
        "MREL Ratio": "Not publicly disclosed for any year - no MREL-related content appears in any Pillar 3 "
                       "document reviewed (FY2018-FY2023); Hampden & Co Plc does not appear to be a UK "
                       "resolution entity subject to a standalone MREL requirement.",
    },
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {
            "FY2025": 1227049, "FY2024": 1089302, "FY2023": 946163, "FY2022": 874485, "FY2021": 756181,
            "FY2020": 556125, "FY2019": 458106, "FY2018": 309210, "FY2017": 240196, "FY2016": 180573,
        }),
        ("Loans and advances to clients", {
            "FY2025": 639581, "FY2024": 585893, "FY2023": 487624, "FY2022": 447675, "FY2021": 422160,
            "FY2020": 326254, "FY2019": 203807, "FY2018": 132488, "FY2017": 94198, "FY2016": 48137,
        }),
        ("Deposits from clients", {
            "FY2025": 1123743, "FY2024": 990720, "FY2023": 857506, "FY2022": 796049, "FY2021": 695590,
            "FY2020": 501163, "FY2019": 409374, "FY2018": 267483, "FY2017": 193926, "FY2016": 143415,
        }),
        ("Total equity", {
            "FY2025": 92036, "FY2024": 90108, "FY2023": 82424, "FY2022": 72852, "FY2021": 57302,
            "FY2020": 51339, "FY2019": 44864, "FY2018": 39852, "FY2017": 43723, "FY2016": 34896,
        }),
    ],
    balance_sheet_unit="£'000",
    income_statement_totals=[
        ("Total income", {
            "FY2025": 31463, "FY2024": 30324, "FY2023": 31187, "FY2022": 22856, "FY2021": 13207,
            "FY2020": 10237, "FY2019": 8683, "FY2018": 6364, "FY2017": 3905, "FY2016": 1639,
        }),
        ("Operating expenses", {
            "FY2025": -24617, "FY2024": -22131, "FY2023": -21941, "FY2022": -20782, "FY2021": -16182,
            "FY2020": -14200, "FY2019": -14239, "FY2018": -12143, "FY2017": -10265, "FY2016": -7898,
        }),
        ("Profit/(loss) for the year", {
            "FY2025": 4989, "FY2024": 9111, "FY2023": 8107, "FY2022": 6864, "FY2021": -2970,
            "FY2020": -4079, "FY2019": -5533, "FY2018": -5577, "FY2017": -6360, "FY2016": -6259,
        }),
    ],
    income_statement_unit="£'000",
    equity_changes_totals=[
        ("Opening equity", {
            "FY2025": 90108, "FY2024": 82424, "FY2023": 72852, "FY2022": 57302, "FY2021": 51339,
            "FY2020": 44864, "FY2019": 39852, "FY2018": 43723, "FY2017": 34896, "FY2016": 37053,
        }),
        ("Profit/(loss) for the year", {
            "FY2025": 4989, "FY2024": 9111, "FY2023": 8107, "FY2022": 6864, "FY2021": -2970,
            "FY2020": -4079, "FY2019": -5533, "FY2018": -5577, "FY2017": -6360, "FY2016": -6259,
        }),
        ("Other equity movements, net", {
            "FY2025": -3061, "FY2024": -1427, "FY2023": 1465, "FY2022": 8686, "FY2021": 8933,
            "FY2020": 10554, "FY2019": 10545, "FY2018": 1706, "FY2017": 15187, "FY2016": 4102,
        }),
        ("Closing equity", {
            "FY2025": 92036, "FY2024": 90108, "FY2023": 82424, "FY2022": 72852, "FY2021": 57302,
            "FY2020": 51339, "FY2019": 44864, "FY2018": 39852, "FY2017": 43723, "FY2016": 34896,
        }),
    ],
    equity_changes_unit="£'000",
    cash_flow_totals=[
        ("Net cash from/(used in) operating activities", {
            "FY2025": 175034, "FY2024": 85876, "FY2023": -14109, "FY2022": 50082, "FY2021": 61740,
            "FY2020": -49545, "FY2019": 46097, "FY2018": 20701, "FY2017": 7208, "FY2016": 59119,
        }),
        ("Net cash from/(used in) investing activities", {
            "FY2025": -142233, "FY2024": -164582, "FY2023": -69327, "FY2022": -977, "FY2021": -1145,
            "FY2020": -160, "FY2019": -457, "FY2018": -248, "FY2017": -866, "FY2016": -25,
        }),
        ("Net cash from/(used in) financing activities", {
            "FY2025": -3098, "FY2024": -2012, "FY2023": 1540, "FY2022": 7468, "FY2021": 7446,
            "FY2020": 9331, "FY2019": 9245, "FY2018": 787, "FY2017": 14960, "FY2016": 3978,
        }),
        ("Cash and cash equivalents at end of year", {
            "FY2025": 154351, "FY2024": 125315, "FY2023": 207363, "FY2022": 294851, "FY2021": 228768,
            "FY2020": 160960, "FY2019": 200970, "FY2018": 148975, "FY2017": 125284, "FY2016": 108931,
        }),
    ],
    cash_flow_unit="£'000",
    ratios=[
        ("CET1 Ratio", {
            "FY2023": "20.53%", "FY2022": "20.77%", "FY2021": "19%",
            "FY2020": "20.2%", "FY2019": "26.1%", "FY2018": "41%",
        }),
        ("Tier 1 Ratio", {
            "FY2023": "20.53%", "FY2022": "20.77%", "FY2021": "19%",
            "FY2020": "20.2%", "FY2019": "26.1%", "FY2018": "41%",
        }),
        ("Total Capital Ratio", {
            "FY2025": "17%", "FY2024": "17%", "FY2023": "20.53%", "FY2022": "20.77%", "FY2021": "19%",
            "FY2020": "20.2%", "FY2019": "26.1%", "FY2018": "41%",
        }),
        ("LCR", {
            "FY2023": "262%", "FY2022": "213%", "FY2021": "180%",
            "FY2020": "286%", "FY2019": "467%", "FY2018": "509%",
        }),
        ("NSFR", {
            "FY2023": "186%", "FY2022": "186%",
        }),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own "
         "source citation for the underlying document/page. FY2024/FY2025 ratios other than Total Capital Ratio "
         "are blank - no standalone Pillar 3 document was found published for either year. FY2016/FY2017 ratios "
         "are blank throughout - no Pillar 3 document exists at all for either year.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/HAMPDEN & CO FINANCIALS.xlsx")
