import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook


YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021", "FY2020", "FY2019", "FY2018", "FY2017", "FY2016", "FY2015"]

AR_URLS = {
    "FY2025": "https://oaknorth.co.uk/wp-content/uploads/2026/03/Annual_Report_2025.pdf",
    "FY2024": "https://oaknorth.co.uk/wp-content/uploads/2025/03/Annual_Report_2024.pdf",
    "FY2023": "https://oaknorth.co.uk/wp-content/uploads/2024/03/OakNorth_Annual_Report_2023.pdf",
    "FY2022": "https://oaknorth.co.uk/wp-content/uploads/2023/03/OakNorth-Annual-Report-2022.pdf",
    "FY2021": "https://www.oaknorth.co.uk/wp-content/uploads/2022/03/OakNorth-Bank-Annual-Report-2021.pdf",
    "FY2020": "https://oaknorth.co.uk/wp-content/uploads/2022/01/AnnualReport2020.pdf",
    "FY2019": "https://oaknorth.co.uk/wp-content/uploads/2022/02/ONB-Annual-Report-2019-1.pdf",
    "FY2018": "https://oaknorth.co.uk/wp-content/uploads/2022/02/ONB-Annual-Report-2018-1.pdf",
    "FY2017": "https://find-and-update.company-information.service.gov.uk/company/08595042/filing-history/MzIwMzQzMDgzMmFkaXF6a2N4/document?format=pdf&download=0",
    "FY2016": "https://find-and-update.company-information.service.gov.uk/company/08595042/filing-history/MzE3NzMxODY4MWFkaXF6a2N4/document?format=pdf&download=0",
    "FY2015": "https://find-and-update.company-information.service.gov.uk/company/08595042/filing-history/MzE1MDI0NzI3NWFkaXF6a2N4/document?format=pdf&download=0",
}
P3_URLS = {
    "FY2025": "https://oaknorth.co.uk/wp-content/uploads/2026/04/Pillar-3-Disclosures-OakNorth-Bank-Plc-2025-1.pdf",
    "FY2024": "https://oaknorth.co.uk/wp-content/uploads/2025/05/Pillar-3-Disclosures-OakNorth-Bank-Plc-2024.pdf",
    "FY2023": "https://oaknorth.co.uk/wp-content/uploads/2024/05/Pillar-3-Disclosure-OakNorth-Bank-Plc-2023.pdf",
    "FY2022": "https://oaknorth.co.uk/wp-content/uploads/2023/05/Pillar-3-disclosures-2022_Final.pdf",
    "FY2021": "https://oaknorth.co.uk/wp-content/uploads/2022/07/OakNorth_Pillar-3_2021.pdf",
    "FY2020": "https://oaknorth.co.uk/wp-content/uploads/2022/02/2020-Pillar-3-Capital-Requirement-and-Remuneration-Policy-disclosures-1.pdf",
    "FY2019": "https://oaknorth.co.uk/wp-content/uploads/2022/02/2019-Pillar-3-Capital-Requirement-and-Remuneration-Policy-disclosures.pdf",
    "FY2018": "https://oaknorth.co.uk/wp-content/uploads/2022/02/2018-Pillar-3-Capital-Requirement-disclosures.pdf",
    "FY2017": "https://oaknorth.co.uk/wp-content/uploads/2022/02/2017-Pillar-3-Capital-Requirement-disclosures.pdf",
    "FY2016": "https://oaknorth.co.uk/wp-content/uploads/2022/02/2016-Pillar-3-Capital-Requirement-disclosures.pdf",
    "FY2015": "https://oaknorth.co.uk/wp-content/uploads/2022/02/2015-Pillar-3-Capital-Requirement-Disclosures.pdf",
}


def cash_flow_sources():
    return (
        "Sources — OakNorth Bank plc cash flows, £'000. FY2025: OakNorth Bank Plc Annual Report 2025, "
        f"pp.102-103 (Statement of cash flows) — {AR_URLS['FY2025']}\n"
        f"FY2024: Annual Report 2024, pp.94-95 — {AR_URLS['FY2024']}\n"
        f"FY2023: Annual Report 2023, pp.87-88 — {AR_URLS['FY2023']}\n"
        f"FY2022: Annual Report 2022, pp.106-107 — {AR_URLS['FY2022']}\n"
        f"FY2021: Annual Report 2021, p.87 — {AR_URLS['FY2021']}\n"
        f"FY2020: Annual Report 2020, Cash flow statement p.55 — {AR_URLS['FY2020']}\n"
        f"FY2019: Annual Report 2019, Cash flow statement p.53 — {AR_URLS['FY2019']}\n"
        f"FY2018: Annual Report 2018, Cash flow statement p.44 — {AR_URLS['FY2018']}\n"
        f"FY2017: OakNorth Bank Limited full accounts made up to 31 December 2017, Cash flow statement p.38 — "
        f"{AR_URLS['FY2017']}\n"
        f"FY2016: OakNorth Bank Limited full accounts made up to 31 December 2016, Cash flow statement p.30 — "
        f"{AR_URLS['FY2016']}\n"
        f"FY2015: OakNorth Bank Limited full accounts made up to 31 December 2015, Cash flow statement p.22 — "
        f"{AR_URLS['FY2015']}\n"
        "The 2022–2025 reports present both Bank Group and standalone Bank columns; this sheet uses the Bank Group "
        "column for those years. The 2015–2021 reports predate the ASK Partners consolidation and present OakNorth "
        "Bank plc/Limited standalone figures. Blank cells mean the line was not separately disclosed under that "
        "year's presentation; they are not zeros. FY2015-FY2020 use each year's own, differently-structured, "
        "presentation (e.g. FY2015-FY2017 itemise 'Increase in receivables'/'Increase in payables' separately, "
        "where FY2018-FY2020 fold these into a single 'Net change in other assets/liabilities' line, and "
        "FY2015-FY2020 combine PP&E and intangible asset purchases into one line where FY2021+ split them) - "
        "rows unique to a given year's own presentation are left blank for other years rather than forced onto "
        "a common line. DATA QUALITY NOTE: the FY2020 Annual Report's own cash flow statement (p.55) labels its "
        "closing reconciliation row 'Net increase in cash and cash equivalents' with a positive value of "
        "£70,342k, but the stated opening (£551,333k) and closing (£480,991k) balances on the same page - which "
        "both independently tie to the adjacent years' own statements - imply a £70,342k DECREASE, not increase; "
        "this appears to be a sign/label error in OakNorth's own published FY2020 statement. This sheet shows "
        "the movement as -70,342 (a decrease) to reconcile the beginning and ending balances as filed, rather "
        "than reproducing the source's positive label. DATA QUALITY NOTE: FY2017's own accounts (as originally "
        "filed) show cash and cash equivalents at end of year of £153,702k, but the Annual Report 2018's FY2017 "
        "comparative opening balance shows £153,738k (a £36k difference) - this ties to the same accrued-interest "
        "reclassification between customer deposits and other liabilities noted in the balance sheet basis note "
        "above, applied when FY2018 restated its FY2017 comparative; this sheet uses each year's own, "
        "contemporaneously-filed closing figure rather than a later restatement, so the FY2017 TOTAL (153,702) "
        "and the FY2018 DATA opening-balance figure (153,738) are both correct on their own terms and do not "
        "indicate a transcription error. DATA QUALITY NOTE: FY2015's own accounts present 'Net cash flows "
        "generated from/(used in) operating activities' as the sum of only the disclosed adjustment lines "
        "(depreciation, other non-cash items, and movements in receivables/payables/loans/deposits), which does "
        "not itself include the period's loss before tax (-2,287) as a separate reconciling item the way later "
        "years' statements do; this sheet transcribes the FY2015 total (-4,061) exactly as filed rather than "
        "re-deriving it, since it is OakNorth's first-ever set of statutory accounts and this appears to be an "
        "idiosyncrasy of that year's own presentation rather than an error."
    )


def p3_sources():
    return (
        "Sources — OakNorth Bank Pillar 3 disclosures, £'000 unless percentages are shown. FY2025: UK KM1 p.14 "
        f"and OV1 p.15 — {P3_URLS['FY2025']}\n"
        f"FY2024: UK KM1 pp.16-17 — {P3_URLS['FY2024']}\n"
        f"FY2023: UK KM1 p.6 and capital adequacy p.10 — {P3_URLS['FY2023']}\n"
        f"FY2022: capital metrics pp.19-23 — {P3_URLS['FY2022']}\n"
        f"FY2021: regulatory capital and leverage pp.11-15 — {P3_URLS['FY2021']}\n"
        f"FY2020: capital resources/adequacy/leverage pp.18-22, liquidity risk p.38 — {P3_URLS['FY2020']}\n"
        f"FY2019: capital resources/adequacy/leverage pp.20-23, liquidity risk p.37 — {P3_URLS['FY2019']}\n"
        f"FY2018: capital resources/adequacy/leverage pp.17-21, liquidity risk p.34 — {P3_URLS['FY2018']}\n"
        f"FY2017: capital resources/adequacy/leverage pp.17-19, liquidity risk p.30 — {P3_URLS['FY2017']}\n"
        f"FY2016: capital resources/adequacy/leverage pp.16-18, liquidity risk p.27 — {P3_URLS['FY2016']}\n"
        f"FY2015: capital resources/adequacy/leverage pp.14-16 — {P3_URLS['FY2015']}\n"
        "The 2025 disclosure states that the prudential disclosures are on a consolidated Bank Group basis, while "
        "the 2022–2024 reports describe the relevant regulatory templates as solo/Bank basis. The 2015–2021 "
        "figures are all standalone Bank figures (each year's own report states the disclosures are prepared for "
        "the stand-alone entity, with no consolidated entities before FY2022)."
    )


bw = BankWorkbook("OakNorth Bank plc", YEARS, header_color="6B8E23")

STATEMENTS_SOURCES = (
    "Sources - OakNorth Bank plc consolidated financial statements, £'000, Bank Group basis (Bank standalone "
    "for FY2015-FY2021 - see basis note below):\n"
    f"FY2025/FY2024: Annual Report 2025, Consolidated Statement of Profit or Loss p.94, Consolidated Statement "
    f"of Comprehensive Income p.95, Consolidated Balance Sheet pp.96-97, Consolidated Statement of Changes in "
    f"Equity p.100 - {AR_URLS['FY2025']}\n"
    f"FY2023: Annual Report 2024, Consolidated Statement of Profit & Loss p.86, Consolidated Statement of "
    f"Comprehensive Income p.87, Consolidated Balance Sheet pp.88-89, Consolidated Statement of Changes in "
    f"Equity p.92 (FY2023 own-year column) - {AR_URLS['FY2024']}\n"
    f"FY2022: Annual Report 2023, Consolidated Statement of Profit & Loss and Comprehensive Income pp.79-80, "
    f"Consolidated Balance Sheet pp.81-82, Consolidated Statement of Changes in Equity p.85 (FY2022 own-year "
    f"column) - {AR_URLS['FY2023']}\n"
    f"FY2021: Annual Report 2022, Consolidated Statement of Profit and Loss and Comprehensive Income p.99, "
    f"Consolidated Balance Sheet pp.100-101, Consolidated Statement of Changes in Equity p.104 (2021 IFRS "
    f"Restated column and 1 Jan 2021 opening) - {AR_URLS['FY2022']}\n"
    f"FY2020: Annual Report 2020, Profit and loss statement p.51, Statement of comprehensive income p.52, "
    f"Balance sheet p.53, Statement of changes in equity p.54 - {AR_URLS['FY2020']}\n"
    f"FY2019: Annual Report 2019, Profit and loss statement p.49, Statement of comprehensive income p.50, "
    f"Balance sheet p.51, Statement of changes in equity p.52 - {AR_URLS['FY2019']}\n"
    f"FY2018: Annual Report 2018, Profit and loss statement p.40, Statement of comprehensive income p.41, "
    f"Balance sheet p.42, Statement of changes in equity p.43 - {AR_URLS['FY2018']}\n"
    f"FY2017: OakNorth Bank Limited full accounts made up to 31 December 2017 (filed with Companies House "
    f"25 April 2018), Balance sheet p.36, Statement of comprehensive income p.35 - {AR_URLS['FY2017']} "
    f"(P&L breakdown corroborated from the FY2017 comparative column of the Annual Report 2018 - "
    f"{AR_URLS['FY2018']})\n"
    f"FY2016: OakNorth Bank Limited full accounts made up to 31 December 2016 (filed with Companies House "
    f"7 June 2017), Profit and loss statement p.26, Statement of comprehensive income p.27, Balance sheet p.28, "
    f"Statement of changes in Equity p.29 - {AR_URLS['FY2016']}\n"
    f"FY2015: OakNorth Bank Limited full accounts made up to 31 December 2015 (filed with Companies House "
    f"7 June 2016), Profit and loss account p.18, Statement of Comprehensive Income p.19, Balance sheet p.20, "
    f"Statement of changes in equity p.21 - {AR_URLS['FY2015']}\n\n"
    "BASIS NOTE: OakNorth Bank plc transitioned from FRS 102 to UK-adopted IAS (IFRS) with effect from the year "
    "ended 31 December 2022 (Annual Report 2022, Note 1.6). FY2021 figures shown throughout the Balance Sheet, "
    "Profit & Loss and Statement of Changes in Equity sheets are the Bank's own officially IFRS-restated FY2021 "
    "comparatives (as republished in the Annual Report 2022), not the originally-reported FRS 102 figures from "
    "the Annual Report 2021 - this is done for comparability with FY2022-FY2025, all of which are prepared under "
    "IFRS. A genuine £470k IFRS transition adjustment (net of tax, to retained earnings) was applied between the "
    "31 December 2021 closing balance and the 1 January 2022 opening balance and is shown as its own explicit "
    "row on the Statement of Changes in Equity sheet, not absorbed into any other line. OakNorth's subsidiary "
    "A.S.K Partners Limited was first consolidated during FY2022 (goodwill and non-controlling interests first "
    "appear that year); FY2015-FY2021's figures are therefore Bank standalone (identical to 'Bank Group' where "
    "that basis is separately referenced). Balance Sheet/P&L/Equity are Bank Group (consolidated) basis from "
    "FY2022 and Bank standalone basis for FY2015-FY2021; the Asset Quality sheet is Bank-standalone (entity-level) "
    "basis throughout - see that sheet's own note for the resulting basis difference against these three sheets' "
    "Bank Group loans and advances to customers figure from FY2022 onward.\n\n"
    "HISTORICAL-DEPTH NOTE (FY2015-FY2020, added under HD-021): OakNorth Bank Limited received its full UK "
    "banking licence from the PRA/FCA on 6 March 2015 and its Companies House filing history confirms FY2015 "
    "(the year ended 31 December 2015) is the earliest full annual-accounts period after authorisation - there "
    "is no earlier bank-trading year to extend back to (a prior 'restated period ended 31 December 2014' exists "
    "in the FY2015 accounts as a comparative column only, covering the pre-authorisation shell-company period "
    "since incorporation on 3 July 2013, and is not itself presented as a full trading year). FY2015 is a "
    "complete 12-month statutory accounting period, but the Bank only exited the PRA's regulatory 'mobilisation' "
    "stage and began deposit-taking on 28 August 2015 (Pillar 3 disclosures 2015, section 1.1) - so the small "
    "FY2015 income figures (e.g. interest income of £198k) reflect roughly the final four months of live "
    "banking activity within an otherwise-full calendar year, not a truncated reporting period. The company "
    "re-registered from a private company (OakNorth Bank Limited) to a public company (OakNorth Bank plc) "
    "effective April 2018; FY2015-FY2017 statements are therefore headed 'OakNorth Bank Limited'. OakNorth "
    "adopted IFRS 9 'Financial Instruments' (replacing IAS 39) with effect from 1 January 2019, without "
    "restating FY2018 comparatives (Annual Report 2019, Note 1.1) - so the FY2018 provision line is an IAS 39 "
    "'incurred but not reported' (IBNR) allowance charge, not an IFRS 9 expected-credit-loss charge; FY2019 "
    "onward are on an IFRS 9 basis. No Basel II-era terminology gap arises anywhere in FY2015-FY2020: OakNorth's "
    "entire trading history postdates the EU Capital Requirements Directive IV (CRD IV, in force from 1 January "
    "2014), so the CET1/Tier 1/Total Capital vocabulary used throughout this workbook was already the Bank's "
    "own from its first Pillar 3 disclosure (year ended 31 December 2015)."
)

# ---------------------------------------------------------------
# Balance Sheet - equity reconciliation ladder step 1: built first so each
# year's own Total equity is the independent check value for the equity
# sheet below. All 5 years tie exactly to the equity statement's own
# opening/closing balances and to Total assets = Total liabilities + equity.
# ---------------------------------------------------------------
bs_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and balances at central bank", {"FY2025": 2184464, "FY2024": 2689013, "FY2023": 1637314, "FY2022": 1235711, "FY2021": 446374, "FY2020": 469459, "FY2019": 540035, "FY2018": 356881, "FY2017": 148340, "FY2016": 51175}),
    ("DATA", "Loans and advances to banks", {"FY2025": 96776, "FY2024": 80632, "FY2023": 38474, "FY2022": 42127, "FY2021": 30019, "FY2020": 11532, "FY2019": 11298, "FY2018": 6394, "FY2017": 5362, "FY2016": 9161, "FY2015": 21571}),
    ("DATA", "Loans and advances to customers", {"FY2025": 4889874, "FY2024": 4393100, "FY2023": 3817344, "FY2022": 3127950, "FY2021": 2886305, "FY2020": 2492249, "FY2019": 2062985, "FY2018": 1297937, "FY2017": 604937, "FY2016": 225508, "FY2015": 14906}),
    ("DATA", "Total investment securities / Debt securities", {"FY2025": 599436, "FY2024": 331238, "FY2023": 237660, "FY2022": 204005, "FY2021": 191849, "FY2020": 131053, "FY2019": 105337, "FY2018": 104420, "FY2017": 2115, "FY2016": 500, "FY2015": 53238}),
    ("DATA", "Investment securities - Long-term UK Gilts & Treasury bills, at amortised cost", {"FY2025": 299979}),
    ("DATA", "Investment securities - Senior tranches in CLOs, at amortised cost", {"FY2025": 111965}),
    ("DATA", "Investment securities - Short-term UK Gilts & Treasury bills, at FVOCI", {"FY2025": 0, "FY2024": 207231, "FY2023": 205872, "FY2022": 204005, "FY2021": 191849, "FY2020": 131053}),
    ("DATA", "Investment securities - Money market funds, at FVOCI", {"FY2025": 187492, "FY2024": 124007, "FY2023": 31788}),
    ("DATA", "Derivative assets held for risk management", {"FY2025": 33742, "FY2024": 2809, "FY2023": 5765, "FY2022": 0}),
    ("DATA", "Goodwill", {"FY2025": 11647, "FY2024": 11647, "FY2023": 11647, "FY2022": 11647}),
    ("DATA", "Intangible assets", {"FY2025": 14238, "FY2024": 8967, "FY2023": 5639, "FY2022": 4293, "FY2021": 28, "FY2020": 168, "FY2019": 204, "FY2018": 240, "FY2017": 276, "FY2016": 312, "FY2015": 350}),
    ("DATA", "Tangible fixed assets", {"FY2025": 116, "FY2024": 79, "FY2023": 51, "FY2022": 305, "FY2021": 484, "FY2020": 1246, "FY2019": 2597, "FY2018": 3497, "FY2017": 3109, "FY2016": 3750, "FY2015": 3914}),
    ("DATA", "Right of use (\"ROU\") assets", {"FY2025": 3202, "FY2024": 2323, "FY2023": 2258, "FY2022": 2557, "FY2021": 0}),
    ("DATA", "Current tax assets", {"FY2025": 785, "FY2024": 4886, "FY2023": 2136, "FY2022": 0}),
    ("DATA", "Deferred tax assets (net)", {"FY2024": 1409, "FY2023": 367, "FY2022": 1012, "FY2021": 872, "FY2020": 870, "FY2019": 552, "FY2018": 319}),
    ("DATA", "Prepayments and accruals", {"FY2020": 4174, "FY2019": 946, "FY2018": 628, "FY2017": 4137, "FY2016": 1225, "FY2015": 730}),
    ("DATA", "Other assets", {"FY2025": 22609, "FY2024": 47056, "FY2023": 51992, "FY2022": 27813, "FY2021": 14380, "FY2020": 5465, "FY2019": 5970, "FY2018": 491, "FY2017": 311, "FY2016": 291, "FY2015": 62}),
    ("TOTAL", "Total assets", {"FY2025": 7856889, "FY2024": 7573159, "FY2023": 5810647, "FY2022": 4657420, "FY2021": 3570311, "FY2020": 3116216, "FY2019": 2729924, "FY2018": 1770807, "FY2017": 768587, "FY2016": 291922, "FY2015": 94771}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Customer deposits", {"FY2025": 6513248, "FY2024": 6103046, "FY2023": 4639352, "FY2022": 3613260, "FY2021": 2643603, "FY2020": 2313628, "FY2019": 1986639, "FY2018": 1185860, "FY2017": 491261, "FY2016": 202397, "FY2015": 10939}),
    ("DATA", "Accrued interest on customer deposits", {"FY2017": 5845, "FY2016": 1297}),
    ("DATA", "Borrowings under BoE facilities (Term Funding Scheme)", {"FY2025": 5031, "FY2024": 202445, "FY2023": 202647, "FY2022": 201423, "FY2021": 200050, "FY2020": 181796, "FY2019": 182013, "FY2018": 182110, "FY2017": 1000}),
    ("DATA", "Derivative liabilities held for risk management", {"FY2025": 7898, "FY2024": 14411, "FY2023": 0}),
    ("DATA", "Trade and other payables", {"FY2025": 35558, "FY2024": 22935, "FY2023": 19780, "FY2022": 14619, "FY2021": 23396, "FY2020": 24363, "FY2019": 16894, "FY2018": 9406, "FY2017": 4561, "FY2016": 1730, "FY2015": 834}),
    ("DATA", "Intercompany borrowings", {"FY2025": 6007, "FY2024": 8345, "FY2023": 11953, "FY2022": 0}),
    ("DATA", "Current tax liabilities", {"FY2025": 745, "FY2024": 58, "FY2023": 0}),
    ("DATA", "Other liabilities", {"FY2025": 30042, "FY2024": 21389, "FY2023": 21644, "FY2022": 33955, "FY2021": 24266, "FY2020": 18193, "FY2019": 24813, "FY2018": 13660, "FY2017": 12085, "FY2016": 5137, "FY2015": 8}),
    ("DATA", "Deferred tax liabilities (net)", {"FY2025": 2754, "FY2024": 0, "FY2018": 0, "FY2017": 6}),
    ("DATA", "Tier 2 subordinated debt", {"FY2025": 188076, "FY2024": 180949, "FY2023": 30141, "FY2022": 49778, "FY2021": 49678, "FY2020": 49559, "FY2019": 49459, "FY2018": 49358}),
    ("TOTAL", "Total liabilities", {"FY2025": 6789359, "FY2024": 6553578, "FY2023": 4925517, "FY2022": 3913035, "FY2021": 2940993, "FY2020": 2587539, "FY2019": 2259818, "FY2018": 1440394, "FY2017": 514758, "FY2016": 210561, "FY2015": 11820}),
    ("SECTION", "Capital and reserves", {}),
    ("DATA", "Called up share capital", {"FY2025": 389320, "FY2024": 389320, "FY2023": 389320, "FY2022": 389320, "FY2021": 389320, "FY2020": 389320, "FY2019": 389320, "FY2018": 299320, "FY2017": 249320, "FY2016": 86320, "FY2015": 85500}),
    ("DATA", "Share-based payments reserve", {"FY2025": 146, "FY2024": 176, "FY2023": 149, "FY2022": 111, "FY2021": 83, "FY2020": 79, "FY2019": 66, "FY2018": 48, "FY2017": 25, "FY2016": 4}),
    ("DATA", "Retained earnings", {"FY2025": 667507, "FY2024": 625420, "FY2023": 487565, "FY2022": 351208, "FY2021": 239670, "FY2020": 139278, "FY2019": 80744, "FY2018": 31091, "FY2017": 4511, "FY2016": -4963, "FY2015": -2542}),
    ("DATA", "Fair value reserve (FVOCI)", {"FY2025": 25, "FY2024": 8, "FY2023": 56, "FY2022": 24, "FY2021": 245, "FY2020": 0, "FY2019": -24, "FY2018": -46, "FY2017": -27, "FY2016": 0, "FY2015": -7}),
    ("DATA", "Cash flow hedge reserve", {"FY2025": -39, "FY2024": -2785, "FY2023": 2261, "FY2022": 0}),
    ("DATA", "Non-controlling interests", {"FY2025": 10571, "FY2024": 7442, "FY2023": 5835, "FY2022": 3722, "FY2021": 0}),
    ("TOTAL", "Total equity", {"FY2025": 1067530, "FY2024": 1019581, "FY2023": 885130, "FY2022": 744385, "FY2021": 629318, "FY2020": 528677, "FY2019": 470106, "FY2018": 330413, "FY2017": 253829, "FY2016": 81361, "FY2015": 82951}),
    ("TOTAL", "Total liabilities and equity", {"FY2025": 7856889, "FY2024": 7573159, "FY2023": 5810647, "FY2022": 4657420, "FY2021": 3570311, "FY2020": 3116216, "FY2019": 2729924, "FY2018": 1770807, "FY2017": 768587, "FY2016": 291922, "FY2015": 94771}),
]

bw.add_balance_sheet_sheet(
    title="OakNorth Bank plc — Balance Sheet",
    subtitle="Bank Group (consolidated) basis from FY2022, Bank standalone basis FY2015-FY2021, £'000 (FY2021 is "
              "the Bank's own officially IFRS-restated comparative - see basis note below). Blank cells indicate "
              "a line not disclosed that year (0 indicates a line disclosed as nil, not a gap). Investment "
              "securities breakdown (by measurement basis and by UK Gilts/Treasury bills vs money market funds/CLO "
              "tranches) sourced from: FY2025/FY2024 - Annual Report 2025, Note 14 'Investment securities', p.130 "
              f"- {AR_URLS['FY2025']}; FY2024/FY2023 - Annual Report 2024, Note 16 'Investment securities', "
              f"pp.114-115 - {AR_URLS['FY2024']}; FY2023/FY2022 - Annual Report 2023, Note 15 'Investment "
              f"securities (Applicable to Bank only)', p.108 - {AR_URLS['FY2023']}; FY2022/FY2021/FY2020 - Annual "
              f"Report 2022, Note 14 'Debt securities (Applicable to Bank only)', p.136 - {AR_URLS['FY2022']}. "
              "All years to date are backed 100% by UK Gilts/Treasury bills except FY2023-FY2025, which also hold "
              "US money market funds, and FY2025, which additionally holds senior CLO tranches and long-term "
              "gilts at amortised cost (the Bank's first amortised-cost investment securities; all prior years' "
              "holdings were entirely at FVOCI).",
    rows=bs_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=68,
    source_height=280,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Profit & Loss
# ---------------------------------------------------------------
pl_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest income", {"FY2025": 568469, "FY2024": 568925, "FY2023": 438860, "FY2022": 248605, "FY2021": 188540, "FY2020": 166433, "FY2019": 130792, "FY2018": 70770, "FY2017": 31218, "FY2016": 8683, "FY2015": 198}),
    ("DATA", "Interest expense", {"FY2025": -287872, "FY2024": -285202, "FY2023": -169664, "FY2022": -47936, "FY2021": -25852, "FY2020": -35331, "FY2019": -34968, "FY2018": -17094, "FY2017": -6294, "FY2016": -1490, "FY2015": -42}),
    ("TOTAL", "Net interest income", {"FY2025": 280597, "FY2024": 283723, "FY2023": 269196, "FY2022": 200669, "FY2021": 162688, "FY2020": 131102, "FY2019": 95824, "FY2018": 53676, "FY2017": 24924, "FY2016": 7193, "FY2015": 156}),
    ("DATA", "Fee and commission income", {"FY2025": 37403, "FY2024": 29027, "FY2023": 27410, "FY2022": 20421, "FY2021": 13502, "FY2020": 9014, "FY2019": 8517, "FY2018": 6402, "FY2017": 3347, "FY2016": 474, "FY2015": 4}),
    ("DATA", "Net gains/(losses) from financial instruments at FVPL", {"FY2025": 47, "FY2024": -791, "FY2023": 173}),
    ("DATA", "Loss on derecognition of financial instruments at amortised cost", {"FY2024": -2108}),
    ("TOTAL", "Net interest and fee income", {"FY2025": 318047, "FY2024": 309851, "FY2023": 296779, "FY2022": 221090, "FY2021": 176190, "FY2020": 140116, "FY2019": 104341, "FY2018": 60078, "FY2017": 28271, "FY2016": 7667, "FY2015": 160}),
    ("SECTION", "Operating expenses and provisions", {}),
    ("DATA", "Administrative expenses", {"FY2025": -88007, "FY2024": -93307, "FY2023": -81843, "FY2022": -57105, "FY2021": -44385, "FY2020": -39512, "FY2019": -32098, "FY2018": -21117, "FY2017": -15291, "FY2016": -8349, "FY2015": -2360}),
    ("DATA", "Depreciation and amortisation", {"FY2025": -3572, "FY2024": -2659, "FY2023": -2490, "FY2022": -887, "FY2021": -959, "FY2020": -1433, "FY2019": -1487, "FY2018": -1212, "FY2017": -980, "FY2016": -864, "FY2015": -25}),
    ("DATA", "(Charge)/reversal of provision for credit impairment losses", {"FY2025": -91, "FY2024": 4427, "FY2023": -25113, "FY2022": -10762, "FY2021": 3694, "FY2020": -21588, "FY2019": -4890, "FY2018": -3895, "FY2017": -1420, "FY2016": -875, "FY2015": -62}),
    ("DATA", "Charge for provision for other assets", {"FY2025": -3848, "FY2024": -3518, "FY2023": -929}),
    ("TOTAL", "Operating expenses and provisions", {"FY2025": -95518, "FY2024": -95057, "FY2023": -109446, "FY2022": -68754, "FY2021": -41650, "FY2020": -62533, "FY2019": -38475, "FY2018": -26224, "FY2017": -17691, "FY2016": -10088, "FY2015": -2447}),
    ("TOTAL", "Profit before tax", {"FY2025": 222529, "FY2024": 214794, "FY2023": 187333, "FY2022": 152336, "FY2021": 134540, "FY2020": 77583, "FY2019": 65866, "FY2018": 33854, "FY2017": 10580, "FY2016": -2421, "FY2015": -2287}),
    ("DATA", "Taxation", {"FY2025": -57318, "FY2024": -55460, "FY2023": -48863, "FY2022": -39077, "FY2021": -34148, "FY2020": -19049, "FY2019": -15890, "FY2018": -7274, "FY2017": -1106, "FY2016": 0, "FY2015": 0}),
    ("TOTAL", "Profit for the year", {"FY2025": 165211, "FY2024": 159334, "FY2023": 138470, "FY2022": 113259, "FY2021": 100392, "FY2020": 58534, "FY2019": 49976, "FY2018": 26580, "FY2017": 9474, "FY2016": -2421, "FY2015": -2287}),
    ("SECTION", "Other comprehensive income/(expense), net of tax", {}),
    ("DATA", "Fair value changes on financial assets at FVOCI", {"FY2025": 17, "FY2024": -48, "FY2023": 32, "FY2022": -221, "FY2021": 245, "FY2020": 24, "FY2019": 22, "FY2018": -19, "FY2017": -27, "FY2016": 7, "FY2015": -7}),
    ("DATA", "Changes in cash flow hedge reserve", {"FY2025": 2746, "FY2024": -5046, "FY2023": 2261}),
    ("DATA", "Changes in cost of hedging reserve", {"FY2024": 56, "FY2023": -56}),
    ("TOTAL", "Total other comprehensive income/(expense) for the year", {"FY2025": 2763, "FY2024": -5038, "FY2023": 2237, "FY2022": -221, "FY2021": 245, "FY2020": 24, "FY2019": 22, "FY2018": -19, "FY2017": -27, "FY2016": 7, "FY2015": -7}),
    ("TOTAL", "Total comprehensive income for the year", {"FY2025": 167974, "FY2024": 154296, "FY2023": 140707, "FY2022": 113038, "FY2021": 100637, "FY2020": 58558, "FY2019": 49998, "FY2018": 26561, "FY2017": 9447, "FY2016": -2414, "FY2015": -2294}),
]

bw.add_income_statement_sheet(
    title="OakNorth Bank plc — Profit & Loss",
    subtitle="Bank Group (consolidated) basis, £'000 (FY2021 is the Bank's own officially IFRS-restated comparative - "
              "see basis note below). FY2025's own presentation combines 'Net gains/(losses) from financial "
              "instruments at FVPL' and 'Loss on derecognition of financial instruments at amortised cost' into a "
              "single 'Other gains/(losses) from financial instruments' line (£47k) - shown here in the FVPL row for "
              "comparability, since no derecognition loss was separately disclosed that year.",
    rows=pl_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=76,
    source_height=280,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Statement of Changes in Equity - per-year reconciliation ladder confirmed:
# every year's own closing balance ties exactly to both the next year's own
# opening balance and that year's own Balance Sheet Total equity. Zero plug
# rows needed anywhere across all 5 years, once the bank's own genuine £470k
# IFRS transition adjustment (FRS 102 -> IFRS, effective FY2022) is shown as
# its own explicit row rather than absorbed elsewhere.
# ---------------------------------------------------------------
equity_headers = ["Called up Share Capital", "Retained earnings", "Fair value reserve (FVOCI)",
                   "Cash flow hedge reserve", "Cost of hedging reserve", "Share-based payments reserve",
                   "Non-controlling interests", "Total equity"]
equity_rows = [
    ("TOTAL", "At 3 July 2013 (incorporation)", (1, None, None, None, None, None, None, 1)),
    ("TOTAL", "At 31 December 2014 (pre-authorisation shell period)", (1180, -255, None, None, None, None, None, 925)),
    ("DATA", "Issue of share capital", (84320, None, None, None, None, None, None, 84320)),
    ("DATA", "Loss for the year", (None, -2287, None, None, None, None, None, -2287)),
    ("DATA", "Fair value changes on available for sale financial instruments", (None, None, -7, None, None, None, None, -7)),
    ("TOTAL", "At 31 December 2015 (FY2015 closing)", (85500, -2542, -7, None, None, None, None, 82951)),
    ("DATA", "Issue of share capital", (820, None, None, None, None, None, None, 820)),
    ("DATA", "Loss for the year", (None, -2421, None, None, None, None, None, -2421)),
    ("DATA", "Capital contribution (employee share-based payments)", (None, None, None, None, None, 4, None, 4)),
    ("DATA", "Fair value changes on available for sale financial instruments", (None, None, 7, None, None, None, None, 7)),
    ("TOTAL", "At 31 December 2016 (FY2016 closing)", (86320, -4963, 0, None, None, 4, None, 81361)),
    ("DATA", "Issue of share capital", (163000, None, None, None, None, None, None, 163000)),
    ("DATA", "Profit for the year", (None, 9474, None, None, None, None, None, 9474)),
    ("DATA", "Employee share-based payments", (None, None, None, None, None, 21, None, 21)),
    ("DATA", "Fair value changes on available for sale financial instruments", (None, None, -33, None, None, None, None, -33)),
    ("DATA", "Deferred tax on available for sale financial instruments", (None, None, 6, None, None, None, None, 6)),
    ("TOTAL", "At 31 December 2017 (FY2017 closing)", (249320, 4511, -27, None, None, 25, None, 253829)),
    ("DATA", "Issue of share capital", (50000, None, None, None, None, None, None, 50000)),
    ("DATA", "Profit for the year", (None, 26580, None, None, None, None, None, 26580)),
    ("DATA", "Employee share-based payments", (None, None, None, None, None, 23, None, 23)),
    ("DATA", "Fair value changes on available for sale financial instruments", (None, None, -25, None, None, None, None, -25)),
    ("DATA", "Deferred tax on available for sale financial instruments", (None, None, 6, None, None, None, None, 6)),
    ("TOTAL", "At 31 December 2018 (FY2018 closing)", (299320, 31091, -46, None, None, 48, None, 330413)),
    ("DATA", "IFRS 9 transition adjustment, net of tax (1 January 2019; the 'available for sale reserve' balance "
             "carries forward unchanged, relabelled 'FVOCI reserve' under IFRS 9)", (None, -323, None, None, None, None, None, -323)),
    ("TOTAL", "At 1 January 2019 (FY2019 opening, IFRS 9 restated)", (299320, 30768, -46, None, None, 48, None, 330090)),
    ("DATA", "Issue of share capital", (90000, None, None, None, None, None, None, 90000)),
    ("DATA", "Profit for the year", (None, 49976, None, None, None, None, None, 49976)),
    ("DATA", "Employee share-based payments", (None, None, None, None, None, 18, None, 18)),
    ("DATA", "Fair value changes on financial assets at FVOCI", (None, None, 22, None, None, None, None, 22)),
    ("TOTAL", "At 31 December 2019 (FY2019 closing)", (389320, 80744, -24, None, None, 66, None, 470106)),
    ("DATA", "Profit for the year", (None, 58534, None, None, None, None, None, 58534)),
    ("DATA", "Employee share-based payments", (None, None, None, None, None, 13, None, 13)),
    ("DATA", "Fair value changes on financial assets at FVOCI", (None, None, 24, None, None, None, None, 24)),
    ("TOTAL", "At 31 December 2020 (FY2020 closing)", (389320, 139278, 0, None, None, 79, None, 528677)),
    ("TOTAL", "At 1 January 2021 (FY2021 opening)", (389320, 139278, None, None, None, 79, None, 528677)),
    ("DATA", "Profit for the year", (None, 100392, None, None, None, None, None, 100392)),
    ("DATA", "Other comprehensive income for the year (FVOCI)", (None, None, 245, None, None, None, None, 245)),
    ("DATA", "Employee share-based payments", (None, None, None, None, None, 4, None, 4)),
    ("TOTAL", "At 31 December 2021 (FY2021 closing, IFRS restated)", (389320, 239670, 245, None, None, 83, None, 629318)),
    ("DATA", "IFRS transition adjustment, net of tax (FRS 102 -> IFRS, Note 1.6)", (None, -470, None, None, None, None, None, -470)),
    ("TOTAL", "At 1 January 2022 (FY2022 opening, IFRS restated)", (389320, 239200, 245, None, None, 83, None, 628848)),
    ("DATA", "Non-controlling interest on acquisition of subsidiary", (None, None, None, None, None, None, 2593, 2593)),
    ("DATA", "Profit for the year", (None, 112069, None, None, None, None, 1190, 113259)),
    ("DATA", "Other comprehensive expense for the year (FVOCI)", (None, None, -221, None, None, None, None, -221)),
    ("DATA", "Employee share-based payments", (None, None, None, None, None, 28, None, 28)),
    ("DATA", "Unwinding of investment in A.S.K entities", (None, -61, None, None, None, None, -61, -122)),
    ("TOTAL", "At 31 December 2022 (FY2022 closing)", (389320, 351208, 24, None, None, 111, 3722, 744385)),
    ("DATA", "Profit for the year", (None, 136357, None, None, None, None, 2113, 138470)),
    ("DATA", "Other comprehensive income for the year", (None, None, 32, 2261, -56, None, None, 2237)),
    ("DATA", "Employee share-based payments", (None, None, None, None, None, 38, None, 38)),
    ("TOTAL", "At 31 December 2023 (FY2023 closing)", (389320, 487565, 56, 2261, -56, 149, 5835, 885130)),
    ("DATA", "Profit for the year", (None, 157823, None, None, None, None, 1511, 159334)),
    ("DATA", "Other comprehensive (expense)/income for the year", (None, None, -48, -5046, 56, None, None, -5038)),
    ("DATA", "Employee share-based payments", (None, None, None, None, None, 27, None, 27)),
    ("DATA", "Issue of growth shares", (None, None, None, None, None, None, 64, 64)),
    ("DATA", "Payment of dividend to parent", (None, -20000, None, None, None, None, None, -20000)),
    ("DATA", "Unwinding of investments in A.S.K Group entities", (None, 32, None, None, None, None, 32, 64)),
    ("TOTAL", "At 31 December 2024 (FY2024 closing)", (389320, 625420, 8, -2785, None, 176, 7442, 1019581)),
    ("DATA", "Profit for the year", (None, 162087, None, None, None, None, 3124, 165211)),
    ("DATA", "Other comprehensive income for the year", (None, None, 17, 2746, None, None, None, 2763)),
    ("DATA", "Employee share-based payments", (None, None, None, None, None, 58, None, 58)),
    ("DATA", "ESS settlement", (None, None, None, None, None, -88, None, -88)),
    ("DATA", "Issue of growth shares", (None, None, None, None, None, None, 5, 5)),
    ("DATA", "Payment of dividend to parent", (None, -120000, None, None, None, None, None, -120000)),
    ("TOTAL", "At 31 December 2025 (FY2025 closing)", (389320, 667507, 25, -39, None, 146, 10571, 1067530)),
]

bw.add_equity_changes_sheet(
    title="OakNorth Bank plc — Statement of Changes in Equity",
    subtitle="Chronological roll-forward from incorporation (3 July 2013) to FY2025 closing, Bank standalone basis "
              "FY2015-FY2021 and Bank Group (consolidated) basis from FY2022, £'000. Equity reconciliation ladder "
              "confirmed: every year's own closing balance ties exactly to both the next year's own opening "
              "balance and that year's own Balance Sheet Total equity across all 11 years - zero undocumented "
              "plug rows anywhere. The two bridging rows (the FRS 102 -> IFRS transition adjustment at 1 January "
              "2022 and the IAS 39 -> IFRS 9 transition adjustment at 1 January 2019) are genuine, bank-disclosed "
              "items, not errors.",
    headers=equity_headers,
    rows=equity_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=66,
)

cash_rows = [
    ("SECTION", "Reconciliation of profit before tax to operating cash flows", {}),
    ("DATA", "Profit before tax", {"FY2025": 222529, "FY2024": 214794, "FY2023": 187333, "FY2022": 152336, "FY2021": 134540, "FY2020": 77583, "FY2019": 65866, "FY2018": 33854, "FY2017": 10580, "FY2016": -2421, "FY2015": -2287}),
    ("DATA", "Adjustments for non-cash items", {"FY2025": 20707, "FY2024": 11139, "FY2023": 30215, "FY2022": 7056, "FY2021": 646}),
    ("DATA", "Depreciation and amortisation", {"FY2020": 1433, "FY2019": 1487, "FY2018": 1212, "FY2017": 980, "FY2016": 864, "FY2015": 25}),
    ("DATA", "Expected credit loss allowance / provisions for incurred but not reported losses", {"FY2020": 21588, "FY2019": 4890, "FY2018": 3895, "FY2017": 1420, "FY2016": 875, "FY2015": 62}),
    ("DATA", "Impairment of fixed assets", {"FY2017": 60, "FY2016": 96}),
    ("DATA", "Share-based payments to employees", {"FY2020": 13, "FY2019": 18, "FY2018": 23, "FY2017": 21, "FY2016": 4}),
    ("DATA", "Fair value changes on available for sale financial instruments (non-cash adjustment)", {"FY2016": 7}),
    ("DATA", "Net change in other assets and liabilities", {"FY2025": 41185, "FY2024": 4665, "FY2023": -30857, "FY2022": -14137, "FY2021": -2050, "FY2020": -3300, "FY2019": 8706, "FY2018": 3123}),
    ("DATA", "Increase in receivables", {"FY2017": -2932, "FY2016": -724, "FY2015": -789}),
    ("DATA", "Increase in payables", {"FY2017": 13368, "FY2016": 7282, "FY2015": 670}),
    ("DATA", "Increase in loan receivables", {"FY2025": -496341, "FY2024": -573437, "FY2023": -714507, "FY2022": -251805, "FY2021": -390362, "FY2020": -450852, "FY2019": -769938, "FY2018": -693358, "FY2017": -380849, "FY2016": -211477, "FY2015": -14968}),
    ("DATA", "Increase in customer deposits", {"FY2025": 408891, "FY2024": 1463663, "FY2023": 1026092, "FY2022": 969657, "FY2021": 329975, "FY2020": 326989, "FY2019": 800779, "FY2018": 688755, "FY2017": 288864, "FY2016": 191458, "FY2015": 10939}),
    ("DATA", "Increase in borrowings (within operating activities, as presented in the FY2017 statement)", {"FY2017": 1000}),
    ("DATA", "(Increase)/decrease in derivatives held for risk management", {"FY2025": -29903, "FY2024": 7655, "FY2023": -2530}),
    ("DATA", "Interest received on investing cash flows", {"FY2020": -446, "FY2019": -713}),
    ("DATA", "Interest paid on financing cash flows", {"FY2020": 4475, "FY2019": 5396}),
    ("DATA", "Income taxes paid", {"FY2025": -49351, "FY2024": -57333, "FY2023": -52840, "FY2022": -39766, "FY2021": -31850, "FY2020": -17948, "FY2019": -12312, "FY2018": -4759, "FY2017": -180}),
    ("DATA", "Income tax refund received", {"FY2018": 3, "FY2017": 45}),
    ("DATA", "Other operating adjustments not separately shown", {"FY2023": 531, "FY2022": 9880, "FY2021": 710}),
    ("TOTAL", "Net cash flows generated from operating activities", {"FY2025": 117717, "FY2024": 1071146, "FY2023": 443437, "FY2022": 833221, "FY2021": 41609, "FY2020": -40465, "FY2019": 104179, "FY2018": 32748, "FY2017": -67623, "FY2016": -14036, "FY2015": -4061}),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Purchase of intangible assets", {"FY2025": -7832, "FY2024": -5279, "FY2023": -2961, "FY2022": -4358}),
    ("DATA", "Purchase of tangible assets", {"FY2025": -299, "FY2024": -75, "FY2023": -18, "FY2022": -19, "FY2021": -57}),
    ("DATA", "Purchase of property, plant & equipment and intangible assets (combined presentation)", {"FY2020": -46, "FY2019": -551, "FY2018": -1564, "FY2017": -363, "FY2016": -758, "FY2015": -3261}),
    ("DATA", "Acquisition of subsidiary, net of cash acquired", {"FY2022": -10475}),
    ("DATA", "Purchase of investment securities", {"FY2025": -621941, "FY2024": -820024, "FY2023": -897488, "FY2022": -202501, "FY2021": -191086, "FY2020": -262057, "FY2019": -105826, "FY2018": -103663, "FY2017": -2148, "FY2016": -499, "FY2015": -53245}),
    ("DATA", "Proceeds from sale/maturity of investment securities", {"FY2025": 409522, "FY2024": 830700, "FY2023": 905244, "FY2022": 191000, "FY2021": 126771, "FY2020": 229000, "FY2019": 103000, "FY2018": 2139, "FY2017": 500, "FY2016": 53238}),
    ("DATA", "Interest received on investment securities", {"FY2025": 21152, "FY2023": 623, "FY2022": 1076, "FY2021": 4029, "FY2020": 7817, "FY2019": 2652}),
    ("DATA", "Other investing cash flows and classification differences", {"FY2025": 90, "FY2024": 19, "FY2023": 18}),
    ("TOTAL", "Net cash flows from/(used in) investing activities", {"FY2025": -199308, "FY2024": 5341, "FY2023": 5418, "FY2022": -25277, "FY2021": -60343, "FY2020": -25286, "FY2019": -725, "FY2018": -103088, "FY2017": -2011, "FY2016": 51981, "FY2015": -56506}),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Increase in borrowings from Bank of England facilities", {"FY2025": 15000}),
    ("DATA", "Repayment of borrowings from Bank of England facilities", {"FY2025": -210000}),
    ("DATA", "Proceeds on issue of shares", {"FY2019": 90000, "FY2018": 50000, "FY2017": 163000, "FY2016": 820, "FY2015": 84320}),
    ("DATA", "Increase in subordinated debt", {"FY2024": 150000, "FY2023": 30000, "FY2018": 48977}),
    ("DATA", "Increase in intercompany borrowings", {"FY2025": 4541, "FY2024": 6326, "FY2023": 11660}),
    ("DATA", "Repayment/decrease of intercompany borrowings", {"FY2025": -7041, "FY2024": -9772}),
    ("DATA", "Interest paid on borrowings and subordinated debt", {"FY2025": -24084, "FY2024": -15538, "FY2023": -10073, "FY2022": -5449, "FY2021": -3964, "FY2020": -4591, "FY2019": -5396}),
    ("DATA", "Cash outflow on lease liabilities", {"FY2025": -1456, "FY2024": -1408, "FY2023": -686, "FY2022": -1050}),
    ("DATA", "Payment of dividend to parent", {"FY2025": -120000, "FY2024": -20000}),
    ("DATA", "Repayment of subordinated debt", {"FY2023": -50000}),
    ("DATA", "Other financing cash flows and classification differences", {"FY2025": -199}),
    ("DATA", "Increase in TFS borrowings", {"FY2021": 18100, "FY2018": 180900}),
    ("TOTAL", "Net cash flows from/(used in) financing activities", {"FY2025": -343239, "FY2024": 109608, "FY2023": -19099, "FY2022": -6499, "FY2021": 14136, "FY2020": -4591, "FY2019": 84604, "FY2018": 279877, "FY2017": 163000, "FY2016": 820, "FY2015": 84320}),
    ("TOTAL", "Net increase/(decrease) in cash and cash equivalents", {"FY2025": -424920, "FY2024": 1186076, "FY2023": 429738, "FY2022": 801445, "FY2021": -4598, "FY2020": -70342, "FY2019": 188058, "FY2018": 209537, "FY2017": 93366, "FY2016": 38765, "FY2015": 21466}),
    ("DATA", "Cash and cash equivalents at beginning of year", {"FY2025": 2893652, "FY2024": 1707576, "FY2023": 1277838, "FY2022": 476393, "FY2021": 480991, "FY2020": 551333, "FY2019": 363275, "FY2018": 153738, "FY2017": 60336, "FY2016": 21571, "FY2015": 105}),
    ("TOTAL", "Cash and cash equivalents at end of year", {"FY2025": 2468732, "FY2024": 2893652, "FY2023": 1707576, "FY2022": 1277838, "FY2021": 476393, "FY2020": 480991, "FY2019": 551333, "FY2018": 363275, "FY2017": 153702, "FY2016": 60336, "FY2015": 21571}),
    ("SECTION", "Reconciliation to cash at banks", {}),
    ("DATA", "Cash and balances at central bank", {"FY2025": 2199053, "FY2024": 2689013, "FY2023": 1637314, "FY2022": 1235711, "FY2021": 446374, "FY2020": 469459, "FY2019": 540035, "FY2018": 356881, "FY2017": 148340, "FY2016": 51175}),
    ("DATA", "Loans and advances to banks", {"FY2025": 77587, "FY2024": 75477, "FY2023": 33458, "FY2022": 37507, "FY2021": 30019, "FY2020": 11532, "FY2019": 11298, "FY2018": 6394, "FY2017": 5362, "FY2016": 9161, "FY2015": 21571}),
    ("DATA", "Investment securities (US money market funds)", {"FY2025": 192092, "FY2024": 124007, "FY2023": 31788}),
    ("TOTAL", "Total cash and cash equivalents", {"FY2025": 2468732, "FY2024": 2888497, "FY2023": 1702560, "FY2022": 1273218, "FY2021": 476393, "FY2020": 480991, "FY2019": 551333, "FY2018": 363275, "FY2017": 153702, "FY2016": 60336, "FY2015": 21571}),
]
bw.add_cash_flow_sheet(
    "OakNorth Bank plc — Consolidated Statement of Cash Flows",
    "Bank Group basis for FY2022–FY2025; standalone Bank basis for FY2015–FY2021, £'000",
    cash_rows, cash_flow_sources(), first_col_width=68, source_height=280, unit_suffix=" (£'000)"
)

# ---------------------------------------------------------------
# Asset Quality - OakNorth Bank standalone (entity-level) loans and advances
# to customers, IFRS 9 stage 1/2/3 split. Bank-only basis (not Bank Group) -
# this is the finest granularity the Bank discloses; net carrying value ties
# exactly to the Balance Sheet's Bank Group loans and advances figure only
# for FY2021 (before the subsidiary was consolidated) - later years differ
# by the subsidiary's own lending, a genuine basis difference, not an error.
# ---------------------------------------------------------------
asset_quality_rows = [
    ("SECTION", "OakNorth Bank (standalone) loans and advances to customers, on-balance sheet, by IFRS 9 stage", {}),
    ("DATA", "Stage 1 gross carrying amount", {"FY2025": 4514265, "FY2024": 3976861, "FY2023": 3397765, "FY2022": 2990755, "FY2021": 2782991, "FY2020": 2342432, "FY2019": 1968550}),
    ("DATA", "Stage 2 gross carrying amount", {"FY2025": 242557, "FY2024": 358650, "FY2023": 357847, "FY2022": 64825, "FY2021": 69097, "FY2020": 82112, "FY2019": 65317}),
    ("DATA", "Stage 3 gross carrying amount", {"FY2025": 146439, "FY2024": 76908, "FY2023": 91089, "FY2022": 95415, "FY2021": 63228, "FY2020": 100579, "FY2019": 40426}),
    ("TOTAL", "Total gross carrying amount", {"FY2025": 4903261, "FY2024": 4412419, "FY2023": 3846701, "FY2022": 3150995, "FY2021": 2915316, "FY2020": 2525123, "FY2019": 2074293}),
    ("DATA", "Stage 1 allowance for ECL", {"FY2025": -7088, "FY2024": -6838, "FY2023": -13260, "FY2022": -13311, "FY2021": -8929, "FY2020": -19928, "FY2019": -7831}),
    ("DATA", "Stage 2 allowance for ECL", {"FY2025": -4303, "FY2024": -6292, "FY2023": -5082, "FY2022": -2507, "FY2021": -6481, "FY2020": -1432, "FY2019": -1581}),
    ("DATA", "Stage 3 allowance for ECL", {"FY2025": -6368, "FY2024": -8949, "FY2023": -12219, "FY2022": -7684, "FY2021": -13601, "FY2020": -11514, "FY2019": -1896}),
    ("TOTAL", "Total allowance for ECL", {"FY2025": -17759, "FY2024": -22079, "FY2023": -30561, "FY2022": -23502, "FY2021": -29011, "FY2020": -32874, "FY2019": -11308}),
    ("TOTAL", "Net carrying amount", {"FY2025": 4885502, "FY2024": 4390340, "FY2023": 3816140, "FY2022": 3127493, "FY2021": 2886305, "FY2020": 2492249, "FY2019": 2062985}),
    ("DATA", "Stage 3 as % of total gross carrying amount (NPL ratio)", {"FY2025": "2.99%", "FY2024": "1.74%", "FY2023": "2.37%", "FY2022": "3.03%", "FY2021": "2.17%", "FY2020": "3.98%", "FY2019": "1.95%"}),
    ("DATA", "Stage 2 as % of total gross carrying amount", {"FY2025": "4.95%", "FY2024": "8.13%", "FY2023": "9.30%", "FY2022": "2.06%", "FY2021": "2.37%", "FY2020": "3.25%", "FY2019": "3.15%"}),
    ("DATA", "Total allowance for ECL as % of total gross carrying amount (coverage)", {"FY2025": "0.36%", "FY2024": "0.50%", "FY2023": "0.79%", "FY2022": "0.75%", "FY2021": "1.00%", "FY2020": "1.30%", "FY2019": "0.55%"}),
]

bw.add_asset_quality_sheet(
    title="OakNorth Bank plc — Asset Quality",
    subtitle="OakNorth Bank plc standalone (entity-level, not Bank Group) loans and advances to customers, IFRS 9 "
              "stage 1/2/3 split, on-balance sheet only (excludes undrawn loan commitments, disclosed separately). £'000.",
    rows=asset_quality_rows,
    sources_text=(
        "Sources - OakNorth Bank plc, on-balance sheet Stage 1/2/3 exposure and ECL allowance tables (OakNorth "
        "Bank standalone, not Bank Group):\n"
        f"FY2025: Annual Report 2025, Table 5 'Movement in gross exposures and impairment allowance ... "
        f"(OakNorth Bank Plc)', p.66 - {AR_URLS['FY2025']}\n"
        f"FY2024: Annual Report 2024, Table 3 (same title), p.63 - {AR_URLS['FY2024']}\n"
        f"FY2023: Annual Report 2023, Table 1 'Maximum exposure to credit risk in the loan book, ECL provisions and "
        f"Staging (OakNorth Bank)', p.55 - {AR_URLS['FY2023']}\n"
        f"FY2022/FY2021: Annual Report 2022, Table 1 (same title, both years shown), p.71 - {AR_URLS['FY2022']}\n"
        f"FY2020/FY2019: Annual Report 2020, Note 9.2 'Loans and advances to customers - Movement in staging', "
        f"pp.74-75 (both years shown) - {AR_URLS['FY2020']}\n\n"
        "DATA QUALITY / BASIS NOTE: this sheet is OakNorth Bank plc standalone (entity-level), the finest "
        "granularity at which IFRS 9 stage data is disclosed - it is NOT the Bank Group consolidated figure used "
        "on the Balance Sheet/Profit & Loss/Statement of Changes in Equity sheets. For FY2019-FY2021 (before the "
        "A.S.K Partners Limited subsidiary was consolidated) the two bases are identical and this sheet's net "
        "carrying amount ties exactly to the Balance Sheet's loans and advances to customers figure for each of "
        "those years (FY2019: 2,062,985; FY2020: 2,492,249; FY2021: 2,886,305). From FY2022 onward the two bases "
        "diverge by the subsidiary's own lending (FY2022: 457; FY2023: 1,204; FY2024: 2,760; FY2025: 4,372) - "
        "each year's own figure is shown as originally disclosed rather than adjusted to force a tie.\n\n"
        "SELF-SKIP, FY2015-FY2018 (HD-021): no IFRS 9 stage 1/2/3 split exists for these years. OakNorth adopted "
        "IFRS 9 'Financial Instruments' (which introduced the stage-based expected-credit-loss model) only with "
        "effect from 1 January 2019, without restating FY2018 comparatives (Annual Report 2019, Note 1.1); its "
        "FY2015-FY2018 accounts were prepared under IAS 39, which uses an incurred-loss 'IBNR' (incurred but not "
        "reported) provisioning model with no stage concept at all. This is a genuine, verified non-existence of "
        "the disclosure in the primary source for those four years, not an unfetched document - the loan-quality "
        "story for FY2015-FY2018 is instead the single aggregate IBNR provision, transcribed on the Profit & Loss "
        "and Cash Flow Statement sheets ('(Charge)/reversal of provision for credit impairment losses' and "
        "'Expected credit loss allowance / provisions for incurred but not reported losses' rows respectively)."
    ),
    first_col_width=76,
    source_height=280,
    unit_suffix=" (£'000)",
)


def metric(name, unit, rows, note=None):
    bw.add_metric_sheet(name, unit, rows, p3_sources(), note=note, first_col_width=52, source_height=155)


metric("CET1 Capital", "£'000", [("Common Equity Tier 1 (CET1) capital", {"FY2025": 988868, "FY2024": 952901, "FY2023": 853523, "FY2022": 719977, "FY2021": 628446, "FY2020": 529089, "FY2019": 463350, "FY2018": 329854, "FY2017": 253553, "FY2016": 81049, "FY2015": 82601})])
metric("CET1 Ratio", "% of RWA", [("Common Equity Tier 1 ratio", {"FY2025": "15.5%", "FY2024": "17.3%", "FY2023": "18.6%", "FY2022": "18.7%", "FY2021": "20.5%", "FY2020": "20.0%", "FY2019": "20.7%", "FY2018": "22.4%", "FY2017": "34.8%", "FY2016": "26.5%", "FY2015": "153.8%"})])
metric("Tier 1 Capital", "£'000", [("Tier 1 capital", {"FY2025": 988868, "FY2024": 952901, "FY2023": 853523, "FY2022": 719977, "FY2021": 628446, "FY2020": 529089, "FY2019": 463350, "FY2018": 329854, "FY2017": 253553, "FY2016": 81049, "FY2015": 82601})])
metric("Tier 1 Ratio", "% of RWA", [("Tier 1 ratio", {"FY2025": "15.5%", "FY2024": "17.3%", "FY2023": "18.6%", "FY2022": "18.7%", "FY2021": "20.5%", "FY2020": "20.0%", "FY2019": "20.7%", "FY2018": "22.4%", "FY2017": "34.8%", "FY2016": "26.5%", "FY2015": "153.8%"})])
metric("Total Capital", "£'000", [("Total capital", {"FY2025": 1168868, "FY2024": 1132901, "FY2023": 883523, "FY2022": 769977, "FY2021": 678446, "FY2020": 579089, "FY2019": 513350, "FY2018": 386106, "FY2017": 255910, "FY2016": 81986, "FY2015": 82663})])
metric("Total Capital Ratio", "% of RWA", [("Total capital ratio", {"FY2025": "18.4%", "FY2024": "20.5%", "FY2023": "19.3%", "FY2022": "20.1%", "FY2021": "22.1%", "FY2020": "21.9%", "FY2019": "22.9%", "FY2018": "26.2%", "FY2017": "35.1%", "FY2016": "26.9%", "FY2015": "154.0%"})])
metric("Total RWAs", "£'000", [("Total risk-weighted exposure amount", {"FY2025": 6363514, "FY2024": 5517819, "FY2023": 4577382, "FY2022": 3840274, "FY2021": 3065585, "FY2020": 2645393, "FY2019": 2236926, "FY2018": 1473692, "FY2017": 729488, "FY2016": 305317, "FY2015": 53691})])

# RWA Breakdown - Pillar 3 UK OV1 template, placed right after Total RWAs per
# the locked sheet order. All years tie to the Total RWAs figure above
# (FY2022/FY2023 off by £1 due to source-document rounding).
rwa_breakdown_rows = [
    ("DATA", "Credit risk (excluding CCR & CVA)", {"FY2025": 5801031, "FY2024": 5057693, "FY2023": 4230433, "FY2022": 3577369, "FY2021": 2875251, "FY2020": 2525393, "FY2019": 2176926, "FY2018": 1451092, "FY2017": 705788, "FY2016": 276142, "FY2015": 24516}),
    ("DATA", "Counterparty credit risk (CCR, including CVA)", {"FY2025": 32843, "FY2024": 31736, "FY2023": 13633}),
    ("DATA", "Securitisation exposures in the non-trading book (after the cap)", {"FY2025": 22393}),
    ("DATA", "Operational risk", {"FY2025": 507247, "FY2024": 428390, "FY2023": 333317, "FY2022": 262904, "FY2021": 190334, "FY2020": 120000, "FY2019": 60000, "FY2018": 22600, "FY2017": 23700, "FY2016": 29175, "FY2015": 29175}),
    ("TOTAL", "Total", {"FY2025": 6363514, "FY2024": 5517819, "FY2023": 4577382, "FY2022": 3840274, "FY2021": 3065585, "FY2020": 2645393, "FY2019": 2236926, "FY2018": 1473692, "FY2017": 729488, "FY2016": 305317, "FY2015": 53691}),
]
bw.add_rwa_breakdown_sheet(
    title="OakNorth Bank plc — RWA Breakdown",
    subtitle="Pillar 3 UK OV1 template (top-level risk-type categories), £'000. FY2025's Bank Group consolidated "
              "basis; FY2022–FY2024 solo/Bank basis; FY2015–FY2021 standalone Bank basis (per each year's own "
              "Pillar 3 disclosure - see p3_sources note). No CCR or securitisation exposure was disclosed "
              "FY2015–FY2023, and no securitisation exposure existed before the FY2025 CLO investment programme "
              "(see that sheet's own note) - both genuine absences, not gaps. OakNorth used the Standardised "
              "Approach for credit risk and market risk, and the Basic Indicator Approach for operational risk, "
              "throughout FY2015–FY2020 (its own Pillar 3 reports, section 1.2/1.1) - the same approaches used "
              "in later years.",
    rows=rwa_breakdown_rows,
    sources_text=p3_sources(),
    first_col_width=68,
    source_height=200,
    unit_suffix=" (£'000)",
)

metric("Leverage Ratio", "£'000 / %", [
    ("Leverage ratio exposure measure excluding central banks", {"FY2025": 6177019, "FY2024": 5262074, "FY2023": 4463419, "FY2022": 4954910, "FY2021": 3855405}),
    ("Leverage ratio excluding central banks", {"FY2025": "16.0%", "FY2024": "18.1%", "FY2023": "19.1%", "FY2022": "14.5%", "FY2021": "21.4%", "FY2020": "21.0%", "FY2019": "22.2%", "FY2018": "25.2%", "FY2017": "41.0%"}),
    ("Leverage ratio exposure measure including central banks", {"FY2025": 8361483, "FY2024": 7951087, "FY2023": 6100733, "FY2020": 3287032, "FY2019": 2885104, "FY2018": 1942695, "FY2017": 843406, "FY2016": 317493, "FY2015": 94822}),
    ("Leverage ratio including central banks", {"FY2025": "11.8%", "FY2024": "12.0%", "FY2023": "14.0%", "FY2020": "16.1%", "FY2019": "16.1%", "FY2018": "17.0%", "FY2017": "30.1%", "FY2016": "25.5%", "FY2015": "87.1%"}),
], note="The FY2021 disclosure labels its 21.4% figure as the UK leverage-ratio-framework calculation excluding claims on central banks; FY2022–FY2025 use the corresponding KM1 excluding-central-bank measure. FY2022–FY2025 do not disclose the including-central-bank variant in the same way until FY2023. FY2015–FY2020: OakNorth's own Pillar 3 reports disclose a single leverage exposure measure each year (the 'EBA calculation', shown here as the including-central-banks row) plus, from FY2017 onward, a second UK-framework ratio excluding claims on central banks computed off that same exposure measure (no separately restated excluding-central-banks exposure figure is given for those years, so that exposure row is left blank for FY2015–FY2020 rather than estimated). No excluding-central-banks variant is disclosed at all for FY2015–FY2016.")
metric("LCR", "£'000 / %", [
    ("Total high-quality liquid assets (HQLA), weighted value-average", {"FY2025": 2609639, "FY2024": 1876341, "FY2023": 1189319, "FY2022": 556199, "FY2021": "Not disclosed", "FY2020": 469400, "FY2019": "Not disclosed", "FY2018": 356800, "FY2017": 149400, "FY2016": "Not disclosed", "FY2015": "Not disclosed"}),
    ("Total net cash outflows, adjusted value", {"FY2025": 555901, "FY2024": 384055, "FY2023": 325606, "FY2022": 158569, "FY2021": "Not disclosed", "FY2020": 139100, "FY2019": "Not disclosed", "FY2018": 72800, "FY2017": 21000, "FY2016": "Not disclosed", "FY2015": "Not disclosed"}),
    ("Liquidity Coverage Ratio", {"FY2025": "478%", "FY2024": "489%", "FY2023": "365%", "FY2022": "351%", "FY2021": "Not publicly disclosed", "FY2020": "338%", "FY2019": "377%", "FY2018": "490%", "FY2017": "713%", "FY2016": "Not publicly disclosed", "FY2015": "Not publicly disclosed"}),
 ], note="The 2022–2025 LCR figures are the reported average/weighted-value disclosures (UK KM1 template). CORRECTED: FY2023 previously showed the FY2023 Pillar 3 disclosure's UK LIQ1 table's Dec-23 quarter-end point-in-time snapshot (HQLA 1,441,255; net cash outflows 374,177; LCR 385%) rather than that same document's own UK KM1 summary table average-of-4-quarters figure used for every other year - corrected to the average basis (HQLA 1,189,319; net cash outflows 325,606; LCR 365%) for consistency across all 5 years. The FY2021 Pillar 3 report does not contain a comparable LCR key-metrics disclosure. FY2017/FY2018/FY2019 LCR figures are OakNorth's own 30-day, point-in-time (year-end) ratio, sourced from the FY2018 and FY2019 Pillar 3 reports' Liquidity risk sections - a different, less-smoothed basis than the FY2022+ average-of-4-quarters figures (FY2019's own report separately discloses a quarterly average of 395%, closer to the later years' basis, shown here only in this note for comparability). FY2020's own Pillar 3 report discloses liquidity buffer £469.4m, net cash outflows £139.1m, and a 30-day LCR of 338% (the FY2021 report repeats the LCR comparative as 338%); these are now populated. FY2015/FY2016 report only the year-end HQLA amount (£53.2m / £51.7m respectively) with no LCR ratio - the UK LCR minimum only began binding from October 2015 and the Bank's earliest reports do not yet present the ratio numerically.")
metric("NSFR", "£'000 / %", [
    ("Total available stable funding", {"FY2025": 6855628, "FY2024": 6303663, "FY2023": 4831446, "FY2022": 3748427, "FY2021": "Not disclosed", "FY2020": "Not disclosed", "FY2019": "Not disclosed", "FY2018": "Not disclosed", "FY2017": "Not disclosed", "FY2016": "Not disclosed", "FY2015": "Not disclosed"}),
    ("Total required stable funding", {"FY2025": 3608230, "FY2024": 3324269, "FY2023": 2993447, "FY2022": 2436946, "FY2021": "Not disclosed", "FY2020": "Not disclosed", "FY2019": "Not disclosed", "FY2018": "Not disclosed", "FY2017": "Not disclosed", "FY2016": "Not disclosed", "FY2015": "Not disclosed"}),
    ("Net Stable Funding Ratio", {"FY2025": "190%", "FY2024": "190%", "FY2023": "161%", "FY2022": "154%", "FY2021": "Not publicly disclosed", "FY2020": "Not publicly disclosed", "FY2019": "Not publicly disclosed", "FY2018": "Not publicly disclosed", "FY2017": "Not publicly disclosed", "FY2016": "Not publicly disclosed", "FY2015": "Not publicly disclosed"}),
], note="UK NSFR disclosures began from 1 January 2022; no NSFR disclosure exists in any of OakNorth's FY2015-FY2021 Pillar 3 reports (NSFR is mentioned only qualitatively, as one of several ratios monitored internally by the ALCO, with no published figure).")
metric("MREL Ratio", None, [("MREL ratio", {y: "Not publicly disclosed" for y in YEARS})], note="No MREL ratio is presented in OakNorth's five annual Pillar 3 disclosures. This is a documented non-disclosure, not a zero.")

bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {"FY2025": 7856889, "FY2024": 7573159, "FY2023": 5810647, "FY2022": 4657420, "FY2021": 3570311, "FY2020": 3116216, "FY2019": 2729924, "FY2018": 1770807, "FY2017": 768587, "FY2016": 291922, "FY2015": 94771}),
        ("Loans and advances to customers", {"FY2025": 4889874, "FY2024": 4393100, "FY2023": 3817344, "FY2022": 3127950, "FY2021": 2886305, "FY2020": 2492249, "FY2019": 2062985, "FY2018": 1297937, "FY2017": 604937, "FY2016": 225508, "FY2015": 14906}),
        ("Customer deposits", {"FY2025": 6513248, "FY2024": 6103046, "FY2023": 4639352, "FY2022": 3613260, "FY2021": 2643603, "FY2020": 2313628, "FY2019": 1986639, "FY2018": 1185860, "FY2017": 491261, "FY2016": 202397, "FY2015": 10939}),
        ("Total equity", {"FY2025": 1067530, "FY2024": 1019581, "FY2023": 885130, "FY2022": 744385, "FY2021": 629318, "FY2020": 528677, "FY2019": 470106, "FY2018": 330413, "FY2017": 253829, "FY2016": 81361, "FY2015": 82951}),
    ],
    balance_sheet_unit="£'000",
    income_statement_totals=[
        ("Net interest and fee income", {"FY2025": 318047, "FY2024": 309851, "FY2023": 296779, "FY2022": 221090, "FY2021": 176190, "FY2020": 140116, "FY2019": 104341, "FY2018": 60078, "FY2017": 28271, "FY2016": 7667, "FY2015": 160}),
        ("Operating expenses and provisions", {"FY2025": -95518, "FY2024": -95057, "FY2023": -109446, "FY2022": -68754, "FY2021": -41650, "FY2020": -62533, "FY2019": -38475, "FY2018": -26224, "FY2017": -17691, "FY2016": -10088, "FY2015": -2447}),
        ("Profit for the year", {"FY2025": 165211, "FY2024": 159334, "FY2023": 138470, "FY2022": 113259, "FY2021": 100392, "FY2020": 58534, "FY2019": 49976, "FY2018": 26580, "FY2017": 9474, "FY2016": -2421, "FY2015": -2287}),
    ],
    income_statement_unit="£'000",
    equity_changes_totals=[
        ("Opening equity", {"FY2025": 1019581, "FY2024": 885130, "FY2023": 744385, "FY2022": 629318, "FY2021": 528677, "FY2020": 470106, "FY2019": 330413, "FY2018": 253829, "FY2017": 81361, "FY2016": 82951, "FY2015": 925}),
        ("Total comprehensive income for the year", {"FY2025": 167974, "FY2024": 154296, "FY2023": 140707, "FY2022": 113038, "FY2021": 100637, "FY2020": 58558, "FY2019": 49998, "FY2018": 26561, "FY2017": 9447, "FY2016": -2414, "FY2015": -2294}),
        ("Other equity movements, net", {"FY2025": -120025, "FY2024": -19845, "FY2023": 38, "FY2022": 2029, "FY2021": 4, "FY2020": 13, "FY2019": 89695, "FY2018": 50023, "FY2017": 163021, "FY2016": 824, "FY2015": 84320}),
        ("Closing equity", {"FY2025": 1067530, "FY2024": 1019581, "FY2023": 885130, "FY2022": 744385, "FY2021": 629318, "FY2020": 528677, "FY2019": 470106, "FY2018": 330413, "FY2017": 253829, "FY2016": 81361, "FY2015": 82951}),
    ],
    equity_changes_unit="£'000",
    cash_flow_totals=[
        ("Net cash flows generated from operating activities", {"FY2025": 117717, "FY2024": 1071146, "FY2023": 443437, "FY2022": 833221, "FY2021": 41609, "FY2020": -40465, "FY2019": 104179, "FY2018": 32748, "FY2017": -67623, "FY2016": -14036, "FY2015": -4061}),
        ("Net cash flows from/(used in) investing activities", {"FY2025": -199308, "FY2024": 5341, "FY2023": 5418, "FY2022": -25277, "FY2021": -60343, "FY2020": -25286, "FY2019": -725, "FY2018": -103088, "FY2017": -2011, "FY2016": 51981, "FY2015": -56506}),
        ("Net cash flows from/(used in) financing activities", {"FY2025": -343239, "FY2024": 109608, "FY2023": -19099, "FY2022": -6499, "FY2021": 14136, "FY2020": -4591, "FY2019": 84604, "FY2018": 279877, "FY2017": 163000, "FY2016": 820, "FY2015": 84320}),
        ("Cash and cash equivalents at end of year", {"FY2025": 2468732, "FY2024": 2888497, "FY2023": 1702560, "FY2022": 1273218, "FY2021": 476393, "FY2020": 480991, "FY2019": 551333, "FY2018": 363275, "FY2017": 153702, "FY2016": 60336, "FY2015": 21571}),
    ],
    cash_flow_unit="£'000",
    ratios=[
        ("CET1 Ratio", {"FY2025": "15.5%", "FY2024": "17.3%", "FY2023": "18.6%", "FY2022": "18.7%", "FY2021": "20.5%", "FY2020": "20.0%", "FY2019": "20.7%", "FY2018": "22.4%", "FY2017": "34.8%", "FY2016": "26.5%", "FY2015": "153.8%"}),
        ("Tier 1 Ratio", {"FY2025": "15.5%", "FY2024": "17.3%", "FY2023": "18.6%", "FY2022": "18.7%", "FY2021": "20.5%", "FY2020": "20.0%", "FY2019": "20.7%", "FY2018": "22.4%", "FY2017": "34.8%", "FY2016": "26.5%", "FY2015": "153.8%"}),
        ("Total Capital Ratio", {"FY2025": "18.4%", "FY2024": "20.5%", "FY2023": "19.3%", "FY2022": "20.1%", "FY2021": "22.1%", "FY2020": "21.9%", "FY2019": "22.9%", "FY2018": "26.2%", "FY2017": "35.1%", "FY2016": "26.9%", "FY2015": "154.0%"}),
        ("Leverage Ratio", {"FY2025": "16.0%", "FY2024": "18.1%", "FY2023": "19.1%", "FY2022": "14.5%", "FY2021": "21.4%", "FY2020": "21.0%", "FY2019": "22.2%", "FY2018": "25.2%", "FY2017": "41.0%", "FY2016": "Not disclosed", "FY2015": "Not disclosed"}),
        ("LCR", {"FY2025": "478%", "FY2024": "489%", "FY2023": "365%", "FY2022": "351%", "FY2021": "Not disclosed", "FY2020": "338%", "FY2019": "377%", "FY2018": "490%", "FY2017": "713%", "FY2016": "Not disclosed", "FY2015": "Not disclosed"}),
        ("NSFR", {"FY2025": "190%", "FY2024": "190%", "FY2023": "161%", "FY2022": "154%", "FY2021": "Not disclosed", "FY2020": "Not disclosed", "FY2019": "Not disclosed", "FY2018": "Not disclosed", "FY2017": "Not disclosed", "FY2016": "Not disclosed", "FY2015": "Not disclosed"}),
    ],
    note="OakNorth's official Pillar 3 archive is annual, so no interim/14th worksheet is added. FY2023's LCR "
         "figures were corrected during the ST-028 rollout to use the average-of-4-quarters basis consistent with "
         "every other year - see the LCR sheet's own note for detail. HD-021 extended the year range back to "
         "FY2015 (OakNorth's confirmed historical floor - the year of its first full annual accounts after "
         "receiving its banking licence in March 2015). The Leverage Ratio row uses the UK-framework "
         "excluding-central-banks basis where available (FY2017-FY2025); FY2015-FY2016 only disclosed a single "
         "leverage measure (which is not excluding-central-banks) so are marked not disclosed on this row rather "
         "than mixing bases - see the Leverage Ratio sheet's own note for the including-central-banks figures "
         "those two years did disclose (87.1% and 25.5% respectively).",
)

bw.save("/Users/armaan/code/katalysis/banks/OAKNORTH BANK FINANCIALS.xlsx")
