import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021", "FY2020", "FY2019", "FY2018", "FY2017", "FY2016"]
YEAR_LABEL = {y: y for y in YEARS}

AR2025_URL = "https://find-and-update.company-information.service.gov.uk/company/01311315/filing-history/MzUyMTMxMjk3OWFkaXF6a2N4/document?format=pdf&download=0"
AR2025_WEBSITE_URL = "https://www.htb.co.uk/htbcontent/uploads/2026/04/HTB_Annual_Report_2025.pdf"
AR2024_URL = "https://find-and-update.company-information.service.gov.uk/company/01311315/filing-history/MzQ2NTc0NTU3N2FkaXF6a2N4/document?format=pdf&download=0"
AR2023_URL = "https://find-and-update.company-information.service.gov.uk/company/01311315/filing-history/MzQyNDU2MzAzMmFkaXF6a2N4/document?format=pdf&download=0"
AR2022_URL = "https://find-and-update.company-information.service.gov.uk/company/01311315/filing-history/MzM4ODU3ODUzOWFkaXF6a2N4/document?format=pdf&download=0"
AR2021_URL = "https://find-and-update.company-information.service.gov.uk/company/01311315/filing-history/MzM0MjI1MzEyMmFkaXF6a2N4/document?format=pdf&download=0"
AR2020_CH_URL = "https://find-and-update.company-information.service.gov.uk/company/01311315/filing-history/MzMwMjA1NDQ0MWFkaXF6a2N4/document?format=pdf&download=0"
AR2020_WEBSITE_URL = "https://www.htb.co.uk/htbcontent/uploads/2021/11/HTB_Annual_Report_2020.pdf"
AR2019_CH_URL = "https://find-and-update.company-information.service.gov.uk/company/01311315/filing-history/MzI3MTk4MjMzN2FkaXF6a2N4/document?format=pdf&download=0"
AR2018_CH_URL = "https://find-and-update.company-information.service.gov.uk/company/01311315/filing-history/MzIzNzQ4OTc1NWFkaXF6a2N4/document?format=pdf&download=0"
AR2017_CH_URL = "https://find-and-update.company-information.service.gov.uk/company/01311315/filing-history/MzIwNDA2OTI3M2FkaXF6a2N4/document?format=pdf&download=0"
AR2017_WEBSITE_URL = "https://www.htb.co.uk/htbcontent/uploads/2019/08/Hampshire-Trust-Bank-HTB-2017-Annual-Report-1.pdf"
AR2016_CH_URL = "https://find-and-update.company-information.service.gov.uk/company/01311315/filing-history/MzE3NDY4MzczMWFkaXF6a2N4/document?format=pdf&download=0"
AR2016_WEBSITE_URL = "https://www.htb.co.uk/htbcontent/uploads/2019/08/Hampshire-Trust-Bank-HTB-2016-Annual-Report-1.pdf"

P3_2025_URL = "https://www.htb.co.uk/htbcontent/uploads/2026/04/HTB_Pillar_3_Disclosures_2025.pdf"
P3_2024_URL = "https://www.htb.co.uk/htbcontent/uploads/2025/07/HTB_Pillar_3_Disclosures_2024.pdf"
P3_2023_URL = "https://www.htb.co.uk/htbcontent/uploads/2024/06/HTB_Pillar_3_Disclosures_2023.pdf"
P3_2022_URL = "https://www.htb.co.uk/htbcontent/uploads/2023/08/Hampshire-Trust-Bank-HTB-2022-Pillar-3-Disclosures.pdf"
P3_2021_URL = "https://www.htb.co.uk/htbcontent/uploads/2022/07/Hampshire-Trust-Bank-HTB-2021-Pillar-3-Disclosures.pdf"
P3_2020_URL = "https://www.htb.co.uk/htbcontent/uploads/2021/07/Hampshire-Trust-Bank-HTB-2020-Pillar-3-Disclosures.pdf"
P3_2019_URL = "https://www.htb.co.uk/htbcontent/uploads/2020/07/Hampshire-Trust-Bank-HTB-2019-Pillar-3-Disclosures.pdf"
P3_2018_URL = "https://www.htb.co.uk/htbcontent/uploads/2019/08/Hampshire-Trust-Bank-HTB-2018-Pillar-3-Disclosures-1.pdf"
P3_2017_URL = "https://www.htb.co.uk/htbcontent/uploads/2019/08/Hampshire-Trust-Bank-HTB-2017-Pillar-3-Disclosures-1.pdf"
P3_2016_URL = "https://www.htb.co.uk/htbcontent/uploads/2019/08/Hampshire-Trust-Bank-HTB-2016-Pillar-3-Disclosures-1.pdf"

PRE_GROUP_NOTE = (
    "FY2016-FY2020 all predate HTB's Group consolidation (first subsidiary acquired during FY2022) and use "
    "the Bank's own single (pre-Group-split) statements/disclosures throughout - there is no separate "
    "Group/Bank column to choose between in any of these 5 years. FY2016-FY2017 also predate IFRS 9 (adopted "
    "1 Jan 2018, not restated in comparatives), IFRS 16 leases (adopted 1 Jan 2019) and any subordinated debt "
    "or central bank facility drawn that early (Central Bank Facilities first drawn FY2017; Subordinated "
    "Liabilities first issued FY2018) - rows that don't exist yet in a given year are left blank rather than "
    "assumed zero, except where that year's own report explicitly discloses a nil/dash balance for a line "
    "item that does exist that year (entered as 0)."
)

STATEMENTS_ENTITY_NOTE = (
    "Balance Sheet, Profit & Loss and Statement of Changes in Equity all use the Bank (parent-entity, "
    "non-consolidated) column, matching the entity-level basis used throughout this workbook. Every "
    "year's own originally-published figures are used (e.g. FY2023 comes from HTB's own FY2023 Annual "
    "Report, FY2024 from its own FY2024 report), not a later restated comparative column - confirmed "
    "identical between each year's own report and the next year's comparative column in every case "
    "checked. FY2021 and earlier all predate any Group consolidation (first subsidiary acquired during "
    "FY2022) and predate HTB's use of cash-flow hedge accounting - no Cash flow hedge reserve, Investment "
    "in subsidiaries, or Other equity instruments (non-controlling interest) balance exists in any of "
    "FY2016-FY2021. Corporation tax asset is only broken out as its own Balance Sheet line from FY2025 "
    "onward - FY2024 and earlier years fold it into Other assets (confirmed: FY2024's Other assets of "
    "227,921 = the 226,100 shown in the FY2025 report's restated FY2024 comparative plus that year's "
    "1,821 Corporation tax asset, transcribed here on each year's own originally-disclosed basis, i.e. "
    "undivided).\n"
    + PRE_GROUP_NOTE +
    "\nA 'Fair value through OCI reserve' equity component (distinct from the later Cash flow hedge "
    "reserve - it holds fair value movements on debt securities held at FVOCI, not derivative hedge "
    "movements) exists only in FY2018-FY2020 (FY2018: £(50)k, FY2019/FY2020: £0, i.e. genuinely nil those "
    "two years, not undisclosed) - added as its own row since it is not the same reserve as the Cash flow "
    "hedge reserve used from FY2022 onward. FY2018's Balance Sheet Deferred Tax Liabilities line (£13k, "
    "no equivalent row in this workbook's standard shape) is folded into that year's Other liabilities "
    "figure (11,886 + 13 = 11,899) so the liabilities total still ties exactly to the £898,423k disclosed "
    "total. Provisions for Liabilities is disclosed as its own Balance Sheet line only FY2016-FY2018 "
    "(FY2016: £36k, FY2017: £303k, FY2018: £0, i.e. genuinely nil that year) - folded into Other "
    "liabilities from FY2019 onward, where it is no longer broken out as a separate line at all."
)

ENTITY_NOTE = (
    "All Cash Flow Statement figures use the Bank (parent-entity, non-consolidated) column, matching the "
    "entity-level basis of the Pillar 3 disclosures below. HTB's FY2021 Annual Report predates any Group "
    "consolidation (its first subsidiary was acquired during FY2022, see the Investing Activities section), "
    "so FY2021 presents a single unified Company statement rather than separate Group/Bank columns - that "
    "single column is used here. The FY2025 Companies House filing (the source used for every other year) is "
    "missing page 64 of its own PDF (the Statement of Cash Flows' operating-activities page - printed page "
    "numbers jump 63 to 65 with no page 64 present in the scan); the operating-activities detail for FY2025 "
    "was instead sourced from the identical statement in HTB's own website copy of the same Annual Report, "
    "which is text-native and paginates differently. Every other line item and every other year comes from "
    "the Companies House filings.\n"
    "IMPORTANT - a genuine FY2020/FY2021 discontinuity, not an error: FY2021's own Annual Report restates "
    "its FY2020 comparative cash flow column (explicitly labelled '(Restated)', with 'Note 6.22 provides "
    "further detail on the nature and value of the restatement to the prior year statement of cash flows') "
    "- the restated FY2020 figures differ from FY2020's own originally-published statement transcribed here "
    "(e.g. Net cash flow from operating activities: originally £96,228k, restated £86,669k; Cash and cash "
    "equivalents at 31 December 2020: originally £156,707k, restated £144,672k - the latter is what FY2021's "
    "own column uses as its opening balance, per that year's own report, unchanged from before this ticket). "
    "Per this project's established convention (each year's own originally-published figures, not a later "
    "restated comparative), the FY2020 column here uses FY2020's own Annual Report throughout - so FY2020's "
    "closing cash (£156,707k) does not tie to FY2021's opening cash (£144,672k) in this workbook, a real, "
    "disclosed source discontinuity rather than a transcription gap. The restatement also introduced a new "
    "'Decrease/(increase) in collateral held with banks' reconciling line for FY2020 (£(9,559)k in the "
    "restated comparative) that FY2020's own originally-published statement does not show at all - left "
    "blank on the FY2020 column here for the same reason.\n"
    "FY2016-FY2020 also each present a single unified Company statement (same pre-Group basis as FY2021). "
    "FY2016-FY2017 are sourced from HTB's own website copies of those Annual Reports (text-native PDFs); the "
    "Companies House filings for those two years are themselves scanned image-only PDFs with no text layer "
    "at all (confirmed via pdffonts - zero embedded fonts), so the website copies - identical statements, "
    "confirmed by their own FY2017-into-FY2016-comparative tie-out - were used instead. FY2018 and FY2019 "
    "have no equivalent text-native website copy of their own Annual Report (the website only carries their "
    "Pillar 3 disclosures, not the Annual Report itself), so those two years were read directly from the "
    "scanned Companies House filing's page images. FY2020 is sourced from HTB's own website copy (text-native)."
)

CASH_FLOW_SOURCES = (
    "Sources - Hampshire Trust Bank Plc's own Consolidated and Bank Statement of Cash Flows (Bank column):\n"
    f"FY2025: Group Annual Report and Accounts 2025 (Companies House, filed 13 May 2026), p.64-65 - {AR2025_URL}\n"
    f"  (operating-activities section from HTB's own website copy of the same report, p.32 - {AR2025_WEBSITE_URL})\n"
    f"FY2024: Annual Report and Accounts for the year ended 31 December 2024 (Companies House, filed 13 May 2025), p.74-75 - {AR2024_URL}\n"
    f"FY2023: Annual Report and Accounts for the year ended 31 December 2023 (Companies House, filed 11 Jun 2024), p.74-75 (FY2023 comparative column) - {AR2023_URL}\n"
    f"FY2022: Annual Report and Accounts for the year ended 31 December 2022 (Companies House, filed 07 Aug 2023), p.61-62 - {AR2022_URL}\n"
    f"FY2021: Annual Report and Accounts for the year ended 31 December 2021 (Companies House, filed 14 Jun 2022), p.54, Statement of Cash flows - {AR2021_URL}\n"
    f"FY2020: Annual Report and Accounts 2020 (HTB website copy, text-native), p.55 - {AR2020_WEBSITE_URL}\n"
    f"  (Companies House filing of the same report, filed 29 May 2021 - {AR2020_CH_URL})\n"
    f"FY2019: Annual Report and Accounts for the year ended 31 December 2019 (Companies House, filed 02 Jul 2020, scanned/image-only), p.47, Statement of Cash flows - {AR2019_CH_URL}\n"
    f"FY2018: Annual Report and Accounts for the year ended 31 December 2018 (Companies House, filed 24 Jun 2019, scanned/image-only), p.39, Statement of Cashflows - {AR2018_CH_URL}\n"
    f"FY2017: Annual Report and Accounts 2017 (HTB website copy, text-native), p.38, Statement of Cashflows - {AR2017_WEBSITE_URL}\n"
    f"  (Companies House filing of the same report, filed 03 May 2018, scanned/image-only - {AR2017_CH_URL})\n"
    f"FY2016: Annual Report and Accounts 2016 (HTB website copy, text-native), p.30, Statement of Cashflows - {AR2016_WEBSITE_URL}\n"
    f"  (Companies House filing of the same report, filed 02 May 2017, scanned/image-only - {AR2016_CH_URL})\n"
    + ENTITY_NOTE
)


def p3_sources(km1_page="10-11"):
    return (
        "Sources - Hampshire Trust Bank Plc Pillar 3 Disclosures, 'Key Metrics' (KM1) table, Bank column "
        "(Group column used only for LCR/NSFR, which HTB discloses only at consolidated/Group level - 'Liquidity "
        "is managed on a consolidated basis hence only Group metrics are reported'; FY2021 and earlier all "
        "predate the Group/Bank split entirely and show a single value used for every metric in those years; "
        "FY2016-FY2020 predate the KM1 template itself and instead use each year's own 'Summary of key ratios' "
        "table plus its Capital Resources/Capital Adequacy section for CET1/Tier 1/Total Capital £ amounts):\n"
        f"FY2025: Pillar 3 Disclosures | 31 December 2025, p.{km1_page} - {P3_2025_URL}\n"
        f"FY2024: Pillar 3 Disclosures | 31 December 2024, p.9-10 - {P3_2024_URL}\n"
        f"FY2023: Pillar 3 Disclosures | 31 December 2023, p.10-11 - {P3_2023_URL}\n"
        f"FY2022: Pillar 3 Disclosures | 31 December 2022, p.10-11 - {P3_2022_URL}\n"
        f"FY2021: Pillar 3 Disclosures | 31 December 2021, Key Metrics table - {P3_2021_URL}\n"
        f"FY2020: Pillar 3 Disclosures | 31 December 2020, Section 4.2/4.3/4.5 (Minimum capital requirement/Leverage Ratio/Liquidity Coverage Ratio) plus Capital Resources table - {P3_2020_URL}\n"
        f"FY2019: Pillar 3 Disclosures | 31 December 2019, Section 5.2/5.4/5.5 plus Capital Resources table - {P3_2019_URL}\n"
        f"FY2018: Pillar 3 Disclosures | 31 December 2018, Section 4.2/4.3/4.4 plus Capital Resources table - {P3_2018_URL}\n"
        f"FY2017: Pillar 3 Disclosures | 31 December 2017, Section 4.1/4.2/4.3/4.4 (Capital Adequacy/Minimum capital requirement/Leverage Ratio/LCR) - {P3_2017_URL}\n"
        f"FY2016: Pillar 3 Disclosures | 31 December 2016, Section 1.5 (Summary of key ratios)/Section 8 (Capital Adequacy) - {P3_2016_URL}\n"
        "MREL is not mentioned anywhere in any year's Pillar 3 disclosure (FY2016-FY2025) - not publicly "
        "disclosed. NSFR is likewise never mentioned in any FY2016-FY2020 disclosure (the concept isn't "
        "introduced in HTB's own Pillar 3 reports until FY2021) - genuinely not disclosed those years, not a "
        "gap in this transcription.\n"
        "Tier 1 capital equals CET1 capital in every year FY2016-FY2020 (no Additional Tier 1 instrument "
        "existed until the Other equity instruments (non-controlling interests) issued in FY2022) - see the "
        "Tier 1 Capital sheet's own note. Total Capital = Tier 1 + Tier 2 from FY2018 onward (Tier 2 = "
        "Subordinated Liabilities, first issued FY2018); FY2016-FY2017 had no Tier 2 capital at all, so Total "
        "Capital = Tier 1 = CET1 those two years too.\n"
        "Each year's own 'Summary of key ratios' table prints a 'Risk weighted assets (£000)' line that is "
        "systematically inconsistent with that same table's own displayed CET1/Total Capital ratios in every "
        "one of FY2018-FY2020: recomputing CET1 capital / RWA against the printed RWA figure gives a ratio "
        "1-2pp off the printed ratio, while the more granular COREP 'Total risk exposure amount' figure found "
        "elsewhere in each of those 3 documents (746,201 for FY2018, 831,229 for FY2019, 809,489 for FY2020) "
        "reproduces the printed ratios almost exactly (e.g. FY2018: 121,690/746,201 = 16.31%, matching the "
        "document's own precise COREP disclosure of 16.31% CET1 exactly, vs 121,690/687,497 = 17.70% using the "
        "summary table's own printed RWA line). The Total RWAs sheet below therefore uses the COREP figure for "
        "FY2018-FY2020, not the mismatched summary-table figure - a genuine, recurring source-document "
        "inconsistency, not a transcription error introduced here. FY2016/FY2017 have no COREP template to "
        "cross-check against, so their summary-table RWA figures (430,807/529,157) are used as-is despite a "
        "smaller (~1pp) rounding gap against their own printed ratios.\n"
        "RESOLVED 2026-09-15 (RWA cross-sheet sweep - do not re-flag): what HTB's headline 'Risk weighted "
        "assets' line actually measures in FY2016-FY2017 is now established from the documents, not inferred. "
        "The FY2017 Pillar 3 p.12 credit-risk exposure-class table foots to exactly 529,157 in its own RWAs "
        "column (42,100 + 67,276 + 264,058 + 142,500 + 6,229 + 0 + 2,233 + 4,763), i.e. the headline line is "
        "CREDIT-RISK RWA ONLY and excludes the separately-disclosed operational risk requirement (FY2017 "
        "3,136 -> 39,200 RWA; FY2016 1,189 -> 14,863 RWA). The FY2018 document proves the same structure "
        "directly: its summary line reads 687,497 while its own COREP row 010 'Total risk exposure amount' on "
        "the same document reads 746,201 - a 58,704 difference matching that year's operational risk RWA "
        "(4,677/0.08 = 58,463). HTB's own printed ratios are computed on the credit-only denominator too "
        "(total regulatory capital 113,435 / 529,157 = 21.44%, matching the printed 21%; against 568,357 it "
        "would be 19.96%, i.e. 20%), so the printed ratio cannot be used to overturn the printed total the way "
        "it was for Redwood. HTB has never published a FY2016 or FY2017 total risk exposure amount in any "
        "document (Pillar 3 or Annual Report - AR2017 and AR2016 repeat the same 529,157/430,807), so there is "
        "no transcribable replacement; credit + operational would be arithmetic, which this project does not "
        "substitute for a disclosed figure. FY2016/FY2017 therefore knowingly hold a credit-risk-only figure, "
        "and the FY2017 -> FY2018 step in this series carries a basis change (credit-only -> COREP total) on "
        "top of real balance-sheet growth. See the RWA Breakdown sheet for the two components."
    )


bw = BankWorkbook(bank_name="Hampshire Trust Bank Plc", years=YEARS, year_label=YEAR_LABEL, header_color="DD741F")

# ---------------------------------------------------------------
# Sheet: Balance Sheet (Bank / entity-level column)
# ---------------------------------------------------------------
BS_SOURCES = (
    "Sources - Hampshire Trust Bank Plc's own Consolidated and Bank Statement of Financial Position "
    "(Bank column), each year's own originally-published report:\n"
    f"FY2025: Group Annual Report and Accounts 2025 (Companies House, filed 13 May 2026), p.59 - {AR2025_URL}\n"
    f"FY2024: Annual Report and Accounts for the year ended 31 December 2024 (Companies House, filed 13 May 2025), p.69 - {AR2024_URL}\n"
    f"FY2023: Annual Report and Accounts for the year ended 31 December 2023 (Companies House, filed 04 Jun 2024) - {AR2023_URL}\n"
    f"FY2022: Annual Report and Accounts for the year ended 31 December 2022 (Companies House, filed 07 Aug 2023), p.56 - {AR2022_URL}\n"
    f"FY2021: Annual Report and Accounts for the year ended 31 December 2021 (Companies House, filed 14 Jun 2022), p.51, Statement of Financial Position - {AR2021_URL}\n"
    f"FY2020: Annual Report and Accounts 2020 (HTB website copy, text-native), p.52 - {AR2020_WEBSITE_URL}\n"
    f"FY2019: Annual Report and Accounts for the year ended 31 December 2019 (Companies House, filed 02 Jul 2020, scanned/image-only), p.44 - {AR2019_CH_URL}\n"
    f"FY2018: Annual Report and Accounts for the year ended 31 December 2018 (Companies House, filed 24 Jun 2019, scanned/image-only), p.37 - {AR2018_CH_URL}\n"
    f"FY2017: Annual Report and Accounts 2017 (HTB website copy, text-native), p.36 - {AR2017_WEBSITE_URL}\n"
    f"FY2016: Annual Report and Accounts 2016 (HTB website copy, text-native), p.28 - {AR2016_WEBSITE_URL}\n"
    + STATEMENTS_ENTITY_NOTE +
    "\n'Investment securities' is relabelled 'Investment securities, held at amortised cost' per Note 26 "
    "'Investment securities held at amortised cost' (Group Annual Report and Accounts 2025, p.109 - "
    f"{AR2025_WEBSITE_URL}), which shows the entire book (FY2025 and FY2024 columns: £693,673k / £219,980k) "
    "as a single 'Debt securities - Floating rate' line, all Aaa-rated, with no FVOCI/FVTPL or "
    "government/other split disclosed - covered bonds and RMBS measured at amortised cost per the report's "
    "own accounting policy note 7.9. FY2020-FY2023 figures are transcribed from scanned/image-only "
    "Companies House filings that could not be text-searched to reconfirm this same-basis wording, but the "
    "bank's investment book composition (covered bonds/RMBS) and accounting policy are unchanged across "
    "those years per the annual reports' own disclosures."
)

bs_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Loans and advances to banks", {
        "FY2025": 679085, "FY2024": 1435307, "FY2023": 476806, "FY2022": 458974, "FY2021": 242323,
        "FY2020": 156707, "FY2019": 84644, "FY2018": 98182, "FY2017": 101619, "FY2016": 136317,
    }),
    ("DATA", "Derivative assets held for risk management", {
        "FY2025": 13326, "FY2024": 51588, "FY2023": 75076, "FY2022": 113319, "FY2021": 19458,
        "FY2020": 1763, "FY2019": 1457, "FY2018": 1708, "FY2017": 903, "FY2016": 622,
    }),
    ("DATA", "Investment securities, held at amortised cost", {
        "FY2025": 693673, "FY2024": 219980, "FY2023": 234509, "FY2022": 217722, "FY2021": 196712,
        "FY2020": 20072, "FY2018": 15098,
    }),
    ("DATA", "Loans and advances to customers - FVTPL", {
        "FY2025": 0, "FY2024": 260, "FY2023": 3305, "FY2022": 4294, "FY2021": 10025,
        "FY2020": 50434, "FY2019": 126530, "FY2018": 166804,
    }),
    ("DATA", "Loans and advances to customers - at amortised cost", {
        "FY2025": 4540376, "FY2024": 3391908, "FY2023": 2967326, "FY2022": 2243123, "FY2021": 1704683,
        "FY2020": 1277092, "FY2019": 1053365, "FY2018": 733192, "FY2017": 632275, "FY2016": 463525,
    }),
    ("DATA", "Investment in subsidiaries", {
        "FY2025": 11703, "FY2024": 38203, "FY2023": 49422, "FY2022": 49422,
    }),
    ("DATA", "Property, plant and equipment", {
        "FY2025": 2969, "FY2024": 3961, "FY2023": 4969, "FY2022": 1443, "FY2021": 1471,
        "FY2020": 1805, "FY2019": 2077, "FY2018": 2309, "FY2017": 2013, "FY2016": 1107,
    }),
    ("DATA", "Right-of-use assets", {
        "FY2025": 1940, "FY2024": 2711, "FY2023": 3602, "FY2022": 685, "FY2021": 1608,
        "FY2020": 2535, "FY2019": 3463,
    }),
    ("DATA", "Intangible assets", {
        "FY2025": 13949, "FY2024": 14712, "FY2023": 11732, "FY2022": 9464, "FY2021": 7606,
        "FY2020": 6701, "FY2019": 5976, "FY2018": 4058, "FY2017": 3097, "FY2016": 1845,
    }),
    ("DATA", "Corporation tax asset", {
        "FY2025": 4416,
    }),
    ("DATA", "Deferred tax asset", {
        "FY2025": 468, "FY2024": 978, "FY2023": 1414, "FY2022": 2538, "FY2021": 1925,
        "FY2020": 1057, "FY2019": 246, "FY2017": 495, "FY2016": 907,
    }),
    ("DATA", "Other assets", {
        "FY2025": 164494, "FY2024": 227921, "FY2023": 235646, "FY2022": 99498, "FY2021": 4720,
        "FY2020": 4196, "FY2019": 6146, "FY2018": 2822, "FY2017": 1858, "FY2016": 2337,
    }),
    ("TOTAL", "Total assets", {
        "FY2025": 6126399, "FY2024": 5387529, "FY2023": 4063807, "FY2022": 3200482, "FY2021": 2190531,
        "FY2020": 1522362, "FY2019": 1283904, "FY2018": 1024173, "FY2017": 742260, "FY2016": 606660,
    }),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Derivative liabilities held for risk management", {
        "FY2025": 18715, "FY2024": 22569, "FY2023": 25456, "FY2022": 19136, "FY2021": 4413,
        "FY2020": 14562, "FY2019": 4599, "FY2018": 836, "FY2017": 292, "FY2016": 526,
    }),
    ("DATA", "Customer deposits", {
        "FY2025": 5232516, "FY2024": 4526003, "FY2023": 3205681, "FY2022": 2420694, "FY2021": 1633046,
        "FY2020": 1125560, "FY2019": 904171, "FY2018": 720718, "FY2017": 596296, "FY2016": 523315,
    }),
    ("DATA", "Lease liabilities", {
        "FY2025": 2900, "FY2024": 3409, "FY2023": 3974, "FY2022": 647, "FY2021": 1895,
        "FY2020": 3086, "FY2019": 4525,
    }),
    ("DATA", "Central bank facilities", {
        "FY2025": 290000, "FY2024": 295000, "FY2023": 300000, "FY2022": 295000, "FY2021": 295000,
        "FY2020": 180000, "FY2019": 173000, "FY2018": 135000, "FY2017": 20000,
    }),
    ("DATA", "Subordinated liabilities", {
        "FY2025": 81669, "FY2024": 56085, "FY2023": 57768, "FY2022": 30336, "FY2021": 30202,
        "FY2020": 30125, "FY2019": 30048, "FY2018": 29970,
    }),
    ("DATA", "Provisions", {
        "FY2025": 2150,
        "FY2018": 0, "FY2017": 303, "FY2016": 36,
    }),
    ("DATA", "Other liabilities", {
        "FY2025": 64082, "FY2024": 109904, "FY2023": 148127, "FY2022": 175805, "FY2021": 37139,
        "FY2020": 14971, "FY2019": 16086, "FY2018": 11899, "FY2017": 9729, "FY2016": 8711,
    }),
    ("TOTAL", "Total liabilities", {
        "FY2025": 5692032, "FY2024": 5012970, "FY2023": 3741006, "FY2022": 2941618, "FY2021": 2001695,
        "FY2020": 1368304, "FY2019": 1132429, "FY2018": 898423, "FY2017": 626620, "FY2016": 532588,
    }),
    ("SECTION", "Equity", {}),
    ("DATA", "Share capital", {
        "FY2025": 139828, "FY2024": 139828, "FY2023": 139828, "FY2022": 139828, "FY2021": 139828,
        "FY2020": 126288, "FY2019": 126288, "FY2018": 111288, "FY2017": 111288, "FY2016": 78288,
    }),
    ("DATA", "Share premium", {
        "FY2025": 196, "FY2024": 196, "FY2023": 196, "FY2022": 196, "FY2021": 196,
        "FY2020": 196, "FY2019": 196, "FY2018": 196, "FY2017": 196, "FY2016": 196,
    }),
    ("DATA", "Cash flow hedge reserve", {
        "FY2025": -2182, "FY2024": -2674, "FY2023": -3099, "FY2022": 129,
    }),
    ("DATA", "Fair value through OCI reserve", {
        "FY2020": 0, "FY2019": 0, "FY2018": -50,
    }),
    ("DATA", "Retained earnings", {
        "FY2025": 279495, "FY2024": 220179, "FY2023": 168846, "FY2022": 101681, "FY2021": 48812,
        "FY2020": 27574, "FY2019": 24991, "FY2018": 14316, "FY2017": 4156, "FY2016": -4412,
    }),
    ("TOTAL", "Total equity, excluding non-controlling interest", {
        "FY2025": 417337, "FY2024": 357529, "FY2023": 305771, "FY2022": 241834, "FY2021": 188836,
        "FY2020": 154058, "FY2019": 151475, "FY2018": 125750, "FY2017": 115640, "FY2016": 74072,
    }),
    ("DATA", "Other equity instruments (non-controlling interests)", {
        "FY2025": 17030, "FY2024": 17030, "FY2023": 17030, "FY2022": 17030,
    }),
    ("TOTAL", "Total equity", {
        "FY2025": 434367, "FY2024": 374559, "FY2023": 322801, "FY2022": 258864, "FY2021": 188836,
        "FY2020": 154058, "FY2019": 151475, "FY2018": 125750, "FY2017": 115640, "FY2016": 74072,
    }),
    ("TOTAL", "Total liabilities and equity", {
        "FY2025": 6126399, "FY2024": 5387529, "FY2023": 4063807, "FY2022": 3200482, "FY2021": 2190531,
        "FY2020": 1522362, "FY2019": 1283904, "FY2018": 1024173, "FY2017": 742260, "FY2016": 606660,
    }),
]

bw.add_balance_sheet_sheet(
    title="Hampshire Trust Bank Plc — Bank Statement of Financial Position",
    subtitle="Bank (parent-entity) column; FY2021 and earlier predate Group consolidation - see source note",
    rows=bs_rows,
    sources_text=BS_SOURCES,
    first_col_width=74,
    source_height=190,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Sheet: Profit & Loss (Bank / entity-level column)
# ---------------------------------------------------------------
PL_SOURCES = (
    "Sources - Hampshire Trust Bank Plc's own Consolidated and Bank Statement of Comprehensive Income "
    "(Bank column), each year's own originally-published report:\n"
    f"FY2025: Group Annual Report and Accounts 2025 (Companies House, filed 13 May 2026), p.58 - {AR2025_URL}\n"
    f"FY2024: Annual Report and Accounts for the year ended 31 December 2024 (Companies House, filed 13 May 2025), p.68 - {AR2024_URL}\n"
    f"FY2023: Annual Report and Accounts for the year ended 31 December 2023 (Companies House, filed 04 Jun 2024), p.59 - {AR2023_URL}\n"
    f"FY2022: Annual Report and Accounts for the year ended 31 December 2022 (Companies House, filed 07 Aug 2023), p.55 - {AR2022_URL}\n"
    f"FY2021: Annual Report and Accounts for the year ended 31 December 2021 (Companies House, filed 14 Jun 2022), p.50, Statement of Comprehensive Income - {AR2021_URL}\n"
    f"FY2020: Annual Report and Accounts 2020 (HTB website copy, text-native), p.51 - {AR2020_WEBSITE_URL}\n"
    f"FY2019: Annual Report and Accounts for the year ended 31 December 2019 (Companies House, filed 02 Jul 2020, scanned/image-only), p.43 - {AR2019_CH_URL}\n"
    f"FY2018: Annual Report and Accounts for the year ended 31 December 2018 (Companies House, filed 24 Jun 2019, scanned/image-only), p.36 - {AR2018_CH_URL}\n"
    f"FY2017: Annual Report and Accounts 2017 (HTB website copy, text-native), p.35 - {AR2017_WEBSITE_URL}\n"
    f"FY2016: Annual Report and Accounts 2016 (HTB website copy, text-native), p.27 - {AR2016_WEBSITE_URL}\n"
    + STATEMENTS_ENTITY_NOTE +
    "\nFY2016-FY2017 predate IFRS 9 entirely (adopted 1 Jan 2018, not restated in comparatives) and use a "
    "different P&L shape: 'Net income from derivatives at fair value through profit or loss' instead of "
    "the later 'Net (loss)/gain on loans and other financial assets at FVTPL' line. FY2016's 2015 "
    "comparative in its own report was itself restated for discontinued activities, per that report's own "
    "footnote - not relevant to the FY2016 column transcribed here.\n"
    "Net (loss)/gain arising from derecognition of financial assets at amortised cost and Impairment "
    "loss on investments in subsidiaries are only disclosed as separate lines from FY2024 onward - not "
    "applicable/nil in earlier years' own disclosures, left blank rather than assumed zero.\n"
    "FY2016's own report also carries a small separate 'Other expenses' line (£(11)k) with no equivalent "
    "row in this workbook's standard shape - folded into Administrative expenses (£(15,491)k + £(11)k = "
    "£(15,502)k transcribed here) so Profit before tax and dividends still ties exactly to the disclosed "
    "£4,406k operating profit before tax. FY2016/FY2017 also each carried a small Discontinued activities "
    "result (asset-backed lending run-off) as a distinct post-tax line in the original statement (FY2016: "
    "£(1,288)k loss, FY2017: £189k profit) - added here as its own new row between Tax expense and Profit "
    "after tax, since this workbook's standard shape has no discontinued-activities row; both years' Net "
    "interest income/Operating income/Profit before tax figures above are the continuing-activities-only "
    "amounts exactly as originally disclosed, with Discontinued activities kept in its own separate row "
    "rather than blended into any continuing-activities line."
)

pl_rows = [
    ("DATA", "Interest and similar income", {
        "FY2025": 396890, "FY2024": 352194, "FY2023": 245613, "FY2022": 131839, "FY2021": 88508,
        "FY2020": 76392, "FY2019": 64933, "FY2018": 50296, "FY2017": 43479, "FY2016": 26695,
    }),
    ("DATA", "Interest expense and similar charges", {
        "FY2025": -229271, "FY2024": -206852, "FY2023": -114551, "FY2022": -33255, "FY2021": -19351,
        "FY2020": -22020, "FY2019": -18694, "FY2018": -13322, "FY2017": -9366, "FY2016": -6070,
    }),
    ("TOTAL", "Net interest income", {
        "FY2025": 167619, "FY2024": 145342, "FY2023": 131062, "FY2022": 98584, "FY2021": 69157,
        "FY2020": 54372, "FY2019": 46239, "FY2018": 36974, "FY2017": 34113, "FY2016": 20625,
    }),
    ("SECTION", "Other operating income", {}),
    ("DATA", "Fees and commissions income", {
        "FY2025": 3006, "FY2024": 3172, "FY2023": 1459, "FY2022": 2078, "FY2021": 1533,
        "FY2020": 1548, "FY2019": 1500, "FY2018": 2554, "FY2017": 373, "FY2016": 413,
    }),
    ("DATA", "Fees and commissions payable", {
        "FY2025": -1110, "FY2024": -1406, "FY2023": -1375, "FY2022": -1637, "FY2021": -805,
        "FY2020": -784, "FY2019": -295, "FY2018": -166, "FY2017": -156, "FY2016": -134,
    }),
    ("DATA", "Net (loss)/gain on loans and other financial assets at fair value through profit or loss", {
        "FY2025": -1010, "FY2024": -315, "FY2023": -2495, "FY2022": 3276, "FY2021": 3175,
        "FY2020": -5369, "FY2019": -1943, "FY2018": -1764, "FY2017": 157, "FY2016": 5,
    }),
    ("DATA", "Net (loss)/gain arising from derecognition of financial assets at amortised cost", {
        "FY2025": -769, "FY2024": 7275,
    }),
    ("DATA", "Other income", {
        "FY2025": 2887, "FY2024": 3927, "FY2023": 5991, "FY2022": 6512, "FY2021": 9,
        "FY2020": 3, "FY2019": 6, "FY2018": -8, "FY2017": 5, "FY2016": 0,
    }),
    ("TOTAL", "Operating income", {
        "FY2025": 170623, "FY2024": 157995, "FY2023": 134642, "FY2022": 108813, "FY2021": 73069,
        "FY2020": 49770, "FY2019": 45507, "FY2018": 37590, "FY2017": 34492, "FY2016": 20909,
    }),
    ("TOTAL", "Administrative expenses", {
        "FY2025": -83039, "FY2024": -75545, "FY2023": -69237, "FY2022": -56984, "FY2021": -46313,
        "FY2020": -32236, "FY2019": -28587, "FY2018": -24700, "FY2017": -20110, "FY2016": -15502,
    }),
    ("DATA", "Impairment loss on investments in subsidiaries", {
        "FY2025": -26500, "FY2024": -11219,
    }),
    ("DATA", "Impairment gains/(losses) on loans and advances to customers", {
        "FY2025": -9063, "FY2024": -9770, "FY2023": -12498, "FY2022": -7308, "FY2021": 590,
        "FY2020": -14671, "FY2019": -3375, "FY2018": -1742, "FY2017": -4514, "FY2016": -1001,
    }),
    ("TOTAL", "Profit before tax and dividends", {
        "FY2025": 52021, "FY2024": 61461, "FY2023": 52907, "FY2022": 44521, "FY2021": 27346,
        "FY2020": 2863, "FY2019": 13545, "FY2018": 11148, "FY2017": 9868, "FY2016": 4406,
    }),
    ("DATA", "Interim dividends received", {
        "FY2025": 26500, "FY2024": 11000, "FY2023": 27500, "FY2022": 20000,
    }),
    ("TOTAL", "Profit before tax", {
        "FY2025": 78521, "FY2024": 72461, "FY2023": 80407, "FY2022": 64521, "FY2021": 27346,
        "FY2020": 2863, "FY2019": 13545, "FY2018": 11148, "FY2017": 9868, "FY2016": 4406,
    }),
    ("DATA", "Tax expense", {
        "FY2025": -18405, "FY2024": -19407, "FY2023": -13134, "FY2022": -10488, "FY2021": -6784,
        "FY2020": -309, "FY2019": -2746, "FY2018": -2118, "FY2017": -2038, "FY2016": -963,
    }),
    ("DATA", "Profit/(loss) from discontinued activities", {
        "FY2017": 189, "FY2016": -1288,
    }),
    ("TOTAL", "Profit after tax for the year", {
        "FY2025": 60116, "FY2024": 53054, "FY2023": 67273, "FY2022": 54033, "FY2021": 20562,
        "FY2020": 2554, "FY2019": 10799, "FY2018": 9030, "FY2017": 8019, "FY2016": 2155,
    }),
    ("SECTION", "Other comprehensive income", {}),
    ("DATA", "Cash flow hedges - effective portion of changes in fair value", {
        "FY2025": -184, "FY2024": -724, "FY2023": -3394, "FY2022": 125,
    }),
    ("DATA", "Cash flow hedges - recycled to profit or loss", {
        "FY2025": 676, "FY2024": 1149, "FY2023": 166, "FY2022": 4,
    }),
    ("DATA", "Net change in fair value of investment securities (AFS/FVOCI)", {
        "FY2020": 0, "FY2019": 50, "FY2018": -50, "FY2016": 0,
    }),
    ("TOTAL", "Total comprehensive income for the year, net of tax", {
        "FY2025": 60608, "FY2024": 53479, "FY2023": 64045, "FY2022": 54162, "FY2021": 20562,
        "FY2020": 2554, "FY2019": 10849, "FY2018": 8980, "FY2017": 8019, "FY2016": 2155,
    }),
]

bw.add_income_statement_sheet(
    title="Hampshire Trust Bank Plc — Bank Statement of Comprehensive Income",
    subtitle="Bank (parent-entity) column; FY2021 and earlier predate Group consolidation and cash flow hedge accounting - see source note",
    rows=pl_rows,
    sources_text=PL_SOURCES,
    first_col_width=88,
    source_height=190,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Sheet: Statement of Changes in Equity (Bank / entity-level column)
# ---------------------------------------------------------------
EQ_SOURCES = (
    "Sources - Hampshire Trust Bank Plc's own Bank Statement of Changes in Equity, each year's own "
    "originally-published report (page as cited on the Balance Sheet/P&L sheets' source notes for that "
    "year - the equity statement sits on the immediately adjacent page in every filing):\n"
    f"FY2025: {AR2025_URL} (p.62)\nFY2024: {AR2024_URL} (p.72)\nFY2023: {AR2023_URL} (p.60ish, Bank statement)\n"
    f"FY2022: {AR2022_URL} (p.59)\nFY2021: {AR2021_URL} (p.52, single Company statement)\n"
    f"FY2020: {AR2020_WEBSITE_URL} (p.53-54, includes FY2019 comparative chain)\n"
    f"FY2019: {AR2019_CH_URL} (p.45, scanned/image-only)\n"
    f"FY2018: {AR2018_CH_URL} (p.38, scanned/image-only)\n"
    f"FY2017: {AR2017_WEBSITE_URL} (p.37)\nFY2016: {AR2016_WEBSITE_URL} (p.29)\n"
    + STATEMENTS_ENTITY_NOTE +
    "\nBuilt using the per-year reconciliation ladder: every year's closing balance ties exactly to both "
    "the next year's own opening balance and that year's own Balance Sheet Total equity - zero plug rows "
    "needed anywhere in this roll-forward. The 'Balance at 31 December 2020 / 1 January 2021' row merges "
    "what were two identical duplicate rows in the original per-year sourcing (that year's closing balance "
    "and the next year's opening balance) into one, as this workbook has done at every other year boundary "
    "in this roll-forward.\n"
    "This workbook's Statement of Changes in Equity has no dedicated 'Fair value through OCI reserve' "
    "column (only the Balance Sheet does, since that reserve exists only in FY2018-FY2020 and is tiny - at "
    "most £50k). Its movements are folded into the 'Retained earnings' column here instead (labelled "
    "'Profit for the year / other comprehensive income (incl. FVOCI reserve movement, see note)' on the "
    "FY2018 and FY2019 movement rows) so this sheet's FY2018/FY2019 'Retained earnings' column reads "
    "£14,266k/£24,991k rather than the Balance Sheet's own separately-stated £14,316k/£24,991k retained "
    "earnings line (FY2018 differs by exactly £50k, the folded-in FVOCI reserve; FY2019's FVOCI reserve "
    "is £0 that year so the two figures happen to coincide) - both are correct on their own sheet's own "
    "convention, not a reconciliation break. FY2018's IFRS 9 transition adjustment (£(506)k ECL day-1 "
    "adjustment plus £1,301k FVTPL reclassification, both net of tax, both hitting retained earnings) is "
    "combined into one 'Adjustment on initial application of IFRS 9' row for the same reason - the "
    "combined £795k figure is exact, not a rounding of the two components."
)

EQ_HEADERS = [
    "Share capital", "Share premium", "Cash flow hedge reserve", "Retained earnings",
    "Attributable to ordinary shareholders", "Other equity reserves (NCI)", "Total equity",
]

eq_rows = [
    ("DATA", "Balance at 1 January 2016", (58288, 196, None, -6908, 51576, None, 51576)),
    ("DATA", "Profit for the year", (None, None, None, 2155, 2155, None, 2155)),
    ("DATA", "Equity settled share-based payment", (None, None, None, 341, 341, None, 341)),
    ("DATA", "Issue of share capital", (20000, None, None, None, 20000, None, 20000)),
    ("TOTAL", "Balance at 31 December 2016", (78288, 196, None, -4412, 74072, None, 74072)),

    ("DATA", "Balance at 1 January 2017", (78288, 196, None, -4412, 74072, None, 74072)),
    ("DATA", "Profit for the year", (None, None, None, 8019, 8019, None, 8019)),
    ("DATA", "Equity settled share-based payment", (None, None, None, 549, 549, None, 549)),
    ("DATA", "Issue of share capital", (33000, None, None, None, 33000, None, 33000)),
    ("TOTAL", "Balance at 31 December 2017", (111288, 196, None, 4156, 115640, None, 115640)),

    ("DATA", "Balance at 1 January 2018", (111288, 196, None, 4156, 115640, None, 115640)),
    ("DATA", "Adjustment on initial application of IFRS 9 (ECL + FVTPL reclassification, net of tax)", (None, None, None, 795, 795, None, 795)),
    ("TOTAL", "Restated balance at 1 January 2018", (111288, 196, None, 4951, 116435, None, 116435)),
    ("DATA", "Profit for the year / other comprehensive income (incl. FVOCI reserve movement, see note)", (None, None, None, 8980, 8980, None, 8980)),
    ("DATA", "Equity settled share-based payment", (None, None, None, 335, 335, None, 335)),
    ("TOTAL", "Balance at 31 December 2018", (111288, 196, None, 14266, 125750, None, 125750)),

    ("DATA", "Balance at 1 January 2019", (111288, 196, None, 14266, 125750, None, 125750)),
    ("DATA", "Adjustment on initial application of IFRS 16", (None, None, None, -108, -108, None, -108)),
    ("TOTAL", "Restated balance at 1 January 2019", (111288, 196, None, 14158, 125642, None, 125642)),
    ("DATA", "Profit for the year / other comprehensive income (incl. FVOCI reserve movement, see note)", (None, None, None, 10849, 10849, None, 10849)),
    ("DATA", "Equity settled share-based payment", (None, None, None, -16, -16, None, -16)),
    ("DATA", "Issue of share capital", (15000, None, None, None, 15000, None, 15000)),
    ("TOTAL", "Balance at 31 December 2019", (126288, 196, None, 24991, 151475, None, 151475)),

    ("DATA", "Balance at 1 January 2020", (126288, 196, None, 24991, 151475, None, 151475)),
    ("DATA", "Profit for the year", (None, None, None, 2554, 2554, None, 2554)),
    ("DATA", "Equity settled share-based payment", (None, None, None, 29, 29, None, 29)),
    ("TOTAL", "Balance at 31 December 2020 / 1 January 2021", (126288, 196, None, 27574, 154058, None, 154058)),

    ("DATA", "Profit for the year", (None, None, None, 20562, 20562, None, 20562)),
    ("DATA", "Equity settled share-based payment", (None, None, None, 676, 676, None, 676)),
    ("DATA", "Issue of share capital", (13540, None, None, None, 13540, None, 13540)),
    ("TOTAL", "Balance at 31 December 2021", (139828, 196, None, 48812, 188836, None, 188836)),

    ("DATA", "Balance at 1 January 2022", (139828, 196, None, 48812, 188836, None, 188836)),
    ("DATA", "Profit for the year", (None, None, None, 54033, 54033, None, 54033)),
    ("DATA", "Cash flow hedges - effective portion of changes in fair value", (None, None, 125, None, 125, None, 125)),
    ("DATA", "Cash-flow hedges - recycled to profit or loss", (None, None, 4, None, 4, None, 4)),
    ("DATA", "Equity settled share-based payment", (None, None, None, 240, 240, None, 240)),
    ("DATA", "Issue of other equity instruments", (None, None, None, None, None, 17030, 17030)),
    ("DATA", "Coupon paid on other equity instruments", (None, None, None, -1404, -1404, None, -1404)),
    ("TOTAL", "Balance at 31 December 2022", (139828, 196, 129, 101681, 241834, 17030, 258864)),

    ("DATA", "Balance at 1 January 2023", (139828, 196, 129, 101681, 241834, 17030, 258864)),
    ("DATA", "Profit for the year", (None, None, None, 67273, 67273, None, 67273)),
    ("DATA", "Cash flow hedges - effective portion of changes in fair value", (None, None, -3394, None, -3394, None, -3394)),
    ("DATA", "Cash-flow hedges - recycled to profit or loss", (None, None, 166, None, 166, None, 166)),
    ("DATA", "Equity settled share-based payment", (None, None, None, 1399, 1399, None, 1399)),
    ("DATA", "Coupon paid on other equity instruments", (None, None, None, -1507, -1507, None, -1507)),
    ("TOTAL", "Balance at 31 December 2023", (139828, 196, -3099, 168846, 305771, 17030, 322801)),

    ("DATA", "Balance at 1 January 2024", (139828, 196, -3099, 168846, 305771, 17030, 322801)),
    ("DATA", "Profit for the year", (None, None, None, 53054, 53054, None, 53054)),
    ("DATA", "Cash flow hedges - effective portion of changes in fair value", (None, None, -724, None, -724, None, -724)),
    ("DATA", "Cash-flow hedges - recycled to profit or loss", (None, None, 1149, None, 1149, None, 1149)),
    ("DATA", "Equity settled share-based payment", (None, None, None, -204, -204, None, -204)),
    ("DATA", "Coupon paid on other equity instruments", (None, None, None, -1517, -1517, None, -1517)),
    ("TOTAL", "Balance at 31 December 2024", (139828, 196, -2674, 220179, 357529, 17030, 374559)),

    ("DATA", "Balance at 1 January 2025", (139828, 196, -2674, 220179, 357529, 17030, 374559)),
    ("DATA", "Profit for the year", (None, None, None, 60116, 60116, None, 60116)),
    ("DATA", "Cash flow hedges - effective portion of changes in fair value", (None, None, -184, None, -184, None, -184)),
    ("DATA", "Cash-flow hedges - recycled to profit or loss", (None, None, 676, None, 676, None, 676)),
    ("DATA", "Equity settled share-based payment", (None, None, None, 718, 718, None, 718)),
    ("DATA", "Coupon paid on other equity instruments", (None, None, None, -1518, -1518, None, -1518)),
    ("TOTAL", "Balance at 31 December 2025", (139828, 196, -2182, 279495, 417337, 17030, 434367)),
]

bw.add_equity_changes_sheet(
    title="Hampshire Trust Bank Plc — Bank Statement of Changes in Equity",
    subtitle="Bank (parent-entity) column, chronological; FY2021 and earlier predate Group consolidation - see source note",
    headers=EQ_HEADERS,
    rows=eq_rows,
    sources_text=EQ_SOURCES,
    source_height=210,
)

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement (Bank / entity-level column)
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Profit before tax for the year", {
        "FY2025": 78521, "FY2024": 72461, "FY2023": 80407, "FY2022": 64521, "FY2021": 27346,
        "FY2020": 2863, "FY2019": 13545, "FY2018": 11148, "FY2017": 10104, "FY2016": 2795,
    }),
    ("DATA", "Depreciation and amortisation", {
        "FY2025": 6963, "FY2024": 5800, "FY2023": 4936, "FY2022": 4411, "FY2021": 3936,
        "FY2020": 3524, "FY2019": 2885, "FY2018": 1409, "FY2017": 991, "FY2016": 676,
    }),
    ("DATA", "Loss on disposal of fixed assets", {
        "FY2023": 503,
    }),
    ("DATA", "Impairment loss on investment in subsidiaries", {
        "FY2025": 26500, "FY2024": 11219,
    }),
    ("DATA", "Foreign exchange gains/(losses)", {
        "FY2025": -29, "FY2022": -2, "FY2021": 9,
        "FY2020": 3, "FY2019": 6, "FY2018": -8, "FY2017": 5, "FY2016": -34,
    }),
    ("DATA", "Gain on securitisation", {
        "FY2024": -10414,
    }),
    ("DATA", "Increase in impairment of loans and advances", {
        "FY2025": 10147, "FY2024": 8939, "FY2023": 7183, "FY2022": 11995, "FY2021": 6362,
        "FY2020": 3753, "FY2019": 776, "FY2018": -1582, "FY2017": 4078, "FY2016": 2607,
    }),
    ("DATA", "Increase/(decrease) in provisions", {
        "FY2025": 1831, "FY2024": 1364, "FY2023": 6036, "FY2022": 3215, "FY2021": -4206,
        "FY2020": 10918, "FY2019": 2599, "FY2018": -303, "FY2017": 267, "FY2016": -9,
    }),
    ("DATA", "Equity-settled share-based payment transactions", {
        "FY2025": 718, "FY2024": -204, "FY2023": 1399, "FY2022": 240, "FY2021": 676,
        "FY2020": 30, "FY2019": -16, "FY2018": 335, "FY2017": 549, "FY2016": 341,
    }),
    ("DATA", "Bond premium/discount amortisation", {
        "FY2025": 157, "FY2024": -1943, "FY2023": -4943, "FY2022": -335, "FY2021": 1275,
        "FY2020": -67,
    }),
    ("DATA", "Decrease/(increase) in fair value of derivative assets", {
        "FY2025": 30481, "FY2024": 18609, "FY2023": 41007, "FY2022": -76695, "FY2021": -28408,
        "FY2020": 10120, "FY2019": 3574, "FY2018": 82, "FY2017": -157, "FY2016": -5,
    }),
    ("DATA", "Increase/(decrease) in fair value of loans and advances designated as hedged items", {
        "FY2025": -32163, "FY2024": -19784, "FY2023": -39698, "FY2022": 73530, "FY2021": 25595,
        "FY2020": -9116, "FY2019": -3243,
    }),
    ("DATA", "Decrease/(increase) in fair value of loans and advances held at FVTPL", {
        "FY2025": 188, "FY2024": -53, "FY2023": 1436, "FY2022": -6981, "FY2021": -749,
        "FY2020": 6463, "FY2019": 4088, "FY2018": 1682,
    }),
    ("DATA", "(Increase)/decrease in fair value of GILTs", {
        "FY2019": 61,
    }),
    ("DATA", "Repayment of the interest accrued on lease liabilities", {
        "FY2025": 228, "FY2024": 258, "FY2023": 142, "FY2022": 70, "FY2021": -129,
        "FY2020": -187, "FY2019": -240,
    }),
    ("DATA", "Dividends received", {
        "FY2025": -26500, "FY2024": -11000, "FY2023": -27500, "FY2022": -20000,
    }),
    ("DATA", "Other acquisition costs recognised through equity", {
        "FY2022": -392,
    }),
    ("DATA", "Corporation tax paid", {
        "FY2025": -21655, "FY2024": -18086, "FY2023": -15835, "FY2022": -14257, "FY2021": -3709,
        "FY2020": -2091, "FY2019": -2230, "FY2018": -2077, "FY2017": -1070,
    }),
    ("DATA", "Corporation tax received", {
        "FY2025": 1166,
    }),
    ("DATA", "(Increase) in loans and advances to customers", {
        "FY2025": -1121847, "FY2024": -717726, "FY2023": -675670, "FY2022": -625569, "FY2021": -419379,
        "FY2020": -158211, "FY2019": -278881, "FY2018": -266849, "FY2017": -173034, "FY2016": -288487,
    }),
    ("DATA", "(Increase)/decrease in other assets", {
        "FY2025": 61605, "FY2024": 6841, "FY2023": -169564, "FY2022": -94775, "FY2021": -508,
        "FY2020": 1950, "FY2019": -3324, "FY2018": -964, "FY2017": 41, "FY2016": -1098,
    }),
    ("DATA", "(Decrease)/increase in central bank facilities", {
        "FY2025": -5000, "FY2024": -5000, "FY2023": 5000, "FY2021": 115000,
        "FY2020": 7000, "FY2019": 38000, "FY2018": 115000, "FY2017": 20000,
    }),
    ("DATA", "(Increase)/decrease in collateral held with banks", {
        "FY2025": -30078, "FY2024": -25256, "FY2023": -33646, "FY2022": 73421, "FY2021": 27594,
        "FY2018": -11, "FY2017": -2750,
    }),
    ("DATA", "(Increase)/decrease in debt securities (operating)", {
        "FY2019": 15098, "FY2018": -15098,
    }),
    ("DATA", "Increase in customer deposits", {
        "FY2025": 702733, "FY2024": 1324101, "FY2023": 765355, "FY2022": 798748, "FY2021": 512682,
        "FY2020": 219961, "FY2019": 183827, "FY2018": 124422, "FY2017": 72981, "FY2016": 336143,
    }),
    ("DATA", "Increase/(decrease) in subordinated and other liabilities", {
        "FY2025": -12373, "FY2024": -20701, "FY2023": 6564, "FY2022": 68205, "FY2021": 3637,
        "FY2020": -685, "FY2019": 3068, "FY2018": 2032, "FY2017": 695, "FY2016": 4613,
    }),
    ("TOTAL", "Net cash from/(used in) operating activities", {
        "FY2025": -328407, "FY2024": 619425, "FY2023": -46888, "FY2022": 259350, "FY2021": 267024,
        "FY2020": 96228, "FY2019": -20407, "FY2018": -30782, "FY2017": -67300, "FY2016": 57542,
    }),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Acquisition of subsidiary, net of cash acquired", {
        "FY2022": -32000,
    }),
    ("DATA", "Dividends received from subsidiary undertakings", {
        "FY2025": 26500, "FY2024": 11000, "FY2023": 27500, "FY2022": 20000,
    }),
    ("DATA", "Purchase of property, plant and equipment", {
        "FY2025": -300, "FY2024": -298, "FY2023": -4742, "FY2022": -543, "FY2021": -231,
        "FY2020": -278, "FY2019": -280, "FY2018": -790, "FY2017": -1329, "FY2016": -761,
    }),
    ("DATA", "Disposal of property, plant and equipment", {
        "FY2024": 51,
    }),
    ("DATA", "Purchase of intangible assets", {
        "FY2025": -4612, "FY2024": -6814, "FY2023": -5424, "FY2022": -4777, "FY2021": -3355,
        "FY2020": -2772, "FY2019": -3400, "FY2018": -1876, "FY2017": -1819, "FY2016": -1150,
    }),
    ("DATA", "Disposal of intangible assets", {
        "FY2025": 477, "FY2024": 67,
    }),
    ("DATA", "Purchase of right of use asset", {
        "FY2023": -3982,
    }),
    ("DATA", "Disposal of right of use asset", {
        "FY2024": -113,
    }),
    ("DATA", "Purchase of investment securities", {
        "FY2025": -500773, "FY2024": -135668, "FY2023": -415054, "FY2022": -424657, "FY2021": -178144,
        "FY2020": -84984,
    }),
    ("DATA", "Settlement/sale of investment securities", {
        "FY2025": 28148, "FY2024": 162520, "FY2023": 439744, "FY2022": 402000,
        "FY2020": 65000,
    }),
    ("TOTAL", "Net cash from/(used in) investing activities", {
        "FY2025": -450560, "FY2024": 30745, "FY2023": 38042, "FY2022": -39977, "FY2021": -181730,
        "FY2020": -23034, "FY2019": -3680, "FY2018": -2666, "FY2017": -3148, "FY2016": -1911,
    }),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Repayments of the principal portion of finance lease liabilities", {
        "FY2025": -737, "FY2024": -710, "FY2023": -797, "FY2022": -1318, "FY2021": -1183,
        "FY2020": -1131, "FY2019": -1078,
    }),
    ("DATA", "Inception of finance lease liability", {
        "FY2023": 3982,
    }),
    ("DATA", "Coupon paid to other equity instrument holders", {
        "FY2025": -1518, "FY2024": -1517, "FY2023": -1507, "FY2022": -1404,
    }),
    ("DATA", "Proceeds from the issuance of subordinated debt", {
        "FY2025": 55000, "FY2023": 25000, "FY2018": 30000,
    }),
    ("DATA", "Repayment of subordinated debt", {
        "FY2025": -30000,
    }),
    ("DATA", "Proceeds from securitisation", {
        "FY2024": 310558,
    }),
    ("DATA", "Proceeds from the issue of share capital", {
        "FY2021": 13540,
        "FY2019": 15000, "FY2017": 33000, "FY2016": 20000,
    }),
    ("TOTAL", "Net cash from/(used in) financing activities", {
        "FY2025": 22745, "FY2024": 308331, "FY2023": 26678, "FY2022": -2722, "FY2021": 12357,
        "FY2020": -1131, "FY2019": 13922, "FY2018": 30000, "FY2017": 33000, "FY2016": 20000,
    }),
    ("TOTAL", "Net (decrease)/increase in cash and cash equivalents", {
        "FY2025": -756222, "FY2024": 958501, "FY2023": 17832, "FY2022": 216651, "FY2021": 97651,
        "FY2020": 72063, "FY2019": -10165, "FY2018": -3448, "FY2017": -37448, "FY2016": 75631,
    }),
    ("DATA", "Cash and cash equivalents at the beginning of the year", {
        "FY2025": 1435307, "FY2024": 476806, "FY2023": 458974, "FY2022": 242323, "FY2021": 144672,
        "FY2020": 84644, "FY2019": 94809, "FY2018": 98257, "FY2017": 135705, "FY2016": 60074,
    }),
    ("TOTAL", "Cash and cash equivalents at the end of the year", {
        "FY2025": 679085, "FY2024": 1435307, "FY2023": 476806, "FY2022": 458974, "FY2021": 242323,
        "FY2020": 156707, "FY2019": 84644, "FY2018": 94809, "FY2017": 98257, "FY2016": 135705,
    }),
]

bw.add_cash_flow_sheet(
    title="Hampshire Trust Bank Plc — Bank Statement of Cash Flows",
    subtitle="Bank (parent-entity) column; FY2021 and earlier predate Group consolidation and use the single "
              "Company statement — see source note",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=74,
    source_height=170,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Sheet: Asset Quality (Bank / entity-level column)
# ---------------------------------------------------------------
AQ_SOURCES = (
    "Sources - Hampshire Trust Bank Plc's own Note 30 'Allowance for credit impairment losses on "
    "financial assets at amortised cost', Bank Total Gross Carrying Value and Bank Total Loss allowance "
    "tables (summed across the Bank's disclosed product lines: Development Finance, Specialist "
    "Mortgages, Asset and Wholesale Finance):\n"
    f"FY2025: Group Annual Report and Accounts 2025 (Companies House, filed 13 May 2026), p.18-25 - {AR2025_URL}\n"
    f"FY2024: same document's FY2024 comparative columns, p.18-25 - {AR2025_URL}\n"
    f"FY2023: Annual Report and Accounts for the year ended 31 December 2024 (Companies House, filed 13 May 2025), FY2023 comparative columns, p.126-136 - {AR2024_URL}\n"
    f"FY2022: same document's FY2022 comparative columns (from the FY2023 GCV/loss allowance tables), p.126-136 - {AR2024_URL}\n"
    f"FY2021: Annual Report and Accounts for the year ended 31 December 2021 (Companies House, filed 14 Jun 2022), single Company basis (pre-Group; only Development Finance + Specialist Mortgages + Asset and Wholesale Finance product lines existed), p.93-97 - {AR2021_URL}\n"
    "Note's own product-level tables are labelled 'Bank' for Development Finance and Specialist "
    "Mortgages in every year checked (identical to the 'Group' tables for those two products - both "
    "are 100% Bank-originated) and separately labelled 'Bank' vs 'Group' for Asset and Wholesale "
    "Finance/Commercial and Retail Finance once the Group had subsidiary-originated lending (from "
    "FY2022) - the Bank Total used here sums only the Bank-basis product lines, consistent with the "
    "Bank basis used throughout this workbook. Commercial and Retail Finance has no Bank-basis line "
    "at all in any year (subsidiary-only origination) - correctly excluded from the Bank Total. FY2024's "
    "Bank Total loss allowance is disclosed as £21,715k in AR2024's own FY2024 closing balance but as "
    "£21,787k in AR2025's FY2024 opening comparative (a £72k gap, both companies' own filings, not "
    "reconciled here - reproduced as each document discloses it). Net carrying value (Gross carrying "
    "value less Loss allowance) does not tie exactly to the Balance Sheet's 'Loans and advances to "
    "customers - at amortised cost' line (e.g. FY2025: £4,528,886k here vs £4,540,376k on the Balance "
    "Sheet) - Note 30's 'financial assets at amortised cost' scope is evidently broader than customer "
    "loans alone (likely also captures loans to banks and/or investment securities held at amortised "
    "cost), not confirmed further from the disclosure alone - not force-reconciled.\n"
    "FY2018-FY2020 (IFRS 9 stage data, same Development Finance/Specialist Mortgages/Asset and Wholesale "
    "Finance product scope as later years): FY2020 from Annual Report and Accounts 2020 (HTB website copy), "
    f"p.92-93 - {AR2020_WEBSITE_URL}; FY2019 from the same document's FY2019 comparative columns, p.92-93; "
    f"FY2018 from Annual Report and Accounts for the year ended 31 December 2018 (Companies House, filed 24 "
    f"Jun 2019, scanned/image-only), p.59-61 - {AR2018_CH_URL} "
    "(this year's Total Exposure is split Stage 2 <=30 / >30 days past due in the source; the two sub-splits "
    "are summed into one Stage 2 figure here to match the later years' 3-stage shape; the source table's own "
    "'Total Gross Exposure' additionally includes Off Balance Sheet Loan Commitments, excluded here to match "
    "the on-balance-sheet-only scope used in every other year - the resulting FY2018 Net carrying value ties "
    "exactly to the Balance Sheet's £733,192k, unlike later years' looser tie). FY2019's Total loss allowance "
    "is disclosed as £4,470k in AR2019's own closing balance table but as £4,469k in AR2020's FY2019 opening "
    "comparative (a trivial £1k rounding gap, both companies' own filings, reproduced as each discloses it, "
    "same pattern as the FY2024 gap noted above). FY2020's Net carrying value (£1,262,933k) sits £14,159k "
    "below the Balance Sheet's £1,277,092k - the source's own 'Add FV gains from portfolio hedging' line "
    "(£14,160k, from fair-value hedge accounting on the loan book) closes almost exactly the whole gap, "
    "unlike the unexplained gap in FY2021 onward - not added into Net carrying value here to keep this row "
    "as a pure Gross-less-Loss-allowance calculation, consistent with every other year on this sheet.\n"
    "FY2016-FY2017 predate IFRS 9 entirely (adopted 1 Jan 2018) - no stage concept exists for these two "
    "years, so a separate 'Legacy IAS 39 basis' section below uses each year's own product-level gross "
    "carrying value/impairment allowance/net carrying value instead (Note 4.2 'Loans and advances to "
    "customers', both years use different product names than the post-2018 Development Finance/Specialist "
    "Mortgages/Asset and Wholesale Finance labels - FY2016/FY2017's own labels are used as-is rather than "
    "force-mapped onto the later taxonomy). Both years' Net carrying value ties exactly to the Balance "
    "Sheet (FY2016: £463,525k, FY2017: £632,275k). Source: FY2017 from Annual Report and Accounts 2017 (HTB "
    f"website copy, text-native), p.57-58 - {AR2017_WEBSITE_URL}; FY2016 from Annual Report and Accounts 2016 "
    f"(HTB website copy, text-native), p.41-42 - {AR2016_WEBSITE_URL}."
)

aq_rows = [
    ("SECTION", "Gross carrying value by IFRS 9 stage (Bank basis)", {}),
    ("DATA", "Stage 1 (12-month ECL)", {
        "FY2025": 3911362, "FY2024": 2958747, "FY2023": 2512679, "FY2022": 1896973, "FY2021": 1565803,
        "FY2020": 1113344, "FY2019": 1004778, "FY2018": 720676,
    }),
    ("DATA", "Stage 2 (lifetime ECL, not credit-impaired)", {
        "FY2025": 471501, "FY2024": 388068, "FY2023": 443933, "FY2022": 407977, "FY2021": 127790,
        "FY2020": 147415, "FY2019": 41077, "FY2018": 10860,
    }),
    ("DATA", "Stage 3 (credit-impaired)", {
        "FY2025": 167492, "FY2024": 91739, "FY2023": 70199, "FY2022": 53821, "FY2021": 38893,
        "FY2020": 17551, "FY2019": 8363, "FY2018": 3528,
    }),
    ("TOTAL", "Total gross carrying value", {
        "FY2025": 4550355, "FY2024": 3438552, "FY2023": 3026811, "FY2022": 2358771, "FY2021": 1732486,
        "FY2020": 1278310, "FY2019": 1054218, "FY2018": 735064,
    }),
    ("SECTION", "Loss allowance (ECL) by IFRS 9 stage (Bank basis)", {}),
    ("DATA", "Stage 1", {
        "FY2025": 4573, "FY2024": 4436, "FY2023": 5307, "FY2022": 3099, "FY2021": 1431,
        "FY2020": 2061, "FY2019": 1115, "FY2018": 891,
    }),
    ("DATA", "Stage 2", {
        "FY2025": 3429, "FY2024": 3998, "FY2023": 6038, "FY2022": 4752, "FY2021": 1475,
        "FY2020": 6924, "FY2019": 861, "FY2018": 433,
    }),
    ("DATA", "Stage 3", {
        "FY2025": 13467, "FY2024": 13281, "FY2023": 9078, "FY2022": 6535, "FY2021": 8265,
        "FY2020": 6392, "FY2019": 2494, "FY2018": 548,
    }),
    ("TOTAL", "Total loss allowance", {
        "FY2025": 21469, "FY2024": 21715, "FY2023": 20423, "FY2022": 14386, "FY2021": 11171,
        "FY2020": 15377, "FY2019": 4470, "FY2018": 1872,
    }),
    ("TOTAL", "Net carrying value (Gross carrying value less Loss allowance)", {
        "FY2025": 4528886, "FY2024": 3416837, "FY2023": 3006388, "FY2022": 2344385, "FY2021": 1721315,
        "FY2020": 1262933, "FY2019": 1049748, "FY2018": 733192,
    }),
    ("SECTION", "Derived ratios", {}),
    ("DATA", "Stage 3 (NPL) ratio (Stage 3 / Total gross carrying value)", {
        "FY2025": "3.68%", "FY2024": "2.67%", "FY2023": "2.32%", "FY2022": "2.28%", "FY2021": "2.25%",
        "FY2020": "1.37%", "FY2019": "0.79%", "FY2018": "0.48%",
    }),
    ("DATA", "ECL coverage ratio (Total loss allowance / Total gross carrying value)", {
        "FY2025": "0.47%", "FY2024": "0.63%", "FY2023": "0.67%", "FY2022": "0.61%", "FY2021": "0.64%",
        "FY2020": "1.20%", "FY2019": "0.42%", "FY2018": "0.25%",
    }),
    ("DATA", "Stage 3 coverage ratio (Stage 3 loss allowance / Stage 3 gross carrying value)", {
        "FY2025": "8.04%", "FY2024": "14.48%", "FY2023": "12.93%", "FY2022": "12.14%", "FY2021": "21.25%",
        "FY2020": "36.43%", "FY2019": "29.83%", "FY2018": "15.53%",
    }),
    ("SECTION", "Legacy IAS 39 basis (pre-IFRS 9) - gross carrying value by product (FY2016-FY2017 only)", {}),
    ("DATA", "Property Finance", {
        "FY2017": 225701, "FY2016": 207709,
    }),
    ("DATA", "Specialist/Commercial Mortgages", {
        "FY2017": 192787, "FY2016": 101428,
    }),
    ("DATA", "Asset Finance (Hire Purchase + Finance Leases)", {
        "FY2017": 155714, "FY2016": 112445,
    }),
    ("DATA", "Block Discounting", {
        "FY2017": 62899, "FY2016": 41718,
    }),
    ("DATA", "Discontinued asset-backed lending", {
        "FY2017": 1601, "FY2016": 2573,
    }),
    ("TOTAL", "Total gross carrying value (legacy basis)", {
        "FY2017": 638702, "FY2016": 465873,
    }),
    ("SECTION", "Legacy IAS 39 basis - impairment allowance by product", {}),
    ("DATA", "Property Finance", {
        "FY2017": -3217, "FY2016": -200,
    }),
    ("DATA", "Specialist/Commercial Mortgages", {
        "FY2017": -222, "FY2016": -127,
    }),
    ("DATA", "Asset Finance (Hire Purchase + Finance Leases)", {
        "FY2017": -1588, "FY2016": -359,
    }),
    ("DATA", "Block Discounting", {
        "FY2017": 0, "FY2016": -62,
    }),
    ("DATA", "Discontinued asset-backed lending", {
        "FY2017": -1400, "FY2016": -1600,
    }),
    ("TOTAL", "Total impairment allowance (legacy basis)", {
        "FY2017": -6427, "FY2016": -2348,
    }),
    ("TOTAL", "Net carrying value (legacy basis)", {
        "FY2017": 632275, "FY2016": 463525,
    }),
]

bw.add_asset_quality_sheet(
    title="Hampshire Trust Bank Plc — Asset Quality",
    subtitle="Bank basis, Note 30's financial-assets-at-amortised-cost scope; FY2016-FY2017 use a Legacy IAS 39 section instead - see source note",
    rows=aq_rows,
    sources_text=AQ_SOURCES,
    source_height=260,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, f"{unit}" if unit else None,
                         rows_data, sources_text, note=note, first_col_width=44, source_height=130)


metric(
    "CET1 Capital", "£'000",
    [("Common Equity Tier 1 (CET1) capital", {
        "FY2025": 397694, "FY2024": 300589, "FY2023": 243719, "FY2022": 180193, "FY2021": 174913,
        "FY2020": 151737, "FY2019": 137496, "FY2018": 121690, "FY2017": 112543, "FY2016": 72227,
    })],
    p3_sources(),
)

metric(
    "CET1 Ratio", "%",
    [("Common Equity Tier 1 (CET1) ratio", {
        "FY2025": "13.5%", "FY2024": "13.6%", "FY2023": "13.3%", "FY2022": "13.8%", "FY2021": "18.9%",
        "FY2020": "18.7%", "FY2019": "16.5%", "FY2018": "16.3%", "FY2017": "21%", "FY2016": "16%",
    })],
    p3_sources(),
    note="FY2016-FY2017 are transcribed exactly as each year's own report discloses them - a whole percent, "
         "no decimal precision given (unlike FY2018 onward, where the COREP template discloses to 2 decimal "
         "places). FY2017's own report's FY2016 comparative shows 17%, not the 16% in FY2016's own report - "
         "reproduced as each document discloses it, not force-reconciled.",
)

metric(
    "Tier 1 Capital", "£'000",
    [("Tier 1 capital", {
        "FY2025": 414725, "FY2024": 317619, "FY2023": 260749, "FY2022": 197223, "FY2021": 174913,
        "FY2020": 151737, "FY2019": 137496, "FY2018": 121690, "FY2017": 112543, "FY2016": 72227,
    })],
    p3_sources(),
    note="No Additional Tier 1 instruments are disclosed for FY2016-FY2021 — Tier 1 capital equals CET1 "
         "capital in every one of those 6 years (the first AT1-eligible instrument is the Other equity "
         "instruments (non-controlling interests) issued in FY2022).",
)

metric(
    "Tier 1 Ratio", "%",
    [("Tier 1 ratio", {
        "FY2025": "14.1%", "FY2024": "14.4%", "FY2023": "14.2%", "FY2022": "15.1%", "FY2021": "18.9%",
        "FY2020": "18.7%", "FY2019": "16.5%", "FY2018": "16.3%", "FY2017": "21%", "FY2016": "16%",
    })],
    p3_sources(),
    note="Equals the CET1 Ratio in every year FY2016-FY2021 - no Additional Tier 1 capital existed yet.",
)

metric(
    "Total Capital", "£'000",
    [("Total capital", {
        "FY2025": 494725, "FY2024": 362750, "FY2023": 311890, "FY2022": 227223, "FY2021": 204913,
        "FY2020": 181737, "FY2019": 167496, "FY2018": 151690, "FY2017": 112543, "FY2016": 72227,
    })],
    p3_sources(),
    note="Equals Tier 1 (= CET1) capital in FY2016-FY2017 - no Tier 2 capital existed yet (Subordinated "
         "Liabilities were first issued in FY2018). From FY2018 onward, Total Capital = Tier 1 + the £30,000k "
         "Tier 2 (subordinated debt) capital disclosed each year.",
)

metric(
    "Total Capital Ratio", "%",
    [("Total capital ratio", {
        "FY2025": "16.8%", "FY2024": "16.4%", "FY2023": "17.0%", "FY2022": "17.4%", "FY2021": "22.2%",
        "FY2020": "22.4%", "FY2019": "20.2%", "FY2018": "20.3%", "FY2017": "21%", "FY2016": "16%",
    })],
    p3_sources(),
)

metric(
    "Total RWAs", "£'000",
    [("Total risk-weighted exposure amount", {
        "FY2025": 2949233, "FY2024": 2207947, "FY2023": 1830864, "FY2022": 1310125, "FY2021": 922921,
        "FY2020": 809489, "FY2019": 831229, "FY2018": 746201, "FY2017": 529157, "FY2016": 430807,
    })],
    p3_sources(),
    note="FY2018-FY2020 use each year's own COREP 'Total risk exposure amount' figure, not that same "
         "document's own (internally inconsistent) 'Summary of key ratios' table RWA line - see the note in "
         "the sources above for why. FY2016 (430,807) and FY2017 (529,157) are HTB's own headline 'Risk "
         "weighted assets' line, which those years' documents show to be CREDIT-RISK RWA ONLY: the FY2017 "
         "Pillar 3 p.12 exposure-class table foots to exactly 529,157, and FY2018's COREP total (746,201) "
         "sits beside the same summary line reading 687,497. HTB published no total risk exposure amount for "
         "FY2016/FY2017 in any document, so these two years are knowingly below the true total by that year's "
         "operational risk RWA (~14,863 / ~39,200) rather than being restated on arithmetic. Treat the "
         "FY2017 -> FY2018 step as a basis change as well as growth. Checked and resolved 2026-09-15.",
)

# ---------------------------------------------------------------
# Sheet: RWA Breakdown (placed right after Total RWAs, Bank basis)
# ---------------------------------------------------------------
RWA_BREAKDOWN_SOURCES = (
    "Sources - Hampshire Trust Bank Plc Pillar 3 Disclosures, 'Minimum capital requirement' RWEA table "
    "(UK OV1-style breakdown by risk category), Bank column:\n"
    f"FY2025: Pillar 3 Disclosures | 31 December 2025, p.12 - {P3_2025_URL}\n"
    f"FY2024: same table's Bank 2024 comparative column, p.12 - {P3_2025_URL}\n"
    f"FY2023: Pillar 3 Disclosures | 31 December 2023, p.12, Bank 2023 column - {P3_2023_URL}\n"
    f"FY2022: same table's Bank 2022 comparative column, p.12 - {P3_2023_URL}\n"
    f"FY2021: Pillar 3 Disclosures | 31 December 2021, p.17, Bank's 'Capital resources requirement - "
    f"Pillar 1' table (only Credit risk and Operational risk capital requirements disclosed that year, "
    f"no Counterparty credit risk/Securitisation breakout) - {P3_2021_URL}\n"
    "FY2021's Credit risk and Operational risk RWA figures are derived from that year's disclosed "
    "capital requirements (requirement / 8%), since no direct RWEA table was published that year - "
    "the derived Total (£921,488k) sits ~£1,433k (0.16%) below the disclosed Total RWAs sheet figure "
    "(£922,921k), likely reflecting a small Counterparty credit risk or other category not captured in "
    "the simplified 2-line disclosure - not force-reconciled. Securitisation exposures are a new "
    "category from FY2025 (HTB's first securitisation) - genuinely nil (not merely undisclosed) in "
    "FY2024-FY2022, confirmed since the Total ties exactly without a Securitisation line those years.\n"
    "FY2016-FY2020 use the same derivation as FY2021 (Credit risk/Operational risk Pillar 1 capital "
    "requirement ÷ 8%, from each year's own Pillar 3 'Capital resources requirement – Pillar 1' table, "
    f"Section 4.2/5.2 of the relevant year's own document - {P3_2016_URL} / {P3_2017_URL} / {P3_2018_URL} / "
    f"{P3_2019_URL} / {P3_2020_URL}), since none of these 5 years published a direct RWEA-by-category table "
    "either. FY2018-FY2020's derived totals sit within 0.2% of the Total RWAs sheet figure (same small gap "
    "pattern as FY2021, most likely a small Market/CCR component not separately requirement-disclosed). "
    "FY2016 and FY2017 are a different, larger pattern: their derived Credit+Operational totals (£445,663k "
    "and £568,363k) sit 3-7% ABOVE the Total RWAs sheet figure (£430,807k/£529,157k) - recomputing shows "
    "the Total RWAs sheet figure for these 2 years is itself extremely close to Credit risk RWA ALONE "
    "(£430,800k and £529,163k respectively, both within £10k), meaning HTB's own FY2016/FY2017 'Risk "
    "weighted assets' summary-table figure appears to exclude Operational risk RWA entirely, unlike "
    "FY2018 onward - a genuine, structural difference in what that year's summary line actually measures, "
    "not a transcription error. Both risk categories are shown here regardless, so this sheet's own Total "
    "row does not match the Total RWAs sheet for FY2016/FY2017 - flagged rather than force-matched.\n"
    "RESOLVED 2026-09-15 (RWA cross-sheet sweep - do not re-flag): the FY2016/FY2017 divergence between this "
    "sheet's Total row and the Total RWAs sheet is confirmed from the primary documents and is expected. The "
    "FY2017 Pillar 3 p.12 credit-risk exposure-class table foots to exactly 529,157 in its RWAs column, "
    "which is the same number HTB prints as headline 'Risk weighted assets' - so the headline line is "
    "credit-only. FY2018 proves it independently: headline 687,497 alongside that document's own COREP row "
    "010 'Total risk exposure amount' of 746,201 (difference 58,704 ~= that year's operational risk RWA of "
    "58,463). HTB never published a FY2016/FY2017 total risk exposure amount anywhere, so the Total RWAs "
    "sheet keeps the only disclosed figure rather than adopting this sheet's derived Total - the two are "
    "measuring different things by design, and neither number is to be changed to make them agree."
)

rwa_breakdown_rows = [
    ("DATA", "Credit risk (excluding CCR)", {
        "FY2025": 2627722, "FY2024": 1952854, "FY2023": 1623626, "FY2022": 1151820, "FY2021": 816163,
        "FY2020": 725113, "FY2019": 757438, "FY2018": 687500, "FY2017": 529163, "FY2016": 430800,
    }),
    ("DATA", "Counterparty credit risk (CCR)", {
        "FY2025": 1435, "FY2024": 8733, "FY2023": 9410, "FY2022": 13524,
    }),
    ("DATA", "Securitisation exposures", {
        "FY2025": 35085, "FY2024": 0, "FY2023": 0, "FY2022": 0,
    }),
    ("DATA", "Operational risk", {
        "FY2025": 284991, "FY2024": 246360, "FY2023": 197828, "FY2022": 144781, "FY2021": 105325,
        "FY2020": 83038, "FY2019": 73525, "FY2018": 58463, "FY2017": 39200, "FY2016": 14863,
    }),
    ("TOTAL", "Total RWAs", {
        "FY2025": 2949233, "FY2024": 2207947, "FY2023": 1830864, "FY2022": 1310125, "FY2021": 921488,
        "FY2020": 808151, "FY2019": 830963, "FY2018": 745963, "FY2017": 568363, "FY2016": 445663,
    }),
]

bw.add_rwa_breakdown_sheet(
    title="Hampshire Trust Bank Plc — RWA Breakdown",
    subtitle="Bank basis; FY2016-FY2021 derived from the disclosed capital requirement (÷8%) - see source note for the FY2016/FY2017 pattern",
    rows=rwa_breakdown_rows,
    sources_text=RWA_BREAKDOWN_SOURCES,
    source_height=230,
    unit_suffix=" (£'000)",
)

metric(
    "Leverage Ratio", "%",
    [("Leverage ratio", {
        "FY2025": "7.5%", "FY2024": "8.1%", "FY2023": "7.5%", "FY2022": "9.2%", "FY2021": "8.0%",
        "FY2020": "10%", "FY2019": "11%", "FY2018": "12%", "FY2017": "15%", "FY2016": "11%",
    })],
    p3_sources(),
    note="FY2016-FY2020 are transcribed exactly as each year's own report discloses them - a whole percent, "
         "no decimal precision given (unlike FY2021 onward's one-decimal figures).",
)

metric(
    "LCR", "%",
    [("Liquidity Coverage Ratio", {
        "FY2025": "346.9%", "FY2024": "391.1%", "FY2023": "388.6%", "FY2022": "386.9%", "FY2021": "314.8%",
        "FY2020": "393%", "FY2019": "242%", "FY2018": "335%", "FY2017": "467%", "FY2016": "816%",
    })],
    p3_sources(),
    note="Disclosed only at consolidated Group level from FY2022 onward ('Liquidity is managed on a "
         "consolidated basis hence only Group metrics are reported') — no separate Bank-solo LCR exists to "
         "report for those years. FY2016-FY2021 all predate the Group/Bank split; each year's single "
         "reported (Bank-only) value is used, transcribed as a whole percent exactly as each year's own "
         "report discloses it (no decimal precision given before FY2022). FY2016's 816% is genuinely this "
         "high - the Bank was very new (first banking-licence year on a materially smaller loan book) and "
         "held a correspondingly outsized liquid-asset buffer relative to its Pillar 1 requirement that year.",
)

metric(
    "NSFR", "%",
    [("Net Stable Funding Ratio", {
        "FY2025": "158.9%", "FY2024": "163.3%", "FY2023": "147.7%", "FY2022": "152.5%", "FY2021": "120.5%",
    })],
    p3_sources(),
    note="Disclosed only at consolidated Group level from FY2022 onward, same basis as LCR above. FY2021 "
         "predates the Group/Bank split; its single reported value is used. NSFR is never mentioned at all "
         "in any of HTB's FY2016-FY2020 Pillar 3 disclosures (confirmed by direct text search of each "
         "document) - the concept isn't introduced into HTB's own reporting until FY2021, a genuine "
         "disclosure-regime floor rather than a search gap.",
)

bw.add_not_disclosed_metric_sheets(["MREL Ratio"], p3_sources())

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {
            "FY2025": 6126399, "FY2024": 5387529, "FY2023": 4063807, "FY2022": 3200482, "FY2021": 2190531,
            "FY2020": 1522362, "FY2019": 1283904, "FY2018": 1024173, "FY2017": 742260, "FY2016": 606660,
        }),
        ("Loans and advances to customers - at amortised cost", {
            "FY2025": 4540376, "FY2024": 3391908, "FY2023": 2967326, "FY2022": 2243123, "FY2021": 1704683,
            "FY2020": 1277092, "FY2019": 1053365, "FY2018": 733192, "FY2017": 632275, "FY2016": 463525,
        }),
        ("Customer deposits", {
            "FY2025": 5232516, "FY2024": 4526003, "FY2023": 3205681, "FY2022": 2420694, "FY2021": 1633046,
            "FY2020": 1125560, "FY2019": 904171, "FY2018": 720718, "FY2017": 596296, "FY2016": 523315,
        }),
        ("Total equity", {
            "FY2025": 434367, "FY2024": 374559, "FY2023": 322801, "FY2022": 258864, "FY2021": 188836,
            "FY2020": 154058, "FY2019": 151475, "FY2018": 125750, "FY2017": 115640, "FY2016": 74072,
        }),
    ],
    balance_sheet_unit="£'000",
    income_statement_totals=[
        ("Net interest income", {
            "FY2025": 167619, "FY2024": 145342, "FY2023": 131062, "FY2022": 98584, "FY2021": 69157,
            "FY2020": 54372, "FY2019": 46239, "FY2018": 36974, "FY2017": 34113, "FY2016": 20625,
        }),
        ("Administrative expenses", {
            "FY2025": -83039, "FY2024": -75545, "FY2023": -69237, "FY2022": -56984, "FY2021": -46313,
            "FY2020": -32236, "FY2019": -28587, "FY2018": -24700, "FY2017": -20110, "FY2016": -15502,
        }),
        ("Profit after tax for the year", {
            "FY2025": 60116, "FY2024": 53054, "FY2023": 67273, "FY2022": 54033, "FY2021": 20562,
            "FY2020": 2554, "FY2019": 10799, "FY2018": 9030, "FY2017": 8019, "FY2016": 2155,
        }),
    ],
    income_statement_unit="£'000",
    equity_changes_totals=[
        ("Opening equity", {
            "FY2025": 374559, "FY2024": 322801, "FY2023": 258864, "FY2022": 188836, "FY2021": 154058,
            "FY2020": 151475, "FY2019": 125750, "FY2018": 115640, "FY2017": 74072, "FY2016": 51576,
        }),
        ("Total comprehensive income for the year", {
            "FY2025": 60608, "FY2024": 53479, "FY2023": 64045, "FY2022": 54162, "FY2021": 20562,
            "FY2020": 2554, "FY2019": 10849, "FY2018": 8980, "FY2017": 8019, "FY2016": 2155,
        }),
        ("Closing equity", {
            "FY2025": 434367, "FY2024": 374559, "FY2023": 322801, "FY2022": 258864, "FY2021": 188836,
            "FY2020": 154058, "FY2019": 151475, "FY2018": 125750, "FY2017": 115640, "FY2016": 74072,
        }),
    ],
    equity_changes_unit="£'000",
    cash_flow_totals=[
        ("Net cash from/(used in) operating activities", {
            "FY2025": -328407, "FY2024": 619425, "FY2023": -46888, "FY2022": 259350, "FY2021": 267024,
            "FY2020": 96228, "FY2019": -20407, "FY2018": -30782, "FY2017": -67300, "FY2016": 57542,
        }),
        ("Net cash from/(used in) investing activities", {
            "FY2025": -450560, "FY2024": 30745, "FY2023": 38042, "FY2022": -39977, "FY2021": -181730,
            "FY2020": -23034, "FY2019": -3680, "FY2018": -2666, "FY2017": -3148, "FY2016": -1911,
        }),
        ("Net cash from/(used in) financing activities", {
            "FY2025": 22745, "FY2024": 308331, "FY2023": 26678, "FY2022": -2722, "FY2021": 12357,
            "FY2020": -1131, "FY2019": 13922, "FY2018": 30000, "FY2017": 33000, "FY2016": 20000,
        }),
        ("Cash and cash equivalents at end of year", {
            "FY2025": 679085, "FY2024": 1435307, "FY2023": 476806, "FY2022": 458974, "FY2021": 242323,
            "FY2020": 156707, "FY2019": 84644, "FY2018": 94809, "FY2017": 98257, "FY2016": 135705,
        }),
    ],
    cash_flow_unit="£'000",
    ratios=[
        ("CET1 Ratio", {
            "FY2025": "13.5%", "FY2024": "13.6%", "FY2023": "13.3%", "FY2022": "13.8%", "FY2021": "18.9%",
            "FY2020": "18.7%", "FY2019": "16.5%", "FY2018": "16.3%", "FY2017": "21%", "FY2016": "16%",
        }),
        ("Tier 1 Ratio", {
            "FY2025": "14.1%", "FY2024": "14.4%", "FY2023": "14.2%", "FY2022": "15.1%", "FY2021": "18.9%",
            "FY2020": "18.7%", "FY2019": "16.5%", "FY2018": "16.3%", "FY2017": "21%", "FY2016": "16%",
        }),
        ("Total Capital Ratio", {
            "FY2025": "16.8%", "FY2024": "16.4%", "FY2023": "17.0%", "FY2022": "17.4%", "FY2021": "22.2%",
            "FY2020": "22.4%", "FY2019": "20.2%", "FY2018": "20.3%", "FY2017": "21%", "FY2016": "16%",
        }),
        ("Leverage Ratio", {
            "FY2025": "7.5%", "FY2024": "8.1%", "FY2023": "7.5%", "FY2022": "9.2%", "FY2021": "8.0%",
            "FY2020": "10%", "FY2019": "11%", "FY2018": "12%", "FY2017": "15%", "FY2016": "11%",
        }),
        ("LCR", {
            "FY2025": "346.9%", "FY2024": "391.1%", "FY2023": "388.6%", "FY2022": "386.9%", "FY2021": "314.8%",
            "FY2020": "393%", "FY2019": "242%", "FY2018": "335%", "FY2017": "467%", "FY2016": "816%",
        }),
        ("NSFR", {
            "FY2025": "158.9%", "FY2024": "163.3%", "FY2023": "147.7%", "FY2022": "152.5%", "FY2021": "120.5%",
        }),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own "
         "source citation for the underlying document/page. All Cash Flow figures are the Bank (entity-level) "
         "column; LCR/NSFR are Group-level from FY2022 onward (see the LCR/NSFR sheets' notes). FY2016-FY2020 "
         "Cash flow figures use each year's own originally-published statement; note the genuine FY2020/FY2021 "
         "cash-flow restatement discontinuity documented on the Cash Flow Statement sheet's own source note.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/HAMPSHIRE TRUST BANK FINANCIALS.xlsx")
