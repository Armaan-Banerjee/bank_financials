import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

# Aldermore Bank PLC (Companies House 00947662, FRN 204503) reports to a
# 30 June fiscal year end - "FY2025" below means the year ended 30 June 2025.
# Historical-depth extension (HD-047, 2026-09-05): extended back to FY2014
# (capped there by explicit user decision - see wayfinder/historical-depth
# ticket HD-047 - even though the Bank's real archive goes back to FY2009).
#
# Two structural quirks in the pre-2021 history, both explained in the
# per-sheet source notes below rather than papered over:
#   - Following the FirstRand acquisition (completed 14 Mar 2018), the Bank
#     changed its accounting reference date from 31 December to 30 June to
#     align with FirstRand Group. This produced one 18-MONTH set of
#     statutory accounts covering 1 Jan 2017 - 30 Jun 2018 ("FY2018" below)
#     instead of a normal 12-month FY2017 + FY2018. There is no standalone
#     12-month FY2017 period in the Bank's own disclosures at all, so
#     FY2017 is left blank throughout (a genuine self-skip, not an
#     oversight) and FY2018's column is an 18-month, not 12-month, period.
#   - No standalone Pillar 3 disclosure document could be located (via the
#     Bank's own site, Wayback Machine CDX search, or web search) for
#     FY2016 or FY2020 specifically, despite real effort - only a single
#     "CET1 ratio" headline figure survives for each in that year's own
#     Annual Report "Financial highlights" page. Balance Sheet/P&L/Cash
#     Flow/Equity/Asset Quality are unaffected (sourced from Companies
#     House statutory accounts, which exist for every year except FY2017)
#     but the other Pillar 3 metric sheets and RWA Breakdown are left
#     blank for FY2016 and FY2020.
YEARS = [
    "FY2025", "FY2024", "FY2023", "FY2022", "FY2021",
    "FY2020", "FY2019", "FY2018", "FY2017", "FY2016", "FY2015", "FY2014",
]
YEAR_LABEL = {
    "FY2025": "FY2025 (y/e 30 Jun 25)",
    "FY2024": "FY2024 (y/e 30 Jun 24)",
    "FY2023": "FY2023 (y/e 30 Jun 23)",
    "FY2022": "FY2022 (y/e 30 Jun 22)",
    "FY2021": "FY2021 (y/e 30 Jun 21)",
    "FY2020": "FY2020 (y/e 30 Jun 20)",
    "FY2019": "FY2019 (y/e 30 Jun 19)",
    "FY2018": "FY2018 (18-month transition period, 1 Jan 17 - 30 Jun 18)",
    "FY2017": "FY2017 (no standalone 12-month period - see note)",
    "FY2016": "FY2016 (y/e 31 Dec 16)",
    "FY2015": "FY2015 (y/e 31 Dec 15)",
    "FY2014": "FY2014 (y/e 31 Dec 14)",
}

CH_2025_URL = "https://find-and-update.company-information.service.gov.uk/company/00947662/filing-history/MzQ4NzM5MDg2MWFkaXF6a2N4/document?format=pdf&download=0"
CH_2024_URL = "https://find-and-update.company-information.service.gov.uk/company/00947662/filing-history/MzQ0MDgwMDc3OWFkaXF6a2N4/document?format=pdf&download=0"
CH_2023_URL = "https://find-and-update.company-information.service.gov.uk/company/00947662/filing-history/MzM5ODA0OTgzOWFkaXF6a2N4/document?format=pdf&download=0"
CH_2022_URL = "https://find-and-update.company-information.service.gov.uk/company/00947662/filing-history/MzM1NTc2ODMxMmFkaXF6a2N4/document?format=pdf&download=0"
CH_2021_URL = "https://find-and-update.company-information.service.gov.uk/company/00947662/filing-history/MzMxODkyMzc2MWFkaXF6a2N4/document?format=pdf&download=0"
CH_2020_URL = "https://find-and-update.company-information.service.gov.uk/company/00947662/filing-history/MzI4MzMzMzM4OGFkaXF6a2N4/document?format=pdf&download=0"
CH_2019_URL = "https://find-and-update.company-information.service.gov.uk/company/00947662/filing-history/MzI0OTY0MTQwMWFkaXF6a2N4/document?format=pdf&download=0"
CH_2018_URL = "https://find-and-update.company-information.service.gov.uk/company/00947662/filing-history/MzIxNzQ4NDUzNmFkaXF6a2N4/document?format=pdf&download=0"
CH_2016_URL = "https://find-and-update.company-information.service.gov.uk/company/00947662/filing-history/MzE3NTQ0MTgwOGFkaXF6a2N4/document?format=pdf&download=0"
CH_2015_URL = "https://find-and-update.company-information.service.gov.uk/company/00947662/filing-history/MzE0OTEzMjU1M2FkaXF6a2N4/document?format=pdf&download=0"

P3_2025_URL = "https://www.aldermore.co.uk/media/sgufisw5/aldermore-group-plc-2025-pillar-3-disclosures.pdf"
P3_2024_URL = "https://www.aldermore.co.uk/media/jkkdbgnu/aldermore-group-plc-2024-pillar-3-disclosures.pdf"
P3_2022_URL = "https://www.aldermore.co.uk/media/hnhpw03l/pillar-3-2022_0.pdf"
P3_2019_URL = "https://www.aldermore.co.uk/media/2prbumkj/aldermore-group-plc-pillar-3-disclosure-document-at-30-june-2019.pdf"
P3_2015_URL = "https://www.aldermore.co.uk/media/ot5axgnp/pillar-3-disclosure-dec-2015.pdf"
INTERIM_P3_2025_URL = "https://www.aldermore.co.uk/media/xx1fg0me/half-year-pillar-3-disclosures-31-dec-2025.pdf"

CASH_FLOW_SOURCES = (
    "Sources — Aldermore Bank PLC (company solo, not the Aldermore Group PLC holding company), "
    "Statement of cash flows from each year's full statutory accounts filed at Companies House "
    "(company no. 00947662), £m:\n"
    f"FY2025 & FY2024 (restated): Full accounts made up to 30 June 2025, filed 04 Nov 2025, p.55 — {CH_2025_URL}\n"
    f"FY2023: Full accounts made up to 30 June 2023, filed 27 Oct 2023, p.53 — {CH_2023_URL}\n"
    f"FY2022: Full accounts made up to 30 June 2022, filed 19 Oct 2022, p.60 — {CH_2022_URL}\n"
    f"FY2021: Full accounts made up to 30 June 2021, filed 04 Nov 2021, p.59 — {CH_2021_URL}\n"
    f"FY2020: Full accounts for the year ended 30 June 2020, filed 13 Nov 2020, p.62 — {CH_2020_URL}\n"
    f"FY2019 & FY2018 (18-month period ended 30 Jun 2018): Full accounts for the year ended 30 June 2019, "
    f"filed 22 Nov 2019, p.51 — {CH_2019_URL}\n"
    f"FY2016 & FY2015: Full accounts for the year ended 31 December 2016, filed 11 May 2017, p.28 — {CH_2016_URL}\n"
    f"FY2014: Full accounts for the year ended 31 December 2015, filed 23 May 2016, p.78 (FY2014 comparative) — {CH_2015_URL}\n"
    "(FY2024 accounts as originally filed are superseded by the FY2025 accounts' restated FY2024 comparative used here — "
    f"{CH_2024_URL})\n"
    "FY2017 has no standalone 12-month cash flow statement (see YEARS comment above); FY2018's column is an "
    "18-month period (1 Jan 2017 - 30 Jun 2018), not a 12-month year, so its flows are roughly 1.5x a normal "
    "year's and are not directly comparable to the years either side of it without adjusting for the extra "
    "6 months.\n"
    "Note: the Bank reclassified its FY2024 comparative cash flow statement (see FY2025 accounts, p.55) to move interest "
    "received/paid on the intercompany loan, interest paid on subordinated notes, and interest received on debt "
    "securities from investing/financing activities into operating activities, and to reclassify proceeds from disposal "
    "of a non-current asset held for sale into operating activities; amounts relating to intercompany loans are also now "
    "presented gross rather than net. FY2023/FY2022/FY2021 below are presented as originally filed under the older "
    "(pre-reclassification) basis. Blank cells indicate a line item was not part of that year's classification of cash "
    "flows; section totals (net cash from operating/investing/financing activities, net change, opening/closing cash) "
    "are directly as reported and comparable across all 5 years. Minor (≤£0.1m) differences between individual line "
    "items and their printed subtotals in the FY2023/FY2022 source documents are presented as disclosed, not adjusted."
)

def p3_sources(page_25="4", page_24="4", page_22="4"):
    return (
        "Sources — Aldermore Bank PLC solo figures from the 'Key metrics'/capital-composition tables (Bank "
        "columns), Aldermore Group PLC Pillar 3 Disclosures (and the Bank's own Annual Report highlights where "
        "noted):\n"
        f"FY2025 & FY2024: Pillar 3 Disclosures for the year ended 30 June 2025, p.{page_25} (Key metrics) — {P3_2025_URL}\n"
        f"FY2023: Pillar 3 Disclosures for the year ended 30 June 2024, p.{page_24} (Key metrics, FY2023 comparative) — {P3_2024_URL}\n"
        f"FY2022 & FY2021: Pillar 3 Disclosures for the year ended 30 June 2022, p.{page_22} (Key metrics) — {P3_2022_URL}\n"
        f"FY2019 & FY2018: Pillar 3 Disclosures for the year ended 30 June 2019, p.57-61 (Appendix 1, Disclosures "
        f"for Aldermore Bank PLC — Total minimum Pillar 1 capital requirement, Capital composition, Leverage "
        f"ratio) — {P3_2019_URL}\n"
        f"FY2015 & FY2014: Pillar 3 Disclosures 31 December 2015, p.58-61 (Appendix 1, Disclosures for Aldermore "
        f"Bank PLC — Total minimum Pillar 1 capital requirement, Capital composition, Leverage ratio) — {P3_2015_URL}\n"
        "FY2016 and FY2020: no standalone Pillar 3 disclosure document could be located for these two years "
        "specifically (checked the Bank's own site, Wayback Machine CDX search, and web search) — only the "
        "single headline CET1 ratio survives, from each year's own Annual Report 'Financial highlights' page "
        "(FY2016: Full accounts for the year ended 31 December 2016, p.4; FY2020: Full accounts for the year "
        "ended 30 June 2020, p.4). Other Pillar 3 metrics (Tier 1/Total capital, RWAs, leverage) are left blank "
        "for FY2016 and FY2020 rather than estimated.\n"
        "FY2017 has no standalone Pillar 3 disclosure at all (see YEARS comment above — no 12-month FY2017 "
        "period exists in the Bank's disclosures); FY2018's column reflects the 18-month transition period."
    )

bw = BankWorkbook(bank_name="Aldermore Bank PLC", years=YEARS, year_label=YEAR_LABEL, header_color="AD1457")

# ---------------------------------------------------------------
# Sheet: Balance Sheet (Statement of Financial Position)
# ---------------------------------------------------------------
BALANCE_SHEET_SOURCES = (
    "Sources — Aldermore Bank PLC (company solo, not the Aldermore Group PLC holding company), Statement of "
    "financial position from each year's full statutory accounts filed at Companies House (company no. 00947662), "
    "£m:\n"
    f"FY2025 & FY2024: Full accounts made up to 30 June 2025, filed 04 Nov 2025, p.54 — {CH_2025_URL}\n"
    f"FY2023 & FY2022: Full accounts made up to 30 June 2023, filed 27 Oct 2023, p.52 — {CH_2023_URL}\n"
    f"FY2021: Full accounts made up to 30 June 2021, filed 04 Nov 2021, p.58 — {CH_2021_URL}\n"
    f"FY2020: Full accounts for the year ended 30 June 2020, filed 13 Nov 2020, p.61 — {CH_2020_URL}\n"
    f"FY2019 & FY2018: Full accounts for the year ended 30 June 2019, filed 22 Nov 2019, p.49 — {CH_2019_URL}\n"
    f"FY2016 & FY2015: Full accounts for the year ended 31 December 2016, filed 11 May 2017, p.27 — {CH_2016_URL}\n"
    f"FY2014: Full accounts for the year ended 31 December 2015, filed 23 May 2016, p.77 (FY2014 comparative) — {CH_2015_URL}\n"
    "FY2017 has no standalone 12-month Statement of financial position: following the Bank's 2018 acquisition by "
    "FirstRand, its accounting reference date changed from 31 December to 30 June, producing one 18-month set of "
    "accounts (1 Jan 2017 - 30 Jun 2018, shown here as FY2018) instead of a normal FY2017 + FY2018 pair — FY2017 "
    "is left blank rather than estimated. FY2018's column is therefore an 18-month, not 12-month, snapshot; as a "
    "balance-sheet (point-in-time) statement this affects comparability less than the flow statements, but the "
    "period length difference should still be borne in mind when reading growth between FY2016 and FY2018.\n"
    "Note: minor (£0.1m) rounding differences appear between the Total equity figure on the face of the "
    "Statement of financial position and the Statement of Changes in Equity's closing balance in some years "
    "(e.g. FY2021: £987.1m here vs £987.2m per the FY2021 accounts' own Statement of Changes in Equity) — "
    "both are presented exactly as disclosed in their respective source tables, not reconciled."
)

balance_sheet_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and balances at central banks", {"FY2025": 1182.3, "FY2024": 2172.2, "FY2023": 1923.4, "FY2022": 838.3, "FY2021": 688.5, "FY2020": 542.4, "FY2019": 482.9, "FY2018": 508.8, "FY2016": 116.4, "FY2015": 105.3, "FY2014": 79.6}),
    ("DATA", "Loans and advances to banks", {"FY2025": 183.6, "FY2024": 170.1, "FY2023": 206.5, "FY2022": 132.8, "FY2021": 106.4, "FY2020": 177.5, "FY2019": 110.6, "FY2018": 80.4, "FY2016": 43.4, "FY2015": 64.0, "FY2014": 86.8}),
    ("DATA", "Amounts owed by / receivable from other Group undertakings", {"FY2025": 3779.6, "FY2024": 3720.5, "FY2023": 3525.1, "FY2022": 3072.5, "FY2021": 2303.8, "FY2020": 1615.2, "FY2019": 390.7, "FY2018": 20.7, "FY2016": 1.5, "FY2015": 0.9, "FY2014": 1.6}),
    ("DATA", "Debt securities", {"FY2025": 2704.2, "FY2024": 2436.5, "FY2023": 2048.9, "FY2022": 2339.2, "FY2021": 1999.5, "FY2020": 1941.1, "FY2019": 1207.8, "FY2018": 829.9, "FY2016": 699.8, "FY2015": 640.1, "FY2014": 542.3}),
    ("DATA", "Derivatives held for risk management", {"FY2025": 170.1, "FY2024": 344.2, "FY2023": 666.3, "FY2022": 259.9, "FY2021": 18.9, "FY2020": 9.1, "FY2019": 9.1, "FY2018": 24.0, "FY2016": 17.5, "FY2015": 17.5, "FY2014": 25.6}),
    ("DATA", "Loans and advances to customers", {"FY2025": 12523.4, "FY2024": 11416.3, "FY2023": 10998.9, "FY2022": 10777.3, "FY2021": 10393.6, "FY2020": 10602.2, "FY2019": 10230.3, "FY2018": 8990.5, "FY2016": 7477.3, "FY2015": 6144.8, "FY2014": 4801.1}),
    ("DATA", "Fair value adjustment for portfolio hedged risk", {"FY2025": 18.8, "FY2024": -129.0, "FY2023": -400.1, "FY2022": -180.2, "FY2021": 15.2, "FY2020": 55.8, "FY2019": 17.9, "FY2018": -15.7, "FY2016": -3.5, "FY2015": 1.1}),
    ("DATA", "Non-current assets held for sale", {"FY2023": 32.8}),
    ("DATA", "Other assets", {"FY2025": 2.8, "FY2024": 9.2, "FY2023": 6.0, "FY2022": 1.6, "FY2021": 2.0, "FY2020": 0, "FY2019": 2.8, "FY2018": 6.4, "FY2016": 3.7, "FY2015": 2.5, "FY2014": 4.7}),
    ("DATA", "Prepayments and accrued income", {"FY2025": 23.6, "FY2024": 22.8, "FY2023": 17.8, "FY2022": 14.5, "FY2021": 13.3, "FY2020": 11.3, "FY2019": 5.3, "FY2018": 6.2, "FY2016": 3.4, "FY2015": 5.1, "FY2014": 6.7}),
    ("DATA", "Taxation asset", {"FY2025": 2.9, "FY2024": 2.2, "FY2023": 0, "FY2022": 7.0, "FY2021": 0.7, "FY2020": 11.8}),
    ("DATA", "Deferred taxation", {"FY2025": 6.3, "FY2024": 5.7, "FY2023": 6.1, "FY2022": 2.6, "FY2021": 5.7, "FY2020": 3.4, "FY2019": 3.7, "FY2018": 2.3, "FY2016": 12.0, "FY2015": 16.9, "FY2014": 6.4}),
    ("DATA", "Property, plant and equipment", {"FY2025": 16.3, "FY2024": 20.5, "FY2023": 15.7, "FY2022": 20.8, "FY2021": 25.8, "FY2020": 23.2, "FY2019": 3.8, "FY2018": 3.7, "FY2016": 3.1, "FY2015": 3.4, "FY2014": 2.8}),
    ("DATA", "Intangible assets", {"FY2025": 4.3, "FY2024": 4.3, "FY2023": 4.3, "FY2022": 4.5, "FY2021": 9.6, "FY2020": 7.7, "FY2019": 7.0, "FY2018": 10.2, "FY2016": 21.9, "FY2015": 19.8, "FY2014": 18.4}),
    ("TOTAL", "Total assets", {"FY2025": 20618.2, "FY2024": 20195.5, "FY2023": 19051.7, "FY2022": 17290.8, "FY2021": 15583.0, "FY2020": 15000.7, "FY2019": 12471.9, "FY2018": 10467.4, "FY2016": 8396.5, "FY2015": 7021.4, "FY2014": 5583.2}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Amounts due to banks", {"FY2025": 795.8, "FY2024": 1365.3, "FY2023": 1681.9, "FY2022": 1341.8, "FY2021": 1326.6, "FY2020": 2173.5, "FY2019": 1814.6, "FY2018": 1678.2, "FY2016": 753.8, "FY2015": 405.1, "FY2014": 305.9}),
    ("DATA", "Customers' accounts", {"FY2025": 17047.6, "FY2024": 16306.7, "FY2023": 15033.3, "FY2022": 14105.4, "FY2021": 12427.3, "FY2020": 10886.4, "FY2019": 8971.8, "FY2018": 7776.3, "FY2016": 6673.7, "FY2015": 5742.0, "FY2014": 4459.0}),
    ("DATA", "Derivatives held for risk management", {"FY2025": 94.1, "FY2024": 37.8, "FY2023": 62.5, "FY2022": 24.5, "FY2021": 40.0, "FY2020": 93.2, "FY2019": 36.6, "FY2018": 16.6, "FY2016": 35.3, "FY2015": 35.2, "FY2014": 53.5}),
    ("DATA", "Fair value adjustment for portfolio hedged risk", {"FY2025": 16.4, "FY2024": 6.5, "FY2023": -21.0, "FY2022": -12.7, "FY2021": 0, "FY2020": 2.1, "FY2019": 1.0, "FY2018": 0.2, "FY2016": -1.2, "FY2015": -0.8, "FY2014": 1.5}),
    ("DATA", "Amounts owed / payable to other Group undertakings", {"FY2025": 952.5, "FY2024": 909.2, "FY2023": 862.0, "FY2022": 531.5, "FY2021": 537.2, "FY2020": 714.4, "FY2019": 550.9, "FY2018": 104.5, "FY2016": 153.1, "FY2015": 213.4, "FY2014": 302.7}),
    ("DATA", "Other liabilities, accruals and deferred income", {"FY2025": 93.3, "FY2024": 96.7, "FY2023": 105.2, "FY2022": 97.9, "FY2021": 92.4, "FY2020": 71.2, "FY2019": 62.0, "FY2018": 57.6, "FY2016": 51.9, "FY2015": 47.5, "FY2014": 38.8}),
    ("DATA", "Taxation liability", {"FY2023": 6.0, "FY2020": 0, "FY2019": 18.3, "FY2018": 5.8, "FY2016": 9.7, "FY2015": 12.5, "FY2014": 8.2}),
    ("DATA", "Provisions", {"FY2025": 3.0, "FY2024": 0.6, "FY2023": 2.5, "FY2022": 3.8, "FY2021": 2.7, "FY2020": 2.5, "FY2019": 2.4, "FY2018": 1.0, "FY2016": 0.8, "FY2015": 1.1, "FY2014": 2.0}),
    ("DATA", "Debt securities in issue", {"FY2023": -0.2, "FY2022": -0.5}),
    ("DATA", "Subordinated notes", {"FY2025": 100.9, "FY2024": 100.9, "FY2023": 100.5, "FY2022": 100.5, "FY2021": 161.4, "FY2020": 161.2, "FY2019": 161.1, "FY2018": 60.5, "FY2016": 100.0, "FY2015": 38.1, "FY2014": 36.8}),
    ("TOTAL", "Total liabilities", {"FY2025": 17050.8, "FY2024": 18823.7, "FY2023": 17832.7, "FY2022": 16192.2, "FY2021": 14595.9, "FY2020": 14104.5, "FY2019": 11618.7, "FY2018": 9700.7, "FY2016": 7777.1, "FY2015": 6494.1, "FY2014": 5208.4}),
    ("SECTION", "Equity", {}),
    ("DATA", "Share capital", {"FY2025": 3.3, "FY2024": 3.3, "FY2023": 3.3, "FY2022": 3.3, "FY2021": 3.3, "FY2020": 3.3, "FY2019": 3.3, "FY2018": 3.3, "FY2016": 3.3, "FY2015": 3.3, "FY2014": 3.3}),
    ("DATA", "Share premium account", {"FY2025": 307.5, "FY2024": 307.5, "FY2023": 307.5, "FY2022": 307.5, "FY2021": 307.5, "FY2020": 307.5, "FY2019": 307.6, "FY2018": 307.6, "FY2016": 307.6, "FY2015": 307.6, "FY2014": 233.4}),
    ("DATA", "Additional Tier 1 capital", {"FY2025": 50.0, "FY2024": 61.0, "FY2023": 61.0, "FY2022": 61.0, "FY2021": 61.0, "FY2020": 61.0, "FY2019": 74.3, "FY2018": 74.3, "FY2016": 74.3, "FY2015": 74.3, "FY2014": 74.3}),
    ("DATA", "Capital contribution / redemption reserve", {"FY2018": 0, "FY2016": 6.9, "FY2015": 3.4, "FY2014": 3.1}),
    ("DATA", "FVOCI / fair value through other comprehensive income reserve", {"FY2025": -5.0, "FY2024": -0.7, "FY2023": 3.3, "FY2022": 6.9, "FY2021": 8.3, "FY2020": 1.5, "FY2019": 0.4, "FY2018": 1.1, "FY2016": 1.8, "FY2015": -1.0, "FY2014": 1.4}),
    ("DATA", "Retained earnings", {"FY2025": 1158.8, "FY2024": 1000.7, "FY2023": 843.9, "FY2022": 719.9, "FY2021": 607.0, "FY2020": 522.9, "FY2019": 467.6, "FY2018": 380.4, "FY2016": 225.5, "FY2015": 139.7, "FY2014": 59.3}),
    ("TOTAL", "Total equity", {"FY2025": 1514.6, "FY2024": 1371.8, "FY2023": 1219.0, "FY2022": 1098.6, "FY2021": 987.1, "FY2020": 896.2, "FY2019": 853.2, "FY2018": 766.7, "FY2016": 619.4, "FY2015": 527.3, "FY2014": 374.8}),
    ("TOTAL", "Total liabilities and equity", {"FY2025": 20618.2, "FY2024": 20195.5, "FY2023": 19051.7, "FY2022": 17290.8, "FY2021": 15583.0, "FY2020": 15000.7, "FY2019": 12471.9, "FY2018": 10467.4, "FY2016": 8396.5, "FY2015": 7021.4, "FY2014": 5583.2}),
]

bw.add_balance_sheet_sheet(
    title="Aldermore Bank PLC — Statement of Financial Position",
    subtitle="Company (Bank solo) basis, £m, as at 30 June",
    rows=balance_sheet_rows,
    sources_text=BALANCE_SHEET_SOURCES,
    first_col_width=72,
    source_height=150,
    unit_suffix=" (£m)",
)

# ---------------------------------------------------------------
# Sheet: Profit & Loss (Income Statement + Statement of Comprehensive Income)
# ---------------------------------------------------------------
INCOME_STATEMENT_SOURCES = (
    "Sources — Aldermore Bank PLC (company solo, not the Aldermore Group PLC holding company), Income "
    "statement and Statement of comprehensive income from each year's full statutory accounts filed at "
    "Companies House (company no. 00947662), £m:\n"
    f"FY2025 & FY2024: Full accounts made up to 30 June 2025, filed 04 Nov 2025, p.53 — {CH_2025_URL}\n"
    f"FY2023 & FY2022: Full accounts made up to 30 June 2023, filed 27 Oct 2023, p.50-51 — {CH_2023_URL}\n"
    f"FY2021: Full accounts made up to 30 June 2021, filed 04 Nov 2021, p.56-57 — {CH_2021_URL}\n"
    f"FY2020: Full accounts for the year ended 30 June 2020, filed 13 Nov 2020, p.59-60 — {CH_2020_URL}\n"
    f"FY2019 & FY2018: Full accounts for the year ended 30 June 2019, filed 22 Nov 2019, p.47-48 — {CH_2019_URL}\n"
    f"FY2016 & FY2015: Full accounts for the year ended 31 December 2016, filed 11 May 2017, p.25-26 — {CH_2016_URL}\n"
    f"FY2014: Full accounts for the year ended 31 December 2015, filed 23 May 2016, p.75-76 (FY2014 comparative) — {CH_2015_URL}\n"
    "FY2019's interest income/expense and net gains from derivatives comparative for FY2018 (period ended 30 June "
    "2018) were restated to align with FirstRand Group policy (total operating income unaffected) — the FY2018 "
    "figures here are the restated ones as re-presented in the FY2019 accounts, not the FY2018 accounts' own "
    "as-originally-filed figures (which had interest income £607.4m, interest expense £(172.5)m).\n"
    "FY2017 has no standalone 12-month period (see YEARS comment above); FY2018's column is an 18-month period "
    "(1 Jan 2017 - 30 Jun 2018), not a 12-month year, so flow figures (income, expenses, profit) are not directly "
    "comparable to the 12-month years either side of it without adjusting for the extra 6 months.\n"
    "Note: each year's own presentation of 'below net-interest-income' income/expense line items differs "
    "(IPO preparation costs in FY2014-FY2016; goodwill impairment in FY2016; transaction/integration costs and "
    "intangible/goodwill impairment in FY2018-FY2019; a combined single 'Administrative expenses' line from "
    "FY2022) — all are transcribed as disclosed in their own year, not restated onto a common basis, and each "
    "year's own reported subtotals/totals are used directly rather than recomputed from the line items shown."
)

income_statement_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest income", {"FY2025": 1240.5, "FY2024": 1234.8, "FY2023": 878.7, "FY2022": 533.4, "FY2021": 473.6, "FY2020": 513.5, "FY2019": 470.1, "FY2018": 599.6, "FY2016": 362.3, "FY2015": 306.2, "FY2014": 235.2}),
    ("DATA", "Interest expense", {"FY2025": -828.0, "FY2024": -808.1, "FY2023": -433.6, "FY2022": -152.5, "FY2021": -157.3, "FY2020": -201.9, "FY2019": -150.3, "FY2018": -168.3, "FY2016": -119.4, "FY2015": -103.6, "FY2014": -92.7}),
    ("TOTAL", "Net interest income", {"FY2025": 412.5, "FY2024": 426.7, "FY2023": 445.1, "FY2022": 380.9, "FY2021": 316.3, "FY2020": 311.6, "FY2019": 319.8, "FY2018": 431.3, "FY2016": 242.9, "FY2015": 202.6, "FY2014": 142.5}),
    ("DATA", "Fee and commission income / fee and other income", {"FY2025": 7.5, "FY2024": 7.1, "FY2023": 11.7, "FY2022": 6.0, "FY2021": 6.5, "FY2020": 5.8, "FY2019": 7.4, "FY2018": 36.6, "FY2016": 30.0, "FY2015": 25.2, "FY2014": 26.4}),
    ("DATA", "Fee and commission expense", {"FY2025": -9.5, "FY2024": -8.2, "FY2023": -5.4, "FY2022": -5.6, "FY2021": -5.4, "FY2020": -5.8, "FY2019": -5.4, "FY2018": -11.0, "FY2016": -7.5, "FY2015": -7.0, "FY2014": -7.8}),
    ("DATA", "Net gains/(losses) from derivatives and other financial instruments at fair value through profit or loss", {"FY2025": 12.6, "FY2024": -3.0, "FY2023": 12.6, "FY2022": -5.3, "FY2021": -3.1, "FY2020": -5.2, "FY2019": 3.2, "FY2018": 1.2, "FY2016": -9.7, "FY2015": -9.1, "FY2014": -5.5}),
    ("DATA", "Net gains on disposal of financial assets at fair value through other comprehensive income", {"FY2025": 1.1, "FY2024": 2.0, "FY2023": 2.1, "FY2022": 0.2, "FY2021": 0.7, "FY2020": -0.1, "FY2019": 0.2, "FY2018": 1.2, "FY2016": 3.8, "FY2015": 2.3, "FY2014": 2.9}),
    ("DATA", "Net gains on financial assets at amortised cost", {"FY2024": 0.2}),
    ("DATA", "Other operating income", {"FY2025": 49.2, "FY2024": 38.1, "FY2023": 10.1, "FY2022": 13.6, "FY2021": 8.4, "FY2020": 6.8, "FY2019": 6.6, "FY2018": 9.2, "FY2016": 6.4, "FY2015": 7.6, "FY2014": 7.6}),
    ("TOTAL", "Total operating income", {"FY2025": 473.4, "FY2024": 462.9, "FY2023": 476.2, "FY2022": 389.8, "FY2021": 323.4, "FY2020": 313.1, "FY2019": 331.8, "FY2018": 468.5, "FY2016": 265.9, "FY2015": 221.6, "FY2014": 166.1}),
    ("SECTION", "Expenses", {}),
    ("DATA", "Provisions", {"FY2025": -3.0, "FY2024": 1.2, "FY2023": -2.0, "FY2022": -2.1, "FY2021": -1.7, "FY2020": -0.5, "FY2019": -1.2, "FY2018": -1.2, "FY2016": -0.8, "FY2015": -2.3, "FY2014": -3.6}),
    ("DATA", "Costs in preparation for Aldermore Group PLC initial public offering", {"FY2015": -0.4, "FY2014": -5.9}),
    ("DATA", "Impairment of goodwill", {"FY2016": -4.1}),
    ("DATA", "Impairment of intangibles and goodwill", {"FY2019": -0.7, "FY2018": -14.2}),
    ("DATA", "Transaction costs", {"FY2018": -3.7}),
    ("DATA", "Integration costs", {"FY2019": -4.6, "FY2018": -2.4}),
    ("DATA", "Other expenses and staff costs / other administrative expenses", {"FY2025": -263.8, "FY2024": -265.0, "FY2023": -251.5, "FY2022": -221.9, "FY2021": -172.0, "FY2020": -148.1, "FY2019": -162.9, "FY2018": -206.3, "FY2016": -112.9, "FY2015": -107.4, "FY2014": -91.3}),
    ("DATA", "Depreciation and amortisation", {"FY2021": -7.3, "FY2020": -6.7, "FY2019": -4.6, "FY2018": -8.4, "FY2016": -5.3, "FY2015": -5.3, "FY2014": -3.9}),
    ("TOTAL", "Administrative expenses", {"FY2025": -266.8, "FY2024": -263.8, "FY2023": -253.5, "FY2022": -224.0, "FY2021": -173.7, "FY2020": -148.7, "FY2019": -169.4, "FY2018": -227.8, "FY2016": -117.8, "FY2015": -110.1, "FY2014": -100.8}),
    ("TOTAL", "Operating profit before impairment losses", {"FY2025": 206.6, "FY2024": 199.1, "FY2023": 222.6, "FY2022": 165.8, "FY2021": 142.4, "FY2020": 157.7, "FY2019": 157.8, "FY2018": 232.3, "FY2016": 142.8, "FY2015": 106.2, "FY2014": 61.4}),
    ("DATA", "Impairment releases/(losses) on loans and advances to customers", {"FY2025": 14.1, "FY2024": 19.1, "FY2023": -51.4, "FY2022": -5.1, "FY2021": -26.7, "FY2020": -65.1, "FY2019": -20.1, "FY2018": -19.5, "FY2016": -15.5, "FY2015": -10.4, "FY2014": -9.6}),
    ("DATA", "Impairment losses on lease modifications", {"FY2021": 0, "FY2020": -11.0}),
    ("TOTAL", "Profit before taxation", {"FY2025": 220.7, "FY2024": 218.2, "FY2023": 171.2, "FY2022": 160.7, "FY2021": 115.7, "FY2020": 81.6, "FY2019": 137.7, "FY2018": 212.8, "FY2016": 127.3, "FY2015": 95.8, "FY2014": 51.8}),
    ("DATA", "Taxation", {"FY2025": -57.5, "FY2024": -56.1, "FY2023": -42.0, "FY2022": -42.7, "FY2021": -26.4, "FY2020": -17.4, "FY2019": -35.5, "FY2018": -56.9, "FY2016": -35.0, "FY2015": -15.7, "FY2014": -12.1}),
    ("TOTAL", "Profit after taxation — attributable to equity holders of the Company/Bank", {"FY2025": 163.2, "FY2024": 162.1, "FY2023": 129.2, "FY2022": 118.0, "FY2021": 89.3, "FY2020": 64.2, "FY2019": 102.2, "FY2018": 155.9, "FY2016": 92.3, "FY2015": 80.1, "FY2014": 39.7}),
    ("SECTION", "Other comprehensive income", {}),
    ("DATA", "FVOCI debt securities: Fair value movements", {"FY2025": -4.6, "FY2024": -3.3, "FY2023": -2.7, "FY2022": -2.2, "FY2021": 10.3, "FY2020": 1.8, "FY2019": -0.2, "FY2018": 0.3, "FY2016": 7.6, "FY2015": -0.9, "FY2014": 3.5}),
    ("DATA", "FVOCI debt securities: Amounts transferred to the income statement", {"FY2025": -1.1, "FY2024": -2.0, "FY2023": -2.1, "FY2022": -0.2, "FY2021": -0.7, "FY2020": -0.5, "FY2019": -0.8, "FY2018": -1.2, "FY2016": -3.8, "FY2015": -2.1, "FY2014": -2.5}),
    ("DATA", "Taxation on other comprehensive income", {"FY2025": 1.4, "FY2024": 1.3, "FY2023": 1.3, "FY2022": 1.0, "FY2021": -2.8, "FY2020": -0.3, "FY2019": 0.3, "FY2018": None, "FY2016": -1.0, "FY2015": 0.6, "FY2014": -0.2}),
    ("TOTAL", "Total other comprehensive (expense)/income", {"FY2025": -4.3, "FY2024": -4.0, "FY2023": -3.6, "FY2022": -1.4, "FY2021": 6.8, "FY2020": 1.0, "FY2019": -0.7, "FY2018": -0.7, "FY2016": 2.8, "FY2015": -2.4, "FY2014": 0.8}),
    ("TOTAL", "Total comprehensive income attributable to equity holders of the Bank", {"FY2025": 158.9, "FY2024": 158.1, "FY2023": 125.7, "FY2022": 116.6, "FY2021": 96.1, "FY2020": 65.2, "FY2019": 101.5, "FY2018": 155.2, "FY2016": 95.1, "FY2015": 77.7, "FY2014": 40.5}),
]

bw.add_income_statement_sheet(
    title="Aldermore Bank PLC — Income Statement and Statement of Comprehensive Income",
    subtitle="Company (Bank solo) basis, £m, year ended 30 June",
    rows=income_statement_rows,
    sources_text=INCOME_STATEMENT_SOURCES,
    first_col_width=78,
    source_height=150,
    unit_suffix=" (£m)",
)

# ---------------------------------------------------------------
# Sheet: Statement of Changes in Equity
# ---------------------------------------------------------------
EQUITY_CHANGES_SOURCES = (
    "Sources — Aldermore Bank PLC (company solo) Statement of changes in equity from each year's full "
    "statutory accounts filed at Companies House (company no. 00947662), £m:\n"
    f"FY2025 & FY2024: Full accounts made up to 30 June 2025, filed 04 Nov 2025, p.56 — {CH_2025_URL}\n"
    f"FY2023 & FY2022: Full accounts made up to 30 June 2023, filed 27 Oct 2023, p.54 — {CH_2023_URL}\n"
    f"FY2021 & FY2020: Full accounts made up to 30 June 2021, filed 04 Nov 2021, p.60 — {CH_2021_URL}\n"
    f"FY2019 & FY2018 (18-month period ended 30 Jun 2018): Full accounts for the year ended 30 June 2019, "
    f"filed 22 Nov 2019, p.52 — {CH_2019_URL}\n"
    f"FY2016 & FY2015: Full accounts for the year ended 31 December 2016, filed 11 May 2017, p.29 — {CH_2016_URL}\n"
    f"FY2014: Full accounts for the year ended 31 December 2015, filed 23 May 2016, p.79 (FY2014 comparative) — {CH_2015_URL}\n"
    "Chronological roll-forward, oldest to newest. 'As at 30 June 2021' shows £987.2m in the FY2021 accounts' "
    "own Statement of Changes in Equity vs £987.1m on the face of the FY2021 Statement of Financial Position "
    "— a £0.1m rounding difference in the Bank's own disclosures, both transcribed as reported. A similar sub-"
    "£0.1m rounding gap exists between the 'As at 30 June 2020' close (896.2, tying to the FY2020 accounts) and "
    "the 'As at 1 July 2020' opening carried over from the FY2022 accounts' own comparative roll-forward "
    "(FVOCI reserve 1.5 vs 1.4) — both reproduced exactly as each source states them, not reconciled.\n"
    "FY2017 has no standalone 12-month roll-forward: following the Bank's change of accounting reference date "
    "(see YEARS comment above), the roll-forward jumps directly from 'As at 31 December 2016' (year-end under "
    "the old Dec-FYE) to 'As at 1 January 2017' opening a single 18-month movement to 'As at 30 June 2018' — "
    "there is no 31 December 2017 balance in the Bank's own disclosures. The 'Capital contribution / redemption "
    "reserve' column is the same underlying reserve renamed across the Bank's own accounts over time ('Capital "
    "contribution reserve' in FY2014-FY2015 and again in the FY2018 18-month accounts; 'Capital redemption "
    "reserve' in FY2016 and FY2019 onward) — carried as one column for continuity; it is fully run down to nil "
    "by FY2019 and stays at nil (explicitly reported as '-') through FY2025, so is omitted from the FY2021-FY2025 "
    "rows below (shown as 0) exactly as the Bank's own more recent accounts no longer print it as a separate line."
)

EQUITY_HEADERS = [
    "Share capital", "Share premium account", "Additional Tier 1 capital",
    "Capital contribution / redemption reserve", "FVOCI reserve", "Retained earnings", "Total",
]

equity_changes_rows = [
    ("TOTAL", "As at 1 January 2014", (3.3, 233.4, None, 2.5, 0.6, 19.6, 259.4)),
    ("DATA", "Profit after taxation (FY2014)", (None, None, None, None, None, 39.7, 39.7)),
    ("DATA", "Other comprehensive income (FY2014)", (None, None, None, None, 0.8, None, 0.8)),
    ("DATA", "Additional Tier 1 perpetual loan issuance", (None, None, 74.3, None, None, None, 74.3)),
    ("DATA", "Share-based payments (FY2014)", (None, None, None, 0.6, None, None, 0.6)),
    ("TOTAL", "As at 31 December 2014", (3.3, 233.4, 74.3, 3.1, 1.4, 59.3, 374.8)),
    ("DATA", "Profit after taxation (FY2015)", (None, None, None, None, None, 80.1, 80.1)),
    ("DATA", "Other comprehensive loss (FY2015)", (None, None, None, None, -2.4, None, -2.4)),
    ("DATA", "Share issue proceeds — Aldermore Group PLC IPO", (None, 68.6, None, None, None, None, 68.6)),
    ("DATA", "Share issue proceeds — exercise of warrants in Aldermore Group PLC", (None, 5.6, None, -2.2, None, 2.2, 5.6)),
    ("DATA", "Coupon paid on Additional Tier 1 perpetual loan, net of tax relief (FY2015)", (None, None, None, None, None, -2.8, -2.8)),
    ("DATA", "Share-based payments, including tax reflected directly in retained earnings (FY2015)", (None, None, None, 3.4, None, None, 3.4)),
    ("DATA", "Transfer of capital contribution to retained earnings re vested share-based payments", (None, None, None, -0.9, None, 0.9, None)),
    ("TOTAL", "As at 31 December 2015", (3.3, 307.6, 74.3, 3.4, -1.0, 139.7, 527.3)),
    ("DATA", "Total comprehensive income (FY2016)", (None, None, None, None, 2.8, 92.3, 95.1)),
    ("DATA", "Share-based payments, including tax reflected directly in retained earnings (FY2016)", (None, None, None, 3.5, None, 0.1, 3.6)),
    ("DATA", "Coupon paid on contingent convertible securities, net of tax (FY2016)", (None, None, None, None, None, -6.6, -6.6)),
    ("TOTAL", "As at 31 December 2016", (3.3, 307.6, 74.3, 6.9, 1.8, 225.5, 619.4)),
    ("TOTAL", "As at 1 January 2017 (opens the 18-month transition period to 30 Jun 2018)", (3.3, 307.6, 74.3, 6.9, 1.8, 225.5, 619.4)),
    ("DATA", "Profit after taxation (18 months to 30 Jun 2018)", (None, None, None, None, None, 155.9, 155.9)),
    ("DATA", "Other comprehensive loss (18 months to 30 Jun 2018)", (None, None, None, None, -0.7, None, -0.7)),
    ("DATA", "Share-based payments, including tax reflected directly in retained earnings (18mo)", (None, None, None, 4.9, None, 1.4, 6.3)),
    ("DATA", "Coupon paid on contingent convertible securities, net of tax (18mo)", (None, None, None, None, None, -13.3, -13.3)),
    ("DATA", "Transfer of share based payment reserve to retained earnings (18mo)", (None, None, None, -11.8, None, 11.8, None)),
    ("DATA", "Release of Employee Benefit Trust loan (18mo)", (None, None, None, None, None, -0.9, -0.9)),
    ("TOTAL", "As at 30 June 2018", (3.3, 307.6, 74.3, 0, 1.1, 380.4, 766.7)),
    ("DATA", "Adjustment for adoption of IFRS 9", (None, None, None, None, None, -7.8, -7.8)),
    ("DATA", "Adjustment for adoption of IFRS 15", (None, None, None, None, None, -0.2, -0.2)),
    ("TOTAL", "Restated balance as at 1 July 2018", (3.3, 307.6, 74.3, 0, 1.1, 372.4, 758.7)),
    ("DATA", "Profit after taxation (FY2019)", (None, None, None, None, None, 102.2, 102.2)),
    ("DATA", "Other comprehensive loss (FY2019)", (None, None, None, None, -0.7, None, -0.7)),
    ("DATA", "Coupon paid on Additional Tier 1 capital securities, net of tax (FY2019)", (None, None, None, None, None, -7.0, -7.0)),
    ("TOTAL", "As at 30 June 2019", (3.3, 307.6, 74.3, 0, 0.4, 467.6, 853.2)),
    ("DATA", "Profit after taxation (FY2020)", (None, None, None, None, None, 64.2, 64.2)),
    ("DATA", "Other comprehensive income (FY2020)", (None, None, None, None, 1.0, None, 1.0)),
    ("DATA", "Issuance of Additional Tier 1 capital (FY2020)", (None, None, 61.0, None, None, None, 61.0)),
    ("DATA", "Redemption of Additional Tier 1 capital (FY2020)", (None, None, -74.3, None, None, None, -74.3)),
    ("DATA", "Coupon paid on Additional Tier 1 capital securities (FY2020)", (None, None, None, None, None, -8.9, -8.9)),
    ("TOTAL", "As at 30 June 2020", (3.3, 307.5, 61.0, 0, 1.4, 522.9, 896.2)),
    ("TOTAL", "As at 1 July 2020", (3.3, 307.6, 61.0, 0, 1.5, 522.9, 896.2)),
    ("DATA", "Profit after taxation (FY2021)", (None, None, None, None, None, 89.3, 89.3)),
    ("DATA", "Other comprehensive income (FY2021)", (None, None, None, None, 6.8, None, 6.9)),
    ("DATA", "Coupon paid on Additional Tier 1 capital securities (FY2021)", (None, None, None, None, None, -5.2, -5.2)),
    ("TOTAL", "As at 30 June 2021", (3.3, 307.6, 61.0, 0, 8.3, 607.0, 987.2)),
    ("DATA", "Profit after taxation (FY2022)", (None, None, None, None, None, 118.0, 118.0)),
    ("DATA", "Other comprehensive loss (FY2022)", (None, None, None, None, -1.4, None, -1.4)),
    ("DATA", "Coupon paid on Additional Tier 1 capital securities (FY2022)", (None, None, None, None, None, -5.2, -5.2)),
    ("TOTAL", "As at 30 June 2022", (3.3, 307.5, 61.0, 0, 6.9, 719.8, 1098.5)),
    ("DATA", "Profit after taxation (FY2023)", (None, None, None, None, None, 129.2, 129.2)),
    ("DATA", "Other comprehensive loss (FY2023)", (None, None, None, None, -3.6, None, -3.6)),
    ("DATA", "Coupon paid on Additional Tier 1 capital securities (FY2023)", (None, None, None, None, None, -5.2, -5.2)),
    ("TOTAL", "As at 30 June 2023", (3.3, 307.5, 61.0, 0, 3.3, 843.9, 1219.0)),
    ("DATA", "Profit after taxation (FY2024)", (None, None, None, None, None, 162.1, 162.1)),
    ("DATA", "Other comprehensive loss (FY2024)", (None, None, None, None, -4.0, None, -4.0)),
    ("DATA", "Coupon paid on Additional Tier 1 capital securities (FY2024)", (None, None, None, None, None, -5.3, -5.3)),
    ("TOTAL", "As at 30 June 2024", (3.3, 307.5, 61.0, 0, -0.7, 1000.7, 1371.8)),
    ("DATA", "Profit after taxation (FY2025)", (None, None, None, None, None, 163.2, 163.2)),
    ("DATA", "Other comprehensive loss (FY2025)", (None, None, None, None, -4.3, None, -4.3)),
    ("DATA", "Redemption of Additional Tier 1 capital", (None, None, -61.0, None, None, None, -61.0)),
    ("DATA", "Issuance of Additional Tier 1 capital", (None, None, 50.0, None, None, None, 50.0)),
    ("DATA", "Coupon paid on Additional Tier 1 capital securities (FY2025)", (None, None, None, None, None, -5.1, -5.1)),
    ("TOTAL", "As at 30 June 2025", (3.3, 307.5, 50.0, 0, -5.0, 1158.8, 1514.6)),
]

bw.add_equity_changes_sheet(
    title="Aldermore Bank PLC — Statement of Changes in Equity",
    subtitle="Company (Bank solo) basis, £m, chronological FY2014-FY2025 (FY2017 has no standalone period — see source notes)",
    headers=EQUITY_HEADERS,
    rows=equity_changes_rows,
    sources_text=EQUITY_CHANGES_SOURCES,
    first_col_width=54,
    source_height=150,
)

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Reconciliation of profit before tax to net cash flows from operating activities", {}),
    ("DATA", "Profit before taxation", {"FY2025": 220.7, "FY2024": 218.2, "FY2023": 171.2, "FY2022": 160.7, "FY2021": 115.7, "FY2020": 81.6, "FY2019": 137.7, "FY2018": 212.8, "FY2016": 127.3, "FY2015": 95.8, "FY2014": 51.8}),
    ("DATA", "Adjustments for non-cash items and other adjustments included within the income statement", {"FY2025": -223.6, "FY2024": -188.9, "FY2023": -49.2, "FY2022": -22.3, "FY2021": 17.0, "FY2020": 58.1, "FY2019": 14.7, "FY2018": 26.4, "FY2016": 7.4, "FY2015": 4.3, "FY2014": -12.7}),
    ("DATA", "Change/(increase) in operating assets", {"FY2025": -1145.9, "FY2024": -439.9, "FY2023": -519.2, "FY2022": -389.0, "FY2021": 265.0, "FY2020": -584.8, "FY2019": -1327.7, "FY2018": -1528.8, "FY2016": -1327.1, "FY2015": -1310.3, "FY2014": -1499.8}),
    ("DATA", "Change/increase in operating liabilities", {"FY2025": 283.3, "FY2024": 992.8, "FY2023": 1539.6, "FY2022": 1526.0, "FY2021": 498.4, "FY2020": 2515.5, "FY2019": 1490.7, "FY2018": 1967.0, "FY2016": 1223.9, "FY2015": 1279.7, "FY2014": 1264.7}),
    ("DATA", "Interest received on intercompany loan (operating basis, FY2024-FY2025)", {"FY2025": 164.5, "FY2024": 135.8}),
    ("DATA", "Interest paid on intercompany loan (operating basis, FY2024-FY2025)", {"FY2025": -53.9, "FY2024": -38.0}),
    ("DATA", "Interest paid on subordinated notes (operating basis, FY2024-FY2025)", {"FY2025": -7.9, "FY2024": -6.4}),
    ("DATA", "Interest received on debt securities (operating basis, FY2024-FY2025)", {"FY2025": 95.2, "FY2024": 86.3}),
    ("DATA", "Proceeds from disposal of non-current assets held for sale (operating basis, FY2024-FY2025)", {"FY2025": 0, "FY2024": 32.8}),
    ("DATA", "Income tax paid", {"FY2025": -57.4, "FY2024": -62.6, "FY2023": -33.9, "FY2022": -59.7, "FY2021": -12.0, "FY2020": -39.7, "FY2019": -18.7, "FY2018": -44.8, "FY2016": -31.5, "FY2015": -20.2, "FY2014": -9.7}),
    ("TOTAL", "Net cash flows (used in)/generated from operating activities", {"FY2025": -725.0, "FY2024": 730.1, "FY2023": 1108.5, "FY2022": 1215.7, "FY2021": 884.1, "FY2020": 2030.7, "FY2019": 296.7, "FY2018": 632.6, "FY2016": 0, "FY2015": 49.3, "FY2014": -205.7}),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Purchase of debt securities", {"FY2025": -1618.2, "FY2024": -1184.9, "FY2023": -358.2, "FY2022": -723.4, "FY2021": -444.6, "FY2020": -1085.2, "FY2019": -810.7, "FY2018": -703.7, "FY2016": -298.4, "FY2015": -414.0, "FY2014": -564.6}),
    ("DATA", "Proceeds from sale and/or maturity of debt securities", {"FY2025": 1278.3, "FY2024": 421.2, "FY2023": 299.3, "FY2022": 159.6, "FY2021": 333.1, "FY2020": 281.4, "FY2019": 386.5, "FY2018": 316.0, "FY2016": 161.7, "FY2015": 279.0, "FY2014": 346.2}),
    ("DATA", "Capital repayments of debt securities", {"FY2025": 81.4, "FY2024": 367.2, "FY2023": 351.3, "FY2022": 223.3, "FY2021": 61.4, "FY2020": 89.7, "FY2019": 53.8, "FY2018": 250.8, "FY2016": 87.5, "FY2015": 32.9, "FY2014": 48.2}),
    ("DATA", "Interest received on debt securities (investing basis, FY2021-FY2023)", {"FY2023": 15.2, "FY2022": 7.6, "FY2021": 6.8}),
    ("DATA", "Interest received on debt securities (investing basis, FY2014-FY2020)", {"FY2020": 8.5, "FY2019": 15.0, "FY2018": 15.5, "FY2016": 13.1, "FY2015": 10.5, "FY2014": 11.2}),
    ("DATA", "Purchase of property, plant and equipment and intangible assets", {"FY2025": -1.0, "FY2024": -5.1, "FY2023": -1.0, "FY2022": -1.9, "FY2021": -11.7, "FY2020": -6.0, "FY2019": -2.3, "FY2018": -11.6, "FY2016": -11.2, "FY2015": -7.3, "FY2014": -5.4}),
    ("TOTAL", "Net cash flows (used in)/generated from investing activities", {"FY2025": -259.5, "FY2024": -401.6, "FY2023": 306.5, "FY2022": -334.8, "FY2021": -55.0, "FY2020": -711.6, "FY2019": -357.7, "FY2018": -133.0, "FY2016": -47.3, "FY2015": -98.9, "FY2014": -164.4}),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Repayment of subordinated debt", {"FY2024": -100.0, "FY2022": -60.0, "FY2018": -40.0}),
    ("DATA", "Proceeds from issue of subordinated debt", {"FY2024": 100.0, "FY2019": 100.0, "FY2016": 60.0}),
    ("DATA", "Issue costs of subordinated debt", {"FY2016": -0.6}),
    ("DATA", "Redemption of Additional Tier 1 Capital", {"FY2025": -61.0, "FY2020": -74.3}),
    ("DATA", "Issuance of Additional Tier 1 Capital", {"FY2025": 50.0, "FY2020": 61.0}),
    ("DATA", "Proceeds from Additional Tier 1 perpetual loan", {"FY2014": 74.3}),
    ("DATA", "Capital repayments on debt securities issued", {"FY2023": 0.4}),
    ("DATA", "Proceeds from issue of shares — Aldermore Group PLC initial public offering", {"FY2015": 68.6}),
    ("DATA", "Proceeds from shares issued — exercise of warrants in Aldermore Group PLC", {"FY2015": 5.6}),
    ("DATA", "Amounts paid on new intercompany loan", {"FY2023": -394.3, "FY2022": -694.4, "FY2021": -686.2, "FY2020": -1222.3, "FY2019": -369.2, "FY2018": -20.4}),
    ("DATA", "Interest received on intercompany loan (financing basis, FY2021-FY2023)", {"FY2023": 68.0, "FY2022": 30.3, "FY2021": 20.1}),
    ("DATA", "Interest received on intercompany loan (financing basis, FY2019-FY2020)", {"FY2020": 13.6, "FY2019": 0.1}),
    ("DATA", "Interest paid on intercompany deposit (FY2019-FY2020)", {"FY2020": -0.2, "FY2019": -0.1}),
    ("DATA", "Deposit placed by related Group companies", {"FY2021": -12.3, "FY2020": -37.4, "FY2019": 311.3}),
    ("DATA", "Coupons paid on Additional Tier 1 capital", {"FY2025": -5.1, "FY2024": -5.3, "FY2023": -5.2, "FY2022": -5.2, "FY2021": -5.2, "FY2020": -8.9, "FY2019": -8.9, "FY2018": -17.8, "FY2016": -8.9, "FY2015": -3.5}),
    ("DATA", "Interest paid on subordinated notes (financing basis)", {"FY2022": -7.4, "FY2021": -9.9, "FY2020": -9.9, "FY2019": -7.5, "FY2018": -10.2, "FY2016": -5.2, "FY2015": -5.2, "FY2014": -5.2}),
    ("DATA", "Repayment of lease liabilities - principal", {"FY2025": -2.3, "FY2024": -3.0, "FY2022": -2.8, "FY2021": -4.0, "FY2020": -1.9}),
    ("DATA", "Interest paid on lease liabilities", {"FY2023": -0.1, "FY2022": -0.1, "FY2021": -0.2, "FY2020": -0.2}),
    ("TOTAL", "Net cash generated/(used in) financing activities", {"FY2025": -18.4, "FY2024": -8.3, "FY2023": -331.2, "FY2022": -739.7, "FY2021": -697.7, "FY2020": -1280.5, "FY2019": 25.7, "FY2018": -88.4, "FY2016": 45.3, "FY2015": 65.5, "FY2014": 69.1}),
    ("TOTAL", "Net (decrease)/increase in cash and cash equivalents", {"FY2025": -1002.9, "FY2024": 320.2, "FY2023": 1083.8, "FY2022": 141.2, "FY2021": 131.4, "FY2020": 38.6, "FY2019": -35.3, "FY2018": 411.2, "FY2016": -2.0, "FY2015": 15.9, "FY2014": -301.0}),
    ("DATA", "Cash and cash equivalents at start of the period", {"FY2025": 2219.6, "FY2024": 1899.4, "FY2023": 815.1, "FY2022": 674.0, "FY2021": 542.6, "FY2020": 504.0, "FY2019": 539.3, "FY2018": 128.1, "FY2016": 130.1, "FY2015": 114.2, "FY2014": 415.2}),
    ("TOTAL", "Cash and cash equivalents at end of the period", {"FY2025": 1216.7, "FY2024": 2219.6, "FY2023": 1899.4, "FY2022": 815.2, "FY2021": 674.0, "FY2020": 542.6, "FY2019": 504.0, "FY2018": 539.3, "FY2016": 128.1, "FY2015": 130.1, "FY2014": 114.2}),
]

bw.add_cash_flow_sheet(
    title="Aldermore Bank PLC — Statement of Cash Flows",
    subtitle="Company (Bank solo) basis, £m, year ended 30 June",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=72,
    source_height=140,
    unit_suffix=" (£m)",
)

# ---------------------------------------------------------------
# Sheet: Asset Quality / Credit Risk Disclosures
# ---------------------------------------------------------------
ASSET_QUALITY_PRESENTATION_NOTE = (
    "PRESENTATION NOTE: figures are from each year's own full statutory accounts' 'Analysis of gross loans "
    "and advances' and 'Analysis of loss allowances' notes (IFRS 9 stage roll-forward tables), Bank solo "
    "basis. 'By product' figures (Business Finance / Property Finance) use the Bank's internal risk-category "
    "disclosure (excludes Property Development, which is separately disclosed only for irrevocable "
    "commitments, not drawn balances) and are only available at this granularity for FY2025/FY2024 in the "
    "documents reviewed; FY2023/FY2022/FY2021 are left blank for the by-product split rather than estimated. "
    "Stage totals (gross and ECL allowance) are available and tie out for all 5 years. FY2024's stage-total "
    "gross loans (11,549.3) differs by £0.1m from the FY2024 Balance Sheet's own 'Loans and advances to "
    "customers' figure (11,416.3 net + 133.0 allowance = 11,549.3) — consistent; both are transcribed as "
    "disclosed.\n\n"
    "HD-047 extension (FY2014-FY2020): IFRS 9 (the source of the Stage 1/2/3 framework above) only took "
    "effect for the Bank from 1 July 2018, so FY2014-FY2016 report credit quality on the older IAS 39 "
    "'individually impaired vs collectively assessed' basis instead — a separate section below carries that "
    "basis for the two years (FY2015, FY2014) where the full impairment-coverage note was reviewed; it is not "
    "mechanically comparable to the IFRS 9 Stage 1/2/3 rows above (different recognition trigger and no forward-"
    "looking ECL overlay). FY2016's own 'by-product' and impairment-coverage note detail, and FY2018/FY2019/"
    "FY2020's IFRS 9 stage-level note detail, were not extracted in this session (the Companies House filings "
    "for these years are scanned images with no text layer, so locating and transcribing note-level tables "
    "requires page-by-page visual review beyond this session's budget) — those three years are therefore left "
    "blank on this sheet. Balance Sheet gross exposure (via 'Loans and advances to customers', net of "
    "allowance) is unaffected and is populated for FY2016/FY2018/FY2019/FY2020 on the Balance Sheet sheet."
)

ASSET_QUALITY_SOURCES = (
    "Sources — Aldermore Bank PLC (company solo) 'Analysis of gross loans and advances' and 'Analysis of "
    "loss allowances' notes, £m:\n"
    f"FY2025 & FY2024 (by product, Business/Property Finance split): Full accounts made up to 30 June 2025, "
    f"filed 04 Nov 2025, p.24-26 (Credit quality and performance of loans) — {CH_2025_URL}\n"
    f"FY2025 & FY2024 (by IFRS 9 stage, gross and allowance): Full accounts made up to 30 June 2025, filed "
    f"04 Nov 2025, p.84-86 (Note 14, Analysis of gross loans and advances / Analysis of loss allowances) — {CH_2025_URL}\n"
    f"FY2023 & FY2022 (by IFRS 9 stage, gross and allowance): Full accounts made up to 30 June 2023, filed "
    f"27 Oct 2023, p.84 (Note 13, Analysis of gross loans and advances / Analysis of loss allowances) — {CH_2023_URL}\n"
    f"FY2021 (by IFRS 9 stage, gross and allowance): Full accounts made up to 30 June 2021, filed 04 Nov "
    f"2021, p.90-91 (Note 18, Analysis of gross loans and advances / Analysis of loss allowances) — {CH_2021_URL}\n"
    f"FY2015 & FY2014 (by product; impaired loans and coverage, IAS 39 basis): Full accounts for the year "
    f"ended 31 December 2015, filed 23 May 2016, p.55-58 (Risk Management — Impaired loan analysis, "
    f"Impairment coverage ratio, Credit concentration by product) — {CH_2015_URL}\n\n"
    + ASSET_QUALITY_PRESENTATION_NOTE
)

asset_quality_rows = [
    ("SECTION", "Gross loans and advances to customers, by product (excl. Property Development commitments)", {}),
    ("DATA", "Business Finance", {"FY2025": 3903.8, "FY2024": 3716.7}),
    ("DATA", "Property Finance", {"FY2025": 8728.4, "FY2024": 7832.5}),
    ("TOTAL", "Total gross loans and advances (by product)", {"FY2025": 12632.2, "FY2024": 11549.2}),
    ("SECTION", "Gross loans and advances to customers, by IFRS 9 stage", {}),
    ("DATA", "Stage 1 (performing)", {"FY2025": 11395.2, "FY2024": 10466.4, "FY2023": 10211.2, "FY2022": 9591.1, "FY2021": 9209.1}),
    ("DATA", "Stage 2 (underperforming)", {"FY2025": 814.8, "FY2024": 716.4, "FY2023": 664.9, "FY2022": 1026.0, "FY2021": 956.6}),
    ("DATA", "Stage 3 (credit-impaired)", {"FY2025": 422.2, "FY2024": 366.4, "FY2023": 287.3, "FY2022": 277.1, "FY2021": 343.9}),
    ("TOTAL", "Total gross loans and advances (by stage)", {"FY2025": 12632.2, "FY2024": 11549.3, "FY2023": 11163.4, "FY2022": 10894.2, "FY2021": 10509.6}),
    ("SECTION", "Allowance for impairment losses, by IFRS 9 stage", {}),
    ("DATA", "Stage 1 (performing)", {"FY2025": -34.2, "FY2024": -50.2, "FY2023": -91.4, "FY2022": -48.3, "FY2021": -32.8}),
    ("DATA", "Stage 2 (underperforming)", {"FY2025": -22.6, "FY2024": -25.6, "FY2023": -25.2, "FY2022": -19.8, "FY2021": -24.1}),
    ("DATA", "Stage 3 (credit-impaired)", {"FY2025": -52.0, "FY2024": -57.2, "FY2023": -48.0, "FY2022": -48.7, "FY2021": -59.1}),
    ("TOTAL", "Total allowance for impairment losses", {"FY2025": -108.8, "FY2024": -133.0, "FY2023": -164.6, "FY2022": -116.8, "FY2021": -116.0}),
    ("SECTION", "Asset quality ratios", {}),
    ("DATA", "ECL coverage ratio (Total allowance / Total gross loans)", {"FY2025": "0.86%", "FY2024": "1.15%", "FY2023": "1.47%", "FY2022": "1.07%", "FY2021": "1.10%"}),
    ("DATA", "Stage 3 (NPL) ratio (Stage 3 gross loans / Total gross loans)", {"FY2025": "3.34%", "FY2024": "3.17%", "FY2023": "2.57%", "FY2022": "2.54%", "FY2021": "3.27%"}),
    ("DATA", "Stage 3 coverage ratio (Stage 3 allowance / Stage 3 gross loans)", {"FY2025": "12.32%", "FY2024": "15.61%", "FY2023": "16.71%", "FY2022": "17.58%", "FY2021": "17.18%"}),
    ("SECTION", "Gross loans and advances to customers, by product (IAS 39 basis, pre-IFRS 9)", {}),
    ("DATA", "Asset Finance", {"FY2015": 1346.7, "FY2014": 1044.3}),
    ("DATA", "Invoice Finance", {"FY2015": 160.8, "FY2014": 180.6}),
    ("DATA", "SME Commercial Mortgages", {"FY2015": 829.2, "FY2014": 552.4}),
    ("DATA", "Buy-to-Let", {"FY2015": 2417.9, "FY2014": 2044.1}),
    ("DATA", "Residential Mortgages", {"FY2015": 1390.2, "FY2014": 979.7}),
    ("TOTAL", "Total gross loans and advances (by product, IAS 39 basis)", {"FY2015": 6144.8, "FY2014": 4801.1}),
    ("SECTION", "Impaired loans and coverage (IAS 39 basis, pre-IFRS 9)", {}),
    ("DATA", "Individually impaired loans (all products)", {"FY2015": 22.8, "FY2014": 20.8}),
    ("DATA", "Allowance for losses — individual provisions", {"FY2015": -10.2, "FY2014": -14.0}),
    ("DATA", "Individually impaired loans as a % of gross loans and advances", {"FY2015": "0.37%", "FY2014": "0.43%"}),
    ("DATA", "Coverage ratio (individual provisions / individually impaired loans)", {"FY2015": "44.74%", "FY2014": "67.40%"}),
]

bw.add_asset_quality_sheet(
    title="Aldermore Bank PLC — Asset Quality / Credit Risk Disclosures",
    subtitle="Company (Bank solo) basis, £m",
    rows=asset_quality_rows,
    sources_text=ASSET_QUALITY_SOURCES,
    first_col_width=68,
    source_height=170,
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, f"Bank solo basis, {unit}" if unit else "Bank solo basis",
                         rows_data, sources_text, note=note, first_col_width=46, source_height=110)

metric(
    "CET1 Capital", "£m",
    [("Common Equity Tier 1 (CET1) capital", {"FY2025": 1337.8, "FY2024": 1321.5, "FY2023": 1203.8, "FY2022": 1065.9, "FY2021": 947.0, "FY2019": 781.6, "FY2018": 682.2, "FY2015": 433.2, "FY2014": 280.7})],
    p3_sources(),
    note="FY2016 and FY2020: no CET1 capital £m figure survives outside a full Pillar 3 document (only the CET1 "
         "ratio % does, from each year's own Annual Report highlights) — see the CET1 Ratio sheet.",
)

metric(
    "CET1 Ratio", "% of RWA",
    [("Common Equity Tier 1 ratio", {"FY2025": "18.4%", "FY2024": "19.2%", "FY2023": "18.5%", "FY2022": "17.0%", "FY2021": "15.9%", "FY2020": "13.4%", "FY2019": "12.6%", "FY2018": "12.5%", "FY2016": "11.4%", "FY2015": "11.7%", "FY2014": "10.3%"})],
    p3_sources(),
    note="FY2020 and FY2016 CET1 ratios are sourced from the Bank's own Annual Report 'Financial highlights' "
         "page (no standalone Pillar 3 document survives for those two years — see p3_sources note above), not "
         "from a Pillar 3 Key metrics table as for every other year on this sheet.",
)

metric(
    "Tier 1 Capital", "£m",
    [("Tier 1 capital", {"FY2025": 1387.8, "FY2024": 1382.5, "FY2023": 1264.8, "FY2022": 1126.6, "FY2021": 1008.0, "FY2019": 855.9, "FY2018": 756.5, "FY2015": 507.5, "FY2014": 355.0})],
    p3_sources(),
)

metric(
    "Tier 1 Ratio", "% of RWA",
    [("Tier 1 ratio", {"FY2025": "19.1%", "FY2024": "20.1%", "FY2023": "19.4%", "FY2022": "18.0%", "FY2021": "16.9%", "FY2019": "13.9%", "FY2018": "13.9%", "FY2015": "13.8%", "FY2014": "13.1%"})],
    p3_sources(),
)

metric(
    "Total Capital", "£m",
    [("Total capital", {"FY2025": 1487.8, "FY2024": 1482.5, "FY2023": 1364.8, "FY2022": 1226.6, "FY2021": 1168.0, "FY2019": 1015.9, "FY2018": 833.9, "FY2015": 556.1, "FY2014": 400.3})],
    p3_sources(),
)

metric(
    "Total Capital Ratio", "% of RWA",
    [("Total capital ratio", {"FY2025": "20.5%", "FY2024": "21.6%", "FY2023": "21.0%", "FY2022": "19.6%", "FY2021": "19.6%", "FY2019": "16.4%", "FY2018": "15.3%", "FY2015": "15.1%", "FY2014": "14.7%"})],
    p3_sources(),
)

metric(
    "Total RWAs", "£m",
    [("Total risk-weighted assets (RWA)", {"FY2025": 7271.6, "FY2024": 6875.6, "FY2023": 6504.9, "FY2022": 6260.1, "FY2021": 5964.1, "FY2019": 6179.0, "FY2018": 5451.0, "FY2015": 3687.5, "FY2014": 2719.5})],
    p3_sources(),
)

# ---------------------------------------------------------------
# Sheet: RWA Breakdown (Pillar 3's UK OV1 template - placed next to
# Total RWAs, since it's itself a Pillar 3 disclosure)
# ---------------------------------------------------------------
RWA_BREAKDOWN_PRESENTATION_NOTE = (
    "PRESENTATION NOTE: transcribed from each year's own Pillar 3 disclosures' 'Overview of RWA' table, Bank "
    "solo (not Group) column, where a full Pillar 3 document is available. FY2019/FY2018 and FY2015/FY2014 use "
    "the simpler 'Total minimum Pillar 1 capital requirement' table instead (credit risk / market risk / "
    "operational risk / CVA only — no separate counterparty-credit-risk or securitisation RWA line existed in "
    "that disclosure format), so those two rows are blank for those years rather than estimated. FY2016 and "
    "FY2020 have no RWA breakdown at all (no standalone Pillar 3 document survives — see the Total RWAs sheet's "
    "note). This sheet's Total row ties out exactly to the Total RWAs sheet for every year with data."
)

RWA_BREAKDOWN_SOURCES = (
    "Sources — Aldermore Bank PLC solo figures from the 'Overview of RWA' / 'Total minimum Pillar 1 capital "
    "requirement' table, Aldermore Group PLC Pillar 3 Disclosures:\n"
    f"FY2025 & FY2024: Pillar 3 Disclosures for the year ended 30 June 2025, p.9 (Overview Of RWA, Bank "
    f"column) — {P3_2025_URL}\n"
    f"FY2023: Pillar 3 Disclosures for the year ended 30 June 2024, p.8 (Overview Of RWA, Bank column, "
    f"FY2023 comparative) — {P3_2024_URL}\n"
    f"FY2022 & FY2021: Pillar 3 Disclosures for the year ended 30 June 2022, p.7 (Overview of RWA, Bank "
    f"column) — {P3_2022_URL}\n"
    f"FY2019 & FY2018: Pillar 3 Disclosures for the year ended 30 June 2019, p.57 (Appendix 1, Table 34 — "
    f"Total minimum Pillar 1 capital requirement, Bank only) — {P3_2019_URL}\n"
    f"FY2015 & FY2014: Pillar 3 Disclosures 31 December 2015, p.58 (Appendix 1, Table 31 — Total minimum "
    f"Pillar 1 capital requirement, Bank only) — {P3_2015_URL}\n\n" + RWA_BREAKDOWN_PRESENTATION_NOTE
)

rwa_breakdown_rows = [
    ("DATA", "Credit risk (excluding CCR)", {"FY2025": 6410.7, "FY2024": 6071.2, "FY2023": 5802.1, "FY2022": 5624.9, "FY2021": 5338.2, "FY2019": 5643.3, "FY2018": 4950.6, "FY2015": 3480.6, "FY2014": 2592.5}),
    ("DATA", "Counterparty credit risk (CCR)", {"FY2025": 4.8, "FY2024": 20.9, "FY2023": 37.1, "FY2022": 0.9, "FY2021": 0.9}),
    ("DATA", "Securitisation exposures in the non-trading book", {"FY2025": 25.5, "FY2024": 40.0, "FY2023": 22.5, "FY2022": 29.2, "FY2021": 23.1}),
    ("DATA", "Position, foreign exchange and commodities risks (market risk)", {"FY2025": 0, "FY2024": 0.1, "FY2023": 1.8, "FY2022": 0.4, "FY2021": 0.1, "FY2019": 0.3, "FY2018": 0.4, "FY2015": 0.1, "FY2014": 0.3}),
    ("DATA", "Credit valuation adjustment (CVA)", {"FY2019": 2.1, "FY2018": 1.0, "FY2015": 1.3, "FY2014": 1.6}),
    ("DATA", "Operational risk", {"FY2025": 830.6, "FY2024": 743.4, "FY2023": 641.4, "FY2022": 604.7, "FY2021": 601.8, "FY2019": 533.3, "FY2018": 499.0, "FY2015": 205.5, "FY2014": 125.1}),
    ("TOTAL", "Total risk-weighted assets (RWA)", {"FY2025": 7271.6, "FY2024": 6875.6, "FY2023": 6504.9, "FY2022": 6260.1, "FY2021": 5964.1, "FY2019": 6179.0, "FY2018": 5451.0, "FY2015": 3687.5, "FY2014": 2719.5}),
]

bw.add_rwa_breakdown_sheet(
    title="Aldermore Bank PLC — RWA Breakdown (Overview of Risk Weighted Assets)",
    subtitle="Bank solo basis, £m",
    rows=rwa_breakdown_rows,
    sources_text=RWA_BREAKDOWN_SOURCES,
    first_col_width=58,
    source_height=140,
)

metric(
    "Leverage Ratio", "£m / %",
    [
        ("Total exposure measure excluding claims on central banks (£m)", {"FY2025": 15674.3, "FY2024": 14337.2, "FY2023": 13609.6, "FY2022": 13850.3, "FY2021": "n/a", "FY2019": 12671.6, "FY2018": 10585.1, "FY2015": 7095.9, "FY2014": 5630.4}),
        ("Leverage ratio excluding claims on central banks (%)", {"FY2025": "8.9%", "FY2024": "9.6%", "FY2023": "9.3%", "FY2022": "8.1%", "FY2021": "n/a", "FY2019": "6.8%", "FY2018": "7.1%", "FY2015": "7.2%", "FY2014": "6.3%"}),
    ],
    p3_sources(),
    note="FY2021 leverage ratio disclosure basis was introduced from 1 January 2022; the FY2022 Pillar 3 report explicitly "
         "marks FY2021 as 'n/a' with no comparative provided under the new template. FY2019/FY2018 and FY2015/FY2014 "
         "figures are each year's own pre-2022 leverage ratio disclosure basis (both are the CRR Part Eight / EBA "
         "Implementing Technical Standard leverage ratio, but the 'excluding claims on central banks' variant used from "
         "FY2022 onward did not exist as a separate disclosure before then, so these earlier figures are the Bank's "
         "then-current all-exposures leverage ratio, not a like-for-like restatement) — FY2016 and FY2020 have no "
         "leverage ratio figure at all (no standalone Pillar 3 document survives for either year).",
)

metric(
    "LCR", "£m / %",
    [
        ("Total high-quality liquid assets (HQLA), weighted value average (£m)", {"FY2025": 3723.1, "FY2024": 4208.6, "FY2023": 3280.6, "FY2022": 2838.5, "FY2021": "n/a", "FY2020": "n/a", "FY2019": "n/a", "FY2018": "n/a", "FY2016": "n/a", "FY2015": "n/a", "FY2014": "n/a"}),
        ("Total net cash outflows, adjusted value (£m)", {"FY2025": 1968.3, "FY2024": 1959.4, "FY2023": 1686.4, "FY2022": 772.6, "FY2021": "n/a", "FY2020": "n/a", "FY2019": "n/a", "FY2018": "n/a", "FY2016": "n/a", "FY2015": "n/a", "FY2014": "n/a"}),
        ("Liquidity Coverage Ratio (%)", {"FY2025": "189.2%", "FY2024": "214.8%", "FY2023": "194.5%", "FY2022": "367.4%", "FY2021": "n/a", "FY2020": "n/a", "FY2019": "n/a", "FY2018": "n/a", "FY2016": "n/a", "FY2015": "n/a", "FY2014": "n/a"}),
    ],
    p3_sources(),
    note="LCR is computed as a 12-month average to the period end. FY2021 and earlier are all 'n/a' — the Bank-solo "
         "LCR disclosure template used on this sheet was introduced from 1 January 2022 (see FY2022 Pillar 3 report); "
         "no comparable Bank-solo LCR figure was located for FY2014-FY2020 in the documents reviewed for this "
         "extension (the Basel LCR standard itself phased in nationally from 2015, but the Bank's own Pillar 3 "
         "reports for those years did not publish a Bank-solo LCR figure in the format used here).",
)

metric(
    "NSFR", "£m / %",
    [
        ("Total available stable funding (£m)", {"FY2025": 15972.4, "FY2024": 16133.4, "FY2023": 15490.2, "FY2022": 15667.6, "FY2021": "n/a", "FY2020": "n/a", "FY2019": "n/a", "FY2018": "n/a", "FY2016": "n/a", "FY2015": "n/a", "FY2014": "n/a"}),
        ("Total required stable funding (£m)", {"FY2025": 12166.9, "FY2024": 11778.0, "FY2023": 12161.3, "FY2022": 12169.6, "FY2021": "n/a", "FY2020": "n/a", "FY2019": "n/a", "FY2018": "n/a", "FY2016": "n/a", "FY2015": "n/a", "FY2014": "n/a"}),
        ("Net Stable Funding Ratio (%)", {"FY2025": "131.3%", "FY2024": "137.0%", "FY2023": "127.4%", "FY2022": "128.7%", "FY2021": "n/a", "FY2020": "n/a", "FY2019": "n/a", "FY2018": "n/a", "FY2016": "n/a", "FY2015": "n/a", "FY2014": "n/a"}),
    ],
    p3_sources(),
    note="NSFR is computed as a 4-quarter average to the period end. FY2021 and earlier are all 'n/a' — the UK NSFR "
         "requirement did not take effect until 1 January 2022 (see FY2022 Pillar 3 report), so no NSFR figure exists "
         "for FY2014-FY2020 at all.",
)

metric(
    "MREL Ratio", None,
    [("MREL ratio", {y: "Not publicly disclosed" for y in YEARS})],
    p3_sources(),
    note="MREL is not disclosed for Aldermore Bank PLC/Aldermore Group PLC in any Pillar 3 report reviewed — the Group "
         "sits below the balance-sheet threshold at which the Bank of England sets a bail-in MREL requirement above "
    "minimum capital requirements, so no separate MREL ratio is published.",
)

# ---------------------------------------------------------------
# Interim Pillar 3 disclosures
# ---------------------------------------------------------------
INTERIM_HEADERS = [
    "Period",
    "Disclosure type",
    "Metric",
    "Value",
    "Unit",
    "Basis",
    "Source document",
    "Page / table",
]

INTERIM_PERIODS = [
    ("31 Dec 2025", "H1 2025 interim (current period)"),
    ("30 Jun 2025", "H1 2025 interim (comparative)"),
    ("31 Dec 2024", "H1 2025 interim (comparative)"),
]

INTERIM_METRICS = [
    ("CET1 capital", [1342.5, 1337.8, 1306.1], "£m"),
    ("Tier 1 capital", [1392.5, 1387.8, 1367.1], "£m"),
    ("Total capital", [1692.5, 1487.8, 1467.1], "£m"),
    ("Total risk-weighted exposure amount", [7352.0, 7271.6, 6997.3], "£m"),
    ("CET1 ratio", ["18.3%", "18.4%", "18.7%"], "%"),
    ("Tier 1 ratio", ["18.9%", "19.1%", "19.5%"], "%"),
    ("Total capital ratio", ["23.0%", "20.5%", "21.0%"], "%"),
    ("Total exposure measure excluding claims on central banks", [15369.1, 15526.0, 14826.8], "£m"),
    ("Leverage ratio excluding claims on central banks", ["9.1%", "8.9%", "9.2%"], "%"),
    ("Total high-quality liquid assets (HQLA), weighted-value average", [3518.6, 3723.1, 4062.3], "£m"),
    ("Total net cash outflows (adjusted value)", [1964.8, 1968.3, 2047.1], "£m"),
    ("Liquidity coverage ratio", ["179.1%", "189.2%", "198.4%"], "%"),
    ("Total available stable funding", [16221.9, 15972.4, 16013.1], "£m"),
    ("Total required stable funding", [12699.7, 12166.9, 11856.4], "£m"),
    ("NSFR ratio", ["127.7%", "131.3%", "135.1%"], "%"),
    ("MREL ratio", ["Not disclosed", "Not disclosed", "Not disclosed"], "%"),
]

interim_rows = []
for period_index, (period, disclosure_type) in enumerate(INTERIM_PERIODS):
    for metric_name, values, unit in INTERIM_METRICS:
        interim_rows.append(
            [
                period,
                disclosure_type,
                metric_name,
                values[period_index],
                unit,
                "Aldermore Bank PLC (Bank solo)",
                "Aldermore Group PLC Interim Pillar 3 Disclosure — 31 December 2025",
                "p.4, Key Metrics (Bank column)",
            ]
        )

interim_hyperlinks = {(i, 6): INTERIM_P3_2025_URL for i in range(len(interim_rows))}
bw.add_wide_interim_sheet(
    "Interim Pillar 3",
    rows=interim_rows,
    hyperlink_cells=interim_hyperlinks,
    title="Aldermore Bank PLC — Interim Pillar 3",
    subtitle="Bank solo basis; amounts in £m and ratios in %, as disclosed in the official interim Key Metrics table",
    note=(
        "Source: Aldermore Group PLC Interim Pillar 3 Disclosure as at 31 December 2025, p.4, Key Metrics — Bank column. "
        f"Official PDF: {INTERIM_P3_2025_URL}\n"
        "The document reports 31 Dec 2025 and comparative 30 Jun 2025 and 31 Dec 2024 figures. No separate official "
        "half-year Pillar 3 document was located in the archive for 2021, 2022, 2023, or 2024; those periods are therefore "
        "not inferred or backfilled. MREL is not included in the Key Metrics table and is recorded as not disclosed."
    ),
)
# Keep the source register immediately after the matrix so the current
# verifier can discover it without changing the shared helper.
interim_ws = bw.wb["Interim Pillar 3"]
interim_ws.delete_rows(5 + len({row[2] for row in interim_rows}), 2)
for row_number in range(5, interim_ws.max_row + 1):
    if interim_ws.cell(row=row_number, column=1).value == "Source register":
        source_register_row = row_number
        break
    for column_number in range(4, interim_ws.max_column + 1):
        cell = interim_ws.cell(row=row_number, column=column_number)
        if cell.value not in (None, ""):
            cell.hyperlink = INTERIM_P3_2025_URL
            cell.style = "Hyperlink"
for row_number in range(source_register_row + 2, interim_ws.max_row + 1):
    if interim_ws.cell(row=row_number, column=1).value in (None, ""):
        break
    source_cell = interim_ws.cell(row=row_number, column=3)
    source_cell.hyperlink = INTERIM_P3_2025_URL
    source_cell.style = "Hyperlink"

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {"FY2025": 20618.2, "FY2024": 20195.5, "FY2023": 19051.7, "FY2022": 17290.8, "FY2021": 15583.0, "FY2020": 15000.7, "FY2019": 12471.9, "FY2018": 10467.4, "FY2016": 8396.5, "FY2015": 7021.4, "FY2014": 5583.2}),
        ("Loans and advances to customers", {"FY2025": 12523.4, "FY2024": 11416.3, "FY2023": 10998.9, "FY2022": 10777.3, "FY2021": 10393.6, "FY2020": 10602.2, "FY2019": 10230.3, "FY2018": 8990.5, "FY2016": 7477.3, "FY2015": 6144.8, "FY2014": 4801.1}),
        ("Customers' accounts", {"FY2025": 17047.6, "FY2024": 16306.7, "FY2023": 15033.3, "FY2022": 14105.4, "FY2021": 12427.3, "FY2020": 10886.4, "FY2019": 8971.8, "FY2018": 7776.3, "FY2016": 6673.7, "FY2015": 5742.0, "FY2014": 4459.0}),
        ("Total equity", {"FY2025": 1514.6, "FY2024": 1371.8, "FY2023": 1219.0, "FY2022": 1098.6, "FY2021": 987.1, "FY2020": 896.2, "FY2019": 853.2, "FY2018": 766.7, "FY2016": 619.4, "FY2015": 527.3, "FY2014": 374.8}),
    ],
    balance_sheet_unit="£m",
    income_statement_totals=[
        ("Total operating income", {"FY2025": 473.4, "FY2024": 462.9, "FY2023": 476.2, "FY2022": 389.8, "FY2021": 323.4, "FY2020": 313.1, "FY2019": 331.8, "FY2018": 468.5, "FY2016": 265.9, "FY2015": 221.6, "FY2014": 166.1}),
        ("Administrative expenses", {"FY2025": -266.8, "FY2024": -263.8, "FY2023": -253.5, "FY2022": -224.0, "FY2021": -173.7, "FY2020": -148.7, "FY2019": -169.4, "FY2018": -227.8, "FY2016": -117.8, "FY2015": -110.1, "FY2014": -100.8}),
        ("Profit after taxation", {"FY2025": 163.2, "FY2024": 162.1, "FY2023": 129.2, "FY2022": 118.0, "FY2021": 89.3, "FY2020": 64.2, "FY2019": 102.2, "FY2018": 155.9, "FY2016": 92.3, "FY2015": 80.1, "FY2014": 39.7}),
    ],
    income_statement_unit="£m",
    equity_changes_totals=[
        ("Opening equity", {"FY2025": 1371.8, "FY2024": 1219.0, "FY2023": 1098.5, "FY2022": 987.1, "FY2021": 896.2, "FY2020": 853.2, "FY2019": 766.7, "FY2018": 619.4, "FY2016": 527.3, "FY2015": 374.8, "FY2014": 259.4}),
        ("Total comprehensive income", {"FY2025": 158.9, "FY2024": 158.1, "FY2023": 125.7, "FY2022": 116.6, "FY2021": 96.1, "FY2020": 65.2, "FY2019": 101.5, "FY2018": 155.2, "FY2016": 95.1, "FY2015": 77.7, "FY2014": 40.5}),
        ("Other equity movements, net", {"FY2025": -16.1, "FY2024": -5.3, "FY2023": -5.2, "FY2022": -5.2, "FY2021": -5.2, "FY2020": -22.2, "FY2019": -15.0, "FY2018": -7.9, "FY2016": -3.0, "FY2015": 74.8, "FY2014": 74.9}),
        ("Closing equity", {"FY2025": 1514.6, "FY2024": 1371.8, "FY2023": 1219.0, "FY2022": 1098.6, "FY2021": 987.1, "FY2020": 896.2, "FY2019": 853.2, "FY2018": 766.7, "FY2016": 619.4, "FY2015": 527.3, "FY2014": 374.8}),
    ],
    equity_changes_unit="£m",
    cash_flow_totals=[
        ("Net cash from operating activities", {"FY2025": -725.0, "FY2024": 730.1, "FY2023": 1108.5, "FY2022": 1215.7, "FY2021": 884.1, "FY2020": 2030.7, "FY2019": 296.7, "FY2018": 632.6, "FY2016": 0, "FY2015": 49.3, "FY2014": -205.7}),
        ("Net cash from investing activities", {"FY2025": -259.5, "FY2024": -401.6, "FY2023": 306.5, "FY2022": -334.8, "FY2021": -55.0, "FY2020": -711.6, "FY2019": -357.7, "FY2018": -133.0, "FY2016": -47.3, "FY2015": -98.9, "FY2014": -164.4}),
        ("Net cash from financing activities", {"FY2025": -18.4, "FY2024": -8.3, "FY2023": -331.2, "FY2022": -739.7, "FY2021": -697.7, "FY2020": -1280.5, "FY2019": 25.7, "FY2018": -88.4, "FY2016": 45.3, "FY2015": 65.5, "FY2014": 69.1}),
        ("Cash and cash equivalents at end of year", {"FY2025": 1216.7, "FY2024": 2219.6, "FY2023": 1899.4, "FY2022": 815.2, "FY2021": 674.0, "FY2020": 542.6, "FY2019": 504.0, "FY2018": 539.3, "FY2016": 128.1, "FY2015": 130.1, "FY2014": 114.2}),
    ],
    cash_flow_unit="£m",
    ratios=[
        ("CET1 Ratio", {"FY2025": "18.4%", "FY2024": "19.2%", "FY2023": "18.5%", "FY2022": "17.0%", "FY2021": "15.9%", "FY2020": "13.4%", "FY2019": "12.6%", "FY2018": "12.5%", "FY2016": "11.4%", "FY2015": "11.7%", "FY2014": "10.3%"}),
        ("Tier 1 Ratio", {"FY2025": "19.1%", "FY2024": "20.1%", "FY2023": "19.4%", "FY2022": "18.0%", "FY2021": "16.9%", "FY2019": "13.9%", "FY2018": "13.9%", "FY2015": "13.8%", "FY2014": "13.1%"}),
        ("Total Capital Ratio", {"FY2025": "20.5%", "FY2024": "21.6%", "FY2023": "21.0%", "FY2022": "19.6%", "FY2021": "19.6%", "FY2019": "16.4%", "FY2018": "15.3%", "FY2015": "15.1%", "FY2014": "14.7%"}),
        ("Leverage Ratio", {"FY2025": "8.9%", "FY2024": "9.6%", "FY2023": "9.3%", "FY2022": "8.1%", "FY2019": "6.8%", "FY2018": "7.1%", "FY2015": "7.2%", "FY2014": "6.3%"}),
        ("LCR", {"FY2025": "189.2%", "FY2024": "214.8%", "FY2023": "194.5%", "FY2022": "367.4%"}),
        ("NSFR", {"FY2025": "131.3%", "FY2024": "137.0%", "FY2023": "127.4%", "FY2022": "128.7%"}),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own source "
         "citation for the underlying document/page. Fiscal year ends 30 June (31 December for FY2014-FY2016; the "
         "Bank's accounting reference date changed following its 2018 acquisition by FirstRand). Balance Sheet, "
         "Profit & Loss, Statement of Changes in Equity and Cash Flow figures are all Bank-solo; Pillar 3 ratios use "
         "the Bank-solo columns of Aldermore Group PLC's Pillar 3 disclosures (the only level at which Pillar 3 is "
         "published), except CET1 Ratio for FY2016/FY2020 which is sourced from the Bank's own Annual Report "
         "highlights (no standalone Pillar 3 document survives for those two years). "
         "'Other equity movements, net' combines Additional Tier 1 capital issuance/redemption, AT1 coupon "
         "payments, and (FY2015/FY2014) the Aldermore Group PLC IPO share issue proceeds and warrant exercise. "
         "Leverage/LCR/NSFR have no FY2021 figure; LCR/NSFR have no figure at all before FY2022 (disclosure "
         "templates introduced from 1 Jan 2022) and Leverage Ratio has none for FY2016/FY2020 — see the Leverage "
         "Ratio/LCR/NSFR sheets for the disclosure-template basis note. FY2017 has no standalone 12-month period "
         "at all (see the Balance Sheet sheet's source note) and FY2018's column is an 18-month, not 12-month, "
         "period — both are omitted or flagged accordingly rather than estimated.",
)

bw.save("/Users/armaan/code/katalysis/banks/ALDERMORE FINANCIALS.xlsx")
