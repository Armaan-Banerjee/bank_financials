import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021", "FY2020", "FY2019", "FY2018", "FY2017", "FY2016", "FY2015"]  # most recent first

AR25_URL = "https://v.icbc.com.cn/userfiles/resources/icbc/haiwai/standardbank/download/2023/consolidatedannualreport2025.pdf"
AR23_URL = "https://v.icbc.com.cn/userfiles/resources/icbc/haiwai/standardbank/download/2023/2023annualreportyasuo.pdf"
AR21_URL = "https://v.icbc.com.cn/userfiles/Resources/ICBC/haiwai/StandardBank/Download/2022/Consolidated_Annual_Report_2021.pdf"
AR20_URL = "https://v.icbc.com.cn/userfiles/Resources/ICBC/haiwai/StandardBank/Download/2021/ConsolidatedAnnualReport20.pdf"
AR19_URL = "https://v.icbc.com.cn/userfiles/Resources/ICBC/haiwai/StandardBank/Download/2020/ConsolidatedAnnualReport.pdf"
AR18_URL = "https://v.icbc.com.cn/userfiles/Resources/ICBC/haiwai/StandardBank/Download/2019/Consolidated_Annual_Report_2018.pdf"
AR17_URL = "https://v.icbc.com.cn/userfiles/Resources/ICBC/haiwai/StandardBank/Download/2019/Consolidated_Annual_Report_2017.pdf"
AR16_URL = "https://v.icbc.com.cn/userfiles/Resources/ICBC/haiwai/StandardBank/Download/2019/ConsolidatedAnnualReport2016.pdf"
AR15_URL = "https://v.icbc.com.cn/userfiles/Resources/ICBC/haiwai/StandardBank/Download/2019/ICBCStandardBankPlcAFS2015.pdf"

P3_25_URL = "https://v.icbc.com.cn/userfiles/resources/icbc/haiwai/standardbank/download/2023/2025pillar3disclosures.pdf"
P3_23_URL = "https://v.icbc.com.cn/userfiles/resources/icbc/haiwai/standardbank/download/2023/2023pillar3.pdf"
P3_21_URL = "https://v.icbc.com.cn/userfiles/Resources/ICBC/haiwai/StandardBank/Download/2022/2021_Pillar_3_document.pdf"
P3_20_URL = "https://v.icbc.com.cn/userfiles/Resources/ICBC/haiwai/StandardBank/Download/2021/2020Pillar3.pdf"
P3_19_URL = "https://v.icbc.com.cn/userfiles/Resources/ICBC/haiwai/StandardBank/Download/2020/Pillar3Disclosures19.pdf"
P3_18_URL = "https://v.icbc.com.cn/userfiles/Resources/ICBC/haiwai/StandardBank/Download/2019/Pillar_3_Disclosures_2018.pdf"
P3_17_URL = "https://v.icbc.com.cn/userfiles/Resources/ICBC/haiwai/StandardBank/Download/2019/Pillar_3_Disclosures_2017.pdf"
P3_16_URL = "https://v.icbc.com.cn/userfiles/Resources/ICBC/haiwai/StandardBank/Download/2019/Pillar3Disclosures2016.pdf"
P3_15_URL = "https://v.icbc.com.cn/userfiles/Resources/ICBC/haiwai/StandardBank/Download/2019/ICBCS_Pillar_3_2015.pdf"

AR_STATEMENT_SOURCES_2015_2020 = (
    f"FY2020: ICBC Standard Bank Consolidated Annual Report 2020 (\"Primary Financial Statements\"), section 6-10 — {AR20_URL}\n"
    f"FY2019: ICBC Standard Bank Consolidated Annual Report 2019, section 6-10 — {AR19_URL}\n"
    f"FY2018: ICBC Standard Bank Consolidated Annual Report 2018, section 6-10 — {AR18_URL}\n"
    f"FY2017: ICBC Standard Bank Consolidated Annual Report 2017, section 6-10 — {AR17_URL}\n"
    f"FY2016: ICBC Standard Bank Consolidated Annual Report 2016, section 6-10 — {AR16_URL}\n"
    f"FY2015: ICBC Standard Bank Consolidated Annual Report 2015 (published as \"ICBC Standard Bank Plc AFS 2015\"), "
    f"section 6-10 — {AR15_URL}\n"
    "FY2015 is the entity's genuine historical floor: ICBC Standard Bank Plc was created on 1 February 2015 when "
    "Industrial and Commercial Bank of China Limited acquired 60% of the existing issued shares in Standard Bank Plc "
    "(previously wholly owned by Standard Bank Group) - there is no earlier ICBC Standard Bank Plc annual report; "
    "the FY2015 Annual Report's own FY2014 comparative column is the predecessor Standard Bank Plc entity's restated "
    "figures, not a genuine ICBC Standard Bank Plc FY2014 report, and is not used here."
)

CASH_FLOW_SOURCES = (
    "Sources — all figures are ICBC Standard Bank Plc consolidated (Group) statement of cash flows, $m:\n"
    f"FY2025 & FY2024: ICBC Standard Bank Consolidated Annual Report 2025, p.68 (Consolidated Statement of Cash Flows) — {AR25_URL}\n"
    f"FY2023 & FY2022: ICBC Standard Bank Consolidated Annual Report 2023, p.65 (11. Consolidated statement of cash flows) — {AR23_URL}\n"
    f"FY2021: ICBC Standard Bank Consolidated Annual Report 2021, p.65 (10. Consolidated statement of cash flows) — {AR21_URL}\n"
    f"FY2020: ICBC Standard Bank Consolidated Annual Report 2020, p.55 (10. Consolidated statement of cash flows) — {AR20_URL}\n"
    f"FY2019: ICBC Standard Bank Consolidated Annual Report 2019, p.51 (10. Consolidated statement of cash flows) — {AR19_URL}\n"
    f"FY2018: ICBC Standard Bank Consolidated Annual Report 2018, p.40 (10. Consolidated statement of cash flows) — {AR18_URL}\n"
    f"FY2017: ICBC Standard Bank Consolidated Annual Report 2017, p.36 (10. Consolidated statement of cash flows) — {AR17_URL}\n"
    f"FY2016: ICBC Standard Bank Consolidated Annual Report 2016, p.24 (10. Consolidated statement of cash flows) — {AR16_URL}\n"
    f"FY2015: ICBC Standard Bank Consolidated Annual Report 2015, p.39 (10. Consolidated statement of cash flows) — {AR15_URL}\n"
    "Note: presentation granularity changed across report vintages. FY2025/FY2024 report a single 'Non-cash items "
    "included in profit before tax' adjustment and disclose interest received/paid only in a footnote; FY2023/FY2022 "
    "separately reconcile 'Net interest income' and show 'Interest received'/'Interest paid' as distinct lines within "
    "operating activities; FY2021-FY2019 itemise several non-cash adjustments (equity/cash-settled share-based "
    "payments, impairments, restructuring/commodity-inventory provisions, fair-value hedge movements) matching "
    "FY2021's own structure; FY2018-FY2015 use a shorter adjustments list (no fair-value-hedge or commodity-"
    "inventory-provision lines, since those specific instruments/policies did not yet exist) and FY2017-FY2015 "
    "additionally show 'Interest received'/'Interest paid' as explicit operating-activities lines (dropped from "
    "FY2018 onward, reappearing only as the FY2023/FY2022 explicit lines). FY2015's statement further splits "
    "'Loss before taxation' into continuing vs. discontinued-operations rows (ICBCS discontinued a small business "
    "line in 2014/2015) - shown here as a single 'Profit before taxation' figure equal to their sum, with a separate "
    "'Discontinued operations' adjusting row. Blank cells indicate that year's report did not disclose that specific "
    "line; all section totals (cash flows from operating/investing/financing activities, and cash and cash "
    "equivalents at start/end of year) reconcile exactly year-on-year across all 11 years, including FY2020's own "
    "closing cash and cash equivalents ($3,906.4m) tying exactly to FY2021's own opening balance."
)

def p3_sources(page_25="5", page_23="5", page_21_capital="23", page_21_leverage="87", page_21_lcr="28",
               page_20="26", page_19="27", page_18="25", page_17="25", page_16="23", page_15="25",
               table_name="Table 5: ICBCS - Capital Resources", include_pre2021=True):
    result = (
        "Sources — ICBC Standard Bank Plc (ICBCS Group) consolidated (Pillar 3) basis:\n"
        f"FY2025 & FY2024: ICBC Standard Bank Pillar 3 Disclosures 2025, p.{page_25} (UK KM1 - Key metrics template) — {P3_25_URL}\n"
        f"FY2023 & FY2022: ICBC Standard Bank Pillar 3 Disclosures 2023, p.{page_23} (UK KM1 - Key metrics template) — {P3_23_URL}\n"
        f"FY2021: ICBC Standard Bank Pillar 3 Disclosures 2021, p.{page_21_capital} (Table 5: ICBCS - Capital Resources), "
        f"p.{page_21_leverage} (Annex D: Leverage Ratio Common Disclosure Template), "
        f"p.{page_21_lcr} (Table 8: Average Consolidated Liquidity Coverage Ratio for ICBCS Group) — {P3_21_URL}"
    )
    if include_pre2021:
        result += (
            f"\nFY2020: ICBC Standard Bank Pillar 3 Disclosures 2020, p.{page_20} ({table_name}) — {P3_20_URL}\n"
            f"FY2019: ICBC Standard Bank Pillar 3 Disclosures 2019, p.{page_19} ({table_name}) — {P3_19_URL}\n"
            f"FY2018: ICBC Standard Bank Pillar 3 Disclosures 2018, p.{page_18} ({table_name}) — {P3_18_URL}\n"
            f"FY2017: ICBC Standard Bank Pillar 3 Disclosures 2017, p.{page_17} ({table_name}) — {P3_17_URL}\n"
            f"FY2016: ICBC Standard Bank Pillar 3 Disclosures 2016, p.{page_16} ({table_name}) — {P3_16_URL}\n"
            f"FY2015: ICBC Standard Bank Pillar 3 Disclosures 2015, p.{page_15} ({table_name}) — {P3_15_URL}\n"
            "Caveat: Additional Tier 1 capital did not exist in ICBCS's structure until a $160.0m AT1 issuance to "
            "ICBC in December 2019 - for FY2015-FY2018, Total Tier 1 capital equals CET1 capital exactly (Additional "
            "Tier 1 is nil), and the 'Tier 1 ratio'/'CET1 ratio' rows are numerically identical for those years."
        )
    return result

bw = BankWorkbook(bank_name="ICBC Standard Bank Plc", years=YEARS, header_color="C1272D")

STATEMENTS_ENTITY_NOTE = (
    "All figures are ICBC Standard Bank Plc consolidated (Group) basis, $m unless stated, each year's own "
    "originally-published figures (not a later restated comparative). ICBCS is jointly owned by Industrial and "
    "Commercial Bank of China Limited (60%) and Standard Bank Group Limited (40%)."
)

# ---------------------------------------------------------------
# Sheet 1: Balance Sheet
# ---------------------------------------------------------------
balance_sheet_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and balances with central banks", {"FY2025": 764.5, "FY2024": 2674.1, "FY2023": 2635.9, "FY2022": 4856.1, "FY2021": 6056.5, "FY2020": 3117.0, "FY2019": 2844.3, "FY2018": 1920.9, "FY2017": 2989.5, "FY2016": 1174.3, "FY2015": 3254.2}),
    ("DATA", "Due from banks and other financial institutions", {"FY2025": 5438.2, "FY2024": 3727.2, "FY2023": 2248.4, "FY2022": 2182.3, "FY2021": 2306.7, "FY2020": 2777.7, "FY2019": 1768.3, "FY2018": 1579.5, "FY2017": 2059.5, "FY2016": 1842.3, "FY2015": 1510.9}),
    ("DATA", "Financial assets held for trading", {"FY2025": 1413.4, "FY2024": 1211.9, "FY2023": 1278.5, "FY2022": 702.7, "FY2021": 2455.7, "FY2020": 2187.6, "FY2019": 1920.0, "FY2018": 1582.4, "FY2017": 2579.5, "FY2016": 970.5, "FY2015": 2443.9}),
    ("DATA", "Non-trading financial assets at fair value through profit or loss", {"FY2025": 1017.6, "FY2024": 689.0, "FY2023": 2856.6, "FY2022": 2193.7, "FY2021": 1972.1, "FY2020": 1971.5, "FY2019": 1305.3, "FY2018": 1340.7, "FY2017": 1335.9, "FY2016": 1339.2, "FY2015": 7.9}),
    ("DATA", "Derivative financial assets", {"FY2025": 8686.4, "FY2024": 3911.2, "FY2023": 3383.2, "FY2022": 4968.0, "FY2021": 4392.1, "FY2020": 6084.5, "FY2019": 3981.9, "FY2018": 4019.8, "FY2017": 4299.5, "FY2016": 4715.0, "FY2015": 6223.0}),
    ("DATA", "Reverse repurchase agreements", {"FY2025": 4987.3, "FY2024": 3526.8, "FY2023": 2936.0, "FY2022": 2614.6, "FY2021": 2287.8, "FY2020": 4021.1, "FY2019": 3210.3, "FY2018": 4060.9, "FY2017": 4705.5, "FY2016": 3601.1, "FY2015": 2684.5}),
    ("DATA", "Loans and advances to customers", {"FY2025": 1828.0, "FY2024": 1303.0, "FY2023": 771.3, "FY2022": 818.6, "FY2021": 1608.7, "FY2020": 581.2, "FY2019": 798.4, "FY2018": 737.3, "FY2017": 606.9, "FY2016": 855.3, "FY2015": 427.1}),
    ("DATA", "Financial investments", {"FY2025": 3721.7, "FY2024": 3176.9, "FY2023": 2052.8, "FY2022": 1293.4, "FY2021": 925.5, "FY2020": 1569.5, "FY2019": 1865.5, "FY2018": 1952.3, "FY2017": 962.0, "FY2016": 1300.7, "FY2015": 105.3}),
    ("DATA", "Property and equipment", {"FY2025": 70.8, "FY2024": 70.3, "FY2023": 66.9, "FY2022": 34.6, "FY2021": 47.4, "FY2020": 57.9, "FY2019": 72.2, "FY2018": 20.2, "FY2017": 18.9, "FY2016": 22.6, "FY2015": 21.1}),
    ("DATA", "Current tax assets", {"FY2025": 10.9, "FY2024": 7.6, "FY2023": 11.8, "FY2022": 5.5, "FY2021": 3.5, "FY2020": 0.0, "FY2019": 0.5, "FY2018": 0.3, "FY2017": 0.4, "FY2016": 0.4, "FY2015": 1.1}),
    ("DATA", "Deferred tax assets", {"FY2025": 13.7, "FY2024": 13.3, "FY2023": 8.0, "FY2022": 0.6, "FY2021": 0.7, "FY2020": 0.7, "FY2019": 0.4, "FY2018": 0.3, "FY2017": 1.1, "FY2016": 1.4, "FY2015": 3.0}),
    ("DATA", "Other assets (incl. non-financial commodities inventory held for trading)", {"FY2025": 9848.2, "FY2024": 6289.1, "FY2023": 4997.7, "FY2022": 2957.2, "FY2021": 4211.8, "FY2020": 5367.6, "FY2019": 6658.4, "FY2018": 7359.9, "FY2017": 4295.0, "FY2016": 4400.8, "FY2015": 3455.5}),
    ("TOTAL", "Total assets", {"FY2025": 37800.7, "FY2024": 26600.4, "FY2023": 23247.1, "FY2022": 22627.3, "FY2021": 26268.5, "FY2020": 27736.3, "FY2019": 24425.5, "FY2018": 24574.5, "FY2017": 23853.7, "FY2016": 20223.6, "FY2015": 20137.5}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Financial liabilities held for trading", {"FY2025": 1876.9, "FY2024": 938.0, "FY2023": 1634.7, "FY2022": 1295.2, "FY2021": 1566.5, "FY2020": 1615.8, "FY2019": 1310.3, "FY2018": 855.6, "FY2017": 1544.2, "FY2016": 781.7, "FY2015": 984.3}),
    ("DATA", "Non-trading financial liabilities at fair value through profit or loss", {"FY2025": 7342.6, "FY2024": 6975.3, "FY2023": 3744.0, "FY2022": 2951.2, "FY2021": 2099.9, "FY2020": 2068.2, "FY2019": 1227.6, "FY2018": 1257.7, "FY2017": 1337.6, "FY2016": 1313.3}),
    ("DATA", "Derivative financial liabilities", {"FY2025": 7368.4, "FY2024": 4194.9, "FY2023": 3782.3, "FY2022": 5352.8, "FY2021": 5050.7, "FY2020": 6558.5, "FY2019": 4563.8, "FY2018": 4134.7, "FY2017": 4652.6, "FY2016": 4849.3, "FY2015": 5926.3}),
    ("DATA", "Due to banks and other financial institutions", {"FY2025": 7761.1, "FY2024": 4731.3, "FY2023": 6553.2, "FY2022": 6221.9, "FY2021": 11646.5, "FY2020": 9065.3, "FY2019": 8639.7, "FY2018": 9271.2, "FY2017": 10120.3, "FY2016": 8022.7, "FY2015": 10259.2}),
    ("DATA", "Repurchase agreements", {"FY2025": 1079.1, "FY2024": 1080.4, "FY2023": 853.1, "FY2022": 530.1, "FY2021": 693.6, "FY2020": 2417.1, "FY2019": 1560.8, "FY2018": 1114.7, "FY2017": 1794.2, "FY2016": 2097.7, "FY2015": 361.4}),
    ("DATA", "Certificates of deposit (line eliminated from FY2019 onward - fully repaid)", {"FY2018": 0.0, "FY2017": 16.7, "FY2016": 63.3, "FY2015": 97.4}),
    ("DATA", "Due to customers", {"FY2025": 2386.8, "FY2024": 1431.0, "FY2023": 1077.1, "FY2022": 1736.5, "FY2021": 1235.8, "FY2020": 2273.8, "FY2019": 424.6, "FY2018": 469.7, "FY2017": 600.8, "FY2016": 519.3, "FY2015": 573.4}),
    ("DATA", "Current tax liabilities", {"FY2025": 3.2, "FY2024": 0.8, "FY2023": 2.4, "FY2022": 3.5, "FY2021": 1.9, "FY2020": 3.6, "FY2019": 3.1, "FY2018": 0.8, "FY2017": 0.7, "FY2016": 0.5, "FY2015": 0.0}),
    ("DATA", "Subordinated debt", {"FY2025": 251.9, "FY2024": 248.6, "FY2023": 247.6, "FY2022": 245.4, "FY2021": 250.8, "FY2020": 250.8, "FY2019": 251.2, "FY2018": 659.8, "FY2017": 668.4, "FY2016": 529.2, "FY2015": 682.9}),
    ("DATA", "Other liabilities (incl. precious metal payables)", {"FY2025": 7599.3, "FY2024": 5056.4, "FY2023": 3481.8, "FY2022": 2608.7, "FY2021": 2352.8, "FY2020": 2181.7, "FY2019": 5270.9, "FY2018": 5552.5, "FY2017": 1835.9, "FY2016": 1089.7, "FY2015": 177.6}),
    ("TOTAL", "Total liabilities", {"FY2025": 35669.3, "FY2024": 24656.7, "FY2023": 21376.2, "FY2022": 20945.3, "FY2021": 24898.5, "FY2020": 26434.8, "FY2019": 23252.0, "FY2018": 23316.7, "FY2017": 22571.4, "FY2016": 19266.7, "FY2015": 19062.5}),
    ("SECTION", "Equity", {}),
    ("DATA", "Share capital (and share premium pre-FY2021 restructure)", {"FY2025": 1083.5, "FY2024": 1083.5, "FY2023": 1083.5, "FY2022": 1083.5, "FY2021": 1083.5, "FY2020": 2079.5, "FY2019": 2079.5, "FY2018": 2079.5, "FY2017": 2079.5, "FY2016": 1814.5, "FY2015": 1814.5}),
    ("DATA", "Other equity instruments", {"FY2025": 160.0, "FY2024": 160.0, "FY2023": 160.0, "FY2022": 160.0, "FY2021": 160.0, "FY2020": 160.0, "FY2019": 160.0}),
    ("DATA", "Reserves", {"FY2025": 887.9, "FY2024": 700.2, "FY2023": 627.4, "FY2022": 438.5, "FY2021": 126.5, "FY2020": -938.0, "FY2019": -1066.0, "FY2018": -821.7, "FY2017": -797.2, "FY2016": -857.6, "FY2015": -739.5}),
    ("TOTAL", "Total equity (attributable to ordinary shareholders)", {"FY2025": 2131.4, "FY2024": 1943.7, "FY2023": 1870.9, "FY2022": 1682.0, "FY2021": 1370.0, "FY2020": 1301.5, "FY2019": 1173.5, "FY2018": 1257.8, "FY2017": 1282.3, "FY2016": 956.9, "FY2015": 1075.0}),
    ("TOTAL", "Total liabilities and equity", {"FY2025": 37800.7, "FY2024": 26600.4, "FY2023": 23247.1, "FY2022": 22627.3, "FY2021": 26268.5, "FY2020": 27736.3, "FY2019": 24425.5, "FY2018": 24574.5, "FY2017": 23853.7, "FY2016": 20223.6, "FY2015": 20137.5}),
]

BALANCE_SHEET_SOURCES = (
    f"Sources — {STATEMENTS_ENTITY_NOTE}\n"
    f"FY2025 & FY2024: ICBC Standard Bank Consolidated Annual Report 2025, p.64 (Consolidated balance sheet) — {AR25_URL}\n"
    f"FY2023 & FY2022: ICBC Standard Bank Consolidated Annual Report 2023, p.61 (7. Consolidated balance sheet) — {AR23_URL}\n"
    f"FY2021: ICBC Standard Bank Consolidated Annual Report 2021, p.61 (6. Consolidated balance sheet) — {AR21_URL}\n"
    f"FY2020: ICBC Standard Bank Consolidated Annual Report 2020, p.51 (6. Consolidated balance sheet) — {AR20_URL}\n"
    f"FY2019: ICBC Standard Bank Consolidated Annual Report 2019, p.47 (6. Consolidated balance sheet) — {AR19_URL}\n"
    f"FY2018: ICBC Standard Bank Consolidated Annual Report 2018, p.36 (6. Consolidated balance sheet) — {AR18_URL}\n"
    f"FY2017: ICBC Standard Bank Consolidated Annual Report 2017, p.32 (6. Consolidated balance sheet) — {AR17_URL}\n"
    f"FY2016: ICBC Standard Bank Consolidated Annual Report 2016, p.20 (6. Consolidated balance sheet) — {AR16_URL}\n"
    f"FY2015: ICBC Standard Bank Consolidated Annual Report 2015, p.31 (6. Consolidated balance sheet) — {AR15_URL}\n"
    "Note: an 'Ordinary share premium' line ($996.0m at FY2020) was eliminated via a June 2021 share premium "
    "restructure (cancelled and transferred to retained earnings) - by FY2021 year-end onward, share capital and "
    "premium are a single, fully-merged line; for FY2015-FY2020 the combined 'Share capital (and share premium "
    "pre-FY2021 restructure)' row is the sum of each year's own separately disclosed 'Share capital' and 'Ordinary "
    "share premium' lines. FY2015-FY2018 additionally disclose a separate 'Certificates of deposit' liability line "
    "(fully repaid by FY2018 year-end, last carried at $nil, and dropped from the balance sheet format entirely "
    "from FY2019 onward) - shown as its own row rather than folded into 'Due to customers'. 'Financial assets/"
    "liabilities designated at fair value through profit or loss' was the FY2015-FY2017 IAS 39-era name for the "
    "same line renamed 'Non-trading financial assets/liabilities at fair value through profit or loss' from FY2018 "
    "onward under IFRS 9 - treated here as the same row throughout. 'Other equity instruments' (Additional Tier 1 "
    "capital) did not exist before a $160.0m issuance to ICBC in December 2019 - blank, not zero, for FY2015-FY2018. "
    "All years' Total assets = Total liabilities and equity exactly, and each year's own closing Total equity ties "
    "to the Statement of Changes in Equity sheet."
)

bw.add_balance_sheet_sheet(
    title="ICBC Standard Bank Plc — Consolidated Balance Sheet",
    subtitle="ICBC Standard Bank Group (consolidated basis), $m unless stated",
    rows=balance_sheet_rows,
    sources_text=BALANCE_SHEET_SOURCES,
    first_col_width=68,
    source_height=110,
    unit_suffix=" ($m)",
)

# ---------------------------------------------------------------
# Sheet 2: Profit & Loss
# ---------------------------------------------------------------
income_statement_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest income", {"FY2025": 730.8, "FY2024": 613.4, "FY2023": 524.7, "FY2022": 254.8, "FY2021": 135.1, "FY2020": 180.6, "FY2019": 296.8, "FY2018": 249.9, "FY2017": 191.3, "FY2016": 90.2, "FY2015": 57.3}),
    ("DATA", "Interest expense", {"FY2025": -482.7, "FY2024": -449.5, "FY2023": -370.8, "FY2022": -156.3, "FY2021": -23.1, "FY2020": -67.7, "FY2019": -205.0, "FY2018": -179.0, "FY2017": -110.6, "FY2016": -54.1, "FY2015": -61.0}),
    ("TOTAL", "Net interest income", {"FY2025": 248.1, "FY2024": 163.9, "FY2023": 153.9, "FY2022": 98.5, "FY2021": 112.0, "FY2020": 112.9, "FY2019": 91.8, "FY2018": 70.9, "FY2017": 80.7, "FY2016": 36.1, "FY2015": -3.7}),
    ("DATA", "Fees and commission income", {"FY2025": 81.3, "FY2024": 68.9, "FY2023": 65.7, "FY2022": 43.2, "FY2021": 52.0, "FY2020": 63.4, "FY2019": 44.7, "FY2018": 55.9, "FY2017": 42.7, "FY2016": 19.3, "FY2015": 20.2}),
    ("DATA", "Fees and commission expenses", {"FY2025": -27.1, "FY2024": -24.8, "FY2023": -27.1, "FY2022": -17.8, "FY2021": -19.1, "FY2020": -19.7, "FY2019": -16.6, "FY2018": -11.8, "FY2017": -11.6, "FY2016": -1.6, "FY2015": -1.6}),
    ("TOTAL", "Net fees and commission", {"FY2025": 54.2, "FY2024": 44.1, "FY2023": 38.6, "FY2022": 25.4, "FY2021": 32.9, "FY2020": 43.7, "FY2019": 28.1, "FY2018": 44.1, "FY2017": 31.1, "FY2016": 17.7, "FY2015": 18.6}),
    ("DATA", "Net trading revenue", {"FY2025": 351.7, "FY2024": 257.0, "FY2023": 314.0, "FY2022": 400.6, "FY2021": 260.6, "FY2020": 285.1, "FY2019": 213.0, "FY2018": 216.2, "FY2017": 248.8, "FY2016": 215.9, "FY2015": 107.3}),
    ("DATA", "Net gain on non-trading financial assets/liabilities at fair value through profit or loss", {"FY2025": 85.8, "FY2024": 107.1, "FY2023": 51.5, "FY2022": 51.7, "FY2021": 48.3, "FY2020": 24.0, "FY2019": 3.2, "FY2018": 14.9, "FY2017": 21.8, "FY2016": 19.0}),
    ("DATA", "Recoveries/(losses) on commodity inventory intermediation", {"FY2022": 233.7, "FY2021": 8.8, "FY2020": -13.7, "FY2019": -198.7}),
    ("DATA", "Recoveries on commodity reverse repurchase agreements", {"FY2021": 3.4, "FY2020": 37.1, "FY2018": 37.9, "FY2016": -2.5, "FY2015": 50.5}),
    ("TOTAL", "Non-interest revenue", {"FY2025": 491.7, "FY2024": 408.2, "FY2023": 404.1, "FY2022": 711.4, "FY2021": 354.0, "FY2020": 376.2, "FY2019": 45.6, "FY2018": 313.1, "FY2017": 301.7, "FY2016": 250.1, "FY2015": 176.4}),
    ("TOTAL", "Total operating income", {"FY2025": 739.8, "FY2024": 572.1, "FY2023": 558.0, "FY2022": 809.9, "FY2021": 466.0, "FY2020": 489.1, "FY2019": 137.4, "FY2018": 384.0, "FY2017": 382.4, "FY2016": 286.2, "FY2015": 172.7}),
    ("DATA", "Credit impairment charges/(recoveries)", {"FY2025": -15.0, "FY2024": -2.7, "FY2023": 50.2, "FY2022": -60.8, "FY2021": 2.8, "FY2020": -4.7, "FY2019": -0.4, "FY2018": -0.7, "FY2017": 8.4, "FY2016": -0.3, "FY2015": 0.4}),
    ("TOTAL", "Income after credit impairments", {"FY2025": 724.8, "FY2024": 569.4, "FY2023": 608.2, "FY2022": 749.1, "FY2021": 468.8, "FY2020": 484.4, "FY2019": 137.0, "FY2018": 383.3, "FY2017": 390.8, "FY2016": 285.9, "FY2015": 173.1}),
    ("SECTION", "Operating expenses", {}),
    ("DATA", "Staff costs", {"FY2025": -279.2, "FY2024": -248.5, "FY2023": -247.8, "FY2022": -223.9, "FY2021": -216.1, "FY2020": -211.8, "FY2019": -216.4, "FY2018": -243.5, "FY2017": -262.2, "FY2016": -251.8, "FY2015": -229.1}),
    ("DATA", "Other operating expenses", {"FY2025": -156.8, "FY2024": -130.8, "FY2023": -145.9, "FY2022": -147.9, "FY2021": -127.7, "FY2020": -117.0, "FY2019": -123.9, "FY2018": -130.4, "FY2017": -103.2, "FY2016": -124.6, "FY2015": -152.2}),
    ("DATA", "Restructuring costs and other impairments", {"FY2021": 1.4, "FY2020": -18.8, "FY2019": -29.6}),
    ("DATA", "Indirect taxation", {"FY2025": -7.9, "FY2024": -3.1, "FY2023": -3.9, "FY2022": -1.8, "FY2021": -5.7, "FY2020": -3.9, "FY2019": -4.5, "FY2018": -5.2, "FY2017": -5.9, "FY2016": -6.5, "FY2015": -4.8}),
    ("TOTAL", "Operating expenses", {"FY2025": -443.9, "FY2024": -382.4, "FY2023": -397.6, "FY2022": -373.6, "FY2021": -348.1, "FY2020": -351.5, "FY2019": -374.4, "FY2018": -379.1, "FY2017": -371.3, "FY2016": -382.9, "FY2015": -386.1}),
    ("TOTAL", "Profit before taxation", {"FY2025": 280.9, "FY2024": 187.0, "FY2023": 210.6, "FY2022": 375.5, "FY2021": 120.7, "FY2020": 132.9, "FY2019": -237.4, "FY2018": 4.2, "FY2017": 19.5, "FY2016": -97.0, "FY2015": -213.0}),
    ("DATA", "Income tax charge", {"FY2025": -56.0, "FY2024": -30.5, "FY2023": -23.5, "FY2022": -58.4, "FY2021": -22.1, "FY2020": -17.4, "FY2019": -10.8, "FY2018": -19.0, "FY2017": 10.2, "FY2016": -1.8, "FY2015": -19.8}),
    ("DATA", "Discontinued operations (FY2015 only - a business line discontinued in 2014/2015)", {"FY2016": 0.0, "FY2015": -34.9}),
    ("TOTAL", "Profit attributable to equity shareholders", {"FY2025": 224.9, "FY2024": 156.5, "FY2023": 187.1, "FY2022": 317.1, "FY2021": 98.6, "FY2020": 115.5, "FY2019": -248.2, "FY2018": -14.8, "FY2017": 29.7, "FY2016": -98.8, "FY2015": -267.7}),
    ("SECTION", "Other comprehensive income", {}),
    ("DATA", "Foreign currency translation reserve", {"FY2025": 1.3, "FY2024": -0.7, "FY2023": -0.7, "FY2022": -2.6, "FY2021": 0.8, "FY2020": 1.8, "FY2019": -1.2, "FY2018": -3.9, "FY2017": 4.7, "FY2016": -5.2, "FY2015": -3.7}),
    ("DATA", "Cash flow hedging reserve, net", {"FY2025": 15.6, "FY2024": -22.8, "FY2023": 13.5, "FY2022": 13.1, "FY2021": -19.3, "FY2020": 10.2, "FY2019": 5.8, "FY2018": -4.9, "FY2017": 25.1, "FY2016": -13.6, "FY2015": -8.7}),
    ("DATA", "Net investment hedge reserve", {"FY2018": 0.0, "FY2017": -1.7}),
    ("DATA", "Changes in fair value of debt instruments measured at FVOCI", {"FY2025": 0.1, "FY2024": 0.9, "FY2023": 0.9, "FY2022": -2.5, "FY2021": 0.6, "FY2020": 0.8, "FY2019": -0.6, "FY2018": -0.9, "FY2017": 2.6, "FY2016": -0.5, "FY2015": -0.9}),
    ("DATA", "Gains/(losses) attributable to own credit risk", {"FY2025": 0.0, "FY2024": 1.0, "FY2023": 0.3, "FY2022": -0.9, "FY2021": -0.1, "FY2020": -0.3}),
    ("TOTAL", "Other comprehensive income/(losses) for the year", {"FY2025": 17.0, "FY2024": -21.6, "FY2023": 14.0, "FY2022": 7.1, "FY2021": -17.9, "FY2020": 12.5, "FY2019": 4.0, "FY2018": -9.7, "FY2017": 30.7, "FY2016": -19.3, "FY2015": -13.3}),
    ("TOTAL", "Total comprehensive income attributable to equity shareholders", {"FY2025": 241.9, "FY2024": 134.9, "FY2023": 201.1, "FY2022": 324.2, "FY2021": 80.7, "FY2020": 128.0, "FY2019": -244.2, "FY2018": -24.5, "FY2017": 60.4, "FY2016": -118.1, "FY2015": -281.0}),
]

INCOME_STATEMENT_SOURCES = (
    f"Sources — {STATEMENTS_ENTITY_NOTE}\n"
    f"FY2025 & FY2024: ICBC Standard Bank Consolidated Annual Report 2025, p.65 (Consolidated income statement) and p.66 (Consolidated statement of comprehensive income) — {AR25_URL}\n"
    f"FY2023 & FY2022: ICBC Standard Bank Consolidated Annual Report 2023, p.62-63 (8-9. Consolidated income statement / statement of comprehensive income) — {AR23_URL}\n"
    f"FY2021: ICBC Standard Bank Consolidated Annual Report 2021, p.62-63 (7-8. Consolidated income statement / statement of comprehensive income) — {AR21_URL}\n"
    f"FY2020: ICBC Standard Bank Consolidated Annual Report 2020, p.52 (7-8. Consolidated income statement / statement of comprehensive income) — {AR20_URL}\n"
    f"FY2019: ICBC Standard Bank Consolidated Annual Report 2019, p.48-49 (7-8. Consolidated income statement / statement of comprehensive income) — {AR19_URL}\n"
    f"FY2018: ICBC Standard Bank Consolidated Annual Report 2018, p.37-38 (7-8. Consolidated income statement / statement of comprehensive income) — {AR18_URL}\n"
    f"FY2017: ICBC Standard Bank Consolidated Annual Report 2017, p.33-34 (7-8. Consolidated income statement / statement of comprehensive income) — {AR17_URL}\n"
    f"FY2016: ICBC Standard Bank Consolidated Annual Report 2016, p.21 (7-8. Consolidated income statement / statement of comprehensive income) — {AR16_URL}\n"
    f"FY2015: ICBC Standard Bank Consolidated Annual Report 2015, p.33-35 (7-8. Consolidated income statement / statement of comprehensive income) — {AR15_URL}\n"
    "Note: 'Recoveries/(losses) on commodity inventory intermediation' and 'Recoveries on commodity reverse "
    "repurchase agreements' are one-off lines that appear intermittently across vintages depending on that year's "
    "own commodity-book activity - blank cells indicate that year's report did not disclose or did not have that "
    "specific line, not a genuine zero. 'Restructuring costs and other impairments' likewise only appears in "
    "FY2021/FY2020/FY2019 (net credit sign in FY2021, net cost in FY2020/FY2019). FY2021's 'Other comprehensive "
    "income/(losses) for the year' ($(17.9)m) is derived (Total comprehensive income less Profit for the year) "
    "since that year's report does not show an explicit OCI subtotal row - the disclosed OCI component lines sum "
    "to $(18.0)m, a $0.1m rounding difference reproduced as disclosed, not forced to match. 'Net investment hedge "
    "reserve' is a distinct OCI line only for FY2017 ($(1.7)m, a one-off) and shown as an explicit $nil at "
    "FY2018 year-end (no further movements reported in FY2019/FY2020, and the static $(1.7)m balance carries "
    "unchanged on the Statement of Changes in Equity through FY2021-FY2025 with no further P&L movement disclosed "
    "in any of those years either). FY2015's income statement structurally splits results into continuing and "
    "discontinued operations (ICBCS discontinued a small business line in 2014/2015); shown here as a single "
    "'Profit before taxation' plus a separate 'Discontinued operations' adjusting row, consistent with all other "
    "years' single-line presentation. IAS 39-era years (FY2015-FY2017) label the FVOCI-equivalent OCI reserve "
    "'available-for-sale reserve'; IFRS 9 (effective 1 January 2018) renamed it 'debt instruments measured at "
    "FVOCI' - both are shown on the same 'Changes in fair value of debt instruments measured at FVOCI' row as the "
    "same underlying reserve, per the FY2018 report's own reconciliation which explicitly marks the FY2017 AFS "
    "column as the FVOCI reserve's predecessor. Total comprehensive income reconciles exactly (Profit for the "
    "year + Other comprehensive income) in every year FY2015-FY2025."
)

bw.add_income_statement_sheet(
    title="ICBC Standard Bank Plc — Consolidated Income Statement",
    subtitle="ICBC Standard Bank Group (consolidated basis), $m unless stated",
    rows=income_statement_rows,
    sources_text=INCOME_STATEMENT_SOURCES,
    first_col_width=76,
    source_height=130,
    unit_suffix=" ($m)",
)

# ---------------------------------------------------------------
# Sheet 3: Statement of Changes in Equity
# ---------------------------------------------------------------
EQUITY_HEADERS = [
    "Share capital (and premium pre-restructure)",
    "Other equity instruments",
    "Cash flow hedging reserve",
    "FVOCI reserve",
    "FX translation reserve",
    "Net investment hedge reserve",
    "Own credit reserve",
    "Retained earnings",
    "Total equity",
]

equity_rows = [
    ("TOTAL", "Balance at 1 January 2015 (predecessor Standard Bank Plc entity's restated FY2014 close, not a genuine ICBC Standard Bank Plc figure)", (1514.5, None, 0.3, 2.4, 6.8, None, None, -508.9, 1015.1)),
    ("DATA", "Total comprehensive loss for the year", (None, None, -8.7, -0.9, -3.7, None, None, -267.7, -281.0)),
    ("DATA", "Equity contribution under indemnity claim (capital contribution from Standard Bank Group)", (None, None, None, None, None, None, None, 40.9, 40.9)),
    ("DATA", "Shares issued including share premium (to Standard Bank London Holdings Limited)", (300.0, None, None, None, None, None, None, None, 300.0)),
    ("TOTAL", "Balance at 31 December 2015 (FY2015 close = FY2016 opening)", (1814.5, None, -8.4, 1.5, 3.1, None, None, -735.7, 1075.0)),
    ("DATA", "Total comprehensive loss for the year", (None, None, -13.6, -0.5, -5.2, None, None, -98.8, -118.1)),
    ("TOTAL", "Balance at 31 December 2016 (FY2016 close = FY2017 opening)", (1814.5, None, -22.0, 1.0, -2.1, None, None, -834.5, 956.9)),
    ("DATA", "Total comprehensive profit/(loss) for the year", (None, None, 25.1, 2.6, 4.7, -1.7, None, 29.7, 60.4)),
    ("DATA", "Issue of share capital and share premium (to ICBC and Standard Bank London Holdings Limited)", (265.0, None, None, None, None, None, None, None, 265.0)),
    ("TOTAL", "Balance at 31 December 2017 (FY2017 close = FY2018 opening)", (2079.5, None, 3.1, 3.6, 2.6, -1.7, None, -804.8, 1282.3)),
    ("DATA", "Changes on initial application of IFRS 9 (transition adjustment, 1 January 2018)", (None, None, None, -2.0, None, None, None, 2.0, 0.0)),
    ("DATA", "Total comprehensive loss for the year", (None, None, -4.9, -0.9, -3.9, None, None, -14.8, -24.5)),
    ("TOTAL", "Balance at 31 December 2018 (FY2018 close = FY2019 opening)", (2079.5, None, -1.8, 0.7, -1.3, -1.7, None, -817.6, 1257.8)),
    ("DATA", "Total comprehensive loss for the year", (None, None, 5.8, -0.6, -1.2, None, None, -248.2, -244.2)),
    ("DATA", "Other equity instrument issuance (Additional Tier 1 capital, to ICBC)", (None, 160.0, None, None, None, None, None, -0.1, 159.9)),
    ("TOTAL", "Balance at 31 December 2019 (FY2019 close = FY2020 opening)", (2079.5, 160.0, 4.0, 0.1, -2.5, -1.7, None, -1065.9, 1173.5)),
    ("DATA", "Total comprehensive gains/(losses) for the year", (None, None, 10.2, 0.8, 1.8, None, -0.3, 115.5, 128.0)),
    ("TOTAL", "Balance at 31 December 2020 (FY2020 close = FY2021 opening)", (2079.5, 160.0, 14.2, 0.9, -0.7, -1.7, -0.3, -950.4, 1301.5)),
    ("DATA", "Total comprehensive gains/(losses) for the year", (None, None, -19.3, 0.6, 0.8, None, -0.1, 98.6, 80.7)),
    ("DATA", "Share premium restructure (cancellation of share premium, transferred to retained earnings)", (-996.0, None, None, None, None, None, None, 996.0, 0.0)),
    ("DATA", "Coupon payment on other equity instruments", (None, None, None, None, None, None, None, -12.2, -12.2)),
    ("TOTAL", "Balance at 31 December 2021 (FY2021 close = FY2022 opening)", (1083.5, 160.0, -5.1, 1.5, 0.1, -1.7, -0.4, 132.1, 1370.0)),
    ("DATA", "Total comprehensive gains/(losses) for the year", (None, None, 13.1, -2.5, -2.6, None, -0.9, 317.1, 324.2)),
    ("DATA", "Coupon payment on other equity instruments", (None, None, None, None, None, None, None, -12.2, -12.2)),
    ("TOTAL", "Balance at 31 December 2022 (FY2022 close = FY2023 opening)", (1083.5, 160.0, 8.0, -1.0, -2.5, -1.7, -1.3, 437.0, 1682.0)),
    ("DATA", "Total comprehensive gains/(losses) for the year", (None, None, 13.5, 0.9, -0.7, None, 0.3, 187.1, 201.1)),
    ("DATA", "Coupon payment on other equity instruments", (None, None, None, None, None, None, None, -12.2, -12.2)),
    ("TOTAL", "Balance at 31 December 2023 (FY2023 close = FY2024 opening)", (1083.5, 160.0, 21.5, -0.1, -3.2, -1.7, -1.0, 611.9, 1870.9)),
    ("DATA", "Total comprehensive gains/(losses) for the year", (None, None, -22.8, 0.9, -0.7, None, 1.0, 156.5, 134.9)),
    ("DATA", "Dividend payment on ordinary share capital", (None, None, None, None, None, None, None, -49.9, -49.9)),
    ("DATA", "Coupon payment on other equity instruments", (None, None, None, None, None, None, None, -12.2, -12.2)),
    ("TOTAL", "Balance at 31 December 2024 (FY2024 close = FY2025 opening)", (1083.5, 160.0, -1.3, 0.8, -3.9, -1.7, 0.0, 706.3, 1943.7)),
    ("DATA", "Total comprehensive gains for the year", (None, None, 15.6, 0.1, 1.3, None, 0.0, 224.9, 241.9)),
    ("DATA", "Dividend payment on ordinary share capital", (None, None, None, None, None, None, None, -41.8, -41.8)),
    ("DATA", "Coupon payment on other equity instruments", (None, None, None, None, None, None, None, -12.4, -12.4)),
    ("TOTAL", "Balance at 31 December 2025 (FY2025 close)", (1083.5, 160.0, 14.3, 0.9, -2.6, -1.7, 0.0, 877.0, 2131.4)),
]

EQUITY_SOURCES = (
    f"Sources — {STATEMENTS_ENTITY_NOTE}\n"
    f"FY2025 & FY2024 movements: ICBC Standard Bank Consolidated Annual Report 2025, p.67 (Consolidated statement of changes in shareholders' equity) — {AR25_URL}\n"
    f"FY2023 & FY2022 movements: ICBC Standard Bank Consolidated Annual Report 2023, p.64 (10. Consolidated statement of changes in shareholders' equity) — {AR23_URL}\n"
    f"FY2021 movements: ICBC Standard Bank Consolidated Annual Report 2021, p.64 (9. Consolidated statement of changes in shareholders' equity) — {AR21_URL}\n"
    f"FY2020 movements: ICBC Standard Bank Consolidated Annual Report 2020, p.54 (9. Consolidated statement of changes in shareholders' equity) — {AR20_URL}\n"
    f"FY2019 movements: ICBC Standard Bank Consolidated Annual Report 2019, p.50 (9. Consolidated statement of changes in shareholders' equity) — {AR19_URL}\n"
    f"FY2018 movements: ICBC Standard Bank Consolidated Annual Report 2018, p.39 (9. Consolidated statement of changes in shareholders' equity) — {AR18_URL}\n"
    f"FY2017 movements: ICBC Standard Bank Consolidated Annual Report 2017, p.35 (9. Consolidated statement of changes in shareholders' equity) — {AR17_URL}\n"
    f"FY2016 movements: ICBC Standard Bank Consolidated Annual Report 2016, p.23 (9. Consolidated statement of changes in shareholders' equity) — {AR16_URL}\n"
    f"FY2015 movements: ICBC Standard Bank Consolidated Annual Report 2015, p.37 (9. Consolidated statement of changes in shareholders' equity) — {AR15_URL}\n"
    "Reconciliation ladder confirmed: every year's own closing balance ties exactly to both the next year's own "
    "opening balance and that year's own Balance Sheet Total equity - zero plug rows needed anywhere across all "
    "11 years, all the way back to the 1 January 2015 opening balance (itself the predecessor Standard Bank Plc "
    "entity's restated 31 December 2014 close - ICBC Standard Bank Plc's own first balance sheet date is "
    "1 February 2015, so this is the closest genuine opening figure available, not fabricated). The June 2021 "
    "share premium restructure (cancellation of the $996.0m share premium account, transferred to retained "
    "earnings) is shown as an explicit, net-zero movement row rather than absorbed silently, matching how the "
    "1 January 2018 IFRS 9 transition adjustment ($2.0m reclassified from the AFS/FVOCI reserve to retained "
    "earnings) is also shown as its own explicit, net-zero row rather than silently folded into that year's total "
    "comprehensive income. 'Own credit reserve' and 'Net investment hedge reserve' columns did not exist before "
    "FY2019/FY2017 respectively (blank, not zero, in earlier years - the reserve itself had not yet been "
    "introduced into the Group's capital structure); 'Other equity instruments' (Additional Tier 1 capital) is "
    "blank before its December 2019 issuance. 'Own credit reserve' genuinely nets to $0.0m from FY2024 year-end "
    "onward (shown as '-' in the Bank's own tables), not a blank/inapplicable cell."
)

bw.add_equity_changes_sheet(
    title="ICBC Standard Bank Plc — Consolidated Statement of Changes in Equity",
    subtitle="ICBC Standard Bank Group (consolidated basis), $m, chronological roll-forward",
    headers=EQUITY_HEADERS,
    rows=equity_rows,
    sources_text=EQUITY_SOURCES,
    first_col_width=58,
    source_height=140,
)

# ---------------------------------------------------------------
# Sheet 4: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Reconciliation of profit before tax to net cash flows from operating activities", {}),
    ("DATA", "Profit before taxation", {"FY2025": 280.9, "FY2024": 187.0, "FY2023": 210.6, "FY2022": 375.5, "FY2021": 120.7, "FY2020": 132.9, "FY2019": -237.4, "FY2018": 4.2, "FY2017": 19.5, "FY2016": -97.0, "FY2015": -213.0}),
    ("DATA", "Discontinued operations (loss before taxation, FY2015 only)", {"FY2016": 0.0, "FY2015": -34.9}),
    ("DATA", "Non-cash items included in profit before tax (as reported)", {"FY2025": -4.5, "FY2024": -48.1}),
    ("DATA", "Net interest income (as reported)", {"FY2023": -153.9, "FY2022": -98.5, "FY2021": -112.0, "FY2020": -112.9, "FY2019": -91.8, "FY2018": -70.9, "FY2017": -80.7, "FY2016": -36.1, "FY2015": 3.7}),
    ("DATA", "Amortisation of intangible assets", {"FY2025": 6.5, "FY2024": 8.7, "FY2023": 9.6, "FY2022": 11.0, "FY2021": 11.2, "FY2020": 11.4, "FY2019": 7.0, "FY2018": 4.1, "FY2017": 0.7, "FY2016": 0.1, "FY2015": 11.7}),
    ("DATA", "Depreciation of property and equipment", {"FY2025": 12.5, "FY2024": 14.8, "FY2023": 17.5, "FY2022": 18.2, "FY2021": 17.9, "FY2020": 17.9, "FY2019": 20.0, "FY2018": 4.6, "FY2017": 5.1, "FY2016": 7.9, "FY2015": 10.1}),
    ("DATA", "Non-cash flow movements on fair value hedges", {"FY2025": 2.3, "FY2024": -2.8, "FY2023": -2.2, "FY2022": 0.9, "FY2021": 0, "FY2020": -23.6, "FY2019": -60.7}),
    ("DATA", "Non-cash flow movements on subordinated debt (FY2015-FY2018 only - superseded by the fair value hedges line from FY2019)", {"FY2018": -8.6, "FY2017": -11.1, "FY2016": -8.9, "FY2015": -1.7}),
    ("DATA", "Incentive charges / cash-settled incentive payments", {"FY2025": 93.1, "FY2024": 69.4, "FY2023": 72.9, "FY2022": 64.6, "FY2021": 10.4, "FY2020": 25.7, "FY2019": 6.8, "FY2018": 8.6, "FY2017": 8.0, "FY2016": 12.2, "FY2015": 10.9}),
    ("DATA", "Equity-settled share-based payments", {"FY2021": -0.3, "FY2015": 0.0}),
    ("DATA", "Net credit impairment charges/(recoveries)", {"FY2025": 15.0, "FY2024": 2.7, "FY2023": -50.2, "FY2022": 60.8, "FY2021": -2.8, "FY2020": 4.7, "FY2019": 0.4, "FY2018": 0.7, "FY2017": -8.4, "FY2016": 0.3, "FY2015": 0.4}),
    ("DATA", "Impairment of property and equipment", {"FY2021": -0.9, "FY2020": 2.9, "FY2019": 3.5}),
    ("DATA", "Impairment of intangible assets", {"FY2021": 0, "FY2020": 5.4}),
    ("DATA", "Provisions for commodity inventory intermediation costs", {"FY2021": -7.0, "FY2020": 11.0, "FY2019": 49.8}),
    ("DATA", "Restructuring provisions", {"FY2021": -5.3, "FY2020": -10.3, "FY2019": 18.6}),
    ("DATA", "Other (FY2020 only)", {"FY2020": 16.8}),
    ("DATA", "Provisions for leave pay", {"FY2025": -0.1, "FY2024": 0.3, "FY2023": 0.3, "FY2022": -1.4, "FY2021": -0.3, "FY2020": 1.9, "FY2019": 0.2, "FY2018": 0.1, "FY2017": 0.3, "FY2016": -0.2, "FY2015": 1.7}),
    ("TOTAL", "Subtotal after non-cash adjustments", {"FY2025": 405.7, "FY2024": 232.0, "FY2023": 104.6, "FY2022": 431.1, "FY2021": 31.6, "FY2020": 83.8, "FY2019": -283.6, "FY2018": -57.2, "FY2017": -66.6, "FY2016": -121.7, "FY2015": -211.1}),
    ("SECTION", "Changes in operating funds", {}),
    ("DATA", "(Increase)/decrease in income-earning assets", {"FY2025": -8294.0, "FY2024": -2780.4, "FY2023": -4382.4, "FY2022": 2981.5, "FY2021": 1974.8, "FY2020": -949.1, "FY2019": 1025.8, "FY2018": -1901.8, "FY2017": -2498.7, "FY2016": -3948.8, "FY2015": -816.4}),
    ("DATA", "Increase/(decrease) in interest bearing and non-interest bearing liabilities", {"FY2025": 6161.5, "FY2024": 2706.7, "FY2023": 1994.6, "FY2022": -4589.9, "FY2021": 154.2, "FY2020": 1072.1, "FY2019": 296.4, "FY2018": 1029.5, "FY2017": 3598.7, "FY2016": 1868.1, "FY2015": 2464.7}),
    ("TOTAL", "Changes in operating funds (subtotal)", {"FY2025": -2132.5, "FY2024": -73.7, "FY2023": -2387.8, "FY2022": -1608.4, "FY2021": 2129.0, "FY2020": 123.0, "FY2019": 1322.2, "FY2018": -872.3, "FY2017": 1100.0, "FY2016": -2080.7, "FY2015": 1648.3}),
    ("DATA", "Interest received (as reported)", {"FY2023": 505.7, "FY2022": 244.1, "FY2021": 146.2, "FY2020": 182.6, "FY2019": 300.0, "FY2018": 243.6, "FY2017": 183.2, "FY2016": 77.2, "FY2015": 59.0}),
    ("DATA", "Interest paid (as reported)", {"FY2023": -336.2, "FY2022": -149.5, "FY2021": -24.0, "FY2020": -85.5, "FY2019": -201.0, "FY2018": -176.1, "FY2017": -100.2, "FY2016": -51.1, "FY2015": -55.0}),
    ("DATA", "Corporation and withholding tax paid", {"FY2025": -53.5, "FY2024": -30.2, "FY2023": -37.0, "FY2022": -54.6, "FY2021": -27.0, "FY2020": -21.9, "FY2019": -10.2, "FY2018": -20.2, "FY2017": -8.6, "FY2016": -0.2, "FY2015": -3.4}),
    ("TOTAL", "Cash flows (used in)/from operating activities", {"FY2025": -1780.3, "FY2024": 128.1, "FY2023": -2150.7, "FY2022": -1137.3, "FY2021": 2255.8, "FY2020": 282.0, "FY2019": 1127.4, "FY2018": -882.2, "FY2017": 1107.8, "FY2016": -2176.5, "FY2015": 1437.8}),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Capital expenditure on intangible assets", {"FY2025": -5.0, "FY2024": -11.5, "FY2023": -5.1, "FY2022": -11.4, "FY2021": -9.4, "FY2020": -5.7, "FY2019": -14.7, "FY2018": -13.0, "FY2017": -14.2}),
    ("DATA", "Capital expenditure on property and equipment", {"FY2025": -13.0, "FY2024": -4.9, "FY2023": -1.8, "FY2022": -4.1, "FY2021": -3.1, "FY2020": -2.5, "FY2019": -3.2, "FY2018": -5.9, "FY2017": -1.4, "FY2016": -9.4, "FY2015": -2.0}),
    ("TOTAL", "Cash flows used in investing activities", {"FY2025": -18.0, "FY2024": -16.4, "FY2023": -6.9, "FY2022": -15.5, "FY2021": -12.5, "FY2020": -8.2, "FY2019": -17.9, "FY2018": -18.9, "FY2017": -15.6, "FY2016": -9.4, "FY2015": -2.0}),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Equity contribution under indemnity claim (capital contribution from Standard Bank Group, FY2015 only)", {"FY2015": 40.9}),
    ("DATA", "Proceeds from issue of ordinary share capital to shareholders", {"FY2017": 265.0, "FY2015": 300.0}),
    ("DATA", "Proceeds from issuance of other equity instruments (Additional Tier 1 capital, FY2019 only)", {"FY2019": 160.0}),
    ("DATA", "Proceeds from issuance of subordinated debt", {"FY2024": 100.0, "FY2022": 150.0, "FY2019": 100.0, "FY2017": 150.0}),
    ("DATA", "Repayment of subordinated debt", {"FY2024": -100.0, "FY2022": -150.0, "FY2019": -500.0, "FY2016": -137.9}),
    ("DATA", "Dividend payment on ordinary share capital", {"FY2025": -41.8, "FY2024": -49.9}),
    ("DATA", "Coupon payment on other equity instruments", {"FY2025": -12.4, "FY2024": -12.2, "FY2023": -12.2, "FY2022": -12.2, "FY2021": -12.2}),
    ("DATA", "Principal payments on leasehold liabilities", {"FY2025": -9.4, "FY2024": -8.5, "FY2023": -10.4, "FY2022": -9.7, "FY2021": -12.5, "FY2020": -16.0, "FY2019": -19.7}),
    ("TOTAL", "Cash flows used in financing activities", {"FY2025": -63.6, "FY2024": -70.6, "FY2023": -22.6, "FY2022": -21.9, "FY2021": -24.7, "FY2020": -16.0, "FY2019": -259.7, "FY2018": 0.0, "FY2017": 415.0, "FY2016": -137.9, "FY2015": 340.9}),
    ("TOTAL", "Net (decrease)/increase in cash and cash equivalents", {"FY2025": -1861.9, "FY2024": 41.1, "FY2023": -2180.2, "FY2022": -1174.7, "FY2021": 2218.6, "FY2020": 257.8, "FY2019": 849.8, "FY2018": -901.1, "FY2017": 1507.2, "FY2016": -2323.8, "FY2015": 1776.7}),
    ("DATA", "Effects of exchange rate changes on cash and cash equivalents", {"FY2025": 2.5, "FY2024": -23.5, "FY2023": -65.8, "FY2022": 42.6, "FY2021": -2.5, "FY2020": 0.5, "FY2019": 5.7, "FY2018": 0.9, "FY2017": 51.0, "FY2016": -17.8, "FY2015": -0.7}),
    ("DATA", "Cash and cash equivalents at beginning of the year", {"FY2025": 2762.0, "FY2024": 2744.4, "FY2023": 4990.4, "FY2022": 6122.5, "FY2021": 3906.4, "FY2020": 3648.1, "FY2019": 2792.6, "FY2018": 3692.8, "FY2017": 2134.6, "FY2016": 4476.2, "FY2015": 2700.2}),
    ("TOTAL", "Cash and cash equivalents at end of the year", {"FY2025": 902.6, "FY2024": 2762.0, "FY2023": 2744.4, "FY2022": 4990.4, "FY2021": 6122.5, "FY2020": 3906.4, "FY2019": 3648.1, "FY2018": 2792.6, "FY2017": 3692.8, "FY2016": 2134.6, "FY2015": 4476.2}),
]

bw.add_cash_flow_sheet(
    title="ICBC Standard Bank Plc — Consolidated Statement of Cash Flows",
    subtitle="ICBC Standard Bank Group (consolidated basis), $m unless stated",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=72,
    source_height=110,
    unit_suffix=" ($m)",
)

# ---------------------------------------------------------------
# Sheet 5: Asset Quality
# ---------------------------------------------------------------
asset_quality_rows = [
    ("SECTION", "Gross balances subject to the three-stage ECL model (IFRS 9, FY2018 onward)", {}),
    ("DATA", "Stage 1 (12-month ECL)", {"FY2025": 13357.1, "FY2024": 11465.1, "FY2023": 9323.6, "FY2022": 10617.5, "FY2021": 11586.6, "FY2020": 12106.4, "FY2019": 10363.9, "FY2018": 10256.9}),
    ("DATA", "Stage 2 (lifetime ECL, not credit-impaired)", {"FY2025": 38.3, "FY2024": 0.0, "FY2023": 0.0, "FY2022": 9.8, "FY2021": 66.8, "FY2020": 5.1, "FY2019": 9.1, "FY2018": 34.6}),
    ("DATA", "Stage 3 (lifetime ECL, credit-impaired)", {"FY2025": 0.0, "FY2024": 0.0, "FY2023": 0.0, "FY2022": 28.3, "FY2020": 7.7, "FY2019": 135.9, "FY2018": 0.2}),
    ("DATA", "Purchased or originated credit-impaired (POCI)", {"FY2025": 5.7, "FY2024": 5.3, "FY2023": 10.8, "FY2022": 95.1}),
    ("TOTAL", "Total gross balances subject to ECL", {"FY2025": 13401.1, "FY2024": 11470.4, "FY2023": 9334.4, "FY2022": 10750.7, "FY2021": 11653.4, "FY2020": 12119.2, "FY2019": 10508.9, "FY2018": 10291.7}),
    ("SECTION", "Credit loss allowance, by stage (year-end balance) (IFRS 9, FY2018 onward)", {}),
    ("DATA", "Stage 1 (12-month ECL)", {"FY2025": -25.4, "FY2024": -15.9, "FY2023": -13.2, "FY2022": -7.3, "FY2021": -5.0, "FY2020": -4.2, "FY2019": -3.8, "FY2018": -3.9}),
    ("DATA", "Stage 2 (lifetime ECL, not credit-impaired)", {"FY2025": -4.0, "FY2024": 0.0, "FY2023": 0.0, "FY2022": -3.8, "FY2021": -0.3, "FY2020": -0.1, "FY2019": -0.5, "FY2018": -0.1}),
    ("DATA", "Stage 3 (lifetime ECL, credit-impaired)", {"FY2025": 0.0, "FY2024": 0.0, "FY2023": 0.0, "FY2022": -4.1, "FY2021": 0.0, "FY2020": -4.8, "FY2019": -0.2, "FY2018": -0.2}),
    ("DATA", "Purchased or originated credit-impaired (POCI)", {"FY2025": -5.3, "FY2024": -3.5, "FY2023": -3.6, "FY2022": -51.4}),
    ("TOTAL", "Total credit loss allowance", {"FY2025": -34.7, "FY2024": -19.4, "FY2023": -16.8, "FY2022": -66.6, "FY2021": -5.3, "FY2020": -9.0, "FY2019": -4.5, "FY2018": -4.2}),
    ("SECTION", "Derived coverage ratio (IFRS 9 years)", {}),
    ("DATA", "Total credit loss allowance / total gross balances subject to ECL", {"FY2025": "0.26%", "FY2024": "0.17%", "FY2023": "0.18%", "FY2022": "0.62%", "FY2021": "0.05%", "FY2020": "0.07%", "FY2019": "0.04%", "FY2018": "0.04%"}),
    ("SECTION", "Pre-IFRS 9 basis (IAS 39 incurred-loss model, FY2015-FY2017 - not directly comparable to the three-stage ECL figures above)", {}),
    ("DATA", "Specifically impaired loans and advances (gross)", {"FY2017": 0.5, "FY2016": 0.0, "FY2015": 0.0}),
    ("DATA", "Specific impairment allowance", {"FY2017": -0.4, "FY2016": 0.0, "FY2015": 0.0}),
    ("DATA", "Portfolio (collective) impairment allowance for performing loans", {"FY2017": -3.8, "FY2016": -6.3, "FY2015": -12.3}),
    ("TOTAL", "Total impairment allowance (specific + portfolio)", {"FY2017": -4.2, "FY2016": -6.3, "FY2015": -12.3}),
]

ASSET_QUALITY_SOURCES = (
    f"Sources — {STATEMENTS_ENTITY_NOTE}\n"
    f"FY2025 & FY2024: ICBC Standard Bank Consolidated Annual Report 2025, p.159-160 (Note 37.4 Credit risk - Analysis of gross balances/Movements in credit loss allowances) — {AR25_URL}\n"
    f"FY2023 & FY2022: ICBC Standard Bank Consolidated Annual Report 2023, p.147-148 (Note 37 Risk management - same tables) — {AR23_URL}\n"
    f"FY2021: ICBC Standard Bank Consolidated Annual Report 2021, p.143-144 (Note 37 Risk management - same tables) — {AR21_URL}\n"
    f"FY2020: ICBC Standard Bank Consolidated Annual Report 2020, p.130-131 (Note 37 Risk management - Analysis of gross balances / Movements in credit loss allowances) — {AR20_URL}\n"
    f"FY2019: ICBC Standard Bank Consolidated Annual Report 2019, p.123-124 (Note 37 Risk management - same tables) — {AR19_URL}\n"
    f"FY2018: ICBC Standard Bank Consolidated Annual Report 2018, p.104 (Note 37 Risk management - same tables) — {AR18_URL}\n"
    f"FY2017: ICBC Standard Bank Consolidated Annual Report 2017, p.95 (Note 37 Risk management - Analysis of specifically impaired loans and advances / Performing portfolio impairments) — {AR17_URL}\n"
    f"FY2016: ICBC Standard Bank Consolidated Annual Report 2016, p.82 (Note 37 Risk management - same tables) — {AR16_URL}\n"
    f"FY2015: ICBC Standard Bank Consolidated Annual Report 2015, p.123 (Note 37 Risk management - same tables) — {AR15_URL}\n"
    "Note: coverage is across the Group's entire ECL-model population (cash, interbank placements, reverse repos, "
    "loans and advances, financial investments, commitments/guarantees) - not restricted to customer loans, since "
    "that is how the Group's own credit-risk note is structured. FY2021's own disclosure does not break out a "
    "separate POCI column (leave blank, not zero) or a distinct 'Sub-standard/Doubtful/Loss' Stage 3 sub-split; "
    "FY2021 Stage 3 total is genuinely nil. The derived coverage ratio (total allowance / total gross balances) is "
    "computed here for a comparable cross-year signal, not itself a disclosed figure. IMPORTANT BASIS CAVEAT: "
    "ICBCS adopted IFRS 9's three-stage expected credit loss (ECL) model from 1 January 2018 (see the Statement of "
    "Changes in Equity sheet's transition-adjustment row); FY2015-FY2017 instead disclose impairment under IAS 39's "
    "incurred-loss model - an 'Analysis of specifically impaired loans and advances' (Sub-standard/Doubtful/Loss "
    "grading) plus a separate collective 'Performing portfolio impairment' provision, not a forward-looking staged "
    "model. These are shown in their own section below the IFRS 9 figures rather than force-mapped into the "
    "Stage 1/2/3 columns, since the two bases measure genuinely different things (incurred losses already "
    "identified vs. forward-looking expected losses) - a caveat, not a data gap. FY2015-FY2016 both show zero "
    "specifically-impaired loans (all impairment was portfolio/collective); FY2017 shows a small $0.5m specifically "
    "impaired balance. There are no past-due-but-not-impaired exposures disclosed in any of FY2015-FY2021."
)

bw.add_asset_quality_sheet(
    title="ICBC Standard Bank Plc — Asset Quality",
    subtitle="ICBC Standard Bank Group (consolidated basis), $m unless stated",
    rows=asset_quality_rows,
    sources_text=ASSET_QUALITY_SOURCES,
    first_col_width=68,
    source_height=140,
    unit_suffix=" ($m)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, f"Consolidated basis, {unit}" if unit else "Consolidated basis",
                         rows_data, sources_text, note=note, first_col_width=48, source_height=100)

# ---------------------------------------------------------------
# KM1 Key Metrics (the bank's own UK KM1 template, reproduced whole).
# Called BEFORE the first add_metric_sheet() so the sheet lands immediately
# after Asset Quality and immediately before CET1 Capital.
# ---------------------------------------------------------------
# KM1-017: the 2022 and 2024 editions were NOT in this script's URL list before
# this ticket. They were found on ICBCS's own downloads index
# (www.icbcstandard.com/en/column/1438058492186738749.html), which lists every
# Pillar 3 edition 2015-2025. Both are own-year editions, so FY2022 and FY2024
# are transcribed from them rather than from a later edition's comparative.
P3_24_URL = "https://v.icbc.com.cn/userfiles/resources/icbc/haiwai/standardbank/download/2023/2024pillar3.pdf"
P3_22_URL = "https://v.icbc.com.cn/userfiles/resources/icbc/haiwai/standardbank/download/2023/2022pillar3re-publish.pdf"

KM1_SOURCES = (
    "Sources — ICBC Standard Bank Plc's own 'UK KM1 - Key metrics template', reproduced as published. "
    "ICBCS Group (consolidated basis), USD millions, the presentation currency of the template itself.\n"
    f"FY2025 & FY2024 column-header years 2025/2024: Pillar 3 Disclosures 2025, p.5 (Table: UK KM1 - Key "
    f"metrics template, in section 'Key metrics and overview of risk-weighted exposure amounts') — {P3_25_URL}\n"
    f"FY2024: Pillar 3 Disclosures 2024, p.5 (UK KM1), its OWN reporting year — {P3_24_URL}\n"
    f"FY2023: Pillar 3 Disclosures 2023, p.5 (UK KM1), its OWN reporting year — {P3_23_URL}\n"
    f"FY2022: Pillar 3 Disclosures 2022, p.5 (UK KM1), its OWN reporting year — {P3_22_URL}\n"
    f"FY2021: NOT from a FY2021 KM1 — the Pillar 3 Disclosures 2021 document prints NO UK KM1 template at all "
    f"(see the sheet note). The FY2021 column here is the 2022 edition's own '31.12.2021' COMPARATIVE column, "
    f"p.5 — {P3_22_URL}\n"
    "Each of FY2025/FY2024/FY2023/FY2022 is taken from the edition in which that year is the REPORTING year, "
    "not from a later edition's comparative. Where both were available they were compared and agree digit for "
    "digit (e.g. the 2025 edition's 2024 comparative reproduces the 2024 edition's own 2024 column exactly, and "
    "the same holds for 2023 in the 2024 edition and 2022 in the 2023 edition).\n"
    "Column-header style is the bank's own and changes between editions (the 2022 edition heads its columns "
    "'31.12.2022 / 31.12.2021'; the 2023, 2024 and 2025 editions use bare years). Every row number, row label, "
    "row order and printed precision below is the bank's own."
)

KM1_NOTE = (
    "FY2020 AND EARLIER ARE BLANK BECAUSE THE TEMPLATE DOES NOT EXIST IN THOSE EDITIONS, not because it was "
    "not found. All eleven ICBC Standard Bank Pillar 3 editions 2015-2025 were downloaded and searched this "
    "session. The 2015-2021 editions print no UK KM1 template: what they do print is 'Table 9: IFRS9 "
    "Transitionals', a DIFFERENT prescribed template (the IFRS9-FL transitional-arrangements disclosure). It "
    "carries seventeen of its own row numbers covering CET1/Tier 1/Total capital, RWAs, the three capital "
    "ratios and the leverage ratio, each also shown 'as if IFRS 9 transitional arrangements had not been "
    "applied' — but it has NO SREP rows, no buffer rows, no LCR rows and no NSFR rows. On the row-set test it "
    "is not the KM1 template, and mapping its rows onto KM1 row numbers would invent a correspondence the bank "
    "never published. Those years' figures are on the eleven single-metric sheets instead, sourced from that "
    "table and from Table 5 (Capital Resources), as each of those sheets' own notes records.\n\n"
    "FY2021 IS FILLED FROM A COMPARATIVE, AND IS THE ONLY COLUMN ON THIS SHEET THAT IS. The FY2021 edition "
    "prints no KM1 at all (above), so there is no own-edition table for that year to displace; the column is "
    "the 2022 edition's own 31.12.2021 comparative. It is independently corroborated by the 2021 edition's own "
    "Table 9, which prints the same CET1 capital (1,148.4), Tier 1 capital (1,308.4), Total capital (1,558.4), "
    "RWAs (8,526.3) and leverage exposure measure (25,679.8) to the same decimal.\n\n"
    "PRECISION DIFFERS BETWEEN THE TWO FY2021 SOURCES AND IS REPRODUCED, NOT RECONCILED. The 2021 edition's "
    "Table 9 prints the FY2021 ratios to two decimals (CET1 13.47%, Tier 1 15.35%, Total capital 18.28%, "
    "leverage 5.09%) while the 2022 edition's KM1 comparative rounds the same ratios to one (13.5%, 15.4%, "
    "18.3%, 5.1%). This sheet shows the KM1 comparative as the KM1 template printed it; the single-metric "
    "sheets show the 2021 edition's own two-decimal figures. Both are the bank's own numbers at different "
    "printed precision, and each is left exactly as the document that carries it printed it.\n\n"
    "SOURCE DEFECT RECORDED, NOT CORRECTED: the NSFR sheet in this workbook states that no FY2021 NSFR figure "
    "is available because the UK NSFR regime only took effect on 1 January 2022. The 2022 edition's KM1 "
    "nevertheless prints a 31.12.2021 NSFR comparative (121.8%, with available/required stable funding of "
    "8,474.8 / 6,955.7). Both statements are the bank's own; the comparative is reproduced here as printed and "
    "the NSFR sheet is left as it stands rather than being edited to agree.\n\n"
    "Rows UK 8a, UK 9a, 10 and UK 10a are printed as an explicit '0.0%' in every edition from 2022 onward, not "
    "as a dash, so they are recorded as zeros. Rows UK 14a-14e are absent from every edition: each one states "
    "in a footnote that they 'have not been disclosed as these are only applicable to LREQ firms', and the 2025 "
    "edition adds that ICBCS is out of scope of the PRA's binding leverage ratio requirement by way of a "
    "modification by consent. That is a stated exclusion, not a gap."
)

bw.add_km1_sheet(
    title="ICBC Standard Bank Plc — UK KM1 Key Metrics Template",
    subtitle="ICBCS Group (consolidated basis), as published. Amounts in USD millions; ratios as printed.",
    rows=[
        ("SECTION", "Available own funds (amounts)", {}),
        ("DATA", "1 Common Equity Tier 1 (CET1) capital ($m)", {"FY2025": 1819.5, "FY2024": 1676.1, "FY2023": 1629.1, "FY2022": 1454.6, "FY2021": 1148.4}),
        ("DATA", "2 Tier 1 capital ($m)", {"FY2025": 1979.5, "FY2024": 1836.1, "FY2023": 1789.1, "FY2022": 1614.6, "FY2021": 1308.4}),
        ("DATA", "3 Total capital ($m)", {"FY2025": 2229.5, "FY2024": 2086.1, "FY2023": 2039.1, "FY2022": 1864.6, "FY2021": 1558.4}),
        ("SECTION", "Risk-weighted exposure amounts", {}),
        ("DATA", "4 Total risk-weighted exposure amount ($m)", {"FY2025": 14902.7, "FY2024": 11500.1, "FY2023": 9653.2, "FY2022": 9251.0, "FY2021": 8526.3}),
        ("SECTION", "Capital ratios (as a percentage of risk-weighted exposure amount)", {}),
        ("DATA", "5 Common Equity Tier 1 ratio (%)", {"FY2025": "12.2%", "FY2024": "14.6%", "FY2023": "16.9%", "FY2022": "15.7%", "FY2021": "13.5%"}),
        ("DATA", "6 Tier 1 ratio (%)", {"FY2025": "13.3%", "FY2024": "16.0%", "FY2023": "18.5%", "FY2022": "17.5%", "FY2021": "15.4%"}),
        ("DATA", "7 Total capital ratio (%)", {"FY2025": "15.0%", "FY2024": "18.1%", "FY2023": "21.1%", "FY2022": "20.2%", "FY2021": "18.3%"}),
        ("SECTION", "Additional own funds requirements based on SREP (as a percentage of risk-weighted exposure amount)", {}),
        ("DATA", "UK 7a Additional CET1 SREP requirements (%)", {"FY2025": "1.3%", "FY2024": "1.7%", "FY2023": "1.7%", "FY2022": "1.9%", "FY2021": "1.9%"}),
        ("DATA", "UK 7b Additional AT1 SREP requirements (%)", {"FY2025": "0.4%", "FY2024": "0.6%", "FY2023": "0.6%", "FY2022": "0.6%", "FY2021": "0.6%"}),
        ("DATA", "UK 7c Additional T2 SREP requirements (%)", {"FY2025": "0.6%", "FY2024": "0.8%", "FY2023": "0.8%", "FY2022": "0.8%", "FY2021": "0.8%"}),
        ("DATA", "UK 7d Total SREP own funds requirements (%)", {"FY2025": "10.3%", "FY2024": "11.0%", "FY2023": "11.0%", "FY2022": "11.3%", "FY2021": "11.3%"}),
        ("SECTION", "Combined buffer requirement (as a percentage of risk-weighted exposure amount)", {}),
        ("DATA", "8 Capital conservation buffer (%)", {"FY2025": "2.5%", "FY2024": "2.5%", "FY2023": "2.5%", "FY2022": "2.5%", "FY2021": "2.5%"}),
        ("DATA", "UK 8a Conservation buffer due to macro-prudential or systemic risk identified at the level of a Member State (%)", {"FY2025": "0.0%", "FY2024": "0.0%", "FY2023": "0.0%", "FY2022": "0.0%", "FY2021": "0.0%"}),
        ("DATA", "9 Institution specific countercyclical capital buffer (%)", {"FY2025": "0.5%", "FY2024": "0.5%", "FY2023": "0.4%", "FY2022": "0.2%", "FY2021": "0.1%"}),
        ("DATA", "UK 9a Systemic risk buffer (%)", {"FY2025": "0.0%", "FY2024": "0.0%", "FY2023": "0.0%", "FY2022": "0.0%", "FY2021": "0.0%"}),
        ("DATA", "10 Global Systemically Important Institution buffer (%)", {"FY2025": "0.0%", "FY2024": "0.0%", "FY2023": "0.0%", "FY2022": "0.0%", "FY2021": "0.0%"}),
        ("DATA", "UK 10a Other Systemically Important Institution buffer", {"FY2025": "0.0%", "FY2024": "0.0%", "FY2023": "0.0%", "FY2022": "0.0%", "FY2021": "0.0%"}),
        ("DATA", "11 Combined buffer requirement (%)", {"FY2025": "3.0%", "FY2024": "3.0%", "FY2023": "2.9%", "FY2022": "2.7%", "FY2021": "2.6%"}),
        ("DATA", "UK 11a Overall capital requirements (%)", {"FY2025": "13.3%", "FY2024": "14.0%", "FY2023": "13.9%", "FY2022": "14.1%", "FY2021": "13.9%"}),
        ("DATA", "12 CET1 available after meeting the total SREP own funds requirements (%)", {"FY2025": "4.3%", "FY2024": "7.2%", "FY2023": "10.7%", "FY2022": "9.4%", "FY2021": "7.1%"}),
        ("SECTION", "Leverage ratio", {}),
        ("DATA", "13 Total exposure measure excluding claims on central banks ($m)", {"FY2025": 35294.7, "FY2024": 26624.0, "FY2023": 23301.0, "FY2022": 20958.2, "FY2021": 25679.8}),
        ("DATA", "14 Leverage ratio excluding claims on central banks (%)", {"FY2025": "5.6%", "FY2024": "6.9%", "FY2023": "7.7%", "FY2022": "7.7%", "FY2021": "5.1%"}),
        ("SECTION", "Liquidity Coverage Ratio", {}),
        ("DATA", "15 Total high-quality liquid assets (HQLA) (Weighted value - average) ($m)", {"FY2025": 5294.2, "FY2024": 5216.2, "FY2023": 5704.2, "FY2022": 6280.5, "FY2021": 5026.7}),
        ("DATA", "UK 16a Cash outflows - Total weighted value ($m)", {"FY2025": 11109.0, "FY2024": 8275.1, "FY2023": 8049.2, "FY2022": 8343.0, "FY2021": 9199.3}),
        ("DATA", "UK 16b Cash inflows - Total weighted value ($m)", {"FY2025": 9539.9, "FY2024": 6036.4, "FY2023": 4559.5, "FY2022": 5656.9, "FY2021": 7290.9}),
        ("DATA", "16 Total net cash outflows (adjusted value) ($m)", {"FY2025": 2777.2, "FY2024": 2422.5, "FY2023": 3561.5, "FY2022": 2926.2, "FY2021": 2425.2}),
        ("DATA", "17 Liquidity coverage ratio (%)", {"FY2025": "197.3%", "FY2024": "226.7%", "FY2023": "165.3%", "FY2022": "206.0%", "FY2021": "207.3%"}),
        ("SECTION", "Net Stable Funding Ratio", {}),
        ("DATA", "18 Total available stable funding ($m)", {"FY2025": 9393.0, "FY2024": 8348.6, "FY2023": 7963.4, "FY2022": 8417.6, "FY2021": 8474.8}),
        ("DATA", "19 Total required stable funding ($m)", {"FY2025": 7736.7, "FY2024": 6118.4, "FY2023": 4462.0, "FY2022": 5266.3, "FY2021": 6955.7}),
        ("DATA", "20 NSFR ratio (%)", {"FY2025": "122.8%", "FY2024": "136.4%", "FY2023": "183.3%", "FY2022": "163.8%", "FY2021": "121.8%"}),
    ],
    sources_text=KM1_SOURCES + "\n\n" + KM1_NOTE,
    first_col_width=96,
    source_height=330,
)

metric(
    "CET1 Capital", "$m",
    [("Common Equity Tier 1 (CET1) capital", {"FY2025": 1819.5, "FY2024": 1676.1, "FY2023": 1629.1, "FY2022": 1454.6, "FY2021": 1148.4, "FY2020": 1072.9, "FY2019": 948.3, "FY2018": 1204.0, "FY2017": 1229.5, "FY2016": 928.6, "FY2015": 1051.0})],
    p3_sources(page_20="26", page_19="27", page_18="25", page_17="25", page_16="23", page_15="25"),
    note="FY2021-FY2015 figures are each year's own 'Total Common Equity Tier I' from that year's Table 5 (Capital "
         "Resources), the transitional-basis equivalent of the UK KM1 template row used from FY2022 onward. "
         "Additional Tier 1 capital did not exist before a $160.0m issuance to ICBC in December 2019, so CET1 "
         "capital equals Tier 1 capital exactly for FY2015-FY2018.",
)

metric(
    "CET1 Ratio", "% of RWA",
    [("Common Equity Tier 1 (CET1) ratio", {"FY2025": "12.2%", "FY2024": "14.6%", "FY2023": "16.9%", "FY2022": "15.7%", "FY2021": "13.47%", "FY2020": "13.21%", "FY2019": "13.64%", "FY2018": "18.52%", "FY2017": "15.59%", "FY2016": "14.6%", "FY2015": "13.87%"})],
    p3_sources(page_20="26", page_19="27", page_18="25", page_17="25", page_16="23", page_15="25"),
)

metric(
    "Tier 1 Capital", "$m",
    [("Tier 1 capital", {"FY2025": 1979.5, "FY2024": 1836.1, "FY2023": 1789.1, "FY2022": 1614.6, "FY2021": 1308.4, "FY2020": 1232.9, "FY2019": 1108.3, "FY2018": 1204.0, "FY2017": 1229.5, "FY2016": 928.6, "FY2015": 1051.0})],
    p3_sources(page_20="26", page_19="27", page_18="25", page_17="25", page_16="23", page_15="25"),
)

metric(
    "Tier 1 Ratio", "% of RWA",
    [("Tier 1 ratio", {"FY2025": "13.3%", "FY2024": "16.0%", "FY2023": "18.5%", "FY2022": "17.5%", "FY2021": "15.35%", "FY2020": "15.18%", "FY2019": "15.94%", "FY2018": "18.52%", "FY2017": "15.59%", "FY2016": "14.6%", "FY2015": "13.9%"})],
    p3_sources(page_20="26", page_19="27", page_18="25", page_17="25", page_16="23", page_15="25"),
    note="FY2021 figure is 'Tier 1 Risk Asset Ratio' from Table 5, the transitional-basis equivalent of the later "
         "UK KM1 template row; same for FY2020-FY2015. Tier 1 ratio equals the CET1 ratio exactly for FY2015-FY2018 "
         "(no Additional Tier 1 capital existed yet).",
)

metric(
    "Total Capital", "$m",
    [("Total capital", {"FY2025": 2229.5, "FY2024": 2086.1, "FY2023": 2039.1, "FY2022": 1864.6, "FY2021": 1558.4, "FY2020": 1482.9, "FY2019": 1358.3, "FY2018": 1446.1, "FY2017": 1575.4, "FY2016": 1227.3, "FY2015": 1449.6})],
    p3_sources(page_20="26", page_19="27", page_18="25", page_17="25", page_16="23", page_15="25"),
    note="FY2021-FY2015 figures are each year's own 'Total eligible capital' from that year's Table 5, the "
         "transitional-basis equivalent of the later UK KM1 template row.",
)

metric(
    "Total Capital Ratio", "% of RWA",
    [("Total capital ratio", {"FY2025": "15.0%", "FY2024": "18.1%", "FY2023": "21.1%", "FY2022": "20.2%", "FY2021": "18.28%", "FY2020": "18.26%", "FY2019": "19.54%", "FY2018": "22.25%", "FY2017": "19.97%", "FY2016": "19.3%", "FY2015": "19.13%"})],
    p3_sources(page_20="26", page_19="27", page_18="25", page_17="25", page_16="23", page_15="25"),
    note="FY2021-FY2015 figures are each year's own 'Capital Adequacy ratio' from that year's Table 5, the "
         "transitional-basis equivalent of the later UK KM1 template row.",
)

metric(
    "Total RWAs", "$m",
    [("Total risk-weighted exposure amount", {"FY2025": 14902.7, "FY2024": 11500.1, "FY2023": 9653.2, "FY2022": 9251.0, "FY2021": 8526.3, "FY2020": 8122.8, "FY2019": 6952.8, "FY2018": 6500.2, "FY2017": 7887.7, "FY2016": 6362.8, "FY2015": 7579.7})],
    p3_sources(page_20="26", page_19="27", page_18="25", page_17="25", page_16="23", page_15="25"),
)

# ---------------------------------------------------------------
# RWA Breakdown (placed right after Total RWAs, itself a Pillar 3 disclosure)
# ---------------------------------------------------------------
rwa_breakdown_rows = [
    ("SECTION", "Risk-weighted exposure amounts by category", {}),
    ("DATA", "Credit risk (excluding CCR)", {"FY2025": 3495.0, "FY2024": 2736.3, "FY2023": 2692.2, "FY2022": 1770.9}),
    ("DATA", "Credit risk, counterparty credit risk and dilution risk, combined (pre-UK-OV1 disclosure format used FY2015-FY2021 - not separable into the components above; derived from each year's own capital requirement ÷8%)", {"FY2021": 3830.0, "FY2020": 3565.0, "FY2019": 3590.0, "FY2018": 3116.25, "FY2017": 3396.25, "FY2016": 2772.5, "FY2015": 2832.5}),
    ("DATA", "Counterparty credit risk (CCR)", {"FY2025": 5023.6, "FY2024": 2843.7, "FY2023": 2109.9, "FY2022": 1854.0}),
    ("DATA", "Of which credit valuation adjustment (CVA)", {"FY2025": 460.4, "FY2024": 276.0, "FY2023": 219.9, "FY2022": 243.4, "FY2021": 193.75, "FY2020": 286.25, "FY2019": 278.75, "FY2018": 601.25, "FY2017": 312.5, "FY2016": 246.25, "FY2015": 308.75}),
    ("DATA", "Settlement risk", {"FY2025": 0.2, "FY2024": 0.6, "FY2023": 0.1, "FY2022": 24.9, "FY2021": 2.5, "FY2020": 1.25, "FY2019": 10.0, "FY2018": 2.5, "FY2017": 2.5, "FY2016": 3.75, "FY2015": 1.25}),
    ("DATA", "Securitisation exposures in the non-trading book", {"FY2025": 0.0, "FY2024": 0.0, "FY2023": 0.0, "FY2022": 0.0}),
    ("DATA", "Market risk (position, foreign exchange and commodities)", {"FY2025": 4799.2, "FY2024": 4464.4, "FY2023": 3475.5, "FY2022": 4277.5, "FY2021": 3681.25, "FY2020": 3485.0, "FY2019": 2396.25, "FY2018": 1991.25, "FY2017": 3612.5, "FY2016": 2706.25, "FY2015": 3175.0}),
    ("DATA", "Operational risk", {"FY2025": 1402.4, "FY2024": 1455.1, "FY2023": 1375.5, "FY2022": 1323.7, "FY2021": 818.75, "FY2020": 757.5, "FY2019": 677.5, "FY2018": 790.0, "FY2017": 460.0, "FY2016": 537.5, "FY2015": 760.0}),
    ("DATA", "Large exposures in the trading book (pre-UK-OV1 disclosure format only - no equivalent line in the later UK OV1 template)", {"FY2020": 28.75, "FY2019": 0.0, "FY2018": 0.0, "FY2017": 103.75, "FY2016": 96.25, "FY2015": 500.0}),
    ("DATA", "Amounts below thresholds for deduction (subject to 250% risk weight, for information)", {"FY2025": 4.9, "FY2024": 3.0, "FY2023": 5.4, "FY2022": 1.5}),
    ("TOTAL", "Total risk-weighted exposure amount", {"FY2025": 14902.7, "FY2024": 11500.1, "FY2023": 9653.2, "FY2022": 9251.0, "FY2021": 8526.3, "FY2020": 8122.8, "FY2019": 6952.8, "FY2018": 6500.2, "FY2017": 7887.7, "FY2016": 6362.8, "FY2015": 7579.7}),
]

RWA_BREAKDOWN_SOURCES = (
    f"Sources — {STATEMENTS_ENTITY_NOTE}\n"
    f"FY2025 & FY2024: ICBC Standard Bank Pillar 3 Disclosures 2025, p.6 (UK OV1 - Overview of risk-weighted exposure amounts) — {P3_25_URL}\n"
    f"FY2023 & FY2022: ICBC Standard Bank Pillar 3 Disclosures 2023, p.6-7 (UK OV1) — {P3_23_URL}\n"
    f"FY2021: ICBC Standard Bank Pillar 3 Disclosures 2021, p.24 (Table 6: ICBCS - Capital Requirements, pre-UK-OV1 format) — {P3_21_URL}\n"
    f"FY2020: ICBC Standard Bank Pillar 3 Disclosures 2020, p.25 (Table 7: ICBCS - Capital Requirements) — {P3_20_URL}\n"
    f"FY2019: ICBC Standard Bank Pillar 3 Disclosures 2019, p.26 (Table 8: ICBCS - Capital Requirements) — {P3_19_URL}\n"
    f"FY2018: ICBC Standard Bank Pillar 3 Disclosures 2018, p.24 (Table 6: ICBCS - Capital Requirements) — {P3_18_URL}\n"
    f"FY2017: ICBC Standard Bank Pillar 3 Disclosures 2017, p.24 (Table 6: ICBCS - Capital Requirements) — {P3_17_URL}\n"
    f"FY2016: ICBC Standard Bank Pillar 3 Disclosures 2016, p.22 (Table 6: ICBCS - Capital Requirements) — {P3_16_URL}\n"
    f"FY2015: ICBC Standard Bank Pillar 3 Disclosures 2015, p.25-26 (Table 6: ICBCS - Capital Requirements) — {P3_15_URL}\n"
    "Note: every one of FY2015-FY2021's Pillar 3 documents predates the UK OV1 template and combines credit, "
    "counterparty credit and dilution risk into one 'standardised approach' capital-requirement line, so none of "
    "them can be split into 'Credit risk (excluding CCR)' and 'Counterparty credit risk (CCR)' the way FY2022 "
    "onward's disclosures are - shown as its own combined line instead of blended into either category. All "
    "FY2015-FY2021 category figures are derived (disclosed capital requirement ÷ 8%, the standard CRR conversion), "
    "not directly disclosed as RWA amounts; each year's derived components sum to that year's own disclosed Total "
    "RWA (to within rounding, e.g. FY2015: $7,577.5m derived vs. $7,579.7m disclosed). FY2015-FY2021's documents "
    "also carry a 'Large exposures in the trading book' capital-requirement line with no equivalent in the later "
    "UK OV1 template (shown as its own row, genuinely zero for FY2018/FY2019 rather than not disclosed) and have "
    "no 'Securitisation exposures' or 'Amounts below thresholds for deduction' line at all (genuinely not "
    "disclosed in that format, left blank rather than assumed zero)."
)

bw.add_rwa_breakdown_sheet(
    title="ICBC Standard Bank Plc — RWA Breakdown",
    subtitle="ICBC Standard Bank Group (consolidated basis), $m",
    rows=rwa_breakdown_rows,
    sources_text=RWA_BREAKDOWN_SOURCES,
    first_col_width=88,
    source_height=150,
    unit_suffix=" ($m)",
)

metric(
    "Leverage Ratio", "$m / %",
    [
        ("Total exposure measure excluding claims on central banks ($m)", {"FY2025": 35294.7, "FY2024": 26624.0, "FY2023": 23301.0, "FY2022": 20958.2, "FY2021": 25680, "FY2020": 25179, "FY2019": 23166, "FY2018": 23996, "FY2017": 25016, "FY2016": 19938, "FY2015": 19607}),
        ("Leverage ratio excluding claims on central banks (%)", {"FY2025": "5.6%", "FY2024": "6.9%", "FY2023": "7.7%", "FY2022": "7.7%", "FY2021": "5.09%", "FY2020": "4.90%", "FY2019": "4.78%", "FY2018": "5.02%", "FY2017": "4.91%", "FY2016": "4.66%", "FY2015": "5.36%"}),
    ],
    p3_sources(page_20="90", page_19="94", page_18="87", page_17="88", page_16="85", page_15="83",
               table_name="Annex D: Leverage Ratio Common Disclosure Template"),
    note="FY2021-FY2015 all use the CRR Leverage Ratio Common Disclosure Template's 'Total leverage ratio "
         "exposures' and 'Leverage ratio' rows (Annex D) — the pre-'excluding central banks' presentation format "
         "used before the later UK KM1 template split the exposure measure basis.",
)

metric(
    "LCR", "$m / %",
    [
        ("Total high-quality liquid assets (HQLA), weighted value (average) ($m)", {"FY2025": 5294.2, "FY2024": 5216.2, "FY2023": 5704.2, "FY2022": 6280.5, "FY2021": 5027, "FY2020": 4371, "FY2019": 4856, "FY2018": 4458, "FY2017": 4322}),
        ("Total net cash outflows, adjusted value ($m)", {"FY2025": 2777.2, "FY2024": 2422.5, "FY2023": 3561.5, "FY2022": 2926.2, "FY2021": 2425, "FY2020": 2426, "FY2019": 2509, "FY2018": 2062, "FY2017": 3126}),
        ("Liquidity Coverage Ratio (%)", {"FY2025": "197.3%", "FY2024": "226.7%", "FY2023": "165.3%", "FY2022": "206.0%", "FY2021": "207%", "FY2020": "180%", "FY2019": "195%", "FY2018": "217%", "FY2017": "145%", "FY2016": "159%", "FY2015": "Not publicly disclosed"}),
    ],
    p3_sources(page_20="30", page_19="31", page_18="29", page_17="30", page_16="27", page_15="27",
               table_name="Table 8/9/10: Consolidated Liquidity Coverage Ratio for ICBCS (Group)"),
    note="LCR figures are averages of month-end observations over the 12 months preceding each year-end. FY2021-"
         "FY2017 figures are each year's own 31 December quarter-end column of the 'Consolidated Liquidity "
         "Coverage Ratio for ICBCS (Group)' table, the same consolidated-Group basis used by the later UK KM1 "
         "template rows. FY2016's Pillar 3 document discloses only a single point-in-time LCR% as at 31 December "
         "2016 (159%, PRA minimum 80% that year) with no HQLA/net-outflow $ breakdown and not framed as a 12-month "
         "average - a narrower disclosure format than later years', shown with blank $m cells rather than a "
         "fabricated breakdown. FY2015's Pillar 3 document discusses the LCR requirement only qualitatively, with "
         "no numeric LCR%, HQLA or net-outflow figure disclosed at all that year (the EBA/PRA quarterly LCR "
         "disclosure tables used from FY2017 onward were not yet in place) - a genuine self-skip, not a search "
         "failure.",
)

metric(
    "NSFR", "$m / %",
    [
        ("Total available stable funding ($m)", {"FY2025": 9393.0, "FY2024": 8348.6, "FY2023": 7963.4, "FY2022": 8417.6}),
        ("Total required stable funding ($m)", {"FY2025": 7736.7, "FY2024": 6118.4, "FY2023": 4462.0, "FY2022": 5266.3}),
        ("Net Stable Funding Ratio (%)", {
            **{"FY2025": "122.8%", "FY2024": "136.4%", "FY2023": "183.3%", "FY2022": "163.8%"},
            **{y: "Not disclosed" for y in YEARS if y not in ("FY2025", "FY2024", "FY2023", "FY2022")},
        }),
    ],
    p3_sources(include_pre2021=False),
    note="OMISSION CORRECTED 2026-09-17 (KM1-017): the four NSFR percentages for FY2025-FY2022 were MISSING "
         "from this sheet until this ticket. The available and required stable funding amounts were present "
         "for those four years but the ratio row carried no value for any of them - it was built from a "
         "comprehension that assigned 'Not disclosed' to every year EXCEPT FY2025-FY2022, and then never "
         "assigned those four anything at all, so they rendered blank. The bank does disclose them: they are "
         "row 20 of its own UK KM1 template in each year's edition (FY2025 122.8%, FY2024 136.4%, FY2023 "
         "183.3%, FY2022 163.8%), the same table this workbook's KM1 Key Metrics sheet reproduces and the same "
         "table the stable-funding amounts on the rows above already came from. Nothing was re-derived: each "
         "figure is transcribed from the edition in which that year is the reporting year. The omission came to "
         "light on 2026-09-17, when this workbook gained a KM1 Key Metrics sheet reproducing row 20 of the same "
         "table for the same years and so placed a second, independent transcription of each of those four "
         "figures beside this sheet's.\n"
         "NSFR was not a UK Pillar 3 disclosure requirement until 1 January 2022 (the UK NSFR regime's effective "
         "date), so no FY2015-FY2021 figures are available in any of the eleven ICBC Standard Bank Pillar 3 "
         "Disclosures reports reviewed (2015-2025). FY2015's own Pillar 3 document explicitly notes 'the NSFR is "
         "expected to go live in January 2018' (an EU timeline later superseded by the UK's own 1 January 2022 "
         "implementation) - confirming this is a genuine regulatory-timeline gap, not a missed disclosure. "
         "Balances shown for FY2022 onward are averages of the four quarter-ends preceding each year-end.",
)

metric(
    "MREL Ratio", None,
    [("MREL ratio", {y: "Not publicly disclosed" for y in YEARS})],
    p3_sources(include_pre2021=False),
    note="No MREL disclosure appears in any of the eleven ICBC Standard Bank Pillar 3 Disclosures reports "
         "reviewed (2015-2025) — ICBC Standard Bank Plc is not itself a resolution entity subject to a standalone "
         "MREL requirement.",
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {"FY2025": 37800.7, "FY2024": 26600.4, "FY2023": 23247.1, "FY2022": 22627.3, "FY2021": 26268.5, "FY2020": 27736.3, "FY2019": 24425.5, "FY2018": 24574.5, "FY2017": 23853.7, "FY2016": 20223.6, "FY2015": 20137.5}),
        ("Loans and advances to customers", {"FY2025": 1828.0, "FY2024": 1303.0, "FY2023": 771.3, "FY2022": 818.6, "FY2021": 1608.7, "FY2020": 581.2, "FY2019": 798.4, "FY2018": 737.3, "FY2017": 606.9, "FY2016": 855.3, "FY2015": 427.1}),
        ("Total liabilities", {"FY2025": 35669.3, "FY2024": 24656.7, "FY2023": 21376.2, "FY2022": 20945.3, "FY2021": 24898.5, "FY2020": 26434.8, "FY2019": 23252.0, "FY2018": 23316.7, "FY2017": 22571.4, "FY2016": 19266.7, "FY2015": 19062.5}),
        ("Total equity", {"FY2025": 2131.4, "FY2024": 1943.7, "FY2023": 1870.9, "FY2022": 1682.0, "FY2021": 1370.0, "FY2020": 1301.5, "FY2019": 1173.5, "FY2018": 1257.8, "FY2017": 1282.3, "FY2016": 956.9, "FY2015": 1075.0}),
    ],
    balance_sheet_unit="$m",
    income_statement_totals=[
        ("Total operating income", {"FY2025": 739.8, "FY2024": 572.1, "FY2023": 558.0, "FY2022": 809.9, "FY2021": 466.0, "FY2020": 489.1, "FY2019": 137.4, "FY2018": 384.0, "FY2017": 382.4, "FY2016": 286.2, "FY2015": 172.7}),
        ("Operating expenses", {"FY2025": -443.9, "FY2024": -382.4, "FY2023": -397.6, "FY2022": -373.6, "FY2021": -348.1, "FY2020": -351.5, "FY2019": -374.4, "FY2018": -379.1, "FY2017": -371.3, "FY2016": -382.9, "FY2015": -386.1}),
        ("Profit attributable to equity shareholders", {"FY2025": 224.9, "FY2024": 156.5, "FY2023": 187.1, "FY2022": 317.1, "FY2021": 98.6, "FY2020": 115.5, "FY2019": -248.2, "FY2018": -14.8, "FY2017": 29.7, "FY2016": -98.8, "FY2015": -267.7}),
    ],
    income_statement_unit="$m",
    equity_changes_totals=[
        ("Opening equity", {"FY2025": 1943.7, "FY2024": 1870.9, "FY2023": 1682.0, "FY2022": 1370.0, "FY2021": 1301.5, "FY2020": 1173.5, "FY2019": 1257.8, "FY2018": 1282.3, "FY2017": 956.9, "FY2016": 1075.0, "FY2015": 1015.1}),
        ("Total comprehensive income/(loss) for the year", {"FY2025": 241.9, "FY2024": 134.9, "FY2023": 201.1, "FY2022": 324.2, "FY2021": 80.7, "FY2020": 128.0, "FY2019": -244.2, "FY2018": -24.5, "FY2017": 60.4, "FY2016": -118.1, "FY2015": -281.0}),
        ("Other equity movements, net", {"FY2025": -54.2, "FY2024": -62.1, "FY2023": -12.2, "FY2022": -12.2, "FY2021": -12.2, "FY2020": 0.0, "FY2019": 159.9, "FY2018": 0.0, "FY2017": 265.0, "FY2016": 0.0, "FY2015": 340.9}),
    ],
    equity_changes_unit="$m",
    cash_flow_totals=[
        ("Cash flows (used in)/from operating activities", {"FY2025": -1780.3, "FY2024": 128.1, "FY2023": -2150.7, "FY2022": -1137.3, "FY2021": 2255.8, "FY2020": 282.0, "FY2019": 1127.4, "FY2018": -882.2, "FY2017": 1107.8, "FY2016": -2176.5, "FY2015": 1437.8}),
        ("Cash flows used in investing activities", {"FY2025": -18.0, "FY2024": -16.4, "FY2023": -6.9, "FY2022": -15.5, "FY2021": -12.5, "FY2020": -8.2, "FY2019": -17.9, "FY2018": -18.9, "FY2017": -15.6, "FY2016": -9.4, "FY2015": -2.0}),
        ("Cash flows used in financing activities", {"FY2025": -63.6, "FY2024": -70.6, "FY2023": -22.6, "FY2022": -21.9, "FY2021": -24.7, "FY2020": -16.0, "FY2019": -259.7, "FY2018": 0.0, "FY2017": 415.0, "FY2016": -137.9, "FY2015": 340.9}),
        ("Cash and cash equivalents at end of the year", {"FY2025": 902.6, "FY2024": 2762.0, "FY2023": 2744.4, "FY2022": 4990.4, "FY2021": 6122.5, "FY2020": 3906.4, "FY2019": 3648.1, "FY2018": 2792.6, "FY2017": 3692.8, "FY2016": 2134.6, "FY2015": 4476.2}),
    ],
    cash_flow_unit="$m",
    ratios=[
        ("CET1 Ratio", {"FY2025": "12.2%", "FY2024": "14.6%", "FY2023": "16.9%", "FY2022": "15.7%", "FY2021": "13.47%", "FY2020": "13.21%", "FY2019": "13.64%", "FY2018": "18.52%", "FY2017": "15.59%", "FY2016": "14.6%", "FY2015": "13.87%"}),
        ("Tier 1 Ratio", {"FY2025": "13.3%", "FY2024": "16.0%", "FY2023": "18.5%", "FY2022": "17.5%", "FY2021": "15.35%", "FY2020": "15.18%", "FY2019": "15.94%", "FY2018": "18.52%", "FY2017": "15.59%", "FY2016": "14.6%", "FY2015": "13.9%"}),
        ("Total Capital Ratio", {"FY2025": "15.0%", "FY2024": "18.1%", "FY2023": "21.1%", "FY2022": "20.2%", "FY2021": "18.28%", "FY2020": "18.26%", "FY2019": "19.54%", "FY2018": "22.25%", "FY2017": "19.97%", "FY2016": "19.3%", "FY2015": "19.13%"}),
        ("Leverage Ratio", {"FY2025": "5.6%", "FY2024": "6.9%", "FY2023": "7.7%", "FY2022": "7.7%", "FY2021": "5.09%", "FY2020": "4.90%", "FY2019": "4.78%", "FY2018": "5.02%", "FY2017": "4.91%", "FY2016": "4.66%", "FY2015": "5.36%"}),
        ("LCR", {"FY2025": "197.3%", "FY2024": "226.7%", "FY2023": "165.3%", "FY2022": "206.0%", "FY2021": "207%", "FY2020": "180%", "FY2019": "195%", "FY2018": "217%", "FY2017": "145%", "FY2016": "159%", "FY2015": "Not publicly disclosed"}),
        ("NSFR", {"FY2025": "122.8%", "FY2024": "136.4%", "FY2023": "183.3%", "FY2022": "163.8%", "FY2021": "Not disclosed", "FY2020": "Not disclosed", "FY2019": "Not disclosed", "FY2018": "Not disclosed", "FY2017": "Not disclosed", "FY2016": "Not disclosed", "FY2015": "Not disclosed"}),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own source "
         "citation for the underlying document/page. All amounts are in USD ($m), the reporting currency used "
         "throughout ICBC Standard Bank Plc's Annual Reports and Pillar 3 Disclosures. FY2015 is the entity's "
         "genuine historical floor (ICBC Standard Bank Plc was created 1 February 2015); pre-2018 figures reflect "
         "IAS 39 accounting and Basel III's transitional (non-KM1-template) Pillar 3 disclosure format - see the "
         "Balance Sheet, Profit & Loss, Asset Quality and Pillar 3 metric sheets' own source notes for the specific "
         "terminology/basis shifts (IAS 39→IFRS 9 in 2018, no Additional Tier 1 capital before December 2019, no "
         "UK NSFR requirement before 2022).",
)

bw.save("/Users/armaan/code/katalysis/banks/ICBC STANDARD BANK PLC FINANCIALS.xlsx")
