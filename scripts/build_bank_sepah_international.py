import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2026", "FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first, y/e 31 March
YEAR_LABEL = {y: y for y in YEARS}

AR2026_URL = "https://find-and-update.company-information.service.gov.uk/company/04189598/filing-history/MzU0NTE3NTc3MGFkaXF6a2N4/document?format=pdf&download=0"
AR2025_URL = "https://find-and-update.company-information.service.gov.uk/company/04189598/filing-history/MzQ3Mzg4ODM0MGFkaXF6a2N4/document?format=pdf&download=0"
AR2024_URL = "https://find-and-update.company-information.service.gov.uk/company/04189598/filing-history/MzQyOTk1Mjg2NmFkaXF6a2N4/document?format=pdf&download=0"
AR2022_URL = "https://find-and-update.company-information.service.gov.uk/company/04189598/filing-history/MzM1MTIwNTQ2MGFkaXF6a2N4/document?format=pdf&download=0"

ENTITY_NOTE = (
    "Bank Sepah International Plc (FRN 208019, company 04189598) is a wholly-owned UK subsidiary of Bank Sepah "
    "(Iran). Companies House status Active, accounts filed every year through FY2026 (y/e 31 March; the FY2026 "
    "accounts were approved 6 August 2026 and filed 16 September 2026), no insolvency/administration notices. "
    "The Managing Director's Statement in the FY2025 Annual "
    "Report (signed 27 June 2025) states 'there are currently no UN, EU or UK sanctions against Bank Sepah "
    "International Plc' as at that date, though US OFAC sanctions on Iranian entities since 2018 severely restrict "
    "its business (SWIFT access suspended Nov 2018) - this predates the UK 'snapback' sanctions on Iran-linked "
    "entities that took effect 29 September 2025 (which affected Bank Saderat Plc, built earlier in this project); "
    "the FY2025 accounts do not reflect any post-September-2025 development. The FY2026 Annual Report's Managing "
    "Director's Statement (p.2) states the Bank 'was placed under sanctions by the UK Government and the United "
    "Nations (UN) on the 28 September 2025 in the form of a complete asset freeze', operating since then only "
    "under OFSI licences; its Statement of Cash Flows (p.27) adds 'All the above balances are restricted being "
    "subject to direct sanctions'. FY2026 is therefore the first year in this workbook affected by the freeze. "
    "Does NOT take "
    "the FRS 101/102 cash-flow exemption - full Statement of Cash Flows every year. Reports in EUR (majority of "
    "assets/liabilities are Euro-denominated per the Strategic Report), converted to GBP here for consistency with "
    "every other workbook in this project."
)

# GBP/EUR conversion rates as disclosed in the Bank's own FY2025 Annual Report's 5-year "Performance Summary" table
# (Strategic Report, p.5) - "Year-end exchange rate - EURO/GBP" and "Average exchange rate - EURO/GBP", i.e. GBP per
# EUR 1. Used directly rather than re-derived from Bank of England data, since the entity discloses its own rates.
YEAR_END_RATE = {"FY2026": 0.8683, "FY2025": 0.8354, "FY2024": 0.8548, "FY2023": 0.8782, "FY2022": 0.8459, "FY2021": 0.8520}
AVG_RATE = {"FY2026": 0.8653, "FY2025": 0.8418, "FY2024": 0.8636, "FY2023": 0.8645, "FY2022": 0.8366, "FY2021": 0.8911}
FX_NOTE = (
    "FX conversion methodology: point-in-time/balance figures (capital, RWA, cash balances) converted at the "
    "Bank's own disclosed EUR/GBP year-end rate; cash-flow figures converted at its own disclosed EUR/GBP average "
    "rate (both from the FY2025 Annual Report's 5-year Performance Summary table, p.5; the FY2026 rates, "
    "0.8683 year-end and 0.8653 average, from the FY2026 Annual Report's same table, p.5, which reprints the "
    "FY2025/FY2024/FY2023 rates identically). Ratios are not converted "
    "(dimensionless). The 'Effect of GBP/EUR translation' line in the Cash Flow Statement is computed "
    "programmatically from the actual converted figures (opening + net change + entity's own FX line + this plug = "
    "closing, exactly) - see this project's established FX conversion methodology (first used for SMBC Bank "
    "International plc)."
)

CASH_FLOW_SOURCES = (
    "Sources - Bank Sepah International Plc's own Statement of Cash Flows (Companies House filings):\n"
    f"FY2026: Full accounts to 31 March 2026 (filed 16 Sep 2026), p.27 - {AR2026_URL}\n"
    f"FY2025/FY2024: Full accounts to 31 March 2025, p.28 - {AR2025_URL}\n"
    f"FY2023: Full accounts to 31 March 2024's own FY2023 comparative column, p.30 - {AR2024_URL}\n"
    f"FY2022/FY2021: Full accounts to 31 March 2022, p.26 - {AR2022_URL}\n"
    "All 4 filings are fully scanned/image-only (0 text blocks/page) - rendered and read visually, cross-checked "
    "where years overlap between filings (FY2024 figures match exactly between the FY2024 and FY2025 accounts; "
    "FY2025's operating/investing/net change/FX/opening/closing figures match exactly between the FY2025 and "
    "FY2026 accounts).\n"
    + ENTITY_NOTE + "\n" + FX_NOTE
)


def p3_sources():
    return (
        "Sources - Bank Sepah International Plc's own 'Performance Summary' 5-year table, Strategic Report p.5, "
        f"FY2025 Annual Report - {AR2025_URL}; FY2026 from the same table in the FY2026 Annual Report "
        f"(full accounts to 31 March 2026, filed at Companies House 16 Sep 2026), p.5 - {AR2026_URL} (Total "
        "capital resources EUR172m; 'Total capital to total risk- weighted assets' and 'Tier 1 capital to total "
        "risk- weighted assets' both printed as 85%, with no decimal place, where FY2022-FY2025 carry one; p.6 "
        "gives Tier 1 capital as EUR171.7m). CET1 = Tier 1 = Total Capital every year (no AT1/Tier 2 instruments "
        "mentioned; the Bank discloses a single 'Total capital to total risk-weighted assets' ratio, identical to "
        "'Tier 1 capital to total risk-weighted assets' every year). No leverage ratio, LCR, NSFR or MREL figure "
        "appears in the Annual Report itself - those are disclosed instead in the Bank's own Pillar 3 Disclosures "
        "documents, published separately at www.banksepah.co.uk/information. That site's TLS certificate has "
        "EXPIRED, so browsers refuse the connection outright and a default command-line fetch fails with no "
        "HTTP status at all - this is a certificate-date problem, NOT a dead link, and the documents are "
        "retrieved perfectly well with certificate validation bypassed (see the expired-certificate note "
        "below). See the Leverage Ratio / LCR / NSFR sheets' own citations for the exact PDFs and pages used. "
        "No MREL figure was found in either source (see that sheet's own note).\n" + FX_NOTE
        + "\n\n" + P3_FETCH_NOTE
    )


# FY2026 (31 March 2026) Pillar 3: NOT PUBLISHED YET at 2026-09-19. Routes tried that day:
# (1) https://www.banksepah.co.uk/information (curl -k --http1.1, HTTP 200, 9,252 bytes) links Pillar 3
#     editions for March 2023, 2024 and 2025 only; (2) seven FY2026 variants of the three filename patterns
#     (Pillar3Disclosureasat31March2026, Pillar3Disclosuresasat31March2026, Pillar_3_Disclosures_31_March_2026,
#     Pillar-3-Disclosures-31-March-2026, ...) all 404, while the positive control (the March 2025 URL, same
#     flags) returned 200 / application/pdf / %PDF / 619,903 bytes; (3) Wayback CDX for
#     banksepah.co.uk/uploads/documents/* from 2026 returns only the March 2025 PDF.
P3_2026_PENDING = (
    "Not published yet – the 31 March 2026 Pillar 3 is not on banksepah.co.uk/information at 2026-09-19 "
    "(newest listed: March 2025). The Bank publishes it after the audit (2025 ed. p.6); the 2025 PDF is dated "
    "1 Jul 2025, days after those accounts were signed. The FY2026 accounts were approved 6 Aug 2026 and filed "
    "16 Sep 2026, so it is due now; the Bank has been under a UK/UN asset freeze since 28 Sep 2025 (AR2026 p.2)"
)
P3_2025_URL = "https://www.banksepah.co.uk/uploads/documents/Pillar3Disclosureasat31March2025.pdf"
P3_2024_URL = "https://www.banksepah.co.uk/uploads/documents/Pillar3Disclosuresasat31March2024.pdf"
P3_2023_URL = "https://www.banksepah.co.uk/uploads/documents/Pillar_3_Disclosures_31_March_2023.pdf"
P3_2022_URL = "https://www.banksepah.co.uk/uploads/documents/Pillar_3_Disclosures_31_March_2022.pdf"
P3_2021_URL = "https://www.banksepah.co.uk/uploads/documents/Pillar-3-Disclosures-31-March-2021.pdf"

P3_FETCH_NOTE = (
    "The Bank's own Pillar 3 Disclosures documents are published at www.banksepah.co.uk/information, a site "
    "whose TLS certificate has expired (a normal browser or fetch refuses the connection outright). The "
    "documents were successfully retrieved on 2026-09-04 via curl with the -k/--insecure flag (bypassing "
    "certificate validation) and a spoofed Chrome user-agent - the PDFs are genuine, digitally-produced (not "
    "scanned) Pillar 3 reports bearing the Bank's own branding, each headed 'BANK SEPAH INTERNATIONAL plc / "
    "PILLAR 3 DISCLOSURES' and dated for its own year-end.\n\n"
    + "EXPIRED CERTIFICATE - NOT A DEAD LINK. READ THIS BEFORE 'FIXING' ANY banksepah.co.uk URL.\n"
    "A browser opening any of the five Pillar 3 URLs below will show a full-page security warning, and a "
    "default command-line fetch will fail outright with no HTTP status at all (curl reports exit 60 / "
    "'SSL certificate problem: certificate has expired', and prints status 000 - NOT a 404). That failure is "
    "a certificate-date problem on the Bank's server. It is NOT link rot, the files are NOT missing, and NO "
    "URL here needs re-pointing. Do not delete, replace or Wayback-substitute these URLs on the strength of a "
    "certificate warning.\n"
    "CERTIFICATE AS INSPECTED 16 September 2026 (openssl s_client + x509): subject CN=banksepah.co.uk; issuer "
    "'ZeroSSL RSA Domain Secure Site CA' (C=AT, O=ZeroSSL); notBefore 25 Jun 2025, notAfter 25 Jun 2026 - i.e. "
    "expired 83 days before this check. Subject Alternative Names are DNS:banksepah.co.uk and "
    "DNS:www.banksepah.co.uk, so the hostname actually matches and EXPIRY IS THE ONLY DEFECT: the certificate "
    "is the right certificate for the right host, merely out of date. There is no hostname mismatch, no "
    "self-signed certificate and no untrusted root, so the documents are genuinely being served by the Bank's "
    "own domain and can be trusted as primary sources.\n"
    "HOW TO RE-FETCH: add curl's -k/--insecure flag (or the equivalent certificate-validation bypass). "
    "RE-VERIFIED 16 September 2026 - all five Pillar 3 URLs returned HTTP 200 with %PDF magic bytes (checked "
    "as magic bytes, not merely a 200 status), at these sizes and page counts: 31 March 2025, 619,903 bytes, "
    "31 pages; 31 March 2024, 929,132 bytes, 31 pages; 31 March 2023, 613,571 bytes, 32 pages; 31 March 2022, "
    "654,861 bytes, 32 pages; 31 March 2021, 644,221 bytes, 32 pages. Covers re-read and all are headed 'BANK "
    "SEPAH INTERNATIONAL plc / PILLAR 3 DISCLOSURES'. The three Companies House filing-history URLs used "
    "elsewhere in this workbook are on a different host, are unaffected, and were re-checked the same day "
    "(HTTP 200, %PDF).\n"
    "If the Bank renews the certificate, plain HTTPS will simply start working again and nothing in this "
    "script needs to change."
)


def liquidity_leverage_sources():
    return (
        "FY2026: the March 2026 Pillar 3 is not published yet (see the statement in the FY2026 cells and the "
        "KM1 Key Metrics sheet's note). The LCR sheet's FY2026 figure, 1310%, is instead from the FY2026 Annual "
        "Report (full accounts to 31 March 2026, filed 16 Sep 2026), Strategic Report 'Liquidity' paragraph, "
        f"p.6 - {AR2026_URL} - which prints 'The LCR at the year-end was 1310% (2025 2034%)'; its 2025 "
        "comparative agrees with the March 2025 Pillar 3's own Table 1. That report prints no leverage ratio "
        "or NSFR.\n\n"
        "Sources - Bank Sepah International Plc's own Pillar 3 Disclosures documents, Table 1 'Summary of Key "
        "Metrics' (each report's own p.5):\n"
        f"FY2025 ('Mar 25' column): Pillar 3 Disclosures as at 31 March 2025, p.5 - {P3_2025_URL}\n"
        f"FY2024 ('Mar 24' column): Pillar 3 Disclosures as at 31 March 2024, p.5 - {P3_2024_URL}\n"
        f"FY2023 ('Mar 23' column): Pillar 3 Disclosures 31 March 2023, p.5 - {P3_2023_URL}\n"
        f"FY2022 ('Mar 22' column): Pillar 3 Disclosures 31 March 2022, pp.5/16 - {P3_2022_URL}\n"
        f"FY2021: Bank's own Pillar 3 Disclosures 31 March 2021, pp.5/16 - {P3_2021_URL}\n\n"
        "Each year's own report's own year-end column is used in preference to a later report's comparative "
        "column for the same date, where both exist - the two occasionally differ by a rounding point (e.g. "
        "NSFR at March 2022: 458% in the March-2022 report's own column vs 459% in the March-2023 report's "
        "comparative column); both are the Bank's own figures, not reconciled, immaterial.\n\n"
        + P3_FETCH_NOTE
    )


bw = BankWorkbook(bank_name="Bank Sepah International Plc", years=YEARS, year_label=YEAR_LABEL, header_color="444444")

# ---------------------------------------------------------------
# ST- rollout (batch ST-013): Balance Sheet, P&L, Statement of Changes in
# Equity, Asset Quality, RWA Breakdown. Sourced from the same 3 scanned
# Companies House filings already cited above (AR2025_URL/AR2024_URL/
# AR2022_URL) - transcribed via pdf_tools.py render + visual read.
# ---------------------------------------------------------------
def gbp_spot(eur_by_year):
    """Convert a {year: EUR '000} dict to £'000 using that year's own year-end spot rate (stocks)."""
    return {y: round(v * YEAR_END_RATE[y], 1) for y, v in eur_by_year.items()}


def gbp_avg(eur_by_year):
    """Convert a {year: EUR '000} dict to £'000 using that year's own average rate (flows)."""
    return {y: round(v * AVG_RATE[y], 1) for y, v in eur_by_year.items()}


STATEMENTS_SOURCES = (
    "Sources - Bank Sepah International Plc's own Statement of Comprehensive Income / Statement of Financial "
    "Position / Statement of Changes in Equity, converted from EUR to GBP (see FX conversion note below):\n"
    f"FY2026: Full accounts to 31 March 2026 (filed 16 Sep 2026), Statement of Comprehensive Income p.24, "
    f"Statement of Financial Position p.25, Statement of Changes in Equity p.26 - {AR2026_URL}\n"
    f"FY2025/FY2024: Full accounts to 31 March 2025, pp.25-27 - {AR2025_URL}\n"
    f"FY2023: Full accounts to 31 March 2024's own FY2023 comparative column, pp.27-29 - {AR2024_URL}\n"
    f"FY2022/FY2021: Full accounts to 31 March 2022, pp.23-25 - {AR2022_URL}\n\n"
    + ENTITY_NOTE + "\n\n" + FX_NOTE
)

PRESENTATION_NOTE = (
    "PRESENTATION NOTE: FY2025 introduces a new 'Restricted cash and cash equivalents' line (EUR989k, note 9) not "
    "present in any earlier year - not merged into ordinary Cash and cash equivalents, since the source treats it "
    "as a distinct balance. FY2023-25 split 'Deposits from Banks' between Current (small) and Non-Current "
    "(EUR130,000k, a stable long-term funding line) - FY2021/22's own statements show this entirely within Current "
    "liabilities (no non-current split disclosed that far back), reproduced as disclosed rather than reclassified. "
    "Similarly, 'Debt instruments' only splits into current/non-current portions from FY2022 onward. A EUR1k "
    "rounding gap exists between the FY2022 Annual Report's own Statement of Financial Position (retained earnings "
    "EUR9,065k at 31 March 2021) and its own Statement of Changes in Equity (EUR9,064k for the same date) - both "
    "figures are the Bank's own, immaterial, not adjusted; the equity statement's own figure is used on that sheet "
    "for internal consistency, the balance sheet's own figure on this one.\n\n"
    "FY2026 PRESENTATION CHANGE: the FY2026 edition (p.25) presents the Statement of Financial Position 'in "
    "order of liquidity', with NO current/non-current split for any asset or liability, and states that 'the "
    "comparative information for the prior year has been reclassified' to match. FY2026 is therefore shown in "
    "its own block at the top of the Balance Sheet sheet, in the edition's own line order, and is NOT forced "
    "into the current/non-current rows below, which keep FY2021-FY2025 exactly as each year's own edition "
    "printed them. The reclassified FY2025 comparative is not used (FY2025 comes from its own edition; e.g. "
    "the FY2026 edition's FY2025 'Cash and cash equivalents' of EUR147,796k is the FY2025 edition's EUR146,807k "
    "plus its separate EUR989k 'Restricted cash', and its FY2025 'Deposits from banks' of EUR137,722k is the "
    "current EUR7,722k plus non-current EUR130,000k). Total assets (EUR315,169k), Total liabilities "
    "(EUR142,390k) and every equity line for FY2025 are identical in both editions. The equity rows at the "
    "bottom are common to both presentations and carry FY2026 too. In EUR the FY2026 edition foots exactly "
    "(assets sum to 316,225; liabilities to 144,455; 144,455 + 171,770 = 316,225). Because each line is converted "
    "at 0.8683 and rounded to £0.1k on its own, the converted FY2026 asset lines sum to £274,577.9k against a "
    "converted total of £274,578.2k, and the liability lines to £125,430.2k against £125,430.3k - conversion "
    "rounding, not a difference in the source.\n\n"
    "FY2026 PROFIT & LOSS: the FY2026 edition (p.24) inserts an 'Operating Profit' subtotal (EUR601k; FY2025 "
    "comparative EUR909k) between General administrative expenses and Credit impairment; no earlier edition "
    "prints it and it is not added as a row here. Its 'Other Comprehensive Income' line is printed as a dash "
    "for FY2026, reproduced as '-' (the FY2021-FY2025 cells carry 0 as originally built and were not re-read "
    "for their glyph in this pass)."
)

# ---------------------------------------------------------------
# Balance Sheet (EUR '000, raw units - converted at each year's own year-end spot rate)
# ---------------------------------------------------------------
BS_RESTRICTED_CASH = {"FY2025": 989}
BS_PLACEMENTS_BANKS_NC = {"FY2025": 9914, "FY2024": 9230, "FY2023": 8731, "FY2022": 8729, "FY2021": 8732}
BS_PROPERTY_EQUIPMENT = {"FY2025": 2570, "FY2024": 2602, "FY2023": 2153, "FY2022": 2180, "FY2021": 2206}
BS_INTANGIBLE = {"FY2025": 434, "FY2024": 574, "FY2023": 588, "FY2022": 789, "FY2021": 1083}
BS_DEBT_INSTR_NC = {"FY2025": 9647, "FY2024": 15913, "FY2023": 15403, "FY2022": 17799, "FY2021": 17470}
BS_TOTAL_NC = {"FY2025": 23554, "FY2024": 28319, "FY2023": 26875, "FY2022": 29497, "FY2021": 29491}

BS_CASH = {"FY2025": 146807, "FY2024": 154198, "FY2023": 152835, "FY2022": 204262, "FY2021": 187011}
BS_PLACEMENTS_BANKS_C = {"FY2025": 127292, "FY2024": 118578, "FY2023": 94363, "FY2022": 94327, "FY2021": 132926}
BS_LOANS_CUSTOMERS = {"FY2026": 510, "FY2025": 399, "FY2024": 479, "FY2023": 28101, "FY2022": 29024, "FY2021": 2900}
BS_OTHER_ASSETS = {"FY2025": 6928, "FY2024": 6597, "FY2023": 7586, "FY2022": 6434, "FY2021": 6564}
BS_DEBT_INSTR_C = {"FY2025": 8572, "FY2024": 3621, "FY2023": 2570}
BS_PREPAYMENTS = {"FY2025": 1617, "FY2024": 1684, "FY2023": 1488, "FY2022": 555, "FY2021": 877}
BS_TOTAL_ASSETS = {"FY2026": 316225, "FY2025": 315169, "FY2024": 313476, "FY2023": 313818, "FY2022": 364099, "FY2021": 359769}

BS_DEPOSITS_BANKS_C = {"FY2025": 7722, "FY2024": 7726, "FY2023": 7696, "FY2022": 187584, "FY2021": 187346}
BS_DEPOSITORS = {"FY2026": 1930, "FY2025": 1958, "FY2024": 2041, "FY2023": 1978, "FY2022": 2063, "FY2021": 2036}
BS_CORP_TAX = {"FY2025": 225, "FY2023": 225, "FY2022": 140}
BS_OTHER_LIAB = {"FY2025": 565, "FY2024": 554, "FY2023": 1156, "FY2022": 2602, "FY2021": 530}
BS_ACCRUALS = {"FY2025": 1920, "FY2024": 1144, "FY2023": 962, "FY2022": 1099, "FY2021": 792}
BS_TOTAL_CURRENT_LIAB = {"FY2025": 12390, "FY2024": 11465, "FY2023": 12017, "FY2022": 193488, "FY2021": 190704}
BS_DEPOSITS_BANKS_NC = {"FY2025": 130000, "FY2024": 130000, "FY2023": 130000}
BS_TOTAL_LIAB = {"FY2025": 142390, "FY2024": 141465, "FY2023": 142017, "FY2022": 193488, "FY2021": 190704}

BS_SHARE_CAPITAL = {y: 160000 for y in YEARS}
BS_RETAINED_EARNINGS = {"FY2026": 11770, "FY2025": 12779, "FY2024": 12011, "FY2023": 11801, "FY2022": 10611, "FY2021": 9065}
BS_TOTAL_EQUITY = {"FY2026": 171770, "FY2025": 172779, "FY2024": 172011, "FY2023": 171801, "FY2022": 170611, "FY2021": 169065}

# FY2026 edition (p.25): order-of-liquidity presentation, no current/non-current
# split (see PRESENTATION_NOTE). Own block, own line order; EUR '000.
BS26_ASSETS = [
    ("Cash and cash equivalents", 159838),
    ("Placements with and loans and advances to banks", 133901),
    ("Loans and advances to customers", 510),
    ("Debt instruments", 8289),
    ("Other assets", 8467),
    ("Prepayments and accrued income", 2532),
    ("Property, plant and equipment", 2620),
    ("Intangibles", 68),
]
BS26_LIABS = [
    ("Deposits from banks", 137578),
    ("Amounts owed to other depositors", 1930),
    ("Corporation taxation", 41),
    ("Other liabilities", 535),
    ("Accruals and deferred income", 4371),
]
BS26_TOTAL_LIAB = 144455
_OLD = [y for y in YEARS if y != "FY2026"]


def _old(d):
    """FY2021-FY2025 only: the current/non-current rows below are their editions' presentation."""
    return {y: v for y, v in d.items() if y in _OLD}


balance_sheet_rows = [
    ("SECTION", "Assets - FY2026 edition presentation (order of liquidity, no current/non-current split)", {}),
    *[("DATA", lbl, gbp_spot({"FY2026": v})) for lbl, v in BS26_ASSETS],
    ("TOTAL", "Total assets (FY2026 presentation)", gbp_spot({"FY2026": BS_TOTAL_ASSETS["FY2026"]})),
    ("SECTION", "Liabilities - FY2026 edition presentation (order of liquidity, no current/non-current split)", {}),
    *[("DATA", lbl, gbp_spot({"FY2026": v})) for lbl, v in BS26_LIABS],
    ("TOTAL", "Total liabilities (FY2026 presentation)", gbp_spot({"FY2026": BS26_TOTAL_LIAB})),
    ("SECTION", "Non-current assets (FY2021-FY2025 editions' presentation)", {}),
    ("DATA", "Restricted cash and cash equivalents", gbp_spot(BS_RESTRICTED_CASH)),
    ("DATA", "Placements with and loans and advances to banks", gbp_spot(BS_PLACEMENTS_BANKS_NC)),
    ("DATA", "Property and equipment", gbp_spot(BS_PROPERTY_EQUIPMENT)),
    ("DATA", "Intangible assets", gbp_spot(BS_INTANGIBLE)),
    ("DATA", "Debt instruments", gbp_spot(BS_DEBT_INSTR_NC)),
    ("TOTAL", "Total non-current assets", gbp_spot(BS_TOTAL_NC)),
    ("SECTION", "Current assets", {}),
    ("DATA", "Cash and cash equivalents", gbp_spot(BS_CASH)),
    ("DATA", "Placements with and loans and advances to banks", gbp_spot(BS_PLACEMENTS_BANKS_C)),
    ("DATA", "Loans and advances to customers", gbp_spot(_old(BS_LOANS_CUSTOMERS))),
    ("DATA", "Other assets", gbp_spot(BS_OTHER_ASSETS)),
    ("DATA", "Debt instruments", gbp_spot(BS_DEBT_INSTR_C)),
    ("DATA", "Prepayments and accrued income", gbp_spot(BS_PREPAYMENTS)),
    ("TOTAL", "Total assets", gbp_spot(_old(BS_TOTAL_ASSETS))),
    ("SECTION", "Current liabilities", {}),
    ("DATA", "Deposits from banks", gbp_spot(BS_DEPOSITS_BANKS_C)),
    ("DATA", "Amounts owed to other depositors", gbp_spot(_old(BS_DEPOSITORS))),
    ("DATA", "Corporation taxation", gbp_spot(BS_CORP_TAX)),
    ("DATA", "Other liabilities", gbp_spot(BS_OTHER_LIAB)),
    ("DATA", "Accruals and deferred income", gbp_spot(BS_ACCRUALS)),
    ("TOTAL", "Total current liabilities", gbp_spot(BS_TOTAL_CURRENT_LIAB)),
    ("SECTION", "Non-current liabilities", {}),
    ("DATA", "Deposits from banks", gbp_spot(BS_DEPOSITS_BANKS_NC)),
    ("TOTAL", "Total liabilities", gbp_spot(BS_TOTAL_LIAB)),
    ("SECTION", "Equity", {}),
    ("DATA", "Called up share capital", gbp_spot(BS_SHARE_CAPITAL)),
    ("DATA", "Retained earnings", gbp_spot(BS_RETAINED_EARNINGS)),
    ("TOTAL", "Total equity", gbp_spot(BS_TOTAL_EQUITY)),
    ("TOTAL", "Total liabilities and equity", gbp_spot(BS_TOTAL_ASSETS)),
]

bw.add_balance_sheet_sheet(
    title="Bank Sepah International Plc — Statement of Financial Position",
    subtitle="£'000, converted from EUR - see source note at bottom for FX methodology and rates used.",
    rows=balance_sheet_rows,
    sources_text=STATEMENTS_SOURCES + "\n\n" + PRESENTATION_NOTE,
    first_col_width=70,
    source_height=460,
    unit_suffix=" (£'000, conv. from EUR)",
)

# ---------------------------------------------------------------
# Profit & Loss (EUR '000, raw units - flow figures converted at each year's average rate)
# ---------------------------------------------------------------
IS_INTEREST_INCOME = {"FY2026": 9878, "FY2025": 10080, "FY2024": 9564, "FY2023": 7624, "FY2022": 7321, "FY2021": 7200}
IS_INTEREST_EXPENSE = {"FY2026": -3362, "FY2025": -3639, "FY2024": -3, "FY2023": -209, "FY2022": -680, "FY2021": -552}
IS_NET_INTEREST_INCOME = {"FY2026": 6516, "FY2025": 6441, "FY2024": 9561, "FY2023": 7415, "FY2022": 6641, "FY2021": 6648}
IS_FEE_EXPENSE = {"FY2026": -62, "FY2025": -77, "FY2024": -120, "FY2023": -211, "FY2022": -125, "FY2021": -87}
IS_FX = {"FY2026": -194, "FY2025": -3, "FY2024": -11, "FY2023": -107, "FY2022": -5, "FY2021": 110}
IS_OTHER_OPERATING = {"FY2026": 264, "FY2025": 72, "FY2024": 1291, "FY2023": 0, "FY2022": 0, "FY2021": 0}
IS_TOTAL_OPERATING_INCOME = {"FY2026": 6524, "FY2025": 6433, "FY2024": 10721, "FY2023": 7097, "FY2022": 6511, "FY2021": 6671}
IS_ADMIN_EXPENSES = {"FY2026": -5923, "FY2025": -5524, "FY2024": -5008, "FY2023": -4701, "FY2022": -4864, "FY2021": -4905}
IS_CREDIT_IMPAIRMENT = {"FY2026": -1794, "FY2025": 120, "FY2024": -5513, "FY2023": -981, "FY2022": 40, "FY2021": -140}
IS_PROFIT_BEFORE_TAX = {"FY2026": -1193, "FY2025": 1029, "FY2024": 200, "FY2023": 1415, "FY2022": 1687, "FY2021": 1626}
IS_TAX = {"FY2026": 184, "FY2025": -261, "FY2024": 10, "FY2023": -225, "FY2022": -140, "FY2021": 0}
IS_PROFIT_AFTER_TAX = {"FY2026": -1009, "FY2025": 768, "FY2024": 210, "FY2023": 1190, "FY2022": 1547, "FY2021": 1626}
IS_OCI = {y: 0 for y in YEARS if y != "FY2026"}
IS_TOTAL_COMPREHENSIVE = dict(IS_PROFIT_AFTER_TAX)
# FY2026 edition p.24 prints Other Comprehensive Income as a dash: kept as "-" (see PRESENTATION_NOTE).
IS_OCI_CELLS = {**gbp_avg(IS_OCI), "FY2026": "-"}

income_statement_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest and similar income", gbp_avg(IS_INTEREST_INCOME)),
    ("DATA", "Interest expense and similar charges", gbp_avg(IS_INTEREST_EXPENSE)),
    ("TOTAL", "Net interest income", gbp_avg(IS_NET_INTEREST_INCOME)),
    ("DATA", "Net fee and commission expense", gbp_avg(IS_FEE_EXPENSE)),
    ("DATA", "Foreign currency (loss)/gain", gbp_avg(IS_FX)),
    ("DATA", "Other operating income", gbp_avg(IS_OTHER_OPERATING)),
    ("TOTAL", "Total operating income", gbp_avg(IS_TOTAL_OPERATING_INCOME)),
    ("DATA", "General administrative expenses", gbp_avg(IS_ADMIN_EXPENSES)),
    ("DATA", "Credit impairment gains/(losses)", gbp_avg(IS_CREDIT_IMPAIRMENT)),
    ("TOTAL", "Profit before taxation", gbp_avg(IS_PROFIT_BEFORE_TAX)),
    ("DATA", "Taxation (charge)/credit", gbp_avg(IS_TAX)),
    ("TOTAL", "Profit for the year after taxation", gbp_avg(IS_PROFIT_AFTER_TAX)),
    ("SECTION", "Other comprehensive income", {}),
    ("DATA", "Other comprehensive income", IS_OCI_CELLS),
    ("TOTAL", "Total comprehensive income for the year", gbp_avg(IS_TOTAL_COMPREHENSIVE)),
]

bw.add_income_statement_sheet(
    title="Bank Sepah International Plc — Statement of Comprehensive Income",
    subtitle="£'000, converted from EUR - see source note at bottom for FX methodology and rates used.",
    rows=income_statement_rows,
    sources_text=STATEMENTS_SOURCES + "\n\n" + PRESENTATION_NOTE,
    first_col_width=70,
    source_height=460,
    unit_suffix=" (£'000, conv. from EUR)",
)

# ---------------------------------------------------------------
# Statement of Changes in Equity (chronological; each snapshot converted at
# its own period-end spot rate, each year's profit at that year's average
# rate - an "FX translation effect" plug row absorbs the resulting gap per
# component column, same treatment as Bank Saderat/Bank Mandiri Europe.
# FY2021's own movement (profit + 1 April 2020 opening) is OMITTED - no
# verified FY2020 EUR/GBP rate exists for this bank (same reason the Cash
# Flow Statement sheet leaves FY2021's opening cash blank) - the sheet
# instead opens at "31 March 2021 / 1 April 2021", converted at FY2021's
# own (verified) year-end rate.
# ---------------------------------------------------------------
EQUITY_EUR = [
    ("2021-03-31", "opening", {"cap": 160000, "retained": 9064, "total": 169064}),
    ("FY2022", "profit", {"cap": 0, "retained": 1547, "total": 1547}),
    ("2022-03-31", "closing", {"cap": 160000, "retained": 10611, "total": 170611}),
    ("FY2023", "profit", {"cap": 0, "retained": 1190, "total": 1190}),
    ("2023-03-31", "closing", {"cap": 160000, "retained": 11801, "total": 171801}),
    ("FY2024", "profit", {"cap": 0, "retained": 210, "total": 210}),
    ("2024-03-31", "closing", {"cap": 160000, "retained": 12011, "total": 172011}),
    ("FY2025", "profit", {"cap": 0, "retained": 768, "total": 768}),
    ("2025-03-31", "closing", {"cap": 160000, "retained": 12779, "total": 172779}),
    # FY2026 edition p.26: 'Loss for year ended 31 March 2026' (1,009) = Total comprehensive income.
    ("FY2026", "profit", {"cap": 0, "retained": -1009, "total": -1009}),
    ("2026-03-31", "closing", {"cap": 160000, "retained": 11770, "total": 171770}),
]

SNAPSHOT_SPOT = {
    "2021-03-31": YEAR_END_RATE["FY2021"],
    "2022-03-31": YEAR_END_RATE["FY2022"],
    "2023-03-31": YEAR_END_RATE["FY2023"],
    "2024-03-31": YEAR_END_RATE["FY2024"],
    "2025-03-31": YEAR_END_RATE["FY2025"],
    "2026-03-31": YEAR_END_RATE["FY2026"],
}


def _to_gbp(eur, rate):
    return round(eur * rate, 1)


equity_gbp = {}
for key, kind, comps in EQUITY_EUR:
    rate = AVG_RATE[key] if kind == "profit" else SNAPSHOT_SPOT[key]
    equity_gbp[key] = {c: _to_gbp(v, rate) for c, v in comps.items()}

equity_changes_rows = []
for idx, (key, kind, comps) in enumerate(EQUITY_EUR):
    g = equity_gbp[key]
    if kind == "opening":
        equity_changes_rows.append(("TOTAL", "At 31 March 2021 / 1 April 2021", (g["cap"], g["retained"], g["total"])))
    elif kind == "profit":
        label = f"{'Loss' if comps['total'] < 0 else 'Profit'} and total comprehensive income for the year ({key})"
        equity_changes_rows.append(("DATA", label, (None, g["retained"], g["total"])))
    else:  # closing
        opening_key = EQUITY_EUR[idx - 2][0]
        profit_key = EQUITY_EUR[idx - 1][0]
        plug = {
            c: round(g[c] - equity_gbp[opening_key][c] - equity_gbp[profit_key].get(c, 0), 1)
            for c in ("cap", "retained", "total")
        }
        if any(abs(v) > 0.05 for v in plug.values()):
            equity_changes_rows.append((
                "DATA", "FX translation effect on equity, net",
                (plug["cap"], plug["retained"], plug["total"]),
            ))
        label = f"At {key[8:10]} {['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'][int(key[5:7])-1]}. {key[:4]}"
        equity_changes_rows.append(("TOTAL", label, (g["cap"], g["retained"], g["total"])))

bw.add_equity_changes_sheet(
    title="Bank Sepah International Plc — Statement of Changes in Equity",
    subtitle="£'000, converted from EUR - see source note at bottom for FX methodology; an 'FX translation effect' "
              "row is included since Called up share capital is EUR-constant but still shifts in £ terms because "
              "each snapshot is converted at that period's own spot rate. FY2021's own movement is omitted - see "
              "note below.",
    headers=["Called up share capital", "Retained earnings", "Total"],
    rows=equity_changes_rows,
    sources_text=STATEMENTS_SOURCES + "\n\n" + PRESENTATION_NOTE + "\n\nNote: FY2021's own opening balance (at 1 "
                 "April 2020) and profit movement are omitted - no verified FY2020 EUR/GBP rate exists for this "
                 "bank (same reason the Cash Flow Statement sheet leaves FY2021's opening cash blank); the sheet "
                 "instead opens at 31 March 2021 (FY2021's closing / FY2022's opening), which IS converted at a "
                 "verified rate. The opening figure used here (EUR9,064k) is the Bank's own Statement of Changes "
                 "in Equity figure for that date - see PRESENTATION_NOTE for a EUR1k rounding gap vs. the Balance "
                 "Sheet sheet's own figure (EUR9,065k) for the same date, both from the same source document.",
    first_col_width=56,
    source_height=460,
)

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
# Source figures (EUR '000), from the Bank's own Statement of Cash Flows, cross-checked across overlapping filings.
OPERATING_EUR = {"FY2026": 3131, "FY2025": -7597, "FY2024": 5217, "FY2023": -51049, "FY2022": 18042, "FY2021": 2189}
INVESTING_EUR = {"FY2026": 9850, "FY2025": 1137, "FY2024": -2122, "FY2023": -122, "FY2022": -515, "FY2021": -499}
NET_CHANGE_EUR = {"FY2026": 12981, "FY2025": -6460, "FY2024": 3105, "FY2023": -51171, "FY2022": 17208, "FY2021": 1690}
FX_EUR = {"FY2026": -227, "FY2025": -106, "FY2024": -44, "FY2023": -264, "FY2022": 36, "FY2021": -259}
OPENING_EUR = {"FY2026": 149503, "FY2025": 156069, "FY2024": 153018, "FY2023": 204453, "FY2022": 187209, "FY2021": 185778}
CLOSING_EUR = {"FY2026": 162257, "FY2025": 149503, "FY2024": 156069, "FY2023": 153018, "FY2022": 204453, "FY2021": 187209}


def flow(eur):
    # eur values are already in EUR '000, so v * rate gives GBP '000 directly.
    return {y: round(v * AVG_RATE[y], 1) for y, v in eur.items()}


def stock(eur):
    return {y: round(v * YEAR_END_RATE[y], 1) for y, v in eur.items()}


OPERATING_GBP = flow(OPERATING_EUR)
INVESTING_GBP = flow(INVESTING_EUR)
NET_CHANGE_GBP = flow(NET_CHANGE_EUR)
FX_GBP = flow(FX_EUR)
CLOSING_GBP = stock(CLOSING_EUR)

# Opening balance: converted at the SAME year's year-end rate applied to the prior year's own EUR closing figure
# (i.e. it equals the prior year's own closing GBP figure exactly) - FY2021's opening has no available FY2020 rate
# and is deliberately left blank rather than sourcing an unverified rate (same convention as Access Bank UK's FY2020).
OPENING_GBP = {
    "FY2026": CLOSING_GBP["FY2025"],
    "FY2025": CLOSING_GBP["FY2024"],
    "FY2024": CLOSING_GBP["FY2023"],
    "FY2023": CLOSING_GBP["FY2022"],
    "FY2022": CLOSING_GBP["FY2021"],
}

# Translation plug computed programmatically (never hardcoded) so it can't hide a conversion bug.
TRANSLATION_PLUG = {
    y: round(CLOSING_GBP[y] - OPENING_GBP[y] - NET_CHANGE_GBP[y] - FX_GBP[y], 1)
    for y in YEARS if y in OPENING_GBP
}

rows = [
    ("SECTION", "Operating activities", {}),
    ("TOTAL", "Net cash from/(used in) operating activities", OPERATING_GBP),
    ("SECTION", "Investing activities", {}),
    ("TOTAL", "Net cash from/(used in) investing activities", INVESTING_GBP),
    ("TOTAL", "Net (decrease)/increase in cash and cash equivalents", NET_CHANGE_GBP),
    ("DATA", "Foreign currency exchange (loss)/gain (Bank's own, EUR functional currency)", FX_GBP),
    ("DATA", "Effect of GBP/EUR translation (this workbook's own conversion, not in the source)", TRANSLATION_PLUG),
    ("DATA", "Cash and cash equivalents at the beginning of the year", OPENING_GBP),
    ("TOTAL", "Cash and cash equivalents at the end of the year", CLOSING_GBP),
]

bw.add_cash_flow_sheet(
    title="Bank Sepah International Plc — Statement of Cash Flows",
    subtitle="Entity-level basis, reports in EUR, converted to GBP - see source note below for methodology",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=90,
    source_height=260,
    unit_suffix=" (£'000, conv. from EUR)",
)

# ---------------------------------------------------------------
# Asset Quality: loans and advances to customers (gross/net + allowance,
# Note 10/11) plus the Bank's own total ECL provision by IFRS 9 stage
# across ALL financial asset classes (Note 11/12) - a richer risk view
# than the customer loan book alone, since almost all of this Bank's
# balance sheet is interbank placements, not customer lending.
# ---------------------------------------------------------------
AQ_GROSS_LOANS = {"FY2026": 5519, "FY2025": 5716, "FY2024": 5810, "FY2023": 31405, "FY2022": 31288, "FY2021": 4980}
AQ_ALLOWANCE_CUSTOMERS = {"FY2026": 5009, "FY2025": 5317, "FY2024": 5331, "FY2023": 3304, "FY2022": 2264, "FY2021": 2080}
AQ_NET_LOANS = {"FY2026": 510, "FY2025": 399, "FY2024": 479, "FY2023": 28101, "FY2022": 29024, "FY2021": 2900}

AQ_ECL_STAGE1 = {"FY2026": 11, "FY2025": 2014, "FY2024": 2198, "FY2023": 302, "FY2022": 374, "FY2021": 418}
AQ_ECL_STAGE2 = {"FY2026": 5400, "FY2025": 1603, "FY2024": 1551, "FY2023": 2, "FY2022": 5, "FY2021": 1}
AQ_ECL_STAGE3 = {"FY2026": 5019, "FY2025": 5328, "FY2024": 5326, "FY2023": 3300, "FY2022": 2197, "FY2021": 2474}
AQ_ECL_TOTAL = {"FY2026": 10430, "FY2025": 8945, "FY2024": 9075, "FY2023": 3604, "FY2022": 2576, "FY2021": 2893}

AQ_COVERAGE_RATIO = {y: f"{AQ_ALLOWANCE_CUSTOMERS[y] / AQ_GROSS_LOANS[y] * 100:.1f}%" for y in YEARS}
AQ_STAGE3_SHARE = {y: f"{AQ_ECL_STAGE3[y] / AQ_ECL_TOTAL[y] * 100:.1f}%" for y in YEARS}

asset_quality_rows = [
    ("SECTION", "Loans and advances to customers (Note 10/11)", {}),
    ("DATA", "Gross loans and advances to customers", gbp_spot(AQ_GROSS_LOANS)),
    ("DATA", "Less: IFRS 9 impairment provisions", gbp_spot({y: -v for y, v in AQ_ALLOWANCE_CUSTOMERS.items()})),
    ("TOTAL", "Net loans and advances to customers", gbp_spot(AQ_NET_LOANS)),
    ("DATA", "Allowance coverage ratio (allowance / gross loans to customers)", AQ_COVERAGE_RATIO),
    ("SECTION", "Total ECL provisions, all financial asset classes, by IFRS 9 stage (Note 11/12)", {}),
    ("DATA", "Stage 1 (12-month ECL)", gbp_spot(AQ_ECL_STAGE1)),
    ("DATA", "Stage 2 (lifetime ECL, not credit-impaired)", gbp_spot(AQ_ECL_STAGE2)),
    ("DATA", "Stage 3 (lifetime ECL, credit-impaired)", gbp_spot(AQ_ECL_STAGE3)),
    ("TOTAL", "Total ECL provisions across all financial assets", gbp_spot(AQ_ECL_TOTAL)),
    ("DATA", "Stage 3 share of total ECL provisions", AQ_STAGE3_SHARE),
]

bw.add_asset_quality_sheet(
    title="Bank Sepah International Plc — Asset Quality / Credit Risk Disclosures",
    subtitle="£'000, converted from EUR. Almost all of this Bank's ECL provision sits against Loans and advances "
              "to customers (a small share of total assets - most of the balance sheet is interbank placements), "
              "so the total ECL-by-stage view (across ALL financial asset classes) is included alongside the "
              "customer loan book split for a fuller risk picture.",
    rows=asset_quality_rows,
    sources_text=(
        "Sources - Bank Sepah International Plc's own Note 10/11 (Loans and advances to customers) and Note 11/12 "
        "(IFRS 9 Impairment losses, by stage, all financial asset classes):\n"
        f"FY2026: Full accounts to 31 March 2026 (filed 16 Sep 2026), Notes 11 and 12, p.38 - {AR2026_URL}\n"
        f"FY2025: Full accounts to 31 March 2025, p.39 - {AR2025_URL}\n"
        f"FY2024/FY2023: Full accounts to 31 March 2024, pp.40-41 - {AR2024_URL}\n"
        f"FY2022/FY2021: Full accounts to 31 March 2022, pp.36-37 - {AR2022_URL}\n\n"
        "Note: the FY2025/FY2024 tables label the Stage 2 column 'Specific' while FY2023-FY2021 label it "
        "'Collective' - reproduced exactly as each year's own report presents it, not reclassified. The FY2026 "
        "edition's Note 12 table heads its columns simply 'Stage 1 / Stage 2 / Stage 3 / Total'. FY2026 figures "
        "foot as printed: gross 5,519 (511 performing + 5,008 overdue) less 5,009 = 510; ECL by stage 11 + 5,400 "
        "+ 5,019 = 10,430 (EUR'000). The FY2026 Stage 2 jump (EUR1,603k to EUR5,400k) sits entirely on cash and "
        "cash equivalents (2,405) and loans and advances to banks (2,995), which the edition shows by asset "
        "class; the FY2026 credit impairment charge is EUR1,794k (2025: recovery EUR120k).\n\n"
        + ENTITY_NOTE + "\n\n" + FX_NOTE
    ),
    first_col_width=76,
    source_height=440,
    unit_suffix=" (£'000, conv. from EUR)",
)

# ---------------------------------------------------------------
# KM1 Key Metrics - the Bank's own 'Summary of Key Metrics', in EUR
# ---------------------------------------------------------------
KM1_SOURCES = (
    "Source - Bank Sepah International Plc's own 'Table 1 Summary of Key Metrics', p.5 of each year's Pillar 3 "
    "Disclosures, reproduced exactly as printed:\n"
    f"FY2025 ('Mar 25' column): Pillar 3 Disclosures as at 31 March 2025, p.5 - {P3_2025_URL}\n"
    f"FY2024 ('Mar 24' column): Pillar 3 Disclosures as at 31 March 2024, p.5 - {P3_2024_URL}\n"
    f"FY2023 ('Mar 23' column): Pillar 3 Disclosures 31 March 2023, p.5 - {P3_2023_URL}\n"
    f"FY2022 ('Mar 22' column): Pillar 3 Disclosures 31 March 2022, p.5 - {P3_2022_URL}\n"
    f"FY2021 ('Mar 21' column): Pillar 3 Disclosures 31 March 2021, p.5 - {P3_2021_URL}\n\n"
    "AMOUNTS ARE IN EURO THOUSANDS (EUR'000), NOT STERLING. The Bank reports in euro and prints this table "
    "headed '€000'. It is reproduced in its published currency and is therefore NOT comparable cell-for-cell "
    "with the individual metric sheets in this workbook, which are converted to sterling at the Bank's own "
    "disclosed year-end rates (see the FX note on those sheets). No conversion, and no derivation of any "
    "kind, has been applied to anything on this sheet.\n\n"
    "THE COLUMNS IN THE SOURCE ARE QUARTER-ENDS, NOT YEARS. Each edition prints five columns - its own "
    "financial year-end followed by the preceding four quarters (e.g. the March-2025 edition prints Mar 25, "
    "Dec 24, Sep 24, Jun 24, Mar 24). The Bank's year-end is 31 MARCH, so only the 'Mar' column of each "
    "edition is that financial year, and that is the only column used here. The four quarterly columns are "
    "not reproduced.\n\n"
    "EACH YEAR COMES FROM ITS OWN EDITION, WHICH MATTERS HERE - the same date is printed differently in "
    "different editions, and the own-edition figure is the one used:\n"
    "  March 2022: Total Risk Exposure 252,734 in the March-2022 edition vs 252,058 as the March-2023 "
    "edition's comparative; NSFR 458% vs 459%.\n"
    "  March 2023: CET1 172,027 and TRE 208,649 in the March-2023 edition vs 171,801 and 209,637 as the "
    "March-2024 edition's comparatives.\n"
    "  March 2024: LCR 2877% in the March-2024 edition vs 2875% as the March-2025 edition's comparative.\n\n"
    "ROW-SET NOTE. The Bank captions this 'Summary of Key Metrics' and prints no template row numbers. It "
    "carries the backbone of the KM1 template - capital, total risk exposure, the capital ratio, the "
    "conservation and countercyclical buffers, CET1 available after the minimum requirement, the leverage "
    "ratio, the LCR with its HQLA/outflow/inflow components, and the NSFR with its available/required stable "
    "funding components - but it does NOT print separate Tier 1 or Total capital rows (the Bank has no AT1 or "
    "Tier 2 instruments, so CET1 = Tier 1 = Total capital), nor a leverage exposure measure, nor the SREP or "
    "combined-buffer blocks. Row labels are reproduced exactly as the Bank prints them, including "
    "'Total required sable funding', which is spelled that way - missing the 't' - in all five editions. "
    "Because these labels are the Bank's own rather than the template's, the workbook verifier's KM1 "
    "cross-check matches none of them and reports zero cross-checked cells for this sheet. That is the "
    "expected result, not a failure: the rows were not renamed to force agreement.\n\n"
    "ROW DIFFERENCES BETWEEN EDITIONS (a row not printed is left blank, never filled from another year): the "
    "March-2021 edition prints neither a 'Cash Outflows' nor a 'Cash Inflows' row, and labels its net figure "
    "'Total net cash outflow' in the singular. It also prints the countercyclical buffer as 0%, where every "
    "later edition prints a dash - so FY2021 carries a zero and the other four years carry that dash. The two "
    "are deliberately not the same cell: at March 2021 the Bank measured its countercyclical buffer and "
    "reported nil, and from March 2022 onward it printed a dash instead, saying the line did not apply to it. "
    "Flattening both to an empty cell, or both to a zero, would erase a change the Bank itself made. Verified "
    "2026-09-18 by retrieving all five editions and reading each year from its own Table 1, printed page 5, "
    "first column (each edition also prints the four preceding quarter-ends, which are not used here).\n\n"
    "LATEST-EDITION CHECK, 2026-09-16: the Bank's own documents page "
    "(https://www.banksepah.co.uk/information) lists the March 2023, March 2024 and March 2025 Pillar 3 "
    "disclosures; March 2025 is the newest and this workbook already holds it. No March-2026 edition has "
    "been published. Note that the page no longer links the March-2021 or March-2022 editions even though "
    "both URLs still serve the documents, so the citation list above is a better record of what exists than "
    "the live page is. Retrieval requires certificate validation to be bypassed - the site's TLS certificate "
    "is expired, which makes a default fetch fail with no HTTP status at all; that is a certificate-date "
    "problem, not a dead link (see the expired-certificate note elsewhere in this workbook).\n\n"
    "ENTITY: Bank Sepah International Plc, the UK-authorised bank, on its own solo basis. No parent figure is "
    "used anywhere on this sheet.\n\n"
    "FY2026 (year to 31 March 2026), checked 2026-09-19: the FY2026 statutory accounts ARE published (Companies "
    f"House, filed 16 Sep 2026 - {AR2026_URL}), but the March 2026 Pillar 3 is NOT. The Bank's documents page "
    "still lists March 2025 as the newest edition, every FY2026 variant of the Bank's filename patterns returns "
    "404 while the March 2025 URL fetched with the same flags returns the PDF, and Wayback holds no 2026 "
    "document. The FY2026 column therefore carries a single statement row and no figures: the Annual Report is "
    "a different document and none of its numbers are placed on this template sheet (it prints the capital "
    "ratio as 85% and the LCR as 1310%, which appear on the single-metric sheets with that citation)."
)

km1_rows = [
    # STATEMENT ROW, not a table row (same shape as SBI UK / Chetwood): FY2026's own
    # edition is not published yet, so there is no Table 1 to reproduce for it and
    # nothing from the FY2026 Annual Report is placed on this sheet.
    ("DATA", "[No Table 1 published for this year yet - see note below]", {"FY2026": P3_2026_PENDING}),
    ("SECTION", "TABLE 1  SUMMARY OF KEY METRICS (the Bank's own caption; amounts in EUR'000)", {}),
    ("DATA", "CET1 (€'000)",
     {"FY2025": 172779, "FY2024": 172011, "FY2023": 172027, "FY2022": 170751, "FY2021": 169065}),
    ("DATA", "Total Risk Exposure (€'000)",
     {"FY2025": 167006, "FY2024": 188600, "FY2023": 208649, "FY2022": 252734, "FY2021": 277208}),
    ("DATA", "CET1 as a % of TRE",
     {"FY2025": "103%", "FY2024": "91%", "FY2023": "82%", "FY2022": "68%", "FY2021": "61%"}),
    ("DATA", "Capital Conservation Buffer",
     {"FY2025": "2.50%", "FY2024": "2.50%", "FY2023": "2.50%", "FY2022": "2.5%", "FY2021": "2.5%"}),
    # All five editions re-read at source 2026-09-18, each year taken from its OWN
    # edition's Table 1 "Summary of Key Metrics", printed page 5, FIRST column only.
    # Every edition prints its reporting date plus the four preceding QUARTER-ends,
    # so columns 2-5 are within-year observations and are never used for another
    # financial year. March-2025/2024/2023/2022 each print "-" in that first column;
    # the March-2021 edition prints "0%" there, and that zero STAYS a zero. The Bank
    # changed what it printed, and the sheet now shows that it did.
    ("DATA", "Countercyclical buffer %",
     {"FY2025": "-", "FY2024": "-", "FY2023": "-", "FY2022": "-", "FY2021": "0%"}),
    ("DATA", "CET1 available after meeting Minimum Capital Requirement as a % of TRE",
     {"FY2025": "95%", "FY2024": "83%", "FY2023": "74%", "FY2022": "60%", "FY2021": "53%"}),
    ("DATA", "Leverage ratio",
     {"FY2025": "55%", "FY2024": "55%", "FY2023": "54%", "FY2022": "46%", "FY2021": "47%"}),
    ("DATA", "Total HQLA (€'000)",
     {"FY2025": 19041, "FY2024": 20009, "FY2023": 16244, "FY2022": 14609, "FY2021": 13585}),
    ("DATA", "Cash Outflows (€'000)",
     {"FY2025": 3744, "FY2024": 2782, "FY2023": 2778, "FY2022": 53766}),
    ("DATA", "Cash Inflows (€'000)",
     {"FY2025": 152541, "FY2024": 158931, "FY2023": 156620, "FY2022": 255734}),
    ("DATA", "Total net cash outflows (€'000)",
     {"FY2025": 936, "FY2024": 696, "FY2023": 695, "FY2022": 13419, "FY2021": 918}),
    ("DATA", "LCR %",
     {"FY2025": "2034%", "FY2024": "2877%", "FY2023": "2339%", "FY2022": "109%", "FY2021": "1480%"}),
    ("DATA", "Total available stable funding (€'000)",
     {"FY2025": 306143, "FY2024": 305367, "FY2023": 304095, "FY2022": 302584, "FY2021": 300254}),
    ("DATA", "Total required sable funding (€'000)",
     {"FY2025": 52659, "FY2024": 80677, "FY2023": 33914, "FY2022": 66013, "FY2021": 81302}),
    ("DATA", "NSFR %",
     {"FY2025": "581%", "FY2024": "379%", "FY2023": "897%", "FY2022": "458%", "FY2021": "369%"}),
]

bw.add_km1_sheet(
    title="Bank Sepah International Plc - KM1 Key Metrics",
    subtitle="The Bank's own 'Table 1 Summary of Key Metrics', year-end (March) column of each edition - EUR'000 as published",
    rows=km1_rows,
    sources_text=KM1_SOURCES,
    first_col_width=72,
    source_height=620,
    years=YEARS,
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, note=None):
    bw.add_metric_sheet(name, unit, rows_data, p3_sources(), note=note, first_col_width=52, source_height=560)


# Total capital resources (EUR m), = CET1 = Tier 1 = Total Capital (no AT1/Tier 2 disclosed)
CAPITAL_EUR_M = {"FY2026": 172, "FY2025": 173, "FY2024": 172, "FY2023": 172, "FY2022": 170, "FY2021": 169}
CAPITAL_RATIO = {"FY2026": "85%", "FY2025": "102.7%", "FY2024": "91.8%", "FY2023": "81.5%", "FY2022": "67.5%", "FY2021": "61.2%"}
CAPITAL_GBP_M = {y: round(v * YEAR_END_RATE[y], 1) for y, v in CAPITAL_EUR_M.items()}

# Directly disclosed in the Bank's own Pillar 3 Table 4 (Total Risk Exposure = Total RWAs).
RWA_EUR_M = {"FY2025": 167.006, "FY2024": 188.600, "FY2023": 209.637,
             "FY2022": 252.583, "FY2021": 277.208}
RWA_GBP_M = {y: round(v * YEAR_END_RATE[y], 1) for y, v in RWA_EUR_M.items()}
# FY2026: Total Risk Exposure comes only from Pillar 3 Table 4, not yet published (never back-solved from
# the 85% ratio and EUR172m capital).
RWA_CELLS = {**RWA_GBP_M, "FY2026": P3_2026_PENDING}

CAPITAL_NOTE = "CET1 = Tier 1 = Total Capital every year - the Bank discloses only a single combined capital figure, no AT1/Tier 2 instruments mentioned anywhere in the Annual Report."
RATIO_NOTE = "The Bank discloses one 'Total capital / Tier 1 capital to total risk-weighted assets' ratio (identical each year, confirming no AT1/Tier 2) - used for CET1/Tier1/Total Capital Ratio alike."
RWA_NOTE = ("DIRECTLY DISCLOSED by the Bank's own Pillar 3 Table 4 'Total Risk Exposure' (equivalent to Total "
            "Risk Weighted Assets), rather than calculated from rounded capital ratios. Each year's own report "
            "is used (March 2025/2024/2023/2022/2021, Table 4 p.16). EUR amounts are converted to GBP at the "
            "Bank's own year-end EUR/GBP rate.")
MREL_NOTE = ("Not publicly disclosed - no MREL figure appears in the FY2021-FY2025 Annual Reports, nor in the "
             "Bank's own Pillar 3 Disclosures documents for FY2022-FY2025 (see the Leverage Ratio/LCR/NSFR "
             "sheets' citations - the same Table 1 'Summary of Key Metrics' that discloses those three ratios "
             "has no MREL line; the full text of all 4 available Pillar 3 PDFs was also searched for the word "
             "'MREL' and found no matches). The March 2021 Pillar 3 (cited on the RWA and liquidity sheets) was "
             "searched the same way on 2026-09-19 and has no 'MREL' or 'eligible liabilities' either. The FY2026 "
             "Annual Report has no MREL figure; the March 2026 Pillar 3 is not published yet. Consistent with "
             "the PRA classifying BSIP as a small, non-systemic firm (Category 3 as at FY2025, Category 5 in "
             "earlier years) - such firms are not generally subject to a bail-in MREL requirement.")

metric("CET1 Capital", "£m (conv. from EUR)", [("Common Equity Tier 1 (CET1) capital", CAPITAL_GBP_M)], note=CAPITAL_NOTE)
metric("CET1 Ratio", "%", [("CET1 to total risk-weighted assets", CAPITAL_RATIO)], note=RATIO_NOTE)
metric("Tier 1 Capital", "£m (conv. from EUR)", [("Tier 1 capital", CAPITAL_GBP_M)], note=CAPITAL_NOTE)
metric("Tier 1 Ratio", "%", [("Tier 1 capital to total risk-weighted assets", CAPITAL_RATIO)], note=RATIO_NOTE)
metric("Total Capital", "£m (conv. from EUR)", [("Total capital resources", CAPITAL_GBP_M)], note=CAPITAL_NOTE)
metric("Total Capital Ratio", "%", [("Total capital to total risk-weighted assets", CAPITAL_RATIO)], note=RATIO_NOTE)
metric("Total RWAs", "£m (conv. from EUR)", [("Total risk-weighted assets", RWA_CELLS)], note=RWA_NOTE)

RWA_CREDIT_EUR_M = {"FY2025": 149.153, "FY2024": 171.615, "FY2023": 195.297,
                    "FY2022": 239.515, "FY2021": 264.441}
RWA_MARKET_EUR_M = {"FY2025": 3.547, "FY2024": 2.586, "FY2023": 1.665,
                    "FY2022": 1.379, "FY2021": 1.601}
RWA_OPERATIONAL_EUR_M = {"FY2025": 14.305, "FY2024": 14.399, "FY2023": 12.675,
                         "FY2022": 11.689, "FY2021": 11.166}
bw.add_rwa_breakdown_sheet(
    title="Bank Sepah International Plc — RWA Breakdown",
    subtitle="£m (conv. from EUR) — risk type split, as disclosed",
    rows=[("DATA", "Credit risk", {y: round(v * YEAR_END_RATE[y], 1) for y, v in RWA_CREDIT_EUR_M.items()}),
          ("DATA", "Market risk", {y: round(v * YEAR_END_RATE[y], 1) for y, v in RWA_MARKET_EUR_M.items()}),
          ("DATA", "Operational risk", {y: round(v * YEAR_END_RATE[y], 1) for y, v in RWA_OPERATIONAL_EUR_M.items()}),
          ("TOTAL", "Total Risk Exposure", RWA_CELLS)],
    unit_suffix=" (£m, conv. from EUR)",
    sources_text=p3_sources() + "\n\nThe Bank's own Pillar 3 Table 4 directly discloses the risk-type split "
                 "Bank's own Pillar 3 Disclosures documents (see the Leverage Ratio/LCR/NSFR sheets' citations - "
                 "these were successfully fetched despite the site's expired TLS certificate). Those documents' "
                 "own Table 4 'Total Risk Exposure' splits Total Risk Exposure only 3 ways, by risk TYPE (credit/"
                 "market/operational, e.g. EUR149,153k/3,547k/14,305k at March 2025) - not by risk CATEGORY/asset "
                 "class in the UK OV1 format this sheet is structured for (sovereign, institutions, corporate, "
                 "retail, etc.). The directly disclosed risk-type split is provided above; it is the Bank's "
                 "own Table 4 classification and sums to Total Risk Exposure (minor GBP conversion rounding may "
                 "leave a 0.1m difference).\n\nFY2026: the March 2026 Pillar 3 (and so its Table 4) is not "
                 "published yet - see the statement in the FY2026 cell and the KM1 Key Metrics sheet's note.",
    first_col_width=54,
    source_height=620,
)

# Leverage Ratio / LCR / NSFR: found in the Bank's own Pillar 3 Disclosures documents (published at
# www.banksepah.co.uk/information, fetched via curl -k due to the site's expired TLS certificate - see
# liquidity_leverage_sources() below), Table 1 "Summary of Key Metrics", each report's own p.5.
LEVERAGE_RATIO = {"FY2026": P3_2026_PENDING, "FY2025": "55%", "FY2024": "55%", "FY2023": "54%", "FY2022": "46%", "FY2021": "47%"}
# FY2026 LCR from the FY2026 Annual Report, Strategic Report 'Liquidity', p.6: "The LCR at the year-end
# was 1310% (2025 2034%)" - its FY2025 comparative equals the March 2025 Pillar 3's own figure.
LCR_RATIO = {"FY2026": "1310%", "FY2025": "2034%", "FY2024": "2877%", "FY2023": "2339%", "FY2022": "109%", "FY2021": "1480%"}
NSFR_RATIO = {"FY2026": P3_2026_PENDING, "FY2025": "581%", "FY2024": "379%", "FY2023": "897%", "FY2022": "458%", "FY2021": "369%"}

LIQ_LEV_NOTE = ("Sourced from the Bank's own Pillar 3 Disclosures documents (Table 1 'Summary of Key Metrics'), "
                "not the Annual Report - see this sheet's own source citation below for the exact PDFs/pages and "
                "the TLS-certificate workaround used to fetch them.")

bw.add_metric_sheet("Leverage Ratio", "%", [("Leverage ratio", LEVERAGE_RATIO)], liquidity_leverage_sources(),
                     note=LIQ_LEV_NOTE, first_col_width=52, source_height=500)
bw.add_metric_sheet("LCR", "%", [("Liquidity Coverage Ratio", LCR_RATIO)], liquidity_leverage_sources(),
                     note=LIQ_LEV_NOTE, first_col_width=52, source_height=500)
bw.add_metric_sheet("NSFR", "%", [("Net Stable Funding Ratio", NSFR_RATIO)], liquidity_leverage_sources(),
                     note=LIQ_LEV_NOTE, first_col_width=52, source_height=500)

# GA-020 (2026-09-19). Evidence is MREL_NOTE above, which names the documents
# (FY2021-FY2025 Annual Reports; FY2022-FY2025 Pillar 3 Table 1 'Summary of Key
# Metrics' plus full-text search). Re-fetch attempted 2026-09-19: every
# banksepah.co.uk Pillar 3 URL now returns HTTP 403 and Wayback returns no PDF,
# and the Companies House accounts are image-only, so no fresh text search was
# possible today; the cells rest on the recorded check. NB the March 2021
# Pillar 3 DOES exist (it is the FY2021 source of the RWA and liquidity
# sheets), contrary to MREL_NOTE's last sentences; its MREL content was not
# recorded, so FY2021 cites the Annual Report only.
# CORRECTION 2026-09-19 (FY2026 pass): the 403 above was reach, not the site.
# With curl -k --http1.1 and a browser user-agent, the March 2025 and March
# 2021 Pillar 3 URLs both returned 200 / application/pdf / %PDF the same day
# (644,221 bytes for 2021, the size recorded in P3_FETCH_NOTE). The March 2021
# text layer was then searched: 0 lines match "MREL" or "eligible liabilities",
# against 68 lines matching "capital" and 11 the whole word "leverage" (the
# control), so FY2021 now rests on that edition too.
SEPAH_MREL = {y: ("Not published – no MREL line in the bank's Pillar 3 Table 1 'Summary of Key Metrics' or its "
                  "Annual Report for this year (full-text search recorded in sheet note)")
              for y in ("FY2025", "FY2024", "FY2023", "FY2022")}
SEPAH_MREL["FY2026"] = ("Not published yet – no MREL figure in the FY2026 Annual Report (p.5-6 capital and "
                        "liquidity sections); the March 2026 Pillar 3 is not on banksepah.co.uk at 2026-09-19")
SEPAH_MREL["FY2021"] = ("Not published – no MREL figure in the FY2021 Annual Report (recorded in sheet note) "
                        "or in the March 2021 Pillar 3 (text searched 2026-09-19: no 'MREL' or 'eligible "
                        "liabilities')")
bw.add_not_disclosed_metric_sheets(
    ["MREL Ratio"],
    p3_sources(),
    per_note={"MREL Ratio": MREL_NOTE},
    statements={"MREL Ratio": SEPAH_MREL},
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
OPENING_KEY = {"FY2026": "2025-03-31", "FY2022": "2021-03-31", "FY2023": "2022-03-31", "FY2024": "2023-03-31", "FY2025": "2024-03-31"}
CLOSING_KEY = {"FY2026": "2026-03-31", "FY2022": "2022-03-31", "FY2023": "2023-03-31", "FY2024": "2024-03-31", "FY2025": "2025-03-31"}
eq_opening = {y: equity_gbp[OPENING_KEY[y]]["total"] for y in OPENING_KEY}
eq_tci = {y: equity_gbp[y]["total"] for y in OPENING_KEY}
eq_closing = {y: equity_gbp[CLOSING_KEY[y]]["total"] for y in OPENING_KEY}
eq_other = {y: round(eq_closing[y] - eq_opening[y] - eq_tci[y], 1) for y in OPENING_KEY}

bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", gbp_spot(BS_TOTAL_ASSETS)),
        ("Loans and advances to customers", gbp_spot(BS_LOANS_CUSTOMERS)),
        ("Amounts owed to other depositors", gbp_spot(BS_DEPOSITORS)),
        ("Total equity", gbp_spot(BS_TOTAL_EQUITY)),
    ],
    balance_sheet_unit="£'000 (conv. from EUR)",
    income_statement_totals=[
        ("Net interest income", gbp_avg(IS_NET_INTEREST_INCOME)),
        ("General administrative expenses", gbp_avg(IS_ADMIN_EXPENSES)),
        ("Profit for the year after taxation", gbp_avg(IS_PROFIT_AFTER_TAX)),
    ],
    income_statement_unit="£'000 (conv. from EUR)",
    equity_changes_totals=[
        ("Opening equity", eq_opening),
        ("Total comprehensive income for the year", eq_tci),
        ("Other movements, net (FX translation effect)", eq_other),
        ("Closing equity", eq_closing),
    ],
    equity_changes_unit="£'000 (conv. from EUR) - FY2021 omitted, see Statement of Changes in Equity sheet's note",
    cash_flow_totals=[
        ("Net cash from/(used in) operating activities", OPERATING_GBP),
        ("Net cash from/(used in) investing activities", INVESTING_GBP),
        ("Cash and cash equivalents at end of year", CLOSING_GBP),
    ],
    cash_flow_unit="£'000 (conv. from EUR)",
    ratios=[
        ("CET1 Ratio", CAPITAL_RATIO),
        ("Tier 1 Ratio", CAPITAL_RATIO),
        ("Total Capital Ratio", CAPITAL_RATIO),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own "
         "source citation for the underlying document/page. All capital ratios are identical every year (no "
         "AT1/Tier 2 capital) so all three lines overlap on the chart. The Statement of Changes in Equity "
         "block omits FY2021 - no verified FY2020 EUR/GBP rate exists for this bank (see that sheet's own note).",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/BANK SEPAH INTERNATIONAL FINANCIALS.xlsx")
