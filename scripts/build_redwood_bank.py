import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook


YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021", "FY2020", "FY2019", "FY2018", "FY2017"]
YEAR_LABEL = {y: y for y in YEARS}

AR2025_URL = "https://redwoodbank.co.uk/media/howpdnen/2025-annual-report-and-accounts_redwood-bank-signed-150426.pdf"
AR2024_URL = "https://redwoodbank.co.uk/media/0h5hp3ku/2024-redwood-bank-annual-report-and-accounts.pdf"
AR2023_URL = "https://redwoodbank.co.uk/media/zrjnifqm/redwood-year-end-annual-report-and-accounts-2023-1.pdf"
CH_URL = "https://find-and-update.company-information.service.gov.uk/company/09872265/filing-history"
CH2022_URL = "https://find-and-update.company-information.service.gov.uk/company/09872265/filing-history/MzM4NjEzNjAwN2FkaXF6a2N4/document?download=0&format=pdf"
CH2021_FILING_URL = "https://find-and-update.company-information.service.gov.uk/company/09872265/filing-history/MzMxNTg5MTEzOWFkaXF6a2N4/document?download=0&format=pdf"
CH2020_FILING_URL = "https://find-and-update.company-information.service.gov.uk/company/09872265/filing-history/MzI3OTU5MDgxMmFkaXF6a2N4/document?download=0&format=pdf"
CH2019_FILING_URL = "https://find-and-update.company-information.service.gov.uk/company/09872265/filing-history/MzI0NTgzMDAyMWFkaXF6a2N4/document?download=0&format=pdf"
CH2018_FILING_URL = "https://find-and-update.company-information.service.gov.uk/company/09872265/filing-history/MzIxNTgzNTUxNWFkaXF6a2N4/document?download=0&format=pdf"

ENTITY_NOTE = (
    "ENTITY NOTE: Redwood Bank Limited (company 09872265, FRN 755924) is the exact legal entity in the bank list. "
    "It is a UK-authorised bank and a wholly owned subsidiary of Redwood Financial Partners Limited. The annual "
    "reports present the Bank on a Company-only basis; no Group cash-flow statement has been substituted. The "
    "company was previously named Acorn Financial Partners Limited, but the name change occurred before the years "
    "covered and does not create an entity ambiguity."
)

FLOOR_NOTE = (
    "HISTORICAL FLOOR NOTE (HD-020): the entity (company 09872265) was incorporated on 13 November 2015 as Acorn "
    "Financial Partners Limited, but this is NOT the Bank's real disclosure floor. Its FY2015/FY2016 Companies "
    "House filings (the FY2016 one is the earliest on file, a 13-page 'total exemption full accounts' filing for "
    "the period ended 31 December 2016) show a dormant pre-launch shell with no banking licence, no loans, no "
    "deposits, and a net liability of GBP376,997 - i.e. no real banking activity of any kind. Redwood Bank's own "
    "FY2017 Strategic Report confirms it 'opened for business in August 2017, just four months after securing its "
    "initial banking licence' (obtained April 2017); its first customer loan was drawn down and its first customer "
    "deposit was taken during 2017, both evidenced in its FY2017 Annual Report and Accounts (its first year filed "
    "under the Redwood Bank name, audited by KPMG, covering the year ended 31 December 2017). FY2017 is therefore "
    "the real, independently verified disclosure floor - not the GLEIF/HD-001 entity-creation year of 2015. Years "
    "FY2015 and FY2016 are excluded from this workbook as pre-licence, pre-launch periods with no banking "
    "activity to report."
)

CASH_FLOW_SOURCES = (
    "Sources - Redwood Bank Limited Company-only statement of cash flows, £:\n"
    f"FY2025: Redwood Bank Annual Report and Accounts 2025, p.50 - {AR2025_URL}\n"
    f"FY2024: Redwood Bank Annual Report and Accounts 2024, p.47 - {AR2024_URL}\n"
    f"FY2023: Redwood Bank Annual Report and Accounts 2023, p.59 - {AR2023_URL}\n"
    f"FY2022: Redwood Bank Limited full accounts made up to 31 December 2022 filed at Companies House, p.33 "
    f"(comparative column) - {CH2022_URL}\n"
    f"FY2021: Redwood Bank Limited full accounts made up to 31 December 2022 filed at Companies House, p.33 "
    f"(comparative column for 2021), with the 2021 account used as a cross-check, p.28 - {CH2022_URL}\n"
    f"FY2020: Redwood Bank Limited full accounts made up to 31 December 2020 filed at Companies House, p.26 - "
    f"{CH2021_FILING_URL}\n"
    f"FY2019: Redwood Bank Limited full accounts made up to 31 December 2019 filed at Companies House, p.24 - "
    f"{CH2020_FILING_URL}\n"
    f"FY2018: Redwood Bank Limited full accounts made up to 31 December 2018 filed at Companies House, p.21 - "
    f"{CH2019_FILING_URL}\n"
    f"FY2017: Redwood Bank Limited Annual Report and Financial Statements for the year ended 31 December 2017 "
    f"(first year filed under the Redwood Bank name, audited by KPMG LLP), filed at Companies House, p.15 - "
    f"{CH2018_FILING_URL}\n\n"
    "The FY2022 and FY2021 columns use later-year comparative columns where available, following the project rule "
    "to inspect comparatives before seeking separate documents. The FY2021 comparative presents a small internal "
    "reclassification of TFSME interest and financing cash: its operating subtotal is £15,466,786 and financing "
    "subtotal £28,300,000, while the standalone 2021 report prints £15,456,792 and £28,309,994. Both produce the "
    "same reported net cash increase of £23,972,927 and the same closing cash of £105,308,945; the later comparative "
    "is used consistently here. FY2020-FY2017 are each taken from that year's own originally-filed statement "
    "(cross-checked against the following year's comparative column where available); FY2020's closing cash of "
    "£81,336,018 ties exactly to FY2021's opening cash, confirming continuity across the FY2020/FY2021 boundary. "
    "The FY2017 statement uses the labels 'Interest income'/'Interest expense' rather than later years' 'Interest "
    "receivable'/'Interest payable' - a presentational difference only.\n\n" + FLOOR_NOTE + "\n\n" + ENTITY_NOTE
)

P3_2023_URL = "https://redwoodbank.co.uk/media/c0hpdvqn/redwood-pillar-3-2023.pdf"
P3_2022_URL = "https://redwoodbank.co.uk/media/f5la0lih/redwood-pillar-3-2022.pdf"
# The /getmedia/<guid>/ path for the FY2021 edition now returns HTTP 404 - the
# CMS migration that produced the /media/<shortid>/ convention has since retired
# the old paths. The live /media/ URL below replaces it (re-verified 2026-09-15).
P3_2021_URL = "https://redwoodbank.co.uk/media/u5sb3ky5/redwood-pillar-3-2021-1.pdf"
P3_2021_OLD_URL = "https://redwoodbank.co.uk/getmedia/e38875ba-5520-4dc9-bcbe-cffbe05bd276/2021-Pillar-3_Redwood-Bank.pdf"
P3_2020_URL = "https://redwoodbank.co.uk/media/tu2f2l2x/redwood-bank-pillar-3-2020.pdf"
P3_2019_URL = "https://redwoodbank.co.uk/media/sybdkdyg/redwood-bank-2019-pillar-3-disclosures.pdf"
P3_2018_URL = "https://redwoodbank.co.uk/media/ezed3mwh/redwood-pillar-3-2018-1.pdf"
P3_2017_URL = "https://redwoodbank.co.uk/media/55un2r5s/pillar-3-disclosures-2017.pdf"

PILLAR3_DISCOVERY_NOTE = (
    "MAJOR CORRECTION 2026-09-15 (maximum-effort re-search; prior 'not publicly disclosed' verdict DISPROVED). "
    "Redwood Bank DOES publish standalone Pillar 3 disclosure documents, with full UK KM1 key-metrics tables, and "
    "this workbook previously recorded Tier 1 Ratio, Total RWAs, Leverage Ratio and NSFR as 'Not publicly "
    "disclosed' for every year. That was wrong. An unfiltered Wayback CDX sweep of redwoodbank.co.uk (2,802 "
    "archived URLs) surfaced an unbroken Pillar 3 series for FY2017 through FY2023, under two different CMS path "
    "conventions (/getmedia/<guid>/ for the older editions, /media/<shortid>/ for the current ones) - which is why "
    "filename-permutation searches against either convention alone had missed them:\n"
    f"  FY2023: {P3_2023_URL}\n"
    f"  FY2022: {P3_2022_URL}\n"
    f"  FY2021: {P3_2021_URL}\n"
    f"  FY2020: {P3_2020_URL}\n"
    f"  FY2019: {P3_2019_URL}\n"
    f"  FY2018: {P3_2018_URL}\n"
    f"  FY2017: {P3_2017_URL}\n"
    "All seven were downloaded live and have real text layers (no OCR needed).\n"
    "SECOND PASS 2026-09-15 (same day): the first pass read only the FY2020-FY2023 editions and left the "
    "FY2017-FY2019 cells blank, and recorded the FY2021 edition under its /getmedia/ URL. Both have now been "
    f"corrected. The old FY2021 path ({P3_2021_OLD_URL}) returns HTTP 404 - the CMS migration retired it - while "
    "the /media/ path above returns HTTP 200; a workbook citing only the dead URL would have looked like a "
    "sourcing failure on re-check. The FY2017, FY2018 and FY2019 editions were then read in full, which filled "
    "the RWA Breakdown for five further years and surfaced the KM1 row 4 defect described below.\n"
    "INDEPENDENT LINK SWEEP 2026-09-15 (third pass, different session): every URL in this script was re-fetched "
    "and checked for %PDF magic bytes rather than just an HTTP 200. All sixteen are healthy - the seven Pillar 3 "
    "PDFs above, the four redwoodbank.co.uk Annual Report PDFs, and the five Companies House filing-history "
    "documents for company 09872265. The /getmedia/ FY2021 path is confirmed still HTTP 404. IMPORTANTLY, it is "
    "now the ONLY /getmedia/ URL anywhere in this script: every other redwoodbank.co.uk citation already uses the "
    "current /media/<shortid>/ convention, so there is no remaining exposure to the CMS migration that killed it "
    "and nothing further to pre-emptively re-point. The FY2021 edition's own figures were also re-read from the "
    "/media/ replacement to confirm it is the same edition, not a revision: KM1 Table 1 p.4 (CET1 39,399,478; "
    "Tier 1 39,399,478; total regulatory capital 49,909,754; RWA 233,133,033; CET1/Tier 1 ratio 16.9%; total "
    "capital ratio 21.4%; leverage exposure 535,602,756; leverage ratio 7.4%; HQLA 111,539,577; net cash outflows "
    "11,495,946; LCR 970.3%), Table 7 p.21 (institutions 626,025; residential 68,247,424; commercial real estate "
    "137,862,947; past due 5,461,469; other items 798,294; total credit risk 212,996,159; operational risk "
    "20,136,875; Total Pillar 1 RWA 233,133,034) and section 8 p.28 (NSFR 148.9%, 2020: 150.5%). Every one "
    "reproduces this workbook exactly, including the documented £1 KM1-vs-Table-7 disagreement.\n"
    "VALIDATION GATE PASSED: the FY2023 edition's KM1 gives a CET1 ratio of 16.0% (2022: 15.4%) and the FY2021 "
    "edition gives 16.9%, all three reproducing EXACTLY the values this workbook already carried from the Annual "
    "Reports. The FY2022 edition's own FY2021 comparative column independently reproduces the FY2021 edition's "
    "CET1 39,399,478 / Total capital 49,909,754 / RWA 233,133,033 / CET1 ratio 16.9% / total capital ratio 21.4% "
    "to the pound and the decimal place.\n"
    "WHY THE SERIES STOPS AT FY2023 - it is not an access gap. The Bank of England consolidated waivers list "
    "(downloaded 2026-09-15) carries a Rule 3.1 SDDT row for FRN 755924, 'REDWOOD BANK LIMITED': 'Modification by "
    "Consent - PRA Rulebook - CRR Firms - Rule 3.1 of the SDDT Regime - General Application Part', START DATE "
    "26/07/2024, no end date. Rule 3.1 REMOVES the Pillar 3 disclosure obligation outright. Redwood's accounting "
    "reference date is 31 December, so FY2024 (year-end 31 Dec 2024) and FY2025 both fall AFTER the opt-in and are "
    "structurally exempt, while FY2023 (31 Dec 2023) predates it - which is exactly why an FY2023 Pillar 3 exists "
    "and no FY2024 or FY2025 edition does. A further Wayback sweep of all post-2025 captures confirms no Pillar 3 "
    "document later than the FY2023 edition has ever appeared on the domain.\n"
)

P3_SOURCES = (
    "Sources - Redwood Bank Limited regulatory capital and liquidity KPIs:\n"
    f"FY2025/FY2024: Redwood Bank Annual Report and Accounts 2025, pp.17 and 26, own-funds table p.26 - {AR2025_URL}\n"
    f"FY2024/FY2023: Redwood Bank Annual Report and Accounts 2024, pp.16 and 68 - {AR2024_URL}\n"
    f"FY2023/FY2022: Redwood Bank Annual Report and Accounts 2023, pp.22 and 81, own-funds table pp.81-82 - {AR2023_URL}\n"
    f"FY2021: Redwood Bank Limited full accounts made up to 31 December 2022 filed at Companies House, pp.6 and 60 "
    f"(comparative column), cross-checked against the 2021 accounts pp.6 and 53 - {CH2022_URL}\n"
    f"FY2020/FY2019: Redwood Bank Limited full accounts made up to 31 December 2020 filed at Companies House, "
    f"Strategic Report p.5 (LCR, CET1 capital) and Note 11 capital risk management pp.51-52 (regulatory capital "
    f"table) - {CH2021_FILING_URL}\n"
    f"FY2019/FY2018: Redwood Bank Limited full accounts made up to 31 December 2019 filed at Companies House, "
    f"Note 14 liquidity risk p.42 and Note 14 capital risk management pp.46-47 - {CH2020_FILING_URL}\n"
    f"FY2018/FY2017: Redwood Bank Limited full accounts made up to 31 December 2018 filed at Companies House, "
    f"Note 13 liquidity risk p.39 and Note 13 capital risk management pp.43-44 - {CH2019_FILING_URL}\n"
    f"FY2017: Redwood Bank Limited Annual Report and Financial Statements for the year ended 31 December 2017, "
    f"filed at Companies House, liquidity risk note p.33 and capital risk management note p.37 - "
    f"{CH2018_FILING_URL}\n\n"
    "Redwood's public reports do not provide separate entity-level numeric disclosures for Total RWAs, leverage "
    "ratio, NSFR, or MREL. Those fields remain explicitly undisclosed rather than being derived from other ratios.\n\n"
    "CET1 RATIO NOTE (FY2017-FY2019): each of these three years' capital risk management notes states in its own "
    "narrative that 'the Bank's capital resources are comprised of 100% CET1 regulatory capital', even though the "
    "accompanying regulatory-capital breakdown table in each of those years shows a small non-zero Tier 2 capital "
    "figure (paid-up capital instruments plus part of the collective loan-loss provision). Following the Bank's own "
    "explicit narrative statement, the CET1 Ratio for FY2017-FY2019 is transcribed as equal to the disclosed Total "
    "Capital Ratio for each of those years, rather than derived arithmetically from the Tier 1/Total Capital split "
    "in the breakdown table. From FY2020 the Bank's capital resources are explicitly described as 'a minimum of 75% "
    "CET1 and a maximum of 25% Tier 2' with no separate CET1 ratio stated anywhere in the report, so FY2020's CET1 "
    "Ratio is left as not publicly disclosed rather than derived.\n\n" + FLOOR_NOTE
)

STATEMENTS_SOURCES = (
    "Sources - Redwood Bank Limited Company-only Balance Sheet / Profit & Loss / Statement of Changes in Equity, £:\n"
    f"FY2025/FY2024: Redwood Bank Annual Report and Accounts 2025, pp.47-49 - {AR2025_URL}\n"
    f"FY2024/FY2023: Redwood Bank Annual Report and Accounts 2024, pp.44-45 - {AR2024_URL}\n"
    f"FY2023/FY2022: Redwood Bank Annual Report and Accounts 2023, pp.56-58 - {AR2023_URL}\n"
    f"FY2021: Redwood Bank Limited full accounts made up to 31 December 2022 filed at Companies House, pp.29-31 "
    f"(2021 comparative column) - {CH2022_URL}\n"
    f"FY2020: Redwood Bank Limited full accounts made up to 31 December 2020 filed at Companies House, pp.23-25 - "
    f"{CH2021_FILING_URL}\n"
    f"FY2019: Redwood Bank Limited full accounts made up to 31 December 2019 filed at Companies House, pp.21-23 - "
    f"{CH2020_FILING_URL}\n"
    f"FY2018: Redwood Bank Limited full accounts made up to 31 December 2018 filed at Companies House, pp.18-20 - "
    f"{CH2019_FILING_URL}\n"
    f"FY2017: Redwood Bank Limited Annual Report and Financial Statements for the year ended 31 December 2017 "
    f"(the Bank's first annual report, audited by KPMG LLP), filed at Companies House, pp.12-14 - "
    f"{CH2018_FILING_URL}\n\n"
    "FY2017 PRESENTATION NOTE: the FY2017 statement of comprehensive income shows 'Depreciation' as a separate "
    "line from 'Administrative expenses' (£30,961 interest expense, £3,320,707 administrative expenses, £59,568 "
    "depreciation); this workbook folds the depreciation line into Administrative expenses (giving £3,380,275) to "
    "match the single-line presentation used in FY2018 onward, consistent with Note 10's own statement that the "
    "£3,341,382 operating loss is stated after charging total expenses of £3,380,276 (FY2017 report's own rounding). "
    "No customer loans, deposits, or provisions existed before 2017 (see FLOOR NOTE below): the Bank's own FY2017 "
    "statement of changes in equity begins at 'At 18 November 2015' with a nil-activity pre-launch shell, and its "
    "FY2017 balance sheet's 2016 comparative column shows a total of £108 (a dormant, un-licensed entity)."
    "\n\n"
    "RESTATEMENT NOTE: the FY2025 report presents a RESTATED FY2024 comparative Balance Sheet (Total assets "
    "£635,583,084) that differs from AR2024's own originally-published FY2024 figure (Total assets £635,400,816, "
    "a difference of £182,268), splitting 'Cash and balances at central banks' into a separate 'Loans and advances "
    "to banks' line and adding a 'Derivative assets'/'Fair value adjustments on hedged assets' split not present "
    "in the original AR2024 presentation. Following the project convention of using each year's own "
    "originally-published figure rather than a later restatement, the FY2024 column below reproduces AR2024's own "
    "figures, not AR2025's restated comparative.\n\n"
    "PRESENTATION NOTE: FY2025 splits 'Other assets and prepayments' into two lines ('Other assets' and "
    "'Prepayments and accrued income') and 'Other liabilities and accruals' into two lines ('Other liabilities' "
    "and 'Accruals and deferred income'); FY2024-FY2021 disclose each as a single combined line - both are shown "
    "as separate rows, populated only for the years that split them. 'Loans and advances to banks' and 'Fair "
    "value adjustments on hedged assets'/'Derivative assets' are new lines from FY2025 (FY2024's own figures fold "
    "these into other lines); blank for FY2023-FY2021. The Available-for-sale reserve was fully utilised by "
    "FY2023 year-end and the FY2024/FY2025 statements of changes in equity no longer carry the column - blank "
    "(nil) from FY2024 onward. P&L: FY2024-FY2025 disclose 'Fair value gains/(losses) on financial instruments' "
    "and a 'Total income' subtotal as separate lines; FY2021-FY2023 do not - net interest income flows directly "
    "into administrative expenses in those years' own statements, so 'Total income' is blank for FY2021-FY2023.\n\n"
    + FLOOR_NOTE + "\n\n" + ENTITY_NOTE
)

ASSET_QUALITY_SOURCES = (
    "Sources - Redwood Bank Limited mortgage portfolio arrears/impairment and loan loss provisions, £:\n"
    f"FY2025/FY2024: Redwood Bank Annual Report and Accounts 2025, pp.63-64 and 73-74 - {AR2025_URL}\n"
    f"FY2024/FY2023: Redwood Bank Annual Report and Accounts 2024, pp.60-61 and 70 - {AR2024_URL}\n"
    f"FY2023/FY2022: Redwood Bank Annual Report and Accounts 2023, pp.75 and 84 - {AR2023_URL}\n"
    f"FY2021: Redwood Bank Limited full accounts made up to 31 December 2022 filed at Companies House, pp.50 and "
    f"63 (2021 comparative column) - {CH2022_URL}\n"
    f"FY2020/FY2019: Redwood Bank Limited full accounts made up to 31 December 2020 filed at Companies House, "
    f"Note 14 credit risk pp.42-45 and Note 15 loan loss provisions p.57 - {CH2021_FILING_URL}\n"
    f"FY2019/FY2018: Redwood Bank Limited full accounts made up to 31 December 2019 filed at Companies House, "
    f"Note 14 credit risk pp.39-41 and Note 16 loan loss provisions p.49 - {CH2020_FILING_URL}\n"
    f"FY2018/FY2017: Redwood Bank Limited full accounts made up to 31 December 2018 filed at Companies House, "
    f"Note 13 credit risk pp.35-37 and Note 15 loan loss provisions p.46 - {CH2019_FILING_URL}\n"
    f"FY2017: Redwood Bank Limited Annual Report and Financial Statements for the year ended 31 December 2017, "
    f"filed at Companies House, Note 16 loans and advances p.38 (there were no arrears, impairments, or loan loss "
    f"provisions in the Bank's first year - confirmed by FY2018's own comparative note stating 'There were no "
    f"arrears as at 31 December 2017') - {CH2018_FILING_URL}\n\n"
    "The Bank lends only against fixed UK property (max 75% LTV) to SME/commercial and residential property "
    "investors; there is no IFRS 9 stage 1/2/3 disclosure (FRS 102 basis, not IFRS) - the Bank's own 'impaired / "
    "past due but not impaired / forborne' categorisation is used instead. 'Total impaired' combines 'past due and "
    "impaired' and 'not past due and impaired' where both are disclosed (FY2023 only; other years show impaired "
    "loans as entirely past due). Forborne totals are 'not past due and forborne' plus 'past due and forborne' "
    "where both exist; FY2022 and FY2021 forbearance was £nil. Gross loans and advances to customers (before "
    "deferred fee income and loan loss provisions) and derived NPL/coverage ratios are calculated from the same "
    "notes, not separately disclosed by the Bank. FY2020's Forborne loans figure (£18,657,071) is the Bank's own "
    "disclosed total of loans in arrears granted COVID-19 payment holidays/tailored support, which is not "
    "necessarily disjoint from that year's impaired/not-impaired totals (the Bank did not disclose a non-overlapping "
    "breakdown). FY2017 had zero loans in arrears, zero impairment, and zero provisions (its first, partial year of "
    "lending), so its NPL and coverage ratios are shown as 0.00% and 'n/a' (0/0) respectively.\n\n"
    + FLOOR_NOTE + "\n\n" + ENTITY_NOTE
)

bw = BankWorkbook("Redwood Bank Limited", YEARS, YEAR_LABEL, header_color="8B3A3A")

bs_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and balances at central banks", {"FY2025": 85516188, "FY2024": 115416225, "FY2023": 109250259, "FY2022": 84018745, "FY2021": 105308945, "FY2020": 81336018, "FY2019": 36558154, "FY2018": 17832333, "FY2017": 4191328}),
    ("DATA", "Treasury bills and gilts", {"FY2025": 20013691, "FY2024": 25011813, "FY2023": 73494617, "FY2022": 49958358, "FY2021": 49938351, "FY2020": 30253815, "FY2019": 50121948, "FY2018": 40149039, "FY2017": 15027745}),
    ("DATA", "Loans and advances to banks", {"FY2025": 8841755}),
    ("DATA", "Loans and advances to customers", {"FY2025": 490444848, "FY2024": 492244170, "FY2023": 413983306, "FY2022": 403371972, "FY2021": 369798691, "FY2020": 323879674, "FY2019": 170218565, "FY2018": 79422117, "FY2017": 8413052}),
    ("DATA", "Fair value adjustments on hedged assets", {"FY2025": 1302543}),
    ("DATA", "Derivative assets", {"FY2025": 0}),
    ("DATA", "Other assets and prepayments", {"FY2024": 1231228, "FY2023": 1037196, "FY2022": 853781, "FY2021": 652247, "FY2020": 540042, "FY2019": 498138, "FY2018": 408207, "FY2017": 242244}),
    ("DATA", "Other assets", {"FY2025": 1483513}),
    ("DATA", "Prepayments and accrued income", {"FY2025": 1088724}),
    ("DATA", "Tangible fixed assets", {"FY2025": 104511, "FY2024": 151269, "FY2023": 174182, "FY2022": 166207, "FY2021": 182226, "FY2020": 258654, "FY2019": 323777, "FY2018": 305045, "FY2017": 359424}),
    ("DATA", "Intangible fixed assets", {"FY2025": 1132393, "FY2024": 1011135, "FY2023": 783820, "FY2022": 448996, "FY2021": 182069, "FY2020": 180203, "FY2019": 191854, "FY2018": 217654, "FY2017": 163105}),
    ("DATA", "Deferred tax assets", {"FY2025": 115182, "FY2024": 307517, "FY2023": 331990, "FY2022": 1442426, "FY2021": 1910683}),
    ("TOTAL", "Total assets", {"FY2025": 610043348, "FY2024": 635400816, "FY2023": 599055370, "FY2022": 540260485, "FY2021": 527973212, "FY2020": 436448406, "FY2019": 257912436, "FY2018": 138334395, "FY2017": 28396898}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Amounts due to banks", {"FY2024": 18726182, "FY2023": 38067988, "FY2022": 37862456, "FY2021": 37611747, "FY2020": 19201753}),
    ("DATA", "Customer deposits", {"FY2025": 546762522, "FY2024": 552995571, "FY2023": 499967473, "FY2022": 447173300, "FY2021": 438038613, "FY2020": 379609727, "FY2019": 230922849, "FY2018": 122443079, "FY2017": 18661835}),
    ("DATA", "Derivative liabilities", {"FY2025": 1224574}),
    ("DATA", "Other liabilities and accruals", {"FY2024": 4994868, "FY2023": 4245490, "FY2022": 2898770, "FY2021": 1826748, "FY2020": 1056219, "FY2019": 963042, "FY2018": 617041, "FY2017": 429808}),
    ("DATA", "Other liabilities", {"FY2025": 603027}),
    ("DATA", "Accruals and deferred income", {"FY2025": 2470155}),
    ("DATA", "Tax liabilities", {"FY2024": 303938, "FY2023": 222250}),
    ("DATA", "Subordinated debt", {"FY2025": 9000000, "FY2024": 9000000, "FY2023": 9000000, "FY2022": 9000000, "FY2021": 9000000, "FY2020": 9000000}),
    ("TOTAL", "Total liabilities", {"FY2025": 560060278, "FY2024": 586020559, "FY2023": 551503201, "FY2022": 496934526, "FY2021": 486477108, "FY2020": 408867699, "FY2019": 231885891, "FY2018": 123060120, "FY2017": 19091643}),
    ("SECTION", "Equity", {}),
    ("DATA", "Called up share capital", {"FY2025": 111, "FY2024": 111, "FY2023": 111, "FY2022": 111, "FY2021": 111, "FY2020": 111, "FY2019": 111, "FY2018": 111, "FY2017": 111}),
    ("DATA", "Share premium reserve", {"FY2025": 47922405, "FY2024": 47922405, "FY2023": 47922405, "FY2022": 47922405, "FY2021": 47922405, "FY2020": 38022405, "FY2019": 34822405, "FY2018": 22822405, "FY2017": 13018539}),
    ("DATA", "Available-for-sale reserve", {"FY2023": 0, "FY2022": -21961, "FY2021": -54202, "FY2020": 14876, "FY2019": -42763, "FY2018": -23776, "FY2017": 5092}),
    ("DATA", "Retained earnings", {"FY2025": 2060554, "FY2024": 1457741, "FY2023": -370347, "FY2022": -4574596, "FY2021": -6372210, "FY2020": -10456685, "FY2019": -8753208, "FY2018": -7524465, "FY2017": -3718487}),
    ("TOTAL", "Total equity", {"FY2025": 49983070, "FY2024": 49380257, "FY2023": 47552169, "FY2022": 43325959, "FY2021": 41496104, "FY2020": 27580707, "FY2019": 26026545, "FY2018": 15274275, "FY2017": 9305255}),
    ("TOTAL", "Total equity and liabilities", {"FY2025": 610043348, "FY2024": 635400816, "FY2023": 599055370, "FY2022": 540260485, "FY2021": 527973212, "FY2020": 436448406, "FY2019": 257912436, "FY2018": 138334395, "FY2017": 28396898}),
]

bw.add_balance_sheet_sheet(
    title="Redwood Bank Limited — Balance Sheet",
    subtitle="Company-only basis, £. FY2021 uses the comparative column in the FY2022 Companies House filing; FY2020-FY2017 are each from that year's own filed accounts; see source note.",
    rows=bs_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=68,
    source_height=320,
    unit_suffix=" (£)",
)

pl_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest receivable", {"FY2025": 45241843, "FY2024": 49521006, "FY2023": 46123616, "FY2022": 28087329, "FY2021": 19924820, "FY2020": 15124939, "FY2019": 8812730, "FY2018": 2669838, "FY2017": 69854}),
    ("DATA", "Interest payable", {"FY2025": -22521076, "FY2024": -23269459, "FY2023": -17294646, "FY2022": -7219223, "FY2021": -4789284, "FY2020": -4728423, "FY2019": -2438965, "FY2018": -777169, "FY2017": -30961}),
    ("TOTAL", "Net interest income", {"FY2025": 22720767, "FY2024": 26251547, "FY2023": 28828970, "FY2022": 20868106, "FY2021": 15135536, "FY2020": 10396516, "FY2019": 6373765, "FY2018": 1892669, "FY2017": 38893}),
    ("DATA", "Fair value gains/(losses) on financial instruments", {"FY2025": 80899, "FY2024": -8932}),
    ("TOTAL", "Total income", {"FY2025": 22801666, "FY2024": 26242615}),
    ("TOTAL", "Administrative expenses", {"FY2025": -21265984, "FY2024": -21675255, "FY2023": -20509671, "FY2022": -16105258, "FY2021": -12922871, "FY2020": -9382145, "FY2019": -7297813, "FY2018": -5457647, "FY2017": -3380275}),
    ("TOTAL", "Operating profit before impairment charge", {"FY2025": 1535682, "FY2024": 4567360, "FY2023": 8319299, "FY2022": 4762848, "FY2021": 2212665, "FY2020": 1014371, "FY2019": -924048, "FY2018": -3564978, "FY2017": -3341382}),
    ("DATA", "Impairment charge on loans and advances to customers", {"FY2025": -756168, "FY2024": -1869546, "FY2023": -2782364, "FY2022": -2496977, "FY2021": -38873, "FY2020": -2717848, "FY2019": -304694, "FY2018": -241000, "FY2017": 0}),
    ("TOTAL", "Profit before tax", {"FY2025": 779514, "FY2024": 2697814, "FY2023": 5536935, "FY2022": 2265871, "FY2021": 2173792, "FY2020": -1703477, "FY2019": -1228742, "FY2018": -3805978, "FY2017": -3341382}),
    ("DATA", "Tax (charge)/credit", {"FY2025": -176701, "FY2024": -869726, "FY2023": -1332686, "FY2022": -468257, "FY2021": 1910683, "FY2020": 0, "FY2019": 0, "FY2018": 0, "FY2017": 0}),
    ("TOTAL", "Profit for the year", {"FY2025": 602813, "FY2024": 1828088, "FY2023": 4204249, "FY2022": 1797614, "FY2021": 4084475, "FY2020": -1703477, "FY2019": -1228742, "FY2018": -3805978, "FY2017": -3341382}),
    ("SECTION", "Other comprehensive income", {}),
    ("DATA", "Movement in available-for-sale investments", {"FY2023": 21961, "FY2022": 32241, "FY2021": -69078, "FY2020": 57639, "FY2019": -18987, "FY2018": -23776, "FY2017": 5092}),
    ("TOTAL", "Total comprehensive income", {"FY2025": 602813, "FY2024": 1828088, "FY2023": 4226210, "FY2022": 1829855, "FY2021": 4015397, "FY2020": -1645838, "FY2019": -1247729, "FY2018": -3829754, "FY2017": -3336290}),
]

bw.add_income_statement_sheet(
    title="Redwood Bank Limited — Profit & Loss",
    subtitle="Company-only basis, £. FY2021 uses the comparative column in the FY2022 Companies House filing; FY2020-FY2017 are each from that year's own filed accounts; see source note.",
    rows=pl_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=68,
    source_height=320,
    unit_suffix=" (£)",
)

equity_headers = ["Share capital", "Share premium", "Available-for-sale reserve", "Retained earnings", "Total equity"]
equity_rows = [
    ("TOTAL", "At 1 January 2017", (108, 0, 0, -377105, -376997)),
    ("DATA", "Loss for the year", (None, None, None, -3341382, -3341382)),
    ("DATA", "Other comprehensive income for the year", (None, None, 5092, None, 5092)),
    ("TOTAL", "Total comprehensive income for the year", (None, None, 5092, -3341382, -3336290)),
    ("DATA", "Issue of share capital", (3, 13018539, None, None, 13018542)),
    ("TOTAL", "Total transactions with owners", (3, 13018539, None, None, 13018542)),
    ("TOTAL", "At 31 December 2017", (111, 13018539, 5092, -3718487, 9305255)),
    ("TOTAL", "At 1 January 2018", (111, 13018539, 5092, -3718487, 9305255)),
    ("DATA", "Loss for the year", (None, None, None, -3805978, -3805978)),
    ("DATA", "Other comprehensive loss for the year", (None, None, -28868, None, -28868)),
    ("TOTAL", "Total comprehensive income for the year", (None, None, -28868, -3805978, -3834846)),
    ("DATA", "Issue of share capital", (None, 9803866, None, None, 9803866)),
    ("TOTAL", "Total transactions with owners", (None, 9803866, None, None, 9803866)),
    ("TOTAL", "At 31 December 2018", (111, 22822405, -23776, -7524465, 15274275)),
    ("TOTAL", "At 1 January 2019", (111, 22822405, -23776, -7524465, 15274275)),
    ("DATA", "Loss for the year", (None, None, None, -1228742, -1228742)),
    ("DATA", "Other comprehensive loss for the year", (None, None, -18987, None, -18987)),
    ("TOTAL", "Total comprehensive income for the year", (None, None, -18987, -1228742, -1247729)),
    ("DATA", "Issue of share capital", (None, 12000000, None, None, 12000000)),
    ("TOTAL", "Total transactions with owners", (None, 12000000, None, None, 12000000)),
    ("TOTAL", "At 31 December 2019", (111, 34822405, -42763, -8753208, 26026545)),
    ("TOTAL", "At 1 January 2020", (111, 34822405, -42763, -8753208, 26026545)),
    ("DATA", "Loss for the year", (None, None, None, -1703477, -1703477)),
    ("DATA", "Other comprehensive income for the year", (None, None, 57639, None, 57639)),
    ("TOTAL", "Total comprehensive income for the year", (None, None, 57639, -1703477, -1645838)),
    ("DATA", "Issue of share capital", (None, 3200000, None, None, 3200000)),
    ("TOTAL", "Total transactions with owners", (None, 3200000, None, None, 3200000)),
    ("TOTAL", "At 31 December 2020", (111, 38022405, 14876, -10456685, 27580707)),
    ("TOTAL", "At 1 January 2021", (111, 38022405, 14876, -10456685, 27580707)),
    ("DATA", "Profit for the year", (None, None, None, 4084475, 4084475)),
    ("DATA", "Other comprehensive loss for the year", (None, None, -69078, None, -69078)),
    ("TOTAL", "Total comprehensive income for the year", (None, None, -69078, 4084475, 4015397)),
    ("DATA", "Issue of share capital", (None, 9900000, None, None, 9900000)),
    ("TOTAL", "Total transactions with owners, recognised directly in equity", (None, 9900000, None, None, 9900000)),
    ("TOTAL", "At 31 December 2021", (111, 47922405, -54202, -6372210, 41496104)),
    ("TOTAL", "At 1 January 2022", (111, 47922405, -54202, -6372210, 41496104)),
    ("DATA", "Profit for the year", (None, None, None, 1797614, 1797614)),
    ("DATA", "Other comprehensive income for the year", (None, None, 32241, None, 32241)),
    ("TOTAL", "Total comprehensive income for the year", (None, None, 32241, 1797614, 1829855)),
    ("TOTAL", "At 31 December 2022", (111, 47922405, -21961, -4574596, 43325959)),
    ("TOTAL", "At 1 January 2023", (111, 47922405, -21961, -4574596, 43325959)),
    ("DATA", "Profit for the year", (None, None, None, 4204249, 4204249)),
    ("DATA", "Other comprehensive income for the year", (None, None, 21961, None, 21961)),
    ("TOTAL", "Total comprehensive income for the year", (None, None, 21961, 4204249, 4226210)),
    ("TOTAL", "At 31 December 2023", (111, 47922405, None, -370347, 47552169)),
    ("TOTAL", "At 1 January 2024", (111, 47922405, None, -370347, 47552169)),
    ("DATA", "Profit for the year", (None, None, None, 1828088, 1828088)),
    ("TOTAL", "Total comprehensive income for the year", (None, None, None, 1828088, 1828088)),
    ("TOTAL", "At 31 December 2024", (111, 47922405, None, 1457741, 49380257)),
    ("TOTAL", "At 1 January 2025", (111, 47922405, None, 1457741, 49380257)),
    ("DATA", "Profit for the year", (None, None, None, 602813, 602813)),
    ("TOTAL", "Total comprehensive income for the year", (None, None, None, 602813, 602813)),
    ("TOTAL", "At 31 December 2025", (111, 47922405, None, 2060554, 49983070)),
]

bw.add_equity_changes_sheet(
    title="Redwood Bank Limited — Statement of Changes in Equity",
    subtitle="Company-only basis, £, chronological, from FY2017 (the Bank's first year of banking operations; see FLOOR NOTE) to FY2025. "
              "Zero undocumented plug rows across all 9 years - every movement is profit/loss for the year, an available-for-sale reserve "
              "fair value movement, or a share issue.",
    headers=equity_headers,
    rows=equity_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=52,
    source_height=320,
)

rows = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Profit for the year", {"FY2025": 602813, "FY2024": 1828088, "FY2023": 4204249, "FY2022": 1797614, "FY2021": 4084475, "FY2020": -1703477, "FY2019": -1228742, "FY2018": -3805978, "FY2017": -3341382}),
    ("DATA", "Amortisation of intangibles", {"FY2025": 359914, "FY2024": 336289, "FY2023": 216413, "FY2022": 133808, "FY2021": 85194, "FY2020": 68623, "FY2019": 52259, "FY2018": 46776, "FY2017": 11650}),
    ("DATA", "Depreciation of tangible assets", {"FY2025": 91501, "FY2024": 92566, "FY2023": 96581, "FY2022": 104682, "FY2021": 98689, "FY2020": 107637, "FY2019": 99994, "FY2018": 87874, "FY2017": 47918}),
    ("DATA", "Write off of fixed/intangible assets", {"FY2021": 0, "FY2020": 838}),
    ("DATA", "Impairment losses on intangible assets", {"FY2019": 32440}),
    ("DATA", "Impairment charge on loans and advances to customers", {"FY2025": 756168, "FY2024": 1869546, "FY2023": 2782364, "FY2022": 2496977, "FY2021": 38873, "FY2020": 2717848, "FY2019": 304694}),
    ("DATA", "Net increase in loans to banks", {"FY2025": -1870000}),
    ("DATA", "Net decrease/(increase) in loans to customers", {"FY2025": 1043154, "FY2024": -80130410}),
    ("DATA", "Net increase in customer deposits", {"FY2024": 53028098, "FY2023": 52794173, "FY2022": 9134687, "FY2021": 58428886, "FY2020": 148686878, "FY2019": 108479770, "FY2018": 103781244, "FY2017": 18661835}),
    ("DATA", "(Decrease)/increase in customer deposits", {"FY2025": -6233049}),
    ("DATA", "Increase in other liabilities", {"FY2024": 749378, "FY2023": 1346720, "FY2022": 1072022, "FY2021": 770530, "FY2020": 94931, "FY2019": 346001, "FY2018": 187233, "FY2017": 52704}),
    ("DATA", "(Decrease)/increase in other liabilities", {"FY2025": -1322763}),
    ("DATA", "Increase in other assets", {"FY2024": -194032, "FY2023": -183415, "FY2022": -201534, "FY2021": -112205, "FY2020": -41905, "FY2019": -89931, "FY2018": -165963, "FY2017": -240401}),
    ("DATA", "Increase in other assets", {"FY2025": -1390656}),
    ("DATA", "Net increase in loans to customers", {"FY2023": -13393698, "FY2022": -36070258, "FY2021": -45957889, "FY2020": -156378957, "FY2019": -91101142, "FY2018": -71009065, "FY2017": -8413052}),
    ("DATA", "Increase in accruals and deferred income", {"FY2025": -781191}),
    ("DATA", "Decrease/(increase) in payments and accrued income", {"FY2025": 49647}),
    ("DATA", "Increase in interest payable on TFSME", {"FY2023": 205532, "FY2022": 250709, "FY2021": 9994}),
    ("DATA", "(Decrease)/increase in interest payable on TFSME", {"FY2025": -226182, "FY2024": -241806}),
    ("DATA", "Redemption of TFSME", {"FY2025": -18500000, "FY2024": -19100000}),
    ("DATA", "Net increase in derivatives and hedged items", {"FY2025": -50510, "FY2024": -27459}),
    ("DATA", "Finance cost for subordinated debt", {"FY2025": 585000, "FY2024": 586603, "FY2023": 585000, "FY2022": 585000, "FY2021": 583397}),
    ("DATA", "Fair value change of treasury bills and gilts", {"FY2024": 0, "FY2023": 21961, "FY2022": 32241, "FY2021": -69078, "FY2017": 6287}),
    ("DATA", "Income tax", {"FY2025": -111603, "FY2024": 106161, "FY2023": 1332686, "FY2022": 468257, "FY2021": -1910683}),
    ("DATA", "Interest paid for subordinated debt", {"FY2025": -585000, "FY2024": -586603, "FY2023": -585000, "FY2022": -585000, "FY2021": -583397}),
    ("TOTAL", "Net cash from/(used in) operating activities", {"FY2025": -27582757, "FY2024": -41683581, "FY2023": 49423566, "FY2022": -20780795, "FY2021": 15466786, "FY2020": -6447584, "FY2019": 16895343, "FY2018": 29122121, "FY2017": 6785559}),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Purchases of tangible fixed assets", {"FY2025": -44743, "FY2024": -69653, "FY2023": -104556, "FY2022": -88663, "FY2021": -22261, "FY2020": -43352, "FY2019": -118727, "FY2018": -33495, "FY2017": -407342}),
    ("DATA", "Purchases of intangible assets", {"FY2025": -481172, "FY2024": -563604, "FY2023": -551237, "FY2022": -400735, "FY2021": -87059, "FY2020": -56972, "FY2019": -58899, "FY2018": -101325, "FY2017": -174755}),
    ("DATA", "Acquisition of treasury bills and gilts", {"FY2024": -5053587, "FY2023": -44402384, "FY2022": -9165232, "FY2021": -19884208, "FY2020": -45233273, "FY2019": -54517186, "FY2018": -77038998, "FY2017": -15027745}),
    ("DATA", "Acquisition of gilts", {"FY2025": 0}),
    ("DATA", "Proceeds on sale/maturity of treasury bills and gilts", {"FY2025": 4998122, "FY2024": 53536391, "FY2023": 20866125, "FY2022": 9145225, "FY2021": 199669, "FY2020": 65159045, "FY2019": 44525290, "FY2018": 51888836}),
    ("TOTAL", "Net cash generated/(used in) investing activities", {"FY2025": 4472207, "FY2024": 47849547, "FY2023": -24192052, "FY2022": -509405, "FY2021": -19793859, "FY2020": 19825448, "FY2019": -10169522, "FY2018": -25284982, "FY2017": -15609842}),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Proceeds of issue of ordinary shares", {"FY2021": 9900000, "FY2020": 3200000, "FY2019": 12000000, "FY2018": 9803866, "FY2017": 13018542}),
    ("DATA", "Proceeds of issue of subordinated debt", {"FY2020": 9000000}),
    ("DATA", "Proceeds of TFSME", {"FY2021": 18400000, "FY2020": 19200000}),
    ("TOTAL", "Net cash from financing activities", {"FY2021": 28300000, "FY2020": 31400000, "FY2019": 12000000, "FY2018": 9803866, "FY2017": 13018542}),
    ("TOTAL", "Net cash (decrease)/increase in cash and cash equivalents", {"FY2025": -23110550, "FY2024": 6165966, "FY2023": 25231514, "FY2022": -21290200, "FY2021": 23972927, "FY2020": 44777864, "FY2019": 18725821, "FY2018": 13641005, "FY2017": 4194259}),
    ("DATA", "Cash and cash equivalents at the beginning of year", {"FY2025": 113293493, "FY2024": 109250259, "FY2023": 84018745, "FY2022": 105308945, "FY2021": 81336018, "FY2020": 36558154, "FY2019": 17832333, "FY2018": 4191328, "FY2017": -2931}),
    ("TOTAL", "Cash and cash equivalents at the end of year", {"FY2025": 90182943, "FY2024": 115416225, "FY2023": 109250259, "FY2022": 84018745, "FY2021": 105308945, "FY2020": 81336018, "FY2019": 36558154, "FY2018": 17832333, "FY2017": 4191328}),
]

bw.add_cash_flow_sheet("Redwood Bank Limited — Cash Flow Statement", "Company-only basis, £. FY2021 uses the later FY2022 comparative column; FY2020-FY2017 are each from that year's own filed accounts; see source note.", rows, CASH_FLOW_SOURCES, first_col_width=68, source_height=300, unit_suffix=" (£)")

asset_quality_rows = [
    ("SECTION", "Loan book quality (mortgage portfolio)", {}),
    ("DATA", "Gross loans and advances to customers (before deferred fees/provisions)", {"FY2025": 496453100, "FY2024": 498343502, "FY2023": 422021987, "FY2022": 410806685, "FY2021": 375065639, "FY2020": 329124138, "FY2019": 172178122, "FY2018": 80504046, "FY2017": 8518188}),
    ("DATA", "Total impaired loans", {"FY2025": 12772475, "FY2024": 18348860, "FY2023": 23868967, "FY2022": 11956906, "FY2021": 6913006, "FY2020": 5485856, "FY2019": 618209, "FY2018": 684648, "FY2017": 0}),
    ("DATA", "Past due but not impaired", {"FY2025": 20604947, "FY2024": 26789634, "FY2023": 21410656, "FY2022": 19429780, "FY2021": 11469228, "FY2020": 22078538, "FY2019": 5825418, "FY2018": 468524, "FY2017": 0}),
    ("DATA", "Forborne loans", {"FY2025": 5185947, "FY2024": 7471460, "FY2023": 9739221, "FY2020": 18657071}),
    ("SECTION", "Loan loss provisions", {}),
    ("DATA", "Collective loan provision (closing)", {"FY2025": 659129, "FY2024": 1066643, "FY2023": 1124076, "FY2022": 889925, "FY2021": 1510276, "FY2020": 2251174, "FY2019": 377000, "FY2018": 91000, "FY2017": 0}),
    ("DATA", "Individual loan provision (closing)", {"FY2025": 4259401, "FY2024": 3934301, "FY2023": 5522602, "FY2022": 4745925, "FY2021": 1628597, "FY2020": 848826, "FY2019": 5153, "FY2018": 150000, "FY2017": 0}),
    ("TOTAL", "Total loan loss provisions", {"FY2025": 4918530, "FY2024": 5000944, "FY2023": 6646678, "FY2022": 5635850, "FY2021": 3138873, "FY2020": 3100000, "FY2019": 382153, "FY2018": 241000, "FY2017": 0}),
    ("SECTION", "Derived ratios", {}),
    ("DATA", "NPL ratio (total impaired / gross loans)", {"FY2025": "2.57%", "FY2024": "3.68%", "FY2023": "5.66%", "FY2022": "2.91%", "FY2021": "1.84%", "FY2020": "1.67%", "FY2019": "0.36%", "FY2018": "0.85%", "FY2017": "0.00%"}),
    ("DATA", "Coverage ratio (total loan loss provisions / total impaired loans)", {"FY2025": "38.51%", "FY2024": "27.25%", "FY2023": "27.85%", "FY2022": "47.13%", "FY2021": "45.41%", "FY2020": "56.52%", "FY2019": "61.82%", "FY2018": "35.20%", "FY2017": "n/a (0/0)"}),
]

bw.add_asset_quality_sheet(
    title="Redwood Bank Limited — Asset Quality",
    subtitle="Company-only basis, £. FRS 102 basis (no IFRS 9 stage 1/2/3 split); see source note for category definitions. "
              "NPL and coverage ratios are derived, not separately disclosed by the Bank.",
    rows=asset_quality_rows,
    sources_text=ASSET_QUALITY_SOURCES,
    first_col_width=68,
    source_height=280,
    unit_suffix=" (£)",
)

P3_SOURCES = P3_SOURCES + "\n\n" + PILLAR3_DISCOVERY_NOTE


def metric(name, unit, rows_data, note=None):
    bw.add_metric_sheet(name, unit, rows_data, P3_SOURCES, note=note, first_col_width=46, source_height=190)


KM1_SOURCES = (
    "Sources - Redwood Bank Limited's own Pillar 3 disclosures, key-metrics table, Bank basis, amounts in single "
    "pounds as printed (this bank publishes its template in plain £, not £'000 or £m). Every column is that "
    "year's OWN edition, at the folio its own contents page gives:\n"
    f"FY2023: 'Table 1: Key metrics', printed p.5 - {P3_2023_URL}\n"
    f"FY2022: 'Table 1: Key metrics', printed p.6 - {P3_2022_URL}\n"
    f"FY2021: 'Table 1: Key metrics', printed pp.4-5 (the table breaks across the page) - {P3_2021_URL}\n"
    f"FY2020: 'Table 4: Overview of prudential metrics', printed pp.18-19 - {P3_2020_URL}\n"
    f"FY2019: 'Table 4: Overview of prudential metrics', printed pp.17-18 - {P3_2019_URL}\n"
    f"FY2018: 'Table 4 : Overview of prudential metrics', printed pp.17-18 - {P3_2018_URL}\n"
    f"FY2017: 'Table 4 - Overview of prudential metrics', printed pp.18-19 - {P3_2017_URL}\n\n"
    "TWO TEMPLATES, DELIBERATELY NOT MERGED. FY2022 and FY2023 are the UK KM1 template (SREP rows numbered "
    "'UK 7a'/'UK7d', an overall-capital-requirements row 'UK 11a', leverage on the excluding-central-bank-claims "
    "basis, and NSFR rows 18-20). FY2017-FY2021 are the earlier Basel III 'Overview of prudential metrics' "
    "template, which REUSES ROW NUMBERS FOR DIFFERENT METRICS: its plain '7a' is the fully loaded ECL total "
    "capital ratio, where the UK template's 'UK 7a' is the additional CET1 SREP requirement, and its rows 1a/2a/"
    "3a/5a/6a/14a are fully loaded ECL twins that the UK template does not carry at all. Its leverage rows are the "
    "Basel III total exposure measure, a different basis from rows 13/14 of the UK template. The two blocks are "
    "therefore kept separate and nothing is carried across them.\n\n"
    "FY2025 AND FY2024 ARE BLANK BECAUSE THE DUTY ENDED, and the instrument is dated. The Bank of England "
    "consolidated waivers register (re-downloaded and re-read 2026-09-17) carries, for FRN 755924 REDWOOD BANK "
    "LIMITED, a 'Modification by Consent - PRA Rulebook - CRR Firms - Rule 3.1 of the SDDT Regime - General "
    "Application Part' (rule description 'SDDT Regime - General Application', sub-rule 'Ru 3.1', waiver ref "
    "A00008317P.pdf), start date 26/07/2024, no end date. Rule 3.1 removes the Pillar 3 disclosure obligation "
    "itself. Redwood's year-end is 31 December, so the FY2024 (31 Dec 2024) and FY2025 (31 Dec 2025) year-ends "
    "both fall after that date while FY2023 (31 Dec 2023) precedes it - which is exactly the pattern the documents "
    "show, an unbroken series to FY2023 and nothing after. Opting in does not by itself stop a bank publishing, so "
    "the absence was also checked directly on 2026-09-17: the bank's own reports page (redwoodbank.co.uk/legal/"
    "reports/), which listed the FY2017-FY2022 Pillar 3 PDFs when it was archived in March 2024, now returns HTTP "
    "404, and the current site navigation carries no reports or disclosures page at all; its performance-summary "
    "page links the 2023, 2024 and 2025 Annual Reports and no Pillar 3 document. The FY2023 edition is the last "
    "one published.\n\n"
    "THE PRINTED ROW 4 IS WRONG IN THE THREE OLDEST EDITIONS, AND IS REPRODUCED ANYWAY. For FY2019, FY2018 and "
    "FY2017 the key-metrics row 4 carries the CREDIT-RISK subtotal rather than total Pillar 1 risk-weighted "
    "assets: 114,001,332 + operational risk 14,611,306 = 128,612,638 (FY2019); 52,495,810 + 13,398,025 = "
    "65,893,829 (FY2018); 8,268,832 + 7,025,000 = 15,293,832 (FY2017), each equal to that edition's own Pillar 1 "
    "capital-requirements table total. The bank's own printed ratios only reconcile against the Pillar 1 totals "
    "(25,830,817/128,612,638 = 20.08% against a printed 20.08%; 9,142,150/15,293,832 = 59.78% against a printed "
    "59.78%), which is what identifies the row-4 figures as the subtotal. This sheet prints row 4 as the bank "
    "printed it; the Total RWAs and RWA Breakdown sheets carry the Pillar 1 totals. From the FY2020 edition "
    "onward row 4 is correct.\n\n"
    "WHERE TWO EDITIONS PRINT THE SAME YEAR DIFFERENTLY, each column here is its own edition's printing:\n"
    "- FY2020 total regulatory capital is 38,647,805 and the total capital ratio 18.81% in the FY2020 edition "
    "(printed here). The FY2021 edition restates both, to 36,528,841 and 17.8%, footnoted 'Restated due to the "
    "correction of total regulatory capital and its ratio and leverage ratio'; the Total Capital and Total Capital "
    "Ratio metric sheets carry those restated figures. Both printings are internally consistent against the same "
    "RWA (38,647,805/205,441,523 = 18.81%; 36,528,841/205,441,523 = 17.78%), so this is a genuine restatement of "
    "the capital figure and not a rounding or unit artefact.\n"
    "- FY2019 row 16 total net cash outflows: 18,699,805 in the FY2019 edition (printed here) against 15,634,030 "
    "in the FY2020 edition's comparative; both editions print the LCR as 541.05%.\n"
    "- FY2018 rows 15 and 17: 56,305,459 HQLA and a 399.32% LCR in the FY2018 edition (printed here) against "
    "56,205,459 and 391.32% in the FY2019 edition's comparative.\n"
    "- FY2022 row 12: 9.38% in the FY2022 edition (printed here) against 6.47% in the FY2023 edition.\n"
    "- FY2020 row 5: 13.34% in the FY2020 edition (printed here); the FY2021 edition prints 13.3%.\n\n"
    "OTHER THINGS THE READER SHOULD KNOW ABOUT THE PRINTING:\n"
    "- An NSFR row appears in ONE edition only: the FY2019 edition prints '18 NSFR (%) 170.9%' (with a 193.4% "
    "comparative for 2018). The FY2017, FY2018, FY2020 and FY2021 editions print no NSFR row in the key-metrics "
    "table at all, so those cells are blank here even where a later edition or that edition's narrative gives a "
    "figure - the NSFR metric sheet carries those, sourced from the narrative sections.\n"
    "- FY2017's buffer rows 8-12 are printed as '0%' - printed zeros, kept as zeros, not dashes.\n"
    "- Label drift between editions is the bank's, not ours: row 3 reads 'Total regulatory capital' in the FY2020 "
    "and FY2021 editions and 'Total capital' in the FY2017-FY2019 ones; row 7 reads 'Total regulatory capital "
    "ratio (%)' in the FY2021-FY2023 editions and 'Total capital ratio (%)' in the earlier ones; row 12 reads "
    "'CET1 available after meeting the Bank's minimum capital requirements (%)' in the old template and 'CET1 "
    "available after meeting the total SREP own funds requirements (%)' in the UK one. Each block uses one "
    "printed wording, named here.\n"
    "- The CET1 Capital metric sheet carries 9,142,150 for FY2017 and 15,052,747 for FY2018, while row 1 of the "
    "bank's own key-metrics table prints 9,142,139 and 15,052,746 for those years - the FY2017 figure on that "
    "sheet is in fact the total capital figure the same table prints on row 3 (9,142,150, which includes £11 of "
    "Tier 2). Both printings are recorded; nothing has been altered here to make them agree.\n\n"
    + ENTITY_NOTE
)

bw.add_km1_sheet(
    title="Redwood Bank Limited — KM1 Key Metrics",
    subtitle="The bank's own published key-metrics template, Bank basis, amounts in single pounds as printed. "
             "FY2022-FY2023 are the UK KM1 template; FY2017-FY2021 are the earlier Basel III 'Overview of "
             "prudential metrics' template, kept as a separate block because it reuses the same row numbers for "
             "different metrics. Every column is that year's own edition. FY2024 and FY2025 are blank: Redwood "
             "became an SDDT on 26 July 2024 and publishes no Pillar 3 for those years - see the source note.",
    rows=[
        ("SECTION", "FY2022-FY2023 editions - UK KM1 template", {}),
        ("SECTION", "Available own funds (amounts)", {}),
        ("DATA", "1 Common Equity Tier 1 (CET1) capital (£, single pounds as printed)", {"FY2023": 46764475, "FY2022": 41430663}),
        ("DATA", "2 Tier 1 (£, single pounds as printed)", {"FY2023": 46764475, "FY2022": 41430663}),
        ("DATA", "3 Total capital (£, single pounds as printed)", {"FY2023": 56888551, "FY2022": 51320588}),
        ("SECTION", "Risk-weighted exposure amounts", {}),
        ("DATA", "4 Total risk-weighted assets (RWA) (£, single pounds as printed)", {"FY2023": 294050082, "FY2022": 269415717}),
        ("SECTION", "Capital ratios (as a percentage of risk-weighted exposure amount)", {}),
        ("DATA", "5 Common Equity Tier 1 ratio (%)", {"FY2023": "16.0%", "FY2022": "15.4%"}),
        ("DATA", "6 Tier 1 ratio (%)", {"FY2023": "16.0%", "FY2022": "15.4%"}),
        ("DATA", "7 Total regulatory capital ratio (%)", {"FY2023": "19.4%", "FY2022": "19.0%"}),
        ("SECTION", "Additional own funds requirements based on SREP (as a percentage of risk-weighted exposure amount)", {}),
        ("DATA", "UK 7a Additional CET1 SREP requirements (%)", {"FY2023": "3.59%", "FY2022": "3.88%"}),
        ("DATA", "UK7d Total SREP own funds requirements (%)", {"FY2023": "11.59%", "FY2022": "11.88%"}),
        ("SECTION", "Combined buffer requirement (as a percentage of risk-weighted exposure amount)", {}),
        ("DATA", "8 Capital conservation buffer requirement (%)", {"FY2023": "2.5%", "FY2022": "2.5%"}),
        ("DATA", "9 Countercyclical buffer requirement (%)", {"FY2023": "2.0%", "FY2022": "1.0%"}),
        ("DATA", "11 Total of Bank CET1 specific buffer requirements (%) (row 8 + row 9 + row 10)", {"FY2023": "4.5%", "FY2022": "3.5%"}),
        ("DATA", "UK 11a Overall capital requirements (%)", {"FY2023": "16.09%", "FY2022": "15.38%"}),
        ("DATA", "12 CET1 available after meeting the total SREP own funds requirements (%)", {"FY2023": "7.21%", "FY2022": "9.38%"}),
        ("SECTION", "Leverage ratio", {}),
        ("DATA", "13 Total exposure measure excluding claims on central banks (£, single pounds as printed)", {"FY2023": 505085850, "FY2022": 472748850}),
        ("DATA", "14 Leverage ratio excluding claims on central banks (%)", {"FY2023": "9.3%", "FY2022": "8.8%"}),
        ("SECTION", "Liquidity Coverage Ratio (* average of preceding 12 months, per the editions' own footnote)", {}),
        ("DATA", "15 Total high-quality liquid assets (HQLA) (weighted value -average) (£, single pounds as printed)", {"FY2023": 119485890, "FY2022": 111134353}),
        ("DATA", "UK 16a Cash outflows - total weighted value (£, single pounds as printed)", {"FY2023": 31080764, "FY2022": 33822803}),
        ("DATA", "UK 16b Cash inflows - total weighted value (£, single pounds as printed)", {"FY2023": 7395149, "FY2022": 5606270}),
        ("DATA", "16 Total net cash outflows (adjusted value) (£, single pounds as printed)", {"FY2023": 23685615, "FY2022": 28216533}),
        ("DATA", "17 Liquidity coverage ratio (%)", {"FY2023": "504%", "FY2022": "394%"}),
        ("SECTION", "Net Stable Funding Ratio (** average of preceding four quarters, per the editions' own footnote)", {}),
        ("DATA", "18 Total available stable funding (£, single pounds as printed)", {"FY2023": 521345972, "FY2022": 475506474}),
        ("DATA", "19 Total required stable funding (£, single pounds as printed)", {"FY2023": 351654764, "FY2022": 331042832}),
        ("DATA", "20 Net stable funding ratio (%)", {"FY2023": "148%", "FY2022": "144%"}),
        ("SECTION", "FY2017-FY2021 editions - earlier Basel III 'Overview of prudential metrics' template. Row numbers are NOT the UK template's: plain '7a' here is the fully loaded ECL total capital ratio, not an SREP requirement.", {}),
        ("SECTION", "Available capital (amounts)", {}),
        ("DATA", "1 Common Equity Tier 1 (CET1) (£, single pounds as printed)", {"FY2021": 39399478, "FY2020": 27396631, "FY2019": 25830817, "FY2018": 15052746, "FY2017": 9142139}),
        ("DATA", "1a Fully loaded ECL accounting model (£, single pounds as printed)", {"FY2021": 39399478, "FY2020": 27396631, "FY2019": 25830817, "FY2018": 15052746, "FY2017": 9142139}),
        ("DATA", "2 Tier 1 (£, single pounds as printed)", {"FY2021": 39399478, "FY2020": 27396631, "FY2019": 25830817, "FY2018": 15052746, "FY2017": 9142139}),
        ("DATA", "2a Fully loaded ECL accounting model Tier 1 (£, single pounds as printed)", {"FY2021": 39399478, "FY2020": 27396631, "FY2019": 25830817, "FY2018": 15052746, "FY2017": 9142139}),
        ("DATA", "3 Total regulatory capital (£, single pounds as printed)", {"FY2021": 49909754, "FY2020": 38647805, "FY2019": 26211691, "FY2018": 15147620, "FY2017": 9142150}),
        ("DATA", "3a Fully loaded ECL accounting model regulatory capital (£, single pounds as printed)", {"FY2021": 49909754, "FY2020": 38647805, "FY2019": 26211691, "FY2018": 15147620, "FY2017": 9142150}),
        ("SECTION", "Risk-weighted assets (amounts)", {}),
        ("DATA", "4 Total risk-weighted assets (RWA) (£, single pounds as printed)", {"FY2021": 233133033, "FY2020": 205441523, "FY2019": 114001332, "FY2018": 52495810, "FY2017": 8268832}),
        ("SECTION", "Risk-based capital ratios as a percentage of RWA", {}),
        ("DATA", "5 Common Equity Tier 1 ratio (%)", {"FY2021": "16.9%", "FY2020": "13.34%", "FY2019": "20.08%", "FY2018": "22.83%", "FY2017": "59.78%"}),
        ("DATA", "5a Fully loaded ECL accounting model Common Equity Tier 1 (%)", {"FY2021": "16.9%", "FY2020": "13.34%", "FY2019": "20.08%", "FY2018": "22.83%", "FY2017": "59.78%"}),
        ("DATA", "6 Tier 1 ratio (%)", {"FY2021": "16.9%", "FY2020": "13.34%", "FY2019": "20.08%", "FY2018": "22.83%", "FY2017": "59.78%"}),
        ("DATA", "6a Fully loaded ECL accounting model Tier 1 ratio (%)", {"FY2021": "16.9%", "FY2020": "13.34%", "FY2019": "20.08%", "FY2018": "22.83%", "FY2017": "59.78%"}),
        ("DATA", "7 Total regulatory capital ratio (%)", {"FY2021": "21.4%", "FY2020": "18.81%", "FY2019": "20.38%", "FY2018": "22.99%", "FY2017": "59.78%"}),
        ("DATA", "7a Fully loaded ECL accounting model total capital ratio (%)", {"FY2021": "21.4%", "FY2020": "18.81%", "FY2019": "20.38%", "FY2018": "22.99%", "FY2017": "59.78%"}),
        ("SECTION", "Additional CET1 buffer requirements as a percentage of RWA", {}),
        ("DATA", "8 Capital conservation buffer requirement (%)", {"FY2021": "2.5%", "FY2020": "2.50%", "FY2019": "2.50%", "FY2018": "1.875%", "FY2017": "0%"}),
        ("DATA", "9 Countercyclical buffer requirement (%)", {"FY2021": "0.0%", "FY2020": "0.00%", "FY2019": "1.00%", "FY2018": "1.00%", "FY2017": "0%"}),
        ("DATA", "10 Bank G-SIB and/or D-SIB additional requirements (%)", {"FY2021": "0.0%", "FY2020": "0%", "FY2019": "0%", "FY2018": "0%", "FY2017": "0%"}),
        ("DATA", "11 Total of Bank CET1 specific buffer requirements (%) (row 8 + row 9 + row 10)", {"FY2021": "2.5%", "FY2020": "2.50%", "FY2019": "3.50%", "FY2018": "2.875%", "FY2017": "0%"}),
        ("DATA", "12 CET1 available after meeting the Bank's minimum capital requirements (%)", {"FY2021": "10.9%", "FY2020": "4.34%", "FY2019": "4.09%", "FY2018": "8.275%", "FY2017": "0%"}),
        ("SECTION", "Basel III Leverage Ratio", {}),
        ("DATA", "13 Total Basel III Leverage ratio exposure measure (£, single pounds as printed)", {"FY2021": 535602756, "FY2020": 448047098, "FY2019": 264626187, "FY2018": 143250300, "FY2017": 34912525}),
        ("DATA", "14 Basel III leverage ratio (%) (row 2 / row 13)", {"FY2021": "7.4%", "FY2020": "6.11%", "FY2019": "9.76%", "FY2018": "10.51%", "FY2017": "26.19%"}),
        ("DATA", "14a Fully loaded ECL accounting model Basel III leverage ratio (%) (row 3 / row 13)", {"FY2021": "9.3%", "FY2020": "8.15%", "FY2019": "9.91%", "FY2018": "10.51%", "FY2017": "28.67%"}),
        ("SECTION", "Liquidity Coverage Ratio", {}),
        ("DATA", "15 Total HQLA (£, single pounds as printed)", {"FY2021": 111539577, "FY2020": 88860083, "FY2019": 84588399, "FY2018": 56305459, "FY2017": 15024205}),
        ("DATA", "16 Total net cash outflows (£, single pounds as printed)", {"FY2021": 11495946, "FY2020": 18303758, "FY2019": 18699805, "FY2018": 16501130, "FY2017": 2412433}),
        ("DATA", "17 LCR ratio (%)", {"FY2021": "970.3%", "FY2020": "485.47%", "FY2019": "541.05%", "FY2018": "399.32%", "FY2017": "622.78%"}),
        ("DATA", "18 NSFR (%)", {"FY2019": "170.9%"}),
    ],
    sources_text=KM1_SOURCES,
    first_col_width=84,
    source_height=560,
)

metric("CET1 Capital", "£", [("Common Equity Tier 1 capital (rounded as reported)", {"FY2025": 48900000, "FY2024": 48400000, "FY2023": 46800000, "FY2022": 41400000, "FY2021": 39400000, "FY2020": 27396631, "FY2019": 25830817, "FY2018": 15052747, "FY2017": 9142150})], "The annual reports state CET1 capital rounded to £m; these values preserve that stated precision and are not presented as inferred exact amounts. FY2020-FY2017 use the Total Tier 1 capital figure from each year's own regulatory capital note (no AT1 capital is disclosed in any year, so Tier 1 = CET1).")
metric("CET1 Ratio", "% of RWA", [("Common Equity Tier 1 ratio", {"FY2025": "16.6%", "FY2024": "15.1%", "FY2023": "16.0%", "FY2022": "15.4%", "FY2021": "16.9%", "FY2020": "13.34%", "FY2019": "20.08%", "FY2018": "22.83%", "FY2017": "59.78%"})], "FY2019 AND FY2018 REPLACED 2026-09-15 (second pass) WITH THE BANK'S OWN DIRECTLY-PRINTED FIGURES. These cells previously read 20.3% and 23.18%, values NOT disclosed as CET1 ratios at all - they were each year's Annual Report total capital ratio, copied across on the strength of the Bank's narrative that capital resources were '100% CET1'. Row 5 of the KM1 table in the Bank's own Pillar 3 disclosures prints the CET1 ratio directly for all three of these years: FY2019 20.08% and FY2018 22.83% (FY2019 edition, Table 4, p.16, and reconfirmed by the FY2020 edition's comparative), FY2017 59.78% (FY2017 edition, row 5 - which happens to equal the previously-carried value, so that cell is unchanged). A directly printed figure supersedes a derived equivalence, so the derivation is retired. The replacements reconcile: 25,830,817/128,612,638 = 20.08% and 15,052,746/65,893,829 = 22.84% against a printed 22.83%. On the FY2018 figure specifically, the Annual Report's 23.18% is not a rounding difference from 22.83% but a different measure - total EQUITY of 15,274,275 divided by RWA of 65,893,829 gives exactly 23.18%, where the regulatory ratio uses CET1 own funds of 15,052,746. FY2020 FILLED 2026-09-15: this cell previously read 'Not publicly disclosed', on the ground that from FY2020 the Bank moved to a 75% CET1 / 25% Tier 2 structure 'with no separate CET1 ratio disclosed anywhere in the report'. That was true of the ANNUAL REPORT but not of the Bank's Pillar 3 disclosure, which was not consulted at the time - row 5 of the FY2020 edition's KM1 table states the CET1 ratio as 13.34% (2019: 20.08%) directly. The FY2021 edition restates it as 13.3%, a rounding difference only. This is a disclosed figure, not a derivation. See the PILLAR 3 DISCOVERY NOTE in the source citation.")
metric("Tier 1 Capital", "£", [("Total Tier 1 capital", {"FY2025": 48846803, "FY2024": 48365248, "FY2023": 46764475, "FY2022": 41430663, "FY2021": 39399478, "FY2020": 27396631, "FY2019": 25830817, "FY2018": 15052747, "FY2017": 9142150})])
metric("Tier 1 Ratio", "% of RWA", [("Tier 1 ratio", {"FY2023": "16.0%", "FY2022": "15.4%", "FY2021": "16.9%", "FY2020": "13.34%", "FY2019": "20.08%", "FY2018": "22.83%", "FY2017": "59.78%"})],
       "RECOVERED 2026-09-15 - this sheet previously read 'Not publicly disclosed' for every year, on the stated ground that 'no separate Tier 1 ratio is stated in the public Redwood reports'. That was wrong: row 6 of the KM1 table in each of the Bank's own Pillar 3 disclosures states it directly. FY2023/FY2022 from the FY2023 edition (Table 1, p.4); FY2021/FY2020 from the FY2021 edition (Table 1, pp.4-5); FY2019 from the FY2019 edition's own Table 4 (and reconfirmed by the FY2020 edition's comparative); FY2018 and FY2017 added on a second pass the same day from the FY2019 and FY2017 editions' own row 6. In every year Tier 1 ratio equals the CET1 ratio, which is consistent with the Bank disclosing no AT1 capital in any year - note this is the source's own printed row 6, NOT a value copied across from row 5. FY2025/FY2024 are blank because the Bank became an SDDT on 26/07/2024 and publishes no Pillar 3 for those years; the Annual Reports state only a CET1 ratio and a total capital ratio, not a Tier 1 ratio. See the PILLAR 3 DISCOVERY NOTE in the source citation.")
metric("Total Capital", "£", [("Total regulatory capital / own funds", {"FY2025": 58505932, "FY2024": 58431891, "FY2023": 56888551, "FY2022": 51320588, "FY2021": 49909754, "FY2020": 36528841, "FY2019": 26211691, "FY2018": 15147621, "FY2017": 9142150})])
metric("Total Capital Ratio", "% of RWA", [("Total capital ratio", {"FY2025": "19.8%", "FY2024": "18.3%", "FY2023": "19.4%", "FY2022": "19.0%", "FY2021": "21.4%", "FY2020": "17.8%", "FY2019": "20.38%", "FY2018": "22.99%", "FY2017": "59.78%"})],
       "FY2019 AND FY2018 MOVED TO THE PILLAR 3 BASIS 2026-09-15 (second pass), replacing 20.3% and 23.18% taken "
       "from each year's Annual Report capital risk management note (which states its ratios as '(unaudited)'). "
       "Row 7 of the KM1 table in the Bank's own Pillar 3 disclosures gives 20.38% for FY2019 and 22.99% for "
       "FY2018, both reconciling exactly against this workbook's own figures: 26,211,691/128,612,638 = 20.38% and "
       "15,147,620/65,893,829 = 22.99%. FY2019's change is a rounding refinement only. FY2018's is not: the "
       "Annual Report's 23.18% is total EQUITY of 15,274,275 over the same RWA, i.e. a different numerator, so "
       "the two are not two roundings of one number and the regulatory figure is the one carried. FY2017's "
       "59.78% is identical on both bases and is unchanged. FY2020's 17.8% is the Bank's own RESTATED figure - "
       "the FY2020 edition originally printed total regulatory capital of 38,647,805 and a ratio of 18.81%, and "
       "the FY2021 edition restates both to 36,528,841 and 17.8% with the footnote 'Restated due to the "
       "correction of total regulatory capital and its ratio and leverage ratio'; the restated value is carried "
       "and the superseded one recorded here. FY2025-FY2021 are unchanged.")
metric("Total RWAs", "£", [("Total risk-weighted assets (RWA)", {"FY2023": 294050082, "FY2022": 269415717, "FY2021": 233133033, "FY2020": 205441523, "FY2019": 128612638, "FY2018": 65893829, "FY2017": 15293832})],
       "RECOVERED 2026-09-15 - previously 'Not publicly disclosed' for every year. FY2023/FY2022 from the FY2023 "
       "edition's KM1 (Table 1, p.4); FY2021/FY2020 from the FY2021 edition's KM1 (Table 1, p.4). Cross-checked: "
       "the FY2022 edition's own FY2021 comparative reproduces 233,133,033 exactly.\n"
       "FY2019 CORRECTED AND FY2018/FY2017 ADDED, SECOND PASS, SAME DAY - AND THE SOURCE'S OWN KM1 ROW 4 IS "
       "WRONG FOR THOSE YEARS. FY2019 previously read 114,001,332, taken from row 4 of the FY2020 edition's KM1 "
       "comparative column. That figure is the CREDIT-RISK SUBTOTAL, not total RWA: the FY2019 edition's own "
       "Pillar 1 table (Table 6) prints 'Total Credit Risk 114,001,332' and then 'Operational Risk - Basic "
       "Indicator Approach 14,611,306', giving 'Total Pillar 1 Risk Weighted Assets 128,612,638'. The Bank's own "
       "printed ratios settle which is the real denominator: CET1 25,830,817 / 128,612,638 = 20.08% and total "
       "capital 26,211,691 / 128,612,638 = 20.38%, exactly the 20.08% and 20.38% printed in the same KM1 table; "
       "against 114,001,332 the same capital gives 22.66% and 22.99%, which appear nowhere. The defect is "
       "systematic across the three oldest editions - FY2017's KM1 row 4 reads 8,268,832 (credit risk) where the "
       "Pillar 1 table totals 15,293,832, and FY2018's reads 52,495,810 where the table totals 65,893,829 - and "
       "in each case the printed ratio reconciles only against the Pillar 1 table total (9,142,150/15,293,832 = "
       "59.78%; 15,052,746/65,893,829 = 22.84% vs a printed 22.83%). From the FY2020 edition onward row 4 is "
       "correct (205,441,523 against a Pillar 1 table total of 205,441,525, a GBP2 rounding difference only). "
       "This sheet therefore takes FY2019-FY2017 from each year's Pillar 1 capital-requirements table rather "
       "than from its KM1 row 4, and the discarded row 4 values are recorded here so the choice is auditable.\n"
       "FY2025/FY2024 are blank because the Bank became an SDDT on 26/07/2024 and publishes no Pillar 3 for "
       "those years; no RWA figure appears in the FY2024 or FY2025 Annual Report, and none is derived here from "
       "the disclosed capital and ratio. See the PILLAR 3 DISCOVERY NOTE in the source citation.")

bw.add_rwa_breakdown_sheet(
    title="Redwood Bank Limited — RWA Breakdown",
    subtitle="Pillar 1 risk-weighted assets by standardised exposure class, £, FY2017-FY2023 (every year the Bank "
             "published a Pillar 3). Recovered 2026-09-15 from the Bank's own Pillar 3 disclosures; previously "
             "recorded as not publicly disclosed. FY2025/FY2024 blank - SDDT, no Pillar 3 published.",
    rows=[
        ("SECTION", "Credit risk - standardised approach, by exposure class", {}),
        ("DATA", "Institutions", {"FY2023": 583047, "FY2022": 946102, "FY2021": 626025, "FY2020": 508930, "FY2019": 425199, "FY2018": 334991, "FY2017": 838261}),
        ("DATA", "Secured by mortgages on residential property", {"FY2023": 70065294, "FY2022": 27562520, "FY2021": 68247424, "FY2020": 57320883, "FY2019": 26921059, "FY2018": 13274257, "FY2017": 1194463}),
        ("DATA", "Secured by mortgages on commercial real estate", {"FY2023": 145500647, "FY2022": 196007206, "FY2021": 137862947, "FY2020": 128085685, "FY2019": 85870604, "FY2018": 38181083, "FY2017": 5619059}),
        ("DATA", "Past due", {"FY2023": 35540399, "FY2022": 14025145, "FY2021": 5461469, "FY2020": 6309056}),
        ("DATA", "Other items", {"FY2023": 1839907, "FY2022": 1095331, "FY2021": 798294, "FY2020": 773708, "FY2019": 784469, "FY2018": 705480, "FY2017": 617049}),
        ("TOTAL", "Total credit risk", {"FY2023": 253529294, "FY2022": 239636304, "FY2021": 212996159, "FY2020": 192998262, "FY2019": 114001332, "FY2018": 52495810, "FY2017": 8268832}),
        ("SECTION", "Operational risk", {}),
        ("DATA", "Operational risk - basic indicator approach", {"FY2023": 40520788, "FY2022": 29779413, "FY2021": 20136875, "FY2020": 12443263, "FY2019": 14611306, "FY2018": 13398025, "FY2017": 7025000}),
        ("TOTAL", "Total Pillar 1 risk-weighted assets", {"FY2023": 294050082, "FY2022": 269415717, "FY2021": 233133034, "FY2020": 205441525, "FY2019": 128612638, "FY2018": 65893829, "FY2017": 15293832}),
    ],
    sources_text=(
        "Sources - each year's own Redwood Bank Limited Pillar 3 Disclosures, 'Total Pillar 1 risk weighted "
        "assets / capital requirement' table (Table 7 in the FY2021 edition, Table 6 in the FY2019 edition, "
        "section 6 in the FY2023 edition - the Bank renumbers it between vintages but the table is the same "
        "one):\n"
        f"FY2023 and its own FY2022 comparative: FY2023 edition, p.20 - {P3_2023_URL}\n"
        f"FY2021 and its own FY2020 comparative: FY2021 edition, Table 7, p.21 - {P3_2021_URL}\n"
        f"FY2019 and its own FY2018 comparative: FY2019 edition, Table 6 - {P3_2019_URL}\n"
        f"FY2017: FY2017 edition - {P3_2017_URL} (the FY2018 edition, {P3_2018_URL}, reproduces the same FY2017 "
        "column and was used to confirm it)\n\n"
        "ALL SEVEN YEARS ADDED OR CONFIRMED 2026-09-15. The first pass this day filled FY2023/FY2022 only and "
        "recorded here that the FY2021 and FY2020 editions 'present capital requirements in a different format "
        "rather than this single consolidated RWA-by-exposure-class table'. That was wrong - the FY2021 edition "
        "carries exactly this table as its Table 7, with a full 2020 comparative column, and the FY2019, FY2018 "
        "and FY2017 editions carry it too. Five further years were transcribed as a result.\n\n"
        "VALIDATION - every year's exposure classes foot to that year's printed credit-risk subtotal and then to "
        "its printed Pillar 1 total. FY2023 583,047+70,065,294+145,500,647+35,540,399+1,839,907 = 253,529,294; "
        "+40,520,788 = 294,050,082. FY2022 = 239,636,304; +29,779,413 = 269,415,717. FY2021 626,025+68,247,424+"
        "137,862,947+5,461,469+798,294 = 212,996,159; +20,136,875 = 233,133,034. FY2020 508,930+57,320,883+"
        "128,085,685+6,309,056+773,708 = 192,998,262; +12,443,263 = 205,441,525. FY2017 838,261+1,194,463+"
        "5,619,059+617,049 = 8,268,832; +7,025,000 = 15,293,832.\n"
        "THREE PENCE-LEVEL RESIDUALS IN THE SOURCE, CARRIED NOT SILENTLY FIXED: FY2019's classes sum to "
        "114,001,331 against a printed credit-risk subtotal of 114,001,332 (GBP1); FY2018's sum to 52,495,811 "
        "against a printed 52,495,810 (GBP1), and its printed Pillar 1 total of 65,893,829 sits GBP6 below "
        "52,495,810+13,398,025 = 65,893,835. In each case the PRINTED figure is carried, because it is the one "
        "the Bank's own capital requirement column is computed from (65,893,829 x 8% = 5,271,506, the printed "
        "requirement). These are the Bank's roundings, not transcription errors.\n\n"
        "TOTALS VS THE TOTAL RWAs SHEET: FY2023-FY2017 tie exactly, with two GBP1-GBP2 exceptions where the KM1 "
        "and the Pillar 1 table disagree in the Bank's own documents - FY2021 233,133,034 here against KM1's "
        "233,133,033, and FY2020 205,441,525 here against KM1's 205,441,523. Far more importantly, see the Total "
        "RWAs sheet's note on why FY2019-FY2017 CANNOT be taken from KM1 row 4 at all: in those three editions "
        "row 4 prints the credit-risk subtotal (the 'Total credit risk' row above) instead of the Pillar 1 "
        "total, and this sheet is what makes that visible.\n\n"
        "PAST DUE is blank for FY2019, FY2018 and FY2017 because the source leaves the row empty in those years "
        "- the Bank held no past-due exposure attracting a separate risk weight - not because the figure is "
        "unknown.\n"
        "EXPOSURE CLASSES PRINTED BUT EMPTY in every year (no exposure held): central government and central "
        "banks, regional governments or local authorities, administrative bodies and non-commercial, multilateral "
        "development banks, international organisations, corporates, retail, regulatory high-risk categories, "
        "covered bonds, securitisation positions, short-term claims on institutions and corporates, and "
        "collective investment undertakings. These are omitted above rather than written as zero, since the "
        "source leaves them blank. MARKET RISK is structurally nil and is stated as such: 'The Bank is not "
        "exposed to market risk as it does not operate a trading book.'\n"
        "FY2025 AND FY2024: no Pillar 3 exists - the Bank became an SDDT on 26/07/2024 (see below), and neither "
        "Annual Report contains an RWA breakdown.\n\n"
        + PILLAR3_DISCOVERY_NOTE
    ),
    first_col_width=54,
    source_height=300,
    unit_suffix=" (£)",
)

metric("Leverage Ratio", "%",
       [("Leverage ratio excluding claims on central banks (UK KM1 row 14)", {"FY2023": "9.3%", "FY2022": "8.8%", "FY2021": "8.6%"}),
        ("Basel III leverage ratio, Tier 1 / total exposure incl. central bank claims (row 2 / row 13)", {"FY2021": "7.4%", "FY2020": "6.11%", "FY2019": "9.76%", "FY2018": "10.51%", "FY2017": "26.19%"})],
       "RECOVERED 2026-09-15 - previously 'Not publicly disclosed' for every year. TWO CLEARLY-SEPARATED BASES, deliberately not merged into one row: the Bank changed its leverage definition between the FY2021 and FY2022 editions, and the two are not like-for-like. The FY2022 and FY2023 editions report row 14 as 'Leverage ratio excluding claims on central banks'; the FY2021 and FY2020 editions report a Basel III leverage ratio computed as Tier 1 over a total exposure measure that INCLUDES central bank claims. FY2021 appears on both rows because both documents state it - 8.6% on the newer basis (FY2022 edition's own comparative column) and 7.4% on the older (FY2021 edition, Table 1 row 14) - which quantifies the gap at ~1.2pp and is exactly why they are kept apart. Splicing these into a single series would manufacture a false trend. FY2020's 6.11% and FY2019's 9.76% are from the FY2020 edition (Table 1, row 14); FY2018's 10.51% and FY2017's 26.19% were added on a second pass the same day from the FY2019 and FY2017 editions' own row 14, and the FY2018 edition's own comparative column independently reproduces both. Every year on this row uses the pre-FY2022 Basel III definition, so FY2017-FY2021 read as a single consistent series. NOTE the FY2021 edition restates FY2020's leverage ratio to 6.1% with the footnote 'Restated due to the correction of total regulatory capital and its ratio and leverage ratio'; the FY2020 edition's own originally-published 6.11% is shown here per this project's own-year convention, with the restatement recorded. FY2025/FY2024 blank - SDDT exempt from 26/07/2024, and no leverage ratio appears in either Annual Report. See the PILLAR 3 DISCOVERY NOTE in the source citation.")
metric("LCR", "%",
       [("Liquidity coverage ratio - Annual Report basis (as previously carried)", {"FY2025": "362%", "FY2024": "284%", "FY2023": "481%", "FY2022": "352%", "FY2021": "970%", "FY2020": "485%", "FY2019": "557%", "FY2018": "391%", "FY2017": "339%"}),
        ("Liquidity coverage ratio - Pillar 3 KM1 row 17, average of preceding 12 months", {"FY2023": "504%", "FY2022": "394%", "FY2021": "500%"}),
        ("Liquidity coverage ratio - Pillar 3, point-in-time at 31 December", {"FY2021": "970.3%", "FY2020": "485.5%", "FY2019": "541.05%", "FY2018": "391.32%", "FY2017": "622.78%"})],
       "SPLIT INTO SEPARATE BASES 2026-09-15. The single row previously carried here was silently mixed, and the Bank's own Pillar 3 disclosures prove it. The FY2022 and FY2023 editions footnote row 17 as '* Average of preceding 12 months' and give 394% and 504%; the FY2021 and FY2020 editions instead print a point-in-time ratio (HQLA 111,539,577 / net outflows 11,495,946 = 970.3% at 31 December 2021, and 485.5% at 31 December 2020). The previously-carried row took FY2021 and FY2020 from the point-in-time basis (970%, 485%) but FY2022 and FY2023 from the Annual Report (352%, 481%) - three different bases in one series. Most starkly, FY2021 is 970.3% point-in-time but 500% as the FY2022 edition's own 12-month-average comparative: a 470pp gap on the SAME year and the SAME entity, purely from the averaging convention. All three rows are kept, each labelled, and none is deleted - following the treatment applied to Access Bank and Zenith Bank in this workbook set. DO NOT read a trend across rows. FY2019, FY2018 and FY2017 were added to the point-in-time row on a second pass the same day, from row 17 of each year's own KM1 plus the matching narrative ('The Bank's LCR as at the 31st December 2019 was 541.05% (2018: 391.32%)'; the FY2017 edition states 622.78%). FY2018's 391.32% and FY2017's 339% vs 622.78% are worth contrasting: FY2018 shows the Annual Report and the Pillar 3 agreeing to the decimal on the same point-in-time basis, while FY2019 (557% vs 541.05%) and FY2017 (339% vs 622.78%) show them diverging materially - which is why the two rows stay separate rather than being merged into one 'LCR' series.")
metric("NSFR", "%", [("Net stable funding ratio", {"FY2023": "148%", "FY2022": "144%", "FY2021": "148.9%", "FY2020": "150.5%", "FY2019": "170.9%", "FY2018": "193.38%"})],
       "RECOVERED 2026-09-15 - previously 'Not publicly disclosed' for every year. Row 20 of the KM1 table in the Bank's own Pillar 3 disclosures, stated as an average of the preceding four quarters. FY2023/FY2022 from the FY2023 edition (Table 1, p.5); FY2021/FY2020 from the FY2021 edition, which states in narrative form 'NSFR as at 31 December 2021 is 148.9% (2020: 150.5%), against a regulatory requirement of 100%' and backs it with full Tables 17 and 18. FY2019 AND FY2018 ADDED on a second pass the same day: the FY2019 edition states 'the NSFR as at 31 December 2019 is 170.9% (2018: 193.38%)' in narrative and prints 170.9% as row 34 of its full NSFR template (Table 15), and 170.9% also appears as row 18 of its KM1. FY2017 stays blank - the FY2017 edition's KM1 stops at row 17 (LCR) and carries no NSFR row or template, so the Bank simply had not begun disclosing it. NOTE FY2021, FY2020, FY2019 and FY2018 all PREDATE the UK NSFR requirement, which took effect only on 1 January 2022 under PRA PS17/21 - Redwood therefore disclosed these voluntarily, and they are genuine disclosed figures rather than a regulatory-template obligation. Minor basis nuance: the FY2022 edition's own FY2021 comparative shows 148% against the FY2021 edition's own 148.9%, a rounding/averaging difference between two of the Bank's own documents; each year's own report is used. FY2025/FY2024 blank - SDDT exempt from 26/07/2024. See the PILLAR 3 DISCOVERY NOTE in the source citation.")
metric("MREL Ratio", None, [("MREL ratio", {y: "Not publicly disclosed" for y in YEARS})])

bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {"FY2025": 610043348, "FY2024": 635400816, "FY2023": 599055370, "FY2022": 540260485, "FY2021": 527973212, "FY2020": 436448406, "FY2019": 257912436, "FY2018": 138334395, "FY2017": 28396898}),
        ("Loans and advances to customers", {"FY2025": 490444848, "FY2024": 492244170, "FY2023": 413983306, "FY2022": 403371972, "FY2021": 369798691, "FY2020": 323879674, "FY2019": 170218565, "FY2018": 79422117, "FY2017": 8413052}),
        ("Customer deposits", {"FY2025": 546762522, "FY2024": 552995571, "FY2023": 499967473, "FY2022": 447173300, "FY2021": 438038613, "FY2020": 379609727, "FY2019": 230922849, "FY2018": 122443079, "FY2017": 18661835}),
        ("Total equity", {"FY2025": 49983070, "FY2024": 49380257, "FY2023": 47552169, "FY2022": 43325959, "FY2021": 41496104, "FY2020": 27580707, "FY2019": 26026545, "FY2018": 15274275, "FY2017": 9305255}),
    ],
    balance_sheet_unit="£",
    income_statement_totals=[
        ("Net interest income", {"FY2025": 22720767, "FY2024": 26251547, "FY2023": 28828970, "FY2022": 20868106, "FY2021": 15135536, "FY2020": 10396516, "FY2019": 6373765, "FY2018": 1892669, "FY2017": 38893}),
        ("Administrative expenses", {"FY2025": -21265984, "FY2024": -21675255, "FY2023": -20509671, "FY2022": -16105258, "FY2021": -12922871, "FY2020": -9382145, "FY2019": -7297813, "FY2018": -5457647, "FY2017": -3380275}),
        ("Profit for the year", {"FY2025": 602813, "FY2024": 1828088, "FY2023": 4204249, "FY2022": 1797614, "FY2021": 4084475, "FY2020": -1703477, "FY2019": -1228742, "FY2018": -3805978, "FY2017": -3341382}),
    ],
    income_statement_unit="£",
    equity_changes_totals=[
        ("Total equity (closing)", {"FY2025": 49983070, "FY2024": 49380257, "FY2023": 47552169, "FY2022": 43325959, "FY2021": 41496104, "FY2020": 27580707, "FY2019": 26026545, "FY2018": 15274275, "FY2017": 9305255}),
    ],
    equity_changes_unit="£",
    cash_flow_totals=[
        ("Net cash from/(used in) operating activities", {"FY2025": -27582757, "FY2024": -41683581, "FY2023": 49423566, "FY2022": -20780795, "FY2021": 15466786, "FY2020": -6447584, "FY2019": 16895343, "FY2018": 29122121, "FY2017": 6785559}),
        ("Net cash generated/(used in) investing activities", {"FY2025": 4472207, "FY2024": 47849547, "FY2023": -24192052, "FY2022": -509405, "FY2021": -19793859, "FY2020": 19825448, "FY2019": -10169522, "FY2018": -25284982, "FY2017": -15609842}),
        ("Net cash from financing activities", {"FY2025": 0, "FY2024": 0, "FY2023": 0, "FY2022": 0, "FY2021": 28300000, "FY2020": 31400000, "FY2019": 12000000, "FY2018": 9803866, "FY2017": 13018542}),
        ("Cash and cash equivalents at end of year", {"FY2025": 90182943, "FY2024": 115416225, "FY2023": 109250259, "FY2022": 84018745, "FY2021": 105308945, "FY2020": 81336018, "FY2019": 36558154, "FY2018": 17832333, "FY2017": 4191328}),
    ],
    cash_flow_unit="£",
    ratios=[
        ("CET1 Ratio", {"FY2025": "16.6%", "FY2024": "15.1%", "FY2023": "16.0%", "FY2022": "15.4%", "FY2021": "16.9%", "FY2020": "13.34%", "FY2019": "20.3%", "FY2018": "23.18%", "FY2017": "59.78%"}),
        ("Total Capital Ratio", {"FY2025": "19.8%", "FY2024": "18.3%", "FY2023": "19.4%", "FY2022": "19.0%", "FY2021": "21.4%", "FY2020": "17.8%", "FY2019": "20.3%", "FY2018": "23.18%", "FY2017": "59.78%"}),
        ("LCR", {"FY2025": "362%", "FY2024": "284%", "FY2023": "481%", "FY2022": "352%", "FY2021": "970%", "FY2020": "485%", "FY2019": "557%", "FY2018": "391%", "FY2017": "339%"}),
    ],
    note="CET1 capital is rounded to the nearest £m as stated in Redwood's KPI narrative. Undisclosed regulatory metrics remain blank/not publicly disclosed on their detail sheets.",
)

bw.save("/Users/armaan/code/katalysis/banks/REDWOOD BANK FINANCIALS.xlsx")
