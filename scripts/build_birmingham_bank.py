import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first - only 5 years exist
YEAR_LABEL = {y: y for y in YEARS}

CH_URL = "https://find-and-update.company-information.service.gov.uk/company/00555071"
AR2025_URL = CH_URL + "/filing-history/MzU0NDA2NTQ1MWFkaXF6a2N4/document?format=pdf&download=0"
AR2024_URL = CH_URL + "/filing-history/MzQ2MDU0MTMzM2FkaXF6a2N4/document?format=pdf&download=0"
AR2023_URL = CH_URL + "/filing-history/MzQxNDU2Njk3NGFkaXF6a2N4/document?format=pdf&download=0"
AR2022_URL = CH_URL + "/filing-history/MzM5NzY1NjE1N2FkaXF6a2N4/document?format=pdf&download=0"
P3_URL = "https://www.birminghambank.com/hubfs/Birmingham%20Bank%202024%20Theme/PDFs/09i-Pillar-3-Disclosures-Report-as-at-140425.pdf"
# FY2022 Pillar 3, recovered 2026-09-15 via a Wayback CDX sweep of birminghambank.com.
# MUST be cited as the Wayback snapshot, NOT the bare live URL: the bank has since
# re-uploaded its FY2023 report OVER this filename, so the live
# .../wp-content/uploads/Birmingham-Bank-Pillar-3-Disclosures-2022-final.pdf returns
# HTTP 200 but serves the year-ended-31-December-2023 document. Verified 2026-09-15.
P3_2022_URL = (
    "https://web.archive.org/web/20240224223816id_/"
    "https://www.birminghambank.com/wp-content/uploads/Birmingham-Bank-Pillar-3-Disclosures-2022-final.pdf"
)
# FY2023 Pillar 3 - what that re-used filename currently serves.
P3_2023_URL = "https://www.birminghambank.com/wp-content/uploads/Birmingham-Bank-Pillar-3-Disclosures-2022-final.pdf"
SR2023_URL = AR2023_URL  # Strategic Report KPI table is in the same FY2023 Annual Report filing

ENTITY_NOTE = (
    "Entity note: company 00555071, formerly Hardware Federation Finance Company Limited (1955-1990), "
    "then Bira Finance Limited (2011-2013), then Bira Bank Limited (2013-2021), renamed Birmingham Bank "
    "Limited 26 Jan 2021 - same company throughout, FRN 204478 confirmed on the bank's own site footer, "
    "matching the bank list exactly. Four Companies House accounts filings exist (FY2022-FY2025, calendar "
    "year-end); there is no FY2021-specific standalone filing (the FY2022 filing's own FY2021 comparative "
    "column is the only source for FY2021). The Bank "
    "raised fresh capital (a GBP20m injection completing a change of control) in April 2023 and paused new "
    "lending for most of 2023 to build infrastructure - explains the large FY2023 capital-ratio jump.\n"
    "FY2025 ADDED 2026-09-18 (GA-003). Latest-edition check made against the Bank's own site and Companies "
    "House on 18 Sep 2026: the FY2025 full accounts (51pp, Board-approved 10 March 2026) were filed at "
    "Companies House on 14 SEPTEMBER 2026, four days before this check, and are the newest edition of any "
    "kind. PUBLICATION LAG, for the next session: the Bank approves its accounts in Feb/March and files "
    "them at Companies House between March and September (FY2023 filed 20 Mar 2024, FY2024 filed 31 Mar "
    "2025, FY2025 approved 10 Mar 2026 but not filed until 14 Sep 2026 - a six-month gap between signature "
    "and filing). A FY2026 edition should therefore not be looked for before about March 2027, and might "
    "not appear at Companies House until September 2027.\n"
    "THE FY2025 EDITION IS AN IMAGE-ONLY SCAN, exactly as the FY2024 one was: 51 pages with no text layer. "
    "Every FY2025 figure in this workbook was read from an OCR pass over that scan and then confirmed two "
    "ways - by arithmetic (each statement's own footings and cross-footings reproduce exactly: assets "
    "644,796; liabilities 580,892; equity 63,904; cash-flow subtotals -12,425 / 1,230 / -32,104 / 4,126; "
    "closing cash 15,289 = 14,686 + 603) and by eye against a 140-dpi render of the page. Where a FY2024 "
    "comparative in the FY2025 edition reproduces a figure this workbook already held from the FY2024 "
    "edition (LCR 725%, depreciation 32 + amortisation 205 = the 237 already on the Cash Flow sheet, "
    "interest payable 1,997, loss for the year 10,844, total equity 38,115), that agreement is itself an "
    "OCR control and is what establishes the reading is sound."
)

RESTATEMENT_NOTE = (
    "FY2024 IS RESTATED AND RE-CUT IN THE FY2025 EDITION, AND THIS WORKBOOK DOES NOT ADOPT THE RESTATEMENT. "
    "Each year's column is that year's OWN filing, this project's standing convention, so the FY2024 column "
    "below is still the FY2024 filing's own presentation. For the record, the FY2025 edition's FY2024 "
    "comparative column differs as follows: total assets 148,505 (this workbook: 151,081); total "
    "liabilities 110,390 (112,966); cash at bank / loans and advances to banks 11,163 (11,172); debt "
    "securities 42,937 (43,093); loans and advances to customers 88,635 (90,310); other assets 2,900 "
    "(3,617); prepayments 672 (691); customer deposits 108,309 (106,868); other liabilities 2,081 (6,098); "
    "gross loans 90,361 (90,352); total interest receivable 4,321 (4,436); administrative expenses 13,277 "
    "(13,155 plus 237 of depreciation and amortisation shown separately). Total equity (38,115), retained "
    "earnings (-24,885), share capital (60,138), share premium (2,862), loss for the year (-10,844) and "
    "the FY2024 capital ratio (76%, printed as 76.03% in the FY2025 Strategic Report) are unchanged "
    "between the two editions. What can be said from the documents alone is that it is a reclassification "
    "and not a correction touching equity: assets fall by GBP2,576k (717 + 156 + 1,675 + 9 + 19 across the "
    "five asset lines) and liabilities fall by the same GBP2,576k (other liabilities -4,017, customer "
    "deposits +1,441, the latter being the accrued deposit interest that the FY2025 edition's Note 20 says "
    "is now included within the deposit balance). No reason for the re-cut is given in either edition, and "
    "none is invented here."
)

STATEMENTS_SOURCES = (
    "Sources - Birmingham Bank Limited's own primary financial statements (FRS 102), all figures GBP'000:\n"
    f"FY2025: Full accounts made up to 31 Dec 2025 (Board-approved 10 Mar 2026, filed at Companies House 14 "
    f"Sep 2026, 51pp), Statement of Comprehensive Income p.28, Statement of Financial Position p.29, "
    f"Statement of Changes in Equity p.30, Statement of Cash Flows p.31 - {AR2025_URL}\n"
    f"FY2024: Full accounts made up to 31 Dec 2024 (filed 31 Mar 2025), Statement of Comprehensive Income "
    f"p.22, Statement of Financial Position p.23, Statement of Changes in Equity p.24 - {AR2024_URL}\n"
    f"FY2023: Full accounts made up to 31 Dec 2023 (filed 20 Mar 2024), same statements pp.22-24 - "
    f"{AR2023_URL}\n"
    f"FY2022 & FY2021: Amended full accounts made up to 31 Dec 2022 (filed 25 Oct 2023), Income Statement "
    f"p.25, Statement of Financial Position p.26, Statement of Changes in Equity p.27 - {AR2022_URL}. This "
    "filing reports in exact GBP (not GBP'000) with a FY2021 comparative column - both years converted to "
    "GBP'000 here (divided by 1,000, rounded) for consistency with the later filings' own units; no other "
    "conversion applied. Each year's own primary filing is used as that year's column (not a later filing's "
    "restated comparative), matching this project's standing convention.\n"
    + ENTITY_NOTE + "\n\n"
    + RESTATEMENT_NOTE + "\n\n"
    "LINE-BY-LINE MAPPING OF THE FY2025 EDITION ONTO THIS WORKBOOK'S ROWS. The FY2025 edition re-presents "
    "every statement, so the rule applied here is: where its line is the same item under a new name, the "
    "figure goes on the existing row and the rename is recorded; where its line has no counterpart in the "
    "earlier editions, it gets its own row, populated for FY2025 only; and a row the FY2025 edition dropped "
    "keeps its FY2021-FY2024 figures and is blank in the FY2025 column. Nothing is merged, summed or "
    "re-cut to make the two presentations agree. The cases are:\n"
    "  - 'Cash at Bank' (FY2021-FY2024) becomes 'Loans and advances to banks' (FY2025, GBP603k), and a new "
    "line 'Cash balances at central banks' (GBP14,686k) appears. Note 13 shows the two summing to "
    "GBP15,289k. The FY2022/FY2021 'Loans and advances to Banks' row is a DIFFERENT, third line those two "
    "editions printed alongside 'Cash at Bank' and is kept separate.\n"
    "  - 'Treasury Bills and similar securities' is called 'Investment in debt securities' from FY2025; "
    "same row, renamed here to carry both names.\n"
    "  - 'Derivative financial liability' (GBP1,210k) is new in FY2025. The FY2025 edition prints a DASH "
    "against it in its own FY2024 comparative column, but the FY2024 edition had no such line at all, so "
    "the FY2024 cell here is left blank rather than dashed.\n"
    "  - 'Derivative financial asset' is printed as a DASH by the FY2025 edition in its own FY2025 column "
    "and is carried as a literal '-', per this project's rule that a printed dash is the bank saying 'not "
    "applicable to us' and is a different statement from silence. (Consequence worth knowing: "
    "verify_workbook.py cannot reconcile a block containing a text cell, so the FY2025 Assets block is "
    "skipped by the automated check. It was reconciled by hand: 14,686 + 603 + 77,121 + 540,372 + 8,162 + "
    "508 + 95 + 3,249 = 644,796, the reported total exactly.)\n"
    "  - The P&L's 'Total income' TOTAL row is renamed 'Total interest receivable and similar income', "
    "which is what it has always held, because the FY2025 edition uses the words 'Total income' for a "
    "DIFFERENT subtotal (GBP5,872k, struck after interest payable, fees and derivative gains). That "
    "FY2025 subtotal is the same cut as the earlier editions' 'Net income', so the two share one row.\n"
    "  - The FY2025 edition prints no separate 'Depreciation and amortisation' expense line: Note 8 shows "
    "depreciation GBP19k and amortisation GBP470k inside administrative expenses of GBP15,184k. The D&A "
    "row is therefore blank for FY2025, and is NOT back-derived out of the admin figure.\n\n"
    "PRESENTATION NOTE: independently rounding each £'000 line (rather than rounding a pre-summed exact-£ "
    "total) occasionally leaves a component sum GBP1k off its own total row for FY2022/FY2021 (e.g. FY2022 "
    "Total assets: components sum to GBP17,058k vs the reported GBP17,059k) - both figures are shown exactly "
    "as each filing's own numbers round to; not forced to tie. No Additional Tier 1/Tier 2 capital is "
    "disclosed in any year. Off-balance-sheet items are disclosed from FY2024 onward in the commitments "
    "note only (FY2025: GBP32.1m of post-offer commitments to lend, FY2024: GBP45.5m) and are not carried "
    "as balance-sheet rows."
)

PL_NOTE = (
    "The 'Net (loss)/gain on financial instruments held at fair value through profit and loss' line only "
    "appears from FY2024 onward (GBP27k) - not disclosed as a separate line in FY2021-FY2023, where it did "
    "not exist or was immaterial/nil. The FY2025 edition renames it 'Net gain from derivatives and hedge "
    "accounting' (GBP211k) and its Note 7 splits that into hedge ineffectiveness GBP40k and gains on "
    "derivatives not in a hedging relationship GBP171k. (Source defect, reproduced not corrected: Note 22's "
    "hedge-effectiveness table prints the same ineffectiveness as GBP(39)k on the same basis, against Note "
    "7's +GBP40k. Neither figure is used on this sheet; both are recorded here.)\n\n"
    "FY2025 SUBTOTALS NOT CARRIED AS ROWS. The FY2025 edition strikes a 'Net interest income' subtotal of "
    "GBP5,782k (21,563 less 15,781), which no earlier edition printed. It is recorded here rather than "
    "given a row of its own, because a row holding one year in five would read as a four-year gap where "
    "there is none; the two figures it is struck from are both on this sheet. The Strategic Report's KPI "
    "table gives the same figure as 'Net interest income GBP5.8m (2024: GBP2.3m)'.\n\n"
    "FY2025 'Other comprehensive income' is shown as 0 on the authority of the FY2025 statement's own "
    "sentence 'There were no recognised gains or losses other than those reported above' - an explicit nil, "
    "not an assumed one. The edition prints the caption with no figure beneath it.\n\n"
    "CORRECTION (2026-09-06 audit): FY2022 Total income and Net income were previously shown as GBP758k and "
    "GBP668k - the FY2023 filing's own restated £'000 comparative column for FY2022 (itself component-rounded: "
    "530+228=758). The FY2022 filing's own primary Income Statement (exact GBP, this project's stated "
    "per-year sourcing convention) states Total income of GBP757,483 and Net income of GBP667,285, which "
    "round to GBP757k/GBP667k - now corrected to match. All other FY2022 P&L lines already matched the FY2022 "
    "filing exactly; only these two subtotals had drifted to the later filing's rounding. The downstream "
    "'Loss on ordinary activities before taxation' (GBP4,194k) is unaffected - it is each filing's own reported "
    "total, not a re-derived sum of the (rounded) lines above it, so it does not tie by simple subtraction to "
    "the corrected Net income figure; this is the same independent-rounding artifact already documented on "
    "the Balance Sheet sheet (a component sum landing GBP1k off its own total row)."
)

ASSET_QUALITY_NOTE = (
    "The Bank reports under FRS 102 (incurred-loss impairment model), not IFRS 9 - no Stage 1/2/3 or "
    "non-performing-loan split is disclosed in any year's Annual Report or in any Pillar 3 document "
    "published; only a single 'bad debt provisions' balance (with a separate 'general' provision component "
    "in FY2021, reduced to nil during 2021) and a maturity-band breakdown of the gross loan book. Coverage "
    "ratio shown is Bad debt provisions / Gross loans and advances to customers - a coverage proxy, not an "
    "NPL ratio, since no non-performing/past-due balance is disclosed. This remains true of the FY2025 "
    "edition, and was tested rather than assumed (OCR text of all 51 pages, 2026-09-18): 'Stage 1', 'Stage "
    "2', 'Stage 3', 'IFRS 9' and 'non-performing' return ZERO hits; 'forbearance' returns 2 and 'past due' "
    "1, all three inside the accounting-policy prose on impaired lending (p.36) and none of them "
    "attached to a balance. RICHNESS CONTROL: the same extraction returns 'provision' 52 times and "
    "'impairment' 47, so a zero here is a property of the document, not of the extraction.\n\n"
    "FY2025 - TWO SEPARATE MATURITY SECTIONS, BECAUSE THE BANK CHANGED THE TABLE. The FY2021-FY2024 "
    "editions each printed a maturity analysis of the GROSS loan book on four 'repayable' bands. The "
    "FY2025 edition drops that table and, in its Note 15, refers the reader instead to Note 29, which is a "
    "table of INTEREST-RATE RE-PRICING mismatches on NET carrying amounts across all balance-sheet lines. "
    "Those are different cuts of a different quantity, so they are shown as two sections rather than as "
    "one set of rows that silently changes basis at FY2025. FY2025's three bands (18 / 8,031 / 532,323) "
    "foot to the GBP540,372k net loans figure on the balance sheet; there is no 'repayable on demand' or "
    "'over 5 years' band in that table.\n\n"
    "FY2025 build-up of the loan book, as Note 15 prints it: gross loans 549,420, less an effective "
    "interest rate adjustment of 10,205 (= 539,215, the edition's own 'total gross loans after EIR "
    "adjustment'), less provision for impairment losses 292 (= 538,923, its 'total net loans'), plus a "
    "fair value adjustment for the hedged asset of 1,449 = 540,372. The two intermediate subtotals are "
    "recorded here rather than given TOTAL rows of their own, so that the one TOTAL row on this section "
    "means the same thing in every year. The coverage ratio is computed on the same definition as every "
    "other year - 292 / 549,420 = 0.053%, shown as 0.05% - i.e. against gross loans BEFORE the EIR "
    "adjustment.\n\n"
    "NOT CARRIED, AND WHY. The FY2025 edition's Note 15 adds two breakdowns of the gross mortgage book "
    "that no earlier edition published: by region (London GBP217,196k / 39.5% the largest of ten) and by "
    "loan-to-value band (GBP447,918k / 81.6% in the 70.01%-80% band, nothing above 90%). Both are printed "
    "with a FY2024 comparative, but this project sources each year from its OWN edition and the FY2024 "
    "edition is an image-only scan that has not been read for these tables, so carrying them would create "
    "rows populated for one year in five. They are recorded here instead. Both tables foot to GBP548,923k, "
    "which is neither the gross (549,420) nor the after-EIR (539,215) figure - a GBP497k difference the "
    "edition does not explain; reproduced as a fact about the source, not reconciled."
)

CASH_FLOW_SOURCES = (
    "Sources - Birmingham Bank Limited's own Statement of Cash Flows (FRS 102), all figures GBP'000:\n"
    f"FY2025: Full accounts made up to 31 Dec 2025 (Board-approved 10 Mar 2026, filed 14 Sep 2026), p.31 "
    f"(Statement of Cash Flows, presented as the first note) - {AR2025_URL}\n"
    f"FY2024: Full accounts made up to 31 Dec 2024 (filed 31 Mar 2025), p.25 (Statement of Cash Flows) - {AR2024_URL}\n"
    f"FY2023: Full accounts made up to 31 Dec 2023 (filed 20 Mar 2024), p.26 (Statement of Cash Flows) - {AR2023_URL}\n"
    f"FY2022 & FY2021: Amended full accounts made up to 31 Dec 2022 (filed 25 Oct 2023), p.28 (Statement of "
    f"Cash Flows) - {AR2022_URL}. This filing reports in exact GBP (not GBP'000) with a FY2021 comparative "
    "column - both years converted to GBP'000 here (divided by 1,000, rounded) for consistency with the "
    "later filings' own units; no other conversion applied.\n"
    + ENTITY_NOTE + "\n\n"
    "DATA NOTE: the FY2024 filing's own 'Analysis of the balances of cash' table mislabels its opening-balance "
    "column '01.01.2023' (should read 01.01.2024) - the VALUE (GBP3,866k) is used as printed, since it exactly "
    "matches FY2023's own reported closing balance; only the column label in the source appears to be a "
    "typo, not the figure. Separately, the FY2022 filing's own closing balance (GBP1,896k, rounded from the "
    "exact GBP1,895,707) differs by an immaterial GBP1k from FY2023's own filing's stated opening balance "
    "(GBP1,897k) for the same date - both are shown here exactly as each filing states them, not forced to "
    "match. FY2021's own opening cash balance is not available in any filing found (the FY2022 filing's "
    "comparative column starts from FY2021's closing balance only) - left blank, not estimated.\n\n"
    + RESTATEMENT_NOTE + "\n\n"
    "HOW THE FY2025 EDITION'S CASH FLOW STATEMENT MAPS ONTO THIS SHEET. The FY2025 edition re-presents the "
    "statement, and the two presentations strike their first subtotal in different places: the FY2021-"
    "FY2024 editions' 'Net cash outflow from trading activities' includes the movements in prepayments and "
    "in accruals, whereas the FY2025 edition's 'Total' (GBP(12,425)k) is struck BEFORE any working-capital "
    "movement and shows those two movements underneath, inside a 'Changes in operating assets and "
    "liabilities' block. The rows are ordered here so that BOTH bases foot in their own column without "
    "anything being re-derived: FY2025's prepayments (+164) and other liabilities (-74) movements sit on "
    "their own rows below the subtotal, and FY2025's non-cash adjustments sit above it. Every column of "
    "this sheet reconciles to its own edition's printed subtotal: FY2025 -9,211 + 250 + 19 + 470 - 211 - "
    "3,742 = -12,425, then -450,539 + 469,366 - 5,262 + 164 - 74 = +13,655 giving the printed +1,230.\n"
    "Renames and re-cuts, recorded rather than merged:\n"
    "  - The FY2025 edition prints 'Depreciation' (19) and 'Amortisation' (470) as two lines where earlier "
    "editions printed one combined 'Depreciation and amortisation' line. Both are carried as the source "
    "prints them; they are NOT summed onto the legacy row. Note 8 shows the same two figures inside "
    "administrative expenses. The FY2025 edition's FY2024 comparative for these two lines (32 + 205 = 237) "
    "reproduces this workbook's existing FY2024 combined figure exactly - which is one of the controls "
    "that establishes the OCR reading of this scan is sound.\n"
    "  - 'Fair value movement on derivatives' (FY2025, -211) is NOT the same row as 'Increase in derivative "
    "financial asset' (FY2024, -27): the FY2025 edition prints the FY2024 comparative of its own row as "
    "+27, the opposite sign. Kept as two rows.\n"
    "  - 'Interest income from debt securities' (-3,742) has no counterpart before FY2025: earlier editions "
    "did not strip accrued securities interest out of the operating reconciliation.\n"
    "  - Purchases and maturities of debt securities move from the operating section ('Decrease/(increase) "
    "in financial assets / treasury bills') to the INVESTING section in FY2025, where they are shown gross "
    "(-215,414 and +184,972). The legacy operating row is therefore blank for FY2025, and the investing "
    "block foots for both bases because the blank cells contribute nothing.\n"
    "  - 'Taxation - credit' is blank for FY2025: the FY2025 edition prints that line with a figure in the "
    "2024 column only and nothing in the 2025 column.\n"
    "FY2025 OPENING CASH. The FY2025 edition's 'Analysis of the balances of cash' opens at GBP11,163k where "
    "the FY2024 edition closed at GBP11,172k - the same GBP9k reclassification described in the "
    "restatement note above, and the same class of inter-edition difference already documented between "
    "FY2022 and FY2023. Both are shown exactly as each filing states them, not forced to match. Closing "
    "cash of GBP15,289k ties to the balance sheet as GBP14,686k at the Bank of England plus GBP603k at "
    "commercial banks (Note 13)."
)


P3_FY2025_NOTE = (
    "FY2025 - THERE IS NO FY2025 PILLAR 3 REPORT, AND THE FY2025 FIGURES ON THESE SHEETS COME FROM THE "
    "ANNUAL REPORT INSTEAD. Checked 18 Sep 2026 against the Bank's OWN site, three ways:\n"
    "  (a) The Bank's public footer - which appears on every page of birminghambank.com and is its only "
    "index of regulatory documents - carries exactly ONE 'Pillar 3' link, and it still resolves to the "
    "FY2024 report at the URL cited above. That URL was fetched on 18 Sep 2026 and verified live (HTTP "
    "200, Content-Type application/pdf, %PDF magic bytes, 1,049,830 bytes) and its cover page still reads "
    "'Pillar 3 Disclosures / For the year ended 31 December 2024' - i.e. the Bank has NOT overwritten it "
    "with a FY2025 edition, which matters because overwriting a Pillar 3 file in place is precisely what "
    "this Bank did in 2024 (see the citation trap below).\n"
    "  (b) RICHNESS CONTROL ON THAT INDEX: the same footer links documents version-stamped 14-07-2026 "
    "(cookie policy v2.2, website terms v2.4, tax strategy v2.2) and a third-party privacy policy dated "
    "July 2026. The page is therefore being maintained two months before this check, so 'one Pillar 3 "
    "link' is a fact about the Bank's publishing, not a stale page. (The site's own HubSpot search API "
    "indexes pages and blog posts only, not files, so it cannot answer this question either way - noted so "
    "that a later session does not mistake its empty result for evidence.)\n"
    "  (c) A Wayback CDX sweep of the whole birminghambank.com domain returns five Pillar 3 captures and "
    "no more: FY2020, FY2022, FY2023 (twice, under two paths) and FY2024. Direct probes of 29 plausible "
    "FY2025 filenames under the current hubfs folder, a 2026-themed folder and the legacy WordPress "
    "uploads path all returned HTTP 404 - with the known-good FY2024 URL run through the SAME probe as a "
    "reach control, returning 200/application/pdf/%PDF. That control proves the probe reaches the host; it "
    "does NOT prove the guessed names are what a FY2025 file would be called, so (c) is corroboration for "
    "(a) and (b) and is not load-bearing on its own.\n"
    "WHY NO FY2025 EDITION IS EXPECTED, AND WHY THAT IS NOT THE EVIDENCE. Birmingham Bank's SDDT Rule 3.1 "
    "modification by consent - the opt-in that removes the Pillar 3 disclosure duty - took effect 14 APRIL "
    "2026 (see the full register note below). The FY2024 report was published 'as at 14/04/25', so a "
    "FY2025 report would have been due around April 2026, the same month the duty fell away. A waiver "
    "removing a DUTY to disclose is not evidence that a bank DID NOT disclose, so the finding above rests "
    "on (a) and (b) - the Bank's own live index - and the waiver only explains it. Forward-looking: no "
    "FY2025 or FY2026 Pillar 3 should be expected, and a future session should not spend a session "
    "looking for one.\n"
    "WHAT THE FY2025 ANNUAL REPORT DOES AND DOES NOT GIVE. It gives the Capital Adequacy Ratio (30.43%, "
    "2024: 76.03%) twice - in the Strategic Report's KPI table, p.4, and again in the Capital Risk section, "
    "p.8 - and the Liquidity Coverage Ratio (460%, 2024: 725%) in the same KPI table. It states 'The Bank "
    "only has Common Equity Tier 1', so CET1 Ratio = Tier 1 Ratio = Total Capital Ratio = 30.43% for "
    "FY2025, as in every earlier year. It gives NO capital amount, NO risk-weighted assets, NO leverage "
    "ratio, NO NSFR and NO MREL figure, and those cells are marked 'Not publicly disclosed' for FY2025 "
    "rather than left blank. RICHNESS CONTROL on that negative (OCR text of all 51 pages, 2026-09-18): "
    "'risk weighted', 'risk-weighted', 'CET1', 'own funds', 'leverage', 'net stable', 'NSFR' and 'MREL' "
    "each return ZERO hits, in a document where 'capital adequacy' returns 5, 'liquidity coverage' 2 and "
    "'cash flow' 23. A bare search for 'RWA' returns 11 hits and every one of them is the letter sequence "
    "inside 'forward' or 'straightforward' - recorded because that is exactly the sort of false positive "
    "that would otherwise look like a disclosure.\n"
    "FY2024's 76% (this workbook, from the Pillar 3) against the FY2025 Annual Report's 76.03% for the "
    "same date is the Bank's own rounding in its own two documents, not a restatement; FY2024 keeps its "
    "own edition's figure, as every year on these sheets does.\n"
)


def p3_sources():
    return (
        "Sources - Birmingham Bank Limited Pillar 3 disclosures (Bank-solo basis):\n"
        + P3_FY2025_NOTE
        + f"FY2025 (capital ratios and LCR only): Full accounts made up to 31 Dec 2025, Strategic Report "
        f"KPI table p.4 and Capital Risk section p.8 - {AR2025_URL}\n"
        f"FY2024 & FY2023: Pillar 3 Disclosures Report as at 14 Apr 2025 (covers year ended 31 Dec 2024, "
        f"FY2023 comparative), Section 1.4 'Summary Analysis' (headline figures) and Section 5 (RWA/Pillar 1 "
        f"detail table) - {P3_URL}\n"
        f"FY2022 & FY2021 (capital amounts, capital ratios, leverage ratio): Pillar 3 Disclosures 'For the "
        f"year ended 31 December 2022', Section 1.4 summary table (Tier 1 capital, Risk Weighted assets, Tier "
        f"1 Capital ratio, Leverage ratio, Liquidity coverage ratio - both years side by side), Section 5.1 "
        f"'regulatory capital resources' table (CET1 build-up, both years) and Section 10 'Own Funds "
        f"Disclosure' table (FY2022) - {P3_2022_URL}\n"
        "ADDED 2026-09-15. This document was recovered via a Wayback CDX sweep and supersedes the previous "
        "statement that 'the bank's only Pillar 3 document covers FY2023-FY2024 only' - a second, earlier "
        "Pillar 3 report does exist and covers FY2022 with a full FY2021 comparative. MUST be cited at the "
        "Wayback snapshot above: the live URL bearing this filename now serves the FY2023 document (the Bank "
        "re-uploaded over it), so the bare URL would silently point at the wrong year. See the capital "
        "sheets' own CAPITAL_2022_NOTE for the full citation-trap warning and the ratio restatement.\n"
        f"FY2022 & FY2021 (superseded ratio source, retained for the record): the Strategic Report 'key "
        f"financial performance indicators' tables - Full accounts made up to 31 Dec 2023 (filed 20 Mar "
        f"2024) p.4 for FY2022 ({SR2023_URL}), and Amended full accounts made up to 31 Dec 2022 (filed 25 "
        f"Oct 2023) p.5 for FY2021 ({AR2022_URL}, disclosing 96.69%). These were the only source for these "
        "years before the FY2022 Pillar 3 report was recovered, and gave 91% (FY2022) and 97% (FY2021). The "
        "Pillar 3 report gives 90% and 96% on the same dates; its figures are now carried because they are "
        "internally consistent with the capital amounts and RWAs this workbook holds. The difference is a "
        "genuine source-basis difference between two of the Bank's own documents - documented, not resolved. "
        "The LCR cells (2,983% / 16,250%) are unaffected: both sources agree exactly.\n"
        "The Bank has no Additional Tier 1 or Tier 2 capital in any year (per the Pillar 3 report's own "
        "statement), so CET1 Capital = Tier 1 Capital = Total Capital, and CET1 Ratio = Tier 1 Ratio = Total "
        "Capital Ratio, throughout.\n"
        "SDDT - EXPLICIT NEGATIVE, recorded 2026-09-15 (cross-bank SDDT date-fit pass) so that a future pass "
        "does not wrongly apply the Small Domestic Deposit Taker exemption to this workbook's gap years. "
        "Birmingham Bank DOES hold the SDDT opt-in, but it is far too recent to explain anything here. The Bank "
        "of England consolidated list of waivers and modifications granted to PRA-authorised firms (downloaded "
        "2026-09-15, https://www.bankofengland.co.uk/-/media/boe/files/prudential-regulation/authorisations/"
        "waivers-and-modifications-of-rules/consolidated-waivers-pra-firms.csv) carries two SDDT rows for FRN "
        "204478, 'BIRMINGHAM BANK LIMITED': (a) 'Modification by Consent - PRA Rulebook - CRR Firms - Rule 3.1 "
        "of the SDDT Regime - General Application Part', sub rule 'Ru 3.1', waiver ref 'A00012036P.pdf', START "
        "DATE 14/04/2026, no end date; and (b) a modification of the criterion in rule 2.1(9) ('any parent "
        "undertaking of the firm is a UK undertaking'), sub rule 'Ru 2.1(9)', ref 'A0011828P.pdf', start "
        "16/03/2026, end 16/03/2029. Only row (a) is evidence of a disclosure exemption. Row (b) modifies an "
        "ELIGIBILITY CRITERION only - it is what let the Bank qualify despite its overseas ownership - and a "
        "firm holding only such a row is not a confirmed SDDT at all.\n"
        "DATE FIT - IT DOES NOT FIT. The Bank's accounting reference date is 31 DECEMBER, confirmed at Companies "
        "House (company 00555071, accounts filed to 31 December for 2019 through 2025). The outstanding gap "
        "years are FY2021 and FY2022, which ended 31 December 2021 and 31 December 2022. The Rule 3.1 "
        "modification began 14 APRIL 2026 - more than three years after the later of those two year-ends. A "
        "modification cannot explain a gap that predates it, so the SDDT regime explains NEITHER the FY2021 nor "
        "the FY2022 blanks.\n"
        "Those gaps keep an entirely separate explanation, though it is now much narrower than when this note "
        "was written: the FY2022 Pillar 3 report recovered on 2026-09-15 supplies capital amounts, capital "
        "ratios and the leverage ratio for BOTH FY2022 and FY2021, so those years are no longer "
        "Strategic-Report-only and are no longer materially blank. What remains genuinely unavailable for "
        "them is an RWA category breakdown reconciled to the restated basis, and NSFR. Either way this is a "
        "narrower-source gap, not a regulatory exemption. The register finding changes no cell in this "
        "workbook. Forward-looking only: from 14 April "
        "2026 the Bank is an SDDT, so no further Pillar 3 document should be expected for FY2026 onward. This is "
        "the SDDT DISCLOSURE exemption, in force now - not the separate SDDT CAPITAL regime beginning 1 January "
        "2027."
    )


RWA_NOTE = (
    "FY2023 RWA shown here (GBP5,229k) is the figure the FY2024 Pillar 3 report carries as its FY2023 "
    "comparative in Section 1.4 'Summary Analysis'. The FY2023 Pillar 3 report's OWN Section 1.4 states "
    "GBP5,101k for that year, and its Section 5 detail table agrees exactly (credit risk GBP4,056k + "
    "operational risk GBP1,045k = GBP5,101k). So the ~2.5% difference is a RESTATEMENT between two "
    "documents, not an internal inconsistency within one: GBP5,229k is the later, restated view. The "
    "restated figure is retained here for consistency with how FY2024 is sourced (both from the FY2024 "
    "report), while the RWA Breakdown sheet's FY2023 column ticks to GBP5,101k because its category rows "
    "are the as-originally-disclosed ones. Corrected 2026-09-15: this note previously described both "
    "figures as coming from the same report's Section 1.4 and Section 5, which is not what the documents "
    "say. FY2022 and FY2021 are unaffected - for those years the summary and detail tables agree exactly "
    "(6,822 and 8,648 respectively)."
)

bw = BankWorkbook(bank_name="Birmingham Bank Limited", years=YEARS, year_label=YEAR_LABEL, header_color="946B2D")

# ---------------------------------------------------------------
# Balance Sheet
# ---------------------------------------------------------------
balance_sheet_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash balances at central banks (FY2025 edition only)", {"FY2025": 14686}),
    ("DATA", "Cash at Bank (Loans and advances to banks from FY2025)", {"FY2025": 603, "FY2024": 11172, "FY2023": 3866, "FY2022": 1896, "FY2021": 2506}),
    ("DATA", "Treasury Bills and similar securities (Investment in debt securities from FY2025)", {"FY2025": 77121, "FY2024": 43093, "FY2023": 20250, "FY2022": 6500, "FY2021": 9750}),
    ("DATA", "Loans and advances to Banks (separate line, FY2022/FY2021 editions)", {"FY2022": 1275, "FY2021": 1271}),
    ("DATA", "Loans and advances to customers", {"FY2025": 540372, "FY2024": 90310, "FY2023": 4195, "FY2022": 6867, "FY2021": 8868}),
    ("DATA", "Tangible fixed assets", {"FY2025": 95, "FY2024": 70, "FY2023": 66, "FY2022": 70, "FY2021": 85}),
    ("DATA", "Intangible fixed assets", {"FY2025": 3249, "FY2024": 2101, "FY2023": 324}),
    ("DATA", "Other assets", {"FY2025": 8162, "FY2024": 3617, "FY2023": 431, "FY2022": 239, "FY2021": 120}),
    ("DATA", "Prepayments and accrued income", {"FY2025": 508, "FY2024": 691, "FY2023": 463, "FY2022": 211, "FY2021": 177}),
    ("DATA", "Derivative financial asset", {"FY2025": "-", "FY2024": 27}),
    ("TOTAL", "Total assets", {"FY2025": 644796, "FY2024": 151081, "FY2023": 29595, "FY2022": 17059, "FY2021": 22777}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Customer accounts (Customer deposits from FY2025)", {"FY2025": 577675, "FY2024": 106868, "FY2023": 9299, "FY2022": 10399, "FY2021": 13916}),
    ("DATA", "Derivative financial liability (FY2025 edition only)", {"FY2025": 1210}),
    ("DATA", "Other liabilities", {"FY2025": 2007, "FY2024": 6098, "FY2023": 1337, "FY2022": 454, "FY2021": 498}),
    ("TOTAL", "Total liabilities", {"FY2025": 580892, "FY2024": 112966, "FY2023": 10636, "FY2022": 10853, "FY2021": 14415}),
    ("SECTION", "Equity", {}),
    ("DATA", "Called up share capital", {"FY2025": 95138, "FY2024": 60138, "FY2023": 30138, "FY2022": 10138, "FY2021": 8207}),
    ("DATA", "Share Premium", {"FY2025": 2862, "FY2024": 2862, "FY2023": 2862, "FY2022": 2862, "FY2021": 2793}),
    ("DATA", "Retained earnings", {"FY2025": -34096, "FY2024": -24885, "FY2023": -14041, "FY2022": -6794, "FY2021": -2637}),
    ("TOTAL", "Total equity", {"FY2025": 63904, "FY2024": 38115, "FY2023": 18959, "FY2022": 6206, "FY2021": 8363}),
    ("TOTAL", "Total liabilities and equity", {"FY2025": 644796, "FY2024": 151081, "FY2023": 29595, "FY2022": 17059, "FY2021": 22777}),
]

bw.add_balance_sheet_sheet(
    title="Birmingham Bank Limited — Balance Sheet",
    subtitle="Bank-solo basis, FRS 102, £'000 (FY2022/FY2021 converted from the source's exact-£ figures)",
    rows=balance_sheet_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=76,
    source_height=280,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Profit & Loss
# ---------------------------------------------------------------
income_statement_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest receivable and similar income arising from debt securities", {"FY2024": 1756, "FY2023": 313, "FY2022": 530, "FY2021": 602}),
    ("DATA", "Other interest receivable and similar income", {"FY2024": 2680, "FY2023": 805, "FY2022": 228, "FY2021": 14}),
    ("DATA", "Interest receivable and similar income (single undivided line, FY2025 edition)", {"FY2025": 21563}),
    ("TOTAL", "Total interest receivable and similar income", {"FY2025": 21563, "FY2024": 4436, "FY2023": 1118, "FY2022": 757, "FY2021": 616}),
    ("DATA", "Interest payable and similar charges", {"FY2025": -15781, "FY2024": -1997, "FY2023": -213, "FY2022": -90, "FY2021": -115}),
    ("DATA", "Fee and commissions expense (FY2025 edition only)", {"FY2025": -121}),
    ("DATA", "Net (loss)/gain on financial instruments at fair value through profit and loss (Net gain from derivatives and hedge accounting from FY2025)", {"FY2025": 211, "FY2024": 27}),
    ("TOTAL", "Net income (Total income in the FY2025 edition)", {"FY2025": 5872, "FY2024": 2466, "FY2023": 905, "FY2022": 667, "FY2021": 500}),
    ("DATA", "Administrative expenses", {"FY2025": -15184, "FY2024": -13155, "FY2023": -8475, "FY2022": -4817, "FY2021": -3858}),
    ("DATA", "Depreciation and amortisation", {"FY2024": -237, "FY2023": -32, "FY2022": -24, "FY2021": -42}),
    ("DATA", "Impairment charge for loan losses (Provision for bad and doubtful debts from FY2025)", {"FY2025": -250, "FY2024": -22, "FY2023": -4, "FY2022": -21, "FY2021": -34}),
    ("TOTAL", "Loss on ordinary activities before taxation", {"FY2025": -9562, "FY2024": -10948, "FY2023": -7606, "FY2022": -4194, "FY2021": -3434}),
    ("DATA", "Tax on profit on ordinary activities", {"FY2025": 351, "FY2024": 104, "FY2023": 359, "FY2022": 38, "FY2021": 0}),
    ("TOTAL", "Loss for the financial year", {"FY2025": -9211, "FY2024": -10844, "FY2023": -7247, "FY2022": -4156, "FY2021": -3434}),
    ("SECTION", "Other comprehensive income", {}),
    ("DATA", "Other comprehensive income", {"FY2025": 0, "FY2024": 0, "FY2023": 0, "FY2022": 0, "FY2021": 0}),
    ("TOTAL", "Total comprehensive income for the year", {"FY2025": -9211, "FY2024": -10844, "FY2023": -7247, "FY2022": -4156, "FY2021": -3434}),
]

bw.add_income_statement_sheet(
    title="Birmingham Bank Limited — Profit & Loss",
    subtitle="Bank-solo basis, FRS 102, £'000 (FY2022/FY2021 converted from the source's exact-£ figures)",
    rows=income_statement_rows,
    sources_text=STATEMENTS_SOURCES + "\n\n" + PL_NOTE,
    first_col_width=76,
    source_height=300,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Statement of Changes in Equity
# ---------------------------------------------------------------
EQUITY_HEADERS = ["Called up Share Capital", "Share Premium", "Retained Earnings", "Total Equity"]

equity_changes_rows = [
    ("TOTAL", "At 1 January 2021", (2000, 0, 796, 2796)),
    ("DATA", "Capital injection", (6207, 2793, 0, 9000)),
    ("DATA", "Total comprehensive income", (0, 0, -3434, -3434)),
    ("TOTAL", "At 31 December 2021", (8207, 2793, -2637, 8363)),
    ("DATA", "Capital injection", (1931, 69, 0, 2000)),
    ("DATA", "Total comprehensive income", (0, 0, -4156, -4156)),
    ("TOTAL", "At 31 December 2022", (10138, 2862, -6794, 6206)),
    ("DATA", "Issue of new shares", (20000, 0, 0, 20000)),
    ("DATA", "Total comprehensive income", (0, 0, -7247, -7247)),
    ("TOTAL", "At 31 December 2023", (30138, 2862, -14041, 18959)),
    ("DATA", "Issue of new shares", (30000, 0, 0, 30000)),
    ("DATA", "Total comprehensive income", (0, 0, -10844, -10844)),
    ("TOTAL", "At 31 December 2024", (60138, 2862, -24885, 38115)),
    ("DATA", "Issue of new shares", (35000, 0, 0, 35000)),
    ("DATA", "Total comprehensive expense", (0, 0, -9211, -9211)),
    ("TOTAL", "At 31 December 2025", (95138, 2862, -34096, 63904)),
]

bw.add_equity_changes_sheet(
    title="Birmingham Bank Limited — Statement of Changes in Equity",
    subtitle="Bank-solo basis, FRS 102, £'000, chronological, 1 January 2021 - 31 December 2025",
    headers=EQUITY_HEADERS,
    rows=equity_changes_rows,
    sources_text=STATEMENTS_SOURCES
    + "\n\nThe capital-raise row is labelled 'Capital injection' in the bank's own 2021/2022 filings and "
    "'Issue of new shares' in its 2023/2024/2025 filings - same underlying event (a share capital + share "
    "premium increase), the bank's own wording just changed year to year; reproduced here as each filing "
    "states it. The comprehensive-income row is likewise labelled 'Total comprehensive income' through "
    "FY2024 and 'Total comprehensive expense' in FY2025 (the amount is a loss in every year).\n"
    "FY2025's movements come from the FY2025 edition's own Statement of Changes in Equity, p.30: 35,000,000 "
    "ordinary GBP1 shares issued at par to the immediate parent (Note 23), taking called-up share capital "
    "to GBP95,138k, and a total comprehensive expense of GBP9,211k taking retained earnings to "
    "GBP(34,096)k. This is the one sheet the FY2025 edition does NOT restate: its opening 'At 1 January "
    "2024' and 'At 31 December 2024' lines reproduce the FY2024 edition's figures exactly.",
    first_col_width=50,
    source_height=260,
)

# ---------------------------------------------------------------
# Sheet: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Reconciliation of operating (loss) to net operating cash flows", {}),
    ("DATA", "Loss on ordinary activities after taxation", {"FY2025": -9211, "FY2024": -10844, "FY2023": -7247, "FY2022": -4156, "FY2021": -3434}),
    ("DATA", "Increase in prepayments and accrued income", {"FY2024": -228, "FY2023": -252, "FY2022": -34, "FY2021": -238}),
    ("DATA", "Increase in derivative financial asset", {"FY2024": -27}),
    ("DATA", "Increase/(decrease) in accruals and deferred income", {"FY2024": 4761, "FY2023": 883, "FY2022": -44, "FY2021": 396}),
    ("DATA", "Increase/(decrease) in provision for bad and doubtful debts", {"FY2025": 250, "FY2024": 22, "FY2023": -4, "FY2022": -21, "FY2021": -8}),
    ("DATA", "Loans and advances written off net of recoveries", {"FY2022": 0, "FY2021": 0}),
    ("DATA", "Depreciation and amortisation", {"FY2024": 237, "FY2023": 32, "FY2022": 24, "FY2021": 42}),
    ("DATA", "Depreciation (separate line, FY2025 edition)", {"FY2025": 19}),
    ("DATA", "Amortisation (separate line, FY2025 edition)", {"FY2025": 470}),
    ("DATA", "Fair value movement on derivatives (FY2025 edition)", {"FY2025": -211}),
    ("DATA", "Interest income from debt securities (FY2025 edition)", {"FY2025": -3742}),
    ("DATA", "Taxation - credit", {"FY2024": -104, "FY2023": -123, "FY2022": -38, "FY2021": 0}),
    ("TOTAL", "Net cash outflow from trading activities ('Total' in the FY2025 edition)", {"FY2025": -12425, "FY2024": -6183, "FY2023": -6711, "FY2022": -4270, "FY2021": -3242}),
    ("DATA", "Net (increase)/decrease in loans and advances to credit institutions and customers (customers only from FY2025)", {"FY2025": -450539, "FY2024": -86137, "FY2023": 3951, "FY2022": 2018, "FY2021": 1328}),
    ("DATA", "Decrease/(increase) in financial assets / treasury bills", {"FY2024": -22843, "FY2023": -13750, "FY2022": 3250, "FY2021": -4250}),
    ("DATA", "Increase/(decrease) in deposits by customers", {"FY2025": 469366, "FY2024": 97569, "FY2023": -1100, "FY2022": -3518, "FY2021": -1837}),
    ("DATA", "Increase/(decrease) in other assets", {"FY2025": -5262, "FY2024": -3082, "FY2023": 167, "FY2022": -81, "FY2021": 8}),
    ("DATA", "(Increase)/decrease in accrued income and prepayments (FY2025 edition, below the subtotal)", {"FY2025": 164}),
    ("DATA", "Increase/(decrease) in other liabilities (FY2025 edition, below the subtotal)", {"FY2025": -74}),
    ("TOTAL", "Net cash (outflow)/inflow from operating activities", {"FY2025": 1230, "FY2024": -20676, "FY2023": -17679, "FY2022": -2601, "FY2021": -7994}),
    ("SECTION", "Cash flow from investing activities", {}),
    ("DATA", "Purchase of debt securities (FY2025 edition)", {"FY2025": -215414}),
    ("DATA", "Proceeds from sale/maturity of debt securities (FY2025 edition)", {"FY2025": 184972}),
    ("DATA", "Purchase of fixed assets", {"FY2025": -44, "FY2024": -36, "FY2023": -45, "FY2022": -9, "FY2021": -42}),
    ("DATA", "Purchase of intangible assets", {"FY2025": -1618, "FY2024": -1982, "FY2023": -307, "FY2022": 0}),
    ("TOTAL", "Net cash outflow from investing activities", {"FY2025": -32104, "FY2024": -2018, "FY2023": -352, "FY2022": -9, "FY2021": -42}),
    ("SECTION", "Cash flow from financing activities", {}),
    ("DATA", "Called up share capital additions", {"FY2025": 35000, "FY2024": 30000, "FY2023": 20000, "FY2022": 2000, "FY2021": 9000}),
    ("TOTAL", "Net cash inflow from financing activities", {"FY2025": 35000, "FY2024": 30000, "FY2023": 20000, "FY2022": 2000, "FY2021": 9000}),
    ("TOTAL", "Increase/(decrease) in cash and cash equivalents", {"FY2025": 4126, "FY2024": 7306, "FY2023": 1969, "FY2022": -610, "FY2021": 964}),
    ("SECTION", "Analysis of the balances of cash", {}),
    ("DATA", "Cash at bank at beginning of year", {"FY2025": 11163, "FY2024": 3866, "FY2023": 1897, "FY2022": 2506}),
    ("TOTAL", "Cash at bank at end of year", {"FY2025": 15289, "FY2024": 11172, "FY2023": 3866, "FY2022": 1896, "FY2021": 2506}),
]

bw.add_cash_flow_sheet(
    title="Birmingham Bank Limited — Statement of Cash Flows",
    subtitle="Bank-solo basis, FRS 102, £'000 (FY2022/FY2021 converted from the source's exact-£ figures)",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=90,
    source_height=280,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Asset Quality
# ---------------------------------------------------------------
asset_quality_rows = [
    ("SECTION", "Loans and advances to customers", {}),
    ("DATA", "Gross loans and advances to customers", {"FY2025": 549420, "FY2024": 90352, "FY2023": 4215, "FY2022": 6879, "FY2021": 8901}),
    ("DATA", "Effective interest rate adjustment (FY2025 edition only)", {"FY2025": -10205}),
    ("DATA", "Bad debt provisions", {"FY2025": -292, "FY2024": -42, "FY2023": -20, "FY2022": -12, "FY2021": -33}),
    ("DATA", "Fair value adjustment for hedged asset (FY2025 edition only)", {"FY2025": 1449}),
    ("TOTAL", "Net loans and advances to customers", {"FY2025": 540372, "FY2024": 90310, "FY2023": 4195, "FY2022": 6867, "FY2021": 8868}),
    ("SECTION", "Gross loan book by maturity (FY2021-FY2024 editions' own maturity analysis)", {}),
    ("DATA", "Repayable on demand", {"FY2024": 5, "FY2023": 5, "FY2022": 13, "FY2021": 44}),
    ("DATA", "Repayable within 3 months", {"FY2024": 277, "FY2023": 409, "FY2022": 927, "FY2021": 1182}),
    ("DATA", "Repayable between 3 months and one year", {"FY2024": 611, "FY2023": 1198, "FY2022": 2374, "FY2021": 2919}),
    ("DATA", "Repayable between one year and five years", {"FY2024": 89459, "FY2023": 2603, "FY2022": 3564, "FY2021": 4758}),
    ("SECTION", "Loan book by interest-rate re-pricing band (FY2025 edition, Note 29 - net carrying amount)", {}),
    ("DATA", "Not more than 3 months", {"FY2025": 18}),
    ("DATA", "3 months to 1 year", {"FY2025": 8031}),
    ("DATA", "1 year to 5 years", {"FY2025": 532323}),
    ("TOTAL", "Loans and advances to customers (net, per Note 29)", {"FY2025": 540372}),
    ("SECTION", "Coverage", {}),
    ("DATA", "Bad debt provision coverage (Provision / Gross loans)", {"FY2025": "0.05%", "FY2024": "0.05%", "FY2023": "0.47%", "FY2022": "0.17%", "FY2021": "0.37%"}),
]

bw.add_asset_quality_sheet(
    title="Birmingham Bank Limited — Asset Quality",
    subtitle="Bank-solo basis, FRS 102, £'000. See source note at bottom.",
    rows=asset_quality_rows,
    sources_text=STATEMENTS_SOURCES + "\n\n" + ASSET_QUALITY_NOTE,
    first_col_width=78,
    source_height=280,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# KM1 Key Metrics - NOT APPLICABLE (no such table in any edition)
# ---------------------------------------------------------------
KM1_SOURCES = (
    "Birmingham Bank Limited has never published the UK KM1 'Key metrics' template. This is a bounded "
    "negative, not a gap: every Pillar 3 disclosure the Bank has issued was fetched and read in full "
    "(checked 2026-09-16).\n\n"
    "EDITIONS CHECKED - three exist, one per year, and each is a different document:\n"
    f"FY2024 (cover: 'For the year ended 31 December 2024'), 24pp - {P3_URL}\n"
    f"FY2023 (cover: 'For the year ended 31 December 2023'), 24pp, md5 ae21adfa2ee6000cf6a8df9801b28487 - "
    f"{P3_2023_URL}\n"
    f"FY2022 (cover: 'For the year ended 31 December 2022'), 24pp, md5 e1a32b0e3f4a9f64576a9092859f45ab - "
    f"{P3_2022_URL}\n"
    "NOTE ON THOSE LAST TWO URLs: they are the SAME path. The Bank overwrites its Pillar 3 file in place, so "
    "the live URL now serves the FY2023 edition while the dated Wayback capture still serves the FY2022 one - "
    "which is exactly why the FY2022 citation is pinned to a capture. The two files differ (md5s above). "
    "Do not 'simplify' the FY2022 citation to the live URL; that would silently swap the edition.\n\n"
    "WHY 'NOT APPLICABLE' RATHER THAN 'NOT FOUND'. Searching each edition's text: 'KM1' occurs 0 times and "
    "'key metric' 0 times, while the same extraction returns CET1/Common Equity 18 times, 'own funds' 3, "
    "'leverage' 5 and LCR 7-9 times in every edition. The extraction demonstrably reaches the capital and "
    "liquidity vocabulary where it is printed, so the absence of the template is a property of the documents, "
    "not of the tool. The Bank instead publishes a narrative Pillar 3 whose Section 1.4 'Summary Analysis' "
    "carries the headline figures; those feed the individual metric sheets in this workbook and are cited "
    "there. Nothing on this sheet is back-filled from the statutory accounts.\n\n"
    "PARENT CHECKED TOO (a subsidiary's KM1 is often published inside its parent's Pillar 3, as extra columns "
    "or an appendix table). Companies House PSC register for company 00555071, read 2026-09-16, shows the "
    "controlling party has been: Bira Trading Limited (England, reg 11628600, 75%+) until it CEASED on 8 "
    "January 2021; and Better Home And Finance Holding Company (ACTIVE, notified 22 December 2025, 75%+ of "
    "shares and voting rights, 3 World Trade Center, New York; governing law Delaware Corporate Law; place "
    "registered Delaware; registration number 1484882; incorporated in the United States). A UK private "
    "holding company and a US Delaware corporation respectively - neither is a UK CRR institution carrying a "
    "Pillar 3 / Article 433 disclosure duty, nor an EU CRR institution carrying an Article 13(1) large-"
    "subsidiary duty. So there is no parent Pillar 3 in which a Birmingham Bank KM1 could appear, in any "
    "year this workbook covers. (The FY2024 Annual Report could not answer this: it is an image-only scan - "
    "39 pages carrying 38 characters of text layer.)\n\n"
    "SDDT IS NOT THE EXPLANATION - see the fuller note on the Total Capital sheet. The Bank does hold the "
    "SDDT Rule 3.1 opt-in, but it starts 14/04/2026, which post-dates all three editions above and therefore "
    "explains none of them. It is consistent with no FY2025 edition having appeared as at 2026-09-16, when "
    "the Bank's own site linked exactly one Pillar 3 document (the FY2024 one).\n\n"
    "FY2025 RE-CHECKED 2026-09-18 (GA-003). Still three editions, still no KM1. The Bank's own footer - its "
    "only index of regulatory documents, and one carrying policy PDFs version-stamped 14-07-2026, so "
    "demonstrably current - links exactly one Pillar 3 report, and that URL still serves the FY2024 "
    "edition (fetched 18 Sep 2026: HTTP 200, application/pdf, %PDF magic bytes, cover reads 'For the year "
    "ended 31 December 2024'). A Wayback CDX sweep of the domain returns the same five captures and no "
    "sixth. So no FY2025 Pillar 3 document exists to hold a KM1 table, and the FY2025 column here is "
    "'Not applicable' on the same footing as the four before it. The FY2025 Annual Report cannot supply "
    "one either: 'KM1' and 'key metric' return zero hits across its 51 pages, as do 'CET1', 'own funds', "
    "'leverage' and 'risk weighted', in a document returning 'capital adequacy' 5 times and 'liquidity "
    "coverage' twice - so the absence is the document's, not the extraction's. (Unlike the FY2024 scan, "
    "the FY2025 scan HAS been OCR'd and read in full for this check, which is why a text search of it can "
    "be quoted at all.)\n"
    "The controlling party finding above is unchanged and is confirmed by the FY2025 accounts themselves: "
    "Note 27 states 'The Bank is 100% owned by Better Home and Finance Holding Company. A US listed "
    "company.' A US listed holding company carries no UK or EU Pillar 3 disclosure duty, so there is still "
    "no parent report in which a Birmingham Bank KM1 could appear."
)

bw.add_km1_sheet(
    title="Birmingham Bank Limited - KM1 Key Metrics",
    subtitle="Not applicable - the Bank publishes a narrative Pillar 3 and has never printed the UK KM1 template",
    rows=[
        ("DATA", "UK KM1 'Key metrics' template", {y: "Not applicable" for y in YEARS}),
    ],
    sources_text=KM1_SOURCES,
    first_col_width=76,
    source_height=520,
    years=YEARS,
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, note=None):
    bw.add_metric_sheet(name, unit, rows_data, p3_sources(), note=note, first_col_width=52, source_height=190)


# FY2022/FY2021 added 2026-09-15 from the recovered FY2022 Pillar 3 report - see CAPITAL_2022_NOTE.
TOTAL_CAPITAL = {"FY2025": "Not publicly disclosed", "FY2024": 35985, "FY2023": 18617, "FY2022": 6172, "FY2021": 8314}
# FY2022/FY2021 RESTATED 2026-09-15 from the Strategic Report's 91%/97% onto the Pillar 3's own
# 90%/96% - same basis as the capital amounts above and the RWAs below. See CAPITAL_2022_NOTE.
CAPITAL_RATIO = {"FY2025": "30.43%", "FY2024": "76%", "FY2023": "365%", "FY2022": "90%", "FY2021": "96%"}
RWA = {"FY2025": "Not publicly disclosed", "FY2024": 47333, "FY2023": 5229, "FY2022": 6822, "FY2021": 8648}
LEVERAGE = {"FY2025": "Not publicly disclosed", "FY2024": "24%", "FY2023": "63%", "FY2022": "36%", "FY2021": "37%"}
LCR = {"FY2025": "460%", "FY2024": "725%", "FY2023": "11,351%", "FY2022": "2,983%", "FY2021": "16,250%"}

SINGLE_TIER_NOTE = "No Additional Tier 1 or Tier 2 capital in any year - equals CET1 Capital exactly."

CAPITAL_2022_NOTE = (
    "FY2022 & FY2021 ADDED/RESTATED 2026-09-15 from the recovered FY2022 Pillar 3 report, which prints "
    "both years side by side and which earlier builds did not have. This supersedes the previous position "
    "that 'no GBP CET1/Tier 1/Total Capital figure for FY2021 was found in any document'.\n"
    "AMOUNTS (new cells): Total CET1 capital GBP6,172k (FY2022) and GBP8,314k (FY2021), from the "
    "'regulatory capital resources' table, Section 5.1. Both foot exactly within that table - FY2022 Total "
    "Equity 6,206 less regulatory deductions 34 = 6,172; FY2021 Total Equity 8,363 less 49 = 8,314 - and "
    "FY2022 is independently repeated in the report's own Section 10 'Own Funds Disclosure' table (CET1 "
    "before regulatory adjustments 6,206, total regulatory adjustments (34), CET1 capital 6,172, Tier 1 "
    "capital 6,172, Total capital 6,172). The report states 'The Bank holds only tier 1 capital', so CET1 = "
    "Tier 1 = Total Capital for both years, consistent with every other year on these sheets.\n"
    "CROSS-CHECK PASSED: the same Section 1.4 summary table gives Risk Weighted assets of 6,822 (FY2022) "
    "and 8,648 (FY2021), which reproduce this workbook's existing Total RWAs figures for both years "
    "exactly, and Liquidity coverage ratio 2,983% / 16,250%, which reproduce the existing LCR cells "
    "exactly. That is what confirms the document is the right entity, basis and years.\n"
    "RATIOS RESTATED, AND THE SUPERSEDED VALUES ARE RECORDED HERE RATHER THAN DISCARDED: this workbook "
    "previously carried FY2022 91% and FY2021 97% (the latter disclosed as 96.69%), taken from the "
    "Strategic Report 'key financial performance indicators' table, which was the only source available "
    "before the Pillar 3 report was recovered. The Pillar 3 report gives 90% and 96% for the same two "
    "years - in its Section 1.4 summary ('Tier 1 Capital ratio') and, for FY2022, again in its Section 10 "
    "own-funds table, where CET1, Tier 1 and Total capital ratios are each printed as 90%. The Pillar 3 "
    "figures are now carried because they are internally consistent with the capital amounts and RWAs on "
    "these same sheets (6,172/6,822 = 90.5%; 8,314/8,648 = 96.1%), whereas retaining 91%/97% alongside "
    "those amounts would have left the sheets arithmetically self-contradictory. The ~0.5pp difference is "
    "a genuine source-basis difference between the two documents, NOT a rounding artefact and NOT an error "
    "in either - it is documented, not resolved. No ratio here is back-solved: every value is printed in "
    "the source.\n"
    "CITATION TRAP - DO NOT 'SIMPLIFY' THE SOURCE URL. The FY2022 report is cited above at a Wayback "
    "snapshot. The live URL bearing the FY2022 filename "
    "(birminghambank.com/wp-content/uploads/Birmingham-Bank-Pillar-3-Disclosures-2022-final.pdf) returns "
    "HTTP 200 but now serves the FY2023 DOCUMENT - the Bank re-uploaded over it. Only the snapshot reaches "
    "the real FY2022 edition, verified on fetch by its own cover line 'For the year ended 31 December "
    "2022'. Rewriting the citation to the live URL would silently repoint every figure above at the wrong "
    "year."
)

CAPITAL_FIGURE_NOTE = (
    "The Pillar 3 report's own Section 1.4 'Summary Analysis' headline FY2024 Tier 1 capital (GBP35,985k, "
    "shown here) differs from the same report's own Section 5.1 capital-resources table and Section 9 'Own "
    "Funds Disclosure' table (Total Equity GBP38,115k less regulatory deductions GBP2,008k = GBP36,107k) - "
    "both are the entity's own genuine disclosures in the same document, ~0.3% apart; the headline summary "
    "figure is used for consistency with how every other year/metric on this sheet is sourced (same class of "
    "internal document inconsistency as the RWA figures - see the Total RWAs sheet's own note). FY2023 has "
    "no such discrepancy - both of the report's tables agree at GBP18,617k."
)

metric("CET1 Capital", "£'000", [("Common Equity Tier 1 (CET1) capital", TOTAL_CAPITAL)],
       note=CAPITAL_FIGURE_NOTE + "\n" + CAPITAL_2022_NOTE)
metric("CET1 Ratio", "%", [("CET1 Ratio (= Capital Adequacy Ratio)", CAPITAL_RATIO)],
       note=CAPITAL_2022_NOTE)
metric("Tier 1 Capital", "£'000", [("Tier 1 capital", TOTAL_CAPITAL)],
       note=SINGLE_TIER_NOTE + " " + CAPITAL_FIGURE_NOTE + "\n" + CAPITAL_2022_NOTE)
metric("Tier 1 Ratio", "%", [("Tier 1 Capital ratio", CAPITAL_RATIO)],
       note=CAPITAL_2022_NOTE)
metric("Total Capital", "£'000", [("Total capital", TOTAL_CAPITAL)],
       note=SINGLE_TIER_NOTE + " " + CAPITAL_FIGURE_NOTE + "\n" + CAPITAL_2022_NOTE)
metric("Total Capital Ratio", "%", [("Total Capital Ratio (= Capital Adequacy Ratio)", CAPITAL_RATIO)],
       note=CAPITAL_2022_NOTE)
metric("Total RWAs", "£'000", [("Total risk-weighted assets", RWA)], note=RWA_NOTE)

rwa_breakdown_rows = [
    ("DATA", "Credit risk", {"FY2025": "Not publicly disclosed", "FY2024": 46037, "FY2023": 4056, "FY2022": 5797, "FY2021": 7133}),
    ("DATA", "Operational risk", {"FY2025": "Not publicly disclosed", "FY2024": 1296, "FY2023": 1045, "FY2022": 1025, "FY2021": 1515}),
    ("TOTAL", "Total RWAs (Pillar 1)", {"FY2025": "Not publicly disclosed", "FY2024": 47333, "FY2023": 5101, "FY2022": 6822, "FY2021": 8648}),
]

bw.add_rwa_breakdown_sheet(
    title="Birmingham Bank Limited — RWA Breakdown",
    subtitle="Bank-solo basis, £'000. See source note at bottom.",
    rows=rwa_breakdown_rows,
    sources_text=p3_sources()
    + "\n\nThe Bank has no exposure to market risk under Pillar 1 (per the Pillar 3 report's own statement) "
    "- credit risk and operational risk are the only two categories.\n\n"
    "FY2022 & FY2021 ADDED 2026-09-15, correcting a prior claim. This sheet previously stated that 'no "
    "Pillar 3 document covers those years'. That was wrong: a Wayback CDX sweep of birminghambank.com "
    "recovered 'Birmingham-Bank-Pillar-3-Disclosures-2022-final.pdf', a genuine text-layer Pillar 3 report "
    "headed 'For the year ended 31 December 2022', whose Section 5.2 RWA detail table gives both FY2022 and "
    "its FY2021 comparative:\n"
    "  FY2022 - total credit risk exposure 5,797 + operational risk 1,025 = 6,822\n"
    "  FY2021 - total credit risk exposure 7,133 + operational risk 1,515 = 8,648\n"
    "Both tie exactly to that same document's Section 1.4 'Summary Analysis' headline Risk Weighted assets "
    f"row (6,822 and 8,648). Source: {P3_2022_URL}\n"
    "FY2022 is further corroborated INDEPENDENTLY by the FY2023 Pillar 3 report, whose own comparative "
    "column reproduces 5,797 + 1,025 = 6,822 exactly. A third consistency check: this document's Section "
    "1.4 liquidity coverage ratios (FY2022 2,983%, FY2021 16,250%) reproduce the LCR figures already "
    "carried on this workbook's LCR sheet for those years, confirming the same entity and basis.\n\n"
    "CITATION TRAP - do not 'simplify' the FY2022 URL to the live one. The bank has re-uploaded its FY2023 "
    "report OVER that filename, so the live "
    "https://www.birminghambank.com/wp-content/uploads/Birmingham-Bank-Pillar-3-Disclosures-2022-final.pdf "
    "returns HTTP 200 but serves the year-ended-31-December-2023 document. The Wayback snapshot above is "
    "the only reliable route to the real FY2022 edition. (Verified 2026-09-15: the live file's first page "
    "reads 'For the year ended 31 December 2023'.)\n\n"
    "Also recovered but NOT used: a 'Birmingham-Bank-Pillar-3.pdf' for the year ended 31 December 2020, "
    "archived 2021-08-05. FY2020 is outside this workbook's YEARS range, so it is recorded here only as a "
    "known-existing document should the range ever be extended.\n\n"
    "FY2025 IS MARKED 'Not publicly disclosed' ON ALL THREE ROWS, NOT LEFT BLANK. There is no FY2025 "
    "Pillar 3 report (see the dated three-route check in the sources above), and the FY2025 Annual Report "
    "prints no RWA figure of any kind: 'risk weighted' and 'risk-weighted' return zero hits across its 51 "
    "pages, and the 11 apparent hits on the bare string 'RWA' are all the letter sequence inside 'forward' "
    "and 'straightforward'. So there is no FY2025 total to break down and no categories to break it into.",
    first_col_width=46,
    source_height=200,
    unit_suffix=" (£'000)",
)

metric("Leverage Ratio", "%", [("Leverage ratio", LEVERAGE)],
       note=CAPITAL_2022_NOTE)
metric("LCR", "%", [("Liquidity Coverage Ratio", LCR)],
       note="FY2022/FY2023 figures (2,983% / 11,351%) are genuinely this large - a small, low-loan-volume "
            "bank holding a large liquidity buffer relative to its (paused) lending book during its 2023 "
            "infrastructure-build year. Not a transcription error - see ENTITY_NOTE on the Cash Flow sheet.")

bw.add_not_disclosed_metric_sheets(
    ["NSFR", "MREL Ratio"],
    p3_sources(),
    per_note={
        "NSFR": "Not found in any Annual Report or in any of the three Pillar 3 documents published. "
                "Re-tested on the FY2025 Annual Report, 2026-09-18: 'NSFR' and 'net stable' each return "
                "zero hits across its 51 pages, in a document returning 'liquidity coverage' twice and "
                "'cash flow' 23 times - so the term is absent from the document, not from the extraction.",
        "MREL Ratio": "Not found - the Bank is small enough to plausibly sit below the BoE's MREL "
                      "threshold, but no explicit statement to that effect was found either. Re-tested on "
                      "the FY2025 Annual Report, 2026-09-18: 'MREL' returns zero hits across its 51 pages, "
                      "with the same richness control as the NSFR sheet.",
    },
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {"FY2025": 644796, "FY2024": 151081, "FY2023": 29595, "FY2022": 17059, "FY2021": 22777}),
        ("Total liabilities", {"FY2025": 580892, "FY2024": 112966, "FY2023": 10636, "FY2022": 10853, "FY2021": 14415}),
        ("Total equity", {"FY2025": 63904, "FY2024": 38115, "FY2023": 18959, "FY2022": 6206, "FY2021": 8363}),
    ],
    balance_sheet_unit="£'000",
    income_statement_totals=[
        ("Total interest receivable and similar income", {"FY2025": 21563, "FY2024": 4436, "FY2023": 1118, "FY2022": 757, "FY2021": 616}),
        ("Loss for the financial year", {"FY2025": -9211, "FY2024": -10844, "FY2023": -7247, "FY2022": -4156, "FY2021": -3434}),
    ],
    income_statement_unit="£'000",
    equity_changes_totals=[
        ("Total equity (period end)", {"FY2025": 63904, "FY2024": 38115, "FY2023": 18959, "FY2022": 6206, "FY2021": 8363}),
    ],
    equity_changes_unit="£'000",
    cash_flow_totals=[
        ("Net cash (outflow)/inflow from operating activities", {"FY2025": 1230, "FY2024": -20676, "FY2023": -17679, "FY2022": -2601, "FY2021": -7994}),
        ("Net cash outflow from investing activities", {"FY2025": -32104, "FY2024": -2018, "FY2023": -352, "FY2022": -9, "FY2021": -42}),
        ("Net cash inflow from financing activities", {"FY2025": 35000, "FY2024": 30000, "FY2023": 20000, "FY2022": 2000, "FY2021": 9000}),
        ("Cash at bank at end of year", {"FY2025": 15289, "FY2024": 11172, "FY2023": 3866, "FY2022": 1896, "FY2021": 2506}),
    ],
    cash_flow_unit="£'000",
    ratios=[
        ("CET1 Ratio", CAPITAL_RATIO),
        ("Leverage Ratio", LEVERAGE),
        ("LCR", LCR),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own "
         "source citation for the underlying document/page. Only 5 years of history exist (FY2021-FY2025) - "
         "the entity's own accounts filing history and Pillar 3 disclosures don't go back further. "
         "FY2025 was added 2026-09-18 from the FY2025 full accounts filed at Companies House on 14 Sep 2026; "
         "the Leverage Ratio has no FY2025 value because there is no FY2025 Pillar 3 report and the Annual "
         "Report does not print one. The income row is labelled 'Total interest receivable and similar "
         "income' rather than 'Total income' because the FY2025 edition uses 'Total income' for a different "
         "subtotal - see the Profit & Loss sheet's note.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/BIRMINGHAM BANK FINANCIALS.xlsx")
