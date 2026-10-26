#!/usr/bin/env /usr/bin/python3
"""Which banks' Balance Sheet and Profit & Loss share a basis, and which do not.

A profitability ratio cancels its unit ONLY if both sides share it. The house
FX convention (project_fx_conversion_convention) converts STOCKS at the fiscal
year-end SPOT rate and FLOWS at that year's AVERAGE rate - so on a converted
workbook the denominator and the numerator are both labelled GBP but were
struck at DIFFERENT rates, and the ratio carries the spot/average spread.
Nothing on the page shows it and no check axis in CLAUDE.md can see it: the
figure is self-consistent on every one of them.

Relative bias is exactly spot/avg - 1, and it CHANGES SIGN year to year, so it
distorts the trend as well as the level:
    FY2021 -1.68%   FY2022 -2.14%   FY2023 +2.36%   FY2024 -2.09%   FY2025 +1.93%

THIS TABLE IS EXPLICIT, NOT INFERRED, and that is deliberate. Three detection
routes were tried and all three fail:
  * grepping for stock()/flow() on the row literal - FAILS. In most converted
    scripts the wrapper is applied by a comprehension over the WHOLE row list
    (Credit Suisse International, Goldman Sachs, UBA UK, Zenith, Persia) or by
    a per-key accessor (Union Bank of India UK), so the row literal looks raw.
    This produced a confidently wrong "clean" verdict for Credit Suisse
    International and Gulf International Bank UK.
  * the helper names - FAIL. They are stock/flow in some scripts, gbp_spot/
    gbp_avg in SMBC and Bank Saderat, bs_stock/bs_flow in Access Bank,
    stock2/flow2 in Zenith, _stock1/_flow1 in Union Bank of India UK.
  * the printed unit string - FAILS BOTH WAYS. It under-counts, because
    FirstBank UK, J.P. Morgan Securities, Bank Mandiri Europe and FCMB UK are
    contaminated while printing a plain unit; and FirstBank UK has no FX
    helper at all - its two rates are baked into literals and recorded only in
    prose, invisible to any code scan.

So each entry below was settled by reading that bank's build script. Keys are
the WORKBOOK KEY - the filename without " FINANCIALS.xlsx", which is also the
key published_returns.jsonl uses, so one bank has one identifier across this
work. (They were first written as each bank's display bank_name and 26 of the
29 then matched nothing: the display name is not an identifier.) Values:
    "mixed"        - every year's ratio is contaminated
    {"FY20xx", ..} - only these years are contaminated
    "cancels"      - both sides share a basis; the ratio is safe
A bank absent from this table whose statements print a converted unit will
RAISE at build time rather than quietly computing - see
BankWorkbook.add_profitability_sheet. Silence must not read as a clean bill of
health; that is the whole lesson above.

Audited 2026-10-26 against all 29 workbooks that involve a non-GBP currency.
"""

FX_RATIO_BASIS = {
    # ---- contaminated for every reported year -----------------------------
    "ACCESS BANK UK": "mixed",               # bs_stock/bs_flow, loop-applied
    "ARAB BANK EUROPE": "mixed",             # gbp_spot/gbp_avg
    "BANK MANDIRI EUROPE": "mixed",          # BS={k:stock(v)}, IS={k:flow(v)}
    "BANK SADERAT": "mixed",                 # gbp_m_spot/gbp_m_avg
    "BANK SEPAH INTERNATIONAL": "mixed",     # gbp_spot/gbp_avg
    "CREDIT SUISSE INTERNATIONAL": "mixed",  # comprehension-applied stock/flow
    "FCMB UK": "mixed",                      # stock/flow, bs_rows/pl_rows
    "FIDBANK UK": "mixed",                   # stock/flow, inline rows
    "GOLDMAN SACHS INTERNATIONAL BANK": "mixed",
    "GULF INTERNATIONAL BANK UK": "mixed",
    "JP MORGAN SECURITIES": "mixed",       # converted 2026-10-09; see below
    "PERSIA INTERNATIONAL BANK": "mixed",    # plus FY2015/16, see note
    "PUNJAB NATIONAL BANK INTERNATIONAL": "mixed",
    "SMBC": "mixed",                         # gbp_spot/gbp_avg
    "UBA UK": "mixed",
    "UNION BANK OF INDIA UK": "mixed",       # _stock1/_flow1 via bs_line/is_line

    # ---- contaminated only in part of the series --------------------------
    # FirstBank UK reports in $'000 and has NO FX helper: FY2019-FY2021 were
    # converted offline from the Bank's own GBP figures, balances at year-end
    # spot and flows at the average rate, and the two rates are recorded only
    # in the subtitles and CURRENCY_NOTE. FY2022-FY2025 are the Bank's own
    # native $ and cancel cleanly.
    "FIRSTBANK UK": {"FY2019", "FY2020", "FY2021"},
    # Zenith is native GBP for FY2009-FY2013 (NATIVE_GBP_YEARS), where stock2
    # and flow2 take the identical no-FX branch, and converted from FY2014.
    "ZENITH": {"FY2014", "FY2015", "FY2016", "FY2017", "FY2018", "FY2019",
               "FY2020", "FY2021", "FY2022", "FY2023", "FY2024", "FY2025"},

    # ---- same basis on both sides; the ratio is safe ----------------------
    # BPI Europe has no average-rate table at all, so its P&L flows are
    # converted at period-end spot like its balances. The ratio cancels - but
    # it cancels because of an approximation the script itself flags, not
    # because anyone designed the ratio. The P&L LEVELS carry that caveat.
    "BANK OF THE PHILIPPINE ISLANDS EUROPE": "cancels",
    "ICBC (LONDON) PLC": "cancels",          # raw $'000 both sides
    "ICBC STANDARD BANK PLC": "cancels",     # raw $m both sides
    "ICICI BANK UK": "cancels",              # raw USD'000 both sides
    "ITAU BBA INTERNATIONAL": "cancels",     # raw USD'000 both sides
    "JP MORGAN EUROPE": "cancels",           # £'000 both sides, bank's own restatement
    "KUWAIT FINANCE HOUSE": "cancels",       # units cancel - ENTITY DOES NOT, see below
    "MELLI BANK": "cancels",                 # raw EUR '000 both sides
    "NATIONAL BANK OF KUWAIT INTERNATIONAL": "cancels",  # each year own currency
    "NOMURA BANK INTERNATIONAL": "cancels",  # raw $'000 both sides
    "STANDARD CHARTERED BANK": "cancels",    # units cancel - ENTITY DOES NOT, see below
}

# Problems a UNIT test cannot see, found by the same audit. These are NOT
# fixable by choosing a different rate; the two sheets describe different
# things. A ratio struck across them divides one entity by another.
ENTITY_MISMATCH = {
    "KUWAIT FINANCE HOUSE": (
        "Balance Sheet is Bank/solo; Profit & Loss is Consolidated (Group) - "
        "the entity publishes no standalone Bank income statement, which the "
        "script states. A ratio divides GROUP profit by SOLO equity/assets."),
    "STANDARD CHARTERED BANK": (
        "Balance Sheet is the standalone Bank Company column; Profit & Loss is "
        "the Bank GROUP consolidated income statement, because the Company has "
        "no standalone P&L. A Company-level profit after tax IS disclosed in "
        "each year's balance-sheet note and is quoted in the script's prose, so "
        "a same-entity numerator exists in the sources but is not a P&L row."),
}

# Further findings from the 2026-10-26 audit, recorded so they are not
# rediscovered. None is a profitability-ratio question in itself.
OTHER_FINDINGS = {
    "PERSIA INTERNATIONAL BANK": (
        "FY2015 and FY2016 are MIXED CURRENCY, not merely mixed rate: "
        "YEAR_END_RATE has no key for those years so the Balance Sheet passes "
        "through as raw EUR '000, while AVG_RATE does carry them so the P&L IS "
        "converted to GBP. The ratio would be GBP over EUR. Separately, both "
        "sheets' column headers read '(GBP'000, conv. from EUR)' for those two "
        "years even on the Balance Sheet where the figures are raw EUR, and the "
        "P&L subtitle's claim that FY2015/FY2016 are 'EUR '000 shown' is false "
        "for that sheet. Those are labelling defects independent of any ratio."),
    "NATIONAL BANK OF KUWAIT INTERNATIONAL": (
        "Presentation currency changes mid-series - US$'000 for FY2021-FY2023, "
        "GBP'000 for FY2024-FY2025 - and unit_suffix is empty, so the printed "
        "column headers carry NO currency marker. Each year's ratio is sound; "
        "comparing ratio levels across the FY2023/FY2024 boundary is not, and "
        "nothing on the sheet warns the reader."),
    "BANK SEPAH INTERNATIONAL": (
        "Two total-assets rows: 'Total assets' (FY2021-FY2025 only) and 'Total "
        "assets (FY2026 presentation)'. A lookup on the plain label silently "
        "drops FY2026. Both are gbp_spot, so the basis verdict is unaffected."),
    "JP MORGAN SECURITIES": (
        "project_fx_conversion_convention records this bank as deliberately "
        "holding its Balance Sheet and P&L in US$'000 with only stock() "
        "defined. That is STALE: the script's own HISTORY block records the "
        "2026-10-09 conversion onto the corpus convention, and it now defines "
        "both stock() and flow(). Only the KM1 sheet remains unconverted."),
}


# A profitability ratio divides a PROFIT AND LOSS flow by a BALANCE SHEET
# stock. Where a year column's flows cover something other than twelve months,
# the quotient is still exact arithmetic on two figures the bank published -
# and it is NOT an annual return, and is not comparable with the columns
# either side of it. The user's decision (2026-10-26) is to PRINT it and state
# the period, rather than refuse it as a mixed FX basis is refused: nothing
# about the ratio is contaminated, only its interpretation, and annualising it
# would be this project's arithmetic on a period the bank never annualised.
#
# So NOTHING here feeds a calculation. Each entry is prose for the sheet note,
# which is why a disagreement inside a script is recorded as a disagreement
# rather than resolved into a number.
#
# Audited 2026-10-26 across the 30 build scripts that mention a month-length,
# a transition, a stub or an accounting-reference-date change; each citation
# below was checked against the script's own line. Eleven of those 30 turned
# out to have no affected column - ACCESS BANK UK, ALLICA, ARBUTHNOT LATHAM,
# THE BANK OF LONDON GROUP, CHETWOOD, CLEARBANK, CLOSE BROTHERS, PARAGON,
# STATE BANK OF INDIA UK, UNION BANK OF INDIA UK and UNITED NATIONAL - mostly
# because the irregular period sits BELOW the workbook's floor and was
# deliberately excluded from the year grid rather than squeezed into a column.
#
# The year label is NOT a detector for this, and that was measured: only
# ALDERMORE encodes the period length in year_label, so a scan of the labels
# finds 2 of the 20 affected bank-years. Same lesson as FX_RATIO_BASIS above.
NON_ANNUAL_PERIODS = {
    "ALDERMORE": {
        "FY2018": "an 18-month transition period, 1 January 2017 to 30 June "
                  "2018, after the Group changed its accounting reference "
                  "date; its flows are roughly 1.5x a normal year's",
        "FY2009": "a 9-month stub, 1 April 2009 to 31 December 2009",
    },
    "BANK OF CHINA UK": {
        "FY2008": "a 15-month period, 1 October 2007 to 31 December 2008, "
                  "during which the year-end moved to December",
    },
    "CLYDESDALE": {
        "FY2025": "an 18-month PRA-approved transition period, 1 October 2023 "
                  "to 31 March 2025, which moved the year-end from 30 "
                  "September to 31 March. There is no separate FY2024 column: "
                  "that period is entirely contained within this one",
    },
    "GB BANK": {
        "FY2024": "a shortened 9-month period ended 30 September 2024, after "
                  "the accounting period end changed. The start date is not "
                  "printed in the Bank's own accounts; the prior column ends "
                  "31 December 2023",
    },
    "GRIFFIN BANK": {
        "FY2023": "a 15-month period, 1 July 2022 to 30 September 2023 - the "
                  "Bank's first published period - reported as originally "
                  "stated and not annualised",
    },
    "HABIB BANK ZURICH": {
        "FY2016": "a 9-month first trading period, 1 April 2016 to 31 "
                  "December 2016, the Bank having begun operations on 1 April "
                  "2016 via a Part VII transfer of the UK branch",
    },
    "HANDELSBANKEN": {
        # Recorded as the script records it, both sides, because the script
        # disagrees with itself and a ratio note must not pick a side.
        "FY2018": "a stub period whose length the Bank's own documents state "
                  "three different ways: the report is titled 'for the 9 "
                  "month period ended 31 December 2018', the dates it gives "
                  "(11 April to 31 December 2018) span 8 months and 20 days, "
                  "and the Bank only actually traded for the FINAL MONTH, "
                  "following the 1 December 2018 transfer of trade and assets "
                  "from the UK branch. The balance sheet is a full "
                  "point-in-time snapshot at 31 December 2018. So this year's "
                  "return is UNDERSTATED, not overstated - roughly one month "
                  "of profit over a whole balance sheet",
    },
    "JULIAN HODGE BANK": {
        "FY2020": "an 11-month transition period ended 30 September 2020, the "
                  "year the fiscal year-end changed from 31 October to 30 "
                  "September",
    },
    "METHODIST CHAPEL AID": {
        "FY2025": "a 9-month period ended 30 September 2025, after the "
                  "accounting reference date changed from 31 December. The "
                  "start date is not printed; the prior column ends 31 "
                  "December 2024",
    },
    "METRO BANK": {
        "FY2010": "the Bank's first accounts, covering from the 18 September "
                  "2009 change of accounting reference date to 31 December "
                  "2010. The column is labelled '16m' and the script calls it "
                  "a 16-month period; the dates it gives span 15 months and "
                  "12 days, so the 16 is a round-up",
    },
    "MONZO": {
        "FY2024": "a 13-month period, 1 March 2023 to 31 March 2024, when "
                  "Monzo moved its year-end from 28 February to 31 March. It "
                  "is not directly run-rate comparable with the other "
                  "columns, and this year is ALSO where the reporting entity "
                  "changes from Monzo Bank Ltd to Monzo Bank Holding Group",
    },
    "NATIONAL BANK OF EGYPT UK": {
        "FY2021": "an 18-month period, 1 July 2020 to 31 December 2021, after "
                  "the entity's accounting reference date moved from 30 June "
                  "to 31 December. Reported exactly as originally presented, "
                  "neither annualised nor restated - the largest period "
                  "distortion in this corpus at 1.5x a normal year",
    },
    "RECOGNISE BANK": {
        "FY2018": "a 14-month first statutory period, from incorporation on 6 "
                  "February 2017 to 31 March 2018",
    },
    "STARLING": {
        "FY2021": "a 16-month period, 1 December 2019 to 31 March 2021 - "
                  "Starling's first period reporting to a 31 March year-end. "
                  "There is no FY2020 column at all: the twelve months to 30 "
                  "November 2020 fall inside this period",
    },
    "STREAMBANK": {
        "FY2023": "a 15-month transition period, 1 January 2022 to 31 March "
                  "2023, the accounting period having been extended from 31 "
                  "December 2022. There is no separate FY2022 column",
    },
    "THIS BANK": {
        "FY2020": "a 16-month first statutory period, from incorporation on "
                  "19 December 2018 to 31 March 2020, the accounting "
                  "reference date having been extended",
    },
    "TRIODOS": {
        "FY2019": "presented as a full financial year to 31 December 2019, "
                  "and covering only EIGHT MONTHS of actual trading, 1 May "
                  "2019 to 31 December 2019: the entity was dormant until the "
                  "Part VII transfer of Triodos Bank N.V.'s UK branch on 1 "
                  "May 2019, and its own Annual Report 2019 states that 'the "
                  "figures presented represent eight months of trading'. Both "
                  "readings are recorded because the document supports both. "
                  "Either way the flows are short against a full balance "
                  "sheet, so this year's return is UNDERSTATED, not "
                  "overstated",
    },
    "UNION BANCAIRE PRIVEE UK": {
        "FY1998": "an 11-month period, 1 April 1997 to 28 February 1998, not "
                  "a calendar year. A SECOND period ended in calendar 1998 - "
                  "the 10 months ended 31 December 1998 - and is deliberately "
                  "given no column of its own, since two periods cannot share "
                  "one FY label; it is carried in the Balance Sheet sheet's "
                  "note",
    },
}

# KINGDOM BANK FY2004 is an 11-month period (1 February to 31 December 2004)
# and is deliberately NOT in the table above, because it cannot distort a
# ratio: the Bank's own Note 1(d) states "No profit and loss account has been
# prepared for the period ended 31 December 2004, as Kingdom Bank Limited did
# not commence trading until 1 January 2005", so that column holds a balance
# sheet and nothing else. There is no numerator to divide.
