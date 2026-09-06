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
    "NSFR are self-skipped as genuinely undisclosed in any filing obtained (confirmed via a Wayback CDX "
    "search of credit-suisse.com for a standalone Pillar 3 document, which returned no CSUK-specific hit "
    "before the search was judged uneconomical to keep pursuing) - FY2016 CET1/Tier 1 Capital (the £ amount) "
    "IS available, from the Capital adequacy note's Own Funds table.\n"
    "- Leverage Ratio is disclosed only in the FY2017/FY2018 KPI tables (6.3%/7.8%) - absent from FY2016 "
    "(no KPI table) and from FY2019/FY2020's own KPI tables (which dropped the 'Statement of Financial "
    "Position' KPI section entirely), consistent with the already-known gap before it reappears in FY2024/"
    "FY2025. Average LCR is disclosed only in the FY2018 KPI table (154%) - FY2017's KPI table explicitly "
    "shows 'n/a', and FY2019/FY2020 KPI tables carry no LCR figure at all (only a Liquidity Buffer £ "
    "amount), consistent with the already-known gap before LCR reappears from FY2022. NSFR is not found "
    "disclosed anywhere in FY2016-FY2020.\n"
    "- Total Capital / Total Capital Ratio: a Capital adequacy note ('Own Funds' table: Total Tier 1/CET1 "
    "capital + Total Tier 2 capital = Own Funds) exists in every FY2016-FY2020 filing and gives a genuine, "
    "directly disclosed Total Capital (£ Own Funds) figure each year - populated on this sheet for FY2016-"
    "FY2020 only. This contradicts the existing FY2021-FY2025 columns' 'not directly disclosed' claim on "
    "the same sheet (that claim was based on the KPI table alone, which never carried a Total Capital line "
    "in any year checked) - flagged here as a likely correctness gap for a future audit-only ticket to "
    "resolve for FY2021-FY2025, but deliberately NOT fixed in this ticket (out of scope: this ticket only "
    "extends the year window). No Total Capital RATIO (%) was found disclosed in any year FY2016-FY2020 "
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
    "Not publicly disclosed in any of the 10 years (FY2016-FY2025) - confirmed by reading each year's "
    "Annual Report in full (all numbered notes through to the final note in each filing - Note 36 "
    "'Subsequent events' in the FY2025 report, similarly the last note in each of the FY2023/FY2021/FY2020/"
    "FY2019/FY2018/FY2017/FY2016 reports), plus the existing Pillar 3 KPI-table sourcing already used for "
    "the CET1/Tier 1/Total RWAs/Leverage/LCR/NSFR sheets. No 'Capital Adequacy' note with an RWA category "
    "breakdown (credit risk/counterparty credit risk/market risk/operational risk) exists in any of the 8 "
    "Companies House filings reviewed (each year's own Capital adequacy note gives only a single Own Funds/"
    "Total-eligible-capital figure and a general statement that RWAs 'reflect the credit, market, "
    "operational and other risks of the institution', with no numeric category breakdown), and (per the "
    "existing Pillar 3 sheets' own source note) no standalone Pillar 3 document for this entity was located "
    "either - only the single aggregate Total RWA figure already used on the Total RWAs sheet is disclosed "
    "anywhere."
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
        "table (no standalone Pillar 3 document was located for CSUK; the FY2025 Annual Report's own "
        "Strategic Report states 'Pillar 3 disclosures can be found separately at "
        "https://www.ubs.com/global/en/investor-relations', but a CSUK-specific document was not "
        "identified there within budget - WebSearch quota was already exhausted):\n"
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
        + page_note
    )


CET1_TIER1_CAPITAL = {"FY2025": 306, "FY2024": 299, "FY2023": 291, "FY2022": 330, "FY2021": 336,
                       "FY2020": 314, "FY2019": 300, "FY2018": 276, "FY2017": 213, "FY2016": 186}
CET1_TIER1_RATIO = {"FY2025": "191%", "FY2024": "45%", "FY2023": "29.15%", "FY2022": "29.39%", "FY2021": "25.09%",
                     "FY2020": "22%", "FY2019": "21.9%", "FY2018": "22.5%", "FY2017": "17.2%"}
RWA = {"FY2025": 160, "FY2024": 672, "FY2023": 1000, "FY2022": 1124, "FY2021": 1340,
       "FY2020": 1338, "FY2019": 1371, "FY2018": 1225, "FY2017": 1241}
LEVERAGE_RATIO = {"FY2025": "87%", "FY2024": "17%", "FY2018": "7.8%", "FY2017": "6.3%"}
LCR = {"FY2025": "1,154%", "FY2024": "451%", "FY2023": "554.67%", "FY2022": "216.40%", "FY2018": "154%"}
NSFR = {"FY2025": "3,600%", "FY2024": "167%", "FY2023": "129.25%", "FY2022": "131.72%"}

COMBINED_NOTE = (
    "The Bank's own KPI table discloses a single combined 'Tier 1 and Common Equity Tier 1 (CET1)' "
    "line, not separate Tier 1/CET1 figures - used identically for both the CET1 and Tier 1 sheets. FY2016's "
    "£ figure is the Capital adequacy note's 'Total Tier 1 (and CET1) capital' (£185,547k, rounded to £186m) "
    "- no ratio/RWA is available for FY2016 to pair with it (see ENTITY NOTE and p3_sources above)."
)

metric("CET1 Capital", "£m", [("Common Equity Tier 1 (CET1) capital (combined with Tier 1)", CET1_TIER1_CAPITAL)],
       p3_sources(), note=COMBINED_NOTE)
metric("CET1 Ratio", "%", [("CET1 Ratio (combined with Tier 1)", CET1_TIER1_RATIO)], p3_sources(), note=COMBINED_NOTE)
metric("Tier 1 Capital", "£m", [("Tier 1 Capital (combined with CET1)", CET1_TIER1_CAPITAL)], p3_sources(), note=COMBINED_NOTE)
metric("Tier 1 Ratio", "%", [("Tier 1 Ratio (combined with CET1)", CET1_TIER1_RATIO)], p3_sources(), note=COMBINED_NOTE)

TOTAL_CAPITAL = {"FY2025": 306, "FY2024": 299, "FY2023": 345, "FY2022": 385, "FY2021": 391,
                 "FY2020": 369, "FY2019": 355, "FY2018": 331, "FY2017": 238, "FY2016": 211}
TOTAL_CAPITAL_NOTE = (
    "FY2016-FY2020 (added under HD-026): a real, directly disclosed 'Own Funds' figure (Total Tier 1/CET1 "
    "capital + Total Tier 2 capital, i.e. subordinated debt) exists in every one of these 5 years' own "
    "Capital adequacy note, rounded to £m here (precise £'000 figures: FY2020 £368,692k, FY2019 £355,328k, "
    "FY2018 £330,660k, FY2017 £238,126k, FY2016 £210,547k). FY2021-FY2025: NOT directly disclosed as a "
    "separate figure in any of those 5 years' KPI tables - only a combined 'Tier 1 and CET1' figure is given "
    "there, with no mention of AT1 or Tier 2 instruments. The later own-funds tables in CSUK's official UBS-hosted "
    "Pillar 3 disclosures confirm Total Capital (rounded to £m) for FY2021-FY2025 as 391, 385, 345, 299 and 306 respectively."
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
    ("SECTION", "RWA by risk category", {}),
    ("TOTAL", "Total RWAs", {y: "Not publicly disclosed" for y in YEARS}),
]

bw.add_rwa_breakdown_sheet(
    title="Credit Suisse (UK) Limited — RWA Breakdown",
    subtitle="Not publicly disclosed in any year. See source note at bottom.",
    rows=rwa_breakdown_rows,
    sources_text=RWA_BREAKDOWN_SOURCES,
)

metric("Leverage Ratio", "%", [("Leverage Ratio", LEVERAGE_RATIO)], p3_sources(
    "\nLeverage Ratio reappears in the KPI table format used from the FY2025 Annual Report onward. It was "
    "also disclosed in the FY2017/FY2018 KPI tables (6.3%/7.8%, under a 'Statement of Financial Position' "
    "KPI section) - but that section was dropped from the KPI table format used in the FY2019 and FY2020 "
    "Annual Reports, and FY2023/FY2022/FY2021's KPI tables (a further later format) don't include this "
    "metric either. FY2016 has no KPI table at all. Confirmed genuinely absent for FY2016/FY2019-FY2023, "
    "not omitted by search."))

metric("LCR", "%", [("Liquidity Coverage Ratio (LCR)", LCR)], p3_sources(
    "\nFY2021's KPI table (earliest format checked before this ticket) discloses only a 'Liquidity Buffer "
    "(£m)' figure, no LCR% - confirmed genuinely absent for that year, not omitted by search. FY2018's KPI "
    "table is the only other year with an LCR figure (an 'Average Liquidity Coverage Ratio' of 154%, itself "
    "flagged there as a new disclosure that year); FY2017's own comparative column explicitly states 'n/a' "
    "for this metric; FY2019/FY2020's KPI tables carry only a Liquidity Buffer figure again, no LCR%; FY2016 "
    "has no KPI table at all."))

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
