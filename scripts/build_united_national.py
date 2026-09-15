import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

# Fiscal year-end 31 December. Extended FY2016-FY2025 (HD-027, 2026-09-06) -
# FY2016 is this entity's confirmed historical floor per HD-004 (own-domain
# Wayback signal), re-verified here against the actual Companies House
# filings and ubluk.com Pillar 3 archive rather than assumed from that scan.
YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021", "FY2020", "FY2019", "FY2018", "FY2017", "FY2016"]  # most recent first
YEAR_LABEL = {y: y for y in YEARS}

AR2025_URL = "https://find-and-update.company-information.service.gov.uk/company/04146820/filing-history/MzUxODk3MTQ2NWFkaXF6a2N4/document?format=pdf"
AR2023_URL = "https://find-and-update.company-information.service.gov.uk/company/04146820/filing-history/MzQyNTcyMzI0MGFkaXF6a2N4/document?format=pdf"
AR2022_URL = "https://find-and-update.company-information.service.gov.uk/company/04146820/filing-history/MzM3ODQxMzg4MWFkaXF6a2N4/document?format=pdf"
AR2021_URL = "https://find-and-update.company-information.service.gov.uk/company/04146820/filing-history/MzMzNzgyNzI3OGFkaXF6a2N4/document?format=pdf"
AR2020_URL = "https://find-and-update.company-information.service.gov.uk/company/04146820/filing-history/MzI5OTQ5NjA4NWFkaXF6a2N4/document?format=pdf"
AR2019_URL = "https://find-and-update.company-information.service.gov.uk/company/04146820/filing-history/MzI2NjczOTQyMmFkaXF6a2N4/document?format=pdf"
AR2018_URL = "https://find-and-update.company-information.service.gov.uk/company/04146820/filing-history/MzIzMjM1MjQ2N2FkaXF6a2N4/document?format=pdf"
AR2017_URL = "https://find-and-update.company-information.service.gov.uk/company/04146820/filing-history/MzIwMzc4OTY1M2FkaXF6a2N4/document?format=pdf"
AR2016_URL = "https://find-and-update.company-information.service.gov.uk/company/04146820/filing-history/MzE4MjAzNTU0NWFkaXF6a2N4/document?format=pdf"
P3_2023_URL = "https://www.ubluk.com/media/lupbssja/annual-report-unb-2023-pillar3-final-approved.pdf"
P3_2022_URL = "https://web.archive.org/web/20230923163742if_/https://www.ubluk.com/media/1368/ubl-2022-pillar-3-final-published.pdf"
# CORRECTION (2026-09-15). This used to point at
# https://www.ubluk.com/media/vsvfbmui/pillar260825.pdf , found by Wayback CDX and
# noted at the time as "not linked from the live site's own resources page". That
# turned out to be the reason: it is a PRE-FINAL DRAFT, not the published edition.
# Proof, not inference - that file still contains an unresolved internal reviewer
# query inside the CCR Mark to Market Method table, printed in the document body:
# "Interest rate contract (Why is this blank - we had IRS notional of 66.019 m?)".
# Its PDF creation date is 26 Aug 2025 (matching the "260825" in its filename).
# The URL below is the edition actually linked from the bank's own document index
# at https://www.ubluk.com/footer-pages/annual-reports/ , is titled "UNB 2024
# Pillar3", is dated 1 July 2026, and has that reviewer query removed (the row
# reads plain "Interest rate contract"). Every figure this workbook takes from the
# FY2024 edition is unchanged between the two - CET1/Tier 1 capital 97,948,100,
# Total capital 98,654,693, Total RWAs 493,153k and the Tier 2 collective
# provision 706,593 all appear identically in both - so this is a provenance fix,
# not a data restatement, and no FY2024 value moved.
P3_2024_URL = "https://www.ubluk.com/media/sr5puvji/unb-2024-pillar3-approved-finalplusamended.pdf"
P3_2024_SUPERSEDED_DRAFT_URL = "https://www.ubluk.com/media/vsvfbmui/pillar260825.pdf"
P3_2021_URL = "https://web.archive.org/web/20250726151714if_/https://www.ubluk.com/media/pqqda2ng/pillar-iii-disclosure-2021.pdf"
P3_2020_URL = "https://web.archive.org/web/20250803030355if_/https://www.ubluk.com/media/xq1lvuuj/pillar-iii-disclosure-2020.pdf"
P3_2019_URL = "https://web.archive.org/web/20250804025501if_/https://www.ubluk.com/media/sqgdszjz/pillar-iii-disclosure-2019.pdf"
P3_2018_URL = "https://web.archive.org/web/20250804031750if_/https://www.ubluk.com/media/5avboizc/pillar-iii-disclosure-2018.pdf"
P3_2017_URL = "https://web.archive.org/web/20250802155220if_/https://www.ubluk.com/media/o0bp44wd/pillar-iii-disclosure-2017.pdf"
P3_2016_URL = "https://web.archive.org/web/20250805064645if_/https://www.ubluk.com/media/sp5brt0v/pillar-iii-disclosure-2016.pdf"

ENTITY_NOTE = (
    "ENTITY NOTE: United National Bank Limited (Companies House 04146820) was formed in 2001 from the merger of the "
    "UK branches of two Pakistani banks, United Bank Limited ('UBL') and National Bank of Pakistan ('NBP'), who had "
    "operated in the UK since the 1960s - historically 55% UBL / 45% NBP owned, trading as 'UBL UK'. In July 2024, "
    "following regulatory approval, Bestway Group Financial Services Limited (a wholly-owned subsidiary of Bestway "
    "Group, a UK diversified conglomerate) acquired 95.1% of the Company's shares from UBL and NBP - the Company is "
    "now majority UK-owned rather than a foreign subsidiary in the usual sense, though UBL/NBP retain a residual "
    "stake and a preference-share arrangement (see Notes). All financial statements are prepared under FRS 102 in "
    "Pound Sterling (the Company's functional currency) - no cash-flow-statement exemption is taken.\n\n"
    "DATA AVAILABILITY NOTE: 10 years (FY2016-FY2025) sourced from nine Companies House annual report filings "
    "(FY2025/FY2024 from the 2025 filing, FY2023 from the 2023 filing, and FY2022 down to FY2016 each from that "
    "year's own filing rather than a later filing's restated comparative - all fully scanned/image-only PDFs, "
    "transcribed directly from the source page images; pdftotext extracts 0 real characters from every one of "
    "them, confirmed before transcription). Pillar 3: the pre-Bestway entity ('UBL UK') published 'Pillar 3 and "
    "Remuneration Code Disclosures' on its own site (ubluk.com) for every year FY2016-FY2024; the live site no "
    "longer links to most of these (only the current year's edition is navigable from ubluk.com/resources), but "
    "every year's PDF is still reachable at its original URL or via the Wayback Machine once located via a CDX "
    "search - FY2016 through FY2024 were all recovered this way (FY2016-FY2021 recovered/re-verified in the "
    "2026-09-06 extension: the first Wayback snapshot found for each of these 6 years' original media/NNNN URL "
    "was truncated at exactly 1,048,576 bytes (1 MiB), a known crawl-truncation artefact also seen on other banks' "
    "Wayback-recovered PDFs on this project - a second, later (2024-2025) snapshot of each document's newer "
    "media/<slug> URL was untruncated and used instead, confirmed via `file`/`pdftotext` page-count and "
    "character-count checks before transcribing any figure).\n\n"
    "FY2025 PILLAR 3 - ENUMERATED ABSENCE ON A CURRENT INDEX (upgraded from 'access gap' on 2026-09-15). The "
    "bank's own document index at https://www.ubluk.com/footer-pages/annual-reports/ was fetched and fully "
    "parsed on 15 September 2026. It is organised year by year, and each year from 2016 to 2024 carries BOTH an "
    "'Annual Report' link and a 'Pillar III Disclosure' link. The 2025 block carries the Annual Report "
    "(/media/405naqby/ye2025-statutory-accounts-final-23apr2026_signed.pdf) but NO Pillar III Disclosure link at "
    "all. That distinction matters: because the index has already been updated with the 2025 statutory accounts, "
    "this is not a stale page lagging behind publication - the page is current and the FY2025 Pillar 3 is absent "
    "from it. So the gap is an enumerated negative, not a failure to find.\n"
    "It is NOT, however, a permanent non-publication, and should stay on the re-check list. This bank publishes "
    "its Pillar 3 extremely late: the FY2024 edition linked from that same index is dated 1 July 2026, roughly 18 "
    "months after its year-end and over two months after the FY2025 Annual Report was signed (23 April 2026). On "
    "that cadence an FY2025 edition would not be due until well into 2027. The FY2025 Annual Report also still "
    "refers readers to 'the unaudited Pillar III disclosures' for capital management policy, so the bank has not "
    "said it has stopped publishing them.\n"
    "Nothing exists before FY2016 on any basis: the index's earliest year block is 2016, for both document types.\n"
    "Where a FY2025 figure appears on a sheet it is therefore Annual-Report-sourced and labelled as such."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are United National Bank Limited's own Statement of Cash Flows, exact £ as reported "
    "(not rounded to £'000/£m):\n"
    f"FY2025 & FY2024: Annual report and financial statements 2025, p.26 (Statement of cash flows) - {AR2025_URL}\n"
    f"FY2023 & FY2022 (as restated): Annual report and financial statements 2023, p.32 (Statement of cash flows) - "
    f"{AR2023_URL}\n"
    f"FY2021: Annual report and financial statements 2021, p.30 - {AR2021_URL}\n"
    f"FY2020: Annual report and financial statements 2020, p.28 - {AR2020_URL}\n"
    f"FY2019: Annual Report and Financial Statements 2019, p.29 - {AR2019_URL}\n"
    f"FY2018: Annual report and financial statements 2018, p.26 - {AR2018_URL}\n"
    f"FY2017: Annual report and financial statements 2017, p.26 - {AR2017_URL}\n"
    f"FY2016: Report and Financial Statements 2016, p.22 - {AR2016_URL}\n"
    "FY2023's own closing balance (£9,725,415) matches the FY2025 report's own FY2024 opening balance exactly, "
    "confirming consistency across the two source documents. FY2022 is labelled '(as restated)' in the FY2023 "
    "report; its own originally-published cash flow figures were not sourced separately here (unlike the new "
    "Balance Sheet / Profit & Loss / Statement of Changes in Equity / Asset Quality sheets added in this build, "
    "which do use FY2022's own originally-published figures throughout - see those sheets' own source notes for "
    "the ~£2.26m net-loans restatement this creates between FY2022's own Balance Sheet and the FY2023 report's "
    "restated FY2022 comparative). Every one of FY2016-FY2021's own closing cash balance ties exactly to the "
    "following year's own opening balance - a clean unbroken chain across all 6 filings.\n"
    "CASH FLOW PRESENTATION NOTE (FY2016-FY2021): the Company's own cash flow statement format (categorisation "
    "of adjustment/working-capital lines between Operating/Investing/Financing) genuinely changes across these "
    "filings - not a transcription artefact. 'Accretion of discounts and amortisation of premiums on debt "
    "securities' is classified within Operating activities in the FY2016 and FY2021 filings but within Investing "
    "activities in the FY2017-FY2020 filings (the FY2021 filing's own footnote confirms this: 'The statement of "
    "cash flows has been re-presented for 2020 to reflect a change applied in the year related to the "
    "presentation of debt securities' - so even FY2020's own re-presented comparative in the FY2021 filing differs "
    "from FY2020's own originally-published figures, which this workbook uses per project convention). This sheet "
    "keeps the 'Accretion...' row grouped under Investing (the majority classification) for all years for "
    "continuity; FY2016 and FY2021's own filings would place that year's figure under Operating instead. FY2016's "
    "'Change in derivative financial instruments' (asset-side and liability-side) and FY2017's equivalent lines "
    "are folded into 'Change in other operating assets'/'Change in other operating liabilities' respectively "
    "(both disclosed sub-lines, netted for continuity with the row set used in later years - not a fabricated "
    "figure). FY2020's own filing shows debt securities purchases/sales as one net '(Increase)/decrease in debt "
    "securities' line rather than separate purchase/sale lines (unlike every other year); that net figure is "
    "recorded in the 'Purchase of debt securities' row with 'Sale and maturity of debt securities' left blank "
    "that year only. FY2019's 'Gain on investment property disposal' and 'Proceeds on disposal of investment "
    "property' are genuinely investment-property-specific (not tangible fixed assets) but are recorded in the "
    "existing 'Fair value (gain)/loss on investment properties' and 'Proceeds from disposal of fixed assets' rows "
    "respectively for continuity with the row set used elsewhere.\n"
    "DISCREPANCY: FY2021's own filing does not self-foot exactly - operating (£(73,063,723)) + investing "
    "(£55,618,680) + financing (£(25,464)) = £(17,470,507), but the filing's own printed 'Net decrease in cash and "
    "cash equivalents' is £(17,472,507), a £2,000 gap. Reproduced exactly as printed, not force-tied.\n"
    "FY2016's own filing presents 'Effects of exchange rate changes on cash and cash equivalents' at the bottom "
    "of the statement purely as a compositional breakdown of the closing cash balance (Cash at bank and in hand "
    "£67,051,374 + Effects of exchange rate changes £8,328,960 = £75,380,334), not as an additional reconciling "
    "step after opening+net change (opening £36,182,195 + net change £39,198,139 already equals the closing "
    "£75,380,334 exactly on its own) - unlike every other year FY2017-FY2025, where that same row IS an additional "
    "reconciling step. The 'Effects of exchange rate changes on cash and cash equivalents (tail)' row is "
    "therefore left blank for FY2016 only, to avoid implying a double-counted reconciling relationship that "
    "isn't in the source.\n\n"
    + ENTITY_NOTE
)


def p3_sources():
    return (
        "Sources - United National Bank Limited (trading as 'UBL UK' at the time) Pillar 3 basis:\n"
        f"FY2023: UBL UK Pillar 3 and Remuneration Code Disclosures at 31 December 2023, various pages (Table LRSum/"
        f"LRCom p.47-48; Appendix VI Own funds disclosure p.61-63) - {P3_2023_URL}\n"
        f"FY2022: UBL UK Pillar 3 and Remuneration Code Disclosures at 31 December 2022, p.27 (Pillar 1 capital "
        f"requirements), p.48-49 (Leverage Ratio), p.22-23 (Own Funds) - {P3_2022_URL} (recovered via Wayback "
        f"Machine; the live ubluk.com URL for this document now 301-redirects to the site's generic resources page).\n"
        f"FY2024: UBL UK Pillar 3 and Remuneration Code Disclosures at 31 December 2024, p.26 (Pillar 1 capital "
        f"requirements), p.46-47 (Leverage Ratio), p.22 (Own Funds) - {P3_2024_URL} (the approved final edition, "
        f"linked from the bank's own index at https://www.ubluk.com/footer-pages/annual-reports/ and dated 1 July "
        f"2026). PROVENANCE CORRECTION 2026-09-15: an earlier build cited {P3_2024_SUPERSEDED_DRAFT_URL} instead, "
        f"recovered via Wayback CDX and flagged then as 'not linked from the live site's resources page'. That "
        f"file is a PRE-FINAL DRAFT - it still prints an unresolved internal reviewer query inside the CCR Mark "
        f"to Market Method table ('Interest rate contract (Why is this blank - we had IRS notional of 66.019 m?)') "
        f"and is dated 26 August 2025. Every FY2024 figure used in this workbook is byte-identical between the two "
        f"documents (CET1/Tier 1 capital 97,948,100; Total capital 98,654,693; Total RWAs 493,153k; Tier 2 "
        f"collective provision 706,593), so no value changed - only the citation.\n"
        f"FY2021: UBL UK Pillar 3 and Remuneration Code Disclosures at 31 December 2021, p.4 (Key metrics), p.21-22 "
        f"(Own Funds), p.25 (Pillar 1 capital requirements), p.46-48 (Leverage Ratio) - {P3_2021_URL}\n"
        f"FY2020: UBL UK Pillar 3 and Remuneration Code Disclosures at 31 December 2020, p.3 (Key metrics), p.21 "
        f"(Own Funds), p.25 (Pillar 1 capital requirements), p.45-46 (Leverage Ratio) - {P3_2020_URL}\n"
        f"FY2019: UBL UK Pillar 3 and Remuneration Code Disclosures at 31 December 2019, p.3 (Key metrics), p.20-21 "
        f"(Own Funds), p.24 (Pillar 1 capital requirements), p.45-46 (Leverage Ratio) - {P3_2019_URL}\n"
        f"FY2018: UBL UK Pillar 3 and Remuneration Code Disclosures at 31 December 2018, p.3 (Key metrics), p.20-21 "
        f"(Own Funds), p.25 (Pillar 1 capital requirements), p.45-46 (Leverage Ratio) - {P3_2018_URL}\n"
        f"FY2017: UBL UK Pillar 3 and Remuneration Code Disclosures at 31 December 2017, p.3 (Key metrics), p.20-21 "
        f"(Own Funds), p.25 (Pillar 1 capital requirements), p.45-46 (Leverage Ratio) - {P3_2017_URL}\n"
        f"FY2016: UBL UK Pillar 3 and Remuneration Code Disclosures at 31 December 2016, p.3 (Key metrics), p.20-21 "
        f"(Own Funds), p.25 (Pillar 1 capital requirements), p.45-46 (Leverage Ratio) - {P3_2016_URL}\n"
        f"FY2025: NO Pillar 3 edition is published. This is an enumerated absence, not a failed search - the "
        f"bank's own index (https://www.ubluk.com/footer-pages/annual-reports/, fetched and fully parsed 15 "
        f"September 2026) lists BOTH an Annual Report and a Pillar III Disclosure for every year 2016-2024, but "
        f"its 2025 block lists the Annual Report ONLY. The index is demonstrably current, since it already "
        f"carries the 2025 statutory accounts. Re-checkable rather than permanent: this bank publishes very late "
        f"(its FY2024 edition is dated 1 July 2026), so an FY2025 edition would not be due until well into 2027. "
        f"Where a FY2025 figure IS shown on a sheet, it is taken from the Annual report and financial "
        f"statements 2025 instead: p.5 (Key Performance Indicators table) for the Capital Adequacy Ratio and LCR, "
        f"p.13 (Capital resources table) for the Tier 1 / Total capital amounts - {AR2025_URL}\n"
        f"CET1/Tier 1/Total Capital ratios for FY2022 and FY2024 are computed here (capital ÷ Total RWAs, both "
        f"directly from the sources above) since neither document states the ratio as text, unlike FY2023's "
        f"document, which states its ratios directly; FY2016-FY2021 all state CET1/Tier1/Total Capital ratios "
        f"directly as text in each document's own 'Key metrics' summary box (p.3/p.4), so those are used as-is "
        f"rather than computed.\n"
        f"Tier 1 capital and Total capital £ amounts for FY2022-FY2025 cross-check exactly against each year's own "
        f"audited Annual Report 'Capital resources' note (see Cash Flow Statement sheet source note for URLs). "
        f"FY2016-FY2021 CET1/Tier1/Total Capital £ amounts are each year's own Appendix 'Own Funds' breakdown "
        f"table (exact £, not rounded) rather than that same document's own rounded 'Key metrics' summary box "
        f"figure (£m, 1 d.p.) - the two normally agree to the nearest £0.1m except FY2016, where the 'Key metrics' "
        f"box states CET1 capital/Tier 1 capital as £78.9m, matching that year's Total regulatory capital "
        f"(£78,876,144) rather than its own CET1/Tier 1 capital (£76,866,226, per the Own Funds table 2 pages "
        f"later) - a genuine source-document internal inconsistency in the FY2016 filing, reproduced here using "
        f"the Own Funds table's figure (consistent with every other year) rather than force-matched to the "
        f"summary box. Total RWAs for FY2016-FY2021 are each year's own Pillar 1 capital requirements table (same "
        f"convention as FY2022-2024); FY2016's table sums to £424,125,000, which is ~£10.2m below that same "
        f"document's own 'Key metrics' box figure of £434.3m - another instance of the same FY2016 box/detail-"
        f"table mismatch, again resolved in favour of the detailed table (used consistently with every other "
        f"year, and the only version with a category-level breakdown that ties to the RWA Breakdown sheet). "
        f"FY2016-FY2021 Leverage Ratio Tier 1 capital (Table LRCom row 20) matches that year's own CET1/Tier 1 "
        f"capital almost exactly in most years (FY2016: exact; FY2017: exact; FY2018: exact) but diverges in "
        f"FY2019 (£77,766k vs £77,324k), FY2020 (£75,844k vs £75,474k) and FY2021 (£76,227k vs £79,543k, the "
        f"largest gap) - the same kind of same-document capital-figure inconsistency already documented for "
        f"FY2024 below; reproduced exactly as each table states, not forced to tie."
    )


bw = BankWorkbook(bank_name="United National Bank Limited", years=YEARS, year_label=YEAR_LABEL, header_color="4A1E4D")

STATEMENTS_SOURCES = (
    "Sources - all figures are United National Bank Limited's own statements, exact £ as reported (not rounded to "
    "£'000/£m):\n"
    f"FY2025 & FY2024: Annual report and financial statements 2025 - p.22 (Statement of profit or loss), p.24 "
    f"(Balance sheet), p.25 (Statement of changes in equity), p.42-43 (Note 9, Loans and advances to customers) - "
    f"{AR2025_URL}\n"
    f"FY2023: Annual report and financial statements 2023 - p.28 (Statement of profit or loss), p.30 (Balance "
    f"sheet), p.31 (Statement of changes in equity), p.47 (Note 9, Loans and advances to customers) - {AR2023_URL}\n"
    f"FY2022 (own originally-published figures, not the FY2023 report's restated comparative): Full accounts made "
    f"up to 31 December 2022 (filed 10 May 2023) - p.27 (Statement of profit or loss), p.29 (Balance sheet), p.30 "
    f"(Statement of changes in equity), p.45 (Note 8, Loans and advances to customers) - {AR2022_URL}\n"
    f"FY2021: Annual report and financial statements 2021 - p.26 (Statement of profit or loss), p.28 (Balance "
    f"sheet), p.29 (Statement of changes in equity), p.43 (Note 8, Loans and advances to customers) - {AR2021_URL}\n"
    f"FY2020: Annual report and financial statements 2020 - p.24 (Statement of profit or loss), p.26 (Balance "
    f"sheet), p.27 (Statement of changes in equity), p.41 (Note 8, Loans and advances to customers) - {AR2020_URL}\n"
    f"FY2019: Annual Report and Financial Statements 2019 - p.25 (Statement of profit or loss), p.27 (Balance "
    f"sheet), p.28 (Statement of changes in equity), p.41 (Note 7, Loans and advances to customers) - {AR2019_URL}\n"
    f"FY2018: Annual report and financial statements 2018 - p.22 (Profit and loss account), p.24 (Balance sheet), "
    f"p.25 (Statement of changes in equity), p.38 (Note 7, Loans and advances to customers) - {AR2018_URL}\n"
    f"FY2017: Annual report and financial statements 2017 - p.22 (Profit and loss account), p.24 (Balance sheet), "
    f"p.25 (Statement of changes in equity), p.38 (Note 7, Loans and advances to customers) - {AR2017_URL}\n"
    f"FY2016: Report and Financial Statements 2016 - p.18 (Profit and loss account), p.20 (Balance Sheet), p.21 "
    f"(Statement of changes in equity), p.34 (Note 6, Loans and advances to customers) - {AR2016_URL}\n"
    "All 6 of FY2016-FY2021's own-filing figures were verified against pdftotext extracting effectively zero real "
    "characters from each PDF (scanned/image-only, same as every other year) before transcribing from the "
    "rendered page images.\n"
    "PRESENTATION NOTE: the Balance Sheet's own line items genuinely differ across FY2016-FY2021 filings (not a "
    "transcription gap): 'Loans and advances to banks' has no line at all in FY2016 (absent, not zero) and "
    "FY2019 (also absent that year), is an explicit disclosed nil in FY2018, and is a real balance in FY2017/"
    "FY2020/FY2021; 'Subordinated debt' is a real balance in FY2016/FY2017, an explicit disclosed nil in FY2018 "
    "(the subordinated loan was repaid in full on maturity in October 2018, per that year's own note), and no "
    "line at all thereafter; 'Repurchase agreements' is a real balance in FY2016-FY2019, an explicit disclosed nil "
    "in FY2020, and no line at all in FY2021; the combined 'Accruals and deferred income' line used in FY2016-"
    "FY2020 was split by FY2021 into a standalone 'Deferred income' line with no separate accruals line - shown "
    "here as two distinct rows rather than conflating a combined figure with a narrower later one.\n"
    "DISCREPANCY: FY2018's own SOCIE 'As at 1 January 2018' opening balance (£45,000,000 / £29,993,994 / "
    "£(1,654,351) / £10,822,966 / £84,162,609 total) does not exactly match FY2017's own SOCIE closing balance at "
    "31 December 2017 (£45,000,000 / £29,993,994 / £(1,654,351) / £10,472,966 / £83,812,609 total) - the Property "
    "revaluation reserve differs by £350,001 (£10,822,966 vs £10,472,966), a genuine restatement between the two "
    "filings' own figures for the same date. Both years' own SOCIE closing/opening rows are reproduced exactly as "
    "each filing states, not force-tied.\n"
    "DISCREPANCY: FY2022's own net loans figure (£638,315,902, tying to its own Balance Sheet and Note 8) differs "
    "from the FY2023 report's restated FY2022 comparative (£636,057,857) by ~£2.26m - a genuine restatement "
    "between the two filings. This workbook uses FY2022's own originally-published figures throughout, per project "
    "convention, so this Balance Sheet / Profit & Loss / Statement of Changes in Equity / Asset Quality sheet will "
    "not exactly match a later report's restated FY2022 comparative column.\n"
    "DISCREPANCY: the FY2025 Statement of Changes in Equity's own 31 December 2025 closing Total (£117,048,805) "
    "does not exactly match the FY2025 Balance Sheet's own Total equity for the same date (£117,048,800) - both "
    "figures are transcribed exactly as each statement states; this ~£5 gap is a source-document-internal rounding "
    "artefact, not a transcription error, and is not forced to tie.\n\n"
    + ENTITY_NOTE
)

BALANCE_SHEET_SOURCES = (
    STATEMENTS_SOURCES + "\n\n"
    "DEBT SECURITIES BREAKDOWN: the 'Debt securities - ...' sub-rows below the headline 'Total debt securities' "
    "line are transcribed from each year's own 'Financial instruments and risk management' note (categorising "
    "the balance by measurement basis - available for sale ('AFS') vs held to maturity ('HTM') - and, for "
    "FY2020/FY2021 only, by issuer sector as well):\n"
    f"FY2025: Note 25, p.52 (2025 table, 100% AFS - no FVPL/amortised-cost component for debt securities) - {AR2025_URL}\n"
    f"FY2024: same FY2025 filing's own FY2024 comparative column, Note 25, p.53 (100% AFS)\n"
    f"FY2023: Note 26, p.59 (2023 table, 100% AFS) - {AR2023_URL}\n"
    f"FY2022: Note 24, p.56 (2022 table, 100% AFS - this is the Company's own FY2022 filing, not the FY2023 "
    f"filing's restated comparative, per this workbook's own-year-filing convention) - {AR2022_URL}\n"
    f"FY2021 and FY2020: Note 24, p.58 ('Analysis of sector concentration' table - Central government / Financial "
    f"institutions / Corporates), both years' own columns disclosed side-by-side in the FY2021 filing - {AR2021_URL}. "
    f"FY2020's own filing (Note 25, p.49-50) confirms the same 100% AFS carrying value (£148,064,178) but does not "
    f"itself disclose the sector-concentration split - only the FY2021 filing's comparative column does.\n"
    f"FY2019: Note 23, p.53 (2019 table, 100% AFS), cross-checked against the FY2020 filing's own FY2019 "
    f"comparative (Note 25, p.50, same figure) - {AR2019_URL}\n"
    f"FY2018: Note 22, p.48 (2018 table - AFS/HTM/FVTPL/Loans&receivables category table with an HTM column "
    f"present but £Nil that year, i.e. already 100% AFS) - {AR2018_URL}\n"
    f"FY2017 and FY2016: Note 22, p.48 (both years' own AFS/HTM/FVTPL/Loans&receivables category table, stated "
    f"to the nearest £'000) - {AR2017_URL}\n\n"
    "Every year's sub-rows sum to that year's headline 'Total debt securities' line: exactly for FY2018-FY2025 "
    "(each sourced to the exact £ from its own category table) and to within £205 (FY2016) / £10 (FY2017) for the "
    "two years where the only available category table is stated at the nearest £'000 rather than the exact £ "
    "used in the primary statements - both genuine source-rounding gaps, not transcription errors, consistent "
    "with how £'000-only disclosures are already handled elsewhere in this workbook (see e.g. the Leverage Ratio "
    "sheet's FY2018 note).\n"
    "MEASUREMENT BASIS: 100% of the debt securities balance was classified as available for sale ('AFS' - the "
    "FRS 102/IAS 39 predecessor to the mark-to-market 'FVOCI' terminology used at most other banks in this "
    "project) in every year FY2018-FY2025; FY2016 and FY2017 alone also carried a held-to-maturity ('HTM', "
    "amortised-cost) component (£53.5m and £57.2m respectively) that had been fully run off/reclassified by "
    "FY2018. No fair-value-through-profit-or-loss ('FVTPL') debt securities were disclosed in any year (the "
    "'FVTPL' figures in each year's own category table relate only to derivatives, not debt securities).\n"
    "ISSUER TYPE: only the FY2021 filing's own 'Analysis of sector concentration' table splits debt securities by "
    "issuer sector (for both FY2021 and its FY2020 comparative) - no other year's filing (FY2016-FY2019, "
    "FY2022-FY2025) discloses an equivalent issuer-type/country breakdown of the debt securities balance, only "
    "the Fitch-rating breakdown reproduced in the entity note above; this is a genuine year-by-year disclosure "
    "gap in the Company's own filings, not an omission on this workbook's part."
)

# ---------------------------------------------------------------
# Sheet: Balance Sheet
# ---------------------------------------------------------------
balance_sheet_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and balances at banks", {"FY2025": 13278966, "FY2024": 8271317, "FY2023": 9725415, "FY2022": 6703512, "FY2021": 33695043, "FY2020": 51425237, "FY2019": 56401421, "FY2018": 41303910, "FY2017": 53211996, "FY2016": 75380334}),
    ("DATA", "Loans and advances to customers", {"FY2025": 1540326075, "FY2024": 1032354956, "FY2023": 718597663, "FY2022": 638315902, "FY2021": 505967194, "FY2020": 371849345, "FY2019": 283814684, "FY2018": 194150630, "FY2017": 224061810, "FY2016": 180722026}),
    ("DATA", "Loans and advances to banks", {"FY2025": 23388100, "FY2024": 22616365, "FY2023": 13576284, "FY2022": 2000329, "FY2021": 2253488, "FY2020": 570000, "FY2018": 0, "FY2017": 3500173}),
    ("DATA", "Derivative financial assets", {"FY2025": 245277, "FY2024": 331288, "FY2023": 632792, "FY2022": 3137104, "FY2021": 414198, "FY2020": 2819986, "FY2019": 3482846, "FY2018": 350369, "FY2017": 2868194, "FY2016": 930058}),
    ("DATA", "Total debt securities", {"FY2025": 297504303, "FY2024": 178309427, "FY2023": 138342935, "FY2022": 122536714, "FY2021": 92219766, "FY2020": 148064178, "FY2019": 137827144, "FY2018": 229966518, "FY2017": 207095990, "FY2016": 234153205}),
    ("DATA", "Debt securities - Available for sale (AFS)", {"FY2025": 297504303, "FY2024": 178309427, "FY2023": 138342935, "FY2022": 122536714, "FY2019": 137827144, "FY2018": 229966518, "FY2017": 149912000, "FY2016": 180624000}),
    ("DATA", "Debt securities - Held to maturity (HTM, amortised cost)", {"FY2017": 57184000, "FY2016": 53529000}),
    ("DATA", "Debt securities - Central government (government securities, available for sale)", {"FY2021": 25791136, "FY2020": 67124074}),
    ("DATA", "Debt securities - Financial institutions (available for sale)", {"FY2021": 54297596, "FY2020": 62870405}),
    ("DATA", "Debt securities - Corporates (available for sale)", {"FY2021": 12131034, "FY2020": 18069699}),
    ("DATA", "Prepayments and accrued income", {"FY2025": 1387861, "FY2024": 1002759, "FY2023": 1140078, "FY2022": 772017, "FY2021": 827884, "FY2020": 546073, "FY2019": 389754, "FY2018": 434839, "FY2017": 293327, "FY2016": 643737}),
    ("DATA", "Other assets", {"FY2025": 6369330, "FY2024": 8673325, "FY2023": 6382510, "FY2022": 1906588, "FY2021": 1503458, "FY2020": 2556378, "FY2019": 1826419, "FY2018": 3377080, "FY2017": 4856662, "FY2016": 3924840}),
    ("DATA", "Investment property", {"FY2025": 2900000, "FY2024": 2960000, "FY2023": 9604343, "FY2022": 9446895, "FY2021": 9446895, "FY2020": 8239267, "FY2019": 8187309, "FY2018": 8757309, "FY2017": 7970068, "FY2016": 7970068}),
    ("DATA", "Tangible fixed assets", {"FY2025": 29230135, "FY2024": 28954170, "FY2023": 21774348, "FY2022": 21122931, "FY2021": 21854142, "FY2020": 19453579, "FY2019": 18651189, "FY2018": 19160217, "FY2017": 17616883, "FY2016": 17881812}),
    ("DATA", "Intangible assets", {"FY2025": 2928124, "FY2024": 153494, "FY2023": 157144, "FY2022": 254630, "FY2021": 538802, "FY2020": 638479, "FY2019": 468847, "FY2018": 485176, "FY2017": 587124, "FY2016": 656451}),
    ("TOTAL", "Total assets", {"FY2025": 1917558171, "FY2024": 1283627101, "FY2023": 919933512, "FY2022": 806196622, "FY2021": 668720870, "FY2020": 606162522, "FY2019": 511049613, "FY2018": 497986048, "FY2017": 522062227, "FY2016": 522262531}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Derivative financial liabilities", {"FY2025": 4578229, "FY2024": 302453, "FY2023": 151115, "FY2022": 213652, "FY2021": 1699142, "FY2020": 267337, "FY2019": 75835, "FY2018": 1458058, "FY2017": 8672, "FY2016": 2801297}),
    ("DATA", "Provision for liabilities", {"FY2025": 9565009, "FY2024": 9788808, "FY2023": 7577361, "FY2022": 4881234, "FY2021": 5220425, "FY2020": 3921161, "FY2019": 3006943, "FY2018": 3181730, "FY2017": 3097429, "FY2016": 3908429}),
    ("DATA", "Other liabilities", {"FY2025": 5808142, "FY2024": 3011086, "FY2023": 3534309, "FY2022": 2711282, "FY2021": 3963156, "FY2020": 2928630, "FY2019": 2468305, "FY2018": 2957737, "FY2017": 4487164, "FY2016": 5984752}),
    ("DATA", "Deferred income", {"FY2022": 2299569, "FY2021": 2170663}),
    ("DATA", "Accruals and deferred income", {"FY2020": 2312541, "FY2019": 1627665, "FY2018": 1317518, "FY2017": 821209, "FY2016": 606853}),
    ("DATA", "Subordinated debt", {"FY2018": 0, "FY2017": 2014857, "FY2016": 2013009}),
    ("DATA", "Deposits by banks and credit unions", {"FY2025": 36695947, "FY2024": 19058682, "FY2023": 19917773, "FY2022": 21387884, "FY2021": 41317578, "FY2020": 14763891, "FY2019": 15720883, "FY2018": 5349870, "FY2017": 9638462, "FY2016": 12841595}),
    ("DATA", "Repurchase agreements", {"FY2023": 19284670, "FY2020": 0, "FY2019": 18259683, "FY2018": 10303788, "FY2017": 18343054, "FY2016": 10298714}),
    ("DATA", "Customer accounts", {"FY2025": 1743862044, "FY2024": 1146536321, "FY2023": 777311509, "FY2022": 700089790, "FY2021": 534268186, "FY2020": 505856479, "FY2019": 392097803, "FY2018": 402810377, "FY2017": 399838771, "FY2016": 404285205}),
    ("TOTAL", "Total liabilities", {"FY2025": 1800509371, "FY2024": 1178697350, "FY2023": 827776737, "FY2022": 731583411, "FY2021": 588639150, "FY2020": 530050039, "FY2019": 433257117, "FY2018": 427379078, "FY2017": 438249618, "FY2016": 442739854}),
    ("TOTAL", "Net assets", {"FY2025": 117048800, "FY2024": 104929751, "FY2023": 92156775, "FY2022": 74613211, "FY2021": 80081720, "FY2020": 76112483, "FY2019": 77792496, "FY2018": 70606970, "FY2017": 83812609, "FY2016": 79522677}),
    ("SECTION", "Equity", {}),
    ("DATA", "Called up share capital", {"FY2025": 45000000, "FY2024": 45000000, "FY2023": 45000000, "FY2022": 45000000, "FY2021": 45000000, "FY2020": 45000000, "FY2019": 45000000, "FY2018": 45000000, "FY2017": 45000000, "FY2016": 45000000}),
    ("DATA", "Property revaluation reserve", {"FY2025": 15764478, "FY2024": 15447589, "FY2023": 13672082, "FY2022": 13326168, "FY2021": 13646702, "FY2020": 12462475, "FY2019": 12561893, "FY2018": 12744491, "FY2017": 10472966, "FY2016": 10482684}),
    ("DATA", "Investment revaluation reserve", {"FY2025": -350290, "FY2024": -1348598, "FY2023": -4894285, "FY2022": -13936218, "FY2021": -3862585, "FY2020": -3102989, "FY2019": -4354181, "FY2018": -12272279, "FY2017": -1654351, "FY2016": -8274621}),
    ("DATA", "Profit and loss account", {"FY2025": 56634612, "FY2024": 45830760, "FY2023": 38378978, "FY2022": 30223261, "FY2021": 25297603, "FY2020": 21752997, "FY2019": 24584784, "FY2018": 25134758, "FY2017": 29993994, "FY2016": 32314614}),
    ("TOTAL", "Total equity", {"FY2025": 117048800, "FY2024": 104929751, "FY2023": 92156775, "FY2022": 74613211, "FY2021": 80081720, "FY2020": 76112483, "FY2019": 77792496, "FY2018": 70606970, "FY2017": 83812609, "FY2016": 79522677}),
]

bw.add_balance_sheet_sheet(
    title="United National Bank Limited — Balance Sheet",
    subtitle="Company basis, exact £ (not £'000/£m) - see source note at bottom.",
    rows=balance_sheet_rows,
    sources_text=BALANCE_SHEET_SOURCES,
    first_col_width=76,
    source_height=420,
    unit_suffix=" (£)",
)

# ---------------------------------------------------------------
# Sheet: Profit & Loss
# ---------------------------------------------------------------
income_statement_rows = [
    ("SECTION", "Interest income", {}),
    ("DATA", "Interest receivable from debt securities", {"FY2025": 12639358, "FY2024": 8810361, "FY2023": 6781043, "FY2022": 3402074, "FY2021": 1636909, "FY2020": 3137323, "FY2019": 5201026, "FY2018": 7974396, "FY2017": 8620957, "FY2016": 10087595}),
    ("DATA", "Interest receivable from group undertakings", {"FY2025": 129941, "FY2024": 366363, "FY2023": 471110, "FY2022": 85430, "FY2021": 82669, "FY2020": 222018, "FY2019": 347080, "FY2018": 236006, "FY2017": 237693, "FY2016": 65142}),
    ("DATA", "Other interest receivable and similar income", {"FY2025": 89261113, "FY2024": 54771776, "FY2023": 36417814, "FY2022": 26604318, "FY2021": 19462715, "FY2020": 14980696, "FY2019": 11365617, "FY2018": 11886359, "FY2017": 9972557, "FY2016": 9140372}),
    ("TOTAL", "Total interest receivable", {"FY2025": 102030412, "FY2024": 63948500, "FY2023": 43669967, "FY2022": 30091822, "FY2021": 21182293, "FY2020": 18340037, "FY2019": 16913723, "FY2018": 20096761, "FY2017": 18831207, "FY2016": 19293109}),
    ("SECTION", "Interest expense", {}),
    ("DATA", "Interest payable to group undertakings", {"FY2025": -36039, "FY2024": -53937, "FY2023": -291812, "FY2022": -108360, "FY2020": -27460, "FY2019": -48801, "FY2018": -312180, "FY2017": -830698, "FY2016": -558126}),
    ("DATA", "Interest payable", {"FY2025": -70542609, "FY2024": -39858637, "FY2023": -22302031, "FY2022": -11235244, "FY2021": -7648141, "FY2020": -8740927, "FY2019": -9202679, "FY2018": -10822647, "FY2017": -9850892, "FY2016": -9715587}),
    ("TOTAL", "Total interest payable", {"FY2025": -70578648, "FY2024": -39912574, "FY2023": -22593843, "FY2022": -11343604, "FY2021": -7648141, "FY2020": -8768387, "FY2019": -9251480, "FY2018": -11134827, "FY2017": -10681590, "FY2016": -10273713}),
    ("TOTAL", "Net interest income", {"FY2025": 31451764, "FY2024": 24035926, "FY2023": 21076124, "FY2022": 18748218, "FY2021": 13534152, "FY2020": 9571650, "FY2019": 7662243, "FY2018": 8961934, "FY2017": 8149617, "FY2016": 9019396}),
    ("SECTION", "Non-interest income", {}),
    ("DATA", "Fees and commissions receivable", {"FY2025": 465923, "FY2024": 574808, "FY2023": 531356, "FY2022": 463844, "FY2021": 364505, "FY2020": 759979, "FY2019": 925317, "FY2018": 1536106, "FY2017": 2334474, "FY2016": 3475840}),
    ("DATA", "Profit from foreign exchange", {"FY2025": 380059, "FY2024": 270867, "FY2023": 623278, "FY2022": 720867, "FY2021": 695012, "FY2020": 775519, "FY2019": 708265, "FY2018": 970269, "FY2017": -8672, "FY2016": -2084527}),
    ("DATA", "Fair value loss on investment properties", {"FY2025": -60000, "FY2024": -1692678, "FY2021": 1207628, "FY2020": 51958, "FY2018": 787241}),
    ("DATA", "Profit/(loss) on realised debt securities", {"FY2025": 255520, "FY2024": -759855, "FY2023": 139910, "FY2022": 344705, "FY2021": 221247, "FY2020": 956817, "FY2019": 1089460, "FY2018": -704103, "FY2017": 5358117, "FY2016": 5043480}),
    ("DATA", "Other operating income", {"FY2025": 90942, "FY2024": 776648, "FY2023": 366513, "FY2022": 139404, "FY2021": 34028, "FY2020": 149007, "FY2019": 243870, "FY2018": 317882, "FY2017": 291796, "FY2016": 346832}),
    ("DATA", "Profit on disposal of fixed assets", {"FY2024": 46958, "FY2022": 372270}),
    ("DATA", "Gain on investment property disposal", {"FY2019": 208884}),
    ("DATA", "Fair value gains/(losses) on derivatives", {"FY2025": -36260, "FY2024": -8502, "FY2023": -206509, "FY2022": 3635562, "FY2017": 1650504, "FY2016": 3744814}),
    ("TOTAL", "Total income", {"FY2025": 32547948, "FY2024": 23244172, "FY2023": 22530672, "FY2022": 24424870, "FY2021": 16056572, "FY2020": 12264930, "FY2019": 10838039, "FY2018": 11869329, "FY2017": 17775836, "FY2016": 19545835}),
    ("SECTION", "Operating expenses", {}),
    ("DATA", "Administrative expenses", {"FY2025": -16827131, "FY2024": -14816212, "FY2023": -12549595, "FY2022": -12752766, "FY2021": -12688136, "FY2020": -11839897, "FY2019": -11671393, "FY2018": -12302513, "FY2017": -11642444, "FY2016": -10854031}),
    ("DATA", "Remeasurement of financial liability", {"FY2025": -291571, "FY2024": -2561700, "FY2023": -2650000}),
    ("DATA", "Depreciation and amortisation", {"FY2025": -297373, "FY2024": -344925, "FY2023": -597021, "FY2022": -755530, "FY2021": -721946, "FY2020": -540113, "FY2019": -699285, "FY2018": -912170, "FY2017": -890889, "FY2016": -883599}),
    # Not itself a printed AR subtotal - the sum of Administrative expenses +
    # Depreciation and amortisation above. Excludes the financial-liability
    # remeasurement, impairment (losses)/recoveries, and other debt recoveries
    # per standard cost-to-income convention (operating costs only, not
    # credit risk or fair-value items).
    ("TOTAL", "Total operating expenses (sum of Administrative expenses + Depreciation and amortisation - excludes financial liability remeasurement, impairment (losses)/recoveries, and other debt recoveries)",
     {"FY2025": -17124504, "FY2024": -15161137, "FY2023": -13146616, "FY2022": -13508296, "FY2021": -13410082, "FY2020": -12380010, "FY2019": -12370678, "FY2018": -13214683, "FY2017": -12533333, "FY2016": -11737630}),
    ("DATA", "Impairment (losses)/recoveries", {"FY2025": -555015, "FY2024": -277396, "FY2023": 177172, "FY2022": -5620263, "FY2021": 579196, "FY2020": -2263480, "FY2019": 523476, "FY2018": -2651807, "FY2017": -4798824, "FY2016": -557756}),
    ("DATA", "Other debt recoveries", {"FY2018": 218430, "FY2017": 267203, "FY2016": 150000}),
    ("TOTAL", "Profit before tax on ordinary activities", {"FY2025": 14576858, "FY2024": 5243939, "FY2023": 6911228, "FY2022": 5296311, "FY2021": 3225686, "FY2020": -2378560, "FY2019": -1009163, "FY2018": -3778731, "FY2017": 710882, "FY2016": 7400449}),
    ("DATA", "Income tax (expense)/credit", {"FY2025": -3731753, "FY2024": 1894527, "FY2023": 1689239, "FY2022": -754543, "FY2021": -307680, "FY2020": 183161, "FY2019": 293640, "FY2018": -1283194, "FY2017": -1539350, "FY2016": -3003823}),
    ("TOTAL", "Profit for the year", {"FY2025": 10845105, "FY2024": 7138466, "FY2023": 8600467, "FY2022": 4541768, "FY2021": 2918006, "FY2020": -2195399, "FY2019": -715523, "FY2018": -5061925, "FY2017": -828468, "FY2016": 4396626}),
]

bw.add_income_statement_sheet(
    title="United National Bank Limited — Profit & Loss",
    subtitle="Company basis, exact £ (not £'000/£m) - see source note at bottom.",
    rows=income_statement_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=76,
    source_height=280,
    unit_suffix=" (£)",
)

# ---------------------------------------------------------------
# Sheet: Statement of Changes in Equity
# ---------------------------------------------------------------
equity_headers = ["Called up share capital", "Profit and Loss Account", "Investment revaluation reserve", "Property Revaluation reserve", "Total"]
equity_rows = [
    ("TOTAL", "Balance at 1 January 2016", (45000000, 30972630, -10864062, 9974209, 75082777)),
    ("DATA", "Profit for the year", (None, 4396626, None, None, 4396626)),
    ("DATA", "Actuarial loss recognised relating to the pension scheme", (None, -682000, None, None, -682000)),
    ("DATA", "Movement on deferred tax relating to pension liability", (None, 117640, None, None, 117640)),
    ("DATA", "Fair value movement on available for sale investment", (None, None, 3234823, None, 3234823)),
    ("DATA", "Current tax related to available for sale debt securities", (None, None, -645382, None, -645382)),
    ("DATA", "Deferred tax adjustment due to rate reduction", (None, None, None, 518193, 518193)),
    ("DATA", "Dividend paid", (None, -2500000, None, None, -2500000)),
    ("TOTAL", "Total", (45000000, 32304896, -8274621, 10492402, 79522677)),
    ("DATA", "Transfer of depreciation on revaluation surplus", (None, 9718, None, -9718, 0)),
    ("TOTAL", "Balance as at 31 December 2016", (45000000, 32314614, -8274621, 10482684, 79522677)),
    ("TOTAL", "Balance at 1 January 2017", (45000000, 32314614, -8274621, 10482684, 79522677)),
    ("DATA", "(Loss) for the year", (None, -828468, None, None, -828468)),
    ("DATA", "Actuarial gain recognised relating to the pension scheme", (None, 836000, None, None, 836000)),
    ("DATA", "Movement on deferred tax relating to pension liability", (None, -137870, None, None, -137870)),
    ("DATA", "Fair value movement on available for sale investments", (None, None, 5636046, None, 5636046)),
    ("DATA", "Tax related to available for sale investment", (None, None, 984224, None, 984224)),
    ("DATA", "Dividend paid", (None, -2200000, None, None, -2200000)),
    ("TOTAL", "Total", (45000000, 29984276, -1654351, 10482684, 83812609)),
    ("DATA", "Transfer of depreciation on revaluation surplus", (None, 9718, None, -9718, 0)),
    ("TOTAL", "Balance as at 31 December 2017", (45000000, 29993994, -1654351, 10472966, 83812609)),
    ("TOTAL", "Balance at 1 January 2018", (45000000, 29993994, -1654351, 10822966, 84162609)),
    ("DATA", "Loss for the year", (None, -5061925, None, None, -5061925)),
    ("DATA", "Actuarial gain recognised relating to the pension scheme", (None, 221000, None, None, 221000)),
    ("DATA", "Movement on deferred tax relating to pension liability", (None, -27370, None, None, -27370)),
    ("DATA", "Fair value movement on available for sale investment", (None, None, -10279086, None, -10279086)),
    ("DATA", "Current tax related to available for sale debt securities", (None, None, -338842, None, -338842)),
    ("DATA", "Revaluation gain on freehold property", (None, None, None, 1915014, 1915014)),
    ("DATA", "Movement on deferred tax relating to freehold property", (None, None, None, -325552, -325552)),
    ("DATA", "Deferred tax adjustment due to change in calculation basis", (None, None, None, 341122, 341122)),
    ("TOTAL", "Total", (45000000, 25125699, -12272279, 12753550, 70606970)),
    ("DATA", "Transfer of depreciation on revaluation surplus", (None, 9059, None, -9059, 0)),
    ("TOTAL", "Balance as at 31 December 2018", (45000000, 25134758, -12272279, 12744491, 70606970)),
    ("TOTAL", "Balance as at 1 January 2019", (45000000, 25134759, -12272279, 12744490, 70606970)),
    ("DATA", "Loss for the year", (None, -715523, None, None, -715523)),
    ("DATA", "Actuarial loss recognised relating to the pension scheme", (None, -225000, None, None, -225000)),
    ("DATA", "Fair value movement on available for sale investment", (None, None, 7918098, None, 7918098)),
    ("DATA", "Revaluation gain on freehold property", (None, None, None, 72167, 72167)),
    ("DATA", "Movement on deferred tax relating to freehold property", (None, None, None, 11931, 11931)),
    ("DATA", "Recycling of revaluation related to investment property disposal", (None, 381724, None, -381724, 0)),
    ("DATA", "Deferred tax adjustment", (None, None, None, 123853, 123853)),
    ("TOTAL", "Total", (45000000, 24575960, -4354181, 12570717, 77792496)),
    ("DATA", "Transfer of depreciation on revaluation surplus", (None, 8824, None, -8824, 0)),
    ("TOTAL", "Balance as at 31 December 2019", (45000000, 24584784, -4354181, 12561893, 77792496)),
    ("TOTAL", "Balance as at 1 January 2020", (45000000, 24584784, -4354181, 12561893, 77792496)),
    ("DATA", "Loss for the year", (None, -2195399, None, None, -2195399)),
    ("DATA", "Actuarial loss recognised relating to the pension scheme", (None, -646000, None, None, -646000)),
    ("DATA", "Fair value movement on available for sale investment", (None, None, 1251192, None, 1251192)),
    ("DATA", "Revaluation gain on freehold property", (None, None, None, 242804, 242804)),
    ("DATA", "Movement on deferred tax relating to freehold property", (None, None, None, -46131, -46131)),
    ("DATA", "Deferred tax adjustment due to change in tax rates", (None, None, None, -286479, -286479)),
    ("TOTAL", "Total", (45000000, 21743385, -3102989, 12472087, 76112483)),
    ("DATA", "Transfer of depreciation on revaluation surplus", (None, 9612, None, -9612, 0)),
    ("TOTAL", "Balance as at 31 December 2020", (45000000, 21752997, -3102989, 12462475, 76112483)),
    ("TOTAL", "Balance as at 1 January 2021", (45000000, 21752997, -3102989, 12462475, 76112483)),
    ("DATA", "Profit for the year", (None, 2918006, None, None, 2918006)),
    ("DATA", "Actuarial gain recognised relating to the pension scheme", (None, 617000, None, None, 617000)),
    ("DATA", "Fair value movement on available for sale investment", (None, None, -759595, None, -759595)),
    ("DATA", "Revaluation gain on freehold property", (None, None, None, 2757109, 2757109)),
    ("DATA", "Movement on deferred tax relating to freehold property", (None, None, None, -523851, -523851)),
    ("DATA", "Deferred tax adjustment due to change in tax rates", (None, None, None, -1039431, -1039431)),
    ("TOTAL", "Total", (45000000, 25288003, -3862585, 13656302, 80081720)),
    ("DATA", "Transfer of depreciation on revaluation surplus", (None, 9600, None, -9600, 0)),
    ("TOTAL", "Balance at 1 January 2022", (45000000, 25297603, -3862585, 13646702, 80081720)),
    ("DATA", "Profit for the year", (None, 4541768, None, None, 4541768)),
    ("DATA", "Actuarial gain recognised relating to the pension scheme", (None, 889850, None, None, 889850)),
    ("DATA", "Fair value loss on available for sale debt securities", (None, None, -10073633, None, -10073633)),
    ("DATA", "Gain on revaluation of freehold property", (None, None, None, 98316, 98316)),
    ("DATA", "Deferred tax relating to revaluation of freehold property", (None, None, None, 90190, 90190)),
    ("DATA", "Release of revaluation reserve on disposal of property", (None, 499440, None, -499440, 0)),
    ("DATA", "Dividend paid and declared", (None, -1015000, None, None, -1015000)),
    ("TOTAL", "Total", (45000000, 30213661, -13936218, 13335768, 74613211)),
    ("DATA", "Transfer of depreciation on revaluation surplus", (None, 9600, None, -9600, 0)),
    ("TOTAL", "Balance as at 31 December 2022", (45000000, 30223261, -13936218, 13326168, 74613211)),
    ("TOTAL", "Balance as at 1 January 2023", (45000000, 30223261, -13936218, 13326168, 74613211)),
    ("DATA", "Profit for the year", (None, 8600467, None, None, 8600467)),
    ("DATA", "Actuarial loss recognised relating to the pension scheme", (None, -454350, None, None, -454350)),
    ("DATA", "Fair value gain on available for sale debt securities", (None, None, 7410504, None, 7410504)),
    ("DATA", "Deferred tax related to available for sale debt securities", (None, None, 1631429, None, 1631429)),
    ("DATA", "Gain on revaluation of freehold property", (None, None, None, 440867, 440867)),
    ("DATA", "Deferred tax relating to revaluation of freehold property", (None, None, None, -85353, -85353)),
    ("TOTAL", "Total", (45000000, 38369378, -4894285, 13681682, 92156775)),
    ("DATA", "Transfer of depreciation on revaluation surplus", (None, 9600, None, -9600, 0)),
    ("TOTAL", "Balance as at 31 December 2023", (45000000, 38378978, -4894285, 13672082, 92156775)),
    ("TOTAL", "Balance as at 1 January 2024", (45000000, 38378978, -4894285, 13672082, 92156775)),
    ("DATA", "Profit for the year", (None, 7138466, None, None, 7138466)),
    ("DATA", "Actuarial gain recognised relating to the pension scheme", (None, 185250, None, None, 185250)),
    ("DATA", "Fair value movement on available for sale debt securities", (None, None, 4727584, None, 4727584)),
    ("DATA", "Deferred tax related to available for sale debt securities", (None, None, -1181897, None, -1181897)),
    ("DATA", "Gain on revaluation of freehold property", (None, None, None, 2514243, 2514243)),
    ("DATA", "Deferred tax relating to revaluation of freehold property", (None, None, None, -610670, -610670)),
    ("DATA", "Transfer of depreciation on disposal of property", (None, 118466, None, -118466, 0)),
    ("TOTAL", "Total", (45000000, 45821160, -1348598, 15457189, 104929751)),
    ("DATA", "Transfer of depreciation on revaluation surplus", (None, 9600, None, -9600, 0)),
    ("TOTAL", "Balance as at 31 December 2024", (45000000, 45830760, -1348598, 15447589, 104929751)),
    ("TOTAL", "Balance as at 1 January 2025", (45000000, 45830760, -1348598, 15447589, 104929751)),
    ("DATA", "Profit for the year", (None, 10845105, None, None, 10845105)),
    ("DATA", "Actuarial (loss) recognised relating to the pension scheme", (None, -41250, None, None, -41250)),
    ("DATA", "Fair value gain on available for sale debt securities", (None, None, 1331077, None, 1331077)),
    ("DATA", "Deferred tax related to available for sale debt securities", (None, None, -332769, None, -332769)),
    ("DATA", "Gain on revaluation of freehold property", (None, None, None, 394391, 394391)),
    ("DATA", "Deferred tax relating to revaluation of freehold property", (None, None, None, -77500, -77500)),
    ("TOTAL", "Balance as at 31 December 2025", (45000000, 56634615, -350290, 15764480, 117048805)),
]

bw.add_equity_changes_sheet(
    title="United National Bank Limited — Statement of Changes in Equity",
    subtitle="Company basis, exact £ (not £'000/£m), chronological (oldest to newest) - see source note at bottom.",
    headers=equity_headers,
    rows=equity_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=58,
    source_height=280,
)

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Profit before tax on ordinary activities for the year", {"FY2025": 14576858, "FY2024": 5243939, "FY2023": 6911228, "FY2022": 5296311, "FY2021": 3225686, "FY2020": -2378560, "FY2019": -1009163, "FY2018": -3778731, "FY2017": 710882, "FY2016": 7400449}),
    ("DATA", "Depreciation and amortisation", {"FY2025": 297373, "FY2024": 344925, "FY2023": 597021, "FY2022": 755530, "FY2021": 721946, "FY2020": 540113, "FY2019": 699285, "FY2018": 912170, "FY2017": 890889, "FY2016": 883599}),
    ("DATA", "Remeasurement of financial liability", {"FY2025": 291571, "FY2024": 2561700, "FY2023": 2650000}),
    ("DATA", "Net (reversal)/charge in respect of defined benefit pension scheme", {"FY2025": 36000, "FY2024": 35000, "FY2023": -54000, "FY2022": 3000, "FY2021": 11000, "FY2020": 6000, "FY2019": -5000, "FY2018": 60000, "FY2017": 25000, "FY2016": 10000}),
    ("DATA", "Impairment charge/(recoveries) on loans and advances and other items", {"FY2025": 555015, "FY2024": 277396, "FY2023": -133448, "FY2022": -190335, "FY2021": -579196, "FY2020": 2263480, "FY2019": -523476, "FY2018": 2433377, "FY2017": 4531621, "FY2016": 407757}),
    ("DATA", "Impairment (recoveries)/charge on available for sale investments", {"FY2023": -43724, "FY2022": 5081559}),
    ("DATA", "Non-cash movements relating to AFS debt securities", {"FY2025": 1798841, "FY2024": 518237, "FY2023": -38664, "FY2022": 472140}),
    ("DATA", "Fair value (gain)/loss on investment properties", {"FY2025": 60000, "FY2024": 1692678, "FY2023": -157448, "FY2021": -1207628, "FY2020": -51958, "FY2018": -787241}),
    ("DATA", "Fair value losses on derivatives", {"FY2025": 36260, "FY2024": 8502}),
    ("DATA", "Disposal of fixed assets - non cash", {"FY2024": -46958, "FY2022": -950000}),
    ("DATA", "Interest payable on preference shares", {"FY2018": 233674, "FY2017": 777910, "FY2016": 479110}),
    ("DATA", "Accretion of discounts and amortisation of premiums (Operating activities in the FY2016/FY2021 filings only - see source note)", {"FY2021": -797587, "FY2016": -7681412}),
    ("DATA", "Effects of exchange rate changes on cash and cash equivalents (within adjustments)", {"FY2025": 78789, "FY2024": 203350, "FY2023": -1040191, "FY2022": 1310294, "FY2021": 257687, "FY2020": 1171331, "FY2019": 144285, "FY2018": -1244042, "FY2017": -198765, "FY2016": -8328960}),
    ("DATA", "Change in loans to banks", {"FY2025": -771732, "FY2024": -9040080, "FY2023": -11575956, "FY2022": 253159, "FY2021": -1683487, "FY2020": -570000, "FY2018": 3500173, "FY2017": -3500173}),
    ("DATA", "Change in loans and advances", {"FY2025": -508526134, "FY2024": -314034689, "FY2023": -82406357, "FY2022": -129900329, "FY2021": -133538654, "FY2020": -88045665, "FY2019": -89140578, "FY2018": 27477802, "FY2017": -47871405, "FY2016": 5932316}),
    ("DATA", "Change in other operating assets", {"FY2025": 1574513, "FY2024": -4401232, "FY2023": -2726540, "FY2022": -1703767, "FY2021": 3793897, "FY2020": -1019407, "FY2019": -1386364, "FY2018": 3855839, "FY2017": -2519548, "FY2016": 773709}),
    ("DATA", "Change in deposits from banks and customers", {"FY2025": 614962983, "FY2024": 368365721, "FY2023": 75751608, "FY2022": 145891909, "FY2021": 54965395, "FY2020": 112801684, "FY2019": -341561, "FY2018": -1316986, "FY2017": -7649567, "FY2016": 55213062}),
    ("DATA", "Change in other operating liabilities", {"FY2025": 4362320, "FY2024": 3532520, "FY2023": 4913759, "FY2022": -5203335, "FY2021": 1767218, "FY2020": 2120938, "FY2019": -1489551, "FY2018": -187962, "FY2017": -5740969, "FY2016": -3877343}),
    ("DATA", "Corporate income tax paid", {"FY2025": -1630000, "FY2024": -1440000, "FY2023": -907009, "FY2022": -563132}),
    ("TOTAL", "Net cash from/(used in) operating activities", {"FY2025": 127702657, "FY2024": 53821009, "FY2023": -8259721, "FY2022": 20553004, "FY2021": -73063723, "FY2020": 26837956, "FY2019": -93052123, "FY2018": 31158073, "FY2017": -60544125, "FY2016": 51212287}),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Purchase of tangible fixed and intangible assets", {"FY2025": -2953578, "FY2024": -246091, "FY2023": -710084, "FY2022": -216696, "FY2021": -265723, "FY2020": -1119343, "FY2019": -383843, "FY2018": -438486, "FY2017": -556633, "FY2016": -907238}),
    ("DATA", "Proceeds from disposal of fixed assets", {"FY2024": 237859, "FY2022": 950000, "FY2019": 910603}),
    ("DATA", "Accretion of discounts and amortisation of premiums (Investing activities in the FY2017-FY2019 filings - see source note; FY2020's own filing shows a single net debt-securities line instead, see 'Purchase of debt securities' row)", {"FY2019": 423383454, "FY2018": 388733635, "FY2017": 172967224}),
    ("DATA", "Gain on investment property disposal", {"FY2019": -208884}),
    ("DATA", "Purchase of debt securities", {"FY2025": -1051570428, "FY2024": -750228210, "FY2023": -595299208, "FY2022": -572112956, "FY2021": -291404230, "FY2020": -11238317, "FY2019": -1417859464, "FY2018": -2050650514, "FY2017": -3130458713, "FY2016": -197319973}),
    ("DATA", "Sale and maturity of debt securities", {"FY2025": 931907787, "FY2024": 714471065, "FY2023": 586985878, "FY2022": 526168675, "FY2021": 347286633, "FY2019": 1094533482, "FY2018": 1628428423, "FY2017": 2991168974, "FY2016": 180548002}),
    ("TOTAL", "Net cash from/(used in) investing activities", {"FY2025": -122616219, "FY2024": -35765377, "FY2023": -9023414, "FY2022": -45210977, "FY2021": 55618680, "FY2020": -12357660, "FY2019": 100375348, "FY2018": -33926942, "FY2017": 33120852, "FY2016": -17679209}),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Repayment of obligations under finance lease", {"FY2024": -21710, "FY2023": -19823, "FY2022": -8263, "FY2021": -25464, "FY2020": -25466, "FY2019": -37324, "FY2018": -22954, "FY2017": -12108, "FY2016": -12107}),
    ("DATA", "Proceeds from/(repayment of) repurchase agreements", {"FY2024": -19284670, "FY2023": 19284670, "FY2020": -18259683, "FY2019": 7955895, "FY2018": -8039266, "FY2017": 8044340, "FY2016": 10298714}),
    ("DATA", "Payment to preference shareholders", {"FY2018": -306182, "FY2017": -777910, "FY2016": -2118294}),
    ("DATA", "Net increase/(decrease) in subordinated debt", {"FY2018": -2014857, "FY2017": 1848, "FY2016": -3252}),
    ("DATA", "Dividends paid", {"FY2022": -1015000, "FY2017": -2200000, "FY2016": -2500000}),
    ("TOTAL", "Net cash from/(used in) financing activities", {"FY2024": -19306380, "FY2023": 19264847, "FY2022": -1023263, "FY2021": -25464, "FY2020": -18285149, "FY2019": 7918571, "FY2018": -10383259, "FY2017": 5056170, "FY2016": 5665061}),
    ("TOTAL", "Net increase/(decrease) in cash and cash equivalents", {"FY2025": 5086438, "FY2024": -1250748, "FY2023": 1981712, "FY2022": -25681236, "FY2021": -17472507, "FY2020": -3804853, "FY2019": 15241796, "FY2018": -13152128, "FY2017": -22367103, "FY2016": 39198139}),
    ("DATA", "Cash and cash equivalents at the beginning of the financial year", {"FY2025": 8271317, "FY2024": 9725415, "FY2023": 6703512, "FY2022": 33695042, "FY2021": 51425237, "FY2020": 56401421, "FY2019": 41303910, "FY2018": 53211996, "FY2017": 75380334, "FY2016": 36182195}),
    ("DATA", "Effects of exchange rate changes on cash and cash equivalents (tail)", {"FY2025": -78789, "FY2024": -203350, "FY2023": 1040191, "FY2022": -1310294, "FY2021": -257687, "FY2020": -1171331, "FY2019": -144285, "FY2018": 1244042, "FY2017": 198765}),
    ("TOTAL", "Cash and cash equivalents at the end of the financial year", {"FY2025": 13278966, "FY2024": 8271317, "FY2023": 9725415, "FY2022": 6703512, "FY2021": 33695043, "FY2020": 51425237, "FY2019": 56401421, "FY2018": 41303910, "FY2017": 53211996, "FY2016": 75380334}),
]

bw.add_cash_flow_sheet(
    title="United National Bank Limited — Cash Flow Statement",
    subtitle="Company basis, exact £ (not £'000/£m) - see source note at bottom.",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=76,
    source_height=260,
    unit_suffix=" (£)",
)

# ---------------------------------------------------------------
# Sheet: Asset Quality
# ---------------------------------------------------------------
asset_quality_rows = [
    ("SECTION", "Loans and advances to customers by impairment status (FRS 102 basis - not IFRS 9 stage 1/2/3)", {}),
    ("DATA", "Impaired loans", {"FY2025": 8563357, "FY2024": 7627387, "FY2023": 14038077, "FY2022": 8027926, "FY2021": 12673647, "FY2020": 7475832, "FY2019": 4162605, "FY2018": 2701236, "FY2017": 9519038, "FY2016": 10410395}),
    ("DATA", "Non-impaired loans", {"FY2025": 1533904725, "FY2024": 1028820429, "FY2023": 707202735, "FY2022": 631590077, "FY2021": 494785983, "FY2020": 365853745, "FY2019": 281564926, "FY2018": 193884712, "FY2017": 224499328, "FY2016": 176436113}),
    ("TOTAL", "Gross loans and advances to customers", {"FY2025": 1542468082, "FY2024": 1036447816, "FY2023": 721240812, "FY2022": 639618003, "FY2021": 507459630, "FY2020": 373329577, "FY2019": 285727531, "FY2018": 196585948, "FY2017": 234018366, "FY2016": 186846508}),
    ("DATA", "Unamortised portion of loan fees", {"FY2025": -5320210, "FY2024": -3331731, "FY2023": -2198275}),
    ("DATA", "Collective provision", {"FY2025": -1261608, "FY2024": -706593, "FY2023": -444874, "FY2022": -368530, "FY2021": -411884, "FY2020": -192412, "FY2019": -575883, "FY2018": -854078, "FY2017": -1634905, "FY2016": -1276069}),
    ("DATA", "Specific impairment allowance on impaired loans", {"FY2022": -933571, "FY2021": -1080552, "FY2020": -1287820, "FY2019": -1336964, "FY2018": -1581240, "FY2017": -8321651, "FY2016": -4848413}),
    ("DATA", "Fair value of hedged risk", {"FY2025": 4439811, "FY2024": -54536}),
    ("TOTAL", "Net loans and advances to customers", {"FY2025": 1540326075, "FY2024": 1032354956, "FY2023": 718597663, "FY2022": 638315902, "FY2021": 505967194, "FY2020": 371849345, "FY2019": 283814684, "FY2018": 194150630, "FY2017": 224061810, "FY2016": 180722026}),
    ("SECTION", "Asset quality ratios", {}),
    ("DATA", "Impaired loans as % of gross loans", {"FY2025": "0.56%", "FY2024": "0.74%", "FY2023": "1.95%", "FY2022": "1.26%", "FY2021": "2.50%", "FY2020": "2.00%", "FY2019": "1.46%", "FY2018": "1.37%", "FY2017": "4.07%", "FY2016": "5.57%"}),
    ("DATA", "Total provisions as % of gross loans", {"FY2025": "0.08%", "FY2024": "0.07%", "FY2023": "0.06%", "FY2022": "2.04%", "FY2021": "0.29%", "FY2020": "0.40%", "FY2019": "0.67%", "FY2018": "1.24%", "FY2017": "4.25%", "FY2016": "3.28%"}),
]

bw.add_asset_quality_sheet(
    title="United National Bank Limited — Asset Quality",
    subtitle="Company basis, exact £ (not £'000/£m) - see source note at bottom.",
    rows=asset_quality_rows,
    sources_text=STATEMENTS_SOURCES + (
        "\n\nACCOUNTING BASIS NOTE: the Company reports under FRS 102 (not IFRS 9), so its own loan-book disclosure "
        "categorises loans as 'Impaired'/'Non-Impaired' with 'Specific'/'Collective' provisions, rather than the "
        "IFRS 9 stage-1/2/3 staging used by most other banks in this project - this sheet reproduces the Company's "
        "own categories rather than forcing an IFRS 9 shape onto FRS 102 data. FY2022's collective provision "
        "(£368,530) plus specific impairment allowance (£933,571) together give total provisions of £1,302,101 "
        "against gross loans of £639,618,003 (2.04%) - materially higher than other years because FY2022 carried a "
        "specific impairment allowance against impaired loans (later years show £Nil specific allowance, impaired "
        "loans covered entirely by collective provision and/or expected recovery).\n"
        "TERMINOLOGY NOTE: FY2016-FY2018's own filings use 'Non-performing'/'Performing' loans as the category "
        "labels (not 'Impaired'/'Non-Impaired', which only appears from FY2019 onward) - the same underlying "
        "concept (loans overdue/individually provisioned vs not), shown here under the later terminology for row "
        "continuity across all years rather than adding a third label pair. FY2016-FY2020's 'Specific impairment "
        "allowance on impaired loans' figure is each year's own Note 6/7/8 'Impairment losses on loans and "
        "advances' balance (occasionally net of amounts written off in the same note, e.g. FY2020); FY2016-FY2020 "
        "carry no separate 'Unamortised portion of loan fees' or 'Fair value of hedged risk' line (both first "
        "appear later) - gross less the two provision rows ties to net loans exactly in every one of these years."
    ),
    first_col_width=68,
    source_height=340,
    unit_suffix=" (£)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, f"Company basis, {unit}" if unit else "Company basis",
                         rows_data, sources_text, note=note, first_col_width=48, source_height=150)


metric(
    "CET1 Capital", "£",
    [("Common Equity Tier 1 (CET1) capital", {
        "FY2025": 108644570, "FY2024": 97948100, "FY2023": 88559510, "FY2022": 73598731,
        "FY2021": 79542918, "FY2020": 75474004, "FY2019": 77323649, "FY2018": 70121794,
        "FY2017": 81564327, "FY2016": 74666226,
    })],
    p3_sources(),
    note="Equal to Tier 1 capital in every year - the Company has no Additional Tier 1 (AT1) instruments. FY2023's "
         "figure is confirmed to the nearest £'000 by the Pillar 3 document's own Appendix VI (£88,559k). "
         "FY2016-FY2021 are each year's own Own Funds Disclosure table (Appendix), consistent with FY2022-FY2024's "
         "sourcing - not the rounded £m figure in that year's own front-page Key Metrics box, which for FY2016 in "
         "particular differs materially (£78.9m) from this table's £74.7m; see the Total RWAs/RWA Breakdown sheet "
         "notes for the related FY2016 RWA inconsistency.",
)

metric(
    "CET1 Ratio", "% of RWA",
    [("Common Equity Tier 1 (CET1) ratio", {
        "FY2023": "21.46%", "FY2022": "19.08%", "FY2024": "19.86%", "FY2025": "Not disclosed",
        "FY2021": "22.2%", "FY2020": "23.9%", "FY2019": "21.4%", "FY2018": "21.1%",
        "FY2017": "18.6%", "FY2016": "17.6%",
    })],
    p3_sources(),
    note="FY2023 is directly stated in that year's Pillar 3 document (equal to its stated Tier 1 ratio, since "
         "CET1=Tier 1 capital exactly that year). FY2022 and FY2024 are computed here (CET1 capital ÷ Total RWAs, "
         "both from that year's own Pillar 3 document - see Total RWAs sheet) since neither document states the "
         "ratio as text. FY2025: no Pillar 3 edition is published - an ENUMERATED absence, since the bank's own index lists a Pillar III Disclosure for every year 2016-2024 but only an Annual Report for 2025, and that index is current (it already carries the 2025 statutory accounts). Re-checkable, not permanent: this bank publishes very late (FY2024's edition is dated 1 July 2026). "
         "FY2016-FY2021 are each stated directly as text in that year's own front-page Key Metrics box (unlike "
         "FY2022/FY2024, which are computed) - reproduced as stated even though the same document's detailed Table "
         "CC1 shows a different (in FY2021's case, implausibly halved: 11% vs this 22.2%) percentage in its row 61; "
         "the Key Metrics box figure is used throughout FY2016-FY2021 for consistency and because it is the "
         "document's own headline disclosure.",
)

metric(
    "Tier 1 Capital", "£",
    [("Tier 1 capital", {
        "FY2025": 108644570, "FY2024": 97948100, "FY2023": 88559510, "FY2022": 73598731,
        "FY2021": 79542918, "FY2020": 75474004, "FY2019": 77323649, "FY2018": 70121794,
        "FY2017": 81564327, "FY2016": 74666226,
    })],
    p3_sources(),
)

metric(
    "Tier 1 Ratio", "% of RWA",
    [("Tier 1 ratio", {
        "FY2023": "21.46%", "FY2022": "19.08%", "FY2024": "19.86%", "FY2025": "Not disclosed",
        "FY2021": "22.2%", "FY2020": "23.9%", "FY2019": "21.4%", "FY2018": "21.1%",
        "FY2017": "18.6%", "FY2016": "17.6%",
    })],
    p3_sources(),
    note="Equal to the CET1 Ratio in every year - the Company has no Additional Tier 1 (AT1) instruments. FY2023 is "
         "directly stated in that year's Pillar 3 document (Table CC1, row 62); FY2022/FY2024 computed (see CET1 "
         "Ratio sheet note); FY2025 not disclosed (no Pillar 3 edition is published - enumerated absence on the bank's own current index); FY2016-FY2021 stated directly "
         "in that year's own Key Metrics box (see CET1 Ratio sheet note re the FY2021 Table CC1 discrepancy).",
)

metric(
    "Total Capital", "£",
    [("Total capital", {
        "FY2025": 109906178, "FY2024": 98654693, "FY2023": 89004384, "FY2022": 73967261,
        "FY2021": 79954802, "FY2020": 75666416, "FY2019": 77899532, "FY2018": 70975872,
        "FY2017": 83532099, "FY2016": 76676144,
    })],
    p3_sources(),
    note="Tier 1 capital plus a Tier 2 collective provision figure disclosed in each year's own Annual Report. "
         "FY2016-FY2021 from each year's own Own Funds Disclosure table (Appendix), consistent with FY2022-FY2024.",
)

metric(
    "Total Capital Ratio", "% of RWA",
    [("Total capital ratio", {
        "FY2023": "21.56%", "FY2022": "19.18%", "FY2024": "20.00%", "FY2025": "16.3%",
        "FY2021": "22.3%", "FY2020": "24%", "FY2019": "21.6%", "FY2018": "21.4%",
        "FY2017": "19.0%", "FY2016": "18.3%",
    })],
    p3_sources(),
    note="FY2023 directly stated in that year's Pillar 3 document (Table CC1, row 63). FY2022/FY2024 computed "
         "(Total capital ÷ Total RWAs, both from that year's own Pillar 3 document). FY2016-FY2021 stated directly "
         "in that year's own Key Metrics box (see "
         "CET1 Ratio sheet note re the FY2021 Table CC1 discrepancy, which is also present in this ratio: 11.1% vs "
         "22.3%). "
         "BASIS CAVEAT - FY2025 (16.3%) is the ONLY year here taken from the Annual Report rather than a Pillar 3 "
         "document: no FY2025 Pillar 3 edition is published (enumerated absence on the bank's own current index), but the FY2025 Annual Report's own KPI table (p.5, 'Capital "
         "Adequacy Ratio = Total Capital / risk-weighted assets') states it directly. That table is NOT on the same "
         "basis as the Pillar 3-derived years above it - it restates FY2024 as 18.8%, against the 20.00% computed "
         "here from the FY2024 Pillar 3's own Total capital and Total RWAs. The two sources disagree by ~120bps on "
         "the same year, so FY2025 is not strictly comparable with FY2016-FY2024 in this row. Retained because it "
         "is a genuine, directly-stated disclosure; revisit and restate onto the Pillar 3 basis once the FY2025 "
         "Pillar 3 is published - which on this bank's demonstrated cadence (its FY2024 edition is dated 1 July 2026, some 18 months after that year-end) would not be before well into 2027.",
)

metric(
    "Total RWAs", "£",
    [("Total risk-weighted exposure amount", {
        "FY2023": 412732000, "FY2022": 385707000, "FY2024": 493153000, "FY2025": "Not disclosed",
        "FY2021": 342987000, "FY2020": 316139000, "FY2019": 361460000, "FY2018": 331832000,
        "FY2017": 438970000, "FY2016": 434265000,
    })],
    p3_sources(),
    note="Each year's own Pillar 1 Capital Requirement table (Credit & Counterparty Credit Risk + Market Risk + "
         "CVA Risk + Operational Risk RWAs, summed) - see the RWA Breakdown sheet for the category-level split. "
         "FY2025: no Pillar 3 edition is published - an ENUMERATED absence, since the bank's own index lists a Pillar III Disclosure for every year 2016-2024 but only an Annual Report for 2025, and that index is current (it already carries the 2025 statutory accounts). Re-checkable, not permanent: this bank publishes very late (FY2024's edition is dated 1 July 2026). FY2016's "
         "figure here (£434,265,000, Table CC1 row 60 / Key Metrics box) does NOT equal the FY2016 Pillar 1 table's "
         "own category sum (£424,125,000) - a genuine ~£10.1m internal inconsistency in that year's own document, "
         "reproduced as stated rather than forced to tie (see RWA Breakdown sheet note); FY2017-FY2021 all sum "
         "exactly (to the nearest £1,000 rounding) to their category-level breakdown.",
)

rwa_breakdown_rows = [
    ("SECTION", "RWA by risk category (Pillar 1 Minimum Capital Requirement)", {}),
    ("DATA", "Credit and Counterparty Credit Risk (Standardised)", {
        "FY2023": 382394000, "FY2022": 363317000, "FY2024": 456897000,
        "FY2021": 322069000, "FY2020": 294787000, "FY2019": 336098000, "FY2018": 304923000,
        "FY2017": 410796000, "FY2016": 397610000,
    }),
    ("DATA", "Market Risk (Position Risk Requirement)", {
        "FY2023": 1222000, "FY2022": 0, "FY2024": 0,
        "FY2021": 0, "FY2020": 0, "FY2019": 0, "FY2018": 0, "FY2017": 0, "FY2016": 0,
    }),
    ("DATA", "Credit Valuation Adjustment Risk (Simplified Method)", {
        "FY2023": 161000, "FY2022": 250000, "FY2024": 311000,
        "FY2021": 522000, "FY2020": 262000, "FY2019": 1171000, "FY2018": 411000,
        "FY2017": 931000, "FY2016": 1033000,
    }),
    ("DATA", "Operational Risk (Basic Indicator Approach)", {
        "FY2023": 28955000, "FY2022": 22140000, "FY2024": 35945000,
        "FY2021": 20396000, "FY2020": 21090000, "FY2019": 24191000, "FY2018": 26497000,
        "FY2017": 27243000, "FY2016": 25482000,
    }),
    ("TOTAL", "Total risk-weighted exposure amount", {
        "FY2023": 412732000, "FY2022": 385707000, "FY2024": 493153000, "FY2025": "Not disclosed",
        "FY2021": 342987000, "FY2020": 316139000, "FY2019": 361460000, "FY2018": 331832000,
        "FY2017": 438970000, "FY2016": 434265000,
    }),
]

bw.add_rwa_breakdown_sheet(
    title="United National Bank Limited — RWA Breakdown",
    subtitle="Company basis, exact £ (not £'000/£m) - see source note at bottom.",
    rows=rwa_breakdown_rows,
    sources_text=p3_sources() + (
        "\n\nEach year's category-level RWAs are its own Pillar 1 Capital Requirement table (same table cited on "
        "the Total RWAs sheet). FY2017-FY2024 all sum exactly (to the nearest £1,000 rounding) to that year's Total "
        "RWAs row above. FY2016 is a genuine exception: the Pillar 1 table's own category-level figures here "
        "(Credit £397,610,000 + Market £0 + CVA £1,033,000 + Operational £25,482,000 = £424,125,000, per that "
        "table's own 'Pillar 1 Capital Resources Requirement' line) do not sum to the £434,265,000 Total RWAs "
        "figure used on the Total RWAs sheet (from Table CC1 row 60 / the Key Metrics box) - both figures are each "
        "exactly as stated in the FY2016 document's own two tables, reproduced without forcing a tie. FY2025: no "
        "Pillar 3 edition is published - an enumerated absence on the bank's own current index, re-checkable given its very late publication cadence (FY2024's edition is dated 1 July 2026)."
    ),
    first_col_width=58,
    source_height=180,
    unit_suffix=" (£)",
)

metric(
    "Leverage Ratio", "£ / %",
    [
        ("Leverage ratio total exposure measure", {
            "FY2023": 954151000, "FY2022": 815698000, "FY2024": 1310997000,
            "FY2021": 694808000, "FY2020": 604467000, "FY2019": 501223000, "FY2018": 502571597,
            "FY2017": 515832000, "FY2016": 533423000,
        }),
        ("Tier 1 capital used in leverage ratio calculation", {
            "FY2022": 73599000, "FY2024": 93996000,
            "FY2021": 76227000, "FY2020": 75844000, "FY2019": 77766000, "FY2018": 70122000,
            "FY2017": 81564000, "FY2016": 76866000,
        }),
        ("Leverage ratio (%)", {
            "FY2023": "8.52%", "FY2022": "8.43%", "FY2024": "7.17%", "FY2025": "Not disclosed",
            "FY2021": "10.97%", "FY2020": "12.55%", "FY2019": "15.51%", "FY2018": "13.95%",
            "FY2017": "15.8%", "FY2016": "14.4%",
        }),
    ],
    p3_sources(),
    note="FY2022 and FY2024 now fully evidenced by each year's own Pillar 3 document (Table LRSum/LRCom), not just "
         "the narrative comparator this workbook previously relied on for FY2022. DISCREPANCY: FY2024's Pillar 3 "
         "leverage-ratio Tier 1 capital (£93,996,000, Table LRCom row 20) is ~£3.95m lower than the CET1/Tier 1 "
         "capital figure used elsewhere in this workbook for FY2024 (£97,948,100, per that same document's own "
         "Appendix VI Own Funds disclosure) - both figures are reproduced exactly as each table states, not forced "
         "to tie; the FY2022 document shows no such gap (£73,599,000 vs £73,598,731, a rounding-only difference). "
         "FY2025 not disclosed (no Pillar 3 edition is published - enumerated absence on the bank's own current index; see entity note on the Cash Flow Statement sheet). "
         "FY2016-FY2021's Table LRCom Tier 1 capital also diverges from the CET1/Tier 1 Capital sheet figure in "
         "every one of these years (by amounts ranging from a rounding-only ~£300 in FY2017/FY2018 up to ~£3.3m in "
         "FY2021) - each year's Table LRCom is its own distinct disclosure from the Own Funds Disclosure table and "
         "both are reproduced exactly as stated, not reconciled. FY2018's total exposure measure is given to the "
         "exact £ in that year's own Table LRSum (£502,571,597), unlike other years which state it only to the "
         "nearest £'000 (multiplied by 1,000 here).",
)

metric(
    "LCR", "%",
    [("Liquidity Coverage Ratio (%) (Annual Report KPI basis)", {
        "FY2025": "196.0%", "FY2024": "199.8%",
    })],
    p3_sources()
    + "\nFY2025/FY2024 LCR SOURCE (added 2026-09-15): United National Bank Limited, Annual Report and "
      "Financial Statements for the year ended 31 December 2025, Strategic Report, \"Key Performance "
      "Indicators ('KPI')\" table, p.5 - the row labelled \"LCR / Liquidity Coverage Ratio\", which prints "
      "196.0% for 2025 against 199.8% for 2024. Retrieved from the Bank's own annual-reports page "
      "(https://www.ubluk.com/footer-pages/annual-reports/, document "
      "/media/405naqby/ye2025-statutory-accounts-final-23apr2026_signed.pdf).\n",
    note="CORRECTION (2026-09-15): this sheet previously stated that no LCR figure was disclosed in any year. "
         "That was wrong for FY2025 and FY2024 - the FY2025 Annual Report introduces an LCR row in its Key "
         "Performance Indicators table, giving 196.0% with a 199.8% comparative.\n\n"
         "BASIS CAVEAT - THIS IS NOT A PILLAR 3 LCR, and it is labelled accordingly. Every other liquidity or "
         "capital figure on this workbook's Pillar-3-sourced sheets comes from the Bank's own Pillar 3 "
         "documents, which do NOT disclose a numeric LCR in any year: the FY2024 Pillar 3 discusses the LCR "
         "and the NSFR only in narrative terms (\"the principal measure used by the Bank for managing "
         "liquidity risk is the Liquidity Coverage Ratio\"; \"the Bank is also required to report the Net "
         "Stable Funding Ratio... monitored on a daily basis\") and prints no figure for either. The KPI "
         "table gives no definition beyond the metric name, so whether it is a year-end point-in-time ratio "
         "or a 12-month average is not stated. Treat these two values as an Annual-Report KPI series in their "
         "own right, not as the start of a Pillar 3 LCR series.\n\n"
         "RELATED BASIS EVIDENCE: the same KPI table reports the Capital Adequacy Ratio as 16.3% (2025) and "
         "18.8% (2024), where the FY2024 Pillar 3 gives 20.00% for FY2024 - a ~120bp disagreement between the "
         "Bank's own two documents for the same year-end. That is the clearest demonstration that the AR-KPI "
         "and Pillar 3 bases are genuinely different for this bank, and why these LCR values are kept on a "
         "distinctly labelled row.\n\n"
         "FY2016-FY2023 remain blank: no LCR figure, numeric or tabular, appears in any of those years' "
         "Pillar 3 documents, and the FY2021-FY2024 Annual Reports were each searched in full (real text "
         "layers) with zero occurrences of \"LCR\" or \"liquidity coverage ratio\" - the KPI row is new in the "
         "FY2025 report.",
)

bw.add_not_disclosed_metric_sheets(
    ["NSFR"], p3_sources(),
    per_note={"NSFR": "No numeric NSFR is disclosed in any year. Re-verified 2026-09-15 against the FY2024 "
                      "Pillar 3 document and the FY2021-FY2025 Annual Reports: the FY2024 Pillar 3 refers to "
                      "the NSFR only in narrative terms (\"the Bank is also required to report the Net Stable "
                      "Funding Ratio (NSFR), and to ensure that the ratio remains above 100%. The NSFR "
                      "position is monitored on a daily basis\") without ever printing the ratio, and no "
                      "Annual Report carries an NSFR figure. Note the FY2025 Annual Report DID introduce an "
                      "LCR row into its KPI table (see the LCR sheet) but added no NSFR row alongside it. "
                      "Nothing has been derived."})

metric(
    "MREL Ratio", None,
    [("MREL ratio", {y: "Not disclosed" for y in YEARS})],
    p3_sources(),
    note="No numeric or qualitative MREL disclosure of any kind was found for this bank in any year reviewed.",
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {"FY2025": 1917558171, "FY2024": 1283627101, "FY2023": 919933512, "FY2022": 806196622, "FY2021": 668720870, "FY2020": 606162522, "FY2019": 511049613, "FY2018": 497986048, "FY2017": 522062227, "FY2016": 522262531}),
        ("Loans and advances to customers", {"FY2025": 1540326075, "FY2024": 1032354956, "FY2023": 718597663, "FY2022": 638315902, "FY2021": 505967194, "FY2020": 371849345, "FY2019": 283814684, "FY2018": 194150630, "FY2017": 224061810, "FY2016": 180722026}),
        ("Customer accounts", {"FY2025": 1743862044, "FY2024": 1146536321, "FY2023": 777311509, "FY2022": 700089790, "FY2021": 534268186, "FY2020": 505856479, "FY2019": 392097803, "FY2018": 402810377, "FY2017": 399838771, "FY2016": 404285205}),
        ("Total equity", {"FY2025": 117048800, "FY2024": 104929751, "FY2023": 92156775, "FY2022": 74613211, "FY2021": 80081720, "FY2020": 76112483, "FY2019": 77792496, "FY2018": 70606970, "FY2017": 83812609, "FY2016": 79522677}),
    ],
    balance_sheet_unit="£",
    income_statement_totals=[
        ("Net interest income", {"FY2025": 31451764, "FY2024": 24035926, "FY2023": 21076124, "FY2022": 18748218, "FY2021": 13534152, "FY2020": 9571650, "FY2019": 7662243, "FY2018": 8961934, "FY2017": 8149617, "FY2016": 9019396}),
        ("Total income", {"FY2025": 32547948, "FY2024": 23244172, "FY2023": 22530672, "FY2022": 24424870, "FY2021": 16056572, "FY2020": 12264930, "FY2019": 10838039, "FY2018": 11869329, "FY2017": 17775836, "FY2016": 19545835}),
        ("Profit for the year", {"FY2025": 10845105, "FY2024": 7138466, "FY2023": 8600467, "FY2022": 4541768, "FY2021": 2918006, "FY2020": -2195399, "FY2019": -715523, "FY2018": -5061925, "FY2017": -828468, "FY2016": 4396626}),
    ],
    income_statement_unit="£",
    equity_changes_totals=[
        ("Opening equity", {"FY2025": 104929751, "FY2024": 92156775, "FY2023": 74613211, "FY2022": 80081720, "FY2021": 76112483, "FY2020": 77792496, "FY2019": 70606970, "FY2018": 84162609, "FY2017": 79522677, "FY2016": 75082777}),
        ("Total comprehensive income for the year", {"FY2025": 12119054, "FY2024": 12772976, "FY2023": 17543564, "FY2022": -4453509, "FY2021": 3969238, "FY2020": -1680013, "FY2019": 7185526, "FY2018": -13555639, "FY2017": 6489932, "FY2016": 6939900}),
        ("Other equity movements, net", {"FY2025": 0, "FY2024": 0, "FY2023": 0, "FY2022": -1015000, "FY2021": 0, "FY2020": 0, "FY2019": 0, "FY2018": 0, "FY2017": -2200000, "FY2016": -2500000}),
        ("Closing equity", {"FY2025": 117048805, "FY2024": 104929751, "FY2023": 92156775, "FY2022": 74613211, "FY2021": 80081720, "FY2020": 76112483, "FY2019": 77792496, "FY2018": 70606970, "FY2017": 83812609, "FY2016": 79522677}),
    ],
    equity_changes_unit="£",
    cash_flow_totals=[
        ("Net cash from/(used in) operating activities", {"FY2025": 127702657, "FY2024": 53821009, "FY2023": -8259721, "FY2022": 20553004, "FY2021": -73063723, "FY2020": 26837956, "FY2019": -93052123, "FY2018": 31158073, "FY2017": -60544125, "FY2016": 51212287}),
        ("Net cash from/(used in) investing activities", {"FY2025": -122616219, "FY2024": -35765377, "FY2023": -9023414, "FY2022": -45210977, "FY2021": 55618680, "FY2020": -12357660, "FY2019": 100375348, "FY2018": -33926942, "FY2017": 33120852, "FY2016": -17679209}),
        ("Net cash from/(used in) financing activities", {"FY2024": -19306380, "FY2023": 19264847, "FY2022": -1023263, "FY2021": -25464, "FY2020": -18285149, "FY2019": 7918571, "FY2018": -10383259, "FY2017": 5056170, "FY2016": 5665061}),
        ("Cash and cash equivalents at end of year", {"FY2025": 13278966, "FY2024": 8271317, "FY2023": 9725415, "FY2022": 6703512, "FY2021": 33695043, "FY2020": 51425237, "FY2019": 56401421, "FY2018": 41303910, "FY2017": 53211996, "FY2016": 75380334}),
    ],
    cash_flow_unit="£",
    ratios=[
        ("CET1 Ratio", {"FY2023": "21.46%", "FY2022": "19.08%", "FY2024": "19.86%", "FY2021": "22.2%", "FY2020": "23.9%", "FY2019": "21.4%", "FY2018": "21.1%", "FY2017": "18.6%", "FY2016": "17.6%"}),
        ("Tier 1 Ratio", {"FY2023": "21.46%", "FY2022": "19.08%", "FY2024": "19.86%", "FY2021": "22.2%", "FY2020": "23.9%", "FY2019": "21.4%", "FY2018": "21.1%", "FY2017": "18.6%", "FY2016": "17.6%"}),
        ("Total Capital Ratio", {"FY2023": "21.56%", "FY2022": "19.18%", "FY2024": "20.00%", "FY2021": "22.3%", "FY2020": "24%", "FY2019": "21.6%", "FY2018": "21.4%", "FY2017": "19.0%", "FY2016": "18.3%"}),
        ("Leverage Ratio", {"FY2023": "8.52%", "FY2022": "8.43%", "FY2024": "7.17%", "FY2021": "10.97%", "FY2020": "12.55%", "FY2019": "15.51%", "FY2018": "13.95%", "FY2017": "15.8%", "FY2016": "14.4%"}),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own source "
         "citation for the underlying document/page. Pillar 3 ratios/RWA now available for all 10 years FY2016-"
         "FY2024 (FY2016-FY2021 recovered from the Wayback Machine after an initial 1-MiB crawl-truncation of the "
         "first-found snapshots was identified and resolved by locating later, complete captures); FY2025 remains "
         "not disclosed because no FY2025 Pillar 3 edition is published - an enumerated absence on the bank's own "
         "current document index, re-checkable given its very late cadence (see Cash Flow Statement sheet entity "
         "note). LCR/NSFR/MREL: not disclosed in any year reviewed. Balance Sheet/Profit & Loss/Statement of "
         "Changes in Equity/Asset Quality use FY2022's own originally-published figures, not the FY2023 report's "
         "restated FY2022 comparative - see those sheets' own source notes for the resulting ~£2.26m net-loans "
         "discrepancy. Equity roll-forward figures for FY2016-FY2021 combine each year's actuarial/AFS-fair-value/"
         "property-revaluation OCI items into 'Total comprehensive income for the year' (dividends shown "
         "separately as 'Other equity movements, net'); see the Statement of Changes in Equity sheet for the full "
         "line-by-line movements and the FY2017/FY2018 opening-balance restatement noted there.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/UNITED NATIONAL FINANCIALS.xlsx")
