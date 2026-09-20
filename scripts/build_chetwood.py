import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021", "FY2020", "FY2019"]  # most recent first
YEAR_LABEL = {
    "FY2025": "FY2025",
    "FY2024": "FY2024",
    "FY2023": "FY2023",
    "FY2022": "FY2022",
    "FY2021": "FY2021†",
    "FY2020": "FY2020†‡",
    "FY2019": "FY2019†‡",
}

AR25_URL = "https://chetwoodbank.co.uk/documents/chetwood-bank-annual-report.pdf"
AR24_URL = "http://web.archive.org/web/20240920030034id_/https://chetwood.co/static/97d26e488d5277699e5b9a9983db4d5b/AnnualReport.pdf"
AR22_URL = "http://web.archive.org/web/20230131231341id_/https://chetwood.co/static/7fbc3d1ed9c0913dca3435f640a5a570/AnnualReport.pdf"
AR21_URL = "http://web.archive.org/web/20210830132929id_/https://chetwood.co/static/3d0ade6e892213e246ca03dc1d84b417/AnnualReport.pdf"
AR20_URL = "https://find-and-update.company-information.service.gov.uk/company/09964966/filing-history/MzI3NDIxOTQ2OWFkaXF6a2N4/document?format=pdf&download=0"
AR19_URL = "https://find-and-update.company-information.service.gov.uk/company/09964966/filing-history/MzI0MTExMzg0OGFkaXF6a2N4/document?format=pdf&download=0"

P3_25_URL = "https://chetwoodbank.co.uk/documents/chetwood-bank-pillar-three-disclosures.pdf"
# FOUND 2026-09-19 (GA-020 second pass). The FY2024 edition ("Pillar 3 Disclosures November 2024",
# "as at 31 March 2024", 15 pp., PDF created 5 Dec 2024) was never at a chetwood.co or
# chetwoodbank.co.uk address: the chetwoodbank.co.uk site is built on the Sanity CMS and served its
# documents from the CDN host cdn.sanity.io. Archived chetwoodbank.co.uk homepages (Wayback
# 20250430162819, 20250515011815) link this file under "Pillar Three Disclosures"; the Nov-2024 and
# Jan-2025 captures link an earlier file, .../9f8bdd8617631ef0b2fae5ed91acdd4e7273727f.pdf, which is the
# FY2023 edition ("January 2024", as at 31 March 2023) already cited below via chetwood.co. Both files
# were live on cdn.sanity.io on 2026-09-19 (HTTP 200, application/pdf, %PDF magic; this one 347,693
# bytes). Every earlier search missed it because it looked only on the bank's own two domains.
# FY2025 EDITION COMPARISON, 2026-09-19 (GA-020 leads pass). Question: is the "September 2025" edition this
# script cites a different file from the one now live (PDF created 7 Nov 2025), i.e. a restatement?
FY2025_EDITION_CHECK = (
    "FY2025 EDITION CHECK, 2026-09-19. 'September 2025' is the cover date printed on the live file, not a "
    "separate edition. The live undated URL (P3_25_URL) was re-downloaded on 2026-09-19 (HTTP 200, "
    "application/pdf, %PDF-1.7, 368,755 bytes, 15 pp., cover 'Pillar 3 Disclosures September 2025', 'as at 31 "
    "March 2025'; PDF CreationDate 7 Nov 2025 15:27:41 GMT, ModDate 15:27:42 GMT; MD5 b0be18a50b91c88280a99aced75e2265). "
    "The copies other sessions saved earlier in 2026 are byte-identical to it, and this workbook's FY2025 figures "
    "were first transcribed in 2026, so they come from this 7 Nov 2025 file. Every FY2025 figure the workbook "
    "carries was compared with it on 2026-09-19 and ALL MATCH: KM1 (Section 5, printed pp.9-10) rows 1-3 "
    "187,605; 4 1,233,321; 5-7 15.2%; UK 7a 1.92%; UK 7b/7c '-'; UK 7d 9.92%; 8 2.50%; 9 2.00%; 11 4.50%; "
    "UK 11a 14.42%; 12 5.29%; 13 3,615,720; 14 5.19%; 15 897,493; UK 16a 489,794; UK 16b 28,009; 16 461,785; "
    "17 194%; 18 3,677,559; 19 2,536,343; 20 145%; and OV1 (Section 6.3, printed p.11) 2025 column credit risk "
    "1,017,779, CCR 23,777, securitisation 102,610, operational risk 89,154, total 1,233,321, plus its 2024 "
    "comparative 703,828 / 13,638 / 62,980 / 44,177 / 824,623, which also equals the FY2024 edition's own "
    "figures. No other FY2025 copy was found, so no second edition could be compared: Wayback CDX holds no "
    "capture of any chetwoodbank.co.uk/documents/ URL (prefix query); the nine cdn.sanity.io PDFs linked from "
    "archived homepages of Nov 2024-Jun 2025 are the FY2023/FY2024 Pillar 3, AR2024, complaints, governance, "
    "gender-pay, tax and supplier documents, none the FY2025 Pillar 3; CDX of cdn.sanity.io/files/cdijb9eo/ "
    "holds 7 files, none of them it; homepages from 7 Aug 2025 onward link only the undated /documents/ path; "
    "archive.ph has no copy (404); a web search returned none. The homepage of 7 Aug 2025 already links the "
    "/documents/ Pillar 3 path, so an earlier file may have been served there before 7 Nov 2025. It was never "
    "captured, so whether it differs is unreached, not established."
)
P3_24_URL = "https://cdn.sanity.io/files/cdijb9eo/production/c43453174d3cd53859ae5bf91d91ff6a901b314b.pdf"
P3_23_URL = "http://web.archive.org/web/20240315022245id_/https://chetwood.co/static/330c40d433df90b83d3b3e5c673e21cc/Pillar3Disclosures.pdf"
P3_22_URL = "http://web.archive.org/web/20230131235943id_/https://chetwood.co/static/815e2dd174c4655ddf55a93ca1029ce3/Pillar3Disclosures.pdf"
P3_21_URL = "http://web.archive.org/web/20211128171331id_/https://chetwood.co/static/221a3946677e4d8c49c5525d22f9b534/Pillar3Disclosures.pdf"
# Located 2026-09-15 via a Wayback CDX scan of the whole chetwood.co domain. This
# is a genuine 23-page "Pillar 3 Disclosures, June 2020 / as at 31st March 2020"
# PDF (767,512 bytes, real text layer) that earlier sessions missed - the page
# count was recorded as 8 in error and corrected 2026-09-16 after a full
# download of the id_ capture (pdfinfo: 23 pages, last printed page 22, which
# is what the "p.18" citations below rely on) - it predates the
# "as at 31 March 2021" edition previously believed to be Chetwood's earliest,
# and it populates the FY2020 column on every Pillar 3 sheet below.
P3_20_URL = "http://web.archive.org/web/20200929085826id_/https://chetwood.co/static/ea27728be3ae831ddb0ef7888e332546/Pillar3Disclosures.pdf"

ENTITY_NOTE = (
    "ENTITY NOTE: Chetwood Financial Limited (trading as Chetwood Bank) is the entity on the PRA register - no "
    "holding-company substitution was needed here (unlike Monzo). All years are Chetwood Financial Limited, "
    "consolidated/Group basis, EXCEPT FY2021-FY2019 (marked †), which are Chetwood's own standalone entity "
    "accounts - the Group didn't exist yet (Chetwood acquired Yobota Limited on 1 March 2022, and CHL Mortgages "
    "for Intermediaries Limited later still), so there is no consolidated cash flow statement before FY2022. "
    "Companies House confirms FY2019-FY2021 accounts were filed as 'Full accounts' (solo), while FY2022-FY2025 "
    "were filed as 'Group of companies' accounts' (consolidated). Per user direction, FY2019-FY2021 are included "
    "on a standalone basis and clearly flagged, rather than omitted.\n"
    "FY2024 is consolidated. Its Pillar 3 ('Pillar 3 Disclosures November 2024', as at 31 March 2024) was long "
    "believed unpublished and was located on 2026-09-19 on the bank's CMS file host (cdn.sanity.io) - see the "
    "note on each Pillar 3 sheet.\n\n"
    "HISTORICAL-DEPTH FLOOR NOTE (added 2026-09-06, HD-023): the workbook's true floor is FY2019, not FY2016 as "
    "originally listed on that ticket, and not FY2021 as a since-corrected version of the same ticket guessed. "
    "Verified against Chetwood's own Companies House filing history (company no. 09964966, incorporated 22 Jan "
    "2016) and its own statutory accounts, not a domain/snapshot scan:\n"
    "- Period to 31 Dec 2016: dormant shell only ('Total exemption full accounts', total assets £954k, no lending "
    "or deposits) - pre-banking, excluded.\n"
    "- FY2018 (15-month period, 1 Jan 2017 - 31 Mar 2018): the Company was granted a banking licence WITH "
    "RESTRICTIONS only on 22 Dec 2017; consumer lending commenced Feb 2018 (2 months of the 15-month period); "
    "there were zero customer deposits all period (total assets £7.1m, no deposit-taking yet) - this is a "
    "pre-launch/development-stage period, not a genuine operating bank year, so excluded as a self-skipped year "
    "despite audited accounts existing for it.\n"
    "- FY2019 (year ended 31 Mar 2019): the PRA's restrictions on the banking licence were lifted 13 Dec 2018; "
    "this is the first year with real customer deposits (£26.1m) and a meaningful loan book (£46.3m) - i.e. the "
    "first genuine full year of Chetwood operating as an unrestricted retail bank. Treated as the floor.\n"
    "- FY2019 and FY2020 statutory accounts (like FY2018's) were prepared under UK GAAP FRS 102, NOT IFRS - "
    "Chetwood only adopted IFRS (and IFRS 9 stage-based credit-quality disclosure, and Pillar 3 reporting) from "
    "FY2021 onward, per its own accounting-policy notes ('in compliance with...FRS 102') each year 2018-2020. "
    "This is analogous to the ticket's flagged Basel II/CET1 terminology shift, but for the whole accounting "
    "framework: FY2019-FY2020 (marked ‡) have no IFRS 9 loan-stage table. "
    "SUPERSEDED IN PART (2026-09-15): this note previously also claimed FY2019 and FY2020 had 'no Pillar 3 "
    "disclosure at all' and that all 11 Pillar 3 metric sheets plus the RWA Breakdown sheet were genuinely not "
    "disclosed for both years. That holds for FY2019 only. A 'Pillar 3 Disclosures June 2020 (as at 31st March "
    "2020)' document was located 2026-09-15 and FY2020 is now populated across the Pillar 3 sheets - see the "
    "source note on any Pillar 3 sheet for the document and the correction. The accounting-framework point "
    "itself is unaffected: FY2019 and FY2020 statutory accounts remain FRS 102, and that FY2020 Pillar 3 "
    "document says so itself ('Chetwood currently prepares its Financial Statements under FRS 102. Chetwood has "
    "developed an IFRS9 expected loss model that will be adopted in due course').\n"
    "- A further consequence of the FRS 102-to-IFRS transition: the FY2021 Annual Report's own FY2020 comparative "
    "equity balance (used as the prior-year opening figure in that report) does not exactly match FY2020's own "
    "originally-filed Statement of Changes in Equity (originally-filed closing Profit and Loss account -£36,357k, "
    "Total Equity £51,182k, vs the FY2021 AR's stated FY2020-closing comparative of -£44,513k / £43,067k, a "
    "~£8.1m gap most likely reflecting transition adjustments on first-time IFRS application). The Statement of "
    "Changes in Equity sheet below uses Chetwood's own FY2019/FY2020 AS-FILED figures for the FY2019-FY2020 rows "
    "(matching those years' own Balance Sheet), and switches to the FY2021 AR's own stated FY2020-comparative "
    "opening balance only at the point the FY2021 movements begin - the ~£8.1m gap is disclosed here rather than "
    "silently bridged."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are Chetwood Financial Limited Group (consolidated) cash flow statement, £'000, unless "
    "noted. See entity note above re: FY2021 (standalone) and FY2024 (Pillar 3 gap).\n"
    f"FY2025: Chetwood Financial Limited Annual Report and Financial Statements, year ended 31 March 2025, "
    f"p.48-49 (Consolidated and company statement of cashflows) - {AR25_URL}\n"
    f"FY2024: Chetwood Financial Limited Annual Report and Financial Statements, year ended 31 March 2024, "
    f"p.29 (Consolidated and Company Statement of Cashflows) - {AR24_URL}\n"
    f"FY2023: Chetwood Financial Limited Annual Report and Financial Statements, year ended 31 March 2024, "
    f"p.29 (prior-year comparative column) - {AR24_URL}. (The FY2023 Annual Report's own PDF has a text-encoding "
    f"fault that corrupts extracted figures; the FY2024 report's clean comparative column was used instead - "
    f"both present the same audited FY2023 statutory figures.)\n"
    f"FY2022: Chetwood Financial Limited Annual Report and Financial Statements, year ended 31 March 2022, "
    f"p.26 (Consolidated and Company Statement of Cashflows) - {AR22_URL}\n"
    f"FY2021: Chetwood Financial Limited Annual Report and Financial Statements, year ended 31 March 2021, "
    f"p.28 (Statement of Cashflows, standalone entity) - {AR21_URL}\n"
    f"FY2020: Chetwood Financial Limited Annual Report and Financial Statements, year ended 31 March 2020, "
    f"p.22 (Statement of Cashflows, standalone entity, FRS 102 basis) - {AR20_URL} (Companies House filing history, "
    f"company no. 09964966)\n"
    f"FY2019: Chetwood Financial Limited Annual Report and Financial Statements, year ended 31 March 2019, "
    f"p.17 (Statement of Cashflows, standalone entity, FRS 102 basis) - {AR19_URL} (Companies House filing history, "
    f"company no. 09964966)\n\n" + ENTITY_NOTE + "\n\n"
    "PRESENTATION NOTE: Line items changed across the five years as the business grew (e.g. debt securities and "
    "derivative-related lines were introduced/split differently year to year, and FY2025 switched the starting "
    "line from 'Loss after tax' to '(Loss)/profit before tax'). Blank cells indicate that year's report did not "
    "disclose that specific split. Section totals (net cash from operating/investing/financing, cash and cash "
    "equivalents) are consistent and reconcile exactly across all 5 years.\n\n"
    "DATA QUALITY NOTE (added 2026-08-27, found during a project-wide sanity check): the AR24/AR25 source "
    "statements print BOTH a Group and a Company column side by side for each year; three line items were "
    "originally transcribed from the wrong column or with a digit error, causing FY2023/FY2024's operating and "
    "investing TOTALs to not reconcile to their own line items. Corrected against both AR24 (own-year figures) "
    "and AR25's FY2024 comparative column (cross-checked, both agree): 'Fair value adjustment on hedged items' "
    "FY2024 corrected from -11,182 to the Group figure -11,782 (a transcription slip); 'Interest received from "
    "investing activities' FY2024 corrected from 11,601 to the Group figure 17,601 (transcription slip); 'Loss on "
    "disposal of property, plant and equipment' FY2023 corrected from 4 to the Group figure 8 (was the Company "
    "figure); 'Impairment of investment in subsidiary/Yobota' FY2023 corrected from 6,753 to 0/nil (the Group "
    "figure is nil - 6,753 was the Company-only figure); 'Subscription of shares in subsidiary undertaking' "
    "FY2023 (-1,500) removed entirely - it is a Company-only line with no Group-basis equivalent, so it never "
    "belonged in this Group-basis statement. All four sections now reconcile exactly to the penny against the "
    "primary source.\n\n"
    "FY2019/FY2020 PRESENTATION NOTE: these two years' statements (FRS 102 basis) do not split depreciation from "
    "amortisation, so a single combined line is shown for those years only rather than force-splitting it across "
    "the FY2021+ 'Depreciation of property, plant and equipment' / 'Amortisation of intangibles' rows. 'Purchase "
    "of financial investments' (debt securities) is classified by Chetwood's own FY2019/FY2020 statements under "
    "Financing activities, not Investing activities as in every later year - kept in its own as-disclosed section "
    "rather than moved. FY2020's own statement shows FY2019 comparative figures (£27,620k operating cashflow, "
    "£25,109k net cashflow for the period, £27,608k closing cash) that differ by £1k from FY2019's own filed "
    "figures (£27,621k / £25,108k / £27,607k) used here - an immaterial rounding difference between the two "
    "filings, not corrected."
)

def p3_sources(extra_note=""):
    return (
        "Sources (see entity note on Cash Flow Statement sheet):\n"
        f"FY2025: Chetwood Bank Pillar 3 Disclosures, September 2025 (as at 31 March 2025), Section 5 (Key Metrics "
        f"- KM1) - {P3_25_URL}\n" + FY2025_EDITION_CHECK + "\n"
        f"FY2024: Chetwood Bank Pillar 3 Disclosures, November 2024 (as at 31 March 2024), Section 5 (Key Metrics "
        f"- KM1) pp.10-11 of 15 and Section 6.3 (OV1) p.12 - {P3_24_URL}\n"
        f"FY2024 CORRECTION, 2026-09-19. Until 2026-09-19 this workbook said that no FY2024 Pillar 3 "
        f"was ever published, after a search of chetwood.co and chetwoodbank.co.uk (live site, dated URL variants, "
        f"Wayback CDX of both domains) and of both Annual Reports. That was a claim about our search, not about the "
        f"bank: the edition exists and was on the CMS file host cdn.sanity.io all along, linked from the bank's own "
        f"homepage (Wayback 20250430162819). Its KM1 column is headed '2023' although the document states on p.3 "
        f"that it is 'as at 31 March 2024' and its KM1 row 4 (824,623) equals the OV1 table's '2024' column on p.12 "
        f"(and the FY2025 edition's 2024 comparative), so the '2023' heading is a source labelling defect, "
        f"reproduced in this note rather than corrected in the data.\n"
        f"OUT-OF-SCOPE LEAD (not acted on here): that CDX scan also turned up an un-cited Pillar 3 snapshot at "
        f"http://web.archive.org/web/20200929085826id_/https://chetwood.co/static/"
        f"ea27728be3ae831ddb0ef7888e332546/Pillar3Disclosures.pdf, captured Sept 2020 - i.e. predating the "
        f"'as at 31 March 2021' edition this workbook currently treats as Chetwood's earliest. It was not "
        f"opened or transcribed in this pass (the FY2019/FY2020 columns are an exterior, not interior, gap and "
        f"were out of scope), but it should be checked before the FY2019/FY2020 'no Pillar 3 was ever "
        f"published' claim below is relied on.\n"
        f"FY2023: Chetwood Financial Ltd Pillar 3 Disclosure, as at 31 March 2023, Section 6 (Key Metrics - KM1) "
        f"and Section 7.1 (Capital Resources) - {P3_23_URL}\n"
        f"FY2022: Chetwood Financial Ltd Pillar 3 Disclosure, as at 31 March 2022, Annex B (Key Metrics - KM1) "
        f"- {P3_22_URL}\n"
        f"FY2021: Chetwood Financial Ltd Pillar 3 Disclosure, as at 31 March 2021, Section 1.2 (Summary Analysis) "
        f"and Section 4 (Capital Resources) - {P3_21_URL} (pre-dates the formal KM1 template; Chetwood adopted the "
        f"CRR KM1 annex from the FY2022 report onward)\n"
        f"FY2020: Chetwood Financial Ltd Pillar 3 Disclosures, June 2020 ('as at 31st March 2020'), Section 1.2 "
        f"(Summary analysis, p.3), Section 3.3 (Capital Resources, p.15), Section 3.6 (The leverage ratio, p.16) "
        f"and Section 5.2 (Liquidity ratios, p.18) - {P3_20_URL}\n"
        f"CORRECTION (2026-09-15): earlier versions of this workbook stated that 'no Pillar 3 disclosure was ever "
        f"published' for FY2019/FY2020 and that the 'as at 31 March 2021' edition was Chetwood's earliest. That "
        f"was wrong for FY2020. A Wayback CDX scan of the whole chetwood.co domain surfaced a 23-page 'Pillar 3 "
        f"Disclosures June 2020' PDF at an un-cited static path (captured 29 Sept 2020, real text layer, 767KB - "
        f"not a soft 404), carrying a full FY2020 capital/leverage/liquidity set. Every FY2020 Pillar 3 figure in "
        f"this workbook comes from that document. It pre-dates the formal KM1 template (like the FY2021 edition), "
        f"so its figures are narrative/summary-table style rather than KM1 rows; the capital-resources table's "
        f"build-up (share capital 84,688 + share premium 2,851 + retained earnings (36,357) - intangibles (485) = "
        f"CET1 50,697) ties exactly to the FY2020 Balance Sheet sheet's own as-filed FRS 102 figures, an "
        f"independent confirmation that the document is Chetwood's own and is for the right year.\n"
        f"FY2019: still genuinely blank. The FY2020 document is a single-column 'as at 31 March 2020' disclosure "
        f"with no FY2019 comparative anywhere in it, and no earlier Pillar 3 snapshot exists in the Wayback CDX "
        f"index for either chetwood.co or chetwoodbank.co.uk (Chetwood's own FY2018/FY2019 strategic reports say "
        f"a Pillar 3 document 'will be published...in due course')." + (f"\n{extra_note}" if extra_note else "")
    )

bw = BankWorkbook(bank_name="Chetwood Financial Limited", years=YEARS, year_label=YEAR_LABEL, header_color="003232")

STATEMENTS_SOURCES = (
    "Sources - Chetwood Financial Limited's own Consolidated Statement of Financial Position / Statement of Total "
    "Comprehensive Income / Statement of Changes in Equity, transcribed from each year's own Annual Report (not a "
    "later year's comparative column, except where noted). See entity note below re: FY2021 (standalone) and the "
    "FY2024 P&L OCR-corruption note.\n"
    f"FY2025/FY2024: Chetwood Financial Limited Annual Report and Financial Statements, year ended 31 March 2025, "
    f"p.44-47 (Consolidated Statement of Financial Position / Statement of Total Comprehensive Income / Statement "
    f"of Changes in Equity) - {AR25_URL}\n"
    f"FY2023: Chetwood Financial Limited Annual Report and Financial Statements, year ended 31 March 2024, "
    f"p.24-27 (prior-year comparative column) - {AR24_URL}. (As with the Cash Flow Statement, the FY2023 Annual "
    f"Report's own PDF has a text-encoding fault; the FY2024 report's clean comparative column was used instead - "
    f"both present the same audited FY2023 statutory figures.)\n"
    f"FY2022/FY2021: Chetwood Financial Limited Annual Report and Financial Statements, year ended 31 March 2022, "
    f"p.22-25 (Consolidated Statement of Financial Position / Statement of Total Comprehensive Income / Statement "
    f"of Changes in Equity, Group and Company for FY2021) - {AR22_URL}\n"
    f"FY2020: Chetwood Financial Limited Annual Report and Financial Statements, year ended 31 March 2020, "
    f"p.19-21 (Statement of Total Comprehensive Income / Statement of Financial Position / Statement of Changes "
    f"in Equity, standalone entity, FRS 102 basis) - {AR20_URL} (Companies House filing history, company no. "
    f"09964966)\n"
    f"FY2019: Chetwood Financial Limited Annual Report and Financial Statements, year ended 31 March 2019, "
    f"p.14-16 (Statement of Total Comprehensive Income / Statement of Financial Position / Statement of Changes "
    f"in Equity, standalone entity, FRS 102 basis) - {AR19_URL} (Companies House filing history, company no. "
    f"09964966)\n\n" + ENTITY_NOTE + "\n\n"
    "DATA QUALITY NOTE: the FY2024 Annual Report's own P&L page (used for FY2023's comparative column) has the "
    "same text-encoding fault as its Cash Flow Statement page, corrupting individual digits in places (e.g. that "
    "page's own FY2024 'Impairment of loans and advances to customers' prints as -855, matching the clean FY2025 "
    "report's comparative figure exactly). The equity statement page in the same FY2024 report similarly corrupts "
    "one FY2024 'Total comprehensive income' cell (prints -8,605 instead of -8,685) - the FY2025 report's own "
    "FY2023-25 equity table and the P&L's own OCI total agree exactly on -8,685, so -8,685 is used here.\n\n"
    "INVESTMENT IN DEBT SECURITIES BREAKDOWN NOTE (added 2026-09-07): 'Investment in debt securities' is split into "
    "'UK government treasury bills, measured at FVOCI' and 'Other debt securities (ABS loan notes / fixed rate bonds "
    "/ covered bonds / senior loan notes), at amortised cost', sourced from each year's own Note 14/15/16 "
    "('Investment in debt securities'), which reconciles exactly to the original total in every year it is "
    "disclosed:\n"
    f"FY2025/FY2024: Annual Report 2025, p.71 (Note 14) - {AR25_URL}. FY2025: FVOCI Treasury Bills £202,151k; "
    "amortised cost £1,119,515k (ABS £525,248k + Fixed rate bonds £384,031k + Covered bonds £39,059k + Senior loan "
    "notes £171,177k). FY2024: no Treasury Bills held (FVOCI leg £nil); amortised cost £537,291k (ABS £435,075k + "
    "Fixed rate bonds £102,216k).\n"
    f"FY2023: Annual Report 2024, p.40 (Note 15, FY2023 comparative column) - {AR24_URL}. FVOCI Treasury Bills "
    "£4,825k; amortised cost £124,770k (ABS loan notes only).\n"
    f"FY2022: Annual Report 2022, p.39 (Note 16) - {AR22_URL}. The entire £4,883k balance is Treasury Bills measured "
    "at FVOCI ('all instruments are investments in UK sovereign treasury bills') - no amortised-cost leg that year.\n"
    "FY2020/FY2019: no note breaks down this line at all in either year's own Annual Report - the Statement of "
    "Financial Position shows 'Investment in debt securities' with no note-reference number next to it (unlike "
    "every other line, which cross-references a numbered note), confirmed by reading both years' full note set "
    "(pages 23-39 of the FY2020 AR, pages 18-32 of the FY2019 AR) - genuinely no further detail available for "
    "these two years.\n\n"
    "PRESENTATION NOTE: 'Cash and cash equivalents' (FY2023-25) and 'Loans and advances to banks' (FY2021-22) are "
    "the same balance-sheet line under two labels - shown on one row. 'Capital redemption reserve' (FY2023-25) and "
    "'Capital contribution' (FY2022, first appearing that year as a debt waiver from the ultimate controlling "
    "party) are the same £6,247k reserve under two labels - shown on one row. P&L structure changed across the "
    "five years as the business grew: FY2025 nets fee income/expense into a single 'Net fee and commission "
    "(expense)/income' line with no separate 'Other income' row; FY2022-23 include a 'Net gain arising from "
    "derecognition of financial assets at amortised cost' line with no FY2024-25 equivalent; only FY2024-25 "
    "disclose 'Deferred tax liabilities' or a 'Goodwill' balance sheet line, both absent 2021-23; only FY2025 "
    "discloses 'Debt securities in issue' as a live balance (£89k), though the line existed as a zero balance from "
    "FY2024. Blank cells indicate that year's report did not disclose that specific line."
)

# ---------------------------------------------------------------
# Sheet: Balance Sheet
# ---------------------------------------------------------------
balance_sheet_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and cash equivalents / Loans and advances to banks", {"FY2025": 387550, "FY2024": 586134, "FY2023": 688362, "FY2022": 74498, "FY2021": 52173, "FY2020": 88480, "FY2019": 27607}),
    ("DATA", "Derivative financial assets", {"FY2025": 49410, "FY2024": 58475, "FY2023": 4565, "FY2022": 138, "FY2021": 19, "FY2020": 4}),
    ("DATA", "UK government treasury bills, measured at FVOCI", {"FY2025": 202151, "FY2024": 0, "FY2023": 4825, "FY2022": 4883}),
    ("DATA", "Other debt securities (ABS loan notes / fixed rate bonds / covered bonds / senior loan notes), at amortised cost", {"FY2025": 1119515, "FY2024": 537291, "FY2023": 124770, "FY2022": 0}),
    ("TOTAL", "Investment in debt securities - total", {"FY2025": 1321666, "FY2024": 537291, "FY2023": 129595, "FY2022": 4883, "FY2020": 30170, "FY2019": 1994}),
    ("DATA", "Loans and advances to customers", {"FY2025": 2691247, "FY2024": 1833411, "FY2023": 649179, "FY2022": 302546, "FY2021": 156249, "FY2020": 145022, "FY2019": 46269}),
    ("DATA", "Fair value adjustments on hedged assets", {"FY2025": 5615, "FY2024": 12926, "FY2023": -1069}),
    ("DATA", "Other assets", {"FY2025": 63998, "FY2024": 43910, "FY2023": 18897, "FY2022": 8620, "FY2021": 3486, "FY2020": 605, "FY2019": 448}),
    ("DATA", "Prepayments and accrued income", {"FY2025": 4177, "FY2024": 4353, "FY2023": 999, "FY2022": 930, "FY2021": 555, "FY2020": 810, "FY2019": 406}),
    ("DATA", "Property, plant and equipment", {"FY2025": 913, "FY2024": 883, "FY2023": 1246, "FY2022": 690, "FY2021": 819, "FY2020": 477, "FY2019": 557}),
    ("DATA", "Intangible assets", {"FY2025": 2044, "FY2024": 521, "FY2023": 2767, "FY2022": 7669, "FY2021": 3178, "FY2020": 485, "FY2019": 486}),
    ("DATA", "Goodwill", {"FY2025": 5927}),
    ("TOTAL", "Total assets", {"FY2025": 4532547, "FY2024": 3077904, "FY2023": 1494541, "FY2022": 400038, "FY2021": 216524, "FY2020": 266053, "FY2019": 77767}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Customer deposits", {"FY2025": 3812429, "FY2024": 2856737, "FY2023": 1383305, "FY2022": 322625, "FY2021": 160015, "FY2020": 210783, "FY2019": 26107}),
    ("DATA", "Fair value adjustments on hedged liabilities", {"FY2025": 621, "FY2024": -1073, "FY2023": -3286}),
    ("DATA", "Provisions", {"FY2025": 2252, "FY2024": 2909, "FY2023": 2015, "FY2022": 591}),
    ("DATA", "Amounts owed to credit institutions", {"FY2025": 488932, "FY2024": 9107}),
    ("DATA", "Debt securities in issue", {"FY2025": 89, "FY2024": 99}),
    ("DATA", "Accruals", {"FY2025": 10864, "FY2024": 9766, "FY2023": 7279, "FY2022": 6790, "FY2021": 4127, "FY2020": 2768, "FY2019": 1649}),
    ("DATA", "Derivative financial liabilities", {"FY2025": 12216, "FY2024": 18713, "FY2023": 6645, "FY2022": 457, "FY2021": 5, "FY2020": 9}),
    ("DATA", "Other liabilities", {"FY2025": 8795, "FY2024": 8564, "FY2023": 6100, "FY2022": 3582, "FY2021": 1547, "FY2020": 1311, "FY2019": 527}),
    ("DATA", "Deferred tax liabilities", {"FY2025": 206}),
    ("TOTAL", "Total liabilities", {"FY2025": 4336404, "FY2024": 2904822, "FY2023": 1402058, "FY2022": 334045, "FY2021": 165694, "FY2020": 214871, "FY2019": 28283}),
    ("SECTION", "Equity", {}),
    ("DATA", "Called up share capital", {"FY2025": 253913, "FY2024": 253730, "FY2023": 253297, "FY2022": 168688, "FY2021": 113688, "FY2020": 84688, "FY2019": 64688}),
    ("DATA", "Share premium account", {"FY2025": 118236, "FY2024": 91418, "FY2023": 2851, "FY2022": 2851, "FY2021": 2851, "FY2020": 2851, "FY2019": 2851}),
    ("DATA", "Capital redemption reserve / Capital contribution", {"FY2025": 6247, "FY2024": 6247, "FY2023": 6247, "FY2022": 6247}),
    ("DATA", "Other reserves", {"FY2025": 877, "FY2024": 692, "FY2023": 232, "FY2022": 203, "FY2021": 114}),
    ("DATA", "Retained losses", {"FY2025": -183900, "FY2024": -179775, "FY2023": -170914, "FY2022": -112766, "FY2021": -65823, "FY2020": -36357, "FY2019": -18055}),
    ("DATA", "Merger reserve", {"FY2025": 770, "FY2024": 770, "FY2023": 770, "FY2022": 770}),
    ("TOTAL", "Total equity", {"FY2025": 196143, "FY2024": 173082, "FY2023": 92483, "FY2022": 65993, "FY2021": 50830, "FY2020": 51182, "FY2019": 49484}),
    ("TOTAL", "Total liabilities and equity", {"FY2025": 4532547, "FY2024": 3077904, "FY2023": 1494541, "FY2022": 400038, "FY2021": 216524, "FY2020": 266053, "FY2019": 77767}),
]

bw.add_balance_sheet_sheet(
    title="Chetwood Financial Limited — Consolidated Statement of Financial Position",
    subtitle="£'000. Consolidated (Group) basis except FY2019-FY2021 († standalone entity - Group and Company are identical those years; FY2019-FY2020 also FRS 102 basis, marked ‡). See source note at bottom.",
    rows=balance_sheet_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=58,
    source_height=220,
)

# ---------------------------------------------------------------
# Sheet: Profit & Loss
# ---------------------------------------------------------------
income_statement_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest income calculated using the effective interest rate method", {"FY2025": 216716, "FY2024": 149127, "FY2023": 35406, "FY2022": 29755, "FY2021": 17567, "FY2020": 9687, "FY2019": 2666}),
    ("DATA", "Interest payable and similar charges", {"FY2025": -174940, "FY2024": -104811, "FY2023": -14914, "FY2022": -2542, "FY2021": -3135, "FY2020": -2014, "FY2019": -967}),
    ("TOTAL", "Net interest income", {"FY2025": 41776, "FY2024": 44316, "FY2023": 20492, "FY2022": 27213, "FY2021": 14432, "FY2020": 7673, "FY2019": 1699}),
    ("DATA", "Fee and commission income", {"FY2025": 851, "FY2024": 1794, "FY2023": 2731, "FY2022": 244}),
    ("DATA", "Fee and commission expense", {"FY2025": -4758, "FY2024": -3162, "FY2023": -718, "FY2022": -152}),
    ("TOTAL", "Net fee and commission income/(expense)", {"FY2025": -3907, "FY2024": -1368, "FY2023": 2013, "FY2022": 92}),
    ("DATA", "Net income/(expense) from financial instruments held at fair value through profit and loss", {"FY2025": 16369, "FY2024": 3041, "FY2023": -1160, "FY2022": 108, "FY2021": 15}),
    ("DATA", "Other income", {"FY2023": 126, "FY2022": 15}),
    ("TOTAL", "Total income", {"FY2025": 54238, "FY2024": 45989, "FY2023": 21471, "FY2022": 27428, "FY2021": 14447, "FY2020": 7673, "FY2019": 1699}),
    ("DATA", "Administrative expenses", {"FY2025": -57209, "FY2024": -53995, "FY2023": -56119, "FY2022": -30809, "FY2021": -22372, "FY2020": -14413, "FY2019": -11240}),
    ("DATA", "Impairment of loans and advances to customers", {"FY2025": -1731, "FY2024": -855, "FY2023": -25126, "FY2022": -30737, "FY2021": -13375, "FY2020": -11574, "FY2019": -1995}),
    ("DATA", "Net gain arising from derecognition of financial assets measured at amortised cost", {"FY2023": 1727, "FY2022": 4369}),
    ("TOTAL", "Loss before taxation", {"FY2025": -4702, "FY2024": -8861, "FY2023": -58047, "FY2022": -29749, "FY2021": -21300, "FY2020": -18314, "FY2019": -11536}),
    ("DATA", "Taxation", {"FY2023": -101, "FY2022": -4, "FY2021": -10}),
    ("TOTAL", "Loss after tax and loss for the year", {"FY2025": -4702, "FY2024": -8861, "FY2023": -58148, "FY2022": -29753, "FY2021": -21310, "FY2020": -18314, "FY2019": -11536}),
    ("SECTION", "Other comprehensive income/(expense)", {}),
    ("DATA", "Fair value gains/(losses) on debt instruments during the year", {"FY2025": 824, "FY2024": 145, "FY2023": -178, "FY2022": -120, "FY2021": 5}),
    ("DATA", "Debt instruments at FVOCI - reclassified to profit or loss", {"FY2025": 0, "FY2024": 31, "FY2023": 2, "FY2021": -34}),
    ("DATA", "Deferred tax on fair value gains on debt instruments", {"FY2025": -206}),
    ("TOTAL", "Total other comprehensive income/(expense) for the year", {"FY2025": 618, "FY2024": 176, "FY2023": -176, "FY2022": -120, "FY2021": -29}),
    ("TOTAL", "Total comprehensive loss for the year", {"FY2025": -4084, "FY2024": -8685, "FY2023": -58324, "FY2022": -29873, "FY2021": -21339, "FY2020": -18314, "FY2019": -11536}),
]

bw.add_income_statement_sheet(
    title="Chetwood Financial Limited — Consolidated Statement of Total Comprehensive Income",
    subtitle="£'000. Consolidated (Group) basis except FY2019-FY2021 († standalone entity - Group and Company are identical those years; FY2019-FY2020 also FRS 102 basis, marked ‡). See source note at bottom.",
    rows=income_statement_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=66,
    source_height=220,
)

# ---------------------------------------------------------------
# Sheet: Statement of Changes in Equity
# ---------------------------------------------------------------
equity_headers = [
    "Called-up Share Capital", "Share Premium", "Retained losses", "Share-based payment reserve",
    "Debt securities revaluation reserve", "Capital redemption/contribution reserve", "Merger reserve", "Total equity",
]
equity_rows = [
    ("TOTAL", "At 1 April 2018", (9451, 2851, -6519, None, None, None, None, 5783)),
    ("DATA", "Issue of shares", (55237, None, None, None, None, None, None, 55237)),
    ("DATA", "Loss for the period (FY2019)", (None, None, -11536, None, None, None, None, -11536)),
    ("TOTAL", "At 31 March 2019", (64688, 2851, -18055, None, None, None, None, 49484)),
    ("DATA", "Issue of shares", (20000, None, None, None, None, None, None, 20000)),
    ("DATA", "Equity-settled share-based payment transactions", (None, None, 12, None, None, None, None, 12)),
    ("DATA", "Loss for the period (FY2020)", (None, None, -18314, None, None, None, None, -18314)),
    ("TOTAL", "At 31 March 2020 (as filed in the FY2020 accounts)", (84688, 2851, -36357, None, None, None, None, 51182)),
    ("TOTAL", "At 1 April 2020 (per FY2021 AR's own comparative - see gap note)", (84688, 2851, -44513, 12, 29, None, None, 43067)),
    ("DATA", "Loss for the period (FY2021)", (None, None, -21310, None, None, None, None, -21310)),
    ("DATA", "Net changes in fair value", (None, None, None, None, 5, None, None, 5)),
    ("DATA", "Reclassified to income statement", (None, None, None, None, -34, None, None, -34)),
    ("DATA", "Equity-settled share-based payment transactions", (None, None, None, 102, None, None, None, 102)),
    ("DATA", "Issue of shares", (29000, None, None, None, None, None, None, 29000)),
    ("TOTAL", "At 31 March 2021", (113688, 2851, -65823, 114, 0, None, None, 50830)),
    ("DATA", "Loss for the period (FY2022)", (None, None, -29753, None, None, None, None, -29753)),
    ("DATA", "Retained losses acquired on purchase of subsidiary", (None, None, -17190, None, None, None, None, -17190)),
    ("DATA", "Net changes in fair value", (None, None, None, None, -120, None, None, -120)),
    ("DATA", "Equity-settled share-based payment transactions", (None, None, None, 209, None, None, None, 209)),
    ("DATA", "Debt waiver by ultimate controlling party", (None, None, None, None, None, 6247, None, 6247)),
    ("DATA", "Merger reserve arising on consolidation", (None, None, None, None, None, None, 770, 770)),
    ("DATA", "Issue of shares", (55000, None, None, None, None, None, None, 55000)),
    ("TOTAL", "At 31 March 2022", (168688, 2851, -112766, 323, -120, 6247, 770, 65993)),
    ("DATA", "Loss for the period (FY2023)", (None, None, -58148, None, None, None, None, -58148)),
    ("DATA", "Net changes in fair value", (None, None, None, None, -58, None, None, -58)),
    ("DATA", "Reclassified to income statement", (None, None, None, None, 2, None, None, 2)),
    ("DATA", "Equity-settled share-based payment transactions", (None, None, None, 85, None, None, None, 85)),
    ("DATA", "Issue of shares", (84609, None, None, None, None, None, None, 84609)),
    ("TOTAL", "At 31 March 2023", (253297, 2851, -170914, 408, -176, 6247, 770, 92483)),
    ("DATA", "Loss for the period (FY2024)", (None, None, -8861, None, None, None, None, -8861)),
    ("DATA", "Net changes in fair value", (None, None, None, None, 145, None, None, 145)),
    ("DATA", "Reclassified to income statement", (None, None, None, None, 31, None, None, 31)),
    ("DATA", "Equity-settled share-based payment transactions", (None, None, None, 284, None, None, None, 284)),
    ("DATA", "Issue of shares", (433, 88561, None, None, None, None, None, 89000)),
    ("TOTAL", "At 31 March 2024", (253730, 91418, -179775, 692, 0, 6247, 770, 173082)),
    ("DATA", "Loss for the period (FY2025)", (None, None, -4702, None, None, None, None, -4702)),
    ("DATA", "Net changes in fair value", (None, None, None, None, 824, None, None, 824)),
    ("DATA", "Tax on other comprehensive income", (None, None, None, None, -206, None, None, -206)),
    ("DATA", "Equity-settled share-based payment transactions", (None, None, None, 144, None, None, None, 144)),
    ("DATA", "Reclassified to retained losses", (None, None, 577, -577, None, None, None, 0)),
    ("DATA", "Issue of shares", (183, 26818, None, None, None, None, None, 27001)),
    ("TOTAL", "At 31 March 2025", (253913, 118236, -183900, 259, 618, 6247, 770, 196143)),
]

bw.add_equity_changes_sheet(
    title="Chetwood Financial Limited — Statement of Changes in Equity",
    subtitle="Consolidated basis (FY2019-FY2021 standalone entity), £'000, chronological (oldest to newest). FY2019-FY2020 as filed under FRS 102; a ~£8.1m gap vs the FY2021 AR's own FY2020-comparative opening balance is shown and explained, not bridged - see source note at bottom.",
    headers=equity_headers,
    rows=equity_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=52,
    source_height=220,
)

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Cash flows from operating activities", {}),
    ("DATA", "Loss after tax", {"FY2024": -8861, "FY2023": -58148, "FY2022": -29753, "FY2021": -21310}),
    ("DATA", "Loss for the period (FY2019-FY2020, FRS 102 basis)", {"FY2020": -18314, "FY2019": -11536}),
    ("DATA", "(Loss)/profit before tax", {"FY2025": -4702}),
    ("DATA", "Depreciation of property, plant and equipment", {"FY2025": 615, "FY2024": 560, "FY2023": 496, "FY2022": 322, "FY2021": 347}),
    ("DATA", "Depreciation and amortisation (combined line, FY2019-FY2020 only)", {"FY2020": 230, "FY2019": 151}),
    ("DATA", "Remeasurement of right-of-use asset", {"FY2023": -217, "FY2022": 304}),
    ("DATA", "Amortisation of intangibles", {"FY2025": 536, "FY2024": 1261, "FY2023": 2235, "FY2022": 694, "FY2021": 106}),
    ("DATA", "Impairment of intangibles", {"FY2024": 985, "FY2023": 3069}),
    ("DATA", "Interest income on debt securities", {"FY2025": -50560, "FY2024": -18163, "FY2023": -1885}),
    ("DATA", "Interest expense/(income) on financing activities", {"FY2025": 6800, "FY2024": 180, "FY2023": 36, "FY2022": 35, "FY2021": 40}),
    ("DATA", "Equity-settled share-based payment transactions", {"FY2025": 144, "FY2024": 284, "FY2023": 85, "FY2022": 209, "FY2021": 102, "FY2020": 12}),
    ("DATA", "Movement in fair value of financial instruments at FVTPL", {"FY2025": -22983, "FY2024": 9208, "FY2023": 1399}),
    ("DATA", "Movement in fair value of derivative financial assets", {"FY2022": -119, "FY2021": -15, "FY2020": 5}),
    ("DATA", "Movement in fair value of derivative financial liabilities", {"FY2022": 452, "FY2021": -4}),
    ("DATA", "Fair value adjustment on hedged items", {"FY2025": 9005, "FY2024": -11782, "FY2023": -2217}),
    ("DATA", "Loss on disposal of property, plant and equipment", {"FY2025": 1, "FY2023": 8, "FY2022": 1, "FY2021": 12}),
    ("DATA", "Profit on sale of investments in debt securities", {"FY2025": -1, "FY2024": -42}),
    ("DATA", "Discount unwind on debt securities", {"FY2025": 536}),
    ("DATA", "Loss on disposal of intangible assets", {"FY2022": 18, "FY2021": 402}),
    ("DATA", "Movement in provision", {"FY2025": -657, "FY2024": 894, "FY2023": 1424, "FY2022": 591, "FY2020": 11316, "FY2019": 1920}),
    ("DATA", "Impairment of investment in subsidiary / impairment of Yobota", {"FY2024": 0, "FY2023": 0}),
    ("DATA", "Net gain arising from derecognition of financial assets measured at amortised cost", {"FY2022": -4369}),
    ("DATA", "Net increase in loans and advances to customers", {"FY2025": -857836, "FY2024": -1184232, "FY2023": -346633, "FY2022": -146297, "FY2021": -19344, "FY2020": -110070, "FY2019": -44506}),
    ("DATA", "Net interest paid on derivative financial assets", {"FY2025": 25551, "FY2024": 1448, "FY2023": 37}),
    ("DATA", "Net cash flow on derivative financial instruments", {"FY2024": -52498, "FY2023": 325}),
    ("DATA", "Increase/(decrease) in prepayments and accrued income", {"FY2025": 324, "FY2024": -3353, "FY2023": -69, "FY2022": -175, "FY2021": 223, "FY2020": -404, "FY2019": -159}),
    ("DATA", "Increase in other assets", {"FY2025": -20076, "FY2024": -25013, "FY2023": -10277, "FY2022": -4696, "FY2021": -2881, "FY2020": -157, "FY2019": -421}),
    ("DATA", "(Increase)/decrease in tax asset", {"FY2023": 64, "FY2022": -19, "FY2021": -45}),
    ("DATA", "Increase/(decrease) in customer deposits", {"FY2025": 955692, "FY2024": 1473432, "FY2023": 1060680, "FY2022": 162610, "FY2021": -52195, "FY2020": 184676, "FY2019": 26107}),
    ("DATA", "Increase/(decrease) in accruals and deferred income", {"FY2025": 507, "FY2024": 2487, "FY2023": 489, "FY2022": 1612, "FY2021": 2838, "FY2020": 1119, "FY2019": 829}),
    ("DATA", "Increase/(decrease) in other liabilities", {"FY2025": 142, "FY2024": 2725, "FY2023": 2518, "FY2022": 1447, "FY2021": -396, "FY2020": 784, "FY2019": -6}),
    ("DATA", "Purchase of mortgage portfolio", {"FY2022": 157842}),
    ("DATA", "Derecognition of assets at amortised cost on sale", {"FY2022": -123733}),
    ("TOTAL", "Net cash from operating activities", {"FY2025": 43038, "FY2024": 189520, "FY2023": 653419, "FY2022": 16976, "FY2021": -92120, "FY2020": 69197, "FY2019": -27621}),
    ("SECTION", "Cash flows from investing activities", {}),
    ("DATA", "Proceeds from sale and maturity of debt securities", {"FY2025": 1401, "FY2024": 36835, "FY2023": 11031}),
    ("DATA", "Acquisition of debt securities", {"FY2025": -910238, "FY2024": -505077, "FY2023": -135674, "FY2022": -5003}),
    ("DATA", "Principal repayments on investments in debt securities", {"FY2025": 134509, "FY2024": 61327}),
    ("DATA", "Interest received from investing activities", {"FY2025": 40802, "FY2024": 17601, "FY2023": 1760}),
    ("DATA", "Net maturity/(purchase) of debt securities", {"FY2021": 30170}),
    ("DATA", "Purchase of loans and advances to customers", {"FY2022": -157842}),
    ("DATA", "Purchases of property, plant and equipment", {"FY2025": -617, "FY2024": -461, "FY2023": -843, "FY2022": -119, "FY2021": -116, "FY2020": -85, "FY2019": -462}),
    ("DATA", "Proceeds from sale of property, plant and equipment", {"FY2025": 11}),
    ("DATA", "Investment in Intangible assets", {"FY2025": -9, "FY2023": -402, "FY2022": -1852, "FY2021": -3201, "FY2020": -64, "FY2019": -52}),
    ("DATA", "Acquisition of subsidiary net of cash acquired", {"FY2025": -7497, "FY2022": -12903}),
    ("TOTAL", "Net cash from/(used in) investing activities", {"FY2025": -741638, "FY2024": -389775, "FY2023": -124128, "FY2022": -177719, "FY2021": 26853, "FY2020": -149, "FY2019": -514}),
    ("SECTION", "Cash flows from financing activities", {}),
    ("DATA", "Principal drawdowns on amounts owed to credit institutions", {"FY2025": 476000, "FY2024": 9000}),
    ("DATA", "Interest paid on amounts owed to credit institutions", {"FY2025": -2930}),
    ("DATA", "Purchase of financial investments (FY2019-FY2020 only - classified under financing that year, see presentation note)", {"FY2020": -28176, "FY2019": -1994}),
    ("DATA", "Issuance of ordinary shares", {"FY2025": 27001, "FY2024": 89000, "FY2023": 84609, "FY2022": 55000, "FY2021": 29000, "FY2020": 20000, "FY2019": 55237}),
    ("DATA", "Issuance of debt securities", {"FY2024": 100}),
    ("DATA", "Repayment of debt securities", {"FY2025": -10}),
    ("DATA", "Interest (paid)/received on debt securities", {"FY2025": -6}),
    ("DATA", "Interest expense on debt securities", {"FY2024": 0}),
    ("DATA", "Proceeds from the sale of loans and advances at amortised cost", {"FY2022": 128103}),
    ("DATA", "Interest paid on lease liabilities", {"FY2025": -39, "FY2024": -73, "FY2023": -36, "FY2022": -35, "FY2021": -40}),
    ("TOTAL", "Net cash from/(used in) financing activities", {"FY2025": 500016, "FY2024": 98027, "FY2023": 84573, "FY2022": 183068, "FY2021": 28960, "FY2020": -8176, "FY2019": 53243}),
    ("TOTAL", "Net cash flows for the period", {"FY2025": -198584, "FY2024": -102228, "FY2023": 613864, "FY2022": 22325, "FY2021": -36307, "FY2020": 60872, "FY2019": 25108}),
    ("DATA", "Opening cash and cash equivalents", {"FY2025": 586134, "FY2024": 688362, "FY2023": 74498, "FY2022": 52173, "FY2021": 88480, "FY2020": 27608, "FY2019": 2499}),
    ("TOTAL", "Closing cash and cash equivalents", {"FY2025": 387550, "FY2024": 586134, "FY2023": 688362, "FY2022": 74498, "FY2021": 52173, "FY2020": 88480, "FY2019": 27607}),
]

bw.add_cash_flow_sheet(
    title="Chetwood Financial Limited — Cash Flow Statement",
    subtitle="£'000 unless stated. Consolidated (Group) basis except FY2019-FY2021 († standalone entity). See source note at bottom.",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=66,
    source_height=150,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Sheet: Asset Quality
# ---------------------------------------------------------------
ASSET_QUALITY_SOURCES = (
    "Sources - Chetwood Financial Limited's own Credit Risk / Note 36 (37 in earlier years) disclosures, combining "
    "the separately-disclosed 'unsecured lending at amortised cost' and 'secured lending' IFRS 9 stage tables "
    "(secured mortgage lending only exists from FY2022, when CHL Mortgages for Intermediaries Limited was "
    "acquired - FY2021 is unsecured lending only, and ties exactly to that year's Balance Sheet loan figure).\n"
    f"FY2025/FY2024: Annual Report 2025, p.96-100 (Note 36.2/36.3 Credit quality) - {AR25_URL}\n"
    f"FY2023: Annual Report 2024, p.51-52 (Note 37, FY2023 comparative tables) - {AR24_URL}\n"
    f"FY2022/FY2021: Annual Report 2022, p.49-52 (Note 31.2 Credit quality) - {AR22_URL}\n"
    f"FY2020: Annual Report and Financial Statements, year ended 31 March 2020, p.20/28 (Statement of Financial "
    f"Position net loan balance; no IFRS 9 stage table - see FRS 102 note below) - {AR20_URL}\n"
    f"FY2019: Annual Report and Financial Statements, year ended 31 March 2019, p.15 (Statement of Financial "
    f"Position net loan balance; no IFRS 9 stage table - see FRS 102 note below) - {AR19_URL}\n\n" + ENTITY_NOTE + "\n\n"
    "PRESENTATION NOTE: these Note 36/37 tables report gross/net loans and advances measured at amortised cost "
    "only. The Balance Sheet's own 'Loans and advances to customers' line is larger in every year from FY2022 "
    "onward (e.g. FY2025: £2,691,247k on the Balance Sheet vs £2,665,626k gross / £2,655,384k net summed here) "
    "because some loans are measured at fair value through profit or loss and fall outside this amortised-cost "
    "IFRS 9 note - this gap is a genuine measurement-basis difference disclosed by the Bank, not a transcription "
    "error, and is not force-reconciled here. FY2021 is the exception: with no secured book yet and no FVTPL "
    "loans, the combined stage total ties to the Balance Sheet exactly (£156,249k both ways).\n\n"
    "FY2019/FY2020 NOTE: these two years' statutory accounts were prepared under UK GAAP FRS 102 (not IFRS), "
    "before Chetwood adopted IFRS 9 - there is no loan-staging (Stage 1/2/3) table in either year's accounts, only "
    "a single aggregate net loan balance and a simple impairment-allowance movement in the notes. The Stage/ECL "
    "breakdown rows above are genuinely 'Not publicly disclosed' for FY2019 and FY2020; only the single 'Net loans "
    "and advances to customers' total row is populated for those two years, tying exactly to the Balance Sheet."
)
asset_quality_rows = [
    ("SECTION", "Loan book by IFRS 9 stage (secured + unsecured combined)", {}),
    ("DATA", "Stage 1 - gross carrying amount", {"FY2025": 2129852, "FY2024": 1632661, "FY2023": 594912, "FY2022": 273792, "FY2021": 145496}),
    ("DATA", "Stage 2 - gross carrying amount", {"FY2025": 520622, "FY2024": 186714, "FY2023": 47246, "FY2022": 24685, "FY2021": 22064}),
    ("DATA", "Stage 3 - gross carrying amount", {"FY2025": 15152, "FY2024": 30817, "FY2023": 26237, "FY2022": 21297, "FY2021": 14585}),
    ("DATA", "Purchased or originated credit-impaired (POCI) - gross carrying amount", {"FY2025": 0, "FY2024": 0, "FY2023": 284, "FY2022": 550}),
    ("TOTAL", "Total gross loans and advances to customers (amortised cost)", {"FY2025": 2665626, "FY2024": 1850192, "FY2023": 668679, "FY2022": 320324, "FY2021": 182145}),
    ("DATA", "Stage 1 - ECL allowance", {"FY2025": -1356, "FY2024": -1887, "FY2023": -5118, "FY2022": -7791, "FY2021": -6292}),
    ("DATA", "Stage 2 - ECL allowance", {"FY2025": -2912, "FY2024": -4073, "FY2023": -8469, "FY2022": -8517, "FY2021": -7149}),
    ("DATA", "Stage 3 - ECL allowance", {"FY2025": -5974, "FY2024": -24527, "FY2023": -23300, "FY2022": -18255, "FY2021": -12455}),
    ("DATA", "POCI - ECL allowance", {"FY2025": 0, "FY2024": 0, "FY2023": -17, "FY2022": -13}),
    ("TOTAL", "Total ECL allowance", {"FY2025": -10242, "FY2024": -30487, "FY2023": -36904, "FY2022": -34576, "FY2021": -25896}),
    ("TOTAL", "Net loans and advances to customers (amortised cost)", {"FY2025": 2655384, "FY2024": 1819705, "FY2023": 631775, "FY2022": 285748, "FY2021": 156249, "FY2020": 145022, "FY2019": 46269}),
    ("SECTION", "Derived ratios", {}),
    ("DATA", "Stage 3 / NPL ratio (Stage 3 gross / total gross)", {"FY2025": "0.57%", "FY2024": "1.67%", "FY2023": "3.92%", "FY2022": "6.65%", "FY2021": "8.01%"}),
    ("DATA", "ECL coverage ratio (total allowance / total gross)", {"FY2025": "0.38%", "FY2024": "1.65%", "FY2023": "5.52%", "FY2022": "10.79%", "FY2021": "14.22%"}),
    ("DATA", "Stage 3 coverage ratio (Stage 3 allowance / Stage 3 gross)", {"FY2025": "39.43%", "FY2024": "79.59%", "FY2023": "88.81%", "FY2022": "85.71%", "FY2021": "85.40%"}),
]
bw.add_asset_quality_sheet(
    title="Chetwood Financial Limited — Asset Quality / Credit Risk Disclosures",
    subtitle="£'000. Consolidated (Group) basis except FY2019-FY2021 († standalone entity). No IFRS 9 stage table for FY2019-FY2020 (FRS 102 basis - see source note). See source note at bottom.",
    rows=asset_quality_rows,
    sources_text=ASSET_QUALITY_SOURCES,
    first_col_width=64,
    source_height=220,
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, unit, rows_data, sources_text, note=note, first_col_width=46, source_height=150)

FY2024_GAP_NOTE = (
    "FY2024 comes from Chetwood's own FY2024 Pillar 3 ('Pillar 3 Disclosures November 2024', as at 31 March "
    "2024), located 2026-09-19 on the bank's CMS file host after earlier passes had recorded it as never "
    "published (see source note). Its KM1 is single-column and headed '2023' although the document is as at "
    "31 March 2024 - a source labelling defect; row 4 (824,623) equals the same document's OV1 '2024' total, "
    "which fixes the date. The Annual Reports' whole-percent KPI CET1 ratio remains a separate row on the "
    "CET1 Ratio sheet.\n"
    "FY2019 is likewise blank - Chetwood published no Pillar 3 disclosure for that year. FY2020 WAS previously "
    "blank on this basis and is now populated: see the source note's 2026-09-15 correction.\n"
    "SDDT RULED OUT, 2026-09-15 (cross-bank SDDT pass) - recorded as a negative result so this line of enquiry "
    "is not reopened. Many small UK deposit-takers' FY2024/FY2025 Pillar 3 gaps turn out to be the Small "
    "Domestic Deposit Taker (SDDT) exemption, which removes the Pillar 3 disclosure obligation outright. That "
    "is NOT the explanation here. Chetwood Financial Limited does not appear at all in the SDDT rows of the "
    "PRA's own firm-level register - the Bank of England consolidated list of waivers and modifications "
    "granted to PRA-authorised firms (downloaded 2026-09-15, "
    "https://www.bankofengland.co.uk/-/media/boe/files/prudential-regulation/authorisations/"
    "waivers-and-modifications-of-rules/consolidated-waivers-pra-firms.csv). FRN 740551 'Chetwood Financial "
    "Limited' holds four modifications in that register (two Capital Requirements Regulation entries from "
    "2017/2018, a Capital Buffers Part 5.1-5.3/5.5 direction from 10/09/2021, and an Individual Consolidation "
    "permission from 19/08/2024) and NONE is a modification by consent under Rule 3.1 of the 'SDDT Regime - "
    "General Application' Part - the instrument by which a firm becomes an SDDT, and which ten other banks "
    "checked in this same pass do hold.\n"
    "Corroborated by Chetwood's own documents. The FY2024 and FY2025 Annual Reports and the FY2025 Pillar 3 "
    "disclosure were downloaded and text-extracted in full (all three have readable text layers - 523k, 457k "
    "and 60k characters respectively, so these are true negatives, not scanned-PDF false negatives) and "
    "searched for 'SDDT', 'Small Domestic Deposit Taker', 'modification by consent', 'Simplified Retail "
    "Deposit Ratio', 'SRDR', 'Strong and Simple', 'Interim Capital Regime' and 'Basel 3.1'. Zero hits in any "
    "of the three - Chetwood does not mention the SDDT regime anywhere.\n"
    "What the FY2025 Pillar 3 document DOES state is a different proportionality regime, and it is the "
    "evidenced reason that document is short and single-column: section 2.3 'Basis of Preparation', p.3 - "
    "'Chetwood meets the definition of a \"small and non-complex institution\" and is therefore subject to "
    "proportional disclosure requirements in accordance with Article 433b of the Disclosure (CRR) Part of the "
    "PRA Rulebook.' Article 433b is the reduced annual-disclosure article; unlike the SDDT modification it "
    "does not remove the obligation to publish, which is consistent with Chetwood still publishing a Pillar 3 "
    "document. (Written when FY2024 was believed absent; the FY2024 edition has since been found, 2026-09-19, "
    "and the SDDT finding above stands: no exemption applies.)"
)

FY2020_P3_NOTE = (
    "FY2020 added 2026-09-15 from Chetwood's own 'Pillar 3 Disclosures June 2020 (as at 31st March 2020)' - a "
    "document earlier sessions concluded did not exist (see the source note's correction). That edition pre-dates "
    "the KM1 template, so it reports a narrative Summary-analysis table plus a capital-resources build-up rather "
    "than KM1 rows, and it states its ratios and RWA to whole percents / one decimal place of £m only."
)

# The FY2024 and FY2025 Annual Reports' own KPI tables publish a Group CET1
# capital ratio rounded to a whole percent. It was once thought the only FY2024
# capital figure obtainable; the FY2024 Pillar 3 was found 2026-09-19 (20.8%,
# consistent with the KPI table's 21%). It is not on the same basis as the KM1
# rows above - FY2025 prints 16% against KM1's 15.2%, which is not even a
# rounding of it - so it is carried as its own clearly-labelled row rather than
# merged into the primary series, per the project's basis-discipline rule.
AR_CET1_RATIO_ROW = (
    "Common Equity Tier 1 (CET1) capital ratio per Annual Report KPI table (whole %, alternative basis - see note)",
    {"FY2025": "16%", "FY2024": "21%", "FY2023": "27%"},
)

# ---------------------------------------------------------------
# KM1 Key Metrics - Chetwood's own published template, reproduced as printed.
#
# Only three of Chetwood's five located Pillar 3 editions carry a KM1 table at
# all: the FY2022 edition ("Annex B: Key Metrics - KM1"), the FY2023 edition
# (Section 6 "Key Metrics") and the FY2025 edition (Section 5 "Key Metrics").
# Each is SINGLE-COLUMN - the header block is literally "a  £'000s" over one
# year - so no year here is a comparative and no column can be back-filled from
# a neighbouring edition. FY2024's edition (Nov 2024) was found 2026-09-19 and
# is also single-column, headed '2023' in error (see FY2024_GAP_NOTE); the FY2021 and FY2020 editions pre-date the template (the
# FY2021 document was re-read for this sheet: the strings "key metric", "KM1",
# "combined buffer" and "risk weighted exposure" appear nowhere in it, and its
# capital disclosure is a narrative "Total CET1 Capital" table); FY2019 has no
# Pillar 3 document. Those four columns are therefore blank, and the figures
# they do carry on the single-metric sheets are narrative-table figures, not
# KM1 rows.
#
# ROW SET DRIFT (the union is shown, in the template's canonical order):
#   - UK 8a, UK 9a, 10, UK 10a and UK 14a-14f are printed ONLY by the FY2022
#     edition. The FY2023 and FY2025 editions omit them from the table.
#   - The FY2022 edition prints rows 13/14 and then a further "Additional own
#     funds requirements to address risks of excessive leverage" section; the
#     FY2023 and FY2025 editions go straight from row 14 to the LCR section.
#
# TWO SOURCE DEFECTS in the FY2022 edition, reproduced rather than corrected:
#   - row 11 "Combined buffer requirement (%)" prints "0%" even though row 8
#     above it prints a 2.5% capital conservation buffer, so the combined
#     buffer cannot be nil. The FY2023 and FY2025 editions print 3.50% and
#     4.50% for the same row and are internally consistent.
#   - row 12 is captioned "(%)" but prints 20,034 - a £'000 amount, not a
#     percentage. Same defect Monzo's row 12 carries in two of its editions.
#
# DASH vs ZERO: the FY2022 edition prints BOTH glyphs and means different
# things by them. Rows UK 7b, UK 7c and UK 14a-14e print "-" (the cells CARRY
# that dash); rows UK 8a, 9, UK 9a, 10, UK 10a, 11 and UK 14f print "0%" (kept
# as a measured zero). The FY2023 and FY2025 editions print "-" for UK 7b/7c
# only. Do not tidy either glyph into the other - one table, two meanings.
#
# LEVERAGE CAPTION CHANGE: the FY2022 and FY2023 editions caption rows 13/14
# "Leverage ratio total exposure measure" / "Leverage ratio"; the FY2025
# edition captions the same two rows "Total exposure measure excluding claims
# on central banks" / "Leverage ratio excluding claims on central banks (%)".
# Shown as two separately-captioned blocks rather than one merged series. All
# three reporting dates fall AFTER the 1 January 2022 UK leverage change, so
# the underlying basis is very likely the same throughout and this is the
# caption catching up - but Chetwood never says so in any edition, and a
# reproduction sheet may not assert what the source does not.
# ---------------------------------------------------------------
km1_rows = [
    # FY2024 (2026-09-19): transcribed from the FY2024 edition's own KM1 (Nov 2024,
    # pp.10-11), read off page images. That edition prints UK 7b/7c as an en dash
    # "–" (carried as ASCII "-", KM1 rule 2) and, like FY2023/FY2025, omits UK 8a,
    # UK 9a, 10, UK 10a and UK 14a-14f. The statement row that stood here from
    # 2026-09-18 ("No UK KM1 published") was false and has been removed.
    ("SECTION", "Available own funds (amounts, £'000s)", {}),
    ("DATA", "1    Common Equity Tier 1 (CET1) capital",
     {"FY2025": 187605, "FY2024": 171791, "FY2023": 91268, "FY2022": 57554}),
    ("DATA", "2    Tier 1 capital",
     {"FY2025": 187605, "FY2024": 171791, "FY2023": 91268, "FY2022": 57554}),
    ("DATA", "3    Total capital",
     {"FY2025": 187605, "FY2024": 171791, "FY2023": 91268, "FY2022": 57554}),
    ("SECTION", "Risk-weighted exposure amounts (£'000s)", {}),
    ("DATA", "4    Total risk-weighted exposure amount",
     {"FY2025": 1233321, "FY2024": 824623, "FY2023": 343668, "FY2022": 196750}),
    ("SECTION", "Capital ratios (as a percentage of risk-weighted exposure amount)", {}),
    ("DATA", "5    Common Equity Tier 1 ratio (%)",
     {"FY2025": "15.2%", "FY2024": "20.8%", "FY2023": "26.6%", "FY2022": "29.3%"}),
    ("DATA", "6    Tier 1 ratio (%)",
     {"FY2025": "15.2%", "FY2024": "20.8%", "FY2023": "26.6%", "FY2022": "29.3%"}),
    ("DATA", "7    Total capital ratio (%)",
     {"FY2025": "15.2%", "FY2024": "20.8%", "FY2023": "26.6%", "FY2022": "29.3%"}),
    ("SECTION", "Additional own funds requirements based on SREP (as a percentage of risk-weighted exposure amount)", {}),
    ("DATA", "UK 7a    Additional CET1 SREP requirements (%)",
     {"FY2025": "1.92%", "FY2024": "5.35%", "FY2023": "11.07%", "FY2022": "11.1%"}),
    # Dashed in all three editions - re-read at source 2026-09-18 in the FY2025,
    # FY2023 and FY2022 PDFs. Every one of those editions is SINGLE-COLUMN, so
    # each year comes from its own reporting-year table and no rule-1 question
    # arises. Note what sits a few rows below: UK 8a, 9, UK 9a, 10, UK 10a, 11
    # and UK 14f are printed "0%" in the SAME FY2022 table and stay numeric.
    ("DATA", "UK 7b    Additional AT1 SREP requirements (%)",
     {"FY2025": "-", "FY2024": "-", "FY2023": "-", "FY2022": "-"}),
    ("DATA", "UK 7c    Additional T2 SREP requirements (%)",
     {"FY2025": "-", "FY2024": "-", "FY2023": "-", "FY2022": "-"}),
    ("DATA", "UK 7d    Total SREP own funds requirements (%)",
     {"FY2025": "9.92%", "FY2024": "13.35%", "FY2023": "19.07%", "FY2022": "19.1%"}),
    ("SECTION", "Combined buffer requirement (as a percentage of risk-weighted exposure amount)", {}),
    ("DATA", "8    Capital conservation buffer (%)",
     {"FY2025": "2.50%", "FY2024": "2.50%", "FY2023": "2.50%", "FY2022": "2.5%"}),
    ("DATA", "UK 8a    Conservation buffer due to macro-prudential or systemic risk identified at the level of a Member State (%)",
     {"FY2022": "0%"}),
    ("DATA", "9    Institution specific countercyclical capital buffer (%)",
     {"FY2025": "2.00%", "FY2024": "2.00%", "FY2023": "1%", "FY2022": "0%"}),
    ("DATA", "UK 9a    Systemic risk buffer (%)", {"FY2022": "0%"}),
    ("DATA", "10    Global Systemically Important Institution buffer (%)", {"FY2022": "0%"}),
    ("DATA", "UK 10a    Other Systemically Important Institution buffer", {"FY2022": "0%"}),
    ("DATA", "11    Combined buffer requirement (%)",
     {"FY2025": "4.50%", "FY2024": "4.50%", "FY2023": "3.50%", "FY2022": "0%"}),
    ("DATA", "UK 11a    Overall capital requirements (%)",
     {"FY2025": "14.42%", "FY2024": "17.85%", "FY2023": "22.57%", "FY2022": "21.6%"}),
    ("DATA", "12    CET1 available after meeting the total SREP own funds requirements (%)",
     {"FY2025": "5.29%", "FY2024": "7.48%", "FY2023": "7.49%", "FY2022": 20034}),
    ("SECTION", "Leverage ratio — as captioned in the FY2024 and FY2025 editions (excluding claims on central banks)", {}),
    ("DATA", "13    Total exposure measure excluding claims on central banks",
     {"FY2025": 3615720, "FY2024": 2387717}),
    ("DATA", "14    Leverage ratio excluding claims on central banks (%)",
     {"FY2025": "5.19%", "FY2024": "7.19%"}),
    ("SECTION", "Leverage ratio — as captioned in the FY2022 and FY2023 editions (basis not stated)", {}),
    ("DATA", "13    Leverage ratio total exposure measure",
     {"FY2023": 1519817, "FY2022": 394658}),
    ("DATA", "14    Leverage ratio",
     {"FY2023": "6.01%", "FY2022": "14.58%"}),
    ("SECTION", "Additional own funds requirements to address risks of excessive leverage (as a percentage of leverage ratio total exposure amount)", {}),
    # All five dashed in the FY2022 edition (printed pp.35-36), which is the only
    # edition that prints this block at all; FY2023 and FY2025 omit it, so their
    # cells stay blank. UK 14f immediately below is a printed "0%" in that same
    # block and is deliberately NOT touched - one table, both glyphs.
    ("DATA", "UK 14a    Additional CET1 leverage ratio requirements (%)", {"FY2022": "-"}),
    ("DATA", "UK 14b    Additional AT1 leverage ratio requirements (%)", {"FY2022": "-"}),
    ("DATA", "UK 14c    Additional T2 leverage ratio requirements (%)", {"FY2022": "-"}),
    ("DATA", "UK 14d    Total SREP leverage ratio requirements (%)", {"FY2022": "-"}),
    ("DATA", "UK 14e    Applicable leverage buffer", {"FY2022": "-"}),
    ("DATA", "UK 14f    Overall leverage ratio requirements (%)", {"FY2022": "0%"}),
    ("SECTION", "Liquidity Coverage Ratio (£'000s / %)", {}),
    ("DATA", "15    Total high-quality liquid assets (HQLA) (Weighted value -average)",
     {"FY2025": 897493, "FY2024": 665116, "FY2023": 302266, "FY2022": 67841}),
    ("DATA", "UK 16a    Cash outflows - Total weighted value",
     {"FY2025": 489794, "FY2024": 395674, "FY2023": 52035, "FY2022": 5627}),
    ("DATA", "UK 16b    Cash inflows - Total weighted value",
     {"FY2025": 28009, "FY2024": 34098, "FY2023": 15169, "FY2022": 13656}),
    ("DATA", "16    Total net cash outflows (adjusted value)",
     {"FY2025": 461785, "FY2024": 361576, "FY2023": 36865, "FY2022": 1407}),
    ("DATA", "17    Liquidity coverage ratio (%)",
     {"FY2025": "194%", "FY2024": "184%", "FY2023": "1,015%", "FY2022": "4,823%"}),
    ("SECTION", "Net Stable Funding Ratio (£'000s / %)", {}),
    ("DATA", "18    Total available stable funding",
     {"FY2025": 3677559, "FY2024": 2862609, "FY2023": 1387511, "FY2022": 380549}),
    ("DATA", "19    Total required stable funding",
     {"FY2025": 2536343, "FY2024": 1760110, "FY2023": 572002, "FY2022": 233566}),
    ("DATA", "20    NSFR ratio (%)",
     {"FY2025": "145%", "FY2024": "163%", "FY2023": "243%", "FY2022": "162.9%"}),
]

KM1_SOURCES = (
    "Sources - Chetwood's own UK KM1 key-metrics template, reproduced as printed. Each column is transcribed "
    "from the edition in which that year is the reporting year; every one of these editions is SINGLE-COLUMN "
    "(header block 'a  £'000s' over one year only), so no figure here is a later edition's comparative.\n"
    f"FY2025: Chetwood Bank Pillar 3 Disclosures, September 2025 (as at 31 March 2025), Section 5 'Key Metrics', "
    f"pp.9-10 of 15 - {P3_25_URL}\n" + FY2025_EDITION_CHECK + "\n"
    f"FY2023: Chetwood Financial Ltd Pillar 3 Disclosure, as at 31st March 2023, Section 6 'Key Metrics', p.17 "
    f"(PDF p.18 of 34) - {P3_23_URL}\n"
    f"FY2022: Chetwood Financial Ltd Pillar 3 Disclosure, as at 31st March 2022, 'Annex B: Key Metrics - KM1', "
    f"pp.35-36 (PDF pp.36-37 of 41) - {P3_22_URL}\n"
    f"FY2024: Chetwood Bank Pillar 3 Disclosures, November 2024 (as at 31 March 2024), Section 5 'Key Metrics', "
    f"pp.10-11 of 15 - {P3_24_URL}. SOURCE DEFECT: its single KM1 column is headed '2023', but the document is "
    "'as at 31 March 2024' (p.3) and its row 4 (824,623) equals the OV1 '2024' column on p.12; reproduced under "
    "FY2024 with the heading recorded here. It prints UK 7b/UK 7c as an en dash '–'. CORRECTION: from 2026-09-18 "
    "to 2026-09-19 this column carried a statement that no Pillar 3 was published for FY2024; that was false - "
    "the edition was on the bank's CMS file host (cdn.sanity.io), which no earlier search had looked at.\n"
    "FY2021, FY2020 and FY2019 are blank, for two different reasons, none of which is a failed "
    "search:\n"
    "• FY2021 and FY2020 - both editions pre-date the template. The FY2021 document was re-read in full for "
    "this sheet: 'key metric', 'KM1', 'combined buffer' and 'risk weighted exposure' appear nowhere in it, and "
    "its only capital table is a narrative 'Total CET1 Capital' build-up. The FY2020 edition is the same shape. "
    "The FY2020/FY2021 figures on the single-metric sheets come from those narrative tables and are deliberately "
    "NOT re-assembled into KM1 rows here.\n"
    "• FY2019 - Chetwood published no Pillar 3 disclosure at all that year.\n\n"
    "PRESENTATION NOTES:\n"
    "• ROW SET DRIFT: rows UK 8a, UK 9a, 10, UK 10a and UK 14a-UK 14f are printed by the FY2022 edition only; "
    "the FY2023, FY2024 and FY2025 editions omit them from the table entirely. The union is shown, in the template's "
    "canonical order, so the sheet matches the table a reader of the FY2022 report would recognise.\n"
    "• DASH vs ZERO, AND THIS SHEET NOW SHOWS THE DIFFERENCE. The FY2022 edition uses both glyphs in ONE "
    "table and means different things by them. It prints '-' at rows UK 7b, UK 7c and UK 14a-UK 14e - those "
    "cells carry a literal dash, because the requirement does not apply to Chetwood - and it prints '0%' at "
    "rows UK 8a, 9, UK 9a, 10, UK 10a, 11 and UK 14f, which are kept as the measured zeros the Bank "
    "published. The FY2023, FY2024 and FY2025 editions print a dash at UK 7b/UK 7c only, and those carry dashes too; "
    "all three editions were re-read at source on 2026-09-18. Chetwood is the clearest demonstration in this "
    "corpus of why the two glyphs must not be flattened together: a single table, printed by a single bank "
    "on a single date, deliberately using a dash for 'does not apply' and a zero for 'measured at nil'. "
    "Anything that rendered both as the same thing would be discarding a distinction Chetwood took care to "
    "draw. Rows UK 14a-UK 14e are blank for FY2023 and FY2025 because those editions omit the block "
    "entirely - a third state again, and not the same as either.\n"
    "• SOURCE DEFECT, row 11 (FY2022): the FY2022 edition prints Combined buffer requirement as '0%' even "
    "though row 8 immediately above prints a 2.50% capital conservation buffer, so the combined buffer cannot "
    "be nil. Reproduced as published and flagged here; the FY2023 (3.50%) and FY2025 (4.50%) editions are "
    "internally consistent.\n"
    "• SOURCE DEFECT, row 12 (FY2022): captioned 'CET1 available after meeting the total SREP own funds "
    "requirements (%)' but printed as 20,034 - a £'000 amount, not a percentage. Reproduced as printed.\n"
    "• LEVERAGE CAPTION CHANGE: the FY2022 and FY2023 editions caption rows 13/14 'Leverage ratio total "
    "exposure measure' / 'Leverage ratio' with no basis stated; the FY2024 and FY2025 editions caption the same rows "
    "'Total exposure measure excluding claims on central banks' / 'Leverage ratio excluding claims on central "
    "banks (%)'. Shown as two separately-captioned blocks rather than merged. All three reporting dates fall "
    "after the 1 January 2022 UK change that excluded claims on central banks from the exposure measure, so "
    "the underlying basis is very likely unchanged and only the caption moved - but no Chetwood edition says "
    "so, and this sheet reproduces rather than infers. The Leverage Ratio metric sheet carries the same four "
    "figures as one series, with its own note.\n"
    "• PRECISION: the FY2022 edition prints ratios to one decimal place ('29.3%', '11.1%', '2.5%'); the FY2023 "
    "and FY2025 editions print two ('11.07%', '2.50%', '1.92%'), while still printing row 9 as '1%' in FY2023 "
    "and rows 17/20 as whole percents in FY2025. Each cell keeps the precision of its own edition.\n"
    "• Row 15 is a weighted 12-month average (the caption says so); rows 17 and 20 are as printed, including "
    "the FY2023 thousands separator in '1,015%'.\n\n"
    "LATEST-EDITION CHECK, 2026-09-16: chetwoodbank.co.uk publishes its documents at undated, overwritten URLs "
    "(/documents/chetwood-bank-pillar-three-disclosures.pdf and /documents/chetwood-bank-annual-report.pdf, "
    "both linked from /about-us). Both were downloaded fresh on that date: the Pillar 3 file is still the "
    "'September 2025' edition with a single 2025 column, and the Annual Report file is still 'year ended 31 "
    "March 2025'. No FY2026 edition of either had been published. Checked, none newer.\n"
    "FY2026 CHECK, 2026-09-19 (year ended 31 March 2026): no FY2026 edition of either document is out, so no "
    "FY2026 column is added. Routes: (1) both undated live URLs re-downloaded - the Annual Report is still 'Year "
    "ended 31 March 2025' (PDF created 29 Oct 2025, modified 17 Nov 2025) and the Pillar 3 still 'as at 31 March "
    "2025' (PDF created 7 Nov 2025); (2) Companies House filing history for 09964966, unfiltered, page 1: the "
    "newest accounts filing is AA 'Group of companies' accounts made up to 31 March 2025' (20 Dec 2025), and the "
    "company page gives next accounts made up to 31 March 2026 due by 31 December 2026; (3) Wayback CDX of "
    "chetwoodbank.co.uk holds no /documents/ capture, and archived homepages link only the FY2023-FY2025 "
    "cdn.sanity.io files. Prior pattern: the FY2025 Annual Report was filed 20 Dec 2025 and its Pillar 3 "
    "published Sept-Nov 2025; the FY2024 accounts were filed 4 Oct 2024 and its Pillar 3 is dated Nov 2024."
)

bw.add_km1_sheet(
    title="Chetwood Financial Limited — KM1 Key Metrics",
    subtitle="Chetwood's own published UK key-metrics (KM1) template, reproduced in its row order with its own "
             "template row numbers, labels and printed precision. Amounts in £'000s, ratios as printed. "
             "Group/consolidated basis. Only the FY2022-FY2025 Pillar 3 editions carry a KM1 table, "
             "and each is single-column (FY2024's is headed '2023' in error - see note); FY2021/FY2020 (editions pre-date the template) "
             "and FY2019 (no document) are intentionally blank. See source note below.",
    rows=km1_rows,
    sources_text=KM1_SOURCES,
    first_col_width=72,
    source_height=460,
)

metric(
    "CET1 Capital", "£'000, Group/consolidated basis (FY2020-FY2021: standalone entity)",
    [("Common Equity Tier 1 (CET1) capital", {"FY2025": 187605, "FY2024": 171791, "FY2023": 91268, "FY2022": 57554, "FY2021": 50637, "FY2020": 50697})],
    p3_sources(),
    note=FY2024_GAP_NOTE + "\n" + FY2020_P3_NOTE,
)

metric(
    "CET1 Ratio", "% of RWA",
    [
        ("Common Equity Tier 1 (CET1) ratio", {"FY2025": "15.2%", "FY2024": "20.8%", "FY2023": "26.6%", "FY2022": "29.3%", "FY2021": "28%", "FY2020": "30%"}),
        AR_CET1_RATIO_ROW,
    ],
    p3_sources(),
    note=FY2024_GAP_NOTE + " FY2021 is as stated in the source (rounded to the nearest whole percent; no decimal "
         "figure was disclosed that year).\n" + FY2020_P3_NOTE + " The FY2020 document's Summary-analysis table "
         "prints a 'Tier 1 Ratio' of 30% and no separate CET1 ratio line; its own capital-resources table shows "
         "CET1 £50,697k going straight to Tier 2 with no Additional Tier 1 line, so Tier 1 = CET1 that year and "
         "30% is the CET1 ratio as well - the same treatment already applied to every other year on this sheet.\n"
         "SECOND ROW (alternative basis, added 2026-09-15): the Annual Reports' KPI tables were then thought the "
         "only source of any FY2024 capital ratio (the FY2024 Pillar 3, found 2026-09-19, prints 20.8%), and "
         "their whole-percent Group CET1 ratio is carried on its own "
         "row - FY2024 21% (stated identically in the FY2024 report's own year column and the FY2025 report's "
         "FY2024 comparative column, two independent confirmations). It is NOT merged into the primary row "
         "because the two series do not agree: for FY2025 the KPI table says 16% where the Pillar 3 KM1 says "
         "15.2%, a difference too large to be rounding, cause not explained in either document (FY2023 does "
         "reconcile: 27% vs 26.6%). Treat the FY2024 21% as indicative of level, not as a KM1-basis figure.",
)

metric(
    "Tier 1 Capital", "£'000",
    [("Tier 1 capital", {"FY2025": 187605, "FY2024": 171791, "FY2023": 91268, "FY2022": 57554, "FY2021": 50637, "FY2020": 50697})],
    p3_sources(),
    note=FY2024_GAP_NOTE + " Equal to CET1 capital in every year shown - Chetwood has no Additional Tier 1 (AT1) "
         "instruments (in FY2020 confirmed by its capital-resources table running CET1 -> Tier 2 -> Total with no "
         "AT1 line).\n" + FY2020_P3_NOTE,
)

metric(
    "Tier 1 Ratio", "% of RWA",
    [("Tier 1 ratio", {"FY2025": "15.2%", "FY2024": "20.8%", "FY2023": "26.6%", "FY2022": "29.3%", "FY2021": "28%", "FY2020": "30%"})],
    p3_sources(),
    note=FY2024_GAP_NOTE + "\n" + FY2020_P3_NOTE,
)

metric(
    "Total Capital", "£'000",
    [("Total capital", {"FY2025": 187605, "FY2024": 171791, "FY2023": 91268, "FY2022": 57554, "FY2021": 50637, "FY2020": 52835})],
    p3_sources(),
    note=FY2024_GAP_NOTE + " Equal to CET1/Tier 1 capital in FY2021-FY2025 - Chetwood had no Tier 2 capital in "
         "those years. FY2020 is the exception and the only year that differs: its capital-resources table "
         "discloses £2,138k of Tier 2 capital on top of CET1 £50,697k, giving Total regulatory capital £52,835k "
         "as printed.\n" + FY2020_P3_NOTE,
)

metric(
    "Total Capital Ratio", "% of RWA",
    [("Total capital ratio", {"FY2025": "15.2%", "FY2024": "20.8%", "FY2023": "26.6%", "FY2022": "29.3%", "FY2021": "28%", "FY2020": "31%"})],
    p3_sources(),
    note=FY2024_GAP_NOTE + "\n" + FY2020_P3_NOTE + " FY2020's 31% is higher than that year's 30% Tier 1 ratio "
         "because of the £2,138k of Tier 2 capital described on the Total Capital sheet - both figures are "
         "printed in the document's own Summary-analysis table, neither is derived.",
)

metric(
    "Total RWAs", "£'000",
    [("Total risk-weighted exposure amount", {"FY2025": 1233321, "FY2024": 824623, "FY2023": 343668, "FY2022": 196750, "FY2021": 178987, "FY2020": 171000})],
    p3_sources(),
    note=FY2020_P3_NOTE + " FY2020's £171,000k is the document's own printed 'Risk Weighted Assets (£m) £171.0m' "
         "- disclosed to one decimal place of £m only, so the trailing three digits are the unit conversion, not "
         "spurious precision. It reconciles exactly to that document's own two components (Credit Risk RWAs "
         "£119.4m + operational-risk RWAs £51.6m = £171.0m), shown on the RWA Breakdown sheet.\n"
         "FY2024's 824,623 is printed in the FY2024 edition's own KM1 row 4 (p.10) and OV1 total (p.12), and "
         "identically as the FY2025 edition's OV1 2024 comparative.",
)

# ---------------------------------------------------------------
# Sheet: RWA Breakdown
# ---------------------------------------------------------------
RWA_BREAKDOWN_SOURCES = (
    "Sources - Chetwood's own Pillar 3 Disclosures, Section 6 'Overview of RWAs' (OV1 template from FY2022 onward; "
    "FY2021 uses an equivalent pre-KM1 category table).\n"
    f"FY2025: Chetwood Bank Pillar 3 Disclosures, September 2025 (as at 31 March 2025), Section 6.3 OV1, p.11 - {P3_25_URL}\n"
    + FY2025_EDITION_CHECK + "\n"
    f"FY2024: Chetwood Bank Pillar 3 Disclosures, November 2024 (as at 31 March 2024), Section 6.3 OV1, p.12, "
    f"'2024' column - {P3_24_URL}. Every FY2024 figure is identical to the FY2025 edition's 2024 comparative, "
    "from which this column was first filled.\n"
    f"FY2023/FY2022: Chetwood Financial Ltd Pillar 3 Disclosure, as at 31 March 2023, Section 8.3 (OV1 table with "
    f"FY2022 comparative) - {P3_23_URL}\n"
    f"FY2021: Chetwood Financial Ltd Pillar 3 Disclosure, as at 31 March 2021, Section 5.4 (pre-KM1 category "
    f"table) - {P3_21_URL}\n"
    f"FY2020: Chetwood Financial Ltd Pillar 3 Disclosures, June 2020 (as at 31st March 2020), Section 1.2 "
    f"('Credit Risk Weighted Assets', p.3) and Section 8 (Operational risk, p.19) - {P3_20_URL}. This edition "
    f"has no OV1 or category table at all; it states only Credit Risk RWAs of £119.4m (itself split in the "
    f"narrative into £112.1m customer lending + £5.5m other assets + £1.8m lending to banks) and an "
    f"operational-risk RWA requirement of £51.6m, which together make its printed £171.0m total exactly. "
    f"Counterparty credit risk and securitisation are left blank rather than assumed nil - the document never "
    f"mentions either, and Chetwood had no securitised exposures that early.\n\n" + ENTITY_NOTE + "\n\n"
    "CORRECTION, 2026-09-19: this note previously said no 'as at 31 March 2024' Pillar 3 was ever published. "
    "It was: see the FY2024 line above.\n\n"
    "PRESENTATION NOTE: FY2021's pre-KM1 category table has no separate 'Securitisation' line (Chetwood had no "
    "securitised exposures that early) and combines credit valuation adjustment into Counterparty credit risk "
    "rather than breaking it out - both blank rather than assumed zero-and-separate."
)
rwa_breakdown_rows = [
    ("SECTION", "OV1 'Overview of RWAs' template — Chetwood's own Pillar 3 Disclosures, Section 6.3 (FY2025; FY2024 from its own November 2024 edition, identical to the FY2025 comparative) and Section 8.3 (FY2023, with the FY2022 comparative column)", {}),
    ("DATA", "Credit risk (excluding CCR)", {"FY2025": 1017779, "FY2024": 703828, "FY2023": 290536, "FY2022": 179962}),
    ("DATA", "Counterparty credit risk (CCR)", {"FY2025": 23777, "FY2024": 13638, "FY2023": 4143, "FY2022": 1937}),
    ("DATA", "Securitisation exposures in the non-trading book", {"FY2025": 102610, "FY2024": 62980, "FY2023": 18124}),
    ("DATA", "Operational risk", {"FY2025": 89154, "FY2024": 44177, "FY2023": 30865, "FY2022": 14852}),
    ("TOTAL", "Total", {"FY2025": 1233321, "FY2024": 824623, "FY2023": 343668, "FY2022": 196750}),
    ("SECTION", "Pre-KM1 equivalent category table — Pillar 3 Disclosure as at 31 March 2021 (FY2021). This edition predates Chetwood's use of the OV1 template and carries no securitisation line", {}),
    ("DATA", "Credit risk (excluding CCR)", {"FY2021": 126942}),
    ("DATA", "Counterparty credit risk (CCR)", {"FY2021": 450}),
    ("DATA", "Operational risk", {"FY2021": 51595}),
    ("TOTAL", "Total", {"FY2021": 178987}),
    ("SECTION", "No OV1 or category table published (FY2020) — figures taken from narrative sections of the Pillar 3 Disclosures of June 2020: Section 1.2 'Credit Risk Weighted Assets' (p.3) and Section 8 (operational risk, p.19), stated to 0.1 of £m only", {}),
    ("DATA", "Credit risk (excluding CCR)", {"FY2020": 119400}),
    ("DATA", "Operational risk", {"FY2020": 51600}),
    ("TOTAL", "Total", {"FY2020": 171000}),
]
bw.add_rwa_breakdown_sheet(
    title="Chetwood Financial Limited — RWA Breakdown",
    subtitle="£'000, Group/consolidated basis (FY2020-FY2021: standalone entity). FY2019 blank - Chetwood published no Pillar 3 disclosure that year. FY2020 added 2026-09-15 and is stated to 0.1 of £m only. See source note at bottom.",
    rows=rwa_breakdown_rows,
    sources_text=RWA_BREAKDOWN_SOURCES,
    first_col_width=54,
    source_height=220,
)

metric(
    "Leverage Ratio", "£'000 / %",
    [
        ("Leverage ratio total exposure measure", {"FY2025": 3615720, "FY2024": 2387717, "FY2023": 1519817, "FY2022": 394658, "FY2021": 216375}),
        ("Leverage ratio (%)", {"FY2025": "5.19%", "FY2024": "7.19%", "FY2023": "6.01%", "FY2022": "14.58%", "FY2021": "23.4%", "FY2020": "19%"}),
    ],
    p3_sources(),
    note=FY2024_GAP_NOTE + " Unlike Barclays/Monzo, Chetwood's disclosures do not distinguish an 'excluding/including "
         "claims on central banks' basis in any year - a single leverage ratio definition is used throughout "
         "(Tier 1 capital / total exposure measure). FY2021 used a pre-KM1 narrative table; FY2022 onward uses the "
         "formal KM1 rows 13-14.\n" + FY2020_P3_NOTE + " FY2020 discloses only the headline ratio (19%, stated "
         "twice - in the Summary-analysis table and again in Section 3.6, 'At 31 March 2020, the leverage ratio "
         "stood at 19%'); no total exposure measure is given anywhere in that document, so that row stays blank "
         "for FY2020 rather than being back-solved from the ratio.",
)

metric(
    "LCR", "£'000 / %",
    [
        ("Total high-quality liquid assets (HQLA) (weighted value - average)", {"FY2025": 897493, "FY2024": 665116, "FY2023": 302266, "FY2022": 67841}),
        ("Cash outflows - total weighted value", {"FY2025": 489794, "FY2024": 395674, "FY2023": 52035, "FY2022": 5627}),
        ("Cash inflows - total weighted value", {"FY2025": 28009, "FY2024": 34098, "FY2023": 15169, "FY2022": 13656}),
        ("Total net cash outflows (adjusted value)", {"FY2025": 461785, "FY2024": 361576, "FY2023": 36865, "FY2022": 1407}),
        ("Liquidity Coverage Ratio (%)", {"FY2025": "194%", "FY2024": "184%", "FY2023": "1,015%", "FY2022": "4,823%", "FY2021": "51,086%", "FY2020": "68,110%"}),
    ],
    p3_sources(),
    note=FY2024_GAP_NOTE + " FY2020 and FY2021 disclosed only the headline ratio in narrative form (no HQLA/outflow "
         "£ breakdown was published those years - the formal KM1 liquidity rows were introduced from FY2022). "
         "Chetwood's LCR ratios are extremely high because, as a young/small deposit-taker at the time, its "
         "regulatory outflow assumptions were small relative to its liquid asset holdings - this is as disclosed "
         "by Chetwood, not a transcription error; the FY2020 document says so in terms ('Given the early stage of "
         "Chetwood's development and the limited value of outflows the calculation of the Liquidity Coverage "
         "Ratio (LCR) results in a very high value. Chetwood's LCR ratio as at 31st March 2020 was 68,110%').\n"
         + FY2020_P3_NOTE,
)

metric(
    "NSFR", "£'000 / %",
    [
        ("Total available stable funding", {"FY2025": 3677559, "FY2024": 2862609, "FY2023": 1387511, "FY2022": 380549}),
        ("Total required stable funding", {"FY2025": 2536343, "FY2024": 1760110, "FY2023": 572002, "FY2022": 233566}),
        ("Net Stable Funding Ratio (%)", {"FY2025": "145%", "FY2024": "163%", "FY2023": "243%", "FY2022": "162.9%", "FY2021": "146.5%", "FY2020": "193%"})
    ],
    p3_sources(),
    note=FY2024_GAP_NOTE + " FY2021's NSFR figure (146.5%) is quoted exactly as printed in the FY2021 Pillar 3 "
         "report, which oddly labels it 'as at the 31 March 2020' in a document otherwise dated 'as at 31 March "
         "2021' - this looks like a typo in Chetwood's own document, but it is reproduced verbatim rather than "
         "silently corrected; no £ breakdown was published for FY2020 or FY2021 (the formal KM1 NSFR rows were "
         "introduced from FY2022).\n" + FY2020_P3_NOTE + " FY2020's own 193% comes from that year's own document "
         "('The Company's Net Stable Funding Ratio (NSFR) as at the 31 March 2020 was 193%') and is a genuinely "
         "different figure from the 146.5% the FY2021 report mislabels as 'at the 31 March 2020' - further "
         "evidence that the FY2021 label is the typo, and that 146.5% belongs to FY2021 as carried here.",
)

# GA-020 (2026-09-19): the bare "Not applicable" is split by what each year's document says.
# FY2021/FY2022/FY2023 Pillar 3 (Wayback id_ captures, text): "has no minimum requirements for Own
# funds and Eligible Liabilities (MREL) above its minimum capital requirement". FY2025 Pillar 3
# (live, SNCI reduced format): no MREL statement or figure; FY2025 and FY2024 Annual Reports
# (text): zero MREL hits. SNCI status alone does not settle MREL, so FY2025 is "Not published",
# not extrapolated. FY2024: the FY2024 Pillar 3 (Nov 2024, cdn.sanity.io, found in the GA-020
# second pass 2026-09-19) is the same SNCI reduced format: text layer rich ('capital' 79 whole-word
# hits, 'liquidity' 11, 'own funds' 5) and 0 hits for MREL, 'eligible liabilities', 'loss-absorbing'
# or 'insolvency'; its contents page has no MREL section. So FY2024 is "Not published", like FY2025.
_MREL_NA = ("Not applicable – Chetwood Pillar 3 {y}: 'has no minimum requirements for Own funds and Eligible "
            "Liabilities (MREL) above its minimum capital requirement'.")
MREL_ST = {y: _MREL_NA.format(y=y) for y in ["FY2023", "FY2022", "FY2021"]}
MREL_ST["FY2025"] = ("Not published – Chetwood Pillar 3 FY2025 (SNCI reduced format) and Annual Report 2025 (text "
                     "search, 2026-09-19) give no MREL figure or statement.")
MREL_ST["FY2024"] = ("Not published – Chetwood Pillar 3 FY2024 (Nov 2024, SNCI reduced format, contents p.2) and Annual "
                     "Report 2024 (text search, 2026-09-19) give no MREL figure or statement.")
metric(
    "MREL Ratio", None,
    [("MREL ratio", MREL_ST)],
    p3_sources(),
    note="Chetwood is classified as a 'small and non-complex institution' (SNCI) and is not subject to any MREL "
         "requirement above its minimum capital requirement - stated explicitly in the FY2021, FY2022 and FY2023 "
         "Pillar 3 reports ('...has no minimum requirements for Own funds and Eligible Liabilities (MREL) above "
         "its [minimum capital requirement]'). The FY2025 report uses a shorter reduced-disclosure format that "
         "omits this narrative section, but there is no indication Chetwood's MREL/SNCI status has changed. "
         "FY2019/FY2020 are left blank rather than 'Not applicable'. For FY2019 no Pillar 3 disclosure was "
         "published at all. For FY2020 one was (located 2026-09-15 - see the source note), but it was read in "
         "full and the word MREL does not appear anywhere in it, so Chetwood's SNCI/MREL status as at 31 March "
         "2020 was still never publicly stated - blank remains correct for that year, now on evidence rather "
         "than on the absence of a document.",
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {"FY2025": 4532547, "FY2024": 3077904, "FY2023": 1494541, "FY2022": 400038, "FY2021": 216524, "FY2020": 266053, "FY2019": 77767}),
        ("Loans and advances to customers", {"FY2025": 2691247, "FY2024": 1833411, "FY2023": 649179, "FY2022": 302546, "FY2021": 156249, "FY2020": 145022, "FY2019": 46269}),
        ("Customer deposits", {"FY2025": 3812429, "FY2024": 2856737, "FY2023": 1383305, "FY2022": 322625, "FY2021": 160015, "FY2020": 210783, "FY2019": 26107}),
        ("Total equity", {"FY2025": 196143, "FY2024": 173082, "FY2023": 92483, "FY2022": 65993, "FY2021": 50830, "FY2020": 51182, "FY2019": 49484}),
    ],
    balance_sheet_unit="£'000",
    income_statement_totals=[
        ("Total income", {"FY2025": 54238, "FY2024": 45989, "FY2023": 21471, "FY2022": 27428, "FY2021": 14447, "FY2020": 7673, "FY2019": 1699}),
        ("Administrative expenses", {"FY2025": -57209, "FY2024": -53995, "FY2023": -56119, "FY2022": -30809, "FY2021": -22372, "FY2020": -14413, "FY2019": -11240}),
        ("Loss after tax and loss for the year", {"FY2025": -4702, "FY2024": -8861, "FY2023": -58148, "FY2022": -29753, "FY2021": -21310, "FY2020": -18314, "FY2019": -11536}),
    ],
    income_statement_unit="£'000",
    equity_changes_totals=[
        ("Opening equity", {"FY2025": 173082, "FY2024": 92483, "FY2023": 65993, "FY2022": 50830, "FY2021": 43067, "FY2020": 49484, "FY2019": 5783}),
        ("Total comprehensive income/(loss)", {"FY2025": -4084, "FY2024": -8685, "FY2023": -58324, "FY2022": -29873, "FY2021": -21339, "FY2020": -18314, "FY2019": -11536}),
        ("Other movements, net", {"FY2025": 27145, "FY2024": 89284, "FY2023": 84814, "FY2022": 45036, "FY2021": 29102, "FY2020": 20012, "FY2019": 55237}),
        ("Closing equity", {"FY2025": 196143, "FY2024": 173082, "FY2023": 92483, "FY2022": 65993, "FY2021": 50830, "FY2020": 51182, "FY2019": 49484}),
    ],
    equity_changes_unit="£'000",
    cash_flow_totals=[
        ("Net cash from operating activities", {"FY2025": 43038, "FY2024": 189520, "FY2023": 653419, "FY2022": 16976, "FY2021": -92120, "FY2020": 69197, "FY2019": -27621}),
        ("Net cash from/(used in) investing activities", {"FY2025": -741638, "FY2024": -389775, "FY2023": -124128, "FY2022": -177719, "FY2021": 26853, "FY2020": -149, "FY2019": -514}),
        ("Net cash from/(used in) financing activities", {"FY2025": 500016, "FY2024": 98027, "FY2023": 84573, "FY2022": 183068, "FY2021": 28960, "FY2020": -8176, "FY2019": 53243}),
        ("Closing cash and cash equivalents", {"FY2025": 387550, "FY2024": 586134, "FY2023": 688362, "FY2022": 74498, "FY2021": 52173, "FY2020": 88480, "FY2019": 27607}),
    ],
    cash_flow_unit="£'000",
    ratios=[
        ("CET1 Ratio", {"FY2025": "15.2%", "FY2024": "20.8%", "FY2023": "26.6%", "FY2022": "29.3%", "FY2021": "28%", "FY2020": "30%"}),
        ("Tier 1 Ratio", {"FY2025": "15.2%", "FY2024": "20.8%", "FY2023": "26.6%", "FY2022": "29.3%", "FY2021": "28%", "FY2020": "30%"}),
        ("Total Capital Ratio", {"FY2025": "15.2%", "FY2024": "20.8%", "FY2023": "26.6%", "FY2022": "29.3%", "FY2021": "28%", "FY2020": "31%"}),
        ("Leverage Ratio", {"FY2025": "5.19%", "FY2024": "7.19%", "FY2023": "6.01%", "FY2022": "14.58%", "FY2021": "23.4%", "FY2020": "19%"}),
        ("LCR", {"FY2025": "194%", "FY2024": "184%", "FY2023": "1,015%", "FY2022": "4,823%", "FY2021": "51,086%", "FY2020": "68,110%"}),
        ("NSFR", {"FY2025": "145%", "FY2024": "163%", "FY2023": "243%", "FY2022": "162.9%", "FY2021": "146.5%", "FY2020": "193%"}),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own source "
         "citation for the underlying document/page. Ratios are blank for FY2019 (Chetwood published no Pillar 3 "
         "disclosure that year); FY2020 was blank on the same basis until 2026-09-15, when its own 'as at 31 "
         "March 2020' Pillar 3 document was located - see any Pillar 3 sheet's source note for that correction. "
         "Note the ~£8.1m FY2020-closing/FY2021-opening equity gap explained on the "
         "Statement of Changes in Equity sheet (FRS 102-to-IFRS transition). " + FY2024_GAP_NOTE,
)

bw.save("/Users/armaan/code/katalysis/banks/CHETWOOD FINANCIALS.xlsx")
