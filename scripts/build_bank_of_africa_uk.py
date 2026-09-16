import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021", "FY2020", "FY2019",
         "FY2018", "FY2017", "FY2016", "FY2015", "FY2014"]  # most recent first

# Companies House annual accounts filings (company 05321714, formerly BMCE Bank
# International Plc / MediCapital Bank Plc). All filings are fully scanned
# (image-only) - every figure below was OCR'd/read visually and cross-checked
# against the adjoining year's own comparative column.
AR2025_URL = "https://find-and-update.company-information.service.gov.uk/company/05321714/filing-history/MzUxODk4NzcyM2FkaXF6a2N4/document?format=pdf&download=0"
AR2023_URL = "https://find-and-update.company-information.service.gov.uk/company/05321714/filing-history/MzQzODczNDQ5OWFkaXF6a2N4/document?format=pdf&download=0"
AR2022_URL = "https://find-and-update.company-information.service.gov.uk/company/05321714/filing-history/MzM5NDE3NzEwN2FkaXF6a2N4/document?format=pdf&download=0"
AR2021_URL = "https://find-and-update.company-information.service.gov.uk/company/05321714/filing-history/MzM1NDAwMjc2N2FkaXF6a2N4/document?format=pdf&download=0"
# HD-017 extension (FY2014-FY2020): additional Companies House annual accounts
# filings, same fully-scanned/image-only pattern as above.
AR2020_URL = "https://find-and-update.company-information.service.gov.uk/company/05321714/filing-history/MzMyODY1ODY3N2FkaXF6a2N4/document?format=pdf&download=0"
AR2019_URL = "https://find-and-update.company-information.service.gov.uk/company/05321714/filing-history/MzI3MzkxNzgyN2FkaXF6a2N4/document?format=pdf&download=0"
AR2018_URL = "https://find-and-update.company-information.service.gov.uk/company/05321714/filing-history/MzIzNTgyNTYxOWFkaXF6a2N4/document?format=pdf&download=0"
AR2017_URL = "https://find-and-update.company-information.service.gov.uk/company/05321714/filing-history/MzIwMzc5MjgxOGFkaXF6a2N4/document?format=pdf&download=0"
AR2016_URL = "https://find-and-update.company-information.service.gov.uk/company/05321714/filing-history/MzE3NDg0MjU5MGFkaXF6a2N4/document?format=pdf&download=0"
AR2014_URL = "https://find-and-update.company-information.service.gov.uk/company/05321714/filing-history/MzEyMjYyNzE2M2FkaXF6a2N4/document?format=pdf&download=0"

# Standalone Pillar 3 disclosures, found on the Bank's own site
# (bankofafricaunitedkingdom.co.uk/finances.html) - text-native PDFs, no OCR
# needed. No FY2021 or FY2025 edition exists (site's earliest is FY2022; FY2025
# not yet published).
P3_2022_URL = "https://www.bankofafricaunitedkingdom.co.uk/pdfs/finances/BOA_UK_Pillar_III_2022.pdf"
P3_2023_URL = "https://www.bankofafricaunitedkingdom.co.uk/pdfs/finances/Pillar3-Disclosures-2023.pdf"
P3_2024_URL = "https://www.bankofafricaunitedkingdom.co.uk/pdfs/finances/Pillar3-Disclosures-2024.pdf"
BOA_FINANCES_URL = "https://www.bankofafricaunitedkingdom.co.uk/finances.html"
# HD-017 extension: standalone Pillar 3 disclosures for FY2015 and FY2017 -
# not linked from the bank's current site, but archived by the Wayback Machine
# from an earlier version of the site (bmcebankint.com era). Both are
# text-native PDFs. FY2015's own edition also carries an FY2014 comparative
# column, and FY2017's own edition carries an FY2016 comparative column - used
# to fill the FY2016 Pillar 3 gap the same way this project already fills
# comparative-column gaps elsewhere (e.g. FY2021 above, sourced from FY2022's
# own comparative rather than a dedicated FY2021 document). FY2018-FY2020 have
# no equivalent standalone Pillar 3 document anywhere in the Wayback archive of
# either domain (bankofafricaunitedkingdom.co.uk or bmcebankint.com) - a
# genuine archive gap, confirmed by HD-002's deep dive and re-confirmed here
# with a fresh CDX search before treating it as unobtainable; left blank on
# every Pillar 3 sheet for those 3 years rather than guessed.
# 2026-09-16 UPDATE: both of these are LIVE again on the bank's own site. They
# were not deleted, they moved - from /assets/<n>/ to /pdfs/finances/, the same
# directory the FY2022-FY2024 editions above sit in. Both live URLs were fetched
# in full and confirmed: FY2017 = 1,164,813 bytes / 32pp, cover "2017 PILLAR III
# DISCLOSURES"; FY2015 = 430,862 bytes / 5pp, cover "BMCE BANK INTERNATIONAL plc
# PILLAR 3 DISCLOSURES FOR THE YEAR 2015" - both "Company Registration N°5321714
# (England and Wales)", i.e. the UK entity, not the Moroccan parent. The primary
# citation is therefore the live URL; the Wayback captures are kept below as the
# archival fallback and are NOT deleted.
#
# The FY2017 Wayback capture must not be promoted back to primary: it is
# TRUNCATED at exactly 1,048,576 bytes (the Wayback per-capture 1 MiB limit)
# against the live file's 1,164,813 - re-checked 2026-09-16 in all three
# playback forms (bare, if_ and id_), all three return the identical 1 MiB
# truncated body. The tail of the document is missing.
P3_2015_URL = "https://www.bankofafricaunitedkingdom.co.uk/pdfs/finances/BMCE___Pillar_3_disclosures____2015.pdf"
P3_2017_URL = "https://www.bankofafricaunitedkingdom.co.uk/pdfs/finances/BMCE___Pillar_III_VF___31122017.pdf"
P3_2015_WAYBACK = "https://web.archive.org/web/20220519121800id_/https://www.bankofafricaunitedkingdom.co.uk/assets/0/BMCE___Pillar_3_disclosures____2015.pdf"
P3_2017_WAYBACK = "https://web.archive.org/web/20220519120942/https://www.bankofafricaunitedkingdom.co.uk/assets/239/BMCE___Pillar_III_VF___31122017.pdf"

ENTITY_NOTE = (
    "Entity: BANK OF AFRICA United Kingdom Plc (FRN 454750, company 05321714, formerly "
    "BMCE Bank International Plc / MediCapital Bank Plc), a UK-incorporated subsidiary of "
    "Bank of Africa S.A. (Morocco). Reports in GBP; no FX conversion needed. Does NOT take "
    "the FRS 101/102 cash-flow-statement exemption - a full Statement of Cash Flows exists "
    "every year. All 11 Companies House filings used (FY2014-FY2025) are fully scanned/"
    "image-only; every figure was read from the rendered page image and cross-checked "
    "against the following year's own comparative column (all ties confirmed exact across "
    "the chain: FY2014 closing = FY2015 opening = 100,949; FY2016 closing = FY2017 opening = "
    "117,350; FY2017 closing = FY2018 opening = 74,382 (2016 comparative in the FY2017 "
    "Annual Report reclassifies the Group subordinated debt cash movement from operating to "
    "financing activities vs. how the FY2016 Annual Report itself presented it - a genuine "
    "presentational reclassification, not an error; both are used exactly as each report "
    "states them); FY2021 closing = FY2022 opening = 87,968; FY2022 closing = FY2023 "
    "opening = 68,544; FY2023 closing = FY2024 opening = 54,575; FY2024 closing = FY2025 "
    "opening = 51,070. HD-017 extension (2026-09-05, FY2014-FY2020): FY2019 and FY2020 use "
    "AR2020's own primary/comparative pair (FY2019 shown there as 'Restated' - see the "
    "prior-period-adjustment note below); FY2018 and FY2017 use AR2018's own primary/"
    "comparative pair; FY2016 and FY2015 use AR2016's own primary/comparative pair; FY2014 "
    "uses AR2014 standalone (its own FY2013 comparative not needed, since FY2014 is this "
    "project's confirmed floor for this entity per HD-002).\n\n"
    "DATA QUALITY NOTE - genuine restatement, distinct from an arithmetic-error correction: "
    "the FY2023 Annual Report restates FY2022's comparative Statement of Changes in Equity "
    "(loss for the year (GBP3,839k) as originally reported in the FY2022 Annual Report vs. "
    "(GBP4,556k) restated; closing equity GBP75,751k vs. GBP75,034k restated) and, within the "
    "Cash Flow Statement itself, restates two line items within operating activities (Change "
    "in operating liabilities GBP(35,633)k original vs. GBP(35,509)k restated; Other non-cash "
    "items GBP(5,399)k vs. GBP(5,512)k restated) - the operating-activities TOTAL is "
    "unaffected (GBP(27,463)k both times) and the closing cash balance is unaffected. The "
    "FY2022 Independent Auditor's Report itself references 'prior year adjustments and "
    "ongoing regulatory investigation' as an audit risk factor, consistent with this being a "
    "genuine, disclosed restatement rather than a transcription error on our part. This "
    "workbook uses each year's own originally-reported cash flow figures as the primary "
    "column (project convention), with the restatement noted here rather than silently "
    "blended in.\n\n"
    "SECOND DATA QUALITY NOTE, found during the HD-017 extension - a further, independent "
    "restatement break: this workbook's existing FY2021 opening equity (Other reserves "
    "GBP1,625k, Total GBP82,378k, sourced from the FY2022 Annual Report's own FY2021 "
    "comparative) does not tie to the FY2020 Annual Report's own closing balance at 31 "
    "December 2020 (Other reserves GBP1,890k, Total GBP82,643k - a GBP265k break, entirely "
    "within Other reserves). Both are used exactly as each report states them; not "
    "reconciled further. A third, larger restatement is separately documented on the "
    "Statement of Changes in Equity sheet itself: the FY2018 Annual Report's own 'Impact of "
    "correction of errors' adjustments to the FY2017 opening and closing equity positions "
    "(the FY2017 Annual Report's own, non-error primary figures - profit for the year "
    "GBP5,510k, closing equity GBP77,889k - are used as this workbook's FY2017 primary "
    "column, per project convention; the FY2018 Annual Report's restated FY2017 comparative "
    "shows profit GBP4,933k and closing equity GBP76,434k instead).\n\n"
    "BASEL III / IFRS 9 TRANSITION NOTE: FY2014-FY2017 Pillar 3 disclosures predate this "
    "entity's adoption of the explicit 'CET1' label (first used in the FY2017 Pillar 3 "
    "document, which states Tier 1 Capital 'is comprised entirely of Common Equity Tier 1 "
    "capital (CET1)') - the FY2014 and FY2015 Pillar 3 documents disclose only 'Tier 1 "
    "capital' without using the CET1 term. Structurally unchanged from later years (wholly "
    "CET1, no AT1 instruments), so CET1 is treated as equal to Tier 1 Capital for FY2014-"
    "FY2017 too, consistent with how every other year in this workbook is presented, but "
    "flagged here per HD-017's instruction on Basel-era terminology shifts. Separately, the "
    "FY2014 and FY2015 Pillar 3 documents' own 'Tier 2 capital' row is arithmetically Tier 1 "
    "Capital + Subordinated debt (principal) - i.e. it is actually Total Capital / Own Funds, "
    "not Tier 2 alone (Tier 2 for this entity is just the subordinated debt); reproduced here "
    "under this workbook's 'Total Capital' metric, treating the source document's own row "
    "label as an apparent labelling error rather than following it literally. IFRS 9 "
    "(replacing IAS 39's incurred-loss model) was adopted 1 January 2018 - FY2014-FY2017 "
    "Asset Quality figures use the entity's own pre-IFRS 9 individual-impairment disclosure "
    "format (no IFRS 9 stage split exists for those years), presented in a separate section "
    "of the Asset Quality sheet from FY2018 onward's stage-based figures. IFRS 16 (leases) "
    "was adopted 1 January 2019 - FY2014-FY2018 have no Right-of-use Assets/lease-related "
    "figures, consistent with pre-adoption presentation."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are Bank of Africa United Kingdom Plc's own Statement of Cash "
    "Flows, GBP'000:\n"
    f"FY2025 & FY2024: Annual Report and Financial Statements 2025, p.42 (Statement of Cash Flows) - {AR2025_URL}\n"
    f"FY2023 (& FY2022 restated comparative, see note): Annual Report and Financial Statements 2023, p.43 (Statement of cash flows) - {AR2023_URL}\n"
    f"FY2022 (originally reported, used as primary column): Annual Report and Financial Statements 2022, p.42 (Statement of cash flows) - {AR2022_URL}\n"
    f"FY2021: Annual Report and Financial Statements 2022, p.42 (Statement of cash flows, FY2021 comparative column) - {AR2022_URL}\n"
    f"FY2020 (& FY2019 restated comparative, used as primary column - see note): Annual Report and Financial Statements 2020, p.34 - {AR2020_URL}\n"
    f"FY2018: Annual Report and Financial Statements 2018, p.28 - {AR2018_URL}\n"
    f"FY2017 (own primary column): Annual Report and Financial Statements 2017, p.27 - {AR2017_URL}\n"
    f"FY2016 (& FY2015 comparative, used as primary column): Annual Report and Financial Statements 2016, p.22 - {AR2016_URL}\n"
    f"FY2014: Annual Report and Financial Statements 2014, p.19 - {AR2014_URL}\n\n"
    + ENTITY_NOTE
)


def p3_sources(extra=""):
    return (
        "Sources - Bank of Africa United Kingdom Plc, own entity-level Pillar 3 disclosures "
        "(KM1 Key Metrics), GBP'000 unless stated:\n"
        f"FY2024: Pillar 3 Disclosures 2024, p.6 (Key Metrics) and p.20 (composition of capital resources table) - {P3_2024_URL}\n"
        f"FY2023: Pillar 3 Disclosures 2023, p.6 (Key Metrics) and p.20 (composition of capital resources table) - {P3_2023_URL}\n"
        f"FY2022: Pillar 3 Disclosures 2022, p.17 (composition of capital resources table, as originally published) - {P3_2022_URL}\n"
        f"FY2021: Pillar 3 Disclosures 2022, p.17 (composition of capital resources table, FY2021 comparative column) - {P3_2022_URL}\n"
        f"FY2025: no Pillar 3 edition published yet (as of this build) - Annual Report and Financial Statements 2025, p.23 (Capital Management) - {AR2025_URL}\n"
        f"FY2017: Pillar III Disclosures 2017, p.13 (Own Funds/Solvency ratio table) - {P3_2017_URL}\n"
        f"FY2016: Pillar III Disclosures 2017, p.13 (Own Funds/Solvency ratio table, FY2016 comparative column) - {P3_2017_URL}\n"
        f"FY2015: Pillar 3 Disclosures 2015, p.2 (Ratios table) - {P3_2015_URL}\n"
        f"FY2014: Pillar 3 Disclosures 2015, p.2 (Ratios table, FY2014 comparative column; also independently cross-checked against the FY2014 Annual Report's own Part III Pillar 3 Disclosures, p.64) - {P3_2015_URL}\n"
        f"SOURCE-URL NOTE (2026-09-16): the FY2015 and FY2017 editions were previously cited "
        f"via the Wayback Machine because they were no longer linked from the bank's site. They "
        f"are live again at the /pdfs/finances/ path above (moved from /assets/<n>/, not "
        f"withdrawn), re-fetched and re-read 2026-09-16 - FY2017 1,164,813 bytes/32pp, FY2015 "
        f"430,862 bytes/5pp, both bearing Company Registration N°5321714, the UK entity. The live "
        f"URLs are now cited in preference. Archival fallbacks, retained deliberately: FY2015 - "
        f"{P3_2015_WAYBACK}; FY2017 - {P3_2017_WAYBACK}. The FY2017 Wayback capture is TRUNCATED "
        f"at exactly 1,048,576 bytes (the Wayback 1 MiB per-capture limit) in every playback form "
        f"- bare, if_ and id_ alike - so it is recorded as provenance only and must not be "
        f"promoted back to the primary citation; use the live URL.\n"
        f"FY2018-FY2020: no standalone Pillar 3 document found anywhere in the Wayback Machine "
        "archive of either bankofafricaunitedkingdom.co.uk or its earlier bmcebankint.com "
        "domain (re-confirmed via a fresh CDX search during the HD-017 extension, consistent "
        "with HD-002's earlier finding) - a genuine archive gap, left blank rather than "
        "guessed."
        + extra
    )


bw = BankWorkbook(bank_name="Bank of Africa United Kingdom Plc", years=YEARS, header_color="3D5A80")

# ---------------------------------------------------------------
# Sheet: Balance Sheet
# ---------------------------------------------------------------
BALANCE_SHEET_PRESENTATION_NOTE = (
    "PRESENTATION NOTE: FY2025/FY2024 (Annual Report 2025) split Property, Plant and Equipment "
    "and Right-of-use Assets, and Goodwill and Other intangible assets, into separate lines; "
    "FY2023 (Annual Report 2023) and FY2022/FY2021/FY2020/FY2019 combine each of those "
    "pairs into a single 'Property, Plant and Equipment and Right-of-use Assets' line and a "
    "single 'Goodwill and other intangible assets' line - reproduced here as originally "
    "disclosed rather than artificially split. FY2023-2025 include a 'Provisions' line "
    "(introduced FY2023); FY2021-2022 have none. FY2025's Balance Sheet folds Collateral held "
    "with third parties into Other assets (same convention as the other statement sheets in "
    "this workbook). HD-017 extension: FY2018-FY2014 predate IFRS 16 (adopted 1 January 2019) "
    "so have no Right-of-use Assets line at all - their 'Property and equipment' values are "
    "shown on this sheet's 'Property, Plant and Equipment' row (a pure-PPE figure, not "
    "combined with ROU, since none exists for those years). FY2016/FY2015 (Annual Report "
    "2016) and FY2018 (Annual Report 2018) still separately disclose 'Financial investments "
    "- held to maturity'/'- Amortised cost' alongside '- available for sale'/'- FVOCI' - both "
    "map onto this sheet's existing Amortised Cost / FVOCI rows (the same underlying "
    "categories under IAS 39 and IFRS 9 respectively); FY2020/FY2019/FY2017/FY2014 disclose "
    "only the FVOCI/AFS category (no amortised-cost/HTM holdings those years - left blank, "
    "not zero, since the category is simply absent from the source balance sheet)."
)
BALANCE_SHEET_SOURCES = (
    "Sources - Bank of Africa United Kingdom Plc's own Statement of Financial Position, GBP'000:\n"
    f"FY2025 & FY2024: Annual Report and Financial Statements 2025, p.40 - {AR2025_URL}\n"
    f"FY2023 (& FY2022 restated comparative, not used - see note): Annual Report and Financial Statements 2023, p.41 - {AR2023_URL}\n"
    f"FY2022 (originally reported, used as primary column): Annual Report and Financial Statements 2022, p.40 - {AR2022_URL}\n"
    f"FY2021: Annual Report and Financial Statements 2022, p.40 (FY2021 comparative column) - {AR2022_URL}\n"
    f"FY2020 (& FY2019 restated comparative, used as primary column - see note): Annual Report and Financial Statements 2020, p.25 - {AR2020_URL}\n"
    f"FY2018 (& FY2017 comparative, used as primary column): Annual Report and Financial Statements 2018, p.25 - {AR2018_URL}\n"
    f"FY2017: Annual Report and Financial Statements 2017, p.25 (own primary column) - {AR2017_URL}\n"
    f"FY2016 (& FY2015 comparative, used as primary column): Annual Report and Financial Statements 2016, p.20 - {AR2016_URL}\n"
    f"FY2014: Annual Report and Financial Statements 2014, p.17 - {AR2014_URL}\n\n"
    + BALANCE_SHEET_PRESENTATION_NOTE + "\n\n" + ENTITY_NOTE
)

balance_sheet_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and balances with central banks", {"FY2025": 3145, "FY2024": 15397, "FY2023": 27447, "FY2022": 45655, "FY2021": 43395, "FY2020": 42930, "FY2019": 3108, "FY2018": 17698, "FY2017": 17489, "FY2016": 13339, "FY2015": 4369, "FY2014": 1887}),
    ("DATA", "Due from banks", {"FY2025": 112586, "FY2024": 66588, "FY2023": 40848, "FY2022": 90560, "FY2021": 121178, "FY2020": 138092, "FY2019": 85493, "FY2018": 157397, "FY2017": 120104, "FY2016": 149004, "FY2015": 136700, "FY2014": 123940}),
    ("DATA", "Derivative assets", {"FY2025": 993, "FY2024": 546, "FY2023": 766, "FY2022": 42, "FY2021": 89, "FY2020": 433, "FY2019": 254, "FY2018": 231, "FY2017": 1140, "FY2016": 32, "FY2015": 222, "FY2014": 15}),
    ("DATA", "Loans and advances to customers", {"FY2025": 41952, "FY2024": 28985, "FY2023": 28332, "FY2022": 148285, "FY2021": 162016, "FY2020": 173173, "FY2019": 215391, "FY2018": 211596, "FY2017": 207964, "FY2016": 175945, "FY2015": 167713, "FY2014": 149257}),
    ("DATA", "Financial investments - Amortised Cost", {"FY2025": 66165, "FY2024": 80814, "FY2023": 82889, "FY2022": 89665, "FY2021": 87687, "FY2018": 48545, "FY2016": 16846, "FY2015": 7337}),
    ("DATA", "Financial investments - FVOCI", {"FY2025": 63507, "FY2024": 57583, "FY2023": 37667, "FY2022": 43949, "FY2021": 52020, "FY2020": 100569, "FY2019": 131889, "FY2018": 113678, "FY2017": 117555, "FY2016": 144263, "FY2015": 102378, "FY2014": 66109}),
    ("DATA", "Property, Plant and Equipment", {"FY2025": 476, "FY2024": 578, "FY2018": 426, "FY2017": 333, "FY2016": 300, "FY2015": 226, "FY2014": 987}),
    ("DATA", "Right-of-use Assets", {"FY2025": 1192, "FY2024": 1366}),
    ("DATA", "Property, Plant and Equipment and Right-of-use Assets", {"FY2023": 1885, "FY2022": 1496, "FY2021": 2517, "FY2020": 3687, "FY2019": 5363}),
    ("DATA", "Goodwill", {"FY2025": 8766, "FY2024": 8304}),
    ("DATA", "Other intangible assets", {"FY2025": 4969, "FY2024": 4941}),
    ("DATA", "Goodwill and other intangible assets", {"FY2023": 12787, "FY2022": 11561, "FY2021": 9802, "FY2020": 10904, "FY2019": 11182, "FY2018": 12115, "FY2017": 11371, "FY2016": 10310, "FY2015": 8031, "FY2014": 7791}),
    ("DATA", "Deferred tax assets", {"FY2025": 12597, "FY2024": 13428, "FY2023": 8822, "FY2022": 8781, "FY2021": 8191, "FY2020": 6626, "FY2019": 5851, "FY2018": 6640, "FY2017": 6531, "FY2016": 6966, "FY2015": 6418, "FY2014": 4893}),
    ("DATA", "Other assets", {"FY2025": 12616, "FY2024": 13002, "FY2023": 12998, "FY2022": 12396, "FY2021": 9791, "FY2020": 8958, "FY2019": 7717, "FY2018": 6737, "FY2017": 8473, "FY2016": 10713, "FY2015": 8288, "FY2014": 10473}),
    ("TOTAL", "Total assets", {"FY2025": 328964, "FY2024": 291532, "FY2023": 254441, "FY2022": 452390, "FY2021": 496686, "FY2020": 485372, "FY2019": 466248, "FY2018": 575063, "FY2017": 490960, "FY2016": 527718, "FY2015": 441682, "FY2014": 365352}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Due to banks", {"FY2025": 149668, "FY2024": 153081, "FY2023": 120940, "FY2022": 289489, "FY2021": 297704, "FY2020": 276280, "FY2019": 263150, "FY2018": 367631, "FY2017": 279739, "FY2016": 305077, "FY2015": 264777, "FY2014": 189419}),
    ("DATA", "Derivative liabilities", {"FY2025": 26, "FY2024": 868, "FY2023": 69, "FY2022": 502, "FY2021": 25, "FY2020": 135, "FY2019": 34, "FY2017": 74, "FY2016": 1298, "FY2015": 859, "FY2014": 4267}),
    ("DATA", "Due to customers", {"FY2025": 84367, "FY2024": 44717, "FY2023": 42227, "FY2022": 59541, "FY2021": 92028, "FY2020": 99556, "FY2019": 95291, "FY2018": 109231, "FY2017": 112349, "FY2016": 129706, "FY2015": 98537, "FY2014": 101419}),
    ("DATA", "Other liabilities", {"FY2025": 8317, "FY2024": 9171, "FY2023": 9623, "FY2022": 11254, "FY2021": 9316, "FY2020": 10641, "FY2019": 11722, "FY2018": 6453, "FY2017": 4837, "FY2016": 4577, "FY2015": 3517, "FY2014": 1785}),
    ("DATA", "Provisions", {"FY2025": 334, "FY2024": 700, "FY2023": 500}),
    ("DATA", "Subordinated debt", {"FY2025": 15623, "FY2024": 14824, "FY2023": 15556, "FY2022": 15853, "FY2021": 15032, "FY2020": 16117, "FY2019": 15231, "FY2018": 16294, "FY2017": 16072, "FY2016": 15503, "FY2015": 13316, "FY2014": 14138}),
    ("TOTAL", "Total liabilities", {"FY2025": 258335, "FY2024": 223361, "FY2023": 188915, "FY2022": 376639, "FY2021": 414105, "FY2020": 402729, "FY2019": 385428, "FY2018": 499609, "FY2017": 413071, "FY2016": 456161, "FY2015": 381006, "FY2014": 311028}),
    ("SECTION", "Equity attributable to equity holders", {}),
    ("DATA", "Share capital", {"FY2025": 102173, "FY2024": 102173, "FY2023": 102173, "FY2022": 102173, "FY2021": 102173, "FY2020": 102173, "FY2019": 102173, "FY2018": 102173, "FY2017": 102173, "FY2016": 102173, "FY2015": 102173, "FY2014": 102173}),
    ("DATA", "Other reserves", {"FY2025": -1303, "FY2024": -1488, "FY2023": -2354, "FY2022": -6845, "FY2021": -3854, "FY2020": 1890, "FY2019": 1172, "FY2018": -1538, "FY2017": 130, "FY2016": -692, "FY2015": -2989, "FY2014": -2635}),
    ("DATA", "Accumulated losses", {"FY2025": -30241, "FY2024": -32514, "FY2023": -34293, "FY2022": -19577, "FY2021": -15738, "FY2020": -21420, "FY2019": -22525, "FY2018": -25181, "FY2017": -24414, "FY2016": -29924, "FY2015": -38508, "FY2014": -45214}),
    ("TOTAL", "Total equity", {"FY2025": 70629, "FY2024": 68171, "FY2023": 65526, "FY2022": 75751, "FY2021": 82581, "FY2020": 82643, "FY2019": 80820, "FY2018": 75454, "FY2017": 77889, "FY2016": 71557, "FY2015": 60676, "FY2014": 54324}),
    ("TOTAL", "Total liabilities and equity", {"FY2025": 328964, "FY2024": 291532, "FY2023": 254441, "FY2022": 452390, "FY2021": 496686, "FY2020": 485372, "FY2019": 466248, "FY2018": 575063, "FY2017": 490960, "FY2016": 527718, "FY2015": 441682, "FY2014": 365352}),
]

bw.add_balance_sheet_sheet(
    title="Bank of Africa United Kingdom Plc — Statement of Financial Position",
    subtitle="Entity-level (solo) basis, as reported in each year's own Annual Report",
    rows=balance_sheet_rows,
    sources_text=BALANCE_SHEET_SOURCES,
    first_col_width=64,
    source_height=220,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Sheet: Profit & Loss
# ---------------------------------------------------------------
INCOME_STATEMENT_PRESENTATION_NOTE = (
    "PRESENTATION NOTE: FY2025/FY2024 (Annual Report 2025) reach 'Net operating income' via "
    "Net interest income + Net fee and commission income + Net trading income (no separate "
    "'Other operating income' line), then 'Total operating expenses' followed by a 'Net "
    "impairment gain/(loss)' line to reach Profit/(Loss) before tax. FY2023 (Annual Report "
    "2023) and FY2022/FY2021 (Annual Report 2022) additionally disclose a separate 'Other "
    "operating income' line feeding into Net operating income, then 'Total operating expenses "
    "before impairment losses' followed by 'Net impairment (losses)/recoveries' to reach the "
    "same (Loss)/Profit before tax subtotal - economically the same structure, reproduced as "
    "originally labelled each year. 'Redundancy cost' is a one-off line only disclosed in "
    "FY2023. HD-017 extension: FY2018-FY2014 predate IFRS 16 (adopted 1 January 2019), so "
    "depreciation is pure 'Depreciation on property, plant and equipment' with no "
    "right-of-use component (shown on that row, not the combined FY2023-2019 row). FY2014's "
    "own Statement of Profit or Loss has a unique 'Profit from discontinued activity' line "
    "(GBP0k for FY2014 itself; its FY2013 comparative of GBP1,197k is not carried into this "
    "workbook, since FY2013 is outside this project's FY2014 floor for this entity). FY2017 "
    "is shown here using the FY2017 Annual Report's own primary figures (Net fee and "
    "commission income GBP1,015k, Profit for the year GBP5,510k) rather than the FY2018 "
    "Annual Report's restated FY2017 comparative (Net fee and commission income GBP307k, "
    "Profit for the year GBP4,933k) - both are genuine, disclosed figures; see the Statement "
    "of Changes in Equity sheet for the full restatement note."
)
INCOME_STATEMENT_SOURCES = (
    "Sources - Bank of Africa United Kingdom Plc's own Statement of Profit or Loss, GBP'000:\n"
    f"FY2025 & FY2024: Annual Report and Financial Statements 2025, p.38 - {AR2025_URL}\n"
    f"FY2023 (& FY2022 restated comparative, not used - see note): Annual Report and Financial Statements 2023, p.39 - {AR2023_URL}\n"
    f"FY2022 (originally reported, used as primary column): Annual Report and Financial Statements 2022, p.38 - {AR2022_URL}\n"
    f"FY2021: Annual Report and Financial Statements 2022, p.38 (FY2021 comparative column) - {AR2022_URL}\n"
    f"FY2020 (& FY2019 restated comparative, used as primary column - see note): Annual Report and Financial Statements 2020, p.30 - {AR2020_URL}\n"
    f"FY2018: Annual Report and Financial Statements 2018, p.23 - {AR2018_URL}\n"
    f"FY2017 (own primary column, not the FY2018 Annual Report's restated comparative - see note): Annual Report and Financial Statements 2017, p.23 - {AR2017_URL}\n"
    f"FY2016 (& FY2015 comparative, used as primary column): Annual Report and Financial Statements 2016, p.18 - {AR2016_URL}\n"
    f"FY2014: Annual Report and Financial Statements 2014, p.15 - {AR2014_URL}\n\n"
    + INCOME_STATEMENT_PRESENTATION_NOTE + "\n\n" + ENTITY_NOTE
)

income_statement_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest and similar income", {"FY2025": 12676, "FY2024": 12402, "FY2023": 17701, "FY2022": 21817, "FY2021": 21793, "FY2020": 22036, "FY2019": 25094, "FY2018": 23532, "FY2017": 21034, "FY2016": 19038, "FY2015": 14664, "FY2014": 8221}),
    ("DATA", "Interest expense and similar charges", {"FY2025": -5587, "FY2024": -6728, "FY2023": -10927, "FY2022": -6747, "FY2021": -3212, "FY2020": -4068, "FY2019": -8425, "FY2018": -6766, "FY2017": -4586, "FY2016": -3930, "FY2015": -1683, "FY2014": -1022}),
    ("TOTAL", "Net interest income", {"FY2025": 7089, "FY2024": 5674, "FY2023": 6774, "FY2022": 15070, "FY2021": 18581, "FY2020": 17968, "FY2019": 16669, "FY2018": 16766, "FY2017": 16448, "FY2016": 15108, "FY2015": 12981, "FY2014": 7199}),
    ("DATA", "Fee and commission income", {"FY2025": 3193, "FY2024": 3678, "FY2023": 3691, "FY2022": 3034, "FY2021": 3193, "FY2020": 2149, "FY2019": 1622, "FY2018": 2728, "FY2017": 2668, "FY2016": 3889, "FY2015": 3170, "FY2014": 5351}),
    ("DATA", "Fee and commission expense", {"FY2025": -958, "FY2024": -1332, "FY2023": -2532, "FY2022": -1632, "FY2021": -1526, "FY2020": -2229, "FY2019": -2107, "FY2018": -2147, "FY2017": -1653, "FY2016": -1487, "FY2015": -1310, "FY2014": -241}),
    ("TOTAL", "Net fee and commission income", {"FY2025": 2235, "FY2024": 2346, "FY2023": 1159, "FY2022": 1402, "FY2021": 1667, "FY2020": -80, "FY2019": -485, "FY2018": 581, "FY2017": 1015, "FY2016": 2402, "FY2015": 1860, "FY2014": 5110}),
    ("DATA", "Net trading income/(expense)", {"FY2025": 716, "FY2024": 578, "FY2023": -4039, "FY2022": 3000, "FY2021": 4298, "FY2020": 750, "FY2019": 4261, "FY2018": 105, "FY2017": 2898, "FY2016": 2530, "FY2015": 1065, "FY2014": 1487}),
    ("DATA", "Other operating income", {"FY2023": 284, "FY2022": 33, "FY2021": 51, "FY2020": 69, "FY2019": 979, "FY2018": 16, "FY2017": -31, "FY2016": 538, "FY2015": 258, "FY2014": 352}),
    ("TOTAL", "Net operating income", {"FY2025": 10040, "FY2024": 8598, "FY2023": 4178, "FY2022": 19505, "FY2021": 24597, "FY2020": 18707, "FY2019": 21424, "FY2018": 17468, "FY2017": 20330, "FY2016": 20578, "FY2015": 16164, "FY2014": 14148}),
    ("SECTION", "Operating expenses", {}),
    ("DATA", "Personnel expenses", {"FY2025": -7191, "FY2024": -7054, "FY2023": -8648, "FY2022": -10282, "FY2021": -8982, "FY2020": -8236, "FY2019": -7082, "FY2018": -6201, "FY2017": -6163, "FY2016": -5983, "FY2015": -4945, "FY2014": -4268}),
    ("DATA", "Redundancy cost", {"FY2023": -765}),
    ("DATA", "Depreciation on property, plant and equipment", {"FY2025": -180, "FY2024": -111, "FY2018": -172, "FY2017": -111, "FY2016": -71, "FY2015": -119, "FY2014": -249}),
    ("DATA", "Depreciation on right-of-use assets", {"FY2025": -211, "FY2024": -658}),
    ("DATA", "Depreciation of property, plant and equipment; and right-of-use assets", {"FY2023": -976, "FY2022": -1244, "FY2021": -1236, "FY2020": -1244, "FY2019": -809}),
    ("DATA", "Amortisation of intangible assets", {"FY2025": -826, "FY2024": -730, "FY2023": -459, "FY2022": -461, "FY2021": -653, "FY2020": -852, "FY2019": -761, "FY2018": -707, "FY2017": -508, "FY2016": -135, "FY2015": -30, "FY2014": 0}),
    ("DATA", "Other operating expenses", {"FY2025": -2251, "FY2024": -6351, "FY2023": -6814, "FY2022": -7471, "FY2021": -7018, "FY2020": -6519, "FY2019": -8025, "FY2018": -7820, "FY2017": -5231, "FY2016": -4443, "FY2015": -5408, "FY2014": -3442}),
    ("TOTAL", "Total operating expenses", {"FY2025": -10659, "FY2024": -14904, "FY2023": -17662, "FY2022": -19458, "FY2021": -17889, "FY2020": -16851, "FY2019": -16677, "FY2018": -14900, "FY2017": -12012, "FY2016": -10632, "FY2015": -10502, "FY2014": -7959}),
    ("DATA", "Net impairment gain/(losses)", {"FY2025": 3723, "FY2024": 3482, "FY2023": -420, "FY2022": -5325, "FY2021": -1648, "FY2020": -1759, "FY2019": -865, "FY2018": -104, "FY2017": -1510, "FY2016": -886, "FY2015": 1143, "FY2014": -1361}),
    ("TOTAL", "Profit/(Loss) before tax", {"FY2025": 3104, "FY2024": -2824, "FY2023": -13904, "FY2022": -5278, "FY2021": 5060, "FY2020": 97, "FY2019": 3882, "FY2018": 2464, "FY2017": 6808, "FY2016": 9060, "FY2015": 6805, "FY2014": 4828}),
    ("DATA", "Taxation credit/(expense)", {"FY2025": -831, "FY2024": 4603, "FY2023": -95, "FY2022": 1439, "FY2021": 622, "FY2020": 1000, "FY2019": -1260, "FY2018": -295, "FY2017": -1298, "FY2016": -476, "FY2015": 990, "FY2014": 880}),
    ("DATA", "Profit from discontinued activity", {"FY2014": 0}),
    ("TOTAL", "Profit/(Loss) for the year", {"FY2025": 2273, "FY2024": 1779, "FY2023": -13999, "FY2022": -3839, "FY2021": 5682, "FY2020": 1097, "FY2019": 2622, "FY2018": 2169, "FY2017": 5510, "FY2016": 8584, "FY2015": 7795, "FY2014": 5708}),
]

bw.add_income_statement_sheet(
    title="Bank of Africa United Kingdom Plc — Statement of Profit or Loss",
    subtitle="Entity-level (solo) basis, as reported in each year's own Annual Report",
    rows=income_statement_rows,
    sources_text=INCOME_STATEMENT_SOURCES,
    first_col_width=68,
    source_height=220,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Sheet: Statement of Changes in Equity
# ---------------------------------------------------------------
EQUITY_HEADERS = ["Share capital", "Other reserves", "Accumulated losses", "Total equity"]
EQUITY_CHANGES_SOURCES = (
    "Sources - Bank of Africa United Kingdom Plc's own Statement of Changes in Equity, GBP'000:\n"
    f"1 Jan 2021 - 31 Dec 2022 (originally reported): Annual Report and Financial Statements 2022, p.41 - {AR2022_URL}\n"
    f"1 Jan 2023 - 31 Dec 2023 (opening balance restated - see note): Annual Report and Financial Statements 2023, p.42 - {AR2023_URL}\n"
    f"1 Jan 2024 - 31 Dec 2025: Annual Report and Financial Statements 2025, p.41 - {AR2025_URL}\n"
    f"1 Jan 2019 - 31 Dec 2020: Annual Report and Financial Statements 2020, p.31 - {AR2020_URL}\n"
    f"1 Jan 2018 - 31 Dec 2018: Annual Report and Financial Statements 2018, p.26 - {AR2018_URL}\n"
    f"1 Jan 2017 - 31 Dec 2017 (own primary chain, not the FY2018 Annual Report's restated version - see note): Annual Report and Financial Statements 2017, p.26 - {AR2017_URL}\n"
    f"1 Jan 2014 - 31 Dec 2016: Annual Report and Financial Statements 2016, p.21 (FY2015/FY2016) and Annual Report and Financial Statements 2014, p.18 (FY2014) - {AR2016_URL} / {AR2014_URL}\n\n"
    "DATA QUALITY NOTE - genuine restatement break, same one already documented on the Cash "
    "Flow Statement sheet: the FY2022 Annual Report's own closing balance at 31 December 2022 "
    "was Share capital 102,173 / Other reserves (6,845) / Accumulated losses (19,577) / Total "
    "75,751 (loss for the year (3,839)). The FY2023 Annual Report's own opening balance at 1 "
    "January 2023 restates this to Accumulated losses (20,294) / Total 75,034 (loss for the "
    "year restated to (4,556)), consistent with the FY2022 Independent Auditor's Report's own "
    "reference to 'prior year adjustments and ongoing regulatory investigation'. This workbook "
    "shows both: the FY2021-2022 rows follow the originally-reported chain (project "
    "convention - each year's own primary report), and the FY2023 opening row uses the FY2023 "
    "Annual Report's own restated opening balance (since that is the actual starting point of "
    "its own statement) - the £717k break between the two 'Balance at 31 Dec 2022 / 1 Jan "
    "2023' rows is the restatement, not a transcription error.\n\n"
    "HD-017 EXTENSION - THIRD DATA QUALITY NOTE, a further genuine restatement found further "
    "back in the chain: the FY2018 Annual Report's own 'Impact of correction of errors' "
    "restates the FY2017 opening position (Accumulated losses (29,924) as originally reported "
    "at 1 Jan 2017 vs. (30,803) restated, a GBP879k adjustment) and the FY2017 profit for the "
    "year (GBP5,510k originally reported vs. GBP4,933k restated, a further GBP577k "
    "adjustment), reaching a restated 31 Dec 2017 balance of Other reserves 130 / Accumulated "
    "losses (25,869) / Total 76,434 vs. the FY2017 Annual Report's own originally-reported "
    "31 Dec 2017 balance of Other reserves 130 / Accumulated losses (24,414) / Total 77,889. "
    "This workbook shows both the originally-reported FY2017 chain (rows below, project "
    "convention) and the FY2018 Annual Report's own restated opening figures (since that is "
    "the actual starting point of its own FY2018 statement) - not reconciled further. A "
    "fourth, separate GBP265k break (entirely within Other reserves) exists between the "
    "FY2020 Annual Report's own closing balance at 31 December 2020 and this workbook's "
    "existing FY2021 opening balance (sourced from the FY2022 Annual Report's FY2021 "
    "comparative, predating this extension) - see the entity note above for the exact "
    "figures; also not reconciled further.\n\n" + ENTITY_NOTE
)

equity_changes_rows = [
    ("TOTAL", "Balance as at 1 January 2014", (102173, -848, -50922, 50403)),
    ("DATA", "Profit for the year", (None, None, 5708, 5708)),
    ("DATA", "Other comprehensive income", (None, -1787, None, -1787)),
    ("TOTAL", "Balance as at 31 December 2014 / 1 January 2015", (102173, -2635, -45214, 54324)),
    ("DATA", "Profit for the year", (None, None, 7795, 7795)),
    ("DATA", "Other comprehensive income", (None, -354, None, -354)),
    ("TOTAL", "Balance as at 31 December 2015 / 1 January 2016", (102173, -2989, -38508, 60676)),
    ("DATA", "Profit for the year", (None, None, 8584, 8584)),
    ("DATA", "Other comprehensive income", (None, 2297, None, 2297)),
    ("TOTAL", "Balance as at 31 December 2016 / 1 January 2017 (as originally reported)", (102173, -692, -29924, 71557)),
    ("DATA", "Impact of correction of errors (FY2018 Annual Report restatement)", (None, None, -879, -879)),
    ("TOTAL", "Balance as at 1 January 2017 (restated - see note)", (102173, -692, -30803, 70678)),
    ("DATA", "Profit for the year (as originally reported)", (None, None, 5510, 5510)),
    ("DATA", "Other comprehensive income", (None, 822, None, 822)),
    ("TOTAL", "Balance as at 31 December 2017 (as originally reported)", (102173, 130, -24414, 77889)),
    ("DATA", "Impact of correction of errors (FY2018 Annual Report restatement)", (None, None, -577, -577)),
    ("TOTAL", "Balance as at 1 January 2018 (restated - see note)", (102173, 130, -25869, 76434)),
    ("DATA", "Profit for the year", (None, None, 2169, 2169)),
    ("DATA", "Other comprehensive income", (None, -1668, None, -1668)),
    ("TOTAL", "Balance as at 31 December 2018 / 1 January 2019 (as originally reported)", (102173, -1538, -25181, 75454)),
    ("DATA", "Impact of correction of errors (FY2020 Annual Report restatement)", (None, None, 34, 34)),
    ("TOTAL", "Balance as at 1 January 2019 (restated - see note)", (102173, -1538, -25147, 75488)),
    ("DATA", "Profit for the year (as originally reported)", (None, None, 2852, 2852)),
    ("DATA", "Impact of correction of errors (FY2020 Annual Report restatement)", (None, None, -230, -230)),
    ("DATA", "Other comprehensive income", (None, 2710, None, 2710)),
    ("TOTAL", "Balance as at 31 December 2019 / 1 January 2020", (102173, 1172, -22525, 80820)),
    ("DATA", "Profit for the year", (None, None, 1097, 1097)),
    ("DATA", "Impact of correction of errors (opening deferred tax adjustment)", (None, None, 8, 8)),
    ("DATA", "Other comprehensive income", (None, 718, None, 718)),
    ("TOTAL", "Balance as at 31 December 2020", (102173, 1890, -21420, 82643)),
    ("TOTAL", "Balance as at 1 January 2021", (102173, 1625, -21420, 82378)),
    ("DATA", "Profit for the year", (None, None, 5682, 5682)),
    ("DATA", "Other comprehensive income", (None, -5479, None, -5479)),
    ("TOTAL", "Balance as at 31 December 2021", (102173, -3854, -15738, 82581)),
    ("TOTAL", "Balance as at 1 January 2022", (102173, -3854, -15738, 82581)),
    ("DATA", "Loss for the year", (None, None, -3839, -3839)),
    ("DATA", "Other comprehensive income", (None, -2991, None, -2991)),
    ("TOTAL", "Balance as at 31 December 2022 (as originally reported)", (102173, -6845, -19577, 75751)),
    ("TOTAL", "Balance as at 1 January 2023 (restated - see note)", (102173, -6845, -20294, 75034)),
    ("DATA", "Loss for the year", (None, None, -13999, -13999)),
    ("DATA", "Other comprehensive income", (None, 4491, None, 4491)),
    ("TOTAL", "Balance as at 31 December 2023", (102173, -2354, -34293, 65526)),
    ("TOTAL", "Balance as at 1 January 2024", (102173, -2354, -34293, 65526)),
    ("DATA", "Profit for the year", (None, None, 1779, 1779)),
    ("DATA", "Other comprehensive income", (None, 866, None, 866)),
    ("TOTAL", "Balance as at 31 December 2024", (102173, -1488, -32514, 68171)),
    ("TOTAL", "Balance as at 1 January 2025", (102173, -1488, -32514, 68171)),
    ("DATA", "Profit for the year", (None, None, 2273, 2273)),
    ("DATA", "Other comprehensive income", (None, 185, None, 185)),
    ("TOTAL", "Balance as at 31 December 2025", (102173, -1303, -30241, 70629)),
]

bw.add_equity_changes_sheet(
    title="Bank of Africa United Kingdom Plc — Statement of Changes in Equity",
    subtitle="Entity-level (solo) basis, chronological, 1 January 2014 - 31 December 2025",
    headers=EQUITY_HEADERS,
    rows=equity_changes_rows,
    sources_text=EQUITY_CHANGES_SOURCES,
)

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Cash flows from continuing operating activities", {}),
    ("DATA", "Profit/(loss) before tax", {"FY2025": 3104, "FY2024": -2824, "FY2023": -13904, "FY2022": -5278, "FY2021": 5060, "FY2020": 97, "FY2019": 3882, "FY2018": 2464, "FY2017": 6808, "FY2016": 9060, "FY2015": 6805, "FY2014": 4828}),
    ("DATA", "Net interest income", {"FY2025": -7089, "FY2024": -5674, "FY2023": -6774, "FY2022": -15070, "FY2021": -18581, "FY2020": -17968, "FY2019": -16669, "FY2018": 16766, "FY2017": 16448, "FY2016": 15108, "FY2015": 12981, "FY2014": 7199}),
    ("DATA", "Interest received", {"FY2025": 13028, "FY2024": 12048, "FY2023": 20919, "FY2022": 19859, "FY2021": 27104, "FY2020": 22440, "FY2019": 24090, "FY2018": -5245, "FY2017": -5704, "FY2016": -7638, "FY2015": -7870, "FY2014": -4620}),
    ("DATA", "Interest paid", {"FY2025": -6175, "FY2024": -6777, "FY2023": -10607, "FY2022": -7197, "FY2021": -4236, "FY2020": -2905, "FY2019": -9691, "FY2018": 6295, "FY2017": 4711, "FY2016": 3725, "FY2015": 1719, "FY2014": 1059}),
    ("DATA", "Change in operating assets", {"FY2025": -54573, "FY2024": -17912, "FY2023": 170939, "FY2022": 21084, "FY2021": 35264, "FY2020": -29407, "FY2019": 42218, "FY2018": -42081, "FY2017": -64434, "FY2016": -41817, "FY2015": -25324, "FY2014": -106599}),
    ("DATA", "Change in operating liabilities", {"FY2025": 34977, "FY2024": 33274, "FY2023": -189466, "FY2022": -35633, "FY2021": 14726, "FY2020": 18426, "FY2019": -119601, "FY2018": 85298, "FY2017": -41412, "FY2016": 76000, "FY2015": 69582, "FY2014": 147429}),
    ("DATA", "Other (non-cash) items included in profit before tax", {"FY2025": -7125, "FY2024": -1465, "FY2023": 18778, "FY2022": -5399, "FY2021": 1625, "FY2020": 5209, "FY2019": -1549, "FY2018": 882, "FY2017": -890, "FY2016": 970, "FY2015": 1586, "FY2014": 1250}),
    ("DATA", "Corporation tax", {"FY2023": 0, "FY2022": 171, "FY2021": -868, "FY2020": -97, "FY2019": -436, "FY2018": -295, "FY2017": -1298, "FY2016": -1418}),
    ("TOTAL", "Net cash flows from/(used in) operating activities", {"FY2025": -23853, "FY2024": 10670, "FY2023": -10115, "FY2022": -27463, "FY2021": 60094, "FY2020": -4205, "FY2019": -77756, "FY2018": 64083, "FY2017": -85771, "FY2016": 53990, "FY2015": 59479, "FY2014": 50546}),
    ("SECTION", "Cash flows from investing activities", {}),
    ("DATA", "Purchase of financial investments", {"FY2025": -53189, "FY2024": -44212, "FY2023": -7685, "FY2022": -6272, "FY2021": -82228, "FY2020": -17350, "FY2019": -151190, "FY2018": -87875, "FY2017": -72258, "FY2016": -114745, "FY2015": -48498, "FY2014": -73137}),
    ("DATA", "Proceeds from sales of financial investments", {"FY2025": 64477, "FY2024": 32257, "FY2023": 8036, "FY2022": 17338, "FY2021": 39068, "FY2020": 48166, "FY2019": 186750, "FY2018": 41262, "FY2017": 115811, "FY2016": 63354, "FY2015": 4892, "FY2014": 47315}),
    ("DATA", "Proceeds from disposal of property and equipment", {"FY2014": 0}),
    ("DATA", "Proceeds from disposal of intangible assets", {"FY2014": 0}),
    ("DATA", "Purchase of Property, Plant and Equipment (and Right-of-use Assets)", {"FY2025": -22, "FY2024": -470, "FY2023": -1550, "FY2022": -233, "FY2021": -66, "FY2020": -60, "FY2019": -81, "FY2018": -267, "FY2017": -135, "FY2016": -115, "FY2015": -72, "FY2014": -125}),
    ("DATA", "Purchase of intangible assets", {"FY2025": -877, "FY2024": -1569, "FY2023": -1858, "FY2022": -1744, "FY2021": -745, "FY2020": -63, "FY2019": -333, "FY2018": -1325, "FY2017": -1244, "FY2016": -1160, "FY2015": -724}),
    ("TOTAL", "Net cash flows from/(used in) investing activities", {"FY2025": 10389, "FY2024": -13994, "FY2023": -3057, "FY2022": 9089, "FY2021": -43971, "FY2020": 30693, "FY2019": 35146, "FY2018": -48205, "FY2017": 42174, "FY2016": -52666, "FY2015": -44402, "FY2014": -25947}),
    ("SECTION", "Cash flows from financing activities", {}),
    ("DATA", "Repayment of lease principal", {"FY2025": -89, "FY2024": -181, "FY2023": -797, "FY2022": -1050, "FY2021": -944, "FY2020": -1107, "FY2019": -877}),
    ("DATA", "Group subordinated debt", {"FY2018": 635, "FY2017": 629}),
    ("TOTAL", "Net cash flows from/(used in) financing activities", {"FY2025": -89, "FY2024": -181, "FY2023": -797, "FY2022": -1050, "FY2021": -944, "FY2020": -1107, "FY2019": -877, "FY2018": 635, "FY2017": 629, "FY2016": 0, "FY2015": 0, "FY2014": 0}),
    ("TOTAL", "Net increase/(decrease) in cash and cash equivalents", {"FY2025": -13553, "FY2024": -3505, "FY2023": -13969, "FY2022": -19424, "FY2021": 15179, "FY2020": 25381, "FY2019": -43487, "FY2018": 16513, "FY2017": -42968, "FY2016": 1324, "FY2015": 15077, "FY2014": 24599}),
    ("DATA", "Cash and cash equivalents as at 1 January", {"FY2025": 51070, "FY2024": 54575, "FY2023": 68544, "FY2022": 87968, "FY2021": 72789, "FY2020": 47408, "FY2019": 90895, "FY2018": 74382, "FY2017": 117350, "FY2016": 116026, "FY2015": 100949, "FY2014": 76350}),
    ("TOTAL", "Cash and cash equivalents as at 31 December", {"FY2025": 37517, "FY2024": 51070, "FY2023": 54575, "FY2022": 68544, "FY2021": 87968, "FY2020": 72789, "FY2019": 47408, "FY2018": 90895, "FY2017": 74382, "FY2016": 117350, "FY2015": 116026, "FY2014": 100949}),
]

bw.add_cash_flow_sheet(
    title="Bank of Africa United Kingdom Plc — Statement of Cash Flows",
    subtitle="Entity-level (solo) basis, as reported in each year's own Annual Report",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=70,
    source_height=210,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Sheet: Asset Quality
# ---------------------------------------------------------------
ASSET_QUALITY_PRESENTATION_NOTE = (
    "PRESENTATION NOTE: BOA UK's Loans and advances to customers note (Note 16 in most years' "
    "Annual Reports, Note 19 in FY2018's) discloses only a single IFRS 9 stage breakdown - no "
    "by-product/by-sector split. Gross carrying amount FY2025 (42,440) + FY2024 (34,168) + "
    "FY2023 (33,745) + FY2022 (154,905) + FY2021 (168,272) + FY2018 (215,927) and Carrying "
    "amount figures all tie exactly to the Balance Sheet's own 'Loans and advances to "
    "customers' line for each year. HD-017 extension: IFRS 9 (replacing IAS 39's "
    "incurred-loss impairment model) was adopted 1 January 2018, so FY2014-FY2017 have no "
    "stage split at all - those years' own Note 16 instead discloses a single net loan "
    "balance plus a period-end individual impairment provision and the gross amount of "
    "loans individually determined to be impaired (no collective/portfolio provision is "
    "held any of those years - 'the Bank now assesses all loans on an individual basis'). "
    "This workbook presents that pre-IFRS 9 data in a separate section below, with its own "
    "derived ratios computed on a different denominator (net loans + provision, as an "
    "estimate of the gross loan book, since no total-gross-book figure is separately stated "
    "pre-IFRS 9) - not comparable to the IFRS 9 stage-based ratios above it."
)
ASSET_QUALITY_SOURCES = (
    "Sources - Bank of Africa United Kingdom Plc's own Loans and advances to customers note "
    "(Note 16, or Note 19 in the FY2018 Annual Report), GBP'000:\n"
    f"FY2025 & FY2024: Annual Report and Financial Statements 2025, p.65 - {AR2025_URL}\n"
    f"FY2023: Annual Report and Financial Statements 2023, p.67 - {AR2023_URL}\n"
    f"FY2022 (originally reported, used as primary column): Annual Report and Financial Statements 2022, p.66 - {AR2022_URL}\n"
    f"FY2021: Annual Report and Financial Statements 2022, p.66 (FY2021 comparative column) - {AR2022_URL}\n"
    f"FY2018: Annual Report and Financial Statements 2018, p.50 (Note 19) - {AR2018_URL}\n"
    f"FY2017: Annual Report and Financial Statements 2017, p.45 (Note 16) - {AR2017_URL}\n"
    f"FY2016 (& FY2015 comparative, used as primary column): Annual Report and Financial Statements 2016, p.42 (Note 16) - {AR2016_URL}\n"
    f"FY2014: Annual Report and Financial Statements 2014, p.39 (Note 17) - {AR2014_URL}\n\n"
    + ASSET_QUALITY_PRESENTATION_NOTE + "\n\n" + ENTITY_NOTE
)

asset_quality_rows = [
    ("SECTION", "Loans and advances to customers by IFRS 9 stage - gross carrying amount", {}),
    ("DATA", "Stage 1 - 12 months ECL", {"FY2025": 39023, "FY2024": 25334, "FY2023": 20047, "FY2022": 138815, "FY2021": 152521, "FY2018": 172960}),
    ("DATA", "Stage 2 - Lifetime ECL", {"FY2025": 678, "FY2024": 3938, "FY2023": 6350, "FY2022": 7799, "FY2021": 0, "FY2018": 37903}),
    ("DATA", "Stage 3 - Non performing - Lifetime ECL", {"FY2025": 2739, "FY2024": 4896, "FY2023": 7348, "FY2022": 8291, "FY2021": 15751, "FY2018": 5065}),
    ("TOTAL", "Total gross carrying amount", {"FY2025": 42440, "FY2024": 34168, "FY2023": 33745, "FY2022": 154905, "FY2021": 168272, "FY2018": 215927}),
    ("SECTION", "Loss allowance by IFRS 9 stage", {}),
    ("DATA", "Stage 1 - 12 months ECL", {"FY2025": -49, "FY2024": -51, "FY2023": -106, "FY2022": -568, "FY2021": -837, "FY2018": -503}),
    ("DATA", "Stage 2 - Lifetime ECL", {"FY2025": -29, "FY2024": -236, "FY2023": -114, "FY2022": -127, "FY2021": 0, "FY2018": -1475}),
    ("DATA", "Stage 3 - Non performing - Lifetime ECL", {"FY2025": -410, "FY2024": -4896, "FY2023": -5193, "FY2022": -5925, "FY2021": -5419, "FY2018": -2354}),
    ("TOTAL", "Total loss allowance", {"FY2025": -488, "FY2024": -5183, "FY2023": -5413, "FY2022": -6620, "FY2021": -6256, "FY2018": -4331}),
    ("SECTION", "Carrying amount", {}),
    ("TOTAL", "Loans and advances to customers (carrying amount)", {"FY2025": 41952, "FY2024": 28985, "FY2023": 28332, "FY2022": 148285, "FY2021": 162016, "FY2018": 211596}),
    ("SECTION", "Derived ratios (IFRS 9 stage basis)", {}),
    ("DATA", "ECL coverage ratio (total loss allowance / total gross)", {"FY2025": "1.15%", "FY2024": "15.17%", "FY2023": "16.04%", "FY2022": "4.27%", "FY2021": "3.72%", "FY2018": "2.01%"}),
    ("DATA", "Stage 3 / NPL ratio (Stage 3 gross / total gross)", {"FY2025": "6.45%", "FY2024": "14.33%", "FY2023": "21.78%", "FY2022": "5.35%", "FY2021": "9.36%", "FY2018": "2.35%"}),
    ("DATA", "Stage 3 coverage ratio (Stage 3 allowance / Stage 3 gross)", {"FY2025": "14.97%", "FY2024": "100.00%", "FY2023": "70.68%", "FY2022": "71.46%", "FY2021": "34.40%", "FY2018": "46.48%"}),
    ("SECTION", "Pre-IFRS 9 (IAS 39) loan quality metrics - FY2014-FY2017 (individual-impairment basis, no stage split exists)", {}),
    ("DATA", "Loans and advances to customers (net carrying amount)", {"FY2017": 207964, "FY2016": 175945, "FY2015": 167713, "FY2014": 149257}),
    ("DATA", "Individual impairment provision (period-end balance)", {"FY2017": 3023, "FY2016": 1581, "FY2015": 597, "FY2014": 1785}),
    ("DATA", "Gross amount of loans individually determined to be impaired", {"FY2017": 21840, "FY2016": 5250, "FY2015": 1829, "FY2014": 9929}),
    ("SECTION", "Derived ratios (pre-IFRS 9 basis - not comparable to the stage-based ratios above)", {}),
    ("DATA", "Estimated NPL ratio (impaired loans / [net loans + provision])", {"FY2017": "10.35%", "FY2016": "2.96%", "FY2015": "1.09%", "FY2014": "6.57%"}),
    ("DATA", "Estimated coverage ratio (provision / impaired loans)", {"FY2017": "13.84%", "FY2016": "30.11%", "FY2015": "32.64%", "FY2014": "17.98%"}),
]

bw.add_asset_quality_sheet(
    title="Bank of Africa United Kingdom Plc — Asset Quality / Credit Risk Disclosures",
    subtitle="Loans and advances to customers by IFRS 9 stage, entity-level (solo) basis",
    rows=asset_quality_rows,
    sources_text=ASSET_QUALITY_SOURCES,
    first_col_width=64,
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, f"{unit}" if unit else None,
                         rows_data, sources_text, note=note, first_col_width=44, source_height=130)


RESTATEMENT_NOTE = (
    "FY2022 shown here as originally published in the Pillar 3 Disclosures 2022 (Tier 1 "
    "GBP55,465k, Own funds GBP71,130k, RWA GBP453,124k, Total Capital Ratio 15.70%). The "
    "Pillar 3 Disclosures 2023's FY2022 comparative restates this to Tier 1 GBP54,760k, Own "
    "funds GBP70,425k, RWA GBP453,125k, Total Capital Ratio 15.54% - the same restatement "
    "documented on the Cash Flow Statement sheet, consistent with the FY2022 Annual Report's "
    "own auditor's report flagging 'prior year adjustments and ongoing regulatory "
    "investigation'."
)

EARLY_YEARS_NOTE = (
    "FY2014-FY2017 (HD-017 extension): see this workbook's entity-level source note for the "
    "Basel III/CET1-terminology and 'Tier 2 capital' source-labelling caveats that apply to "
    "these four years' Pillar 3 figures. FY2018-FY2020 have no Pillar 3 disclosure at all "
    "(genuine archive gap) - left blank on this sheet."
)

# ---------------------------------------------------------------
# Sheet: KM1 Key Metrics (KM1-005) - documented NOT APPLICABLE
# ---------------------------------------------------------------
# BOA UK publishes a Pillar 3 every year and does NOT use the UK KM1 template.
# That is a different finding from "no Pillar 3 is published" (map rule 8), and
# it is recorded here on positive evidence rather than on a failed search.
KM1_SOURCES = (
    "UK KM1 - KEY METRICS TEMPLATE: NOT USED BY THIS BANK IN ANY YEAR.\n"
    "This is not the same finding as 'no Pillar 3 is published'. BOA UK publishes a Pillar 3 disclosure every "
    "year and the recent editions are carried and cited throughout this workbook; what they do not contain is "
    "the prescribed KM1 template. Recorded on positive evidence, checked 2026-09-16.\n"
    "\n"
    "WHAT WAS CHECKED. The FY2024, FY2023 and FY2022 editions were fetched live (HTTP 200, "
    "Content-Type application/pdf, %PDF magic bytes; 929,719 / 972,691 / 991,180 bytes; 36, 38 and 35 pages) "
    "and read in full. All three are text-native, extracting 121,946 / 112,368 / 109,444 characters - roughly "
    "3,000 characters a page - so the absences below are facts about the documents, not about the extractor "
    "(map rule 15). Each contains ZERO occurrences of 'KM1' case-insensitively, and zero occurrences of any "
    "other template code: no UK OV1, CC1, CC2, LR2, LIQ1 or LIQ2 caption appears anywhere in any of them. The "
    "section structure is narrative throughout - 1. INTRODUCTION, 2. RISK MANAGEMENT OBJECTIVES AND POLICIES, "
    "3. OVERVIEW OF THE RISK MANAGEMENT FRAMEWORK, 4. OWN FUNDS, 5. CREDIT RISK, 7. UNENCUMBERED ASSETS, "
    "8. USE OF ECAIS, 9. MARKET AND LIQUIDITY RISK, 10. OPERATIONAL RISK, 11. LEVERAGE RATIO, "
    "12. SECURITISATION, 13. FINANCIAL RISK FROM CLIMATE CHANGE, 14. GLOSSARY.\n"
    "\n"
    "THE 'KEY METRICS' SECTION IS A PICTURE OF FOUR BAR CHARTS, NOT A TABLE.\n"
    "Section 1.1.4 KEY METRICS, on p.6 of each edition, carries a heading and then an embedded image where a "
    "table would sit (954x606 px in FY2022, 729x393 in FY2023, 879x526 in FY2024), with only 18 digits of "
    "extractable text on the whole page. That is exactly the signature of map rule 13 - a table hidden inside a "
    "bitmap in an otherwise text-native PDF - so the page was rendered at 300dpi and READ, which is what the "
    "rule requires before any conclusion. It is not a hidden table: it is four bar charts titled OWN FUNDS, "
    "CREDIT RWA, LEVERAGE RATIO and LCR RATIO, each plotting three years. A chart is not the template and its "
    "bars are not template rows, so nothing from it is transcribed onto a KM1 sheet.\n"
    "\n"
    "AND THE CHARTS DO NOT RECONCILE TO THE SAME DOCUMENT'S OWN TABLES, which is the second reason not to use "
    "them. In the FY2022 edition the OWN FUNDS chart plots 63.2 for 2022, while that edition's own capital "
    "table on p.17 prints Own funds of 71,130 (£'000) for the same date; its CREDIT RWA chart plots 459,714 "
    "for 2022 against Risk Weighted Assets of 453,124 in that table. The single-metric sheets in this workbook "
    "take their figures from those TABLES, which is why they are unaffected.\n"
    "\n"
    "THE CHARTS ALSO RESTATE BETWEEN EDITIONS (map rule 1), consistent with the restatement already documented "
    "on the capital sheets: 2022 OWN FUNDS is plotted as 63.2 in the FY2022 edition but 70.4 in both the "
    "FY2023 and FY2024 editions, and 2022 CREDIT RWA as 459,714 then 453,125. Leverage (13.98% for 2022) and "
    "LCR (207% for 2022) plot identically in all three.\n"
    "\n"
    "NO ARTICLE 432 EXCLUSION IS CLAIMED (map rule 10): none of the three editions contains an 'excluded "
    "templates' appendix, or any occurrence of 'Article 432', 'excluded template' or 'omitted'. The bank "
    "states the opposite - 'The Bank does not seek any exemption from disclosure based on materiality or based "
    "on proprietary or confidential information' (s.1.1.5, all three editions). So the template is absent "
    "because this bank does not use it, not because its rows were formally excluded.\n"
    "\n"
    "A NOTE ON HOW THIS WAS NEARLY MISSED, for whoever re-checks: a case-sensitive search for 'KM1|Key "
    "metric' returns NOTHING in any of the three editions, because the heading is printed 'KEY METRICS' in "
    "capitals. The zero was the search's, not the bank's (map rule 15).\n"
    "\n"
    "LATEST-EDITION CHECK, 2026-09-16: the bank's own disclosures index "
    f"({BOA_FINANCES_URL}, HTTP 200, not blocked) lists exactly five Pillar 3 reports - 2024, 2023, 2022, 2017 "
    "and 2015. The newest is the Pillar 3 Disclosure Report 2024, already carried and cited by this script. "
    "NONE NEWER. FY2025 has no Pillar 3 edition yet; that year's capital figures come from the FY2025 Annual "
    "Report, as the single-metric sheets' own citations state.\n"
    "\n" + ENTITY_NOTE
)

bw.add_km1_sheet(
    title="Bank of Africa United Kingdom Plc - KM1 Key Metrics",
    subtitle="Not applicable: this bank publishes a Pillar 3 every year but does not use the UK KM1 template "
             "in any of them. Its own 'Key Metrics' section is a four-panel bar chart embedded as a picture, "
             "whose values do not reconcile to the same document's capital tables. See the sources note for "
             "the positive evidence and for what was checked.",
    rows=[("DATA", "UK KM1 - Key metrics template: not used by this bank in any year",
           {y: "Not applicable" for y in YEARS})],
    sources_text=KM1_SOURCES,
    first_col_width=64,
    source_height=300,
    years=YEARS,
)

metric(
    "CET1 Capital", "£'000",
    [("Common Equity Tier 1 (CET1) capital (= Tier 1 capital; wholly CET1, no AT1 instruments)",
      {"FY2025": 41047, "FY2024": 45680, "FY2023": 44826, "FY2022": 55465, "FY2021": 59466,
       "FY2017": 60536, "FY2016": 51512, "FY2015": 45544, "FY2014": 40825})],
    p3_sources(), note=RESTATEMENT_NOTE + "\n\n" + EARLY_YEARS_NOTE,
)

metric(
    "CET1 Ratio", "%",
    [("CET1 Ratio (= Tier 1 Capital Ratio)",
      {"FY2025": "17.46%", "FY2024": "19.65%", "FY2023": "17.75%", "FY2022": "12.24%", "FY2021": "12.36%",
       "FY2017": "15.1%", "FY2016": "13.0%", "FY2015": "12.6%", "FY2014": "13.3%"})],
    p3_sources(), note=RESTATEMENT_NOTE + "\n\n" + EARLY_YEARS_NOTE,
)

metric(
    "Tier 1 Capital", "£'000",
    [("Tier 1 Capital",
      {"FY2025": 41047, "FY2024": 45680, "FY2023": 44826, "FY2022": 55465, "FY2021": 59466,
       "FY2017": 60536, "FY2016": 51512, "FY2015": 45544, "FY2014": 40825})],
    p3_sources(), note=RESTATEMENT_NOTE + "\n\n" + EARLY_YEARS_NOTE,
)

metric(
    "Tier 1 Ratio", "%",
    [("Tier 1 Capital Ratio",
      {"FY2025": "17.46%", "FY2024": "19.65%", "FY2023": "17.75%", "FY2022": "12.24%", "FY2021": "12.36%",
       "FY2017": "15.1%", "FY2016": "13.0%", "FY2015": "12.6%", "FY2014": "13.3%"})],
    p3_sources(), note=RESTATEMENT_NOTE + "\n\n" + EARLY_YEARS_NOTE,
)

metric(
    "Total Capital", "£'000",
    [("Total Capital / Own Funds (Tier 1 + Tier 2)",
      {"FY2025": 56485, "FY2024": 60323, "FY2023": 60197, "FY2022": 71130, "FY2021": 74498,
       "FY2017": 76231, "FY2016": 66652, "FY2015": 58545, "FY2014": 54600})],
    p3_sources(), note=RESTATEMENT_NOTE + "\n\n" + EARLY_YEARS_NOTE,
)

metric(
    "Total Capital Ratio", "%",
    [("Total Capital Ratio (Solvency Ratio)",
      {"FY2025": "24.03%", "FY2024": "25.95%", "FY2023": "23.83%", "FY2022": "15.70%", "FY2021": "15.49%",
       "FY2017": "19.0%", "FY2016": "16.9%", "FY2015": "16.2%", "FY2014": "17.9%"})],
    p3_sources(), note=RESTATEMENT_NOTE + "\n\n" + EARLY_YEARS_NOTE,
)

metric(
    "Total RWAs", "£'000",
    [("Total Risk Weighted Assets (Credit RWA)",
      {"FY2025": 235076, "FY2024": 232412, "FY2023": 252608, "FY2022": 453124, "FY2021": 480918,
       "FY2017": 401388, "FY2016": 395244, "FY2015": 360523, "FY2014": 305024})],
    p3_sources(), note=EARLY_YEARS_NOTE,
)

RWA_BREAKDOWN_PRESENTATION_NOTE = (
    "PRESENTATION NOTE: FY2025 category breakdown not available - no FY2025 Pillar 3 "
    "disclosure has been published yet (same gap already noted on the Total RWAs and other "
    "Pillar 3 sheets), so only the aggregate Total RWA figure exists for that year and it is "
    "(re-confirmed 2026-09-12: bank's own finances.html page still lists Pillar3-Disclosures-2024.pdf "
    "as the latest, no 2025 edition) "
    "not repeated on this sheet. FY2023's category breakdown (Credit risk 167,168 + CCR 447 + "
    "Market risk 45,736 + Operational risk 39,255 = 252,606) is £2k below the Total RWAs "
    "sheet's own FY2023 total of 252,608 - both figures are transcribed exactly as each "
    "source document states them; not reconciled further. FY2022 and FY2021 totals tie exactly "
    "to the Total RWAs sheet (453,124 and 480,918 respectively). HD-017 extension: FY2017's "
    "own breakdown (Credit risk 292,139 + CCR 225 + Market risk 77,898 + Operational risk "
    "31,126 = 401,388) and FY2016's comparative in the same document (Credit risk 277,878 + "
    "CCR 226 + Market risk 90,900 + Operational risk 26,239 = 395,244) both tie exactly to "
    "the Total RWAs sheet. FY2014/FY2015's Pillar 3 documents disclose Pillar 1 capital "
    "requirements by exposure class (sovereign/institution/corporate/retail/other), not by "
    "risk type (credit/market/operational) - not the same breakdown shape as this sheet, so "
    "not included here; FY2018-FY2020 have no Pillar 3 disclosure at all (see entity note)."
)
RWA_BREAKDOWN_SOURCES = (
    "Sources - Bank of Africa United Kingdom Plc's own Pillar 3 Disclosures, 'Overview of Risk "
    "Weighted Assets and Minimum Capital Required under Pillar 1' table, GBP'000:\n"
    f"FY2024 (& FY2023 comparative): Pillar 3 Disclosures 2024, p.22 - {P3_2024_URL}\n"
    f"FY2023 (used as primary column): Pillar 3 Disclosures 2023, p.22 - {P3_2023_URL}\n"
    f"FY2022 (used as primary column, & FY2021 comparative): Pillar 3 Disclosures 2022, p.18-19 - {P3_2022_URL}\n"
    f"FY2017 (used as primary column, & FY2016 comparative): Pillar III Disclosures 2017, p.16 - {P3_2017_URL}\n\n"
    + RWA_BREAKDOWN_PRESENTATION_NOTE
)

rwa_breakdown_rows = [
    ("DATA", "Credit risk (excluding counterparty credit risk)", {"FY2024": 194090, "FY2023": 167168, "FY2022": 345166, "FY2021": 238172, "FY2017": 292139, "FY2016": 277878}),
    ("DATA", "Counterparty credit risk (of which CVA)", {"FY2024": 1442, "FY2023": 447, "FY2022": 246, "FY2021": 350, "FY2017": 225, "FY2016": 226}),
    ("DATA", "Market risk", {"FY2024": 7152, "FY2023": 45736, "FY2022": 67257, "FY2021": 206395, "FY2017": 77898, "FY2016": 90900}),
    ("DATA", "Operational risk", {"FY2024": 29727, "FY2023": 39255, "FY2022": 40455, "FY2021": 36001, "FY2017": 31126, "FY2016": 26239}),
    ("TOTAL", "Total RWA", {"FY2024": 232412, "FY2023": 252606, "FY2022": 453124, "FY2021": 480918, "FY2017": 401388, "FY2016": 395244}),
]

bw.add_rwa_breakdown_sheet(
    title="Bank of Africa United Kingdom Plc — RWA Breakdown",
    subtitle="Overview of Risk Weighted Assets under Pillar 1, entity-level (solo) basis",
    rows=rwa_breakdown_rows,
    sources_text=RWA_BREAKDOWN_SOURCES,
    first_col_width=54,
)

metric(
    "Leverage Ratio", "%",
    [("Leverage Ratio",
      {"FY2024": "17.67%", "FY2023": "20.66%", "FY2022": "13.98%", "FY2021": "11.51%",
       "FY2017": "12.08%", "FY2016": "9.62%"})],
    p3_sources(
        "\n\nFY2025 leverage ratio not found - left blank rather than guessed. Re-verified "
        "independently on 15 September 2026, three ways: (1) the bank's own finances.html "
        "index still lists Pillar3-Disclosures-2024.pdf as the newest Pillar 3 edition, with "
        "no 2025 entry; (2) four filename permutations for a 2025 edition "
        "(Pillar3-Disclosures-2025.pdf, BOA_UK_Pillar_III_2025.pdf, "
        "Pillar3_Disclosures_2025.pdf, Pillar3-Disclosures-2025_.pdf) all return HTTP 404 "
        "while the 2024 file at the same path still serves a real 929KB PDF, so the site is "
        "live and the absence is real rather than a broken path; (3) the FY2025 Annual Report "
        "(Companies House, a 100-page scanned image-only filing, Creator 'go-tiff2pdf', with "
        "no text layer at all) was rendered at 200 dpi and OCR'd in full - all 100 pages - "
        "and contains ZERO occurrences of the word 'leverage' anywhere in the document, not "
        "merely in the Strategic Report. Its capital note discloses Tier 1 capital of £41.05m "
        "(2024: £41.44m) but no exposure measure and no leverage ratio, so the ratio is not "
        "derivable either. FY2015/FY2014: leverage ratio not disclosed in either year's "
        "Pillar 3 document - plausible, since the UK leverage ratio framework (and its "
        "public disclosure requirement) only phased in from 2016 onward; left blank rather "
        "than guessed. FY2018-FY2020: no Pillar 3 disclosure at all (see entity note)."
    ),
    note="No FY2025 figure - a confirmed disclosure gap, not an unchecked one. See the source note for the "
         "three-way verification (site index, filename permutations against a live control file, and a full "
         "100-page OCR of the scanned FY2025 Annual Report) carried out on 15 September 2026.",
)

metric(
    "LCR", "%",
    [("Liquidity Coverage Ratio",
      {"FY2025": "212%", "FY2024": "207%", "FY2023": "351%", "FY2022": "207%", "FY2021": "203%",
       "FY2017": "158%", "FY2016": "143%", "FY2015": "160%"})],
    p3_sources(
        "\n\nBASIS NOTE: FY2021-FY2024 are point-in-time (31 December) LCR from each year's "
        "own Pillar 3 KM1 disclosure (FY2024's 207% independently verified by reconstructing "
        "the LCR composition table: HQLA GBP54,641k / net cash outflows GBP26,427k = 206.75% "
        "≈ 207%). FY2025 (212%) is instead the *average LCR throughout the year* as stated "
        "in the FY2025 Annual Report's 'Liquidity and funding' section (no Pillar 3 edition "
        "exists yet for FY2025) - the FY2025 Annual Report separately states FY2024's average "
        "LCR as 228%, a different basis to the 207% point-in-time figure used for FY2024 "
        "above, kept for consistency with every other year in this row. Same "
        "spot-vs-average distinction documented across this project (e.g. ALRAYAN Bank). "
        "FY2017/FY2016/FY2015 come from the FY2017 Pillar 3 document's own 3-year bar chart "
        "(basis not separately stated in that document - not confirmed spot vs. average). "
        "FY2014: not disclosed - plausible, since the EU LCR requirement only phased in from "
        "October 2015; left blank rather than guessed. FY2018-FY2020: no Pillar 3 disclosure "
        "at all (see entity note)."
    ),
    note="FY2025 is an average-throughout-year figure (Annual Report); FY2021-FY2024 are "
         "point-in-time at 31 December (Pillar 3 KM1); FY2015-FY2017's own basis is not "
         "stated in their source document - see source note.",
)

metric(
    "NSFR", "%",
    [("Net Stable Funding Ratio",
      {"FY2025": "173%", "FY2024": "146%"})],
    p3_sources(
        "\n\nNSFR is not quantified in any Pillar 3 KM1 disclosure found (FY2022-FY2024 "
        "editions mention only that the Bank 'monitors net stable funding ratio' "
        "qualitatively). FY2024 and FY2025 figures instead come from the FY2025 Annual "
        "Report's 'Liquidity and funding' narrative. FY2021-FY2023 not found anywhere - left "
        "blank rather than guessed (plausible given the UK NSFR requirement only took effect "
        "from 1 January 2022). FY2014-FY2020: not disclosed in any document checked "
        "during the HD-017 extension - plausible for the same pre-2022 reason; left blank."
    ),
    note="FY2014-FY2023 not publicly disclosed - see source note.",
)

bw.add_not_disclosed_metric_sheets(
    ["MREL Ratio"],
    "No MREL disclosure found in any Annual Report or Pillar 3 document for any year "
    "(FY2014-FY2025) - no numeric ratio and no qualitative exemption statement either. BOA "
    "UK is a small, non-systemic entity; plausibly below the Bank of England's "
    "MREL-setting threshold throughout (the UK MREL framework itself dates from 2016), but "
    "left as not disclosed rather than assumed. Official Bank of Africa UK financial reports "
    f"and Pillar 3 disclosures archive reviewed: {BOA_FINANCES_URL}. The available official "
    f"Pillar 3 reports are also cited directly above (2015: {P3_2015_URL}; 2017: "
    f"{P3_2017_URL}; 2022: {P3_2022_URL}; 2023: {P3_2023_URL}; 2024: {P3_2024_URL}).",
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {"FY2025": 328964, "FY2024": 291532, "FY2023": 254441, "FY2022": 452390, "FY2021": 496686, "FY2020": 485372, "FY2019": 466248, "FY2018": 575063, "FY2017": 490960, "FY2016": 527718, "FY2015": 441682, "FY2014": 365352}),
        ("Loans and advances to customers", {"FY2025": 41952, "FY2024": 28985, "FY2023": 28332, "FY2022": 148285, "FY2021": 162016, "FY2020": 173173, "FY2019": 215391, "FY2018": 211596, "FY2017": 207964, "FY2016": 175945, "FY2015": 167713, "FY2014": 149257}),
        ("Due to customers", {"FY2025": 84367, "FY2024": 44717, "FY2023": 42227, "FY2022": 59541, "FY2021": 92028, "FY2020": 99556, "FY2019": 95291, "FY2018": 109231, "FY2017": 112349, "FY2016": 129706, "FY2015": 98537, "FY2014": 101419}),
        ("Total equity", {"FY2025": 70629, "FY2024": 68171, "FY2023": 65526, "FY2022": 75751, "FY2021": 82581, "FY2020": 82643, "FY2019": 80820, "FY2018": 75454, "FY2017": 77889, "FY2016": 71557, "FY2015": 60676, "FY2014": 54324}),
    ],
    balance_sheet_unit="£'000",
    income_statement_totals=[
        ("Net operating income", {"FY2025": 10040, "FY2024": 8598, "FY2023": 4178, "FY2022": 19505, "FY2021": 24597, "FY2020": 18707, "FY2019": 21424, "FY2018": 17468, "FY2017": 20330, "FY2016": 20578, "FY2015": 16164, "FY2014": 14148}),
        ("Total operating expenses", {"FY2025": -10659, "FY2024": -14904, "FY2023": -17662, "FY2022": -19458, "FY2021": -17889, "FY2020": -16851, "FY2019": -16677, "FY2018": -14900, "FY2017": -12012, "FY2016": -10632, "FY2015": -10502, "FY2014": -7959}),
        ("Profit/(Loss) for the year", {"FY2025": 2273, "FY2024": 1779, "FY2023": -13999, "FY2022": -3839, "FY2021": 5682, "FY2020": 1097, "FY2019": 2622, "FY2018": 2169, "FY2017": 5510, "FY2016": 8584, "FY2015": 7795, "FY2014": 5708}),
    ],
    income_statement_unit="£'000",
    equity_changes_totals=[
        ("Opening equity", {"FY2025": 68171, "FY2024": 65526, "FY2023": 75034, "FY2022": 82581, "FY2021": 82378, "FY2020": 80820, "FY2019": 75488, "FY2018": 76434, "FY2017": 71557, "FY2016": 60676, "FY2015": 54324, "FY2014": 50403}),
        ("Total comprehensive income/(loss) for the year", {"FY2025": 2458, "FY2024": 2645, "FY2023": -9508, "FY2022": -6830, "FY2021": 203, "FY2020": 1823, "FY2019": 5332, "FY2018": 501, "FY2017": 6332, "FY2016": 10881, "FY2015": 7441, "FY2014": 3921}),
        ("Other equity movements, net", {"FY2025": 0, "FY2024": 0, "FY2023": 0, "FY2022": 0, "FY2021": 0, "FY2020": 0, "FY2019": 0, "FY2018": 0, "FY2017": 0, "FY2016": 0, "FY2015": 0, "FY2014": 0}),
        ("Closing equity", {"FY2025": 70629, "FY2024": 68171, "FY2023": 65526, "FY2022": 75751, "FY2021": 82581, "FY2020": 82643, "FY2019": 80820, "FY2018": 75454, "FY2017": 77889, "FY2016": 71557, "FY2015": 60676, "FY2014": 54324}),
    ],
    equity_changes_unit="£'000",
    cash_flow_totals=[
        ("Net cash flows from/(used in) operating activities", {"FY2025": -23853, "FY2024": 10670, "FY2023": -10115, "FY2022": -27463, "FY2021": 60094, "FY2020": -4205, "FY2019": -77756, "FY2018": 64083, "FY2017": -85771, "FY2016": 53990, "FY2015": 59479, "FY2014": 50546}),
        ("Net cash flows from/(used in) investing activities", {"FY2025": 10389, "FY2024": -13994, "FY2023": -3057, "FY2022": 9089, "FY2021": -43971, "FY2020": 30693, "FY2019": 35146, "FY2018": -48205, "FY2017": 42174, "FY2016": -52666, "FY2015": -44402, "FY2014": -25947}),
        ("Net cash flows from/(used in) financing activities", {"FY2025": -89, "FY2024": -181, "FY2023": -797, "FY2022": -1050, "FY2021": -944, "FY2020": -1107, "FY2019": -877, "FY2018": 635, "FY2017": 629, "FY2016": 0, "FY2015": 0, "FY2014": 0}),
        ("Cash and cash equivalents as at 31 December", {"FY2025": 37517, "FY2024": 51070, "FY2023": 54575, "FY2022": 68544, "FY2021": 87968, "FY2020": 72789, "FY2019": 47408, "FY2018": 90895, "FY2017": 74382, "FY2016": 117350, "FY2015": 116026, "FY2014": 100949}),
    ],
    cash_flow_unit="£'000",
    ratios=[
        ("CET1 Ratio", {"FY2025": "17.46%", "FY2024": "19.65%", "FY2023": "17.75%", "FY2022": "12.24%", "FY2021": "12.36%", "FY2017": "15.1%", "FY2016": "13.0%", "FY2015": "12.6%", "FY2014": "13.3%"}),
        ("Total Capital Ratio", {"FY2025": "24.03%", "FY2024": "25.95%", "FY2023": "23.83%", "FY2022": "15.70%", "FY2021": "15.49%", "FY2017": "19.0%", "FY2016": "16.9%", "FY2015": "16.2%", "FY2014": "17.9%"}),
        ("Leverage Ratio", {"FY2024": "17.67%", "FY2023": "20.66%", "FY2022": "13.98%", "FY2021": "11.51%", "FY2017": "12.08%", "FY2016": "9.62%"}),
        ("LCR", {"FY2025": "212%", "FY2024": "207%", "FY2023": "351%", "FY2022": "207%", "FY2021": "203%", "FY2017": "158%", "FY2016": "143%", "FY2015": "160%"}),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own "
         "source citation for the underlying document/page, and the Cash Flow Statement / Statement of "
         "Changes in Equity sheets' source notes for the several genuine restatements affecting this "
         "workbook (FY2022, FY2017, and a further FY2020/FY2021 break - see entity note). FY2018-FY2020 "
         "have no Pillar 3 ratios (genuine archive gap, confirmed during the HD-017 historical-depth "
         "extension); FY2014-FY2020 Balance Sheet/P&L/Cash Flow/Equity figures were added in that same "
         "extension.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/BANK OF AFRICA UK FINANCIALS.xlsx")
print("Saved.")
