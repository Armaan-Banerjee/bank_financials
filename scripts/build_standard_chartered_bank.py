import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook


# STANDARD CHARTERED BANK (ZC000018 / FRN 114276)
# The annual reports provide distinct Group and Company columns.  Cash-flow
# values below are the standalone Bank Company column.
#
# The regulatory sheets use a different basis, deliberately.  The annual
# reports' own capital disclosures are for Standard Chartered Bank Group, and
# those are NOT imported here.  What is imported, as of 2026-09-15, is the
# solo-consolidation section of Standard Chartered PLC's Pillar 3 reports: the
# PRA sets this entity's capital requirements on a solo-consolidated basis (the
# Company plus four named subsidiaries), and that section discloses this entity
# under the full UK templates.  It is this entity's own regulatory basis, not a
# parent's consolidated figures standing in for it.  See SOLO_BASIS_NOTE.

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021", "FY2020", "FY2019", "FY2018"]
YEAR_LABEL = {y: y for y in YEARS}

REPORTS = {
    "FY2025": "https://www.sc.com/en/uploads/sites/66/content/docs/sc-bank-2025-report.pdf",
    "FY2024": "https://www.sc.com/en/uploads/sites/66/content/docs/sc-bank-2024-results.pdf",
    "FY2023": "https://www.sc.com/EN/uploads/sites/66/content/docs/sc-bank-2023-annual-report.pdf",
    "FY2022": "https://www.sc.com/en/uploads/sites/66/content/docs/sc-bank-2022-annual-report.pdf",
    "FY2021": "https://www.sc.com/EN/uploads/sites/66/content/docs/sc-bank-2021-results.pdf",
    # FY2020-FY2018 added 2026-10-07.  Each is Standard Chartered Bank's OWN
    # Directors' Report and Financial Statements, not a Standard Chartered PLC
    # document; each was fetched from sc.com and verified by HTTP status,
    # Content-Type (application/pdf) and %PDF magic bytes.
    "FY2020": "https://www.sc.com/en/uploads/sites/66/content/docs/sc-bank-2020-results.pdf",
    "FY2019": "https://www.sc.com/en/uploads/sites/66/content/docs/SC-Bank-Financial-Statements-full-year-2019.pdf",
    "FY2018": "https://www.sc.com/en/uploads/sites/66/content/docs/uk-directors-report-2018.pdf",
}
CH_URL = "https://find-and-update.company-information.service.gov.uk/company/ZC000018/filing-history"

# ---------------------------------------------------------------------------
# NO BANK-LEVEL REGULATORY DISCLOSURE EXISTS BEFORE FY2021 (established
# 2026-10-07 by reading the editions themselves, not by a failed search).
#
# This workbook's regulatory basis is SOLO CONSOLIDATION - the PRA's own basis
# for this entity.  The solo-consolidation annex first appears in the FY2022
# Pillar 3 edition, which carries a single prior-year comparative column
# (FY2021).  The FY2021, FY2020, FY2019 and FY2018 editions were each
# downloaded from sc.com (status, Content-Type and %PDF checked) and read:
#
#   FY2021 (146pp)  Annex 1 "Standard Chartered Significant Subsidiaries"
#                   DOES carry a Standard Chartered Bank column (Tables 99-108)
#                   - but on the SCB GROUP CONSOLIDATED basis, not solo.  The
#                   narrative above Table 100 says "Tables 100 to 108 summarise
#                   the CONSOLIDATED capital position of Standard Chartered
#                   Bank", and footnote 1 to Table 99 says it "aligns with the
#                   capital section of the 2021 Standard Chartered Bank
#                   Accounts".  Its FY2021 total RWA is 193,988 $m against
#                   142,161 $m on the solo-consolidated basis this workbook
#                   uses.  The word "solo" appears ONCE in the entire edition,
#                   in the IMA permission list on p.82.
#   FY2020 (145pp)  No solo section AND no significant-subsidiaries capital
#                   annex at all.
#   FY2019 (138pp)  Same.
#   FY2018 (118pp)  Same; "Solo" appears only in the VaR backtesting narrative.
#
# So for FY2020 and earlier there is no Bank-level capital, leverage, liquidity
# or RWA disclosure on ANY basis this workbook may use.  Every pre-FY2021 cell
# on the 11 Pillar 3 metric sheets, the KM1 sheet and the RWA Breakdown sheet
# is therefore a STATEMENT.  Standard Chartered PLC GROUP figures have NOT been
# substituted for any of them.
# ---------------------------------------------------------------------------
P3_EDITION_URLS = {
    "FY2021": "https://www.sc.com/en/uploads/sites/66/content/docs/Standard_Chartered_PLC_Pillar3_Full_Year_2021_Report.pdf",
    "FY2020": "https://www.sc.com/en/uploads/sites/66/content/docs/standard-chartered-plc-full-year-2020-pillar3-disclosure.pdf",
    "FY2019": "https://www.sc.com/en/uploads/sites/66/content/docs/standard-chartered-plc-full-year-2019-pillar3.pdf",
    "FY2018": "https://www.sc.com/en/uploads/sites/66/content/docs/Standard_Chartered_PLC_Pillar3_Full_Year_2018_Report.pdf",
}

NO_SOLO = {
    "FY2020": "Not published – SC PLC Full Year 2020 Pillar 3 Disclosure, whole 145-page edition read: "
              "Pillar 3 FY2020 has no solo-consolidation/Bank-level section; only SC PLC group figures",
    "FY2019": "Not published – SC PLC Full Year 2019 Pillar 3 Disclosure, whole 138-page edition read: "
              "Pillar 3 FY2019 has no solo-consolidation/Bank-level section; only SC PLC group figures",
    "FY2018": "Not published – SC PLC Full Year 2018 Pillar 3 Disclosure, whole 118-page edition read: "
              "Pillar 3 FY2018 has no solo-consolidation/Bank-level section; only SC PLC group figures",
}

PRE_FY2021_SOURCES = (
    "FY2020, FY2019 AND FY2018 ON THIS SHEET ARE STATEMENTS, NOT GAPS (established 2026-10-07). The basis this "
    "sheet uses - Standard Chartered Bank on the solo-consolidated basis - is disclosed only from the FY2022 "
    "Pillar 3 edition onward, and that edition's single comparative column (FY2021) is the oldest solo figure "
    "that exists. The FY2021, FY2020, FY2019 and FY2018 editions were each downloaded from sc.com (HTTP status, "
    "Content-Type and %PDF magic bytes verified) and read end to end:\n"
    "FY2021 edition - " + P3_EDITION_URLS["FY2021"] + "\n"
    "FY2020 edition - " + P3_EDITION_URLS["FY2020"] + "\n"
    "FY2019 edition - " + P3_EDITION_URLS["FY2019"] + "\n"
    "FY2018 edition - " + P3_EDITION_URLS["FY2018"] + "\n\n"
    "WHAT THE FY2021 EDITION ACTUALLY CONTAINS, AND WHY IT CANNOT FILL THESE CELLS. Its Annex 1 'Standard "
    "Chartered Significant Subsidiaries' does carry a Standard Chartered Bank column (Table 99 capital resources, "
    "Tables 100-108, Table 109 overview of RWA, Table 110 leverage), with a 2020 comparative. But that column is "
    "the SCB GROUP CONSOLIDATED basis, not solo consolidation: the narrative above Table 100 states 'Tables 100 to "
    "108 summarise the CONSOLIDATED capital position of Standard Chartered Bank', and footnote 1 to Table 99 "
    "states that the column 'aligns with the capital section of the 2021 Standard Chartered Bank Accounts'. Its "
    "FY2021 total RWA is 193,988 $m and FY2020 187,901 $m, against 142,161 $m for FY2021 on the solo-consolidated "
    "basis carried elsewhere on this sheet - three different perimeters, not three measurements of one. Importing "
    "it would mix bases inside a single row, which this workbook does not do. The FY2020, FY2019 and FY2018 "
    "editions have no significant-subsidiaries capital annex at all.\n\n"
    "NO STANDARD CHARTERED PLC GROUP FIGURE HAS BEEN SUBSTITUTED for any of these years, on this sheet or any "
    "other."
)

ENTITY_NOTE = (
    "ENTITY AND BASIS: Standard Chartered Bank (Companies House Royal Charter reference ZC000018, FRN 114276) "
    "is incorporated in England with limited liability by Royal Charter 1853. The source reports distinguish "
    "Standard Chartered Bank Group (the Bank and subsidiaries) from Standard Chartered Bank Company (the "
    "standalone legal entity). All cash-flow rows in this workbook use the Company column only."
)

REGULATORY_GAP_NOTE = (
    "REGULATORY BASIS: no standalone Company KM1 series exists, because the PRA sets this entity's capital "
    "requirements on a SOLO-CONSOLIDATED basis - the Company plus four subsidiaries (Standard Chartered Holdings "
    "(International) B.V., Standard Chartered Grindlays Pty Limited, SCMB Overseas Limited and Corrasi Covered "
    "Bonds LLP). The Pillar 3 metric sheets and the RWA Breakdown sheet in this workbook therefore carry "
    "solo-consolidated figures, taken from the solo-consolidation section of Standard Chartered PLC's Pillar 3 "
    "reports (added 2026-09-15). Standard Chartered PLC GROUP figures are a different and much larger basis and "
    "have NOT been substituted anywhere. The balance sheet, cash flow, equity and asset quality sheets remain on "
    "the standalone Company basis, so figures must not be divided across the two."
)

SOURCE_NOTE = (
    "Sources - standalone Standard Chartered Bank Company cash flows, $million:\n"
    "FY2025: Directors' Report and Financial Statements 2025, cash flow statement p.89 - " + REPORTS["FY2025"] + "\n"
    "FY2024: Directors' Report and Financial Statements 2024, cash flow statement p.89 - " + REPORTS["FY2024"] + "\n"
    "FY2023: Directors' Report and Financial Statements 2023, cash flow statements p.165 - " + REPORTS["FY2023"] + "\n"
    "FY2022: Directors' Report and Financial Statements 2022, cash flow statements p.172 - " + REPORTS["FY2022"] + "\n"
    "FY2021: Directors' Report and Financial Statements 2021, cash flow statements p.172 - " + REPORTS["FY2021"] + "\n"
    "FY2020: Directors' Report and Financial Statements 2020, Cash flow statement p.168 - " + REPORTS["FY2020"] + "\n"
    "FY2019: Directors' Report and Financial Statements 2019, Cash flow statement p.154 - " + REPORTS["FY2019"] + "\n"
    "FY2018: Directors' Report and Financial Statements 2018, Cash flow statement p.191 - " + REPORTS["FY2018"] + "\n"
    "Entity filing history and identity: Companies House ZC000018 - " + CH_URL + "\n\n" + ENTITY_NOTE
)

BACKFILL_NOTE = (
    "FY2020, FY2019 AND FY2018 ADDED 2026-10-07. Each year is taken from Standard Chartered Bank's OWN Directors' "
    "Report and Financial Statements for that year - its own primary document, not a later edition's comparative "
    "column - and from the Company column, on the same basis as FY2021-FY2025. Every figure was read off a "
    "rendered page image. sc.com publishes the Bank's own accounts only back to FY2018 (uk-directors-report-2018."
    "pdf); a Wayback CDX prefix sweep of the sc.com document directory returns no earlier edition, so the "
    "workbook stops at FY2018 rather than reaching further on a comparative column.\n\n"
    "THE 2019 GROUP REORGANISATION IS A REAL DISCONTINUITY, NOT A DATA ERROR. Standard Chartered PLC reorganised "
    "in 2019 and Standard Chartered Bank transferred out a large part of its business; the Bank's own 2019 "
    "accounts record a dividend declared as a result of Group restructuring of $6,987m and a loss from "
    "discontinued operations of $4,573m. FY2018 therefore covers a materially larger entity than FY2019 onward, "
    "and the two are NOT like-for-like. Each year is carried as that year's own report printed it; nothing has "
    "been restated or rebased to make the series look continuous.\n\n"
    "RESTATEMENTS ACROSS EDITIONS, RECORDED AND NOT RECONCILED. (1) The 2020 report restates the 2019 Company "
    "column, labelling it 'restated 2019', for a reversal of impairment in subsidiary undertakings: +$612m to "
    "retained earnings, total assets and investments in subsidiary undertakings at 31 December 2019 (of which "
    "+$388m at 31 December 2018 and +$224m in 2019 profit). FY2019 above carries the 2019 report's own "
    "as-reported column (total assets 388,141; total equity 30,102) and not the 2020 report's restated one "
    "(388,753; 30,714). (2) The 2021 report opens its Company equity roll-forward at 1 January 2020 with a "
    "further +$81m, described in its own footnote as a 'correction of fair value hedge accounting adjustment'. "
    "FY2020 above carries the 2020 report's own column (total equity 28,460), not the 2021 report's restated "
    "28,541. Both versions of each year are stated here; neither has been adjusted toward the other, and this is "
    "the same treatment the sheet already gives the FY2022 cash-flow restatement."
)

bw = BankWorkbook(
    bank_name="Standard Chartered Bank (standalone Company basis)",
    years=YEARS,
    year_label=YEAR_LABEL,
    header_color="005A70",
)

# Company column only.  FY2022 uses the 2022 report's own as-reported figures;
# the 2023 report restated the FY2022 comparative, so the discontinuity is
# documented in the source note below.
CF = {
    "Profit before taxation": {"FY2025": 3245, "FY2024": 3058, "FY2023": 3088, "FY2022": 2996, "FY2021": 2496, "FY2020": 255, "FY2019": 1260, "FY2018": 179},
    "Adjustments for non-cash items and other adjustments": {"FY2025": -429, "FY2024": -1, "FY2023": -790, "FY2022": 381, "FY2021": -659, "FY2020": 1462, "FY2019": 2405, "FY2018": 1346},
    "Change in operating assets": {"FY2025": 273, "FY2024": -26161, "FY2023": 23104, "FY2022": -5451, "FY2021": -1178, "FY2020": -3622, "FY2019": 27141, "FY2018": -11804},
    "Change in operating liabilities": {"FY2025": 11452, "FY2024": 13864, "FY2023": -13891, "FY2022": 4521, "FY2021": 18902, "FY2020": 13290, "FY2019": -33457, "FY2018": 26942},
    "Contributions to defined benefit schemes": {"FY2025": -46, "FY2024": -39, "FY2023": -46, "FY2022": -36, "FY2021": -82, "FY2020": -75, "FY2019": -93, "FY2018": -90},
    "UK and overseas taxes paid": {"FY2025": -711, "FY2024": -720, "FY2023": -658, "FY2022": -359, "FY2021": -274, "FY2020": -418, "FY2019": -697, "FY2018": -230},
    "Net cash from/(used in) operating activities": {"FY2025": 13784, "FY2024": -9999, "FY2023": 10807, "FY2022": 2052, "FY2021": 19205, "FY2020": 10892, "FY2019": -3441, "FY2018": 16343},
    # No "Internally generated capitalised software" line exists in the FY2020,
    # FY2019 or FY2018 statements - the line is introduced later - so those
    # years are blank here rather than zero.
    "Internally generated capitalised software": {"FY2025": -521, "FY2024": -246, "FY2023": -378, "FY2022": -501, "FY2021": -503},
    "Purchase of property, plant and equipment": {"FY2025": -149, "FY2024": -176, "FY2023": -53, "FY2022": -59, "FY2021": -67, "FY2020": -69, "FY2019": -74, "FY2018": -49},
    "Disposal of property, plant and equipment": {"FY2025": 3, "FY2024": 15, "FY2023": 1, "FY2022": 14, "FY2021": 6, "FY2020": 20, "FY2019": 9, "FY2018": 2},
    "Acquisition of investment in subsidiaries, associates and joint ventures, net of cash acquired": {"FY2020": 0, "FY2019": 0, "FY2018": -596},
    "Dividends received from subsidiaries, associates and joint ventures": {"FY2025": 1260, "FY2024": 1052, "FY2023": 2060, "FY2022": 1046, "FY2021": 1626, "FY2020": 403, "FY2019": 0, "FY2018": 941},
    "Disposals of subsidiaries, associates and joint ventures / held-for-sale assets": {"FY2025": 0, "FY2024": 26, "FY2023": 108, "FY2022": 0, "FY2021": 0, "FY2020": 1281, "FY2019": 0, "FY2018": 5},
    "Purchase of investment securities": {"FY2025": -68809, "FY2024": -84630, "FY2023": -91970, "FY2022": -114671, "FY2021": -131168, "FY2020": -139256, "FY2019": -112413, "FY2018": -119676},
    "Disposal and maturity of investment securities": {"FY2025": 72962, "FY2024": 91907, "FY2023": 97216, "FY2022": 98999, "FY2021": 113905, "FY2020": 141611, "FY2019": 104913, "FY2018": 110368},
    "Net cash from/(used in) investing activities": {"FY2025": 4746, "FY2024": 7948, "FY2023": 6984, "FY2022": -15172, "FY2021": -16201, "FY2020": 3990, "FY2019": -7565, "FY2018": -9005},
    # FY2018 predates IFRS 16: the 2018 statement has no lease-liability line.
    "Premises and equipment lease liability principal payment": {"FY2025": -42, "FY2024": -43, "FY2023": -45, "FY2022": -78, "FY2021": -72, "FY2020": -92, "FY2019": -155},
    "Issue of ordinary and preference share capital, net of expenses": {"FY2025": 0, "FY2024": 0, "FY2023": 0, "FY2022": 0, "FY2021": 1273, "FY2020": 300},
    "Cancellation of shares including share buyback": {"FY2025": 0, "FY2024": 0, "FY2023": -750, "FY2022": 0, "FY2021": 0},
    "Issue of Additional Tier 1 capital, net of expenses": {"FY2025": 0, "FY2024": 980, "FY2023": 992, "FY2022": 1000, "FY2021": 2750, "FY2018": 0},
    "Redemption of Tier 1 capital": {"FY2025": 0, "FY2024": 0, "FY2023": -1000, "FY2022": -999, "FY2021": -1042, "FY2020": -2000},
    "Gross proceeds from issue of subordinated liabilities": {"FY2025": 0, "FY2024": 0, "FY2023": 0, "FY2022": 750, "FY2021": 0, "FY2020": 4630, "FY2019": 1000},
    "Interest paid on subordinated liabilities": {"FY2025": -492, "FY2024": -528, "FY2023": -583, "FY2022": -378, "FY2021": -456, "FY2020": -480, "FY2019": -1629, "FY2018": -584},
    "Repayment of subordinated liabilities": {"FY2025": -2173, "FY2024": -1000, "FY2023": -2160, "FY2022": -1008, "FY2021": -16, "FY2020": -2869, "FY2019": -1000, "FY2018": -2162},
    "Proceeds from issue of senior debts": {"FY2025": 2455, "FY2024": 3114, "FY2023": 4820, "FY2022": 4091, "FY2021": 660, "FY2020": 650, "FY2019": 431, "FY2018": 3765},
    "Repayment of senior debts": {"FY2025": -3986, "FY2024": -2471, "FY2023": -1806, "FY2022": -298, "FY2021": -422, "FY2020": -577, "FY2019": -1736, "FY2018": -2781},
    "Interest paid on senior debts": {"FY2025": -374, "FY2024": -282, "FY2023": -235, "FY2022": -1, "FY2021": -16, "FY2020": -14, "FY2019": -45, "FY2018": -128},
    "Distributions and dividends paid to preference shareholders and AT1 securities": {"FY2025": -389, "FY2024": -349, "FY2023": -363, "FY2022": -311, "FY2021": -292, "FY2020": -458, "FY2019": -441, "FY2018": -438},
    "Dividends paid to ordinary shareholders": {"FY2025": -2276, "FY2024": -2395, "FY2023": -2599, "FY2022": -575, "FY2021": -1511, "FY2020": 0, "FY2019": -3403, "FY2018": -384},
    "Net cash used in financing activities": {"FY2025": -7277, "FY2024": -2974, "FY2023": -3729, "FY2022": 2193, "FY2021": 856, "FY2020": -910, "FY2019": -6978, "FY2018": -2712},
    "Net increase/(decrease) in cash and cash equivalents": {"FY2025": 11253, "FY2024": -5025, "FY2023": 14062, "FY2022": -10927, "FY2021": 3860, "FY2020": 13972, "FY2019": -17984, "FY2018": 4626},
    "Cash and cash equivalents at beginning of year": {"FY2025": 48101, "FY2024": 53988, "FY2023": 40264, "FY2022": 59406, "FY2021": 56151, "FY2020": 41873, "FY2019": 59904, "FY2018": 55832},
    "Effect of exchange rate movements on cash and cash equivalents": {"FY2025": -64, "FY2024": -862, "FY2023": -338, "FY2022": -861, "FY2021": -605, "FY2020": 306, "FY2019": -47, "FY2018": -554},
    "Cash and cash equivalents at end of year": {"FY2025": 59290, "FY2024": 48101, "FY2023": 53988, "FY2022": 47618, "FY2021": 59406, "FY2020": 56151, "FY2019": 41873, "FY2018": 59904},
}

cash_rows = []
for label in list(CF):
    if label == "Profit before taxation":
        cash_rows.append(("SECTION", "Cash flows from operating activities", {}))
    elif label == "Internally generated capitalised software":
        cash_rows.append(("SECTION", "Cash flows from investing activities", {}))
    elif label == "Premises and equipment lease liability principal payment":
        cash_rows.append(("SECTION", "Cash flows from financing activities", {}))
    elif label == "Net increase/(decrease) in cash and cash equivalents":
        cash_rows.append(("SECTION", "Cash and cash equivalents reconciliation", {}))
    kind = "TOTAL" if label.startswith("Net cash") or label.startswith("Cash and cash") or label.startswith("Net increase") else "DATA"
    cash_rows.append((kind, label, CF[label]))

STATEMENT_REPORTS_NOTE = (
    "Statement sources - standalone Standard Chartered Bank Company balance sheet and equity, Group income "
    "statement (see note below), $million:\n"
    "FY2025/FY2024: Directors' Report and Financial Statements 2025, Balance sheets p.86, Cash flow statement p.88, "
    "Company statement of changes in equity p.89, Consolidated income statement p.84 - " + REPORTS["FY2025"] + "\n"
    "FY2023/FY2022: Directors' Report and Financial Statements 2023, Consolidated balance sheet p.162, Company "
    "statement of changes in equity p.165, Consolidated income statement p.160 - " + REPORTS["FY2023"] + "\n"
    "FY2021: Directors' Report and Financial Statements 2021, Consolidated balance sheet p.169, Company statement "
    "of changes in equity p.172, Consolidated income statement p.167 - " + REPORTS["FY2021"] + "\n"
    "FY2020: Directors' Report and Financial Statements 2020, Consolidated balance sheet p.166, Consolidated "
    "income statement p.164, Consolidated statement of comprehensive income p.165, Company statement of changes "
    "in equity p.169 - " + REPORTS["FY2020"] + "\n"
    "FY2019: Directors' Report and Financial Statements 2019, Consolidated balance sheet p.152, Consolidated "
    "income statement p.150, Consolidated statement of comprehensive income p.151, Company statement of changes "
    "in equity p.155 - " + REPORTS["FY2019"] + "\n"
    "FY2018: Directors' Report and Financial Statements 2018, Consolidated balance sheet p.189, Consolidated "
    "income statement p.187, Consolidated statement of comprehensive income p.188 - " + REPORTS["FY2018"] + "\n"
    "Entity filing history and identity: Companies House ZC000018 - " + CH_URL + "\n\n" + ENTITY_NOTE
    + "\n\n" + BACKFILL_NOTE
)

INCOME_STATEMENT_NOTE = (
    "The Company has taken advantage of the exemption in section 408 of the Companies Act 2006 not to present its "
    "individual income statement/statement of comprehensive income. This Profit & Loss sheet therefore uses the "
    "Bank GROUP consolidated income statement (not the Company column used on the Balance Sheet/Equity sheets). "
    "The Company's own profit after tax (disclosed as a single figure in each year's balance sheet note) was: "
    "FY2025 $2,517m, FY2024 $2,325m, FY2023 $2,585m, FY2022 $2,372m, FY2021 $2,146m, FY2020 a LOSS of $141m, "
    "FY2019 $654m and FY2018 a LOSS of $568m - these tie exactly to the 'Profit/(loss) for the year' rows on the "
    "Statement of Changes in Equity sheet (Company basis), confirming the two sheets are internally consistent "
    "despite using different consolidation bases. (The 2020 report restates the Company's 2019 profit after tax "
    "to $878m, +$224m, for the reversal of impairment in subsidiary undertakings; the $654m above is the 2019 "
    "report's own figure and both are recorded.)"
)

# --- Balance Sheet (Company column) ---------------------------------------
BS = {
    "Cash and balances at central banks": {"FY2025": 52348, "FY2024": 45233, "FY2023": 52758, "FY2022": 38867, "FY2021": 48165, "FY2020": 46476, "FY2019": 34734, "FY2018": 44749},
    "Financial assets held at fair value through profit or loss": {"FY2025": 99894, "FY2024": 88349, "FY2023": 86412, "FY2022": 75792, "FY2021": 99705, "FY2020": 80626, "FY2019": 74835, "FY2018": 71650},
    "Derivative financial instruments (assets)": {"FY2025": 66631, "FY2024": 82844, "FY2023": 53221, "FY2022": 65481, "FY2021": 53478, "FY2020": 68910, "FY2019": 48524, "FY2018": 46930},
    "Loans and advances to banks": {"FY2025": 11108, "FY2024": 11755, "FY2023": 10135, "FY2022": 18548, "FY2021": 16117, "FY2020": 14997, "FY2019": 22265, "FY2018": 23732},
    "Loans and advances to customers": {"FY2025": 80091, "FY2024": 77597, "FY2023": 75883, "FY2022": 80611, "FY2021": 71161, "FY2020": 72969, "FY2019": 76845, "FY2018": 77282},
    "Investment securities": {"FY2025": 79684, "FY2024": 82101, "FY2023": 92771, "FY2022": 95372, "FY2021": 86389, "FY2020": 71102, "FY2019": 71841, "FY2018": 63983},
    "Other assets": {"FY2025": 23568, "FY2024": 21552, "FY2023": 21742, "FY2022": 31715, "FY2021": 25688, "FY2020": 28896, "FY2019": 22288, "FY2018": 21631},
    "Due from subsidiary undertakings and other related parties": {"FY2025": 11538, "FY2024": 10066, "FY2023": 10053, "FY2022": 13214, "FY2021": 10741, "FY2020": 10885, "FY2019": 21926, "FY2018": 12025},
    "Current tax assets": {"FY2025": 412, "FY2024": 516, "FY2023": 395, "FY2022": 347, "FY2021": 487, "FY2020": 605, "FY2019": 326, "FY2018": 284},
    "Prepayments and accrued income": {"FY2025": 1392, "FY2024": 1535, "FY2023": 1386, "FY2022": 1598, "FY2021": 905, "FY2020": 958, "FY2019": 1387, "FY2018": 1322},
    # Printed as a dash in the Company column of the FY2020 and FY2019 reports
    # (so carried as 0); the line is dropped from the Company column entirely
    # from FY2021 onward, hence the blanks.
    "Interests in associates and joint ventures": {"FY2020": 0, "FY2019": 0, "FY2018": 839},
    "Investments in subsidiary undertakings": {"FY2025": 10800, "FY2024": 10671, "FY2023": 10066, "FY2022": 10300, "FY2021": 9694, "FY2020": 8258, "FY2019": 8615, "FY2018": 13598},
    "Goodwill and intangible assets": {"FY2025": 2245, "FY2024": 1988, "FY2023": 2359, "FY2022": 2279, "FY2021": 2121, "FY2020": 1958, "FY2019": 2117, "FY2018": 2673},
    "Property, plant and equipment": {"FY2025": 714, "FY2024": 659, "FY2023": 521, "FY2022": 430, "FY2021": 627, "FY2020": 708, "FY2019": 814, "FY2018": 320},
    "Deferred tax assets": {"FY2025": 251, "FY2024": 233, "FY2023": 379, "FY2022": 579, "FY2021": 508, "FY2020": 486, "FY2019": 714, "FY2018": 665},
    "Retirement benefit schemes in surplus": {"FY2025": 104, "FY2024": 118},
    "Assets classified as held for sale": {"FY2025": 240, "FY2024": 474, "FY2023": 68, "FY2022": 592, "FY2021": 91, "FY2020": 89, "FY2019": 910, "FY2018": 43655},
    "Total assets": {"FY2025": 441020, "FY2024": 435691, "FY2023": 418149, "FY2022": 435725, "FY2021": 425877, "FY2020": 407923, "FY2019": 388141, "FY2018": 425338},
    "Deposits by banks": {"FY2025": 20607, "FY2024": 17824, "FY2023": 18280, "FY2022": 17900, "FY2021": 18870, "FY2020": 18482, "FY2019": 19232, "FY2018": 22434},
    "Customer accounts": {"FY2025": 132018, "FY2024": 119502, "FY2023": 121648, "FY2022": 137422, "FY2021": 135478, "FY2020": 122061, "FY2019": 124032, "FY2018": 120890},
    "Repurchase agreements and other similar secured borrowing": {"FY2025": 4828, "FY2024": 9845, "FY2023": 11977, "FY2022": 1723, "FY2021": 283, "FY2020": 0, "FY2019": 178, "FY2018": 434},
    "Financial liabilities held at fair value through profit or loss": {"FY2025": 64880, "FY2024": 61683, "FY2023": 64467, "FY2022": 66189, "FY2021": 73902, "FY2020": 59101, "FY2019": 57415, "FY2018": 51059},
    "Derivative financial instruments (liabilities)": {"FY2025": 67556, "FY2024": 82745, "FY2023": 55531, "FY2022": 69203, "FY2021": 53835, "FY2020": 68423, "FY2019": 48447, "FY2018": 46668},
    "Debt securities in issue": {"FY2025": 37849, "FY2024": 36081, "FY2023": 34740, "FY2022": 34992, "FY2021": 33826, "FY2020": 27661, "FY2019": 30748, "FY2018": 23898},
    "Other liabilities": {"FY2025": 19421, "FY2024": 21486, "FY2023": 19213, "FY2022": 20990, "FY2021": 20460, "FY2020": 23515, "FY2019": 18810, "FY2018": 21183},
    "Due to parent companies, subsidiary undertakings & other related parties": {"FY2025": 50980, "FY2024": 42313, "FY2023": 47317, "FY2022": 39933, "FY2021": 40745, "FY2020": 43012, "FY2019": 43357, "FY2018": 40697},
    "Current tax liabilities": {"FY2025": 254, "FY2024": 294, "FY2023": 188, "FY2022": 329, "FY2021": 168, "FY2020": 250, "FY2019": 259, "FY2018": 265},
    "Accruals and deferred income": {"FY2025": 2620, "FY2024": 2441, "FY2023": 2453, "FY2022": 2140, "FY2021": 1550, "FY2020": 1411, "FY2019": 1747, "FY2018": 1970},
    "Subordinated liabilities and other borrowed funds": {"FY2025": 8158, "FY2024": 9801, "FY2023": 10896, "FY2022": 12729, "FY2021": 14076, "FY2020": 14339, "FY2019": 12489, "FY2018": 12467},
    "Deferred tax liabilities": {"FY2025": 358, "FY2024": 308, "FY2023": 477, "FY2022": 486, "FY2021": 583, "FY2020": 505, "FY2019": 435, "FY2018": 410},
    "Provisions for liabilities and charges": {"FY2025": 191, "FY2024": 186, "FY2023": 171, "FY2022": 249, "FY2021": 298, "FY2020": 336, "FY2019": 498, "FY2018": 1375},
    "Retirement benefit obligations (net deficit)": {"FY2025": 216, "FY2024": 200, "FY2023": 133, "FY2022": 124, "FY2021": 156, "FY2020": 367, "FY2019": 383, "FY2018": 324},
    "Liabilities included in disposal groups held for sale": {"FY2025": 150, "FY2020": 0, "FY2019": 9, "FY2018": 43649},
    "Total liabilities": {"FY2025": 410086, "FY2024": 404709, "FY2023": 387496, "FY2022": 404754, "FY2021": 394230, "FY2020": 379463, "FY2019": 358039, "FY2018": 387723},
    "Share capital and share premium account": {"FY2025": 21643, "FY2024": 21643, "FY2023": 21643, "FY2022": 22393, "FY2021": 22393, "FY2020": 21120, "FY2019": 20820, "FY2018": 28320},
    "Other reserves": {"FY2025": -3666, "FY2024": -3804, "FY2023": -3403, "FY2022": -4252, "FY2021": -2089, "FY2020": -1736, "FY2019": -1906, "FY2018": -1702},
    "Retained earnings": {"FY2025": 7235, "FY2024": 7421, "FY2023": 7671, "FY2022": 8080, "FY2021": 6594, "FY2020": 6076, "FY2019": 6188, "FY2018": 5997},
    "Total parent company shareholders' equity": {"FY2025": 25212, "FY2024": 25260, "FY2023": 25911, "FY2022": 26221, "FY2021": 26898, "FY2020": 25460, "FY2019": 25102, "FY2018": 32615},
    "Other equity instruments": {"FY2025": 5722, "FY2024": 5722, "FY2023": 4742, "FY2022": 4750, "FY2021": 4749, "FY2020": 3000, "FY2019": 5000, "FY2018": 5000},
    "Total equity": {"FY2025": 30934, "FY2024": 30982, "FY2023": 30653, "FY2022": 30971, "FY2021": 31647, "FY2020": 28460, "FY2019": 30102, "FY2018": 37615},
    "Total equity and liabilities": {"FY2025": 441020, "FY2024": 435691, "FY2023": 418149, "FY2022": 435725, "FY2021": 425877, "FY2020": 407923, "FY2019": 388141, "FY2018": 425338},
}

bs_rows = []
for label in list(BS):
    if label == "Cash and balances at central banks":
        bs_rows.append(("SECTION", "Assets", {}))
    elif label == "Deposits by banks":
        bs_rows.append(("SECTION", "Liabilities", {}))
    elif label == "Share capital and share premium account":
        bs_rows.append(("SECTION", "Equity", {}))
    kind = "TOTAL" if label in (
        "Total assets", "Total liabilities", "Total parent company shareholders' equity",
        "Total equity", "Total equity and liabilities",
    ) else "DATA"
    bs_rows.append((kind, label, BS[label]))

bw.add_balance_sheet_sheet(
    title="Standard Chartered Bank — Balance Sheet",
    subtitle="Standalone Bank Company column (Consolidated balance sheet/'Balance sheets' statement), $million.",
    rows=bs_rows,
    sources_text=STATEMENT_REPORTS_NOTE + "\n\nNote: 'Retirement benefit schemes in surplus' is only reported as a "
    "separate asset line from FY2024 onward; earlier years' reports show only a net retirement benefit "
    "obligations/deficit liability. 'Liabilities included in disposal groups held for sale' is reported in FY2018, "
    "FY2019 and FY2020 (a printed dash, carried as 0, in FY2020), then not as a line at all in FY2021-FY2024, then "
    "again in FY2025. 'Interests in associates and joint ventures' carries a Company figure only at FY2018 (839); "
    "the FY2019 and FY2020 reports print a dash in the Company column (carried as 0) and later editions drop the "
    "line from the Company column altogether.\n\n"
    "FY2018 IS A MUCH LARGER ENTITY. Total assets fall from 425,338 at FY2018 to 388,141 at FY2019 and the "
    "held-for-sale blocks swing from 43,655 of assets and 43,649 of liabilities at FY2018 to 910 and 9 at FY2019: "
    "that is the 2019 Standard Chartered PLC group reorganisation, in which this Bank transferred out a large part "
    "of its business, not a trading movement. Share capital falls 28,320 -> 20,820 across the same break because "
    "the Bank cancelled 7,500 of shares in 2019.",
    first_col_width=68,
    source_height=260,
    unit_suffix=" ($m)",
)

# --- Profit & Loss (Group consolidated - see INCOME_STATEMENT_NOTE) -------
PL = {
    "Interest income": {"FY2025": 16888, "FY2024": 19310, "FY2023": 18380, "FY2022": 9765, "FY2021": 6185, "FY2020": 7807, "FY2019": 10831, "FY2018": 17285},
    "Interest expense": {"FY2025": -13173, "FY2024": -14910, "FY2023": -13773, "FY2022": -5314, "FY2021": -2133, "FY2020": -3707, "FY2019": -6360, "FY2018": -8221},
    "Net interest income": {"FY2025": 3715, "FY2024": 4400, "FY2023": 4607, "FY2022": 4451, "FY2021": 4052, "FY2020": 4100, "FY2019": 4471, "FY2018": 9064},
    "Fees and commission income": {"FY2025": 3957, "FY2024": 3486, "FY2023": 3094, "FY2022": 2863, "FY2021": 2972, "FY2020": 2601, "FY2019": 2752, "FY2018": 4062},
    "Fees and commission expense": {"FY2025": -1031, "FY2024": -824, "FY2023": -656, "FY2022": -709, "FY2021": -576, "FY2020": -596, "FY2019": -416, "FY2018": -649},
    "Net fee and commission income": {"FY2025": 2926, "FY2024": 2662, "FY2023": 2438, "FY2022": 2154, "FY2021": 2396, "FY2020": 2005, "FY2019": 2336, "FY2018": 3413},
    "Net trading income": {"FY2025": 6185, "FY2024": 5530, "FY2023": 4100, "FY2022": 3743, "FY2021": 2280, "FY2020": 2606, "FY2019": 2384, "FY2018": 1814},
    "Other operating income": {"FY2025": 128, "FY2024": -178, "FY2023": 404, "FY2022": -114, "FY2021": 132, "FY2020": 525, "FY2019": 187, "FY2018": 649},
    "Operating income": {"FY2025": 12954, "FY2024": 12414, "FY2023": 11549, "FY2022": 10234, "FY2021": 8860, "FY2020": 9236, "FY2019": 9378, "FY2018": 14940},
    "Staff costs": {"FY2025": -6773, "FY2024": -6417, "FY2023": -6286, "FY2022": -5748, "FY2021": -5591, "FY2020": -5128, "FY2019": -5245, "FY2018": -7062},
    "Premises costs": {"FY2025": -267, "FY2024": -254, "FY2023": -241, "FY2022": -228, "FY2021": -224, "FY2020": -249, "FY2019": -249, "FY2018": -772},
    "General administrative expenses": {"FY2025": -194, "FY2024": -223, "FY2023": 27, "FY2022": -75, "FY2021": -71, "FY2020": -414, "FY2019": -858, "FY2018": -2857},
    "Depreciation and amortisation": {"FY2025": -721, "FY2024": -656, "FY2023": -647, "FY2022": -611, "FY2021": -594, "FY2020": -672, "FY2019": -629, "FY2018": -812},
    "Operating expenses": {"FY2025": -7955, "FY2024": -7550, "FY2023": -7147, "FY2022": -6662, "FY2021": -6480, "FY2020": -6463, "FY2019": -6981, "FY2018": -11503},
    "Operating profit before impairment losses and taxation": {"FY2025": 4999, "FY2024": 4864, "FY2023": 4402, "FY2022": 3572, "FY2021": 2380, "FY2020": 2773, "FY2019": 2397, "FY2018": 3437},
    "Credit impairment": {"FY2025": -248, "FY2024": -15, "FY2023": 58, "FY2022": 22, "FY2021": 30, "FY2020": -1976, "FY2019": -699, "FY2018": -653},
    "Goodwill, property, plant and equipment and other impairment": {"FY2025": -29, "FY2024": -410, "FY2023": -42, "FY2022": -107, "FY2021": -30, "FY2020": -262, "FY2019": -34, "FY2018": -164},
    "Profit/(loss) from associates and joint ventures": {"FY2025": 2, "FY2024": 8, "FY2023": -4, "FY2022": -13, "FY2021": 1, "FY2020": 1, "FY2019": 55, "FY2018": 238},
    "Profit before taxation": {"FY2025": 4724, "FY2024": 4447, "FY2023": 4414, "FY2022": 3474, "FY2021": 2381, "FY2020": 536, "FY2019": 1719, "FY2018": 2858},
    "Taxation": {"FY2025": -1314, "FY2024": -1465, "FY2023": -1177, "FY2022": -1122, "FY2021": -743, "FY2020": -514, "FY2019": -796, "FY2018": -1447},
    # Continuing/discontinued split is presented only in the FY2019 and FY2020
    # statements (the 2019 group reorganisation).  Blank elsewhere: FY2021
    # onward do not present it, and the FY2018 statement predates it.
    "Profit for the year from continuing operations": {"FY2020": 22, "FY2019": 923},
    "(Loss)/profit from discontinued operations": {"FY2020": 0, "FY2019": -4573},
    "Profit for the year": {"FY2025": 3410, "FY2024": 2982, "FY2023": 3237, "FY2022": 2352, "FY2021": 1638, "FY2020": 22, "FY2019": -3650, "FY2018": 1411},
    "Other comprehensive income/(loss), net of taxation": {"FY2025": 908, "FY2024": -476, "FY2023": 362, "FY2022": -2766, "FY2021": -599, "FY2020": 266, "FY2019": -376, "FY2018": -811},
    "Other comprehensive income/(loss) from discontinued operations": {"FY2020": 0, "FY2019": 1345},
    "Total comprehensive income/(loss) for the year": {"FY2025": 4318, "FY2024": 2506, "FY2023": 3599, "FY2022": -414, "FY2021": 1039, "FY2020": 288, "FY2019": -2681, "FY2018": 600},
}

pl_rows = []
for label in list(PL):
    if label == "Interest income":
        pl_rows.append(("SECTION", "Income", {}))
    elif label == "Staff costs":
        pl_rows.append(("SECTION", "Operating expenses", {}))
    elif label == "Other comprehensive income/(loss), net of taxation":
        pl_rows.append(("SECTION", "Other comprehensive income", {}))
    kind = "TOTAL" if label in (
        "Net interest income", "Net fee and commission income", "Operating income", "Operating expenses",
        "Operating profit before impairment losses and taxation", "Profit before taxation", "Profit for the year",
        "Total comprehensive income/(loss) for the year",
    ) else "DATA"
    pl_rows.append((kind, label, PL[label]))

PL_BACKFILL_NOTE = (
    "FY2020, FY2019 AND FY2018 ON THIS SHEET. All three are the Bank GROUP consolidated income statement, the same "
    "basis as FY2021-FY2025, read off the rendered pages of the Bank's own reports named above.\n\n"
    "FY2019 AND FY2020 SPLIT CONTINUING FROM DISCONTINUED OPERATIONS; FY2018 AND FY2021 ONWARD DO NOT. Two rows "
    "were added so this is visible rather than implied. In the FY2019 column every line from 'Interest income' "
    "down to 'Taxation' is CONTINUING operations only: profit before taxation 1,719 and taxation (796) give 923 "
    "from continuing operations, and the statutory result for the year is a LOSS of 3,650 after a 4,573 loss from "
    "discontinued operations. The same is true of the FY2020 column, where discontinued operations are a printed "
    "dash, so 22 is both the continuing and the statutory figure. Do not read the FY2019 'Profit before taxation' "
    "as comparable with the FY2018 one.\n\n"
    "FY2018 IS THE 2018 REPORT'S OWN AS-REPORTED PRESENTATION, which still includes the businesses later "
    "classified as discontinued. The 2019 report restates the same 2018 year for discontinued operations to: "
    "operating income 8,925, operating expenses (7,830), profit before taxation 519, taxation (1,058), loss from "
    "continuing operations (539), profit from discontinued operations 1,950. Only 'Profit for the year' (1,411) "
    "and 'Total comprehensive income' (600) are common to both presentations and are unchanged by the "
    "restatement. BOTH are recorded here and neither is reconciled to the other; the FY2018 column carries the "
    "2018 report's own figures, consistent with every other year on this sheet. The fall in operating income from "
    "14,940 at FY2018 to 9,378 at FY2019 is overwhelmingly the reorganisation, not trading.\n\n"
    "EDITION DISAGREEMENT AT FY2019, RECORDED NOT RECONCILED. The 2019 report prints 'Other comprehensive loss "
    "for the year from continuing operations' as (376) and 'Total comprehensive (loss)/income for the year' as "
    "(2,681). The 2020 report's 2019 comparative column prints the same two lines as (377) and (2,682). The "
    "FY2019 column above carries the 2019 report's own figures. The $1m difference is the documents', not a "
    "transcription slip, and is not adjusted away.\n\n"
    "LABEL DRIFT. The FY2020 statement calls the impairment line 'Goodwill and other impairment' and the FY2018 "
    "statement splits it into 'Goodwill' (a printed dash at FY2018) and 'Other' (164); the FY2019 statement "
    "splits it into 'Goodwill impairment' (23) and 'Other impairment' (11), and the (34) carried for FY2019 above "
    "is the combined figure AS PRINTED in the 2020 report's 2019 comparative column, not a sum struck here."
)

bw.add_income_statement_sheet(
    title="Standard Chartered Bank — Profit & Loss",
    subtitle="Bank GROUP consolidated income statement, $million - see source note (Company has no standalone P&L).",
    rows=pl_rows,
    sources_text=STATEMENT_REPORTS_NOTE + "\n\n" + INCOME_STATEMENT_NOTE + "\n\n" + PL_BACKFILL_NOTE,
    first_col_width=68,
    source_height=300,
    unit_suffix=" ($m)",
)

# --- Statement of Changes in Equity (Company column, chronological) -------
EQ_HEADERS = [
    "Share capital and share premium account", "Capital and merger reserves", "Own credit adjustment reserve",
    "FVOCI reserve - debt", "FVOCI reserve - equity", "Cash flow hedge reserve", "Translation reserve",
    "Retained earnings", "Parent company shareholders' equity", "Other equity instruments", "Total equity",
]

equity_rows = [
    # --- 2018 movement year (2019 report, Company SOCIE, printed p.155) -----
    ("TOTAL", "Balance at 1 January 2018", (28320, 40, 52, -77, 52, -43, -1384, 7413, 34373, 5000, 39373)),
    ("DATA", "Loss for the year", (None, None, None, None, None, None, None, -568, -568, None, -568)),
    ("DATA", "Other comprehensive income/(loss), net of tax", (None, None, 270, -112, -5, 1, -496, 26, -316, None, -316)),
    ("DATA", "Share option expense, net of taxation", (None, None, None, None, None, None, None, 139, 139, None, 139)),
    ("DATA", "Dividends on ordinary shares", (None, None, None, None, None, None, None, -384, -384, None, -384)),
    ("DATA", "Dividends on preference shares and AT1 securities", (None, None, None, None, None, None, None, -438, -438, None, -438)),
    ("DATA", "Deemed distribution to parent", (None, None, None, None, None, None, None, -191, -191, None, -191)),
    ("TOTAL", "Balance at 31 December 2018", (28320, 40, 322, -189, 47, -42, -1880, 5997, 32615, 5000, 37615)),
    # --- 2019 movement year (2019 report, Company SOCIE, printed p.155) -----
    ("DATA", "Profit for the year", (None, None, None, None, None, None, None, 654, 654, None, 654)),
    ("DATA", "Other comprehensive (loss)/income, net of tax", (None, None, -295, 217, 18, 15, -159, -139, -343, None, -343)),
    ("DATA", "Share option expense, net of taxation", (None, None, None, None, None, None, None, 97, 97, None, 97)),
    ("DATA", "Dividends on ordinary shares", (None, None, None, None, None, None, None, -393, -393, None, -393)),
    ("DATA", "Dividends on preference shares and AT1 securities", (None, None, None, None, None, None, None, -441, -441, None, -441)),
    ("DATA", "Dividends declared as a result of Group restructuring", (None, None, None, None, None, None, None, -6987, -6987, None, -6987)),
    ("DATA", "Deemed distribution to parent", (None, None, None, None, None, None, None, -100, -100, None, -100)),
    ("DATA", "Cancellation of shares", (-7500, None, None, None, None, None, None, 7500, None, None, None)),
    ("TOTAL", "Balance at 31 December 2019 (as reported in the 2019 report)", (20820, 40, 27, 28, 65, -27, -2039, 6188, 25102, 5000, 30102)),
    # --- Two printed prior-year restatements bridge the 2019 report's closing
    # balance to the 2021 report's opening balance.  Both amounts are printed
    # in the later reports' own footnotes; neither is computed here.
    ("DATA", "Restatement: reversal of impairment in subsidiary undertakings (2020 report, SOCIE note 1: +$612m at 31 December 2019)",
     (None, None, None, None, None, None, None, 612, 612, None, 612)),
    ("DATA", "Restatement: correction of fair value hedge accounting adjustment (2021 report, SOCIE note 2: +$81m)",
     (None, None, None, None, None, None, None, 81, 81, None, 81)),
    ("TOTAL", "Balance at 1 January 2020 (as restated in the 2021 report)", (20820, 40, 27, 28, 65, -27, -2039, 6881, 25795, 5000, 30795)),
    # --- 2020 movement year (2021 report, Company SOCIE, printed p.172) -----
    ("DATA", "Loss for the year", (None, None, None, None, None, None, None, -141, -141, None, -141)),
    ("DATA", "Other comprehensive income, net of tax", (None, None, -52, 140, 11, -5, -56, -4, 34, None, 34)),
    ("DATA", "Shares issued, net of expenses", (300, None, None, None, None, None, None, None, 300, None, 300)),
    ("DATA", "Redemption of other equity instruments", (None, None, None, None, None, None, None, None, None, -2000, -2000)),
    ("DATA", "Share option expenses", (None, None, None, None, None, None, None, 76, 76, None, 76)),
    ("DATA", "Dividends on preference shares and AT1 securities", (None, None, None, None, None, None, None, -458, -458, None, -458)),
    ("DATA", "Deemed distribution to parent", (None, None, None, None, None, None, None, -65, -65, None, -65)),
    ("DATA", "Other movements (FX reclass)", (None, None, None, None, None, None, 132, -132, None, None, None)),
    ("TOTAL", "Balance at 31 December 2020 (as restated in the 2021 report)", (21120, 40, -25, 168, 76, -32, -1963, 6157, 25541, 3000, 28541)),
    # --- 2021 movement year (2021 report, Company SOCIE, printed p.172) -----
    ("DATA", "Profit for the year", (None, None, None, None, None, None, None, 2146, 2146, None, 2146)),
    ("DATA", "Other comprehensive income/(loss), net of tax", (None, None, 26, -258, 72, -7, -186, 146, -207, None, -207)),
    ("DATA", "Shares issued, net of expenses", (1273, None, None, None, None, None, None, None, 1273, None, 1273)),
    ("DATA", "Other equity instruments issued, net of expenses", (None, None, None, None, None, None, None, None, None, 2750, 2750)),
    ("DATA", "Redemption of other equity instruments", (None, None, None, None, None, None, None, -41, -41, -1001, -1042)),
    ("DATA", "Share option expenses", (None, None, None, None, None, None, None, 86, 86, None, 86)),
    ("DATA", "Dividends on ordinary shares", (None, None, None, None, None, None, None, -1511, -1511, None, -1511)),
    ("DATA", "Dividends on preference shares and AT1 securities", (None, None, None, None, None, None, None, -292, -292, None, -292)),
    ("DATA", "Deemed distribution to parent", (None, None, None, None, None, None, None, -85, -85, None, -85)),
    ("DATA", "Other movements", (None, None, None, None, None, None, None, -12, -12, None, -12)),
    ("TOTAL", "Balance at 31 December 2021", (22393, 40, 1, -90, 148, -39, -2149, 6594, 26898, 4749, 31647)),
    # --- 2022 movement year (2022 report, Company SOCIE, printed p.172).
    # This whole block was MISSING before 2026-10-07; see the source note.
    ("DATA", "Profit for the year", (None, None, None, None, None, None, None, 2372, 2372, None, 2372)),
    ("DATA", "Other comprehensive (loss)/income, net of tax", (None, None, -25, -950, -1, -483, -704, 6, -2157, None, -2157)),
    ("DATA", "Other equity instruments issued, net of expenses", (None, None, None, None, None, None, None, None, None, 1000, 1000)),
    ("DATA", "Redemption of other equity instruments", (None, None, None, None, None, None, None, None, None, -999, -999)),
    ("DATA", "Share option expenses", (None, None, None, None, None, None, None, 98, 98, None, 98)),
    ("DATA", "Dividends on ordinary shares", (None, None, None, None, None, None, None, -575, -575, None, -575)),
    ("DATA", "Dividends on preference shares and AT1 securities", (None, None, None, None, None, None, None, -311, -311, None, -311)),
    ("DATA", "Deemed distribution to parent", (None, None, None, None, None, None, None, -104, -104, None, -104)),
    ("TOTAL", "Balance at 31 December 2022", (22393, 40, -24, -1040, 147, -522, -2853, 8080, 26221, 4750, 30971)),
    ("DATA", "Profit for the year", (None, None, None, None, None, None, None, 2585, 2585, None, 2585)),
    ("DATA", "Other comprehensive income/(loss), net of tax", (None, None, 73, 324, 67, 471, -86, -21, 828, None, 828)),
    ("DATA", "Other equity instruments issued, net of expenses", (None, None, None, None, None, None, None, None, None, 992, 992)),
    ("DATA", "Redemption of other equity instruments", (None, None, None, None, None, None, None, None, None, -1000, -1000)),
    ("DATA", "Share option expenses", (None, None, None, None, None, None, None, 114, 114, None, 114)),
    ("DATA", "Dividends on ordinary shares", (None, None, None, None, None, None, None, -2599, -2599, None, -2599)),
    ("DATA", "Dividends on preference shares and AT1 securities", (None, None, None, None, None, None, None, -363, -363, None, -363)),
    ("DATA", "Deemed distribution to parent", (None, None, None, None, None, None, None, -113, -113, None, -113)),
    ("DATA", "Share buyback (preference shares cancelled)", (-750, None, None, None, None, None, None, None, -750, None, -750)),
    ("DATA", "Other movements", (None, None, None, None, None, None, None, -12, -12, None, -12)),
    ("TOTAL", "Balance at 31 December 2023", (21643, 40, 49, -716, 214, -51, -2939, 7671, 25911, 4742, 30653)),
    ("DATA", "Profit for the year", (None, None, None, None, None, None, None, 2325, 2325, None, 2325)),
    ("DATA", "Other comprehensive (loss)/income, net of tax", (None, None, -291, 308, -83, 34, -326, 194, -164, None, -164)),
    ("DATA", "Other equity instruments issued, net of expenses", (None, None, None, None, None, None, None, None, None, 980, 980)),
    ("DATA", "Share option expenses", (None, None, None, None, None, None, None, 127, 127, None, 127)),
    ("DATA", "Dividends on ordinary shares", (None, None, None, None, None, None, None, -2395, -2395, None, -2395)),
    ("DATA", "Dividends on preference shares and AT1 securities", (None, None, None, None, None, None, None, -349, -349, None, -349)),
    ("DATA", "Deemed distribution to parent", (None, None, None, None, None, None, None, -144, -144, None, -144)),
    ("DATA", "Other movements", (None, None, -1, 7, None, None, -49, -8, -51, None, -51)),
    ("TOTAL", "Balance at 31 December 2024", (20893 + 750, 40, -243, -401, 131, -17, -3314, 7421, 25260, 5722, 30982)),
    ("DATA", "Profit for the year", (None, None, None, None, None, None, None, 2517, 2517, None, 2517)),
    # Retained-earnings component is 18, not 182: the 2025 report prints it as
    # "18" with a superscript footnote marker 2 ("18 2"), which was read as 182
    # before 2026-10-07.  With 18 the whole roll-forward closes on the printed
    # 31 December 2025 retained earnings of 7,235.
    ("DATA", "Other comprehensive (loss)/income, net of tax", (None, None, -64, 295, -7, 54, -140, 18, 156, None, 156)),
    ("DATA", "Share option expenses", (None, None, None, None, None, None, None, 135, 135, None, 135)),
    ("DATA", "Dividends on ordinary shares", (None, None, None, None, None, None, None, -2276, -2276, None, -2276)),
    ("DATA", "Dividends on preference shares and AT1 securities", (None, None, None, None, None, None, None, -389, -389, None, -389)),
    ("DATA", "Deemed distribution to parent", (None, None, None, None, None, None, None, -191, -191, None, -191)),
    ("TOTAL", "Balance at 31 December 2025", (21643, 40, -307, -106, 124, 37, -3454, 7235, 25212, 5722, 30934)),
]

bw.add_equity_changes_sheet(
    title="Standard Chartered Bank — Statement of Changes in Equity",
    subtitle="Standalone Bank Company column, chronological, $million.",
    headers=EQ_HEADERS,
    rows=equity_rows,
    sources_text=STATEMENT_REPORTS_NOTE + "\n\nNote: FY2025's report combines share capital/premium into a single "
    "'Ordinary' ($20,893m) + 'Preference' ($750m) column pair that were shown as one combined column in earlier "
    "reports - the FY2024 closing balance above (21,643) is the sum of both, consistent with prior years' single "
    "column. Zero undocumented plug rows: every movement traces to a named line in the source reports (profit or "
    "loss for the year, OCI, share/AT1 issuance and redemption, share option expense, dividends, deemed "
    "distributions to parent, the 2019 dividend declared as a result of Group restructuring and share "
    "cancellation, and the FY2023 preference share buyback/capital reduction).\n\n"
    "DEFECT FOUND AND CORRECTED, 2026-10-07 - READ THIS BEFORE COMPARING THIS SHEET WITH AN EARLIER COPY OF THE "
    "WORKBOOK. As built before that date this roll-forward was mis-stitched in two ways, and both are now fixed "
    "against the primary Company statements of changes in equity. (1) The block headed 'Balance at 1 January "
    "2021' -> 'Balance at 31 December 2021' was actually the 2020 movement year: its loss of 141 is the "
    "COMPANY'S 2020 loss after tax, printed on p.166 of the 2020 Bank report, and its closing row is the 2021 "
    "report's 'As at 31 December 2020'. (2) The block that followed (profit 2,146, shares issued 1,273, AT1 "
    "issued 2,750, redemption 1,042, dividends 1,511 and 292) is the 2021 movement year, but it was labelled as "
    "closing at 31 December 2022 and carried the FY2022 balance-sheet values. Rolled forward it gives retained "
    "earnings 6,594, other equity instruments 4,749 and total equity 31,647 - exactly the FY2021 Balance Sheet "
    "column - which is what the 'Balance at 31 December 2021' row above now shows. (3) Because of that shift "
    "there was NO block at all for the 2022 movement year: FY2022's Company profit of 2,372 appeared nowhere. "
    "That block has been added from the 2022 report's own Company SOCIE (printed p.172). The three closing "
    "balances from 31 December 2023 onward were, and remain, correct.\n\n"
    "WHICH REPORT EACH BLOCK COMES FROM: 2018 and 2019 movement years - 2019 report, Company statement of "
    "changes in equity, printed p.155; 2020 and 2021 - 2021 report, printed p.172; 2022 - 2022 report, printed "
    "p.172; 2023, 2024 and 2025 - the respective years' reports. Every figure was read off a rendered page image.\n\n"
    "TWO PRINTED RESTATEMENT ROWS BRIDGE 2019 TO 2020, AND THEY ARE NOT PLUGS. The 2019 report closes at total "
    "equity 30,102 while the 2021 report opens 1 January 2020 at 30,795. The 693 between them is two prior-period "
    "corrections, each stated in the later report's own footnote and each carried above as its own named row: "
    "+612 for the reversal of impairment in subsidiary undertakings (2020 report, SOCIE note 1 - 'an increase in "
    "retained earnings as at 31 December 2019 of $612 million', of which $388m at 31 December 2018 and $224m in "
    "2019 profit), and +81 'correction of fair value hedge accounting adjustment' (2021 report, SOCIE note 2). "
    "Showing both the as-reported and the restated balance records both documents rather than reconciling them.\n\n"
    "WHERE THIS SHEET AND THE BALANCE SHEET DIVERGE, AND WHY NEITHER HAS BEEN ADJUSTED. The closing balances at "
    "31 December 2018, 2019, 2021, 2022, 2023, 2024 and 2025 tie exactly to those years' Balance Sheet Total "
    "equity. FY2020 does not, by 81: the Balance Sheet carries the 2020 report's own as-reported 28,460 while "
    "this roll-forward necessarily continues on the 2021 report's restated chain and closes at 28,541. That is "
    "the fair-value-hedge correction above, created by the documents themselves. DO NOT reconcile it by editing "
    "either sheet.\n\n"
    "ONE-CELL TRANSCRIPTION ERROR ALSO CORRECTED, 2026-10-07. The 2025 movement year's 'Other comprehensive "
    "(loss)/income' row carried 182 in the retained-earnings column; the 2025 report (printed p.89) prints 18 "
    "there, with a superscript footnote marker 2 immediately after it, and the row's parent-company total of 156 "
    "is only consistent with 18 (the reserve components sum to 138). With 18 the roll-forward closes on the "
    "printed 31 December 2025 retained earnings of 7,235; with 182 it closed on 7,399, which is printed nowhere. "
    "Every 'Balance at' row on this sheet now ties column-for-column to the next one.",
    first_col_width=42,
    source_height=280,
    col_width=13,
)

bw.add_cash_flow_sheet(
    title="Standard Chartered Bank — Cash Flow Statement",
    subtitle="Standalone Bank Company column, $million; Group figures deliberately excluded.",
    rows=cash_rows,
    sources_text=SOURCE_NOTE + "\n\n" + REGULATORY_GAP_NOTE + "\n\nNote: the FY2023 report restates FY2022 cash-flow comparatives; FY2022 above preserves the FY2022 report's own as-reported Company figures."
    + "\n\n" + BACKFILL_NOTE + "\n\nLINE-ITEM AVAILABILITY IN THE OLDER STATEMENTS. 'Internally generated "
    "capitalised software' is not a line in the FY2020, FY2019 or FY2018 statements, so those cells are blank "
    "rather than zero. 'Premises and equipment lease liability principal payment' first appears at FY2019 (IFRS "
    "16), so FY2018 is blank. The FY2018 statement has no 'Gross proceeds from issue of subordinated liabilities' "
    "line and the FY2019 statement has no share-issue line, so those too are blank. One line that the older "
    "statements DO carry and the newer ones drop - 'Acquisition of investment in subsidiaries, associates and "
    "joint ventures, net of cash acquired' - has been added as its own row; it is 596 at FY2018 and a printed "
    "dash at FY2019 and FY2020. Printed dashes are carried as 0 throughout, the same treatment the rest of this "
    "workbook uses.\n\n"
    "CLOSING-TO-OPENING CHAIN CHECKS ACROSS THE NEW YEARS: FY2018 closes at 59,904 and FY2019 opens there; "
    "FY2019 closes at 41,873 and FY2020 opens there; FY2020 closes at 56,151 and FY2021 opens there. The "
    "FY2018-FY2020 columns are each from that year's own report, so these are three independent documents "
    "agreeing, not one document restated.",
    first_col_width=72,
    source_height=260,
    unit_suffix=" ($m)",
)

# --- Asset Quality (Company loans and advances to customers, IFRS 9 stage) -
AQ = {
    "Stage 1 - gross carrying amount": {"FY2025": 75255, "FY2024": 72697, "FY2023": 70343, "FY2022": 73476, "FY2021": 59760, "FY2020": 60252, "FY2019": 66728, "FY2018": 68277},
    "Stage 1 - expected credit loss": {"FY2025": -124, "FY2024": -116, "FY2023": -89, "FY2022": -148, "FY2021": -151, "FY2020": -188, "FY2019": -119, "FY2018": -151},
    "Stage 2 - gross carrying amount": {"FY2025": 3817, "FY2024": 4010, "FY2023": 4077, "FY2022": 5296, "FY2021": 9795, "FY2020": 10891, "FY2019": 8878, "FY2018": 7491},
    "Stage 2 - expected credit loss": {"FY2025": -112, "FY2024": -99, "FY2023": -80, "FY2022": -77, "FY2021": -235, "FY2020": -387, "FY2019": -147, "FY2018": -204},
    "Stage 3 - gross carrying amount (credit-impaired)": {"FY2025": 2697, "FY2024": 2685, "FY2023": 3761, "FY2022": 4685, "FY2021": 5019, "FY2020": 5993, "FY2019": 5211, "FY2018": 5002},
    "Stage 3 - expected credit loss": {"FY2025": -1442, "FY2024": -1580, "FY2023": -2129, "FY2022": -2621, "FY2021": -3027, "FY2020": -3592, "FY2019": -3706, "FY2018": -3133},
    "Total gross carrying amount": {"FY2025": 81769, "FY2024": 79392, "FY2023": 78181, "FY2022": 83457, "FY2021": 74574, "FY2020": 77136, "FY2019": 80817, "FY2018": 80770},
    "Total expected credit loss": {"FY2025": -1678, "FY2024": -1795, "FY2023": -2298, "FY2022": -2846, "FY2021": -3413, "FY2020": -4167, "FY2019": -3972, "FY2018": -3488},
    "Net carrying value (= Loans and advances to customers)": {"FY2025": 80091, "FY2024": 77597, "FY2023": 75883, "FY2022": 80611, "FY2021": 71161, "FY2020": 72969, "FY2019": 76845, "FY2018": 77282},
    "NPL ratio (Stage 3 gross / Total gross)": {"FY2025": "3.30%", "FY2024": "3.38%", "FY2023": "4.81%", "FY2022": "5.61%", "FY2021": "6.73%", "FY2020": "7.77%", "FY2019": "6.45%", "FY2018": "6.19%"},
    "Stage 3 coverage ratio (Stage 3 ECL / Stage 3 gross)": {"FY2025": "53.47%", "FY2024": "58.85%", "FY2023": "56.61%", "FY2022": "55.94%", "FY2021": "60.31%", "FY2020": "59.94%", "FY2019": "71.12%", "FY2018": "62.63%"},
}

aq_rows = []
for label in list(AQ):
    if label == "Stage 1 - gross carrying amount":
        aq_rows.append(("SECTION", "Loans and advances to customers (amortised cost) by IFRS 9 stage", {}))
    elif label == "NPL ratio (Stage 3 gross / Total gross)":
        aq_rows.append(("SECTION", "Derived ratios", {}))
    kind = "TOTAL" if label.startswith("Total") or label.startswith("Net carrying value") else "DATA"
    aq_rows.append((kind, label, AQ[label]))

bw.add_asset_quality_sheet(
    title="Standard Chartered Bank — Asset Quality",
    subtitle="Standalone Bank Company column, loans and advances to customers by IFRS 9 stage, $million.",
    rows=aq_rows,
    sources_text=STATEMENT_REPORTS_NOTE + "\n\nSource for stage tables: each year's Directors' Report and Financial "
    "Statements, Risk review and Capital review section, 'Analysis of financial instrument by stage' / 'All "
    "segments - Company' tables. Net carrying value ties exactly to the Balance Sheet's 'Loans and advances to "
    "customers' line every year. Only the on-balance-sheet loans and advances to customers line is shown here "
    "(cash, banks, debt securities, and off-balance-sheet commitments/guarantees also carry their own stage splits "
    "in the source reports but are outside this sheet's scope).\n\n"
    "FY2020, FY2019 AND FY2018 ADDED 2026-10-07, from the 'Loans and advances by client segment - Company' table "
    "in each year's own Bank report ('Customer Total' column): 2020 report printed p.66, 2019 report printed "
    "p.60, 2018 report printed p.69. Net carrying value ties exactly to that year's Balance Sheet 'Loans and "
    "advances to customers' in all three years (72,969 / 76,845 / 77,282), the same check the later years pass.\n"
    "The NPL and Stage 3 coverage ratios in the two rows above are DERIVED from the gross and ECL rows on this "
    "sheet, as they are for every other year; they are not lifted from the reports. For FY2020 and FY2018 the "
    "source happens to print its own Stage 3 cover ratio for the Customer Total column to one decimal place - "
    "59.9% and 62.6% - on the same definition, agreeing with the 59.94% and 62.63% derived here.\n"
    "FY2018 IS A LARGER ENTITY than FY2019 onward (the 2019 Group reorganisation), so the stage balances are not "
    "like-for-like across that break even though the loan book happens to be a similar size."
    ,
    first_col_width=58,
    source_height=260,
    unit_suffix=" ($m)",
)


def unavailable(name, note, cells=None):
    bw.add_metric_sheet(
        name,
        "$million / %",
        [(name + " — standalone Bank Company basis", cells or {y: "Not publicly disclosed" for y in YEARS})],
        SOURCE_NOTE + "\n\n" + REGULATORY_GAP_NOTE + "\n\n" + PRE_FY2021_SOURCES,
        note=note,
        first_col_width=58,
        source_height=230,
    )


# ---------------------------------------------------------------------------
# Standard Chartered Bank — SOLO CONSOLIDATION (the PRA's own basis for this
# entity).  Added 2026-09-15, replacing a "Not publicly disclosed" block.
#
# The earlier claim that no entity-level regulatory series existed was wrong.
# Standard Chartered PLC's annual Pillar 3 report carries a dedicated "Solo
# consolidation" section disclosing Standard Chartered Bank's own regulatory
# position under the full UK templates (UK CC1 own funds, UK LR2 leverage,
# UK LIQ1 LCR, UK LIQ2 NSFR).  Table 109 of the FY2023 edition lists it among
# the Group's significant subsidiaries with "Local Regulator: PRA".
#
# This is NOT a parent-group substitution.  The SCB Bank Report states:
# "Capital requirements are set by the PRA for Standard Chartered Bank on a
# solo consolidation basis. The solo-consolidated group differs from Standard
# Chartered Bank (Company) in that it includes the full consolidation of four
# subsidiaries, namely Standard Chartered Holdings (International) B.V.,
# Standard Chartered Grindlays PTY Limited, SCMB Overseas Limited and Corrasi
# Covered Bonds LLP."  Solo consolidation is a permission that widens the
# firm's own INDIVIDUAL prudential position; the perimeter is headed by this
# entity, not by Standard Chartered PLC.
#
# Entity distinctness is proved by the numbers: SC PLC group total RWA at
# FY2023 is 244,151 $m against 122,408 $m here.
# ---------------------------------------------------------------------------
SOLO = {
    "CET1 Capital":        {"FY2025": 14526, "FY2024": 14730, "FY2023": 14730, "FY2022": 14079, "FY2021": 16475},
    "CET1 Ratio":          {"FY2025": "11.1%", "FY2024": "11.7%", "FY2023": "12.0%", "FY2022": "10.7%", "FY2021": "11.6%"},
    "Tier 1 Capital":      {"FY2025": 18678, "FY2024": 19003, "FY2023": 18601, "FY2022": 18257, "FY2021": 21151},
    "Tier 1 Ratio":        {"FY2025": "14.3%", "FY2024": "15.0%", "FY2023": "15.2%", "FY2022": "13.9%", "FY2021": "14.9%"},
    "Total Capital":       {"FY2025": 24375, "FY2024": 27186, "FY2023": 27714, "FY2022": 29058, "FY2021": 32016},
    "Total Capital Ratio": {"FY2025": "18.7%", "FY2024": "21.5%", "FY2023": "22.6%", "FY2022": "22.1%", "FY2021": "22.5%"},
    "Total RWAs":          {"FY2025": 130608, "FY2024": 126383, "FY2023": 122408, "FY2022": 131175, "FY2021": 142161},
}

# FY2020 and earlier carry a statement, not a figure, on every regulatory
# sheet: no solo-consolidation (Bank-level) disclosure exists in any Pillar 3
# edition before FY2022's, whose oldest column is the FY2021 comparative above.
# See NO_SOLO and PRE_FY2021_SOURCES at the top of this file.
for _series in SOLO.values():
    _series.update(NO_SOLO)

P3_URLS = {
    "FY2025": "https://www.sc.com/en/uploads/sites/66/content/docs/standard-chartered-plc-full-year-2025-pillar3-disclosure.pdf",
    "FY2024": "https://www.sc.com/en/uploads/sites/66/content/docs/standard-chartered-plc-full-year-2024-pillar3-disclosure.pdf",
    "FY2023": "https://www.sc.com/en/uploads/sites/66/content/docs/standard_chartered_plc_pillar3_full_year_2023_report.pdf",
    "FY2022": "https://www.sc.com/en/uploads/sites/66/content/docs/standard_chartered_plc_pillar3_full_year_2022_report.pdf",
}

SOLO_SOURCES = (
    "SOLO-CONSOLIDATION REGULATORY SOURCES (added 2026-09-15). Each year is taken from that year's OWN Pillar 3 "
    "edition, and every year was additionally cross-checked against the following edition's comparative column:\n"
    "FY2025: Standard Chartered PLC Full Year 2025 Pillar 3 Disclosure, Table 109 'Composition of regulatory own "
    "funds (UK CC1) - Solo consolidation', rows 29/45/59/60/61/62/63 - " + P3_URLS["FY2025"] + "\n"
    "FY2024: Standard Chartered PLC Full Year 2024 Pillar 3 Disclosure, Table 113 (same UK CC1 solo template) - "
    + P3_URLS["FY2024"] + "\n"
    "FY2023: Standard Chartered PLC Full Year 2023 Pillar 3 Disclosure, Table 110 (same UK CC1 solo template) - "
    + P3_URLS["FY2023"] + "\n"
    "FY2022: Standard Chartered PLC Full Year 2022 Pillar 3 Disclosure, Table 106 (same UK CC1 solo template) - "
    + P3_URLS["FY2022"] + "\n"
    "FY2021: the FY2022 edition's 2021 comparative column (Table 106). The FY2021 Pillar 3 edition contains NO solo-"
    "consolidation section at all - the section was introduced in the FY2022 edition - so the comparative is the "
    "only source for that year.\n\n"
    "SOURCE DEFECT FOUND AND AVOIDED: the FY2025 edition's 2024 comparative column misprints the three capital "
    "RATIO rows, showing 12.0%/15.2%/22.6% - which are FY2023's ratios - against FY2024 amounts. Those ratios do "
    "not reconcile with the amounts printed beside them (14,730/126,383 = 11.7%, not 12.0%). FY2024's ratios here "
    "are taken from the FY2024 edition's own column (11.7%/15.0%/21.5%), which reconcile exactly and whose FY2023 "
    "comparative reproduces the FY2023 edition line for line. Do not 'correct' these to the FY2025 edition's "
    "comparative.\n\n"
    "ENTITY CHECK: Standard Chartered PLC group total RWA at FY2023 is 244,151 $m (group UK KM1) against 122,408 "
    "$m on this solo-consolidated basis, confirming these are the Bank entity's figures and not the listed "
    "parent's.\n\n" + PRE_FY2021_SOURCES
)

SOLO_BASIS_NOTE = (
    "BASIS: Standard Chartered Bank on the SOLO-CONSOLIDATED basis, which is the basis on which the PRA sets this "
    "entity's capital requirements. It comprises Standard Chartered Bank (Company) plus the full consolidation of "
    "four subsidiaries (Standard Chartered Holdings (International) B.V., Standard Chartered Grindlays PTY Limited, "
    "SCMB Overseas Limited and Corrasi Covered Bonds LLP). This is a regulatory perimeter headed by this entity, "
    "NOT the Standard Chartered PLC listed group. It is therefore a different basis from the Balance Sheet, Cash "
    "Flow and Statement of Changes in Equity sheets in this workbook, which use the narrower standalone Bank "
    "Company column - do not divide figures across the two bases."
)

# ---------------------------------------------------------------
# KM1 Key Metrics - NOT APPLICABLE for this entity, on affirmative evidence.
#
# The only UK KM1 template in the Standard Chartered document set belongs to
# Standard Chartered PLC, the listed GROUP, and that is a different and much
# larger entity: Table 1 of the FY2025 edition shows group RWEA of 258,031 $m
# against 130,608 $m on this entity's solo-consolidated basis. Substituting it
# would put a parent's consolidated figures in a subsidiary's workbook, which
# this project does not do.
#
# The solo-consolidation annex that DOES cover this entity publishes 18 UK
# templates, enumerated in the source note below, and KM1 is not among them.
# That is an absence established by reading what the annex contains, not by a
# failed search.
# ---------------------------------------------------------------
KM1_SOURCES = (
    "Sources - none for this entity. Standard Chartered Bank does not publish the UK KM1 key-metrics template "
    "on any basis, and the Standard Chartered PLC group KM1 has NOT been substituted for it.\n\n"
    "LATEST-EDITION CHECK, 2026-09-17: sc.com's own investor financial-results pages were read directly (HTTP "
    "200). The newest annual Pillar 3 is the Standard Chartered PLC Full Year 2025 Pillar 3 Disclosure, which "
    "this workbook already uses; a half-year 2026 Pillar 3 also exists and carries no solo KM1 either. Checked, "
    "none newer.\n\n"
    "WHAT WAS READ. The FY2025, FY2024, FY2023 and FY2022 editions were downloaded from sc.com and verified by "
    "HTTP status, Content-Type and %PDF magic bytes, as was the FY2021 edition. Each edition from FY2022 onward "
    "carries a solo-consolidation annex disclosing THIS entity under the UK templates: CC1, CC2, CCyB1, CCyB2, "
    "LR1, LR2, LR3, CR1, CR1-A, CR2, CQ1, CQ3, CQ4, CQ5, CR3, CR4, LIQ1, LIQ2 and the REM1-REM5 remuneration "
    "templates. UK KM1 is not among them in any of the four editions. The FY2021 edition has no solo-"
    "consolidation section at all - the section was introduced in the FY2022 edition - which is why this "
    "workbook's FY2021 metric figures come from the FY2022 edition's comparative column.\n\n"
    "WHY THE GROUP'S KM1 IS NOT USED. Each edition states its own scope in section 1.1: 'This report presents "
    "the annual Pillar 3 disclosures of Standard Chartered PLC (the Group)'. Its Table 1 UK KM1 is therefore the "
    "listed group's, on the consolidated basis: total RWEA 258,031 $m at 31 December 2025, against 130,608 $m "
    "for Standard Chartered Bank on the solo-consolidated basis on which the PRA actually sets this entity's "
    "capital requirements. The two are different entities and the gap between them is the proof - see "
    "SOLO_BASIS_NOTE on the metric sheets for the perimeter this workbook does use.\n\n"
    "THE NEAREST THING TO A KM1 FOR THIS ENTITY FAILS THE ROW-SET TEST. The group Pillar 3 does print a 'Capital "
    "resources of significant subsidiaries' table (Table 108 in the FY2025 edition) with a Standard Chartered "
    "solo-consolidation column, and this workbook takes its capital figures from that family of tables. But it "
    "is a short summary - own funds, RWAs and the three capital ratios - with no SREP rows (UK 7a-7d), no "
    "combined buffer block, no UK 11a overall capital requirement row, no leverage exposure measure and no LCR "
    "or NSFR rows. Mapping it onto KM1 row numbers would assert a correspondence Standard Chartered never "
    "published, so it is not done here. Every figure this workbook takes from those tables is on the individual "
    "Pillar 3 metric sheets and the RWA Breakdown sheet, where it belongs.\n\n"
    "This is therefore 'Pillar 3 is published but the template is not used at this entity level', not 'no "
    "Pillar 3 is published' and not a failed fetch."
)

bw.add_km1_sheet(
    title="Standard Chartered Bank — KM1 Key Metrics",
    subtitle="Not applicable — Standard Chartered Bank does not publish the UK KM1 key-metrics template on any "
             "basis. The solo-consolidation annex of Standard Chartered PLC's Pillar 3 reports, which is where "
             "this entity's own regulatory figures are disclosed, publishes 18 UK templates and KM1 is not one "
             "of them; the only KM1 in the document set is Standard Chartered PLC GROUP's, a different and much "
             "larger entity (258,031 $m of RWEA at 31 December 2025 against 130,608 $m here), and it has not "
             "been substituted. See the source note for what was read and for the entity evidence.",
    rows=[
        ("DATA", "UK KM1 key-metrics template",
         {**{y: "Not published at this entity level" for y in ("FY2025", "FY2024", "FY2023", "FY2022", "FY2021")},
          **{y: NO_SOLO[y].replace("Not published – ", "Not published – no KM1 and no Bank-level section. ")
             for y in ("FY2020", "FY2019", "FY2018")}}),
    ],
    sources_text=KM1_SOURCES + "\n\n" + PRE_FY2021_SOURCES,
    first_col_width=48,
    source_height=320,
)

for _metric, _unit in [
    ("CET1 Capital", "$million"), ("CET1 Ratio", "% of RWA"),
    ("Tier 1 Capital", "$million"), ("Tier 1 Ratio", "% of RWA"),
    ("Total Capital", "$million"), ("Total Capital Ratio", "% of RWA"),
    ("Total RWAs", "$million"),
]:
    bw.add_metric_sheet(
        _metric,
        _unit,
        [(_metric + " — solo-consolidated basis", SOLO[_metric])],
        SOLO_SOURCES,
        note=SOLO_BASIS_NOTE,
        first_col_width=58,
        source_height=300,
    )

# RWA breakdown, solo-consolidated basis.  Added 2026-09-15, replacing a
# "Not publicly disclosed" block.  The same Pillar 3 annex that carries the
# solo-consolidation capital templates also prints a full OV1-shaped RWA
# breakdown for this entity, in the "Overview of RWA - Significant
# Subsidiaries" table (named "Large Subsidiaries" in the FY2022 edition).
# Its first column is headed "Standard Chartered - Solo consolidation" with
# "Local Regulator: PRA", the same column heading used by the capital tables
# above.
RWA_BREAKDOWN = {
    "Credit risk (excluding CCR)":      {"FY2025": 65489, "FY2024": 65425, "FY2023": 66630, "FY2022": 74581, "FY2021": 89824},
    "Of which the standardised approach": {"FY2025": 13796, "FY2024": 11425, "FY2023": 11038, "FY2022": 10548, "FY2021": 18575},
    "Of which slotting approach":        {"FY2025": 2842, "FY2024": 2313, "FY2023": 1999, "FY2022": 2284, "FY2021": 2415},
    "Of which the advanced IRB (AIRB) approach": {"FY2025": 48851, "FY2024": 51688, "FY2023": 53593, "FY2022": 61749, "FY2021": 68834},
    "Counterparty credit risk (CCR)":    {"FY2025": 16773, "FY2024": 15638, "FY2023": 14087, "FY2022": 15888, "FY2021": 16384},
    "Of which the standardised approach (CCR)": {"FY2025": 2891, "FY2024": 2435, "FY2023": 2476, "FY2022": 2971, "FY2021": 2875},
    "Of which internal model method (IMM)": {"FY2025": 7840, "FY2024": 7798, "FY2023": 7080, "FY2022": 7436, "FY2021": 6340},
    "Of which exposures to a CCP":       {"FY2025": 1022, "FY2024": 717, "FY2023": 719, "FY2022": 688, "FY2021": 1009},
    "Of which credit valuation adjustment (CVA)": {"FY2025": 1639, "FY2024": 1824, "FY2023": 1381, "FY2022": 1961, "FY2021": 2890},
    "Of which other CCR":                {"FY2025": 3382, "FY2024": 2864, "FY2023": 2431, "FY2022": 2832, "FY2021": 3270},
    "Settlement risk":                   {"FY2025": 0, "FY2024": 0, "FY2023": 0, "FY2022": 6, "FY2021": 4},
    "Securitisation exposures in the banking book": {"FY2025": 3429, "FY2024": 3712, "FY2023": 4457, "FY2022": 4830, "FY2021": 3606},
    "Position, foreign exchange and commodities risks (Market risk)": {"FY2025": 22466, "FY2024": 21914, "FY2023": 18436, "FY2022": 17070, "FY2021": 18582},
    "Of which the standardised approach (market risk)": {"FY2025": 10859, "FY2024": 7905, "FY2023": 7077, "FY2022": 5664, "FY2021": 8039},
    "Of which IMA":                      {"FY2025": 11607, "FY2024": 14008, "FY2023": 11360, "FY2022": 11406, "FY2021": 10542},
    "Large exposures":                   {"FY2025": 0, "FY2024": 0, "FY2023": 0, "FY2022": 0, "FY2021": 0},
    "Operational risk":                  {"FY2025": 15632, "FY2024": 14258, "FY2023": 13045, "FY2022": 12880, "FY2021": 12701},
    "Amounts below the thresholds for deduction (subject to 250% risk weight)": {"FY2025": 6819, "FY2024": 5427, "FY2023": 5753, "FY2022": 5920, "FY2021": 1060},
    "Floor adjustment":                  {"FY2025": 0, "FY2024": 0, "FY2023": 0, "FY2022": 0, "FY2021": 0},
    "Total risk weighted assets":        {"FY2025": 130608, "FY2024": 126375, "FY2023": 122408, "FY2022": 131175, "FY2021": 142161},
}

# Same position as the capital sheets: no solo-consolidated RWA breakdown
# exists before the FY2022 Pillar 3 edition's FY2021 comparative column.
for _series in RWA_BREAKDOWN.values():
    _series.update(NO_SOLO)

RWA_BREAKDOWN_ROWS = [
    ("SECTION", "Credit risk", {}),
    ("DATA", "Credit risk (excluding CCR)", RWA_BREAKDOWN["Credit risk (excluding CCR)"]),
    ("DATA", "  of which: standardised approach", RWA_BREAKDOWN["Of which the standardised approach"]),
    ("DATA", "  of which: slotting approach", RWA_BREAKDOWN["Of which slotting approach"]),
    ("DATA", "  of which: advanced IRB (AIRB) approach", RWA_BREAKDOWN["Of which the advanced IRB (AIRB) approach"]),
    ("SECTION", "Counterparty credit risk", {}),
    ("DATA", "Counterparty credit risk (CCR)", RWA_BREAKDOWN["Counterparty credit risk (CCR)"]),
    ("DATA", "  of which: standardised approach", RWA_BREAKDOWN["Of which the standardised approach (CCR)"]),
    ("DATA", "  of which: internal model method (IMM)", RWA_BREAKDOWN["Of which internal model method (IMM)"]),
    ("DATA", "  of which: exposures to a CCP", RWA_BREAKDOWN["Of which exposures to a CCP"]),
    ("DATA", "  of which: credit valuation adjustment (CVA)", RWA_BREAKDOWN["Of which credit valuation adjustment (CVA)"]),
    ("DATA", "  of which: other CCR", RWA_BREAKDOWN["Of which other CCR"]),
    ("SECTION", "Other risk categories", {}),
    ("DATA", "Settlement risk", RWA_BREAKDOWN["Settlement risk"]),
    ("DATA", "Securitisation exposures in the banking book", RWA_BREAKDOWN["Securitisation exposures in the banking book"]),
    ("DATA", "Position, foreign exchange and commodities risks (Market risk)", RWA_BREAKDOWN["Position, foreign exchange and commodities risks (Market risk)"]),
    ("DATA", "  of which: standardised approach", RWA_BREAKDOWN["Of which the standardised approach (market risk)"]),
    ("DATA", "  of which: internal model approach (IMA)", RWA_BREAKDOWN["Of which IMA"]),
    ("DATA", "Large exposures", RWA_BREAKDOWN["Large exposures"]),
    ("DATA", "Operational risk", RWA_BREAKDOWN["Operational risk"]),
    ("DATA", "Amounts below the thresholds for deduction (subject to 250% risk weight)", RWA_BREAKDOWN["Amounts below the thresholds for deduction (subject to 250% risk weight)"]),
    ("DATA", "Floor adjustment", RWA_BREAKDOWN["Floor adjustment"]),
    ("TOTAL", "Total risk weighted assets", RWA_BREAKDOWN["Total risk weighted assets"]),
]

RWA_BREAKDOWN_SOURCES = (
    "SOLO-CONSOLIDATION RWA BREAKDOWN (added 2026-09-15, replacing a 'Not publicly disclosed' block). The same "
    "annex of Standard Chartered PLC's Pillar 3 report that carries this entity's capital templates also prints a "
    "full OV1-shaped RWA breakdown for it. In each edition the table's FIRST column is headed 'Standard Chartered "
    "- Solo consolidation' with 'Local Regulator: PRA' - the identical column heading used by the capital "
    "resources table - and the remaining columns are other significant subsidiaries (Standard Chartered Bank (HK) "
    "Ltd, Standard Chartered Bank Korea Ltd, Standard Chartered Bank (Singapore) Ltd), which are NOT used here.\n"
    "FY2025: Full Year 2025 Pillar 3 Disclosure, Table 132 'Overview of RWA - Significant Subsidiaries', 2025 "
    "column, p.147 - " + P3_URLS["FY2025"] + "\n"
    "FY2024: Full Year 2024 Pillar 3 Disclosure, Table 136 'Overview of RWA - Significant Subsidiaries', 2024 "
    "column, p.170 - " + P3_URLS["FY2024"] + "\n"
    "FY2023: Full Year 2023 Pillar 3 Disclosure, Table 133 'Overview of RWA - Significant Subsidiaries', 2023 "
    "column, p.168 - " + P3_URLS["FY2023"] + "\n"
    "FY2022: Full Year 2022 Pillar 3 Disclosure, Table 128 'Overview of RWA - Large Subsidiaries' (the table was "
    "renamed 'Significant Subsidiaries' from the FY2023 edition), 2022 column, p.132 - " + P3_URLS["FY2022"] + "\n"
    "FY2021: the FY2022 edition's 2021 comparative column (Table 128 continued). The FY2021 Pillar 3 edition has "
    "no solo-consolidation section at all, so this comparative is the only source for that year - the same "
    "position as the capital sheets.\n\n"
    "VALIDATION: every year's categories sum to that year's own printed total with no residual (FY2025 "
    "65,489+16,773+3,429+22,466+15,632+6,819 = 130,608; FY2023 = 122,408; FY2022 including 6 of settlement risk = "
    "131,175; FY2021 including 4 of settlement risk = 142,161). Four of the five totals also reproduce the Total "
    "RWAs sheet exactly.\n\n"
    "KNOWN 8 $M DIFFERENCE AT FY2024 - NOT AN ERROR IN EITHER SHEET. This sheet's FY2024 total is 126,375, while "
    "the Total RWAs sheet carries 126,383. Both figures are printed in the SAME FY2024 Pillar 3 edition, in two "
    "different tables: Table 112 'Capital resources of significant subsidiaries' (p.153) gives 126,383, and Table "
    "136 (this sheet's source, p.170) gives 126,375. The document itself flags why, in the narrative above Table "
    "112: 'The significant subsidiary data is subject to change due to local timing and local regulatory "
    "requirements.' Each sheet carries the figure printed in its own source table and neither has been adjusted "
    "toward the other. The FY2025 edition's 2024 comparative reproduces 126,375, confirming the OV1 figure is "
    "stable rather than a misprint. DO NOT reconcile these by editing either sheet. The other four years agree "
    "across both tables.\n\n"
    "Values are $million on the solo-consolidated basis. 'Settlement risk', 'Large exposures' and 'Floor "
    "adjustment' are printed as nil ('-') in the source and are carried as 0; settlement risk is genuinely "
    "non-zero only at FY2022 (6) and FY2021 (4).\n\n" + PRE_FY2021_SOURCES + "\n\n"
    "(The FY2021 Pillar 3 edition's Table 109 'Overview of RWA - Significant Subsidiaries' is the nearest thing "
    "to this breakdown for FY2021 and FY2020, and it IS a full OV1. It is not used here because its Standard "
    "Chartered Bank column is the SCB group consolidated perimeter, the same one as its Table 99: FY2021 total "
    "193,988 $m against 142,161 $m on this sheet. Two perimeters, not two measurements.)\n\n" + SOLO_BASIS_NOTE
)

bw.add_rwa_breakdown_sheet(
    title="Standard Chartered Bank — RWA Breakdown",
    subtitle="Solo-consolidated basis (the PRA's basis for this entity) - see source note.",
    rows=RWA_BREAKDOWN_ROWS,
    sources_text=RWA_BREAKDOWN_SOURCES,
    first_col_width=58,
    source_height=330,
    unit_suffix=" ($m)",
)

# Leverage / LCR / NSFR, same solo-consolidated basis and same editions.
bw.add_metric_sheet(
    "Leverage Ratio",
    "% (UK leverage exposure)",
    [("Leverage ratio excluding claims on central banks — solo-consolidated basis",
      {"FY2025": "4.2%", "FY2024": "4.5%", "FY2023": "4.4%", "FY2022": "4.2%", "FY2021": "4.1%", **NO_SOLO})],
    SOLO_SOURCES + "\n\nLEVERAGE: Table 'LRCom: Leverage ratio common disclosure (UK LR2) - Solo consolidation', "
    "row 25, in each edition (FY2025 Table 114; FY2024 Table 118; FY2023 Table 115; FY2022 Table 111; FY2021 from "
    "the FY2022 edition's comparative). Every year appears in two consecutive editions and agrees in both. "
    "FY2020 and earlier: no solo LR2 exists. The FY2021 edition's Table 110 'Leverage ratio common disclosure - "
    "Significant Subsidiaries' does print a Standard Chartered Bank leverage ratio for 2021 and 2020, but on the "
    "SCB GROUP CONSOLIDATED basis (the same column family as its Table 99), which is a different perimeter from "
    "this sheet's and has not been imported.",
    note=SOLO_BASIS_NOTE + " Row 25 of the UK LR2 template is reported as 'Leverage ratio EXCLUDING claims on "
    "central banks' - that is the only leverage ratio the UK template discloses, not a variant chosen here.",
    first_col_width=58,
    source_height=300,
)

bw.add_metric_sheet(
    "LCR",
    "% (12-month average)",
    [("Liquidity coverage ratio — solo-consolidated basis, 12-month average to 31 December",
      {"FY2025": "169.2%", "FY2024": "152.7%", "FY2023": "162.1%", "FY2022": "154%",
       "FY2021": ("Not published – FY2021 SC PLC Pillar 3 has no solo-consolidation section and its SCB annex "
                  "(Tables 99-108) has no LIQ1 or LCR row; the FY2022 edition's solo LIQ1 (Table 122) is a single "
                  "page headed 2022 with no prior-year page, and the Bank's own 2021 accounts state that SC Bank "
                  "is not regulated for LCR (see note)"),
       **NO_SOLO})],
    SOLO_SOURCES + "\n\nLCR: Table 'Liquidity Coverage Ratio (LCR) (UK LIQ1) - Solo consolidation', row 23, in each "
    "edition (FY2025 Table 125; FY2024; FY2023 Table 126; FY2022). The template reports four quarterly columns, "
    "each a 12-month average; the figure carried here is the 31 December column, i.e. the average of the 12 months "
    "to the year end.\n"
    "FY2021 RE-EXAMINED 2026-10-07 AND STILL NOT PUBLISHED - three independent checks, all negative. (a) The "
    "FY2021 Pillar 3 edition has no solo-consolidation section at all; its Annex 1 Standard Chartered Bank block "
    "(Tables 99-108) is capital resources, capital ratios and RWA, exposure at default by geography/industry/"
    "maturity, CR1-A and CR1-C credit quality, and guarantees and collateral - there is no LIQ1 and no LCR row "
    "anywhere in it, and that block is on the SCB group consolidated basis in any case. (b) The FY2022 edition's "
    "Table 122 'Liquidity Coverage Ratio (LCR) (UK LIQ1) - Solo consolidation' (p.127) is a SINGLE page headed "
    "2022, with columns 31.03.22/30.06.22/30.09.22/31.12.22 and no 'continued' prior-year page - unlike the GROUP "
    "Table 98, which does carry a 2021 page. Row 23 reads 148%/150%/154%/154%, and the 154% at 31.12.22 is the "
    "FY2022 figure above. (c) Standard Chartered Bank's own Directors' Report and Financial Statements 2021 "
    "states in its Strategic report: 'SC Bank is not regulated for Liquidity Coverage Ratio (LCR), however, the "
    "bank and material subsidiaries in the consolidation have standalone LCR ratios above 100 per cent.' The "
    "identical sentence appears in the 2020 edition. So no Bank-level FY2021 LCR exists to transcribe. Not "
    "derived, and the group's LCR has not been substituted.\n"
    "FY2020 and earlier: the same, with the added point that those Pillar 3 editions have no solo section of any "
    "kind.",
    note=SOLO_BASIS_NOTE + " This is a 12-month AVERAGE, not a point-in-time year-end ratio - the two are not "
    "interchangeable.",
    first_col_width=58,
    source_height=300,
)

bw.add_metric_sheet(
    "NSFR",
    "% (average)",
    [("Net stable funding ratio — solo-consolidated basis",
      {"FY2025": "122.7%", "FY2024": "121.4%", "FY2023": "121.9%", "FY2022": "117.6%",
       "FY2021": ("Not published – FY2021 SC PLC Pillar 3 has no solo-consolidation section or NSFR table; UK NSFR "
                  "disclosure began 1 Jan 2022 (PRA PS22/21)"),
       **{y: NO_SOLO[y] + "; and no UK NSFR requirement or template existed before 1 Jan 2022"
          for y in ("FY2020", "FY2019", "FY2018")}})],
    SOLO_SOURCES + "\n\nNSFR: Table 'Net Stable Funding Ratio (UK LIQ2) - Solo consolidation', row 34, in each "
    "edition (FY2025 Table 126; FY2024 Table 130; FY2023 Table 127; FY2022 Table 123). Each edition prints row 34 "
    "twice - the first occurrence is that edition's own year and the second is the prior-year comparative - which "
    "gives a complete cross-check: FY2024 reads 121.4% in both the FY2024 edition's own column and the FY2025 "
    "edition's comparative; FY2023 reads 121.9% in both the FY2023 and FY2024 editions; FY2022 reads 117.6% in "
    "both the FY2022 and FY2023 editions.\n"
    "FY2021 is 'Not applicable' rather than blank: the UK had no NSFR requirement and no NSFR disclosure template "
    "before 1 January 2022 (PRA PS17/21 / PS22/21, 'Implementation of Basel standards'), and the FY2021 Pillar 3 "
    "edition accordingly contains no solo-consolidation section or NSFR table.",
    note=SOLO_BASIS_NOTE,
    first_col_width=58,
    source_height=300,
)

unavailable(
    "MREL Ratio",
    "No solo-consolidated MREL ratio is disclosed. MREL requirements are set for UK resolution entities; the "
    "resolution entity in this group is Standard Chartered PLC, not this Bank entity, so a group MREL figure "
    "would not be an entity-level substitute. GA-020 (2026-09-19): the FY2025 Standard Chartered PLC Pillar 3 was "
    "re-read - its MREL/TLAC ratios are Table 2 'Key metrics - TLAC requirements (KM2)' for the SC PLC resolution "
    "group only; for Standard Chartered Bank it prints Table 13 'Standard Chartered Bank - creditor ranking "
    "(TLAC2)', which gives TLAC-eligible amounts by rank ($43,746m total at 2025) but no ratio. The FY2022 "
    "edition carries the same SCB TLAC2 table. The amounts are not transcribed: a ratio from them would be a "
    "back-solve.",
    cells={**{y: ("Not published – SC PLC Pillar 3 gives MREL/TLAC ratios (KM2) only for the SC PLC resolution "
                  "group; for this Bank only a TLAC2 creditor-ranking table, no ratio") for y in ("FY2025", "FY2024", "FY2023", "FY2022")},
           "FY2021": ("Not published – FY2021 SC PLC Pillar 3 has no Bank-level (solo) section; MREL/TLAC ratios are "
                      "given only for the SC PLC resolution group"),
           **{y: NO_SOLO[y] + "; MREL/TLAC ratios are given only for the SC PLC resolution group"
              for y in ("FY2020", "FY2019", "FY2018")}},
)

EQUITY_CHANGES_OVERVIEW = [
    ("Profit/(loss) for the year (Company)", {"FY2025": 2517, "FY2024": 2325, "FY2023": 2585, "FY2022": 2372, "FY2021": 2146, "FY2020": -141, "FY2019": 654, "FY2018": -568}),
    # Sum of the two dividend lines on the Statement of Changes in Equity sheet
    # for that movement year.  FY2022 and FY2021 were wrong here before
    # 2026-10-07 (both carried -292, the preference/AT1 line alone, with
    # FY2021's ordinary dividend of -1,511 and FY2022's -575 omitted) because
    # the equity roll-forward they were read off was mis-stitched; see the
    # Statement of Changes in Equity sheet's source note.  FY2019 excludes the
    # separate -6,987 dividend declared as a result of Group restructuring.
    ("Dividends and distributions paid (ordinary + preference/AT1)", {"FY2025": -2665, "FY2024": -2744, "FY2023": -2962, "FY2022": -886, "FY2021": -1803, "FY2020": -458, "FY2019": -834, "FY2018": -822}),
    ("Total equity (closing)", BS["Total equity"]),
]

bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", BS["Total assets"]),
        ("Loans and advances to customers", BS["Loans and advances to customers"]),
        ("Customer accounts", BS["Customer accounts"]),
        ("Total equity", BS["Total equity"]),
    ],
    balance_sheet_unit="$million",
    income_statement_totals=[
        ("Operating income", PL["Operating income"]),
        ("Operating expenses", PL["Operating expenses"]),
        ("Profit for the year", PL["Profit for the year"]),
    ],
    income_statement_unit="$million (Bank Group - see Profit & Loss sheet's source note)",
    equity_changes_totals=EQUITY_CHANGES_OVERVIEW,
    equity_changes_unit="$million (Company)",
    cash_flow_totals=[("Net cash from/(used in) operating activities", CF["Net cash from/(used in) operating activities"]),
                      ("Net cash from/(used in) investing activities", CF["Net cash from/(used in) investing activities"]),
                      ("Net cash used in financing activities", CF["Net cash used in financing activities"]),
                      ("Net increase/(decrease) in cash and cash equivalents", CF["Net increase/(decrease) in cash and cash equivalents"])],
    cash_flow_unit="$million",
    ratios=[],
    note=(
        "Balance Sheet, Statement of Changes in Equity, Cash Flow, and Asset Quality figures use the standalone "
        "Bank Company column throughout. The Profit & Loss figures use the Bank GROUP consolidated income "
        "statement instead, because the Company takes the s.408 Companies Act 2006 exemption and does not publish "
        "its own income statement (see the Profit & Loss sheet's source note for the Company's own profit-after-tax "
        "figures, which tie exactly to this Overview's equity-changes block). The regulatory Pillar 3 metric sheets "
        "use a THIRD basis: Standard Chartered Bank on the solo-consolidated basis, which is how the PRA sets this "
        "entity's capital requirements (the Company plus four named subsidiaries). Those figures were added on "
        "2026-09-15 from the solo-consolidation section of Standard Chartered PLC's annual Pillar 3 reports, which "
        "discloses this entity under the full UK templates; an earlier note recording them as not publicly "
        "disclosed was incorrect. They are NOT the Standard Chartered PLC group's figures - group RWA at FY2023 is "
        "244,151 $m against 122,408 $m here. Do not divide figures across the Company and solo-consolidated bases. "
        "The RWA Breakdown sheet was filled on the same date and from the same solo-consolidation annex, and so "
        "shares the Pillar 3 sheets' basis - but note the 8 $m FY2024 difference between it and the Total RWAs "
        "sheet, which the FY2024 Pillar 3 report itself creates by printing two different totals in two tables. "
        "That difference is documented on both sheets and is not to be reconciled away.\n\n"
        "FY2020, FY2019 AND FY2018 ADDED 2026-10-07. The statement sheets (Balance Sheet, Profit & Loss, "
        "Statement of Changes in Equity, Cash Flow, Asset Quality) carry figures for all three, each from "
        "Standard Chartered Bank's OWN Directors' Report and Financial Statements for that year. The regulatory "
        "sheets - all 11 Pillar 3 metric sheets, KM1 Key Metrics and RWA Breakdown - carry a STATEMENT for all "
        "three, because no solo-consolidation (Bank-level) disclosure exists in any Pillar 3 edition before the "
        "FY2022 one, whose oldest column is the FY2021 comparative. The FY2021, FY2020, FY2019 and FY2018 "
        "editions were each read end to end to establish that. The FY2021 edition DOES carry a Standard "
        "Chartered Bank column (Annex 1, Tables 99-110, with a 2020 comparative), but on the SCB GROUP "
        "CONSOLIDATED basis - a third perimeter again, with FY2021 RWA of 193,988 $m against 142,161 $m on the "
        "solo-consolidated basis used here - so it has not been imported. NO STANDARD CHARTERED PLC GROUP FIGURE "
        "HAS BEEN USED AS THIS BANK'S, ANYWHERE IN THIS WORKBOOK.\n\n"
        "FY2018 IS NOT LIKE-FOR-LIKE WITH FY2019 ONWARD. Standard Chartered PLC reorganised in 2019 and this "
        "Bank transferred out a large part of its business: total assets fall 425,338 -> 388,141, operating "
        "income 14,940 -> 9,378, and the 2019 accounts record a 6,987 dividend declared as a result of Group "
        "restructuring and a 4,573 loss from discontinued operations. Read the FY2018 column as a different-sized "
        "entity, not as a trading comparison.\n\n"
        "The Statement of Changes in Equity sheet was ALSO corrected on 2026-10-07: its year labels were shifted "
        "by one from 2021 onward and the whole 2022 movement year was missing. Read that sheet's source note "
        "before comparing this workbook with a copy built earlier."
    ),
)

bw.save("/Users/armaan/code/katalysis/banks/STANDARD CHARTERED BANK FINANCIALS.xlsx")
