import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021", "FY2020", "FY2019",
         "FY2018", "FY2017", "FY2016", "FY2015"]
YEAR_LABEL = {y: y for y in YEARS}

P3_2025_URL = "https://www.pnb.com.ph/storage/asset-libraries/Me1hxgtaSlrRs32Dvl6SIB1qgOfY1WbTDfGv2ZzQ.pdf"
P3_2024_URL = "https://pnb-website.s3-ap-southeast-1.amazonaws.com/uploads/docs/Pillar3_Disclosures.pdf"
# Older Pillar 3 disclosures are no longer live on pnb.com.ph/pnb-website's S3 bucket; recovered via
# Wayback Machine CDX search of both hosts (pnb.com.ph/europe/images/stories/docs/ and the
# pnb-website S3 bucket). Only three historical snapshots survived: FY2017, FY2019, and a FY2023
# snapshot captured under the live/current filename in Aug 2024 (before it was overwritten by the
# FY2024 document at the same URL).
P3_2017_URL = ("https://web.archive.org/web/20240712011133/"
               "https://www.pnb.com.ph/europe/images/stories/docs/Pillar3_Disclosures_for_2017.pdf")
P3_2019_URL = ("https://web.archive.org/web/20200922133733/"
               "https://www.pnb.com.ph/europe/images/stories/docs/Pillar3_Disclosures_for_2019.pdf")
P3_2023_URL = ("https://web.archive.org/web/20240807151122/"
               "https://pnb-website.s3-ap-southeast-1.amazonaws.com/uploads/docs/Pillar3_Disclosures.pdf")
P3_2016_URL = "https://www.pnb.com.ph/europe/images/stories/docs/Pillar3_Disclosures_for_2016.pdf"
P3_2015_URL = "https://www.pnb.com.ph/europe/images/stories/docs/Pillar3_Disclosures_for_2015.pdf"
# FY2021/FY2020 recovered 2026-09-15: live on the pnb-website S3 bucket at the same predictable
# filename pattern as the years above, both with a real text layer. The long-standing "genuinely
# unobtainable" claim rested on the www.pnb.com.ph/europe host, which 403s every path - including
# years that ARE present - so a 403 there is not evidence of absence.
P3_2021_URL = "https://pnb-website.s3-ap-southeast-1.amazonaws.com/uploads/docs/Pillar3_Disclosures_for_2021.pdf"
P3_2020_URL = "https://pnb-website.s3-ap-southeast-1.amazonaws.com/uploads/docs/Pillar3_Disclosures_for_2020.pdf"

CH_PROFILE_URL = "https://find-and-update.company-information.service.gov.uk/company/02939223"
CH_ACCOUNTS_URL = CH_PROFILE_URL + "/filing-history?category=accounts"
AR2025_URL = CH_ACCOUNTS_URL  # Full Report and Financial Statements, year ended 31 December 2025, filed via Companies House (image-only scan)


def _ch_doc(transaction_id):
    return f"https://find-and-update.company-information.service.gov.uk/company/02939223/filing-history/{transaction_id}/document"


AR2023_URL = _ch_doc("MzQyNDgzNzM4N2FkaXF6a2N4")  # Report and Financial Statements, year ended 31 Dec 2023 (filed 14 Jun 2024)
AR2021_URL = _ch_doc("MzMzODgzMDAxNmFkaXF6a2N4")  # year ended 31 Dec 2021 (filed 13 May 2022)
AR2019_URL = _ch_doc("MzI3MjAzNDU5MmFkaXF6a2N4")  # year ended 31 Dec 2019 (filed 07 Jul 2020)
AR2017_URL = _ch_doc("MzIwMzkwNDM4NGFkaXF6a2N4")  # year ended 31 Dec 2017 (filed 01 May 2018)
AR2015_URL = _ch_doc("MzE1MDIzMzM5NWFkaXF6a2N4")  # year ended 31 Dec 2015 (filed 10 Jun 2016)

ENTITY_NOTE = (
    "ENTITY/BASIS: Philippine National Bank (Europe) Plc (Companies House 02939223; FRN 204532; "
    "LEI 8945002FWV05NGBXJJ26) is the UK-registered bank, wholly owned by Philippine National Bank "
    "(Manila). The Bank's Pillar 3 disclosures in every year located state that PNBE has no "
    "subsidiaries and disclose on an un-consolidated basis. Parent PNB Manila figures and "
    "parent-group disclosures are expressly excluded throughout. Companies House confirms the "
    "entity and its annual 31 December accounts history back to (at least) 2013."
)

HD022_NOTE = (
    "HD-022 HISTORICAL-DEPTH EXTENSION (2026-09): this workbook was extended from a FY2024-FY2025 "
    "window back to FY2015 (the confirmed floor per HD-004's re-scan), re-verifying primary source "
    "PDFs rather than relying on that scan's year alone. Balance Sheet / Profit & Loss / Statement "
    "of Changes in Equity figures for FY2015-FY2023 are transcribed from the Bank's own Report and "
    "Financial Statements filed at Companies House (image-only scans, read directly page-by-page); "
    "five filings (FY2015, FY2017, FY2019, FY2021, FY2023) were fetched, each supplying both its own "
    "year and its prior-year comparative column, covering all nine years FY2015-FY2023 without "
    "needing every intervening filing. Pillar 3 quantitative data (CET1/Tier1/Total Capital, RWA "
    "breakdown) for FY2015-FY2023 was originally not found, but a renewed primary-source check "
    "recovered the live FY2015 and FY2016 documents from the Bank's historical document host. "
    "Those documents add FY2015 Total Capital and FY2016 capital, ratios and RWA breakdown. "
    "UPDATED 2026-09-15: FY2021 and FY2020 are no longer unobtainable - both editions are live on the "
    "pnb-website S3 bucket and are now fully transcribed (capital, ratios and RWA breakdown). Only "
    "FY2018 and FY2022 remain unobtainable. That verdict now rests on ENUMERATION rather than on "
    "filename guessing, which can only ever fail to find a document and never show it is absent "
    "(2026-09-15 sweep): (i) an unfiltered Wayback CDX sweep of the whole pnb.com.ph domain returned "
    "3,617 archived PDF captures, of which the ONLY PNBE Pillar 3 files are the FY2017 and FY2019 "
    "editions already cited below; (ii) an unfiltered CDX sweep of the whole pnb-website S3 bucket "
    "returned 1,564 captures containing exactly one capture of uploads/docs/Pillar3_Disclosures.pdf "
    "(2024-08-07, the FY2023 edition cited below) - the live overwriting URL was never archived at any "
    "other date, which is precisely why FY2022 was lost; (iii) all 31 archived PDFs under the Bank's "
    "newer /storage/asset-libraries/ hashed-filename path were downloaded and read, and none is a "
    "Pillar 3 document (they are credit-card forms, holiday advisories and product terms); and (iv) "
    "PNBE's Pillar 3 template carries NO prior-year comparative column - the Own Fund Composition, "
    "Pillar 1 capital requirements and Capital Buffers tables are each headed by a single 'As at 31 "
    "Dec <year>' column, verified in the FY2019 and FY2023 editions - so neither hole can be filled "
    "from the adjacent year's document the way many banks' KM1 tables allow. Separately, the live "
    "www.pnb.com.ph host now returns HTTP 403 to every request from this environment regardless of "
    "user agent, including the FY2025 asset-libraries URL cited below that was successfully fetched "
    "earlier; that is an access block on the host, NOT evidence about any document's existence, and a "
    "future pass from a different network should re-probe rather than treat these two years as closed. "
    "NOT DERIVED, deliberately: in all four years where both are known (FY2019, FY2021, FY2023, FY2025) "
    "PNBE's Pillar 3 Own Funds equals its Balance Sheet Total equity exactly, which would make FY2022 "
    "Own Funds 'obviously' 10,115. That figure is NOT written to any Pillar 3 sheet here - it would be "
    "a derived number in a disclosure cell, which this project does not do. "
    "FY2015 uses older Basel II/BIPRU terminology and does not disclose "
    "a CET1 ratio; it is populated only in Tier 1/Total Capital where the source supports it. "
    "FY2016 onward uses CRR/CET1 terminology and the Bank states it holds no Tier 2 capital."
)

P3_SOURCES = (
    "Sources - PNBE's own standalone Pillar 3 disclosures (GBP '000 unless stated):\n"
    f"FY2025: Pillar 3 Disclosures for 31 December 2025, pp.3, 5-8 - {P3_2025_URL}\n"
    f"FY2024: Pillar 3 Disclosures for 31 December 2024, pp.3, 5-8 - {P3_2024_URL}\n"
    f"FY2023: Pillar 3 Disclosures for 31 December 2023 (April 2024), pp.5-7 - recovered via Wayback "
    f"Machine (snapshot 2024-08-07) of the pnb-website S3 bucket, since overwritten by the FY2024 "
    f"document at the same live URL - {P3_2023_URL}\n"
    f"FY2021: Pillar 3 Disclosures for 31 December 2021 (April 2022), p.5 Own Fund Composition "
    f"table, p.6 Pillar 1 capital requirements table, p.7 Capital Buffers CET1 capital ratio table "
    f"- {P3_2021_URL}\n"
    f"FY2020: Pillar 3 Disclosures for 31 December 2020 (March 2021), p.5 Own Fund Composition "
    f"table, p.6 Pillar 1 capital requirements table, p.7 Capital Buffers CET1 capital ratio table "
    f"- {P3_2020_URL}\n"
    f"FY2019: Pillar 3 Disclosures for 31 December 2019 (May 2020), pp.5-7 - recovered via Wayback "
    f"Machine (snapshot 2020-09-22) - {P3_2019_URL}\n"
    f"FY2017: Pillar 3 Disclosures for 31 December 2017 (April 2018), pp.5-7 - recovered via Wayback "
    f"Machine (snapshot 2024-07-12) - {P3_2017_URL}\n"
    f"FY2016: Pillar 3 Disclosures for 31 December 2016 (April 2017), pp.5-9 - {P3_2016_URL}\n"
    f"FY2015: Pillar 3 Disclosures for 31 December 2015 (April 2016), pp.5-8 - {P3_2015_URL}\n"
    f"Entity identity and accounts filing history: Companies House - {CH_PROFILE_URL}; {CH_ACCOUNTS_URL}\n"
    "SDDT - EXPLICIT NEGATIVE, recorded 2026-09-15 (cross-bank SDDT date-fit pass) so that a future pass does "
    "not wrongly apply the Small Domestic Deposit Taker exemption to this workbook's gap years. PNBE DOES hold "
    "the SDDT opt-in, but it is too recent to explain anything here. The Bank of England consolidated list of "
    "waivers and modifications granted to PRA-authorised firms (downloaded 2026-09-15, "
    "https://www.bankofengland.co.uk/-/media/boe/files/prudential-regulation/authorisations/"
    "waivers-and-modifications-of-rules/consolidated-waivers-pra-firms.csv) carries two SDDT rows for FRN "
    "204532, 'Philippine National Bank (Europe) Plc': (a) 'Modification by Consent - PRA Rulebook - CRR Firms - "
    "Rule 3.1 of the SDDT Regime - General Application Part', sub rule 'Ru 3.1', waiver ref 'A00011144P.pdf', "
    "START DATE 10/11/2025, no end date; and (b) 'SDDT MbA', sub rule 'Ru 2.1(9)', ref 'A00009160P.pdf', start "
    "27/11/2024, end 27/11/2027. The distinction matters here more than for most firms in this project. Row (b) "
    "modifies an ELIGIBILITY CRITERION only - rule 2.1(9) requires that 'any parent undertaking of the firm is "
    "a UK undertaking', which PNBE plainly fails as a subsidiary of Philippine National Bank, so the "
    "modification is what made it eligible at all. It is NOT a disclosure exemption, and had only row (b) "
    "existed this firm would not be a confirmed SDDT. Only row (a), Rule 3.1, is the opt-in that removes the "
    "Pillar 3 disclosure obligation.\n"
    "DATE FIT - IT DOES NOT FIT. PNBE's accounting reference date is 31 DECEMBER, confirmed at Companies House "
    "(company 02939223, an unbroken run of accounts to 31 December from 2013 to 2025). The outstanding Pillar 3 "
    "gap years are FY2018 and FY2022, which ended 31 December 2018 and 31 December 2022 (this sentence "
    "previously read 'FY2021 and FY2022'; FY2021 was recovered on 2026-09-15 and the date-fit reasoning below "
    "is unaffected, since FY2018 is earlier still). The Rule 3.1 "
    "modification began 10 NOVEMBER 2025 - nearly three years after the later of those year-ends, and nearly "
    "seven after the earlier. Even the "
    "earlier criteria-only row (b) starts 27 November 2024, itself almost two years after FY2022's year-end, "
    "and would not evidence an exemption in any case. So the SDDT regime explains NEITHER the FY2018 nor the "
    "FY2022 blanks.\n"
    "Those gaps keep their existing and entirely separate explanation, unchanged: PNBE's own Pillar 3 documents "
    "are published to a single overwritten live URL, so the FY2022 edition was displaced by a later "
    "one and no Wayback snapshot of it was recovered (FY2018 predates that URL scheme and was never archived "
    "under the older /europe/images/stories/docs/ path either). That is a document-availability gap, not a "
    "regulatory exemption, and it is materially different in kind - PNBE was subject to the obligation in both "
    "years and, so far as anything here shows, discharged it; the documents are simply no longer reachable. The "
    "register finding changes no cell in this workbook. Forward-looking only: from 10 November 2025 PNBE is an "
    "SDDT, so no Pillar 3 document should be expected for FY2026 onward - note that the FY2025 disclosure "
    "sourced above still exists, its 31 December 2025 year-end falling after the modification, which is a "
    "reminder that the exemption permits a firm to stop disclosing but does not force it to. This is the SDDT "
    "DISCLOSURE exemption, in force now - not the separate SDDT CAPITAL regime beginning 1 January 2027.\n"
    + ENTITY_NOTE + "\n\n" + HD022_NOTE
)

EXEMPTION_NOTE = (
    "PILLAR-3-ONLY for FY2015-FY2023 Pillar 3 sheets, no cash-flow statement in any year: the prior "
    "project screening identified PNBE's qualifying-entity cash-flow disclosure exemption in its UK "
    "accounts (confirmed present in every Report and Financial Statements reviewed, FY2015 through "
    "FY2025), so no audited cash-flow statement is populated for any year. The current build does "
    "not infer cash flows from parent PNB disclosures."
)

BS_PL_SOURCES = (
    "Sources - Philippine National Bank (Europe) Plc's own Report and Financial Statements "
    "(Companies House filing history, all image-only scans read page-by-page):\n"
    f"FY2025/FY2024: year ended 31 December 2025 - Statement of Comprehensive Income p.18/printed "
    f"p.17, Statement of Financial Position p.19/printed p.18, Statement of Changes in Equity "
    f"p.20/printed p.19 - {AR2025_URL}\n"
    f"FY2023/FY2022 (2022 \"as restated\", per Note 25): year ended 31 December 2023 - Statement of "
    f"Comprehensive Income printed p.17, Statement of Financial Position printed p.18, Statement of "
    f"Changes in Equity printed p.19 - {AR2023_URL}\n"
    f"FY2021/FY2020: year ended 31 December 2021 - Statement of Comprehensive Income printed p.16, "
    f"Statement of Financial Position printed p.17, Statement of Changes in Equity printed p.18 - "
    f"{AR2021_URL}\n"
    f"FY2019/FY2018: year ended 31 December 2019 - Statement of Comprehensive Income printed p.16, "
    f"Statement of Financial Position printed p.18, Statement of Changes in Equity printed p.19 - "
    f"{AR2019_URL}\n"
    f"FY2017/FY2016 (Total column = continuing + discontinued operations; PNBE wound down a "
    f"discontinued business line around 2017-2018): year ended 31 December 2017 - Statement of "
    f"Comprehensive Income printed p.12, Statement of Financial Position printed p.14, Statement of "
    f"Changes in Equity printed p.15 - {AR2017_URL}\n"
    f"FY2015 (\"Company\" column, i.e. excluding the pro-forma merger column also shown): year ended "
    f"31 December 2015 - Statement of Comprehensive Income printed p.9, Statement of Financial "
    f"Position printed p.11, Statement of Changes in Equity printed p.12 - {AR2015_URL}\n\n"
    + ENTITY_NOTE
)

RESTATEMENT_NOTE = (
    "RESTATEMENT DISCREPANCY (documented, not resolved further): the FY2019 Annual Report's own "
    "comparative Statement of Changes in Equity opens with \"As at 31 December 2017\" totalling "
    "GBP 10,646k (accumulated losses -7,052k, combined with the by-then-zeroed foreign exchange "
    "reserve), whereas the FY2017 Annual Report's own closing balance for the same date is GBP "
    "10,747k (accumulated losses -6,951k + FX reserve 16k = -6,935k combined). The GBP 101k gap is "
    "an apparent prior-period restatement made during FY2018 that we could not further itemize "
    "without the FY2018 Annual Report itself (not fetched in this pass). Each year's own document is "
    "used as the authoritative source for that year's figures; the FY2015-FY2025 chronological "
    "Statement of Changes in Equity sheet carries an explicit \"Prior period restatement\" plug row "
    "of GBP -101k between the FY2017 and FY2018 sections so the roll-forward still sums correctly. "
    "No other year-to-year break of this kind was found - FY2015/2016, FY2019/2020, FY2020/2021 and "
    "FY2021/2022 closing-to-opening balances all tie exactly across adjacent source documents."
)

bw = BankWorkbook(bank_name="Philippine National Bank (Europe) Plc", years=YEARS,
                  year_label=YEAR_LABEL, header_color="007A33")

# --- Balance Sheet -------------------------------------------------------
balance_sheet_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash in hand", {"FY2025": 58, "FY2024": 136, "FY2023": 77, "FY2022": 86, "FY2021": 67,
                              "FY2020": 83, "FY2019": 98, "FY2018": 70, "FY2017": 62, "FY2016": 152,
                              "FY2015": 119}),
    ("DATA", "Treasury bills (captioned \"Investments\" - UK Treasury Gilts - in the FY2015 accounts)",
     {"FY2025": 1294, "FY2024": 2263, "FY2023": 2270, "FY2022": 2285, "FY2021": 2312, "FY2020": 1132,
      "FY2019": 1109, "FY2018": 1106, "FY2017": 1107, "FY2016": 1106, "FY2015": 1141}),
    ("DATA", "Loans and advances to banks", {"FY2025": 12073, "FY2024": 12073, "FY2023": 13113,
                                             "FY2022": 12778, "FY2021": 12370, "FY2020": 15056,
                                             "FY2019": 15875, "FY2018": 15817, "FY2017": 16510,
                                             "FY2016": 19121, "FY2015": 18382}),
    ("DATA", "Loans and advances to customers", {"FY2025": 5, "FY2024": 10, "FY2023": 8, "FY2022": 14,
                                                 "FY2021": 15, "FY2020": 21, "FY2019": 21, "FY2018": 19,
                                                 "FY2017": 22, "FY2016": 20, "FY2015": 29}),
    ("DATA", "Tangible fixed assets", {"FY2025": 364, "FY2024": 412, "FY2023": 408, "FY2022": 448,
                                       "FY2021": 465, "FY2020": 512, "FY2019": 573, "FY2018": 598,
                                       "FY2017": 641, "FY2016": 770, "FY2015": 146}),
    ("DATA", "Pension asset (disclosed nil in FY2016/2018/2019; not a separate line in other years)",
     {"FY2017": 1, "FY2018": 0, "FY2019": 0, "FY2016": 0}),
    ("DATA", "Other assets", {"FY2025": 37, "FY2024": 33, "FY2023": 29, "FY2022": 28, "FY2021": 87,
                              "FY2020": 99, "FY2019": 141, "FY2018": 153, "FY2017": 449, "FY2016": 471,
                              "FY2015": 445}),
    ("DATA", "Prepayments", {"FY2025": 142, "FY2024": 35, "FY2023": 218}),
    ("TOTAL", "Total assets", {"FY2025": 13973, "FY2024": 14962, "FY2023": 16123, "FY2022": 15725,
                               "FY2021": 15316, "FY2020": 16903, "FY2019": 17817, "FY2018": 17763,
                               "FY2017": 18792, "FY2016": 21640, "FY2015": 20262}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Customer accounts", {"FY2025": 397, "FY2024": 411, "FY2023": 426, "FY2022": 438,
                                   "FY2021": 442}),
    ("DATA", "Other liabilities", {"FY2025": 3002, "FY2024": 3849, "FY2023": 5112, "FY2022": 4937,
                                   "FY2021": 4726, "FY2020": 6423, "FY2019": 7497, "FY2018": 7232,
                                   "FY2017": 7831, "FY2016": 10039, "FY2015": 8670}),
    ("DATA", "Accruals and deferred income", {"FY2025": 162, "FY2024": 170, "FY2023": 183, "FY2022": 177,
                                              "FY2021": 152, "FY2020": 141, "FY2019": 175, "FY2018": 162,
                                              "FY2017": 214, "FY2016": 175, "FY2015": 143}),
    ("DATA", "Dilapidation provision", {"FY2025": 68, "FY2024": 65, "FY2023": 61, "FY2022": 58}),
    ("DATA", "Pension liability (disclosed nil in FY2017)", {"FY2017": 0, "FY2016": 198, "FY2015": 252}),
    ("TOTAL", "Total liabilities", {"FY2025": 3629, "FY2024": 4495, "FY2023": 5782, "FY2022": 5610,
                                    "FY2021": 5320, "FY2020": 7024, "FY2019": 7672, "FY2018": 7394,
                                    "FY2017": 8045, "FY2016": 10412, "FY2015": 9065}),
    ("SECTION", "Equity", {}),
    ("DATA", "Called up share capital", {y: 10914 for y in YEARS}),
    ("DATA", "Merger reserve", {y: 6768 for y in YEARS}),
    ("DATA", "Foreign exchange reserve (fully reclassified into accumulated losses during FY2018; "
             "not a separate line from FY2018 on)", {"FY2017": 16, "FY2016": 12, "FY2015": 11}),
    ("DATA", "Accumulated losses", {"FY2025": -7338, "FY2024": -7215, "FY2023": -7341, "FY2022": -7567,
                                    "FY2021": -7686, "FY2020": -7803, "FY2019": -7537, "FY2018": -7313,
                                    "FY2017": -6951, "FY2016": -6466, "FY2015": -6496}),
    ("TOTAL", "Total equity", {"FY2025": 10344, "FY2024": 10467, "FY2023": 10341, "FY2022": 10115,
                               "FY2021": 9996, "FY2020": 9879, "FY2019": 10145, "FY2018": 10369,
                               "FY2017": 10747, "FY2016": 11228, "FY2015": 11197}),
    ("TOTAL", "Total liabilities and equity", {"FY2025": 13973, "FY2024": 14962, "FY2023": 16123,
                                                "FY2022": 15725, "FY2021": 15316, "FY2020": 16903,
                                                "FY2019": 17817, "FY2018": 17763, "FY2017": 18792,
                                                "FY2016": 21640, "FY2015": 20262}),
]

bw.add_balance_sheet_sheet(
    title="Philippine National Bank (Europe) Plc — Statement of Financial Position",
    subtitle="Entity-level (solo, no subsidiaries), £'000. FY2022 figures are \"as restated\" per Note "
             "25 of the FY2023 Annual Report.",
    rows=balance_sheet_rows,
    sources_text=BS_PL_SOURCES + "\n\n" + RESTATEMENT_NOTE,
    first_col_width=68,
    source_height=340,
    unit_suffix=" (£'000)",
)

# --- Profit & Loss ---------------------------------------------------------
income_statement_rows = [
    ("SECTION", "Continuing operations", {}),
    ("DATA", "Interest receivable and similar income arising from debt securities",
     {"FY2025": 281, "FY2024": 329, "FY2023": 249, "FY2022": 77, "FY2021": 14, "FY2020": 49,
      "FY2019": 79, "FY2018": 59, "FY2017": 35, "FY2016": 57, "FY2015": 73}),
    ("DATA", "Other interest receivable and similar income", {"FY2015": 1}),
    ("DATA", "Interest payable", {"FY2018": -2, "FY2017": -11, "FY2016": -5}),
    ("TOTAL", "Net interest income", {"FY2025": 281, "FY2024": 329, "FY2023": 249, "FY2022": 77,
                                      "FY2021": 14, "FY2020": 49, "FY2019": 79, "FY2018": 57,
                                      "FY2017": 24, "FY2016": 52, "FY2015": 74}),
    ("DATA", "Fees and commission income", {"FY2025": 915, "FY2024": 913, "FY2023": 919, "FY2022": 964,
                                            "FY2021": 1011, "FY2020": 1039, "FY2019": 1282, "FY2018": 1317,
                                            "FY2017": 1440, "FY2016": 1467, "FY2015": 1693}),
    ("DATA", "Dealing profits", {"FY2025": 450, "FY2024": 460, "FY2023": 513, "FY2022": 518,
                                 "FY2021": 489, "FY2020": 421, "FY2019": 424, "FY2018": 310,
                                 "FY2017": 256, "FY2016": 754, "FY2015": 415}),
    ("DATA", "Other operating income", {"FY2025": 19, "FY2024": 30, "FY2023": 27, "FY2022": 23,
                                        "FY2021": 68, "FY2020": 75, "FY2019": 104, "FY2018": 94,
                                        "FY2017": 31, "FY2016": 24, "FY2015": 40}),
    ("DATA", "(Losses)/gains from foreign exchange transactions",
     {"FY2025": -18, "FY2024": -10, "FY2023": -1, "FY2022": -18, "FY2021": -15, "FY2020": 10,
      "FY2019": -23}),
    ("TOTAL", "Operating income", {"FY2025": 1647, "FY2024": 1722, "FY2023": 1707, "FY2022": 1564,
                                   "FY2021": 1567, "FY2020": 1594, "FY2019": 1866, "FY2018": 1790,
                                   "FY2017": 1751, "FY2016": 2297, "FY2015": 2222}),
    ("DATA", "Administrative expenses", {"FY2025": -2091, "FY2024": -1665, "FY2023": -1441,
                                         "FY2022": -1373, "FY2021": -1406, "FY2020": -1456,
                                         "FY2019": -1602, "FY2018": -1589, "FY2017": -2042,
                                         "FY2016": -1978, "FY2015": -2314}),
    ("DATA", "Depreciation and amortisation", {"FY2025": -48, "FY2024": -46, "FY2023": -40,
                                               "FY2022": -45, "FY2021": -44, "FY2020": -61,
                                               "FY2019": -63, "FY2018": -61, "FY2017": -136,
                                               "FY2016": -86, "FY2015": -55}),
    ("TOTAL", "Operating (loss)/profit before provisions (FY2015-FY2017 only; no provisions line "
              "shown from FY2018 on)", {"FY2017": -427, "FY2016": 233, "FY2015": -147}),
    ("DATA", "Provisions for bad and doubtful debts (recovery)/charge", {"FY2017": -15, "FY2016": -15,
                                                                          "FY2015": 10}),
    ("TOTAL", "(Loss)/profit on ordinary activities before tax", {"FY2025": -492, "FY2024": 11,
                                                                   "FY2023": 226, "FY2022": 146,
                                                                   "FY2021": 117, "FY2020": 77,
                                                                   "FY2019": 201, "FY2018": 140,
                                                                   "FY2017": -442, "FY2016": 218,
                                                                   "FY2015": -137}),
    ("DATA", "Taxation", {y: 0 for y in YEARS}),
    ("TOTAL", "(Loss)/profit for the year", {"FY2025": -492, "FY2024": 11, "FY2023": 226, "FY2022": 146,
                                              "FY2021": 117, "FY2020": 77, "FY2019": 201, "FY2018": 140,
                                              "FY2017": -442, "FY2016": 218, "FY2015": -137}),
    ("SECTION", "Other comprehensive income", {}),
    ("DATA", "Foreign exchange reserve movement", {"FY2017": 4, "FY2016": 1, "FY2015": 3}),
    ("DATA", "Pension plan actuarial gain/(loss) recognised", {"FY2025": 369, "FY2024": 115,
                                                                "FY2020": -343}),
    ("DATA", "Other comprehensive income (not separately itemized in the Statement of Comprehensive "
             "Income; per the Statement of Changes in Equity)",
     {"FY2019": -425, "FY2018": -417, "FY2017": -43, "FY2016": -188, "FY2015": 6}),
    ("DATA", "Prior year adjustment (per Note 25 of the FY2023 Annual Report's restatement)",
     {"FY2022": -27}),
    ("TOTAL", "Total comprehensive (loss)/income", {"FY2025": -123, "FY2024": 126, "FY2023": 226,
                                                     "FY2022": 119, "FY2021": 117, "FY2020": -266,
                                                     "FY2019": -224, "FY2018": -277, "FY2017": -481,
                                                     "FY2016": 31, "FY2015": -128}),
]

bw.add_income_statement_sheet(
    title="Philippine National Bank (Europe) Plc — Statement of Comprehensive Income",
    subtitle="Entity-level (solo, no subsidiaries), £'000. Taxation is £nil in every year shown (as "
             "\"-\" in each source), not a blank/undisclosed cell. FY2016-FY2017 use each source "
             "document's \"Total\" column (continuing + discontinued operations combined).",
    rows=income_statement_rows,
    sources_text=BS_PL_SOURCES + "\n\n" + RESTATEMENT_NOTE,
    first_col_width=80,
    source_height=340,
    unit_suffix=" (£'000)",
)

# --- Statement of Changes in Equity (chronological) ------------------------
# Foreign exchange reserve is folded into "Accumulated losses" throughout (it is fully reclassified
# there during FY2018 in the source documents anyway; combining it from the start keeps every row a
# clean 4-column tuple matching the FY2024/FY2025 rows below, and every combined-column balance below
# ties exactly to that year's own Balance Sheet Total equity figure - see RESTATEMENT_NOTE for the one
# genuine break, between FY2017 and FY2018).
EQUITY_HEADERS = ["Called up share capital", "Merger reserve", "Accumulated losses", "Total equity"]
equity_changes_rows = [
    ("TOTAL", "Balance as at 31 December 2014 (opening; pre-scope, from the FY2015 Annual Report's "
              "own comparative column)", (10914, 1768, -6357, 6325)),
    ("DATA", "(Loss) for the year (2015)", (None, None, -137, -137)),
    ("DATA", "Other comprehensive income (2015; FX translation + P&L account items, combined)",
     (None, None, 9, 9)),
    ("TOTAL", "Total comprehensive (loss) for the year (2015)", (None, None, -128, -128)),
    ("DATA", "Increase in merger reserve (2015)", (None, 5000, None, 5000)),
    ("TOTAL", "Balance as at 31 December 2015", (10914, 6768, -6485, 11197)),
    ("DATA", "Profit for the year (2016)", (None, None, 218, 218)),
    ("DATA", "Other comprehensive income (2016; FX translation + P&L account items, combined)",
     (None, None, -187, -187)),
    ("TOTAL", "Total comprehensive income for the year (2016)", (None, None, 31, 31)),
    ("TOTAL", "Balance as at 31 December 2016", (10914, 6768, -6454, 11228)),
    ("DATA", "(Loss) for the year (2017)", (None, None, -442, -442)),
    ("DATA", "Other comprehensive income (2017; FX translation + P&L account items, combined)",
     (None, None, -39, -39)),
    ("TOTAL", "Total comprehensive (loss) for the year (2017)", (None, None, -481, -481)),
    ("TOTAL", "Balance as at 31 December 2017 (per the Bank's own FY2017 Annual Report)",
     (10914, 6768, -6935, 10747)),
    ("DATA", "Prior period restatement recognised during FY2018 (magnitude only - see "
             "RESTATEMENT_NOTE in the source citations below)", (None, None, -101, -101)),
    ("TOTAL", "Balance as at 31 December 2017 (as restated; opening balance per the FY2019 Annual "
              "Report's own comparative column)", (10914, 6768, -7036, 10646)),
    ("DATA", "Profit for the year (2018)", (None, None, 140, 140)),
    ("DATA", "Other comprehensive income (2018)", (None, None, -417, -417)),
    ("TOTAL", "Total comprehensive income for the year (2018)", (None, None, -277, -277)),
    ("TOTAL", "Balance as at 31 December 2018", (10914, 6768, -7313, 10369)),
    ("DATA", "Profit for the year (2019)", (None, None, 201, 201)),
    ("DATA", "Other comprehensive income (2019)", (None, None, -425, -425)),
    ("TOTAL", "Total comprehensive income for the year (2019)", (None, None, -224, -224)),
    ("TOTAL", "Balance as at 31 December 2019", (10914, 6768, -7537, 10145)),
    ("DATA", "Profit for the year (2020)", (None, None, 77, 77)),
    ("DATA", "Other comprehensive loss (2020) - pension liability actuarial loss recognised",
     (None, None, -343, -343)),
    ("TOTAL", "Total comprehensive (loss)/income for the year (2020)", (None, None, -266, -266)),
    ("TOTAL", "Balance as at 31 December 2020", (10914, 6768, -7803, 9879)),
    ("DATA", "Profit for the year (2021)", (None, None, 117, 117)),
    ("TOTAL", "Total comprehensive income for the year (2021)", (None, None, 117, 117)),
    ("TOTAL", "Balance as at 31 December 2021", (10914, 6768, -7686, 9996)),
    ("DATA", "Profit for the year (2022, as restated)", (None, None, 146, 146)),
    ("DATA", "Prior year adjustment (per Note 25 of the FY2023 Annual Report's restatement)",
     (None, None, -27, -27)),
    ("TOTAL", "Total comprehensive income for the year (2022, as restated)", (None, None, 119, 119)),
    ("TOTAL", "Balance as at 31 December 2022 (as restated)", (10914, 6768, -7567, 10115)),
    ("DATA", "Profit for the year (2023)", (None, None, 226, 226)),
    ("TOTAL", "Total comprehensive income for the year (2023)", (None, None, 226, 226)),
    ("TOTAL", "Balance as at 31 December 2023", (10914, 6768, -7341, 10341)),
    ("DATA", "Profit for the year", (None, None, 11, 11)),
    ("DATA", "Change in the pension scheme asset ceiling", (None, None, 185, 185)),
    ("DATA", "Actuarial loss on pension scheme", (None, None, -70, -70)),
    ("TOTAL", "Total comprehensive income for the year", (None, None, 126, 126)),
    ("TOTAL", "Balance as at 31 December 2024", (10914, 6768, -7215, 10467)),
    ("DATA", "(Loss) for the year", (None, None, -492, -492)),
    ("DATA", "Change in the pension scheme asset ceiling", (None, None, 741, 741)),
    ("DATA", "Actuarial loss on pension scheme", (None, None, -372, -372)),
    ("TOTAL", "Total comprehensive (loss) for the year", (None, None, -123, -123)),
    ("TOTAL", "Balance as at 31 December 2025", (10914, 6768, -7338, 10344)),
]

bw.add_equity_changes_sheet(
    title="Philippine National Bank (Europe) Plc — Statement of Changes in Equity",
    subtitle="Entity-level (solo, no subsidiaries), £'000, chronological, FY2015-FY2025. The foreign "
             "exchange reserve (a separate column in the Bank's own statements through FY2017) is "
             "folded into \"Accumulated losses\" throughout this sheet for a consistent 4-column "
             "shape - it is fully reclassified there in the source documents themselves during "
             "FY2018 in any case. Opening row is the Bank's own 31 December 2014 balance, reproduced "
             "from the FY2015 Annual Report's own comparative column - not itself a covered year in "
             "this workbook's scope.",
    headers=EQUITY_HEADERS,
    rows=equity_changes_rows,
    sources_text=BS_PL_SOURCES + "\n\n" + RESTATEMENT_NOTE + (
        "\n\nEQUITY-SHEET-SPECIFIC NOTE: every movement above is a distinct line the Bank's own "
        "Statement of Changes in Equity discloses for that year (or, for FY2015-2017, the sum of its "
        "disclosed foreign exchange reserve movement and P&L account movement, collapsed into one "
        "combined-column figure - see the sheet subtitle). Every TOTAL balance row ties exactly to "
        "that year's own Balance Sheet Total equity figure, except the single documented restatement "
        "break between FY2017 and FY2018 (see RESTATEMENT_NOTE above)."
    ),
)

bw.add_cash_flow_sheet(
    title="Philippine National Bank (Europe) Plc — Cash Flow Statement",
    subtitle="Not applicable — Pillar-3-only scope; see the exemption and coverage note below.",
    rows=[
        ("SECTION", "No standalone Statement of Cash Flows populated", {}),
        ("DATA", "PNBE cash-flow disclosure exemption (confirmed present FY2015-FY2025); "
                 "parent-group cash flows are not substituted.", {}),
    ],
    sources_text=ENTITY_NOTE + "\n\n" + EXEMPTION_NOTE + "\n\n" + P3_SOURCES,
    first_col_width=78, source_height=280, unit_suffix=" (£'000)",
)

# --- Asset Quality ----------------------------------------------------------
ASSET_QUALITY_NOTE = (
    "SCOPE NOTE: the granular by-maturity and related-party sub-breakdowns below (payable-on-demand "
    "vs. 3-6 month buckets, amounts due from parent/fellow subsidiaries, customer-loan maturity "
    "bands) were transcribed only for FY2024-FY2025, from each year's own Note 6/7 loan-maturity "
    "tables. Extending that granular sub-note transcription back through FY2015 was out of scope for "
    "this pass; the two TOTAL rows below (which ARE fully extended to FY2015) are the same "
    "Loans and advances to banks / to customers figures already shown on the Balance Sheet sheet, "
    "sourced from the same five Annual Report filings cited there."
)

asset_quality_rows = [
    ("SECTION", "Loans and advances to banks, by maturity (sub-breakdown: FY2024-FY2025 only)", {}),
    ("DATA", "Payable on demand", {"FY2025": 7045, "FY2024": 8794}),
    ("DATA", "Payable in more than three months but not more than six months", {"FY2025": 5028, "FY2024": 3279}),
    ("TOTAL", "Total loans and advances to banks", {"FY2025": 12073, "FY2024": 12073, "FY2023": 13113,
                                                     "FY2022": 12778, "FY2021": 12370, "FY2020": 15056,
                                                     "FY2019": 15875, "FY2018": 15817, "FY2017": 16510,
                                                     "FY2016": 19121, "FY2015": 18382}),
    ("DATA", "of which: due from parent and fellow subsidiary undertakings (FY2024-FY2025 only)",
     {"FY2025": 134, "FY2024": 447}),
    ("SECTION", "Loans and advances to customers, by maturity (sub-breakdown: FY2024-FY2025 only)", {}),
    ("DATA", "Not more than three months", {"FY2025": 1, "FY2024": 0}),
    ("DATA", "More than three months but less than one year", {"FY2025": 0, "FY2024": 1}),
    ("DATA", "More than one year but less than five years", {"FY2025": 4, "FY2024": 9}),
    ("TOTAL", "Total loans and advances to customers", {"FY2025": 5, "FY2024": 10, "FY2023": 8,
                                                         "FY2022": 14, "FY2021": 15, "FY2020": 21,
                                                         "FY2019": 21, "FY2018": 19, "FY2017": 22,
                                                         "FY2016": 20, "FY2015": 29}),
]

bw.add_asset_quality_sheet(
    title="Philippine National Bank (Europe) Plc — Asset Quality",
    subtitle="Entity-level, £'000. No IFRS 9 Stage 1/2/3 split, no impairment provision, and no "
             "credit-quality grading is disclosed for either loan category in any year reviewed.",
    rows=asset_quality_rows,
    sources_text=BS_PL_SOURCES + "\n\n" + ASSET_QUALITY_NOTE + (
        "\n\nDATA QUALITY NOTE: this Bank carries almost no customer-facing lending book across every "
        "year reviewed - Loans and advances to customers peaks at £29k (FY2015) and is as low as £5k "
        "(FY2025), consistently a handful of personal loans to employees. No impairment provision, "
        "write-off, or IFRS 9 stage split is disclosed against this balance in any year - the Bank's "
        "own notes show no bad-debt note at all for it, consistent with its immateriality. The Bank's "
        "principal credit exposure is instead Loans and advances to banks (its correspondent/"
        "deposit-placement business with other banks including its own parent and fellow PNB "
        "subsidiaries) - this Bank is a treasury/correspondent-banking entity for its parent, not a "
        "retail or commercial lender, in every year reviewed."
    ),
    first_col_width=78,
    source_height=320,
    unit_suffix=" (£'000)",
)


def metric(name, unit, rows, note=None):
    bw.add_metric_sheet(name, unit, rows, P3_SOURCES, note=note,
                        first_col_width=48, source_height=280)


# FY2015 uses the older Basel II/BIPRU disclosure convention: only Tier 1/Total Capital is reported.
# FY2018, FY2020, FY2021 and FY2022 remain self-skipped after the renewed Wayback/live-host search.
CET1_FUNDS = {"FY2025": 10344, "FY2024": 10467, "FY2023": 10341, "FY2021": 9996, "FY2020": 9879,
              "FY2019": 10145, "FY2017": 10747, "FY2016": 11228}
# FY2022/FY2021/FY2020 were first recovered 2026-09-12 from the Bank's OWN statutory accounts (the
# "Capital management" table in Note 18/20 "Risk management"). That table labels its two rows exactly
# "Tier 1 Capital" and "Total Capital" and gives an identical amount for both.
#
# UPDATED 2026-09-15: the FY2021 and FY2020 Pillar 3 documents have since been recovered, and their
# "Own Fund Composition" tables independently reproduce those same two amounts to the pound -
# GBP9,996k (FY2021) and GBP9,879k (FY2020). No cell value changes; what changes is that these two
# years are now corroborated by the like-for-like Pillar 3 source used for every other year here,
# and the Pillar 3 documents DO use the CET1 label ("Being CET1 capital the same as Tier 1 capital
# and Total capital"), which is what now justifies populating CET1 Capital for them.
#
# FY2022 is unchanged and remains statutory-accounts-only: no FY2022 Pillar 3 document survives, the
# accounts never use the CET1 label, and inferring it would go beyond what that source states - so
# FY2022 still populates Tier 1 Capital and Total Capital but NOT CET1 Capital or any ratio.
AR_CAPITAL = {"FY2022": 10147, "FY2021": 9996, "FY2020": 9879}
TIER1_FUNDS = {**CET1_FUNDS, "FY2015": 11197, **AR_CAPITAL}
CAPITAL_RATIO = {"FY2025": "127.55%", "FY2024": "136.95%", "FY2023": "121.95%", "FY2021": "124.45%",
                 "FY2020": "95.80%", "FY2019": "96.76%", "FY2017": "96.63%", "FY2016": "92.23%"}
TOTAL_RWA = {"FY2025": 8110, "FY2024": 7643, "FY2023": 8480, "FY2021": 8031, "FY2020": 10312,
             "FY2019": 10485, "FY2017": 11122, "FY2016": 12174}
PILLAR3_SKIP_NOTE = ("CORRECTED 2026-09-15 - THE FY2021 AND FY2020 PILLAR 3 DOCUMENTS DO SURVIVE AND ARE "
                     "NOW USED. This note previously read that FY2015, FY2018, FY2020, FY2021 and FY2022 "
                     "were 'genuinely unobtainable'. That was wrong for FY2021 and FY2020: both are live "
                     "on the pnb-website S3 bucket right now, at the same predictable filename pattern as "
                     "the years already cited - "
                     "pnb-website.s3-ap-southeast-1.amazonaws.com/uploads/docs/Pillar3_Disclosures_for_2021"
                     ".pdf (452KB) and .../Pillar3_Disclosures_for_2020.pdf (411KB), both with a real text "
                     "layer. The earlier conclusion appears to have rested on the www.pnb.com.ph/europe "
                     "host, which returns HTTP 403 to every path including the years that ARE present, so "
                     "a 403 there proves nothing about whether a document exists. FY2022, FY2018 and "
                     "FY2015 were re-probed on the S3 bucket this session across seven filename "
                     "permutations and do genuinely 403 while FY2021/FY2020 return 200 from the identical "
                     "pattern - so those three remain unobtainable, now on much better evidence.\n"
                     "NOW TRANSCRIBED 2026-09-15 (this supersedes the follow-up note that previously stood "
                     "here): both editions' capital tables have been read and are in this workbook. FY2021 "
                     "p.5 'Own Fund Composition' gives Own Funds (Total capital) GBP9,996k, built as share "
                     "capital 10,914 + merger reserve 6,768 + profit and loss reserve (7,686); FY2020 p.5 "
                     "gives GBP9,879k as 10,914 + 6,768 + (7,803). Both foot exactly, and both reproduce "
                     "the amount this workbook already held for that year from the statutory accounts - "
                     "independent confirmation of entity and year. Each document states 'Tier 1 capital "
                     "comprises ordinary share capital plus reserves. The Bank does not hold any Tier 2 "
                     "capital', so CET1 = Tier 1 = Total capital, and CET1 Capital is now populated for "
                     "both years on the Bank's own explicit statement rather than by inference.\n"
                     "RATIOS: the 'Capital Buffers' table (p.7 of each) prints a single CET1 capital ratio "
                     "- 124.45% at 31 Dec 2021 and 95.80% at 31 Dec 2020 - under footnote 1/ 'Being CET1 "
                     "capital the same as Tier 1 capital and Total capital, the CET1 capital ratio is equal "
                     "to Tier 1 capital ratio and Total capital ratio.' That footnote is why one printed "
                     "figure populates all three ratio sheets for these years; it is the Bank's own stated "
                     "equivalence, not a derivation. FY2020 ties exactly against this workbook's own "
                     "figures (9,879 / 10,312 = 95.80%). FY2021 gives 9,996 / 8,031 = 124.47% against the "
                     "124.45% printed - a 0.02pp rounding difference inside the Bank's own calculation. The "
                     "PRINTED value is carried, not the recomputed one; no ratio in this workbook is "
                     "back-solved from capital and RWAs.\n"
                     "PARTIAL RECOVERY 2026-09-12 (disclosure audit): FY2022, FY2021 and FY2020 Tier 1 "
                     "Capital and Total Capital are now populated from the Bank's own statutory accounts "
                     "instead - the 'Capital management' table in Note 18 (FY2021 accounts) and Note 20 "
                     "(FY2023 accounts) gives Tier 1 Capital = Total Capital of GBP10,147k (FY2022), "
                     "GBP9,996k (FY2021) and GBP9,879k (FY2020). SUPERSEDED IN PART 2026-09-15: FY2021 and "
                     "FY2020 now have their own Pillar 3 documents (above), so only FY2022 still rests on "
                     "the accounts alone, and only FY2022's CET1 Capital, ratios and Total RWAs remain "
                     "blank. The reason is unchanged for that year: the accounts' capital note discloses no "
                     "CET1 figure, no RWA figure and no ratio, only the two capital amounts plus the PRA's "
                     "total capital requirement in GBP (FY2022 GBP4,812k; FY2021 GBP4,634k; FY2020 "
                     "GBP5,088k), which is a capital requirement and not an RWA - it must not be converted "
                     "to an RWA by dividing by 8%.\n"
                     "BASIS DIFFERENCE WORTH KNOWING: for FY2023 the statutory accounts' capital note "
                     "states Tier 1/Total Capital of GBP10,378k, whereas this workbook's FY2023 figure "
                     "(GBP10,341k) comes from that year's Pillar 3 document. The GBP37k difference is a "
                     "genuine source-basis difference, left as each document states it rather than "
                     "reconciled; the Pillar 3 figure is retained for FY2023 because it is the like-for-"
                     "like source used for every other Pillar-3-sourced year.")

metric("CET1 Capital", "GBP '000", [("Common Equity Tier 1 (CET1) capital", CET1_FUNDS)],
       note=PILLAR3_SKIP_NOTE)
metric("CET1 Ratio", "%", [("CET1 capital ratio", CAPITAL_RATIO)],
       note="CET1 = Tier 1 = total capital in every year located; PNBE states it holds no Tier 2 "
            "capital. " + PILLAR3_SKIP_NOTE)
metric("Tier 1 Capital", "GBP '000", [("Tier 1 capital", TIER1_FUNDS)], note=PILLAR3_SKIP_NOTE)
metric("Tier 1 Ratio", "%", [("Tier 1 capital ratio", CAPITAL_RATIO)], note=PILLAR3_SKIP_NOTE)
metric("Total Capital", "GBP '000", [("Own funds / total capital", TIER1_FUNDS)], note=PILLAR3_SKIP_NOTE)
metric("Total Capital Ratio", "%", [("Total capital ratio", CAPITAL_RATIO)], note=PILLAR3_SKIP_NOTE)
metric("Total RWAs", "GBP '000", [("Total risk-weighted assets", TOTAL_RWA)],
       note="Total is the sum of credit/counterparty, market and operational RWA components in each "
            "source table. " + PILLAR3_SKIP_NOTE)

# --- RWA Breakdown (placed right after Total RWAs, per the locked sheet order) ---
rwa_breakdown_rows = [
    ("DATA", "Credit and counterparty credit risk", {"FY2025": 4568, "FY2024": 4486, "FY2023": 5236,
                                                      "FY2021": 4751, "FY2020": 6194,
                                                      "FY2019": 6444, "FY2017": 6845, "FY2016": 7635}),
    ("DATA", "Market risk", {"FY2025": 370, "FY2024": 36, "FY2023": 220,
                              "FY2021": 138, "FY2020": 837,
                              "FY2019": 661, "FY2017": 358, "FY2016": 351}),
    ("DATA", "Operational risk", {"FY2025": 3172, "FY2024": 3121, "FY2023": 3024,
                                  "FY2021": 3142, "FY2020": 3281,
                                  "FY2019": 3380, "FY2017": 3919, "FY2016": 4188}),
    ("TOTAL", "Total Pillar 1 risk-weighted assets", {"FY2025": 8110, "FY2024": 7643, "FY2023": 8480,
                                                       "FY2021": 8031, "FY2020": 10312,
                                                       "FY2019": 10485, "FY2017": 11122, "FY2016": 12174}),
]

bw.add_rwa_breakdown_sheet(
    title="Philippine National Bank (Europe) Plc — RWA Breakdown",
    subtitle="Entity-level, GBP '000. Pillar 1 capital requirements table, by risk category.",
    rows=rwa_breakdown_rows,
    sources_text=P3_SOURCES + (
        "\n\nEach year's table (\"The Bank's Pillar 1 capital requirements are presented in the table "
        f"below\") - FY2025/FY2024 p.6, FY2023 p.6, FY2019 p.6, FY2017 p.6 of the respective Pillar 3 "
        "Disclosures. Every year shown ties exactly to that year's Total RWAs sheet figure and to that "
        "year's own Own Funds/Total Capital figure on the Balance Sheet / equity sheets.\n\n"
        "FY2021 & FY2020 ADDED 2026-09-15 from the same table in those years' own Pillar 3 Disclosures "
        "(p.6 of each), headed 'As at 31 Dec 2021' and 'As at 31 Dec 2020' respectively, in the same "
        "'GBP 000 / RWAs / Capital Requirements' two-column format as every other year on this sheet. "
        "Both are internally exact: FY2021 credit and counterparty 4,751 + market 138 + operational "
        "3,142 = the document's own printed Total of 8,031; FY2020 6,194 + 837 + 3,281 = its own printed "
        "Total of 10,312. Each category's Capital Requirements column is 8% of its RWA column to the "
        "rounding (4,751 x 8% = 380; 6,194 x 8% = 496), confirming the first column is RWA and not a "
        "capital requirement. The Total RWAs sheet's FY2021/FY2020 figures were previously blank and are "
        "now populated from these same two Total rows - the figures are the same disclosure, so leaving "
        "one sheet blank while the other showed a total would have been internally inconsistent. "
        "Both documents have a real text layer; no OCR was involved. "
        + PILLAR3_SKIP_NOTE
    ),
    first_col_width=54,
    source_height=280,
    unit_suffix=" (GBP '000)",
)

UNDISCLOSED = ["Leverage Ratio", "LCR", "NSFR", "MREL Ratio"]
bw.add_not_disclosed_metric_sheets(
    UNDISCLOSED, P3_SOURCES,
    per_note={name: "No quantitative standalone PNBE disclosure was located in any Pillar 3 document "
                    "reviewed (FY2017, FY2019, FY2023, FY2024 or FY2025); left blank rather than "
                    "estimated for every year in scope.\n"
                    "RE-CHECKED 2026-09-12 (disclosure audit) - this is now partly an ACCESS problem, "
                    "not only a disclosure one, and the distinction matters for anyone retrying it. "
                    "The whole pnb.com.ph host now returns HTTP 403 to automated requests, including "
                    "the FY2016 and FY2017 Pillar 3 URLs this workbook already cites as live sources "
                    "and the site root itself, so a live fetch can no longer distinguish 'document "
                    "absent' from 'document present but blocked'. A Wayback CDX sweep of the whole "
                    "pnb.com.ph domain returns only two archived Pillar 3 PDFs ever (2017 and 2019), "
                    "so the missing years are genuinely unarchived. A human with a browser could "
                    "confirm whether FY2018/FY2020/FY2021/FY2022 documents exist at the site's own "
                    "naming convention, https://www.pnb.com.ph/europe/images/stories/docs/"
                    "Pillar3_Disclosures_for_<YEAR>.pdf. Separately confirmed this pass: the Bank's "
                    "statutory accounts carry no leverage ratio, LCR or NSFR in any year - their "
                    "capital note covers capital amounts only - so these metrics would have to come "
                    "from a Pillar 3 document even if one were reachable. MREL is additionally "
                    "inapplicable: PNBE is not a UK resolution entity."
              for name in UNDISCLOSED},
)

bw.add_overview_sheet(
    cash_flow_totals=[], cash_flow_unit=None,
    ratios=[("CET1 Ratio", CAPITAL_RATIO), ("Tier 1 Ratio", CAPITAL_RATIO),
            ("Total Capital Ratio", CAPITAL_RATIO)],
    balance_sheet_totals=[
        ("Total assets", {"FY2025": 13973, "FY2024": 14962, "FY2023": 16123, "FY2022": 15725,
                          "FY2021": 15316, "FY2020": 16903, "FY2019": 17817, "FY2018": 17763,
                          "FY2017": 18792, "FY2016": 21640, "FY2015": 20262}),
        ("Loans and advances to banks", {"FY2025": 12073, "FY2024": 12073, "FY2023": 13113,
                                         "FY2022": 12778, "FY2021": 12370, "FY2020": 15056,
                                         "FY2019": 15875, "FY2018": 15817, "FY2017": 16510,
                                         "FY2016": 19121, "FY2015": 18382}),
        ("Customer accounts", {"FY2025": 397, "FY2024": 411, "FY2023": 426, "FY2022": 438,
                               "FY2021": 442}),
        ("Total equity", {"FY2025": 10344, "FY2024": 10467, "FY2023": 10341, "FY2022": 10115,
                          "FY2021": 9996, "FY2020": 9879, "FY2019": 10145, "FY2018": 10369,
                          "FY2017": 10747, "FY2016": 11228, "FY2015": 11197}),
    ],
    balance_sheet_unit="£'000",
    income_statement_totals=[
        ("Operating income", {"FY2025": 1647, "FY2024": 1722, "FY2023": 1707, "FY2022": 1564,
                              "FY2021": 1567, "FY2020": 1594, "FY2019": 1866, "FY2018": 1790,
                              "FY2017": 1751, "FY2016": 2297, "FY2015": 2222}),
        ("Administrative expenses", {"FY2025": -2091, "FY2024": -1665, "FY2023": -1441, "FY2022": -1373,
                                     "FY2021": -1406, "FY2020": -1456, "FY2019": -1602, "FY2018": -1589,
                                     "FY2017": -2042, "FY2016": -1978, "FY2015": -2314}),
        ("(Loss)/profit for the year", {"FY2025": -492, "FY2024": 11, "FY2023": 226, "FY2022": 146,
                                        "FY2021": 117, "FY2020": 77, "FY2019": 201, "FY2018": 140,
                                        "FY2017": -442, "FY2016": 218, "FY2015": -137}),
    ],
    income_statement_unit="£'000",
    equity_changes_totals=[
        ("Opening equity", {"FY2025": 10467, "FY2024": 10341, "FY2023": 10115, "FY2022": 9996,
                            "FY2021": 9879, "FY2020": 10145, "FY2019": 10369, "FY2018": 10646,
                            "FY2017": 11228, "FY2016": 11197, "FY2015": 6325}),
        ("Total comprehensive income/(loss) for the year", {"FY2025": -123, "FY2024": 126,
                                                             "FY2023": 226, "FY2022": 119,
                                                             "FY2021": 117, "FY2020": -266,
                                                             "FY2019": -224, "FY2018": -277,
                                                             "FY2017": -481, "FY2016": 31,
                                                             "FY2015": -128}),
        ("Closing equity", {"FY2025": 10344, "FY2024": 10467, "FY2023": 10341, "FY2022": 10115,
                            "FY2021": 9996, "FY2020": 9879, "FY2019": 10145, "FY2018": 10369,
                            "FY2017": 10747, "FY2016": 11228, "FY2015": 11197}),
    ],
    equity_changes_unit="£'000",
    note=("HD-022 extension (2026-09): FY2015-FY2025 Balance Sheet / P&L / Equity coverage in full "
          "(11 years); Pillar 3 capital ratios and RWA breakdown for the seven years with a "
          "surviving Pillar 3 document - FY2016, FY2017, FY2019, FY2023, FY2024, FY2025 and, added "
          "2026-09-15 after both editions were recovered live from the pnb-website S3 bucket, FY2021 "
          "and FY2020 - see the Pillar 3 sheets' own notes for the years that remain self-skipped "
          "(FY2015 partial, FY2018 and FY2022). No cash-flow statement in any year "
          "(qualifying-entity exemption). No parent-group data is used in any year. FY2017's opening "
          "equity above (11,228) is FY2016's own closing balance; FY2018's opening equity (10,646) "
          "reflects a documented prior-period restatement - see the Statement of Changes in Equity "
          "sheet's own RESTATEMENT_NOTE."),
)

bw.save("/Users/armaan/code/katalysis/banks/PHILIPPINE NATIONAL BANK EUROPE FINANCIALS.xlsx")
