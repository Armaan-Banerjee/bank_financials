import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021", "FY2020", "FY2019"]

AR2025_URL = "https://www.ghanabank.co.uk/app/uploads/2026/04/GHIB-ANNUAL-REPORT-2025-2-page-view.pdf"
AR2024_URL = "https://www.ghanabank.co.uk/app/uploads/2025/04/GHIB-ANNUAL-REPORT-2024.pdf"
AR2022_URL = "https://www.ghanabank.co.uk/app/uploads/2023/03/GHIB-Annual-Report-and-Financial-Statements-2022-.pdf"

# FY2025 edition located 2026-09-18, the DAY IT WAS UPLOADED (the Bank's own
# WordPress media index dates it 2026-09-18T14:45:36; the PDF's own CreationDate
# is 18 September 2026 11:27 BST). Found by querying that media endpoint, not by
# guessing a path - GHIB's /legal-documents/ and homepage still linked only the
# FY2024 edition at the time. It arrives ~2 months EARLIER in the year than the
# ~November cadence this script previously projected. It is also the FIRST GHIB
# edition whose key-metrics table is LIVE TEXT rather than a pasted bitmap
# (Creator: Adobe Illustrator 29.8), so unlike FY2019-FY2024 it did not have to
# be read visually.
P3_2025_URL = "https://www.ghanabank.co.uk/app/uploads/2026/09/GHIB-2025-Pillar-3-Disclosures.pdf"
P3_2024_URL = "https://www.ghanabank.co.uk/app/uploads/2025/11/GHIB-2024-Pillar-3-Disclosures.pdf"
P3_2023_URL = "https://www.ghanabank.co.uk/app/uploads/2024/11/GHIB-2023-Pillar-3-Disclosures.pdf"
P3_2022_URL = "https://www.ghanabank.co.uk/app/uploads/2023/09/GHIB-2022-Pillar-3-Disclosures.pdf"
P3_2021_URL = "https://www.ghanabank.co.uk/app/uploads/2022/10/GHIB-2021-Pillar-3-Disclosures.pdf"
# FY2020 and FY2019 editions located 2026-09-15 - see P3_DISCOVERY_NOTE. Both verified
# (%PDF magic bytes; cover and running header read "GHIB Pillar 3 Disclosures / as at
# 31st December <year>", "Ghana International Bank plc"). They fill FY2019/FY2020 cells
# that had been blank or carried only lower-precision Annual Report figures.
P3_2020_URL = "https://www.ghanabank.co.uk/app/uploads/2021/06/Pillar-3-Disclosures-2020.pdf"
P3_2019_URL = "https://www.ghanabank.co.uk/app/uploads/2020/11/GHIB-2019-Pillar-3-Disclosures_FINAL_publish-on-website.pdf"

# ---------------------------------------------------------------------------
# HOW THESE DOCUMENTS WERE FOUND, AND WHY THAT MATTERS FOR ANY NEGATIVE HERE.
#
# GHIB HAS NO ENUMERATING INDEX PAGE. https://www.ghanabank.co.uk/about-us/
# (fetched with curl 2026-09-15) links only the LATEST set of documents - the
# FY2024 and FY2025 Annual Reports, the FY2025 summary and 5-year financials,
# and the FY2024 Pillar 3. It is a "current documents" page, not a history, so
# it CANNOT be used to establish that a given year was never published.
#
# Every Pillar 3 URL above was therefore found by SEARCH, not by enumeration.
# That distinction is the whole point of this note: an absence established by
# search is a WEAK NEGATIVE (nobody indexed it / it was not found), whereas an
# absence established against a bank's own complete index is a STRONG NEGATIVE
# (the bank itself lists what exists and this is not on the list). Both
# negatives recorded for this bank - "nothing before FY2019" and "no FY2025
# edition yet" - rest on search alone and must be treated as re-checkable, NOT
# as settled. Do not let a later pass promote either into a permanent negative
# without an index or an explicit statement from the Bank.
#
# ALSO: ghanabank.co.uk FAILS TLS VERIFICATION for WebFetch ("unable to verify
# the first certificate"). Use curl. A fetch failure here is a transport
# problem, not evidence that a document is missing.
# ---------------------------------------------------------------------------
P3_DISCOVERY_NOTE = (
    "SOURCING METHOD AND THE STRENGTH OF THE NEGATIVES (recorded 2026-09-15). Ghana "
    "International Bank has NO enumerating index page: https://www.ghanabank.co.uk/about-us/ "
    "links only the latest set of documents (FY2024/FY2025 Annual Reports, FY2025 summary and "
    "5-year financials, FY2024 Pillar 3), not a document history. Every Pillar 3 edition cited "
    "here was therefore located by SEARCH rather than by enumerating the Bank's own list. This "
    "matters for how much weight the negatives below can carry: an absence found by search is a "
    "WEAK negative (it was not found), whereas an absence checked against a bank's own complete "
    "index is a STRONG negative (the bank lists what exists and this is not on it). Both "
    "negatives recorded for this bank - that no Pillar 3 edition exists before FY2019, and that "
    "no FY2025 edition is posted yet - are weak, search-based negatives and are RE-CHECKABLE, "
    "not settled. A future pass must not promote either into a permanent negative without "
    "either an index page or an explicit statement from the Bank. Separately: ghanabank.co.uk "
    "fails TLS verification for WebFetch; use curl. A fetch failure on this domain is a "
    "transport problem and is not evidence that a document is missing."
)

CH_2020_URL = "https://find-and-update.company-information.service.gov.uk/company/03468216/filing-history/MzI5NzMxNjk1NWFkaXF6a2N4/document?format=pdf&download=0"
CH_2019_URL = "https://find-and-update.company-information.service.gov.uk/company/03468216/filing-history/MzI1OTU0MzQ4NmFkaXF6a2N4/document?format=pdf&download=0"

CASH_FLOW_NOTE = (
    "Note: FY2023/FY2024/FY2025 statements include an additional adjustment line, 'Net interest "
    "income and other non-cash items', not present in the FY2021/FY2022 presentation - this is a "
    "genuine year-on-year presentation change by the Bank, not a missing figure; the blank cells for "
    "FY2021/FY2022 reflect that this split simply wasn't disclosed that way in those years' accounts. "
    "Section totals (net cash from operating/investing/financing activities, cash and cash equivalents) "
    "are consistent and comparable across all 6 years."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are Ghana International Bank Plc's own Statement of Cash Flow, £:\n"
    f"FY2025 & FY2024: Annual Report and Financial Statements 2025, p.76 (Statement of Cash Flow) - {AR2025_URL}\n"
    f"FY2024 & FY2023: Annual Report and Financial Statements 2024, p.82 (Statement of cash flow) - {AR2024_URL}\n"
    f"FY2022 & FY2021: Annual Report and Financial Statements 2022, p.49 (Statement of cash flow) - {AR2022_URL}\n"
    "FY2020: Annual Report and Financial Statements 2020, p.40 (supplied Companies House scan; company basis)\n"
    "(FY2022 report is a scanned/image-only Companies House filing with no text layer - transcribed "
    "by direct visual reading of the rendered page.)\n"
    + CASH_FLOW_NOTE
)


def p3_sources(page="4-5"):
    return (
        "Sources - Ghana International Bank Plc Pillar 3 Disclosures, Table 1: Key Metrics ratios:\n"
        f"FY2025: Pillar 3 Disclosures 31 December 2025, p.14 printed (PDF p.13), \"Table1: Key Metrics "
        f"ratios as at 31 December 2025\" - {P3_2025_URL}\n"
        f"FY2024: Pillar 3 Disclosures 31 December 2024, p.{page} - {P3_2024_URL}\n"
        f"FY2023: Pillar 3 Disclosures 31 December 2023, p.5 - {P3_2023_URL}\n"
        f"FY2022: Pillar 3 Disclosures 31 December 2022, p.4 - {P3_2022_URL}\n"
        f"FY2021: Pillar 3 Disclosures 31 December 2021, p.4 - {P3_2021_URL}\n"
        f"FY2020: Pillar 3 as at 31st December 2020, Table 1 'Key capital resources, capital, leverage and "
        f"liquidity ratios', p.8 - {P3_2020_URL}\n"
        f"FY2019: Pillar 3 as at 31st December 2019, Table 1 'Key capital resources, capital, leverage and "
        f"liquidity ratios', p.9 (that page is an image in the PDF - the table was read VISUALLY from the "
        f"rendered page, not OCR'd, per this project's rule that OCR output must be eye-checked) - "
        f"{P3_2019_URL}\n"
        "The FY2020 and FY2019 editions were located 2026-09-15; before that the script had no Pillar 3 "
        "source for either year and fell back to the Annual Report for FY2020 (LCR 310%, CET1 ratio 35.3%) "
        "with FY2019 left blank throughout. The Pillar 3 figures reproduce those Annual Report values at "
        "higher precision (LCR 310.06%, CET1 ratio 35.33%), so the validation gate passes and they are "
        "upgrades rather than conflicts.\n"
        + P3_DISCOVERY_NOTE + "\n"
        + FY2025_SOURCE_NOTE
    )


# FY2025 Pillar 3 not published as at 15 September 2026: GHIB's own website
# (homepage, /about-us/ and /legal-documents/, all re-checked 15 Sep 2026) still
# lists the FY2024 Pillar 3 as the latest, and every 2026 upload-folder
# permutation of the FY2024 filename 404s. Pillar 3 reports historically follow
# the Annual Report by ~7 months (FY2024 Pillar 3 published November 2025, seven
# months after the FY2024 Annual Report), so the FY2025 edition is expected
# around November 2026. The capital figures we DO have for FY2025 therefore come
# from the Annual Report instead, which the Directors' Report and Note 37 state
# directly. Those two bases agree for this bank: the AR2025 comparatives
# reproduce the Pillar 3 FY2024 figures (CET1 "£156.7m" vs 156,657; ratio "22.4%"
# vs 22.37%), and the AR2024's own year-end LCR of 256% matches the FY2024
# Pillar 3 LCR of 256.31%.
FY2025_SOURCE_NOTE = (
    "FY2025 NOW COMES FROM ITS OWN PILLAR 3, FOUND 2026-09-18 - THIS SHEET'S FY2025 SOURCE CHANGED ON "
    "THAT DATE. Until 18 September 2026 this workbook recorded that no FY2025 Pillar 3 existed and filled "
    "FY2025 from the Annual Report instead. That was correct when written: GHIB's homepage and "
    "/legal-documents/ still linked only the FY2024 edition, and the projected publication date was "
    "~November 2026 on the historical ~7-month lag after the Annual Report. The FY2025 edition was in "
    "fact uploaded on 18 September 2026 - the Bank's own WordPress media index "
    "(/wp-json/wp/v2/media?search=pillar) dates it 2026-09-18T14:45:36 and the PDF's own CreationDate is "
    "18 September 2026 11:27 BST - two months ahead of that projection, and before any page on the site "
    "linked to it. It was found by querying that media index, not by guessing a filename.\n"
    "WHAT CHANGED AS A RESULT. Total RWAs (751,519), the Leverage Ratio (14.17%), the NSFR (181.39%), the "
    "full RWA Breakdown and the whole KM1 FY2025 column were BLANK and are now populated. CET1/Tier 1/"
    "Total Capital moved from the Annual Report's rounded \"£161.7m\" to the Pillar 3's 161,750; the three "
    "capital ratios from \"21.5%\" to 21.52%; and the LCR from \"213%\" to 213.49%. Those five are the SAME "
    "figures at higher precision, not different ones, so the change is an upgrade and not a conflict - "
    "which is also the validation gate this workbook applied when the FY2020/FY2019 editions were found.\n"
    "The superseded Annual Report citations, kept for traceability: CET1 capital from Annual Report and "
    "Financial Statements 2025, Note 37 'Capital management', p.116 (\"resulted in £161.7m CET1 at 31 "
    "December 2025 (2024: £156.7m)\"); the ratios from its Directors' Report, pp.52-53 (\"GHIB recorded a "
    "CRD IV capital adequacy ratio of 21.5% (2024: 22.4%) with a core tier 1 capital ratio of 21.5% "
    "(2024: 22.4%)\" and \"The Liquidity Coverage Ratio (LCR) as at 31 December 2025 was 213%\").\n"
    "BASIS CHECK: the AR and Pillar 3 bases agree for this bank - AR2025's FY2024 comparatives reproduce "
    "the Pillar 3 FY2024 figures (£156.7m vs 156,657; 22.4% vs 22.37%), and AR2024's year-end LCR of 256% "
    "matches the FY2024 Pillar 3 LCR of 256.31%.\n"
    "TWO FY2025 INTERNAL INCONSISTENCIES IN THE BANK'S OWN FY2025 EDITION, recorded and NOT reconciled - "
    "both are the same defect this workbook already documents for FY2024:\n"
    "  (a) LEVERAGE RATIO. The KM1 row 14 and the section 1.6 narrative both say 14.17% (\"The leverage "
    "ratio as at 31 December 2025 was 14.17%\", p.14 printed), while section 5.14 'Risk of Excessive "
    "Leverage' (p.39 printed, PDF p.38) says \"The Bank's leverage ratio as at 31st of December 2025 was "
    "12.79%\". The Leverage Ratio sheet carries 14.17%, the figure the KM1 and the capital narrative "
    "agree on. The FY2024 edition has exactly the same split (14.66% in KM1/narrative vs 13.9% in its own "
    "section 5.14), and section 5.14 of every GHIB edition captions its ratio as struck on a TRANSITIONAL "
    "definition of Tier 1 capital - see the KM1 sheet's long note for the evidence on this divergence.\n"
    "  (b) PRECISION - AND THIS ONE IS NEW IN FY2025, so verify_workbook.py reports it. KM1 row 17 prints "
    "the LCR as 213.4% and row 20 the NSFR as 181.4%, while Table 13 (p.37 printed) and the section 5.4 "
    "narrative print 213.49% and 181.39%. Each sheet carries the figure appropriate to it: the KM1 sheet "
    "reproduces the template exactly as printed, the LCR and NSFR metric sheets carry the fuller "
    "2dp figures. In FY2024 and earlier the FY-edition KM1 itself printed 2dp (256.31%, 255.98%) so the "
    "two sides agreed and nothing was reported; the FY2025 edition rounds its own KM1 row 17 and row 20 "
    "to 1dp for the 2025 and 2024 columns while leaving 2dp in the 2023/2022/2021 columns. Neither side "
    "has been edited to make the check pass - both are GHIB's own printed figures from the same PDF."
)


NSFR_NOTE = (
    "The Bank's FY2022 Pillar 3 states that comparable NSFR figures for earlier periods are not "
    "available, because the NSFR rules introduced under CRR2 only commenced on 1 January 2022. "
    "CORRECTED 2026-09-15: this sheet previously summarised that as 'NSFR only reported from FY2022 "
    "onward', which is not what the documents show. The Bank's own FY2020 Pillar 3 (Table 1) does "
    "report an NSFR of 198%, with its components, two years before the rules commenced - a voluntary "
    "early disclosure. The Bank's statement is about comparability under the CRR2 definition, not "
    "about whether any NSFR was ever published, and the two should not be conflated. The FY2021 "
    "edition likewise reports an NSFR, of 195% (available stable funding 318,949 / required stable "
    "funding 163,592), repeated in that document's narrative. FY2020 and FY2021 are therefore both "
    "populated from primary disclosures. FY2019 is the only genuine negative on this sheet before "
    "FY2022: that edition's Table 1 was read in full and has no Net Stable Funding Ratio section at "
    "all - the block first appears in the FY2020 edition."
)
NO_AT1_NOTE = "No Additional Tier 1 or Tier 2 instruments disclosed any year - Tier 1/Total Capital equal CET1 Capital throughout."

bw = BankWorkbook(bank_name="Ghana International Bank Plc", years=YEARS, header_color="619578")

STATEMENTS_ENTITY_NOTE = (
    "Ghana International Bank Plc (Company basis, GHIB has no subsidiaries or branches) reports in £ "
    "throughout - no currency conversion applied. Each year's own originally-published figures used "
    "throughout - the Statement of Changes in Equity ties exactly at every year boundary (opening = "
    "prior year's own closing = prior year's own Balance Sheet Total Equity) across all 6 years, zero "
    "plug rows needed.\n"
    "COLUMN-ORDER CAUTION (2025 Annual Report only): the FY2025 Annual Report is published as a "
    "'2-page-view' PDF (two facing pages per PDF page) - naive text extraction interleaves the 2025 and "
    "2024 columns of the Balance Sheet in a way that looks plausible but is backwards (the block of "
    "values immediately following the P&L's 2024 column is actually the Balance Sheet's OWN 2024 "
    "comparative, not FY2025). All figures below were independently confirmed by rendering the actual "
    "page image and by cross-checking every FY2024 figure against the FY2024 Annual Report's own "
    "originally-published Balance Sheet (Company basis) - which are identical, as they must be.\n"
    "PRESENTATION CHANGES: the cash/central-bank balances line is labelled 'Cash and balances at banks "
    "including items in course of collection' in the FY2021/FY2022 reports vs 'Cash and balances at "
    "central banks' FY2023-FY2025 (same line, relabelled - not a new item). 'Right of use assets' only "
    "appears as its own line from FY2023 (lease accounting change). 'Term financing' only appears from "
    "FY2024 (new funding line; nil/not applicable before). 'Current tax asset' was a separate line "
    "FY2021-FY2024 (nil in FY2021/FY2024, £945,584 in FY2022/FY2023) but was dropped entirely from the "
    "FY2025 Annual Report's Balance Sheet structure (both the FY2025 and FY2024-comparative columns) - "
    "left blank for FY2025 as a genuine structural change, not a data gap."
)

STATEMENTS_SOURCES = (
    "Sources - Ghana International Bank Plc's own Statement of Financial Position / Statement of "
    "Comprehensive Income / Statement of Changes in Equity, £:\n"
    f"FY2025 & FY2024: Annual Report and Financial Statements 2025, p.74-77 (Statement of Comprehensive Income, "
    f"Statement of Financial Position, Statement of Changes in Equity) - {AR2025_URL}\n"
    f"FY2024 & FY2023: Annual Report and Financial Statements 2024, p.80-83 (own-year FY2024 figures; "
    f"cross-checked against the FY2025 report's FY2024 comparative column, matched exactly) - {AR2024_URL}\n"
    f"FY2022 & FY2021: Annual Report and Financial Statements 2022, p.46-48 - {AR2022_URL}\n"
    "FY2020: Annual Report and Financial Statements 2020, pp.37-40 (supplied Companies House scan; company basis)\n"
    "FY2019: Annual Report and Financial Statements 2019, pp.25-28 (supplied Companies House scan; company basis)\n"
    + STATEMENTS_ENTITY_NOTE
)

ASSET_QUALITY_SOURCES = (
    "Sources - Ghana International Bank Plc's own 'Provisions for credit losses' note (Note 13/12), "
    "'Total provision for credit losses' table (aggregate IFRS 9 stage reconciliation across placements/"
    "loans to banks, loans to customers, and government/other securities combined), £'000:\n"
    f"FY2025: Annual Report and Financial Statements 2025, p.92-93 - {AR2025_URL}\n"
    f"FY2024 & FY2023: Annual Report and Financial Statements 2024, p.98-99 (own-year closing balances; "
    f"FY2024 closing cross-checked against FY2025's own opening-balance comparative, matched exactly) - {AR2024_URL}\n"
    f"FY2022: Annual Report and Financial Statements 2024, p.99 (FY2022's own closing balance, sourced from "
    f"AR2024's prior-year reconciliation table, since AR2022 itself only discloses ECL by stage without a "
    f"Gross Exposure breakdown at this granularity) - {AR2024_URL}\n"
    f"FY2021: Annual Report and Financial Statements 2022, p.65, 'Provisions for credit losses' note, ECL by "
    f"stage only (no Gross Exposure by stage disclosed this early - table introduced the Gross Exposure "
    f"columns from FY2022 onward) - {AR2022_URL}\n"
    "Net carrying amount by stage = Gross Exposure - ECL allowance for that stage (both are directly "
    "disclosed together in this note). NPL ratio = Stage 3 gross / Total gross; Stage 3 coverage ratio = "
    "Stage 3 ECL / Stage 3 gross; Total ECL coverage ratio = Total ECL / Total gross - all blank for FY2021, "
    "which lacks a Gross Exposure breakdown by stage.\n"
    + STATEMENTS_ENTITY_NOTE
)

GOV_OTHER_SPLIT_SOURCES = (
    "'Government securities' / 'Other investment securities' sub-split of 'Total government and other "
    "securities' - Ghana International Bank Plc's own 'Government and other securities' note, which breaks "
    "the carrying amount down by issuer type, £:\n"
    f"FY2025 & FY2024: Annual Report and Financial Statements 2025, Note 14, p.96-97 - Treasury bills, "
    f"Supranational and multilateral development bank bonds, Other corporate bonds, African sovereign bonds "
    f"- {AR2025_URL}\n"
    f"FY2024 & FY2023: Annual Report and Financial Statements 2024, Note 14, p.99-100 (own-year FY2024 split; "
    f"the FY2024 comparative column in the FY2025 report re-labels part of this year's 'Other corporate "
    f"bonds' as a separate 'Supranational and multilateral development bank bonds' line, but the combined "
    f"'other' total is identical either way, and Treasury bills/African sovereign bonds are unchanged) - "
    f"{AR2024_URL}\n"
    f"FY2022 & FY2021: Annual Report and Financial Statements 2022, Note 13, p.68 - Sovereign bonds - Africa, "
    f"Other corporate bonds, US and German treasury bills - {AR2022_URL}\n"
    f"FY2020 & FY2019: Annual Report and Financial Statements 2020, Note 13, p.53 (Companies House filing, "
    f"company basis) - Sovereign bonds - Africa, Other corporate bonds, US Treasury bills - {CH_2020_URL}\n"
    "'Government securities' = Treasury bills + sovereign/government bonds of any jurisdiction (US, German, "
    "African sovereign, or generic 'Sovereign bonds' lines); 'Other investment securities' = corporate bonds "
    "+ supranational/multilateral development bank bonds (non-sovereign issuers). Both sub-rows reconcile "
    "exactly to 'Total government and other securities' every year - verified by direct summation against "
    "each year's own note.\n"
    "Note: no separate FY2019 Annual Report/Companies House filing was refetched for this split - the "
    "FY2019 figures above are the FY2020 Annual Report's own FY2019 comparative column in the same note, "
    "which is that year's own originally-published breakdown."
)

# ---------------------------------------------------------------
# Sheet: Balance Sheet (Statement of Financial Position), £, own-year
# figures throughout - built FIRST per the equity reconciliation ladder,
# so each year's own Total Equity is an independent check value before
# the equity sheet is built year-by-year.
# ---------------------------------------------------------------
bs_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and balances at central banks", {
        "FY2025": 162234361, "FY2024": 181980487, "FY2023": 256691647, "FY2022": 135432668, "FY2021": 69522404, "FY2020": 75240729, "FY2019": 82248890}),
    ("DATA", "Placements with and loans and advances to banks", {
        "FY2025": 426835273, "FY2024": 471210664, "FY2023": 353387088, "FY2022": 510389547, "FY2021": 499653769, "FY2020": 517900464, "FY2019": 453894935}),
    ("DATA", "Loans and advances to customers", {
        "FY2025": 152082149, "FY2024": 57178671, "FY2023": 53066533, "FY2022": 65038106, "FY2021": 89440019, "FY2020": 72138823, "FY2019": 80109596}),
    ("TOTAL", "Total government and other securities", {
        "FY2025": 428235831, "FY2024": 366183607, "FY2023": 119321238, "FY2022": 170000415, "FY2021": 93657043, "FY2020": 73283983, "FY2019": 54352460}),
    ("DATA", "Government securities", {
        "FY2025": 229201258, "FY2024": 264479047, "FY2023": 111641532, "FY2022": 166175781, "FY2021": 89141697, "FY2020": 71728019, "FY2019": 53558982}),
    ("DATA", "Other investment securities", {
        "FY2025": 199034573, "FY2024": 101704560, "FY2023": 7679706, "FY2022": 3824634, "FY2021": 4515346, "FY2020": 1555964, "FY2019": 793478}),
    ("DATA", "Prepayments and other receivables", {
        "FY2025": 4074887, "FY2024": 5172009, "FY2023": 2778164, "FY2022": 2289462, "FY2021": 2333255, "FY2020": 1940133, "FY2019": 1878511}),
    ("DATA", "Property, plant and equipment", {
        "FY2025": 1407862, "FY2024": 1679557, "FY2023": 1878621, "FY2022": 4139799, "FY2021": 4304452, "FY2020": 3565999, "FY2019": 2621639}),
    ("DATA", "Right of use assets", {"FY2025": 1573125, "FY2024": 2010863, "FY2023": 1605924}),
    ("DATA", "Intangible assets", {
        "FY2025": 7998495, "FY2024": 7829045, "FY2023": 6130633, "FY2022": 5252083, "FY2021": 2527506, "FY2020": 909018}),
    ("DATA", "Current tax asset", {"FY2024": 0, "FY2023": 945584, "FY2022": 945584, "FY2021": 0, "FY2020": 166307}),
    ("DATA", "Deferred tax asset", {
        "FY2025": 405217, "FY2024": 2441160, "FY2023": 4843256, "FY2022": 6362609, "FY2021": 5189176, "FY2020": 1328079, "FY2019": 254870}),
    ("TOTAL", "Total assets", {
        "FY2025": 1184847200, "FY2024": 1095686063, "FY2023": 800648688, "FY2022": 899850273, "FY2021": 766627624, "FY2020": 746473535, "FY2019": 676561478}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Deposits by banks", {
        "FY2025": 570571847, "FY2024": 619446707, "FY2023": 355749487, "FY2022": 368415004, "FY2021": 377412107, "FY2020": 316857125, "FY2019": 297598719}),
    ("DATA", "Amounts owed to depositors", {
        "FY2025": 393649207, "FY2024": 255765401, "FY2023": 270972181, "FY2022": 347038076, "FY2021": 258550273, "FY2020": 276077311, "FY2019": 219743960}),
    ("DATA", "Term financing", {"FY2025": 34616710, "FY2024": 14562133, "FY2023": 0}),
    ("DATA", "Other liabilities", {
        "FY2025": 2726095, "FY2024": 30261027, "FY2023": 6287092, "FY2022": 22784211, "FY2021": 7791171, "FY2020": 18276926, "FY2019": 18914366}),
    ("DATA", "Accruals and deferred income", {
        "FY2025": 8565137, "FY2024": 7184339, "FY2023": 5311755, "FY2022": 3763989, "FY2021": 2808672, "FY2020": 3456111, "FY2019": 3258801}),
    ("TOTAL", "Total liabilities", {
        "FY2025": 1010128996, "FY2024": 927219607, "FY2023": 638320515, "FY2022": 742001280, "FY2021": 646562223, "FY2020": 614667473, "FY2019": 539559387}),
    ("SECTION", "Equity", {}),
    ("DATA", "Ordinary shares", {
        "FY2025": 63739927, "FY2024": 63739927, "FY2023": 63739927, "FY2022": 63739927, "FY2021": 45000000, "FY2019": 45000000}),
    ("DATA", "Share premium", {
        "FY2025": 61212787, "FY2024": 61212787, "FY2023": 61212787, "FY2022": 61212787, "FY2021": 30000000, "FY2019": 30000000}),
    ("DATA", "FVOCI revaluation reserve", {
        "FY2025": 1040762, "FY2024": -656013, "FY2023": -3179954, "FY2022": -4546839, "FY2021": -1420695, "FY2020": 1276842, "FY2019": 1000468}),
    ("DATA", "Profit and loss account", {
        "FY2025": 48724728, "FY2024": 44169755, "FY2023": 40555413, "FY2022": 37443118, "FY2021": 46486096, "FY2020": 55529220, "FY2019": 61001623}),
    ("TOTAL", "Total Equity", {
        "FY2025": 174718204, "FY2024": 168466456, "FY2023": 162328173, "FY2022": 157848993, "FY2021": 120065401, "FY2020": 131806062, "FY2019": 137002091}),
    ("TOTAL", "Total liabilities and equity", {
        "FY2025": 1184847200, "FY2024": 1095686063, "FY2023": 800648688, "FY2022": 899850273, "FY2021": 766627624, "FY2020": 746473535, "FY2019": 676561478}),
]

bw.add_balance_sheet_sheet(
    title="Ghana International Bank Plc — Statement of Financial Position",
    subtitle="Company basis (GHIB has no subsidiaries or branches), £. See source note at bottom.",
    rows=bs_rows,
    sources_text=STATEMENTS_SOURCES + "\n\n" + GOV_OTHER_SPLIT_SOURCES,
    first_col_width=68,
    source_height=460,
    unit_suffix=" (£)",
)

# ---------------------------------------------------------------
# Sheet: Profit & Loss (Statement of Comprehensive Income), £, own-year
# figures throughout.
# ---------------------------------------------------------------
pl_rows = [
    ("SECTION", "Continuing operations", {}),
    ("DATA", "Interest receivable and similar income", {
        "FY2025": 44645524, "FY2024": 45634349, "FY2023": 35055214, "FY2022": 20784717, "FY2021": 11402644, "FY2020": 12054372, "FY2019": 20127664}),
    ("DATA", "Other interest income arising from debt and other fixed income securities", {
        "FY2025": 13537189, "FY2024": 9820312, "FY2023": 9075263, "FY2022": 3177870, "FY2021": 1335400, "FY2020": 2244746, "FY2019": 2326696}),
    ("TOTAL", "Total interest income", {
        "FY2025": 58182713, "FY2024": 55454661, "FY2023": 44130477, "FY2022": 23962587, "FY2021": 12738044, "FY2020": 14299118, "FY2019": 22454360}),
    ("DATA", "Interest expense and similar charges", {
        "FY2025": -21177326, "FY2024": -19083832, "FY2023": -12823804, "FY2022": -4638083, "FY2021": -2641590, "FY2020": -5218595, "FY2019": -7178683}),
    ("TOTAL", "Net interest income", {
        "FY2025": 37005387, "FY2024": 36370829, "FY2023": 31306673, "FY2022": 19324504, "FY2021": 10096454, "FY2020": 9080523, "FY2019": 15275677}),
    ("DATA", "Fees and commission income", {
        "FY2025": 10547351, "FY2024": 8240062, "FY2023": 6490818, "FY2022": 5475061, "FY2021": 4495862, "FY2020": 4007440, "FY2019": 3639850}),
    ("DATA", "Net foreign currency income", {
        "FY2025": 2111389, "FY2024": 1944169, "FY2023": 1989283, "FY2022": 2218117, "FY2021": 1446706, "FY2020": 3010751, "FY2019": 2561547}),
    ("DATA", "Investments gains/(losses) from sale of government and other securities", {
        "FY2025": 912197, "FY2024": -163241, "FY2023": 79998, "FY2022": 0, "FY2021": 228305, "FY2020": 1356116, "FY2019": 653640}),
    ("DATA", "Other income", {
        "FY2025": 5164, "FY2024": 1012475, "FY2023": 89352, "FY2022": 4404, "FY2021": 9652, "FY2020": 92382, "FY2019": 87069}),
    ("TOTAL", "Total non-interest income", {
        "FY2025": 13576101, "FY2024": 11033465, "FY2023": 8649451, "FY2022": 7697582, "FY2021": 6180525, "FY2020": 8466689, "FY2019": 6942106}),
    ("TOTAL", "Operating income", {
        "FY2025": 50581488, "FY2024": 47404294, "FY2023": 39956124, "FY2022": 27022086, "FY2021": 16276979, "FY2020": 17547212, "FY2019": 22217783}),
    ("DATA", "Staff costs", {
        "FY2025": -28184476, "FY2024": -26959541, "FY2023": -23423228, "FY2022": -18937087, "FY2021": -16723434, "FY2020": -14149127, "FY2019": -12133494}),
    ("DATA", "Other administrative expenses", {
        "FY2025": -12134745, "FY2024": -11815526, "FY2023": -11021926, "FY2022": -14536226, "FY2021": -9674690, "FY2020": -7465181, "FY2019": -8347885}),
    ("DATA", "Depreciation and amortisation", {
        "FY2025": -3318426, "FY2024": -2383646, "FY2023": -2277366, "FY2022": -1682232, "FY2021": -1258265, "FY2020": -1300282, "FY2019": -1253581}),
    ("TOTAL", "Total operating expenses", {
        "FY2025": -43637647, "FY2024": -41158713, "FY2023": -36722520, "FY2022": -35155545, "FY2021": -27656389, "FY2020": -22914590, "FY2019": -21734960}),
    ("DATA", "Reversal of provisions/(provisions) for credit losses", {
        "FY2025": 82778, "FY2024": -408819, "FY2023": 1024498, "FY2022": -1986487, "FY2021": -1090971, "FY2020": -966406, "FY2019": 320650}),
    ("TOTAL", "Profit/(Loss) before taxation", {
        "FY2025": 7026619, "FY2024": 5836762, "FY2023": 4258102, "FY2022": -10119946, "FY2021": -12470381, "FY2020": -6333784, "FY2019": 803473}),
    ("DATA", "Taxation", {
        "FY2025": -1623905, "FY2024": -1599961, "FY2023": -1145807, "FY2022": 1076968, "FY2021": 3427257, "FY2020": 1181057, "FY2019": -164122}),
    ("TOTAL", "Profit/(Loss) for the year", {
        "FY2025": 5402714, "FY2024": 4236801, "FY2023": 3112295, "FY2022": -9042978, "FY2021": -9043124, "FY2020": -5152727, "FY2019": 639351}),
    ("SECTION", "Other comprehensive income - that may be reclassified to profit or loss", {}),
    ("DATA", "Fair value movements on FVOCI financial instruments", {
        "FY2025": 2262367, "FY2024": 3365255, "FY2023": 1821050, "FY2022": -4168194, "FY2021": -2965070, "FY2020": 27112, "FY2019": 1476640}),
    ("DATA", "Taxation on FVOCI financial instruments", {
        "FY2025": -565592, "FY2024": -841314, "FY2023": -454165, "FY2022": 1042050, "FY2021": 267533, "FY2020": 59262, "FY2019": -61839}),
    ("TOTAL", "Total other comprehensive income/(loss)", {
        "FY2025": 1696775, "FY2024": 2523941, "FY2023": 1366885, "FY2022": -3126144, "FY2021": -2697537, "FY2020": 276374, "FY2019": 1727668}),
    ("TOTAL", "Total comprehensive income/(loss) for the year attributable to equity holders", {
        "FY2025": 7099489, "FY2024": 6760742, "FY2023": 4479180, "FY2022": -12169122, "FY2021": -11740661, "FY2020": -4876353, "FY2019": 2367019}),
]

bw.add_income_statement_sheet(
    title="Ghana International Bank Plc — Statement of Comprehensive Income",
    subtitle="Company basis (GHIB has no subsidiaries or branches), £. See source note at bottom.",
    rows=pl_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=80,
    source_height=340,
    unit_suffix=" (£)",
)

# ---------------------------------------------------------------
# Sheet: Statement of Changes in Equity - chronological, oldest to newest.
# Built via the per-year reconciliation ladder against the Balance Sheet
# above: every year's closing balance ties exactly to both the next
# year's own opening balance and that year's Balance Sheet Total Equity -
# zero plug rows needed anywhere.
# ---------------------------------------------------------------
EQUITY_HEADERS = ["Ordinary shares", "Share Premium", "Profit and Loss", "FVOCI Reserves", "Total"]

equity_changes_rows = [
    ("TOTAL", "At 31 December 2018", (45000000, 30000000, 62474059, -727200, 136746859)),
    ("DATA", "Profit for the year (FY2019)", (None, None, 639351, None, 639351)),
    ("DATA", "Other comprehensive income (FY2019)", (None, None, None, 1727668, 1727668)),
    ("TOTAL", "Total comprehensive income for the year (FY2019)", (None, None, 639351, 1727668, 2367019)),
    ("DATA", "Dividend paid (FY2019)", (None, None, -2111787, None, -2111787)),
    ("TOTAL", "At 31 December 2019", (45000000, 30000000, 61001623, 1000468, 137002091)),
    ("DATA", "Loss for the year (FY2020)", (None, None, -5152727, None, -5152727)),
    ("DATA", "Fair value gains on FVOCI financial instruments net of tax (FY2020)", (None, None, None, 276374, 276374)),
    ("TOTAL", "Total comprehensive loss for the year (FY2020)", (None, None, -5152727, 276374, -4876353)),
    ("DATA", "Dividend paid (FY2020)", (None, None, -319676, None, -319676)),
    ("TOTAL", "At 31 December 2020", (45000000, 30000000, 55529220, 1276842, 131806062)),
    ("DATA", "Loss for the year (FY2021)", (None, None, -9043124, None, -9043124)),
    ("DATA", "Fair value losses on FVOCI financial instruments net of tax (FY2021)", (None, None, None, -2469232, -2469232)),
    ("DATA", "Gains on FVOCI financial instruments transferred to Income statement (FY2021)", (None, None, None, -228305, -228305)),
    ("TOTAL", "Total comprehensive loss for the year (FY2021)", (None, None, -9043124, -2697537, -11740661)),
    ("TOTAL", "At 31 December 2021", (45000000, 30000000, 46486096, -1420695, 120065401)),

    ("DATA", "Loss for the year (FY2022)", (None, None, -9042978, None, -9042978)),
    ("DATA", "Fair value losses on FVOCI financial instruments net of tax (FY2022)", (None, None, None, -3126144, -3126144)),
    ("TOTAL", "Total comprehensive loss for the year (FY2022)", (None, None, -9042978, -3126144, -12169122)),
    ("DATA", "Issue of share capital (FY2022)", (18739927, 31212787, None, None, 49952714)),
    ("TOTAL", "At 31 December 2022", (63739927, 61212787, 37443118, -4546839, 157848993)),

    ("DATA", "Profit for the year (FY2023)", (None, None, 3112295, None, 3112295)),
    ("DATA", "Fair value movements on FVOCI financial instruments net of tax (FY2023)", (None, None, None, 1446883, 1446883)),
    ("DATA", "Gains on FVOCI financial instruments transferred to Income statement (FY2023)", (None, None, None, -79998, -79998)),
    ("TOTAL", "Total comprehensive income for the year (FY2023)", (None, None, 3112295, 1366885, 4479180)),
    ("TOTAL", "At 31 December 2023", (63739927, 61212787, 40555413, -3179954, 162328173)),

    ("DATA", "Profit for the year (FY2024)", (None, None, 4236801, None, 4236801)),
    ("DATA", "Fair value movements on FVOCI financial instruments net of tax (FY2024)", (None, None, None, 2360700, 2360700)),
    ("DATA", "Losses on FVOCI financial instruments transferred to Income statement (FY2024)", (None, None, None, 163241, 163241)),
    ("TOTAL", "Total comprehensive income for the year (FY2024)", (None, None, 4236801, 2523941, 6760742)),
    ("DATA", "Dividend paid (FY2024)", (None, None, -622459, None, -622459)),
    ("TOTAL", "At 31 December 2024", (63739927, 61212787, 44169755, -656013, 168466456)),

    ("DATA", "Profit for the year (FY2025)", (None, None, 5402714, None, 5402714)),
    ("DATA", "Fair value movements on FVOCI financial instruments net of tax (FY2025)", (None, None, None, 2608972, 2608972)),
    ("DATA", "Gains on FVOCI financial instruments transferred to Income statement (FY2025)", (None, None, None, -912197, -912197)),
    ("TOTAL", "Total comprehensive income for the year (FY2025)", (None, None, 5402714, 1696775, 7099489)),
    ("DATA", "Dividend paid (FY2025)", (None, None, -847741, None, -847741)),
    ("TOTAL", "At 31 December 2025", (63739927, 61212787, 48724728, 1040762, 174718204)),
]

EQUITY_SOURCES = (
    STATEMENTS_SOURCES + "\n\n"
    "No dividends paid FY2021/FY2022/FY2023 (each year's own report shows a dash). Dividend paid reduces "
    "the Profit and Loss column directly (verified arithmetically - the source page's own 'Dividend paid' "
    "row shows a dash under the Profit and Loss column but a non-zero amount only in the Total column; the "
    "closing Profit and Loss balance only ties if the dividend is treated as reducing that column too)."
)

bw.add_equity_changes_sheet(
    title="Ghana International Bank Plc — Statement of Changes in Equity",
    subtitle="£, chronological - oldest to newest. See source note for details.",
    headers=EQUITY_HEADERS,
    rows=equity_changes_rows,
    sources_text=EQUITY_SOURCES,
    first_col_width=68,
    source_height=280,
)

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Cash flows from operating activities", {}),
    ("DATA", "Profit/(loss) before taxation", {
        "FY2025": 7026619, "FY2024": 5836762, "FY2023": 4258102, "FY2022": -10119946, "FY2021": -12470381, "FY2020": -6333784, "FY2019": 803473}),
    ("DATA", "Foreign currency income - Translation of assets & liabilities", {
        "FY2025": -856667, "FY2024": -748521, "FY2023": -525892, "FY2022": -661420, "FY2021": -297613, "FY2020": -445485, "FY2019": -515013}),
    ("DATA", "Depreciation and amortisation", {
        "FY2025": 3318426, "FY2024": 2383646, "FY2023": 2277366, "FY2022": 1682232, "FY2021": 1258265, "FY2020": 1300282, "FY2019": 1253581}),
    ("DATA", "Lease finance charge", {
        "FY2025": 168908, "FY2024": 165240, "FY2023": 140727, "FY2022": 159254, "FY2021": 168528, "FY2020": 176507, "FY2019": 191087}),
    ("DATA", "(Reversal of provisions)/provisions for credit losses", {
        "FY2025": -82778, "FY2024": 408819, "FY2023": -1024498, "FY2022": 1986487, "FY2021": 1090971, "FY2020": 966406, "FY2019": -320650}),
    ("DATA", "Gain on disposal of fixed asset", {"FY2025": -5164, "FY2022": -4404, "FY2021": -7648}),
    ("DATA", "Net interest income and other non-cash items", {
        "FY2025": -5354639, "FY2024": 6709610, "FY2023": -790883}),
    ("DATA", "Decrease/(increase) in loans and advances to banks and customers", {
        "FY2025": -102290341, "FY2024": -79379510, "FY2023": -8318223, "FY2022": 37516914, "FY2021": -40250490, "FY2020": 62262668, "FY2019": -11745843}),
    ("DATA", "Decrease/(increase) in government and other securities", {
        "FY2025": -56902275, "FY2024": -246603941, "FY2023": 52729216, "FY2022": -82184444, "FY2021": -23355251, "FY2020": -18705895, "FY2019": -3068231}),
    ("DATA", "Decrease/(increase) in prepayments and other receivables", {
        "FY2025": 1097161, "FY2024": -2393680, "FY2023": -488671, "FY2022": 43806, "FY2021": -919472, "FY2020": -61623, "FY2019": -825241}),
    ("DATA", "Increase/(decrease) in deposits by banks and customers", {
        "FY2025": 91632232, "FY2024": 247285853, "FY2023": -90180843, "FY2022": 79813107, "FY2021": 43175607, "FY2020": 75807373, "FY2019": -29253211}),
    ("DATA", "Increase/(decrease) in other liabilities", {
        "FY2025": -40316, "FY2024": 382531, "FY2023": -323153, "FY2022": 866972, "FY2021": 252000, "FY2020": -291778, "FY2019": 2564032}),
    ("DATA", "Increase/(decrease) in accruals and deferred income", {
        "FY2025": 1430553, "FY2024": 1574625, "FY2023": 1816917, "FY2022": 955575, "FY2021": -647350, "FY2020": 197755, "FY2019": 830724}),
    ("DATA", "Income taxes refunded", {"FY2025": 0, "FY2024": 945584}),
    ("DATA", "Foreign income taxes paid", {"FY2025": -198914, "FY2024": -38468, "FY2019": -694064}),
    ("TOTAL", "Net cash generated from/(used in) operating activities", {
        "FY2025": -61057195, "FY2024": -63471450, "FY2023": -40429835, "FY2022": 30054133, "FY2021": -32002834, "FY2020": 114829689, "FY2019": -40779356}),
    ("SECTION", "Cash flows from investing activities", {}),
    ("DATA", "Purchase of property, plant and equipment", {
        "FY2025": -578036, "FY2024": -478827, "FY2023": -303289, "FY2022": -786227, "FY2021": -800543, "FY2020": -1729692, "FY2019": -277456}),
    ("DATA", "Purchase of intangible assets", {
        "FY2025": -1992939, "FY2024": -2751634, "FY2023": -1914732, "FY2022": -3455929, "FY2021": -1585110, "FY2020": -237660, "FY2019": -609948}),
    ("DATA", "Proceeds from sale of fixed asset", {"FY2025": 5164, "FY2022": 4404, "FY2021": 7648}),
    ("TOTAL", "Net cash used in investing activities", {
        "FY2025": -2565811, "FY2024": -3230461, "FY2023": -2218021, "FY2022": -4237752, "FY2021": -2378005, "FY2020": -1967352, "FY2019": -887404}),
    ("SECTION", "Cash flows from financing activities", {}),
    ("DATA", "Dividends paid", {"FY2025": -847741, "FY2024": -622459, "FY2020": -319676, "FY2019": -2111787}),
    ("DATA", "Net increase in term financing", {"FY2025": 19945689, "FY2024": 14377227}),
    ("DATA", "Proceeds from an equity share issue (net of issuance cost)", {"FY2022": 49952714}),
    ("DATA", "Repayment of lease liabilities", {
        "FY2025": -848145, "FY2024": -1157028, "FY2023": -874791, "FY2022": -915051, "FY2021": -849159, "FY2020": -501218, "FY2019": -133396}),
    ("TOTAL", "Net cash generated from/(used in) financing activities", {
        "FY2025": 18249803, "FY2024": 12597740, "FY2023": -874791, "FY2022": 49037663, "FY2021": -849159, "FY2020": -820894, "FY2019": -2245183}),
    ("TOTAL", "(Decrease)/increase in cash and cash equivalents", {
        "FY2025": -45373203, "FY2024": -54104171, "FY2023": -43522647, "FY2022": 74854044, "FY2021": -35229998, "FY2020": 112041443, "FY2019": -43756973}),
    ("DATA", "Effect of exchange rate changes on cash and cash equivalents", {
        "FY2025": 89985, "FY2024": 108502, "FY2023": 112750, "FY2022": 162049, "FY2021": 71416, "FY2020": 112708, "FY2019": 76737}),
    ("TOTAL", "Net (decrease)/increase in cash and cash equivalents", {
        "FY2025": -45283218, "FY2024": -53995669, "FY2023": -43409897, "FY2022": 75016093, "FY2021": -35158582, "FY2020": 112154151, "FY2019": -43680236}),
    ("DATA", "Cash and cash equivalents at the beginning of the year", {
        "FY2025": 376370085, "FY2024": 430365754, "FY2023": 473775651, "FY2022": 398759558, "FY2021": 433918140, "FY2020": 321763989, "FY2019": 365444225}),
    ("TOTAL", "Cash and cash equivalents at the end of the year", {
        "FY2025": 331086867, "FY2024": 376370085, "FY2023": 430365754, "FY2022": 473775651, "FY2021": 398759558, "FY2020": 433918140, "FY2019": 321763989}),
]

bw.add_cash_flow_sheet(
    title="Ghana International Bank Plc — Statement of Cash Flow",
    subtitle="Company basis (GHIB has no subsidiaries or branches), £. See source note at bottom.",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=85,
    source_height=210,
    unit_suffix=" (£)",
)

# ---------------------------------------------------------------
# Sheet: Asset Quality / Credit Risk Disclosures - aggregate "Total
# provision for credit losses" table (placements/loans to banks + loans
# to customers + government/other securities combined), £'000 as
# disclosed. FY2021 lacks a Gross Exposure by stage breakdown (only ECL
# by stage was disclosed that early) - left blank per project convention.
# ---------------------------------------------------------------
AQ_GROSS = {
    "Stage 1": {"FY2025": 973433, "FY2024": 849658, "FY2023": 467106, "FY2022": 494742},
    "Stage 2": {"FY2025": 178375, "FY2024": 289258, "FY2023": 191935, "FY2022": 200525},
    "Stage 3": {"FY2025": 1004, "FY2024": 2784, "FY2023": 4993, "FY2022": 2451},
    "Total": {"FY2025": 1152812, "FY2024": 1141700, "FY2023": 664034, "FY2022": 697718},
}
AQ_ECL = {
    "Stage 1": {"FY2025": 686, "FY2024": 416, "FY2023": 472, "FY2022": 856, "FY2021": 1214, "FY2020": 637263, "FY2019": 489522},
    "Stage 2": {"FY2025": 347, "FY2024": 788, "FY2023": 1238, "FY2022": 2259, "FY2021": 1336, "FY2020": 825947, "FY2019": 40947},
    "Stage 3": {"FY2025": 30, "FY2024": 668, "FY2023": 1945, "FY2022": 1773, "FY2021": 0, "FY2020": 0},
    "Total": {"FY2025": 1063, "FY2024": 1872, "FY2023": 3655, "FY2022": 4888, "FY2021": 2551, "FY2020": 1463210},
}
AQ_NET = {
    stage: {y: AQ_GROSS[stage][y] - AQ_ECL[stage][y] for y in AQ_GROSS[stage]}
    for stage in ("Stage 1", "Stage 2", "Stage 3", "Total")
}
AQ_NPL_RATIO = {y: f"{AQ_GROSS['Stage 3'][y] / AQ_GROSS['Total'][y] * 100:.2f}%" for y in AQ_GROSS["Total"]}
AQ_STAGE3_COVERAGE = {y: f"{AQ_ECL['Stage 3'][y] / AQ_GROSS['Stage 3'][y] * 100:.2f}%" for y in AQ_GROSS["Total"]}
AQ_TOTAL_COVERAGE = {y: f"{AQ_ECL['Total'][y] / AQ_GROSS['Total'][y] * 100:.2f}%" for y in AQ_GROSS["Total"]}

aq_rows = [
    ("SECTION", "Gross exposure by IFRS 9 stage", {}),
    ("DATA", "Stage 1 (12-month ECL)", AQ_GROSS["Stage 1"]),
    ("DATA", "Stage 2 (lifetime ECL, not credit-impaired)", AQ_GROSS["Stage 2"]),
    ("DATA", "Stage 3 (credit-impaired)", AQ_GROSS["Stage 3"]),
    ("TOTAL", "Total gross exposure", AQ_GROSS["Total"]),
    ("SECTION", "ECL allowance by stage", {}),
    ("DATA", "Stage 1 ECL", AQ_ECL["Stage 1"]),
    ("DATA", "Stage 2 ECL", AQ_ECL["Stage 2"]),
    ("DATA", "Stage 3 ECL", AQ_ECL["Stage 3"]),
    ("TOTAL", "Total ECL allowance", AQ_ECL["Total"]),
    ("SECTION", "Net carrying amount by stage (calculated - see source note)", {}),
    ("DATA", "Stage 1", AQ_NET["Stage 1"]),
    ("DATA", "Stage 2", AQ_NET["Stage 2"]),
    ("DATA", "Stage 3", AQ_NET["Stage 3"]),
    ("TOTAL", "Total net carrying amount", AQ_NET["Total"]),
    ("SECTION", "Derived ratios", {}),
    ("DATA", "NPL ratio (Stage 3 gross / Total gross)", AQ_NPL_RATIO),
    ("DATA", "Stage 3 coverage ratio (Stage 3 ECL / Stage 3 gross)", AQ_STAGE3_COVERAGE),
    ("DATA", "Total ECL coverage ratio (Total ECL / Total gross)", AQ_TOTAL_COVERAGE),
]

bw.add_asset_quality_sheet(
    title="Ghana International Bank Plc — Asset Quality / Credit Risk Disclosures",
    subtitle="£'000 (as disclosed - see source note; rest of workbook is in £). Aggregate across all credit "
             "exposure classes (placements/loans to banks, loans to customers, government and other securities).",
    rows=aq_rows,
    sources_text=ASSET_QUALITY_SOURCES,
    first_col_width=68,
    source_height=310,
    unit_suffix="",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, note=None, page="4-5"):
    bw.add_metric_sheet(name, unit, rows_data, p3_sources(page), note=note, first_col_width=48, source_height=170)


# FY2025 values came from the Annual Report until 2026-09-18 and now come from
# the FY2025 Pillar 3, published that day - see FY2025_SOURCE_NOTE for the full
# before/after and for the two internal inconsistencies in that edition.
# FY2025 UPGRADED 2026-09-18 from the Annual Report's rounded "£161.7m" to the
# 161,750 printed in row 1 of the FY2025 Pillar 3's own KM1 - same figure, now to
# £'000 rather than £0.1m, and from the source every other year on this sheet uses.
CET1_CAPITAL = {"FY2025": 161750, "FY2024": 156657, "FY2023": 153053, "FY2022": 152019, "FY2021": 120301,
                "FY2020": 131539, "FY2019": 137828}
TOTAL_RWA = {"FY2025": 751519, "FY2024": 700374, "FY2023": 493080, "FY2022": 537708, "FY2021": 450231,
             "FY2020": 372287, "FY2019": 329256}
# FY2019 CORRECTED 2026-09-16 from 329,260 to 329,256. The old figure was rounded off
# the FY2020 edition's narrative ("£329.26m"); 329,256 is printed directly as row 4 of
# the KM1 key-metrics table in GHIB's FY2022 and FY2023 Pillar 3 editions. Same figure
# to the stated precision, now transcribed rather than derived - see the KM1 sheet.
# FY2019's own Table 1 prints a "Total Risk-Weighted Assets" of 281,553, which is
# demonstrably the CREDIT-RISK SUBTOTAL rather than total RWAs - see TOTAL_RWA_NOTE.
# Kept on its own labelled row rather than discarded or silently substituted.
TOTAL_RWA_AS_PRINTED_FY2019 = {"FY2019": 281553}
# FY2025 ratios UPGRADED 2026-09-18 from the Annual Report's rounded statements
# ("21.5%", "213%") to the FY2025 Pillar 3's own figures, per the standing rule
# that each year comes from its own edition and this workbook's convention that a
# ratio takes the most precise figure that edition prints.
CET1_RATIO = {"FY2025": "21.52%", "FY2024": "22.37%", "FY2023": "31.04%", "FY2022": "28.27%", "FY2021": "26.72%",
              "FY2020": "35.33%", "FY2019": "41.86%"}
LEVERAGE_RATIO = {"FY2025": "14.17%", "FY2024": "14.66%", "FY2023": "25.88%", "FY2022": "23.86%", "FY2021": "15.20%",
                  "FY2020": "17.14%", "FY2019": "20.06%"}
LCR = {"FY2025": "213.49%", "FY2024": "256.31%", "FY2023": "370.09%", "FY2022": "409.87%", "FY2021": "378.34%",
       "FY2020": "310.06%", "FY2019": "278.41%"}
NSFR = {"FY2025": "181.39%", "FY2024": "255.98%", "FY2023": "273.27%", "FY2022": "292.79%", "FY2021": "195%",
        "FY2020": "198%",
        "FY2019": "Not disclosed (no NSFR row in the FY2019 Pillar 3's Table 1)"}

TOTAL_RWA_NOTE = (
    "FY2019 AND FY2020 FILLED 2026-09-15 from the newly-located FY2019/FY2020 Pillar 3 editions. "
    "FLAGGED - FY2019 IS NOT A STRAIGHT TRANSCRIPTION AND MUST BE READ WITH THIS NOTE. The FY2019 "
    "Pillar 3's own Table 1 prints 'Total Risk-Weighted Assets (£'000) 281,553'. That figure is "
    "demonstrably the CREDIT-RISK SUBTOTAL, not total RWAs, and the document disproves itself three "
    "ways: (1) the same Table 1 prints a CET1 ratio of 41.86% against CET1 capital of 137,828, and "
    "137,828/281,553 is 48.95%, not 41.86%; (2) the FY2019 Table 2 'Breakdown of the Bank's "
    "Regulatory Capital Requirement' shows 281,553 as the TOTAL of the credit-risk exposure-class "
    "rows only, with operational risk (capital requirement 3,731) and market risk (85) listed "
    "separately below it and excluded from that total; (3) the FY2020 edition's own narrative "
    "states GHIB 'experienced an increase of 13% in risk weighted assets (£329.26m in 2019 to "
    "£372.29m in 2020)'. The 329,260 carried here is that FY2020-edition figure, transcribed - it "
    "is NOT back-solved from the ratio, and this project's rule against deriving RWA from capital "
    "divided by a ratio has not been broken. It is stated only to £0.01m, so it carries about £5k "
    "of rounding; the RWA Breakdown sheet's own component sum for FY2019 comes to 329,254, "
    "corroborating it. The figure as printed in FY2019's Table 1 is preserved on its own labelled "
    "row so nothing is hidden. This is the same defect already corrected for Redwood, whose KM1 "
    "row 4 likewise carried the credit-risk subtotal. FY2020 has no such problem: its Table 1 "
    "total of 372,287 reconciles with its own Table 2 components (325,809 credit + 45,813 "
    "operational + 675 market = 372,297, within rounding)."
)

FY2025_AR_BASIS_NOTE = (
    "FY2025 IS NOW PILLAR 3-SOURCED. It was Annual Report-sourced until 18 September 2026, when GHIB "
    "published its FY2025 Pillar 3 Disclosures; the Pillar 3 figure is the same value at higher "
    "precision, never a different one. See the source note below for the full before/after."
)

CET1_CAP_NOTE = FY2025_AR_BASIS_NOTE + " FY2025 now carries the Pillar 3's 161,750; the Annual Report stated the same figure only to £0.1m (\"£161.7m\")."
NO_AT1_FY2025_NOTE = NO_AT1_NOTE + " " + FY2025_AR_BASIS_NOTE

# ---------------------------------------------------------------
# KM1 Key Metrics - GHIB's own published template, reproduced as printed.
#
# HOW THIS TABLE WAS FOUND, AND WHY A TEXT SEARCH SAID IT DID NOT EXIST.
# In EVERY GHIB Pillar 3 edition the key-metrics table is a PASTED IMAGE, not
# live text. The PDFs are otherwise fully text-extractable, so `pdftotext`
# returns the caption ("Table1: Key Metrics ratios as at 31 December 2024")
# followed by white space where the table should be, and any token- or
# label-based detector reports NO KM1 for this bank in all six years. The
# table is plainly there on the rendered page. Every figure below was read
# VISUALLY - not OCR'd - which is the same method this script already uses for
# the FY2019 Table 2, and read TWICE from two independent renderings: the whole
# page rasterised at 200 dpi, and the embedded bitmap extracted at its native
# resolution with pdfimages. The two reads agree digit for digit.
#
# WHICH EDITION EACH COLUMN COMES FROM. GHIB did not adopt the KM1 template
# until its FY2022 edition. The FY2022, FY2023 and FY2024 editions each print
# the full five-column template (T to T-4):
#   FY2024 edition -> 2024 2023 2022 2021 2020
#   FY2023 edition -> 2023 2022 2021 2020 2019
#   FY2022 edition -> 2022 2021 2020 2019 2018
# So FY2024, FY2023 and FY2022 each come from the edition in which that year
# is the reporting year, per the project's standing rule. FY2021, FY2020 and
# FY2019 have NO own-edition KM1 at all - their own editions (and the FY2019
# one) print a bespoke single-column "Key Metrics" list with no row numbers,
# no SREP/buffer rows and no UK 16a/16b split, which is not the template - so
# those three columns are taken from the FY2022 edition, the EARLIEST edition
# that prints them inside the template. Same treatment as Allica's FY2021.
#
# FY2025 is blank: no FY2025 Pillar 3 exists yet (checked against the Bank's
# own WordPress media index 16 September 2026 - see KM1_SOURCES). The FY2025
# figures on the metric sheets are Annual Report-sourced and are deliberately
# NOT reassembled into a KM1 shape here.
#
# ROWS GHIB DOES NOT PRINT. UK 7b, UK 7c, UK 8a, UK 9a, 10, UK 10a and the
# 14a-14e leverage block appear in no GHIB edition and are not shown: this is
# the bank's own row set, not a gap in transcription.
# ---------------------------------------------------------------
km1_rows = [
    ("SECTION", "Available own funds (amounts) — £'000", {}),
    ("DATA", "1    Common Equity Tier 1 (CET1) capital",
     {"FY2025": 161750, "FY2024": 156657, "FY2023": 153053, "FY2022": 152019, "FY2021": 120301, "FY2020": 131539,
      "FY2019": 137827.8}),
    ("DATA", "2    Tier 1 capital",
     {"FY2025": 161750, "FY2024": 156657, "FY2023": 153053, "FY2022": 152019, "FY2021": 120301, "FY2020": 131539,
      "FY2019": 137827.8}),
    ("DATA", "3    Total capital",
     {"FY2025": 161750, "FY2024": 156657, "FY2023": 153053, "FY2022": 152019, "FY2021": 120301, "FY2020": 131539,
      "FY2019": 137827.8}),
    ("SECTION", "Risk-weighted exposure amounts — £'000", {}),
    ("DATA", "4    Total risk-weighted exposure amount",
     {"FY2025": 751519, "FY2024": 700374, "FY2023": 493080, "FY2022": 537708, "FY2021": 450231, "FY2020": 372287,
      "FY2019": 329256}),
    ("SECTION", "Capital ratios  (as a percentage of risk-weighted exposure amount)", {}),
    ("DATA", "5    Common Equity Tier 1 ratio (%)",
     {"FY2025": "21.52%", "FY2024": "22.37%", "FY2023": "31.04%", "FY2022": "28.27%", "FY2021": "26.72%", "FY2020": "35.33%",
      "FY2019": "41.86%"}),
    ("DATA", "6    Tier 1 ratio (%)",
     {"FY2025": "21.52%", "FY2024": "22.37%", "FY2023": "31.04%", "FY2022": "28.27%", "FY2021": "26.72%", "FY2020": "35.33%",
      "FY2019": "41.86%"}),
    ("DATA", "7    Total capital ratio (%)",
     {"FY2025": "21.52%", "FY2024": "22.37%", "FY2023": "31.04%", "FY2022": "28.27%", "FY2021": "26.72%", "FY2020": "35.33%",
      "FY2019": "41.86%"}),
    ("SECTION", "Additional own funds requirements based on SREP (as a percentage of risk-weighted "
                "exposure amount) pillar 2A", {}),
    ("DATA", "UK 7a    Additional CET1 SREP requirements (%)",
     {"FY2025": "5.85%", "FY2024": "5.85%", "FY2023": "5.85%", "FY2022": "7.37%", "FY2021": "7.37%", "FY2020": "7.37%",
      "FY2019": "5.80%"}),
    ("DATA", "UK 7d    Total SREP own funds requirements (%)",
     {"FY2025": "13.85%", "FY2024": "13.85%", "FY2023": "13.85%", "FY2022": "15.37%", "FY2021": "15.37%", "FY2020": "15.37%",
      "FY2019": "13.80%"}),
    ("SECTION", "Combined buffer requirement (as a percentage of risk-weighted exposure amount)", {}),
    ("DATA", "8    Capital conservation buffer (%)",
     {"FY2025": "2.50%", "FY2024": "2.50%", "FY2023": "2.50%", "FY2022": "2.50%", "FY2021": "2.50%", "FY2020": "2.50%",
      "FY2019": "2.50%"}),
    ("DATA", "9    Institution specific countercyclical capital buffer (%)",
     {"FY2025": "0.26%", "FY2024": "0.32%", "FY2023": "0.17%", "FY2022": "0.05%", "FY2021": "0.00%", "FY2020": "0.00%",
      "FY2019": "0.01%"}),
    ("DATA", "11    Combined buffer requirement (%)",
     {"FY2025": "2.76%", "FY2024": "2.82%", "FY2023": "2.67%", "FY2022": "2.55%", "FY2021": "2.50%", "FY2020": "2.50%",
      "FY2019": "2.51%"}),
    ("DATA", "UK 11a    Overall capital requirements (%)",
     {"FY2025": "16.61%", "FY2024": "16.67%", "FY2023": "16.52%", "FY2022": "17.92%", "FY2021": "17.87%", "FY2020": "17.87%",
      "FY2019": "16.31%"}),
    ("DATA", "12    CET1 available after meeting the total SREP own funds requirements (%)",
     {"FY2025": "7.67%", "FY2024": "8.52%", "FY2023": "17.19%", "FY2022": "12.90%", "FY2021": "11.35%", "FY2020": "19.96%",
      "FY2019": "28.06%"}),
    ("SECTION", "Leverage ratio — £'000 / %", {}),
    ("DATA", "13    Total exposure measure excluding claims on central banks",
     {"FY2025": 1141156, "FY2024": 1071784, "FY2023": 591309, "FY2022": 637251, "FY2021": 791289, "FY2020": 767198,
      "FY2019": 686553}),
    ("DATA", "14    Leverage ratio excluding claims on central banks (%)",
     {"FY2025": "14.17%", "FY2024": "14.66%", "FY2023": "25.88%", "FY2022": "23.86%", "FY2021": "15.18%", "FY2020": "17.10%",
      "FY2019": "19.99%"}),
    ("SECTION", "Liquidity Coverage Ratio — £'000 / %", {}),
    ("DATA", "15    Total high-quality liquid assets (HQLA) (Weighted value -average)",
     {"FY2025": 447862, "FY2024": 428070, "FY2023": 263896, "FY2022": 306067, "FY2021": 236427, "FY2020": 199128,
      "FY2019": 206996}),
    ("DATA", "UK 16a    Cash outflows - Total weighted value",
     {"FY2025": 451692, "FY2024": 466537, "FY2023": 285221, "FY2022": 298700, "FY2021": 249962, "FY2020": 256894,
      "FY2019": 221049}),
    ("DATA", "UK 16b    Cash inflows - Total weighted value",
     {"FY2025": 241912, "FY2024": 299522, "FY2023": 275604, "FY2022": 345041, "FY2021": 249320, "FY2020": 248271,
      "FY2019": 146701}),
    ("DATA", "16    Total net cash outflows (adjusted value)",
     {"FY2025": 209779, "FY2024": 167015, "FY2023": 71305, "FY2022": 74675, "FY2021": 62491, "FY2020": 64224,
      "FY2019": 74348}),
    ("DATA", "17    Liquidity coverage ratio (%)",
     {"FY2025": "213.4%", "FY2024": "256.31%", "FY2023": "370.09%", "FY2022": "409.87%", "FY2021": "378.34%",
      "FY2020": "310.06%", "FY2019": "278.41%"}),
    ("SECTION", "Net Stable Funding Ratio* — £'000 / %", {}),
    ("DATA", "18    Total available stable funding",
     {"FY2025": 483227, "FY2024": 391313, "FY2023": 317974, "FY2022": 370817}),
    ("DATA", "19    Total required stable funding",
     {"FY2025": 266394, "FY2024": 152868, "FY2023": 116361, "FY2022": 126647}),
    ("DATA", "20    NSFR ratio (%)",
     {"FY2025": "181.4%", "FY2024": "255.98%", "FY2023": "273.27%", "FY2022": "292.79%"}),
    ("DATA", "* Comparable figures for other periods are not available because the new NSFR rules from "
             "CRR2 only commenced in 2022 (GHIB's own footnote to the table)", {}),
]

KM1_SOURCES = (
    "Sources - Ghana International Bank Plc's own key-metrics (UK KM1) template, £'000 and percentages as "
    "printed, entity basis (GHIB plc is a single entity with no consolidated group):\n"
    f"FY2025: Pillar 3 Disclosures 31 December 2025, p.14 printed (PDF p.13), \"Table1: Key Metrics "
    f"ratios as at 31 December 2025\" - {P3_2025_URL}\n"
    f"FY2024: Pillar 3 Disclosures 31 December 2024, p.5, \"Table1: Key Metrics ratios as at 31 December "
    f"2024\" - {P3_2024_URL}\n"
    f"FY2023: Pillar 3 Disclosures 31 December 2023, p.5, \"Table1: Key Metrics ratios as at 31 December "
    f"2023\" - {P3_2023_URL}\n"
    f"FY2022: Pillar 3 Disclosures 31 December 2022, p.4, \"Table1: Key Metrics ratios as at 31 December "
    f"2022\" - {P3_2022_URL}\n"
    f"FY2021, FY2020 and FY2019: the comparative columns of that same FY2022 edition (see the note on "
    f"edition choice below) - {P3_2022_URL}\n"
    "\n"
    "THE TABLE IS AN IMAGE IN EVERY EDITION UP TO FY2024 - A SOURCE DEFECT, RECORDED NOT HIDDEN (the FY2025 "
    "edition finally breaks the pattern; see below). In all six of those GHIB Pillar 3 "
    "PDFs the key-metrics table is a pasted picture, not live text, even though the surrounding document "
    "extracts perfectly (pdfimages confirms one embedded bitmap on each of those pages: 940x665 px in the "
    "FY2024 edition, 915x668 in FY2023, 597x630 in FY2022). A text search of these PDFs returns the caption "
    "and then nothing, so any automated KM1 detector reports that GHIB publishes no KM1 - which is false.\n"
    "HOW IT WAS READ, AND HOW THAT READING WAS CHECKED. Every figure above was read VISUALLY, never OCR'd, "
    "and read TWICE from two INDEPENDENT renderings: (a) the whole page rasterised from the PDF at 200 dpi, "
    "and (b) the embedded bitmap extracted at its own native resolution with pdfimages. The two reads were "
    "compared cell by cell and agree digit for digit across every column of all three editions, including "
    "the two figures most likely to be misread - the FY2022 edition's \"137827.8\" for 2019 and its 0.05%/"
    "2.55% for 2022. A single read of a bitmap would not be good enough to stand behind.\n"
    "\n"
    "EDITION CHOICE. GHIB adopted the KM1 template in its FY2022 edition. The FY2022, FY2023 and FY2024 "
    "editions each print the full five-column template (T to T-4), so FY2024, FY2023 and FY2022 are each "
    "taken from the edition in which that year is the reporting year. FY2021, FY2020 and FY2019 have no "
    "own-edition KM1: the FY2021, FY2020 and FY2019 Pillar 3 reports print instead a bespoke single-column "
    "list headed \"Key Metrics\" (Available capital / Risk-Weighted Assets / Risk-based capital ratios / "
    "leverage / LCR / NSFR) with no template row numbers, no SREP or buffer rows and no cash-inflow/outflow "
    "split. That is not the KM1 template, so it is not reproduced here; those three columns come from the "
    "FY2022 edition, the earliest edition that carries them inside the template.\n"
    "\n"
    "FY2025 IS NOW POPULATED, AND THE ROUTE MATTERS. This sheet said \"FY2025 is blank, not missing\" as "
    "recently as 16 September 2026, on the strength of the same WordPress media endpoint used here: at "
    "that date /wp-json/wp/v2/media?search=pillar enumerated exactly six Pillar 3 PDFs ever uploaded, the "
    "newest being GHIB-2024-Pillar-3-Disclosures.pdf (12 November 2025). Re-queried on 18 September 2026 "
    "the same endpoint returns SEVEN, the new one being GHIB-2025-Pillar-3-Disclosures.pdf, uploaded that "
    "same day at 14:45:36 (the PDF's own CreationDate is 18 September 2026 11:27 BST). The earlier "
    "negative was therefore correct at the time and simply expired - which is the argument for re-testing "
    "a leading-edge negative against the bank's own index rather than treating it as settled. Note also "
    "that on 18 September the Bank's homepage and /legal-documents/ page still linked only the FY2024 "
    "edition, so following links alone would have missed it; the media index is the enumerating source "
    "for this bank.\n"
    "THE FY2025 TABLE IS LIVE TEXT, THE FIRST GHIB EDITION THAT IS. Unlike FY2019-FY2024, where the "
    "key-metrics table is a pasted bitmap and every figure had to be read visually from two independent "
    "renderings, the FY2025 edition was produced in Adobe Illustrator 29.8 with the table as selectable "
    "text, and pdftotext -layout extracts every cell. The FY2025 column above is a text transcription, "
    "not a visual read. Two artefacts of that extraction were resolved against the rendered page and are "
    "noted here rather than silently fixed: row 13's FY2025 value wraps across two lines as \"1,141,15\" / "
    "\"6\" (it is 1,141,156), and row 1's FY2022 COMPARATIVE prints as \"152, 19\" where rows 2 and 3 print "
    "152,019 - a typo in the Bank's own FY2025 table, which costs this workbook nothing because FY2022 is "
    "taken from the FY2022 edition, not from this comparative.\n"
    "\n"
    "ROW SET. GHIB prints rows 1-9, 11, UK 7a, UK 7d, UK 11a, 12-17, UK 16a, UK 16b and 18-20 and no "
    "others. UK 7b, UK 7c, UK 8a, UK 9a, 10, UK 10a and the 14a-14e additional-leverage block appear in no "
    "GHIB edition at all. Those rows are therefore absent from this sheet because the Bank does not print "
    "them, not because they were not found. The row set is identical across the FY2022, FY2023 and FY2024 "
    "editions.\n"
    "\n"
    "ZERO GLYPHS. GHIB uses no dashes in this table. Rows 18-20 for FY2021, FY2020 and FY2019 are printed "
    "as EMPTY cells (with the asterisked footnote reproduced above), and are left blank here. Every \"0.00%\" "
    "in row 9 is a printed measured zero and is kept as such.\n"
    "\n"
    "RESTATEMENTS BETWEEN GHIB'S OWN EDITIONS, recorded and not reconciled. (a) Row 9 for 2022: the FY2022 "
    "edition prints 0.05% and row 11 prints 2.55%, while the FY2023 and FY2024 editions restate the same "
    "2022 column to 0.00% and 2.50%. The FY2022 edition's own figures are used, per the standing rule. "
    "(b) Rows 1-3 for 2019: the FY2022 edition prints \"137827.8\" - one decimal place, unique in the whole "
    "table - where the FY2023 edition prints \"137,828\". Reproduced as the FY2022 edition printed it.\n"
    "\n"
    "DIFFERENCES AGAINST THE SINGLE-METRIC SHEETS IN THIS WORKBOOK, all of them real basis differences "
    "rather than transcription slips:\n"
    "• Leverage Ratio, FY2021, FY2020 and FY2019 - A CROSS-EDITION DIVERGENCE, NOT A BASIS DIFFERENCE. "
    "Row 14 here shows 15.18% / 17.10% / 19.99%; the Leverage Ratio sheet shows 15.20% / 17.14% / 20.06%. "
    "WHICH SOURCE EACH SIDE COMES FROM: this sheet's three figures are the COMPARATIVE columns of the "
    f"FY2022 edition's KM1 (p.4, Table1, read from the embedded bitmap - {P3_2022_URL}); the Leverage Ratio "
    f"sheet's three figures come from each year's OWN edition - the FY2021 Pillar 3 p.4 Table1 ({P3_2021_URL}), "
    f"the FY2020 Pillar 3 p.8 Table1 ({P3_2020_URL}) and the FY2019 Pillar 3 p.9 Table1 ({P3_2019_URL}). "
    "AN EARLIER VERSION OF THIS NOTE ATTRIBUTED THE GAP TO THE UK-vs-Basel III BASIS. That explanation was "
    "tested against the documents on 16 September 2026 and does NOT hold, so it has been withdrawn. Two "
    "findings rule it out. (a) The FY2021 edition's own table is headed \"UK leverage ratio\" and its line is "
    "\"Total UK leverage ratio exposure measure (%)\" - already the UK basis - yet it still prints 15.20% "
    "against the KM1's 15.18%. (b) Excluding GHIB's Bank of England reserves (£161m of a £791m FY2021 "
    "exposure) would move the ratio by whole percentage points, not by four hundredths of one. THE ACTUAL "
    "PATTERN, which is arithmetic and checkable in the FY2022 table itself: row 14 ties exactly to that "
    "table's own rows 1 and 13 in the REPORTING year (152,019/637,251 = 23.855% -> the 23.86% printed) but "
    "falls slightly BELOW its own rows 1/13 in EVERY comparative column - 120,301/791,289 = 15.203% against "
    "15.18% printed, 131,539/767,198 = 17.145% against 17.10%, 137,827.8/686,553 = 20.075% against 19.99%, "
    "and 137,348/716,336 = 19.174% against the 19.07% printed for 2018. In each case the quotient of the "
    "FY2022 table's own rows reproduces that year's OWN edition figure (15.20% / 17.14% / 20.06%), which is "
    "what the Leverage Ratio sheet carries. So the FY2022 edition restated row 14 alone in its comparative "
    "columns, leaving it inconsistent with rows 1 and 13 printed beside it. Every other comparative in that "
    "table agrees with the earlier editions exactly - the FY2020 edition's own Table1 prints the same "
    "131,539 CET1, 372,287 RWAs, 199,128 HQLA, 64,224 net outflow and 310.06% LCR that the FY2022 KM1's 2020 "
    "column prints - so row 14 is the single divergent line. BOTH SETS ARE GHIB'S OWN PUBLISHED FIGURES AND "
    "NEITHER HAS BEEN ADJUSTED: each sheet carries the figure from the source appropriate to it (KM1 from "
    "the template, the metric sheet from each year's own edition), the divergence is recorded here rather "
    "than reconciled, and no value was changed to make the two sides agree. A further wrinkle on FY2021 "
    "only: that edition contradicts ITSELF, its Table1 printing 15.20% while its own narrative two "
    "paragraphs below says \"The leverage ratio as at 31 December 2021 was 15.18%\" - so the FY2022 "
    "comparative reproduces the FY2021 narrative while the Leverage Ratio sheet reproduces the FY2021 "
    "table.\n"
    "WHAT MOST LIKELY DRIVES THE GAP - a footnote found on 2026-09-16 that reclassifies the metric-sheet "
    "side, recorded as the well-evidenced reading it is and NOT as a figure change. Section 5.14 'Risk of "
    "Excessive Leverage' of EVERY GHIB edition captions its leverage ratio as computed 'using a "
    "TRANSITIONAL definition of Tier 1 capital' - FY2021 15.2%, FY2020 17.14%, FY2019 20.06%, the very "
    "figures the Leverage Ratio sheet carries. The FY2022 KM1's row 14 carries no such caption. Back out "
    "the numerator implied by each printed row 14 against that table's own row 13 exposure and the "
    "shortfall against its own row 1 capital is 743 (2018), 586 (2019), 348 (2020), 183 (2021) and "
    "effectively nil (2022, the reporting year) - a monotonic decay to zero, which is the characteristic "
    "shape of an IFRS 9 transitional relief add-back amortising away. So the most likely reading is that "
    "row 14 is struck on FULLY LOADED Tier 1 while row 1 and the earlier editions are on the TRANSITIONAL "
    "definition. THIS IS AN INFERENCE FROM THE ARITHMETIC PLUS THAT CAPTION, NOT SOMETHING GHIB STATES: "
    "the Bank prints no fully-loaded/transitional split (it prints none of the 14a-14e rows where that "
    "split normally lives), so it is offered as the best available explanation and not as a sourced fact. "
    "Nothing above was recomputed or adjusted on the strength of it - both sides keep the figures their "
    "own sources print.\n"
    "• LCR, FY2025 - A ROUNDING DIFFERENCE WITHIN ONE DOCUMENT, NEW IN THE FY2025 EDITION. Row 17 here "
    "prints 213.4% and row 20 prints 181.4%; the LCR and NSFR metric sheets carry 213.49% and 181.39% "
    "from that same edition's Table 13 (p.37 printed) and section 5.4 narrative. The FY2025 edition "
    "rounds its own KM1 rows 17 and 20 to 1dp in the 2025 and 2024 columns while printing 2dp in the "
    "2023/2022/2021 columns of the very same rows; earlier editions printed 2dp throughout, which is why "
    "this disagreement appears for the first time in FY2025. Both figures are GHIB's own and neither has "
    "been adjusted.\n"
    "• NSFR, FY2021 and FY2020: rows 18-20 are blank here because GHIB's KM1 leaves them blank, while the "
    "NSFR sheet carries 195% (FY2021) and 198% (FY2020) from those years' own bespoke tables, with "
    "available/required stable funding of 318,949/163,592 and 293,588/148,293 respectively. The KM1 "
    "footnote explains the blanks: the CRR2 NSFR rules only commenced in 2022.\n"
    "• Total RWAs, FY2019: row 4 here is 329,256, transcribed directly from the FY2022 edition's KM1. The "
    "Total RWAs sheet previously carried 329,260, rounded off the FY2020 edition's narrative \"£329.26m\"; "
    "it has now been corrected to the KM1's directly-disclosed 329,256. The FY2019 edition's own Table 1 "
    "figure of 281,553 is the credit-risk subtotal and is preserved on its own labelled row of that sheet - "
    "see its note.\n"
    "\n"
    + P3_DISCOVERY_NOTE
)

bw.add_km1_sheet(
    title="Ghana International Bank Plc — KM1 Key Metrics",
    subtitle="The Bank's own published UK key-metrics (KM1) template, reproduced in GHIB's row order with "
             "its own template row numbers, labels and printed precision. Amounts in £'000, ratios as "
             "printed. Entity basis. The table is an IMAGE in every GHIB Pillar 3 PDF and was read visually "
             "from the rendered page for FY2024 and earlier; the FY2025 edition is the first with a live-text "
             "table. FY2021-FY2019 come from the FY2022 edition because GHIB published no KM1 template "
             "before it.",
    rows=km1_rows,
    sources_text=KM1_SOURCES,
    first_col_width=76,
    source_height=460,
)

metric("CET1 Capital", "£'000", [("Common Equity Tier 1 (CET1) capital", CET1_CAPITAL)], note=CET1_CAP_NOTE)
metric("CET1 Ratio", "%", [("Common Equity Tier 1 ratio", CET1_RATIO)], note=FY2025_AR_BASIS_NOTE)
metric("Tier 1 Capital", "£'000", [("Tier 1 capital", CET1_CAPITAL)], note=NO_AT1_FY2025_NOTE + " FY2025 is stated only to £0.1m.")
metric("Tier 1 Ratio", "%", [("Tier 1 ratio", CET1_RATIO)], note=NO_AT1_FY2025_NOTE + " The FY2025 Annual Report states the core tier 1 capital ratio as 21.5%, equal to the CET1 ratio.")
metric("Total Capital", "£'000", [("Total capital", CET1_CAPITAL)], note=NO_AT1_FY2025_NOTE + " FY2025 is stated only to £0.1m.")
metric("Total Capital Ratio", "%", [("Total capital ratio", CET1_RATIO)], note=NO_AT1_FY2025_NOTE + " The FY2025 Annual Report states the CRD IV capital adequacy ratio as 21.5%, equal to the CET1 and core tier 1 ratios.")
metric("Total RWAs", "£'000",
       [("Total risk-weighted exposure amount", TOTAL_RWA),
        ("FY2019 only — as printed in the FY2019 Pillar 3's Table 1 (credit-risk subtotal, see note)",
         TOTAL_RWA_AS_PRINTED_FY2019)],
       note="FY2025 FILLED 2026-09-18 with 751,519, printed directly as row 4 of the FY2025 Pillar 3's own "
            "KM1 (p.14 printed). It had been blank because the FY2025 Annual Report states no RWA figure "
            "and was deliberately NOT back-solved from CET1 / 21.5% - the document has now supplied it, so "
            "nothing was ever derived. The Bank's own narrative corroborates it (\"an increase of 7% in risk "
            "weighted assets (£700.37m in 2024 to £751.51m in 2025)\"), and 161,750/751,519 = 21.522%, "
            "reproducing the printed 21.52% CET1 ratio. " + TOTAL_RWA_NOTE)

# ---------------------------------------------------------------
# RWA Breakdown: Table 2 "Breakdown of the Bank's Regulatory Capital
# Requirement" from each year's own Pillar 3 Disclosures - Credit risk
# categories give RWA directly; Operational risk and Market risk RWA are
# CALCULATED as (Capital Requirement / 8%), since the table only states
# their capital requirement, not RWA - cross-checked against each year's
# own disclosed Total RWAs figure (Total RWAs sheet), matching within
# rounding for every year (e.g. FY2024: 700,375 calculated vs 700,374
# disclosed).
# ---------------------------------------------------------------
RWA_CATEGORIES = {
    "Central Gov/Central Banks": {"FY2025": 66628, "FY2024": 27645, "FY2023": 27361, "FY2022": 35066,
                                  "FY2021": 43896, "FY2020": 21860, "FY2019": 33795},
    "Corporates": {"FY2025": 502959, "FY2024": 475975, "FY2023": 283530, "FY2022": 274893,
                   "FY2021": 201102, "FY2020": 151082, "FY2019": 148056},
    "Institutions": {"FY2025": 58742, "FY2024": 64563, "FY2023": 80749, "FY2022": 125314,
                     "FY2021": 92530, "FY2020": 99623, "FY2019": 60002},
    "Other Items": {"FY2025": 14082, "FY2024": 18447, "FY2023": 20363, "FY2022": 20893,
                    "FY2021": 21987, "FY2020": 9577, "FY2019": 3452},
    "Public Sector Entities": {"FY2025": 32952, "FY2024": 55699, "FY2023": 32940, "FY2022": 37618,
                               "FY2021": 46854, "FY2020": 43483, "FY2019": 34593},
    "Retail": {"FY2025": 139, "FY2024": 148, "FY2023": 5870, "FY2022": 133, "FY2021": 1226,
               "FY2020": 184, "FY2019": 234},
    # FY2025 prints an em-dash for Multilateral Development Banks in BOTH the
    # capital-requirement and RWA columns (the class still carries a 34,369 EAD).
    # Kept as the literal dash the Bank printed, NOT converted to 0 - which is a
    # different statement, and is what the FY2024/FY2019 tables actually print.
    "Multilateral Development Banks": {"FY2025": "-", "FY2024": 0, "FY2019": 0},
    "Covered bonds": {"FY2025": 3030, "FY2024": 2020},
    # An exposure class that appears for the first time in the FY2025 table.
    "Claims on inst & corp with CR assessment": {"FY2025": 1193},
    # An "Exposures in Default" exposure class appears only in the FY2019 table.
    "Exposures in Default": {"FY2019": 1421},
}
RWA_CREDIT_TOTAL = {"FY2025": 679725, "FY2024": 644497, "FY2023": 450813, "FY2022": 493919, "FY2021": 407595,
                    "FY2020": 325809, "FY2019": 281553}
RWA_OPRISK_CAPREQ = {"FY2025": 5723, "FY2024": 4147, "FY2023": 2963, "FY2022": 2690, "FY2021": 3173,
                     "FY2020": 3665, "FY2019": 3731}
RWA_MARKET_CAPREQ = {"FY2025": 20, "FY2024": 323, "FY2023": 418, "FY2022": 813, "FY2021": 237,
                     "FY2020": 54, "FY2019": 85}
RWA_OPRISK = {y: round(v / 0.08) for y, v in RWA_OPRISK_CAPREQ.items()}
RWA_MARKET = {y: round(v / 0.08) for y, v in RWA_MARKET_CAPREQ.items()}
RWA_TOTAL_CALC = {y: RWA_CREDIT_TOTAL[y] + RWA_OPRISK[y] + RWA_MARKET[y] for y in RWA_CREDIT_TOTAL}

rwa_rows = [
    ("SECTION", "Credit risk RWA by exposure class", {}),
    ("DATA", "Central Gov/Central Banks", RWA_CATEGORIES["Central Gov/Central Banks"]),
    ("DATA", "Corporates", RWA_CATEGORIES["Corporates"]),
    ("DATA", "Institutions", RWA_CATEGORIES["Institutions"]),
    ("DATA", "Other Items", RWA_CATEGORIES["Other Items"]),
    ("DATA", "Public Sector Entities", RWA_CATEGORIES["Public Sector Entities"]),
    ("DATA", "Retail", RWA_CATEGORIES["Retail"]),
    ("DATA", "Multilateral Development Banks", RWA_CATEGORIES["Multilateral Development Banks"]),
    ("DATA", "Covered bonds", RWA_CATEGORIES["Covered bonds"]),
    ("DATA", "Claims on inst & corp with CR assessment (a separate class in the FY2025 table only)",
     RWA_CATEGORIES["Claims on inst & corp with CR assessment"]),
    ("DATA", "Exposures in Default (a separate class in the FY2019 table only)", RWA_CATEGORIES["Exposures in Default"]),
    ("TOTAL", "Total credit and counterparty risk RWA", RWA_CREDIT_TOTAL),
    ("SECTION", "Other risk types (RWA calculated as Capital Requirement / 8% - see source note)", {}),
    ("DATA", "Operational risk (Basic Indicator Approach)", RWA_OPRISK),
    ("DATA", "Market risk", RWA_MARKET),
    ("TOTAL", "Total RWAs (calculated - cross-checked against Total RWAs sheet)", RWA_TOTAL_CALC),
]

bw.add_rwa_breakdown_sheet(
    title="Ghana International Bank Plc — RWA Breakdown",
    subtitle="£'000, FY2019-FY2025. Credit risk RWA directly disclosed by exposure class; Operational/Market "
             "risk RWA calculated from disclosed capital requirements - see source note.",
    rows=rwa_rows,
    sources_text=p3_sources(page="7") + "\n\nRWA BREAKDOWN NOTE: sourced from Table 2 'Breakdown of the "
        "Bank's Regulatory Capital Requirement' in each year's own Pillar 3 Disclosures (Central Gov/Central "
        "Banks, Corporates, Institutions, Other Items, Public Sector Entities, and Retail columns give RWA "
        "directly; Multilateral Development Banks and Covered bonds are new categories introduced FY2024, "
        "and 'Claims on inst & corp with CR assessment' is a further new class introduced FY2025). "
        "FY2025 ADDED 2026-09-18 from the FY2025 Pillar 3's Table 2, p.16 printed (PDF p.15) - the first "
        "GHIB edition in which this table is live text rather than a bitmap, so it is a text "
        "transcription rather than a visual read. The cross-check that this sheet applies to every other "
        "year passes for FY2025 too: 679,725 credit + 71,538 operational + 250 market = 751,513 against "
        "the 751,519 that edition's own KM1 row 4 discloses, a 6 (0.0008%) rounding difference of the "
        "same order as FY2024's 1. THE FY2025 MULTILATERAL DEVELOPMENT BANKS CELL IS A PRINTED DASH and "
        "is reproduced as the literal \"-\" the Bank printed, NOT as 0: that class still carries a 34,369 "
        "exposure at default in the same table, so a dash and a zero are not interchangeable here. "
        "Operational risk and Market risk RWA are CALCULATED as (Capital Requirement / 8%), since the table "
        "states only their capital requirement, not RWA directly - independently cross-checked against each "
        "year's own disclosed Total RWAs figure (Total RWAs sheet), matching within rounding for every year "
        "(e.g. FY2024: 700,375 calculated here vs 700,374 disclosed). "
        "FY2020 AND FY2019 ADDED 2026-09-15 from the newly-located editions of those years (FY2020 Table 2, "
        "p.11, text-extractable; FY2019 Table 2, p.11, an image in the PDF and therefore read VISUALLY from "
        "the rendered page rather than OCR'd). FY2019 introduces one exposure class the later tables do not "
        "carry, 'Exposures in Default' - a genuine presentation difference, not a transcription gap. "
        "IMPORTANT for FY2019: the calculated total here (281,553 credit + 46,638 operational + 1,063 market "
        "= 329,254) does NOT agree with the 281,553 that the FY2019 Pillar 3's own Table 1 prints as 'Total "
        "Risk-Weighted Assets' - because that Table 1 figure is the credit-risk subtotal, as the breakdown "
        "above makes plain. See the Total RWAs sheet's note for the full evidence; the cross-check that "
        "passes for every other year deliberately fails here and the failure is the finding.",
    first_col_width=58,
    source_height=260,
    unit_suffix="",
)

metric("Leverage Ratio", "%", [("Leverage ratio excluding claims on central banks", LEVERAGE_RATIO)],
       note="FY2025 FILLED 2026-09-18 with 14.17%, from row 14 of the FY2025 Pillar 3's KM1, which its own "
            "section 1.6 narrative repeats verbatim (\"The leverage ratio as at 31 December 2025 was "
            "14.17%\", p.14 printed). THE SAME DOCUMENT ALSO SAYS 12.79%, in section 5.14 'Risk of "
            "Excessive Leverage' (p.39 printed). Recorded, not reconciled: 14.17% is carried here because "
            "two independent places in the document agree on it and because section 5.14 of EVERY GHIB "
            "edition is struck on a transitional Tier 1 definition and diverges the same way (FY2024: "
            "14.66% in the KM1 versus 13.9% in its own section 5.14). No figure was adjusted to make the "
            "two agree. FY2019 (20.06%) and FY2020 (17.14%) FILLED 2026-09-15 "
            "from the newly-located editions of those years. BASIS CAVEAT for those two years only: the "
            "FY2019/FY2020 Table 1 labels this line 'Total Basel III leverage ratio exposure measure (%)' "
            "- which is itself a mislabel by the Bank, since the value is plainly the ratio and not an "
            "exposure amount - while the FY2021 edition heads the same line 'UK leverage ratio' / 'Total UK "
            "leverage ratio exposure measure (%)', which is where this row's title comes from. The labels "
            "differ across the run and are reported as the Bank writes them. THE LABEL CHANGE DOES NOT "
            "APPEAR TO BE A BASIS CHANGE, though: all three figures reconcile to the central-bank-EXCLUDING "
            "exposure measure that the FY2022 edition's KM1 prints on its row 13 (131,539/767,198 = 17.145% "
            "for FY2020 and 137,827.8/686,553 = 20.075% for FY2019, against the 17.14% and 20.06% carried "
            "here). An earlier version of this note suggested FY2019/FY2020 might sit on the wider, "
            "central-bank-inclusive denominator; that was checked against the documents on 16 September 2026 "
            "and withdrawn, since excluding GHIB's Bank of England reserves would move these ratios by whole "
            "percentage points rather than by hundredths. DIVERGENCE AGAINST THE KM1 SHEET, recorded not "
            "reconciled: the FY2022 edition's KM1 comparative columns print 15.18% / 17.10% / 19.99% for "
            "FY2021 / FY2020 / FY2019 where this sheet carries each year's own edition figure of 15.20% / "
            "17.14% / 20.06%. That KM1 row 14 ties to its own rows 1 and 13 in its reporting year but falls "
            "below them in every comparative column, so the two sides are both GHIB's own and neither has "
            "been adjusted to agree - the full arithmetic is set out in the KM1 Key Metrics sheet's note. "
            "Separately, the FY2021 edition contradicts itself by a rounding step: Table 1 prints "
            "15.20% (the value carried here) while that document's own narrative says 15.18% - reproduced "
            "as printed, not reconciled. BASIS CAPTION FOUND 2026-09-16 (applies to every year on this "
            "sheet, not just FY2019/FY2020): section 5.14 'Risk of Excessive Leverage' of every GHIB "
            "edition states these ratios are computed 'using a transitional definition of Tier 1 "
            "capital'. The row title is therefore a TRANSITIONAL-basis leverage ratio, which is most "
            "likely why it sits slightly above the FY2022 KM1's comparative row 14 in each of FY2021, "
            "FY2020 and FY2019 - see the KM1 Key Metrics sheet's note for the arithmetic behind that "
            "reading, and note that it is an inference rather than something the Bank states.")
metric("LCR", "%", [("Liquidity coverage ratio", LCR)],
       note=FY2025_AR_BASIS_NOTE + " FY2025 UPGRADED 2026-09-18 from the Annual Report's \"213%\" to "
            "213.49%, printed in the FY2025 Pillar 3's Table 13 (p.37 printed) and repeated in its "
            "section 5.4 narrative, with components HQLA 447,861,842 / net liquidity outflow "
            "209,779,358. Its KM1 row 17 prints the same ratio to 1dp as 213.4%, which is what the KM1 "
            "sheet reproduces as printed - so verify_workbook.py reports a KM1-vs-this-sheet "
            "disagreement for FY2025 that is a rounding difference inside one document, not a "
            "transcription slip, and neither side has been changed to silence it. The AR and Pillar 3 "
            "LCR bases agree for this bank: the FY2024 "
            "Annual Report's year-end LCR of 256% matches the FY2024 Pillar 3 LCR of 256.31%. FY2019 "
            "(278.41%) FILLED and FY2020 UPGRADED 2026-09-15: FY2020 previously read '310%' from the "
            "Annual Report and now reads 310.06% from the FY2020 Pillar 3's own Table 1, which also "
            "discloses the components (HQLA 199,128 / net liquidity outflow 64,224). The two agree, so "
            "this is a precision upgrade, not a conflict. FY2019's components are HQLA 206,996 / net "
            "liquidity outflow 74,348. Both are point-in-time 31 December figures, consistent with the "
            "rest of this row - none of GHIB's editions report a 12-month-average LCR, so there is no "
            "average-vs-point-in-time mixing on this sheet.")
metric("NSFR", "%", [("Net Stable Funding Ratio", NSFR)],
       note=NSFR_NOTE + " FY2025 FILLED 2026-09-18 with 181.39%, from the FY2025 Pillar 3's section 5.4 "
            "narrative (available stable funding 483,227 / required stable funding 266,394, KM1 rows "
            "18-19). Its KM1 row 20 prints the same ratio to 1dp as 181.4%, which is what the KM1 sheet "
            "reproduces as printed; the FY2025 edition rounds this row where its FY2024 predecessor "
            "printed 2dp. FY2020 FILLED "
            "2026-09-15 with 198%, a real "
            "disclosure from the FY2020 Pillar 3's Table 1 (available stable funding 293,588 / required "
            "stable funding 148,293), which the Bank published voluntarily well before the UK NSFR "
            "requirement began on 1 January 2022 - so this project's default assumption that pre-FY2022 "
            "NSFR blanks are structural does not apply to FY2020 or FY2021 here. FY2021 FILLED with 195% "
            "at the same time, from the FY2021 edition's Table 1 (available stable funding 318,949 / "
            "required stable funding 163,592), read visually from the rendered page because that table is "
            "an image, and independently corroborated by that document's own narrative ('the Net Stable "
            "Funding Ratio (NSFR), at 195%'). FY2019 is a genuine, document-level negative rather than an "
            "unresearched gap: the FY2019 edition's Table 1 was read in full and simply has no Net Stable "
            "Funding Ratio section at all, the NSFR block first appearing in the FY2020 edition.")

bw.add_not_disclosed_metric_sheets(
    ["MREL Ratio"], p3_sources(),
    # GA-020 (2026-09-19): all seven editions (P3_2019..P3_2025_URL, 33-44 pages,
    # native text) full-text searched for MREL / loss-absorbing / eligible
    # liabilities / 'minimum requirement for own funds': zero hits.
    statements={"MREL Ratio": {y: (f"Not published – GHIB {y} Pillar 3 Disclosures (full text searched 2026-09-19) "
                                   "contain no MREL figure or reference") for y in YEARS}},
    per_note={"MREL Ratio": "No MREL figure or statement appears in any GHIB Pillar 3 edition FY2019-FY2025 "
                            "(each full-text searched 2026-09-19). The earlier wording here - that GHIB 'is not a "
                            "UK resolution entity subject to MREL' - was an inference no document states, so the "
                            "cells record non-publication rather than non-applicability."},
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {
            "FY2025": 1184847200, "FY2024": 1095686063, "FY2023": 800648688, "FY2022": 899850273, "FY2021": 766627624, "FY2020": 746473535}),
        ("Loans and advances to customers", {
            "FY2025": 152082149, "FY2024": 57178671, "FY2023": 53066533, "FY2022": 65038106, "FY2021": 89440019, "FY2020": 72138823}),
        ("Amounts owed to depositors", {
            "FY2025": 393649207, "FY2024": 255765401, "FY2023": 270972181, "FY2022": 347038076, "FY2021": 258550273, "FY2020": 276077311}),
        ("Total Equity", {
            "FY2025": 174718204, "FY2024": 168466456, "FY2023": 162328173, "FY2022": 157848993, "FY2021": 120065401, "FY2020": 131806062}),
    ],
    balance_sheet_unit="£",
    income_statement_totals=[
        ("Operating income", {
            "FY2025": 50581488, "FY2024": 47404294, "FY2023": 39956124, "FY2022": 27022086, "FY2021": 16276979, "FY2020": 17547212}),
        ("Total operating expenses", {
            "FY2025": -43637647, "FY2024": -41158713, "FY2023": -36722520, "FY2022": -35155545, "FY2021": -27656389, "FY2020": -22914590}),
        ("Profit/(Loss) for the year", {
            "FY2025": 5402714, "FY2024": 4236801, "FY2023": 3112295, "FY2022": -9042978, "FY2021": -9043124, "FY2020": -5152727}),
    ],
    income_statement_unit="£",
    equity_changes_totals=[
        ("Opening equity", {
            "FY2025": 168466456, "FY2024": 162328173, "FY2023": 157848993, "FY2022": 120065401, "FY2021": 131806062}),
        ("Total comprehensive income/(loss) for the year", {
            "FY2025": 7099489, "FY2024": 6760742, "FY2023": 4479180, "FY2022": -12169122, "FY2021": -11740661}),
        ("Closing equity", {
            "FY2025": 174718204, "FY2024": 168466456, "FY2023": 162328173, "FY2022": 157848993, "FY2021": 120065401}),
    ],
    equity_changes_unit="£",
    cash_flow_totals=[
        ("Net cash generated from/(used in) operating activities", {
            "FY2025": -61057195, "FY2024": -63471450, "FY2023": -40429835, "FY2022": 30054133, "FY2021": -32002834, "FY2020": 114829689}),
        ("Net cash used in investing activities", {
            "FY2025": -2565811, "FY2024": -3230461, "FY2023": -2218021, "FY2022": -4237752, "FY2021": -2378005, "FY2020": -1967352}),
        ("Net cash generated from/(used in) financing activities", {
            "FY2025": 18249803, "FY2024": 12597740, "FY2023": -874791, "FY2022": 49037663, "FY2021": -849159, "FY2020": -820894}),
        ("Cash and cash equivalents at the end of the year", {
            "FY2025": 331086867, "FY2024": 376370085, "FY2023": 430365754, "FY2022": 473775651, "FY2021": 398759558, "FY2020": 433918140}),
    ],
    cash_flow_unit="£",
    ratios=[
        ("CET1 Ratio", CET1_RATIO),
        ("Leverage Ratio", LEVERAGE_RATIO),
        ("LCR", LCR),
        ("NSFR", NSFR),
    ],
    note="GHIB is a UK-incorporated PLC (registered England & Wales no. 03468216, a subsidiary of the "
         "Government of Ghana) that reports in GBP throughout - no currency conversion applied. Pillar 3 "
         "figures are not yet available for FY2025 (see the Pillar 3 sheets' own source notes). Figures "
         "are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own "
         "source citation for the underlying document/page.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/GHANA INTERNATIONAL BANK FINANCIALS.xlsx")
