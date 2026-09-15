import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021", "FY2020"]  # most recent first
YEAR_LABEL = {y: y for y in YEARS}

AR2025_URL = "https://wp-dfcapital-investors-2020.s3.eu-west-2.amazonaws.com/media/2026/03/DF-Capital-Annual-Report-and-Accounts-year-ending-2025.pdf"
AR2023_URL = "https://wp-dfcapital-investors-2020.s3.eu-west-2.amazonaws.com/media/2024/04/DF-Capital-Annual-Report-and-Accounts-year-ending-2023-1.pdf"
AR2021_URL = "https://wp-dfcapital-investors-2020.s3.eu-west-2.amazonaws.com/media/2022/05/Annual-report-and-accounts-year-end-2021.pdf"
AR2020_URL = "https://wp-dfcapital-investors-2020.s3.eu-west-2.amazonaws.com/media/2021/04/21070044/Annual-report-and-accounts-Year-end-2020-Final-compressed.pdf"
P3_2025_URL = "https://wp-dfcapital-investors-2020.s3.eu-west-2.amazonaws.com/media/2026/03/DF-Capital-Pillar-III-2025.pdf"
P3_2024_URL = "https://wp-dfcapital-investors-2020.s3.eu-west-2.amazonaws.com/media/2025/04/Distribution-Finance-Capital-Holdings-plc-Pillar-3-Disclosures-at-31-December-2024.pdf"
P3_2023_URL = "https://wp-dfcapital-investors-2020.s3.eu-west-2.amazonaws.com/media/2024/04/DF-Capital-Pillar-III_2024-FINAL.pdf"
P3_2022_URL = "https://wp-dfcapital-investors-2020.s3.eu-west-2.amazonaws.com/media/2023/04/Pillar-3-Disclosures-31-December-2022.pdf"
P3_2021_URL = "https://wp-dfcapital-investors-2020.s3.eu-west-2.amazonaws.com/media/2022/04/DF-Capital-Pillar-III_Dec-2021-Final.pdf"
P3_2020_URL = "https://wp-dfcapital-investors-2020.s3.eu-west-2.amazonaws.com/media/2021/04/21065603/Distribution-Finance-Capital-Holdings-plc-Pillar-3-31-December-2020.pdf"

ENTITY_NOTE = (
    "ENTITY NOTE: DF Capital Bank Limited (FRN 848291, company 10198535) is the PRA-regulated bank "
    "entity, a wholly-owned subsidiary of the AIM-listed Distribution Finance Capital Holdings plc "
    "(company 11911574, 'the Group'). The Bank's own Companies House filings are fully scanned "
    "(no text layer). Both the Annual Report and the Pillar 3 disclosure are published ONLY at the "
    "Group-consolidated level - the Pillar 3 document itself states 'there are no differences between "
    "the basis of consolidation of the Group for accounting and regulatory purposes,' confirming this "
    "is not a basis mismatch. From FY2021-FY2023 the Group comprised only DFCH plc and DF Capital Bank "
    "Limited; two further lending subsidiaries (DF Capital Financial Solutions Limited, DF Capital "
    "Retail Finance Limited) were added by FY2025 per the Annual Report's own country-by-country note. "
    "The FY2021 Pillar 3 document uniquely also discloses a Bank-solo column alongside Group - the "
    "Group column is used throughout for consistency with every later year, which only shows Group. "
    "NSFR was disclosed FY2021-FY2023 but stops appearing in the FY2024 and FY2025 Pillar 3 documents "
    "entirely (checked directly, not assumed).\n"
    "REASON ESTABLISHED 2026-09-15 (cross-bank SDDT pass), replacing the earlier 'plausibly linked' / "
    "'consistent with' wording, which was an inference rather than evidence. The FY2024 and FY2025 "
    "NSFR (and MREL) gaps are an EVIDENCED STRUCTURAL REDUCTION IN DISCLOSURE SCOPE, stated by the Group "
    "itself in the documents concerned. DF Capital is unusual among the SDDTs in this project in that it "
    "keeps publishing a Pillar 3 document - it just publishes a shorter one - so the gap is a narrowed "
    "template, not a missing document.\n"
    "Evidence 1 - the Group's own words, identically in both editions, section 1.3: 'The Group has opted "
    "into the Small Domestic Deposit Takers ('SDDT') regime at both Consolidated and Bank levels. Having "
    "received PRA approval, disclosures are prepared in accordance with the regime's reduced disclosure "
    f"requirements as prescribed by Article 433b.' - Pillar 3 Disclosures at 31 December 2024, p.3 "
    f"({P3_2024_URL}) and Pillar 3 Disclosures 2025, p.3 ({P3_2025_URL}).\n"
    "Evidence 2 - Annual Report and Accounts 2025, p.37: 'The Group decided to use the Smaller Domestic "
    f"Deposit Taker (\"SDDT\") approach to prudential regulation.' - {AR2025_URL}\n"
    "Evidence 3 - the PRA's own firm-level register. Bank of England consolidated list of waivers and "
    "modifications granted to PRA-authorised firms (downloaded 2026-09-15) carries the row: FRN 848291, "
    "'DF Capital Bank Limited', 'Modification by Consent - PRA Rulebook - CRR Firms - Rule 3.1 of the SDDT "
    "Regime - General Application Part', sub rule 'Ru 3.1', waiver ref 'A00009982P.pdf', start date "
    "'07/03/2025', no end date - https://www.bankofengland.co.uk/-/media/boe/files/prudential-regulation/"
    "authorisations/waivers-and-modifications-of-rules/consolidated-waivers-pra-firms.csv\n"
    "DATE FIT: the modification took effect 7 March 2025 and the FY2024 Pillar 3 document was published in "
    "April 2025 - after it - which is why that FY2024 document is already the reduced Article 433b form and "
    "already states 'Having received PRA approval'. The exemption therefore explains the FY2024 and FY2025 "
    "narrowing and explains NOTHING about FY2020-FY2023, whose Pillar 3 documents are full-scope and whose "
    "own MREL absence has a separate cause (no MREL requirement disclosed for an institution of this size in "
    "any year). Do not read SDDT back onto FY2023 or earlier. No Simplified Retail Deposit Ratio value is "
    "disclosed, so nothing replaces the NSFR series here. Note also that the Annual Report's reference to "
    "moving to 'the new SDDT Capital Regime ... from 1st January 2027' (p.82) is the separate, later "
    "simplified CAPITAL regime, not the disclosure exemption that already applies.\n"
    "HISTORICAL FLOOR NOTE (HD-023, re-verified from primary sources, not assumed from HD-001's GLEIF-"
    "grouping guess): the Bank entity (company 10198535) was incorporated 25 May 2016 as 'Distribution "
    "Finance Capital Ltd', a non-bank specialist lender - it did NOT hold a banking licence and was not "
    "PRA-regulated until it 'was granted its banking licence in September 2020' (Annual Report and "
    "Accounts 2020, Note 1.1), at which point it renamed to 'DF Capital Bank Limited'. The Group entity "
    "(DFCH plc, company 11911574) was itself only incorporated 28 March 2019 - there is no Group-"
    "consolidated set of accounts before FY2019, and the FY2019 Annual Report has no accompanying "
    "Pillar 3 disclosure at all (the Group was not yet a regulated bank that year). FY2016-FY2019 are "
    "therefore self-skipped in full: FY2016-FY2018 predate the Group's very existence and predate any "
    "banking licence: FY2019 has a Group Annual Report but genuinely no Pillar 3 disclosure (confirmed "
    "by checking dfcapital-investors.com's own reports archive, which lists an Annual Report-only entry "
    "for 2019 with no paired Pillar 3 document, unlike every other year). FY2020 is therefore the real "
    "confirmed floor for the full 18/19-sheet shape (statements + Pillar 3) - not FY2016 as HD-023's "
    "ticket text and HD-001's GLEIF-grouping scale-out stated (that FY2016 figure is the Bank ENTITY's "
    "creation year, not the year it became a bank with regulatory disclosures - the same kind of "
    "GLEIF-grouping-vs-real-check gap already found for Chetwood Financial in this same ticket). FY2020 "
    "was the Bank's first year as an authorised institution (licensed only in the final ~4 months of "
    "the calendar year); its Pillar 3 document's Key Regulatory Metrics table (Table 1) is a CRD IV-era "
    "format that predates the later years' UK KM1 template, but already uses the CET1/Tier 1/Total "
    "Capital vocabulary (no Basel II-era terminology gap to flag - CET1 as a concept has existed under "
    "Basel III/CRD IV since 2014, well before this Bank's 2020 floor)."
)

CASH_FLOW_SOURCES = (
    "Sources - Distribution Finance Capital Holdings plc's Consolidated Cash Flow Statement (Group "
    "basis, the Bank's own filed accounts are fully scanned - see ENTITY NOTE):\n"
    f"FY2025/FY2024: Annual Report and Accounts 2025, p.114-115 (Consolidated Cash Flow Statement) - {AR2025_URL}\n"
    f"FY2023/FY2022: Annual Report and Accounts 2023, p.114-115 (Consolidated Cash Flow Statement) - {AR2023_URL}\n"
    f"FY2021: Annual Report and Accounts 2021, p.106-107 (Consolidated Cash Flow Statement) - {AR2021_URL}\n"
    f"FY2020: Annual Report and Financial Statements 2020, p.94 (Consolidated Cash Flow Statement) - {AR2020_URL}\n"
    "Each year's own originally-published figures are used; the closing balance of each year ties "
    "exactly to the opening balance of the next, no restatements found across any vintage (including "
    "FY2020's own closing GBP21,233k, which ties to FY2021's own opening balance). FY2022's "
    "own printed operating-activities total (-GBP3,408k) is GBP8k off its own component lines' sum "
    "(-GBP3,416k) - an immaterial rounding artifact in the source document itself, kept as printed "
    "rather than force-corrected; every other year's total ties to the penny, hand-traced across every "
    "year boundary FY2020-FY2025.\n"
    + ENTITY_NOTE
)


def p3_sources(page):
    return (
        f"Sources - Distribution Finance Capital Holdings plc Pillar 3 Disclosures (Consolidated "
        f"Group basis), Key Metrics (UK KM1) table, p.{page}:\n"
        f"FY2025: DF Capital Pillar III 2025 - {P3_2025_URL}\n"
        f"FY2024: DF Capital Pillar 3 Disclosures at December 2024 - {P3_2024_URL}\n"
        f"FY2023/FY2022: DF Capital Pillar III 2024 (FY2023 with Dec-22 comparative) - {P3_2023_URL}\n"
        f"FY2021: DF Capital Pillar III Dec 2021, Table 1 (Group column used, Bank-solo column also "
        f"disclosed that year only, not used - see ENTITY NOTE) - {P3_2021_URL}\n"
        f"FY2020: DF Capital Pillar 3 Disclosures at 31 December 2020, Table 1 'Key Regulatory "
        f"Metrics', p.16 (CRD IV-era format, pre-dates the later years' UK KM1 template - Group "
        f"column used, Bank-solo column also disclosed that year only, not used) - {P3_2020_URL}\n"
        + ENTITY_NOTE
    )


bw = BankWorkbook(bank_name="DF Capital Bank Limited", years=YEARS, year_label=YEAR_LABEL, header_color="D80034")

STATEMENTS_SOURCES = (
    "Sources - Distribution Finance Capital Holdings plc's Consolidated Financial Statements (Group basis, "
    "the Bank's own filed accounts are fully scanned - see ENTITY NOTE):\n"
    f"FY2025/FY2024: Annual Report and Accounts 2025, p.111-114 (Consolidated Statement of Comprehensive "
    f"Income / Financial Position / Changes in Equity) - {AR2025_URL}\n"
    f"FY2023/FY2022: Annual Report and Accounts 2023, p.111-114 (same statements) - {AR2023_URL}\n"
    f"FY2021: Annual Report and Accounts 2021, p.103-105 (same statements) - {AR2021_URL}\n"
    f"FY2020: Annual Report and Financial Statements 2020, p.91-93 (Consolidated Statement of "
    f"Comprehensive Income / Financial Position / Changes in Equity) - {AR2020_URL}\n"
    "Each year's own originally-published figures used; the equity roll-forward ties exactly at every "
    "boundary (each year's closing Total equity ties to both the next year's own opening balance and that "
    "year's own Balance Sheet Total equity, including FY2020's own closing GBP50,889k tying to FY2021's own "
    "opening balance) - no plug rows needed anywhere in this series.\n"
    f"INVESTMENT SECURITIES COMPOSITION: the Investment/debt securities line is 100% one bucket in every year "
    f"shown, but which bucket changes over time (confirmed against each year's own note, no sub-row split is "
    f"possible since there is nothing to reconcile against within a year): FY2020 (GBP66,601k) and FY2021 "
    f"(GBP108,867k) are 100% FVOCI debt securities split between Treasury bills (GBP49,011k/GBP53,085k) and UK "
    f"government gilts (GBP17,590k/GBP55,782k) - both UK sovereign issuer, just different instruments - Annual "
    f"Report and Accounts 2021, Note 20 'Debt securities', p.139 - {AR2021_URL}. FY2022 (GBP22,964k) and FY2023 "
    f"(GBP14,839k) are 100% FVOCI UK government gilts (Treasury bills line is GBPnil both years) - Annual Report "
    f"and Accounts 2023, Note 21 'Debt securities', p.149 - {AR2023_URL}. FY2024 (GBP769k) and FY2025 (GBP5,722k) "
    f"are 100% a Euro liquidity money market fund carried at amortised cost/not measured at fair value (the FVOCI "
    f"gilts/T-bills book was fully sold down during FY2024) - Annual Report and Accounts 2025, Note 20 "
    f"'Investment Securities', p.149 - {AR2025_URL}.\n"
    "PRESENTATION NOTE: FY2021-FY2022 label the investment line 'Debt securities'; FY2024-FY2025 relabel it "
    "'Investment securities' (same line, a money market fund holding was added) - shown on one row. FY2020- "
    "FY2021's cash line is labelled 'Cash and cash equivalents' vs later years' 'Cash and balances at central "
    "banks' - same line, relabelled. FY2020-FY2021 don't disclose separate Loans and advances to banks, "
    "Current/Deferred taxation asset, Derivatives, Amounts due to banks, Fair value adjustments on hedged "
    "liabilities or Subordinated liabilities lines (business was smaller and pre-dated some of these "
    "balances/hedge relationships - FY2020 specifically pre-dates any derivative/hedge activity entirely) - "
    "left blank rather than assumed zero. Share premium was cancelled during FY2023 (transferred to retained "
    "earnings) and Treasury shares only introduced FY2025 (share buyback) - both shown as blank in years "
    "they don't apply. FY2020's own P&L splits out a distinct 'Exceptional items' line (GBP0k in FY2020, "
    "material only in the FY2019 comparative which is out of scope - see ENTITY NOTE) not carried as its "
    "own row since it nets to zero for every year actually included here.\n"
    + ENTITY_NOTE
)

bw.add_balance_sheet_sheet(
    title="DF Capital Bank Limited — Consolidated Balance Sheet",
    subtitle="Distribution Finance Capital Holdings plc Group basis, £'000. See source note at bottom.",
    rows=[
        ("SECTION", "Assets", {}),
        ("DATA", "Cash and balances at central banks",
         {"FY2025": 131676, "FY2024": 110030, "FY2023": 89552, "FY2022": 107353, "FY2021": 29597, "FY2020": 21233}),
        ("DATA", "Loans and advances to banks",
         {"FY2025": 5894, "FY2024": 3771, "FY2023": 3475, "FY2022": 3848}),
        ("DATA", "Investment/debt securities (UK govt gilts/T-bills, FVOCI, FY2020-FY2023; money market "
                 "fund, amortised cost, FY2024-FY2025)",
         {"FY2025": 5722, "FY2024": 769, "FY2023": 14839, "FY2022": 22964, "FY2021": 108867, "FY2020": 66601}),
        ("DATA", "Derivatives held for risk management (asset)",
         {"FY2025": 411, "FY2024": 295, "FY2023": 537, "FY2022": 57}),
        ("DATA", "Loans and advances to customers",
         {"FY2025": 839526, "FY2024": 660772, "FY2023": 568044, "FY2022": 435883, "FY2021": 247205, "FY2020": 111337}),
        ("DATA", "Trade and other receivables",
         {"FY2025": 7734, "FY2024": 4678, "FY2023": 5335, "FY2022": 1524, "FY2021": 1133, "FY2020": 1154}),
        ("DATA", "Current taxation asset",
         {"FY2025": 40, "FY2023": 55, "FY2022": 55}),
        ("DATA", "Deferred taxation asset",
         {"FY2025": 1912, "FY2024": 3980, "FY2023": 7111, "FY2022": 8457}),
        ("DATA", "Property, plant and equipment",
         {"FY2025": 3797, "FY2024": 1093, "FY2023": 1145, "FY2022": 1045, "FY2021": 99, "FY2020": 139}),
        ("DATA", "Right-of-use assets",
         {"FY2025": 2355, "FY2024": 202, "FY2023": 1227, "FY2022": 433, "FY2021": 641, "FY2020": 64}),
        ("DATA", "Intangible assets",
         {"FY2025": 745, "FY2024": 950, "FY2023": 618, "FY2022": 877, "FY2021": 1066, "FY2020": 794}),
        ("TOTAL", "Total assets",
         {"FY2025": 999812, "FY2024": 786540, "FY2023": 691938, "FY2022": 582496, "FY2021": 388608, "FY2020": 201322}),

        ("SECTION", "Liabilities", {}),
        ("DATA", "Customer deposits",
         {"FY2025": 840565, "FY2024": 649665, "FY2023": 574622, "FY2022": 479736, "FY2021": 296856, "FY2020": 145982}),
        ("DATA", "Amounts due to banks", {"FY2024": 180}),
        ("DATA", "Derivatives held for risk management (liability)",
         {"FY2025": 819, "FY2024": 6, "FY2023": 565, "FY2022": 42}),
        ("DATA", "Fair value adjustments on hedged liabilities",
         {"FY2025": 375, "FY2024": 136, "FY2023": 424, "FY2022": -84}),
        ("DATA", "Financial liabilities",
         {"FY2025": 2444, "FY2024": 90, "FY2023": 1255, "FY2022": 445, "FY2021": 554, "FY2020": 107}),
        ("DATA", "Trade and other payables",
         {"FY2025": 12822, "FY2024": 9335, "FY2023": 4297, "FY2022": 6041, "FY2021": 5067, "FY2020": 4261}),
        ("DATA", "Provisions",
         {"FY2025": 255, "FY2024": 285, "FY2023": 67, "FY2022": 77, "FY2021": 73, "FY2020": 83}),
        ("DATA", "Current taxation liability",
         {"FY2024": 1259, "FY2023": 73}),
        ("DATA", "Subordinated liabilities",
         {"FY2025": 15302, "FY2024": 10230, "FY2023": 10221}),
        ("TOTAL", "Total liabilities",
         {"FY2025": 872582, "FY2024": 671186, "FY2023": 591524, "FY2022": 486257, "FY2021": 302550, "FY2020": 150433}),

        ("SECTION", "Equity", {}),
        ("DATA", "Issued share capital",
         {"FY2025": 1793, "FY2024": 1793, "FY2023": 1793, "FY2022": 1793, "FY2021": 1793, "FY2020": 1066}),
        ("DATA", "Share premium", {"FY2022": 39273}),
        ("DATA", "Merger relief",
         {"FY2025": 94911, "FY2024": 94911, "FY2023": 94911, "FY2022": 94911, "FY2021": 94911, "FY2020": 94911}),
        ("DATA", "Merger reserve",
         {"FY2025": -20609, "FY2024": -20609, "FY2023": -20609, "FY2022": -20609, "FY2021": -20609, "FY2020": -20609}),
        ("DATA", "Own shares",
         {"FY2025": -548, "FY2024": -440, "FY2023": -401, "FY2022": -364, "FY2021": -364, "FY2020": -364}),
        ("DATA", "Treasury shares", {"FY2025": -4755}),
        ("DATA", "Retained earnings/(loss)",
         {"FY2025": 56438, "FY2024": 39699, "FY2023": 24720, "FY2022": -18765, "FY2021": -28946, "FY2020": -24115}),
        ("TOTAL", "Total equity",
         {"FY2025": 127230, "FY2024": 115354, "FY2023": 100414, "FY2022": 96239, "FY2021": 86058, "FY2020": 50889}),
        ("TOTAL", "Total equity and liabilities",
         {"FY2025": 999812, "FY2024": 786540, "FY2023": 691938, "FY2022": 582496, "FY2021": 388608, "FY2020": 201322}),
    ],
    sources_text=STATEMENTS_SOURCES,
    first_col_width=68,
    source_height=340,
    unit_suffix=" (£'000)",
)

bw.add_income_statement_sheet(
    title="DF Capital Bank Limited — Consolidated Income Statement",
    subtitle="Distribution Finance Capital Holdings plc Group basis, £'000. See source note at bottom.",
    rows=[
        ("SECTION", "Income", {}),
        ("DATA", "Interest and similar income",
         {"FY2025": 90698, "FY2024": 76820, "FY2023": 59970, "FY2022": 25407, "FY2021": 13259, "FY2020": 11233}),
        ("DATA", "Interest and similar expenses",
         {"FY2025": -34897, "FY2024": -31208, "FY2023": -22336, "FY2022": -6411, "FY2021": -2338, "FY2020": -9174}),
        ("TOTAL", "Net interest income",
         {"FY2025": 55801, "FY2024": 45612, "FY2023": 37634, "FY2022": 18996, "FY2021": 10921, "FY2020": 2059}),
        ("DATA", "Fee income",
         {"FY2025": 1684, "FY2024": 1237, "FY2023": 1393, "FY2022": 1348, "FY2021": 466, "FY2020": 168}),
        ("DATA", "Fee expenses",
         {"FY2025": -1608, "FY2024": -1626, "FY2023": -719}),
        ("DATA", "Net losses on disposal of financial assets at FVOCI", {"FY2022": -17, "FY2020": 15}),
        ("DATA", "Net (losses)/gains from derivatives and other financial instruments at FVTPL",
         {"FY2025": -773, "FY2024": 372, "FY2023": -303, "FY2022": 99, "FY2021": -3}),
        ("DATA", "Other operating income",
         {"FY2025": 28, "FY2024": 2, "FY2023": 9, "FY2022": 5, "FY2020": 95}),
        ("DATA", "Other operating (expense)/income", {"FY2021": -81}),
        ("DATA", "Foreign currency gain/(loss)", {"FY2025": 907, "FY2024": -107}),
        ("TOTAL", "Total operating income",
         {"FY2025": 56039, "FY2024": 45490, "FY2023": 38014, "FY2022": 20431, "FY2021": 11303, "FY2020": 2337}),

        ("SECTION", "Expenses", {}),
        ("DATA", "Staff costs",
         {"FY2025": -20684, "FY2024": -16044, "FY2023": -13431, "FY2022": -10848, "FY2021": -9121, "FY2020": -9805}),
        ("DATA", "Other operating expenses",
         {"FY2025": -11497, "FY2024": -10563, "FY2023": -8412, "FY2022": -5983, "FY2021": -5386, "FY2020": -5182}),
        ("DATA", "Net impairment (loss)/gain on financial assets",
         {"FY2025": -4267, "FY2024": 241, "FY2023": -11598, "FY2022": -2296, "FY2021": -556, "FY2020": -1294}),
        ("DATA", "Other provisions", {"FY2025": 50, "FY2024": -50, "FY2021": 25, "FY2020": 417}),
        ("DATA", "Other losses", {"FY2021": 0, "FY2020": -76}),
        ("TOTAL", "Total operating profit/(loss)",
         {"FY2025": 19641, "FY2024": 19074, "FY2023": 4573, "FY2022": 1304, "FY2021": -3735, "FY2020": -13603}),
        ("TOTAL", "Profit/(loss) before taxation",
         {"FY2025": 19641, "FY2024": 19074, "FY2023": 4573, "FY2022": 1304, "FY2021": -3735, "FY2020": -13603}),
        ("DATA", "Taxation (charge)/credit",
         {"FY2025": -4482, "FY2024": -5053, "FY2023": -1418, "FY2022": 8457, "FY2021": 59, "FY2020": 0}),
        ("TOTAL", "Profit/(loss) after taxation",
         {"FY2025": 15159, "FY2024": 14021, "FY2023": 3155, "FY2022": 9761, "FY2021": -3676, "FY2020": -13603}),

        ("SECTION", "Other comprehensive income", {}),
        ("DATA", "FVOCI debt securities: amounts transferred to the income statement",
         {"FY2024": 75, "FY2022": 17, "FY2021": 3}),
        ("DATA", "FVOCI debt securities: fair value movements",
         {"FY2023": 183, "FY2022": -96, "FY2021": -165, "FY2020": -22}),
        ("TOTAL", "Total other comprehensive income/(loss) for the year, net of tax",
         {"FY2025": 0, "FY2024": 75, "FY2023": 183, "FY2022": -79, "FY2021": -162, "FY2020": -22}),
        ("TOTAL", "Total comprehensive income/(loss) for the year",
         {"FY2025": 15159, "FY2024": 14096, "FY2023": 3338, "FY2022": 9682, "FY2021": -3838, "FY2020": -13625}),
    ],
    sources_text=STATEMENTS_SOURCES,
    first_col_width=78,
    source_height=340,
    unit_suffix=" (£'000)",
)

EQUITY_HEADERS = [
    "Issued share capital", "Share premium", "Merger relief", "Merger reserve",
    "Own shares", "Treasury shares", "Retained earnings/(loss)", "Total equity",
]
bw.add_equity_changes_sheet(
    title="DF Capital Bank Limited — Consolidated Statement of Changes in Equity",
    subtitle="Distribution Finance Capital Holdings plc Group basis, £'000. See source note at bottom.",
    headers=EQUITY_HEADERS,
    rows=[
        ("TOTAL", "At 31 December 2019 (FY2020 opening)",
         (1066, None, 94911, -20609, None, None, -10812, 64556)),
        ("DATA", "Loss after taxation (FY2020)", (None, None, None, None, None, None, -13603, -13603)),
        ("DATA", "Other comprehensive loss (FY2020)", (None, None, None, None, None, None, -22, -22)),
        ("TOTAL", "Total comprehensive loss for the year (FY2020)",
         (None, None, None, None, None, None, -13625, -13625)),
        ("DATA", "Share-based payments (FY2020)", (None, None, None, None, None, None, 322, 322)),
        ("DATA", "Employee Benefit Trust loan (FY2020)", (None, None, None, None, -364, None, None, -364)),
        ("TOTAL", "At 31 December 2020 (FY2021 opening)",
         (1066, None, 94911, -20609, -364, None, -24115, 50889)),
        ("DATA", "Loss after taxation (FY2021)", (None, None, None, None, None, None, -3676, -3676)),
        ("DATA", "Other comprehensive loss (FY2021)", (None, None, None, None, None, None, -162, -162)),
        ("TOTAL", "Total comprehensive loss for the year (FY2021)",
         (None, None, None, None, None, None, -3838, -3838)),
        ("DATA", "Share-based payments (FY2021)", (None, None, None, None, None, None, 362, 362)),
        ("DATA", "Issue of new shares (FY2021)", (727, 39273, None, None, None, None, -1355, 38645)),
        ("TOTAL", "At 31 December 2021",
         (1793, 39273, 94911, -20609, -364, None, -28946, 86058)),

        ("DATA", "Profit after taxation (FY2022)", (None, None, None, None, None, None, 9761, 9761)),
        ("DATA", "Other comprehensive loss (FY2022)", (None, None, None, None, None, None, -79, -79)),
        ("TOTAL", "Total comprehensive income for the year (FY2022)",
         (None, None, None, None, None, None, 9682, 9682)),
        ("DATA", "Share-based payments (FY2022)", (None, None, None, None, None, None, 499, 499)),
        ("TOTAL", "At 31 December 2022",
         (1793, 39273, 94911, -20609, -364, None, -18765, 96239)),

        ("DATA", "Profit after taxation (FY2023)", (None, None, None, None, None, None, 3155, 3155)),
        ("DATA", "Other comprehensive income (FY2023)", (None, None, None, None, None, None, 183, 183)),
        ("TOTAL", "Total comprehensive income for the year (FY2023)",
         (None, None, None, None, None, None, 3338, 3338)),
        ("DATA", "Share-based payments (FY2023)", (None, None, None, None, None, None, 905, 905)),
        ("DATA", "Employee Benefit Trust (FY2023)", (None, None, None, None, -37, None, -31, -68)),
        ("DATA", "Share premium account cancellation (FY2023)", (None, -39273, None, None, None, None, 39273, 0)),
        ("TOTAL", "At 31 December 2023",
         (1793, 0, 94911, -20609, -401, None, 24720, 100414)),

        ("DATA", "Profit after taxation (FY2024)", (None, None, None, None, None, None, 14021, 14021)),
        ("DATA", "Other comprehensive income (FY2024)", (None, None, None, None, None, None, 75, 75)),
        ("TOTAL", "Total comprehensive income for the year (FY2024)",
         (None, None, None, None, None, None, 14096, 14096)),
        ("DATA", "Share-based payments (FY2024)", (None, None, None, None, None, None, 985, 985)),
        ("DATA", "Employee Benefit Trust (FY2024)", (None, None, None, None, -39, None, -102, -141)),
        ("TOTAL", "At 31 December 2024",
         (1793, 0, 94911, -20609, -440, None, 39699, 115354)),

        ("DATA", "Profit after taxation (FY2025)", (None, None, None, None, None, None, 15159, 15159)),
        ("DATA", "Other comprehensive income (FY2025)", (None, None, None, None, None, None, 0, 0)),
        ("TOTAL", "Total comprehensive income for the year (FY2025)",
         (None, None, None, None, None, None, 15159, 15159)),
        ("DATA", "Share-based payments (FY2025)", (None, None, None, None, None, None, 1254, 1254)),
        ("DATA", "Employee Benefit Trust (FY2025)", (None, None, None, None, -108, None, -84, -192)),
        ("DATA", "Share Buyback (FY2025)", (None, None, None, None, None, -4877, None, -4877)),
        ("DATA", "Settlement of share options (FY2025)", (None, None, None, None, None, 122, -6, 116)),
        ("DATA", "Deferred tax asset on share-based payments (FY2025)",
         (None, None, None, None, None, None, 416, 416)),
        ("TOTAL", "At 31 December 2025",
         (1793, 0, 94911, -20609, -548, -4755, 56438, 127230)),
    ],
    sources_text=STATEMENTS_SOURCES,
    first_col_width=64,
    source_height=340,
)

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Profit/(loss) before taxation",
     {"FY2025": 19641, "FY2024": 19074, "FY2023": 4573, "FY2022": 1304, "FY2021": -3735, "FY2020": -13603}),
    ("DATA", "Adjustments for non-cash items and other adjustments included in the income statement",
     {"FY2025": 7794, "FY2024": 3822, "FY2023": 13000, "FY2022": 4664, "FY2021": 1446, "FY2020": 2059}),
    ("DATA", "Increase/(decrease) in operating assets",
     {"FY2025": -186354, "FY2024": -92390, "FY2023": -149456, "FY2022": -193189, "FY2021": -136244, "FY2020": 96764}),
    ("DATA", "Increase/(decrease) in operating liabilities",
     {"FY2025": 195168, "FY2024": 79376, "FY2023": 94171, "FY2022": 183809, "FY2021": 151711, "FY2020": -19073}),
    ("DATA", "Taxation paid/(received)",
     {"FY2025": -3296, "FY2024": -681, "FY2023": 0, "FY2022": -4, "FY2021": 0, "FY2020": 0}),
    ("TOTAL", "Net cash generated from/(used in) operating activities",
     {"FY2025": 32953, "FY2024": 9201, "FY2023": -37712, "FY2022": -3408, "FY2021": 13178, "FY2020": 66147}),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Purchase of investment/debt securities",
     {"FY2025": -498, "FY2024": -9918, "FY2023": -14554, "FY2022": 0, "FY2021": -350980, "FY2020": -120721}),
    ("DATA", "Proceeds from sale and maturity of investment/debt securities",
     {"FY2025": 500, "FY2024": 25000, "FY2023": 23000, "FY2022": 85070, "FY2021": 307958, "FY2020": 62107}),
    ("DATA", "Dividends received on money market funds", {"FY2025": 57, "FY2024": 25}),
    ("DATA", "Interest received on investment/debt securities",
     {"FY2025": 2, "FY2024": 75, "FY2023": 383, "FY2022": 746, "FY2021": 549}),
    ("DATA", "Purchase of own shares", {"FY2023": -67}),
    ("DATA", "Purchase of property, plant and equipment",
     {"FY2025": -3557, "FY2024": -397, "FY2023": -418, "FY2022": -1041, "FY2021": -253, "FY2020": -32}),
    ("DATA", "Cash received on disposal of property, plant and equipment", {"FY2025": 34}),
    ("DATA", "Purchase of right of use assets", {"FY2025": -81}),
    ("DATA", "Purchase of intangible assets",
     {"FY2025": -80, "FY2024": -623, "FY2023": -117, "FY2022": -193, "FY2021": -586, "FY2020": -226}),
    ("TOTAL", "Net cash (used in)/generated from investing activities",
     {"FY2025": -3623, "FY2024": 14162, "FY2023": 8227, "FY2022": 84582, "FY2021": -43312, "FY2020": -58872}),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Issue of new shares", {"FY2021": 38645}),
    ("DATA", "Repayment of lease liabilities",
     {"FY2025": -108, "FY2024": -252, "FY2023": -227, "FY2022": -141, "FY2021": -147, "FY2020": -164}),
    ("DATA", "Issuance of subordinated liabilities", {"FY2025": 5000, "FY2023": 10000}),
    ("DATA", "Acquisition of subordinated liabilities", {"FY2023": -51}),
    ("DATA", "Coupon paid on subordinated liabilities", {"FY2025": -1269, "FY2024": -1273}),
    ("DATA", "Purchase of own shares", {"FY2025": -192, "FY2024": -142}),
    ("DATA", "Purchase of treasury shares", {"FY2025": -4877}),
    ("DATA", "Receipt of cash from settlement of share options", {"FY2025": 116}),
    ("TOTAL", "Net cash (used in)/generated from financing activities",
     {"FY2025": -1330, "FY2024": -1667, "FY2023": 9722, "FY2022": -141, "FY2021": 38498, "FY2020": -164}),
    ("TOTAL", "Net increase/(decrease) in cash and cash equivalents",
     {"FY2025": 28000, "FY2024": 21696, "FY2023": -19763, "FY2022": 81033, "FY2021": 8364, "FY2020": 7111}),
    ("DATA", "Cash and cash equivalents at start of the period",
     {"FY2025": 112563, "FY2024": 90867, "FY2023": 110630, "FY2022": 29597, "FY2021": 21233, "FY2020": 14122}),
    ("TOTAL", "Cash and cash equivalents at end of the period",
     {"FY2025": 140563, "FY2024": 112563, "FY2023": 90867, "FY2022": 110630, "FY2021": 29597, "FY2020": 21233}),
]

bw.add_cash_flow_sheet(
    title="DF Capital Bank Limited — Consolidated Cash Flow Statement",
    subtitle="Distribution Finance Capital Holdings plc Group basis, £'000. See source note at bottom.",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=80,
    source_height=280,
    unit_suffix=" (£'000)",
)

bw.add_asset_quality_sheet(
    title="DF Capital Bank Limited — Asset Quality",
    subtitle="Loans and advances to customers, by IFRS 9 stage, £'000. Group basis. See source note at bottom.",
    rows=[
        ("SECTION", "Loans and advances to customers - composition", {}),
        ("DATA", "Loan book principal",
         {"FY2025": 845966, "FY2024": 665709, "FY2023": 580525, "FY2022": 439282}),
        ("DATA", "Accrued interest and fees",
         {"FY2025": 4141, "FY2024": 4067, "FY2023": 3602, "FY2022": 2002}),
        ("TOTAL", "Gross carrying amount",
         {"FY2025": 850107, "FY2024": 669776, "FY2023": 584127, "FY2022": 441284, "FY2021": 249454, "FY2020": 113259}),
        ("DATA", "less: impairment allowance",
         {"FY2025": -8501, "FY2024": -6577, "FY2023": -14596, "FY2022": -3720, "FY2021": -1718, "FY2020": -1288}),
        ("DATA", "less: effective interest rate adjustment",
         {"FY2025": -2080, "FY2024": -2427, "FY2023": -1487, "FY2022": -1681, "FY2021": -531, "FY2020": -634}),
        ("TOTAL", "Total loans and advances to customers",
         {"FY2025": 839526, "FY2024": 660772, "FY2023": 568044, "FY2022": 435883, "FY2021": 247205, "FY2020": 111337}),

        ("SECTION", "Gross carrying amount, by IFRS 9 stage", {}),
        ("DATA", "Stage 1",
         {"FY2025": 785729, "FY2024": 643513, "FY2023": 545952, "FY2022": 410756, "FY2021": 239327, "FY2020": 103823}),
        ("DATA", "Stage 2",
         {"FY2025": 54741, "FY2024": 18484, "FY2023": 21052, "FY2022": 13323, "FY2021": 9585, "FY2020": 8726}),
        ("DATA", "Stage 3",
         {"FY2025": 9637, "FY2024": 7779, "FY2023": 17123, "FY2022": 17205, "FY2021": 542, "FY2020": 710}),
        ("TOTAL", "Total gross carrying amount (by stage)",
         {"FY2025": 850107, "FY2024": 669776, "FY2023": 584127, "FY2022": 441284, "FY2021": 249454, "FY2020": 113259}),

        ("SECTION", "Loss allowance (ECL), by IFRS 9 stage", {}),
        ("DATA", "Stage 1",
         {"FY2025": -4368, "FY2024": -3692, "FY2023": -2522, "FY2022": -1943, "FY2021": -1142, "FY2020": -645}),
        ("DATA", "Stage 2",
         {"FY2025": -711, "FY2024": -166, "FY2023": -160, "FY2022": -84, "FY2021": -155, "FY2020": -49}),
        ("DATA", "Stage 3",
         {"FY2025": -3422, "FY2024": -2719, "FY2023": -11914, "FY2022": -1693, "FY2021": -421, "FY2020": -594}),
        ("TOTAL", "Total loss allowance (by stage)",
         {"FY2025": -8501, "FY2024": -6577, "FY2023": -14596, "FY2022": -3720, "FY2021": -1718, "FY2020": -1288}),

        ("SECTION", "Derived ratios", {}),
        ("DATA", "Stage 3 / gross carrying amount (NPL ratio)",
         {"FY2025": "1.13%", "FY2024": "1.16%", "FY2023": "2.93%", "FY2022": "3.90%", "FY2021": "0.22%", "FY2020": "0.63%"}),
        ("DATA", "Stage 3 coverage (Stage 3 loss allowance / Stage 3 gross)",
         {"FY2025": "35.51%", "FY2024": "34.95%", "FY2023": "69.58%", "FY2022": "9.84%", "FY2021": "77.68%", "FY2020": "83.66%"}),
        ("DATA", "Total loss allowance coverage (total allowance / total gross)",
         {"FY2025": "1.00%", "FY2024": "0.98%", "FY2023": "2.50%", "FY2022": "0.84%", "FY2021": "0.69%", "FY2020": "1.14%"}),
    ],
    sources_text=(
        "Sources - Distribution Finance Capital Holdings plc's own Notes to the Consolidated Financial "
        "Statements, 'Loans and advances to customers' note and its 'Analysis of gross/impairment losses on "
        "loans and advances to customers' stage-migration tables:\n"
        f"FY2025/FY2024: Annual Report and Accounts 2025, p.148-151 - {AR2025_URL}\n"
        f"FY2023/FY2022: Annual Report and Accounts 2023, p.148-151 - {AR2023_URL}\n"
        f"FY2021: Annual Report and Accounts 2021, p.136-139 - {AR2021_URL}\n"
        f"FY2020: Annual Report and Financial Statements 2020, p.118-121 (Note 20, 'Loans and advances "
        f"to customers') - {AR2020_URL}\n"
        "Each year's own originally-published figures used; every stage-split total ties exactly to the "
        "note's own Gross carrying amount and to the note's own disclosed 'Loss allowance coverage' "
        "percentages (used directly for the Derived ratios where disclosed, not independently recomputed, "
        "to avoid rounding drift; FY2020's Stage 3 coverage and Total coverage percentages are the note's "
        "own disclosed 'Loss allowance coverage' figures, its NPL ratio is computed from the note's own "
        "Stage 3/Total gross carrying amount since the note doesn't disclose that ratio directly). "
        "FY2020-FY2021's reports do not disclose a Loan book principal/Accrued interest split "
        "(pre-dates that level of note detail) - left blank rather than guessed.\n"
        + ENTITY_NOTE
    ),
    first_col_width=64,
    source_height=300,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, page, note=None):
    bw.add_metric_sheet(name, unit, rows_data, p3_sources(page), note=note, first_col_width=48, source_height=180)


CET1_CAPITAL = {"FY2025": 112443, "FY2024": 98780, "FY2023": 79269, "FY2022": 84579, "FY2021": 82690, "FY2020": 47792}
TOTAL_CAPITAL = {"FY2025": 127745, "FY2024": 109010, "FY2023": 89538, "FY2022": 84579, "FY2021": 82690, "FY2020": 47792}
TOTAL_RWA = {"FY2025": 623607, "FY2024": 457565, "FY2023": 347034, "FY2022": 381972, "FY2021": 216353, "FY2020": 95427}
CET1_RATIO = {"FY2025": "18.0%", "FY2024": "21.6%", "FY2023": "22.8%", "FY2022": "22.1%", "FY2021": "38.2%", "FY2020": "50.1%"}
TOTAL_CAPITAL_RATIO = {"FY2025": "20.5%", "FY2024": "23.8%", "FY2023": "25.8%", "FY2022": "22.1%", "FY2021": "38.2%", "FY2020": "50.1%"}
LEVERAGE_RATIO = {"FY2025": "12.8%", "FY2024": "14.5%", "FY2023": "13.0%", "FY2022": "17.6%", "FY2021": "21.2%", "FY2020": "23.6%"}
LCR = {"FY2025": "704.0%", "FY2024": "836.6%", "FY2023": "618%", "FY2022": "1029%", "FY2021": "5597%", "FY2020": "6820%"}
NSFR = {"FY2023": "148.2%", "FY2022": "163%", "FY2021": "214%", "FY2020": "253%"}

NO_AT1_NOTE = "No Additional Tier 1 or Tier 2 instruments disclosed any year - Tier 1/Total Capital equal CET1 Capital throughout."
NSFR_NOTE = (
    "NSFR was disclosed for FY2020-FY2023 but does not appear anywhere in the FY2024 or FY2025 Pillar "
    "3 documents (confirmed by direct search of both, not assumed). STRUCTURALLY EXEMPT, not undisclosed "
    "(established 2026-09-15): both of those documents state at p.3 that 'The Group has opted into the "
    "Small Domestic Deposit Takers ('SDDT') regime at both Consolidated and Bank levels. Having received "
    "PRA approval, disclosures are prepared in accordance with the regime's reduced disclosure requirements "
    "as prescribed by Article 433b.' The PRA's own register confirms the underlying instrument - Rule 3.1 "
    "SDDT modification by consent, ref A00009982P.pdf, effective 07/03/2025. NSFR is one of the items the "
    "reduced template drops; becoming an SDDT also replaces the full NSFR with a Simplified Retail Deposit "
    "Ratio, which this Group does not publish a value for. So FY2024/FY2025 NSFR is a regulatory absence, "
    "not a search miss. This says nothing about FY2020-FY2023, which are disclosed in full above."
)

metric("CET1 Capital", "£'000", [("Common Equity Tier 1 (CET1) capital", CET1_CAPITAL)], "4")
metric("CET1 Ratio", "%", [("CET1 ratio", CET1_RATIO)], "4")
metric("Tier 1 Capital", "£'000", [("Tier 1 capital", CET1_CAPITAL)], "4", note=NO_AT1_NOTE)
metric("Tier 1 Ratio", "%", [("Tier 1 ratio", CET1_RATIO)], "4", note=NO_AT1_NOTE)
metric("Total Capital", "£'000", [("Total capital", TOTAL_CAPITAL)], "4")
metric("Total Capital Ratio", "%", [("Total capital ratio", TOTAL_CAPITAL_RATIO)], "4")
metric("Total RWAs", "£'000", [("Total risk-weighted exposure amount", TOTAL_RWA)], "4")

bw.add_rwa_breakdown_sheet(
    title="DF Capital Bank Limited — RWA Breakdown",
    subtitle="Distribution Finance Capital Holdings plc Group basis, £'000 (UK OV1 template). FY2023 category split OCR-recovered from an image-rendered table (2026-09-12). See source note at bottom.",
    rows=[
        ("DATA", "Credit risk (excluding CCR)",
        {"FY2025": 533039, "FY2024": 388533, "FY2023": 323338, "FY2022": 369638, "FY2021": 211065, "FY2020": 90139}),
        ("DATA", "Counterparty credit risk (CCR) - of which standardised approach",
         {"FY2025": 2259, "FY2024": 1635, "FY2023": 1651, "FY2022": 662}),
        ("DATA", "Counterparty credit risk (CCR) - of which credit valuation adjustment (CVA)",
         {"FY2025": 1027, "FY2024": 2371, "FY2023": 751, "FY2022": 367}),
        ("TOTAL", "Counterparty credit risk (CCR), total",
         {"FY2025": 3286, "FY2024": 4006, "FY2023": 2402, "FY2022": 1029}),
        ("DATA", "Operational risk (Basic Indicator Approach)",
         {"FY2025": 87281, "FY2024": 65026, "FY2023": 21294, "FY2022": 11305, "FY2021": 5288, "FY2020": 5288}),
        ("TOTAL", "Total RWAs",
         {"FY2025": 623607, "FY2024": 457565, "FY2023": 347034, "FY2022": 381972, "FY2021": 216353, "FY2020": 95427}),
        ("DATA", "Securitisation exposures in the non-trading book (after the cap, deducted from CET1 - not part of Total RWAs)",
         {"FY2025": 10942, "FY2024": 10095, "FY2023": 11281, "FY2020": 0}),
    ],
    sources_text=(
        "Sources - Distribution Finance Capital Holdings plc Pillar 3 Disclosures, 'Overview of risk "
        "weighted exposure amounts' (UK OV1) table:\n"
        f"FY2025/FY2024: DF Capital Pillar III 2025, p.5 (FY2024 shown as the document's own comparative "
        f"column) - {P3_2025_URL}\n"
        f"FY2021: DF Capital Pillar III Dec 2021, Table 3, p.22 (pre-dates CCR/CVA and the securitisation "
        f"programme, which only began March 2023 per the FY2023 Pillar 3 document's own approach-to-RWAs "
        f"note) - {P3_2021_URL}\n"
        f"FY2020: DF Capital Pillar 3 Disclosures at 31 December 2020, Table 3 'Pillar 1 capital "
        f"requirement', p.20 (pre-dates CCR/CVA and securitisation entirely - the document's own s.10 "
        f"states 'At 31 December 2020 the Group had no exposure to securitisation structures', hence the "
        f"explicit GBP0k rather than blank) - {P3_2020_URL}\n"
        f"FY2022: DF Capital Pillar 3 Disclosures at 31 December 2022, p.22 (FY2022 OV1-style table) - {P3_2022_URL}; "
        "the FY2022 table discloses credit risk £369,638k and operational risk £11,305k, with CCR £1,029k "
        "(including standardised £662k and CVA £367k), all summing to total RWA £381,972k. "
        f"FY2023 (2026-09-12 re-verification): DF Capital Pillar III 2024, p.15 - {P3_2023_URL}. The OV1-style "
        "table is rendered as an image within the PDF (no text layer for this specific table, hence the earlier "
        "'not recoverable' claim - confirmed via OCR at 300dpi, p.15, section 3.4 'Approach to RWAs'): credit "
        "risk (excl. CCR) £323,338k [standardised approach, same figure], CCR £2,402k (of which standardised "
        "£1,651k, of which CVA £751k), operational risk £21,294k, securitisation exposures (after cap) £11,281k "
        "(n/a for own-funds deduction that year), total RWA £347,034k - ties exactly to the Total RWAs sheet.\n"
        + ENTITY_NOTE
    ),
    first_col_width=70,
    source_height=280,
    unit_suffix=" (£'000)",
)

metric("Leverage Ratio", "%", [("Leverage ratio excluding claims on central banks", LEVERAGE_RATIO)], "4")
metric("LCR", "%", [("Liquidity coverage ratio", LCR)], "4")
metric("NSFR", "%", [("Net Stable Funding Ratio", NSFR)], "4", note=NSFR_NOTE)

bw.add_not_disclosed_metric_sheets(
    ["MREL Ratio"], p3_sources("n/a"),
    per_note={"MREL Ratio": (
        "Not publicly disclosed in any year (FY2020-FY2025), and no document states an MREL exemption. "
        "The earlier gloss 'consistent with a small SDDT-regime institution' was removed 2026-09-15 as an "
        "unevidenced inference: the Group's SDDT opt-in is now separately evidenced (see ENTITY NOTE) but "
        "it is dated 07/03/2025 and so cannot account for the FY2020-FY2023 MREL blanks, and no source "
        "links SDDT status to the MREL absence in any year. Recorded simply as not disclosed."
    )},
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets",
         {"FY2025": 999812, "FY2024": 786540, "FY2023": 691938, "FY2022": 582496, "FY2021": 388608, "FY2020": 201322}),
        ("Loans and advances to customers",
         {"FY2025": 839526, "FY2024": 660772, "FY2023": 568044, "FY2022": 435883, "FY2021": 247205, "FY2020": 111337}),
        ("Customer deposits",
         {"FY2025": 840565, "FY2024": 649665, "FY2023": 574622, "FY2022": 479736, "FY2021": 296856, "FY2020": 145982}),
        ("Total equity",
         {"FY2025": 127230, "FY2024": 115354, "FY2023": 100414, "FY2022": 96239, "FY2021": 86058, "FY2020": 50889}),
    ],
    balance_sheet_unit="£'000",
    income_statement_totals=[
        ("Total operating income",
         {"FY2025": 56039, "FY2024": 45490, "FY2023": 38014, "FY2022": 20431, "FY2021": 11303, "FY2020": 2337}),
        ("Total operating expenses (staff + other operating expenses)",
         {"FY2025": -32181, "FY2024": -26607, "FY2023": -21843, "FY2022": -16831, "FY2021": -14507, "FY2020": -14987}),
        ("Profit/(loss) after taxation",
         {"FY2025": 15159, "FY2024": 14021, "FY2023": 3155, "FY2022": 9761, "FY2021": -3676, "FY2020": -13603}),
    ],
    income_statement_unit="£'000",
    equity_changes_totals=[
        ("Opening equity",
         {"FY2025": 115354, "FY2024": 100414, "FY2023": 96239, "FY2022": 86058, "FY2021": 50889, "FY2020": 64556}),
        ("Total comprehensive income/(loss) for the year",
         {"FY2025": 15159, "FY2024": 14096, "FY2023": 3338, "FY2022": 9682, "FY2021": -3838, "FY2020": -13625}),
        ("Other equity movements, net",
         {"FY2025": -3283, "FY2024": 844, "FY2023": 837, "FY2022": 499, "FY2021": 39007, "FY2020": -42}),
        ("Closing equity",
         {"FY2025": 127230, "FY2024": 115354, "FY2023": 100414, "FY2022": 96239, "FY2021": 86058, "FY2020": 50889}),
    ],
    equity_changes_unit="£'000",
    cash_flow_totals=[
        ("Net cash generated from/(used in) operating activities",
         {"FY2025": 32953, "FY2024": 9201, "FY2023": -37712, "FY2022": -3408, "FY2021": 13178, "FY2020": 66147}),
        ("Net cash (used in)/generated from investing activities",
         {"FY2025": -3623, "FY2024": 14162, "FY2023": 8227, "FY2022": 84582, "FY2021": -43312, "FY2020": -58872}),
        ("Net cash (used in)/generated from financing activities",
         {"FY2025": -1330, "FY2024": -1667, "FY2023": 9722, "FY2022": -141, "FY2021": 38498, "FY2020": -164}),
        ("Cash and cash equivalents at end of the period",
         {"FY2025": 140563, "FY2024": 112563, "FY2023": 90867, "FY2022": 110630, "FY2021": 29597, "FY2020": 21233}),
    ],
    cash_flow_unit="£'000",
    ratios=[
        ("CET1 Ratio", CET1_RATIO),
        ("Total Capital Ratio", TOTAL_CAPITAL_RATIO),
        ("Leverage Ratio", LEVERAGE_RATIO),
        ("LCR", LCR),
        ("NSFR", NSFR),
    ],
    note="Figures are Distribution Finance Capital Holdings plc Group-consolidated basis (the PRA-"
         "regulated Bank's own filed accounts are fully scanned with no text layer; the Group and "
         "regulatory consolidation bases are confirmed identical, so this is not a basis mismatch — "
         "see the Cash Flow Statement sheet's source note). Figures are duplicated from the detail "
         "sheets for at-a-glance trend viewing; see each sheet's own source citation for the "
         "underlying document/page. FY2020 is this workbook's confirmed floor (HD-023, re-verified "
         "against Companies House and the Bank's own disclosure archive) — the Bank only became a "
         "PRA-authorised deposit-taker in September 2020 and the Group entity itself was only "
         "incorporated March 2019, so no earlier year has both financial statements and a Pillar 3 "
         "disclosure; see the Cash Flow Statement sheet's ENTITY NOTE for the full chain of evidence.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/DF CAPITAL BANK FINANCIALS.xlsx")
