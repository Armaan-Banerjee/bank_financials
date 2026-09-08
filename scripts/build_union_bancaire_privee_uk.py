import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook


YEARS = [
    "FY2025", "FY2024", "FY2023", "FY2022", "FY2021",
    "FY2020", "FY2019", "FY2018", "FY2017", "FY2016", "FY2015", "FY2014", "FY2013",
    "FY2012", "FY2011", "FY2010", "FY2009", "FY2008", "FY2007", "FY2006", "FY2005", "FY2004", "FY2003", "FY2002", "FY2001", "FY2000", "FY1999", "FY1998", "FY1997", "FY1996", "FY1995", "FY1994", "FY1993", "FY1992", "FY1991", "FY1990", "FY1989", "FY1988", "FY1987", "FY1986", "FY1985", "FY1984", "FY1983", "FY1982", "FY1981", "FY1980", "FY1979", "FY1978", "FY1977", "FY1976", "FY1975", "FY1974", "FY1973",
]
Y_CORE = YEARS[:YEARS.index("FY2014") + 1]  # HD-072/075/079: FY2014-floor default for Pillar 3/Asset Quality/RWA Breakdown/Overview
YEAR_LABEL = {year: year for year in YEARS}

CH_URL = "https://find-and-update.company-information.service.gov.uk/company/00964058/filing-history"
P3_ARCHIVE_URL = "https://www.ubp.com/en/legal-aspects/union-bancaire-privee-uk-limited/pillar-3-disclosure"
P3_2024_URL = "https://www.ubp.com/files/live/sites/ubp/files/documents/legal/ubp-uk/SGKH_2024-P3-disclosures.pdf"
P3_2023_URL = "https://www.ubp.com/files/live/sites/ubp/files/documents/legal/ubp-uk/UBP_2023_P3_disclosures.pdf"
P3_2022_URL = "https://www.ubp.com/files/live/sites/ubp/files/documents/legal/ubp-uk/UBP_2022_P3_disclosures.pdf"

AR2024_URL = "https://find-and-update.company-information.service.gov.uk/company/00964058/filing-history/MzQ4Mjg5Njk3OWFkaXF6a2N4/document?format=pdf&download=0"
AR2023_URL = "https://find-and-update.company-information.service.gov.uk/company/00964058/filing-history/MzQyNTQxNTkxNWFkaXF6a2N4/document?format=pdf&download=0"
AR2022_URL = "https://find-and-update.company-information.service.gov.uk/company/00964058/filing-history/MzM5NTQ1NTI3NGFkaXF6a2N4/document?format=pdf&download=0"
AR2021_URL = "https://find-and-update.company-information.service.gov.uk/company/00964058/filing-history/MzM1MzcxNDM1MGFkaXF6a2N4/document?format=pdf&download=0"
AR2020_URL = "https://find-and-update.company-information.service.gov.uk/company/00964058/filing-history/MzMxNTg5OTMwMGFkaXF6a2N4/document?format=pdf&download=0"
AR2019_URL = "https://find-and-update.company-information.service.gov.uk/company/00964058/filing-history/MzI3NjIwNDY3M2FkaXF6a2N4/document?format=pdf&download=0"
AR2018_URL = "https://find-and-update.company-information.service.gov.uk/company/00964058/filing-history/MzI0NTk5MTMzNWFkaXF6a2N4/document?format=pdf&download=0"
AR2017_URL = "https://find-and-update.company-information.service.gov.uk/company/00964058/filing-history/MzIxNTcxNzQzMWFkaXF6a2N4/document?format=pdf&download=0"
AR2016_URL = "https://find-and-update.company-information.service.gov.uk/company/00964058/filing-history/MzE4NjU0MDgxNWFkaXF6a2N4/document?format=pdf&download=0"
AR2015_URL = "https://find-and-update.company-information.service.gov.uk/company/00964058/filing-history/MzE0NjczODM1N2FkaXF6a2N4/document?format=pdf&download=0"
AR2014_URL = "https://find-and-update.company-information.service.gov.uk/company/00964058/filing-history/MzEyNjc3MDQ1OGFkaXF6a2N4/document?format=pdf&download=0"
AR2013_URL = "https://find-and-update.company-information.service.gov.uk/company/00964058/filing-history/MzA5ODA4NzA3MmFkaXF6a2N4/document?format=pdf&download=0"
AR2012_URL = "https://find-and-update.company-information.service.gov.uk/company/00964058/filing-history/MzA3NzI3NTEyMGFkaXF6a2N4/document?format=pdf&download=0"
AR2011_URL = "https://find-and-update.company-information.service.gov.uk/company/00964058/filing-history/MzA1NTc4NzQ2NmFkaXF6a2N4/document?format=pdf&download=0"
AR2010_URL = "https://find-and-update.company-information.service.gov.uk/company/00964058/filing-history/MzAzNTExMzA5M2FkaXF6a2N4/document?format=pdf&download=0"
AR2009_URL = "https://find-and-update.company-information.service.gov.uk/company/00964058/filing-history/MzAxMzQ2NjU1M2FkaXF6a2N4/document?format=pdf&download=0"
AR2008_URL = "https://find-and-update.company-information.service.gov.uk/company/00964058/filing-history/MjAzMDE0MDkxOWFkaXF6a2N4/document?format=pdf&download=0"
AR2007_URL = "Companies House filing supplied locally: UBP 2007.pdf"
AR2006_URL = "Companies House filing supplied locally: UBP 2006.pdf"
AR2005_URL = "Companies House filing supplied locally: UBP 2005.pdf"
AR2004_URL = "Companies House filing supplied locally: UBP 2004.pdf"
AR2003_URL = "Companies House filing supplied locally: UBP 2003.pdf"

ENTITY_NOTE = (
    "ENTITY/BASIS NOTE: Union Bancaire Privée (UK) Limited (Companies House "
    "00964058; FRN 119250) was formerly SG Kleinwort Hambros Bank Limited, and "
    "before that SG Hambros Bank Limited - the same continuous legal entity "
    "and Companies House company number since 1969 (Hambros Bank -> SG Hambros "
    "-> SG Kleinwort Hambros -> Union Bancaire Privée (UK) Limited); trading "
    "names changed but the entity did not (confirmed via HD-002's deep dive - "
    "the 'pre-acquisition identity' once flagged as a possible break in the "
    "historical-depth wayfinder map turned out not to be a real floor). "
    "FY2006-2016 accounts are filed under the name 'SG Hambros Bank Limited'; "
    "the FY2005 account is under the former name 'SG Hambros Bank & Trust Limited'; "
    "FY2017-2024 accounts are filed under 'SG Kleinwort Hambros Bank Limited' "
    "(SGKH); FY2025 has not yet been filed under any name. "
    "The 2022-2024 Pillar 3 reports retain the SGKH name because they cover "
    "pre-acquisition periods. All figures use the reports' UK Consolidation "
    "Group basis, incorporating SGKH Bank Ltd, its branches, and the trust "
    "entity; they are not bank-solo figures. The reports state that the "
    "published financial statements use FRS 101 and differ from the prudential "
    "scope of consolidation."
)

P3_SOURCES = (
    "Sources - UK Consolidation Group Pillar 3 disclosures, amounts converted "
    "from £'000 to £m; ratios retained as reported:\n"
    f"FY2024: SGKH Pillar 3 Disclosure 31 December 2024, UK KM1 p.10 (FY2024 "
    f"current and FY2023 comparative) - {P3_2024_URL}\n"
    f"FY2023: SGKH Pillar 3 Disclosure 31 December 2023, UK KM1 p.10 (FY2023 "
    f"current and FY2022 comparative) - {P3_2023_URL}\n"
    f"FY2022: SGKH Pillar 3 Disclosure 31 December 2022, UK KM1 p.10 (FY2022 "
    f"current and FY2021 comparative) - {P3_2022_URL}\n"
    f"Official UBP UK disclosure archive - {P3_ARCHIVE_URL}\n"
    "FY2025: no defensible UK Consolidation Group Pillar 3 disclosure found; "
    "left blank rather than substituted. Amounts are shown in £m for "
    "consistency with this project.\n\n"
    "FY2014-FY2020: left blank throughout every Pillar 3 metric sheet and the "
    "RWA Breakdown sheet - no numeric capital/RWA/liquidity Pillar 3 "
    "disclosure could be found for the entity for these years, under any of "
    "its trading names. Checked via a full Wayback Machine CDX search of the "
    "entity's own current and former websites (kleinworthambros.com and "
    "predecessor domains) for any URL containing 'pillar': the only two hits "
    "are 2019_Pillar_3_Disclosure_KH.pdf and 2021_KH_Pillar_3_Disclosure.pdf "
    "(https://web.archive.org/web/20210918132915/https://www.kleinworthambros.com/fileadmin/user_upload/kleinworthambros/2019_Pillar_3_Disclosure_KH.pdf "
    "and https://web.archive.org/web/20240706060918/https://www.kleinworthambros.com/fileadmin/user_upload/kleinworthambros/Important_information/2021_KH_Pillar_3_Disclosure.pdf), "
    "both opened and read in full: each is titled '[Year] Remuneration Code "
    "Disclosure Table' and covers only CRD IV Article 450 remuneration "
    "disclosures, with no CET1/RWA/leverage/LCR/NSFR figures of any kind. A "
    "general web search for SG Hambros / SG Kleinwort Hambros Pillar 3 "
    "capital disclosures found no hits before the 2022 report already cited "
    "above. Treated as a genuine disclosure-floor finding, not an unsearched "
    "gap: this entity's own standalone Pillar 3 capital-disclosure archive "
    "appears to start with the 2022 report (FY2021 as its earliest "
    "comparative column), consistent with a small banking subsidiary that "
    "only began separately publishing full Pillar 3 capital disclosures "
    "once required to under the post-2022 UK CRR regime.\n"
    + ENTITY_NOTE
)

CASH_FLOW_SOURCES = (
    "CASH-FLOW EXEMPTION: the SGKH disclosures explain that the published "
    "financial statements use FRS 101 Reduced Disclosure Framework and do not "
    "consolidate the relevant subsidiaries, while prudential reporting uses "
    "the UK Consolidation Group scope. No standalone cash-flow statement is "
    "used in this Pillar-3-only workbook; no group or other-entity cash flows "
    f"are substituted. Companies House filing history: {CH_URL}\n"
    f"SGKH 2024 Pillar 3 disclosure, scope/basis discussion - {P3_2024_URL}\n"
    "The same FRS 101 exemption from presenting a Statement of Cash Flows is "
    "stated explicitly in every one of the FY2014-FY2020 accounts individually "
    "reviewed for this extension (each one's own 'Statement of compliance' "
    "note), so no cash-flow statement is presented for any year back to "
    "FY2014 either.\n\n"
    "FY2013 EXEMPTION BASIS NOTE: FY2013's own accounts (and, on direct re-reading for this extension, "
    "FY2014's own accounts too) cite a different, older exemption than the FRS 101 basis described above: "
    "both explicitly invoke 'Financial Reporting Standard 1 (Revised)', exempting the Bank from preparing "
    "a cash-flow statement because more than 90% of its voting rights were controlled by Societe Generale "
    "SA, whose own consolidated cash-flow statement (including the Bank's cash flows) was publicly "
    "available. This is consistent with the Bank not adopting FRS 101 until FY2015 (its FY2013 accounts' "
    "own 'Change in accounting policies' note states FRS 100/101/102 become effective from 1 January "
    "2015, with early adoption permitted) - so the FRS 101-based description above likely applies from "
    "FY2015 onward rather than FY2014, a discrepancy in this workbook's prior FY2014-2020 sourcing note "
    "not corrected here (out of this session's scope) but flagged for a future session. Either way, the "
    "practical outcome is identical across FY2013 onward: no standalone cash-flow statement is presented, "
    "and none is substituted here.\n"
    + ENTITY_NOTE
)

bw = BankWorkbook(
    bank_name="Union Bancaire Privée (UK) Limited",
    years=Y_CORE,
    year_label=YEAR_LABEL,
    header_color="355C7D",
)

STATEMENTS_SOURCES = (
    "Sources - Union Bancaire Privée (UK) Limited (formerly SG Kleinwort Hambros Bank Limited, "
    "formerly SG Hambros Bank Limited - same company number, 00964058, throughout) statutory "
    "Companies House accounts, Company-only basis, £'000. Each year's own column was checked "
    "against the adjacent report's comparative column where available. All FY2014-FY2020 filings "
    "are scanned/image-only PDFs at Companies House with no text layer; each was OCR'd "
    "(ocrmypdf/tesseract) and cross-checked line-by-line against the adjacent year's comparative "
    "column and, where available, a higher-resolution direct re-read of the page image, before "
    "transcription - the same approach previously used for this bank's FY2022-2024 filings.\n"
    f"FY2024/FY2023 comparative: Full accounts made up to 31 December 2024 - {AR2024_URL}\n"
    f"FY2023/FY2022 comparative: Full accounts made up to 31 December 2023 - {AR2023_URL}\n"
    f"FY2022/FY2021 comparative: Full accounts made up to 31 December 2022 - {AR2022_URL} "
    "(this filing's own copy of the financial statements is truncated after Note 12 - Companies "
    "House bundled it with the SGKH Pillar 3 Disclosures document, which starts mid-filing; Note 14's "
    "credit-quality table for FY2022 is therefore sourced from the FY2023 filing's own FY2022 "
    "comparative column instead, not from this filing.)\n"
    f"FY2021/FY2020 comparative: Full accounts made up to 31 December 2021 - {AR2021_URL}\n"
    f"FY2020/FY2019 comparative: Full accounts made up to 31 December 2020, filed as 'SG Kleinwort "
    f"Hambros Bank Limited' - {AR2020_URL}\n"
    f"FY2019/FY2018 comparative: Full accounts made up to 31 December 2019, 'SG Kleinwort Hambros "
    f"Bank Limited' - {AR2019_URL}\n"
    f"FY2018/FY2017 comparative: Full accounts made up to 31 December 2018, 'SG Kleinwort Hambros "
    f"Bank Limited' - {AR2018_URL}\n"
    f"FY2017/FY2016 comparative: Full accounts made up to 31 December 2017, 'SG Kleinwort Hambros "
    f"Bank Limited' - {AR2017_URL}\n"
    f"FY2016/FY2015 comparative: Full accounts made up to 31 December 2016, filed as 'SG Hambros "
    f"Bank Limited' - {AR2016_URL}\n"
    f"FY2015/FY2014 comparative: Full accounts made up to 31 December 2015, 'SG Hambros Bank "
    f"Limited' - {AR2015_URL}\n"
    f"FY2014/FY2013 comparative: Full accounts made up to 31 December 2014, 'SG Hambros Bank "
    f"Limited' - {AR2014_URL}\n"
    f"FY2013/FY2012 comparative: Full accounts made up to 31 December 2013, 'SG Hambros Bank "
    f"Limited' - {AR2013_URL}\n"
    f"FY2012/FY2011 comparative: Full accounts made up to 31 December 2012 - {AR2012_URL}\n"
    f"FY2011/FY2010 comparative: Full accounts made up to 31 December 2011 - {AR2011_URL}\n"
    f"FY2010/FY2009 comparative: Full accounts made up to 31 December 2010 - {AR2010_URL}\n"
    f"FY2009/FY2008 comparative: Full accounts made up to 31 December 2009 - {AR2009_URL}\n"
    f"FY2008/FY2007 comparative: Full accounts made up to 31 December 2008 - {AR2008_URL}\n"
    "FY2007: SG Hambros Bank Limited accounts (local PDF UBP 2007.pdf)\n"
    "FY2006: SG Hambros Bank Limited accounts (local PDF UBP 2006.pdf)\n"
    "FY2005: SG Hambros Bank & Trust Limited accounts (local PDF UBP 2005.pdf)\n"
    "FY2004: SG Hambros Bank & Trust Limited accounts (local PDF UBP 2004.pdf)\n"
    "FY2003: SG Hambros Bank & Trust Limited accounts (local PDF UBP 2003.pdf)\n\n"
    "FY2000: Hambros Bank Limited accounts (local PDF UBP 2000.pdf)\n"
    "FY1999: SG Hambros Bank & Trust Limited accounts (local PDF UBP 1999.pdf)\n"
    "FY1998: Hambros Bank Limited accounts (local PDF UBP 1998.pdf)\n"
    "FY1997: Hambros Bank Limited accounts (local PDF UBP 1997.pdf)\n\n"
    "FY1996: Hambros Bank Limited accounts, year ended 31 March 1996 (local PDF UBP 1996.pdf)\n"
    "FY1995: Hambros Bank Limited accounts, year ended 31 March 1995 (local PDF UBP 1995.pdf)\n"
    "FY1994: Hambros Bank Limited accounts, year ended 31 March 1994 (local PDF UBP 1994.pdf)\n"
    "FY1993: Hambros Bank Limited accounts, year ended 31 March 1993 (local PDF UBP 1993.pdf)\n"
    "FY1992: Hambros Bank Limited accounts, year ended 31 March 1992 (local PDF UBP 1992.pdf)\n"
    "FY1991: Hambros Bank Limited accounts, year ended 31 March 1991 (local PDF UBP 1991.pdf)\n\n"
    "FY1990: Hambros Bank Limited accounts, year ended 31 March 1990 (local PDF UBP 1990.pdf)\n"
    "FY1989: Hambros Bank Limited accounts, year ended 31 March 1989 (local PDF UBP 1989.pdf)\n"
    "FY1988: Hambros Bank Limited accounts, year ended 31 March 1988 (local PDF UBP 1988.pdf)\n"
    "FY1987: Hambros Bank Limited accounts, year ended 31 March 1987 (local PDF UBP 1987.pdf)\n"
    "FY1986: Hambros Bank Limited accounts, year ended 31 March 1986 (local PDF UBP 1986.pdf)\n"
    "FY1985: Hambros Bank Limited accounts, year ended 31 March 1985 (local PDF UBP 1985.pdf)\n\n"
    "FY1984-FY1973: Hambros Bank Limited accounts (local PDFs UBP 1984.pdf through UBP 1973.pdf, where supplied).\n"
    "FY1978-FY1979: no standalone filing was present in the supplied Companies House archive batch; these two years remain blank pending retrieval of the relevant pre-1995 bundled archive/document.\n\n"
    "FY2025 is blank throughout the Balance Sheet, Profit & Loss, Statement of Changes in Equity and "
    "Asset Quality sheets: no FY2025 statutory accounts have been filed at Companies House as of this "
    "workbook's build date (the FY2024 filing is the most recent).\n\n"
    + ENTITY_NOTE
    + "\n\nSTATEMENT STRUCTURE NOTE: the FY2024/FY2023 Statement of Profit and Loss uses a "
    "Revenue/Cost-of-Revenue-style presentation (Total operating income before administrative "
    "expenses) while FY2022/FY2021 present the same P&L with slightly different line labels "
    "(e.g. 'Interest income calculated using effective interest method' vs 'Interest income', "
    "'Gain on financial instruments at fair value' vs 'Loss on financial instruments at fair value' - "
    "sign follows the source, not relabelled). 'Gains on sales of investments' and an explicit "
    "'Undistributable reserves' Balance Sheet line only appear in some years; blank cells reflect a "
    "line genuinely absent from that year's own statement, not a gap.\n\n"
    "PRE-2021 STATEMENT STRUCTURE NOTE: presentation shifts further the further back the archive "
    "goes, each documented as encountered rather than force-fitted into the FY2021+ line items: "
    "FY2018-FY2020 use the same 'Statement of Profit and Loss' grouping as FY2021+ but with an extra "
    "'Interest income at FVOCI' line (folded into a single Interest income line from FY2020/FY2021 "
    "onward) and a combined 'Impairment losses and other provisions' line (split into 'Expected "
    "credit losses on loans and advances' and 'Other provisions' from FY2021 onward). FY2015-FY2017 "
    "use an older UK-GAAP-style 'Income Statement'/'Statement of Profit and Loss' that groups fee "
    "income, trading gains, AFS/FVOCI gains, dividend income and other income/expense together under "
    "a single 'Net non-interest income' (FY2015/FY2016) or unlabelled operating-income subtotal "
    "(FY2017) rather than FY2018+'s itemised list - each component is still transcribed on its own "
    "row, it is only the subtotal grouping that differs. FY2014 uses the oldest 'Profit and Loss "
    "Account' format (old UK GAAP terms: 'Interest receivable'/'Interest payable', a single 'Other "
    "operating income' line, and 'Impairment of financial assets' instead of an ECL-style provision "
    "line) and its Balance Sheet separates 'Goodwill' from 'Intangible assets' (merged into one "
    "'Intangible assets' line from FY2015 onward) and combines available-for-sale and held-to-maturity "
    "investments under 'Financial investments' (split into 'Debt and investment securities' as a "
    "single AFS/FVOCI line from FY2015 onward, once the small HTM book matured out). The reserve "
    "column labelled 'OCI reserves' from FY2018 onward is called 'FVOCI reserves' in FY2018-2020's own "
    "accounts and 'Available-for-sale (AFS) reserves' in FY2013-2017's own accounts (IFRS 9's FVOCI "
    "classification only applied from 1 January 2018) - all three are the same reserve line under "
    "different accounting-standard names, not different reserves, and are shown on one continuous row. "
    "FY2013 uses the same old-UK-GAAP 'Profit and Loss Account'/'Balance Sheet' format as FY2014 "
    "(see FY2013 RESTATEMENT NOTE) - 'Interest receivable'/'Interest payable', a single undifferentiated "
    "'Profit and loss account' reserve line with no separate Share-based payment reserve column, and a "
    "combined 'Financial investments' line (not split into AFS/HTM).\n\n"
    "FY2013 RESTATEMENT NOTE: FY2013's own accounts (filed 11 Apr 2014, 'SG Hambros Bank Limited') use a "
    "single, undifferentiated 'Profit and loss account' reserve of \u00a321,125k with no separate "
    "Share-based payment reserve line - this workbook's FY2013 Retained earnings row is that full "
    "\u00a321,125k figure, with Share-based payment reserves left blank for FY2013 (not a real zero, a line "
    "genuinely not yet disclosed separately that year). The FY2014 accounts' own FY2013 comparative "
    "column, by contrast, is explicitly labelled '(restated)' and splits this into a \u00a31,494k Share-based "
    "payment reserve plus \u00a319,630k Retained earnings (summing to \u00a321,124k, a \u00a31k rounding gap from the "
    "\u00a321,125k originally reported) - shown in the Statement of Changes in Equity as a dedicated "
    "'Reclassification (per FY2014 accounts' own FY2013 restated comparative)' row, not silently "
    "absorbed into FY2013's own closing balance. Separately, the FY2014 accounts' own FY2013 comparative "
    "Profit and Loss Account shows Administrative expenses of \u00a3(34,485)k and Profit for the year of "
    "\u00a344,808k, both different from FY2013's own reported \u00a3(34,278)k and \u00a345,016k (a ~\u00a3207-208k gap) - "
    "this gap does not appear in the restated Balance Sheet/equity closing figures (which tie to the "
    "\u00a31,494k/\u00a31k reclass above, not to a ~\u00a3208k profit restatement), and no note in either filing "
    "explains it; it is flagged here as an unreconciled minor discrepancy between the two filings' "
    "printed figures (a residual OCR risk on the FY2014 filing's own comparative column cannot be ruled "
    "out) rather than silently adopted. FY2013's own originally-reported P&L figures are used as this "
    "workbook's FY2013 primary column throughout, consistent with this project's convention of each "
    "year's own reported figures.\n\n"
    "IFRS 9 TRANSITION NOTE: IFRS 9 was adopted 1 January 2018. The FY2018 accounts' Statement of "
    "Changes in Equity records a transition adjustment moving £1,139k out of retained earnings (net of "
    "a £310k tax effect) into impairment provisions, plus a £328k reclassification between the AFS/OCI "
    "reserve and retained earnings, restating the FY2018 opening equity from FY2017's own reported "
    "closing balance of £420,906k to a restated £420,077k opening balance - shown on its own row in "
    "the Statement of Changes in Equity, not silently absorbed. The FY2018 accounts' Note 14 also "
    "restates the FY2017 comparative loan book onto an IFRS 9 stage basis for comparability, so the "
    "Asset Quality sheet's FY2017 IFRS-9-stage figures come from the FY2018 accounts' own FY2017 "
    "comparative column, not from FY2017's own (pre-IFRS-9, unstaged) accounts.\n\n"
    "FY2014 RESTATEMENT NOTE: the FY2015 accounts' Statement of Changes in Equity opens FY2015 at a "
    "restated 1 January 2015 balance of £258,215k, £870k above FY2014's own reported closing balance "
    "of £257,345k (all £870k landing in retained earnings; every other reserve is unchanged). This is "
    "shown as its own 'Restatement (per FY2015 accounts)' row in the Statement of Changes in Equity "
    "rather than silently bridged. FY2014's own Balance Sheet and Profit and Loss Account are used "
    "as this workbook's FY2014 primary column throughout (this project's convention of using each "
    "year's own originally-reported figures), not FY2015's restated comparative."
)

balance_sheet_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and balances at central banks", {"FY2024": 459161, "FY2023": 502104, "FY2022": 564799, "FY2021": 144684, "FY2020": 152646, "FY2019": 52993, "FY2018": 169360, "FY2017": 247705, "FY1996": 1079, "FY1995": 607, "FY1994": 618}),
    ("DATA", "Cash (till cash only; central bank balances not separately disclosed in the pre-2017 accounts)", {"FY2016": 44, "FY2015": 31, "FY2014": 20, "FY2013": 30, "FY2012": 23, "FY2011": 40, "FY2010": 53, "FY2009": 276, "FY2008": 13, "FY2007": 31, "FY2006": 36, "FY2005": 30, "FY2004": 27, "FY2003": 28, "FY2002": 38, "FY2001": 22, "FY2000": 351, "FY1999": 441, "FY1998": 459, "FY1997": 836}),
    ("DATA", "Derivative assets", {"FY2024": 7409, "FY2023": 6993, "FY2022": 6360, "FY2021": 4817, "FY2020": 5883, "FY2019": 7130, "FY2018": 12342, "FY2017": 16325, "FY2016": 13212, "FY2015": 2834, "FY2014": 1700, "FY2013": 1361}),
    ("DATA", "Loans and advances to banks", {"FY2024": 143664, "FY2023": 124270, "FY2022": 181081, "FY2021": 28831, "FY2020": 22933, "FY2019": 41744, "FY2018": 31344, "FY2017": 43388, "FY2016": 264808, "FY2015": 47626, "FY2014": 57504, "FY2013": 49764, "FY2012": 50477, "FY2011": 111992, "FY2010": 61920, "FY2009": 84242, "FY2008": 199485, "FY2007": 417903, "FY2006": 475864, "FY2005": 258512, "FY2004": 154433, "FY2003": 68143, "FY2002": 87924, "FY2001": 46168, "FY2000": 74828, "FY1999": 212052, "FY1998": 1357560, "FY1997": 826517, "FY1996": 1198880, "FY1995": 1114060, "FY1994": 1521810}),
    ("DATA", "Loans and advances to customers", {"FY2024": 1667863, "FY2023": 1923638, "FY2022": 2355390, "FY2021": 1248614, "FY2020": 1166560, "FY2019": 1119362, "FY2018": 1074474, "FY2017": 1168605, "FY2016": 996763, "FY2015": 938170, "FY2014": 713024, "FY2013": 657026, "FY2012": 615237, "FY2011": 593602, "FY2010": 508684, "FY2009": 339382, "FY2008": 3199951, "FY2007": 213839, "FY2006": 236786, "FY2005": 191832, "FY2004": 107216, "FY2003": 69712, "FY2002": 62156, "FY2001": 60352, "FY2000": 58328, "FY1999": 49872, "FY1998": 527395, "FY1997": 801489, "FY1996": 988078, "FY1995": 1140272, "FY1994": 1098541}),
    ("DATA", "Revaluation differences on portfolios hedged against interest rate risk", {"FY2024": -249, "FY2023": 634}),
    ("DATA", "Debt and investment securities", {"FY2024": 2410283, "FY2023": 1902435, "FY2022": 2036353, "FY2021": 761764, "FY2020": 723734, "FY2019": 846575, "FY2018": 1253521, "FY2017": 1010102, "FY2016": 830431, "FY2015": 579199, "FY2009": 1149745, "FY2008": 1378440, "FY2007": 1273448, "FY2006": 628049, "FY2005": 41741, "FY2004": 438460, "FY2003": 430420, "FY2002": 326088, "FY2001": 362109, "FY2000": 244428, "FY1999": 60042, "FY1998": 1031034, "FY1997": 1287258, "FY1996": 917973, "FY1995": 1198364, "FY1994": 1294973}),
    ("DATA", "Financial investments (held-to-maturity + available-for-sale combined)", {"FY2014": 738955, "FY2013": 481117, "FY2012": 465049, "FY2011": 404994, "FY2010": 791082}),
    ("DATA", "Shares in group undertakings", {"FY2024": 22114, "FY2023": 22415, "FY2022": 95040, "FY2021": 231352, "FY2020": 232785, "FY2019": 232835, "FY2018": 232883, "FY2017": 232802, "FY2016": 121153, "FY2015": 104853, "FY2014": 104860, "FY2013": 108898, "FY2012": 109269, "FY2011": 124863, "FY2010": 152061, "FY2009": 150305, "FY2008": 153320, "FY2007": 102792, "FY2006": 103327, "FY2005": 106972, "FY2004": 61158, "FY2003": 63337, "FY2002": 133088, "FY2001": 138828, "FY2000": 151271, "FY1999": 145388, "FY1998": 160250, "FY1997": 210098, "FY1996": 218984, "FY1995": 143169, "FY1994": 141954}),
    ("DATA", "Interests in associates / participating interest (equity shares in FY2008)", {"FY2016": 1588, "FY2015": 1594, "FY2014": 1533, "FY2013": 1407, "FY2012": 1432, "FY2011": 1555, "FY2010": 1660, "FY2009": 1660, "FY2008": 1660, "FY2007": 1660, "FY2006": 1660, "FY2005": 2573, "FY2004": 2861, "FY2003": 3016, "FY2002": 3256, "FY2001": 2160, "FY2000": 6848, "FY1999": 6742, "FY1998": 6886, "FY1997": 0}),
    ("DATA", "Goodwill", {"FY2014": 10157, "FY2013": 11247, "FY2012": 12338, "FY2011": 13347}),
    ("DATA", "Intangible assets", {"FY2024": 1908, "FY2023": 3067, "FY2022": 5023, "FY2021": 3469, "FY2020": 4378, "FY2019": 3175, "FY2018": 38271, "FY2017": 44992, "FY2016": 11354, "FY2015": 11952, "FY2010": 8054, "FY2009": 8725, "FY2008": 9396}),
    ("DATA", "Tangible assets", {"FY2024": 7923, "FY2023": 6180, "FY2022": 9284, "FY2021": 1205, "FY2020": 421, "FY2019": 425, "FY2018": 332, "FY2017": 581, "FY2016": 651, "FY2015": 156, "FY2014": 456, "FY2013": 695, "FY2012": 968, "FY2011": 1214, "FY2010": 1287, "FY2009": 2351, "FY2008": 3238, "FY2007": 3329, "FY2006": 213, "FY2005": 201, "FY2004": 238, "FY2003": 316, "FY2002": 632, "FY2001": 987, "FY2000": 1518, "FY1999": 1565, "FY1998": 96475, "FY1997": 111818, "FY1996": 121047, "FY1995": 124263, "FY1994": 40732}),
    ("DATA", "Current income tax assets", {"FY2024": 2617, "FY2023": 0, "FY2022": 0, "FY2021": 887, "FY2020": 0, "FY2019": 2779, "FY2018": 0, "FY2017": 2952, "FY2016": 1559}),
    ("DATA", "Deferred income tax assets", {"FY2024": 11717, "FY2023": 12847, "FY2022": 10247, "FY2021": 2570, "FY2020": 1790, "FY2019": 2288, "FY2018": 4140, "FY2017": 1144, "FY2016": 491, "FY2015": 754, "FY2014": 667, "FY2013": 552, "FY2012": 718, "FY2011": 1205, "FY2010": 1229, "FY2009": 730}),
    ("DATA", "Pension asset", {"FY2024": 2934, "FY2023": 169, "FY2022": 521, "FY2021": 0}),
    ("DATA", "Trade and other receivables / other assets", {"FY2024": 28064, "FY2023": 25347, "FY2022": 27503, "FY2021": 20270, "FY2020": 23739, "FY2019": 23292, "FY2018": 26577, "FY2017": 44388, "FY2016": 23016, "FY2015": 8131, "FY2014": 9500, "FY2013": 6384, "FY2012": 3628, "FY2011": 2129, "FY2010": 2361, "FY2009": 732, "FY2008": 7985, "FY2007": 8330, "FY2006": 1492, "FY2005": 801, "FY2004": 3570, "FY2003": 282, "FY2002": 1849, "FY2001": 1983, "FY2000": 5382, "FY1999": 14799, "FY1998": 518080, "FY1997": 703823, "FY1996": 1019177, "FY1995": 1689920, "FY1994": 1000709}),
    ("DATA", "Prepayments and accrued income", {"FY2012": 4886, "FY2011": 2700, "FY2010": 3433, "FY2009": 1938, "FY2008": 30815, "FY2007": 13545, "FY2006": 11923, "FY2005": 10160, "FY2004": 5094, "FY2003": 3167, "FY2002": 2943, "FY2001": 2536, "FY2000": 3323, "FY1999": 1131, "FY1998": 53264, "FY1997": 94638, "FY1996": 85672, "FY1995": 66530, "FY1994": 41843}),
    ("TOTAL", "Total assets", {"FY2024": 4765408, "FY2023": 4530099, "FY2022": 5291601, "FY2021": 2448463, "FY2020": 2334869, "FY2019": 2332598, "FY2018": 2843244, "FY2017": 2812984, "FY2016": 2265070, "FY2015": 1695300, "FY2014": 1638376, "FY2013": 1318481, "FY2012": 1265919, "FY2011": 1260518, "FY2010": 1535928, "FY2009": 1746330, "FY2008": 4984303, "FY2007": 2048541, "FY2006": 1459370, "FY2005": 982822, "FY2004": 770057, "FY2003": 638421, "FY2002": 617974, "FY2001": 615165, "FY2000": 546277, "FY1999": 492032, "FY1998": 4862584, "FY1997": 5196668, "FY1996": 5463050, "FY1995": 6320640, "FY1994": 5549175, "FY1990": 3435592, "FY1989": 2447908, "FY1988": 2938151, "FY1987": 2774024, "FY1986": 2567340, "FY1985": 2756321, "FY1984": 2846926, "FY1983": 2587575, "FY1982": 2081221, "FY1981": 1803125, "FY1980": 1480469, "FY1979": 1380793, "FY1977": 1196753, "FY1976": 1084419, "FY1975": 1003285, "FY1974": 1003285, "FY1973": 807994}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Deposits by banks", {"FY2024": 61031, "FY2023": 68185, "FY2022": 87141, "FY2021": 1116, "FY2020": 3424, "FY2019": 11543, "FY2018": 41768, "FY2017": 67683, "FY2016": 8292, "FY2015": 981, "FY2014": 1162, "FY2013": 9599, "FY2012": 8329, "FY2011": 115292, "FY2010": 308907, "FY2009": 423711, "FY2008": 3571649, "FY2007": 542219, "FY2006": 665982, "FY2005": 354158, "FY2004": 204249, "FY2003": 134745, "FY2002": 103586, "FY2001": 73183, "FY2000": 29155, "FY1999": 44013, "FY1998": 1083370, "FY1997": 1420128, "FY1996": 1631296, "FY1995": 1825322, "FY1994": 1810514}),
    ("DATA", "Customers' accounts", {"FY2024": 4329605, "FY2023": 3970768, "FY2022": 4654279, "FY2021": 1934968, "FY2020": 1828626, "FY2019": 1836229, "FY2018": 2191216, "FY2017": 2203384, "FY2016": 1727180, "FY2015": 1354614, "FY2014": 1345833, "FY2013": 1031036, "FY2012": 971047, "FY2011": 860577, "FY2010": 914537, "FY2009": 1007214, "FY2008": 1087065, "FY2007": 1220958, "FY2006": 515597, "FY2005": 350629, "FY2004": 343798, "FY2003": 289091, "FY2002": 281069, "FY2001": 308068, "FY2000": 265904, "FY1999": 207526, "FY1998": 1031638, "FY1997": 917014, "FY1996": 894951, "FY1995": 1178248, "FY1994": 1480080}),
    ("DATA", "Revaluation differences on portfolios hedged against interest rate risk", {"FY2024": -481, "FY2023": 2908}),
    ("DATA", "Financial liabilities at fair value through profit or loss", {"FY2020": 0, "FY2019": 9526, "FY2018": 35478, "FY2017": 39056, "FY2016": 38938, "FY2015": 36531}),
    ("DATA", "Derivative liabilities", {"FY2024": 5864, "FY2023": 6365, "FY2022": 5242, "FY2021": 5024, "FY2020": 8636, "FY2019": 6307, "FY2018": 6049, "FY2017": 11220, "FY2016": 161849, "FY2015": 7276, "FY2014": 7818, "FY2013": 2733, "FY2012": 1772, "FY2011": 4575, "FY2010": 9870, "FY2009": 16740}),
    ("DATA", "Current income tax liabilities", {"FY2024": 392, "FY2023": 2712, "FY2022": 89, "FY2021": 0, "FY2020": 1674, "FY2019": 577, "FY2018": 896, "FY2017": 0, "FY2016": 2382, "FY2015": 416, "FY2014": 1067, "FY2013": 0, "FY2012": 319, "FY2011": 1652, "FY2010": 2382, "FY2009": 577}),
    ("DATA", "Deferred income tax liabilities", {"FY2024": 492, "FY2023": 69, "FY2022": 183, "FY2021": 0, "FY2016": 1052}),
    ("DATA", "Other liabilities (includes accruals and deferred income, combined per FY2013-2014 own presentation)", {"FY2024": 70263, "FY2023": 72669, "FY2022": 66326, "FY2021": 35454, "FY2020": 44140, "FY2019": 48909, "FY2018": 60018, "FY2017": 68368, "FY2016": 43907, "FY2015": 26263, "FY2014": 25151, "FY2013": 21187, "FY2012": 22069, "FY2011": 21544, "FY2010": 20737, "FY2009": 19088, "FY2008": 47461, "FY2007": 31455, "FY2006": 23533, "FY2005": 20544, "FY2004": 15009, "FY2003": 7843, "FY2002": 14399, "FY2001": 15887, "FY2000": 11783, "FY1999": 19543, "FY1998": 2513212, "FY1997": 2575178, "FY1996": 1841061, "FY1995": 2339217, "FY1994": 1314470}),
    ("DATA", "Provisions for liabilities", {"FY2024": 1021, "FY2023": 1026, "FY2022": 1079, "FY2021": 8391, "FY2020": 10763, "FY2019": 1696, "FY2018": 2365, "FY2017": 2167, "FY2016": 362, "FY2015": 1482, "FY1996": 45956, "FY1995": 42999, "FY1994": 57328}),
    ("TOTAL", "Total liabilities", {"FY2024": 4468187, "FY2023": 4124702, "FY2022": 4814339, "FY2021": 1984953, "FY2020": 1897263, "FY2019": 1914210, "FY2018": 2337790, "FY2017": 2392078, "FY2016": 1981580, "FY2015": 1427563, "FY2014": 1381031, "FY2013": 1064555, "FY2007": 1794632, "FY2006": 1203112, "FY2005": 725331, "FY2004": 563056, "FY2003": 431679, "FY2002": 399054, "FY2001": 397138, "FY1996": 5167711, "FY1995": 6121072, "FY1994": 5313551}),
    ("SECTION", "Equity", {}),
    ("DATA", "Share capital", {"FY2024": 265750, "FY2023": 328266, "FY2022": 328266, "FY2021": 328266, "FY2020": 328266, "FY2019": 328266, "FY2018": 328266, "FY2017": 303266, "FY2016": 160067, "FY2015": 143800, "FY2014": 143800, "FY2013": 143800, "FY2012": 143800, "FY2011": 143800, "FY2010": 143800, "FY2009": 143800, "FY2008": 143800, "FY2002": 143800, "FY2001": 143800, "FY1996": 143800, "FY1995": 143800, "FY1994": 143800, "FY1990": 143800, "FY1989": 30000, "FY1988": 30000, "FY1987": 30000, "FY1986": 30000, "FY1985": 30000, "FY1984": 20000, "FY1983": 20000, "FY1982": 20000, "FY1981": 13000, "FY1980": 13000, "FY1979": 13000, "FY1977": 13000, "FY1976": 13000, "FY1975": 13000, "FY1974": 13000, "FY1973": 13000}),
    ("DATA", "Share premium", {"FY2024": 0, "FY2023": 45500, "FY2022": 45500, "FY2021": 45500, "FY2020": 45500, "FY2019": 45500, "FY2018": 45500, "FY2017": 45500, "FY2016": 45500, "FY2015": 45500, "FY2014": 45500, "FY2013": 45500, "FY2012": 45500, "FY2011": 45500, "FY2010": 45500, "FY2009": 45500, "FY2008": 45500, "FY2002": 45500, "FY2001": 45500, "FY1996": 45500, "FY1995": 45500, "FY1994": 45500, "FY1990": 45500, "FY1989": 45500, "FY1988": 45500, "FY1987": 45500, "FY1986": 45500, "FY1985": 45500, "FY1984": 27500, "FY1983": 27500, "FY1982": 27500, "FY1981": 24500, "FY1980": 24500, "FY1979": 24500, "FY1977": 24500, "FY1976": 24500, "FY1975": 24500, "FY1974": 24500, "FY1973": 24500}),
    ("DATA", "Share-based payment reserves (not separately disclosed in FY2013's own accounts - see FY2013 RESTATEMENT NOTE; embedded within Retained earnings for FY2013)", {"FY2024": 5214, "FY2023": 5082, "FY2022": 4735, "FY2021": 2542, "FY2020": 2502, "FY2019": 2383, "FY2018": 2264, "FY2017": 2145, "FY2016": 1944, "FY2015": 1690, "FY2014": 1732}),
    ("DATA", "Undistributable reserves", {"FY2022": 42500, "FY2021": 42500, "FY2020": 42500, "FY2019": 42500, "FY2018": 42500, "FY2017": 42500, "FY2016": 42500, "FY2015": 42500, "FY2014": 42500, "FY2013": 42500, "FY2012": 42500, "FY2011": 42500, "FY2010": 42500, "FY2009": 42500, "FY2008": 42500, "FY2007": 42500, "FY2006": 42500, "FY2005": 42500}),
    ("DATA", "OCI reserves", {"FY2024": -13632, "FY2023": -19227, "FY2022": -30856, "FY2021": 3083, "FY2020": 7670, "FY2019": 5727, "FY2018": 2215, "FY2017": 4495, "FY2016": 3760, "FY2015": 2974, "FY2014": 3480, "FY2013": 1001, "FY2012": 4974, "FY2011": 2577, "FY2010": 136, "FY2009": -981, "FY2008": 0, "FY1996": 103031, "FY1994": 1702}),
    ("DATA", "Revaluation reserve (pre-IFRS presentation)", {"FY1990": 12704, "FY1989": 12704}),
    ("DATA", "Retained earnings", {"FY2024": 39889, "FY2023": 45776, "FY2022": 87117, "FY2021": 41619, "FY2020": 11168, "FY2019": -5988, "FY2018": 84709, "FY2017": 23000, "FY2016": 29719, "FY2015": 31273, "FY2014": 20333, "FY2013": 21125, "FY2012": 25609, "FY2011": 22501, "FY2010": 47559, "FY2009": 48181, "FY2008": 46328, "FY2007": 22109, "FY2006": 25691, "FY2005": 25691, "FY2004": 17701, "FY2003": 17442, "FY2002": 29620, "FY2001": 28727, "FY1996": 3008, "FY1995": 10268, "FY1994": 44622, "FY1990": 35266, "FY1989": 25065, "FY1988": 28817, "FY1987": 23087, "FY1986": 20756, "FY1985": 16281, "FY1984": 15884, "FY1983": 22354, "FY1982": 20524, "FY1981": 16830, "FY1980": 13034, "FY1979": 6906, "FY1977": 5427, "FY1976": 4680, "FY1975": 4062, "FY1974": 3255, "FY1973": 1850}),
    ("TOTAL", "Equity attributable to owners of the Company", {"FY2024": 297221, "FY2023": 405397, "FY2022": 477262, "FY2021": 463510, "FY2020": 437606, "FY2019": 418388, "FY2018": 505454, "FY2017": 420906, "FY2016": 283490, "FY2015": 267737, "FY2014": 257345, "FY2013": 253926, "FY2012": 262383, "FY2011": 256878, "FY2010": 279495, "FY2009": 279000, "FY2008": 278128, "FY2007": 253909, "FY2006": 257491, "FY2005": 257491, "FY2004": 207001, "FY2003": 206742, "FY2002": 218920, "FY2001": 218027, "FY1996": 295339, "FY1995": 199568, "FY1994": 235624, "FY1990": 237270, "FY1989": 113269, "FY1988": 104317, "FY1987": 98587, "FY1986": 96256, "FY1985": 91781, "FY1984": 63384, "FY1983": 69854, "FY1982": 68024, "FY1981": 54330, "FY1980": 50534, "FY1979": 44406, "FY1977": 42927, "FY1976": 42180, "FY1975": 41562, "FY1974": 40785, "FY1973": 39350}),
    ("TOTAL", "Total liabilities and equity", {"FY2024": 4765408, "FY2023": 4530099, "FY2022": 5291601, "FY2021": 2448463, "FY2020": 2334869, "FY2019": 2332598, "FY2018": 2843244, "FY2017": 2812984, "FY2016": 2265070, "FY2015": 1695300, "FY2014": 1638376, "FY2013": 1318481, "FY2012": 1265919, "FY2011": 1260518, "FY2010": 1535928, "FY2009": 1746330, "FY2008": 4984303, "FY2007": 2048541, "FY2006": 1459370, "FY2005": 982822, "FY2004": 770057, "FY2003": 638421, "FY2002": 617974, "FY2001": 615165, "FY1990": 3435592, "FY1989": 2447908, "FY1988": 2938151, "FY1987": 2774024, "FY1986": 2567340, "FY1985": 2756321}),
]
bw.add_balance_sheet_sheet(
    title="Union Bancaire Privée (UK) Limited — Balance Sheet",
    subtitle="Statement of Financial Position, Company-only basis, £'000. Blank cells indicate a line not presented that year; 0 indicates a line disclosed as nil.",
    rows=balance_sheet_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=82,
    source_height=340,
    unit_suffix=" (£'000)",
    years=YEARS,
)

income_statement_rows = [
    ("SECTION", "Interest", {}),
    ("DATA", "Interest receivable on debt securities (pre-2009 presentation)", {"FY2008": 56216, "FY2007": 42576, "FY2006": 24495, "FY2005": 14197, "FY2004": 17429, "FY2003": 16046, "FY1996": 5646, "FY1995": 7719, "FY1994": 9961}),
    ("DATA", "Other interest receivable (pre-2009 presentation)", {"FY2008": 92560, "FY2007": 25423, "FY2006": 24100, "FY2005": 19392, "FY2004": 7709, "FY2003": 4668, "FY1996": 317667, "FY1995": 286353, "FY1994": 257414}),
    ("DATA", "Interest income", {"FY2024": 238931, "FY2023": 227011, "FY2022": 78433, "FY2021": 29774, "FY2020": 33512, "FY2019": 34595, "FY2018": 35545, "FY2017": 37695, "FY2016": 35672, "FY2015": 31702, "FY2014": 28597, "FY2013": 25615, "FY2012": 22694, "FY2011": 30749, "FY2010": 30317, "FY2009": 51349, "FY2007": 67999, "FY2006": 48595, "FY2005": 33589, "FY2004": 25138, "FY2003": 20714, "FY2002": 20603, "FY2001": 26029, "FY2000": 19100, "FY1999": 39630, "FY1997": 266299, "FY1996": 323313, "FY1995": 294072, "FY1994": 267375}),
    ("DATA", "Interest income at FVOCI (separate line FY2018-2019 only; folded into Interest income from FY2020)", {"FY2019": 12732, "FY2018": 15748}),
    ("DATA", "Interest expense", {"FY2024": -149685, "FY2023": -113785, "FY2022": -20695, "FY2021": -4372, "FY2020": -7564, "FY2019": -14255, "FY2018": -11655, "FY2017": -9845, "FY2016": -11524, "FY2015": -8101, "FY2014": -8252, "FY2013": -5597, "FY2012": -6314, "FY2011": -14170, "FY2010": -12890, "FY2009": -29563, "FY2008": -128860, "FY2007": -54241, "FY2006": -37034, "FY2005": -22079, "FY2004": -13310, "FY2003": -10116, "FY2002": -11012, "FY2001": -17525, "FY2000": -12296, "FY1999": -32679, "FY1997": -259168, "FY1996": -313204, "FY1995": -273469, "FY1994": -239980}),
    ("TOTAL", "Net interest income", {"FY2024": 89246, "FY2023": 113226, "FY2022": 57738, "FY2021": 25402, "FY2020": 25948, "FY2019": 33072, "FY2018": 39638, "FY2017": 27850, "FY2016": 24148, "FY2015": 23601, "FY2014": 20345, "FY2013": 20018, "FY2012": 16380, "FY2011": 16579, "FY2010": 17427, "FY2009": 21786, "FY2008": 19916, "FY2007": 13758, "FY2006": 11561, "FY2005": 11510, "FY2004": 11828, "FY2003": 10598, "FY2002": 9591, "FY2001": 8504, "FY2000": 6804, "FY1999": 6951, "FY1997": 7131, "FY1996": 10109, "FY1995": 20603, "FY1994": 27395}),
    ("SECTION", "Fees and commissions", {}),
    ("DATA", "Fee and commission income", {"FY2024": 53735, "FY2023": 53948, "FY2022": 45677, "FY2021": 42430, "FY2020": 47800, "FY2019": 50995, "FY2018": 51348, "FY2017": 35116, "FY2016": 31783, "FY2015": 30072, "FY2014": 24282, "FY2013": 23710, "FY2012": 22208, "FY2011": 22792, "FY2010": 20350, "FY2009": 20819, "FY2008": 20166, "FY2007": 15844, "FY2006": 13498, "FY2005": 9478, "FY2004": 7993, "FY2003": 5554, "FY2002": 3499, "FY2001": 3429, "FY2000": 2478, "FY1999": 4584, "FY1997": 64362, "FY1996": 67241, "FY1995": 60094, "FY1994": 67761}),
    ("DATA", "Fee and commission expense", {"FY2024": -1252, "FY2023": -1745, "FY2022": -988, "FY2021": -1054, "FY2020": -245, "FY2019": -1004, "FY2018": -1062, "FY2017": -1796, "FY2016": -1347, "FY2015": -1336, "FY2014": -1682, "FY2013": -1997, "FY2012": -1575, "FY2011": -1721, "FY2010": -304, "FY2009": -311, "FY2008": -434, "FY2007": -220, "FY2006": -42, "FY2005": -67, "FY2004": -67}),
    ("DATA", "Fee and commission expense (older accounts; not separately presented in FY2000)", {"FY1999": -2527, "FY1997": 0}),
    ("TOTAL", "Net fee and commission income", {"FY2024": 52483, "FY2023": 52203, "FY2022": 44689, "FY2021": 41376, "FY2020": 47555, "FY2019": 49991, "FY2018": 50286, "FY2017": 33320, "FY2016": 30436, "FY2015": 28736, "FY2014": 22600, "FY2013": 21713, "FY2012": 20633, "FY2011": 21071, "FY2010": 20046, "FY2009": 20508, "FY2008": 19732, "FY2007": 15624, "FY2006": 13456, "FY2005": 9411, "FY2004": 7926, "FY2003": 5554, "FY2000": 2478, "FY1999": 2057, "FY1997": 64362}),
    ("SECTION", "Other operating income", {}),
    ("DATA", "Gain/(loss) on financial instruments at fair value", {"FY2024": -11818, "FY2023": -1138, "FY2022": 6746, "FY2021": 4083, "FY2020": -2599, "FY2019": -2000, "FY2018": -3763, "FY2017": 787}),
    ("DATA", "Net gain on available-for-sale financial assets (FY2015-2016 only; folded into Gain/(loss) on FI at FV convention from FY2017)", {"FY2016": 3157, "FY2015": 25}),
    ("DATA", "Net gain/(loss) from trading", {"FY2016": 1365, "FY2015": 615, "FY2014": 1134, "FY2013": 1078, "FY2012": 1922, "FY2011": 3601, "FY2010": 2708, "FY2009": -2934, "FY2002": 431, "FY2001": 122}),
    ("DATA", "Other income/(expense)", {"FY2024": 88, "FY2023": 358, "FY2022": 1, "FY2021": 399, "FY2020": 57, "FY2019": -1422, "FY2018": -1250, "FY2017": -308, "FY2016": -313, "FY2015": -329}),
    ("DATA", "Other operating income (FY2013-2014 only, unitemised)", {"FY2014": 5036, "FY2013": 40306}),
    ("DATA", "Gains on sales of investments", {"FY2024": 393, "FY2023": 0, "FY2017": 164}),
    ("DATA", "Dividend income", {"FY2024": 12, "FY2023": 2383, "FY2022": 0, "FY2021": 25000, "FY2020": 18502, "FY2019": 1308, "FY2018": 64809, "FY2016": 2, "FY2015": 5003, "FY2002": 2396, "FY2001": 1561}),
    ("DATA", "Dealing profits (pre-2009 presentation)", {"FY2008": 1281, "FY2007": 914, "FY2006": 571, "FY2005": 714, "FY2004": 933, "FY2003": 408, "FY1996": 15895, "FY1995": 21062, "FY1994": 32353}),
    ("DATA", "Other operating income (FY2009-2012)", {"FY2012": 9108, "FY2011": 27141, "FY2010": 653, "FY2009": 245}),
    ("DATA", "Other pre-2008 operating income lines", {"FY2007": 355, "FY2006": 311, "FY2005": 5173, "FY2004": 340, "FY2003": 155, "FY1996": 8215, "FY1995": 2257, "FY1994": 3298}),
    ("DATA", "Dividend income (pre-2009 presentation)", {"FY2008": 22121, "FY2000": 3784, "FY1999": 15863, "FY1997": 28449, "FY1996": 41055, "FY1995": 4350, "FY1994": 13302}),
    ("DATA", "Other operating income (pre-2008 presentation)", {"FY2000": 89, "FY1999": 1299, "FY1997": 2393}),
    ("TOTAL", "Total operating income", {"FY2024": 130404, "FY2023": 167032, "FY2022": 109174, "FY2021": 96260, "FY2020": 89463, "FY2019": 80949, "FY2018": 149720, "FY2017": 61813, "FY2016": 58795, "FY2015": 57651, "FY2014": 49115, "FY2013": 83113, "FY2012": 48043, "FY2011": 68392, "FY2010": 40834, "FY2009": 39605, "FY2008": 63050, "FY2007": 30651, "FY2006": 25899, "FY2005": 26818, "FY2004": 21017, "FY2003": 16715, "FY2002": 15917, "FY2001": 13749, "FY2000": 13155, "FY1999": 29574, "FY1997": 114488, "FY1996": 142515, "FY1995": 108366, "FY1994": 144109}),
    ("SECTION", "Operating expenses", {}),
    ("DATA", "Administrative expenses", {"FY2024": -122303, "FY2023": -120040, "FY2022": -84000, "FY2021": -57258, "FY2020": -65178, "FY2019": -76615, "FY2018": -90695, "FY2017": -71319, "FY2016": -55448, "FY2015": -44104, "FY2014": -41370, "FY2013": -34278, "FY2012": -31414, "FY2011": -36096, "FY2010": -34381, "FY2009": -33262, "FY2008": -31711, "FY2007": -25203, "FY2006": -20153, "FY2005": -14993, "FY2004": -13188, "FY2003": -11644, "FY2002": -8360, "FY2001": -8012, "FY2000": -7083, "FY1999": -6537, "FY1997": -108508, "FY1996": -104428, "FY1995": -96034, "FY1994": -92595}),
    ("DATA", "Amortisation", {"FY2024": -1219, "FY2023": -1896, "FY2022": -1430, "FY2021": -1649, "FY2020": -708, "FY2019": -589, "FY2018": -228, "FY2017": -826, "FY2016": -268, "FY2015": -27, "FY2014": -1091, "FY2013": -1091, "FY2012": -1088, "FY2011": -918, "FY2010": -671, "FY2009": -671, "FY2008": -671, "FY2007": -103, "FY2006": -80, "FY2005": -89, "FY2004": -109, "FY2003": -351, "FY2002": -392, "FY2001": -413}),
    ("DATA", "Amortisation (older accounts)", {"FY2000": -397, "FY1999": -1059, "FY1997": -8901}),
    ("DATA", "Depreciation", {"FY2024": -2335, "FY2023": -2369, "FY2022": -719, "FY2021": -248, "FY2020": -171, "FY2019": -254, "FY2018": -260, "FY2017": -283, "FY2016": -284, "FY2015": -217, "FY2014": -246, "FY2013": -378, "FY2012": -300, "FY2011": -639, "FY2010": -1106, "FY2009": -1249, "FY2008": -1128}),
    ("DATA", "(Increase)/decrease in expected credit loss provisions", {"FY2024": 5014, "FY2023": -2320, "FY2022": -639, "FY2021": -4288, "FY2020": -1347}),
    ("DATA", "Other provisions", {"FY2024": -352, "FY2023": -673, "FY2022": -1233, "FY2021": -1158, "FY2020": -9714, "FY2017": 680, "FY2016": -1588, "FY2007": -3, "FY2006": -8, "FY2005": -80, "FY2004": 0, "FY2003": 24, "FY2002": -66, "FY2001": 1368}),
    ("DATA", "Other provisions / impairment (pre-2001 presentation)", {"FY2000": -13, "FY1999": -25244, "FY1997": -10695}),
    ("DATA", "Amounts written off fixed asset investments (pre-2001 presentation)", {"FY2000": 25990, "FY1999": -25274}),
    ("DATA", "Impairment losses and other provisions (combined line, FY2018-2019 only)", {"FY2019": -1503, "FY2018": 608}),
    ("DATA", "Impairment of goodwill", {"FY2019": -37190}),
    ("DATA", "Other operating expenses (FY2015-2016 only, unitemised)", {"FY2016": 358, "FY2015": -198}),
    ("DATA", "Impairment of financial assets", {"FY2014": -382, "FY2013": -261, "FY2012": -739, "FY2011": -709, "FY2010": -741, "FY2009": -125, "FY2008": -949}),
    ("DATA", "Impairment of shares in group undertakings (FY2010-2012)", {"FY2012": -9159, "FY2011": -27019, "FY2010": -3212}),
    ("DATA", "Impairment of shares in participating interests (FY2011-2012)", {"FY2012": -123, "FY2011": -105}),
    ("DATA", "Loss on sale of group undertakings (FY2012)", {"FY2012": -449}),
    ("DATA", "Impairment of shares in group undertakings (FY2013 only; nil in FY2013, was £(9,159)k in FY2012)", {"FY2013": 0}),
    ("DATA", "Impairment of shares in participating interests (FY2013 only)", {"FY2013": -25}),
    ("DATA", "Loss on sale of group undertakings (FY2013 only)", {"FY2013": -1}),
    # FY2008-FY2012 filings printed the component expense lines and profit
    # before tax, but no subtotal. These five values are the exact sums of
    # their printed expense lines, retained so cost-to-income remains
    # comparable and never looks like a directly printed subtotal.
    ("TOTAL", "Total operating expenses (derived from reported lines for FY2008-FY2012)", {"FY2024": -121195, "FY2023": -127298, "FY2022": -88021, "FY2021": -64601, "FY2020": -77118, "FY2019": -116151, "FY2018": -90575, "FY2017": -71748, "FY2016": -57230, "FY2015": -46521, "FY2014": -43089, "FY2013": -36034, "FY2012": -43272, "FY2011": -65381, "FY2010": -40111, "FY2009": -35307, "FY2008": -34459, "FY2007": -25309, "FY2006": -20241, "FY2005": -15162, "FY2004": -13297, "FY2003": -11971, "FY2002": -8818, "FY2001": -7057, "FY2000": -7493, "FY1999": -32840, "FY1997": -128004}),
    ("TOTAL", "Profit before income tax", {"FY2024": 9209, "FY2023": 39734, "FY2022": 21153, "FY2021": 31659, "FY2020": 12345, "FY2019": -35202, "FY2018": 59145, "FY2017": -9935, "FY2016": 1565, "FY2015": 11130, "FY2014": 6026, "FY2013": 47079, "FY2012": 4771, "FY2011": 3011, "FY2010": 723, "FY2009": 4298, "FY2008": 28591, "FY2007": 5342, "FY2006": 6167, "FY2005": 11689, "FY2004": 7560, "FY2003": -11350, "FY2002": 7099, "FY2001": 6692, "FY2000": 31652, "FY1999": 14062, "FY1997": -14321, "FY1996": -6469, "FY1995": -8802, "FY1994": 37793}),
    ("DATA", "Income tax (expense)/credit", {"FY2024": -555, "FY2023": -4495, "FY2022": -3389, "FY2021": -1208, "FY2020": 4811, "FY2019": 1207, "FY2018": 3065, "FY2017": 3216, "FY2016": -119, "FY2015": -1060, "FY2014": -323, "FY2013": -2063, "FY2012": -1663, "FY2011": -1155, "FY2010": -1345, "FY2009": -2055, "FY2008": -4372, "FY2007": -1691, "FY2006": -1900, "FY2005": -3699, "FY2004": -2301, "FY2003": -828, "FY2002": 183, "FY2001": -294, "FY2000": -1223, "FY1999": -6003, "FY1997": 12359, "FY1996": 13305, "FY1995": 2713, "FY1994": -9445}),
    ("TOTAL", "Profit for the year", {"FY2024": 8654, "FY2023": 35239, "FY2022": 17764, "FY2021": 30451, "FY2020": 17156, "FY2019": -33995, "FY2018": 62210, "FY2017": -6719, "FY2016": 1446, "FY2015": 10070, "FY2014": 5703, "FY2013": 45016, "FY2012": 3108, "FY2011": 1856, "FY2010": -622, "FY2009": 2243, "FY2008": 24219, "FY2007": 3651, "FY2006": 4267, "FY2005": 7990, "FY2004": 5259, "FY2003": -12178, "FY2002": 7282, "FY2001": 6398, "FY2000": 30429, "FY1999": 8059, "FY1997": -1962, "FY1996": 6836, "FY1995": -6089, "FY1994": 28348, "FY1993": 23332, "FY1992": 26797, "FY1991": 21618, "FY1990": 28076, "FY1989": 9468, "FY1988": 10230, "FY1987": 7331, "FY1986": 8475, "FY1985": 397, "FY1984": 2546, "FY1983": 1830, "FY1982": 3694, "FY1981": 3796, "FY1980": 6728, "FY1979": 1599, "FY1977": 2547, "FY1976": 2398, "FY1975": 4877, "FY1974": 4085, "FY1973": 3262}),
    ("SECTION", "Other comprehensive income", {}),
    ("DATA", "Gains/(losses) on revaluation of AFS/FVOCI investments taken to equity", {"FY2020": 7935, "FY2019": 4256, "FY2018": -6537, "FY2017": 564, "FY2016": -1555, "FY2015": -1142, "FY2014": 3124, "FY2013": -4982}),
    ("DATA", "Tax on AFS/FVOCI investments taken to equity", {"FY2020": -1673, "FY2019": -469, "FY2018": 739, "FY2017": -169, "FY2016": -816, "FY2015": 611, "FY2014": -679, "FY2013": 1204}),
    ("DATA", "Transfer to profit or loss on disposal of AFS/FVOCI investments", {"FY2020": -4319, "FY2019": -275, "FY2018": 3846, "FY2017": 340, "FY2016": 3157, "FY2015": 25, "FY2014": 34, "FY2013": -195}),
    ("DATA", "Other comprehensive income for the year, net of tax", {"FY2024": 5151, "FY2023": 12549, "FY2022": -14588, "FY2021": -4587, "FY2020": 1943, "FY2019": 3512, "FY2018": -1952, "FY2017": 735, "FY2016": 786, "FY2015": -506}),
    ("TOTAL", "Total comprehensive income for the year, net of tax", {"FY2024": 13805, "FY2023": 47788, "FY2022": 3176, "FY2021": 25864, "FY2020": 19099, "FY2019": -30483, "FY2018": 60258, "FY2017": -5984, "FY2016": 2232, "FY2015": 9564, "FY2014": 8182, "FY2013": 41043, "FY2002": 7282, "FY2001": 6398, "FY2000": 18585, "FY1999": -13414, "FY1997": -10991}),
]
bw.add_income_statement_sheet(
    title="Union Bancaire Privée (UK) Limited — Profit & Loss",
    subtitle="Statement of Profit and Loss / Statement of Comprehensive Income, Company-only basis, £'000. All results derived from continuing operations, entirely attributable to owners of the Company.",
    rows=income_statement_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=82,
    source_height=340,
    unit_suffix=" (£'000)",
    years=YEARS,
)

equity_headers = ["Share capital", "Share premium", "Share-based payment reserve", "Undistributable reserves", "OCI reserves", "Retained earnings", "Total equity"]
equity_rows = [
    ("TOTAL", "At 31 March 1997 (Balance Sheet closing reserves; no separate SOCIE presented)", (143800, 45500, None, None, 94002, 1046, 284348)),
    ("TOTAL", "At 28 February 1998 (Balance Sheet closing reserves; no separate SOCIE presented)", (143800, 45500, None, None, 44359, 705, 234364)),
    ("TOTAL", "At 31 December 1998 (Balance Sheet closing reserves; no separate SOCIE presented)", (143800, 45500, None, None, 35363, -3713, 220950)),
    ("TOTAL", "At 31 December 1999 (Balance Sheet closing reserves; no separate SOCIE presented)", (143800, 45500, None, None, 22306, 27829, 239435)),
    ("TOTAL", "At 1 January 2013", (143800, 45500, None, 42500, 4974, 25609, 262383)),
    ("DATA", "Profit for the year (FY2013)", (None, None, None, None, None, 45016, 45016)),
    ("DATA", "Released on disposal of AFS investments to profit and loss (FY2013)", (None, None, None, None, -195, None, -195)),
    ("DATA", "Decrease in fair value on revaluation of AFS investments (FY2013)", (None, None, None, None, -4982, None, -4982)),
    ("DATA", "Dividends paid (FY2013)", (None, None, None, None, None, -49500, -49500)),
    ("DATA", "Tax on fair value movement of AFS investment (FY2013)", (None, None, None, None, 1204, None, 1204)),
    ("TOTAL", "At 31 December 2013", (143800, 45500, None, 42500, 1001, 21125, 253926)),
    ("DATA", "Reclassification (per FY2014 accounts' own FY2013 restated comparative - see FY2013 RESTATEMENT NOTE)", (None, None, 1494, None, None, -1495, -1)),
    ("TOTAL", "At 1 January 2014", (143800, 45500, 1494, 42500, 1001, 19630, 253925)),
    ("DATA", "Profit for the year (FY2014)", (None, None, None, None, None, 5703, 5703)),
    ("DATA", "Increase in fair value on revaluation of AFS investments (FY2014)", (None, None, None, None, 3124, None, 3124)),
    ("DATA", "Released on disposal of AFS investments to profit and loss (FY2014)", (None, None, None, None, 34, None, 34)),
    ("DATA", "Equity settled payments (FY2014)", (None, None, 238, None, None, None, 238)),
    ("DATA", "Tax on fair value movement of AFS investment (FY2014)", (None, None, None, None, -679, None, -679)),
    ("DATA", "Dividends paid (FY2014)", (None, None, None, None, None, -5000, -5000)),
    ("TOTAL", "At 31 December 2014", (143800, 45500, 1732, 42500, 3480, 20333, 257345)),
    ("DATA", "Restatement (per FY2015 accounts' own 1 Jan 2015 opening balance - see FY2014 RESTATEMENT NOTE)", (None, None, None, None, None, 870, 870)),
    ("TOTAL", "At 1 January 2015 (restated)", (143800, 45500, 1732, 42500, 3480, 21203, 258215)),
    ("DATA", "Profit for the year (FY2015)", (None, None, None, None, None, 10070, 10070)),
    ("DATA", "Equity settled payments (FY2015)", (None, None, -42, None, None, None, -42)),
    ("DATA", "Released on disposal of AFS investments to profit and loss (FY2015)", (None, None, None, None, 25, None, 25)),
    ("DATA", "Decrease in fair value on revaluation of AFS investments (FY2015)", (None, None, None, None, -1142, None, -1142)),
    ("DATA", "Tax on fair value movement of AFS investment (FY2015)", (None, None, None, None, 611, None, 611)),
    ("TOTAL", "At 31 December 2015", (143800, 45500, 1690, 42500, 2974, 31273, 267737)),
    ("DATA", "Profit for the year (FY2016)", (None, None, None, None, None, 1446, 1446)),
    ("DATA", "Increase in share capital (FY2016)", (16267, None, None, None, None, None, 16267)),
    ("DATA", "Equity settled payments (FY2016)", (None, None, 254, None, None, None, 254)),
    ("DATA", "Released on disposal of AFS investments to profit and loss (FY2016)", (None, None, None, None, 3157, None, 3157)),
    ("DATA", "Decrease in fair value on revaluation of AFS investments (FY2016)", (None, None, None, None, -1555, None, -1555)),
    ("DATA", "Dividends paid (FY2016)", (None, None, None, None, None, -3000, -3000)),
    ("DATA", "Tax on fair value movement of AFS investment (FY2016)", (None, None, None, None, -816, None, -816)),
    ("TOTAL", "At 31 December 2016", (160067, 45500, 1944, 42500, 3760, 29719, 283490)),
    ("DATA", "Loss for the year (FY2017)", (None, None, None, None, None, -6719, -6719)),
    ("DATA", "Released on disposal of AFS investments to profit and loss (FY2017)", (None, None, None, None, 340, None, 340)),
    ("DATA", "Increase in fair value on revaluation of AFS investments (FY2017)", (None, None, None, None, 564, None, 564)),
    ("DATA", "Tax on fair value movement of AFS investment (FY2017)", (None, None, None, None, -169, None, -169)),
    ("DATA", "Capital increase (FY2017)", (143199, None, None, None, None, None, 143199)),
    ("DATA", "Equity settled payments (FY2017)", (None, None, 201, None, None, None, 201)),
    ("TOTAL", "At 31 December 2017", (303266, 45500, 2145, 42500, 4495, 23000, 420906)),
    ("DATA", "IFRS 9 transition: impairments adjustment (1 Jan 2018, Note 4)", (None, None, None, None, None, -1139, -1139)),
    ("DATA", "IFRS 9 transition: tax effect (1 Jan 2018, Note 4)", (None, None, None, None, None, 310, 310)),
    ("DATA", "IFRS 9 transition: transfer from OCI reserves to retained earnings (1 Jan 2018, Note 4)", (None, None, None, None, -328, 328, 0)),
    ("TOTAL", "At 1 January 2018 (restated under IFRS 9 - see IFRS 9 TRANSITION NOTE)", (303266, 45500, 2145, 42500, 4167, 22499, 420077)),
    ("DATA", "Profit for the year (FY2018)", (None, None, None, None, None, 62210, 62210)),
    ("DATA", "Increase on disposal of FVOCI investments to profit and loss (FY2018)", (None, None, None, None, 3846, None, 3846)),
    ("DATA", "Decrease in fair value on revaluation of FVOCI investments (FY2018)", (None, None, None, None, -6537, None, -6537)),
    ("DATA", "Tax on fair value movement of FVOCI investment (FY2018)", (None, None, None, None, 739, None, 739)),
    ("DATA", "Capital increase (FY2018)", (25000, None, None, None, None, None, 25000)),
    ("DATA", "Equity settled payments (FY2018)", (None, None, 119, None, None, None, 119)),
    ("TOTAL", "At 31 December 2018", (328266, 45500, 2264, 42500, 2215, 84709, 505454)),
    ("DATA", "Total comprehensive income/(expense) (FY2019)", (None, None, None, None, 3512, -33995, -30483)),
    ("DATA", "Equity settled payments (FY2019)", (None, None, 119, None, None, None, 119)),
    ("DATA", "Dividends paid (FY2019)", (None, None, None, None, None, -56702, -56702)),
    ("TOTAL", "At 31 December 2019", (328266, 45500, 2383, 42500, 5727, -5988, 418388)),
    ("DATA", "Total comprehensive income/(expense) (FY2020)", (None, None, None, None, 1943, 17156, 19099)),
    ("DATA", "Equity settled payments (FY2020)", (None, None, 119, None, None, None, 119)),
    ("TOTAL", "At 1 January 2021", (328266, 45500, 2502, 42500, 7670, 11168, 437606)),
    ("DATA", "Total comprehensive income/(expense) (FY2021)", (None, None, None, None, -4587, 30451, 25864)),
    ("DATA", "Equity settled payments (FY2021)", (None, None, 40, None, None, None, 40)),
    ("TOTAL", "At 31 December 2021", (328266, 45500, 2542, 42500, 3083, 41619, 463510)),
    ("DATA", "Total comprehensive income/(expense) (FY2022)", (None, None, None, None, -14588, 17764, 3176)),
    ("DATA", "Transfer of net assets from SGKHCIL (Note 30, FY2022)", (None, None, 1913, None, -18670, 22529, 5772)),
    ("DATA", "Transfer of net assets from SGKHGL (Note 30, FY2022)", (None, None, None, None, -681, 5205, 4524)),
    ("DATA", "Equity settled payments (FY2022)", (None, None, 280, None, None, None, 280)),
    ("TOTAL", "At 31 December 2022", (328266, 45500, 4735, 42500, -30856, 87117, 477262)),
    ("DATA", "Total comprehensive income/(expense) (FY2023)", (None, None, None, None, 12549, 35239, 47788)),
    ("DATA", "Transfer of undistributable reserves to retained earnings (Note 24, FY2023)", (None, None, None, -42500, None, 42500, 0)),
    ("DATA", "Transfer from reserves (FY2023)", (None, None, None, None, -920, 920, 0)),
    ("DATA", "Equity settled payments (FY2023)", (None, None, 347, None, None, None, 347)),
    ("DATA", "Dividends paid (FY2023)", (None, None, None, None, None, -120000, -120000)),
    ("TOTAL", "At 31 December 2023", (328266, 45500, 5082, 0, -19227, 45776, 405397)),
    ("DATA", "Total comprehensive income/(expense) (FY2024)", (None, None, None, None, 5151, 8654, 13805)),
    ("DATA", "Transfer from reserves (FY2024)", (None, None, None, None, 444, -444, 0)),
    ("DATA", "Equity settled payments (FY2024)", (None, None, 132, None, None, None, 132)),
    ("DATA", "Capital repayment (FY2024)", (-62516, -27484, None, None, None, None, -90000)),
    ("DATA", "Cancellation of share premium (FY2024)", (None, -18016, None, None, None, 18016, 0)),
    ("DATA", "Dividends paid (FY2024)", (None, None, None, None, None, -32113, -32113)),
    ("TOTAL", "At 31 December 2024", (265750, 0, 5214, 0, -13632, 39889, 297221)),
]
bw.add_equity_changes_sheet(
    title="Union Bancaire Privée (UK) Limited — Statement of Changes in Equity",
    subtitle="Chronological roll-forward, oldest to newest, Company-only basis, £'000. Equity reconciliation ladder "
              "confirmed: every year's own closing balance ties exactly to both the next year's own opening balance "
              "and that year's own Balance Sheet Total equity - zero undocumented plug rows across all 12 years, "
              "FY2013 to FY2024, including the FY2013/FY2014 reclassification bridge (see FY2013 RESTATEMENT NOTE), "
              "the FY2014/FY2015 restatement bridge, the FY2018 IFRS 9 transition "
              "adjustment, the FY2022 acquisition-related transfers of net assets from SGKHCIL/SGKHGL, and FY2024's "
              "capital repayment and share premium cancellation. FY2025 is not yet disclosed (no FY2025 statutory "
              "accounts filed).",
    headers=equity_headers,
    rows=equity_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=54,
    source_height=300,
)

bw.add_cash_flow_sheet(
    title="Union Bancaire Privée (UK) Limited — Statement of Cash Flows",
    subtitle="Not applicable: the Company's own FRS 101 Reduced Disclosure Framework accounts do not include a Statement of Cash Flows in any year covered (a permitted FRS 101 exemption, distinct from the separate Pillar 3/statutory consolidation-scope mismatch noted below).",
    rows=[
        ("SECTION", "FRS 101 exemption", {}),
        ("DATA", "Standalone cash-flow statement", {year: "Not presented" for year in YEARS}),
    ],
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=82,
    source_height=250,
    unit_suffix="",
    years=YEARS,
)

asset_quality_rows = [
    ("SECTION", "Loans and advances to customers, by product (gross)", {}),
    ("DATA", "Retail mortgages", {"FY2024": 1162158, "FY2023": 1409121, "FY2022": 1690736, "FY2021": 865254, "FY2020": 865388, "FY2019": 836349, "FY2018": 827576}),
    ("DATA", "Other loans", {"FY2024": 518784, "FY2023": 532693, "FY2022": 684771, "FY2021": 392952, "FY2020": 307356, "FY2019": 287701, "FY2018": 250797}),
    ("TOTAL", "Total gross loans and advances to customers", {"FY2024": 1680942, "FY2023": 1941814, "FY2022": 2375507, "FY2021": 1258206, "FY2020": 1172744, "FY2019": 1124050, "FY2018": 1078373, "FY2017": 1168605, "FY2016": 1000895, "FY2015": 941546, "FY2014": 715788}),
    ("DATA", "Expected credit loss / impairment", {"FY2024": -13079, "FY2023": -18176, "FY2022": -20117, "FY2021": -9592, "FY2020": -6184, "FY2019": -4688, "FY2018": -3899, "FY2017": -3056, "FY2016": -4132, "FY2015": -3376, "FY2014": -2764}),
    ("TOTAL", "Net loans and advances to customers", {"FY2024": 1667863, "FY2023": 1923638, "FY2022": 2355390, "FY2021": 1248614, "FY2020": 1166560, "FY2019": 1119362, "FY2018": 1074474, "FY2017": 1168605, "FY2016": 996763, "FY2015": 938170, "FY2014": 713024}),
    ("SECTION", "Credit quality by IFRS 9 stage, net of ECL (IFRS 9 adopted 1 January 2018 - see IFRS 9 TRANSITION NOTE; not applicable pre-2018)", {}),
    ("DATA", "Stage 1 (performing)", {"FY2024": 1524977, "FY2023": 1710531, "FY2022": 2132521, "FY2021": 1138843, "FY2020": 1073652, "FY2019": 1072056}),
    ("DATA", "Stage 2 (underperforming)", {"FY2024": 55231, "FY2023": 100344, "FY2022": 132207, "FY2021": 39609, "FY2020": 36131, "FY2019": 5805}),
    ("DATA", "Stage 3 (non-performing)", {"FY2024": 87655, "FY2023": 112763, "FY2022": 90662, "FY2021": 70162, "FY2020": 56777, "FY2019": 41501}),
    ("TOTAL", "Total, net of ECL", {"FY2024": 1667863, "FY2023": 1923638, "FY2022": 2355390, "FY2021": 1248614, "FY2020": 1166560, "FY2019": 1119362}),
    ("SECTION", "Gross carrying amount by IFRS 9 stage", {}),
    ("DATA", "Stage 1 (performing), gross", {"FY2024": 1526322, "FY2023": 1712678, "FY2022": 2135104, "FY2021": 1141352, "FY2020": 1076060, "FY2019": 1073672}),
    ("DATA", "Stage 2 (underperforming), gross", {"FY2024": 57078, "FY2023": 102584, "FY2022": 134462, "FY2021": 39936, "FY2020": 36286, "FY2019": 5894}),
    ("DATA", "Stage 3 (non-performing), gross", {"FY2024": 97542, "FY2023": 126552, "FY2022": 105941, "FY2021": 76918, "FY2020": 60398, "FY2019": 44484}),
    ("TOTAL", "Total gross carrying amount", {"FY2024": 1680942, "FY2023": 1941814, "FY2022": 2375507, "FY2021": 1258206, "FY2020": 1172744, "FY2019": 1124050}),
    ("SECTION", "Loan book by security type, net of ECL", {}),
    ("DATA", "Lombard", {"FY2024": 323533, "FY2023": 339135, "FY2022": 504694, "FY2021": 283206, "FY2020": 238902, "FY2019": 223153}),
    ("DATA", "Real estate", {"FY2024": 1265966, "FY2023": 1546376, "FY2022": 1799430, "FY2021": 944242, "FY2020": 916189, "FY2019": 883525}),
    ("DATA", "Asset-backed", {"FY2024": 6086, "FY2023": 14554, "FY2022": 23401, "FY2021": 2860, "FY2020": 3383, "FY2019": 1809}),
    ("DATA", "Unsecured", {"FY2024": 72278, "FY2023": 23573, "FY2022": 27865, "FY2021": 18306, "FY2020": 8086, "FY2019": 10875}),
    ("TOTAL", "Total, net of ECL (by security type)", {"FY2024": 1667863, "FY2023": 1923638, "FY2022": 2355390, "FY2021": 1248614, "FY2020": 1166560, "FY2019": 1119362}),
    ("SECTION", "Loan book by security type, net of ECL (FY2017-2018 own category labels: Non-guaranteed/Defaulted, not yet Unsecured)", {}),
    ("DATA", "Lombard (FY2017-2018)", {"FY2018": 228172, "FY2017": 236136}),
    ("DATA", "Real estate (FY2017-2018)", {"FY2018": 826814, "FY2017": 916226}),
    ("DATA", "Asset-backed (FY2017-2018)", {"FY2018": 2210, "FY2017": 957}),
    ("DATA", "Non-guaranteed (FY2017-2018)", {"FY2018": 12508, "FY2017": 15286}),
    ("DATA", "Defaulted (FY2017-2018)", {"FY2018": 4770, "FY2017": 0}),
    ("TOTAL", "Total, net of ECL (FY2017-2018 category basis)", {"FY2018": 1074474, "FY2017": 1168605}),
    ("SECTION", "Loans and advances to customers, by remaining contractual maturity (only credit disclosure available FY2014-2016; gross)", {}),
    ("DATA", "3 months or less", {"FY2016": 235192, "FY2015": 312216, "FY2014": 325972}),
    ("DATA", "Between 3 months and 1 year (or '1 year or less but over 3 months')", {"FY2016": 64667, "FY2015": 22355, "FY2014": 31185}),
    ("DATA", "Greater than 1 year", {"FY2016": 701036, "FY2015": 606975, "FY2014": 358631}),
    ("TOTAL", "Total gross (by maturity)", {"FY2016": 1000895, "FY2015": 941546, "FY2014": 715788}),
    ("DATA", "Of which repayable on demand (memo, included within the maturity buckets above)", {"FY2016": 232226, "FY2015": 276531, "FY2014": 318234}),
    ("SECTION", "Derived ratios (as reported)", {}),
    ("DATA", "Non-performing loan ratio (Stage 3 gross / total gross)", {"FY2024": "5.80%", "FY2023": "6.52%", "FY2022": "4.46%", "FY2021": "6.11%"}),
    ("DATA", "Total coverage ratio (total ECL / total gross)", {"FY2024": "0.78%", "FY2023": "0.94%", "FY2022": "0.79%", "FY2021": "0.76%"}),
    ("DATA", "Stage 3 coverage ratio", {"FY2024": "10.14%", "FY2023": "10.90%", "FY2022": "14.41%", "FY2021": "8.78%"}),
]
bw.add_asset_quality_sheet(
    title="Union Bancaire Privée (UK) Limited — Asset Quality",
    subtitle="Loans and advances to customers by product, IFRS 9 stage and security type (Note 14), Company-only basis, £'000. FY2014-2017 predate IFRS 9 staging (adopted 1 Jan 2018) and disclosed no product/security breakdown - only gross loans, a single impairment allowance, and a contractual-maturity split, shown in their own section rather than forced into the IFRS-9-era rows. FY2017-2018 use different security-type category labels (Non-guaranteed/Defaulted) than FY2019 onward (Unsecured) - both shown, not merged. Every populated block ties exactly to the Balance Sheet's Loans and advances to customers line and to each other.",
    rows=asset_quality_rows,
    sources_text=STATEMENTS_SOURCES + (
        "\n\nNote 14 (Loans and advances to customers) page references - FY2024/FY2023: AR2024 p.56-57; "
        "FY2023/FY2022: AR2023 p.55-56 (FY2022's own credit-quality table is not in the AR2022 Companies "
        "House filing, which is truncated after Note 12 - see the note above); FY2021/FY2020: AR2021 p.49-50; "
        "FY2020/FY2019: AR2020 Note 14; FY2019/FY2018: AR2019 Note 14; FY2018/FY2017: AR2018 Note 14 "
        "(FY2017's IFRS-9-stage figures are this filing's own FY2017 restated comparative, not FY2017's own "
        "pre-IFRS-9 accounts - see IFRS 9 TRANSITION NOTE); FY2017/FY2016: AR2017 Note 14/15 (contractual "
        "maturity only, pre-IFRS 9); FY2016/FY2015: AR2016 Note 16; FY2015/FY2014: AR2015 Note "
        "'Loans to customers'; FY2014: AR2014 Note 15. "
        "Coverage/NPL ratios derived from each year's own reported gross-by-stage and ECL-by-stage tables; "
        "the total coverage ratio and Stage 3 coverage ratio are reproduced exactly as reported."
    ),
    first_col_width=90,
    source_height=340,
    unit_suffix=" (£'000)",
)


def metric(name, unit, rows_data, note=None):
    bw.add_metric_sheet(
        name,
        unit,
        rows_data,
        P3_SOURCES,
        note=note,
        first_col_width=65,
        source_height=240,
    )


CAPITAL = {"FY2024": 291.256, "FY2023": 356.795, "FY2022": 426.529, "FY2021": 461.392}
RWA = {"FY2024": 1373.096, "FY2023": 1450.014, "FY2022": 1830.761, "FY2021": 1951.543}
CAPITAL_RATIO = {"FY2024": "21.2%", "FY2023": "24.6%", "FY2022": "23.3%", "FY2021": "23.6%"}
LEVERAGE_EXPOSURE = {"FY2024": 4407.957, "FY2023": 4161.978, "FY2022": 4707.494, "FY2021": 5203.049}
LEVERAGE = {"FY2024": "6.6%", "FY2023": "8.6%", "FY2022": "9.1%", "FY2021": "8.9%"}
HQLA = {"FY2024": 2565.121, "FY2023": 2191.986, "FY2022": 2372.431, "FY2021": 2319.358}
LCR_OUTFLOWS = {"FY2024": 1167.142, "FY2023": 971.156, "FY2022": 1029.869, "FY2021": 1079.986}
LCR_INflows = {"FY2024": 135.972, "FY2023": 103.495, "FY2022": 208.111, "FY2021": 301.570}
LCR_NET = {"FY2024": 1031.169, "FY2023": 867.661, "FY2022": 821.759, "FY2021": 778.416}
LCR = {"FY2024": "248.8%", "FY2023": "252.6%", "FY2022": "288.7%", "FY2021": "298.0%"}
ASF = {"FY2024": 3202.089, "FY2023": 3140.112, "FY2022": 3765.621, "FY2021": 3792.308}
RSF = {"FY2024": 1265.791, "FY2023": 1441.162, "FY2022": 1698.754, "FY2021": 2108.413}
NSFR = {"FY2024": "253.0%", "FY2023": "217.9%", "FY2022": "221.7%", "FY2021": "179.9%"}

GAP_NOTE = (
    "FY2025 is blank because the official UBP UK archive currently provides "
    "SGKH UK Consolidation Group disclosures through 31 December 2024 only. "
    "FY2021-FY2024 are populated from the 2022-2024 reports. FY2014-FY2020 are "
    "blank throughout - no Pillar 3 capital/RWA disclosure could be located for "
    "the entity for those years under any trading name; see the FY2014-FY2020 "
    "note above for the Wayback Machine search performed. Amounts are "
    "converted from £'000 to £m; ratios remain as reported."
)

metric("CET1 Capital", "£m", [("Common Equity Tier 1 (CET1) capital", CAPITAL)], GAP_NOTE)
metric("CET1 Ratio", "%", [("Common Equity Tier 1 ratio", CAPITAL_RATIO)], GAP_NOTE)
metric("Tier 1 Capital", "£m", [("Tier 1 capital", CAPITAL)], "Tier 1 capital equals CET1 capital in every populated year; the UK KM1 tables report the same amount.\n" + GAP_NOTE)
metric("Tier 1 Ratio", "%", [("Tier 1 ratio", CAPITAL_RATIO)], GAP_NOTE)
metric("Total Capital", "£m", [("Total capital", CAPITAL)], "Total capital equals CET1 and Tier 1 capital in every populated year in the UK KM1 tables.\n" + GAP_NOTE)
metric("Total Capital Ratio", "%", [("Total capital ratio", CAPITAL_RATIO)], GAP_NOTE)
metric("Total RWAs", "£m", [("Total risk-weighted exposure amounts", RWA)], GAP_NOTE)

RWA_CREDIT = {"FY2024": 1088.247, "FY2023": 1209.992, "FY2022": 1556.662, "FY2021": 1663.351}
RWA_CCR = {"FY2024": 38.962, "FY2023": 32.907, "FY2022": 34.661, "FY2021": 21.756}
RWA_SETTLEMENT = {"FY2024": 0.000, "FY2023": 0.092, "FY2022": 0.004, "FY2021": 0.042}
RWA_MARKET = {"FY2024": 1.174, "FY2023": 1.336, "FY2022": 1.158, "FY2021": 0.881}
RWA_OPERATIONAL = {"FY2024": 244.713, "FY2023": 205.688, "FY2022": 238.276, "FY2021": 265.514}
RWA_THRESHOLD_MEMO = {"FY2024": 30.604, "FY2023": 31.439, "FY2022": 35.922, "FY2021": 12.243}
rwa_breakdown_rows = [
    ("SECTION", "UK OV1 - Overview of Risk-Weighted Exposure Amounts", {}),
    ("DATA", "Credit Risk (excluding CCR)", RWA_CREDIT),
    ("DATA", "Counterparty Credit Risk (CCR)", RWA_CCR),
    ("DATA", "Settlement Risk", RWA_SETTLEMENT),
    ("DATA", "Position, foreign exchange and commodities risks (Market Risk)", RWA_MARKET),
    ("DATA", "Operational risk", RWA_OPERATIONAL),
    ("TOTAL", "Total risk-weighted exposure amounts", RWA),
    ("DATA", "Memo: amounts below thresholds for deduction (250% risk weight, excluded from Total)", RWA_THRESHOLD_MEMO),
]
bw.add_rwa_breakdown_sheet(
    title="Union Bancaire Privée (UK) Limited — RWA Breakdown",
    subtitle="UK Consolidation Group basis, £m. Category rows sum exactly to Total RWAs (the 'amounts below thresholds for deduction' row is a memo/for-information line excluded from the additive total, per the source template's own footnote).",
    rows=rwa_breakdown_rows,
    sources_text=P3_SOURCES + (
        "\n\nUK OV1 category breakdown: FY2024/FY2023 - SGKH Pillar 3 Disclosure 31 December 2024, "
        f"Table UK OV1 p.9 - {P3_2024_URL}\nFY2022/FY2021 - SGKH Pillar 3 Disclosure 31 December 2022, "
        f"Table UK OV1 p.9 - {P3_2022_URL}. FY2021's Counterparty Credit Risk (CCR) figure is transcribed "
        "as £21.756m: the source document prints '21,7561' (a trailing-digit typo confirmed by the column "
        "summing to the reported Total RWAs of £1,951.543m only when read as 21,756)."
    ),
    first_col_width=76,
    source_height=300,
    unit_suffix=" (£m)",
)

metric(
    "Leverage Ratio",
    "£m / %",
    [
        ("Total exposure measure excluding claims on central banks", LEVERAGE_EXPOSURE),
        ("Leverage ratio excluding claims on central banks", LEVERAGE),
    ],
    "SGKH states that it is outside the binding LREQ framework but continues to monitor leverage. The reported ratio uses the excluding-central-bank-claims basis.\n" + GAP_NOTE,
)
metric(
    "LCR",
    "£m / %",
    [
        ("Total HQLA, weighted value average", HQLA),
        ("Cash outflows, total weighted value", LCR_OUTFLOWS),
        ("Cash inflows, total weighted value", LCR_INflows),
        ("Total net cash outflows, adjusted value", LCR_NET),
        ("Liquidity Coverage Ratio", LCR),
    ],
    "LCR is presented on the reports' weighted-average basis. FY2021 component values are taken from the FY2022 report's comparative column.\n" + GAP_NOTE,
)
metric(
    "NSFR",
    "£m / %",
    [
        ("Total available stable funding", ASF),
        ("Total required stable funding", RSF),
        ("NSFR ratio", NSFR),
    ],
    "NSFR is presented on the reports' four-quarter average basis. FY2021 component values are taken from the FY2022 report's comparative column.\n" + GAP_NOTE,
)

bw.add_not_disclosed_metric_sheets(
    ["MREL Ratio"],
    P3_SOURCES,
    per_note={
        "MREL Ratio": "No numeric MREL ratio was found in the 2022-2024 UK Consolidation Group disclosures reviewed. FY2025 is also outside the located disclosure coverage.",
    },
)

bw.add_overview_sheet(
    cash_flow_totals=[],
    cash_flow_unit=None,
    ratios=[
        ("CET1 Ratio", CAPITAL_RATIO),
        ("Tier 1 Ratio", CAPITAL_RATIO),
        ("Total Capital Ratio", CAPITAL_RATIO),
        ("Leverage Ratio", LEVERAGE),
        ("LCR", LCR),
        ("NSFR", NSFR),
    ],
    note=(
        "Balance Sheet/P&L/Equity are on the Company-only statutory basis, FY2013-FY2024 (Asset Quality "
        "is FY2014-FY2024 only - see that sheet); Pillar 3 ratios are on the UK Consolidation Group basis, "
        "FY2021-FY2024 only - two different scopes, per the Company's own disclosures (see the entity/basis "
        "note on each sheet). FY2025 is blank throughout because no FY2025 statutory accounts or UK "
        "Consolidation Group Pillar 3 disclosure had been filed/located as of this workbook's build date. "
        "FY2014-FY2020 are blank on every Pillar 3 sheet and the RWA Breakdown sheet - no such disclosure "
        "could be located for the entity that far back (confirmed via a Wayback Machine search; see the "
        "P3_SOURCES note on each Pillar 3 sheet). Cash flow is not substituted for any year because the "
        "published accounts state an exemption from presenting a Statement of Cash Flows in every year "
        "back to FY2013 (see CASH_FLOW_SOURCES/FY2013 EXEMPTION BASIS NOTE on the Cash Flow sheet for the "
        "exact basis, which differs between FY2013-2014 and FY2015 onward). The entity traded as SG "
        "Hambros Bank Limited (FY2013-2016), then SG Kleinwort "
        "Hambros Bank Limited (FY2017-2024), then Union Bancaire Privée (UK) Limited - same company "
        "number, 00964058, throughout (see ENTITY/BASIS NOTE)."
    ),
    balance_sheet_totals=[
        ("Total assets", {"FY2024": 4765408, "FY2023": 4530099, "FY2022": 5291601, "FY2021": 2448463, "FY2020": 2334869, "FY2019": 2332598, "FY2018": 2843244, "FY2017": 2812984, "FY2016": 2265070, "FY2015": 1695300, "FY2014": 1638376, "FY2013": 1318481}),
        ("Loans and advances to customers", {"FY2024": 1667863, "FY2023": 1923638, "FY2022": 2355390, "FY2021": 1248614, "FY2020": 1166560, "FY2019": 1119362, "FY2018": 1074474, "FY2017": 1168605, "FY2016": 996763, "FY2015": 938170, "FY2014": 713024, "FY2013": 657026}),
        ("Customers' accounts", {"FY2024": 4329605, "FY2023": 3970768, "FY2022": 4654279, "FY2021": 1934968, "FY2020": 1828626, "FY2019": 1836229, "FY2018": 2191216, "FY2017": 2203384, "FY2016": 1727180, "FY2015": 1354614, "FY2014": 1345833, "FY2013": 1031036}),
        ("Total equity", {"FY2024": 297221, "FY2023": 405397, "FY2022": 477262, "FY2021": 463510, "FY2020": 437606, "FY2019": 418388, "FY2018": 505454, "FY2017": 420906, "FY2016": 283490, "FY2015": 267737, "FY2014": 257345, "FY2013": 253926}),
    ],
    balance_sheet_unit=" (£'000)",
    income_statement_totals=[
        ("Total operating income", {"FY2024": 130404, "FY2023": 167032, "FY2022": 109174, "FY2021": 96260, "FY2020": 89463, "FY2019": 80949, "FY2018": 149720, "FY2017": 61813, "FY2016": 58795, "FY2015": 57651, "FY2014": 49115, "FY2013": 83113}),
        ("Total operating expenses (derived from reported lines for FY2008-FY2012)", {"FY2024": -121195, "FY2023": -127298, "FY2022": -88021, "FY2021": -64601, "FY2020": -77118, "FY2019": -116151, "FY2018": -90575, "FY2017": -71748, "FY2016": -57230, "FY2015": -46521, "FY2014": -43089, "FY2013": -36034, "FY2012": -43272, "FY2011": -65381, "FY2010": -40111, "FY2009": -35307, "FY2008": -34459}),
        ("Profit for the year", {"FY2024": 8654, "FY2023": 35239, "FY2022": 17764, "FY2021": 30451, "FY2020": 17156, "FY2019": -33995, "FY2018": 62210, "FY2017": -6719, "FY2016": 1446, "FY2015": 10070, "FY2014": 5703, "FY2013": 45016}),
    ],
    income_statement_unit=" (£'000)",
    equity_changes_totals=[
        ("Opening equity", {"FY2024": 405397, "FY2023": 477262, "FY2022": 463510, "FY2021": 437606, "FY2020": 418388, "FY2019": 505454, "FY2018": 420077, "FY2017": 283490, "FY2016": 267737, "FY2015": 258215, "FY2014": 253925, "FY2013": 262383}),
        ("Total comprehensive income/(expense) for the year", {"FY2024": 13805, "FY2023": 47788, "FY2022": 3176, "FY2021": 25864, "FY2020": 19099, "FY2019": -30483, "FY2018": 60258, "FY2017": -5984, "FY2016": 2232, "FY2015": 9564, "FY2014": 8182, "FY2013": 41043}),
        ("Closing equity", {"FY2024": 297221, "FY2023": 405397, "FY2022": 477262, "FY2021": 463510, "FY2020": 437606, "FY2019": 418388, "FY2018": 505454, "FY2017": 420906, "FY2016": 283490, "FY2015": 267737, "FY2014": 257345, "FY2013": 253926}),
    ],
    equity_changes_unit=" (£'000)",
)

bw.save("/Users/armaan/code/katalysis/banks/UNION BANCAIRE PRIVEE UK FINANCIALS.xlsx")
print("Saved.")
