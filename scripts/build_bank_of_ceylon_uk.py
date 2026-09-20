import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

# FY2013 (2026-09-15) is a DELIBERATELY NON-CONTIGUOUS column. The Bank's 31
# December 2013 Pillar 3 edition was recovered from the Internet Archive; the
# 2014-2017 editions were not, and the Wayback CDX sweep of the whole
# bankofceylon.co.uk domain lists Pillar 3 captures for 2013, 2018, 2019, 2020,
# 2021, 2024 and 2025 only. Rather than insert four wholly empty FY2017-FY2014
# columns to make the series look continuous, the one recovered year is placed
# next to FY2018 and the four-year break is stated in its column label and in
# every sheet note. (Same shape as build_national_bank_of_egypt_uk.py, whose
# YEARS jumps FY2021 -> FY2017.)
#
# FY2013 is a REGULATORY-ONLY column: it carries Pillar 3 capital figures only.
# No Companies House statutory filing for 2013 was sourced in this pass, so the
# Balance Sheet, Profit & Loss, Cash Flow and Asset Quality sheets are blank for
# it - blank because unsourced, not because the Bank published nothing.
YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021", "FY2020", "FY2019", "FY2018", "FY2013"]  # most recent first
YEAR_LABEL = {y: y for y in YEARS}
YEAR_LABEL["FY2013"] = "FY2013 (Pillar 3 only - 4-year gap, see notes)"

CH2025_URL = "https://find-and-update.company-information.service.gov.uk/company/06736473/filing-history/MzUyMjY1MjQxM2FkaXF6a2N4/document?format=pdf&download=0"
CH2023_URL = "https://find-and-update.company-information.service.gov.uk/company/06736473/filing-history/MzQyMTM2NzE0MWFkaXF6a2N4/document?format=pdf&download=0"
CH2021_URL = "https://find-and-update.company-information.service.gov.uk/company/06736473/filing-history/MzMzODIzNzc0NWFkaXF6a2N4/document?format=pdf&download=0"
CH2020_URL = "https://find-and-update.company-information.service.gov.uk/company/06736473/filing-history/MzMwNDA2MDQ0MmFkaXF6a2N4/document?format=pdf&download=0"
CH2019_URL = "https://find-and-update.company-information.service.gov.uk/company/06736473/filing-history/MzI2MzgzMDIxNWFkaXF6a2N4/document?format=pdf&download=0"
CH2018_URL = "https://find-and-update.company-information.service.gov.uk/company/06736473/filing-history/MzIzMDcwOTM1MGFkaXF6a2N4/document?format=pdf&download=0"

P3_2025_URL = "https://www.bankofceylon.co.uk/downloads/corporate/BOCUK_Pillar%203%20Disclosures%2031%20December%202025.pdf"
P3_2024_URL = "https://www.bankofceylon.co.uk/downloads/corporate/BOCUK_Pillar%203%20Disclosures%2031%20December%202024.pdf"
P3_2021_URL = "https://www.bankofceylon.co.uk/downloads/corporate/BOCUK_Pillar%203%20Disclosures%2031%20December%202021.pdf"
P3_2020_URL = "https://www.bankofceylon.co.uk/downloads/corporate/BOCUK_Pillar%203%20Disclosures%2031%20December%202020.pdf"
P3_2019_URL = "https://www.bankofceylon.co.uk/downloads/corporate/BOCUK_Pillar%203%20Disclosures%2031%20December%202019.pdf"
P3_2018_URL = "https://www.bankofceylon.co.uk/downloads/corporate/BOCUK_Pillar%203%20Disclosures%2031%20December%202018.pdf"
# Recovered from the Internet Archive 2026-09-15 (the live site no longer serves it;
# it sat under the older /documents/corporate/ path, not today's /downloads/corporate/).
P3_2013_URL = "https://web.archive.org/web/20150813084438id_/http://www.bankofceylon.co.uk:80/documents/corporate/BOCUK_Pillar_3_2013.pdf"

ENTITY_NOTE = (
    "Entity note: Bank of Ceylon (UK) Limited (company 06736473, FRN 514744) is a wholly-owned UK subsidiary of "
    "Bank of Ceylon (Sri Lanka, state-owned). Unlike several other single-country foreign-parented subsidiaries "
    "in this project, it does NOT take the FRS 101/102 cash-flow-statement exemption - a full Statement of Cash "
    "Flows is filed every year, in GBP (no FX conversion needed)."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are Bank of Ceylon (UK) Limited's own Statement of Cash Flows, £'000, as filed at "
    "Companies House (all 8 filings are fully scanned/image-only - OCR'd with tesseract, cross-verified against "
    "rendered page images at up to 400dpi):\n"
    f"FY2025 & FY2024: Full accounts made up to 31 December 2025, p.27 (Statement of Cash Flows) - {CH2025_URL}\n"
    f"FY2023 & FY2022: Full accounts made up to 31 December 2023, p.42 (Statement of Cashflow) - {CH2023_URL}\n"
    f"FY2021 (& FY2020 comparative, not used): Full accounts made up to 31 December 2021, p.29 (Statement of "
    f"Cashflow) - {CH2021_URL}\n"
    f"FY2020 (& FY2019 comparative, not used): Full accounts made up to 31 December 2020, p.31 (Statement of "
    f"Cash Flow) - {CH2020_URL}\n"
    f"FY2019 (& FY2018 comparative, not used): Full accounts made up to 31 December 2019, p.31 (Statement of "
    f"Cash Flows) - {CH2019_URL}\n"
    f"FY2018 (& FY2017 comparative, not used): Full accounts made up to 31 December 2018, p.26 (Statement of "
    f"Cash Flows) - {CH2018_URL}\n"
    "DATA ERROR NOTE: the FY2021 filing's own printed 'Other assets and derivatives' line for 2021 reads '-761' "
    "(a bare minus sign, inconsistent with every other negative figure in the same column, which uses "
    "parentheses). This does not reconcile with that same document's own printed subtotals ('635' changes-in "
    "subtotal, '927' net operating cash flow) - summing the 7 itemised 'Changes in' lines with -761 gives -887, "
    "not 635. Using +761 instead reconciles exactly to both printed subtotals (635 and 927). +761 is used here; "
    "the original printed '-761' is preserved in this note for reference. The FY2020 comparative column's "
    "equivalent line (-304) is internally consistent as printed and was not changed.\n"
    "PRESENTATION NOTE: the FY2021, FY2023 AND FY2020 filings all mislabel their investing/financing subtotal "
    "rows - the FY2021 filing's 'Net cash flow from financing activities' caption sits directly above the "
    "FY2020 column's investing-activities value (-149, which is actually 'Acquisition of fixed assets'), the "
    "FY2023 filing's 'Net cash flow from investing activities' caption sits directly above a value that is "
    "actually the operating-activities subtotal (matches 'Cash generated by operations' exactly), and the "
    "FY2020 filing itself (own year, both 2020 and 2019 columns) captions its only investing line item "
    "('Acquisition of fixed assets') as 'Net cash flow from financing activities' with no separate financing "
    "section at all that year - the same recurring mislabeling pattern, now confirmed across 3 separate "
    "filings/vintages. Neither year discloses any financing activity beyond a single investing-classified line "
    "('Acquisition of fixed assets' FY2021/FY2020/FY2019/FY2018, 'Purchase of operating property, plant and "
    "equipment' FY2023/FY2022) or, in FY2022, a genuine financing line ('Repayment on investments', £747k). "
    "This workbook places each line under its correct economic section (Operating/Investing/Financing) "
    "regardless of the source's caption placement; every section TOTAL and the full opening/closing cash chain "
    "reconciles exactly across all 8 years once corrected.\n"
    + ENTITY_NOTE
)


FY2013_NOTE = (
    "  FY2013 FIGURES AS TRANSCRIBED (£'000, entity-level, Company Registration no. 06736473 printed on the "
    "cover - the same entity as every other column here). Capital Resources table, p.7: Share capital 15,000; "
    "Fair value reserve 31; Cumulative revenue losses (1,073); sub-total 13,958; less Intangible assets (522); "
    "CORE TIER 1 CAPITAL 13,436. Tier 2 Capital: Revaluation reserve 463. TOTAL REGULATORY CAPITAL 13,899. "
    "Minimum Capital Requirement - Pillar 1 table, p.8: Credit Risk 2,454; Market Risk 24; Operational Risk "
    "(basic indicator approach) 292; TOTAL PILLAR 1 REQUIREMENT 2,770. Credit-risk capital requirement at 8% "
    "by exposure class, p.9: Central Governments and Central Banks 0; Financial Institutions 1,620; Personal "
    "loans and advances 156; Secured on real estate 231; Commercial loans and advances 227; Fixed and other "
    "assets 220; total 2,454. Gross credit risk exposure before mitigation, p.9: 63,175 at 31 December 2013 "
    "(81,691 average for the period). This edition has a genuine text layer - figures were read directly, not "
    "by OCR.\n"
    "  FY2013 BASIS CAVEATS. (1) NO RISK-WEIGHTED-ASSET FIGURE AND NO CAPITAL RATIO IS DISCLOSED ANYWHERE IN "
    "THIS EDITION. It publishes the Pillar 1 CAPITAL requirement (expressly '8% of the risk weighted exposure "
    "amounts') instead. So Total RWAs, CET1 Ratio, Tier 1 Ratio and Total Capital Ratio are blank for FY2013 "
    "and are NOT back-solved - dividing the 2,770 Pillar 1 requirement by 8% would give an apparent ~£34.6m "
    "that no document states, and this project does not derive. The capital requirements that ARE disclosed "
    "appear on the RWA Breakdown sheet as capital, on their own labelled rows. (2) Leverage ratio, LCR and "
    "NSFR are blank: none existed as a UK disclosure requirement at 31 December 2013 and the edition contains "
    "none of them - its liquidity section describes the then-current BIPRU 12 / ILAA / Individual Liquidity "
    "Guidance regime narratively, with no ratio. (3) The edition's capital table is headed 'CRD IV' even "
    "though CRD IV did not apply until 1 January 2014; transcribed as printed, with no attempt to reclassify "
    "the components onto a Basel II presentation.\n"
    "  FY2013 MATERIALLY REVISES THIS WORKBOOK'S TIER 2 NOTE - recorded so a later pass does not re-derive it. "
    "The Total Capital sheet previously described the Bank's recognition of its revaluation reserve as Tier 2 "
    "capital as something that began 'from FY2020 on'. The FY2013 edition shows it was already doing exactly "
    "that seven years earlier: Tier 2 Capital consists of the Revaluation reserve, 463. So the real anomaly is "
    "FY2018/FY2019, the two years with NO Tier 2 at all, not FY2020 onward. The FY2020-onward wording is left "
    "in place on that sheet because it correctly describes the FY2018-FY2025 window it was written about, but "
    "it should not be read as the start of the practice.\n"
    "  EDITIONS BETWEEN FY2013 AND FY2018 - NOT RECOVERED, and the gap is genuine rather than unsearched: the "
    "Wayback CDX sweep of the whole bankofceylon.co.uk domain (already run for the FY2022/FY2023 closure "
    "below) returns Pillar 3 captures for 2013, 2018, 2019, 2020, 2021, 2024 and 2025 only. No 2014-2017 "
    "edition is captured, and the FY2018 edition's comparative column is FY2017 in its Key Metrics table only "
    "(already used on these sheets), not a full capital table, so nothing further is recoverable from it. "
    "FY2017-FY2014 are therefore omitted as columns entirely rather than added blank.\n"
    "  VALIDATION GATE: FY2013 is additive - it occupies a column that did not exist before this pass and "
    "overlaps no existing column, so nothing was overwritten. No cross-edition check was possible (the "
    "nearest surviving edition is FY2018, five years later, and carries no FY2013 comparative), so the column "
    "rests on this single document. It is internally consistent: 15,000 + 31 - 1,073 = 13,958, less 522 = "
    "13,436 Core Tier 1; 13,436 + 463 = 13,899 Total Regulatory Capital; and 2,454 + 24 + 292 = 2,770 Total "
    "Pillar 1 Requirement, with the p.9 exposure-class column summing to the same 2,454."
)


def p3_sources(page_25="3", page_24="4", page_21="12"):
    return (
        "Sources - Bank of Ceylon (UK) Limited Pillar 3 disclosures (own entity-level basis; UK KM1-style Key "
        "Metrics template FY2018-FY2019 and again from FY2022 on, PRA's pre-2022 own-funds/leverage tables for "
        "FY2021, an infographic-style 'Key Metrics' summary plus a differently-laid-out Own Funds/Leverage "
        "section for FY2020), £'000 unless stated:\n"
        f"FY2025 & FY2024 comparative: Pillar 3 Disclosures 31 December 2025, p.{page_25} (1.1 Key Metrics) - {P3_2025_URL}\n"
        f"FY2024 (own year) & FY2023 comparative: Pillar 3 Disclosures 31 December 2024, p.{page_24} (1.1 Key Metrics) - {P3_2024_URL}\n"
        f"FY2021 (own year): Pillar 3 Disclosures as at 31st December 2021, p.{page_21} (4.1 Total Available Capital) - {P3_2021_URL}\n"
        f"FY2020 (own year) & FY2019 restated comparative: Pillar 3 Disclosures as at 31st December 2020, p.12 "
        f"(4.1 Total Available Capital) and p.19 (7. Leverage) - {P3_2020_URL}\n"
        f"FY2019 (own year, as originally published) & FY2018 comparative: Pillar 3 Disclosures as at 31st "
        f"December 2019, p.6 (Key metrics) - {P3_2019_URL}\n"
        f"FY2018 (own year, as originally published) & FY2017 comparative: Pillar 3 Disclosures as at 31st "
        f"December 2018, p.5 (Key metrics) - {P3_2018_URL}\n"
        f"FY2013 (own year, RECOVERED 2026-09-15 from the Internet Archive): Capital & Risk Management - Pillar 3 "
        f"Disclosures 31st December 2013, p.7 (Capital Resources), p.8 (Minimum Capital Requirement - Pillar 1) "
        f"and p.9 (Capital Resource Requirement at 8% by exposure class; Gross credit risk exposure) - "
        f"{P3_2013_URL}\n" + FY2013_NOTE + "\n"
        "FY2022: no standalone Pillar 3 document exists (2022 and 2023 editions are both absent from the bank's "
        "own published list; FY2023 is covered here only via FY2024's own comparative column).\n"
        "RE-CONFIRMED 2026-09-19, AND NOW WRITTEN INTO THE CELLS. The bank's own Financial Statements index "
        "(https://bankofceylon.co.uk/financial-statements/, fetched today, HTTP 200, text/html, 195,840 bytes, "
        "read as HTML rather than slug-guessed) links exactly six Pillar 3 PDFs - 2018, 2019, 2020, 2021, 2024 "
        "and 2025. There is still nothing for 2022 or 2023, twenty months after the FY2023 year end, so the "
        "absence is settled rather than pending. The five FY2022 cells that this establishes as absent - Tier 1 "
        "Ratio, Total RWAs, the RWA Breakdown total, Leverage Ratio and LCR - previously stood BLANK, which made "
        "an established negative indistinguishable from a cell nobody had looked at. They now carry a short "
        "statement naming the reason. This changes no figure and asserts nothing new; it moves an existing "
        "finding from these notes into the grid where a reader and the gap census can both see it.\n"
        f"FY2022 PARTIAL FILL (2026-09-15, interior-gap sweep): the CET1 Capital and Tier 1 Capital sheets are "
        f"no longer blank for FY2022. The figure comes not from a Pillar 3 document but from the Bank's own "
        f"audited FY2022 statutory accounts, Note 28 'Capital Management' (Annual Financial Report 2022, p.60), "
        f"which states in terms: 'As at 31 December 2022, after deducting book value of intangible assets from "
        f"shareholder funds is GBP 13,734,398 on a fully loaded basis. The regulatory CET1 capital after "
        f"adjusting for transitional relief under IFRS9 would be GBP 13,958,648. (GBP 13,425,750 at 31 December "
        f"2021).' Source: https://www.bankofceylon.co.uk/downloads/corporate/BOCUK_Financial_statements_2022.pdf "
        f"(image-only scan; OCR'd with tesseract and re-read at 400dpi to confirm every digit). The £13,425,750 "
        f"comparative in that same sentence is within £2k of the FY2021 Pillar 3 document's own CET1 of "
        f"£13,424k already on this sheet, which is what confirms the two are the same measure - i.e. the FY2022 "
        f"figure is on the same transitional basis as the surrounding years, not a differently-defined one.\n"
        "SUPERSEDED IN PART, 2026-09-15 (second pass): the statement below that 'neither the FY2022 nor the "
        "FY2023 statutory accounts state ... a capital ratio anywhere' was WRONG, and is corrected here rather "
        "than deleted so the error is traceable. The FY2023 accounts' Strategic Report, p.8 ('CAPITAL'), states "
        "in terms: 'The Bank maintained a strong CET1 capital position of GBP 13,684,688 (2022- GBP 12,852,280) "
        "with a CET1 ratio of 43% (2022: 44 %) and a total capital of GBP 14,788,668 (2022-13,818,899) with a "
        "ratio of 46% at 31st of December 2023 (2022: 48%).' That single sentence supplies four previously-blank "
        "FY2022 cells (CET1 capital, CET1 ratio, Total capital, Total capital ratio) - all four are now entered "
        "on clearly-labelled separate rows, see the CONFLICT note below. Source: "
        "https://bankofceylon.co.uk/downloads/corporate/BOCUK_Financial_statements_2023.pdf (image-only scan; "
        "OCR'd with tesseract AND re-rendered at 400dpi and read visually digit by digit to confirm, per this "
        "project's OCR rule). The earlier pass evidently searched the notes (Note 32) and not the Strategic "
        "Report narrative.\n"
        "FY2022 CELLS STILL DELIBERATELY LEFT BLANK after that correction: Total RWAs and Leverage Ratio. "
        "Neither the FY2022 nor the FY2023 statutory accounts state an RWA figure or a leverage ratio anywhere "
        "(both OCR'd page by page in full), and the FY2023 accounts' own Note 32 gives only that year's "
        "available capital (GBP 13,684,668) with no FY2022 comparative. RWA is NOT back-solved from the newly "
        "found FY2022 capital and ratio - 12,852,280 / 0.44 would give an apparent ~GBP 29.2m, but a ratio "
        "rounded to a whole percent cannot support that, and this project does not derive. Similarly, the "
        "observation that in every disclosed year the Bank's Tier 2 capital equals its revaluation reserve is "
        "left as an observation: FY2022's Total capital is now entered from the FY2023 accounts' stated "
        "GBP 13,818,899, NOT from CET1 + reserve.\n"
        "FY2022/FY2023 DOCUMENT SEARCH (2026-09-15, exhausted): eight URL variants of the bank's own stable "
        "'BOCUK_Pillar 3 Disclosures 31 December <year>.pdf' naming pattern were probed on both www and apex "
        "hosts - all returned the site's HTML 404, not a PDF. A Wayback CDX scan of the whole "
        "bankofceylon.co.uk domain lists Pillar 3 captures for 2013, 2018, 2019, 2020, 2021 and 2024 only. The "
        "bank's redesigned WordPress site's own Financial Statements page (and its July 2026 Wayback capture) "
        "links Pillar 3 PDFs for 2018, 2019, 2020, 2021, 2024 and 2025 and nothing for 2022 or 2023 - i.e. the "
        "two editions were never published, rather than published and lost.\n"
        "SOURCED NEGATIVE, RE-RUN WITH CONTROLS 2026-09-15: the FY2022/FY2023 absence is evidence, not merely a "
        "failure to find, because the probe was run against both a POSITIVE and a NEGATIVE control on the one "
        "naming pattern the site uses uniformly. POSITIVE CONTROLS: the 2021 file returned HTTP 200, 503,885 "
        "bytes, Content-Type application/pdf, first five bytes '%PDF-'; the 2024 file returned HTTP 200, 978,715 "
        "bytes, application/pdf, '%PDF-'. TEST CASES: the 2022 and 2023 files on that identical pattern each "
        "returned HTTP 404, 146 bytes, Content-Type text/html. NEGATIVE CONTROL: an invented path "
        "(BOCUK_THIS_FILE_DOES_NOT_EXIST_CONTROL.pdf) in the same directory returned the same HTTP 404, 146 "
        "bytes, text/html - and the three 404 bodies are BYTE-IDENTICAL (md5 8eec510e57f5f732fd2cce73df7b73ef "
        "for all three). A server that returns a real 404 for a made-up path and the same real 404 for the 2022 "
        "and 2023 paths is not soft-404ing a file it actually holds; combined with the index and the Wayback "
        "sweep, the two editions do not exist.\n"
        "CAVEAT RECORDED HONESTLY, NOT USED AS EVIDENCE: the FY2022 accounts' Board Audit and Compliance "
        "Committee focus list (p.23) includes 'Approved the Pillar 3 disclosures as 31 December 2021', and no "
        "equivalent line appears in the FY2023, FY2024 or FY2025 accounts. It is tempting to read that silence "
        "as confirmation that no 2022/2023 Pillar 3 was approved - but the FY2024 and FY2025 Pillar 3 editions "
        "demonstrably exist and are fetched by this script, so the absence of the line proves nothing either "
        "way. It is noted here only so a later pass does not rediscover it and mistake it for proof.\n"
        "CROSS-VINTAGE NOTE (Leverage Ratio only): the FY2024 Pillar 3 document's own figures for FY2024 (Total "
        "exposure £75,247k, Leverage ratio 18.5%) differ slightly from the FY2025 document's restated FY2024 "
        "comparative (£76,247k, 18.3%). This workbook uses each year's own originally-published figure as the "
        "primary column (FY2024 = 18.5%, from the FY2024 document); the restatement is noted here, not silently "
        "blended. Separately, the FY2025 document's own narrative text states the leverage ratio 'declined from "
        "18.5% to 15.2%' in 2025 - this contradicts both that same document's Key Metrics table and its own "
        "Section 7 reconciliation table, which independently agree at 14.3% (FY2025) / 18.3% (FY2024 restated). "
        "The two internally-consistent tables are used; the narrative sentence appears to be a drafting error.\n"
        "CROSS-VINTAGE RESTATEMENT (FY2019, all capital/leverage metrics): the FY2020 Pillar 3 document's own "
        "'restated' FY2019 comparative (CET1/Total capital £13,143k, Total RWAs £28,513k, CET1/Total capital "
        "ratio 46.1%/49.3%, leverage exposure £40,135k, leverage ratio 32.7%) differs materially from the "
        "FY2019 document's own originally-published FY2019 figures (£13,569k / £23,604k / 57.5% both ratios / "
        "£39,619k exposure / 34.2% leverage) - driven by the same office-building revaluation restatement "
        "documented on the Statement of Changes in Equity sheet (the FY2020 document explicitly states '2019 "
        "comparative numbers have been restated in 2020, following the decision to include the revaluation of "
        "the office building in the 2019 accounts'), plus an apparent change in how RWA is computed (the "
        "FY2019 document's own £23,604k is credit-risk RWA only - now PROVEN, see the RWA Breakdown and Total "
        "RWAs sheets' notes - while the FY2020 document's £28,513k restated figure is the full Pillar 1 "
        "total). This workbook uses each year's own originally-published figure as the primary column, per "
        "this project's standard convention, with ONE deliberate exception created 2026-09-15: the Total RWAs "
        "sheet's FY2019 cell now carries the FY2020 edition's restated £28,513k, because the FY2019 edition's "
        "own £23,604k is not a total RWA at all but a credit-risk subtotal, and no total exists in the FY2019 "
        "edition. That is the Ghana International route (take the corrected total from the following "
        "edition's own statement of the prior year) and it is preferred here to leaving a knowingly wrong "
        "measure in place. The consequence is that FY2019 is the one year where the Total RWAs sheet and the "
        "capital sheets come from different editions - CET1/Total capital stay at the FY2019 edition's "
        "£13,569k, so 13,569/28,513 reproduces neither the FY2019 edition's printed 57.5% nor the FY2020 "
        "edition's restated 46.1% (which is 13,143/28,513). Divide across those sheets for FY2019 at your own "
        "risk; both editions' full sets are recorded here and on the Total RWAs sheet's memo row.\n"
        + ENTITY_NOTE
    )


bw = BankWorkbook(bank_name="Bank of Ceylon (UK) Limited", years=YEARS, year_label=YEAR_LABEL, header_color="8D6A9F")

STATEMENTS_SOURCES = (
    "Sources - Bank of Ceylon (UK) Limited's own Statement of Financial Position / Statement of Comprehensive "
    "Income / Statement of Changes to Equity, £'000, as filed at Companies House (all 6 filings are fully "
    "scanned/image-only - visually transcribed by rendering each page to PNG at 150-200dpi and reading it "
    "directly, the same OCR-equivalent workflow used elsewhere in this project for image-only statutory "
    "filings, cross-checked against a tesseract OCR pass):\n"
    f"FY2025 & FY2024: Full accounts made up to 31 December 2025, pp.24-26 - {CH2025_URL}\n"
    f"FY2023 & FY2022: Full accounts made up to 31 December 2023, pp.39-41,57 (Note 15) - {CH2023_URL}\n"
    f"FY2021 (& FY2020 comparative, not used): Full accounts made up to 31 December 2021, pp.26-28,43 (Note 14) - "
    f"{CH2021_URL}\n"
    f"FY2020 (own year, as originally filed) & FY2019 restated comparative: Full accounts made up to 31 "
    f"December 2020, pp.28-30 - {CH2020_URL}\n"
    f"FY2019 (own year, as originally published) & FY2018 comparative: Full accounts made up to 31 December "
    f"2019, pp.28-30,42 (Note 15) - {CH2019_URL}\n"
    f"FY2018 (own year, as originally published) & FY2017 comparative: Full accounts made up to 31 December "
    f"2018, pp.23-26,38 (Note 16) - {CH2018_URL}\n"
    "PRESENTATION NOTE: line items are not fully consistent year to year in these filings - Derivatives (assets "
    "and liabilities) appear as a separate line in the FY2020-FY2023 filings (introduced in FY2020, per that "
    "filing's own Notes 20a/20b/17a/17b), not FY2018/FY2019/FY2024/FY2025 (likely folded into Other assets/"
    "Other liabilities those years, not stated explicitly); Prepayments and accrued income and Accruals are "
    "separate lines FY2022-FY2025 but not disclosed separately FY2018-FY2021 (folded into Other assets/Other "
    "liabilities); Current tax is a separate line FY2023-FY2025 only; Deferred tax is a separate liability line "
    "FY2020-FY2025 but not FY2018/FY2019 (immaterial/not applicable those years - no deferred tax asset or "
    "liability recognised per Note 13 of the FY2019 filing). None of this affects Total assets/Total "
    "liabilities/Total equity, which tie out exactly every year.\n"
    "STRUCTURAL BREAK (P&L, FY2020 boundary): the FY2018 and FY2019 filings present operating expenses as a "
    "single 'Administration expenses' line (plus separately-disclosed Depreciation/Amortisation/ECL "
    "provisioning); from FY2020 on, this is split into 'Personnel expenses' and 'Operational expenses' as two "
    "separate lines. Both are genuine, not a transcription choice - reproduced as each source discloses; the "
    "'Administration expenses' line is populated only for FY2018/FY2019, and 'Personnel expenses'/'Operational "
    "expenses' only from FY2020 on.\n"
    "DATA CONSISTENCY NOTE: the FY2025 filing's own SOCE opening balance for 1 January 2024 (15,000/(1,293)/"
    "1,104/14,811) ties out exactly to the FY2023 filing's own closing balance for 31 December 2023, and "
    "similarly FY2023's opening 1 January 2022 balance (15,000/(1,989)/820/13,831) via the FY2023 filing itself, "
    "and FY2021's closing 31 December 2021 balance (15,000/(1,843)/745/13,902) matches the FY2023 filing's own "
    "'1 January 2022' opening row exactly, and FY2020's closing 31 December 2020 balance (15,000/(1,955)/904/"
    "13,949) matches FY2021's own '1 January 2021' opening row exactly, and FY2018's own filing chains "
    "correctly through FY2019's own filing (FY2018 close 15,000/(2,037)/417/13,380 = FY2019's own '1 January "
    "2019' opening row) - full chain verified across 6 source documents EXCEPT at the FY2019/FY2020 boundary, "
    "where a genuine restatement breaks it (see below).\n"
    "RESTATEMENT FLAGGED (FY2019/FY2020 boundary): the FY2020 filing's own Statement of Changes to Equity opens "
    "with 'Equity shareholder's funds 1 January 2020' of 15,000/(1,932)/914/13,982 - the revaluation reserve "
    "(914) and total equity (13,982) do NOT match FY2019's own originally-published 31 December 2019 closing "
    "balance (15,000/(1,932)/408/13,476, as filed a year earlier). The FY2020 filing explains this directly: "
    "'Prior year restatement incorporates the revaluation surplus of the Bank's office building. The valuation "
    "was carried out during February 2020... The amount shown under revaluation reserves in 2019 is the value "
    "net of deferred tax liability' (revaluation reserve +506 net of the FY2020 P&L's own disclosed 'Fair value "
    "gain on valuation of property' £685k less 'Deferred tax liability' £(179)k). This is a genuine one-off "
    "prior-year restatement, not a transcription error. This workbook uses each year's own originally-published "
    "closing figures for FY2018/FY2019 (per that year's own filing) and reproduces the restatement explicitly "
    "as a bridging row on the Statement of Changes in Equity sheet, rather than silently editing FY2019's own "
    "figures or silently absorbing the break.\n"
    "P&L NOTE: the FY2023 filing's Statement of Changes to Equity includes a 'Retained earnings Adjustment' of "
    "£(193)k for FY2023 that is NOT part of that year's Statement of Comprehensive Income (which shows Total "
    "comprehensive income of £1,173k) - this is a genuine one-off equity adjustment outside the P&L, not a "
    "transcription error; it is captured in the Overview's equity bridge as part of 'Other movements, net'. "
    "Similarly, FY2018's, FY2019's, FY2021's and FY2022's Revaluation reserve movements ((9), (9), (159) and 75 "
    "respectively) bypass the P&L's Other Comprehensive Income section entirely in the source document and are "
    "booked directly to equity via the Statement of Changes to Equity - reproduced as disclosed. FY2018 also "
    "carries a £(35)k 'Adjustment on adoption of IFRS 9' at 1 January 2018, likewise outside the P&L.\n"
    + ENTITY_NOTE
)

# ---------------------------------------------------------------
# Sheet: Balance Sheet
# ---------------------------------------------------------------
balance_sheet_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and cash equivalents", {"FY2025": 109027, "FY2024": 100818, "FY2023": 115702, "FY2022": 86759, "FY2021": 2866, "FY2020": 1939, "FY2019": 770, "FY2018": 992}),
    ("DATA", "Loans and advances to banks", {"FY2025": 4053, "FY2024": 7121, "FY2023": 1831, "FY2022": 7501, "FY2021": 21104, "FY2020": 113717, "FY2019": 143924, "FY2018": 136517}),
    ("DATA", "Loans and advances to customers", {"FY2025": 76043, "FY2024": 56807, "FY2023": 34032, "FY2022": 18096, "FY2021": 19359, "FY2020": 20364, "FY2019": 17577, "FY2018": 12708}),
    ("DATA", "Derivatives", {"FY2023": 268, "FY2022": 1146, "FY2021": 88, "FY2020": 657}),
    ("DATA", "Prepayments and accrued income", {"FY2025": 300, "FY2024": 154, "FY2023": 103, "FY2022": 68}),
    ("DATA", "Other assets", {"FY2025": 57, "FY2024": 83, "FY2023": 148, "FY2022": 115, "FY2021": 129, "FY2020": 321, "FY2019": 217, "FY2018": 538}),
    ("DATA", "Investments", {"FY2025": 1414, "FY2024": 3712, "FY2023": 435, "FY2022": 453, "FY2021": 1499, "FY2020": 3139, "FY2019": 4798, "FY2018": 4642}),
    ("DATA", "Property, plant and equipment", {"FY2025": 4079, "FY2024": 4071, "FY2023": 3812, "FY2022": 3450, "FY2021": 3563, "FY2020": 3679, "FY2019": 2981, "FY2018": 2885}),
    ("DATA", "Intangible assets", {"FY2025": 140, "FY2024": 94, "FY2023": 22, "FY2022": 11, "FY2021": 22, "FY2020": 34, "FY2019": 18, "FY2018": 33}),
    ("TOTAL", "Total assets", {"FY2025": 195113, "FY2024": 172860, "FY2023": 156353, "FY2022": 117599, "FY2021": 48630, "FY2020": 143850, "FY2019": 170285, "FY2018": 158315}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Deposits by banks", {"FY2025": 100091, "FY2024": 111334, "FY2023": 120815, "FY2022": 90034, "FY2021": 28123, "FY2020": 124016, "FY2019": 149400, "FY2018": 138890}),
    ("DATA", "Customer account deposits", {"FY2025": 76703, "FY2024": 44538, "FY2023": 19229, "FY2022": 11427, "FY2021": 5811, "FY2020": 4732, "FY2019": 6545, "FY2018": 5367}),
    ("DATA", "Derivatives", {"FY2023": 189, "FY2022": 852, "FY2021": 86, "FY2020": 573}),
    ("DATA", "Accruals", {"FY2025": 162, "FY2024": 258, "FY2023": 357, "FY2022": 236}),
    ("DATA", "Other liabilities", {"FY2025": 2082, "FY2024": 973, "FY2023": 239, "FY2022": 974, "FY2021": 377, "FY2020": 401, "FY2019": 864, "FY2018": 678}),
    ("TOTAL", "Current liabilities", {"FY2025": 179038, "FY2024": 157103, "FY2023": 140829, "FY2022": 103523, "FY2021": 34397, "FY2020": 129722}),
    ("DATA", "Current tax", {"FY2025": 80, "FY2024": 85, "FY2023": 179}),
    ("DATA", "Deferred tax", {"FY2025": 502, "FY2024": 502, "FY2023": 534, "FY2022": 245, "FY2021": 331, "FY2020": 179}),
    ("TOTAL", "Total liabilities", {"FY2025": 179620, "FY2024": 157690, "FY2023": 141542, "FY2022": 103768, "FY2021": 34728, "FY2020": 129901, "FY2019": 156809, "FY2018": 144935}),
    ("SECTION", "Equity", {}),
    ("DATA", "Share capital", {"FY2025": 15000, "FY2024": 15000, "FY2023": 15000, "FY2022": 15000, "FY2021": 15000, "FY2020": 15000, "FY2019": 15000, "FY2018": 15000}),
    ("DATA", "Revaluation reserve", {"FY2025": 1136, "FY2024": 1136, "FY2023": 1104, "FY2022": 820, "FY2021": 745, "FY2020": 904, "FY2019": 408, "FY2018": 417}),
    ("DATA", "Accumulated losses", {"FY2025": -643, "FY2024": -966, "FY2023": -1293, "FY2022": -1989, "FY2021": -1843, "FY2020": -1955, "FY2019": -1932, "FY2018": -2037}),
    ("TOTAL", "Equity shareholders' funds", {"FY2025": 15493, "FY2024": 15170, "FY2023": 14811, "FY2022": 13831, "FY2021": 13902, "FY2020": 13949, "FY2019": 13476, "FY2018": 13380}),
    ("TOTAL", "Total liabilities and equity", {"FY2025": 195113, "FY2024": 172860, "FY2023": 156353, "FY2022": 117599, "FY2021": 48630, "FY2020": 143850, "FY2019": 170285, "FY2018": 158315}),
]

bw.add_balance_sheet_sheet(
    title="Bank of Ceylon (UK) Limited — Statement of Financial Position",
    subtitle="Bank of Ceylon (UK) Limited (own entity basis), £'000",
    rows=balance_sheet_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=46,
    source_height=260,
)

# ---------------------------------------------------------------
# Sheet: Profit & Loss
# ---------------------------------------------------------------
income_statement_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest income", {"FY2025": 8926, "FY2024": 9265, "FY2023": 6466, "FY2022": 2795, "FY2021": 1918, "FY2020": 1788, "FY2019": 2348, "FY2018": 1835}),
    ("DATA", "Interest expense", {"FY2025": -6758, "FY2024": -6885, "FY2023": -4272, "FY2022": -1084, "FY2021": -229, "FY2020": -382, "FY2019": -918, "FY2018": -467}),
    ("TOTAL", "Net interest income", {"FY2025": 2168, "FY2024": 2380, "FY2023": 2194, "FY2022": 1711, "FY2021": 1689, "FY2020": 1406, "FY2019": 1430, "FY2018": 1368}),
    ("DATA", "Fees and commission income", {"FY2025": 885, "FY2024": 564, "FY2023": 530, "FY2022": 474, "FY2021": 361, "FY2020": 634, "FY2019": 816, "FY2018": 814}),
    ("DATA", "Net gains from foreign exchange transactions", {"FY2025": 108, "FY2024": 97, "FY2023": 421, "FY2022": 193, "FY2021": 50, "FY2020": 119, "FY2019": 81, "FY2018": 119}),
    ("TOTAL", "Net operating income", {"FY2025": 3161, "FY2024": 3041, "FY2023": 3145, "FY2022": 2378, "FY2021": 2100, "FY2020": 2159, "FY2019": 2327, "FY2018": 2301}),
    ("SECTION", "Operating expenses", {}),
    ("DATA", "Personnel expenses", {"FY2025": -1512, "FY2024": -1459, "FY2023": -1302, "FY2022": -1126, "FY2021": -1085, "FY2020": -1112}),
    ("DATA", "Operational expenses", {"FY2025": -1168, "FY2024": -1133, "FY2023": -940, "FY2022": -877, "FY2021": -723, "FY2020": -766}),
    ("DATA", "Administration expenses", {"FY2019": -2065, "FY2018": -2103}),
    ("DATA", "Depreciation", {"FY2025": -84, "FY2024": -120, "FY2023": -116, "FY2022": -106, "FY2021": -107, "FY2020": -97, "FY2019": -57, "FY2018": -56}),
    ("DATA", "Amortisation", {"FY2025": -14, "FY2024": -10, "FY2023": -9, "FY2022": -11, "FY2021": -12, "FY2020": -14, "FY2019": -15, "FY2018": -44}),
    ("DATA", "Impairment (charge)/gain on credit exposure", {"FY2025": -15, "FY2024": 93, "FY2023": 290, "FY2022": -405, "FY2021": -59, "FY2020": -196, "FY2019": -82, "FY2018": -13}),
    ("TOTAL", "Total operating expenses", {"FY2025": -2793, "FY2024": -2629, "FY2023": -2077, "FY2022": -2525, "FY2021": -1986, "FY2020": -2185, "FY2019": -2219, "FY2018": -2216}),
    ("TOTAL", "Profit/(loss) from ordinary activities before tax", {"FY2025": 368, "FY2024": 412, "FY2023": 1068, "FY2022": -147, "FY2021": 114, "FY2020": -26, "FY2019": 108, "FY2018": 85}),
    ("DATA", "Tax charge/(credit) on profit", {"FY2025": -45, "FY2024": -85, "FY2023": -179, "FY2022": 1, "FY2021": -2, "FY2020": 3, "FY2019": -3, "FY2018": 0}),
    ("TOTAL", "Profit/(loss) from ordinary activities after tax", {"FY2025": 323, "FY2024": 327, "FY2023": 889, "FY2022": -146, "FY2021": 112, "FY2020": -23, "FY2019": 105, "FY2018": 85}),
    ("SECTION", "Other comprehensive income", {}),
    ("DATA", "Fair value gain on revaluation of property", {"FY2023": 574}),
    ("DATA", "Deferred tax on revaluation", {"FY2024": 32, "FY2023": -290}),
    ("TOTAL", "Total other comprehensive income", {"FY2025": 0, "FY2024": 32, "FY2023": 284, "FY2022": 0, "FY2021": 0, "FY2020": 0, "FY2019": 0, "FY2018": 0}),
    ("TOTAL", "Total comprehensive income/(loss) for the year", {"FY2025": 323, "FY2024": 359, "FY2023": 1173, "FY2022": -146, "FY2021": 112, "FY2020": -23, "FY2019": 105, "FY2018": 85}),
]

bw.add_income_statement_sheet(
    title="Bank of Ceylon (UK) Limited — Statement of Comprehensive Income",
    subtitle="Bank of Ceylon (UK) Limited (own entity basis), £'000",
    rows=income_statement_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=52,
    source_height=260,
)

# ---------------------------------------------------------------
# Sheet: Statement of Changes in Equity
# ---------------------------------------------------------------
EQUITY_HEADERS = ["Share capital", "Accumulated losses", "Revaluation reserve", "Total equity"]
equity_changes_rows = [
    ("TOTAL", "Balance at 31 December 2017", (15000, -2087, 426, 13339)),
    ("DATA", "Adjustment on adoption of IFRS 9", (None, -35, None, -35)),
    ("TOTAL", "Balance at 1 January 2018", (15000, -2122, 426, 13304)),
    ("DATA", "Profit for the year", (None, 85, None, 85)),
    ("DATA", "Revaluation reserve movement", (None, None, -9, -9)),
    ("TOTAL", "Balance at 31 December 2018", (15000, -2037, 417, 13380)),
    ("DATA", "Profit for the year", (None, 105, None, 105)),
    ("DATA", "Revaluation reserve movement", (None, None, -9, -9)),
    ("TOTAL", "Balance at 31 December 2019", (15000, -1932, 408, 13476)),
    ("DATA", "Prior year restatement - revaluation of office building, net of deferred tax", (None, None, 506, 506)),
    ("TOTAL", "Balance at 1 January 2020 (as restated)", (15000, -1932, 914, 13982)),
    ("DATA", "Loss for the year", (None, -23, None, -23)),
    ("DATA", "Revaluation reserve movement", (None, None, -10, -10)),
    ("TOTAL", "Balance at 31 December 2020", (15000, -1955, 904, 13949)),
    ("DATA", "Total comprehensive income", (None, 112, None, 112)),
    ("DATA", "Revaluation reserve movement", (None, None, -159, -159)),
    ("TOTAL", "Balance at 31 December 2021", (15000, -1843, 745, 13902)),
    ("DATA", "Total comprehensive income", (None, -146, None, -146)),
    ("DATA", "Revaluation reserve movement", (None, None, 75, 75)),
    ("TOTAL", "Balance at 31 December 2022", (15000, -1989, 820, 13831)),
    ("DATA", "Profit for the year", (None, 889, None, 889)),
    ("DATA", "Retained earnings adjustment", (None, -193, None, -193)),
    ("DATA", "Revaluation reserve movement", (None, None, 284, 284)),
    ("TOTAL", "Balance at 31 December 2023", (15000, -1293, 1104, 14811)),
    ("DATA", "Profit for the year", (None, 327, None, 327)),
    ("DATA", "Other comprehensive income", (None, None, 32, 32)),
    ("TOTAL", "Balance at 31 December 2024", (15000, -966, 1136, 15170)),
    ("DATA", "Profit for the year", (None, 323, None, 323)),
    ("TOTAL", "Balance at 31 December 2025", (15000, -643, 1136, 15493)),
]

bw.add_equity_changes_sheet(
    title="Bank of Ceylon (UK) Limited — Statement of Changes to Equity",
    subtitle="Bank of Ceylon (UK) Limited (own entity basis), £'000, chronological (oldest to newest)",
    headers=EQUITY_HEADERS,
    rows=equity_changes_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=42,
    source_height=260,
)

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Cash flows from operating activities", {}),
    ("DATA", "Profit/(loss) before tax", {"FY2025": 368, "FY2024": 412, "FY2023": 1068, "FY2022": -147, "FY2021": 114, "FY2020": -26, "FY2019": 108, "FY2018": 85}),
    ("DATA", "Depreciation of property, plant and equipment", {"FY2025": 84, "FY2024": 120, "FY2023": 116, "FY2022": 106, "FY2021": 107, "FY2020": 97, "FY2019": 57, "FY2018": 56}),
    ("DATA", "Amortisation of intangible assets", {"FY2025": 14, "FY2024": 10, "FY2023": 9, "FY2022": 11, "FY2021": 12, "FY2020": 14, "FY2019": 15, "FY2018": 44}),
    ("DATA", "Impairment charge/(gain) on loans", {"FY2025": 15, "FY2024": -431, "FY2023": -290, "FY2022": 392, "FY2021": 59, "FY2020": 196, "FY2019": 82, "FY2018": 13}),
    ("DATA", "Loans to customers / Loans and advances to customers", {"FY2025": -19255, "FY2024": -22782, "FY2023": -15946, "FY2022": 1260, "FY2021": 1001, "FY2020": -2725, "FY2019": -4869, "FY2018": 784}),
    ("DATA", "Financial instruments (assets) / Investments", {"FY2025": 5370, "FY2024": -7861, "FY2023": 6867, "FY2022": 13513, "FY2021": 1760, "FY2020": 1440, "FY2019": -156, "FY2018": 755}),
    ("DATA", "Other receivables / other assets and derivatives", {"FY2025": -84, "FY2024": 14, "FY2023": -68, "FY2022": -1112, "FY2021": 761, "FY2020": -304, "FY2019": 322, "FY2018": -275}),
    ("DATA", "Loans and advances to banks", {"FY2021": 92438, "FY2020": 30286, "FY2019": -7409, "FY2018": -60541}),
    ("DATA", "Retail deposits / customer accounts", {"FY2025": 32166, "FY2024": 25309, "FY2023": 7802, "FY2022": 5616, "FY2021": 1079, "FY2020": -1813, "FY2019": 1178, "FY2018": 653}),
    ("DATA", "Financial instruments (liabilities) / deposits by bank", {"FY2025": -11243, "FY2024": -9670, "FY2023": 30118, "FY2022": 61911, "FY2021": -95893, "FY2020": -25384, "FY2019": 10510, "FY2018": 58056}),
    ("DATA", "Other liabilities and derivatives", {"FY2025": 1013, "FY2024": 635, "FY2023": -617, "FY2022": 1598, "FY2021": -511, "FY2020": -463, "FY2019": 102, "FY2018": 241}),
    ("DATA", "Corporate tax paid", {"FY2025": -87, "FY2024": -179}),
    ("TOTAL", "Net cash flow from operating activities", {"FY2025": 8361, "FY2024": -14423, "FY2023": 29059, "FY2022": 83148, "FY2021": 927, "FY2020": 1318, "FY2019": -60, "FY2018": -129}),
    ("SECTION", "Cash flows from investing activities", {}),
    ("DATA", "Purchase of property, plant and equipment / acquisition of fixed assets", {"FY2025": -152, "FY2024": -461, "FY2023": -116, "FY2022": -2, "FY2021": 0, "FY2020": -149, "FY2019": -162, "FY2018": -21}),
    ("TOTAL", "Net cash flow from investing activities", {"FY2025": -152, "FY2024": -461, "FY2023": -116, "FY2022": -2, "FY2021": 0, "FY2020": -149, "FY2019": -162, "FY2018": -21}),
    ("SECTION", "Cash flows from financing activities", {}),
    ("DATA", "Repayment on investments", {"FY2023": 0, "FY2022": 747}),
    ("TOTAL", "Net cash flow from financing activities", {"FY2025": 0, "FY2024": 0, "FY2023": 0, "FY2022": 747, "FY2021": 0, "FY2020": 0, "FY2019": 0, "FY2018": 0}),
    ("TOTAL", "Net increase/(decrease) in cash and cash equivalents", {"FY2025": 8209, "FY2024": -14884, "FY2023": 28943, "FY2022": 83893, "FY2021": 927, "FY2020": 1169, "FY2019": -222, "FY2018": -150}),
    ("DATA", "Opening cash and cash equivalents", {"FY2025": 100818, "FY2024": 115702, "FY2023": 86759, "FY2022": 2866, "FY2021": 1939, "FY2020": 770, "FY2019": 992, "FY2018": 1142}),
    ("TOTAL", "Closing cash and cash equivalents", {"FY2025": 109027, "FY2024": 100818, "FY2023": 115702, "FY2022": 86759, "FY2021": 2866, "FY2020": 1939, "FY2019": 770, "FY2018": 992}),
]

bw.add_cash_flow_sheet(
    title="Bank of Ceylon (UK) Limited — Statement of Cash Flows",
    subtitle="Bank of Ceylon (UK) Limited (own entity basis), £'000 unless stated",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=56,
    source_height=220,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Sheet: Asset Quality
# ---------------------------------------------------------------
ASSET_QUALITY_SOURCES = (
    "Sources - Bank of Ceylon (UK) Limited's own Companies House filings (visually transcribed, see the "
    "Balance Sheet sheet's source note for the OCR-equivalent method):\n"
    f"FY2025 & FY2024 (by IFRS 9 stage): Full accounts made up to 31 December 2025, p.39 ('Credit exposure by "
    f"stage' note) - {CH2025_URL}\n"
    f"FY2023 & FY2022 (by product): Full accounts made up to 31 December 2023, p.57 (Note 15) - {CH2023_URL}\n"
    f"FY2021 (by product): Full accounts made up to 31 December 2021, p.43 (Note 14) - {CH2021_URL}\n"
    f"FY2020 (by product, own year): Full accounts made up to 31 December 2020, p.44 (Note 13) - {CH2020_URL}\n"
    f"FY2019 (by product, own year): Full accounts made up to 31 December 2019, p.42 (Note 15) - {CH2019_URL}\n"
    f"FY2018 (by product, own year): Full accounts made up to 31 December 2018, p.38 (Note 16) - {CH2018_URL}\n"
    "STRUCTURAL BREAK: the FY2025 filing introduced a new IFRS 9 stage-level credit exposure disclosure not "
    "present in the earlier filings - FY2025/FY2024 are shown by stage (Stage 1/2/3), FY2023/FY2022/FY2021/"
    "FY2020/FY2019/FY2018 are shown by product (Personal/Commercial) instead, since that is genuinely all that "
    "was disclosed those years. The two breakdowns are NOT additive across the table (different bases) - both "
    "are transcribed as their own source discloses, not forced into one shape.\n"
    "FY2024's ECL allowance on loans and advances to customers (£26k) is DERIVED (gross £56,833k less carrying "
    "£56,807k per the Balance Sheet/Note 15), not a directly disclosed per-portfolio figure for that year - the "
    "FY2025 filing's reconciliation table (gross->ECL->net) is only given for FY2025 itself. FY2019's own "
    "filing's comparative FY2018 note-level gross/impairment figures (Personal 8,895/(16), Commercial 8,770/"
    "(23)) differ slightly from FY2018's own filing (Personal 8,874/(16), Commercial 8,742/(23)) - each year's "
    "own filing is used for its own year, consistent with this project's standard convention; the ~£49k "
    "difference is immaterial (<0.3% of gross loans) and not separately flagged as a restatement.\n"
    + ENTITY_NOTE
)

asset_quality_rows = [
    ("SECTION", "Loans and advances to customers - by IFRS 9 stage (FY2024-FY2025 only)", {}),
    ("DATA", "Stage 1 (performing)", {"FY2025": 72088, "FY2024": 55739}),
    ("DATA", "Stage 2 (significant increase in credit risk)", {"FY2025": 3646, "FY2024": 1094}),
    ("DATA", "Stage 3 (credit-impaired)", {"FY2025": 354, "FY2024": 0}),
    ("TOTAL", "Gross loans and advances to customers (by stage)", {"FY2025": 76088, "FY2024": 56833}),
    ("SECTION", "Loans and advances to customers - by product (FY2018-FY2023 only)", {}),
    ("DATA", "Personal loans and advances (gross)", {"FY2023": 30188, "FY2022": 10750, "FY2021": 11277, "FY2020": 10899, "FY2019": 8874, "FY2018": 5492}),
    ("DATA", "Commercial loans and advances (gross)", {"FY2023": 3862, "FY2022": 7355, "FY2021": 8088, "FY2020": 9467, "FY2019": 8742, "FY2018": 7248}),
    ("TOTAL", "Gross loans and advances to customers (by product)", {"FY2023": 34050, "FY2022": 18105, "FY2021": 19365, "FY2020": 20366, "FY2019": 17616, "FY2018": 12740}),
    ("SECTION", "Impairment", {}),
    ("DATA", "ECL allowance on loans and advances to customers", {"FY2025": -45, "FY2024": -26, "FY2023": -18, "FY2022": -9, "FY2021": -6, "FY2020": -2, "FY2019": -39, "FY2018": -32}),
    ("TOTAL", "Net loans and advances to customers", {"FY2025": 76043, "FY2024": 56807, "FY2023": 34032, "FY2022": 18096, "FY2021": 19359, "FY2020": 20364, "FY2019": 17577, "FY2018": 12708}),
    ("SECTION", "Asset quality ratios", {}),
    ("DATA", "ECL coverage ratio (ECL allowance / gross loans)", {"FY2025": "0.06%", "FY2024": "0.05%", "FY2023": "0.05%", "FY2022": "0.05%", "FY2021": "0.03%", "FY2020": "0.01%", "FY2019": "0.22%", "FY2018": "0.25%"}),
    ("DATA", "Stage 3 / NPL ratio (Stage 3 gross / total gross)", {"FY2025": "0.47%", "FY2024": "0.00%"}),
]

bw.add_asset_quality_sheet(
    title="Bank of Ceylon (UK) Limited — Asset Quality / Credit Risk Disclosures",
    subtitle="Bank of Ceylon (UK) Limited (own entity basis), £'000 unless stated",
    rows=asset_quality_rows,
    sources_text=ASSET_QUALITY_SOURCES,
    first_col_width=58,
    source_height=220,
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, note=None):
    bw.add_metric_sheet(name, unit, rows_data, p3_sources(), note=note, first_col_width=46, source_height=200)

FY2022_CAPITAL_NOTE = (
    "FY2022 (£13,959k) added 2026-09-15 and is the ONLY Pillar 3 metric recoverable for that year. It is not "
    "from a Pillar 3 document - none was ever published for FY2022 - but from the Bank's own audited FY2022 "
    "statutory accounts, Note 28 'Capital Management', which states the regulatory CET1 capital after IFRS 9 "
    "transitional relief as GBP 13,958,648 (and, on a fully loaded basis, GBP 13,734,398). The transitional "
    "figure is used because it is the basis the surrounding Pillar 3 years are on: the same sentence's own "
    "31 December 2021 comparative (GBP 13,425,750) matches the FY2021 Pillar 3 document's £13,424k to within "
    "£2k. See the source note for the full quotation, URL and the OCR method."
)

# ---------------------------------------------------------------
# FY2022 capital: three different figures, three different sources, NOT reconciled.
# Recorded on separate labelled rows per this project's validation-gate rule.
# ---------------------------------------------------------------
FY2022_CONFLICT_NOTE = (
    "UNRESOLVED FY2022 CONFLICT (documented 2026-09-15, deliberately NOT resolved). Three different FY2022 CET1 "
    "figures are stated by the Bank's own audited accounts, on three different (or unstated) bases. They are "
    "shown on separate labelled rows above; none is preferred, averaged, or inferred to be 'the right one'.\n"
    "  (a) GBP 13,958,648 -> £13,959k. FY2022 Annual Financial Report, Note 28 'Capital Management' (p.60): "
    "'The regulatory CET1 capital after adjusting for transitional relief under IFRS9 would be GBP 13,958,648.' "
    "BASIS: IFRS 9 transitional relief applied - that same report's Strategic Report (p.20) states 'The Bank has "
    "adopted the CET1 addback percentage of 50% for relevant provisions raised from 1 January 2022 in arriving "
    "at the regulatory capital, as set out in note 28.' This is the figure the earlier pass entered, on the "
    "reasoning that the same sentence's 31 December 2021 comparative (GBP 13,425,750) matches the FY2021 Pillar "
    "3 document's own £13,424k to within £2k, i.e. it is the basis the surrounding Pillar 3 years are on. It is "
    "retained unchanged as the primary series rather than silently overwritten.\n"
    "  (b) GBP 13,734,398 -> £13,734k. Same Note 28, same sentence: 'after deducting book value of intangible "
    "assets from shareholder funds is GBP 13,734,398 on a fully loaded basis.' BASIS: fully loaded (IFRS 9 "
    "transitional relief NOT applied). Stated explicitly by the Bank.\n"
    "  (c) GBP 12,852,280 -> £12,852k. FY2023 Annual Financial Report, Strategic Report p.8 'CAPITAL', as the "
    "2022 comparative to that year's own GBP 13,684,688. BASIS: NOT STATED anywhere in the FY2023 document. It "
    "is £1,106k below (a) and £882k below (b), so it is neither the transitional nor the fully loaded figure "
    "from the FY2022 accounts - it is either a different basis again or an unannounced restatement. The FY2023 "
    "accounts contain no restatement note covering it, and its own Note 32 carries no 2022 comparative at all, "
    "so this workbook cannot and does not determine which.\n"
    "The FY2022 ratios (CET1 44%, Total capital 48%) and Total capital (GBP 13,818,899) come from that same "
    "FY2023 p.8 sentence and therefore belong with basis (c). They are kept on rows labelled as (c) so they are "
    "never read as ratios of the basis-(a) capital sitting on the primary row.\n"
    "ALL FOUR OCR'd FIGURES WERE VISUALLY VERIFIED: the FY2022 and FY2023 accounts are image-only scans, so "
    "each page was re-rendered at 400 dpi and read directly to confirm every digit, in addition to the tesseract "
    "pass. Digit-level confirmation obtained for 13,958,648 / 13,734,398 / 13,425,750 (FY2022 Note 28) and for "
    "13,684,688 / 12,852,280 / 43% / 44% / 14,788,668 / 13,818,899 / 46% / 48% (FY2023 p.8).\n"
    "VALIDATION GATE - the FY2023 figures in that same sentence PASS and confirm the sentence is being read "
    "correctly: its GBP 13,684,688 CET1 and GBP 14,788,668 total capital reproduce the FY2024 Pillar 3 "
    "document's own 2023 comparative column exactly (£13,685k and £14,789k), and its 43%/46% are those same "
    "sheets' 42.5%/45.9% rounded to whole percents. So the sentence is reliable as to FY2023; it is only its "
    "FY2022 comparative that cannot be reconciled.\n"
    "MINOR INTERNAL INCONSISTENCY, noted not corrected: the FY2023 accounts state FY2023 CET1 as GBP 13,684,688 "
    "in the Strategic Report (p.8) and GBP 13,684,668 in Note 32 (p.67) - a GBP 20 discrepancy inside one "
    "document. Both were visually verified at 400 dpi; both round to £13,685k, which is what this workbook holds "
    "and what the FY2024 Pillar 3 independently confirms."
)

# ---------------------------------------------------------------
# Sheet: KM1 Key Metrics (KM1-005) - documented NOT APPLICABLE
# ---------------------------------------------------------------
# BOCUK publishes a bank-styled key-metrics summary, not the prescribed
# template. Applying the row-set test (map rule 8) to every edition it has ever
# published, in full, rather than keying on the token "KM1" or on numbering.
KM1_SOURCES = (
    "UK KM1 - KEY METRICS TEMPLATE: NOT USED BY THIS BANK IN ANY YEAR.\n"
    "BOCUK publishes a Pillar 3 disclosure in most years and does head a section 'Key metrics' in several of "
    "them - but what it prints there is the bank's own summary, not the prescribed template. That is a "
    "different finding from 'no Pillar 3 is published', and it is reached by the row-set test (map rule 8) "
    "rather than by searching for the token 'KM1'. Every edition the bank has published was fetched and read "
    "for this, 2026-09-16.\n"
    "\n"
    "WHAT EACH EDITION ACTUALLY PRINTS:\n"
    f"  FY2025 (p.3, '1.1 Key Metrics') - {P3_2025_URL}: an UNNUMBERED table, £'000, two dates, with sections "
    "Available Capital / Risk-Weighted Exposure Amount / Capital Ratios / Leverage / Liquidity Coverage Ratio "
    "/ Net Stable Funding Ratio.\n"
    f"  FY2024 (p.4, '1.1 Key Metrics') - {P3_2024_URL}: the same unnumbered table, plus a buffer block "
    "(capital conservation, countercyclical, combined buffer, overall capital requirements) that the FY2025 "
    "edition drops.\n"
    f"  FY2021 (p.3) and FY2020 (p.3) - {P3_2021_URL} / {P3_2020_URL}: 'KEY METRICS' is not a table at all but "
    "six INFOGRAPHIC TILES (for FY2021: £13.4M common equity tier 1 capital, £14.3M regulatory capital, 54.8% "
    "common equity tier 1 ratio, 57.8% total capital ratio, £24.5M total risk weighted, 345% liquidity "
    "ratio).\n"
    f"  FY2019 (p.6) and FY2018 (p.5) - {P3_2019_URL} / {P3_2018_URL}: an unnumbered 'Key metrics' table, "
    "£000s, two dates, which additionally carries IFRS 9 transitional-arrangement variants of most rows, has "
    "an LCR block but NO NSFR block at all.\n"
    "  FY2022 and FY2023: no Pillar 3 document exists - both are absent from the bank's own published list "
    "(re-confirmed against that list 2026-09-16).\n"
    "\n"
    "WHY NONE OF THESE IS THE TEMPLATE. The row-set test asks whether a table carries the template's ROW SET, "
    "whatever its title and whether or not its rows are numbered - an unnumbered table can certainly be the "
    "template. These are not, and the reason is the same in every edition: NO edition, in any year, prints "
    "Tier 1 capital (row 2), Tier 1 ratio (row 6), or ANY of the SREP rows (UK 7a, UK 7b, UK 7c, UK 7d). "
    "Those are the spine of the template, not optional extras, and their absence is structural rather than a "
    "year's drift: it holds across 2018, 2019, 2020, 2021, 2024 and 2025 alike. No edition numbers its rows "
    "either, and the row set itself moves materially between editions (NSFR absent before FY2024; the buffer "
    "block present in FY2024 and gone in FY2025; tiles instead of a table in FY2020-FY2021). Mapping this "
    "summary onto template row numbers would invent a correspondence the bank never published, which is the "
    "specific error map rule 8 exists to prevent.\n"
    "\n"
    "WHAT THIS BANK'S FIGURES DO SUPPORT is the eleven single-metric sheets in this workbook, which carry "
    "them under their own citations, on their own stated bases, and with their own documented FY2022 "
    "conflict. Nothing on those sheets is affected by this one being blank.\n"
    "\n"
    "LATEST-EDITION CHECK, 2026-09-16: the bank's own index "
    "(https://bankofceylon.co.uk/financial-statements/, HTTP 200, not blocked) lists Pillar 3 disclosures for "
    "31 December 2025, 2024, 2021, 2020, 2019 and 2018 - and nothing for 2022 or 2023, which corroborates the "
    "gap recorded above from the bank's own publication list. The newest is the 31 December 2025 edition, "
    "already carried and cited by this script. NONE NEWER."
)

# GA-020 (2026-09-19): each year says WHICH outcome it is, on the edition-by-
# edition evidence in KM1_SOURCES.
KM1_CELLS = {y: ("Not published – the bank's Pillar 3 'Key metrics' (2018-21, 2024-25 eds) is its own summary, not "
                 "UK KM1: no Tier 1, Tier 1 ratio or SREP rows in any edition (row-set test, 2026-09-16)")
             for y in YEARS}
for _y in ("FY2022", "FY2023"):
    KM1_CELLS[_y] = ("Not published – no Pillar 3 for this year: the bank's own index (bankofceylon.co.uk/"
                     "financial-statements, re-read 2026-09-19) lists 2018-21 and 2024-25 only")
KM1_CELLS["FY2013"] = ("Not published – the recovered 31 Dec 2013 Pillar 3 (Wayback) pre-dates the KM1 template "
                       "and prints no such table")

bw.add_km1_sheet(
    title="Bank of Ceylon (UK) Limited - KM1 Key Metrics",
    subtitle="Not applicable: this bank publishes Pillar 3 disclosures but does not use the UK KM1 template in "
             "any year. What it heads 'Key metrics' is its own unnumbered summary (and, in FY2020-FY2021, six "
             "infographic tiles), which omits Tier 1 capital, the Tier 1 ratio and every SREP row in every "
             "edition. See the sources note for the row-set test applied edition by edition.",
    rows=[("DATA", "UK KM1 - Key metrics template: not used by this bank in any year",
           KM1_CELLS)],
    sources_text=KM1_SOURCES,
    first_col_width=64,
    source_height=300,
    years=YEARS,
)

metric(
    "CET1 Capital", "£'000",
    [
        ("Common Equity Tier 1 (CET1) capital", {"FY2025": 14217, "FY2024": 13940, "FY2023": 13685, "FY2022": 13959, "FY2021": 13424, "FY2020": 13338, "FY2019": 13569, "FY2018": 13393, "FY2013": 13436}),
        ("FY2022 alternative (b): CET1 capital, fully loaded basis (FY2022 accounts, Note 28)", {"FY2022": 13734}),
        ("FY2022 alternative (c): CET1 capital per the FY2023 accounts' 2022 comparative (basis not stated)", {"FY2022": 12852}),
    ],
    note=FY2022_CAPITAL_NOTE + "\n\n" + FY2022_CONFLICT_NOTE
         + "\n\nFY2013 13,436 is the recovered 31 December 2013 edition's own printed 'Core Tier 1 capital' line "
           "(Share capital 15,000 + Fair value reserve 31 - Cumulative revenue losses 1,073 = 13,958, less Intangible "
           "assets 522). It is placed on the primary row on the same convention as every other year here: the Bank has "
           "no Additional Tier 1 capital in any year, and that edition's capital table shows Tier 1 consisting only of "
           "share capital and reserves. Strictly, CET1 as a defined CRD IV measure did not apply at 31 December 2013 - "
           "though this edition heads its own capital table 'CRD IV' - so the figure is a Core Tier 1 measure carried "
           "under a CET1 heading. Four intervening editions (FY2017-FY2014) are not recoverable and those columns are "
           "omitted rather than shown blank; see the source note.",
)

metric(
    "CET1 Ratio", "% of RWA",
    [
        ("Common Equity Tier 1 (CET1) ratio", {"FY2025": "20.1%", "FY2024": "22.7%", "FY2023": "42.5%", "FY2021": "54.8%", "FY2020": "34.3%", "FY2019": "57.5%", "FY2018": "46.9%"}),
        ("FY2022 per the FY2023 accounts' 2022 comparative, basis (c) (whole percent as stated)", {"FY2022": "44%"}),
    ],
    note="FY2022 ADDED 2026-09-15 on a separate row, not on the primary row. The FY2023 accounts' Strategic "
         "Report (p.8) states the FY2022 CET1 ratio as 44% alongside a FY2022 CET1 capital of GBP 12,852,280 - "
         "basis (c) in the conflict note below. It is NOT placed on the primary row because the primary CET1 "
         "Capital row for FY2022 holds basis (a) (GBP 13,958,648, IFRS 9 transitional), and a 44% derived from a "
         "different capital figure must never be read as a ratio of that one. No FY2022 ratio is available on "
         "basis (a) or (b): the FY2022 accounts state no capital ratio anywhere, and no FY2022 Pillar 3 document "
         "exists. The 44% is also a whole percent as printed, not a one-decimal regulatory figure like the "
         "surrounding Pillar 3 years.\n"
         "FY2013 IS BLANK BY DESIGN, not unresearched: the recovered 31 December 2013 edition discloses no "
         "risk-weighted-asset figure and no capital ratio of any kind - it publishes the Pillar 1 CAPITAL "
         "requirement (expressly '8% of the risk weighted exposure amounts') instead - so there is no denominator "
         "to state and no ratio to transcribe. Grossing the 2,770 Pillar 1 requirement up to an implied ~34,625 RWA "
         "and dividing would be back-solving, and is deliberately not done.\n\n" + FY2022_CONFLICT_NOTE,
)

metric(
    "Tier 1 Capital", "£'000",
    [("Tier 1 capital", {"FY2025": 14217, "FY2024": 13940, "FY2023": 13685, "FY2022": 13959, "FY2021": 13424, "FY2020": 13338, "FY2019": 13569, "FY2018": 13393, "FY2013": 13436})],
    note="BOCUK has no Additional Tier 1 capital in any year - Tier 1 capital equals CET1 capital throughout. "
         "For FY2022 specifically this is stated by the Bank itself in the same FY2022 accounts: its Strategic "
         "Report's 'Capital Adequacy' section says 'The Bank's regulatory capital comprises ordinary share "
         "capital, revaluation reserves and retained earnings' - no AT1 instrument exists, so the CET1 figure "
         "below is also the Tier 1 figure.\n" + FY2022_CAPITAL_NOTE
         + "\n\nFY2022 ALTERNATIVE BASES: two further FY2022 CET1 figures exist (fully loaded GBP 13,734,398, and "
           "GBP 12,852,280 per the FY2023 accounts' comparative). They are carried on the CET1 Capital sheet's "
           "own labelled rows and are deliberately NOT mirrored here, because the Bank never states a Tier 1 "
           "figure on either of those bases - equating them to Tier 1 would be this workbook's inference rather "
           "than the Bank's statement. See the CET1 Capital sheet for the full conflict.",
)

metric(
    "Tier 1 Ratio", "% of RWA",
    [("Tier 1 ratio", {"FY2025": "20.1%", "FY2024": "22.7%", "FY2023": "42.5%", "FY2022": "Not published - no FY2022 Pillar 3; accounts give a CET1 ratio only", "FY2021": "54.8%", "FY2020": "34.3%", "FY2019": "57.5%", "FY2018": "46.9%"})],
    note="Equal to the CET1 ratio - no Additional Tier 1 capital in any year. FY2022 CARRIES A RECORDED ABSENCE "
         "RATHER THAN A BLANK (2026-09-19): the finding below was already established and was invisible to a "
         "reader of the grid and to the gap census, both of which saw only an empty cell. The only "
         "FY2022 ratio the Bank ever states (44%) is captioned a CET1 ratio in the FY2023 accounts' Strategic "
         "Report p.8, and is carried on the CET1 Ratio sheet's own labelled row. It is not copied across, "
         "because restating a CET1-captioned ratio as a Tier 1 ratio would be this workbook's inference; the "
         "FY2022 accounts state no capital ratio at all and no FY2022 Pillar 3 document exists. FY2013 is likewise "
         "blank: the recovered 31 December 2013 edition discloses no RWA and no capital ratio at all, only the "
         "Pillar 1 capital requirement, and nothing is derived from it. See the CET1 Ratio sheet and sources.",
)

metric(
    "Total Capital", "£'000",
    [
        ("Total capital (own funds)", {"FY2025": 15353, "FY2024": 15076, "FY2023": 14789, "FY2021": 14169, "FY2020": 14242, "FY2019": 13569, "FY2018": 13393, "FY2013": 13899}),
        ("FY2022 per the FY2023 accounts' 2022 comparative, basis (c)", {"FY2022": 13819}),
    ],
    note="FY2022 ADDED 2026-09-15 on a separate row (GBP 13,818,899 -> £13,819k), correcting this sheet's "
         "previous 'no FY2022 total capital is disclosed anywhere' claim. It IS disclosed: the FY2023 accounts' "
         "Strategic Report p.8 gives 'a total capital of GBP 14,788,668 (2022-13,818,899)'. It sits on its own "
         "row rather than the primary row because it belongs to basis (c) - the same sentence's FY2022 CET1 of "
         "GBP 12,852,280 - whereas the primary CET1/Tier 1 row for FY2022 holds basis (a) (GBP 13,958,648). "
         "Putting £13,819k on the primary row would create an internally inconsistent FY2022 capital stack "
         "across sheets. Note also that £13,819k - £12,852k = £967k, which is NOT the FY2022 revaluation reserve "
         "of £820k, so the 'Tier 2 = revaluation reserve' pattern observed in other years does not hold on this "
         "basis - one more reason the basis is genuinely different and is not resolved here. Total capital on "
         "bases (a) and (b) remains undisclosed and blank: the FY2022 accounts state no Tier 2 figure at all. "
         "In the years it IS disclosed, Tier 2 does equal the revaluation reserve exactly "
         "(FY2021 14,169-13,424 = 745 = the reserve; FY2023 14,789-13,685 = 1,104 = the reserve), so a basis-(a) "
         "FY2022 total of 13,959 + 820 = 14,779 is plausible - but that is an arithmetic inference from a "
         "pattern, not a disclosed figure, and is not entered. "
         "FY2018/FY2019: Total capital equals CET1 capital - the Pillar 3 documents for those years show no "
         "Tier 2 capital. From FY2020 on, the Bank's revaluation reserve is recognised as Tier 2 capital, "
         "adding to Total capital over and above CET1 - see the FY2020 Pillar 3 document's own Section 4.1. "
         "This is a genuine methodology change disclosed by the Bank, not a transcription inconsistency. "
         "REVISED 2026-09-15 BY THE RECOVERED FY2013 EDITION: 'from FY2020 on' describes the FY2018-FY2025 window "
         "correctly but is not the start of the practice. The 31 December 2013 edition already recognises the "
         "revaluation reserve as Tier 2 capital (Tier 2 Capital: Revaluation reserve 463), so the genuine anomaly "
         "is FY2018/FY2019, the two years with no Tier 2 at all. FY2013's 13,899 on the primary row above is that "
         "edition's own printed 'Total Regulatory Capital' line - a stated total, not Core Tier 1 plus the reserve "
         "computed here (though it does equal 13,436 + 463, which is what confirms the reading)."
         + "\n\n" + FY2022_CONFLICT_NOTE,
)

metric(
    "Total Capital Ratio", "% of RWA",
    [
        ("Total capital ratio", {"FY2025": "21.7%", "FY2024": "24.6%", "FY2023": "45.9%", "FY2021": "57.8%", "FY2020": "36.7%", "FY2019": "57.5%", "FY2018": "46.9%"}),
        ("FY2022 per the FY2023 accounts' 2022 comparative, basis (c) (whole percent as stated)", {"FY2022": "48%"}),
    ],
    note="FY2022 ADDED 2026-09-15 on a separate row: the FY2023 accounts' Strategic Report p.8 states the total "
         "capital ratio as '46% at 31st of December 2023 (2022: 48%)'. Basis (c), same sentence as that year's "
         "GBP 12,852,280 CET1 and GBP 13,818,899 total capital - see the conflict note below. Kept off the "
         "primary row for the same reason as the CET1 Ratio sheet. The FY2023 value in that sentence (46%) is "
         "this sheet's own 45.9% rounded to a whole percent, which is what confirms the sentence is being read "
         "correctly.\n\n"
         "LABEL TRAP CHECKED AND RESOLVED (FY2024) - recorded because this project has mapped a ratio to the "
         "wrong sheet three times (Bank Saderat, Monument, Alpha Bank). The FY2024 accounts contain the sentence "
         "'The CET1 total capital ratio at the end of 2024 was 24% (2023 46%) see note 32.' Despite saying "
         "'CET1', BOTH figures are TOTAL capital ratios, not CET1 ratios. Verified against the FY2024 Pillar 3 "
         "document's own Key Metrics table (section 1.1) and its section 6 capital table, which independently "
         "agree: FY2024 CET1 ratio 22.7% and total capital ratio 24.6%; FY2023 CET1 ratio 42.5% and total "
         "capital ratio 45.9%. 24% matches 24.6% and cannot be 22.7%; 46% matches 45.9% exactly (and matches "
         "the FY2023 accounts' own 46% total capital ratio) and is nowhere near the 43%/42.5% CET1 ratio. So "
         "neither figure was mapped anywhere - this sheet and the CET1 Ratio sheet already carry the correct "
         "Pillar 3 KM1 values for FY2024/FY2023, and the FY2024 narrative sentence is simply mislabelled.\n"
         "RELATED FY2024 UNRELIABILITY, flagged not merged: the FY2024 accounts' Strategic Report p.6 CAPITAL "
         "paragraph gives FY2024 CET1 as GBP 13,939,366 (agrees with the Pillar 3's £13,940k) but its FY2023 "
         "comparatives as GBP 14,573,608 and 45% - neither of which matches the FY2023 accounts' own "
         "GBP 13,684,688 / 43% nor the Pillar 3's £13,685k / 42.5%. Two independent sources agree at £13,685k, "
         "so the validation gate keeps the existing figure and the FY2024 comparative is treated as the outlier. "
         "That same paragraph also gives FY2024 total capital as GBP 14,717,109 against the Pillar 3 KM1's "
         "£15,076k; the KM1 regulatory template is retained on the primary row above and the narrative figure is "
         "not blended in.\n"
         "FY2013 is blank for the same structural reason as the other FY2013 ratio cells: the recovered 31 December "
         "2013 edition publishes the Pillar 1 capital requirement and no RWA or ratio anywhere. See sources.\n\n" + FY2022_CONFLICT_NOTE,
)

metric(
    "Total RWAs", "£'000",
    [("Total risk-weighted exposure amount", {"FY2025": 70733, "FY2024": 61344, "FY2023": 32187, "FY2022": "Not published - no FY2022 Pillar 3; no RWA in the FY2022/FY2023 accounts", "FY2021": 29052, "FY2020": 38848, "FY2019": 28513, "FY2018": 24492}),
     ("Memo - figure the Bank itself printed as 'Total RWAs' that year (credit and counterparty credit risk ONLY; superseded above for FY2019/FY2021 - see note)",
      {"FY2021": 24509, "FY2019": 23604, "FY2018": 24492})],
    note="FY2013 IS BLANK, AND DELIBERATELY SO. The recovered 31 December 2013 edition discloses no "
         "risk-weighted-asset amount anywhere - it publishes the Pillar 1 CAPITAL requirement instead (Credit "
         "2,454 + Market 24 + Operational 292 = Total Pillar 1 Requirement 2,770), which its own text defines as "
         "'8% of the risk weighted exposure amounts'. Dividing 2,770 by 8% would yield an apparent ~34,625 that "
         "no document states. Given that this bank's printed 'Total RWAs' has already been shown to be a "
         "credit-risk subtotal in FY2018/FY2019/FY2021, inventing a FY2013 total by arithmetic is exactly the "
         "wrong move; the disclosed capital requirements are carried on the RWA Breakdown sheet's own labelled "
         "rows instead. See sources.\n"
         "CORRECTION 2026-09-15 (RWA cross-sheet sweep). FY2021 corrected 24,509 -> 29,052 and FY2019 corrected "
         "23,604 -> 28,513. Both superseded values are retained on the memo row above rather than discarded.\n"
         "WHY FY2021 WAS WRONG: the FY2021 Pillar 3 Disclosures' own section 5.4 'Own Funds Requirement' table "
         "(p.16) carries an explicit RWA column, and in that column it prints Credit and Counterparty Credit "
         "Risk 24,509 (the exposure-class subtotal: Central Governments & Central Banks 2,079 + Institutions "
         "704 + Corporates-SME 4,523 + Financial corporates 6,556 + Mortgages 6,426 + Retail 529 + Other 3,692), "
         "Market Risk 302, Operational Risk (Basic Indicator Approach) 4,241, and 'Total Pillar 1 Requirement "
         "29,052'. So 29,052 is a figure the Bank PRINTS in its own RWA column - it is transcribed here, not "
         "derived - and the 24,509 that section 4.1 labels 'Risk Weighted Assets' is that same table's "
         "credit-risk subtotal. Section 4.1's accompanying claim that 'the total for Risk Weighted Assets is "
         "the amount reported in the Bank's regulatory returns' is contradicted by its own section 5.4. Note "
         "that BOCUK's printed FY2021 ratios are computed on the credit-only denominator (CET1 13,424 / 24,509 "
         "= 54.77%, matching the printed 54.8%), so - unlike Redwood - the printed ratio here does NOT disprove "
         "the printed total; the same document's own RWA column does. The CET1/Tier 1/Total Capital Ratio "
         "sheets therefore still carry the Bank's printed percentages and will NOT reproduce if divided against "
         "this sheet; that divergence is the Bank's, is deliberate, and must not be 'fixed'.\n"
         "WHY FY2019 WAS WRONG, AND WHERE 28,513 COMES FROM: the FY2019 document has no RWA column at all - its "
         "sections 5.3/5.4 are capital-requirement only (Credit risk 1,888 + Market risk 7 + Operational risk "
         "335 = Total Pillar 1 Requirement 2,230) - and its KM1 'Total RWAs 23,604' is the credit-risk figure "
         "(its printed CET1 ratio of 57.5% uses it: 13,569/23,604 = 57.49%). 28,513 is NOT derived: it is "
         "printed directly in the FY2020 Pillar 3 Disclosures' section 4.1 capital table, whose Risk Weighted "
         "Assets line reads '38,848   28,513' for 2020 and 2019. This is the same route used for Ghana "
         "International's FY2019 correction - the following edition's own statement of the prior year - and is "
         "legitimate where back-solving from a ratio would not be. It is on the FY2020 edition's RESTATED basis "
         "(that edition also restates FY2019's Pillar 1 requirement to 2,281 = credit 1,888 + market 77 + "
         "operational 316, versus the FY2019 edition's own 2,230, alongside the office-building revaluation "
         "restatement documented on the Statement of Changes in Equity sheet), so it will not tie to the RWA "
         "Breakdown sheet's FY2019 own-edition total of 27,876 - that divergence is a restatement and is not to "
         "be reconciled.\n"
         "WHY FY2018 WAS **NOT** CHANGED, THOUGH IT IS WRONG THE SAME WAY: the FY2018 defect is proven "
         "Redwood-style by the document's own arithmetic - its KM1 prints CET1 capital 13,393, Total RWAs "
         "24,492 and a CET1 ratio of 46.9%, but 13,393/24,492 = 54.7%, not 46.9%. The same table's FY2017 "
         "column is internally consistent (13,263/36,385 = 36.45% = the printed 36.5%), so FY2018 is the year "
         "the line switched to credit-only (1,959/0.08 = 24,488, effectively the printed 24,492). No BOCUK "
         "document anywhere prints a FY2018 total risk exposure amount, however: the FY2018 and FY2019 editions "
         "have no RWA column, and the FY2019 edition's comparative simply repeats 24,492. The only candidate "
         "(28,538 = the FY2018 document's own Total Pillar 1 Requirement of 2,283 divided by 8%, which does "
         "reproduce the printed 46.9%) would be a derivation, and this project does not substitute a derived "
         "figure for a disclosed one on this sheet. FY2018 therefore knowingly carries a credit-risk-only "
         "figure, understated by roughly the market + operational component. Treat FY2018 -> FY2019 as a basis "
         "break, not growth.\n"
         "FY2022 is genuinely unobtainable, re-verified 2026-09-15: no FY2022 or FY2023 Pillar 3 document was "
         "ever published, and the FY2022 and FY2023 statutory accounts (both image-only scans, OCR'd page by "
         "page in full) state no RWA figure anywhere - the FY2022 accounts' Note 28 gives only a CET1 amount "
         "and the FY2023 accounts' Note 32 only that year's available capital. "
         "CORRECTION 2026-09-15: this note previously also said 'no ratio is disclosed for FY2022 either' - that "
         "was wrong. The FY2023 accounts' Strategic Report p.8 does state FY2022 ratios (CET1 44%, total capital "
         "48%) alongside a FY2022 CET1 of GBP 12,852,280 and total capital of GBP 13,818,899; all four are now "
         "on the relevant sheets' own labelled rows. That does NOT unblank this sheet: RWA is not back-solved "
         "from capital and a ratio here, and in any case 12,852,280 / 0.44 = ~GBP 29.2m is meaningless precision "
         "off a whole-percent ratio (a 44% printed to the nearest percent spans roughly GBP 28.9m-GBP 29.9m of "
         "RWA). FY2022 Total RWAs stays blank. "
         "FY2020 is the first year whose own Pillar 3 document states a comprehensive Total RWA directly: its "
         "section 5.4 RWA column prints Credit and Counterparty Credit Risk 34,473, Market Risk 187, "
         "Operational Risk 4,188 and 'Total Pillar 1 Requirement 38,848', and its section 4.1 prints the same "
         "38,848 as 'Risk Weighted Assets'. FY2023-FY2025 follow the same (correct) pattern.",
)

RWA_BREAKDOWN_SOURCES = (
    "Sources - Bank of Ceylon (UK) Limited Pillar 3 disclosures, UK OV1-equivalent 'Own Funds Requirement' "
    "exposure-class table (own entity-level basis), £'000:\n"
    f"FY2025: Pillar 3 Disclosures 31 December 2025, p.13 (5.4 Own Funds Requirement) - {P3_2025_URL}\n"
    f"FY2024: Pillar 3 Disclosures 31 December 2024, p.25 (5.4 Own Funds Requirement) - {P3_2024_URL}\n"
    f"FY2023: DERIVED from the FY2024 Pillar 3 document's own '2023 Capital Requirement' comparative column "
    f"(RWA = capital requirement / 8%, the standard Pillar 1 minimum capital ratio) - {P3_2024_URL}. No "
    f"standalone FY2023 Pillar 3 document was found (consistent with the other Pillar 3 sheets' note). The "
    f"derived total (£32,188k) is £1k above the pre-existing Total RWAs sheet's FY2023 figure (£32,187k) due "
    f"to rounding in this back-calculation - not treated as an error, both are within £1k of each other.\n"
    f"FY2021: Pillar 3 Disclosures as at 31st December 2021, p.16 (5.4 Own Funds Requirement) - {P3_2021_URL}\n"
    f"FY2020: Pillar 3 Disclosures as at 31st December 2020, p.16 (5.4 Own Funds Requirement) - {P3_2020_URL}. "
    f"CORRECTED 2026-09-15: these four figures are now TRANSCRIBED from that table's own RWA column (Credit "
    f"and Counterparty Credit Risk 34,473, Market Risk 187, Operational Risk 4,188, 'Total Pillar 1 "
    f"Requirement' 38,848) instead of being derived from the capital-requirement column at /8%. The earlier "
    f"derived values (34,463 / 188 / 4,188 / 38,839) were each within £10k but were an unnecessary derivation "
    f"where the document states the RWAs directly, and the derived total left a spurious £9k gap against the "
    f"Total RWAs sheet. FY2020 now ties exactly.\n"
    f"FY2019: DERIVED the same way from the Pillar 3 Disclosures as at 31st December 2019, p.13 (Own funds "
    f"Requirement) - {P3_2019_URL}. Derived total £27,876k.\n"
    f"FY2018: DERIVED the same way from the Pillar 3 Disclosures as at 31st December 2018, p.12 (Own funds "
    f"Requirement) - {P3_2018_URL}. Derived total £28,538k.\n"
    "FY2022: no standalone Pillar 3 document was found (see other Pillar 3 sheets' note) - left blank rather "
    "than guessed.\n"
    "FY2022 EXHAUSTIVELY RE-VERIFIED 2026-09-15 - a genuine publication gap, not a sourcing miss, proven four "
    "independent ways. (1) The Bank's own financial-statements index page lists its Pillar 3 documents for "
    "2018, 2019, 2020, 2021, 2024 and 2025 and skips 2022 and 2023 entirely, while listing Financial Statements "
    "for every year 2010-2025 without a break. (2) Both predicted URLs, built on the site's completely regular "
    "'BOCUK_Pillar 3 Disclosures 31 December YYYY.pdf' pattern, return HTTP 404 for 2022 and 2023 while the "
    "2021 and 2024 files on that identical pattern serve real PDFs. (3) A full Wayback CDX sweep of the whole "
    "bankofceylon.co.uk domain returns Pillar 3 filenames for 2013, 2018, 2019, 2020, 2021, 2024 and 2025 and "
    "no 2022 or 2023 capture has ever existed, so the documents were not published and later withdrawn - they "
    "were never published. (4) No surviving document's comparative column reaches FY2022: the FY2024 "
    "document's section 5.4 table carries exactly two columns, 'Capital Requirements 2024' and 'Capital "
    "Requirements 2023' (which is where this sheet's FY2023 figures come from), and the FY2021 document's "
    "comparative is FY2020. The FY2022 Annual Report was also checked directly and is not a usable substitute: "
    "it is a scanned, image-only filing with no text layer, and OCR of all 64 pages at 200 dpi finds only "
    "narrative capital-adequacy and risk-management prose with no risk-weighted-asset table of any kind. "
    "Nothing further to chase for this year.\n"
    "DISCREPANCY RESOLVED 2026-09-15 (was 'DISCREPANCY FLAGGED' here; do not re-flag). The flag was correct: "
    "the Total RWAs sheet's FY2018/FY2019/FY2021 figures (£24,492k / £23,604k / £24,509k) were the Credit and "
    "Counterparty Credit Risk subtotal only, excluding Market and Operational risk - the same "
    "credit-subtotal-as-total defect found at Redwood and Ghana International. It has now been acted on, with "
    "each year settled from the primary documents rather than by arithmetic:\n"
    "  - FY2021 CORRECTED on the Total RWAs sheet, 24,509 -> 29,052. 29,052 is not derived: the FY2021 "
    "document's section 5.4 table has an explicit RWA column and prints 'Total Pillar 1 Requirement 29,052' "
    "in it, directly beneath Credit and Counterparty Credit Risk 24,509, Market Risk 302 and Operational Risk "
    "4,241. This sheet already carried the transcribed column and is unchanged.\n"
    "  - FY2019 CORRECTED on the Total RWAs sheet, 23,604 -> 28,513, transcribed from the FY2020 edition's "
    "section 4.1 capital table ('Risk Weighted Assets 38,848  28,513'), the same following-edition route used "
    "for Ghana International. That is the FY2020 edition's RESTATED FY2019 (it also restates FY2019's Pillar 1 "
    "requirement to 2,281 vs the FY2019 edition's own 2,230), so it deliberately does NOT equal this sheet's "
    "FY2019 own-edition total of £27,876k. Per the project's restatement rule each year keeps its own "
    "edition's components here; the ~£637k difference is a restatement and is not to be reconciled.\n"
    "  - FY2018 NOT CHANGED, though the defect is proven there too: the FY2018 KM1 prints CET1 13,393, Total "
    "RWAs 24,492 and a CET1 ratio of 46.9%, and 13,393/24,492 = 54.7%, not 46.9% (13,393/28,538 = 46.93% "
    "does reproduce it, and the FY2017 column of that same table is internally consistent at 13,263/36,385 = "
    "36.5%). But no BOCUK document anywhere prints a FY2018 total risk exposure amount - the FY2018 and FY2019 "
    "editions have no RWA column and the FY2019 comparative repeats 24,492 - so the only available replacement "
    "(£28,538k = Total Pillar 1 Requirement 2,283 / 8%, shown on this sheet's Total row) would be a "
    "derivation, and a derived figure is not substituted for a disclosed one on the Total RWAs sheet. FY2018 "
    "is therefore the one year where this sheet's Total legitimately exceeds the Total RWAs sheet.\n"
    "From FY2020 on the Bank's own section 4.1 'Risk Weighted Assets' line is already the full Pillar 1 total, "
    "so the pattern does not recur.\n"
    "FY2013 HAS NO RWA ROWS AT ALL, AND THE TWO BLOCKS AT THE FOOT OF THIS SHEET ARE NOT RWA. The recovered "
    "31 December 2013 edition (see the metric sheets' source note for the URL) never discloses a "
    "risk-weighted-asset amount - not by risk type, not by exposure class, not in total. What it publishes is "
    "the Pillar 1 CAPITAL requirement, which its own text defines as '8% of the risk weighted exposure "
    "amounts'. Those figures are transcribed exactly as printed, in £'000 of capital, on their own clearly "
    "labelled rows, and are NOT divided by 8% to manufacture an RWA. Doing so would imply a total of roughly "
    "34,625 that no document states - and this is precisely the bank where a printed 'Total RWAs' has already "
    "been shown to be a credit-risk subtotal three times over, so an invented total is the last thing these "
    "sheets need. The two FY2013 blocks are internally consistent (2,454 + 24 + 292 = 2,770; and the six "
    "exposure-class lines sum to the same 2,454), which is the only check available: the nearest surviving "
    "edition is FY2018, five years later, and carries no FY2013 comparative. Source: Capital & Risk "
    "Management - Pillar 3 Disclosures 31st December 2013, p.8 (Minimum Capital Requirement - Pillar 1) and "
    "p.9 (Capital Resource Requirement at 8%; Gross credit risk exposure) - " + P3_2013_URL + "\n"
    + ENTITY_NOTE
)

rwa_breakdown_rows = [
    ("SECTION", "Risk-weighted exposure amounts by risk type", {}),
    ("DATA", "Credit and counterparty credit risk", {"FY2025": 65343, "FY2024": 56022, "FY2023": 26888, "FY2021": 24509, "FY2020": 34473, "FY2019": 23600, "FY2018": 24488}),
    ("DATA", "Market risk", {"FY2025": 37, "FY2024": 557, "FY2023": 1150, "FY2021": 302, "FY2020": 187, "FY2019": 88, "FY2018": 100}),
    ("DATA", "Operational risk (Basic Indicator Approach)", {"FY2025": 5353, "FY2024": 4765, "FY2023": 4150, "FY2021": 4241, "FY2020": 4188, "FY2019": 4188, "FY2018": 3950}),
    ("TOTAL", "Total risk-weighted exposure amount", {"FY2025": 70733, "FY2024": 61344, "FY2023": 32188, "FY2022": "Not published - no FY2022 Pillar 3; no RWA in the FY2022/FY2023 accounts", "FY2021": 29052, "FY2020": 38848, "FY2019": 27876, "FY2018": 28538}),
    ("SECTION", "FY2013 only - Pillar 1 CAPITAL requirement by risk type (£'000 of CAPITAL, not RWA - deliberately NOT divided by 8%; do not read down the same column as the RWA rows above)", {}),
    ("DATA", "Capital requirement - credit risk (standardised approach)", {"FY2013": 2454}),
    ("DATA", "Capital requirement - market risk (foreign currency position risk requirement)", {"FY2013": 24}),
    ("DATA", "Capital requirement - operational risk (Basic Indicator Approach)", {"FY2013": 292}),
    ("TOTAL", "Total Pillar 1 Requirement as printed", {"FY2013": 2770}),
    ("SECTION", "FY2013 only - credit-risk capital requirement at 8% by exposure class (£'000 of CAPITAL, not RWA)", {}),
    ("DATA", "Central Governments and Central Banks", {"FY2013": 0}),
    ("DATA", "Financial Institutions", {"FY2013": 1620}),
    ("DATA", "Personal loans and advances", {"FY2013": 156}),
    ("DATA", "Secured on real estate", {"FY2013": 231}),
    ("DATA", "Commercial loans and advances", {"FY2013": 227}),
    ("DATA", "Fixed and other assets", {"FY2013": 220}),
    ("TOTAL", "Total credit-risk Pillar 1 capital requirement as printed", {"FY2013": 2454}),
    ("DATA", "Memo: gross credit risk exposure before credit risk mitigation (an exposure measure, not an RWA)", {"FY2013": 63175}),
]

bw.add_rwa_breakdown_sheet(
    title="Bank of Ceylon (UK) Limited — RWA Breakdown",
    subtitle="Bank of Ceylon (UK) Limited (own entity basis), £'000",
    rows=rwa_breakdown_rows,
    sources_text=RWA_BREAKDOWN_SOURCES,
    first_col_width=48,
    source_height=260,
)

metric(
    "Leverage Ratio", "£'000 / %",
    [
        ("Tier 1 capital available (£'000)", {"FY2025": 14217, "FY2024": 13940, "FY2023": 13685, "FY2021": 13424, "FY2020": 13338, "FY2019": 13569, "FY2018": 13393, "FY2013": 13436}),
        ("Total leverage ratio exposure measure (£'000)", {"FY2025": 99213, "FY2024": 75247, "FY2023": 47579, "FY2021": 29072, "FY2020": 37808, "FY2019": 39619, "FY2018": 28733}),
        ("Leverage ratio (%)", {"FY2025": "14.3%", "FY2024": "18.5%", "FY2023": "28.8%", "FY2022": "Not published - no FY2022 Pillar 3; none in the FY2022/FY2023 accounts", "FY2021": "46.2%", "FY2020": "35.3%", "FY2019": "34.2%", "FY2018": "46.6%"}),
    ],
    note="FY2024 uses the FY2024 Pillar 3 document's own originally-published figures; see the source note above "
         "for the slightly different restated FY2024 comparative (£76,247k / 18.3%) published a year later in "
         "the FY2025 document, and for the FY2025 document's separate self-contradictory narrative text. "
         "FY2019 likewise uses the FY2019 document's own originally-published figures (£39,619k / 34.2%); the "
         "FY2020 document's own restated FY2019 comparative (£40,135k / 32.7%, alongside a restated Tier 1 "
         "capital of £13,143k) is materially different, driven by the office-building revaluation restatement "
         "described on the Statement of Changes in Equity sheet - see the p3_sources cross-vintage note.\n"
         "FY2013 carries the Tier 1 capital row only (13,436, the recovered edition's own Core Tier 1 line). The "
         "exposure-measure and ratio rows are blank for a structural reason, not a sourcing one: the leverage ratio "
         "did not exist as a UK regulatory measure or disclosure at 31 December 2013 - it arrived with CRD IV/CRR - "
         "and the recovered edition contains no leverage exposure measure and no leverage ratio in any form.",
)

metric(
    "LCR", "£'000 / %",
    [
        ("Total high-quality liquid assets (HQLA) (£'000)", {"FY2025": 101212, "FY2024": 99206, "FY2023": 108880, "FY2019": 131851, "FY2018": 130130}),
        ("Total net cash outflows (£'000)", {"FY2025": 77081, "FY2024": 66349, "FY2023": 86856, "FY2019": 118123, "FY2018": 116560}),
        ("Liquidity Coverage Ratio (%)", {"FY2025": "131%", "FY2024": "149%", "FY2023": "125%", "FY2022": "Not published - no FY2022 Pillar 3; accounts' liquidity sections are narrative only", "FY2021": "345%", "FY2020": "109%", "FY2019": "112%", "FY2018": "111%"}),
    ],
    note="FY2021 ADDED 2026-09-18 (interior-gap sweep): 345%, from the FY2021 Pillar 3 document's own "
         "infographic-style 'KEY METRICS' panel, printed p.3, where it is captioned 'LIQUIDITY RATIO' - the "
         "SAME panel, in the same document series, with the same caption, that already supplies this row's "
         "FY2020 figure of 109%. This note previously said FY2021 was 'Not disclosed' because 'the Key "
         "Metrics/KM1-style LCR template was not yet used in BOCUK's FY2021 Pillar 3 disclosure'. The KM1-style "
         "template really is absent from that edition - but so is it from the FY2020 edition, whose headline "
         "figure this workbook had already accepted, so the reason given did not distinguish the two years and "
         "the FY2021 panel had simply not been read. Both years are the Bank's headline liquidity ratio, both "
         "are whole-percent, and neither edition breaks out HQLA or net cash outflows anywhere - the two "
         "absolute £'000 rows stay blank for FY2020 AND FY2021 rather than being guessed. "
         "FY2022 remains genuinely blank: no FY2022 Pillar 3 document was ever published (see the sourced "
         "negative in the source note), and the FY2022 and FY2023 statutory accounts state no liquidity ratio "
         "of any kind - re-checked 2026-09-18 by re-rendering the FY2023 accounts' Strategic Report and "
         "risk-management pages at 300 dpi and OCR'ing them, since that document is an image-only scan; its "
         "liquidity sections are entirely narrative (ILAAP, stress testing, HQLA portfolio) with no figure. "
         "FY2013 is blank "
         "on all three rows for a structural reason: the LCR did not exist as a UK requirement or disclosure at "
         "31 December 2013 (it was phased in from October 2015), and the recovered 31 December 2013 edition "
         "contains no liquidity ratio at all - its liquidity section describes the then-applicable BIPRU 12 / "
         "ILAA / Individual Liquidity Guidance regime narratively, with no figure.",
)

metric(
    "NSFR", "£'000 / %",
    [
        ("Total required stable funds (£'000)", {"FY2025": 65823, "FY2024": 64648, "FY2023": 35141}),
        ("Total available stable funds (£'000)", {"FY2025": 121764, "FY2024": 91457, "FY2023": 49594}),
        ("Net Stable Funding Ratio (%)", {"FY2025": "185%", "FY2024": "141%", "FY2023": "141%"})
    ],
    note="FY2023 and FY2024 NSFR ratios are both printed as 141% in the source document despite different "
         "underlying £'000 figures for both years - transcribed as printed, not treated as an error since the "
         "absolute figures genuinely differ. Not disclosed for FY2018/FY2019/FY2020/FY2021/FY2022 - no NSFR "
         "line appears in any of the Key Metrics/Own Funds/Leverage sections of the FY2018, FY2019, FY2020 or "
         "FY2021 Pillar 3 documents, and no FY2022 document was found (see LCR sheet note for the same cause "
         "re FY2021/FY2022). FY2013 is blank on firmer ground still: 31 December 2013 predates even the Basel III "
         "NSFR observation period in the UK, the UK NSFR requirement did not take effect until 1 January 2022, and "
         "the recovered 31 December 2013 edition contains no NSFR.",
)

bw.add_not_disclosed_metric_sheets(
    ["MREL Ratio"],
    p3_sources(),
    per_note={"MREL Ratio": "Not disclosed in any of the 7 available Pillar 3 editions (FY2018, FY2019, FY2020, FY2021, FY2023 via comparative, FY2024, FY2025), any year - no numeric ratio or explicit exemption statement found. GA-020 RE-CHECK 2026-09-19: full-text search of the 2013, 2018, 2019, 2020, 2021, 2024 and 2025 Pillar 3 PDFs returns zero 'MREL', 'loss-absorbing' or 'eligible liabilities' (against 64-97 hits for 'capital' in each); the image-only FY2022 accounts (no Pillar 3 that year) were OCR'd and also return zero."},
    statements={"MREL Ratio": ("Not published – zero 'MREL'/'loss-absorbing' in every Pillar 3 edition (2013, "
                               "2018-21, 2024-25; 2024 ed. carries FY2023 comparatives) and in the FY2022 accounts "
                               "(OCR), searched 2026-09-19")},
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {"FY2025": 195113, "FY2024": 172860, "FY2023": 156353, "FY2022": 117599, "FY2021": 48630, "FY2020": 143850, "FY2019": 170285, "FY2018": 158315}),
        ("Loans and advances to customers", {"FY2025": 76043, "FY2024": 56807, "FY2023": 34032, "FY2022": 18096, "FY2021": 19359, "FY2020": 20364, "FY2019": 17577, "FY2018": 12708}),
        ("Customer account deposits", {"FY2025": 76703, "FY2024": 44538, "FY2023": 19229, "FY2022": 11427, "FY2021": 5811, "FY2020": 4732, "FY2019": 6545, "FY2018": 5367}),
        ("Total equity", {"FY2025": 15493, "FY2024": 15170, "FY2023": 14811, "FY2022": 13831, "FY2021": 13902, "FY2020": 13949, "FY2019": 13476, "FY2018": 13380}),
    ],
    balance_sheet_unit="£'000",
    income_statement_totals=[
        ("Net operating income", {"FY2025": 3161, "FY2024": 3041, "FY2023": 3145, "FY2022": 2378, "FY2021": 2100, "FY2020": 2159, "FY2019": 2327, "FY2018": 2301}),
        ("Total operating expenses", {"FY2025": -2793, "FY2024": -2629, "FY2023": -2077, "FY2022": -2525, "FY2021": -1986, "FY2020": -2185, "FY2019": -2219, "FY2018": -2216}),
        ("Profit/(loss) for the year", {"FY2025": 323, "FY2024": 327, "FY2023": 889, "FY2022": -146, "FY2021": 112, "FY2020": -23, "FY2019": 105, "FY2018": 85}),
    ],
    income_statement_unit="£'000",
    equity_changes_totals=[
        ("Opening equity", {"FY2025": 15170, "FY2024": 14811, "FY2023": 13831, "FY2022": 13902, "FY2021": 13949, "FY2020": 13982, "FY2019": 13380, "FY2018": 13339}),
        ("Total comprehensive income", {"FY2025": 323, "FY2024": 359, "FY2023": 1173, "FY2022": -146, "FY2021": 112, "FY2020": -23, "FY2019": 105, "FY2018": 85}),
        ("Other movements, net", {"FY2025": 0, "FY2024": 0, "FY2023": -193, "FY2022": 75, "FY2021": -159, "FY2020": -10, "FY2019": -9, "FY2018": -44}),
        ("Closing equity", {"FY2025": 15493, "FY2024": 15170, "FY2023": 14811, "FY2022": 13831, "FY2021": 13902, "FY2020": 13949, "FY2019": 13476, "FY2018": 13380}),
    ],
    equity_changes_unit="£'000",
    cash_flow_totals=[
        ("Net cash flow from operating activities", {"FY2025": 8361, "FY2024": -14423, "FY2023": 29059, "FY2022": 83148, "FY2021": 927, "FY2020": 1318, "FY2019": -60, "FY2018": -129}),
        ("Net cash flow from investing activities", {"FY2025": -152, "FY2024": -461, "FY2023": -116, "FY2022": -2, "FY2021": 0, "FY2020": -149, "FY2019": -162, "FY2018": -21}),
        ("Net cash flow from financing activities", {"FY2025": 0, "FY2024": 0, "FY2023": 0, "FY2022": 747, "FY2021": 0, "FY2020": 0, "FY2019": 0, "FY2018": 0}),
        ("Closing cash and cash equivalents", {"FY2025": 109027, "FY2024": 100818, "FY2023": 115702, "FY2022": 86759, "FY2021": 2866, "FY2020": 1939, "FY2019": 770, "FY2018": 992}),
    ],
    cash_flow_unit="£'000",
    ratios=[
        ("CET1 Ratio", {"FY2025": "20.1%", "FY2024": "22.7%", "FY2023": "42.5%", "FY2021": "54.8%", "FY2020": "34.3%", "FY2019": "57.5%", "FY2018": "46.9%"}),
        ("Total Capital Ratio", {"FY2025": "21.7%", "FY2024": "24.6%", "FY2023": "45.9%", "FY2021": "57.8%", "FY2020": "36.7%", "FY2019": "57.5%", "FY2018": "46.9%"}),
        ("Leverage Ratio", {"FY2025": "14.3%", "FY2024": "18.5%", "FY2023": "28.8%", "FY2021": "46.2%", "FY2020": "35.3%", "FY2019": "34.2%", "FY2018": "46.6%"}),
        ("LCR", {"FY2025": "131%", "FY2024": "149%", "FY2023": "125%", "FY2021": "345%", "FY2020": "109%", "FY2019": "112%", "FY2018": "111%"}),
        ("NSFR", {"FY2025": "185%", "FY2024": "141%", "FY2023": "141%"}),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own "
         "source citation for the underlying document/page. FY2021/FY2022/FY2020/FY2019/FY2018 NSFR are "
         "genuinely absent from the source documents, not omitted in error. "
         "FY2022 RATIOS - UPDATED 2026-09-15: FY2022 CET1 and Total capital ratios (44% and 48%) ARE stated, in "
         "the FY2023 accounts' Strategic Report p.8, and are now carried on the CET1 Ratio and Total Capital "
         "Ratio detail sheets. They are deliberately NOT copied into this trend view, because they belong to a "
         "different and unstated capital basis from the Pillar 3 series plotted here (that same sentence's "
         "FY2022 CET1 of GBP 12,852,280 is GBP 1.1m below the FY2022 accounts' own Note 28 figure, unreconciled "
         "- see the CET1 Capital sheet's conflict note) and are printed to whole percents rather than the one "
         "decimal used by every other year. Dropping them into the same trend line would present a basis break "
         "as a movement. The FY2022 Leverage Ratio and Total RWAs remain genuinely undisclosed. "
         "FY2020's opening equity (13,982) reflects a prior-year restatement (office building revaluation) "
         "disclosed in the FY2020 filing itself, not FY2019's own originally-published closing equity (13,476) "
         "- see the Statement of Changes in Equity sheet for the full bridge.",
)

bw.save("/Users/armaan/code/katalysis/banks/BANK OF CEYLON UK FINANCIALS.xlsx")
