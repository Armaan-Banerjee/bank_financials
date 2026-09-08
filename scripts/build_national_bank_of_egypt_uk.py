import os
import sys
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021", "FY2017"]

AR = {
    "FY2017": "https://www.nbeuk.com/wp-content/uploads/2021/02/NBE_UK_Financial_Statements_2018.pdf",
    "FY2025": "https://find-and-update.company-information.service.gov.uk/company/02743734/filing-history/MzU0MDExNTA0NGFkaXF6a2N4/document?format=pdf&download=0",
    "FY2024": "https://find-and-update.company-information.service.gov.uk/company/02743734/filing-history/MzQ2Mjk2OTExMGFkaXF6a2N4/document?format=pdf&download=0",
    "FY2023": "https://find-and-update.company-information.service.gov.uk/company/02743734/filing-history/MzQxOTgxMTA0NmFkaXF6a2N4/document?format=pdf&download=0",
    "FY2022": "https://find-and-update.company-information.service.gov.uk/company/02743734/filing-history/MzM5NDYwNDY2OGFkaXF6a2N4/document?format=pdf&download=0",
    "FY2021": "https://find-and-update.company-information.service.gov.uk/company/02743734/filing-history/MzM1MTQyMDQxMmFkaXF6a2N4/document?format=pdf&download=0",
}
P3 = {
    "FY2024": "https://www.nbeuk.com/wp-content/uploads/2025/04/Pillar-3-Disclosures-31st-December-2024.pdf",
    "FY2023": "https://www.nbeuk.com/wp-content/uploads/2024/09/Pillar-3-Disclosures-31st-December-2023-FINAL.pdf",
    "FY2022": "https://www.nbeuk.com/wp-content/uploads/2023/10/NBE-UK-Pillar-3-31-December-2022-approved.pdf",
    "FY2021": "https://www.nbeuk.com/wp-content/uploads/2023/05/Pillar-3-31-December-2021-approved.pdf",
}

ENTITY = (
    "ENTITY NOTE: National Bank of Egypt (UK) Limited (Companies House 02743734, FRN 204520, LEI "
    "2TV5CTDU7ZDMT8HL5F58) matches Banks List 2608.xlsx and Companies House. It is a UK-incorporated, "
    "wholly owned subsidiary of National Bank of Egypt. The accounts contain a full entity-level cash-flow "
    "statement. The annual reports and Pillar 3 documents are image-only or mixed scans for the older years; "
    "figures were OCR'd and checked against the following year's comparative columns where available. "
    "Pillar 3 is annual: no defensible entity-level interim disclosure was located, so this is a 13-sheet workbook."
)

P3_2025_URL = None  # no 2025 Pillar 3 document located on nbeuk.com as of this build (confirmed 404, no listing hit)

STATEMENTS_SOURCES = (
    "Sources - National Bank of Egypt (UK) Limited's own Profit and loss account / Balance sheet / Statement of changes "
    "in equity, entity-level basis, £ (Companies House filings, all fully scanned/image-only):\n"
    f"FY2025 & FY2024: Annual Report 2025, p.38 (Profit and loss account), p.39 (Balance sheet), p.40 (Statement of "
    "changes in equity) - " + AR["FY2025"] + "\n"
    f"FY2024 (own): Annual Report 2024 - " + AR["FY2024"] + "\n"
    f"FY2023 & FY2022: Annual Report 2023, p.36 (Profit and loss account), p.37 (Balance sheet), p.38 (Statement of "
    "changes in equity) - " + AR["FY2023"] + "\n"
    f"FY2022 (own): Annual Report 2022, p.35 (Profit and loss account), p.36 (Balance sheet), p.37 (Statement of "
    "changes in equity), p.37 (Cash flow) - " + AR["FY2022"] + "\n"
    f"FY2021 (own, 18-month period 1 July 2020 to 31 December 2021, following an accounting-reference-date change): "
    "Annual Report 2022 (restated comparative column), p.33 (Profit and loss account), p.34 (Balance sheet) - "
    + AR["FY2022"] + "\n"
    + ENTITY + "\n\n"
    "PRESENTATION NOTES: (1) FY2021 covers an 18-month period (1 July 2020 to 31 December 2021), not a 12-month year - "
    "the entity's own accounting reference date changed from 30 June to 31 December during this period, and this is "
    "reported here exactly as originally presented in the Bank's own audited accounts, not annualised or restated. "
    "(2) FY2025/FY2024's 'Fees and commission' line is net of Trade Finance expense per the Bank's own Note 4; "
    "FY2023/FY2022/FY2021's equivalent line is presented gross in the primary statement (the net figure is not shown "
    "as a single line for those years) - each year's own primary-statement figure is used, not recalculated onto a "
    "common basis. (3) FY2021's 'Administrative expenses' combines Staff costs with a small (£93,724) 'Other "
    "administrative expenses' balance that FY2022 onward reports separately as part of Other operating charges - a "
    "genuine source-document composition difference, not a transcription error. (4) FY2021's 'Net impairment reversal' "
    "(+£443,787, an income addback) reflects the release of a specific bad-debt provision that had stood at £951,955 "
    "since 30 June 2019 and was fully released/written off during the 18-month period to 31 December 2021 - the Bank "
    "has carried a nil provision balance in every year since (see the Asset Quality sheet). (5) FY2022/FY2021's "
    "Balance Sheet has no separate 'Intangible fixed assets' line (nil/immaterial, folded into Tangible fixed assets); "
    "FY2023 onward shows it separately. (6) The equity reconciliation ladder was confirmed exactly across all 5 years: "
    "every year's own closing balance ties to both the next year's opening balance and that year's own Balance Sheet "
    "Total capital and reserves - zero plug rows needed anywhere. This entity has no share premium, no revaluation "
    "reserve, no dividends, and no share issuances in any of the 5 years reviewed - Called up share capital has stayed "
    "at £130,000,000 throughout, and every equity movement is simply that year's own Total comprehensive income."
)

BALANCE_SHEET_SOURCES = (
    STATEMENTS_SOURCES + "\n\n"
    "DEBT SECURITIES BREAKDOWN: the 'Debt securities - ...' sub-rows below the headline 'Total debt securities' "
    "line are transcribed from the Bank's own Note 12/Note 10 'Debt securities' of each year's own Notes to the "
    "Financial Statements, which splits the balance both by issuer type (issued by public bodies - government "
    "securities - vs other securities) and by an interest rate fair value adjustment relating to hedge accounting "
    "(see below):\n"
    "FY2025 & FY2024: Note 12, p.54 - " + AR["FY2025"] + "\n"
    "FY2023 & FY2022: Note 10, p.52 - " + AR["FY2023"] + "\n"
    "FY2021 (own, 18-month period to 31 December 2021): Note 10, p.48 - " + AR["FY2021"] + "\n\n"
    "Each year's 3 sub-rows (Issued by public bodies / Other securities / Interest rate fair value adjustment) sum "
    "exactly to that year's headline 'Total debt securities' line - verified directly against the note. "
    "MEASUREMENT BASIS: the Bank's own Note 17/Note 15 'Financial instruments' (same filings, adjoining pages) "
    "classifies the ENTIRE debt securities book - both the portion 'packaged in asset swaps' and the portion "
    "held outright - as 'Financial assets at amortised cost'; no FVOCI/FVTPL/available-for-sale/trading leg is "
    "disclosed in any year reviewed. The 'packaged in asset swaps' portion (FY2025 £215,335,237; FY2024 "
    "£241,498,548; FY2023 £206,526,248; FY2022 £229,494,910; FY2021 £206,590,056) is the hedged item in an "
    "effective fair-value interest-rate-hedging relationship and carries a hedge-accounting basis adjustment "
    "(the 'Interest rate fair value adjustment' sub-row above, refer to Note 18/Note 16/Note 15 per year) added "
    "to its amortised-cost carrying value - this is a hedge-accounting mechanism, not a change of measurement "
    "category, so all 3 sub-rows above are labelled '(amortised cost)' rather than introducing a fabricated "
    "mark-to-market leg. Not added as separate rows here (would double the reconciling total against the issuer-"
    "type split above), but confirmed identically for all 5 years via each year's own Note 12/Note 10 first table "
    "('Debt securities packaged in asset swaps' + 'Debt securities at amortised cost' = same headline total)."
)

ASSET_QUALITY_SOURCES = (
    "Sources - National Bank of Egypt (UK) Limited's own loans-and-advances-to-customers concentration note and "
    "bad-and-doubtful-debt provision note, entity-level basis, £ (Companies House filings, all fully scanned/"
    "image-only):\n"
    f"FY2025 & FY2024: Annual Report 2025, p.51-52 (Note 8 Provisions for bad and doubtful debts; Note 11 Loans and "
    "advances to customers) - " + AR["FY2025"] + "\n"
    f"FY2023 & FY2022: Annual Report 2023, p.47, p.51 (Note 6; Note 9) - " + AR["FY2023"] + "\n"
    f"FY2021 (own, 18-month period): Annual Report 2022, p.42-43 (Note 6 Provisions for bad and doubtful debts, "
    "including the full movement table and non-performing-loan status) - " + AR["FY2022"] + "\n"
    + ENTITY + "\n\n"
    "This is an FRS 102 entity - no IFRS 9 stage 1/2/3 split is disclosed in any year; a specific bad-and-doubtful-"
    "debt provision is used instead. The Bank's own Note 8/Note 6 explicitly discloses a nil net impairment "
    "charge/reversal (shown as '-') for FY2022 through FY2025, and a nil provision balance against loans and "
    "advances to customers at every one of these 5 year-ends - confirmed via the loans-and-advances-to-customers "
    "note's own 'Bad and doubtful debt provision - specific' line, not inferred. FY2021's provision was fully "
    "released/written off during the 18-month period (see the Profit & Loss sheet's presentation notes) from an "
    "opening balance of £951,955 at 30 June 2020; the Bank's own Note 6(c) also confirms nil non-performing loans "
    "(net of suspended interest) at 31 December 2021, down from £949,661 at 30 June 2020 - a genuine full resolution "
    "of the prior non-performing book within the period, not a data gap. A non-performing-loan sub-analysis "
    "equivalent to FY2021's own Note 6(c) was not located in the FY2022-FY2025 filings reviewed this session - left "
    "blank rather than assumed nil. Geographic concentration for FY2021 was not sourced this session - left blank."
)

RWA_BREAKDOWN_SOURCES = (
    "Sources - National Bank of Egypt (UK) Limited's own Pillar 3 disclosures, entity-level basis, £000:\n"
    "FY2024 (own, Template UK OV1): Pillar 3 Disclosures 31 December 2024, Section 5 - " + P3["FY2024"] + "\n"
    "FY2023 (own, Template UK OV1): Pillar 3 Disclosures 31 December 2023, Section 5 - " + P3["FY2023"] + "\n"
    "FY2022 (own, Pillar 1 capital-requirement-by-asset-class table): Pillar 3 disclosure 31 December 2022, Section "
    "9/10 - " + P3["FY2022"] + "\n"
    "FY2021 (own, Pillar 1 capital-requirement-by-asset-class table AND a separately-disclosed 'Risk Weighted Assets' "
    "figure): Pillar 3 disclosure 31 December 2021, Section 3/4 - " + P3["FY2021"] + "\n"
    "FY2025: no 2025 Pillar 3 disclosure located as of this build (confirmed 404 on the expected URL pattern and no "
    "listing-page hit); values left blank rather than estimated.\n\n"
    + ENTITY + "\n\n"
    "GENUINE CROSS-DOCUMENT DISCREPANCY (flagged, not silently reconciled): this bank's own Pillar 3 documents do not "
    "give one single consistent 'Total RWA' figure per year. FY2024's OV1-template total (£1,047,061k) matches the "
    "Total RWAs sheet exactly. FY2023's OV1-template total (£1,040,542k, this table) does NOT match FY2023's own KM1 "
    "summary table in the SAME document (£962,119k, used on the Total RWAs sheet) - a genuine within-document "
    "inconsistency, not a transcription error. FY2022/FY2021 have no OV1 template at all; the categories below are "
    "derived from each year's own Pillar 1 capital-requirement-by-asset-class table (multiplied by 12.5, the standard "
    "8%-to-RWA conversion), giving derived totals of £951,513k (FY2022) and £813,226k (FY2021) that do NOT match "
    "either year's own separately and explicitly disclosed 'Risk Weighted Assets' figure (£906,134k / £779,381k, used "
    "on the Total RWas sheet) - again a genuine document-internal gap (the capital-requirement components evidently "
    "don't sum linearly to the disclosed RWA total via the standard 12.5x scalar), not an error introduced here. Each "
    "year's own best-available category split is shown as-is."
)


def sources(kind):
    if kind == "cash":
        return ("Sources - National Bank of Egypt (UK) Limited entity-level Cash Flow Statement, £:\n" +
                "\n".join(f"{y}: Companies House Annual Report for {y[2:]}, Cash Flow Statement - {AR[y]}" for y in YEARS) +
                "\n\nFY2021/FY2022 are condensed cash-flow presentations in the filed accounts; the reported subtotals and opening/closing cash chain are preserved.\n\n"
                "CORRECTION (2026-08-29 correctness sweep): the original transcription omitted a real, separately-disclosed "
                "'Effect of foreign exchange rate changes' line that sits between the opening and closing cash balances in the "
                "FY2023, FY2024, and FY2025 filings' own Cash Flow Statements (FY2025 Annual Report p.41; FY2023 Annual Report p.39, "
                "restated FY2022 comparative). Without it, the opening + net change chain did not tie to the printed closing balance "
                "for those 3 years (confirmed by re-reading each source page directly): FY2023 -18,919,972; FY2024 +3,491,832; FY2025 "
                "-15,465,348. Added as its own line; the chain now reconciles exactly for FY2023-FY2025. FY2021/FY2022 needed no change "
                "- their condensed presentation already embeds this effect within operating activities, and the chain already tied.\n\n"
                + ENTITY)
    return ("Sources - National Bank of Egypt (UK) Limited entity-level Pillar 3 / regulatory capital disclosures, £000 unless stated:\n" +
            "\n".join(f"{y}: annual Pillar 3 disclosure, UK KM1 / capital adequacy table - {P3[y]}" for y in ["FY2021", "FY2022", "FY2023", "FY2024"]) +
            "\nFY2025: no 2025 Pillar 3 disclosure located as of this build; values left blank rather than estimated.\n\n" + ENTITY)

bw = BankWorkbook("National Bank of Egypt (UK) Limited", YEARS, header_color="7B2D26")

# ---------------------------------------------------------------
# Sheet 1: Balance Sheet - built first per the equity reconciliation
# ladder so each year's own Total capital and reserves is an
# independent check value. Zero plug rows across all 5 years.
# ---------------------------------------------------------------
bs_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and balances at central banks", {"FY2025": 371451, "FY2024": 397639, "FY2023": 398999, "FY2022": 402993, "FY2021": 302328}),
    ("DATA", "Loans and advances to banks", {"FY2025": 651571869, "FY2024": 654586394, "FY2023": 726791733, "FY2022": 709298405, "FY2021": 577213067}),
    ("DATA", "Loans and advances to customers", {"FY2025": 487762621, "FY2024": 181521123, "FY2023": 61860769, "FY2022": 46503635, "FY2021": 37151779}),
    ("DATA", "Total debt securities", {"FY2025": 604021714, "FY2024": 488086660, "FY2023": 505332212, "FY2022": 508564166, "FY2021": 550750341}),
    ("DATA", "Debt securities - Issued by public bodies (government securities, amortised cost)", {"FY2025": 246733992, "FY2024": 181040174, "FY2023": 192504359, "FY2022": 180661405, "FY2021": 189275634}),
    ("DATA", "Debt securities - Other securities (amortised cost)", {"FY2025": 356026463, "FY2024": 311841237, "FY2023": 320191387, "FY2022": 343276052, "FY2021": 356876457}),
    ("DATA", "Debt securities - Interest rate fair value adjustment (hedge-accounting basis adjustment on securities packaged in interest rate asset swaps, amortised cost)", {"FY2025": 1261259, "FY2024": -4794751, "FY2023": -7363534, "FY2022": -15373291, "FY2021": 4598250}),
    ("DATA", "Derivative financial instruments", {"FY2025": 4323287, "FY2024": 8754822, "FY2023": 11054880, "FY2022": 16652823, "FY2021": 378832}),
    ("DATA", "Tangible fixed assets", {"FY2025": 41411528, "FY2024": 42218048, "FY2023": 42910866, "FY2022": 42356164, "FY2021": 41363058}),
    ("DATA", "Intangible fixed assets (no separate line FY2021-FY2022 - nil/immaterial)", {"FY2025": 4126398, "FY2024": 1896837, "FY2023": 580386}),
    ("DATA", "Prepayments and accrued income", {"FY2025": 1622582, "FY2024": 1263240, "FY2023": 1410882, "FY2022": 1989589, "FY2021": 5356899}),
    ("DATA", "Current tax assets", {"FY2023": 736026, "FY2022": 188232, "FY2021": 116855}),
    ("DATA", "Deferred tax assets", {"FY2021": 81576}),
    ("DATA", "Other assets", {"FY2025": 295821, "FY2024": 229528, "FY2023": 21241, "FY2022": 91313, "FY2021": 38172}),
    ("TOTAL", "Total assets", {"FY2025": 1795507271, "FY2024": 1378954291, "FY2023": 1351097994, "FY2022": 1326047320, "FY2021": 1212752908}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Deposits by banks", {"FY2025": 162146460, "FY2024": 137050906, "FY2023": 193404628, "FY2022": 519965127, "FY2021": 756896286}),
    ("DATA", "Customer accounts", {"FY2025": 1388254579, "FY2024": 1032921877, "FY2023": 956051029, "FY2022": 608680668, "FY2021": 248279581}),
    ("DATA", "Derivative financial instruments", {"FY2025": 5157961, "FY2024": 1044103, "FY2023": 577008, "FY2022": 205870, "FY2021": 6763860}),
    ("DATA", "Other liabilities", {"FY2025": 1326258, "FY2024": 741899, "FY2023": 648940, "FY2022": 1054200, "FY2021": 10900143}),
    ("DATA", "Current tax liabilities", {"FY2025": 251723, "FY2024": 446704}),
    ("DATA", "Deferred tax liabilities", {"FY2025": 501721, "FY2024": 685514, "FY2023": 639935, "FY2022": 187556, "FY2021": 215467}),
    ("DATA", "Accruals and deferred income", {"FY2025": 1742619, "FY2024": 1816045, "FY2023": 1871759, "FY2022": 478286, "FY2021": 1908577}),
    ("DATA", "Long-term subordinated debt", {"FY2025": 59539251, "FY2024": 31600262, "FY2023": 31047446, "FY2022": 35269364, "FY2021": 33284024}),
    ("TOTAL", "Total liabilities", {"FY2025": 1618920572, "FY2024": 1206307310, "FY2023": 1184240745, "FY2022": 1165841071, "FY2021": 1058247938}),
    ("SECTION", "Capital and reserves", {}),
    ("DATA", "Called up share capital", {"FY2025": 130000000, "FY2024": 130000000, "FY2023": 130000000, "FY2022": 130000000, "FY2021": 130000000}),
    ("DATA", "Retained earnings (Profit and loss account)", {"FY2025": 46586699, "FY2024": 42646981, "FY2023": 36857249, "FY2022": 30206249, "FY2021": 24504970}),
    ("TOTAL", "Total capital and reserves", {"FY2025": 176586699, "FY2024": 172646981, "FY2023": 166857249, "FY2022": 160206249, "FY2021": 154504970}),
    ("TOTAL", "Total liabilities and equity", {"FY2025": 1795507271, "FY2024": 1378954291, "FY2023": 1351097994, "FY2022": 1326047320, "FY2021": 1212752908}),
]

bw.add_balance_sheet_sheet(
    title="National Bank of Egypt (UK) Limited — Balance Sheet",
    subtitle="Entity-level basis, £. See source note at bottom.",
    rows=bs_rows,
    sources_text=BALANCE_SHEET_SOURCES,
    first_col_width=100,
    source_height=560,
    unit_suffix=" (£)",
)

# ---------------------------------------------------------------
# Sheet 2: Profit & Loss
# ---------------------------------------------------------------
pl_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest receivable and similar income", {"FY2025": 79298348, "FY2024": 86041222, "FY2023": 75891278, "FY2022": 35253247, "FY2021": 23479081}),
    ("DATA", "Interest payable and similar expense", {"FY2025": -58376403, "FY2024": -64559189, "FY2023": -57165609, "FY2022": -26890680, "FY2021": -14723846}),
    ("TOTAL", "Net interest income", {"FY2025": 20921945, "FY2024": 21482033, "FY2023": 18725669, "FY2022": 8362567, "FY2021": 8755235}),
    ("DATA", "Fees and commission income (net of Trade Finance expense FY2025-FY2024; gross FY2023-FY2021 - see note)", {"FY2025": 2210138, "FY2024": 3457485, "FY2023": 6611004, "FY2022": 12316045, "FY2021": 10227474}),
    ("DATA", "Profit on sale of investments and debt securities", {"FY2025": 1463060, "FY2024": 248249, "FY2023": 499009, "FY2022": 1252198, "FY2021": 1937399}),
    ("DATA", "Net foreign currency gains/(dealing profits)", {"FY2025": 233256, "FY2024": 765137, "FY2023": 176126, "FY2022": 280255, "FY2021": 189766}),
    ("TOTAL", "Operating income", {"FY2025": 24828399, "FY2024": 25952904, "FY2023": 26011808, "FY2022": 22211065, "FY2021": 21109874}),
    ("SECTION", "Operating expenses", {}),
    ("DATA", "Staff costs (Administrative expenses FY2021 - see note)", {"FY2025": -11077928, "FY2024": -10618557, "FY2023": -10150025, "FY2022": -8523451, "FY2021": -12064461}),
    ("DATA", "Depreciation and amortisation", {"FY2025": -1349478, "FY2024": -1150941, "FY2023": -1183345, "FY2022": -791016, "FY2021": -1273488}),
    ("DATA", "Other operating charges", {"FY2025": -6927010, "FY2024": -6292275, "FY2023": -5846753, "FY2022": -5788032, "FY2021": -7916877}),
    # Not itself a printed AR subtotal - the sum of Staff costs + Depreciation
    # and amortisation + Other operating charges above. Excludes Net
    # impairment (charge)/reversal on financial assets, which sits below
    # Operating profit in this bank's own presentation, per standard
    # cost-to-income convention (operating costs only, not credit risk).
    ("TOTAL", "Total operating expenses (sum of Staff costs + Depreciation and amortisation + Other operating charges - excludes net impairment charge/reversal on financial assets)",
     {"FY2025": -19354416, "FY2024": -18061773, "FY2023": -17180123, "FY2022": -15102499, "FY2021": -21254826}),
    ("TOTAL", "Operating profit", {"FY2025": 5473983, "FY2024": 7891131, "FY2023": 8831685, "FY2022": 7108566, "FY2021": -144952}),
    ("DATA", "Net impairment (charge)/reversal on financial assets (Provisions for bad and doubtful debts)", {"FY2025": 0, "FY2024": 0, "FY2023": 0, "FY2022": 0, "FY2021": 443787}),
    ("TOTAL", "Profit on ordinary activities before tax", {"FY2025": 5473983, "FY2024": 7891131, "FY2023": 8831685, "FY2022": 7108566, "FY2021": 298835}),
    ("DATA", "Tax (charge)/credit on profit on ordinary activities", {"FY2025": -1534265, "FY2024": -2101399, "FY2023": -2180685, "FY2022": -1407287, "FY2021": -209949}),
    ("TOTAL", "Profit for the period", {"FY2025": 3939718, "FY2024": 5789732, "FY2023": 6651000, "FY2022": 5701279, "FY2021": 88886}),
    ("DATA", "Other comprehensive income", {"FY2025": 0, "FY2024": 0, "FY2023": 0, "FY2022": 0, "FY2021": 0}),
    ("TOTAL", "Total comprehensive income for the period", {"FY2025": 3939718, "FY2024": 5789732, "FY2023": 6651000, "FY2022": 5701279, "FY2021": 88886}),
]

bw.add_income_statement_sheet(
    title="National Bank of Egypt (UK) Limited — Profit & Loss",
    subtitle="Entity-level basis, £. FY2021 covers an 18-month period (1 July 2020 to 31 December 2021) following an "
              "accounting-reference-date change - see source note at bottom.",
    rows=pl_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=100,
    source_height=380,
    unit_suffix=" (£)",
)

# ---------------------------------------------------------------
# Sheet 3: Statement of Changes in Equity - per-year reconciliation
# ladder confirmed: every year's own closing balance ties exactly to
# both the next year's own opening balance and that year's own
# Balance Sheet Total capital and reserves. Zero plug rows anywhere -
# this entity has no share premium, revaluation reserve, dividends,
# or share issuances in any of the 5 years reviewed.
# ---------------------------------------------------------------
equity_headers = ["Called up share capital", "Profit and loss account", "Total"]
equity_rows = [
    ("TOTAL", "Balance at 1 July 2020 (FY2021 opening)", (130000000, 24416084, 154416084)),
    ("DATA", "Total comprehensive income for the period (18 months to 31 December 2021)", (None, 88886, 88886)),
    ("TOTAL", "Balance at 31 December 2021 (FY2021 closing)", (130000000, 24504970, 154504970)),
    ("DATA", "Total comprehensive income for the year", (None, 5701279, 5701279)),
    ("TOTAL", "Balance at 31 December 2022 (FY2022 closing)", (130000000, 30206249, 160206249)),
    ("DATA", "Total comprehensive income for the year", (None, 6651000, 6651000)),
    ("TOTAL", "Balance at 31 December 2023 (FY2023 closing)", (130000000, 36857249, 166857249)),
    ("DATA", "Total comprehensive income for the year", (None, 5789732, 5789732)),
    ("TOTAL", "Balance at 31 December 2024 (FY2024 closing)", (130000000, 42646981, 172646981)),
    ("DATA", "Total comprehensive income for the year", (None, 3939718, 3939718)),
    ("TOTAL", "Balance at 31 December 2025 (FY2025 closing)", (130000000, 46586699, 176586699)),
]

bw.add_equity_changes_sheet(
    title="National Bank of Egypt (UK) Limited — Statement of Changes in Equity",
    subtitle="Chronological roll-forward, oldest to newest, £. Equity reconciliation ladder confirmed exactly across "
              "all 5 years - zero plug rows. No share premium, revaluation reserve, dividends, or share issuances in "
              "any year reviewed - Called up share capital is unchanged at £130,000,000 throughout.",
    headers=equity_headers,
    rows=equity_rows,
    sources_text=STATEMENTS_SOURCES,
)

rows = [
    ("SECTION", "Operating activities", {}),
    ("TOTAL", "Net cash generated/(used) from operating activities", {"FY2025":101280910,"FY2024":-44497653,"FY2023":-110688337,"FY2022":-91172027,"FY2021":5256681}),
    ("SECTION", "Investing activities", {}),
    ("TOTAL", "Net cash generated/(used) from investing activities", {"FY2025":-122997984,"FY2024":21089132,"FY2023":-16905485,"FY2022":83292813,"FY2021":-5782456}),
    ("SECTION", "Financing activities", {}),
    ("TOTAL", "Net cash generated/(used) in financing activities", {"FY2025":27813180,"FY2024":-2299886,"FY2023":-4776099,"FY2022":-2491694,"FY2021":0}),
    ("TOTAL", "Net decrease/(increase) in cash and cash equivalents", {"FY2025":6096106,"FY2024":-25708407,"FY2023":-132369921,"FY2022":-10370908,"FY2021":-525775}),
    ("DATA", "Cash and cash equivalents at the beginning of year", {"FY2025":286126277,"FY2024":308342852,"FY2023":459632745,"FY2022":53727035,"FY2021":54252810}),
    ("DATA", "Effect of foreign exchange rate changes", {"FY2025":-15465348,"FY2024":3491832,"FY2023":-18919972}),
    ("TOTAL", "Cash and cash equivalents at the end of year", {"FY2025":276757036,"FY2024":286126277,"FY2023":308342852,"FY2022":43356127,"FY2021":53727035}),
]
bw.add_cash_flow_sheet("National Bank of Egypt (UK) Limited — Cash Flow Statement", "Entity-level basis, £", rows, sources("cash"), first_col_width=65, source_height=190, unit_suffix=" (£)")

# ---------------------------------------------------------------
# Sheet 5: Asset Quality - geographic concentration of gross loans
# and advances to customers, plus the bad-and-doubtful-debt
# provision movement. FRS 102 entity - no IFRS 9 stage split
# disclosed. The Bank's own notes explicitly confirm a nil provision
# balance at every one of the 5 year-ends reviewed.
# ---------------------------------------------------------------
asset_quality_rows = [
    ("SECTION", "Gross loans and advances to customers by geography", {}),
    ("DATA", "Europe and North America", {"FY2025": 433660879, "FY2024": 147230099, "FY2023": 17850413, "FY2022": 6344117}),
    ("DATA", "Middle East and Egypt", {"FY2025": 54101742, "FY2024": 33418909, "FY2023": 43127670, "FY2022": 31305384}),
    ("DATA", "Rest of the world", {"FY2025": 0, "FY2024": 872115, "FY2023": 882686, "FY2022": 8854134}),
    ("TOTAL", "Gross loans and advances to customers", {"FY2025": 487762621, "FY2024": 181521123, "FY2023": 61860769, "FY2022": 46503635, "FY2021": 37151779}),
    ("DATA", "Bad and doubtful debt provision - specific (explicitly disclosed as nil every year - not inferred)", {"FY2025": 0, "FY2024": 0, "FY2023": 0, "FY2022": 0, "FY2021": 0}),
    ("TOTAL", "Net loans and advances to customers", {"FY2025": 487762621, "FY2024": 181521123, "FY2023": 61860769, "FY2022": 46503635, "FY2021": 37151779}),
    ("SECTION", "Bad and doubtful debt provision movement and non-performing loans", {}),
    ("DATA", "Net (release)/charge of provisions for bad and doubtful debts", {"FY2025": 0, "FY2024": 0, "FY2023": 0, "FY2022": 0, "FY2021": -443787}),
    ("DATA", "Non-performing loans, net of suspended interest (FY2021 only - see note)", {"FY2021": 0}),
]

bw.add_asset_quality_sheet(
    title="National Bank of Egypt (UK) Limited — Asset Quality",
    subtitle="Entity-level basis, £. FRS 102 entity - no IFRS 9 stage 1/2/3 split disclosed. See source note at bottom.",
    rows=asset_quality_rows,
    sources_text=ASSET_QUALITY_SOURCES,
    first_col_width=100,
    source_height=320,
    unit_suffix=" (£)",
)

def metric(name, unit, label, data, note=None):
    bw.add_metric_sheet(name, unit, [(label, data)], sources("p3"), note=note, first_col_width=48, source_height=170)

metric("CET1 Capital", "£000", "CET1 / Tier 1 capital", {"FY2024":170750,"FY2023":166857,"FY2022":160206,"FY2021":154505}, "FY2021–FY2022 source tables report Tier 1 capital; no AT1 instruments are disclosed, so it is used as CET1. FY2025 not disclosed.")
metric("CET1 Ratio", "%", "CET1 ratio", {"FY2024":"16.31%","FY2023":"17.3%","FY2022":"16.8%"}, "FY2021 standalone CET1 ratio was not separately stated and is left blank rather than substituting the reported leverage ratio.")
metric("Tier 1 Capital", "£000", "Tier 1 capital", {"FY2024":170750,"FY2023":166857,"FY2022":160206,"FY2021":154505})
metric("Tier 1 Ratio", "%", "Tier 1 ratio", {"FY2024":"16.31%","FY2023":"17.3%","FY2022":"16.8%"}, "FY2021 standalone Tier 1 ratio was not separately stated; the reported 12.47% leverage ratio is kept only on the Leverage Ratio sheet.")
metric("Total Capital", "£000", "Total capital resources", {"FY2024":201853,"FY2023":197905,"FY2022":195475,"FY2021":187789})
metric("Total Capital Ratio", "%", "Total capital ratio / capital adequacy ratio", {"FY2024":"19.28%","FY2023":"20.6%","FY2022":"20.54%","FY2021":"15.15%"}, "The older reports label this capital adequacy/total capital ratio and use their stated regulatory denominator; values are not recalculated.")
metric("Total RWAs", "£000", "Total risk-weighted exposure amount / RWA", {"FY2024":1047061,"FY2023":962119,"FY2022":906134,"FY2021":779381})

# ---------------------------------------------------------------
# RWA Breakdown - placed immediately after Total RWAs, before
# Leverage Ratio, per the locked sheet order. A genuine within- and
# cross-document total mismatch exists for FY2021-FY2023 (see source
# note) - flagged, not silently reconciled. FY2025 blank (no Pillar 3
# document located).
# ---------------------------------------------------------------
rwa_breakdown_rows = [
    ("SECTION", "Risk-weighted exposure amounts by category (own OV1 template, FY2024-FY2023; derived from the Pillar 1 capital-requirement table x12.5, FY2022-FY2021 - see note)", {}),
    ("DATA", "Credit risk (excluding CCR)", {"FY2024": 988313, "FY2023": 973878, "FY2022": 906138, "FY2021": 779375}),
    ("DATA", "Counterparty credit risk (CCR)", {"FY2024": 12424, "FY2023": 23332}),
    ("DATA", "Of which: credit valuation adjustment (CVA)", {"FY2024": 5039, "FY2023": 8789, "FY2022": 11350, "FY2021": 363}),
    ("DATA", "Market risk", {"FY2024": 0, "FY2023": 0, "FY2022": 1125, "FY2021": 2138}),
    ("DATA", "Operational risk", {"FY2024": 46325, "FY2023": 43333, "FY2022": 32900, "FY2021": 31350}),
    ("TOTAL", "Total (this table's own category sum)", {"FY2024": 1047061, "FY2023": 1040542, "FY2022": 951513, "FY2021": 813226}),
    ("DATA", "For comparison: this bank's own separately-disclosed Total RWA (Total RWAs sheet - does not tie to the row above for FY2021-FY2023, see note)", {"FY2024": 1047061, "FY2023": 962119, "FY2022": 906134, "FY2021": 779381}),
]

bw.add_rwa_breakdown_sheet(
    title="National Bank of Egypt (UK) Limited — RWA Breakdown",
    subtitle="Entity-level basis, £000. Genuine cross-document/within-document total discrepancy for FY2021-FY2023 - see source note.",
    rows=rwa_breakdown_rows,
    sources_text=RWA_BREAKDOWN_SOURCES,
    first_col_width=100,
    source_height=300,
)

metric("Leverage Ratio", "%", "Leverage ratio", {"FY2024":"11.6%","FY2023":"12.1%","FY2022":"11.65%","FY2021":"12.47%"})
metric("LCR", "%", "Liquidity coverage ratio (average)", {"FY2024":"418%","FY2023":"387%","FY2022":"296%"}, "FY2021 average LCR was not quantified in the located disclosure; FY2025 has no Pillar 3 edition.")
metric("NSFR", "%", "Net stable funding ratio (average)", {"FY2024":"194%","FY2023":"176%","FY2022":"135%"}, "FY2021 NSFR was not quantified in the located disclosure; FY2025 has no Pillar 3 edition.")
bw.add_not_disclosed_metric_sheets(["MREL Ratio"], sources("p3"), per_note={"MREL Ratio": "No MREL ratio was disclosed in the located annual Pillar 3 documents."})

bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {"FY2025": 1795507271, "FY2024": 1378954291, "FY2023": 1351097994, "FY2022": 1326047320, "FY2021": 1212752908}),
        ("Loans and advances to customers", {"FY2025": 487762621, "FY2024": 181521123, "FY2023": 61860769, "FY2022": 46503635, "FY2021": 37151779}),
        ("Customer accounts", {"FY2025": 1388254579, "FY2024": 1032921877, "FY2023": 956051029, "FY2022": 608680668, "FY2021": 248279581}),
        ("Total capital and reserves", {"FY2025": 176586699, "FY2024": 172646981, "FY2023": 166857249, "FY2022": 160206249, "FY2021": 154504970}),
    ],
    balance_sheet_unit="£",
    income_statement_totals=[
        ("Operating income", {"FY2025": 24828399, "FY2024": 25952904, "FY2023": 26011808, "FY2022": 22211065, "FY2021": 21109874}),
        ("Staff costs", {"FY2025": -11077928, "FY2024": -10618557, "FY2023": -10150025, "FY2022": -8523451, "FY2021": -12064461}),
        ("Profit for the period", {"FY2025": 3939718, "FY2024": 5789732, "FY2023": 6651000, "FY2022": 5701279, "FY2021": 88886}),
    ],
    income_statement_unit="£",
    equity_changes_totals=[
        ("Opening total capital and reserves", {"FY2025": 172646981, "FY2024": 166857249, "FY2023": 160206249, "FY2022": 154504970, "FY2021": 154416084}),
        ("Total comprehensive income for the period", {"FY2025": 3939718, "FY2024": 5789732, "FY2023": 6651000, "FY2022": 5701279, "FY2021": 88886}),
        ("Closing total capital and reserves", {"FY2025": 176586699, "FY2024": 172646981, "FY2023": 166857249, "FY2022": 160206249, "FY2021": 154504970}),
    ],
    equity_changes_unit="£",
    cash_flow_totals=[
        ("Net cash generated/(used) from operating activities", {"FY2025":101280910,"FY2024":-44497653,"FY2023":-110688337,"FY2022":-91172027,"FY2021":5256681}),
        ("Net cash generated/(used) from investing activities", {"FY2025":-122997984,"FY2024":21089132,"FY2023":-16905485,"FY2022":83292813,"FY2021":-5782456}),
        ("Net cash generated/(used) in financing activities", {"FY2025":27813180,"FY2024":-2299886,"FY2023":-4776099,"FY2022":-2491694,"FY2021":0}),
        ("Cash and cash equivalents at end of year", {"FY2025":276757036,"FY2024":286126277,"FY2023":308342852,"FY2022":43356127,"FY2021":53727035}),
    ], cash_flow_unit="£", ratios=[
        ("CET1 Ratio", {"FY2024":"16.31%","FY2023":"17.3%","FY2022":"16.8%"}),
        ("Total Capital Ratio", {"FY2024":"19.28%","FY2023":"20.6%","FY2022":"20.54%","FY2021":"15.15%"}),
        ("Leverage Ratio", {"FY2024":"11.6%","FY2023":"12.1%","FY2022":"11.65%","FY2021":"12.47%"}),
        ("LCR", {"FY2024":"418%","FY2023":"387%","FY2022":"296%"}),
    ], note=ENTITY)
# FY2017 (year ended 30 June 2017) headline extension. The Bank's 2018
# annual report identifies the 2017 comparative figures; no historical
# entity-level Pillar 3 document was located, so regulatory metrics stay blank.
_fy17 = {
    "Balance Sheet": {"Total assets": 1438234},
    "Profit & Loss": {"Total operating income": 24891, "Net interest income": 16273,
                      "Profit before taxation": 14438, "Profit for the year": 11514},
}
for _sheet, _values in _fy17.items():
    _ws = bw.wb[_sheet]
    _labels = {str(_ws.cell(r, 1).value).strip(): r for r in range(4, _ws.max_row + 1)}
    _col = 1 + YEARS.index("FY2017") + 1
    for _label, _value in _values.items():
        if _label in _labels:
            _ws.cell(_labels[_label], _col, _value)

bw.save("/Users/armaan/code/katalysis/banks/NATIONAL BANK OF EGYPT UK FINANCIALS.xlsx")
print("Saved.")
