import os
import sys
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021", "FY2017",
         "FY2015", "FY2014", "FY2013", "FY2012", "FY2010", "FY2009"]

# HISTORICAL PILLAR 3 EDITIONS recovered from the Internet Archive on 2026-09-15.
# All are 30 JUNE year-ends (this Bank's accounting reference date until the
# 18-month period ended 31 December 2021) and all are Basel II / CRD-era
# documents predating the UK KM1 template - see HIST_SOURCE_NOTE for the basis
# caveats and for the ratio-label traps that had to be tested arithmetically.
P3_HIST = {
    "FY2015": "https://web.archive.org/web/20160622053404id_/http://nbeuk.com/Pillar3-30062015.pdf",
    "FY2013": "https://web.archive.org/web/20160824045329id_/http://www.nbeuk.com:80/eng/pdf/mak16139-Pillar_3.pdf",
    "FY2010": "https://web.archive.org/web/20110419125423id_/http://www.nbeuk.com:80/eng/pdf/financial/pillar_3_20100630.pdf",
}

AR = {
    "FY2017": "https://www.nbeuk.com/wp-content/uploads/2021/02/NBE_UK_Financial_Statements_2018.pdf",
    "FY2025": "https://find-and-update.company-information.service.gov.uk/company/02743734/filing-history/MzU0MDExNTA0NGFkaXF6a2N4/document?format=pdf&download=0",
    "FY2024": "https://find-and-update.company-information.service.gov.uk/company/02743734/filing-history/MzQ2Mjk2OTExMGFkaXF6a2N4/document?format=pdf&download=0",
    "FY2023": "https://find-and-update.company-information.service.gov.uk/company/02743734/filing-history/MzQxOTgxMTA0NmFkaXF6a2N4/document?format=pdf&download=0",
    "FY2022": "https://find-and-update.company-information.service.gov.uk/company/02743734/filing-history/MzM5NDYwNDY2OGFkaXF6a2N4/document?format=pdf&download=0",
    "FY2021": "https://find-and-update.company-information.service.gov.uk/company/02743734/filing-history/MzM1MTQyMDQxMmFkaXF6a2N4/document?format=pdf&download=0",
}
P3 = {
    "FY2025": "https://www.nbeuk.com/wp-content/uploads/2026/04/NBEUK-Pillar-3-Disclosures-31st-December-2025.pdf",
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
    "Pillar 3 is annual: no defensible entity-level interim disclosure was located."
)

# The Bank's Pillar 3 documents are NOT listed on nbeuk.com's homepage - they sit on the
# /about-us/ page, which is why earlier passes concluded (wrongly) that later editions did
# not exist. nbeuk.com also returns 403 text/html to a bare curl; that is a bot block, not
# an absence. The PDFs retrieve normally (200, application/pdf) with a browser User-Agent
# plus "Referer: https://www.nbeuk.com/about-us/".
#
# Enumerated from that index on 15 September 2026: Pillar 3 editions exist for 2017-2025
# (nine documents); financial reports for 2011-2025.
#
# CORRECTION (2026-09-15, later pass): this script previously concluded "NO Pillar 3 for
# 2011-2016". That was a statement about the CURRENT nbeuk.com index only. The Bank ran an
# older site (www.nbeuk.com/eng/pdf/... and later a flat nbeuk.com/ root) whose Pillar 3
# PDFs are no longer linked from anywhere live but ARE preserved in the Internet Archive.
# Three historical editions were recovered there: 30 June 2010, 30 June 2013 and 30 June
# 2015 (see P3_HIST). They in turn carry prior-year comparative columns that recover a
# further three year-ends - 30 June 2009, 30 June 2012 and 30 June 2014 - as directly
# transcribed figures, not derived ones. Six previously-blank years are now populated.
#
# YEAR-END NOTE. This Bank moved its accounting reference date from 30 June to 31 December
# over an 18-month period ended 31 December 2021, and its Pillar 3 series moves with it:
# the 2017-2020 editions are as at 30 JUNE, the 2021-2025 editions as at 31 DECEMBER
# (confirmed from each document's own cover and running header, not its filename). That
# matters here only for FY2017, which is a 30 June year-end in this workbook - so the
# June-dated FY2017 edition is the correct match, not a mismatch. Independently proved:
# that edition's operational-risk table prints June 2017 Gross Income 24,891 and Net
# Interest Income 16,274, and this workbook's FY2017 column already carried Total operating
# income 24,891 and Net interest income 16,273. The 30 June 2018/2019/2020 editions have no
# corresponding column in this workbook and are deliberately not mapped anywhere.

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
    "FY2025 (own, Template UK OV1): Pillar 3 Disclosures 31 December 2025, Section 5, p.11 - " + P3["FY2025"] + "\n"
    "FY2024 (own, Template UK OV1): Pillar 3 Disclosures 31 December 2024, Section 5 - " + P3["FY2024"] + "\n"
    "FY2023 (own, Template UK OV1): Pillar 3 Disclosures 31 December 2023, Section 5 - " + P3["FY2023"] + "\n"
    "FY2022 (own, Pillar 1 capital-requirement-by-asset-class table): Pillar 3 disclosure 31 December 2022, Section "
    "9/10 - " + P3["FY2022"] + "\n"
    "FY2021 (own, Pillar 1 capital-requirement-by-asset-class table AND a separately-disclosed 'Risk Weighted Assets' "
    "figure): Pillar 3 disclosure 31 December 2021, Section 3/4 - " + P3["FY2021"] + "\n"
    "FY2017: category split deliberately LEFT BLANK. The FY2017 edition is Basel II-era and has no OV1 template; it "
    "gives only a Pillar 1 capital-requirement-by-asset-class table (credit risk 60,601; operational risk 2,349; FX "
    "PRR 90; CVA 41). Converting those to RWAs would require the same x12.5 scalar used for FY2022/FY2021 below, and "
    "that scalar is already demonstrated NOT to reconcile for this bank - so rather than manufacture a third "
    "non-tying total, only the FY2017 edition's own explicitly disclosed 'Risk Weighted Assets' figure (757,515) is "
    "recorded, on the comparison row. Source: Basel II Pillar 3 disclosures for the year ended 30th June 2017, "
    "Sections 3-4, pp.11-13 - https://www.nbeuk.com/wp-content/uploads/2021/02/Draft_Pillar_3-30062017_30112017.pdf "
    "(corroborated by the FY2018 edition's 30/06/2017 comparative column).\n\n"
    + ENTITY + "\n\n"
    "GENUINE CROSS-DOCUMENT DISCREPANCY (flagged, not silently reconciled): this bank's own Pillar 3 documents do not "
    "give one single consistent 'Total RWA' figure per year. FY2025's OV1-template total (£1,261,174k) and FY2024's "
    "(£1,047,061k) both match the Total RWAs sheet exactly - the modern UK OV1/KM1 editions are internally "
    "consistent. FY2023's OV1-template total (£1,040,542k, this table) does NOT match FY2023's own KM1 "
    "summary table in the SAME document (£962,119k, used on the Total RWAs sheet) - a genuine within-document "
    "inconsistency, not a transcription error. FY2022/FY2021 have no OV1 template at all; the categories below are "
    "derived from each year's own Pillar 1 capital-requirement-by-asset-class table (multiplied by 12.5, the standard "
    "8%-to-RWA conversion), giving derived totals of £951,513k (FY2022) and £813,226k (FY2021) that do NOT match "
    "either year's own separately and explicitly disclosed 'Risk Weighted Assets' figure (£906,134k / £779,381k, used "
    "on the Total RWas sheet) - again a genuine document-internal gap (the capital-requirement components evidently "
    "don't sum linearly to the disclosed RWA total via the standard 12.5x scalar), not an error introduced here. Each "
    "year's own best-available category split is shown as-is.\n\n"
    "FY2015-FY2009 (the recovered Basel II editions): NO RWA CATEGORY SPLIT IS SHOWN, for the same reason as FY2017. "
    "Those editions give only a Pillar 1 capital-requirement-by-risk-type table, and converting it to RWAs would "
    "need the same x12.5 scalar that is already demonstrated not to reconcile for this bank in FY2022/FY2021. What "
    "IS shown for those years, on its own clearly-labelled block of rows, is the printed CAPITAL requirement by risk "
    "type exactly as disclosed - in £000 of capital, not RWA, and not to be read down the same column as the RWA "
    "rows above it. That block is worth having because it is the direct evidence that each of those years' printed "
    "'Risk Weighted Assets' line is the credit-risk RWA only: credit risk capital x12.5 reproduces the printed RWA "
    "in all six columns, while the printed total Pillar 1 requirement x12.5 does not. Sources: 30 June 2015 edition "
    "Section 4, p.13 (FY2015 and its FY2014 comparative); 30 June 2013 edition Section 4, p.14 (FY2013 and its "
    "FY2012 comparative); 30 June 2010 edition Section 3, p.11 (FY2010 and its FY2009 comparative) - see the "
    "historical-series note on the metric sheets for the three URLs. The FY2013 and FY2012 counterparty line is the "
    "printed combined figure (counterparty risk capital component plus foreign exchange PRR: 43 + 56 = 99 for "
    "FY2013, 210 + 262 = 472 for FY2012), because those two editions subtotal them together on the face of the "
    "table; FY2015/FY2014 print market risk separately and are shown that way."
)


def sources(kind):
    if kind == "cash":
        return ("Sources - National Bank of Egypt (UK) Limited entity-level Cash Flow Statement, £:\n" +
                "\n".join(f"{y}: Companies House Annual Report for {y[2:]}, Cash Flow Statement - {AR[y]}" for y in YEARS if y in AR) +
                "\n\nFY2015/FY2014/FY2013/FY2012/FY2010/FY2009 are regulatory-only columns added from the Bank's recovered "
                "historical Pillar 3 editions (see the Pillar 3 metric sheets); no Companies House annual report for those "
                "years was sourced in this pass, so the financial-statement sheets are deliberately blank for them rather "
                "than populated from the Pillar 3 documents, which disclose regulatory capital only.\n\n"
                "FY2021/FY2022 are condensed cash-flow presentations in the filed accounts; the reported subtotals and opening/closing cash chain are preserved.\n\n"
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
            "\n" + FY2025_SOURCE_NOTE + "\n\n" + FY2017_SOURCE_NOTE + "\n\n" + HIST_SOURCE_NOTE + "\n\n" + ENTITY)


# FY2025 (year ended 31 December 2025 - a normal 12-month December year-end; see
# the YEAR-END NOTE above for the June-to-December reference-date change that
# ended with the 18-month FY2021 period).
#
# CORRECTION (2026-09-15). This script previously asserted, in five places, that
# "no FY2025 Pillar 3 disclosure exists as at 15 September 2026", and carried
# FY2025 on an Annual-Report basis with Total RWAs, CET1 Ratio, Tier 1 Ratio and
# NSFR left blank. That was WRONG. The FY2025 Pillar 3 is published, at
# /wp-content/uploads/2026/04/, and carries a complete UK KM1 and UK OV1.
#
# Two things had masked it. (1) The Pillar 3 documents are linked from nbeuk.com's
# /about-us/ page, not the homepage. (2) nbeuk.com returns 403 text/html to a bare
# curl - a bot block that reads as a 404-ish absence; the file downloads normally
# with a browser User-Agent plus a /about-us/ Referer. Neither is evidence of
# non-publication, and the earlier "confirmed 404 on the expected URL pattern"
# conclusion was an artefact of both.
#
# The previously-recorded Annual-Report figures all survive the switch: the
# Pillar 3 states 18.2% / 9.2% / 390% where the Annual Report stated 18.24% /
# 9.2% / 390.41%, i.e. the two agree to the Annual Report's extra decimal place.
# Those more precise AR values are therefore KEPT rather than rounded down to the
# Pillar 3's one-decimal presentation.
FY2025_SOURCE_NOTE = (
    "FY2025: Pillar 3 Disclosures 31 December 2025 - " + P3["FY2025"] + "\n"
    "  - UK KM1 'Key metrics', p.4 (rows 1-3): CET1 capital 172,460; Tier 1 capital 172,460; Total capital "
    "230,038. Row 4: Total risk-weighted exposure amount 1,261,174. Rows 5-7: CET1 ratio 13.7%, Tier 1 "
    "ratio 13.7%, Total capital ratio 18.2%. Rows 13-14/14b: leverage ratio 9.2% both including and "
    "excluding claims on central banks. Row 17: LCR 390%. Row 20: NSFR 150%.\n"
    "  - UK OV1 'Own funds requirements and risk-weighted exposure amounts', p.11: category split behind "
    "the 1,261,174 total (see the RWA Breakdown sheet).\n"
    "  - Narrative, p.4: 'the Bank's CET1 ratio decreased from 16.3% to 13.7% and the Bank's total capital "
    "ratio reduced from 19.3% to 18.2%', RWAs up 20% on 30.2% total-asset growth; Tier 2 reflects $40m of "
    "subordinated debt raised in the year.\n"
    "PRECISION NOTE: Total Capital Ratio 18.24%, Leverage Ratio 9.2% and LCR 390.41% are retained from the "
    "Annual Report 2025 (Strategic Report pp.12/23 - " + AR["FY2025"] + ", a scanned image-only Companies "
    "House filing read by OCR), because the Pillar 3 states the same figures to one decimal place (18.2% / "
    "9.2% / 390%). The two documents agree; the more precise statement is used.\n"
    "VALIDATION GATE PASSED: every FY2024 comparative in the FY2025 Pillar 3 reproduces this workbook's "
    "existing FY2024 figures exactly - CET1 and Tier 1 capital 170,750; Total capital 201,853; Total RWA "
    "1,047,061; CET1 and Tier 1 ratio 16.3% (recorded here as 16.31%); total capital ratio 19.3% (19.28%); "
    "leverage ratio 11.6%; LCR 418%; NSFR 194%. The FY2024 OV1 comparative column ties too: credit risk "
    "988,313, CCR 12,424, CVA 5,039, market risk nil, operational risk 46,325, total 1,047,061. Nothing was "
    "overwritten."
)

# FY2017 (year ended 30 June 2017). Regulatory data added 2026-09-15 from the
# Bank's own Basel II Pillar 3 disclosure for that year - previously blank on
# every metric sheet because the 2017-2020 editions had not been located.
#
# The file is named Draft_Pillar_3-30062017_30112017.pdf. It is NOT a draft in
# substance: the string "draft" appears nowhere in the document, and its cover and
# running header both read "Basel II, Pillar 3 disclosures for the year ended 30th
# June 2017". The trailing 30112017 is a publication/approval date, consistent
# with its note 1 referring to the Board and AGM meetings of 18 September 2017.
# In any case nothing rests on that file alone: every FY2017 figure below is
# independently reproduced by the FY2018 edition's own 30/06/2017 comparative
# column, which is a separate, unambiguously final document.
FY2017_SOURCE_NOTE = (
    "FY2017 (year ended 30 June 2017 - this Bank's year-end was 30 June until the 18-month period ended "
    "31 December 2021): Basel II Pillar 3 disclosures for the year ended 30th June 2017, Section 3 "
    "'Capital Resources' / Section 4 'Capital Adequacy', pp.11-13 - "
    "https://www.nbeuk.com/wp-content/uploads/2021/02/Draft_Pillar_3-30062017_30112017.pdf\n"
    "  - Tier 1 capital after deductions 143,847 (called up share capital 130,000 + retained earnings and "
    "other reserves 13,847; no AT1 instruments disclosed, so used as CET1 on the same convention as the "
    "other years). Tier 2 (subordinated debt) 34,629. Total capital resources 178,476. Risk Weighted Assets "
    "757,515. Total Exposures 1,453,451. Total Pillar 1 capital requirement 63,082.\n"
    "  - CONFIRMED INDEPENDENTLY: the FY2018 edition's own 30/06/2017 comparative column (Section 3, p.12 - "
    "https://www.nbeuk.com/wp-content/uploads/2021/02/2018_Basel_ll_Pillar_3_Disclosure.pdf) reproduces "
    "every one of those figures exactly, so the 'Draft'-named FY2017 file is corroborated rather than "
    "relied on alone.\n"
    "  - YEAR MATCH PROVED, not assumed: the FY2017 edition's operational-risk table prints June 2017 Gross "
    "Income 24,891 and Net Interest Income 16,274, matching the Total operating income 24,891 and Net "
    "interest income 16,273 already carried in this workbook's FY2017 column from the 2018 Annual Report.\n"
    "  - RATIO LABELS IN THAT TABLE ARE UNRELIABLE AND WERE TESTED ARITHMETICALLY BEFORE USE (see the "
    "individual ratio sheets' notes). Three of the four printed ratios are NOT what their labels say: "
    "'SOLVENCY RATIO' 282.93% is a capital-COVER ratio (capital against the capital requirement), not a CRR "
    "ratio, and is used nowhere; 'TOTAL CAPITAL RATIO' 12.28% is total capital divided by total EXPOSURES "
    "(178,476 / 1,453,451 = 12.279%, and on the 2016 column 160,423 / 1,464,093 = 10.957% vs the printed "
    "10.95%), a leverage-style measure that is deliberately NOT placed on the Total Capital Ratio sheet; "
    "and 'TIER 1 CAPITAL RATIO ( LEVERAGE )' 9.90% is the leverage ratio (143,847 / 1,453,451 = 9.897%), "
    "not a CRR Tier 1 ratio, so it appears only on the Leverage Ratio sheet.\n"
    "  - WITHIN-DOCUMENT CONTRADICTION, RESOLVED: the FY2017 edition's note 3 narrative says the capital "
    "adequacy ratio 'declined to 21.90%' and the leverage ratio 'stood at 9.5%', contradicting its own "
    "table on the facing page (22.63% and 9.90%). The FY2018 edition settles it - its table repeats 22.63% "
    "and 9.90% for 30/06/2017, and its note 3 reads 'capital adequacy ratio increased to 22.77% at the end "
    "of June 2018 compared to 22.63% in June 2017'. The table values are used; the two narrative figures "
    "are errors confined to that one document. Recorded here so a later pass does not reverse this."
)

# FY2015 / FY2014 / FY2013 / FY2012 / FY2010 / FY2009 - the recovered historical
# Pillar 3 series (all 30 June year-ends, all Basel II / CRD-era). Added 2026-09-15.
#
# BASIS WARNING, applied throughout below. These editions predate CRD IV entirely.
# They have no CET1 concept, no CRR leverage-ratio template, no CRR LCR and no UK
# NSFR. Nothing from them is placed on a CRR row without an explicit basis label,
# and nothing is back-solved: every figure below is a line printed in a document.
#
# The three recovered documents share this Bank's characteristic house style, in
# which the ratio ROW LABELS do not mean what they say. Each was tested against
# the document's own figures before any use:
#   * "SOLVENCY RATIO" is a capital-COVER ratio - total capital resources over the
#     total Pillar 1 capital requirement - not a CRR ratio. Proved on four columns:
#     FY2009 122,391/47,903 = 255.50% (printed 255.50%); FY2010 127,422/42,050 =
#     303.03% (printed 303.03%); FY2012 150,469/24,870 = 605.02% (printed 605.02%);
#     FY2013 149,733/28,474 = 525.85% (printed 525.85%). USED NOWHERE.
#   * "CAPITAL ADEQUACY RATIO" IS a genuine total-capital-to-RWA ratio in these
#     older editions, unlike FY2017's. Proved on all six columns: FY2009
#     122,391/562,792 = 21.75%; FY2010 127,422/480,466 = 26.52%; FY2012
#     150,469/275,431 = 54.63%; FY2013 149,733/324,189 = 46.19%; FY2014
#     151,829/487,653 = 31.13%; FY2015 153,368/469,969 = 32.63% - each reproducing
#     the printed figure exactly. It is therefore placed on the Total Capital Ratio
#     sheet, with the denominator caveat recorded on that sheet.
#   * "TIER 1 CAPITAL RATIO ( LEVERAGE )" (FY2015 edition only) is the leverage
#     ratio, not a CRR Tier 1 ratio: FY2015 134,291/1,044,368 = 12.858% vs the
#     printed 12.86%. It goes on the Leverage Ratio sheet only.
# No CET1 ratio and no Tier 1 ratio is printed in any of the three editions, and
# none is derived here.
#
# PRINTED "RISK WEIGHTED ASSETS" IS THE CREDIT-RISK RWA ONLY - a real defect in
# the source documents, recorded rather than corrected because no document states
# a true total. In every one of the six columns the printed RWA line equals that
# column's own "Credit Risk Capital 8%" line times 12.5, to the rounding: FY2009
# 45,023 -> 562,787 vs printed 562,792; FY2010 38,437 -> 480,462 vs 480,466;
# FY2012 22,034 -> 275,425 vs 275,431; FY2013 25,935 -> 324,187 vs 324,189;
# FY2014 39,012 -> 487,650 vs 487,653; FY2015 37,598 -> 469,975 vs 469,969. The
# operational-, market- and counterparty-risk capital components are excluded, so
# each year's true total RWA is higher. The standard test in this project - does
# the document's own printed capital ratio reproduce against that denominator? -
# comes back YES here, because the Bank computes its own printed capital adequacy
# ratio on the same credit-only denominator. So the printed ratio cannot be used
# as evidence to replace the total, and grossing the total Pillar 1 requirement up
# by 12.5 would be back-solving. Both the printed RWA and the printed ratio are
# transcribed exactly as disclosed, and the understatement is flagged on the Total
# RWAs and RWA Breakdown sheets so the series is not read as comparable with the
# FY2021-FY2025 UK OV1/KM1 totals.
HIST_SOURCE_NOTE = (
    "HISTORICAL PILLAR 3 SERIES (FY2015, FY2014, FY2013, FY2012, FY2010, FY2009 - all 30 JUNE year-ends, all "
    "Basel II/CRD-era, £000). Recovered from the Internet Archive on 15 September 2026 from this Bank's former "
    "website; they are no longer linked from anywhere live on nbeuk.com and had previously been recorded in this "
    "script as non-existent.\n"
    "FY2015 & FY2014: 'Basel II, Pillar 3 disclosures for the year ended 30th June 2015', Section 3 'Capital "
    "Resources' / Section 4 'Capital Adequacy', p.11, and Section 5 'Liquidity Risk', p.14 - " + P3_HIST["FY2015"] + "\n"
    "  - As at 30/06/2015: called up share capital 130,000 + retained earnings and other reserves 4,291 = Tier 1 "
    "capital after deductions 134,291; Tier 2 (subordinated debt) 19,077; total capital resources 153,368; total "
    "exposures 1,044,368; Risk Weighted Assets 469,969; credit risk capital 37,598, operational risk capital 2,418, "
    "market risk capital 9, counterparty risk capital 26, TOTAL PILLAR 1 CAPITAL 40,051.\n"
    "  - As at 30/06/2014 (that edition's own comparative column): Tier 1 134,291; Tier 2 17,538; total capital "
    "151,829; total exposures 1,418,324; Risk Weighted Assets 487,653; credit risk capital 39,012, operational risk "
    "2,424, market risk 41, counterparty risk 20, TOTAL PILLAR 1 CAPITAL 41,497.\n"
    "  - This document is a photocopier scan with no text layer. It was rendered at 250dpi and OCR'd, and every "
    "figure above was then re-read visually off the page image before use (p.11 capital table and p.14 liquidity "
    "table), per this project's standing OCR rule. Two OCR misreads were caught and corrected that way: the market "
    "risk capital line came back as 'A 9' (correct: 41 and 9) and the Core Funding Ratio as 'WM%' (correct: 31%).\n"
    "FY2013 & FY2012: 'Basel II, Pillar 3 disclosures for the year ended 30th June 2013', Section 3 'Capital "
    "Resources' / Section 4 'Capital Adequacy', pp.12-14, and Section 5 'Liquidity Risk', p.14 - " + P3_HIST["FY2013"] + "\n"
    "  - As at 30/06/2013: called up share capital 130,000 + retained earnings and other reserves 0 = Tier 1 capital "
    "after deductions 130,000; Tier 2 (subordinated debt 19,733 + collective provisions 0) 19,733; total capital "
    "resources 149,733; total exposures 1,051,317; Risk Weighted Assets 324,189; credit risk capital 25,935, "
    "operational risk capital 2,440, counterparty risk capital 99, TOTAL CAPITAL ALLOCATIONS 28,474.\n"
    "  - As at 30/06/2012 (that edition's own comparative column): Tier 1 130,000; Tier 2 20,469 (subordinated debt "
    "19,119 + collective provisions 1,350); total capital 150,469; total exposures 1,148,476; Risk Weighted Assets "
    "275,431; credit risk capital 22,034, operational risk 2,364, counterparty risk 472, TOTAL CAPITAL ALLOCATIONS "
    "24,870.\n"
    "  - This edition has a genuine text layer; figures were read directly, not by OCR.\n"
    "FY2010 & FY2009: 'Basel II, Pillar 3 disclosures for the year ended 30th June 2010', Section 3 'Capital "
    "Resources', p.11 - " + P3_HIST["FY2010"] + "\n"
    "  - As at 30/06/2010: called up share capital 130,000 + retained earnings and other reserves (6,078) = Tier 1 "
    "capital after deductions 123,922; Tier 2 (collective provisions 3,500; subordinated debt NIL) 3,500; total "
    "capital resources 127,422; total exposures 1,479,384; Risk Weighted Assets 480,466; credit risk capital 38,437, "
    "operational risk capital 2,656, counterparty risk capital 957, TOTAL CAPITAL ALLOCATIONS 42,050.\n"
    "  - As at 30/06/2009 (that edition's own comparative column): Tier 1 118,891 (share capital 130,000 + reserves "
    "(11,109)); Tier 2 3,500; total capital 122,391; total exposures 1,391,957; Risk Weighted Assets 562,792; credit "
    "risk capital 45,023, operational risk 2,700, counterparty risk 180, TOTAL CAPITAL ALLOCATIONS 47,903.\n"
    "  - Also a photocopier scan with no text layer, OCR'd at 250dpi and re-read visually off the p.11 page image.\n"
    "  - That edition's own note 3 independently confirms the RWA reading: it describes the GBP3.5mn collective "
    "provision as '0.73% of the total risk weighted assets (GBP480.5mn)', matching the 480,466 transcribed above.\n\n"
    "RATIO LABELS TESTED ARITHMETICALLY BEFORE USE - this Bank's house style mislabels them. 'SOLVENCY RATIO' is a "
    "capital-COVER ratio (total capital over the total Pillar 1 requirement), proved on four columns (FY2009 "
    "122,391/47,903 = 255.50%; FY2010 127,422/42,050 = 303.03%; FY2012 150,469/24,870 = 605.02%; FY2013 "
    "149,733/28,474 = 525.85%, each reproducing its printed figure exactly) and is used NOWHERE. 'CAPITAL ADEQUACY "
    "RATIO' in these older editions IS a genuine total-capital-over-RWA ratio - unlike the FY2017 edition's "
    "separately-labelled 'TOTAL CAPITAL RATIO', which is capital over total EXPOSURES - and reproduces exactly on "
    "all six columns, so it is placed on the Total Capital Ratio sheet. 'TIER 1 CAPITAL RATIO ( LEVERAGE )', printed "
    "only in the FY2015 edition, is the leverage ratio (FY2015 134,291/1,044,368 = 12.858% vs printed 12.86%) and "
    "appears only on the Leverage Ratio sheet. NO CET1 ratio and NO Tier 1 ratio is printed in any of the three "
    "editions; neither is derived here, so both sheets stay blank for these years.\n\n"
    "THE PRINTED 'RISK WEIGHTED ASSETS' LINE IS THE CREDIT-RISK RWA ONLY, in all six columns - a defect in the "
    "source documents, recorded rather than corrected. Each printed RWA equals that column's own 'Credit Risk "
    "Capital 8%' line x12.5 to the rounding (FY2009 45,023 -> 562,787 vs printed 562,792; FY2010 38,437 -> 480,462 "
    "vs 480,466; FY2012 22,034 -> 275,425 vs 275,431; FY2013 25,935 -> 324,187 vs 324,189; FY2014 39,012 -> 487,650 "
    "vs 487,653; FY2015 37,598 -> 469,975 vs 469,969), excluding the operational-, market- and counterparty-risk "
    "components, so each year's true total RWA is higher than shown. The usual test for this defect - does the "
    "document's own printed capital ratio reproduce against that denominator? - comes back YES here, because the "
    "Bank computes its printed capital adequacy ratio on the same credit-only denominator. So there is no printed "
    "ratio that contradicts the total, and grossing the TOTAL PILLAR 1 CAPITAL line up by 12.5 would be back-solving "
    "a figure no document states. Both the printed RWA and the printed ratio are therefore transcribed exactly as "
    "disclosed and flagged, not adjusted.\n\n"
    "EDITIONS SEARCHED FOR AND NOT RECOVERED - the distinction matters and is recorded so it is not re-chased:\n"
    "  - FY2016 (30 June 2016): PUBLISHED, CAPTURE BROKEN. The Internet Archive holds a capture of the expected URL, "
    "but it is a capture of a 404 page, not of the document. Absent, not proven unpublished.\n"
    "  - FY2011, FY2012, FY2014 (30 June 2011/2012/2014): PUBLISHED BUT LOST - not 'never published'. No Internet "
    "Archive capture of any of the three exists, yet the Bank's own FY2014 financial statements state that its "
    "Pillar 3 disclosures were published on its website, and the Bank's own FY2013 edition states the report 'will "
    "be made on an annual basis ... and will be published within six months of the Accounting Reference Date'. The "
    "documents existed and were public; the web captures simply do not. FY2012 and FY2014 data is nonetheless "
    "recovered in full above from the FY2013 and FY2015 editions' own comparative columns. FY2011 is not recovered "
    "by any comparative column, because the edition that would carry it - FY2011's or FY2012's own - is itself one "
    "of the lost three; its cells are left blank rather than filled from any other basis.\n"
    "  - FY2008 and earlier: not searched in this pass.\n\n"
    "VALIDATION GATE. These six columns are additive - they occupy year columns that were entirely empty before this "
    "pass, and they overlap no existing column, so nothing was overwritten. Each recovered edition's comparative "
    "column was reconciled against the adjacent edition where one exists: none of the three recovered editions is "
    "adjacent to another (2010/2013/2015), so no cross-edition comparative check was possible, and each year's "
    "figures rest on the single edition cited for it. The FY2015 edition's 30/06/2014 column and the FY2013 "
    "edition's 30/06/2012 column are each internally consistent with their own document (capital components sum to "
    "the printed totals; the printed capital adequacy and solvency ratios reproduce from the printed capital and "
    "RWA lines), which is the only verification available for those two years."
)

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

PILLAR3_BASIS_FY2025 = (
    " FY2025 is Pillar 3-basis, from the FY2025 Pillar 3's UK KM1 (p.4). A previous build wrongly recorded "
    "that no FY2025 Pillar 3 existed; it does - see sources. PAGE CORRECTED 2026-09-17 from p.5 to p.4 "
    "(both places this script cited it): the KM1 table sits on the page whose own printed folio is 4, "
    "which the document states twice - the page carries '4' in its header, and the contents page indexes "
    "section 2 'KEY METRICS' to page 3, the narrative occupying p.3 and the table p.4. The same holds in "
    "the FY2024 and FY2023 editions."
)

FY2017_BASIS = (
    " FY2017 is a 30 June year-end (this Bank's year-end before the 18-month period ended 31 December 2021) "
    "and is Basel II-era, from the FY2017 Pillar 3's capital resources/capital adequacy table, corroborated "
    "figure-for-figure by the FY2018 edition's 30/06/2017 comparative column - see sources."
)

HIST_BASIS = (
    " FY2015-FY2009 are 30 June year-ends on a Basel II/CRD basis, from three Internet-Archive-recovered Pillar 3 "
    "editions (30 June 2010, 2013 and 2015) plus those editions' own comparative columns for FY2009/FY2012/FY2014. "
    "They are NOT on the UK CRR/KM1 basis used for FY2021-FY2025 and should not be read as one continuous series "
    "with them. FY2011 is blank because the edition carrying it is lost, and FY2016's only archive capture is a 404 "
    "- see sources."
)


# ---------------------------------------------------------------
# KM1 Key Metrics - the Bank's own "Template UK KM1 - Key metrics", printed
# in the FY2023, FY2024 and FY2025 Pillar 3 editions. FY2022 is filled from
# the FY2023 edition's own 31/12/2022 comparative column because the FY2022
# edition prints NO key-metrics template at all (map rule 28); FY2021 stays
# blank because no edition anywhere prints a 31/12/2021 KM1 column.
# ---------------------------------------------------------------
KM1_YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]

km1_rows = [
    ("SECTION", "Available own funds (amounts) £000s", {}),
    ("DATA", "1 Common Equity Tier 1 (CET1) capital (£000s)", {"FY2025": 172460, "FY2024": 170750, "FY2023": 166857, "FY2022": 160206}),
    ("DATA", "2 Tier 1 capital (£000s)", {"FY2025": 172460, "FY2024": 170750, "FY2023": 166857, "FY2022": 160206}),
    ("DATA", "3 Total capital (£000s)", {"FY2025": 230038, "FY2024": 201853, "FY2023": 197905, "FY2022": 195090}),
    ("SECTION", "Risk-weighted exposure amounts £000s", {}),
    ("DATA", "4 Total risk-weighted exposure amount (£000s)", {"FY2025": 1261174, "FY2024": 1047061, "FY2023": 962119, "FY2022": 951508}),
    ("SECTION", "Capital ratios (as a percentage of risk-weighted exposure amount)", {}),
    ("DATA", "5 Common Equity Tier 1 ratio (%)", {"FY2025": "13.7", "FY2024": "16.31", "FY2023": "17.3", "FY2022": "16.8"}),
    ("DATA", "6 Tier 1 ratio (%)", {"FY2025": "13.7", "FY2024": "16.31", "FY2023": "17.3", "FY2022": "16.8"}),
    ("DATA", "7 Total capital ratio (%)", {"FY2025": "18.2", "FY2024": "19.28", "FY2023": "20.6", "FY2022": "20.5"}),
    ("SECTION", "Additional own funds requirements based on SREP (as a percentage of risk-weighted exposure amount)", {}),
    ("DATA", "UK 7a Additional CET1 SREP requirements (%)", {"FY2025": "2.7", "FY2024": "2.71", "FY2023": "2.7", "FY2022": "2.7"}),
    ("DATA", "UK 7b Additional AT1 SREP requirements (%)", {"FY2025": "0.9", "FY2024": "0.91", "FY2023": "0.9", "FY2022": "0.9"}),
    ("DATA", "UK 7c Additional T2 SREP requirements (%)", {"FY2025": "1.2", "FY2024": "1.20", "FY2023": "1.2", "FY2022": "1.2"}),
    ("DATA", "UK 7d Total SREP own funds requirements (%)", {"FY2025": "12.8", "FY2024": "12.82", "FY2023": "12.9", "FY2022": "12.9"}),
    ("SECTION", "Combined buffer requirement (as a percentage of risk-weighted exposure amount)", {}),
    ("DATA", "8 Capital conservation buffer (%)", {"FY2025": "2.5", "FY2024": "2.50", "FY2023": "2.5", "FY2022": "2.5"}),
    ("DATA", "UK 8a Conservation buffer due to macro-prudential or systemic risk identified at the level of a Member State (%)", {}),
    ("DATA", "9 Institution specific countercyclical capital buffer (%)", {"FY2025": "0.7", "FY2024": "0.33", "FY2023": "0.3"}),
    ("DATA", "UK 9a Systemic risk buffer (%)", {}),
    ("DATA", "10 Global Systemically Important Institution buffer (%)", {}),
    ("DATA", "UK 10a Other Systemically Important Institution buffer", {}),
    ("DATA", "11 Combined buffer requirement (%)", {"FY2025": "3.2", "FY2024": "2.83", "FY2023": "2.8", "FY2022": "2.5"}),
    ("DATA", "UK 11a Overall capital requirements (%)", {"FY2025": "16.1", "FY2024": "15.65", "FY2023": "15.7", "FY2022": "15.4"}),
    ("DATA", "12 CET1 available after meeting the total SREP own funds requirements (%)", {"FY2025": "6.5", "FY2024": "9.10", "FY2023": "10.1", "FY2022": "9.6"}),
    ("SECTION", "Leverage ratio", {}),
    ("DATA", "13 Total exposure measure excluding claims on central banks (£000s)", {"FY2025": 1866639, "FY2024": 1469717, "FY2023": 1382667, "FY2022": 1611977}),
    ("DATA", "14 Leverage ratio excluding claims on central banks (%)", {"FY2025": "9.2", "FY2024": "11.6", "FY2023": "12.1", "FY2022": "9.9"}),
    ("SECTION", "Additional leverage ratio disclosure requirements", {}),
    ("DATA", "14a Fully loaded ECL accounting model leverage ratio excluding claims on central banks (%)", {"FY2023": "12.1", "FY2022": "9.9"}),
    ("DATA", "14b Leverage ratio including claims on central banks (%)", {"FY2025": "9.2", "FY2024": "11.6", "FY2023": "12.1", "FY2022": "9.9"}),
    ("SECTION", "Liquidity Coverage Ratio", {}),
    ("DATA", "15 Total high-quality liquid assets (HQLA) (Weighted value - average) (£000s)", {"FY2025": 162904, "FY2024": 161608, "FY2023": 170092, "FY2022": 196635}),
    ("DATA", "UK 16a Cash outflows - Total weighted value (£000s)", {"FY2025": 166904, "FY2024": 154826, "FY2023": 175689, "FY2022": 265921}),
    ("DATA", "UK 16b Cash inflows - Total weighted value (£000s)", {"FY2025": 227895, "FY2024": 374963, "FY2023": 303103, "FY2022": 437377}),
    ("DATA", "16 Total net cash outflows (adjusted value) (£000s)", {"FY2025": 41726, "FY2024": 38707, "FY2023": 43922, "FY2022": 66480}),
    ("DATA", "17 Liquidity coverage ratio (%)", {"FY2025": "390", "FY2024": "418", "FY2023": "387", "FY2022": "296"}),
    ("SECTION", "Net Stable Funding Ratio", {}),
    ("DATA", "18 Total available stable funding (£000s)", {"FY2025": 1075320, "FY2024": 923549, "FY2023": 811359, "FY2022": 579930}),
    ("DATA", "19 Total required stable funding (£000s)", {"FY2025": 715469, "FY2024": 476002, "FY2023": 460395, "FY2022": 428828}),
    ("DATA", "20 NSFR ratio (%)", {"FY2025": "150", "FY2024": "194", "FY2023": "176", "FY2022": "135"}),
]

bw.add_km1_sheet(
    title="National Bank of Egypt (UK) Limited — KM1 Key Metrics",
    subtitle="The Bank's own 'Template UK KM1 - Key metrics', reproduced whole in its own row order, row "
             "numbers, labels and precision, entity-level (NBEUK) basis, £000s for amounts and "
             "percentages as printed - the Bank prints its ratios as bare numbers (13.7, not 13.7%) and "
             "that is kept. FY2025, FY2024 and FY2023 are each from that year's own edition. FY2022 is "
             "the FY2023 edition's 31/12/2022 comparative column, because the FY2022 edition prints no "
             "KM1 at all. FY2021 is blank: no edition anywhere prints a 31/12/2021 KM1 column. Years "
             "before FY2021 are not shown - they predate the template entirely (see the source note).",
    rows=km1_rows,
    sources_text=sources("p3") + "\n\n" + (
        "KM1 SHEET SOURCES - one edition per column:\n"
        "FY2025: Pillar 3 Disclosures 31 December 2025, section 2 'KEY METRICS', Template UK KM1, p.4 - "
        + P3["FY2025"] + "\n"
        "FY2024: Pillar 3 Disclosures 31 December 2024, section 2 'KEY METRICS', Template UK KM1, p.4 - "
        + P3["FY2024"] + "\n"
        "FY2023: Pillar 3 Disclosures 31 December 2023, section 2 'KEY METRICS', Template UK KM1, p.4 - "
        + P3["FY2023"] + "\n"
        "FY2022: THE FY2022 EDITION PRINTS NO KM1 TEMPLATE, so this column is the FY2023 edition's own "
        "31/12/2022 comparative column (same table, p.4). This is the one filled-from-a-comparative "
        "column on this sheet and it is flagged so a reader can always tell it from an own-edition "
        "column. It is filled rather than blanked because the FY2022 document publishes no such table "
        "for a later one to displace: the FY2022 edition (" + P3["FY2022"] + ") is a Basel II-style "
        "document whose section 9.0 'CAPITAL RESOURCES' and 10.0 'CAPITAL ADEQUACY' print a bespoke "
        "two-column table - called up share capital, retained earnings, Tier 1/Tier 2 after deductions, "
        "total exposures, RWAs, the four Pillar 1 capital requirement lines, a capital planning buffer, "
        "a solvency ratio, a capital adequacy ratio, a 'Tier 1 Capital Ratio (Leverage)' and a 'Total "
        "Capital Ratio'. That is NOT an unnumbered KM1: it has no SREP rows, no combined buffer "
        "requirement, no LCR and no NSFR rows, so mapping it onto template row numbers would invent a "
        "correspondence the Bank never published.\n"
        "FY2021 AND EARLIER ARE BLANK. The FY2021 edition (" + P3["FY2021"] + ") prints the same "
        "bespoke capital-resources/capital-adequacy pair as FY2022 and no template, and NO later "
        "edition carries a 31/12/2021 comparative - the FY2022 edition has no KM1 at all and the "
        "FY2023 edition's comparative column is 31/12/2022. So there is nothing to fill FY2021 from, "
        "on any basis, in any edition. The earlier years this workbook carries (FY2017 and the "
        "recovered Basel II years FY2015-FY2009) predate the UK KM1 template altogether and are not "
        "shown as columns on this sheet; their figures remain on the single-metric sheets, on the "
        "Basel II basis those sheets describe.\n\n"
        "PAGE CITATIONS CORRECTED 2026-09-17. This script previously cited the FY2025 KM1 at p.5 in two "
        "places. The table is on the page whose own printed folio is 4, stated twice by the document: "
        "the page carries '4' in its header, and the contents page indexes section 2 'KEY METRICS' to "
        "page 3, with the narrative on p.3 and the table on p.4. The same holds in the FY2024 and "
        "FY2023 editions.\n\n"
        "KNOWN DISAGREEMENTS WITH THE SINGLE-METRIC SHEETS - ALL IN FY2022, ALL CROSS-EDITION, NONE "
        "RECONCILED. The single-metric sheets carry FY2022 from the FY2022 edition's own bespoke table; "
        "this sheet carries the FY2023 edition's restated comparative for the same date. They differ on "
        "three rows and the differences are the finding, not an error:\n"
        "  - Total capital: 195,090 here against 195,475 on the Total Capital sheet.\n"
        "  - Total risk-weighted exposure amount: 951,508 here against 906,134 on the Total RWAs sheet "
        "(the FY2022 edition's own 'Risk Weighted Assets' line).\n"
        "  - Leverage ratio: 9.9 here against 11.65% on the Leverage Ratio sheet. The FY2022 edition's "
        "figure is its row labelled 'Tier 1 Capital Ratio (Leverage)', computed on that table's own "
        "'Total Exposures' of 1,375,734; the KM1 comparative uses a UK CRR total exposure measure of "
        "1,611,977 for the same date. Different denominators on different bases, both printed by the "
        "Bank, neither adjusted here.\n"
        "A fourth, smaller one sits in FY2025: row 7 prints 18.2 where the Total Capital Ratio sheet "
        "carries the Annual Report's more precise 18.24%, and row 17 prints 390 against the Annual "
        "Report's 390.41%. Those are the same figures at different precision and are left as each "
        "document printed them."
    ),
    first_col_width=88,
    source_height=420,
    years=KM1_YEARS,
)


def metric(name, unit, label, data, note=None):
    metric_rows(name, unit, [(label, data)], note=note)


def metric_rows(name, unit, rows, note=None):
    """rows: list of (label, {year: value}) pairs - used where two series must be
    kept on separate labelled rows rather than merged into one (e.g. the Basel II
    observation-period LCR, which is not the same measure as the later CRR LCR)."""
    bw.add_metric_sheet(name, unit, rows, sources("p3"), note=note,
                        first_col_width=48, source_height=170)

metric("CET1 Capital", "£000", "CET1 / Tier 1 capital", {"FY2025":172460,"FY2024":170750,"FY2023":166857,"FY2022":160206,"FY2021":154505,"FY2017":143847,"FY2015":134291,"FY2014":134291,"FY2013":130000,"FY2012":130000,"FY2010":123922,"FY2009":118891}, "FY2021-FY2022 and FY2017 source tables report Tier 1 capital; no AT1 instruments are disclosed in any year, so it is used as CET1 (the FY2025 accounts' own capital-management note states the Directors apply Common Equity Tier 1 Capital and Tier 2 Capital only). FY2025's own UK KM1 states CET1 and Tier 1 capital as the same 172,460, confirming that treatment directly. FY2017 is called up share capital 130,000 plus retained earnings and other reserves 13,847. FY2015-FY2009 apply the same convention to the recovered Basel II editions' 'Tier 1 capital after deductions' line, which in those years is called up share capital 130,000 plus retained earnings and other reserves of 4,291 (FY2015 and FY2014), nil (FY2013 and FY2012), (6,078) (FY2010) and (11,109) (FY2009); those editions disclose no AT1 or hybrid instrument, and Tier 2 in them is subordinated debt and collective provisions only. STRICTLY SPEAKING CET1 DID NOT EXIST BEFORE CRD IV (1 January 2014), so for FY2013 and earlier this row carries the Basel II core Tier 1 measure under a CET1 heading, not a CRD IV CET1 calculation - no CET1-specific deduction or filter regime applied at the time." + PILLAR3_BASIS_FY2025 + FY2017_BASIS + HIST_BASIS)
metric("CET1 Ratio", "%", "CET1 ratio", {"FY2025":"13.7%","FY2024":"16.31%","FY2023":"17.3%","FY2022":"16.8%"}, "FY2025 13.7% is stated directly at UK KM1 row 5 and repeated in the FY2025 Pillar 3's own narrative ('the Bank's CET1 ratio decreased from 16.3% to 13.7%'), the fall driven by a 20% rise in RWAs against 1% CET1 growth. FY2021 standalone CET1 ratio was not separately stated and is left blank rather than substituting the reported leverage ratio. FY2017 blank: neither the FY2017 nor the FY2018 edition states a CET1-to-RWA ratio - the only Tier 1 ratio printed is the leverage one - and it is deliberately not back-solved from 143,847 / 757,515. FY2015-FY2009 blank for the same reason: none of the three recovered Basel II editions prints a CET1 ratio (the concept did not exist before CRD IV), and the only Tier-1-labelled ratio any of them prints is the FY2015 edition's 'TIER 1 CAPITAL RATIO ( LEVERAGE )', which is the leverage ratio and is recorded only there." + FY2017_BASIS + HIST_BASIS)
metric("Tier 1 Capital", "£000", "Tier 1 capital", {"FY2025":172460,"FY2024":170750,"FY2023":166857,"FY2022":160206,"FY2021":154505,"FY2017":143847,"FY2015":134291,"FY2014":134291,"FY2013":130000,"FY2012":130000,"FY2010":123922,"FY2009":118891}, "FY2017 and FY2015-FY2009 are each edition's own 'Tier 1 capital after deductions' line as printed, on a Basel II/CRD basis. Note the FY2015 and FY2014 columns are identical at 134,291 because the FY2015 edition's own note 1 records that the Bank retained the FY2014 profit of GBP4.291mn and then resolved at the 2015 AGM to pay out 100% of realised FY2015 profit as a dividend - so share capital plus reserves did not move over the year; this is the source documents' own position, not a duplicated transcription." + PILLAR3_BASIS_FY2025 + FY2017_BASIS + HIST_BASIS)
metric("Tier 1 Ratio", "%", "Tier 1 ratio", {"FY2025":"13.7%","FY2024":"16.31%","FY2023":"17.3%","FY2022":"16.8%"}, "FY2025 13.7% is stated directly at UK KM1 row 6 (equal to the CET1 ratio, as the Bank has no AT1). FY2021 standalone Tier 1 ratio was not separately stated; the reported 12.47% leverage ratio is kept only on the Leverage Ratio sheet. FY2017 blank: the FY2017 table's row labelled 'TIER 1 CAPITAL RATIO ( LEVERAGE )' 9.90% is arithmetically the LEVERAGE ratio (143,847 / 1,453,451 = 9.897%), not a CRR Tier 1 ratio, so it is recorded only on the Leverage Ratio sheet and no Tier 1 ratio is claimed here. FY2015-FY2009 blank for the same reason - the FY2015 edition repeats that same mislabelled leverage row and the FY2013 and FY2010 editions print no Tier-1-based ratio at all; none is derived." + FY2017_BASIS + HIST_BASIS)
metric("Total Capital", "£000", "Total capital resources", {"FY2025":230038,"FY2024":201853,"FY2023":197905,"FY2022":195475,"FY2021":187789,"FY2017":178476,"FY2015":153368,"FY2014":151829,"FY2013":149733,"FY2012":150469,"FY2010":127422,"FY2009":122391}, "FY2015-FY2009 are each edition's own 'Total capital resources' line: Tier 1 after deductions plus Tier 2 after deductions, where Tier 2 is subordinated debt of 19,077 (FY2015), 17,538 (FY2014), 19,733 (FY2013) and 19,119 (FY2012) plus collective provisions of 1,350 (FY2012) and 3,500 (FY2010 and FY2009, where the subordinated debt line reads NIL - the FY2010 edition's note 2 records a USD30m lower Tier 2 facility committed by the parent on 25/02/2009 that was still undrawn). FY2025 comprises Tier 1 172,460 plus Tier 2 57,578 (long-term subordinated debt from the parent Bank, reflecting $40m raised during the year per the FY2025 Pillar 3's own narrative); the Tier 2 element grew from 31,103 at FY2024. FY2017 comprises Tier 1 143,847 plus Tier 2 subordinated debt 34,629." + PILLAR3_BASIS_FY2025 + FY2017_BASIS + HIST_BASIS)
metric("Total Capital Ratio", "%", "Total capital ratio / capital adequacy ratio", {"FY2025":"18.24%","FY2024":"19.28%","FY2023":"20.6%","FY2022":"20.54%","FY2021":"15.15%","FY2017":"22.63%","FY2015":"32.63%","FY2014":"31.13%","FY2013":"46.19%","FY2012":"54.63%","FY2010":"26.52%","FY2009":"21.75%"}, "FY2015-FY2009 are each edition's own printed 'CAPITAL ADEQUACY RATIO'. Unlike FY2017's, these ARE genuine total-capital-over-RWA ratios and were proved so before use, each reproducing its printed value exactly from the same document's own capital and RWA lines (FY2015 153,368/469,969 = 32.63%; FY2014 151,829/487,653 = 31.13%; FY2013 149,733/324,189 = 46.19%; FY2012 150,469/275,431 = 54.63%; FY2010 127,422/480,466 = 26.52%; FY2009 122,391/562,792 = 21.75%). The FY2015 and FY2013 editions corroborate their own figures in narrative too ('our capital adequacy ratio improved to 32.63% in June 2015 compared to 31.13% in June 2014'; 'our capital adequacy ratio stood at 46.19% in June 2013 compared to 54.63% in June 2012'). DENOMINATOR CAVEAT, and the reason these levels look extraordinarily high next to FY2021-FY2025: the denominator is each edition's printed 'Risk Weighted Assets' line, which is demonstrably the CREDIT-RISK RWA only (it equals that column's own credit risk capital x12.5 in all six years - see sources), so it excludes operational, market and counterparty risk. The ratios are therefore overstated relative to a true total-RWA basis, and are not comparable with the UK CRR figures for FY2021-FY2025. They are transcribed exactly as disclosed rather than recomputed, because no document states a true total RWA and recomputing would mean back-solving one. The older reports label this capital adequacy/total capital ratio and use their stated regulatory denominator; values are not recalculated. FY2025 18.24% is the Annual Report's more precise statement of the 18.2% at UK KM1 row 7 - the two documents agree. FY2017 22.63% is the printed 'CAPITAL ADEQUACY RATIO', confirmed by the FY2018 edition both in its comparative column and in its note 3 ('compared to 22.63% in June 2017'); it supersedes the 21.90% in the FY2017 edition's own note 3, which contradicts its own table. Note the FY2017 table ALSO prints a row labelled 'TOTAL CAPITAL RATIO' (12.28%) which is deliberately NOT used here: it is total capital over total EXPOSURES (178,476 / 1,453,451), a leverage-style measure, as the 2016 column proves (160,423 / 1,464,093 = 10.957% vs printed 10.95%). The printed 22.63% likewise does not reproduce as 178,476 / 757,515 (= 23.56%), so it is recorded exactly as disclosed and not recalculated." + PILLAR3_BASIS_FY2025 + FY2017_BASIS + HIST_BASIS)
metric("Total RWAs", "£000", "Total risk-weighted exposure amount / RWA", {"FY2025":1261174,"FY2024":1047061,"FY2023":962119,"FY2022":906134,"FY2021":779381,"FY2017":757515,"FY2015":469969,"FY2014":487653,"FY2013":324189,"FY2012":275431,"FY2010":480466,"FY2009":562792}, "FY2015-FY2009 ARE UNDERSTATED AND ARE NOT COMPARABLE WITH THE LATER YEARS - read this before using them. Each is the printed 'Risk Weighted Assets' line of that year's Basel II edition, but that line is the CREDIT-RISK RWA only: in all six columns it equals the same column's own 'Credit Risk Capital 8%' line x12.5 to the rounding (FY2015 37,598 -> 469,975 vs printed 469,969; FY2014 39,012 -> 487,650 vs 487,653; FY2013 25,935 -> 324,187 vs 324,189; FY2012 22,034 -> 275,425 vs 275,431; FY2010 38,437 -> 480,462 vs 480,466; FY2009 45,023 -> 562,787 vs 562,792). Operational, market and counterparty risk are excluded, so each year's true total RWA is higher - materially so in FY2013, where the total Pillar 1 capital allocation of 28,474 is 9.8% above the credit-only 25,935. The project's usual diagnostic (does the document's own printed capital ratio reproduce against that denominator?) does NOT rescue these: it reproduces exactly, because the Bank computes its printed capital adequacy ratio on the same credit-only base. There is therefore no printed ratio contradicting the total and no document-stated total to substitute, and grossing the total Pillar 1 requirement up by 12.5 would be back-solving - so the printed figures stand as disclosed, flagged. The FY2010 edition's own note 3 confirms the Bank itself treated 480,466 as its total ('0.73% of the total risk weighted assets (GBP480.5mn)'), i.e. the understatement is the source's, not this workbook's. FY2025 1,261,174 is stated at UK KM1 row 4 and is corroborated within the same document by the UK OV1 total (see the RWA Breakdown sheet) - the two tie exactly for FY2025, unlike FY2023 where this Bank's own OV1 and KM1 disagree. A previous build left FY2025 blank on the incorrect basis that no FY2025 Pillar 3 existed. FY2017 757,515 is the 'Risk Weighted Assets' line of the FY2017 capital adequacy table, confirmed by the FY2018 edition's comparative column." + PILLAR3_BASIS_FY2025 + FY2017_BASIS + HIST_BASIS)

# ---------------------------------------------------------------
# RWA Breakdown - placed immediately after Total RWAs, before
# Leverage Ratio, per the locked sheet order. A genuine within- and
# cross-document total mismatch exists for FY2021-FY2023 (see source
# note) - flagged, not silently reconciled. FY2025 blank (no Pillar 3
# document located).
# ---------------------------------------------------------------
rwa_breakdown_rows = [
    ("SECTION", "Risk-weighted exposure amounts by category (own OV1 template, FY2025-FY2023; derived from the Pillar 1 capital-requirement table x12.5, FY2022-FY2021 - see note. FY2017 category split deliberately left blank - see note)", {}),
    ("DATA", "Credit risk (excluding CCR)", {"FY2025": 1198794, "FY2024": 988313, "FY2023": 973878, "FY2022": 906138, "FY2021": 779375}),
    ("DATA", "Counterparty credit risk (CCR)", {"FY2025": 15766, "FY2024": 12424, "FY2023": 23332}),
    ("DATA", "Of which: credit valuation adjustment (CVA)", {"FY2025": 4804, "FY2024": 5039, "FY2023": 8789, "FY2022": 11350, "FY2021": 363}),
    ("DATA", "Market risk", {"FY2025": 0, "FY2024": 0, "FY2023": 0, "FY2022": 1125, "FY2021": 2138}),
    ("DATA", "Operational risk", {"FY2025": 46614, "FY2024": 46325, "FY2023": 43333, "FY2022": 32900, "FY2021": 31350}),
    ("TOTAL", "Total (this table's own category sum)", {"FY2025": 1261174, "FY2024": 1047061, "FY2023": 1040542, "FY2022": 951513, "FY2021": 813226}),
    ("DATA", "For comparison: this bank's own separately-disclosed Total RWA (Total RWAs sheet - ties exactly for FY2025 and FY2024; does NOT tie for FY2023-FY2021, see note. FY2015-FY2009 are credit-risk RWA only - see note)", {"FY2025": 1261174, "FY2024": 1047061, "FY2023": 962119, "FY2022": 906134, "FY2021": 779381, "FY2017": 757515, "FY2015": 469969, "FY2014": 487653, "FY2013": 324189, "FY2012": 275431, "FY2010": 480466, "FY2009": 562792}),
    ("SECTION", "Pillar 1 capital requirement by risk type, Basel II editions FY2015-FY2009 (£000 of CAPITAL, not RWA - deliberately NOT multiplied by 12.5, see note)", {}),
    ("DATA", "Capital requirement - credit risk (standardised)", {"FY2015": 37598, "FY2014": 39012, "FY2013": 25935, "FY2012": 22034, "FY2010": 38437, "FY2009": 45023}),
    ("DATA", "Capital requirement - operational risk (basic indicator)", {"FY2015": 2418, "FY2014": 2424, "FY2013": 2440, "FY2012": 2364, "FY2010": 2656, "FY2009": 2700}),
    ("DATA", "Capital requirement - market risk (no separate line disclosed FY2013/FY2012/FY2010/FY2009)", {"FY2015": 9, "FY2014": 41}),
    ("DATA", "Capital requirement - counterparty risk (FY2013/FY2012 line combines counterparty risk capital with foreign exchange PRR: FY2013 43 + 56; FY2012 210 + 262)", {"FY2015": 26, "FY2014": 20, "FY2013": 99, "FY2012": 472, "FY2010": 957, "FY2009": 180}),
    ("TOTAL", "Total Pillar 1 capital requirement as printed ('TOTAL PILLAR 1 CAPITAL' / 'TOTAL CAPITAL ALLOCATIONS')", {"FY2015": 40051, "FY2014": 41497, "FY2013": 28474, "FY2012": 24870, "FY2010": 42050, "FY2009": 47903}),
]

bw.add_rwa_breakdown_sheet(
    title="National Bank of Egypt (UK) Limited — RWA Breakdown",
    subtitle="Entity-level basis, £000. Genuine cross-document/within-document total discrepancy for FY2021-FY2023 - see source note.",
    rows=rwa_breakdown_rows,
    sources_text=RWA_BREAKDOWN_SOURCES,
    first_col_width=100,
    source_height=300,
)

metric("Leverage Ratio", "%", "Leverage ratio", {"FY2025":"9.2%","FY2024":"11.6%","FY2023":"12.1%","FY2022":"11.65%","FY2021":"12.47%","FY2017":"9.9%","FY2015":"12.86%","FY2014":"9.17%"}, "FY2015 12.86% and FY2014 9.17% are the FY2015 edition's row labelled 'TIER 1 CAPITAL RATIO ( LEVERAGE )' - the same mislabelled row as FY2017's, and a leverage ratio rather than a CRR Tier 1 ratio, so it is recorded here and not on the Tier 1 Ratio sheet. FY2015 reproduces exactly as Tier 1 over that table's own Total Exposures line (134,291 / 1,044,368 = 12.858%), and the edition's own note 4 repeats it in narrative ('NBEUK's leverage ratio stood at 12.86% which is maintained well above the regulatory requirements of 3%'). FY2014's 9.17% does NOT reproduce that way (134,291 / 1,418,324 = 9.468%), and the difference is recorded rather than resolved: the most likely explanation is that the June 2014 figure was computed on the then-new CRD IV leverage exposure measure, which includes off-balance-sheet and derivative add-ons and so differs from the accounting 'Total Exposures' line printed beside it, but no document reviewed states the exposure measure used. It is transcribed exactly as printed and is NOT recalculated to 9.47%, which would be substituting a back-solved figure for a disclosed one. FY2013, FY2012, FY2010 and FY2009 are blank: those editions print no leverage ratio of any kind, and for FY2010/FY2009 the concept did not yet exist (Basel III was not published until December 2010). FY2025 9.2% is stated at UK KM1 rows 14 and 14b - identical including and excluding claims on central banks - and the Annual Report 2025 states the same 9.2%. The Annual Report 2025 states FY2024 as 11.62%, consistent with the 11.6% recorded here from the FY2024 Pillar 3. FY2017 9.9% is the FY2017 table's row labelled 'TIER 1 CAPITAL RATIO ( LEVERAGE )', which is arithmetically Tier 1 over total exposures (143,847 / 1,453,451 = 9.897%) and is therefore a leverage ratio, not a CRR Tier 1 ratio; the FY2018 edition's comparative column repeats 9.90% for 30/06/2017, superseding the 9.5% in the FY2017 edition's own note 3, which contradicts its own table." + PILLAR3_BASIS_FY2025 + FY2017_BASIS + HIST_BASIS)
metric_rows("LCR", "%", [
    ("Liquidity coverage ratio (12-month average, UK CRR basis)", {"FY2025":"390.41%","FY2024":"418%","FY2023":"387%","FY2022":"296%","FY2021":"Not disclosed - FY2021 P3 s.5 (p.11) is prose only, no figure printed"}),
    ("One-month liquidity coverage ratio (Basel II observation-period basis, point-in-time - NOT comparable with the row above)", {"FY2017":"201%","FY2015":"314%","FY2014":"Not available - no 30/06/2014 edition; FY2015 table is single-column","FY2013":"422%"}),
], "FY2015 314% and FY2013 422% extend the LOWER row only, never the upper one. Both are printed in their edition's own Section 5 liquidity-mismatch table as 'One month liquidity coverage ratio (LCR)' against an internal minimum of 60%, and both sit directly above a footnote stating that 'LCR, Core Funding and NFSR ratios are currently on an observation period and will be implemented as a regulatory requirement by January 2015 and January 2018 respectively' - i.e. they are pre-CRR internal point-in-time measures on the Bank's own definition, computed alongside FSA 047/048 mismatch reporting, not the CRR Delegated Regulation 2015/61 LCR and not a 12-month average. FY2014 and FY2012 are blank because the liquidity tables in those editions carry no comparative column (unlike the capital tables, which do). FY2010 and FY2009 are blank because the 30 June 2010 edition quantifies no liquidity ratio at all - its liquidity section is narrative only - and no LCR existed in any form before Basel III was published in December 2010. TWO DIFFERENT SERIES, DELIBERATELY NOT MERGED INTO ONE ROW. The upper row is the UK CRR 12-month average LCR: FY2025 is UK KM1 row 17 (390%), recorded to the Annual Report 2025's more precise 390.41%; the Annual Report also states FY2024 as 417.52% and FY2023 as 387.26%, matching the 418% and 387% recorded here from those years' Pillar 3 summaries. FY2021 average LCR IS NOT QUANTIFIED ANYWHERE, and that was tested properly on 2026-09-18 rather than left as 'not located'. The FY2021 Pillar 3 (31 December 2021) was re-downloaded and read: its Section 5 'LIQUIDITY RISK' on printed p.11 is four paragraphs of prose with no table and no number, ending 'The LCR is comfortably above the minimum regulatory requirements and conforms to best practice standards' - an explicit refusal to state the figure, not an omission. The FY2022 edition's Section 5 does the same for both ratios ('The LCR of the Bank is comfortably above...', 'The NSFR is also comfortably above...'), so the neighbouring edition cannot supply it either, and the FY2023 edition's UK KM1 carries a 31/12/2022 comparative column only. FY2021 is the 18-month period ended 31 December 2021 and no KM1 was published for it at all. FY2014 is likewise unobtainable rather than merely unfound: the whole nbeuk.com domain was enumerated via Wayback CDX on 2026-09-18 (888 captured URLs, archive up and answering) and the only Pillar 3 editions ever captured are 30/06/2010, 30/06/2015, the undated /eng/pdf/mak16139-Pillar_3.pdf already cited here, 30/06/2017, 30/06/2018, 30/06/2019, 30/06/2020 and the December editions from 2021 on - there is no 30 June 2014 edition in the index, and the 30/06/2015 edition's Section 5 liquidity table was re-read at 200 dpi and is single-column (30 June 2015 only), unlike that same document's counterparty, provisions and exposure tables, which all print a 30/06/2014 comparative. So the FY2014 blank is a genuine absence in every document that can be reached, with the question of whether a 30 June 2014 edition was ever published left open. The lower row is a different measure entirely: the FY2017 Pillar 3's Section 5 prints 'One month liquidity coverage ratio (LCR) 201%' against an internal minimum of 90%, and that same page states 'LCR, Core Funding and NFSR ratios are currently on an observation period and will be implemented as a regulatory standard starting from 1 January 2018'. It is a pre-CRR, point-in-time internal metric, so combining it with the 12-month CRR averages above would create a false trend. RE-VERIFIED INDEPENDENTLY 2026-09-19, AND THE TWO BLANKS NOW SAY WHAT THEY ARE. (a) FY2021: the 31 December 2021 Pillar 3 was re-downloaded from the Bank's own site and re-read from the document, not from this note. The first attempt returned HTTP 403 with a bare 'Mozilla/5.0'; a full browser header set with a Referer returned HTTP 200, Content-Type application/pdf, %PDF magic bytes, 456,363 bytes - recorded because a 403 here is a fact about the request, never about the Bank. Extracted text is native (72,161 characters; richness control 418 occurrences of ' the '). Section 5 'LIQUIDITY RISK' on printed p.11 runs four paragraphs and ends, verbatim: 'The LCR is comfortably above the minimum regulatory requirements and conforms to best practice standards.' No table, no number. The string 'NSFR' occurs ONCE in the whole document, in a sentence about which daily reports the Financial Control team issues. So the FY2021 absence is the Bank declining to state a figure it plainly computes - outcome 'never published', and the cell says so rather than standing empty. (b) FY2014: the nbeuk.com domain was re-enumerated by Wayback CDX and now returns 972 captured URLs (up from 888 last year - the archive is live and answering, which is the positive control). Sixteen of them are Pillar 3 or Basel artefacts, and the edition list is unchanged: 30/06/2010, 30/06/2015, the undated mak16139 file, a 404-status capture of a 30/06/2016 filename, 30/06/2017, 2018, 30/06/2019, 30/06/2020 and the December editions from 2021 on. There is still no 30 June 2014 edition anywhere. The WordPress media REST endpoint - the one route that can list UNLINKED uploads - is blocked on this host (HTTP 401, 'itsec_rest_api_access_restricted', Kadence Security), so that rung was tried and failed and is reported as a limit rather than a result. FY2014 therefore stays classified UNREACHED, not never-published: its cell reads 'Not available', deliberately different wording from FY2021's, because the two are different findings." + PILLAR3_BASIS_FY2025 + FY2017_BASIS + HIST_BASIS)
# GA-020 (2026-09-19): the bare "Not applicable" on the UK-CRR NSFR row now gives
# its reason. This row is by definition the UK CRR NSFR (PRA PS17/21, in force
# 1 January 2022), which cannot exist for a period ending before that date; what
# the pre-2022 editions DID print is the Basel observation-period NFSR, kept on
# its own row below (FY2015 81%, FY2013 97%). The FY2017 edition's s.5 states
# the NSFR was still 'on an observation period'.
NSFR_PRE2022_NA = ("Not applicable – this row is the UK CRR NSFR, in force from 1 Jan 2022 (PRA PS17/21); pre-2022 "
                   "editions print only a Basel observation-period NFSR, carried on the row below where printed")
metric_rows("NSFR", "%", [
    ("Net stable funding ratio (average, UK CRR basis)", {"FY2025":"150%","FY2024":"194%","FY2023":"176%","FY2022":"135%","FY2021":"Not applicable - UK NSFR began 1 Jan 2022; FY2021 P3 prints no figure",**{y: NSFR_PRE2022_NA for y in ["FY2017","FY2015","FY2014","FY2013","FY2012","FY2010","FY2009"]}}),
    ("Net stable funding ratio (Basel observation-period basis, point-in-time - NOT comparable with the row above)", {"FY2015":"81%","FY2013":"97%"}),
], "THE 'NOT APPLICABLE' CELLS ON THE UPPER ROW ARE STRUCTURAL, NOT GAPS. The UK had no NSFR requirement and no NSFR disclosure template before 1 January 2022 (PRA PS17/21), so no CRR-basis NSFR can exist for FY2017 or for any of FY2015-FY2009. The lower row carries what those years' documents DO state, on a different basis and therefore on its own row: the 30 June 2015 edition's Section 5 liquidity table prints 'Net Stable Funding Ratio (NFSR) 81%' against an internal minimum of 100%, and the 30 June 2013 edition prints 97% on the same line, each directly above the same footnote - 'LCR, Core Funding and NFSR ratios are currently on an observation period and will be implemented as a regulatory requirement by January 2015 and January 2018 respectively'. Those are the Bank's own point-in-time observation-period measures under the then-draft Basel III standard, not the UK NSFR, and merging them into the upper row would manufacture a fifteen-year series out of two incompatible definitions. FY2014 and FY2012 are blank on the lower row because those editions' liquidity tables have no comparative column; FY2010 and FY2009 are blank there because the 30 June 2010 edition quantifies no liquidity ratio at all. FY2025 150% is stated at UK KM1 row 20 (available stable funding 1,075,320 / required stable funding 715,469), the fall from 194% attributed by the Bank's own narrative to growth in corporate loans and debt securities; a previous build left this blank on the incorrect basis that no FY2025 Pillar 3 existed. FY2021 NSFR is not quantified anywhere, and there are two reasons rather than one - the structural reason and a documentary one, both checked 2026-09-18. Structurally, the UK had no NSFR requirement or disclosure template before 1 January 2022, and FY2021 is the 18-month period ended 31 December 2021. Documentarily, the FY2021 Pillar 3's Section 5 (printed p.11) is prose with no figures at all, the FY2022 edition's equivalent section says only 'The NSFR is also comfortably above the minimum regulatory requirements', and the FY2023 edition's UK KM1 prints a 31/12/2022 comparative column and nothing earlier. So there is no NSFR figure to recover for FY2021 from any edition, and the cell stays blank. FY2017 is marked Not applicable on the same structural ground, and the FY2017 Pillar 3 confirms it directly: the NSFR was then on an 'observation period' with no figure disclosed. UPDATED 2026-09-19: FY2021 no longer stands BLANK - it now carries the same 'Not applicable' statement as FY2017 and earlier, with its own reason, because a blank cell cannot distinguish an established finding from a cell nobody examined and this one is established twice over. The structural half: the UK NSFR requirement began 1 January 2022 and FY2021 is the 18-month period ended 31 December 2021, one day before it. The documentary half, re-checked from the document today rather than from this note: the 31 December 2021 Pillar 3 was re-fetched (HTTP 200, application/pdf, %PDF, 456,363 bytes, 72,161 characters of native text, 418 occurrences of ' the ' as the richness control) and the string 'NSFR' appears ONCE in the entire document - in a sentence listing the daily reports the Financial Control team issues - with no figure anywhere. See the LCR sheet's note for the full re-verification, including the HTTP 403 that the first fetch attempt returned and which a fuller header set cleared." + PILLAR3_BASIS_FY2025 + HIST_BASIS)
# GA-020 (2026-09-19): every edition that can be reached was re-downloaded
# (browser headers + /about-us/ Referer for nbeuk.com; the two image-only Wayback
# editions, 30/06/2015 and 30/06/2010, OCR'd) and full-text searched for MREL /
# loss-absorbing / eligible liabilities: zero hits in all nine. Periods ending
# before 1 January 2015 predate the BRRD's UK transposition, which created MREL.
_NBE_MREL = {y: (f"Not published – NBE UK {y} Pillar 3 (full text searched 2026-09-19) contains no MREL figure or "
                 "reference to MREL, loss-absorbing capacity or eligible liabilities")
             for y in ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021", "FY2017", "FY2015"]}
_NBE_MREL.update({y: (f"Not applicable – MREL did not exist for a period ending 30 June {y[2:]}: it was created by the "
                      "BRRD (Directive 2014/59/EU), transposed in the UK from 1 January 2015")
                  for y in ["FY2014", "FY2013", "FY2012", "FY2010", "FY2009"]})
bw.add_not_disclosed_metric_sheets(["MREL Ratio"], sources("p3"), statements={"MREL Ratio": _NBE_MREL}, per_note={"MREL Ratio": "No MREL ratio was disclosed in the located annual Pillar 3 documents. For FY2017 and the recovered Basel II years FY2015-FY2009 this is structural as well as factual: MREL did not exist as a UK requirement then (BRRD was transposed in the UK in January 2015 and the Bank of England's MREL policy statement followed in November 2016), so no MREL ratio could have been disclosed."})

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
        ("CET1 Ratio", {"FY2025":"13.7%","FY2024":"16.31%","FY2023":"17.3%","FY2022":"16.8%"}),
        # FY2015-FY2009 Total Capital Ratio is on a Basel II credit-risk-only RWA
        # denominator (see the Total Capital Ratio sheet) - carried here because it
        # is the same printed "capital adequacy ratio" measure the sheet holds, with
        # the basis flagged in the row label rather than silently presented as one
        # continuous CRR series.
        ("Total Capital Ratio (FY2017 and earlier are Basel II-basis - see Total Capital Ratio sheet)", {"FY2025":"18.24%","FY2024":"19.28%","FY2023":"20.6%","FY2022":"20.54%","FY2021":"15.15%","FY2017":"22.63%","FY2015":"32.63%","FY2014":"31.13%","FY2013":"46.19%","FY2012":"54.63%","FY2010":"26.52%","FY2009":"21.75%"}),
        ("Leverage Ratio", {"FY2025":"9.2%","FY2024":"11.6%","FY2023":"12.1%","FY2022":"11.65%","FY2021":"12.47%","FY2017":"9.9%","FY2015":"12.86%","FY2014":"9.17%"}),
        # LCR: FY2017's 201% is the Basel II observation-period one-month LCR, a
        # different measure from the 12-month CRR average shown for FY2022-FY2025.
        # It is kept on its own labelled row on the LCR sheet and deliberately NOT
        # carried into this single Overview row, which would imply one series.
        ("LCR (12-month average, UK CRR basis)", {"FY2025":"390.41%","FY2024":"418%","FY2023":"387%","FY2022":"296%"}),
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
    # Resolve the column from the sheet's own header, never from an index into
    # YEARS: column trimming cannot see a year supplied out-of-band like this,
    # so `YEARS.index(...)` silently pointed past the end of the header and
    # wrote these figures into an unlabelled column. See patch_year_column.
    bw.patch_year_column(_sheet, "FY2017", _values)

bw.save("/Users/armaan/code/katalysis/banks/NATIONAL BANK OF EGYPT UK FINANCIALS.xlsx")
print("Saved.")
