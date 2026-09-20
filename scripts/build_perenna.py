import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

# Perenna Bank PLC (Companies House 13084174, PRA FRN 956138) was incorporated
# as Perenna FFL PLC and renamed on 30 September 2022.  The five available
# year-end filings are 31 December 2021-2025.  The 2021-2023 filings are
# company-only accounts; the 2024-2025 filings include consolidated statements
# and the workbook uses those consolidated cash flows for the two later years.
YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]
YEAR_LABEL = {y: y for y in YEARS}

AR2025_URL = "https://find-and-update.company-information.service.gov.uk/company/13084174/filing-history/MzUyNTM5NTkxM2FkaXF6a2N4/document?format=pdf&download=0"
AR2024_URL = "https://find-and-update.company-information.service.gov.uk/company/13084174/filing-history/MzQ3MjEwNTk2M2FkaXF6a2N4/document?format=pdf&download=0"
AR2023_URL = "https://find-and-update.company-information.service.gov.uk/company/13084174/filing-history/MzQyNTQzMzk4MGFkaXF6a2N4/document?format=pdf&download=0"
AR2022_URL = "https://find-and-update.company-information.service.gov.uk/company/13084174/filing-history/MzM4MjAzMDY1OWFkaXF6a2N4/document?format=pdf&download=0"
AR2021_URL = "https://find-and-update.company-information.service.gov.uk/company/13084174/filing-history/MzM1MTg2MDczOWFkaXF6a2N4/document?format=pdf&download=0"

ENTITY_NOTE = (
    "ENTITY NOTE: Perenna Bank PLC (Companies House 13084174; PRA FRN 956138) was incorporated as "
    "Perenna FFL PLC and changed its legal name on 30 September 2022. This is the same legal entity, "
    "not a substituted group or predecessor. It received a restricted banking licence in August 2022 "
    "and a full banking licence in 2023. FY2021-FY2023 are company-only accounts; FY2024-FY2025 also "
    "present consolidated Group accounts, and the consolidated cash-flow statement is used for those "
    "years. All figures below are in pounds (£), as reported.\n\n"
    "FY2020 SELF-SKIP (whole year, re-verified 2026-09-06 per HD-061): Companies House confirms the "
    "company was incorporated on 16 December 2020 and did not receive its s761 Companies Act trading "
    "certificate (required for a public company to do business or borrow at all) until 9 July 2021. Its "
    "very first statutory accounts, filed 14 September 2022, cover the period from incorporation "
    "(16 December 2020) through 31 December 2021 - a single extended first accounting reference period, "
    "not two separate years. No FY2020-dated accounts, dormant-company accounts, or any other financial "
    "filing exists for this entity in Companies House's filing history (checked page by page across the "
    "full accounts-category history: Incorporation 16 Dec 2020 -> Trading Certificate 9 Jul 2021 -> "
    "Director appointments Jul 2021 -> Confirmation Statement 16 Dec 2021 -> first Full accounts, to "
    "31 Dec 2021, filed 14 Sep 2022 -> Memorandum/Resolutions Apr 2022). There is therefore no FY2020 "
    "financial year to extend into: the company had at most ~2 weeks of pre-trading-certificate corporate "
    "existence in calendar 2020, and the FY2021 column already is the entity's full first reporting "
    "period. This is a genuine whole-year self-skip, not an access gap - confirmed directly against the "
    "primary Companies House record, not assumed from the earlier scan."
)

DATA_QUALITY_NOTE = (
    "DATA QUALITY NOTE: The FY2024 and FY2025 reports contain an internal presentation/arithmetic "
    "inconsistency in the intermediate operating-cash subtotal labelled 'Cash used in operations'. "
    "The final reported net operating cash totals do reconcile to the full preceding line-item chain, "
    "so the intermediate subtotal is omitted rather than double-counted; all underlying line items and "
    "the final reported totals are transcribed as printed. FY2024's final net operating total is "
    "(£51,800,587), while FY2025's is (£62,911,585)."
)

STATEMENTS_PRESENTATION_NOTE = (
    "PRESENTATION NOTE: this entity's own reporting basis and statement format both change across the "
    "5 years. Basis: FY2021-FY2023 statements below are the Bank's own Company/standalone accounts "
    "(no Group existed yet); FY2024-FY2025 are the Consolidated Group accounts (matching the Cash Flow "
    "Statement sheet's existing basis convention). Format: FY2021's own originally-filed accounts used "
    "UK GAAP FRS 102 format (Fixed assets/Current assets, netted to 'Total assets less current "
    "liabilities', no explicit gross Total assets/Total liabilities line) - the Balance Sheet sheet's "
    "FY2021 column instead uses the Company's own IFRS-style restated comparative from the FY2022 "
    "Annual Report (Note: Statement of Financial Position, restated, p.27), which ties to the exact "
    "same closing equity figure as the FY2021 accounts' own FRS 102-format total - a presentation "
    "difference, not a substantive restatement. FY2021-FY2023's Profit & Loss uses a single aggregated "
    "'Administrative expenses' line; FY2024-FY2025 break this into Personnel expenses/Impairment losses/"
    "Depreciation and amortisation/Other expenses, and additionally structure income as 'Net revenue/"
    "(loss)' rather than a flat total. Both are reproduced exactly as each year's own report presents "
    "them, not forced into a single template.\n\n"
    "DATA QUALITY NOTE: two small (£1) source-level rounding artifacts exist between the FY2022 "
    "Balance Sheet's own reported Total equity/Retained earnings (£15,183,389 / £(16,194,183)) and the "
    "Statement of Changes in Equity's own reported closing balance for the same date (£15,183,390 / "
    "£(16,194,182)) - both figures are reproduced exactly as each source table itself shows them, not "
    "reconciled to a single value. Separately, AR2022's P&L shows a 'restated' FY2021 comparative loss "
    "of £(5,672,429) that does not match FY2021's own originally-filed accounts (£(5,797,708), which "
    "also ties to that year's own Balance Sheet retained earnings) - the P&L and Equity sheets both use "
    "FY2021's own originally-filed figure, not the later unexplained restatement."
)

CASH_FLOW_SOURCES = (
    "Sources - FY2021-FY2023 are Perenna Bank PLC's own company-only Statement of Cash Flows; "
    "FY2024-FY2025 are the consolidated Group Statement of Cash Flows:\n"
    f"FY2025: Group Annual Report and Financial Statements 2025, p.29-30 (Consolidated Statement of Cash Flows) - {AR2025_URL}\n"
    f"FY2024: Group Annual Report and Financial Statements 2024, p.32-33 (Consolidated Statement of Cash Flows) - {AR2024_URL}\n"
    f"FY2023: Annual Report and Financial Statements 2023, p.33-34 (Statement of Cash Flows) - {AR2023_URL}\n"
    f"FY2022: Annual Report and Financial Statements 2022, p.30-31 (Statement of Cash Flows; 2021 comparative is restated) - {AR2022_URL}\n"
    f"FY2021: Annual Report and Financial Statements 2021, p.14 (Statement of Cash Flows) - {AR2021_URL}\n"
    + ENTITY_NOTE + "\n\n" + DATA_QUALITY_NOTE
)


def p3_sources():
    return (
        "Sources - Perenna Bank PLC regulatory/key-metric disclosures:\n"
        f"FY2025 & FY2024: Group Annual Report and Financial Statements 2025, p.1 (Key Performance Indicators; "
        f"2025 and 2024 comparative) - {AR2025_URL}\n"
        f"FY2023 & FY2022: Annual Report and Financial Statements 2023, p.3 (Key performance indicators; "
        f"2023 and 2022 comparative) - {AR2023_URL}\n"
        "No separate Perenna Pillar 3/KM1 disclosure was located on the Bank's website or in its Companies "
        "House filings. The Annual Reports disclose only CET1 ratio and leverage ratio as named key metrics; "
        "the other fixed workbook metrics are therefore left explicitly not publicly disclosed.\n"
        "RE-VERIFIED 2026-09-12 (independent disclosure audit): the FY2025 Annual Report was re-downloaded "
        "from Companies House and OCR'd in full (76 pages, scanned/no text layer) - the only regulatory "
        "metrics anywhere in it are the two on the Key Metrics table, p.1: Leverage ratio 21.47% (2024: "
        "46.38%) and CET1 ratio 48% (2024: 133%), matching what this workbook already carries. A Wayback "
        "CDX search of perenna.com for any archived Pillar 3 or regulatory-disclosure PDF returned zero "
        "results, and the live site exposes no legal/regulatory document page (perenna.com/legal-and-"
        "regulatory returns HTTP 404; the homepage is JS-rendered and links only to /about). Confirmed a "
        "genuine non-disclosure rather than an access gap.\n"
        "MAXIMUM-EFFORT RE-SEARCH 2026-09-15 (prior 'unavailable' verdicts treated as unproven; rotated user "
        "agents, both curl and WebFetch). Four NEW routes were tried that no earlier pass had used, and all four "
        "are negative:\n"
        "  (1) perenna.com runs WordPress, so its REST media library was enumerated directly - "
        "/wp-json/wp/v2/media?mime_type=application/pdf and ?media_type=application both return an EMPTY ARRAY: "
        "the site hosts no PDF of any kind. Targeted searches (?search=pillar / disclosure / regulatory / "
        "prudential) likewise return nothing.\n"
        "  (2) A SIBLING HOST exists and was found and probed: static.perenna.com carries every Perenna PDF. A "
        "full Wayback CDX sweep of the domain WITHOUT a filter (1,095 archived URLs) lists 13 PDFs there - all "
        "product, broker, complaints and tariff documents; zero matches for pillar/disclos/regulat/capital/"
        "prudent across the entire archived URL set. Twelve Pillar 3 filename permutations were then probed "
        "live against static.perenna.com and ALL returned 404 against a known-good control "
        "(tariff_of_mortgage_charges.pdf, HTTP 200) - so the 404s are real absences, not a blanket block.\n"
        "  (3) perenna.com/legal and /regulatory both return HTTP 404, and the homepage's full link set (24 "
        "site paths) contains no regulatory or investor-relations page.\n"
        "  (4) The FY2024 Annual Report was downloaded from Companies House and OCR'd IN FULL for the first "
        "time (90 pages, scanned/no text layer, rendered at 200 dpi). The ONLY regulatory metrics anywhere in "
        "those 90 pages are the two KPI-table ratios on p.1 - Leverage Ratio 46.38% (2023: 91.97%) and CET1 "
        "Ratio 133% (2023: 269%) - which independently reproduce the four values this workbook already carries "
        "for FY2024/FY2023. No risk-weighted-asset figure, no capital amount, no LCR and no NSFR appears in any "
        "note, including the ALCo/capital-surplus discussion in the risk section.\n"
        "CONCLUSION: Perenna's non-disclosure is confirmed on much stronger evidence than before. The gap is "
        "genuine, not an access failure, and the Annual Report KPI table is the only source that will ever "
        "exist for these metrics.\n"
        "SDDT - CHECKED 2026-09-15 (cross-bank SDDT date-fit pass). This REPLACES the earlier closing remark "
        "here, which read 'Perenna is a small, recently-authorised specialist lender, consistent with the "
        "reduced Pillar 3 requirements for such firms'. That was an inference, not evidence, and it also blurred "
        "two different reliefs. Perenna does hold the Small Domestic Deposit Taker opt-in: the Bank of England "
        "consolidated list of waivers and modifications granted to PRA-authorised firms (downloaded 2026-09-15, "
        "https://www.bankofengland.co.uk/-/media/boe/files/prudential-regulation/authorisations/"
        "waivers-and-modifications-of-rules/consolidated-waivers-pra-firms.csv) carries one SDDT row for FRN "
        "956138, 'Perenna Bank PLC': 'Modification by Consent - PRA Rulebook - CRR Firms - Rule 3.1 of the SDDT "
        "Regime - General Application Part', sub rule 'Ru 3.1', waiver ref 'A00010865P.pdf', START DATE "
        "10/06/2025, no end date. Rule 3.1 is the operative opt-in and REMOVES the Pillar 3 disclosure "
        "obligation outright; Perenna holds no criteria-only rows (1.2 / 2.1(9) / 2.6) alongside it. Note that "
        "this is a different and stronger relief than the 'reduced requirements' the old wording gestured at - "
        "the Article 433b small-and-non-complex-institution route reduces disclosure to an annual subset, "
        "whereas Rule 3.1 removes it. The two must not be conflated.\n"
        "DATE FIT - IT DOES NOT FIT THE GAP YEAR. Perenna's accounting reference date is 31 DECEMBER, confirmed "
        "at Companies House (company 13084174, accounts filed to 31 December for 2021 through 2025). The "
        "outstanding gap year is FY2021, whose reporting period ran from incorporation on 16 December 2020 to 31 "
        "DECEMBER 2021 - three and a half years BEFORE the 10 June 2025 start date. A modification cannot "
        "explain a gap that predates it, so the SDDT regime explains NONE of the FY2021 blanks.\n"
        "FY2021's gap keeps its existing and entirely separate explanation, unchanged and in fact stronger than "
        "an exemption: Perenna held NO banking licence at all during that period - it received a restricted "
        "licence only in August 2022 and a full licence in 2023 - so no Pillar 3 obligation existed to be "
        "exempted from. Do not read SDDT back onto FY2021, or onto FY2022 and FY2023 either, both of which also "
        "predate 10 June 2025.\n"
        "What the modification DOES establish is forward-looking, and it is worth recording because it settles a "
        "question this note previously left open: from 10 June 2025 Perenna is an SDDT, so the standalone Pillar "
        "3/KM1 document searched for above will never be published for FY2025 or later, and the Annual Report "
        "KPI table will remain the only source for these metrics. A future session should not spend further "
        "effort hunting for one. Perenna does not state its SDDT status in its own words - the FY2025 Annual "
        "Report was OCR'd in full for the 2026-09-12 audit recorded above (76 scanned pages, no text layer) and "
        "the only regulatory metrics anywhere in it are the leverage and CET1 ratios already carried here. No "
        "Simplified Retail Deposit Ratio value is disclosed, so nothing replaces the NSFR series. This is the "
        "SDDT DISCLOSURE exemption, in force now - not the separate SDDT CAPITAL regime beginning 1 January "
        "2027.\n"
        + ENTITY_NOTE
    )


bw = BankWorkbook(bank_name="Perenna Bank PLC", years=YEARS, year_label=YEAR_LABEL, header_color="0F5B78")

STATEMENTS_SOURCES = (
    "Sources - Balance Sheet/Profit & Loss/Statement of Changes in Equity:\n"
    f"FY2025: Group Annual Report and Financial Statements 2025, p.24 (Consolidated statement of profit or "
    f"loss), p.25 (Consolidated statement of financial position), p.27 (Consolidated statement of changes "
    f"in equity) - {AR2025_URL}\n"
    f"FY2024: Group Annual Report and Financial Statements 2024, p.25 (Consolidated statement of profit or "
    f"loss), p.26 (Consolidated statement of financial position), p.30 (Consolidated statement of changes "
    f"in equity) - {AR2024_URL}\n"
    f"FY2023: Annual Report and Financial Statements 2023, p.29 (Statement of profit or loss), p.30-31 "
    f"(Statement of financial position), p.32 (Statement of changes in equity) - {AR2023_URL}\n"
    f"FY2022: Annual Report and Financial Statements 2022, p.25 (Statement of profit or loss), p.27 "
    f"(Statement of financial position, includes FY2021's own restated comparative), p.34 (Statement of "
    f"changes in equity, includes FY2021/FY2022 roll-forward) - {AR2022_URL}\n"
    f"FY2021: Annual Report and Financial Statements 2021 (Perenna FFL PLC), p.9 (Statement of "
    f"comprehensive income), p.12 (Statement of financial position), p.13 (Statement of changes in "
    f"equity) - {AR2021_URL}\n"
    + ENTITY_NOTE + "\n\n" + STATEMENTS_PRESENTATION_NOTE
)

balance_sheet_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and cash equivalents", {"FY2025": 15457063, "FY2024": 10649380, "FY2023": 11656289, "FY2022": 913033, "FY2021": 359627}),
    ("DATA", "Investments at FVTPL", {"FY2025": 4994700, "FY2024": 6438400, "FY2023": 32375738, "FY2022": 12887070}),
    ("DATA", "Derivative financial assets", {"FY2025": 2257365, "FY2024": 381420}),
    ("DATA", "Loans and advances to customers", {"FY2025": 85739558, "FY2024": 34827768, "FY2023": 108683}),
    ("DATA", "Property, plant and equipment", {"FY2025": 52176, "FY2024": 92038, "FY2023": 142768, "FY2022": 114442, "FY2021": 70764}),
    ("DATA", "Intangible assets", {"FY2025": 456697, "FY2024": 1798023, "FY2023": 2337685, "FY2022": 2153777, "FY2021": 1120614}),
    ("DATA", "Prepayments, accrued income and other assets", {"FY2025": 1591877, "FY2024": 1327462, "FY2023": 796865, "FY2022": 395789, "FY2021": 136084}),
    ("TOTAL", "Total assets", {"FY2025": 110549436, "FY2024": 55514491, "FY2023": 47418028, "FY2022": 16464111, "FY2021": 1687089}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Trade and other payables", {"FY2025": 7153448, "FY2024": 2622285, "FY2023": 2516439, "FY2022": 1280722, "FY2021": 7434797}),
    ("DATA", "Loans and borrowings", {"FY2025": 79583000, "FY2024": 24650000}),
    ("DATA", "Derivative financial liabilities", {"FY2025": 3045967, "FY2024": 381420}),
    ("TOTAL", "Total liabilities", {"FY2025": 89782415, "FY2024": 27653705, "FY2023": 2516439, "FY2022": 1280722, "FY2021": 7434797}),
    ("SECTION", "Equity", {}),
    ("DATA", "Called up share capital", {"FY2025": 203989, "FY2024": 91559, "FY2023": 90981, "FY2022": 70149, "FY2021": 50000}),
    ("DATA", "Share premium account", {"FY2025": 88779333, "FY2024": 77694013, "FY2023": 76413962, "FY2022": 31307423}),
    ("DATA", "Retained earnings/(accumulated losses)", {"FY2025": -68216301, "FY2024": -49924786, "FY2023": -31603354, "FY2022": -16194183, "FY2021": -5797708}),
    ("TOTAL", "Total equity", {"FY2025": 20767021, "FY2024": 27860786, "FY2023": 44901589, "FY2022": 15183389, "FY2021": -5747708}),
    ("TOTAL", "Total liabilities and equity", {"FY2025": 110549436, "FY2024": 55514491, "FY2023": 47418028, "FY2022": 16464111, "FY2021": 1687089}),
]

bw.add_balance_sheet_sheet(
    title="Perenna Bank PLC — Balance Sheet",
    subtitle="FY2021-FY2023 Company-only basis; FY2024-FY2025 consolidated Group basis; £; see source and presentation notes. Blank cells indicate that year's report did not disclose that specific line.",
    rows=balance_sheet_rows, sources_text=STATEMENTS_SOURCES, first_col_width=70, source_height=340, unit_suffix=" (£)",
)

income_statement_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Finance income", {"FY2025": 4106571, "FY2024": 1613480}),
    ("DATA", "Finance expense", {"FY2025": -3078579, "FY2024": -569951}),
    ("DATA", "Income from investment securities at amortised cost", {"FY2025": 199630, "FY2024": 618090}),
    ("DATA", "Net gains/(losses) from other financial instruments at FVTPL", {"FY2025": -1254779, "FY2024": -10467}),
    ("DATA", "Investment income", {"FY2023": 1038666, "FY2022": 93422}),
    ("DATA", "Fair value gains/(losses)", {"FY2023": 7778, "FY2022": -13541}),
    ("TOTAL", "Net revenue/(loss)", {"FY2025": -27157, "FY2024": 1651152}),
    ("DATA", "Administrative expenses", {"FY2023": -16474530, "FY2022": -10476355, "FY2021": -5797708}),
    ("DATA", "Personnel expenses", {"FY2025": -9190338, "FY2024": -11876208}),
    ("DATA", "Impairment losses on financial instruments", {"FY2025": -28134, "FY2024": -43769}),
    ("DATA", "Depreciation and amortisation", {"FY2025": -1525703, "FY2024": -1009005}),
    ("DATA", "Other expenses", {"FY2025": -7519883, "FY2024": -7043427}),
    ("TOTAL", "Loss before tax", {"FY2025": -18291215, "FY2024": -18321257, "FY2023": -15409172, "FY2022": -10396474, "FY2021": -5797708}),
    ("DATA", "Income tax (expense)/credit", {"FY2025": -300, "FY2024": -175, "FY2023": 0, "FY2022": 0, "FY2021": 0}),
    ("TOTAL", "Loss for the year/period", {"FY2025": -18291515, "FY2024": -18321432, "FY2023": -15409172, "FY2022": -10396474, "FY2021": -5797708}),
]

bw.add_income_statement_sheet(
    title="Perenna Bank PLC — Profit & Loss",
    subtitle="FY2021-FY2023 Company-only basis (single aggregated 'Administrative expenses' line, no OCI); FY2024-FY2025 consolidated Group basis (expanded expense lines); £; see source and presentation notes. There was no other comprehensive income in any year - Loss for the year equals Total comprehensive income/(loss) for the year throughout.",
    rows=income_statement_rows, sources_text=STATEMENTS_SOURCES, first_col_width=70, source_height=340, unit_suffix=" (£)",
)

equity_headers = ["Share capital", "Share premium", "Retained earnings", "Total equity"]
equity_rows = [
    ("DATA", "Loss for the period (FY2021)", (None, None, -5797708, -5797708)),
    ("DATA", "Shares issued during the period", (50000, None, None, 50000)),
    ("TOTAL", "At 31 December 2021 (FY2021 closing)", (50000, None, -5797708, -5747708)),
    ("DATA", "Loss for the year (FY2022)", (None, None, -10396474, -10396474)),
    ("DATA", "Issue of share capital (FY2022)", (20149, 31307423, None, 31327572)),
    ("TOTAL", "At 31 December 2022 (FY2022 closing)", (70149, 31307423, -16194182, 15183390)),
    ("DATA", "Loss for the year (FY2023)", (None, None, -15409172, -15409172)),
    ("DATA", "Issue of share capital (note 19)", (19726, 42830263, None, 42849989)),
    ("DATA", "Issue of share capital in relation to share options (note 19)", (1106, 2470859, None, 2471965)),
    ("DATA", "Transaction cost for share issuance", (None, -194583, None, -194583)),
    ("TOTAL", "At 31 December 2023 (FY2023 closing)", (90981, 76413962, -31603354, 44901589)),
    ("DATA", "Loss for the year (FY2024)", (None, None, -18321432, -18321432)),
    ("DATA", "Issue of share capital (note 23)", (578, 1290958, None, 1291536)),
    ("DATA", "Transaction cost for share issuance", (None, -10907, None, -10907)),
    ("TOTAL", "At 31 December 2024 (FY2024 closing)", (91559, 77694013, -49924786, 27860786)),
    ("DATA", "Loss for the year (FY2025)", (None, None, -18291515, -18291515)),
    ("DATA", "Issue of share capital (note 23)", (112430, 11130582, None, 11243012)),
    ("DATA", "Transaction cost for share issuance", (None, -45262, None, -45262)),
    ("TOTAL", "At 31 December 2025 (FY2025 closing)", (203989, 88779333, -68216301, 20767021)),
]

bw.add_equity_changes_sheet(
    title="Perenna Bank PLC — Statement of Changes in Equity",
    subtitle="Chronological roll-forward, oldest to newest, £. FY2021-FY2023 Company-only basis; FY2024-FY2025 consolidated Group basis. Equity reconciliation ladder confirmed: every year's own closing balance ties exactly to both the next year's own opening balance and that year's own Profit & Loss loss figure - zero undocumented plug rows across all 5 years. See the Balance Sheet sheet's data quality note for a £1 rounding difference between this sheet's FY2022 closing balance and the FY2022 Balance Sheet's own reported total.",
    headers=equity_headers, rows=equity_rows, sources_text=STATEMENTS_SOURCES, first_col_width=52, source_height=340,
)

rows = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Loss for the year/period", {"FY2025": -18291515, "FY2024": -18321432, "FY2023": -15409172, "FY2022": -10396474, "FY2021": -5797708}),
    ("DATA", "Depreciation of property, plant and equipment", {"FY2025": 55644, "FY2024": 82462, "FY2023": 64899, "FY2022": 43771, "FY2021": 14212}),
    ("DATA", "Amortisation of intangible fixed assets", {"FY2025": 826967, "FY2024": 926543, "FY2023": 226638, "FY2022": 10946}),
    ("DATA", "Impairment losses on intangible assets", {"FY2025": 643093, "FY2023": 18000}),
    ("DATA", "Interest received", {"FY2025": -555881, "FY2024": -28237}),
    ("DATA", "Interest paid", {"FY2025": 2796060, "FY2024": 445826}),
    ("DATA", "Fair value losses/(gain)", {"FY2025": 1254779, "FY2024": 10467, "FY2023": -7778, "FY2022": 13541}),
    ("DATA", "Investment income", {"FY2025": -199630, "FY2024": -618090, "FY2023": -386793, "FY2022": -93422}),
    ("DATA", "Investment income received", {"FY2022": 20529}),
    ("DATA", "Share-based payment expense", {"FY2024": 1291536, "FY2023": 2471965, "FY2022": 207333}),
    ("DATA", "Corporation tax charge", {"FY2025": 300, "FY2024": 175}),
    ("DATA", "Corporation tax paid", {"FY2025": -175}),
    ("DATA", "Impairment loss on loans and advances to customers", {"FY2024": 29621, "FY2023": 108}),
    ("DATA", "(Increase)/decrease in debtors", {"FY2021": -136084}),
    ("DATA", "Increase in creditors", {"FY2021": 581228}),
    ("DATA", "Increase in amounts owed to group companies", {"FY2021": 6853569}),
    ("DATA", "Increase in prepayments, accrued income and other assets", {"FY2025": -268941, "FY2024": -530597, "FY2023": -401076}),
    ("DATA", "Increase in trade and other payables", {"FY2025": 4535562, "FY2024": 105671, "FY2023": 1235718, "FY2022": 699493}),
    ("DATA", "Increase in loans and advances to customers", {"FY2025": -50911788, "FY2024": -34748706, "FY2023": -108791}),
    ("DATA", "Interest paid (cash flow movement)", {"FY2025": -2796060, "FY2024": -445826}),
    ("DATA", "Increase in trade and other receivables", {"FY2022": -259705}),
    ("TOTAL", "Net cash from/(used in) operating activities", {"FY2025": -62911585, "FY2024": -51800587, "FY2023": -12296282, "FY2022": -9753988, "FY2021": 1515217}),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Purchases of property, plant and equipment", {"FY2025": -15782, "FY2024": -31732, "FY2023": -93225, "FY2022": -87449, "FY2021": -84976}),
    ("DATA", "Purchase of intangible assets", {"FY2025": -128734, "FY2024": -386881, "FY2023": -428546, "FY2022": -1044109, "FY2021": -1120614}),
    ("DATA", "Sale/(purchases) of available-for-sale financial assets", {"FY2025": 1177153, "FY2024": 26544961, "FY2023": -19094097}),
    ("DATA", "Purchases of FVTPL investments", {"FY2022": -12807189}),
    ("DATA", "Investment income cash flow on maturity", {"FY2022": -20529}),
    ("DATA", "Interest received", {"FY2025": 555881, "FY2024": 28237}),
    ("TOTAL", "Net cash from/(used in) investing activities", {"FY2025": 1588518, "FY2024": 26154585, "FY2023": -19615868, "FY2022": -13959276, "FY2021": -1205590}),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Issue of ordinary shares", {"FY2025": 112430, "FY2023": 19726, "FY2022": 20149, "FY2021": 50000}),
    ("DATA", "Issue of ordinary shares at a premium", {"FY2025": 11130582, "FY2023": 42830263, "FY2022": 24453854}),
    ("DATA", "Transaction cost for share issuance", {"FY2025": -45262, "FY2024": -10907, "FY2023": -194583, "FY2022": -207333}),
    ("DATA", "Proceeds from loans and borrowings", {"FY2025": 54933000, "FY2024": 24650000}),
    ("TOTAL", "Net cash from/(used in) financing activities", {"FY2025": 66130750, "FY2024": 24639093, "FY2023": 42655406, "FY2022": 24266670, "FY2021": 50000}),
    ("TOTAL", "Net increase/(decrease) in cash and cash equivalents", {"FY2025": 4807683, "FY2024": -1006909, "FY2023": 10743256, "FY2022": 553406, "FY2021": 359627}),
    ("DATA", "Cash and cash equivalents at the beginning of year/period", {"FY2025": 10649380, "FY2024": 11656289, "FY2023": 913033, "FY2022": 359627}),
    ("TOTAL", "Cash and cash equivalents at the end of year/period", {"FY2025": 15457063, "FY2024": 10649380, "FY2023": 11656289, "FY2022": 913033, "FY2021": 359627}),
]

bw.add_cash_flow_sheet(
    title="Perenna Bank PLC — Statement of Cash Flows",
    subtitle="FY2021-FY2023 company-only; FY2024-FY2025 consolidated Group basis; £; see source and data-quality notes",
    rows=rows, sources_text=CASH_FLOW_SOURCES, first_col_width=70, source_height=250, unit_suffix=" (£)",
)


ASSET_QUALITY_SOURCES = (
    "Sources - Perenna Bank PLC Loans and advances to customers, IFRS 9 credit quality:\n"
    f"FY2025: Group Annual Report and Financial Statements 2025, p.54 (Note 16, Loans and advances to "
    f"customers), p.65-66 (Note 27.5, Credit quality analysis / overdue status / amounts arising from "
    f"ECL) - {AR2025_URL}\n"
    f"FY2024: Group Annual Report and Financial Statements 2024, p.62 (Note 16, Loans and advances to "
    f"customers) - {AR2024_URL}\n"
    f"FY2023: Annual Report and Financial Statements 2023, p.30 (Statement of financial position, Loans "
    f"and advances to customers) - {AR2023_URL}\n"
    + ENTITY_NOTE + "\n\n"
    "DATA QUALITY NOTE: FY2024's gross carrying amount is disclosed as £34,857,497 in Note 16 (loss "
    "allowance basis) but as £34,857,910 in the FY2025 report's own credit-quality-analysis/overdue-status "
    "tables (a £413 difference between two notes in different Annual Reports) - both figures are "
    "reproduced exactly as each source table shows them, not forced to match. No IFRS 9 stage split "
    "(Stage 1/2/3) is disclosed for FY2023, and no loan book existed at all in FY2021-FY2022 (the Bank's "
    "restricted licence period, before its first mortgage completions) - both are genuine absences, not "
    "access gaps."
)

asset_quality_rows = [
    ("SECTION", "Loans and advances to customers - gross carrying amount by IFRS 9 stage", {}),
    ("DATA", "Stage 1", {"FY2025": 83505753, "FY2024": 34857910}),
    ("DATA", "Stage 2", {"FY2025": 2262415}),
    ("DATA", "Stage 3", {"FY2025": 41030}),
    ("TOTAL", "Total gross carrying amount", {"FY2025": 85809197, "FY2024": 34857910, "FY2023": 108791}),
    ("SECTION", "Loss allowance (ECL) by IFRS 9 stage", {}),
    ("DATA", "Stage 1 ECL", {"FY2025": 41978, "FY2024": 30126, "FY2023": 108}),
    ("DATA", "Stage 2 ECL", {"FY2025": 26641}),
    ("DATA", "Stage 3 ECL", {"FY2025": 1019}),
    ("TOTAL", "Total loss allowance", {"FY2025": 69638, "FY2024": 30126, "FY2023": 108}),
    ("TOTAL", "Net loans and advances to customers", {"FY2025": 85739558, "FY2024": 34827768, "FY2023": 108683}),
    ("DATA", "ECL coverage ratio (loss allowance / gross carrying amount)", {"FY2025": "0.08%", "FY2024": "0.09%", "FY2023": "0.10%"}),
    ("DATA", "Stage 2 + Stage 3 as % of gross loans (early-warning/NPL proxy)", {"FY2025": "2.68%", "FY2024": "0.00%"}),
]

bw.add_asset_quality_sheet(
    title="Perenna Bank PLC — Asset Quality",
    subtitle="Group basis (mortgage lending only began under the Bank's full licence from FY2023). £. Blank cells indicate that year's report did not disclose that specific split; the Bank had no loan book at all in FY2021-FY2022.",
    rows=asset_quality_rows,
    sources_text=ASSET_QUALITY_SOURCES,
    first_col_width=76,
    source_height=280,
    unit_suffix=" (£)",
)


# FY2021 is marked explicitly rather than left blank. Perenna held no banking
# licence at all in that period - a restricted licence came only in August 2022
# and a full licence in 2023 - so no Pillar 3 obligation existed and no figure
# can ever be sourced. The reasoning was already written into the notes below,
# but the cells themselves were empty, which is indistinguishable from a year
# nobody had researched: a cross-bank coverage audit counted all ten as
# chaseable gaps. Matches build_vida.py and build_afin_bank.py.
PRE_LICENCE_YEARS = ["FY2021"]

# GA-020 (2026-09-19): every former bare "Not publicly disclosed" / "Not
# applicable" cell now states WHICH outcome it is and on what document. FY2022
# and FY2023 Annual Reports were OCR'd in full on 2026-09-19 (55 and 73 scanned
# pages) for this: their only regulatory metrics are the leverage and CET1
# ratios in the KPI list (FY2022 AR p.5; FY2023 AR printed p.3).
PRE_LICENCE_TEXT = ("Not applicable – no banking licence in the period to 31/12/2021: FY2021 accounts, Strategic "
                    "Report p.1, say Perenna was still applying for Part 4A permission (restricted licence Aug 2022)")
ND_BY_YEAR = {
    "FY2025": "Not published – FY2025 Annual Report (full OCR, 76pp) gives only CET1 and leverage ratios (KPI table "
              "p.1); no Pillar 3 exists (SDDT Rule 3.1 opt-in from 10/06/2025). See note.",
    "FY2024": "Not published – FY2024 Annual Report (full OCR, 90pp) gives only CET1 and leverage ratios (KPI table "
              "p.1); no Pillar 3 on perenna.com, static.perenna.com, Wayback or Companies House.",
    "FY2023": "Not published – FY2023 Annual Report (full OCR, 73pp) gives only CET1 and leverage ratios (KPIs, "
              "p.3); no Pillar 3 on perenna.com, static.perenna.com, Wayback or Companies House.",
    "FY2022": "Not published – FY2022 Annual Report (full OCR, 55pp) gives only CET1 and leverage ratios (KPIs, "
              "p.5); no Pillar 3 on perenna.com, static.perenna.com, Wayback or Companies House.",
    "FY2021": PRE_LICENCE_TEXT,
}


# ---------------------------------------------------------------
# KM1 Key Metrics - "Not applicable". Perenna has never published a Pillar 3
# disclosure of any kind, so there is no UK KM1 template to reproduce. This is
# an affirmative, evidenced non-disclosure, not a gap in our sourcing, and it
# is NOT back-filled from the statutory accounts (a different basis).
# ---------------------------------------------------------------
KM1_SOURCES = (
    "NOT APPLICABLE - Perenna Bank PLC publishes no Pillar 3 disclosure, and therefore no UK KM1 key-metrics "
    "template, for any year FY2021-FY2025. This is an evidenced absence, established on positive evidence and "
    "re-confirmed 2026-09-18, not an unchecked blank or a failed fetch.\n\n"
    "WHAT WAS CHECKED, AND WHAT EACH CHECK RETURNED:\n"
    "1. perenna.com runs WordPress, so its media library was enumerated directly through the REST API rather "
    "than by guessing filenames: /wp-json/wp/v2/media?mime_type=application/pdf returns an EMPTY ARRAY "
    "(re-run 2026-09-18). The site hosts no PDF of any kind. A keyword search endpoint "
    "(/wp-json/wp/v2/search?search=pillar) likewise returns an empty array.\n"
    "2. The site's own sitemap index (perenna.com/sitemap_index.xml, named in its robots.txt) lists a single "
    "page sitemap of 22 URLs. There is no investor-relations, regulatory-disclosures or legal page among them "
    "- the set is product, complaints, privacy, careers and help pages (re-checked 2026-09-18).\n"
    "3. A SIBLING HOST carrying every Perenna PDF was found and probed: static.perenna.com. A full Wayback CDX "
    "sweep of that domain (1,095 archived URLs) lists 13 PDFs, all product, broker, complaints and tariff "
    "documents, with zero matches for pillar/disclos/regulat/capital/prudent across the whole archived set. "
    "Live probes for Pillar 3 filename permutations all return HTTP 404 against a KNOWN-GOOD CONTROL on the "
    "same host (tariff_of_mortgage_charges.pdf, HTTP 200, re-confirmed 2026-09-18) - so the 404s are real "
    "absences on a reachable host, not a blanket block.\n"
    "4. The FY2024 and FY2025 Annual Reports were downloaded from Companies House and OCR'd IN FULL (90 and 76 "
    "scanned pages respectively, no text layer). The ONLY regulatory metrics anywhere in either document are "
    "the two ratios on the Key Performance Indicators table at p.1. No risk-weighted-asset figure, no capital "
    "amount, no LCR and no NSFR appears in any note.\n\n"
    "WHY THE DUTY DOES NOT APPLY GOING FORWARD, WITH THE DATE FIT STATED. The Bank of England's consolidated "
    "register of waivers and modifications granted to PRA-authorised firms carries one SDDT row for FRN 956138, "
    "'Perenna Bank PLC': 'Modification by Consent - PRA Rulebook - CRR Firms - Rule 3.1 of the SDDT Regime - "
    "General Application Part', waiver ref A00010865P.pdf, START DATE 10/06/2025, no end date. Rule 3.1 is the "
    "operative opt-in and REMOVES the Pillar 3 disclosure obligation outright (unlike rules 1.2, 2.1(9) and "
    "2.6, which modify the regime's ELIGIBILITY CRITERIA and remove no duty; Perenna holds none of those). "
    "DATE FIT: Perenna's accounting reference date is 31 December, so the 10 June 2025 start date falls inside "
    "FY2025 and explains that year forward. IT EXPLAINS NONE OF FY2021-FY2024, every one of which predates it "
    "- a modification cannot explain a gap that precedes it.\n\n"
    "FY2021-FY2023 HAVE A SEPARATE AND STRONGER EXPLANATION: Perenna held no banking licence during the period "
    "ended 31 December 2021 (restricted licence August 2022, full licence 2023), so no Pillar 3 obligation "
    "existed at all to be exempted from. FY2024 is the one year with a live duty and no located disclosure; "
    "the searches above are the evidence for that, and the Bank's small-and-non-complex status under Article "
    "433b reduces the required disclosure to an annual subset rather than removing it.\n\n"
    "CONSEQUENCE, RECORDED SO A LATER SESSION DOES NOT REPEAT THE SEARCH: from 10 June 2025 Perenna is an "
    "SDDT, so no standalone Pillar 3 or KM1 document will be published for FY2025 or later, and the Annual "
    "Report KPI table will remain the only source for this workbook's ratio sheets. The same evidence is why "
    "the RWA Breakdown sheet and most Pillar 3 metric sheets carry 'Not published –' statements: those are genuine "
    "non-disclosures by this bank, not omissions in this workbook.\n\n" + ENTITY_NOTE
)

bw.add_km1_sheet(
    title="Perenna Bank PLC — KM1 Key Metrics",
    subtitle="Not applicable — Perenna publishes no Pillar 3 disclosure of any kind, in any year, so there is "
             "no UK KM1 key-metrics template to reproduce. See the source note below for the searches that "
             "establish this and for the dated PRA modification that removes the duty from 10 June 2025. "
             "Nothing here is back-filled from the statutory accounts, which are a different basis.",
    rows=[
        ("DATA", "UK KM1 key-metrics template",
         {y: "No Pillar 3 disclosure published" for y in YEARS}),
    ],
    sources_text=KM1_SOURCES,
    first_col_width=48,
    source_height=460,
)


def metric(name, unit, rows_data, note=None):
    rows_data = [(label, {**{y: PRE_LICENCE_TEXT for y in PRE_LICENCE_YEARS}, **values})
                 for label, values in rows_data]
    bw.add_metric_sheet(name, unit, rows_data, p3_sources(), note=note, first_col_width=48, source_height=170)


metric("CET1 Capital", None, [("CET1 capital", dict(ND_BY_YEAR))])
metric("CET1 Ratio", "%", [("CET1 ratio", {"FY2025": "48%", "FY2024": "133%", "FY2023": "269%", "FY2022": "101.66%"})],
       note="The Annual Reports disclose this ratio as a Key Performance Indicator, but do not provide a "
            "separate Pillar 3/KM1 capital amount. FY2021 is blank for a STRUCTURAL reason, not a sourcing "
            "gap: Perenna did not hold a banking licence at all during that period (restricted licence "
            "granted August 2022, full licence 2023 - see the entity note), so no regulatory capital ratio "
            "existed to disclose for the period ended 31 December 2021. Re-verified 2026-09-12.")
metric("Tier 1 Capital", None, [("Tier 1 capital", dict(ND_BY_YEAR))])
metric("Tier 1 Ratio", None, [("Tier 1 ratio", dict(ND_BY_YEAR))])
metric("Total Capital", None, [("Total capital", dict(ND_BY_YEAR))])
metric("Total Capital Ratio", None, [("Total capital ratio", dict(ND_BY_YEAR))])
metric("Total RWAs", None, [("Total risk-weighted assets", dict(ND_BY_YEAR))])

bw.add_rwa_breakdown_sheet(
    title="Perenna Bank PLC — RWA Breakdown",
    subtitle="Not published by the bank - see the per-year statements and source note. £.",
    rows=[("DATA", "RWA breakdown by risk category", dict(ND_BY_YEAR))],
    sources_text=(
        "No separate Perenna Pillar 3/KM1 disclosure or category-level RWA breakdown was located on the "
        "Bank's website or in its Companies House filings (the full document was read through to its "
        "final note, including the credit risk, liquidity risk, and fair value measurement sections of "
        "Note 27, with no risk-weighted-asset figure of any kind disclosed) - confirmed as a genuine "
        "non-disclosure, not an access gap.\n" + ENTITY_NOTE
    ),
    first_col_width=48,
    source_height=170,
)

metric("Leverage Ratio", "%", [("Leverage ratio", {"FY2025": "21.47%", "FY2024": "46.38%", "FY2023": "91.97%", "FY2022": "91.05%"})],
       note="The Annual Reports disclose this ratio as a Key Performance Indicator. FY2021 is blank for the "
            "same STRUCTURAL reason as the CET1 Ratio sheet - the entity held no banking licence during the "
            "period ended 31 December 2021. Re-verified 2026-09-12.")
metric("LCR", None, [("Liquidity coverage ratio", dict(ND_BY_YEAR))])
metric("NSFR", None, [("Net stable funding ratio", dict(ND_BY_YEAR))])
metric("MREL Ratio", None, [("MREL ratio", dict(ND_BY_YEAR))])

bw.add_overview_sheet(
    cash_flow_totals=[
        ("Net cash from/(used in) operating activities", {"FY2025": -62911585, "FY2024": -51800587, "FY2023": -12296282, "FY2022": -9753988, "FY2021": 1515217}),
        ("Net cash from/(used in) investing activities", {"FY2025": 1588518, "FY2024": 26154585, "FY2023": -19615868, "FY2022": -13959276, "FY2021": -1205590}),
        ("Net cash from/(used in) financing activities", {"FY2025": 66130750, "FY2024": 24639093, "FY2023": 42655406, "FY2022": 24266670, "FY2021": 50000}),
        ("Cash and cash equivalents at end of year/period", {"FY2025": 15457063, "FY2024": 10649380, "FY2023": 11656289, "FY2022": 913033, "FY2021": 359627}),
    ],
    cash_flow_unit="£",
    balance_sheet_totals=[
        ("Total assets", {"FY2025": 110549436, "FY2024": 55514491, "FY2023": 47418028, "FY2022": 16464111, "FY2021": 1687089}),
        ("Loans and advances to customers", {"FY2025": 85739558, "FY2024": 34827768, "FY2023": 108683}),
        ("Total liabilities", {"FY2025": 89782415, "FY2024": 27653705, "FY2023": 2516439, "FY2022": 1280722, "FY2021": 7434797}),
        ("Total equity", {"FY2025": 20767021, "FY2024": 27860786, "FY2023": 44901589, "FY2022": 15183389, "FY2021": -5747708}),
    ],
    balance_sheet_unit="£",
    income_statement_totals=[
        ("Net revenue/(loss)", {"FY2025": -27157, "FY2024": 1651152}),
        ("Total operating/administrative expenses", {"FY2025": -18264058, "FY2024": -19972409, "FY2023": -16474530, "FY2022": -10476355, "FY2021": -5797708}),
        ("Loss before tax", {"FY2025": -18291215, "FY2024": -18321257, "FY2023": -15409172, "FY2022": -10396474, "FY2021": -5797708}),
        ("Loss for the year/period", {"FY2025": -18291515, "FY2024": -18321432, "FY2023": -15409172, "FY2022": -10396474, "FY2021": -5797708}),
    ],
    income_statement_unit="£",
    equity_changes_totals=[
        ("Opening equity", {"FY2025": 27860786, "FY2024": 44901589, "FY2023": 15183390, "FY2022": -5747708}),
        ("Loss for the year/period", {"FY2025": -18291515, "FY2024": -18321432, "FY2023": -15409172, "FY2022": -10396474, "FY2021": -5797708}),
        ("Other equity movements, net", {"FY2025": 11197750, "FY2024": 1280629, "FY2023": 45127371, "FY2022": 31327572, "FY2021": 50000}),
        ("Closing equity", {"FY2025": 20767021, "FY2024": 27860786, "FY2023": 44901589, "FY2022": 15183390, "FY2021": -5747708}),
    ],
    equity_changes_unit="£",
    ratios=[
        ("CET1 Ratio", {"FY2025": "48%", "FY2024": "133%", "FY2023": "269%", "FY2022": "101.66%"}),
        ("Leverage Ratio", {"FY2025": "21.47%", "FY2024": "46.38%", "FY2023": "91.97%", "FY2022": "91.05%"}),
    ],
    note="The ratio figures are the Annual Reports' named Key Performance Indicators, not a substitute Pillar 3/KM1 dataset. No FY2021 ratio was disclosed; other fixed workbook metrics are explicitly not publicly disclosed. Balance Sheet/P&L/Equity Changes summaries follow the same FY2021-FY2023 Company-only / FY2024-FY2025 consolidated Group basis split as those sheets themselves - see the Balance Sheet sheet's presentation note.",
)

bw.save("/Users/armaan/code/katalysis/banks/PERENNA FINANCIALS.xlsx")
