import sys, os

sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = [
    "FY2025", "FY2024", "FY2023", "FY2022", "FY2021",
    "FY2020", "FY2019", "FY2018", "FY2017", "FY2016", "FY2015", "FY2014",
]  # most recent first

AR25_URL = "https://www.tsb.co.uk/content/dam/tsb-public/documents/investors/financial-results-and-reports/2025/TSB-Bank-ARA-2025.pdf"
AR24_URL = "https://www.tsb.co.uk/content/dam/tsb-public/documents/investors/financial-results-and-reports/2024/TSB-Bank-ARA-2024.pdf"
AR23_URL = "https://www.tsb.co.uk/content/dam/tsb-public/documents/investors/financial-results-and-reports/2023/TSB-Bank-2023.pdf"
AR21_URL = "https://www.tsb.co.uk/content/dam/tsb-public/documents/investors/financial-results-and-reports/2021/tsb-bank-ara-2021.pdf"
AR20_URL = "https://www.tsb.co.uk/content/dam/tsb-public/documents/investors/financial-results-and-reports/2020/tsb-bank-ara-2020.pdf"
AR18_URL = "https://www.tsb.co.uk/content/dam/tsb-public/documents/investors/financial-results-and-reports/2018/tsb-bank-ara-2018.pdf"
AR17_URL = "https://www.tsb.co.uk/content/dam/tsb-public/documents/investors/financial-results-and-reports/2017/tsb-bank-ara-2017.pdf"
# FY2014-FY2016: no standalone "TSB Bank plc" entity annual report was published; only
# "TSB Banking Group plc" (the then-listed/Sabadell-owned holding company whose only direct
# subsidiary is TSB Bank plc) annual reports are available for these years - see ENTITY_NOTE.
BG_AR16_URL = "https://www.tsb.co.uk/content/dam/tsb-public/documents/investors/financial-results-and-reports/2016/tsb-2016-results.pdf"
BG_AR15_URL = "https://www.tsb.co.uk/content/dam/tsb-public/documents/investors/financial-results-and-reports/2015/tsb-2015-annual-report.pdf"
BG_AR17_URL = "https://www.tsb.co.uk/content/dam/tsb-public/documents/investors/financial-results-and-reports/2017/tsb-banking-group-annual-report-2017.pdf"
BG_AR18_URL = "https://www.tsb.co.uk/content/dam/tsb-public/documents/investors/financial-results-and-reports/2018/tsb-banking-group-ara-2018.pdf"

P3_25_URL = "https://www.tsb.co.uk/content/dam/tsb-public/documents/investors/rns/tsb-large-subsidiary-disclosure-2025.pdf"
P3_24_URL = "https://www.tsb.co.uk/content/dam/tsb-public/documents/investors/rns/TSB-Large-subsidiary-Disclosure-2024.pdf"
P3_23_URL = "https://www.tsb.co.uk/content/dam/tsb-public/documents/investors/rns/TSB-large-subsidiary-disclosure-2023.pdf"
P3_22_URL = "https://www.tsb.co.uk/content/dam/tsb-public/documents/investors/rns/TSB-Large-subsidiary-Disclosure-2022.pdf"
P3_21_URL = "https://www.tsb.co.uk/content/dam/tsb-public/documents/investors/rns/TSB-Large-Subsidiary-Disclosure-2021.pdf"
P3_20_URL = "https://www.tsb.co.uk/content/dam/tsb-public/documents/investors/rns/TSB-Significant-Subsidiary-Disclosure-2020.pdf"
# FY2017/FY2018: TSB published no standalone Pillar 3/Significant Subsidiary Disclosure
# document (the Annual Report itself states minimum Pillar 3 disclosure requirements are
# "Disclosed in the Sabadell Pillar 3 report", which had "not been approved" as at each
# report's own publication date) - so FY2017/FY2018 capital metrics are sourced from the
# TSB Banking Group plc Annual Report's own "Capital resources"/"Sources of funding" section.
P3_16_URL = "https://www.tsb.co.uk/content/dam/tsb-public/documents/investors/financial-results-and-reports/2016/tsb-material-subsidiary-2016.pdf"
P3_15_URL = "https://www.tsb.co.uk/investors/results-and-reports/TSB-Significant-Subsidiary-Disclosures-2015.pdf"
P3_14_URL = "https://www.tsb.co.uk/content/dam/tsb-public/documents/investors/financial-results-and-reports/2014/TSB-Pillar-3-2014,0.pdf"

ENTITY_NOTE = (
    "ENTITY NOTE: TSB Bank plc (Companies House SC095237) is the entity on the PRA register; its own Annual "
    "Report and Accounts (consolidated 'Bank (Consolidated)' column used throughout) is used for the cash flow "
    "statement from FY2017 onward. TSB Banking Group plc's only direct subsidiary is TSB Bank plc, so 'TSB "
    "Banking Group plc' consolidated Pillar 3 disclosures (published under that name, as TSB is a 'large "
    "subsidiary' of Banco Sabadell for CRR Article 13 purposes) are effectively the same consolidation scope and "
    "are used for all Pillar 3 metric sheets.\n"
    "ENTITY BASIS CHANGE (FY2014-FY2016): no standalone 'TSB Bank plc' entity Annual Report was published for "
    "these years, only 'TSB Banking Group plc' (the then Sabadell-owned holding company) Annual Report and "
    "Accounts. As TSB Banking Group plc's only direct subsidiary is TSB Bank plc, the underlying banking business "
    "and consolidation scope are effectively the same, but the holding company's own share capital/share "
    "premium/reserve structure differs from TSB Bank plc's (a holdco-level, not operating-entity-level, "
    "difference) - so FY2016 closing Shareholder's equity as reported by the Group (£1,865.0m) does not exactly "
    "tie to FY2016 closing equity as later restated in TSB Bank plc's own FY2017 Annual Report comparative "
    "(£1,879.6m), a genuine ~£14.6m entity-basis break at the FY2016/FY2017 boundary, not a data error. Balance "
    "Sheet/P&L/Equity/Cash Flow/Asset Quality figures for FY2014-FY2016 are TSB Banking Group plc consolidated; "
    "FY2017 onward are TSB Bank plc consolidated.\n"
    "CONTEXT: TSB was owned by Banco de Sabadell, S.A. (Spain) throughout FY2014-FY2025 (following the 2013 "
    "demerger from Lloyds Banking Group and TSB Banking Group plc's IPO in 2014; Sabadell acquired full control "
    "in 2015). Santander UK plc agreed to acquire TSB in July 2025 and completed the acquisition on 30 April 2026 "
    "(after this workbook's FY2025 year-end) - so all years of data here reflect the Sabadell-owned period; TSB's "
    "board ceased dividend payments to Sabadell following the announcement per TSB's FY2025 Pillar 3 disclosure.\n"
    "BASEL II/CRD III CAVEAT: TSB Banking Group plc's Pillar 3 Disclosures 2014 present 31 December 2013 "
    "comparatives on both a Basel II basis and a CRD IV-restated basis (CRD IV took effect for the Group's own "
    "31 December 2014 disclosure, its first full year of Pillar 3 reporting as a standalone entity post-demerger) "
    "- CET1/Common Equity Tier 1 terminology is already used from FY2014 onward on a CRD IV basis, so no "
    "Basel II-era terminology substitution was required for any year in this workbook."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are TSB Bank plc / TSB Banking Group plc Bank (Consolidated) basis, £ million (see "
    "entity note below for the FY2014-FY2016 vs FY2017 onward entity change).\n"
    f"FY2025 & FY2024: TSB Bank plc Annual Report and Accounts 2025, p.49 and p.106 (Cash flow statements and "
    f"note 32) - {AR25_URL}\n"
    f"FY2023 & FY2022 (restated): TSB Bank plc Annual Report and Accounts 2023, p.33-34 and p.83-84 (Cash flow "
    f"statements and note 32) - {AR23_URL}\n"
    f"FY2021: TSB Bank plc Annual Report and Accounts 2021, p.29 and p.78 (Cash flow statements and note 31) "
    f"- {AR21_URL}\n"
    f"FY2020 & FY2019: TSB Bank plc Annual Report and Accounts 2020, p.27-28 and p.75-76 (Cash flow statements "
    f"and note 32) - {AR20_URL}\n"
    f"FY2018 & FY2017: TSB Bank plc Annual Report and Accounts 2018, p.29-30 and p.78-79 (Cash flow statements "
    f"and note 34) - {AR18_URL}\n"
    f"FY2016 & FY2015: TSB Banking Group plc Annual Report and Accounts 2016, p.60 (Consolidated cash flow "
    f"statement) - {BG_AR16_URL}\n"
    f"FY2014: TSB Banking Group plc Annual Report and Accounts 2015, p.55 (Consolidated cash flow statement, "
    f"FY2014 comparative column) - {BG_AR15_URL}\n\n" + ENTITY_NOTE + "\n\n"
    "RESTATEMENT NOTE: The 2023 Annual Report restated FY2022 (and earlier) to include on-demand loans and "
    "advances to credit institutions within cash and cash equivalents; this added £56.1m to the FY2021 closing "
    "cash position and £159.2m to the FY2022 opening position on a comparative basis, but FY2021's own Annual "
    "Report was never itself restated. As a result, FY2021's closing cash and cash equivalents (£4,851.1m, as "
    "originally reported) does not exactly tie to FY2022's opening balance shown here (£4,907.2m, restated) - a "
    "known £56.1m definitional break at that one boundary, not a data error. FY2022 onward reconciles exactly. "
    "The 2023 Annual Report also reclassified a derivatives/hedge-accounting fair value line from 'change in "
    "operating assets and liabilities' into 'non-cash and other items' from FY2023 onward; FY2021 and FY2022 keep "
    "their original as-reported classification for that line (see the two separate rows below).\n\n"
    "PRESENTATION NOTE: Line items were relabelled and reorganised across these 5 years as TSB's funding mix "
    "evolved (e.g. 'Issue of debt securities in issue' in FY2021 became separate covered bond/senior "
    "unsecured/securitisation/AT1 lines by FY2024-25; a repurchase-agreements financing line appeared only in "
    "FY2022-23). Blank cells indicate that year's report did not disclose or did not have that specific line; "
    "'0' indicates the report explicitly showed a nil ('-') value. The 'Change in operating assets and "
    "liabilities' and 'Non-cash and other items' rows are TSB's own audited primary-statement subtotals; the "
    "rows above each are the supporting breakdown from the cash flow note.\n\n"
    "FY2019 RECONCILIATION NOTE: TSB Bank plc Annual Report and Accounts 2020's own FY2019 comparative column shows "
    "Net cash used in operating activities of £(360.3)m, investing £403.8m and financing £(2,545.8)m, which sum to "
    "£(2,502.3)m - not the £(2,543.1)m 'Change in cash and cash equivalents' also shown in that same comparative "
    "column, a £40.8m gap. The 2020 Annual Report's own footnote explains why: 'interest received on debt "
    "securities of £53.2 million and interest paid on borrowings from central banks, debt securities in issue and "
    "subordinated liabilities of £(94.0) million' were reclassified into operating activities for FY2020 but the "
    "FY2019 comparative subtotals shown were not fully restated to match (94.0-53.2=40.8, exactly the gap) - "
    "reproduced exactly as TSB's own report shows it, not force-tied.\n\n"
    "FY2014-FY2016 PRESENTATION NOTE: TSB Banking Group plc's FY2014-FY2016 cash flow statements only disclose "
    "'Change in operating assets' and 'Change in operating liabilities' as two combined top-level subtotals (no "
    "further line-item breakdown was published for those years, unlike the note-32/34 breakdowns available from "
    "FY2017 onward), and financing-activity interest payments are presented net within each funding-source line "
    "rather than split out - reproduced at the level of detail each year's own report actually discloses, not "
    "forced into the later years' more granular structure."
)


def p3_sources(page_km1, table_km1="Table 1: Key metrics (KM1)"):
    return (
        "Sources - TSB Banking Group plc consolidated Pillar 3/capital disclosure basis (see entity note on Cash "
        "Flow Statement sheet):\n"
        f"FY2025: TSB Banking Group plc Large Subsidiary Disclosures, as at 31 December 2025, p.6 ({table_km1}) "
        f"- {P3_25_URL}\n"
        f"FY2024: TSB Banking Group plc Large Subsidiary Disclosures, as at 31 December 2024, p.6 (Table 1a: Key "
        f"metrics (KM1)) - {P3_24_URL}\n"
        f"FY2023: TSB Banking Group plc Large Subsidiary Disclosures 2023, p.6 (Table 1a: Key metrics (KM1)) "
        f"- {P3_23_URL}\n"
        f"FY2022: TSB Banking Group plc Large Subsidiary Disclosures 2022, p.6 (Table 1a: Key metrics (KM1)) "
        f"- {P3_22_URL}\n"
        f"FY2021: TSB Banking Group plc Large Subsidiary Disclosures 2021, p.5 (Table 1: Key metrics (KM1 / IFRS "
        f"9-FL)) - {P3_21_URL}\n"
        f"FY2020 & FY2019: TSB Banking Group plc Significant Subsidiary Disclosures 2020, p.5 (Table 1: Key "
        f"metrics (KM1 / IFRS 9-FL)) - {P3_20_URL}\n"
        f"FY2018: TSB Banking Group plc Annual Report and Accounts 2018, p.11 ('Capital resources' table within "
        f"'Sources of funding') - {BG_AR18_URL}\n"
        f"FY2017: TSB Banking Group plc Annual Report and Accounts 2017, p.16 ('Capital ratios' table within "
        f"'Sources of funding') - {BG_AR17_URL}\n"
        f"FY2016: TSB Banking Group plc Material Subsidiary Pillar 3 Disclosures 2016, p.4 (Table 1: Own funds) "
        f"- {P3_16_URL}\n"
        f"FY2015: TSB Banking Group plc Pillar 3 Disclosures 2015, p.5 (Table 1: Own funds) - {P3_15_URL}\n"
        f"FY2014: TSB Banking Group plc Pillar 3 Disclosures 2014, p.17 (Table 6: Own funds) - {P3_14_URL}\n\n"
        "NOTE (FY2017/FY2018): TSB published no standalone Pillar 3/Significant Subsidiary Disclosure document "
        "for these two years - see ENTITY NOTE on the Cash Flow Statement sheet. Figures are sourced from the "
        "capital summary within the Banking Group's own Annual Report instead, which discloses CET1/Tier 1/Total "
        "capital, RWAs, and capital ratios on the same fully-loaded CRD IV basis as the standalone Pillar 3 "
        "documents used for adjacent years."
    )


bw = BankWorkbook(bank_name="TSB Bank plc", years=YEARS, header_color="002D5B")

# ---------------------------------------------------------------
# Statement sources - TSB Bank plc, Bank (Consolidated) basis, £ million,
# each year's own Annual Report figures, independently cross-checked against
# the adjacent report's comparative column - ties exactly across all 5 years
# for Total assets/Total liabilities/Total equity, Profit for the year, and
# Total comprehensive income. Zero undocumented plug rows anywhere.
# ---------------------------------------------------------------
STATEMENTS_SOURCES = (
    "Sources - TSB Bank plc / TSB Banking Group plc, Bank (Consolidated) basis, £ million (see entity note "
    "below for the FY2014-FY2016 vs FY2017 onward entity change):\n"
    f"FY2025 & FY2024: TSB Bank plc Annual Report and Accounts 2025, p.46 (Balance sheets), p.47 (Consolidated "
    f"statement of comprehensive income), p.48 (Statements of changes in equity) - {AR25_URL}\n"
    f"FY2023 & FY2022: TSB Bank plc Annual Report and Accounts 2023, p.30 (Balance sheets), p.31 (Consolidated "
    f"statement of comprehensive income), p.32 (Statements of changes in equity) - {AR23_URL}\n"
    f"FY2021: TSB Bank plc Annual Report and Accounts 2021, p.26 (Balance sheets), p.27 (Consolidated statement "
    f"of comprehensive income), p.28 (Statements of changes in equity); FY2021's closing equity ties exactly to "
    f"AR2023's own 'Balance at 1 January 2022' comparative - {AR21_URL}\n"
    f"FY2020 & FY2019: TSB Bank plc Annual Report and Accounts 2020, p.25 (Balance sheets), p.26 (Consolidated "
    f"statement of comprehensive income), p.27 (Statements of changes in equity) - {AR20_URL}\n"
    f"FY2018 & FY2017: TSB Bank plc Annual Report and Accounts 2018, p.26 (Balance sheets), p.27 (Consolidated "
    f"statement of comprehensive income), p.28 (Statements of changes in equity); FY2017's closing equity ties "
    f"exactly to TSB Bank plc Annual Report and Accounts 2017's own p.19-20 figures - {AR18_URL}\n"
    f"FY2016 & FY2015: TSB Banking Group plc Annual Report and Accounts 2016, p.57 (Consolidated balance sheet), "
    f"p.58 (Consolidated statement of comprehensive income), p.59 (Consolidated statement of changes in equity) "
    f"- {BG_AR16_URL}\n"
    f"FY2014: TSB Banking Group plc Annual Report and Accounts 2015, p.52 (Consolidated balance sheet), p.53 "
    f"(Consolidated statement of comprehensive income), p.54 (Consolidated statement of changes in equity), "
    f"FY2014 comparative columns - {BG_AR15_URL}\n\n" + ENTITY_NOTE + "\n\n"
    "PRESENTATION NOTE: Balance sheet - 'Loans and advances to credit institutions' is shown as a standalone line "
    "from FY2025 only; FY2021-FY2024 combine it with central bank placements as 'Loans and advances to central "
    "banks and credit institutions' (same figures reused here). 'Other equity instruments' (Additional Tier 1) "
    "first appears FY2024, following TSB's first AT1 issuance that year (see Cash Flow Statement financing "
    "activities). Income statement - FY2024/FY2025 itemise 'Gains on derecognition of financial assets/liabilities' "
    "lines that differ from FY2021-FY2023's own line items (e.g. FVOCI derecognition gains only shown FY2021-23); "
    "each year's own as-published structure is preserved rather than forced into a common format.\n\n"
    "FY2014-FY2020 PRESENTATION NOTE: pre-IFRS 9 (FY2014-FY2017) balance sheets classify lending as 'Loans and "
    "receivables' (IAS 39) rather than 'Financial assets at amortised cost' (IFRS 9, from FY2018); equity reserve "
    "line items also change name over time ('Available-for-sale reserve' pre-IFRS 9 becomes 'Fair value reserve' "
    "from FY2018, following the reclassification recorded in the FY2018 Statement of Changes in Equity's 'Change "
    "on initial application of IFRS 9' transition row - both are shown under their as-published label for each "
    "year rather than relabelled retrospectively). TSB Banking Group plc's FY2014-FY2016 equity structure (Share "
    "capital £5.0m, Share premium £965.1m, Merger reserve £616.5m, Capital reorganisation reserve -£1,311.6m, "
    "Capital reserve £410.0m) differs from TSB Bank plc's own FY2017-2025 structure (Share capital £79.4m, Share "
    "premium £195.6m, Merger reserve £412.8m, no separate capital reorganisation/capital reserve lines) - a "
    "genuine holdco-vs-operating-entity difference, not a data error; see ENTITY NOTE above."
)

# ---------------------------------------------------------------
# Balance Sheet - equity reconciliation ladder step 1: built first so each
# year's own Total equity is the independent check value for the equity
# sheet below.
# ---------------------------------------------------------------
balance_sheet_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash, cash balances at central banks and other demand deposits", {"FY2025": 4202.1, "FY2024": 4823.8, "FY2023": 5897.3, "FY2022": 5238.8, "FY2021": 4851.1, "FY2020": 5056.3, "FY2019": 4592.8, "FY2018": 7135.9, "FY2017": 7563.4, "FY2016": 3698.3, "FY2015": 2755.6, "FY2014": 4396.3}),
    ("DATA", "Debt securities at amortised cost", {"FY2025": 1986.4, "FY2024": 1982.5, "FY2023": 2124.2, "FY2022": 1951.6, "FY2021": 2166.7, "FY2020": 1123.7, "FY2019": 548.6, "FY2018": 96.2}),
    ("DATA", "Financial assets at fair value through profit or loss (equity instruments)", {"FY2018": 1.4, "FY2017": 1.3}),
    ("DATA", "Current tax assets", {"FY2018": 19.7}),
    ("DATA", "Loans and advances to customers", {"FY2025": 36268.4, "FY2024": 36330.9, "FY2023": 36245.9, "FY2022": 38050.0, "FY2021": 37383.8, "FY2020": 33317.9, "FY2019": 31075.8, "FY2018": 30008.5, "FY2017": 30854.2, "FY2016": 29419.1, "FY2015": 26402.2, "FY2014": 21641.4}),
    ("DATA", "Loans and advances to central banks and credit institutions", {"FY2025": 305.2, "FY2024": 277.8, "FY2023": 328.0, "FY2022": 303.5, "FY2021": 199.7, "FY2020": 164.2, "FY2019": 469.3, "FY2018": 458.4, "FY2017": 385.2, "FY2016": 550.4, "FY2015": 331.7, "FY2014": 134.5}),
    ("DATA", "Reverse repurchase agreement", {"FY2025": 62.0, "FY2024": 0, "FY2019": 201.1}),
    ("DATA", "Other advances", {"FY2025": 66.9, "FY2024": 130.2, "FY2023": 209.6, "FY2022": 703.2, "FY2021": 80.7, "FY2020": 217.5, "FY2019": 279.6, "FY2018": 381.4, "FY2017": 896.0}),
    ("DATA", "Items in course of collection from banks", {"FY2016": 213.8, "FY2015": 163.0, "FY2014": 135.7}),
    ("DATA", "Equity instruments (held for trading)", {"FY2016": 8.7}),
    ("DATA", "Debt securities at fair value through other comprehensive income / Available-for-sale financial assets", {"FY2025": 440.2, "FY2024": 328.6, "FY2023": 356.6, "FY2022": 509.5, "FY2021": 1069.0, "FY2020": 1496.9, "FY2019": 1587.4, "FY2018": 2387.8, "FY2017": 2123.3, "FY2016": 2103.5, "FY2015": 1262.8, "FY2014": 339.7}),
    ("DATA", "Derivative financial assets not in hedge accounting relationships", {"FY2025": 362.4, "FY2024": 667.6, "FY2023": 822.9, "FY2022": 1158.7, "FY2021": 168.4, "FY2020": 198.3, "FY2019": 111.5, "FY2018": 88.4, "FY2017": 111.1, "FY2016": 143.2}),
    ("DATA", "Hedging derivative financial assets", {"FY2025": 1149.2, "FY2024": 1274.3, "FY2023": 1346.9, "FY2022": 1565.9, "FY2021": 244.5, "FY2020": 139.9, "FY2019": 93.4, "FY2018": 106.6, "FY2017": 103.7, "FY2016": 104.3}),
    ("DATA", "Derivative financial assets (combined, pre-FY2016 presentation)", {"FY2015": 90.5, "FY2014": 123.1}),
    ("DATA", "Fair value adjustments for portfolio hedged risk", {"FY2025": 4.5, "FY2024": -170.9, "FY2023": -154.9, "FY2022": -542.8, "FY2021": -109.3, "FY2020": 80.2, "FY2019": 20.5, "FY2018": -37.3, "FY2017": -22.2, "FY2016": 0.8}),
    ("DATA", "Property and equipment", {"FY2025": 215.1, "FY2024": 233.9, "FY2023": 253.5, "FY2022": 287.5, "FY2021": 300.3, "FY2020": 258.9, "FY2019": 293.2, "FY2018": 163.1, "FY2017": 172.7, "FY2016": 168.3, "FY2015": 161.1, "FY2014": 149.2}),
    ("DATA", "Intangible assets", {"FY2025": 123.4, "FY2024": 109.9, "FY2023": 86.1, "FY2022": 75.6, "FY2021": 72.1, "FY2020": 49.5, "FY2019": 20.3, "FY2018": 18.4, "FY2017": 10.1, "FY2016": 2.6}),
    ("DATA", "Deferred tax asset", {"FY2025": 6.1, "FY2024": 8.1, "FY2023": 43.2, "FY2022": 64.5, "FY2021": 122.6, "FY2020": 144.5, "FY2019": 96.1, "FY2018": 113.0, "FY2017": 68.6, "FY2016": 99.6, "FY2015": 121.1, "FY2014": 108.1}),
    ("DATA", "Other assets", {"FY2025": 89.6, "FY2024": 102.4, "FY2023": 93.6, "FY2022": 83.6, "FY2021": 156.0, "FY2020": 174.6, "FY2019": 146.3, "FY2018": 197.1, "FY2017": 269.3, "FY2016": 685.7, "FY2015": 330.0, "FY2014": 143.4}),
    ("TOTAL", "Total assets", {"FY2025": 45281.5, "FY2024": 46099.1, "FY2023": 47652.9, "FY2022": 49449.6, "FY2021": 46705.6, "FY2020": 42422.4, "FY2019": 39535.9, "FY2018": 41138.6, "FY2017": 42536.7, "FY2016": 37195.7, "FY2015": 31618.0, "FY2014": 27171.4}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Customer deposits", {"FY2025": 35209.0, "FY2024": 35051.2, "FY2023": 34764.3, "FY2022": 36338.2, "FY2021": 35951.9, "FY2020": 34375.3, "FY2019": 30182.4, "FY2018": 29084.3, "FY2017": 30520.6, "FY2016": 29383.8, "FY2015": 25915.7, "FY2014": 24624.9}),
    ("DATA", "Borrowings from central banks", {"FY2025": 598.9, "FY2024": 1406.9, "FY2023": 4057.9, "FY2022": 5538.3, "FY2021": 5501.6, "FY2020": 3065.8, "FY2019": 4483.5, "FY2018": 6482.2, "FY2017": 5625.7}),
    ("DATA", "Deposits from credit institutions", {"FY2018": 3.4, "FY2016": 49.6, "FY2015": 0.8, "FY2014": 32.5}),
    ("DATA", "Debt securities in issue", {"FY2025": 4869.3, "FY2024": 4583.2, "FY2023": 3664.1, "FY2022": 1955.5, "FY2021": 2199.1, "FY2020": 1699.2, "FY2019": 1676.3, "FY2018": 1122.6, "FY2017": 1318.7, "FY2016": 2940.1, "FY2015": 2899.6, "FY2014": 10.0}),
    ("DATA", "Repurchase agreements", {"FY2023": 0, "FY2022": 360.0, "FY2018": 1084.8, "FY2017": 1446.4, "FY2016": 1409.6}),
    ("DATA", "Subordinated liabilities", {"FY2025": 297.8, "FY2024": 285.9, "FY2023": 277.7, "FY2022": 265.4, "FY2021": 291.8, "FY2020": 391.3, "FY2019": 395.9, "FY2018": 398.2, "FY2017": 405.3, "FY2016": 413.3, "FY2015": 402.1, "FY2014": 405.5}),
    ("DATA", "Lease liabilities", {"FY2025": 107.8, "FY2024": 120.7, "FY2023": 125.0, "FY2022": 145.9, "FY2021": 163.5, "FY2020": 123.3}),
    ("DATA", "Items in course of transmission to banks", {"FY2016": 176.1, "FY2015": 152.3, "FY2014": 144.6}),
    ("DATA", "Other financial liabilities", {"FY2025": 1080.6, "FY2024": 1184.6, "FY2023": 1222.4, "FY2022": 1320.1, "FY2021": 193.6, "FY2020": 51.6, "FY2019": 80.7, "FY2018": 66.4, "FY2017": 247.3}),
    ("DATA", "Derivative financial liabilities not in hedge accounting relationships", {"FY2025": 456.7, "FY2024": 824.2, "FY2023": 982.1, "FY2022": 1252.4, "FY2021": 156.5, "FY2020": 299.7, "FY2019": 127.9, "FY2018": 93.1, "FY2017": 37.5, "FY2016": 97.7}),
    ("DATA", "Hedging derivative financial liabilities", {"FY2025": 99.4, "FY2024": 143.6, "FY2023": 318.7, "FY2022": 301.5, "FY2021": 136.8, "FY2020": 225.2, "FY2019": 288.5, "FY2018": 346.0, "FY2017": 566.5, "FY2016": 529.1}),
    ("DATA", "Derivative financial liabilities (combined, pre-FY2016 presentation)", {"FY2015": 283.3, "FY2014": 116.7}),
    ("DATA", "Fair value adjustments for portfolio hedged risk", {"FY2025": 12.3, "FY2024": -134.7, "FY2023": -85.5, "FY2022": -321.3, "FY2021": -63.6, "FY2020": 117.0, "FY2019": 52.2, "FY2018": 19.4, "FY2017": 42.2, "FY2016": 70.7}),
    ("DATA", "Provisions", {"FY2025": 22.2, "FY2024": 39.8, "FY2023": 75.2, "FY2022": 125.0, "FY2021": 110.2, "FY2020": 153.1, "FY2019": 51.8, "FY2018": 63.6, "FY2017": 34.5, "FY2016": 10.8}),
    ("DATA", "Current tax liabilities", {"FY2017": 6.9, "FY2016": 14.7}),
    ("DATA", "Other liabilities", {"FY2025": 189.5, "FY2024": 473.0, "FY2023": 296.4, "FY2022": 238.8, "FY2021": 197.8, "FY2020": 196.0, "FY2019": 154.1, "FY2018": 495.7, "FY2017": 278.5, "FY2016": 246.0, "FY2015": 217.9, "FY2014": 202.8}),
    ("TOTAL", "Total liabilities", {"FY2025": 42943.5, "FY2024": 43978.4, "FY2023": 45698.3, "FY2022": 47519.8, "FY2021": 44839.2, "FY2020": 40697.5, "FY2019": 37635.1, "FY2018": 39259.7, "FY2017": 40530.1, "FY2016": 35330.7, "FY2015": 29871.7, "FY2014": 25537.0}),
    ("SECTION", "Equity", {}),
    ("DATA", "Share capital", {"FY2025": 79.4, "FY2024": 79.4, "FY2023": 79.4, "FY2022": 79.4, "FY2021": 79.4, "FY2020": 79.4, "FY2019": 79.4, "FY2018": 79.4, "FY2017": 79.4, "FY2016": 5.0, "FY2015": 5.0, "FY2014": 5.0}),
    ("DATA", "Share premium", {"FY2025": 195.6, "FY2024": 195.6, "FY2023": 195.6, "FY2022": 195.6, "FY2021": 195.6, "FY2020": 195.6, "FY2019": 195.6, "FY2018": 195.6, "FY2017": 195.6, "FY2016": 965.1, "FY2015": 965.1, "FY2014": 965.1}),
    ("DATA", "Other equity instruments", {"FY2025": 250.0, "FY2024": 250.0}),
    ("DATA", "Merger reserve / Other reserves", {"FY2025": 412.8, "FY2024": 412.8, "FY2023": 412.8, "FY2022": 412.8, "FY2021": 412.8, "FY2020": 412.8, "FY2019": 412.8, "FY2018": 412.8, "FY2017": 412.8, "FY2016": 616.5, "FY2015": 616.5, "FY2014": 616.5}),
    ("DATA", "Capital reorganisation reserve", {"FY2016": -1311.6, "FY2015": -1311.6, "FY2014": -1311.6}),
    ("DATA", "Capital reserve", {"FY2016": 410.0, "FY2015": 410.0, "FY2014": 410.0}),
    ("DATA", "Retained profits", {"FY2025": 1398.4, "FY2024": 1164.9, "FY2023": 1261.1, "FY2022": 1207.7, "FY2021": 1174.1, "FY2020": 1045.7, "FY2019": 1201.9, "FY2018": 1175.7, "FY2017": 1300.6, "FY2016": 1173.7, "FY2015": 1045.9, "FY2014": 949.0}),
    ("DATA", "Fair value reserve / Available-for-sale reserve", {"FY2025": -6.2, "FY2024": -8.0, "FY2023": -6.5, "FY2022": -6.1, "FY2021": 11.1, "FY2020": 11.6, "FY2019": 13.6, "FY2018": 18.6, "FY2017": 18.7, "FY2016": 5.9, "FY2015": 16.3, "FY2014": 0.4}),
    ("DATA", "Cash flow hedging reserve", {"FY2025": 8.0, "FY2024": 26.0, "FY2023": 12.2, "FY2022": 40.4, "FY2021": -6.6, "FY2020": -20.2, "FY2019": -2.5, "FY2018": -3.2, "FY2017": -0.5, "FY2016": 0.4, "FY2015": -0.9}),
    ("TOTAL", "Total equity", {"FY2025": 2338.0, "FY2024": 2120.7, "FY2023": 1954.6, "FY2022": 1929.8, "FY2021": 1866.4, "FY2020": 1724.9, "FY2019": 1900.8, "FY2018": 1878.9, "FY2017": 2006.6, "FY2016": 1865.0, "FY2015": 1746.3, "FY2014": 1634.4}),
    ("TOTAL", "Total equity and liabilities", {"FY2025": 45281.5, "FY2024": 46099.1, "FY2023": 47652.9, "FY2022": 49449.6, "FY2021": 46705.6, "FY2020": 42422.4, "FY2019": 39535.9, "FY2018": 41138.6, "FY2017": 42536.7, "FY2016": 37195.7, "FY2015": 31618.0, "FY2014": 27171.4}),
]

bw.add_balance_sheet_sheet(
    title="TSB Bank plc — Consolidated Balance Sheet",
    subtitle="Bank (Consolidated) basis, £ million. Total equity ties exactly to the Statement of Changes in "
              "Equity sheet for every year.",
    rows=balance_sheet_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=76,
    source_height=230,
    unit_suffix=" (£m)",
)

# ---------------------------------------------------------------
# Profit & Loss (Consolidated Statement of Comprehensive Income)
# ---------------------------------------------------------------
income_statement_rows = [
    ("SECTION", "Interest and similar income", {}),
    ("DATA", "Interest income calculated using the effective interest method", {"FY2025": 1846.4, "FY2024": 1803.9, "FY2023": 1573.5, "FY2022": 1123.0, "FY2021": 946.4, "FY2020": 922.0, "FY2019": 1050.6}),
    ("DATA", "Other interest income", {"FY2025": 129.3, "FY2024": 273.5, "FY2023": 368.6, "FY2022": 108.7, "FY2021": -35.0, "FY2020": -41.0, "FY2019": -5.8}),
    ("TOTAL", "Total interest and similar income", {"FY2025": 1975.7, "FY2024": 2077.4, "FY2023": 1942.1, "FY2022": 1231.7, "FY2021": 911.4, "FY2020": 881.0, "FY2019": 1044.8, "FY2018": 1070.2, "FY2017": 1080.6, "FY2016": 1097.7, "FY2015": 967.2, "FY2014": 979.1}),
    ("DATA", "Interest and similar expense", {"FY2025": -920.1, "FY2024": -1093.0, "FY2023": -920.1, "FY2022": -250.0, "FY2021": -42.5, "FY2020": -94.6, "FY2019": -203.7, "FY2018": -185.4, "FY2017": -175.3, "FY2016": -243.9, "FY2015": -201.9, "FY2014": -220.9}),
    ("TOTAL", "Net interest income", {"FY2025": 1055.6, "FY2024": 984.4, "FY2023": 1022.0, "FY2022": 981.7, "FY2021": 868.9, "FY2020": 786.4, "FY2019": 841.1, "FY2018": 884.8, "FY2017": 925.9, "FY2016": 853.8, "FY2015": 765.3, "FY2014": 758.2}),
    ("DATA", "Fee and commission income", {"FY2025": 114.1, "FY2024": 124.7, "FY2023": 129.2, "FY2022": 135.5, "FY2021": 121.8, "FY2020": 122.4, "FY2019": 159.8, "FY2018": 122.1, "FY2017": 193.3, "FY2016": 197.5, "FY2015": 198.8, "FY2014": 208.6}),
    ("DATA", "Fee and commission expense", {"FY2025": -37.4, "FY2024": -34.0, "FY2023": -21.2, "FY2022": -21.3, "FY2021": -18.2, "FY2020": -36.5, "FY2019": -41.5, "FY2018": -46.7, "FY2017": -109.6, "FY2016": -97.3, "FY2015": -81.8, "FY2014": -70.4}),
    ("TOTAL", "Net fee and commission income", {"FY2025": 76.7, "FY2024": 90.7, "FY2023": 108.0, "FY2022": 114.2, "FY2021": 103.6, "FY2020": 85.9, "FY2019": 118.3, "FY2018": 75.4, "FY2017": 83.7, "FY2016": 100.2, "FY2015": 117.0, "FY2014": 138.2}),
    ("SECTION", "Other income", {}),
    ("DATA", "Gains on derecognition of financial assets measured at amortised cost", {"FY2025": 2.8}),
    ("DATA", "Gains on derecognition of financial assets measured at FVOCI", {"FY2023": 4.3, "FY2022": 6.3, "FY2021": 7.0, "FY2020": 21.8, "FY2019": 24.6}),
    ("DATA", "Gains on derecognition of financial assets measured at amortised cost / available-for-sale (FY2018 presentation)", {"FY2018": 0}),
    ("DATA", "Gains on derecognition of available-for-sale financial assets (pre-IFRS 9 presentation)", {"FY2017": 49.8, "FY2016": 0, "FY2015": 0, "FY2014": 0}),
    ("DATA", "Losses on derecognition of financial liabilities measured at amortised cost", {"FY2023": -1.0}),
    ("DATA", "Gains on financial assets designated at fair value through profit or loss", {"FY2018": 1.4, "FY2017": 0.1}),
    ("DATA", "Gains/(losses) on derivative financial instruments at fair value through profit or loss", {"FY2025": 40.5, "FY2024": 57.6, "FY2023": 11.2, "FY2022": -8.1}),
    ("DATA", "Losses on derivative financial assets at fair value through profit or loss", {"FY2021": -2.5, "FY2020": -1.3, "FY2019": -15.3}),
    ("DATA", "Losses on financial assets and liabilities held for trading (FY2017/18 presentation)", {"FY2018": -31.8, "FY2017": -14.0}),
    ("DATA", "(Losses)/gains from hedge accounting", {"FY2025": -34.2, "FY2024": -30.1, "FY2023": -2.2, "FY2022": 4.2, "FY2021": -2.4, "FY2020": 5.8, "FY2019": 20.8, "FY2018": 23.3, "FY2017": 24.5}),
    ("DATA", "Gains/(losses) on derecognition of non-financial assets/liabilities", {"FY2025": 0.5, "FY2024": -2.3, "FY2023": -0.1, "FY2022": 0.6, "FY2021": -2.6, "FY2020": -3.5, "FY2019": -3.5, "FY2018": 1.1, "FY2017": 5.8}),
    ("DATA", "Migration related income from LBG", {"FY2018": 318.3}),
    ("DATA", "Other operating income", {"FY2025": 30.4, "FY2024": 36.7, "FY2023": 14.5, "FY2022": 6.6, "FY2021": 10.9, "FY2020": 37.8, "FY2019": 1.2, "FY2018": 1.4, "FY2017": 1.6, "FY2016": 50.0, "FY2015": 8.4, "FY2014": 3.8}),
    ("TOTAL", "Other income", {"FY2025": 116.7, "FY2024": 152.6, "FY2023": 134.7, "FY2022": 123.8, "FY2021": 114.0, "FY2020": 146.5, "FY2019": 146.1, "FY2018": 410.5, "FY2017": 190.8, "FY2016": 150.2, "FY2015": 125.4, "FY2014": 142.0}),
    ("TOTAL", "Total income", {"FY2025": 1172.3, "FY2024": 1137.0, "FY2023": 1156.7, "FY2022": 1105.5, "FY2021": 982.9, "FY2020": 932.9, "FY2019": 987.2, "FY2018": 1295.3, "FY2017": 1096.1, "FY2016": 1004.0, "FY2015": 890.7, "FY2014": 900.2}),
    ("DATA", "Costs of preparing for migration", {"FY2018": -417.3}),
    ("DATA", "Defined benefit pension scheme settlement gain (within FY2014 operating expenses)", {"FY2014": 63.7}),
    ("TOTAL", "Total operating expenses", {"FY2025": -785.9, "FY2024": -821.8, "FY2023": -852.9, "FY2022": -869.5, "FY2021": -827.3, "FY2020": -969.4, "FY2019": -881.3, "FY2018": -905.7, "FY2017": -859.2, "FY2016": -734.7, "FY2015": -740.8, "FY2014": -632.4}),
    ("TOTAL", "Operating profit/(loss) before impairment losses and taxation", {"FY2025": 386.4, "FY2024": 315.2, "FY2023": 303.8, "FY2022": 236.0, "FY2021": 155.6, "FY2020": -36.5, "FY2019": 105.9, "FY2018": -27.7, "FY2017": 236.9, "FY2016": 269.3, "FY2015": 149.9, "FY2014": 267.8}),
    ("DATA", "Impairment losses on financial assets at amortised cost / loans and advances to customers", {"FY2025": -51.2, "FY2024": -31.9, "FY2023": -71.8, "FY2022": -57.7, "FY2021": -2.6, "FY2020": -162.7, "FY2019": -60.9, "FY2018": -72.8, "FY2017": -77.8, "FY2016": -87.3, "FY2015": -82.3, "FY2014": -97.6}),
    ("DATA", "Impairment credit/(losses) on loan commitments", {"FY2025": 4.2, "FY2024": 1.8, "FY2023": 3.5, "FY2022": 2.8, "FY2021": 2.5, "FY2020": -1.3, "FY2019": 0.4, "FY2018": -0.5}),
    ("TOTAL", "Total impairment losses", {"FY2025": -47.0, "FY2024": -30.1, "FY2023": -68.3, "FY2022": -54.9, "FY2021": -0.1, "FY2020": -164.0, "FY2019": -60.5, "FY2018": -73.3}),
    ("TOTAL", "Profit/(loss) before taxation", {"FY2025": 339.4, "FY2024": 285.1, "FY2023": 235.5, "FY2022": 181.1, "FY2021": 155.5, "FY2020": -200.5, "FY2019": 45.4, "FY2018": -101.0, "FY2017": 159.1, "FY2016": 182.0, "FY2015": 67.6, "FY2014": 170.2}),
    ("DATA", "Taxation", {"FY2025": -88.3, "FY2024": -81.3, "FY2023": -62.1, "FY2022": -80.5, "FY2021": -27.1, "FY2020": 44.3, "FY2019": -19.2, "FY2018": 41.9, "FY2017": -44.0, "FY2016": -54.2, "FY2015": 21.2, "FY2014": -35.7}),
    ("TOTAL", "Profit/(loss) for the year", {"FY2025": 251.1, "FY2024": 203.8, "FY2023": 173.4, "FY2022": 100.6, "FY2021": 128.4, "FY2020": -156.2, "FY2019": 26.2, "FY2018": -59.1, "FY2017": 115.1, "FY2016": 127.8, "FY2015": 88.8, "FY2014": 134.5}),
    ("SECTION", "Other comprehensive income/(loss), net of taxation", {}),
    ("DATA", "Change in fair value reserve / available-for-sale reserve", {"FY2025": 1.8, "FY2024": -1.5, "FY2023": -0.4, "FY2022": -17.2, "FY2021": -0.5, "FY2020": -2.0, "FY2019": -5.0, "FY2018": 1.7, "FY2017": 12.8, "FY2016": -10.4, "FY2015": 15.9, "FY2014": 0.4}),
    ("DATA", "Change in cash flow hedging reserve", {"FY2025": -18.0, "FY2024": 13.8, "FY2023": -28.2, "FY2022": 47.0, "FY2021": 13.6, "FY2020": -17.7, "FY2019": 0.7, "FY2018": -2.7, "FY2017": -0.9, "FY2016": 1.3, "FY2015": -0.9}),
    ("TOTAL", "Other comprehensive income/(losses) for the year, net of taxation", {"FY2025": -16.2, "FY2024": 12.3, "FY2023": -28.6, "FY2022": 29.8, "FY2021": 13.1, "FY2020": -19.7, "FY2019": -4.3, "FY2018": -1.0, "FY2017": 11.9, "FY2016": -9.1, "FY2015": 15.0, "FY2014": 0.4}),
    ("TOTAL", "Total comprehensive income/(loss) for the year", {"FY2025": 234.9, "FY2024": 216.1, "FY2023": 144.8, "FY2022": 130.4, "FY2021": 141.5, "FY2020": -175.9, "FY2019": 21.9, "FY2018": -60.1, "FY2017": 127.0, "FY2016": 118.7, "FY2015": 103.8, "FY2014": 134.9}),
]

bw.add_income_statement_sheet(
    title="TSB Bank plc — Consolidated Statement of Comprehensive Income",
    subtitle="Bank (Consolidated) basis, £ million. 'Total comprehensive income/(loss) for the year' ties exactly "
              "to Profit for the year + Other comprehensive income for every year.",
    rows=income_statement_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=76,
    source_height=230,
    unit_suffix=" (£m)",
)

# ---------------------------------------------------------------
# Statement of Changes in Equity - equity reconciliation ladder steps 2-3:
# built year-by-year, confirmed against next year's opening AND that year's
# own Balance Sheet Total equity above (all 5 years tie exactly, including
# the FY2024 AT1 issuance and FY2025 AT1 distribution - two easy-to-skip
# movement categories deliberately checked for). Zero undocumented plug rows.
# ---------------------------------------------------------------
EQUITY_HEADERS = [
    "Share capital", "Share premium", "Other equity instruments", "Merger reserve",
    "Capital reorg. reserve", "Capital reserve",
    "Fair value / AFS reserve", "Cash flow hedging reserve", "Retained profit", "Total equity",
]

equity_rows = [
    # --- FY2014-FY2016: TSB Banking Group plc entity (see ENTITY NOTE) ---
    ("TOTAL", "Balance at 1 January 2014", (0.1, None, None, None, 74.9, 410.0, None, None, 821.7, 1306.7)),
    ("DATA", "Profit for the year", (None, None, None, None, None, None, None, None, 134.5, 134.5)),
    ("DATA", "Change in available-for-sale reserve", (None, None, None, None, None, None, 0.4, None, None, 0.4)),
    ("DATA", "Insertion of parent company (2013 demerger completion)", (0.5, 769.5, None, 616.5, -1386.5, None, None, None, None, 0)),
    ("DATA", "Issue of new shares", (4.4, 195.6, None, None, None, None, None, None, None, 200.0)),
    ("DATA", "Movement in shares held by trusts", (None, None, None, None, None, None, None, None, -9.1, -9.1)),
    ("DATA", "Value of partner services", (None, None, None, None, None, None, None, None, 1.9, 1.9)),
    ("TOTAL", "Balance at 31 December 2014", (5.0, 965.1, None, 616.5, -1311.6, 410.0, 0.4, None, 949.0, 1634.4)),
    ("DATA", "Profit for the year", (None, None, None, None, None, None, None, None, 88.8, 88.8)),
    ("DATA", "Change in available-for-sale reserve", (None, None, None, None, None, None, 15.9, None, None, 15.9)),
    ("DATA", "Change in cash flow hedging reserve", (None, None, None, None, None, None, None, -0.9, None, -0.9)),
    ("DATA", "Movement in shares held by trusts", (None, None, None, None, None, None, None, None, 9.1, 9.1)),
    ("DATA", "Reclassification of equity settled share schemes to cash settled", (None, None, None, None, None, None, None, None, -3.1, -3.1)),
    ("DATA", "Value of partner services", (None, None, None, None, None, None, None, None, 2.1, 2.1)),
    ("TOTAL", "Balance at 31 December 2015", (5.0, 965.1, None, 616.5, -1311.6, 410.0, 16.3, -0.9, 1045.9, 1746.3)),
    ("DATA", "Profit for the year", (None, None, None, None, None, None, None, None, 127.8, 127.8)),
    ("DATA", "Change in available-for-sale reserve", (None, None, None, None, None, None, -10.4, None, None, -10.4)),
    ("DATA", "Change in cash flow hedging reserve", (None, None, None, None, None, None, None, 1.3, None, 1.3)),
    ("TOTAL", "Balance at 31 December 2016", (5.0, 965.1, None, 616.5, -1311.6, 410.0, 5.9, 0.4, 1173.7, 1865.0)),
    # --- FY2017 onward: TSB Bank plc entity (see ENTITY NOTE for the ~£14.6m FY2016/FY2017 entity-basis break) ---
    ("TOTAL", "Balance at 1 January 2017 (TSB Bank plc entity basis)", (79.4, 195.6, None, 412.8, None, None, 5.9, 0.4, 1185.5, 1879.6)),
    ("DATA", "Profit for the year", (None, None, None, None, None, None, None, None, 115.1, 115.1)),
    ("DATA", "Change in available-for-sale reserve", (None, None, None, None, None, None, 12.8, None, None, 12.8)),
    ("DATA", "Change in cash flow hedging reserve", (None, None, None, None, None, None, None, -0.9, None, -0.9)),
    ("TOTAL", "Balance at 31 December 2017", (79.4, 195.6, None, 412.8, None, None, 18.7, -0.5, 1300.6, 2006.6)),
    ("DATA", "Change on initial application of IFRS 9 (available-for-sale reserve 18.7 replaced by fair value reserve 16.9; both use the merged column here)", (None, None, None, None, None, None, -1.8, None, -70.1, -71.9)),
    ("DATA", "Change on initial application of IFRS 15", (None, None, None, None, None, None, None, None, 4.3, 4.3)),
    ("TOTAL", "Balance at 1 January 2018", (79.4, 195.6, None, 412.8, None, None, 16.9, -0.5, 1234.8, 1939.0)),
    ("DATA", "Loss for the year", (None, None, None, None, None, None, None, None, -59.1, -59.1)),
    ("DATA", "Change in fair value reserve", (None, None, None, None, None, None, 1.7, None, None, 1.7)),
    ("DATA", "Change in cash flow hedging reserve", (None, None, None, None, None, None, None, -2.7, None, -2.7)),
    ("TOTAL", "Balance at 31 December 2018", (79.4, 195.6, None, 412.8, None, None, 18.6, -3.2, 1175.7, 1878.9)),
    ("DATA", "Profit for the year", (None, None, None, None, None, None, None, None, 26.2, 26.2)),
    ("DATA", "Change in fair value reserve", (None, None, None, None, None, None, -5.0, None, None, -5.0)),
    ("DATA", "Change in cash flow hedging reserve", (None, None, None, None, None, None, None, 0.7, None, 0.7)),
    ("TOTAL", "Balance at 31 December 2019", (79.4, 195.6, None, 412.8, None, None, 13.6, -2.5, 1201.9, 1900.8)),
    ("DATA", "Loss for the year", (None, None, None, None, None, None, None, None, -156.2, -156.2)),
    ("DATA", "Change in fair value reserve", (None, None, None, None, None, None, -2.0, None, None, -2.0)),
    ("DATA", "Change in cash flow hedging reserve", (None, None, None, None, None, None, None, -17.7, None, -17.7)),
    ("TOTAL", "Balance at 31 December 2020", (79.4, 195.6, None, 412.8, None, None, 11.6, -20.2, 1045.7, 1724.9)),
    ("TOTAL", "Balance at 1 January 2021", (79.4, 195.6, None, 412.8, None, None, 11.6, -20.2, 1045.7, 1724.9)),
    ("DATA", "Profit for the year", (None, None, None, None, None, None, None, None, 128.4, 128.4)),
    ("DATA", "Change in fair value reserve", (None, None, None, None, None, None, -0.5, None, None, -0.5)),
    ("DATA", "Change in cash flow hedging reserve", (None, None, None, None, None, None, None, 13.6, None, 13.6)),
    ("TOTAL", "Balance at 31 December 2021", (79.4, 195.6, None, 412.8, None, None, 11.1, -6.6, 1174.1, 1866.4)),
    ("DATA", "Profit for the year", (None, None, None, None, None, None, None, None, 100.6, 100.6)),
    ("DATA", "Change in fair value reserve", (None, None, None, None, None, None, -17.2, None, None, -17.2)),
    ("DATA", "Change in cash flow hedging reserve", (None, None, None, None, None, None, None, 47.0, None, 47.0)),
    ("DATA", "Dividend paid", (None, None, None, None, None, None, None, None, -67.0, -67.0)),
    ("TOTAL", "Balance at 31 December 2022", (79.4, 195.6, None, 412.8, None, None, -6.1, 40.4, 1207.7, 1929.8)),
    ("DATA", "Profit for the year", (None, None, None, None, None, None, None, None, 173.4, 173.4)),
    ("DATA", "Change in fair value reserve", (None, None, None, None, None, None, -0.4, None, None, -0.4)),
    ("DATA", "Change in cash flow hedging reserve", (None, None, None, None, None, None, None, -28.2, None, -28.2)),
    ("DATA", "Dividend paid", (None, None, None, None, None, None, None, None, -120.0, -120.0)),
    ("TOTAL", "Balance at 31 December 2023", (79.4, 195.6, None, 412.8, None, None, -6.5, 12.2, 1261.1, 1954.6)),
    ("DATA", "Profit for the year", (None, None, None, None, None, None, None, None, 203.8, 203.8)),
    ("DATA", "Change in fair value reserve", (None, None, None, None, None, None, -1.5, None, None, -1.5)),
    ("DATA", "Change in cash flow hedging reserve", (None, None, None, None, None, None, None, 13.8, None, 13.8)),
    ("DATA", "Issue of Additional Tier 1 Securities", (None, None, 250.0, None, None, None, None, None, None, 250.0)),
    ("DATA", "Dividends paid on ordinary shares", (None, None, None, None, None, None, None, None, -300.0, -300.0)),
    ("TOTAL", "Balance at 31 December 2024", (79.4, 195.6, 250.0, 412.8, None, None, -8.0, 26.0, 1164.9, 2120.7)),
    ("DATA", "Profit for the year", (None, None, None, None, None, None, None, None, 251.1, 251.1)),
    ("DATA", "Change in fair value reserve", (None, None, None, None, None, None, 1.8, None, None, 1.8)),
    ("DATA", "Change in cash flow hedging reserve", (None, None, None, None, None, None, None, -18.0, None, -18.0)),
    ("DATA", "Distributions on other equity instruments", (None, None, None, None, None, None, None, None, -17.6, -17.6)),
    ("TOTAL", "Balance at 31 December 2025", (79.4, 195.6, 250.0, 412.8, None, None, -6.2, 8.0, 1398.4, 2338.0)),
]

bw.add_equity_changes_sheet(
    title="TSB Bank plc — Statement of Changes in Equity",
    subtitle="Bank (Consolidated) basis, £ million, chronological (oldest to newest). Each year's closing Total "
              "equity ties exactly to that year's own Balance Sheet Total equity and to the next year's opening "
              "balance - zero undocumented plug rows across all 5 years.",
    headers=EQUITY_HEADERS,
    rows=equity_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=50,
    source_height=230,
)

# ---------------------------------------------------------------
# Sheet: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Cash flows from operating activities", {}),
    ("DATA", "Profit/(loss) before taxation", {"FY2025": 339.4, "FY2024": 285.1, "FY2023": 235.5, "FY2022": 181.1, "FY2021": 155.5, "FY2020": -200.5, "FY2019": 45.4, "FY2018": -101.0, "FY2017": 159.1, "FY2016": 182.0, "FY2015": 67.6, "FY2014": 170.2}),
    ("DATA", "Decrease in loans to central banks", {"FY2025": 0, "FY2024": 136.0}),
    ("DATA", "Increase in loans to central banks (FY2019-20 presentation)", {"FY2020": -24.8, "FY2019": -8.3}),
    ("DATA", "Increase in loans to central banks (FY2021 presentation)", {"FY2021": -22.7}),
    ("DATA", "(Increase)/decrease in loans to credit institutions", {"FY2021": -12.8}),
    ("DATA", "Decrease/(increase) in loans to credit institutions (FY2019-20 presentation)", {"FY2020": 329.9, "FY2019": -2.6}),
    ("DATA", "Decrease/(increase) in loans and advances to customers", {"FY2025": -1.4, "FY2024": -124.6, "FY2023": 1719.2, "FY2022": -722.5, "FY2021": -4070.2, "FY2020": -2402.4, "FY2019": -1132.8}),
    ("DATA", "Change in operating assets (as reported, FY2014-FY2018 presentation)", {"FY2018": 1194.6, "FY2017": -1482.9, "FY2016": -3920.6, "FY2015": -2270.5, "FY2014": 5697.6}),
    ("DATA", "Change in operating liabilities (as reported, FY2014-FY2018 presentation)", {"FY2018": -1557.8, "FY2017": 1173.8, "FY2016": 3990.2, "FY2015": 1478.1, "FY2014": 1568.5}),
    ("DATA", "Increase in reverse repurchase agreements", {"FY2025": -62.0, "FY2024": 0}),
    ("DATA", "Decrease in reverse purchase agreements (FY2021 presentation)", {"FY2021": 0}),
    ("DATA", "Decrease/(increase) in reverse purchase agreements (FY2019-20 presentation)", {"FY2020": 201.1, "FY2019": -201.1}),
    ("DATA", "Decrease/(increase) in other advances", {"FY2025": 63.3, "FY2024": 79.3, "FY2023": 493.6, "FY2022": -622.6, "FY2021": 136.8, "FY2020": 62.1, "FY2019": 101.8}),
    ("DATA", "Net change in derivative financial instruments and FV adjustments for portfolio hedged risk (within operating assets/liabilities - FY2021/22 as originally presented)", {"FY2022": -63.1, "FY2021": -147.6}),
    ("DATA", "Net change in derivative financial instruments and FV adjustments for portfolio hedged risk (within operating assets/liabilities - FY2019/20 as originally presented)", {"FY2020": -216.0, "FY2019": -161.7}),
    ("DATA", "Decrease/(increase) in other assets", {"FY2025": 11.2, "FY2024": 2.0, "FY2023": -6.5, "FY2022": 72.4, "FY2021": 18.6, "FY2020": -25.4, "FY2019": 52.3}),
    ("DATA", "(Decrease)/increase in deposits from credit institutions (FY2021 presentation)", {"FY2021": 0}),
    ("DATA", "Increase/(decrease) in deposits from credit institutions (FY2019-20 presentation)", {"FY2020": 4.2, "FY2019": -2.7}),
    ("DATA", "Increase/(decrease) in customer deposits", {"FY2025": 176.0, "FY2024": 280.8, "FY2023": -1666.5, "FY2022": 357.0, "FY2021": 1591.2, "FY2020": 4217.0, "FY2019": 1089.9}),
    ("DATA", "(Decrease)/increase in other financial liabilities", {"FY2025": -148.8, "FY2024": -91.9, "FY2023": -156.4, "FY2022": 1126.5, "FY2021": 141.9, "FY2020": -33.3, "FY2019": 13.6}),
    ("DATA", "(Decrease)/increase in provisions", {"FY2025": -13.4, "FY2024": -33.5, "FY2023": -46.5, "FY2022": 17.6, "FY2021": -40.4, "FY2020": 101.3, "FY2019": -11.8}),
    ("DATA", "Increase/(decrease) in other liabilities", {"FY2025": 16.4, "FY2024": -3.3, "FY2023": -11.6, "FY2022": -25.4, "FY2021": 0.7, "FY2020": 41.9, "FY2019": -332.9}),
    ("TOTAL", "Change in operating assets and liabilities (as reported)", {"FY2025": 41.3, "FY2024": 244.8, "FY2023": 333.6, "FY2022": 202.3, "FY2021": -2404.5, "FY2020": 2255.6, "FY2019": -596.3}),
    ("DATA", "Interest expense on financing activities", {"FY2025": 291.1, "FY2024": 402.3, "FY2023": 398.8, "FY2022": 160.0}),
    ("DATA", "Interest income on investing activities", {"FY2025": -63.4, "FY2024": -63.2, "FY2023": -60.0, "FY2022": -33.2}),
    ("DATA", "Net change in derivative financial instruments and FV adjustments for portfolio hedged risk (within non-cash items - FY2023 onward presentation)", {"FY2025": 127.1, "FY2024": 259.6, "FY2023": 147.6}),
    ("DATA", "Depreciation and amortisation", {"FY2025": 63.4, "FY2024": 72.5, "FY2023": 67.0, "FY2022": 66.0, "FY2021": 70.2, "FY2020": 74.3, "FY2019": 60.2}),
    ("DATA", "Net movement in allowance for credit impairment losses", {"FY2025": -8.9, "FY2024": -31.7}),
    ("DATA", "Impairment losses on loans and advances to customers (FY2021-23 presentation)", {"FY2023": 13.8, "FY2022": 57.8, "FY2021": 2.6}),
    ("DATA", "Impairment losses on loans and advances to customers (FY2019-20 presentation)", {"FY2020": 162.7, "FY2019": 60.9}),
    ("DATA", "Exchange differences", {"FY2021": 0, "FY2020": 13.7, "FY2019": -20.5}),
    ("DATA", "Other non-cash items", {"FY2025": -48.8, "FY2024": -115.5, "FY2023": 97.4, "FY2022": -64.2, "FY2021": 39.2, "FY2020": 13.9, "FY2019": 69.5, "FY2018": 152.4, "FY2017": 116.4, "FY2016": 76.2, "FY2015": 142.1, "FY2014": 41.1}),
    ("TOTAL", "Non-cash and other items (as reported)", {"FY2025": 360.5, "FY2024": 524.0, "FY2023": 664.6, "FY2022": 247.4, "FY2021": 112.0, "FY2020": 264.6, "FY2019": 170.1}),
    ("DATA", "Taxation paid", {"FY2025": -78.8, "FY2024": -57.0, "FY2023": -33.0, "FY2022": -34.4, "FY2021": -8.7, "FY2020": 0, "FY2019": 20.5, "FY2018": -7.0, "FY2017": -25.5, "FY2016": -8.7, "FY2015": -8.5, "FY2014": -3.7}),
    ("TOTAL", "Net cash (used in)/provided by operating activities", {"FY2025": 662.4, "FY2024": 996.9, "FY2023": 1200.7, "FY2022": 596.4, "FY2021": -2145.7, "FY2020": 2319.7, "FY2019": -360.3, "FY2018": -318.8, "FY2017": -59.1, "FY2016": 319.1, "FY2015": -591.2, "FY2014": 7473.7}),
    ("SECTION", "Cash flows from investing activities", {}),
    ("DATA", "Purchase of property and equipment", {"FY2025": -18.3, "FY2024": -22.2, "FY2023": -20.2, "FY2022": -36.8, "FY2021": -44.5, "FY2020": -30.2, "FY2019": -18.0, "FY2018": -15.8, "FY2017": -15.8, "FY2016": -35.9, "FY2015": -39.7, "FY2014": -85.8}),
    ("DATA", "Purchase and development of intangible assets", {"FY2025": -38.4, "FY2024": -41.8, "FY2023": -28.0, "FY2022": -17.5, "FY2021": -30.3, "FY2020": -35.9, "FY2019": -7.6}),
    ("DATA", "Purchase of financial assets (FY2014-FY2018 presentation)", {"FY2018": -398.1, "FY2017": -62.9, "FY2016": -779.2, "FY2015": -3969.6, "FY2014": -3682.1}),
    ("DATA", "Interest received on financial assets (FY2014-FY2018 presentation)", {"FY2018": 76.6, "FY2017": 83.3, "FY2016": 53.7, "FY2015": 32.8}),
    ("DATA", "Proceeds on disposal of equity assets", {"FY2018": 9.2, "FY2016": 25.3}),
    ("DATA", "Maturity/(issue) of reverse repurchase agreements (FY2014-16 presentation)", {"FY2016": 20.3, "FY2015": -20.3}),
    ("DATA", "Interest received on reverse repurchase agreements", {"FY2018": 0.4, "FY2017": 0.4, "FY2016": 2.2}),
    ("DATA", "Purchase of Sabadell shares", {"FY2018": -0.9, "FY2017": -0.9, "FY2016": -5.2, "FY2015": -7.1}),
    ("DATA", "Disposal/(purchase) of shares held by trusts", {"FY2015": 7.6, "FY2014": -9.1}),
    ("DATA", "Purchase of debt securities", {"FY2025": -247.4, "FY2024": -124.7, "FY2023": -219.8, "FY2022": -580.1, "FY2021": -1324.5, "FY2020": -1341.3, "FY2019": -994.9}),
    ("DATA", "Sale of debt securities", {"FY2024": 0, "FY2023": 252.6, "FY2022": 442.6, "FY2021": 500.9, "FY2020": 977.8, "FY2019": 1424.3}),
    ("DATA", "Proceeds from maturing investments", {"FY2025": 169.3, "FY2024": 141.7, "FY2023": 39.3, "FY2022": 67.0, "FY2021": 23.0}),
    ("DATA", "Interest received on debt securities", {"FY2025": 67.6, "FY2024": 68.1, "FY2023": 64.6, "FY2022": 44.5, "FY2021": 36.3}),
    ("TOTAL", "Net cash (used in)/provided by investing activities", {"FY2025": -67.2, "FY2024": 21.1, "FY2023": 88.5, "FY2022": -80.3, "FY2021": -839.1, "FY2020": -429.6, "FY2019": 403.8, "FY2018": -328.6, "FY2017": 4.1, "FY2016": -718.8, "FY2015": -3996.3, "FY2014": -3777.0}),
    ("SECTION", "Cash flows from financing activities", {}),
    ("DATA", "Additional borrowings from central banks", {"FY2025": 5.0, "FY2024": 0, "FY2023": 5.0, "FY2022": 510.0, "FY2021": 5500.0}),
    ("DATA", "Proceeds from borrowings from central banks (FY2017-18 presentation)", {"FY2018": 850.0, "FY2017": 5615.0}),
    ("DATA", "Repayment of borrowing from central banks", {"FY2025": -797.0, "FY2024": -2620.0, "FY2023": -1500.0, "FY2022": -510.0, "FY2021": -3065.0, "FY2020": -1410.0, "FY2019": -1995.0}),
    ("DATA", "Repayment of debt securities in issue (incl. securitisation repayments, FY2017-FY2020 presentation)", {"FY2020": -440.2, "FY2019": -177.5, "FY2018": -197.9, "FY2017": -2128.4, "FY2016": -557.4}),
    ("DATA", "Proceeds from debt securities issued (FY2014-16 presentation)", {"FY2016": 553.7, "FY2015": 2873.7, "FY2014": 10.0}),
    ("DATA", "Interest paid on debt securities in issue (FY2017-18 presentation)", {"FY2018": -12.4, "FY2017": -13.4, "FY2016": -40.6, "FY2015": -0.3, "FY2014": -0.6}),
    ("DATA", "Repurchase of debt securities", {"FY2014": -0.8}),
    ("DATA", "Proceeds from subordinated liabilities issued", {"FY2014": 383.0}),
    ("DATA", "Interest paid on borrowings from central banks", {"FY2025": -46.2, "FY2024": -177.1, "FY2023": -191.7, "FY2022": -57.3, "FY2021": -7.8, "FY2018": -32.0, "FY2017": -6.4}),
    ("DATA", "Issue of covered bonds", {"FY2025": 495.5, "FY2024": 926.1, "FY2023": 1750.0, "FY2022": 0, "FY2019": 750.0}),
    ("DATA", "Repayment of covered bonds", {"FY2025": 0, "FY2024": -500.0}),
    ("DATA", "Buyback of covered bonds", {"FY2023": -251.0, "FY2022": -500.0}),
    ("DATA", "Interest paid on covered bonds", {"FY2025": -143.2, "FY2024": -144.4, "FY2023": -120.1, "FY2022": -29.5}),
    ("DATA", "Issue of securitisation notes", {"FY2025": 0, "FY2024": 498.3}),
    ("DATA", "Repayment of securitisation notes", {"FY2025": -20.0, "FY2024": -5.0}),
    ("DATA", "Interest paid on securitisation notes", {"FY2025": -24.2, "FY2024": -11.8}),
    ("DATA", "Issue of Additional Tier 1 securities", {"FY2025": 0, "FY2024": 249.7}),
    ("DATA", "Issue of senior unsecured debt securities", {"FY2024": 0, "FY2023": 200.0, "FY2022": 700.0, "FY2020": 450.0}),
    ("DATA", "Repayment of senior unsecured debt securities", {"FY2025": -250.0, "FY2024": 0, "FY2023": 0, "FY2022": -450.0}),
    ("DATA", "Interest paid on senior unsecured debt securities", {"FY2025": -65.3, "FY2024": -72.4, "FY2023": -51.1, "FY2022": -15.8}),
    ("DATA", "Issue of debt securities in issue (FY2021 presentation)", {"FY2021": 500.0}),
    ("DATA", "Interest paid on debt securities in issue (FY2021 presentation)", {"FY2021": -21.0}),
    ("DATA", "Issue of subordinated liabilities", {"FY2021": 300.0}),
    ("DATA", "Repayment of subordinated liabilities", {"FY2021": -385.0}),
    ("DATA", "Interest paid on subordinated liabilities", {"FY2025": -10.3, "FY2024": -10.3, "FY2023": -10.3, "FY2022": -10.3, "FY2021": -18.8, "FY2018": -22.4, "FY2017": -22.1, "FY2016": -22.1, "FY2015": -22.1, "FY2014": -11.4}),
    ("DATA", "Proceeds from shares issued", {"FY2014": 200.0}),
    ("DATA", "Proceeds from/(repayment of) repurchase agreements (FY2014-16 presentation)", {"FY2016": 1408.6, "FY2015": -32.5, "FY2014": 32.5}),
    ("DATA", "(Repayment)/issue of repurchase agreements", {"FY2023": -359.9, "FY2022": 359.9, "FY2018": -361.9, "FY2017": 36.9}),
    ("DATA", "Interest paid on repurchase agreements", {"FY2023": -1.0, "FY2022": -2.6, "FY2018": -3.5, "FY2017": -8.4, "FY2016": -9.5, "FY2015": -0.4}),
    ("DATA", "Net securitisation funding (FY2021 presentation)", {"FY2021": 0}),
    ("DATA", "Lease payments", {"FY2025": -16.2, "FY2024": -18.8, "FY2023": -17.8, "FY2022": -19.7, "FY2021": -22.8, "FY2020": -26.4, "FY2019": -38.8}),
    ("DATA", "Distributions on other equity instruments", {"FY2025": -17.6, "FY2024": 0}),
    ("DATA", "Dividends paid", {"FY2025": -300.0, "FY2024": -120.0, "FY2023": -50.0, "FY2022": 0}),
    ("TOTAL", "Net cash (used in)/provided by financing activities", {"FY2025": -1189.5, "FY2024": -2005.7, "FY2023": -597.9, "FY2022": -25.3, "FY2021": 2779.6, "FY2020": -1426.6, "FY2019": -2545.8, "FY2018": 219.9, "FY2017": 3970.7, "FY2016": 1332.7, "FY2015": 2818.4, "FY2014": 612.7}),
    ("TOTAL", "Change in cash and cash equivalents", {"FY2025": -594.3, "FY2024": -987.7, "FY2023": 691.3, "FY2022": 490.8, "FY2021": -205.2, "FY2020": 463.5, "FY2019": -2543.1, "FY2018": -427.5, "FY2017": 3915.7, "FY2016": 933.0, "FY2015": -1769.1, "FY2014": 4309.4}),
    ("DATA", "Cash and cash equivalents at 1 January", {"FY2025": 5101.6, "FY2024": 6089.3, "FY2023": 5398.0, "FY2022": 4907.2, "FY2021": 5056.3, "FY2020": 4592.8, "FY2019": 7135.9, "FY2018": 7563.4, "FY2017": 3647.7, "FY2016": 2714.7, "FY2015": 4483.8, "FY2014": 174.4}),
    ("TOTAL", "Cash and cash equivalents at 31 December", {"FY2025": 4507.3, "FY2024": 5101.6, "FY2023": 6089.3, "FY2022": 5398.0, "FY2021": 4851.1, "FY2020": 5056.3, "FY2019": 4592.8, "FY2018": 7135.9, "FY2017": 7563.4, "FY2016": 3647.7, "FY2015": 2714.7, "FY2014": 4483.8}),
]

bw.add_cash_flow_sheet(
    title="TSB Bank plc — Consolidated Cash Flow Statement",
    subtitle="Bank (Consolidated) basis, £ million unless stated. See source note at bottom (incl. an FY2021/FY2022 restatement break).",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=80,
    source_height=220,
    unit_suffix=" (£m)",
)

# ---------------------------------------------------------------
# Asset Quality - loan book by IFRS 9 stage. FY2022-FY2025 sourced from the
# 'Sensitivity to alternative economic scenario weightings' note's weighted
# gross customer lending balances/ECL table; FY2021 sourced from the fuller
# 'Reconciliation of movements in gross customer balances and allowances for
# credit impairment losses' table (a differently-scoped disclosure - see
# source note). Neither table ties exactly to the Balance Sheet's narrower
# 'Loans and advances to customers' net line (a documented, genuine
# cross-statement presentation difference, not forced to tie).
# ---------------------------------------------------------------
asset_quality_rows = [
    ("SECTION", "Gross customer lending balances by IFRS 9 stage (weighted forecast)", {}),
    ("DATA", "Stage 1", {"FY2025": 33038.7, "FY2024": 33151.6, "FY2023": 32115.9, "FY2022": 33737.1, "FY2021": 34280.5, "FY2020": 29753.5, "FY2019": 28181.7, "FY2018": 26732.5}),
    ("DATA", "Stage 2", {"FY2025": 2738.6, "FY2024": 2697.2, "FY2023": 3684.9, "FY2022": 3866.8, "FY2021": 2583.9, "FY2020": 3201.4, "FY2019": 2449.9, "FY2018": 2884.2}),
    ("DATA", "Stage 3 (non-performing)", {"FY2025": 525.7, "FY2024": 528.2, "FY2023": 508.1, "FY2022": 472.1, "FY2021": 502.4, "FY2020": 399.5, "FY2019": 382.5, "FY2018": 400.3}),
    ("DATA", "POCI (purchased or originated credit impaired)", {"FY2025": 73.2, "FY2024": 84.1, "FY2023": 94.9, "FY2022": 109.3, "FY2021": 124.8, "FY2020": 144.0, "FY2019": 161.3, "FY2018": 190.2}),
    ("DATA", "Impaired loans (IAS 39 basis, pre-IFRS 9 - broadly equivalent to Stage 3 above)", {"FY2017": 154.1, "FY2016": 140.0, "FY2015": 159.0, "FY2014": 205.0}),
    ("TOTAL", "Total gross customer lending balances", {"FY2025": 36376.2, "FY2024": 36461.1, "FY2023": 36403.8, "FY2022": 38185.3, "FY2021": 37491.6, "FY2020": 33498.4, "FY2019": 31175.4, "FY2018": 30207.2, "FY2017": 30925.8, "FY2016": 29492.8, "FY2015": 26473.4, "FY2014": 21727.5}),
    ("SECTION", "Allowance for credit losses and credit impairment provisions", {}),
    ("DATA", "Stage 1", {"FY2025": 34.1, "FY2024": 50.2, "FY2023": 60.5, "FY2022": 42.5, "FY2021": 59.0, "FY2020": 66.9, "FY2019": 52.3, "FY2018": 50.8}),
    ("DATA", "Stage 2", {"FY2025": 52.4, "FY2024": 57.7, "FY2023": 80.9, "FY2022": 103.2, "FY2021": 74.4, "FY2020": 119.2, "FY2019": 60.8, "FY2018": 69.7}),
    ("DATA", "Stage 3", {"FY2025": 86.5, "FY2024": 80.0, "FY2023": 79.8, "FY2022": 65.5, "FY2021": 55.4, "FY2020": 50.1, "FY2019": 47.7, "FY2018": 71.0}),
    ("DATA", "POCI", {"FY2025": 2.6, "FY2024": 0.8, "FY2023": 1.0, "FY2022": 0.7, "FY2021": 0.8, "FY2020": 2.8, "FY2019": 2.2, "FY2018": 7.2}),
    ("DATA", "Allowance for impairment losses (IAS 39 basis, pre-IFRS 9)", {"FY2017": 71.6, "FY2016": 73.7, "FY2015": 71.2, "FY2014": 86.1}),
    ("TOTAL", "Total allowance for credit losses and credit impairment provisions", {"FY2025": 175.6, "FY2024": 188.7, "FY2023": 222.2, "FY2022": 211.9, "FY2021": 189.6, "FY2020": 239.0, "FY2019": 163.0, "FY2018": 198.7, "FY2017": 71.6, "FY2016": 73.7, "FY2015": 71.2, "FY2014": 86.1}),
    ("SECTION", "Derived ratios", {}),
    ("DATA", "NPL / impaired ratio (Stage 3 or impaired gross / Total gross customer lending)", {"FY2025": "1.45%", "FY2024": "1.45%", "FY2023": "1.40%", "FY2022": "1.24%", "FY2021": "1.34%", "FY2020": "1.19%", "FY2019": "1.23%", "FY2018": "1.33%", "FY2017": "0.50%", "FY2016": "0.47%", "FY2015": "0.60%", "FY2014": "0.94%"}),
    ("DATA", "Stage 3 coverage ratio (Stage 3 allowance / Stage 3 gross) - not meaningful pre-IFRS 9", {"FY2025": "16.45%", "FY2024": "15.15%", "FY2023": "15.71%", "FY2022": "13.87%", "FY2021": "11.03%", "FY2020": "12.54%", "FY2019": "12.47%", "FY2018": "17.74%"}),
    ("DATA", "Total coverage ratio (Total allowance / Total gross)", {"FY2025": "0.48%", "FY2024": "0.52%", "FY2023": "0.61%", "FY2022": "0.55%", "FY2021": "0.51%", "FY2020": "0.71%", "FY2019": "0.52%", "FY2018": "0.66%", "FY2017": "0.23%", "FY2016": "0.25%", "FY2015": "0.27%", "FY2014": "0.40%"}),
]

bw.add_asset_quality_sheet(
    title="TSB Bank plc — Asset Quality",
    subtitle="Bank and Company, £ million. See source note for why this doesn't tie exactly to the Balance Sheet's "
              "Loans and advances to customers line, and for a FY2021 vs FY2022-25 disclosure-basis difference.",
    rows=asset_quality_rows,
    sources_text=(
        "Sources - Bank and Company basis, £ million:\n"
        f"FY2025: TSB Bank plc Annual Report and Accounts 2025, p.62 (Note 8, 'Sensitivity to alternative economic "
        f"scenario weightings', weighted column) - {AR25_URL}\n"
        f"FY2024: TSB Bank plc Annual Report and Accounts 2025, p.63 (Note 8, FY2024 comparative, weighted column) "
        f"- {AR25_URL}\n"
        f"FY2023: TSB Bank plc Annual Report and Accounts 2023, p.45 (Note 8, weighted column) - {AR23_URL}\n"
        f"FY2022: TSB Bank plc Annual Report and Accounts 2023, p.46 (Note 8, FY2022 comparative, weighted column) "
        f"- {AR23_URL}\n"
        f"FY2021: TSB Bank plc Annual Report and Accounts 2021, p.54 ('Reconciliation of movements in gross "
        f"customer balances and allowances for credit impairment losses', at 31 December 2021 closing row) "
        f"- {AR21_URL}\n"
        f"FY2020 & FY2019: TSB Bank plc Annual Report and Accounts 2020, p.38-39 (Note 9, 'Allowance for credit "
        f"impairment losses on financial assets at amortised cost', closing rows) - {AR20_URL}\n"
        f"FY2018 & FY2017 (as if IFRS 9): TSB Bank plc Annual Report and Accounts 2018, p.42 (Note 11, 'Allowance "
        f"for credit impairment losses on financial assets at amortised cost - IFRS 9', closing row) - {AR18_URL}\n"
        f"FY2017 (IAS 39, as originally reported) & FY2016: TSB Bank plc Annual Report and Accounts 2017, p.32-33 "
        f"(Note 9, 'Allowance for impairment losses on loans and receivables' and 'Credit quality of assets' "
        f"tables) - {AR17_URL}\n"
        f"FY2015 & FY2014: TSB Banking Group plc Annual Report and Accounts 2015, p.62-63 (Note 10, 'Allowance for "
        f"impairment losses on loans and receivables' and 'Credit quality of assets' tables) - {BG_AR15_URL}\n\n"
        "PRESENTATION NOTE: FY2022-FY2025 use the 'Sensitivity to alternative economic scenario weightings' note's "
        "weighted-forecast gross lending/ECL table (a narrower disclosure scope than the full 'Reconciliation of "
        "movements' table, which TSB stopped publishing after the 2021 Annual Report). FY2021-FY2018 use that "
        "older, fuller reconciliation table instead ('Note 9'/'Note 11: Allowance for credit impairment losses on "
        "financial assets at amortised cost') - a genuine disclosure-format change, not a data error. Neither "
        "table's Total gross/Total allowance figures tie exactly to the Balance Sheet's 'Loans and advances to "
        "customers' net line (a small gap, consistent in direction and rough magnitude across years, most likely "
        "reflecting a scope difference such as loan commitment provisions or accrued interest treated differently "
        "between the two disclosures) - reproduced faithfully from each source rather than forced to tie.\n\n"
        "IAS 39/IFRS 9 CAVEAT (FY2014-FY2017): TSB adopted IFRS 9 from 1 January 2018 (see the Statement of "
        "Changes in Equity sheet's 'Change on initial application of IFRS 9' transition row). FY2014-FY2017 predate "
        "IFRS 9 and use IAS 39's 'incurred loss' impairment model instead: loans are classified as 'neither past "
        "due nor impaired', 'past due but not impaired', or 'impaired' (no Stage 1/2/3/POCI concept existed), and "
        "the allowance is split into 'specific coverage (individual)', 'specific coverage (collective)' and "
        "'incurred but not reported (IBNR)' categories rather than by stage. The 'Impaired loans' row above is the "
        "closest IAS 39-era equivalent to the IFRS 9 'Stage 3' concept, and 'NPL / impaired ratio' is computed on "
        "the same basis for comparability across the full FY2014-FY2025 window; 'Stage 3 coverage ratio' has no "
        "equivalent IAS 39 breakdown and is left blank for FY2014-FY2017 rather than approximated.\n\n" + ENTITY_NOTE
    ),
    first_col_width=64,
    source_height=260,
    unit_suffix=" (£m)",
)


# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(
        name,
        unit,
        rows_data,
        sources_text,
        note=note,
        first_col_width=52,
        source_height=120,
    )


metric(
    "CET1 Capital",
    "£'000",
    [
        (
            "Common Equity Tier 1 (CET1) capital",
            {
                "FY2025": 1949276,
                "FY2024": 1738133,
                "FY2023": 1842646,
                "FY2022": 1791545,
                "FY2021": 1724002,
                "FY2020": 1630434,
                "FY2019": 1837943,
                "FY2018": 1805500,
                "FY2017": 1898100,
                "FY2016": 1785437,
                "FY2015": 1672458,
                "FY2014": 1593000,
            },
        )
    ],
    p3_sources("6"),
)

metric(
    "CET1 Ratio",
    "% of RWA",
    [
        (
            "Common Equity Tier 1 (CET1) ratio",
            {
                "FY2025": "16.74%",
                "FY2024": "15.45%",
                "FY2023": "16.7%",
                "FY2022": "17.2%",
                "FY2021": "15.9%",
                "FY2020": "15.3%",
                "FY2019": "20.8%",
                "FY2018": "19.5%",
                "FY2017": "20.0%",
                "FY2016": "18.5%",
                "FY2015": "17.8%",
                "FY2014": "23.0%",
            },
        )
    ],
    p3_sources("6"),
)

metric(
    "Tier 1 Capital",
    "£'000",
    [
        (
            "Tier 1 capital",
            {
                "FY2025": 2198973,
                "FY2024": 1987837,
                "FY2023": 1842646,
                "FY2022": 1791545,
                "FY2021": 1724002,
                "FY2020": 1630434,
                "FY2019": 1837943,
                "FY2018": 1805500,
                "FY2017": 1898100,
                "FY2016": 1785437,
                "FY2015": 1672458,
                "FY2014": 1593000,
            },
        )
    ],
    p3_sources("6"),
    note="Equal to CET1 capital for every year FY2014-FY2023 - TSB held no Additional Tier 1 (AT1) capital until "
    "it issued £249.7m of AT1 securities during FY2024 (see the Cash Flow Statement sheet), which is why Tier 1 "
    "capital first exceeds CET1 capital from FY2024 onward.",
)

metric(
    "Tier 1 Ratio",
    "% of RWA",
    [
        (
            "Tier 1 ratio",
            {
                "FY2025": "18.88%",
                "FY2024": "17.67%",
                "FY2023": "16.7%",
                "FY2022": "17.2%",
                "FY2021": "15.9%",
                "FY2020": "15.3%",
                "FY2019": "20.8%",
                "FY2018": "19.5%",
                "FY2017": "20.0%",
                "FY2016": "18.5%",
                "FY2015": "17.8%",
                "FY2014": "23.0%",
            },
        )
    ],
    p3_sources("6"),
)

metric(
    "Total Capital",
    "£'000",
    [
        (
            "Total capital",
            {
                "FY2025": 2498973,
                "FY2024": 2287837,
                "FY2023": 2167829,
                "FY2022": 2109761,
                "FY2021": 2024002,
                "FY2020": 2015339,
                "FY2019": 2222569,
                "FY2018": 2196100,
                "FY2017": 2282200,
                "FY2016": 2169371,
                "FY2015": 2055971,
                "FY2014": 1977300,
            },
        )
    ],
    p3_sources("6"),
)

metric(
    "Total Capital Ratio",
    "% of RWA",
    [
        (
            "Total capital ratio",
            {
                "FY2025": "21.46%",
                "FY2024": "20.33%",
                "FY2023": "19.6%",
                "FY2022": "20.2%",
                "FY2021": "18.7%",
                "FY2020": "18.9%",
                "FY2019": "25.1%",
                "FY2018": "23.7%",
                "FY2017": "24.0%",
                "FY2016": "22.4%",
                "FY2015": "21.9%",
                "FY2014": "28.5%",
            },
        )
    ],
    p3_sources("6"),
)

metric(
    "Total RWAs",
    "£'000",
    [
        (
            "Total risk-weighted exposure amount",
            {
                "FY2025": 11646331,
                "FY2024": 11250820,
                "FY2023": 11052751,
                "FY2022": 10442066,
                "FY2021": 10851867,
                "FY2020": 10644263,
                "FY2019": 8841425,
                "FY2018": 9271000,
                "FY2017": 9490700,
                "FY2016": 9674544,
                "FY2015": 9402364,
                "FY2014": 6930200,
            },
        )
    ],
    p3_sources("6"),
)

# ---------------------------------------------------------------
# RWA Breakdown - Pillar 3 UK OV1 template. All 5 years sourced from TSB
# Banking Group plc's own Large Subsidiary Disclosures (own-year figures
# cross-checked against the adjacent year's comparative column, which agrees
# exactly in every case). All 5 years tie exactly to the Total RWAs metric
# above.
# ---------------------------------------------------------------
rwa_breakdown_rows = [
    ("SECTION", "RWA by risk category (Pillar 3 UK OV1 template)", {}),
    ("DATA", "Credit risk (excluding counterparty credit risk)", {"FY2025": 9802107, "FY2024": 9417095, "FY2023": 9285021, "FY2022": 8781922, "FY2021": 9375601, "FY2020": 7584270, "FY2019": 7181081, "FY2016": 7796692, "FY2015": 7618079}),
    ("DATA", "Counterparty credit risk (CCR, incl. CVA)", {"FY2025": 34637, "FY2024": 44008, "FY2023": 47113, "FY2022": 107036, "FY2021": 17276, "FY2020": 17452, "FY2019": 48287, "FY2016": 206645, "FY2015": 52017}),
    ("DATA", "Operational risk", {"FY2025": 1725340, "FY2024": 1710925, "FY2023": 1633140, "FY2022": 1475213, "FY2021": 1400010, "FY2020": 1400392, "FY2019": 1484429, "FY2016": 1400642, "FY2015": 1416377}),
    ("DATA", "Amounts below the thresholds for deduction (subject to 250% risk weight)", {"FY2025": 84247, "FY2024": 78792, "FY2023": 87477, "FY2022": 77895, "FY2021": 58980, "FY2020": 50591, "FY2019": 127628, "FY2016": 270565, "FY2015": 315891}),
    ("DATA", "Credit risk, Standardised approach (FY2017-FY2018 presentation, incl. CCR)", {"FY2018": 7673500, "FY2017": 7907400}),
    ("DATA", "Counterparty credit risk (FY2017-FY2018 presentation, memo only - already included above)", {"FY2018": 109900, "FY2017": 119600}),
    ("DATA", "Operational risk (FY2017-FY2018 presentation)", {"FY2018": 1487600, "FY2017": 1463700}),
    ("DATA", "Credit risk (IRB approach, FY2014 presentation)", {"FY2014": 3187300}),
    ("DATA", "Credit risk (Standardised approach, FY2014 presentation)", {"FY2014": 2285400}),
    ("DATA", "Credit risk (CCP contribution, FY2014 presentation)", {"FY2014": 1000}),
    ("DATA", "Counterparty credit risk (FY2014 presentation, memo only - already included above)", {"FY2014": 4300}),
    ("DATA", "Credit valuation adjustment (CVA) risk (FY2014 presentation)", {"FY2014": 700}),
    ("DATA", "Operational risk (FY2014 presentation)", {"FY2014": 1451500}),
    ("TOTAL", "Total RWAs", {"FY2025": 11646331, "FY2024": 11250820, "FY2023": 11052751, "FY2022": 10442066, "FY2021": 10851867, "FY2020": 10644263, "FY2019": 8841425, "FY2018": 9271000, "FY2017": 9490700, "FY2016": 9674544, "FY2015": 9402364, "FY2014": 6930200}),
]

bw.add_rwa_breakdown_sheet(
    title="TSB Bank plc — RWA Breakdown",
    subtitle="TSB Banking Group plc consolidated Pillar 3 basis, £'000. FY2019-FY2025 and FY2015-FY2016 use the "
              "standard 4-row UK OV1 template, which sums exactly to Total RWAs; FY2017-FY2018 and FY2014 are shown "
              "on each year's own as-published, non-OV1-template category structure (memo rows do not double-count "
              "into the total - see PRESENTATION NOTE below).",
    rows=rwa_breakdown_rows,
    sources_text=(
        "Sources - TSB Banking Group plc consolidated Pillar 3 basis, UK OV1: Overview of risk-weighted exposure "
        "amounts (see entity note on Cash Flow Statement sheet):\n"
        f"FY2025: TSB Banking Group plc Large Subsidiary Disclosures, as at 31 December 2025, p.10 (Table 4: OV1) "
        f"- {P3_25_URL}\n"
        f"FY2024: TSB Banking Group plc Large Subsidiary Disclosures, as at 31 December 2024, p.12 (Table 5: OV1; "
        f"independently cross-checked against the FY2025 disclosure's own FY2024 comparative column, which agrees "
        f"exactly) - {P3_24_URL}\n"
        f"FY2023: TSB Banking Group plc Large Subsidiary Disclosures, as at 31 December 2024, p.12 (Table 5: OV1, "
        f"FY2023 comparative column) - {P3_24_URL}\n"
        f"FY2022: TSB Banking Group plc Large Subsidiary Disclosures 2022, p.12 (Table 5: OV1) - {P3_22_URL}\n"
        f"FY2021: TSB Banking Group plc Large Subsidiary Disclosures 2021, p.11 (Table 5: OV1; independently "
        f"cross-checked against the 2022 disclosure's own FY2021 comparative column, which agrees exactly) "
        f"- {P3_21_URL}\n"
        f"FY2020/FY2019: TSB Banking Group plc Large Subsidiary Disclosures, as at 31 December 2020, OV1 table "
        f"(FY2019 as its own comparative column) - {P3_20_URL}\n"
        f"FY2018: TSB Banking Group plc Annual Report and Accounts 2018, 'Capital resources' section - {BG_AR18_URL}\n"
        f"FY2017: TSB Banking Group plc Annual Report and Accounts 2017, 'Capital resources' section - {BG_AR17_URL}\n"
        f"FY2016: TSB Banking Group plc Large Subsidiary Disclosures, as at 31 December 2016, OV1 table (also "
        f"gives FY2015 as its own comparative column, used for the FY2015 figures here) - {P3_16_URL}\n"
        f"FY2015: as above (FY2016 disclosure's own FY2015 comparative column) - {P3_16_URL}\n"
        f"FY2014: TSB Banking Group plc Pillar 3 Disclosures 2014, Table 3 (own-year IRB/Standardised/CCP/CCR/CVA/"
        f"operational risk breakdown) - {P3_14_URL}\n\n"
        "PRESENTATION NOTE (FY2014, FY2017, FY2018): these three years predate the standardised UK OV1 template's "
        "4-category structure and are instead shown using each year's own as-published risk-category breakdown "
        "(FY2017/FY2018: Standardised-approach credit risk, CCR memo, operational risk from the Banking Group "
        "Annual Report's own 'Capital resources' table; FY2014: IRB + Standardised + CCP credit risk components, "
        "CCR memo, CVA risk, and operational risk from the Pillar 3 disclosure's own Table 3). In each of these "
        "three years the 'memo only' CCR row is already included within the adjacent credit-risk row(s) above it "
        "(exactly as each source document presents it) and is shown separately purely for transparency - it does "
        "not double count into Total RWAs, which still ties exactly to the Total RWAs metric sheet for every year."
    ),
    first_col_width=64,
    source_height=340,
    unit_suffix=" (£'000)",
)

metric(
    "Leverage Ratio",
    "£'000 / %",
    [
        (
            "Leverage ratio total exposure measure excluding claims on central banks",
            {
                "FY2025": 40220383,
                "FY2024": 40126116,
                "FY2023": 40338726,
                "FY2022": 42544451,
                "FY2021": 42569754,
            },
        ),
        (
            "Leverage ratio excluding claims on central banks (%)",
            {
                "FY2025": "5.47%",
                "FY2024": "4.95%",
                "FY2023": "4.57%",
                "FY2022": "4.2%",
                "FY2021": "4.0%",
            },
        ),
        (
            "Leverage ratio total exposure measure including claims on central banks (FY2021 as originally reported, pre-2022 PRA methodology)",
            {"FY2021": 47412008},
        ),
        (
            "Leverage ratio including claims on central banks (%) (FY2021 as originally reported, pre-2022 PRA methodology)",
            {"FY2021": "3.6%"},
        ),
        (
            "Leverage ratio total exposure measure (FY2014-FY2020 as originally reported, pre-2022 PRA methodology, including claims on central banks)",
            {
                "FY2020": 42933969,
                "FY2019": 39889242,
                "FY2018": 41445900,
                "FY2017": 42668600,
                "FY2016": 37525812,
                "FY2015": 32026192,
            },
        ),
        (
            "Leverage ratio (%) (FY2014-FY2020 as originally reported, pre-2022 PRA methodology)",
            {
                "FY2020": "3.8%",
                "FY2019": "4.6%",
                "FY2018": "4.4%",
                "FY2017": "4.5%",
                "FY2016": "4.8%",
                "FY2015": "5.2%",
                "FY2014": "5.8%",
            },
        ),
    ],
    p3_sources("6"),
    note="From the PRA Rulebook change effective January 2022, TSB's leverage ratio is calculated excluding "
    "central bank claims; FY2021 figures on that basis (42,569,754 / 4.0%) are a restatement published "
    "as the FY2021 comparator in the FY2022 disclosure, not TSB's own FY2021 report - which itself reported "
    "on the pre-2022 basis including central bank claims (47,412,008 / 3.6%, kept on its own row). FY2014-FY2020 "
    "are shown on the pre-2022 'including claims on central banks' basis throughout, as originally reported "
    "each year (not restated) - FY2020's leverage ratio also had a temporary COVID-related alternative "
    "measure of 4.3% disclosed alongside the standard 3.8% figure used here; FY2014's leverage-ratio capital "
    "numerator basis in the source Pillar 3 table is not fully reconcilable to the CET1 figure used elsewhere "
    "on this sheet, so only the ratio itself (5.8%, as published) is shown for FY2014, with the exposure measure "
    "left blank rather than backed into.",
)

metric(
    "LCR",
    "£'000 / %",
    [
        (
            "Total high-quality liquid assets (HQLA) (weighted value - average)",
            {
                "FY2025": 6476199,
                "FY2024": 6921589,
                "FY2023": 7371627,
                "FY2022": 6788964,
                "FY2021": 6441563,
            },
        ),
        (
            "Cash outflows - total weighted value",
            {
                "FY2025": 3765659,
                "FY2024": 4056488,
                "FY2023": 4134068,
                "FY2022": 4326960,
                "FY2021": 4123393,
            },
        ),
        (
            "Cash inflows - total weighted value",
            {
                "FY2025": 250510,
                "FY2024": 230451,
                "FY2023": 218878,
                "FY2022": 260513,
                "FY2021": 202253,
            },
        ),
        (
            "Total net cash outflows (adjusted value)",
            {
                "FY2025": 3515149,
                "FY2024": 3826038,
                "FY2023": 3915190,
                "FY2022": 4066447,
                "FY2021": 3921140,
            },
        ),
        (
            "Liquidity Coverage Ratio (%)",
            {
                "FY2025": "185%",
                "FY2024": "182%",
                "FY2023": "188%",
                "FY2022": "168%",
                "FY2021": "165%",
            },
        ),
    ],
    p3_sources("6"),
    note="LCR is a twelve-month simple average per TSB's disclosed methodology. Not disclosed for FY2014-FY2020: "
    "TSB's Pillar 3/large-subsidiary disclosures and TSB Banking Group plc's Annual Reports for these years do "
    "not include a KM1/LIQ1-style LCR breakdown (confirmed by searching each source document used elsewhere on "
    "this sheet - TSB's earliest disclosed LCR breakdown of this granularity is FY2021's). Left blank rather "
    "than estimated.",
)

metric(
    "NSFR",
    "£'000 / %",
    [
        (
            "Total available stable funding",
            {
                "FY2025": 40945691,
                "FY2024": 42119435,
                "FY2023": 42368266,
                "FY2022": 42774578,
            },
        ),
        (
            "Total required stable funding",
            {
                "FY2025": 26999917,
                "FY2024": 27582817,
                "FY2023": 27601540,
                "FY2022": 28845131,
            },
        ),
        (
            "Net Stable Funding Ratio (%)",
            {
                "FY2025": "152%",
                "FY2024": "153%",
                "FY2023": "154%",
                "FY2022": "148%",
                "FY2021": "Not disclosed",
            },
        ),
    ],
    p3_sources("6"),
    note="NSFR is a four-quarter simple average per TSB's disclosed methodology. Not disclosed for FY2021: the "
    "PRA's averaging methodology for NSFR was only introduced from 1 January 2022, so no FY2021 comparative "
    "was reported (confirmed explicitly in the FY2022 disclosure). Separately, the FY2024 disclosure's own "
    "FY2023 comparator shows NSFR as 153% rather than the 154% in TSB's own FY2023 disclosure used here - a "
    "1 percentage point drift, most likely rounding/methodology refinement between report vintages rather "
    "than an error; both are reproduced faithfully from their respective source documents. Not disclosed for "
    "FY2014-FY2020 for the same reason as FY2021 above (PRA averaging methodology only from 1 January 2022) - "
    "no NSFR breakdown of this kind appears in any of TSB's disclosures for these years.",
)

MREL_SOURCES = (
    "Sources - TSB Banking Group plc consolidated Pillar 3 basis, Section 4.4 'Minimum requirement for own funds "
    "and eligible liabilities (MREL)' (see entity note on Cash Flow Statement sheet):\n"
    f"FY2025: TSB Banking Group plc Large Subsidiary Disclosures, as at 31 December 2025, p.13 - {P3_25_URL}\n"
    f"FY2024: TSB Banking Group plc Large Subsidiary Disclosures, as at 31 December 2024, p.16 - {P3_24_URL}\n"
    f"FY2023: TSB Banking Group plc Large Subsidiary Disclosures 2023, p.16 - {P3_23_URL}\n"
    f"FY2022: TSB Banking Group plc Large Subsidiary Disclosures 2022, p.17 - {P3_22_URL}\n"
    f"FY2021: TSB Banking Group plc Large Subsidiary Disclosures 2021, p.14 - {P3_21_URL}\n"
    f"FY2020: TSB Banking Group plc Large Subsidiary Disclosures, as at 31 December 2020, Section 4.4 "
    f"'Minimum requirement for own funds and eligible liabilities (MREL)' - {P3_20_URL}"
)

metric(
    "MREL Ratio",
    "%",
    [
        (
            "MREL ratio",
            {
                "FY2025": "27.04%",
                "FY2024": "28.33%",
                "FY2023": "27.8%",
                "FY2022": "26.9%",
                "FY2021": "22.8%",
                "FY2020": "23.2%",
            },
        ),
        (
            "Internal MREL requirement (TSB is a UK subsidiary of Banco Sabadell; not a resolution entity in its own right)",
            {
                "FY2025": "23.58%",
                "FY2024": "24.03%",
                "FY2023": "18.4%",
                "FY2022": "16.2%",
                "FY2021": "16.2%",
                "FY2020": "16.2%",
            },
        ),
    ],
    MREL_SOURCES,
    note="TSB is subject to an internal MREL requirement (not external/resolution-entity MREL) as a UK subsidiary "
    "of Banco Sabadell. The requirement shown is TSB's disclosed internal MREL requirement each year - basis "
    "changed from 'excluding regulatory stress buffers' (FY2021-23) to an all-in figure 'including regulatory "
    "stress buffers' (FY2024-25), per TSB's own wording each year; TSB's MREL ratio exceeded its requirement "
    "in every year shown. Not disclosed for FY2014-FY2019: the interim MREL requirement period only began "
    "1 January 2020 per TSB's own FY2020 disclosure, and FY2020 is the first year TSB reports an MREL ratio "
    "at all (no FY2019 comparator is given in the FY2020 disclosure) - FY2014-FY2019 left blank as genuinely "
    "not applicable/not yet in effect, rather than simply undisclosed.",
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {"FY2025": 45281.5, "FY2024": 46099.1, "FY2023": 47652.9, "FY2022": 49449.6, "FY2021": 46705.6, "FY2020": 42422.4, "FY2019": 39535.9, "FY2018": 41138.6, "FY2017": 42536.7, "FY2016": 37195.7, "FY2015": 31618.0, "FY2014": 27171.4}),
        ("Loans and advances to customers", {"FY2025": 36268.4, "FY2024": 36330.9, "FY2023": 36245.9, "FY2022": 38050.0, "FY2021": 37383.8, "FY2020": 33317.9, "FY2019": 31075.8, "FY2018": 30008.5, "FY2017": 30854.2, "FY2016": 29419.1, "FY2015": 26402.2, "FY2014": 21641.4}),
        ("Customer deposits", {"FY2025": 35209.0, "FY2024": 35051.2, "FY2023": 34764.3, "FY2022": 36338.2, "FY2021": 35951.9, "FY2020": 34375.3, "FY2019": 30182.4, "FY2018": 29084.3, "FY2017": 30520.6, "FY2016": 29383.8, "FY2015": 25915.7, "FY2014": 24624.9}),
        ("Total equity", {"FY2025": 2338.0, "FY2024": 2120.7, "FY2023": 1954.6, "FY2022": 1929.8, "FY2021": 1866.4, "FY2020": 1724.9, "FY2019": 1900.8, "FY2018": 1878.9, "FY2017": 2006.6, "FY2016": 1865.0, "FY2015": 1746.3, "FY2014": 1634.4}),
    ],
    balance_sheet_unit="£m",
    income_statement_totals=[
        ("Total income", {"FY2025": 1172.3, "FY2024": 1137.0, "FY2023": 1156.7, "FY2022": 1105.5, "FY2021": 982.9, "FY2020": 932.9, "FY2019": 987.2, "FY2018": 1295.3, "FY2017": 1096.1, "FY2016": 1004.0, "FY2015": 890.7, "FY2014": 900.2}),
        ("Total operating expenses", {"FY2025": -785.9, "FY2024": -821.8, "FY2023": -852.9, "FY2022": -869.5, "FY2021": -827.3, "FY2020": -969.4, "FY2019": -881.3, "FY2018": -905.7, "FY2017": -859.2, "FY2016": -734.7, "FY2015": -740.8, "FY2014": -632.4}),
        ("Profit/(loss) for the year", {"FY2025": 251.1, "FY2024": 203.8, "FY2023": 173.4, "FY2022": 100.6, "FY2021": 128.4, "FY2020": -156.2, "FY2019": 26.2, "FY2018": -59.1, "FY2017": 115.1, "FY2016": 127.8, "FY2015": 88.8, "FY2014": 134.5}),
    ],
    income_statement_unit="£m",
    equity_changes_totals=[
        ("Opening equity", {"FY2025": 2120.7, "FY2024": 1954.6, "FY2023": 1929.8, "FY2022": 1866.4, "FY2021": 1724.9, "FY2020": 1900.8, "FY2019": 1878.9, "FY2018": 2006.6, "FY2017": 1865.0, "FY2016": 1746.3, "FY2015": 1634.4, "FY2014": 1306.7}),
        ("Total comprehensive income/(loss) for the year", {"FY2025": 234.9, "FY2024": 216.1, "FY2023": 144.8, "FY2022": 130.4, "FY2021": 141.5, "FY2020": -175.9, "FY2019": 21.9, "FY2018": -60.1, "FY2017": 127.0, "FY2016": 118.7, "FY2015": 103.8, "FY2014": 134.9}),
        ("Other equity movements, net", {"FY2025": -17.6, "FY2024": -50.0, "FY2023": -120.0, "FY2022": -67.0, "FY2021": 0, "FY2020": 0.0, "FY2019": 0.0, "FY2018": -67.6, "FY2017": 14.6, "FY2016": 0.0, "FY2015": 8.1, "FY2014": 192.8}),
        ("Closing equity", {"FY2025": 2338.0, "FY2024": 2120.7, "FY2023": 1954.6, "FY2022": 1929.8, "FY2021": 1866.4, "FY2020": 1724.9, "FY2019": 1900.8, "FY2018": 1878.9, "FY2017": 2006.6, "FY2016": 1865.0, "FY2015": 1746.3, "FY2014": 1634.4}),
    ],
    equity_changes_unit="£m",
    cash_flow_totals=[
        ("Net cash (used in)/provided by operating activities", {"FY2025": 662.4, "FY2024": 996.9, "FY2023": 1200.7, "FY2022": 596.4, "FY2021": -2145.7, "FY2020": 2319.7, "FY2019": -360.3, "FY2018": -318.8, "FY2017": -59.1, "FY2016": 319.1, "FY2015": -591.2, "FY2014": 7473.7}),
        ("Net cash (used in)/provided by investing activities", {"FY2025": -67.2, "FY2024": 21.1, "FY2023": 88.5, "FY2022": -80.3, "FY2021": -839.1, "FY2020": -429.6, "FY2019": 403.8, "FY2018": -328.6, "FY2017": 4.1, "FY2016": -718.8, "FY2015": -3996.3, "FY2014": -3777.0}),
        ("Net cash (used in)/provided by financing activities", {"FY2025": -1189.5, "FY2024": -2005.7, "FY2023": -597.9, "FY2022": -25.3, "FY2021": 2779.6, "FY2020": -1426.6, "FY2019": -2545.8, "FY2018": 219.9, "FY2017": 3970.7, "FY2016": 1332.7, "FY2015": 2818.4, "FY2014": 612.7}),
        ("Cash and cash equivalents at 31 December", {"FY2025": 4507.3, "FY2024": 5101.6, "FY2023": 6089.3, "FY2022": 5398.0, "FY2021": 4851.1, "FY2020": 5056.3, "FY2019": 4592.8, "FY2018": 7135.9, "FY2017": 7563.4, "FY2016": 3647.7, "FY2015": 2714.7, "FY2014": 4483.8}),
    ],
    cash_flow_unit="£m",
    ratios=[
        ("CET1 Ratio", {"FY2025": "16.74%", "FY2024": "15.45%", "FY2023": "16.7%", "FY2022": "17.2%", "FY2021": "15.9%", "FY2020": "15.3%", "FY2019": "20.8%", "FY2018": "19.5%", "FY2017": "20.0%", "FY2016": "18.5%", "FY2015": "17.8%", "FY2014": "23.0%"}),
        ("Tier 1 Ratio", {"FY2025": "18.88%", "FY2024": "17.67%", "FY2023": "16.7%", "FY2022": "17.2%", "FY2021": "15.9%", "FY2020": "15.3%", "FY2019": "20.8%", "FY2018": "19.5%", "FY2017": "20.0%", "FY2016": "18.5%", "FY2015": "17.8%", "FY2014": "23.0%"}),
        ("Total Capital Ratio", {"FY2025": "21.46%", "FY2024": "20.33%", "FY2023": "19.6%", "FY2022": "20.2%", "FY2021": "18.7%", "FY2020": "18.9%", "FY2019": "25.1%", "FY2018": "23.7%", "FY2017": "24.0%", "FY2016": "22.4%", "FY2015": "21.9%", "FY2014": "28.5%"}),
        ("Leverage Ratio", {"FY2025": "5.47%", "FY2024": "4.95%", "FY2023": "4.57%", "FY2022": "4.2%", "FY2021": "4.0%", "FY2020": "3.8%", "FY2019": "4.6%", "FY2018": "4.4%", "FY2017": "4.5%", "FY2016": "4.8%", "FY2015": "5.2%", "FY2014": "5.8%"}),
        ("LCR", {"FY2025": "185%", "FY2024": "182%", "FY2023": "188%", "FY2022": "168%", "FY2021": "165%", "FY2020": "Not disclosed", "FY2019": "Not disclosed", "FY2018": "Not disclosed", "FY2017": "Not disclosed", "FY2016": "Not disclosed", "FY2015": "Not disclosed", "FY2014": "Not disclosed"}),
        ("NSFR", {"FY2025": "152%", "FY2024": "153%", "FY2023": "154%", "FY2022": "148%", "FY2021": "Not disclosed", "FY2020": "Not disclosed", "FY2019": "Not disclosed", "FY2018": "Not disclosed", "FY2017": "Not disclosed", "FY2016": "Not disclosed", "FY2015": "Not disclosed", "FY2014": "Not disclosed"}),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own source "
    "citation for the underlying document/page. Tier 1 capital first exceeds CET1 from FY2024 onward following "
    "TSB's first AT1 issuance that year. Leverage ratio shown on the 'excluding claims on central banks' basis "
    "from FY2021 onward for comparability (FY2021 was originally reported on the pre-2022 'including' basis; "
    "FY2014-FY2020 are each shown on their own as-originally-reported 'including claims on central banks' "
    "basis, not restated - see Leverage Ratio sheet). 'Opening equity' and 'Other equity movements, net' are "
    "each year's own 31 December closing/1 January opening balance so as to preserve, rather than force-tie "
    "away, two genuine one-off breaks: the FY2016-to-FY2017 entity-basis change from TSB Banking Group plc to "
    "TSB Bank plc (+£14.6m, see Statement of Changes in Equity sheet) and the FY2017-to-FY2018 IFRS 9/IFRS 15 "
    "transition adjustment (-£67.6m). LCR/NSFR are not disclosed by TSB for FY2014-FY2020 (see those sheets).",
)

bw.save("/Users/armaan/code/katalysis/banks/TSB FINANCIALS.xlsx")
