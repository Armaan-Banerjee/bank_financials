import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021",
         "FY2020", "FY2019", "FY2018", "FY2017", "FY2016"]  # most recent first
YEAR_LABEL = {y: y for y in YEARS}

AR2025_URL = ("https://find-and-update.company-information.service.gov.uk/company/02009520/"
              "filing-history/MzUxNzE0OTI3NGFkaXF6a2N4/document?format=pdf&download=0")
AR2023_URL = ("https://find-and-update.company-information.service.gov.uk/company/02009520/"
              "filing-history/MzQxOTY5NDQ0MWFkaXF6a2N4/document?format=pdf&download=0")
AR2021_URL = ("https://find-and-update.company-information.service.gov.uk/company/02009520/"
              "filing-history/MzMzNzU0NDMwOWFkaXF6a2N4/document?format=pdf&download=0")
AR2020_URL = ("https://find-and-update.company-information.service.gov.uk/company/02009520/"
              "filing-history/MzMwMTQ3Nzk1MmFkaXF6a2N4/document?format=pdf&download=0")
AR2019_URL = ("https://find-and-update.company-information.service.gov.uk/company/02009520/"
              "filing-history/MzI2MjYyNzE3OGFkaXF6a2N4/document?format=pdf&download=0")
AR2018_URL = ("https://find-and-update.company-information.service.gov.uk/company/02009520/"
              "filing-history/MzIzMzQ0Nzg3OWFkaXF6a2N4/document?format=pdf&download=0")
AR2017_URL = ("https://find-and-update.company-information.service.gov.uk/company/02009520/"
              "filing-history/MzIwMzkxNjcwMmFkaXF6a2N4/document?format=pdf&download=0")
AR2016_URL = ("https://find-and-update.company-information.service.gov.uk/company/02009520/"
              "filing-history/MzE3NDY1MzYyMmFkaXF6a2N4/document?format=pdf&download=0")

ENTITY_NOTE = (
    "Credit Suisse (UK) Limited ('CSUK', company 02009520, FRN 124269) - a UK private-banking/wealth-"
    "management subsidiary. Ultimate parent is UBS Group AG following UBS's acquisition of Credit Suisse "
    "Group (announced March 2023, completed June 2023) - CSUK itself remains an active, separately-"
    "reporting PRA entity throughout, still filing under its original name as of the FY2025 filing (Apr "
    "2026). All 10 Companies House filings (FY2016-FY2025) were fully scanned/image-only, transcribed via "
    "page rendering.\n\n"
    "HISTORICAL-DEPTH EXTENSION (HD-026, 2026-09-06): extended back to FY2016, this entity's confirmed "
    "floor per HD-004 (entity itself dates to 1985 as company 02009520, but this is capped project-wide at "
    "FY2014 regardless, and no FY2014/FY2015 filing was in scope for this ticket). Re-verified via each "
    "year's own Companies House filing rather than relying on HD-004's domain/scan signal alone. Genuine "
    "format changes found across the extended window, all documented rather than smoothed over:\n"
    "- FY2016/FY2017 Annual Reports carry no 'Key Performance Indicators' summary table at all (introduced "
    "only from the FY2018 Annual Report onward) - FY2017's KPI-style figures (RWA, CET1 ratio, Leverage "
    "Ratio, CET1 Capital) were sourced from the FY2018 report's own FY2017 comparative column; no such "
    "comparative exists anywhere for FY2016, so FY2016's RWA, CET1/Tier1 Ratio, Leverage Ratio, LCR and "
    "NSFR are self-skipped as undisclosed in any filing obtained. QUALIFIED 18 September 2026 (KM1-032): "
    "the parenthetical here used to read 'confirmed via a Wayback CDX search of credit-suisse.com for a "
    "standalone Pillar 3 document, which returned no CSUK-specific hit before the search was judged "
    "uneconomical to keep pursuing', and the word 'confirmed' was doing work the search cannot support. A "
    "CDX search that was abandoned for cost is not an enumeration, and an archive scan can never see a "
    "live-only document in any case. The correct status of the FY2016 standalone Pillar 3 is UNPROVEN, not "
    "absent - and note that CSUK's standalone Pillar 3 documents for later years demonstrably DO exist and "
    "are used on the KM1 and capital sheets of this workbook, so the premise that CSUK published none is "
    "already known to be false for other years. "
    "SETTLED IN PART, 18 September 2026 (interior-gap sweep): a 2016 CSUK Pillar 3 edition DOES exist and "
    "is listed by name on the UBS-hosted Credit Suisse legal-entity ARCHIVE index, which was successfully "
    "enumerated that day at https://www.ubs.com/global/en/investor-relations/complementary-financial-"
    "information/disclosure-legal-entities/archive-credit-suisse.html (plain curl clears the 403 that a "
    "browser User-Agent triggers). That index lists a CSUK edition for every year 2014-2023. "
    "The 2016 edition was NOT opened in that pass, which was scoped to interior gaps only, so FY2016 stays "
    "blank as an UNCHECKED LEAD - a document known to exist and not yet read - rather than as anything "
    "resembling an absence. FY2016 CET1/Tier 1 Capital (the £ amount) "
    "IS available, from the Capital adequacy note's Own Funds table.\n"
    "- Leverage Ratio is disclosed only in the FY2017/FY2018 KPI TABLES (6.3%/7.8%) - absent from FY2016 "
    "(no KPI table) and from FY2019/FY2020's own KPI tables (which dropped the 'Statement of Financial "
    "Position' KPI section entirely). Average LCR is disclosed only in the FY2018 KPI table (154%) - "
    "FY2017's KPI table explicitly shows 'n/a', and FY2019/FY2020 KPI tables carry no LCR figure at all "
    "(only a Liquidity Buffer £ amount). NSFR is not found in any FY2016-FY2020 KPI table.\n"
    "  CORRECTED 18 September 2026: every sentence in the paragraph above is about ONE DOCUMENT TYPE, the "
    "Annual Report KPI table, and it is still accurate about that document. What it used to do, and no "
    "longer does, is finish each clause with 'consistent with the already-known gap' - reading an absence "
    "from the KPI table as an absence from the Bank's disclosure. It is not. CSUK published a leverage "
    "ratio for FY2019, FY2020, FY2021, FY2022 AND FY2023, and an LCR for all five, in its own standalone "
    "Pillar 3 editions for those years; all five leverage figures and a full seven-year average-basis LCR "
    "series are now on the Leverage Ratio and LCR sheets. See those sheets' notes for document, printed "
    "folio and the cross-edition restatements that are recorded but not applied.\n"
    "- Total Capital / Total Capital Ratio: a Capital adequacy note ('Own Funds' table: Total Tier 1/CET1 "
    "capital + Total Tier 2 capital = Own Funds) exists in every FY2016-FY2020 filing and gives a genuine, "
    "directly disclosed Total Capital (£ Own Funds) figure each year - populated on this sheet for FY2016-"
    "FY2020 only. The contradiction this paragraph used to flag - that the FY2021-FY2025 columns carried a "
    "'not directly disclosed' claim on the same sheet - was referred to 'a future audit-only ticket'. THAT "
    "TICKET WAS KM1-032 AND THE CONTRADICTION IS NOW RESOLVED (18 September 2026): Total Capital IS "
    "directly disclosed for FY2021-FY2025, as row 3 of CSUK's own KM1 template and row 59 of its CC1, in "
    "the standalone Pillar 3 editions this workbook already cites. Both the Total Capital and Total Capital "
    "Ratio sheets now carry those years and name that source. The original claim was true only of the KPI "
    "table, which never carried a Total Capital line - a statement about ONE document read as a statement "
    "about the bank's disclosure. No Total Capital RATIO (%) was found disclosed in any year FY2016-FY2020 "
    "either (only the £ Own Funds figure), so that row stays blank for the new years too.\n"
    "- Asset Quality's loan-book note uses the SAME UK/Foreign x Commercial/Consumer borrower-type format "
    "in every FY2016-FY2020 filing checked as the format already used on this sheet for FY2021-FY2023 - no "
    "IFRS 9 stage-level (Stage 1/2/3) split exists in the PRIMARY 'Loans and advances' note in any year "
    "(a separate, secondary Stage 1/2/3 ECL-movement table exists in the Expected Credit Loss Measurement "
    "note from FY2019 onward, but that is not the note the Balance Sheet's own Loans and advances figure "
    "ties to - the borrower-type note is). FY2018's own filing lacks the borrower-type table entirely (it "
    "only shows loans by maturity bucket and by collateral, with no 'Gross Impaired loans' concept at all) - "
    "its borrower-type figures and Gross Impaired loans total were instead sourced from the FY2019 filing's "
    "own FY2018 comparative column, which independently reconciles to FY2018's own disclosed Total Net "
    "loans. FY2016's Gross Impaired loans figure was similarly sourced from FY2017's own FY2016 comparative "
    "column (FY2016's own filing has no Gross Impaired loans line either). Pre-IFRS 9 (adopted 1 January "
    "2018) years show no Profit & Loss 'Allowance for credit losses' line item at all - only a Statement of "
    "Financial Position note giving a simple opening/closing impairment-allowance movement (an incurred-loss "
    "model, IAS 39 basis) - left blank on the P&L for FY2016/FY2017 rather than force-mapped.\n"
    "- Statement of Changes in Equity: FY2016-FY2018 carry a genuine 'Accumulated other comprehensive "
    "income' (available-for-sale reserve) equity component that FY2019 onward does not - added as a new "
    "column on that sheet, populated only where it applies, rather than merged into Retained earnings. The "
    "IFRS 9 initial-application adjustment at 1 January 2018 (a genuine +£2,535k reclassification into "
    "Retained earnings, -£2,289k out of AOCI) is shown as its own adjustment row, not folded into 'the "
    "year's comprehensive income'. FY2019's own filing reports closing Total shareholders' equity of "
    "£322,943k (Retained earnings £9,013k) - FY2020's own filing then restates the FY2019 OPENING balance "
    "down by £1,431k (net of tax, a 'correction of error', not otherwise explained) to £321,512k. Per this "
    "project's convention of using each year's own filing rather than a later year's restated comparative, "
    "FY2019's column keeps its own-filing figure (£322,943k/£9,013k); the FY2020 restatement is instead "
    "shown as an explicit 'Correction of error' bridging row between the FY2019 and FY2020 columns, so nothing "
    "is silently overwritten and the FY2020 opening balance still ties exactly to the £341,173k FY2020 closing.\n"
    "- Cash Flow Statement: FY2016/FY2017/FY2018's own filings show no separate 'Effect of exchange rate "
    "fluctuations on cash and cash equivalents' line after the net movement in cash (FX effects are folded "
    "into the operating-activities reconciliation instead) - that line only appears as its own row from the "
    "FY2019 filing onward. Left blank for FY2016-FY2018 rather than force-derived from a residual.\n\n"
    "TWO MAJOR DISCLOSED BUSINESS EVENTS, both flagged rather than treated as anomalies:\n"
    "(1) FY2023: a pre-tax loss of £26.2m driven by £44.8m of UBS-acquisition-related expenses "
    "(accelerated lease costs, intangibles impairment, recharged transaction costs) - underlying "
    "profit before tax (excluding these) was £18.6m.\n"
    "(2) FY2025: on 20 June 2025 CSUK completed a Part VII business transfer (Financial Services and "
    "Markets Act 2000) of most of its wealth-management clients to UBS AG London Branch, following a "
    "Business Transfer Agreement signed 20 December 2024. This shows up directly in the FY2025 cash flow "
    "statement as a £539,843k 'Cash receipt from business transfer' investing-activities line and a "
    "£1,278k 'Loss from the business transfer' operating-activities adjustment, and drove RWAs down from "
    "£672m (FY2024) to £160m (FY2025) and CET1/leverage ratios sharply higher (smaller balance sheet, "
    "same capital base). CSUK's remaining business post-transfer is the limited-scope Credit Suisse "
    "London Nominees ('CSLN') hedge-fund sub-custody activity.\n\n"
    "Full opening-to-closing cash bridge ties across all 10 years, with several small gaps in the source "
    "documents' own printed figures, none force-corrected: FY2022 closing £475,709k vs FY2023 opening "
    "£475,664k (£45k gap, explicitly explained by the FY2023 report's own footnote as the year-over-year "
    "change in the ECL allowance excluded from the cash figure); and FY2023's own three-line tail (opening "
    "£475,664k + net increase £97,529k - FX effect £24,570k = £548,623k) doesn't quite match FY2023's own "
    "printed closing balance of £548,659k (a £36k gap, source unexplained, not present in any other year - "
    "kept exactly as printed on both sides rather than adjusted to force a match). FY2021 closing £408,082k "
    "= FY2022 opening exactly; FY2023 closing £548,659k = FY2024 opening exactly; FY2024 closing £341,768k "
    "= FY2025 opening exactly; FY2016 closing £432,924k = FY2017 opening exactly; FY2018 closing £197,301k "
    "= FY2019 opening exactly. Two further gaps found in the newly-added FY2016-FY2020 window, both kept as "
    "printed rather than force-matched: FY2017's own filing shows FY2017 closing cash of £499,549k, but "
    "FY2018's own filing's FY2017 COMPARATIVE column shows only £457,975k - a £41,574k gap that exactly "
    "equals the difference between the two filings' 'Interest-bearing deposits with banks' figures for the "
    "same date (£4,885k per FY2017's own filing vs £46,459k per FY2018's FY2017 comparative), confirming "
    "this is a genuine RECLASSIFICATION between the two balance-sheet lines made in the FY2018 filing's "
    "presentation of its FY2017 comparative, not a real cash discrepancy - both years' own-filing figures "
    "are kept as reported. FY2019's own filing shows FY2019 closing cash of £447,816k, but FY2020's own "
    "filing's FY2019 comparative shows £440,029k (a £7,787k gap, source unexplained - no matching "
    "reclassification was found this time, flagged for a future audit ticket rather than silently resolved)."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are Credit Suisse (UK) Limited's own Statement of Cash Flows:\n"
    "FY2025: Full accounts to 31 Dec 2025 (Companies House, filed 25 Apr 2026), "
    "Statement of Cash Flows p.47 - " + AR2025_URL + "\n"
    "FY2024: same FY2025 filing's own FY2024 comparative column, p.47\n"
    "FY2023: Full accounts to 31 Dec 2023 (Companies House, filed 27 Apr 2024), "
    "Statement of Cash Flows p.41 - " + AR2023_URL + "\n"
    "FY2022: same FY2023 filing's own FY2022 comparative column, p.41\n"
    "FY2021: Full accounts to 31 Dec 2021 (Companies House, filed 28 Apr 2022), "
    "Statement of Cash Flows p.46 - " + AR2021_URL + "\n"
    "FY2020: Full accounts to 31 Dec 2020 (Companies House, filed 25 May 2021), "
    "Statement of Cash Flows p.47 - " + AR2020_URL + "\n"
    "FY2019: Full accounts to 31 Dec 2019 (Companies House, filed 20 Apr 2020), "
    "Statement of Cash Flows p.41 - " + AR2019_URL + "\n"
    "FY2018: Full accounts to 31 Dec 2018 (Companies House, filed 01 May 2019), "
    "Statement of Cash Flows p.44 - " + AR2018_URL + "\n"
    "FY2017: Full accounts to 31 Dec 2017 (Companies House, filed 01 May 2018), "
    "Statement of Cash Flows p.28 - " + AR2017_URL + "\n"
    "FY2016: Full accounts to 31 Dec 2016 (Companies House, filed 28 Apr 2017), "
    "Statement of Cash Flows p.24 - " + AR2016_URL + "\n\n"
    + ENTITY_NOTE
)

STATEMENTS_SOURCES = (
    "Sources - Credit Suisse (UK) Limited's own Statement of Income / Statement of Financial Position / "
    "Statement of Changes in Equity, transcribed from each year's own Companies House filing (not a later "
    "year's comparative column):\n"
    "FY2025/FY2024: Full accounts to 31 Dec 2025 (Companies House, filed 25 Apr 2026), pp.44-47 - "
    + AR2025_URL + "\n"
    "FY2023/FY2022: Full accounts to 31 Dec 2023 (Companies House, filed 27 Apr 2024), pp.38-40 - "
    + AR2023_URL + "\n"
    "FY2021: Full accounts to 31 Dec 2021 (Companies House, filed 22 Apr 2022), pp.43-45 - "
    + AR2021_URL + "\n"
    "FY2020: Full accounts to 31 Dec 2020 (Companies House, filed 25 May 2021), pp.44-46 - "
    + AR2020_URL + "\n"
    "FY2019: Full accounts to 31 Dec 2019 (Companies House, filed 20 Apr 2020), pp.38-40 - "
    + AR2019_URL + "\n"
    "FY2018: Full accounts to 31 Dec 2018 (Companies House, filed 01 May 2019), pp.41-43 - "
    + AR2018_URL + "\n"
    "FY2017: Full accounts to 31 Dec 2017 (Companies House, filed 01 May 2018), pp.24-27 - "
    + AR2017_URL + "\n"
    "FY2016: Full accounts to 31 Dec 2016 (Companies House, filed 28 Apr 2017), pp.20-23 - "
    + AR2016_URL + "\n\n"
    + ENTITY_NOTE + "\n\n"
    "PRESENTATION NOTE: the Balance Sheet's own line items vary genuinely across years - 'Current tax "
    "assets' is absent from the FY2021 report (present FY2022-25); 'Deferred tax assets' appears only "
    "FY2021/FY2022; 'Intangible assets'/'Goodwill' are FY2021-23 only (goodwill fully impaired in FY2021, "
    "intangibles fully impaired/written off by FY2025); 'Short-term borrowings' as its own liability line "
    "first appears FY2022 onward (not disclosed as a separate line in FY2021). The Profit & Loss reflects "
    "two genuine one-off lines: FY2021's 'Impairment on goodwill' (£13,752k, no equivalent in later years) "
    "and FY2025's 'Loss from the business transfer' (£1,278k, tied to the Part VII transfer - see ENTITY "
    "NOTE above). All reproduced as reported, blank cells where a year's own report doesn't carry that line.\n\n"
    "FY2016-FY2020 (added under HD-026): 'Current tax assets' is present FY2016-FY2019 (£287k/£274k/£287k/"
    "£0k respectively) but absent as a line item in FY2020 (continuing the same absence into FY2021, "
    "reappearing FY2022); 'Deferred tax assets' and 'Intangible assets'/'Goodwill' (constant £13,752k every "
    "year, only impaired in FY2021 - see above) are present in all 5; 'Financial assets available for sale' "
    "is a genuine asset line existing FY2016-FY2018 only (£2,010k/£2,326k/£0k) - it disappears entirely "
    "from FY2019 onward, in step with the AOCI equity component it funds (see Statement of Changes in "
    "Equity note above), both consistent with the 1 January 2018 IFRS 9 transition reclassifying available-"
    "for-sale securities; 'Short-term borrowings' as its own "
    "liability line does not "
    "exist in any of FY2016-FY2020 (first appears FY2022). Pre-IFRS-9 (adopted 1 January 2018) years "
    "FY2016/FY2017 show no 'Allowance for expected credit losses' P&L line at all (an incurred-loss, not "
    "expected-loss, model) - left blank rather than force-mapped from the separate impairment-movement note. "
    "See ENTITY NOTE above for the FY2016-FY2018 AOCI equity component and the FY2019/FY2020 restatement."
)

ASSET_QUALITY_SOURCES = (
    "Sources - Credit Suisse (UK) Limited's own Loans and advances / Expected Credit Loss notes:\n"
    "FY2025/FY2024: Full accounts to 31 Dec 2025, Note 'Loans' (ECL by IFRS 9 stage), pp.69-70, and "
    "Note 35 (Transfer of business to UBS AG London Branch), p.89 - " + AR2025_URL + "\n"
    "FY2023/FY2022: Full accounts to 31 Dec 2023, Note 11 (Loans and advances, by UK/Foreign x "
    "Commercial/Consumer), p.58 - " + AR2023_URL + "\n"
    "FY2021: Full accounts to 31 Dec 2021, Note 11 (Loans and advances, by UK/Foreign x "
    "Commercial/Consumer), p.64 - " + AR2021_URL + "\n"
    "FY2020: Full accounts to 31 Dec 2020, Note 15 (Loans and advances, by UK/Foreign x "
    "Commercial/Consumer), p.68 - " + AR2020_URL + "\n"
    "FY2019: Full accounts to 31 Dec 2019, Note 15 (Net Loans, by UK/Foreign x Commercial/Consumer), "
    "p.64 - " + AR2019_URL + "\n"
    "FY2018: borrower-type breakdown and Gross Impaired loans sourced from the FY2019 filing's own FY2018 "
    "comparative column (p.64, same document as above) - FY2018's own filing (Note 16, p.71) discloses only "
    "a by-maturity/by-collateral breakdown with no borrower-type split and no impaired-loans concept; both "
    "years' totals independently reconcile to FY2018's own disclosed Total Net loans of £2,141,288k.\n"
    "FY2017: Full accounts to 31 Dec 2017, Note 13 (Loans and receivables, by UK/Foreign x "
    "Commercial/Consumer), p.47 - " + AR2017_URL + "\n"
    "FY2016: borrower-type/maturity/collateral breakdown from FY2016's own filing, Note 13, p.43 - "
    + AR2016_URL + "; Gross Impaired loans for FY2016 (£13,996k) sourced instead from FY2017's own FY2016 "
    "comparative column (same Note 13 above), since FY2016's own filing carries no impaired-loans concept "
    "either.\n\n"
    "GRANULARITY NOTE: the Bank's own disclosed granularity genuinely changes across years, confirmed by "
    "reading each year's own note in full (not assumed). FY2025/FY2024 use a full IFRS 9 Stage 1/2/3 "
    "gross-carrying-amount/allowance table (the format introduced from the FY2025 Annual Report) - note this "
    "is a DIFFERENT, secondary note from the primary 'Loans and advances' note that FY2019/FY2020 (and, per "
    "their own comparative columns, FY2016-FY2018) also carry: that secondary Stage 1/2/3 table exists "
    "inside the Expected Credit Loss Measurement note from FY2019 onward, but the Balance Sheet's own Loans "
    "and advances figure ties to the primary UK/Foreign x Commercial/Consumer note, not the Stage table - so "
    "FY2019/FY2020 are shown on the same borrower-type basis as FY2016-FY2023, not switched to a Stage "
    "basis. FY2023/FY2022/FY2021 instead disclose a UK-vs-Foreign, Commercial-vs-Consumer breakdown plus a "
    "single aggregate allowance figure and a 'Gross Impaired loans' total (the FY2023-and-earlier report "
    "format, confirmed the SAME format used continuously back to FY2016) - no Stage 1/2/3 split exists in "
    "the primary note for any of FY2016-FY2023 despite checking. Both are shown on their own basis "
    "rather than forced onto one; the FY2024 Stage-table's net figure (£820,752k = £829,923k gross less "
    "£9,171k ECL allowance) is £1,803k higher than the Balance Sheet's own £818,949k net Loans and advances "
    "figure for that year - the Stage table tracks ECL only, not the further 'Deferred fee income' "
    "deduction the FY2023/2022/2021 Note 11 shows separately (£4,043k/£6,449k/£7,733k respectively), which "
    "plausibly accounts for the FY2024 gap too even though it isn't separately disclosed that year - flagged "
    "as a probable explanation, not force-reconciled. FY2025's entire loan book (customer-facing business) "
    "was transferred to UBS AG London Branch on 20 June 2025 under a Part VII scheme (Note 35) - all FY2025 "
    "figures on this sheet are correctly nil, not a disclosure gap."
)

RWA_BREAKDOWN_SOURCES = (
    "CORRECTION (fresh re-verification, 2026-09-12): the prior version of this sheet claimed no category-level "
    "RWA breakdown was disclosed in any year, based only on a check of the Companies House Annual Report "
    "filings. That check was incomplete - a standalone Pillar 3 disclosure document for this entity DOES exist "
    "(UBS-hosted, since UBS's acquisition of Credit Suisse), and it carries a full risk-category RWA breakdown "
    "for FY2021-FY2025 (FY2016-FY2020 remain genuinely undisclosed - no standalone Pillar 3 document for this "
    "entity has been found for those years, consistent with the existing CET1/Tier 1/Total RWAs sheets' own "
    "source notes).\n\n"
    "Sources - Credit Suisse (UK) Limited Pillar 3 Disclosures, £'000s, each year's own originally-published "
    "figures used as primary (not a later restated comparative), per project convention:\n"
    "FY2025: Pillar 3 Disclosures 2025, 'OV1 - Overview of risk weighted exposure amounts', p.18 - "
    "https://www.ubs.com/global/en/investor-relations/complementary-financial-information/other-subsidiaries.html "
    "(csuk-pillar-3-disclosures-2026.pdf)\n"
    "FY2024: Pillar 3 Disclosures 2024, 'OV1 - Overview of risk weighted exposure amounts', p.26 - same page "
    "(csuk-pillar-3-disclosures-2024.pdf)\n"
    "FY2023: sourced from the FY2024 Pillar 3 Disclosures' own FY2023 comparative column (same table/page) - "
    "FY2023's own standalone Pillar 3 document was not located separately.\n"
    "FY2022: Pillar 3 Disclosures 2022, 'OV1 - Overview of risk weighted exposure amounts' - "
    "https://www.ubs.com/global/en/investor-relations/complementary-financial-information/disclosure-legal-"
    "entities/archive-credit-suisse.html (csuk-pillar-3-disclosures-2022.pdf)\n"
    "FY2021: Pillar 3 Disclosures 2021, 'RWA and Capital Requirements' table (pre-dates the OV1 template/label, "
    "same underlying disclosure, broken down further by credit-risk exposure class) - same archive page "
    "(2021-csuk-pillar-3-disclosures.pdf)\n\n"
    "Every year's Total ties to the Total RWAs sheet's own figure (to the nearest £m). FY2021's own document "
    "uses an older, pre-OV1 layout (exposure-class detail within credit risk; three summary lines 'Total credit "
    "and counterparty credit risk' / 'Total market risk' / 'Total other risks') rather than the UK OV1 template "
    "used from FY2022 onward - shown here collapsed to the three summary lines for consistency, with a "
    "£3k Settlement risk line disclosed only in FY2022 (immaterial, included in that year's Total). No separate "
    "Market risk RWA line is disclosed for FY2022/FY2024 (each document's own notes state there is no market "
    "risk RWA those years, non-GBP FX exposure below the 2%-of-capital threshold) - left blank rather than "
    "forced to zero, consistent with each year's own template only carrying the rows it actually discloses.\n\n"
    "FY2016-FY2020: not publicly disclosed - confirmed by reading each year's Annual Report in full (all "
    "numbered notes through to the final note in each filing), plus the existing Pillar 3 KPI-table sourcing "
    "already used for the CET1/Tier 1/Total RWAs/Leverage/LCR/NSFR sheets. No 'Capital Adequacy' note with an "
    "RWA category breakdown exists in any of these Companies House filings, and no standalone Pillar 3 document "
    "for this entity has been found covering these years."
)

bw = BankWorkbook(bank_name="Credit Suisse (UK) Limited", years=YEARS, year_label=YEAR_LABEL, header_color="50B633")

# ---------------------------------------------------------------
# Sheet: Balance Sheet
# ---------------------------------------------------------------
balance_sheet_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and cash equivalents / cash and due from banks",
     {"FY2025": 21709, "FY2024": 341768, "FY2023": 548659, "FY2022": 475664, "FY2021": 408064,
      "FY2020": 483710, "FY2019": 447805, "FY2018": 197292, "FY2017": 499549, "FY2016": 432924}),
    ("DATA", "Interest-bearing deposits with banks",
     {"FY2024": 25335, "FY2023": 17198, "FY2022": 48748,
      "FY2020": 187482, "FY2019": 39941, "FY2018": 74910, "FY2017": 4885, "FY2016": 75528}),
    ("DATA", "Securities purchased under resale agreements",
     {"FY2025": 328684, "FY2024": 565944, "FY2023": 455796, "FY2022": 562004, "FY2021": 1048198,
      "FY2020": 880396, "FY2019": 810044, "FY2018": 1033715, "FY2017": 601879, "FY2016": 829694}),
    ("DATA", "Trading financial assets mandatorily at FVTPL",
     {"FY2024": 13944, "FY2023": 13630, "FY2022": 18813, "FY2021": 14333,
      "FY2020": 35146, "FY2019": 8309, "FY2018": 5993, "FY2017": 8643, "FY2016": 16332}),
    ("DATA", "Financial assets available for sale",
     {"FY2018": 0, "FY2017": 2326, "FY2016": 2010}),
    ("DATA", "Loans and advances, net",
     {"FY2024": 818949, "FY2023": 1307573, "FY2022": 1706528, "FY2021": 2041139,
      "FY2020": 1990006, "FY2019": 2126766, "FY2018": 2141288, "FY2017": 2166554, "FY2016": 1547855}),
    ("DATA", "Current tax assets",
     {"FY2025": 38, "FY2024": 3057, "FY2023": 2058,
      "FY2019": 0, "FY2018": 287, "FY2017": 274, "FY2016": 287}),
    ("DATA", "Other assets",
     {"FY2025": 2097, "FY2024": 32158, "FY2023": 46419, "FY2022": 56795, "FY2021": 48352,
      "FY2020": 46609, "FY2019": 25239, "FY2018": 24309, "FY2017": 24078, "FY2016": 19010}),
    ("DATA", "Deferred tax assets",
     {"FY2022": 3304, "FY2021": 5041,
      "FY2020": 4919, "FY2019": 5364, "FY2018": 6603, "FY2017": 7803, "FY2016": 1750}),
    ("DATA", "Intangible assets",
     {"FY2023": 1137, "FY2022": 13933, "FY2021": 14044,
      "FY2020": 12675, "FY2019": 6760, "FY2018": 4195, "FY2017": 4993, "FY2016": 7222}),
    ("DATA", "Goodwill",
     {"FY2020": 13752, "FY2019": 13752, "FY2018": 13752, "FY2017": 13752, "FY2016": 13752}),
    ("TOTAL", "Total assets",
     {"FY2025": 352528, "FY2024": 1801155, "FY2023": 2392470, "FY2022": 2885789, "FY2021": 3579171,
      "FY2020": 3654695, "FY2019": 3483980, "FY2018": 3502344, "FY2017": 3334736, "FY2016": 2946364}),

    ("SECTION", "Liabilities", {}),
    ("DATA", "Deposits",
     {"FY2025": 27218, "FY2024": 548119, "FY2023": 654960, "FY2022": 1094750, "FY2021": 3118581,
      "FY2020": 3183065, "FY2019": 3040602, "FY2018": 3087177, "FY2017": 2990492, "FY2016": 2635334}),
    ("DATA", "Trading financial liabilities mandatorily at FVTPL",
     {"FY2024": 13849, "FY2023": 13496, "FY2022": 18613, "FY2021": 14023,
      "FY2020": 34940, "FY2019": 8073, "FY2018": 5784, "FY2017": 8087, "FY2016": 15844}),
    ("DATA", "Current income tax liability",
     {"FY2025": 6238, "FY2022": 7676, "FY2021": 4747,
      "FY2020": 2267, "FY2019": 16460, "FY2018": 22549, "FY2017": 16176, "FY2016": 2948}),
    ("DATA", "Other liabilities",
     {"FY2025": 3610, "FY2024": 26128, "FY2023": 43883, "FY2022": 34128, "FY2021": 32883,
      "FY2020": 36824, "FY2019": 38999, "FY2018": 34100, "FY2017": 37319, "FY2016": 36497}),
    ("DATA", "Provisions",
     {"FY2024": 1388, "FY2023": 1403, "FY2022": 713, "FY2021": 2709,
      "FY2020": 1426, "FY2019": 1903, "FY2018": 444, "FY2017": 19818, "FY2016": 22247}),
    ("DATA", "Short-term borrowings",
     {"FY2025": 9661, "FY2024": 857231, "FY2023": 831176, "FY2022": 827333}),
    ("DATA", "Long term debt",
     {"FY2024": 55000, "FY2023": 555000, "FY2022": 556890, "FY2021": 55000,
      "FY2020": 55000, "FY2019": 55000, "FY2018": 55000, "FY2017": 25000, "FY2016": 25000}),
    ("TOTAL", "Total liabilities",
     {"FY2025": 46727, "FY2024": 1501715, "FY2023": 2099918, "FY2022": 2540103, "FY2021": 3227943,
      "FY2020": 3313522, "FY2019": 3161037, "FY2018": 3205054, "FY2017": 3096892, "FY2016": 2737870}),

    ("SECTION", "Shareholders' equity", {}),
    ("DATA", "Share capital",
     {"FY2025": 245230, "FY2024": 245230, "FY2023": 245230, "FY2022": 245230, "FY2021": 245230,
      "FY2020": 245230, "FY2019": 245230, "FY2018": 245230, "FY2017": 245230, "FY2016": 245230}),
    ("DATA", "Share premium",
     {"FY2025": 11200, "FY2024": 11200, "FY2023": 11200, "FY2022": 11200, "FY2021": 11200,
      "FY2020": 11200, "FY2019": 11200, "FY2018": 11200, "FY2017": 11200, "FY2016": 11200}),
    ("DATA", "Capital contribution",
     {"FY2025": 27500, "FY2024": 27500, "FY2023": 27500, "FY2022": 57500, "FY2021": 57500,
      "FY2020": 57500, "FY2019": 57500, "FY2018": 57500, "FY2017": 27500, "FY2016": 27500}),
    ("DATA", "Accumulated other comprehensive income (AOCI, available-for-sale reserve)",
     {"FY2018": 0, "FY2017": 2289, "FY2016": 1973}),
    ("DATA", "Retained earnings",
     {"FY2025": 21871, "FY2024": 15510, "FY2023": 8622, "FY2022": 31756, "FY2021": 37298,
      "FY2020": 27243, "FY2019": 9013, "FY2018": -16640, "FY2017": -48375, "FY2016": -77409}),
    ("TOTAL", "Total shareholders' equity",
     {"FY2025": 305801, "FY2024": 299440, "FY2023": 292552, "FY2022": 345686, "FY2021": 351228,
      "FY2020": 341173, "FY2019": 322943, "FY2018": 297290, "FY2017": 237844, "FY2016": 208494}),
    ("TOTAL", "Total liabilities and shareholders' equity",
     {"FY2025": 352528, "FY2024": 1801155, "FY2023": 2392470, "FY2022": 2885789, "FY2021": 3579171,
      "FY2020": 3654695, "FY2019": 3483980, "FY2018": 3502344, "FY2017": 3334736, "FY2016": 2946364}),
]

bw.add_balance_sheet_sheet(
    title="Credit Suisse (UK) Limited — Statement of Financial Position",
    subtitle="Entity basis, £'000. See source note at bottom.",
    rows=balance_sheet_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=88,
    source_height=380,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Sheet: Profit & Loss
# ---------------------------------------------------------------
income_statement_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest income",
     {"FY2025": 42437, "FY2024": 124113, "FY2023": 156430, "FY2022": 88830, "FY2021": 56275,
      "FY2020": 74605, "FY2019": 94730, "FY2018": 85631, "FY2017": 65517, "FY2016": 49992}),
    ("DATA", "Interest expense",
     {"FY2025": -18060, "FY2024": -73480, "FY2023": -94427, "FY2022": -28065, "FY2021": -5122,
      "FY2020": -10829, "FY2019": -23571, "FY2018": -16701, "FY2017": -7865, "FY2016": -6574}),
    ("TOTAL", "Net interest income",
     {"FY2025": 24377, "FY2024": 50633, "FY2023": 62003, "FY2022": 60765, "FY2021": 51153,
      "FY2020": 63776, "FY2019": 71159, "FY2018": 68930, "FY2017": 57652, "FY2016": 43418}),
    ("DATA", "Commission and fee income",
     {"FY2025": 18904, "FY2024": 31922, "FY2023": 42185, "FY2022": 54048, "FY2021": 55219,
      "FY2020": 52104, "FY2019": 57538, "FY2018": 58533, "FY2017": 57734, "FY2016": 48959}),
    ("DATA", "Commission and fee expense",
     {"FY2025": -79, "FY2024": -737, "FY2023": -472, "FY2022": -740, "FY2021": -1068,
      "FY2020": -1593, "FY2019": -2107, "FY2018": -3746, "FY2017": -3197, "FY2016": -2009}),
    ("TOTAL", "Net commission and fee income",
     {"FY2025": 18825, "FY2024": 31185, "FY2023": 41713, "FY2022": 53308, "FY2021": 54151,
      "FY2020": 50511, "FY2019": 55431, "FY2018": 54787, "FY2017": 54537, "FY2016": 46950}),
    ("DATA", "Reversal of/(allowance for) expected credit losses",
     {"FY2025": 489, "FY2024": -1526, "FY2023": -3167, "FY2022": -1754, "FY2021": 2571,
      "FY2020": -2441, "FY2019": -4913, "FY2018": 214}),
    ("DATA", "Net gain from financial assets/liabilities at FVTPL",
     {"FY2025": 63, "FY2024": 151, "FY2023": 88, "FY2022": 172, "FY2021": 195,
      "FY2020": 200, "FY2019": -219, "FY2018": 1081}),
    ("DATA", "Loss from business transfer", {"FY2025": -1278}),
    ("DATA", "Other revenue and foreign exchange fluctuations",
     {"FY2025": 5331, "FY2024": 2302, "FY2023": 271, "FY2022": -8, "FY2021": -196,
      "FY2020": 873, "FY2019": 1772, "FY2018": 393, "FY2017": 28486, "FY2016": 544}),
    ("TOTAL", "Net revenue",
     {"FY2025": 47807, "FY2024": 82745, "FY2023": 100908, "FY2022": 112483, "FY2021": 107874,
      "FY2020": 112919, "FY2019": 123230, "FY2018": 125405, "FY2017": 140675, "FY2016": 90912}),

    ("SECTION", "Operating expenses", {}),
    ("DATA", "Compensation and benefits",
     {"FY2025": -11338, "FY2024": -36643, "FY2023": -42927, "FY2022": -39202, "FY2021": -41686,
      "FY2020": -47982, "FY2019": -51599, "FY2018": -49507, "FY2017": -52496, "FY2016": -49408}),
    ("DATA", "General and administrative expenses",
     {"FY2025": -26666, "FY2024": -35298, "FY2023": -84180, "FY2022": -51860, "FY2021": -41529,
      "FY2020": -39770, "FY2019": -37050, "FY2018": -36018, "FY2017": -51968, "FY2016": -40306}),
    ("DATA", "Impairment on goodwill", {"FY2021": -13752}),
    ("TOTAL", "Total operating expenses",
     {"FY2025": -38004, "FY2024": -71941, "FY2023": -127107, "FY2022": -91062, "FY2021": -96967,
      "FY2020": -87752, "FY2019": -88649, "FY2018": -85525, "FY2017": -104464, "FY2016": -89714}),

    ("TOTAL", "Profit/(loss) before tax",
     {"FY2025": 9803, "FY2024": 10804, "FY2023": -26199, "FY2022": 21421, "FY2021": 10907,
      "FY2020": 25167, "FY2019": 34581, "FY2018": 39880, "FY2017": 36211, "FY2016": 1198}),
    ("DATA", "Income tax benefit/(expense)",
     {"FY2025": -3442, "FY2024": -3916, "FY2023": 3065, "FY2022": -6963, "FY2021": -852,
      "FY2020": -5506, "FY2019": -8928, "FY2018": -10680, "FY2017": -7177, "FY2016": -1642}),
    ("TOTAL", "Profit/(loss) after tax",
     {"FY2025": 6361, "FY2024": 6888, "FY2023": -23134, "FY2022": 14458, "FY2021": 10055,
      "FY2020": 19661, "FY2019": 25653, "FY2018": 29200, "FY2017": 29034, "FY2016": -444}),
    ("TOTAL", "Total comprehensive income/(loss) for the year",
     {"FY2025": 6361, "FY2024": 6888, "FY2023": -23134, "FY2022": 14458, "FY2021": 10055,
      "FY2020": 19661, "FY2019": 25653, "FY2018": 29200, "FY2017": 29350, "FY2016": -129}),
]

bw.add_income_statement_sheet(
    title="Credit Suisse (UK) Limited — Statement of Income",
    subtitle="Entity basis, £'000. No items of other comprehensive income FY2019 onward; FY2016-FY2018 "
              "carry a small available-for-sale-reserve OCI movement (+£315k/+£316k/£0k) reflected in the "
              "'Total comprehensive income' row only. See source note at bottom.",
    rows=income_statement_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=88,
    source_height=380,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Sheet: Statement of Changes in Equity
# ---------------------------------------------------------------
equity_headers = ["Share capital", "Share premium", "Capital contribution", "AOCI (available-for-sale reserve)",
                   "Retained earnings", "Total equity"]
equity_rows = [
    ("TOTAL", "At 1 January 2016", (245230, 11200, 27500, 1658, -76965, 208623)),
    ("DATA", "Total comprehensive loss for the year (FY2016)", (None, None, None, 315, -444, -129)),
    ("TOTAL", "At 31 December 2016", (245230, 11200, 27500, 1973, -77409, 208494)),
    ("DATA", "Total comprehensive income for the year (FY2017)", (None, None, None, 316, 29034, 29350)),
    ("TOTAL", "At 31 December 2017", (245230, 11200, 27500, 2289, -48375, 237844)),
    ("DATA", "IFRS 9 initial-application adjustment (net of tax, 1 Jan 2018)",
     (None, None, None, -2289, 2535, 246)),
    ("TOTAL", "Adjusted balance at 1 January 2018", (245230, 11200, 27500, 0, -45840, 238090)),
    ("DATA", "Total comprehensive income for the year (FY2018)", (None, None, None, None, 29200, 29200)),
    ("DATA", "Contribution to Capital reserve (FY2018)", (None, None, 30000, None, None, 30000)),
    ("TOTAL", "At 31 December 2018", (245230, 11200, 57500, 0, -16640, 297290)),
    ("DATA", "Total comprehensive income for the year (FY2019, as originally reported)",
     (None, None, None, None, 25653, 25653)),
    ("TOTAL", "At 31 December 2019 (as originally reported)", (245230, 11200, 57500, 0, 9013, 322943)),
    ("DATA", "Correction of error, net of tax (per FY2020's own filing, not otherwise explained)",
     (None, None, None, None, -1431, -1431)),
    ("TOTAL", "Restated balance at 1 January 2020", (245230, 11200, 57500, 0, 7582, 321512)),
    ("DATA", "Total comprehensive income for the year (FY2020)", (None, None, None, None, 19661, 19661)),
    ("TOTAL", "At 31 December 2020", (245230, 11200, 57500, 0, 27243, 341173)),
    ("TOTAL", "At 1 January 2021", (245230, 11200, 57500, None, 27243, 341173)),
    ("DATA", "Total comprehensive income for the year (FY2021)", (None, None, None, None, 10055, 10055)),
    ("TOTAL", "At 31 December 2021", (245230, 11200, 57500, None, 37298, 351228)),
    ("DATA", "Total comprehensive income for the year (FY2022)", (None, None, None, None, 14458, 14458)),
    ("DATA", "Dividend paid (FY2022)", (None, None, None, None, -20000, -20000)),
    ("TOTAL", "At 31 December 2022", (245230, 11200, 57500, None, 31756, 345686)),
    ("DATA", "Total comprehensive loss for the year (FY2023)", (None, None, None, None, -23134, -23134)),
    ("DATA", "Dividend paid (FY2023)", (None, None, -30000, None, None, -30000)),
    ("TOTAL", "At 31 December 2023", (245230, 11200, 27500, None, 8622, 292552)),
    ("DATA", "Total comprehensive income for the year (FY2024)", (None, None, None, None, 6888, 6888)),
    ("TOTAL", "At 31 December 2024", (245230, 11200, 27500, None, 15510, 299440)),
    ("DATA", "Total comprehensive income for the year (FY2025)", (None, None, None, None, 6361, 6361)),
    ("TOTAL", "At 31 December 2025", (245230, 11200, 27500, None, 21871, 305801)),
]

bw.add_equity_changes_sheet(
    title="Credit Suisse (UK) Limited — Statement of Changes in Equity",
    subtitle="£'000, chronological, FY2016-FY2025. Every year's closing balance ties exactly to the Balance "
              "Sheet's own Total shareholders' equity and to the next year's own opening balance - no plug "
              "row needed, aside from the two explicit bridging rows (IFRS 9 initial application and the "
              "FY2020 correction of error) which are themselves fully disclosed movements, not plugs. AOCI "
              "(an available-for-sale reserve) only exists FY2016-FY2018 - blank thereafter, not zero, since "
              "it stops being a distinct line item rather than being drawn down to nil. See source note at "
              "bottom.",
    headers=equity_headers,
    rows=equity_rows,
    sources_text=STATEMENTS_SOURCES,
)

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Profit/(loss) before tax for the year",
     {"FY2025": 9803, "FY2024": 10804, "FY2023": -26199, "FY2022": 21421, "FY2021": 10907,
      "FY2020": 25167, "FY2019": 34581, "FY2018": 39880, "FY2017": 36211, "FY2016": 1198}),
    ("DATA", "Loss from the business transfer", {"FY2025": 1278}),
    ("DATA", "Amortisation and impairment of intangible assets",
     {"FY2024": 1137, "FY2023": 13582, "FY2022": 3566, "FY2021": 1852,
      "FY2020": 952, "FY2019": 1416, "FY2018": 3265, "FY2017": 3168, "FY2016": 3168}),
    ("DATA", "Impairment on goodwill", {"FY2021": 13752}),
    ("DATA", "Gain on sale of financial assets, net of withholding tax", {"FY2018": -542}),
    ("DATA", "Accrued interest on long term debt",
     {"FY2025": 1836, "FY2024": 14677, "FY2023": 34049, "FY2022": 12300, "FY2021": 1635,
      "FY2020": 1794, "FY2019": 2008, "FY2018": 720, "FY2017": 860, "FY2016": 909}),
    ("DATA", "Accrued interest on short-term borrowings",
     {"FY2025": 12765, "FY2024": 40087, "FY2023": 44712, "FY2022": 8822}),
    ("DATA", "Deferred fee income on loans",
     {"FY2025": -499, "FY2024": -2784, "FY2023": -3102, "FY2022": -3821}),
    ("DATA", "Foreign exchange (gain)/loss",
     {"FY2025": -2005, "FY2024": -1583, "FY2023": 1721, "FY2022": -2954, "FY2021": -1339,
      "FY2020": -6037, "FY2019": 9943, "FY2018": -13, "FY2017": 12, "FY2016": -41}),
    ("DATA", "Share based Compensation (charge)/reversal",
     {"FY2024": -385, "FY2023": 394, "FY2022": -40}),
    ("DATA", "Allowance for expected credit losses (ECL)",
     {"FY2025": -489, "FY2024": 1526, "FY2023": 3094, "FY2022": 1754, "FY2021": -2571,
      "FY2020": 2441, "FY2019": 4913, "FY2018": -214}),
    ("TOTAL", "Cash generated before changes in operating assets and liabilities",
     {"FY2025": 22689, "FY2024": 63479, "FY2023": 68251, "FY2022": 41048, "FY2021": 24236,
      "FY2020": 24317, "FY2019": 52861, "FY2018": 43096, "FY2017": 40251, "FY2016": 5234}),
    ("DATA", "Securities purchased under resale agreements",
     {"FY2025": 237260, "FY2024": -110148, "FY2023": 106208, "FY2022": 486194, "FY2021": -167802,
      "FY2020": -70352, "FY2019": 223671, "FY2018": -431836, "FY2017": 227815, "FY2016": -11756}),
    ("DATA", "Trading financial assets mandatorily at fair value through profit or loss",
     {"FY2025": 13944, "FY2024": -314, "FY2023": 5183, "FY2022": -4480, "FY2021": 20813,
      "FY2020": -26837, "FY2019": -2316, "FY2018": 2650, "FY2017": 7689, "FY2016": 8665}),
    ("DATA", "Loans and advances",
     {"FY2025": -39272, "FY2024": 489850, "FY2023": 398930, "FY2022": 336715, "FY2021": -48586,
      "FY2020": 134342, "FY2019": 9605, "FY2018": 25862, "FY2017": -618699, "FY2016": -224159}),
    ("DATA", "Interest bearing deposits with banks (excluding ECL)",
     {"FY2025": 25338, "FY2024": -8136, "FY2023": 31552, "FY2022": -48754, "FY2021": 187491,
      "FY2020": -147539, "FY2019": 34968, "FY2018": -28461, "FY2017": 70643, "FY2016": -27166}),
    ("DATA", "Other assets",
     {"FY2025": 17904, "FY2024": 13274, "FY2023": 8322, "FY2022": -8451, "FY2021": -1141,
      "FY2020": -13605, "FY2019": -923, "FY2018": -266, "FY2017": -5068, "FY2016": -1161}),
    ("TOTAL", "Net decrease/(increase) in operating assets",
     {"FY2025": 255174, "FY2024": 384526, "FY2023": 550195, "FY2022": 761224, "FY2021": -9225,
      "FY2020": -123991, "FY2019": 265005, "FY2018": -432051, "FY2017": -317620, "FY2016": -255577}),
    ("DATA", "Deposits",
     {"FY2025": -195682, "FY2024": -106841, "FY2023": -439790, "FY2022": -517522, "FY2021": -64484,
      "FY2020": 142463, "FY2019": -46575, "FY2018": 96685, "FY2017": 355158, "FY2016": 298670}),
    ("DATA", "Trading financial liabilities mandatorily at fair value through profit or loss",
     {"FY2025": -13849, "FY2024": 353, "FY2023": -5117, "FY2022": 4590, "FY2021": -20917,
      "FY2020": 26867, "FY2019": 2289, "FY2018": -2303, "FY2017": -7757, "FY2016": -8215}),
    ("DATA", "Share based compensation", {"FY2024": -220, "FY2023": -1774, "FY2022": -3649}),
    ("DATA", "Other liabilities and provisions",
     {"FY2025": -14841, "FY2024": -15915, "FY2023": 11963, "FY2022": 1266, "FY2021": -2672,
      "FY2020": -4447, "FY2019": 6358, "FY2018": -22636, "FY2017": -1601, "FY2016": 17612}),
    ("TOTAL", "Net decrease/(increase) in operating liabilities",
     {"FY2025": -224372, "FY2024": -122623, "FY2023": -434718, "FY2022": -515315, "FY2021": -88073,
      "FY2020": 164883, "FY2019": -37928, "FY2018": 71746, "FY2017": 345800, "FY2016": 308067}),
    ("DATA", "Income tax refunded/(paid)", {"FY2024": 119, "FY2021": 1101, "FY2020": -10662}),
    ("DATA", "Group relief received/(paid)",
     {"FY2025": 6127, "FY2024": -4800, "FY2023": -3319, "FY2022": -2522, "FY2021": 406,
      "FY2020": -8186, "FY2019": -13495, "FY2018": -3189, "FY2016": -266}),
    ("TOTAL", "Net cash flow generated from/(used in) operating activities",
     {"FY2025": 59618, "FY2024": 320701, "FY2023": 180409, "FY2022": 284435, "FY2021": -71555,
      "FY2020": 46361, "FY2019": 266443, "FY2018": -320398, "FY2017": 68431, "FY2016": 57458}),

    ("SECTION", "Investing activities", {}),
    ("DATA", "Cash receipt from business transfer", {"FY2025": 539843}),
    ("DATA", "Sale of financial assets", {"FY2018": 2868}),
    ("DATA", "Capital expenditures for intangible assets",
     {"FY2023": -786, "FY2022": -3455, "FY2021": -3799,
      "FY2020": -6867, "FY2019": -3981, "FY2018": -2467, "FY2017": -939}),
    ("TOTAL", "Net cash flow generated from/(used in) investing activities",
     {"FY2025": 539843, "FY2024": 0, "FY2023": -786, "FY2022": -3455, "FY2021": -3799,
      "FY2020": -6867, "FY2019": -3981, "FY2018": 401, "FY2017": -939, "FY2016": 0}),

    ("SECTION", "Financing activities", {}),
    ("DATA", "Dividend paid", {"FY2023": -30000, "FY2022": -20000}),
    ("DATA", "Interest paid on long term debt",
     {"FY2025": -1916, "FY2024": -15460, "FY2023": -33420, "FY2022": -12293, "FY2021": -1620,
      "FY2020": -1843, "FY2019": -2008, "FY2018": -677, "FY2017": -867, "FY2016": -920}),
    ("DATA", "Capital contribution", {"FY2018": 30000}),
    ("DATA", "Issuance of long term debt", {"FY2023": 530803, "FY2022": 500000, "FY2018": 30000}),
    ("DATA", "Repayment of long term debt",
     {"FY2025": -55000, "FY2024": -500000, "FY2023": -532693, "FY2022": -503689}),
    ("DATA", "Interest paid on short-term borrowings",
     {"FY2025": -17039, "FY2024": -39775, "FY2023": -43476, "FY2022": -6928}),
    ("DATA", "Issuance of short-term borrowings",
     {"FY2025": 12865, "FY2024": 713897, "FY2023": 601802, "FY2022": 615993}),
    ("DATA", "Repayment of short-term borrowings",
     {"FY2025": -845507, "FY2024": -689448, "FY2023": -575110, "FY2022": -824808}),
    ("TOTAL", "Net cash flow used in financing activities",
     {"FY2025": -906597, "FY2024": -530786, "FY2023": -82094, "FY2022": -251725, "FY2021": -1620,
      "FY2020": -1843, "FY2019": -2008, "FY2018": 59323, "FY2017": -867, "FY2016": -920}),

    ("TOTAL", "Net (decrease)/increase in cash and cash equivalents",
     {"FY2025": -307136, "FY2024": -210085, "FY2023": 97529, "FY2022": 29255, "FY2021": -76974,
      "FY2020": 37651, "FY2019": 260454, "FY2018": -260674, "FY2017": 66625, "FY2016": 56538}),
    ("DATA", "Cash and cash equivalents at the beginning of the year",
     {"FY2025": 341768, "FY2024": 548659, "FY2023": 475664, "FY2022": 408082, "FY2021": 483717,
      "FY2020": 440029, "FY2019": 197301, "FY2018": 457975, "FY2017": 432924, "FY2016": 376386}),
    ("DATA", "Effect of exchange rate fluctuations on cash and cash equivalents",
     {"FY2025": -12923, "FY2024": 3194, "FY2023": -24570, "FY2022": 38372, "FY2021": 1339,
      "FY2020": 6037, "FY2019": -9939}),
    ("TOTAL", "Cash and cash equivalents at the end of the year",
     {"FY2025": 21709, "FY2024": 341768, "FY2023": 548659, "FY2022": 475709, "FY2021": 408082,
      "FY2020": 483717, "FY2019": 447816, "FY2018": 197301, "FY2017": 499549, "FY2016": 432924}),
]

bw.add_cash_flow_sheet(
    title="Credit Suisse (UK) Limited — Statement of Cash Flows",
    subtitle="Entity basis, £'000. See source note at bottom.",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=88,
    source_height=340,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Sheet: Asset Quality
# ---------------------------------------------------------------
asset_quality_rows = [
    ("SECTION", "Loan book by borrower type, gross (FY2016-FY2023 basis)", {}),
    ("DATA", "United Kingdom - Commercial",
     {"FY2023": 1069, "FY2022": 1556, "FY2021": 8891,
      "FY2020": 167719, "FY2019": 150011, "FY2018": 130738, "FY2017": 135735, "FY2016": 81404}),
    ("DATA", "United Kingdom - Consumer",
     {"FY2023": 612720, "FY2022": 791672, "FY2021": 940312,
      "FY2020": 653738, "FY2019": 775633, "FY2018": 824688, "FY2017": 862482, "FY2016": 619490}),
    ("DATA", "Foreign - Commercial",
     {"FY2023": 15870, "FY2022": 18896, "FY2021": 14577,
      "FY2020": 703004, "FY2019": 731631, "FY2018": 706545, "FY2017": 667395, "FY2016": 462233}),
    ("DATA", "Foreign - Consumer",
     {"FY2023": 689570, "FY2022": 905338, "FY2021": 1093926,
      "FY2020": 486568, "FY2019": 490607, "FY2018": 494104, "FY2017": 516087, "FY2016": 395082}),
    ("TOTAL", "Total gross loans and advances, by borrower type",
     {"FY2023": 1319229, "FY2022": 1717462, "FY2021": 2057706,
      "FY2020": 2011029, "FY2019": 2147882, "FY2018": 2156075, "FY2017": 2181699, "FY2016": 1558209}),

    ("SECTION", "Loan book by IFRS 9 stage, gross (FY2024-FY2025 basis)", {}),
    ("DATA", "Stage 1 - gross carrying amount", {"FY2025": 0, "FY2024": 630187}),
    ("DATA", "Stage 2 - gross carrying amount", {"FY2025": 0, "FY2024": 107024}),
    ("DATA", "Stage 3 - gross carrying amount", {"FY2025": 0, "FY2024": 92712}),
    ("TOTAL", "Total gross loans, IFRS 9 stage basis", {"FY2025": 0, "FY2024": 829923}),

    ("SECTION", "Expected credit loss allowance", {}),
    ("DATA", "Stage 1 allowance", {"FY2025": 0, "FY2024": -537}),
    ("DATA", "Stage 2 allowance", {"FY2025": 0, "FY2024": -342}),
    ("DATA", "Stage 3 allowance", {"FY2025": 0, "FY2024": -8292}),
    ("DATA", "Allowance for credit losses, aggregate (FY2016-FY2023 basis)",
     {"FY2023": -7613, "FY2022": -4485, "FY2021": -8834,
      "FY2020": -11381, "FY2019": -8963, "FY2018": -3244, "FY2017": -4495, "FY2016": -1768}),
    ("TOTAL", "Total ECL allowance",
     {"FY2025": 0, "FY2024": -9171, "FY2023": -7613, "FY2022": -4485, "FY2021": -8834,
      "FY2020": -11381, "FY2019": -8963, "FY2018": -3244, "FY2017": -4495, "FY2016": -1768}),
    ("DATA", "Deferred fee income",
     {"FY2023": -4043, "FY2022": -6449, "FY2021": -7733,
      "FY2020": -9642, "FY2019": -12153, "FY2018": -11543, "FY2017": -10650, "FY2016": -8586}),
    ("TOTAL", "Total Loans and advances, net (ties to Balance Sheet)",
     {"FY2025": 0, "FY2024": 818949, "FY2023": 1307573, "FY2022": 1706528, "FY2021": 2041139,
      "FY2020": 1990006, "FY2019": 2126766, "FY2018": 2141288, "FY2017": 2166554, "FY2016": 1547855}),

    ("SECTION", "Credit quality indicators", {}),
    ("DATA", "Gross impaired loans / Stage 3 gross carrying amount",
     {"FY2025": 0, "FY2024": 92712, "FY2023": 175850, "FY2022": 105926, "FY2021": 177499,
      "FY2020": 191569, "FY2019": 98031, "FY2018": 115146, "FY2017": 59686, "FY2016": 13996}),
    ("DATA", "Impaired/Stage 3 loans as % of total gross loans",
     {"FY2024": "11.17%", "FY2023": "13.33%", "FY2022": "6.17%", "FY2021": "8.63%",
      "FY2020": "9.53%", "FY2019": "4.56%", "FY2018": "5.34%", "FY2017": "2.74%", "FY2016": "0.90%"}),
    ("DATA", "ECL coverage of impaired/Stage 3 loans",
     {"FY2024": "8.94%", "FY2023": "4.33%", "FY2022": "4.23%", "FY2021": "4.98%",
      "FY2020": "5.94%", "FY2019": "9.14%", "FY2018": "2.82%", "FY2017": "7.53%", "FY2016": "12.63%"}),
]

bw.add_asset_quality_sheet(
    title="Credit Suisse (UK) Limited — Asset Quality",
    subtitle="Entity basis, £'000 unless %. Disclosed granularity genuinely changes across years - see "
              "source note at bottom. FY2025 loan book transferred to UBS AG London Branch (Part VII, 20 "
              "June 2025) - all FY2025 figures on this sheet are correctly nil.",
    rows=asset_quality_rows,
    sources_text=ASSET_QUALITY_SOURCES,
    first_col_width=70,
    source_height=340,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, unit, rows_data, sources_text, note=note, first_col_width=52, source_height=170)


def p3_sources(page_note=""):
    return (
        "Sources - Credit Suisse (UK) Limited's own Annual Report 'Key Performance Indicators (KPIs)' "
        "table.\n"
        "CORRECTED 18 September 2026 (KM1-032). This citation previously read '(no standalone Pillar 3 "
        "document was located for CSUK; the FY2025 Annual Report's own Strategic Report states \"Pillar 3 "
        "disclosures can be found separately at https://www.ubs.com/global/en/investor-relations\", but a "
        "CSUK-specific document was not identified there within budget - WebSearch quota was already "
        "exhausted)'. THAT WAS FALSE, and it is the clearest example in this workbook of a limit on our "
        "REACH being written down as a fact about the BANK: the sentence recorded that a search had run out "
        "of budget, and then read as though the document did not exist. Because p3_sources() is attached to "
        "every metric sheet, that one sentence shipped the claim across the whole workbook.\n"
        "CSUK publishes standalone, entity-level Pillar 3 disclosures, and THIS WORKBOOK ALREADY USES THEM: "
        "the KM1 Key Metrics sheet reproduces CSUK's own 'KM1 - Key metrics' template from the Pillar 3 "
        "Disclosures editions for 2022, 2023, 2024 and 2025 (see that sheet's citation, which names each "
        "edition, its printed folio and the filename trap whereby the 2025 edition is published as "
        "'csuk-pillar-3-disclosures-2026.pdf'), and the Total Capital and Total Capital Ratio sheets are "
        "sourced from those same editions' own-funds tables. The editions are reached from the Credit Suisse "
        "legal-entity disclosure index at " + CSUK_P3_INDEX_URL + " .\n"
        "THE UBS HOST IS REACHABLE - a correction to this note's own previous paragraph, recorded because "
        "it is the same class of error as the sentence above. That paragraph said that on 18 September "
        "2026 'both routes to those documents were unavailable to this session', the UBS host returning "
        "HTTP 403 with a 483-byte AkamaiGHost 'Access Denied' body 'which an ordinary browser User-Agent "
        "does not clear'. The observation was accurate; the inference was backwards. The 403 is caused BY "
        "the browser User-Agent, not cured by it. Later the same day, PLAIN curl with no added headers "
        "returned HTTP 200 and the full index page, and every CSUK Pillar 3 PDF then downloaded cleanly "
        "(Content-Type application/pdf, %PDF magic bytes). The lowest rung of the fetching ladder passes "
        "an edge rule that the highest rung trips. Five editions - 2019, 2020, 2021, 2022 and 2023 - were "
        "downloaded and read on that basis and now source the Leverage Ratio and LCR sheets.\n"
        "Sources by year:\n"
        "FY2025/FY2024: FY2025 Annual Report, KPI table p.6 - " + AR2025_URL + "\n"
        "FY2023/FY2022: FY2023 Annual Report, KPI table p.7 - " + AR2023_URL + "\n"
        "FY2021: FY2021 Annual Report, KPI table p.8 - " + AR2021_URL + "\n"
        "FY2020: FY2020 Annual Report, KPI table p.8 - " + AR2020_URL + "\n"
        "FY2019: FY2019 Annual Report, KPI table p.7 - " + AR2019_URL + "\n"
        "FY2018: FY2018 Annual Report, KPI table p.7 - " + AR2018_URL + "\n"
        "FY2017: FY2018 Annual Report's own FY2017 comparative column, p.7 (FY2017's own Annual Report "
        "carries no KPI table at all - only introduced from the FY2018 report) - " + AR2018_URL + "\n"
        "FY2016: no KPI table exists for FY2016 in any filing obtained, and no comparative column reaches "
        "back that far (FY2017's own report also lacks a KPI table) - RWA/CET1-Tier1 Ratio/Leverage/LCR/"
        "NSFR are self-skipped for FY2016 as genuinely undisclosed (see ENTITY NOTE); FY2016 CET1/Tier 1 "
        "Capital (£) is instead sourced from the Capital adequacy note's Own Funds table, FY2016 Annual "
        "Report p.88 - " + AR2016_URL + "\n"
        "FY2021-FY2023: CSUK official Pillar 3 disclosures hosted by UBS (KM1 / capital composition tables) - "
        "https://www.ubs.com/global/en/investor-relations/complementary-financial-information/disclosure-legal-entities/archive-credit-suisse.html\n"
        "FY2024-FY2025: CSUK official Pillar 3 disclosures hosted by UBS (KM1 / capital composition tables) - "
        "https://www.ubs.com/global/en/investor-relations/complementary-financial-information/other-subsidiaries.html\n"
        "FY2019-FY2023: CSUK standalone Pillar 3 editions, reached from the UBS-hosted Credit Suisse "
        "legal-entity ARCHIVE index - https://www.ubs.com/global/en/investor-relations/complementary-"
        "financial-information/disclosure-legal-entities/archive-credit-suisse.html - which lists one CSUK "
        "edition per year for 2014-2023. Each edition's own title carries the fiscal year ('Pillar 3 "
        "Disclosures 2019', '2020 Pillar 3 Disclosures', and so on), so the filename-year trap that "
        "affects the FY2025 edition does not arise for these. Editions 2014-2018 are listed on the same "
        "index and have NOT been opened by this workbook - a standing lead, not an absence.\n"
        + page_note
    )


CET1_TIER1_CAPITAL = {"FY2025": 306, "FY2024": 299, "FY2023": 291, "FY2022": 330, "FY2021": 336,
                       "FY2020": 314, "FY2019": 300, "FY2018": 276, "FY2017": 213, "FY2016": 186}
CET1_TIER1_RATIO = {"FY2025": "191%", "FY2024": "45%", "FY2023": "29.15%", "FY2022": "29.39%", "FY2021": "25.09%",
                     "FY2020": "22%", "FY2019": "21.9%", "FY2018": "22.5%", "FY2017": "17.2%"}
RWA = {"FY2025": 160, "FY2024": 672, "FY2023": 1000, "FY2022": 1124, "FY2021": 1340,
       "FY2020": 1338, "FY2019": 1371, "FY2018": 1225, "FY2017": 1241}
# FY2023-FY2019 added 2026-09-18 (interior-gap sweep, GA- series). Each year is
# the figure printed by THAT year's OWN CSUK standalone Pillar 3 edition - see
# LEVERAGE_INTERIOR_NOTE for the document, printed folio and the cross-edition
# restatements that are deliberately NOT applied.
LEVERAGE_RATIO = {"FY2025": "87%", "FY2024": "17%", "FY2023": "12.09%", "FY2022": "11.40%",
                  "FY2021": "9.30%", "FY2020": "8.07%", "FY2019": "8.47%",
                  "FY2018": "7.8%", "FY2017": "6.3%"}
# FY2021 added 2026-09-18 on the SPOT basis this row uses - see LCR_INTERIOR_NOTE.
LCR = {"FY2025": "1,154%", "FY2024": "451%", "FY2023": "554.67%", "FY2022": "216.40%",
       "FY2021": "216%", "FY2018": "154%"}
# Second, separately-labelled row on the LCR sheet: CSUK's own Pillar 3 12-month
# average LCR. NOT merged into the row above - the two are different measures and
# the Bank says so itself (2020 edition, p.21 footnote: "For the purpose of
# Pillar 3, the values are calculated as the simple average of the month-end
# observations over the preceding twelve months. The HQLA and LCR reported as at
# 31 December 2020 in CSUK Annual Report represents the spot value as of the
# reporting date."). This row is what fills FY2020 and FY2019, which have no
# published spot figure anywhere located.
LCR_P3_AVERAGE = {"FY2025": "4860.58%", "FY2024": "539.19%", "FY2023": "729.77%", "FY2022": "229.60%",
                  "FY2021": "230%", "FY2020": "300%", "FY2019": "246%"}
NSFR = {"FY2025": "3,600%", "FY2024": "167%", "FY2023": "129.25%", "FY2022": "131.72%"}

COMBINED_NOTE = (
    "The Bank's own KPI table discloses a single combined 'Tier 1 and Common Equity Tier 1 (CET1)' "
    "line, not separate Tier 1/CET1 figures - used identically for both the CET1 and Tier 1 sheets. FY2016's "
    "£ figure is the Capital adequacy note's 'Total Tier 1 (and CET1) capital' (£185,547k, rounded to £186m) "
    "- no ratio/RWA is available for FY2016 to pair with it (see ENTITY NOTE and p3_sources above)."
)

CSUK_P3_INDEX_URL = ("https://www.ubs.com/global/en/investor-relations/complementary-financial-information/"
                     "other-subsidiaries.html")

# ---------------------------------------------------------------
# UBS-hosted Credit Suisse legal-entity ARCHIVE index, and the CSUK standalone
# Pillar 3 editions reached from it. Enumerated directly on 2026-09-18 (interior-
# gap sweep) - the index's own table links, not guessed slugs. It lists a CSUK
# Pillar 3 edition for EVERY year 2014-2023 inclusive.
#
# FETCHING-LADDER NOTE, recorded because it inverts what this file previously
# said. On 2026-09-18 an earlier session recorded the UBS host as returning an
# AkamaiGHost 403 "Access Denied" and concluded the documents were unreachable.
# That is true ONLY of the browser-User-Agent rung: sending a Chrome UA (with or
# without --http1.1) still returns 403/530 bytes, while PLAIN `curl` with no
# added headers at all returns HTTP 200 and the full 552,569-byte index page,
# and each PDF below then downloads clean (HTTP 200, Content-Type
# application/pdf, %PDF magic bytes, 0.5-8 MB). The edge rule is evidently
# UA-based and the lower rung of the ladder passes it. Rung 1 (plain curl) is
# the one that works here; do not start at rung 4.
CSUK_P3_ARCHIVE_INDEX_URL = ("https://www.ubs.com/global/en/investor-relations/complementary-financial-"
                             "information/disclosure-legal-entities/archive-credit-suisse.html")
_UBS_DAM = ("https://www.ubs.com/global/en/investor-relations/complementary-financial-information/"
            "disclosure-legal-entities/archive-credit-suisse/_jcr_content/root/contentarea/mainpar/"
            "toplevelgrid_1145414446/col_1/accordionbox/")
P3_2019_URL = (_UBS_DAM + "accordionsplit_ba44/table.1211843275.file/dGFibGVUZXh0PS9jb250ZW50L2RhbS9hc3NldHMv"
               "Y2MvaW52ZXN0b3ItcmVsYXRpb25zL2NvbXBsZW1lbnRhcnktZmluYW5jaWFsLWluZm9ybWF0aW9uL2FyY2hpdmUvMjAx"
               "OS8yMDE5LWNzdWstcGlsbGFyLTMtZGlzY2xvc3VyZXMucGRm/2019-csuk-pillar-3-disclosures.pdf")
P3_2020_URL = (_UBS_DAM + "accordionsplit/table.670434488.file/dGFibGVUZXh0PS9jb250ZW50L2RhbS9hc3NldHMvY2Mv"
               "aW52ZXN0b3ItcmVsYXRpb25zL2NvbXBsZW1lbnRhcnktZmluYW5jaWFsLWluZm9ybWF0aW9uL2FyY2hpdmUvMjAyMC8y"
               "MDIwLWNzdWstcGlsbGFyLTMtZGlzY2xvc3VyZXMucGRm/2020-csuk-pillar-3-disclosures.pdf")
P3_2021_URL = (_UBS_DAM + "accordionsplit_794647952/table_1735174296.1230522569.file/dGFibGVUZXh0PS9jb250ZW50"
               "L2RhbS9hc3NldHMvY2MvaW52ZXN0b3ItcmVsYXRpb25zL2NvbXBsZW1lbnRhcnktZmluYW5jaWFsLWluZm9ybWF0aW9u"
               "L2FyY2hpdmUvMjAyMS8yMDIxLWNzdWstcGlsbGFyLTMtZGlzY2xvc3VyZXMucGRm/2021-csuk-pillar-3-"
               "disclosures.pdf")
P3_2022_URL = (_UBS_DAM + "accordionsplit_1343042181/innergrid/col_1/table.1831372465.file/dGFibGVUZXh0PS9jb"
               "250ZW50L2RhbS9hc3NldHMvY2MvaW52ZXN0b3ItcmVsYXRpb25zL2NvbXBsZW1lbnRhcnktZmluYW5jaWFsLWluZm9y"
               "bWF0aW9uL2FyY2hpdmUvMjAyMi9jc3VrLXBpbGxhci0zLWRpc2Nsb3N1cmVzLTIwMjIucGRm/csuk-pillar-3-"
               "disclosures-2022.pdf")
P3_2023_URL = (_UBS_DAM + "accordionsplit_485894160/table.1454258810.file/dGFibGVUZXh0PS9jb250ZW50L2RhbS9hc"
               "3NldHMvY2MvaW52ZXN0b3ItcmVsYXRpb25zL2NvbXBsZW1lbnRhcnktZmluYW5jaWFsLWluZm9ybWF0aW9uL2FyY2hp"
               "dmUvMjAyMy8yMDIzLWNzdWstcGlsbGFyLTMtZGlzY2xvc3VyZXMucGRm/2023-csuk-pillar-3-disclosures.pdf")

KM1_YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]

KM1_SOURCES = (
    "Sources - Credit Suisse (UK) Limited's own published 'KM1 - Key metrics' template, reproduced whole in "
    "the Bank's own row order, row numbers, labels and precision. All amounts are the template's own "
    "'Amounts in GBP '000'; ratios exactly as printed. Each edition is UBS-hosted and reached from the "
    "Credit Suisse legal-entity disclosure index - " + CSUK_P3_INDEX_URL + "\n"
    "FY2025: Pillar 3 Disclosures 2025, 'KM1 - Key metrics' (end-2025 column). NOTE THE FILENAME TRAP: this "
    "edition is published as 'csuk-pillar-3-disclosures-2026.pdf' - UBS names the file by publication year, "
    "while the document itself is titled 'Pillar 3 Disclosures 2025' and its column is headed 'end of 2025'. "
    "The document's own title governs here, not the filename.\n"
    "FY2024: Pillar 3 Disclosures 2024, 'KM1 - Key metrics' (end-2024 column).\n"
    "FY2023: Pillar 3 Disclosures 2023, 'KM1 - Key metrics' (end-2023 column).\n"
    "FY2022: Pillar 3 Disclosures 2022, 'KM1 - Key metrics' (end-2022 column).\n"
    "FY2021: FILLED FROM A LATER EDITION'S COMPARATIVE, and flagged here rather than presented as an own-year "
    "figure. CSUK's FY2021 edition prints NO KM1 template at all - it belongs to the pre-UK-CRR format, "
    "carrying an 'Own Funds' composition table (whose 'Total Capital (Own Funds)' of £391,172k does match "
    "row 3 below) but none of the template's structure. This was tested rather than assumed: the FY2021 "
    "edition contains zero occurrences of 'KM1', 'combined buffer', 'total exposure measure', 'Total SREP' "
    "and 'high-quality liquid', while the same document returns healthy counts for the control phrases 'own "
    "funds' (7), 'risk-weighted' (6), 'countercyclical' (3) and 'net stable funding' (3) - so the text is "
    "fully readable and the template is genuinely absent, not missed. The FY2021 column here is therefore "
    "the FY2022 edition's own '2021' comparative column.\n\n"
    "ROWS 18-20 ARE BLANK FOR FY2021 BY FORMAL EXCLUSION, not for want of data. The FY2022 edition's own "
    "footnote (4) states: 'Net Stable Funding Ratio is computed as an average of the last four spot quarter "
    "end positions. This is new disclosure effective 2022, thus comparative figures for 2021 not shown.'\n"
    "Rows UK 8a, UK 9a, 10, UK 10a and 14a-14e are not printed in any CSUK edition. Footnote (2) records why "
    "the leverage block is short: 'CSUK not being a LREQ firm, is not subject to minimum leverage ratio "
    "capital requirement.'\n"
    "ROW 13 CROSS-EDITION DIVERGENCE (documented, not reconciled): the FY2023 edition prints a total exposure "
    "measure of 2,409,589 for end-2023, while the FY2024 edition's own 2023 comparative prints 2,409,588. The "
    "own-year edition's figure is used here.\n\n"
    "WHY THIS SHEET DISAGREES WITH THE 11 METRIC SHEETS - A SOURCE DIFFERENCE, NOT AN ERROR. The metric "
    "sheets in this workbook are sourced from CSUK's Companies House ANNUAL REPORT KPI tables (see "
    "p3_sources above); this sheet reproduces the PILLAR 3 KM1 template. The two report different things on "
    "the liquidity rows, and the template says so itself:\n"
    "  - Row 17 LCR. KM1 footnote (3): 'Liquidity coverage ratio computed as an average of 12 month-end "
    "observations to the reporting date.' The Annual Report's figure is a year-end spot ratio. Hence KM1 "
    "4860.58% / 539.19% / 729.77% / 229.60% against the LCR sheet's 1,154% / 451% / 554.67% / 216.40% for "
    "FY2025-FY2022. Both are correct on their own basis; neither has been adjusted toward the other.\n"
    "  - BUT THE AVERAGING BASIS DOES NOT EXPLAIN FY2025, and it is recorded here rather than left to that "
    "assumption. Dividing each edition's own printed row 15 by its own printed row 16 gives a ratio the "
    "printed row 17 should be close to, and for FY2021-FY2024 it is: printed-over-implied is 1.015, 1.029, "
    "1.236 and 1.059 respectively, the sort of gap an average-of-ratios rather than ratio-of-averages "
    "produces. For FY2025 the same test gives 4860.58% printed against 419,937 / 28,755 = 1460.40% implied, "
    "a factor of 3.33; and on the NSFR rows 3599.46% printed against 486,909 / 150,879 = 322.71% implied, a "
    "factor of 11.15, where FY2022 and FY2023 reconcile almost exactly (0.999 and 1.000). No averaging "
    "convention produces those. The FY2025 edition's own rows 17 and 20 therefore do not reconcile with its "
    "own rows 15/16 and 18/19.\n"
    "    This was checked against the PAGE IMAGE, not merely the text layer, precisely because a number "
    "that fails its own arithmetic is usually a transcription fault rather than a fact about the bank. It is "
    "not one here: the rendered page of 'Pillar 3 Disclosures 2025', printed folio 16, plainly shows "
    "4860.58% on row 17 and 3599.46% on row 20 beside HQLA 419,937, net cash outflows 28,755, available "
    "stable funding 486,909 and required stable funding 150,879. The figures are reproduced as published. "
    "Nothing here is derived or back-solved, and the implied percentages above are shown only as evidence of "
    "the non-reconciliation - they are deliberately NOT used in place of what the Bank printed.\n"
    "  - Row 20 NSFR. KM1 footnote (4): 'computed as an average of the last four spot quarter end "
    "positions.' Hence 129.96% (KM1) against 129.25% (sheet) for FY2023, and 133.33% against 131.72% for "
    "FY2022.\n"
    "  - Rows 4/5/6/7 for FY2021 come from the FY2022 edition's comparative column (see above), which "
    "restates what the Annual Report reported at the time: RWA 1,335,858 (£1,336m) against the sheet's "
    "£1,340m, CET1/Tier 1 ratio 25.17% against 25.09%, and Total capital ratio 29.28% against 29.19%.\n"
    "  - Row 20 FY2025 differs additionally because the NSFR sheet rounds to '3,600%' where the template "
    "prints 3599.46% - a presentation difference of under a fiftieth of one percent, on top of the "
    "non-reconciliation described above.\n"
    "  - Rows 5/6/14 for FY2024 differ in the source documents only by the Annual Report's rounding to "
    "whole percentages (KM1 44.58% and 16.56% against the sheets' '45%' and '17%'); those now fall inside "
    "tolerance and no longer register.\n"
    "SEVEN cells differ in total, and every one falls into a class above: three from the restated FY2021 "
    "comparative on rows 5/6/7, two from the averaged-versus-spot NSFR on row 20 (FY2023 and FY2022), one "
    "from the restated FY2021 RWA on row 4, and one from rounding on row 20 FY2025. "
    "IT WAS ELEVEN UNTIL 18 SEPTEMBER 2026, and the four that went were the row 17 LCR cells for "
    "FY2025-FY2022. They did not go because a figure changed - none did - but because the LCR sheet now "
    "carries the Bank's Pillar 3 12-month-average LCR as its own second row alongside the Annual Report's "
    "spot row, so the template's row 17 has a same-basis counterpart to be checked against and matches it "
    "exactly. The basis difference that produced those four disagreements is unchanged and is still "
    "described above; it is simply now represented on both sheets instead of only one. "
    "Rows 1, 2, 3, 13 and 14 agree throughout - including row 3 "
    "FY2024, which is the figure corrected from 299 to 347 under this ticket. Rows 1 and 2 formerly "
    "registered as well, on FY2024/FY2023/FY2022, but that was a tolerance artefact of comparing a whole-£m "
    "sheet against a £'000 template and was resolved in verify_workbook.py on 2026-09-17; no figure changed.\n"
    "These are recorded here deliberately. A verifier disagreement on any of these rows is the expected "
    "consequence of two genuinely different published bases and must not be removed by editing a figure.\n\n"
    "ROWS 1, 2 AND 3 ARE EQUAL FOR FY2025 IN THE SOURCE - READ FROM THE DOCUMENT ON 2026-09-18, NOT "
    "INFERRED FROM THE OTHER SHEETS. The 'Pillar 3 Disclosures 2025' edition prints 305,801 on row 1 "
    "(CET1 capital), row 2 (Tier 1 capital) AND row 3 (Total capital) on printed folio 16, and prints "
    "191.10% on rows 5, 6 and 7. The three coincide because CSUK had NO Additional Tier 1 and NO Tier 2 "
    "in issue at 31 December 2025. The same edition says so three ways: its CC1 prints row 29 CET1 "
    "305,801 and row 59 Total capital 305,801 with no AT1 or Tier 2 amount row populated at all (the only "
    "Tier 2 line is row 77, a CAP on the inclusion of credit risk adjustments, 62); its balance-sheet "
    "reconciliation prints 'Long term debt -' and 'of which: Subordinated debt -', with total "
    "shareholders' equity of 305,801, equal to CET1 to the pound; and its Article 437 narrative states "
    "'CSUK's CET1 comprises permanent share capital of ordinary shares and reserves.' The Tier 2 of "
    "47,430 that stood at end-2024 (346,842 - 299,412) had been redeemed. CSUK is in run-off following "
    "the UBS acquisition, which is also why RWA falls from 671,676 to 160,021 while CET1 holds flat.\n"
    "Rows UK 7a/7b/7c/7d repeat FY2024's 3.32% / 1.11% / 1.48% / 13.91% exactly. That was confirmed in "
    "the FY2025 edition itself rather than carried over, because a repeated block is also what a copied "
    "column looks like.\n\n"
    "THE FY2025 EDITION'S OWN 2024 COMPARATIVE COLUMN IS DEFECTIVE, and is recorded rather than "
    "corrected, the same treatment as the row 13 divergence above. That column prints rows 1, 2 and 3 "
    "all as 299,412 - repeating CET1 into the Total capital slot - while printing row 7 for the same "
    "column as 51.64%, a percentage which against its own row 4 of 671,676 is 346,842. The edition "
    "contradicts itself, and FY2024's own edition prints 346,842. FY2024 on this sheet therefore stays "
    "346,842 under rule 1 and must not be 'corrected' toward this later comparative. This is very likely "
    "the origin of the FY2024 error corrected on 2026-09-17: the duplication was printed by the Bank "
    "first, in the edition a transcriber would reach for last.\n\n"
    "LATEST-EDITION CHECK (2026-09-17, re-confirmed 2026-09-18): the UBS-hosted Credit Suisse legal-entity disclosure index was "
    "enumerated directly. The newest CSUK Pillar 3 is the 'Pillar 3 Disclosures 2025' edition used above for "
    "FY2025, so this workbook is current; no FY2026 edition exists yet.\n"
)

km1_rows = [
    ("SECTION", "Available own funds (amounts)", {}),
    ("DATA", "1  Common Equity Tier 1 (CET1) capital (£'000)", {
        "FY2025": 305801, "FY2024": 299412, "FY2023": 291388, "FY2022": 330376, "FY2021": 336173}),
    ("DATA", "2  Tier 1 capital (£'000)", {
        "FY2025": 305801, "FY2024": 299412, "FY2023": 291388, "FY2022": 330376, "FY2021": 336173}),
    ("DATA", "3  Total capital (£'000)", {
        "FY2025": 305801, "FY2024": 346842, "FY2023": 344861, "FY2022": 385376, "FY2021": 391173}),
    ("SECTION", "Risk-weighted exposure amounts", {}),
    ("DATA", "4  Total risk-weighted exposure amount (£'000)", {
        "FY2025": 160021, "FY2024": 671676, "FY2023": 999597, "FY2022": 1123970, "FY2021": 1335858}),
    ("SECTION", "Capital ratios (as a percentage of risk-weighted exposure amount)", {}),
    ("DATA", "5  Common Equity Tier 1 ratio (%)", {
        "FY2025": "191.10%", "FY2024": "44.58%", "FY2023": "29.15%", "FY2022": "29.39%", "FY2021": "25.17%"}),
    ("DATA", "6  Tier 1 ratio (%)", {
        "FY2025": "191.10%", "FY2024": "44.58%", "FY2023": "29.15%", "FY2022": "29.39%", "FY2021": "25.17%"}),
    ("DATA", "7  Total capital ratio (%)", {
        "FY2025": "191.10%", "FY2024": "51.64%", "FY2023": "34.50%", "FY2022": "34.29%", "FY2021": "29.28%"}),
    ("SECTION", "Additional own funds requirements based on Supervisory Review and Evaluation Process "
                "('SREP') (as a percentage of risk-weighted exposure amount)", {}),
    ("DATA", "UK 7a  Additional CET1 SREP requirements (%)", {
        "FY2025": "3.32%", "FY2024": "3.32%", "FY2023": "1.77%", "FY2022": "1.77%", "FY2021": "3.51%"}),
    ("DATA", "UK 7b  Additional AT1 SREP requirements (%)", {
        "FY2025": "1.11%", "FY2024": "1.11%", "FY2023": "0.59%", "FY2022": "0.59%", "FY2021": "1.17%"}),
    ("DATA", "UK 7c  Additional T2 SREP requirements (%)", {
        "FY2025": "1.48%", "FY2024": "1.48%", "FY2023": "0.79%", "FY2022": "0.79%", "FY2021": "1.56%"}),
    ("DATA", "UK 7d  Total SREP own funds requirements (%)", {
        "FY2025": "13.91%", "FY2024": "13.91%", "FY2023": "11.15%", "FY2022": "11.15%", "FY2021": "14.24%"}),
    ("SECTION", "Combined buffer requirement (as a percentage of risk-weighted exposure amount)", {}),
    ("DATA", "8  Capital conservation buffer (%)", {
        "FY2025": "2.50%", "FY2024": "2.50%", "FY2023": "2.50%", "FY2022": "2.50%", "FY2021": "2.50%"}),
    ("DATA", "9  Institution specific countercyclical capital buffer (%)", {
        "FY2025": "0.69%", "FY2024": "0.81%", "FY2023": "0.80%", "FY2022": "0.49%", "FY2021": "0.04%"}),
    ("DATA", "11  Combined buffer requirement (%)", {
        "FY2025": "3.19%", "FY2024": "3.31%", "FY2023": "3.30%", "FY2022": "2.99%", "FY2021": "2.54%"}),
    ("DATA", "UK 11a  Overall capital requirements (%)", {
        "FY2025": "17.10%", "FY2024": "17.22%", "FY2023": "14.45%", "FY2022": "14.14%", "FY2021": "16.78%"}),
    ("DATA", "12  CET1 available after meeting the total SREP own funds requirements (%)", {
        "FY2025": "183.28%", "FY2024": "36.75%", "FY2023": "22.88%", "FY2022": "23.12%", "FY2021": "17.16%"}),
    ("SECTION", "Leverage ratio", {}),
    ("DATA", "13  Leverage ratio total exposure measure excluding claims on central banks (£'000)", {
        "FY2025": 352528, "FY2024": 1808065, "FY2023": 2409589, "FY2022": 2899039, "FY2021": 3616433}),
    ("DATA", "14  Leverage ratio excluding claims on central banks (%)", {
        "FY2025": "86.75%", "FY2024": "16.56%", "FY2023": "12.09%", "FY2022": "11.40%", "FY2021": "9.30%"}),
    ("SECTION", "Liquidity Coverage Ratio", {}),
    ("DATA", "15  Total high-quality liquid assets (HQLA) (Weighted value - average) (£'000)", {
        "FY2025": 419937, "FY2024": 530822, "FY2023": 494954, "FY2022": 884980, "FY2021": 1084683}),
    ("DATA", "UK 16a  Cash outflows - Total weighted value (£'000)", {
        "FY2025": 80955, "FY2024": 225651, "FY2023": 241742, "FY2022": 640811, "FY2021": 734039}),
    ("DATA", "UK 16b  Cash inflows - Total weighted value (£'000)", {
        "FY2025": 56043, "FY2024": 121416, "FY2023": 174440, "FY2022": 244370, "FY2021": 255399}),
    ("DATA", "16  Total net cash outflows (adjusted value) (£'000)", {
        "FY2025": 28755, "FY2024": 104235, "FY2023": 83862, "FY2022": 396440, "FY2021": 478638}),
    ("DATA", "17  Liquidity coverage ratio (%)", {
        "FY2025": "4860.58%", "FY2024": "539.19%", "FY2023": "729.77%", "FY2022": "229.60%",
        "FY2021": "230.07%"}),
    ("SECTION", "Net Stable Funding Ratio", {}),
    ("DATA", "18  Total available stable funding (£'000)", {
        "FY2025": 486909, "FY2024": 1249395, "FY2023": 1398068, "FY2022": 1773117}),
    ("DATA", "19  Total required stable funding (£'000)", {
        "FY2025": 150879, "FY2024": 762813, "FY2023": 1076052, "FY2022": 1328489}),
    ("DATA", "20  NSFR ratio (%)", {
        "FY2025": "3599.46%", "FY2024": "167.13%", "FY2023": "129.96%", "FY2022": "133.33%"}),
]

bw.add_km1_sheet(
    title="Credit Suisse (UK) Limited — KM1 Key Metrics",
    subtitle="The Bank's own published 'KM1 - Key metrics' template, reproduced whole; amounts in GBP '000 "
             "and ratios as printed. FY2021 is filled from the FY2022 edition's comparative column - see note.",
    rows=km1_rows,
    sources_text=KM1_SOURCES,
    first_col_width=74,
    source_height=470,
    years=KM1_YEARS,
)

metric("CET1 Capital", "£m", [("Common Equity Tier 1 (CET1) capital (combined with Tier 1)", CET1_TIER1_CAPITAL)],
       p3_sources(), note=COMBINED_NOTE)
metric("CET1 Ratio", "%", [("CET1 Ratio (combined with Tier 1)", CET1_TIER1_RATIO)], p3_sources(), note=COMBINED_NOTE)
metric("Tier 1 Capital", "£m", [("Tier 1 Capital (combined with CET1)", CET1_TIER1_CAPITAL)], p3_sources(), note=COMBINED_NOTE)
metric("Tier 1 Ratio", "%", [("Tier 1 Ratio (combined with CET1)", CET1_TIER1_RATIO)], p3_sources(), note=COMBINED_NOTE)

TOTAL_CAPITAL = {"FY2025": 306, "FY2024": 347, "FY2023": 345, "FY2022": 385, "FY2021": 391,
                 "FY2020": 369, "FY2019": 355, "FY2018": 331, "FY2017": 238, "FY2016": 211}
TOTAL_CAPITAL_NOTE = (
    "FY2016-FY2020 (added under HD-026): a real, directly disclosed 'Own Funds' figure (Total Tier 1/CET1 "
    "capital + Total Tier 2 capital, i.e. subordinated debt) exists in every one of these 5 years' own "
    "Capital adequacy note, rounded to £m here (precise £'000 figures: FY2020 £368,692k, FY2019 £355,328k, "
    "FY2018 £330,660k, FY2017 £238,126k, FY2016 £210,547k). FY2021-FY2025: NOT directly disclosed as a "
    "separate figure in any of those 5 years' KPI tables - only a combined 'Tier 1 and CET1' figure is given "
    "there, with no mention of AT1 or Tier 2 instruments. The later own-funds tables in CSUK's official UBS-hosted "
    "Pillar 3 disclosures confirm Total Capital (rounded to £m) for FY2021-FY2025 as 391, 385, 345, 347 and 306 respectively.\n"
    "FY2024 CORRECTED 2026-09-17 (was 299, under KM1-011): 299 is the CET1/Tier 1 figure, duplicated into the "
    "Total Capital slot. The cited source - CSUK's own 'Pillar 3 Disclosures 2024', table 'KM1 - Key metrics', "
    "row 3 'Total capital' - prints £346,842k for end-2024 against £299,412k of CET1 on rows 1 and 2, so the "
    "two genuinely differ that year by £47,430k of Tier 2. Three independent checks agree: the printed row 3 "
    "itself; that document's row 7 Total capital ratio of 51.64%, which against its printed RWA of £671,676k "
    "corresponds to £346.9m and cannot be reconciled with £299m (which is 44.58%, the printed CET1 ratio on "
    "rows 5/6); and the sourcing pattern of the four surrounding years, whose values here (391, 385, 345, 306) "
    "each match their own edition's printed row 3 exactly. This is a transcription slip corrected against the "
    "note's own cited document - not a figure altered to satisfy a checker."
)
metric("Total Capital", "£m", [("Total Capital (Own Funds)", TOTAL_CAPITAL)], p3_sources(), note=TOTAL_CAPITAL_NOTE)

TOTAL_CAPITAL_RATIO_NOTE = (
    "Directly disclosed in the official UBS-hosted Pillar 3 KM1 tables for FY2021-FY2025; FY2016-FY2020 were not "
    "reported as a percentage in the located KPI/capital-adequacy tables. "
    "Not directly disclosed as a percentage ratio in any of the 5 earlier years' KPI tables or Capital adequacy "
    "notes checked (FY2016-FY2025) - only the £ Own Funds figure is given (see the Total Capital sheet), "
    "with no accompanying Total Capital Ratio %. NOT assumed or derived by dividing Own Funds by RWA "
    "without an explicit stated ratio, per project convention - left blank rather than guessed for FY2016-FY2020."
)
metric("Total Capital Ratio", "%", [("Total Capital Ratio", {"FY2025": "191.10%", "FY2024": "51.64%", "FY2023": "34.50%", "FY2022": "34.29%", "FY2021": "29.19%"})], p3_sources(), note=TOTAL_CAPITAL_RATIO_NOTE)

metric("Total RWAs", "£m", [("Risk Weighted Assets (RWA)", RWA)], p3_sources())

# ---------------------------------------------------------------
# Sheet: RWA Breakdown (placed right after Total RWAs)
# ---------------------------------------------------------------
rwa_breakdown_rows = [
    ("SECTION", "UK OV1 — Overview of risk weighted exposure amounts (FY2022-FY2025)", {}),
    ("DATA", "Credit risk (excluding CCR)", {"FY2025": 4053, "FY2024": 449009, "FY2023": 750436, "FY2022": 884443}),
    ("DATA", "Counterparty credit risk (CCR)", {"FY2025": 887, "FY2024": 33553, "FY2023": 30969, "FY2022": 30213}),
    ("DATA", "Market risk", {"FY2025": 7791, "FY2023": 15933}),
    ("DATA", "Operational risk", {"FY2025": 147290, "FY2024": 189114, "FY2023": 202259, "FY2022": 209312}),
    ("DATA", "Settlement risk", {"FY2022": 3}),
    ("SECTION", "Pre-OV1 format, collapsed to summary lines (FY2021)", {}),
    ("DATA", "Total credit and counterparty credit risk", {"FY2021": 1109433}),
    ("DATA", "Total market risk", {"FY2021": 0}),
    ("DATA", "Total other risks (operational risk)", {"FY2021": 230434}),
    ("TOTAL", "Total RWAs", {"FY2025": 160021, "FY2024": 671676, "FY2023": 999597, "FY2022": 1123970, "FY2021": 1339867,
                             "FY2020": "Not publicly disclosed", "FY2019": "Not publicly disclosed", "FY2018": "Not publicly disclosed",
                             "FY2017": "Not publicly disclosed", "FY2016": "Not publicly disclosed"}),
]

bw.add_rwa_breakdown_sheet(
    title="Credit Suisse (UK) Limited — RWA Breakdown",
    subtitle="£'000s. UK OV1 template FY2022-FY2025; older pre-OV1 format for FY2021. Not publicly disclosed FY2016-FY2020 - see source note.",
    rows=rwa_breakdown_rows,
    sources_text=RWA_BREAKDOWN_SOURCES,
    first_col_width=58,
    source_height=340,
)

LEVERAGE_INTERIOR_NOTE = (
    "\nFY2023-FY2019 FILLED 2026-09-18 (interior-gap sweep). This row previously jumped from FY2018 to "
    "FY2024 with five blank years between - the classic interior hole, and it was ours, not the Bank's. "
    "The sentence it replaces read that the metric was 'confirmed genuinely absent for FY2016/FY2019-"
    "FY2023, not omitted by search'. That was a true statement about ONE document - the Annual Report KPI "
    "table, which really does drop the 'Statement of Financial Position' KPI section for those years - "
    "written down as a statement about the BANK. CSUK published a leverage ratio in every one of those "
    "five years, in its own standalone Pillar 3 disclosure, and each figure below is from THAT YEAR'S OWN "
    "EDITION (no comparative columns used):\n"
    f"  FY2023 12.09% - 'Pillar 3 Disclosures 2023', KM1 row 14 'Leverage ratio excluding claims on central "
    f"banks (%)', printed folio 20, and repeated in that edition's Leverage Ratio narrative ('CSUK's "
    f"leverage ratio increased to 12.09% as at 31 December 2023 from 11.40% as at 31 December 2022') - "
    f"{P3_2023_URL}\n"
    f"  FY2022 11.40% - 'Pillar 3 Disclosures 2022', KM1 row 14, printed folio 19, and repeated in that "
    f"edition's narrative ('CSUK's leverage ratio increased to 11.40% as at 31 December 2022 from 9.30% as "
    f"at 31 December 2021') - {P3_2022_URL}\n"
    f"  FY2021 9.30% - '2021 Pillar 3 Disclosures', 'Leverage Ratio Common Disclosure' table, final row, "
    f"printed folio 33 ('Leverage Ratio 9.30 %') - {P3_2021_URL}\n"
    f"  FY2020 8.07% - '2020 Pillar 3 Disclosures', 'Leverage Ratio Common Disclosure' table, printed folio "
    f"24 ('Leverage Ratio 8.07%'; Tier 1 Capital 295,460 / Total Exposures 3,659,748) - {P3_2020_URL}\n"
    f"  FY2019 8.47% - 'Pillar 3 Disclosures 2019', 'Leverage Ratio Common Disclosure' table, printed folio "
    f"22 ('Leverage Ratio 8.47%'; Tier 1 Capital 300,176 / Total Exposures 3,544,752) - {P3_2019_URL}\n"
    "CROSS-EDITION RESTATEMENTS, DOCUMENTED AND DELIBERATELY NOT APPLIED. Two of these years are restated "
    "by the NEXT edition's narrative comparative, and the own-year figure is kept in both cases per this "
    "project's own-edition rule: the 2020 edition says the ratio 'increased to 8.07% as at 31 December "
    "2020 from 7.74% as at 31 December 2019', against the 2019 edition's own 8.47%; and the 2021 edition "
    "says it 'increased to 9.30% as at 31 December 2021 from 8.57% as at 31 December 2020', against the "
    "2020 edition's own 8.07%. CSUK never explains either movement. Do not reconcile them.\n"
    "BASIS BREAK, stated rather than smoothed: FY2019-FY2021 are the CRR / Commission Delegated Act "
    "leverage ratio (Tier 1 capital over total exposures) as each of those editions defines it, whereas "
    "FY2022 onward are captioned 'excluding claims on central banks' under the UK leverage framework. The "
    "two coincide at the FY2021/FY2022 join - the FY2022 edition's own 2021 comparative on the UK-captioned "
    "row prints exactly the 9.30% the 2021 edition printed on the CRR row - but that is the Bank's own "
    "arithmetic, not an equivalence asserted here.\n"
    "FY2016 remains blank: that year has no KPI table and its standalone Pillar 3 was not opened in this "
    "pass (an edition for 2016 IS listed on the UBS archive index - see the reach note in the sources "
    "above - so the FY2016 blank is an UNCHECKED lead, not a demonstrated absence)."
)
metric("Leverage Ratio", "%", [("Leverage Ratio", LEVERAGE_RATIO)], p3_sources(LEVERAGE_INTERIOR_NOTE))

LCR_INTERIOR_NOTE = (
    "\nTWO ROWS, TWO DIFFERENT MEASURES - read the labels. The Bank publishes an LCR on two bases and says "
    "so itself, so they are kept as separate rows and neither is adjusted toward the other. The Pillar 3 "
    "2020 edition, printed folio 21, footnotes its own table: 'For the purpose of Pillar 3, the values are "
    "calculated as the simple average of the month-end observations over the preceding twelve months. The "
    "HQLA and LCR reported as at 31 December 2020 in CSUK Annual Report represents the spot value as of the "
    "reporting date.'\n"
    "ROW 1 (spot, year-end) is the Annual Report basis. FY2021 ADDED 2026-09-18: 216%, stated by CSUK "
    f"itself in the '2021 Pillar 3 Disclosures', printed folio 29, footnote to the LCR table - 'the HQLA "
    f"and LCR reported as at 31 December 2021 in CSUK Annual Report represents the spot value of 216% as "
    f"of the reporting date' - {P3_2021_URL}. It is a spot figure quoted from the Annual Report by the "
    "Bank's own Pillar 3, so it belongs on this row and not the average row. FY2020 and FY2019 have NO "
    "published spot LCR anywhere located: the 2020 edition's footnote names the Annual Report's spot "
    "value without printing it, the 2019 edition carries no such footnote at all, and those years' KPI "
    "tables give only a Liquidity Buffer £ amount. Those two cells stay blank on this row. FY2018's 154% "
    "is itself captioned 'Average Liquidity Coverage Ratio' in that year's KPI table - a pre-existing "
    "basis inconsistency on this row, flagged here rather than silently corrected. FY2017's own "
    "comparative column explicitly states 'n/a'; FY2016 has no KPI table at all.\n"
    "ROW 2 (Pillar 3, 12-month average) ADDED 2026-09-18. This is the row that fills FY2020 and FY2019, "
    "and every figure is the reporting-year column of that year's OWN edition:\n"
    f"  FY2019 246% - 'Pillar 3 Disclosures 2019', LCR table, printed folio 19, 'Quarter ending on "
    f"31/12/2019' column (Liquidity Buffer £1,010m / Total Net Cash Outflows £462m) - {P3_2019_URL}\n"
    f"  FY2020 300% - '2020 Pillar 3 Disclosures', LCR table, printed folio 21, 'Quarter ending on "
    f"31/12/2020' column (£938m / £365m) - {P3_2020_URL}\n"
    f"  FY2021 230% - '2021 Pillar 3 Disclosures', LCR table, printed folio 29, 'Quarter ending on "
    f"31/12/2021' column (£1,085m / £479m), printed as '230 %' - {P3_2021_URL}. The FY2022 edition's own "
    "2021 KM1 comparative prints this to two decimals as 230.07%; the own-edition figure is used here and "
    "the KM1 Key Metrics sheet keeps the comparative's 230.07% on its own row, so the workbook shows both.\n"
    f"  FY2022 229.60% and FY2023 729.77% - KM1 row 17 of the 2022 and 2023 editions, printed folios 19 "
    f"and 20 - {P3_2022_URL} / {P3_2023_URL}\n"
    "  FY2024 539.19% and FY2025 4860.58% - KM1 row 17 of the 2024 and 2025 editions, as already "
    "reproduced on the KM1 Key Metrics sheet (see that sheet's note on FY2025's failure to reconcile with "
    "its own rows 15/16 - reproduced as published, not corrected).\n"
    "WHAT THIS REPLACES: this note used to say FY2019/FY2020/FY2021 were 'confirmed genuinely absent for "
    "that year, not omitted by search'. They were absent from the Annual Report KPI table, which is the "
    "only document that sentence had actually looked at."
)
metric("LCR", "%", [("Liquidity Coverage Ratio (LCR) - spot, year-end basis (Annual Report)", LCR),
                    ("Liquidity Coverage Ratio (LCR) - Pillar 3 basis, 12-month average of month-end "
                     "observations", LCR_P3_AVERAGE)],
       p3_sources(LCR_INTERIOR_NOTE))

metric("NSFR", "%", [("Net Stable Funding Ratio (NSFR)", NSFR)], p3_sources(
    "\nFY2021's KPI table (earliest format checked before this ticket) discloses only a 'Liquidity Buffer "
    "(£m)' figure, no NSFR% - confirmed genuinely absent for that year, not omitted by search. No NSFR "
    "figure was found in any of the FY2016-FY2020 KPI tables/comparative columns either, despite each "
    "year's Strategic Report discussing NSFR in general regulatory terms."))

MREL_NOTE = (
    "Not disclosed anywhere in any of the 10 years' Companies House filings reviewed (FY2016-FY2025), no "
    "exemption stated. Plausibly below the "
    "Bank of England's MREL threshold given CSUK's small and (post-Part-VII-transfer) shrinking balance "
    "sheet, but not confirmed - left blank rather than guessed."
)
bw.add_not_disclosed_metric_sheets(["MREL Ratio"], p3_sources(), per_note={"MREL Ratio": MREL_NOTE})

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets",
         {"FY2025": 352528, "FY2024": 1801155, "FY2023": 2392470, "FY2022": 2885789, "FY2021": 3579171,
          "FY2020": 3654695, "FY2019": 3483980, "FY2018": 3502344, "FY2017": 3334736, "FY2016": 2946364}),
        ("Loans and advances, net",
         {"FY2025": 0, "FY2024": 818949, "FY2023": 1307573, "FY2022": 1706528, "FY2021": 2041139,
          "FY2020": 1990006, "FY2019": 2126766, "FY2018": 2141288, "FY2017": 2166554, "FY2016": 1547855}),
        ("Deposits",
         {"FY2025": 27218, "FY2024": 548119, "FY2023": 654960, "FY2022": 1094750, "FY2021": 3118581,
          "FY2020": 3183065, "FY2019": 3040602, "FY2018": 3087177, "FY2017": 2990492, "FY2016": 2635334}),
        ("Total equity",
         {"FY2025": 305801, "FY2024": 299440, "FY2023": 292552, "FY2022": 345686, "FY2021": 351228,
          "FY2020": 341173, "FY2019": 322943, "FY2018": 297290, "FY2017": 237844, "FY2016": 208494}),
    ],
    balance_sheet_unit="£'000",
    income_statement_totals=[
        ("Net revenue",
         {"FY2025": 47807, "FY2024": 82745, "FY2023": 100908, "FY2022": 112483, "FY2021": 107874,
          "FY2020": 112919, "FY2019": 123230, "FY2018": 125405, "FY2017": 140675, "FY2016": 90912}),
        ("Total operating expense",
         {"FY2025": -38004, "FY2024": -71941, "FY2023": -127107, "FY2022": -91062, "FY2021": -96967,
          "FY2020": -87752, "FY2019": -88649, "FY2018": -85525, "FY2017": -104464, "FY2016": -89714}),
        ("Profit/(loss) for the year",
         {"FY2025": 6361, "FY2024": 6888, "FY2023": -23134, "FY2022": 14458, "FY2021": 10055,
          "FY2020": 19661, "FY2019": 25653, "FY2018": 29200, "FY2017": 29034, "FY2016": -444}),
    ],
    income_statement_unit="£'000",
    equity_changes_totals=[
        ("Opening equity",
         {"FY2025": 299440, "FY2024": 292552, "FY2023": 345686, "FY2022": 351228, "FY2021": 341173,
          "FY2020": 322943, "FY2019": 297290, "FY2018": 237844, "FY2017": 208494, "FY2016": 208623}),
        ("Total comprehensive income/(loss) for the year",
         {"FY2025": 6361, "FY2024": 6888, "FY2023": -23134, "FY2022": 14458, "FY2021": 10055,
          "FY2020": 19661, "FY2019": 25653, "FY2018": 29200, "FY2017": 29350, "FY2016": -129}),
        ("Other equity movements, net",
         {"FY2025": 0, "FY2024": 0, "FY2023": -30000, "FY2022": -20000, "FY2021": 0,
          "FY2020": -1431, "FY2019": 0, "FY2018": 30246, "FY2017": 0, "FY2016": 0}),
        ("Closing equity",
         {"FY2025": 305801, "FY2024": 299440, "FY2023": 292552, "FY2022": 345686, "FY2021": 351228,
          "FY2020": 341173, "FY2019": 322943, "FY2018": 297290, "FY2017": 237844, "FY2016": 208494}),
    ],
    equity_changes_unit="£'000",
    cash_flow_totals=[
        ("Net cash flow generated from/(used in) operating activities",
         {"FY2025": 59618, "FY2024": 320701, "FY2023": 180409, "FY2022": 284435, "FY2021": -71555,
          "FY2020": 46361, "FY2019": 266443, "FY2018": -320398, "FY2017": 68431, "FY2016": 57458}),
        ("Net cash flow generated from/(used in) investing activities",
         {"FY2025": 539843, "FY2024": 0, "FY2023": -786, "FY2022": -3455, "FY2021": -3799,
          "FY2020": -6867, "FY2019": -3981, "FY2018": 401, "FY2017": -939, "FY2016": 0}),
        ("Net cash flow used in financing activities",
         {"FY2025": -906597, "FY2024": -530786, "FY2023": -82094, "FY2022": -251725, "FY2021": -1620,
          "FY2020": -1843, "FY2019": -2008, "FY2018": 59323, "FY2017": -867, "FY2016": -920}),
        ("Cash and cash equivalents at the end of the year",
         {"FY2025": 21709, "FY2024": 341768, "FY2023": 548659, "FY2022": 475709, "FY2021": 408082,
          "FY2020": 483717, "FY2019": 447816, "FY2018": 197301, "FY2017": 499549, "FY2016": 432924}),
    ],
    cash_flow_unit="£'000",
    ratios=[
        ("CET1/Tier 1 Ratio", CET1_TIER1_RATIO),
        ("Leverage Ratio", LEVERAGE_RATIO),
        ("LCR", LCR),
        ("NSFR", NSFR),
    ],
    note="FY2025's cash flow figures reflect a major one-off event: the 20 June 2025 Part VII transfer of "
         "most of CSUK's business to UBS AG London Branch (a £539,843k cash receipt in investing "
         "activities), which also drove RWAs and capital ratios sharply post-transfer. See the Cash Flow "
         "Statement sheet's source note for detail. Extended back to FY2016 under HD-026 (2026-09-06); "
         "FY2020's 'Other equity movements' includes a -£1,431k correction of error restated in FY2020's "
         "own filing (see Statement of Changes in Equity source note), and FY2018's includes both a "
         "+£246k IFRS 9 transition adjustment and a +£30,000k capital contribution. Figures are duplicated "
         "from the detail sheets for at-a-glance trend viewing.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/CREDIT SUISSE UK FINANCIALS.xlsx")
