import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook


# EXTENDED HISTORY: Afin Bank Limited's first Pillar 3 disclosure (its
# standalone regulatory reporting) is for 31 December 2024 only - the
# company was authorised as a bank with restrictions in October 2024 and
# its 2024 Pillar 3 report explicitly states no prior-period comparatives
# are provided. However, the same legal entity (company 13090556) existed
# since incorporation on 18 December 2020 under the name "All Africa
# Capital Limited" and filed ordinary Companies Act statutory accounts for
# each year back to its first accounting period. This workbook therefore
# extends FY2024's Pillar-3-only build back using those pre-authorisation
# statutory accounts for the Balance Sheet / Profit & Loss / Statement of
# Changes in Equity / Cash Flow Statement sheets (FY2021-FY2023), while the
# 11 Pillar 3 metric sheets, Asset Quality and RWA Breakdown remain
# genuinely "Not applicable" for those years - see NOT_APPLICABLE_P3_NOTE.
#
# FY2020 IS SELF-SKIPPED IN FULL (not a document-availability problem, a
# non-existence one): the company was incorporated 18 December 2020, and
# its first statutory accounts filed at Companies House cover the period
# from incorporation to 31 December 2021 (a ~13.5-month first accounting
# period) - confirmed by inspecting the filing history in full (pages 1-4,
# every accounts filing back to incorporation): the earliest accounts filed
# are for "the period ended 31 December 2021", with no discrete FY2020
# (1 Jan-31 Dec 2020) accounts ever filed, because no such period exists
# for this entity. See CH_FILING_HISTORY_URL.
YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]
YEAR_LABEL = {y: y for y in YEARS}

AR_2024_URL = "https://afinbank.com/wp-content/uploads/2025/09/Afin-Bank-Ltd-Year-End-Accounts-FV24-FINAL-SIGNED.pdf"
# FY2025 audited accounts: filed at Companies House 25 September 2026 as
# "AA - Full accounts made up to 31 December 2025" (69 pages); signed and
# authorised for issue 10 April 2026. Obtained from Companies House, NOT from
# afinbank.com. The PDF is a pure image scan with no text layer - every figure
# below was read off a 300 dpi page rendering (500 dpi for the primary
# statements), never from OCR text.
CH_2025_ACCOUNTS_URL = "https://find-and-update.company-information.service.gov.uk/company/13090556/filing-history/MzU0NzU5MDQzNmFkaXF6a2N4/document?format=pdf&download=0"
P3_2024_URL = "https://afinbank.com/wp-content/uploads/2025/09/Afin-Bank-2024-Pillar-3-Disclosures-FINAL.pdf"
CH_OVERVIEW_URL = "https://find-and-update.company-information.service.gov.uk/company/13090556"
CH_FILING_HISTORY_URL = "https://find-and-update.company-information.service.gov.uk/company/13090556/filing-history"
CH_2024_ACCOUNTS_URL = "https://find-and-update.company-information.service.gov.uk/company/13090556/filing-history/MzQ4MjgwOTc2M2FkaXF6a2N4/document?download=0&format=pdf"
CH_2023_ACCOUNTS_URL = "https://find-and-update.company-information.service.gov.uk/company/13090556/filing-history/MzQyNDA1MjMwOGFkaXF6a2N4/document?format=pdf&download=0"
CH_2022_ACCOUNTS_URL = "https://find-and-update.company-information.service.gov.uk/company/13090556/filing-history/MzM5MzI3MzYzNmFkaXF6a2N4/document?format=pdf&download=0"
CH_2021_ACCOUNTS_URL = "https://find-and-update.company-information.service.gov.uk/company/13090556/filing-history/MzM2MjY4Mzc2MGFkaXF6a2N4/document?format=pdf&download=0"

ENTITY_NOTE = (
    "ENTITY NOTE: Afin Bank Limited (company 13090556, FRN 1004742) is the UK legal entity covered here. "
    "The 2024 Pillar 3 report says the disclosure scope applies to Afin Bank Limited only; it is a majority-owned "
    "subsidiary of WAICA Reinsurance Corporation PLC, but no parent-level figures are substituted. The company was "
    "incorporated 18 December 2020 as All Africa Capital Limited, traded under that name through FY2021-FY2023, "
    "and changed its name to Afin Bank Limited after receiving banking authorisation with restrictions in "
    "October 2024. FY2021-FY2023 figures below are therefore All Africa Capital Limited's own pre-bank statutory "
    "accounts for the same continuous legal entity, sourced from Companies House (not from afinbank.com, which "
    "only hosts the FY2024 bank-era documents).\n"
    "FY2025 ADDED 2026-10-08 - THE WORKBOOK NO LONGER STOPS AT FY2024. Afin Bank Limited's audited annual "
    "report and financial statements for the year ended 31 December 2025 were filed at Companies House on "
    "25 September 2026 as 'AA - Full accounts made up to 31 December 2025' (69 pages) and were approved by the "
    "board and authorised for issue on 10 April 2026 (auditor MHA Audit Services LLP, senior statutory auditor "
    "Ahmer Khan; UNQUALIFIED opinion, no emphasis of matter and no material going-concern uncertainty, the "
    "going-concern work relying on a letter of support from the parent WAICA Reinsurance Corporation Plc; audit "
    "materiality £234,000, 1% of net assets, against £154,000 in 2024). That filing presents all four primary "
    "statements in full - none of the small-company exemptions that limited FY2021/FY2022 apply - so FY2025 "
    "fills the Balance Sheet, Profit & Loss, Statement of Changes in Equity, Cash Flow Statement and (for the "
    "first time) a real Asset Quality sheet. The document is a pure image scan with no text layer: every FY2025 "
    "figure in this workbook was read off a 300 dpi rendering of the cited page, with the primary statements "
    f"re-read at 500 dpi, and OCR was used only to navigate to a page - {CH_2025_ACCOUNTS_URL}\n"
    "This resolves the two September 2026 re-checks recorded below, both of which correctly found no FY2025 "
    "document of either kind at the time: the accounts landed on 25 September 2026, six days after the "
    "19 September check, at the statutory deadline and exactly in the pattern that check predicted.\n"
    "NO FY2025 PILLAR 3 DISCLOSURE IS IN HAND, AND THE ANNUAL REPORT IS NOT A SUBSTITUTE FOR ONE. The 11 "
    "Pillar 3 single-metric sheets, the KM1 Key Metrics sheet and the RWA Breakdown therefore carry NO FY2025 "
    "figure; their FY2025 column is deliberately left EMPTY, as a visible gap at the newest end of the "
    "workbook. The FY2025 annual report does print a 'Key Performance Indicators' table (strategic report, "
    "printed p. 6) reading Common Equity Tier 1 Ratio 290.6%, UK Leverage Ratio 46.4%, Liquidity Coverage Ratio "
    "5012.8%, Net Stable Funding Ratio 840.6%, and high quality liquid assets 79.1% of total gross assets "
    "(31 December 2024: 418.5% / 87.4% / 999999% / 492.2% / 51.7%) - but that is an annual-report KPI summary, "
    "not a Pillar 3 disclosure, and it is NOT used to fill any Pillar 3 metric sheet or the KM1 sheet. The "
    "document prints no capital amount in £, no risk-weighted exposure amount, no Tier 1 or total capital "
    "ratio, no MREL figure, and neither an OV1 nor a KM1 template anywhere. Note 23 'Capital risk management' "
    "(printed p. 60) points only to 'the Pillar 3 Disclosures, which can be found on the Bank's website', "
    "states no publication date, and gives no numeric Total Capital Requirement. Worth recording as a positive "
    "control rather than as a licence to use the table: the KPI table's four 31 December 2024 ratios reproduce "
    "the FY2024 Pillar 3 KM1 exactly, so the 2025 ratios are very probably on the same basis - which is a "
    "reason to go and find the FY2025 Pillar 3, not a reason to transcribe the annual report in its place.\n"
    "EARLIER NEGATIVE CHECKS, KEPT FOR THE RECORD (both superseded by the 25 September 2026 filing above).\n"
    "CHECKED 18 SEPTEMBER 2026 - NO FY2025 DOCUMENT THEN. Three "
    "independent routes, all positive readings rather than failed fetches. (1) The bank's own index at "
    "https://afinbank.com/about/annual-reports-and-disclosures/ returns HTTP 200 unblocked and links exactly "
    "three PDFs: the FY2024 Pillar 3, the FY2024 signed year-end accounts, and an interest-rate history. "
    "(2) The site's WordPress media REST API is open and was searched across the WHOLE library, not just the "
    "page - search=pillar, annual, accounts, disclosure, financial - and returns exactly two report documents, "
    "both FY2024, both uploaded 24 September 2025. The same API returns dozens of hits for product and "
    "rate documents dated through August 2026, so the library is live and current and the two-document result "
    "is a fact about what the bank has published, not about the query. (3) Companies House filing history for "
    "company 13090556 shows the newest accounts filing is 'AA - Full accounts made up to 31 December 2024', "
    "filed 29 September 2025; no FY2025 accounts had been filed as at 18 September 2026.\n"
    "WHEN TO LOOK AGAIN (written 18 September 2026; the prediction held): very soon. This company files at the "
    "statutory deadline - FY2024 accounts were filed "
    "29 September 2025 (the deadline for a 31 December 2024 year-end is 30 September 2025) and posted to the "
    "website on 24 September 2025; FY2023 was filed 3 June 2024. The FY2025 filing deadline is 30 SEPTEMBER "
    "2026, twelve days after this check, and the FY2024 pattern suggests the Pillar 3 and the website upload "
    "land in the same week. A re-check in October 2026 should find both. [OUTCOME: the ACCOUNTS were filed "
    "25 September 2026 and are transcribed here. The FY2025 PILLAR 3 has still not been obtained - that half "
    "of the prediction is still open and is the live gap for this bank.]\n"
    "RE-CHECKED 19 SEPTEMBER 2026 (GA-020) - STILL NO FY2025 DOCUMENT OF EITHER KIND. (1) Companies House "
    "filing history for 13090556, read UNFILTERED on page 1: the newest rows are an ANNOTATION (9 Sep 2026), "
    "RESOLUTIONS (25 Aug 2026) and SH01/SH19/SH20/CAP-SS capital filings (Jul 2026); the newest AA is still "
    "'Full accounts made up to 31 December 2024', filed 29 Sep 2025. The company profile still reads 'Next "
    "accounts made up to 31 December 2025 due by 30 September 2026'. (2) The bank's index page (HTTP 200) still "
    "links only the FY2024 Pillar 3, the FY2024 accounts and an interest-rate history dated 2026/08; the WordPress "
    "media API (search=pillar, annual, accounts, disclosure, financial, 2025, FY25) returns the same two FY2024 "
    "reports only, while its newest item is dated 9 Sep 2026, so the library is current. (Six days later the "
    "FY2025 accounts were filed at Companies House - see the FY2025 paragraph above.) Direct probes of "
    "/wp-content/uploads/2026/08/ and /2026/09/ for 'Afin-Bank-2025-Pillar-3-Disclosures-FINAL.pdf' and "
    "'Afin-Bank-Ltd-Year-End-Accounts-FV25-FINAL-SIGNED.pdf' (and the FY25 spelling) all return a genuine 404, "
    "against a 200/application/pdf/%PDF control on the FY2024 Pillar 3 URL. (3) Wayback CDX for afinbank.com "
    "from 2026 onward: 54 PDF captures, none an FY2025 report. Look again after 30 September 2026."
)

FY2020_SKIP_NOTE = (
    "FY2020 SELF-SKIPPED IN FULL: the company was incorporated 18 December 2020, so no financial year beginning "
    "1 January 2020 exists for this entity, and no such period was ever filed at Companies House. Its first "
    "statutory accounts (filed 16 December 2022) cover the period from incorporation (18 December 2020) to "
    "31 December 2021 - a single ~13.5-month first accounting period, not a discrete FY2020 followed by a "
    "discrete FY2021. This was confirmed by reading the full Companies House filing history for company 13090556 "
    "(all 4 pages, back to incorporation), not assumed from the entity-creation-date signal alone - "
    f"{CH_FILING_HISTORY_URL}"
)

NOT_APPLICABLE_P3_NOTE = (
    "NOT APPLICABLE for FY2021-FY2023: All Africa Capital Limited (this entity's name before October 2024) was "
    "not a PRA-authorised bank during FY2021-FY2023 and had no Pillar 3 disclosure obligation - its own filed "
    "accounts for those years contain no capital/liquidity/leverage/RWA figures of any kind. This is a genuine "
    "'not applicable' (no obligation existed), distinct from 'not publicly disclosed' (an obligated but unpublished "
    "figure), which is how FY2024's own non-disclosures are marked.\n"
    "RE-VERIFIED 2026-09-12 (disclosure audit): confirmed independently against the Companies House register - "
    "company 13090556 was incorporated 18 December 2020 and was named 'ALL AFRICA CAPITAL LIMITED' from "
    "18 Dec 2020 until 22 October 2024, when it was renamed Afin Bank Limited on receiving banking authorisation "
    "with restrictions. FY2021-FY2023 therefore sit wholly inside the pre-authorisation period and the blanks are "
    "structural. Also confirmed the workbook's FY2024 endpoint is still current: the latest accounts on the "
    "register are made up to 31 December 2024, with FY2025 accounts not yet filed (due 30 September 2026)."
)

# GA-020 (2026-09-19) evidenced statement texts.
NA_PREBANK = (
    "Not applicable – not a PRA-authorised bank until 18 Oct 2024 (FY2024 Pillar 3 s.1 p.2, KM1 footnote p.5; "
    "Companies House 13090556); no Pillar 3 duty for FY2021-FY2023"
)
AQ_NO_LOANS = (
    "Not applicable – no loan book at 31 Dec 2024: FY2024 annual report, strategic report credit risk, printed p.6, "
    "says the Bank 'holds no loans or receivables from customers'"
)
MREL_NOT_PUB = (
    "Not published – FY2024 Pillar 3 (7pp; KM1 pp.4-5, OV1 p.5) and FY2024 annual report contain no MREL figure "
    "or reference (checked 2026-09-19)"
)

CASH_FLOW_SOURCES = (
    "Sources - FY2025: Afin Bank Limited audited annual report and financial statements for the year ended "
    "31 December 2025, STATEMENT OF CASH FLOWS FOR THE YEAR ENDED 31 DECEMBER 2025, printed p. 39 (PDF sheet "
    f"41); supporting note 28, printed p. 66 - {CH_2025_ACCOUNTS_URL}\n"
    "FY2024: Afin Bank Limited audited annual report and financial statements for the year ended "
    f"31 December 2024, statement of cash flows, printed p. 36 - {AR_2024_URL}\n"
    "FY2023: All Africa Capital Limited audited annual report and financial statements for the year ended "
    f"31 December 2023, statement of cash flows, p. 9 (2023 column; 2022 comparative column, itself unaudited "
    f"per the auditor's report on p. 4) - {CH_2023_ACCOUNTS_URL}\n"
    "FY2022: as above (FY2023 report's own 2022 comparative column - the standalone FY2022 filing is a "
    f"balance-sheet-only unaudited filing with no cash flow statement) - {CH_2022_ACCOUNTS_URL}\n"
    "FY2021: NOT DISCLOSED - All Africa Capital Limited's first accounts (period ended 31 December 2021) take the "
    "small companies' exemption from preparing a cash flow statement (FRS 102 Section 1A); no cash flow statement "
    f"exists for this period in any source reviewed - {CH_2021_ACCOUNTS_URL}\n"
    f"Companies House filing history - {CH_FILING_HISTORY_URL}\n"
    "STRUCTURAL NOTE: FY2023/FY2022 route net interest through two new 'Interest received'/'Interest paid' rows "
    "under Operating activities (per those years' own statement); FY2024 instead reports 'Finance income' under "
    "Investing and 'Finance cost' under Financing (per that year's own statement) - both are reproduced exactly "
    "as each year's own source presents them, not forced into a single common layout.\n"
    "\nFY2025 PRESENTS A FULL CASH FLOW STATEMENT - no exemption is taken, and FY2025 is the first year in "
    "which operations GENERATED cash rather than absorbing it. Row labels on this sheet are unchanged; the "
    "FY2025 edition's own wording differs on five of them and is recorded here: 'Cash absorbed by operations' "
    "is printed 'Cash generated from/(absorbed by) operations' (note 28); 'Interest received' is printed "
    "'Interest and similar income received'; 'Interest paid' is printed 'Interest and similar expense paid'; "
    "'Net cash outflow from operating activities' is printed 'Net cash inflow/(outflow) from operating "
    "activities'; 'Purchase of investments' is printed 'Acquisition of investments'; and 'Net increase in "
    "cash and cash equivalents' is printed 'Net (decrease)/increase in cash and cash equivalents'.\n"
    "TWO NEW ROWS, in their printed positions and printed wording: 'Disposal of investments' £85,237,612 "
    "(investing activities, immediately after Acquisition of investments; note 11) and 'Share based payment "
    "movements' £29,920 (financing activities, between Proceeds from issue of shares and Payment of lease "
    "liabilities). The FY2025 edition prints a DASH as the 2024 comparative for 'Disposal of investments'; "
    "that cell is left EMPTY here, because this workbook's FY2024 column is transcribed from the FY2024 "
    "edition, which prints no such row - the dash is recorded here instead.\n"
    "TWO ROWS ARE NOT PRINTED IN FY2025 AND ARE LEFT BLANK, NOT ZERO: 'Finance income' under investing and "
    "'Finance cost' under financing. FY2025 routes interest through the two operating rows instead - the same "
    "layout FY2023/FY2022 used, so the FY2024 edition's investing/financing placement is the odd one out "
    "across the five years, and all three layouts are reproduced exactly as each edition printed them.\n"
    "ALL FOUR FY2025 SUBTOTALS FOOT EXACTLY as printed, and closing cash £2,727,794 ties to the statement of "
    "financial position. Note 28 (printed p. 66) reconciles the £7,736,229: loss for the year before income "
    "tax £(10,238,793); interest and similar expense £172,347; interest and similar income £(963,661); gain "
    "on disposal of PPE £(3,926); loss on disposal of intangibles £9,923; amortisation of intangible assets "
    "£533,759; depreciation of PPE £436,072; interest on right of use assets £73,869; impairment of "
    "intangible assets £14,539; provision for impairment charges £2,330; decrease in trade and other "
    "receivables £23,289; changes in loans to customers £(999,808); increase in trade and other payables "
    "£198,043; changes in deposits from customers £18,478,246 - which foots exactly to £7,736,229.\n"
    "FY2024 WAS RE-PRESENTED IN THE FY2025 EDITION, AND THIS SHEET'S FY2024 COLUMN IS NOT CHANGED. Both "
    "presentations are recorded, neither is reconciled. (a) 'Cash absorbed by operations': FY2024 edition "
    "£(5,854,403); FY2025 edition's 2024 comparative £(5,819,305) - £35,098 apart. (b) The FY2025 edition "
    "prints a 2024 comparative of £35,277 on an 'Interest and similar income received' row that the FY2024 "
    "edition does not have at all. (c) 'Net cash outflow from operating activities': £(5,854,403) against "
    "£(5,784,028) - £70,375 apart, being (a) plus (b). (d) 'Finance income' of £75,152 under investing is not "
    "printed in the FY2025 edition, whose 'Net cash used in investing activities' for 2024 is accordingly "
    "£(12,420,801) against this sheet's £(12,345,649), exactly £75,152 apart. (e) 'Proceeds from issue of "
    "shares': £20,523,855 against £20,256,229, with the FY2025 edition showing the £267,626 difference on its "
    "own separate 'Share based payment movements' row - the FY2024 edition lumped the two together, the "
    "FY2025 edition separates them, consistent with its own statement of changes in equity. (f) 'Finance "
    "cost' of £(4,777) under financing is not printed in the FY2025 edition, whose 'Net cash generated from "
    "financing activities' for 2024 is £20,389,072 against this sheet's £20,384,295. Everything else ties "
    "exactly across the two editions: purchase of intangible assets £(2,668,378), purchase of PPE £(52,008), "
    "acquisition of investments £(9,700,415), payment of lease liabilities £(134,783), net increase "
    "£2,184,243, opening £971,678, closing £3,155,921.\n"
    + ENTITY_NOTE + "\n" + FY2020_SKIP_NOTE
)

NO_FY2025_P3_NOTE = (
    "FY2025 IS DELIBERATELY EMPTY ON THIS SHEET, AND THE EMPTY CELL IS THE POINT. No FY2025 Pillar 3 "
    "disclosure for Afin Bank Limited has been obtained. That is a statement about what this workbook holds, "
    "not a finding that the bank published nothing - note 23 of the FY2025 annual report ('Capital risk "
    "management', printed p. 60) refers the reader to 'the Pillar 3 Disclosures, which can be found on the "
    "Bank's website', so a FY2025 edition may well exist and has simply not been fetched. The blank at the "
    "newest end of this sheet is therefore a GAP TO CHASE, and is left visible for that reason rather than "
    "being filled with something else.\n"
    "WHAT IS NOT USED TO FILL IT, AND WHY. The FY2025 annual report prints a 'Key Performance Indicators' "
    "table in its strategic report (printed p. 6): Common Equity Tier 1 Ratio 290.6%, UK Leverage Ratio "
    "46.4%, Liquidity Coverage Ratio 5012.8%, Net Stable Funding Ratio 840.6%, high quality liquid assets "
    "79.1% of total gross assets (31 December 2024: 418.5% / 87.4% / 999999% / 492.2% / 51.7%). Those figures "
    "are NOT written into any Pillar 3 metric sheet or the KM1 sheet: an annual-report KPI summary is not a "
    "Pillar 3 disclosure, and these sheets carry only what a Pillar 3 document discloses. The annual report "
    "prints no capital amount in £, no risk-weighted exposure amount, no Tier 1 or total capital ratio, no "
    "MREL figure, and neither an OV1 nor a KM1 template anywhere in its 69 pages. Worth recording: the KPI "
    "table's four 31 December 2024 ratios reproduce the FY2024 Pillar 3 KM1 exactly, which is a positive "
    "control that the 2025 figures are probably on the same basis - and therefore a reason to go and get the "
    "FY2025 Pillar 3, not a licence to transcribe the annual report in its place."
)

P3_SOURCES = (
    "Sources - Afin Bank Limited standalone Pillar 3 Disclosures for the year ended 31 December 2024:\n"
    f"FY2024: UK KM1 Key Metrics, printed pp. 4-5, and UK OV1, printed p. 5 - {P3_2024_URL}\n"
    "Afin Bank annual reports and disclosures page - https://afinbank.com/about/annual-reports-and-disclosures/\n"
    + NO_FY2025_P3_NOTE + "\n"
    + ENTITY_NOTE + "\n" + NOT_APPLICABLE_P3_NOTE
)

bw = BankWorkbook(
    bank_name="Afin Bank Limited",
    years=YEARS,
    year_label=YEAR_LABEL,
    header_color="4A1E4D",
)


BALANCE_SHEET_SOURCES = (
    "Sources - FY2025: Afin Bank Limited audited annual report and financial statements for the year ended "
    "31 December 2025, STATEMENT OF FINANCIAL POSITION AS AT 31 DECEMBER 2025, printed p. 37 (PDF sheet 39; "
    f"the printed folio runs two behind the PDF sheet throughout this document) - {CH_2025_ACCOUNTS_URL}\n"
    "FY2024: Afin Bank Limited audited annual report and financial statements for the year ended "
    f"31 December 2024, statement of financial position, printed p. 34 - {AR_2024_URL}\n"
    "FY2023: All Africa Capital Limited audited annual report and financial statements for the year ended "
    f"31 December 2023, statement of financial position, p. 7 (2023 column; 2022 comparative column) - {CH_2023_ACCOUNTS_URL}\n"
    "FY2022: All Africa Capital Limited unaudited financial statements for the year ended 31 December 2022, "
    f"balance sheet, p. 1 (cross-checked against the FY2023 report's own 2022 comparative - ties exactly) - {CH_2022_ACCOUNTS_URL}\n"
    "FY2021: All Africa Capital Limited unaudited financial statements for the period ended 31 December 2021 "
    f"(first accounting period, from incorporation 18 December 2020), balance sheet, p. 1 - {CH_2021_ACCOUNTS_URL}\n"
    + ENTITY_NOTE
    + "\nSTRUCTURAL NOTES: (1) 'Treasury assets', 'Right-of-use assets', 'Revaluation reserve' and 'Share based "
    "payment reserve' are all genuinely new line items that first appear on the FY2024 face statement (post-"
    "banking-authorisation) - left blank, not zero, for FY2021-FY2023, where the underlying asset/liability class "
    "simply did not exist on the company's books. (2) FY2023's face statement combines right-of-use assets into "
    "the single 'Property, plant and equipment' line (its own note 10 breaks out Computer equipment £22,098 + "
    "Right of use asset £130,091 = £152,189); FY2022/FY2021 predate IFRS 16 entirely (no leases). (3) FY2021's "
    "'Debtors' £19,562 is a single undifferentiated line (no prepayments split existed yet) - reproduced under "
    "'Receivables' with FY2021's own 'Prepayments' cell left blank rather than zero. (4) 'Receivables' for "
    "FY2023 combines the current £147,604 and non-current £19,200 other-receivables notes into one face-equivalent "
    "figure, consistent with how FY2024's own single 'Receivables' row is presented. (5) 'Treasury assets' note "
    "10 (Listed investments, non-current, printed p. 44) discloses only the single lump £9,767,797 figure with no "
    "further split - the note's narrative and the accounting policy note (note 1.7 'Financial asset investments "
    f"under IFRS 9', printed p. 38) both state these are UK government securities (gilts and Treasury bills) "
    "classified as debt instruments measured at fair value through other comprehensive income (FVOCI). Note 1.7's "
    "own fair-value disclosure (p. 38) further splits the £9,767,797 total by instrument as UK Gilts £5,813,980 + "
    "Treasury Bills £3,953,817 (reconciles exactly), but since both instruments share the same issuer type (UK "
    "government) and the same measurement basis (FVOCI), there is no real split by either dimension - the row is "
    f"labelled in place rather than broken into sub-rows - {AR_2024_URL}\n"
    "\nFY2025 EDITION - FOUR ROWS RENAMED, TWO ROWS ADDED, AND ONE RESERVE THAT CHANGED MEANING AS WELL AS "
    "NAME. The row LABELS in this sheet are the ones this workbook has carried since the FY2024 build and are "
    "deliberately left unchanged, so that a column is never silently re-based; what the FY2025 edition prints "
    "instead is recorded here. (1) 'Treasury assets - UK Government gilts & Treasury bills, at FVOCI' is "
    "printed in FY2025 simply as 'Investments' (note 11, printed p. 53). It is the same asset class under a "
    "shorter name: note 11 still reads 'government securities, including UK gilts and Treasury bills ... "
    "measured at FVOCI'. Note 11 also splits it current/non-current - at 31 December 2025 the whole £34,820,044 "
    "is CURRENT and the non-current cell is a printed dash (2024: £5,935,817 current + £3,831,980 non-current) "
    "- and gives the movement: at 1 January 2025 £9,767,797; additions £109,977,186; accrued interest on "
    "acquisitions £366,483; fair value adjustment through OCI £(53,810); disposals £(85,237,612); at "
    "31 December 2025 £34,820,044 (foots exactly). (2) 'Prepayments' is printed in FY2025 as 'Other assets' "
    "(note 14); the identity is confirmed by that row's own 2024 comparative, £372,022, which is exactly this "
    "workbook's FY2024 'Prepayments'. (3) 'Share based payment reserve' is printed in FY2025 as 'Share "
    "premium' (note 22), carrying the same static £267,626 as FY2024. (4) 'Revaluation reserve' is printed in "
    "FY2025 as 'Other reserves' (note 21) AND HAS CHANGED MEANING, not just name - this is the one relabelling "
    "that is not cosmetic. Note 21 (printed p. 59) states 'Other reserves is comprised of fair value "
    "adjustments relating to FVOCI assets in 2025 and 2024. Other reserves is also comprised of the share "
    "based payment reserve', and breaks the £44,646 down as: at 1 January £67,382; other comprehensive loss "
    "£(52,656); share based payment reserve £47,079; share based payments £(17,159); at 31 December £44,646. "
    "So FY2025's figure MIXES the FVOCI revaluation with share-based-payment movements, while the FY2024 "
    "figure of £67,382 in the same row is a pure FVOCI revaluation. The two are NOT on the same basis, and the "
    "earlier year has deliberately NOT been retro-fitted to the new meaning: the edition that changed it is "
    "the FY2025 annual report, and both figures stand as each edition reported them. (£47,079 less £17,159 is "
    "the £29,920 that the statement of changes in equity shows as the FY2025 'Share based payments' movement - "
    "a cross-check, not a derivation.) The £17,159 is explained in the same note: in December 2025 a payment "
    "of £17,159 was made to a departing employee in relation to their B shareholding.\n"
    "TWO NEW ROWS, both printed for the first time in FY2025 and both with a PRINTED DASH as their 2024 "
    "comparative: 'Loans to customers' £1,004,721 (note 12, printed p. 53), third asset row, between "
    "Investments and Receivables; and 'Deposits from customers' £18,648,096 (note 17, printed p. 56), the "
    "FIRST liability row, above Trade and other payables. Their FY2024 cells are left EMPTY rather than "
    "carrying that dash, because this workbook's FY2024 column is transcribed from the FY2024 edition, whose "
    "own statement of financial position has no such row at all; the dash is recorded here instead. Both "
    "columns foot exactly as printed (assets £44,037,548; liabilities £20,735,053; net assets and total equity "
    "£23,302,495), and every one of the FY2025 edition's 2024 comparatives on this statement ties exactly to "
    "the FY2024 figures already in this workbook - no balance-sheet comparative was re-presented.\n"
    "ONE FIGURE THE BANK PRINTS TWO WAYS, REPRODUCED AS PRINTED AND NOT RECONCILED: note 17's narrative line "
    "reads 'total deposits from customers at 31 December 2025 was £18,648,095', one pound below the "
    "£18,648,096 printed on the face of the statement and in note 17's own table. The FACE figure is the one "
    "carried here, because it is the one that makes total liabilities foot; the narrative figure is recorded "
    "but not adopted. Note 17 also splits the deposits current £8,928,176 / non-current £11,719,920 (2024: "
    "both a printed dash).\n"
    + FY2020_SKIP_NOTE
)

INCOME_STATEMENT_SOURCES = (
    "Sources - FY2025: Afin Bank Limited audited annual report and financial statements for the year ended "
    "31 December 2025, STATEMENT OF COMPREHENSIVE INCOME FOR THE YEAR ENDED 31 DECEMBER 2025, printed p. 36 "
    f"(PDF sheet 38) - {CH_2025_ACCOUNTS_URL}\n"
    "FY2024: Afin Bank Limited audited annual report and financial statements for the year ended "
    f"31 December 2024, statement of comprehensive income, printed p. 33 - {AR_2024_URL}\n"
    "FY2023: All Africa Capital Limited audited annual report and financial statements for the year ended "
    f"31 December 2023, statement of comprehensive income p. 6 and operating loss note 5 p. 14 (2023 column; "
    f"2022 comparative column, itself unaudited) - {CH_2023_ACCOUNTS_URL}\n"
    "FY2022: as above (FY2023 report's own 2022 comparative and note 5 breakdown - the standalone FY2022 filing "
    f"states the directors elected not to include a P&L account within the filed financial statements) - {CH_2022_ACCOUNTS_URL}\n"
    "FY2021: NOT DISCLOSED - the directors of All Africa Capital Limited elected not to include a copy of the "
    "profit and loss account within the filed financial statements for the period ended 31 December 2021 (a "
    f"small-companies filing exemption); no P&L breakdown exists in any source reviewed - {CH_2021_ACCOUNTS_URL}\n"
    + ENTITY_NOTE
    + "\nSTRUCTURAL NOTE: FY2023/FY2022's own administrative-expenses note (note 5) splits costs as Staff costs / "
    "Computer running costs / Legal and professional fees / Consultancy fees / Audit fees / Depreciation / Other "
    "costs and separately discloses 'Other operating income' (£231 in FY2022, £nil in FY2023) - reproduced as "
    "its own set of rows rather than force-mapped onto FY2024's differently-labelled 'Other operating costs' "
    "bucket. Both years' figures were verified to foot exactly to the reported Administrative expenses total.\n"
    "\nFY2025 RESHAPED THE TOP OF THIS STATEMENT - A NET INTEREST INCOME BLOCK WAS ADDED. FY2025 runs: "
    "Interest and similar income (note 3) -> Interest and similar expense (note 4) -> NET INTEREST INCOME -> "
    "Allowance for credit losses -> NET OPERATING INCOME -> the expense block -> Total operating expenses "
    "(note 7) -> OPERATING LOSS -> Income tax expense (note 9) -> LOSS FOR THE YEAR. The five new lines are "
    "added above in the bank's printed order and printed wording. Expense components (Staff costs, "
    "Depreciation, Amortisation of intangibles, Other operating costs) are printed UNBRACKETED in an inner "
    "column, with only the 'Total operating expenses' subtotal bracketed; they are signed negative here, as in "
    "every earlier year of this sheet.\n"
    "FOUR ROWS OF THIS SHEET ARE SIMPLY NOT PRINTED IN FY2025 AND ARE LEFT BLANK, NOT ZERO: 'Other operating "
    "income'; 'Finance income' and 'Finance costs' (superseded by the new interest block - see the "
    "re-presentation note below); and 'LOSS BEFORE TAXATION', which FY2025 does not print at all. FY2025's "
    "'Operating loss' now occupies the position this sheet's 'Loss before taxation' row held, and the two are "
    "the same number, £(10,238,793) - but a line the bank did not print is not written into a row, so the "
    "figure sits on 'Operating loss' only.\n"
    "'INCOME TAX EXPENSE' FY2025 IS A PRINTED DASH, NOT A ZERO, and is carried as the literal '-'. (The "
    "FY2024 edition's own figure is left exactly as this workbook has always carried it. The FY2025 edition "
    "prints a dash in its 2024 comparative column too - a glyph change, recorded here, not applied.)\n"
    "THE OTHER COMPREHENSIVE INCOME BLOCK GAINED A SUB-HEADING AND A SECOND LINE. FY2025 prints 'Other "
    "comprehensive income:' then the sub-heading 'Items that may be reclassified to profit or loss', then two "
    "lines: 'Net change in fair value of FVOCI investments' £(53,810) - which is this sheet's existing "
    "'Treasury asset revaluation' row under a new name, carried in place with the label unchanged - and the "
    "genuinely NEW 'Net change in ECL on FVOCI investments' £1,154, added in its printed position with its "
    "printed wording. The FY2025 edition prints a DASH as the 2024 comparative for that new line; it is left "
    "blank here for the same reason as the new balance-sheet rows. The subtotal is printed as 'Other "
    "comprehensive (loss)/income for the year' £(52,656) and the bottom line as 'Total comprehensive loss for "
    "the year' £(10,291,449); both sit on this sheet's existing, unchanged row labels. Note 11 (printed p. 53) "
    "and note 24 (printed p. 63) together explain the two OCI lines: the £(53,810) is the fair value "
    "adjustment through OCI on the investment portfolio, and the £1,154 is an ECL on FVOCI investments which "
    "'does not reduce the carrying value of the asset'.\n"
    "FY2024 WAS RE-PRESENTED IN THE FY2025 EDITION. THE FY2024 FIGURES IN THIS SHEET ARE NOT CHANGED, AND THE "
    "TWO PRESENTATIONS ARE NOT RECONCILED - BOTH ARE RECORDED HERE, each with the edition that printed it. "
    "The loss is identical on both presentations, £(6,193,551); what moved is where three amounts sit. "
    "(a) 'Other operating costs': FY2024 edition £2,149,595; FY2025 edition's 2024 comparative £2,161,565 - "
    "£11,970 higher, being the FY2024 'Finance costs' of £11,970 absorbed into operating costs. (b) 'Total "
    "operating expenses': FY2024 edition £(6,256,733); FY2025 edition's 2024 comparative £(6,268,703) - the "
    "same £11,970. (c) 'Operating loss': FY2024 edition £(6,256,733); FY2025 edition's 2024 comparative "
    "£(6,193,551) - a £63,182 difference that is the caption being repositioned one block lower, below the "
    "finance lines, not a change of measurement. (d) 'Finance income' £75,152 is not printed under that name "
    "in the FY2025 edition; it appears there as 'Interest and similar income' at the TOP of the statement, "
    "same amount. (e) 'Finance costs' £(11,970) is not printed at all in the FY2025 edition - see (a). "
    "Everything else ties exactly across the two editions: Staff costs £3,941,455, Depreciation £142,504, "
    "Amortisation of intangibles £23,179, Loss for the year £(6,193,551), other comprehensive income £67,382, "
    "total comprehensive loss £(6,126,169).\n"
    "THE FY2025 SUBTOTALS CASCADE, WHICH IS WHY SOME OF THEM DO NOT ADD UP FROM THE LINES DIRECTLY ABOVE "
    "THEM. 'Net operating income' £788,984 is 'Net interest income' £791,314 less 'Allowance for credit "
    "losses' £2,330 - a subtotal feeding the next subtotal, exactly as the bank prints it. The same shape "
    "already runs through the rest of this statement in every year: 'Loss before taxation' is the operating "
    "loss plus the finance lines, and 'Loss for the year' is the loss before taxation plus tax. Every figure "
    "here is the bank's own printed figure and none has been adjusted to make any run of rows sum to the "
    "subtotal beneath it. 'Net interest income' is tagged as a bold subtotal because the statement prints it "
    "bold. (As at 2026-10-08 the repository's generic DATA-run reconciliation reported these cascades as "
    "mismatches, as it does on other banks' profit and loss sheets for the same reason; that is a property of "
    "a flat-shaped check, not of the figures.)\n"
    + FY2020_SKIP_NOTE
)

EQUITY_CHANGES_SOURCES = (
    "Sources - FY2025: Afin Bank Limited audited annual report and financial statements for the year ended "
    "31 December 2025, STATEMENT OF CHANGES IN EQUITY FOR THE YEAR ENDED 31 DECEMBER 2025, printed p. 38 "
    "(PDF sheet 40), covering 1 January 2024 to 31 December 2025 - "
    f"{CH_2025_ACCOUNTS_URL}\n"
    "FY2024: Afin Bank Limited audited annual report and financial statements for the year ended "
    f"31 December 2024, statement of changes in equity, p. 35, covering 1 January 2023 to 31 December 2024 - {AR_2024_URL}\n"
    "FY2021-FY2023: All Africa Capital Limited's own statement of changes in equity (FY2023 report, p. 8, "
    f"covering 1 January 2022 to 31 December 2023) - {CH_2023_ACCOUNTS_URL} - plus the FY2021 first-period "
    f"balance sheet (opening/closing bridge derived from its own reported balances) - {CH_2021_ACCOUNTS_URL}\n"
    + ENTITY_NOTE
    + "\nThis sheet now runs chronologically from incorporation (18 December 2020) through 31 December 2024, the "
    "one sheet in the workbook not self-skipping FY2020: even though no discrete FY2020 accounts exist (see "
    "FY2020_SKIP_NOTE), the equity roll-forward correctly shows the company's true opening position at "
    "incorporation (£0) as its own row, with the first accounting period's entire movement (18 December 2020 to "
    "31 December 2021) shown as a single aggregate line - the small-companies filing exemption from including a "
    "P&L account means no finer split of that movement is available from any source.\n"
    "\nTHE SECOND AND THIRD COLUMNS CHANGED MEANING IN THE FY2025 EDITION, AND THE EARLIER YEARS HAVE NOT BEEN "
    "RETRO-FITTED. The FY2025 statement's own column headers are: Share capital | Other reserves | Share "
    "premium | Retained earnings | Total. This sheet's headers are, and remain, Share capital | Revaluation "
    "reserve | Share based payment | Retained earnings | Total equity. The edition that changed them is the "
    "FY2025 annual report. Two distinct things changed:\n"
    "(a) NAME. 'Revaluation reserve' is the column the FY2025 edition calls 'Other reserves'; 'Share based "
    "payment' is the column it calls 'Share premium'. The 1 January 2024 and 31 December 2024 balances are "
    "identical across both editions (3,357,807 / - / - / (2,395,628) / 962,179 and 23,614,036 / 67,382 / "
    "267,626 / (8,589,179) / 15,359,865), so the columns are the same columns; only the captions moved.\n"
    "(b) MEANING, which is the part that matters. In the FY2024 edition the £267,626 share-based-payment "
    "movement sits in the THIRD column; in the FY2025 edition the £29,920 share-based-payment movement sits "
    "in the SECOND column, alongside the FVOCI revaluation, because note 21 (printed p. 59) now defines "
    "'Other reserves' as comprising BOTH the FVOCI fair value adjustments AND the share based payment "
    "reserve. The bank moved the item between columns between editions. This sheet reproduces each year's "
    "movement in the column the bank put it in THAT YEAR - FY2024's £267,626 in the third column, FY2025's "
    "£29,920 in the second - and does NOT rewrite FY2021-FY2024 to the new meaning. A reader comparing the "
    "second column across 2024 and 2025 is therefore comparing two different definitions, and must not treat "
    "the column as one continuous series. Note 21's own breakdown of the FY2025 figure: at 1 January £67,382; "
    "other comprehensive loss £(52,656); share based payment reserve £47,079; share based payments "
    "£(17,159); at 31 December £44,646 - and £47,079 less £17,159 is exactly the £29,920 shown here.\n"
    "FY2025 ROWS AS PRINTED. The FY2025 statement prints, under the heading 'Year ended 31 December 2025:', "
    "Loss for the year; Other comprehensive loss; Total comprehensive loss; the heading 'Transactions with "
    "owners:'; Issue of share capital (note 21); Share based payments (note 21); Balance at 31 December 2025. "
    "Every blank cell in that block is a PRINTED DASH, not an omission, and every column rolls forward "
    "exactly from the printed 31 December 2024 balances. Row labels on this sheet carry the year in brackets, "
    "as they have since the FY2024 build, so that a chronological roll-forward spanning five reporting "
    "periods stays readable.\n"
    "NO FY2024 COMPARATIVE ON THIS STATEMENT WAS RE-PRESENTED: every 2024 figure the FY2025 edition prints "
    "ties exactly to the figures already in this sheet. The only change to 2024 is the column caption in (a).\n"
    + FY2020_SKIP_NOTE
)

ASSET_QUALITY_SOURCES = (
    "Sources - FY2025: Afin Bank Limited audited annual report and financial statements for the year ended "
    "31 December 2025 - note 12 'Loans to customers', printed p. 53 (PDF sheet 55); note 24 'Financial risk "
    "management - Credit risk', maximum-exposure tables, printed p. 63 (PDF sheet 65); note 24 continued, "
    "'Net carrying amount of exposure by risk grade and stage' and 'Expected credit loss by risk grade and "
    f"stage', printed p. 64 (PDF sheet 66) - {CH_2025_ACCOUNTS_URL}\n"
    f"FY2024: Afin Bank Limited 2024 Annual Report - {AR_2024_URL} - and 2024 Pillar 3 Disclosures - "
    f"{P3_2024_URL}\n"
    + ENTITY_NOTE
    + "\nTHIS SHEET WAS A SINGLE 'NOT APPLICABLE' ROW UNTIL FY2025, AND THAT FY2024 FINDING STILL STANDS: "
    f"\"{AQ_NO_LOANS}\". The FY2024 balance sheet has no lending line at all. The bank launched its lending "
    "products during 2025 - the FY2025 strategic report (printed p. 6) describes the year's key target as "
    "'to launch into the market, following the removal of the deposit taking restrictions and to develop the "
    "suite of mortgage products' - so FY2025 is the first year this sheet carries real figures.\n"
    "WHAT FY2025 ACTUALLY DISCLOSES, AND WHAT IT DOES NOT. Note 12 gives the loan book's three components. "
    "Note 24 gives maximum exposure to credit risk on three measures (gross exposure, ECL provision, net "
    "exposure) across four exposure classes, and then grades the whole credit book Strong / Good / "
    "Satisfactory / Weak against IFRS 9 Stage 1 / Stage 2 / Stage 3. There is NO product-level split of the "
    "loan book in this document - no residential versus buy-to-let table - and NO non-performing-loan or "
    "coverage-ratio table. That is a real absence in the source, not a gap in transcription, and it has an "
    "obvious reason: EVERY Stage 2 and Stage 3 cell in both of note 24's grade tables is a printed dash. All "
    "£42,808,740 of net exposure sits in Stage 1, so at 31 December 2025 there is nothing non-performing for "
    "an NPL ratio to measure. The 'Weak' grade row is likewise a printed dash throughout. Because Stage 2 and "
    "Stage 3 are empty, Stage 1 equals Total in both tables, and the two grade blocks below are labelled "
    "Stage 1 accordingly rather than being padded out with rows of dashes.\n"
    "THE FY2024 COLUMN OF THE EXPOSURE BLOCKS COMES FROM THE FY2025 EDITION, WHICH IS SAID OUT LOUD HERE "
    "BECAUSE IT IS THE ONLY PLACE IN THIS WORKBOOK WHERE THAT HAPPENS. Note 24's second maximum-exposure "
    "table is headed 'As at 31 December 2024' and is the first credit-risk exposure table Afin has published "
    "for that date; the FY2024 edition contains no equivalent. Nothing is being overwritten - those cells "
    "were empty - and no FY2024 figure anywhere else in this workbook is touched. Within that 2024 table, "
    "cash £3,155,921 and investments £9,767,797 are printed figures and are carried; loans to customers and "
    "off-balance-sheet loan commitments are printed DASHES and are left blank, consistent with the bank "
    "having had no loan book; every ECL cell for 2024 is a printed dash, so the whole FY2024 ECL block is "
    "blank. The note states explicitly: 'In 2024, all exposures were in stage 1 and there was no ECL "
    "reported.' The FY2024 gross and net totals are each £12,923,718, as printed.\n"
    "FIGURES CARRIED HERE THAT ARE WORTH KNOWING THE PROVENANCE OF. 'Loans to customers' gross exposure in "
    "note 24 is £1,005,226, which is note 12's £999,808 principal plus £5,418 accrued interest; the net "
    "£1,004,721 is that less the £505 ECL and is the figure on the face of the balance sheet. The "
    "off-balance-sheet loan commitments of £4,256,852 gross are UNDRAWN COMMITMENTS and are therefore NOT on "
    "the balance sheet - the exposure blocks below total more than total assets for that reason, which is "
    "correct and not a footing error. Note 24 also states 'The impact of the provisioning calculations "
    "performed under IFRS 9 on the balance sheet as at 31 December 2025 is £2,370 (2024: nil)', which is a "
    "different figure from the £1,176 ECL provision in the exposure table and from the £2,330 total expected "
    "credit loss in the grade table - the bank prints all three, they are reproduced as printed, and none is "
    "adjusted to agree with another. The £1,154 of the £2,330 that relates to FVOCI investments is the same "
    "£1,154 shown on the Profit & Loss sheet as the new OCI line; note 24 says it 'does not reduce the "
    "carrying value of the asset and therefore does not impact the exposure to credit risk', which is why "
    "the investments row shows a dash in the ECL block.\n"
    "ALSO IN THE DOCUMENT, NOT REPRODUCED AS ROWS: the IFRS 9 three-stage policy, the significant-increase-"
    "in-credit-risk criteria and the 90-days-past-due default definition (printed p. 46), and the ECL "
    "scenario weighting (printed p. 49).\n"
    + "\nNOT APPLICABLE (FY2023-FY2021):\n"
    + NOT_APPLICABLE_P3_NOTE
)

RWA_BREAKDOWN_SOURCES = (
    "Sources - Afin Bank Limited standalone Pillar 3 Disclosures for the year ended 31 December 2024:\n"
    f"FY2024: UK OV1 - Overview of risk weighted exposure amounts (Table 2), printed p. 5 - {P3_2024_URL}\n"
    "FY2024 figures are directly disclosed (not derived): Credit risk (excluding CCR) £2,489k + Operational risk "
    "£598k = £3,087k, which reconciles exactly to the Total RWAs sheet's own FY2024 figure of £3,087k (UK KM1, "
    "row 4). No counterparty credit risk, securitisation or market risk rows are shown in Afin Bank's own OV1 "
    "table (rows 2-22 and 24-28 of the standard OV1 template are blank/not populated), consistent with a small, "
    "newly-authorised institution with no trading book or derivatives exposure - not a gap in transcription.\n"
    + NO_FY2025_P3_NOTE + "\n"
    + ENTITY_NOTE
    + "\nNOT APPLICABLE / NOT DISCLOSED (FY2023-FY2021): as above (see NOT_APPLICABLE_P3_NOTE) - the entity had no "
    "Pillar 3 disclosure obligation for these years.\n"
    + NOT_APPLICABLE_P3_NOTE
)

bw.add_balance_sheet_sheet(
    title="Afin Bank Limited — Consolidated Statement of Financial Position",
    subtitle=(
        "Afin Bank Limited (All Africa Capital Limited pre-October 2024) audited/unaudited statement of "
        "financial position; amounts in £. FY2021 covers the first accounting period, 18 Dec 2020-31 Dec 2021 "
        "(FY2020 does not exist as a discrete period - see source note). FY2025 adds 'Loans to customers' and "
        "'Deposits from customers'; four rows were renamed in the FY2025 edition and 'Revaluation reserve' "
        "changed MEANING as well as name - labels here are unchanged and the change is documented in the "
        "source note."
    ),
    rows=[
        ("SECTION", "Assets", {}),
        ("DATA", "Cash and cash equivalents", {"FY2025": 2727794, "FY2024": 3155921, "FY2023": 971678, "FY2022": 7333, "FY2021": 86318}),
        ("DATA", "Treasury assets - UK Government gilts & Treasury bills, at FVOCI", {"FY2025": 34820044, "FY2024": 9767797}),
        ("DATA", "Loans to customers", {"FY2025": 1004721}),
        ("DATA", "Receivables", {"FY2025": 226057, "FY2024": 450628, "FY2023": 166804, "FY2022": 6859, "FY2021": 19562}),
        ("DATA", "Prepayments", {"FY2025": 559842, "FY2024": 372022, "FY2023": 50123, "FY2022": 0}),
        ("DATA", "Property, plant and equipment", {"FY2025": 115718, "FY2024": 57172, "FY2023": 152189, "FY2022": 360, "FY2021": 487}),
        ("DATA", "Right-of-use assets", {"FY2025": 766773, "FY2024": 967204}),
        ("DATA", "Intangible assets", {"FY2025": 3816599, "FY2024": 2657199, "FY2023": 12000}),
        ("TOTAL", "Total assets", {"FY2025": 44037548, "FY2024": 17427943, "FY2023": 1352794, "FY2022": 14552, "FY2021": 106367}),
        ("SECTION", "Liabilities", {}),
        ("DATA", "Deposits from customers", {"FY2025": 18648096}),
        ("DATA", "Trade and other payables", {"FY2025": 1301608, "FY2024": 1102894, "FY2023": 260524, "FY2022": 50338, "FY2021": 59537}),
        ("DATA", "Lease liabilities", {"FY2025": 785349, "FY2024": 965184, "FY2023": 130091, "FY2022": 0}),
        ("TOTAL", "Total liabilities", {"FY2025": 20735053, "FY2024": 2068078, "FY2023": 390615, "FY2022": 50338, "FY2021": 59537}),
        ("TOTAL", "Net assets", {"FY2025": 23302495, "FY2024": 15359865, "FY2023": 962179, "FY2022": -35786, "FY2021": 46830}),
        ("SECTION", "Equity", {}),
        ("DATA", "Called up share capital", {"FY2025": 41818195, "FY2024": 23614036, "FY2023": 3357807, "FY2022": 590654, "FY2021": 266750}),
        ("DATA", "Revaluation reserve", {"FY2025": 44646, "FY2024": 67382}),
        ("DATA", "Share based payment reserve", {"FY2025": 267626, "FY2024": 267626}),
        ("DATA", "Retained earnings", {"FY2025": -18827972, "FY2024": -8589179, "FY2023": -2395628, "FY2022": -626440, "FY2021": -219920}),
        ("TOTAL", "Total equity", {"FY2025": 23302495, "FY2024": 15359865, "FY2023": 962179, "FY2022": -35786, "FY2021": 46830}),
    ],
    sources_text=BALANCE_SHEET_SOURCES,
    first_col_width=48,
    source_height=210,
    unit_suffix=" (£)",
)

bw.add_income_statement_sheet(
    title="Afin Bank Limited — Consolidated Statement of Comprehensive Income",
    subtitle=(
        "Afin Bank Limited (All Africa Capital Limited pre-October 2024) audited/unaudited statement of "
        "comprehensive income; amounts in £. FY2021 NOT DISCLOSED (small-companies exemption - see source "
        "note). FY2025 adds the bank's new net interest income block and a second OCI line, and does not print "
        "'Other operating income', 'Finance income', 'Finance costs' or 'Loss before taxation' at all - those "
        "cells are blank, not zero. FY2024 was re-presented in the FY2025 edition; the FY2024 figures here are "
        "as FY2024 reported them and both presentations are recorded in the source note."
    ),
    rows=[
        ("SECTION", "Net interest income (FY2025 presentation)", {}),
        ("DATA", "Interest and similar income", {"FY2025": 963661}),
        ("DATA", "Interest and similar expense", {"FY2025": -172347}),
        ("TOTAL", "Net interest income", {"FY2025": 791314}),
        ("DATA", "Allowance for credit losses", {"FY2025": -2330}),
        ("TOTAL", "Net operating income", {"FY2025": 788984}),
        ("SECTION", "Operating income and expenses", {}),
        ("DATA", "Other operating income", {"FY2023": 0, "FY2022": 231}),
        ("DATA", "Staff costs", {"FY2025": -6260752, "FY2024": -3941455, "FY2023": -1088800, "FY2022": -224067}),
        ("DATA", "Computer running costs", {"FY2023": -45103, "FY2022": -3026}),
        ("DATA", "Legal and professional fees", {"FY2023": -166504, "FY2022": -42042}),
        ("DATA", "Consultancy fees", {"FY2023": -276803, "FY2022": -123016}),
        ("DATA", "Audit fees", {"FY2023": -8760, "FY2022": 0}),
        ("DATA", "Depreciation", {"FY2025": -436072, "FY2024": -142504, "FY2023": -21488, "FY2022": -127}),
        ("DATA", "Amortisation of intangibles", {"FY2025": -533759, "FY2024": -23179, "FY2023": 0}),
        ("DATA", "Other operating costs", {"FY2025": -3797194, "FY2024": -2149595}),
        ("TOTAL", "Total operating expenses", {"FY2025": -11027777, "FY2024": -6256733, "FY2023": -1767933, "FY2022": -406751}),
        ("TOTAL", "Operating loss", {"FY2025": -10238793, "FY2024": -6256733, "FY2023": -1767933, "FY2022": -406520}),
        ("DATA", "Finance income", {"FY2024": 75152, "FY2023": 8}),
        ("DATA", "Finance costs", {"FY2024": -11970, "FY2023": -1263}),
        ("TOTAL", "Loss before taxation", {"FY2024": -6193551, "FY2023": -1769188, "FY2022": -406520}),
        ("DATA", "Income tax expense", {"FY2025": "-", "FY2024": 0, "FY2023": 0, "FY2022": 0}),
        ("TOTAL", "Loss for the year", {"FY2025": -10238793, "FY2024": -6193551, "FY2023": -1769188, "FY2022": -406520}),
        ("SECTION", "Other comprehensive income", {}),
        ("SECTION", "Items that may be reclassified to profit or loss", {}),
        ("DATA", "Treasury asset revaluation", {"FY2025": -53810, "FY2024": 67382, "FY2023": 0, "FY2022": 0}),
        ("DATA", "Net change in ECL on FVOCI investments", {"FY2025": 1154}),
        ("TOTAL", "Total other comprehensive income for the year", {"FY2025": -52656, "FY2024": 67382, "FY2023": 0, "FY2022": 0}),
        ("TOTAL", "Total comprehensive income for the year", {"FY2025": -10291449, "FY2024": -6126169, "FY2023": -1769188, "FY2022": -406520}),
    ],
    sources_text=INCOME_STATEMENT_SOURCES,
    first_col_width=48,
    source_height=210,
    unit_suffix=" (£)",
)

EQUITY_HEADERS = ["Share capital", "Revaluation reserve", "Share based payment", "Retained earnings", "Total equity"]
bw.add_equity_changes_sheet(
    title="Afin Bank Limited — Statement of Changes in Equity",
    subtitle=(
        "Afin Bank Limited (All Africa Capital Limited pre-October 2024) statement of changes in equity, "
        "18 December 2020 (incorporation) to 31 December 2025; amounts in £. The FY2025 edition renamed "
        "columns 2 and 3 to 'Other reserves' and 'Share premium' and moved the share-based-payment movement "
        "from column 3 into column 2; earlier years are NOT restated to that meaning - see the source note."
    ),
    headers=EQUITY_HEADERS,
    rows=[
        ("TOTAL", "Balance at 18 December 2020 (date of incorporation)", (0, None, None, 0, 0)),
        ("DATA", "Total comprehensive income for the period (18 Dec 2020 to 31 Dec 2021)", (None, None, None, -219920, -219920)),
        ("DATA", "Issue of share capital (2021)", (266750, None, None, None, 266750)),
        ("TOTAL", "Balance at 31 December 2021", (266750, 0, 0, -219920, 46830)),
        ("DATA", "Total comprehensive income for the year (2022)", (None, None, None, -406520, -406520)),
        ("DATA", "Issue of share capital (2022)", (323904, None, None, None, 323904)),
        ("TOTAL", "Balance at 1 January 2023", (590654, None, None, -626440, -35786)),
        ("DATA", "Total comprehensive income for the year (2023)", (None, None, None, -1769188, -1769188)),
        ("DATA", "Issue of share capital (2023)", (2767153, None, None, None, 2767153)),
        ("TOTAL", "Balance at 31 December 2023", (3357807, 0, 0, -2395628, 962179)),
        ("DATA", "Loss for the year (2024)", (None, None, None, -6193551, -6193551)),
        ("DATA", "Other comprehensive income - Treasury asset revaluation (2024)", (None, 67382, None, None, 67382)),
        ("TOTAL", "Total comprehensive income for the year (2024)", (None, 67382, None, -6193551, -6126169)),
        ("DATA", "Issue of share capital (2024)", (20256229, None, None, None, 20256229)),
        ("DATA", "Share based payment (2024)", (None, None, 267626, None, 267626)),
        ("TOTAL", "Balance at 31 December 2024", (23614036, 67382, 267626, -8589179, 15359865)),
        ("DATA", "Loss for the year (2025)", (None, None, None, -10238793, -10238793)),
        ("DATA", "Other comprehensive loss (2025)", (None, -52656, None, None, -52656)),
        ("TOTAL", "Total comprehensive loss for the year (2025)", (None, -52656, None, -10238793, -10291449)),
        ("DATA", "Issue of share capital (2025)", (18204159, None, None, None, 18204159)),
        ("DATA", "Share based payments (2025)", (None, 29920, None, None, 29920)),
        ("TOTAL", "Balance at 31 December 2025", (41818195, 44646, 267626, -18827972, 23302495)),
    ],
    sources_text=EQUITY_CHANGES_SOURCES,
    source_height=210,
)

bw.add_cash_flow_sheet(
    title="Afin Bank Limited — Cash Flow Statement",
    subtitle=(
        "Afin Bank Limited (All Africa Capital Limited pre-October 2024) audited/unaudited statement of cash "
        "flows; amounts in £. FY2021 NOT DISCLOSED (small-companies exemption - see source note). FY2025 is "
        "the first year operations generated rather than absorbed cash; it adds 'Disposal of investments' and "
        "'Share based payment movements' and prints no 'Finance income'/'Finance cost' rows. FY2024's cash "
        "flow comparatives were re-presented in the FY2025 edition - this sheet keeps FY2024 as FY2024 "
        "reported it and records both in the source note."
    ),
    rows=[
        ("SECTION", "Cash flows from operating activities", {}),
        ("DATA", "Cash absorbed by operations", {"FY2025": 7736229, "FY2024": -5854403, "FY2023": -1746327, "FY2022": -402889}),
        ("DATA", "Interest received", {"FY2025": 605222, "FY2023": 8, "FY2022": 0}),
        ("DATA", "Interest paid", {"FY2025": -2498, "FY2023": -1263, "FY2022": 0}),
        ("TOTAL", "Net cash outflow from operating activities", {"FY2025": 8338953, "FY2024": -5854403, "FY2023": -1747582, "FY2022": -402889}),
        ("SECTION", "Investing activities", {}),
        ("DATA", "Purchase of intangible assets", {"FY2025": -1717621, "FY2024": -2668378, "FY2023": -12000, "FY2022": 0}),
        ("DATA", "Purchase of property, plant and equipment", {"FY2025": -113812, "FY2024": -52008, "FY2023": -19717, "FY2022": 0}),
        ("DATA", "Purchase of investments", {"FY2025": -109977186, "FY2024": -9700415}),
        ("DATA", "Disposal of investments", {"FY2025": 85237612}),
        ("DATA", "Finance income", {"FY2024": 75152}),
        ("TOTAL", "Net cash used in investing activities", {"FY2025": -26571007, "FY2024": -12345649, "FY2023": -31717, "FY2022": 0}),
        ("SECTION", "Financing activities", {}),
        ("DATA", "Proceeds from issue of shares", {"FY2025": 18204159, "FY2024": 20523855, "FY2023": 2767153, "FY2022": 323904}),
        ("DATA", "Share based payment movements", {"FY2025": 29920}),
        ("DATA", "Payment of lease liabilities", {"FY2025": -430152, "FY2024": -134783, "FY2023": -23509, "FY2022": 0}),
        ("DATA", "Finance cost", {"FY2024": -4777}),
        ("TOTAL", "Net cash generated from financing activities", {"FY2025": 17803927, "FY2024": 20384295, "FY2023": 2743644, "FY2022": 323904}),
        ("TOTAL", "Net increase in cash and cash equivalents", {"FY2025": -428127, "FY2024": 2184243, "FY2023": 964345, "FY2022": -78985}),
        ("DATA", "Cash and cash equivalents at the beginning of the year", {"FY2025": 3155921, "FY2024": 971678, "FY2023": 7333, "FY2022": 86318}),
        ("TOTAL", "Cash and cash equivalents at the end of the year", {"FY2025": 2727794, "FY2024": 3155921, "FY2023": 971678, "FY2022": 7333, "FY2021": 86318}),
    ],
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=62,
    source_height=225,
    unit_suffix=" (£)",
)


bw.add_asset_quality_sheet(
    title="Afin Bank Limited — Asset Quality / Credit Risk Disclosures",
    subtitle=(
        "Afin Bank Limited loan book / credit risk disclosures; amounts in £. FY2025 is the first year with a "
        "loan book: the bank launched lending in 2025 and held no loans or receivables from customers at "
        "31 December 2024. Every Stage 2 and Stage 3 cell in the bank's own grade tables is a printed dash, "
        "so all exposure is Stage 1 and the document contains no NPL or coverage ratio - see the source note."
    ),
    rows=[
        ("SECTION", "Loans to customers (note 12, printed p. 53)", {}),
        ("DATA", "Loans to customers", {"FY2025": 999808}),
        ("DATA", "Accrued interest on loans to customers", {"FY2025": 5418}),
        ("DATA", "Expected credit loss on loans to customers", {"FY2025": -505}),
        ("TOTAL", "Loans to customers - net carrying amount", {"FY2025": 1004721}),
        ("SECTION", "Maximum exposure to credit risk - gross exposure (note 24, printed p. 63)", {}),
        ("DATA", "Cash and cash equivalents - gross exposure", {"FY2025": 2727794, "FY2024": 3155921}),
        ("DATA", "Loans to customers - gross exposure", {"FY2025": 1005226}),
        ("DATA", "Investments - gross exposure", {"FY2025": 34820044, "FY2024": 9767797}),
        ("DATA", "Off-balance sheet loan commitments - gross exposure", {"FY2025": 4256852}),
        ("TOTAL", "Maximum exposure to credit risk - total gross exposure", {"FY2025": 42809916, "FY2024": 12923718}),
        ("SECTION", "Maximum exposure to credit risk - ECL provision (note 24, printed p. 63)", {}),
        ("DATA", "Cash and cash equivalents - ECL provision", {}),
        ("DATA", "Loans to customers - ECL provision", {"FY2025": 505}),
        ("DATA", "Investments - ECL provision", {}),
        ("DATA", "Off-balance sheet loan commitments - ECL provision", {"FY2025": 671}),
        ("TOTAL", "Maximum exposure to credit risk - total ECL provision", {"FY2025": 1176}),
        ("SECTION", "Maximum exposure to credit risk - net exposure (note 24, printed p. 63)", {}),
        ("DATA", "Cash and cash equivalents - net exposure", {"FY2025": 2727794, "FY2024": 3155921}),
        ("DATA", "Loans to customers - net exposure", {"FY2025": 1004721}),
        ("DATA", "Investments - net exposure", {"FY2025": 34820044, "FY2024": 9767797}),
        ("DATA", "Off-balance sheet loan commitments - net exposure", {"FY2025": 4256181}),
        ("TOTAL", "Maximum exposure to credit risk - total net exposure", {"FY2025": 42808740, "FY2024": 12923718}),
        ("SECTION", "Net carrying amount of exposure by risk grade, Stage 1 (note 24, printed p. 64)", {}),
        ("DATA", "Strong - Stage 1", {"FY2025": 37547838}),
        ("DATA", "Good - Stage 1", {"FY2025": 3545767}),
        ("DATA", "Satisfactory - Stage 1", {"FY2025": 1715135}),
        ("DATA", "Weak - Stage 1", {}),
        ("TOTAL", "Total net carrying amount - Stage 1", {"FY2025": 42808740}),
        ("SECTION", "Expected credit loss by risk grade, Stage 1 (note 24, printed p. 64)", {}),
        ("DATA", "Strong - Stage 1 ECL", {"FY2025": 1154}),
        ("DATA", "Good - Stage 1 ECL", {"FY2025": 689}),
        ("DATA", "Satisfactory - Stage 1 ECL", {"FY2025": 487}),
        ("DATA", "Weak - Stage 1 ECL", {}),
        ("TOTAL", "Total expected credit loss - Stage 1", {"FY2025": 2330}),
        ("SECTION", "Not applicable", {}),
        ("DATA", "Not publicly disclosed / Not applicable", {
            "FY2023": NA_PREBANK,
            "FY2022": NA_PREBANK,
            "FY2021": NA_PREBANK,
        }),
    ],
    sources_text=ASSET_QUALITY_SOURCES,
    first_col_width=58,
    source_height=180,
    unit_suffix=" (£)",
)


def metric(name, unit, rows_data, note=None):
    bw.add_metric_sheet(
        name,
        unit,
        rows_data,
        P3_SOURCES,
        note=note,
        first_col_width=56,
        source_height=180,
    )


# ---------------------------------------------------------------
# Sheet: KM1 Key Metrics (KM1-003)
# ---------------------------------------------------------------
# ONE COLUMN, AND THE BANK SAYS WHY. Afin prints a single 31/12/2024 column
# and footnotes it: "*We were authorised as a bank by the PRA (with
# restrictions) in Oct 2024. Therefore we do not provide comparative
# information for the prior periods." That is the document declaring the
# exclusion, which is a far stronger finding than a year we merely failed to
# locate - FY2023/FY2022/FY2021 are blank here because no KM1 obligation or
# disclosure existed, not because none was found.
#
# THE FULL TEMPLATE, INCLUDING ITS DASHED ROWS. Afin prints the complete UK KM1
# row set, including UK 8a, UK 9a, 10 and UK 10a - each as a DASH, re-read off
# the FY2024 PDF on 2026-09-18. Each of those four cells carries a literal "-":
# the dash is Afin stating the requirement does not apply to it, which is a
# different statement from a blank. That matters here
# because this same table also prints GENUINE ZEROES two blocks below (UK 16a
# and row 16 are "0", not "-"), so the two glyphs appear in one column and mean
# different things. Recording the dashes as zeros would assert that Afin has a
# systemic risk buffer requirement of exactly nil where the bank in fact
# disclosed nothing.
#
# ROW 17 IS A SENTINEL, NOT A RATIO, AND IS REPRODUCED AS PUBLISHED (rule 7).
# Afin prints "999999%" for the liquidity coverage ratio with its own
# footnote: "(1) We are currently authorised as a bank by the PRA (with
# restrictions). At present we do not have any qualifying cash outflows.
# Therefore our LCR is reported as 999999%." It follows directly from row 16
# being a printed zero. It is carried verbatim rather than blanked or capped:
# blanking it would hide a disclosure the bank made, and "fixing" it would
# invent a number the bank did not publish.
#
# PRECISION IS THE BANK'S OWN (rule 3): row 8 prints "2.5%" while row 9 prints
# "2%", and UK 11a and row 12 print "147%" and "276%" with no decimals at all,
# in the same column as "418.5%" and "142.5%". Not normalised.
#
# The table BREAKS ACROSS PAGES (rule 12): rows 1-14 and the "Liquidity
# Coverage Ratio" heading sit on p.4, rows 15-20 and both footnotes on p.5.
# The citation names both pages.
km1_rows = [
    ("SECTION", "Available own funds (amounts)", {}),
    ("DATA", "1  Common Equity Tier 1 (CET1) capital (£'000)", {"FY2024": 12922}),
    ("DATA", "2  Tier 1 capital (£'000)", {"FY2024": 12922}),
    ("DATA", "3  Total capital (£'000)", {"FY2024": 12922}),
    ("SECTION", "Risk-weighted exposure amounts", {}),
    ("DATA", "4  Total risk-weighted exposure amount (£'000)", {"FY2024": 3087}),
    ("SECTION", "Capital ratios (as a percentage of risk-weighted exposure amount)", {}),
    ("DATA", "5  Common Equity Tier 1 ratio (%)", {"FY2024": "418.5%"}),
    ("DATA", "6  Tier 1 ratio (%)", {"FY2024": "418.5%"}),
    ("DATA", "7  Total capital ratio (%)", {"FY2024": "418.5%"}),
    ("SECTION", "Additional own funds requirements based on SREP (as a percentage of risk-weighted exposure amount)", {}),
    ("DATA", "UK 7a  Additional CET1 SREP requirements (%)", {"FY2024": "75.7%"}),
    ("DATA", "UK 7b  Additional AT1 SREP requirements (%)", {"FY2024": "25.2%"}),
    ("DATA", "UK 7c  Additional T2 SREP requirements (%)", {"FY2024": "33.6%"}),
    ("DATA", "UK 7d  Total SREP own funds requirements (%)", {"FY2024": "142.5%"}),
    ("SECTION", "Combined buffer requirement (as a percentage of risk-weighted exposure amount)", {}),
    ("DATA", "8  Capital conservation buffer (%)", {"FY2024": "2.5%"}),
    ("DATA", "UK 8a  Conservation buffer due to macro-prudential or systemic risk identified at the "
             "level of a Member State (%)", {"FY2024": "-"}),
    ("DATA", "9  Institution specific countercyclical capital buffer (%)", {"FY2024": "2%"}),
    ("DATA", "UK 9a  Systemic risk buffer (%)", {"FY2024": "-"}),
    ("DATA", "10  Global Systemically Important Institution buffer (%)", {"FY2024": "-"}),
    ("DATA", "UK 10a  Other Systemically Important Institution buffer", {"FY2024": "-"}),
    ("DATA", "11  Combined buffer requirement (%)", {"FY2024": "4.5%"}),
    ("DATA", "UK 11a  Overall capital requirements (%)", {"FY2024": "147%"}),
    ("DATA", "12  CET1 available after meeting the total SREP own funds requirements (%)", {"FY2024": "276%"}),
    ("SECTION", "Leverage ratio", {}),
    ("DATA", "13  Total exposure measure excluding claims on central banks (£'000)", {"FY2024": 14782}),
    ("DATA", "14  Leverage ratio excluding claims on central banks (%)", {"FY2024": "87.4%"}),
    ("SECTION", "Liquidity Coverage Ratio", {}),
    ("DATA", "15  Total high-quality liquid assets (HQLA) (Weighted value - average) (£'000)", {"FY2024": 8909}),
    ("DATA", "UK 16a  Cash outflows - Total weighted value (£'000)", {"FY2024": 0}),
    ("DATA", "UK 16b  Cash inflows - Total weighted value (£'000)", {"FY2024": 3971}),
    ("DATA", "16  Total net cash outflows (adjusted value) (£'000)", {"FY2024": 0}),
    ("DATA", "17  Liquidity coverage ratio (%)", {"FY2024": "999999%"}),
    ("SECTION", "Net Stable Funding Ratio", {}),
    ("DATA", "18  Total available stable funding (£'000)", {"FY2024": 21486}),
    ("DATA", "19  Total required stable funding (£'000)", {"FY2024": 4365}),
    ("DATA", "20  NSFR ratio (%)", {"FY2024": "492.2%"}),
]

KM1_SOURCES = (
    "Sources - Afin Bank Limited's own published UK KM1 template, reproduced in its own row order, row "
    "numbers, labels and precision. Amounts in £'000 as published.\n"
    f"FY2024: Afin Bank 2024 Pillar 3 Disclosures, pp.4-5, 'Table 1 UK KM1 - Key Metrics', column 31/12/2024 "
    f"- {P3_2024_URL}\n"
    "The table BREAKS ACROSS A PAGE: rows 1-14 and the 'Liquidity Coverage Ratio' heading on p.4, rows 15-20 "
    "and both of the bank's footnotes on p.5. A citation naming only p.4 would send a checker to a page that "
    "does not contain the liquidity rows.\n"
    "ENTITY: Afin Bank Limited (company 13090556) only. The document states the template 'has been disclosed "
    "in accordance with Annex I and Annex II of the Disclosure (CRR) Part of the PRA Rulebook'.\n"
    "\n"
    + NO_FY2025_P3_NOTE + "\n"
    "\n"
    "WHY FY2024 IS THE ONLY COLUMN WITH FIGURES - AT THE OLD END, THE BANK STATES IT.\n"
    "Footnote to the column header: \"*We were authorised as a bank by the PRA (with restrictions) in Oct "
    "2024. Therefore we do not provide comparative information for the prior periods.\" FY2023, FY2022 and "
    "FY2021 are blank because Afin was not an authorised bank and published no KM1 for those years - a "
    "declared exclusion, not a document we failed to find, and not a figure to be back-filled from the "
    "statutory accounts, which are a different basis.\n"
    "\n"
    "TWO MISSING-VALUE GLYPHS APPEAR IN THIS ONE COLUMN AND THEY MEAN DIFFERENT THINGS.\n"
    "Rows UK 8a, UK 9a, 10 and UK 10a are printed as a DASH and are therefore left BLANK here (map rule 2): "
    "the bank disclosed no figure, which is not the same as disclosing nil. Rows UK 16a and 16 are printed as "
    "'0' and are recorded as genuine zeroes. Both glyphs sit in the same column of the same table, so "
    "normalising either one would misstate what Afin published.\n"
    "\n"
    "ROW 17 IS PUBLISHED AS '999999%' AND IS REPRODUCED, NOT CORRECTED (rule 7).\n"
    "Afin's own footnote: \"(1) We are currently authorised as a bank by the PRA (with restrictions). At "
    "present we do not have any qualifying cash outflows. Therefore our LCR is reported as 999999%.\" It is a "
    "sentinel standing for an undefined ratio - row 16, the denominator, is a printed zero - and it is carried "
    "exactly as disclosed. It is not a conventional finite ratio and should not be charted or compared as one.\n"
    "\n"
    "THE FIGURES ARE SMALL AND THE RATIOS EXTREME, AND THAT IS CORRECT AS PUBLISHED. Total risk-weighted "
    "exposures of £3,087k against CET1 of £12,922k give the printed 418.5% capital ratios, and the SREP "
    "requirement is correspondingly high (UK 7d 142.5%). This is what a bank authorised with restrictions in "
    "October 2024, two months before its year-end, actually looks like; none of it is derived here.\n"
    "\n"
    "PRECISION IS THE BANK'S OWN (rule 3): row 8 prints '2.5%' while row 9 prints '2%', and UK 11a and row 12 "
    "print '147%' and '276%' without decimals, in the same column as '418.5%' and '142.5%'.\n"
    "\n"
    "SDDT STATUS - INTENT, NOT A WAIVER. The report's section 3.4 says that under the proposals in CP 7/24 "
    "Afin 'would meet the definition of a Small Domestic Deposit Taker (SDDT) and intends to become an SDDT, "
    "if this proposed regulatory change is implemented', in which case it 'would therefore no longer be "
    "required to make Pillar 3 disclosures under CRR Article 433b'. That is a stated future intention "
    "contingent on a consultation, NOT a PRA Rulebook Rule 3.1 election, and it removes no disclosure duty for "
    "FY2024 - which is why a full KM1 exists for this year.\n"
    "\n"
    "LATEST-EDITION CHECK, RE-RUN 18 SEPTEMBER 2026 - NONE NEWER, ON POSITIVE EVIDENCE. Afin's own index at "
    "https://afinbank.com/about/annual-reports-and-disclosures/ reads successfully (HTTP 200, unblocked) and "
    "lists exactly three PDFs: this 2024 Pillar 3 document, the FY2024 signed year-end accounts, and an "
    "interest-rate history. The 2024 edition is the newest Pillar 3 published. This check went further than the "
    "2026-09-16 one: the site's WordPress media REST API is open and was searched across the whole library "
    "(search=pillar / annual / accounts / disclosure / financial), which returns those same two FY2024 report "
    "documents and nothing else, against dozens of product and rate PDFs dated through August 2026 - so the "
    "library is live and the negative is about the bank's publishing, not about the index page. Companies "
    "House agrees: the newest accounts filing for company 13090556 is 'Full accounts made up to 31 December "
    "2024', filed 29 September 2025. See the entity note for the publication lag and when to look again."
)

bw.add_km1_sheet(
    title="Afin Bank Limited - KM1 Key Metrics",
    subtitle="Afin Bank's own published UK KM1 template, in its own row order, row numbers, labels and "
             "precision. Amounts in £'000; ratios as printed. FY2024 is the only column with figures: at the "
             "old end FY2023-FY2021 are blank because the bank was authorised (with restrictions) only in "
             "October 2024 and states it provides no prior-period comparatives; at the new end FY2025 is "
             "blank because no FY2025 Pillar 3 disclosure has been obtained - the FY2025 annual report's KPI "
             "ratios are not a Pillar 3 disclosure and are deliberately NOT used here. "
             "Dashed rows carry the dash Afin printed; the zeroes in UK 16a and row 16 are the bank's own. "
             "Row 17 is published as 999999% - see the sources note.",
    rows=km1_rows,
    sources_text=KM1_SOURCES,
    first_col_width=70,
    source_height=320,
    years=YEARS,
)

metric("CET1 Capital", "£'000", [
    ("Common Equity Tier 1 (CET1) capital", {"FY2024": 12922, "FY2023": NA_PREBANK, "FY2022": NA_PREBANK, "FY2021": NA_PREBANK}),
])
metric("CET1 Ratio", "% of RWA", [
    ("Common Equity Tier 1 (CET1) ratio", {"FY2024": "418.5%", "FY2023": NA_PREBANK, "FY2022": NA_PREBANK, "FY2021": NA_PREBANK}),
])
metric("Tier 1 Capital", "£'000", [
    ("Tier 1 capital", {"FY2024": 12922, "FY2023": NA_PREBANK, "FY2022": NA_PREBANK, "FY2021": NA_PREBANK}),
])
metric("Tier 1 Ratio", "% of RWA", [
    ("Tier 1 ratio", {"FY2024": "418.5%", "FY2023": NA_PREBANK, "FY2022": NA_PREBANK, "FY2021": NA_PREBANK}),
])
metric("Total Capital", "£'000", [
    ("Total capital", {"FY2024": 12922, "FY2023": NA_PREBANK, "FY2022": NA_PREBANK, "FY2021": NA_PREBANK}),
])
metric("Total Capital Ratio", "% of RWA", [
    ("Total capital ratio", {"FY2024": "418.5%", "FY2023": NA_PREBANK, "FY2022": NA_PREBANK, "FY2021": NA_PREBANK}),
])
metric("Total RWAs", "£'000", [
    ("Total risk-weighted exposure amount", {"FY2024": 3087, "FY2023": NA_PREBANK, "FY2022": NA_PREBANK, "FY2021": NA_PREBANK}),
])
bw.add_rwa_breakdown_sheet(
    title="Afin Bank Limited — RWA Breakdown",
    subtitle=(
        "Afin Bank Limited risk-weighted exposure amount breakdown; amounts in £'000. FY2024 per the Pillar 3 "
        "UK OV1 template; FY2023-FY2021 not applicable (entity not yet a PRA-authorised bank); FY2025 blank "
        "because no FY2025 Pillar 3 disclosure has been obtained and the FY2025 annual report prints no RWA "
        "figure of any kind - a gap to chase, see the source note."
    ),
    rows=[
        ("SECTION", "UK OV1 — Overview of risk weighted exposure amounts", {}),
        ("DATA", "Credit risk (excluding CCR)", {"FY2024": 2489}),
        ("DATA", "Operational risk", {"FY2024": 598}),
        ("TOTAL", "Total risk weighted exposure amount", {"FY2024": 3087}),
        ("SECTION", "Not applicable", {}),
        ("DATA", "Not publicly disclosed / Not applicable", {
            "FY2023": NA_PREBANK,
            "FY2022": NA_PREBANK,
            "FY2021": NA_PREBANK,
        }),
    ],
    sources_text=RWA_BREAKDOWN_SOURCES,
    first_col_width=58,
    source_height=180,
    unit_suffix=" (£'000)",
)
metric("Leverage Ratio", "£'000 / %", [
    ("Total exposure measure excluding claims on central banks", {"FY2024": 14782, "FY2023": NA_PREBANK, "FY2022": NA_PREBANK, "FY2021": NA_PREBANK}),
    ("Leverage ratio excluding claims on central banks", {"FY2024": "87.4%", "FY2023": NA_PREBANK, "FY2022": NA_PREBANK, "FY2021": NA_PREBANK}),
])
metric("LCR", "£'000 / %", [
    ("Total high-quality liquid assets (HQLA) (weighted value - average)", {"FY2024": 8909, "FY2023": NA_PREBANK, "FY2022": NA_PREBANK, "FY2021": NA_PREBANK}),
    ("Cash outflows - total weighted value", {"FY2024": 0, "FY2023": NA_PREBANK, "FY2022": NA_PREBANK, "FY2021": NA_PREBANK}),
    ("Cash inflows - total weighted value", {"FY2024": 3971, "FY2023": NA_PREBANK, "FY2022": NA_PREBANK, "FY2021": NA_PREBANK}),
    ("Total net cash outflows (adjusted value)", {"FY2024": 0, "FY2023": NA_PREBANK, "FY2022": NA_PREBANK, "FY2021": NA_PREBANK}),
    ("Liquidity coverage ratio", {"FY2024": "999999%", "FY2023": NA_PREBANK, "FY2022": NA_PREBANK, "FY2021": NA_PREBANK}),
], note=(
    "Afin states that it had no qualifying cash outflows at 31 December 2024; the source therefore reports the "
    "LCR as 999999%. This is reproduced as reported and is not interpreted as a conventional finite ratio. "
    "FY2021-FY2023 predate Afin's banking authorisation - no LCR obligation existed."
))
metric("NSFR", "£'000 / %", [
    ("Total available stable funding", {"FY2024": 21486, "FY2023": NA_PREBANK, "FY2022": NA_PREBANK, "FY2021": NA_PREBANK}),
    ("Total required stable funding", {"FY2024": 4365, "FY2023": NA_PREBANK, "FY2022": NA_PREBANK, "FY2021": NA_PREBANK}),
    ("NSFR ratio", {"FY2024": "492.2%", "FY2023": NA_PREBANK, "FY2022": NA_PREBANK, "FY2021": NA_PREBANK}),
])
metric("MREL Ratio", None, [
    ("MREL ratio", {"FY2024": MREL_NOT_PUB, "FY2023": NA_PREBANK, "FY2022": NA_PREBANK, "FY2021": NA_PREBANK}),
], note=(
    "No numeric MREL ratio is disclosed in the 2024 Pillar 3 report or the audited annual accounts for FY2024. "
    "FY2021-FY2023 predate Afin's banking authorisation (October 2024), so no MREL obligation existed for those years."
))


bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {"FY2025": 44037548, "FY2024": 17427943, "FY2023": 1352794, "FY2022": 14552, "FY2021": 106367}),
        ("Deposits from customers", {"FY2025": 18648096}),
        ("Trade and other payables", {"FY2025": 1301608, "FY2024": 1102894, "FY2023": 260524, "FY2022": 50338, "FY2021": 59537}),
        ("Total equity", {"FY2025": 23302495, "FY2024": 15359865, "FY2023": 962179, "FY2022": -35786, "FY2021": 46830}),
    ],
    balance_sheet_unit="£",
    income_statement_totals=[
        ("Total operating expenses", {"FY2025": -11027777, "FY2024": -6256733, "FY2023": -1767933, "FY2022": -406751}),
        ("Loss for the year", {"FY2025": -10238793, "FY2024": -6193551, "FY2023": -1769188, "FY2022": -406520}),
    ],
    income_statement_unit="£",
    equity_changes_totals=[
        ("Opening equity", {"FY2025": 15359865, "FY2024": 962179, "FY2023": -35786, "FY2022": 46830, "FY2021": 0}),
        ("Total comprehensive income", {"FY2025": -10291449, "FY2024": -6126169, "FY2023": -1769188, "FY2022": -406520, "FY2021": -219920}),
        ("Other movements, net", {"FY2025": 18234079, "FY2024": 20523855, "FY2023": 2767153, "FY2022": 323904, "FY2021": 266750}),
        ("Closing equity", {"FY2025": 23302495, "FY2024": 15359865, "FY2023": 962179, "FY2022": -35786, "FY2021": 46830}),
    ],
    equity_changes_unit="£",
    cash_flow_totals=[
        ("Net cash outflow from operating activities", {"FY2025": 8338953, "FY2024": -5854403, "FY2023": -1747582, "FY2022": -402889}),
        ("Net cash used in investing activities", {"FY2025": -26571007, "FY2024": -12345649, "FY2023": -31717, "FY2022": 0}),
        ("Net cash generated from financing activities", {"FY2025": 17803927, "FY2024": 20384295, "FY2023": 2743644, "FY2022": 323904}),
        ("Cash and cash equivalents at end of year", {"FY2025": 2727794, "FY2024": 3155921, "FY2023": 971678, "FY2022": 7333, "FY2021": 86318}),
    ],
    cash_flow_unit="£",
    ratios=[
        ("CET1 Ratio", {"FY2024": "418.5%", "FY2023": "Not applicable", "FY2022": "Not applicable", "FY2021": "Not applicable"}),
        ("Tier 1 Ratio", {"FY2024": "418.5%", "FY2023": "Not applicable", "FY2022": "Not applicable", "FY2021": "Not applicable"}),
        ("Total Capital Ratio", {"FY2024": "418.5%", "FY2023": "Not applicable", "FY2022": "Not applicable", "FY2021": "Not applicable"}),
        ("Leverage Ratio", {"FY2024": "87.4%", "FY2023": "Not applicable", "FY2022": "Not applicable", "FY2021": "Not applicable"}),
        ("LCR", {"FY2024": "999999%", "FY2023": "Not applicable", "FY2022": "Not applicable", "FY2021": "Not applicable"}),
        ("NSFR", {"FY2024": "492.2%", "FY2023": "Not applicable", "FY2022": "Not applicable", "FY2021": "Not applicable"}),
    ],
    note=(
        "FY2025 ADDED 2026-10-08, AND IT IS THE YEAR AFIN BECAME A BANK IN SUBSTANCE RATHER THAN IN LICENCE. "
        "Afin launched lending and deposit-taking during 2025 after the removal of its deposit-taking "
        "restrictions, and the shape of the statements changes accordingly: a net interest income block "
        "appears at the top of the profit and loss account for the first time (interest and similar income "
        "£963,661 less expense £172,347, net £791,314); the balance sheet gains 'Loans to customers' "
        "£1,004,721 and 'Deposits from customers' £18,648,096, neither of which existed at 31 December 2024; "
        "total assets grow from £17.43m to £44.04m; the Asset Quality sheet carries real figures for the "
        "first time, having been a single 'not applicable' row before; and operations generated £7.74m of "
        "cash where every prior year absorbed it. The loss widened to £(10,238,793) as the cost base scaled "
        "up (staff costs £6,260,752 against £3,941,455), and £18,204,159 of fresh share capital was issued. "
        "Source: the audited annual report and financial statements for the year ended 31 December 2025, "
        "filed at Companies House 25 September 2026 and signed 10 April 2026, unqualified opinion, no "
        "material going-concern uncertainty.\n"
        "THE RATIO BLOCK BELOW HAS NO FY2025 ENTRY, DELIBERATELY. No FY2025 Pillar 3 disclosure has been "
        "obtained for this bank, so the 11 Pillar 3 metric sheets, the KM1 Key Metrics sheet and the RWA "
        "Breakdown all carry an empty FY2025 column, and that blank is left visible as a gap to chase. The "
        "FY2025 annual report does print capital and liquidity ratios in a strategic-report KPI table "
        "(CET1 290.6%, UK leverage 46.4%, LCR 5012.8%, NSFR 840.6% at 31 December 2025), but an annual-report "
        "KPI summary is not a Pillar 3 disclosure and those figures are not used on any Pillar 3 sheet. See "
        "the KM1 and metric sheets' own source notes.\n"
        "TWO EDITION-LEVEL FINDINGS, BOTH RECORDED AND NEITHER RECONCILED. (1) The FY2025 edition RE-PRESENTS "
        "several FY2024 comparatives on the profit and loss account and the cash flow statement; this "
        "workbook's FY2024 column is unchanged and both presentations are set out on those two sheets. (2) "
        "The two reserve columns of the statement of changes in equity were renamed AND one of them changed "
        "meaning - FY2025's 'Other reserves' mixes the FVOCI revaluation with share-based payments, which "
        "FY2024's did not - and earlier years have NOT been retro-fitted to the new meaning.\n"
        "EXTENDED HISTORY: this workbook now covers FY2021-FY2025 (five years), extended back from an original "
        "FY2024-only Pillar-3-only build. Afin Bank Limited was named All Africa Capital Limited and was not yet "
        "a PRA-authorised bank until October 2024, so FY2021-FY2023's Balance Sheet/P&L/Equity/Cash Flow figures "
        "are that same continuous legal entity's own pre-bank Companies House statutory accounts, while all 11 "
        "Pillar 3 metric sheets plus Asset Quality and RWA Breakdown are genuinely 'Not applicable' for those "
        "three years (no disclosure obligation existed) - only FY2024 carries real Pillar 3 figures. "
        "FY2020 is self-skipped in full: the company was incorporated 18 December 2020 and its first statutory "
        "accounts cover the period from incorporation to 31 December 2021 - no discrete FY2020 period was ever "
        "filed, because none exists for this entity (confirmed by reading the complete Companies House filing "
        "history, not assumed from the entity-creation-date signal alone). FY2021's Profit & Loss and Cash Flow "
        "Statement are themselves NOT DISCLOSED (small-companies filing exemptions - no P&L account or cash flow "
        "statement was ever filed for that period); only its Balance Sheet and the equity roll-forward derived "
        "from it are available. Genuine structural findings, all documented on their own sheets: FY2023 is the "
        "first year with intangible assets, a lease/right-of-use asset, and an audit (FY2021-FY2022 were "
        "unaudited small-company filings); the FY2023 report's own 2022 comparative column is itself unaudited "
        "per its auditor's report. Every closing cash and equity balance ties exactly into the next year's own "
        "opening balance across all five years, including into the pre-existing FY2024 figures unchanged from "
        "the original build and on into FY2025 (closing cash £3,155,921 and closing equity £15,359,865 at "
        "31 December 2024 are FY2025's own printed opening balances)."
    ),
)

bw.save("/Users/armaan/code/katalysis/banks/AFIN BANK FINANCIALS.xlsx")
