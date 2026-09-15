import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook


YEARS = ["FY2026", "FY2025", "FY2024", "FY2023", "FY2021"]
YEAR_LABEL = {
    "FY2026": "FY2026",
    "FY2025": "FY2025",
    "FY2024": "FY2024",
    "FY2023": "FY2023 (15m)",
    "FY2021": "FY2021",
}

AR2026_URL = "https://find-and-update.company-information.service.gov.uk/company/11995458/filing-history/MzUzNDg0MTU0OWFkaXF6a2N4/document?format=pdf&download=0"
AR2025_URL = "https://streambank.co.uk/pdf/March-2025-Annual-Report-2025.pdf"
AR2024_URL = "https://streambank.co.uk/pdf/StreamBank-Plc-FY24-Live-PwC-Signed.pdf"
AR2023_URL = "https://streambank.co.uk/pdf/StreamBank-Plc-Financial-Statements-31-March-2023-Signed.pdf"
AR2021_URL = "https://find-and-update.company-information.service.gov.uk/company/11995458/filing-history/MzM0MzQ4NDk4M2FkaXF6a2N4/document?download=0&format=pdf"
P3_2025_URL = "https://streambank.co.uk/pdf/March-2025-Pillar-3-Disclosures.pdf"
P3_2024_URL = "https://streambank.co.uk/pdf/FY24-Pillar-3-StreamBank-PLC.pdf"
# FOUND 2026-09-15 by enumerating the site's JavaScript bundle (see SITE ENUMERATION
# NOTE in p3_sources). The Bank publishes its own FY2026 Annual Report at this URL,
# and unlike the Companies House filing already cited as AR2026_URL - a scanned,
# image-only PDF that yields 79 characters from 79 pages and has to be OCR'd - this
# copy is fully TEXT-NATIVE (232,811 extracted characters). Same document, far more
# reliable to search, which is what makes the FY2026 negatives below strong rather
# than OCR-dependent.
AR2026_SITE_URL = "https://streambank.co.uk/pdf/StreamBank-PLC-Annual-Report-and-Financial-Statements.pdf"

ENTITY_NOTE = (
    "ENTITY / PERIOD NOTE: StreamBank PLC (FRN 954876, Companies House no. 11995458, "
    "LEI 213800KDQFY4NBXFKP66) is the exact PRA-authorised entity covered. It was "
    "previously named Activtrades Loans PLC until 19 July 2022. The accounting period "
    "was extended from 31 December 2022 to 31 March 2023, so the FY2023 figures cover "
    "15 months (1 January 2022 to 31 March 2023); no separate FY2022 annual period is "
    "invented. StreamBank has no subsidiaries."
)

STATEMENTS_SOURCES = (
    "Sources - StreamBank PLC standalone/entity basis; all figures £'000:\n"
    f"FY2026: StreamBank Plc Annual report and financial statements 2026 (Companies House full accounts made up to 31 March 2026, filed 31 July 2026), p.44 (Income Statement), p.45 (Statement of Comprehensive Income), p.46 (Statement of Financial Position), p.47 (Statement of Changes in Equity) - {AR2026_URL}\n"
    f"FY2025: StreamBank Plc Annual report and financial statements 2025, p.37 (Income Statement), p.38 (Statement of Comprehensive Income), p.39 (Statement of Financial Position), p.40 (Statement of Changes in Equity) - {AR2025_URL}\n"
    f"FY2024: StreamBank Plc Annual report and financial statements 2024, p.37 (Income Statement), p.39 (Statement of Financial Position) - {AR2024_URL}\n"
    f"FY2023 (15 months) and FY2021: StreamBank Plc Annual report and accounts 2023, p.36 (Income Statement), p.37 (Statement of Other Comprehensive Income), p.38 (Statement of Financial Position), p.39 (Statement of Changes in Equity) - {AR2023_URL}\n\n"
    + ENTITY_NOTE
)

CASH_FLOW_SOURCES = (
    "Sources - StreamBank PLC standalone/entity basis; all figures £'000:\n"
    f"FY2026: StreamBank Plc Annual report and financial statements 2026, p.48 (Statement of Cash Flows) - {AR2026_URL}\n"
    f"FY2025 and FY2024: StreamBank Plc Annual report and financial statements 2025, p.41 (cash flow statement) - {AR2025_URL}\n"
    f"FY2023 (15 months) and FY2021: StreamBank Plc Annual report and accounts 2023, p.40 (cash flow statement and 2021 comparative) - {AR2023_URL}\n"
    f"FY2021 filing copy: Companies House full accounts made up to 31 December 2021 - {AR2021_URL}\n\n"
    + ENTITY_NOTE
)


def p3_sources():
    return (
        "Sources - StreamBank PLC standalone regulatory basis:\n"
        f"FY2026: StreamBank Plc Annual report and financial statements 2026, Note 22 'Capital' p.78 (Ordinary "
        f"share capital 40,600.0; Accumulated losses and other reserves (8,101.9); Regulatory deductions 146.0; "
        f"Total eligible tier 1 capital (CET1) 32,644.1; Total eligible regulatory capital 32,644.1, all £'000) "
        f"and KPI page p.15 (CET1 ratio 21.6%) - {AR2026_URL}\n"
        "SITE ENUMERATION NOTE (2026-09-15) - THIS REPLACES FILENAME PERMUTATION AS THE BASIS FOR EVERY "
        "'no such document' FINDING ON THIS BANK, AND IS THE REASON THOSE FINDINGS CAN NOW BE TRUSTED. "
        "streambank.co.uk is a Laravel/Inertia single-page application: EVERY url on the domain - the homepage, "
        "/legal/, /about-us/, even /sitemap.xml - returns the same 25,989-byte HTML shell with HTTP 200 and "
        "content-type text/html, and all document links are rendered client-side, so no amount of fetching pages "
        "will reveal them and a soft-404 is indistinguishable from a real page by status code or size. Permutation "
        "against such a site can only ever fail to find; it can never prove absence. The route that does prove it: "
        "the compiled front-end bundle at https://streambank.co.uk/js/app.js (930,330 bytes) was downloaded and "
        "every '.pdf' string in it extracted. That yields the COMPLETE set of documents the site can link to, and "
        "for this bank it is exactly SIX files:\n"
        "      /pdf/StreamBank-Plc-Financial-Statements-31-March-2023-Signed.pdf   (FY2023 Annual Report)\n"
        "      /pdf/StreamBank-Plc-FY24-Live-PwC-Signed.pdf                        (FY2024 Annual Report)\n"
        "      /pdf/FY24-Pillar-3-StreamBank-PLC.pdf                               (FY2024 Pillar 3)\n"
        "      /pdf/March-2025-Annual-Report-2025.pdf                              (FY2025 Annual Report)\n"
        "      /pdf/March-2025-Pillar-3-Disclosures.pdf                            (FY2025 Pillar 3)\n"
        "      /pdf/StreamBank-PLC-Annual-Report-and-Financial-Statements.pdf      (FY2026 Annual Report)\n"
        "EXACTLY TWO PILLAR 3 DOCUMENTS EXIST, covering FY2024 and FY2025 ONLY. There is no FY2026 edition and no "
        "FY2023 edition - enumerated and absent, not merely not-found. (Wayback is no help here and its silence "
        "proves nothing: a CDX sweep of the whole domain filtered for PDFs returns only 11 captures, of which just "
        "one is a bank report - the FY2024 Annual Report - so the archive has never captured either Pillar 3 file "
        "or four of the six documents that demonstrably exist live. An absence in Wayback is not an absence on the "
        "live site.) Confirming probes on the same date: March-2026-Pillar-3-Disclosures.pdf, "
        "March-2026-Annual-Report-2026.pdf, FY26-Pillar-3-StreamBank-PLC.pdf and Pillar-3-Disclosures-2026.pdf all "
        "return the 25,989-byte soft-404, while March-2025-Pillar-3-Disclosures.pdf still returns a real 779,478-byte "
        "application/pdf from the same directory - so the absence is genuine and not a site-wide outage.\n"
        "      The enumeration also turned up a document this workbook did not have: the Bank's own copy of the "
        "FY2026 Annual Report (AR2026_SITE_URL above). It is the same report as the Companies House filing already "
        "cited, but TEXT-NATIVE (232,811 characters) rather than a 79-page scan yielding 79 characters. All the "
        "FY2026 negatives below were re-established against that native text on 2026-09-15, replacing an "
        "OCR-dependent finding with a directly-searchable one.\n"
        "FY2026 BASIS WARNING, read before comparing years: no FY2026 Pillar 3 Disclosures document has been "
        "published. The FY2026 capital figures above are therefore on ANNUAL "
        "REPORT basis, whereas FY2025 and FY2024 are on Pillar 3 (UKB KM1) basis, and the two do not agree: the "
        "FY2026 Annual Report's own FY2025 comparative is CET1 34,182.8 / CET1 ratio 24.1%, against the 35,066.3 / "
        "24.8% that the FY2025 Pillar 3 document reports and that this workbook retains for FY2025. The FY2025 "
        "figures have deliberately NOT been overwritten. Consequence: the FY2026-vs-FY2025 movement shown here "
        "(24.8% -> 21.6%) mixes the two bases and overstates the decline; the like-for-like Annual-Report-basis "
        "movement is 24.1% -> 21.6%. This mirrors how FY2023 is already sourced in this workbook (Annual Report "
        "capital note, no Pillar 3 document existing for that period).\n"
        f"FY2025 and FY2024: StreamBank Pillar 3 Disclosures 2025, p.10 (UKB KM1 key metrics), p.28 (leverage), pp.31-32 (LCR/NSFR) - {P3_2025_URL}\n"
        f"FY2024: StreamBank Pillar 3 Disclosures 2024, p.9 (UKB KM1 key metrics), pp.23-24 (leverage), pp.26-27 (LCR/NSFR) - {P3_2024_URL}\n"
        f"FY2023 (15m): StreamBank Plc Annual report and accounts 2023, 'Capital management' note, p.28 "
        f"(table marked Unaudited, giving Common Equity Tier 1 capital 32,171; Total risk weighted assets "
        f"63,586; Common Equity Tier 1 capital ratio 50.6%; Total own funds 32,171; Total capital ratio "
        f"50.6%, all £'000) - {AR2023_URL}\n"
        "FY2023 ACCESS/AVAILABILITY - UPGRADED 2026-09-15 FROM PERMUTATION TO ENUMERATION. No standalone FY2023 "
        "Pillar 3 document exists, and that is now an enumerated finding rather than a failure to guess the right "
        "filename: the site's JS bundle (see SITE ENUMERATION NOTE above) contains the complete list of six PDFs "
        "the site links to, and the only two Pillar 3 files in it are the FY2024 and FY2025 editions. StreamBank "
        "began publishing Pillar 3 disclosures with FY2024 and has never published one covering the FY2023 "
        "15-month period. Independently, the FY2024 Pillar 3 document's UKB KM1 table is single-column (FY2024 "
        "only) and carries no FY2023 comparative, so that route is closed too. The FY2023 Annual Report capital "
        "note cited above is therefore the only public source for FY2023, and it discloses capital, RWAs and "
        "ratios but NO leverage, LCR or NSFR figure - which is why those three sheets read 'Not publicly "
        "disclosed' for FY2023 rather than carrying anything.\n"
        "FY2021 STRUCTURAL: the entity (then named Activtrades Loans PLC) held no banking licence during "
        "that period - Authorisation with Restrictions was granted in June 2022 and the full licence in "
        "February 2023 (FY2023 Annual Report, pp.6 and 9) - so no Pillar 3 or regulatory-capital "
        "disclosure obligation applied and no such figures exist for FY2021.\n"
        "SDDT STATUS - CHECKED 2026-09-15 (cross-bank SDDT date-fit pass) AND DELIBERATELY NOT USED TO "
        "EXPLAIN ANY GAP HERE. StreamBank does hold the Small Domestic Deposit Taker opt-in: the Bank of "
        "England consolidated list of waivers and modifications granted to PRA-authorised firms (downloaded "
        "2026-09-15, https://www.bankofengland.co.uk/-/media/boe/files/prudential-regulation/authorisations/"
        "waivers-and-modifications-of-rules/consolidated-waivers-pra-firms.csv) carries one SDDT row for FRN "
        "954876, 'StreamBank PLC': 'Modification by Consent - PRA Rulebook- CRR Firms- Rule 3.1 of the SDDT "
        "Regime - General Application Part 3.1', rule 'SDDT Regime - General Application', sub rule 'Ru 3.1', "
        "waiver ref 'A00007820P.pdf', start date 04/05/2024, no end date. Rule 3.1 is the operative opt-in "
        "(not one of the eligibility-criteria modifications under rules 1.2 / 2.1(9) / 2.6), and it normally "
        "removes the Pillar 3 disclosure obligation outright.\n"
        "      WHY IT IS NOT APPLIED. StreamBank's accounting reference date is 31 MARCH, confirmed at "
        "Companies House (company 11995458: accounts for the period ended 31 December 2021, then 31 March "
        "2023, 2024, 2025 and 2026 - the year-end moved, which is why FY2023 is a 15-month period here). On a "
        "pure date test the modification would cover FY2025 and FY2026. But the Bank's own conduct refutes "
        "that reading: it PUBLISHED a full Pillar 3 disclosure for FY2025 - the year ended 31 March 2025, "
        "eleven months AFTER the 4 May 2024 start date - and this workbook's FY2025 and FY2024 figures are "
        "transcribed from it. A firm that had actually dropped its Pillar 3 obligation would not have "
        "produced that document, whose Board approval is dated 18 September 2025.\n"
        "      The Bank says as much itself, and in two respects contradicts the register. StreamBank Pillar 3 "
        "Disclosures 2025, p.3, 'Regulatory changes - Strong and Simple': 'In January 2025, the Bank applied, "
        "and has since been confirmed, as a SDDT regime institution. Final implementation of these changes has "
        "been delayed until 1 January 2027.' First, it dates its own application to JANUARY 2025, eight months "
        "after the register's 04/05/2024 start date - the two do not reconcile, and neither is discarded here. "
        "Second, and decisively, StreamBank states that it regards the SDDT changes as not implemented until 1 "
        "JANUARY 2027, so by its own account it remained subject to Pillar 3 disclosure throughout FY2025 and "
        "FY2026. (That 2027 date is the SDDT CAPITAL regime, which the same passage runs together with the "
        "disclosure relief; the disclosure relief itself took effect from 1 July 2024 under PS15/23. The "
        "conflation is the Bank's, not this workbook's - but what matters is that it explains why StreamBank "
        "kept disclosing.)\n"
        "      FY2026 ANNUAL REPORT - WHAT IT DOES AND DOES NOT DISCLOSE, re-established 2026-09-15 against the "
        "TEXT-NATIVE copy on the Bank's own site (AR2026_SITE_URL), which supersedes the earlier OCR-based check "
        "of the scanned Companies House filing. Exact whole-document string counts over all 232,811 characters: "
        "'SDDT' 0, 'Small Domestic' 0, 'Strong and Simple' 0, 'Pillar 3' 0, 'Pillar III' 0, 'NSFR' 0, 'net "
        "stable' 0, 'LCR' 0, 'exposure measure' 0, 'high quality liquid' 0. The handful of near-misses were all "
        "read in context and none is a disclosed figure: 'Liquidity Coverage' appears exactly once, purely "
        "qualitatively ('All liquidity levels remained well within board risk appetite and regulatory "
        "requirements throughout the year, including the Liquidity Coverage Ratio, which ensures that sufficient "
        "high-quality liquid assets are held to sustain a short term severe but plausible liquidity stress') with "
        "no number attached; 'HQLA' appears once, in a committee's list of responsibilities ('Manage the HQLA "
        "portfolio'), again with no figure; 'leverage' appears once, in the KPI table whose footnote disqualifies "
        "it (see the Leverage Ratio sheet); and 'risk weighted' appears twice, both times as a DEFINITION of the "
        "CET1 ratio ('CET1 capital divided by total risk weighted assets' and 'Regulatory Capital /Risk Weighted "
        "Assets') with no RWA amount anywhere. BEWARE A NAIVE SUBSTRING SEARCH HERE: grepping this document for "
        "'RWA' returns six hits and every single one is inside the word 'forward' or 'forward-looking' - not the "
        "acronym at all. A future pass that counts those as disclosure hits will reach the wrong conclusion. So "
        "FY2026 genuinely has a CET1 amount and a CET1 ratio and nothing else usable.\n"
        "      SO: FY2026 IS UNDETERMINED, NOT SDDT-EXEMPT. The most likely explanation is publication lag, "
        "not exemption - the FY2025 Pillar 3 was Board-approved 18 September 2025, roughly six months after "
        "its 31 March 2025 year-end, so an FY2026 equivalent would only be due around September 2026, which is "
        "exactly when the 2026-09-15 check above was run. A future pass should re-check streambank.co.uk/pdf/ "
        "for an FY2026 Pillar 3 rather than treating this cell as structurally exempt. Corroborating the "
        "absence of any exemption claim: the FY2026 Annual Report was re-checked on 2026-09-15 and contains no "
        "mention of 'SDDT', 'Small Domestic Deposit Taker', 'Strong and Simple' or 'Pillar 3' anywhere. That "
        "filing is a SCANNED, IMAGE-ONLY Companies House PDF - pdftotext extracted 79 characters from 79 pages "
        "- so it was OCR'd page-by-page at 200dpi with tesseract (185k characters recovered, 74 hits for "
        "'capital') before being searched; a plain text search would have returned a false negative.\n"
        "      WHAT THE MODIFICATION DOES NOT EXPLAIN, IN ANY READING: FY2021 and FY2023. Both pre-date "
        "04/05/2024 by years - FY2021 ended 31 December 2021 and FY2023 ended 31 March 2023 - and both already "
        "have their own established and unrelated causes set out above (no banking licence in FY2021; no "
        "standalone FY2023 Pillar 3 document ever published, with the Annual Report capital note used "
        "instead). Do not read SDDT back onto either. No cell in this workbook is changed by this finding, and "
        "StreamBank discloses no Simplified Retail Deposit Ratio value.\n\n"
        + ENTITY_NOTE
    )


bw = BankWorkbook(
    bank_name="StreamBank PLC",
    years=YEARS,
    year_label=YEAR_LABEL,
    header_color="0B4F6C",
)

balance_sheet_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and balances at central banks", {"FY2026": 26943.9, "FY2025": 38692.5, "FY2024": 32730.1}),
    ("DATA", "Cash and balances with other banks / credit institutions", {"FY2026": 6192.7, "FY2025": 7956.8, "FY2024": 8342.1, "FY2023": 14534.8, "FY2021": 100.1}),
    ("DATA", "Debt instruments at fair value through OCI", {"FY2026": 4279.1, "FY2025": 4190.0, "FY2024": 4092.2, "FY2023": 2985.5}),
    ("DATA", "Loans and advances to customers", {"FY2026": 154981.9, "FY2025": 156706.3, "FY2024": 137242.0, "FY2023": 31221.0}),
    ("DATA", "Intangible assets", {"FY2026": 82.8, "FY2025": 139.0, "FY2024": 193.8, "FY2023": 249.8, "FY2021": 222.8}),
    ("DATA", "Property, plant & equipment", {"FY2026": 74.9, "FY2025": 71.3, "FY2024": 76.1, "FY2023": 64.1}),
    ("DATA", "Deferred tax assets", {"FY2026": 2606.6, "FY2025": 1683.3, "FY2024": 2017.1, "FY2023": 1017.3, "FY2021": 125.0}),
    ("DATA", "Other assets", {"FY2026": 1188.9, "FY2025": 944.2, "FY2024": 557.9, "FY2023": 642.2}),
    ("TOTAL", "Total assets", {"FY2026": 196350.8, "FY2025": 210383.4, "FY2024": 185251.3, "FY2023": 50714.7, "FY2021": 447.9}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Deposits from customers", {"FY2026": 163123.0, "FY2025": 173512.6, "FY2024": 149625.7, "FY2023": 16632.2}),
    ("DATA", "Other liabilities", {"FY2026": 853.0, "FY2025": 1661.3, "FY2024": 1398.4, "FY2023": 644.7, "FY2021": 800.5}),
    ("TOTAL", "Total liabilities", {"FY2026": 163976.0, "FY2025": 175173.9, "FY2024": 151024.1, "FY2023": 17276.9, "FY2021": 800.5}),
    ("SECTION", "Equity", {}),
    ("DATA", "Share capital", {"FY2026": 40600.0, "FY2025": 40600.0, "FY2024": 40600.0, "FY2023": 37500.0, "FY2021": 50.0}),
    ("DATA", "Accumulated losses", {"FY2026": -8225.2, "FY2025": -5390.5, "FY2024": -6372.8, "FY2023": -4062.2, "FY2021": -402.6}),
    ("TOTAL", "Total equity", {"FY2026": 32374.8, "FY2025": 35209.5, "FY2024": 34227.2, "FY2023": 33437.8, "FY2021": -352.6}),
    ("TOTAL", "Total equity and liabilities", {"FY2026": 196350.8, "FY2025": 210383.4, "FY2024": 185251.3, "FY2023": 50714.7, "FY2021": 447.9}),
]

bw.add_balance_sheet_sheet(
    title="StreamBank Plc — Balance Sheet",
    subtitle="Standalone entity basis, £'000; FY2023 covers the 15-month transition period ended 31 March 2023; no separate FY2022 period was published",
    rows=balance_sheet_rows,
    sources_text=STATEMENTS_SOURCES + (
        "\n\nPRESENTATION NOTE: FY2025/FY2024's own report labels the cash line 'Cash balances held with "
        "other banks'; FY2023/FY2021's own report labels the equivalent line 'Loans and advances to credit "
        "institutions'. Both are combined here under one label as they cover the same underlying balance "
        "(repayable-on-demand deposits with UK banks). FY2021 had not yet begun lending or taking deposits "
        "(confirmed by that year's own Balance Sheet showing no Loans and advances to customers or Deposits "
        "from customers line at all) - blank cells for FY2021 are genuinely nil, not a data gap."
    ),
    first_col_width=64,
    source_height=260,
    unit_suffix=" (£'000)",
)

income_statement_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest receivable and similar income", {"FY2026": 19405.3, "FY2025": 19996.4, "FY2024": 8950.3, "FY2023": 2039.8}),
    ("DATA", "Interest payable and similar charges", {"FY2026": -7825.9, "FY2025": -8737.1, "FY2024": -3608.2, "FY2023": -290.0}),
    ("TOTAL", "Net interest income", {"FY2026": 11579.4, "FY2025": 11259.3, "FY2024": 5342.1, "FY2023": 1749.8}),
    ("DATA", "Other operating income/(expense)", {"FY2026": 450.4, "FY2025": 121.3, "FY2024": -96.6, "FY2023": 99.0}),
    ("TOTAL", "Net operating income", {"FY2026": 12029.8, "FY2025": 11380.6, "FY2024": 5245.5, "FY2023": 1848.8}),
    ("SECTION", "Operating expenses", {}),
    ("DATA", "Staff costs", {"FY2026": -5603.4, "FY2025": -5243.6, "FY2024": -4701.2, "FY2023": -3754.5}),
    ("DATA", "Other operating expenses", {"FY2026": -3759.7, "FY2025": -3141.0, "FY2024": -2670.9, "FY2023": -1980.4, "FY2021": -527.6}),
    ("DATA", "Impairment losses on loans and advances to customers", {"FY2026": -6414.6, "FY2025": -1678.4, "FY2024": -1201.9, "FY2023": -600.8}),
    ("DATA", "Depreciation and amortisation", {"FY2026": -99.3, "FY2025": -100.3, "FY2024": -89.6, "FY2023": -50.4}),
    # Not itself a printed AR subtotal - the sum of Staff costs + Other
    # operating expenses + Depreciation and amortisation above. Excludes
    # Impairment losses on loans and advances per standard cost-to-income
    # convention (operating costs only, not credit risk).
    ("TOTAL", "Total operating expenses (sum of Staff costs + Other operating expenses + Depreciation and amortisation - excludes impairment losses on loans and advances)",
     {"FY2026": -9462.4, "FY2025": -8484.9, "FY2024": -7461.7, "FY2023": -5785.3, "FY2021": -527.6}),
    ("TOTAL", "Profit/(Loss) before taxation", {"FY2026": -3847.2, "FY2025": 1217.3, "FY2024": -3418.1, "FY2023": -4537.4, "FY2021": -527.6}),
    ("DATA", "Tax (charge)/credit", {"FY2026": 945.5, "FY2025": -309.0, "FY2024": 1023.1, "FY2023": 892.3, "FY2021": 125.0}),
    ("TOTAL", "Profit/(Loss) for the year", {"FY2026": -2901.7, "FY2025": 908.3, "FY2024": -2395.0, "FY2023": -3645.1, "FY2021": -402.6}),
    ("SECTION", "Other comprehensive income", {}),
    ("DATA", "Fair value adjustment through OCI", {"FY2026": 89.1, "FY2025": 98.8, "FY2024": 107.7, "FY2023": -14.5}),
    ("DATA", "Deferred tax thereon", {"FY2026": -22.2, "FY2025": -24.8, "FY2024": -23.3}),
    ("TOTAL", "Total other comprehensive income", {"FY2026": 66.9, "FY2025": 74.0, "FY2024": 84.4, "FY2023": -14.5}),
    ("TOTAL", "Total comprehensive income/(expense) for the year", {"FY2026": -2834.8, "FY2025": 982.3, "FY2024": -2310.6, "FY2023": -3659.6, "FY2021": -402.6}),
]

bw.add_income_statement_sheet(
    title="StreamBank Plc — Profit & Loss",
    subtitle="Standalone entity basis, £'000; FY2023 covers the 15-month transition period ended 31 March 2023; results relate entirely to continuing operations",
    rows=income_statement_rows,
    sources_text=STATEMENTS_SOURCES + (
        "\n\nFY2021 predates the start of lending/deposit-taking operations - no interest income/expense, "
        "impairment, or OCI was disclosed for that year (confirmed by that year's own Income Statement and "
        "Statement of Other Comprehensive Income, both showing '-' for those lines); FY2021's sole cost was "
        "Other Operating expenses."
    ),
    first_col_width=64,
    source_height=260,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Statement of Changes in Equity (chronological) - built using the per-year
# reconciliation ladder: Balance Sheet built first (above), then each
# year's closing balance checked against both the next year's own opening
# balance and that year's own Balance Sheet Total equity. Ties exactly at
# every boundary - zero plug rows needed.
# ---------------------------------------------------------------
equity_changes_rows = [
    ("TOTAL", "As at 1 January 2021", (50.0, 0.0, 50.0)),
    ("DATA", "Loss for the financial year (FY2021)", (None, -527.6, -527.6)),
    ("DATA", "Other comprehensive income (FY2021)", (None, 125.0, 125.0)),
    ("TOTAL", "As at 31 December 2021", (50.0, -402.6, -352.6)),
    ("DATA", "Loss for the financial period (FY2023, 15mo)", (None, -3645.1, -3645.1)),
    ("DATA", "Fair value adjustment through OCI (FY2023)", (None, -14.5, -14.5)),
    ("DATA", "Increase in share capital (FY2023)", (37450.0, None, 37450.0)),
    ("TOTAL", "As at 31 March 2023", (37500.0, -4062.2, 33437.8)),
    ("DATA", "Loss for the financial year (FY2024)", (None, -2395.0, -2395.0)),
    ("DATA", "Other comprehensive income (FY2024)", (None, 84.4, 84.4)),
    ("DATA", "Increase in share capital (FY2024)", (3100.0, None, 3100.0)),
    ("TOTAL", "As at 31 March 2024", (40600.0, -6372.8, 34227.2)),
    ("DATA", "Profit for the financial year (FY2025)", (None, 908.3, 908.3)),
    ("DATA", "Other comprehensive income (FY2025)", (None, 74.0, 74.0)),
    ("DATA", "Increase in share capital (FY2025)", (0.0, None, 0.0)),
    ("TOTAL", "As at 31 March 2025", (40600.0, -5390.5, 35209.5)),
    ("DATA", "Loss for the financial year (FY2026)", (None, -2901.7, -2901.7)),
    ("DATA", "Other comprehensive income (FY2026)", (None, 66.9, 66.9)),
    ("DATA", "Increase in share capital (FY2026)", (0.0, None, 0.0)),
    ("TOTAL", "As at 31 March 2026", (40600.0, -8225.2, 32374.8)),
]

bw.add_equity_changes_sheet(
    title="StreamBank Plc — Statement of Changes in Equity",
    subtitle="Standalone entity basis, £'000; FY2023 row covers the 15-month transition period ended 31 "
              "March 2023. Ties exactly to the Balance Sheet's own Total equity at every year-end except "
              "FY2026, where the source itself is £0.1k out - see source note.",
    headers=["Called up share capital", "Accumulated losses", "Total"],
    rows=equity_changes_rows,
    sources_text=STATEMENTS_SOURCES + (
        "\n\nSOURCE ANOMALY, reproduced as disclosed, not silently corrected: the FY2021 row of StreamBank's "
        "own Statement of Changes in Equity (AR2023, p.39) labels a +£125.0k movement 'Other comprehensive "
        "income', but that figure exactly matches the FY2021 tax credit reported in the Income Statement "
        "(p.36), while the same year's own Statement of Other Comprehensive Income (p.37) shows nil OCI for "
        "FY2021. The 'Loss for the financial year' row used here (£527.6k) is therefore the FY2021 loss "
        "before tax, not the £402.6k loss after tax - the two figures net to the correct £402.6k movement "
        "and tie exactly to the Balance Sheet's own FY2021 Total equity, so the underlying numbers are not "
        "in question, only the source's own row labelling for that one year."
        "\n\nSECOND SOURCE ANOMALY (FY2026), reproduced as disclosed, not force-reconciled: the FY2026 Statement "
        "of Changes in Equity (AR2026, p.47) opens at Accumulated losses (5,390.4) / Total equity 35,209.6, but "
        "the FY2025 section of that same statement closes at (5,390.5) / 35,209.5, which is also what both the "
        "FY2026 and FY2025 Balance Sheets report. The £0.1k break is in the source, not in transcription - "
        "confirmed by re-rendering p.47 at 450 DPI. This workbook carries the Balance-Sheet-consistent (5,390.5) "
        "/ 35,209.5 opening, so the FY2026 movement rows (loss 2,901.7 + OCI 66.9 = 2,834.8) arithmetically "
        "imply a closing of (8,225.3) / 32,374.7 rather than the printed (8,225.2) / 32,374.8. The printed "
        "closing is used, because it is what both the FY2026 Balance Sheet and Note 22 report; the residual "
        "£0.1k is the source's own rounding, not a missing movement."
    ),
    first_col_width=76,
    source_height=260,
)

cash_flow_rows = [
    ("SECTION", "Cash flows from operating activities", {}),
    ("DATA", "Cash generated from operations", {"FY2026": -13466.0, "FY2025": 5616.8, "FY2024": 24482.0, "FY2023": 9419.8, "FY2021": 272.8}),
    ("TOTAL", "Net cash from operating activities", {"FY2026": -13466.0, "FY2025": 5616.8, "FY2024": 24482.0, "FY2023": 9419.8, "FY2021": 272.8}),
    ("SECTION", "Cash flows from investing activities", {}),
    ("DATA", "Purchase of debt instruments", {"FY2024": -1000.0, "FY2023": -3000.0}),
    ("DATA", "Disposal of debt instruments", {"FY2025": 1.0, "FY2024": 1.0}),
    ("DATA", "Additions of intangible fixed assets", {"FY2025": -1.2}),
    ("DATA", "Purchase of intangible fixed assets", {"FY2023": -57.0, "FY2021": -222.7}),
    ("DATA", "Additions of tangible fixed assets", {"FY2026": -46.7, "FY2025": -39.5, "FY2024": -45.6, "FY2023": -84.6}),
    ("DATA", "Purchase of loans and advances to customers", {"FY2023": -8343.5}),
    ("TOTAL", "Net cash from investing activities", {"FY2026": -46.7, "FY2025": -39.7, "FY2024": -1044.6, "FY2023": -11485.1, "FY2021": -222.7}),
    ("SECTION", "Cash flows from financing activities", {}),
    ("DATA", "Share issuance", {"FY2024": 3100.0, "FY2023": 16500.0, "FY2021": 37.5}),
    ("TOTAL", "Net cash from financing activities", {"FY2026": 0.0, "FY2025": 0.0, "FY2024": 3100.0, "FY2023": 16500.0, "FY2021": 37.5}),
    ("TOTAL", "Net movement in cash and cash equivalents", {"FY2026": -13512.7, "FY2025": 5577.1, "FY2024": 26537.4, "FY2023": 14434.7, "FY2021": 87.6}),
    ("DATA", "Cash and cash equivalents at beginning of year", {"FY2026": 46649.3, "FY2025": 41072.2, "FY2024": 14534.8, "FY2023": 100.1, "FY2021": 12.5}),
    ("TOTAL", "Cash and cash equivalents at end of year", {"FY2026": 33136.6, "FY2025": 46649.3, "FY2024": 41072.2, "FY2023": 14534.8, "FY2021": 100.1}),
]

bw.add_cash_flow_sheet(
    title="StreamBank PLC — Statement of Cash Flows",
    subtitle="Standalone entity basis, £'000; FY2023 covers the 15-month transition period ended 31 March 2023; no separate FY2022 period was published",
    rows=cash_flow_rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=72,
    source_height=220,
    unit_suffix=" (£'000)",
)


asset_quality_rows = [
    ("SECTION", "Loan book", {}),
    ("DATA", "Gross loans and advances to customers", {"FY2026": 165422.4, "FY2025": 160288.5, "FY2024": 139145.8, "FY2023": 31821.8}),
    ("DATA", "Less: ECL allowance", {"FY2026": -10440.5, "FY2025": -3582.2, "FY2024": -1903.8, "FY2023": -600.8}),
    ("TOTAL", "Net loans and advances to customers", {"FY2026": 154981.9, "FY2025": 156706.3, "FY2024": 137242.0, "FY2023": 31221.0}),
    ("SECTION", "Gross loan balance by IFRS 9 stage", {}),
    ("DATA", "Stage 1 (satisfactory)", {"FY2026": 102055.6, "FY2025": 97094.5, "FY2024": 118244.3}),
    ("DATA", "Stage 2 (watchlist)", {"FY2026": 8545.1, "FY2025": 21609.2, "FY2024": 9807.4}),
    ("DATA", "Stage 3 (default / credit-impaired)", {"FY2026": 54821.7, "FY2025": 41584.8, "FY2024": 11094.1}),
    ("SECTION", "ECL allowance by IFRS 9 stage", {}),
    ("DATA", "Stage 1 (12-month ECL)", {"FY2026": 310.9, "FY2025": 307.0, "FY2024": 233.0, "FY2023": 47.7}),
    ("DATA", "Stage 2 (lifetime ECL, not credit-impaired)", {"FY2026": 96.4, "FY2025": 107.0, "FY2024": 3.6, "FY2023": 0.6}),
    ("DATA", "Stage 3 (lifetime ECL, credit-impaired)", {"FY2026": 10033.2, "FY2025": 3168.2, "FY2024": 1667.2, "FY2023": 552.5}),
    ("SECTION", "Derived ratios", {}),
    ("DATA", "ECL coverage ratio (total ECL / gross loans)", {"FY2026": "6.31%", "FY2025": "2.23%", "FY2024": "1.37%", "FY2023": "1.89%"}),
    ("DATA", "Stage 3 share of gross loans (NPL ratio)", {"FY2026": "33.14%", "FY2025": "25.94%", "FY2024": "7.97%"}),
]

bw.add_asset_quality_sheet(
    title="StreamBank Plc — Asset Quality / Credit Risk Disclosures",
    subtitle="Standalone entity basis, £'000; FY2023 covers the 15-month transition period ended 31 March "
              "2023. FY2021 predates the start of lending - genuinely nil, not a data gap.",
    rows=asset_quality_rows,
    sources_text=(
        "Sources - StreamBank PLC standalone/entity basis, all figures £'000:\n"
        f"FY2026 and FY2025: StreamBank Plc Annual report and financial statements 2026, p.63 (Note 12 Loans "
        f"and advances to customers, Note 13 Impairment losses by IFRS 9 stage) and p.75 (Note 21, gross loan "
        f"balance stage roll-forward tables for March 2026 and March 2025) - {AR2026_URL}\n"
        f"FY2024 gross-by-stage: StreamBank Plc Annual report and financial statements 2026, p.75, opening "
        f"'At 31 March 2024' row of the March 2025 roll-forward (Stage 1 118,244.3; Stage 2 9,807.4; Stage 3 "
        f"11,094.1; Total 139,145.8, which ties exactly to the FY2024 gross balance above) - {AR2026_URL}\n"
        f"FY2025 and FY2024: StreamBank Plc Annual report and financial statements 2025, p.53-54 (Note 12 "
        f"Loans and advances to customers, Note 13 Impairment losses by IFRS 9 stage) - {AR2025_URL}\n"
        f"FY2023: StreamBank Plc Annual report and accounts 2023, p.51-52 (Note 11 Loans and advances to "
        f"customers, Note 12 Impairment losses by IFRS 9 stage) - {AR2023_URL}\n\n"
        + ENTITY_NOTE
        + "\n\nFY2021 had no loans and advances to customers at all (confirmed by that year's own Balance "
          "Sheet and Note 11 comparative column, both showing '-') - the Bank had not yet begun lending.\n"
          "GROSS-BY-STAGE, added 2026-09-15: the FY2026 Annual Report is the first StreamBank report to "
          "disclose the gross loan balance split by IFRS 9 stage. Its Note 21 roll-forward tables give the "
          "split at 31 March 2026, 31 March 2025 and 31 March 2024, so those three years are now populated. "
          "FY2023 remains blank - neither the FY2023 nor the FY2025 report discloses a gross-by-stage split, "
          "only the ECL allowance roll-forward. The Stage 3 share of gross loans is therefore available from "
          "FY2024 onward and is left blank for FY2023.\n"
          "Both derived ratios are calculated from the disclosed figures on the same sheet, not transcribed: "
          "ECL coverage ratio = total ECL allowance / gross loans; Stage 3 share = Stage 3 gross balance / "
          "total gross loans. (The FY2025 coverage ratio was corrected from 2.24% to 2.23% on 2026-09-15; "
          "3,582.2 / 160,288.5 = 2.2348%, which rounds down.)"
    ),
    first_col_width=64,
    source_height=220,
)


# FY2021 is marked explicitly rather than left blank. The entity (then named
# Activtrades Loans PLC) held no banking licence in that period - Authorisation
# with Restrictions came in June 2022 and the full licence in February 2023 - so
# no Pillar 3 obligation existed and no figure can ever be sourced. The reasoning
# was already written into the notes below, but the cells themselves were empty,
# which is indistinguishable from a year nobody had researched: a cross-bank
# coverage audit counted all ten as chaseable gaps. Matches build_vida.py and
# build_afin_bank.py.
PRE_LICENCE_YEARS = ["FY2021"]

# FY2026 and FY2023 gap cells are written explicitly for the same reason FY2021 is:
# a blank cell cannot be distinguished from a year nobody researched. The two labels
# are NOT interchangeable. "Not applicable" means no obligation could attach (FY2021:
# no banking licence). "Not publicly disclosed" means the obligation existed, the
# search was done, and it came back empty - which is the FY2026 and FY2023 case, both
# now established by enumerating the site's full document list rather than by guessing
# filenames (see the SITE ENUMERATION NOTE in p3_sources).
NOT_DISCLOSED = "Not publicly disclosed"
NOT_APPLICABLE = "Not applicable"


def metric(name, unit, rows_data, note=None):
    rows_data = [(label, {**{y: "Not applicable" for y in PRE_LICENCE_YEARS}, **values})
                 for label, values in rows_data]
    bw.add_metric_sheet(name, unit, rows_data, p3_sources(), note=note, first_col_width=48, source_height=180)


metric("CET1 Capital", "£'000", [("Common Equity Tier 1 (CET1) capital", {"FY2026": 32644.1, "FY2025": 35066.3, "FY2024": 32012.2, "FY2023": 32171})], "FY2026 is from the Bank's own FY2026 Annual Report Note 22 'Capital' (p.78) and KPI page (p.15), NOT from a Pillar 3 document - none has been published for FY2026. It is therefore on a different basis from FY2025/FY2024; see the source note above for the size of the difference. FY2023 (15m) from the Bank's own FY2023 Annual Report 'Capital management' note (p.28, marked unaudited) - located in the 2026-09-12 disclosure audit; no standalone FY2023 Pillar 3 document exists (see p3_sources). FY2021 is structural: the Bank held no banking licence in that period (Authorisation with Restrictions granted June 2022, full licence February 2023), so no Pillar 3 / regulatory capital disclosure obligation applied and none exists.")
metric("CET1 Ratio", "%", [("Common Equity Tier 1 (CET1) ratio", {"FY2026": "21.6%", "FY2025": "24.8%", "FY2024": "22.2%", "FY2023": "50.6%"})], "FY2026 is from the Bank's own FY2026 Annual Report Note 22 'Capital' (p.78) and KPI page (p.15), NOT from a Pillar 3 document - none has been published for FY2026. It is therefore on a different basis from FY2025/FY2024; see the source note above for the size of the difference. FY2023 (15m) from the Bank's own FY2023 Annual Report 'Capital management' note (p.28, marked unaudited) - located in the 2026-09-12 disclosure audit; no standalone FY2023 Pillar 3 document exists (see p3_sources). FY2021 is structural: the Bank held no banking licence in that period (Authorisation with Restrictions granted June 2022, full licence February 2023), so no Pillar 3 / regulatory capital disclosure obligation applied and none exists.")
metric("Tier 1 Capital", "£'000", [("Tier 1 capital", {"FY2026": 32644.1, "FY2025": 35066.3, "FY2024": 32012.2, "FY2023": 32171})], "FY2026 is from the Bank's own FY2026 Annual Report Note 22 'Capital' (p.78) and KPI page (p.15), NOT from a Pillar 3 document - none has been published for FY2026. It is therefore on a different basis from FY2025/FY2024; see the source note above for the size of the difference. FY2023's own note discloses Total own funds of £32,171k equal to its CET1 capital, i.e. no Additional Tier 1 or Tier 2 instrument was in issue at 31 March 2023, so Tier 1 = CET1 that year. FY2023 (15m) from the Bank's own FY2023 Annual Report 'Capital management' note (p.28, marked unaudited) - located in the 2026-09-12 disclosure audit; no standalone FY2023 Pillar 3 document exists (see p3_sources). FY2021 is structural: the Bank held no banking licence in that period (Authorisation with Restrictions granted June 2022, full licence February 2023), so no Pillar 3 / regulatory capital disclosure obligation applied and none exists.")
metric("Tier 1 Ratio", "%", [("Tier 1 capital ratio", {"FY2026": "21.6%", "FY2025": "24.8%", "FY2024": "22.2%", "FY2023": "50.6%"})], "FY2026 is from the Bank's own FY2026 Annual Report Note 22 'Capital' (p.78) and KPI page (p.15), NOT from a Pillar 3 document - none has been published for FY2026. It is therefore on a different basis from FY2025/FY2024; see the source note above for the size of the difference. FY2023 (15m) from the Bank's own FY2023 Annual Report 'Capital management' note (p.28, marked unaudited) - located in the 2026-09-12 disclosure audit; no standalone FY2023 Pillar 3 document exists (see p3_sources). FY2021 is structural: the Bank held no banking licence in that period (Authorisation with Restrictions granted June 2022, full licence February 2023), so no Pillar 3 / regulatory capital disclosure obligation applied and none exists.")
metric("Total Capital", "£'000", [("Total capital", {"FY2026": 32644.1, "FY2025": 35066.3, "FY2024": 32012.2, "FY2023": 32171})], "FY2026 is from the Bank's own FY2026 Annual Report Note 22 'Capital' (p.78) and KPI page (p.15), NOT from a Pillar 3 document - none has been published for FY2026. It is therefore on a different basis from FY2025/FY2024; see the source note above for the size of the difference. FY2023 is the note's own 'Total own funds' line. FY2023 (15m) from the Bank's own FY2023 Annual Report 'Capital management' note (p.28, marked unaudited) - located in the 2026-09-12 disclosure audit; no standalone FY2023 Pillar 3 document exists (see p3_sources). FY2021 is structural: the Bank held no banking licence in that period (Authorisation with Restrictions granted June 2022, full licence February 2023), so no Pillar 3 / regulatory capital disclosure obligation applied and none exists.")
metric("Total Capital Ratio", "%", [("Total capital ratio", {"FY2026": "21.6%", "FY2025": "24.8%", "FY2024": "22.2%", "FY2023": "50.6%"})], "FY2026 is from the Bank's own FY2026 Annual Report Note 22 'Capital' (p.78) and KPI page (p.15), NOT from a Pillar 3 document - none has been published for FY2026. It is therefore on a different basis from FY2025/FY2024; see the source note above for the size of the difference. FY2023 (15m) from the Bank's own FY2023 Annual Report 'Capital management' note (p.28, marked unaudited) - located in the 2026-09-12 disclosure audit; no standalone FY2023 Pillar 3 document exists (see p3_sources). FY2021 is structural: the Bank held no banking licence in that period (Authorisation with Restrictions granted June 2022, full licence February 2023), so no Pillar 3 / regulatory capital disclosure obligation applied and none exists.")
metric("Total RWAs", "£'000", [("Risk-weighted exposure amounts", {"FY2026": NOT_DISCLOSED, "FY2025": 141336.1, "FY2024": 143947.0, "FY2023": 63586})], "FY2026 IS DELIBERATELY BLANK: no FY2026 Pillar 3 Disclosures document has been published (verified 2026-09-15), and the FY2026 Annual Report discloses no figure for this metric - its Note 22 'Capital' gives eligible capital amounts only, with no risk-weighted assets, leverage exposure, LCR or NSFR anywhere in the document. Nothing here is derived or back-solved from the CET1 ratio. FY2023 ties internally: £32,171k CET1 / £63,586k RWA = 50.6%, the ratio the same note states. FY2023 (15m) from the Bank's own FY2023 Annual Report 'Capital management' note (p.28, marked unaudited) - located in the 2026-09-12 disclosure audit; no standalone FY2023 Pillar 3 document exists (see p3_sources). FY2021 is structural: the Bank held no banking licence in that period (Authorisation with Restrictions granted June 2022, full licence February 2023), so no Pillar 3 / regulatory capital disclosure obligation applied and none exists.")
rwa_breakdown_rows = [
    ("SECTION", "Risk-weighted exposure amounts (UK OV1)", {}),
    ("DATA", "Credit risk (excluding CCR)", {"FY2026": NOT_DISCLOSED, "FY2025": 123094.2, "FY2024": 126646.0, "FY2023": NOT_DISCLOSED, "FY2021": NOT_APPLICABLE}),
    ("DATA", "Operational risk", {"FY2026": NOT_DISCLOSED, "FY2025": 18241.9, "FY2024": 17301.0, "FY2023": NOT_DISCLOSED, "FY2021": NOT_APPLICABLE}),
    ("TOTAL", "Total risk-weighted exposure amount", {"FY2026": NOT_DISCLOSED, "FY2025": 141336.1, "FY2024": 143947.0, "FY2023": 63586, "FY2021": NOT_APPLICABLE}),
]

bw.add_rwa_breakdown_sheet(
    title="StreamBank Plc — RWA Breakdown",
    subtitle="Standalone regulatory basis, £'000; not publicly disclosed for FY2026, FY2023 (15m) or FY2021 - see source note.",
    rows=rwa_breakdown_rows,
    sources_text=p3_sources() + (
        "\n\nFY2026 is blank because no FY2026 Pillar 3 Disclosures document has been published yet (verified "
        "2026-09-15); the FY2026 Annual Report contains no risk-weighted asset figure of any kind, let alone "
        "a UK OV1 breakdown. Expect this column to become fillable when the FY2026 Pillar 3 document appears.\n"
        "StreamBank's Pillar 3 Disclosures document is only published from FY2024 onward; no standalone "
        "Pillar 3 report covering the FY2023 (15-month) or FY2021 periods was found on the Bank's own site "
        "or via Wayback Machine - a genuine access/non-existence gap, consistent with the pre-existing "
        "Total RWAs and capital ratio sheets, which mark those two periods 'Not publicly disclosed'."
    ),
    first_col_width=54,
    source_height=200,
)

metric("Leverage Ratio", "%", [("Leverage ratio excluding claims on central banks (CRR basis)", {"FY2026": NOT_DISCLOSED, "FY2025": "20.4%", "FY2024": "21.0%", "FY2023": NOT_DISCLOSED}),
                               ("Leverage ratio including claims on central banks (CRR basis)", {"FY2026": NOT_DISCLOSED, "FY2025": "16.6%", "FY2024": "17.3%", "FY2023": NOT_DISCLOSED}),
                               ("Memo - Annual Report 'Leverage ratio' KPI, defined as CET1 capital / liabilities (NOT a CRR leverage ratio - do not compare)", {"FY2026": "19.2%", "FY2025": "19.5%", "FY2024": NOT_DISCLOSED, "FY2023": "182.3%"})], "THREE ROWS, TWO COMPLETELY DIFFERENT MEASURES - READ THE ROW LABELS BEFORE COMPARING ANYTHING. Rows 1 and 2 are the real CRR leverage ratio (Tier 1 capital divided by the total leverage exposure measure), taken from the UKB KM1/leverage templates of the FY2024 and FY2025 Pillar 3 documents, which are the only two Pillar 3 editions StreamBank has ever published. Row 3 is a MEMO row carrying a completely different statistic that the Bank happens to headline in its Annual Reports under the same words, and it must never be spliced into rows 1 or 2.\n"
       "WHY ROW 3 IS QUARANTINED: the FY2026 Annual Report's KPI table (p.15) prints \"Leverage ratio 19.2%\" (FY2025 comparative 19.5%), and the FY2023 Annual Report (p.11) prints \"Leverage ratio 182.3%\" - but each report's own footnote defines the measure as \"CET1 capital divided by liabilities\" (FY2023's footnote 2: \"Common equity Tier 1 capital divided by liabilities\"). That is capital over LIABILITIES, not capital over a regulatory exposure measure, and it is not a CRR ratio at all. The FY2023 figure of 182.3% is the giveaway - a leverage ratio above 100% is arithmetically impossible on the CRR definition, and it arises here only because at 31 March 2023 the Bank had £32.2m of capital against £17.3m of liabilities, having been capitalised well ahead of taking deposits. The figures are preserved on row 3 rather than discarded, because they are genuine disclosures and a reader is entitled to see them, but they are labelled so they cannot be mistaken for the CRR series. Carrying them on rows 1-2 would have shown StreamBank's leverage ratio leaping from 21.0% to 19.2% between FY2024 and FY2026 on a silently-changed definition.\n"
       "ROWS 1-2, FY2026: 'Not publicly disclosed'. No FY2026 Pillar 3 Disclosures document has been published - an ENUMERATED finding as of 2026-09-15, not a failed guess: the site's JS bundle lists the complete set of six PDFs it links to and only two are Pillar 3 files, covering FY2024 and FY2025 (see the SITE ENUMERATION NOTE in the source citation). The FY2026 Annual Report contains no CRR leverage ratio and no exposure measure either - a whole-document search of the text-native copy returns zero occurrences of 'exposure measure' and exactly one of 'leverage', the disqualified KPI above. Nothing is derived or back-solved from the CET1 ratio.\n"
       "ROWS 1-2, FY2023: 'Not publicly disclosed' for the same enumerated reason - StreamBank began publishing Pillar 3 disclosures with FY2024 and none covers the FY2023 15-month period, and the FY2023 Annual Report's capital note gives capital, RWAs and ratios but no leverage exposure measure.\n"
       "Row 2 exists because the Pillar 3 documents report BOTH bases and this workbook should not hide one: the excluding-central-bank-claims ratio is the headline (20.4% / 21.0%) and the including-claims ratio is lower (16.6% / 17.3%). Do not compare row 1 against another bank's including-claims figure or vice versa.\n"
       "FY2021 is structural on every row - no banking licence was held in that period.")
metric("LCR", "%", [("Liquidity Coverage Ratio", {"FY2026": NOT_DISCLOSED, "FY2025": "9081.1%", "FY2024": "54235.0%", "FY2023": NOT_DISCLOSED})], "FY2026 IS DELIBERATELY BLANK: no FY2026 Pillar 3 Disclosures document has been published (verified 2026-09-15), and the FY2026 Annual Report discloses no figure for this metric - its Note 22 'Capital' gives eligible capital amounts only, with no risk-weighted assets, leverage exposure, LCR or NSFR anywhere in the document. Nothing here is derived or back-solved from the CET1 ratio. Not publicly disclosed for FY2023 (15m) - the FY2023 Annual Report's capital note gives CET1/RWA/ratios only, with no LCR figure, and no standalone FY2023 Pillar 3 document exists. FY2021 is structural (no banking licence held). The source rounds the FY2025 table presentation to 9,081% in one location and reports 9,081.1% in UKB KM1; the latter is retained here.")
metric("NSFR", "%", [("Net Stable Funding Ratio", {"FY2026": NOT_DISCLOSED, "FY2025": "171.6%", "FY2024": "223.8%", "FY2023": NOT_DISCLOSED})], "FY2026 IS DELIBERATELY BLANK: no FY2026 Pillar 3 Disclosures document has been published (verified 2026-09-15), and the FY2026 Annual Report discloses no figure for this metric - its Note 22 'Capital' gives eligible capital amounts only, with no risk-weighted assets, leverage exposure, LCR or NSFR anywhere in the document. Nothing here is derived or back-solved from the CET1 ratio. Not publicly disclosed for FY2023 (15m) - the FY2023 Annual Report's capital note gives CET1/RWA/ratios only, with no NSFR figure, and no standalone FY2023 Pillar 3 document exists. FY2021 is structural (no banking licence held).")
metric("MREL Ratio", None, [("MREL ratio", {y: "Not publicly disclosed" for y in YEARS})], "No quantitative MREL ratio was found in the annual reports or Pillar 3 disclosures reviewed. StreamBank states it is assigned to the Modified Insolvency resolution category.")

bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {"FY2026": 196350.8, "FY2025": 210383.4, "FY2024": 185251.3, "FY2023": 50714.7, "FY2021": 447.9}),
        ("Loans and advances to customers", {"FY2026": 154981.9, "FY2025": 156706.3, "FY2024": 137242.0, "FY2023": 31221.0}),
        ("Deposits from customers", {"FY2026": 163123.0, "FY2025": 173512.6, "FY2024": 149625.7, "FY2023": 16632.2}),
        ("Total equity", {"FY2026": 32374.8, "FY2025": 35209.5, "FY2024": 34227.2, "FY2023": 33437.8, "FY2021": -352.6}),
    ],
    balance_sheet_unit="£'000",
    income_statement_totals=[
        ("Net interest income", {"FY2026": 11579.4, "FY2025": 11259.3, "FY2024": 5342.1, "FY2023": 1749.8}),
        ("Total operating expense", {"FY2026": -15877.0, "FY2025": -10163.3, "FY2024": -8663.6, "FY2023": -6386.1, "FY2021": -527.6}),
        ("Profit/(Loss) for the year", {"FY2026": -2901.7, "FY2025": 908.3, "FY2024": -2395.0, "FY2023": -3645.1, "FY2021": -402.6}),
    ],
    income_statement_unit="£'000",
    equity_changes_totals=[
        ("Opening equity", {"FY2026": 35209.5, "FY2025": 34227.2, "FY2024": 33437.8, "FY2023": -352.6, "FY2021": 50.0}),
        ("Total comprehensive income/(loss) for the year", {"FY2026": -2834.8, "FY2025": 982.3, "FY2024": -2310.6, "FY2023": -3659.6, "FY2021": -402.6}),
        ("Other equity movements, net", {"FY2026": 0.0, "FY2025": 0.0, "FY2024": 3100.0, "FY2023": 37450.0, "FY2021": 0.0}),
        ("Closing equity", {"FY2026": 32374.8, "FY2025": 35209.5, "FY2024": 34227.2, "FY2023": 33437.8, "FY2021": -352.6}),
    ],
    equity_changes_unit="£'000",
    cash_flow_totals=[
        ("Net cash from operating activities", {"FY2026": -13466.0, "FY2025": 5616.8, "FY2024": 24482.0, "FY2023": 9419.8, "FY2021": 272.8}),
        ("Net cash from investing activities", {"FY2026": -46.7, "FY2025": -39.7, "FY2024": -1044.6, "FY2023": -11485.1, "FY2021": -222.7}),
        ("Net cash from financing activities", {"FY2026": 0.0, "FY2025": 0.0, "FY2024": 3100.0, "FY2023": 16500.0, "FY2021": 37.5}),
        ("Cash and cash equivalents at end of year", {"FY2026": 33136.6, "FY2025": 46649.3, "FY2024": 41072.2, "FY2023": 14534.8, "FY2021": 100.1}),
    ],
    cash_flow_unit="£'000",
    ratios=[
        ("CET1 Ratio", {"FY2026": "21.6%", "FY2025": "24.8%", "FY2024": "22.2%", "FY2023": "50.6%"}),
        ("Tier 1 Ratio", {"FY2026": "21.6%", "FY2025": "24.8%", "FY2024": "22.2%", "FY2023": "50.6%"}),
        ("Total Capital Ratio", {"FY2026": "21.6%", "FY2025": "24.8%", "FY2024": "22.2%", "FY2023": "50.6%"}),
        ("Leverage Ratio (CRR, excl. central bank claims)", {"FY2026": NOT_DISCLOSED, "FY2025": "20.4%", "FY2024": "21.0%", "FY2023": NOT_DISCLOSED, "FY2021": NOT_APPLICABLE}),
        ("LCR", {"FY2026": NOT_DISCLOSED, "FY2025": "9081.1%", "FY2024": "54235.0%", "FY2023": NOT_DISCLOSED, "FY2021": NOT_APPLICABLE}),
        ("NSFR", {"FY2026": NOT_DISCLOSED, "FY2025": "171.6%", "FY2024": "223.8%", "FY2023": NOT_DISCLOSED, "FY2021": NOT_APPLICABLE}),
    ],
    note="Coverage is FY2021, FY2023 (15-month transition period), FY2024, FY2025 and FY2026. FY2026 was added on 2026-09-15 from the Annual report and financial statements 2026 (Companies House full accounts made up to 31 March 2026, filed 31 July 2026). IMPORTANT for FY2026: the four statement sheets and Asset Quality are complete, but the capital metrics come from that report's Note 22 'Capital' rather than a Pillar 3 document, because no FY2026 Pillar 3 report has been published yet - a different basis from FY2025/FY2024 (the FY2026 report's own FY2025 comparative is CET1 34,182.8 / 24.1%, against the Pillar 3 35,066.3 / 24.8% retained here), so read the FY2026-vs-FY2025 capital movement with that in mind. FY2026 Total RWAs, RWA Breakdown, Leverage Ratio, LCR and NSFR read 'Not publicly disclosed' (they previously sat blank, which is indistinguishable from an unresearched year) because the FY2026 Annual Report discloses none of them and nothing was derived. THAT ABSENCE IS NOW ENUMERATED, NOT GUESSED AT (2026-09-15): streambank.co.uk is a single-page app where every URL returns the same 25,989-byte shell, so filename permutation could never prove anything; instead the compiled JS bundle at /js/app.js was downloaded and every PDF path in it extracted, giving the complete set of six documents the site links to - of which EXACTLY TWO are Pillar 3 files, covering FY2024 and FY2025 only. There is no FY2026 and no FY2023 Pillar 3 edition. That enumeration also surfaced a text-native copy of the FY2026 Annual Report on the Bank's own site, which replaced the OCR of the scanned Companies House filing as the basis for these negatives. NOTE THE LEVERAGE RATIO SHEET CARRIES THREE ROWS: the Annual Reports headline a \"Leverage ratio\" (FY2026 19.2%, FY2023 182.3%) that their own footnotes define as \"CET1 capital divided by liabilities\" - not a CRR ratio at all, as the impossible FY2023 figure above 100% makes plain - so those are quarantined on a clearly-labelled memo row and the CRR rows stay blank for those years. StreamBank is NOT treated as SDDT-exempt despite holding the Rule 3.1 modification (waiver ref A00007820P.pdf, start 04/05/2024, no end date, confirmed against a fresh download of the PRA register on 2026-09-15): on a pure date test it would cover FY2025 and FY2026, but the Bank published a full Pillar 3 disclosure for FY2025 anyway (Board-approved 18 September 2025, eleven months after the start date) and states in that document that it regards the changes as \"delayed until 1 January 2027\". FY2026's gap is therefore most likely publication lag - the FY2025 edition appeared about six months after its year-end, so an FY2026 equivalent would only be due around September 2026 - and is worth ONE re-check rather than being closed as structural. The FY2026 report is also the first to split gross loans by IFRS 9 stage, so the Asset Quality sheet now carries that split for FY2024-FY2026. FY2022 is intentionally absent because the accounting period was extended to 31 March 2023. Blank metric cells mean not publicly disclosed, not zero. FY2023 capital/RWA/ratio figures were added in the 2026-09-12 disclosure audit from the Bank's own FY2023 Annual Report capital note (unaudited); FY2023 leverage/LCR/NSFR remain genuinely undisclosed, and FY2021 predates the Bank's banking licence entirely (Authorisation with Restrictions June 2022, full licence February 2023) so no regulatory metrics exist for it. Sources are entity-level; wider group data was not substituted.",
)

bw.save("/Users/armaan/code/katalysis/banks/STREAMBANK FINANCIALS.xlsx")
