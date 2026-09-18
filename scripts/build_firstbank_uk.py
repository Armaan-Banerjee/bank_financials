import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021", "FY2020", "FY2019"]  # most recent first
YEAR_LABEL = {y: y for y in YEARS}

# ---------------------------------------------------------------
# Source documents. FirstBank UK Limited (Companies House no. 04459383, FRN
# 216772) was named FBN Bank (UK) Limited until its FY2022/FY2023 rename -
# same legal entity throughout, continuity confirmed via Companies House
# filing history. It is a wholly-owned UK subsidiary of First Bank of Nigeria
# Limited. All Annual Report PDFs are DocuSign-flattened scans (0 extractable
# text) - every cash flow figure below was read directly off the rendered
# page image, not OCR'd/extracted text.
# ---------------------------------------------------------------
AR2025_URL = "https://find-and-update.company-information.service.gov.uk/company/04459383/filing-history/MzUyNzc5Nzc3MWFkaXF6a2N4/document?format=pdf&download=0"
AR2024_URL = "https://find-and-update.company-information.service.gov.uk/company/04459383/filing-history/MzQ3MzE2Nzc1OGFkaXF6a2N4/document?format=pdf&download=0"
AR2023_URL = "https://find-and-update.company-information.service.gov.uk/company/04459383/filing-history/MzQyNjA0OTI3OWFkaXF6a2N4/document?format=pdf&download=0"
AR2022_URL = "https://find-and-update.company-information.service.gov.uk/company/04459383/filing-history/MzM4NTMzODE5NmFkaXF6a2N4/document?format=pdf&download=0"
AR2021_URL = "https://find-and-update.company-information.service.gov.uk/company/04459383/filing-history/MzM0MTI4NjI3MGFkaXF6a2N4/document?format=pdf&download=0"
AR2020_URL = "https://find-and-update.company-information.service.gov.uk/company/04459383/filing-history/MzMxMTQ1Nzc1OGFkaXF6a2N4/document?download=0&format=pdf"
AR2019_URL = "https://find-and-update.company-information.service.gov.uk/company/04459383/filing-history/MzI3NzY5NDQwNWFkaXF6a2N4/document?download=0&format=pdf"

# --- Pillar 3 source URLs ----------------------------------------------------
# ALL SIX of the Bank's own Pillar 3 URLs on fbnbank.co.uk are DEAD as at
# 2026-09-16. Each was re-fetched this session and returns HTTP 404 with
# Content-Type text/html (a ~363KB WordPress "not found" page), not a PDF - so
# this is a genuine removal, not a 403/WAF block and not a throttled fetch. The
# dead originals are preserved below as ORIG_P3_* and are still named in every
# citation, because the provenance chain must stay readable after the host drops
# the file; the citations additionally carry a Wayback Machine snapshot, which is
# now the only working form.
#
# Snapshots are given in the "id_" form (.../web/<timestamp>id_/<original URL>),
# which is a contract to return the original archived bytes; the bare
# .../web/<timestamp>/ form returns the Wayback *viewer*, whose behaviour the
# Internet Archive can change at any time.
#
# PATH TRAP - DO NOT INFER THE REPORTING YEAR FROM THE URL. Five of the six files
# sit under the upload directory /wp-content/uploads/2019/06/ regardless of which
# financial year they report (only the FY2024 edition is under 2025/09). The
# "2019/06" is the WordPress media-library upload folder, not a reporting date.
# Every one of the six was therefore downloaded and its COVER PAGE read on
# 2026-09-16 to establish the year from the document itself:
#   FY2019 -> "FBN Bank (UK) Limited / Pillar 3 Disclosures / As at 31st December
#             2019", v2.2, issued July 2020         - 650,322 bytes, 27pp
#   FY2020 -> "FBN Bank (UK) Limited ... As at 31st December 2020", v2.0,
#             issued March 2021                     - 974,989 bytes, 36pp
#   FY2021 -> "FBN Bank (UK) Limited ... As at 31st December 2021", v1.0,
#             issued March 2022                     - 832,706 bytes, 39pp
#   FY2022 -> "FirstBank UK Limited ... As at 31st December 2022", v1.0,
#             issued March 2023                     - 785,557 bytes, 39pp
#   FY2023 -> "FirstBank UK Limited ... As at 31st December 2023", v1.0,
#             issued April 2024                     - 705,562 bytes, 33pp
#   FY2024 -> "FirstBank UK Limited ... As at 31st December 2024"
#                                                   - 764,866 bytes, 39pp
# All six begin "%PDF", all six page counts match, and none is exactly 1 MiB (the
# known Wayback truncation failure mode). The cover pages also corroborate the
# FY2022/FY2023 rename from "FBN Bank (UK) Limited" to "FirstBank UK Limited"
# already documented above: the FY2022 edition is the first titled FirstBank UK.
ORIG_P3_2024_URL = "https://www.fbnbank.co.uk/wp-content/uploads/2025/09/FirstBank-UK-Pillar-3-Dec-2024-1.pdf"
ORIG_P3_2023_URL = "https://www.fbnbank.co.uk/wp-content/uploads/2019/06/FirstBank-UK-Pillar-3-Dec-2023.pdf"
ORIG_P3_2022_URL = "https://www.fbnbank.co.uk/wp-content/uploads/2019/06/FirstBank-UK-Pillar-3-Dec-2022-V1.0.pdf"
ORIG_P3_2021_URL = "https://www.fbnbank.co.uk/wp-content/uploads/2019/06/FBNUK-Pillar-3-Disclosures_-2021.pdf"
ORIG_P3_2020_URL = "https://www.fbnbank.co.uk/wp-content/uploads/2019/06/FBNUK_Pillar-3-Disclosures_2020.pdf"
ORIG_P3_2019_URL = "https://www.fbnbank.co.uk/wp-content/uploads/2019/06/FBNUK-Pillar-3-Dec-19-FINAL-Published_v3.pdf"

P3_2024_URL = "https://web.archive.org/web/20251203042809id_/" + ORIG_P3_2024_URL
P3_2023_URL = "https://web.archive.org/web/20240527034030id_/" + ORIG_P3_2023_URL
P3_2022_URL = "https://web.archive.org/web/20240219211830id_/" + ORIG_P3_2022_URL
P3_2021_URL = "https://web.archive.org/web/20240718195901id_/" + ORIG_P3_2021_URL
P3_2020_URL = "https://web.archive.org/web/20231206074745id_/" + ORIG_P3_2020_URL
P3_2019_URL = "https://web.archive.org/web/20200918094410id_/" + ORIG_P3_2019_URL

P3_DEAD_URL_NOTE = (
    "DEAD SOURCE URL REGISTER (recorded 2026-09-16, nothing deleted). Every one of FirstBank UK's six "
    "Pillar 3 disclosure PDFs has been removed from the Bank's own website. The original published URLs "
    "were: FY2024 " + ORIG_P3_2024_URL + "; FY2023 " + ORIG_P3_2023_URL + "; FY2022 " + ORIG_P3_2022_URL +
    "; FY2021 " + ORIG_P3_2021_URL + "; FY2020 " + ORIG_P3_2020_URL + "; FY2019 " + ORIG_P3_2019_URL + ". "
    "All six were re-fetched on 2026-09-16 and every one returned HTTP 404 with Content-Type text/html "
    "(a ~363KB WordPress 'not found' page) rather than a PDF - a genuine removal by the host, NOT a "
    "403/WAF block and not a failed or throttled fetch. They are recorded here rather than deleted so the "
    "provenance of each figure stays readable now that the publisher no longer serves the document. The "
    "working replacement for each is the Wayback Machine snapshot cited alongside it on every sheet, given "
    "in the 'id_' form (https://web.archive.org/web/<timestamp>id_/<original URL>) which returns the "
    "original archived bytes rather than the Wayback viewer page. "
    "IMPORTANT - the URL path does NOT indicate the reporting year: five of the six files sit under the "
    "WordPress upload folder /wp-content/uploads/2019/06/ whatever year they report (only FY2024 is under "
    "2025/09). Each snapshot was therefore downloaded and its cover page read on 2026-09-16 to confirm the "
    "year from the document itself, and all six matched: 'As at 31st December 2019' (27pp), '...2020' "
    "(36pp), '...2021' (39pp), '...2022' (39pp), '...2023' (33pp) and '...2024' (39pp). All six begin "
    "'%PDF' with the page counts stated. The covers also corroborate the entity rename: the FY2022 edition "
    "is the first headed 'FirstBank UK Limited', the FY2021 and earlier editions being headed 'FBN Bank "
    "(UK) Limited' - the same legal entity (company 04459383, FRN 216772) throughout. "
    "No figure in this workbook was changed as part of this URL repair."
)

# ---------------------------------------------------------------
# Currency note: the Bank changed its presentation/functional currency from
# GBP to USD starting with its FY2023 Annual Report and FY2023 Pillar 3
# disclosures (both published in $ from that point on; FY2022 was restated
# by the Bank itself into $ as the FY2023 AR/Pillar 3's own comparative
# column). FY2021 has no $ figure published anywhere by the Bank - to keep
# this whole workbook on one consistent $ basis (rather than mixing £ and $
# across columns), FY2021 is converted here from the Bank's own as-reported
# £ figures using the same Bank of England GBP/USD spot/average methodology
# established for Zenith Bank (UK) Limited (see build_zenith.py): flow
# (P&L/cash-flow) figures at that year's average rate, £1 = $1.3752; balance
# (period-end/capital/RWA) figures at that year-end's spot rate, £1 = $1.3521
# (31 Dec 2021) / $1.3661 (31 Dec 2020, for FY2021's opening cash balance
# only). Rates are Bank of England GBP/USD archive values via
# poundsterlinglive.com's published archive, same source used for Zenith.
# Because flows and balances are converted at different rates, the cash flow
# sheet includes an explicit "Effect of GBP/USD translation" line for FY2021
# so opening + all flows + this line = closing exactly in $ terms - this
# line is purely an artefact of $ translation and has no bearing on the
# Bank's underlying £ results for that year.
# ---------------------------------------------------------------
FX_SPOT_2020 = 1.3661  # 31 Dec 2020 - only used for FY2021's opening cash balance
FX_SPOT_2021 = 1.3521  # 31 Dec 2021
FX_AVG_2021 = 1.3752
FX_SPOT_2019 = 1.3210
FX_AVG_2019 = 1.2767
FX_AVG_2020 = 1.2837

CURRENCY_NOTE = (
    "CURRENCY NOTE: FirstBank UK Limited changed its presentation currency from GBP to USD starting with its "
    "FY2023 Annual Report and FY2023 Pillar 3 disclosures (FY2022 was restated by the Bank itself into $ as "
    "that year's own comparative). FY2021 is not published in $ anywhere by the Bank - to keep this whole "
    "workbook on one consistent $ basis, FY2021 figures below are converted from the Bank's own as-reported £ "
    "figures using the Bank of England GBP/USD spot/average methodology established for Zenith Bank (UK) "
    "Limited: flow figures at the FY2021 average rate (£1 = $1.3752), balance figures at the FY2021 year-end "
    "spot rate (£1 = $1.3521; the FY2020 year-end spot rate of £1 = $1.3661 is used only for FY2021's opening "
    "cash balance). Ratios are NOT converted - dimensionless and currency-invariant, so FY2021's ratios below "
    "are the Bank's own as-reported % figures unchanged. The FY2021 cash flow column includes an explicit "
    "'Effect of GBP/USD translation' line so opening + flows + this line = closing exactly in $ terms; this "
    "line is a translation artefact only and has no bearing on the Bank's underlying £ results for FY2021. "
    "FY2020 and FY2019 comparative figures are converted from the Bank's own five-year summary at the "
    "FY2020/FY2019 year-end spot rates ($1.3661/$1.3210) for balances and calendar-year average rates "
    "($1.2837/$1.2767) for flows."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are FirstBank UK Limited's own Statement of Cash Flows (page images, statutory "
    "accounts filed at Companies House - each report's own accounts are DocuSign-flattened scans):\n"
    f"FY2025: Annual Report and Financial Statements for the year ended 31 December 2025, p.56 (Statement of "
    f"Cash Flows), as filed at Companies House 03 Jul 2026 - {AR2025_URL}\n"
    f"FY2024: Annual Report and Financial Statements for the year ended 31 December 2024, p.48 (Statement of "
    f"Cash Flows), as filed at Companies House 10 Jul 2025 - {AR2024_URL}\n"
    f"FY2023: Annual Report and Financial Statements for the year ended 31 December 2023, p.42 (Statement of "
    f"Cash Flows), as filed at Companies House 26 Jun 2024 - {AR2023_URL}\n"
    f"FY2022: Annual Report and Financial Statements for the year ended 31 December 2023, p.42 (Statement of "
    f"Cash Flows, Restated 31 December 2022 comparative column, $ - the Bank's own USD restatement), as filed "
    f"at Companies House 26 Jun 2024 - {AR2023_URL}\n"
    f"FY2021: Annual Report and Financial Statements (as FBN Bank (UK) Limited) for the year ended 31 December "
    f"2021, p.33 (Statement of Cash Flows, £ as originally reported), as filed at Companies House 08 Jun 2022 - "
    f"{AR2021_URL} - converted to $ per the currency note below.\n\n"
    + CURRENCY_NOTE
)


def p3_sources(page2024=None, page2023=None, page2022=None, page2021=None, table=None):
    lines = ["Sources - FirstBank UK Limited Pillar 3 Disclosures (UK KM1 - Key Metrics" +
             (f", {table}" if table else "") + "):\n"]
    if page2024:
        lines.append(f"FY2024: Pillar 3 Disclosures, 31st December 2024, p.{page2024} - {P3_2024_URL}\n")
    lines.append(f"FY2023: Pillar 3 Disclosures, 31st December 2023, p.{page2023} ($, own report) - {P3_2023_URL}\n")
    lines.append(f"FY2022: Pillar 3 Disclosures, 31st December 2023, p.{page2023} (Table 1, 2022 comparative "
                 f"column, $ - the Bank's own USD restatement) - {P3_2023_URL}\n")
    lines.append(f"FY2021: Pillar 3 Disclosures (as FBN Bank (UK) Limited), 31st December 2022, p.{page2022} "
                 f"(Table 6, 2021 comparative column, £ as originally reported) - {P3_2022_URL} - converted to "
                 f"$ per the Cash Flow Statement sheet's currency note (ratios unconverted).\n")
    lines.append(f"FY2020/FY2019: Pillar 3 Disclosures (as FBN Bank (UK) Limited), 31st December 2021, Table 1 "
                 f"comparative columns (£ as originally reported; FY2020/FY2019 balance metrics converted at "
                 f"year-end spot rates; ratios unchanged) - {P3_2021_URL}\n")
    lines.append("FY2025: no FY2025 Pillar 3 Disclosures document has been published. THE BANK ITSELF SAYS SO "
                 "IN PRINT: the FY2025 Annual Report's Directors' Report, under 'Capital Structure' (p.5 "
                 "printed, PDF p.8), states that further information on capital adequacy is contained in "
                 "'the Pillar 3 disclosures WHICH WILL BE PUBLISHED on the Bank's website at "
                 "https://www.fbnbank.co.uk/ AFTER THE APPROVAL OF THESE FINANCIAL STATEMENTS' (emphasis "
                 "added). That is a future tense in the Bank's own audited report, which settles the question "
                 "far more strongly than any absence of a link can: the FY2025 edition is pending, not missed. "
                 "Re-confirmed 18 September 2026, the day the FY2025 Annual Report itself first appeared on the "
                 "site (uploads/2026/09/). The Bank has also withdrawn its existing Pillar 3 documents from its "
                 "own website - even the FY2024 URL cited above (last archived 18 October 2025) now returns "
                 "404, and no Pillar 3 file appears anywhere "
                 "under fbnbank.co.uk/wp-content/uploads/2026/, in the site's WordPress media index (the "
                 "wp-json media endpoint returns an empty array for every query, including an unfiltered "
                 "control, so it is disabled rather than empty), in the Yoast page sitemap (which lists no "
                 "disclosures page at all), in the site's own ?s=pillar search, or in the "
                 "Wayback CDX index for the domain (whose newest Pillar 3 capture is the Dec-2024 report). "
                 "CAVEAT ON THAT 404 EVIDENCE, recorded rather than glossed: because the live FY2024 URL 404s "
                 "too, a 404 on a guessed FY2025 path proves nothing here - this site demonstrably moves its "
                 "uploads (the FY2024 Annual Report itself moved from uploads/2019/06/ to uploads/2025/11/). "
                 "The load-bearing evidence is the Bank's own future-tense statement above, not the probes. The "
                 "FY2025 figures populated below therefore come from the Bank's own audited Annual Report and "
                 "Financial Statements for the year ended 31 December 2025, a DocuSign-flattened scan with no "
                 "text layer, read via OCR at 400 dpi:\n"
                 "  - CET1/Tier 1 capital and Total capital: note 32 'Capital management', p.109 (printed), "
                 "PDF p.112 - 'Tier one capital' $413,014,692 and 'Total available capital' $451,590,815, "
                 "restated here in $'000.\n"
                 "  - Total RWAs, CET1 ratio and Total capital ratio: Strategic Report, 'Capital and Liquidity "
                 "Management' table, p.8 (printed), PDF p.11 - Risk Weighted Assets $1,879mn, CET 1 Ratio "
                 "22.0%, Total Capital Adequacy Ratio 24.0%.\n"
                 f"  - Source document: {AR2025_URL}\n"
                 "Both tables are on the same basis as the Pillar 3 KM1 they replace: their own FY2024 "
                 "comparative columns (Tier one capital $363,762,866, Total available capital $414,073,903, "
                 "RWAs $1,396mn, CET 1 Ratio 26.1%, Total Capital Adequacy Ratio 29.7%) match this workbook's "
                 "FY2024 Pillar 3 figures ($363,763k, $414,074k, $1,395,598k, 26.07%, 29.67%) exactly. The "
                 "Strategic Report table also labels the $413mn figure 'CET 1 Capital' while note 32 labels the "
                 "same amount 'Tier one capital', which is why FY2025 is recorded on both the CET1 Capital and "
                 "Tier 1 Capital sheets.\n"
                 "Metrics the Annual Report does NOT print, left blank for FY2025 rather than derived: Tier 1 "
                 "ratio (only the CET1 ratio is labelled, even though the Bank holds no AT1), leverage ratio, "
                 "LCR and NSFR. In particular the Strategic Report's 'Liquidity Capital Ratio (Pillar 1)' "
                 "(FY2025 282%, FY2024 278%) is NOT the LCR and has not been used as one: this workbook's "
                 "FY2024 LCR from the Pillar 3 report is 409.09%, so that line is a different measure.\n")
    lines.append("\n" + P3_DEAD_URL_NOTE)
    return "".join(lines)


bw = BankWorkbook(bank_name="FirstBank UK Limited", years=YEARS, year_label=YEAR_LABEL, header_color="060F0B")

STATEMENTS_SOURCES = (
    "Sources - FirstBank UK Limited's own Statement of Comprehensive Income / Statement of Financial "
    "Position / Statement of Changes in Equity (page images, statutory accounts filed at Companies House - "
    "each report's own accounts are DocuSign-flattened scans):\n"
    f"FY2025/FY2024: Annual Report and Financial Statements for the year ended 31 December 2025, p.53-55 - "
    f"{AR2025_URL}\n"
    f"FY2023/FY2022 (restated): Annual Report and Financial Statements for the year ended 31 December 2023, "
    f"p.39-41 (2022 column restated by the Bank itself into $ - see CURRENCY NOTE below) - {AR2023_URL}\n"
    f"FY2021 (as FBN Bank (UK) Limited, £ as originally reported, converted to $ per the Cash Flow "
    f"Statement's currency note): Annual Report and Financial Statements for the year ended 31 December "
    f"2021, p.30-32 - {AR2021_URL}\n\n"
    f"FY2020/FY2019 (as FBN Bank (UK) Limited, £ as originally reported, converted to $ per the currency "
    f"note): Annual Report and Financial Statements for the years ended 31 December 2020/2019, filed at "
    f"Companies House - {AR2020_URL} / {AR2019_URL}\n\n"
    "EQUITY RECONCILIATION NOTE: the equity roll-forward ties exactly at every boundary from FY2022 onward "
    "using the Bank's own real reported $ figures. The FY2021->FY2022 boundary is the one exception: FY2021's "
    "own report publishes only £ figures, and independently converting FY2021's own closing Statement of "
    "Financial Position at the FY2021 year-end spot rate (£1=$1.3521, matching the Balance Sheet sheet) "
    "produces a Total equity of $285,340k - $443k more than the $284,897k opening balance the Bank itself "
    "later restated into its FY2023 Annual Report's own comparative Statement of Changes in Equity (as at 1 "
    "January 2022, using an implied ~$1.35 flat rate, not a BoE spot rate). This $443k gap is a currency-"
    "conversion-methodology difference, not a transcription error - shown as an explicit, labelled bridging "
    "row rather than force-reconciled or silently adopting one rate over the other. Separately, and NOT an "
    "FX artefact: during FY2022 the Bank's own accounts show a real, disclosed 'Translation impact on share "
    "capital and premium' of $(30,904)k - this is the Bank's own corporate action redenominating its £200m "
    "nominal share capital to a $242m US-dollar-denominated figure (alongside a smaller share premium "
    "adjustment and a new $475k translation reserve), not something this project computed.\n\n"
    + CURRENCY_NOTE
)

bw.add_balance_sheet_sheet(
    title="FirstBank UK Limited — Statement of Financial Position",
    subtitle="$'000 throughout - FY2021 converted from £ at the FY2021 year-end spot rate. See source note at bottom.",
    rows=[
        ("SECTION", "Assets", {}),
        ("DATA", "Cash and bank balances", {
        "FY2025": 22682, "FY2024": 54720, "FY2023": 38231, "FY2022": 28824, "FY2021": 54417,
            "FY2020": 36385, "FY2019": 34028,
        }),
        ("DATA", "Loans and advances to banks", {
        "FY2025": 1036649, "FY2024": 999895, "FY2023": 1186213, "FY2022": 1244332, "FY2021": 1007414,
            "FY2020": 1023554, "FY2019": 939625,
        }),
        ("DATA", "Loans and advances to customers", {
        "FY2025": 939009, "FY2024": 601178, "FY2023": 529947, "FY2022": 400733, "FY2021": 568544,
            "FY2020": 650060, "FY2019": 609612,
        }),
        ("DATA", "Financial assets at fair value through profit or loss", {
        "FY2025": 489526, "FY2024": 33816, "FY2023": 37038, "FY2022": 31396, "FY2021": 20714,
            "FY2020": 36409, "FY2019": 25948,
        }),
        ("DATA", "Investment securities / financial investments at amortised cost", {
        "FY2025": 576261, "FY2024": 1456429, "FY2023": 634655, "FY2022": 1741397, "FY2021": 1805594,
            "FY2020": 1437962, "FY2019": 1845773,
        }),
        ("DATA", "Property and equipment", {
        "FY2025": 5374, "FY2024": 6556, "FY2023": 7738, "FY2022": 9105, "FY2021": 11830,
            "FY2020": 13662, "FY2019": 14707,
        }),
        ("DATA", "Intangible assets", {
        "FY2025": 232, "FY2024": 417, "FY2023": 1122, "FY2022": 1781, "FY2021": 2734,
            "FY2020": 3756, "FY2019": 4216,
        }),
        ("DATA", "Current tax asset", {
            "FY2025": 1917, "FY2024": 952, "FY2021": None,
            # not disclosed as a separate line in FY2023/FY2022 (own report) or FY2021
        }),
        ("DATA", "Other assets", {
        "FY2025": 4701, "FY2024": 3310, "FY2023": 3281, "FY2022": 2429, "FY2021": 2541,
            "FY2020": 2227, "FY2019": 2202,
        }),
        ("DATA", "Deferred tax asset", {
        "FY2025": 8830, "FY2024": 17049, "FY2023": 25819, "FY2022": 32636, "FY2021": 34025,
            "FY2020": 33406, "FY2019": 29057,
        }),
        ("TOTAL", "Total assets", {
        "FY2025": 3085183, "FY2024": 3174323, "FY2023": 2464043, "FY2022": 3492632, "FY2021": 3507813,
            "FY2020": 3237419, "FY2019": 3505179,
        }),
        ("SECTION", "Liabilities", {}),
        ("DATA", "Deposits from banks", {
        "FY2025": 788631, "FY2024": 1518434, "FY2023": 713970, "FY2022": 1764739, "FY2021": 1862419,
            "FY2020": 1656655, "FY2019": 1906883,
        }),
        ("DATA", "Deposits from customers", {
        "FY2025": 1672792, "FY2024": 1060135, "FY2023": 1249444, "FY2022": 1208196, "FY2021": 1030261,
            "FY2020": 1058435, "FY2019": 1003418,
        }),
        ("DATA", "Financial liabilities at fair value through profit or loss", {
        "FY2025": 2143, "FY2024": 3007, "FY2023": 16660, "FY2022": 27888, "FY2021": 19375,
            "FY2020": 172, "FY2019": 0,
        }),
        ("DATA", "Current tax liability", {
            "FY2025": None, "FY2024": None, "FY2023": 1296, "FY2022": 2494, "FY2021": 1573,
            # not disclosed as a separate line in FY2025/FY2024 (nil/not applicable that year)
        }),
        ("DATA", "Subordinated liabilities", {
        "FY2025": 60255, "FY2024": 60240, "FY2023": 60255, "FY2022": 60255, "FY2021": 60427,
            "FY2020": 60227, "FY2019": 60380,
        }),
        ("DATA", "Other liabilities", {
        "FY2025": 138694, "FY2024": 150204, "FY2023": 85964, "FY2022": 128922, "FY2021": 248418,
            "FY2020": 211271, "FY2019": 313847,
        }),
        ("TOTAL", "Total liabilities", {
        "FY2025": 2662514, "FY2024": 2792020, "FY2023": 2127589, "FY2022": 3192494, "FY2021": 3222473,
            "FY2020": 2986760, "FY2019": 3284527,
        }),
        ("SECTION", "Equity", {}),
        ("DATA", "Called up share capital", {
        "FY2025": 242000, "FY2024": 242000, "FY2023": 242000, "FY2022": 242000, "FY2021": 270420,
            "FY2020": 273220, "FY2019": 264200,
        }),
        ("DATA", "Share premium", {
        "FY2025": 24228, "FY2024": 24228, "FY2023": 24228, "FY2022": 24228, "FY2021": 27650,
            "FY2020": 27936, "FY2019": 27014,
        }),
        ("DATA", "Translation reserve", {
            "FY2025": 475, "FY2024": 475, "FY2023": 475, "FY2022": 475, "FY2021": None,
            # translation reserve first created during FY2022 - see Statement of Changes in Equity
        }),
        ("DATA", "Retained earnings / (Accumulated losses)", {
        "FY2025": 155941, "FY2024": 115532, "FY2023": 69751, "FY2022": 33436, "FY2021": -12730,
            "FY2020": -50497, "FY2019": -70562,
        }),
        ("DATA", "Fair value reserve", {
            "FY2025": 26, "FY2024": 69, "FY2023": None, "FY2022": None, "FY2021": None,
        }),
        ("TOTAL", "Equity shareholders' funds", {
        "FY2025": 422669, "FY2024": 382303, "FY2023": 336454, "FY2022": 300139, "FY2021": 285340,
            "FY2020": 250659, "FY2019": 220652,
        }),
        ("TOTAL", "Total equity and liabilities", {
        "FY2025": 3085183, "FY2024": 3174323, "FY2023": 2464043, "FY2022": 3492632, "FY2021": 3507813,
            "FY2020": 3237419, "FY2019": 3505179,
        }),
    ],
    sources_text=STATEMENTS_SOURCES,
    first_col_width=70,
    source_height=340,
    unit_suffix=" ($'000, FY2021 conv. from £)",
)

bw.add_income_statement_sheet(
    title="FirstBank UK Limited — Statement of Profit or Loss and Other Comprehensive Income",
    subtitle="$'000 throughout - FY2021 converted from £ at the FY2021 average rate. See source note at bottom.",
    rows=[
        ("SECTION", "Income", {}),
        ("DATA", "Interest income", {
            "FY2025": 165148, "FY2024": 184560, "FY2023": 153507, "FY2022": 106490, "FY2021": 82152,
        }),
        ("DATA", "Interest income on financial assets at FVTPL", {
            "FY2025": 5910, "FY2024": 2696, "FY2023": 1769, "FY2022": 1808,
            # not a separate line in FY2021's report structure - included within "Interest income" above
        }),
        ("DATA", "Interest expense", {
            "FY2025": -66300, "FY2024": -77075, "FY2023": -59896, "FY2022": -25048, "FY2021": -19399,
        }),
        ("TOTAL", "Net interest income", {
            "FY2025": 104758, "FY2024": 110181, "FY2023": 95379, "FY2022": 83250, "FY2021": 62753,
        }),
        ("DATA", "Net fee and commission income", {
            "FY2025": 8281, "FY2024": 8245, "FY2023": 11223, "FY2022": 7659, "FY2021": 7880,
        }),
        ("DATA", "Foreign exchange gains/(losses)", {
            "FY2025": 6922, "FY2024": -3435, "FY2023": -5820, "FY2022": -3830, "FY2021": -1828,
        }),
        ("DATA", "Losses on derecognition of financial assets at amortised cost", {
            "FY2025": -351, "FY2024": -35, "FY2023": -747, "FY2022": -2509,
        }),
        ("DATA", "Net (losses)/gains on financial assets at FVOCI", {
            "FY2025": -3, "FY2024": 278,
        }),
        ("DATA", "Net gains on financial assets at FVTPL", {
            "FY2025": 4478, "FY2024": 3469, "FY2023": 3136, "FY2022": 3194,
        }),
        ("DATA", "Investment income", {
            "FY2025": None, "FY2024": None, "FY2021": 4326,
            # only a separate line in FY2021's report structure - later years fold this into the FVOCI/FVTPL lines above
        }),
        ("DATA", "Other operating income", {
            "FY2025": 3364, "FY2024": 3599, "FY2023": 5332, "FY2022": 2263, "FY2021": 2656,
        }),
        ("DATA", "Profit on sale of property and equipment", {
            "FY2023": 3,
        }),
        ("TOTAL", "Operating income", {
        "FY2025": 127450, "FY2024": 122301, "FY2023": 108507, "FY2022": 90026, "FY2021": 75787,
            "FY2020": 60905, "FY2019": 69228,
        }),
        ("SECTION", "Operating expenses", {}),
        ("DATA", "Personnel expenses", {
            "FY2025": -40361, "FY2024": -32903, "FY2023": -24913, "FY2022": -22716, "FY2021": -23216,
        }),
        ("DATA", "Depreciation and amortisation", {
            "FY2025": -1444, "FY2024": -2016, "FY2023": -2388, "FY2022": -2637, "FY2021": -3083,
        }),
        ("DATA", "Other operating expenses", {
            "FY2025": -26712, "FY2024": -25445, "FY2023": -23000, "FY2022": -15945, "FY2021": -11289,
        }),
        ("TOTAL", "Total operating expenses", {
        "FY2025": -68516, "FY2024": -60363, "FY2023": -50301, "FY2022": -41297, "FY2021": -37588,
            "FY2020": -28314, "FY2019": -31030,
        }),
        ("DATA", "Credit impairment charge/(reversal)", {
            "FY2025": -4749, "FY2024": -870, "FY2023": -10653, "FY2022": -1145, "FY2021": 1356,
        }),
        ("TOTAL", "Profit before taxation", {
        "FY2025": 54184, "FY2024": 61068, "FY2023": 47553, "FY2022": 47584, "FY2021": 39555,
            "FY2020": 14862, "FY2019": 32981,
        }),
        ("DATA", "Income tax (expense)/credit", {
        "FY2025": -13775, "FY2024": -15288, "FY2023": -11238, "FY2022": -1437, "FY2021": -1669,
            "FY2020": 1589, "FY2019": -5999,
        }),
        ("TOTAL", "Profit for the year", {
        "FY2025": 40409, "FY2024": 45781, "FY2023": 36315, "FY2022": 46146, "FY2021": 37886,
            "FY2020": 16451, "FY2019": 26981,
        }),
        ("SECTION", "Other comprehensive income", {}),
        ("DATA", "Net changes in fair value of debt securities at FVOCI", {
            "FY2025": -88, "FY2024": 92,
            # not disclosed for FY2023/FY2022/FY2021 - no OCI items reported those years
        }),
        ("DATA", "Tax effect of fair value changes", {
            "FY2025": 45, "FY2024": -23,
        }),
        ("TOTAL", "Other comprehensive income for the year", {
            "FY2025": -43, "FY2024": 69, "FY2023": 0, "FY2022": 0, "FY2021": 0,
        }),
        ("TOTAL", "Total comprehensive income for the year", {
            "FY2025": 40366, "FY2024": 45849, "FY2023": 36315, "FY2022": 46146, "FY2021": 37886,
        }),
    ],
    sources_text=STATEMENTS_SOURCES,
    first_col_width=72,
    source_height=340,
    unit_suffix=" ($'000, FY2021 conv. from £)",
)

EQUITY_HEADERS = [
    "Share capital", "Share premium", "Translation reserve",
    "Retained earnings / (Accumulated losses)", "Fair value reserve", "Total equity",
]

bw.add_equity_changes_sheet(
    title="FirstBank UK Limited — Statement of Changes in Equity",
    subtitle="$'000 throughout - FY2021 converted from £, see source note at bottom.",
    headers=EQUITY_HEADERS,
    rows=[
        ("TOTAL", "At 1 January 2021 (FY2020 closing, conv. from £ at FY2020 year-end spot rate)",
         (273220, 27936, None, -50497, None, 250659)),
        ("DATA", "Profit for the year (FY2021, conv. from £ at FY2021 average rate)",
         (None, None, None, 37886, None, 37886)),
        ("DATA", "Effect of GBP/USD translation (FY2021 - see source note; Total only, not allocated to a component)",
         (None, None, None, None, None, -3205)),
        ("TOTAL", "At 31 December 2021 (ties to Balance Sheet's own FY2021 Total equity)",
         (270420, 27650, None, -12730, None, 285340)),

        ("DATA", "FX translation-methodology bridge to the Bank's own restated $ opening (see source note)",
         (None, None, None, None, None, -443)),
        ("TOTAL", "At 1 January 2022 (restated, the Bank's own $ figure per its FY2023 Annual Report)",
         (270000, 27607, None, -12710, None, 284897)),
        ("DATA", "Translation impact on share capital and premium (FY2022 - redenomination of £200m nominal share capital to $242m, a real corporate action, not this project's FX conversion)",
         (-28000, -3380, 475, None, None, -30904)),
        ("TOTAL", "Total comprehensive income for the year (FY2022)",
         (None, None, None, 46146, None, 46146)),
        ("TOTAL", "At 31 December 2022",
         (242000, 24228, 475, 33436, None, 300139)),

        ("TOTAL", "Total comprehensive income for the year (FY2023)",
         (None, None, None, 36315, None, 36315)),
        ("TOTAL", "At 31 December 2023",
         (242000, 24228, 475, 69751, None, 336454)),

        ("DATA", "Profit for the year (FY2024)",
         (None, None, None, 45781, None, 45781)),
        ("DATA", "Net changes in fair value (FY2024)",
         (None, None, None, None, 69, 69)),
        ("TOTAL", "Total comprehensive income for the year (FY2024)",
         (None, None, None, 45781, 69, 45849)),
        ("TOTAL", "At 31 December 2024",
         (242000, 24228, 475, 115532, 69, 382303)),

        ("DATA", "Profit for the year (FY2025)",
         (None, None, None, 40409, None, 40409)),
        ("DATA", "Net changes in fair value (FY2025)",
         (None, None, None, None, 26, 26)),
        ("DATA", "Net reclassified gains to profit or loss (FY2025)",
         (None, None, None, None, -69, -69)),
        ("TOTAL", "Total comprehensive income for the year (FY2025)",
         (None, None, None, 40409, -43, 40366)),
        ("TOTAL", "At 31 December 2025 (ties to Balance Sheet's own FY2025 Total equity)",
         (242000, 24228, 475, 155941, 26, 422669)),
    ],
    sources_text=STATEMENTS_SOURCES,
    first_col_width=66,
    source_height=380,
)


def th(rows):
    """Rescale whole-dollar cash flow figures to $'000, matching this project's usual scale for a bank this
    size (see build_fidbank_uk.py's £'000 precedent for the same Nigerian-subsidiary FX-conversion pattern)."""
    out = []
    for kind, label, values in rows:
        scaled = {y: (round(v / 1000) if isinstance(v, (int, float)) else v) for y, v in values.items()}
        out.append((kind, label, scaled))
    return out


def th2(rows):
    """Same as th() but for the (label, values) pairs add_overview_sheet's cash_flow_totals expects."""
    out = []
    for label, values in rows:
        scaled = {y: (round(v / 1000) if isinstance(v, (int, float)) else v) for y, v in values.items()}
        out.append((label, scaled))
    return out


# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("DATA", "Profit for the year before taxation", {
        "FY2025": 54183785, "FY2024": 61068239, "FY2023": 47553062, "FY2022": 47583861,
        "FY2021": 39555278,
    }),
    ("SECTION", "Adjustment to reconcile profit to cash flow from operating activities", {}),
    ("DATA", "Depreciation of property and equipment", {
        "FY2025": 1234619, "FY2024": 1305257, "FY2023": 1553258, "FY2022": 1577263,
        "FY2021": 1869076,
    }),
    ("DATA", "Amortisation of intangible assets", {
        "FY2025": 209127, "FY2024": 710483, "FY2023": 834713, "FY2022": 1059948,
        "FY2021": 1214143,
    }),
    ("DATA", "Interest expenses on subordinated liability", {
        "FY2025": 5475000, "FY2024": 5490000, "FY2023": 5475000, "FY2022": 11863324,
        "FY2021": 5640848,
    }),
    ("DATA", "Net gains/(loss) from sale of investment securities", {
        "FY2025": 354336, "FY2024": -242362, "FY2023": 747336, "FY2022": 2509443,
        "FY2021": -407341,
    }),
    ("DATA", "Net gains on sale of financial assets at FVTPL", {
        "FY2025": -102818, "FY2024": -28597,
        # not a separate line in the FY2023 AR's own FY2023 column, or in the FY2022/FY2021-era format
    }),
    ("DATA", "Foreign currency revaluation (gains)/losses", {
        "FY2025": -6402369, "FY2024": 3201086, "FY2023": 5819509, "FY2022": 3830135,
        "FY2021": 1828225,
    }),
    ("DATA", "Credit impairment losses/(gains)", {
        "FY2025": 5279783, "FY2024": 1786453, "FY2023": 10652655, "FY2022": 1144902,
        "FY2021": -1356255,
    }),
    ("TOTAL", "Operating cash flow before changes in operating assets/liabilities", {
        "FY2025": 60231463, "FY2024": 73290559, "FY2023": 72635533, "FY2022": 69568876,
        "FY2021": 48343973,
    }),
    ("SECTION", "Net (increase)/decrease in assets relating to operating activities", {}),
    ("DATA", "Loans and advances to banks", {
        "FY2025": 66031212, "FY2024": 36160880, "FY2023": 22100735, "FY2022": -76514233,
        "FY2021": -253446737,
    }),
    ("DATA", "Loans and advances to customers", {
        "FY2025": -342954781, "FY2024": -74018980, "FY2023": -139867128, "FY2022": 105947878,
        "FY2021": 64373734,
    }),
    ("DATA", "Financial assets held at fair value through profit or loss", {
        "FY2025": -453774426, "FY2024": 3250178, "FY2023": -5642530, "FY2022": -12894565,
        "FY2021": 15583489,
    }),
    ("DATA", "Other assets", {
        "FY2025": -1391047, "FY2024": -29588, "FY2023": -851334, "FY2022": -159470,
        "FY2021": -342346,
    }),
    ("TOTAL", "Net (increase)/decrease in assets relating to operating activities", {
        "FY2025": -732089042, "FY2024": -34637510, "FY2023": -124260257, "FY2022": 16379610,
        "FY2021": -173831862,
    }),
    ("SECTION", "Net (decrease)/increase in liabilities relating to operating activities", {}),
    ("DATA", "Deposits from banks", {
        "FY2025": -729802922, "FY2024": 804463093, "FY2023": -1050768435, "FY2022": 101289192,
        "FY2021": 226547256,
    }),
    ("DATA", "Deposits from customers", {
        "FY2025": 612656527, "FY2024": -189309183, "FY2023": 41248076, "FY2022": 288002144,
        "FY2021": -17623266,
    }),
    ("DATA", "Other liabilities", {
        "FY2025": -11465920, "FY2024": 66945979, "FY2023": -41704800, "FY2022": -91730351,
        "FY2021": 42689697,
    }),
    ("DATA", "Financial liabilities at fair value through profit or loss", {
        "FY2025": 3774572, "FY2024": -17087478, "FY2023": -17047705, "FY2022": 6824115,
        "FY2021": 17704719,
    }),
    ("DATA", "Income taxes paid", {
        "FY2025": -6545402, "FY2024": -8679449, "FY2023": -5819386, "FY2022": -2567718,
        "FY2021": -2032427,
    }),
    ("TOTAL", "Net (decrease)/increase in liabilities relating to operating activities", {
        "FY2025": -131383145, "FY2024": 656332962, "FY2023": -1074092250, "FY2022": 301817382,
        "FY2021": 267285979,
    }),
    ("TOTAL", "Net cashflow from/(used in) operating activities", {
        # not an explicit line item in the FY2023 AR (own FY2023 column) or FY2022/FY2021-era reports -
        # left blank rather than a figure this project computed itself; see the three subtotals above.
        "FY2025": -803240724, "FY2024": 694986011,
    }),
    ("SECTION", "Cash flows from/(used in) investing activities", {}),
    ("DATA", "Acquisition of property, plant and equipment", {
        "FY2025": -52523, "FY2024": -123689, "FY2023": -186105, "FY2022": -86580,
        "FY2021": -147944,
    }),
    ("DATA", "Acquisition of intangible assets", {
        "FY2025": -24776, "FY2024": -5653, "FY2023": -175283, "FY2022": -379395,
        "FY2021": -213771,
    }),
    ("DATA", "Proceeds from sale/maturity of investment securities", {
        "FY2025": 2625720668, "FY2024": 2958772741,
    }),
    ("DATA", "Purchase of investment securities", {
        "FY2025": -1744047207, "FY2024": -3780168736,
    }),
    ("DATA", "Proceeds from/(purchase of) financial investments at amortised cost", {
        "FY2023": 1105994751, "FY2022": -131164090, "FY2021": -388494432,
    }),
    ("DATA", "Proceeds from sale of property and equipment", {
        "FY2023": 3171,
    }),
    ("TOTAL", "Net cash from/(used in) investing activities", {
        "FY2025": 881596162, "FY2024": -821525337, "FY2023": 1105636534, "FY2022": -131630065,
        "FY2021": -388856147,
    }),
    ("SECTION", "Cash flows used in financing activities", {}),
    ("DATA", "Interest paid on subordinated liability", {
        "FY2025": -5460000, "FY2024": -5505000, "FY2023": -5475000, "FY2022": -5459692,
        "FY2021": -4809745,
    }),
    ("DATA", "Principal element of lease payment", {
        "FY2025": -1313025, "FY2024": -931173, "FY2023": -1253403, "FY2022": -1225171,
        "FY2021": -1721371,
    }),
    ("TOTAL", "Net cash used in financing activities", {
        "FY2025": -6773025, "FY2024": -6436173, "FY2023": -6728403, "FY2022": -6684863,
        "FY2021": -6531116,
    }),
    ("TOTAL", "Net increase/(decrease) in cash and cash equivalents", {
        "FY2025": 71582413, "FY2024": -132975499, "FY2023": -26808842, "FY2022": 249450940,
        "FY2021": -253589172,
    }),
    ("DATA", "Cash and cash equivalents at the beginning of the year", {
        "FY2025": 362737524, "FY2024": 495730749, "FY2023": 522342258, "FY2022": 274093095,
        "FY2021": 621026011,
    }),
    ("DATA", "Exchange difference", {
        "FY2025": 520174, "FY2024": -17726, "FY2023": 197332, "FY2022": -1201776,
    }),
    ("DATA", "Effect of GBP/USD translation (FY2021 only - see currency note)", {
        "FY2021": -2104691,
    }),
    ("TOTAL", "Cash and cash equivalents at the end of the year", {
        "FY2025": 434840111, "FY2024": 362737524, "FY2023": 495730748, "FY2022": 522342259,
        "FY2021": 365332148,
    }),
]

bw.add_cash_flow_sheet(
    title="FirstBank UK Limited — Statement of Cash Flows",
    subtitle="Consolidated basis, as filed at Companies House ($ throughout - FY2021 converted from £, see source note)",
    rows=th(rows),
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=76,
    source_height=220,
    unit_suffix=" ($'000, FY2021 conv. from £)",
)

ASSET_QUALITY_SOURCES = (
    "Sources - FirstBank UK Limited's own Note 16 'Loans and advances to customers' impairment allowance "
    "disclosure (page images, statutory accounts filed at Companies House):\n"
    f"FY2025/FY2024: Annual Report and Financial Statements 2025, p.83-84 (full IFRS 9 Stage 1/2/3 gross "
    f"carrying amount table, $) - {AR2025_URL}\n"
    f"FY2023/FY2022 (restated): Annual Report and Financial Statements 2023, p.68 (12-month/Lifetime ECL "
    f"allowance split and Corporate/Individual composition only - no full Stage 1/2/3 gross table disclosed "
    f"this vintage, $) - {AR2023_URL}\n"
    f"FY2021 (as FBN Bank (UK) Limited, £ as originally reported, converted to $ at the FY2021 year-end spot "
    f"rate per the Balance Sheet sheet's source note): Annual Report and Financial Statements 2021, p.61 "
    f"(full IFRS 9 Stage 1/2/3 gross carrying amount table, £) - {AR2021_URL}\n\n"
    "GRANULARITY NOTE: the Bank's own disclosed granularity genuinely changes across this series - "
    "FY2025/FY2024 and FY2021 disclose a full Stage 1/2/3 gross-carrying-amount/loss-allowance/net table; "
    "FY2023/FY2022 disclose only the 12-month ECL vs Lifetime ECL allowance split (no Stage 1/2/3 gross "
    "breakdown for the loan book itself that vintage) - each year shown on its own actually-disclosed basis, "
    "not blended or estimated to fill the gap.\n"
    + CURRENCY_NOTE
)

bw.add_asset_quality_sheet(
    title="FirstBank UK Limited — Asset Quality",
    subtitle="Loans and advances to customers, by IFRS 9 stage. $'000 throughout - FY2021 conv. from £. See source note at bottom.",
    rows=[
        ("SECTION", "Gross carrying amount by IFRS 9 stage", {}),
        ("DATA", "Stage 1 (12-month ECL)", {
            "FY2025": 908653, "FY2024": 586279, "FY2021": 550279,
        }),
        ("DATA", "Stage 2 (Lifetime ECL, not credit-impaired)", {
            "FY2025": 25017, "FY2024": 2512, "FY2021": 2002,
        }),
        ("DATA", "Stage 3 / Default (Lifetime ECL, credit-impaired)", {
            "FY2025": 26187, "FY2024": 27797, "FY2021": 32507,
        }),
        ("DATA", "Gross carrying amount (Corporate + Individual, FY2023/FY2022 - no Stage 1/2/3 split disclosed)", {
            "FY2023": 543982, "FY2022": 404298,
        }),
        ("TOTAL", "Total gross carrying amount", {
            "FY2025": 959857, "FY2024": 616589, "FY2023": 543982, "FY2022": 404298, "FY2021": 584788,
        }),
        ("SECTION", "Loss allowance", {}),
        ("DATA", "Stage 1 loss allowance", {
            "FY2025": -11165, "FY2024": -7004, "FY2021": -3704,
        }),
        ("DATA", "Stage 2 loss allowance", {
            "FY2025": -1131, "FY2024": -77, "FY2021": -63,
        }),
        ("DATA", "Stage 3 loss allowance", {
            "FY2025": -8552, "FY2024": -8329, "FY2021": -12477,
        }),
        ("DATA", "12-month ECL allowance (FY2023/FY2022 - no Stage 1/2/3 split disclosed)", {
            "FY2023": -6621, "FY2022": -2999,
        }),
        ("DATA", "Lifetime ECL allowance (FY2023/FY2022 - no Stage 1/2/3 split disclosed)", {
            "FY2023": -7414, "FY2022": -567,
        }),
        ("TOTAL", "Total loss allowance", {
            "FY2025": -20848, "FY2024": -15410, "FY2023": -14035, "FY2022": -3566, "FY2021": -16244,
        }),
        ("TOTAL", "Net loans and advances to customers", {
            "FY2025": 939009, "FY2024": 601178, "FY2023": 529947, "FY2022": 400733, "FY2021": 568544,
        }),
        ("SECTION", "Composition and non-performing accounts", {}),
        ("DATA", "Corporate", {
            "FY2025": 757997, "FY2024": 466491, "FY2023": 390231, "FY2022": 279069,
        }),
        ("DATA", "Individual", {
            "FY2025": 201860, "FY2024": 150098, "FY2023": 153751, "FY2022": 125229,
        }),
        ("DATA", "Non-performing accounts (within maturity analysis)", {
            "FY2025": 26187, "FY2024": 27797, "FY2023": 22645, "FY2022": 5397, "FY2021": 32507,
        }),
        ("DATA", "Stage 3 / non-performing coverage ratio (loss allowance / non-performing accounts)", {
            "FY2025": "32.66%", "FY2024": "29.96%", "FY2021": "38.38%",
        }),
    ],
    sources_text=ASSET_QUALITY_SOURCES,
    first_col_width=78,
    source_height=280,
    unit_suffix=" ($'000, FY2021 conv. from £)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, f"{unit}" if unit else None,
                         rows_data, sources_text, note=note, first_col_width=44, source_height=140)


# ---------------------------------------------------------------
# KM1 Key Metrics - the Bank's own UK KM1 template, reproduced whole
# ---------------------------------------------------------------
KM1_NOTE = (
    "\n\nKM1 KEY METRICS SHEET - WHAT THIS IS AND HOW IT WAS BUILT\n"
    "This is the Bank's own UK KM1 key-metrics template, with the Bank's own row numbers, reproduced from "
    "each year's OWN edition rather than from a later edition's comparative column.\n"
    "\n"
    "THE TABLE IS SPLIT INTO TWO CURRENCY BLOCKS BECAUSE THE BANK CHANGED PRESENTATION CURRENCY, and the "
    "two blocks are NOT merged into one row. FY2024 and FY2023 were published in US dollars; FY2022, "
    "FY2021, FY2020 and FY2019 were published in pounds sterling. Converting either block onto the other's "
    "currency would be a computation, not a transcription, so each block is shown in the currency its own "
    "edition printed. The amounts are therefore NOT comparable across the two blocks, and the ratios - "
    "which are currency-free - are the only rows that run continuously from FY2024 to FY2019. Note that "
    "the Bank itself restated FY2022 into dollars as the FY2023 edition's comparative; that restatement is "
    "not used here, because FY2022's own edition is the sterling one.\n"
    "\n"
    "THE BANK'S ROW NUMBERING IS SHIFTED AGAINST THE PUBLISHED TEMPLATE, AND IS REPRODUCED AS PRINTED. In "
    "the UK KM1 template, row 1 is 'Common Equity Tier 1 (CET1) capital'. This Bank prints row 1 as 'Common "
    "Equity Tier 1 (CET1) capital: Instruments and reserves' - a larger, pre-deduction figure - and prints "
    "the actual CET1 capital figure on row 2, with no separate Tier 1 capital row at all. The CET1 Capital "
    "metric sheet in this workbook correctly carries the row-2 figure (FY2024: 363,763), so an automated "
    "cross-check that maps template row 1 to the CET1 Capital sheet will report a disagreement against this "
    "sheet's row 1 (FY2024: 382,235). That disagreement is expected and is a property of the source's "
    "numbering, not an error in either transcription. The rows are NOT renumbered to make the check pass.\n"
    "\n"
    "ROW 12 IS LABELLED '(%)' BUT PRINTS AN AMOUNT in every edition (FY2024: 129,093; FY2022: 57,670). The "
    "mislabelling is the Bank's own and is reproduced rather than corrected; the values are amounts in the "
    "block's currency.\n"
    "\n"
    "FY2023 LEVERAGE RATIO DIVERGES BETWEEN EDITIONS AND BOTH FIGURES ARE CORRECT AS PUBLISHED. The FY2023 "
    "edition prints a 19.75% leverage ratio on a total exposure measure of 1,567,144. The FY2024 edition "
    "restates the same year to 19.64% on an exposure measure of 1,575,739. This sheet carries the FY2023 "
    "edition's own 19.75%, because each year comes from its own edition; the Leverage Ratio metric sheet "
    "carries the later restated 19.64%. The cross-check will flag this. It is a genuine cross-edition "
    "restatement - corroborated by the exposure measure moving in the same edition - and is documented here "
    "rather than silenced by editing either figure.\n"
    "\n"
    "ROW-SET DRIFT. Rows UK 14a-UK 14f (additional own funds requirements to address the risk of excessive "
    "leverage) appear only in the FY2021 edition, where they are printed as 0.00% for every year that "
    "edition covers. They are absent from the FY2022, FY2023 and FY2024 editions and are left blank for "
    "those years rather than carried forward as zeros.\n"
    "\n"
    "DEFECTIVE NSFR BLOCK IN THE FY2021 EDITION. That edition's Net Stable Funding Ratio section does not "
    "print rows 18, 19 and 20 at all: it repeats the labels of rows 15, UK 16a and UK 16b with no values "
    "beneath them. The CRR2 NSFR rules commenced on 1 January 2022 and the Bank's own FY2022 edition states "
    "that prior periods are not available on a comparable basis, so FY2021 and earlier NSFR rows are blank. "
    "The duplicated labels are recorded as a source defect and are not reproduced as rows.\n"
    "\n"
    "FY2025 IS BLANK. No FY2025 Pillar 3 disclosure has been published, and the FY2025 Annual Report "
    "contains no key-metrics table - confirmed by reading its full text layer, not by a failed search."
)

km1_rows = [
    ("SECTION", "US DOLLAR BLOCK — FY2024 and FY2023, as published by the Bank in US dollars", {}),
    ("SECTION", "Available own funds (amounts)", {}),
    ("DATA", "1  Common Equity Tier 1 (CET1) capital: Instruments and reserves ($'000)",
     {"FY2024": 382235, "FY2023": 336454}),
    ("DATA", "2  Common Equity Tier 1 (CET1) capital ($'000)", {"FY2024": 363763, "FY2023": 309460}),
    ("DATA", "3  Total capital (TC = T1 + T2) ($'000)", {"FY2024": 414074, "FY2023": 353999}),
    ("SECTION", "Risk-Weighted exposure amounts", {}),
    ("DATA", "4  Total risk-weighted exposure amounts ($'000)", {"FY2024": 1395598, "FY2023": 1235478}),
    ("SECTION", "Capital ratios (as a percentage of risk-weighted exposure amount)", {}),
    ("DATA", "5  Common Equity Tier 1 ratio (%)", {"FY2024": "26.07%", "FY2023": "25.05%"}),
    ("DATA", "6  Tier 1 ratio (%)", {"FY2024": "26.07%", "FY2023": "25.05%"}),
    ("DATA", "7  Total capital ratio (%)", {"FY2024": "29.67%", "FY2023": "28.65%"}),
    ("SECTION", "Additional own funds requirements based on SREP (as a percentage of risk-weighted exposure amount)", {}),
    ("DATA", "UK 7a  Additional CET1 SREP requirements (%)", {"FY2024": "4.82%", "FY2023": "4.82%"}),
    ("DATA", "UK 7c  Additional T2 SREP requirements (%)", {"FY2024": "1.61%", "FY2023": "1.61%"}),
    ("DATA", "UK 7d  Total SREP own funds requirements (%)", {"FY2024": "14.42%", "FY2023": "14.42%"}),
    ("SECTION", "Combined buffer requirement (as a percentage of risk-weighted exposure amount)", {}),
    ("DATA", "8  of which: capital conservation buffer", {"FY2024": "2.50%", "FY2023": "2.50%"}),
    ("DATA", "9  Institution specific countercyclical capital buffer (%)", {"FY2024": "0.14%", "FY2023": "0.09%"}),
    ("DATA", "11  Combined buffer requirement (%)", {"FY2024": "2.64%", "FY2023": "2.59%"}),
    ("DATA", "UK 11a  Overall capital requirements (%)", {"FY2024": "17.06%", "FY2023": "17.01%"}),
    ("DATA", "12  CET1 available after meeting the total SREP own funds requirements (%) [prints an amount, $'000]",
     {"FY2024": 129093, "FY2023": 101715}),
    ("SECTION", "Leverage", {}),
    ("DATA", "13  Leverage ratio total exposure measure ($'000)", {"FY2024": 2575327, "FY2023": 1567144}),
    ("DATA", "14  Leverage ratio", {"FY2024": "14.12%", "FY2023": "19.75%"}),
    ("SECTION", "Liquidity Coverage Ratio", {}),
    ("DATA", "15  Total high-quality liquid assets (HQLA) (Weighted value -average) ($'000)",
     {"FY2024": 1400356, "FY2023": 1084674}),
    ("DATA", "UK 16a  Cash outflows - Total weighted value ($'000)", {"FY2024": 685809, "FY2023": 620176}),
    ("DATA", "UK 16b  Cash inflows - Total weighted value ($'000)", {"FY2024": 343498, "FY2023": 337095}),
    ("DATA", "16  Total net cash outflows (adjusted value) ($'000)", {"FY2024": 342311, "FY2023": 283081}),
    ("DATA", "17  Liquidity coverage ratio (%)", {"FY2024": "409.09%", "FY2023": "383.17%"}),
    ("SECTION", "Net Stable Funding Ratio", {}),
    ("DATA", "18  Total available stable funding ($'000)", {"FY2024": 1423612, "FY2023": 1506379}),
    ("DATA", "19  Total required stable funding ($'000)", {"FY2024": 669559, "FY2023": 526030}),
    ("DATA", "20  NSFR ratio (%)", {"FY2024": "213%", "FY2023": "286.37%"}),

    ("SECTION", "POUND STERLING BLOCK — FY2022 to FY2019, as published by the Bank in pounds sterling", {}),
    ("SECTION", "Available own funds (amounts) ", {}),
    ("DATA", "1  Common Equity Tier 1 (CET1) capital: Instruments and reserves (£'000)",
     {"FY2022": 247363, "FY2021": 211035, "FY2020": 183485, "FY2019": 167034}),
    ("DATA", "2  Common Equity Tier 1 (CET1) capital (£'000)",
     {"FY2022": 229026, "FY2021": 201907, "FY2020": 181579, "FY2019": 172577}),
    ("DATA", "3  Total capital (TC = T1 + T2) (£'000)",
     {"FY2022": 265764, "FY2021": 241216, "FY2020": 216165, "FY2019": 205132}),
    ("SECTION", "Risk-Weighted exposure amounts ", {}),
    ("DATA", "4  Total risk-weighted exposure amounts (£'000)",
     {"FY2022": 1019070, "FY2021": 1135077, "FY2020": 898917, "FY2019": 885249}),
    ("SECTION", "Capital ratios (as a percentage of risk-weighted exposure amount) ", {}),
    ("DATA", "5  Common Equity Tier 1 ratio (%) ",
     {"FY2022": "22.47%", "FY2021": "17.79%", "FY2020": "20.20%", "FY2019": "19.49%"}),
    ("DATA", "6  Tier 1 ratio (%) ",
     {"FY2022": "22.47%", "FY2021": "17.79%", "FY2020": "20.20%", "FY2019": "19.49%"}),
    ("DATA", "7  Total capital ratio (%) ",
     {"FY2022": "26.08%", "FY2021": "21.25%", "FY2020": "24.05%", "FY2019": "23.17%"}),
    ("SECTION", "Additional own funds requirements based on SREP (as a percentage of risk-weighted exposure amount) ", {}),
    ("DATA", "UK 7a  Additional CET1 SREP requirements (%) ",
     {"FY2022": "4.82%", "FY2021": "4.39%", "FY2020": "5.54%", "FY2019": "5.03%"}),
    ("DATA", "UK 7c  Additional T2 SREP requirements (%) ",
     {"FY2022": "1.61%", "FY2021": "1.46%", "FY2020": "1.85%", "FY2019": "1.68%"}),
    ("DATA", "UK 7d  Total SREP own funds requirements (%) ",
     {"FY2022": "14.42%", "FY2021": "13.85%", "FY2020": "15.39%", "FY2019": "14.71%"}),
    ("SECTION", "Combined buffer requirement (as a percentage of risk-weighted exposure amount) ", {}),
    ("DATA", "8  of which: capital conservation buffer ",
     {"FY2022": "2.50%", "FY2021": "2.50%", "FY2020": "2.50%", "FY2019": "2.50%"}),
    ("DATA", "9  Institution specific countercyclical capital buffer (%) ",
     {"FY2022": "0.05%", "FY2021": "0.00%", "FY2020": "0.00%", "FY2019": "0.06%"}),
    ("DATA", "11  Combined buffer requirement (%) ",
     {"FY2022": "2.55%", "FY2021": "2.50%", "FY2020": "2.50%", "FY2019": "2.56%"}),
    ("DATA", "UK 11a  Overall capital requirements (%) ",
     {"FY2022": "16.97%", "FY2021": "16.35%", "FY2020": "17.89%", "FY2019": "17.27%"}),
    ("DATA", "12  CET1 available after meeting the total SREP own funds requirements (%) [prints an amount, £'000]",
     {"FY2022": 57670, "FY2021": 15875, "FY2020": 23886, "FY2019": 21797}),
    ("SECTION", "Leverage ", {}),
    ("DATA", "13  Leverage ratio total exposure measure (£'000)",
     {"FY2022": 2327282, "FY2021": 2749530, "FY2020": 2444955, "FY2019": 2809165}),
    ("DATA", "14  Leverage ratio ",
     {"FY2022": "9.84%", "FY2021": "6.83%", "FY2020": "6.75%", "FY2019": "4.98%"}),
    ("SECTION", "Additional own funds requirements to address risks of excessive leverage (as a percentage of leverage ratio total exposure amount) — printed in the FY2021 edition only", {}),
    ("DATA", "UK 14a  Additional CET1 leverage ratio requirements (%)",
     {"FY2021": "0.00%", "FY2020": "0.00%", "FY2019": "0.00%"}),
    ("DATA", "UK 14b  Additional AT1 leverage ratio requirements (%)",
     {"FY2021": "0.00%", "FY2020": "0.00%", "FY2019": "0.00%"}),
    ("DATA", "UK 14c  Additional T2 leverage ratio requirements (%)",
     {"FY2021": "0.00%", "FY2020": "0.00%", "FY2019": "0.00%"}),
    ("DATA", "UK 14d  Total SREP leverage ratio requirements (%)",
     {"FY2021": "0.00%", "FY2020": "0.00%", "FY2019": "0.00%"}),
    ("DATA", "UK 14e  Applicable leverage buffer",
     {"FY2021": "0.00%", "FY2020": "0.00%", "FY2019": "0.00%"}),
    ("DATA", "UK 14f  Overall leverage ratio requirements (%)",
     {"FY2021": "0.00%", "FY2020": "0.00%", "FY2019": "0.00%"}),
    ("SECTION", "Liquidity Coverage Ratio ", {}),
    ("DATA", "15  Total high-quality liquid assets (HQLA) (Weighted value -average) (£'000)",
     {"FY2022": 1580997, "FY2021": 1198742, "FY2020": 1334462}),
    ("DATA", "UK 16a  Cash outflows - Total weighted value (£'000)",
     {"FY2022": 926814, "FY2021": 788438, "FY2020": 846608}),
    ("DATA", "UK 16b  Cash inflows - Total weighted value (£'000)",
     {"FY2022": 269843, "FY2021": 295280, "FY2020": 318660}),
    ("DATA", "16  Total net cash outflows (adjusted value) (£'000)",
     {"FY2022": 656972, "FY2021": 493157, "FY2020": 527948}),
    ("DATA", "17  Liquidity coverage ratio (%) ",
     {"FY2022": "240.65%", "FY2021": "243.08%", "FY2020": "252.76%"}),
    ("SECTION", "Net Stable Funding Ratio (FY2021 and earlier: the CRR2 NSFR rules commenced 1 January 2022 and no comparable prior figure is published)", {}),
    ("DATA", "18  Total available stable funding (£'000)", {"FY2022": 1089789}),
    ("DATA", "19  Total required stable funding (£'000)", {"FY2022": 396700}),
    ("DATA", "20  NSFR ratio (%) ", {"FY2022": "274.71%"}),
]

bw.add_km1_sheet(
    title="FirstBank UK Limited — KM1 Key Metrics",
    subtitle="The Bank's own UK KM1 key-metrics template (individual/solo basis), reproduced in its own row "
             "order, row numbers, labels and precision, each year from its own edition. THE TABLE IS IN TWO "
             "CURRENCY BLOCKS: FY2024-FY2023 as published in US dollars, FY2022-FY2019 as published in "
             "pounds sterling. Amounts are not comparable across the two blocks; the ratio rows are. FY2025 "
             "is blank - no Pillar 3 has been published for it. See the note for the Bank's own row-number "
             "shift, its '(%)'-labelled amount row, and the FY2023 leverage-ratio restatement.",
    rows=km1_rows,
    sources_text=p3_sources(page2024=3, page2023=3, page2022=19, page2021=9, table="Table 1 - Key Metrics") + (
        "\n\nKM1 key-metrics table by edition (printed folios, not PDF sheet indices): FY2024 = Pillar 3 "
        "Disclosures 31st December 2024, folio 3 ($'000). FY2023 = Pillar 3 Disclosures 31st December 2023, "
        "folio 3 ($'000). FY2022 = Pillar 3 Disclosures 31st December 2022, folio 19 (£'000). FY2021, "
        "FY2020 and FY2019 = Pillar 3 Disclosures 31st December 2021, folio 9 (£'000) - that edition prints "
        "a five-column table covering 2021, 2020, 2019, 2018 and 2017, and the three columns falling inside "
        "this workbook's year range are taken from it.\n"
        "LATEST-EDITION CHECK (2026-09-17): the Bank's website carries prose referring to a disclosures "
        "archive but no link behind it anywhere on the site, and its WordPress media API returns zero items "
        "even with no search filter - the API is disabled, which is an instrument failure and NOT evidence "
        "that documents are absent. The FY2025 Annual Report was retrieved and read in full; its text layer "
        "is rich (over 450,000 characters) and contains no key-metrics table. The newest Pillar 3 edition "
        "remains FY2024."
    ) + KM1_NOTE,
    first_col_width=84,
    source_height=900,
)

metric(
    "CET1 Capital", "$'000",
    [("Common Equity Tier 1 (CET1) capital", {
        "FY2025": 413015, "FY2024": 363763, "FY2023": 309460, "FY2022": 276585, "FY2021": 272998,
        "FY2020": 248055, "FY2019": 227974,
    })],
    p3_sources(page2024=3, page2023=3, page2022=19, table="Table 1 / Table 6"),
    note="CET1 capital equals Tier 1 capital for this Bank - it holds no Additional Tier 1 instruments (CET1 "
         "ratio and Tier 1 ratio are identical every year, see the Tier 1 Ratio and CET1 Ratio sheets).",
)

metric(
    "CET1 Ratio", "%",
    [("Common Equity Tier 1 (CET1) ratio", {
        "FY2025": "22.0%", "FY2024": "26.07%", "FY2023": "25.05%", "FY2022": "22.47%", "FY2021": "17.79%",
        "FY2020": "20.20%", "FY2019": "19.49%",
    })],
    p3_sources(page2024=3, page2023=3, page2022=19, table="Table 1 / Table 6"),
)

metric(
    "Tier 1 Capital", "$'000",
    [("Tier 1 capital", {
        "FY2025": 413015, "FY2024": 363763, "FY2023": 309460, "FY2022": 276585, "FY2021": 272998,
        "FY2020": 248055, "FY2019": 227974,
    })],
    p3_sources(page2024=3, page2023=3, page2022=19, table="Table 1 / Table 6"),
    note="Tier 1 capital equals CET1 capital for this Bank - it holds no Additional Tier 1 instruments.",
)

metric(
    "Tier 1 Ratio", "%",
    [("Tier 1 ratio", {
        "FY2024": "26.07%", "FY2023": "25.05%", "FY2022": "22.47%", "FY2021": "17.79%",
        "FY2020": "20.20%", "FY2019": "19.49%",
    })],
    p3_sources(page2024=3, page2023=3, page2022=19, table="Table 1 / Table 6"),
)

metric(
    "Total Capital", "$'000",
    [("Total capital (TC = T1 + T2)", {
        "FY2025": 451591, "FY2024": 414074, "FY2023": 353999, "FY2022": 320951, "FY2021": 326148,
        "FY2020": 295303, "FY2019": 270979,
    })],
    p3_sources(page2024=3, page2023=3, page2022=19, table="Table 1 / Table 6"),
)

metric(
    "Total Capital Ratio", "%",
    [("Total capital ratio", {
        "FY2025": "24.0%", "FY2024": "29.67%", "FY2023": "28.65%", "FY2022": "26.08%", "FY2021": "21.25%",
        "FY2020": "24.05%", "FY2019": "23.17%",
    })],
    p3_sources(page2024=3, page2023=3, page2022=19, table="Table 1 / Table 6"),
)

metric(
    "Total RWAs", "$'000",
    [("Total risk-weighted exposure amounts", {
        "FY2025": 1879000, "FY2024": 1395598, "FY2023": 1235478, "FY2022": 1230686, "FY2021": 1534738,
        "FY2020": 1228011, "FY2019": 1169414,
    })],
    p3_sources(page2024=3, page2023=3, page2022=19, table="Table 1 / Table 6"),
    note="PRECISION NOTE - FY2025 is the one year here that is NOT exact to the nearest $'000. Every other "
         "year comes from a Pillar 3 KM1 table stated in $'000; FY2025 has no Pillar 3 report and its only "
         "published RWA figure is the Strategic Report's 'Risk Weighted Assets $1,879mn', rounded to the "
         "nearest $ million, shown here as $1,879,000k. Treat the last three digits as rounding, not precision. "
         "The rounding is corroborated by the same table's own ratios: $413,015k/$1,879,000k = 21.98% against a "
         "printed CET 1 Ratio of 22.0%, and $451,591k/$1,879,000k = 24.03% against a printed Total Capital "
         "Adequacy Ratio of 24.0%.\n"
         "FY2022 corrected to $1,230,686k (2026-09-03 follow-up): the Bank's FY2023 Pillar 3 Disclosures "
         "Table 1 (KM1) shows FY2022's own restated $ Total risk-weighted exposure amount as $1,230,686k, "
         "confirmed identical to Table 3 (OV1)'s FY2022 comparative in the same document - this workbook "
         "previously carried $1,019,070, which is actually the Bank's own as-originally-reported £'000 FY2022 "
         "figure from the earlier 31 Dec 2022 Pillar 3 Disclosures' own KM1 table (Table 6), mislabelled as $.",
)

RWA_BREAKDOWN_SOURCES = (
    "Sources - FirstBank UK Limited Pillar 3 Disclosures, category-level RWA breakdown (all solo/individual "
    "basis throughout - the Bank discloses Pillar 3 on an individual basis only, per its own 'solo basis'/"
    "'individual basis' wording in every dated report below):\n"
    f"FY2024/FY2023: Pillar 3 Disclosures, 31st December 2024, p.5 (Table 2, $) - {P3_2024_URL}\n"
    f"FY2023/FY2022 (2026-09-12 CORRECTION - a real FY2022 category breakdown DOES exist; the prior 'genuinely "
    f"not disclosed' claim below was wrong): Pillar 3 Disclosures, 31st December 2023, Table 3 'OV1 Risk "
    f"Weighted Assets', p.5 (both the FY2023 own-year column and the FY2022 comparative column, both already "
    f"in $'000, the Bank's own restatement) - {P3_2023_URL} (live URL now 404s; re-fetched via Wayback Machine "
    "archive, snapshot 20240527034030). FY2022 column: Credit risk (excl. CCR) $967,989k, CCR $23,857k "
    "(standardised $23,857k, of which CVA $5,202k), Settlement risk $55k, Market risk $98,823k, Operational "
    "risk $134,759k, Total $1,230,686k - ties exactly to the Total RWAs sheet's existing FY2022 figure.\n\n"
    "(The earlier claim that the FY2022 Pillar 3 Disclosures document itself, as FBN Bank (UK) Limited, 31st "
    "December 2022, has no OV1 table was independently re-checked and is FALSE: that document's own Table 9 "
    "'UK OV1 - Overview of RWAs' (p.23, via Wayback Machine snapshot 20231206084043, the live URL also now "
    "404s) discloses the same FY2022 year natively in £'000: credit risk £801,544k, CCR £19,755k (of which CVA "
    "£4,308k), settlement risk £46k, market risk £81,831k, operational risk £111,587k, total £1,019,070k - a "
    "different total from the $1,230,686k figure above because this is the £-denominated table pre-dating the "
    "Bank's later $ restatement; not used here since the $ comparative in the FY2023 report is the more "
    "directly comparable, already-consistent-currency source, but this independently confirms a genuine OV1 "
    "category table did exist for FY2022 all along - it was simply not found by the earlier research pass.)\n\n"
    "FY2021 (2026-09-08 follow-up - found where the earlier pass missed it): Pillar 3 Disclosures (as FBN Bank "
    f"(UK) Limited), 31st December 2021, Table 9 'UK OV1 - Overview of RWAs' (own-year 2021 column, £'000) - "
    f"{P3_2021_URL} (via Wayback Machine archive - the live fbnbank.co.uk copy now 404s). This table's own "
    "Total (£1,137,015k) does not tie to this same document's own KM1 Key Metrics table (Table 6: £1,135,077k, "
    "the figure the Total RWAs sheet is built from) - a £1,938k / 0.17% discrepancy internal to the Bank's own "
    "FY2021 report between its two RWA tables. Both are the Bank's own genuine disclosures on the same solo "
    "basis; this workbook flags rather than resolves the mismatch. £ converted to $ at the FY2021 year-end "
    "spot rate (£1 = $1.3521, see CURRENCY NOTE); the DATA rows below sum to $1,537,358k, i.e. the $ "
    "equivalent of this table's own £1,137,015k Total, not the Total RWAs sheet's $1,534,738k.\n\n"
    "FY2020/FY2019 (2026-09-08 follow-up): each year's own dedicated Pillar 3 report, both found where the "
    "earlier pass missed them:\n"
    f"  FY2020: Pillar 3 Disclosures (as FBN Bank (UK) Limited), 31 December 2020, p.18, Table 11 'EU OV1 - "
    f"Overview of RWAs' (own-year 2020 column, £'000) - {P3_2020_URL} (via Wayback Machine archive). Converted "
    "to $ at the FY2020 year-end spot rate (£1 = $1.3661); DATA rows sum to $1,228,011k, matching the Total "
    "RWAs sheet's FY2020 figure exactly.\n"
    f"  FY2019: Pillar 3 Disclosures (as FBN Bank (UK) Limited), 31st December 2019, p.4, Table 1 'Analysis of "
    f"Pillar 1 Capital Requirement' (RWA column, £'000; this report predates the OV1 template and doesn't "
    f"split CCR out of credit risk - shown as one combined 'Credit risk (including CCR)' row) - "
    f"{P3_2019_URL} (via Wayback Machine archive). Converted to $ at the FY2019 year-end spot rate (£1 = "
    "$1.3210); DATA rows sum to $1,169,415k, matching the Total RWAs sheet's FY2019 figure of $1,169,414k "
    "within $1k rounding.\n\n"
    + P3_DEAD_URL_NOTE + "\n\n"
    + CURRENCY_NOTE
)

bw.add_rwa_breakdown_sheet(
    title="FirstBank UK Limited — RWA Breakdown",
    subtitle="Solo basis throughout, $'000. FY2019 combines CCR into credit risk (pre-OV1 template report); "
             "FY2021 carries a small flagged discrepancy vs the Total RWAs sheet (see source note). See source "
             "note at bottom.",
    rows=[
        ("SECTION", "UK OV1 template (FY2024-FY2021)", {}),
        ("DATA", "Credit risk (excluding CCR)", {
            "FY2024": 1196695, "FY2023": 1060740, "FY2022": 967989, "FY2021": 1293719,
        }),
        ("DATA", "Counterparty Credit Risk (CCR)", {
            "FY2024": 4007, "FY2023": 8023, "FY2022": 23857, "FY2021": 11788,
        }),
        ("DATA", "Of which CVA", {
            "FY2024": 611, "FY2023": 922, "FY2022": 5202, "FY2021": 1774,
        }),
        ("DATA", "Settlement risk", {
            "FY2024": 30, "FY2023": 2, "FY2022": 55, "FY2021": 14,
        }),
        ("DATA", "Market risk", {
            "FY2024": 4235, "FY2023": 9945, "FY2022": 98823, "FY2021": 80096,
        }),
        ("DATA", "Operational risk", {
            "FY2024": 190020, "FY2023": 155846, "FY2022": 134759, "FY2021": 149967,
        }),
        ("TOTAL", "Total RWAs", {
            "FY2024": 1395598, "FY2023": 1235478,
            "FY2022": 1230686,  # now category-broken-down - see FY2022 note below (2026-09-12 re-verification)
            "FY2021": 1537358,  # this table's own total - see source note re: discrepancy vs Total RWAs sheet
        }),
        ("SECTION", "Table 11 EU OV1 (FY2020)", {}),
        ("DATA", "Credit risk (excluding CCR)", {"FY2020": 1042450}),
        ("DATA", "Counterparty Credit Risk (CCR)", {"FY2020": 13681}),
        ("DATA", "Of which CVA", {"FY2020": 1921}),
        ("DATA", "Settlement risk", {"FY2020": 0}),
        ("DATA", "Market risk", {"FY2020": 18446}),
        ("DATA", "Operational risk", {"FY2020": 151513}),
        ("TOTAL", "Total RWAs", {"FY2020": 1228011}),
        ("SECTION", "Table 1 Analysis of Pillar 1 Capital Requirement (FY2019, pre-OV1 template)", {}),
        ("DATA", "Credit risk (including CCR)", {"FY2019": 1011400}),
        ("DATA", "Settlement risk", {"FY2019": 8}),
        ("DATA", "Market risk", {"FY2019": 14534}),
        ("DATA", "Operational risk", {"FY2019": 142881}),
        ("DATA", "Of which CVA", {"FY2019": 592}),
        ("TOTAL", "Total RWAs", {"FY2019": 1169415}),
    ],
    sources_text=RWA_BREAKDOWN_SOURCES,
    first_col_width=68,
    source_height=340,
    unit_suffix=" ($'000)",
)

metric(
    "Leverage Ratio", "%",
    [("Leverage ratio", {
        "FY2024": "14.12%", "FY2023": "19.64%", "FY2022": "9.84%", "FY2021": "6.83%",
        "FY2020": "6.75%", "FY2019": "4.98%",
    })],
    p3_sources(page2024=3, page2023=3, page2022=19, table="Table 1 / Table 6"),
)

metric(
    "LCR", "%",
    [("Liquidity Coverage Ratio (12-month trailing average)", {
        "FY2024": "409.09%", "FY2023": "383.17%", "FY2022": "240.65%", "FY2021": "243.08%",
        "FY2020": "252.76%",
    })],
    p3_sources(page2024=3, page2023=3, page2022=26, table="Table 1 / Table 6"),
)

metric(
    "NSFR", "%",
    [("Net Stable Funding Ratio", {
        "FY2024": "213%", "FY2023": "286.37%", "FY2022": "274.71%",
        # FY2021: not disclosed on a comparable basis - the CRR2 NSFR rules commenced 1 Jan 2022 and the
        # Bank's own Pillar 3 Dec-2022 report states prior-period data is "not available on an equivalent basis"
    })],
    p3_sources(page2024=3, page2023=3, page2022=26, table="Table 1 / Table 6"),
    note="FY2021 not disclosed: the CRR2 NSFR rules commenced 1 January 2022 and the Bank's own Pillar 3 "
         "Disclosures (Dec 2022) state prior-period NSFR data is 'not available on an equivalent basis'.",
)

metric(
    "MREL Ratio", None,
    [("Minimum Requirement for Own Funds and Eligible Liabilities (MREL) ratio", {
        y: "Not publicly disclosed" for y in bw.years
    })],
    "Sources - FirstBank UK Limited Pillar 3 Disclosures (31st December 2022, p.26) describes the Bank's MREL "
    "requirement qualitatively (set equal to its Pillar 1 + Pillar 2A capital requirements by the Bank of "
    "England as resolution authority under the BRRD) but does not disclose a quantitative MREL ratio figure in "
    f"any year's Pillar 3 Disclosures reviewed for this workbook - {P3_2022_URL}",
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {
            "FY2025": 3085183, "FY2024": 3174323, "FY2023": 2464043, "FY2022": 3492632, "FY2021": 3507813,
            "FY2020": 3237419, "FY2019": 3505179,
        }),
        ("Loans and advances to customers", {
            "FY2025": 939009, "FY2024": 601178, "FY2023": 529947, "FY2022": 400733, "FY2021": 568544,
            "FY2020": 650060, "FY2019": 609612,
        }),
        ("Deposits from customers", {
            "FY2025": 1672792, "FY2024": 1060135, "FY2023": 1249444, "FY2022": 1208196, "FY2021": 1030261,
            "FY2020": 1058435, "FY2019": 1003418,
        }),
        ("Total equity", {
            "FY2025": 422669, "FY2024": 382303, "FY2023": 336454, "FY2022": 300139, "FY2021": 285340,
            "FY2020": 250659, "FY2019": 220652,
        }),
    ],
    balance_sheet_unit="$'000",
    income_statement_totals=[
        ("Operating income", {
            "FY2025": 127450, "FY2024": 122301, "FY2023": 108507, "FY2022": 90026, "FY2021": 75787,
            "FY2020": 60905, "FY2019": 69228,
        }),
        ("Total operating expenses", {
            "FY2025": -68516, "FY2024": -60363, "FY2023": -50301, "FY2022": -41297, "FY2021": -37588,
            "FY2020": -28314, "FY2019": -31030,
        }),
        ("Profit for the year", {
            "FY2025": 40409, "FY2024": 45781, "FY2023": 36315, "FY2022": 46146, "FY2021": 37886,
            "FY2020": 16451, "FY2019": 26981,
        }),
    ],
    income_statement_unit="$'000",
    equity_changes_totals=[
        ("Opening equity", {
            "FY2025": 382303, "FY2024": 336454, "FY2023": 300139, "FY2022": 284897, "FY2021": 250659,
        }),
        ("Total comprehensive income for the year", {
            "FY2025": 40366, "FY2024": 45849, "FY2023": 36315, "FY2022": 46146, "FY2021": 37886,
        }),
        ("Other equity movements, net", {
            "FY2025": 0, "FY2024": 0, "FY2023": 0, "FY2022": -30904, "FY2021": -3205,
        }),
        ("Closing equity", {
            "FY2025": 422669, "FY2024": 382303, "FY2023": 336454, "FY2022": 300139, "FY2021": 285340,
        }),
    ],
    equity_changes_unit="$'000",
    cash_flow_totals=th2([
        ("Net cashflow from/(used in) operating activities", {
            "FY2025": -803240724, "FY2024": 694986011,
        }),
        ("Net cash from/(used in) investing activities", {
            "FY2025": 881596162, "FY2024": -821525337, "FY2023": 1105636534, "FY2022": -131630065,
            "FY2021": -388856147,
        }),
        ("Net cash used in financing activities", {
            "FY2025": -6773025, "FY2024": -6436173, "FY2023": -6728403, "FY2022": -6684863,
            "FY2021": -6531116,
        }),
        ("Cash and cash equivalents at end of year", {
            "FY2025": 434840111, "FY2024": 362737524, "FY2023": 495730748, "FY2022": 522342259,
            "FY2021": 365332148,
        }),
    ]),
    cash_flow_unit="$'000",
    ratios=[
        ("CET1 Ratio", {
            "FY2024": "26.07%", "FY2023": "25.05%", "FY2022": "22.47%", "FY2021": "17.79%",
        }),
        ("Tier 1 Ratio", {
            "FY2024": "26.07%", "FY2023": "25.05%", "FY2022": "22.47%", "FY2021": "17.79%",
        }),
        ("Total Capital Ratio", {
            "FY2024": "29.67%", "FY2023": "28.65%", "FY2022": "26.08%", "FY2021": "21.25%",
        }),
        ("Leverage Ratio", {
            "FY2024": "14.12%", "FY2023": "19.64%", "FY2022": "9.84%", "FY2021": "6.83%",
        }),
        ("LCR", {
            "FY2024": "409.09%", "FY2023": "383.17%", "FY2022": "240.65%", "FY2021": "243.08%",
        }),
        ("NSFR", {
            "FY2024": "213%", "FY2023": "286.37%", "FY2022": "274.71%",
        }),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own "
         "source citation for the underlying document/page. The Bank changed its presentation currency from "
         "GBP to USD in FY2023 - see the Cash Flow Statement sheet's currency note for how FY2021/FY2022 were "
         "put on a consistent $ basis here.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/FIRSTBANK UK FINANCIALS.xlsx")
