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
    "years. All figures below are in pounds (£), as reported."
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


def metric(name, unit, rows_data, note=None):
    bw.add_metric_sheet(name, unit, rows_data, p3_sources(), note=note, first_col_width=48, source_height=170)


metric("CET1 Capital", None, [("CET1 capital", {y: "Not publicly disclosed" for y in YEARS})])
metric("CET1 Ratio", "%", [("CET1 ratio", {"FY2025": "48%", "FY2024": "133%", "FY2023": "269%", "FY2022": "101.66%"})],
       note="The Annual Reports disclose this ratio as a Key Performance Indicator, but do not provide a separate Pillar 3/KM1 capital amount. No FY2021 ratio is disclosed.")
metric("Tier 1 Capital", None, [("Tier 1 capital", {y: "Not publicly disclosed" for y in YEARS})])
metric("Tier 1 Ratio", None, [("Tier 1 ratio", {y: "Not publicly disclosed" for y in YEARS})])
metric("Total Capital", None, [("Total capital", {y: "Not publicly disclosed" for y in YEARS})])
metric("Total Capital Ratio", None, [("Total capital ratio", {y: "Not publicly disclosed" for y in YEARS})])
metric("Total RWAs", None, [("Total risk-weighted assets", {y: "Not publicly disclosed" for y in YEARS})])

bw.add_rwa_breakdown_sheet(
    title="Perenna Bank PLC — RWA Breakdown",
    subtitle="Not publicly disclosed. £.",
    rows=[("DATA", "RWA breakdown by risk category", {y: "Not publicly disclosed" for y in YEARS})],
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
       note="The Annual Reports disclose this ratio as a Key Performance Indicator. No FY2021 ratio is disclosed.")
metric("LCR", None, [("Liquidity coverage ratio", {y: "Not publicly disclosed" for y in YEARS})])
metric("NSFR", None, [("Net stable funding ratio", {y: "Not publicly disclosed" for y in YEARS})])
metric("MREL Ratio", None, [("MREL ratio", {y: "Not publicly disclosed" for y in YEARS})])

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
