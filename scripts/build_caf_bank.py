import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

# CAF Bank Limited (Companies House 01837656, FRN 204451), owned by Charities
# Aid Foundation (CAF), serves charities/non-profits. Fiscal year-end 30 April.
YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021", "FY2020"]  # most recent first
YEAR_LABEL = {y: y for y in YEARS}

CH_BASE = "https://find-and-update.company-information.service.gov.uk/company/01837656/filing-history"
AR2025_URL = f"{CH_BASE}/MzUwNDA1NTExOGFkaXF6a2N4/document?format=pdf&download=0"
AR2023_URL = f"{CH_BASE}/MzM5MjYwNDE2NmFkaXF6a2N4/document?format=pdf&download=0"
AR2021_URL = f"{CH_BASE}/MzMxMTMwNTcwNWFkaXF6a2N4/document?format=pdf&download=0"
# FY2020 own filing (found 2026-09-06 during HD-061's FY2020 extension) - re-verified directly
# against a rendered page-image read (0 text layer, same as every other CAF Bank filing), not
# assumed from the ticket's nominal "confirmed floor" alone. Its own FY2019 comparative column
# and FY2021's own FY2020 comparative column (in AR2021_URL) both cross-check exactly.
AR2020_URL = f"{CH_BASE}/MzI3NzEzMDk0OWFkaXF6a2N4/document?format=pdf&download=0"

# CAF Bank's own Pillar 3 archive (cafonline.org) - found 2026-09-05 during a
# historical-depth feasibility check (wayfinder/historical-depth/, HD-002)
# that flagged this workbook's original "no Pillar 3 disclosure of any kind"
# finding as likely wrong; a dedicated verification pass confirmed real,
# CAF-Bank-specific standalone Pillar 3 PDFs exist for FY2021-FY2024 (FY2020
# too, outside this workbook's window). FY2025 has no standalone document -
# CAF Bank moved to the PRA's SDDT ("Small Domestic Deposit Taker") regime,
# which doesn't require one - but the FY2025 Annual Report's own Strategic
# Report discloses 3 of the metrics directly (Total Capital Ratio, Leverage
# Ratio, LCR), used below instead of leaving that year fully blank.
P3_2021_URL = "https://www.cafonline.org/docs/default-source/about-us-governance/caf_bank_pillar3_2021.pdf"
P3_2022_URL = "https://www.cafonline.org/docs/default-source/about-us-governance/caf_bank_pillar3_2022.pdf"
P3_2023_URL = "https://www.cafonline.org/docs/default-source/about-us-governance/caf_bank_pillar_ar_2023.pdf"
P3_2024_URL = "https://www.cafonline.org/docs/default-source/annual-reports/caf-bank-pillar-3-disclosure-2023_2024.pdf"
# FY2020 Pillar 3 (found 2026-09-06, HD-061): NOT at the naive "caf_bank_pillar3_2020.pdf" guess
# (404s live - a different, retired page path) - recovered via a Wayback CDX domain scan of
# cafonline.org for historical Pillar 3 filenames, which surfaced this bank's own internal
# publish-date-coded naming convention (each PDF's filename ends in a YYMMDD publish-date code,
# e.g. "_250920" = published 25 Sep 2020). Confirmed live at its original URL (not just archived).
P3_2020_URL = "https://www.cafonline.org/docs/default-source/about-us-about-caf-bank/cafbank_pillar3_disclosure_2921d_250920.pdf"

ENTITY_NOTE = (
    "ENTITY NOTE: CAF Bank Limited (Companies House 01837656, FRN 204451, formerly Cafcash Limited) is a UK bank "
    "wholly owned by the Charities Aid Foundation (CAF, registered charity 268369), serving charities/non-profits. "
    "It takes no FRS 101/102 cash-flow exemption - full Cash Flow Statement every year. All 4 source Companies "
    "House filings used (FY2025, FY2023-with-FY2022-comparative, FY2021, FY2020) are fully scanned/image-only (0 "
    "text blocks/page) - every figure was transcribed via high-resolution page-image review, cross-checked against "
    "the following year's comparative column where available. FY2024's own standalone filing was not needed since "
    "FY2025's filing carries it as a comparative; FY2022's standalone filing was likewise not needed since FY2023's "
    "filing carries it as a comparative.\n\n"
    "HISTORICAL-DEPTH EXTENSION (2026-09-06, HD-061): extended back to FY2020, this project's confirmed floor for "
    "this entity. FY2020's own filing was re-verified directly (rendered page images, not assumed from the "
    "ticket's nominal floor) and cross-checks exactly against FY2021's own FY2020 comparative column in every "
    "statement - no restatement found anywhere in this extension. One genuine label quirk in FY2020's own "
    "Profit and Loss Account, reproduced as printed rather than silently corrected: its fee-income subtotal is "
    "itself labelled 'Net operating income' (a mislabelling that FY2021 onward's own presentation calls 'Net fee "
    "income', reserving 'Net operating income' for the combined interest+fee total) - this workbook's 'Net fee "
    "income' row for FY2020 uses that same figure, and its 'Net operating income' row for FY2020 is a computed "
    "sum (interest £11,499k + fee £1,101k = £12,600k) since FY2020's own document never prints that combined "
    "total under any label. The FY2020 Companies House filing (Note 10) discloses the individual/collective loan "
    "loss provision split directly - unlike FY2022/FY2023, no follow-up pass was needed to find it.\n\n"
    "DATA QUALITY NOTE: the FY2025 column's 'Net cash generated from operating activities' total (£20,729k) and "
    "'Net cash used in investing activities' total (£60,368k) are both independently corroborated - they sum "
    "exactly to the stated 'Change in cash and cash equivalents in the year' (£(39,639)k), and the closing balance "
    "these imply matches the 'Represented by' breakdown exactly. However, one underlying adjustment line "
    "('Amortisation of investments') is genuinely ambiguous in the source scan between the two plausible digit "
    "readings £(6,041)k and £(8,041)k - only the former makes the itemised adjustments sum exactly to the stated "
    "operating total, so £(6,041)k is used here as the internally-consistent figure (the same approach used "
    "elsewhere in this project for LHV/Zempler/Vanquis source-document ambiguities). The FY2024 comparative "
    "column's own itemised lines sum exactly to its own stated totals with no ambiguity.\n\n"
    "CORRECTION (2026-09-05): an earlier version of this workbook stated that no Pillar 3 disclosure of any kind "
    "existed for this entity - that was wrong. CAF Bank Limited publishes its own standalone Pillar 3 Disclosure "
    "PDFs on cafonline.org; the original build simply didn't find them (it checked the Annual Report/Companies "
    "House filings only, where the observation of 'no figures in the financial statements themselves' is true but "
    "incomplete). Real solo-basis Pillar 3 documents exist for FY2020-FY2024 (see PILLAR3_SOURCES below for exact "
    "URLs/pages); see each metric sheet for its own sourcing. FY2025 has no standalone Pillar 3 document - CAF "
    "Bank's own site states it 'has become part of the PRA's SDDT (\"Small Domestic Deposit Taker\") regime under "
    "which, as a non-listed institution, the Bank is not required to publish a Pillar 3 report' (quoted verbatim "
    "and in full from https://www.cafonline.org/home/caf-bank/about-us/legal-information/pillar-3-disclosure, "
    "fetched and read again on 2026-09-15 - that single sentence is the entire substantive content of the page. "
    "Note what the page does NOT do: it carries no date of its own, states no effective date for the change, and "
    "names no rule number. That is exactly why the PRA register, not this page, is treated as the evidence - see "
    "the SDDT DATE TEST below) - but the FY2025 "
    "Annual Report's own Strategic Report ('Liquidity, the Investment Portfolio and Capital' section, p.27-28) "
    "discloses 3 of the 11 metrics directly (Total Capital Ratio, Leverage Ratio, LCR), used on those 3 sheets "
    "instead of leaving FY2025 blank; CET1/Tier 1/Total Capital (£)/Total RWAs/RWA Breakdown/NSFR are genuinely "
    "not disclosed anywhere for FY2025, confirmed by a full-document search of the 51-page Annual Report. MREL "
    "Ratio is not disclosed in any year FY2020-FY2025, in either the Pillar 3 documents or the Annual Reports.\n\n"
    "SDDT DATE TEST (checked 2026-09-15) - OUTCOME: UNDETERMINED, two sourced facts in tension, both recorded.\n"
    "FACT 1 (the register): the PRA's consolidated list of waivers and modifications granted to PRA-authorised "
    "firms records that CAF BANK LIMITED (FRN 204451) holds a 'Modification by Consent - PRA Rulebook - CRR Firms "
    "- Rule 3.1 of the SDDT Regime - General Application Part', rule 'SDDT Regime - General Application', "
    "sub-rule 'Ru 3.1', waiver ref 'A00010742P.pdf', with a START DATE of 08/08/2025 and NO END DATE. That "
    "modification removes the Pillar 3 obligation outright - a stronger relief than UK CRR Article 433b, which "
    "only reduces frequency/content for small and non-complex institutions, and quite different again from the "
    "eligibility-criterion modifications (Ru 1.2 / 2.1(9) / 2.6) that some firms hold without being SDDTs at all. "
    "Rule 3.1 is the operative opt-in, and it is the ONLY SDDT row against FRN 204451 - CAF holds no "
    "criteria-only row. RE-DOWNLOADED AND RE-VERIFIED INDEPENDENTLY 2026-09-15: the register was pulled fresh "
    "from https://www.bankofengland.co.uk/-/media/boe/files/prudential-regulation/authorisations/"
    "waivers-and-modifications-of-rules/consolidated-waivers-pra-firms.csv - a UTF-16 little-endian, "
    "TAB-separated file of 2,919 data rows despite the .csv extension, which must be decoded as UTF-16 or it "
    "reads as binary noise - and the row above reproduces to the character. CAF Bank's four OTHER register rows "
    "were captured in the same pass and are recorded here so the Rule 3.1 row is not confused with any of them: "
    "Ar 26(3) CRR (A3908085P.pdf, start 18/01/2017); Capital Buffers 5.1-5.3 (00007843.pdf, start 10/05/2024); "
    "Ar 26(2) inclusion of interim profits (A00008787P.pdf, start 03/10/2024, END DATE 01/11/2026 - the only CAF "
    "row that expires); and a second Ar 26(3) CET1-classification permission (A00005546P.pdf, start 03/11/2022). "
    "None of those four touches disclosure. The register is a living document, so this re-pull also confirms the "
    "Rule 3.1 row has not been withdrawn or re-dated since the original check.\n"
    "FACT 2 (the year-end): CAF Bank's year-end is 30 April, stable across its Companies House accounts filing "
    "history (company 01837656; accounts made up to 30 April 2025, 2024, 2023 ...). FY2025 therefore ended on 30 "
    "April 2025 - THREE MONTHS BEFORE the 08/08/2025 modification took effect.\n"
    "THE TENSION: on a strict year-end reading, FY2025 predates the relief, so the Bank was still subject to the "
    "disclosure obligation for that financial year and its FY2025 blanks would be a genuine gap rather than a "
    "structural exemption. On a publication-date reading, the FY2025 Pillar 3 would not have fallen due until "
    "after 08/08/2025, by which point the obligation had been disapplied. CAF's own site asserts the second "
    "reading in substance (quoted above: 'is not required to publish a Pillar 3 report'). This project does not "
    "resolve the tension by picking a side: the FY2025 cells stay blank either way, and the distinction only "
    "affects how the blank is LABELLED. Recorded here so the next sweep does not re-litigate it.\n"
    "LABELLING RESOLVED WITHOUT RESOLVING THE TENSION (2026-09-19). The KM1 sheet's FY2025 column was the last "
    "wholly-empty column in this workbook, and a blank cell cannot distinguish 'established absent' from 'never "
    "examined' - so it now carries a short statement instead. The statement is worded to assert only what is "
    "settled: that no FY2025 edition exists, and that the date fit is UNDETERMINED. It deliberately does NOT "
    "say the SDDT opt-in explains FY2025, because on the year-end reading it does not - 30 April 2025 precedes "
    "08/08/2025 by three months. Compare Cambridge & Counties (opt-in 20/02/2025, year end 31 December 2025) "
    "and Brown Shipley (28/10/2025, year end 31 December 2025), where the fit is unambiguous and the cells say "
    "so; the difference between those banks and this one is exactly the three months, and it is the reason a "
    "waiver must be date-fitted per bank and per year rather than read as a blanket explanation. The register "
    "row itself was re-downloaded and re-matched on BOTH required columns again on 2026-09-19 (description "
    "'SDDT Regime - General Application' AND sub-rule 'Ru 3.1', FRN 204451, start 08/08/2025, no end date) and "
    "is unchanged.\n"
    "NOT IN TENSION: FY2026 (year ending 30 April 2026) falls unambiguously after the modification, so FY2026 "
    "onward is structurally exempt. FY2024 and earlier unambiguously predate it - and, consistent with that, real "
    "standalone Pillar 3 documents do exist for FY2020-FY2024.\n\n"
    "FY2025 RE-VERIFIED 2026-09-15 (independent second pass, latest-year gap sweep). Three checks, all negative:\n"
    "(1) No FY2025 standalone Pillar 3 document exists. cafonline.org serves a 136kB HTML soft-404 (HTTP 200, "
    "content-type text/html) for every plausible filename under both of this bank's known Pillar 3 folders - "
    "/docs/default-source/about-us-governance/ (caf_bank_pillar3_2025.pdf, caf_bank_pillar_ar_2025.pdf) and "
    "/docs/default-source/annual-reports/ (caf-bank-pillar-3-disclosure-2024_2025.pdf, ...-2024-2025.pdf, "
    "...-2025.pdf, ...-2024_25.pdf, caf-bank-pillar-3-report-2024_2025.pdf) - while the FY2024 file at "
    "P3_2024_URL still returns a real 1.4MB application/pdf from the same folder, so the soft-404 is a genuine "
    "absence and not a site-wide outage. No Pillar 3 link appears on the bank's live pages either.\n"
    "(2) The 51-page FY2025 Annual Report was re-OCR'd in full from the Companies House filing (it is a "
    "go-tiff2pdf scan with a zero-byte text layer, and its pages are rotated 90 degrees - tesseract --psm 6 "
    "returns noise, --psm 1 with orientation detection is required). A whole-document search of that OCR for "
    "'risk-weighted', 'RWA', 'CET1', 'Common Equity', 'NSFR' and 'net stable' returns no hits at all, "
    "independently confirming that CET1/Tier 1/Total Capital (GBP)/Total RWAs/RWA Breakdown/NSFR really are "
    "absent rather than merely missed.\n"
    "(3) The three figures that ARE populated were re-read against the same OCR and agree: Overall Regulatory "
    "Capital Ratio 29.7% (vs 30.3% at 30 April 2024), and LCR 543% (vs 257%). The Leverage Ratio is a "
    "deliberate exception to trusting OCR here: tesseract read '6.15%' at both 250 and 450 DPI, but a "
    "magnified visual read of that line in the page image shows '6 35%' - the carried 6.35% is correct and was "
    "left unchanged. Recorded because the same 3-as-1 misread would silently corrupt any future machine-only "
    "pass over this filing."
)

PILLAR3_SOURCES = (
    "Sources - CAF Bank Limited's own standalone Pillar 3 Disclosure PDFs (solo basis, fiscal year-end 30 April), "
    "found on cafonline.org (not Companies House) - a 2026-09-05 correction, see ENTITY_NOTE above:\n"
    f"FY2020: CAF Bank Ltd Pillar 3 Disclosure, 30 April 2020, 'Capital resources' table (p.7) and 'Pillar 1 "
    f"capital requirement' table (p.9) - {P3_2020_URL}\n"
    f"FY2021: CAF Bank Ltd Pillar 3 Disclosure, 30 April 2021, 'Total Capital Resources' table (p.4) and 'Pillar 1 "
    f"capital requirement' table (p.7) - {P3_2021_URL}\n"
    f"FY2022: CAF BANK LTD Pillar 3 Disclosure, 30 April 2022, Template UK KM1 'Key metrics' (p.5), Template UK OV1 "
    f"'Overview of risk weighted exposure amounts' (p.11), Template UK LIQ1/LIQ2 (p.25-26) - {P3_2022_URL}\n"
    f"FY2023: Pillar 3 Report 2022/23, CAF Bank Ltd Pillar 3 Disclosure, 30 April 2023, Template UK KM1 (p.4), "
    f"Template UK OV1 (p.7) - {P3_2023_URL}\n"
    f"FY2024: Pillar 3 Report 2023/24, Pillar 3 Disclosure, CAF Bank Ltd, 30 April 2024, Template UK KM1 (p.5), "
    f"Template UK OV1 (p.8), Template UK LRCom (p.9) - {P3_2024_URL}\n"
    f"FY2025: no standalone Pillar 3 document exists (SDDT-exempt) - CAF Bank Ltd Annual Report and Financial "
    f"Statements for the year ended 30 April 2025, Strategic Report, 'Liquidity, the Investment Portfolio and "
    f"Capital' section (p.27-28) - {AR2025_URL}\n\n"
    "RESTATEMENT NOTE (each year's own originally-published figure used, not a later comparative, per this "
    "project's standard convention): FY2022's own document's 2021 comparative column shows Total RWAs of "
    "£127,844k and Leverage Ratio (incl. central banks) of 2.74% - both differ immaterially from FY2021's own "
    "originally-published figures (£127,881k and 2.72% respectively, used here). FY2021's own document also "
    "predates the LIQ1/KM1 templates that introduced LCR/NSFR reporting - FY2022's document later shows a 268% "
    "LCR comparative for FY2021, but since FY2021's own document never disclosed an LCR figure at all, FY2021 LCR "
    "is left 'Not publicly disclosed' here rather than back-filled from a later document. FY2020's own document "
    "(pre-dating the KM1/LIQ1 templates even more than FY2021's) confirms the same absence: no LCR, NSFR or MREL "
    "figure of any kind appears anywhere in the FY2020 Pillar 3 document, found by a full read of all 27 pages - "
    "not assumed from the FY2021 pattern alone. FY2021's own document's 2020 comparative column shows CET1/Tier1/"
    "Total Capital/RWA/leverage figures identical to FY2020's own originally-published figures (used here) - no "
    "restatement at all between the two, unlike the FY2021-to-FY2022 gap above."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are CAF Bank Limited's own Cash Flow Statement, transcribed from each year's own "
    "Companies House filing (or, for FY2024/FY2022, that year's own comparative column in the following year's "
    "filing):\n"
    f"FY2025/FY2024: Full accounts made up to 30 April 2025 (filed 10 Feb 2026), Cash Flow Statement - {AR2025_URL}\n"
    f"FY2023/FY2022: Full accounts made up to 30 April 2023 (filed 14 Sep 2023), Cash Flow Statement - {AR2023_URL}\n"
    f"FY2021: Full accounts made up to 30 April 2021 (filed 31 Aug 2021), Cash Flow Statement - {AR2021_URL}\n"
    f"FY2020: Full accounts made up to 30 April 2020 (filed 10 Sep 2020), Cash Flow Statement (p.36) - {AR2020_URL}\n"
    + ENTITY_NOTE
)

bw = BankWorkbook(bank_name="CAF Bank Limited", years=YEARS, year_label=YEAR_LABEL, header_color="2E7D32")

DEBT_SECURITIES_BREAKDOWN_NOTE = (
    "DEBT SECURITIES BREAKDOWN: the 'Debt securities - ...' sub-rows below the renamed 'Total debt securities' "
    "line are transcribed from each year's own 'Debt securities'/'Investments' note, which splits the balance by "
    "issuer type (UK government, multilateral financial institutions, fixed/floating coupon corporate bonds, "
    "certificates of deposit) but not by measurement basis - accounting policy note 1.5/1.6 states debt "
    "securities held for investment purposes are 'held to redemption at par' and 'measured at amortised cost "
    "using the effective interest method' in every year covered, so all sub-rows are amortised cost (no FVOCI/"
    "FVTPL instruments held in any year):\n"
    f"FY2025/FY2024: Note 10 'Debt securities', Investments table, p.89 - {AR2025_URL}\n"
    f"FY2023/FY2022: Note 10 'Debt securities', Investments table, p.67 - {AR2023_URL}\n"
    f"FY2021: Note 11 'Debt securities', section 11.1 Investments, p.44 - {AR2021_URL}\n"
    f"FY2020: FY2021 filing's own FY2020 comparative column (same note/page as above); independently cross-checked "
    f"against FY2020's own filing, Note 11 'Debt securities', section 11.1 Investments, p.44 - {AR2020_URL} "
    "(both agree exactly on all 5 sub-row figures).\n\n"
    "Each year's sub-rows sum exactly to that year's 'Total debt securities' line. 'UK government' is disclosed "
    "as its own line only in FY2020 (£63,036k) and FY2021 (explicitly £0 - the note still prints the line with a "
    "nil balance); no 'UK government' line appears in the FY2022-FY2025 notes at all (fully divested by FY2022), "
    "not a gap. 'Certificates of deposit' (the note's 'Unlisted:' section) is disclosed FY2020-FY2023 only - the "
    "FY2024/FY2025 notes present a 'Listed:' section only with no unlisted holdings, again a genuine change in "
    "composition rather than missing data."
)

STATEMENTS_SOURCES = (
    "Sources - all figures are CAF Bank Limited's own Profit and Loss Account / Balance Sheet / Statement of "
    "Changes in Equity, transcribed from each year's own Companies House filing (or, for FY2024/FY2022, that "
    "year's own comparative column in the following year's filing):\n"
    f"FY2025/FY2024: Full accounts made up to 30 April 2025 (filed 10 Feb 2026), Profit and loss account/Balance "
    f"sheet/Statement of changes in equity - {AR2025_URL}\n"
    f"FY2023/FY2022: Full accounts made up to 30 April 2023 (filed 14 Sep 2023), Profit and loss account/Balance "
    f"sheet/Statement of changes in equity - {AR2023_URL}\n"
    f"FY2021: Full accounts made up to 30 April 2021 (filed 31 Aug 2021), Profit and loss account/Balance sheet - "
    f"{AR2021_URL}\n"
    f"FY2020: Full accounts made up to 30 April 2020 (filed 10 Sep 2020), Profit and loss account (p.33)/Balance "
    f"sheet (p.34)/Statement of changes in equity (p.35) - {AR2020_URL}\n"
    + ENTITY_NOTE
    + "\n\nPRESENTATION NOTE: the Statement of Changes in Equity had 4 equity components (Called-up share "
    "capital, Additional Tier 1 securities, Distributable reserve, Retained earnings) through FY2023; the AT1 "
    "securities were redeemed and the distributable reserve fully transferred to retained earnings during "
    "FY2023, leaving only 2 components (Called-up share capital, Retained earnings) from FY2024 onward. "
    "DISCREPANCY NOTE: the FY2021 filing's own Balance Sheet shows the Distributable reserve at 30 April 2021 as "
    "£939k, but the FY2023 filing's own equity reconciliation shows the same opening balance (at 1 May 2021) as "
    "£1,000k - a £61k gap between the two source filings, reproduced here as each document states it rather than "
    "silently reconciled. FY2020's own filing's Statement of Changes in Equity and FY2021's own filing's FY2020 "
    "comparative column agree exactly (Distributable reserve £1,000k, Retained earnings £0k, Total £41,350k at "
    "30 April 2020) - no equivalent discrepancy at the FY2019/FY2020 boundary.\n\n"
    "ROLL-FORWARD NOTE: the Statement of Changes in Equity now opens at 'At 30 April 2019' purely as the anchoring "
    "opening balance for FY2020's own movement rows (FY2019 itself is outside this workbook's year window, one "
    "year before the confirmed floor). Before the FY2020 extension (HD-061, 2026-09-06), this sheet started "
    "directly at a row labelled 'At 1 May 2021' with no FY2021 movement detail shown at all - that row's figures "
    "(29,350/11,000/1,000/(61)/41,289) were always FY2021's own CLOSING balance, just used as a shortcut opening "
    "seed for FY2022 since FY2020/FY2021 were both then out of scope. It is now correctly split into its own "
    "'At 30 April 2021' TOTAL row with FY2021's real movements (comprehensive profit £929k, AT1 dividends payable "
    "£(990)k, no charitable donation that year) shown leading up to it - no figures changed, only the previously-"
    "collapsed roll-forward detail restored."
)

ASSET_QUALITY_SOURCES = (
    "Sources - CAF Bank Limited's own Notes to the Financial Statements (Note 10, Loans and advances to "
    f"customers, p.43 of {AR2021_URL} for FY2021's individual/collective impairment tables; p.43 of {AR2020_URL} "
    "for FY2020's own equivalent table), same filings as STATEMENTS_SOURCES above.\n"
    + ENTITY_NOTE
    + "\n\nDISCLOSURE GRANULARITY NOTE: this is an FRS 102 bank (not IFRS 9), so there is no Stage 1/2/3 split - "
    "only an individual/collective impairment provision split. FY2021's own filing (Note 10, p.43) does in fact "
    "disclose this split (Individual impairments provision closing balance £(1,376)k, Collective impairments "
    "provision closing balance £(802)k, summing to the £(2,178)k aggregate) - found on a follow-up pass after an "
    "earlier build initially left FY2021 blank, having assumed (without having actually located the note) that "
    "the split was only disclosed from FY2024 onward. FY2022/FY2023 were not re-checked in this follow-up pass "
    "for a similar split (their columns above still show the single aggregate figure only, £(1,078)k/£(1,651)k, "
    "as originally sourced) - worth a similar check if those years are revisited. FY2020's own filing (Note 10, "
    "p.43) also discloses the split directly (Individual impairments provision closing balance £(938)k, "
    "Collective impairments provision closing balance £(707)k, summing to £(1,645)k) - and independently ties to "
    "the Profit and Loss Account's own £(1,200)k loan loss provision charge for the year (£938k newly individually "
    "provided + £262k collective movement = £1,200k), a cross-check performed before transcribing."
)

# ---------------------------------------------------------------
# Sheet 1: Balance Sheet
# ---------------------------------------------------------------
balance_sheet_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Balances at Bank of England", {"FY2025": 610671, "FY2024": 630526, "FY2023": 620476, "FY2022": 602553, "FY2021": 417756, "FY2020": 327571}),
    ("DATA", "Loans and advances to banks", {"FY2025": 4214, "FY2024": 23998, "FY2023": 6116, "FY2022": 7471, "FY2021": 7897, "FY2020": 6273}),
    ("DATA", "Loans and advances to customers", {"FY2025": 219101, "FY2024": 197701, "FY2023": 177734, "FY2022": 160407, "FY2021": 124506, "FY2020": 103625}),
    ("DATA", "Total debt securities", {"FY2025": 682783, "FY2024": 637376, "FY2023": 752100, "FY2022": 777145, "FY2021": 885876, "FY2020": 771083}),
    ("DATA", "Debt securities - UK government (sovereign, amortised cost)", {"FY2021": 0, "FY2020": 63036}),
    ("DATA", "Debt securities - Multilateral financial institutions (supranational, amortised cost)", {"FY2025": 563083, "FY2024": 511053, "FY2023": 670370, "FY2022": 679925, "FY2021": 758564, "FY2020": 536545}),
    ("DATA", "Debt securities - Fixed coupon corporate bonds (amortised cost)", {"FY2025": 59570, "FY2024": 49368, "FY2023": 23498, "FY2022": 23723, "FY2021": 24093, "FY2020": 43521}),
    ("DATA", "Debt securities - Floating rate corporate bonds (amortised cost)", {"FY2025": 60130, "FY2024": 76955, "FY2023": 48232, "FY2022": 63497, "FY2021": 83398, "FY2020": 107981}),
    ("DATA", "Debt securities - Certificates of deposit (other, amortised cost)", {"FY2023": 10000, "FY2022": 10000, "FY2021": 19821, "FY2020": 20000}),
    ("DATA", "Prepayments and accrued income", {"FY2025": 11882, "FY2024": 10566, "FY2023": 8775, "FY2022": 3792, "FY2021": 4067, "FY2020": 4378}),
    ("DATA", "Intangible assets", {"FY2025": 15908, "FY2024": 10758, "FY2023": 6333, "FY2022": 4676, "FY2021": 1194}),
    ("TOTAL", "Total assets", {"FY2025": 1544559, "FY2024": 1510925, "FY2023": 1571534, "FY2022": 1556044, "FY2021": 1441296, "FY2020": 1212930}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Customer accounts", {"FY2025": 1450926, "FY2024": 1419433, "FY2023": 1505425, "FY2022": 1508937, "FY2021": 1398146, "FY2020": 1156995}),
    ("DATA", "Repurchase agreements", {"FY2025": 12394, "FY2024": 13852, "FY2023": 8852, "FY2021": 0, "FY2020": 10142}),
    ("DATA", "Other liabilities", {"FY2025": 5000, "FY2024": 7540, "FY2023": 5784, "FY2022": 4178, "FY2021": 1848, "FY2020": 4197}),
    ("DATA", "Accruals and deferred income", {"FY2021": 13, "FY2020": 246}),
    ("DATA", "Subordinated debt", {"FY2024": 5000}),
    ("TOTAL", "Total liabilities", {"FY2025": 1468320, "FY2024": 1445825, "FY2023": 1520061, "FY2022": 1513115, "FY2021": 1400007, "FY2020": 1171580}),
    ("SECTION", "Shareholders' funds", {}),
    ("DATA", "Called up share capital", {"FY2025": 40319, "FY2024": 40319, "FY2023": 40319, "FY2022": 29350, "FY2021": 29350, "FY2020": 29350}),
    ("DATA", "Additional Tier 1 capital", {"FY2022": 11000, "FY2021": 11000, "FY2020": 11000}),
    ("DATA", "Distributable reserve", {"FY2022": 1000, "FY2021": 939, "FY2020": 1000}),
    ("DATA", "Retained earnings", {"FY2025": 35920, "FY2024": 24781, "FY2023": 11154, "FY2022": 1579, "FY2021": -61, "FY2020": 0}),
    ("TOTAL", "Total shareholders' funds", {"FY2025": 76239, "FY2024": 65100, "FY2023": 51473, "FY2022": 42929, "FY2021": 41289, "FY2020": 41350}),
    ("TOTAL", "Total liabilities and shareholders' funds", {"FY2025": 1544559, "FY2024": 1510925, "FY2023": 1571534, "FY2022": 1556044, "FY2021": 1441296, "FY2020": 1212930}),
]

bw.add_balance_sheet_sheet(
    title="CAF Bank Limited — Balance Sheet",
    subtitle="CAF Bank Limited's own basis, £'000. See source note at bottom.",
    rows=balance_sheet_rows,
    sources_text=STATEMENTS_SOURCES + "\n\n" + DEBT_SECURITIES_BREAKDOWN_NOTE,
    first_col_width=88,
    source_height=420,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Sheet 2: Profit & Loss
# ---------------------------------------------------------------
income_statement_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest receivable", {"FY2025": 66478, "FY2024": 65025, "FY2023": 35396, "FY2022": 10823, "FY2021": 10059, "FY2020": 12534}),
    ("DATA", "Interest payable", {"FY2025": -20929, "FY2024": -20250, "FY2023": -7350, "FY2022": -182, "FY2021": -263, "FY2020": -1035}),
    ("TOTAL", "Net interest income", {"FY2025": 45549, "FY2024": 44775, "FY2023": 28046, "FY2022": 10641, "FY2021": 9796, "FY2020": 11499}),
    ("DATA", "Fees and commissions receivable", {"FY2025": 2744, "FY2024": 2710, "FY2023": 2560, "FY2022": 2947, "FY2021": 2230, "FY2020": 2109}),
    ("DATA", "Fees and commissions payable", {"FY2025": -989, "FY2024": -945, "FY2023": -913, "FY2022": -885, "FY2021": -815, "FY2020": -1008}),
    ("TOTAL", "Net fee income", {"FY2025": 1755, "FY2024": 1765, "FY2023": 1647, "FY2022": 2062, "FY2021": 1415, "FY2020": 1101}),
    ("TOTAL", "Net operating income", {"FY2025": 47304, "FY2024": 46540, "FY2023": 29693, "FY2022": 12703, "FY2021": 11211, "FY2020": 12600}),
    ("SECTION", "Expenses", {}),
    ("DATA", "Administrative expenses", {"FY2025": -32827, "FY2024": -27655, "FY2023": -18472, "FY2022": -11774, "FY2021": -9763, "FY2020": -10109}),
    ("DATA", "Loan loss provision credit/(charge)", {"FY2025": 184, "FY2024": -716, "FY2023": -573, "FY2022": 1100, "FY2021": -533, "FY2020": -1200}),
    ("TOTAL", "Profit on ordinary activities before taxation", {"FY2025": 14661, "FY2024": 18169, "FY2023": 10648, "FY2022": 2029, "FY2021": 915, "FY2020": 1291}),
    ("DATA", "Tax on profit on ordinary activities", {"FY2025": -2522, "FY2024": -4542, "FY2023": -2073, "FY2022": -389, "FY2021": 14, "FY2020": -1}),
    ("TOTAL", "Profit on ordinary activities after taxation", {"FY2025": 12139, "FY2024": 13627, "FY2023": 8575, "FY2022": 1640, "FY2021": 929, "FY2020": 1290}),
    ("TOTAL", "Total comprehensive income for the year, net of tax", {"FY2025": 12139, "FY2024": 13627, "FY2023": 8575, "FY2022": 1640, "FY2021": 929, "FY2020": 1290}),
]

bw.add_income_statement_sheet(
    title="CAF Bank Limited — Profit & Loss",
    subtitle="CAF Bank Limited's own basis, £'000. No OCI - there are no recognised gains or losses in any "
              "year other than those shown in the profit and loss account (per the Bank's own disclosure). See "
              "source note at bottom.",
    rows=income_statement_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=88,
    source_height=280,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Sheet 3: Statement of Changes in Equity
# ---------------------------------------------------------------
equity_headers = ["Called-up share capital", "Additional Tier 1 securities", "Distributable reserve", "Retained earnings", "Total"]
equity_rows = [
    ("TOTAL", "At 30 April 2019", (29350, 11000, 1000, 0, 41350)),
    ("DATA", "Total comprehensive profit for the financial year", (None, None, None, 1290, 1290)),
    ("DATA", "Charitable donation to parent", (None, None, None, -297, -297)),
    ("DATA", "AT1 dividends payable", (None, None, None, -993, -993)),
    ("TOTAL", "At 30 April 2020", (29350, 11000, 1000, 0, 41350)),
    ("DATA", "Total comprehensive profit for the financial year", (None, None, None, 929, 929)),
    ("DATA", "AT1 dividends payable", (None, None, None, -990, -990)),
    ("TOTAL", "At 30 April 2021", (29350, 11000, 1000, -61, 41289)),
    ("DATA", "Total comprehensive profit for the financial year", (None, None, None, 1640, 1640)),
    ("TOTAL", "At 30 April 2022", (29350, 11000, 1000, 1579, 42929)),
    ("DATA", "Total comprehensive profit for the financial year", (None, None, None, 8575, 8575)),
    ("DATA", "Transferred from distributable reserve", (None, None, -1000, 1000, 0)),
    ("DATA", "Redemption of additional tier 1 securities", (None, -11000, None, None, -11000)),
    ("DATA", "Issue of share capital", (10969, None, None, None, 10969)),
    ("TOTAL", "At 30 April 2023", (40319, 0, 0, 11154, 51473)),
    ("DATA", "Profit on ordinary activities after taxation for the financial year", (None, None, None, 13627, 13627)),
    ("TOTAL", "At 30 April 2024", (40319, 0, 0, 24781, 65100)),
    ("DATA", "Profit on ordinary activities after taxation for the financial year", (None, None, None, 11139, 11139)),
    ("TOTAL", "At 30 April 2025", (40319, 0, 0, 35920, 76239)),
]

bw.add_equity_changes_sheet(
    title="CAF Bank Limited — Statement of Changes in Equity",
    subtitle="CAF Bank Limited's own basis, £'000, chronological (oldest to newest). See source note at bottom.",
    headers=equity_headers,
    rows=equity_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=58,
    source_height=280,
)

# ---------------------------------------------------------------
# Sheet: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Cash flows from operating activities", {}),
    ("DATA", "Profit on ordinary activities", {"FY2025": 14661, "FY2024": 18169, "FY2023": 8575, "FY2022": 1640, "FY2021": 929, "FY2020": 1291}),
    ("DATA", "Amortisation of investments", {"FY2025": -6041, "FY2024": -2450, "FY2023": 344, "FY2022": 1170, "FY2021": 21919, "FY2020": 2451}),
    ("DATA", "Corporation tax paid", {"FY2025": -1705, "FY2024": -5815, "FY2023": -830, "FY2021": None, "FY2020": 0}),
    ("DATA", "(Increase)/decrease in prepayments and accrued income", {"FY2025": -1316, "FY2024": -1791, "FY2023": -4982, "FY2022": 275, "FY2021": 311, "FY2020": 206}),
    ("DATA", "(Decrease)/increase in accruals and deferred income", {"FY2021": -98, "FY2020": 4}),
    ("DATA", "Increase/(decrease) in Cash Ratio Deposit with the Bank of England", {"FY2024": 3582, "FY2023": -369, "FY2022": -918, "FY2021": -828, "FY2020": -242}),
    ("DATA", "Decrease in loans and advances to banks", {"FY2021": 0, "FY2020": 0}),
    ("DATA", "(Increase) in loans and advances to customers", {"FY2025": -21216, "FY2024": -20683, "FY2023": -17900, "FY2022": -34801, "FY2021": -21414, "FY2020": -14363}),
    ("DATA", "Increase/(decrease) in loan loss provision", {"FY2025": -184, "FY2024": 716, "FY2023": 573, "FY2022": -1100, "FY2021": 533, "FY2020": 1200}),
    ("DATA", "Increase/(decrease) in customer accounts", {"FY2025": 31493, "FY2024": -85992, "FY2023": -3512, "FY2022": 110791, "FY2021": 241151, "FY2020": 122767}),
    ("DATA", "Increase in other liabilities", {"FY2025": 5037, "FY2024": 3028, "FY2023": 2435, "FY2022": 2317, "FY2021": -2052, "FY2020": 2335}),
    ("TOTAL", "Net cash generated from/(used in) operating activities", {"FY2025": 20729, "FY2024": -91236, "FY2023": -15666, "FY2022": 79374, "FY2021": 240451, "FY2020": 115649}),
    ("SECTION", "Cash flows from investing activities", {}),
    ("DATA", "Acquisitions of debt securities", {"FY2025": -156964, "FY2024": -254111, "FY2023": -88130, "FY2022": -228836, "FY2021": -293668, "FY2020": -514420}),
    ("DATA", "Redemptions of debt securities", {"FY2025": 115598, "FY2024": 371286, "FY2023": 112831, "FY2022": 336397, "FY2021": 156956, "FY2020": 408809}),
    ("DATA", "Disposals of debt securities", {"FY2021": 0, "FY2020": 2163}),
    ("DATA", "Net proceeds/(repayments) from repurchase agreements", {"FY2025": -13852, "FY2024": 5000, "FY2023": 8852, "FY2021": -10142}),
    ("DATA", "Acquisition of intangible assets", {"FY2025": -5150, "FY2024": -4425, "FY2023": -1657, "FY2022": -3482, "FY2021": -1194}),
    ("DATA", "Proceeds from subordinated debt", {"FY2024": 15000}),
    ("DATA", "Repayment of subordinated debt", {"FY2024": -10000}),
    ("TOTAL", "Net cash generated from/(used in) investing activities", {"FY2025": -60368, "FY2024": 122750, "FY2023": 31896, "FY2022": 104079, "FY2021": -148048, "FY2020": -103448}),
    ("SECTION", "Cash flows from financing activities", {}),
    ("DATA", "Costs of redemption of additional tier 1 securities and exchange for ordinary share capital", {"FY2023": -31}),
    ("DATA", "Charitable donations paid", {"FY2021": -297, "FY2020": -4908}),
    ("DATA", "AT1 dividend paid", {"FY2021": -1126, "FY2020": -858}),
    ("TOTAL", "Net cash used in financing activities", {"FY2025": 0, "FY2024": 0, "FY2023": -31, "FY2022": 0, "FY2021": -1423, "FY2020": -5766}),
    ("TOTAL", "Change in cash and cash equivalents in the year", {"FY2025": -39639, "FY2024": 31514, "FY2023": 16199, "FY2022": 183453, "FY2021": 90980, "FY2020": 6435}),
    ("DATA", "Cash and cash equivalents at beginning of year", {"FY2025": 654524, "FY2024": 623010, "FY2023": 606811, "FY2022": 423358, "FY2021": 332378, "FY2020": 325943}),
    ("TOTAL", "Cash and cash equivalents at end of year", {"FY2025": 614885, "FY2024": 654524, "FY2023": 623010, "FY2022": 606811, "FY2021": 423358, "FY2020": 332378}),
    ("SECTION", "Represented by:", {}),
    ("DATA", "Balances at Bank of England repayable on demand", {"FY2025": 610671, "FY2024": 630526, "FY2023": 616894, "FY2022": 599340, "FY2021": 415461, "FY2020": 326105}),
    ("DATA", "Loans and advances to banks repayable on demand", {"FY2025": 4214, "FY2024": 23998, "FY2023": 6116, "FY2022": 7471, "FY2021": 7897, "FY2020": 6273}),
]

bw.add_cash_flow_sheet(
    title="CAF Bank Limited — Cash Flow Statement",
    subtitle="CAF Bank Limited's own basis, £'000. See source note at bottom.",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=88,
    source_height=320,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Sheet: Asset Quality
# ---------------------------------------------------------------
asset_quality_rows = [
    ("SECTION", "Loan book", {}),
    ("DATA", "Loans and advances to customers, net", {"FY2025": 219101, "FY2024": 197701, "FY2023": 177734, "FY2022": 160407, "FY2021": 124506, "FY2020": 103625}),
    ("SECTION", "Loan loss provision (FRS 102 - no IFRS 9 stage split)", {}),
    ("DATA", "Individual impairment provision, closing balance", {"FY2025": -1021, "FY2024": -552, "FY2021": -1376, "FY2020": -938}),
    ("DATA", "Collective impairment provision, closing balance", {"FY2025": -1162, "FY2024": -1815, "FY2021": -802, "FY2020": -707}),
    ("TOTAL", "Total loan loss provision, closing balance", {"FY2025": -2183, "FY2024": -2367, "FY2023": -1651, "FY2022": -1078, "FY2021": -2178, "FY2020": -1645}),
    ("DATA", "Loan loss provision credit/(charge) for the year", {"FY2025": 184, "FY2024": -716, "FY2023": -573, "FY2022": 1100, "FY2021": -533, "FY2020": -1200}),
]

bw.add_asset_quality_sheet(
    title="CAF Bank Limited — Asset Quality",
    subtitle="CAF Bank Limited's own basis, £'000. FRS 102 incurred-loss bank (not IFRS 9) - individual/"
              "collective split disclosed FY2020/FY2021/FY2024/FY2025; FY2022/FY2023 only an aggregate was "
              "sourced. See source note at bottom.",
    rows=asset_quality_rows,
    sources_text=ASSET_QUALITY_SOURCES,
    first_col_width=88,
    source_height=260,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets — corrected 2026-09-05: real data exists, see
# PILLAR3_SOURCES/ENTITY_NOTE above for how the original "not publicly
# disclosed" finding was wrong and what changed.
# ---------------------------------------------------------------
def metric(name, unit, rows_data, note=None):
    bw.add_metric_sheet(name, unit, rows_data, PILLAR3_SOURCES, note=note, first_col_width=54, source_height=320)

# FY2025 cells on the sheets below are written explicitly rather than left
# blank. A blank cell cannot be told apart from an unresearched gap and gets
# re-chased indefinitely; "Not publicly disclosed" records that the search was
# done and came back empty. See FY2025_NO_STANDALONE_NOTE for the evidence and
# the SDDT DATE TEST in ENTITY_NOTE for why this is labelled as non-disclosure
# rather than as a structural exemption.
NOT_DISCLOSED = "Not publicly disclosed"
NOT_APPLICABLE = "Not applicable"
# GA-020 outcome vocabulary (2026-09-19): every statement cell names its evidence.
FY25_NOT_PUBLISHED = ("Not published – no FY2025 Pillar 3 exists (bank's Pillar 3 page: 'not required to publish'); "
                      "FY2025 Annual Report 'Key regulatory ratios' (p.28) gives only total capital, leverage, LCR")
LEV_INCL_FY24 = ("Not published – FY2024 Pillar 3 UK LRCom prints the incl.-central-banks exposure (row 24, "
                 "1,531,996) but no ratio on that basis")
LEV_INCL_FY25 = ("Not published – FY2025 Annual Report Strategic Report (pp.27-28) gives the excl.-central-banks "
                 "ratio only; no FY2025 Pillar 3 exists")
LCR_FY2020 = ("Not published – FY2020 Pillar 3 (27pp, full read) has no LCR, and no later edition prints an "
              "April 2020 LCR")
NSFR_NA = ("Not applicable – UK NSFR in force only from 1 Jan 2022 (PRA PS17/21), after this 30 April year-end; "
           "FY2022 edition's KM1 prints the 2021 NSFR cells blank")
MREL_NP = ("Not published – no MREL figure in CAF's Pillar 3 FY2020-FY2024 (text-searched 2026-09-19; only UK CCA "
           "template labels); FY2025 AR 'Key regulatory ratios' (p.28) has none")

FY2025_NO_STANDALONE_NOTE = (
    "FY2025 reads 'Not publicly disclosed' rather than sitting blank: the absence is evidenced, not unchecked. No "
    "standalone FY2025 Pillar 3 document exists (searched across both of this bank's known Pillar 3 folders on "
    "cafonline.org, which return a 136kB HTML soft-404 at HTTP 200 for every plausible filename while the FY2024 "
    "file in the same folder still serves a real 1.4MB PDF - so the absence is genuine and not a site outage), "
    "and the metric is absent from the FY2025 Annual Report too, confirmed by a full-document OCR search of all "
    "51 pages. NOTE THE LABEL IS DELIBERATE: this is recorded as non-disclosure and NOT as an SDDT structural "
    "exemption, because CAF Bank's Rule 3.1 modification starts 08/08/2025 while FY2025 ended 30 April 2025, "
    "three months earlier - see the SDDT DATE TEST in the Entity Note, whose outcome is explicitly UNDETERMINED "
    "and must not be quietly resolved in either direction."
)

# ---------------------------------------------------------------
# KM1 Key Metrics - CAF Bank's own "Key metrics (Template UK KM1)", which it
# names as the template explicitly, reproduced whole.
#
# WHICH EDITION EACH COLUMN COMES FROM (rule 1 - each year from the edition
# where that year is the REPORTING year, never a later comparative):
#   FY2024 <- Pillar 3 Report 2023/24, Template UK KM1, printed p.8 (PDF p.5)
#   FY2023 <- Pillar 3 Report 2022/23, Template UK KM1, printed p.6 (PDF p.4)
#   FY2022 <- Pillar 3 Disclosure 30 April 2022, Template UK KM1, p.5
#   FY2021 <- the FY2022 edition's own 2021 COMPARATIVE column. The FY2021
#             edition carries no KM1 at all (see below), so this is the only
#             UK-template 30-April-2021 column CAF Bank ever printed.
#   FY2025, FY2020 <- blank, each on positive evidence, see below.
#
# UNITS ARE £000 IN EVERY EDITION - no rule-17 unit break at this bank, and
# each edition states "£000" under its own year headings.
#
# ROW SET - CAF PRINTS A REDUCED SET, IDENTICALLY IN ALL THREE EDITIONS.
# Present: 1, 2, 3, 4, 5, 6, 7, UK 7a-7d, 8, 9, 11, UK 11a, 12, 13, 14, 15,
# UK 16a, UK 16b, 16, 17, 18, 19, 20. Absent from EVERY edition: UK 8a, UK 9a,
# 10, UK 10a and the whole 14a-14f additional-leverage block. Those rows are
# not blank here - they do not appear at all, because the bank never printed
# them (map rule 4: a row the bank did not print is not the same as a row we
# failed to find, so this note says which).
#
# THE FY2021 AND FY2020 EDITIONS PUBLISH PILLAR 3 BUT DO NOT USE THIS
# TEMPLATE (map rule 8, second limb). Both are CRD IV-era documents - each
# says so in its own opening paragraph - and their capital section is a
# bespoke three-block table headed "Total Capital Resources / Total Capital
# Requirement / Capital Surplus", with CET1 / Total T1 / Total Capital as its
# only rows, each shown as a £000 amount beside a %. No row numbers, no SREP
# rows, no buffer rows, no LCR, no NSFR. That is a different and much shorter
# table, not an unnumbered KM1, and mapping it onto template row numbers would
# invent a correspondence CAF never published. Established positively:
#   - each document's OWN contents list (map rule 16 - anchor on the
#     document's structure, never on digit density) was read and followed to
#     the named page: FY2020 "Overview of capital position versus capital
#     requirement ... 5", FY2021 the same section at p.4;
#   - extraction is RICH, so the zeroes are facts about the documents rather
#     than about the tool (map rule 15): FY2021 scores 120 hits for "capital",
#     77 for "ratio", 24 for "leverage", 19 for "buffer", 10 for "CET1", and
#     FY2020 scores 110/61/16/17/7 - against 0 hits in BOTH for "KM1", "key
#     metric", "SREP", "risk-weighted" and "liquidity coverage";
#   - images were enumerated because a table can be a picture inside an
#     otherwise text-native PDF (map rule 13): the FY2020 file contains NO
#     images at all, and the FY2021 file's only image is the 2484x3388 cover
#     photograph on page 1. There is no page where a table could be hiding.
# The UK KM1 template arrived with the Disclosure (CRR) Part of the PRA
# Rulebook on 1 January 2022; CAF Bank's year-end is 30 April, so FY2021
# (ended 30 April 2021) and FY2020 (ended 30 April 2020) both close before it
# existed. FY2022, ending 30 April 2022, is the first year after it and is
# exactly where the template first appears - the boundary falls where the
# rulebook predicts.
#
# FY2025 HAS NO PILLAR 3 DOCUMENT AT ALL, re-verified 2026-09-16; see the
# latest-edition note in KM1_SOURCES. Left blank on this sheet rather than
# "Not publicly disclosed": there is no KM1 template to reproduce, which is a
# different statement from a template that omits a row.
#
# GLYPHS, read off a 150 dpi rendering of the page and not off the text layer
# (map rule 2 - a dash is not a zero): there is not one dash anywhere in this
# bank's KM1 in any edition. Rows UK 7a, UK 7b, UK 7c and 9 print "0.0%" or
# "0.00%" - measured zeros, kept as zeros. The only empty cells in the whole
# series are the FY2021 column's NSFR rows 18-20, which are visibly blank with
# no glyph: the UK NSFR requirement took effect on 1 January 2022, after that
# year ended, so there was no ratio to print.
# ---------------------------------------------------------------
km1_rows = [
    ("SECTION", "Available own funds (amounts)", {}),
    ("DATA", "1    Common Equity Tier 1 (CET1) capital (£'000)",
     {"FY2024": 54342, "FY2023": 45140, "FY2022": 27253, "FY2021": 29095}),
    ("DATA", "2    Tier 1 capital (£'000)",
     {"FY2024": 54342, "FY2023": 45140, "FY2022": 38253, "FY2021": 40095}),
    ("DATA", "3    Total capital (£'000)",
     {"FY2024": 56157, "FY2023": 45140, "FY2022": 38253, "FY2021": 40095}),
    ("SECTION", "Risk-weighted exposure amounts", {}),
    # FY2025 carries a recorded absence rather than a blank (2026-09-19). Row 4
    # is chosen because the Total RWAs sheet already holds a text cell for
    # FY2025, so no verifier comparison exists here to lose. The wording
    # deliberately does NOT assert that the SDDT opt-in explains FY2025 - the
    # date test below is UNDETERMINED, because the 30 April 2025 year end
    # precedes the 08/08/2025 modification by three months.
    ("DATA", "4    Total risk-weighted exposure amount (£'000)",
     {"FY2025": "Not published - no FY2025 edition exists; SDDT date fit undetermined",
      "FY2024": 185123, "FY2023": 146334, "FY2022": 124243, "FY2021": 127844}),
    ("SECTION", "Capital ratios (as a percentage of risk-weighted exposure amount)", {}),
    ("DATA", "5    Common Equity Tier 1 ratio (%)",
     {"FY2024": "29.35%", "FY2023": "30.8%", "FY2022": "21.9%", "FY2021": "22.8%"}),
    ("DATA", "6    Tier 1 ratio (%)",
     {"FY2024": "29.35%", "FY2023": "30.8%", "FY2022": "30.8%", "FY2021": "31.4%"}),
    ("DATA", "7    Total capital ratio (%)",
     {"FY2024": "30.33%", "FY2023": "30.8%", "FY2022": "30.8%", "FY2021": "31.4%"}),
    ("SECTION", "Additional own funds requirements based on SREP (as a percentage of risk-weighted "
                "exposure amount)", {}),
    ("DATA", "UK 7a    Additional CET1 SREP requirements (%)",
     {"FY2024": "0.00%", "FY2023": "0.0%", "FY2022": "0.0%", "FY2021": "0.0%"}),
    ("DATA", "UK 7b    Additional AT1 SREP requirements (%)",
     {"FY2024": "0.00%", "FY2023": "0.0%", "FY2022": "0.0%", "FY2021": "0.0%"}),
    ("DATA", "UK 7c    Additional T2 SREP requirements (%)",
     {"FY2024": "0.00%", "FY2023": "0.0%", "FY2022": "0.0%", "FY2021": "0.0%"}),
    ("DATA", "UK 7d    Total SREP own funds requirements (%)",
     {"FY2024": "8.00%", "FY2023": "8.0%", "FY2022": "8.0%", "FY2021": "8.0%"}),
    ("SECTION", "Combined buffer requirements (as a percentage of risk-weighted exposure amount)", {}),
    ("DATA", "8    Capital conservation buffer (%)",
     {"FY2024": "2.50%", "FY2023": "2.5%", "FY2022": "2.5%", "FY2021": "2.5%"}),
    ("DATA", "9    Institution specific countercyclical capital buffer (%)",
     {"FY2024": "2.00%", "FY2023": "1.0%", "FY2022": "0.0%", "FY2021": "0.0%"}),
    ("DATA", "11    Combined buffer requirement (%)",
     {"FY2024": "4.50%", "FY2023": "3.5%", "FY2022": "2.5%", "FY2021": "2.5%"}),
    ("DATA", "UK 11a    Overall capital requirements (%)",
     {"FY2024": "12.50%", "FY2023": "11.5%", "FY2022": "10.5%", "FY2021": "10.5%"}),
    ("DATA", "12    CET1 available after meeting the total SREP own funds requirements (%)",
     {"FY2024": "22.33%", "FY2023": "22.8%", "FY2022": "22.8%", "FY2021": "23.4%"}),
    ("SECTION", "Leverage ratio", {}),
    ("DATA", "13    Total exposure measure excluding claims on central banks (£'000)",
     {"FY2024": 897612, "FY2023": 972360, "FY2022": 963904, "FY2021": 1044543}),
    ("DATA", "14    Leverage ratio excluding claims on central banks (%)",
     {"FY2024": "6.05%", "FY2023": "4.64%", "FY2022": "3.97%", "FY2021": "3.84%"}),
    ("SECTION", "Liquidity coverage ratio", {}),
    ("DATA", "15    Total high quality liquid assets (HQLA) (Weighted average value) (£'000)",
     {"FY2024": 1150942, "FY2023": 1244786, "FY2022": 1255456, "FY2021": 1130354}),
    ("DATA", "UK 16a    Cash outflows - total weighted value (£'000)",
     {"FY2024": 449191, "FY2023": 483494, "FY2022": 477707, "FY2021": 435790}),
    ("DATA", "UK 16b    Cash inflows - total weighted value (£'000)",
     {"FY2024": 1605, "FY2023": 4690, "FY2022": 1523, "FY2021": 14140}),
    ("DATA", "16    Total net cash outflows (adjusted value) (£'000)",
     {"FY2024": 447586, "FY2023": 478804, "FY2022": 476184, "FY2021": 421650}),
    ("DATA", "17    Liquidity coverage ratio (%)",
     {"FY2024": "257%", "FY2023": "260%", "FY2022": "264%", "FY2021": "268%"}),
    ("SECTION", "Net stable funding ratio", {}),
    ("DATA", "18    Total available stable funding (£'000)",
     {"FY2024": 1377360, "FY2023": 1429893, "FY2022": 1426183}),
    ("DATA", "19    Total required stable funding (£'000)",
     {"FY2024": 272188, "FY2023": 154418, "FY2022": 177361}),
    ("DATA", "20    NSFR ratio (%)",
     {"FY2024": "506%", "FY2023": "926%", "FY2022": "804%"}),
]

KM1_SOURCES = (
    "Sources - CAF Bank Limited's own \"Key metrics (Template UK KM1)\", solo basis, fiscal year-end 30 "
    "April, reproduced whole in the bank's own row order, numbering, labels and printed precision. CAF "
    "names the template explicitly in its own heading, so no presence judgement was needed. Each column "
    "is taken from the edition in which that year is the REPORTING year, with the one flagged exception "
    "of FY2021:\n"
    f"FY2024: Pillar 3 Report 2023/24, Template UK KM1, printed p.8 (PDF p.5), column '2024' - "
    f"{P3_2024_URL}\n"
    f"FY2023: Pillar 3 Report 2022/23, Template UK KM1, printed p.6 (PDF p.4), column '2023' - "
    f"{P3_2023_URL}\n"
    f"FY2022: CAF Bank Ltd Pillar 3 Disclosure 30 April 2022, Template UK KM1, p.5, column '2022' - "
    f"{P3_2022_URL}\n"
    f"FY2021: CAF Bank Ltd Pillar 3 Disclosure 30 April 2022, Template UK KM1, p.5, COMPARATIVE column "
    f"'2021' - {P3_2022_URL}. This is the only comparative column on the sheet and it is unavoidable: the "
    "FY2021 edition publishes no KM1 at all (see below), so the FY2022 edition's 2021 column is the only "
    "UK-template 30-April-2021 column CAF Bank has ever printed. Its divergences from the FY2021 "
    "edition's own figures are set out below rather than smoothed over.\n"
    "FY2025 and FY2020: BLANK, each for a documented reason given below - not for want of searching.\n\n"
    "KM1 presentation notes:\n"
    "• UNITS: £000 in every edition, stated by the bank under its own year headings. No unit break "
    "anywhere in this series, so every amount row carries a single caption.\n"
    "• BASIS: solo throughout - the bank states 'prepared on a solo basis' in each edition's opening "
    "section. No edition prints a second entity column, so the solo-beside-consolidated trap does not "
    "arise here.\n"
    "• ROW SET - CAF PRINTS A REDUCED SET, IDENTICALLY IN ALL THREE EDITIONS, with no drift. Present: 1, "
    "2, 3, 4, 5, 6, 7, UK 7a-7d, 8, 9, 11, UK 11a, 12, 13, 14, 15, UK 16a, UK 16b, 16, 17, 18, 19, 20. "
    "ABSENT FROM EVERY EDITION, and therefore absent here rather than shown blank: UK 8a, UK 9a, 10, UK "
    "10a and the entire 14a-14f additional-leverage block. That is a row the bank never printed, which is "
    "a different thing from a row we failed to find - hence this list.\n"
    "• A DASH IS NOT A ZERO, AND THERE IS NOT ONE DASH IN THIS TABLE IN ANY EDITION. The page was "
    "rendered at 150 dpi and read as an image rather than trusted to its text layer. Rows UK 7a, UK 7b, "
    "UK 7c and row 9 print '0.0%' (FY2021-FY2023) or '0.00%' (FY2024) - measured zeros, kept as zeros. "
    "The only empty cells in the whole series are the FY2021 column's NSFR rows 18-20, which are visibly "
    "blank with no glyph of any kind: the UK NSFR requirement took effect on 1 January 2022, after that "
    "year had ended, so there was no ratio to print. That is a structural absence and must never be "
    "back-filled.\n"
    "• PRECISION DRIFTS BETWEEN EDITIONS AND IS KEPT AS EACH EDITION PRINTED IT. The FY2022 and FY2023 "
    "editions print capital and buffer ratios to ONE decimal place (30.8%, 8.0%, 2.5%) while the FY2024 "
    "edition prints the same rows to TWO (30.33%, 8.00%, 2.50%); leverage is two decimals in all three. "
    "This is the bank's own house style changing, not an inconsistency to normalise.\n"
    "• SECTION CAPTION CHANGE, reproduced as a finding rather than merged: the FY2024 edition heads the "
    "LCR block 'Liquidity coverage ratio (Last 3 months average)' where the FY2022 and FY2023 editions "
    "head it simply 'Liquidity coverage ratio'. The averaging basis is stated only in the later edition; "
    "no basis break is asserted here that the bank did not print.\n"
    "• NO LEVERAGE BASIS BREAK WITHIN THIS SHEET. Rows 13/14 are captioned 'excluding claims on central "
    "banks' in every edition that prints the template. The 1 January 2022 basis break is real for this "
    "bank but falls BEFORE this sheet's first own-edition column: the Leverage Ratio metric sheet carries "
    "both bases on their own separate rows for FY2020-FY2023 and must be read there, not inferred from "
    "this one.\n\n"
    "INTER-EDITION DIVERGENCE ON THE FY2021 COLUMN - RECORDED IN FULL, NOT ADOPTED, AND THE REASON THIS "
    "WORKBOOK'S KM1-vs-METRIC-SHEET CROSS-CHECK REPORTS ONE DELIBERATE DISAGREEMENT. The FY2022 edition "
    "restates FY2021 in three places without marking it as restated:\n"
    "   (1) ROW 14, LEVERAGE RATIO. This sheet shows 3.84%, which is what the FY2022 edition's KM1 prints "
    "in its 2021 column (and its template UK LR2 row 25 agrees). THE FY2021 EDITION'S OWN 'UK Leverage "
    "Ratio' table prints 3.81%, on Tier 1 resources of GBP40,095k over a leverage exposure of "
    "GBP1,052,245k. The FY2022 edition arrives at 3.84% because it restates that exposure DOWN to "
    "GBP1,044,543k (row 13 above) on the same GBP40,095k of Tier 1 - 40,095/1,052,245 = 3.810% against "
    "40,095/1,044,543 = 3.838%. Both figures are the bank's own, for the same date, on the same "
    "excluding-central-banks basis; neither is a transcription slip. The Leverage Ratio metric sheet "
    "carries 3.81% because it follows this project's convention of using each year's own "
    "originally-published figure, so the automated cross-check flags row 14 FY2021 as a disagreement. "
    "THAT DISAGREEMENT IS EXPECTED AND CORRECT: it is a restated comparative meeting an as-published "
    "figure, and neither side has been altered to make the two agree.\n"
    "   (2) ROW 4, TOTAL RWA. This sheet shows 127,844 as the FY2022 edition printed it; the FY2021 "
    "edition's own figure is 127,881, which is what the Total RWAs metric sheet carries. A GBP37k "
    "difference, within the cross-check's tolerance, so it does not flag - recorded here anyway so it is "
    "not mistaken later for agreement.\n"
    "   (3) The same edition's template UK LR2 row 25c restates FY2021's INCLUDING-central-banks leverage "
    "ratio to 2.74% against the FY2021 edition's own 2.72%. That row is not part of the KM1 template and "
    "so does not appear on this sheet, but it is the same restatement showing through on the other basis, "
    "and the Leverage Ratio metric sheet already records it.\n\n"
    "LATEST-EDITION CHECK 2026-09-16 - CHECKED, NONE NEWER. Two independent checks:\n"
    "   (a) PILLAR 3. No FY2025 or FY2026 Pillar 3 document exists. Both of this bank's known Pillar 3 "
    "folders on its own site were probed directly with a browser user-agent - "
    "/docs/default-source/about-us-governance/ (caf_bank_pillar3_2025.pdf, caf_bank_pillar3_2026.pdf) and "
    "/docs/default-source/annual-reports/ (caf-bank-pillar-3-disclosure-2024_2025.pdf, "
    "...-2025_2026.pdf) - and every one returns an HTTP 302 redirect into the site's soft-404 page, while "
    "THE FY2024 FILE IN THE SAME FOLDER STILL SERVES A REAL 1,401,132-BYTE application/pdf WITH %PDF "
    "MAGIC BYTES. That control is the point: the negative is a fact about those filenames, not a site "
    "outage and not a blocked fetch. cafonline.org also no longer serves a sitemap (its /sitemap.xml is "
    "itself a 404) and its governance pages now 301/404, so the file-level probe against a live control "
    "is the strongest available check.\n"
    "   (a2) THE BANK'S OWN PILLAR 3 INDEX PAGE, READ 2026-09-18 - the check (a) above was missing, and this "
    "supplies it. Check (a) probed FILENAMES under two folders, which is a guess-set and not an enumeration (the "
    "same error that hid Arbuthnot Banking Group's FY2025 annual Pillar 3 for a week). The real index is "
    "https://www.cafonline.org/home/caf-bank/about-us/legal-information/pillar-3-disclosure (HTTP 200, "
    "text/html, 42,404 bytes, reached with a browser user-agent over HTTP/1.1 after following redirects). It "
    "carries NO document links of any kind - zero hrefs to any .pdf, its only 'pillar' href being its own "
    "canonical self-link - and its entire body text under 'Legal information' reads: 'CAF Bank has become part "
    "of the PRA's SDDT (\"Small Domestic Deposit Taker\") regime under which, as a non-listed institution, the "
    "Bank is not required to publish a Pillar 3 report.' That is the bank stating the absence itself, on the "
    "page whose job is to host the document, and it is far stronger evidence than any filename probe. It still "
    "does not date the change, so the FY2025 date test below is UNCHANGED and still unresolved.\n"
    "   (b) ANNUAL REPORT. Companies House filing history for CAF Bank Limited (01837656) was read in "
    "full on 2026-09-16: the newest accounts filing is 'Full accounts made up to 30 April 2025', filed 10 "
    "Feb 2026, 51 pages - which this workbook already cites. There is NO FY2026 filing (year ending 30 "
    "April 2026); the most recent filings after it are Memorandum and Articles (04 Aug 2026), a "
    "resolution, and director/secretary appointments. Since the FY2025 accounts themselves took until "
    "February 2026 to file, an FY2026 filing is not yet due. So YEARS is unchanged at FY2025-FY2020.\n\n"
    "FY2026 RE-CHECK 2026-09-19 - STILL NONE; NO FY2026 COLUMN ADDED. Routes and results: (1) Companies House, "
    "UNFILTERED filing history for 01837656, page 1 (which reaches back to July 2025, so it spans the whole "
    "window in which an FY2026 filing could appear): newest accounts entry is still 'Full accounts made up to 30 "
    "April 2025' (10 Feb 2026); everything later is non-accounts (MA and RES01 04 Aug 2026, AP03 21 Jul 2026, "
    "AP01 22 Jun 2026, CS01 01 Apr 2026). (2) The bank's own site: the CAF Bank 'Legal information' page "
    "(https://www.cafonline.org/home/caf-bank/about-us/legal-information, HTTP 200, 62,847 bytes) links annual "
    "reports, and its newest, /docs/default-source/annual-reports/caf_bank_annual-report.pdf (HTTP 200, "
    "application/pdf, %PDF, 8,300,402 bytes, 51 pages), is the report for the year ended 30 April 2025 "
    "(title page; PDF created 12 Aug 2025) - the edition already cited. The Pillar 3 index page is unchanged "
    "(the SDDT sentence, no document links). FY2026 variants of the known filenames "
    "(annual-reports/caf-bank-annual-report-2025_2026.pdf and -2024_2025.pdf, "
    "caf-bank-pillar-3-disclosure-2025_2026.pdf and -2024_2025.pdf) each return the 136kB text/html soft-404, "
    "while the control caf-bank-pillar-3-disclosure-2023_2024.pdf in the same folder returns 200 / "
    "application/pdf / 1,401,132 bytes. The CAF group annual report linked from "
    "/home/about-us/governance-and-policies/annual-reports (caf_group_annual-report.pdf) is also for the year "
    "ended 30 April 2025. (3) Wayback CDX could not be queried that afternoon (the Internet Archive served its "
    "'Temporarily Offline' page) - UNREACHED, not a negative. So the FY2026 (year to 30 April 2026) accounts "
    "are not published at either Companies House or cafonline.org as of 2026-09-19; as a private company with a "
    "30 April year-end the filing deadline is 31 January 2027. No FY2026 Pillar 3 is expected at all (Rule 3.1 "
    "SDDT modification from 08/08/2025, above).\n\n"
    "WHY FY2025 IS BLANK. There is no Pillar 3 document, therefore no KM1 template, therefore nothing to "
    "reproduce. Note the deliberate difference from the single-metric sheets, which write 'Not publicly "
    "disclosed' in their FY2025 cells: on those sheets a metric exists and was searched for, whereas here "
    "the whole template is absent, and a blank column is the honest reproduction of a template that was "
    "never printed. Whether that absence is an SDDT structural exemption or a publication gap is "
    "deliberately left UNDETERMINED - CAF Bank's PRA Rule 3.1 modification starts 08/08/2025 while FY2025 "
    "ended 30 April 2025, three months earlier - and the SDDT DATE TEST in the Entity Note below sets out "
    "both sourced facts without resolving them. FY2026 onward falls unambiguously after the "
    "modification and is structurally exempt.\n\n"
    "WHY FY2021 AND FY2020 ARE BLANK - 'PILLAR 3 IS PUBLISHED BUT THE TEMPLATE IS NOT USED', which is a "
    "different and stronger finding than 'nothing was found'. Both editions are CRD IV-era documents - "
    "each says so in its own opening paragraph - and their capital section is a bespoke three-block table "
    "headed 'Total Capital Resources / Total Capital Requirement / Capital Surplus', whose only rows are "
    "CET1, Total T1 and Total Capital, each as a GBP000 amount beside a percentage. No row numbers, no "
    "SREP rows, no buffer rows, no LCR, no NSFR. That is a different and much shorter table, not an "
    "unnumbered KM1, and mapping it onto template row numbers would invent a correspondence CAF never "
    "published - so those years' capital figures live on the single-metric sheets, sourced from those "
    "tables, and are never back-filled into this template. Established positively, three ways, each "
    "guarding a known failure mode: (a) each document's OWN contents list was read and followed to the "
    "named page rather than any page-selection heuristic - FY2020 'Overview of capital position versus "
    "capital requirement ... 5', FY2021 the same section at p.4; (b) text extraction is RICH, which "
    "converts a zero from 'the tool failed' into a fact about the document - FY2021 returns 120 hits for "
    "'capital', 77 for 'ratio', 24 for 'leverage', 19 for 'buffer' and 10 for 'CET1', and FY2020 returns "
    "110/61/16/17/7, against 0 hits in BOTH documents for 'KM1', 'key metric', 'SREP', 'risk-weighted' "
    "and 'liquidity coverage'; (c) embedded images were enumerated, because a table can be a picture "
    "inside an otherwise text-native PDF - the FY2020 file contains NO images at all and the FY2021 "
    "file's only image is the 2,484x3,388 cover photograph on page 1, so there is no page anywhere in "
    "either document where a table could be hiding. Finally the dates agree with the rulebook: the UK KM1 "
    "template arrived on 1 January 2022, CAF Bank's year-end is 30 April, and the template duly first "
    "appears in FY2022 - the first year to END after that date.\n\n"
    + ENTITY_NOTE
    + "\n\n"
    "ROWS 1, 2 AND 3 ARE EQUAL IN THE SOURCE FOR FY2023 - READ FROM THE DOCUMENT ON 2026-09-18 AND RECORDED HERE "
    "SO THE QUESTION IS NOT RE-OPENED. The Pillar 3 disclosure for the year ended 30 April 2023 prints 45,140 on "
    "rows 1, 2 and 3 for 2023, with no Additional Tier 1 or Tier 2 line populated. The 2022 column of that same "
    "table is the control and is DISTINCT - CET1 27,253 against Tier 1 and Total capital of 38,253 - so this Bank "
    "prints the rows apart when they are apart, and they are held apart on this sheet.\n"
)

bw.add_km1_sheet(
    title="CAF Bank Limited — KM1 Key Metrics",
    subtitle="The bank's own 'Key metrics (Template UK KM1)', solo basis, £000, reproduced whole in its own "
             "row order, numbering, labels and precision. FY2024/FY2023/FY2022 each from its own edition; "
             "FY2021 from the FY2022 edition's comparative, the only UK-template FY2021 column CAF ever "
             "printed - and restated by it, see the note. FY2025 blank: no Pillar 3 document exists. "
             "FY2020 blank: that edition publishes Pillar 3 but does not use this template. CAF prints a "
             "reduced row set - UK 8a, UK 9a, 10, UK 10a and 14a-14f appear in NO edition.",
    rows=km1_rows,
    sources_text=KM1_SOURCES,
    first_col_width=80,
    source_height=800,
)

metric(
    "CET1 Capital", "£'000",
    [("Common Equity Tier 1 (CET1) capital", {"FY2025": FY25_NOT_PUBLISHED, "FY2024": 54342, "FY2023": 45140, "FY2022": 27253, "FY2021": 29095, "FY2020": 30350})],
    note=FY2025_NO_STANDALONE_NOTE,
)

metric(
    "CET1 Ratio", "% of RWA",
    [("CET1 ratio", {"FY2025": FY25_NOT_PUBLISHED, "FY2024": "29.35%", "FY2023": "30.8%", "FY2022": "21.9%", "FY2021": "22.8%", "FY2020": "20.6%"})],
    note=FY2025_NO_STANDALONE_NOTE,
)

metric(
    "Tier 1 Capital", "£'000",
    [("Tier 1 capital", {"FY2025": FY25_NOT_PUBLISHED, "FY2024": 54342, "FY2023": 45140, "FY2022": 38253, "FY2021": 40095, "FY2020": 41350})],
    note=FY2025_NO_STANDALONE_NOTE + " Equal to CET1 capital from FY2023 onward - CAF Bank's Additional Tier 1 "
         "securities were fully redeemed during FY2023 (see Statement of Changes in Equity); FY2020/FY2021/FY2022 "
         "include the AT1 instrument.",
)

metric(
    "Tier 1 Ratio", "% of RWA",
    [("Tier 1 ratio", {"FY2025": FY25_NOT_PUBLISHED, "FY2024": "29.35%", "FY2023": "30.8%", "FY2022": "30.8%", "FY2021": "31.4%", "FY2020": "28.0%"})],
    note=FY2025_NO_STANDALONE_NOTE,
)

metric(
    "Total Capital", "£'000",
    [("Total capital", {"FY2025": FY25_NOT_PUBLISHED, "FY2024": 56157, "FY2023": 45140, "FY2022": 38253, "FY2021": 40095, "FY2020": 41350})],
    note=FY2025_NO_STANDALONE_NOTE + " FY2024 is the only year with Tier 2 capital (£1,815k) - equal to Tier 1 "
         "capital in every other year shown.",
)

metric(
    "Total Capital Ratio", "% of RWA",
    [("Total capital ratio", {"FY2025": "29.7%", "FY2024": "30.33%", "FY2023": "30.8%", "FY2022": "30.8%", "FY2021": "31.4%", "FY2020": "28.0%"})],
    note="FY2025 is the only ratio sourced from the Annual Report's own Strategic Report (no standalone Pillar 3 "
         "document exists for FY2025) - see PILLAR3_SOURCES.",
)

metric(
    "Total RWAs", "£'000",
    [("Total risk-weighted exposure amount", {"FY2025": FY25_NOT_PUBLISHED, "FY2024": 185123, "FY2023": 146334, "FY2022": 124243, "FY2021": 127881, "FY2020": 147540})],
    note=FY2025_NO_STANDALONE_NOTE + " FY2021's own document states £127,881k; a later document's FY2021 "
         "comparative shows a immaterially different £127,844k - FY2021's own originally-published figure is "
         "used here, per this project's standard convention (see PILLAR3_SOURCES restatement note). FY2020's own "
         "document (£147,540k) ties exactly to FY2021's own FY2020 comparative column - no restatement at that "
         "boundary.",
)

rwa_breakdown_rows = [
    ("SECTION", "RWA by risk category", {}),
    ("DATA", "Credit risk (incl. counterparty credit risk, FY2020-FY2021 only)", {"FY2025": FY25_NOT_PUBLISHED, "FY2021": 105880, "FY2020": 125890}),
    ("DATA", "Credit risk and counterparty credit risk", {"FY2025": FY25_NOT_PUBLISHED, "FY2024": 129538, "FY2023": 112829, "FY2022": 102044}),
    ("DATA", "Operational risk", {"FY2025": FY25_NOT_PUBLISHED, "FY2024": 55585, "FY2023": 33505, "FY2022": 22199, "FY2021": 22001, "FY2020": 21650}),
    ("TOTAL", "Total", {"FY2025": FY25_NOT_PUBLISHED, "FY2024": 185123, "FY2023": 146334, "FY2022": 124243, "FY2021": 127881, "FY2020": 147540}),
]
bw.add_rwa_breakdown_sheet(
    title="CAF Bank Limited — RWA Breakdown",
    subtitle="£'000, solo basis. FY2025 not disclosed (no standalone Pillar 3 document - SDDT-exempt). See source note at bottom.",
    rows=rwa_breakdown_rows,
    sources_text=PILLAR3_SOURCES + "\n\nFY2020-FY2021's pre-KM1/OV1 category table combines credit and "
         "counterparty credit risk into a single 'Credit risk' line, unlike FY2022 onward's OV1 template which "
         "keeps them combined too under a single 'Credit risk and counterparty credit risk' row - both eras' "
         "rows are kept exactly as each document itself presents them, not force-aligned into one label.",
    first_col_width=54,
    source_height=320,
)

metric(
    "Leverage Ratio", "%",
    [
        ("Leverage ratio, excluding claims on central banks", {"FY2025": "6.35%", "FY2024": "6.05%", "FY2023": "4.64%", "FY2022": "3.97%", "FY2021": "3.81%", "FY2020": "4.62%"}),
        ("Leverage ratio, including claims on central banks", {"FY2025": LEV_INCL_FY25, "FY2024": LEV_INCL_FY24, "FY2023": "2.83%", "FY2022": "2.44%", "FY2021": "2.72%", "FY2020": "3.35%"}),
    ],
    note="FY2025 sourced from the Annual Report's Strategic Report (no standalone Pillar 3 document - SDDT-exempt); "
         "its 6.35% figure reconciles exactly against FY2024's own 6.05% 'excluding central banks' comparative "
         "quoted in the same Annual Report passage. FY2024's own Pillar 3 document discloses only the 'excluding' "
         "basis (the 'including central banks' exposure measure is given with no accompanying %, a genuine "
         "reduction in disclosure granularity vs. FY2021-2023) - FY2024/FY2025 'including central banks' left "
         "blank rather than calculated. FY2021's own document states 2.72%; a later document's FY2021 comparative "
         "shows an immaterially different 2.74% - FY2021's own originally-published figure is used here. "
         "THE SAME RESTATEMENT SHOWS ON THE EXCLUDING BASIS TOO, and it is the larger of the two (recorded here "
         "2026-09-16 so this sheet and the KM1 Key Metrics sheet do not tell different stories about one year): "
         "the FY2021 edition's own 'UK Leverage Ratio' table gives 3.81%, on Tier 1 resources of GBP40,095k over "
         "a leverage exposure of GBP1,052,245k, and that 3.81% is what the row above carries. The FY2022 "
         "edition's KM1 row 14 and its template UK LR2 row 25 both print 3.84% for the same date, because that "
         "edition restates the exposure measure DOWN to GBP1,044,543k on the same GBP40,095k of Tier 1 "
         "(40,095/1,052,245 = 3.810%; 40,095/1,044,543 = 3.838%). Both are the bank's own figures on the same "
         "basis for the same date, and neither is a transcription error. The KM1 Key Metrics sheet reproduces "
         "the 3.84% because that is what the template it reproduces printed, so this workbook's automated "
         "KM1-vs-metric-sheet cross-check reports row 14 FY2021 as one DELIBERATE, EXPECTED disagreement - a "
         "restated comparative meeting an as-published figure. Neither side has been edited to make them agree. "
         "FY2020's "
         "own document (4.62%/3.35%) ties exactly to FY2021's own FY2020 comparative column - no restatement at "
         "that boundary, unlike the FY2021-to-FY2022 gap.",
)

metric(
    "LCR", "£'000 / %",
    [
        ("High-quality liquid assets (weighted, average)", {"FY2025": FY25_NOT_PUBLISHED, "FY2024": 1150942, "FY2023": 1244786, "FY2022": 1255456, "FY2021": 1130354, "FY2020": LCR_FY2020}),
        ("Net cash outflows (adjusted)", {"FY2025": FY25_NOT_PUBLISHED, "FY2024": 447586, "FY2023": 478804, "FY2022": 476184, "FY2021": 421650, "FY2020": LCR_FY2020}),
        ("Liquidity Coverage Ratio (%)", {"FY2025": "543%", "FY2024": "257%", "FY2023": "260%", "FY2022": "264%", "FY2021": "268%", "FY2020": LCR_FY2020}),
    ],
    note="FY2021 FILLED 2026-09-19 (GA-020) - SUPERSEDES THE LAST SENTENCE OF THIS NOTE. The FY2021 LCR block "
         "(HQLA 1,130,354; net cash outflows 421,650; LCR 268%) is the bank's own printed '2021' comparative "
         "column of Template UK KM1 in the CAF Bank Ltd Pillar 3 Disclosure 30 April 2022, p.5 (rows 15, 16, 17), "
         "read off a rendered page image on 2026-09-19 - " + P3_2022_URL + ". The FY2021 edition itself prints "
         "no LCR, so this is the only place CAF ever published an April 2021 LCR; a published figure is FOUND, "
         "not 'not disclosed', and it is the same column the KM1 Key Metrics sheet already reproduces for "
         "FY2021. FY2020 remains an absence: no edition prints an April 2020 LCR.\n"
         "FY2025's 543% is sourced from the Annual Report's Strategic Report (no standalone Pillar 3 document - "
         "SDDT-exempt); its own comparator ties exactly to FY2024's Pillar 3 KM1 figure. FY2020 and FY2021 are "
         "both 'Not publicly disclosed' - both years' own Pillar 3 documents predate the LIQ1/KM1 templates that "
         "introduced LCR reporting, so no LCR figure was ever published for either year in its own document (a "
         "later document's FY2021 comparative of 268% exists, but per this project's convention of using each "
         "year's own originally-published figure, it is not back-filled here); confirmed for FY2020 by a full "
         "27-page read of its own Pillar 3 document, not assumed from the FY2021 pattern.",
)

metric(
    "NSFR", "£'000 / %",
    [
        ("Available stable funding", {"FY2025": FY25_NOT_PUBLISHED, "FY2024": 1377360, "FY2023": 1429893, "FY2022": 1426183, "FY2021": NSFR_NA, "FY2020": NSFR_NA}),
        ("Required stable funding", {"FY2025": FY25_NOT_PUBLISHED, "FY2024": 272188, "FY2023": 154418, "FY2022": 177361, "FY2021": NSFR_NA, "FY2020": NSFR_NA}),
        ("Net Stable Funding Ratio (%)", {"FY2025": FY25_NOT_PUBLISHED, "FY2024": "506%", "FY2023": "926%", "FY2022": "804%", "FY2021": NSFR_NA, "FY2020": NSFR_NA}),
    ],
    note="THREE MISSING YEARS, TWO DIFFERENT REASONS, LABELLED DIFFERENTLY ON PURPOSE (split 2026-09-15; all "
         "three previously sat blank and were described together as 'not disclosed', which conflated a "
         "regulatory boundary with a publication gap).\n"
         "FY2021 and FY2020 read 'Not applicable'. The UK Net Stable Funding Ratio requirement took effect only "
         "on 1 January 2022, under PRA PS17/21. CAF Bank's year-end is 30 April, so FY2021 ended 30 April 2021 "
         "and FY2020 ended 30 April 2020 - both comfortably before the requirement existed. There was no NSFR "
         "for the Bank to disclose at either date, which is why both years' own Pillar 3 documents predate the "
         "KM1 template that carries the NSFR rows at all. This is a structural absence, not a failure to "
         "publish, and it should never be re-chased. (FY2022 ended 30 April 2022, after the requirement began, "
         "and CAF did disclose 804% for it - which confirms the boundary falls exactly where stated.)\n"
         "FY2025 reads 'Not publicly disclosed' - a different and weaker finding. No standalone FY2025 Pillar 3 "
         "document exists, and unlike the three ratios CAF does put in its FY2025 Strategic Report (Total "
         "Capital Ratio, Leverage Ratio, LCR), NSFR is not mentioned there either; a full-document OCR search of "
         "the 51-page Annual Report for 'NSFR' and 'net stable' returns no hits. Not labelled as an SDDT "
         "exemption - see FY2025_NO_STANDALONE_NOTE and the SDDT DATE TEST for why that remains undetermined.",
)

bw.add_not_disclosed_metric_sheets(
    ["MREL Ratio"],
    PILLAR3_SOURCES,
    statements={"MREL Ratio": MREL_NP},
    per_note={"MREL Ratio": "Not publicly disclosed by CAF Bank Limited in any year FY2020-FY2025 - not in any "
              "standalone Pillar 3 document, nor in any Annual Report. CAF Bank is not a UK resolution entity."},
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {"FY2025": 1544559, "FY2024": 1510925, "FY2023": 1571534, "FY2022": 1556044, "FY2021": 1441296, "FY2020": 1212930}),
        ("Loans and advances to customers", {"FY2025": 219101, "FY2024": 197701, "FY2023": 177734, "FY2022": 160407, "FY2021": 124506, "FY2020": 103625}),
        ("Customer accounts", {"FY2025": 1450926, "FY2024": 1419433, "FY2023": 1505425, "FY2022": 1508937, "FY2021": 1398146, "FY2020": 1156995}),
        ("Total shareholders' funds", {"FY2025": 76239, "FY2024": 65100, "FY2023": 51473, "FY2022": 42929, "FY2021": 41289, "FY2020": 41350}),
    ],
    balance_sheet_unit="£'000",
    income_statement_totals=[
        ("Net operating income", {"FY2025": 47304, "FY2024": 46540, "FY2023": 29693, "FY2022": 12703, "FY2021": 11211, "FY2020": 12600}),
        ("Administrative expenses", {"FY2025": -32827, "FY2024": -27655, "FY2023": -18472, "FY2022": -11774, "FY2021": -9763, "FY2020": -10109}),
        ("Profit on ordinary activities after taxation", {"FY2025": 12139, "FY2024": 13627, "FY2023": 8575, "FY2022": 1640, "FY2021": 929, "FY2020": 1290}),
    ],
    income_statement_unit="£'000",
    equity_changes_totals=[
        ("Opening equity", {"FY2025": 65100, "FY2024": 51473, "FY2023": 42929, "FY2022": 41289, "FY2021": 41350}),
        ("Total comprehensive income for the year", {"FY2025": 12139, "FY2024": 13627, "FY2023": 8575, "FY2022": 1640, "FY2021": 929, "FY2020": 1290}),
        ("Other equity movements, net", {"FY2023": -31, "FY2021": -990, "FY2020": -1290}),
        ("Closing equity", {"FY2025": 76239, "FY2024": 65100, "FY2023": 51473, "FY2022": 42929, "FY2021": 41289, "FY2020": 41350}),
    ],
    equity_changes_unit="£'000",
    cash_flow_totals=[
        ("Net cash generated from/(used in) operating activities", {"FY2025": 20729, "FY2024": -91236, "FY2023": -15666, "FY2022": 79374, "FY2021": 240451, "FY2020": 115649}),
        ("Net cash generated from/(used in) investing activities", {"FY2025": -60368, "FY2024": 122750, "FY2023": 31896, "FY2022": 104079, "FY2021": -148048, "FY2020": -103448}),
        ("Net cash used in financing activities", {"FY2025": 0, "FY2024": 0, "FY2023": -31, "FY2022": 0, "FY2021": -1423, "FY2020": -5766}),
        ("Cash and cash equivalents at end of year", {"FY2025": 614885, "FY2024": 654524, "FY2023": 623010, "FY2022": 606811, "FY2021": 423358, "FY2020": 332378}),
    ],
    cash_flow_unit="£'000",
    ratios=[
        ("CET1 Ratio", {"FY2025": FY25_NOT_PUBLISHED, "FY2024": "29.35%", "FY2023": "30.8%", "FY2022": "21.9%", "FY2021": "22.8%", "FY2020": "20.6%"}),
        ("Tier 1 Ratio", {"FY2025": FY25_NOT_PUBLISHED, "FY2024": "29.35%", "FY2023": "30.8%", "FY2022": "30.8%", "FY2021": "31.4%", "FY2020": "28.0%"}),
        ("Total Capital Ratio", {"FY2025": "29.7%", "FY2024": "30.33%", "FY2023": "30.8%", "FY2022": "30.8%", "FY2021": "31.4%", "FY2020": "28.0%"}),
        ("Leverage Ratio", {"FY2025": "6.35%", "FY2024": "6.05%", "FY2023": "4.64%", "FY2022": "3.97%", "FY2021": "3.81%", "FY2020": "4.62%"}),
        ("LCR", {"FY2025": "543%", "FY2024": "257%", "FY2023": "260%", "FY2022": "264%", "FY2021": "268%", "FY2020": LCR_FY2020}),
        ("NSFR", {"FY2025": FY25_NOT_PUBLISHED, "FY2024": "506%", "FY2023": "926%", "FY2022": "804%", "FY2021": NSFR_NA, "FY2020": NSFR_NA}),
    ],
    note="Full 6-year Balance Sheet/P&L/Statement of Changes in Equity/Cash Flow Statement (FY2020-FY2025), no "
         "FRS 101/102 cash-flow exemption. Extended back to FY2020 2026-09-06 (HD-061) - re-verified directly "
         "against a rendered page-image read of FY2020's own Companies House filing and FY2021's own FY2020 "
         "comparative column, both of which tie exactly with no restatement found. CORRECTION (2026-09-05): CAF "
         "Bank Limited does publish real Pillar 3 disclosure via standalone PDFs on cafonline.org (not Companies "
         "House) for FY2020-FY2024, and the FY2025 Annual Report's own Strategic Report discloses Total Capital "
         "Ratio/Leverage Ratio/LCR directly; an earlier build of this workbook incorrectly marked all 11 Pillar 3 "
         "metric sheets 'Not publicly disclosed' - only MREL Ratio remains genuinely undisclosed in every year. "
         "See ENTITY_NOTE and PILLAR3_SOURCES on the Cash Flow Statement sheet for the full correction and "
         "citations. Asset Quality's individual/collective loan loss provision split is disclosed for FY2020, "
         "FY2021, FY2024 and FY2025 but not FY2022/FY2023 (FRS 102, not IFRS 9 - no stage split at all).\n\n"
         "EMPTY CELLS WERE MADE EXPLICIT 2026-09-15. Every previously-blank Pillar 3 cell now carries a word, "
         "because a blank is indistinguishable from an unresearched gap and had caused this bank to be re-chased. "
         "Two different words are used and the difference matters. 'Not applicable' appears only on NSFR FY2021 "
         "and FY2020: the UK NSFR requirement began on 1 January 2022 under PRA PS17/21, and CAF's 30 April "
         "year-end puts both those reference dates before it, so there was nothing to disclose - a regulatory "
         "boundary that should never be re-chased. Everything else reads 'Not publicly disclosed', meaning the "
         "search was done and came back empty.\n"
         "THE FY2025 LABEL IS DELIBERATELY *NOT* 'SDDT-EXEMPT', AND THIS MUST NOT BE 'TIDIED UP'. CAF Bank's own "
         "website does assert an exemption - verbatim, and it is the whole of that page: 'CAF Bank has become "
         "part of the PRA's SDDT (\"Small Domestic Deposit Taker\") regime under which, as a non-listed "
         "institution, the Bank is not required to publish a Pillar 3 report' (fetched 2026-09-15). But that page "
         "carries no date, no effective date and no rule number, and the PRA's own register - the thing that "
         "actually settles it - shows CAF Bank Limited (FRN 204451) holding the Rule 3.1 SDDT modification "
         "(waiver ref A00010742P.pdf) with a START DATE of 08/08/2025, while FY2025 ended on 30 April 2025, three "
         "months earlier. On a reference-date reading FY2025 predates the relief and the blanks are a genuine "
         "gap; on a publication-date reading the FY2025 report would not have fallen due until after the relief "
         "bit. The tension is real, both facts are sourced, and this workbook does not resolve it by picking a "
         "side - the cells are blank either way and only the LABEL is at stake. FY2026 onward (year ending 30 "
         "April 2026) falls unambiguously after 08/08/2025 and IS structurally exempt; FY2024 and earlier "
         "unambiguously predate it, which is consistent with real standalone Pillar 3 documents existing for "
         "FY2020-FY2024.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/CAF BANK FINANCIALS.xlsx")
