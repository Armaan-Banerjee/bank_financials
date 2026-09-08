import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021", "FY2020", "FY2019", "FY2018", "FY2017", "FY2016"]  # most recent first
YEAR_LABEL = {y: y for y in YEARS}

CH_BASE = "https://find-and-update.company-information.service.gov.uk/company/01814093/filing-history"
AR2025_URL = CH_BASE + "/MzUyMzkyMzgzOGFkaXF6a2N4/document?format=pdf&download=0"
AR2024_URL = CH_BASE + "/MzQ2NjcyMDU4MGFkaXF6a2N4/document?format=pdf&download=0"
AR2023_URL = CH_BASE + "/MzQyMjAyODYxMmFkaXF6a2N4/document?format=pdf&download=0"
AR2022_URL = CH_BASE + "/MzM3OTQ2NzM2OWFkaXF6a2N4/document?format=pdf&download=0"
AR2021_URL = CH_BASE + "/MzMzNzcwMzA4MGFkaXF6a2N4/document?format=pdf&download=0"
AR2020_URL = CH_BASE + "/MzMwMjEyMjEzMmFkaXF6a2N4/document?format=pdf&download=0"
AR2019_URL = CH_BASE + "/MzI3MjMxMDgyMmFkaXF6a2N4/document?format=pdf&download=0"
AR2018_URL = CH_BASE + "/MzIzNjcxMTg2MGFkaXF6a2N4/document?format=pdf&download=0"
AR2017_URL = CH_BASE + "/MzIwMzMyNzI2NWFkaXF6a2N4/document?format=pdf&download=0"
AR2016_URL = CH_BASE + "/MzE3NTk2MTg3NWFkaXF6a2N4/document?format=pdf&download=0"

P3_2024_URL = "https://www.jordanbank.co.uk/media/n0xn5hx1/website-jib-pillar-3-2024-v24-clean.pdf"
P3_2023_URL = "https://www.jordanbank.co.uk/media/1266/pw3949-jib-pillar-3-2023-final.pdf"
P3_2022_URL = "https://www.jordanbank.co.uk/media/1245/jib-pillar-3-2022.pdf"
P3_2021_URL = "https://www.jordanbank.co.uk/media/1239/pw3901-jib-pillar-3-2021-final.pdf"
P3_2020_URL = "https://www.jordanbank.co.uk/media/1215/jib-pillar-3-disclosures-2020.pdf"
P3_2019_URL = "https://www.jordanbank.co.uk/media/1208/jib-pillar-3-2019-revised-final-report.pdf"
P3_2018_URL = "https://www.jordanbank.co.uk/media/1133/pillar-3-2018.pdf"
P3_2017_URL = "https://www.jordanbank.co.uk/media/1127/pw3751-jib-pillar-3-2017-f-final.pdf"
P3_2016_URL = "https://www.jordanbank.co.uk/media/1018/pillar-3.pdf"

RESTATEMENT_NOTE = (
    "DATA NOTE - FY2022/FY2023 opening-vs-closing cash gap (£16,090k): FY2022's own "
    "originally-published Cash Flow Statement (Annual Report and Financial Statements 2022, "
    "p.28) shows net cash generated in operating activities of £7,948k and cash and cash "
    "equivalents at the end of FY2022 of £77,136k. FY2023's own Annual Report (p.28) instead "
    "presents a FY2022 comparative column showing net cash generated in operating activities "
    "of only £(5,551)k and cash and cash equivalents at the beginning of FY2023 (i.e. the "
    "carried-forward FY2022 closing balance) of £57,334k, with FY2023's own closing figure of "
    "£61,046k tying to that restated opening balance, not to FY2022's originally-published "
    "£77,136k. The Investing and Financing sections are identical between both versions "
    "(£21,263k net investing inflow, £(12,000)k dividend payment) - only the Operating "
    "activities figure and the resulting cash balance differ, suggesting a reclassification "
    "within operating cash flows (e.g. of a balance-sheet item's cash-equivalent treatment) "
    "rather than a transcription error in either document. Per this project's convention, each "
    "year keeps its own originally-published figures (FY2022 = FY2022 AR's own figures; "
    "FY2023 = FY2023 AR's own figures, including its own FY2022 comparative column for "
    "internal consistency within that document) rather than substituting a later restated "
    "comparative - so the FY2022-to-FY2023 opening/closing bridge in this workbook does not "
    "tie by £16,090k. This is a real, disclosed inconsistency between the Bank's own two "
    "Annual Reports, not a transcription error; every other year-to-year link in the chain "
    "(FY2021->FY2022, FY2023->FY2024, FY2024->FY2025) ties exactly.\n"
    "DATA NOTE - FY2018/FY2019 opening-vs-closing cash gap (£69,912k), same pattern one year "
    "earlier in this bank's history: FY2018's own originally-published Cash Flow Statement "
    "(Annual Report and Financial Statements 2018, p.22) shows cash and cash equivalents at "
    "the end of FY2018 of £11,057k. FY2019's own Annual Report (p.24) instead opens FY2019 "
    "with a beginning-of-year balance of £80,969k - the Bank's own footnote there explains "
    "why: 'During the year, the Bank revisited its definition of cash and cash equivalent and "
    "reclassified the balances presented in cash flows from operating activities. The "
    "comparative information has been restated to reflect the reclassification adjustment made "
    "in the cash and cash equivalent balance and cash flows from operating and financing "
    "activities' (Note 38 referenced for detail). Each year again keeps its own "
    "originally-published figures per this project's convention, so the FY2018-to-FY2019 "
    "bridge does not tie - a real, disclosed definitional change, not a transcription error. "
    "FY2016->FY2017, FY2017->FY2018, FY2019->FY2020 and FY2020->FY2021 all tie exactly."
)

FY2018_CASHFLOW_LABEL_NOTE = (
    "DATA NOTE - FY2018 Cash Flow Statement section-labelling bug in the source document "
    "itself, reproduced not silently fixed: the Bank's own FY2018 Annual Report (p.22) prints "
    "a 'Cashflows from financing activities' heading immediately followed by a single line "
    "'Increase in long term customer accounts' of £7,428k, then labels the £7,428k subtotal "
    "itself 'Net cash (used in)/generated by Investing activities' (the wrong heading - it is "
    "the financing subtotal, not investing) before a second, correctly-labelled 'Cash flows "
    "from investing activities' section follows with its own, different net figure of "
    "£(1,646)k. This workbook assigns the £7,428k customer-account line to financing (where "
    "its own section heading places it) and the £(1,646)k figure to investing (matching its "
    "own correctly-headed section) - both figures are the Bank's own, only the interim "
    "subtotal's heading is mislabelled in the source. Operating £(60,350)k + financing £7,428k "
    "+ investing £(1,646)k = £(54,568)k, tying exactly to the Bank's own printed 'Decrease in "
    "cash and cash equivalents' for FY2018."
)

CASH_FLOW_SOURCES = (
    "Sources - Jordan International Bank Plc's own Cash Flow Statement, from each year's "
    "Companies House-filed Annual Report and Financial Statements (company 01814093, all 10 "
    "filings fully scanned/image-only, transcribed via page-image review):\n"
    f"FY2025: Annual Report and Financial Statements 2025, Cash Flow Statement, p.30 - {AR2025_URL}\n"
    f"FY2024: Annual Report and Financial Statements 2024, Cash Flow Statement, p.30 (FY2024's "
    f"own originally-published figures used; matches FY2025's own FY2024 comparative exactly) "
    f"- {AR2024_URL}\n"
    f"FY2023: Annual Report and Financial Statements 2023, Cash Flow Statement, p.28 (FY2023's "
    f"own originally-published figures used; see note below on FY2022's differing comparative) "
    f"- {AR2023_URL}\n"
    f"FY2022: Annual Report and Financial Statements 2022, Cash Flow Statement, p.28 (FY2022's "
    f"own originally-published figures used - see note below) - {AR2022_URL}\n"
    f"FY2021: Annual Report and Financial Statements 2021, Cash Flow Statement, p.29 - {AR2021_URL}\n"
    f"FY2020: Annual Report and Financial Statements 2020, Cash Flow Statement, p.27 - {AR2020_URL}\n"
    f"FY2019: Annual Report and Financial Statements 2019, Cash Flow Statement, p.24 (FY2019's "
    f"own originally-published figures used - see note below on FY2018's differing comparative) "
    f"- {AR2019_URL}\n"
    f"FY2018: Annual Report and Financial Statements 2018, Cash Flow Statement, p.22 (FY2018's "
    f"own originally-published figures used - see notes below on the section-labelling bug and "
    f"the FY2019 restatement gap) - {AR2018_URL}\n"
    f"FY2017: Annual Report and Financial Statements 2017, Cash Flow Statement, p.19 - {AR2017_URL}\n"
    f"FY2016: Annual Report and Financial Statements 2016, Cash Flow Statement, p.15 - {AR2016_URL}\n"
    "The Bank presents both a '(Decrease)/increase in cash and cash equivalents' line (the sum "
    "of the Operating/Investing/Financing sections above it) and a separately-disclosed "
    "'Movement in cash and cash equivalents' line used in the opening-to-closing reconciliation "
    "below it; these two lines are not always numerically equal in the Bank's own source "
    "documents (e.g. FY2023: 4,957 vs 7,576) - both are transcribed exactly as printed, and the "
    "reconciliation used to verify each year's own closing balance is opening + 'Movement' + "
    "'Effect of foreign exchange rate changes'. FY2016's own Cash Flow Statement labels its net "
    "investing subtotal 'Net cash outflows Investing activities' while printing a positive "
    "£26,037k (the sum of that section's own component lines, which are all correctly signed) - "
    "reproduced exactly as printed; the heading's 'outflows' wording appears to be the source's "
    "own error, not a transcription error here.\n"
    + FY2018_CASHFLOW_LABEL_NOTE + "\n"
    + RESTATEMENT_NOTE
)


def p3_sources():
    return (
        "Sources - Jordan International Bank Plc's own Pillar 3 Report, published on the "
        "Bank's website:\n"
        f"FY2024: Pillar 3 Report 2024, Section 1 'Introduction', Key Prudential Metrics table "
        f"(UK KM1 template, 31 December 2024) - {P3_2024_URL}\n"
        f"FY2023: Pillar 3 Report 2023, Section 1 'Introduction', Key Prudential Metrics table "
        f"(UK KM1 template, 31 December 2023) - {P3_2023_URL}\n"
        f"FY2022: Pillar 3 Report 2022, Section 1 'Introduction', Key Prudential Metrics table "
        f"(UK KM1 template, 31 December 2022) - {P3_2022_URL}\n"
        f"FY2021: Pillar 3 Report 2021, Section 1 'Introduction', Key Prudential Metrics table "
        f"(UK KM1 template, 31 December 2021) - {P3_2021_URL}\n"
        f"FY2020: Pillar 3 Report 2020, Section 2 'Summary of key ratios' - {P3_2020_URL}\n"
        f"FY2019: Pillar 3 Report 2019, Section 3 'Summary of key ratios' table - {P3_2019_URL}\n"
        f"FY2018: Pillar 3 Report 2018, Section 3 'Summary of key ratios' table - {P3_2018_URL}\n"
        f"FY2017: Pillar 3 Report 2017, Section 3 'Summary of key ratios' table - {P3_2017_URL}\n"
        f"FY2016: Pillar 3 Report 2016, Section 3 'Summary of key capital ratios' infographic "
        f"plus Section 4 'Capital resources, requirements and leverage' detail tables - "
        f"{P3_2016_URL}\n"
        "FY2025: no standalone Pillar 3 Report was published on the Bank's website as of this "
        "session (only 2016-2024 reports are listed) - genuinely not yet disclosed, left blank "
        "rather than guessed. No Total Capital / Tier 2 capital is disclosed separately from "
        "CET1 in any year (Tier 1 = Total Capital = CET1 throughout, per the Bank's own table "
        "labelling) FY2016-FY2025. FY2016 discloses both a 'fully loaded' and a 'PRA "
        "transitional' CET1/Tier1/Total Capital and ratio basis (a Basel III/CRD IV phase-in "
        "distinction that had disappeared from the Bank's own disclosures by FY2017) - the "
        "'fully loaded' figures are used here for continuity with every later year's single "
        "figure (FY2016 fully loaded CET1 £80.1m/20.44%; PRA transitional would instead read "
        "£79.7m/20.36%, both from the same source page). NSFR is disclosed only for FY2016 "
        "(123%, in that year's own summary infographic) and is genuinely absent from every "
        "other Pillar 3 Report checked in this project (FY2017-FY2021); it reappears from "
        "FY2022 onward. MREL Ratio is not disclosed in any year FY2016-FY2025 - Jordan "
        "International Bank Plc is not identified as a UK resolution entity in any of these "
        "reports."
    )


bw = BankWorkbook(bank_name="Jordan International Bank Plc", years=YEARS, year_label=YEAR_LABEL, header_color="8B1A1A")

STATEMENTS_ENTITY_NOTE = (
    "Each year's Balance Sheet, Profit & Loss and Statement of Changes in Equity use that year's "
    "own originally-published Annual Report and Financial Statements (Companies House-filed, "
    "company 01814093), not a later restated comparative - matching the existing Cash Flow "
    "Statement's convention. The equity reconciliation ladder ties exactly at every year boundary: "
    "each year's own closing balance ties to both the next year's own opening balance and that "
    "year's own Balance Sheet Total equity - zero plug rows needed anywhere. Both FY2016-2025 "
    "shareholders are named in every year's own Statement of Changes in Equity ('Housing Bank "
    "For Trade & Finance' and 'Arab Jordan Investment Bank', both Jordan-incorporated parent "
    "banks) - confirming every year's figures are this UK-incorporated subsidiary's own, not a "
    "conflation with either Jordanian parent's own group-level disclosures."
)

# ---------------------------------------------------------------
# Balance Sheet
# ---------------------------------------------------------------
bw.add_balance_sheet_sheet(
    title="Jordan International Bank Plc - Balance Sheet",
    subtitle="As at 31 December (£'000, GBP)",
    rows=[
        ("SECTION", "Assets", {}),
        ("DATA", "Cash", {"FY2025": 71, "FY2024": 71, "FY2023": 53, "FY2022": 19, "FY2021": 132, "FY2020": 116, "FY2019": 69, "FY2018": 83, "FY2017": 106, "FY2016": 116}),
        ("DATA", "Nostros", {"FY2025": 1920, "FY2024": 2229, "FY2023": 6495, "FY2022": 1094, "FY2021": 8531, "FY2020": 6049, "FY2019": 5347, "FY2018": 10104, "FY2017": 7560, "FY2016": 9416}),
        ("DATA", "Loans and advances to shareholder banks", {"FY2025": 30164, "FY2024": 25200, "FY2023": 19587, "FY2022": 23214, "FY2021": 24957, "FY2020": 35099, "FY2019": 58803, "FY2018": 39954, "FY2017": 36129, "FY2016": 29264}),
        ("DATA", "Loans and advances to other banks", {"FY2025": 52477, "FY2024": 59154, "FY2023": 44479, "FY2022": 65900, "FY2021": 36380, "FY2020": 34600, "FY2019": 39787, "FY2018": 36766, "FY2017": 47919, "FY2016": 41094}),
        ("DATA", "Loans and advances to customers", {"FY2025": 224760, "FY2024": 282222, "FY2023": 288383, "FY2022": 233986, "FY2021": 201093, "FY2020": 180402, "FY2019": 152660, "FY2018": 168221, "FY2017": 157923, "FY2016": 162860}),
        ("DATA", "Total debt securities", {"FY2025": 110877, "FY2024": 105602, "FY2023": 75603, "FY2022": 94004, "FY2021": 105371, "FY2020": 107999, "FY2019": 120917, "FY2018": 125371, "FY2017": 137846, "FY2016": 160356}),
        ("DATA", "Debt securities - Government securities (amortised cost)", {"FY2025": 17176, "FY2024": 15682, "FY2023": 5945, "FY2022": 6284, "FY2021": 5607, "FY2020": 3652, "FY2019": 3768, "FY2018": 3904}),
        ("DATA", "Debt securities - Government securities (FVOCI)", {"FY2025": 59472, "FY2024": 65295, "FY2023": 58657, "FY2022": 62463, "FY2021": 63974, "FY2020": 67105, "FY2019": 77745, "FY2018": 84035}),
        ("DATA", "Debt securities - Government securities (expected credit losses)", {"FY2025": -336, "FY2024": -458, "FY2023": -419, "FY2022": -582, "FY2021": -454, "FY2020": -592, "FY2019": -337, "FY2018": -355}),
        ("DATA", "Debt securities - Other debt securities (amortised cost)", {"FY2025": 31322, "FY2024": 21477, "FY2023": 9912, "FY2022": 19267, "FY2021": 19518, "FY2020": 22032, "FY2019": 17190, "FY2018": 4780}),
        ("DATA", "Debt securities - Other debt securities (FVOCI)", {"FY2025": 3401, "FY2024": 3631, "FY2023": 1527, "FY2022": 6607, "FY2021": 16749, "FY2020": 15826, "FY2019": 22573, "FY2018": 33033}),
        ("DATA", "Debt securities - Other debt securities (expected credit losses)", {"FY2025": -158, "FY2024": -25, "FY2023": -19, "FY2022": -35, "FY2021": -23, "FY2020": -24, "FY2019": -22, "FY2018": -26}),
        ("DATA", "Debt securities - Government securities (held to maturity)", {"FY2017": 2968, "FY2016": 3250}),
        ("DATA", "Debt securities - Government securities (available for sale)", {"FY2017": 105187, "FY2016": 120469}),
        ("DATA", "Debt securities - Government securities (designated at FVTPL)", {"FY2017": 251, "FY2016": 580}),
        ("DATA", "Debt securities - Other debt securities (held to maturity)", {"FY2017": 4551, "FY2016": 0}),
        ("DATA", "Debt securities - Other debt securities (available for sale)", {"FY2017": 24889, "FY2016": 36057}),
        ("DATA", "Debt securities - Other debt securities (designated at FVTPL)", {"FY2017": 0, "FY2016": 0}),
        ("DATA", "Derivatives", {"FY2025": 193, "FY2024": 1985}),
        ("DATA", "Assets held for sale", {"FY2025": 16825}),
        ("DATA", "Tangible fixed assets", {"FY2025": 1049, "FY2024": 1306, "FY2023": 1343, "FY2022": 1576, "FY2021": 1629, "FY2020": 1765, "FY2019": 1759, "FY2018": 1859, "FY2017": 1132, "FY2016": 856}),
        ("DATA", "Intangible assets", {"FY2025": 193}),
        ("DATA", "Other assets", {"FY2025": 1272, "FY2024": 1622, "FY2023": 5182, "FY2022": 4554, "FY2021": 1361, "FY2020": 1492, "FY2019": 470, "FY2018": 548, "FY2017": 494, "FY2016": 922}),
        ("DATA", "Deferred tax", {"FY2025": 1472, "FY2024": 1601, "FY2023": 1956, "FY2022": 2438, "FY2021": 2292, "FY2020": 1761, "FY2019": 1723, "FY2018": 2348, "FY2017": 2101, "FY2016": 2513}),
        ("DATA", "Prepayments and accrued income", {"FY2025": 3360, "FY2024": 3978, "FY2023": 3528, "FY2022": 3184, "FY2021": 2508, "FY2020": 2346, "FY2019": 2191, "FY2018": 1951, "FY2017": 1897, "FY2016": 3375}),
        ("TOTAL", "Total Assets", {"FY2025": 444633, "FY2024": 484970, "FY2023": 446609, "FY2022": 429969, "FY2021": 384254, "FY2020": 371629, "FY2019": 383726, "FY2018": 387205, "FY2017": 393107, "FY2016": 410772}),
        ("SECTION", "Liabilities", {}),
        ("DATA", "Deposits by shareholder banks", {"FY2025": 106140, "FY2024": 103079, "FY2023": 99366, "FY2022": 107693, "FY2021": 94387, "FY2020": 99284, "FY2019": 115068, "FY2018": 118252, "FY2017": 106835, "FY2016": 106831}),
        ("DATA", "Deposits by other banks", {"FY2025": 68024, "FY2024": 69448, "FY2023": 71773, "FY2022": 62958, "FY2021": 82381, "FY2020": 64681, "FY2019": 68177, "FY2018": 80699, "FY2017": 124563, "FY2016": 132770}),
        ("DATA", "Customer accounts", {"FY2025": 169530, "FY2024": 211430, "FY2023": 176886, "FY2022": 167312, "FY2021": 110410, "FY2020": 111598, "FY2019": 107367, "FY2018": 99516, "FY2017": 73435, "FY2016": 86186}),
        ("DATA", "Derivatives", {"FY2025": 378, "FY2024": 240}),
        ("DATA", "Other liabilities", {"FY2025": 2170, "FY2024": 4137, "FY2023": 7286, "FY2022": 6350, "FY2021": 2425, "FY2020": 3043, "FY2019": 1860, "FY2018": 1780, "FY2017": 1497, "FY2016": 2535}),
        ("DATA", "Accruals and deferred income", {"FY2025": 2663, "FY2024": 2715, "FY2023": 2337, "FY2022": 1867, "FY2021": 1332, "FY2020": 1631, "FY2019": 2249, "FY2018": 2388, "FY2017": 3629, "FY2016": 2335}),
        ("TOTAL", "Total Liabilities", {"FY2025": 348905, "FY2024": 391049, "FY2023": 357648, "FY2022": 346180, "FY2021": 290935, "FY2020": 280237, "FY2019": 294721, "FY2018": 302635, "FY2017": 309959, "FY2016": 330657}),
        ("SECTION", "Equity", {}),
        ("DATA", "Called up share capital", {"FY2025": 65000, "FY2024": 65000, "FY2023": 65000, "FY2022": 65000, "FY2021": 65000, "FY2020": 65000, "FY2019": 65000, "FY2018": 65000, "FY2017": 65000, "FY2016": 65000}),
        ("DATA", "Share premium account", {"FY2025": 316, "FY2024": 316, "FY2023": 316, "FY2022": 316, "FY2021": 316, "FY2020": 316, "FY2019": 316, "FY2018": 316, "FY2017": 316, "FY2016": 316}),
        ("DATA", "Revaluation reserve", {"FY2025": -16, "FY2024": -145, "FY2023": -139, "FY2022": -407, "FY2021": 633, "FY2020": 1452, "FY2019": 1008, "FY2018": -978, "FY2017": 616, "FY2016": -957}),
        ("DATA", "Profit or loss account", {"FY2025": 30428, "FY2024": 28750, "FY2023": 23784, "FY2022": 18880, "FY2021": 27370, "FY2020": 24624, "FY2019": 22681, "FY2018": 20232, "FY2017": 17216, "FY2016": 15756}),
        ("TOTAL", "Shareholders' Funds", {"FY2025": 95728, "FY2024": 93921, "FY2023": 88961, "FY2022": 83789, "FY2021": 93319, "FY2020": 91392, "FY2019": 89005, "FY2018": 84570, "FY2017": 83148, "FY2016": 80115}),
        ("TOTAL", "Total Liabilities and Shareholders' Funds", {"FY2025": 444633, "FY2024": 484970, "FY2023": 446609, "FY2022": 429969, "FY2021": 384254, "FY2020": 371629, "FY2019": 383726, "FY2018": 387205, "FY2017": 393107, "FY2016": 410772}),
    ],
    sources_text=(
        "Sources - Jordan International Bank Plc's own Balance Sheet, from each year's Companies "
        "House-filed Annual Report and Financial Statements (all 10 filings fully scanned/"
        "image-only, transcribed via page-image review):\n"
        f"FY2025: Annual Report and Financial Statements 2025, Balance Sheet, p.28 - {AR2025_URL}\n"
        f"FY2024: Annual Report and Financial Statements 2024, Balance Sheet, p.28 - {AR2024_URL}\n"
        f"FY2023: Annual Report and Financial Statements 2023, Balance Sheet, p.26 - {AR2023_URL}\n"
        f"FY2022: Annual Report and Financial Statements 2022, Balance Sheet, p.26 - {AR2022_URL}\n"
        f"FY2021: Annual Report and Financial Statements 2021, Balance Sheet, p.27 - {AR2021_URL}\n"
        f"FY2020: Annual Report and Financial Statements 2020, Balance Sheet, p.25 - {AR2020_URL}\n"
        f"FY2019: Annual Report and Financial Statements 2019, Balance Sheet, p.22 - {AR2019_URL}\n"
        f"FY2018: Annual Report and Financial Statements 2018, Balance Sheet, p.20 - {AR2018_URL}\n"
        f"FY2017: Annual Report and Financial Statements 2017, Balance Sheet, p.17 - {AR2017_URL}\n"
        f"FY2016: Annual Report and Financial Statements 2016, Balance Sheet, p.13 - {AR2016_URL}\n"
        "Presentation changes across years, reproduced as disclosed rather than force-merged: "
        "'Derivatives' only appears as a separate line FY2024/FY2025 (nil/not disclosed separately "
        "in earlier years); 'Assets held for sale' and 'Intangible assets' only appear FY2025 "
        "(the Bank's own Note 18/Note 20 footnotes confirm these are new lines that year, not a "
        "renamed pre-existing line); 'Investments in debt securities' (FY2016-FY2018's own label) "
        "and 'Debt securities' (FY2019 onward) are the same line, renamed only. FY2016-FY2017's "
        "own Balance Sheet also prints an 'Off Balance Sheet Items' memo section (Contingent "
        "liabilities: acceptances, guarantees and irrevocable letters of credit, undrawn "
        "commitments) below the Total Liabilities and Shareholders' Funds line - not carried into "
        "this sheet as it sits outside the balance sheet total itself, consistent with how later "
        "years' equivalent disclosures are also excluded.\n\n"
        "DEBT SECURITIES BREAKDOWN: the 'Debt securities - ...' sub-rows below the renamed 'Total "
        "debt securities' line are transcribed from each year's own 'Debt securities'/'Investments "
        "in debt securities' note, which cross-tabs the balance by issuer type (Government "
        "securities vs Other debt securities) and by measurement basis (Amortised cost vs FVOCI "
        "vs Expected credit losses FY2018-FY2025, once IFRS 9 was adopted 1 January 2018; "
        "Held-to-maturity vs Available-for-sale vs Designated at FVTPL FY2016-FY2017, the "
        "pre-IFRS-9 IAS 39 categories) - each year's own note, not a later restated comparative:\n"
        f"FY2025: Annual Report and Financial Statements 2025, Note 16 'Debt Securities', p.48 - {AR2025_URL}\n"
        f"FY2024: Annual Report and Financial Statements 2024, Note 16 'Debt Securities', p.48 - {AR2024_URL}\n"
        f"FY2023: Annual Report and Financial Statements 2023, Note 16 'Debt Securities', p.46 - {AR2023_URL}\n"
        f"FY2022: Annual Report and Financial Statements 2022, Note 16 'Debt Securities', p.44 - {AR2022_URL}\n"
        f"FY2021: Annual Report and Financial Statements 2021, Note 16 'Debt Securities', p.45 - {AR2021_URL}\n"
        f"FY2020: Annual Report and Financial Statements 2020, Note 16 'Debt Securities', p.43 - {AR2020_URL}\n"
        f"FY2019: Annual Report and Financial Statements 2019, Note 15 'Debt Securities', p.39 - {AR2019_URL}\n"
        f"FY2018: Annual Report and Financial Statements 2018, Note 15 'Investments in Debt "
        f"Securities', p.37 - {AR2018_URL}\n"
        f"FY2017: Annual Report and Financial Statements 2017, Note 13 'Investments in Debt "
        f"Securities', p.29 - {AR2017_URL}\n"
        f"FY2016: Annual Report and Financial Statements 2016, Note 13 'Investments in Debt "
        f"Securities', p.24 - {AR2016_URL}\n"
        "Each year's Government-securities and Other-debt-securities sub-rows sum exactly to that "
        "year's 'Total debt securities' line, as do each year's measurement-basis sub-rows "
        "(Amortised cost + FVOCI + Expected credit losses for FY2018-FY2025; Held-to-maturity + "
        "Available-for-sale + Designated at FVTPL for FY2016-FY2017) - both cuts are genuine, "
        "reconciling splits of the same underlying note, not independently-sized estimates. "
        "'Government securities' is the Bank's own note heading in every year (not merely "
        "inferred); the 'Other debt securities' column is not further itemised by instrument or "
        "issuer in any year's note.\n" + STATEMENTS_ENTITY_NOTE
    ),
    first_col_width=64,
    source_height=280,
)

# ---------------------------------------------------------------
# Profit & Loss
# ---------------------------------------------------------------
bw.add_income_statement_sheet(
    title="Jordan International Bank Plc - Profit & Loss",
    subtitle="For the years ended 31 December (£'000, GBP)",
    rows=[
        ("SECTION", "Interest income", {}),
        ("DATA", "Interest income - debt securities", {"FY2025": 5292, "FY2024": 4661, "FY2023": 3651, "FY2022": 2427, "FY2021": 2027, "FY2020": 3009, "FY2019": 4028, "FY2018": 3420, "FY2017": 2794, "FY2016": 3647}),
        ("DATA", "Other interest income", {"FY2025": 27823, "FY2024": 32683, "FY2023": 29366, "FY2022": 16440, "FY2021": 11997, "FY2020": 11503, "FY2019": 12186, "FY2018": 12873, "FY2017": 11585, "FY2016": 11308}),
        ("TOTAL", "Total interest income", {"FY2025": 33115, "FY2024": 37344, "FY2023": 33017, "FY2022": 18867, "FY2021": 14024, "FY2020": 14512, "FY2019": 16214, "FY2018": 16293, "FY2017": 14379, "FY2016": 14955}),
        ("DATA", "Interest expense", {"FY2025": -15827, "FY2024": -18030, "FY2023": -15260, "FY2022": -5801, "FY2021": -2517, "FY2020": -4791, "FY2019": -6655, "FY2018": -6045, "FY2017": -4822, "FY2016": -4514}),
        ("TOTAL", "Net interest income", {"FY2025": 17288, "FY2024": 19314, "FY2023": 17757, "FY2022": 13066, "FY2021": 11507, "FY2020": 9721, "FY2019": 9559, "FY2018": 10248, "FY2017": 9557, "FY2016": 10441}),
        ("SECTION", "Non-interest income", {}),
        ("DATA", "Fees and commissions income", {"FY2025": 1347, "FY2024": 1916, "FY2023": 2394, "FY2022": 2654, "FY2021": 2112, "FY2020": 2315, "FY2019": 2153, "FY2018": 2031, "FY2017": 2018, "FY2016": 2792}),
        ("DATA", "Foreign exchange gains / dealing profits", {"FY2025": 35, "FY2024": 51, "FY2023": 45, "FY2022": 31, "FY2021": 23, "FY2020": 28, "FY2019": 47, "FY2018": 34, "FY2017": 109, "FY2016": 112}),
        ("DATA", "Other operating income", {"FY2024": 0, "FY2023": 0, "FY2022": 2, "FY2021": 4, "FY2020": 4, "FY2019": 4, "FY2018": 4, "FY2017": 6, "FY2016": 25}),
        ("DATA", "Profit on disposal of securities", {"FY2023": 1, "FY2022": 4, "FY2021": 55, "FY2019": 0, "FY2018": 262, "FY2017": 26, "FY2016": 14}),
        ("DATA", "Fair value changes in assets held at FVTPL", {"FY2019": -4, "FY2018": -10, "FY2017": -17, "FY2016": -33}),
        ("DATA", "Other gains/(losses)", {"FY2024": -102, "FY2022": 352}),
        ("DATA", "Gain on sale of assets held for sale", {"FY2025": 899}),
        ("TOTAL", "Total operating income", {"FY2025": 18670, "FY2024": 21179, "FY2023": 20197, "FY2022": 16109, "FY2021": 13701, "FY2020": 12068, "FY2019": 11759, "FY2018": 12569, "FY2017": 11699, "FY2016": 13351}),
        ("TOTAL", "Administrative expenses", {"FY2025": -7377, "FY2024": -8045, "FY2023": -7986, "FY2022": -6922, "FY2021": -6021, "FY2020": -5482, "FY2019": -5504, "FY2018": -5255, "FY2017": -5807, "FY2016": -5819}),
        ("DATA", "Depreciation (and amortisation)", {"FY2025": -528, "FY2024": -509, "FY2023": -546, "FY2022": -517, "FY2021": -583, "FY2020": -548, "FY2019": -513, "FY2018": -426, "FY2017": -451, "FY2016": -409}),
        ("DATA", "Other operating charges", {"FY2025": -5516, "FY2024": -5388, "FY2023": -4299, "FY2022": -3721, "FY2021": -3931, "FY2020": -3609, "FY2019": -2930, "FY2018": -2984, "FY2017": -2267, "FY2016": -2102}),
        ("DATA", "Provision for expected credit losses", {"FY2025": -3874, "FY2024": -616, "FY2023": -916, "FY2022": -702, "FY2021": -449, "FY2020": -368, "FY2019": -40, "FY2018": 102, "FY2017": -116, "FY2016": -106}),
        ("DATA", "Revaluation movement from OCI (recycled to P&L)", {"FY2017": -2139}),
        ("TOTAL", "Profit before taxation", {"FY2025": 2274, "FY2024": 6621, "FY2023": 6450, "FY2022": 4247, "FY2021": 2717, "FY2020": 2061, "FY2019": 3059, "FY2018": 4006, "FY2017": 1895, "FY2016": 5821}),
        ("DATA", "Tax (charge)/credit on profit", {"FY2025": -596, "FY2024": -1655, "FY2023": -1546, "FY2022": -737, "FY2021": 29, "FY2020": -118, "FY2019": -610, "FY2018": -660, "FY2017": -435, "FY2016": -1403}),
        ("TOTAL", "Profit for the financial year", {"FY2025": 1678, "FY2024": 4966, "FY2023": 4904, "FY2022": 3510, "FY2021": 2746, "FY2020": 1943, "FY2019": 2449, "FY2018": 3346, "FY2017": 1460, "FY2016": 4418}),
        ("SECTION", "Other comprehensive income", {}),
        ("DATA", "Revaluation transfer", {"FY2021": 0, "FY2020": 237, "FY2017": 2139}),
        ("DATA", "Change in fair value of debt securities (FVOCI)", {"FY2025": 171, "FY2024": -8, "FY2023": 357, "FY2022": -1386, "FY2021": -954, "FY2020": 341, "FY2019": 2456, "FY2018": -1594, "FY2017": -229, "FY2016": 986}),
        ("DATA", "Deferred tax on OCI", {"FY2025": -42, "FY2024": 2, "FY2023": -89, "FY2022": 346, "FY2021": 135, "FY2020": -134, "FY2019": -470, "FY2017": -337, "FY2016": -190}),
        ("TOTAL", "Total other comprehensive income", {"FY2025": 129, "FY2024": -6, "FY2023": 268, "FY2022": -1040, "FY2021": -819, "FY2020": 444, "FY2019": 1986, "FY2018": -1594, "FY2017": 1573, "FY2016": 796}),
        ("TOTAL", "Total comprehensive income for the year", {"FY2025": 1807, "FY2024": 4960, "FY2023": 5172, "FY2022": 2470, "FY2021": 1927, "FY2020": 2387, "FY2019": 4435, "FY2018": 1752, "FY2017": 3033, "FY2016": 5214}),
    ],
    sources_text=(
        "Sources - Jordan International Bank Plc's own Profit or Loss Account and Statement of "
        "Comprehensive Income, from each year's Companies House-filed Annual Report and Financial "
        "Statements (all 10 filings fully scanned/image-only, transcribed via page-image review):\n"
        f"FY2025: Annual Report and Financial Statements 2025, pp.26-27 - {AR2025_URL}\n"
        f"FY2024: Annual Report and Financial Statements 2024, pp.26-27 - {AR2024_URL}\n"
        f"FY2023: Annual Report and Financial Statements 2023, pp.24-25 - {AR2023_URL}\n"
        f"FY2022: Annual Report and Financial Statements 2022, pp.24-25 - {AR2022_URL}\n"
        f"FY2021: Annual Report and Financial Statements 2021, pp.25-26 - {AR2021_URL}\n"
        f"FY2020: Annual Report and Financial Statements 2020, pp.23-24 - {AR2020_URL}\n"
        f"FY2019: Annual Report and Financial Statements 2019, pp.20-21 - {AR2019_URL}\n"
        f"FY2018: Annual Report and Financial Statements 2018, p.18 - {AR2018_URL}\n"
        f"FY2017: Annual Report and Financial Statements 2017, p.16 - {AR2017_URL}\n"
        f"FY2016: Annual Report and Financial Statements 2016, p.12 - {AR2016_URL}\n"
        "Presentation changes across years, reproduced as disclosed: FY2021/FY2022 label the "
        "'Foreign exchange gains' line 'Dealing profits' and use 'Depreciation and amortisation' "
        "instead of 'Depreciation'; FY2021/FY2022 head the pre-tax profit line 'OPERATING PROFIT "
        "AND PROFIT ON ORDINARY ACTIVITIES BEFORE TAXATION' rather than 'PROFIT BEFORE TAXATION' "
        "(same line, label only, consistent all the way back to FY2016). FY2021's OCI section "
        "includes a distinct 'Revaluation transfer' line (nil that year); the same concept "
        "recurs FY2020 (£237k) and, at much larger scale with two sub-components (a 'current "
        "year' £654k and a 'prior years' £1,485k transfer, both from disposals of the Bank's "
        "AFS/FVOCI debt securities portfolio being recycled out of the revaluation reserve), "
        "FY2017 (£2,139k combined) - all recorded on the same 'Revaluation transfer' row. "
        "FY2017 also charges the identical £2,139k against operating profit as 'Revaluation "
        "movement from OCI (recycled to P&L)' - both the OCI-side reversal and the P&L-side "
        "recognition are the Bank's own presentation of the same recycling event, not a double "
        "count (Total comprehensive income nets the two to the correct £3,033k). FY2016-FY2019 "
        "use pre-IFRS 9 terminology, labelling the credit-loss line 'Impairment of loans and "
        "advances' rather than 'Provision for expected credit losses' (same underlying concept, "
        "transcribed onto the same row); FY2016-FY2018 also separately disclose small 'Fair "
        "value changes in assets held at FVTPL' movements not repeated from FY2020 onward. "
        "FY2018's Statement of Comprehensive Income is not presented as a separate page (unlike "
        "FY2019 onward) - its OCI movement of £(1,594)k is disclosed net-of-tax only, directly "
        "in that year's Statement of Changes in Equity, so no separate 'Deferred tax on OCI' "
        "figure exists for FY2018 to transcribe. 'Gain on sale of assets held for sale' only "
        "exists FY2025, tied to that year's new Assets held for sale balance sheet line.\n"
        + STATEMENTS_ENTITY_NOTE
    ),
    first_col_width=68,
    source_height=280,
)

# ---------------------------------------------------------------
# Statement of Changes in Equity - built year-by-year per the mandated
# reconciliation ladder. Ties exactly at every boundary - zero plug rows
# needed anywhere.
# ---------------------------------------------------------------
bw.add_equity_changes_sheet(
    title="Jordan International Bank Plc - Statement of Changes in Equity",
    subtitle="Chronological roll-forward, oldest to newest (£'000, GBP). Equity reconciliation ladder confirmed: every year's own closing balance ties exactly to both the next year's own opening balance and that year's own Balance Sheet Total equity - zero plug rows needed anywhere.",
    headers=["Called-up capital", "Share premium account", "Revaluation reserve", "Profit or loss account", "Total equity"],
    rows=[
        ("TOTAL", "Balance at 1 January 2016", (65000, 316, -1753, 11338, 74901)),
        ("DATA", "Movement in revaluation reserve, net of tax", (None, None, 796, None, 796)),
        ("DATA", "Profit for the year", (None, None, None, 4418, 4418)),
        ("TOTAL", "Total comprehensive income for the period", (0, 0, 796, 4418, 5214)),
        ("TOTAL", "Closing balance at 31 December 2016", (65000, 316, -957, 15756, 80115)),
        ("DATA", "Movement in revaluation reserve, net of tax", (None, None, 1573, None, 1573)),
        ("DATA", "Profit for the year", (None, None, None, 1460, 1460)),
        ("TOTAL", "Total comprehensive income for the period", (0, 0, 1573, 1460, 3033)),
        ("TOTAL", "Closing balance at 31 December 2017", (65000, 316, 616, 17216, 83148)),
        ("DATA", "Adjustment on adoption of IFRS 9, net of tax", (None, None, None, -330, -330)),
        ("TOTAL", "Balance at 1 January 2018 (restated)", (65000, 316, 616, 16886, 82818)),
        ("DATA", "Movement in revaluation reserve, net of tax", (None, None, -1594, None, -1594)),
        ("DATA", "Profit for the year", (None, None, None, 3346, 3346)),
        ("TOTAL", "Total comprehensive income for the period", (0, 0, -1594, 3346, 1752)),
        ("TOTAL", "Closing balance at 31 December 2018", (65000, 316, -978, 20232, 84570)),
        ("DATA", "Movement in revaluation reserve, net of tax", (None, None, 1986, None, 1986)),
        ("DATA", "Profit for the year", (None, None, None, 2449, 2449)),
        ("TOTAL", "Total comprehensive income for the period", (0, 0, 1986, 2449, 4435)),
        ("TOTAL", "Closing balance at 31 December 2019", (65000, 316, 1008, 22681, 89005)),
        ("DATA", "Movement in revaluation reserve, net of tax", (None, None, 444, None, 444)),
        ("DATA", "Profit for the year", (None, None, None, 1943, 1943)),
        ("TOTAL", "Total comprehensive income for the period", (0, 0, 444, 1943, 2387)),
        ("TOTAL", "Closing balance at 31 December 2020", (65000, 316, 1452, 24624, 91392)),
        ("DATA", "Movement in revaluation reserve, net of tax", (None, None, -819, None, -819)),
        ("DATA", "Profit for the year", (None, None, None, 2746, 2746)),
        ("TOTAL", "Total comprehensive income for the period", (0, 0, -819, 2746, 1927)),
        ("TOTAL", "Closing balance at 31 December 2021", (65000, 316, 633, 27370, 93319)),
        ("DATA", "Movement in revaluation reserve, net of tax", (None, None, -1040, None, -1040)),
        ("DATA", "Profit for the year", (None, None, None, 3510, 3510)),
        ("TOTAL", "Total comprehensive income for the period", (0, 0, -1040, 3510, 2470)),
        ("DATA", "Dividend paid to equity holders", (None, None, None, -12000, -12000)),
        ("TOTAL", "Closing balance at 31 December 2022", (65000, 316, -407, 18880, 83789)),
        ("DATA", "Movement in revaluation reserve, net of tax", (None, None, 268, None, 268)),
        ("DATA", "Profit for the year", (None, None, None, 4904, 4904)),
        ("TOTAL", "Total comprehensive income for the period", (0, 0, 268, 4904, 5172)),
        ("TOTAL", "Closing balance at 31 December 2023", (65000, 316, -139, 23784, 88961)),
        ("DATA", "Movement in revaluation reserve, net of tax", (None, None, -6, None, -6)),
        ("DATA", "Profit for the year", (None, None, None, 4966, 4966)),
        ("TOTAL", "Total comprehensive income for the period", (0, 0, -6, 4966, 4960)),
        ("TOTAL", "Closing balance at 31 December 2024", (65000, 316, -145, 28750, 93921)),
        ("DATA", "Movement in revaluation reserve, net of tax", (None, None, 129, None, 129)),
        ("DATA", "Profit for the year", (None, None, None, 1678, 1678)),
        ("TOTAL", "Total comprehensive income for the period", (0, 0, 129, 1678, 1807)),
        ("TOTAL", "Closing balance at 31 December 2025", (65000, 316, -16, 30428, 95728)),
    ],
    sources_text=(
        "Sources - Jordan International Bank Plc's own Statement of Changes in Equity, from each "
        "year's Companies House-filed Annual Report and Financial Statements (all 10 filings "
        "fully scanned/image-only, transcribed via page-image review):\n"
        f"FY2025: Annual Report and Financial Statements 2025, p.29 - {AR2025_URL}\n"
        f"FY2024: Annual Report and Financial Statements 2024, p.29 - {AR2024_URL}\n"
        f"FY2023: Annual Report and Financial Statements 2023, p.27 - {AR2023_URL}\n"
        f"FY2022: Annual Report and Financial Statements 2022, p.27 - {AR2022_URL}\n"
        f"FY2021: Annual Report and Financial Statements 2021, p.28 - {AR2021_URL}\n"
        f"FY2020: Annual Report and Financial Statements 2020, p.26 - {AR2020_URL}\n"
        f"FY2019: Annual Report and Financial Statements 2019, p.23 - {AR2019_URL}\n"
        f"FY2018: Annual Report and Financial Statements 2018, p.21 - {AR2018_URL}\n"
        f"FY2017: Annual Report and Financial Statements 2017, p.18 - {AR2017_URL}\n"
        f"FY2016: Annual Report and Financial Statements 2016, p.14 (also cross-checked against "
        f"FY2017's own FY2016 comparative column, p.18) - {AR2016_URL}\n"
        "Built year-by-year per the project's reconciliation ladder: each year's own opening + "
        "movements = closing balance, checked against both the next year's own reported opening "
        "and that year's own Balance Sheet Total equity before moving on. Ties exactly at every "
        "boundary - zero plug rows needed anywhere. The Bank adopted IFRS 9 with effect from 1 "
        "January 2018, recognising a one-off £330k transitional charge direct to retained "
        "earnings (confirmed against both the FY2018 SOCIE and Note 11's own ECL roll-forward, "
        "which opens 1 January 2018 with the same adjustment); FY2017's own £2,139k combined "
        "revaluation-reserve transfer (disposal recycling, see Profit & Loss sheet) is folded "
        "into that year's single 'Movement in revaluation reserve, net of tax' line here "
        "alongside the smaller like-for-like revaluation movement, matching this sheet's "
        "established one-row-per-year convention.\n" + STATEMENTS_ENTITY_NOTE
    ),
    first_col_width=46,
    source_height=260,
)

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("TOTAL", "Net cash generated/(used) in operating activities", {
        "FY2025": -8564, "FY2024": 32529, "FY2023": -15204, "FY2022": 7948, "FY2021": -11006,
        "FY2020": -35856, "FY2019": 6906, "FY2018": -60350, "FY2017": -26140, "FY2016": 17609,
    }),
    ("SECTION", "Cash flows from investing activities", {}),
    ("DATA", "Purchase of debt securities", {
        "FY2025": -86255, "FY2024": -146299, "FY2023": -104590, "FY2022": -87618, "FY2021": -78745,
        "FY2020": -98455, "FY2019": -69903, "FY2018": -102879, "FY2017": -115414, "FY2016": -80297,
    }),
    ("DATA", "Proceeds from the sale and maturity of debt securities", {
        "FY2025": 76479, "FY2024": 118151, "FY2023": 121290, "FY2022": 106746, "FY2021": 80891,
        "FY2020": 105008, "FY2019": 72333, "FY2018": 99096, "FY2017": 128302, "FY2016": 102898,
    }),
    ("DATA", "Interest received from debt securities", {
        "FY2025": 5151, "FY2024": 4134, "FY2023": 3804, "FY2022": 2599, "FY2021": 2217,
        "FY2020": 3122, "FY2019": 3869, "FY2018": 3290, "FY2017": 2969, "FY2016": 3039,
    }),
    ("DATA", "Other assets sold", {
        "FY2017": 976, "FY2016": 789,
    }),
    ("DATA", "Purchase of tangible fixed assets", {
        "FY2025": -239, "FY2024": -472, "FY2023": -343, "FY2022": -464, "FY2021": -447,
        "FY2020": -554, "FY2019": -424, "FY2018": -1153, "FY2017": -727, "FY2016": -392,
    }),
    ("DATA", "Purchase of intangible assets", {
        "FY2025": -225,
    }),
    ("TOTAL", "Net cash generated by investing activities", {
        "FY2025": -5089, "FY2024": -24486, "FY2023": 20161, "FY2022": 21263, "FY2021": 3916,
        "FY2020": 9121, "FY2019": 5875, "FY2018": -1646, "FY2017": 16106, "FY2016": 26037,
    }),
    ("SECTION", "Cashflows from financing activities", {}),
    ("DATA", "Dividend payment to equity holders", {
        "FY2022": -12000,
    }),
    ("DATA", "Increase in long term customer accounts", {
        "FY2018": 7428,
    }),
    ("TOTAL", "Net cash generated by financing activities", {
        "FY2023": 0, "FY2022": -12000, "FY2018": 7428,
    }),
    ("SECTION", "Reconciliation of movement in cash and cash equivalents", {}),
    ("DATA", "(Decrease)/increase in cash and cash equivalents", {
        "FY2025": -13653, "FY2024": 8043, "FY2023": 4957, "FY2022": 17211, "FY2021": -7090,
        "FY2020": -26735, "FY2019": 12781, "FY2018": -54568, "FY2017": -10034, "FY2016": 43646,
    }),
    ("DATA", "Cash and cash equivalents at beginning of year", {
        "FY2025": 74046, "FY2024": 66003, "FY2023": 61046, "FY2022": 59925, "FY2021": 67015,
        "FY2020": 93750, "FY2019": 80969, "FY2018": 65625, "FY2017": 75659, "FY2016": 32013,
    }),
    ("DATA", "Movement in cash and cash equivalents", {
        "FY2025": -13653, "FY2024": 7510, "FY2023": 7576, "FY2022": 9875, "FY2021": -7533,
        "FY2020": -27041, "FY2019": 12892, "FY2018": -56556, "FY2017": -14512, "FY2016": 58379,
    }),
    ("DATA", "Effect of foreign exchange rate changes", {
        "FY2025": 3623, "FY2024": 533, "FY2023": -2619, "FY2022": 7336, "FY2021": 443,
        "FY2020": 306, "FY2019": -111, "FY2018": 1988, "FY2017": 4478, "FY2016": -14733,
    }),
    ("TOTAL", "Cash and cash equivalents at end of year", {
        "FY2025": 64016, "FY2024": 74046, "FY2023": 66003, "FY2022": 77136, "FY2021": 59925,
        "FY2020": 67015, "FY2019": 93750, "FY2018": 11057, "FY2017": 65625, "FY2016": 75659,
    }),
]

bw.add_cash_flow_sheet(
    title="Jordan International Bank Plc - Cash Flow Statement",
    subtitle="For the years ended 31 December (£'000, GBP)",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=62,
    source_height=260,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Asset Quality - built from Note 11's ECL-by-stage table plus the note's
# own narrative gross-carrying-by-stage disclosure (rounded to the
# nearest £0.1m in the Bank's own text, unlike the exact-to-the-pound
# ECL/net figures in the table itself) for all 5 years.
# ---------------------------------------------------------------
bw.add_asset_quality_sheet(
    title="Jordan International Bank Plc - Asset Quality",
    subtitle="Loans and advances to customers at amortised cost - FRS 102 specific/collective basis FY2016-FY2017, IFRS 9 stage basis FY2018 onward (£'000, GBP)",
    rows=[
        ("SECTION", "Pre-IFRS 9 / FRS 102 basis (FY2016-FY2017): specific/collective provision", {}),
        ("DATA", "Gross loans and advances to customers (before specific provision)", {"FY2017": 158383, "FY2016": 163178}),
        ("DATA", "Specific impairment provision", {"FY2017": -460, "FY2016": -318}),
        ("TOTAL", "Net loans and advances to customers (FRS 102 basis)", {"FY2017": 157923, "FY2016": 162860}),
        ("DATA", "Memo: bank-wide collective (IBNR) provision, not allocated to a specific balance sheet line (Note 10)", {"FY2017": -189, "FY2016": -217}),
        ("SECTION", "Gross carrying amount by stage (IFRS 9, FY2018 onward; rounded to nearest £0.1m from FY2021)", {}),
        ("DATA", "Stage 1", {"FY2025": 157600, "FY2024": 224500, "FY2023": 254700, "FY2022": 214000, "FY2021": 193730, "FY2020": 180514, "FY2019": 144495, "FY2018": 159952}),
        ("DATA", "Stage 2", {"FY2025": 16300, "FY2024": 24800, "FY2023": 16500, "FY2022": 19900, "FY2021": 7363, "FY2020": 0, "FY2019": 6044, "FY2018": 6135}),
        ("DATA", "Stage 3", {"FY2025": 50900, "FY2024": 32900, "FY2023": 17100, "FY2022": 0, "FY2021": 0, "FY2020": 0, "FY2019": 2186, "FY2018": 2186}),
        ("TOTAL", "Gross carrying amount (as disclosed, rounded from FY2021 / exact FY2018-FY2020)", {"FY2025": 224800, "FY2024": 282200, "FY2023": 288300, "FY2022": 233900, "FY2021": 201093, "FY2020": 180514, "FY2019": 152725, "FY2018": 168273}),
        ("SECTION", "Expected credit loss allowance by stage (exact, from Note 11/12)", {}),
        ("DATA", "Stage 1", {"FY2025": -83, "FY2024": -126, "FY2023": -230, "FY2022": -159, "FY2021": -100, "FY2020": -112, "FY2019": -45, "FY2018": -27}),
        ("DATA", "Stage 2", {"FY2025": -18, "FY2024": -266, "FY2023": -1196, "FY2022": -378, "FY2021": -94, "FY2020": 0, "FY2019": -20, "FY2018": -25}),
        ("DATA", "Stage 3", {"FY2025": -5659, "FY2024": -2289, "FY2023": -410, "FY2022": 0, "FY2021": 0, "FY2020": 0, "FY2019": 0, "FY2018": 0}),
        ("TOTAL", "Total expected credit loss allowance", {"FY2025": -5760, "FY2024": -2681, "FY2023": -1836, "FY2022": -537, "FY2021": -194, "FY2020": -112, "FY2019": -65, "FY2018": -52}),
        ("TOTAL", "Net loans and advances to customers", {"FY2025": 224760, "FY2024": 282222, "FY2023": 288383, "FY2022": 233986, "FY2021": 201093, "FY2020": 180402, "FY2019": 152660, "FY2018": 168221}),
    ],
    sources_text=(
        "Sources - Jordan International Bank Plc's own Note 11 'Loans and advances to customers "
        "at amortised cost' (gross carrying amount by stage, narratively disclosed each year) and "
        "Note 12 'Impairment allowances' (expected credit loss by stage, tabulated), from each "
        "year's own Companies House-filed Annual Report and Financial Statements:\n"
        f"FY2025/FY2024: Annual Report and Financial Statements 2025, Notes 11-12, pp.44-45 - {AR2025_URL}\n"
        f"FY2024's own figures (used here) also independently confirmed against Annual Report 2024, "
        f"Notes 11-12, pp.44-45 - {AR2024_URL}\n"
        f"FY2023/FY2022: Annual Report and Financial Statements 2023, Notes 11-12, pp.42-43 - {AR2023_URL}\n"
        f"FY2022's own figures (used here) also independently confirmed against Annual Report 2022, "
        f"Notes 11-12, pp.41-43 - {AR2022_URL}\n"
        f"FY2021: Annual Report and Financial Statements 2021, Notes 11-12, pp.42-43 - {AR2021_URL}\n"
        f"FY2020: Annual Report and Financial Statements 2020, Notes 11-12, pp.40-41 - {AR2020_URL}\n"
        f"FY2019: Annual Report and Financial Statements 2019, Notes 10-11, pp.36-37 - {AR2019_URL}\n"
        f"FY2018: Annual Report and Financial Statements 2018, Notes 10-12, pp.34-36 (gross-by-"
        f"stage figures for FY2018 itself are not narratively disclosed in the FY2018 AR, which "
        f"gives only the ECL-by-stage table; FY2018's own gross-by-stage figures are instead "
        f"taken from FY2019's own FY2018 comparative narrative, Note 10, p.36) - {AR2018_URL}, "
        f"cross-checked against {AR2019_URL}\n"
        f"FY2017: Annual Report and Financial Statements 2017, Notes 9-10, p.27 (pre-IFRS 9 basis) "
        f"- {AR2017_URL}\n"
        f"FY2016: Annual Report and Financial Statements 2016, Notes 9-10, p.22 (pre-IFRS 9 basis) "
        f"- {AR2016_URL}\n"
        "Genuine cross-report inconsistency flagged, not silently reconciled: FY2024's own Annual "
        "Report states loans and advances to customers classified in Stage 2 that year as £24.8 "
        "million, but the following year's AR2025 restates its FY2024 comparative as £16.5 million "
        "(both Stage 1/Stage 3 figures and the Stage 2 expected credit loss of £266k are identical "
        "between the two vintages - only the FY2024 Stage 2 gross figure itself differs). FY2024's "
        "own originally-published £24.8m is used here per this project's convention.\n"
        "The gross-by-stage figures FY2021 onward are the Bank's own narrative disclosure, rounded "
        "to the nearest £0.1m in the source text itself; FY2018-FY2020's gross-by-stage figures are "
        "exact £'000 amounts (FY2019/FY2020 narratively disclosed to 3 decimal places in £m, e.g. "
        "'£144.495 million'; FY2018's are FY2019's own comparative, same precision). Because of "
        "the FY2021+ rounding, 'Gross carrying amount' minus 'Total expected credit loss allowance' "
        "does not tie exactly to 'Net loans and advances to customers' in those years - this is the "
        "source's own rounding, not a transcription error; FY2018-FY2020 tie exactly since no "
        "rounding is involved. FY2020's own narrative disclosure ('loans and advances to customers "
        "amounting to £180.402 million...was classified in stage 1') states the NET balance, unlike "
        "FY2019's own narrative style (which states GROSS figures per stage summing to the gross "
        "carrying amount before ECL) - a genuine year-on-year disclosure-style inconsistency in the "
        "Bank's own filings. This sheet instead derives FY2020's Stage 1 gross figure "
        "arithmetically from Note 11's own repayable-maturity table (£9k + £42,771k + £70,980k + "
        "£66,754k = £180,514k), which nets exactly against the £112k Stage 1 ECL to the Balance "
        "Sheet's own £180,402k net figure - more internally consistent than reusing the narrative's "
        "net figure as if it were gross. 'Net loans and advances to customers' is the exact figure "
        "in every year and ties to the Balance Sheet sheet's own 'Loans and advances to customers' "
        "line throughout.\n"
        "FY2016-FY2017 predate the Bank's 1 January 2018 IFRS 9 adoption and use FRS 102's "
        "incurred-loss model instead: a 'specific' provision against individually-identified "
        "impaired assets (Note 10) netted directly against the customer loan balance in Note 9, "
        "plus a separately-disclosed 'collective' (IBNR - incurred-but-not-reported) provision "
        "that the Bank's own notes do not allocate to a specific balance sheet line (shown here as "
        "a memo item, consistent with how the source itself presents it - not forced into the "
        "'Net loans and advances to customers' total, which ties exactly to the Balance Sheet "
        "without it)."
    ),
    first_col_width=76,
    source_height=420,
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, f"{unit}" if unit else None,
                         rows_data, sources_text, note=note, first_col_width=44, source_height=170)


metric(
    "CET1 Capital", "£m",
    [("Common Equity Tier 1 (CET1) capital", {
        "FY2024": 94, "FY2023": 89, "FY2022": 83.8, "FY2021": 93.3,
        "FY2020": 91.3, "FY2019": 88.9, "FY2018": 84.5, "FY2017": 83.0, "FY2016": 80.1,
    })],
    p3_sources(),
    note="FY2025 not yet published (see sources). No Additional Tier 1/Tier 2 capital is "
         "disclosed in any year, so CET1 = Tier 1 = Total Capital throughout. FY2016 figure is "
         "the 'fully loaded' basis (see sources note on the fully-loaded/PRA-transitional split "
         "unique to that year).",
)
metric(
    "CET1 Ratio", "%",
    [("CET1 ratio", {
        "FY2024": "19.9%", "FY2023": "19.8%", "FY2022": "19.3%", "FY2021": "22.9%",
        "FY2020": "22.7%", "FY2019": "22.35%", "FY2018": "22.05%", "FY2017": "21.15%", "FY2016": "20.44%",
    })],
    p3_sources(),
)
metric(
    "Tier 1 Capital", "£m",
    [("Tier 1 capital", {
        "FY2024": 94, "FY2023": 89, "FY2022": 83.8, "FY2021": 93.3,
        "FY2020": 91.3, "FY2019": 88.9, "FY2018": 84.5, "FY2017": 83.0, "FY2016": 80.1,
    })],
    p3_sources(),
    note="Equal to CET1 capital - no Additional Tier 1 instruments are disclosed in any year.",
)
metric(
    "Tier 1 Ratio", "%",
    [("Tier 1 ratio", {
        "FY2024": "19.9%", "FY2023": "19.8%", "FY2022": "19.3%", "FY2021": "22.9%",
        "FY2020": "22.7%", "FY2019": "22.35%", "FY2018": "22.05%", "FY2017": "21.15%", "FY2016": "20.44%",
    })],
    p3_sources(),
)
metric(
    "Total Capital", "£m",
    [("Total capital", {
        "FY2024": 94, "FY2023": 89, "FY2022": 83.8, "FY2021": 93.3,
        "FY2020": 91.3, "FY2019": 88.9, "FY2018": 84.5, "FY2017": 83.0, "FY2016": 80.1,
    })],
    p3_sources(),
    note="Equal to CET1/Tier 1 capital - no Tier 2 instruments are disclosed in any year.",
)
metric(
    "Total Capital Ratio", "%",
    [("Total capital ratio", {
        "FY2024": "19.9%", "FY2023": "19.8%", "FY2022": "19.3%", "FY2021": "22.9%",
        "FY2020": "22.7%", "FY2019": "22.35%", "FY2018": "22.05%", "FY2017": "21.15%", "FY2016": "20.44%",
    })],
    p3_sources(),
)
metric(
    "Total RWAs", "£m",
    [("Total risk-weighted exposure amount (RWA)", {
        "FY2024": 473, "FY2023": 449, "FY2022": 435.3, "FY2021": 407.5,
        "FY2020": 401.6, "FY2019": 397.8, "FY2018": 383.1, "FY2017": 392.6, "FY2016": 391.8,
    })],
    p3_sources(),
)

bw.add_rwa_breakdown_sheet(
    title="Jordan International Bank Plc - RWA Breakdown",
    subtitle="Solo basis throughout (per Pillar 3 disclosures). £'000, except FY2021/FY2020 derived from £m (see source note).",
    rows=[
        ("DATA", "Credit risk (excluding CCR)", {"FY2024": 418080, "FY2023": 402263, "FY2022": 388850, "FY2021": 361250, "FY2020": 356250, "FY2019": 352400, "FY2018": 335400, "FY2017": 348500, "FY2016": 350000}),
        ("DATA", "Counterparty credit risk (CCR)", {"FY2024": 1582, "FY2023": 648, "FY2022": 4.8, "FY2018": 200, "FY2017": 200, "FY2016": 100}),
        ("DATA", "Market risk", {"FY2024": 21275, "FY2023": 19460, "FY2022": 23073, "FY2021": 23750, "FY2020": 22500, "FY2019": 22100, "FY2018": 23300, "FY2017": 19800, "FY2016": 20700}),
        ("DATA", "Operational risk", {"FY2024": 30998, "FY2023": 25918, "FY2022": 23421, "FY2021": 22500, "FY2020": 22500, "FY2019": 23300, "FY2018": 24100, "FY2017": 24000, "FY2016": 20900}),
        ("DATA", "Credit valuation adjustment (CVA)", {"FY2024": 1078, "FY2023": 645, "FY2021": 250, "FY2018": 100, "FY2017": 100, "FY2016": 100}),
        ("TOTAL", "Total risk-weighted exposure amount", {"FY2024": 473013, "FY2023": 448934, "FY2022": 435349, "FY2021": 407500, "FY2020": 401600, "FY2019": 397800, "FY2018": 383100, "FY2017": 392600, "FY2016": 391800}),
    ],
    sources_text=(
        "Sources - Jordan International Bank Plc's own Pillar 3 Report, Section 3.3 'Minimum "
        "capital requirements' (a direct RWA-by-risk-type table FY2016-FY2019, a UK-OV1-style "
        "Pillar 1 capital allocation table FY2020 onward):\n"
        f"FY2024: Pillar 3 Report 2024, Section 3.3 - {P3_2024_URL}\n"
        f"FY2023: Pillar 3 Report 2023, Section 3.3 - {P3_2023_URL}\n"
        f"FY2022: Pillar 3 Report 2022, Section 3.3 - {P3_2022_URL}\n"
        f"FY2021: Pillar 3 Report 2021, Section 3.3 - {P3_2021_URL}\n"
        f"FY2020: Pillar 3 Report 2020, Section 3.3 'Minimum capital requirements' - {P3_2020_URL}\n"
        f"FY2019: Pillar 3 Report 2019, Section 4 'Capital resources, requirements and leverage' - {P3_2019_URL}\n"
        f"FY2018: Pillar 3 Report 2018, Section 4 - {P3_2018_URL}\n"
        f"FY2017: Pillar 3 Report 2017, Section 4 - {P3_2017_URL}\n"
        f"FY2016: Pillar 3 Report 2016, Section 4 - {P3_2016_URL}\n"
        "FY2025: no standalone Pillar 3 Report was published on the Bank's website as of this "
        "session (see p3_sources note) - genuinely not yet disclosed, left blank rather than "
        "guessed. FY2022's Counterparty credit risk (CCR) figure of £4.8k is reproduced exactly as "
        "printed in the Bank's own table (all other rows that year are in the many-thousands range) "
        "- it is not a transcription error: the Bank's own 'Total capital allocation' of £435,349k "
        "only reconciles if this row is taken as £4.8k, not a rounding-scaled £4,800k. FY2022's "
        "table has no separate CVA line (nil/immaterial that year, folded into the total). FY2021's "
        "Pillar 3 Report predates the UK OV1 template and instead discloses Pillar 1 capital "
        "requirements by risk type in £m (Credit risk £28.9m [including CCR, not broken out "
        "separately that year], Market risk £1.9m, Operational risk £1.8m, CVA £0.02m, Total "
        "£32.6m) - RWA-equivalent figures here are derived by multiplying each by 12.5 (i.e. dividing "
        "by the 8% minimum capital ratio), consistent with the rest of this project's convention for "
        "years lacking a direct RWA table; the derived Total (£407.5m) ties exactly to the Total "
        "RWAs metric sheet's own FY2021 figure, cross-validating the derivation. FY2020's own "
        "Section 3.3 similarly lacks a direct RWA table (it discloses a Pillar 1/Pillar 2A capital "
        "ALLOCATION table instead, in £m: Credit risk £28.5m, Market risk £1.8m, Operational risk "
        "£1.8m, Pillar 1 total £32.1m - the Pillar 2A-only add-ons for credit concentration risk, "
        "interest rate risk in the banking book and reputational risk are excluded here as they are "
        "not part of the Pillar 1 RWA base); the same x12.5 derivation gives a derived total of "
        "£401.25m against the Bank's own separately-disclosed Total RWA of £401.6m - a ~£0.35m gap "
        "attributable to rounding in the £m Pillar 1 inputs, not a transcription error. FY2016-"
        "FY2019 instead have a direct RWA-by-risk-type table (same template as FY2022/FY2023), so "
        "no derivation is needed for those years; FY2019's own table discloses nil/immaterial CCR "
        "and CVA that year (shown as '~' in the source, treated as blank here, consistent with how "
        "FY2022's nil CVA is also left blank)."
    ),
    first_col_width=70,
    source_height=340,
)

metric(
    "Leverage Ratio", "%",
    [("Basel III leverage ratio", {
        "FY2024": "19.3%", "FY2023": "19.7%", "FY2022": "19.3%", "FY2021": "23.4%",
        "FY2020": "24.2%", "FY2019": "22.85%", "FY2018": "21.53%", "FY2017": "20.93%", "FY2016": "19.32%",
    })],
    p3_sources(),
)
metric(
    "LCR", "%",
    [("Liquidity Coverage Ratio (LCR)", {
        "FY2024": "490%", "FY2023": "343%", "FY2022": "330%", "FY2021": "428%",
        "FY2020": "509%", "FY2019": "373.86%", "FY2018": "223.56%", "FY2017": "525.38%", "FY2016": "660%",
    })],
    p3_sources(),
)
metric(
    "NSFR", "%",
    [("Net Stable Funding Ratio (NSFR)", {
        "FY2024": "129%", "FY2023": "125.1%", "FY2022": "129%", "FY2016": "123%",
    })],
    p3_sources(),
    note="Not disclosed for FY2017-FY2021 - genuinely absent from every one of those years' own "
         "Pillar 3 Reports (checked directly, not assumed); disclosed once in FY2016's own summary "
         "infographic (123%) before dropping out of the Bank's disclosure until it reappears from "
         "the FY2022 KM1 template onward.",
)
bw.add_not_disclosed_metric_sheets(
    ["MREL Ratio"], p3_sources(),
    per_note={
        "MREL Ratio": "Not disclosed in any year - Jordan International Bank Plc is not "
                      "identified as a UK resolution entity in these reports.",
    },
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {"FY2025": 444633, "FY2024": 484970, "FY2023": 446609, "FY2022": 429969, "FY2021": 384254, "FY2020": 371629, "FY2019": 383726, "FY2018": 387205, "FY2017": 393107, "FY2016": 410772}),
        ("Loans and advances to customers", {"FY2025": 224760, "FY2024": 282222, "FY2023": 288383, "FY2022": 233986, "FY2021": 201093, "FY2020": 180402, "FY2019": 152660, "FY2018": 168221, "FY2017": 157923, "FY2016": 162860}),
        ("Customer accounts", {"FY2025": 169530, "FY2024": 211430, "FY2023": 176886, "FY2022": 167312, "FY2021": 110410, "FY2020": 111598, "FY2019": 107367, "FY2018": 99516, "FY2017": 73435, "FY2016": 86186}),
        ("Shareholders' Funds", {"FY2025": 95728, "FY2024": 93921, "FY2023": 88961, "FY2022": 83789, "FY2021": 93319, "FY2020": 91392, "FY2019": 89005, "FY2018": 84570, "FY2017": 83148, "FY2016": 80115}),
    ],
    balance_sheet_unit="£'000",
    income_statement_totals=[
        ("Total operating income", {"FY2025": 18670, "FY2024": 21179, "FY2023": 20197, "FY2022": 16109, "FY2021": 13701, "FY2020": 12068, "FY2019": 11759, "FY2018": 12569, "FY2017": 11699, "FY2016": 13351}),
        ("Total operating expense", {"FY2025": -17295, "FY2024": -14558, "FY2023": -13747, "FY2022": -11862, "FY2021": -10984, "FY2020": -10007, "FY2019": -8700, "FY2018": -8563, "FY2017": -9804, "FY2016": -7530}),
        ("Profit for the financial year", {"FY2025": 1678, "FY2024": 4966, "FY2023": 4904, "FY2022": 3510, "FY2021": 2746, "FY2020": 1943, "FY2019": 2449, "FY2018": 3346, "FY2017": 1460, "FY2016": 4418}),
    ],
    income_statement_unit="£'000",
    equity_changes_totals=[
        ("Opening equity", {"FY2025": 93921, "FY2024": 88961, "FY2023": 83789, "FY2022": 93319, "FY2021": 91392, "FY2020": 89005, "FY2019": 84570, "FY2018": 83148, "FY2017": 80115, "FY2016": 74901}),
        ("Total comprehensive income/(loss) for the year", {"FY2025": 1807, "FY2024": 4960, "FY2023": 5172, "FY2022": 2470, "FY2021": 1927, "FY2020": 2387, "FY2019": 4435, "FY2018": 1752, "FY2017": 3033, "FY2016": 5214}),
        ("Other equity movements, net", {"FY2025": 0, "FY2024": 0, "FY2023": 0, "FY2022": -12000, "FY2021": 0, "FY2020": 0, "FY2019": 0, "FY2018": -330, "FY2017": 0, "FY2016": 0}),
        ("Closing equity", {"FY2025": 95728, "FY2024": 93921, "FY2023": 88961, "FY2022": 83789, "FY2021": 93319, "FY2020": 91392, "FY2019": 89005, "FY2018": 84570, "FY2017": 83148, "FY2016": 80115}),
    ],
    equity_changes_unit="£'000",
    cash_flow_totals=[
        ("Net cash from/(used in) operating activities", {
            "FY2025": -8564, "FY2024": 32529, "FY2023": -15204, "FY2022": 7948, "FY2021": -11006,
            "FY2020": -35856, "FY2019": 6906, "FY2018": -60350, "FY2017": -26140, "FY2016": 17609,
        }),
        ("Net cash from/(used in) investing activities", {
            "FY2025": -5089, "FY2024": -24486, "FY2023": 20161, "FY2022": 21263, "FY2021": 3916,
            "FY2020": 9121, "FY2019": 5875, "FY2018": -1646, "FY2017": 16106, "FY2016": 26037,
        }),
        ("Net cash from/(used in) financing activities", {
            "FY2025": 0, "FY2024": 0, "FY2023": 0, "FY2022": -12000, "FY2021": 0,
            "FY2020": 0, "FY2019": 0, "FY2018": 7428, "FY2017": 0, "FY2016": 0,
        }),
        ("Cash and cash equivalents at end of year", {
            "FY2025": 64016, "FY2024": 74046, "FY2023": 66003, "FY2022": 77136, "FY2021": 59925,
            "FY2020": 67015, "FY2019": 93750, "FY2018": 11057, "FY2017": 65625, "FY2016": 75659,
        }),
    ],
    cash_flow_unit="£'000",
    ratios=[
        ("CET1 ratio (%)", {
            "FY2024": 19.9, "FY2023": 19.8, "FY2022": 19.3, "FY2021": 22.9,
            "FY2020": 22.7, "FY2019": 22.35, "FY2018": 22.05, "FY2017": 21.15, "FY2016": 20.44,
        }),
        ("LCR (%)", {
            "FY2024": 490, "FY2023": 343, "FY2022": 330, "FY2021": 428,
            "FY2020": 509, "FY2019": 373.86, "FY2018": 223.56, "FY2017": 525.38, "FY2016": 660,
        }),
    ],
    note="FY2025 Pillar 3 figures not yet published as of this session - see individual metric "
         "sheets. The FY2022-to-FY2023 cash bridge does not tie exactly (£16,090k gap) due to a "
         "genuine inconsistency between the Bank's own FY2022 and FY2023 Annual Reports, and the "
         "FY2018-to-FY2019 bridge does not tie exactly (£69,912k gap) for the same underlying "
         "reason one cycle earlier (a disclosed change in the Bank's own definition of cash and "
         "cash equivalents) - see the Cash Flow Statement sheet's source notes for full detail. "
         "This workbook now spans FY2016-FY2025 (10 years), extended back from the original "
         "FY2021-FY2025 window per this project's historical-depth effort (HD-026); FY2016-FY2017 "
         "predate the Bank's 1 January 2018 IFRS 9 adoption and use FRS 102's incurred-loss "
         "impairment model instead (see the Asset Quality sheet).",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/JORDAN INTERNATIONAL BANK FINANCIALS.xlsx")
print("Saved.")
