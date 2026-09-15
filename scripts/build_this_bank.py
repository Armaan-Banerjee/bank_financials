import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook


YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021", "FY2020"]
YEAR_LABEL = {y: y for y in YEARS}
CH = "https://find-and-update.company-information.service.gov.uk/company/11734380/filing-history"
AR = {
    "FY2025": CH + "/MzQ5MTMwMDUxNWFkaXF6a2N4/document?format=pdf&download=0",
    "FY2024": CH + "/MzQ0ODU3NTgzNmFkaXF6a2N4/document?format=pdf&download=0",
    "FY2023": CH + "/MzQwNjUwNzIyNmFkaXF6a2N4/document?format=pdf&download=0",
    "FY2022": CH + "/MzM2MTc0NDEyNGFkaXF6a2N4/document?format=pdf&download=0",
    "FY2021": CH + "/MzMyMzU2MjI3MGFkaXF6a2N4/document?format=pdf&download=0",
    "FY2020": CH + "/MzI4NjQ2NzM3NmFkaXF6a2N4/document?format=pdf&download=0",
}

ENTITY_NOTE = (
    "THIS BANK LIMITED (company 11734380, FRN 832786) is the UK bank formerly named JN Bank UK Ltd. "
    "The legal name changed on 19 January 2026; the FY2021-FY2025 Companies House accounts were filed under "
    "the former JN Bank UK Ltd name. The entity is a UK private bank authorised by the PRA and regulated by the "
    "PRA/FCA. The FY2025 accounts discuss the post-2024 change in ownership; figures in this workbook remain the "
    "UK entity's own annual-account figures, not parent-group figures."
)

HISTORICAL_FLOOR_NOTE = (
    "HISTORICAL FLOOR: the company was incorporated 19 December 2018 (Companies House #11734380) and its "
    "accounting reference date was extended (AA01 filed 29 Aug 2019) so that its FIRST statutory accounts cover "
    "a 16-month period from incorporation to 31 March 2020, filed 22 Dec 2020 - there is no distinct FY2018 or "
    "FY2019 period, filed or otherwise, for this entity. FY2020 is therefore this bank's true confirmed floor, "
    "not FY2018 as a generic project-wide target might suggest; re-verified directly against the FY2020 Companies "
    "House filing itself (a scanned/image-only PDF, OCR'd and cross-checked page-by-page), not assumed from any "
    "earlier scan."
)


def account_sources():
    return (
        "Sources - THIS BANK LIMITED / JN Bank UK Ltd own annual accounts, all figures in £'000 unless stated otherwise:\n"
        "FY2025: Annual report and financial statements for year ended 31 March 2025, Statement of cash flows p.33 and financial KPIs pp.6-7 - " + AR["FY2025"] + "\n"
        "FY2024: Annual report and financial statements for year ended 31 March 2024, Statement of cash flows pp.32-33 and financial KPIs pp.6-7 - " + AR["FY2024"] + "\n"
        "FY2023: Annual report and financial statements for year ended 31 March 2023, Statement of cash flows p.28 and risk/capital disclosures pp.71-72 - " + AR["FY2023"] + "\n"
        "FY2022: Annual report and financial statements for year ended 31 March 2022, Statement of cash flows p.27 and financial KPIs p.8 - " + AR["FY2022"] + "\n"
        "FY2021: Annual report and financial statements for year ended 31 March 2021, Statement of cash flows p.23 and financial KPIs p.7 - " + AR["FY2021"] + "\n"
        "FY2020: Annual report and financial statements for the 16-month period from incorporation (19 December "
        "2018) to 31 March 2020 - the Bank's first filed accounts - Statement of cash flows p.20 and financial "
        "KPIs p.7 - " + AR["FY2020"] + "\n"
        + ENTITY_NOTE + " " + HISTORICAL_FLOOR_NOTE + " All six Companies House PDFs are scanned/image-only; figures were transcribed using OCR and cross-checked against rendered pages."
    )


def p3_sources():
    return (
        "Sources - regulatory capital and liquidity figures disclosed in the entity's own annual accounts (not a separate public Pillar 3 archive):\n"
        "FY2025: financial KPIs and regulatory-capital table, pp.6-7 - " + AR["FY2025"] + "\n"
        "FY2024: financial KPIs and regulatory-capital table, p.6 - " + AR["FY2024"] + "\n"
        "FY2023: the FY2024 accounts' comparative KPI/capital figures are used where the FY2023 report does not present a numeric KPI table, p.6 - " + AR["FY2024"] + "\n"
        "FY2022: financial KPIs and regulatory-capital table, p.8 - " + AR["FY2022"] + "\n"
        "FY2021: 2021 comparative column in the FY2022 regulatory-capital table, p.8; FY2021 accounts' KPI narrative p.7 - " + AR["FY2022"] + " / " + AR["FY2021"] + "\n"
        "FY2020: own regulatory-capital resources table, Note 27 'Risk Management cont.', p.50; KPI narrative p.7 "
        "(CET1 stated only to the nearest £0.1m there, £15.7m) - " + AR["FY2020"] + "\n"
        "SDDT - EXPLICIT NEGATIVE, recorded 2026-09-15 (cross-bank SDDT date-fit pass) so that a future pass "
        "does not wrongly apply the Small Domestic Deposit Taker exemption to this workbook's gap years. The "
        "Bank DOES hold the SDDT opt-in, but it is far too recent to explain anything here. The Bank of England "
        "consolidated list of waivers and modifications granted to PRA-authorised firms (downloaded 2026-09-15, "
        "https://www.bankofengland.co.uk/-/media/boe/files/prudential-regulation/authorisations/"
        "waivers-and-modifications-of-rules/consolidated-waivers-pra-firms.csv) carries two SDDT rows for FRN "
        "832786, 'THIS BANK LIMITED': (a) 'Description - Modification by Consent - PRA Rulebook- CRR Firms- Rule "
        "3.1 of the SDDT Regime - General Application Part 3.1', sub rule 'Ru 3.1', waiver ref 'A00011138P.pdf', "
        "START DATE 06/11/2025, no end date; and (b) 'CRR firms: SDDT Regime - General Application Part 1.2 & "
        "2.1(9)', sub rule 'Ru 1.2 & 2.1(9)', ref 'A00010624P.pdf', start 27/08/2025, end 27/08/2028. Only row "
        "(a) evidences a disclosure exemption. Row (b) modifies ELIGIBILITY CRITERIA only - rule 2.1(9) requires "
        "that 'any parent undertaking of the firm is a UK undertaking', which this entity failed as JN Bank UK "
        "Ltd under Jamaican ownership - and a firm holding only such a row is not a confirmed SDDT.\n"
        "DATE FIT - IT DOES NOT FIT. The Bank's accounting reference date is 31 MARCH, confirmed at Companies "
        "House (company 11734380, accounts filed to 31 March for 2020 through 2025) - note this is NOT a "
        "December year-end, so each FY label here ends on 31 March of that calendar year. The outstanding gap "
        "years are FY2021 and FY2022, which ended 31 MARCH 2021 and 31 MARCH 2022. The Rule 3.1 modification "
        "began 6 NOVEMBER 2025 - more than three and a half years after the later of those two year-ends. A "
        "modification cannot explain a gap that predates it, so the SDDT regime explains NEITHER the FY2021 nor "
        "the FY2022 blanks.\n"
        "Those gaps keep their existing and entirely separate explanation, unchanged: this entity has never "
        "published a standalone Pillar 3 document in ANY year - its accounts state that Pillar 3 disclosures "
        "were available on request - so every regulatory figure in this workbook is transcribed from the annual "
        "accounts, and what is blank is blank because the accounts do not state it (no RWA, leverage, NSFR or "
        "MREL values, and no numeric LCR before FY2023). That is a never-published-anyway gap, not an exemption, "
        "and it is unaffected by the register in every year. The register finding changes no cell in this "
        "workbook. Its only forward-looking value: from 6 November 2025 the Bank is an SDDT, so the "
        "'available on request' Pillar 3 material should not be expected to become a published document for "
        "FY2026 onward. This is the SDDT DISCLOSURE exemption, in force now - not the separate SDDT CAPITAL "
        "regime beginning 1 January 2027.\n"
        + ENTITY_NOTE + " " + HISTORICAL_FLOOR_NOTE + " The accounts state that Pillar 3 disclosures were available on request rather than publishing a standalone Pillar 3 document."
        + "\nRE-VERIFIED 2026-09-15 AT SITE LEVEL (maximum-effort disclosure sweep, prior 'unavailable' verdicts "
        "treated as unproven): thisbank.co.uk is live and was enumerated from its OWN WordPress sitemap index "
        "(wp-sitemap.xml -> page-sitemap.xml) rather than by guessing paths, so this is a complete list of the "
        "site's published pages, not a failed search. It contains no Pillar 3, regulatory-disclosures, investor "
        "or reports page of any kind - the pages are retail product, support-hub, careers and policy pages only. "
        "Five direct path probes (/pillar-3-disclosures, /regulatory-disclosures, /about-us/regulatory-"
        "disclosures, /disclosures, /about-us/pillar-3) each returned HTTP 404 against a site serving HTTP 200. "
        "This corroborates the accounts' own 'available on request' wording from the publication side: the Bank "
        "does not publish Pillar 3 material, so the blanks here are a genuine non-publication rather than an "
        "access failure or an unsearched source."
    )


def statements_sources(kind):
    return (
        f"Sources - THIS BANK LIMITED / JN Bank UK Ltd own {kind}, all figures in £'000 unless stated otherwise:\n"
        "FY2025 & FY2024: Annual report and financial statements for year ended 31 March 2025 - " + AR["FY2025"] + "\n"
        "FY2023 & FY2022: Annual report and financial statements for year ended 31 March 2023 - " + AR["FY2023"] + "\n"
        "FY2021: Annual report and financial statements for year ended 31 March 2021 (own-year figures; the FY2020 comparative column ties FY2021's own report to the FY2022 report's later restated comparative where checked) - " + AR["FY2021"] + "\n"
        "FY2020: Annual report and financial statements for the 16-month period from incorporation (19 December "
        "2018) to 31 March 2020 - the Bank's first filed accounts, own-year figures (not a comparative-column "
        "extraction) - " + AR["FY2020"] + "\n"
        + ENTITY_NOTE + " " + HISTORICAL_FLOOR_NOTE + " All six Companies House PDFs are scanned/image-only; figures were transcribed by rendering and reading each statutory-account page directly."
    )


BS_SOURCES = (
    statements_sources("Statement of Financial Position")
    + "\n\nPage references: FY2025 & FY2024 p.31; FY2023 & FY2022 p.26; FY2021 p.21; FY2020 (own report) p.18."
    + "\n\nPRESENTATION NOTE: FY2025's own statement foots Total assets at £369,555k against Total liabilities and "
    "equity of £369,554k - a genuine £1k rounding difference in the source document itself, reproduced as-is, not "
    "corrected. Investment securities is blank for FY2025 (the account shows a dash - i.e. nil, held as 0 here "
    "would misstate an explicit sold-down position; treated as not applicable that year since the FY2025 report "
    "does not carry the line at all). Deferred tax asset is reported as nil (-) in every year shown. FY2020's own "
    "statement labels the related-party lines 'Due from/to related entities' rather than 'Amounts owed by/to "
    "related party' - the same balances, mapped onto the same rows as every later year. FY2020's Total assets "
    "(£21,653k) ties exactly to Total liabilities (£3,015k) plus Total equity (£18,638k) with zero rounding gap."
    "\n\nINVESTMENT SECURITIES COMPOSITION: checked against the 'Investment securities' note in each year's own "
    "annual accounts - FY2024 Note 12 (also showing the FY2023 comparative column), p.59 of the FY2025 accounts' "
    "prior-year filing (Annual report and financial statements for year ended 31 March 2024); FY2022 Note 13 "
    "(also showing the FY2021 comparative column), p.47 of the Annual report and financial statements for year "
    "ended 31 March 2022; FY2020 Note 11, p.37 of the Annual report and financial statements for the 16-month "
    "period to 31 March 2020. Every year's note breaks the balance into Gilts, Certificates of Deposit and "
    "Treasury Bills, all measured at amortised cost - the Bank's own accounting policy note (Note g.2, 'Investment "
    "Securities') states these 'are UK government bonds and Treasury Bills which are held by the Bank as highly "
    "liquid assets... held at amortised cost'. Certificates of Deposit are nil in every year reviewed (FY2020, "
    "FY2021, FY2022, FY2023, FY2024) and there is no FVOCI/FVTPL column with a nonzero value in the Bank's own "
    "financial-instruments-by-measurement-basis table (Note 32/33) in any year checked - so the balance is 100% "
    "UK-government-issued (gilts and/or Treasury Bills) and 100% amortised cost throughout, with no cross-category "
    "split to show: FY2020 Treasury Bills £14,987k (Gilts nil); FY2021 Treasury Bills £26,705k less £5k ECL "
    "(Gilts nil); FY2022 Gilts £8,536k + Treasury Bills £8,000k + £9k interest receivable less £2k ECL; FY2023 "
    "Gilts £4,878k + Treasury Bills £40,894k + £293k interest receivable less £6k ECL; FY2024 Treasury Bills "
    "£16,580k (Gilts nil) + £222k interest receivable less £2k ECL - each reconciling exactly to the row's own "
    "reported total for that year. FY2025 carries no Investment securities line at all (see above), so no note "
    "exists to check that year."
)
PL_SOURCES = (
    statements_sources("Statement of Profit or Loss and Other Comprehensive Income")
    + "\n\nPage references: FY2025 & FY2024 p.30; FY2023 & FY2022 p.25; FY2021 p.20; FY2020 (own report) p.17."
    + "\n\nPRESENTATION NOTE: FY2025/FY2024's own statement splits interest income into investment securities/loans "
    "and advances/cash & cash equivalents lines and separately shows Net fees and commission expense and Net "
    "operating income subtotals; FY2023/FY2022's own statement does not carry the cash & cash equivalents interest "
    "split or the fees/operating-income subtotals (Other income sits directly under Net interest income); "
    "FY2021/FY2020's own statement is the simplest of the three, with no Other income figure at all in those years "
    "(reported as a dash - i.e. nil). Blank cells above reflect a line genuinely not carried in that year's own "
    "statement structure, not a missing figure. FY2020's own statement additionally has no 'Interest on loans and "
    "advances to customers' line at all (the loan book was still only £15k gross that period - not yet disbursing "
    "at scale - so all interest income that period is investment-securities interest); FY2020's P&L also prints "
    "Depreciation and Amortisation as one combined £(225)k line, but Note 14/Note 15 both confirm the entire "
    "charge is depreciation (amortisation had not yet started - the Bank's own Note 15 states 'Amortisation will "
    "commence once the asset is put into use'), so £(225)k is placed on the Depreciation row and Amortisation is "
    "shown as a genuine nil (0) for FY2020, not a missing figure. All six years' Loss/Profit for the year and "
    "Total comprehensive income/(loss) rows are the fully comparable rows across the whole window."
)
EQ_SOURCES = (
    statements_sources("Statement of Changes in Equity")
    + "\n\nPage references: FY2025 (chains FY2023-FY2025) p.32; FY2021 opening balance and FY2022-FY2023 movements "
    "p.27; FY2020 (own report, first-period roll-forward from incorporation) p.19."
    + "\n\nEvery year ties exactly to both the next year's opening balance and that year's own Balance Sheet Total "
    "equity - zero undocumented plug rows across all 6 years, independently cross-checked at 31 March 2023 (£8,637k) "
    "which appears identically as a closing balance in the FY2023 report and an opening balance in the FY2025 "
    "report's own equity roll-forward, and at 31 March 2020 (£18,638k) which appears identically as FY2020's own "
    "closing balance and as the FY2021 report's own comparative opening balance. FY2025's 'Capital reorganisation' "
    "row is a genuine reclassification between Share capital and Share premium with zero net effect on Total "
    "equity, reproduced as reported. FY2020 is the entity's true first period: its own roll-forward opens at "
    "£nil as at 19 December 2018 (incorporation), not a continuation of any prior column."
)
AQ_SOURCES = (
    statements_sources("Note 12/14, Loans and advances to customers, by IFRS 9 stage")
    + "\n\nPage references: FY2025 & FY2024 p.57; FY2023 & FY2022 p.50; FY2021 p.42; FY2020 (own report) Note 12, "
    "p.39."
    + "\n\nAll 6 years' Total Net Loans ties exactly to the Balance Sheet's own Loans and advances to customers "
    "line. FY2025 is the first year the loan book is split between Unsecured personal loans and Secured loans; "
    "FY2024-FY2020 are shown entirely under Unsecured personal loans as the Bank's own note structure carried no "
    "secured-loans category in those years (a genuine change in the loan book's composition and disclosure, not an "
    "omission). FY2023's own Stage 1/2/3 ECL allowances sum to £12,381k against the note's own reported subtotal "
    "of £12,380k - a £1k source rounding difference, reproduced as reported. Stage 3 (NPL) ratio and Stage 3 "
    "coverage ratio are derived from the note's own gross/ECL figures. FY2020 is the Bank's first disclosure of "
    "this note at all - the entire £15k gross loan book sat in Stage 1, not past due, and the Bank's own note "
    "states its calculated ECL provision 'has been determined as immaterial and accordingly no ECL related "
    "disclosures are provided', so no Stage 1/2/3 allowance split is shown for FY2020 (Total allowances taken as "
    "£0, i.e. net loans = gross loans, per that same statement) and Stage 3 coverage ratio is shown as not "
    "meaningful (no Stage 3 exposure existed that period)."
)


bw = BankWorkbook(bank_name="THIS BANK LIMITED", years=YEARS, year_label=YEAR_LABEL, header_color="5C2751")

BS_ROWS = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and cash equivalents", {"FY2025": 90674, "FY2024": 247547, "FY2023": 5264, "FY2022": 4159, "FY2021": 6720, "FY2020": 2066}),
    ("DATA", "Investment securities (UK gilts and Treasury Bills, held at amortised cost)", {"FY2024": 16800, "FY2023": 46059, "FY2022": 16543, "FY2021": 26700, "FY2020": 14987}),
    ("DATA", "Loans and advances to customers", {"FY2025": 277269, "FY2024": 83069, "FY2023": 55364, "FY2022": 57279, "FY2021": 8585, "FY2020": 15}),
    ("DATA", "Amounts owed by related party", {"FY2025": 313, "FY2024": 178, "FY2023": 994, "FY2022": 158, "FY2021": 145, "FY2020": 13}),
    ("DATA", "Other assets", {"FY2025": 403, "FY2024": 607, "FY2023": 408, "FY2022": 403, "FY2021": 429, "FY2020": 156}),
    ("DATA", "Property and equipment", {"FY2025": 565, "FY2024": 814, "FY2023": 967, "FY2022": 1121, "FY2021": 1294, "FY2020": 1444}),
    ("DATA", "Intangible assets", {"FY2025": 331, "FY2024": 359, "FY2023": 536, "FY2022": 2310, "FY2021": 2644, "FY2020": 2972}),
    ("DATA", "Deferred tax asset", {"FY2025": 0, "FY2024": 0, "FY2023": 0, "FY2022": 0, "FY2021": 0, "FY2020": 0}),
    ("TOTAL", "Total assets", {"FY2025": 369555, "FY2024": 349374, "FY2023": 109592, "FY2022": 81973, "FY2021": 46517, "FY2020": 21653}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Customer deposits", {"FY2025": 340963, "FY2024": 338301, "FY2023": 98503, "FY2022": 69516, "FY2021": 31955, "FY2020": 4}),
    ("DATA", "Amounts owed to related party", {"FY2025": 585, "FY2024": 334, "FY2023": 747, "FY2022": 375, "FY2021": 193, "FY2020": 257}),
    ("DATA", "Other liabilities", {"FY2025": 2410, "FY2024": 2126, "FY2023": 1705, "FY2022": 1760, "FY2021": 2052, "FY2020": 2754}),
    ("TOTAL", "Total liabilities", {"FY2025": 343958, "FY2024": 340761, "FY2023": 100955, "FY2022": 71651, "FY2021": 34200, "FY2020": 3015}),
    ("SECTION", "Equity", {}),
    ("DATA", "Share capital", {"FY2025": 422, "FY2024": 24930, "FY2023": 24930, "FY2022": 24930, "FY2021": 24930, "FY2020": 24930}),
    ("DATA", "Share premium", {"FY2025": 78104, "FY2024": 26996, "FY2023": 15996, "FY2022": 4996, "FY2021": 496, "FY2020": 496}),
    ("DATA", "Accumulated loss", {"FY2025": -52929, "FY2024": -43313, "FY2023": -32289, "FY2022": -19604, "FY2021": -13109, "FY2020": -6788}),
    ("TOTAL", "Total equity", {"FY2025": 25597, "FY2024": 8613, "FY2023": 8637, "FY2022": 10322, "FY2021": 12317, "FY2020": 18638}),
    ("TOTAL", "Total liabilities and equity", {"FY2025": 369554, "FY2024": 349374, "FY2023": 109592, "FY2022": 81973, "FY2021": 46517, "FY2020": 21653}),
]
bw.add_balance_sheet_sheet(
    title="THIS BANK LIMITED — Statement of Financial Position",
    subtitle="Own entity basis; £'000; years ended 31 March.",
    rows=BS_ROWS,
    sources_text=BS_SOURCES,
    first_col_width=62,
    source_height=440,
    unit_suffix=" (£'000)",
)

PL_ROWS = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest on investment securities", {"FY2025": 204, "FY2024": 2470, "FY2023": 533, "FY2022": 18, "FY2021": 7, "FY2020": 38}),
    ("DATA", "Interest on loans and advances to customers", {"FY2025": 18032, "FY2024": 7036, "FY2023": 8082, "FY2022": 3619, "FY2021": 224}),
    ("DATA", "Interest on cash & cash equivalents", {"FY2025": 6793, "FY2024": 4016}),
    ("DATA", "Interest payable and similar charges", {"FY2025": -16599, "FY2024": -8251, "FY2023": -1790, "FY2022": -585, "FY2021": -99, "FY2020": -6}),
    ("TOTAL", "Net interest income", {"FY2025": 8430, "FY2024": 5271, "FY2023": 6825, "FY2022": 3052, "FY2021": 132, "FY2020": 32}),
    ("DATA", "Net fees and commission expense", {"FY2025": 381, "FY2024": -147}),
    ("TOTAL", "Net operating income", {"FY2025": 8811, "FY2024": 5124}),
    ("DATA", "Other income", {"FY2025": 740, "FY2024": 428, "FY2023": 974, "FY2022": 115}),
    ("SECTION", "Operating expenses", {}),
    ("DATA", "Administrative expenses", {"FY2025": -14212, "FY2024": -10705, "FY2023": -8651, "FY2022": -6331, "FY2021": -5326, "FY2020": -6595}),
    ("DATA", "Impairment losses on financial instruments", {"FY2025": -5197, "FY2024": -3452, "FY2023": -10820, "FY2022": -2438, "FY2021": -448, "FY2020": 0}),
    ("DATA", "Depreciation", {"FY2025": -352, "FY2024": -178, "FY2023": -173, "FY2022": -182, "FY2021": -195, "FY2020": -225}),
    ("DATA", "Amortisation", {"FY2025": -101, "FY2024": -241, "FY2023": -480, "FY2022": -631, "FY2021": -482, "FY2020": 0}),
    ("DATA", "Other expenses", {"FY2025": 695, "FY2024": -2000, "FY2023": -360, "FY2022": -80, "FY2021": -2}),
    # Not itself a printed AR subtotal - the sum of Administrative expenses +
    # Depreciation + Amortisation + Other expenses above. Excludes Impairment
    # losses on financial instruments per standard cost-to-income convention
    # (operating costs only, not credit risk).
    ("TOTAL", "Total operating expenses (sum of Administrative expenses + Depreciation + Amortisation + Other expenses - excludes impairment losses on financial instruments)",
     {"FY2025": -13970, "FY2024": -13124, "FY2023": -9664, "FY2022": -7224, "FY2021": -6005, "FY2020": -6820}),
    ("TOTAL", "Loss before tax", {"FY2025": -9616, "FY2024": -11024, "FY2023": -12685, "FY2022": -6495, "FY2021": -6321, "FY2020": -6788}),
    ("DATA", "Income tax expense", {"FY2025": 0, "FY2024": 0, "FY2023": 0, "FY2022": 0, "FY2021": 0, "FY2020": 0}),
    ("TOTAL", "Loss for the year", {"FY2025": -9616, "FY2024": -11024, "FY2023": -12685, "FY2022": -6495, "FY2021": -6321, "FY2020": -6788}),
    ("TOTAL", "Total comprehensive loss for the year, net of tax", {"FY2025": -9616, "FY2024": -11024, "FY2023": -12685, "FY2022": -6495, "FY2021": -6321, "FY2020": -6788}),
]
bw.add_income_statement_sheet(
    title="THIS BANK LIMITED — Statement of Profit or Loss and Other Comprehensive Income",
    subtitle="Own entity basis; £'000; years ended 31 March.",
    rows=PL_ROWS,
    sources_text=PL_SOURCES,
    first_col_width=62,
    source_height=280,
    unit_suffix=" (£'000)",
)

EQ_ROWS = [
    ("TOTAL", "Balance as at 19 December 2018 (incorporation)", (0, 0, 0, 0)),
    ("TOTAL", "Loss for the period (FY2020)", (None, None, -6788, -6788)),
    ("DATA", "Issue of shares (FY2020)", (24930, 496, None, 25426)),
    ("TOTAL", "Balance as at 31 March 2020", (24930, 496, -6788, 18638)),
    ("TOTAL", "Loss for the year (FY2021)", (None, None, -6321, -6321)),
    ("TOTAL", "Balance as at 31 March 2021", (24930, 496, -13109, 12317)),
    ("TOTAL", "Loss for the year (FY2022)", (None, None, -6495, -6495)),
    ("DATA", "Issue of shares (FY2022)", (None, 4500, None, 4500)),
    ("TOTAL", "Balance as at 31 March 2022", (24930, 4996, -19604, 10322)),
    ("TOTAL", "Loss for the year (FY2023)", (None, None, -12685, -12685)),
    ("DATA", "Issue of shares (FY2023)", (None, 11000, None, 11000)),
    ("TOTAL", "Balance as at 31 March 2023", (24930, 15996, -32289, 8637)),
    ("TOTAL", "Loss for the year (FY2024)", (None, None, -11024, -11024)),
    ("DATA", "Issue of shares (FY2024)", (None, 11000, None, 11000)),
    ("TOTAL", "Balance as at 31 March 2024", (24930, 26996, -43313, 8613)),
    ("TOTAL", "Loss for the year (FY2025)", (None, None, -9616, -9616)),
    ("DATA", "Capital reorganisation (FY2025)", (-33577, 33577, None, 0)),
    ("DATA", "Issue of shares (FY2025)", (9069, 17531, None, 26600)),
    ("TOTAL", "Balance as at 31 March 2025", (422, 78104, -52929, 25597)),
]
bw.add_equity_changes_sheet(
    title="THIS BANK LIMITED — Statement of Changes in Equity",
    subtitle="Own entity basis; £'000; years ended 31 March, read chronologically.",
    headers=["Share capital", "Share premium", "Accumulated loss", "Total equity"],
    rows=EQ_ROWS,
    sources_text=EQ_SOURCES,
    first_col_width=46,
    source_height=230,
)

# The source statements provide complete annual activity totals and opening/
# closing cash balances. The totals are retained exactly as reported; detailed
# OCR line-item transcription is avoided where the scans are ambiguous.
cash_rows = [
    ("SECTION", "Operating activities", {}),
    ("TOTAL", "Net cash from/(used in) operating activities", {"FY2025": -200221, "FY2024": 199773, "FY2023": 19008, "FY2022": -16676, "FY2021": 16721, "FY2020": -3562}),
    ("SECTION", "Investing activities", {}),
    ("TOTAL", "Net cash from/(used in) investing activities", {"FY2025": 16885, "FY2024": 31630, "FY2023": -28783, "FY2022": 9735, "FY2021": -11912, "FY2020": -19590}),
    ("SECTION", "Financing activities", {}),
    ("TOTAL", "Net cash from/(used in) financing activities", {"FY2025": 26463, "FY2024": 10880, "FY2023": 10880, "FY2022": 4380, "FY2021": -155, "FY2020": 25218}),
    ("TOTAL", "Net increase/(decrease) in cash and cash equivalents", {"FY2025": -156873, "FY2024": 242283, "FY2023": 1105, "FY2022": -2561, "FY2021": 4654, "FY2020": 2066}),
    ("DATA", "Cash and cash equivalents at beginning of year", {"FY2025": 247547, "FY2024": 5264, "FY2023": 4159, "FY2022": 6720, "FY2021": 2066, "FY2020": 0}),
    ("TOTAL", "Cash and cash equivalents at end of year", {"FY2025": 90674, "FY2024": 247547, "FY2023": 5264, "FY2022": 4159, "FY2021": 6720, "FY2020": 2066}),
]
bw.add_cash_flow_sheet(
    title="THIS BANK LIMITED — Statement of Cash Flows",
    subtitle="Own entity basis; £'000; years ended 31 March; activity totals transcribed from the filed annual accounts.",
    rows=cash_rows,
    sources_text=account_sources() + "\nReconciliation: each year's net change equals operating + investing + financing totals; closing cash equals opening cash + net change.",
    first_col_width=68,
    source_height=290,
    unit_suffix=" (£'000)",
)


AQ_ROWS = [
    ("SECTION", "Gross loans and advances by IFRS 9 stage", {}),
    ("DATA", "Stage 1 (12-month ECL)", {"FY2025": 244224, "FY2024": 81546, "FY2023": 40573, "FY2022": 54865, "FY2021": 8208, "FY2020": 15}),
    ("DATA", "Stage 2 (lifetime ECL, not credit-impaired)", {"FY2025": 18452, "FY2024": 60, "FY2023": 17958, "FY2022": 3373, "FY2021": 751, "FY2020": 0}),
    ("DATA", "Stage 3 (credit-impaired)", {"FY2025": 19618, "FY2024": 15306, "FY2023": 9213, "FY2022": 1771, "FY2021": 69, "FY2020": 0}),
    ("DATA", "POCI loans", {"FY2025": 676}),
    ("TOTAL", "Total gross loans and advances", {"FY2025": 282970, "FY2024": 96912, "FY2023": 67744, "FY2022": 60009, "FY2021": 9028, "FY2020": 15}),
    ("SECTION", "Allowances for expected credit losses (ECL)", {}),
    ("DATA", "Stage 1 allowance", {"FY2025": -2693, "FY2024": -721, "FY2023": -2278, "FY2022": -728, "FY2021": -261}),
    ("DATA", "Stage 2 allowance", {"FY2025": -1629, "FY2024": -3, "FY2023": -1944, "FY2022": -533, "FY2021": -120}),
    ("DATA", "Stage 3 allowance", {"FY2025": -1494, "FY2024": -13119, "FY2023": -8159, "FY2022": -1469, "FY2021": -62}),
    ("DATA", "POCI loans allowance", {"FY2025": 115}),
    ("TOTAL", "Total allowances for ECLs", {"FY2025": -5701, "FY2024": -13843, "FY2023": -12380, "FY2022": -2730, "FY2021": -443, "FY2020": 0}),
    ("TOTAL", "Total net loans and advances", {"FY2025": 277269, "FY2024": 83069, "FY2023": 55364, "FY2022": 57279, "FY2021": 8585, "FY2020": 15}),
    ("SECTION", "Asset quality ratios", {}),
    ("DATA", "Stage 3 (NPL) ratio, gross", {"FY2025": "6.93%", "FY2024": "15.79%", "FY2023": "13.60%", "FY2022": "2.95%", "FY2021": "0.76%", "FY2020": "0.00%"}),
    ("DATA", "Stage 3 coverage ratio (Stage 3 ECL / Stage 3 gross)", {"FY2025": "7.61%", "FY2024": "85.71%", "FY2023": "88.56%", "FY2022": "82.95%", "FY2021": "89.86%", "FY2020": "n/m (no Stage 3 exposure)"}),
]
bw.add_asset_quality_sheet(
    title="THIS BANK LIMITED — Asset Quality",
    subtitle="Own entity basis, loan book by IFRS 9 stage; £'000; years ended 31 March.",
    rows=AQ_ROWS,
    sources_text=AQ_SOURCES,
    first_col_width=58,
    source_height=250,
    unit_suffix=" (£'000)",
)


def metric(name, unit, rows, note=None):
    bw.add_metric_sheet(name, unit, rows, p3_sources(), note=note, first_col_width=58, source_height=250)


CET1 = {"FY2025": 25927, "FY2024": 8254, "FY2023": 8101, "FY2022": 8012, "FY2021": 11965, "FY2020": 15666}
CET1_RATIO = {"FY2025": "16.44%", "FY2024": "19.20%", "FY2023": "16.28%", "FY2022": "15.90%", "FY2021": "66.50%", "FY2020": "Not publicly disclosed"}
LCR = {"FY2025": "554%", "FY2024": "4840%", "FY2023": "7758%", "FY2022": "Not publicly disclosed", "FY2021": "Not publicly disclosed", "FY2020": "Not publicly disclosed"}
DISCLOSURE_NOTE = (
    "The accounts provide entity-level regulatory capital data but do not publish a complete standalone Pillar 3 "
    "template. FY2023 values use the FY2024 report's comparative KPI/capital figures. FY2021 values use the FY2022 "
    "report's 2021 comparative regulatory-capital column. Ratios are as reported; no RWA, leverage, NSFR, or MREL "
    "values are derived from them. Where narrative KPI percentages differ from the regulatory-capital table, the "
    "regulatory-capital table is used: FY2025 narrative CET1 ratio 16.58% versus table 16.44%, and FY2025's "
    "comparative FY2024 presentation differs from the FY2024 own-year table. FY2020's own report (its first, "
    "covering the 16-month period to 31 March 2020) gives CET1/Total Regulatory Capital of £15,666k in its own "
    "Note 27 regulatory-capital table, but no CET1/Tier1/Total Capital ratio (%) was found anywhere - neither in "
    "FY2020's own report nor in the FY2021 report's later FY2020 comparative column - so the FY2020 ratio cells "
    "are genuinely not publicly disclosed, not merely uncollected."
)

metric("CET1 Capital", "£'000", [("Common Equity Tier 1 (CET1) capital", CET1)], DISCLOSURE_NOTE)
metric("CET1 Ratio", "% of RWA", [("Common Equity Tier 1 ratio", CET1_RATIO)], DISCLOSURE_NOTE)
metric("Tier 1 Capital", "£'000", [("Tier 1 capital", CET1)], "No AT1 capital is reported; Tier 1 equals CET1 in the reviewed accounts.\n" + DISCLOSURE_NOTE)
metric("Tier 1 Ratio", "% of RWA", [("Tier 1 ratio", CET1_RATIO)], DISCLOSURE_NOTE)
metric("Total Capital", "£'000", [("Total regulatory capital", CET1)], "No Tier 2 capital is reported; total regulatory capital equals CET1 in the reviewed accounts.\n" + DISCLOSURE_NOTE)
metric("Total Capital Ratio", "% of RWA", [("Total capital ratio", CET1_RATIO)], DISCLOSURE_NOTE)
bw.add_not_disclosed_metric_sheets(
    ["Total RWAs"],
    p3_sources(),
    per_note={"Total RWAs": "No numeric standalone value was identified in the FY2020-FY2025 annual accounts reviewed; no value has been derived."},
)
bw.add_not_disclosed_metric_sheets(
    ["RWA Breakdown"],
    p3_sources(),
    per_note={"RWA Breakdown": "No RWA category breakdown (UK OV1 template or equivalent) was identified in the FY2020-FY2025 annual accounts reviewed; the accounts do not publish a standalone Pillar 3 document and Total RWAs itself is undisclosed."},
)
bw.add_not_disclosed_metric_sheets(
    ["Leverage Ratio"],
    p3_sources(),
    per_note={"Leverage Ratio": "No numeric standalone value was identified in the FY2020-FY2025 annual accounts reviewed; no value has been derived."},
)
metric("LCR", "%", [("Liquidity coverage ratio", LCR)], "FY2022, FY2021 and FY2020 accounts disclose HQLA amounts and describe LCR as above minimum (FY2020's own report states >1,000% and HQLA of £17.1m), but do not provide a numeric LCR ratio.\n" + DISCLOSURE_NOTE)
bw.add_not_disclosed_metric_sheets(
    ["NSFR", "MREL Ratio"],
    p3_sources(),
    per_note={name: "No numeric standalone value was identified in the FY2020-FY2025 annual accounts reviewed; no value has been derived." for name in ["NSFR", "MREL Ratio"]},
)

bw.add_overview_sheet(
    cash_flow_totals=[
        ("Net cash from/(used in) operating activities", {"FY2025": -200221, "FY2024": 199773, "FY2023": 19008, "FY2022": -16676, "FY2021": 16721, "FY2020": -3562}),
        ("Net cash from/(used in) investing activities", {"FY2025": 16885, "FY2024": 31630, "FY2023": -28783, "FY2022": 9735, "FY2021": -11912, "FY2020": -19590}),
        ("Net cash from/(used in) financing activities", {"FY2025": 26463, "FY2024": 10880, "FY2023": 10880, "FY2022": 4380, "FY2021": -155, "FY2020": 25218}),
        ("Cash and cash equivalents at end of year", {"FY2025": 90674, "FY2024": 247547, "FY2023": 5264, "FY2022": 4159, "FY2021": 6720, "FY2020": 2066}),
    ],
    cash_flow_unit="£'000",
    balance_sheet_totals=[
        ("Total assets", {"FY2025": 369555, "FY2024": 349374, "FY2023": 109592, "FY2022": 81973, "FY2021": 46517, "FY2020": 21653}),
        ("Loans and advances to customers", {"FY2025": 277269, "FY2024": 83069, "FY2023": 55364, "FY2022": 57279, "FY2021": 8585, "FY2020": 15}),
        ("Customer deposits", {"FY2025": 340963, "FY2024": 338301, "FY2023": 98503, "FY2022": 69516, "FY2021": 31955, "FY2020": 4}),
        ("Total equity", {"FY2025": 25597, "FY2024": 8613, "FY2023": 8637, "FY2022": 10322, "FY2021": 12317, "FY2020": 18638}),
    ],
    balance_sheet_unit="£'000",
    income_statement_totals=[
        ("Net interest income", {"FY2025": 8430, "FY2024": 5271, "FY2023": 6825, "FY2022": 3052, "FY2021": 132, "FY2020": 32}),
        ("Administrative expenses", {"FY2025": -14212, "FY2024": -10705, "FY2023": -8651, "FY2022": -6331, "FY2021": -5326, "FY2020": -6595}),
        ("Loss for the year", {"FY2025": -9616, "FY2024": -11024, "FY2023": -12685, "FY2022": -6495, "FY2021": -6321, "FY2020": -6788}),
    ],
    income_statement_unit="£'000",
    equity_changes_totals=[
        ("Opening equity", {"FY2025": 8613, "FY2024": 8637, "FY2023": 10322, "FY2022": 12317, "FY2021": 18638, "FY2020": 0}),
        ("Total comprehensive loss for the year", {"FY2025": -9616, "FY2024": -11024, "FY2023": -12685, "FY2022": -6495, "FY2021": -6321, "FY2020": -6788}),
        ("Other equity movements, net", {"FY2025": 26600, "FY2024": 11000, "FY2023": 11000, "FY2022": 4500, "FY2021": 0, "FY2020": 25426}),
        ("Closing equity", {"FY2025": 25597, "FY2024": 8613, "FY2023": 8637, "FY2022": 10322, "FY2021": 12317, "FY2020": 18638}),
    ],
    equity_changes_unit="£'000",
    ratios=[("CET1 Ratio", CET1_RATIO), ("Tier 1 Ratio", CET1_RATIO), ("Total Capital Ratio", CET1_RATIO), ("LCR", LCR)],
    note="Full annual accounts build for the entity formerly named JN Bank UK Ltd. FY2020 is the entity's confirmed historical floor (first filed accounts, a 16-month period from incorporation 19 Dec 2018 to 31 March 2020) - no FY2018/FY2019 period exists for this bank. See detail sheets for source basis and disclosure gaps.",
)

bw.save("/Users/armaan/code/katalysis/banks/THIS BANK FINANCIALS.xlsx")
