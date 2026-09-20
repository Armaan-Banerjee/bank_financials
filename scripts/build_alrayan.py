import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

# Full 6 years of cash flow AND Pillar 3 coverage for FY2020-FY2025. FY2025's Pillar 3
# disclosure lagged its accounts by ~9 months and only appeared in September 2026; it
# was picked up and transcribed on 2026-09-15. No FRS 101/102 cash-flow exemption at all.
# FY2020 extension (HD-062): re-verified directly against the primary-source PDFs
# (Companies House's own FY2020 Annual Report filing, plus the bank's own standalone
# FY2020 Pillar 3 Disclosures document, recovered via a Wayback CDX domain scan of
# alrayanbank.co.uk since its FY2021 successor's URL guess pattern 404s for FY2020's
# own naming convention) rather than assumed from HD-002's nominal "confirmed floor
# FY2020" domain-scan signal - both documents obtained and read in full, no self-skip
# needed for this bank. FY2020's own Balance Sheet/P&L/Statement of Changes in Equity/
# Cash Flow figures are transcribed from the FY2021 Annual Report's own FY2020
# comparative column (image-only, read visually) rather than FY2020's own standalone
# AR, consistent with this workbook's established convention of using a year's most
# contemporary appearance; FY2020's Asset Quality/Pillar 3/RWA figures are transcribed
# directly from the FY2020 Pillar 3 Disclosures PDF (which has a genuine text layer,
# unlike the scanned ARs) cross-checked against the FY2021 AR's own FY2020 credit-risk
# comparative note. IMPORTANT genuine finding: FY2020's own cash-flow figures (as
# originally reported, the only version that exists - no restated FY2020 comparator
# was ever published) do NOT tie exactly to FY2021's already-in-workbook restated
# opening cash figure - see CASH_FLOW_SOURCES below for the full explanation.
YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021", "FY2020"]  # most recent first
YEAR_LABEL = {y: y for y in YEARS}

CH_URL = "https://find-and-update.company-information.service.gov.uk/company/04483430"
AR2025_URL = "https://find-and-update.company-information.service.gov.uk/company/04483430/filing-history/MzUxNTE1ODIyNGFkaXF6a2N4/document?format=pdf&download=0"
AR2024_URL = "https://www.alrayanbank.co.uk/sites/default/files/media/file-uploads/2025-04/04a_-_arb_financial_statements_fy_31-12-2024_-_signed_ey.cleaned.pdf"
AR2022_URL = "https://find-and-update.company-information.service.gov.uk/company/04483430/filing-history/MzM4MzEwOTk0N2FkaXF6a2N4/document?format=pdf&download=0"
AR2021_URL = "https://find-and-update.company-information.service.gov.uk/company/04483430/filing-history/MzM0NDI4NjkxNGFkaXF6a2N4/document?format=pdf&download=0"
AR2020_URL = "https://find-and-update.company-information.service.gov.uk/company/04483430/filing-history/MzMwMzI3NTQ0NmFkaXF6a2N4/document?format=pdf&download=0"
P3_2020_URL = "https://www.alrayanbank.co.uk/sites/default/files/media/file-uploads/2021-07/2020_pillar_3_disclosures_-_final.pdf"
P3_2021_URL = "https://www.alrayanbank.co.uk/sites/default/files/media/file-uploads/2022-10/inv-rep-2021-pillar-3.pdf"
P3_2023_URL = "https://www.alrayanbank.co.uk/sites/default/files/media/file-uploads/2024-08/pb7703_al_rayan_pillar_3_disclosures_2023_v2.pdf"
P3_2024_URL = "https://www.alrayanbank.co.uk/sites/default/files/media/file-uploads/2025-09/alrayan_pillar_3_disclosures_2024_web_-_010925.pdf"
P3_2025_URL = "https://www.alrayanbank.co.uk/sites/default/files/media/file-uploads/2026-09/pb8084_alrayan_pillar_3_disclosures_2025.pdf"

ENTITY_NOTE = (
    "ENTITY NOTE: Alrayan Bank Limited (FRN 229148, Companies House 04483430, matches Banks List 2608.xlsx "
    "exactly) is a UK Sharia-compliant bank, wholly owned by AlRayan Bank (Q.P.S.C.) of Qatar. Its own Annual "
    "Report/Pillar 3 documents style it 'Al Rayan Bank PLC' but Companies House confirms its current registered "
    "name is 'ALRAYAN BANK LIMITED' - same company number throughout, not an entity change, just inconsistent "
    "branding between the statutory filing and the bank's own PDFs."
)

CASH_FLOW_SOURCES = (
    "Sources - Al Rayan Bank's own Statement of Cash Flows, £'000s, all years:\n"
    f"FY2025: FY2025 Annual Report and Financial Statements (Companies House filing, made up to 31 Dec 2025, "
    f"filed 16 Apr 2026), p.41 - {AR2025_URL}\n"
    f"FY2024: FY2024 Annual Report and Financial Statements, p.42 - {AR2024_URL}\n"
    f"FY2023: sourced from the FY2024 Annual Report's own FY2023 comparative column, p.42 - {AR2024_URL}\n"
    f"FY2022: FY2022 Annual Report and Financial Statements (Companies House filing, made up to 31 Dec 2022, "
    f"filed 23 Jun 2023), p.38 - {AR2022_URL}\n"
    f"FY2021 (restated): sourced from the FY2022 Annual Report's own FY2021 comparative column, p.38 - "
    f"{AR2022_URL}. The FY2022 report's own footnote explains the FY2021 restatement: the Bank of England cash "
    f"ratio deposit was removed from 'Cash and cash equivalents' and MasterCard balances were added, following "
    f"updated IFRS Interpretations Committee guidance - the originally-reported FY2021 figures (from a standalone "
    f"FY2021 Annual Report) were not used, this restated version was, consistent with project convention of using "
    f"a year's most contemporary/authoritative appearance.\n"
    f"FY2020: sourced from the FY2021 Annual Report's own FY2020 comparative column (scanned/image-only - "
    f"transcribed via visual reading of the rendered page), p.43 - {AR2021_URL}. This is FY2020's ONLY available "
    "appearance anywhere - no FY2022 report (or later) carries a FY2020 comparative column, so there is no "
    "restated version of FY2020 to prefer over the original, unlike FY2021. GENUINE RECONCILIATION BREAK (not a "
    "transcription error): FY2020's own reported closing cash and cash equivalents is £385,376k, on the "
    "pre-restatement classification basis (BoE cash ratio deposit still included, MasterCard balances not yet "
    "added) - this does NOT tie to FY2021's own opening cash of £383,234k shown above, because that FY2021 figure "
    "is the FY2022-restated version. The ~£2,142k gap at the FY2020/FY2021 boundary is the direct, unavoidable "
    "effect of a restatement that was only ever published one year back (in FY2022's FY2021 comparative), never "
    "restated further back to FY2020 - so this workbook shows FY2020 on its own original basis (the only basis "
    "that exists for it) with the break documented here rather than force-adjusted to an invented restated figure. "
    "Several of FY2020's own 'Movement in' line items likewise differ from FY2021's restated figures already in "
    "this workbook for the same reason (e.g. Treasury Placements FY2021 shows -1,318 restated above, but FY2021's "
    "OWN original figure per this same FY2021 Annual Report page is +148 - not used here, shown only to explain "
    "why FY2020's -126 doesn't sit on an identical footing to the FY2021 column beside it). FY2020 also carries a "
    "one-off 'Deferred tax asset' movement line (+131) not present in any other year's own cash flow statement - "
    "shown as its own row rather than merged into 'Other liabilities'.\n"
    "FY2025's Statement of Cash Flows introduces new line-item names not used in earlier years (e.g. 'Structured "
    "real estate' replacing 'Commercial property finance', a new 'Securities purchased under reverse repurchase "
    "agreements' line, 'Encumbered non-cash balances' replacing 'Treasury placements') - these are shown as "
    "separate rows below rather than force-merged into the old line items, consistent with how this project "
    "handles other banks' presentation changes; every year's own reported section TOTALs are unaffected and the "
    "full chain reconciles exactly across FY2021-FY2025 except one immaterial £1k FY2021 rounding gap in the "
    "source document itself (opening 383,234 + net change -138,791 + FX -354 = 244,089 vs the printed closing "
    "balance of 244,090), kept as printed not force-corrected. FY2020's own column ties exactly within itself "
    "(opening 339,739 + net change 46,477 + FX -840 = 385,376 = the printed closing balance) but not into FY2021's "
    "column beside it, per the restatement break explained above.\n\n"
    + ENTITY_NOTE
)


def p3_sources(extra=""):
    return (
        "Sources - Alrayan Bank Limited's own Pillar 3 Disclosures, £m capital amounts / % ratios, all years:\n"
        f"FY2025: Pillar 3 Disclosures - 31 December 2025, Annex I KM1 table, p.39 - {P3_2025_URL}\n"
        f"FY2024: Pillar 3 Disclosures - 31 December 2024, Annex I KM1 table, p.38 - {P3_2024_URL}\n"
        f"FY2023: Pillar 3 Disclosures - 31 December 2023, Annex I KM1 table, p.33 - {P3_2023_URL}\n"
        f"FY2022: sourced from the FY2023 Pillar 3 Disclosures' own FY2022 comparative column, Annex I KM1 table, "
        f"p.33 - {P3_2023_URL}\n"
        f"FY2021: Pillar 3 Disclosures - 31 December 2021, Table 1/2/3 (this edition pre-dates the bank's adoption "
        f"of the standardised KM1 Annex template, so FY2021 figures come from the Executive Summary tables "
        f"instead), p.5 - {P3_2021_URL}\n"
        f"FY2020: Pillar 3 Disclosures - 31 December 2020, Table 1/2 'Available capital'/'Capital ratios as a "
        f"percentage of RWA' (same pre-KM1 Executive Summary format as FY2021's edition - this document has a "
        f"genuine text layer, unlike the scanned Annual Reports, so figures are machine-read not visually "
        f"transcribed), p.3 - {P3_2020_URL}. Cross-checked against the FY2021 Annual Report's own FY2020 credit-"
        "risk comparative note and ties exactly.\n"
        "FY2025 FILLED 2026-09-15: the FY2025 Pillar 3 Disclosures PDF is now live on the Bank's "
        "investor-relations regulatory-information page (published 2026-09), and every FY2025 Pillar 3 cell in "
        "this workbook is transcribed from its Annex I KM1/OV1 templates - nothing is carried over from the "
        "Annual Report. One consequence: the CET1 ratio cell for FY2025 was previously 15.41% (the FY2025 "
        "Annual Report's own KPI table, the only capital figure available before the Pillar 3 document "
        "appeared) and is now 15.45%, the KM1 Annex figure. The two are different bases, not a correction of "
        "an error - the same AR-KPI-vs-KM1 spread this project keeps blank elsewhere - and the KM1 figure is "
        "used here for consistency with FY2020-FY2024 and with every other bank in this project. Likewise the "
        "LCR cell uses KM1 line 17's twelve-month average (481%), not the Executive Summary's point-in-time "
        "598%.\n"
        "This bank's own Pillar 3 documents show small internal discrepancies between their Executive Summary "
        "narrative tables and their formal KM1 Annex tables in a couple of instances (e.g. FY2023 NSFR: 160% "
        "exec summary vs 157% KM1 annex; FY2022 Leverage Ratio: 6.8% exec summary vs 6.7% KM1 annex) - this "
        "workbook uses the KM1 Annex figures throughout for consistency with the standard regulatory template and "
        "with every other bank in this project.\n"
        + (extra + "\n" if extra else "")
        + "\n" + ENTITY_NOTE
    )


bw = BankWorkbook(bank_name="Alrayan Bank Limited", years=YEARS, year_label=YEAR_LABEL, header_color="4361EE")

# ---------------------------------------------------------------
# Sheet: Balance Sheet
# ---------------------------------------------------------------
BALANCE_SHEET_PRESENTATION_NOTE = (
    "Presentation note: Al Rayan Bank's own line-item labels have changed across the 5 years shown - "
    "'Commercial Property Finance' (FY2021-24) was renamed 'Structured Real Estate' in FY2025 (shown as a "
    "separate row here, not force-merged); 'Investment securities' (one line, FY2021-24) was split into "
    "'Investment securities through FVOCI' and 'Investment securities at amortised cost' plus a new "
    "'Securities purchased under reverse repurchase agreements' line in FY2025 (shown separately); "
    "'Deferred tax asset' and 'Derivative financial instruments' (assets) are not disclosed as separate lines "
    "in FY2022 (blank that year, not zero); 'Financing from banks' (liability) only appears from FY2024 "
    "onward; 'Assets held for sale' only appears FY2024-25; 'Sharia compliant derivative financial "
    "instruments' (liability) is labelled that way FY2021-22, then just 'Derivative financial instruments' "
    "FY2023-25 - same line, relabelled. On equity: 'Share premium' (£54,807k at 1 Jan 2021) was fully "
    "cancelled during FY2021 and is £0/blank at every year-end shown; 'Reserve on investment securities' "
    "(FY2021-22 label) was relabelled 'Investment securities fair value reserve' from FY2023; 'Property "
    "revaluation reserve' only appears from FY2024 (the freehold property revaluation that year); 'Cash flow "
    "hedge reserve' only appears from FY2025 (a new hedge programme that year). Blank cells indicate that "
    "year's own balance sheet did not carry that line at all (not that the value was zero), except where "
    "noted as a disclosed nil ('-') above. FY2020 additionally carries a genuine £5,137k 'Sharia compliant "
    "derivative financial instruments' ASSET balance (merged into the 'Derivative financial instruments "
    "(asset)' row below) - the only year of the 5 shown where that asset-side line is non-nil; FY2020's "
    "'Sukuk funding' liability (£146,944k) was fully repaid during FY2021 and never reappears; FY2020's "
    "'Share premium' (£54,807k) and equity reserve labels match FY2021's, both pre-dating the FY2021 "
    "cancellation/relabelling described above.\n\n" + ENTITY_NOTE
)

balance_sheet_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash", {"FY2025": 1379, "FY2024": 1118, "FY2023": 953, "FY2022": 1234, "FY2021": 1867, "FY2020": 2638}),
    ("DATA", "Treasury placements and cash balances with banks",
     {"FY2025": 288533, "FY2024": 539414, "FY2023": 401615, "FY2022": 353062, "FY2021": 246809, "FY2020": 383864}),
    ("DATA", "Securities purchased under reverse repurchase agreements", {"FY2025": 74193}),
    ("DATA", "Investment securities through FVOCI", {"FY2025": 209111}),
    ("DATA", "Investment securities at amortised cost", {"FY2025": 30046}),
    ("DATA", "Investment securities",
     {"FY2024": 141863, "FY2023": 148713, "FY2022": 108821, "FY2021": 123532, "FY2020": 170751}),
    ("DATA", "Home Purchase Plans",
     {"FY2025": 887078, "FY2024": 933032, "FY2023": 993121, "FY2022": 1099728, "FY2021": 1191984, "FY2020": 1193727}),
    ("DATA", "Structured Real Estate / Commercial Property Finance",
     {"FY2025": 1588996, "FY2024": 1173952, "FY2023": 899686, "FY2022": 789370, "FY2021": 669653, "FY2020": 557267}),
    ("DATA", "Property and equipment",
     {"FY2025": 33780, "FY2024": 34833, "FY2023": 33561, "FY2022": 33072, "FY2021": 7628, "FY2020": 11198}),
    ("DATA", "Intangible assets", {"FY2025": 3071, "FY2024": 2972, "FY2023": 3166, "FY2022": 3075, "FY2021": 4101, "FY2020": 5069}),
    ("DATA", "Assets held for sale", {"FY2025": 2084, "FY2024": 2084}),
    ("DATA", "Deferred tax asset", {"FY2025": 316, "FY2024": 2049, "FY2023": 4838, "FY2021": 7607, "FY2020": 5977}),
    ("DATA", "Derivative financial instruments (asset)",
     {"FY2025": 792, "FY2024": 733, "FY2023": 3344, "FY2020": 5137}),
    ("DATA", "Other assets", {"FY2025": 6053, "FY2024": 3674, "FY2023": 4221, "FY2022": 3578, "FY2021": 5710, "FY2020": 4193}),
    ("TOTAL", "Total assets",
     {"FY2025": 3125432, "FY2024": 2835724, "FY2023": 2493218, "FY2022": 2400294, "FY2021": 2258891, "FY2020": 2339821}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Deposits from banks and financial institutions",
     {"FY2025": 221222, "FY2024": 64752, "FY2023": 111237, "FY2022": 145703, "FY2021": 98962, "FY2020": 37867}),
    ("DATA", "Deposits from customers",
     {"FY2025": 2477658, "FY2024": 2412883, "FY2023": 2149200, "FY2022": 2044149, "FY2021": 1959663, "FY2020": 1965001}),
    ("DATA", "Financing from banks", {"FY2025": 176023, "FY2024": 80776}),
    ("DATA", "Sukuk funding", {"FY2020": 146944}),
    ("DATA", "Subordinated funding", {"FY2025": 2500, "FY2024": 25000, "FY2023": 25000, "FY2022": 25000, "FY2021": 25000, "FY2020": 25000}),
    ("DATA", "Derivative financial instruments (liability)",
     {"FY2025": 1950, "FY2024": 665, "FY2023": 22, "FY2022": 866, "FY2021": 592, "FY2020": 5}),
    ("DATA", "Other liabilities",
     {"FY2025": 12076, "FY2024": 35174, "FY2023": 12621, "FY2022": 17261, "FY2021": 17363, "FY2020": 14948}),
    ("TOTAL", "Total liabilities",
     {"FY2025": 2891429, "FY2024": 2619250, "FY2023": 2298080, "FY2022": 2232979, "FY2021": 2101580, "FY2020": 2189765}),
    ("SECTION", "Equity", {}),
    ("DATA", "Share capital", {"FY2025": 121219, "FY2024": 121219, "FY2023": 121219, "FY2022": 121219, "FY2021": 121219, "FY2020": 121219}),
    ("DATA", "Share premium", {"FY2022": 0, "FY2021": 0, "FY2020": 54807}),
    ("DATA", "Contingent convertible investment",
     {"FY2025": 3000, "FY2024": 3000, "FY2023": 3000, "FY2022": 3000, "FY2021": 3000, "FY2020": 3000}),
    ("DATA", "Investment securities fair value reserve / Reserve on investment securities",
     {"FY2025": 86, "FY2024": -202, "FY2023": -1572, "FY2022": -6648, "FY2021": -995, "FY2020": 753}),
    ("DATA", "Property revaluation reserve", {"FY2025": 2491, "FY2024": 2531}),
    ("DATA", "Cash flow hedge reserve", {"FY2025": -63}),
    ("DATA", "Retained earnings/(deficit)",
     {"FY2025": 107172, "FY2024": 89830, "FY2023": 72392, "FY2022": 49647, "FY2021": 33989, "FY2020": -29823}),
    ("DATA", "Profit stabilisation reserve", {"FY2025": 98, "FY2024": 96, "FY2023": 99, "FY2022": 97, "FY2021": 98, "FY2020": 100}),
    ("TOTAL", "Total equity",
     {"FY2025": 234003, "FY2024": 216474, "FY2023": 195138, "FY2022": 167315, "FY2021": 157311, "FY2020": 150056}),
    ("TOTAL", "Total liabilities & equity",
     {"FY2025": 3125432, "FY2024": 2835724, "FY2023": 2493218, "FY2022": 2400294, "FY2021": 2258891, "FY2020": 2339821}),
]

bw.add_balance_sheet_sheet(
    title="Alrayan Bank Limited — Statement of Financial Position",
    subtitle="Bank entity-level basis, £'000s.",
    rows=balance_sheet_rows,
    sources_text=(
        "Sources - Al Rayan Bank's own Statement of Financial Position, £'000s, all years:\n"
        f"FY2025: FY2025 Annual Report and Financial Statements (Companies House filing, made up to 31 Dec 2025, "
        f"filed 16 Apr 2026, scanned/image-only - transcribed via visual reading of the rendered page), p.39 - "
        f"{AR2025_URL}\n"
        f"FY2024: FY2024 Annual Report and Financial Statements, p.40 - {AR2024_URL}\n"
        f"FY2023: sourced from the FY2024 Annual Report's own FY2023 comparative column, p.40 - {AR2024_URL}\n"
        f"FY2022: FY2022 Annual Report and Financial Statements (Companies House filing, made up to 31 Dec 2022, "
        f"filed 23 Jun 2023, scanned/image-only - transcribed via visual reading of the rendered page), p.36 - "
        f"{AR2022_URL}\n"
        f"FY2021: sourced from the FY2022 Annual Report's own FY2021 comparative column, p.36 - {AR2022_URL}\n"
        f"FY2020: sourced from the FY2021 Annual Report's own FY2020 comparative column (scanned/image-only - "
        f"transcribed via visual reading of the rendered page), p.41 - {AR2021_URL}\n\n"
        + BALANCE_SHEET_PRESENTATION_NOTE
    ),
    first_col_width=68,
    source_height=280,
    unit_suffix=" (£'000s)",
)

# ---------------------------------------------------------------
# Sheet: Profit & Loss
# ---------------------------------------------------------------
INCOME_STATEMENT_PRESENTATION_NOTE = (
    "Presentation note: Al Rayan Bank's income statement structure changed materially between FY2021-22 and "
    "FY2023-25. FY2021-22 used 'Income from Islamic financing transactions' as the top line and included "
    "'Impairment (charge)/reversal' as one of several operating-expense lines below Total income (i.e. before "
    "Total operating expenses, not netted against income); FY2023-25 renamed the top line 'Income from "
    "financing transactions' (no P&L-level change, entity remains fully Sharia-compliant per ENTITY_NOTE) and "
    "moved the credit-loss line to 'Expected credit loss charge' within Total operating expenses too, so the "
    "structural difference is presentational (line placement/ordering) not substantive - Total income and "
    "Total operating expenses are comparable across all 5 years despite the internal reordering. FY2023-25 "
    "additionally show a 'Net (loss)/gain on profit rate swaps at fair value' line (FY2021-22 had no swap "
    "programme). Other comprehensive income sub-items ('Items that will not be reclassified' - the freehold "
    "property revaluation and its associated cash flow hedge reserve movement) only appear from FY2024 "
    "onward, consistent with the Balance Sheet sheet's presentation note. 'Total comprehensive income for the "
    "financial year' is the one row genuinely comparable and populated across all 6 years. FY2020 uses the same "
    "'Income from Islamic financing transactions' top line as FY2021-22 (predates the FY2023 relabelling) and "
    "reports a genuine £nil 'Other non-fee income' that year (shown as 0, not blank, since the line is otherwise "
    "populated in every other year).\n\n" + ENTITY_NOTE
)

income_statement_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Income from financing transactions",
     {"FY2025": 172541, "FY2024": 166206, "FY2023": 143577, "FY2022": 84762, "FY2021": 65755, "FY2020": 65896}),
    ("DATA", "Returns to banks and customers",
     {"FY2025": -108402, "FY2024": -103641, "FY2023": -71869, "FY2022": -29308, "FY2021": -22140, "FY2020": -29682}),
    ("TOTAL", "Net income from financing transactions",
     {"FY2025": 64139, "FY2024": 62565, "FY2023": 71708, "FY2022": 55454, "FY2021": 43615, "FY2020": 36214}),
    ("DATA", "Fees and commission income",
     {"FY2025": 530, "FY2024": 882, "FY2023": 996, "FY2022": 1107, "FY2021": 1098, "FY2020": 1157}),
    ("DATA", "Fees and commission expense",
     {"FY2025": -596, "FY2024": -658, "FY2023": -394, "FY2022": -745, "FY2021": -452, "FY2020": -363}),
    ("TOTAL", "Net fees and commission (expense)/income",
     {"FY2025": -66, "FY2024": 224, "FY2023": 602, "FY2022": 362, "FY2021": 646, "FY2020": 794}),
    ("DATA", "Net (loss)/gain on profit rate swaps at fair value", {"FY2025": -54, "FY2024": 733}),
    ("DATA", "Loss on disposal of investment securities", {"FY2023": -3766}),
    ("DATA", "Gain on disposal of investment securities", {"FY2022": 51, "FY2021": 25, "FY2020": 2941}),
    ("DATA", "Foreign exchange gain/(loss)",
     {"FY2025": 4, "FY2024": -274, "FY2023": -266, "FY2022": -10, "FY2021": -354, "FY2020": -840}),
    ("DATA", "Other non-fee income/(loss)",
     {"FY2025": 181, "FY2024": 183, "FY2023": 119, "FY2022": -50, "FY2021": 464, "FY2020": 0}),
    ("TOTAL", "Other income/(loss)", {"FY2025": 131, "FY2024": 642, "FY2023": -3913, "FY2022": -9, "FY2021": 135, "FY2020": 2101}),
    ("TOTAL", "Total income",
     {"FY2025": 64204, "FY2024": 63431, "FY2023": 68397, "FY2022": 55807, "FY2021": 44396, "FY2020": 39109}),
    ("SECTION", "Operating expenses", {}),
    ("DATA", "Impairment (charge)/reversal", {"FY2022": -183, "FY2021": 468, "FY2020": -1544}),
    ("DATA", "Staff costs",
     {"FY2025": -20773, "FY2024": -20093, "FY2023": -20423, "FY2022": -18153, "FY2021": -17737, "FY2020": -17686}),
    ("DATA", "General and administrative expenses",
     {"FY2025": -13575, "FY2024": -13728, "FY2023": -13370, "FY2022": -12840, "FY2021": -13016, "FY2020": -11329}),
    ("DATA", "Expected credit loss charge", {"FY2025": -3798, "FY2024": -2936, "FY2023": -1428}),
    ("DATA", "Depreciation & Impairment",
     {"FY2025": -1407, "FY2024": -1844, "FY2023": -1338, "FY2022": -1843, "FY2021": -2968, "FY2020": -3040}),
    ("DATA", "Amortisation", {"FY2025": -1064, "FY2024": -1361, "FY2023": -1230, "FY2022": -1991, "FY2021": -1516, "FY2020": -1312}),
    ("TOTAL", "Total operating expenses",
     {"FY2025": -40617, "FY2024": -39962, "FY2023": -37789, "FY2022": -35010, "FY2021": -34769, "FY2020": -34911}),
    ("TOTAL", "Profit before tax",
     {"FY2025": 23587, "FY2024": 23469, "FY2023": 30608, "FY2022": 20797, "FY2021": 9627, "FY2020": 4198}),
    ("DATA", "Tax charge", {"FY2025": -5906, "FY2024": -5752, "FY2023": -7580, "FY2022": -4297, "FY2021": -624, "FY2020": -360}),
    ("TOTAL", "Profit for the financial year",
     {"FY2025": 17681, "FY2024": 17717, "FY2023": 23028, "FY2022": 16500, "FY2021": 9003, "FY2020": 3838}),
    ("SECTION", "Other comprehensive income", {}),
    ("DATA", "Change in fair value of investment securities at FVOCI",
     {"FY2025": 386, "FY2024": 1825, "FY2023": 3003, "FY2022": -5602, "FY2021": -1723, "FY2020": 3338}),
    ("DATA", "Amounts transferred to the income statement",
     {"FY2024": 0, "FY2023": 3766, "FY2022": -51, "FY2021": -25, "FY2020": -2941}),
    ("DATA", "Taxation - deferred (investment securities)", {"FY2025": -98, "FY2024": -455}),
    ("DATA", "Change in fair value of cash flow hedge", {"FY2025": -84}),
    ("DATA", "Taxation - deferred (cash flow hedge)", {"FY2025": 21}),
    ("DATA", "Gain on the revaluation of freehold property", {"FY2024": 3374}),
    ("DATA", "Taxation - deferred (property revaluation)", {"FY2024": -843}),
    ("TOTAL", "Total comprehensive income for the financial year",
     {"FY2025": 17906, "FY2024": 21618, "FY2023": 28104, "FY2022": 10847, "FY2021": 7255, "FY2020": 4235}),
]

bw.add_income_statement_sheet(
    title="Alrayan Bank Limited — Statement of Comprehensive Income",
    subtitle="Bank entity-level basis, £'000s.",
    rows=income_statement_rows,
    sources_text=(
        "Sources - Al Rayan Bank's own Statement of Comprehensive Income, £'000s, all years:\n"
        f"FY2025: FY2025 Annual Report and Financial Statements (scanned/image-only - transcribed via visual "
        f"reading of the rendered pages), pp.37-38 - {AR2025_URL}\n"
        f"FY2024: FY2024 Annual Report and Financial Statements, p.39 - {AR2024_URL}\n"
        f"FY2023: sourced from the FY2024 Annual Report's own FY2023 comparative column, p.39 - {AR2024_URL}\n"
        f"FY2022: FY2022 Annual Report and Financial Statements (scanned/image-only - transcribed via visual "
        f"reading of the rendered page), p.35 - {AR2022_URL}\n"
        f"FY2021: sourced from the FY2022 Annual Report's own FY2021 comparative column, p.35 - {AR2022_URL}\n"
        f"FY2020: sourced from the FY2021 Annual Report's own FY2020 comparative column (scanned/image-only - "
        f"transcribed via visual reading of the rendered page), p.40 - {AR2021_URL}\n\n"
        + INCOME_STATEMENT_PRESENTATION_NOTE
    ),
    first_col_width=68,
    source_height=280,
    unit_suffix=" (£'000s)",
)

# ---------------------------------------------------------------
# Sheet: Statement of Changes in Equity
# ---------------------------------------------------------------
EQUITY_CHANGES_PRESENTATION_NOTE = (
    "Presentation note: read chronologically (oldest to newest), unlike every other sheet in this workbook. "
    "'Share premium' (£54,807k at 1 Jan 2021) was fully cancelled during FY2021 and is £0/blank at every "
    "later balance date - shown as a column here for completeness, not force-dropped. 'Investment securities "
    "fair value reserve' was labelled 'Reserve on investment securities' in the FY2021-22 statements (same "
    "reserve, relabelled from FY2023). 'Property revaluation reserve' and 'Cash flow hedge reserve' columns "
    "are blank before the balance in which they first appear (FY2024 and FY2025 respectively) since the "
    "component didn't exist yet - see the Balance Sheet sheet's presentation note for the same components. "
    "'Transfer to profit stabilisation reserve' rows are small (net-zero-to-Total) reallocations between "
    "retained earnings and the profit stabilisation reserve, reported as-is from each year's own statement. "
    "FY2020's ladder starts at 1 January 2020 (the earliest opening balance obtainable, from the FY2021 Annual "
    "Report's own FY2020 comparative column) - Share premium (£54,807k) and the reserve on investment "
    "securities are both still present at their pre-FY2021-cancellation/relabelling levels.\n\n"
    + ENTITY_NOTE
)

EQUITY_HEADERS = [
    "Share capital", "Share premium", "Contingent convertible investment",
    "Investment securities fair value reserve", "Property revaluation reserve",
    "Cash flow hedge reserve", "Retained earnings/(deficit)", "Profit stabilisation reserve", "Total",
]

equity_changes_rows = [
    ("TOTAL", "Balance at 1 January 2020", (121219, 54807, 3000, 356, None, None, -33660, 99, 145821)),
    ("DATA", "Profit for the year", (None, None, None, None, None, None, 3838, None, 3838)),
    ("DATA", "Other comprehensive income", (None, None, None, 397, None, None, None, None, 397)),
    ("TOTAL", "Total comprehensive income", (None, None, None, 397, None, None, 3838, None, 4235)),
    ("DATA", "Transfer to profit stabilisation reserve", (None, None, None, None, None, None, -1, 1, 0)),
    ("TOTAL", "Balance at 31 December 2020", (121219, 54807, 3000, 753, None, None, -29823, 100, 150056)),

    ("TOTAL", "Balance at 1 January 2021", (121219, 54807, 3000, 753, None, None, -29823, 100, 150056)),
    ("DATA", "Profit for the year", (None, None, None, None, None, None, 9003, None, 9003)),
    ("DATA", "Other comprehensive loss", (None, None, None, -1748, None, None, None, None, -1748)),
    ("TOTAL", "Total comprehensive income", (None, None, None, -1748, None, None, 9003, None, 7255)),
    ("DATA", "Cancellation of Share Premium", (None, -54807, None, None, None, None, 54807, None, 0)),
    ("DATA", "Transfer to profit stabilisation reserve", (None, None, None, None, None, None, 2, -2, 0)),
    ("TOTAL", "Balance at 31 December 2021", (121219, 0, 3000, -995, None, None, 33989, 98, 157311)),

    ("DATA", "Profit for the year", (None, None, None, None, None, None, 16500, None, 16500)),
    ("DATA", "Other comprehensive loss", (None, None, None, -5653, None, None, None, None, -5653)),
    ("TOTAL", "Total comprehensive income", (None, None, None, -5653, None, None, 16500, None, 10847)),
    ("DATA", "Profit Payment to Additional Tier 1 capital holders",
     (None, None, None, None, None, None, -843, None, -843)),
    ("DATA", "Transfer to profit stabilisation reserve", (None, None, None, None, None, None, 1, -1, 0)),
    ("TOTAL", "Balance at 31 December 2022", (121219, 0, 3000, -6648, None, None, 49647, 97, 167315)),

    ("DATA", "Profit for the year", (None, None, None, None, None, None, 23028, None, 23028)),
    ("DATA", "Other comprehensive income", (None, None, None, 5076, None, None, None, None, 5076)),
    ("TOTAL", "Total comprehensive income", (None, None, None, 5076, None, None, 23028, None, 28104)),
    ("DATA", "Profit payment to additional Tier 1 capital holders",
     (None, None, None, None, None, None, -281, None, -281)),
    ("DATA", "Transfer to profit stabilisation reserve", (None, None, None, None, None, None, -2, 2, 0)),
    ("TOTAL", "Balance at 31 December 2023", (121219, None, 3000, -1572, None, None, 72392, 99, 195138)),

    ("DATA", "Profit for the year", (None, None, None, None, None, None, 17717, None, 17717)),
    ("DATA", "Other comprehensive income", (None, None, None, 1370, 2531, None, None, None, 3901)),
    ("TOTAL", "Total comprehensive income", (None, None, None, 1370, 2531, None, 17717, None, 21618)),
    ("DATA", "Profit payment to additional Tier 1 capital holders",
     (None, None, None, None, None, None, -282, None, -282)),
    ("DATA", "Transfer to profit stabilisation reserve", (None, None, None, None, None, None, 3, -3, 0)),
    ("TOTAL", "Balance at 31 December 2024", (121219, None, 3000, -202, 2531, None, 89830, 96, 216474)),

    ("DATA", "Profit for the year", (None, None, None, None, None, None, 17681, None, 17681)),
    ("DATA", "Other comprehensive income", (None, None, None, 288, None, -63, None, None, 225)),
    ("TOTAL", "Total comprehensive income", (None, None, None, 288, None, -63, 17681, None, 17906)),
    ("DATA", "Profit payment to additional Tier 1 capital holders",
     (None, None, None, None, None, None, -377, None, -377)),
    ("DATA", "Transfer to profit stabilisation reserve", (None, None, None, None, None, None, -2, 2, 0)),
    ("DATA", "Transfer of depreciation on revaluation surplus",
     (None, None, None, None, -40, None, 40, None, 0)),
    ("TOTAL", "Balance at 31 December 2025", (121219, None, 3000, 86, 2491, -63, 107172, 98, 234003)),
]

bw.add_equity_changes_sheet(
    title="Alrayan Bank Limited — Statement of Changes in Equity",
    subtitle="Bank entity-level basis, £'000s. Chronological, oldest to newest.",
    headers=EQUITY_HEADERS,
    rows=equity_changes_rows,
    sources_text=(
        "Sources - Al Rayan Bank's own Statement of Changes in Equity, £'000s, all years:\n"
        f"FY2020-2021: FY2021 Annual Report and Financial Statements (scanned/image-only - transcribed via "
        f"visual reading of the rendered page), p.42 - {AR2021_URL}\n"
        f"FY2021-2022: FY2022 Annual Report and Financial Statements (scanned/image-only - transcribed via "
        f"visual reading of the rendered page), p.37 - {AR2022_URL}\n"
        f"FY2023-2024: FY2024 Annual Report and Financial Statements, p.41 - {AR2024_URL}\n"
        f"FY2025: FY2025 Annual Report and Financial Statements (scanned/image-only - transcribed via visual "
        f"reading of the rendered page), p.40 - {AR2025_URL}\n\n"
        + EQUITY_CHANGES_PRESENTATION_NOTE
    ),
    first_col_width=44,
    source_height=280,
    col_width=16,
)

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Profit before tax", {"FY2025": 23587, "FY2024": 23469, "FY2023": 30608, "FY2022": 20797, "FY2021": 9627, "FY2020": 4198}),
    ("DATA", "Depreciation", {"FY2025": 1407, "FY2024": 1844, "FY2023": 1338, "FY2022": 1843, "FY2021": 2968, "FY2020": 3040}),
    ("DATA", "Amortisation", {"FY2025": 1064, "FY2024": 1361, "FY2023": 1230, "FY2022": 1991, "FY2021": 1516, "FY2020": 1312}),
    ("DATA", "Loss/(gain) on disposal of investment securities", {"FY2023": 3766, "FY2022": -51, "FY2021": -25, "FY2020": -2941}),
    ("DATA", "Cost of subordinated funding", {"FY2025": 1118, "FY2024": 2000, "FY2023": 2000}),
    ("DATA", "Impairment / expected credit loss charge on financial assets",
     {"FY2025": 3798, "FY2024": 2936, "FY2023": 1428, "FY2022": 183, "FY2021": -464, "FY2020": 1544}),
    ("DATA", "Other non-cash items", {"FY2025": 191, "FY2024": 943, "FY2023": 340, "FY2022": 292, "FY2021": 565, "FY2020": 1092}),
    ("TOTAL", "Net cash generated before changes in operating assets and liabilities",
     {"FY2025": 31165, "FY2024": 32553, "FY2023": 40710, "FY2022": 25055, "FY2021": 14187, "FY2020": 8245}),
    ("DATA", "Treasury placements", {"FY2024": 3330, "FY2023": -350, "FY2022": 120, "FY2021": -1318, "FY2020": -126}),
    ("DATA", "Encumbered non-cash balances", {"FY2025": -1054}),
    ("DATA", "Home purchase plans", {"FY2025": 45000, "FY2024": 61204, "FY2023": 106281, "FY2022": 92488, "FY2021": 1971, "FY2020": -9860}),
    ("DATA", "Commercial property finance", {"FY2024": -278317, "FY2023": -111420, "FY2022": -120113, "FY2021": -112138, "FY2020": -92616}),
    ("DATA", "Structured real estate", {"FY2025": -417886}),
    ("DATA", "Securities purchased under reverse repurchase agreements", {"FY2025": -74193}),
    ("DATA", "Other assets", {"FY2025": -2105, "FY2024": 925, "FY2023": -138, "FY2022": 2191, "FY2021": -1514, "FY2020": -150}),
    ("DATA", "Derivative financial instruments", {"FY2025": 1143, "FY2024": 3254, "FY2023": -4188, "FY2022": 275, "FY2021": 5137, "FY2020": -3852}),
    ("DATA", "Deposits from banks and financial institutions",
     {"FY2025": 156470, "FY2024": -46485, "FY2023": -34466, "FY2022": 46741, "FY2021": 61095, "FY2020": 61}),
    ("DATA", "Deposits from customers", {"FY2025": 64775, "FY2024": 263683, "FY2023": 105052, "FY2022": 84485, "FY2021": -5338, "FY2020": 124178}),
    ("DATA", "Other liabilities", {"FY2025": -22811, "FY2024": 22284, "FY2023": -3379, "FY2022": 2767, "FY2021": 3871, "FY2020": -1053}),
    ("DATA", "Deferred tax asset", {"FY2020": 131}),
    ("DATA", "Taxation paid", {"FY2025": -4547, "FY2024": -4688, "FY2023": -6300, "FY2022": -3140, "FY2021": -1945, "FY2020": -432}),
    ("TOTAL", "Net cash generated from/(used in) operating activities",
     {"FY2025": -224043, "FY2024": 57743, "FY2023": 91802, "FY2022": 130869, "FY2021": -35992, "FY2020": 24526}),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Purchase of investment securities", {"FY2025": -302813, "FY2024": -200801, "FY2023": -226418}),
    ("DATA", "Sales/maturities of investment securities", {"FY2025": 205903, "FY2024": 209476, "FY2023": 189530}),
    ("DATA", "Net sales of investment securities", {"FY2022": 7253, "FY2021": 46245, "FY2020": 60010}),
    ("DATA", "Purchase of property and equipment", {"FY2025": -354, "FY2024": -1826, "FY2023": -1828, "FY2022": -29430, "FY2021": -40, "FY2020": -251}),
    ("DATA", "Investment in intangible assets", {"FY2025": -1163, "FY2024": -1167, "FY2023": -1321, "FY2022": -966, "FY2021": -548, "FY2020": -2319}),
    ("TOTAL", "Net cash generated from/(used in) investing activities",
     {"FY2025": -98427, "FY2024": 5682, "FY2023": -40037, "FY2022": -23143, "FY2021": 45657, "FY2020": 57440}),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Redemption of sukuk funding", {"FY2021": -146944, "FY2020": -34047}),
    ("DATA", "Financing from banks", {"FY2025": 95247, "FY2024": 80776}),
    ("DATA", "Payment of principal in respect of leases", {"FY2025": -435, "FY2024": -325, "FY2023": -1260, "FY2022": -1019, "FY2021": -1318, "FY2020": -1096}),
    ("DATA", "Payment of financing in respect of leases", {"FY2025": -25, "FY2024": -27, "FY2023": -33, "FY2022": -116, "FY2021": -194, "FY2020": -346}),
    ("DATA", "Payment of Additional Tier 1 Financing profit", {"FY2025": -377, "FY2024": -282, "FY2023": -281, "FY2022": -843}),
    ("DATA", "Payment of subordinated funding / profit on subordinated funding", {"FY2025": -23618, "FY2024": -2000, "FY2023": -2000}),
    ("TOTAL", "Net cash generated from/(used in) financing activities",
     {"FY2025": 70792, "FY2024": 78142, "FY2023": -3574, "FY2022": -1978, "FY2021": -148456, "FY2020": -35489}),
    ("TOTAL", "Net change in cash and cash equivalents",
     {"FY2025": -251678, "FY2024": 141567, "FY2023": 48191, "FY2022": 105748, "FY2021": -138791, "FY2020": 46477}),
    ("DATA", "Foreign exchange gain/(loss)", {"FY2025": 4, "FY2024": -274, "FY2023": -266, "FY2022": -10, "FY2021": -354, "FY2020": -840}),
    ("DATA", "Opening cash and cash equivalents", {"FY2025": 539046, "FY2024": 397753, "FY2023": 349828, "FY2022": 244090, "FY2021": 383234, "FY2020": 339739}),
    ("TOTAL", "Closing cash and cash equivalents",
     {"FY2025": 287372, "FY2024": 539046, "FY2023": 397753, "FY2022": 349828, "FY2021": 244090, "FY2020": 385376}),
]

bw.add_cash_flow_sheet(
    title="Alrayan Bank Limited — Statement of Cash Flows",
    subtitle="Bank entity-level basis, £'000s. Full 6 years, no cash-flow exemption.",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=78,
    source_height=280,
    unit_suffix=" (£'000s)",
)

# ---------------------------------------------------------------
# Sheet: Asset Quality
# ---------------------------------------------------------------
ASSET_QUALITY_PRESENTATION_NOTE = (
    "Presentation note: scope is the Bank's customer financing book only (Home Purchase Plans + Structured "
    "Real Estate/Commercial Property Finance + Consumer Finance) - Treasury placements and Investment "
    "securities are excluded from this sheet as they are 100% Stage 1 with ~0% coverage every year (pure "
    "treasury exposure, not customer lending; see the Balance Sheet sheet for their carrying values). "
    "'Structured Real Estate' is FY2025's renamed 'Commercial Property Finance' line (same product, see the "
    "Balance Sheet sheet's note). By-IFRS9-stage figures for FY2021-2023 are derived by subtracting Treasury/"
    "Investment securities' Stage 1 exposure (which is disclosed together with customer financing in a "
    "combined 'Total financing assets and ECL' table in those years' own Annual Reports) from that combined "
    "table's totals - Stage 2/3 are unaffected since treasury/investment securities carry none. This nets out "
    "to the exact same figures as the customer-financing-only table both FY2024 and FY2025 disclose directly, "
    "cross-checked line for line. ECL coverage / NPL (Stage 3) ratio / Stage 3 coverage are calculated here "
    "(gross carrying amount and ECL allowance are as disclosed; the ratios are this workbook's own division, "
    "not transcribed from a source document's own rounded coverage % column, so they may differ from a "
    "source table's own coverage % column in the last decimal place). FY2020's own source document has a "
    "genuine internal £1k rounding gap between its combined Stage 3 total (£4,642k) and the by-product Stage 3 "
    "figures it separately discloses (HPP £4,601k + Consumer Finance £40k + nil CPF = £4,641k) - kept as printed "
    "in each of this sheet's own by-product and by-stage sections, not force-corrected; likewise FY2020's "
    "by-product Total ECL allowance (£3,932k) is £1k off its by-stage Total ECL allowance (£3,931k), same "
    "source-document rounding, both kept as printed.\n\n" + ENTITY_NOTE
)

asset_quality_rows = [
    ("SECTION", "Customer financing by product (gross carrying amount)", {}),
    ("DATA", "Home Purchase Plans",
     {"FY2025": 888120, "FY2024": 933121, "FY2023": 994318, "FY2022": 1100598, "FY2021": 1193086, "FY2020": 1195056}),
    ("DATA", "Structured Real Estate / Commercial Property Finance",
     {"FY2025": 1599705, "FY2024": 1181818, "FY2023": 903501, "FY2022": 792082, "FY2021": 671968, "FY2020": 559830}),
    ("DATA", "Consumer Finance", {"FY2025": 57, "FY2024": 55, "FY2023": 62, "FY2022": 64, "FY2021": 47, "FY2020": 40}),
    ("TOTAL", "Total customer financing (gross)",
     {"FY2025": 2487882, "FY2024": 2114994, "FY2023": 1897881, "FY2022": 1892744, "FY2021": 1865101, "FY2020": 1754926}),
    ("SECTION", "Customer financing by product (ECL allowance)", {}),
    ("DATA", "Home Purchase Plans",
     {"FY2025": -1042, "FY2024": -89, "FY2023": -1197, "FY2022": -870, "FY2021": -1102, "FY2020": -1329}),
    ("DATA", "Structured Real Estate / Commercial Property Finance",
     {"FY2025": -10709, "FY2024": -7866, "FY2023": -3815, "FY2022": -2712, "FY2021": -2315, "FY2020": -2563}),
    ("DATA", "Consumer Finance", {"FY2025": -57, "FY2024": -55, "FY2023": -62, "FY2022": -64, "FY2021": -47, "FY2020": -40}),
    ("TOTAL", "Total ECL allowance",
     {"FY2025": -11808, "FY2024": -8010, "FY2023": -5074, "FY2022": -3646, "FY2021": -3464, "FY2020": -3932}),
    ("SECTION", "Customer financing by IFRS 9 stage - gross carrying amount", {}),
    ("DATA", "Stage 1",
     {"FY2025": 2317361, "FY2024": 1944293, "FY2023": 1748008, "FY2022": 1802774, "FY2021": 1713571, "FY2020": 1645461}),
    ("DATA", "Stage 2", {"FY2025": 67436, "FY2024": 91124, "FY2023": 88514, "FY2022": 70443, "FY2021": 143576, "FY2020": 104823}),
    ("DATA", "Stage 3", {"FY2025": 103085, "FY2024": 79577, "FY2023": 61359, "FY2022": 19527, "FY2021": 7954, "FY2020": 4642}),
    ("TOTAL", "Total (gross)",
     {"FY2025": 2487882, "FY2024": 2114994, "FY2023": 1897881, "FY2022": 1892744, "FY2021": 1865101, "FY2020": 1754926}),
    ("SECTION", "Customer financing by IFRS 9 stage - ECL allowance", {}),
    ("DATA", "Stage 1", {"FY2025": -604, "FY2024": -350, "FY2023": -327, "FY2022": -2519, "FY2021": -1279, "FY2020": -1797}),
    ("DATA", "Stage 2", {"FY2025": -50, "FY2024": -155, "FY2023": -142, "FY2022": -106, "FY2021": -1807, "FY2020": -1765}),
    ("DATA", "Stage 3", {"FY2025": -11154, "FY2024": -7505, "FY2023": -4605, "FY2022": -1021, "FY2021": -378, "FY2020": -369}),
    ("TOTAL", "Total ECL allowance",
     {"FY2025": -11808, "FY2024": -8010, "FY2023": -5074, "FY2022": -3646, "FY2021": -3464, "FY2020": -3931}),
    ("SECTION", "Derived ratios", {}),
    ("DATA", "ECL coverage ratio (Total ECL / Total gross)",
     {"FY2025": "0.47%", "FY2024": "0.38%", "FY2023": "0.27%", "FY2022": "0.19%", "FY2021": "0.19%", "FY2020": "0.22%"}),
    ("DATA", "Stage 3 (NPL) ratio (Stage 3 gross / Total gross)",
     {"FY2025": "4.14%", "FY2024": "3.76%", "FY2023": "3.23%", "FY2022": "1.03%", "FY2021": "0.43%", "FY2020": "0.26%"}),
    ("DATA", "Stage 3 coverage ratio (Stage 3 ECL / Stage 3 gross)",
     {"FY2025": "10.82%", "FY2024": "9.43%", "FY2023": "7.51%", "FY2022": "5.23%", "FY2021": "4.75%", "FY2020": "7.95%"}),
]

bw.add_asset_quality_sheet(
    title="Alrayan Bank Limited — Asset Quality / Credit Risk Disclosures",
    subtitle="Customer financing book (HPP + Structured Real Estate/CPF + Consumer Finance), £'000s.",
    rows=asset_quality_rows,
    sources_text=(
        "Sources - Al Rayan Bank's own credit risk note (IFRS 9 staging and by-product gross/ECL/coverage "
        "tables), £'000s, all years:\n"
        f"FY2025: FY2025 Annual Report and Financial Statements, Note 30 'Financial risk management' "
        f"(scanned/image-only - transcribed via visual reading of the rendered pages), pp.73, 75 - "
        f"{AR2025_URL}\n"
        f"FY2024: FY2024 Annual Report and Financial Statements, Note 28/29 'Financing assets' / 'Financial "
        f"risk management', pp.65, 68 - {AR2024_URL}\n"
        f"FY2023: sourced from the FY2024 Annual Report's own FY2023 comparative columns, Note 28/29, "
        f"pp.65, 69 - {AR2024_URL}\n"
        f"FY2022: FY2022 Annual Report and Financial Statements, Note 26 'Financial risk management' "
        f"(scanned/image-only - transcribed via visual reading of the rendered page), p.62 - {AR2022_URL}\n"
        f"FY2021: sourced from the FY2022 Annual Report's own FY2021 comparative table, Note 26, p.63 - "
        f"{AR2022_URL}\n"
        f"FY2020: FY2021 Annual Report and Financial Statements, Note 29 'Financial risk management' - "
        f"'Total financing assets and ECL at 31 December 2020' table (scanned/image-only - transcribed via "
        f"visual reading of the rendered page), p.74 - {AR2021_URL}\n\n"
        + ASSET_QUALITY_PRESENTATION_NOTE
    ),
    first_col_width=58,
    source_height=260,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, f"{unit}" if unit else "", rows_data, sources_text,
                         note=note, first_col_width=52, source_height=200)


# ---------------------------------------------------------------
# KM1 Key Metrics - Alrayan's own published Annex I template, as printed.
#
# Alrayan prints a REDUCED row set: rows UK 7b, UK 7c, UK 8a, UK 9a, 10,
# UK 10a and UK 14a-14e never appear in any edition. Only UK 7a and UK 7d are
# given for the SREP block. The "Additional leverage ratio disclosure
# requirements" section header IS printed in the FY2023 and FY2024 editions
# with no rows beneath it, and is dropped again in the FY2025 edition; it is
# kept here because that is what the bank published.
#
# Amounts are in £m (not £'000 as most banks use for KM1) - that is Alrayan's
# own unit, and matches the rest of this workbook.
#
# Row 12 is printed to whole percents ("38%") while rows 5-7 carry two
# decimals ("15.45%") and rows 14/17/20 one or none - reproduced as printed.
#
# FY2021 and FY2020 are blank: the FY2020 and FY2021 Pillar 3 Disclosures
# pre-date Alrayan's adoption of the Annex I templates and contain no KM1 at
# all (their capital figures come from Executive Summary tables instead, which
# is why the individual metric sheets below still carry those years).
# ---------------------------------------------------------------
km1_rows = [
    ("SECTION", "Available own funds (amounts, £m)", {}),
    ("DATA", "1    Common Equity Tier 1 (CET1) capital",
     {"FY2025": 227.3, "FY2024": 208.2, "FY2023": 183.9, "FY2022": 152.7}),
    ("DATA", "2    Tier 1 capital",
     {"FY2025": 230.3, "FY2024": 211.2, "FY2023": 186.9, "FY2022": 155.7}),
    ("DATA", "3    Total capital",
     {"FY2025": 232.8, "FY2024": 224.9, "FY2023": 205.5, "FY2022": 178.4}),
    ("SECTION", "Risk-weighted exposure amounts (£m)", {}),
    ("DATA", "4    Total risk-weighted exposure amount",
     {"FY2025": 1471.7, "FY2024": 1307.8, "FY2023": 1059.1, "FY2022": 1022.3}),
    ("SECTION", "Capital ratios (as a percentage of risk-weighted exposure amount)", {}),
    ("DATA", "5    Common Equity Tier 1 ratio (%)",
     {"FY2025": "15.45%", "FY2024": "15.95%", "FY2023": "17.36%", "FY2022": "14.93%"}),
    ("DATA", "6    Tier 1 ratio (%)",
     {"FY2025": "15.65%", "FY2024": "16.15%", "FY2023": "17.65%", "FY2022": "15.23%"}),
    ("DATA", "7    Total capital ratio (%)",
     {"FY2025": "15.82%", "FY2024": "17.19%", "FY2023": "19.41%", "FY2022": "17.45%"}),
    ("SECTION", "Additional own funds requirements based on SREP (as a percentage of risk-weighted exposure amount)", {}),
    ("DATA", "UK 7a    Additional CET1 SREP requirements (%)",
     {"FY2025": "1.54%", "FY2024": "1.80%", "FY2023": "1.80%", "FY2022": "2.82%"}),
    ("DATA", "UK 7d    Total SREP own funds requirements (%)",
     {"FY2025": "9.54%", "FY2024": "9.80%", "FY2023": "9.80%", "FY2022": "10.82%"}),
    ("SECTION", "Combined buffer requirement (as a percentage of risk-weighted exposure amount)", {}),
    ("DATA", "8    Capital conservation buffer (%)",
     {"FY2025": "2.50%", "FY2024": "2.50%", "FY2023": "2.50%", "FY2022": "2.50%"}),
    ("DATA", "9    Institution specific countercyclical capital buffer (%)",
     {"FY2025": "1.38%", "FY2024": "1.25%", "FY2023": "1.33%", "FY2022": "0.65%"}),
    ("DATA", "11    Combined buffer requirement (%)",
     {"FY2025": "3.88%", "FY2024": "3.75%", "FY2023": "3.83%", "FY2022": "3.15%"}),
    ("DATA", "UK 11a    Overall capital requirements (%)",
     {"FY2025": "13.42%", "FY2024": "13.55%", "FY2023": "13.63%", "FY2022": "13.97%"}),
    ("DATA", "12    CET1 available after meeting the total SREP own funds requirements (%)",
     {"FY2025": "38%", "FY2024": "38%", "FY2023": "44%", "FY2022": "28%"}),
    ("SECTION", "Leverage ratio (£m / %)", {}),
    ("DATA", "13    Total exposure measure excluding claims on central banks",
     {"FY2025": 3027.0, "FY2024": 2758.0, "FY2023": 2399.4, "FY2022": 2306.6}),
    ("DATA", "14    Leverage ratio excluding claims on central banks (%)",
     {"FY2025": "7.6%", "FY2024": "7.7%", "FY2023": "7.8%", "FY2022": "6.7%"}),
    ("SECTION", "Additional leverage ratio disclosure requirements", {}),
    ("SECTION", "Liquidity Coverage Ratio (£m / %)", {}),
    ("DATA", "15    Total high-quality liquid assets (HQLA) (Weighted value -average)",
     {"FY2025": 249.5, "FY2024": 229.7, "FY2023": 202.1, "FY2022": 173.6}),
    ("DATA", "UK 16a    Cash outflows – Total weighted value",
     {"FY2025": 208.5, "FY2024": 198.3, "FY2023": 132.4, "FY2022": 159.4}),
    ("DATA", "UK 16b    Cash inflows – Total weighted value",
     {"FY2025": 290.2, "FY2024": 344.0, "FY2023": 266.6, "FY2022": 255.1}),
    ("DATA", "16    Total net cash outflows (adjusted value)",
     {"FY2025": 52.1, "FY2024": 49.6, "FY2023": 33.1, "FY2022": 39.8}),
    ("DATA", "17    Liquidity coverage ratio (%)",
     {"FY2025": "481%", "FY2024": "523%", "FY2023": "641%", "FY2022": "442%"}),
    ("SECTION", "Net Stable Funding Ratio (£m / %)", {}),
    ("DATA", "18    Total available stable funding",
     {"FY2025": 2540.2, "FY2024": 2331.0, "FY2023": 2071.3, "FY2022": 1982.3}),
    ("DATA", "19    Total required stable funding",
     {"FY2025": 1687.6, "FY2024": 1449.3, "FY2023": 1321.3, "FY2022": 1280.8}),
    ("DATA", "20    NSFR ratio (%)",
     {"FY2025": "151%", "FY2024": "161%", "FY2023": "157%", "FY2022": "155%"}),
]

KM1_SOURCES = p3_sources(
    "KM1 presentation notes:\n"
    "• Alrayan publishes the table under the heading \"Key Metrics Template – KM1\" in Annex I of each "
    "Pillar 3 Disclosures document, in £m. Rows are reproduced in the bank's own order with its own "
    "template row numbers and printed precision.\n"
    "• REDUCED ROW SET: Alrayan has never printed rows UK 7b, UK 7c, UK 8a, UK 9a, 10, UK 10a or "
    "UK 14a-14e in any edition — only UK 7a and UK 7d appear in the SREP block. Those rows are absent "
    "here rather than shown blank, because the bank's template does not contain them.\n"
    "• The \"Additional leverage ratio disclosure requirements\" heading is printed with no rows beneath "
    "it in the FY2023 and FY2024 editions and is dropped entirely in the FY2025 edition. It is retained here "
    "as published.\n"
    "• UK 16b (cash inflows) exceeds UK 16a (cash outflows) in every year. That is as published and is "
    "why row 16 (net outflows) is not 16a minus 16b: the LCR calculation caps recognised inflows at 75% of "
    "outflows, so the excess inflow is disregarded.\n"
    "• Row 12 is printed to whole percents while rows 5-7 carry two decimals; that mixed precision is "
    "the bank's own.\n"
    "• FY2021 and FY2020 are blank: the Pillar 3 Disclosures for those years pre-date Alrayan's adoption "
    "of the Annex I templates and contain no key-metrics table. The FY2021/FY2020 figures on the individual "
    "metric sheets in this workbook come from those editions' Executive Summary tables instead."
)

bw.add_km1_sheet(
    title="Alrayan Bank Limited — KM1 Key Metrics",
    subtitle="The bank's own published UK KM1 template (Annex I of its Pillar 3 Disclosures), reproduced in "
             "Alrayan's row order with its own template row numbers and printed precision. Amounts in £m, "
             "ratios as printed. FY2021 and FY2020 pre-date the template and are intentionally blank.",
    rows=km1_rows,
    sources_text=KM1_SOURCES,
)


metric(
    "CET1 Capital", "£m",
    [("Common Equity Tier 1 (CET1) capital", {"FY2025": 227.3, "FY2024": 208.2, "FY2023": 183.9, "FY2022": 152.7, "FY2021": 142.4, "FY2020": 135.7})],
    p3_sources(),
)

metric(
    "CET1 Ratio", "% of RWA",
    [("CET1 ratio", {"FY2025": "15.45%", "FY2024": "15.95%", "FY2023": "17.36%", "FY2022": "14.93%", "FY2021": "15.1%", "FY2020": "13.4%"})],
    p3_sources("FY2020-FY2021 are from the pre-KM1 Executive Summary table (rounded to 1dp in the source); "
               "FY2022-FY2024 are from the formal KM1 Annex template (2dp)."),
)

metric(
    "Tier 1 Capital", "£m",
    [("Tier 1 capital", {"FY2025": 230.3, "FY2024": 211.2, "FY2023": 186.9, "FY2022": 155.7, "FY2021": 145.4, "FY2020": 138.7})],
    p3_sources(),
)

metric(
    "Tier 1 Ratio", "% of RWA",
    [("Tier 1 ratio", {"FY2025": "15.65%", "FY2024": "16.15%", "FY2023": "17.65%", "FY2022": "15.23%", "FY2021": "15.4%", "FY2020": "13.7%"})],
    p3_sources(),
)

metric(
    "Total Capital", "£m",
    [("Total capital", {"FY2025": 232.8, "FY2024": 224.9, "FY2023": 205.5, "FY2022": 178.4, "FY2021": 170.4, "FY2020": 163.7})],
    p3_sources(),
)

metric(
    "Total Capital Ratio", "% of RWA",
    [("Total capital ratio", {"FY2025": "15.82%", "FY2024": "17.19%", "FY2023": "19.41%", "FY2022": "17.45%", "FY2021": "18.1%", "FY2020": "16.2%"})],
    p3_sources(),
)

metric(
    "Total RWAs", "£m",
    [("Total risk-weighted assets", {"FY2025": 1471.7, "FY2024": 1307.8, "FY2023": 1059.1, "FY2022": 1022.3, "FY2021": 943.9, "FY2020": 1012.5})],
    p3_sources(),
)

# ---------------------------------------------------------------
# Sheet: RWA Breakdown
# ---------------------------------------------------------------
RWA_BREAKDOWN_PRESENTATION_NOTE = (
    "Presentation note: FY2025 was added 2026-09-15 from the newly published FY2025 Pillar 3 Disclosures' "
    "own Annex I OV1 template (p.40). FY2020-FY2021's Pillar 3 editions pre-date the bank's adoption of the "
    "standardised UK OV1 template - their 'Table 7/8: Pillar 1 capital requirements: credit risk' presents "
    "credit risk RWA together with small counterparty-credit-risk-like 'Commitment to finance' and 'Sharia "
    "compliant derivatives' categories as one combined total (£937.3m FY2020, £865.1m FY2021), rather than the "
    "later editions' separate 'Credit risk (excluding CCR)' / 'Counterparty credit risk - CCR' OV1 line split - "
    "so FY2020/FY2021's Credit risk cells below are those combined figures, and the CCR cells are left blank "
    "rather than force-split. Every year's Total ties out exactly to the pre-existing Total RWAs sheet.\n\n"
    + ENTITY_NOTE
)

rwa_breakdown_rows = [
    ("SECTION", "Risk-weighted exposure amounts (£m)", {}),
    ("DATA", "Credit risk (excluding CCR)", {"FY2025": 1335.0, "FY2024": 1184.1, "FY2023": 950.5, "FY2022": 936.3}),
    ("DATA", "Credit risk (incl. commitments/Sharia-compliant derivatives, pre-OV1 combined basis)",
     {"FY2021": 865.1, "FY2020": 937.3}),
    ("DATA", "Counterparty credit risk (CCR)", {"FY2025": 14.2, "FY2024": 6.4, "FY2023": 3.2, "FY2022": 0.1}),
    ("DATA", "Operational risk", {"FY2025": 122.5, "FY2024": 117.3, "FY2023": 105.4, "FY2022": 85.9, "FY2021": 78.8, "FY2020": 75.2}),
    ("TOTAL", "Total risk-weighted exposure amounts",
     {"FY2025": 1471.7, "FY2024": 1307.8, "FY2023": 1059.1, "FY2022": 1022.3, "FY2021": 943.9, "FY2020": 1012.5}),
]

bw.add_rwa_breakdown_sheet(
    title="Alrayan Bank Limited — RWA Breakdown (UK OV1)",
    subtitle="Bank entity-level basis, £m.",
    rows=rwa_breakdown_rows,
    sources_text=(
        "Sources - Alrayan Bank Limited's own Pillar 3 Disclosures, UK OV1 'Overview of risk weighted exposure "
        "amounts' template (or its pre-KM1 equivalent for FY2020-FY2021), £m, all years:\n"
        f"FY2025: Pillar 3 Disclosures - 31 December 2025, Annex I OV1 table, p.40 - {P3_2025_URL}\n"
        f"FY2024: Pillar 3 Disclosures - 31 December 2024, Annex I OV1 table, p.39 - {P3_2024_URL}\n"
        f"FY2023: Pillar 3 Disclosures - 31 December 2023, Annex I OV1 table, p.34 - {P3_2023_URL}\n"
        f"FY2022: sourced from the FY2023 Pillar 3 Disclosures' own FY2022 comparative column, Annex I OV1 "
        f"table, p.34 - {P3_2023_URL}\n"
        f"FY2021: Pillar 3 Disclosures - 31 December 2021, Table 7 'Pillar 1 capital requirements: credit "
        f"risk' + Table 29 'Operational risk RWAs flow statement', pp.18, 31 - {P3_2021_URL}\n"
        f"FY2020: Pillar 3 Disclosures - 31 December 2020, Table 34 'Overview of RWA & Pillar I' + Table 29 "
        f"'Operational risk RWAs flow statement', pp.30, 26 - {P3_2020_URL}\n"
        + RWA_BREAKDOWN_PRESENTATION_NOTE
    ),
    first_col_width=64,
    source_height=220,
    unit_suffix=" (£m)",
)

metric(
    "Leverage Ratio", "%",
    [("Leverage ratio", {"FY2025": "7.6%", "FY2024": "7.7%", "FY2023": "7.8%", "FY2022": "6.7%", "FY2021": "6.4%", "FY2020": "5.9%"})],
    p3_sources(),
    note="FY2022-FY2024 are on the 'excluding claims on central banks' KM1 basis; FY2020-FY2021 (5.9%/6.4%) are "
         "on the older CRR/LRSum basis, from before the PRA's leverage-framework methodology change (PRA "
         "PS21/21) - not directly comparable, same industry-wide basis break documented for several other banks "
         "in this project.",
)

metric(
    "LCR", "%",
    [("Liquidity Coverage Ratio (12-month average, KM1 basis)",
      {"FY2025": "481%", "FY2024": "523%", "FY2023": "641%", "FY2022": "442%", "FY2021": "316%", "FY2020": "352%"})],
    p3_sources(),
    note="This bank's Pillar 3 documents disclose TWO different LCR figures each year: a spot/point-in-time "
         "figure in the Executive Summary (FY2020 288%, FY2021 635%, FY2022 458%, FY2023 786%, FY2024 746% - "
         "none of these used here) and a 12-month AVERAGE figure in the formal KM1/Annex template (used here, "
         "for consistency with every other bank in this project and the standard regulatory template). "
         "FY2020-FY2021's average figures come from a dedicated 'Analysis of the Bank's average liquidity "
         "coverage ratio' table rather than a KM1 template (those editions pre-date the bank's KM1 adoption).",
)

metric(
    "NSFR", "%",
    [("Net Stable Funding Ratio", {"FY2025": "151%", "FY2024": "161%", "FY2023": "157%", "FY2022": "155%", "FY2021": "146%", "FY2020": "145%"})],
    p3_sources(),
)

# GA-020 (2026-09-19). The FY2022 Pillar 3 edition EXISTS and is live on the Bank's own host, under a filename
# that does not say "2022" (found via Wayback CDX of alrayanbank.co.uk, filter mimetype:application/pdf, then
# fetched live: HTTP 200, application/pdf, %PDF, 32 pages, cover 'Pillar 3 Disclosures 31 December 2022').
# It is recorded here for the MREL search only; the KM1/OV1 FY2022 columns elsewhere in this script still come
# from the FY2023 edition's comparative and have NOT been re-sourced in this pass (flagged to the coordinator).
P3_2022_URL = ("https://www.alrayanbank.co.uk/sites/default/files/media/file-uploads/2023-08/"
               "al_rayan_pillar_three_32pp_brochure_-_final.pdf")
bw.add_not_disclosed_metric_sheets(
    ["MREL Ratio"],
    p3_sources(),
    statements={"MREL Ratio": ("Not published – no MREL figure or reference in this year's Pillar 3 (all six "
                               "editions FY2020-FY2025 full-text searched 2026-09-19, zero 'MREL')")},
    per_note={
        "MREL Ratio": "MREL is not mentioned anywhere in the FY2020, FY2021, FY2022, FY2023, FY2024 or FY2025 Pillar 3 "
                      "Disclosures (full-text searched 2026-09-19 for 'MREL', 'minimum requirement for own funds' and "
                      "'eligible liabilities': no hits, against 98-115 hits for 'capital' per edition). The FY2022 "
                      "edition is " + P3_2022_URL + " . The FY2024 annual report's single 'eligible liabilities' hit "
                      "is the Bank of England cash ratio deposit scheme, not MREL. Consistent with a bank of this size "
                      "not being its own resolution entity under the Bank of England's MREL framework.",
    },
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets",
         {"FY2025": 3125432, "FY2024": 2835724, "FY2023": 2493218, "FY2022": 2400294, "FY2021": 2258891, "FY2020": 2339821}),
        ("Loans and advances to customers (HPP + SRE/CPF)",
         {"FY2025": 2476074, "FY2024": 2106984, "FY2023": 1892807, "FY2022": 1889098, "FY2021": 1861637, "FY2020": 1750994}),
        ("Customer deposits",
         {"FY2025": 2477658, "FY2024": 2412883, "FY2023": 2149200, "FY2022": 2044149, "FY2021": 1959663, "FY2020": 1965001}),
        ("Total equity",
         {"FY2025": 234003, "FY2024": 216474, "FY2023": 195138, "FY2022": 167315, "FY2021": 157311, "FY2020": 150056}),
    ],
    balance_sheet_unit="£'000",
    income_statement_totals=[
        ("Total income",
         {"FY2025": 64204, "FY2024": 63431, "FY2023": 68397, "FY2022": 55807, "FY2021": 44396, "FY2020": 39109}),
        ("Total operating expense",
         {"FY2025": -40617, "FY2024": -39962, "FY2023": -37789, "FY2022": -35010, "FY2021": -34769, "FY2020": -34911}),
        ("Profit for the financial year",
         {"FY2025": 17681, "FY2024": 17717, "FY2023": 23028, "FY2022": 16500, "FY2021": 9003, "FY2020": 3838}),
    ],
    income_statement_unit="£'000",
    equity_changes_totals=[
        ("Opening equity",
         {"FY2025": 216474, "FY2024": 195138, "FY2023": 167315, "FY2022": 157311, "FY2021": 150056, "FY2020": 145821}),
        ("Total comprehensive income for the year",
         {"FY2025": 17906, "FY2024": 21618, "FY2023": 28104, "FY2022": 10847, "FY2021": 7255, "FY2020": 4235}),
        ("Other equity movements, net",
         {"FY2025": -377, "FY2024": -282, "FY2023": -281, "FY2022": -843, "FY2021": 0, "FY2020": 0}),
        ("Closing equity",
         {"FY2025": 234003, "FY2024": 216474, "FY2023": 195138, "FY2022": 167315, "FY2021": 157311, "FY2020": 150056}),
    ],
    equity_changes_unit="£'000",
    cash_flow_totals=[
        ("Net cash from/(used in) operating activities",
         {"FY2025": -224043, "FY2024": 57743, "FY2023": 91802, "FY2022": 130869, "FY2021": -35992, "FY2020": 24526}),
        ("Net cash from/(used in) investing activities",
         {"FY2025": -98427, "FY2024": 5682, "FY2023": -40037, "FY2022": -23143, "FY2021": 45657, "FY2020": 57440}),
        ("Net cash from/(used in) financing activities",
         {"FY2025": 70792, "FY2024": 78142, "FY2023": -3574, "FY2022": -1978, "FY2021": -148456, "FY2020": -35489}),
        ("Closing cash and cash equivalents",
         {"FY2025": 287372, "FY2024": 539046, "FY2023": 397753, "FY2022": 349828, "FY2021": 244090, "FY2020": 385376}),
    ],
    cash_flow_unit="£'000s",
    ratios=[
        ("CET1 Ratio", {"FY2025": "15.45%", "FY2024": "15.95%", "FY2023": "17.36%", "FY2022": "14.93%", "FY2021": "15.1%", "FY2020": "13.4%"}),
        ("Tier 1 Ratio", {"FY2025": "15.65%", "FY2024": "16.15%", "FY2023": "17.65%", "FY2022": "15.23%", "FY2021": "15.4%", "FY2020": "13.7%"}),
        ("Total Capital Ratio", {"FY2025": "15.82%", "FY2024": "17.19%", "FY2023": "19.41%", "FY2022": "17.45%", "FY2021": "18.1%", "FY2020": "16.2%"}),
        ("Leverage Ratio", {"FY2025": "7.6%", "FY2024": "7.7%", "FY2023": "7.8%", "FY2022": "6.7%", "FY2021": "6.4%", "FY2020": "5.9%"}),
        ("LCR", {"FY2025": "481%", "FY2024": "523%", "FY2023": "641%", "FY2022": "442%", "FY2021": "316%", "FY2020": "352%"}),
        ("NSFR", {"FY2025": "151%", "FY2024": "161%", "FY2023": "157%", "FY2022": "155%", "FY2021": "146%", "FY2020": "145%"}),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own source "
         "citation for the underlying document/page. CORRECTION, 18 September 2026 (KM1-032): this note "
         "previously read 'Pillar 3 ratios and RWA Breakdown are blank for FY2025 (no Pillar 3 disclosure "
         "published yet)'. That sentence was true when written and became false on 2026-09-15, when Alrayan's "
         "FY2025 Pillar 3 Disclosures appeared and every FY2025 Pillar 3 cell in this workbook was transcribed "
         "from its Annex I KM1/OV1 templates. The detail sheets were updated in that pass; this Overview block "
         "was not, so it carried a stale non-publication claim beside sheets that already held the figures. "
         "FY2025 is now filled here too, from the same KM1 Annex source the detail sheets cite. "
         "LCR uses the 12-month average/KM1 basis throughout, not the "
         "spot figures also disclosed in this bank's own Executive Summary tables - see the LCR sheet's note. "
         "'Loans and advances to customers' combines Home Purchase Plans and Structured Real Estate/Commercial "
         "Property Finance (Al Rayan's Sharia-compliant financing products, functionally equivalent to "
         "loans/mortgages at a conventional bank). 'Other equity movements, net' combines the Additional Tier 1 "
         "profit payment and the small profit-stabilisation-reserve/share-premium-cancellation transfers each "
         "year - see the Statement of Changes in Equity sheet for the full breakdown. FY2020's own cash flow "
         "figures are on a pre-restatement classification basis and do not tie exactly into FY2021's opening "
         "cash figure - see the Cash Flow Statement sheet's own source note for the full explanation.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/ALRAYAN BANK FINANCIALS.xlsx")
