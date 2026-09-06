import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook


# Morgan Stanley Bank International Limited, company 03722571, FRN 195430.
# The legal entity and FRN are confirmed against Banks List 2608.xlsx,
# Companies House, and Morgan Stanley's UK office/FCA information.
YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021",
         "FY2020", "FY2019", "FY2018", "FY2017", "FY2016", "FY2015", "FY2014",
         "FY2013", "FY2012", "FY2011", "FY2010", "FY2009"]

# HD-073 (2026-09-06): extends Balance Sheet, Profit & Loss, Statement of
# Changes in Equity, and Cash Flow Statement back to FY2009 only. Pillar 3
# (all 11 metric sheets), Asset Quality, and RWA Breakdown stay FY2014-onward
# - every call building one of those sheets passes years=PILLAR3_YEARS
# explicitly, since BankWorkbook otherwise defaults to the full (now
# FY2009-extended) self.years for any sheet-builder call with no override.
PILLAR3_YEARS = [y for y in YEARS if y not in ("FY2013", "FY2012", "FY2011", "FY2010", "FY2009")]

# FY2014-FY2020 extension (HD-048, capped at FY2014 per project-wide decision -
# real archive extends to FY2009 per HD-004, not sourced here). Filing links
# re-verified 2026-09 against Companies House filing-history for company
# 03722571 (each is that year's own "Full accounts made up to 31 December
# <year>" filing) - all 7 PDFs downloaded and read directly (scanned-image
# filings, no text layer; transcribed by hand from the rendered pages).
AR_URLS = {
    "FY2025": "https://find-and-update.company-information.service.gov.uk/company/03722571/filing-history/MzUxNTMzMjAyMmFkaXF6a2N4/document?format=pdf&download=0",
    "FY2024": "https://find-and-update.company-information.service.gov.uk/company/03722571/filing-history/MzQ2MjkyNzg4N2FkaXF6a2N4/document?format=pdf&download=0",
    "FY2023": "https://find-and-update.company-information.service.gov.uk/company/03722571/filing-history/MzQyMDQ2MzQxOGFkaXF6a2N4/document?format=pdf&download=0",
    "FY2022": "https://find-and-update.company-information.service.gov.uk/company/03722571/filing-history/MzM3ODM5NTg1NmFkaXF6a2N4/document?format=pdf&download=0",
    "FY2021": "https://find-and-update.company-information.service.gov.uk/company/03722571/filing-history/MzMzODIzODA1MmFkaXF6a2N4/document?format=pdf&download=0",
    "FY2020": "https://find-and-update.company-information.service.gov.uk/company/03722571/filing-history/MzMwMTE4OTc0MWFkaXF6a2N4/document?format=pdf&download=0",
    "FY2019": "https://find-and-update.company-information.service.gov.uk/company/03722571/filing-history/MzI2MzcyNjY2MGFkaXF6a2N4/document?format=pdf&download=0",
    "FY2018": "https://find-and-update.company-information.service.gov.uk/company/03722571/filing-history/MzIzMzQ0NTc3NWFkaXF6a2N4/document?format=pdf&download=0",
    "FY2017": "https://find-and-update.company-information.service.gov.uk/company/03722571/filing-history/MzIwNDA4MDg1M2FkaXF6a2N4/document?format=pdf&download=0",
    "FY2016": "https://find-and-update.company-information.service.gov.uk/company/03722571/filing-history/MzE3NTI3MTY1OWFkaXF6a2N4/document?format=pdf&download=0",
    "FY2015": "https://find-and-update.company-information.service.gov.uk/company/03722571/filing-history/MzE0NzU0MjE4NGFkaXF6a2N4/document?format=pdf&download=0",
    "FY2014": "https://find-and-update.company-information.service.gov.uk/company/03722571/filing-history/MzEyMjM5NTcyOWFkaXF6a2N4/document?format=pdf&download=0",
}

ENTITY_NOTE = (
    "ENTITY NOTE: Morgan Stanley Bank International Limited (company 03722571, FRN 195430) is the legal entity "
    "listed in Banks List 2608.xlsx. Companies House confirms the active UK private limited company, incorporated "
    "23 February 1999, with registered office at 25 Cabot Square, London E14 4QA. The figures below are standalone "
    "Company figures from the entity's own annual reports, not Morgan Stanley International group figures."
)

HD073_AR2013_URL = "https://find-and-update.company-information.service.gov.uk/company/03722571/filing-history/MzA5OTE2NDI1N2FkaXF6a2N4/document?format=pdf&download=0"
HD073_AR2011_URL = "https://find-and-update.company-information.service.gov.uk/company/03722571/filing-history/MzA1NzUxOTkzNGFkaXF6a2N4/document?format=pdf&download=0"
HD073_AR2009_URL = "https://find-and-update.company-information.service.gov.uk/company/03722571/filing-history/MzAxNjAzOTk5M2FkaXF6a2N4/document?format=pdf&download=0"

HD073_SOURCING_NOTE = (
    "HD-073 (2026-09-06) HISTORICAL SOURCING NOTE (FY2009-FY2013): Balance Sheet, Profit & Loss, and Statement of "
    "Changes in Equity only (Pillar 3, Asset Quality, and RWA Breakdown stay FY2014-onward, unchanged). Re-verified "
    "via each year's own Companies House statutory filing (company 03722571), all genuine scanned/no-text-layer "
    "filings transcribed directly from the rendered pages, same as the existing FY2014-FY2020 sourcing: "
    f"FY2013/FY2012 from the FY2013 Annual Report (pp.15-18) — {HD073_AR2013_URL}; FY2011/FY2010 from the FY2011 "
    f"Annual Report (pp.13-16) — {HD073_AR2011_URL}; FY2009 from the FY2009 Annual Report (pp.7-9, and Note 25 "
    f"p.28 for the equity reconciliation) — {HD073_AR2009_URL}. The Company takes the FRS 101/predecessor "
    "reduced-disclosure exemption from presenting a cash-flow statement in every one of these years too - "
    "confirmed directly against each year's own Contents page (Profit and loss account / Statement of total "
    "recognised gains and losses / Balance sheet only, no cash flow statement listed), not merely carried forward "
    "from the FY2014-FY2020 finding. No years self-skipped.\n"
    "FY2013/FY2012 continuing/discontinued-operations split: the FY2013 Annual Report itself already splits "
    "continuing vs discontinued operations (the Wealth Management segment was substantially sold during "
    "FY2013/FY2014), consistent with the existing FY2014 note above - the Profit & Loss sheet uses the FY2013 "
    "report's own Total columns (continuing + discontinued combined) for both FY2013 and its FY2012 comparative.\n"
    "FY2009 Balance Sheet structural note: the FY2009 Annual Report's own equity section discloses a distinct "
    "'Pension reserve' component (£252k at 31 December 2009) not present as a separate line in any later year's "
    "Balance Sheet (folded into the Profit and loss account line from FY2010 onward per that year's own report) - "
    "shown here as its own row rather than silently merged, and the FY2009 closing Total equity of £841,906k ties "
    "exactly to both components disclosed. FY2009 also does not separately disclose 'Reverse repurchase "
    "agreements' as an asset-side line or 'Repurchase agreements' as a liability-side line (both fold into the "
    "broader loans-and-advances/other-liabilities figures that year); these lines first appear as their own rows "
    "from FY2010 onward - a genuine presentational difference confirmed directly against the FY2009 report's own "
    "Balance Sheet, not an omission."
)


def annual_sources():
    return (
        ENTITY_NOTE + "\n\n"
        "Sources — Morgan Stanley Bank International Limited Annual Reports and Financial Statements, "
        "Strategic Report capital/liquidity tables and financial statements:\n"
        f"FY2025: Annual Report and Financial Statements for year ended 31 December 2025, pp.5, 8-10, 47 — {AR_URLS['FY2025']}\n"
        f"FY2024: Annual Report and Financial Statements for year ended 31 December 2024, pp.5, 8-10 — {AR_URLS['FY2024']}\n"
        f"FY2023: Annual Report and Financial Statements for year ended 31 December 2023, pp.5, 8-10 — {AR_URLS['FY2023']}\n"
        f"FY2022: Annual Report and Financial Statements for year ended 31 December 2022, pp.5, 8-10 — {AR_URLS['FY2022']}\n"
        f"FY2021: Annual Report and Financial Statements for year ended 31 December 2021, pp.6, 9-10 — {AR_URLS['FY2021']}\n"
        f"FY2020: Annual Report and Financial Statements for year ended 31 December 2020, pp.5, 12-13 (Key performance "
        f"indicators / Own Funds / Leverage ratio) — {AR_URLS['FY2020']}\n"
        f"FY2019: Annual Report and Financial Statements for year ended 31 December 2020's own FY2019 comparative "
        f"columns, pp.5, 12-13 — {AR_URLS['FY2020']}\n"
        f"FY2018: Annual Report and Financial Statements for year ended 31 December 2018, p.3 (Key performance "
        f"indicators - Tier 1 capital, Tier 1 ratio, leverage ratio only; no CET1/Total Capital/RWA/LCR/NSFR "
        f"disclosed) — {AR_URLS['FY2018']}\n"
        f"FY2017: Annual Report and Financial Statements for year ended 31 December 2017, p.3 (same limited KPI "
        f"disclosure as FY2018) — {AR_URLS['FY2017']}\n"
        f"FY2016: Annual Report and Financial Statements for year ended 31 December 2016, p.3 (same limited KPI "
        f"disclosure) — {AR_URLS['FY2016']}\n"
        f"FY2015: Annual Report and Financial Statements for year ended 31 December 2016's own FY2015 comparative "
        f"column, p.3 (Tier 1 capital/ratio and leverage ratio; the Company's own FY2015 Annual Report carried no "
        f"capital KPI section at all) — {AR_URLS['FY2016']}\n"
        f"FY2014: Annual Report and Financial Statements for year ended 31 December 2014, p.3 — {AR_URLS['FY2014']}. "
        f"No Tier 1 capital, CET1, Total Capital, RWA, leverage or LCR/NSFR figures are disclosed anywhere in the "
        f"FY2014 report itself or in any later year's comparative (the KPI section first appears in the FY2016 "
        f"report, reaching back only to FY2015) — genuinely undisclosed, not merely unsourced by us.\n"
        "The annual reports state that the Company takes the FRS 101 reduced-disclosure exemption from presenting a "
        "cash-flow statement. Blank or non-disclosed entries are not estimates or zeros. FY2014-FY2018 annual "
        "reports disclose materially less capital/liquidity detail than FY2019 onward: only Tier 1 capital, Tier 1 "
        "ratio and leverage ratio are given (no separately-stated CET1, Total Capital, Total RWAs, LCR or NSFR). "
        "Because the Company's Own Funds tables in the FY2019/FY2020 reports confirm CET1 = Tier 1 capital exactly "
        "in every year reviewed (no Additional Tier 1 instruments), CET1 Capital/CET1 Ratio for FY2015-FY2018 are "
        "populated with the same disclosed Tier 1 figures on that structural basis, clearly noted; Total Capital, "
        "Total Capital Ratio, Total RWAs, Leverage Exposure, LCR, NSFR and the RWA Breakdown are left blank for "
        "FY2014-FY2018 (FY2014-FY2020 for RWA Breakdown, and FY2014-FY2018 for LCR/NSFR) as genuinely not "
        "disclosed, rather than estimated."
    )


bw = BankWorkbook("Morgan Stanley Bank International Limited", YEARS, header_color="1F4E79")

STATEMENTS_SOURCES = (
    ENTITY_NOTE + "\n\n"
    "Sources — Morgan Stanley Bank International Limited Annual Reports and Financial Statements "
    "(Income Statement, Statement of Comprehensive Income, Statement of Financial Position, Statement of Changes "
    "in Equity, and Note 28 credit risk disclosures):\n"
    f"FY2025: Annual Report and Financial Statements for year ended 31 December 2025, pp.43-46, 76-77 — {AR_URLS['FY2025']}\n"
    f"FY2024: Annual Report and Financial Statements for year ended 31 December 2024, pp.42-45, 74-75 — {AR_URLS['FY2024']}\n"
    f"FY2023: Annual Report and Financial Statements for year ended 31 December 2023 (via FY2024 report's own "
    f"FY2023 comparative columns, pp.42-45, 74-75) — {AR_URLS['FY2024']}\n"
    f"FY2022: Annual Report and Financial Statements for year ended 31 December 2022, pp.39-43, 71-72 — {AR_URLS['FY2022']}\n"
    f"FY2021: Annual Report and Financial Statements for year ended 31 December 2021 (via FY2022 report's own "
    f"FY2021 comparative columns, pp.39-43, 71-72) — {AR_URLS['FY2022']}\n"
    f"FY2020: Annual Report and Financial Statements for year ended 31 December 2020, pp.53-56, 90-94 (Income "
    f"Statement, Statement of Comprehensive Income, Statement of Changes in Equity, Statement of Financial "
    f"Position, Note 35 credit risk) — {AR_URLS['FY2020']}\n"
    f"FY2019: via the FY2020 report's own FY2019 comparative columns, pp.53-56, 90-94 — {AR_URLS['FY2020']}\n"
    f"FY2018: Annual Report and Financial Statements for year ended 31 December 2018, pp.29-32, 74-76 (Income "
    f"Statement, Statement of Comprehensive Income, Statement of Changes in Equity, Statement of Financial "
    f"Position, Note 32 credit risk) — {AR_URLS['FY2018']}\n"
    f"FY2017: via the FY2018 report's own FY2017 comparative columns (pp.29-32, 76) and the Company's own FY2017 "
    f"Annual Report, pp.27-30, 64 (Note 28 credit risk) — {AR_URLS['FY2018']} / {AR_URLS['FY2017']}\n"
    f"FY2016: via the FY2017 report's own FY2016 comparative columns (pp.27-30, 64) and the Company's own FY2016 "
    f"Annual Report, pp.16-19, 51 (Note 28 credit risk) — {AR_URLS['FY2017']} / {AR_URLS['FY2016']}\n"
    f"FY2015: via the FY2016 report's own FY2015 comparative columns, pp.16-19, 51-52 — {AR_URLS['FY2016']}\n"
    f"FY2014: Annual Report and Financial Statements for year ended 31 December 2014, pp.15-17, 51 (Profit and "
    f"Loss Account, Statement of Total Recognised Gains and Losses, Balance Sheet, Note 29 credit risk) — "
    f"{AR_URLS['FY2014']}. This is the earliest UK GAAP/FRS 101-era filing before this entity switched to the "
    f"Income Statement/Statement of Comprehensive Income/Statement of Changes in Equity naming used from FY2015 "
    f"onward; FY2014 also uniquely presents a continuing/discontinued-operations split (the Company's Investment "
    f"Management and Wealth Management segments were both transferred out or closed during FY2014) - the Profit & "
    f"Loss sheet uses the FY2014 report's own Total columns (continuing + discontinued combined).\n"
    "The Company takes the FRS 101 reduced-disclosure exemption from presenting a cash-flow statement. Blank or "
    "non-disclosed entries are not estimates or zeros. FY2014-FY2017 predate IFRS 9 (adopted 1 January 2018): "
    "those years' credit-risk note uses the incurred-loss 'individually impaired' concept rather than ECL "
    "staging, and the Asset Quality sheet reflects this distinction explicitly rather than forcing a Stage 1/"
    "Stage 3 label onto pre-IFRS 9 disclosures. A genuine, material FY2014 finding: one borrower's entry into "
    "administration in March 2014 drove an £83,173k impairment loss on loans and advances to customers that year "
    "(gross £111,239k, net carrying £28,066k) - materially larger than the de minimis impaired balances "
    "(£1,674k FY2015, £126k FY2016, £131k FY2017) seen in every other year reviewed."
)

# STATUTORY_SOURCES is used ONLY by the four in-scope sheets (Balance Sheet,
# Profit & Loss, Statement of Changes in Equity, Cash Flow Statement) so that
# Asset Quality's own citation text (which reuses STATEMENTS_SOURCES as its
# base, unmodified) stays byte-for-byte unchanged - see HD-073.
STATUTORY_SOURCES = (
    STATEMENTS_SOURCES + "\n\n"
    f"FY2013: Annual Report and Financial Statements for year ended 31 December 2013, pp.15-18 (Profit and Loss "
    f"Account, Statement of Total Recognised Gains and Losses, Balance Sheet) — {HD073_AR2013_URL}\n"
    f"FY2012: via the FY2013 Annual Report's own FY2012 comparative columns, pp.15-18 — {HD073_AR2013_URL}\n"
    f"FY2011: Annual Report and Financial Statements for year ended 31 December 2011, pp.13-15 — {HD073_AR2011_URL}\n"
    f"FY2010: via the FY2011 Annual Report's own FY2010 comparative columns, pp.13-15 — {HD073_AR2011_URL}\n"
    f"FY2009: Annual Report and Financial Statements for year ended 31 December 2009, pp.7-9, Note 25 p.28 "
    f"(reconciliation of shareholders' funds and movements on reserves) — {HD073_AR2009_URL}\n"
    + HD073_SOURCING_NOTE
)

# ---------------------------------------------------------------
# Balance Sheet - equity reconciliation ladder step 1: built first so each
# year's own Total equity is the independent check value for the equity
# sheet below. All 5 years tie exactly to the equity statement's own
# opening/closing balances - zero plug rows needed anywhere.
# ---------------------------------------------------------------
bs_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and balances at central banks", {"FY2025": 24687, "FY2024": 17404, "FY2023": 6870, "FY2022": 47133, "FY2021": 20144, "FY2020": 14613, "FY2019": 122601, "FY2018": 15, "FY2017": 52687, "FY2016": 63784, "FY2015": 30279, "FY2014": 3308, "FY2013": 28138, "FY2012": 31428, "FY2011": 13459, "FY2010": 29719, "FY2009": 16153}),
    ("DATA", "Secured financing", {"FY2025": 836854, "FY2024": 1163336, "FY2023": 1150162, "FY2022": 1330363, "FY2021": 1139856, "FY2020": 1501101, "FY2019": 1480900, "FY2018": 1280633, "FY2017": 1039793, "FY2016": 879913, "FY2015": 921954, "FY2014": 825761}),
    ("DATA", "Reverse repurchase agreements (FY2010-FY2013 label; not separately disclosed FY2009)", {"FY2013": 2807459, "FY2012": 2194621, "FY2011": 1952073, "FY2010": 1456466}),
    ("DATA", "Loans and advances to banks", {"FY2025": 140542, "FY2024": 212774, "FY2023": 187090, "FY2022": 175841, "FY2021": 129608, "FY2020": 337581, "FY2019": 131940, "FY2018": 107412, "FY2017": 147815, "FY2016": 157136, "FY2015": 89547, "FY2014": 152123, "FY2013": 172848, "FY2012": 270996, "FY2011": 624248, "FY2010": 352185, "FY2009": 187133}),
    ("DATA", "Loans and advances to customers", {"FY2025": 422190, "FY2024": 775727, "FY2023": 760186, "FY2022": 1227715, "FY2021": 380124, "FY2020": 24573, "FY2019": 180250, "FY2018": 363113, "FY2017": 354177, "FY2016": 385052, "FY2015": 155311, "FY2014": 617659, "FY2013": 965499, "FY2012": 756208, "FY2011": 748579, "FY2010": 2499609, "FY2009": 1499221}),
    ("DATA", "Trading financial assets", {"FY2025": 3022186, "FY2024": 3746151, "FY2023": 3613350, "FY2022": 4868282, "FY2021": 3358044, "FY2020": 4184122, "FY2019": 3446503, "FY2018": 3290194, "FY2017": 3572024, "FY2016": 4123722, "FY2015": 3358901, "FY2014": 3247108, "FY2013": 2646987, "FY2012": 3161175, "FY2011": 3503456, "FY2010": 3477185, "FY2009": 3930918}),
    ("DATA", "Investment securities", {"FY2025": 23, "FY2024": 472, "FY2023": 463, "FY2022": 23, "FY2021": 679, "FY2020": 4828, "FY2019": 6557}),
    ("DATA", "Financial assets designated at fair value through profit or loss", {"FY2014": 0, "FY2013": 44842, "FY2012": 46916, "FY2011": 41704, "FY2010": 0, "FY2009": 3117}),
    ("DATA", "Investment in subsidiary undertaking", {"FY2021": 105374, "FY2020": 105374, "FY2019": 105374, "FY2018": 105374, "FY2017": 105374, "FY2016": 105374, "FY2015": 105374, "FY2014": 105374, "FY2013": 105374, "FY2012": 105374, "FY2011": 105374, "FY2010": 105374, "FY2009": 105374}),
    ("DATA", "Tangible fixed assets", {"FY2025": 681, "FY2024": 926, "FY2023": 1093, "FY2022": 1382, "FY2021": 567, "FY2020": 749, "FY2019": 3618, "FY2018": 898, "FY2017": 848, "FY2016": 1065, "FY2015": 1022, "FY2014": 437, "FY2013": 570, "FY2012": 780, "FY2011": 984, "FY2010": 1447, "FY2009": 1761}),
    ("DATA", "Other receivables", {"FY2025": 26119, "FY2024": 23892, "FY2023": 34100, "FY2022": 30374, "FY2021": 22811, "FY2020": 13774, "FY2019": 10013, "FY2018": 16071, "FY2017": 29716, "FY2016": 11526, "FY2015": 19736, "FY2014": 23098}),
    ("DATA", "Other assets (FY2009-FY2013 label - a broader concept than 'Other receivables' above, see sourcing note)", {"FY2013": 36385, "FY2012": 33861, "FY2011": 34290, "FY2010": 288012, "FY2009": 271942}),
    ("DATA", "Current tax assets", {"FY2025": 1218, "FY2024": 282, "FY2023": 296, "FY2022": 2451, "FY2021": 287, "FY2020": 2010, "FY2019": 3654, "FY2018": 5844, "FY2017": 5310, "FY2016": 4088, "FY2015": 5623}),
    ("DATA", "Deferred tax assets", {"FY2025": 75, "FY2024": 1961, "FY2023": 7415, "FY2022": 7698, "FY2021": 8696, "FY2020": 2350, "FY2019": 5401, "FY2018": 8596, "FY2017": 13102, "FY2016": 10381, "FY2015": 3311}),
    ("DATA", "Prepayments and accrued income", {"FY2025": 126, "FY2024": 157, "FY2023": 156, "FY2022": 172, "FY2021": 127, "FY2020": 130, "FY2019": 445, "FY2018": 555, "FY2017": 504, "FY2016": 25, "FY2015": 38, "FY2014": 68, "FY2013": 70, "FY2012": 122, "FY2011": 95, "FY2010": 2217, "FY2009": 188}),
    ("TOTAL", "Total assets", {"FY2025": 4474701, "FY2024": 5943082, "FY2023": 5761181, "FY2022": 7691434, "FY2021": 5166317, "FY2020": 6191205, "FY2019": 5497256, "FY2018": 5178705, "FY2017": 5321350, "FY2016": 5742066, "FY2015": 4691096, "FY2014": 4974936, "FY2013": 6808172, "FY2012": 6601481, "FY2011": 7024262, "FY2010": 8212214, "FY2009": 6015807}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Deposits by banks", {"FY2025": 279651, "FY2024": 462429, "FY2023": 251784, "FY2022": 440764, "FY2021": 153851, "FY2020": 124229, "FY2019": 135962, "FY2018": 323778, "FY2017": 226045, "FY2016": 230883, "FY2015": 110708, "FY2014": 101036, "FY2013": 137581, "FY2012": 202366, "FY2011": 212465, "FY2010": 233641, "FY2009": 268609}),
    ("DATA", "Customer accounts", {"FY2025": 632759, "FY2024": 783693, "FY2023": 1246212, "FY2022": 1814583, "FY2021": 1502764, "FY2020": 1647638, "FY2019": 1331496, "FY2018": 1072143, "FY2017": 875555, "FY2016": 747831, "FY2015": 719706, "FY2014": 1092621, "FY2013": 860388, "FY2012": 919422, "FY2011": 2657109, "FY2010": 4184133, "FY2009": 1665107}),
    ("DATA", "Secured borrowing", {"FY2025": 103105, "FY2024": 123656, "FY2023": 86502, "FY2022": 128224, "FY2021": 85181, "FY2020": 60718, "FY2019": 273663, "FY2018": 258331, "FY2017": 363057, "FY2016": 478743, "FY2015": 499063, "FY2014": 542723}),
    ("DATA", "Repurchase agreements / securities sold under agreements to repurchase (FY2009-FY2013 label)", {"FY2013": 3122575, "FY2012": 2002150, "FY2011": 698476, "FY2010": 585076, "FY2009": 1032682}),
    ("DATA", "Trading financial liabilities", {"FY2025": 2409008, "FY2024": 3311515, "FY2023": 2957832, "FY2022": 4081489, "FY2021": 2270962, "FY2020": 3206555, "FY2019": 2762477, "FY2018": 2528574, "FY2017": 2893498, "FY2016": 3373992, "FY2015": 2511905, "FY2014": 2409122, "FY2013": 1824899, "FY2012": 2194711, "FY2011": 2175345, "FY2010": 1905986, "FY2009": 1783226}),
    ("DATA", "Financial liabilities designated at fair value through profit or loss", {"FY2014": 0, "FY2013": 44842, "FY2012": 18465, "FY2011": 18357, "FY2010": 0, "FY2009": 3117}),
    ("DATA", "Other payables", {"FY2025": 18473, "FY2024": 20906, "FY2023": 27230, "FY2022": 45937, "FY2021": 41460, "FY2020": 55647, "FY2019": 13919, "FY2018": 42337, "FY2017": 23819, "FY2016": 19090, "FY2015": 16116, "FY2014": 14042, "FY2013": 13735, "FY2012": 31088, "FY2011": 29918, "FY2010": 147590, "FY2009": 142885}),
    ("DATA", "Accruals and deferred income", {"FY2025": 4080, "FY2024": 9391, "FY2023": 2059, "FY2022": 1497, "FY2021": 2290, "FY2020": 5317, "FY2019": 11790, "FY2018": 14202, "FY2017": 9514, "FY2016": 17150, "FY2015": 25874, "FY2014": 29563, "FY2013": 43724, "FY2012": 40199, "FY2011": 37914, "FY2010": 21257, "FY2009": 24969}),
    ("DATA", "Current tax liabilities", {"FY2025": 19853, "FY2024": 11677, "FY2023": 13754, "FY2022": 10758, "FY2021": 37356, "FY2020": 28260, "FY2019": 4047, "FY2018": 14560, "FY2017": 24501, "FY2016": 24655, "FY2015": 5945}),
    ("DATA", "Deferred tax liabilities", {"FY2025": 1079, "FY2024": 0, "FY2016": 0, "FY2015": 3567}),
    ("DATA", "Retirement benefit liability", {"FY2025": 394, "FY2024": 424, "FY2023": 126, "FY2022": 111, "FY2021": 287, "FY2020": 244, "FY2019": 557, "FY2018": 429, "FY2017": 685, "FY2016": 513, "FY2015": 433, "FY2014": 522, "FY2013": 474, "FY2012": 623, "FY2011": 1970, "FY2010": 1895, "FY2009": 2383}),
    ("DATA", "Provisions for liabilities and charges", {"FY2025": 178, "FY2024": 179, "FY2023": 193, "FY2022": 203, "FY2021": 183, "FY2020": 236, "FY2019": 376, "FY2018": 158, "FY2014": 0, "FY2013": 9150, "FY2012": 0, "FY2011": 0, "FY2010": 891, "FY2009": 923}),
    ("DATA", "Subordinated debt", {"FY2025": 258220, "FY2024": 408727, "FY2023": 409506, "FY2022": 401644, "FY2021": 250000, "FY2020": 250000, "FY2019": 250000, "FY2018": 250000, "FY2017": 250000, "FY2016": 250000, "FY2015": 250000, "FY2014": 250000, "FY2013": 250000, "FY2012": 250000, "FY2011": 250000, "FY2010": 250000, "FY2009": 250000}),
    ("TOTAL", "Total liabilities", {"FY2025": 3726800, "FY2024": 5132597, "FY2023": 4995198, "FY2022": 6925210, "FY2021": 4344334, "FY2020": 5378844, "FY2019": 4784287, "FY2018": 4504512, "FY2017": 4666674, "FY2016": 5142857, "FY2015": 4143317, "FY2014": 4439629, "FY2013": 6307368, "FY2012": 5659024, "FY2011": 6081554, "FY2010": 7330469, "FY2009": 5173901}),
    ("SECTION", "Equity", {}),
    ("DATA", "Called up share capital", {"FY2025": 340000, "FY2024": 340000, "FY2023": 340000, "FY2022": 340000, "FY2021": 340000, "FY2020": 340000, "FY2019": 340000, "FY2018": 340000, "FY2017": 340000, "FY2016": 340000, "FY2015": 340000, "FY2014": 340000, "FY2013": 340000, "FY2012": 790000, "FY2011": 790000, "FY2010": 790000, "FY2009": 790000}),
    ("DATA", "Capital contribution reserve", {"FY2025": 89654, "FY2024": 89654, "FY2023": 89654, "FY2022": 89654, "FY2021": 89654, "FY2020": 89654, "FY2019": 89654, "FY2018": 89654, "FY2017": 89654, "FY2016": 89654, "FY2015": 89654, "FY2014": 89654, "FY2013": 89654, "FY2012": 89654, "FY2011": 89654, "FY2010": 89654, "FY2009": 89654}),
    ("DATA", "Foreign currency revaluation reserve", {"FY2025": 35165, "FY2024": 35368, "FY2023": 36668, "FY2022": 37201, "FY2021": 37213, "FY2020": 37546, "FY2019": 36629, "FY2018": 35801, "FY2017": 43119, "FY2016": 37348, "FY2015": 13889, "FY2014": 16168, "FY2013": 14366, "FY2012": 13172, "FY2011": 8904, "FY2010": 10228, "FY2009": 4615}),
    ("DATA", "Pension reserve (FY2009 only - folded into Profit and loss account from FY2010 onward, see sourcing note)", {"FY2009": 252}),
    ("DATA", "Profit and loss account", {"FY2025": 283082, "FY2024": 345463, "FY2023": 299661, "FY2022": 299369, "FY2021": 355116, "FY2020": 345161, "FY2019": 246686, "FY2018": 208738, "FY2017": 181903, "FY2016": 132207, "FY2015": 104236, "FY2014": 89485, "FY2013": 56784, "FY2012": 49631, "FY2011": 54150, "FY2010": -8137, "FY2009": -42615}),
    ("TOTAL", "Equity shareholders' funds", {"FY2025": 747901, "FY2024": 810485, "FY2023": 765983, "FY2022": 766224, "FY2021": 821983, "FY2020": 812361, "FY2019": 712969, "FY2018": 674193, "FY2017": 654676, "FY2016": 599209, "FY2015": 547779, "FY2014": 535307, "FY2013": 500804, "FY2012": 942457, "FY2011": 942708, "FY2010": 881745, "FY2009": 841906}),
    ("TOTAL", "Total liabilities and equity", {"FY2025": 4474701, "FY2024": 5943082, "FY2023": 5761181, "FY2022": 7691434, "FY2021": 5166317, "FY2020": 6191205, "FY2019": 5497256, "FY2018": 5178705, "FY2017": 5321350, "FY2016": 5742066, "FY2015": 4691096, "FY2014": 4974936, "FY2013": 6808172, "FY2012": 6601481, "FY2011": 7024262, "FY2010": 8212214, "FY2009": 6015807}),
]

bw.add_balance_sheet_sheet(
    title="Morgan Stanley Bank International Limited — Balance Sheet",
    subtitle="Standalone Company basis (FRS 101). £'000. FY2021 uniquely shows an 'Investment in subsidiary "
              "undertaking' line (£105,374k) - disposed of during FY2022, generating that year's £93,978k 'Gain "
              "on disposal of subsidiary' on the Profit & Loss sheet and dropping to £nil from FY2022 onward. "
              "'Deferred tax liabilities' only appears as its own line from FY2024 (shown as '–'/nil that year, "
              "£1,079k in FY2025); FY2021-FY2023 disclose no such line at all (shown blank, not zero).",
    rows=bs_rows,
    sources_text=STATUTORY_SOURCES,
    first_col_width=68,
    source_height=260,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Profit & Loss
# ---------------------------------------------------------------
pl_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest receivable and similar income", {"FY2025": 111211, "FY2024": 150183, "FY2023": 176532, "FY2022": 67078, "FY2021": 17558, "FY2020": 47242, "FY2019": 46585, "FY2018": 34101, "FY2017": 33340, "FY2016": 28414, "FY2015": 42958, "FY2014": 42225, "FY2013": 46892, "FY2012": 87747, "FY2011": 149909, "FY2010": 155163, "FY2009": 174453}),
    ("DATA", "Interest payable and similar charges", {"FY2025": -67596, "FY2024": -93121, "FY2023": -124244, "FY2022": -46738, "FY2021": -2930, "FY2020": -14088, "FY2019": -34627, "FY2018": -33005, "FY2017": -19856, "FY2016": -22865, "FY2015": -23802, "FY2014": -28141, "FY2013": -23086, "FY2012": -73353, "FY2011": -97833, "FY2010": -84753, "FY2009": -93442}),
    ("TOTAL", "Net interest income", {"FY2025": 43615, "FY2024": 57062, "FY2023": 52288, "FY2022": 20340, "FY2021": 14628, "FY2020": 33154, "FY2019": 11958, "FY2018": 1096, "FY2017": 13484, "FY2016": 5549, "FY2015": 19156, "FY2014": 14084, "FY2013": 23806, "FY2012": 14394, "FY2011": 52076, "FY2010": 70410, "FY2009": 81011}),
    ("DATA", "Fee and commission income", {"FY2025": 9777, "FY2024": 10790, "FY2023": 9348, "FY2022": 2326, "FY2021": 21255, "FY2020": 85890, "FY2019": 69862, "FY2018": 81612, "FY2017": 77076, "FY2016": 65328, "FY2015": 59469, "FY2014": 73950, "FY2013": 89400, "FY2012": 97048, "FY2011": 124883, "FY2010": 84491, "FY2009": 79946}),
    ("DATA", "Fee and commission expense", {"FY2025": -5676, "FY2024": -6506, "FY2023": -16211, "FY2022": -14348, "FY2021": -12916, "FY2020": -9760, "FY2019": -10179, "FY2018": -8658, "FY2017": -3149, "FY2016": -7299, "FY2015": -12727, "FY2014": -17742, "FY2013": -6979, "FY2012": -7200, "FY2011": -9511, "FY2010": -7676, "FY2009": -2304}),
    ("DATA", "Net gain from financial instruments at fair value through profit or loss", {"FY2025": 23982, "FY2024": 30718, "FY2023": 21129, "FY2022": 36542, "FY2021": 42393}),
    ("DATA", "Net trading income / net gains on financial instruments classified as held for trading", {"FY2020": 98050, "FY2019": 56209, "FY2018": 46548, "FY2017": 44951, "FY2016": 20426, "FY2015": 29719, "FY2014": 26609, "FY2013": 27093, "FY2012": 1472, "FY2011": -20927, "FY2010": -18066, "FY2009": 39620}),
    ("DATA", "Net (loss)/income from other financial instruments held at fair value", {"FY2020": -6193, "FY2019": 432, "FY2018": -1049}),
    ("DATA", "Net gains/(losses) on financial instruments designated at fair value through profit or loss (FY2009-FY2013 label)", {"FY2013": 392, "FY2012": 1121, "FY2011": 1328, "FY2010": 0, "FY2009": 0}),
    ("DATA", "Net gains/(losses) on loans and receivables (pre-IFRS 9; FY2017 per the Company's own FY2017 report - "
             "the FY2018 report's restated FY2017 comparative instead splits this into a -389 derecognition loss "
             "and a +1,733 impairment reversal, net identical)", {"FY2017": 1344, "FY2016": 563, "FY2015": -21812, "FY2014": -6678, "FY2013": -55839, "FY2012": -27963, "FY2011": 9792, "FY2010": 15851, "FY2009": -95460}),
    ("DATA", "Net reversal of impairment loss on financial instruments", {"FY2022": 0, "FY2021": 416, "FY2020": -406, "FY2019": 20, "FY2018": 160}),
    ("DATA", "Gain on disposal of subsidiary", {"FY2022": 93978}),
    ("DATA", "Other operating income (FY2009-FY2013)", {"FY2013": 78, "FY2012": 198, "FY2011": 0, "FY2010": 2, "FY2009": 19}),
    ("DATA", "Gain on disposal of discontinued operations", {"FY2014": 665, "FY2013": 1692}),
    ("DATA", "Administrative expenses", {"FY2025": -21070, "FY2024": -27722, "FY2023": -34895, "FY2022": -32647, "FY2021": -48725, "FY2020": -76126, "FY2019": -81870, "FY2018": -82152, "FY2017": -75348, "FY2016": -41791, "FY2015": -44792, "FY2014": -57487, "FY2013": -66190, "FY2012": -73750, "FY2011": -74975, "FY2010": -79017, "FY2009": -85141}),
    ("DATA", "Depreciation of tangible fixed assets", {"FY2025": -239, "FY2024": -229, "FY2023": -267, "FY2022": -270, "FY2021": -215, "FY2020": -1058, "FY2019": -1310, "FY2018": -482, "FY2017": -418, "FY2016": -362, "FY2015": -236, "FY2014": -180, "FY2013": -421, "FY2012": -646, "FY2011": -699, "FY2010": -830, "FY2009": -988}),
    ("TOTAL", "Profit before tax", {"FY2025": 50389, "FY2024": 64113, "FY2023": 31392, "FY2022": 105921, "FY2021": 16836, "FY2020": 123551, "FY2019": 45122, "FY2018": 37075, "FY2017": 57940, "FY2016": 42414, "FY2015": 28777, "FY2014": 33221, "FY2013": 13032, "FY2012": 4674, "FY2011": 81967, "FY2010": 65165, "FY2009": 16703}),
    ("DATA", "Income tax expense", {"FY2025": -12810, "FY2024": -18332, "FY2023": -31078, "FY2022": -11768, "FY2021": -6959, "FY2020": -29121, "FY2019": -7000, "FY2018": -9382, "FY2017": -8235, "FY2016": -14426, "FY2015": -10643, "FY2014": -2455, "FY2013": -5877, "FY2012": -9017, "FY2011": -19568, "FY2010": -29201, "FY2009": -29089}),
    ("TOTAL", "Profit for the year", {"FY2025": 37579, "FY2024": 45781, "FY2023": 314, "FY2022": 94153, "FY2021": 9877, "FY2020": 94430, "FY2019": 38122, "FY2018": 27693, "FY2017": 49705, "FY2016": 27988, "FY2015": 18134, "FY2014": 30766, "FY2013": 7155, "FY2012": -4343, "FY2011": 62399, "FY2010": 35964, "FY2009": -12386}),
    ("SECTION", "Other comprehensive income/(loss), net of tax", {}),
    ("DATA", "Remeasurement of net defined benefit liability", {"FY2025": 40, "FY2024": 21, "FY2023": -22, "FY2022": 100, "FY2021": 78, "FY2020": -234, "FY2019": -174, "FY2018": 2, "FY2017": -9, "FY2016": -17, "FY2015": 195, "FY2014": -124, "FY2013": 6, "FY2012": -126, "FY2011": 48, "FY2010": -109, "FY2009": -634}),
    ("DATA", "Foreign currency translation differences arising on foreign operations", {"FY2025": -8951, "FY2024": -19706, "FY2023": -15179, "FY2022": 10400, "FY2021": -14755, "FY2020": 6114, "FY2019": -12707, "FY2018": 2752, "FY2017": 5771, "FY2016": 23459, "FY2015": -2279, "FY2014": 1802, "FY2013": 1194, "FY2012": 4268, "FY2011": -1324, "FY2010": 5613, "FY2009": 2142}),
    ("DATA", "Gain/(loss) arising on hedging instruments designated in net investment hedges", {"FY2025": 8748, "FY2024": 18406, "FY2023": 14646, "FY2022": -10412, "FY2021": 14422, "FY2020": -5197, "FY2019": 13535, "FY2018": -10070}),
    ("TOTAL", "Other comprehensive income/(loss) after income tax", {"FY2025": -163, "FY2024": -1279, "FY2023": -555, "FY2022": 88, "FY2021": -255, "FY2020": 683, "FY2019": 654, "FY2018": -7316, "FY2017": 5762, "FY2016": 23442, "FY2015": -2084, "FY2014": 1678, "FY2013": 1200, "FY2012": 4142, "FY2011": -1276, "FY2010": 5504, "FY2009": 1508}),
    ("TOTAL", "Total comprehensive income for the year", {"FY2025": 37416, "FY2024": 44502, "FY2023": -241, "FY2022": 94241, "FY2021": 9622, "FY2020": 95113, "FY2019": 38776, "FY2018": 20377, "FY2017": 55467, "FY2016": 51430, "FY2015": 16050, "FY2014": 32444, "FY2013": 8355, "FY2012": -201, "FY2011": 61123, "FY2010": 41468, "FY2009": -10878}),
]

bw.add_income_statement_sheet(
    title="Morgan Stanley Bank International Limited — Profit & Loss",
    subtitle="Standalone Company basis (FRS 101). £'000. FY2022's 'Gain on disposal of subsidiary' (£93,978k) is "
              "the disposal of the subsidiary undertaking held on the FY2021 Balance Sheet. FY2021/FY2022 disclose "
              "a 'Net reversal of impairment loss on financial instruments' line not shown FY2023-FY2025 (genuinely "
              "£nil/not disclosed those years, not omitted).",
    rows=pl_rows,
    sources_text=STATUTORY_SOURCES,
    first_col_width=78,
    source_height=260,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Statement of Changes in Equity - per-year reconciliation ladder confirmed
# exactly across all 5 years (opening ties to prior closing, closing ties to
# that year's own Balance Sheet Total equity) via the FY2022 Annual Report's
# own FY2021 comparative for the FY2021 opening balance (at 1 January 2021).
# Zero plug rows needed anywhere.
# ---------------------------------------------------------------
equity_headers = ["Called up share capital", "Capital contribution reserve",
                   "Foreign currency revaluation reserve", "Profit and loss account", "Total equity"]
equity_rows = [
    ("TOTAL", "At 1 January 2009 (FY2009 opening, per the FY2009 Annual Report's own Note 25 - the 'Pension "
              "reserve' component (£886k) is folded into this Profit and loss account column here, matching how "
              "the Company's own later Annual Reports (FY2011 onward) present this same balance with no separate "
              "Pension reserve column at all - see sourcing note)", (790000, 89654, 2473, -30588, 851539)),
    ("DATA", "Profit/(loss) for the period", (None, None, None, -12386, -12386)),
    ("DATA", "Remeasurement of net defined benefit pension liability, net of deferred tax (folded into the "
             "Profit and loss account column per Note 25 - see above)", (None, None, None, -634, -634)),
    ("DATA", "Foreign currency translation differences arising during the period", (None, None, 2142, None, 2142)),
    ("DATA", "Share-based payments", (None, None, None, 1245, 1245)),
    ("TOTAL", "At 31 December 2009 (FY2009 closing, per the Company's own FY2009 Annual Report Note 25)", (790000, 89654, 4615, -42363, 841906)),
    ("DATA", "Profit for the year", (None, None, None, 35964, 35964)),
    ("DATA", "Remeasurement loss on net defined benefit liability", (None, None, None, -109, -109)),
    ("DATA", "Foreign currency translation differences arising during the year", (None, None, 5613, None, 5613)),
    ("DATA", "Share-based payments", (None, None, None, -1629, -1629)),
    ("TOTAL", "At 31 December 2010 (FY2010 closing, per the FY2011 Annual Report's own Note 26 comparative)", (790000, 89654, 10228, -8137, 881745)),
    ("DATA", "Profit for the year", (None, None, None, 62399, 62399)),
    ("DATA", "Remeasurement gain on net defined benefit liability", (None, None, None, 48, 48)),
    ("DATA", "Foreign currency translation differences arising during the year", (None, None, -1324, None, -1324)),
    ("DATA", "Share-based payments", (None, None, None, -160, -160)),
    ("TOTAL", "At 31 December 2011 (FY2011 closing, per the Company's own FY2011 Annual Report Note 26)", (790000, 89654, 8904, 54150, 942708)),
    ("DATA", "Profit/(loss) for the year", (None, None, None, -4343, -4343)),
    ("DATA", "Remeasurement loss on net defined benefit liability", (None, None, None, -126, -126)),
    ("DATA", "Foreign currency translation differences arising during the year", (None, None, 4268, None, 4268)),
    ("DATA", "Share-based payments", (None, None, None, -50, -50)),
    ("TOTAL", "At 31 December 2012 (FY2012 closing, per the FY2013 Annual Report's own Note 26 comparative)", (790000, 89654, 13172, 49631, 942457)),
    ("DATA", "Share capital reduction (27 September 2013 - 450,000,000 £1 ordinary shares redeemed for a £450,000k consideration)", (-450000, None, None, None, -450000)),
    ("DATA", "Profit for the year", (None, None, None, 7155, 7155)),
    ("DATA", "Remeasurement gain on net defined benefit liability", (None, None, None, 6, 6)),
    ("DATA", "Foreign currency translation differences arising during the year", (None, None, 1194, None, 1194)),
    ("DATA", "Share-based payments", (None, None, None, -8, -8)),
    ("TOTAL", "At 1 January 2014 (FY2014 opening, per FY2014 Annual Report's own 2013 comparative)", (340000, 89654, 14366, 56784, 500804)),
    ("DATA", "Profit for the year", (None, None, None, 30766, 30766)),
    ("DATA", "Foreign currency translation differences arising during the year", (None, None, 1802, None, 1802)),
    ("DATA", "Actuarial loss on defined benefit scheme, net of deferred tax", (None, None, None, -124, -124)),
    ("DATA", "Consideration received on transfer of Investment Management business (Note 10)", (None, None, None, 2839, 2839)),
    ("DATA", "Other equity movements (per Note 26; residual not separately itemised in the source reviewed)", (None, None, None, -780, -780)),
    ("TOTAL", "At 31 December 2014 (FY2014 closing, per the Company's own FY2014 Annual Report)", (340000, 89654, 16168, 89485, 535307)),
    ("DATA", "Restatement of opening P&L account balance (per the FY2015/FY2016 Annual Reports' own FY2015 "
             "opening comparative; the £3,578k difference is not itemised in any source reviewed)", (None, None, None, -3578, -3578)),
    ("TOTAL", "At 1 January 2015 (FY2015 opening, restated)", (340000, 89654, 16168, 85907, 531729)),
    ("DATA", "Profit for the year", (None, None, None, 18134, 18134)),
    ("DATA", "Foreign currency translation differences arising during the year", (None, None, -2279, None, -2279)),
    ("DATA", "Remeasurement gain on net defined benefit liability", (None, None, None, 195, 195)),
    ("TOTAL", "At 31 December 2015 (FY2015 closing)", (340000, 89654, 13889, 104236, 547779)),
    ("DATA", "Profit for the year", (None, None, None, 27988, 27988)),
    ("DATA", "Foreign currency translation differences arising during the year", (None, None, 23459, None, 23459)),
    ("DATA", "Remeasurement loss on net defined benefit liability", (None, None, None, -17, -17)),
    ("TOTAL", "At 31 December 2016 (FY2016 closing)", (340000, 89654, 37348, 132207, 599209)),
    ("DATA", "Profit for the year", (None, None, None, 49705, 49705)),
    ("DATA", "Foreign currency translation differences arising during the year", (None, None, 5771, None, 5771)),
    ("DATA", "Remeasurement loss on net defined benefit liability", (None, None, None, -9, -9)),
    ("TOTAL", "At 31 December 2017 (FY2017 closing)", (340000, 89654, 43119, 181903, 654676)),
    ("DATA", "Impact of adoption of new accounting standards (IFRS 9)", (None, None, None, -860, -860)),
    ("DATA", "Profit for the year", (None, None, None, 27693, 27693)),
    ("DATA", "Remeasurement gain on net defined benefit liability", (None, None, None, 2, 2)),
    ("DATA", "Foreign currency translation differences arising on foreign operations", (None, None, 2752, None, 2752)),
    ("DATA", "Loss arising on hedging instruments designated in net investment hedges", (None, None, -10070, None, -10070)),
    ("TOTAL", "At 31 December 2018 (FY2018 closing)", (340000, 89654, 35801, 208738, 674193)),
    ("DATA", "Impact of adoption of new accounting standards", (None, None, None, -174, -174)),
    ("DATA", "Profit for the year", (None, None, None, 38122, 38122)),
    ("DATA", "Other comprehensive income (FY2019: not split into components in the Statement of Changes in "
             "Equity itself)", (None, None, 828, None, 828)),
    ("TOTAL", "At 31 December 2019 (FY2019 closing)", (340000, 89654, 36629, 246686, 712969)),
    ("DATA", "Profit for the year", (None, None, None, 94430, 94430)),
    ("DATA", "Remeasurement loss on net defined benefit liability", (None, None, None, -234, -234)),
    ("DATA", "Foreign currency translation differences arising on foreign operations", (None, None, 6114, None, 6114)),
    ("DATA", "Loss arising on hedging instruments designated in net investment hedges", (None, None, -5197, None, -5197)),
    ("DATA", "Gain on business transfer (UK withdrawal from the EU restructuring, Note 4)", (None, None, None, 5603, 5603)),
    ("DATA", "Current tax charge on business transfer", (None, None, None, -1520, -1520)),
    ("DATA", "Remeasurement gain on net defined benefit liability", (None, None, None, 196, 196)),
    ("TOTAL", "At 31 December 2020 (FY2020 closing)", (340000, 89654, 37546, 345161, 812361)),
    ("TOTAL", "At 1 January 2021 (FY2021 opening)", (340000, 89654, 37546, 345161, 812361)),
    ("DATA", "Profit for the year", (None, None, None, 9877, 9877)),
    ("DATA", "Remeasurement gain on net defined benefit liability", (None, None, None, 78, 78)),
    ("DATA", "Foreign currency translation differences arising during the year", (None, None, -14755, None, -14755)),
    ("DATA", "Gain arising on hedging instruments designated in net investment hedges", (None, None, 14422, None, 14422)),
    ("TOTAL", "At 31 December 2021 (FY2021 closing)", (340000, 89654, 37213, 355116, 821983)),
    ("DATA", "Profit for the year", (None, None, None, 94153, 94153)),
    ("DATA", "Remeasurement gain on net defined benefit liability", (None, None, None, 100, 100)),
    ("DATA", "Foreign currency translation differences arising during the year", (None, None, 10400, None, 10400)),
    ("DATA", "(Loss) arising on hedging instruments designated in net investment hedges", (None, None, -10412, None, -10412)),
    ("DATA", "Dividend", (None, None, None, -150000, -150000)),
    ("TOTAL", "At 31 December 2022 (FY2022 closing)", (340000, 89654, 37201, 299369, 766224)),
    ("DATA", "Profit for the year", (None, None, None, 314, 314)),
    ("DATA", "Remeasurement loss on net defined benefit liability", (None, None, None, -22, -22)),
    ("DATA", "Foreign currency translation differences arising during the year", (None, None, -15179, None, -15179)),
    ("DATA", "Gain arising on hedging instruments designated in net investment hedges", (None, None, 14646, None, 14646)),
    ("TOTAL", "At 31 December 2023 (FY2023 closing)", (340000, 89654, 36668, 299661, 765983)),
    ("DATA", "Profit for the year", (None, None, None, 45781, 45781)),
    ("DATA", "Remeasurement gain on net defined benefit liability", (None, None, None, 21, 21)),
    ("DATA", "Foreign currency translation differences arising during the year", (None, None, -19706, None, -19706)),
    ("DATA", "Gain arising on hedging instruments designated in net investment hedges", (None, None, 18406, None, 18406)),
    ("TOTAL", "At 31 December 2024 (FY2024 closing)", (340000, 89654, 35368, 345463, 810485)),
    ("DATA", "Profit for the year", (None, None, None, 37579, 37579)),
    ("DATA", "Remeasurement gain on net defined benefit liability", (None, None, None, 40, 40)),
    ("DATA", "Foreign currency translation differences arising during the year", (None, None, -8951, None, -8951)),
    ("DATA", "Gain arising on hedging instruments designated in net investment hedges", (None, None, 8748, None, 8748)),
    ("DATA", "Dividends", (None, None, None, -100000, -100000)),
    ("TOTAL", "At 31 December 2025 (FY2025 closing)", (340000, 89654, 35165, 283082, 747901)),
]

bw.add_equity_changes_sheet(
    title="Morgan Stanley Bank International Limited — Statement of Changes in Equity",
    subtitle="Chronological roll-forward, oldest to newest, standalone Company basis (FRS 101/UK GAAP for FY2014). "
              "£'000. Every year's own closing balance ties exactly to both the next year's own opening balance "
              "and that year's own Balance Sheet Total equity for FY2015-FY2025, with zero plug rows needed. "
              "FY2014 is the one exception: the Company's own FY2014 Annual Report closing P&L account balance "
              "(£89,485k) does not match the £85,907k opening comparative shown in the FY2015/FY2016 Annual "
              "Reports - a £3,578k downward restatement not itemised in any source reviewed (plausibly a FRS 101 "
              "transition adjustment), shown here as an explicit 'Restatement' row rather than silently plugged. "
              "The FY2014 row itself also carries a smaller £780k residual (per Note 26's own reconciliation, not "
              "separately itemised) after the disclosed profit, OCI and Investment Management business-transfer "
              "consideration are applied - both gaps are documented, not absorbed into other lines. FY2021 opening "
              "balance ties exactly to the Company's own FY2020 Annual Report closing balance. HD-073 (2026-09-06) "
              "FY2009-FY2013 extension: every year's own closing balance ties exactly to the Balance Sheet's own "
              "Total equity, sourced from each year's own Note 25/26 reconciliation (FY2009 Annual Report Note 25; "
              "FY2011 and FY2013 Annual Reports' own Note 26, which also carry the FY2010 and FY2012 comparatives "
              "respectively) - zero plug rows needed anywhere in this span. FY2009's Balance Sheet shows a separate "
              "'Pension reserve' equity component (£252k at 31 December 2009) not present in any later year; it is "
              "folded into this sheet's Profit and loss account column throughout FY2009 (both opening and "
              "closing), matching how the Company's own FY2011 Annual Report already presents the FY2010 opening/"
              "closing balances with no separate Pension reserve column - a genuine presentational change on the "
              "Company's part, not one introduced by this project.",
    headers=equity_headers,
    rows=equity_rows,
    sources_text=STATUTORY_SOURCES,
    first_col_width=64,
)

# ---------------------------------------------------------------
# Asset Quality - "Exposure to credit risk by class" (Note 28.2.3/28.2.4),
# external-counterparty exposures only. Morgan Stanley Group undertaking
# exposures are separately disclosed each year but are fully offset by
# intercompany collateral/guarantee arrangements (net exposure £nil) and are
# excluded from the totals below as they carry no third-party credit risk.
# Genuine finding: the Company's own Note 28.2.4 confirms ALL exposures
# subject to ECL are Stage 1 in every year reviewed, with £nil Stage 3/
# default balances - a wholesale/broker-dealer credit profile, not a retail
# loan book, so no NPL coverage ratios are meaningful here.
# ---------------------------------------------------------------
asset_quality_rows = [
    ("SECTION", "Exposure to credit risk by class, subject to ECL / gross credit exposure (external counterparties only)", {}),
    ("DATA", "Cash and balances at central banks", {"FY2025": 24687, "FY2024": 17404, "FY2023": 6870, "FY2022": 47133, "FY2021": 20144, "FY2020": 14613, "FY2019": 122601, "FY2018": 15, "FY2017": 52687, "FY2016": 63784, "FY2015": 30279, "FY2014": 3308}),
    ("DATA", "Loans and advances to banks — external counterparties", {"FY2025": 133463, "FY2024": 205239, "FY2023": 181342, "FY2022": 169755, "FY2021": 124091, "FY2020": 330642, "FY2019": 131145, "FY2018": 106124, "FY2017": 144462, "FY2016": 154943, "FY2015": 89402, "FY2014": 150932}),
    ("DATA", "Loans and advances to customers — external counterparties", {"FY2025": 156, "FY2024": 40747, "FY2023": 226, "FY2022": 285, "FY2021": 0, "FY2020": 7206, "FY2019": 28437, "FY2018": 31845, "FY2017": 95640, "FY2016": 82865, "FY2015": 81932, "FY2014": 431190}),
    ("DATA", "Other receivables", {"FY2025": 16304, "FY2024": 20082, "FY2023": 34100, "FY2022": 30374, "FY2021": 22811, "FY2020": 13774, "FY2019": 10013, "FY2018": 16071, "FY2017": 29716, "FY2016": 11526, "FY2015": 19736, "FY2014": 23098}),
    ("TOTAL", "Total gross credit exposure (external)", {"FY2025": 174610, "FY2024": 283472, "FY2023": 222538, "FY2022": 247547, "FY2021": 167046, "FY2020": 366235, "FY2019": 292196, "FY2018": 154055, "FY2017": 322505, "FY2016": 313118, "FY2015": 221349, "FY2014": 608528}),
    ("DATA", "Of which: Stage 1 (IFRS 9, FY2018 onward)", {"FY2025": "100%", "FY2024": "100%", "FY2023": "100%", "FY2022": "100%", "FY2021": "100%", "FY2020": "~99%", "FY2019": "100%", "FY2018": "100%"}),
    ("DATA", "Of which: Stage 3 / default (NPL ratio, IFRS 9, FY2018 onward)", {"FY2025": "0.0%", "FY2024": "0.0%", "FY2023": "0.0%", "FY2022": "0.0%", "FY2021": "0.0%", "FY2020": "0.0%", "FY2019": "0.0%", "FY2018": "0.0%"}),
    ("DATA", "Individually impaired loans and advances to customers, gross (pre-IFRS 9, FY2014-FY2017)", {"FY2017": 131, "FY2016": 126, "FY2015": 1674, "FY2014": 111239}),
]

# The Company explicitly takes the FRS 101 exemption from presenting a cash-flow
# statement. Retain the standard tab and document the structural limitation.
bw.add_cash_flow_sheet(
    "Morgan Stanley Bank International Limited — Statement of Cash Flows",
    "Standalone Company basis; cash-flow statement not presented under the FRS 101 reduced-disclosure exemption",
    [("DATA", "Cash-flow statement not separately disclosed under FRS 101", {})],
    annual_sources() + "\n\n" + HD073_SOURCING_NOTE,
    first_col_width=72,
    source_height=220,
    unit_suffix=" (£'000)",
)

bw.add_asset_quality_sheet(
    title="Morgan Stanley Bank International Limited — Asset Quality",
    subtitle="Exposure to credit risk by class, external counterparties only. £'000. Morgan Stanley Group "
              "undertaking exposures (Secured financing, and large portions of Loans and advances to banks/"
              "customers) are separately disclosed each year but are fully covered by intercompany collateral or "
              "the Morgan Stanley parent guarantee, leaving £nil net exposure — excluded here as not "
              "third-party credit risk. All exposures subject to ECL are internally rated Stage 1 in every "
              "IFRS 9-era year reviewed (£nil Stage 3/default; FY2020 carried a small ~£3.0m Stage 2 loan "
              "commitment balance, immaterial to the total) — a wholesale/broker-dealer credit profile, not a "
              "retail loan book. FY2014-FY2017 predate IFRS 9 (adopted 1 January 2018) and used the incurred-loss "
              "'individually impaired' concept instead of ECL staging; those years' Stage 1/Stage 3 cells are left "
              "blank (the concept did not exist yet) and a separate row reports the actual pre-IFRS 9 impaired "
              "balance. FY2014 is a genuine, material outlier: one borrower's entry into administration in March "
              "2014 drove an £83,173k impairment loss (gross exposure £111,239k, net carrying £28,066k) — over "
              "800x the impaired balances seen in FY2015-FY2017 (£1,674k/£126k/£131k) — a real credit event in "
              "the source documents, not a transcription error.",
    rows=asset_quality_rows,
    sources_text=STATEMENTS_SOURCES + (
        "\n\nFY2025: Note 28.2.3 'Exposure to credit risk by class' p.76, Note 28.2.4 'Exposure to Credit Risk by "
        "Internal Rating Grades' p.77. FY2024/FY2023: Note 27.2.3, p.75. FY2022/FY2021: Note 28.2.4 'Exposure to "
        "Credit Risk' p.72. FY2020: Note 35 'Exposure to credit risk by class' / 'by internal rating grades', "
        f"pp.91-94 — {AR_URLS['FY2020']}. FY2019: via the FY2020 report's own FY2019 comparative, same pages. "
        f"FY2018: Note 32 'Exposure to credit risk by class' p.75 and 'by internal rating grades' pp.77-80 — "
        f"{AR_URLS['FY2018']}. FY2017: Note 28 'Exposure to credit risk by class' p.64 and 'Maximum exposure to "
        f"credit risk by credit rating' p.65 (individually impaired balance) — {AR_URLS['FY2017']}. FY2016: Note "
        f"28 'Exposure to credit risk by class' p.51 and 'Financial assets individually impaired' p.52 — "
        f"{AR_URLS['FY2016']}. FY2015: via the FY2016 report's own FY2015 comparative, same pages. FY2014: Note "
        f"29 'Exposure to credit risk by class' p.51 and 'Financial assets individually impaired' p.52 — "
        f"{AR_URLS['FY2014']}."
    ),
    first_col_width=76,
    source_height=280,
    unit_suffix=" (£'000)",
    years=PILLAR3_YEARS,
)


def metric(name, unit, rows, note=None):
    bw.add_metric_sheet(name, unit, rows, annual_sources(), note=note, first_col_width=54, source_height=220,
                         years=PILLAR3_YEARS)


metric("CET1 Capital", "£'000", [("Common Equity Tier 1 (CET1) capital", {
    "FY2025": 676229, "FY2024": 709078, "FY2023": 685522, "FY2022": 702944, "FY2021": 717693,
    "FY2020": 574718, "FY2019": 593318, "FY2018": 578569, "FY2017": 543786, "FY2016": 517117, "FY2015": 472587,
})])
metric("CET1 Ratio", "% of RWA", [("CET1 capital ratio", {
    "FY2025": "42.6%", "FY2024": "46.7%", "FY2023": "31.7%", "FY2022": "34.0%", "FY2021": "34.4%",
    "FY2020": "23.3%", "FY2019": "20.9%", "FY2018": "17.3%", "FY2017": "19.0%", "FY2016": "18.4%", "FY2015": "17.1%",
})], note="FY2015-FY2018: the annual reports disclose only 'Tier 1 capital' and 'Tier 1 capital ratio', not a "
          "separately-labelled CET1 figure. The FY2019/FY2020 reports' own Own Funds tables confirm CET1 = Tier 1 "
          "capital exactly in both years (no Additional Tier 1 instruments), so the disclosed Tier 1 figures are "
          "used here on that structural basis. FY2014: no capital ratio of any kind was disclosed (see Total RWAs "
          "sheet note).")
metric("Tier 1 Capital", "£'000", [("Tier 1 capital", {
    "FY2025": 676229, "FY2024": 709078, "FY2023": 685522, "FY2022": 702944, "FY2021": 717693,
    "FY2020": 574718, "FY2019": 593318, "FY2018": 578569, "FY2017": 543786, "FY2016": 517117, "FY2015": 472587,
})])
metric("Tier 1 Ratio", "% of RWA", [("Tier 1 capital ratio", {
    "FY2025": "42.6%", "FY2024": "46.7%", "FY2023": "31.7%", "FY2022": "34.0%", "FY2021": "34.4%",
    "FY2020": "23.3%", "FY2019": "20.9%", "FY2018": "17.3%", "FY2017": "19.0%", "FY2016": "18.4%", "FY2015": "17.1%",
})])
metric("Total Capital", "£'000", [("Total capital resources", {
    "FY2025": 934449, "FY2024": 908739, "FY2023": 935655, "FY2022": 1003410, "FY2021": 916488,
    "FY2020": 824718, "FY2019": 843318,
})], note="FY2014-FY2018: Total Capital / Total Own Funds was not disclosed - only Tier 1 capital, Tier 1 ratio "
          "and leverage ratio appear in those years' annual reports.")
metric("Total Capital Ratio", "% of RWA", [("Total capital ratio", {
    "FY2025": "58.9%", "FY2024": "59.8%", "FY2023": "43.3%", "FY2022": "48.5%", "FY2021": "44.0%",
    "FY2020": "33.5%", "FY2019": "29.7%",
})], note="FY2014-FY2018: not disclosed (see Total Capital sheet note).")
metric("Total RWAs", "£'000", [("Total risk-weighted assets", {
    "FY2025": 1586014, "FY2024": 1519269, "FY2023": 2161713, "FY2022": 2068356, "FY2021": 2081783,
    "FY2020": 2462638, "FY2019": 2836626,
})], note="FY2014-FY2018: Total RWAs were not disclosed as a standalone figure in those years' annual reports "
          "(only Tier 1 capital and Tier 1 ratio, from which RWAs could be back-calculated, but that would be an "
          "estimate rather than a disclosed figure, so is left blank per this project's convention). FY2014: no "
          "capital metric of any kind (CET1/Tier 1/Total Capital/RWA/leverage/LCR/NSFR) was disclosed anywhere in "
          "the FY2014 Annual Report, nor as a comparative in any later report - the KPI section first appears in "
          "the FY2016 report and reaches back only to FY2015. This is a genuine disclosure gap, not an omission "
          "by this project.")

# RWA Breakdown - placed right after Total RWAs per the locked sheet order.
# Sourced from each year's own Strategic Report "RWAs" table (not a separate
# Pillar 3 document - this entity discloses its RWA category split within the
# Annual Report itself). All 5 years tie exactly to the Total RWAs figure above.
rwa_breakdown_rows = [
    ("DATA", "Credit RWAs", {"FY2025": 438035, "FY2024": 427744, "FY2023": 513578, "FY2022": 619276, "FY2021": 736089}),
    ("DATA", "Market RWAs", {"FY2025": 1004032, "FY2024": 964352, "FY2023": 1537651, "FY2022": 1254480, "FY2021": 1098855}),
    ("DATA", "Operational risk RWAs", {"FY2025": 143947, "FY2024": 127173, "FY2023": 110484, "FY2022": 194600, "FY2021": 246839}),
    ("TOTAL", "Total RWAs", {"FY2025": 1586014, "FY2024": 1519269, "FY2023": 2161713, "FY2022": 2068356, "FY2021": 2081783}),
]
bw.add_rwa_breakdown_sheet(
    title="Morgan Stanley Bank International Limited — RWA Breakdown",
    subtitle="Company's own 'RWAs' table (Strategic Report), by risk category. £'000. Ties exactly to the Total "
              "RWAs sheet in every year FY2021-FY2025. FY2014-FY2020: not disclosed - those years' annual reports "
              "give only a single Total RWAs figure (and only from FY2019 onward; see the Total RWAs sheet), with "
              "no credit/market/operational risk category split found anywhere in the Strategic Report or notes "
              "reviewed.",
    rows=rwa_breakdown_rows,
    sources_text=annual_sources(),
    first_col_width=54,
    source_height=220,
    unit_suffix=" (£'000)",
    years=PILLAR3_YEARS,
)

metric("Leverage Ratio", "£'000 / %", [
    ("Leverage exposure", {"FY2025": 2233488, "FY2024": 2436257, "FY2023": 2874295, "FY2022": 3795132, "FY2021": 2384965,
                            "FY2020": 2900986, "FY2019": 3635898}),
    ("Leverage ratio", {"FY2025": "30.3%", "FY2024": "29.1%", "FY2023": "23.9%", "FY2022": "18.5%", "FY2021": "30.1%",
                         "FY2020": "19.8%", "FY2019": "16.3%", "FY2018": "18.0%", "FY2017": "16.0%", "FY2016": "13.7%", "FY2015": "14.7%"}),
], note="FY2014-FY2018: Leverage exposure (the £'000 figure) was not disclosed, only the leverage ratio itself. "
        "FY2014 has no leverage ratio at all - public disclosure requirements for this ratio only became "
        "effective for reporting periods from 1 January 2015, per the Company's own FY2016 Annual Report.")
metric("LCR", "£'000 / %", [
    ("Liquidity buffer — HQLA", {"FY2025": 1110032, "FY2024": 1825386, "FY2023": 1190200, "FY2022": 1230539, "FY2021": 1240953,
                                  "FY2020": 1594671, "FY2019": 1220056}),
    ("Liquidity coverage ratio", {"FY2025": "412%", "FY2024": "417%", "FY2023": "250%", "FY2022": "191%", "FY2021": "226%",
                                   "FY2020": "219%", "FY2019": "210%"}),
], note="The reports state that the HQLA amounts are reported to the regulator in USD and converted to GBP using an average annual exchange rate; the ratios are calculated using the preceding twelve months. FY2014-FY2018: no LCR/HQLA figure was disclosed anywhere in those years' annual reports (confirmed by direct review of each year's liquidity risk note).")
metric("NSFR", "£'000 / %", [
    ("Available stable funding", {"FY2025": 1485790, "FY2024": 1597110, "FY2023": 2191000, "FY2022": 2344000, "FY2021": "Not disclosed"}),
    ("Required stable funding", {"FY2025": 574724, "FY2024": 716541, "FY2023": 1346000, "FY2022": 1417000, "FY2021": "Not disclosed"}),
    ("Net Stable Funding Ratio", {"FY2025": "263%", "FY2024": "223%", "FY2023": "163%", "FY2022": "165%", "FY2021": "Not disclosed"}),
], note="The Company states that NSFR became a PRA requirement from 1 January 2022; no NSFR was disclosed for FY2014-FY2021.")
bw.add_not_disclosed_metric_sheets(
    ["MREL Ratio"],
    annual_sources() + "\nNo standalone MREL ratio was numerically disclosed in any of the twelve annual reports reviewed (FY2014-FY2025); group-level resolution disclosures were not substituted.",
    years=PILLAR3_YEARS,
)

bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {"FY2025": 4474701, "FY2024": 5943082, "FY2023": 5761181, "FY2022": 7691434, "FY2021": 5166317,
                           "FY2020": 6191205, "FY2019": 5497256, "FY2018": 5178705, "FY2017": 5321350, "FY2016": 5742066, "FY2015": 4691096, "FY2014": 4974936}),
        ("Loans and advances to customers", {"FY2025": 422190, "FY2024": 775727, "FY2023": 760186, "FY2022": 1227715, "FY2021": 380124,
                                              "FY2020": 24573, "FY2019": 180250, "FY2018": 363113, "FY2017": 354177, "FY2016": 385052, "FY2015": 155311, "FY2014": 617659}),
        ("Customer accounts", {"FY2025": 632759, "FY2024": 783693, "FY2023": 1246212, "FY2022": 1814583, "FY2021": 1502764,
                                "FY2020": 1647638, "FY2019": 1331496, "FY2018": 1072143, "FY2017": 875555, "FY2016": 747831, "FY2015": 719706, "FY2014": 1092621}),
        ("Total equity", {"FY2025": 747901, "FY2024": 810485, "FY2023": 765983, "FY2022": 766224, "FY2021": 821983,
                           "FY2020": 812361, "FY2019": 712969, "FY2018": 674193, "FY2017": 654676, "FY2016": 599209, "FY2015": 547779, "FY2014": 535307}),
    ],
    balance_sheet_unit="£'000",
    income_statement_totals=[
        ("Net interest income", {"FY2025": 43615, "FY2024": 57062, "FY2023": 52288, "FY2022": 20340, "FY2021": 14628,
                                  "FY2020": 33154, "FY2019": 11958, "FY2018": 1096, "FY2017": 13484, "FY2016": 5549, "FY2015": 19156, "FY2014": 14084}),
        ("Administrative expenses", {"FY2025": -21070, "FY2024": -27722, "FY2023": -34895, "FY2022": -32647, "FY2021": -48725,
                                      "FY2020": -76126, "FY2019": -81870, "FY2018": -82152, "FY2017": -75348, "FY2016": -41791, "FY2015": -44792, "FY2014": -57487}),
        ("Profit for the year", {"FY2025": 37579, "FY2024": 45781, "FY2023": 314, "FY2022": 94153, "FY2021": 9877,
                                  "FY2020": 94430, "FY2019": 38122, "FY2018": 27693, "FY2017": 49705, "FY2016": 27988, "FY2015": 18134, "FY2014": 30766}),
    ],
    income_statement_unit="£'000",
    equity_changes_totals=[
        ("Opening equity", {"FY2025": 810485, "FY2024": 765983, "FY2023": 766224, "FY2022": 821983, "FY2021": 812361,
                             "FY2020": 712969, "FY2019": 674193, "FY2018": 654676, "FY2017": 599209, "FY2016": 547779, "FY2015": 531729, "FY2014": 500804}),
        ("Total comprehensive income for the year", {"FY2025": 37416, "FY2024": 44502, "FY2023": -241, "FY2022": 94241, "FY2021": 9622,
                                                        "FY2020": 95113, "FY2019": 38776, "FY2018": 20377, "FY2017": 55467, "FY2016": 51430, "FY2015": 16050, "FY2014": 32444}),
        ("Other equity movements, net", {"FY2025": -100000, "FY2024": 0, "FY2023": 0, "FY2022": -150000, "FY2021": 0,
                                          "FY2020": 4279, "FY2019": 0, "FY2018": -860, "FY2017": 0, "FY2016": 0, "FY2015": 0, "FY2014": 2059}),
        ("Closing equity", {"FY2025": 747901, "FY2024": 810485, "FY2023": 765983, "FY2022": 766224, "FY2021": 821983,
                             "FY2020": 812361, "FY2019": 712969, "FY2018": 674193, "FY2017": 654676, "FY2016": 599209, "FY2015": 547779, "FY2014": 535307}),
    ],
    equity_changes_unit="£'000",
    cash_flow_totals=[],
    cash_flow_unit="£'000",
    ratios=[
        ("CET1 Ratio", {"FY2025": "42.6%", "FY2024": "46.7%", "FY2023": "31.7%", "FY2022": "34.0%", "FY2021": "34.4%",
                         "FY2020": "23.3%", "FY2019": "20.9%", "FY2018": "17.3%", "FY2017": "19.0%", "FY2016": "18.4%", "FY2015": "17.1%"}),
        ("Total Capital Ratio", {"FY2025": "58.9%", "FY2024": "59.8%", "FY2023": "43.3%", "FY2022": "48.5%", "FY2021": "44.0%",
                                  "FY2020": "33.5%", "FY2019": "29.7%"}),
        ("Leverage Ratio", {"FY2025": "30.3%", "FY2024": "29.1%", "FY2023": "23.9%", "FY2022": "18.5%", "FY2021": "30.1%",
                             "FY2020": "19.8%", "FY2019": "16.3%", "FY2018": "18.0%", "FY2017": "16.0%", "FY2016": "13.7%", "FY2015": "14.7%"}),
        ("LCR", {"FY2025": "412%", "FY2024": "417%", "FY2023": "250%", "FY2022": "191%", "FY2021": "226%",
                  "FY2020": "219%", "FY2019": "210%"}),
        ("NSFR", {"FY2025": "263%", "FY2024": "223%", "FY2023": "163%", "FY2022": "165%", "FY2021": "Not disclosed"}),
    ],
    note="The Company takes the FRS 101 exemption from presenting a cash-flow statement. Interim Morgan Stanley International Pillar 3 reports are group-level and do not provide defensible standalone MSBIL interim data. FY2014-FY2018: CET1 Ratio uses the disclosed Tier 1 ratio (CET1 = Tier 1 capital in every year checked); Total Capital Ratio, LCR and NSFR are blank where not disclosed (see the RWA/Total Capital/LCR/NSFR sheets for detail); FY2014 additionally has no Leverage Ratio (first required from FY2015) and no capital ratio of any kind besides what appears here.",
)

bw.save("/Users/armaan/code/katalysis/banks/MORGAN STANLEY BANK INTERNATIONAL FINANCIALS.xlsx")
