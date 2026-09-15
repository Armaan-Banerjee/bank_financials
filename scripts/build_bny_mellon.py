import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

# PILLAR-3-ONLY WORKBOOK: The Bank of New York Mellon (International) Limited
# takes the FRS 101 cash-flow-statement disclosure exemption every year (its
# ultimate parent, The Bank of New York Mellon Corporation, publishes its own
# consolidated financial statements including a cash flow statement) - no
# Statement of Cash Flows exists in any year's accounts, confirmed directly in
# the FY2023 and FY2025 financial statements (identical wording) and
# previously also confirmed via 3 separate Companies House filings
# (FY2021/FY2023/FY2025). Pillar 3 disclosures, by contrast, are complete and
# strong for all 5 years, so this workbook keeps the standard 13-sheet
# structure but the "Cash Flow Statement" sheet documents the exemption
# instead of line items, and the Overview sheet omits the cash-flow chart.

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021", "FY2020", "FY2019", "FY2018", "FY2017", "FY2016"]  # most recent first, calendar year-end (31 December)
YEAR_LABEL = {y: y for y in YEARS}

FS2025_URL = "https://www.bnymellon.com/content/dam/bnymellon/documents/pdf/investor-relations/Signed-2025-BNYMIL-Financial-Statements.pdf"
FS2023_URL = "https://www.bnymellon.com/content/dam/bnymellon/documents/pdf/investor-relations/bnymil-financial-statement-2023.pdf"
FS2021_URL = ("https://find-and-update.company-information.service.gov.uk/company/03236121/filing-history/"
              "MzMzNzcwMzgzM2FkaXF6a2N4/document?format=pdf&download=0")  # Companies House, filed 28 Apr 2022, scanned/image-only
FS2020_URL = ("https://find-and-update.company-information.service.gov.uk/company/03236121/filing-history/"
              "MzI5OTc0NjM1MGFkaXF6a2N4/document?format=pdf&download=0")  # Companies House, filed 22 Apr 2021, scanned/image-only
FS2019_URL = ("https://find-and-update.company-information.service.gov.uk/company/03236121/filing-history/"
              "MzI2Mzk0NzI2OWFkaXF6a2N4/document?format=pdf&download=0")  # Companies House, filed 21 Apr 2020, scanned/image-only
FS2018_URL = ("https://find-and-update.company-information.service.gov.uk/company/03236121/filing-history/"
              "MzIzNzIyMzk4NmFkaXF6a2N4/document?format=pdf&download=0")  # Companies House, filed 17 Apr 2019, scanned/image-only
FS2017_URL = ("https://find-and-update.company-information.service.gov.uk/company/03236121/filing-history/"
              "MzIwMzQ1MjI5OWFkaXF6a2N4/document?format=pdf&download=0")  # Companies House, filed 17 Apr 2018, scanned/image-only
FS2016_URL = ("https://find-and-update.company-information.service.gov.uk/company/03236121/filing-history/"
              "MzE3NTQ0NTUzNGFkaXF6a2N4/document?format=pdf&download=0")  # Companies House, filed 19 Apr 2017, scanned/image-only

P3_2021_URL = "https://www.bnymellon.com/content/dam/bnymellon/documents/pdf/investor-relations/the-bank-of-new-york-mellon-international-limited-2021-pillar-3-disclosure.pdf"
P3_2022_URL = "https://www.bnymellon.com/content/dam/bnymellon/documents/pdf/investor-relations/the-bank-of-new-york-mellon-international-limited-2022-pillar-3-disclosure.pdf"
P3_2023_URL = "https://www.bnymellon.com/content/dam/bnymellon/documents/pdf/investor-relations/the-bank-of-new-york-mellon-international-limited-2023-pillar-3-disclosure.pdf"
P3_2024_URL = "https://www.bnymellon.com/content/dam/bnymellon/documents/pdf/investor-relations/the-bank-of-new-york-mellon-international-limited-2024-pillar-3-disclosure.pdf"
P3_2025_URL = "https://www.bnymellon.com/content/dam/bnymellon/documents/pdf/investor-relations/the-bank-of-new-york-mellon-international-limited-2025-pillar-3-disclosure.pdf"
P3_2020_URL = "https://www.bnymellon.com/content/dam/bnymellon/documents/pdf/investor-relations/the-bank-of-new-york-mellon-international-limited-2020-pillar-3-disclosure.pdf"
P3_2019_URL = "https://www.bnymellon.com/content/dam/bnymellon/documents/pdf/investor-relations/the-bank-of-new-york-mellon-international-limited-2019-pillar-3-disclosure.pdf"
P3_2018_URL = "https://www.bnymellon.com/content/dam/bnymellon/documents/pdf/investor-relations/the-bank-of-new-york-mellon-international-limited-2018-pillar-3-disclosure.pdf"
P3_2017_URL = "https://www.bnymellon.com/content/dam/bnymellon/documents/pdf/investor-relations/the-bank-of-new-york-mellon-international-limited-2017-pillar-3-disclosure.pdf"
P3_2016_URL = "https://www.bnymellon.com/content/dam/bnymellon/documents/pdf/investor-relations/the-bank-of-new-york-mellon-international-limited-2016-pillar-3-disclosure.pdf"

ENTITY_NOTE = (
    "ENTITY NOTE: The Bank of New York Mellon (International) Limited (company 03236121, FRN 183100) is a wholly-"
    "owned subsidiary of The Bank of New York Mellon Corporation (US). Figures are the Company's own entity-level "
    "disclosure throughout; the 2021 Pillar 3 report separately labelled 'Consolidated' and 'Solo' bases but both "
    "were identical every year shown (the Company has no material subsidiaries of its own), and from the 2022 "
    "report onward BNY Mellon International's Pillar 3 disclosures present a single, unified figure. Functional/"
    "presentational currency is GBP throughout - no FX conversion needed."
)

EXEMPTION_NOTE = (
    "FRS 101 CASH-FLOW EXEMPTION: this entity's Annual Report and Financial Statements state every year: \"The "
    "Company's ultimate parent undertaking, The Bank of New York Mellon Corporation includes the Company and all "
    "its subsidiary undertakings in its consolidated financial statements... Accordingly, the Company is a "
    "qualifying entity for the purpose of FRS 101 disclosure exemptions... the Company has applied the exemptions "
    "available under FRS 101 in respect of the following disclosures: A Statement of cash flows and related "
    f"notes...\" - FY2025 Financial Statements, note 1.1, p.29 - {FS2025_URL}; identical wording confirmed in the "
    f"FY2023 Financial Statements, note 1.1, p.41 - {FS2023_URL}. This has also been independently confirmed via "
    "Companies House filings for FY2021, FY2023 and FY2025 (OCR'd scanned filings, prior research pass). No "
    "Statement of Cash Flows or cash-flow notes exist in any of the entity's published accounts for any year - this "
    "is a standing structural feature of the entity, not a one-off or a data gap. Per the project's established "
    "policy for this exemption (see United Trust Bank Limited, self-skipped for the same reason), this workbook is "
    "built as a PILLAR-3-ONLY variant: all 11 Pillar 3 metric sheets are fully populated below, but no cash flow "
    "figures exist to show. See the Overview sheet for the equivalent treatment there."
)

CASH_FLOW_SOURCES = ENTITY_NOTE + "\n\n" + EXEMPTION_NOTE

STATEMENTS_SOURCES = (
    "Sources - The Bank of New York Mellon (International) Limited's own audited financial statements (all "
    "Companies House filings FY2016-FY2021 are scanned/image-only, visually transcribed; FY2016-FY2020 sourced for "
    "HD-025):\n"
    f"FY2025/FY2024: Financial Statements, year ended 31 December 2025, Statement of profit and loss p.25, "
    f"Statement of comprehensive income p.26, Balance sheet p.27, Statement of changes in equity p.28 - {FS2025_URL}\n"
    f"FY2023/FY2022: Financial Statements, year ended 31 December 2023, Statement of profit and loss p.37, "
    f"Other comprehensive income p.38, Balance sheet p.39, Statement of changes in equity p.40 - {FS2023_URL}\n"
    f"FY2021 (and FY2020 comparative used for the opening equity roll-forward): Financial Statements, year ended 31 "
    f"December 2021, Statement of profit and loss p.35, Other comprehensive income p.36, Balance sheet p.37, "
    f"Statement of changes in equity p.38 - Companies House filing, 28 April 2022 - {FS2021_URL}\n"
    f"FY2020 (own year): Financial Statements, year ended 31 December 2020, Statement of profit and loss p.30, "
    f"Other comprehensive income p.31, Balance sheet p.32, Statement of changes in equity p.33 - Companies House "
    f"filing, 22 April 2021 - {FS2020_URL}\n"
    f"FY2019: Financial Statements, year ended 31 December 2019, Statement of profit and loss p.26, Other "
    f"comprehensive income p.27, Balance sheet p.28, Statement of changes in equity p.29 - Companies House filing, "
    f"21 April 2020 - {FS2019_URL}\n"
    f"FY2018: Financial Statements, year ended 31 December 2018, Statement of profit and loss p.19, Other "
    f"comprehensive income p.20, Balance sheet p.21, Statement of changes in equity p.22 - Companies House filing, "
    f"17 April 2019 - {FS2018_URL}\n"
    f"FY2017: Financial Statements, year ended 31 December 2017, Statement of profit and loss p.17, Other "
    f"comprehensive income p.18, Balance sheet p.19, Statement of changes in equity p.20 - Companies House filing, "
    f"17 April 2018 - {FS2017_URL}\n"
    f"FY2016: Financial Statements, year ended 31 December 2016, Statement of profit and loss p.15, Other "
    f"comprehensive income p.16, Balance sheet p.17, Statement of changes in equity p.18 - Companies House filing, "
    f"19 April 2017 - {FS2016_URL}\n\n" + ENTITY_NOTE
)

PRESENTATION_NOTE = (
    "PRESENTATION NOTE: this entity's statement structure changed twice across the 5 years shown. (1) Income "
    "statement: FY2021-FY2023 place 'Income from investments in affiliates' before a combined 'Total income' "
    "subtotal; FY2024-FY2025 instead show a narrower 'Total operating income' (excluding investments-in-affiliates "
    "income) and add investments-in-affiliates income only after 'Total operating expenses', immediately before "
    "'Profit before taxation' - both years' own reported total is shown on the 'Total operating income / Total "
    "income' row below, not reconciled to a common basis. FY2024 also separately discloses 'Amounts written off "
    "investments in affiliates' (£57,148k), a line that doesn't exist in the other 4 years. (2) Other comprehensive "
    "income: FY2021-FY2023 split the FVOCI movement into 'Movement in financial assets measured at FVOCI' and a "
    "separate 'Change in ECL on financial assets measured at FVOCI' line; FY2024-FY2025 combine both into a single "
    "'Net movement in financial instruments measured at FVOCI' line - shown on the FVOCI-movement row with the ECL "
    "row left blank those 2 years, not split arbitrarily. (3) Balance sheet: FY2021's own statement uses the label "
    "'Cash in hand and on demand balances at central banks' (relabelled 'Cash and balances at central banks' from "
    "FY2022 onward - same line) and has no separate Intangible assets line (first appears FY2022); 'Deferred tax "
    "asset'/'Deferred tax liabilities' appear as explicit lines (value or nil) only in the years the Company had a "
    "recognised balance or an adjacent-year comparative required it - blank cells mean the year's own statement has "
    "no such line at all, not that the value is unknown. 'Loan due to fellow group undertakings' is a FY2025-only "
    "line (a new, discrete intercompany funding arrangement that year).\n\n"
    "PRE-2021 STRUCTURAL NOTES (added for the HD-025 FY2016-FY2020 extension): (4) FY2016-FY2019 carry a "
    "'Subordinated loan due to fellow Group undertaking' liability line (£75,000k, constant) that FY2020 onward "
    "does not - the loan was redeemed during FY2020 (confirmed via the FY2020 KM1 Pillar 3 table showing Tier 2 "
    "capital fall to nil that year), a real capital-structure event, not a gap. (5) The balance sheet line labelled "
    "'Investment securities' from FY2018 onward is labelled 'Financial instruments - available-for-sale' in "
    "FY2016-FY2017 (pre-IFRS 9; same underlying line, relabelled on the FVOCI transition, consistent with the "
    "P&L's AFS->FVOCI relabelling on the Profit & Loss sheet). (6) The 'Investments in affiliates' line is labelled "
    "simply 'Investments' in FY2016-FY2017 - same continuous ~£171-182m holding across all 5 years, relabelled "
    "FY2018 onward, not a new asset. (7) 'Provisions for liabilities and commitments' appears as a balance-sheet "
    "line every year FY2016-FY2020 except FY2019 (nil/no line that year); it reappears FY2020 (£7,579k, a new "
    "provision raised that year). (8) The Statement of Changes in Equity's 'Fair value reserve' column does not "
    "exist as a separately-disclosed component in FY2016 or in FY2017's own originally-published statement (both "
    "years' fair-value movements are folded into a single combined 'Other reserves' column) - the split first "
    "appears in the FY2018 Annual Report's own restated FY2017 comparative column. This workbook keeps FY2016 and "
    "FY2017 on their own originally-published combined-column basis (Fair value reserve left blank, the full "
    "movement sitting in Other reserves) and shows the FY2018 report's split as an explicit reclassification "
    "bridging row between the FY2017 and FY2018 columns on the Statement of Changes in Equity sheet, per this "
    "project's convention of not silently restating an earlier year's own figures. (9) The FY2018 IFRS 9 "
    "transition (1 January 2018) had a genuine NIL adjustment to opening equity - the FY2018 statement's own "
    "'Restated balance at 1 January 2018' row is identical to the FY2017 closing balance, confirmed directly in "
    "the source rather than assumed."
)


INVESTMENT_SECURITIES_NOTE = (
    "INVESTMENT SECURITIES BREAKDOWN NOTE: 'Total investment securities' is broken down below by measurement basis "
    "(FVOCI vs amortised cost) and by issuer type, sourced from the Company's own Note 17/18/13 'Investment "
    "securities' (numbering varies by year) in the same financial statements cited above for the Balance Sheet - the "
    "sub-rows reconcile exactly to the total in every year:\n"
    f"FY2025/FY2024: Note 17 'Investment securities', pp.61-62 - {FS2025_URL}\n"
    f"FY2023/FY2022: Note 17 'Investment securities', pp.76-77 - {FS2023_URL}\n"
    f"FY2021/FY2020: Note 17 'Investment securities', p.74 - Companies House filing, 28 April 2022 (scanned/image-"
    f"only, OCR'd) - {FS2021_URL}\n"
    f"FY2019/FY2018: Note 18 'Investment securities', p.63 - Companies House filing, 21 April 2020 (scanned/image-"
    f"only, OCR'd) - {FS2019_URL}\n"
    f"FY2017/FY2016: Note 13 'Financial instruments - available-for-sale', p.51 - Companies House filing, 17 April "
    f"2018 (scanned/image-only, OCR'd) - {FS2017_URL}\n"
    "FY2025-FY2018 all disclose a genuine multi-category issuer-type split (Covered bonds, Government guaranteed, "
    "Sovereign debt, Sub-Sovereign debt, Supranational debt, plus Non-Agency Residential Mortgage Backed Securities "
    "FY2025-FY2022 only and Treasuries FY2018 only) within the FVOCI leg, and a small residual Supranational-debt "
    "amortised-cost leg FY2024-FY2022 (nil FY2025). FY2017-FY2016 (pre-IFRS 9, 'Financial instruments - available-"
    "for-sale') disclose no further split at all - the Company's own note shows the entire balance as a single line, "
    "'Debt instruments issued by central governments', i.e. 100% sovereign/government debt those 2 years - reproduced "
    "on the Sovereign debt sub-row above rather than fabricating a finer split that the source doesn't carry. Blank "
    "cells on a sub-row mean that year's own note has no such category at all, not that the value is unknown; a 0 "
    "means the note explicitly shows a nil/dash for that category that year."
)


def p3_sources(page):
    return (
        "Sources - The Bank of New York Mellon (International) Limited Pillar 3 Disclosure, Table 1: UK KM1 - Key "
        "metrics template (entity/'Solo' basis, not the 'Consolidated' column also shown in every report - see "
        "ENTITY NOTE):\n"
        f"FY2025: Pillar 3 Disclosure, December 31, 2025, p.{page['FY2025']} - {P3_2025_URL}\n"
        f"FY2024: Pillar 3 Disclosure, December 31, 2024, p.{page['FY2024']} - {P3_2024_URL}\n"
        f"FY2023: Pillar 3 Disclosure, December 31, 2023, p.{page['FY2023']} - {P3_2023_URL}\n"
        f"FY2022: Pillar 3 Disclosure, December 31, 2022, p.{page['FY2022']} - {P3_2022_URL}\n"
        f"FY2021: Pillar 3 Disclosure, December 31, 2021, p.{page['FY2021']} (\"1.8 Key metrics\") - {P3_2021_URL}\n"
        f"FY2020: Pillar 3 Disclosure 2020, p.{page['FY2020']} (\"Table 1: KM1 - Key metrics\") - {P3_2020_URL}\n"
        f"FY2019: Pillar 3 Disclosure 2019, p.{page['FY2019']} (\"Table 1: KM1 - Key metrics\") - {P3_2019_URL}\n"
        f"FY2018: Pillar 3 Disclosure 2018, p.{page['FY2018']} (\"Table 1: KM1 - Key metrics\") - {P3_2018_URL}\n"
        f"FY2017: Pillar 3 Disclosure 2017, p.{page['FY2017']} (\"Table 1: Capital ratios\") - {P3_2017_URL}\n"
        f"FY2016: Pillar 3 Disclosure, p.{page['FY2016']} (\"1.8 Key Metrics, Table 1: Capital ratios\") - "
        f"{P3_2016_URL}\n"
        "NOTE ON FY2016-FY2020: every report shows both a 'Consolidated' and 'BNYMIL Solo' column; this workbook "
        "uses the Solo (entity-level) column throughout, consistent with FY2021-FY2025. Unlike FY2021-FY2025, "
        "FY2016-FY2019 carry a real Tier 2 capital balance (£74-75m, a subordinated loan from a fellow Group "
        "undertaking - see the Balance Sheet sheet's presentation note) - so Total Capital genuinely exceeds "
        "CET1/Tier 1 in those 4 years; the loan was redeemed during FY2020, after which Total Capital = CET1 = "
        "Tier 1 again, as already true for FY2021-2025.\n"
        + ENTITY_NOTE
    )


KM1_PAGE = {"FY2025": "5", "FY2024": "6", "FY2023": "6", "FY2022": "8", "FY2021": "10-11",
            "FY2020": "12-13", "FY2019": "12-14", "FY2018": "11-12", "FY2017": "9-11", "FY2016": "8-9"}

bw = BankWorkbook(bank_name="The Bank of New York Mellon (International) Limited", years=YEARS,
                   year_label=YEAR_LABEL, header_color="1F3B57")

# ---------------------------------------------------------------
# Balance Sheet
# ---------------------------------------------------------------
balance_sheet_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and balances at central banks", {"FY2025": 2666888, "FY2024": 2687665, "FY2023": 3781275, "FY2022": 4706360, "FY2021": 4949582, "FY2020": 5270609, "FY2019": 4570725, "FY2018": 8487623, "FY2017": 7026059, "FY2016": 4942402}),
    ("DATA", "Loans and advances to banks", {"FY2025": 2037724, "FY2024": 1891637, "FY2023": 1645021, "FY2022": 2520019, "FY2021": 1579113, "FY2020": 795307, "FY2019": 1149814, "FY2018": 2049210, "FY2017": 2085358, "FY2016": 1543683}),
    ("DATA", "Loans and advances to customers", {"FY2025": 28495, "FY2024": 173578, "FY2023": 108153, "FY2022": 138345, "FY2021": 104419, "FY2020": 195590, "FY2019": 117788, "FY2018": 275544, "FY2017": 152291, "FY2016": 112638}),
    ("TOTAL", "Total investment securities", {"FY2025": 2969599, "FY2024": 2994460, "FY2023": 3072747, "FY2022": 4054942, "FY2021": 4357861, "FY2020": 3824637, "FY2019": 3668276, "FY2018": 1298470, "FY2017": 593296, "FY2016": 20353}),
    ("DATA", "Investment securities measured at FVOCI (available-for-sale pre-2018) - Sovereign debt (government)", {"FY2025": 707356, "FY2024": 494219, "FY2023": 229920, "FY2022": 503709, "FY2021": 522683, "FY2020": 146329, "FY2019": 1156170, "FY2018": 145112, "FY2017": 593296, "FY2016": 20353}),
    ("DATA", "Investment securities measured at FVOCI - Covered bonds", {"FY2025": 1131472, "FY2024": 1304511, "FY2023": 1625338, "FY2022": 1517309, "FY2021": 1314732, "FY2020": 1316905, "FY2019": 960811, "FY2018": 382113}),
    ("DATA", "Investment securities measured at FVOCI - Government guaranteed", {"FY2025": 328582, "FY2024": 379110, "FY2023": 390682, "FY2022": 527317, "FY2021": 680887, "FY2020": 564413, "FY2019": 352699, "FY2018": 292892}),
    ("DATA", "Investment securities measured at FVOCI - Sub-Sovereign debt", {"FY2025": 489248, "FY2024": 377500, "FY2023": 370732, "FY2022": 352322, "FY2021": 514317, "FY2020": 388374, "FY2019": 296081, "FY2018": 0}),
    ("DATA", "Investment securities measured at FVOCI - Supranational debt", {"FY2025": 277536, "FY2024": 355747, "FY2023": 374002, "FY2022": 1099825, "FY2021": 1325242, "FY2020": 1408616, "FY2019": 902515, "FY2018": 274388}),
    ("DATA", "Investment securities measured at FVOCI - Non-Agency Residential Mortgage Backed Securities", {"FY2025": 35405, "FY2024": 45886, "FY2023": 44613, "FY2022": 17027}),
    ("DATA", "Investment securities measured at FVOCI - Treasuries", {"FY2019": 0, "FY2018": 203965}),
    ("DATA", "Investment securities measured at amortised cost - Supranational debt", {"FY2025": 0, "FY2024": 37487, "FY2023": 37460, "FY2022": 37433}),
    ("DATA", "Investments in affiliates", {"FY2025": 118150, "FY2024": 127028, "FY2023": 181821, "FY2022": 188620, "FY2021": 174576, "FY2020": 173549, "FY2019": 177636, "FY2018": 181386, "FY2017": 171163, "FY2016": 182342}),
    ("DATA", "Intangible assets", {"FY2025": 2909, "FY2024": 156, "FY2023": 209, "FY2022": 12, "FY2019": 0, "FY2018": 52, "FY2017": 12, "FY2016": 41}),
    ("DATA", "Tangible fixed assets", {"FY2025": 31, "FY2024": 47, "FY2023": 65, "FY2022": 1, "FY2021": 1, "FY2020": 6, "FY2019": 26, "FY2018": 699, "FY2017": 272, "FY2016": 447}),
    ("DATA", "Deferred tax asset", {"FY2024": 8926, "FY2023": 15014, "FY2022": 26967, "FY2021": 2150}),
    ("DATA", "Prepayments and accrued income", {"FY2025": 65789, "FY2024": 58890, "FY2023": 58804, "FY2022": 44398, "FY2021": 27008, "FY2020": 26201, "FY2019": 29609, "FY2018": 37961, "FY2017": 17298, "FY2016": 22717}),
    ("DATA", "Other assets", {"FY2025": 29188, "FY2024": 65384, "FY2023": 33543, "FY2022": 22380, "FY2021": 32358, "FY2020": 29641, "FY2019": 48106, "FY2018": 57423, "FY2017": 71471, "FY2016": 83780}),
    ("TOTAL", "Total assets", {"FY2025": 7918773, "FY2024": 8007771, "FY2023": 8896652, "FY2022": 11702044, "FY2021": 11227068, "FY2020": 10315540, "FY2019": 9761980, "FY2018": 12388368, "FY2017": 10117220, "FY2016": 6908403}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Deposits by banks", {"FY2025": 2240411, "FY2024": 2575276, "FY2023": 3297200, "FY2022": 4164947, "FY2021": 3152969, "FY2020": 2373955, "FY2019": 1589018, "FY2018": 1767652, "FY2017": 2017767, "FY2016": 1617285}),
    ("DATA", "Customer accounts", {"FY2025": 4303354, "FY2024": 4316535, "FY2023": 4583519, "FY2022": 6631188, "FY2021": 7137353, "FY2020": 7004361, "FY2019": 7265408, "FY2018": 9685207, "FY2017": 7459508, "FY2016": 4656755}),
    ("DATA", "Loan due to fellow group undertakings", {"FY2025": 118897}),
    ("DATA", "Subordinated loan due to fellow Group undertaking", {"FY2019": 75000, "FY2018": 75000, "FY2017": 75000, "FY2016": 75000}),
    ("DATA", "Other liabilities", {"FY2025": 31960, "FY2024": 20810, "FY2023": 30819, "FY2022": 28159, "FY2021": 50260, "FY2020": 56983, "FY2019": 40143, "FY2018": 106978, "FY2017": 33326, "FY2016": 37129}),
    ("DATA", "Deferred tax liabilities", {"FY2025": 288, "FY2024": 0, "FY2021": 0, "FY2020": 7727}),
    ("DATA", "Accruals and deferred income", {"FY2025": 7166, "FY2024": 6077, "FY2023": 26455, "FY2022": 9641, "FY2021": 4080, "FY2020": 5828, "FY2019": 5185, "FY2018": 6052, "FY2017": 6961, "FY2016": 6811}),
    ("DATA", "Provisions", {"FY2025": 1656, "FY2024": 4312, "FY2023": 4606, "FY2022": 4753, "FY2021": 4226, "FY2020": 7579, "FY2018": 0, "FY2017": 70, "FY2016": 3753}),
    ("TOTAL", "Total liabilities", {"FY2025": 6703732, "FY2024": 6923010, "FY2023": 7942599, "FY2022": 10838688, "FY2021": 10348888, "FY2020": 9456433, "FY2019": 8974754, "FY2018": 11640889, "FY2017": 9592632, "FY2016": 6396733}),
    ("SECTION", "Capital and reserves", {}),
    ("DATA", "Called up share capital", {"FY2025": 519695, "FY2024": 519695, "FY2023": 519695, "FY2022": 519695, "FY2021": 519695, "FY2020": 519695, "FY2019": 519695, "FY2018": 519695, "FY2017": 519695, "FY2016": 519695}),
    ("DATA", "Fair value reserve", {"FY2025": 1758, "FY2024": -21742, "FY2023": -37213, "FY2022": -67625, "FY2021": -2488, "FY2020": 23365, "FY2019": 1352, "FY2018": -5401}),
    ("DATA", "Other reserves", {"FY2025": 7139, "FY2024": 7139, "FY2023": 7139, "FY2022": 7139, "FY2021": 7150, "FY2020": 7276, "FY2019": 7359, "FY2018": 7352, "FY2017": 3645, "FY2016": 7206}),
    ("DATA", "Profit and loss account", {"FY2025": 686449, "FY2024": 579669, "FY2023": 464432, "FY2022": 404147, "FY2021": 353823, "FY2020": 308771, "FY2019": 258820, "FY2018": 225833, "FY2017": 1248, "FY2016": -15231}),
    ("TOTAL", "Shareholder's funds", {"FY2025": 1215041, "FY2024": 1084761, "FY2023": 954053, "FY2022": 863356, "FY2021": 878180, "FY2020": 859107, "FY2019": 787226, "FY2018": 747479, "FY2017": 524588, "FY2016": 511670}),
    ("TOTAL", "Total liabilities and shareholder's funds", {"FY2025": 7918773, "FY2024": 8007771, "FY2023": 8896652, "FY2022": 11702044, "FY2021": 11227068, "FY2020": 10315540, "FY2019": 9761980, "FY2018": 12388368, "FY2017": 10117220, "FY2016": 6908403}),
]

bw.add_balance_sheet_sheet(
    title="The Bank of New York Mellon (International) Limited — Balance Sheet",
    subtitle="Entity-level basis, £'000s.",
    rows=balance_sheet_rows,
    sources_text=STATEMENTS_SOURCES + "\n\n" + PRESENTATION_NOTE + "\n\n" + INVESTMENT_SECURITIES_NOTE,
    first_col_width=64,
    source_height=440,
    unit_suffix=" (£'000s)",
)

# ---------------------------------------------------------------
# Profit & Loss
# ---------------------------------------------------------------
income_statement_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest receivable and similar income", {"FY2025": 292194, "FY2024": 367509, "FY2023": 368769, "FY2022": 163522, "FY2021": 34976, "FY2020": 52419, "FY2019": 107473, "FY2018": 113871, "FY2017": 37955, "FY2016": 16696}),
    ("DATA", "Interest payable and similar charges", {"FY2025": -197224, "FY2024": -273351, "FY2023": -269549, "FY2022": -92414, "FY2021": -5231, "FY2020": -15533, "FY2019": -57537, "FY2018": -64622, "FY2017": -27213, "FY2016": -11420}),
    ("TOTAL", "Net interest income", {"FY2025": 94970, "FY2024": 94158, "FY2023": 99220, "FY2022": 71108, "FY2021": 29745, "FY2020": 36886, "FY2019": 49936, "FY2018": 49249, "FY2017": 10742, "FY2016": 5276}),
    ("DATA", "Fees and commissions receivable", {"FY2025": 145423, "FY2024": 147547, "FY2023": 139362, "FY2022": 133709, "FY2021": 140708, "FY2020": 125554, "FY2019": 126733, "FY2018": 166234, "FY2017": 131014, "FY2016": 130885}),
    ("DATA", "Net foreign exchange translation gain/(loss)", {"FY2025": 74, "FY2024": -315, "FY2023": -337, "FY2022": -1268, "FY2021": -468, "FY2020": 428, "FY2019": -88, "FY2018": 81, "FY2017": -159, "FY2016": -660}),
    ("DATA", "Other operating income", {"FY2025": 8154, "FY2024": 6088, "FY2023": 10802, "FY2022": 14993, "FY2021": 11998, "FY2020": 14479, "FY2019": 9803, "FY2018": 11766, "FY2017": 30462, "FY2016": 32660}),
    ("TOTAL", "Non-interest income", {"FY2025": 153651, "FY2024": 153320, "FY2023": 149827, "FY2022": 147434, "FY2021": 152238, "FY2020": 140461, "FY2019": 136448, "FY2018": 178081, "FY2017": 161317, "FY2016": 162885}),
    ("TOTAL", "Total operating income (FY2024-25 basis, excl. investments-in-affiliates income)", {"FY2025": 248621, "FY2024": 247478}),
    ("TOTAL", "Total income (FY2016-23 basis, incl. investments-in-affiliates income where disclosed)", {"FY2023": 266563, "FY2022": 240697, "FY2021": 210480, "FY2020": 206619, "FY2019": 200573, "FY2018": 421016, "FY2017": 172059, "FY2016": 168161}),
    ("SECTION", "Expenses", {}),
    ("DATA", "Administration/administrative expenses", {"FY2025": -141192, "FY2024": -156924, "FY2023": -167758, "FY2022": -171390, "FY2021": -155502, "FY2020": -143551, "FY2019": -145271, "FY2018": -176615, "FY2017": -149999, "FY2016": -165422}),
    ("DATA", "Change in Expected Credit Loss (ECL) on financial assets", {"FY2025": 101, "FY2024": 451, "FY2023": -283, "FY2022": -124, "FY2021": 50}),
    ("DATA", "Provisions for liabilities and commitments (movement, pre-2018 presentation)", {"FY2017": 415, "FY2016": 1315}),
    ("TOTAL", "Total operating expenses", {"FY2025": -141091, "FY2024": -156473, "FY2023": -168041, "FY2022": -171514, "FY2021": -155452, "FY2020": -143551, "FY2019": -145271, "FY2018": -176615, "FY2017": -149584, "FY2016": -164107}),
    ("DATA", "Income from investments in affiliates", {"FY2025": 44810, "FY2024": 102898, "FY2023": 17516, "FY2022": 22155, "FY2021": 28497, "FY2020": 29272, "FY2019": 14189, "FY2018": 193686}),
    ("DATA", "Amounts written off investments in affiliates", {"FY2025": 0, "FY2024": -57148}),
    ("TOTAL", "Profit before taxation", {"FY2025": 152340, "FY2024": 136755, "FY2023": 98522, "FY2022": 69183, "FY2021": 55028, "FY2020": 63068, "FY2019": 55302, "FY2018": 244401, "FY2017": 22475, "FY2016": 4054}),
    ("DATA", "Taxation on profit", {"FY2025": -45560, "FY2024": -21518, "FY2023": -38209, "FY2022": -18870, "FY2021": -10102, "FY2020": -13117, "FY2019": -22316, "FY2018": -19816, "FY2017": -5996, "FY2016": -6226}),
    ("TOTAL", "Total profit for the financial year", {"FY2025": 106780, "FY2024": 115237, "FY2023": 60313, "FY2022": 50313, "FY2021": 44926, "FY2020": 49951, "FY2019": 32986, "FY2018": 224585, "FY2017": 16479, "FY2016": -2172}),
    ("SECTION", "Other comprehensive income", {}),
    ("DATA", "Movement in financial assets measured at FVOCI", {"FY2025": 32634, "FY2024": 21463, "FY2023": 42230, "FY2022": -90166, "FY2021": -35721, "FY2020": 30085, "FY2019": 9018, "FY2018": -2310, "FY2017": -4776, "FY2016": -111}),
    ("DATA", "Change in ECL on financial assets measured at FVOCI", {"FY2023": 15, "FY2022": -22, "FY2021": 1, "FY2020": -3, "FY2019": -11, "FY2018": -3}),
    ("DATA", "Related tax", {"FY2025": -9134, "FY2024": -5992, "FY2023": -11833, "FY2022": 25051, "FY2021": 9867, "FY2020": -8152, "FY2019": -2254, "FY2018": 577, "FY2017": 1194, "FY2016": 28}),
    ("TOTAL", "Other comprehensive income/(loss), net of tax", {"FY2025": 23500, "FY2024": 15471, "FY2023": 30412, "FY2022": -65137, "FY2021": -25853, "FY2020": 21930, "FY2019": 6753, "FY2018": -1736, "FY2017": -3582, "FY2016": -83}),
    ("TOTAL", "Total comprehensive income for the financial year", {"FY2025": 130280, "FY2024": 130708, "FY2023": 90725, "FY2022": -14824, "FY2021": 19073, "FY2020": 71881, "FY2019": 39739, "FY2018": 222849, "FY2017": 12897, "FY2016": -2255}),
]

bw.add_income_statement_sheet(
    title="The Bank of New York Mellon (International) Limited — Profit & Loss",
    subtitle="Entity-level basis, £'000s.",
    rows=income_statement_rows,
    sources_text=STATEMENTS_SOURCES + "\n\n" + PRESENTATION_NOTE,
    first_col_width=64,
    source_height=440,
    unit_suffix=" (£'000s)",
)

# ---------------------------------------------------------------
# Statement of Changes in Equity (chronological)
# ---------------------------------------------------------------
equity_changes_rows = [
    ("TOTAL", "At 1 January 2016", (249695, None, 7054, -13059, 243690)),
    ("DATA", "Loss for the financial year (FY2016)", (None, None, None, -2172, -2172)),
    ("DATA", "Change in fair value of assets classified as available-for-sale (FY2016, no separate Fair value "
             "reserve column existed this year - kept in Other reserves)", (None, None, -111, None, -111)),
    ("DATA", "Tax on other comprehensive income (FY2016)", (None, None, 28, None, 28)),
    ("TOTAL", "Total comprehensive (loss) for the year (FY2016)", (None, None, -83, -2172, -2255)),
    ("DATA", "Issue of shares (FY2016)", (270000, None, None, None, 270000)),
    ("DATA", "Amortisation of share based payments (FY2016)", (None, None, 235, None, 235)),
    ("TOTAL", "At 31 December 2016 (as originally reported, single combined reserves column)", (519695, None, 7206, -15231, 511670)),
    ("DATA", "Profit for the financial year (FY2017)", (None, None, None, 16479, 16479)),
    ("DATA", "Change in fair value of assets classified as available-for-sale (FY2017, as originally reported - no "
             "separate Fair value reserve column existed in FY2017's own statement)", (None, None, -4776, None, -4776)),
    ("DATA", "Tax on other comprehensive income (FY2017)", (None, None, 1194, None, 1194)),
    ("TOTAL", "Total comprehensive income for the year (FY2017)", (None, None, -3582, 16479, 12897)),
    ("DATA", "Amortisation of share based payments (FY2017)", (None, None, 21, None, 21)),
    ("TOTAL", "At 31 December 2017 (as originally reported, single combined reserves column)", (519695, None, 3645, 1248, 524588)),
    ("DATA", "Reclassification: split of the combined 'Other reserves' column into a separate Fair value reserve "
             "component (first shown in the FY2018 Annual Report's own restated FY2017 comparative - see "
             "Balance Sheet sheet's presentation note)", (None, -3665, 3665, None, 0)),
    ("TOTAL", "At 1 January 2018 (restated onto the post-FY2018 5-column split basis; IFRS 9 transition had a "
              "confirmed NIL impact on opening equity)", (519695, -3665, 7310, 1248, 524588)),
    ("DATA", "Profit for the financial year (FY2018)", (None, None, None, 224585, 224585)),
    ("DATA", "Change in fair value of financial assets measured at FVOCI (FY2018)", (None, -2310, None, None, -2310)),
    ("DATA", "ECL on financial assets measured at FVOCI (FY2018)", (None, -3, None, None, -3)),
    ("DATA", "Tax on other comprehensive income (FY2018)", (None, 577, None, None, 577)),
    ("TOTAL", "Total comprehensive income for the year (FY2018)", (None, -1736, None, 224585, 222849)),
    ("DATA", "Amortisation of share based payments (FY2018)", (None, None, 42, None, 42)),
    ("TOTAL", "At 31 December 2018", (519695, -5401, 7352, 225833, 747479)),
    ("DATA", "Profit for the financial year (FY2019)", (None, None, None, 32986, 32986)),
    ("DATA", "Change in fair value of financial assets measured at FVOCI (FY2019)", (None, 9018, None, None, 9018)),
    ("DATA", "ECL on financial assets measured at FVOCI (FY2019)", (None, -11, None, None, -11)),
    ("DATA", "Tax on other comprehensive income (FY2019)", (None, -2254, None, None, -2254)),
    ("TOTAL", "Total comprehensive income for the year (FY2019)", (None, 6753, None, 32986, 39739)),
    ("DATA", "Amortisation of share based payments (FY2019)", (None, None, 7, None, 7)),
    ("TOTAL", "At 31 December 2019", (519695, 1352, 7359, 258820, 787226)),
    ("DATA", "Profit for the financial year (FY2020)", (None, None, None, 49951, 49951)),
    ("DATA", "Change in fair value of financial assets measured at FVOCI (FY2020)", (None, 30085, None, None, 30085)),
    ("DATA", "ECL on financial assets measured at FVOCI (FY2020)", (None, -3, None, None, -3)),
    ("DATA", "Tax on other comprehensive income (FY2020)", (None, -8152, None, None, -8152)),
    ("TOTAL", "Total comprehensive income for the year (FY2020)", (None, 21930, None, 49951, 71881)),
    ("DATA", "Reclassification adjustment (FY2020)", (None, 83, -83, None, 0)),
    ("TOTAL", "At 1 January 2021", (519695, 23365, 7276, 308771, 859107)),
    ("DATA", "Movement in financial assets measured at FVOCI (FY2021)", (None, -35721, None, None, -35721)),
    ("DATA", "Change in ECL on financial assets measured at FVOCI (FY2021)", (None, 1, None, None, 1)),
    ("DATA", "Tax on other comprehensive income (FY2021)", (None, 9867, None, None, 9867)),
    ("DATA", "Profit for the financial year (FY2021)", (None, None, None, 44926, 44926)),
    ("TOTAL", "Total comprehensive income for the year (FY2021)", (None, -25853, None, 44926, 19073)),
    ("DATA", "Transfer between reserve accounts (FY2021)", (None, None, -126, 126, 0)),
    ("TOTAL", "At 31 December 2021", (519695, -2488, 7150, 353823, 878180)),
    ("DATA", "Profit for the financial year (FY2022)", (None, None, None, 50313, 50313)),
    ("DATA", "Movement in financial assets measured at FVOCI (FY2022)", (None, -90166, None, None, -90166)),
    ("DATA", "Change in ECL on financial assets measured at FVOCI (FY2022)", (None, -22, None, None, -22)),
    ("DATA", "Tax on other comprehensive income (FY2022)", (None, 25051, None, None, 25051)),
    ("TOTAL", "Total comprehensive income for the year (FY2022)", (None, -65137, None, 50313, -14824)),
    ("DATA", "Transfer between reserve accounts (FY2022)", (None, None, -11, 11, 0)),
    ("TOTAL", "At 31 December 2022", (519695, -67625, 7139, 404147, 863356)),
    ("DATA", "Profit for the financial year (FY2023)", (None, None, None, 60313, 60313)),
    ("DATA", "Movement in financial assets measured at FVOCI (FY2023)", (None, 42230, None, None, 42230)),
    ("DATA", "Change in ECL on financial assets measured at FVOCI (FY2023)", (None, 15, None, None, 15)),
    ("DATA", "Tax on other comprehensive income (FY2023)", (None, -11833, None, None, -11833)),
    ("TOTAL", "Total comprehensive income for the year (FY2023)", (None, 30412, None, 60313, 90725)),
    ("DATA", "Dividend in specie (FY2023)", (None, None, None, -28, -28)),
    ("TOTAL", "At 31 December 2023", (519695, -37213, 7139, 464432, 954053)),
    ("DATA", "Profit for the financial year (FY2024)", (None, None, None, 115237, 115237)),
    ("DATA", "Net movement in financial instruments measured at FVOCI (FY2024)", (None, 21463, None, None, 21463)),
    ("DATA", "Tax on other comprehensive income (FY2024)", (None, -5992, None, None, -5992)),
    ("TOTAL", "Total comprehensive income for the year (FY2024)", (None, 15471, None, 115237, 130708)),
    ("TOTAL", "At 31 December 2024", (519695, -21742, 7139, 579669, 1084761)),
    ("DATA", "Profit for the financial year (FY2025)", (None, None, None, 106780, 106780)),
    ("DATA", "Net movement in financial instruments measured at FVOCI (FY2025)", (None, 32634, None, None, 32634)),
    ("DATA", "Tax on other comprehensive income (FY2025)", (None, -9134, None, None, -9134)),
    ("TOTAL", "Total comprehensive income for the year (FY2025)", (None, 23500, None, 106780, 130280)),
    ("TOTAL", "At 31 December 2025", (519695, 1758, 7139, 686449, 1215041)),
]

bw.add_equity_changes_sheet(
    title="The Bank of New York Mellon (International) Limited — Statement of Changes in Equity",
    subtitle="Entity-level basis, £'000s. Chronological roll-forward, oldest to newest. No FX conversion (GBP functional currency throughout).",
    headers=["Called up share capital", "Fair value reserve", "Other reserves", "Profit and loss account", "Total equity"],
    rows=equity_changes_rows,
    sources_text=STATEMENTS_SOURCES + "\n\n" + PRESENTATION_NOTE,
    first_col_width=54,
    source_height=440,
)

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement (exemption note in place of line items)
# ---------------------------------------------------------------
rows = [
    ("SECTION", "No Statement of Cash Flows is published by this entity in any year", {}),
    ("DATA", "See the note below for the FRS 101 exemption this entity relies on every year, and why this "
             "workbook is built as a Pillar-3-only variant.", {}),
]

bw.add_cash_flow_sheet(
    title="The Bank of New York Mellon (International) Limited — Cash Flow Statement",
    subtitle="Not applicable — this entity takes the FRS 101 cash-flow-statement disclosure exemption every year. See source note below.",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=90,
    source_height=260,
    unit_suffix="",
)

# ---------------------------------------------------------------
# Asset Quality: this entity is a liability-driven custody bank, not a
# lender - "Loans and advances to customers" is a small, incidental line
# (£28m-£196m across the 5 years) next to a balance sheet dominated by
# central-bank cash, interbank placements and investment securities. The
# Company's own "Credit quality analysis" note covers ALL financial assets
# subject to IFRS 9 ECL (cash, loans to banks, loans to customers,
# investment securities) by internal credit grade and IFRS 9 stage - used
# here in full (mirroring the richer-than-customer-loans-alone treatment
# used for other placement-heavy banks in this project, e.g. Bank Sepah
# International in ST-013) rather than the narrower customer-loan book
# alone. Every year shown has 100% of exposure in Stage 1 (12-month ECL) -
# confirmed directly ("None of the loans and advances were past due or had
# a material ECL at the current or prior year-end", FY2025 statements) -
# no Stage 2/3 exposures in any of the 5 years.
# ---------------------------------------------------------------
AQ_GROSS = {"FY2025": 7702726, "FY2024": 7747362, "FY2023": 8607292, "FY2022": 11419812, "FY2021": 10991019}
AQ_ALLOWANCE = {"FY2025": -31, "FY2024": -34, "FY2023": -118, "FY2022": -183, "FY2021": -59}
AQ_NET = {y: AQ_GROSS[y] + AQ_ALLOWANCE[y] for y in AQ_GROSS}
AQ_STAGE3_RATIO = {y: "0.00%" for y in AQ_GROSS}
AQ_COVERAGE = {y: f"{-AQ_ALLOWANCE[y] / AQ_GROSS[y] * 100:.4f}%" for y in AQ_GROSS}

asset_quality_rows = [
    ("SECTION", "Gross exposure by IFRS 9 stage, across all ECL-bearing financial assets "
                "(cash at central banks, loans to banks, loans to customers, investment securities)", {}),
    ("DATA", "Stage 1 (12-month ECL) - gross exposure", AQ_GROSS),
    ("DATA", "Stage 2 (lifetime ECL, not credit-impaired) - gross exposure", {y: 0 for y in AQ_GROSS}),
    ("DATA", "Stage 3 (lifetime ECL, credit-impaired) - gross exposure", {y: 0 for y in AQ_GROSS}),
    ("TOTAL", "Total gross exposure", AQ_GROSS),
    ("SECTION", "Expected credit loss (ECL) allowance", {}),
    ("DATA", "Loss allowance (all Stage 1; includes the FVOCI investment-securities ECL memo item)", AQ_ALLOWANCE),
    ("TOTAL", "Net carrying amount", AQ_NET),
    ("SECTION", "Ratios", {}),
    ("DATA", "Stage 3 exposure ratio (Stage 3 / total gross exposure)", AQ_STAGE3_RATIO),
    ("DATA", "Overall coverage ratio (loss allowance / total gross exposure)", AQ_COVERAGE),
]

bw.add_asset_quality_sheet(
    title="The Bank of New York Mellon (International) Limited — Asset Quality / Credit Risk Disclosures",
    subtitle="Credit quality analysis across all ECL-bearing financial assets, £'000s. Entity-level basis.",
    rows=asset_quality_rows,
    sources_text=(
        "Sources - the Company's own 'Credit quality analysis' note (Financial risk management, Note 2.1):\n"
        f"FY2025/FY2024: Financial Statements, year ended 31 December 2025, p.40 - {FS2025_URL}\n"
        f"FY2023/FY2022: Financial Statements, year ended 31 December 2023, p.54 - {FS2023_URL}\n"
        f"FY2021: Financial Statements, year ended 31 December 2021, p.50 (Companies House, scanned/image-only, "
        f"visually transcribed) - {FS2021_URL}\n\n"
        "Note: 100% of exposure sits in Stage 1 (12-month ECL) every year shown - no Stage 2 or Stage 3 exposures "
        "at all in any of these 5 years, and the entity's own note states none of the loans and advances were past "
        "due or had a material ECL at the current or prior year-end. This is a structural feature of a "
        "liability-driven custody bank (counterparties are almost entirely investment-grade banks/central banks/"
        "sovereign and supranational securities), not a data gap.\n\n"
        "HD-025 (FY2016-FY2020 extension) SELF-SKIP: this sheet was NOT extended back to FY2016 - the pre-IFRS 9 "
        "(FY2016-FY2017) statements have no ECL/staging concept at all (an incurred-loss model, with no equivalent "
        "'past due but not impaired' note located within this ticket's time budget across 2 scanned, non-text-layer "
        "annual reports), and locating the equivalent 'Credit quality analysis' note's exact page for FY2018-FY2020 "
        "would have required page-by-page image review of 3 more scanned reports (71-295 pages each, no text "
        "layer, no note-page index available) for a bank whose loan book is a small, incidental balance-sheet line "
        "next to cash/interbank placements/investment securities - judged uneconomical relative to this ticket's "
        "core deliverable (statutory statements + Pillar 3 + RWA Breakdown, all fully extended to FY2016). All "
        "other sheets in this workbook are extended to FY2016; this one remains FY2021-FY2025 only, a genuine, "
        "documented self-skip rather than a silent gap.\n\n" + ENTITY_NOTE
    ),
    first_col_width=76,
    source_height=340,
    unit_suffix=" (£'000s)",
)

# ---------------------------------------------------------------
# RWA Breakdown (UK OV1 / EU OV1 template)
# ---------------------------------------------------------------
RWA_SOURCES = (
    "Sources - The Bank of New York Mellon (International) Limited Pillar 3 Disclosures, Table 4 'UK OV1 - "
    "Overview of risk-weighted exposure amounts' (Table 7 'EU OV1 - Overview of RWAs' for FY2021, the older CRR "
    "template) - each year's own report, not a later restated comparative (see the CET1 Ratio sheet's note on the "
    "FY2025 report's restated FY2024 comparative):\n"
    f"FY2025: Pillar 3 Disclosure, December 31, 2025, p.10 - {P3_2025_URL}\n"
    f"FY2024: Pillar 3 Disclosure, December 31, 2024, p.10 - {P3_2024_URL}\n"
    f"FY2023: Pillar 3 Disclosure, December 31, 2023, p.11 - {P3_2023_URL}\n"
    f"FY2022: Pillar 3 Disclosure, December 31, 2022, p.14 - {P3_2022_URL}\n"
    f"FY2021: Pillar 3 Disclosure, December 31, 2021, p.25 - {P3_2021_URL}\n"
    f"FY2020: Pillar 3 Disclosure 2020, Table 7 'EU OV1 - Overview of RWAs', p.13 - {P3_2020_URL}\n"
    f"FY2019: Pillar 3 Disclosure 2019, Table 8 'EU OV1 - Overview of RWAs', p.14 - {P3_2019_URL}\n"
    f"FY2018: Pillar 3 Disclosure 2018, Table 8 'EU OV1 - Overview of RWAs', p.13 - {P3_2018_URL}\n"
    f"FY2017: Pillar 3 Disclosure 2017, 'Risk Exposure Amount by Risk Type' chart, p.10 (no OV1-format table "
    f"published that year - the chart's own figures tie exactly to the FY2018 report's restated FY2017 OV1 "
    f"comparative) - {P3_2017_URL}\n"
    f"FY2016: Pillar 3 Disclosure 2016, Table 6 'Capital requirements', p.20 (pre-OV1-template era; shows "
    f"consolidated Risk Exposure Amount by risk type directly, not a capital-requirement figure needing "
    f"conversion - Credit risk SA 383 + Counterparty Credit Risk SA 4 + Market risk SA 43 + Operational risk 359 "
    f"+ Credit Valuation Adjustment 4 = Total 793, tying exactly to that year's Consolidated Total RWA from "
    f"Table 1 'Capital ratios'; CCR and CVA combined into the 'Counterparty credit risk' row, same treatment as "
    f"FY2021 above) - {P3_2016_URL}\n\n"
    "Note: FY2021's own report uses the older EU OV1 template, which separately discloses Credit Valuation "
    "Adjustment (CVA) as its own risk type; combined here into the 'Counterparty credit risk' row (£2m CCR + £2m "
    "CVA = £4m) to match the UK OV1 template's grouping used FY2022 onward - the combined figure ties to that "
    "year's own Total RWA (£838m). FY2021's securitisation exposure is a genuine disclosed zero ('the Company's "
    "securitisation portfolio was immaterial'), not a gap.\n\n"
    "HD-025 (FY2016-FY2020 extension) NOTE: the FY2017-FY2020 EU OV1 tables are published on a CONSOLIDATED basis "
    "only (no separate Solo-basis RWA-by-type breakdown exists in any of these 4 reports) - their totals therefore "
    "tie to the Consolidated Total RWA column on the CET1/Tier1/Total Capital Ratio sheets, not the Solo-basis "
    "Total RWAs figure used elsewhere in this workbook (a small, documented gap each year: FY2017 936 vs Solo 881; "
    "FY2018 1,233 vs Solo 1,211; FY2019 996 vs Solo 994; FY2020 939 = Solo 939, exact tie that year only; FY2016 "
    "793 vs Solo 765). FY2016 is now included (2026-09-08 correction): the FY2016 Pillar 3 Disclosure does carry a "
    "risk-type breakdown after all - not an OV1-format table, but Table 6 'Capital requirements', which discloses "
    "the same consolidated Risk Exposure Amount (= RWA) by risk type directly (a prior review of this document "
    "had missed this table).\n\n"
    "RE-VERIFIED 2026-09-15 (RWA cross-sheet sweep - do not re-flag). A sweep comparing every bank's Total "
    "RWAs sheet against its own RWA Breakdown total flagged FY2016 (765 vs 793), FY2017 (881 vs 936) and "
    "FY2018 (1,211 vs 1,233). All three were re-read from the primary documents and the gap is a genuine, "
    "bank-stated basis difference, NOT the credit-risk-subtotal defect found at Redwood and Ghana "
    "International. Each of those Pillar 3 Disclosures prints BOTH totals side by side in a two-column "
    "'Consolidated | Solo' key-metrics table: FY2016 Own Funds table 'Total risk-weighted assets (RWA) 793 "
    "... 765'; FY2017 'Total risk-weighted assets (RWA) 936 793 881 765' (current and prior year for each "
    "basis); FY2018 'Total risk-weighted assets (RWA) 1,233 936 1,211 881'. The FY2018 report states the "
    "reason the breakdown exists on one basis only, in terms: 'There is no material difference in the risk "
    "profile between solo and consolidated and therefore Capital Requirements and Credit Risk Adjustments "
    "information is only shown at the consolidated level' (the FY2017 report carries the same sentence). "
    "The ratio sheets confirm which basis each sheet is on: CET1 412/765 = 53.9% (FY2016), 448/881 = 50.8% "
    "(FY2017), 618/1,211 = 51.0% (FY2018) - all matching the Solo ratios the documents print, so the Total "
    "RWAs and ratio sheets are consistently Solo while this sheet is Consolidated for FY2016-FY2019. Note "
    "'Consolidated' here is BNYMIL's OWN consolidation (the Company plus its subsidiaries - see the FY2018 "
    "report's 'Basis of consolidation' table listing the Luxembourg Branch, BNY Trust Company Limited and "
    "BNY Mellon Trust & Depositary (UK) Limited), not a parent-group figure, so no group number has been put "
    "on an entity-level sheet. Neither figure is to be changed to make the two sheets agree.\n\n" + ENTITY_NOTE
)

rwa_breakdown_rows = [
    ("SECTION", "RWA by risk category (£m)", {}),
    ("DATA", "Credit risk (excluding CCR)", {"FY2025": 435, "FY2024": 519, "FY2023": 539, "FY2022": 569, "FY2021": 466, "FY2020": 538, "FY2019": 582, "FY2018": 804, "FY2017": 504, "FY2016": 383}),
    ("DATA", "Counterparty credit risk (incl. CVA where separately disclosed)", {"FY2025": 1, "FY2024": 1, "FY2023": 0, "FY2022": 0, "FY2021": 4, "FY2020": 8, "FY2019": 6, "FY2018": 4, "FY2017": 0, "FY2016": 8}),
    ("DATA", "Securitisation exposures", {"FY2025": 7, "FY2024": 9, "FY2023": 9, "FY2022": 3, "FY2021": 0}),
    ("DATA", "Market risk (position, FX and commodities)", {"FY2025": 12, "FY2024": 12, "FY2023": 14, "FY2022": 12, "FY2021": 16, "FY2020": 10, "FY2019": 14, "FY2018": 32, "FY2017": 66, "FY2016": 43}),
    ("DATA", "Operational risk", {"FY2025": 592, "FY2024": 577, "FY2023": 489, "FY2022": 415, "FY2021": 352, "FY2020": 383, "FY2019": 394, "FY2018": 393, "FY2017": 366, "FY2016": 359}),
    ("TOTAL", "Total RWAs", {"FY2025": 1047, "FY2024": 1118, "FY2023": 1051, "FY2022": 999, "FY2021": 838, "FY2020": 939, "FY2019": 996, "FY2018": 1233, "FY2017": 936, "FY2016": 793}),
]

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, unit, rows_data, sources_text, note=note, first_col_width=52, source_height=130)


metric(
    "CET1 Capital", "£m",
    [("Common Equity Tier 1 (CET1) capital", {"FY2025": 1091, "FY2024": 955, "FY2023": 833, "FY2022": 733, "FY2021": 761, "FY2020": 745, "FY2019": 659, "FY2018": 618, "FY2017": 448, "FY2016": 412})],
    p3_sources(KM1_PAGE),
)

metric(
    "CET1 Ratio", "% of RWA",
    [("Common Equity Tier 1 (CET1) ratio", {"FY2025": "104.22%", "FY2024": "85.41%", "FY2023": "79.26%", "FY2022": "73.35%", "FY2021": "90.8%", "FY2020": "79.3%", "FY2019": "66.3%", "FY2018": "51.0%", "FY2017": "50.8%", "FY2016": "53.9%"})],
    p3_sources(KM1_PAGE),
    note="The FY2025 Pillar 3 Disclosure's FY2024 comparative column restates RWA (1,118 -> 1,091) and this ratio "
         "(85.41% -> 87.54%) versus the FY2024 report's own originally-reported figures - the FY2024 column above "
         "uses that year's own report as originally published, not the later restated comparative (consistent with "
         "this project's convention of preserving each year's own as-reported figures).",
)

metric(
    "Tier 1 Capital", "£m",
    [("Tier 1 capital", {"FY2025": 1091, "FY2024": 955, "FY2023": 833, "FY2022": 733, "FY2021": 761, "FY2020": 745, "FY2019": 659, "FY2018": 618, "FY2017": 448, "FY2016": 412})],
    p3_sources(KM1_PAGE),
    note="Tier 1 = CET1 every year (no AT1 instruments in issue in any of the 10 years).",
)

metric(
    "Tier 1 Ratio", "% of RWA",
    [("Tier 1 ratio", {"FY2025": "104.22%", "FY2024": "85.41%", "FY2023": "79.26%", "FY2022": "73.35%", "FY2021": "90.8%", "FY2020": "79.3%", "FY2019": "66.3%", "FY2018": "51.0%", "FY2017": "50.8%", "FY2016": "53.9%"})],
    p3_sources(KM1_PAGE),
)

metric(
    "Total Capital", "£m",
    [("Total capital", {"FY2025": 1091, "FY2024": 955, "FY2023": 833, "FY2022": 733, "FY2021": 761, "FY2020": 745, "FY2019": 733, "FY2018": 693, "FY2017": 523, "FY2016": 487})],
    p3_sources(KM1_PAGE),
    note="Total capital = CET1 = Tier 1 for FY2020-FY2025 (no AT1 or Tier 2 instruments in issue). FY2016-FY2019 "
         "differ: the Company held a real £74-75m Tier 2 subordinated loan from a fellow Group undertaking those "
         "4 years (see the Balance Sheet sheet's presentation note), so Total Capital genuinely exceeds CET1/Tier 1 "
         "by that amount - the loan was redeemed during FY2020.",
)

metric(
    "Total Capital Ratio", "% of RWA",
    [("Total capital ratio", {"FY2025": "104.22%", "FY2024": "85.41%", "FY2023": "79.26%", "FY2022": "73.35%", "FY2021": "90.8%", "FY2020": "79.3%", "FY2019": "73.7%", "FY2018": "57.2%", "FY2017": "59.3%", "FY2016": "63.7%"})],
    p3_sources(KM1_PAGE),
    note="See the Total Capital sheet's note on the FY2016-FY2019 Tier 2 subordinated loan, redeemed during FY2020.",
)

metric(
    "Total RWAs", "£m",
    [("Total risk-weighted exposure amount", {"FY2025": 1047, "FY2024": 1118, "FY2023": 1051, "FY2022": 999, "FY2021": 838, "FY2020": 939, "FY2019": 994, "FY2018": 1211, "FY2017": 881, "FY2016": 765})],
    p3_sources(KM1_PAGE),
    note="FY2024 shown as originally reported (1,118); the FY2025 Pillar 3 Disclosure's comparative column restates "
         "this to 1,091 - see the CET1 Ratio sheet note. FY2016-FY2020 figures are the Solo-basis RWA (the same "
         "basis used FY2021-FY2025) - see the RWA Breakdown sheet's note on the Consolidated-basis EU OV1 tables, "
         "which show a slightly different total for FY2017-FY2019.\n"
         "Re-verified 2026-09-15: every FY2016-FY2018 Pillar 3 Disclosure prints the Consolidated and Solo RWA "
         "side by side (FY2016 793 / 765; FY2017 936 / 881; FY2018 1,233 / 1,211) and this sheet takes the Solo "
         "column throughout, matching the basis of the ratio sheets (412/765 = 53.9%, 448/881 = 50.8%, "
         "618/1,211 = 51.0%, all reproducing the documents' own printed Solo ratios). The RWA Breakdown sheet's "
         "Total is the Consolidated column for FY2016-FY2019 because BNYMIL publishes the risk-type split at "
         "the consolidated level only - the reports say so explicitly. The difference between the two sheets "
         "those years is expected and must not be reconciled.",
)

bw.add_rwa_breakdown_sheet(
    title="The Bank of New York Mellon (International) Limited — RWA Breakdown",
    subtitle="£m. FY2020-FY2025 BNYMIL Solo basis (matching the Total RWAs sheet); FY2016-FY2019 BNYMIL "
             "Consolidated basis (the Company and its own subsidiaries - the only basis on which those years' "
             "reports publish a risk-type split), so this sheet's Total exceeds the Total RWAs sheet those "
             "years by design - see source note.",
    rows=rwa_breakdown_rows,
    sources_text=RWA_SOURCES,
    first_col_width=64,
    source_height=280,
    unit_suffix=" (£m)",
)

metric(
    "Leverage Ratio", "£m / %",
    [
        ("Total exposure measure excluding claims on central banks", {"FY2025": 6449, "FY2024": 6276, "FY2023": 5888, "FY2022": 7602}),
        ("Leverage ratio excluding claims on central banks (%)", {"FY2025": "16.92%", "FY2024": "15.22%", "FY2023": "14.15%", "FY2022": "9.64%"}),
        ("Leverage ratio (as reported, basis not specified) (%)", {"FY2021": "6.1%", "FY2020": "6.6%", "FY2019": "5.9%", "FY2018": "4.8%", "FY2017": "4.5%", "FY2016": "5.9%"}),
        ("Total Basel III leverage ratio exposure measure (£m, pre-2022 basis, not excluding central bank claims)", {"FY2020": 11315, "FY2019": 10703, "FY2018": 12907, "FY2017": 9975, "FY2016": 6925}),
    ],
    p3_sources(KM1_PAGE),
    note="The FY2021 Pillar 3 Disclosure's 'Key metrics' page discloses only a single Leverage ratio figure without "
         "specifying an excluding/including-central-bank-claims split (that split, and the exposure-measure £m "
         "figure, first appear in the FY2022 report's KM1 template) - shown on its own row rather than assumed "
         "comparable to the 'excluding' basis used FY2022 onward. FY2016-FY2020 (added for HD-025) are on the same "
         "pre-2022 basis as FY2021 - single ratio, no excl./incl.-central-bank-claims split - with their own total "
         "exposure measure shown on a separate row rather than conflated with the FY2022+ 'excluding central bank "
         "claims' figure. The Company is not subject to a binding leverage ratio requirement in any year shown "
         "(does not meet the LREQ firm thresholds under the PRA Rulebook).",
)

metric(
    "LCR", "£m / %",
    [
        ("Total high-quality liquid assets (HQLA), weighted value (average)", {"FY2025": 5184, "FY2024": 6021, "FY2023": 6887, "FY2022": 8876, "FY2020": 8863, "FY2019": 8018, "FY2018": 9590, "FY2017": 7509, "FY2016": 4840}),
        ("Total net cash outflows, adjusted value", {"FY2025": 1669, "FY2024": 2532, "FY2023": 3305, "FY2022": 4801, "FY2020": 5147, "FY2019": 4080, "FY2018": 4040, "FY2017": 2556, "FY2016": 1451}),
        ("Liquidity Coverage Ratio (%)", {"FY2025": "317.37%", "FY2024": "240.33%", "FY2023": "211.60%", "FY2022": "185.66%", "FY2021": "173%", "FY2020": "172%", "FY2019": "197%", "FY2018": "238%", "FY2017": "294%", "FY2016": "334%"}),
    ],
    p3_sources(KM1_PAGE),
    note="LCR is presented on a 12-month average basis (4-quarter average for FY2022, per that report's own note). "
         "FY2021's Pillar 3 report discloses only the headline ratio (173%, Solo basis) on its 'Key metrics' chart "
         "page, with no HQLA/outflow/inflow £m breakdown available that year and no FY2021 comparative shown in the "
         "FY2022 report (which explicitly states comparatives were not provided for LCR/NSFR due to a change in "
         "reporting instructions) - left blank rather than guessed. FY2016-FY2020 (added for HD-025) each carry a "
         "full HQLA/NCO/ratio breakdown from their own year's KM1 table.",
)

metric(
    "NSFR", "£m / %",
    [
        ("Total available stable funding", {"FY2025": 2561, "FY2024": 2474, "FY2023": 2386, "FY2022": 3210, "FY2020": 3158, "FY2019": 2994, "FY2018": 4533, "FY2017": 3577, "FY2016": 2314}),
        ("Total required stable funding", {"FY2025": 672, "FY2024": 675, "FY2023": 650, "FY2022": 680, "FY2020": 579, "FY2019": 606, "FY2018": 617, "FY2017": 468, "FY2016": 151}),
        ("NSFR ratio (%)", {"FY2025": "381.21%", "FY2024": "366.64%", "FY2023": "368.06%", "FY2022": "472.37%", "FY2021": "446%", "FY2020": "545%", "FY2019": "494%", "FY2018": "735%", "FY2017": "765%", "FY2016": "1534%"}),
    ],
    p3_sources(KM1_PAGE),
    note="NSFR is presented on a 4-quarter average basis. FY2021's Pillar 3 report discloses only the headline "
         "ratio (446%, Solo basis) with no £m breakdown, and no FY2021 comparative appears in the FY2022 report "
         "(same reporting-instruction change noted on the LCR sheet). The FY2025 Pillar 3 Disclosure's FY2024 "
         "comparative column also restates NSFR (ASF 2,474->2,481, RSF 675->664, ratio 366.64%->373.99%) versus "
         "the FY2024 report's own originally-reported figures - the FY2024 column above uses that year's own report "
         "as originally published, consistent with this project's convention. FY2016-FY2020 (added for HD-025) each "
         "carry a full ASF/RSF/ratio breakdown from their own year's KM1 table - the very high FY2016 ratio "
         "(1,534%) is a genuine feature of the entity's small, low-loan/high-deposit balance sheet that year, not "
         "a transcription error.",
)

metric(
    "MREL Ratio", "£m / %",
    [("MREL ratio", {y: "Not publicly disclosed" for y in YEARS})],
    p3_sources(KM1_PAGE),
    note="No MREL figure (numeric or qualitative) appears anywhere in any of the 10 Pillar 3 Disclosures or the "
         "available Financial Statements for this entity - no reason is stated.",
)

# ---------------------------------------------------------------
# Overview sheet (Pillar-3-only: no cash-flow chart)
# ---------------------------------------------------------------
bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {"FY2025": 7918773, "FY2024": 8007771, "FY2023": 8896652, "FY2022": 11702044, "FY2021": 11227068, "FY2020": 10315540, "FY2019": 9761980, "FY2018": 12388368, "FY2017": 10117220, "FY2016": 6908403}),
        ("Loans and advances to customers", {"FY2025": 28495, "FY2024": 173578, "FY2023": 108153, "FY2022": 138345, "FY2021": 104419, "FY2020": 195590, "FY2019": 117788, "FY2018": 275544, "FY2017": 152291, "FY2016": 112638}),
        ("Customer accounts", {"FY2025": 4303354, "FY2024": 4316535, "FY2023": 4583519, "FY2022": 6631188, "FY2021": 7137353, "FY2020": 7004361, "FY2019": 7265408, "FY2018": 9685207, "FY2017": 7459508, "FY2016": 4656755}),
        ("Shareholder's funds", {"FY2025": 1215041, "FY2024": 1084761, "FY2023": 954053, "FY2022": 863356, "FY2021": 878180, "FY2020": 859107, "FY2019": 787226, "FY2018": 747479, "FY2017": 524588, "FY2016": 511670}),
    ],
    balance_sheet_unit="£'000s",
    income_statement_totals=[
        ("Non-interest income", {"FY2025": 153651, "FY2024": 153320, "FY2023": 149827, "FY2022": 147434, "FY2021": 152238, "FY2020": 140461, "FY2019": 136448, "FY2018": 178081, "FY2017": 161317, "FY2016": 162885}),
        ("Total operating expenses", {"FY2025": -141091, "FY2024": -156473, "FY2023": -168041, "FY2022": -171514, "FY2021": -155452, "FY2020": -143551, "FY2019": -145271, "FY2018": -176615, "FY2017": -149584, "FY2016": -164107}),
        ("Total profit for the financial year", {"FY2025": 106780, "FY2024": 115237, "FY2023": 60313, "FY2022": 50313, "FY2021": 44926, "FY2020": 49951, "FY2019": 32986, "FY2018": 224585, "FY2017": 16479, "FY2016": -2172}),
    ],
    income_statement_unit="£'000s",
    equity_changes_totals=[
        ("Opening equity", {"FY2025": 1084761, "FY2024": 954053, "FY2023": 863356, "FY2022": 878180, "FY2021": 859107, "FY2020": 787226, "FY2019": 747479, "FY2018": 524588, "FY2017": 511670, "FY2016": 243690}),
        ("Total comprehensive income/(loss) for the year", {"FY2025": 130280, "FY2024": 130708, "FY2023": 90725, "FY2022": -14824, "FY2021": 19073, "FY2020": 71881, "FY2019": 39739, "FY2018": 222849, "FY2017": 12897, "FY2016": -2255}),
        ("Other movements, net", {"FY2025": 0, "FY2024": 0, "FY2023": -28, "FY2022": 0, "FY2021": 0, "FY2020": 0, "FY2019": 7, "FY2018": 42, "FY2017": 21, "FY2016": 270235}),
        ("Closing equity", {"FY2025": 1215041, "FY2024": 1084761, "FY2023": 954053, "FY2022": 863356, "FY2021": 878180, "FY2020": 859107, "FY2019": 787226, "FY2018": 747479, "FY2017": 524588, "FY2016": 511670}),
    ],
    equity_changes_unit="£'000s",
    cash_flow_totals=[],
    cash_flow_unit=None,
    ratios=[
        ("CET1 Ratio", {"FY2025": "104.22%", "FY2024": "85.41%", "FY2023": "79.26%", "FY2022": "73.35%", "FY2021": "90.8%", "FY2020": "79.3%", "FY2019": "66.3%", "FY2018": "51.0%", "FY2017": "50.8%", "FY2016": "53.9%"}),
        ("Tier 1 Ratio", {"FY2025": "104.22%", "FY2024": "85.41%", "FY2023": "79.26%", "FY2022": "73.35%", "FY2021": "90.8%", "FY2020": "79.3%", "FY2019": "66.3%", "FY2018": "51.0%", "FY2017": "50.8%", "FY2016": "53.9%"}),
        ("Total Capital Ratio", {"FY2025": "104.22%", "FY2024": "85.41%", "FY2023": "79.26%", "FY2022": "73.35%", "FY2021": "90.8%", "FY2020": "79.3%", "FY2019": "73.7%", "FY2018": "57.2%", "FY2017": "59.3%", "FY2016": "63.7%"}),
        ("Leverage Ratio (excl. central bank claims)", {"FY2025": "16.92%", "FY2024": "15.22%", "FY2023": "14.15%", "FY2022": "9.64%"}),
        ("LCR", {"FY2025": "317.37%", "FY2024": "240.33%", "FY2023": "211.60%", "FY2022": "185.66%", "FY2021": "173%", "FY2020": "172%", "FY2019": "197%", "FY2018": "238%", "FY2017": "294%", "FY2016": "334%"}),
        ("NSFR", {"FY2025": "381.21%", "FY2024": "366.64%", "FY2023": "368.06%", "FY2022": "472.37%", "FY2021": "446%", "FY2020": "545%", "FY2019": "494%", "FY2018": "735%", "FY2017": "765%", "FY2016": "1534%"}),
    ],
    note="No cash flow summary or chart is shown here: The Bank of New York Mellon (International) Limited takes "
         "the FRS 101 cash-flow-statement exemption every year (see the Cash Flow Statement sheet). Balance Sheet, "
         "Profit & Loss, Statement of Changes in Equity and Pillar 3 Key Metrics are all fully populated below. See "
         "each sheet's own source citation for the underlying document/page.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/BNY MELLON INTERNATIONAL FINANCIALS.xlsx")
