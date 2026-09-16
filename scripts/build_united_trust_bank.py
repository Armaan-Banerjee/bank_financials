import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook


# PILLAR-3-ONLY WORKBOOK
# United Trust Bank Limited (company 00549690, FRN 204463) is the regulated
# operating bank within UTB Partners Plc.  The available Pillar 3 disclosures
# are prepared on the consolidated UTB Partners group basis, not as a solo UTB
# series.  The statutory accounts omit a cash-flow statement; consequently the
# workbook records the limitation and presents the available regulatory data.

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021", "FY2020"]
YEAR_LABEL = {y: y for y in YEARS}

# The FY2024 Pillar 3 URL is DEAD (see P3_DEAD_URL_NOTE below); it is preserved
# here and replaced by a Wayback snapshot in the P3 dict. Every other year's URL
# was re-checked 2026-09-16 and is still LIVE (HTTP 200, Content-Type
# application/pdf) - they are deliberately left pointing at the publisher.
ORIG_P3_2024 = "https://www.utbank.co.uk/wp-content/uploads/2025/03/UTB-Partners-Pillar-3-Disclosure-2024.pdf"

P3 = {
    "FY2025": "https://www.utbank.co.uk/wp-content/uploads/2026/03/UTB-Partners-Pillar-3-Disclosure-2025.pdf",
    # DEAD original replaced by Wayback "id_" snapshot; verified 2026-09-16,
    # 215,127 bytes, 13pp, cover reads "UTB Partners Plc / Pillar 3 disclosures /
    # as at 31 December 2024".
    "FY2024": "https://web.archive.org/web/20250913035253id_/" + ORIG_P3_2024,
    "FY2023": "https://www.utbank.co.uk/wp-content/uploads/2024/03/UTB-Partners-Pillar-3-Disclosure-2023.pdf",
    "FY2022": "https://www.utbank.co.uk/wp-content/uploads/2023/03/UTB-Partners-Pillar-3-Disclosure-2022-.pdf",
    "FY2021": "https://rebrand-dev.utbank.co.uk/wp-content/uploads/2022/03/UTB-Partners-Pillar-3-Disclosure-2021-FINAL1-.pdf",
    "FY2020": "https://www.utbank.co.uk/wp-content/uploads/2021/05/UTB_Pillar3_Disclosure_2020.pdf",
}

P3_DEAD_URL_NOTE = (
    "DEAD SOURCE URL REGISTER (recorded 2026-09-16, nothing deleted). The FY2024 Pillar 3 disclosure was"
    " published at " + ORIG_P3_2024 + " and that URL is now DEAD: re-fetched 2026-09-16 it returns HTTP 404"
    " with Content-Type text/html, not a PDF. It is kept on the record here rather than deleted so the"
    " provenance of the FY2024 figures stays readable now the publisher no longer serves the file. The"
    " working replacement, cited on every sheet that uses FY2024, is the Wayback Machine snapshot"
    " https://web.archive.org/web/20250913035253id_/" + ORIG_P3_2024 + " - given in the 'id_' form, which"
    " returns the original archived bytes rather than the Wayback viewer page. Verified on fetch: begins"
    " '%PDF', 215,127 bytes, 13pp, and its cover reads 'UTB Partners Plc / Pillar 3 disclosures / as at 31"
    " December 2024', confirming the reporting year from the document itself rather than from its filename."
    " SCOPE OF THE OUTAGE, CHECKED NOT ASSUMED: all six Pillar 3 URLs in this workbook were re-tested on"
    " 2026-09-16 and FY2024 is the ONLY dead one. FY2025, FY2023, FY2022, FY2021 and FY2020 all still return"
    " HTTP 200 with Content-Type application/pdf from the publisher and are therefore still cited live, not"
    " repointed - an archived copy is not substituted for a document the publisher still serves. The FY2025"
    " edition is already sourced in this workbook (utbank.co.uk/wp-content/uploads/2026/03/, live, 216,894"
    " bytes), so there is no missing recent edition to add. No figure was changed by this URL repair."
)
ACCOUNTS_2024 = "https://www.utbank.co.uk/wp-content/uploads/2025/03/UTB-Report-and-Accounts-2024.pdf"
CH = "https://find-and-update.company-information.service.gov.uk/company/00549690/filing-history"

ENTITY_NOTE = (
    "ENTITY AND BASIS: United Trust Bank Limited (company 00549690, FCA/PRA FRN 204463) is the regulated,"
    " material operating bank and wholly-owned subsidiary of UTB Partners Plc. The Pillar 3 reports used here"
    " constitute consolidated disclosures of UTB Partners Plc; UTB Partners is a financial holding company and"
    " the group is supervised on a consolidated basis. SOS Intelligence is immaterial and excluded from regulatory"
    " consolidation. Accordingly, all figures in this workbook are explicitly labelled CONSOLIDATED UTB PARTNERS"
    " BASIS and must not be read as standalone United Trust Bank Limited figures."
)

EXEMPTION_NOTE = (
    "CASH-FLOW LIMITATION: United Trust Bank Limited's published 2024 Report and Accounts contains the"
    " Income Statement, Statement of Comprehensive Income, Statement of Financial Position and Statement of"
    " Changes in Equity, but no Statement of Cash Flows; the Companies House filing history likewise describes"
    " the accounts as full accounts. The available accounts and source material do not provide a cash-flow"
    " statement suitable for this workbook. The Cash Flow Statement sheet therefore records this limitation"
    " rather than inferring or fabricating cash-flow values. Re-checked directly against the FY2020 Report and"
    " Accounts (filed at Companies House 15 Mar 2021): its own table of contents lists only an Income Statement"
    " (p.44), Statement of Comprehensive Income (p.44), Statement of Financial Position (p.45), Statement of"
    " Changes in Equity (p.46) and Notes (pp.47-74) - no Statement of Cash Flows is present for FY2020 either,"
    " so the exemption is confirmed to hold across the full FY2020-FY2025 window, not merely assumed from later"
    " years' precedent."
)

FY2020_BASIS_NOTE = (
    "FY2020 PILLAR 3 BASIS DIFFERS FROM FY2021-FY2025: UTB Partners Plc's own Pillar 3 disclosure series only"
    " begins with the FY2021 report (titled 'UTB Partners Limited Pillar 3 disclosures', the holding company's"
    " name at the time); no UTB Partners-basis Pillar 3 disclosure exists for FY2020, and the FY2021 disclosure"
    " carries no FY2020 comparative figures of any kind (it predates the KM1/OV1 comparative-column template"
    " introduced from the FY2022 disclosure onward). The only FY2020 Pillar 3 document that exists is United"
    " Trust Bank Limited's own, separately-published, SOLO/ENTITY-BASIS 'Pillar 3 disclosures as at 31 December"
    " 2020' (44 pages, published May 2021, confirmed live at its original URL and also archived by the Wayback"
    " Machine, 20211208184401 snapshot). FY2020 figures on every Pillar 3 metric sheet in this workbook are"
    " therefore UTB Limited solo-entity figures, not consolidated UTB Partners Plc group figures like"
    " FY2021-FY2025 - both are the bank's own genuinely published numbers, but they are not directly comparable"
    " across this basis change, and no group-consolidated FY2020 figures exist to substitute. In practice the"
    " gap between the two bases is small for FY2020 specifically (UTB Partners Plc's own consolidation note"
    " elsewhere in this workbook describes SOS Intelligence, the only other group entity, as immaterial), but"
    " the distinction is preserved here rather than blended silently."
)


def sources():
    return (
        "Sources - consolidated UTB Partners Plc basis except FY2020 (solo UTB Limited basis - see note"
        " below), £'000 unless stated:\n"
        "FY2025: UTB Partners Pillar 3 Disclosure 2025, section 2.1 Table KM1, printed p.7 (corrected"
        " 2026-09-16 from 'pp.6-7'; printed p.6 is prose, the whole table is on p.7) - " + P3["FY2025"] + "\n"
        "FY2024: UTB Partners Pillar 3 Disclosure 2024, section 2.1 Table KM1, printed p.7 (footer reads"
        " 'Page 7 of 13'; corrected 2026-09-16 from 'pp.6-7') - " + P3["FY2024"]
        + " (the Bank's own published URL, " + ORIG_P3_2024 + ", is DEAD as at 2026-09-16 and returns HTTP"
        " 404; the Wayback 'id_' snapshot cited here is the working replacement - see the dead source URL"
        " register below)\n"
        "FY2023: UTB Partners Pillar 3 Disclosure 2023, Appendix 1 Table KM1, pp.44-45 - " + P3["FY2023"] + "\n"
        "FY2022: UTB Partners Pillar 3 Disclosure 2022, Appendix 1 Table KM1, p.43 - " + P3["FY2022"] + "\n"
        "FY2021: UTB Partners Pillar 3 Disclosure 2022 comparative column and 2021 disclosure, Appendix 1 /"
        " own-funds and leverage templates - " + P3["FY2021"] + "\n"
        "FY2020: United Trust Bank Limited Pillar 3 disclosures as at 31 December 2020 (solo basis),"
        " Appendix 1 Own Funds Disclosure Template p.39 and Appendix 2 Leverage Ratio Template pp.41-42 - "
        + P3["FY2020"] + "\n"
        "Accounts cross-check: United Trust Bank Report and Accounts 2024, pp.47-50 - " + ACCOUNTS_2024 + "\n"
        "Companies House entity and filing history (company 00549690) - " + CH + "\n\n"
        + ENTITY_NOTE + "\n\n" + FY2020_BASIS_NOTE + "\n\n" + P3_DEAD_URL_NOTE
    )


CH_ACCOUNTS = {
    "FY2025": CH + "/MzUyMTk0MjExM2FkaXF6a2N4/document?format=pdf&download=0",
    "FY2024": CH + "/MzQ2MzA3OTAyMGFkaXF6a2N4/document?format=pdf&download=0",
    "FY2023": CH + "/MzQzMTMzNTk5OGFkaXF6a2N4/document?format=pdf&download=0",
    "FY2022": CH + "/MzM3NzEyOTIyNWFkaXF6a2N4/document?format=pdf&download=0",
    "FY2021": CH + "/MzMzMjI5NTg0MGFkaXF6a2N4/document?format=pdf&download=0",
    "FY2020": CH + "/MzI5NDM0MjUzMGFkaXF6a2N4/document?format=pdf&download=0",
}

STATEMENTS_NOTE = (
    "ENTITY AND BASIS - STATEMENTS ONLY: unlike the Pillar 3 sheets in this workbook (consolidated UTB"
    " Partners Plc basis for FY2021-FY2025; solo UTB Limited basis for FY2020 - see that sheet's own note),"
    " the Balance Sheet, Profit & Loss, Statement of Changes in Equity and Asset Quality sheets are sourced"
    " from United Trust Bank Limited's own entity-level statutory accounts (Companies House, company"
    " 00549690), which report full Income Statement, Statement of Comprehensive Income, Statement of"
    " Financial Position and Statement of Changes in Equity for all 6 years - only the Statement of Cash"
    " Flows is genuinely absent from the entity accounts (see the Cash Flow Statement sheet's note). All 6"
    " filings are scanned/image-only; figures were transcribed directly from the rendered filing pages."
)


def statements_sources():
    return (
        "Sources - United Trust Bank Limited entity-level statutory accounts (Companies House filing"
        " history, company 00549690), £'000:\n"
        "FY2025: Report and Accounts 2025, Income Statement/Statement of Comprehensive Income p.45,"
        " Statement of Financial Position p.46, Statement of Changes in Equity p.47 - " + CH_ACCOUNTS["FY2025"] + "\n"
        "FY2024: comparative column in the Report and Accounts 2025 (own FY2024 filing not separately"
        " re-transcribed; figures are identical audited comparatives) - " + CH_ACCOUNTS["FY2024"] + "\n"
        "FY2023: Report and Accounts 2023, Income Statement/Statement of Comprehensive Income p.49,"
        " Statement of Financial Position p.50, Statement of Changes in Equity p.51 - " + CH_ACCOUNTS["FY2023"] + "\n"
        "FY2022: Report and Accounts 2022, Income Statement/Statement of Comprehensive Income p.57,"
        " Statement of Financial Position p.58, Statement of Changes in Equity p.59 - " + CH_ACCOUNTS["FY2022"] + "\n"
        "FY2021: comparative column in the Report and Accounts 2022 (own FY2021 filing not separately"
        " re-transcribed; figures are identical audited comparatives) - " + CH_ACCOUNTS["FY2021"] + "\n"
        "FY2020: Report and Accounts 2020 (filed at Companies House 15 Mar 2021), Income Statement/Statement"
        " of Comprehensive Income p.44, Statement of Financial Position p.45, Statement of Changes in Equity"
        " p.46 - " + CH_ACCOUNTS["FY2020"] + "\n\n"
        + STATEMENTS_NOTE
    )


def asset_quality_sources():
    return (
        "Sources - United Trust Bank Limited entity-level statutory accounts (Companies House filing"
        " history, company 00549690), Note 8 (Loans and advances to customers) and Note 9 (Provision for"
        " impairment losses on loans and advances to customers), £'000:\n"
        "FY2025/FY2024: Report and Accounts 2025, pp.54-55 - " + CH_ACCOUNTS["FY2025"] + "\n"
        "FY2023/FY2022: Report and Accounts 2023, pp.57-58 - " + CH_ACCOUNTS["FY2023"] + "\n"
        "FY2021: comparative column in the Report and Accounts 2022, pp.65-66 - " + CH_ACCOUNTS["FY2022"] + "\n"
        "FY2020: Report and Accounts 2020, Note 9 (Loans and advances to customers) p.58, Note 10 (Provision"
        " for impairment losses on loans and advances) p.60 - " + CH_ACCOUNTS["FY2020"] + "\n\n"
        "CLASSIFICATION: United Trust Bank Limited reports under FRS 102 (UK GAAP), not IFRS 9; there is no"
        " Stage 1/2/3 staged-ECL split in the source. Asset Quality is instead built from the entity's own"
        " loan-product portfolios (Property / Mortgages / Asset Finance / Finance lease and hire purchase)"
        " and its Individual/Collective impairment-provision classification. Note 9's own portfolio-level"
        " breakdown labels the finance-lease-and-hire-purchase book 'Asset Finance portfolio', distinct from"
        " Note 8's separately-disclosed (near-nil-impairment) 'Asset Finance portfolio loan receivables'"
        " direct-lending book; both are reproduced as their own rows below, matching the source, rather than"
        " merged. In FY2025 and FY2024 only, the Mortgages portfolio's own net figure also includes a fair"
        " value hedge adjustment (+£1,763k in FY2025, -£3,363k in FY2024) that is not part of the impairment"
        " provision; this is why gross-less-impairment does not exactly equal the net total in those two"
        " years (no such adjustment existed in FY2023-FY2021).\n\n"
        "FY2020 GENUINE DATA-QUALITY LIMITATION: FY2020's own Report and Accounts (Note 9) and its own solo"
        " Pillar 3 disclosure both classify loans and advances to customers only as 'Loan receivables' vs"
        " 'Finance lease and hire purchase receivables', with impairment provision split only 'Individual' vs"
        " 'Collective' - the finer Property/Mortgages/Asset Finance product-portfolio breakdown used in"
        " FY2021-FY2025 was not yet disclosed. This is not an access gap: it was checked directly against"
        " FY2020's own filed accounts, and confirmed absent from every other FY2020/FY2021-adjacent document"
        " reviewed (the FY2021 asset quality figures in this workbook are themselves only available via the"
        " FY2022 report's comparative column, i.e. product-portfolio detail was not disclosed in the FY2020 or"
        " FY2021 filings' own year - it starts from the FY2022 report). Accordingly the Property / Mortgages /"
        " Asset Finance portfolio rows are blank for FY2020 (genuinely not disclosed at that granularity, not"
        " zero), while the Finance lease and hire purchase row and every TOTAL row use FY2020's own real,"
        " reported combined figures; the Individual/Collective classification section is fully populated for"
        " FY2020 since that split is disclosed at the aggregate level.\n\n" + STATEMENTS_NOTE
    )


RWA_NOTE = (
    "RWA BREAKDOWN - CONSOLIDATED UTB PARTNERS BASIS, Table UK OV1 (Overview of risk-weighted exposure"
    " amounts): each year uses that year's own disclosure document's own-year column, consistent with"
    " project convention. The FY2021 disclosure predates the OV1 template (it only publishes an 8%-capital"
    " exposure-class table); FY2021's OV1-format category split is instead taken from the FY2022 Pillar 3"
    " disclosure's own 2021 comparative column, the earliest year an OV1 table is available. Each year's OV1"
    " Total differs immaterially (<0.02%) from the Total RWAs metric sheet's KM1-sourced figure - both are"
    " the bank's own published numbers; the gap is a KM1-vs-OV1 rounding difference of the same kind already"
    " documented on the Total RWAs sheet, not a data error.\n\n"
    "FY2020 (2026-09-08 correction — now included on its own SOLO basis, derived, not OV1-format): no"
    " OV1-format category split (Credit risk / CCR / Securitisation / Operational risk) exists for FY2020"
    " anywhere, and no later disclosure carries a FY2020 comparative OV1 column to fall back on (the FY2022"
    " disclosure's own OV1 table only goes back to its 2021 (T-1) comparative, one year, not two). FY2020's own"
    " document instead publishes a differently-structured 'Pillar 1 capital requirement' table (section 5.2,"
    " p.28) which DOES split by RISK TYPE - not the exposure-class table (8%-capital by CRR exposure class:"
    " Central government, Institutions, Retail, Secured by mortgages, Exposures in default, Other items, which"
    " sits ABOVE it in the same table and is itself only a further breakdown of the credit risk row, not used"
    " here): 'Credit risk minimum Pillar 1 capital requirement' (93,316), 'Operational risk Pillar 1 capital"
    " requirement (basic indicator approach)' (10,257), and market risk is a genuine disclosed nil ('the Bank"
    " does not have a trading book and as such its exposure to market risk is immaterial') - summing to the"
    " table's own 'Pillar 1 capital requirement' total (103,573). Each figure is that capital requirement x 12.5"
    " (= / 8%), the standard Basel/CRR identity - not an estimate. This FY2020 breakdown is SOLO basis (United"
    " Trust Bank Limited entity-level, per that year's own document title), NOT consolidated UTB Partners Plc"
    " basis like every other year on this sheet - shown in its own separate SECTION block, not blended with the"
    " OV1 rows above. FY2020's own Total RWA figure (1,294,667, from Appendix 1 row 60) is also on the Total"
    " RWAs Pillar 3 metric sheet; this derived breakdown's own total (1,294,662.5) ties to within £5k."
)


def rwa_sources():
    return (
        "Sources - consolidated UTB Partners Plc basis (FY2020: no comparable data exists - see note), Table"
        " UK OV1, £'000:\n"
        "FY2025: UTB Partners Pillar 3 Disclosure 2025, Table UK OV1, p.11 - " + P3["FY2025"] + "\n"
        "FY2024: UTB Partners Pillar 3 Disclosure 2024, Table UK OV1, p.11 - " + P3["FY2024"] + "\n"
        "FY2023: UTB Partners Pillar 3 Disclosure 2023, Table UK OV1, pp.31-32 - " + P3["FY2023"] + "\n"
        "FY2022: UTB Partners Pillar 3 Disclosure 2022, Table UK OV1, p.32 - " + P3["FY2022"] + "\n"
        "FY2021: UTB Partners Pillar 3 Disclosure 2022, Table UK OV1, 2021 (T-1) comparative column,"
        " p.32 - " + P3["FY2022"] + "\n"
        "FY2020 (SOLO basis, DERIVED via x12.5, see note): United Trust Bank Limited Pillar 3 disclosures as at"
        " 31 December 2020, section 5.2 'Pillar 1 capital requirement' table, p.28, and Appendix 1 row 60 (Total"
        " RWA figure, used on the Total RWAs sheet) - " + P3["FY2020"] + "\n\n"
        + RWA_NOTE
    )


bw = BankWorkbook(
    bank_name="United Trust Bank Limited (consolidated UTB Partners basis)",
    years=YEARS,
    year_label=YEAR_LABEL,
    header_color="1B4965",
)

bw.add_balance_sheet_sheet(
    title="United Trust Bank Limited — Balance Sheet",
    subtitle="Entity (Company-only) basis, £'000. Statement of Financial Position.",
    rows=[
        ("SECTION", "Assets", {}),
        ("DATA", "Loans and advances to banks/central banks", {
            "FY2025": 369339 + 63472, "FY2024": 204053 + 77909, "FY2023": 241996 + 52696,
            "FY2022": 243506 + 25356, "FY2021": 181074 + 23577, "FY2020": 151160 + 54174,
        }),
        ("DATA", "Loans and advances to customers", {
            "FY2025": 3895213, "FY2024": 3487345, "FY2023": 3104356,
            "FY2022": 2426021, "FY2021": 1808607, "FY2020": 1646322,
        }),
        ("DATA", "Loans to group companies", {
            "FY2025": 700, "FY2024": 499, "FY2023": 369, "FY2022": 205, "FY2021": 120,
        }),
        ("DATA", "Debt securities - UK government securities (amortised cost)", {
            "FY2025": 100346, "FY2024": 118562, "FY2023": 19510, "FY2022": 84783, "FY2021": 221816,
        }),
        ("DATA", "Derivative financial instruments (assets)", {
            "FY2025": 1207, "FY2024": 3600, "FY2023": 2039, "FY2022": 3561,
        }),
        ("DATA", "Equity shares", {
            "FY2025": 1300, "FY2024": 1300, "FY2023": 1000, "FY2022": 1000,
        }),
        ("DATA", "Tangible fixed assets", {
            "FY2025": 757, "FY2024": 697, "FY2023": 1003, "FY2022": 812, "FY2021": 552, "FY2020": 667,
        }),
        ("DATA", "Intangible assets", {
            "FY2025": 7885, "FY2024": 6790, "FY2023": 5288, "FY2022": 4092, "FY2021": 3280, "FY2020": 3071,
        }),
        ("DATA", "Other assets", {
            "FY2025": 10418, "FY2024": 12505, "FY2023": 11911, "FY2022": 8981, "FY2021": 15152, "FY2020": 12538,
        }),
        ("TOTAL", "Total assets", {
            "FY2025": 4450637, "FY2024": 3913260, "FY2023": 3440168,
            "FY2022": 2798317, "FY2021": 2254178, "FY2020": 1867932,
        }),
        ("SECTION", "Liabilities", {}),
        ("DATA", "Deposits from customers", {
            "FY2025": 3847845, "FY2024": 3407271, "FY2023": 2797361,
            "FY2022": 2208300, "FY2021": 1715596, "FY2020": 1601361,
        }),
        ("DATA", "Loans from banks/central banks", {
            "FY2025": 80462, "FY2024": 60648, "FY2023": 263441, "FY2022": 302135, "FY2021": 300079, "FY2020": 50013,
        }),
        ("DATA", "Loans from group companies", {
            "FY2025": 1678, "FY2024": 3048, "FY2023": 1522, "FY2022": 1879, "FY2021": 1259, "FY2020": 518,
        }),
        ("DATA", "Derivative financial instruments (liabilities)", {
            "FY2025": 2388, "FY2024": 279, "FY2023": 1329, "FY2022": 96,
        }),
        ("DATA", "Other liabilities", {
            "FY2025": 18224, "FY2024": 22549, "FY2023": 20076, "FY2022": 17474, "FY2021": 12356, "FY2020": 8763,
        }),
        ("DATA", "Long-term subordinated debt", {
            "FY2025": 27204, "FY2024": 56603, "FY2023": 56640, "FY2022": 29324, "FY2021": 29256, "FY2020": 33241,
        }),
        ("TOTAL", "Total liabilities", {
            "FY2025": 3977801, "FY2024": 3550398, "FY2023": 3140369,
            "FY2022": 2559208, "FY2021": 2058546, "FY2020": 1693896,
        }),
        ("SECTION", "Capital and Reserves", {}),
        ("DATA", "Share capital", {
            "FY2025": 10500, "FY2024": 10350, "FY2023": 10350, "FY2022": 10350, "FY2021": 10350, "FY2020": 10350,
        }),
        ("DATA", "Share premium", {
            "FY2025": 33030, "FY2024": 25680, "FY2023": 25680, "FY2022": 25680, "FY2021": 25680, "FY2020": 25680,
        }),
        ("DATA", "Contingent convertible securities", {
            "FY2025": 65913, "FY2024": 16851, "FY2023": 16851, "FY2022": 16851, "FY2021": 16851, "FY2020": 16851,
        }),
        ("DATA", "Retained earnings", {
            "FY2025": 363393, "FY2024": 309981, "FY2023": 246918, "FY2022": 186228, "FY2021": 142751, "FY2020": 121155,
        }),
        ("TOTAL", "Total capital and reserves", {
            "FY2025": 472836, "FY2024": 362862, "FY2023": 299799,
            "FY2022": 239109, "FY2021": 195632, "FY2020": 174036,
        }),
        ("TOTAL", "Total equity and liabilities", {
            "FY2025": 4450637, "FY2024": 3913260, "FY2023": 3440168,
            "FY2022": 2798317, "FY2021": 2254178, "FY2020": 1867932,
        }),
    ],
    sources_text=(
        statements_sources() + "\n\n"
        "DEBT SECURITIES COMPOSITION: Note 10 'Debt securities' of each year's own Notes to the Financial"
        " Statements (Report and Accounts 2025 p.56 for FY2025/FY2024; Report and Accounts 2023 p.59 for"
        " FY2023; Report and Accounts 2022 p.67 for FY2022/FY2021) shows the entire debt securities balance"
        " in a single line, 'Issued by public bodies - government securities', in every one of the 5 years"
        " covered (FY2021-FY2025) - i.e. 100% UK government/gilt issuance, with no supranational, corporate"
        " or other-issuer holdings disclosed in any year. Note 19 'Financial instruments' of the same"
        " accounts classifies debt securities as 'Measured at amortised cost' throughout, with no FVOCI/FVTPL/"
        " available-for-sale/trading debt securities holdings disclosed. There is accordingly no sub-row"
        " breakdown to add; the row label above has been amended in place to reflect this."
    ),
    first_col_width=58,
    source_height=230,
)

bw.add_income_statement_sheet(
    title="United Trust Bank Limited — Profit & Loss",
    subtitle="Entity (Company-only) basis, £'000. Income Statement and Statement of Comprehensive Income.",
    rows=[
        ("DATA", "Interest receivable and similar income", {
            "FY2025": 342801, "FY2024": 320696, "FY2023": 259393, "FY2022": 153034, "FY2021": 119015, "FY2020": 105322,
        }),
        ("DATA", "Interest payable and similar charges", {
            "FY2025": -166396, "FY2024": -155666, "FY2023": -105094, "FY2022": -38374, "FY2021": -23857, "FY2020": -26271,
        }),
        ("TOTAL", "Net interest income", {
            "FY2025": 176405, "FY2024": 165030, "FY2023": 154299, "FY2022": 114660, "FY2021": 95158, "FY2020": 79051,
        }),
        ("DATA", "Other income/(charges)", {
            "FY2025": 26, "FY2024": -59, "FY2023": -153, "FY2022": -18, "FY2021": -18, "FY2020": 3,
        }),
        ("TOTAL", "Operating income", {
            "FY2025": 176431, "FY2024": 164971, "FY2023": 154146, "FY2022": 114642, "FY2021": 95140, "FY2020": 79054,
        }),
        ("DATA", "Administrative expenses", {
            "FY2025": -82353, "FY2024": -75360, "FY2023": -65369, "FY2022": -51245, "FY2021": -43483, "FY2020": -34252,
        }),
        ("DATA", "Depreciation and amortisation", {
            "FY2025": -1763, "FY2024": -1578, "FY2023": -1256, "FY2022": -1452, "FY2021": -765, "FY2020": -678,
        }),
        ("DATA", "Provision for impairment losses", {
            "FY2025": -13629, "FY2024": -1664, "FY2023": -4782, "FY2022": -1789, "FY2021": -6455, "FY2020": -13465,
        }),
        ("TOTAL", "Profit on ordinary activities before tax", {
            "FY2025": 78686, "FY2024": 86369, "FY2023": 82739, "FY2022": 60156, "FY2021": 44437, "FY2020": 30659,
        }),
        ("DATA", "Tax charge for the year", {
            "FY2025": -18006, "FY2024": -20597, "FY2023": -19465, "FY2022": -14761, "FY2021": -9015, "FY2020": -5749,
        }),
        ("TOTAL", "Profit after tax retained for the financial year", {
            "FY2025": 60680, "FY2024": 65772, "FY2023": 63274, "FY2022": 45395, "FY2021": 35422, "FY2020": 24910,
        }),
        ("SECTION", "Statement of Comprehensive Income", {}),
        ("DATA", "Other comprehensive income", {
            "FY2025": 0, "FY2024": 0, "FY2023": 0, "FY2022": 0, "FY2021": 0, "FY2020": 0,
        }),
        ("TOTAL", "Total comprehensive income", {
            "FY2025": 60680, "FY2024": 65772, "FY2023": 63274, "FY2022": 45395, "FY2021": 35422, "FY2020": 24910,
        }),
    ],
    sources_text=(
        statements_sources() + "\n\n"
        "The FY2022 report's own tax-reconciliation note (Note 6) shows FY2021 profit before tax as"
        " £44,368k, £69k below the Income Statement's own FY2021 figure of £44,437k used here; both are"
        " genuine figures from the same source document and the gap is not resolved further. No OCI items"
        " (revaluation reserves, FX translation, cash-flow hedge reserves, etc.) are reported in any of the"
        " 5 years - profit for the year equals total comprehensive income throughout."
    ),
    first_col_width=58,
    source_height=240,
)

bw.add_equity_changes_sheet(
    title="United Trust Bank Limited — Statement of Changes in Equity",
    subtitle="Entity (Company-only) basis, £'000. Chronological roll-forward, 31 December 2019 to 31 December 2025.",
    headers=["Share capital", "Share premium", "Contingent convertible securities", "Retained earnings", "Total"],
    rows=[
        ("TOTAL", "At 31 December 2019", (10350, 25680, 16851, 98093, 150974)),
        ("DATA", "Profit for the financial year", (None, None, None, 24910, 24910)),
        ("DATA", "Coupon paid on contingent convertible securities", (None, None, None, -1848, -1848)),
        ("TOTAL", "At 31 December 2020", (10350, 25680, 16851, 121155, 174036)),
        ("DATA", "Profit for the financial year", (None, None, None, 35422, 35422)),
        ("DATA", "Coupon paid on contingent convertible securities", (None, None, None, -1826, -1826)),
        ("DATA", "Dividend paid", (None, None, None, -12000, -12000)),
        ("TOTAL", "At 31 December 2021", (10350, 25680, 16851, 142751, 195632)),
        ("DATA", "Profit for the financial year", (None, None, None, 45395, 45395)),
        ("DATA", "Coupon paid on contingent convertible securities", (None, None, None, -1918, -1918)),
        ("DATA", "Share based payments charge", (None, None, None, 619, 619)),
        ("DATA", "Share based payments recharged to parent", (None, None, None, -619, -619)),
        ("DATA", "Dividend paid", (None, None, None, 0, 0)),
        ("TOTAL", "At 31 December 2022", (10350, 25680, 16851, 186228, 239109)),
        ("DATA", "Profit for the financial year", (None, None, None, 63274, 63274)),
        ("DATA", "Coupon payable on contingent convertible securities", (None, None, None, -2584, -2584)),
        ("DATA", "Share based payments charge", (None, None, None, 744, 744)),
        ("DATA", "Share based payments recharged to parent", (None, None, None, -744, -744)),
        ("TOTAL", "At 31 December 2023", (10350, 25680, 16851, 246918, 299799)),
        ("DATA", "Profit for the financial year", (None, None, None, 65772, 65772)),
        ("DATA", "Coupon payable on contingent convertible securities", (None, None, None, -2709, -2709)),
        ("DATA", "Share based payments charge", (None, None, None, 1526, 1526)),
        ("DATA", "Share based payments recharged from parent", (None, None, None, -1526, -1526)),
        ("TOTAL", "At 31 December 2024", (10350, 25680, 16851, 309981, 362862)),
        ("DATA", "Profit for the financial year", (None, None, None, 60680, 60680)),
        ("DATA", "Shares issued (net of issue costs)", (150, 7350, None, None, 7500)),
        ("DATA", "Contingent convertible securities issued (net of issue costs)", (None, None, 49062, None, 49062)),
        ("DATA", "Coupon payable on contingent convertible securities", (None, None, None, -7268, -7268)),
        ("DATA", "Share based payments charge", (None, None, None, 1805, 1805)),
        ("DATA", "Share based payments recharged from parent", (None, None, None, -1805, -1805)),
        ("TOTAL", "At 31 December 2025", (10500, 33030, 65913, 363393, 472836)),
    ],
    sources_text=statements_sources(),
    first_col_width=54,
    source_height=210,
)

bw.add_cash_flow_sheet(
    title="United Trust Bank Limited — Cash Flow Statement",
    subtitle="Not available in the published statutory accounts; this is a Pillar-3-only workbook.",
    rows=[
        ("SECTION", "No Statement of Cash Flows available for the covered entity", {}),
        ("DATA", "See the source note below. No cash-flow values are inferred.", {}),
    ],
    sources_text=ENTITY_NOTE + "\n\n" + EXEMPTION_NOTE + "\n\n" + sources(),
    first_col_width=90,
    source_height=270,
    unit_suffix="",
)

bw.add_asset_quality_sheet(
    title="United Trust Bank Limited — Asset Quality",
    subtitle="Entity (Company-only) basis, £'000. FRS 102 classification (no IFRS 9 stage split disclosed) - see source note.",
    rows=[
        ("SECTION", "Gross loans and advances to customers, by portfolio", {}),
        ("DATA", "Property portfolio", {
            "FY2025": 1967527, "FY2024": 1812420, "FY2023": 1656511, "FY2022": 1314165, "FY2021": 1030804,
        }),
        ("DATA", "Mortgages portfolio", {
            "FY2025": 1369028, "FY2024": 1223848, "FY2023": 1065867, "FY2022": 792848, "FY2021": 577629,
        }),
        ("DATA", "Asset Finance portfolio loan receivables", {
            "FY2025": 30646, "FY2024": 12639, "FY2023": 7479, "FY2022": 3568, "FY2021": 0,
        }),
        ("DATA", "Finance lease and hire purchase receivables (net investment)", {
            "FY2025": 545508, "FY2024": 450120, "FY2023": 382623, "FY2022": 320348, "FY2021": 209457, "FY2020": 128166,
        }),
        ("TOTAL", "Gross loans and advances to customers", {
            "FY2025": 3912709, "FY2024": 3499027, "FY2023": 3112480,
            "FY2022": 2430929, "FY2021": 1817890, "FY2020": 1655224,
        }),
        ("SECTION", "Less: provision for impairment losses, by portfolio", {}),
        ("DATA", "Property portfolio", {
            "FY2025": -16163, "FY2024": -4449, "FY2023": -4320, "FY2022": -2972, "FY2021": -5531,
        }),
        ("DATA", "Mortgages portfolio", {
            "FY2025": -1651, "FY2024": -2184, "FY2023": -2209, "FY2022": -985, "FY2021": -1135,
        }),
        ("DATA", "Asset Finance portfolio loan receivables", {
            "FY2025": -125, "FY2024": 0, "FY2023": 0, "FY2022": 0, "FY2021": 0,
        }),
        ("DATA", "Finance lease and hire purchase receivables", {
            "FY2025": -1320, "FY2024": -1686, "FY2023": -1595, "FY2022": -951, "FY2021": -2617, "FY2020": -776,
        }),
        ("TOTAL", "Total provision for impairment losses", {
            "FY2025": -19259, "FY2024": -8319, "FY2023": -8124, "FY2022": -4908, "FY2021": -9283, "FY2020": -8902,
        }),
        ("SECTION", "Net loans and advances to customers, by portfolio", {}),
        ("DATA", "Property portfolio", {
            "FY2025": 1951364, "FY2024": 1807971, "FY2023": 1652191, "FY2022": 1311193, "FY2021": 1025273,
        }),
        ("DATA", "Mortgages portfolio (incl. fair value hedge adjustment)", {
            "FY2025": 1369140, "FY2024": 1218301, "FY2023": 1063658, "FY2022": 791863, "FY2021": 576494,
        }),
        ("DATA", "Asset Finance portfolio loan receivables", {
            "FY2025": 30521, "FY2024": 12639, "FY2023": 7479, "FY2022": 3568, "FY2021": 0,
        }),
        ("DATA", "Finance lease and hire purchase receivables", {
            "FY2025": 544188, "FY2024": 448434, "FY2023": 381028, "FY2022": 319397, "FY2021": 206840, "FY2020": 127390,
        }),
        ("TOTAL", "Net loans and advances to customers", {
            "FY2025": 3895213, "FY2024": 3487345, "FY2023": 3104356,
            "FY2022": 2426021, "FY2021": 1808607, "FY2020": 1646322,
        }),
        ("SECTION", "Impairment provision by FRS 102 classification (balance at 31 December)", {}),
        ("DATA", "Individual impairment provision", {
            "FY2025": 16053, "FY2024": 5248, "FY2023": 5350, "FY2022": 2618, "FY2021": 7471, "FY2020": 7130,
        }),
        ("DATA", "Collective impairment provision", {
            "FY2025": 3206, "FY2024": 3071, "FY2023": 2774, "FY2022": 2290, "FY2021": 1812, "FY2020": 1772,
        }),
        ("TOTAL", "Total impairment provision", {
            "FY2025": 19259, "FY2024": 8319, "FY2023": 8124, "FY2022": 4908, "FY2021": 9283, "FY2020": 8902,
        }),
    ],
    sources_text=asset_quality_sources(),
    first_col_width=64,
    source_height=260,
)


# ---------------------------------------------------------------
# KM1 Key Metrics (KM1-030, 2026-09-16)
#
# Reproduced from each year's OWN edition. UTB Partners prints the UK KM1
# template in its FY2022, FY2023, FY2024 and FY2025 disclosures and in none
# before that; FY2021 is carried from the FY2022 edition's comparative column
# (see KM1_NOTE) and FY2020 is blank, because no KM1 exists for 31-Dec-20 on
# any basis.
#
# Rows the bank did not print are left BLANK, never zero, and never carried
# across from an adjacent edition. The FY2024 and FY2025 editions say in terms
# why their row sets are shorter - "Where rows of the template are not shown,
# this is because they are blank and have been removed for clarity and to
# improve readability" - so a missing row there is the bank's own editorial
# suppression of an empty row, not a gap in this transcription. Rows are held
# in the template's canonical order so the four editions line up as columns.
# ---------------------------------------------------------------
KM1_SOURCES = (
    "Sources - UTB Partners consolidated Pillar 3 basis, Table KM1, each year transcribed from the edition in"
    " which that year is the REPORTING year (not from a later edition's comparative column, except FY2021 -"
    " see the FY2021 note below). Amounts are the bank's own, rounded to the nearest GBP'000 as it presents"
    " them; ratios are reproduced at the bank's own precision, which varies by row and by edition.\n"
    "FY2025: UTB Partners Pillar 3 Disclosure 2025, section 2.1 'Key metrics', table headed KM1, printed"
    " page 7 - " + P3["FY2025"] + "\n"
    "FY2024: UTB Partners Pillar 3 Disclosure 2024, section 2.1 'Key metrics', table headed KM1, printed"
    " page 7 (the page's own footer reads 'Page 7 of 13') - " + P3["FY2024"]
    + " (Wayback 'id_' snapshot; the publisher's own URL for this edition, " + ORIG_P3_2024 + ", is dead -"
    " see the dead source URL register on the other Pillar 3 sheets)\n"
    "FY2023: UTB Partners Pillar 3 Disclosure 2023, 'Appendix 1: Table KM1 - Key Metrics', printed pages"
    " 44-45. THE TABLE BREAKS ACROSS TWO PAGES in this edition: rows 1 to 15 are on p.44 and rows UK 16a to"
    " 20 continue on p.45 - " + P3["FY2023"] + "\n"
    "FY2022: UTB Partners Pillar 3 Disclosure 2022, 'Appendix 1: Table KM1 - Key Metrics', printed page 43,"
    " printed whole on one page - " + P3["FY2022"] + "\n"
    "FY2021: no KM1 exists in that year's own edition; the column here is the 31-Dec-21 COMPARATIVE printed"
    " beside 31-Dec-22 in the FY2022 edition, printed page 43 - " + P3["FY2022"] + "\n"
    "FY2020: blank throughout - no KM1 exists for 31-Dec-20 on any basis. See the FY2020 note below.\n"
    "Page numbers above are the folios PRINTED ON THE PAGE. Verified rather than counted: the printed folio"
    " equals the PDF sheet index in all four of these documents (offset 0), and each cited page carries its"
    " own number in its footer.\n\n"
    "ENTITY (checked per column, not assumed from the cover). The FY2022 edition is headed 'UTB Partners"
    " Limited'; the FY2023, FY2024 and FY2025 editions are headed 'UTB Partners Plc' - the same holding"
    " company after a re-registration, not a different entity. Each edition prints ONE pair of columns"
    " (reporting date and prior-year comparative) and no second entity block, so there is no solo/consolidated"
    " pair to choose between here. Consistent with the rest of this workbook, every KM1 column is the"
    " CONSOLIDATED UTB PARTNERS basis and must not be read as standalone United Trust Bank Limited figures."
)

KM1_NOTE = (
    "WHAT IS AND IS NOT ON THIS SHEET.\n"
    "FY2022-FY2025 are each the bank's own published KM1 for that year. FY2021 is a comparative column"
    " (explained below). FY2020 is blank (explained below). Nothing on this sheet is computed: where the bank"
    " left a cell empty, it is empty here.\n\n"
    "FY2021 - A COMPARATIVE COLUMN, NOT THAT YEAR'S OWN DISCLOSURE. UTB Partners' FY2021 Pillar 3 edition"
    " contains no key-metrics template of any kind: its own contents page lists four appendices (Own Funds"
    " Disclosure Template, Leverage Ratio Template, Asset Encumbrance, and the countercyclical buffer"
    " requirement) and nothing else, the string 'KM1' does not appear in it, and the document contains no"
    " embedded image large enough to hide a table (checked, so the absence is a fact about the document rather"
    " than about text extraction). The template first appears in the FY2022 edition, which prints a full"
    " 31-Dec-21 comparative beside 31-Dec-22 - that comparative is what this column carries, and it is the"
    " same source the CET1/Tier 1/Total Capital/Total RWAs/Leverage/LCR sheets in this workbook already use"
    " for FY2021. It is flagged here because a comparative column is a weaker artefact than a reporting-year"
    " column: it can be, and in this bank's case demonstrably is, restated later.\n\n"
    "FY2020 - BLANK, AND FOR A STRONGER REASON. No KM1 exists for 31-Dec-20 on any basis. The only FY2020"
    " Pillar 3 document is United Trust Bank Limited's own SOLO-basis edition, which likewise publishes only"
    " the four appendix templates and no key-metrics table, and no later edition ever prints a 31-Dec-20"
    " column. So this is not a choice not to carry data; there is no data of this shape to carry. The FY2020"
    " figures shown on the individual metric sheets come from that solo edition's own funds and leverage"
    " templates and are on a different consolidation basis - reassembling them into a KM1 shape here would"
    " produce a row 4 and a row 14 the bank never published as key metrics.\n\n"
    "EDITIONS RESTATE, AND THIS BANK RESTATES A LOT. Every year above is taken from its own edition, so where"
    " a later edition disagrees, the later figure is deliberately NOT used. The differences are material and"
    " are recorded here so a reader comparing this sheet with the bank's latest PDF is not surprised:\n"
    "- 31-Dec-22: the FY2023 edition's comparative gives Tier 1 capital 223,209 (this sheet: 226,701), total"
    " capital 250,576 (257,803), Tier 1 ratio 12.84% (13.04%), total capital ratio 14.41% (14.83%), row 12"
    " 5.41% (5.83%), UK 16a 107,269 (76,739), row 16 27,694 (19,185), LCR 911.22% (1315.36%), row 18"
    " 2,516,383 (2,555,002) and NSFR 152.66% (155.01%).\n"
    "- 31-Dec-23: the FY2024 edition's comparative gives row 13 3,502,389 (this sheet: 3,502,424), row 18"
    " 3,060,242 (3,057,724) and NSFR 148.75% (148.63%).\n"
    "- 31-Dec-24: the FY2025 edition's comparative gives HQLA 292,329 (this sheet: 322,714), UK 16a 177,378"
    " (160,132), UK 16b 130,301 (131,347), row 16 59,696 (40,033), LCR 554.44% (806.12%), row 18 3,190,920"
    " (3,376,614) and NSFR 144.53% (142.63%).\n"
    "The liquidity differences are a change of BASIS, not arithmetic drift. FY2022's own column caps inflows"
    " at 75% of outflows in the CRR way (0.25 x 76,739 = 19,185), while the FY2023 edition's comparative for"
    " the same date nets them uncapped (107,269 - 79,575 = 27,694). And the FY2025 edition footnotes its LCR"
    " as a 12-point, 12-month average and its NSFR as a 4-point, 12-month average, where the FY2024 edition"
    " states no averaging basis at all. Reproduced as each edition printed it; not reconciled.\n\n"
    "ZERO, BLANK AND MISSING ARE THREE DIFFERENT THINGS HERE.\n"
    "- FY2021 row 9 (institution-specific countercyclical buffer) is a printed 0.00% and is kept as a zero.\n"
    "- FY2022's UK 7a and UK 7b, and the UK 8a / UK 9a / 10 / UK 10a rows in both the FY2022 and FY2023"
    " editions, are printed as rows with genuinely EMPTY cells - no dash, no zero, checked at the character"
    " level - and are left blank.\n"
    "- The FY2024 and FY2025 editions do not print the UK 8a / UK 9a / 10 / UK 10a rows at all, and say why:"
    " 'Where rows of the template are not shown, this is because they are blank and have been removed for"
    " clarity and to improve readability.' Those cells are blank here on the bank's own authority that the"
    " underlying values are nil-reportable, not because a row was missed.\n"
    "- The 'Additional leverage ratio disclosure requirements' heading is printed in all four editions with no"
    " rows beneath it. It is kept as a heading, because dropping it would silently change the template's"
    " shape.\n\n"
    "OTHER REPRODUCED-AS-PRINTED DETAILS. The bank's precision is its own and is not harmonised: UK 7a-7c are"
    " given to four decimal places in the FY2024 edition (0.6975%) and two in FY2025 (1.10%); row 14 is one"
    " decimal place while rows 5-7 are two. Row 13/14 carry the post-1-January-2022 caption 'excluding claims"
    " on central banks' in every edition on this sheet, so there is no leverage basis break within the KM1"
    " series - but there IS one against the FY2020 figure on the Leverage Ratio sheet, which predates the"
    " exclusion; see that sheet's own note."
)

bw.add_km1_sheet(
    title="United Trust Bank Limited — KM1 Key Metrics",
    subtitle="UTB Partners Plc consolidated basis. The bank's own UK KM1 key-metrics template, reproduced "
             "row for row from each year's own Pillar 3 edition, amounts in £'000 and ratios as printed. "
             "FY2021 is the FY2022 edition's comparative column; FY2020 is blank because no KM1 exists for "
             "that date on any basis. See the note and sources below.",
    rows=[
        ("SECTION", "Available own funds (amounts)", {}),
        ("DATA", "1  Common Equity Tier 1 (CET1) capital (£'000)", {
            "FY2025": 390450, "FY2024": 330662, "FY2023": 268495, "FY2022": 209850, "FY2021": 170785,
        }),
        ("DATA", "2  Tier 1 capital (£'000)", {
            "FY2025": 453206, "FY2024": 344803, "FY2023": 283710, "FY2022": 226701, "FY2021": 187636,
        }),
        ("DATA", "3  Total capital (£'000)", {
            "FY2025": 482806, "FY2024": 400094, "FY2023": 340213, "FY2022": 257803, "FY2021": 218186,
        }),
        ("SECTION", "Risk-weighted exposure amounts", {}),
        ("DATA", "4  Total risk-weighted exposure amount (£'000)", {
            "FY2025": 2785964, "FY2024": 2535096, "FY2023": 2277864, "FY2022": 1738779, "FY2021": 1340432,
        }),
        ("SECTION", "Capital ratios (as a percentage of risk-weighted exposure amount)", {}),
        ("DATA", "5  Common Equity Tier 1 ratio (%)", {
            "FY2025": "14.01%", "FY2024": "13.04%", "FY2023": "11.79%", "FY2022": "12.07%", "FY2021": "12.74%",
        }),
        ("DATA", "6  Tier 1 ratio (%)", {
            "FY2025": "16.27%", "FY2024": "13.60%", "FY2023": "12.46%", "FY2022": "13.04%", "FY2021": "14.00%",
        }),
        ("DATA", "7  Total capital ratio (%)", {
            "FY2025": "17.33%", "FY2024": "15.78%", "FY2023": "14.94%", "FY2022": "14.83%", "FY2021": "16.28%",
        }),
        ("SECTION", "Additional own funds requirements based on SREP (as a percentage of risk-weighted "
                    "exposure amount)", {}),
        ("DATA", "UK 7a  Additional CET1 SREP requirements (%)", {
            "FY2025": "1.10%", "FY2024": "0.6975%", "FY2023": "0.5625%",
        }),
        ("DATA", "UK 7b  Additional AT1 SREP requirements (%)", {
            "FY2025": "0.37%", "FY2024": "0.2325%", "FY2023": "0.1875%",
        }),
        ("DATA", "UK 7c  Additional T2 SREP requirements (%)", {
            "FY2025": "0.49%", "FY2024": "0.3100%", "FY2023": "0.25%", "FY2022": "1.00%", "FY2021": "1.34%",
        }),
        ("DATA", "UK 7d  Total SREP own funds requirements (%)", {
            "FY2025": "9.96%", "FY2024": "9.24%", "FY2023": "9.00%", "FY2022": "9.00%", "FY2021": "9.34%",
        }),
        ("SECTION", "Combined buffer requirement (as a percentage of risk-weighted exposure amount)", {}),
        ("DATA", "8  Capital conservation buffer (%)", {
            "FY2025": "2.50%", "FY2024": "2.50%", "FY2023": "2.50%", "FY2022": "2.50%", "FY2021": "2.50%",
        }),
        ("DATA", "UK 8a  Conservation buffer due to macro-prudential or systemic risk identified at the "
                 "level of a Member State (%)", {}),
        ("DATA", "9  Institution specific countercyclical capital buffer (%)", {
            "FY2025": "2.00%", "FY2024": "2.00%", "FY2023": "2.00%", "FY2022": "1.00%", "FY2021": "0.00%",
        }),
        ("DATA", "UK 9a  Systemic risk buffer (%)", {}),
        ("DATA", "10  Global Systemically Important Institution buffer (%)", {}),
        ("DATA", "UK 10a  Other Systemically Important Institution buffer", {}),
        ("DATA", "11  Combined buffer requirement (%)", {
            "FY2025": "4.50%", "FY2024": "4.50%", "FY2023": "4.50%", "FY2022": "3.50%", "FY2021": "2.50%",
        }),
        ("DATA", "UK 11a  Overall capital requirements (%)", {
            "FY2025": "14.46%", "FY2024": "13.74%", "FY2023": "13.50%", "FY2022": "12.50%", "FY2021": "11.84%",
        }),
        ("DATA", "12  CET1 available after meeting the total SREP own funds requirements (%)", {
            "FY2025": "7.52%", "FY2024": "6.68%", "FY2023": "5.71%", "FY2022": "5.83%", "FY2021": "6.94%",
        }),
        ("SECTION", "Leverage ratio", {}),
        ("DATA", "13  Total exposure measure excluding claims on central banks (£'000)", {
            "FY2025": 4500670, "FY2024": 3979115, "FY2023": 3502424, "FY2022": 2878801, "FY2021": 2318303,
        }),
        ("DATA", "14  Leverage ratio excluding claims on central banks (%)", {
            "FY2025": "10.1%", "FY2024": "8.7%", "FY2023": "8.1%", "FY2022": "7.9%", "FY2021": "8.1%",
        }),
        ("SECTION", "Additional leverage ratio disclosure requirements (heading printed with no rows in "
                    "every edition)", {}),
        ("SECTION", "Liquidity Coverage Ratio", {}),
        ("DATA", "15  Total high-quality liquid assets (HQLA) (weighted value - average) (£'000)", {
            "FY2025": 384058, "FY2024": 322714, "FY2023": 257050, "FY2022": 252352, "FY2021": 194544,
        }),
        ("DATA", "UK 16a  Cash outflows - Total weighted value (£'000)", {
            "FY2025": 236537, "FY2024": 160132, "FY2023": 129034, "FY2022": 76739, "FY2021": 76791,
        }),
        ("DATA", "UK 16b  Cash inflows - Total weighted value (£'000)", {
            "FY2025": 126370, "FY2024": 131347, "FY2023": 113624, "FY2022": 79575, "FY2021": 67489,
        }),
        ("DATA", "16  Total net cash outflows (adjusted value) (£'000)", {
            "FY2025": 113223, "FY2024": 40033, "FY2023": 32258, "FY2022": 19185, "FY2021": 19198,
        }),
        ("DATA", "17  Liquidity coverage ratio (%)", {
            "FY2025": "398.42%", "FY2024": "806.12%", "FY2023": "796.86%", "FY2022": "1315.36%",
            "FY2021": "1013.36%",
        }),
        ("SECTION", "Net Stable Funding Ratio", {}),
        ("DATA", "18  Total available stable funding (£'000)", {
            "FY2025": 3590720, "FY2024": 3376614, "FY2023": 3057724, "FY2022": 2555002,
        }),
        ("DATA", "19  Total required stable funding (£'000)", {
            "FY2025": 2570256, "FY2024": 2367394, "FY2023": 2057282, "FY2022": 1648317,
        }),
        ("DATA", "20  NSFR ratio (%)", {
            "FY2025": "139.71%", "FY2024": "142.63%", "FY2023": "148.63%", "FY2022": "155.01%",
        }),
    ],
    sources_text=KM1_NOTE + "\n\n" + KM1_SOURCES,
    first_col_width=72,
    source_height=460,
)


def metric(name, unit, rows_data, note=None):
    bw.add_metric_sheet(
        name, unit, rows_data, sources(), note=note, first_col_width=54, source_height=235
    )


metric("CET1 Capital", "£'000", [("Common Equity Tier 1 (CET1) capital", {
    "FY2025": 390450, "FY2024": 330662, "FY2023": 268495,
    "FY2022": 209850, "FY2021": 170785, "FY2020": 148091,
})])
metric("CET1 Ratio", "% of RWA", [("Common Equity Tier 1 (CET1) ratio", {
    "FY2025": "14.01%", "FY2024": "13.04%", "FY2023": "11.79%",
    "FY2022": "12.07%", "FY2021": "12.74%", "FY2020": "11.44%",
})])
metric("Tier 1 Capital", "£'000", [("Tier 1 capital", {
    "FY2025": 453206, "FY2024": 344803, "FY2023": 283710,
    "FY2022": 226701, "FY2021": 187636, "FY2020": 164942,
})])
metric("Tier 1 Ratio", "% of RWA", [("Tier 1 ratio", {
    "FY2025": "16.27%", "FY2024": "13.60%", "FY2023": "12.46%",
    "FY2022": "13.04%", "FY2021": "14.00%", "FY2020": "12.74%",
})])
metric("Total Capital", "£'000", [("Total capital", {
    "FY2025": 482806, "FY2024": 400094, "FY2023": 340213,
    "FY2022": 257803, "FY2021": 218186, "FY2020": 199420,
})])
metric("Total Capital Ratio", "% of RWA", [("Total capital ratio", {
    "FY2025": "17.33%", "FY2024": "15.78%", "FY2023": "14.94%",
    "FY2022": "14.83%", "FY2021": "16.28%", "FY2020": "15.40%",
})])
metric("Total RWAs", "£'000", [("Total risk-weighted exposure amount", {
    "FY2025": 2785964, "FY2024": 2535096, "FY2023": 2277864,
    "FY2022": 1738779, "FY2021": 1340432, "FY2020": 1294667,
})], note=(
    "Each year's own published figure is preserved. The 2024 report's OV1 table shows 2,535,339 for 2024 "
    "versus the KM1 figure 2,535,096; the KM1 value is used for consistency with the capital ratios."
))

bw.add_rwa_breakdown_sheet(
    title="United Trust Bank Limited — RWA Breakdown",
    subtitle="FY2025-FY2021: Consolidated UTB Partners Plc basis, Table UK OV1 - Overview of risk-weighted "
             "exposure amounts, £'000. FY2020: United Trust Bank Limited SOLO basis, derived from disclosed "
             "Pillar 1 capital requirement x 12.5 - see the second SECTION block below and the sources note.",
    rows=[
        ("SECTION", "UK OV1 — Overview of risk weighted exposure amounts (CONSOLIDATED)", {}),
        ("DATA", "Credit risk (excluding CCR)", {
            "FY2025": 2654604, "FY2024": 2420072, "FY2023": 2198914, "FY2022": 1702127, "FY2021": 1261719,
        }),
        ("DATA", "Counterparty credit risk (CCR), of which credit valuation adjustment (CVA)", {
            "FY2025": 2328, "FY2024": 1429, "FY2023": 1646, "FY2022": 1604, "FY2021": 0,
        }),
        ("DATA", "Securitisation exposures in the non-trading book (after the cap)", {
            "FY2025": -146838, "FY2024": -157263, "FY2023": -150150, "FY2022": -145475, "FY2021": -70700,
        }),
        ("DATA", "Operational risk", {
            "FY2025": 275870, "FY2024": 271100, "FY2023": 227455, "FY2022": 180522, "FY2021": 149412,
        }),
        ("TOTAL", "Total risk-weighted exposure amount (Table UK OV1)", {
            "FY2025": 2785964, "FY2024": 2535339, "FY2023": 2277865, "FY2022": 1738778, "FY2021": 1340342,
        }),
        # Own SECTION block, not folded into the OV1 block above: FY2020's own
        # Pillar 3 disclosure predates the OV1 template and is on a different
        # basis entirely (United Trust Bank Limited SOLO, not consolidated
        # UTB Partners Plc). It publishes a Pillar 1 capital requirement table
        # (section 5.2, p.28) that DOES split by risk type (credit / operational;
        # market risk is a genuine disclosed nil - "the Bank does not have a
        # trading book") - each figure below is that table's own capital-
        # requirement figure x 12.5 (= / 8%), the standard Basel/CRR identity,
        # not an estimate. Total ties to within £5k of the Total RWAs sheet's
        # own FY2020 figure (1,294,667).
        ("SECTION", "Pillar 1 capital requirement × 12.5 (SOLO, derived from disclosed capital requirement)", {}),
        ("DATA", "Credit risk", {"FY2020": 93316 * 12.5}),
        ("DATA", "Market risk (nil — Bank has no trading book)", {"FY2020": 0}),
        ("DATA", "Operational risk", {"FY2020": 10257 * 12.5}),
        ("TOTAL", "Total risk-weighted exposure amount (derived)", {"FY2020": 103573 * 12.5}),
    ],
    sources_text=rwa_sources(),
    first_col_width=68,
    source_height=260,
)

metric("Leverage Ratio", "£'000 / %", [
    ("Total exposure measure excluding claims on central banks", {
        "FY2025": 4500670, "FY2024": 3979115, "FY2023": 3502424,
        "FY2022": 2878801, "FY2021": 2318303, "FY2020": 1917202,
    }),
    ("Leverage ratio excluding claims on central banks", {
        "FY2025": "10.1%", "FY2024": "8.7%", "FY2023": "8.1%",
        "FY2022": "7.9%", "FY2021": "8.1%", "FY2020": "8.6%",
    }),
], note=(
    "FY2020 BASIS DIFFERS: the PRA/CRR2 discretion to temporarily exclude central bank claims from the "
    "leverage exposure measure only took effect from June 2021, so the FY2020 disclosure's own Leverage Ratio "
    "Template (Appendix 2, Table LRCom) reports a single non-exclusion-adjusted exposure measure (£1,917,202k) "
    "and ratio (8.6%) - not a like-for-like figure with the FY2021-FY2025 ex-central-bank series, but each "
    "year's own genuinely reported number is preserved here rather than adjusted or omitted."
))
metric("LCR", "£'000 / %", [
    ("Total high-quality liquid assets (HQLA), weighted value - average", {
        "FY2025": 384058, "FY2024": 322714, "FY2023": 257050,
        "FY2022": 252352, "FY2021": 194544,
    }),
    ("Total net cash outflows, adjusted value", {
        "FY2025": 113223, "FY2024": 40033, "FY2023": 32258,
        "FY2022": 19185, "FY2021": 19198,
    }),
    ("Liquidity coverage ratio", {
        "FY2025": "398.42%", "FY2024": "806.12%", "FY2023": "796.86%",
        "FY2022": "1315.36%", "FY2021": "1013.36%",
    }),
], note=(
    "CORRECTION 2026-09-16 (KM1-030): this note previously said 'The FY2021 disclosure does not provide a KM1 "
    "LCR table; only the headline ratio is available in the FY2022 comparative column', and the FY2021 HQLA "
    "and net-outflow cells were left blank on that basis. The first half is right - the FY2021 edition has no "
    "key-metrics table at all - but the second half was wrong. The FY2022 edition's 31-Dec-21 COMPARATIVE "
    "column prints the full LCR block, not just the ratio: KM1 row 15 HQLA 194,544, UK 16a cash outflows "
    "76,791, UK 16b cash inflows 67,489 and row 16 total net cash outflows 19,198. Those components are now "
    "carried here, and they tie: 19,198 is 25% of 76,791, i.e. the CRR cap on inflows binding, which is also "
    "consistent with 194,544 / 19,198 = 1013.4% against the printed 1013.36%. "
    "THE FY2022 AND FY2023 EDITIONS DISAGREE MATERIALLY ABOUT 31-DEC-22, and the difference is a change of "
    "basis rather than a correction: FY2022's own column caps inflows (outflows 76,739, net 19,185 = 25% of "
    "outflows) while the FY2023 edition's comparative for the same date nets them uncapped (outflows 107,269 "
    "less inflows 79,575 = 27,694), giving 911.22% against the originally-published 1315.36%. This series "
    "preserves each year's own as-reported value; see the KM1 Key Metrics sheet for the full list of "
    "restatements. FY2020 GENUINE WHOLE-YEAR SELF-SKIP: United Trust "
    "Bank Limited's own solo-basis FY2020 Pillar 3 disclosure (the only FY2020 Pillar 3 document that exists - "
    "see the CET1/Tier 1/Total Capital sheets' shared note) contains no LCR section of any kind - its own "
    "contents page lists Capital resources, Capital adequacy, Credit risk exposures, Securitisation, "
    "Remuneration and the Own Funds/Leverage Ratio/Asset Encumbrance/CCyB appendices only, with no liquidity "
    "disclosure - so no LCR figure exists to transcribe for FY2020, not merely one that wasn't located."
))
metric("NSFR", "£'000 / %", [
    ("Total available stable funding", {
        "FY2025": 3590720, "FY2024": 3376614, "FY2023": 3057724,
        "FY2022": 2555002,
    }),
    ("Total required stable funding", {
        "FY2025": 2570256, "FY2024": 2367394, "FY2023": 2057282,
        "FY2022": 1648317,
    }),
    ("NSFR ratio", {
        "FY2025": "139.71%", "FY2024": "142.63%", "FY2023": "148.63%",
        "FY2022": "155.01%",
    }),
], note=(
    "FY2021 is blank, re-verified 2026-09-16 (KM1-030) rather than left on the earlier search: the FY2021 "
    "edition contains no key-metrics table at all, and the FY2022 edition's KM1, which does print a full "
    "31-Dec-21 comparative for every other block, prints rows 18/19/20 for 31-Dec-22 ONLY and leaves the "
    "31-Dec-21 cells empty. So the absence is the bank's own, not a document we failed to read - unlike the "
    "FY2021 LCR components, which that same comparative column does print and which have now been recovered "
    "onto the LCR sheet. FY2020 GENUINE WHOLE-YEAR SELF-SKIP: as with LCR, no NSFR of any kind is disclosed in United Trust "
    "Bank Limited's own solo-basis FY2020 Pillar 3 disclosure - confirmed absent from its own contents page, "
    "not merely a document gap."
))
metric("MREL Ratio", "£'000 / %", [("MREL ratio", {y: "Not publicly disclosed" for y in YEARS})], note=(
    "No MREL ratio or numeric MREL requirement was located in the five UTB Partners Pillar 3 reports reviewed."
))

bw.add_overview_sheet(
    cash_flow_totals=[],
    cash_flow_unit=None,
    balance_sheet_totals=[
        ("Total assets", {"FY2025": 4450637, "FY2024": 3913260, "FY2023": 3440168, "FY2022": 2798317, "FY2021": 2254178, "FY2020": 1867932}),
        ("Loans and advances to customers", {"FY2025": 3895213, "FY2024": 3487345, "FY2023": 3104356, "FY2022": 2426021, "FY2021": 1808607, "FY2020": 1646322}),
        ("Deposits from customers", {"FY2025": 3847845, "FY2024": 3407271, "FY2023": 2797361, "FY2022": 2208300, "FY2021": 1715596, "FY2020": 1601361}),
        ("Total capital and reserves", {"FY2025": 472836, "FY2024": 362862, "FY2023": 299799, "FY2022": 239109, "FY2021": 195632, "FY2020": 174036}),
    ],
    balance_sheet_unit="£'000",
    income_statement_totals=[
        ("Operating income", {"FY2025": 176431, "FY2024": 164971, "FY2023": 154146, "FY2022": 114642, "FY2021": 95140, "FY2020": 79054}),
        ("Profit on ordinary activities before tax", {"FY2025": 78686, "FY2024": 86369, "FY2023": 82739, "FY2022": 60156, "FY2021": 44437, "FY2020": 30659}),
        ("Profit after tax retained for the financial year", {"FY2025": 60680, "FY2024": 65772, "FY2023": 63274, "FY2022": 45395, "FY2021": 35422, "FY2020": 24910}),
    ],
    income_statement_unit="£'000",
    equity_changes_totals=[
        ("Opening equity", {"FY2025": 362862, "FY2024": 299799, "FY2023": 239109, "FY2022": 195632, "FY2021": 174036, "FY2020": 150974}),
        ("Total comprehensive income for the year", {"FY2025": 60680, "FY2024": 65772, "FY2023": 63274, "FY2022": 45395, "FY2021": 35422, "FY2020": 24910}),
        ("Other equity movements, net", {"FY2025": 49294, "FY2024": -2709, "FY2023": -2584, "FY2022": -1918, "FY2021": -13826, "FY2020": -1848}),
        ("Closing equity", {"FY2025": 472836, "FY2024": 362862, "FY2023": 299799, "FY2022": 239109, "FY2021": 195632, "FY2020": 174036}),
    ],
    equity_changes_unit="£'000",
    ratios=[
        ("CET1 Ratio", {"FY2025": "14.01%", "FY2024": "13.04%", "FY2023": "11.79%", "FY2022": "12.07%", "FY2021": "12.74%", "FY2020": "11.44%"}),
        ("Tier 1 Ratio", {"FY2025": "16.27%", "FY2024": "13.60%", "FY2023": "12.46%", "FY2022": "13.04%", "FY2021": "14.00%", "FY2020": "12.74%"}),
        ("Total Capital Ratio", {"FY2025": "17.33%", "FY2024": "15.78%", "FY2023": "14.94%", "FY2022": "14.83%", "FY2021": "16.28%", "FY2020": "15.40%"}),
        ("Leverage Ratio", {"FY2025": "10.1%", "FY2024": "8.7%", "FY2023": "8.1%", "FY2022": "7.9%", "FY2021": "8.1%", "FY2020": "8.6%"}),
        ("LCR", {"FY2025": "398.42%", "FY2024": "806.12%", "FY2023": "796.86%", "FY2022": "1315.36%", "FY2021": "1013.36%"}),
        ("NSFR", {"FY2025": "139.71%", "FY2024": "142.63%", "FY2023": "148.63%", "FY2022": "155.01%"}),
    ],
    note=(
        "Statutory cash-flow data is not available in the entity accounts (see the Cash Flow Statement "
        "sheet); the Balance Sheet, Profit & Loss, Statement of Changes in Equity and Asset Quality sheets "
        "are entity (Company-only) basis, while the ratio/RWA and other Pillar 3 metrics are consolidated "
        "UTB Partners basis for FY2021-FY2025 but solo UTB Limited basis for FY2020 (see the Pillar 3 sheets' "
        "shared FY2020 basis note) - see each sheet's own source note. FY2021 LCR is headline-only and FY2021 "
        "NSFR is unavailable; FY2020 has no LCR or NSFR disclosure of any kind in its own source document; "
        "MREL is not publicly disclosed in any year; FY2020's Leverage Ratio also predates the central-bank-"
        "claims exemption used from FY2021 onward (see that sheet's own note)."
    ),
)

bw.save("/Users/armaan/code/katalysis/banks/UNITED TRUST BANK FINANCIALS.xlsx")
