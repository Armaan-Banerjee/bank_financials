import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook


# CUKL, company 11283101, FRN 124579.  The company applies the FRS 101
# IAS 7 exemption, so no statutory cash-flow statement is available (see
# EXEMPTION_NOTE). Every other sheet now runs FY2019-FY2025.
#
# CORRECTION (2026-09-16, KM1-010 latest-edition check). Earlier versions of
# this script stated that "no standalone CUKL Pillar 3 report exists for
# FY2024", reasoning from Citi's own filename scheme: the predicted
# b3p3d241231_uk.pdf returns "asset does not exist" while the FY2023
# equivalent still serves. That inference was WRONG. Citi CHANGED the naming
# convention after FY2023. Both documents exist and are linked from the same
# regulatory-filings index this script already cites:
#     .../public/cukl-pillar-3-disclosures-2024 .pdf   <- note the SPACE
#     .../public/cukl-pillar-3-disclosures-2025.pdf       before ".pdf"
# The index page is a JSON-driven listing; the FY2024/FY2025 entries carry
# entityName "Citibank UK Limited" and never appear as a b3p3d* path, which
# is why a filename-pattern search missed them. A 404 on a PREDICTED URL is
# evidence about the prediction, not about the bank. FY2024 is now fully
# populated from its own Pillar 3, and FY2025 is a new column across every
# sheet (Pillar 3 December 2025 + the audited FY2025 financial statements,
# signed 24 April 2026).
#
# FY2018 is deliberately NOT included, despite HD-056 naming FY2018 as
# CUKL's "confirmed floor": CUKL (formerly Citi Marble Arch Limited) was
# incorporated 29 March 2018 and filed DORMANT COMPANY ACCOUNTS for FY2018
# (Companies House, filed 27 Sep 2019) showing net assets of GBP 1 and no
# income statement - it held no PRA/FCA authorisation (granted 17 May 2019)
# and had transacted no business of any kind. This was verified by reading
# the actual FY2018 filing, not assumed from the earlier scan's domain
# signal. There is therefore no genuine FY2018 figure to transcribe for
# any line on any sheet; FY2019 (the year the retail business was actually
# transferred in and CUKL began trading, per its own FY2019/FY2020 accounts)
# is the true earliest year with real financial substance, and is the new
# floor added by this pass. See CH_2018_DORMANT_URL below.
YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021", "FY2020", "FY2019"]
YEAR_LABEL = {y: y for y in YEARS}

P3_2025_URL = "https://www.citigroup.com/rcs/citigpa/storage/public/cukl-pillar-3-disclosures-2025.pdf"
# The FY2024 file genuinely has a space before ".pdf" in its published path.
P3_2024_URL = "https://www.citigroup.com/rcs/citigpa/storage/public/cukl-pillar-3-disclosures-2024%20.pdf"
P3_2022_URL = "https://www.citigroup.com/rcs/citigpa/storage/public/b3p3d221231_uk.pdf"
P3_2021_URL = "https://www.citigroup.com/rcs/citigpa/akpublic/storage/public/b3p3d211231_uk.pdf"
P3_2023_URL = "https://www.citigroup.com/rcs/citigpa/storage/public/b3p3d231231_uk.pdf"
P3_2020_URL = "https://www.citigroup.com/rcs/citigpa/storage/public/b3p3d201231_uk.pdf"
P3_2019_URL = "https://www.citigroup.com/rcs/citigpa/storage/public/b3p3d191231_uk.pdf"
FS_2025_URL = "https://www.citigroup.com/rcs/citigpa/storage/public/citibank-uk-limited-annual-fs-2025.pdf"
FS_2024_URL = "https://www.citigroup.com/rcs/citigpa/storage/public/citibank-uk-limited-annual-fs-2024.pdf"
CH_2022_URL = "https://find-and-update.company-information.service.gov.uk/company/11283101/filing-history/MzM3OTI1NDA3NWFkaXF6a2N4/document?format=pdf&download=0"
CH_2020_URL = "https://find-and-update.company-information.service.gov.uk/company/11283101/filing-history/MzMwODEyNzk0NGFkaXF6a2N4/document?format=pdf&download=0"
CH_2019_URL = "https://find-and-update.company-information.service.gov.uk/company/11283101/filing-history/MzI3NDY5NDc2MWFkaXF6a2N4/document?format=pdf&download=0"
CH_2018_DORMANT_URL = "https://find-and-update.company-information.service.gov.uk/company/11283101/filing-history/MzI0NTI2MzExOWFkaXF6a2N4/document?format=pdf&download=0"
CH_URL = "https://find-and-update.company-information.service.gov.uk/company/11283101/filing-history"
REG_URL = "https://www.citigroup.com/global/investors/other-regulatory-filings"

STATEMENTS_SOURCES = (
    "Sources - Citibank UK Limited's own audited Annual Report and Financial Statements, transcribed from each "
    "year's own filing (not a later year's comparative column):\n"
    f"FY2025: Annual Financial Statements 2025 (approved by the Board 24 April 2026), Income Statement/Statement "
    f"of Comprehensive Income p.23, Statement of Financial Position p.24, Statement of Changes in Equity p.25 "
    f"(text-native PDF) - {FS_2025_URL}\n"
    f"FY2024: Annual Financial Statements 2024, Income Statement/Statement of Comprehensive Income p.22, Statement "
    f"of Financial Position p.23, Statement of Changes in Equity p.24 (text-native PDF) - {FS_2024_URL}\n"
    f"FY2023: FY2023 comparative column in the same FY2024 document above (same pages) - {FS_2024_URL}\n"
    f"FY2022: Annual Report and Financial Statements for the year ended 31 December 2022 (Companies House filing, "
    f"scanned/image-only, visually transcribed), Income Statement/Statement of Comprehensive Income p.23, Statement "
    f"of Financial Position p.24, Statement of Changes in Equity p.25 - {CH_2022_URL}\n"
    f"FY2021: FY2021 comparative column in the same FY2022 Companies House filing above (same pages, including the "
    f"1 January 2021 opening equity balance) - {CH_2022_URL}\n"
    f"FY2020: Annual Report and Financial Statements for the year ended 31 December 2020 (Companies House filing, "
    f"text-native), Income Statement p.22, Statement of Comprehensive Income p.23, Statement of Financial Position "
    f"p.24, Statement of Changes in Equity p.25 - {CH_2020_URL}\n"
    f"FY2019: Annual Report and Financial Statements for the year ended 31 December 2019 (Companies House filing, "
    f"text-native, CUKL's own first full-year filing after commencing trading - see ENTITY NOTE below), Income "
    f"Statement p.18, Statement of Comprehensive Income p.19, Statement of Financial Position p.20, Statement of "
    f"Changes in Equity p.21 (opening balance at 1 January 2019 is nil across every equity component, reflecting "
    f"CUKL's dormant FY2018) - {CH_2019_URL}\n"
    + "ENTITY NOTE: Citibank UK Limited (CUKL), Companies House company 11283101 and FRN 124579, is the UK legal "
    "entity covered here - not Citibank N.A. London Branch or Citibank Europe plc. CUKL's Total liabilities line "
    "on its own Statement of Financial Position combines actual liabilities with Reserves and the Profit and loss "
    "account (i.e. equity is presented within the same total as liabilities, not as a separate 'Total liabilities "
    "and equity' line) - reproduced here as the Bank's own statutory format presents it; Total assets still ties "
    "exactly to this combined Total liabilities figure every year."
)

ENTITY_NOTE = (
    "ENTITY NOTE: Citibank UK Limited (CUKL), Companies House company 11283101 and FRN 124579, is the UK legal "
    "entity covered here. CUKL's official Pillar 3 disclosures state that it has no subsidiaries and that the "
    "disclosures are prepared on a stand-alone basis. This is not Citibank N.A. London Branch or Citibank Europe plc. "
    "CUKL (formerly Citi Marble Arch Limited) was incorporated 29 March 2018 and was a dormant shell with GBP 1 net "
    "assets throughout FY2018 (Companies House dormant company accounts, filed 27 Sep 2019) - "
    f"{CH_2018_DORMANT_URL}. It was authorised by the PRA/FCA on 17 May 2019, and the Global Consumer Bank retail "
    "business (previously serviced out of Citibank Europe Plc UK branch and Citibank N.A. London Branch) was "
    "transferred to CUKL on 16 September 2019, per CUKL's own FY2019 and FY2020 accounts. FY2019 is therefore the "
    "earliest year with any real financial substance; FY2018 is not populated on any sheet in this workbook."
)

P3_SOURCES = (
    "Sources - official Citibank UK Limited standalone Pillar 3 disclosures, UK KM1 and related tables:\n"
    f"FY2025: CUKL Pillar 3 Disclosures December 2025, Table 1 (UK KM1) p.4 and Table 4 (UK OV1) p.9 - "
    f"{P3_2025_URL}\n"
    f"FY2024: CUKL Pillar 3 Disclosures December 2024, Table 1 (UK KM1) p.4 and Table 4 (UK OV1) p.9 - "
    f"{P3_2024_URL}\n"
    f"FY2024 CORRECTION (2026-09-16): this workbook previously recorded that NO standalone CUKL Pillar 3 report "
    f"existed for FY2024, and populated only three FY2024 cells from the audited accounts. That was wrong, and "
    f"the reasoning behind it is worth stating so it is not repeated: the earlier check predicted the document's "
    f"URL from Citi's own filename scheme (b3p3d<YYMMDD>_uk.pdf), found that b3p3d241231_uk.pdf returned 'asset "
    f"does not exist' while the FY2023 equivalent still served, and read that as a non-publication. Citi in fact "
    f"CHANGED the naming convention after FY2023 - the FY2024 and FY2025 reports are published as "
    f"cukl-pillar-3-disclosures-2024 .pdf (the space before '.pdf' is in the real path) and "
    f"cukl-pillar-3-disclosures-2025.pdf, both linked from the same regulatory-filings index already cited "
    f"below under entityName 'Citibank UK Limited'. A 404 on a PREDICTED filename is evidence about the "
    f"prediction, not about the bank. Every FY2024 Pillar 3 cell in this workbook now comes from CUKL's own "
    f"FY2024 Pillar 3 document.\n"
    f"FY2023: CUKL Pillar 3 Disclosures December 2023, pp. 3-5 and 8 - {P3_2023_URL}\n"
    f"FY2022: CUKL Pillar 3 Disclosures December 2022, Table 1 (UK KM1) p.5 - {P3_2022_URL}. That PDF's text "
    f"layer is broken (subset fonts with no Unicode mapping, so pdftotext and PyMuPDF both return only page "
    f"numbers and bullet glyphs); its KM1 was read by OCR of the rendered page at 300 dpi and every figure was "
    f"cross-checked against the FY2023 edition's own FY2022 comparative column, which agrees on all 26 rows "
    f"except row 9 (0.13% in the FY2022 edition, 0.1% in the FY2023 edition's comparative - a precision "
    f"difference, not a restatement). The FY2022-edition value is the one used.\n"
    f"FY2021: CUKL Pillar 3 Disclosures December 2021, pp. 6 and 15 - {P3_2021_URL}\n"
    f"FY2020: CUKL Pillar 3 Disclosures December 2020, Table 1 (KM1) p.5 - {P3_2020_URL}\n"
    f"FY2019: CUKL Pillar 3 Disclosures December 2019 (CUKL's first Pillar 3 disclosure, no comparatives - see "
    f"note below), Table 1 (KM1) p.5 - {P3_2019_URL}\n"
    f"Regulatory filing index: {REG_URL}\n"
    + ENTITY_NOTE + "\n\n"
    "MREL NOTE: the FY2019 report states MREL was introduced as an internal CUKL requirement effective 1 January "
    "2020 and that the Bank of England set it equal to CUKL's minimum capital requirement; no MREL-eligible debt "
    "had been issued as at FY2019 or FY2020, consistent with later years - no numeric MREL ratio is disclosed for "
    "any year. Re-confirmed in the FY2024 and FY2025 reports, which repeat the same sentence verbatim ('No MREL "
    "eligible debt was issued for CUKL as of 31 December 2024' / '...2025').\n\n"
    "LATEST-EDITION CHECK, 2026-09-16: read off Citi's own regulatory-filings index "
    f"({REG_URL}), not from the URLs previously cited here. The newest CUKL documents published are the Pillar 3 "
    "Disclosures December 2025 and the Annual Financial Statements 2025 (Board-approved 24 April 2026); no "
    "FY2026 document of either kind exists yet, which is expected for a 31 December year-end. Both FY2025 "
    "documents, and the previously-missed FY2024 Pillar 3, were downloaded and verified live (HTTP 200, "
    "Content-Type application/pdf, %PDF magic bytes). This check moved the workbook forward a full year and "
    "filled a year that had been recorded as a non-publication."
)

EXEMPTION_NOTE = (
    "FRS 101 CASH-FLOW EXEMPTION: CUKL's 2024 audited financial statements state that the Company has taken the "
    "FRS 101 exemption from the requirements of IAS 7 Statement of cash flows (note 1, p. 25). The same reduced-"
    "disclosure basis is consistent with the standalone Pillar 3 reports. The 2024 accounts also state that capital "
    f"management is explained in CUKL's Basel Pillar 3 disclosures. Source: {FS_2024_URL}. Companies House filing "
    f"history for company 11283101 confirms the 2024 accounts were filed on 30 May 2025: {CH_URL}."
)

ASSET_QUALITY_SOURCES = (
    "Sources - Citibank UK Limited's own Note 12 (Risk management / Credit Risk):\n"
    f"FY2025: Annual Financial Statements 2025, Statement of Financial Position p.24 and Note 12.2 Credit Risk, "
    f"'Expected credit loss' tables pp.52-53 - {FS_2025_URL}. CUKL's customer loan book is NIL at 31 December "
    f"2025 (the Statement of Financial Position prints a dash on that line), following the wind-down of its "
    f"Consumer and Wealth services; the FY2025 accounts accordingly drop the 'Loans and advances to customers' "
    f"ECL table altogether and disclose ECL only for loans and advances to banks (£34k), cash and balances at "
    f"central banks (£3k) and other financial assets (£19k) - none of which is the customer loan book this "
    f"sheet tracks. The stage-split and ECL rows are therefore BLANK for FY2025 rather than set to zero: the "
    f"bank published no customer-loan stage table for that year.\n"
    f"FY2024/FY2023: Annual Financial Statements 2024, Note 12.2 Credit Risk, 'Expected credit loss' tables "
    f"(loans and advances to customers) p.58 - {FS_2024_URL}\n"
    f"FY2022/FY2021: Annual Report and Financial Statements for the year ended 31 December 2022, Note 12.2 Credit "
    f"Risk, 'Risk Ratings' classifiably-managed exposure table (by Obligor Risk Rating stage) p.58 - {CH_2022_URL}\n"
    f"FY2020: Annual Report and Financial Statements for the year ended 31 December 2020, Note 12.2 Credit Risk, "
    f"'Loans and advances to customers' IFRS 9 stage-by-stage exposure/ECL movement table (b), p.60 - {CH_2020_URL}\n"
    f"FY2019: Annual Report and Financial Statements for the year ended 31 December 2019 (CUKL's own filing, not "
    f"the FY2020 filing's comparative column), Note 13.2 Credit Risk, 'Loans and advances to customers' IFRS 9 "
    f"stage-by-stage exposure/ECL movement table (b), p.50 - {CH_2019_URL}\n"
    + ENTITY_NOTE + "\n\n"
    "DISCLOSURE BASIS NOTE: CUKL's loan book is negligible relative to its balance sheet (a wholesale/treasury "
    "bank whose main assets are cash at central banks, treasury bills, and interbank placements) and its own ECL "
    "allowances on every asset class are correspondingly tiny (well under £0.1m in every year shown). FY2024/FY2023 "
    "use the Bank's own IFRS 9 stage-by-stage ECL movement table for 'Loans and advances to customers' (note "
    "12.2(b)). FY2022/FY2021 instead use the Bank's own 'Risk Ratings' classifiably-managed exposure table, which "
    "only breaks out the CRE (commercial real estate) loan component of the customer loan book by stage - the "
    "remainder of FY2022/FY2021's customer loans (Margin and Securities Backed Finance, a delinquency-managed "
    "retail product per the Bank's own note) is not broken out by IFRS 9 stage in either source document, so the "
    "'Loans and advances to customers, net' row for FY2022/FY2021 is the Balance Sheet's own total (not just the "
    "CRE component) while the stage split beneath it covers CRE only - documented, not blended or backfilled.\n\n"
    "FY2020/FY2019 use a THIRD basis: like FY2024/FY2023, their own Note 12.2/13.2 'Loans and advances to "
    "customers' IFRS 9 stage-by-stage table covers the FULL customer loan book (not just CRE) and reconciles "
    "exactly to the Balance Sheet's net figure every year (e.g. FY2020: 355,233 gross - 1,485 ECL = 353,748 net; "
    "FY2019: 579,400 gross - 551 ECL = 578,849 net). The narrower CRE-only stage split is specific to the "
    "FY2021/FY2022 Companies House filing's own note structure, not a general pattern across all years."
)

RWA_SOURCES = (
    "Sources - official Citibank UK Limited standalone Pillar 3 disclosures, Table 'Overview of risk weighted "
    "exposure amounts (UK OV1)':\n"
    f"FY2025: CUKL Pillar 3 Disclosures December 2025, Table 4 (UK OV1), printed p.9 - {P3_2025_URL}\n"
    f"FY2024: CUKL Pillar 3 Disclosures December 2024, Table 4 (UK OV1), printed p.9 - {P3_2024_URL} (this "
    f"year was previously blank on this sheet in the mistaken belief that no FY2024 Pillar 3 existed - see the "
    f"correction on the other Pillar 3 sheets)\n"
    f"FY2023/FY2022: CUKL Pillar 3 Disclosures December 2023, Table 5 (UK OV1), p.10 - {P3_2023_URL}\n"
    f"FY2021: CUKL Pillar 3 Disclosures December 2021, Table 4 (OV1), p.13 - {P3_2021_URL}\n"
    f"FY2020: CUKL Pillar 3 Disclosures December 2020, Table 6 (OV1), p.14 - {P3_2020_URL}\n"
    f"FY2019: CUKL Pillar 3 Disclosures December 2019, Table 6 (OV1), p.10 - {P3_2019_URL}\n"
    f"Regulatory filing index: {REG_URL}\n"
    + ENTITY_NOTE + "\n\n"
    "PRESENTATION NOTE: the FY2021 table's category labels differ slightly from FY2022/FY2023's (CCR is broken "
    "into mark-to-market/SFT sub-components in FY2021 vs a single CCR line in FY2022/FY2023; FY2021 has no "
    "'amounts below the thresholds for deduction' line, FY2022/FY2023 do) - both years' own category totals are "
    "reproduced as each report presents them, summing exactly to that year's own disclosed Total RWA (which ties "
    "to the existing Total RWAs sheet). "
    "FY2019/FY2020 also have no 'amounts below the thresholds for deduction' line (like FY2021), and both years' "
    "own OV1 tables report Market risk as nil ('-') under the de minimis guidance in CRR article 351 (CUKL's own "
    "FY2020 report states this explicitly) - reproduced here as 0.0, not blended with any other category. The "
    "FY2024 and FY2025 OV1 tables print an em dash for Counterparty credit risk, Settlement risk and "
    "Securitisation (the FY2024 report states 'There was no securitisation exposure at 31 December 2024'); "
    "those are shown as 0.0 for the same reason, so the category rows continue to foot exactly to each year's "
    "own printed Total. This deliberately differs from the convention on the KM1 Key Metrics sheet, where a "
    "dash is left BLANK: there it marks a requirement that does not apply to CUKL, here it marks a measured "
    "nil inside a table that has to sum.\n\n"
    "ROW 24 IS A MEMORANDUM ITEM, corrected 2026-09-16. UK OV1 row 24, 'Amounts below the thresholds for "
    "deduction (subject to 250% risk weight)', is not a risk category alongside credit/market/operational risk "
    "- it is a sub-set of row 1's credit-risk RWA, re-stated for information. This sheet previously listed it "
    "as a peer category, so the category rows over-footed their own Total by exactly that amount in every year "
    "it is disclosed. It is now shown below the Total, under its own memorandum heading. CUKL's own tables "
    "prove the point arithmetically: FY2025 credit 98.3 + market 12.4 + operational 217.0 = 327.7, its printed "
    "Total, with row 24's 9.6 excluded; FY2024 155.4 + 13.2 + 202.8 = 371.4 likewise, with 66.5 excluded."
)

bw = BankWorkbook(
    bank_name="Citibank UK Limited",
    years=YEARS,
    year_label=YEAR_LABEL,
    header_color="1F3B57",
)

bw.add_balance_sheet_sheet(
    title="Citibank UK Limited — Consolidated Statement of Financial Position",
    subtitle="Company (entity-level) basis, £'000. See sources for the combined Total liabilities/equity presentation.",
    rows=[
        ("SECTION", "Assets", {}),
        ("DATA", "Cash and balances at central banks", {"FY2025": 168445, "FY2024": 484139, "FY2023": 680797, "FY2022": 1526980, "FY2021": 1176483, "FY2020": 523979, "FY2019": 410731}),
        ("DATA", "Derivative financial instruments", {"FY2025": 0, "FY2024": 2592, "FY2023": 43848, "FY2022": 201825, "FY2021": 324553, "FY2020": 135163, "FY2019": 31272}),
        ("DATA", "Treasury bills and other eligible bills", {"FY2024": 0, "FY2023": 1651630, "FY2022": 2623200, "FY2021": 2309712, "FY2020": 2113702, "FY2019": 1625349}),
        ("DATA", "Loans and advances to banks", {"FY2025": 190064, "FY2024": 191422, "FY2023": 173568, "FY2022": 170277, "FY2021": 1287129, "FY2020": 624621, "FY2019": 1852319}),
        ("DATA", "Loans and advances to customers", {"FY2025": 0, "FY2024": 160, "FY2023": 40801, "FY2022": 70599, "FY2021": 265672, "FY2020": 353748, "FY2019": 578849}),
        ("DATA", "Debt securities", {"FY2024": 0, "FY2023": 865731, "FY2022": 1823106, "FY2021": 1756683, "FY2020": 1769954, "FY2019": 280016}),
        ("DATA", "Intangible fixed assets", {"FY2025": 14, "FY2024": 24, "FY2023": 2936, "FY2022": 4467, "FY2021": 6687, "FY2020": 7339, "FY2019": 7615}),
        ("DATA", "Other assets", {"FY2025": 2390, "FY2024": 4174, "FY2023": 37418, "FY2022": 65125, "FY2021": 65217, "FY2020": 97394, "FY2019": 24491}),
        ("DATA", "Prepayment and accrued income", {"FY2025": 2022, "FY2024": 2118, "FY2023": 2488, "FY2022": 1661, "FY2021": 2148}),
        ("TOTAL", "Total assets", {"FY2025": 362935, "FY2024": 684629, "FY2023": 3499217, "FY2022": 6487240, "FY2021": 7194284, "FY2020": 5625900, "FY2019": 4810642}),
        ("SECTION", "Liabilities", {}),
        ("DATA", "Deposits by banks", {"FY2025": 0, "FY2024": 84, "FY2023": 9400, "FY2022": 32184, "FY2021": 8316, "FY2020": 18965, "FY2019": 5799}),
        ("DATA", "Customer accounts", {"FY2025": 77335, "FY2024": 140207, "FY2023": 2790344, "FY2022": 5672994, "FY2021": 6372454, "FY2020": 4983443, "FY2019": 4345627}),
        ("DATA", "Derivative financial instruments", {"FY2025": 0, "FY2024": 3015, "FY2023": 43411, "FY2022": 203089, "FY2021": 320789, "FY2020": 139610, "FY2019": 31510}),
        ("DATA", "Other liabilities", {"FY2025": 6421, "FY2024": 8843, "FY2023": 15330, "FY2022": 19456, "FY2021": 56809, "FY2020": 21551, "FY2019": 8758}),
        ("DATA", "Accruals and deferred income", {"FY2025": 2874, "FY2024": 3687, "FY2023": 4877, "FY2022": 7840, "FY2021": 4868, "FY2020": 5733, "FY2019": 4090}),
        ("DATA", "Provisions for liabilities", {"FY2025": 3739, "FY2024": 10833, "FY2023": 10254, "FY2022": 10436, "FY2021": 850, "FY2020": 176, "FY2019": 113}),
        ("DATA", "Subordinated liabilities", {"FY2024": 0, "FY2023": 52382, "FY2022": 52237, "FY2021": 52072, "FY2020": 52092, "FY2019": 52121}),
        ("SECTION", "Equity", {}),
        ("DATA", "Called up share capital", {"FY2025": 0, "FY2024": 0, "FY2023": 0, "FY2022": 0, "FY2021": 0, "FY2020": 0, "FY2019": 0}),
        ("DATA", "Reserves", {"FY2025": 259972, "FY2024": 510934, "FY2023": 505184, "FY2022": 434300, "FY2021": 341987, "FY2020": 375755, "FY2019": 356341}),
        ("DATA", "Profit and loss account", {"FY2025": 12594, "FY2024": 7026, "FY2023": 68035, "FY2022": 54704, "FY2021": 36139, "FY2020": 28575, "FY2019": 6283}),
        ("TOTAL", "Total liabilities (incl. equity - see sources)", {"FY2025": 362935, "FY2024": 684629, "FY2023": 3499217, "FY2022": 6487240, "FY2021": 7194284, "FY2020": 5625900, "FY2019": 4810642}),
    ],
    sources_text=STATEMENTS_SOURCES,
    first_col_width=56,
    source_height=180,
    unit_suffix=" (£'000)",
)

bw.add_income_statement_sheet(
    title="Citibank UK Limited — Income Statement",
    subtitle="Company (entity-level) basis, £'000.",
    rows=[
        ("SECTION", "Income", {}),
        ("DATA", "Interest receivable", {"FY2025": 19839, "FY2024": 65131, "FY2023": 160605, "FY2022": 98603, "FY2021": 42733, "FY2020": 37549, "FY2019": 17376}),
        ("DATA", "Interest payable", {"FY2025": -512, "FY2024": -20935, "FY2023": -43107, "FY2022": -11677, "FY2021": -1816, "FY2020": -5318, "FY2019": -3705}),
        ("DATA", "Fees and commissions receivable", {"FY2025": 12470, "FY2024": 24476, "FY2023": 38466, "FY2022": 48022, "FY2021": 34505, "FY2020": 31551, "FY2019": 9380}),
        ("DATA", "Fees and commissions payable", {"FY2025": -1425, "FY2024": -3389, "FY2023": -4333, "FY2022": -4516, "FY2021": -5050, "FY2020": -3088, "FY2019": -578}),
        ("DATA", "Dealing profits/(loss)", {"FY2025": 535, "FY2024": -70424, "FY2023": -35246, "FY2022": -606, "FY2021": 3743, "FY2020": 26886, "FY2019": 942}),
        ("DATA", "Other operating income", {"FY2025": 1100, "FY2024": 1093, "FY2023": 1559, "FY2022": 825, "FY2021": 530, "FY2020": 40, "FY2019": 0}),
        ("DATA", "Administrative expenses", {"FY2025": -26268, "FY2024": -77701, "FY2023": -95512, "FY2022": -98726, "FY2021": -61763, "FY2020": -50367, "FY2019": -12136}),
        ("DATA", "Depreciation and amortization", {"FY2025": -3, "FY2024": -2913, "FY2023": -1530, "FY2022": -2187, "FY2021": -2346, "FY2020": -1979, "FY2019": -846}),
        ("DATA", "Other operating charges", {"FY2025": 0, "FY2024": -7, "FY2023": -15, "FY2022": -292, "FY2021": -103, "FY2020": -377, "FY2019": -44}),
        ("DATA", "Impairment on financial assets / Provisions", {"FY2025": 8, "FY2024": 53, "FY2023": 110, "FY2022": 416, "FY2021": 1309, "FY2020": -1216, "FY2019": -878}),
        ("TOTAL", "Profit/(loss) on ordinary activities before tax", {"FY2025": 5744, "FY2024": -84616, "FY2023": 20997, "FY2022": 29862, "FY2021": 11742, "FY2020": 33681, "FY2019": 9511}),
        ("DATA", "Tax on profit on ordinary activities", {"FY2025": -176, "FY2024": 27444, "FY2023": -1016, "FY2022": -8047, "FY2021": -928, "FY2020": -8139, "FY2019": -2425}),
        ("TOTAL", "Profit/(loss) for the financial year", {"FY2025": 5568, "FY2024": -57172, "FY2023": 19981, "FY2022": 21815, "FY2021": 10814, "FY2020": 25542, "FY2019": 7086}),
        ("SECTION", "Other comprehensive income", {}),
        ("DATA", "Debt instruments at FVOCI - net change in fair value", {"FY2025": 0, "FY2024": 12450, "FY2023": 66975, "FY2022": -147555, "FY2021": -44921, "FY2020": 53343, "FY2019": -9664}),
        ("DATA", "Debt instruments at FVOCI - reclassified to profit or loss", {"FY2025": 0, "FY2024": 70082, "FY2023": 26902, "FY2022": 0, "FY2021": -3980, "FY2020": -27034, "FY2019": 0}),
        ("DATA", "Related tax", {"FY2025": 0, "FY2024": -24102, "FY2023": -26320, "FY2022": 39779, "FY2021": 15139, "FY2020": -6910, "FY2019": 2416}),
        ("TOTAL", "Other comprehensive income/(loss) for the year, net of tax", {"FY2025": 0, "FY2024": 58430, "FY2023": 67557, "FY2022": -107776, "FY2021": -33762, "FY2020": 19399, "FY2019": -7248}),
        ("TOTAL", "Total comprehensive income/(loss) for the year", {"FY2025": 5568, "FY2024": 1258, "FY2023": 87538, "FY2022": -85961, "FY2021": -22948, "FY2020": 44941, "FY2019": -162}),
    ],
    sources_text=STATEMENTS_SOURCES,
    first_col_width=56,
    source_height=180,
    unit_suffix=" (£'000)",
)

bw.add_equity_changes_sheet(
    title="Citibank UK Limited — Statement of Changes in Equity",
    subtitle="Company (entity-level) basis, £'000. Read chronologically oldest-to-newest.",
    headers=["Called up share capital", "Other reserve", "Fair value reserve", "Equity reserve", "Profit and loss account", "Total"],
    rows=[
        ("TOTAL", "At 1 January 2019 (CUKL dormant throughout FY2018 - see ENTITY NOTE)", (0, 0, 0, 0, 0, 0)),
        ("DATA", "Profit for the financial year (FY2019)", (None, None, None, None, 7086, 7086)),
        ("DATA", "Debt instruments at FVOCI - net change in fair value", (None, None, -9664, None, None, -9664)),
        ("DATA", "Tax on other comprehensive loss", (None, None, 2416, None, None, 2416)),
        ("DATA", "Capital contribution", (None, 318647, None, None, None, 318647)),
        ("DATA", "Equity decrease resulting from common control transaction", (None, -7058, None, None, None, -7058)),
        ("DATA", "Additional Tier 1 Capital", (None, 52000, None, None, None, 52000)),
        ("DATA", "Dividends on Additional Tier 1 Capital", (None, None, None, None, -803, -803)),
        ("TOTAL", "At 31 December 2019", (0, 363589, -7248, 0, 6283, 362624)),
        ("DATA", "Profit for the financial year (FY2020)", (None, None, None, None, 25542, 25542)),
        ("DATA", "Debt instruments at FVOCI - net change in fair value", (None, None, 53343, None, None, 53343)),
        ("DATA", "Debt instruments at FVOCI - reclassified to profit or loss", (None, None, -27034, None, None, -27034)),
        ("DATA", "Tax on other comprehensive income", (None, None, -6910, None, None, -6910)),
        ("DATA", "Dividends on Additional Tier 1 Capital", (None, None, None, None, -3250, -3250)),
        ("DATA", "Equity settled share-based payment", (None, None, None, 21, None, 21)),
        ("DATA", "Tax on equity", (None, None, None, -6, None, -6)),
        ("TOTAL", "At 31 December 2020", (0, 363589, 12151, 15, 28575, 404330)),
        ("DATA", "Profit for the financial year (FY2021)", (None, None, None, None, 10814, 10814)),
        ("DATA", "Debt instruments at FVOCI - net change in fair value", (None, None, -44921, None, None, -44921)),
        ("DATA", "Debt instruments at FVOCI - reclassified to profit or loss", (None, None, -3980, None, None, -3980)),
        ("DATA", "Tax on other comprehensive loss", (None, None, 15139, None, None, 15139)),
        ("DATA", "Capital contribution", (None, 22991, None, None, None, 22991)),
        ("DATA", "Equity decrease resulting from common control transaction", (None, -22991, None, None, None, -22991)),
        ("DATA", "Dividends on Additional Tier 1 Capital", (None, None, None, None, -3250, -3250)),
        ("DATA", "Equity settled share-based payment, net of tax", (None, None, None, -6, None, -6)),
        ("TOTAL", "At 31 December 2021", (0, 363589, -21611, 9, 36139, 378126)),
        ("DATA", "Profit for the financial year (FY2022)", (None, None, None, None, 21815, 21815)),
        ("DATA", "Debt instruments at FVOCI - net change in fair value", (None, None, -147555, None, None, -147555)),
        ("DATA", "Tax on other comprehensive loss", (None, None, 39779, None, None, 39779)),
        ("DATA", "Capital contribution", (None, 200000, None, None, None, 200000)),
        ("DATA", "Dividends on Additional Tier 1 Capital", (None, None, None, None, -3250, -3250)),
        ("DATA", "Equity settled share-based payment", (None, None, None, 89, None, 89)),
        ("TOTAL", "At 31 December 2022", (0, 563589, -129387, 98, 54704, 489004)),
        ("DATA", "Profit for the financial year (FY2023)", (None, None, None, None, 19981, 19981)),
        ("DATA", "Debt instruments at FVOCI - net change in fair value", (None, None, 66975, None, None, 66975)),
        ("DATA", "Debt instruments at FVOCI - reclassified to profit or loss", (None, None, 26902, None, None, 26902)),
        ("DATA", "Tax on other comprehensive loss", (None, None, -26320, None, None, -26320)),
        ("DATA", "Adjustment (reclassification within reserves - see sources)", (None, None, 3400, None, -3400, 0)),
        ("DATA", "Dividends on Additional Tier 1 Capital", (None, None, None, None, -3250, -3250)),
        ("DATA", "Equity settled share-based payment", (None, None, None, -73, None, -73)),
        ("TOTAL", "At 31 December 2023", (0, 563589, -58430, 25, 68035, 573219)),
        ("DATA", "Profit/(loss) for the financial year (FY2024)", (None, None, None, None, -57172, -57172)),
        ("DATA", "Debt instruments at FVOCI - net change in fair value", (None, None, 12450, None, None, 12450)),
        ("DATA", "Debt instruments at FVOCI - reclassified to profit or loss", (None, None, 70082, None, None, 70082)),
        ("DATA", "Tax on other comprehensive income", (None, None, -24102, None, None, -24102)),
        ("DATA", "Dividends on Additional Tier 1 Capital", (None, None, None, None, -3837, -3837)),
        ("DATA", "Additional Tier 1 Capital redemption", (None, -52000, None, None, None, -52000)),
        ("DATA", "Equity settled share-based payment", (None, None, None, -680, None, -680)),
        ("TOTAL", "At 31 December 2024", (0, 511589, 0, -655, 7026, 517960)),
        ("DATA", "Profit for the financial year (FY2025)", (None, None, None, None, 5568, 5568)),
        ("DATA", "Capital contribution/(capital repayment)", (None, -250000, None, None, None, -250000)),
        ("DATA", "Equity settled share-based payment", (None, None, None, -962, None, -962)),
        ("TOTAL", "At 31 December 2025", (0, 261589, 0, -1617, 12594, 272566)),
    ],
    sources_text=STATEMENTS_SOURCES,
    first_col_width=56,
    source_height=180,
)

bw.add_cash_flow_sheet(
    title="Citibank UK Limited — Cash Flow Statement",
    subtitle="Not applicable — CUKL applies the FRS 101 IAS 7 cash-flow disclosure exemption.",
    rows=[
        ("SECTION", "No Statement of Cash Flows is published for the covered entity", {}),
        ("DATA", "Pillar-3-only scope used because the statutory cash-flow statement is exempted and unavailable.", {}),
    ],
    sources_text=ENTITY_NOTE + "\n\n" + EXEMPTION_NOTE,
    first_col_width=90,
    source_height=230,
    unit_suffix="",
)


bw.add_asset_quality_sheet(
    title="Citibank UK Limited — Asset Quality",
    subtitle="Company (entity-level) basis, £'000. See sources - stage-split basis differs FY2024/23/20/19 vs FY2022/21.",
    rows=[
        ("SECTION", "Loan book", {}),
        ("DATA", "Loans and advances to customers, net", {"FY2025": 0, "FY2024": 160, "FY2023": 40801, "FY2022": 70599, "FY2021": 265672, "FY2020": 353748, "FY2019": 578849}),
        ("SECTION", "Stage split (FY2024/23/20/19: full customer loan book; FY2022/21: CRE component only - see sources; FY2025: no customer loan book)", {}),
        ("DATA", "Stage 1 gross exposure", {"FY2024": 162, "FY2023": 40742, "FY2021": 161246, "FY2020": 240290, "FY2019": 579400}),
        ("DATA", "Stage 2 gross exposure", {"FY2023": 53, "FY2020": 114930}),
        ("DATA", "Stage 3 gross exposure", {"FY2023": 17, "FY2020": 13}),
        ("DATA", "Stage 1 ECL allowance", {"FY2024": -2, "FY2023": -11, "FY2020": -150, "FY2019": -551}),
        ("DATA", "Stage 2 ECL allowance", {"FY2020": -1322}),
        ("DATA", "Stage 3 ECL allowance", {"FY2020": -13}),
        ("TOTAL", "Total ECL allowance, closing balance", {"FY2024": -2, "FY2023": -11, "FY2022": 0, "FY2021": 0, "FY2020": -1485, "FY2019": -551}),
    ],
    sources_text=ASSET_QUALITY_SOURCES,
    first_col_width=68,
)


def metric(name, unit, rows_data, note=None):
    bw.add_metric_sheet(name, unit, rows_data, P3_SOURCES, note=note, first_col_width=56, source_height=145)


# ---------------------------------------------------------------
# KM1 Key Metrics - CUKL's own published template, reproduced as printed.
#
# CUKL printed TWO DIFFERENT key-metrics templates over this workbook's seven
# years, and they are not the same table with a few rows added:
#
#   - FY2019, FY2020 and FY2021 editions print the BASEL III KM1 (BCBS
#     "Key Metrics (KM1)"): 17 rows only, captioned "Available capital",
#     "Total risk-weighted assets (RWA)", "Countercyclical buffer
#     requirement", "Bank G-SIB and/or D-SIB additional requirements", "Total
#     Basel III leverage ratio measure", "Total HQLA", "Total net cash
#     outflow", "LCR ratio". No UK 7a-7d SREP rows and NO NSFR rows at all.
#   - FY2022, FY2023, FY2024 and FY2025 editions print the UK KM1 ("Table 1:
#     Key metrics template (UK KM1)"): 26 rows, the UK-prefixed SREP and
#     buffer rows, and rows 18-20 for NSFR.
#
# The SAME ROW NUMBER MEANS DIFFERENT THINGS in the two templates - rows
# 10, 11, 12, 13, 14, 15, 16 and 17 all have different captions and, for
# 13/14, a different leverage basis (Basel III including claims on central
# banks vs the UK measure excluding them). Merging them into one row set
# would silently assert a continuity the bank never claimed - indeed CUKL's
# own FY2022 edition prints "N/A" in its FY2021 comparative for rows 13, 14
# and 18-20, with footnotes saying each is a first-time disclosure with no
# comparative provided. So the sheet carries two separately-captioned blocks.
#
# COLUMN SETS differ too, and are read off each edition's own header block:
#   - FY2019 edition: ONE column, "31 Dec 2019" (CUKL's first Pillar 3).
#   - FY2020 and FY2021 editions: FIVE columns - four quarter-ends plus the
#     prior 31 December. Only the year-end column belongs in a workbook of
#     financial years; the three intra-year quarter columns are not used.
#   - FY2022-FY2025 editions: TWO columns, the year-end and the prior
#     year-end.
#
# EACH YEAR FROM ITS OWN EDITION, which matters here in one concrete place:
# row 12 for FY2019 is 13.06% in the FY2019 edition but 25.2% in the FY2020
# edition's FY2019 comparative, because that edition's own footnote 1 says
# "Basis of calculation for 'CET1 available after meeting the bank's minimum
# capital requirements' has been modified. CET1 ratio does not include CRD IV
# buffers for both current and prior periods." The FY2019 edition's own
# 13.06% is what is shown.
# ---------------------------------------------------------------
km1_rows = [
    ("SECTION", "UK KM1 — 'Table 1: Key metrics template (UK KM1)', as printed in the FY2022-FY2025 editions", {}),
    ("SECTION", "Available own funds (amounts, £ million)", {}),
    ("DATA", "1    Common Equity Tier 1 (CET1) capital",
     {"FY2025": 268.6, "FY2024": 514.5, "FY2023": 418.0, "FY2022": 417.0}),
    ("DATA", "2    Tier 1 capital",
     {"FY2025": 268.6, "FY2024": 514.5, "FY2023": 470.0, "FY2022": 469.0}),
    ("DATA", "3    Total capital",
     {"FY2025": 268.6, "FY2024": 514.5, "FY2023": 522.0, "FY2022": 521.0}),
    ("SECTION", "Risk-weighted exposure amounts (£ million)", {}),
    ("DATA", "4    Total risk-weighted exposure amount",
     {"FY2025": 327.7, "FY2024": 371.4, "FY2023": 574.7, "FY2022": 706.1}),
    ("SECTION", "Capital ratios (as a percentage of risk-weighted exposure amount)", {}),
    ("DATA", "5    Common Equity Tier 1 ratio (%)",
     {"FY2025": "82.0%", "FY2024": "138.6%", "FY2023": "72.7%", "FY2022": "59.1%"}),
    ("DATA", "6    Tier 1 ratio (%)",
     {"FY2025": "82.0%", "FY2024": "138.6%", "FY2023": "81.8%", "FY2022": "66.4%"}),
    ("DATA", "7    Total capital ratio (%)",
     {"FY2025": "82.0%", "FY2024": "138.6%", "FY2023": "90.8%", "FY2022": "73.8%"}),
    ("SECTION", "Additional own funds requirements based on SREP (as a percentage of risk-weighted exposure amount)", {}),
    ("DATA", "UK 7a    Additional CET1 SREP requirements (%)",
     {"FY2025": "1.7%", "FY2024": "17.4%", "FY2023": "17.4%", "FY2022": "6.4%"}),
    ("DATA", "UK 7b    Additional AT1 SREP requirements (%)",
     {"FY2025": "0.6%", "FY2024": "5.8%", "FY2023": "5.8%", "FY2022": "2.1%"}),
    ("DATA", "UK 7c    Additional T2 SREP requirements (%)",
     {"FY2025": "0.7%", "FY2024": "7.7%", "FY2023": "7.7%", "FY2022": "2.8%"}),
    ("DATA", "UK 7d    Total SREP own funds requirements (%)",
     {"FY2025": "11.0%", "FY2024": "39.0%", "FY2023": "39.0%", "FY2022": "19.3%"}),
    ("SECTION", "Combined buffer requirement (as a percentage of risk-weighted exposure amount)", {}),
    ("DATA", "8    Capital conservation buffer (%)",
     {"FY2025": "2.5%", "FY2024": "2.5%", "FY2023": "2.5%", "FY2022": "2.5%"}),
    ("DATA", "UK 8a    Conservation buffer due to macro-prudential or systemic risk identified at the level of a Member State (%)", {}),
    ("DATA", "9    Institution specific countercyclical capital buffer (%)",
     {"FY2025": "1.9%", "FY2024": "1.7%", "FY2023": "1.0%", "FY2022": "0.13%"}),
    ("DATA", "UK 9a    Systemic risk buffer (%)", {}),
    ("DATA", "10    Global Systemically Important Institution buffer (%)", {}),
    ("DATA", "UK 10a    Other Systemically Important Institution buffer", {}),
    ("DATA", "11    Combined buffer requirement (%)",
     {"FY2025": "4.4%", "FY2024": "4.2%", "FY2023": "3.5%", "FY2022": "2.6%"}),
    ("DATA", "UK 11a    Overall capital requirements (%)",
     {"FY2025": "15.4%", "FY2024": "43.2%", "FY2023": "42.4%", "FY2022": "22.0%"}),
    ("DATA", "12    CET1 available after meeting the total SREP own funds requirements (%)",
     {"FY2025": "75.8%", "FY2024": "116.6%", "FY2023": "50.8%", "FY2022": "48.2%"}),
    ("SECTION", "Leverage ratio (£ million / %)", {}),
    ("DATA", "13    Total exposure measure excluding claims on central banks",
     {"FY2025": 343.4, "FY2024": 670, "FY2023": 2812, "FY2022": 4733}),
    ("DATA", "14    Leverage ratio excluding claims on central banks (%)",
     {"FY2025": "78.2%", "FY2024": "76.8%", "FY2023": "16.7%", "FY2022": "9.9%"}),
    ("SECTION", "Additional leverage ratio disclosure requirements (CUKL is not an LREQ company — see note)", {}),
    ("DATA", "14a    Fully loaded ECL accounting model leverage ratio excluding claims on central banks (%)", {}),
    ("DATA", "14b    Leverage ratio including claims on central banks (%)", {}),
    ("DATA", "14c    Average leverage ratio excluding claims on central banks (%)", {}),
    ("DATA", "14d    Average leverage ratio including claims on central banks (%)", {}),
    ("DATA", "14e    Countercyclical leverage ratio buffer (%)", {}),
    ("SECTION", "Liquidity Coverage Ratio (£ million / %)", {}),
    ("DATA", "15    Total high-quality liquid assets (HQLA) (Weighted value -average)",
     {"FY2025": 400.7, "FY2024": 1344.0, "FY2023": 2988.6, "FY2022": 4476.6}),
    ("DATA", "UK 16a    Cash outflows – Total weighted value",
     {"FY2025": 40.1, "FY2024": 195.8, "FY2023": 530.6, "FY2022": 787.2}),
    ("DATA", "UK 16b    Cash inflows – Total weighted value",
     {"FY2025": 33.4, "FY2024": 81.5, "FY2023": 173.1, "FY2022": 100.1}),
    ("DATA", "16    Total net cash outflows (adjusted value)",
     {"FY2025": 20.2, "FY2024": 114.3, "FY2023": 357.5, "FY2022": 687.1}),
    ("DATA", "17    Liquidity coverage ratio (%)",
     {"FY2025": "3089.9%", "FY2024": "1175.7%", "FY2023": "836.0%", "FY2022": "654.5%"}),
    ("SECTION", "Net Stable Funding Ratio (£ million / %)", {}),
    ("DATA", "18    Total available stable funding",
     {"FY2025": 537.3, "FY2024": 1459.8, "FY2023": 4091.4, "FY2022": 6249.1}),
    ("DATA", "19    Total required stable funding",
     {"FY2025": 175.2, "FY2024": 312.0, "FY2023": 1018.8, "FY2022": 1839.5}),
    ("DATA", "20    NSFR ratio (%)",
     {"FY2025": "306.3%", "FY2024": "467.9%", "FY2023": "401.6%", "FY2022": "342.2%"}),
    ("SECTION", "Basel III KM1 — 'Table 1: Key Metrics (KM1)', the SUPERSEDED template printed in the FY2019-FY2021 editions (different row meanings — see note)", {}),
    ("SECTION", "Available capital (amounts, £ million)", {}),
    ("DATA", "1    Common Equity Tier 1 (CET1)",
     {"FY2021": 304.2, "FY2020": 316.7, "FY2019": 291.8}),
    ("DATA", "2    Tier 1",
     {"FY2021": 356.2, "FY2020": 368.7, "FY2019": 343.8}),
    ("DATA", "3    Total capital",
     {"FY2021": 408.2, "FY2020": 420.7, "FY2019": 395.8}),
    ("SECTION", "Risk-weighted assets (£ million)", {}),
    ("DATA", "4    Total risk-weighted assets (RWA)",
     {"FY2021": 805.3, "FY2020": 961.6, "FY2019": 873.2}),
    ("SECTION", "Risk-based capital ratios as a percentage of RWA", {}),
    ("DATA", "5    Common Equity Tier 1 ratio (%)",
     {"FY2021": "37.8%", "FY2020": "32.9%", "FY2019": "33.4%"}),
    ("DATA", "6    Tier 1 ratio (%)",
     {"FY2021": "44.2%", "FY2020": "38.3%", "FY2019": "39.4%"}),
    ("DATA", "7    Total capital ratio (%)",
     {"FY2021": "50.7%", "FY2020": "43.7%", "FY2019": "45.3%"}),
    ("SECTION", "Additional CET1 buffer requirements as a percentage of RWA", {}),
    ("DATA", "8    Capital conservation buffer requirement (%)",
     {"FY2021": "2.50%", "FY2020": "2.50%", "FY2019": "2.5%"}),
    ("DATA", "9    Countercyclical buffer requirement (%)",
     {"FY2021": "0.04%", "FY2020": "0.02%", "FY2019": "0.49%"}),
    ("DATA", "10    Bank G-SIB and/or D-SIB additional requirements (%)  [FY2019 edition: 'Bank G-SIB additional requirements (%)']", {}),
    ("DATA", "11    Total of bank CET1 specific buffer requirements (%)  [FY2019 edition adds '(row 8 + row 9 + row 10)']",
     {"FY2021": "2.54%", "FY2020": "2.52%", "FY2019": "2.99%"}),
    ("DATA", "12    CET1 available after meeting the bank's minimum capital requirements (%)",
     {"FY2021": "27.4%", "FY2020": "25.7%", "FY2019": "13.06%"}),
    ("SECTION", "Basel III Leverage Ratio (£ million / %) — INCLUDING claims on central banks, pre-1 January 2022 basis", {}),
    ("DATA", "13    Total Basel III leverage ratio measure",
     {"FY2021": 6818.1, "FY2020": 5424.1, "FY2019": 4773.6}),
    ("DATA", "14    Basel III leverage ratio (%)",
     {"FY2021": "5.2%", "FY2020": "6.8%", "FY2019": "7.2%"}),
    ("SECTION", "Liquidity Coverage Ratio (£ million / %) — daily averages", {}),
    ("DATA", "15    Total HQLA",
     {"FY2021": 4219.7, "FY2020": 3069.7, "FY2019": 3474.2}),
    ("DATA", "16    Total net cash outflow",
     {"FY2021": 639.8, "FY2020": 434.5, "FY2019": 436.6}),
    ("DATA", "17    LCR ratio (%)",
     {"FY2021": "659%", "FY2020": "707%", "FY2019": "795.8%"}),
]

KM1_SOURCES = (
    "Sources - Citibank UK Limited's own published key-metrics template, reproduced as printed. Each column is "
    "transcribed from the edition in which that year is the reporting year, never from a later edition's "
    "comparative.\n"
    f"FY2025: CUKL Pillar 3 Disclosures December 2025, Table 1 'Key metrics template (UK KM1)', printed p.4 - "
    f"{P3_2025_URL}\n"
    f"FY2024: CUKL Pillar 3 Disclosures December 2024, Table 1 'Key metrics template (UK KM1)', printed p.4 - "
    f"{P3_2024_URL}\n"
    f"FY2023: CUKL Pillar 3 Disclosures December 2023, Table 1 'Key metrics template (UK KM1)', printed p.4 - "
    f"{P3_2023_URL}\n"
    f"FY2022: CUKL Pillar 3 Disclosures December 2022, Table 1 'Key metrics template (UK KM1)', printed p.5 - "
    f"{P3_2022_URL} (read by OCR - that PDF's text layer is broken; see the cross-check described on the other "
    f"Pillar 3 sheets' source note)\n"
    f"FY2021: CUKL Pillar 3 Disclosures December 2021, Table 1 'Key Metrics (KM1)', printed p.6, '31 December "
    f"2021' column - {P3_2021_URL}\n"
    f"FY2020: CUKL Pillar 3 Disclosures December 2020, Table 1 'Key Metrics (KM1)', printed p.5, '31 December "
    f"2020' column - {P3_2020_URL}\n"
    f"FY2019: CUKL Pillar 3 Disclosures December 2019, Table 1 'Key Metrics (KM1)', printed p.5 - "
    f"{P3_2019_URL}\n\n"
    "TWO DIFFERENT TEMPLATES, SHOWN AS TWO BLOCKS. This is the single most important thing about this sheet. "
    "CUKL's FY2019-FY2021 editions print the BASEL III KM1 (BCBS 'Key Metrics (KM1)'): 17 rows, captioned "
    "'Available capital', 'Total risk-weighted assets (RWA)', 'Countercyclical buffer requirement', 'Bank G-SIB "
    "and/or D-SIB additional requirements', 'Total Basel III leverage ratio measure', 'Total HQLA', 'Total net "
    "cash outflow' and 'LCR ratio', with no UK 7a-7d SREP rows and no NSFR rows at all. Its FY2022-FY2025 "
    "editions print the UK KM1: 26 rows, UK-prefixed SREP and buffer rows, and rows 18-20 for NSFR. The same "
    "ROW NUMBER means different things in the two templates (rows 10, 11, 12, 13, 14, 15, 16 and 17 all differ "
    "in caption, and 13/14 differ in basis), so merging them into one row set would assert a continuity CUKL "
    "never claimed. CUKL says so itself: its FY2022 edition prints 'N/A' in the FY2021 comparative for rows 13, "
    "14 and 18-20, footnoted 'Given it is the first-time disclosure of the measures excluding central bank "
    "claims, no comparative of 31 December 2021 is provided' and 'NSFR disclosures have been implemented from 1 "
    "January 2022... N/A in 31 December 2021 indicates that the disclosure is new and no comparatives are being "
    "provided.'\n\n"
    "COLUMN SETS, read off each edition's own header block:\n"
    "• FY2019 edition: ONE column ('31 Dec 2019') - CUKL's first Pillar 3 disclosure, no comparatives.\n"
    "• FY2020 and FY2021 editions: FIVE columns - 31 December, 30 September, 30 June and 31 March of the "
    "reporting year, plus the prior 31 December. Only the year-end column is used here; the three intra-year "
    "quarter-end columns are not financial years and are deliberately not carried into this workbook (for the "
    "record, the FY2021 edition's Q3/Q2/Q1 CET1 were 312.8 / 320.8 / 293.0 and the FY2020 edition's were "
    "323.1 / 331.4 / 318.3).\n"
    "• FY2022-FY2025 editions: TWO columns, the reporting year-end and the prior year-end.\n\n"
    "EACH YEAR FROM ITS OWN EDITION - one concrete consequence. Row 12 for FY2019 is 13.06% here, from the "
    "FY2019 edition. The FY2020 edition shows 25.2% in its own FY2019 comparative column, because that edition "
    "restated the basis: its footnote 1 reads 'Basis of calculation for \"CET1 available after meeting the "
    "bank's minimum capital requirements\" has been modified. CET1 ratio does not include CRD IV buffers for "
    "both current and prior periods.' Both figures are CUKL's; the one shown is the one published for FY2019 as "
    "FY2019's own reporting year.\n\n"
    "DASH vs BLANK. Rows UK 8a, UK 9a, 10 and UK 10a print an em dash '—' in every UK KM1 edition, and row 10 "
    "prints '-' in every Basel III edition; all are left BLANK here, since the dash means the requirement does "
    "not apply, not that it is measured at zero. Rows 14a-14e are printed with NOTHING at all in the "
    "FY2023-FY2025 editions and with '-' in the FY2022 edition; both are blank here, and the reason is a "
    "positive one the bank states in a footnote to the table: 'CUKL is not a UK Leverage Ratio Capital "
    "Requirement (\"LREQ\") Company... and in line with instructions included in Annex II of the PS 21/21 these "
    "rows are left blank.'\n\n"
    "PRECISION AS PRINTED. Row 13 is printed to one decimal place in the FY2025 edition (343.4) but as whole "
    "millions in the FY2024, FY2023 and FY2022 editions (670, 2,812, 4,733) - the FY2025 edition's own FY2024 "
    "comparative reads 670.2, but FY2024's own edition prints 670, and that is what is shown. Row 9 is 0.13% "
    "for FY2022 from the FY2022 edition and 0.1% in the FY2023 edition's comparative; row 8 is '2.5%' in the "
    "FY2019 edition and '2.50%' in the FY2020/FY2021 editions.\n\n"
    "LATEST-EDITION CHECK, 2026-09-16: performed against Citi's own regulatory-filings index, which is how the "
    "FY2025 Pillar 3 and the previously-missed FY2024 Pillar 3 were found. See the other Pillar 3 sheets' "
    "source note for the full correction."
)

bw.add_km1_sheet(
    title="Citibank UK Limited — KM1 Key Metrics",
    subtitle="CUKL's own published key-metrics template, reproduced in its row order with its own row numbers, "
             "labels and printed precision. Amounts in £ million, ratios as printed. Entity (stand-alone) basis. "
             "TWO templates are shown as two blocks: the UK KM1 (FY2022-FY2025 editions) and the superseded "
             "Basel III KM1 (FY2019-FY2021 editions), whose row numbers do NOT mean the same things. "
             "See source note below.",
    rows=km1_rows,
    sources_text=KM1_SOURCES,
    first_col_width=76,
    source_height=520,
)

metric("CET1 Capital", "£m", [
    ("Common Equity Tier 1 (CET1) capital", {"FY2025": 268.6, "FY2024": 514.5, "FY2023": 418.0, "FY2022": 417.0, "FY2021": 304.2, "FY2020": 316.7, "FY2019": 291.8}),
])
metric("CET1 Ratio", "% of RWA", [
    ("Common Equity Tier 1 (CET1) ratio", {"FY2025": "82.0%", "FY2024": "138.6%", "FY2023": "72.7%", "FY2022": "59.1%", "FY2021": "37.8%", "FY2020": "32.9%", "FY2019": "33.4%"}),
])
metric("Tier 1 Capital", "£m", [
    ("Tier 1 capital", {"FY2025": 268.6, "FY2024": 514.5, "FY2023": 470.0, "FY2022": 469.0, "FY2021": 356.2, "FY2020": 368.7, "FY2019": 343.8}),
], note="Tier 1 equals CET1 from FY2024 onward: CUKL redeemed its £52m of Additional Tier 1 capital on 5 December 2024, so there is no AT1 layer in FY2024 or FY2025.")
metric("Tier 1 Ratio", "% of RWA", [
    ("Tier 1 ratio", {"FY2025": "82.0%", "FY2024": "138.6%", "FY2023": "81.8%", "FY2022": "66.4%", "FY2021": "44.2%", "FY2020": "38.3%", "FY2019": "39.4%"}),
])
metric("Total Capital", "£m", [
    ("Total capital", {"FY2025": 268.6, "FY2024": 514.5, "FY2023": 522.0, "FY2022": 521.0, "FY2021": 408.2, "FY2020": 420.7, "FY2019": 395.8}),
])
metric("Total Capital Ratio", "% of RWA", [
    ("Total capital ratio", {"FY2025": "82.0%", "FY2024": "138.6%", "FY2023": "90.8%", "FY2022": "73.8%", "FY2021": "50.7%", "FY2020": "43.7%", "FY2019": "45.3%"}),
])
metric("Total RWAs", "£m", [
    ("Total risk-weighted exposure amount", {"FY2025": 327.7, "FY2024": 371.4, "FY2023": 574.7, "FY2022": 706.1, "FY2021": 805.3, "FY2020": 961.6, "FY2019": 873.2}),
])
bw.add_rwa_breakdown_sheet(
    title="Citibank UK Limited — RWA Breakdown",
    subtitle="UK OV1 template, £m.",
    rows=[
        ("DATA", "Credit risk (excluding CCR)", {"FY2025": 98.3, "FY2024": 155.4, "FY2023": 264.1, "FY2022": 193.6, "FY2021": 419.2, "FY2020": 543.6, "FY2019": 668.2}),
        ("DATA", "Counterparty credit risk (CCR)", {"FY2025": 0.0, "FY2024": 0.0, "FY2023": 0.9, "FY2022": 3.4, "FY2021": 15.2, "FY2020": 39.4, "FY2019": 8.3}),
        ("DATA", "Securitisation exposures in the non-trading/banking book", {"FY2025": 0.0, "FY2024": 0.0, "FY2023": 124.0, "FY2022": 261.5, "FY2021": 245.9, "FY2020": 246.7, "FY2019": 28.0}),
        ("DATA", "Market risk (position, FX and commodities)", {"FY2025": 12.4, "FY2024": 13.2, "FY2023": 43.2, "FY2022": 106.3, "FY2021": 14.1, "FY2020": 0.0, "FY2019": 0.0}),
        ("DATA", "Operational risk", {"FY2025": 217.0, "FY2024": 202.8, "FY2023": 142.4, "FY2022": 141.3, "FY2021": 110.9, "FY2020": 132.0, "FY2019": 168.7}),
        ("TOTAL", "Total RWAs", {"FY2025": 327.7, "FY2024": 371.4, "FY2023": 574.7, "FY2022": 706.1, "FY2021": 805.3, "FY2020": 961.6, "FY2019": 873.2}),
        ("SECTION", "Memorandum (already inside Credit risk above — not an additional category)", {}),
        ("DATA", "Amounts below the thresholds for deduction (250% risk weight) — UK OV1 row 24", {"FY2025": 9.6, "FY2024": 66.5, "FY2023": 107.2, "FY2022": 27.9}),
    ],
    sources_text=RWA_SOURCES,
    first_col_width=68,
    unit_suffix=" (£m)",
)
metric("Leverage Ratio", "£m / %", [
    ("Total exposure measure", {"FY2025": 343.4, "FY2024": 670.0, "FY2023": 2812.0, "FY2022": 4733.0, "FY2021": 6818.1, "FY2020": 5424.1, "FY2019": 4773.6}),
    ("Leverage ratio (Pillar 3 KM1 row 14)", {"FY2025": "78.2%", "FY2024": "76.8%", "FY2023": "16.7%", "FY2022": "9.9%", "FY2021": "5.2%", "FY2020": "6.8%", "FY2019": "7.2%"}),
    ("Leverage Ratio per the audited accounts' own '4. Financial Highlights' table (more decimal places, same basis)", {"FY2025": "78.22%", "FY2024": "76.67%", "FY2023": "16.71%"}),
], note="FY2019-FY2021 are reported on the pre-2022 Basel III basis (leverage exposure INCLUDING claims on central banks); FY2022-FY2025 use the UK KM1 leverage measure EXCLUDING claims on central banks. The two are not one series - CUKL's own FY2022 report prints 'N/A' for the FY2021 comparative of these rows, footnoted as a first-time disclosure with no comparative provided.\nThe third row is the same ratio as CUKL's own audited accounts print it, to two decimal places, and is kept alongside because the FY2024 figure in earlier versions of this workbook came from there (76.67%) rather than from the Pillar 3 (76.8%) - see the FY2024 correction in the source note.")
metric("LCR", "£m / %", [
    ("Total HQLA (weighted value / average)", {"FY2025": 400.7, "FY2024": 1344.0, "FY2023": 2988.6, "FY2022": 4476.6, "FY2021": 4219.7, "FY2020": 3069.7, "FY2019": 3474.2}),
    ("Total net cash outflows (adjusted value)", {"FY2025": 20.2, "FY2024": 114.3, "FY2023": 357.5, "FY2022": 687.1, "FY2021": 639.8, "FY2020": 434.5, "FY2019": 436.6}),
    ("Liquidity coverage ratio", {"FY2025": "3089.9%", "FY2024": "1175.7%", "FY2023": "836.0%", "FY2022": "654.5%", "FY2021": "659%", "FY2020": "707%", "FY2019": "795.8%"}),
], note="FY2019-FY2021 are based on daily averages; FY2022-FY2025 use the revised UK KM1 weighted-average presentation. The FY2025 ratio of 3,089.9% is as CUKL published it: the customer deposit book fell to £77m after the wind-down of Consumer and Wealth services, so net cash outflows collapsed to £20.2m against £400.7m of HQLA.")
metric("NSFR", "£m / %", [
    ("Total available stable funding", {"FY2025": 537.3, "FY2024": 1459.8, "FY2023": 4091.4, "FY2022": 6249.1}),
    ("Total required stable funding", {"FY2025": 175.2, "FY2024": 312.0, "FY2023": 1018.8, "FY2022": 1839.5}),
    ("NSFR ratio", {"FY2025": "306.3%", "FY2024": "467.9%", "FY2023": "401.6%", "FY2022": "342.2%"}),
], note="NSFR was implemented in the UK reporting framework from 2022; no FY2021/FY2020/FY2019 NSFR figure is populated - CUKL's own FY2019 and FY2020 Pillar 3 reports both confirm NSFR was not yet a binding requirement, and its FY2022 report prints 'N/A' in the FY2021 comparative column of rows 18-20 with a footnote saying the disclosure is new and no comparatives are being provided.")
bw.add_not_disclosed_metric_sheets(
    ["MREL Ratio"],
    P3_SOURCES,
    per_note={"MREL Ratio": "The 2021 report states that no MREL eligible debt had been issued. The 2023 report states that the BoE set CUKL's MREL requirement equal to its minimum capital requirement and that no MREL eligible debt had been issued as at 31 December 2023; no numeric MREL ratio is disclosed. The 2019 report states MREL was introduced as an internal CUKL requirement effective 1 January 2020, equal to CUKL's minimum capital requirement, and that no MREL eligible debt had been issued - consistent with FY2020 and all later years."},
)

bw.add_overview_sheet(
    cash_flow_totals=[],
    cash_flow_unit=None,
    ratios=[
        ("CET1 Ratio", {"FY2025": "82.0%", "FY2024": "138.6%", "FY2023": "72.7%", "FY2022": "59.1%", "FY2021": "37.8%", "FY2020": "32.9%", "FY2019": "33.4%"}),
        ("Tier 1 Ratio", {"FY2025": "82.0%", "FY2024": "138.6%", "FY2023": "81.8%", "FY2022": "66.4%", "FY2021": "44.2%", "FY2020": "38.3%", "FY2019": "39.4%"}),
        ("Total Capital Ratio", {"FY2025": "82.0%", "FY2024": "138.6%", "FY2023": "90.8%", "FY2022": "73.8%", "FY2021": "50.7%", "FY2020": "43.7%", "FY2019": "45.3%"}),
        ("Leverage Ratio", {"FY2025": "78.2%", "FY2024": "76.8%", "FY2023": "16.7%", "FY2022": "9.9%", "FY2021": "5.2%", "FY2020": "6.8%", "FY2019": "7.2%"}),
        ("LCR", {"FY2025": "3089.9%", "FY2024": "1175.7%", "FY2023": "836.0%", "FY2022": "654.5%", "FY2021": "659%", "FY2020": "707%", "FY2019": "795.8%"}),
        ("NSFR", {"FY2025": "306.3%", "FY2024": "467.9%", "FY2023": "401.6%", "FY2022": "342.2%"}),
    ],
    balance_sheet_totals=[
        ("Total assets", {"FY2025": 362935, "FY2024": 684629, "FY2023": 3499217, "FY2022": 6487240, "FY2021": 7194284, "FY2020": 5625900, "FY2019": 4810642}),
        ("Loans and advances to customers", {"FY2025": 0, "FY2024": 160, "FY2023": 40801, "FY2022": 70599, "FY2021": 265672, "FY2020": 353748, "FY2019": 578849}),
        ("Customer accounts", {"FY2025": 77335, "FY2024": 140207, "FY2023": 2790344, "FY2022": 5672994, "FY2021": 6372454, "FY2020": 4983443, "FY2019": 4345627}),
        ("Total equity", {"FY2025": 272566, "FY2024": 517960, "FY2023": 573219, "FY2022": 489004, "FY2021": 378126, "FY2020": 404330, "FY2019": 362624}),
    ],
    balance_sheet_unit="£'000",
    income_statement_totals=[
        ("Interest receivable", {"FY2025": 19839, "FY2024": 65131, "FY2023": 160605, "FY2022": 98603, "FY2021": 42733, "FY2020": 37549, "FY2019": 17376}),
        ("Administrative expenses", {"FY2025": -26268, "FY2024": -77701, "FY2023": -95512, "FY2022": -98726, "FY2021": -61763, "FY2020": -50367, "FY2019": -12136}),
        ("Profit/(loss) for the financial year", {"FY2025": 5568, "FY2024": -57172, "FY2023": 19981, "FY2022": 21815, "FY2021": 10814, "FY2020": 25542, "FY2019": 7086}),
    ],
    income_statement_unit="£'000",
    equity_changes_totals=[
        ("Opening equity", {"FY2025": 517960, "FY2024": 573219, "FY2023": 489004, "FY2022": 378126, "FY2021": 404330, "FY2020": 362624, "FY2019": 0}),
        ("Total comprehensive income/(loss) for the year", {"FY2025": 5568, "FY2024": 1258, "FY2023": 87538, "FY2022": -85961, "FY2021": -22948, "FY2020": 44941, "FY2019": -162}),
        ("Other equity movements, net", {"FY2025": -250962, "FY2024": -56517, "FY2023": -3323, "FY2022": 196839, "FY2021": -3256, "FY2020": -3235, "FY2019": 362786}),
        ("Closing equity", {"FY2025": 272566, "FY2024": 517960, "FY2023": 573219, "FY2022": 489004, "FY2021": 378126, "FY2020": 404330, "FY2019": 362624}),
    ],
    equity_changes_unit="£'000",
    note="Every sheet now covers FY2019-FY2025. FY2025 was added 2026-09-16 from CUKL's own Pillar 3 Disclosures December 2025 and its audited Annual Financial Statements 2025 (Board-approved 24 April 2026); the same check found the FY2024 Pillar 3 report, which this workbook had previously and wrongly recorded as never published - see the correction in any Pillar 3 sheet's source note. FY2018 is deliberately excluded from every sheet: CUKL was a dormant shell throughout FY2018 (GBP 1 net assets, no PRA/FCA authorisation, no trading) per its own Companies House dormant-company filing - see ENTITY NOTE in the source cells. NSFR remains blank before FY2022, when the UK NSFR disclosure began. See source notes for the FRS 101 IAS 7 cash-flow exemption and full source coverage.",
)

bw.save("/Users/armaan/code/katalysis/banks/CITIBANK UK FINANCIALS.xlsx")
