import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

# HD-018: extended from FY2021-FY2025 back to FY2014-FY2025 (12 years) using
# BLME's own blme.com media-library filings (Wayback CDX confirmed all 16
# FY2014-FY2020 documents still resolve directly on blme.com - no Wayback
# fallback needed). Bank-solo ("BLME plc") basis throughout, matching the
# FY2021-2025 convention, EXCEPT: FY2014-2016's own Annual Reports only
# publish a CONSOLIDATED (Group) Income Statement - no separate Bank-only
# P&L line-item breakdown exists for those 3 years (Bank-solo profit is only
# derivable as a single total, via the Bank cash flow/equity statements) -
# flagged wherever it applies, not silently substituted.
YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021", "FY2020", "FY2019",
         "FY2018", "FY2017", "FY2016", "FY2015", "FY2014"]
YEAR_LABEL = {y: y for y in YEARS}

CH_URL = "https://find-and-update.company-information.service.gov.uk/company/05897786"
FS2025_URL = "https://www.blme.com/media/z0jd2sah/blme-plc-financial-statements-31-december-2025.pdf"
FS2024_URL = "https://www.blme.com/media/rneds5db/blme-plc-financial-statements-31-december-2024.pdf"
FS2023_URL = "https://www.blme.com/media/2j5fy4tv/blme-plc-financial-statements-31-december-2023.pdf"
FS2022_URL = "https://www.blme.com/media/2014/blme-plc-financial-statements-31-december-2022.pdf"
FS2021_URL = "https://www.blme.com/media/1964/blme-plc-fin-stats-31-december-2021-for-website.pdf"
FS2020_URL = "https://www.blme.com/media/1911/2020-financial-statements-blme-plc.pdf"
FS2019_URL = "https://www.blme.com/media/1852/blme-plc-financial-statements-31-december-2019.pdf"
FS2018_URL = "https://www.blme.com/media/1722/2018-financial-statements-blme-plc.pdf"
FS2017_URL = "https://www.blme.com/media/1634/2017-financial-statements-blme-plc.pdf"
FS2016_URL = "https://www.blme.com/media/1539/2016-financial-statements-blme-plc.pdf"
FS2015_URL = "https://www.blme.com/media/1498/blme-plc-financial-statements-31-december-2015.pdf"
FS2014_URL = "https://www.blme.com/media/1630/2014-financial-statements-blme-plc.pdf"
P32025_URL = "https://www.blme.com/media/jf2dbyrm/2025-pillar-iii-disclosure.pdf"
P32024_URL = "https://www.blme.com/media/mhantsoh/2024-pillar-iii-disclosure.pdf"
P32023_URL = "https://www.blme.com/media/fluobg0d/2023-pillar-iii-disclosure.pdf"
P32022_URL = "https://www.blme.com/media/2017/2022-pillar-iii-disclosure.pdf"
P32021_URL = "https://www.blme.com/media/1997/2021-pillar-iii-disclosure.pdf"
P32020_URL = "https://www.blme.com/media/1921/pillar-3-disclosure-2020.pdf"
P32019_URL = "https://www.blme.com/media/1858/2019-pillar-iii-disclosure.pdf"
P32018_URL = "https://www.blme.com/media/1728/2018-pillar-iii-disclosure.pdf"
P32017_URL = "https://www.blme.com/media/1649/2017-pillar-3-disclosure.pdf"
P32016_URL = "https://www.blme.com/media/1547/pillar-iii-2016-disclosures-blme-plc.pdf"
P32015_URL = "https://www.blme.com/media/1454/2015-pillar-iii-disclosures-blme-plc.pdf"
P32014_URL = "https://www.blme.com/media/1356/2014-pillar-iii-disclosures.pdf"

ENTITY_NOTE = (
    "ENTITY NOTE: Bank of London and The Middle East plc (FRN 464292, Companies House 05897786, matches "
    "Banks List 2608.xlsx exactly) is a UK-incorporated Sharia-compliant wholesale/private bank, majority-owned "
    "by Boubyan Bank (Kuwait). It publishes both wider 'BLME Holdings' group accounts and standalone 'BLME plc' "
    "(Bank-solo) accounts on its own site - this workbook uses the plc/solo figures throughout for both the cash "
    "flow statement and Pillar 3, matching the PRA-regulated entity. Terminology uses 'profit'/'financing' rather "
    "than 'interest'/'loans' (Sharia-compliant banking), consistent with ALRAYAN Bank elsewhere in this project.\n\n"
    "HD-018 EXTENSION CAVEATS (FY2014-FY2020, all verified against the actual PDFs, not assumed from the earlier "
    "domain scan alone):\n"
    "(1) FY2014-2016 Annual Reports publish only a CONSOLIDATED (Group) Income Statement - no separate Bank-only "
    "P&L breakdown exists for those years. This sheet's P&L for FY2014-2016 uses the Group figures (clearly "
    "labelled), while every other sheet (Balance Sheet, Cash Flow, Equity Changes, Asset Quality) uses the Bank-solo "
    "figures as normal - both are disclosed in the same reports. Bank-solo profit/(loss), for reference, was "
    "FY2014 +£498k, FY2015 -£7,101k, FY2016 -£21,458k (vs Group FY2014 +£974k, FY2015 -£6,850k, FY2016 -£21,383k).\n"
    "(2) FY2014-2015 Pillar III disclosures pre-date CRD IV's standardised Pillar 3 template - they disclose "
    "absolute capital resource amounts but NOT risk-weighted assets or any capital/leverage RATIO, and disclose no "
    "LCR/NSFR at all. FY2014's RWA and ratios are DERIVED (not directly disclosed) from the FY2014 Annual Report's "
    "own 'Pillar 1 capital requirements' table, using the standard CRR identity that the Pillar 1 minimum capital "
    "requirement equals 8% of RWA - flagged wherever used. FY2015's RWA/ratios are sourced from the FY2016 Pillar "
    "III Disclosure's own FY2015 comparative column, because the FY2015 edition publishes no such table at all "
    "and there is therefore no own-edition figure for a later comparative to displace. FY2021 is NOT that case "
    "and no longer follows that precedent: its own edition publishes 'Table 2: Key ratios', so every FY2021 "
    "Pillar 3 metric is now taken from it (ticket KM1-034, 18 September 2026).\n"
    "(3) FY2015-2016 held non-zero Tier 2 capital (the collective impairment provision, per CRR transitional rules) "
    "- CET1/Tier1 ratios differ slightly from the Total Capital ratio those two years only, unlike every other year "
    "in this workbook where CET1 = Tier1 = Total Capital exactly (no AT1/T2 instruments from FY2017 onward).\n"
    "(4) Asset Quality: IFRS 9 (with its Stage 1/2/3 model) only took effect 1 January 2018. FY2014-2017 use the "
    "prior IAS 39 credit-quality classification (Neither past due nor impaired / Past due but not impaired / "
    "Individually impaired) - a genuinely different regime, not a gap; shown in separate rows on that sheet, "
    "scoped to Financing arrangements only (the IAS 39-era note's own scope), whereas the FY2018-2025 IFRS 9 "
    "'Exposure by Stage' rows are scoped more broadly (financing arrangements, finance leases, due from financial "
    "institutions/customers and investment securities combined, per the Bank's own note) - the two blocks are not "
    "directly comparable in scope and are not chain-linked."
)

CASH_FLOW_SOURCES = (
    "Sources - BLME plc's own Statement of Cash Flows, £'000s, all years, each from that year's own "
    "originally-published Financial Statements (not a later restated comparative):\n"
    f"FY2025: BLME plc Financial Statements 31 December 2025, p.31-32 - {FS2025_URL}\n"
    f"FY2024: BLME plc Financial Statements 31 December 2024, p.31 - {FS2024_URL}\n"
    f"FY2023: BLME plc Financial Statements 31 December 2023, p.32 - {FS2023_URL}\n"
    f"FY2022: BLME plc Financial Statements 31 December 2022, p.32 - {FS2022_URL}\n"
    f"FY2021: BLME plc Financial Statements 31 December 2021, p.30 - {FS2021_URL}\n"
    f"FY2020: BLME plc Financial Statements 31 December 2020, p.28 - {FS2020_URL}\n"
    f"FY2019: BLME plc Financial Statements 31 December 2019, p.26 - {FS2019_URL}\n"
    f"FY2018: BLME plc Financial Statements 31 December 2018, p.22 - {FS2018_URL}\n"
    f"FY2017: Bank of London and The Middle East plc Annual Report and Financial Statements 2017, 'Statement of "
    f"Cash Flows', p.26 - {FS2017_URL}\n"
    f"FY2016: Bank of London and The Middle East plc Annual Report and Accounts 2016, 'Bank statement of cash "
    f"flows', p.32 - {FS2016_URL}\n"
    f"FY2015: Bank of London and The Middle East plc Annual Report and Accounts 2015, 'Bank statement of cash "
    f"flows', p.32 - {FS2015_URL}\n"
    f"FY2014: Bank of London and The Middle East plc Annual Report and Accounts - Revised 2014, 'Bank statement of "
    f"cash flows', p.35 (originally reported in whole £, converted to £'000s here for consistency with every other "
    f"column) - {FS2014_URL}\n"
    "The FY2025 report restates FY2024's comparative (a prior period adjustment of -£9,035k to retained earnings "
    "at 1 Jan 2024, per its own Note 2.3), and the FY2024 report itself already restated FY2023's comparative "
    "(-£3,964k, per its own Note 2b) - both are genuine disclosed restatements, but every column in this sheet "
    "uses each year's own originally-published figures (project convention), not a later restated version.\n"
    "Presentation changed several times across the 12 years: FY2021-FY2023 include a separate 'Due from customers' "
    "line in operating assets (dropped FY2024 onward, reappearing FY2014-2020); FY2025 combines the 'operating "
    "assets' and 'operating liabilities' movements into a single unlabelled subtotal; FY2014-2020 include "
    "'Operating lease assets' movements (wound down to nil by FY2021, dropped thereafter) - shown as blank cells "
    "where a line doesn't apply that year, not gaps. All TOTAL rows reconcile exactly to source for every year.\n\n"
    + ENTITY_NOTE
)


FY2021_RESOURCING_NOTE = (
    "FY2021 RE-SOURCED TO ITS OWN EDITION, 18 SEPTEMBER 2026 (ticket KM1-034), AND CHECKED FIGURE BY FIGURE "
    "AGAINST THE FY2022 COMPARATIVE IT REPLACES. Until that date every FY2021 figure on these Pillar 3 metric "
    "sheets was taken from the FY2022 Pillar III Disclosure's FY2021 comparative column, justified as being "
    "'for consistency with every other year in this workbook'. That is the reasoning the project's rule - use "
    "each year's OWN edition, never a later edition's comparative - exists to forbid, because consistency is "
    "what makes a substitution feel harmless. Every FY2021 cell above now comes from BLME's own FY2021 "
    "Pillar III Disclosure.\n"
    "The comparison is recorded rather than discarded, so a reader can tell 'we checked and it matched' from "
    "'nobody ever looked'. FY2021 edition vs FY2022 edition's FY2021 comparative:\n"
    "- CET1 capital / Tier 1 capital / Total capital: the FY2021 edition's Table 2 prints £239m for all three "
    "(it captions the third 'Total regulatory capital resources'); the FY2022 comparative prints 238,839 in "
    "GBP'000 (= £238.839m) for all three. THEY AGREE at the precision the FY2021 edition prints. £239m is "
    "carried here, which is the bank's own precision for that year: every year FY2015-FY2020 is likewise an "
    "integer £m, FY2017-FY2020 off the same 'Table 2: Key ratios' in their own editions. The finer 238.839 "
    "figure is not lost: it is "
    "what the KM1 Key Metrics sheet carries, under rule 28, and it is named here.\n"
    "- CET1 ratio / Tier 1 ratio / Total capital ratio: 18.18% in both documents, all three rows. Identical.\n"
    "- Leverage ratio: 14.92% in both. The FY2021 edition prints it twice - Table 2 (p.7) and section 16 "
    "'Table 40: Leverage' (p.55), which gives the Basel and the UK leverage ratio as 14.92% each, and states "
    "BLME has no claims on central banks to exclude, so the two bases coincide for this bank. Its leverage "
    "exposure measure, £1,600m, agrees with the FY2022 comparative's 1,600,428 GBP'000.\n"
    "- Total RWAs: the FY2021 edition's own Table 8 prints £1,313.777m; the FY2022 comparative prints 1,313,776 "
    "GBP'000. A £1,000 rounding difference between the bank's own two printings of the same quantity. Recorded, "
    "not reconciled, and the own-edition 1,313.777 is what this workbook now carries - which is also the figure "
    "the RWA Breakdown sheet's FY2021 total carries, from that same Table 8, so the two sheets now agree where "
    "before they differed by £1k.\n"
    "- LCR: the two documents GENUINELY DIFFER, 208% against 315%, and this is a basis difference rather than a "
    "restatement. See the LCR sheet's own source note and note, which set out the evidence on both sides.\n"
    "- NSFR: only the FY2021 edition prints a figure (113.85%); the FY2022 comparative prints the literal string "
    "'N/A'. See the NSFR sheet.\n"
    "- MREL: neither document prints a ratio. See the MREL Ratio sheet.\n"
    "THE ABSENCE OF A KM1 TEMPLATE IN THE FY2021 EDITION IS A FINDING, NOT A FAILED SEARCH. Text extraction "
    "from the 55-page FY2021 PDF returns 103 hits for 'capital', 123 for 'ratio', 54 for 'liquidity', 21 for "
    "'buffer', 16 for 'own funds' and 14 for 'leverage', and against that richness returns ZERO for 'KM1', "
    "'Key metrics' and 'SREP'. The document uses the bank's own pre-template vocabulary - 'Total regulatory "
    "capital resources', 'Risk-weighted assets', 'Leverage ratio exposure measure' - which is why it still "
    "supplies almost every metric on these sheets even though it supplies no KM1 rows.\n"
)


def p3_sources(extra=""):
    return (
        "Sources - BLME plc's own Pillar III Disclosures, £m capital amounts / % ratios, all years:\n"
        f"FY2025: Pillar III Disclosure - 31 December 2025, Key metrics table, p.4 - {P32025_URL}\n"
        f"FY2024: Pillar III Disclosure - 31 December 2024, Key metrics table, p.4 - {P32024_URL}\n"
        f"FY2023: Pillar III Disclosure - 31 December 2023, Key metrics table, p.4 - {P32023_URL}\n"
        f"FY2022: Pillar III Disclosure - 31 December 2022, Key metrics table, p.4 - {P32022_URL}\n"
        f"FY2021: Pillar III Disclosure - 31 December 2021, section 1.3 'Table 2: Key ratios', p.7 (capital "
        f"amounts, the three capital ratios, leverage exposure and ratio, LCR, NSFR) and section 4.2 'Table 8: "
        f"Overview of Risk Weighted Assets', p.15 (Total RWAs) - {P32021_URL}\n"
        f"FY2020: Pillar III Disclosure - 31 December 2020, Table 2 'Key ratios', p.6 - {P32020_URL}\n"
        f"FY2019: Pillar III Disclosure - 31 December 2019, Table 2 'Key ratios', p.6 - {P32019_URL}\n"
        f"FY2018: Pillar III Disclosure - 31 December 2018, Table 2 'Key ratios', p.6 - {P32018_URL}\n"
        f"FY2017: Pillar III Disclosure - 31 December 2017, Table 2 'Key ratios', p.5 - {P32017_URL}\n"
        f"FY2016: Pillar III Disclosures 2016, Table 3 'Regulatory capital composition' / Table 7 'Leverage ratio', "
        f"pp.13,16 - {P32016_URL}\n"
        f"FY2015: sourced from the FY2016 Pillar III Disclosures' own FY2015 comparative column (Table 3/Table 7, "
        f"pp.13,16) - {P32016_URL} (the FY2015 edition itself, {P32015_URL}, pre-dates CRD IV's standardised "
        f"template and discloses only absolute Tier 1/Tier 2 capital resource amounts - no RWA and no ratio at "
        f"all - so the FY2016 report's comparative column is used. That is the map's rule-28 case, in which a "
        f"year's own edition publishes NO capital table at all and there is therefore no own-edition figure for a "
        f"later comparative to displace; it is NOT the case FY2021 was in - see the FY2021 note below).\n"
        f"FY2014: DERIVED from the FY2014 Annual Report and Accounts - Revised's own 'Capital adequacy' note "
        f"(Total regulatory capital £189,179,557; Total Pillar 1 capital requirement £99,164,000), p.115 - "
        f"{FS2014_URL} - using the standard CRR identity that the Pillar 1 minimum capital requirement equals 8% "
        f"of RWA (RWA = £99,164,000 / 0.08 = £1,239.55m); the FY2014 Pillar III Disclosure itself, {P32014_URL}, "
        f"discloses only absolute Tier 1 capital resource amounts, no RWA and no ratio of any kind.\n"
        + "\n" + FY2021_RESOURCING_NOTE
        + (extra + "\n" if extra else "")
        + "\n" + ENTITY_NOTE
    )


bw = BankWorkbook(bank_name="Bank of London and The Middle East plc", years=YEARS, year_label=YEAR_LABEL,
                   header_color="5D3FD3")

# ---------------------------------------------------------------
# ST- rollout (batch ST-013): Balance Sheet, P&L, Statement of Changes in
# Equity, Asset Quality, RWA Breakdown. Sourced from the same Companies
# House / blme.com Financial Statements filings already cited above
# (FS20XX_URL) - each year's OWN originally-published report is used
# (project convention), not a later restated comparative column, even
# though the FY2024 and FY2025 reports both restate their prior year's
# comparative (Note 2.3/2b) - see PRESENTATION_NOTE below.
# ---------------------------------------------------------------
STATEMENTS_SOURCES = (
    "Sources - BLME plc's own Income Statement / Statement of Financial Position / Statement of Changes in "
    "Equity, £'000s, each from that year's own originally-published Financial Statements:\n"
    f"FY2025: BLME plc Financial Statements 31 December 2025, pp.26,28-29 - {FS2025_URL}\n"
    f"FY2024: BLME plc Financial Statements 31 December 2024, pp.28,30,32 - {FS2024_URL}\n"
    f"FY2023: BLME plc Financial Statements 31 December 2023, pp.29,31,33 - {FS2023_URL}\n"
    f"FY2022: BLME plc Financial Statements 31 December 2022, pp.29,31,33 - {FS2022_URL}\n"
    f"FY2021: BLME plc Financial Statements 31 December 2021, pp.27,29,31 - {FS2021_URL}\n"
    f"FY2020: BLME plc Financial Statements 31 December 2020, pp.25,27,29 - {FS2020_URL}\n"
    f"FY2019: BLME plc Financial Statements 31 December 2019, pp.23,25,27 - {FS2019_URL}\n"
    f"FY2018: BLME plc Financial Statements 31 December 2018, pp.19,21,23 - {FS2018_URL}\n"
    f"FY2017: Bank of London and The Middle East plc Annual Report and Financial Statements 2017, 'Income "
    f"Statement'/'Statement of Financial Position'/'Bank Statement of Changes in Equity', pp.23,25,27 - "
    f"{FS2017_URL}\n"
    f"FY2016: Bank of London and The Middle East plc Annual Report and Accounts 2016, 'Consolidated income "
    f"statement' (P&L only - see ENTITY_NOTE), 'Bank statement of financial position', 'Bank statement of changes "
    f"in equity', pp.28,31,35 - {FS2016_URL}\n"
    f"FY2015: Bank of London and The Middle East plc Annual Report and Accounts 2015, 'Consolidated income "
    f"statement' (P&L only - see ENTITY_NOTE), 'Bank statement of financial position', 'Bank statement of changes "
    f"in equity', pp.28,31,35 - {FS2015_URL}\n"
    f"FY2014: Bank of London and The Middle East plc Annual Report and Accounts - Revised 2014, 'Consolidated "
    f"income statement' (P&L only - see ENTITY_NOTE), 'Bank statement of financial position', 'Bank statement of "
    f"changes in equity', pp.30,33,37 (originally reported in whole £, converted to £'000s here) - {FS2014_URL}\n\n"
    + ENTITY_NOTE
)

PRESENTATION_NOTE = (
    "PRESENTATION NOTE: the FY2024 report restated FY2023's comparative (Note 2b, -£3,964k to retained earnings "
    "at 1 Jan 2023) and the FY2025 report restated FY2024's comparative (Note 2.3, -£8,762k to retained earnings "
    "at 1 Jan 2024) - both genuine disclosed restatements. Every P&L/Balance Sheet column here uses each year's "
    "own originally-published figures (project convention, matching the Cash Flow Statement sheet), and the "
    "Statement of Changes in Equity shows both restatements as explicit 'Prior period adjustment' rows (as "
    "disclosed) rather than silently bridging FY2023->FY2024 or FY2024->FY2025. 'Investments in subsidiaries' "
    "only appears as its own Balance Sheet line FY2024-25 (FY2021-23's own reports don't show it separately); "
    "'Due from customers' only appears FY2014-22 (nil/absent thereafter); 'Profit rate swaps' liability only "
    "appears FY2018-2021 (nil/absent thereafter); 'Assets held for sale' appears FY2019-20 and FY2023 only. "
    "FY2025's own equity statement renames the 'Fair value reserve' column 'Other reserves' - shown here under "
    "the FY2021-24 label for column consistency; the underlying balance is the same reserve. 'Operating lease "
    "assets' (FY2014-2020) and 'Cash flow hedging reserve' (FY2014-2016) both wound down to nil and were dropped "
    "from the Bank's own statements thereafter - see ENTITY_NOTE for the FY2018/2019 IFRS 9/IFRS 16 transition "
    "adjustments shown as explicit rows on the Equity Changes sheet."
)

# ---------------------------------------------------------------
# Balance Sheet
# ---------------------------------------------------------------
balance_sheet_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and cash equivalents", {"FY2025": 130528, "FY2024": 90139, "FY2023": 76008, "FY2022": 135262, "FY2021": 112076,
     "FY2020": 231486, "FY2019": 66746, "FY2018": 103585, "FY2017": 94931, "FY2016": 68560, "FY2015": 72814, "FY2014": 38274}),
    ("DATA", "Due from financial institutions", {"FY2025": 26703, "FY2024": 153704, "FY2023": 299363, "FY2022": 451675, "FY2021": 479210,
     "FY2020": 339629, "FY2019": 23508, "FY2018": 8045, "FY2017": 28544, "FY2016": 107182, "FY2015": 18875, "FY2014": 176526}),
    ("DATA", "Due from customers", {"FY2022": 0, "FY2021": 24993, "FY2020": 34465, "FY2019": 14081, "FY2018": 14612,
     "FY2017": 9027, "FY2016": 0, "FY2015": 0, "FY2014": 5038}),
    ("DATA", "Total investment securities", {"FY2025": 29228, "FY2024": 44584, "FY2023": 44927, "FY2022": 35734, "FY2021": 59807,
     "FY2020": 90835, "FY2019": 111039, "FY2018": 135043, "FY2017": 126250, "FY2016": 112422, "FY2015": 191543, "FY2014": 197290}),
    ("DATA", "Investment securities - Sukuk (amortised cost)", {"FY2025": 29228, "FY2024": 31515, "FY2023": 15774, "FY2022": 10005,
     "FY2021": 15045, "FY2020": 24264, "FY2019": 23502, "FY2018": 9637}),
    ("DATA", "Investment securities - Sukuk (held to maturity, IAS 39)", {"FY2017": 9075, "FY2016": 18000}),
    ("DATA", "Investment securities - Sukuk (FVOCI)", {"FY2024": 12722, "FY2021": 23568, "FY2020": 37542, "FY2019": 59038, "FY2018": 93894}),
    ("DATA", "Investment securities - Sukuk (available-for-sale, IAS 39)", {"FY2017": 104883, "FY2016": 90991, "FY2015": 125807, "FY2014": 136847}),
    ("DATA", "Investment securities - Sukuk (fair value through profit and loss, IAS 39)", {"FY2014": 3417}),
    ("DATA", "Investment securities - Equity (FVOCI)", {"FY2024": 347, "FY2023": 341, "FY2022": 659, "FY2021": 321,
     "FY2020": 318, "FY2019": 328, "FY2018": 341}),
    ("DATA", "Investment securities - Equity (available-for-sale, IAS 39)", {"FY2017": 973, "FY2016": 3170, "FY2015": 4117, "FY2014": 3684}),
    ("DATA", "Investment securities - Sharia'a compliant funds (fair value through profit and loss)",
     {"FY2016": 240, "FY2015": 58056, "FY2014": 53325}),
    ("DATA", "Investment securities - Investment in subsidiaries (at cost, bundled within this line FY2014-FY2023 only)",
     {"FY2023": 28812, "FY2022": 25070, "FY2021": 20873, "FY2020": 28711, "FY2019": 28171, "FY2018": 31171,
      "FY2017": 11319, "FY2016": 21, "FY2015": 3563, "FY2014": 17}),
    ("DATA", "Investments in subsidiaries", {"FY2025": 21574, "FY2024": 29151}),
    ("DATA", "Financing arrangements", {"FY2025": 1218128, "FY2024": 1151123, "FY2023": 1010255, "FY2022": 912937, "FY2021": 800318,
     "FY2020": 819162, "FY2019": 847880, "FY2018": 700949, "FY2017": 556642, "FY2016": 474637, "FY2015": 627223, "FY2014": 723280}),
    ("DATA", "Finance lease receivables", {"FY2025": 1424, "FY2024": 2705, "FY2023": 3014, "FY2022": 35550, "FY2021": 42755,
     "FY2020": 207307, "FY2019": 417970, "FY2018": 256458, "FY2017": 170546, "FY2016": 232701, "FY2015": 281959, "FY2014": 160540}),
    ("DATA", "Operating lease assets", {"FY2020": 0, "FY2019": 39042, "FY2018": 43242, "FY2017": 34205, "FY2016": 21977,
     "FY2015": 29050, "FY2014": 36388}),
    ("DATA", "Investment in joint ventures", {"FY2025": 28994, "FY2024": 32157, "FY2023": 7350, "FY2022": 1154, "FY2021": 1157,
     "FY2020": 1142, "FY2019": 1216}),
    ("DATA", "Profit rate swaps (asset)", {"FY2019": 0, "FY2018": 73}),
    ("DATA", "Property and equipment", {"FY2025": 1336, "FY2024": 2136, "FY2023": 2548, "FY2022": 3801, "FY2021": 2782,
     "FY2020": 3270, "FY2019": 4007, "FY2018": 488, "FY2017": 986, "FY2016": 1521, "FY2015": 2069, "FY2014": 352}),
    ("DATA", "Intangible assets", {"FY2025": 2661, "FY2024": 2611, "FY2023": 1607, "FY2022": 714,
     "FY2020": 0, "FY2019": 56, "FY2018": 266, "FY2017": 837, "FY2016": 1693, "FY2015": 2262, "FY2014": 1633}),
    ("DATA", "Other assets", {"FY2025": 8793, "FY2024": 16450, "FY2023": 6421, "FY2022": 17221, "FY2021": 11719,
     "FY2020": 7326, "FY2019": 15982, "FY2018": 6671, "FY2017": 3920, "FY2016": 8238, "FY2015": 11585, "FY2014": 4682}),
    ("DATA", "Current tax asset", {"FY2025": 1015, "FY2024": 1998, "FY2023": 2243, "FY2022": 2587, "FY2021": 934,
     "FY2020": 803, "FY2017": 0, "FY2016": 0, "FY2015": 700, "FY2014": 500}),
    ("DATA", "Deferred tax asset", {"FY2025": 14418, "FY2024": 13600, "FY2023": 13830, "FY2022": 15741, "FY2021": 13099,
     "FY2020": 7495, "FY2019": 4497, "FY2018": 3514, "FY2017": 0, "FY2016": 0, "FY2015": 3062, "FY2014": 1480}),
    ("DATA", "Assets held for sale", {"FY2023": 29934, "FY2020": 477, "FY2019": 2575}),
    ("TOTAL", "Total assets", {"FY2025": 1484802, "FY2024": 1540358, "FY2023": 1497500, "FY2022": 1612376, "FY2021": 1548850,
     "FY2020": 1743397, "FY2019": 1548599, "FY2018": 1272946, "FY2017": 1025888, "FY2016": 1028931, "FY2015": 1241142, "FY2014": 1345983}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Due to financial institutions", {"FY2025": 49571, "FY2024": 33754, "FY2023": 6967, "FY2022": 51039, "FY2021": 272605,
     "FY2020": 185935, "FY2019": 375565, "FY2018": 672240, "FY2017": 514392, "FY2016": 586964, "FY2015": 669849, "FY2014": 614380}),
    ("DATA", "Due to customers", {"FY2025": 1197104, "FY2024": 1262682, "FY2023": 1248979, "FY2022": 1323870, "FY2021": 1031887,
     "FY2020": 1300714, "FY2019": 917569, "FY2018": 357427, "FY2017": 277341, "FY2016": 213804, "FY2015": 321473, "FY2014": 471444}),
    ("DATA", "Profit rate swaps", {"FY2021": 334, "FY2020": 760, "FY2019": 1196, "FY2018": 469, "FY2017": 636, "FY2016": 1305, "FY2015": 1369, "FY2014": 2236}),
    ("DATA", "Current tax liability", {"FY2019": 1220, "FY2018": 438}),
    ("DATA", "Other liabilities", {"FY2025": 14059, "FY2024": 13088, "FY2023": 13322, "FY2022": 14552, "FY2021": 14307,
     "FY2020": 21727, "FY2019": 19571, "FY2018": 14246, "FY2017": 12998, "FY2016": 10062, "FY2015": 10679, "FY2014": 13872}),
    ("TOTAL", "Total liabilities", {"FY2025": 1260734, "FY2024": 1309524, "FY2023": 1269268, "FY2022": 1389461, "FY2021": 1319133,
     "FY2020": 1509136, "FY2019": 1315121, "FY2018": 1044820, "FY2017": 805367, "FY2016": 812135, "FY2015": 1003370, "FY2014": 1101931}),
    ("SECTION", "Equity", {}),
    ("DATA", "Share capital", {"FY2025": 48933, "FY2024": 48933, "FY2023": 48933, "FY2022": 48933, "FY2021": 48933,
     "FY2020": 48933, "FY2019": 48933, "FY2018": 48933, "FY2017": 48933, "FY2016": 48933, "FY2015": 48933, "FY2014": 48933}),
    ("DATA", "Share premium", {"FY2025": 140623, "FY2024": 140623, "FY2023": 140623, "FY2022": 140623, "FY2021": 140623,
     "FY2020": 140623, "FY2019": 140623, "FY2018": 140623, "FY2017": 180623, "FY2016": 180623, "FY2015": 180623, "FY2014": 205623}),
    ("DATA", "Capital contribution", {"FY2025": 3527, "FY2024": 3527, "FY2023": 3527, "FY2022": 3527, "FY2021": 3527,
     "FY2020": 3527, "FY2019": 3527, "FY2018": 2207, "FY2017": 1911, "FY2016": 1604, "FY2015": 1484, "FY2014": 1410}),
    ("DATA", "Fair value reserve", {"FY2025": -145, "FY2024": -347, "FY2023": -63, "FY2022": -108, "FY2021": -107,
     "FY2020": 101, "FY2019": 230, "FY2018": -713, "FY2017": -380, "FY2016": -331, "FY2015": 537, "FY2014": 151}),
    ("DATA", "Cash flow hedging reserve", {"FY2016": 0, "FY2015": -1166, "FY2014": -1435}),
    ("DATA", "Retained earnings", {"FY2025": 31130, "FY2024": 38098, "FY2023": 35212, "FY2022": 29940, "FY2021": 36741,
     "FY2020": 41077, "FY2019": 40165, "FY2018": 37076, "FY2017": -10566, "FY2016": -14033, "FY2015": 7361, "FY2014": -10630}),
    ("TOTAL", "Total equity", {"FY2025": 224068, "FY2024": 230834, "FY2023": 228232, "FY2022": 222915, "FY2021": 229717,
     "FY2020": 234261, "FY2019": 233478, "FY2018": 228126, "FY2017": 220521, "FY2016": 216796, "FY2015": 237772, "FY2014": 244052}),
    ("TOTAL", "Total liabilities and equity", {"FY2025": 1484802, "FY2024": 1540358, "FY2023": 1497500, "FY2022": 1612376, "FY2021": 1548850,
     "FY2020": 1743397, "FY2019": 1548599, "FY2018": 1272946, "FY2017": 1025888, "FY2016": 1028931, "FY2015": 1241142, "FY2014": 1345983}),
]

INVESTMENT_SECURITIES_BREAKDOWN_NOTE = (
    "INVESTMENT SECURITIES BREAKDOWN: the 'Investment securities - ...' sub-rows below the renamed 'Total "
    "investment securities' line are transcribed from each year's own 'Investment Securities' note (Bank/BLME "
    "plc column, not Group), which splits the balance both by measurement basis (fair value through profit or "
    "loss / fair value through other comprehensive income (FVOCI) / amortised cost under IFRS 9 from FY2018 "
    "onward; fair value through profit or loss / available-for-sale / held-to-maturity under IAS 39 for "
    "FY2014-FY2017) and by instrument (Sukuk, listed equity, Sharia'a compliant funds, investment in "
    "subsidiaries):\n"
    f"FY2025/FY2024: Note 16 'Investment Securities and Investment in Subsidiaries', p.60 - {FS2025_URL}\n"
    f"FY2023/FY2022: Note 18 'Investment Securities', p.67 - {FS2023_URL}\n"
    f"FY2021/FY2020: Note 18 'Investment Securities', p.68 - {FS2021_URL}\n"
    f"FY2019/FY2018: Note 19 'Investment Securities', p.67 - {FS2019_URL}\n"
    f"FY2017/FY2016: Note 17 'Investment Securities', p.57 - {FS2017_URL}\n"
    f"FY2015/FY2014: Note 18 'Investment securities' (Bank column), p.76 - {FS2015_URL}\n\n"
    "Each year's sub-rows sum exactly to that year's 'Total investment securities' line (verified against the "
    "note's own IFRS 9 Stage 1/2/3 ECL and impairment-provision deductions, which are netted into the amortised "
    "cost/held-to-maturity Sukuk sub-row for that year, matching how the note itself nets them before arriving "
    "at its own total). 'Investment in subsidiaries' is bundled inside this note (and this Balance Sheet line) "
    "FY2014-FY2023 only - it moves to its own separate 'Investments in subsidiaries' Balance Sheet line "
    "FY2024-FY2025 (see PRESENTATION_NOTE above); the bundled sub-row here is zero/absent for FY2024-FY2025 to "
    "avoid double-counting. No sub-row split by issuer type (UK government/gilts/sovereign vs supranational/"
    "corporate) is disclosed anywhere in BLME's own notes for any year - Sukuk issuers are not broken out "
    "further than the single 'Sukuk' instrument line shown above."
)

bw.add_balance_sheet_sheet(
    title="Bank of London and The Middle East plc — Statement of Financial Position",
    subtitle="BLME plc, Bank-solo basis, £'000s.",
    rows=balance_sheet_rows,
    sources_text=STATEMENTS_SOURCES + "\n\n" + PRESENTATION_NOTE + "\n\n" + INVESTMENT_SECURITIES_BREAKDOWN_NOTE,
    first_col_width=64,
    source_height=460,
    unit_suffix=" (£'000s)",
)

# ---------------------------------------------------------------
# Profit & Loss - FY2014-2016 are Group (Consolidated) figures, all other
# years Bank-solo. See ENTITY_NOTE.
# ---------------------------------------------------------------
income_statement_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Income from financing and investing activities", {"FY2025": 92246, "FY2024": 96103, "FY2023": 81198, "FY2022": 57261, "FY2021": 47649,
     "FY2020": 55718, "FY2019": 53846, "FY2018": 48725, "FY2017": 39650, "FY2016": 54995, "FY2015": 60099, "FY2014": 53157}),
    ("DATA", "Returns to financial institutions and customers", {"FY2025": -53752, "FY2024": -57877, "FY2023": -45550, "FY2022": -23845, "FY2021": -17678,
     "FY2020": -26230, "FY2019": -25782, "FY2018": -17551, "FY2017": -16285, "FY2016": -19530, "FY2015": -21508, "FY2014": -24423}),
    ("TOTAL", "Net margin", {"FY2025": 38494, "FY2024": 38226, "FY2023": 35648, "FY2022": 33416, "FY2021": 29971,
     "FY2020": 29488, "FY2019": 28064, "FY2018": 31174, "FY2017": 23365, "FY2016": 35465, "FY2015": 38591, "FY2014": 28734}),
    ("DATA", "Fee and commission income", {"FY2025": 2274, "FY2024": 2232, "FY2023": 1764, "FY2022": 364, "FY2021": 665,
     "FY2020": 1778, "FY2019": 2613, "FY2018": 2360, "FY2017": 1816, "FY2016": 2687, "FY2015": 2551, "FY2014": 4109}),
    ("DATA", "Fee and commission expense", {"FY2025": -5321, "FY2024": -2135, "FY2023": -1381, "FY2022": -964, "FY2021": -2417,
     "FY2020": -5175, "FY2019": -2230, "FY2018": -417, "FY2017": -494, "FY2016": -520, "FY2015": -651, "FY2014": -266}),
    ("TOTAL", "Net fee and commission income", {"FY2025": -3047, "FY2024": 97, "FY2023": 383, "FY2022": -600, "FY2021": -1752,
     "FY2020": -3397, "FY2019": 383, "FY2018": 1943, "FY2017": 1322, "FY2016": 2167, "FY2015": 1900, "FY2014": 3843}),
    ("DATA", "Net investment gains/(losses)", {"FY2023": 0, "FY2022": 629, "FY2021": 763,
     "FY2020": 443, "FY2019": 112, "FY2018": -256, "FY2017": -2330, "FY2016": -3117, "FY2015": -1922, "FY2014": -529}),
    ("DATA", "Net fair value gains on investment properties", {"FY2016": -40, "FY2015": 4707, "FY2014": 2667}),
    ("DATA", "Operating lease income", {"FY2020": 6123, "FY2019": 8751, "FY2018": 7733, "FY2017": 5312, "FY2016": 8703,
     "FY2015": 15131, "FY2014": 21027}),
    ("DATA", "Credit impairment (losses)/gains", {"FY2025": -3938, "FY2024": -3236, "FY2023": 555, "FY2022": -13398, "FY2021": -12451,
     "FY2020": -7455, "FY2019": -1699, "FY2018": -2030}),
    ("DATA", "Impairment of investment in subsidiary", {"FY2025": 1185, "FY2024": 339, "FY2023": -3434}),
    ("DATA", "Other operating income", {"FY2025": 17795, "FY2024": 13440, "FY2023": 14785, "FY2022": 11274, "FY2021": 4720,
     "FY2020": 4088, "FY2019": 7195, "FY2018": 2093, "FY2017": 6580, "FY2016": 3682, "FY2015": 4925, "FY2014": 5958}),
    ("DATA", "Share of profit/(loss) of equity-accounted investees, net of tax", {"FY2025": 658, "FY2024": 2921, "FY2023": 81, "FY2022": 97, "FY2021": 98,
     "FY2020": 25, "FY2019": 9}),
    ("TOTAL", "Net operating income / Total operating income", {"FY2025": 51147, "FY2024": 51787, "FY2023": 48018, "FY2022": 31418, "FY2021": 21349,
     "FY2020": 29315, "FY2019": 42815, "FY2018": 40657, "FY2017": 34249, "FY2016": 46860, "FY2015": 63332, "FY2014": 61701}),
    ("SECTION", "Expenses", {}),
    ("DATA", "Personnel/staff costs", {"FY2025": -28090, "FY2024": -27850, "FY2023": -23624, "FY2022": -20134, "FY2021": -14090,
     "FY2020": -12908, "FY2019": -13957, "FY2018": -15827, "FY2017": -15239, "FY2016": -15628, "FY2015": -16518, "FY2014": -16644}),
    ("DATA", "Operating lease depreciation", {"FY2020": -5128, "FY2019": -7197, "FY2018": -6027, "FY2017": -4318, "FY2016": -6366,
     "FY2015": -12025, "FY2014": -16286}),
    ("DATA", "Other operating expenses", {"FY2025": -20212, "FY2024": -15301, "FY2023": -15547, "FY2022": -19364, "FY2021": -13631,
     "FY2020": -9883, "FY2019": -7386, "FY2018": -10015, "FY2017": -12549, "FY2016": -24620, "FY2015": -20067, "FY2014": -14545}),
    ("DATA", "Other depreciation and amortisation", {"FY2025": -1242, "FY2024": -897, "FY2023": -1010, "FY2022": -957, "FY2021": -804,
     "FY2020": -866, "FY2019": -1518, "FY2018": -1069, "FY2017": -1515, "FY2016": -1522, "FY2015": -787, "FY2014": -436}),
    ("DATA", "Exceptional costs - Offer", {"FY2019": -2851}),
    ("DATA", "Change in third party interest in consolidated funds (Group, FY2014-2016 only)", {"FY2016": -45, "FY2015": -1673, "FY2014": -1199}),
    ("TOTAL", "Total operating expenses", {"FY2025": -49544, "FY2024": -44048, "FY2023": -40181, "FY2022": -40455, "FY2021": -28525,
     "FY2020": -28785, "FY2019": -32909, "FY2018": -32938, "FY2017": -33621, "FY2016": -48181, "FY2015": -51070, "FY2014": -49110}),
    ("DATA", "Operating profit/(loss) before impairment charges (FY2014-2017 subtotal only)",
     {"FY2017": 628, "FY2016": -1321, "FY2015": 12262, "FY2014": 12591}),
    ("DATA", "Net impairment credit/(charge) on financial assets and operating leases (FY2014-2017, Group/Bank, IAS 39 - "
             "post-opex placement that year, unlike the pre-opex 'Credit impairment' row used FY2018 onward)",
     {"FY2017": 2734, "FY2016": -15843, "FY2015": -20659, "FY2014": -11602}),
    ("DATA", "Loss on disposal of group company (FY2016 only)", {"FY2016": -1720}),
    ("TOTAL", "Profit/(loss) before tax", {"FY2025": 1603, "FY2024": 7739, "FY2023": 7837, "FY2022": -9037, "FY2021": -7176,
     "FY2020": 530, "FY2019": 9906, "FY2018": 7719, "FY2017": 3362, "FY2016": -18884, "FY2015": -8397, "FY2014": 990}),
    ("DATA", "Tax charge/credit", {"FY2025": -184, "FY2024": -889, "FY2023": -2515, "FY2022": 2230, "FY2021": 2840,
     "FY2020": 382, "FY2019": -1215, "FY2018": 2954, "FY2017": 105, "FY2016": -2499, "FY2015": 1547, "FY2014": -15}),
    ("TOTAL", "Profit/(loss) for the year", {"FY2025": 1419, "FY2024": 6850, "FY2023": 5322, "FY2022": -6807, "FY2021": -4336,
     "FY2020": 912, "FY2019": 8691, "FY2018": 10673, "FY2017": 3467, "FY2016": -21383, "FY2015": -6850, "FY2014": 974}),
    ("SECTION", "Other comprehensive income", {}),
    ("DATA", "Other comprehensive income/(expense), net of tax", {"FY2025": -43, "FY2024": -284, "FY2023": -5, "FY2022": 7, "FY2021": -208,
     "FY2020": -129, "FY2019": 956, "FY2018": 491, "FY2017": -49, "FY2016": 539, "FY2015": 685, "FY2014": 1171}),
    ("TOTAL", "Total comprehensive income/(loss) for the year", {"FY2025": 1376, "FY2024": 6566, "FY2023": 5317, "FY2022": -6800, "FY2021": -4544,
     "FY2020": 783, "FY2019": 9647, "FY2018": 11164, "FY2017": 3418, "FY2016": -20844, "FY2015": -6165, "FY2014": 2146}),
]

bw.add_income_statement_sheet(
    title="Bank of London and The Middle East plc — Income Statement",
    subtitle="BLME plc, Bank-solo basis (FY2017-2025) / Group-consolidated basis (FY2014-2016 - see note), £'000s.",
    rows=income_statement_rows,
    sources_text=STATEMENTS_SOURCES + "\n\n" + PRESENTATION_NOTE,
    first_col_width=72,
    source_height=460,
    unit_suffix=" (£'000s)",
)

# ---------------------------------------------------------------
# Statement of Changes in Equity (chronological, Bank-solo throughout,
# unlike the P&L sheet above - the Bank statement of changes in equity
# exists for every year including FY2014-2016).
# ---------------------------------------------------------------
equity_changes_rows = [
    ("TOTAL", "At 31 December 2013", (48933, 205623, 3210, -524, -2122, -12272, -66, 243621)),
    ("DATA", "Profit for the year (FY2014)", (None, None, None, None, None, 498, None, 498)),
    ("DATA", "Other comprehensive income (FY2014)", (None, None, None, 675, 193, None, None, 868)),
    ("DATA", "Transactions with owners, net (FY2014)", (None, None, -1801, None, None, 639, None, -1162)),
    ("TOTAL", "At 31 December 2014", (48933, 205623, 1410, 151, -1435, -10630, None, 244052)),
    ("DATA", "Loss for the year (FY2015)", (None, None, None, None, None, -7101, None, -7101)),
    ("DATA", "Other comprehensive income (FY2015)", (None, None, None, 386, 269, None, None, 655)),
    ("DATA", "Transactions with owners, net (FY2015)", (None, -25000, 74, None, None, 25092, None, 166)),
    ("TOTAL", "At 31 December 2015", (48933, 180623, 1484, 537, -1166, 7361, None, 237772)),
    ("DATA", "Loss for the year (FY2016)", (None, None, None, None, None, -21458, None, -21458)),
    ("DATA", "Other comprehensive income (FY2016)", (None, None, None, -868, 1166, None, None, 298)),
    ("DATA", "Transactions with owners, net (FY2016)", (None, None, 120, None, None, 64, None, 184)),
    ("TOTAL", "At 31 December 2016", (48933, 180623, 1604, -331, 0, -14033, None, 216796)),
    ("DATA", "Profit for the year (FY2017)", (None, None, None, None, None, 3467, None, 3467)),
    ("DATA", "Other comprehensive expense (FY2017)", (None, None, None, -49, None, None, None, -49)),
    ("DATA", "Transactions with owners, net (FY2017)", (None, None, 307, None, None, None, None, 307)),
    ("TOTAL", "At 31 December 2017", (48933, 180623, 1911, -380, None, -10566, None, 220521)),
    ("DATA", "Changes on initial application of IFRS 9 (1 Jan 2018)", (None, None, None, None, None, 25, None, 25)),
    ("TOTAL", "At 1 January 2018 (as restated)", (48933, 180623, 1911, -380, None, -10541, None, 220546)),
    ("DATA", "Profit for the year (FY2018)", (None, None, None, None, None, 10673, None, 10673)),
    ("DATA", "Other comprehensive income (FY2018)", (None, None, None, 491, None, None, None, 491)),
    ("DATA", "Transactions with owners, net (FY2018)", (None, -40000, 296, -824, None, 36944, None, -3584)),
    ("TOTAL", "At 31 December 2018", (48933, 140623, 2207, -713, None, 37076, None, 228126)),
    ("DATA", "Changes on initial application of IFRS 16 (1 Jan 2019)", (None, None, None, None, None, -237, None, -237)),
    ("TOTAL", "At 1 January 2019 (as restated)", (48933, 140623, 2207, -713, None, 36839, None, 227889)),
    ("DATA", "Profit for the year (FY2019)", (None, None, None, None, None, 8691, None, 8691)),
    ("DATA", "Other comprehensive income (FY2019)", (None, None, None, 956, None, None, None, 956)),
    ("DATA", "Transactions with owners, net (FY2019)", (None, None, 1320, -13, None, -5365, None, -4058)),
    ("TOTAL", "At 31 December 2019", (48933, 140623, 3527, 230, None, 40165, None, 233478)),
    ("DATA", "Profit for the year (FY2020)", (None, None, None, None, None, 912, None, 912)),
    ("DATA", "Other comprehensive expense (FY2020)", (None, None, None, -129, None, None, None, -129)),
    ("TOTAL", "At 31 December 2020", (48933, 140623, 3527, 101, None, 41077, None, 234261)),
    ("DATA", "Loss for the year (FY2021)", (None, None, None, None, None, -4336, None, -4336)),
    ("DATA", "Other comprehensive expense (FY2021)", (None, None, None, -208, None, None, None, -208)),
    ("TOTAL", "At 31 December 2021", (48933, 140623, 3527, -107, None, 36741, None, 229717)),
    ("DATA", "Loss for the year (FY2022)", (None, None, None, None, None, -6807, None, -6807)),
    ("DATA", "Other comprehensive income (FY2022)", (None, None, None, 7, None, None, None, 7)),
    ("DATA", "Transactions with owners, net (FY2022)", (None, None, None, -8, None, 6, None, -2)),
    ("TOTAL", "At 31 December 2022", (48933, 140623, 3527, -108, None, 29940, None, 222915)),
    ("DATA", "Profit for the year (FY2023)", (None, None, None, None, None, 5322, None, 5322)),
    ("DATA", "Other comprehensive expense (FY2023)", (None, None, None, -5, None, None, None, -5)),
    ("DATA", "Transactions with owners, net (FY2023)", (None, None, None, 50, None, -50, None, 0)),
    ("TOTAL", "At 31 December 2023", (48933, 140623, 3527, -63, None, 35212, None, 228232)),
    ("DATA", "Prior period adjustment (FY2024 Annual Report Note 2b)", (None, None, None, None, None, -3964, None, -3964)),
    ("TOTAL", "At 1 January 2024 (as restated)", (48933, 140623, 3527, -63, None, 31248, None, 224268)),
    ("DATA", "Profit for the year (FY2024)", (None, None, None, None, None, 6850, None, 6850)),
    ("DATA", "Other comprehensive expense (FY2024)", (None, None, None, -284, None, None, None, -284)),
    ("TOTAL", "At 31 December 2024", (48933, 140623, 3527, -347, None, 38098, None, 230834)),
    ("DATA", "Prior period adjustment (FY2025 Annual Report Note 2.3)", (None, None, None, None, None, -8762, None, -8762)),
    ("TOTAL", "At 1 January 2025 (as restated)", (48933, 140623, 3527, -347, None, 29336, None, 222072)),
    ("DATA", "Profit for the year (FY2025)", (None, None, None, None, None, 1419, None, 1419)),
    ("DATA", "Other comprehensive income/(expense) (FY2025)", (None, None, None, 202, None, -245, None, -43)),
    ("DATA", "Sale of equity instrument at FVOCI (FY2025)", (None, None, None, None, None, 620, None, 620)),
    ("TOTAL", "At 31 December 2025", (48933, 140623, 3527, -145, None, 31130, None, 224068)),
]

bw.add_equity_changes_sheet(
    title="Bank of London and The Middle East plc — Statement of Changes in Equity",
    subtitle="BLME plc, Bank-solo basis, £'000s. Chronological roll-forward, oldest to newest, FY2013 opening to FY2025 closing.",
    headers=["Share capital", "Share premium", "Capital contribution", "Fair value reserve", "Cash flow hedging reserve",
             "Retained earnings", "Foreign currency translation reserve", "Total"],
    rows=equity_changes_rows,
    sources_text=STATEMENTS_SOURCES + "\n\n" + PRESENTATION_NOTE,
    first_col_width=58,
    source_height=460,
)

# ---------------------------------------------------------------
# Sheet: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Profit/(loss) before tax", {"FY2025": 1603, "FY2024": 7739, "FY2023": 7837, "FY2022": -9037, "FY2021": -7176,
     "FY2020": 530, "FY2019": 9906, "FY2018": 7719, "FY2017": 3362, "FY2016": -19023, "FY2015": -7101, "FY2014": 498}),
    ("DATA", "Exchange differences", {"FY2025": -21, "FY2024": -3, "FY2023": -5, "FY2022": -10, "FY2021": -12,
     "FY2020": 332, "FY2019": -394, "FY2018": -173, "FY2017": -1745, "FY2016": 722, "FY2015": -529, "FY2014": 24}),
    ("DATA", "Fair value (gain)/loss on investment securities", {"FY2022": 195, "FY2021": -8,
     "FY2020": -232, "FY2019": -318, "FY2018": 252, "FY2017": 2359, "FY2016": 202, "FY2015": -2049, "FY2014": -1492}),
    ("DATA", "Share of profit of equity-accounted investees, net of tax", {"FY2025": -658, "FY2024": -2921, "FY2023": -81, "FY2022": -97, "FY2021": -100,
     "FY2020": -25, "FY2019": -9}),
    ("DATA", "Credit impairment losses / provision for impairment", {"FY2025": 3938, "FY2024": 2897, "FY2023": 2879, "FY2022": 13398, "FY2021": 12451,
     "FY2020": 7455, "FY2019": 1806, "FY2018": 2030, "FY2017": -2734, "FY2016": 15791, "FY2015": 20591, "FY2014": 11602}),
    ("DATA", "Impairment of investment in subsidiary", {"FY2025": -1185}),
    ("DATA", "Depreciation and amortisation", {"FY2025": 748, "FY2024": 343, "FY2023": 235, "FY2022": 60, "FY2021": 29,
     "FY2020": 5199, "FY2019": 7886, "FY2018": 7097, "FY2017": 5833, "FY2016": 5199, "FY2015": 7128, "FY2014": 9962}),
    ("DATA", "Gain on sale of property and equipment / intangibles", {"FY2015": -929, "FY2014": 299}),
    ("DATA", "Share-based payment awards", {"FY2020": 0, "FY2019": 392, "FY2018": 293, "FY2017": 307, "FY2016": 171, "FY2015": 166, "FY2014": 54}),
    ("DATA", "Adjustments to cash flow hedge reserve", {"FY2016": 2053}),
    ("DATA", "Accretion of instruments held under financing arrangements", {"FY2014": -13}),
    ("DATA", "Movements relating to profit rate swaps", {"FY2022": -112, "FY2020": -854, "FY2019": 327, "FY2018": 363, "FY2017": 114,
     "FY2016": -250, "FY2015": 1667, "FY2014": 44}),
    ("DATA", "IFRS 16 - depreciation and finance charges/additions", {"FY2025": 494, "FY2024": 630, "FY2023": 775, "FY2022": 2797, "FY2021": 878,
     "FY2020": 933, "FY2019": 995}),
    ("DATA", "Accretion of finance charge on lease liabilities", {"FY2025": 65}),
    ("DATA", "Amortisation of investment securities / future swap present value", {"FY2025": -195, "FY2024": 365, "FY2023": 152, "FY2022": 239, "FY2021": 257,
     "FY2020": 233, "FY2019": 26, "FY2017": 26, "FY2015": -75, "FY2014": -111}),
    ("DATA", "Net change in fair value of investment in equity/debt at FVOCI", {"FY2025": 280}),
    ("DATA", "Gain on other asset", {"FY2015": -608, "FY2014": -745}),
    ("DATA", "Tax (credit)/expense", {"FY2015": -1630, "FY2014": -140}),
    ("DATA", "Loss on disposal of investment", {"FY2016": 1353}),
    ("TOTAL", "Net cash generated before changes in operating assets and liabilities",
     {"FY2025": 5069, "FY2024": 9050, "FY2023": 11792, "FY2022": 7433, "FY2021": 6319,
      "FY2020": 13571, "FY2019": 20617, "FY2018": 17581, "FY2017": 7522, "FY2016": 6218, "FY2015": 16631, "FY2014": 19982}),
    ("DATA", "Due from financial institutions", {"FY2025": 127437, "FY2024": 145520, "FY2023": 152940, "FY2022": 26243, "FY2021": -138243,
     "FY2020": -311592, "FY2019": -15441, "FY2018": 21288, "FY2017": 77139, "FY2016": -81752, "FY2015": 153357, "FY2014": -52750}),
    ("DATA", "Due from customers", {"FY2022": 24950, "FY2021": 9594, "FY2020": -20306, "FY2019": 551, "FY2018": -5585,
     "FY2017": -9027, "FY2016": 0, "FY2015": 5038, "FY2014": -5038}),
    ("DATA", "Financing arrangements", {"FY2025": -69536, "FY2024": -143580, "FY2023": -97301, "FY2022": -126771, "FY2021": 13336,
     "FY2020": 14520, "FY2019": -149067, "FY2018": -150426, "FY2017": -75068, "FY2016": 137129, "FY2015": 77548, "FY2014": -101620}),
    ("DATA", "Finance lease receivables", {"FY2025": 1262, "FY2024": -1367, "FY2023": 32645, "FY2022": 7214, "FY2021": 159360,
     "FY2020": 210667, "FY2019": -160487, "FY2018": -86255, "FY2017": 65383, "FY2016": 41956, "FY2015": -127948, "FY2014": 28822}),
    ("DATA", "Operating lease assets", {"FY2020": 33914, "FY2019": -2997, "FY2018": -15065, "FY2017": -16439, "FY2016": 3045,
     "FY2015": 986, "FY2014": 3875}),
    ("DATA", "Other assets", {"FY2025": 7645, "FY2024": -10275, "FY2023": 10797, "FY2022": -5460, "FY2021": -4206,
     "FY2020": 8560, "FY2019": -10880, "FY2018": -2746, "FY2017": 4138, "FY2016": 3022, "FY2015": -6325, "FY2014": -641}),
    ("DATA", "Due to financial institutions", {"FY2025": 15709, "FY2024": 26815, "FY2023": -42286, "FY2022": -226876, "FY2021": 83757,
     "FY2020": -201668, "FY2019": -285387, "FY2018": 152563, "FY2017": -67650, "FY2016": -122778, "FY2015": 76263, "FY2014": -40753}),
    ("DATA", "Due to customers", {"FY2025": -64011, "FY2024": 13193, "FY2023": -75983, "FY2022": 290262, "FY2021": -263860,
     "FY2020": 386573, "FY2019": 561491, "FY2018": 80168, "FY2017": 63683, "FY2016": -108712, "FY2015": -149866, "FY2014": 162942}),
    ("DATA", "Cash settlement of share-based payment awards", {"FY2015": 0, "FY2014": -841}),
    ("DATA", "Other liabilities", {"FY2025": 1403, "FY2024": -649, "FY2023": 294, "FY2022": 1930, "FY2021": -9295,
     "FY2020": 14255, "FY2019": -5557, "FY2018": 6808, "FY2017": 1190, "FY2016": 8658, "FY2015": -10432, "FY2014": 3250}),
    ("DATA", "Corporation tax paid", {"FY2025": -7, "FY2023": -260, "FY2022": -2062, "FY2021": -2847,
     "FY2020": -4607, "FY2019": -697, "FY2018": -113, "FY2016": 700, "FY2015": -200, "FY2014": -500}),
    ("TOTAL", "Net cash generated from/(used in) operating activities",
     {"FY2025": 24971, "FY2024": 38707, "FY2023": -7362, "FY2022": -3137, "FY2021": -146085,
      "FY2020": 143887, "FY2019": -47854, "FY2018": 18218, "FY2017": 50871, "FY2016": -112514, "FY2015": 35052, "FY2014": 16728}),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Purchase/(disposal) of property and equipment", {"FY2025": 23, "FY2024": -123, "FY2023": -791, "FY2022": -876, "FY2021": -15,
     "FY2020": -71, "FY2018": 0, "FY2017": -7, "FY2016": -25, "FY2015": -964, "FY2014": -89}),
    ("DATA", "Purchase of intangible assets", {"FY2025": -452, "FY2024": -1031, "FY2023": -893, "FY2022": -714,
     "FY2018": 0, "FY2017": -118, "FY2016": -372, "FY2015": -1229, "FY2014": -715}),
    ("DATA", "Purchase of investment securities", {"FY2025": -7598, "FY2024": -34858, "FY2023": -15629, "FY2022": -4873,
     "FY2020": -37036, "FY2019": -63316, "FY2018": -33753, "FY2017": -89021, "FY2016": -54919, "FY2015": -149328, "FY2014": -204325}),
    ("DATA", "Sale of investment securities", {"FY2025": 19615, "FY2024": 8006, "FY2023": 1741, "FY2022": 33130, "FY2021": 30483,
     "FY2020": 57604, "FY2019": 84038, "FY2018": 29790, "FY2017": 62565, "FY2016": 158447, "FY2015": 150467, "FY2014": 163336}),
    ("DATA", "Sale of subsidiary to a fellow subsidiary", {"FY2023": 298}),
    ("DATA", "Purchase of interest in assets held for sale", {"FY2023": -35763, "FY2020": -541, "FY2019": -11116}),
    ("DATA", "Sale of interest in assets held for sale", {"FY2024": 1800, "FY2023": 6000, "FY2021": 485,
     "FY2020": 2100, "FY2019": 8500}),
    ("DATA", "Purchase of interest in joint venture", {"FY2023": -6440, "FY2019": -1235}),
    ("DATA", "Dividend(s) received from joint venture(s)", {"FY2025": 2170, "FY2024": 2284, "FY2023": 325, "FY2022": 100, "FY2021": 100,
     "FY2020": 99, "FY2019": 28}),
    ("DATA", "Sale of equity instrument at FVOCI", {"FY2025": 620}),
    ("DATA", "Sale of interest in joint venture", {"FY2025": 1650}),
    ("TOTAL", "Net cash generated from/(used in) investing activities",
     {"FY2025": 16028, "FY2024": -23922, "FY2023": -51152, "FY2022": 26767, "FY2021": 31053,
      "FY2020": 22155, "FY2019": 16899, "FY2018": -3963, "FY2017": -26581, "FY2016": 103131, "FY2015": -1054, "FY2014": -41793}),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Payment of principal portion of lease liabilities", {"FY2025": -512, "FY2024": -589, "FY2023": -719, "FY2022": -1123, "FY2021": -1086,
     "FY2020": -1104, "FY2019": -1156}),
    ("DATA", "Payment of finance charge on lease liabilities", {"FY2025": -65}),
    ("DATA", "Dividend paid to BLME Holdings plc", {"FY2020": 0, "FY2019": -5400, "FY2018": -3750}),
    ("DATA", "Expenses of BLME Scheme of Arrangement", {"FY2014": 0}),
    ("TOTAL", "Net cash generated from/(used in) financing activities",
     {"FY2025": -577, "FY2024": -589, "FY2023": -719, "FY2022": -1123, "FY2021": -1086,
      "FY2020": -1104, "FY2019": -6556, "FY2018": -3750, "FY2014": 0}),
    ("TOTAL", "Net change in cash and cash equivalents",
     {"FY2025": 40422, "FY2024": 14196, "FY2023": -59233, "FY2022": 22507, "FY2021": -116118,
      "FY2020": 164938, "FY2019": -37511, "FY2018": 10505, "FY2017": 24290, "FY2016": -9383, "FY2015": 33998, "FY2014": -25065}),
    ("DATA", "Exchange differences in respect of cash and cash equivalents", {"FY2025": -33, "FY2024": -65, "FY2023": -21, "FY2022": 679, "FY2021": -3292,
     "FY2020": -198, "FY2019": 672, "FY2018": -1851, "FY2017": 2081, "FY2016": 5129, "FY2015": 542, "FY2014": 2586}),
    ("DATA", "Cash and cash equivalents at the beginning of the period", {"FY2025": 90139, "FY2024": 76008, "FY2023": 135262, "FY2022": 112076, "FY2021": 231486,
     "FY2020": 66746, "FY2019": 103585, "FY2018": 94931, "FY2017": 68560, "FY2016": 72814, "FY2015": 38274, "FY2014": 60753}),
    ("TOTAL", "Cash and cash equivalents at the end of the period",
     {"FY2025": 130528, "FY2024": 90139, "FY2023": 76008, "FY2022": 135262, "FY2021": 112076,
      "FY2020": 231486, "FY2019": 66746, "FY2018": 103585, "FY2017": 94931, "FY2016": 68560, "FY2015": 72814, "FY2014": 38274}),
]

bw.add_cash_flow_sheet(
    title="Bank of London and The Middle East plc — Statement of Cash Flows",
    subtitle="BLME plc, Bank-solo basis, £'000s. Full 12 years, no cash-flow exemption.",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=84,
    source_height=340,
    unit_suffix=" (£'000s)",
)

# ---------------------------------------------------------------
# Asset Quality: FY2018-2025 use the IFRS 9 'Exposure by Stage' / 'ECL by
# Stage' notes (financing arrangements, finance leases, due from financial
# institutions/customers and investment securities combined, incl. undrawn
# commitments - per the Bank's own note). FY2014-2017 pre-date IFRS 9 (which
# took effect 1 Jan 2018) and instead use the IAS 39 credit-quality note,
# scoped to Financing arrangements only - a genuinely different regime and
# scope, not a gap; see ENTITY_NOTE point (4).
# ---------------------------------------------------------------
AQ_GROSS_S1 = {"FY2025": 1091948, "FY2024": 1194794, "FY2023": 1105472, "FY2022": 1379874, "FY2021": 1444155,
               "FY2020": 1585063, "FY2019": 1476469, "FY2018": 1215991}
AQ_GROSS_S2 = {"FY2025": 330284, "FY2024": 226768, "FY2023": 331650, "FY2022": 195379, "FY2021": 99784,
               "FY2020": 138414, "FY2019": 142975, "FY2018": 196034}
AQ_GROSS_S3 = {"FY2025": 62168, "FY2024": 62031, "FY2023": 64893, "FY2022": 78708, "FY2021": 43059,
               "FY2020": 39003, "FY2019": 19369, "FY2018": 21472}
AQ_GROSS_TOTAL = {y: AQ_GROSS_S1[y] + AQ_GROSS_S2[y] + AQ_GROSS_S3[y] for y in AQ_GROSS_S1}

AQ_ECL_S1 = {"FY2025": 998, "FY2024": 534, "FY2023": 504, "FY2022": 577, "FY2021": 559,
             "FY2020": 1338, "FY2019": 2139, "FY2018": 1305}
AQ_ECL_S2 = {"FY2025": 1230, "FY2024": 797, "FY2023": 749, "FY2022": 2151, "FY2021": 1455,
             "FY2020": 2734, "FY2019": 1685, "FY2018": 4425}
AQ_ECL_S3 = {"FY2025": 4851, "FY2024": 12554, "FY2023": 7647, "FY2022": 11236, "FY2021": 13275,
             "FY2020": 12594, "FY2019": 6551, "FY2018": 9018}
AQ_ECL_TOTAL = {y: AQ_ECL_S1[y] + AQ_ECL_S2[y] + AQ_ECL_S3[y] for y in AQ_ECL_S1}

AQ_NET_TOTAL = {y: AQ_GROSS_TOTAL[y] - AQ_ECL_TOTAL[y] for y in AQ_GROSS_TOTAL}
AQ_STAGE3_RATIO = {y: f"{AQ_GROSS_S3[y] / AQ_GROSS_TOTAL[y] * 100:.1f}%" for y in AQ_GROSS_TOTAL}
AQ_STAGE3_COVERAGE = {y: f"{AQ_ECL_S3[y] / AQ_GROSS_S3[y] * 100:.1f}%" for y in AQ_GROSS_TOTAL}
AQ_OVERALL_COVERAGE = {y: f"{AQ_ECL_TOTAL[y] / AQ_GROSS_TOTAL[y] * 100:.2f}%" for y in AQ_GROSS_TOTAL}

# IAS 39 era (FY2014-2017), Financing arrangements only, Bank basis, £'000s
# (FY2014 converted from whole £ as originally reported).
IAS39_NEITHER = {"FY2017": 501318, "FY2016": 421474, "FY2015": 573289, "FY2014": 682881}
IAS39_PAST_DUE = {"FY2017": 40255, "FY2016": 23758, "FY2015": 33257, "FY2014": 17602}
IAS39_IMPAIRED_GROSS = {"FY2017": 24627, "FY2016": 45232, "FY2015": 53838, "FY2014": 56267}
IAS39_ALLOWANCE = {"FY2017": -9558, "FY2016": -15827, "FY2015": -33161, "FY2014": -33470}
IAS39_TOTAL = {y: IAS39_NEITHER[y] + IAS39_PAST_DUE[y] + IAS39_IMPAIRED_GROSS[y] + IAS39_ALLOWANCE[y] for y in IAS39_NEITHER}
IAS39_IMPAIRED_RATIO = {y: f"{IAS39_IMPAIRED_GROSS[y] / (IAS39_NEITHER[y] + IAS39_PAST_DUE[y] + IAS39_IMPAIRED_GROSS[y]) * 100:.1f}%" for y in IAS39_NEITHER}
IAS39_COVERAGE_RATIO = {y: f"{-IAS39_ALLOWANCE[y] / IAS39_IMPAIRED_GROSS[y] * 100:.1f}%" for y in IAS39_NEITHER}

asset_quality_rows = [
    ("SECTION", "IFRS 9 era (FY2018-2025): combined exposure by stage, incl. undrawn commitments", {}),
    ("DATA", "Stage 1 (12-month ECL)", AQ_GROSS_S1),
    ("DATA", "Stage 2 (lifetime ECL, not credit-impaired)", AQ_GROSS_S2),
    ("DATA", "Stage 3 (lifetime ECL, credit-impaired)", AQ_GROSS_S3),
    ("TOTAL", "Total gross exposure", AQ_GROSS_TOTAL),
    ("SECTION", "Expected credit loss (ECL) allowance, by stage", {}),
    ("DATA", "Stage 1 allowance", {y: -v for y, v in AQ_ECL_S1.items()}),
    ("DATA", "Stage 2 allowance", {y: -v for y, v in AQ_ECL_S2.items()}),
    ("DATA", "Stage 3 allowance", {y: -v for y, v in AQ_ECL_S3.items()}),
    ("TOTAL", "Total ECL allowance", {y: -v for y, v in AQ_ECL_TOTAL.items()}),
    ("TOTAL", "Net exposure (IFRS 9 basis)", AQ_NET_TOTAL),
    ("SECTION", "IAS 39 era (FY2014-2017): Financing arrangements only - not comparable in scope to the IFRS 9 rows above", {}),
    ("DATA", "Neither past due nor impaired", IAS39_NEITHER),
    ("DATA", "Past due but not impaired", IAS39_PAST_DUE),
    ("DATA", "Gross exposure associated with impairment provision (individually impaired)", IAS39_IMPAIRED_GROSS),
    ("DATA", "Less: allowance for impairments", IAS39_ALLOWANCE),
    ("TOTAL", "Total Financing arrangements (IAS 39 basis)", IAS39_TOTAL),
    ("SECTION", "Ratios", {}),
    ("DATA", "Stage 3 exposure ratio (Stage 3 / total gross exposure) [IFRS 9, FY2018-2025]", AQ_STAGE3_RATIO),
    ("DATA", "Stage 3 coverage ratio (Stage 3 allowance / Stage 3 exposure) [IFRS 9, FY2018-2025]", AQ_STAGE3_COVERAGE),
    ("DATA", "Overall coverage ratio (total allowance / total gross exposure) [IFRS 9, FY2018-2025]", AQ_OVERALL_COVERAGE),
    ("DATA", "Impaired exposure ratio (impaired / total Financing arrangements) [IAS 39, FY2014-2017]", IAS39_IMPAIRED_RATIO),
    ("DATA", "Impairment coverage ratio (allowance / impaired exposure) [IAS 39, FY2014-2017]", IAS39_COVERAGE_RATIO),
]

bw.add_asset_quality_sheet(
    title="Bank of London and The Middle East plc — Asset Quality / Credit Risk Disclosures",
    subtitle="IFRS 9 combined exposure by stage (FY2018-2025) / IAS 39 Financing-arrangements-only credit quality (FY2014-2017), £'000s. BLME plc, Bank-solo basis.",
    rows=asset_quality_rows,
    sources_text=(
        "Sources - BLME plc's own 'Exposure by Stage'/'ECL by Stage' (Note 15, IFRS 9, FY2018-2025) and 'Analysis "
        "of past due amounts and impairments' (IAS 39, FY2014-2017) notes, Bank column, £'000s:\n"
        f"FY2025/FY2024: BLME plc Financial Statements 31 December 2025, pp.51,53 - {FS2025_URL}\n"
        f"FY2023/FY2022: BLME plc Financial Statements 31 December 2023, pp.59,61 - {FS2023_URL}\n"
        f"FY2021: BLME plc Financial Statements 31 December 2021, p.59 - {FS2021_URL}\n"
        f"FY2020/FY2019: BLME plc Financial Statements 31 December 2020, pp.61-63 - {FS2020_URL}\n"
        f"FY2018: BLME plc Financial Statements 31 December 2019, Note 15 pp.59-60 (FY2018 shown as that report's "
        f"own 1 January 2019 comparative opening balance) - {FS2019_URL}; ECL by Stage FY2018 closing "
        f"cross-checked directly against the FY2018 report's own Note 14, p.54 - {FS2018_URL}\n"
        f"FY2017: Bank of London and The Middle East plc Annual Report and Financial Statements 2017, 'Analysis "
        f"of past due amounts and impairments', Bank column, p.75 - {FS2017_URL}\n"
        f"FY2016: same 2017 Annual Report, Bank column FY2016 comparative, p.75 - {FS2017_URL}\n"
        f"FY2015: Bank of London and The Middle East plc Annual Report and Accounts 2015, 'Analysis of past due "
        f"amounts and impairments', Bank column, p.102 - {FS2015_URL}\n"
        f"FY2014: Bank of London and The Middle East plc Annual Report and Accounts - Revised 2014, 'Analysis of "
        f"past due amounts and impairments', Bank column, p.97 (originally reported in whole £, converted to "
        f"£'000s here) - {FS2014_URL}\n\n"
        "Note: Stage 3 coverage fell sharply from 30.8% (FY2021) to 7.8% (FY2025) - genuine, driven by write-offs "
        "of specifically-provisioned exposures each year (e.g. £13.8m written off in FY2025 alone, per Note 12) "
        "reducing the Stage 3 allowance balance faster than the Stage 3 gross exposure balance - flagged here, "
        "not smoothed. 'Total gross exposure' figures (IFRS 9 rows) are higher than the Balance Sheet's own "
        "Financing arrangements carrying value because they include undrawn credit facilities, off-balance-sheet "
        "commitments, and several other asset classes besides Financing arrangements (per the Bank's own note) - "
        "not a reconciliation error, and not directly comparable to the narrower IAS 39-era Financing-arrangements-"
        "only rows for FY2014-2017. See ENTITY_NOTE point (4) for the full methodology break.\n\n" + ENTITY_NOTE
    ),
    first_col_width=88,
    source_height=440,
    unit_suffix=" (£'000s)",
)

# ---------------------------------------------------------------
# KM1 Key Metrics - BLME's own 'Key metrics' table, FY2022-FY2025 from each
# year's own edition, plus FY2021 from the FY2022 edition's comparative column
# (KM1-035 / map rule 28: the FY2021 edition prints no template at all, only a
# shorter bespoke "Table 2: Key ratios" that fails the row-set test). See the
# sheet note for the evidence and for the two FY2021 figures - LCR and NSFR -
# on which BLME's two tables genuinely disagree.
# ---------------------------------------------------------------
KM1_SOURCES = (
    "Source - BLME plc's own 'Key metrics' table, p.4 of each year's Pillar III Disclosure, amounts in "
    "GBP'000 exactly as printed:\n"
    f"FY2025: Pillar III Disclosure 31 December 2025, p.4 - {P32025_URL}\n"
    f"FY2024: Pillar III Disclosure 31 December 2024, p.4 - {P32024_URL}\n"
    f"FY2023: Pillar III Disclosure 31 December 2023, p.4 - {P32023_URL}\n"
    f"FY2022: Pillar III Disclosure 31 December 2022, p.4 - {P32022_URL}\n"
    f"FY2021 (NOT AN OWN-EDITION COLUMN): the SAME Pillar III Disclosure 2022 document, section 2 'Key "
    f"metrics', printed p.4 ('Page 4 of 5'), COMPARATIVE COLUMN headed 31/12/2021 - {P32022_URL}\n\n"
    "FY2022-FY2025 ARE EACH TAKEN FROM THEIR OWN EDITION'S FIRST COLUMN, so no figure in those four columns "
    "is a later report's restatement. FY2021 is the single exception and is flagged as such above and "
    "explained below.\n\n"
    "THE TABLE IS UNNUMBERED AND UNTITLED AS 'KM1'. BLME captions it simply 'Key metrics' and prints no "
    "template row numbers at all. It is nonetheless the template: it carries the template's row set in the "
    "template's order - available own funds, then risk-weighted exposure amounts, then capital ratios, then "
    "the SREP block, then the combined buffer block, then leverage, then the LCR with its component rows, "
    "then the NSFR with its component rows. Identified by row set rather than by caption, per the map's "
    "row-set test. Row labels are reproduced as BLME prints them, so they carry no row numbers here either.\n\n"
    "WHY FY2021 IS FILLED FROM THE FY2022 EDITION, AND FY2020 AND EARLIER ARE NOT (revised 17 September "
    "2026). BLME adopted this table in its 2022 edition, so THE FY2021 EDITION PUBLISHES NO KM1 TEMPLATE AT "
    "ALL - not a template with rows left blank, but no template, and therefore no own-edition disclosure for "
    "a later comparative to displace. What the FY2021 edition prints instead, at its section 1.3 'Table 2: "
    "Key ratios' (printed p.7 of 55), is a 13-line summary in £m: CET1 / Tier 1 / Total regulatory capital "
    "resources, risk-weighted assets, the three capital ratios, leverage exposure and ratio, LCR%, NSFR%, "
    "and a 'Total capital requirement (Pillar 1 + Pillar 2A)' line that is not a template row at all. No row "
    "numbers, no SREP block, no buffer block, and none of the LCR or NSFR component rows. It fails the "
    "row-set test and is a different and shorter table, not an unnumbered template.\n"
    "That absence was re-established from the document on 17 September 2026 before this column was filled, "
    "and it is a finding rather than a failed search: extraction from the 55-page FY2021 PDF is RICH (103 "
    "hits for 'capital', 123 for 'ratio', 54 for 'liquidity', 21 for 'buffer', 14 for 'leverage'), and "
    "against that richness it returns ZERO hits for 'KM1', 'Key metrics', 'SREP' and 'NSFR' - the last two "
    "being blocks the template cannot omit.\n"
    "THE FY2022 EDITION'S COMPARATIVE COLUMN, headed 31/12/2021 and in GBP'000, carries the complete table "
    "for that date, and THAT IS WHAT THIS SHEET'S FY2021 NOW CARRIES, in the row structure the FY2022 "
    "edition prints it in - the same 24-row structure as the FY2022 column beside it, so nothing is "
    "reshaped. All 24 values were read off the FY2022 PDF directly.\n"
    "This reverses the treatment this sheet carried until 17 September 2026, which omitted FY2021 as a "
    "column entirely and quoted the comparative in this note instead. The evidence above is unchanged; only "
    "the conclusion drawn from it has changed, so that a BLANK on this sheet now means one thing only: BLME "
    "has never published that figure, in any edition, on any basis.\n"
    "FY2020 AND EARLIER REMAIN OFF THIS SHEET for exactly that reason. The FY2021 edition's Table 2 does "
    "carry a 31/12/2020 comparative, but it is the same bespoke 13-line shape, not the template, so it "
    "cannot fill a template column; and no other edition prints FY2020 in template form. Those years' "
    "figures remain on the individual metric sheets, cited to their own editions.\n\n"
    "THE THREE NSFR ROWS FOR FY2021 CARRY '-' BECAUSE THE BANK PRINTS THE LITERAL STRING 'N/A' IN THAT "
    "COLUMN (FY2022 edition p.4, page image re-read 2026-09-19) - not an empty cell. Under KM1 map rule 2 a "
    "printed 'n/a' is carried as the plain ASCII '-' and the glyph actually printed, 'N/A', is recorded here. The "
    "FY2021 column's countercyclical buffer row, by contrast, is a printed '0.00%', a disclosed zero, and is "
    "carried as the zero.\n\n"
    "TWO FY2021 FIGURES ON WHICH THE BANK'S TWO TABLES GENUINELY DISAGREE - BOTH RECORDED, NEITHER "
    "RECONCILED. This surfaced when FY2021 was filled and it is a real finding, not a transcription slip:\n"
    "• LIQUIDITY COVERAGE RATIO. This sheet carries 315%, the figure the FY2022 edition's comparative "
    "column prints, and it is internally consistent with its own component rows in that column (HQLA 71,695 "
    "/ net cash outflows 22,744 = 315.2%), which are 12-month weighted AVERAGES as the row captions say. The "
    "FY2021 edition's own Table 2 prints 208% for the same date, and the LCR metric sheet in this workbook "
    "carries that 208% under its own citation (ticket KM1-034, 18 September 2026 - before that date the "
    "metric sheet carried this sheet's 315% too). The FY2021 edition settles what its own 208% measures: its "
    "section 6.2.6.7 'Table 12: LCR Metrics', p.25, prints the LCR at each 2021 quarter-end (Q1 249%, Q2 "
    "577%, Q3 193%, Q4 208%) with the 31/12/2021 components liquidity buffer £68.65m and net cash outflows "
    "£32.97m, so 208% is a year-end SPOT ratio against this column's 12-month AVERAGE. A BASIS DIFFERENCE, "
    "NOT A RESTATEMENT. The two are not reconciled here and neither is adjusted to match the other; this "
    "sheet reproduces the template column and the metric sheet reproduces the year's own edition, so A "
    "CROSS-CHECK BETWEEN THE TWO SHEETS WILL REPORT THIS CELL, AND THAT REPORT IS CORRECT AND EXPECTED.\n"
    "• NET STABLE FUNDING RATIO. The FY2022 edition's comparative prints 'N/A' for all three NSFR rows, "
    "which is what this sheet shows. The FY2021 edition's own Table 2 does print an NSFR of 113.85%, on its "
    "own bespoke basis, and that is the figure the NSFR metric sheet in this workbook carries under its own "
    "citation. So this sheet and that one legitimately differ for FY2021, each faithful to a different "
    "published table, and neither has been edited to agree with the other.\n"
    "EVERYWHERE ELSE THE TWO FY2021 SOURCES AGREE, AND THAT WAS CHECKED RATHER THAN ASSUMED (ticket KM1-034, "
    "18 September 2026). The FY2021 edition's Table 2 prints CET1 = Tier 1 = Total regulatory capital "
    "resources of £239m against this column's 238,839 GBP'000, all three capital ratios at 18.18% against "
    "18.18%, a leverage exposure measure of £1,600m against 1,600,428 GBP'000 and a leverage ratio of 14.92% "
    "against 14.92%; its Table 8 prints total RWAs of £1,313.777m against this column's 1,313,776 GBP'000, a "
    "£1k rounding difference between the bank's own two printings. The metric sheets now carry the "
    "own-edition figures at the FY2021 edition's own precision, so where they read £239m and this sheet reads "
    "238,839 the two are the same figure printed to different precision, not two figures.\n\n"
    "LATEST-EDITION CHECK: BLME's own Financial Results and Reporting page "
    "(https://www.blme.com/about-us/investors/financial-results-and-reporting/) was read on 2026-09-16. It "
    "lists Pillar III Disclosures for every year from 2009 to 2025; 2025 is the newest and this workbook "
    "already holds it. BLME's year-end is 31 December, so no 2026 edition is due yet.\n\n"
    "ENTITY: BLME plc, the UK-authorised bank and a subsidiary of Boubyan Bank (Kuwait). This is the Bank's "
    "own disclosure, published under its own name - not a parent figure."
)

km1_rows = [
    ("SECTION", "AVAILABLE OWN FUNDS (AMOUNTS)", {}),
    ("DATA", "Common Equity Tier 1 (CET1) capital (£'000)",
     {"FY2025": 225806, "FY2024": 227639, "FY2023": 226478, "FY2022": 227212, "FY2021": 238839}),
    ("DATA", "Tier 1 capital (£'000)",
     {"FY2025": 225806, "FY2024": 227639, "FY2023": 226478, "FY2022": 227212, "FY2021": 238839}),
    ("DATA", "Total capital (£'000)",
     {"FY2025": 225806, "FY2024": 227639, "FY2023": 226478, "FY2022": 227212, "FY2021": 238839}),
    ("SECTION", "RISK-WEIGHTED EXPOSURE AMOUNTS", {}),
    ("DATA", "Total risk-weighted exposure amount (£'000)",
     {"FY2025": 1170428, "FY2024": 1279034, "FY2023": 1342418, "FY2022": 1376389, "FY2021": 1313776}),
    ("SECTION", "CAPITAL RATIOS (AS A PERCENTAGE OF RISK-WEIGHTED EXPOSURE AMOUNT)", {}),
    ("DATA", "Common Equity Tier 1 ratio (%)",
     {"FY2025": "19.29%", "FY2024": "17.80%", "FY2023": "16.87%", "FY2022": "16.51%", "FY2021": "18.18%"}),
    ("DATA", "Tier 1 ratio (%)",
     {"FY2025": "19.29%", "FY2024": "17.80%", "FY2023": "16.87%", "FY2022": "16.51%", "FY2021": "18.18%"}),
    ("DATA", "Total capital ratio (%)",
     {"FY2025": "19.29%", "FY2024": "17.80%", "FY2023": "16.87%", "FY2022": "16.51%", "FY2021": "18.18%"}),
    ("SECTION", "ADDITIONAL OWN FUNDS REQUIREMENTS BASED ON SREP (AS A PERCENTAGE OF RISK-WEIGHTED EXPOSURE AMOUNT)", {}),
    ("DATA", "Additional CET1 SREP requirements (%)",
     {"FY2025": "3.59%", "FY2024": "3.59%", "FY2023": "3.59%", "FY2022": "1.94%", "FY2021": "1.94%"}),
    ("DATA", "Total SREP own funds requirements (%)",
     {"FY2025": "11.59%", "FY2024": "11.59%", "FY2023": "11.59%", "FY2022": "9.94%", "FY2021": "9.94%"}),
    ("SECTION", "COMBINED BUFFER REQUIREMENT (AS A PERCENTAGE OF RISK-WEIGHTED EXPOSURE AMOUNT)", {}),
    ("DATA", "Capital conservation buffer (%)",
     {"FY2025": "2.50%", "FY2024": "2.50%", "FY2023": "2.50%", "FY2022": "2.50%", "FY2021": "2.50%"}),
    ("DATA", "Institution specific countercyclical capital buffer (%)",
     {"FY2025": "1.58%", "FY2024": "1.67%", "FY2023": "1.76%", "FY2022": "0.95%", "FY2021": "0.00%"}),
    ("DATA", "Combined buffer requirement (%)",
     {"FY2025": "4.08%", "FY2024": "4.17%", "FY2023": "4.26%", "FY2022": "3.45%", "FY2021": "2.50%"}),
    ("DATA", "Overall capital requirements (%)",
     {"FY2025": "15.67%", "FY2024": "15.76%", "FY2023": "15.85%", "FY2022": "13.39%", "FY2021": "12.44%"}),
    ("DATA", "CET1 available after meeting the total SREP own funds requirements (%)",
     {"FY2025": "3.62%", "FY2024": "2.04%", "FY2023": "1.02%", "FY2022": "3.11%", "FY2021": "5.74%"}),
    ("SECTION", "LEVERAGE RATIO", {}),
    ("DATA", "Total exposure measure excluding claims on central banks (£'000)",
     {"FY2025": 1510175, "FY2024": 1519554, "FY2023": 1521865, "FY2022": 1622691, "FY2021": 1600428}),
    ("DATA", "Leverage ratio excluding claims on central banks (%)",
     {"FY2025": "14.95%", "FY2024": "14.98%", "FY2023": "14.88%", "FY2022": "14.00%", "FY2021": "14.92%"}),
    ("SECTION", "LIQUIDITY COVERAGE RATIO", {}),
    ("DATA", "Total high-quality liquid assets (HQLA) (Weighted value - average) (£'000)",
     {"FY2025": 63913, "FY2024": 57829, "FY2023": 60522, "FY2022": 92894, "FY2021": 71695}),
    ("DATA", "Cash outflows - Total weighted value (£'000)",
     {"FY2025": 83047, "FY2024": 74573, "FY2023": 83950, "FY2022": 105540, "FY2021": 90975}),
    ("DATA", "Cash inflows - Total weighted value (£'000)",
     {"FY2025": 78968, "FY2024": 69733, "FY2023": 113997, "FY2022": 109725, "FY2021": 140123}),
    ("DATA", "Total net cash outflows (adjusted value) (£'000)",
     {"FY2025": 20762, "FY2024": 18643, "FY2023": 20987, "FY2022": 26385, "FY2021": 22744}),
    ("DATA", "Liquidity coverage ratio (%)",
     {"FY2025": "308%", "FY2024": "310%", "FY2023": "288%", "FY2022": "352%", "FY2021": "315%"}),
    ("SECTION", "NET STABLE FUNDING RATIO", {}),
    ("DATA", "Total available stable funding (£'000)",
     {"FY2025": 1289527, "FY2024": 1281180, "FY2023": 1401110, "FY2022": 1502432, "FY2021": "-"}),
    ("DATA", "Total required stable funding (£'000)",
     {"FY2025": 1070069, "FY2024": 1025644, "FY2023": 969949, "FY2022": 1053953, "FY2021": "-"}),
    ("DATA", "NSFR ratio (%)",
     {"FY2025": "121%", "FY2024": "125%", "FY2023": "144%", "FY2022": "143%", "FY2021": "-"}),
]

bw.add_km1_sheet(
    title="BLME plc - KM1 Key Metrics",
    subtitle="BLME plc's own 'Key metrics' table, as published each year - amounts in GBP'000 as printed. "
             "FY2022-FY2025 come from each year's own edition; FY2021 is the FY2022 edition's comparative "
             "column, because BLME's own FY2021 edition prints no template at all (it prints a shorter "
             "bespoke 'Table 2: Key ratios' instead). See the source note, which also records two FY2021 "
             "figures on which the Bank's two tables disagree.",
    rows=km1_rows,
    sources_text=KM1_SOURCES,
    first_col_width=78,
    source_height=520,
    years=["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"],
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, sources_text, note=None):
    bw.add_metric_sheet(name, f"{unit}" if unit else "", rows_data, sources_text,
                         note=note, first_col_width=52, source_height=200)


metric("CET1 Capital", "£m",
       [("Common Equity Tier 1 (CET1) capital", {"FY2025": 225.806, "FY2024": 227.639, "FY2023": 226.478, "FY2022": 227.212, "FY2021": 239,
         "FY2020": 245, "FY2019": 221, "FY2018": 215, "FY2017": 216, "FY2016": 216, "FY2015": 201, "FY2014": 189.180})],
       p3_sources())

metric("CET1 Ratio", "% of RWA",
       [("CET1 ratio", {"FY2025": "19.29%", "FY2024": "17.80%", "FY2023": "16.87%", "FY2022": "16.51%", "FY2021": "18.18%",
         "FY2020": "16.62%", "FY2019": "15.07%", "FY2018": "17.24%", "FY2017": "20.95%", "FY2016": "20.42%", "FY2015": "15.41%", "FY2014": "15.26%"})],
       p3_sources())

metric("Tier 1 Capital", "£m",
       [("Tier 1 capital", {"FY2025": 225.806, "FY2024": 227.639, "FY2023": 226.478, "FY2022": 227.212, "FY2021": 239,
         "FY2020": 245, "FY2019": 221, "FY2018": 215, "FY2017": 216, "FY2016": 216, "FY2015": 201, "FY2014": 189.180})],
       p3_sources(), note="CET1 = Tier 1 = Total Capital every year from FY2017 onward - BLME has no Additional Tier 1 "
            "or Tier 2 instruments in that period. FY2015-2016 held non-zero Tier 2 capital (the collective "
            "impairment provision, per CRR transitional rules), so Total Capital exceeds CET1/Tier 1 slightly "
            "those two years only (FY2015: Tier1 £201m vs Total £204m; FY2016: Tier1 £216m vs Total £220m) - see "
            "ENTITY_NOTE point (3).")

metric("Tier 1 Ratio", "% of RWA",
       [("Tier 1 ratio", {"FY2025": "19.29%", "FY2024": "17.80%", "FY2023": "16.87%", "FY2022": "16.51%", "FY2021": "18.18%",
         "FY2020": "16.62%", "FY2019": "15.07%", "FY2018": "17.24%", "FY2017": "20.95%", "FY2016": "20.42%", "FY2015": "15.41%", "FY2014": "15.26%"})],
       p3_sources())

metric("Total Capital", "£m",
       [("Total capital", {"FY2025": 225.806, "FY2024": 227.639, "FY2023": 226.478, "FY2022": 227.212, "FY2021": 239,
         "FY2020": 245, "FY2019": 221, "FY2018": 215, "FY2017": 220, "FY2016": 220, "FY2015": 204, "FY2014": 189.180})],
       p3_sources())

metric("Total Capital Ratio", "% of RWA",
       [("Total capital ratio", {"FY2025": "19.29%", "FY2024": "17.80%", "FY2023": "16.87%", "FY2022": "16.51%", "FY2021": "18.18%",
         "FY2020": "16.62%", "FY2019": "15.07%", "FY2018": "17.24%", "FY2017": "21.33%", "FY2016": "20.81%", "FY2015": "15.65%", "FY2014": "15.26%"})],
       p3_sources())

metric("Total RWAs", "£m",
       [("Total risk-weighted exposure amount", {"FY2025": 1170.428, "FY2024": 1279.034, "FY2023": 1342.418, "FY2022": 1376.389, "FY2021": 1313.777,
         "FY2020": 1472.268, "FY2019": 1466.255, "FY2018": 1245.086, "FY2017": 1032, "FY2016": 1055, "FY2015": 1305, "FY2014": 1239.550})],
       p3_sources("FY2014 RWA is derived, not directly disclosed - see the FY2014 line above."))

# ---------------------------------------------------------------
# RWA Breakdown: FY2015-2021 Pillar III Disclosures each include a category
# breakdown (Table 3/Table 8 'Overview of Risk Weighted Assets'); FY2014's
# breakdown is DERIVED from the Annual Report's Pillar 1 capital requirement
# table using the same 8%-of-RWA identity as the Total RWAs sheet. The
# FY2022-2025 Pillar III Disclosures are all short (4-5 page) documents
# containing only the KM1 Key Metrics table (Total RWA as a single figure,
# no category split) - confirmed by reading each document in full, not
# assumed.
# ---------------------------------------------------------------
RWA_SOURCES = (
    "Sources - BLME plc's own Pillar III Disclosures:\n"
    f"FY2021: Pillar III Disclosure - 31 December 2021, Table 8 'Overview of Risk Weighted Assets', p.15 - "
    f"{P32021_URL}\n"
    f"FY2020: Pillar III Disclosure - 31 December 2020, Table 8, p.15 - {P32020_URL}\n"
    f"FY2019: Pillar III Disclosure - 31 December 2019, Table 8, p.15 - {P32019_URL}\n"
    f"FY2018: Pillar III Disclosure - 31 December 2018, Table 8, p.14 - {P32018_URL}\n"
    f"FY2017: Pillar III Disclosure - 31 December 2017, Table 8, p.15 - {P32017_URL}\n"
    f"FY2016: Pillar III Disclosures 2016, Table 3 'Regulatory capital composition', p.13 - {P32016_URL}\n"
    f"FY2015: sourced from the FY2016 Pillar III Disclosures' own FY2015 comparative column, Table 3, p.13 - "
    f"{P32016_URL} (same precedent as the FY2015 capital/ratio figures elsewhere in this workbook).\n"
    f"FY2014: DERIVED from the FY2014 Annual Report's own 'Pillar 1 capital requirements' table (Credit risk "
    f"£93.270m, Market risk £0.239m, Counterparty risk £0.252m, Operational risk £5.403m), p.115 - {FS2014_URL} - "
    f"using the 8%-of-RWA identity (each category's RWA = that category's capital requirement / 0.08).\n"
    f"FY2022-FY2025: Pillar III Disclosures for those years ({P32022_URL}, {P32023_URL}, {P32024_URL}, "
    f"{P32025_URL}) each checked in full (4-5 pages each) - none contains an RWA-by-category breakdown, only the "
    f"single Key metrics 'Total risk-weighted exposure amount' figure (already shown on the Total RWAs sheet). "
    f"Independently RE-VERIFIED 2026-09-12: all 4 PDFs re-downloaded and re-read directly (not just re-checked "
    f"against this note) - each is confirmed still 5 pages, KM1-template-only, no category split. A Wayback "
    f"Machine CDX search of blme.com's full media archive confirms no '-appendices.pdf' companion document (the "
    f"format that carried the FY2019-FY2021 OV1-style category breakdown) was ever published alongside the "
    f"FY2022-FY2025 disclosures - this is a genuine, continuing change in the Bank's own disclosure format, not "
    f"a missed document.\n\n"
    + ENTITY_NOTE
)

# GA-020 (2026-09-19): the FY2022-FY2025 category split is NOT published - each
# edition is a 5-page KM1-only document and each year's financial statements
# (FS2022-FS2025, full text searched 2026-09-19) contain no RWA figure at all.
RWA_SPLIT_NP = {y: (f"Not published – BLME {y} Pillar III Disclosure (5pp) is the Key metrics table only: total "
                    f"RWEA, no split by risk type; {y} financial statements print no RWA")
                for y in ["FY2022", "FY2023", "FY2024", "FY2025"]}

rwa_breakdown_rows = [
    ("SECTION", "RWA by risk category (£m)", {}),
    ("DATA", "Credit risk (excluding counterparty credit risk)", {"FY2021": 1244.608, "FY2020": 1392.593, "FY2019": 1389.033,
     "FY2018": 1162.669, "FY2017": 943, "FY2016": 960, "FY2015": 1220, "FY2014": 1165.875,
     **RWA_SPLIT_NP}),
    ("DATA", "Counterparty credit risk", {"FY2021": 0.509, "FY2020": 0.899, "FY2019": 2.104, "FY2018": 0, "FY2017": 0, "FY2014": 3.150}),
    ("DATA", "Market risk", {"FY2021": 1.397, "FY2020": 5.201, "FY2019": 3.993, "FY2018": 4, "FY2017": 1, "FY2016": 7, "FY2015": 3, "FY2014": 2.988}),
    ("DATA", "Operational risk", {"FY2021": 67.263, "FY2020": 73.575, "FY2019": 77.763, "FY2018": 78, "FY2017": 88, "FY2016": 87, "FY2015": 81, "FY2014": 67.538}),
    ("DATA", "Credit valuation adjustment", {"FY2016": 1, "FY2015": 1}),
    ("TOTAL", "Total RWAs", {"FY2021": 1313.777, "FY2020": 1472.268, "FY2019": 1466.255, "FY2018": 1245.086, "FY2017": 1032,
     "FY2016": 1055, "FY2015": 1305, "FY2014": 1239.550,
     # GA-020 (2026-09-19): FY2022-FY2025 totals FOUND - each edition's Key metrics
     # 'Total risk-weighted exposure amount' (£'000 / 1,000), the same figures the
     # Total RWAs sheet carries. FY2022 re-read off the page image (p.4: 1,376,389).
     "FY2022": 1376.389, "FY2023": 1342.418, "FY2024": 1279.034, "FY2025": 1170.428}),
]

bw.add_rwa_breakdown_sheet(
    title="Bank of London and The Middle East plc — RWA Breakdown",
    subtitle="FY2014-FY2021 (UK OV1-equivalent category split); FY2022-25 publish the total only (Key metrics table), no category split - see note below.",
    rows=rwa_breakdown_rows,
    sources_text=RWA_SOURCES,
    first_col_width=58,
    source_height=340,
    unit_suffix=" (£m)",
)

metric("Leverage Ratio", "%",
       [("Leverage ratio (excluding claims on central banks)", {"FY2025": "14.95%", "FY2024": "14.98%", "FY2023": "14.88%", "FY2022": "14.00%", "FY2021": "14.92%",
         "FY2020": "13.60%", "FY2019": "13.40%", "FY2018": "15.83%", "FY2017": "19.28%", "FY2016": "19.94%", "FY2015": "15.63%",
         "FY2014": ("Not published – FY2014 Annual Report (p.13) says BLME 'was compliant with the leverage ratio' and "
                    "reported it to the PRA, but prints no ratio; FY2014 Pillar III Disclosures (21pp) print none")})],
       p3_sources(),
       note="FY2014 leverage ratio not publicly disclosed - the UK leverage ratio framework was not yet a binding "
            "PRA reporting requirement at that date (per the FY2014 Annual Report's own text: 'the ratio was "
            "reported to the PRA in 2014 and becomes effective in 2018'). No basis break across FY2015-2025 - all "
            "figures are on the 'excluding claims on central banks' basis, unlike several other banks in this "
            "project where FY2021 sits on an older methodology.")

metric("LCR", "%",
       [("Liquidity Coverage Ratio", {"FY2025": "308%", "FY2024": "310%", "FY2023": "288%", "FY2022": "352%", "FY2021": "208%",
         "FY2020": "234.15%", "FY2019": "261.23%", "FY2018": "184.86%", "FY2017": "403%", "FY2016": "4,115%",
         "FY2015": ("Not published – FY2015 Pillar III Disclosures (20pp) and FY2015 financial statements print no LCR "
                    "(full text searched 2026-09-19); FY2016 edition prints none either"),
         "FY2014": ("Not published – FY2014 Pillar III Disclosures (21pp) and FY2014 financial statements print no LCR "
                    "(full text searched 2026-09-19)")})],
       p3_sources(
           f"FY2021 LCR - THE ONE FIGURE ON WHICH BLME'S TWO DOCUMENTS FOR THAT DATE GENUINELY DISAGREE, AND IT "
           f"IS A BASIS DIFFERENCE, NOT A RESTATEMENT. This sheet carries 208%, from BLME's OWN FY2021 Pillar III "
           f"Disclosure - section 1.3 'Table 2: Key ratios', p.7, corroborated inside the same document by section "
           f"6.2.6.7 'Table 12: LCR Metrics', p.25, which prints the LCR 'as reported at the end of each calendar "
           f"quarter of 2021' (Q1 249%, Q2 577%, Q3 193%, Q4 208%) together with its 31/12/2021 components, "
           f"liquidity buffer £68.65m and total net cash outflows £32.97m (68.65 / 32.97 = 208.2%). So 208% is a "
           f"YEAR-END SPOT ratio - {P32021_URL}\n"
           f"The FY2022 Pillar III Disclosure's FY2021 comparative column prints 315% instead, and that figure is "
           f"a 12-MONTH WEIGHTED AVERAGE: its own component rows in that column are captioned 'Weighted value - "
           f"average' and give HQLA 71,695 / total net cash outflows 22,744 = 315.2% - {P32022_URL}. Both figures "
           f"are correct for 31 December 2021 and they are not reconciled here; neither has been adjusted to "
           f"agree with the other. The KM1 Key Metrics sheet in this workbook carries the 315% average, because "
           f"that sheet reproduces the FY2022 edition's template column whole, so THE TWO SHEETS LEGITIMATELY "
           f"DIFFER FOR FY2021 and any cross-check that reports it is reporting a real, documented basis "
           f"divergence rather than a transcription error.\n"
           f"Until 18 September 2026 this sheet carried the 315% average for FY2021 (ticket KM1-034). That was "
           f"the single average-basis figure sitting in the middle of a spot-basis run, which is what made the "
           f"substitution invisible."),
       note="BASIS BREAK AT FY2021/FY2022, and the row caption used to hide it. FY2014-FY2021 are YEAR-END SPOT "
            "ratios, printed in the bespoke 'Table 2: Key ratios' each of those editions carries; FY2022-FY2025 "
            "are the UK KM1 measure, which is a 12-MONTH WEIGHTED AVERAGE. The two are not like-for-like and the "
            "series should not be read as one continuous measure across that boundary. This row was captioned "
            "'Liquidity Coverage Ratio (12-month average)' until 18 September 2026, which was a false statement "
            "about FY2014-FY2021: the FY2020 and FY2021 editions each print a quarterly LCR table of their own "
            "(FY2020's Q4 is 234.15%, FY2021's Q4 is 208%) showing that their Table 2 headline is the "
            "fourth-quarter-end figure, not an average of the four. The caption is now unqualified and the basis "
            "is stated here per year instead.\n"
            "FY2016 sourced from the FY2017 Pillar III Disclosure's own FY2016 comparative column (Table 2, p.5) "
            "since FY2016's own Pillar III Disclosure does not include an LCR figure at all - the 4,115% figure is "
            "transcribed exactly as printed in that source; it is an outlier against every other year in this "
            "series and is flagged here rather than silently corrected or omitted. FY2014-2015 not publicly "
            "disclosed - LCR reporting pre-dates BLME's Pillar 3 disclosure of it.")

metric("NSFR", "%",
       [("Net Stable Funding Ratio", {"FY2025": "121%", "FY2024": "125%", "FY2023": "144%", "FY2022": "143%",
         "FY2021": "113.85%",
         "FY2020": "114.46%", "FY2019": "112.48%", "FY2018": "104%",
         **{y: (f"Not published – BLME {y} Pillar III Disclosures and {y} financial statements (full text searched "
                "2026-09-19) never mention the NSFR; voluntary NSFR disclosure began FY2018")
            for y in ["FY2017", "FY2016", "FY2015", "FY2014"]}})],
       p3_sources(
           f"FY2021 NSFR ONLY: Pillar III Disclosure - 31 December 2021, section 1.3 Table 2 'Key ratios', p.7 - "
           f"{P32021_URL}. The FY2022 report's FY2021 comparative column prints the literal string 'N/A' for NSFR "
           f"rows 18-20, so the FY2021 edition's own Table 2 is the only source for it - as it now is for every "
           f"other FY2021 metric in this workbook too (ticket KM1-034, 18 September 2026).\n"),
       note="FY2018-FY2021 NSFR was voluntarily disclosed by BLME in Table 2 'Key ratios' of its own Pillar III "
            "Disclosure, ahead of the UK's binding NSFR requirement (PRA PS17/21 and PS22/21, in force 1 January "
            "2022); FY2014-2017 pre-date this voluntary disclosure entirely. BASIS NOTE: FY2018-FY2021 are therefore "
            "spot ratios at the reporting date, whereas FY2022 onward are the UK KM1 measure, which PS17/21 requires "
            "to be an average of four quarter-ends - the two are not strictly like-for-like. The FY2022 report's own "
            "FY2021 comparative column shows 'N/A' on that KM1 basis.")

MREL_ST = {y: (f"Not published – BLME {y} Pillar III Disclosures and financial statements (full text searched "
               "2026-09-19) never mention MREL or loss-absorbing capacity") for y in ["FY2014", "FY2015", "FY2016", "FY2017"]}
MREL_ST.update({y: (f"Not published – BLME {y} Pillar III Disclosure (5pp, Key metrics table only) and {y} financial "
                    "statements (full text searched 2026-09-19) never mention MREL") for y in ["FY2022", "FY2023", "FY2024", "FY2025"]})
MREL_ST.update({y: (f"Not applicable – BLME {y} Pillar III s.5.3 (p.{pg}): loss-absorbing capacity equals the minimum "
                    "capital requirement; 'The PRA does not require BLME to hold a MREL recapitalisation reserve'")
                for y, pg in [("FY2018", 15), ("FY2019", 16), ("FY2020", 16), ("FY2021", 16)]})
bw.add_not_disclosed_metric_sheets(
    ["MREL Ratio"],
    p3_sources(),
    statements={"MREL Ratio": MREL_ST},
    per_note={"MREL Ratio": "No MREL ratio is disclosed in any year. CORRECTED 18 September 2026 (ticket "
                             "KM1-034): this note previously said MREL was 'not mentioned in the FY2021-2025 "
                             "Pillar III Disclosures reviewed (searched directly, no hits any year)', which was "
                             "false for FY2021 - that edition mentions it at section 5.3 'Total loss absorbing "
                             "capacity', p.16: 'The total loss absorbing capacity at 31 December 2021 is equal to "
                             "the minimum capital requirement (i.e. Pillar 1 + Pillar 2A capital). The PRA does "
                             "not require BLME to hold a MREL recapitalisation reserve.' That is the same "
                             "statement the FY2018-2020 disclosures make, and it gives no ratio. The FY2022-2025 "
                             "disclosures are 4-5 page documents containing only the KM1 Key metrics table and do "
                             "not mention MREL at all; FY2014-2017 disclosures don't mention it either (it wasn't yet a "
                             "framework) - consistent with a bank of this size not being its own resolution entity "
                             "under the Bank of England's MREL framework throughout the full FY2014-2025 window."},
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {"FY2025": 1484802, "FY2024": 1540358, "FY2023": 1497500, "FY2022": 1612376, "FY2021": 1548850,
         "FY2020": 1743397, "FY2019": 1548599, "FY2018": 1272946, "FY2017": 1025888, "FY2016": 1028931, "FY2015": 1241142, "FY2014": 1345983}),
        ("Financing arrangements", {"FY2025": 1218128, "FY2024": 1151123, "FY2023": 1010255, "FY2022": 912937, "FY2021": 800318,
         "FY2020": 819162, "FY2019": 847880, "FY2018": 700949, "FY2017": 556642, "FY2016": 474637, "FY2015": 627223, "FY2014": 723280}),
        ("Due to customers", {"FY2025": 1197104, "FY2024": 1262682, "FY2023": 1248979, "FY2022": 1323870, "FY2021": 1031887,
         "FY2020": 1300714, "FY2019": 917569, "FY2018": 357427, "FY2017": 277341, "FY2016": 213804, "FY2015": 321473, "FY2014": 471444}),
        ("Total equity", {"FY2025": 224068, "FY2024": 230834, "FY2023": 228232, "FY2022": 222915, "FY2021": 229717,
         "FY2020": 234261, "FY2019": 233478, "FY2018": 228126, "FY2017": 220521, "FY2016": 216796, "FY2015": 237772, "FY2014": 244052}),
    ],
    balance_sheet_unit="£'000s",
    income_statement_totals=[
        ("Net margin", {"FY2025": 38494, "FY2024": 38226, "FY2023": 35648, "FY2022": 33416, "FY2021": 29971,
         "FY2020": 29488, "FY2019": 28064, "FY2018": 31174, "FY2017": 23365, "FY2016": 35465, "FY2015": 38591, "FY2014": 28734}),
        ("Total operating expenses", {"FY2025": -49544, "FY2024": -44048, "FY2023": -40181, "FY2022": -40455, "FY2021": -28525,
         "FY2020": -28785, "FY2019": -33059, "FY2018": -32938, "FY2017": -33621, "FY2016": -48181, "FY2015": -51070, "FY2014": -49110}),
        ("Profit/(loss) for the year", {"FY2025": 1419, "FY2024": 6850, "FY2023": 5322, "FY2022": -6807, "FY2021": -4336,
         "FY2020": 912, "FY2019": 8691, "FY2018": 10673, "FY2017": 3467, "FY2016": -21383, "FY2015": -6850, "FY2014": 974}),
    ],
    income_statement_unit="£'000s (FY2014-2016 Group-consolidated, FY2017-2025 Bank-solo - see ENTITY_NOTE)",
    equity_changes_totals=[
        ("Opening equity (restated where applicable)", {"FY2025": 222072, "FY2024": 224268, "FY2023": 222915, "FY2022": 229717, "FY2021": 234261,
         "FY2020": 233478, "FY2019": 227889, "FY2018": 220546, "FY2017": 216796, "FY2016": 237772, "FY2015": 244052, "FY2014": 243621}),
        ("Total comprehensive income/(loss) for the year", {"FY2025": 1376, "FY2024": 6566, "FY2023": 5317, "FY2022": -6800, "FY2021": -4544,
         "FY2020": 783, "FY2019": 9647, "FY2018": 11164, "FY2017": 3418, "FY2016": -21160, "FY2015": -6446, "FY2014": 1594}),
        ("Other movements, net", {"FY2025": 620, "FY2024": 0, "FY2023": 0, "FY2022": -2, "FY2021": 0,
         "FY2020": 0, "FY2019": -4058, "FY2018": -3584, "FY2017": 307, "FY2016": 184, "FY2015": 166, "FY2014": -1163}),
        ("Closing equity", {"FY2025": 224068, "FY2024": 230834, "FY2023": 228232, "FY2022": 222915, "FY2021": 229717,
         "FY2020": 234261, "FY2019": 233478, "FY2018": 228126, "FY2017": 220521, "FY2016": 216796, "FY2015": 237772, "FY2014": 244052}),
    ],
    equity_changes_unit="£'000s",
    cash_flow_totals=[
        ("Net cash from/(used in) operating activities",
         {"FY2025": 24971, "FY2024": 38707, "FY2023": -7362, "FY2022": -3137, "FY2021": -146085,
          "FY2020": 143887, "FY2019": -47854, "FY2018": 18218, "FY2017": 50871, "FY2016": -112514, "FY2015": 35052, "FY2014": 16728}),
        ("Net cash from/(used in) investing activities",
         {"FY2025": 16028, "FY2024": -23922, "FY2023": -51152, "FY2022": 26767, "FY2021": 31053,
          "FY2020": 22155, "FY2019": 16899, "FY2018": -3963, "FY2017": -26581, "FY2016": 103131, "FY2015": -1054, "FY2014": -41793}),
        ("Net cash from/(used in) financing activities",
         {"FY2025": -577, "FY2024": -589, "FY2023": -719, "FY2022": -1123, "FY2021": -1086,
          "FY2020": -1104, "FY2019": -6556, "FY2018": -3750, "FY2017": 0, "FY2016": 0, "FY2015": 0, "FY2014": 0}),
        ("Cash and cash equivalents at end of period",
         {"FY2025": 130528, "FY2024": 90139, "FY2023": 76008, "FY2022": 135262, "FY2021": 112076,
          "FY2020": 231486, "FY2019": 66746, "FY2018": 103585, "FY2017": 94931, "FY2016": 68560, "FY2015": 72814, "FY2014": 38274}),
    ],
    cash_flow_unit="£'000s",
    ratios=[
        ("CET1 Ratio", {"FY2025": "19.29%", "FY2024": "17.80%", "FY2023": "16.87%", "FY2022": "16.51%", "FY2021": "18.18%",
         "FY2020": "16.62%", "FY2019": "15.07%", "FY2018": "17.24%", "FY2017": "20.95%", "FY2016": "20.42%", "FY2015": "15.41%", "FY2014": "15.26%"}),
        ("Tier 1 Ratio", {"FY2025": "19.29%", "FY2024": "17.80%", "FY2023": "16.87%", "FY2022": "16.51%", "FY2021": "18.18%",
         "FY2020": "16.62%", "FY2019": "15.07%", "FY2018": "17.24%", "FY2017": "20.95%", "FY2016": "20.42%", "FY2015": "15.41%", "FY2014": "15.26%"}),
        ("Total Capital Ratio", {"FY2025": "19.29%", "FY2024": "17.80%", "FY2023": "16.87%", "FY2022": "16.51%", "FY2021": "18.18%",
         "FY2020": "16.62%", "FY2019": "15.07%", "FY2018": "17.24%", "FY2017": "21.33%", "FY2016": "20.81%", "FY2015": "15.65%", "FY2014": "15.26%"}),
        ("Leverage Ratio", {"FY2025": "14.95%", "FY2024": "14.98%", "FY2023": "14.88%", "FY2022": "14.00%", "FY2021": "14.92%",
         "FY2020": "13.60%", "FY2019": "13.40%", "FY2018": "15.83%", "FY2017": "19.28%", "FY2016": "19.94%", "FY2015": "15.63%",
         "FY2014": "Not publicly disclosed"}),
        ("LCR", {"FY2025": "308%", "FY2024": "310%", "FY2023": "288%", "FY2022": "352%", "FY2021": "315%",
         "FY2020": "234.15%", "FY2019": "261.23%", "FY2018": "184.86%", "FY2017": "403%", "FY2016": "4,115%",
         "FY2015": "Not publicly disclosed", "FY2014": "Not publicly disclosed"}),
        ("NSFR", {"FY2025": "121%", "FY2024": "125%", "FY2023": "144%", "FY2022": "143%", "FY2021": "113.85%",
         "FY2020": "114.46%", "FY2019": "112.48%", "FY2018": "104%", "FY2017": "Not publicly disclosed",
         "FY2016": "Not publicly disclosed", "FY2015": "Not publicly disclosed", "FY2014": "Not publicly disclosed"}),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own source "
         "citation for the underlying document/page. NSFR not disclosed FY2014-2017 (pre-dates BLME's voluntary "
         "disclosure of it; the UK NSFR requirement itself only took effect 1 January 2022), and FY2018-FY2021 are "
         "spot ratios rather than the four-quarter average the UK KM1 template requires from FY2022 - see the NSFR "
         "sheet's own note. BLME plc solo basis throughout except the FY2014-2016 Income "
         "Statement figures, which are Group-consolidated (see ENTITY_NOTE) - not the wider BLME Holdings group in "
         "either case. FY2014 leverage ratio and FY2014-2015 LCR not publicly disclosed (pre-dates those "
         "frameworks/templates); FY2014's CET1/Tier1/Total Capital ratios and RWA are derived from the FY2014 "
         "Annual Report's own Pillar 1 capital requirement table (see Total RWAs sheet's source note).",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/BLME FINANCIALS.xlsx")
