import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first

CH_BASE = "https://find-and-update.company-information.service.gov.uk/company/07425398/filing-history"
AR25_URL = f"{CH_BASE}/MzUyNjQ0MDA3MmFkaXF6a2N4/document?format=pdf&download=0"
AR23_URL = f"{CH_BASE}/MzQyMDE3MTk5NWFkaXF6a2N4/document?format=pdf&download=0"
AR21_URL = f"{CH_BASE}/MzMzODgwNTQxMWFkaXF6a2N4/document?format=pdf&download=0"

CASH_FLOW_SOURCES = (
    "Sources — all figures are Itau BBA International plc (\"IBBAInt\"/\"the Bank\") solo-entity (Bank, not Group) "
    "Statement of Cash Flows, USD'000:\n"
    f"FY2025 & FY2024: 2025 Annual Report, p.65 (Statements of Cash Flows) — {AR25_URL}\n"
    f"FY2023 & FY2022: 2023 Annual Report, p.57 (Statement of Cash Flows) — {AR23_URL}\n"
    f"FY2021: 2021 Annual Report, p.56 (Statement of Cash Flows) — {AR21_URL}\n"
    "Note: these are Companies House filing copies (fully scanned/image-only PDFs, no text layer — transcribed via "
    "page-render + manual reading). The bank's own site (itau.co.uk) returned HTTP 403 to every fetch, and the "
    "domain referenced throughout the Annual Report for further disclosures (www.itaubba.co.uk) was unreachable "
    "this session (connection refused/timed out, and no usable Wayback Machine snapshot was found — a genuine "
    "Internet Archive-side outage, not bank-specific), so Companies House was the only available source. The source "
    "labels 'Derivatives designated as hedging instruments' twice per year (once within operating assets, once "
    "within operating liabilities) — disambiguated here as '(assets)' / '(liabilities)' for clarity; this is a "
    "labeling change only, not a data change. 'Purchases of financial assets measured at fair value through OCI' "
    "is printed with an inconsistent sign convention across report vintages (positive in the FY2025 report's own "
    "FY2025/FY2024 columns, negative in the FY2023 report's own FY2023/FY2022 columns) — transcribed exactly as "
    "each source year printed it, not normalized. Blank cells indicate that year's report did not disclose that "
    "specific line; a dash ('-') in the source is shown as 0. All 5 years' opening cash balances tie exactly to "
    "the prior year's closing balance. DATA QUALITY NOTE: summing FY2024's own individually-transcribed line "
    "items gives USD 233,960k for 'Net cash flow from operating activities before payment of income tax', a USD "
    "7k gap against the figure the source itself prints for that subtotal (USD 233,967k, used here) — an "
    "immaterial rounding artifact within the source document, not a transcription error (every individual line "
    "item ties exactly to the source page); flagged rather than silently adjusted, per this project's convention."
)

ENTITY_NOTE = (
    "All 3 statement sheets (Balance Sheet, Profit & Loss, Statement of Changes in Equity) use the Bank/solo "
    "column (not Group/consolidated), matching the entity basis already used for this workbook's Cash Flow "
    "Statement. Asset Quality also uses the Bank column. Pillar 3 metric sheets (CET1/Tier 1/Total Capital, "
    "ratios, Total RWAs, Leverage Ratio) remain Group/consolidated basis, matching how the Annual Report's own "
    "'Capital' section is presented (Group level only, all 5 years) - this is a pre-existing, unchanged choice."
)

def statement_sources(page, doc_label, url, note_extra=""):
    return (
        f"Source — Itau BBA International plc Bank (solo, not Group) financial statements, {doc_label} Annual "
        f"Report, p.{page} — {url}\n"
        + ENTITY_NOTE + (" " + note_extra if note_extra else "")
    )

PILLAR3_2021_URL = "https://www.itau.com.br/content/dam/ibba/en/Pillar-3-2021.pdf"
PILLAR3_2021_WAYBACK = "http://web.archive.org/web/20230502062443/https://www.itau.com.br/content/dam/ibba/en/Pillar-3-2021.pdf"
PILLAR3_2022_URL = "https://www.itau.com.br/media/dam/m/58b090bc84eddb94/original/Pillar-3-2022.pdf"
PILLAR3_2022_WAYBACK = "http://web.archive.org/web/20230502054346/https://www.itau.com.br/media/dam/m/58b090bc84eddb94/original/Pillar-3-2022.pdf"
PILLAR3_2023_URL = "https://www.itau.com.br/media/dam/m/11e1e216dd5df1fd/original/Pillar-3-2023.pdf"
PILLAR3_2023_WAYBACK = "http://web.archive.org/web/20240812211731/https://www.itau.com.br/media/dam/m/11e1e216dd5df1fd/original/Pillar-3-2023.pdf"

def pillar3_disclosure_sources(note_extra=""):
    return (
        "Source — Itau BBA International plc Group (consolidated) standalone Pillar 3 Disclosures documents — "
        "these are the same documents the Annual Report's own 'Capital' section refers readers to via "
        "www.itaubba.co.uk (see the p3_sources note on this workbook's other Pillar 3 sheets); that domain, and "
        "itau.co.uk, were unreachable this session, but the documents themselves were located on itau.com.br "
        "(the Brazilian parent Itau Unibanco's investor-relations site). Live fetches of itau.com.br also "
        "returned HTTP 403 this session (Cloudflare bot-challenge), so all figures below were retrieved via "
        "Wayback Machine archive snapshots instead:\n"
        f"FY2023: 'Market Discipline – 2023 Pillar III' (2023 Pillar 3 Disclosures), Template UK KM1 (Section 10 "
        f"'Key Metrics'), p.41 — live: {PILLAR3_2023_URL} — archived: {PILLAR3_2023_WAYBACK}\n"
        f"FY2022 (and FY2021 comparative column on the same table): '2022 Pillar 3 Disclosures', Template UK KM1 "
        f"(Section 10 'Key Metrics'), p.44 — live: {PILLAR3_2022_URL} — archived: {PILLAR3_2022_WAYBACK}\n"
        f"FY2021 LCR only (the 2021 document predates the UK KM1 template): '2021 Pillar 3 Disclosures', Table 26 "
        f"'Liquidity Coverage Ratio', p.46 — live: {PILLAR3_2021_URL} — archived: {PILLAR3_2021_WAYBACK}\n"
        "All figures are Group/consolidated (IBBAInt Group) basis, matching this workbook's other Pillar 3 sheets. "
        "FY2024/FY2025 are blank — no standalone Pillar 3 Disclosures document for either year was found on "
        "itau.com.br or in the Wayback Machine this session (only quarterly credit fact sheets and the Annual "
        "Reports were found, and the Annual Report itself does not break out these figures for any year)." +
        (" " + note_extra if note_extra else "")
    )

def p3_sources(page, doc_label, url, note_extra=""):
    return (
        f"Source — Itau BBA International plc Group (consolidated) regulatory capital summary, {doc_label} "
        f"Annual Report, p.{page} ('Capital' section of the Strategic Report) — {url}\n"
        "The Annual Report states in full that additional Pillar 3 Disclosures (capital detail, LCR, NSFR, MREL) "
        "are published as a separate, standalone unaudited document on www.itaubba.co.uk — that site was "
        "unreachable this session (connection refused/timed out; no usable Wayback Machine snapshot found), so "
        "only the summary figures printed directly in the Annual Report's own 'Capital' section are used here. "
        "Figures are Group/consolidated basis (the Annual Report's Capital section is presented at Group level "
        "only, not solo Bank level, throughout all 5 years)." + (" " + note_extra if note_extra else "")
    )

bw = BankWorkbook(bank_name="Itau BBA International plc", years=YEARS, header_color="F58220")

# ---------------------------------------------------------------
# Sheet 1: Balance Sheet
# ---------------------------------------------------------------
balance_sheet_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and balances at central banks", {"FY2025": 17, "FY2024": 16, "FY2023": 16, "FY2022": 15, "FY2021": 16}),
    ("DATA", "Trading assets", {"FY2025": 10362, "FY2024": 6920, "FY2023": 11783, "FY2022": 12227, "FY2021": 20508}),
    ("DATA", "Financial assets designated at fair value through profit or loss", {"FY2024": 44509, "FY2023": 49259, "FY2022": 438169, "FY2021": 1022915}),
    ("DATA", "Financial assets measured at fair value through OCI", {"FY2025": 1735647, "FY2024": 1824171, "FY2023": 2029771, "FY2022": 1175521}),
    ("DATA", "Derivative financial instruments", {"FY2025": 402429, "FY2024": 489006, "FY2023": 264447, "FY2022": 414210, "FY2021": 402295}),
    ("DATA", "Loans and advances to banks", {"FY2025": 890765, "FY2024": 1714874, "FY2023": 1122546, "FY2022": 665708, "FY2021": 658659}),
    ("DATA", "Loans and advances to customers", {"FY2025": 4044575, "FY2024": 4104314, "FY2023": 3868767, "FY2022": 3604470, "FY2021": 3221895}),
    ("DATA", "Debt securities at amortised cost", {"FY2023": 2192, "FY2021": 2192}),
    ("DATA", "Property, plant and equipment", {"FY2025": 390, "FY2024": 1188, "FY2023": 2007, "FY2022": 570, "FY2021": 1672}),
    ("DATA", "Goodwill and intangible assets", {"FY2025": 7, "FY2024": 37, "FY2023": 7, "FY2022": 291, "FY2021": 183}),
    ("DATA", "Investments in subsidiaries", {"FY2025": 803125, "FY2024": 743998, "FY2023": 719482, "FY2022": 629248, "FY2021": 627841}),
    ("DATA", "Current tax assets", {"FY2025": 0, "FY2024": 1107, "FY2023": 1148, "FY2022": 55, "FY2021": 1143}),
    ("DATA", "Deferred tax assets", {"FY2025": 2970, "FY2024": 2528, "FY2023": 2675, "FY2022": 2637, "FY2021": 1070}),
    ("DATA", "Other assets", {"FY2025": 5947, "FY2024": 4515, "FY2023": 13667, "FY2022": 38860, "FY2021": 3125}),
    ("TOTAL", "Total Assets", {"FY2025": 7896227, "FY2024": 8937146, "FY2023": 8085575, "FY2022": 6981727, "FY2021": 5963514}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Trading liabilities", {"FY2025": 10306, "FY2024": 6911, "FY2023": 11786, "FY2022": 9587, "FY2021": 18584}),
    ("DATA", "Financial liabilities designated at fair value through profit or loss", {"FY2024": 44456, "FY2023": 49259, "FY2021": 410}),
    ("DATA", "Derivative financial instruments", {"FY2025": 526233, "FY2024": 462780, "FY2023": 278452, "FY2022": 404354, "FY2021": 405816}),
    ("DATA", "Deposits from banks", {"FY2025": 1053183, "FY2024": 925795, "FY2023": 1358652, "FY2022": 837569, "FY2021": 851201}),
    ("DATA", "Customer accounts", {"FY2025": 1740013, "FY2024": 2745061, "FY2023": 1709639, "FY2022": 1914084, "FY2021": 1751887}),
    ("DATA", "Debt securities in issue", {"FY2025": 2364797, "FY2024": 2613477, "FY2023": 2688433, "FY2022": 2373670, "FY2021": 1571907}),
    ("DATA", "Provisions", {"FY2025": 236, "FY2024": 258, "FY2023": 319, "FY2022": 525, "FY2021": 428}),
    ("DATA", "Current tax liabilities", {"FY2025": 285, "FY2024": 1186, "FY2023": 0, "FY2022": 15, "FY2021": 580}),
    ("DATA", "Deferred tax liabilities", {"FY2025": 54, "FY2024": 101, "FY2023": 315, "FY2022": 20, "FY2021": 29}),
    ("DATA", "Other liabilities", {"FY2025": 46646, "FY2024": 74207, "FY2023": 25004, "FY2022": 43366, "FY2021": 32798}),
    ("TOTAL", "Total Liabilities", {"FY2025": 5741753, "FY2024": 6874232, "FY2023": 6121859, "FY2022": 5583190, "FY2021": 4633640}),
    ("SECTION", "Equity", {}),
    ("DATA", "Called-up share capital", {"FY2025": 1221034, "FY2024": 1221034, "FY2023": 1221034, "FY2022": 935000, "FY2021": 600000}),
    ("DATA", "Share premium", {"FY2025": 213966, "FY2024": 213966, "FY2023": 213966, "FY2022": 0, "FY2021": 0}),
    ("DATA", "Revaluation reserves", {"FY2025": 205, "FY2024": -1273, "FY2023": -1644, "FY2022": -4029, "FY2021": 53}),
    ("DATA", "Other reserves", {"FY2022": 0, "FY2021": 332948}),
    ("DATA", "Retained earnings (including profit for the year)", {"FY2025": 719269, "FY2024": 629187, "FY2023": 530360, "FY2022": 467566, "FY2021": 396873}),
    ("TOTAL", "Total Equity", {"FY2025": 2154474, "FY2024": 2062914, "FY2023": 1963716, "FY2022": 1398537, "FY2021": 1329874}),
    ("TOTAL", "Total Liabilities and Equity", {"FY2025": 7896227, "FY2024": 8937146, "FY2023": 8085575, "FY2022": 6981727, "FY2021": 5963514}),
]

bw.add_balance_sheet_sheet(
    title="Itau BBA International plc — Balance Sheet (Bank, solo)",
    subtitle="Itau BBA International plc (Bank/solo basis, not Group), USD'000 unless stated",
    rows=balance_sheet_rows,
    sources_text=statement_sources(61, "2025", AR25_URL) + "\n\n"
        + statement_sources(53, "2023", AR23_URL, "Covers FY2023/FY2022.") + "\n\n"
        + statement_sources(52, "2021", AR21_URL, "Covers FY2021 (FY2020 comparative not used). "
            "'Other reserves' only appears as a distinct line for FY2021 - subsequently merged/relabelled; "
            "'Financial assets designated at fair value through profit or loss' and 'Debt securities at "
            "amortised cost' are genuinely nil/blank for FY2025 and FY2022/FY2023/FY2020 respectively per each "
            "year's own disclosure, not omissions."),
    first_col_width=68,
    source_height=190,
    unit_suffix=" (USD'000)",
)

# ---------------------------------------------------------------
# Sheet 2: Profit & Loss
# ---------------------------------------------------------------
income_statement_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest income", {"FY2025": 355575, "FY2024": 419820, "FY2023": 365401, "FY2022": 148478, "FY2021": 87382}),
    ("DATA", "Interest expense", {"FY2025": -280371, "FY2024": -317737, "FY2023": -278379, "FY2022": -94759, "FY2021": -47981}),
    ("TOTAL", "Net interest income", {"FY2025": 75204, "FY2024": 102083, "FY2023": 87022, "FY2022": 53719, "FY2021": 39401}),
    ("DATA", "Fee and commission income", {"FY2025": 9457, "FY2024": 11268, "FY2023": 10932, "FY2022": 13581, "FY2021": 12554}),
    ("DATA", "Fee and commission expense", {"FY2025": -6329, "FY2024": -8787, "FY2023": -11488, "FY2022": -12687, "FY2021": -17808}),
    ("TOTAL", "Net fee and commission income / (expense)", {"FY2025": 3128, "FY2024": 2481, "FY2023": -556, "FY2022": 894, "FY2021": -5254}),
    ("DATA", "Net income on financial assets and liabilities at fair value through profit or loss", {"FY2025": 66407, "FY2024": 45201, "FY2023": 19474, "FY2022": 32120}),
    ("DATA", "Net income / (expense) on financial assets at fair value through OCI", {"FY2025": -89, "FY2024": -778, "FY2023": 985, "FY2022": -57}),
    ("DATA", "Dividend income", {"FY2024": 5, "FY2023": 0, "FY2022": 20004, "FY2021": 23797}),
    ("DATA", "Net income on other financial operations", {"FY2025": 8208, "FY2024": 9387, "FY2023": 7943, "FY2022": 4469, "FY2021": 5590}),
    ("TOTAL", "Net income on financial operations", {"FY2025": 74526, "FY2024": 53811, "FY2023": 28402, "FY2022": 56536, "FY2021": 29192}),
    ("DATA", "Other operating income", {"FY2025": 5050, "FY2024": 5344, "FY2023": 6806, "FY2022": 6646, "FY2021": 7438}),
    ("TOTAL", "Total operating income", {"FY2025": 157908, "FY2024": 163719, "FY2023": 121674, "FY2022": 117795, "FY2021": 70777}),
    ("DATA", "Credit impairment reversals / (charges) and other provisions", {"FY2025": 64, "FY2024": 306, "FY2023": -6669, "FY2022": 4188, "FY2021": 9753}),
    ("TOTAL", "Net operating income", {"FY2025": 157972, "FY2024": 164025, "FY2023": 115005, "FY2022": 121983, "FY2021": 80530}),
    ("SECTION", "Operating expenses", {}),
    ("DATA", "Staff costs", {"FY2025": -20143, "FY2024": -15973, "FY2023": -17838, "FY2022": -19576, "FY2021": -19475}),
    ("DATA", "General and administrative expenses", {"FY2025": -16306, "FY2024": -14730, "FY2023": -12211, "FY2022": -11842, "FY2021": -11634}),
    ("DATA", "Depreciation and impairment of property, plant and equipment", {"FY2025": -831, "FY2024": -852, "FY2023": -969, "FY2022": -1135, "FY2021": -1107}),
    ("DATA", "Amortisation and impairment of intangible assets", {"FY2024": -7, "FY2023": -30, "FY2022": -145, "FY2021": -169}),
    ("DATA", "Other operating expenses", {"FY2025": -525, "FY2024": -660, "FY2023": -432, "FY2022": -408, "FY2021": -668}),
    ("TOTAL", "Total operating expenses", {"FY2025": -37805, "FY2024": -32222, "FY2023": -31480, "FY2022": -33106, "FY2021": -33053}),
    ("TOTAL", "Profit before tax", {"FY2025": 120167, "FY2024": 131803, "FY2023": 83525, "FY2022": 88877, "FY2021": 47477}),
    ("DATA", "Income tax", {"FY2025": -30085, "FY2024": -32976, "FY2023": -20731, "FY2022": -16132, "FY2021": -4467}),
    ("TOTAL", "Profit for the year", {"FY2025": 90082, "FY2024": 98827, "FY2023": 62794, "FY2022": 72745, "FY2021": 43010}),
]

bw.add_income_statement_sheet(
    title="Itau BBA International plc — Income Statement (Bank, solo)",
    subtitle="Itau BBA International plc (Bank/solo basis, not Group), USD'000 unless stated",
    rows=income_statement_rows,
    sources_text=statement_sources(62, "2025", AR25_URL) + "\n\n"
        + statement_sources(54, "2023", AR23_URL, "Covers FY2023/FY2022.") + "\n\n"
        + statement_sources(53, "2021", AR21_URL, "Covers FY2021. FY2021's report structures "
            "Interest income/expense as single lines (no 'using effective interest rate method' sub-split "
            "shown from FY2022 onward) - both years' Net interest income tie exactly regardless."),
    first_col_width=76,
    source_height=170,
    unit_suffix=" (USD'000)",
)

# ---------------------------------------------------------------
# Sheet 3: Statement of Changes in Equity
# ---------------------------------------------------------------
equity_headers = ["Called-up share capital", "Share premium", "Revaluation reserves", "Other reserves", "Retained earnings", "Total equity"]
equity_rows = [
    ("TOTAL", "Balance as at 1 January 2021 (FY2020 closing, Bank)", (600000, None, 0, 332948, 370949, 1303897)),
    ("DATA", "Profit for the year", (None, None, None, None, 43010, 43010)),
    ("DATA", "Other comprehensive income for the year (cash flow hedge reserve)", (None, None, 53, None, None, 53)),
    ("DATA", "Dividend distribution", (None, None, None, None, -17086, -17086)),
    ("TOTAL", "Balance as at 31 December 2021 (source labels this row \"31 December 2020\" in the Bank's own "
             "equity statement - a genuine labelling error in the primary source, not a transcription error here; "
             "the movements above are unambiguously FY2021's own, and this closing total ties exactly to AR2023's "
             "own restated \"Balances at 1 January 2022\" row)", (600000, None, 53, 332948, 396873, 1329874)),
    ("DATA", "Profit for the year", (None, None, None, None, 72745, 72745)),
    ("DATA", "Other comprehensive income for the year (FVOCI reserves)", (None, None, -4029, None, None, -4029)),
    ("DATA", "Capitalisation of reserves and retained earnings", (335000, None, None, -332948, -2052, 0)),
    ("TOTAL", "Balance as at 31 December 2022 (per FY2023's own restated comparative)", (935000, None, -4029, 0, 467566, 1398537)),
    ("DATA", "Profit for the year", (None, None, None, None, 62794, 62794)),
    ("DATA", "Other comprehensive income for the year (FVOCI + cash flow hedge)", (None, None, 2385, None, None, 2385)),
    ("DATA", "Share capital increase", (286034, 213966, None, None, None, 500000)),
    ("TOTAL", "Balance as at 31 December 2023", (1221034, 213966, -1644, 0, 530360, 1963716)),
    ("DATA", "Profit for the year", (None, None, None, None, 98827, 98827)),
    ("DATA", "Other comprehensive income for the year (FVOCI + own credit + cash flow hedge)", (None, None, 371, None, None, 371)),
    ("TOTAL", "Balance as at 31 December 2024", (1221034, 213966, -1273, 0, 629187, 2062914)),
    ("DATA", "Profit for the year", (None, None, None, None, 90082, 90082)),
    ("DATA", "Other comprehensive income for the year (FVOCI + own credit + cash flow hedge)", (None, None, 1478, None, None, 1478)),
    ("TOTAL", "Balance as at 31 December 2025", (1221034, 213966, 205, 0, 719269, 2154474)),
]

bw.add_equity_changes_sheet(
    title="Itau BBA International plc — Statement of Changes in Equity (Bank, solo)",
    subtitle="Itau BBA International plc (Bank/solo basis, not Group), chronological roll-forward, USD'000",
    headers=equity_headers,
    rows=equity_rows,
    sources_text=statement_sources(64, "2025", AR25_URL) + "\n\n"
        + statement_sources(56, "2023", AR23_URL, "Covers FY2022/FY2023 movements.") + "\n\n"
        + statement_sources(55, "2021", AR21_URL, "Covers FY2021 movements. Reconciliation ladder confirmed: every "
            "year's own closing balance ties exactly to both the next year's own reported opening balance and "
            "that year's own Balance Sheet Total equity, with one exception reproduced as disclosed - the FY2021 "
            "Annual Report's own equity statement mislabels its final closing-balance row \"Balances at 31 "
            "December 2020\" (should read 2021; the movements above it are unambiguously FY2021's, and the "
            "closing total of USD 1,329,874k ties exactly to AR2023's own restated \"Balances at 1 January 2022\" "
            "row) - a genuine source-document labelling error, not a transcription error here."),
    first_col_width=70,
    source_height=190,
)

# ---------------------------------------------------------------
# Sheet 4: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Cash flows from operating activities", {}),
    ("DATA", "Profit before tax and dividends", {"FY2025": 120167, "FY2024": 131803, "FY2023": 83525, "FY2022": 68873, "FY2021": 23680}),
    ("DATA", "Credit impairment charges and other provisions", {"FY2025": -64, "FY2024": -306, "FY2023": 6669, "FY2022": -4188, "FY2021": -9753}),
    ("DATA", "Depreciation, amortisation and impairment of property, plant, equipment and intangibles", {"FY2025": 831, "FY2024": 852, "FY2023": 999, "FY2022": 1280, "FY2021": 1276}),
    ("DATA", "Other non-cash movements", {"FY2025": -104138, "FY2024": 31363, "FY2023": -33091, "FY2022": 9264, "FY2021": 1017}),
    ("DATA", "Trading assets and financial assets designated at fair value", {"FY2025": 124541, "FY2024": -213757, "FY2023": 501113, "FY2022": 629204, "FY2021": 156038}),
    ("DATA", "Loans and advances to banks", {"FY2025": 135096, "FY2024": -240931, "FY2023": 23043, "FY2022": -200127, "FY2021": 37815}),
    ("DATA", "Balances at central banks (mandatory reserves)", {"FY2021": 0}),
    ("DATA", "Loans and advances to customers", {"FY2025": 60053, "FY2024": -235192, "FY2023": -263283, "FY2022": -378299, "FY2021": -32696}),
    ("DATA", "Derivatives designated as hedging instruments (assets)", {"FY2025": 3103, "FY2024": -1190, "FY2023": 38012, "FY2022": -48100, "FY2021": -1705}),
    ("DATA", "Other operating assets", {"FY2025": 17431, "FY2024": 12645, "FY2023": 22312, "FY2022": -33257, "FY2021": 3638}),
    ("DATA", "Trading liabilities", {"FY2025": 71537, "FY2024": 178116, "FY2023": -113085, "FY2022": -37506, "FY2021": 56410}),
    ("DATA", "Financial liabilities designated at fair value", {"FY2025": -44456, "FY2024": -4802, "FY2023": 49259, "FY2022": -410, "FY2021": -1396}),
    ("DATA", "Deposits from banks", {"FY2025": 127432, "FY2024": -432800, "FY2023": 521131, "FY2022": -13577, "FY2021": -545052}),
    ("DATA", "Customer accounts", {"FY2025": -994100, "FY2024": 1035388, "FY2023": -204474, "FY2022": 162167, "FY2021": 509622}),
    ("DATA", "Debt securities in issue", {"FY2025": -259630, "FY2024": -75268, "FY2023": 314516, "FY2022": 802330, "FY2021": -8907}),
    ("DATA", "Derivatives designated as hedging instruments (liabilities)", {"FY2025": -4690, "FY2024": 1337, "FY2023": -10618, "FY2022": 27046, "FY2021": -8097}),
    ("DATA", "Other operating liabilities", {"FY2025": -45452, "FY2024": 46702, "FY2023": -16839, "FY2022": 8370, "FY2021": 4105}),
    ("TOTAL", "Net cash flow from operating activities before payment of income tax", {"FY2025": -792339, "FY2024": 233967, "FY2023": 919189, "FY2022": 993070, "FY2021": 185995}),
    ("DATA", "Income tax paid", {"FY2025": -30862, "FY2024": -31922, "FY2023": -22344, "FY2022": -15859, "FY2021": -2809}),
    ("TOTAL", "Net cash flow from operating activities", {"FY2025": -823201, "FY2024": 202045, "FY2023": 896845, "FY2022": 977211, "FY2021": 183186}),
    ("SECTION", "Cash flows from investing activities", {}),
    ("DATA", "Sales/(Purchases) of debt investments at amortised cost", {"FY2022": 2192, "FY2021": -2192}),
    ("DATA", "Purchases of financial assets measured at fair value through OCI", {"FY2025": 90366, "FY2024": 206101, "FY2023": -851115, "FY2022": -1180856}),
    ("DATA", "Sales/(Purchases) of subsidiaries", {"FY2025": -550, "FY2024": -55880, "FY2023": -65061, "FY2022": -10670, "FY2021": -45297}),
    ("DATA", "Dividends received", {"FY2024": 1, "FY2022": 20004, "FY2021": 8888}),
    ("DATA", "Purchases of intangible assets", {"FY2021": -61}),
    ("DATA", "Sales/(Purchases) of fixed assets", {"FY2025": -33, "FY2024": -33, "FY2023": -2406, "FY2022": -33, "FY2021": -2155}),
    ("TOTAL", "Net cash flow from investing activities", {"FY2025": 89783, "FY2024": 150189, "FY2023": -918582, "FY2022": -1169363, "FY2021": -40817}),
    ("SECTION", "Cash flows from financing activities", {}),
    ("DATA", "Leasing Contracts", {"FY2025": -862, "FY2024": -838, "FY2023": 1619, "FY2022": -926, "FY2021": 948}),
    ("DATA", "Share Capital Increase", {"FY2023": 500000}),
    ("TOTAL", "Net cash flow from financing activities", {"FY2025": -862, "FY2024": -838, "FY2023": 501619, "FY2022": -926, "FY2021": 948}),
    ("TOTAL", "Increase/(decrease) in cash and cash equivalents", {"FY2025": -734280, "FY2024": 351396, "FY2023": 479882, "FY2022": -193078, "FY2021": 143317}),
    ("DATA", "Cash and cash equivalents at beginning of year", {"FY2025": 1149307, "FY2024": 797911, "FY2023": 318029, "FY2022": 511107, "FY2021": 367790}),
    ("DATA", "Effects of exchange rate change on cash and cash equivalents", {"FY2025": 45560, "FY2024": 0, "FY2021": 0}),
    ("TOTAL", "Cash and cash equivalents at end of year", {"FY2025": 460587, "FY2024": 1149307, "FY2023": 797911, "FY2022": 318029, "FY2021": 511107}),
    ("SECTION", "Cash and cash equivalents comprise", {}),
    ("DATA", "Cash and balances at Central Banks", {"FY2025": 17, "FY2024": 16, "FY2023": 16, "FY2022": 15, "FY2021": 16}),
    ("DATA", "Loans and advances to banks with original maturity less than three months", {"FY2025": 460570, "FY2024": 1149291, "FY2023": 797895, "FY2022": 318014, "FY2021": 511091}),
    ("TOTAL", "Cash and cash equivalents at end of year", {"FY2025": 460587, "FY2024": 1149307, "FY2023": 797911, "FY2022": 318029, "FY2021": 511107}),
]

bw.add_cash_flow_sheet(
    title="Itau BBA International plc — Statement of Cash Flows (Bank, solo)",
    subtitle="Itau BBA International plc (Bank/solo basis, not Group), USD'000 unless stated",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=76,
    source_height=170,
    unit_suffix=" (USD'000)",
)

# ---------------------------------------------------------------
# Asset Quality
# ---------------------------------------------------------------
asset_quality_rows = [
    ("SECTION", "Loans and advances to customers, guarantees and commitments, by IFRS 9 stage", {}),
    ("DATA", "Stage 1 gross maximum exposure", {"FY2025": 4433270, "FY2024": 4784996, "FY2023": 4407196, "FY2022": 3926594, "FY2021": 3347695}),
    ("DATA", "Stage 1 ECL provisions", {"FY2025": -1071, "FY2024": -1135, "FY2023": -1441, "FY2022": -2657, "FY2021": -3212}),
    ("DATA", "Stage 1 cash collateral", {"FY2025": -850, "FY2024": -7303, "FY2023": -15535, "FY2022": -47791, "FY2021": -196179}),
    ("TOTAL", "Stage 1 net exposure", {"FY2025": 4431349, "FY2024": 4776558, "FY2023": 4390220, "FY2022": 3876146, "FY2021": 3148304}),
    ("DATA", "Stage 2 gross maximum exposure", {"FY2025": 38424, "FY2024": 41564, "FY2023": 15922, "FY2022": 152346, "FY2021": 249586}),
    ("DATA", "Stage 2 ECL provisions", {"FY2022": -32, "FY2021": -3665}),
    ("DATA", "Stage 2 cash collateral", {"FY2024": -5627}),
    ("TOTAL", "Stage 2 net exposure", {"FY2025": 38424, "FY2024": 35937, "FY2023": 15922, "FY2022": 152314, "FY2021": 245921}),
    ("DATA", "Stage 3 gross maximum exposure", {"FY2025": 91484}),
    ("DATA", "Stage 3 cash collateral", {"FY2025": -250}),
    ("TOTAL", "Stage 3 net exposure", {"FY2025": 91234}),
    ("TOTAL", "Total gross maximum exposure", {"FY2025": 4563178, "FY2024": 4826560, "FY2023": 4423118, "FY2022": 4078940, "FY2021": 3597281}),
    ("TOTAL", "Total ECL provisions", {"FY2025": -1071, "FY2024": -1135, "FY2023": -1441, "FY2022": -2689, "FY2021": -6877}),
    ("TOTAL", "Total cash collateral", {"FY2025": -1100, "FY2024": -12930, "FY2023": -15535, "FY2022": -47791, "FY2021": -196179}),
    ("TOTAL", "Total net exposure", {"FY2025": 4561007, "FY2024": 4812495, "FY2023": 4406142, "FY2022": 4028460, "FY2021": 3394225}),
]

bw.add_asset_quality_sheet(
    title="Itau BBA International plc — Asset Quality (Bank, solo)",
    subtitle="Itau BBA International plc (Bank/solo basis, not Group), USD'000 - covers loans and advances to "
             "customers PLUS off-balance-sheet guarantees and commitments (the Bank's own disclosed population "
             "for this note), not just the on-balance loan book, so totals will not tie exactly to the Balance "
             "Sheet's own 'Loans and advances to customers' line",
    rows=asset_quality_rows,
    sources_text=statement_sources(151, "2025", AR25_URL, "'Quality of the portfolio of Loans and advances to "
        "customers, guarantees and committments' table.") + "\n\n"
        + statement_sources(162, "2023", AR23_URL, "Covers FY2023/FY2022 (same table).") + "\n\n"
        + statement_sources(143, "2021", AR21_URL, "Covers FY2021 (same table; FY2020 comparative not used). "
            "As of every year end covered, the Bank had zero Stage 3 exposure except FY2025 (confirmed by reading "
            "each year's own note in full - not a gap, a genuine feature until FY2025's one impaired loan, "
            "covered by guarantees per the Bank's own disclosure)."),
    first_col_width=64,
    source_height=190,
    unit_suffix=" (USD'000)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, f"Group/consolidated basis, {unit}" if unit else "Group/consolidated basis",
                         rows_data, sources_text, note=note, first_col_width=48, source_height=150)

metric(
    "CET1 Capital", "USD m",
    [("Common equity tier 1 (CET1) capital", {"FY2025": 2276, "FY2024": 2073, "FY2023": 1939, "FY2022": 1334, "FY2021": 1318})],
    p3_sources(21, "2025", AR25_URL),
)

metric(
    "CET1 Ratio", "% of RWA",
    [("Common equity tier 1 ratio", {"FY2025": "29.0%", "FY2024": "23.9%", "FY2023": "27.0%", "FY2022": "19.6%", "FY2021": "22.6%"})],
    p3_sources(21, "2025", AR25_URL),
)

metric(
    "Tier 1 Capital", "USD m",
    [("Tier 1 capital", {"FY2023": 1939, "FY2022": 1334, "FY2021": 1318})],
    pillar3_disclosure_sources(),
    note="No distinct Tier 1 capital figure is broken out in the Annual Report's own 'Capital' section in any "
         "year (only 'Common equity tier 1 capital' and 'Total regulatory capital' are shown there — see the "
         "CET1 Capital and Total Capital sheets), but the standalone Pillar 3 Disclosures documents' Template UK "
         "KM1 table does disclose a distinct 'Tier 1 capital' line for FY2023/FY2022/FY2021 — identical to CET1 "
         "capital in every one of those years (Tier 2 capital is nil), confirming the earlier inference. "
         "FY2024/FY2025 remain blank — no Pillar 3 Disclosures document for either year was found this session.",
)

metric(
    "Tier 1 Ratio", "% of RWA",
    [("Tier 1 ratio", {"FY2023": "27.0%", "FY2022": "19.6%", "FY2021": "22.6%"})],
    pillar3_disclosure_sources(),
    note="Same basis as the Tier 1 Capital sheet — the Annual Report's own 'Capital' section does not break out "
         "a distinct Tier 1 ratio (see the CET1 Ratio and Total Capital Ratio sheets), but the standalone Pillar "
         "3 Disclosures documents' Template UK KM1 table discloses one directly for FY2023/FY2022/FY2021 — "
         "identical to the CET1 ratio and Total capital ratio in every one of those years. FY2024/FY2025 remain "
         "blank — no Pillar 3 Disclosures document for either year was found this session.",
)

metric(
    "Total Capital", "USD m",
    [("Total regulatory capital", {"FY2025": 2276, "FY2024": 2073, "FY2023": 1940, "FY2022": 1334, "FY2021": 1318})],
    p3_sources(21, "2025", AR25_URL),
)

metric(
    "Total Capital Ratio", "% of RWA",
    [("Total capital ratio", {"FY2025": "29.0%", "FY2024": "23.9%", "FY2023": "27.1%", "FY2022": "19.6%", "FY2021": "22.6%"})],
    p3_sources(21, "2025", AR25_URL),
)

metric(
    "Total RWAs", "USD m",
    [("Risk-weighted assets (RWA)", {"FY2025": 7855, "FY2024": 8660, "FY2023": 7170, "FY2022": 6812, "FY2021": 5836})],
    p3_sources(21, "2025", AR25_URL),
)

# ---------------------------------------------------------------
# RWA Breakdown
# ---------------------------------------------------------------
rwa_breakdown_rows = [
    ("DATA", "Credit Risk (Standardised Approach; incl. counterparty credit risk)", {"FY2025": 6987.5, "FY2024": 7875.0, "FY2023": 6525.0, "FY2022": 6250.0, "FY2021": 5362.5}),
    ("DATA", "Credit Valuation Adjustment Risk", {"FY2025": 62.5, "FY2024": 37.5, "FY2023": 25.0, "FY2022": 50.0, "FY2021": 25.0}),
    ("DATA", "Market Risk", {"FY2025": 12.5, "FY2024": 50.0, "FY2023": 62.5, "FY2022": 25.0, "FY2021": 25.0}),
    ("DATA", "Operational Risk (Basic Indicator Approach)", {"FY2025": 787.5, "FY2024": 700.0, "FY2023": 562.5, "FY2022": 487.5, "FY2021": 425.0}),
    ("TOTAL", "Total RWA (derived, sum of above)", {"FY2025": 7850.0, "FY2024": 8662.5, "FY2023": 7175.0, "FY2022": 6812.5, "FY2021": 5837.5}),
]

bw.add_rwa_breakdown_sheet(
    title="Itau BBA International plc — RWA Breakdown (Group)",
    subtitle="Group/consolidated basis, USD m - DERIVED, not directly disclosed as a UK OV1 table",
    rows=rwa_breakdown_rows,
    sources_text=(
        "Source — Itau BBA International plc Group 'Capital requirements By Risk Type' table (Note 41 'Capital "
        "Management'/'Capital requirements'), each year's own Annual Report — "
        f"FY2025/FY2024: 2025 Annual Report, p.170 — {AR25_URL}; "
        f"FY2023/FY2022: 2023 Annual Report, p.186 — {AR23_URL}; "
        f"FY2021: 2021 Annual Report, p.163 — {AR21_URL}.\n"
        "The Annual Report discloses capital REQUIREMENTS by risk type (Credit Risk, Credit Valuation Adjustment, "
        "Market Risk, Operational Risk), not RWA directly - each category's RWA here is derived by multiplying "
        "its capital requirement by 12.5 (the same 8% capital ratio convention the Bank's own 'Risk-weighted "
        "assets (RWA)' = 'Total capital requirements' x 12.5 footnote uses on the Total RWAs sheet, and "
        "independently confirmed against AR2021's own 'Risk-weighted assets - Credit Risk' table, p.164, which "
        "discloses Credit Risk RWA directly as USD 5,363m for FY2021 - ties to the derived USD 5,362.5m here "
        "exactly). No standalone Pillar 3 UK OV1 category-level table was found (the Annual Report states further "
        "Pillar 3 disclosures are published separately on www.itaubba.co.uk, which was unreachable this session, "
        "same constraint as the LCR/NSFR/MREL sheets). Each year's derived Total RWA is within ~USD 5m of the "
        "pre-existing Total RWas sheet's disclosed figure (a rounding artifact from the Bank's own capital "
        "requirement figures being rounded to the nearest USD 1m) - not force-reconciled to match exactly."
    ),
    first_col_width=64,
    source_height=200,
    unit_suffix=" (USD m)",
)

metric(
    "Leverage Ratio", "%",
    [("Leverage ratio", {"FY2025": "19.1%", "FY2024": "16.4%", "FY2023": "16.7%", "FY2022": "11.9%", "FY2021": "14.6%"})],
    p3_sources(21, "2025", AR25_URL, "The Leverage Ratio is quoted in the Capital section's narrative text (not the composition table) each year."),
)

metric(
    "LCR", "%",
    [("Liquidity Coverage Ratio", {"FY2023": "208%", "FY2022": "188%", "FY2021": "169%"})],
    pillar3_disclosure_sources(),
    note="Not found anywhere in the Annual Report's own pages (Strategic Report or Notes) — the Annual Report "
         "defers all liquidity Pillar 3 detail to the standalone Pillar 3 Disclosures documents. Those documents "
         "were located (via Wayback Machine, after itau.co.uk/itaubba.co.uk/live itau.com.br all proved "
         "unreachable) for FY2023/FY2022/FY2021, each disclosing LCR as a 12-month trailing average. "
         "FY2024/FY2025 remain blank — no Pillar 3 Disclosures document for either year was found this session.",
)

metric(
    "NSFR", "%",
    [("Net Stable Funding Ratio", {"FY2023": "161%", "FY2022": "150%"})],
    pillar3_disclosure_sources(),
    note="Same availability constraint as the LCR sheet — deferred by the Annual Report to the standalone Pillar "
         "3 Disclosures documents, located via Wayback Machine for FY2023/FY2022 (trailing four-quarter average). "
         "FY2021 is blank because NSFR was not yet subject to the PRA's reporting requirement (effective 1 "
         "January 2022, per both the FY2022 and FY2023 documents' own notes) — no NSFR % appears in the FY2021 "
         "document. FY2024/FY2025 remain blank — no Pillar 3 Disclosures document for either year was found this "
         "session.",
)

metric(
    "MREL Ratio", None,
    [("MREL ratio", {y: "Not publicly disclosed" for y in YEARS})],
    p3_sources(21, "2025", AR25_URL),
    note="No MREL ratio or resolution-strategy discussion was found in the Annual Report's own pages; deferred to "
         "the unreachable standalone Pillar 3 report, same as LCR/NSFR.",
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total Assets", {"FY2025": 7896227, "FY2024": 8937146, "FY2023": 8085575, "FY2022": 6981727, "FY2021": 5963514}),
        ("Loans and advances to customers", {"FY2025": 4044575, "FY2024": 4104314, "FY2023": 3868767, "FY2022": 3604470, "FY2021": 3221895}),
        ("Customer accounts", {"FY2025": 1740013, "FY2024": 2745061, "FY2023": 1709639, "FY2022": 1914084, "FY2021": 1751887}),
        ("Total Equity", {"FY2025": 2154474, "FY2024": 2062914, "FY2023": 1963716, "FY2022": 1398537, "FY2021": 1329874}),
    ],
    balance_sheet_unit="USD'000",
    income_statement_totals=[
        ("Total operating income", {"FY2025": 157908, "FY2024": 163719, "FY2023": 121674, "FY2022": 117795, "FY2021": 70777}),
        ("Total operating expenses", {"FY2025": -37805, "FY2024": -32222, "FY2023": -31480, "FY2022": -33106, "FY2021": -33053}),
        ("Profit for the year", {"FY2025": 90082, "FY2024": 98827, "FY2023": 62794, "FY2022": 72745, "FY2021": 43010}),
    ],
    income_statement_unit="USD'000",
    equity_changes_totals=[
        ("Opening equity", {"FY2025": 2062914, "FY2024": 1963716, "FY2023": 1398537, "FY2022": 1329874, "FY2021": 1303897}),
        ("Total comprehensive income for the year", {"FY2025": 91560, "FY2024": 99198, "FY2023": 65179, "FY2022": 68663, "FY2021": 43063}),
        ("Other equity movements, net", {"FY2025": 0, "FY2024": 0, "FY2023": 500000, "FY2022": 0, "FY2021": -17086}),
        ("Closing equity", {"FY2025": 2154474, "FY2024": 2062914, "FY2023": 1963716, "FY2022": 1398537, "FY2021": 1329874}),
    ],
    equity_changes_unit="USD'000",
    cash_flow_totals=[
        ("Net cash flow from operating activities", {"FY2025": -823201, "FY2024": 202045, "FY2023": 896845, "FY2022": 977211, "FY2021": 183186}),
        ("Net cash flow from investing activities", {"FY2025": 89783, "FY2024": 150189, "FY2023": -918582, "FY2022": -1169363, "FY2021": -40817}),
        ("Net cash flow from financing activities", {"FY2025": -862, "FY2024": -838, "FY2023": 501619, "FY2022": -926, "FY2021": 948}),
        ("Cash and cash equivalents at end of year", {"FY2025": 460587, "FY2024": 1149307, "FY2023": 797911, "FY2022": 318029, "FY2021": 511107}),
    ],
    cash_flow_unit="USD'000",
    ratios=[
        ("CET1 Ratio", {"FY2025": "29.0%", "FY2024": "23.9%", "FY2023": "27.0%", "FY2022": "19.6%", "FY2021": "22.6%"}),
        ("Total Capital Ratio", {"FY2025": "29.0%", "FY2024": "23.9%", "FY2023": "27.1%", "FY2022": "19.6%", "FY2021": "22.6%"}),
        ("Leverage Ratio", {"FY2025": "19.1%", "FY2024": "16.4%", "FY2023": "16.7%", "FY2022": "11.9%", "FY2021": "14.6%"}),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own source "
         "citation for the underlying document/page. Cash flow figures are Bank/solo basis; capital ratios are "
         "Group/consolidated basis (the only basis the Annual Report discloses for capital). Tier 1 Ratio, LCR and "
         "NSFR are omitted from this chart — each is only available for a subset of years (FY2023/FY2022/FY2021, "
         "and FY2023/FY2022 only for NSFR) via the standalone Pillar 3 Disclosures documents, not the full 5-year "
         "span this chart otherwise shows; see each metric's own sheet for the figures and detail.",
)

bw.save("/Users/armaan/code/katalysis/banks/ITAU BBA INTERNATIONAL FINANCIALS.xlsx")
