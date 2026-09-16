import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021", "FY2020", "FY2019", "FY2018", "FY2017", "FY2016", "FY2015", "FY2014", "FY2013"]
Y_CORE = YEARS[:YEARS.index('FY2014') + 1]  # HD-072/075/079: FY2014-floor default for Pillar 3/Asset Quality/RWA Breakdown/Overview
  # most recent first

AR25_URL = "https://v.icbc.com.cn/userfiles/Resources/ICBC/haiwai/ICBCLondon/download/2025/ICBCReport2025.pdf"
AR24_URL = "https://v.icbc.com.cn/userfiles/Resources/ICBC/haiwai/ICBCLondon/download/2024/ICBCReport2024.pdf"
AR23_URL = "https://find-and-update.company-information.service.gov.uk/company/04552753/filing-history/MzQyNDQ0NTU5OWFkaXF6a2N4/document?format=pdf&download=0"
AR22_URL = "https://find-and-update.company-information.service.gov.uk/company/04552753/filing-history/MzM4MTkxOTA4OGFkaXF6a2N4/document?format=pdf&download=0"
AR21_URL = "https://find-and-update.company-information.service.gov.uk/company/04552753/filing-history/MzM0MDgwMDM4MGFkaXF6a2N4/document?format=pdf&download=0"
AR20_URL = "https://find-and-update.company-information.service.gov.uk/company/04552753/filing-history/MzMwMzE1ODk3MWFkaXF6a2N4/document?format=pdf&download=0"
AR19_URL = "https://find-and-update.company-information.service.gov.uk/company/04552753/filing-history/MzI2NjQ0ODkzMGFkaXF6a2N4/document?format=pdf&download=0"
AR18_URL = "https://find-and-update.company-information.service.gov.uk/company/04552753/filing-history/MzIzNTEzMjQ3NGFkaXF6a2N4/document?format=pdf&download=0"
AR17_URL = "https://find-and-update.company-information.service.gov.uk/company/04552753/filing-history/MzIwNjY1MzA2MGFkaXF6a2N4/document?format=pdf&download=0"
AR16_URL = "https://find-and-update.company-information.service.gov.uk/company/04552753/filing-history/MzE3NzMxODYyNWFkaXF6a2N4/document?format=pdf&download=0"
AR15_URL = "https://find-and-update.company-information.service.gov.uk/company/04552753/filing-history/MzE0ODY5NjMzOGFkaXF6a2N4/document?format=pdf&download=0"
AR14_URL = "https://find-and-update.company-information.service.gov.uk/company/04552753/filing-history/MzEyNTk1Nzg1NGFkaXF6a2N4/document?format=pdf&download=0"

P3_25_URL = "https://v.icbc.com.cn/userfiles/Resources/ICBC/haiwai/ICBCLondon/download/2025/2025_pillar_3_disclosure.pdf"
P3_24_URL = "https://v.icbc.com.cn/userfiles/Resources/ICBC/haiwai/ICBCLondon/download/2024/2024_pillar_3_disclosure.pdf"
# FY2023/FY2022/FY2021 Pillar 3 documents: all live on the Bank's own CDN, but the FY2023, FY2022
# and FY2021 files are each MISFILED one year forward (2023 doc under .../2024/, 2022 doc under
# .../2023/, 2021 doc under .../2022/), and the two older ones use a no-underscore filename style.
# Located via a Wayback CDX listing of the CDN path in the 2026-09-12 disclosure audit.
P3_23_URL = "https://v.icbc.com.cn/userfiles/Resources/ICBC/haiwai/ICBCLondon/download/2024/2023_pillar_3_disclosure.pdf"
P3_22_URL = "https://v.icbc.com.cn/userfiles/Resources/ICBC/haiwai/ICBCLondon/download/2023/2022Pillar3Disclosure.pdf"
P3_21_URL = "https://v.icbc.com.cn/userfiles/Resources/ICBC/haiwai/ICBCLondon/download/2022/2021Pillar3Disclosure.pdf"
# FY2020/FY2019/FY2018 Pillar 3 documents, LOCATED 2026-09-16 (KM1-016). These three were
# previously believed not to exist at all - the script asserted in two places that no Pillar 3
# document existed before FY2021. They do exist, on the Bank's own CDN, under the SAME
# misfiled-one-year-forward pattern already documented for FY2021/FY2022 and with the same
# no-underscore filename style, which is why folder-matched searches missed them. Each was
# verified HTTP 200 + Content-Type application/pdf + %PDF magic bytes on 2026-09-16.
# Nothing earlier than FY2018 was located under any filename tried; that is "not located",
# not "does not exist" (map rule 9).
P3_20_URL = "https://v.icbc.com.cn/userfiles/Resources/ICBC/haiwai/ICBCLondon/download/2021/2020Pillar3Disclosure.pdf"
P3_19_URL = "https://v.icbc.com.cn/userfiles/Resources/ICBC/haiwai/ICBCLondon/download/2020/2019Pillar3Disclosure.pdf"
P3_18_URL = "https://v.icbc.com.cn/userfiles/Resources/ICBC/haiwai/ICBCLondon/download/2019/2018Pillar3Disclosure.pdf"

CASH_FLOW_SOURCES = (
    "Sources — all figures are ICBC (London) plc Statement of Cash Flows, $'000:\n"
    f"FY2025 & FY2024: ICBC (London) plc Annual Report and Financial Statements 2025, p.27 (Statement of Cash Flows) — {AR25_URL}\n"
    f"FY2024 comparative cross-checked against ICBC (London) plc Annual Report 2024, p.29 (Statement of Cash flows) — {AR24_URL}\n"
    f"FY2023: ICBC (London) plc Annual Report and Financial Statements 2023 (Companies House filing, full accounts), p.30 (Statement of Cash flows) — {AR23_URL}\n"
    f"FY2022: ICBC (London) plc Annual Report and Financial Statements 2022 (Companies House filing, full accounts), p.28 (Statement of Cash flows) — {AR22_URL}\n"
    f"FY2021: ICBC (London) plc Annual Report and Financial Statements 2021 (Companies House filing, full accounts), p.30 (Statement of Cash flows) — {AR21_URL}\n"
    f"FY2020: ICBC (London) plc Annual Report and Financial Statements 2020 (Companies House filing, scanned/OCR'd), "
    f"p.26 (Statement of Cash flows, own 2020 column) — {AR20_URL}\n"
    f"FY2019: ICBC (London) plc Annual Report and Financial Statements 2019 (Companies House filing, scanned/OCR'd), "
    f"p.26 (Statement of Cash Flows, own 2019 column) — {AR19_URL}. Cross-checked against the FY2020 filing's "
    f"restated 2019 comparative — {AR20_URL} — which differs by exactly $58k on 'Interest income'/'Interest received' "
    f"only (see note below); the FY2019 filing's own originally-published figures are used.\n"
    f"FY2018: ICBC (London) plc Annual Report and Financial Statements 2019 (Companies House filing, scanned/OCR'd), "
    f"p.26 (2018 comparative column) — {AR19_URL}. The FY2018 filing's own document ({AR18_URL}) has a shaded/"
    f"textured background specifically behind its own 2018 column that badly degrades OCR there; the FY2019 "
    f"filing's clean comparative column is used instead and cross-checked by internal arithmetic.\n"
    f"FY2017: ICBC (London) plc Annual Report and Financial Statements 2017 (Companies House filing, scanned/OCR'd), "
    f"p.21-22 (Statement of Cash flows, own 2017 column) — {AR17_URL}\n"
    f"FY2016: ICBC (London) plc Annual Report and Financial Statements 2016 (Companies House filing, scanned/OCR'd), "
    f"p.16 (Statement of Cash flows, own 2016 column) — {AR16_URL}\n"
    f"FY2015: ICBC (London) plc Annual Report and Financial Statements 2015 (Companies House filing, scanned/OCR'd), "
    f"p.16 (Statement of Cash flows, own 2015 column) — {AR15_URL}\n"
    f"FY2014: no cash flow statement exists in ICBC (London) plc's own FY2014 Annual Report ({AR14_URL}) — its own "
    f"accounting policies note states the Bank 'has taken advantage of the exemption from the requirement to "
    f"prepare a cash flow statement on the grounds that it is a wholly-owned subsidiary' of ICBC Ltd. FY2014 figures "
    f"are therefore sourced entirely from the FY2015 Annual Report's 2014 comparative column, p.16 — {AR15_URL} — "
    f"the earliest year for which a cash flow statement covering FY2014 exists at all.\n"
    "Note: the FY2014-2023 Companies House filings are scanned (image-only) documents; those years' figures were "
    "transcribed from page renders or OCR text, cross-checked by internal arithmetic and year-boundary reconciliation "
    "(each year's own closing cash and cash equivalents equals the following year's opening balance - confirmed at "
    "every boundary FY2014 through FY2025). 'Gain on sale of financial investments at FVOCI' was not a separate line "
    "in several years' statements (folded into the exchange gain/amortisation line); blank cells indicate that year's "
    "statement did not disclose that specific line. The source document's own labels ('Net decrease in cash and cash "
    "equivalents', 'Net cash used in operating activities') are reproduced verbatim even in years where the reported "
    "figure is positive. Presentation change: FY2014-2019's own filings present 'Acquisition/Maturity of financial "
    "investments at FVOCI/amortised cost' under investing activities; from FY2020 onward the same items are folded "
    "into operating activities instead (confirmed by a direct mismatch between FY2019's own reported operating cash "
    "flow of $353,344k and FY2020's restated FY2019 comparative of $391,500k, with investing activities showing "
    "$37,751k vs. $(405)k for the same reason) - each year's own originally-published classification is used, not "
    "force-reconciled to a later year's restated presentation. Separately, FY2020's own filing carries a footnote: "
    "'Interest income from financial derivatives of $58k, which was disclosed under interest income in 2019, has "
    "been reclassified under the dealing profit in 2020' - a $58k difference between FY2019's originally-published "
    "and FY2020's restated comparative 'Interest income'/'Interest received' figures, consistent with the same "
    "reclassification documented on the Profit & Loss sheet. The $100,000k Subordinated loan (see the Balance "
    "Sheet's own note) was fully repaid in April 2019, shown here as a single '$(100,000)k' financing-shaped "
    "outflow within FY2019's operating-liabilities changes, matching the Bank's own presentation of the repayment "
    "within operating activities (not financing activities, which is nil in every year of this workbook)."
)

def p3_sources(note_disclosure_start=True):
    text = (
        "Sources — ICBC (London) plc (solo basis), Annex 2 — UK KM1 - Key metric template:\n"
        f"FY2025: ICBC (London) plc Pillar 3 Disclosures 2025, p.13-14 (31/12/2025 column) — {P3_25_URL}\n"
        f"FY2024: ICBC (London) plc Pillar 3 Disclosures 2024, p.12-13 (31/12/2024 column) — {P3_24_URL}\n"
        f"FY2023: ICBC (London) plc Pillar 3 Disclosures 2023, p.12-13 (31/12/2023 column, the year's own "
        f"authoritative document) — {P3_23_URL}\n"
        f"FY2022: ICBC (London) plc Pillar 3 Disclosures 2022, p.12-13 (31/12/2022 column) — {P3_22_URL}\n"
        f"FY2021: ICBC (London) plc Pillar 3 Disclosures 2021, p.13-14 (31/12/2021 column) — {P3_21_URL}\n"
        "FY2021/FY2022 LOCATED 2026-09-12 (independent disclosure audit) — these two years were previously "
        "recorded as 'not publicly disclosed'. Both documents are live on the Bank's own CDN but each is MISFILED "
        "ONE YEAR FORWARD (the 2021 disclosure sits in the .../download/2022/ folder, the 2022 disclosure in "
        ".../download/2023/), and both use a different filename convention ('2021Pillar3Disclosure.pdf') from the "
        "later underscore style ('2024_pillar_3_disclosure.pdf'), which is why earlier folder-matched searches "
        "missed them. Found via a Wayback Machine CDX listing of the CDN path, then confirmed live. Cross-verified: "
        "the FY2022 document's own T-4 (31/12/2021) comparative column reproduces every FY2021 figure used here "
        "exactly (CET1 451,197.05; RWA 739,776.26; leverage 30.75%; LCR 492.91%; NSFR 150.16%).\n"
        "FY2022 ratio basis: 50.54% is the FY2022 document's OWN 31/12/2022 figure. The FY2023 document's "
        "31/12/2022 comparative column instead shows 50.67% (a small later restatement); this workbook follows the "
        "project convention of using each year's own primary presentation rather than a later restated comparative.\n"
        "FY2023 NSFR CORRECTED 2026-09-12: this sheet previously carried FY2023 NSFR as 135.79% (ASF 694,607 / RSF "
        "511,527), taken from the FY2024 document's 31/12/2023 comparative column. That comparative is demonstrably "
        "wrong in the source itself - it reproduces the FY2022 NSFR row to the cent (the FY2022 document's own "
        "31/12/2022 column reads ASF 694,606.62 / RSF 511,526.78 / 135.79%), i.e. the FY2024 document carried the "
        "prior year's row forward. The FY2023 document's own 31/12/2023 column gives ASF 798,010.24 / RSF "
        "477,595.45 / 167.09%, which is what is now shown. Only the NSFR row is affected: FY2023 capital, RWA, "
        "ratio, leverage and LCR figures all agree exactly between the FY2023 and FY2024 documents."
    )
    if note_disclosure_start:
        text += (
            "\nNote: the UK KM1 key-metrics template is used by ICBC (London) plc from the FY2021 edition "
            "onward. It is NOT used in the FY2018, FY2019 or FY2020 editions, and the reason is in those "
            "documents themselves: each states that the CRR II Pillar 3 requirements (articles 433-455) "
            "'are expected to be applicable from June 2021'. The template post-dates them; they are not an "
            "absence of disclosure.\n"
            "CORRECTION 2026-09-16 (KM1-016): this note previously stated that NO Pillar 3 disclosure "
            "document existed before FY2021. That was wrong. Standalone Pillar 3 Disclosures exist on the "
            "Bank's own CDN for FY2018, FY2019 and FY2020 as well, misfiled one year forward in exactly the "
            "way already documented for FY2021/FY2022:\n"
            f"FY2020: ICBC (London) plc Pillar 3 Disclosures 2020 (31 December 2020) — {P3_20_URL}\n"
            f"FY2019: ICBC (London) plc Pillar 3 Disclosures 2019 (31 December 2019) — {P3_19_URL}\n"
            f"FY2018: ICBC (London) plc Pillar 3 Disclosures 2018 (31 December 2018) — {P3_18_URL}\n"
            "Each verified HTTP 200 + Content-Type application/pdf + %PDF magic bytes. Those three editions "
            "DO disclose total risk-weighted exposures, the three capital ratios and (FY2018-FY2020) the "
            "leverage ratio and its exposure measure, in their own 'Table 1 - Own Funds' and 'The Leverage "
            "Ratio' section - so the Total RWAs, CET1/Tier 1/Total Capital Ratio and Leverage Ratio sheets "
            "now carry FY2018-FY2020 (and FY2017 from the FY2018 edition's own comparative column, the only "
            "source for that year located). Those sheets' FY2014-FY2016 cells remain blank: no Pillar 3 "
            "edition earlier than FY2018 was located under any filename tried, and no RWA figure appears in "
            "the Annual Reports.\n"
            "The NSFR and RWA Breakdown sheets are NOT back-filled from these three editions: no NSFR ratio "
            "of any kind is stated in any of them (the CRR II NSFR disclosure is one of the requirements "
            "they describe as not yet applicable), and their RWA analysis is a 'Table 7 - Pillar 1 capital "
            "requirement' breakdown by EXPOSURE CLASS, which is a different cut from the UK OV1 risk-type "
            "breakdown the RWA Breakdown sheet reproduces; mapping one onto the other would invent a "
            "correspondence the Bank never published.\n"
            "CET1/Tier 1/Total Capital $ amounts are disclosed every year back to FY2014 via each year's "
            "own Annual Report 'Regulatory capital' note (see the CET1/Tier 1/Total Capital sheets' own "
            "FY2014-FY2020 source note), and for FY2017-FY2020 those Annual Report amounts tie EXACTLY to "
            "the Pillar 3 editions' own Table 1 (FY2020 456,128; FY2019 443,521; FY2018 422,168 / Total "
            "Capital 518,606; FY2017 397,848 / Total Capital 500,128).\n"
            "BASIS NOTE, and it matters when reading FY2020 beside FY2021: the pre-KM1 editions and the "
            "KM1 editions are not on the same capital basis where they overlap. The FY2020 edition's own "
            "31 December 2020 column gives CET1 456,128, RWA 1,022,681, all three ratios 44.60%, leverage "
            "exposure 2,058,837 and leverage ratio 22.17%. The FY2021 KM1's 31/12/2020 comparative column "
            "gives CET1 445,536.92, RWA 1,022,680.75 (the same RWA), ratios 43.57% and leverage 2,050,570.53 "
            "/ 21.73%. Each year keeps its OWN edition's figures here; neither set is restated onto the other."
        )
    return text

def p3_capital_sources_1420():
    return (
        "Sources — ICBC (London) plc, Note 'Capital'/'Regulatory capital' in each year's own Annual Report, $'000:\n"
        f"FY2020: Annual Report 2020 (Companies House filing, scanned/OCR'd), Note 32 (own 2020 column) — {AR20_URL}\n"
        f"FY2019: Annual Report 2019 (Companies House filing, scanned/OCR'd), Note ~31 (own 2019 column) — {AR19_URL}\n"
        f"FY2018: Annual Report 2019, Note ~31 (2018 comparative column) — {AR19_URL}. The FY2018 filing's own "
        f"document ({AR18_URL}) has a shaded 2018 column that OCR could not read reliably here either; only its "
        f"2017 comparative column (matching the FY2017 filing's own figures exactly) was legible.\n"
        f"FY2017: Annual Report 2017 (Companies House filing, scanned/OCR'd), Note 35 (own 2017 column) — {AR17_URL}\n"
        f"FY2016: Annual Report 2016 (Companies House filing, scanned/OCR'd), Note 33 (own 2016 column) — {AR16_URL}\n"
        f"FY2015: Annual Report 2015 (Companies House filing, scanned/OCR'd), Note ~32 (own 2015 column) — {AR15_URL}\n"
        f"FY2014: Annual Report 2014 (Companies House filing, scanned/OCR'd), Note 33 (own 2014 column) — {AR14_URL}\n"
        "No risk-weighted-assets figure is disclosed in any of these ANNUAL REPORT notes for any year FY2014-2020 "
        "(confirmed by reading each year's own Annual Report in full, including its Directors'/Strategic Report "
        "capital narrative) - only the $ capital amounts themselves. That is a statement about the Annual Reports "
        "only: the Bank's own standalone Pillar 3 Disclosures for FY2018, FY2019 and FY2020 DO disclose total risk "
        "weighted exposures, and were located on 2026-09-16; the Total RWAs and ratio sheets carry them, and their "
        "Table 1 own-funds figures agree exactly with the Annual Report amounts cited above for FY2017-FY2020. "
        "CET1 Capital = Tier 1 Capital every year shown here "
        "(no Additional Tier 1 instrument has ever existed for this Bank), matching the convention already used for "
        "FY2023-2025 on this workbook. FY2014's own note separately labels a '$200,000k Common Equity Tier 1 "
        "Capital' line ABOVE the Tier 1 Capital build-up ($322,451k = share capital + retained earnings + AFS "
        "reserve) - read in context this is the share-capital component of the build-up, not a distinct, lower CET1 "
        "figure with $122,451k of unexplained Additional Tier 1 capital; no such AT1 instrument is disclosed "
        "anywhere in the FY2014 accounts, so CET1 Capital is shown here as $322,451k (= Tier 1 Capital), consistent "
        "with every other year. 'Tier 1 Capital' before FY2017 is simply total audited equity (share capital + "
        "retained earnings + AFS reserve/other reserves, with no regulatory deduction); from FY2017 a 'Less: "
        "Regulatory adjustments' line first appears, reducing Tier 1 Capital slightly below total equity."
    )

def p3_prekm1_sources():
    """FY2017-FY2020 RWA, capital ratios and leverage - from the three pre-KM1
    standalone Pillar 3 editions located 2026-09-16 (KM1-016). These years were
    previously left blank on the strength of a claim that no Pillar 3 document
    existed before FY2021; it does."""
    return (
        "Sources FY2017-FY2020 - ICBC (London) plc's own standalone Pillar 3 Disclosures for those years, "
        "'Table 1 - Own Funds' (total risk weighted exposures and the three capital ratios) and section 5 "
        "'The Leverage Ratio' (the ratio in the section's own narrative sentence, the exposure measure in "
        "its 'Summary reconciliation of accounting assets and Leverage ratio exposures' table), $'000:\n"
        f"FY2020: Pillar 3 Disclosures 2020, Table 1 p.13 and section 5 p.18 (own 2020 column) — {P3_20_URL}\n"
        f"FY2019: Pillar 3 Disclosures 2019, Table 1 p.12 and section 5 p.17 (own 2019 column) — {P3_19_URL}\n"
        f"FY2018: Pillar 3 Disclosures 2018, Table 1 p.9 and section 5 p.15 (own 2018 column) — {P3_18_URL}\n"
        f"FY2017: Pillar 3 Disclosures 2018, Table 1 p.9 (2017 COMPARATIVE column) — {P3_18_URL}. No FY2017 "
        "or earlier Pillar 3 edition was located under any filename pattern tried, so FY2017 is the one "
        "year here taken from a later edition's comparative rather than its own document; it is flagged "
        "rather than silently mixed in. The FY2018 edition prints no 2017 leverage comparative, so FY2017 "
        "has no leverage figure.\n"
        "These three editions were located on 2026-09-16, misfiled one year forward on the Bank's own CDN "
        "in exactly the way already documented for the FY2021 and FY2022 editions, and each was verified "
        "by HTTP 200, Content-Type application/pdf and %PDF magic bytes. They do NOT use the UK KM1 "
        "template (it post-dates them - see the KM1 Key Metrics sheet's own note), so these figures come "
        "from the Bank's own bespoke tables and are not re-labelled onto template row numbers anywhere.\n"
        "The ratios tie to the CET1/Tier 1/Total Capital amounts already on this workbook for the same "
        "years, which come from each year's Annual Report 'Regulatory capital' note and agree with these "
        "Pillar 3 editions' Table 1 exactly. ICBC's own printed ratios are kept as printed even where "
        "recomputing from the two components would round differently (FY2017 397,848/1,793,374 recomputes "
        "to 22.18% against a printed 22.17%; FY2020 leverage 456,128/2,058,837 recomputes to 22.15% "
        "against a printed 22.17%) - the disclosure is reproduced, not recalculated.\n"
        "BASIS BREAK AT FY2021: these pre-KM1 figures are NOT on the same basis as the KM1 figures for "
        "FY2021 onward, and the overlap proves it. The FY2020 edition's own 31 December 2020 column gives "
        "CET1 456,128 and all three ratios 44.60%; the FY2021 edition's KM1 31/12/2020 comparative gives "
        "CET1 445,536.92 and 43.57% on an identical RWA of 1,022,680.75. Likewise leverage: 2,058,837 / "
        "22.17% in the FY2020 edition against 2,050,570.53 / 21.73% in the FY2021 KM1's comparative. Each "
        "year keeps its own edition's figure; the two series are never merged or restated onto each other."
    )

P3_23_KM1_NOTE = (
    " (KM1 comparative column only - the OV1 category-level RWA breakdown "
    "table is not available for FY2023 or earlier, only the aggregate Total "
    "RWA figure)"
)

STATEMENTS_SOURCES = (
    "Sources — all figures are ICBC (London) plc Balance Sheet / Profit and Loss "
    "Account / Statement of Changes in Equity, $'000, as originally published in "
    "each year's own Annual Report (each year's own primary presentation, not a "
    "later restated comparative, except where noted):\n"
    f"FY2025 & FY2024: ICBC (London) plc Annual Report and Financial Statements 2025, "
    f"pp.23-26 (Profit and Loss Account, Statement of Comprehensive Income, Balance "
    f"Sheet, Statement of Changes in Equity) — {AR25_URL}\n"
    f"FY2023: ICBC (London) plc Annual Report and Financial Statements 2024, pp.25-28 "
    f"(2023 comparative column) — {AR24_URL}. Cross-checked against ICBC (London) plc "
    f"Annual Report and Financial Statements 2023 (Companies House filing), pp.26-29 "
    f"(own originally-published figures) — {AR23_URL}. Both sources agree exactly.\n"
    f"FY2022: ICBC (London) plc Annual Report and Financial Statements 2023 (Companies "
    f"House filing), pp.26-29 (2022 comparative column) — {AR23_URL}\n"
    f"FY2021: ICBC (London) plc Annual Report and Financial Statements 2022 (Companies "
    f"House filing), pp.24-27 (2021 comparative column) — {AR22_URL}\n"
    f"FY2020: ICBC (London) plc Annual Report and Financial Statements 2020 (Companies "
    f"House filing, scanned/OCR'd), pp.21-24 (own 2020 figures) — {AR20_URL}\n"
    f"FY2019: ICBC (London) plc Annual Report and Financial Statements 2019 (Companies "
    f"House filing, scanned/OCR'd), pp.21-24 (own 2019 figures) — {AR19_URL}\n"
    f"FY2018: ICBC (London) plc Annual Report and Financial Statements 2019 (Companies "
    f"House filing), pp.21-24 (2018 comparative column) — {AR19_URL}. The FY2018 filing's "
    f"own document ({AR18_URL}) has a shaded/textured background specifically behind its "
    f"own 2018 column that badly degrades OCR there (its 2017 comparative column is "
    f"unaffected); the FY2019 filing's clean comparative column is used instead, "
    f"cross-checked by internal arithmetic and against the FY2018 filing's own Regulatory "
    f"Capital note (Note 33), which independently ties to the same closing equity figure.\n"
    f"FY2017: ICBC (London) plc Annual Report and Financial Statements 2017 (Companies "
    f"House filing, scanned/OCR'd), pp.16-19 (own 2017 figures) — {AR17_URL}\n"
    f"FY2016: ICBC (London) plc Annual Report and Financial Statements 2016 (Companies "
    f"House filing, scanned/OCR'd), pp.12-15 (own 2016 figures) — {AR16_URL}\n"
    f"FY2015: ICBC (London) plc Annual Report and Financial Statements 2015 (Companies "
    f"House filing, scanned/OCR'd), pp.12-15 (own 2015 figures) — {AR15_URL}\n"
    f"FY2014: ICBC (London) plc Annual Report and Financial Statements 2014 (Companies "
    f"House filing, scanned/OCR'd), pp.10-13 (own 2014 figures: Profit and Loss Account, "
    f"Statement of Total Recognised Gains and Losses, Balance Sheet) — {AR14_URL}\n"
    "Note: the FY2014-2023 Companies House filings are scanned (image-only) documents; "
    "those years' figures were transcribed from page renders or OCR text. The Statement "
    "of Changes in Equity reconciles exactly at every year boundary from FY2014 through "
    "FY2025 (each year's own closing Total shareholder's funds equals the next year's own "
    "opening balance and that year's own Balance Sheet Total Share Capital and Reserves) - "
    "no plug rows were needed anywhere. 'Reimbursement of expenses attributable to the "
    "Branch' offsets operating expenses recharged to the Bank's own overseas Branch "
    "operation - a genuine feature of this entity's cost structure, not a data error; it "
    "is only broken out as a separate P&L line from FY2017 onward (FY2014-2016 present a "
    "single net 'Other operating expenses' figure with no separate reimbursement line - "
    "see the FY2017 filing's own Note 28, which documents this and one other item as "
    "presentational reclassifications of FY2016's comparative figures, with zero net "
    "profit impact). Terminology/classification change: 'Available-for-sale (AFS) "
    "financial investments' (FY2014-2017, IAS 39) becomes 'Financial investments at "
    "FVOCI' (FY2018 onward, IFRS 9) on the Balance Sheet, P&L and Equity sheets - a "
    "genuine disclosed transition (day-1 IFRS 9 adjustment at 1 January 2018: retained "
    "earnings -$189k, other reserves +$25k, net -$164k - shown as its own row on the "
    "Equity sheet), not a data error. 'Held-to-maturity financial investments' (a "
    "distinct Balance Sheet line, disclosed only for FY2017, $69,522k) was folded into "
    "'Financial investments at amortised cost' once IFRS 9 introduced that classification "
    "from FY2018; no equivalent held-to-maturity holding existed in FY2014-2016. A "
    "'Subordinated loan' of $100,000k (classified as Tier 2 capital) existed on the "
    "Balance Sheet from FY2014 through FY2018 and was fully repaid by the Bank in April "
    "2019 - blank cells for FY2019 onward reflect its genuine absence, not a missing "
    "figure. FY2014's own filing uses an older UK GAAP-style format ('Profit and loss "
    "account' and 'Statement of Total Recognised Gains and Losses' rather than 'Profit "
    "and Loss Account'/'Statement of Comprehensive Income') that nets certain fee income "
    "and expense items differently to every later year; the FY2014 column on this "
    "workbook's Income sheet regroups those figures into the same category structure "
    "used from FY2015 onward (moving a $2,482k 'Other operating expenditure' line out of "
    "the netted non-interest-income section into Operating expenses) - this is a "
    "value-preserving regroup only: Profit before tax ($30,526k) and Profit for the year "
    "($23,916k) are exactly as originally reported and unaffected by the regroup."
)

ASSET_QUALITY_SOURCES = (
    "Sources — ICBC (London) plc, Loans and advances to customers, $'000:\n"
    f"FY2025: Annual Report 2025, Note 11(i) — {AR25_URL}\n"
    f"FY2024: Annual Report 2025, Note 11(i) (2024 comparative) — {AR25_URL}. Cross-"
    f"checked against Annual Report 2024, Note 11(i) — {AR24_URL}\n"
    f"FY2023: Annual Report 2024, Note 11(i) (2023 comparative) — {AR24_URL}\n"
    f"FY2022: Annual Report 2023 (Companies House filing), Note 11(i) — {AR23_URL}\n"
    f"FY2021: Annual Report 2022 (Companies House filing), Note 11(i) — {AR22_URL}\n"
    f"FY2020: Annual Report 2020 (Companies House filing, scanned/OCR'd), Note 11(i) "
    f"(own 2020 closing balance) — {AR20_URL}\n"
    f"FY2019: Annual Report 2019 (Companies House filing, scanned/OCR'd), Note 10(i) "
    f"(own 2019 closing balance) — {AR19_URL}. Cross-checked against Annual Report 2020, "
    f"Note 11(i) (2019 comparative) — {AR20_URL}\n"
    f"FY2018: Annual Report 2019 (Companies House filing), Note 10(i) (2018 comparative "
    f"column, showing the 1 January 2018 IFRS 9 day-1 transition) — {AR19_URL}\n"
    f"FY2017: Annual Report 2017 (Companies House filing, scanned/OCR'd), Note 10 "
    f"(own 2017 closing balance, IAS 39 specific/collective basis) — {AR17_URL}\n"
    f"FY2016: Annual Report 2016 (Companies House filing, scanned/OCR'd), Note 10 "
    f"(own 2016 closing balance) — {AR16_URL}\n"
    f"FY2015: Annual Report 2015 (Companies House filing, scanned/OCR'd), Note 10 "
    f"(own 2015 closing balance) — {AR15_URL}\n"
    f"FY2014: Annual Report 2015, Note 10 (2014 comparative column, the earliest year "
    f"with a full specific/collective impairment allowance breakdown) — {AR15_URL}\n"
    "Gross carrying amount and net carrying amount for Loans and advances to customers "
    "sourced from each year's own Note 9/10 (or comparative column); confirmed by reading "
    "the relevant note in full for every year that the Bank's entire loans-and-advances-"
    "to-customers book sits in IFRS 9 Stage 1 throughout FY2021-FY2025 - no Stage 2 or "
    "Stage 3 balance has existed at any year-end in this range (a genuine feature of "
    "this book, not an omission - Stage 2 exposure of $4,594k did exist at the opening "
    "of FY2021 per the Bank's own comparative disclosure, but had cleared to nil by "
    "31 December 2021, before this workbook's coverage begins). Loans and advances to "
    "banks (inter-bank placements) are kept separate from the customer loan book above "
    "and are not included in this sheet's coverage or ratios, consistent with how "
    "other banks in this project separate Inter-Group/interbank placements from "
    "customer-facing credit risk. Methodology change: FY2014-2017 use an IAS 39 "
    "incurred-loss basis (impairment allowance split between 'specific' and 'collective' "
    "provisions, no forward-looking staging); IFRS 9's expected-credit-loss Stage 1/2/3 "
    "model was adopted 1 January 2018, with the transition shown as its own row on this "
    "sheet using the Bank's own day-1 restatement (FY2017 closing allowance across banks "
    "and customers combined of $7,280k restated to $7,096k, a $184k net day-1 credit "
    "release per the Bank's own Note 10 - customer-only allowance moves from $7,035k "
    "[$2,035k collective + $5,000k specific] to a Stage 1/2/3 split of $608k/$1,252k/"
    "$5,000k = $6,860k, before the year's own FY2018 charge is applied) - the two bases "
    "are presented as separate sections rather than forced into a single column, "
    "consistent with how other banks on this project handle the same transition. "
    "'Stage 2/3 exposure as % of gross carrying amount' is left blank for FY2018-2020: "
    "each year's own Note 10/11 discloses the impairment ALLOWANCE by stage (used above) "
    "but not the gross loan balance by stage, so this specific ratio cannot be computed "
    "for those years without guessing an exposure split - blank is used rather than a "
    "derived approximation."
)

def rwa_sources():
    return (
        "Sources — ICBC (London) plc (solo basis), Annex 1 / UK OV1 template (Overview "
        "of risk weighted exposure amounts), $'000:\n"
        f"FY2025: ICBC (London) plc Pillar 3 Disclosures 2025, p.14-15 (31/12/2025 "
        f"column) — {P3_25_URL}\n"
        f"FY2024: ICBC (London) plc Pillar 3 Disclosures 2024, p.15-16 (31/12/2024 "
        f"column) — {P3_24_URL}\n"
        f"FY2023: ICBC (London) plc Pillar 3 Disclosures 2023, p.15, 'UK OV1 - Overview "
        f"of risk weighted exposure amounts' (31/12/2023 column) — "
        f"https://v.icbc.com.cn/userfiles/Resources/ICBC/haiwai/ICBCLondon/download/2024/2023_pillar_3_disclosure.pdf\n\n"
        "CORRECTION (2026-09-12 independent re-verification): this sheet previously stated "
        "'No FY2023 ... OV1 table exists' - that was wrong. The document is live on the "
        "Bank's own site (filed under its 2024 download folder, not 2023) and its own OV1 "
        "table gives Credit risk (excl. CCR) $795,488.58k, Counterparty credit risk (CCR) "
        "nil, Operational risk $47,249.90k, summing exactly to the document's own printed "
        "Total of $842,738.48k - which ties to the Total RWAs sheet's FY2023 figure "
        "($842,738k, KM1-sourced) to the nearest thousand.\n"
        f"FY2022: ICBC (London) plc Pillar 3 Disclosures 2022, p.15-16, 'UK OV1 - Overview "
        f"of risk weighted exposure amounts' (column a, 31/12/2022) — {P3_22_URL}\n"
        f"FY2021: ICBC (London) plc Pillar 3 Disclosures 2021, p.14, 'UK OV1 - Overview of "
        f"risk weighted exposure amounts' (column a, 31/12/2021) — {P3_21_URL}\n\n"
        "SECOND CORRECTION (2026-09-15): this sheet previously stated 'No FY2022 or FY2021 "
        "OV1 table has been located' - that was also wrong, and for the same reason as the "
        "FY2023 error above. Both documents carry a full UK OV1 table, and both were "
        "already cited elsewhere in this very script for other metrics - they had simply "
        "never been read for their OV1. Note the same year-forward misfiling: the FY2021 "
        "document sits in the Bank's /2022/ download folder and the FY2022 document in its "
        "/2023/ folder. Both tables have a real text layer; no OCR was needed.\n"
        "Both tie exactly to the Total RWAs sheet's existing KM1-sourced figures. FY2022: "
        "Credit risk (excl. CCR) $848,322.89k + CCR nil (printed '-') + Operational risk "
        "$54,534.06k = the document's own printed Total of $902,856.95k, against the Total "
        "RWAs sheet's $902,857k. FY2021: Credit risk (excl. CCR) $671,772.29k + CCR "
        "$20.86k + Operational risk $67,983.12k = the document's own printed Total of "
        "$739,776.26k, against the Total RWAs sheet's $739,776k. Both documents report all "
        "credit and counterparty risk under the standardised approach and operational risk "
        "under the basic indicator approach, matching FY2023-FY2025. FY2025's OV1 Total "
        "($675,423.74k) and FY2024's OV1 Total ($719,040.48k, matching the Total RWAs "
        "sheet's disclosed figure exactly) both come from the Bank's own Pillar 3 "
        "documents; FY2025's OV1 Total differs slightly ($675,423.74k vs. $675,668k) from "
        "the Total RWAs sheet's KM1-sourced figure for the same date - both are the Bank's "
        "own official disclosures, reproduced as reported rather than force-reconciled."
    )

bw = BankWorkbook(bank_name="ICBC (London) plc", years=Y_CORE, year_label={y: y for y in YEARS}, header_color="2E5395")

# ---------------------------------------------------------------
# Balance Sheet
# ---------------------------------------------------------------
balance_sheet_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and balances at central banks", {"FY2025": 1062471, "FY2024": 43857, "FY2023": 196360, "FY2022": 107136, "FY2021": 149090, "FY2020": 200967, "FY2019": 376810, "FY2018": 10369, "FY2017": 162, "FY2016": 145, "FY2015": 197, "FY2014": 243, "FY2013": 108}),
    ("DATA", "Loans and advances to banks", {"FY2025": 511222, "FY2024": 934969, "FY2023": 523491, "FY2022": 612456, "FY2021": 537966, "FY2020": 689413, "FY2019": 741330, "FY2018": 900153, "FY2017": 840064, "FY2016": 1171593, "FY2015": 1289728, "FY2014": 967756, "FY2013": 956543}),
    ("DATA", "Loans and advances to customers", {"FY2025": 413326, "FY2024": 336256, "FY2023": 429281, "FY2022": 331484, "FY2021": 128348, "FY2020": 428558, "FY2019": 513279, "FY2018": 809084, "FY2017": 953232, "FY2016": 1024525, "FY2015": 1347144, "FY2014": 2151215, "FY2013": 1845322}),
    ("DATA", "Derivative financial instruments", {"FY2025": 0, "FY2024": 255, "FY2023": 66, "FY2022": 0, "FY2021": 21, "FY2020": 26115, "FY2019": 17623, "FY2018": 12667, "FY2017": 52120, "FY2016": 86329, "FY2015": 33699, "FY2014": 40673, "FY2013": 1455}),
    ("DATA", "Financial investments at FVOCI", {"FY2025": 320996, "FY2024": 313176, "FY2023": 251961, "FY2022": 263048, "FY2021": 350258, "FY2020": 402959, "FY2019": 391350, "FY2018": 393988, "FY2017": 448210, "FY2016": 388541, "FY2015": 489848, "FY2014": 610135, "FY2013": 597407}),
    ("DATA", "Financial investments at amortised cost", {"FY2025": 35803, "FY2024": 27177, "FY2023": 68805, "FY2022": 175266, "FY2021": 209357, "FY2020": 194293, "FY2019": 160762, "FY2018": 191156, "FY2017": 69522}),
    ("DATA", "Intangible assets", {"FY2025": 244, "FY2024": 220, "FY2023": 186, "FY2022": 162, "FY2021": 167, "FY2020": 155, "FY2019": 159, "FY2018": 144, "FY2017": 178, "FY2016": 28}),
    ("DATA", "Tangible fixed assets", {"FY2025": 29460, "FY2024": 29928, "FY2023": 30669, "FY2022": 31651, "FY2021": 32585, "FY2020": 33744, "FY2019": 35321, "FY2018": 36761, "FY2017": 37994, "FY2016": 39488, "FY2015": 41314, "FY2014": 42850, "FY2013": 44732}),
    ("DATA", "Current tax assets", {"FY2022": 0, "FY2021": 28, "FY2020": 6154}),
    ("DATA", "Deferred tax assets", {"FY2025": 614, "FY2024": 614, "FY2023": 569, "FY2022": 3489}),
    ("DATA", "Prepayments, accrued income and other assets", {"FY2025": 19810, "FY2024": 15677, "FY2023": 13332, "FY2022": 13447, "FY2021": 12868, "FY2020": 15355, "FY2019": 17449, "FY2018": 20309, "FY2017": 29757, "FY2016": 11616, "FY2015": 10695, "FY2014": 12366, "FY2013": 16299}),
    ("TOTAL", "Total Assets", {"FY2025": 2393946, "FY2024": 1702129, "FY2023": 1514720, "FY2022": 1538139, "FY2021": 1420688, "FY2020": 1997713, "FY2019": 2254083, "FY2018": 2374631, "FY2017": 2431239, "FY2016": 2722265, "FY2015": 3212625, "FY2014": 3825238, "FY2013": 3461866}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Deposits by banks", {"FY2025": 1622117, "FY2024": 974702, "FY2023": 751531, "FY2022": 810645, "FY2021": 411211, "FY2020": 1110415, "FY2019": 1380084, "FY2018": 1355754, "FY2017": 1475894, "FY2016": 1754538, "FY2015": 2048191, "FY2014": 2487979, "FY2013": 2300836}),
    ("DATA", "Customer accounts", {"FY2025": 160911, "FY2024": 165625, "FY2023": 244297, "FY2022": 247933, "FY2021": 530469, "FY2020": 386884, "FY2019": 395956, "FY2018": 467426, "FY2017": 375734, "FY2016": 391012, "FY2015": 661083, "FY2014": 860894, "FY2013": 742938}),
    ("DATA", "Derivative financial instruments", {"FY2025": 2245, "FY2024": 0, "FY2023": 0, "FY2022": 0, "FY2021": 117, "FY2020": 26708, "FY2019": 17277, "FY2018": 12466, "FY2017": 50936, "FY2016": 85667, "FY2015": 32245, "FY2014": 34706, "FY2013": 3263}),
    ("DATA", "Other liabilities", {"FY2025": 12447, "FY2024": 10872, "FY2023": 11801, "FY2022": 8101, "FY2021": 8054, "FY2020": 11467, "FY2019": 7882, "FY2018": 7363, "FY2017": 18913, "FY2016": 4691, "FY2015": 4191, "FY2014": 4265, "FY2013": 4206}),
    ("DATA", "Accruals and deferred income", {"FY2025": 1924, "FY2024": 3121, "FY2023": 5343, "FY2022": 2751, "FY2021": 476, "FY2020": 1280, "FY2019": 3133, "FY2018": 4564, "FY2017": 3433, "FY2016": 3658, "FY2015": 3933, "FY2014": 12212, "FY2013": 7239}),
    ("DATA", "Subordinated loan", {"FY2018": 100000, "FY2017": 100000, "FY2016": 100000, "FY2015": 100000, "FY2014": 100000, "FY2013": 100000}),
    ("DATA", "Provisions for liabilities", {"FY2022": 0, "FY2021": 1915, "FY2020": 2303, "FY2019": 2633, "FY2018": 2997, "FY2017": 3220, "FY2016": 1135, "FY2015": 241, "FY2014": 440, "FY2013": 1351}),
    ("DATA", "Current tax liabilities", {"FY2025": 27, "FY2024": 1705, "FY2023": 718, "FY2022": 830, "FY2021": 0, "FY2020": 0, "FY2019": 1805, "FY2018": 1175, "FY2017": 4091, "FY2016": 2357, "FY2015": 4421, "FY2014": 2135, "FY2013": 4915}),
    ("DATA", "Deferred tax liabilities", {"FY2025": 2859, "FY2024": 1454, "FY2023": 0, "FY2022": 0, "FY2021": 848, "FY2020": 2171, "FY2019": 1380, "FY2018": 449, "FY2017": 618, "FY2016": 1160, "FY2015": 1045, "FY2014": 156, "FY2013": 233}),
    ("TOTAL", "Total Liabilities", {"FY2025": 1802530, "FY2024": 1157479, "FY2023": 1013690, "FY2022": 1070260, "FY2021": 953090, "FY2020": 1541223, "FY2019": 1810150, "FY2018": 1952194, "FY2017": 2032839, "FY2016": 2344218, "FY2015": 2855350, "FY2014": 3502787, "FY2013": 3164981}),
    ("SECTION", "Share Capital and Reserves", {}),
    ("DATA", "Called up share capital", {"FY2025": 200000, "FY2024": 200000, "FY2023": 200000, "FY2022": 200000, "FY2021": 200000, "FY2020": 200000, "FY2019": 200000, "FY2018": 200000, "FY2017": 200000, "FY2016": 200000, "FY2015": 200000, "FY2014": 200000, "FY2013": 200000}),
    ("DATA", "Retained earnings", {"FY2025": 389313, "FY2024": 346433, "FY2023": 306770, "FY2022": 280635, "FY2021": 269268, "FY2020": 253752, "FY2019": 243217, "FY2018": 224235, "FY2017": 199057, "FY2016": 177359, "FY2015": 156551, "FY2014": 121620, "FY2013": 97704}),
    ("DATA", "Other reserves", {"FY2025": 2103, "FY2024": -1783, "FY2023": -5740, "FY2022": -12756, "FY2021": -1670, "FY2020": 2733, "FY2019": 716, "FY2018": -1798, "FY2017": -657, "FY2016": 688, "FY2015": 724, "FY2014": 831, "FY2013": -819}),
    ("TOTAL", "Total Share Capital and Reserves", {"FY2025": 591416, "FY2024": 544650, "FY2023": 501030, "FY2022": 467879, "FY2021": 467598, "FY2020": 456485, "FY2019": 443933, "FY2018": 422437, "FY2017": 398400, "FY2016": 378047, "FY2015": 357275, "FY2014": 322451, "FY2013": 296885}),
    ("TOTAL", "Total Liabilities and Share Capital and Reserves", {"FY2025": 2393946, "FY2024": 1702129, "FY2023": 1514720, "FY2022": 1538139, "FY2021": 1420688, "FY2020": 1997713, "FY2019": 2254083, "FY2018": 2374631, "FY2017": 2431239, "FY2016": 2722265, "FY2015": 3212625, "FY2014": 3825238, "FY2013": 3461866}),
]

bw.add_balance_sheet_sheet(
    title="ICBC (London) plc — Balance Sheet",
    subtitle="Solo basis, $'000 unless stated",
    rows=balance_sheet_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=75,
    source_height=170,
    unit_suffix=" ($'000)",
    years=YEARS,
)

# ---------------------------------------------------------------
# Profit & Loss
# ---------------------------------------------------------------
income_statement_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest receivable", {"FY2025": 73022, "FY2024": 80464, "FY2023": 64844, "FY2022": 27188, "FY2021": 19740, "FY2020": 30618, "FY2019": 55674, "FY2018": 67411, "FY2017": 57976, "FY2016": 69484, "FY2015": 82919, "FY2014": 89344, "FY2013": 71086}),
    ("DATA", "Interest payable", {"FY2025": -17005, "FY2024": -24461, "FY2023": -28971, "FY2022": -8992, "FY2021": -4294, "FY2020": -12493, "FY2019": -29651, "FY2018": -37960, "FY2017": -29349, "FY2016": -32005, "FY2015": -36884, "FY2014": -39318, "FY2013": -27956}),
    ("TOTAL", "Net interest income", {"FY2025": 56017, "FY2024": 56003, "FY2023": 35873, "FY2022": 18196, "FY2021": 15446, "FY2020": 18125, "FY2019": 26023, "FY2018": 29451, "FY2017": 28627, "FY2016": 37479, "FY2015": 46035, "FY2014": 50026, "FY2013": 43130}),
    ("DATA", "Fees and commissions receivable", {"FY2025": 2656, "FY2024": 2516, "FY2023": 1671, "FY2022": 1234, "FY2021": 1629, "FY2020": 1466, "FY2019": 1750, "FY2018": 4325, "FY2017": 7074, "FY2016": 6777, "FY2015": 13574, "FY2014": 17296, "FY2013": 21279}),
    ("DATA", "Fees and commissions payable", {"FY2025": -360, "FY2024": -403, "FY2023": -371, "FY2022": -369, "FY2021": -394, "FY2020": -550, "FY2019": -2819, "FY2018": -1127, "FY2017": -2339, "FY2016": -1451, "FY2015": -2011, "FY2014": -834, "FY2013": -912}),
    ("TOTAL", "Net fees and commissions", {"FY2025": 2296, "FY2024": 2113, "FY2023": 1300, "FY2022": 865, "FY2021": 1235, "FY2020": 916, "FY2019": -1069, "FY2018": 3198, "FY2017": 4735, "FY2016": 5326, "FY2015": 11563, "FY2014": 16462, "FY2013": 20367}),
    ("DATA", "Dealing (loss)/profit", {"FY2025": 709, "FY2024": 515, "FY2023": 375, "FY2022": -365, "FY2021": 422, "FY2020": 1179, "FY2019": 630, "FY2018": 1396, "FY2017": 1051, "FY2016": 354, "FY2015": -1482, "FY2014": -838, "FY2013": -1175}),
    ("DATA", "Other operating income", {"FY2025": 9798, "FY2024": 6773, "FY2023": 5844, "FY2022": 6583, "FY2021": 6118, "FY2020": 6140, "FY2019": 9374, "FY2018": 8288, "FY2017": 5174, "FY2016": 18010, "FY2015": 14340, "FY2014": 3497, "FY2013": -240}),
    ("TOTAL", "Other income", {"FY2025": 10507, "FY2024": 7288, "FY2023": 6219, "FY2022": 6218, "FY2021": 6540, "FY2020": 7319, "FY2019": 10004, "FY2018": 9715, "FY2017": 6225, "FY2016": 18358, "FY2015": 12858, "FY2014": 2666, "FY2013": -1415}),
    ("TOTAL", "Total operating income", {"FY2025": 68820, "FY2024": 65404, "FY2023": 43392, "FY2022": 25279, "FY2021": 23221, "FY2020": 26360, "FY2019": 34958, "FY2018": 42364, "FY2017": 39587, "FY2016": 61163, "FY2015": 70456, "FY2014": 69154, "FY2013": 62082}),
    ("SECTION", "Operating expenses", {}),
    ("DATA", "Staff costs", {"FY2025": -41255, "FY2024": -38325, "FY2023": -39301, "FY2022": -39373, "FY2021": -38201, "FY2020": -34134, "FY2019": -33657, "FY2018": -30039, "FY2017": -25684, "FY2016": -19533, "FY2015": -16789, "FY2014": -14898, "FY2013": -12955}),
    ("DATA", "Depreciation and amortisation", {"FY2025": -1208, "FY2024": -1154, "FY2023": -1234, "FY2022": -1463, "FY2021": -1962, "FY2020": -1967, "FY2019": -1830, "FY2018": -1783, "FY2017": -1741, "FY2016": -1882, "FY2015": -1912, "FY2014": -1980, "FY2013": -2422}),
    ("DATA", "Other operating charges", {"FY2025": -10247, "FY2024": -10487, "FY2023": -9009, "FY2022": -7385, "FY2021": -8297, "FY2020": -8012, "FY2019": -8291, "FY2018": -9094, "FY2017": -10623, "FY2016": -9885, "FY2015": -7921, "FY2014": -7040, "FY2013": -7755}),
    ("DATA", "Reimbursement of expenses attributable to the Branch", {"FY2025": 41197, "FY2024": 39091, "FY2023": 39539, "FY2022": 38664, "FY2021": 38503, "FY2020": 34543, "FY2019": 33738, "FY2018": 29697, "FY2017": 26621}),
    ("TOTAL", "Operating expenses", {"FY2025": -11513, "FY2024": -10875, "FY2023": -10005, "FY2022": -10609, "FY2021": -3425, "FY2020": -9570, "FY2019": -10040, "FY2018": -11219, "FY2017": -11427, "FY2016": -31300, "FY2015": -26622, "FY2014": -23918, "FY2013": -23132}),
    ("DATA", "Impairment (losses)/releases", {"FY2025": -52, "FY2024": 312, "FY2023": 1180, "FY2022": -1052, "FY2021": 6532, "FY2020": -3907, "FY2019": -618, "FY2018": -167, "FY2017": -1269, "FY2016": -2941, "FY2015": 921, "FY2014": -14710, "FY2013": -247}),
    ("TOTAL", "Profit on ordinary activities before tax", {"FY2025": 57255, "FY2024": 54841, "FY2023": 34567, "FY2022": 14670, "FY2021": 19796, "FY2020": 12883, "FY2019": 24300, "FY2018": 30978, "FY2017": 26891, "FY2016": 26922, "FY2015": 44755, "FY2014": 30526, "FY2013": 38703}),
    ("DATA", "Tax on profit on ordinary activities", {"FY2025": -14375, "FY2024": -15178, "FY2023": -8432, "FY2022": -3303, "FY2021": -4280, "FY2020": -2348, "FY2019": -5318, "FY2018": -5611, "FY2017": -5193, "FY2016": -6114, "FY2015": -9824, "FY2014": -6610, "FY2013": -9802}),
    ("TOTAL", "Profit for the financial year", {"FY2025": 42880, "FY2024": 39663, "FY2023": 26135, "FY2022": 11367, "FY2021": 15516, "FY2020": 10535, "FY2019": 18982, "FY2018": 25367, "FY2017": 21698, "FY2016": 20808, "FY2015": 34931, "FY2014": 23916, "FY2013": 28901}),
    ("SECTION", "Other comprehensive income", {}),
    ("DATA", "Change in fair value of financial investments at FVOCI", {"FY2025": 5190, "FY2024": 5430, "FY2023": 10201, "FY2022": -15385, "FY2021": -5679, "FY2020": 2244, "FY2019": 3342, "FY2018": -1431, "FY2017": -2033, "FY2016": -86, "FY2015": 480, "FY2014": 2279, "FY2013": -6402}),
    ("DATA", "Impairment allowance on financial investments at FVOCI", {"FY2025": -7, "FY2024": -116, "FY2023": -88, "FY2022": 123, "FY2021": -416, "FY2020": 417, "FY2019": 30, "FY2018": 72}),
    ("DATA", "Available-for-sale reserve recycled through profit and loss upon disposal", {"FY2016": 62, "FY2014": -61, "FY2013": 2212}),
    ("DATA", "Tax on components of other comprehensive income", {"FY2025": -1297, "FY2024": -1357, "FY2023": -3097, "FY2022": 4176, "FY2021": 1692, "FY2020": -644, "FY2019": -858, "FY2018": 193, "FY2017": 688, "FY2016": -12, "FY2015": -587, "FY2014": -568, "FY2013": 971}),
    ("TOTAL", "Other comprehensive income for the year, net of income tax", {"FY2025": 3886, "FY2024": 3957, "FY2023": 7016, "FY2022": -11086, "FY2021": -4403, "FY2020": 2017, "FY2019": 2514, "FY2018": -1166, "FY2017": -1345, "FY2016": -36, "FY2015": -107, "FY2014": 1650, "FY2013": -3219}),
    ("TOTAL", "Total comprehensive income for the year", {"FY2025": 46766, "FY2024": 43620, "FY2023": 33151, "FY2022": 281, "FY2021": 11113, "FY2020": 12552, "FY2019": 21496, "FY2018": 24201, "FY2017": 20353, "FY2016": 20772, "FY2015": 34824, "FY2014": 25566, "FY2013": 25682}),
]

bw.add_income_statement_sheet(
    title="ICBC (London) plc — Profit and Loss Account / Statement of Comprehensive Income",
    subtitle="Solo basis, $'000 unless stated",
    rows=income_statement_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=75,
    source_height=170,
    unit_suffix=" ($'000)",
    years=YEARS,
)

# ---------------------------------------------------------------
# Statement of Changes in Equity
# ---------------------------------------------------------------
EQUITY_HEADERS = ["Share capital", "Retained earning", "Other reserves", "Total shareholder's funds"]

equity_rows = [
    ("DATA", "At 1 January 2013", (200000, 68803, 2400, 271203)),
    ("DATA", "Profit for the year", (None, 28901, None, 28901)),
    ("DATA", "Change in fair value of available-for-sale financial investments", (None, None, -6402, -6402)),
    ("DATA", "Available-for-sale reserve recycled through profit and loss upon disposal", (None, None, 2212, 2212)),
    ("DATA", "Tax on other comprehensive income", (None, None, 971, 971)),
    ("TOTAL", "At 31 December 2013", (200000, 97704, -819, 296885)),
    ("DATA", "At 1 January 2014 (= FY2013 closing)", (200000, 97704, -819, 296885)),
    ("DATA", "Profit for the year", (None, 23916, None, 23916)),
    ("DATA", "Change in fair value of available-for-sale financial investments", (None, None, 2279, 2279)),
    ("DATA", "Available-for-sale reserve recycled through profit and loss upon disposal", (None, None, -61, -61)),
    ("DATA", "Tax on other comprehensive income", (None, None, -568, -568)),
    ("TOTAL", "At 31 December 2014", (200000, 121620, 831, 322451)),
    ("DATA", "At 1 January 2015 (= FY2014 closing)", (200000, 121620, 831, 322451)),
    ("DATA", "Profit for the year", (None, 34931, None, 34931)),
    ("DATA", "Change in fair value of available-for-sale financial investments", (None, None, 480, 480)),
    ("DATA", "Tax on other comprehensive income", (None, None, -587, -587)),
    ("TOTAL", "At 31 December 2015", (200000, 156551, 724, 357275)),
    ("DATA", "At 1 January 2016 (= FY2015 closing)", (200000, 156551, 724, 357275)),
    ("DATA", "Profit for the year", (None, 20808, None, 20808)),
    ("DATA", "Change in fair value of available-for-sale financial investments", (None, None, -86, -86)),
    ("DATA", "Available-for-sale reserve recycled through profit and loss upon disposal", (None, None, 62, 62)),
    ("DATA", "Tax on other comprehensive income", (None, None, -12, -12)),
    ("TOTAL", "At 31 December 2016", (200000, 177359, 688, 378047)),
    ("DATA", "At 1 January 2017 (= FY2016 closing)", (200000, 177359, 688, 378047)),
    ("DATA", "Profit for the year", (None, 21698, None, 21698)),
    ("DATA", "Change in fair value of available-for-sale financial investments", (None, None, -2033, -2033)),
    ("DATA", "Tax on other comprehensive income", (None, None, 688, 688)),
    ("TOTAL", "At 31 December 2017", (200000, 199057, -657, 398400)),
    ("DATA", "At 1 January 2018 (= FY2017 closing)", (200000, 199057, -657, 398400)),
    ("DATA", "Adjustment on initial application of IFRS 9", (None, -189, 25, -164)),
    ("TOTAL", "Restated balance at 1 January 2018", (200000, 198868, -632, 398236)),
    ("DATA", "Profit for the year", (None, 25367, None, 25367)),
    ("DATA", "Change in fair value of financial investments at FVOCI", (None, None, -1431, -1431)),
    ("DATA", "Impairment allowance charged on financial investments at FVOCI", (None, None, 72, 72)),
    ("DATA", "Tax on other comprehensive income", (None, None, 193, 193)),
    ("TOTAL", "At 31 December 2018", (200000, 224235, -1798, 422437)),
    ("DATA", "At 1 January 2019 (= FY2018 closing)", (200000, 224235, -1798, 422437)),
    ("DATA", "Profit for the year", (None, 18982, None, 18982)),
    ("DATA", "Change in fair value of financial investments at FVOCI", (None, None, 3342, 3342)),
    ("DATA", "Impairment allowance charged on financial investments at FVOCI", (None, None, 30, 30)),
    ("DATA", "Tax on other comprehensive income", (None, None, -858, -858)),
    ("TOTAL", "At 31 December 2019", (200000, 243217, 716, 443933)),
    ("DATA", "At 1 January 2020 (= FY2019 closing)", (200000, 243217, 716, 443933)),
    ("DATA", "Profit for the year", (None, 10535, None, 10535)),
    ("DATA", "Change in fair value of financial investments at FVOCI", (None, None, 2244, 2244)),
    ("DATA", "Impairment allowance released on financial investments at FVOCI", (None, None, 417, 417)),
    ("DATA", "Tax on other comprehensive income", (None, None, -644, -644)),
    ("TOTAL", "At 31 December 2020", (200000, 253752, 2733, 456485)),
    ("DATA", "At 1 January 2021", (200000, 253752, 2733, 456485)),
    ("DATA", "Profit for the year", (None, 15516, None, 15516)),
    ("DATA", "Change in fair value of financial investments at FVOCI", (None, None, -5679, -5679)),
    ("DATA", "Impairment charged on financial investments at FVOCI", (None, None, -416, -416)),
    ("DATA", "Tax on other comprehensive income", (None, None, 1692, 1692)),
    ("TOTAL", "At 31 December 2021", (200000, 269268, -1670, 467598)),
    ("DATA", "At 1 January 2022 (= FY2021 closing)", (200000, 269268, -1670, 467598)),
    ("DATA", "Profit for the year", (None, 11367, None, 11367)),
    ("DATA", "Change in fair value of financial investments at FVOCI", (None, None, -15385, -15385)),
    ("DATA", "Impairment released on financial investments at FVOCI", (None, None, 123, 123)),
    ("DATA", "Deferred tax liability recognised through equity", (None, None, 4176, 4176)),
    ("TOTAL", "At 31 December 2022", (200000, 280635, -12756, 467879)),
    ("DATA", "At 1 January 2023 (= FY2022 closing)", (200000, 280635, -12756, 467879)),
    ("DATA", "Profit for the year", (None, 26135, None, 26135)),
    ("DATA", "Change in fair value of financial investments at FVOCI", (None, None, 10201, 10201)),
    ("DATA", "Impairment charged on financial investments at FVOCI", (None, None, -88, -88)),
    ("DATA", "Tax on other comprehensive income", (None, None, -3097, -3097)),
    ("TOTAL", "At 31 December 2023", (200000, 306770, -5740, 501030)),
    ("DATA", "At 1 January 2024 (= FY2023 closing)", (200000, 306770, -5740, 501030)),
    ("DATA", "Profit for the year", (None, 39663, None, 39663)),
    ("DATA", "Change in fair value of financial investments at FVOCI", (None, None, 5430, 5430)),
    ("DATA", "Impairment charged on financial investments at FVOCI", (None, None, -116, -116)),
    ("DATA", "Tax on other comprehensive income", (None, None, -1357, -1357)),
    ("TOTAL", "At 31 December 2024", (200000, 346433, -1783, 544650)),
    ("DATA", "At 1 January 2025 (= FY2024 closing)", (200000, 346433, -1783, 544650)),
    ("DATA", "Profit for the year", (None, 42880, None, 42880)),
    ("DATA", "Change in fair value of financial investments at FVOCI", (None, None, 5190, 5190)),
    ("DATA", "Impairment released on financial investments at FVOCI", (None, None, -7, -7)),
    ("DATA", "Tax on other comprehensive income", (None, None, -1297, -1297)),
    ("TOTAL", "At 31 December 2025", (200000, 389313, 2103, 591416)),
]

bw.add_equity_changes_sheet(
    title="ICBC (London) plc — Statement of Changes in Equity",
    subtitle="$'000 - chronological, oldest to newest. Equity reconciliation ladder confirmed: every year's own "
              "closing balance ties exactly to both the next year's own opening balance and that year's own "
              "Balance Sheet Total Share Capital and Reserves - zero plug rows needed anywhere.",
    headers=EQUITY_HEADERS,
    rows=equity_rows,
    sources_text=STATEMENTS_SOURCES,
)

# ---------------------------------------------------------------
# Sheet: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Reconciliation of profit for the year to net cash flows from operating activities", {}),
    ("DATA", "Profit for the year", {"FY2025": 42880, "FY2024": 39663, "FY2023": 26135, "FY2022": 11367, "FY2021": 15516, "FY2020": 10535, "FY2019": 18982, "FY2018": 25367, "FY2017": 21698, "FY2016": 20808, "FY2015": 34931, "FY2014": 23916}),
    ("DATA", "Depreciation of tangible fixed assets", {"FY2025": 1106, "FY2024": 1073, "FY2023": 1070, "FY2022": 1301, "FY2021": 1819, "FY2020": 1816, "FY2019": 1742, "FY2018": 1701, "FY2017": 1668, "FY2016": 1879, "FY2015": 1912, "FY2014": 1980}),
    ("DATA", "Amortisation of intangible assets", {"FY2025": 102, "FY2024": 81, "FY2023": 164, "FY2022": 162, "FY2021": 143, "FY2020": 151, "FY2019": 88, "FY2018": 99, "FY2017": 73, "FY2016": 3}),
    ("DATA", "Impairment losses", {"FY2025": 52, "FY2024": -312, "FY2023": -1180, "FY2022": 1052, "FY2021": -6532, "FY2020": 3907, "FY2019": 618, "FY2018": 167, "FY2017": 1269, "FY2016": 2941, "FY2015": -921, "FY2014": 14710}),
    ("DATA", "Interest income", {"FY2025": -73022, "FY2024": -80464, "FY2023": -64844, "FY2022": -27188, "FY2021": -19740, "FY2020": -30618, "FY2019": -55674, "FY2018": -67411, "FY2017": -57976, "FY2016": -69484, "FY2015": -82919, "FY2014": -89344}),
    ("DATA", "Interest expense", {"FY2025": 17005, "FY2024": 24461, "FY2023": 28971, "FY2022": 8992, "FY2021": 4294, "FY2020": 12493, "FY2019": 29651, "FY2018": 37960, "FY2017": 29349, "FY2016": 32005, "FY2015": 36884, "FY2014": 39318}),
    ("DATA", "Gain on sale of financial investments at FVOCI", {"FY2025": -139, "FY2024": 0, "FY2021": 0, "FY2020": -199, "FY2019": 0, "FY2018": -28, "FY2017": 0, "FY2016": 7, "FY2015": 0}),
    ("DATA", "Exchange gain and accretion of discounts and amortisation of premiums on financial investments", {"FY2025": 4619, "FY2024": 7528, "FY2023": -4149, "FY2022": 21189, "FY2021": 555, "FY2020": -15104, "FY2019": -2297, "FY2018": 474, "FY2017": 1767, "FY2016": 8834, "FY2015": 6506, "FY2014": 13934}),
    ("DATA", "Revaluation (gain)/loss on financial derivatives", {"FY2025": 2500, "FY2024": -189, "FY2023": -66, "FY2022": -96, "FY2021": -497, "FY2020": 939, "FY2019": -145, "FY2018": 983, "FY2017": -522, "FY2016": 792, "FY2015": 4512, "FY2014": -7775}),
    ("DATA", "Tax on profit on ordinary activities", {"FY2025": 14375, "FY2024": 15178, "FY2023": 8432, "FY2022": 3303, "FY2021": 4280, "FY2020": 2348, "FY2019": 5318, "FY2018": 5611, "FY2017": 5193, "FY2016": 6114, "FY2015": 9824, "FY2014": 6610}),
    ("SECTION", "Changes in operating assets and liabilities", {}),
    ("DATA", "Loans to banks", {"FY2025": 764198, "FY2024": -436287, "FY2023": 136996, "FY2022": -160146, "FY2021": 149827, "FY2020": 118342, "FY2019": 183979, "FY2018": -63378, "FY2017": 276532, "FY2016": 203049, "FY2015": -353423, "FY2014": 37241}),
    ("DATA", "Loans and advances to customers", {"FY2025": -77176, "FY2024": 93250, "FY2023": -97842, "FY2022": -203380, "FY2021": 305578, "FY2020": 82313, "FY2019": 294894, "FY2018": 144068, "FY2017": 70269, "FY2016": 319708, "FY2015": 804752, "FY2014": -320653}),
    ("DATA", "Financial investments at FVOCI", {"FY2025": 408, "FY2024": -60711, "FY2023": 17973, "FY2022": 66827, "FY2021": 46073, "FY2020": -6671, "FY2019": 8156}),
    ("DATA", "Financial investments at amortised cost", {"FY2025": -9488, "FY2024": 41729, "FY2023": 106936, "FY2022": 35881, "FY2021": -13036, "FY2020": -30674, "FY2019": 30000}),
    ("DATA", "Other assets", {"FY2025": -3319, "FY2024": -957, "FY2023": 1104, "FY2022": -720, "FY2021": 1762, "FY2020": 512, "FY2019": -801, "FY2018": -3158, "FY2017": -16268, "FY2016": -538, "FY2015": -94, "FY2014": 5198}),
    ("DATA", "Deposits by banks", {"FY2025": 647415, "FY2024": 223171, "FY2023": -59118, "FY2022": 399437, "FY2021": -699204, "FY2020": -269669, "FY2019": 24330, "FY2018": -120140, "FY2017": -278644, "FY2016": -293653, "FY2015": -439788, "FY2014": 187143}),
    ("DATA", "Deposits from customers", {"FY2025": -4714, "FY2024": -78671, "FY2023": -3639, "FY2022": -282533, "FY2021": 143585, "FY2020": -9072, "FY2019": -71470, "FY2018": 91692, "FY2017": -15278, "FY2016": -270071, "FY2015": -199811, "FY2014": 117956}),
    ("DATA", "Subordinated loan repaid", {"FY2019": -100000}),
    ("DATA", "Other liabilities", {"FY2025": 1613, "FY2024": -1030, "FY2023": 3697, "FY2022": -1865, "FY2021": 1733, "FY2020": -2281, "FY2019": 200, "FY2018": 154, "FY2017": 16506, "FY2016": 1149, "FY2015": 251, "FY2014": -852}),
    ("DATA", "Interest received", {"FY2025": 72209, "FY2024": 79076, "FY2023": 63856, "FY2022": 27330, "FY2021": 20462, "FY2020": 32200, "FY2019": 59335, "FY2018": 66312, "FY2017": 66073, "FY2016": 69101, "FY2015": 84684, "FY2014": 88079}),
    ("DATA", "Interest paid", {"FY2025": -18202, "FY2024": -26683, "FY2023": -26378, "FY2022": -6721, "FY2021": -5095, "FY2020": -14346, "FY2019": -30790, "FY2018": -36643, "FY2017": -29773, "FY2016": -32035, "FY2015": -45687, "FY2014": -34345}),
    ("DATA", "Income tax paid", {"FY2025": -15945, "FY2024": -14140, "FY2023": -8715, "FY2022": -2607, "FY2021": -3266, "FY2020": -4680, "FY2019": -4616, "FY2018": -7208, "FY2017": -3313, "FY2016": -8075, "FY2015": -7235, "FY2014": -10035}),
    ("TOTAL", "Net cash used in operating activities", {"FY2025": 1366477, "FY2024": -174234, "FY2023": 129403, "FY2022": -108415, "FY2021": -51743, "FY2020": -117758, "FY2019": 353344, "FY2018": 76619, "FY2017": 78623, "FY2016": -7467, "FY2015": -145622, "FY2014": 73081}),
    ("SECTION", "Cash flow from investing activities", {}),
    ("DATA", "Acquisition of financial investments at FVOCI", {"FY2019": -48844, "FY2018": -224306, "FY2017": -226102, "FY2014": -157226}),
    ("DATA", "Maturity/Disposal of financial investments at FVOCI", {"FY2019": 57000, "FY2018": 275189, "FY2017": 166059, "FY2016": 94644, "FY2015": 115652, "FY2014": 133613}),
    ("DATA", "Acquisition of financial investments at amortised cost", {"FY2018": -142014, "FY2017": -69678}),
    ("DATA", "Maturity of financial investments at amortised cost", {"FY2019": 30000, "FY2018": 19688}),
    ("DATA", "Acquisition of tangible fixed assets", {"FY2025": -638, "FY2024": -332, "FY2023": -87, "FY2022": -367, "FY2021": -660, "FY2020": -239, "FY2019": -302, "FY2018": -468, "FY2017": -174, "FY2016": -53, "FY2015": -376, "FY2014": -98}),
    ("DATA", "Disposal of tangible fixed assets", {"FY2018": 3, "FY2016": 1}),
    ("DATA", "Acquisition of intangible assets", {"FY2025": -126, "FY2024": -115, "FY2023": -188, "FY2022": -158, "FY2021": -133, "FY2020": -147, "FY2019": -103, "FY2018": -65, "FY2017": -223, "FY2016": -31}),
    ("TOTAL", "Net cash used in investing activities", {"FY2025": -764, "FY2024": -447, "FY2023": -275, "FY2022": -525, "FY2021": -793, "FY2020": -386, "FY2019": 37751, "FY2018": -71973, "FY2017": -130118, "FY2016": 94561, "FY2015": 115276, "FY2014": -23711}),
    ("TOTAL", "Net cash from financing activities", {"FY2025": 0, "FY2024": 0, "FY2023": 0, "FY2022": 0, "FY2021": 0, "FY2020": 0, "FY2019": 0, "FY2018": 0, "FY2017": 0, "FY2016": 0, "FY2015": 0, "FY2014": 0}),
    ("TOTAL", "Net decrease in cash and cash equivalents", {"FY2025": 1365713, "FY2024": -174681, "FY2023": 129128, "FY2022": -108940, "FY2021": -52536, "FY2020": -118144, "FY2019": 391095, "FY2018": 4646, "FY2017": -51495, "FY2016": 87094, "FY2015": -30346, "FY2014": 49370}),
    ("DATA", "Cash and cash equivalents at 1 January", {"FY2025": 139627, "FY2024": 316971, "FY2023": 180382, "FY2022": 307556, "FY2021": 361540, "FY2020": 470286, "FY2019": 78694, "FY2018": 71939, "FY2017": 126704, "FY2016": 41812, "FY2015": 73549, "FY2014": 25010}),
    ("DATA", "Effects of exchange rates on cash and cash equivalents", {"FY2025": -6647, "FY2024": -2663, "FY2023": 7461, "FY2022": -18234, "FY2021": -1448, "FY2020": 9398, "FY2019": 497, "FY2018": 2109, "FY2017": -3270, "FY2016": -2202, "FY2015": -1391, "FY2014": -831}),
    ("TOTAL", "Cash and cash equivalents at 31 December", {"FY2025": 1498693, "FY2024": 139627, "FY2023": 316971, "FY2022": 180382, "FY2021": 307556, "FY2020": 361540, "FY2019": 470286, "FY2018": 78694, "FY2017": 71939, "FY2016": 126704, "FY2015": 41812, "FY2014": 73549}),
]

bw.add_cash_flow_sheet(
    title="ICBC (London) plc — Statement of Cash Flows",
    subtitle="Solo basis, $'000 unless stated",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=75,
    source_height=140,
    unit_suffix=" ($'000)",
    years=YEARS,
)

# ---------------------------------------------------------------
# Asset Quality
# ---------------------------------------------------------------
asset_quality_rows = [
    ("SECTION", "Loans and advances to customers, legacy IAS 39 basis (FY2014-2017, specific/collective impairment)", {}),
    ("DATA", "Gross carrying amount (net of loan fees received in advance)", {"FY2017": 960267, "FY2016": 1041515, "FY2015": 1361223, "FY2014": 2165975}),
    ("DATA", "Collective impairment allowance", {"FY2017": -2035, "FY2016": -1990, "FY2015": -2079, "FY2014": -2760}),
    ("DATA", "Specific impairment allowance", {"FY2017": -5000, "FY2016": -15000, "FY2015": -12000, "FY2014": -12000}),
    ("TOTAL", "Net carrying amount", {"FY2017": 953232, "FY2016": 1024525, "FY2015": 1347144, "FY2014": 2151215}),
    ("DATA", "Specific provision coverage of specifically-impaired loans", {"FY2017": "$5,000k allowance held against $5,000k of gross specifically-impaired loans (2016: $15,000k against $30,000k)"}),
    ("SECTION", "Loans and advances to customers, by IFRS 9 stage (FY2018 onward)", {}),
    ("DATA", "Gross carrying amount", {"FY2025": 413561, "FY2024": 336385, "FY2023": 429636, "FY2022": 331794, "FY2021": 128414, "FY2020": 433992, "FY2019": 516305, "FY2018": 816199}),
    ("DATA", "Stage 1 loss allowance", {"FY2025": -235, "FY2024": -129, "FY2023": -355, "FY2022": -310, "FY2021": -66, "FY2020": -840, "FY2019": -306, "FY2018": -1004}),
    ("DATA", "Stage 2 loss allowance", {"FY2025": 0, "FY2024": 0, "FY2023": 0, "FY2022": 0, "FY2021": 0, "FY2020": -4594, "FY2019": -2720, "FY2018": -1111}),
    ("DATA", "Stage 3 loss allowance", {"FY2025": 0, "FY2024": 0, "FY2023": 0, "FY2022": 0, "FY2021": 0, "FY2020": 0, "FY2019": 0, "FY2018": -5000}),
    ("TOTAL", "Net carrying amount", {"FY2025": 413326, "FY2024": 336256, "FY2023": 429281, "FY2022": 331484, "FY2021": 128348, "FY2020": 428558, "FY2019": 513279, "FY2018": 809084}),
    ("DATA", "Stage 1 coverage ratio (Stage 1 allowance / gross carrying amount)", {"FY2025": "0.06%", "FY2024": "0.04%", "FY2023": "0.08%", "FY2022": "0.09%", "FY2021": "0.05%", "FY2020": "0.19%", "FY2019": "0.06%", "FY2018": "0.12%"}),
    ("DATA", "Stage 2/3 (impaired) exposure as % of gross carrying amount", {"FY2025": "0.00%", "FY2024": "0.00%", "FY2023": "0.00%", "FY2022": "0.00%", "FY2021": "0.00%"}),
]

bw.add_asset_quality_sheet(
    title="ICBC (London) plc — Asset Quality",
    subtitle="Loans and advances to customers, solo basis, $'000 unless stated",
    rows=asset_quality_rows,
    sources_text=ASSET_QUALITY_SOURCES,
    first_col_width=75,
    source_height=170,
    unit_suffix=" ($'000)",
)

# ---------------------------------------------------------------
# Sheet: KM1 Key Metrics (KM1-016)
#
# ICBC (London) plc prints the template under its own heading "UK KM1 - Key
# metric template" in every edition FY2021-FY2025 - as a numbered annex
# ("Annex 2") in the FY2021 and FY2025 editions and inline in the risk-
# management section in FY2022-FY2024. The row set, row numbers, labels and
# printed precision are identical across all five editions; only the column
# dates move.
#
# COLUMNS: each edition prints FIVE columns headed T / T-1 / T-2 / T-3 / T-4 -
# 31 December of its own year, then the three preceding quarter-ends, then the
# prior 31 December. Only the leftmost (T, 31 December) column is used, so every
# cell on this sheet is the figure that year's OWN edition published as its
# reporting date. This matters for FY2022, where the two editions disagree: the
# FY2022 edition's own 31/12/2022 column gives RWA 902,856.95 and all three
# ratios 50.54%, while the FY2023 edition's 31/12/2022 comparative gives
# 900,460.13 and 50.67%. The FY2022 edition's own figures are used (map rule 1).
#
# ROW SET: constant across the five editions, and shorter than the full
# template - ICBC prints only the rows that carry a value. Rows UK 7a, UK 7b,
# UK 7c, UK 8a, UK 9a, 10 and UK 10a appear in NO edition, and neither does the
# IFRS9-FL "as if" block. Only UK 7d is printed from the SREP block. The three
# buffer rows ICBC does print are 8, 9, 11 and UK 11a, then 12. Nothing has been
# added to fill the gaps: an omitted row is the Bank's omission, not ours.
#
# UNITS (map rule 17): "USD 000's" in all five editions, with no unit change
# anywhere in the series, so the amount rows need only one caption block. ICBC
# prints the unit once as a caption above the table rather than on each section
# heading; it is repeated on the amount section dividers here so each row's unit
# is readable in isolation, and so the workbook's own unit resolution works.
# This sheet stays in USD, the currency the Bank published it in, like every
# other sheet in this workbook.
#
# THE TABLE BREAKS ACROSS TWO PAGES in all five editions (map rule 12): the
# "Liquidity Coverage Ratio" heading is the last line of the first page and rows
# 15-20 continue on the next, so both pages are cited.
#
# FY2020 AND EARLIER ARE BLANK because the template is not used, not because no
# Pillar 3 exists - see the source note. The FY2018, FY2019 and FY2020 editions
# were located for this ticket and read; they carry bespoke "Table 1 - Own
# Funds" and leverage tables instead, whose figures are on the single-metric
# sheets in this workbook, not re-labelled onto template row numbers here.
# ---------------------------------------------------------------
km1_rows = [
    ("SECTION", "Available own funds (amounts) (USD $'000)", {}),
    ("DATA", "1    Common Equity Tier 1 (CET1) capital",
     {"FY2025": 547878.17, "FY2024": 504453.52, "FY2023": 474458.88, "FY2022": 456299.84, "FY2021": 451197.05}),
    ("DATA", "2    Tier 1 capital",
     {"FY2025": 547878.17, "FY2024": 504453.52, "FY2023": 474458.88, "FY2022": 456299.84, "FY2021": 451197.05}),
    ("DATA", "3    Total capital",
     {"FY2025": 547878.17, "FY2024": 504453.52, "FY2023": 474458.88, "FY2022": 456299.84, "FY2021": 451197.05}),
    ("SECTION", "Risk-weighted exposure amounts (USD $'000)", {}),
    ("DATA", "4    Total risk-weighted exposure amount",
     {"FY2025": 675667.75, "FY2024": 719040.48, "FY2023": 842738.48, "FY2022": 902856.95, "FY2021": 739776.26}),
    ("SECTION", "Capital ratios (as a percentage of risk-weighted exposure amount)", {}),
    ("DATA", "5    Common Equity Tier 1 ratio (%)",
     {"FY2025": "81.09%", "FY2024": "70.16%", "FY2023": "56.30%", "FY2022": "50.54%", "FY2021": "60.99%"}),
    ("DATA", "6    Tier 1 ratio (%)",
     {"FY2025": "81.09%", "FY2024": "70.16%", "FY2023": "56.30%", "FY2022": "50.54%", "FY2021": "60.99%"}),
    ("DATA", "7    Total capital ratio (%)",
     {"FY2025": "81.09%", "FY2024": "70.16%", "FY2023": "56.30%", "FY2022": "50.54%", "FY2021": "60.99%"}),
    ("SECTION", "Additional own funds requirements based on SREP (as a percentage of risk-weighted exposure amount)", {}),
    ("DATA", "UK 7d    Total SREP own funds requirements (%)",
     {"FY2025": "13.05%", "FY2024": "13.05%", "FY2023": "12.89%", "FY2022": "12.89%", "FY2021": "12.89%"}),
    ("SECTION", "Combined buffer requirement (as a percentage of risk-weighted exposure amount)", {}),
    ("DATA", "8    Capital conservation buffer (%)",
     {"FY2025": "2.50%", "FY2024": "2.50%", "FY2023": "2.50%", "FY2022": "2.50%", "FY2021": "2.50%"}),
    ("DATA", "9    Institution specific countercyclical capital buffer (%)",
     {"FY2025": "1.32%", "FY2024": "1.22%", "FY2023": "0.42%", "FY2022": "0.02%", "FY2021": "0.03%"}),
    ("DATA", "11    Combined buffer requirement (%)",
     {"FY2025": "3.82%", "FY2024": "3.72%", "FY2023": "2.92%", "FY2022": "2.52%", "FY2021": "2.53%"}),
    ("DATA", "UK 11a    Overall capital requirements (%)",
     {"FY2025": "16.87%", "FY2024": "16.77%", "FY2023": "15.81%", "FY2022": "15.41%", "FY2021": "15.42%"}),
    ("DATA", "12    CET1 available after meeting the total SREP own funds requirements (%)",
     {"FY2025": "64.21%", "FY2024": "55.39%", "FY2023": "40.49%", "FY2022": "35.13%", "FY2021": "45.58%"}),
    ("SECTION", "Leverage ratio (amounts USD $'000; ratio %)", {}),
    ("DATA", "13    Leverage ratio total exposure measure",
     {"FY2025": 1153888.52, "FY2024": 1493766.54, "FY2023": 1339718.25, "FY2022": 1436983.22, "FY2021": 1467315.30}),
    ("DATA", "14    Leverage ratio",
     {"FY2025": "47.48%", "FY2024": "33.77%", "FY2023": "35.41%", "FY2022": "31.75%", "FY2021": "30.75%"}),
    ("SECTION", "Liquidity Coverage Ratio (amounts USD $'000; ratio %)", {}),
    ("DATA", "15    Total high-quality liquid assets (HQLA) (Weighted value -average)",
     {"FY2025": 1374778.95, "FY2024": 328481.85, "FY2023": 384068.74, "FY2022": 288785.45, "FY2021": 351221.56}),
    ("DATA", "UK 16a    Cash outflows - Total weighted value",
     {"FY2025": 1514094.63, "FY2024": 750256.41, "FY2023": 544239.26, "FY2022": 672293.52, "FY2021": 285016.39}),
    ("DATA", "UK 16b    Cash inflows - Total weighted value",
     {"FY2025": 557414.30, "FY2024": 935548.41, "FY2023": 474499.70, "FY2022": 518663.74, "FY2021": 458374.15}),
    ("DATA", "16    Total net cash outflows (adjusted value)",
     {"FY2025": 956680.33, "FY2024": 187564.10, "FY2023": 136059.82, "FY2022": 168073.38, "FY2021": 71254.10}),
    ("DATA", "17    Liquidity coverage ratio (%)",
     {"FY2025": "143.70%", "FY2024": "175.13%", "FY2023": "282.28%", "FY2022": "171.82%", "FY2021": "492.91%"}),
    ("SECTION", "Net Stable Funding Ratio (amounts USD $'000; ratio %)", {}),
    ("DATA", "18    Total available stable funding",
     {"FY2025": 581574.20, "FY2024": 608923.53, "FY2023": 798010.24, "FY2022": 694606.62, "FY2021": 839388.75}),
    ("DATA", "19    Total required stable funding",
     {"FY2025": 335509.49, "FY2024": 407761.68, "FY2023": 477595.45, "FY2022": 511526.78, "FY2021": 558997.10}),
    ("DATA", "20    NSFR ratio (%)",
     {"FY2025": "173.34%", "FY2024": "149.33%", "FY2023": "167.09%", "FY2022": "135.79%", "FY2021": "150.16%"}),
]

KM1_SOURCES = (
    "Sources - ICBC (London) plc's OWN standalone Pillar 3 Disclosures (solo basis), the table the Bank "
    "heads 'UK KM1 - Key metric template'. Each year is taken from the leftmost (T, 31 December) column of "
    "the edition in which that year is the reporting year - never from a later edition's comparative. The "
    "table breaks across two pages in every edition (the 'Liquidity Coverage Ratio' heading ends one page "
    "and rows 15-20 begin the next), so both pages are cited. Every PDF was re-downloaded for this ticket "
    "and verified by HTTP 200, Content-Type application/pdf and %PDF magic bytes:\n"
    f"FY2025: Pillar 3 Disclosures 2025, 'Annex 2 - UK KM1 - Key metric template', pp.33-34 - {P3_25_URL}\n"
    f"FY2024: Pillar 3 Disclosures 2024, 'UK KM1 - Key metric template', pp.12-13 - {P3_24_URL}\n"
    f"FY2023: Pillar 3 Disclosures 2023, 'UK KM1 - Key metric template', pp.12-13 - {P3_23_URL}\n"
    f"FY2022: Pillar 3 Disclosures 2022, 'UK KM1 - Key metric template', pp.12-13 - {P3_22_URL}\n"
    f"FY2021: Pillar 3 Disclosures 2021, 'UK KM1 - Key metric template', pp.14-15 - {P3_21_URL}\n\n"
    "LATEST-EDITION CHECK, 2026-09-16: checked the Bank's OWN website, not this project's cited URLs and "
    "not Wayback. ICBC (London) plc's site is www.icbclondon.com; its disclosure list is at About Us > "
    "ICBC (London) Plc > Annual Report, which returned HTTP 200 and lists Annual Reports for every year "
    "2003-2025, the newest being the 2025 Annual Report, followed by the line 'Pillar 3 disclosures: "
    "Please click here for disclosure' whose link points at the 2025 Pillar 3 Disclosure. So the newest "
    "Annual Report is FY2025 and the newest Pillar 3 is FY2025, both of which this workbook already "
    "holds. FY2026 is not a complete financial year (the Bank's year end is 31 December) and no 2026 "
    "document of either kind exists. CHECKED, NONE NEWER. Note that the Bank's own page links only ONE "
    "Pillar 3 document - the current one - which is why the back catalogue has to be found by direct URL "
    "rather than by reading the page.\n\n"
    "ENTITY: ICBC (London) plc, FRN 190017, Companies House 04552753 - a UK-incorporated subsidiary of "
    "Industrial and Commercial Bank of China Limited. It is NOT ICBC Standard Bank plc, a separate "
    "PRA-authorised UK bank (FRN 124876) with its own, differently-shaped Pillar 3 disclosures and its own "
    "workbook in this project; the two publish on adjacent paths of the same v.icbc.com.cn CDN and must "
    "not be crossed. Every figure on this sheet comes from a document whose running header reads 'Pillar 3 "
    "Disclosures <year>  ICBC (London) plc'. The Bank has no subsidiaries and the disclosures are solo.\n\n"
    "WHY FY2020 AND EARLIER ARE BLANK - 'the template is not used', on positive evidence, NOT 'no Pillar 3 "
    "is published' (map rules 8 and 16). The FY2018, FY2019 and FY2020 Pillar 3 Disclosures were located "
    "for this ticket and read in full; all three exist on the Bank's own CDN, misfiled one year forward in "
    "exactly the way already documented for FY2021/FY2022:\n"
    f"    FY2020 - {P3_20_URL}\n"
    f"    FY2019 - {P3_19_URL}\n"
    f"    FY2018 - {P3_18_URL}\n"
    "None of the three contains the UK KM1 template, and the reason is stated in the documents themselves: "
    "each says the CRR II Pillar 3 requirements (articles 433-455) 'are expected to be applicable from "
    "June 2021'. The template post-dates them. What they print instead is a bespoke 'Table 1 - Own Funds' "
    "(paid-up capital, retained earnings, CET1, Tier 1, Tier 2, Total Capital, Total risk weighted "
    "exposures, three capital ratios and an 'Institution specific buffer requirement' block) with a "
    "current-year/prior-year column pair, plus a separate narrative leverage ratio section - which fails "
    "the row-set test the same way ABC International Bank's 'Table 3' does: no SREP row, no UK-numbered "
    "buffer rows, no LCR build-up rows, no NSFR rows, and it adds 'Paid up capital' and 'Retained "
    "earnings' lines the template does not have. Those figures are NOT re-labelled onto KM1 row numbers "
    "here; they are carried, as published, on this workbook's Total RWAs, CET1/Tier 1/Total Capital Ratio "
    "and Leverage Ratio sheets, which now run back to FY2017 as a result.\n"
    "This was checked for an image-only table too (map rule 13). Text extraction on all three is rich, not "
    "silent - the FY2020 document yields 111 hits for 'capital', 145 for 'ratio' and 26 for 'Leverage' "
    "against 0 for 'KM1' - so the zero is a fact about the document, not about the tool (rule 15). "
    "`pdfimages -list` reports four embedded bitmaps in each; the two non-logo ones were rendered at "
    "120dpi and LOOKED AT rather than inferred from, and are a governance organisation chart and the ECAI "
    "credit-quality-step mapping table, neither of them a key-metrics table. Page selection was anchored "
    "on each document's own table of contents rather than on any digit-density heuristic (rule 16).\n"
    "No Pillar 3 edition earlier than FY2018 was located under any filename pattern tried. That is 'not "
    "located', not 'does not exist' (rule 9).\n\n"
    "PRECISION AND GLYPHS, reproduced not normalised: ICBC prints amounts to two decimal places of "
    "USD '000 and ratios to two decimal places with a per cent sign, in every edition, and this sheet "
    "keeps both. No cell in any of the five editions' 31 December columns is a dash or a blank, so no "
    "dash-versus-zero judgement arises.\n\n"
    "A SOURCE ANOMALY IN THE FY2025 LCR BLOCK, recorded and not corrected (map rule 7). The FY2025 "
    "edition's 31/12/2025 column reports HQLA of 1,374,778.95 against a leverage ratio total exposure "
    "measure of 1,153,888.52 for the same date - that is, average high-quality liquid assets larger than "
    "the whole balance sheet plus off-balance-sheet exposure. The same column's cash outflows "
    "(1,514,094.63) and net outflows (956,680.33) are roughly three times the previous quarter's, while "
    "the NSFR block beside them (581,574.20 / 335,509.49) is of an ordinary size. The block is internally "
    "consistent - UK 16a minus UK 16b equals row 16 exactly, and row 15 divided by row 16 gives the "
    "printed 143.70% exactly - so it is reproduced verbatim, as is the LCR sheet's FY2025 figure, which "
    "comes from the same table. A reader comparing FY2025 liquidity with FY2024 should know this."
    + "\n\n" + p3_sources()
)

bw.add_km1_sheet(
    title="ICBC (London) plc — KM1 Key Metrics",
    subtitle="ICBC (London) plc's own published 'UK KM1 - Key metric template', reproduced in the Bank's row "
             "order with its own row references, labels and printed precision. Amounts USD $'000, ratios as "
             "printed (%); the sheet stays in the currency the Bank published it in. Solo basis - the Bank has "
             "no subsidiaries. Each year is the 31 December (T) column of that year's own edition. FY2020 and "
             "earlier are blank because those editions predate the template and do not use it — not because no "
             "Pillar 3 exists; see the source note.",
    rows=km1_rows,
    sources_text=KM1_SOURCES,
    years=["FY2025", "FY2024", "FY2023", "FY2022", "FY2021", "FY2020"],
    first_col_width=70,
    source_height=460,
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, f"Solo basis, {unit}" if unit else "Solo basis",
                         rows_data, sources_text, note=note, first_col_width=48, source_height=140)

metric(
    "CET1 Capital", "$'000",
    [("Common Equity Tier 1 (CET1) capital", {"FY2025": 547878, "FY2024": 504454, "FY2023": 474459, "FY2022": 456300, "FY2021": 451197, "FY2020": 456128, "FY2019": 443521, "FY2018": 422168, "FY2017": 397848, "FY2016": 378047, "FY2015": 357275, "FY2014": 322451})],
    p3_sources() + "\n\n" + p3_capital_sources_1420(),
)

metric(
    "CET1 Ratio", "% of RWA",
    [("Common Equity Tier 1 ratio", {"FY2025": "81.09%", "FY2024": "70.16%", "FY2023": "56.30%", "FY2022": "50.54%", "FY2021": "60.99%",
                                     "FY2020": "44.60%", "FY2019": "38.72%", "FY2018": "26.84%", "FY2017": "22.17%"})],
    p3_sources() + "\n\n" + p3_prekm1_sources(),
)

metric(
    "Tier 1 Capital", "$'000",
    [("Tier 1 capital", {"FY2025": 547878, "FY2024": 504454, "FY2023": 474459, "FY2022": 456300, "FY2021": 451197, "FY2020": 456128, "FY2019": 443521, "FY2018": 422168, "FY2017": 397848, "FY2016": 378047, "FY2015": 357275, "FY2014": 322451})],
    p3_sources() + "\n\n" + p3_capital_sources_1420(),
)

metric(
    "Tier 1 Ratio", "% of RWA",
    [("Tier 1 ratio", {"FY2025": "81.09%", "FY2024": "70.16%", "FY2023": "56.30%", "FY2022": "50.54%", "FY2021": "60.99%",
                       "FY2020": "44.60%", "FY2019": "38.72%", "FY2018": "26.84%", "FY2017": "22.17%"})],
    p3_sources() + "\n\n" + p3_prekm1_sources(),
)

metric(
    "Total Capital", "$'000",
    [("Total capital", {"FY2025": 547878, "FY2024": 504454, "FY2023": 474459, "FY2022": 456300, "FY2021": 451197, "FY2020": 456128, "FY2019": 443521, "FY2018": 518606, "FY2017": 500128, "FY2016": 480067, "FY2015": 459354, "FY2014": 425451})],
    p3_sources() + "\n\n" + p3_capital_sources_1420(),
)

metric(
    "Total Capital Ratio", "% of RWA",
    [("Total capital ratio", {"FY2025": "81.09%", "FY2024": "70.16%", "FY2023": "56.30%", "FY2022": "50.54%", "FY2021": "60.99%",
                              "FY2020": "44.60%", "FY2019": "38.72%", "FY2018": "32.97%", "FY2017": "27.87%"})],
    p3_sources() + "\n\n" + p3_prekm1_sources(),
)

metric(
    "Total RWAs", "$'000",
    [("Total risk-weighted exposure amount", {"FY2025": 675668, "FY2024": 719040, "FY2023": 842738, "FY2022": 902857, "FY2021": 739776,
                                              "FY2020": 1022681, "FY2019": 1145387, "FY2018": 1572886, "FY2017": 1793374})],
    p3_sources() + "\n\n" + p3_prekm1_sources(),
)

rwa_breakdown_rows = [
    ("DATA", "Credit risk (excluding CCR)",
     {"FY2025": 590477.63, "FY2024": 660913.86, "FY2023": 795488.58, "FY2022": 848322.89, "FY2021": 671772.29}),
    ("DATA", "Counterparty credit risk (CCR)",
     {"FY2025": 748.81, "FY2024": 294.72, "FY2023": 0, "FY2022": 0, "FY2021": 20.86}),
    ("DATA", "Operational risk",
     {"FY2025": 84197.30, "FY2024": 57831.90, "FY2023": 47249.90, "FY2022": 54534.06, "FY2021": 67983.12}),
    ("TOTAL", "Total risk weighted exposure amount",
     {"FY2025": 675423.74, "FY2024": 719040.48, "FY2023": 842738.48, "FY2022": 902856.95, "FY2021": 739776.26}),
]

bw.add_rwa_breakdown_sheet(
    title="ICBC (London) plc — RWA Breakdown",
    subtitle="Solo basis, UK OV1 template, $'000",
    rows=rwa_breakdown_rows,
    sources_text=rwa_sources(),
    first_col_width=60,
    source_height=170,
    unit_suffix=" ($'000)",
)

metric(
    "Leverage Ratio", "$'000 / %",
    [
        ("Leverage ratio total exposure measure ($'000)", {"FY2025": 1153889, "FY2024": 1493767, "FY2023": 1339718, "FY2022": 1436983, "FY2021": 1467315,
                                                           "FY2020": 2058837, "FY2019": 2327148, "FY2018": 2516920}),
        ("Leverage ratio (%)", {"FY2025": "47.48%", "FY2024": "33.77%", "FY2023": "35.41%", "FY2022": "31.75%", "FY2021": "30.75%",
                                "FY2020": "22.17%", "FY2019": "19.08%", "FY2018": "16.77%"}),
    ],
    p3_sources() + "\n\n" + p3_prekm1_sources(),
)

metric(
    "LCR", "$'000 / %",
    [
        ("Total high-quality liquid assets (HQLA), weighted value ($'000)", {"FY2025": 1374779, "FY2024": 328482, "FY2023": 384069, "FY2022": 288785, "FY2021": 351222}),
        ("Total net cash outflows, adjusted value ($'000)", {"FY2025": 956680, "FY2024": 187564, "FY2023": 136060, "FY2022": 168073, "FY2021": 71254}),
        ("Liquidity Coverage Ratio (%)", {"FY2025": "143.70%", "FY2024": "175.13%", "FY2023": "282.28%", "FY2022": "171.82%", "FY2021": "492.91%", "FY2020": "372%", "FY2019": "255%", "FY2018": "250%", "FY2017": "418%"}),
    ],
    p3_sources(),
    note="LCR figures are single month-end (31 December) spot observations as disclosed in the KM1 template, not a "
         "12-month trailing average. FY2017-2020 figures are as-stated percentages from the narrative risk section "
         "of each year's own Annual Report (no HQLA/net-cash-outflow £ breakdown is disclosed for those years, only "
         "the resulting ratio itself) - e.g. Annual Report 2017, p.14: 'the Bank had a Liquidity Coverage Ratio (LCR) "
         f"of 418%' — {AR17_URL}. CORROBORATED 2026-09-16: the FY2018, FY2019 and FY2020 standalone Pillar 3 "
         "Disclosures, located that day (see the Pillar 3 source note), independently state the same year-end "
         f"figures - 'At 31 December 2018, the LCR closed at 250%' ({P3_18_URL}), 255% for 2019 ({P3_19_URL}) and "
         f"372% for 2020 ({P3_20_URL}). Those editions also print a 'Table 25 - LCR Disclosure (12-month average)' "
         "with four quarterly columns, which is a DIFFERENT measure from the year-end spot figure shown here and has "
         "deliberately not been substituted for it. No LCR percentage of any kind is disclosed in the FY2014-2016 Annual Reports (those "
         "years' own narrative only describes the LCR/NSFR regime being newly implemented, without stating a ratio) "
         "- blank cells for FY2014-2016 are a genuine disclosure gap, not a missing transcription.",
)

metric(
    "NSFR", "$'000 / %",
    [
        ("Total available stable funding ($'000)", {"FY2025": 581574, "FY2024": 608924, "FY2023": 798010, "FY2022": 694607, "FY2021": 839389}),
        ("Total required stable funding ($'000)", {"FY2025": 335509, "FY2024": 407762, "FY2023": 477595, "FY2022": 511527, "FY2021": 558997}),
        ("Net Stable Funding Ratio (%)", {"FY2025": "173.34%", "FY2024": "149.33%", "FY2023": "167.09%", "FY2022": "135.79%", "FY2021": "150.16%"}),
    ],
    p3_sources(),
    note="FY2020 and earlier are blank because no NSFR figure of any kind is stated. This is now a positive "
         "finding rather than an inference: the FY2018, FY2019 and FY2020 standalone Pillar 3 Disclosures "
         "were located and read in full on 2026-09-16 (see the Pillar 3 source note for their URLs), and "
         "none of them states an NSFR - each describes the CRR II net stable funding requirement as one of "
         "the new disclosure requirements 'expected to be applicable from June 2021'. NSFR therefore first "
         "appears for this Bank in the FY2021 edition's UK KM1 table.",
)

bw.add_not_disclosed_metric_sheets(
    ["MREL Ratio"],
    p3_sources(note_disclosure_start=False) + "\nMREL is not referenced anywhere in ANY of the eight standalone "
    "Pillar 3 disclosure documents now located for this Bank (FY2018 through FY2025); ICBC (London) plc does not "
    "appear to be subject to a separate MREL requirement.",
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total Assets", {"FY2025": 2393946, "FY2024": 1702129, "FY2023": 1514720, "FY2022": 1538139, "FY2021": 1420688, "FY2020": 1997713, "FY2019": 2254083, "FY2018": 2374631, "FY2017": 2431239, "FY2016": 2722265, "FY2015": 3212625, "FY2014": 3825238}),
        ("Loans and advances to customers", {"FY2025": 413326, "FY2024": 336256, "FY2023": 429281, "FY2022": 331484, "FY2021": 128348, "FY2020": 428558, "FY2019": 513279, "FY2018": 809084, "FY2017": 953232, "FY2016": 1024525, "FY2015": 1347144, "FY2014": 2151215}),
        ("Customer accounts", {"FY2025": 160911, "FY2024": 165625, "FY2023": 244297, "FY2022": 247933, "FY2021": 530469, "FY2020": 386884, "FY2019": 395956, "FY2018": 467426, "FY2017": 375734, "FY2016": 391012, "FY2015": 661083, "FY2014": 860894}),
        ("Total Share Capital and Reserves", {"FY2025": 591416, "FY2024": 544650, "FY2023": 501030, "FY2022": 467879, "FY2021": 467598, "FY2020": 456485, "FY2019": 443933, "FY2018": 422437, "FY2017": 398400, "FY2016": 378047, "FY2015": 357275, "FY2014": 322451}),
    ],
    balance_sheet_unit="$'000",
    income_statement_totals=[
        ("Total operating income", {"FY2025": 68820, "FY2024": 65404, "FY2023": 43392, "FY2022": 25279, "FY2021": 23221, "FY2020": 26360, "FY2019": 34958, "FY2018": 42364, "FY2017": 39587, "FY2016": 61163, "FY2015": 70456, "FY2014": 69154}),
        ("Operating expenses", {"FY2025": -11513, "FY2024": -10875, "FY2023": -10005, "FY2022": -10609, "FY2021": -3425, "FY2020": -9570, "FY2019": -10040, "FY2018": -11219, "FY2017": -11427, "FY2016": -31300, "FY2015": -26622, "FY2014": -23918}),
        ("Profit for the financial year", {"FY2025": 42880, "FY2024": 39663, "FY2023": 26135, "FY2022": 11367, "FY2021": 15516, "FY2020": 10535, "FY2019": 18982, "FY2018": 25367, "FY2017": 21698, "FY2016": 20808, "FY2015": 34931, "FY2014": 23916}),
    ],
    income_statement_unit="$'000",
    equity_changes_totals=[
        ("Opening equity", {"FY2025": 544650, "FY2024": 501030, "FY2023": 467879, "FY2022": 467598, "FY2021": 456485, "FY2020": 443933, "FY2019": 422437, "FY2018": 398400, "FY2017": 378047, "FY2016": 357275, "FY2015": 322451, "FY2014": 296885}),
        ("Total comprehensive income for the year", {"FY2025": 46766, "FY2024": 43620, "FY2023": 33151, "FY2022": 281, "FY2021": 11113, "FY2020": 12552, "FY2019": 21496, "FY2018": 24201, "FY2017": 20353, "FY2016": 20772, "FY2015": 34824, "FY2014": 25566}),
        ("Closing equity", {"FY2025": 591416, "FY2024": 544650, "FY2023": 501030, "FY2022": 467879, "FY2021": 467598, "FY2020": 456485, "FY2019": 443933, "FY2018": 422437, "FY2017": 398400, "FY2016": 378047, "FY2015": 357275, "FY2014": 322451}),
    ],
    equity_changes_unit="$'000",
    cash_flow_totals=[
        ("Net cash used in operating activities", {"FY2025": 1366477, "FY2024": -174234, "FY2023": 129403, "FY2022": -108415, "FY2021": -51743, "FY2020": -117758, "FY2019": 353344, "FY2018": 76619, "FY2017": 78623, "FY2016": -7467, "FY2015": -145622, "FY2014": 73081}),
        ("Net cash used in investing activities", {"FY2025": -764, "FY2024": -447, "FY2023": -275, "FY2022": -525, "FY2021": -793, "FY2020": -386, "FY2019": 37751, "FY2018": -71973, "FY2017": -130118, "FY2016": 94561, "FY2015": 115276, "FY2014": -23711}),
        ("Net cash from financing activities", {"FY2025": 0, "FY2024": 0, "FY2023": 0, "FY2022": 0, "FY2021": 0, "FY2020": 0, "FY2019": 0, "FY2018": 0, "FY2017": 0, "FY2016": 0, "FY2015": 0, "FY2014": 0}),
        ("Cash and cash equivalents at 31 December", {"FY2025": 1498693, "FY2024": 139627, "FY2023": 316971, "FY2022": 180382, "FY2021": 307556, "FY2020": 361540, "FY2019": 470286, "FY2018": 78694, "FY2017": 71939, "FY2016": 126704, "FY2015": 41812, "FY2014": 73549}),
    ],
    cash_flow_unit="$'000",
    ratios=[
        ("CET1 Ratio", {"FY2025": "81.09%", "FY2024": "70.16%", "FY2023": "56.30%", "FY2022": "50.54%", "FY2021": "60.99%",
                        "FY2020": "44.60%", "FY2019": "38.72%", "FY2018": "26.84%", "FY2017": "22.17%"}),
        ("Tier 1 Ratio", {"FY2025": "81.09%", "FY2024": "70.16%", "FY2023": "56.30%", "FY2022": "50.54%", "FY2021": "60.99%",
                          "FY2020": "44.60%", "FY2019": "38.72%", "FY2018": "26.84%", "FY2017": "22.17%"}),
        ("Total Capital Ratio", {"FY2025": "81.09%", "FY2024": "70.16%", "FY2023": "56.30%", "FY2022": "50.54%", "FY2021": "60.99%",
                                 "FY2020": "44.60%", "FY2019": "38.72%", "FY2018": "32.97%", "FY2017": "27.87%"}),
        ("Leverage Ratio", {"FY2025": "47.48%", "FY2024": "33.77%", "FY2023": "35.41%", "FY2022": "31.75%", "FY2021": "30.75%",
                            "FY2020": "22.17%", "FY2019": "19.08%", "FY2018": "16.77%"}),
        ("LCR", {"FY2025": "143.70%", "FY2024": "175.13%", "FY2023": "282.28%", "FY2022": "171.82%", "FY2021": "492.91%", "FY2020": "372%", "FY2019": "255%", "FY2018": "250%", "FY2017": "418%"}),
        ("NSFR", {"FY2025": "173.34%", "FY2024": "149.33%", "FY2023": "167.09%", "FY2022": "135.79%", "FY2021": "150.16%"}),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own source "
         "citation for the underlying document/page. RWA-denominated Pillar 3 ratios (CET1/Tier1/Total Capital "
         "Ratio, Leverage Ratio) are publicly disclosed from FY2017 onward. Getting to that has taken two "
         "corrections, both from finding documents rather than from re-reading the ones we had: the 2026-09-12 "
         "disclosure audit located the FY2021 and FY2022 standalone Pillar 3 documents (superseding a claim that "
         "nothing before FY2023 was disclosed), and KM1-016 on 2026-09-16 located the FY2018, FY2019 and FY2020 "
         "editions (superseding a claim that no Pillar 3 document existed before FY2021 at all). All five sit on "
         "the Bank's own CDN, each misfiled one year forward - see the Pillar 3 source note. The FY2018-FY2020 "
         "editions do not use the UK KM1 template, which post-dates them, but they do disclose total risk "
         "weighted exposures, the three capital ratios and the leverage ratio in the Bank's own bespoke tables, "
         "and FY2017 comes from the FY2018 edition's comparative column. NSFR still begins at FY2021: none of the "
         "pre-KM1 editions states one. No risk-weighted-assets figure appears in the Bank's own FY2014-FY2020 "
         "ANNUAL REPORTS, which is why the CET1/Tier1/Total Capital $ amounts run back to FY2014 while the ratios "
         "stop at FY2017; blank cells for FY2014-FY2016 are intentional, not zeros, and mean no Pillar 3 edition "
         "for those years has been located. BASIS: the pre-KM1 (FY2017-FY2020) and KM1 (FY2021 onward) figures "
         "are not on the same capital basis - at 31 December 2020 the FY2020 edition reports 44.60% where the "
         "FY2021 edition's comparative reports 43.57% - and are deliberately not reconciled. LCR is the one ratio "
         "disclosed earlier still, as a narrative percentage from FY2017 (see the LCR sheet's own source note for "
         "FY2014-2016's absence).",
)

bw.save("/Users/armaan/code/katalysis/banks/ICBC (LONDON) PLC FINANCIALS.xlsx")
