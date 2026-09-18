import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

# Y is the extended (14-year) list used only for the four statutory-statement
# sheets (Balance Sheet, Profit & Loss, Statement of Changes in Equity, Cash
# Flow Statement), per wayfinder ticket HD-072. Y_CORE is the project-wide
# 12-year list the workbook itself (and hence Pillar 3, Asset Quality, RWA
# Breakdown and the Overview sheet, none of which are in scope for HD-072)
# is built on - passed to BankWorkbook(years=...) so those sheets' own year
# columns are untouched. The three statutory sheets pass years=Y explicitly
# to their add_*_sheet() calls to widen just their own header row.
Y=["FY2025","FY2024","FY2023","FY2022","FY2021","FY2020","FY2019","FY2018","FY2017","FY2016","FY2015","FY2014","FY2013","FY2012"]
Y_CORE=["FY2025","FY2024","FY2023","FY2022","FY2021","FY2020","FY2019","FY2018","FY2017","FY2016","FY2015","FY2014"]
AR={"FY2025":"https://www.shawbrook.co.uk/media/vkkpos4a/shawbrook-bank-limited-2025-annual-report-accounts.pdf","FY2024":"https://www.shawbrook.co.uk/media/jhujcnzh/shawbrook-bank-limited-2024-annual-report-accounts.pdf","FY2023":"https://www.shawbrook.co.uk/media/iflapcxl/shawbrook-bank-ltd-annual-report-and-accounts-2023.pdf","FY2022":"https://www.shawbrook.co.uk/media/wttf0kdt/2022-shawbrook-bank-limited-annual-report-and-accounts.pdf","FY2021":"https://www.shawbrook.co.uk/media/ft4eulfp/shawbrook-bank-ara-2021.pdf",
"FY2020":"https://www.shawbrook.co.uk/media/bvvovq0d/shawbrook-bank-limited-annual-report-2020.pdf","FY2019":"https://www.shawbrook.co.uk/media/pqtkvwzv/sb-limited-ara-2019.pdf",
"FY2018":"https://find-and-update.company-information.service.gov.uk/company/00388466/filing-history (Shawbrook Bank Limited Annual Report and Accounts 2018, as filed with Companies House)",
"FY2017":"https://find-and-update.company-information.service.gov.uk/company/00388466/filing-history (Shawbrook Bank Limited Annual Report and Accounts 2017, as filed with Companies House)",
"FY2016":"https://find-and-update.company-information.service.gov.uk/company/00388466/filing-history (Shawbrook Bank Limited Annual Report and Accounts 2016, as filed with Companies House)",
"FY2015":"https://find-and-update.company-information.service.gov.uk/company/00388466/filing-history (Shawbrook Bank Limited Annual Report and Accounts 2015, as filed with Companies House)",
"FY2014":"https://find-and-update.company-information.service.gov.uk/company/00388466/filing-history (Shawbrook Bank Limited Annual Report and Accounts 2014, as filed with Companies House)",
"FY2013":"https://find-and-update.company-information.service.gov.uk/company/00388466/filing-history (Shawbrook Bank Limited Annual Report and Accounts 2013, as filed with Companies House, filed 09 Jun 2014)",
"FY2012":"https://find-and-update.company-information.service.gov.uk/company/00388466/filing-history (Shawbrook Bank Limited Annual Report and Accounts 2012, as filed with Companies House, filed 20 May 2013)"}
P3={"FY2025":"https://www.shawbrook.co.uk/media/w5chxn4q/shawbrook-pillar-3-disclosures-2025.pdf","FY2024":"https://www.shawbrook.co.uk/media/rzpdavyj/shawbrook-2024-pillar-3-disclosures.pdf","FY2023":"https://www.shawbrook.co.uk/media/wrpglj2h/shawbrook-pillar-3-disclosures-2023.pdf","FY2022":"https://www.shawbrook.co.uk/media/pljhf2fo/2022-shawbrook-pillar-3-disclosures.pdf","FY2021":"https://www.shawbrook.co.uk/media/hlbpmnjm/pillar-3-2021.pdf",
"FY2020":"https://www.shawbrook.co.uk/media/zlibpqlt/pillar-3-2020.pdf","FY2019":"https://www.shawbrook.co.uk/media/yhdl0kcs/pillar-3-2019.pdf",
"FY2018":"https://www.shawbrook.co.uk/media/vypjeoat/pillar-3-2018.pdf","FY2017":"https://www.shawbrook.co.uk/media/3wefl2tu/pillar-3-2017.pdf",
"FY2016":"https://www.shawbrook.co.uk/media/koignkmo/pillar-3-2016.pdf","FY2015":"https://www.shawbrook.co.uk/media/4galhsik/pillar-3-2015.pdf",
"FY2014":"https://www.shawbrook.co.uk/media/cc5dq5j0/pillar-3-2014.pdf"}
# Dead originals, retained for provenance - do NOT delete. shawbrook.co.uk
# relocated its investor documents to /about-us/investors/results-centre/ and
# re-issued new Umbraco media GUIDs for the FY2014-FY2020 Pillar 3 PDFs; the
# URLs below were confirmed HTTP 404 (not blocked, not soft-404) on
# 15 September 2026 and replaced by the /media/... URLs now in P3 above.
P3_DEAD={
"FY2020":"https://www.shawbrook.co.uk/media/xexpjjkq/shawbrook-pillar-3-disclosures-2020.pdf",
"FY2019":"https://www.shawbrook.co.uk/media/2azlz2vz/shawbrook-pillar-3-disclosures-2019.pdf",
"FY2018":"https://www.shawbrook.co.uk/media/kfnfg0oe/shawbrook-pillar-3-disclosures-2018.pdf",
"FY2017":"https://www.shawbrook.co.uk/media/3lifgtxe/shawbrook-pillar-3-disclosures-2017.pdf",
"FY2016":"https://www.shawbrook.co.uk/media/1lhngswy/shawbrook-pillar-3-disclosures-2016.pdf",
"FY2015":"https://www.shawbrook.co.uk/media/wdvhqxsn/shawbrook-pillar-3-disclosures-2015.pdf",
"FY2014":"https://www.shawbrook.co.uk/media/qsxpg41l/shawbrook-pillar-3-disclosures-2014.pdf"}
LINK_PROVENANCE=(
"LINK PROVENANCE (checked 15 September 2026): the FY2014-FY2020 Pillar 3 URLs cited here are REPLACEMENT URLs. "
"shawbrook.co.uk moved its investor documents to /about-us/investors/results-centre/ and re-issued the media GUIDs, "
"so the URLs originally cited in this workbook now return HTTP 404. The dead originals are recorded here so the "
"provenance chain stays readable - each replacement was fetched, confirmed to be a real PDF (%PDF magic bytes, not "
"merely HTTP 200), and its cover and Appendix 1 read to confirm the year and the entity before substitution:\n"
+"\n".join(f"  {y}: DEAD (404 as at 15 Sep 2026) {P3_DEAD[y]}  ->  LIVE {P3[y]}" for y in ["FY2020","FY2019","FY2018","FY2017","FY2016","FY2015","FY2014"])+
"\nREPRODUCTION CHECK: because the replacements were matched on year and entity rather than byte-compared with the "
"dead originals, every FY2014-FY2020 figure in this workbook was re-read from the replacement documents. All "
"reproduce exactly, with no restatement between editions: FY2020/FY2019 from the Pillar 3 Disclosures 2020 "
"'Key risk metrics for Shawbrook Bank Limited', capital-composition, LRCom and 'Risk-weighted assets and minimum "
"capital requirements under Pillar 1 for Shawbrook Bank Limited' tables in Appendix 1; FY2018/FY2017 from the "
"Pillar 3 Disclosures 2018 Appendix 1 capital-composition and LRCom tables; FY2016 from the Pillar 3 Disclosures "
"2016 Appendix 1 (independently cross-checked against the FY2016 comparative column in the 2017 Appendix 1, which "
"agrees exactly); FY2015 and FY2014 from the Pillar 3 Disclosures 2015 and 2014 Appendix 1 tables respectively.\n"
"ENTITY BASIS CHECK: all seven replacement documents are published by Shawbrook GROUP plc, but every figure taken "
"from them is read from the Bank-level section - 'Appendix 1: Disclosures for Shawbrook Bank Limited' (present in "
"the 2014, 2015, 2016, 2017, 2018 and 2020 editions), which is the Article 13 CRR reduced disclosure of Shawbrook "
"Bank Limited as the Group's significant subsidiary, i.e. the entity's own figures, not the Group consolidation. "
"Confirmed by the Group/Bank divergence in the same documents: the 2018 edition's GROUP leverage ratio is 9.2% "
"(2017: 9.4%) whereas its Bank Appendix 1 gives 9.2% (2017: 9.5%) - this workbook records 9.2%/9.5%, the Bank "
"figures. No Group figure sits in any entity-level sheet."
)
# Direct Companies House DOCUMENT urls for the FY2016-FY2018 Shawbrook Bank Limited
# filings. The AR{} entries above point at the filing-history LANDING page for those
# years, which is enough to find the filing but does not cite the document itself;
# these are the per-filing document endpoints, added 2026-09-18 when the "Capital
# risk and management" tables in those three filings were read for the first time.
# All three are IMAGE-ONLY SCANS: pdftotext returns one byte per page and nothing
# else, so a text search of them finds nothing and proves nothing. They were
# rasterised at 150 dpi, OCR'd, and every figure taken from them was then confirmed
# against the rendered page image.
AR_CH_DOC={
"FY2018":"https://find-and-update.company-information.service.gov.uk/company/00388466/filing-history/MzIzNDc4MDM1N2FkaXF6a2N4/document",
"FY2017":"https://find-and-update.company-information.service.gov.uk/company/00388466/filing-history/MzIwMjQ5NTg0MGFkaXF6a2N4/document",
"FY2016":"https://find-and-update.company-information.service.gov.uk/company/00388466/filing-history/MzE3ODQyMDQ3MWFkaXF6a2N4/document"}

# ---------------------------------------------------------------------------
# FY2016-FY2018 Bank capital ratios and RWAs - RECOVERED 2026-09-18.
#
# These three years were an INTERIOR hole: FY2019 above them and FY2015/FY2014
# below them were populated on the CET1 Ratio, Tier 1 Ratio, Total Capital Ratio,
# Total RWAs and RWA Breakdown sheets, and only FY2016-FY2018 were blank. That
# shape rules out the usual explanation ("the disclosure did not exist yet").
#
# The previous note was ACCURATE ABOUT THE PILLAR 3 DOCUMENTS and wrong only in
# treating them as the whole world. Re-read this pass: the Pillar 3 Disclosures
# 2016 (Appendix 1, pp.42-45), 2017 (Appendix 1, pp.42-45) and 2018 (Appendix 1,
# pp.33-36) really do drop the Bank-level "Pillar 1 requirement / capital ratio"
# table that the 2015 edition carried - the 2016 and 2017 Appendix 1 sections
# give only capital composition, an equity reconciliation, a Tier 1 movement
# table and the LRSum/LRCom leverage templates, and the 2018 Appendix 1 adds a
# credit-risk-exposure table whose RWAs (3,830.9 for FY2018) are CREDIT RISK
# ONLY, with no operational-risk component at Bank level. So no Bank Total RWA
# can be assembled from the Pillar 3 documents for these years, exactly as
# recorded. The metric had simply MOVED: for these three years Shawbrook
# published the Bank's total RWAs and capital ratios in the Bank's own Annual
# Report and Accounts instead, in the "Capital risk management"/"Capital risk
# and management" section, with explicit Group and Company columns side by side.
# Only the COMPANY columns are used below - that is Shawbrook Bank Limited,
# the entity this workbook covers - and no Group figure is taken anywhere.
#
#   FY2018: Annual Report and Accounts 2018, Note 12 "Capital risk and
#           management", printed p.62 - "Risk-weighted assets" table (Company
#           2018 total 4,218.1 vs Group 4,206.8) and "Capital ratios" table
#           (Company 2018 CET1 12.2%, Total Tier 1 15.2%, Total capital 16.9%).
#   FY2017: Annual Report and Accounts 2017, "Risk management" section, printed
#           pp.92-93 - RWA table (Company 2017 total 3,335.4 vs Group 3,361.7)
#           and "The key capital ratios" table (Company 2017 CET1 12.9%, Total
#           Tier 1 16.7%, Total capital 19.3%, Leverage 9.5%).
#   FY2016: Annual Report and Accounts 2016, "Risk management - Capital risk
#           management", printed p.90 - one combined table giving the Company
#           2016 ratios (CET1 13.2%, Total capital 16.3%, Leverage 7.7%) and the
#           Company 2016 RWA categories totalling 2,778.6.
#
# ONE FIGURE IS NOT FROM ITS OWN YEAR'S EDITION, and is labelled as such
# wherever it appears: FY2016's TIER 1 RATIO. The 2016 Annual Report's ratio
# table has only three rows (CET1, Total capital, Leverage) and prints no Tier 1
# ratio at all. The 2017 Annual Report's four-column table does, and gives the
# Company 2016 Total Tier 1 capital ratio as 13.2% - i.e. equal to that year's
# CET1 ratio, which is consistent with the Bank holding no Additional Tier 1
# until the £125.0m capital securities issued in 2017, though the 13.2% carried
# here is the PRINTED comparative and not that inference.
#
# CROSS-EDITION DIFFERENCE, RECORDED NOT RECONCILED: the FY2018 Annual Report's
# FY2017 comparative RWA column splits out a "Credit valuation adjustment" row
# of 0.9 and shows "Other" as 65.8, where the FY2017 Annual Report's own column
# shows "Other" 66.7 and no CVA row. The two foot to the identical total of
# 3,335.4. Each year is taken from its own edition, so FY2017 below carries
# Other 66.7 with no CVA row, as its own document prints it.
#
# FY2015 CONTEXT, deliberately left alone: the FY2016 Annual Report's own
# Company 2015 comparative column totals 2,174.6, whereas this workbook's
# FY2015 Total RWA is 2,175.9 - the "Total risk exposure amount" the Bank
# states directly in its own FY2015 Pillar 3 countercyclical-buffer table. That
# £1.3m difference is a genuine cross-document difference for the same date and
# entity; FY2015 keeps its own year's own source and is NOT restated to match.
# ---------------------------------------------------------------------------
BANK_ARA_CAPITAL_NOTE=(
"FY2018-FY2016 Bank Total RWAs and capital ratios come from Shawbrook Bank Limited's OWN ANNUAL REPORT AND "
"ACCOUNTS for each of those years, not from a Pillar 3 document, and specifically from the COMPANY column of "
"tables that print Group and Company side by side (no Group figure is used anywhere in this workbook). "
"Recovered 2026-09-18, closing an interior gap: FY2019 above and FY2015/FY2014 below were already populated, "
"so these three blanks could not be explained by the disclosure not yet existing. The earlier note was right "
"that the Pillar 3 documents of those years cannot supply the figure - re-read this pass, the 2016 and 2017 "
"editions' Appendix 1 gives only capital composition, an equity reconciliation, a Tier 1 movement table and "
"the LRSum/LRCom leverage templates, and the 2018 edition's Appendix 1 adds a credit-risk exposure table whose "
"RWAs (3,830.9 for FY2018) are CREDIT RISK ONLY with no Bank-level operational-risk component - but the "
"metric had moved to the Annual Report rather than ceasing to exist. Sources, each read from that year's own "
"edition: FY2018 - Annual Report and Accounts 2018, Note 12 'Capital risk and management', printed p.62, "
"'Risk-weighted assets' and 'Capital ratios' tables (Company 2018: total RWAs 4,218.1; CET1 12.2%; Total Tier "
"1 15.2%; Total capital 16.9%) - "+AR_CH_DOC["FY2018"]+" ; FY2017 - Annual Report and Accounts 2017, 'Risk "
"management', printed pp.92-93 (Company 2017: total RWAs 3,335.4; CET1 12.9%; Total Tier 1 16.7%; Total "
"capital 19.3%) - "+AR_CH_DOC["FY2017"]+" ; FY2016 - Annual Report and Accounts 2016, 'Risk management - "
"Capital risk management', printed p.90 (Company 2016: total RWAs 2,778.6; CET1 13.2%; Total capital 16.3%) - "
+AR_CH_DOC["FY2016"]+" . All three filings are IMAGE-ONLY SCANS whose text layer is empty (pdftotext returns "
"one byte per page), so a text search of them returns nothing and proves nothing; they were rasterised at 150 "
"dpi, OCR'd, and every figure was then confirmed against the rendered page image itself. "
"THE ONE FIGURE NOT TAKEN FROM ITS OWN YEAR'S EDITION, labelled here and on the Tier 1 Ratio sheet: FY2016's "
"TIER 1 RATIO of 13.2% is the COMPARATIVE COLUMN of the Annual Report and Accounts 2017 (printed p.93). The "
"2016 Annual Report's own ratio table prints only CET1, Total capital and Leverage and gives no Tier 1 ratio. "
"CROSS-EDITION DIFFERENCE, RECORDED NOT RECONCILED: the 2018 Annual Report's FY2017 comparative RWA column "
"splits out a 'Credit valuation adjustment' of 0.9 and shows 'Other' 65.8, while the 2017 Annual Report's own "
"column shows 'Other' 66.7 with no CVA row; both foot to the same 3,335.4, and FY2017 is carried as its own "
"edition prints it. "
"FY2015 IS NOT RESTATED to match these documents: the 2016 Annual Report's Company 2015 comparative totals "
"2,174.6 against the 2,175.9 this workbook carries from the Bank's own FY2015 Pillar 3 countercyclical-buffer "
"table - a genuine £1.3m cross-document difference for the same date and entity, left as each document states "
"it.")

def d(vals): return dict(zip(Y,vals))
note=("Shawbrook Bank Limited (Companies House 00388466; FRN 204574; LEI 213800XSHRKUIZK86B68) is the matched legal entity. "
"Cash flows use the Company column, £m, from the Bank's consolidated-and-company accounts. Bank-specific Pillar 3 metrics are used for FY2015-FY2024 (all years with a Bank-specific figure disclosed). "
"The FY2025 Pillar 3 publication is Group-only after the listing and is not substituted for Bank data - independently re-confirmed 15 September 2026: shawbrook-pillar-3-disclosures-2025.pdf is headed 'Shawbrook Group plc Company No: 07240248', states that the PRA supervises Shawbrook Group plc on a consolidated basis, and contains a single reporting section with no Shawbrook Bank Limited solo or sub-consolidated disclosure. FY2025 Bank-level capital, RWA, leverage and NSFR figures are therefore taken from Shawbrook Bank Limited's own Annual Report and Accounts 2025 instead: Key Performance Indicators table p.9 (CET1 ratio 12.4%, Total Tier 1 capital ratio 13.5%, Total capital ratio 14.9%, Leverage ratio 7.8%, Risk-weighted assets 12,000.4), Risk Report - Regulatory capital (audited) p.90 (Common Equity Tier 1 capital 1,495.7; Additional Tier 1 125.0; Total Tier 1 capital 1,620.7; Tier 2 163.8; Total regulatory capital 1,784.5) and Risk Report - Net stable funding ratio p.89 (NSFR 124.9% at 31 December 2025, 2024: 134.5%). The FY2025 LCR is the one metric on a different basis: the Annual Report's 147.2% is a point-in-time year-end ratio, not the 12-month-average UK KM1 measure used for FY2022-FY2024 here (the same Annual Report reports FY2024 as 176.0% against the 265.0% recorded here from that year's Bank Pillar 3, an 89-point gap for the same date and entity). UPDATED 2026-09-18: it was previously left wholly blank; it is now carried on its own separate, labelled point-in-time row of the LCR sheet, alongside the liquidity buffer and net-cash-outflow amounts it is struck from, so the figure is visible without ever being spliced into the KM1-average series - see the LCR sheet. Every other FY2024 comparative in the Annual Report reproduces this workbook's Bank-level Pillar 3 figures exactly. FY2022 RWA/capital comparatives use the restatement in the 2023 Pillar 3 disclosure; FY2021 and FY2022 leverage bases differ. "
"FY2014-FY2018 statements were sourced from Companies House filing-history (scanned filings, OCR'd) because shawbrook.co.uk's own hosted 'Annual Report' links for those years are Shawbrook Group plc (holdco) documents, not Bank-entity accounts; FY2019-FY2020 statements use the Bank-entity reports hosted on shawbrook.co.uk directly. "
"FY2018-FY2016 Bank-level Total RWAs and CET1/Tier1/Total Capital ratios were POPULATED on 2026-09-18 and are no longer blank. This note previously read that they were blank because those years' Pillar 3 disclosures give a Bank-level credit-risk RWA figure but never an operational-risk RWA component at Bank level. That was true of the Pillar 3 documents and remains true - it was simply not the whole world: for these three years Shawbrook published the Bank's total RWAs and capital ratios in Shawbrook Bank Limited's OWN Annual Report and Accounts, in tables that print Group and Company columns side by side, and the Company column is used here. No Group figure has been substituted anywhere. See the Total RWAs / RWA Breakdown sheet notes for the exact pages and the one comparative-sourced figure (FY2016's Tier 1 ratio). FY2019 Bank Total RWA/ratios use the comparative column in the FY2020 Pillar 3 disclosure (the first year Shawbrook disclosed a full Bank-level RWA-by-category table); FY2019's own Pillar 3 document did not itself disclose this breakdown. "
"FY2015's Bank Total RWA (£2,175.9m) is the 'Total risk exposure amount' of £2,175,860k stated directly in the Bank's own countercyclical-capital-buffer table, Pillar 3 Disclosures 2015 Appendix 1 p.34 - a disclosed figure, not a derived one. FY2014's Bank Total RWA (£1,460.0m) has no such directly stated equivalent (the 2014 disclosure predates the countercyclical-buffer template) and is the one derived figure on this sheet: the Bank's own disclosed Pillar 1 capital requirement (Credit risk £112.4m + Operational risk £4.4m) grossed up at 8%. CORRECTION (15 September 2026): this paragraph previously stated that FY2015 used a derived £2,173.8m total 'in preference to' the disclosed £2,175.9m; that was the wrong way round - the workbook has always carried the disclosed £2,175.9m, and the prose has been corrected to match rather than the figure changed. CONSEQUENCE, stated rather than smoothed: on the RWA Breakdown sheet FY2015's two category rows (Credit risk £2,051.3m and Operational risk £122.5m, each grossed up at 8% from the disclosed £164.1m and £9.8m Pillar 1 requirements, since no Bank-level RWA-by-category template existed in 2015) sum to £2,173.8m, £2.1m short of the disclosed £2,175.9m total - a rounding artefact of grossing up capital requirements stated to £0.1m. FY2015 is therefore the one populated year on that sheet whose categories do not foot exactly to the total. "
"Per wayfinder ticket HD-072 (2026-09-06), FY2013 and FY2012 were added to the four statutory-statement sheets only "
"(Balance Sheet, Profit & Loss, Statement of Changes in Equity, Cash Flow Statement) - Pillar 3, Asset Quality and "
"RWA Breakdown remain FY2014-floored, since Pillar 3 disclosures genuinely aren't comparable pre-CRD IV/Basel III.")
cf="Sources - Shawbrook Bank Limited Company cash flows (£m):\n"+"\n".join(f"{y}: Annual Report and Accounts cash-flow statement, p.{({'FY2021':106,'FY2022':98,'FY2023':111,'FY2024':107,'FY2025':114}[y])}, {AR[y]}" for y in Y if y in {'FY2021','FY2022','FY2023','FY2024','FY2025'})+"\nFY2020: Annual Report and Accounts 2020, p.111 - "+AR['FY2020']+"\nFY2019: Annual Report and Accounts 2019, p.90 - "+AR['FY2019']+"\nFY2018: Annual Report and Accounts 2018 (Companies House filing), p.80 - "+AR['FY2018']+"\nFY2017: Annual Report and Accounts 2017 (Companies House filing), p.37 - "+AR['FY2017']+"\nFY2016: Annual Report and Accounts 2016 (Companies House filing), p.41 - "+AR['FY2016']+"\nFY2015: Annual Report and Accounts 2015 (Companies House filing), p.53 - "+AR['FY2015']+"\nFY2014: Annual Report and Accounts 2014 (Companies House filing) - "+AR['FY2014']+"\nFY2013: Annual Report and Accounts 2013 (Companies House filing), Company Statement of Cashflows p.20 - "+AR['FY2013']+". Independently cross-checked against the FY2013 comparative column in the Annual Report and Accounts 2014 (Companies House filing) p.35, which agrees exactly on the investing- and financing-activities subtotals but diverges on the operating-activities subtotal (-£10.5m there vs -£10.0m per FY2013's own report) and hence on the cash-and-cash-equivalents balances themselves (see note below) - both attributable to the same reclassification.\nFY2012: Annual Report and Accounts 2012 (Companies House filing), Company Statement of Cashflows p.21 - "+AR['FY2012']+"\n\nNOTE ON A GENUINE, DOCUMENTED CASH-FLOW-CHAIN BREAK AT THE FY2013/FY2014 BOUNDARY: FY2013's own Annual Report "
"reports Company cash and cash equivalents of £180.1m at 1 January 2013 and £230.3m at 31 December 2013 (an exact "
"chain from FY2012's own Annual Report, which reports £180.1m at both 1 January 2012 and, after that year's own "
"movements, matches FY2013's opening figure exactly). The FY2014 Annual Report's own comparative column for "
"FY2013, however, shows £179.9m at 1 January 2013 and £229.6m at 31 December 2013/1 January 2014 (already the "
"figure this workbook uses for FY2014's own opening balance) - roughly £0.7m lower throughout. This is not a "
"transcription error: the FY2014 statement introduces a new 'Increase in mandatory balances with central banks' "
"operating-asset line not present in the FY2012/FY2013 statements' own presentation, consistent with the FY2014 "
"Annual Report having redefined 'cash and cash equivalents' to exclude mandatory central-bank balances that "
"FY2012/FY2013's own statements had included. Per this workbook's standing convention (use each year's own "
"Annual Report, not a later year's restated comparative), the FY2013 and FY2012 cash-flow figures below are "
"FY2013's and FY2012's own reported figures - so FY2013's closing balance (£230.3m) does not tie to FY2014's "
"opening balance (£229.6m) already shown on this sheet; this ~£0.7m gap is a genuine, sourced definitional "
"reclassification, not an omitted plug row."+"\n\n"+note
b=BankWorkbook(bank_name="Shawbrook Bank Limited",years=Y_CORE,year_label={y: y for y in Y},header_color="FE1270")

# ---------------------------------------------------------------
# Statement sources shared by Balance Sheet / P&L / Statement of Changes in
# Equity. Balance Sheet and Equity use the Company column (consistent with
# the existing Company-basis Cash Flow Statement); P&L is necessarily
# Group/Consolidated basis - the Company takes the s.408 Companies Act 2006
# exemption and does not publish a standalone income statement, only a
# single disclosed after-tax profit figure each year (documented below).
# ---------------------------------------------------------------
STATEMENTS_SOURCES = (
    "Sources - Shawbrook Bank Limited:\n"
    f"FY2025: Annual Report and Accounts 2025, Consolidated and Company statement of financial position p.111, "
    f"Company statement of changes in equity p.113, Consolidated statement of profit and loss and other "
    f"comprehensive income (Group basis) p.110 - {AR['FY2025']}\n"
    f"FY2024: Annual Report and Accounts 2024, Consolidated and Company statement of financial position p.104, "
    f"Company statement of changes in equity p.106, Consolidated statement of profit and loss and other "
    f"comprehensive income (Group basis) p.103 - {AR['FY2024']}\n"
    f"FY2023: Annual Report and Accounts 2023, Consolidated and Company statement of financial position p.108, "
    f"Company statement of changes in equity p.110, Consolidated statement of profit and loss p.106 and "
    f"Consolidated statement of comprehensive income p.107 (Group basis) - {AR['FY2023']}\n"
    f"FY2022: Annual Report and Accounts 2022, Consolidated and Company statement of financial position p.95, "
    f"Company statement of changes in equity p.97, Consolidated statement of profit and loss p.93 and "
    f"Consolidated statement of comprehensive income p.94 (Group basis) - {AR['FY2022']}\n"
    f"FY2021: Annual Report and Accounts 2021, Consolidated and Company statement of financial position p.104, "
    f"Company statement of changes in equity p.105, Consolidated statement of profit and loss and other "
    f"comprehensive income (Group basis) p.103 - {AR['FY2021']}\n"
    f"FY2020: Annual Report and Accounts 2020, Consolidated and Company statement of financial position p.109, "
    f"Company statement of changes in equity p.110, Consolidated statement of profit and loss and other "
    f"comprehensive income (Group basis) p.108 - {AR['FY2020']}\n"
    f"FY2019: Annual Report and Accounts 2019, Consolidated and Company statement of financial position p.90, "
    f"Company statement of changes in equity p.91, Consolidated statement of profit and loss and other "
    f"comprehensive income (Group basis) p.89 - {AR['FY2019']}\n"
    f"FY2018: Annual Report and Accounts 2018 (Companies House filing, OCR'd), Consolidated and Company "
    f"statement of financial position p.77, Company statement of changes in equity p.79, Consolidated statement "
    f"of profit and loss and other comprehensive income (Group basis) p.76 - {AR['FY2018']}\n"
    f"FY2017: Annual Report and Accounts 2017 (Companies House filing, OCR'd), Consolidated and Company "
    f"statement of financial position p.34, Company statement of changes in equity p.36, Consolidated statement "
    f"of profit and loss and other comprehensive income (Group basis) p.33 - {AR['FY2017']}. This filing's own "
    f"signature page misprints the registered number as 07240248 (the number for the separate holding company "
    f"'Shawbrook Group plc'/f.k.a. 'Shawbrook Group Limited'/f.k.a. 'Laidlaw Acquisitions Limited') instead of "
    f"Shawbrook Bank Limited's own 00388466; the document's Note 1 'Basis of preparation' unambiguously confirms "
    f"the reporting entity is Shawbrook Bank Limited itself, so this is treated as a clerical error in that one "
    f"filing, not evidence of wrong-entity data.\n"
    f"FY2016: Annual Report and Accounts 2016 (Companies House filing, OCR'd), Consolidated and Company "
    f"Statement of Financial Position p.41, Company statement of changes in equity p.40, Consolidated Statement "
    f"of Profit and Loss and Other Comprehensive Income p.40 - {AR['FY2016']}\n"
    f"FY2015: Annual Report and Accounts 2015 (Companies House filing, OCR'd), Consolidated and Company "
    f"Statements of Financial Position p.51, Company Statement of Changes in Equity p.52, Consolidated Statement "
    f"of profit and loss and Other Comprehensive Income p.50 - {AR['FY2015']}\n"
    f"FY2014: Annual Report and Accounts 2014 (Companies House filing, OCR'd), Statements of Financial Position "
    f"p.34, Company Statement of Changes in Equity p.34, Consolidated Income Statement (Group basis) - {AR['FY2014']}\n"
    f"FY2013: Annual Report and Accounts 2013 (Companies House filing, OCR'd), Statements of Financial Position "
    f"p.17, Company Statement of Changes in Equity p.19, Consolidated Income Statement (Group basis) p.15 - "
    f"{AR['FY2013']}. Independently cross-checked against the FY2013 comparative column in the Annual Report and "
    f"Accounts 2014 (Companies House filing) pp.30/32/34, which agrees on every Balance Sheet, P&L and Statement "
    f"of Changes in Equity line (both are already in £m to 1 decimal place, so this cross-check column is used "
    f"directly for FY2013's Balance Sheet/P&L/Equity figures below in preference to independently rounding "
    f"FY2013's own £000 figures) - {AR['FY2014']}.\n"
    f"FY2012: Annual Report and Accounts 2012 (Companies House filing, OCR'd), Company Statement of Financial "
    f"Position p.17, Company Statement of Changes in Equity p.19, Consolidated Income Statement (Group basis) "
    f"p.14, Consolidated Statement of Comprehensive Income p.15 - {AR['FY2012']}. FY2012's own report separately "
    f"discloses, within its Company Statement of Changes in Equity, a small (£55k) restatement of its own opening "
    f"1 January 2012 retained earnings for an accounting policy change made during 2012 - this is folded directly "
    f"into the single 'Balance at 1 January 2012' row below (immaterial at this sheet's £0.1m precision) rather "
    f"than shown as its own row. A second, larger (£549k) restatement of FY2012's Company closing retained "
    f"earnings/Total equity is disclosed in Note 4 of the FY2013 Annual Report and is shown below as its own "
    f"'Effect of restatement (Note 4, FY2013 Annual Report)' row between FY2012's own closing balance and FY2013's "
    f"own opening balance, consistent with how this sheet already shows the FY2018 IFRS 9 transition as its own "
    f"row - this keeps both FY2012's and FY2013's own reported figures intact rather than silently overwriting "
    f"one with the other.\n\n" + note +
    "\n\nPRESENTATION NOTE: the Company has taken the exemption in s.408 Companies Act 2006 not to present its "
    "own individual income statement, so the P&L sheet is necessarily Group/Consolidated basis (the only fully "
    "disclosed income statement each year), while the Balance Sheet and Statement of Changes in Equity sheets "
    "use the Company column to stay consistent with the existing Company-basis Cash Flow Statement. Each year's "
    "Balance Sheet report also separately discloses the Company's own after-tax profit figure in a footnote "
    "(FY2025: £189.2m; FY2024: £203.2m; FY2023: £246.4m; FY2022: £213.0m; FY2021: £153.5m) - these Company "
    "profit figures do NOT equal the Group P&L's 'Profit after tax' shown on the P&L sheet (FY2025: £194.9m; "
    "FY2024: £219.8m; FY2023: £212.6m; FY2022: £179.7m; FY2021: £149.5m), a genuine Group-vs-Company difference, "
    "not an error - the Statement of Changes in Equity sheet's 'Profit for the year' rows correctly use the "
    "Company's own profit figures, ticking exactly to Company Total equity."
    "\n\nINVESTMENT SECURITIES MEASUREMENT-BASIS SPLIT: the Company's 'Investment securities' balance is "
    "disclosed by IFRS 9 measurement category for FY2018-FY2025, splitting into amortised cost and FVOCI "
    "(mandatorily-at-FVTPL is £nil in every reviewed year). No UK government/gilt/treasury-bill vs other-issuer "
    "split is disclosed in any reviewed year - the only issuer-type analysis Shawbrook gives (Note 25 of the "
    "FY2025 Annual Report; Note 16 of the FY2019 Annual Report) is 'covered bonds' vs 'debt securities' (retained "
    "mortgage-backed notes from the Group's own securitisations), neither of which is a government security, so "
    "that split is not reproduced here. "
    "FY2025/FY2024: Note 25 'Investment securities', Annual Report and Accounts 2025 pp.144-145, discloses "
    "'£178.1 million (2024: £nil) classified as FVOCI'; the Company figures used here (FY2025: £1,986.7m "
    "amortised cost / £178.1m FVOCI; FY2024: £1,449.3m amortised cost / £nil FVOCI) are taken from the Risk "
    "Report's 'Exposure to credit risk' table, p.70, which gives the Group/Company split by measurement category "
    "and ties exactly to each year's Balance Sheet total - " + AR['FY2025'] + "\n"
    "FY2023/FY2022: Note 38 'Financial assets and financial liabilities' (Classification of financial assets and "
    "financial liabilities), Annual Report and Accounts 2023 pp.159-160 (Company table p.160), shows Company "
    "Investment securities entirely in the amortised-cost column (FY2023: £816.3m; FY2022: £716.8m; £nil FVOCI/"
    "FVTPL in both years) - " + AR['FY2023'] + "\n"
    "FY2021/FY2020: Note 41 'Financial instruments' (Classification of financial assets and financial "
    "liabilities), Annual Report and Accounts 2021 pp.156-157, gives the Group table (Investment securities "
    "entirely amortised cost: FY2021 £521.4m; FY2020 £358.2m) plus a Company narrative confirming that 'the "
    "measurement categories that the Company's financial assets ... are allocated to are the same as the Group' - "
    "so the Company's own Investment securities balance (FY2021: £614.8m; FY2020: £421.6m) is taken as entirely "
    "amortised cost, £nil FVOCI/FVTPL - " + AR['FY2021'] + "\n"
    "FY2019/FY2018: accounting policy Note 1.7(i), Annual Report and Accounts 2019 p.103, states plainly that "
    "'Investment securities are classified as financial assets measured at amortised cost' with no FVOCI/FVTPL "
    "carve-out disclosed for either year (Note 16 'Investment securities', p.128, gives the £245.9m/£139.9m "
    "Company totals used elsewhere on this sheet, entirely amortised cost) - " + AR['FY2019'] + "\n"
    "FY2017-FY2013 and FY2012 are left blank for this split: FY2017-FY2013 have no Investment securities balance "
    "at all (see the row above); FY2012's own Annual Report was not reviewed for a measurement-basis breakdown, "
    "so rather than assume its £144.9m follows the same amortised-cost-only pattern seen in every other reviewed "
    "year, it is left blank here."
)

# ---------------------------------------------------------------
# Balance Sheet (Consolidated and Company statement of financial position) -
# Company column throughout. Total assets = Total liabilities + Total
# equity for every year; Total equity ties exactly to the Statement of
# Changes in Equity sheet's own opening/closing balances - zero plug rows.
# ---------------------------------------------------------------
balance_sheet_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and balances at central banks", d([1924.5, 2244.7, 2188.1, 2037.1, 1693.8, 1273.2, 1064.6, 645.2, 752.5, 429.9, 521.9, 313.1, 206.6, 0.2])),
    ("DATA", "Loans and advances to banks", d([200.2, 248.8, 337.5, 199.9, 49.0, 84.7, 52.3, 50.1, 28.5, 24.1, 30.9, 36.4, 23.7, 117.0])),
    ("DATA", "Loans and advances to customers", d([17801.1, 15129.4, 13157.9, 10472.8, 8278.9, 7061.3, 6637.7, 5805.7, 4799.3, 4050.4, 3319.1, 2284.7, 1346.8, 684.4])),
    ("DATA", "Investment securities", d([2164.8, 1449.3, 816.3, 716.8, 614.8, 421.6, 245.9, 139.9, None, None, None, None, None, 144.9])),
    ("DATA", "Investment securities at amortised cost", d([1986.7, 1449.3, 816.3, 716.8, 614.8, 421.6, 245.9, 139.9, None, None, None, None, None, None])),
    ("DATA", "Investment securities at FVOCI", d([178.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, None, None, None, None, None, None])),
    ("DATA", "Derivative financial assets", d([64.1, 151.8, 182.1, 271.6, 21.5, 0.6, 3.1, 1.6, 1.8, 5.2, 2.8, 3.7, None, None])),
    ("DATA", "Current tax receivable", d([12.3, 17.9, None, None, 4.2, 3.0, None, None, None, None, None, None, None, None])),
    ("DATA", "Property, plant and equipment", d([54.0, 64.3, 38.9, 47.8, 47.8, 53.6, 57.2, 38.1, 39.2, 42.6, 48.2, 49.0, 52.9, 59.7])),
    ("DATA", "Intangible assets", d([60.9, 56.2, 51.6, 45.6, 44.3, 45.1, 46.6, 46.4, 44.6, 38.8, 33.6, 28.4, 1.1, None])),
    ("DATA", "Deferred tax assets", d([None, None, 5.4, 11.3, 9.2, 12.3, 14.9, 18.0, 15.7, 17.9, 14.2, 10.0, 8.8, 11.4])),
    ("DATA", "Assets held for sale", d([None, None, None, None, 299.7, 2.3, 104.1, None, None, None, None, None, None, None])),
    ("DATA", "Other assets", d([55.6, 55.0, 50.4, 35.5, 17.5, 20.1, 16.2, 55.1, 19.8, 16.1, 7.4, 6.8, 8.6, 11.0])),
    ("DATA", "Deemed loan due from structured entities", d([52.8, 131.0, 214.1, 93.4, None, None, None, None, None, None, None, None, None, None])),
    ("DATA", "Investment in subsidiaries", d([145.4, 80.6, 58.6, 13.9, 13.9, None, None, None, None, None, None, None, None, 0.0])),
    ("DATA", "Investment in associates", d([None, None, None, None, None, 2.8, 5.4, 5.5, None, None, None, None, None, None])),
    ("TOTAL", "Total assets", d([22535.7, 19629.0, 17100.9, 13945.7, 11094.6, 8980.6, 8248.0, 6805.6, 5701.4, 4625.0, 3978.1, 2732.1, 1648.5, 1028.5])),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Amounts due to banks", d([1430.6, 1372.1, 1397.6, 1498.7, 1200.7, 815.5, 881.6, 1029.4, 607.3, 147.7, 39.9, 41.0, 24.6, None])),
    ("DATA", "Customer deposits", d([18353.5, 15804.0, 13562.7, 10914.5, 8358.6, 6894.1, 6109.4, 4977.9, 4376.2, 3943.5, 3186.4, 2421.0, 1463.0, 923.7])),
    ("DATA", "Provisions", d([8.3, 11.5, 15.9, 6.0, 14.2, 18.0, 8.3, 11.6, 2.8, 1.3, 0.9, 0.6, 0.4, 0.8])),
    ("DATA", "Derivative financial liabilities", d([93.2, 117.1, 184.5, 90.5, 7.9, 42.0, 14.9, 5.7, 3.4, 0.4, None, None, None, 0.0])),
    ("DATA", "Current tax liabilities", d([None, None, 0.2, 3.6, None, None, 1.0, 3.9, 7.8, 14.2, 7.5, None, None, None])),
    ("DATA", "Lease liabilities", d([24.4, 25.0, 5.2, 7.1, 9.4, 11.1, 12.4, None, None, None, None, None, None, None])),
    ("DATA", "Deferred tax liabilities", d([14.5, 7.1, None, None, None, None, None, None, None, None, None, None, None, None])),
    ("DATA", "Other liabilities", d([188.3, 122.4, 85.4, 58.5, 60.7, 41.1, 93.9, 40.7, 26.8, 28.7, 333.7, 41.9, 21.3, 23.9])),
    ("DATA", "Subordinated debt liability", d([171.5, 171.2, 188.8, 97.4, 97.5, 97.7, 96.4, 76.1, 76.1, 76.1, 75.0, 30.8, 27.6, None])),
    ("DATA", "Deemed loan due to structured entities", d([375.7, 388.5, 269.2, 133.0, 402.8, 268.2, 286.2, None, None, None, None, None, None, None])),
    ("TOTAL", "Total liabilities", d([20660.0, 18018.9, 15709.5, 12809.3, 10151.8, 8187.7, 7504.1, 6145.3, 5100.4, 4211.9, 3635.9, 2535.3, 1536.9, 948.4])),
    ("SECTION", "Equity", {}),
    ("DATA", "Share capital", d([225.5, 175.5, 175.5, 175.5, 175.5, 175.5, 175.5, 175.5, 175.5, 175.5, 175.5, 174.5, 129.0, 112.0])),
    ("DATA", "Share premium account", d([81.0, 81.0, 81.0, 81.0, 81.0, 81.0, 81.0, 81.0, 81.0, 81.0, 81.0, None, None, None])),
    ("DATA", "Capital securities", d([125.0, 125.0, 125.0, 125.0, 125.0, 125.0, 125.0, 125.0, 125.0, None, None, None, None, None])),
    ("DATA", "Merger reserve", d([1.6, 1.6, 1.6, 1.6, 1.6, 1.6, 1.6, 1.6, 1.6, 1.6, 1.6, 1.6, None, None])),
    ("DATA", "Capital contribution reserve", d([39.7, 39.7, 39.0, 24.0, 23.9, 17.7, 17.2, 16.4, 16.7, 9.2, 4.4, 0.3, 0.2, 0.2])),
    ("DATA", "Cash flow hedging reserve", d([1.3, 0.1, 0.1, None, None, None, None, None, None, None, None, None, None, None])),
    ("DATA", "Fair value through other comprehensive income reserve", d([43.8, 29.6, -0.3, -10.7, None, None, None, None, None, None, None, None, None, None])),
    ("DATA", "Retained earnings", d([1357.8, 1157.6, 969.5, 740.0, 535.8, 392.1, 343.6, 260.8, 201.2, 145.8, 79.7, 20.4, -17.6, -32.0])),
    ("TOTAL", "Total equity", d([1875.7, 1610.1, 1391.4, 1136.4, 942.8, 792.9, 743.9, 660.3, 601.0, 413.1, 342.2, 196.8, 111.6, 80.2])),
    ("TOTAL", "Total liabilities and equity", d([22535.7, 19629.0, 17100.9, 13945.7, 11094.6, 8980.6, 8248.0, 6805.6, 5701.4, 4625.0, 3978.1, 2732.1, 1648.5, 1028.5])),
]

b.add_balance_sheet_sheet(
    title="Shawbrook Bank Limited — Balance Sheet",
    subtitle="Company/entity basis, £m; FY2012-FY2025 calendar year-ends. Total assets = Total liabilities + "
              "Total equity for every year; Total equity ties exactly to the Statement of Changes in Equity "
              "sheet's own opening/closing balances - zero plug rows. FY2013/FY2012 added per wayfinder ticket "
              "HD-072 (see source note); FY2013 figures use the already-£m-rounded comparative column in the "
              "FY2014 Annual Report rather than independently rounding FY2013's own £000 figures. 'Investment "
              "securities at amortised cost'/'at FVOCI' are a sub-split of the 'Investment securities' row above "
              "(see source note); no government/sovereign-bond vs other-issuer split is disclosed for this bank.",
    rows=balance_sheet_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=68,
    source_height=260,
    unit_suffix=" (£m)",
    years=Y,
)

# ---------------------------------------------------------------
# Profit & Loss (Consolidated statement of profit and loss and other
# comprehensive income) - Group/Consolidated basis (see PRESENTATION NOTE
# above). FY2021 uses the Bank's own FY2021 Annual Report figures (not the
# FY2022 Annual Report's restated comparative, which reclassifies ~£28.5m
# between the two interest-income lines below with no effect on Net
# interest income or any other total).
# ---------------------------------------------------------------
income_statement_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest income calculated using the effective interest rate method", d([1284.6, 1199.3, 946.0, 588.1, 456.3, 399.9, 406.0, 356.0, 313.3, 280.2, 216.9, 156.7, 93.3, 46.9])),
    ("DATA", "Other interest and similar income", d([137.3, 187.7, 197.8, 36.2, -12.6, -8.7, -0.3, 0.8, None, None, None, None, None, None])),
    ("DATA", "Interest expense and similar charges", d([-774.9, -795.9, -567.1, -164.4, -88.9, -114.9, -113.1, -87.2, -75.9, -83.0, -63.8, -54.0, -38.4, -27.4])),
    ("TOTAL", "Net interest income", d([647.0, 591.1, 576.7, 459.9, 354.8, 276.3, 292.6, 269.6, 237.4, 197.2, 153.1, 102.7, 54.9, 19.5])),
    ("DATA", "Operating lease rental income", d([7.3, 8.7, 9.6, 10.1, 10.4, 10.9, 10.3, 10.0, 12.3, 13.5, 14.9, 15.7, 17.1, 15.1])),
    ("DATA", "Depreciation on operating leases", d([-6.2, -7.4, -8.2, -8.7, -8.6, -9.1, -8.6, -7.6, -10.6, -11.3, -12.2, -13.1, -13.8, -12.0])),
    ("DATA", "Net other operating lease income/(expense)", d([0.1, 0.1, 0.1, 0.3, None, -0.1, 0.2, -0.6, None, 0.1, 1.1, 1.1, 1.1, None])),
    ("TOTAL", "Net operating lease income", d([1.2, 1.4, 1.5, 1.7, 1.8, 1.7, 1.9, 1.8, 1.7, 2.3, 3.8, 3.7, 4.4, 3.1])),
    ("DATA", "Fee and commission income", d([17.3, 16.2, 16.9, 14.1, 11.5, 8.6, 9.7, 10.7, 12.3, 15.4, 13.1, 7.6, 0.8, 0.5])),
    ("DATA", "Fee and commission expense", d([-19.6, -17.0, -13.3, -8.8, -7.3, -9.2, -8.7, -9.7, -13.5, -5.7, -2.8, -1.7, 0.0, -0.2])),
    ("TOTAL", "Net fee and commission income/(expense)", d([-2.3, -0.8, 3.6, 5.3, 4.2, -0.6, 1.0, 1.0, -1.2, 9.7, 10.3, 5.9, 0.8, 0.4])),
    ("DATA", "Net gains on derecognition of financial assets measured at amortised cost", d([None, None, None, 7.7, 21.7, 9.4, None, None, None, None, None, None, None, None])),
    ("DATA", "Net gains on structured asset sales", d([34.8, 14.1, None, None, None, None, None, None, None, None, None, None, None, None])),
    ("DATA", "Net (losses)/gains on derivative financial instruments and hedge accounting", d([-2.2, 1.9, 5.1, -0.8, 3.1, -5.0, 2.3, 0.5, 0.2, 0.5, -0.3, -0.1, 0.0, None])),
    ("DATA", "Net gains on loans and advances measured at FVTPL", d([0.3, None, None, None, None, None, None, None, None, None, None, None, None, None])),
    ("DATA", "Net other operating income/(expense)", d([2.5, 1.4, -0.9, 2.4, 0.4, 0.6, -2.6, None, None, None, None, None, None, None])),
    ("TOTAL", "Net operating income", d([681.3, 609.1, 586.0, 476.2, 386.0, 282.4, 295.2, 272.9, 238.1, 209.7, 166.9, 112.2, 60.1, 22.9])),
    ("SECTION", "Operating expenses", {}),
    ("DATA", "Acquisition costs", d([None, None, None, None, None, None, None, None, None, None, None, None, None, -2.1])),
    ("DATA", "Administrative expenses", d([-325.9, -252.2, -225.6, -189.3, -164.2, -131.0, -138.4, -128.8, -113.2, -95.2, -84.0, -58.3, -39.1, -26.9])),
    ("DATA", "Impairment losses on financial assets", d([-83.0, -67.2, -60.1, -47.7, -31.4, -54.9, -29.9, -23.2, -23.3, -24.3, -6.5, -6.7, -3.5, -0.9])),
    ("DATA", "Provisions", d([-0.8, 5.3, -13.1, -0.8, 7.0, -20.3, -4.5, -10.1, -2.1, -1.1, -1.6, -1.1, -0.7, -0.7])),
    ("TOTAL", "Total operating expenses", d([-409.7, -314.1, -298.8, -237.8, -188.6, -206.2, -172.8, -162.1, -138.6, -120.6, -92.1, -66.1, -43.3, -30.7])),
    ("DATA", "Share of results of associates", d([None, None, None, None, None, 0.1, -0.1, -0.5, None, None, None, None, None, None])),
    ("DATA", "Impairment of investment in associate", d([None, None, None, None, None, -2.7, None, None, None, None, None, None, None, None])),
    ("DATA", "Net gain on disposal of subsidiary", d([None, None, None, None, None, None, 0.3, None, None, None, None, None, None, None])),
    ("TOTAL", "Profit before tax", d([271.6, 295.0, 287.2, 238.4, 197.4, 73.6, 122.6, 110.3, 99.5, 89.1, 74.8, 46.1, 16.8, -7.8])),
    ("DATA", "Tax", d([-76.7, -75.2, -74.6, -58.7, -47.9, -15.4, -28.8, -28.3, -25.3, -23.4, -11.8, -10.8, -3.3, 0.4])),
    ("TOTAL", "Profit after tax, attributable to owners", d([194.9, 219.8, 212.6, 179.7, 149.5, 58.2, 93.8, 82.0, 74.2, 65.7, 63.0, 35.3, 13.5, -7.4])),
    ("SECTION", "Other comprehensive income, net of tax (items that may be reclassified subsequently to the statement of profit and loss)", {}),
    ("DATA", "Cash flow hedging reserve - net (losses)/gains from effective portion of changes in fair value", d([-4.4, 17.6, -23.1, 38.4, None, None, None, None, None, None, None, None, None, None])),
    ("DATA", "Cash flow hedging reserve - reclassifications to statement of profit and loss", d([-6.6, -6.2, -6.8, -2.2, None, None, None, None, None, None, None, None, None, None])),
    ("DATA", "Cash flow hedging reserve - related tax", d([3.0, -3.2, 8.0, -9.8, None, None, None, None, None, None, None, None, None, None])),
    ("TOTAL", "Movement in cash flow hedging reserve", d([-8.0, 8.2, -21.9, 26.4, None, None, None, None, None, None, None, None, None, None])),
    ("DATA", "FVOCI reserve - net gains/(losses) from changes in fair value", d([18.3, 35.6, 9.9, -17.1, None, None, None, None, None, None, None, None, None, None])),
    ("DATA", "FVOCI reserve - change in loss allowance", d([1.4, 5.3, 4.3, 2.4, None, None, None, None, None, None, None, None, None, None])),
    ("DATA", "FVOCI reserve - related tax", d([-5.5, -11.0, -3.8, 4.0, None, None, None, None, None, None, None, None, None, None])),
    ("TOTAL", "Movement in fair value through other comprehensive income reserve", d([14.2, 29.9, 10.4, -10.7, None, None, None, None, None, None, None, None, None, None])),
    ("TOTAL", "Other comprehensive income/(expense), net of tax", d([6.2, 38.1, -11.5, 15.7, None, None, None, None, None, None, None, None, 0.0, 0.4])),
    ("TOTAL", "Total comprehensive income, attributable to owners", d([201.1, 257.9, 201.1, 195.4, 149.5, 58.2, 93.8, 82.0, 74.2, 65.7, 63.0, 35.3, 13.5, -6.9])),
]

b.add_income_statement_sheet(
    title="Shawbrook Bank Limited — Profit & Loss",
    subtitle="Group/Consolidated basis, £m; FY2012-FY2025 calendar year-ends. Necessarily Group basis - the "
              "Company takes the s.408 Companies Act 2006 exemption and does not publish its own income "
              "statement (see source note for the Company's own disclosed after-tax profit each year, which "
              "differs from Group 'Profit after tax' shown here). FY2014-FY2021 have no disclosed OCI items at "
              "all - 'Profit after tax' equals 'Total comprehensive income' exactly in each of those years, per "
              "that year's own Annual Report. FY2013/FY2012 do have disclosed OCI (cash flow hedge and "
              "available-for-sale reserve movements), but only as a single combined net-of-tax figure per their "
              "own Annual Reports (not split per-reserve the way FY2022-FY2025 are) - so only the 'Other "
              "comprehensive income/(expense), net of tax' total is populated for those two years, not the "
              "per-reserve breakdown rows above it. 'Acquisition costs' (FY2012 only, £2.1m) is a genuine "
              "one-off line from that year's own Income Statement, not disclosed in any other year.",
    rows=income_statement_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=86,
    source_height=260,
    unit_suffix=" (£m)",
    years=Y,
)

# ---------------------------------------------------------------
# Statement of Changes in Equity - Company basis, chronological. Equity
# reconciliation ladder: built year-by-year, each closing balance ties
# exactly to that year's own Balance Sheet Total equity above and to the
# next year's opening balance - zero undocumented plug rows across all 14
# years, including easy-to-skip categories (cash flow hedging reserve,
# FVOCI reserve, capital securities issue/settlement, capital
# contributions, share-based payments, a FY2025 ordinary share issue).
# FY2012/FY2013 added per wayfinder ticket HD-072; see the source note for
# the Note 4 restatement between FY2012's own closing balance and FY2013's
# own opening balance.
# ---------------------------------------------------------------
EQUITY_HEADERS = [
    "Share capital", "Share premium account", "Capital securities", "Merger reserve",
    "Capital contribution reserve", "Cash flow hedging reserve", "FVOCI reserve",
    "Retained earnings", "Total equity",
]

equity_rows = [
    ("TOTAL", "Balance at 1 January 2012", (37.0, None, None, None, None, 0.0, -0.5, -5.7, 30.9)),
    ("DATA", "Loss for the year", (None, None, None, None, None, None, None, -26.3, -26.3)),
    ("DATA", "Movement in cash flow hedging reserve", (None, None, None, None, None, 0.0, None, None, 0.0)),
    ("DATA", "Movement in fair value through other comprehensive income reserve", (None, None, None, None, None, None, 0.5, None, 0.5)),
    ("DATA", "Capital contribution", (None, None, None, None, 0.2, None, None, None, 0.2)),
    ("DATA", "Issue of ordinary shares", (75.0, None, None, None, None, None, None, None, 75.0)),
    ("TOTAL", "Balance at 31 December 2012 / 1 January 2013", (112.0, None, None, None, 0.2, 0.0, 0.0, -32.0, 80.2)),
    ("DATA", "Effect of restatement (Note 4, FY2013 Annual Report)", (None, None, None, None, None, None, None, 0.5, 0.5)),
    ("TOTAL", "Restated balance at 1 January 2013", (112.0, None, None, None, 0.2, 0.0, 0.0, -31.4, 80.7)),
    ("DATA", "Profit for the year", (None, None, None, None, None, None, None, 13.8, 13.8)),
    ("DATA", "Movement in fair value through other comprehensive income reserve", (None, None, None, None, None, None, 0.0, None, 0.0)),
    ("DATA", "Issue of ordinary shares", (17.0, None, None, None, None, None, None, None, 17.0)),
    ("TOTAL", "Balance at 31 December 2013 / 1 January 2014", (129.0, None, None, None, 0.2, None, None, -17.6, 111.6)),
    ("DATA", "Profit for the year", (None, None, None, None, None, None, None, 38.0, 38.0)),
    ("DATA", "Capital contribution", (None, None, None, None, 0.1, None, None, None, 0.1)),
    ("DATA", "Creation of merger reserve", (None, None, None, 1.6, None, None, None, None, 1.6)),
    ("DATA", "Issue of ordinary shares", (45.5, None, None, None, None, None, None, None, 45.5)),
    ("TOTAL", "Balance at 31 December 2014 / 1 January 2015", (174.5, None, None, 1.6, 0.3, None, None, 20.4, 196.8)),
    ("DATA", "Profit for the year", (None, None, None, None, None, None, None, 63.2, 63.2)),
    ("DATA", "Issue of ordinary shares", (1.0, None, None, None, None, None, None, None, 1.0)),
    ("DATA", "Transfer to share premium account", (None, 81.0, None, None, None, None, None, None, 81.0)),
    ("DATA", "Dividend paid to parent", (None, None, None, None, None, None, None, -4.0, -4.0)),
    ("DATA", "Other movements in reserves", (None, None, None, None, 4.1, None, None, None, 4.1)),
    ("TOTAL", "Balance at 31 December 2015 / 1 January 2016", (175.5, 81.0, None, 1.6, 4.4, None, None, 79.7, 342.2)),
    ("DATA", "Profit for the year", (None, None, None, None, None, None, None, 66.1, 66.1)),
    ("DATA", "Share-based payments", (None, None, None, None, 4.8, None, None, None, 4.8)),
    ("TOTAL", "Balance at 31 December 2016 / 1 January 2017", (175.5, 81.0, None, 1.6, 9.2, None, None, 145.8, 413.1)),
    ("DATA", "Profit for the year", (None, None, None, None, None, None, None, 74.9, 74.9)),
    ("DATA", "Dividend paid to shareholders", (None, None, None, None, None, None, None, -19.5, -19.5)),
    ("DATA", "Issue of capital securities", (None, None, 125.0, None, None, None, None, None, 125.0)),
    ("DATA", "Share-based payments", (None, None, None, None, 7.5, None, None, None, 7.5)),
    ("TOTAL", "Balance at 31 December 2017 / 1 January 2018", (175.5, 81.0, 125.0, 1.6, 16.7, None, None, 201.2, 601.0)),
    ("DATA", "Impact of adopting IFRS 9", (None, None, None, None, None, None, None, -15.7, -15.7)),
    ("TOTAL", "Restated balance at 1 January 2018", (175.5, 81.0, 125.0, 1.6, 16.7, None, None, 185.5, 585.3)),
    ("DATA", "Profit for the year", (None, None, None, None, None, None, None, 82.6, 82.6)),
    ("DATA", "Coupon paid on capital securities (net of tax)", (None, None, None, None, None, None, None, -7.3, -7.3)),
    ("DATA", "Share-based payments", (None, None, None, None, -0.3, None, None, None, -0.3)),
    ("TOTAL", "Balance at 31 December 2018 / 1 January 2019", (175.5, 81.0, 125.0, 1.6, 16.4, None, None, 260.8, 660.3)),
    ("DATA", "Profit for the year", (None, None, None, None, None, None, None, 92.6, 92.6)),
    ("DATA", "Coupon paid on capital securities", (None, None, None, None, None, None, None, -9.8, -9.8)),
    ("DATA", "Share-based payments", (None, None, None, None, 0.8, None, None, None, 0.8)),
    ("TOTAL", "Balance at 31 December 2019 / 1 January 2020", (175.5, 81.0, 125.0, 1.6, 17.2, None, None, 343.6, 743.9)),
    ("DATA", "Profit for the year", (None, None, None, None, None, None, None, 58.3, 58.3)),
    ("DATA", "Coupon paid on capital securities", (None, None, None, None, None, None, None, -9.8, -9.8)),
    ("DATA", "Share-based payments", (None, None, None, None, 0.5, None, None, None, 0.5)),
    ("TOTAL", "Balance at 31 December 2020 / 1 January 2021", (175.5, 81.0, 125.0, 1.6, 17.7, None, None, 392.1, 792.9)),
    ("DATA", "Profit for the year", (None, None, None, None, None, None, None, 153.5, 153.5)),
    ("DATA", "Equity-settled share-based payments", (None, None, None, None, 0.6, None, None, None, 0.6)),
    ("DATA", "Coupon paid on capital securities", (None, None, None, None, None, None, None, -9.8, -9.8)),
    ("DATA", "Capital contribution", (None, None, None, None, 5.6, None, None, None, 5.6)),
    ("TOTAL", "Balance at 31 December 2021 / 1 January 2022", (175.5, 81.0, 125.0, 1.6, 23.9, None, None, 535.8, 942.8)),
    ("DATA", "Profit for the year", (None, None, None, None, None, None, None, 213.0, 213.0)),
    ("DATA", "Movement in fair value through other comprehensive income reserve", (None, None, None, None, None, None, -10.7, None, -10.7)),
    ("DATA", "Equity-settled share-based payments", (None, None, None, None, 0.1, None, None, None, 0.1)),
    ("DATA", "Issue of capital securities", (None, None, 124.0, None, None, None, None, None, 124.0)),
    ("DATA", "Settlement of capital securities", (None, None, -124.0, None, None, None, None, None, -124.0)),
    ("DATA", "Coupon paid on capital securities", (None, None, None, None, None, None, None, -8.8, -8.8)),
    ("TOTAL", "Balance at 31 December 2022 / 1 January 2023", (175.5, 81.0, 125.0, 1.6, 24.0, None, -10.7, 740.0, 1136.4)),
    ("DATA", "Profit for the year", (None, None, None, None, None, None, None, 246.4, 246.4)),
    ("DATA", "Movement in cash flow hedging reserve", (None, None, None, None, None, 0.1, None, None, 0.1)),
    ("DATA", "Movement in fair value through other comprehensive income reserve", (None, None, None, None, None, None, 10.4, None, 10.4)),
    ("DATA", "Equity-settled share-based payments", (None, None, None, None, 0.7, None, None, None, 0.7)),
    ("DATA", "Coupon paid on capital securities", (None, None, None, None, None, None, None, -16.9, -16.9)),
    ("DATA", "Capital contribution", (None, None, None, None, 14.3, None, None, None, 14.3)),
    ("TOTAL", "Balance at 31 December 2023 / 1 January 2024", (175.5, 81.0, 125.0, 1.6, 39.0, 0.1, -0.3, 969.5, 1391.4)),
    ("DATA", "Profit for the year", (None, None, None, None, None, None, None, 203.2, 203.2)),
    ("DATA", "Movement in fair value through other comprehensive income reserve", (None, None, None, None, None, None, 29.9, None, 29.9)),
    ("DATA", "Equity-settled share-based payments", (None, None, None, None, 0.7, None, None, None, 0.7)),
    ("DATA", "Coupon paid on capital securities", (None, None, None, None, None, None, None, -15.1, -15.1)),
    ("TOTAL", "Balance at 31 December 2024 / 1 January 2025", (175.5, 81.0, 125.0, 1.6, 39.7, 0.1, 29.6, 1157.6, 1610.1)),
    ("DATA", "Profit for the year", (None, None, None, None, None, None, None, 189.2, 189.2)),
    ("DATA", "Movement in cash flow hedging reserve", (None, None, None, None, None, 1.2, None, None, 1.2)),
    ("DATA", "Movement in fair value through other comprehensive income reserve", (None, None, None, None, None, None, 14.2, None, 14.2)),
    ("DATA", "Issue of ordinary shares", (50.0, None, None, None, None, None, None, None, 50.0)),
    ("DATA", "Equity-settled share-based payments", (None, None, None, None, None, None, None, 26.1, 26.1)),
    ("DATA", "Coupon paid on capital securities", (None, None, None, None, None, None, None, -15.1, -15.1)),
    ("TOTAL", "Balance at 31 December 2025", (225.5, 81.0, 125.0, 1.6, 39.7, 1.3, 43.8, 1357.8, 1875.7)),
]

b.add_equity_changes_sheet(
    title="Shawbrook Bank Limited — Statement of Changes in Equity",
    subtitle="Company/entity basis, £m, chronological (oldest to newest), FY2012-FY2025. Each year's closing "
              "Total equity ties exactly to that year's own Balance Sheet Total equity and to the next year's "
              "opening balance - zero undocumented plug rows across all 14 years. 'Profit for the year' rows use "
              "the Company's own disclosed profit figure (see the Profit & Loss sheet's source note for why this "
              "differs from Group 'Profit after tax'). The 1 January 2018 IFRS 9 transition impact is shown as "
              "its own restatement row, consistent with the Asset Quality sheet's IAS 39/IFRS 9 basis break; the "
              "1 January 2013 Note 4 restatement (a smaller, £549k accounting-policy break disclosed in the "
              "FY2013 Annual Report, affecting only FY2012's Company retained earnings/Total equity) is shown the "
              "same way, between FY2012's own closing balance and FY2013's own opening balance.",
    headers=EQUITY_HEADERS,
    rows=equity_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=50,
    source_height=260,
)

# ---------------------------------------------------------------
# Sheet: Cash Flow Statement
# ---------------------------------------------------------------
r=[("SECTION","Cash flows from operating activities",{}),
("DATA","Profit before tax",d([252.7,271.6,333.8,284.6,203.8,73.7,121.4,110.9,100.2,89.5,75.2,48.8,19.4,-26.3])),
("DATA","Adjustments for non-cash items and other adjustments",d([182.2,52.4,63.2,67.4,2.6,59.1,23.5,39.2,54.3,51.3,26.2,23.6,14.0,34.9])),
("DATA","(Increase)/decrease in operating assets",d([-2597.8,-1906.0,-2632.5,-2234.4,-1526.5,-369.0,-948.5,-1087.2,-777.9,-775.5,-1040.6,-750.5,-578.2,-376.4])),
("DATA","Increase in operating liabilities",d([2590.0,2209.7,2775.8,2627.5,1449.6,768.7,1191.2,626.2,432.3,460.1,1055.3,966.2,537.1,748.4])),
("DATA","Tax (paid)/recovered",d([-56.5,-85.1,-88.5,-61.9,-48.4,-16.8,-28.6,-26.4,-29.5,-20.5,-13.8,-4.6,-2.2,0.0])),
("TOTAL","Net cash generated from operating activities",d([370.6,542.6,451.8,683.2,81.1,515.7,359.0,-337.3,-220.6,-195.1,102.3,283.5,-10.0,380.5])),
("SECTION","Cash flows from investing activities",{}),
("DATA","Purchase of investment securities",d([-1254.0,-691.3,-308.4,-204.8,-231.9,-176.8,-105.9,-139.7,None,None,None,None,None,None])),
("DATA","Disposals and maturities of investment securities",d([441.1,60.7,194.8,92.9,37.7,None,None,None,None,None,None,None,None,None])),
("DATA","Purchase of property, plant and equipment",d([-0.3,-2.3,-0.7,-0.4,-0.7,-0.8,-3.3,-3.4,-1.6,-0.2,-14.8,-11.0,-11.2,-12.5])),
("DATA","Sale of property, plant and equipment",d([None,None,None,None,None,None,None,None,None,0.2,2.7,2.2,3.8,3.8])),
("DATA","Purchase and development of intangible assets",d([-17.2,-13.3,-13.4,-9.1,-7.1,-7.5,-8.0,-9.8,-9.8,-7.9,-6.1,-3.9,-1.1,None])),
("DATA","Investment in right-of-use asset",d([0,-6.9,0,0,0,None,None,None,None,None,None,None,None,None])),
("DATA","Purchase of subsidiary/shares in associate",d([-64.8,-22.0,-44.7,0,-5.5,None,None,-6.0,None,None,None,-76.3,0.0,-15.3])),
("DATA","Disposal of subsidiary, net of cash disposed",d([None,None,None,None,None,None,28.4,None,None,None,None,None,None,None])),
("TOTAL","Net cash (used by)/generated from investing activities",d([-895.2,-675.1,-172.4,-121.4,-207.5,-185.1,-88.8,-158.9,-11.4,-7.9,-18.2,-89.0,-8.5,-24.0])),
("SECTION","Cash flows from financing activities",{}),
("DATA","Increase/(decrease) in amounts due to banks",d([58.5,-25.5,-101.1,298.0,385.2,-66.1,-147.8,422.1,459.6,107.8,-1.1,16.4,24.6,None])),
("DATA","Issue of debt securities",d([0,0,0,0,0,None,None,None,None,None,None,None,None,None])),
("DATA","Repurchase and redemption of debt securities",d([0,0,0,0,0,None,None,None,None,None,None,None,None,None])),
("DATA","Costs arising on issue of debt securities",d([0,0,0,0,0,None,None,None,None,None,None,None,None,None])),
("DATA","Payment of principal portion of lease liabilities",d([-0.6,-1.5,-1.9,-2.1,-1.8,-1.2,-0.8,None,None,None,None,None,None,None])),
("DATA","Issue of subordinated debt",d([75.0,0,90.0,0,0,75.0,20.0,None,None,None,75.0,None,27.1,None])),
("DATA","Redemption of subordinated debt",d([-76.5,-20.0,0,0,0,-75.0,None,None,None,None,-33.7,None,None,None])),
("DATA","Costs arising on issue of subordinated debt",d([-0.9,0,-1.0,0,0,None,None,None,None,None,None,None,None,None])),
("DATA","Net proceeds from issue of share capital",d([50.0,0,0,0,0,None,None,None,None,None,82.0,45.5,17.0,75.0])),
("DATA","Decrease/(increase) in deemed loan due from structured entities",d([78.2,83.1,-120.7,0,0,None,None,None,None,None,None,None,None,None])),
("DATA","(Decrease)/increase in deemed loan due to structured entities",d([-12.8,119.3,136.2,-269.8,134.6,-18.0,286.2,None,None,None,None,None,None,None])),
("DATA","Increase in deemed loan due from structured entities",d([0,0,0,-93.4,0,None,None,None,None,None,None,None,None,None])),
("DATA","Capital contribution",d([0,0,14.3,0,0,None,None,None,None,None,None,None,None,None])),
("DATA","Coupon paid to holders of capital securities",d([-15.1,-15.1,-16.9,-8.8,-9.8,-9.8,-9.8,-9.8,None,None,None,None,None,None])),
("DATA","Payment of subordinated debt interest",d([None,None,None,None,None,None,None,-6.4,-6.4,-5.3,None,None,None,None])),
("DATA","Net proceeds from issue of capital securities",d([None,None,None,None,None,None,None,None,125.0,None,None,None,None,None])),
("DATA","Dividends paid to parent/shareholders",d([None,None,None,None,None,None,None,None,-19.5,None,-4.0,None,None,None])),
("DATA","Repayment of Centric third party funding",d([None,None,None,None,None,None,None,None,None,None,None,-138.2,None,None])),
("DATA","Repayment of SAF third party funding",d([None,None,None,None,None,None,None,None,None,None,None,None,None,-325.1])),
("TOTAL","Net cash (used by)/generated from financing activities",d([155.8,140.3,-1.1,-76.1,508.2,-95.1,147.8,405.9,558.7,102.5,118.2,-76.3,68.7,-250.1])),
("TOTAL","Net (decrease)/increase in cash and cash equivalents",d([-368.8,7.8,278.3,485.7,381.8,235.5,418.0,-90.3,326.7,-100.5,202.7,118.2,50.2,106.4])),
("DATA","Cash and cash equivalents as at 1 January",d([2493.5,2485.7,2207.4,1721.7,1339.9,1104.4,686.4,776.7,450.0,550.5,347.8,229.6,180.1,73.7])),
("TOTAL","Cash and cash equivalents as at 31 December",d([2124.7,2493.5,2485.7,2207.4,1721.7,1339.9,1104.4,686.4,776.7,450.0,550.5,347.8,230.3,180.1]))]
b.add_cash_flow_sheet(title="Shawbrook Bank Limited — Company Cash Flow Statement",subtitle="Company/entity basis, £m; FY2012-FY2025 calendar year-ends. FY2012-FY2017 granular operating-asset/liability line items are condensed into the same 2-line 'increase/decrease' format used from FY2018 onward; each year's condensed subtotal ties exactly to that year's own disclosed net change. FY2012's own closing balance ties exactly to FY2013's own opening balance (both £180.1m, per each year's own Annual Report). FY2013's own closing balance (£230.3m) does NOT tie to FY2014's opening balance already shown here (£229.6m) - a genuine, sourced ~£0.7m break from a 'cash and cash equivalents' definition change first introduced in the FY2014 Annual Report (see source note), not an omitted plug row.",rows=r,sources_text=cf,first_col_width=70,source_height=230,unit_suffix=" (£m)",years=Y)

# ---------------------------------------------------------------
# Asset Quality - loans and advances to customers AT AMORTISED COST ONLY
# (a narrower, but the only comparable, basis across all 5 years - a wider
# "Total loans and advances to customers" table including FVOCI-measured
# loans only appears in the FY2023-FY2025 Annual Reports; using the
# amortised-cost table throughout keeps years on a consistent footing).
# Each year's own Annual Report figures used (not later restated
# comparatives). Note this narrower total does NOT tie to the Balance
# Sheet's "Loans and advances to customers" line (which is Total loans
# across all measurement categories including FVOCI) - a genuine,
# documented cross-statement scope difference, not forced to tie.
# ---------------------------------------------------------------
asset_quality_rows = [
    ("SECTION", "Loans and advances to customers at amortised cost, by IFRS 9 stage (£m)", {}),
    ("DATA", "Gross loans - Stage 1", d([12235.5, 10276.9, 9281.0, 8279.5, 7315.7, 5410.9, 5847.8, 4922.0, None, None, None, None])),
    ("DATA", "Gross loans - Stage 2", d([1064.7, 1023.3, 997.5, 897.3, 831.2, 1552.3, 716.6, 871.6, None, None, None, None])),
    ("DATA", "Gross loans - Stage 3", d([474.7, 506.8, 352.1, 287.9, 221.6, 156.3, 125.6, 121.2, None, None, None, None])),
    ("DATA", "Gross loans - POCI (purchased or originated credit-impaired)", d([40.3, None, None, None, None, None, None, None, None, None, None, None])),
    ("TOTAL", "Gross carrying amount", d([13815.2, 11807.0, 10630.6, 9464.7, 8368.5, 7119.5, 6690.0, 5914.8, None, None, None, None])),
    ("DATA", "Loss allowance - Stage 1", d([-59.8, -48.0, -47.3, -43.2, -25.8, -29.0, -20.6, -23.5, None, None, None, None])),
    ("DATA", "Loss allowance - Stage 2", d([-31.5, -33.4, -29.0, -22.6, -15.2, -34.4, -14.2, -20.7, None, None, None, None])),
    ("DATA", "Loss allowance - Stage 3", d([-93.3, -78.0, -53.9, -46.0, -35.0, -28.9, -26.3, -23.6, None, None, None, None])),
    ("DATA", "Loss allowance - POCI", d([-4.8, None, None, None, None, None, None, None, None, None, None, None])),
    ("TOTAL", "Loss allowance", d([-189.4, -159.4, -130.2, -111.8, -76.0, -92.3, -61.1, -67.8, None, None, None, None])),
    ("TOTAL", "Net carrying amount", d([13625.8, 11647.6, 10500.4, 9352.9, 8292.5, 7027.2, 6628.9, 5847.0, None, None, None, None])),
    ("SECTION", "Derived ratios (IFRS 9 basis)", {}),
    ("DATA", "NPL ratio (Stage 3 gross / Total gross loans)", d(["3.44%", "4.29%", "3.31%", "3.04%", "2.65%", "2.20%", "1.88%", "2.05%", None, None, None, None])),
    ("DATA", "Stage 3 coverage ratio (Stage 3 loss allowance / Stage 3 gross)", d(["19.65%", "15.39%", "15.31%", "15.98%", "15.79%", "18.49%", "20.94%", "19.47%", None, None, None, None])),
    ("SECTION", "Loans and advances to customers, product basis (pre-IFRS 9 / IAS 39; £m) - superseded by the IFRS 9 stage basis above from 1 January 2018", {}),
    ("DATA", "Gross carrying amount (product basis)", d([None, None, None, None, None, None, None, None, 4830.8, 4074.8, 3332.6, 2295.9])),
    ("DATA", "Loss allowance (product basis)", d([None, None, None, None, None, None, None, None, -31.5, -24.4, -13.5, -11.1])),
    ("TOTAL", "Net carrying amount (product basis)", d([None, None, None, None, None, None, None, None, 4799.3, 4050.4, 3319.1, 2284.7])),
]

b.add_asset_quality_sheet(
    title="Shawbrook Bank Limited — Asset Quality",
    subtitle="Group basis, £m. Loans and advances to customers at amortised cost only - see source note for why "
              "this doesn't tie exactly to the Balance Sheet's broader 'Loans and advances to customers' line. "
              "FY2021-FY2024 include POCI loans within the Stage 3 total (each year's own report's footnote "
              "gives the POCI split; FY2025 is the first year POCI is broken out as its own row). A genuine "
              "methodology break occurs at 1 January 2018 (IFRS 9 adoption): FY2014-FY2017 use a pre-IFRS 9 "
              "product-based (loan receivables/finance lease receivables/instalment credit receivables, IAS 39) "
              "gross/allowance/net breakdown shown in its own section below, not comparable to the IFRS 9 "
              "stage-based rows above, which are blank for those years.",
    rows=asset_quality_rows,
    sources_text=(
        "Sources - Shawbrook Bank Limited, 'loans and advances to customers at amortised cost' stage analysis:\n"
        f"FY2025: Annual Report and Accounts 2025, p.54 - {AR['FY2025']}\n"
        f"FY2024: Annual Report and Accounts 2024, p.52 - {AR['FY2024']}\n"
        f"FY2023: Annual Report and Accounts 2023, p.52 (independently cross-checked against the FY2023 "
        f"comparative column in Annual Report and Accounts 2024, p.52, which agrees exactly) - {AR['FY2023']}\n"
        f"FY2022: Annual Report and Accounts 2022, p.49 (independently cross-checked against the FY2022 "
        f"restated comparative in Annual Report and Accounts 2023, p.52, which agrees on Total figures) - "
        f"{AR['FY2022']}\n"
        f"FY2021: Annual Report and Accounts 2021, p.56-57 (independently cross-checked against the FY2021 "
        f"comparative column in Annual Report and Accounts 2022, p.48, which agrees exactly) - {AR['FY2021']}\n"
        f"FY2020: Annual Report and Accounts 2020, IFRS 9 stage analysis by segment, p.44-45 - {AR['FY2020']}\n"
        f"FY2019: Annual Report and Accounts 2019, IFRS 9 stage analysis by segment, p.44 - {AR['FY2019']}\n"
        f"FY2018 (Stage basis): Annual Report and Accounts 2019, FY2018 comparative column in the IFRS 9 stage "
        f"analysis by segment, p.44 - {AR['FY2019']}. FY2018's own Annual Report (Companies House filing) does "
        f"not itself break out this stage analysis at Bank level in a form usable here; using the following "
        f"year's disclosed comparative (same methodology, no restatement) avoids leaving a first-transition-year "
        f"gap.\n"
        f"FY2017 product-basis: Annual Report and Accounts 2017 (Companies House filing), Note 12, p.55-56 - "
        f"{AR['FY2017']}\n"
        f"FY2016 product-basis: Annual Report and Accounts 2016 (Companies House filing), impairment allowance "
        f"movement note, p.44-45 - {AR['FY2016']}\n"
        f"FY2015 product-basis: Annual Report and Accounts 2015 (Companies House filing), Note 13/14, p.68-71 - "
        f"{AR['FY2015']}\n"
        f"FY2014 product-basis: Annual Report and Accounts 2014 (Companies House filing), loans and advances to "
        f"customers note - {AR['FY2014']}\n\n"
        + note
    ),
    first_col_width=64,
    source_height=240,
    unit_suffix="",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
ps="Sources - Bank-specific Pillar 3: FY2021 Appendix 4 pp.54-58; FY2022 Bank tables 17 and KM1 pp.18-21; FY2023 Bank tables 14-15 pp.19-22; FY2024 Bank tables 11-12 pp.16-19; FY2020/FY2019 'Key risk metrics for Shawbrook Bank Limited' table, Appendix 1 (Pillar 3 Disclosures 2020); FY2018/FY2017/FY2016 Appendix 1 capital-composition tables (no Bank RWA breakdown disclosed those 3 years - see note); FY2015 Appendix 1 pp.33-34; FY2014 Appendix (Disclosures for Shawbrook Bank Limited) pp.39-40.\n"+"\n".join(f"{y}: {P3[y]}" for y in Y if y in P3)+"\nLCR SHEET ONLY - the point-in-time rows on that sheet are NOT from a Pillar 3 document. Their source is "
"Shawbrook Bank Limited's own Annual Report and Accounts 2025: the 'Financial position metrics' KPI table on "
"printed p.10 ('Liquidity coverage ratio (%) 147.2 / 176.0'), and the Risk Report's liquidity section on "
"printed p.87, which prints the build-up as Liquidity buffer £2,975.8m (2024: £3,161.5m), Total net cash "
"outflows £2,022.0m (2024: £1,796.1m), LCR 147.2% (2024: 176.0%) - "+AR['FY2025']+" . Read on 2026-09-18 from "
"the text layer of that document. The FY2024 point-in-time column is the Annual Report's own comparative, "
"labelled as such, and is carried only to make the basis gap against the KM1 row visible.\n"
"Blank cells mean not publicly disclosed/not applicable; FY2025 Group-only data is not used as a Bank proxy. FY2013/FY2012 are out of scope for this workbook's Pillar 3 sheets (see wayfinder ticket HD-072) and are simply blank, same as any other undisclosed year.\n\n"+LINK_PROVENANCE
def m(name,unit,data,n=None): b.add_metric_sheet(name,unit,[(name,data)],ps,note=n,first_col_width=54,source_height=280)
AR2025_BANK_BASIS = (
    " FY2025 is sourced from Shawbrook Bank Limited's OWN Annual Report and Accounts 2025 (Bank entity, "
    "Companies House 00388466), NOT from a Pillar 3 disclosure: the FY2025 Pillar 3 publication covers "
    "Shawbrook Group plc (Company No 07240248) on a consolidated basis only - its contents list has a single "
    "reporting section, 'Disclosures for Shawbrook Group plc (the Group)', with no Bank-level section - so it "
    "is not substituted here. Every FY2024 comparative in the Annual Report's own capital tables reproduces "
    "this workbook's existing Bank-level FY2024 figures exactly (CET1 1,297.0; Total Tier 1 1,422.0; Total "
    "regulatory capital 1,586.2; CET1 ratio 13.0%; Tier 1 ratio 14.3%; total capital ratio 15.9%; RWAs "
    "9,952.2; leverage 8.1%; NSFR 134.5%), confirming the two are the same basis. Capital and leverage "
    "metrics are on the transitional (IFRS 9 transitional arrangements applied) basis, consistent with the "
    "earlier years here; the IFRS 9 transitional add-back had run off to nil by FY2025 (FY2024: 10.4).\n"
    "KNOWN INTERNAL INCONSISTENCY IN THE SOURCE (FY2025 only, reproduced rather than silently smoothed): the "
    "Annual Report and Accounts 2025 states FY2025 CET1 capital twice, and the two figures differ by £2.6m. "
    "The audited 'Regulatory capital' composition table on p.90 builds CET1 up line by line to 1,495.7 (share "
    "capital 225.5 + share premium 81.0 + capital contribution reserve 39.7 + merger reserve 1.6 + retained "
    "earnings 1,323.3 - intangibles 140.1 - deferred tax 23.5 - AOCI 0.5 - prudent valuation adjustment 4.4 - "
    "1,250%-risk-weight securitisation position 6.9 = 1,495.7, which foots exactly, as does the same table's "
    "FY2024 column to 1,297.0), and this is the figure used here. The 'IFRS 9 transitional arrangements impact "
    "analysis' table on p.92 instead shows 1,493.1 (and correspondingly Total Tier 1 1,618.1, total regulatory "
    "capital 1,781.9); the two tables agree exactly for FY2024, so the gap is new in FY2025 and the report "
    "offers no reconciliation of it. The ratios recorded here (CET1 12.4%, Tier 1 13.5%, total capital 14.9%, "
    "leverage 7.8%) are the Bank's own headline figures, printed in the financial highlights, the Key "
    "Performance Indicators table (p.9) and the p.92 table alike; the separate 'Capital ratios' and 'Leverage "
    "ratio' tables on p.91 instead print CET1 12.5% and leverage 7.9%, which is what 1,495.7 / 12,000.4 and "
    "1,620.7 / 20,628.1 actually compute to. CONSEQUENCE: the FY2025 CET1 Capital figure here (1,495.7) does "
    "not divide into the FY2025 Total RWAs figure (12,000.4) to give the FY2025 CET1 Ratio shown here (12.4%) "
    "- it gives 12.5%. That is a genuine, documented inconsistency inside the Bank's own report, not a "
    "transcription error in this workbook, and it affects FY2025 alone. It should resolve when a Bank-level "
    "UK KM1 template is next published."
)

# ---------------------------------------------------------------
# KM1 Key Metrics - Shawbrook Bank Limited's OWN published UK KM1 template.
#
# ENTITY: every edition from FY2022 onward is a joint Shawbrook Group plc /
# Shawbrook Bank Limited document that prints the template TWICE - once for
# the Group in section 2 and once for the BANK in the "Disclosures for
# Shawbrook Bank Limited" section. Only the BANK table is reproduced here,
# matching every other Pillar 3 sheet in this workbook. The two differ
# materially (FY2024 Group RWEA 10,146.4 against the Bank's 9,952.2).
#
# YEARS: FY2024/FY2023/FY2022 come from their own editions. FY2021 is filled
# from the FY2022 edition's 31 Dec 2021 comparative column, which is the only
# place a Bank-level KM1 for that date is printed at all (the FY2021 edition
# pre-dates the template). FY2025 is BLANK on entity grounds: the FY2025
# Pillar 3 is Shawbrook Group plc-only, with no Bank section to reproduce -
# the same reason FY2025 is blank on the RWA Breakdown sheet. FY2020 and
# earlier print a short bespoke "Key risk metrics" table that fails the
# row-set test (no SREP block, no buffer block, no LCR/NSFR rows).
#
# FY2022 IS THE BANK'S OWN ORIGINALLY-PUBLISHED COLUMN, NOT THE RESTATEMENT.
# The FY2023 edition restated 31 Dec 2022 RWEA upward by £80.6m; the metric
# sheets below carry the restated figures and this sheet carries what the
# FY2022 edition itself printed. Both are correct, and the gap is the
# restatement - see the sheet note.
# ---------------------------------------------------------------
km1_rows = [
    ("SECTION", "Available own funds (amounts)", {}),
    ("DATA", "1    Common Equity Tier 1 (CET1) capital (£m)",
     {"FY2024": 1297.0, "FY2023": 1122.7, "FY2022": 951.5, "FY2021": 775.7}),
    ("DATA", "2    Tier 1 capital (£m)",
     {"FY2024": 1422.0, "FY2023": 1247.7, "FY2022": 1076.5, "FY2021": 900.7}),
    ("DATA", "3    Total capital (£m)",
     {"FY2024": 1586.2, "FY2023": 1431.7, "FY2022": 1171.5, "FY2021": 995.7}),
    ("SECTION", "Risk-weighted exposure amounts", {}),
    ("DATA", "4    Total risk-weighted exposure amount (£m)",
     {"FY2024": 9952.2, "FY2023": 8707.3, "FY2022": 7385.7, "FY2021": 6134.0}),
    ("SECTION", "Capital ratios (as a percentage of risk-weighted exposure amount)", {}),
    ("DATA", "5    Common Equity Tier 1 ratio (%)",
     {"FY2024": "13.0", "FY2023": "12.9%", "FY2022": "12.9%", "FY2021": "12.6%"}),
    ("DATA", "6    Tier 1 ratio (%)",
     {"FY2024": "14.3", "FY2023": "14.3%", "FY2022": "14.6%", "FY2021": "14.7%"}),
    ("DATA", "7    Total capital ratio (%)",
     {"FY2024": "15.9", "FY2023": "16.4%", "FY2022": "15.9%", "FY2021": "16.2%"}),
    ("SECTION", "Additional own funds requirements based on SREP (as a percentage of risk-weighted exposure amount)", {}),
    ("DATA", "UK 7a    Additional CET1 SREP requirements (%)",
     {"FY2024": "0.7", "FY2023": "0.6%", "FY2022": "0.6%", "FY2021": "0.6%"}),
    ("DATA", "UK 7b    Additional AT1 SREP requirements (%)",
     {"FY2024": "0.2", "FY2023": "0.2%", "FY2022": "0.2%", "FY2021": "0.2%"}),
    ("DATA", "UK 7c    Additional T2 SREP requirements (%)",
     {"FY2024": "0.3", "FY2023": "0.3%", "FY2022": "0.3%", "FY2021": "0.3%"}),
    ("DATA", "UK 7d    Total SREP own funds requirements (%)",
     {"FY2024": "9.2", "FY2023": "9.1%", "FY2022": "9.1%", "FY2021": "9.1%"}),
    ("SECTION", "Combined buffer requirement (as a percentage of risk-weighted exposure amount)", {}),
    ("DATA", "8    Capital conservation buffer (%)",
     {"FY2024": "2.5", "FY2023": "2.5%", "FY2022": "2.5%", "FY2021": "2.5%"}),
    # FY2021 carries a literal dash, read 2026-09-18 from the BANK table (not the
    # Group one) at printed page 19 of the Pillar 3 Disclosures 2022, column (e),
    # 31 Dec 2021. The Bank had no institution-specific countercyclical buffer at
    # that date and said so with a dash; that is a statement, not a missing figure.
    ("DATA", "9    Institution specific countercyclical capital buffer (%)",
     {"FY2024": "2.0", "FY2023": "2.0%", "FY2022": "1.0%", "FY2021": "-"}),
    ("DATA", "11    Combined buffer requirement (%)",
     {"FY2024": "4.5", "FY2023": "4.5%", "FY2022": "3.5%", "FY2021": "2.5%"}),
    ("DATA", "UK 11a    Overall capital requirements (%)",
     {"FY2024": "13.7", "FY2023": "13.6%", "FY2022": "12.6%", "FY2021": "11.6%"}),
    ("DATA", "12    CET1 available after meeting the total SREP own funds requirements (%)",
     {"FY2024": "7.8", "FY2023": "8.4%", "FY2022": "7.8%", "FY2021": "7.5%"}),
    ("SECTION", "Leverage ratio", {}),
    ("DATA", "13    Total exposure measure excluding claims on central banks (£m)",
     {"FY2024": 17506.0, "FY2023": 15171.9, "FY2022": 12227.1}),
    ("DATA", "14    Leverage ratio excluding claims on central banks (%)",
     {"FY2024": "8.1", "FY2023": "8.2%", "FY2022": "8.8%"}),
    ("DATA", "Total exposure measure (pre-1 Jan 2022) (£m)", {"FY2021": 11263.4}),
    ("DATA", "Leverage ratio (pre-1 Jan 2022) (%)", {"FY2021": "8.0%"}),
    ("SECTION", "Liquidity coverage ratio", {}),
    ("DATA", "15    Total high-quality liquid assets (HQLA) (Weighted value -average) (£m)",
     {"FY2024": 3480.5, "FY2023": 2738.6, "FY2022": 2162.5}),
    ("DATA", "UK 16a    Cash outflows - Total weighted value (£m)",
     {"FY2024": 1556.3, "FY2023": 1091.4, "FY2022": 881.3}),
    ("DATA", "UK 16b    Cash inflows - Total weighted value (£m)",
     {"FY2024": 242.9, "FY2023": 210.4, "FY2022": 136.5}),
    ("DATA", "16    Total net cash outflows (adjusted value) (£m)",
     {"FY2024": 1313.4, "FY2023": 881.0, "FY2022": 744.8}),
    ("DATA", "17    Liquidity coverage ratio (%)",
     {"FY2024": "265.0", "FY2023": "310.9%", "FY2022": "290.3%"}),
    ("SECTION", "Net Stable Funding Ratio", {}),
    ("DATA", "18    Total available stable funding (£m)", {"FY2024": 17182.0, "FY2023": 15956.1}),
    ("DATA", "19    Total required stable funding (£m)", {"FY2024": 12770.5, "FY2023": 10945.9}),
    ("DATA", "20    NSFR ratio (%)", {"FY2024": "134.5", "FY2023": "145.8%"}),
]

KM1_SOURCES = (
    "Sources - Shawbrook Bank Limited's own UK KM1 key-metrics template, BANK column, £m and % as printed:\n"
    f"FY2024: Pillar 3 Disclosures 2024, 'Disclosures for Shawbrook Bank Limited (the Bank)', Table 12: UK KM1 - "
    f"Key metrics table, BANK column (a), pp.16-17 - {P3['FY2024']}\n"
    f"FY2023: Pillar 3 Disclosures 2023, same section, Table 15: UK KM1 - Key metrics table, BANK column (a), "
    f"pp.19-20 - {P3['FY2023']}\n"
    f"FY2022: Pillar 3 Disclosures 2022, same section, Table 15: UK KM1 - Key metrics table, BANK column (a), "
    f"pp.18-19 - {P3['FY2022']}\n"
    f"FY2021: the FY2022 edition's 31 Dec 2021 comparative column (e) of that same Table 15, pp.18-19 - "
    f"{P3['FY2022']}\n\n"
    "WHICH TABLE WAS READ, AND HOW IT WAS IDENTIFIED. The Pillar 3 Disclosures 2022 is a JOINT document - its "
    "cover and every page footer read 'Shawbrook Group plc and Shawbrook Bank Limited' - and it prints the UK "
    "KM1 template TWICE, once per entity. This workbook is Shawbrook Bank Limited, so every figure above comes "
    "from the BANK table at printed pages 18-19, never from the Group table at printed pages 7-8. The Bank "
    "table was identified by three independent markers, not by position: its page heading reads 'Disclosures "
    "for Shawbrook Bank Limited'; its own stub column is captioned 'BANK' where the earlier table is captioned "
    "'GROUP'; and its notes refer the reader back to the Group's sections ('Information relating to the ICAAP "
    "is as disclosed for the Group in Section 3.1'), which only the Bank table does. The two tables are "
    "genuinely different and a mix-up would be silent: at 31 Dec 2022 the Bank prints row 12 as 7.8%, row 13 "
    "as 12,227.1 and row 17 as 290.3%, where the Group prints 7.7%, 12,202.7 and 290.4%.\n\n"
    "ROW 9 FY2021 IS A PRINTED DASH, NOT A GAP. Both entity tables print an en-dash at row 9 in the 31 Dec "
    "2021 column - the Group table's Table 3 restates the same fact in words, showing '-' for the "
    "countercyclical capital buffer at 31 Dec 2021 against 1.00% at 31 Dec 2022 - so the reading is "
    "independently corroborated, though the figure carried here is the Bank table's. The cell holds a literal "
    "'-' because the Bank published one: it means the buffer did not apply to it at that date, which is a "
    "different statement from never having disclosed the row.\n\n"
    "FY2021 ROWS 13-17 ARE BLANK BECAUSE THE BANK PRINTED 'N/a', WHICH IS ITS OWN WORD AND IS NOT CONVERTED "
    "TO A DASH. The FY2022 edition's 31 Dec 2021 column marks rows 13, 14, 15, UK 16a, UK 16b, 16 and 17 as "
    "'N/a' and explains why in its own footnotes: the leverage rows changed basis on 1 Jan 2022 under PS21/21 "
    "and 'prior year comparatives have not been restated', with the pre-1 Jan 2022 leverage figures given "
    "instead on the two extra rows this sheet reproduces separately; and the LCR rows are 'a new disclosure "
    "requirement and accordingly comparative information is not provided'. Rows 18-20 are absent for both "
    "years because that edition states the NSFR 'is not applicable until 1 January 2023'.\n\n"
    "LATEST-EDITION CHECK, 2026-09-17: shawbrook.co.uk's own results centre "
    "(/about-us/investors/results-centre/) was read directly (HTTP 200). The newest Pillar 3 document is "
    "Pillar 3 Disclosures 2025, which this workbook already holds. Checked, none newer.\n\n"
    "WHY FY2025 IS BLANK (ENTITY, NOT ABSENCE): the Pillar 3 Disclosures 2025 is a Shawbrook Group plc "
    "document. Its contents list carries a single reporting section, 'Disclosures for Shawbrook Group plc (the "
    "Group)', and it prints Template 1: UK KM1 once, for the Group. There is no 'Disclosures for Shawbrook Bank "
    "Limited' section in it, so there is no Bank-level KM1 for 31 December 2025 to reproduce. The Group's table "
    "is a different entity and has NOT been substituted - the same convention this workbook applies on the RWA "
    "Breakdown and LCR sheets. The Bank's own Annual Report and Accounts 2025 states capital and leverage "
    "figures but does not print the template.\n\n"
    "WHY FY2021 IS FILLED FROM A LATER EDITION: the Pillar 3 Disclosures 2021 pre-dates the UK KM1 template "
    "(the template first appears in Shawbrook's FY2022 edition). The FY2022 edition prints a full 31 Dec 2021 "
    "comparative column for the Bank, which is the only Bank-level KM1 ever published for that date, so the "
    "FY2021 column here is that comparative. It is labelled as such rather than shown as an own-edition column.\n\n"
    "FY2022 IS THE ORIGINALLY-PUBLISHED COLUMN AND DIFFERS FROM THE METRIC SHEETS BY THE RESTATEMENT. The "
    "FY2022 edition printed 31 Dec 2022 RWEA as 7,385.7 and ratios of 12.9% / 14.6% / 15.9%. The FY2023 edition "
    "restated that date - its footnote 1 reads 'risk-weighted assets have increased by £80.6 million from "
    "£7,385.8 million to £7,466.4 million' following a credit valuation adjustment and counterparty credit risk "
    "adjustment on the Bank's structured entities' interest rate swap derivatives - giving 7,466.4 and 12.7% / "
    "14.4% / 15.7%, and restating the leverage exposure measure from 12,227.1 to 12,264.7. This sheet reproduces "
    "the FY2022 edition's own column. The metric sheets in this workbook are NOT uniform about that restatement, "
    "and the split is recorded here rather than smoothed over: the Total RWAs sheet carries the restated 7,466.4 "
    "and the CET1 Ratio sheet the restated 12.7%, while the Tier 1 Ratio sheet carries 14.6% and the Total "
    "Capital Ratio sheet 15.9%, which are the FY2022 edition's ORIGINAL ratios (the restated pair would be 14.4% "
    "and 15.7%). So this sheet disagrees with the Total RWAs and CET1 Ratio sheets for FY2022 by exactly the "
    "restatement, and AGREES with the Tier 1 Ratio and Total Capital Ratio sheets, which are on the original "
    "basis this sheet uses. That inconsistency between the four metric sheets is a pre-existing feature of this "
    "workbook, identified 18 September 2026; no figure has been altered to make the two sides agree, because "
    "which basis those sheets should carry is a question for the source documents and not for this sheet. "
    "Note also that the FY2023 edition's footnote gives the pre-restatement figure as "
    "£7,385.8m while the FY2022 edition itself printed 7,385.7 in both its KM1 (Table 15) and its RWA table "
    "(Table 14, row 29) - a 0.1 discrepancy introduced by the later edition, reproduced here as published.\n\n"
    "ROWS THE BANK DID NOT PRINT ARE BLANK, NOT ZERO:\n"
    "- FY2022 rows 18-20 (NSFR): the FY2022 edition prints a note in place of the rows - 'Disclosures for the "
    "net stable funding ratio (Rows 18-20 of the template) are not applicable until 1 January 2023, as set out "
    "by the PRA in PS22/21 Implementation of Basel standards: Final rules'. The FY2023 edition does print 31 Dec "
    "2022 comparatives for those three rows (12,972.3 / 8,890.8 / 145.9%), but a row the year's own edition "
    "never printed is left blank here rather than back-filled from a later comparative.\n"
    "- FY2021 row 9 (countercyclical buffer): printed as an en-dash '–' in the FY2022 edition's 2021 column, so "
    "the cell is blank. A dash is not a zero.\n"
    "- FY2021 rows 13-17: printed as 'N/a' in the FY2022 edition's 2021 column, because the UK leverage "
    "framework's 'excluding claims on central banks' basis and the averaged LCR build-up both begin on "
    "1 January 2022. The two unnumbered rows beneath row 14 are the FY2022 edition's own pre-1 Jan 2022 "
    "leverage captions, which it prints for 2021 alongside 'N/a' in rows 13/14 - the basis break is kept as two "
    "separate captions and the series is not merged.\n\n"
    "PRINTED-FORM NOTE: the FY2024 edition prints every percentage WITHOUT a '%' glyph (its column reads '13.0' "
    "under the caption 'Common Equity Tier 1 ratio (%)'), while the FY2023 and FY2022 editions print '12.9%' "
    "with the glyph. Both are reproduced as published, which is why one row can show '13.0' beside '12.9%'.\n\n"
    "FY2020 AND EARLIER - THE TEMPLATE IS NOT USED. Those editions do carry a Bank-level appendix ('Key risk "
    "metrics for Shawbrook Bank Limited', Appendix 1), but it is a short bespoke table: capital amounts, RWAs "
    "and ratios only, with no SREP block (UK 7a-7d), no combined buffer block, no leverage exposure measure and "
    "no LCR or NSFR rows. On this project's row-set test that is a different and shorter table, not an "
    "unnumbered template, so those years are blank here rather than mapped onto template row numbers. The "
    "figures those tables do disclose are on the individual metric sheets in this workbook."
)

b.add_km1_sheet(
    title="Shawbrook Bank Limited — KM1 Key Metrics",
    subtitle="The Bank's own published UK KM1 template, reproduced whole in Shawbrook's row order with its own "
             "row numbers, labels and printed precision. BANK column only - every edition prints the template "
             "twice, once for Shawbrook Group plc and once for Shawbrook Bank Limited, and the Group table is "
             "not substituted anywhere. Amounts in £m, ratios as printed. FY2024-FY2022 come from their own "
             "editions; FY2021 is the FY2022 edition's comparative column (no Bank KM1 was published for that "
             "date in any other document). FY2025 is shown but empty because the FY2025 Pillar 3 is Group-only "
             "- an entity finding, not an absence. FY2020 and earlier are not shown at all: they pre-date the "
             "template, so those columns are omitted rather than printed empty - see the source note.",
    rows=km1_rows,
    sources_text=KM1_SOURCES,
    first_col_width=72,
    source_height=520,
    years=["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"],
)

m("CET1 Capital","£m",d([1495.7,1297.0,1122.7,951.5,775.7,663.8,594.4,514.4,431.4,367.6,308.6,168.4]),AR2025_BANK_BASIS.strip())
m("CET1 Ratio","%",d(["12.4%","13.0%","12.9%","12.7%","12.6%","12.6%","12.0%","12.2%","12.9%","13.2%","14.2%","11.5%"]),AR2025_BANK_BASIS+" FY2015/FY2014 CET1 ratio equals the Bank's disclosed Tier 1 capital ratio, since CET1 = Tier 1 capital in both years (no Additional Tier 1 issued until FY2017). "+BANK_ARA_CAPITAL_NOTE)
m("Tier 1 Capital","£m",d([1620.7,1422.0,1247.7,1076.5,900.7,788.8,719.4,639.4,556.4,367.6,308.6,168.4]),AR2025_BANK_BASIS.strip())
m("Tier 1 Ratio","%",d(["13.5%","14.3%","14.3%","14.6%","14.7%","15.0%","14.5%","15.2%","16.7%","13.2%","14.2%","11.5%"]),AR2025_BANK_BASIS+" FY2016's 13.2% IS A COMPARATIVE, not a figure from its own year's edition: the Annual Report and Accounts 2016 prints no Tier 1 ratio at all (its ratio table has only CET1, Total capital and Leverage rows), so FY2016 here is the Company 2016 'Total Tier 1 capital ratio' column of the Annual Report and Accounts 2017, printed p.93. FY2018 and FY2017 are each from their own year's own edition. "+BANK_ARA_CAPITAL_NOTE)
m("Total Capital","£m",d([1784.5,1586.2,1431.7,1171.5,995.7,883.8,814.3,714.4,642.4,452.4,388.2,202.2]),AR2025_BANK_BASIS.strip())
m("Total Capital Ratio","%",d(["14.9%","15.9%","16.4%","15.9%","16.2%","16.8%","16.4%","16.9%","19.3%","16.3%","17.9%","13.8%"]),AR2025_BANK_BASIS+" "+BANK_ARA_CAPITAL_NOTE)
m("Total RWAs","£m",d([12000.4,9952.2,8707.3,7466.4,6134.0,5268.4,4972.5,4218.1,3335.4,2778.6,2175.9,1460.0]),AR2025_BANK_BASIS+" FY2019 uses the comparative column in the FY2020 Pillar 3 disclosure (the first year with a full Bank RWA-by-category table); FY2019's own document did not disclose this breakdown. FY2015 is the 'Total risk exposure amount' stated directly in that year's Bank countercyclical-buffer table; FY2014 alone is derived from the Bank's own disclosed Pillar 1 capital requirement (Credit risk + Operational risk) grossed up at 8%, no directly stated total existing for that year. "+BANK_ARA_CAPITAL_NOTE)

# ---------------------------------------------------------------
# RWA Breakdown - Pillar 3 UK OV1 (FY2022-FY2024)/EU OV1 (FY2021) template,
# Bank-specific (consistent with the existing Bank-specific Pillar 3
# metrics above). FY2022 uses the restated figures published in the FY2023
# Pillar 3 disclosure (see note - RWAs increased £80.6m from £7,385.8m to
# £7,466.4m on a CVA/CCR adjustment for structured-entity interest rate
# swaps). FY2025 is blank - the only available FY2025 Pillar 3 publication
# is Group-only (post-listing) and is not substituted for Bank data, per
# the existing convention on this workbook's other Pillar 3 sheets. All 4
# populated years sum exactly to Total RWAs above.
# ---------------------------------------------------------------
rwa_breakdown_rows = [
    # Five different source tables, in four different formats, across twelve years.
    # Each keeps its own block and its own TOTAL (GA-002); nothing is merged or
    # re-labelled across a break and no figure is changed.
    ("SECTION", "Annual Report and Accounts 2025, Risk Report - 'Risk-weighted assets' table, p.91 (FY2025). NOT a Pillar 3 template: the only FY2025 Pillar 3 publication is Shawbrook Group plc-only (post-listing) and is not substituted for Bank data. This table's four categories map one-for-one onto the UK OV1 rows below, and its FY2024 column reproduces the UK OV1 block's FY2024 figures exactly, line for line - see sources note", {}),
    ("DATA", "Credit risk (excluding CCR)", {"FY2025": 10739.3}),
    ("DATA", "Counterparty credit risk (CCR) - credit valuation adjustment", {"FY2025": 2.5}),
    ("DATA", "Securitisation exposures in the non-trading book (after the cap)", {"FY2025": 213.8}),
    ("DATA", "Operational risk", {"FY2025": 1044.8}),
    ("TOTAL", "Total RWAs", {"FY2025": 12000.4}),

    ("SECTION", "UK OV1 'Overview of risk-weighted exposure amounts', Shawbrook Bank Limited section - Pillar 3 Disclosures 2024, Table 11, p.16 (FY2024) and Pillar 3 Disclosures 2023, Table 14, p.19 (FY2023, with FY2022 as that edition's RESTATED comparative column) (FY2024-FY2022)", {}),
    ("DATA", "Credit risk (excluding CCR)", {"FY2024": 8925.4, "FY2023": 7942.9, "FY2022": 6768.0}),
    ("DATA", "Counterparty credit risk (CCR) - credit valuation adjustment", {"FY2024": 4.2, "FY2023": 2.7, "FY2022": 65.1}),
    ("DATA", "Securitisation exposures in the non-trading book (after the cap)", {"FY2024": 117.3, "FY2023": 46.2, "FY2022": 31.8}),
    ("DATA", "Operational risk", {"FY2024": 905.3, "FY2023": 715.5, "FY2022": 601.5}),
    ("TOTAL", "Total RWAs", {"FY2024": 9952.2, "FY2023": 8707.3, "FY2022": 7466.4}),

    ("SECTION", "EU OV1 'Overview of risk-weighted assets (EU OV1) and minimum capital requirements under Pillar 1 for Shawbrook Bank Limited' - Pillar 3 Disclosures 2021, Appendix 4, p.57 (FY2021)", {}),
    ("DATA", "Credit risk (excluding CCR)", {"FY2021": 5582.3}),
    ("DATA", "Counterparty credit risk (CCR) - credit valuation adjustment", {"FY2021": 1.0}),
    ("DATA", "Securitisation exposures in the non-trading book (after the cap)", {"FY2021": 20.9}),
    ("DATA", "Operational risk", {"FY2021": 529.8}),
    ("TOTAL", "Total RWAs", {"FY2021": 6134.0}),

    ("SECTION", "Appendix 1 Bank-level capital-composition table (RWA by category) - Pillar 3 Disclosures 2020, p.49, with FY2019 taken from that same document's FY2019 comparative column (FY2020, FY2019). Not an OV1 template: FY2019's own Pillar 3 document disclosed no Bank-level operational-risk RWA, and no Bank-level securitisation line is disclosed for FY2019 - blank there, not nil", {}),
    ("DATA", "Credit risk (excluding CCR)", {"FY2020": 4748.0, "FY2019": 4519.0}),
    ("DATA", "Counterparty credit risk (CCR) - credit valuation adjustment", {"FY2020": 2.6, "FY2019": 3.8}),
    ("DATA", "Securitisation exposures in the non-trading book (after the cap)", {"FY2020": 15.9}),
    ("DATA", "Operational risk", {"FY2020": 501.9, "FY2019": 449.7}),
    ("TOTAL", "Total RWAs", {"FY2020": 5268.4, "FY2019": 4972.5}),

    ("SECTION", "Shawbrook Bank Limited's OWN ANNUAL REPORT AND ACCOUNTS, 'Capital risk and management'/'Capital risk management' RWA table, COMPANY column - Annual Report and Accounts 2018 Note 12, printed p.62 (FY2018); Annual Report and Accounts 2017 'Risk management', printed p.92 (FY2017); Annual Report and Accounts 2016 'Risk management - Capital risk management', printed p.90 (FY2016). NOT a Pillar 3 template and NOT an OV1 breakdown: these are Shawbrook's own business-line categories, so these three years are not comparable line-for-line with the OV1 blocks above. Recovered 2026-09-18 - the Pillar 3 documents of these years genuinely carry no Bank-level operational-risk RWA, but the Bank published the full Bank-level RWA table in its Annual Report instead. All three filings are image-only scans, OCR'd and confirmed against the page image; each year is from its own edition", {}),
    ("DATA", "Property Finance", {"FY2018": 1660.7, "FY2017": 1529.1, "FY2016": 1107.1}),
    ("DATA", "Business Finance", {"FY2018": 1476.2, "FY2017": 945.3, "FY2016": 1019.7}),
    ("DATA", "Consumer Lending", {"FY2018": 560.2, "FY2017": 489.8, "FY2016": 372.9}),
    ("DATA", "Other (FY2017 as its own edition prints it, 66.7; the FY2018 edition's FY2017 comparative instead shows 65.8 with the 0.9 credit valuation adjustment split out - same 3,335.4 total, not reconciled here)", {"FY2018": 133.8, "FY2017": 66.7, "FY2016": 66.9}),
    ("DATA", "Operational risk", {"FY2018": 383.8, "FY2017": 304.5, "FY2016": 212.0}),
    ("DATA", "Credit valuation adjustment (a separate row only from the FY2018 edition on)", {"FY2018": 3.4}),
    ("TOTAL", "Total RWAs", {"FY2018": 4218.1, "FY2017": 3335.4, "FY2016": 2778.6}),

    ("SECTION", "'Pillar 1 requirements' table - Pillar 3 Disclosures 2015, Appendix 1, p.33 and Pillar 3 Disclosures 2014, Appendix, pp.39-40 (FY2015, FY2014). DERIVED, not disclosed: each category is that year's own disclosed Bank-level Pillar 1 CAPITAL requirement grossed up at 8%, no RWA-by-category template existing yet. This table has no CCR/CVA and no securitisation line at all, so those rows are absent here rather than nil, and these two years are not comparable line-for-line with an OV1 breakdown. FY2015's two categories sum to 2,173.8 against the £2,175.9m Total risk exposure amount the Bank states directly in its countercyclical-buffer table - a £2.1m rounding artefact of grossing up requirements stated to £0.1m, kept rather than smoothed (see sources note)", {}),
    ("DATA", "Credit risk", {"FY2015": 2051.3, "FY2014": 1405.0}),
    ("DATA", "Operational risk", {"FY2015": 122.5, "FY2014": 55.0}),
    ("TOTAL", "Total RWAs", {"FY2015": 2175.9, "FY2014": 1460.0}),
]

b.add_rwa_breakdown_sheet(
    title="Shawbrook Bank Limited — RWA Breakdown",
    subtitle="Bank-specific basis, £m. FY2025 comes from Shawbrook Bank Limited's own Annual Report and "
              "Accounts 2025, not a Pillar 3 document (the only FY2025 Pillar 3 publication is Shawbrook Group "
              "plc-only, post-listing, and is not substituted for Bank data) - its four risk categories map "
              "one-for-one onto the UK OV1 rows and its FY2024 column reproduces this sheet's FY2024 figures "
              "exactly; see source note. FY2022 uses the restated figures "
              "published in the FY2023 Pillar 3 disclosure (RWAs increased £80.6m on a CVA/CCR adjustment - see "
              "source note). FY2018-FY2016 come from Shawbrook Bank Limited's own Annual Report and Accounts "
              "(Company column), not a Pillar 3 document - those years' Pillar 3 Appendix 1 really does disclose "
              "no Bank-level operational-risk RWA, but the Bank published a full Bank-level RWA table in its "
              "Annual Report instead; the categories there are Shawbrook's own business lines, so those three "
              "years are not comparable line-for-line with the OV1 blocks, and they sum exactly to Total RWAs. "
              "FY2015/FY2014 categories are derived from the Bank's own disclosed Pillar 1 capital requirement "
              "(Credit risk + Operational risk) grossed up at 8%, since no RWA-by-category template existed yet; "
              "no CCR/securitisation breakout is available at Bank level for those two years. FY2015's categories "
              "sum to £2,173.8m against a disclosed Total risk exposure amount of £2,175.9m - a £2.1m rounding "
              "artefact of grossing up capital requirements stated to £0.1m, kept rather than smoothed (see source "
              "note). Every other populated year sums exactly to Total RWAs.",
    rows=rwa_breakdown_rows,
    sources_text=(
        "Sources - Shawbrook Bank Limited, UK OV1 / EU OV1: Overview of risk-weighted exposure amounts:\n"
        f"FY2024: Pillar 3 Disclosures 2024, Table 11 (UK OV1), p.16 - {P3['FY2024']}\n"
        f"FY2023: Pillar 3 Disclosures 2023, Table 14 (UK OV1), p.19 - {P3['FY2023']}\n"
        f"FY2022 (restated): Pillar 3 Disclosures 2023, Table 14 (UK OV1, FY2022 restated comparative column), "
        f"p.19 - RWAs restated from £7,385.8m to £7,466.4m to reflect a CVA/CCR adjustment on the Bank's "
        f"structured entities' interest rate swap derivatives (footnote 1) - {P3['FY2023']}\n"
        f"FY2021: Pillar 3 Disclosures 2021, Appendix 4 ('Overview of risk-weighted assets (EU OV1) and minimum "
        f"capital requirements under Pillar 1 for Shawbrook Bank Limited'), p.57 - independently cross-checked "
        f"against Pillar 3 Disclosures 2022, Table 14's FY2021 comparative column, which agrees exactly - "
        f"{P3['FY2021']}\n"
        f"FY2025: Shawbrook Bank Limited Annual Report and Accounts 2025, Risk Report - 'Principal risks: "
        f"Market, liquidity and capital risk', 'Risk-weighted assets' table, p.91 - {AR['FY2025']}\n"
        f"  The FY2025 Pillar 3 publication ({P3['FY2025']}) is Shawbrook Group plc-only and is NOT used. "
        f"The Annual Report's table splits credit risk by product (Real Estate 3,615.8; SME 4,389.7; Consumer "
        f"Finance 743.0; Retail Mortgage Brands 1,768.9; Other 221.9) and prints its own 'Total credit risk' "
        f"of 10,739.3 - reproduced here on the 'Credit risk (excluding CCR)' row because it is the same "
        f"quantity as the UK OV1 row: the product sub-rows foot exactly to 10,739.3, and the table's remaining "
        f"three lines are labelled identically to the OV1 rows ('Counterparty credit risk: credit valuation "
        f"adjustment' 2.5; 'Securitisation exposures in the banking book' 213.8; 'Operational risk' 1,044.8), "
        f"summing exactly to the disclosed Total risk-weighted assets of 12,000.4. BASIS CHECK: that same "
        f"table's FY2024 column (credit risk 8,925.4; CVA 4.2; securitisation 117.3; operational risk 905.3; "
        f"total 9,952.2) reproduces this sheet's Pillar 3-sourced FY2024 row values exactly, line for line, "
        f"confirming the Annual Report table and the Bank UK OV1 template are the same measure on the same "
        f"Bank (solo-consolidated) basis.\n"
        f"FY2020: Pillar 3 Disclosures 2020, Appendix 1 capital-composition table (Bank-level RWA by category), "
        f"p.49 - {P3['FY2020']}\n"
        f"FY2019: Pillar 3 Disclosures 2020, Appendix 1, FY2019 comparative column, p.49 (FY2019's own Pillar 3 "
        f"document did not itself disclose a Bank-level operational-risk RWA) - {P3['FY2020']}\n"
        f"FY2018: Shawbrook Bank Limited Annual Report and Accounts 2018, Note 12 'Capital risk and management', "
        f"'Risk-weighted assets' table, Company column, printed p.62 - {AR_CH_DOC['FY2018']}\n"
        f"FY2017: Shawbrook Bank Limited Annual Report and Accounts 2017, 'Risk management', RWA table, Company "
        f"column, printed p.92 - {AR_CH_DOC['FY2017']}\n"
        f"FY2016: Shawbrook Bank Limited Annual Report and Accounts 2016, 'Risk management - Capital risk "
        f"management', 'Risk-weighted assets (unaudited)', Company column, printed p.90 - {AR_CH_DOC['FY2016']}\n"
        f"  The Pillar 3 documents of these three years ({P3['FY2018']}, {P3['FY2017']}, {P3['FY2016']}) were "
        f"re-read on 2026-09-18 and confirmed NOT to carry a Bank-level total-RWA breakdown: the 2016 and 2017 "
        f"editions' Appendix 1 gives only capital composition, an equity reconciliation, a Tier 1 movement table "
        f"and the LRSum/LRCom leverage templates, and the 2018 edition's Appendix 1 adds a credit-risk exposure "
        f"table whose Bank RWAs (3,830.9 for FY2018, 3,030.6 for FY2017) are CREDIT RISK ONLY. Those credit-only "
        f"figures are deliberately NOT used on this sheet, since they are a different quantity from the Annual "
        f"Report's category rows and would not foot to the disclosed total.\n"
        f"FY2015 (derived): Pillar 3 Disclosures 2015, Appendix 1 'Pillar 1 requirements' table, p.33 (Credit "
        f"risk £164.1m, Operational risk £9.8m, each grossed up at 8%) - {P3['FY2015']}\n"
        f"FY2014 (derived): Pillar 3 Disclosures 2014, Appendix 1 'Pillar 1 requirements' table, p.39-40 (Credit "
        f"risk £112.4m, Operational risk £4.4m, each grossed up at 8%) - {P3['FY2014']}\n\n" + LINK_PROVENANCE + "\n\n" + note
    ),
    first_col_width=64,
    source_height=300,
    unit_suffix=" (£m)",
)

m("Leverage Ratio","%",d(["7.8%","8.1%","8.2%","8.8%","8.0%","8.6%","8.6%","9.2%","9.5%","7.7%","6.9%","6.1%"]),AR2025_BANK_BASIS+" FY2022 uses the UK leverage framework effective 1 January 2022; FY2021 uses the prior basis and comparatives were not restated. FY2014-FY2020 each use that year's own Bank-specific leverage-ratio disclosure (methodology evolved gradually year to year under CRD IV/Basel III transitional rules).")
b.add_metric_sheet("LCR","%",[
    ("Liquidity coverage ratio - Pillar 3 UK KM1 basis (12-month average)",
     d([None,"265.0%","310.9%","290.3%",None,None,None,None,None,None,None,None])),
    ("Liquidity coverage ratio - Annual Report basis (point-in-time at the year-end)",
     d(["147.2%","176.0%",None,None,None,None,None,None,None,None,None,None])),
    ("Liquidity buffer, point-in-time basis (£m)",
     d([2975.8,3161.5,None,None,None,None,None,None,None,None,None,None])),
    ("Total 30-day net cash outflows, point-in-time basis (£m)",
     d([2022.0,1796.1,None,None,None,None,None,None,None,None,None,None])),
],ps,note=(
    "TWO BASES, ON TWO SEPARATE ROWS - READ THE ROW LABEL BEFORE COMPARING ANYTHING, AND NEVER READ ACROSS "
    "ROW 1 INTO ROW 2. Row 1 is the 12-month-average LCR from Shawbrook Bank Limited's own Pillar 3 UK KM1, "
    "which is the measure this project's LCR sheets carry wherever a Bank-level Pillar 3 exists. Row 2 is the "
    "point-in-time year-end LCR that the Bank's own Annual Report states, with rows 3 and 4 giving the two "
    "quantities it is struck from.\n"
    "WHY FY2025 IS ON ROW 2 AND NOT ROW 1 (changed 2026-09-18; this sheet previously left FY2025 wholly "
    "blank). The FY2025 Pillar 3 publication is Shawbrook Group plc-only and carries no Bank-level section, so "
    "there is no 12-month-average Bank LCR for FY2025 and row 1 is correctly empty. But the figure was not "
    "missing, only on another basis, and leaving the column blank hid a disclosure the Bank did make. It now "
    "appears where it belongs, on its own labelled row.\n"
    "THE SIZE OF THE BASIS GAP, WHICH IS WHY THE TWO ROWS MUST NEVER BE SPLICED: FY2024 appears on BOTH rows "
    "from two of the Bank's own documents for the same date and the same entity - 265.0% on the KM1 average "
    "basis against 176.0% point-in-time, an 89-point difference. Reading 147.2% as the successor to 265.0% "
    "would show a 118-point collapse that did not happen. The FY2024 point-in-time figure is carried here "
    "deliberately so that the gap is visible on the sheet rather than only described in this note.\n"
    "The Annual Report's own explanation of the 2025 fall (176.0% to 147.2%) is a change in the composition of "
    "the liquidity pool: the Bank increased its holdings of Bank of England eligible collateral, which counts "
    "in its internal Liquid Asset Buffer but does not qualify as HQLA for the LCR.\n"
    "This is the ONLY metric where the Annual Report and the Pillar 3 disagree: CET1/Tier 1/Total capital, all "
    "three capital ratios, RWAs, leverage and NSFR all reproduce exactly between the two.\n"
    "Bank-specific FY2021 LCR was not provided and Group data was not substituted; no Bank-specific LCR is "
    "disclosed for any of FY2014-FY2020 either - Group-only throughout."),
    first_col_width=54,source_height=280)
m("NSFR","%",d(["124.9%","134.5%","145.8%",None,None,None,None,None,None,None,None,None]),AR2025_BANK_BASIS+" The Annual Report 2025 states the FY2024 NSFR as 134.5%, exactly matching the figure already recorded here from the FY2024 Pillar 3, so the NSFR basis is unchanged. NSFR was not applicable in the FY2022 disclosure. No Bank-specific NSFR is disclosed for any of FY2014-FY2020 - Group-only throughout, and the UK had no binding NSFR requirement before 1 January 2022 (CRR II).")
m("MREL Ratio","%",d([None,None,None,None,None,None,None,None,None,None,None,None]),"No Bank-specific quantitative MREL ratio was disclosed in any year FY2014-FY2025; MREL itself did not apply to UK banks until several years into this window.")

b.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", d([22535.7, 19629.0, 17100.9, 13945.7, 11094.6, 8980.6, 8248.0, 6805.6, 5701.4, 4625.0, 3978.1, 2732.1])),
        ("Loans and advances to customers", d([17801.1, 15129.4, 13157.9, 10472.8, 8278.9, 7061.3, 6637.7, 5805.7, 4799.3, 4050.4, 3319.1, 2284.7])),
        ("Customer deposits", d([18353.5, 15804.0, 13562.7, 10914.5, 8358.6, 6894.1, 6109.4, 4977.9, 4376.2, 3943.5, 3186.4, 2421.0])),
        ("Total equity", d([1875.7, 1610.1, 1391.4, 1136.4, 942.8, 792.9, 743.9, 660.3, 601.0, 413.1, 342.2, 196.8])),
    ],
    balance_sheet_unit="£m",
    income_statement_totals=[
        ("Net operating income", d([681.3, 609.1, 586.0, 476.2, 386.0, 282.4, 295.2, 272.9, 238.1, 209.7, 166.9, 112.2])),
        ("Total operating expenses", d([-409.7, -314.1, -298.8, -237.8, -188.6, -206.2, -172.8, -162.1, -138.6, -120.6, -92.1, -66.1])),
        ("Profit after tax, attributable to owners", d([194.9, 219.8, 212.6, 179.7, 149.5, 58.2, 93.8, 82.0, 74.2, 65.7, 63.0, 35.3])),
    ],
    income_statement_unit="£m",
    equity_changes_totals=[
        ("Opening equity", d([1610.1, 1391.4, 1136.4, 942.8, 792.9, 743.9, 660.3, 601.0, 413.1, 342.2, 196.8, 111.6])),
        ("Profit for the year", d([189.2, 203.2, 246.4, 213.0, 153.5, 58.3, 92.6, 82.6, 74.9, 66.1, 63.2, 38.0])),
        ("Other equity movements, net", d([76.4, 15.5, 8.6, -19.4, -3.6, -9.3, -9.0, -23.3, 113.0, 4.8, 82.2, 47.2])),
        ("Closing equity", d([1875.7, 1610.1, 1391.4, 1136.4, 942.8, 792.9, 743.9, 660.3, 601.0, 413.1, 342.2, 196.8])),
    ],
    equity_changes_unit="£m",
    cash_flow_totals=[("Net cash generated from operating activities",d([370.6,542.6,451.8,683.2,81.1,515.7,359.0,-337.3,-220.6,-195.1,102.3,283.5])),("Net cash (used by)/generated from investing activities",d([-895.2,-675.1,-172.4,-121.4,-207.5,-185.1,-88.8,-158.9,-11.4,-7.9,-18.2,-89.0])),("Net cash (used by)/generated from financing activities",d([155.8,140.3,-1.1,-76.1,508.2,-95.1,147.8,405.9,558.7,102.5,118.2,-76.3])),("Cash and cash equivalents as at 31 December",d([2124.7,2493.5,2485.7,2207.4,1721.7,1339.9,1104.4,686.4,776.7,450.0,550.5,347.8]))],
    cash_flow_unit="£m",
    ratios=[("CET1 Ratio",d(["12.4%","13.0%","12.9%","12.7%","12.6%","12.6%","12.0%","12.2%","12.9%","13.2%","14.2%","11.5%"])),("Tier 1 Ratio",d(["13.5%","14.3%","14.3%","14.6%","14.7%","15.0%","14.5%","15.2%","16.7%","13.2%","14.2%","11.5%"])),("Total Capital Ratio",d(["14.9%","15.9%","16.4%","15.9%","16.2%","16.8%","16.4%","16.9%","19.3%","16.3%","17.9%","13.8%"])),("Leverage Ratio",d(["7.8%","8.1%","8.2%","8.8%","8.0%","8.6%","8.6%","9.2%","9.5%","7.7%","6.9%","6.1%"])),("LCR",d([None,"265.0%","310.9%","290.3%",None,None,None,None,None,None,None,None])),("NSFR",d(["124.9%","134.5%","145.8%",None,None,None,None,None,None,None,None,None]))],
    note="Balance Sheet/Statement of Changes in Equity use the Company column; Profit & Loss is necessarily "
         "Group basis (Company takes the s.408 exemption) - see the Profit & Loss sheet's source note. "
         "Company-only cash flows and Bank-specific regulatory metrics; FY2025 Bank regulatory metrics are "
         "blank because the available Pillar 3 document is Group-only. FY2016-FY2018 capital ratios are blank "
         "because no Bank-level Total RWA is available those years (see Pillar 3 sheets' source notes). "
         "This Overview stays on the project-wide FY2014 floor; the Balance Sheet, Profit & Loss, Statement of "
         "Changes in Equity and Cash Flow Statement sheets were separately extended back to FY2012 per wayfinder "
         "ticket HD-072 (Pillar 3, Asset Quality and RWA Breakdown were not, since Pillar 3 disclosures genuinely "
         "aren't comparable pre-CRD IV/Basel III) - see those sheets directly for FY2013/FY2012 figures.",
)
b.save("/Users/armaan/code/katalysis/banks/SHAWBROOK FINANCIALS.xlsx")
