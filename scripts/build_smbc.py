import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

# SMBC Bank International plc reports in USD (its functional currency) - this
# workbook converts every $ figure to £ at the user's request. See FX_NOTE
# below for the full methodology; ratios are never converted (see FX_NOTE).
YEARS = ["FY2026", "FY2025", "FY2024", "FY2023", "FY2022", "FY2021", "FY2020", "FY2019", "FY2018", "FY2017", "FY2016",
         "FY2015", "FY2014", "FY2013"]
Y_CORE = YEARS[:YEARS.index('FY2014') + 1]  # HD-072/075/079: FY2014-floor default for Pillar 3/Asset Quality/RWA Breakdown/Overview
  # most recent first; FY2014 was the project-wide historical-depth cap
# (HD-052) until HD-072 lifted it for the four statutory statements only (Balance Sheet/P&L/Statement of Changes
# in Equity/Cash Flow Statement) - Pillar 3/Asset Quality/RWA Breakdown remain capped at FY2014, see those
# sheets' dicts below which deliberately have no FY2013 entries.

AR2021_URL = "https://web.archive.org/web/20240612221125/https://www.smbcgroup.com/emea/images/SMBC/media/SMBC/pdf/disclosures/smbcbi-annual-report-2021.pdf"
AR2022_URL = "https://www.smbcgroup.com/emea/getmedia/efb562ee-627d-41c9-823a-b157f879892f/Annual-Report-and-Financial-Statements-2022-(SMBC-BI).pdf"
AR2023_URL = "https://www.smbcgroup.com/emea/getmedia/1784eaa0-0924-4cd7-a4e4-1613b6cb015f/Annual-Report-and-Financial-Statements-2023-(SMBC-BI).pdf"
AR2024_URL = "https://www.smbcgroup.com/emea/getmedia/1c52fee7-2c0d-4378-b571-bd45d5f6ea9f/PDF-Annual-report-(SMBC-BI).pdf"
AR2025_URL = "https://www.smbcgroup.com/emea/getmedia/28eec268-62ab-4d64-b597-02b7f918c767/smbcbi-annual-report-2025.pdf"
# FY2026: the year-ended-31-March-2026 accounts are not yet on SMBC BI's own EMEA archive (which still ends
# at the 2025 report); they were filed at Companies House on 21 July 2026 as a scanned, image-only PDF with
# no text layer, and were read by OCR at 250 dpi. Every figure taken from it was checked to foot.
AR2026_URL = "https://find-and-update.company-information.service.gov.uk/company/04684034/filing-history/MzUzMjU4ODMxMmFkaXF6a2N4/document?format=pdf&download=0"

# FY2014-FY2020: SMBC BI's own Companies House filing history (04684034), filed
# under its pre-Sep-2020 name "Sumitomo Mitsui Banking Corporation Europe Limited".
AR2020_URL = "https://find-and-update.company-information.service.gov.uk/company/04684034/filing-history/MzI3MzY1NDE4NmFkaXF6a2N4/document?format=pdf&download=0"
AR2019_URL = "https://find-and-update.company-information.service.gov.uk/company/04684034/filing-history/MzIzOTk1Nzc1NWFkaXF6a2N4/document?format=pdf&download=0"
AR2018_URL = "https://find-and-update.company-information.service.gov.uk/company/04684034/filing-history/MzIxMDI4NjgxOWFkaXF6a2N4/document?format=pdf&download=0"
AR2017_URL = "https://find-and-update.company-information.service.gov.uk/company/04684034/filing-history/MzE4MjA0OTM3OWFkaXF6a2N4/document?format=pdf&download=0"
AR2016_URL = "https://find-and-update.company-information.service.gov.uk/company/04684034/filing-history/MzE1MzEzNzE2MWFkaXF6a2N4/document?format=pdf&download=0"
AR2015_URL = "https://find-and-update.company-information.service.gov.uk/company/04684034/filing-history/MzEyNjg1NTk3OWFkaXF6a2N4/document?format=pdf&download=0"
AR2014_URL = "https://find-and-update.company-information.service.gov.uk/company/04684034/filing-history/MzEwMzk5NTEyM2FkaXF6a2N4/document?format=pdf&download=0"
# FY2013 (HD-072): SMBC BI's own Companies House filing history, "Full accounts made up to 31 March 2013",
# filed 04 Jul 2013.
AR2013_URL = "https://find-and-update.company-information.service.gov.uk/company/04684034/filing-history/MzA4MDk2MzYzM2FkaXF6a2N4/document?format=pdf&download=0"

P3_2021_URL = "https://www.smbcgroup.com/emea/getmedia/c956424b-468e-4f29-9650-a4c792a720c3/Pillar-3-Interim-Disclosure-March-2021-(SMBC-BI).pdf"
P3_2022_URL = "https://web.archive.org/web/20240712094621/https://www.smbcgroup.com/emea/images/SMBC/media/Notices-Reporting/Corporate%20Disclosures/smbcbi-pillar3-2022.pdf"
P3_2023_URL = "https://www.smbcgroup.com/emea/getmedia/352315cf-7a34-42d7-9cb1-3082d16539f3/Pillar-3-Interim-Disclosure-March-2023-(SMBC-BI).pdf"
P3_2024_URL = "https://www.smbcgroup.com/emea/getmedia/7690b9ee-bae2-4fc1-bba5-0422a250f84c/Pillar-3-Interim-Disclosure-March-2024-(SMBC-BI).pdf"
P3_2026_URL = "https://www.smbcgroup.com/emea/getmedia/0af76b74-dc6f-4e12-abb8-e87fa2855a03/SMBC_Bank_3-Pillar-Disclosures_260707_Master-v2.pdf"
P3_2025_URL = "https://www.smbcgroup.com/emea/getmedia/2418d0a0-de22-497a-9a9a-4ca69ade9f94/Pillar-3-annual-disclosure-(SMBC-BI-%E2%80%93-31-March-2025).pdf"

# FY2014-FY2020 Pillar 3 disclosures: no longer hosted live on smbcgroup.com -
# retrieved via the Wayback Machine from smbcgroup.com's own disclosures archive.
P3_2020_URL = "https://web.archive.org/web/20240527071545/https://www.smbcgroup.com/emea/images/SMBC/media/SMBC/pdf/disclosures/smbce-pillar3-2020.pdf"
P3_2019_URL = "https://web.archive.org/web/20240527071944/https://www.smbcgroup.com/emea/images/SMBC/media/SMBC/pdf/disclosures/smbce-pillar3-2019.pdf"
P3_2018_URL = "https://web.archive.org/web/20240527071821/https://www.smbcgroup.com/emea/images/SMBC/media/SMBC/pdf/disclosures/smbce-pillar3-20180331.pdf"
P3_2017_URL = "https://web.archive.org/web/20230330205458/https://www.smbcgroup.com/emea/images/SMBC/media/SMBC/pdf/disclosures/pillar3disclosures310317.pdf"
P3_2016_URL = "https://web.archive.org/web/20240527070848/https://www.smbcgroup.com/emea/images/SMBC/media/SMBC/pdf/disclosures/pillar3disclosures310316.pdf"
P3_2015_URL = "https://web.archive.org/web/20240527065243/https://www.smbcgroup.com/emea/images/SMBC/media/SMBC/pdf/disclosures/pillar3-31-03-15.pdf"
P3_2014_URL = "https://web.archive.org/web/20240701160935/https://www.smbcgroup.com/emea/images/SMBC/media/SMBC/pdf/disclosures/pillar3-31mar14.pdf"

# ---------------------------------------------------------------
# FX conversion: GBP-per-1-USD is NOT what these are - these are GBP/USD
# quotes in the market convention "£1 = $X" (Bank of England spot rate,
# sterling into US dollar). To convert a $ amount to £: gbp = usd / rate.
# Source: Bank of England daily reference rates, via poundsterlinglive.com's
# published archive of the official BoE series
# (https://www.poundsterlinglive.com/bank-of-england-spot/historical-spot-exchange-rates/gbp/GBP-to-USD-<year>).
# "period_end" = spot rate on the fiscal year-end date (31 March each year;
# FY2021's *opening* balance needs 31 Mar 2020's rate too, included below).
# "average" = simple arithmetic mean of the 12 month-end spot rates falling
# within that fiscal year (1 April - 31 March) - a standard simplified proxy
# for a true daily average, used because the source's daily series does not
# expose a ready-made period-average figure.
FX_RATES = {
    # 31 Mar 2012 only - needed for the Statement of Changes in Equity's "Balance at 1 April 2012" opening
    # (HD-072). Source: BoE spot rate archive, last business day before the date - 30 Mar 2012 (31 Mar 2012 was
    # a Saturday).
    "FY2012": {"period_end": 1.5981},
    # HD-072: "average" added when FY2013 was extended in as its own year column - simple mean of the 12
    # month-end spot rates 30 Apr 2012 through 28 Mar 2013 (28 Mar was the last business day before Easter;
    # 29-31 Mar 2013 had no BoE rate published), per the same methodology as every other year below.
    "FY2013": {"period_end": 1.5181, "average": 1.5795},
    "FY2014": {"period_end": 1.6673, "average": 1.5964},
    "FY2015": {"period_end": 1.4847, "average": 1.6087},
    "FY2016": {"period_end": 1.4378, "average": 1.5023},
    "FY2017": {"period_end": 1.2507, "average": 1.3046},
    "FY2018": {"period_end": 1.4033, "average": 1.3390},
    "FY2019": {"period_end": 1.3030, "average": 1.3102},
    "FY2020": {"period_end": 1.2403, "average": 1.2713},
    "FY2021": {"period_end": 1.3796, "average": 1.3193},
    "FY2022": {"period_end": 1.3162, "average": 1.3617},
    "FY2023": {"period_end": 1.2364, "average": 1.2043},
    "FY2024": {"period_end": 1.2632, "average": 1.2581},
    "FY2025": {"period_end": 1.2910, "average": 1.2775},
    # FY2026 (HD/FY2026 extension, 2026-09-15): taken directly from the Bank of England's own
    # IADB series XUDLUSS (spot US$ into sterling) rather than poundsterlinglive.com's republication
    # of it, which was the stated source for earlier years. Re-deriving FY2025 from XUDLUSS by the
    # same method reproduces its period_end of 1.2910 exactly and its average as 1.2776 against the
    # 1.2775 recorded above - a 0.0001 difference that confirms the methodology matches.
    "FY2026": {"period_end": 1.3188, "average": 1.3411},
}
PRIOR_YEAR = {
    "FY2013": "FY2012",
    "FY2014": "FY2013", "FY2015": "FY2014", "FY2016": "FY2015", "FY2017": "FY2016", "FY2018": "FY2017",
    "FY2019": "FY2018", "FY2020": "FY2019", "FY2021": "FY2020", "FY2022": "FY2021", "FY2023": "FY2022",
    "FY2024": "FY2023", "FY2025": "FY2024", "FY2026": "FY2025",
}


def gbp_spot(usd_by_year):
    """Convert a {year: $m} dict to £m using that year's OWN period-end spot rate (stocks)."""
    return {y: round(v / FX_RATES[y]["period_end"], 1) for y, v in usd_by_year.items()}


def gbp_spot_prior(usd_by_year):
    """Convert a {year: $m} dict to £m using the PRIOR year's period-end spot rate
    (for opening cash balances, which are last year's closing balance)."""
    return {y: round(v / FX_RATES[PRIOR_YEAR[y]]["period_end"], 1) for y, v in usd_by_year.items()}


def gbp_avg(usd_by_year):
    """Convert a {year: $m} dict to £m using that year's average rate (flows)."""
    return {y: round(v / FX_RATES[y]["average"], 1) for y, v in usd_by_year.items()}


FX_NOTE = (
    "FX CONVERSION NOTE: SMBC Bank International plc reports in US Dollars (its functional currency, per its own "
    "Annual Report). This workbook converts every $ amount to £ at the user's request - conversion was necessary "
    "because every other workbook in this series is £-denominated and SMBC BI does not itself publish £ figures. "
    "Methodology: point-in-time/balance figures (capital, RWA, leverage exposure, HQLA, cash balances) use the "
    "Bank of England GBP/USD SPOT rate as at that fiscal year-end (31 March); flow figures (every cash flow "
    "statement line item) use the AVERAGE of the 12 month-end spot rates over that fiscal year (1 April-31 March), "
    "since a true daily average was not practically obtainable - both from Bank of England daily reference rates "
    "via poundsterlinglive.com's published archive. Rates used (£1 = $X): 31 Mar 2012 spot 1.5981 (FY2013 opening "
    "equity balance only); FY2013 spot 1.5181 / average 1.5795; FY2014 spot 1.6673 / average 1.5964; FY2015 spot 1.4847 / average 1.6087; FY2016 spot 1.4378 / "
    "average 1.5023; FY2017 spot 1.2507 / average 1.3046; FY2018 spot 1.4033 / average 1.3390; FY2019 spot 1.3030 "
    "/ average 1.3102; FY2020 spot 1.2403 / average 1.2713; FY2021 spot 1.3796 / average 1.3193; FY2022 spot "
    "1.3162 / average 1.3617; FY2023 spot 1.2364 / average 1.2043; FY2024 spot 1.2632 / average 1.2581; FY2025 "
    "spot 1.2910 / average 1.2775; FY2026 spot 1.3188 / average 1.3411. FY2026's two rates (added 2026-09-15) "
    "come directly from the Bank of England's own Interactive Statistical Database series XUDLUSS (spot US$ "
    "into sterling), rather than from poundsterlinglive.com's republication of the same Bank of England rates "
    "used for FY2013-FY2025 - the primary source in place of a secondary one. The methodology is unchanged and "
    "was validated against it: re-deriving FY2025 from XUDLUSS on the same basis reproduces its period-end spot "
    "of 1.2910 exactly and gives an average of 1.2776 against the 1.2775 recorded for FY2025 above, a 0.0001 "
    "difference with no material effect on any converted figure. All % ratios (CET1/"
    "Tier 1/Total Capital/Leverage/LCR/NSFR ratios) are shown EXACTLY as reported in USD and were NOT converted - "
    "a ratio is dimensionless and currency-invariant since both its numerator and denominator would move by the "
    "same factor. Because stocks and flows are converted at different rates (standard practice for translating "
    "foreign-currency financial statements), the cash flow statement includes an explicit 'Effect of GBP/USD "
    "translation' reconciling line so opening + all flows + this line = closing exactly in £ terms - this line is "
    "purely an artefact of £ translation and has no bearing on the Bank's underlying USD results."
)

ENTITY_NOTE = (
    "ENTITY NOTE: SMBC Bank International plc (SMBC BI), FRN 223304, is a wholesale bank headquartered in London "
    "and a wholly-owned subsidiary of Sumitomo Mitsui Banking Corporation (SMBC), itself part of Sumitomo Mitsui "
    "Financial Group (Japan). It was incorporated on 3 March 2003 as Sumitomo Mitsui Banking Corporation Europe "
    "Limited and renamed/re-registered as a public limited company on 30 September 2020 (per Companies House's own "
    "filing history for company 04684034: 'Certificate of change of name and re-registration from Private to "
    "Public Limited Company', 30 Sep 2020) - every FY2014-FY2020 Annual Report used in this workbook is therefore "
    "filed under the entity's former name. On 7 October 2024, SMBC BI completed a project "
    "transferring the securities business of SMBC Nikko Capital Markets Limited (a portfolio of debt securities and "
    "other fixed income assets) to itself, and opened a branch in the Abu Dhabi Global Market - this accounts for "
    "new FY2025 cash flow line items (trading portfolio assets/liabilities, repurchase agreements) not present in "
    "earlier years, and for part of the FY2025 RWA increase. Figures are on SMBC Bank International plc's own "
    "(entity-level) basis throughout, both for cash flow and Pillar 3."
)

FY2026_FOOTING_NOTE = (
    "Every FY2026 figure was checked to foot against its own statement before use: Total assets USD 77,915.9m equals the sum of the asset lines and equals Total liabilities USD 71,566.2m plus Total equity USD 6,349.7m; Net interest income, Net fee and commission income, Operating income, Net operating expenses, Profit before tax and Profit for the year each recompute exactly from their own components; and the cash flow statement's operating, investing and financing subtotals, net change, and closing cash all reconcile. Every FY2025 comparative printed in the FY2026 report reproduces this workbook's existing FY2025 figures exactly, so no prior year was restated."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are SMBC Bank International plc's own Statement of cash flows, converted from USD to "
    "£m (see FX conversion note below):\n"
    f"FY2026: SMBC BI Annual report and financial statements, year ended 31 March 2026 (Companies House filing, scanned/image-only - read by OCR at 250 dpi), p.66 (Statement of cash flows) - {AR2026_URL}. Added 2026-09-15. " + FY2026_FOOTING_NOTE + "\n"
    f"FY2025: SMBC BI Annual report and financial statements, year ended 31 March 2025, p.72 (Statement of cash "
    f"flows) - {AR2025_URL}\n"
    f"FY2024: SMBC BI Annual report and financial statements, year ended 31 March 2024, p.85 (Statement of cash "
    f"flows) - {AR2024_URL}\n"
    f"FY2023: SMBC BI Annual report and financial statements, year ended 31 March 2023, p.90 (Statement of cash "
    f"flows) - {AR2023_URL}\n"
    f"FY2022: SMBC BI Annual report and financial statements, year ended 31 March 2022, p.87 (Statement of cash "
    f"flows) - {AR2022_URL}\n"
    f"FY2021: SMBC BI Annual report & financial statements, year ended 31 March 2021, p.75 (Statement of cash "
    f"flows) - {AR2021_URL}\n"
    f"FY2020: Sumitomo Mitsui Banking Corporation Europe Limited (SMBC BI's former name - see entity note) Annual "
    f"report & financial statements, year ended 31 March 2020, p.48 (Statement of cash flows), retrieved via "
    f"Companies House filing history (co. 04684034) - {AR2020_URL}\n"
    f"FY2019: as above, year ended 31 March 2019, p.27 - {AR2019_URL}\n"
    f"FY2018: as above, year ended 31 March 2018, p.25 - {AR2018_URL}\n"
    f"FY2017: as above, year ended 31 March 2017, p.18 - {AR2017_URL}\n"
    f"FY2016: as above, year ended 31 March 2016, p.17 - {AR2016_URL}\n"
    f"FY2015: as above, year ended 31 March 2015, p.17 - {AR2015_URL}\n"
    f"FY2014: as above, year ended 31 March 2014, p.16 - {AR2014_URL}\n"
    f"FY2013 (HD-072): as above, year ended 31 March 2013, p.16 - {AR2013_URL}\n"
    "Each year's own report was used for its own column (not a restated comparative); every year's own figure was "
    "cross-checked against its appearance as the comparative column in the following year's report and matched "
    "exactly in all cases, so there are no presentation-basis restatements to flag across vintages for FY2015-2025 "
    "(only new line items appearing from FY2025 onward - see entity note). FY2013's own figures were specifically "
    "cross-checked against their appearance as the comparative column in AR2014 and matched exactly, with no "
    "restatement. Note: FY2025's operating/investing/"
    "financing subtotals sum to £1,785.5m against a directly-converted net change of £1,785.4m - a £0.1m rounding "
    "artefact from rounding each £ line independently to 1 decimal place before summing, not a data error; the "
    "full statement still ties exactly end-to-end via the net change, FX and translation-effect lines. GENUINE "
    "RESTATEMENT (FY2014 only): FY2014's own report shows 'Unrealised exchange movements' of USD 5.9m and "
    "'Changes in loans and advances to banks - others' consistent with a Derivative assets balance of USD 468.7m "
    "at 31 March 2014; FY2015's own report instead shows FY2014's comparative Derivative assets balance as USD "
    "715.3m (a USD 246.6m increase) with an identical uplift on Derivative liabilities (USD 451.5m to USD 698.1m) "
    "- a genuine derivatives grossing/netting basis change between the two reports, not a transcription error. "
    "FY2014's own originally-published basis is used here, per the general convention above; see also the "
    "Balance Sheet sheet's source note. Two rows are genuinely new-then-discontinued: 'Impairment loss written "
    "off' and 'Changes in income tax' appear as distinct reconciling lines only in FY2013-FY2016's own "
    "presentation (folded into other lines from FY2017 onward); 'Net issue of shares' appears in both FY2013 and "
    "FY2014 (a USD 800.0m ordinary share capital injection each year - see the Statement of Changes in Equity "
    "sheet); 'Repayment and cancellation of subordinated debt' appears only in FY2014 (redemption in full of the "
    "USD 800.0m Subordinated liabilities balance carried on FY2013's own balance sheet - see the Balance Sheet "
    "sheet's source note).\n\n"
    + ENTITY_NOTE + "\n\n" + FX_NOTE
)


def p3_sources(page):
    return (
        "Sources - SMBC Bank International plc's own Basel III Pillar 3 Disclosures, converted from USD to £m "
        f"where a $ amount (see FX conversion note on the Cash Flow Statement sheet; % ratios are unconverted):\n"
        f"FY2026: Table 2.1 KM1 - Key metrics, p.{page['FY2026']} - {P3_2026_URL}\n"
        f"FY2025: Table 2.1 KM1 - Key metrics, p.{page['FY2025']} - {P3_2025_URL}\n"
        f"FY2024: Table 1 KM1 - Key metrics, p.{page['FY2024']} - {P3_2024_URL}\n"
        f"FY2023: Table 1 KM1 - Key metrics, p.{page['FY2023']} - {P3_2023_URL}\n"
        f"FY2022: Table 1 KM1 Key metrics, p.{page['FY2022']} - {P3_2022_URL}\n"
        f"FY2021: 2.1 Key metrics dashboard, p.{page['FY2021']} - {P3_2021_URL}\n"
        f"FY2020: 2.1 Key metrics, p.{page['FY2020']} - {P3_2020_URL}\n"
        f"FY2019: 2.1 Key metrics, p.{page['FY2019']} - {P3_2019_URL}\n"
        f"FY2018: 2.1 Key metrics, p.{page['FY2018']} - {P3_2018_URL}\n"
        f"FY2017: 2.1 Key metrics, p.{page['FY2017']} - {P3_2017_URL}\n"
        f"FY2016: 2.1 Key metrics, p.{page['FY2016']} - {P3_2016_URL}\n"
        f"FY2015: Section 9 Capital Adequacy (pre-dates the standard KM1/'Key metrics' template introduced from the "
        f"FY2016 disclosure onward), p.{page['FY2015']} - {P3_2015_URL}\n"
        f"FY2014: Section 9 Capital Adequacy, p.{page['FY2014']} - {P3_2014_URL}"
    )


bw = BankWorkbook(bank_name="SMBC Bank International plc", years=Y_CORE, year_label={y: y for y in YEARS}, header_color="1B6B3C")

# ---------------------------------------------------------------
# Sheet: Balance Sheet (raw USD figures, converted at build time - spot rate, stocks)
# ---------------------------------------------------------------
BS_CASH = {"FY2026": 12321.1, "FY2025": 25294.6, "FY2024": 22951.2, "FY2023": 25880.0, "FY2022": 25255.4, "FY2021": 24550.4,
           "FY2020": 24726.5, "FY2019": 19670.1, "FY2018": 33655.0, "FY2017": 16559.5, "FY2016": 19559.4,
           "FY2015": 11875.2, "FY2014": 13775.6, "FY2013": 15425.1}
BS_SETTLEMENT = {"FY2026": 695.1, "FY2025": 397.9, "FY2024": 95.5, "FY2023": 115.5, "FY2022": 96.9, "FY2021": 39.2,
                 "FY2020": 4216.8, "FY2019": 131.0}
# FY2018 and earlier: "Loans and advances to banks" was reported as a single combined line (split into
# "included in cash and cash equivalents" + "other" sub-lines pre-FY2019 restatement) - combined here; see BS_SOURCES.
BS_LOANS_BANKS = {"FY2026": 7201.0, "FY2025": 3446.3, "FY2024": 3453.5, "FY2023": 3223.6, "FY2022": 3988.6, "FY2021": 3795.4,
                  "FY2020": 3802.5, "FY2019": 2914.6, "FY2018": 4368.4, "FY2017": 5469.2, "FY2016": 3641.9,
                  "FY2015": 5779.4, "FY2014": 4526.6, "FY2013": 1788.8 + 1157.1}
BS_LOANS_CUSTOMERS = {"FY2026": 13981.7, "FY2025": 19279.8, "FY2024": 18051.7, "FY2023": 17712.7, "FY2022": 19942.6, "FY2021": 20845.5,
                      "FY2020": 22722.7, "FY2019": 21484.2, "FY2018": 20394.1, "FY2017": 14962.0, "FY2016": 15571.3,
                      "FY2015": 11589.8, "FY2014": 11351.5, "FY2013": 11022.7}
BS_REVERSE_REPO = {"FY2026": 33507.9, "FY2025": 17084.1, "FY2024": 1710.4, "FY2023": 1266.9, "FY2022": 1197.9, "FY2021": 1732.7,
                   "FY2020": 1502.5, "FY2019": 1793.4}
BS_TRADING_ASSETS = {"FY2026": 2149.8, "FY2025": 1497.7}
BS_INVESTMENT_SEC = {"FY2026": 4178.6, "FY2025": 764.1, "FY2024": 668.5, "FY2023": 1045.1, "FY2022": 1009.2, "FY2021": 496.5,
                     "FY2020": 624.9, "FY2019": 426.5, "FY2018": 751.1, "FY2017": 455.3, "FY2016": 783.7,
                     "FY2015": 882.9, "FY2014": 1001.7, "FY2013": 476.1}
# Note 12 "Investment securities" breakdown by measurement basis - available FY2020-FY2025 only (see BS_SOURCES'
# INVESTMENT SECURITIES BREAKDOWN paragraph for exact note/page citations per year; FY2013-FY2019 comes from
# scanned/image-only Companies House filings with no extractable text, so no breakdown is available for those years).
# Each year's three figures sum exactly to that year's BS_INVESTMENT_SEC total above.
BS_INV_SEC_AMORTISED = {"FY2026": 0, "FY2025": 18.0, "FY2024": 10.3, "FY2023": 29.3, "FY2022": 65.4, "FY2021": 130.1,
                        "FY2020": 186.2}
BS_INV_SEC_FVOCI = {"FY2026": 4156.0, "FY2025": 724.0, "FY2024": 637.0, "FY2023": 997.0, "FY2022": 925.7, "FY2021": 354.9,
                    "FY2020": 433.4}
BS_INV_SEC_FVTPL = {"FY2026": 22.6, "FY2025": 22.1, "FY2024": 21.2, "FY2023": 18.8, "FY2022": 18.1, "FY2021": 11.5,
                    "FY2020": 5.3}
BS_DERIVATIVE_ASSETS = {"FY2026": 1914.5, "FY2025": 1757.9, "FY2024": 1973.0, "FY2023": 2085.6, "FY2022": 1430.4, "FY2021": 1255.7,
                        "FY2020": 1776.3, "FY2019": 996.0, "FY2018": 1568.2, "FY2017": 1093.6, "FY2016": 1260.9,
                        "FY2015": 1496.5, "FY2014": 468.7, "FY2013": 483.0}
BS_OTHER_ASSETS = {"FY2026": 1582.0, "FY2025": 1461.4, "FY2024": 763.8, "FY2023": 928.9, "FY2022": 696.3, "FY2021": 540.6,
                   "FY2020": 836.4, "FY2019": 481.0, "FY2018": 254.8, "FY2017": 217.2, "FY2016": 213.2,
                   "FY2015": 299.9, "FY2014": 228.0, "FY2013": 185.0}
BS_INTANGIBLES = {"FY2026": 145.3, "FY2025": 107.2, "FY2024": 70.2, "FY2023": 56.4, "FY2022": 46.7, "FY2021": 39.9,
                  "FY2020": 38.3, "FY2019": 30.0, "FY2018": 22.0, "FY2017": 16.4, "FY2016": 13.6,
                  "FY2015": 6.8, "FY2014": 6.2, "FY2013": 3.6}
BS_PPE = {"FY2026": 180.6, "FY2025": 216.2, "FY2024": 243.5, "FY2023": 254.4, "FY2022": 254.6, "FY2021": 219.1,
          "FY2020": 45.1, "FY2019": 30.4, "FY2018": 28.2, "FY2017": 16.8, "FY2016": 19.6,
          "FY2015": 12.0, "FY2014": 17.4, "FY2013": 23.4}
BS_CURRENT_TAX_ASSET = {"FY2025": 8.2, "FY2024": 5.5, "FY2023": 24.2, "FY2022": 6.0, "FY2020": 30.6, "FY2014": 2.2}
BS_DEFERRED_TAX_ASSET = {"FY2026": 18.5, "FY2025": 34.6, "FY2024": 43.7, "FY2023": 26.0, "FY2022": 32.1, "FY2021": 20.4,
                         "FY2020": 6.5, "FY2019": 6.5, "FY2018": 5.3, "FY2017": 6.9, "FY2015": 1.8, "FY2014": 8.1,
                         "FY2013": 8.4}
BS_PENSION_SURPLUS = {"FY2026": 39.8, "FY2025": 36.7, "FY2024": 33.6, "FY2023": 41.8, "FY2022": 60.4, "FY2021": 33.1,
                      "FY2020": 62.2, "FY2019": 45.6, "FY2018": 50.8, "FY2017": 41.1, "FY2016": 46.0,
                      "FY2015": 21.2, "FY2014": 3.7, "FY2013": 0.5}
BS_TOTAL_ASSETS = {"FY2026": 77915.9, "FY2025": 71386.7, "FY2024": 50064.1, "FY2023": 52661.1, "FY2022": 54017.1, "FY2021": 53568.5,
                   "FY2020": 60391.3, "FY2019": 48009.3, "FY2018": 61097.9, "FY2017": 38838.0, "FY2016": 41109.6,
                   "FY2015": 31965.5, "FY2014": 31389.7, "FY2013": 30573.7}

BS_DEPOSITS_BANKS = {"FY2026": 20657.8, "FY2025": 28933.9, "FY2024": 21151.7, "FY2023": 24989.5, "FY2022": 26376.9, "FY2021": 23826.3,
                     "FY2020": 25681.1, "FY2019": 24212.6, "FY2018": 27898.2, "FY2017": 13007.2, "FY2016": 23949.1,
                     "FY2015": 16854.8, "FY2014": 17079.8, "FY2013": 19277.4}
BS_CUSTOMER_ACCOUNTS = {"FY2026": 25394.2, "FY2025": 19678.5, "FY2024": 19829.1, "FY2023": 18669.0, "FY2022": 19754.1, "FY2021": 22319.2,
                        "FY2020": 27648.9, "FY2019": 18193.0, "FY2018": 23188.4, "FY2017": 16918.0, "FY2016": 8010.0,
                        "FY2015": 7648.4, "FY2014": 7825.3, "FY2013": 5116.3}
BS_DEBT_SECURITIES = {"FY2026": 99.4, "FY2025": 1012.0, "FY2024": 901.9, "FY2023": 1048.7, "FY2022": 976.0, "FY2021": 853.6,
                      "FY2019": 13.1, "FY2018": 4045.3, "FY2017": 3730.0, "FY2016": 4098.5, "FY2015": 2378.4,
                      "FY2014": 2375.7, "FY2013": 2240.0}
# FY2013 only: subordinated liabilities, redeemed in full during FY2014 (see the Cash Flow Statement's
# "Repayment and cancellation of subordinated debt" line) - absent from every other year's own balance sheet.
BS_SUBORDINATED = {"FY2013": 800.0}
BS_REPO_AGREEMENTS = {"FY2026": 21229.0, "FY2025": 12669.1}
BS_DERIVATIVE_LIAB = {"FY2026": 1653.5, "FY2025": 1768.1, "FY2024": 1625.2, "FY2023": 1877.3, "FY2022": 1322.6, "FY2021": 1228.8,
                      "FY2020": 1625.9, "FY2019": 870.8, "FY2018": 1621.1, "FY2017": 1036.8, "FY2016": 1177.2,
                      "FY2015": 1351.0, "FY2014": 451.5, "FY2013": 415.1}
BS_TRADING_LIAB = {"FY2026": 634.8, "FY2025": 294.3}
BS_OTHER_LIAB = {"FY2026": 1837.5, "FY2025": 1066.7, "FY2024": 938.6, "FY2023": 847.3, "FY2022": 583.7, "FY2021": 499.3,
                 "FY2020": 826.2, "FY2019": 232.8, "FY2018": 165.0, "FY2017": 204.1, "FY2016": 104.8,
                 "FY2015": 83.7, "FY2014": 100.4, "FY2013": 87.0}
BS_OTHER_PROVISIONS = {"FY2026": 25.0, "FY2025": 16.5, "FY2024": 11.0, "FY2023": 12.0, "FY2022": 34.5, "FY2021": 21.2,
                       "FY2020": 9.6, "FY2019": 5.5, "FY2018": 10.8, "FY2017": 8.4, "FY2016": 14.4,
                       "FY2015": 3.5, "FY2014": 7.8, "FY2013": 6.7}
BS_CURRENT_TAX_LIAB = {"FY2026": 15.7, "FY2021": 18.3, "FY2019": 54.7, "FY2018": 34.4, "FY2017": 18.6, "FY2016": 1.2,
                       "FY2015": 3.0, "FY2014": 23.6, "FY2013": 6.7}
BS_DEFERRED_TAX_LIAB = {"FY2026": 19.3, "FY2025": 21.2, "FY2024": 26.8, "FY2023": 27.9, "FY2022": 23.1, "FY2021": 13.2,
                        "FY2020": 22.3, "FY2019": 18.7, "FY2018": 13.5, "FY2017": 10.2, "FY2016": 3.1}
BS_TOTAL_LIABILITIES = {"FY2026": 71566.2, "FY2025": 65460.3, "FY2024": 44484.3, "FY2023": 47471.7, "FY2022": 49070.9, "FY2021": 48779.9,
                        "FY2020": 55814.0, "FY2019": 43601.2, "FY2018": 56976.7, "FY2017": 34933.3, "FY2016": 37358.3,
                        "FY2015": 28322.8, "FY2014": 27864.1, "FY2013": 27949.2}

BS_SHARE_CAPITAL = {"FY2026": 3200.1, "FY2025": 3200.1, "FY2024": 3200.1, "FY2023": 3200.1, "FY2022": 3200.1, "FY2021": 3200.1,
                    "FY2020": 3200.0, "FY2019": 3200.0, "FY2018": 3200.0, "FY2017": 3200.0, "FY2016": 3200.0,
                    "FY2015": 3200.0, "FY2014": 3200.0, "FY2013": 2400.0}
BS_OTHER_RESERVES = {"FY2026": 80.2, "FY2025": 100.1, "FY2024": 103.8, "FY2023": 110.5, "FY2022": 106.7, "FY2021": 100.9,
                     "FY2020": 103.2, "FY2019": 99.9, "FY2018": 102.5, "FY2017": 101.4, "FY2016": 102.0,
                     "FY2015": 97.8, "FY2014": 99.6, "FY2013": 93.1}
BS_RETAINED_EARNINGS = {"FY2026": 3069.4, "FY2025": 2626.2, "FY2024": 2275.9, "FY2023": 1878.8, "FY2022": 1639.4, "FY2021": 1487.6,
                        "FY2020": 1274.1, "FY2019": 1108.2, "FY2018": 818.7, "FY2017": 603.3, "FY2016": 449.3,
                        "FY2015": 344.9, "FY2014": 226.0, "FY2013": 131.4}
BS_TOTAL_EQUITY = {"FY2026": 6349.7, "FY2025": 5926.4, "FY2024": 5579.8, "FY2023": 5189.4, "FY2022": 4946.2, "FY2021": 4788.6,
                   "FY2020": 4577.3, "FY2019": 4408.1, "FY2018": 4121.2, "FY2017": 3904.7, "FY2016": 3751.3,
                   "FY2015": 3642.7, "FY2014": 3525.6, "FY2013": 2624.5}

BS_SOURCES = (
    "Sources - SMBC Bank International plc's own Statement of financial position, converted from USD to £m (see FX "
    "conversion note below):\n"
    f"FY2026: SMBC BI Annual report and financial statements, year ended 31 March 2026 (Companies House filing, "
    f"scanned/image-only - read by OCR at 250 dpi), p.64 (Statement of financial position) - {AR2026_URL}. "
    f"Added 2026-09-15. " + FY2026_FOOTING_NOTE + " The Bank's FY2026 Pillar 3 disclosure (Table 3.2 CC2) "
    f"prints Total liabilities as USD 71,566.1m against the audited Statement of financial position's "
    f"USD 71,566.2m - a 0.1m difference between the Bank's own two documents. The audited statement's figure "
    f"is used here, and it is the one that foots against the individual liability lines.\n"
    f"FY2025: SMBC BI Annual report and financial statements, year ended 31 March 2025, p.71 (Statement of financial "
    f"position) - {AR2025_URL}\n"
    f"FY2024: SMBC BI Annual report and financial statements, year ended 31 March 2024, p.83 (Statement of financial "
    f"position) - {AR2024_URL}\n"
    f"FY2023: SMBC BI Annual report and financial statements, year ended 31 March 2023, p.88 (Statement of financial "
    f"position) - {AR2023_URL}\n"
    f"FY2022: SMBC BI Annual report and financial statements, year ended 31 March 2022, p.85 (Statement of financial "
    f"position) - {AR2022_URL}\n"
    f"FY2021: SMBC BI Annual report & financial statements, year ended 31 March 2021, p.73 (Statement of financial "
    f"position) - {AR2021_URL}\n"
    f"FY2020: Sumitomo Mitsui Banking Corporation Europe Limited Annual report & financial statements, year ended "
    f"31 March 2020, p.46 - {AR2020_URL}\n"
    f"FY2019: as above, year ended 31 March 2019, p.25 - {AR2019_URL}\n"
    f"FY2018: as above, year ended 31 March 2018, p.23 - {AR2018_URL}\n"
    f"FY2017: as above, year ended 31 March 2017, p.16 - {AR2017_URL}\n"
    f"FY2016: as above, year ended 31 March 2016, p.15 - {AR2016_URL}\n"
    f"FY2015: as above, year ended 31 March 2015, p.15 - {AR2015_URL}\n"
    f"FY2014: as above, year ended 31 March 2014, p.14 - {AR2014_URL}\n"
    f"FY2013 (HD-072): as above, year ended 31 March 2013, p.14 - {AR2013_URL}\n"
    "Each year's own report was used for its own column (not a restated comparative); every year's own figure was "
    "cross-checked against its appearance as the comparative column in the following year's report and matched "
    "exactly in all cases EXCEPT FY2014 (see the genuine derivatives-basis restatement flagged on the Cash Flow "
    "Statement sheet's source note - Derivative assets/liabilities are affected) - FY2013's own figures were "
    "specifically cross-checked against their appearance as the comparative column in AR2014 and matched exactly "
    "with no restatement. Total assets ties exactly to "
    "Total liabilities + Total equity in USD every year; in GBP terms the two sides differ by up to £0.1m due to "
    "independent per-line rounding, not a data error. FY2013 is the only year with a 'Subordinated liabilities' "
    "balance (USD 800.0m, redeemed in full during FY2014 - see the Cash Flow Statement sheet). FY2025 is "
    "the first year to show Trading assets/liabilities and Repurchase agreements as separate lines (following the "
    "securities-business transfer described in the entity note) and the only year with a Deferred tax asset "
    "balance shown alongside a Current tax asset; Current tax liability appears only in FY2021 among FY2021-2025 "
    "(nil/dash in every other of those years) but also appears in FY2014-2019. PRE-FY2019 PRESENTATION: FY2018 and "
    "earlier reports combine 'Loans and advances to banks' into a single line (split pre-restatement into "
    "'included in cash and cash equivalents' + 'other' sub-lines, summed here into one Loans and advances to banks "
    "figure) and do not disclose 'Settlement balances' or 'Reverse repurchase agreements' as separate lines at all "
    "(both blank/not disclosed for FY2014-2018) - a genuine, cited presentation change introduced as at 31 March "
    "2019 per that year's own report ('Changes to the balance sheet were introduced as at 31 March 2018 as a "
    "result of the adoption of IFRS 9 on 1 April 2018'), not a data gap.\n\n"
    "INVESTMENT SECURITIES BREAKDOWN: the 'Investment securities - ...' sub-rows below the headline 'Total "
    "investment securities' line are transcribed from Note 12 'Investment securities' of each year's own Notes to "
    "the financial statements, which splits the balance by measurement basis (amortised cost / fair value through "
    "other comprehensive income (FVOCI) / fair value through profit and loss (FVTPL)):\n"
    f"FY2025: Note 12, p.108 - {AR2025_URL}\n"
    "FY2024: same FY2025 filing's own FY2024 comparative column, Note 12, p.108\n"
    f"FY2023: Note 12, p.134 - {AR2023_URL}\n"
    "FY2022: same FY2023 filing's own FY2022 comparative column, Note 12, p.134\n"
    f"FY2021: Note 12, p.120 - {AR2021_URL}\n"
    "FY2020: same FY2021 filing's own FY2020 comparative column, Note 12, p.120\n"
    "Each year's sub-rows sum exactly to that year's headline 'Total investment securities' line. No breakdown is "
    "available for FY2013-FY2019: those years' own Annual Reports are scanned/image-only Companies House filings "
    "(TIFF-derived PDFs with no extractable text layer, per Companies House filing history for company 04684034) "
    "and Note 12 in this later, text-native format was in any case only introduced following IFRS 9 adoption on "
    "1 April 2018 (see the pre-FY2019 presentation note above) - no issuer-type (e.g. UK government/sovereign vs. "
    "supranational/corporate) breakdown of Investment securities is disclosed in any year's Note 12.\n\n"
    + ENTITY_NOTE + "\n\n" + FX_NOTE
)

BS_ROWS = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and balances at central banks", gbp_spot(BS_CASH)),
    ("DATA", "Settlement balances", gbp_spot(BS_SETTLEMENT)),
    ("DATA", "Loans and advances to banks", gbp_spot(BS_LOANS_BANKS)),
    ("DATA", "Loans and advances to customers", gbp_spot(BS_LOANS_CUSTOMERS)),
    ("DATA", "Reverse repurchase agreements", gbp_spot(BS_REVERSE_REPO)),
    ("DATA", "Trading assets", gbp_spot(BS_TRADING_ASSETS)),
    ("DATA", "Total investment securities", gbp_spot(BS_INVESTMENT_SEC)),
    ("DATA", "Investment securities - Amortised cost", gbp_spot(BS_INV_SEC_AMORTISED)),
    ("DATA", "Investment securities - Fair value through other comprehensive income (FVOCI)", gbp_spot(BS_INV_SEC_FVOCI)),
    ("DATA", "Investment securities - Fair value through profit and loss (FVTPL)", gbp_spot(BS_INV_SEC_FVTPL)),
    ("DATA", "Derivative assets", gbp_spot(BS_DERIVATIVE_ASSETS)),
    ("DATA", "Other assets", gbp_spot(BS_OTHER_ASSETS)),
    ("DATA", "Intangible assets and goodwill", gbp_spot(BS_INTANGIBLES)),
    ("DATA", "Property and equipment", gbp_spot(BS_PPE)),
    ("DATA", "Current tax asset", gbp_spot(BS_CURRENT_TAX_ASSET)),
    ("DATA", "Deferred tax asset", gbp_spot(BS_DEFERRED_TAX_ASSET)),
    ("DATA", "Pensions surplus", gbp_spot(BS_PENSION_SURPLUS)),
    ("TOTAL", "Total assets", gbp_spot(BS_TOTAL_ASSETS)),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Deposits by banks", gbp_spot(BS_DEPOSITS_BANKS)),
    ("DATA", "Customer accounts", gbp_spot(BS_CUSTOMER_ACCOUNTS)),
    ("DATA", "Debt securities in issue", gbp_spot(BS_DEBT_SECURITIES)),
    ("DATA", "Subordinated liabilities (FY2013 only)", gbp_spot(BS_SUBORDINATED)),
    ("DATA", "Repurchase agreements", gbp_spot(BS_REPO_AGREEMENTS)),
    ("DATA", "Derivative liabilities", gbp_spot(BS_DERIVATIVE_LIAB)),
    ("DATA", "Trading liabilities", gbp_spot(BS_TRADING_LIAB)),
    ("DATA", "Other liabilities", gbp_spot(BS_OTHER_LIAB)),
    ("DATA", "Other provisions", gbp_spot(BS_OTHER_PROVISIONS)),
    ("DATA", "Current tax liability", gbp_spot(BS_CURRENT_TAX_LIAB)),
    ("DATA", "Deferred tax liability", gbp_spot(BS_DEFERRED_TAX_LIAB)),
    ("TOTAL", "Total liabilities", gbp_spot(BS_TOTAL_LIABILITIES)),
    ("SECTION", "Shareholders' equity", {}),
    ("DATA", "Called up share capital", gbp_spot(BS_SHARE_CAPITAL)),
    ("DATA", "Other reserves", gbp_spot(BS_OTHER_RESERVES)),
    ("DATA", "Retained earnings", gbp_spot(BS_RETAINED_EARNINGS)),
    ("TOTAL", "Total equity", gbp_spot(BS_TOTAL_EQUITY)),
    ("TOTAL", "Total liabilities and equity", gbp_spot(BS_TOTAL_ASSETS)),
]

bw.add_balance_sheet_sheet(
    title="SMBC Bank International plc — Statement of Financial Position",
    subtitle="£m, converted from USD - see source note at bottom for FX methodology and rates used.",
    rows=BS_ROWS,
    sources_text=BS_SOURCES,
    first_col_width=64,
    source_height=410,
    unit_suffix=" (£m, conv. from USD)",
    years=YEARS,
)

# ---------------------------------------------------------------
# Sheet: Profit & Loss (raw USD figures, converted at build time - average rate, flows)
# ---------------------------------------------------------------
IS_INTEREST_INCOME = {"FY2026": 3096.7, "FY2025": 2817.9, "FY2024": 2477.4, "FY2023": 1240.6, "FY2022": 468.2, "FY2021": 578.6,
                      "FY2020": 878.5, "FY2019": 836.6, "FY2018": 517.1, "FY2017": 461.8, "FY2016": 434.9,
                      "FY2015": 383.2, "FY2014": 303.5, "FY2013": 388.4}
IS_INTEREST_EXPENSE = {"FY2026": -2685.5, "FY2025": -2338.7, "FY2024": -2037.0, "FY2023": -1016.5, "FY2022": -142.5, "FY2021": -238.0,
                       "FY2020": -560.6, "FY2019": -545.1, "FY2018": -294.6, "FY2017": -183.2, "FY2016": -158.5,
                       "FY2015": -148.8, "FY2014": -111.2, "FY2013": -179.7}
IS_NET_INTEREST_INCOME = {"FY2026": 411.2, "FY2025": 479.2, "FY2024": 440.4, "FY2023": 224.1, "FY2022": 325.7, "FY2021": 340.6,
                          "FY2020": 317.9, "FY2019": 291.5, "FY2018": 222.5, "FY2017": 278.6, "FY2016": 276.4,
                          "FY2015": 234.4, "FY2014": 192.3, "FY2013": 208.7}
IS_FEES_INCOME = {"FY2026": 1060.0, "FY2025": 777.0, "FY2024": 582.0, "FY2023": 570.1, "FY2022": 518.6, "FY2021": 482.2,
                  "FY2020": 443.4, "FY2019": 400.3, "FY2018": 372.2, "FY2017": 351.6, "FY2016": 336.6,
                  "FY2015": 347.9, "FY2014": 304.2, "FY2013": 263.0}
IS_FEES_EXPENSE = {"FY2026": -138.2, "FY2025": -74.7, "FY2024": -25.9, "FY2023": -41.6, "FY2022": -49.4, "FY2021": -46.1,
                   "FY2020": -72.1, "FY2019": -54.8, "FY2018": -33.6, "FY2017": -44.5, "FY2016": -26.6,
                   "FY2015": -20.7, "FY2014": -31.5, "FY2013": -33.2}
IS_NET_FEE_INCOME = {"FY2026": 921.8, "FY2025": 702.3, "FY2024": 556.1, "FY2023": 528.5, "FY2022": 469.2, "FY2021": 436.1,
                     "FY2020": 371.3, "FY2019": 345.5, "FY2018": 338.6, "FY2017": 307.1, "FY2016": 310.0,
                     "FY2015": 327.2, "FY2014": 272.7, "FY2013": 229.8}
IS_NET_TRADING_INCOME = {"FY2026": 340.8, "FY2025": 283.0, "FY2024": 277.7, "FY2023": 261.8, "FY2022": 75.9, "FY2021": 64.3,
                         "FY2020": 154.1, "FY2019": 193.8, "FY2018": 178.0, "FY2017": 56.9, "FY2016": 28.2,
                         "FY2015": -11.6, "FY2014": 28.2, "FY2013": 21.8}
IS_LOSS_ON_DISPOSAL = {"FY2026": 43.1, "FY2025": -83.7}
IS_OPERATING_INCOME = {"FY2026": 1716.9, "FY2025": 1380.8, "FY2024": 1274.2, "FY2023": 1014.4, "FY2022": 870.8, "FY2021": 841.0,
                       "FY2020": 843.3, "FY2019": 830.8, "FY2018": 739.1, "FY2017": 642.6, "FY2016": 614.6,
                       "FY2015": 550.0, "FY2014": 493.2, "FY2013": 460.3}
IS_IMPAIRMENT = {"FY2026": -20.7, "FY2025": -28.3, "FY2024": -27.2, "FY2023": -47.7, "FY2022": -95.8, "FY2021": -8.6,
                 "FY2020": -200.3, "FY2019": -13.1, "FY2018": -36.9, "FY2017": -35.6, "FY2016": -72.6,
                 "FY2015": -36.0, "FY2014": -11.8, "FY2013": -29.2}
IS_PERSONNEL = {"FY2026": -596.7, "FY2025": -508.8, "FY2024": -424.6, "FY2023": -373.2, "FY2022": -385.2, "FY2021": -339.2,
                "FY2020": -270.7, "FY2019": -279.6, "FY2018": -267.2, "FY2017": -250.5, "FY2016": -257.9,
                "FY2015": -243.5, "FY2014": -222.5, "FY2013": -198.9}
IS_DEPRECIATION = {"FY2026": -66.7, "FY2025": -62.1, "FY2024": -55.6, "FY2023": -51.9, "FY2022": -42.7, "FY2021": -40.8,
                   "FY2020": -33.6, "FY2019": -19.9, "FY2018": -16.8, "FY2017": -15.9, "FY2016": -13.5,
                   "FY2015": -12.1, "FY2014": -10.4, "FY2013": -9.4}
IS_BANK_LEVY = {"FY2021": -0.6, "FY2020": -7.0}
IS_OTHER_EXPENSES = {"FY2026": -411.7, "FY2025": -298.0, "FY2024": -231.2, "FY2023": -201.3, "FY2022": -166.3, "FY2021": -123.6,
                     "FY2020": -120.8, "FY2019": -129.9, "FY2018": -121.0, "FY2017": -109.9, "FY2016": -130.5,
                     "FY2015": -106.0, "FY2014": -104.5, "FY2013": -100.1}
IS_NET_OPERATING_EXPENSES = {"FY2026": -1095.8, "FY2025": -897.2, "FY2024": -738.6, "FY2023": -674.1, "FY2022": -690.0, "FY2021": -512.8,
                             "FY2020": -632.4, "FY2019": -442.5, "FY2018": -441.9, "FY2017": -411.9, "FY2016": -474.5,
                             "FY2015": -397.6, "FY2014": -349.2, "FY2013": -337.6}
IS_OTHER_INCOME = {"FY2021": 4.9, "FY2020": 8.7}
IS_PROFIT_BEFORE_TAX = {"FY2026": 621.1, "FY2025": 483.6, "FY2024": 535.6, "FY2023": 340.3, "FY2022": 180.8, "FY2021": 333.1,
                        "FY2020": 219.6, "FY2019": 388.3, "FY2018": 297.2, "FY2017": 230.7, "FY2016": 140.1,
                        "FY2015": 152.4, "FY2014": 144.0, "FY2013": 122.7}
IS_TAX = {"FY2026": -179.3, "FY2025": -134.0, "FY2024": -129.3, "FY2023": -88.2, "FY2022": -48.9, "FY2021": -92.2,
          "FY2020": -66.7, "FY2019": -113.0, "FY2018": -84.0, "FY2017": -72.9, "FY2016": -41.3,
          "FY2015": -38.0, "FY2014": -39.9, "FY2013": -32.1}
IS_PROFIT_FOR_YEAR = {"FY2026": 441.8, "FY2025": 349.6, "FY2024": 406.3, "FY2023": 252.1, "FY2022": 131.9, "FY2021": 240.9,
                      "FY2020": 152.9, "FY2019": 275.3, "FY2018": 213.2, "FY2017": 157.8, "FY2016": 98.8,
                      "FY2015": 114.4, "FY2014": 104.1, "FY2013": 90.6}
IS_PROFIT_CONTINUING = {"FY2026": 369.7, "FY2025": 330.9}
IS_PROFIT_DISCONTINUED = {"FY2026": 72.1, "FY2025": 18.7}
IS_ACTUARIAL = {"FY2026": 1.4, "FY2025": 0.7, "FY2024": -9.2, "FY2023": -12.7, "FY2022": 20.0, "FY2021": -27.4,
                "FY2020": 13.0, "FY2019": -1.4, "FY2018": 2.2, "FY2017": -3.8, "FY2016": 5.6,
                "FY2015": 4.5, "FY2014": -9.5, "FY2013": 5.6}
IS_HEDGE_RESERVE_MOVE = {"FY2026": -2.5, "FY2025": -3.7, "FY2024": -6.6, "FY2023": 3.5, "FY2022": 5.6, "FY2021": -2.8,
                         "FY2020": 3.9, "FY2019": 0.0, "FY2018": -0.7, "FY2017": -0.3, "FY2016": 1.2,
                         "FY2015": -1.8, "FY2014": 7.5, "FY2013": -9.0}
IS_FV_HEDGE_MOVE = {"FY2025": 0.0, "FY2024": -0.1, "FY2023": 0.3, "FY2022": 0.2, "FY2021": 0.5,
                    "FY2020": -0.6, "FY2019": -2.6, "FY2018": 1.8, "FY2017": -0.3, "FY2016": 3.0,
                    "FY2015": 0.0, "FY2014": -1.0, "FY2013": -0.6}
IS_TAX_RATE_EFFECT = {"FY2022": -0.1}
IS_OCI_TOTAL = {"FY2026": -18.5, "FY2025": -3.0, "FY2024": -15.9, "FY2023": -8.9, "FY2022": 25.7, "FY2021": -29.7,
                "FY2020": 16.3, "FY2019": -4.0, "FY2018": 3.3, "FY2017": -4.4, "FY2016": 9.8,
                "FY2015": 2.7, "FY2014": -3.0, "FY2013": -4.0}
IS_TOTAL_COMPREHENSIVE = {"FY2026": 423.3, "FY2025": 346.6, "FY2024": 390.4, "FY2023": 243.2, "FY2022": 157.6, "FY2021": 211.2,
                          "FY2020": 169.2, "FY2019": 271.3, "FY2018": 216.5, "FY2017": 153.4, "FY2016": 108.6,
                          "FY2015": 117.1, "FY2014": 101.1, "FY2013": 86.6}

IS_SOURCES = (
    "Sources - SMBC Bank International plc's own Statement of comprehensive income, converted from USD to £m (see "
    "FX conversion note below):\n"
    f"FY2026: SMBC BI Annual report and financial statements, year ended 31 March 2026 (Companies House "
    f"filing, scanned/image-only - read by OCR at 250 dpi), p.63 (Statement of comprehensive income) - "
    f"{AR2026_URL}. Added 2026-09-15. " + FY2026_FOOTING_NOTE + "\n"
    f"FY2025: SMBC BI Annual report and financial statements, year ended 31 March 2025, p.70 (Statement of "
    f"comprehensive income) - {AR2025_URL}\n"
    f"FY2024: SMBC BI Annual report and financial statements, year ended 31 March 2024, p.82 (Statement of "
    f"comprehensive income) - {AR2024_URL}\n"
    f"FY2023: SMBC BI Annual report and financial statements, year ended 31 March 2023, p.87 (Statement of "
    f"comprehensive income) - {AR2023_URL}\n"
    f"FY2022: SMBC BI Annual report and financial statements, year ended 31 March 2022, p.84 (Statement of "
    f"comprehensive income) - {AR2022_URL}\n"
    f"FY2021: SMBC BI Annual report & financial statements, year ended 31 March 2021, p.72 (Statement of "
    f"comprehensive income) - {AR2021_URL}\n"
    f"FY2020: Sumitomo Mitsui Banking Corporation Europe Limited Annual report & financial statements, year ended "
    f"31 March 2020, p.45 - {AR2020_URL}\n"
    f"FY2019: as above, year ended 31 March 2019, p.24 - {AR2019_URL}\n"
    f"FY2018: as above, year ended 31 March 2018, p.22 - {AR2018_URL}\n"
    f"FY2017: as above, year ended 31 March 2017, p.15/16 - {AR2017_URL}\n"
    f"FY2016: as above, year ended 31 March 2016, p.14 - {AR2016_URL}\n"
    f"FY2015: as above, year ended 31 March 2015, p.14 - {AR2015_URL}\n"
    f"FY2014: as above, year ended 31 March 2014, p.13 - {AR2014_URL}\n"
    f"FY2013 (HD-072): as above, year ended 31 March 2013, p.13 - {AR2013_URL}\n"
    "Each year's own report was used for its own column (not a restated comparative); every year's own figure was "
    "cross-checked against its appearance as the comparative column in the following year's report and matched "
    "exactly (FY2013's own figures were specifically cross-checked against their appearance as the comparative "
    "column in AR2014 and matched exactly), EXCEPT: FY2021's own report shows a standalone 'Bank levy' line (USD 0.6m) separate from 'Other "
    "expenses'; AR2022's own comparative column for FY2021 instead folds the bank levy into 'Other expenses' "
    "(USD 124.2m = 123.6 + 0.6). FY2021's own originally-published split (used here) is kept, not AR2022's later "
    "combined presentation - both total the same Net operating expenses either way. Net operating expenses is a "
    "single bracket comprising impairment + personnel + depreciation + (bank levy, FY2020 and FY2021 only) + other "
    "expenses in every year's own presentation, not a separate impairment subtotal. FY2025 is the only year showing a "
    "continuing/discontinued split of Profit for the year (the October 2024 securities-business transfer and Abu "
    "Dhabi branch opening - see entity note); FY2020 and FY2021 are the only years with a separate 'Other income' "
    "line. TERMINOLOGY NOTE (FY2013-2018): the 'Movement in fair value hedge reserve' row is labelled 'Available-"
    "for-sale investments' in these years' own reports (FVOCI/'Fair value reserve' terminology was introduced only "
    "from FY2019's report following IFRS 9 adoption on 1 April 2018) - the same underlying reserve bucket, shown "
    "here under the later, consistent row label.\n\n"
    + ENTITY_NOTE + "\n\n" + FX_NOTE
)

IS_ROWS = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest income", gbp_avg(IS_INTEREST_INCOME)),
    ("DATA", "Interest expense", gbp_avg(IS_INTEREST_EXPENSE)),
    ("TOTAL", "Net interest income", gbp_avg(IS_NET_INTEREST_INCOME)),
    ("DATA", "Fees and commissions income", gbp_avg(IS_FEES_INCOME)),
    ("DATA", "Fees and commissions expense", gbp_avg(IS_FEES_EXPENSE)),
    ("TOTAL", "Net fee and commission income", gbp_avg(IS_NET_FEE_INCOME)),
    ("DATA", "Net trading income", gbp_avg(IS_NET_TRADING_INCOME)),
    ("DATA", "Net losses from disposal of financial assets at amortised cost", gbp_avg(IS_LOSS_ON_DISPOSAL)),
    ("TOTAL", "Operating income", gbp_avg(IS_OPERATING_INCOME)),
    ("SECTION", "Net operating expenses", {}),
    ("DATA", "Net impairment loss on financial assets", gbp_avg(IS_IMPAIRMENT)),
    ("DATA", "Personnel expenses", gbp_avg(IS_PERSONNEL)),
    ("DATA", "Depreciation and amortisation", gbp_avg(IS_DEPRECIATION)),
    ("DATA", "Bank levy", gbp_avg(IS_BANK_LEVY)),
    ("DATA", "Other expenses", gbp_avg(IS_OTHER_EXPENSES)),
    ("TOTAL", "Net operating expenses", gbp_avg(IS_NET_OPERATING_EXPENSES)),
    ("DATA", "Other income", gbp_avg(IS_OTHER_INCOME)),
    ("TOTAL", "Profit before income tax", gbp_avg(IS_PROFIT_BEFORE_TAX)),
    ("DATA", "Income tax charge", gbp_avg(IS_TAX)),
    ("TOTAL", "Profit for the year", gbp_avg(IS_PROFIT_FOR_YEAR)),
    ("DATA", "Profit from continuing operations", gbp_avg(IS_PROFIT_CONTINUING)),
    ("DATA", "Profit from discontinued operations", gbp_avg(IS_PROFIT_DISCONTINUED)),
    ("SECTION", "Other comprehensive income, net of tax", {}),
    ("DATA", "Actuarial gains/(losses) on defined benefit scheme", gbp_avg(IS_ACTUARIAL)),
    ("DATA", "Movement in cash flow hedge reserve", gbp_avg(IS_HEDGE_RESERVE_MOVE)),
    ("DATA", "Movement in fair value hedge reserve", gbp_avg(IS_FV_HEDGE_MOVE)),
    ("DATA", "Effect of changes in tax rate", gbp_avg(IS_TAX_RATE_EFFECT)),
    ("TOTAL", "Other comprehensive income, net of tax", gbp_avg(IS_OCI_TOTAL)),
    ("TOTAL", "Total comprehensive income for the year", gbp_avg(IS_TOTAL_COMPREHENSIVE)),
]

bw.add_income_statement_sheet(
    title="SMBC Bank International plc — Statement of Comprehensive Income",
    subtitle="£m, converted from USD - see source note at bottom for FX methodology and rates used.",
    rows=IS_ROWS,
    sources_text=IS_SOURCES,
    first_col_width=68,
    source_height=340,
    unit_suffix=" (£m, conv. from USD)",
    years=YEARS,
)

# ---------------------------------------------------------------
# Sheet: Statement of Changes in Equity (chronological; spot for balances, average for
# flows - both per the FX_NOTE methodology - with an explicit per-year "Effect of
# GBP/USD translation" line on the Total column bridging the two, the same convention
# already used on the Cash Flow Statement sheet for the same underlying conversion
# problem)
# ---------------------------------------------------------------
EQ_HEADERS = ["Share capital", "Retained earnings", "Capital redemption", "Hedge reserve", "Fair value reserve", "Total equity"]

EQ_SOURCES = (
    "Sources - SMBC Bank International plc's own Statement of changes in equity, converted from USD to £m (see FX "
    "conversion note below):\n"
    f"1 April 2012 opening & FY2013 movements (HD-072): Sumitomo Mitsui Banking Corporation Europe Limited (SMBC "
    f"BI's former name) Annual report & financial statements, year ended 31 March 2013, p.15 - {AR2013_URL}\n"
    f"FY2026: SMBC BI Annual report and financial statements, year ended 31 March 2026 (Companies House "
    f"filing, scanned/image-only - read by OCR at 250 dpi), p.65 (Statement of changes in equity) - "
    f"{AR2026_URL}. Added 2026-09-15. The FY2026 block's own 1 April 2025 opening row (USD 3,200.1m / "
    f"2,626.2m / 100.0m / (0.1)m / 0.2m / 5,926.4m) ties exactly to the 31 March 2025 closing row "
    f"already in this sheet, and each closing component reconciles: retained earnings 2,626.2 + 441.8 "
    f"profit + 1.4 actuarial = 3,069.4; hedge reserve (0.1) + 0.1 - 2.6 = (2.6); FVOCI reserve 0.2 - "
    f"17.4 = (17.2).\n"
    f"FY2014 movements: as above, year ended 31 March 2014, p.15 - {AR2014_URL}\n"
    f"FY2015 movements: as above, year ended 31 March 2015, p.16 - {AR2015_URL}\n"
    f"FY2016 movements: as above, year ended 31 March 2016, p.16 - {AR2016_URL}\n"
    f"FY2017 movements: as above, year ended 31 March 2017, p.17 - {AR2017_URL}\n"
    f"FY2018 movements: as above, year ended 31 March 2018, p.24 - {AR2018_URL}\n"
    f"FY2019 movements (incl. 1 April 2018 IFRS 9 transition effect): as above, year ended 31 March 2019, p.26 - "
    f"{AR2019_URL}\n"
    f"FY2020 movements: as above, year ended 31 March 2020, p.47 - {AR2020_URL}\n"
    f"1 April 2020 opening & FY2021 movements: SMBC BI Annual report & financial statements, year ended 31 March "
    f"2021, p.74 - {AR2021_URL}\n"
    f"FY2022 movements: SMBC BI Annual report and financial statements, year ended 31 March 2022, p.86 - {AR2022_URL}\n"
    f"FY2023 movements: SMBC BI Annual report and financial statements, year ended 31 March 2023, p.89 - {AR2023_URL}\n"
    f"FY2024 movements: SMBC BI Annual report and financial statements, year ended 31 March 2024, p.84 - {AR2024_URL}\n"
    f"FY2025 movements: SMBC BI Annual report and financial statements, year ended 31 March 2025, p.72 - {AR2025_URL}\n"
    "Each year's own report was used for its own movements column; every year's own closing balance was "
    "cross-checked against its appearance as the opening balance in the following year's report and matched "
    "exactly in USD (FY2013's own 'At 1 April 2012' opening and 'At 31 March 2013' closing were specifically "
    "cross-checked against AR2014's own comparative equity statement and matched exactly). GENUINE FX ARTEFACT, "
    "NOT A PLUG ROW: because Share capital/Capital redemption are static USD "
    "amounts and opening/closing balances are converted at each year's own period-end spot rate while movements "
    "are converted at that year's average rate (see FX note), a large 'Effect of GBP/USD translation' bridging "
    "line is needed on the Total column every year purely from GBP/USD rate movement - this has no bearing on the "
    "Bank's underlying USD equity position, which reconciles exactly without any such line. Individual component "
    "columns (Share capital/Retained earnings/Capital redemption/Hedge reserve/Fair value reserve) are shown "
    "directly spot/average-converted without a matching per-column translation line, so only the Total column is "
    "guaranteed to tie exactly row-to-row; components will not sum to Total's own movements exactly for this "
    "reason. 'Issue of new shares' occurs in FY2013 (USD 800.0m), FY2014 (USD 800.0m, a further injection on top "
    "of FY2013's) and FY2021 (USD 0.1m) - the three genuine (non-FX) capital transactions across all 13 years. This single "
    "'Fair value reserve' column merges what FY2014-2018's own reports called the 'Available-for-sale reserve' and "
    "what FY2019 onward calls the 'Fair value reserve'/'FVOCI reserve' (renamed following IFRS 9 adoption on 1 "
    "April 2018 - see the Profit & Loss sheet's source note) - the same underlying reserve bucket throughout. The "
    "IFRS 9 transition on 1 April 2018 also reclassified USD 2.5m from what was then a separate 'AFS Reserve' "
    "sub-column into the 'Fair Value Reserve' sub-column within FY2019's own six-column presentation; because "
    "both map to this sheet's single merged 'Fair value reserve' column, that specific reclassification nets to "
    "nil here and only the genuine USD 15.6m retained-earnings transition effect is shown.\n\n"
    + ENTITY_NOTE + "\n\n" + FX_NOTE
)

EQ_ROWS = [
    ("TOTAL", "Balance at 1 April 2012 (converted at 31 Mar 2012 spot rate)", (1001.2, 22.0, 62.6, 1.9, -0.3, 1087.5)),
    ("DATA", "Profit for the year", (None, 57.4, None, None, None, 57.4)),
    ("DATA", "Effective portion of changes in fair value", (None, None, None, -3.7, None, -3.7)),
    ("DATA", "Net gains/(losses) transferred to net profit", (None, None, None, -2.0, None, -2.0)),
    ("DATA", "Actuarial gain/(loss) on defined benefit scheme", (None, 3.5, None, None, None, 3.5)),
    ("DATA", "Change in fair value of assets classified as FVOCI", (None, None, None, None, -0.6, -0.6)),
    ("DATA", "Net gains/(losses) transferred to net profit on FVOCI", (None, None, None, None, 0.3, 0.3)),
    ("TOTAL", "Total comprehensive income for the year", (None, 60.9, None, -5.7, -0.4, 54.8)),
    ("DATA", "Issue of new shares", (506.5, None, None, None, None, 506.5)),
    ("DATA", "Effect of GBP/USD translation (£ conversion artefact - see FX note)", (None, None, None, None, None, 80.0)),
    ("TOTAL", "Balance at 31 March 2013", (1580.9, 86.6, 65.9, -3.9, -0.7, 1728.8)),
    ("DATA", "Profit for the year", (None, 65.2, None, None, None, 65.2)),
    ("DATA", "Effective portion of changes in fair value", (None, None, None, 3.7, None, 3.7)),
    ("DATA", "Net gains/(losses) transferred to net profit", (None, None, None, 1.0, None, 1.0)),
    ("DATA", "Actuarial gain/(loss) on defined benefit scheme", (None, -6.0, None, None, None, -6.0)),
    ("DATA", "Change in fair value of assets classified as FVOCI", (None, None, None, None, 0.3, 0.3)),
    ("DATA", "Net gains/(losses) transferred to net profit on FVOCI", (None, None, None, None, -0.9, -0.9)),
    ("TOTAL", "Total comprehensive income for the year", (None, 59.3, None, 4.7, -0.6, 63.3)),
    ("DATA", "Issue of new shares", (501.1, None, None, None, None, 501.1)),
    ("DATA", "Effect of GBP/USD translation (£ conversion artefact - see FX note)", (None, None, None, None, None, -178.6)),
    ("TOTAL", "Balance at 31 March 2014", (1919.3, 135.5, 60.0, 1.0, -1.2, 2114.6)),
    ("DATA", "Profit for the year", (None, 71.1, None, None, None, 71.1)),
    ("DATA", "Effective portion of changes in fair value", (None, None, None, -0.1, None, -0.1)),
    ("DATA", "Net gains/(losses) transferred to net profit", (None, None, None, -1.0, None, -1.0)),
    ("DATA", "Actuarial gain/(loss) on defined benefit scheme", (None, 2.8, None, None, None, 2.8)),
    ("DATA", "Change in fair value of assets classified as FVOCI", (None, None, None, None, -0.1, -0.1)),
    ("DATA", "Net gains/(losses) transferred to net profit on FVOCI", (None, None, None, None, 0.1, 0.1)),
    ("TOTAL", "Total comprehensive income for the year", (None, 73.9, None, -1.1, 0.0, 72.8)),
    ("DATA", "Effect of GBP/USD translation (£ conversion artefact - see FX note)", (None, None, None, None, None, 266.1)),
    ("TOTAL", "Balance at 31 March 2015", (2155.3, 232.3, 67.4, -0.1, -1.3, 2453.5)),
    ("DATA", "Profit for the year", (None, 65.8, None, None, None, 65.8)),
    ("DATA", "Effective portion of changes in fair value", (None, None, None, 0.1, None, 0.1)),
    ("DATA", "Net gains/(losses) transferred to net profit", (None, None, None, 0.7, None, 0.7)),
    ("DATA", "Actuarial gain/(loss) on defined benefit scheme", (None, 3.7, None, None, None, 3.7)),
    ("DATA", "Change in fair value of assets classified as FVOCI", (None, None, None, None, 1.6, 1.6)),
    ("DATA", "Net gains/(losses) transferred to net profit on FVOCI", (None, None, None, None, 0.4, 0.4)),
    ("TOTAL", "Total comprehensive income for the year", (None, 69.5, None, 0.8, 2.0, 72.3)),
    ("DATA", "Effect of GBP/USD translation (£ conversion artefact - see FX note)", (None, None, None, None, None, 83.3)),
    ("TOTAL", "Balance at 31 March 2016", (2225.6, 312.5, 69.6, 0.7, 0.7, 2609.1)),
    ("DATA", "Effective portion of changes in fair value", (None, None, None, 0.5, None, 0.5)),
    ("DATA", "Net gains/(losses) transferred to net profit", (None, None, None, -0.8, None, -0.8)),
    ("DATA", "Profit for the year", (None, 121.0, None, None, None, 121.0)),
    ("DATA", "Actuarial gain/(loss) on defined benefit scheme", (None, -2.9, None, None, None, -2.9)),
    ("DATA", "Change in fair value of assets classified as FVOCI", (None, None, None, None, -0.2, -0.2)),
    ("TOTAL", "Total comprehensive income for the year", (None, 118.0, None, -0.2, -0.2, 117.6)),
    ("DATA", "Effect of GBP/USD translation (£ conversion artefact - see FX note)", (None, None, None, None, None, 395.3)),
    ("TOTAL", "Balance at 31 March 2017", (2558.6, 482.4, 80.0, 0.6, 0.6, 3122.0)),
    ("DATA", "Profit for the year", (None, 159.2, None, None, None, 159.2)),
    ("DATA", "Net gains/(losses) transferred to net profit", (None, None, None, -0.5, None, -0.5)),
    ("DATA", "Actuarial gain/(loss) on defined benefit scheme", (None, 1.6, None, None, None, 1.6)),
    ("DATA", "Change in fair value of assets classified as FVOCI", (None, None, None, None, 0.9, 0.9)),
    ("DATA", "Net gains/(losses) transferred to net profit on FVOCI", (None, None, None, None, 0.4, 0.4)),
    ("TOTAL", "Total comprehensive income for the year", (None, 160.9, None, -0.5, 1.3, 161.7)),
    ("DATA", "Effect of GBP/USD translation (£ conversion artefact - see FX note)", (None, None, None, None, None, -346.9)),
    ("TOTAL", "Balance at 31 March 2018", (2280.3, 583.4, 71.3, 0.0, 1.8, 2936.8)),
    ("DATA", "Effect of changes in accounting policy (IFRS 9), net of tax", (None, 11.9, None, None, 0.0, 11.9)),
    ("TOTAL", "Balance at 1 April 2018 (restated)", (2280.3, 594.5, 71.3, 0.0, 1.8, 2947.9)),
    ("DATA", "Profit for the year", (None, 210.1, None, None, None, 210.1)),
    ("DATA", "Actuarial gain/(loss) on defined benefit scheme", (None, -1.1, None, None, None, -1.1)),
    ("DATA", "Net gains/(losses) transferred to net profit on FVOCI", (None, None, None, None, -2.0, -2.0)),
    ("TOTAL", "Total comprehensive income for the year", (None, 209.1, None, 0.0, -2.0, 207.1)),
    ("DATA", "Effect of GBP/USD translation (£ conversion artefact - see FX note)", (None, None, None, None, None, 228.0)),
    ("TOTAL", "Balance at 31 March 2019", (2455.9, 850.5, 76.7, 0.0, -0.1, 3383.0)),
    ("DATA", "Profit for the year", (None, 120.3, None, None, None, 120.3)),
    ("DATA", "Actuarial gain/(loss) on defined benefit scheme", (None, 10.2, None, None, None, 10.2)),
    ("DATA", "Effective portion of changes in fair value (cash flow hedges)", (None, None, None, 3.1, None, 3.1)),
    ("DATA", "Fair value through other comprehensive income", (None, None, None, None, -0.5, -0.5)),
    ("TOTAL", "Total comprehensive income for the year", (None, 130.5, None, 3.1, -0.5, 133.1)),
    ("DATA", "Effect of GBP/USD translation (£ conversion artefact - see FX note)", (None, None, None, None, None, 174.4)),
    ("TOTAL", "Balance at 1 April 2020 (converted at 31 Mar 2020 spot rate)", (2580.0, 1027.3, 80.6, 3.1, -0.6, 3690.5)),
    ("DATA", "Profit for the year", (None, 182.6, None, None, None, 182.6)),
    ("DATA", "Net gains/(losses) transferred to net profit", (None, None, None, -3.0, None, -3.0)),
    ("DATA", "Actuarial gain/(loss) on defined benefit scheme", (None, -20.8, None, None, None, -20.8)),
    ("DATA", "Change in fair value of assets classified as FVOCI", (None, None, None, None, 0.4, 0.4)),
    ("DATA", "Effective portion of changes in fair value", (None, None, None, 0.8, None, 0.8)),
    ("TOTAL", "Total comprehensive income for the year", (None, 161.8, None, -2.2, 0.4, 160.1)),
    ("DATA", "Issue of new shares", (0.1, None, None, None, None, 0.1)),
    ("DATA", "Effect of GBP/USD translation (£ conversion artefact - see FX note)", (None, None, None, None, None, -379.7)),
    ("TOTAL", "Balance at 31 March 2021", (2319.6, 1078.3, 72.5, 0.8, -0.1, 3471.0)),
    ("DATA", "Profit for the year", (None, 96.9, None, None, None, 96.9)),
    ("DATA", "Net gains/(losses) transferred to net profit", (None, None, None, -0.8, None, -0.8)),
    ("DATA", "Actuarial gain/(loss) on defined benefit scheme", (None, 14.7, None, None, None, 14.7)),
    ("DATA", "Change in fair value of assets classified as FVOCI", (None, None, None, None, 0.1, 0.1)),
    ("DATA", "Effective portion of changes in fair value", (None, None, None, 4.9, None, 4.9)),
    ("TOTAL", "Total comprehensive income for the year", (None, 111.6, None, 4.1, 0.1, 115.8)),
    ("DATA", "Effect of GBP/USD translation (£ conversion artefact - see FX note)", (None, None, None, None, None, 171.1)),
    ("TOTAL", "Balance at 31 March 2022", (2431.3, 1245.6, 76.0, 5.1, 0.0, 3757.9)),
    ("DATA", "Profit for the year", (None, 209.3, None, None, None, 209.3)),
    ("DATA", "Net gains/(losses) transferred to net profit", (None, None, None, -5.6, None, -5.6)),
    ("DATA", "Actuarial gain/(loss) on defined benefit scheme", (None, -10.5, None, None, None, -10.5)),
    ("DATA", "Change in fair value of assets classified as FVOCI", (None, None, None, None, 0.2, 0.2)),
    ("DATA", "Effective portion of changes in fair value", (None, None, None, 8.5, None, 8.5)),
    ("TOTAL", "Total comprehensive income for the year", (None, 198.8, None, 2.9, 0.2, 201.9)),
    ("DATA", "Effect of GBP/USD translation (£ conversion artefact - see FX note)", (None, None, None, None, None, 237.4)),
    ("TOTAL", "Balance at 31 March 2023", (2588.2, 1519.6, 80.9, 8.2, 0.2, 4197.2)),
    ("DATA", "Profit for the year", (None, 322.9, None, None, None, 322.9)),
    ("DATA", "Net gains/(losses) transferred to net profit", (None, None, None, -8.1, None, -8.1)),
    ("DATA", "Actuarial gain/(loss) on defined benefit scheme", (None, -7.3, None, None, None, -7.3)),
    ("DATA", "Effective portion of changes in fair value", (None, None, None, 2.9, -0.1, 2.8)),
    ("TOTAL", "Total comprehensive income for the year", (None, 315.6, None, -5.2, -0.1, 310.3)),
    ("DATA", "Effect of GBP/USD translation (£ conversion artefact - see FX note)", (None, None, None, None, None, -90.3)),
    ("TOTAL", "Balance at 31 March 2024", (2533.3, 1801.7, 79.2, 2.8, 0.2, 4417.2)),
    ("DATA", "Net profit for the period", (None, 273.7, None, None, None, 273.7)),
    ("DATA", "Net gains/(losses) transferred to net profit", (None, None, None, -2.8, None, -2.8)),
    ("DATA", "Actuarial gain/(loss) on defined benefit scheme", (None, 0.5, None, None, None, 0.5)),
    ("DATA", "Effective portion of changes in fair value", (None, None, None, -0.1, None, -0.1)),
    ("TOTAL", "Total comprehensive income for the year", (None, 274.2, None, -2.9, 0.0, 271.3)),
    ("DATA", "Effect of GBP/USD translation (£ conversion artefact - see FX note)", (None, None, None, None, None, -98.0)),
    ("TOTAL", "Balance at 31 March 2025", (2478.8, 2034.2, 77.5, -0.1, 0.2, 4590.5)),
    ("DATA", "Net profit for the year", (None, 329.4, None, None, None, 329.4)),
    ("DATA", "Net gains/(losses) transferred to net profit", (None, None, None, 0.1, None, 0.1)),
    ("DATA", "Actuarial gain/(loss) on defined benefit scheme", (None, 1.0, None, None, None, 1.0)),
    ("DATA", "Change in fair value of assets classified as FVOCI", (None, None, None, None, -13.0, -13.0)),
    ("DATA", "Effective portion of changes in fair value", (None, None, None, -1.9, None, -1.9)),
    ("TOTAL", "Total comprehensive income for the year", (None, 330.4, None, -1.8, -13.0, 315.6)),
    ("DATA", "Effect of GBP/USD translation (£ conversion artefact - see FX note)", (None, None, None, None, None, -91.3)),
    ("TOTAL", "Balance at 31 March 2026", (2426.5, 2327.4, 75.8, -2.0, -13.0, 4814.8)),
]

bw.add_equity_changes_sheet(
    title="SMBC Bank International plc — Statement of Changes in Equity",
    subtitle="£m, converted from USD - chronological 1 April 2012 through 31 March 2025 - see source note for FX methodology.",
    headers=EQ_HEADERS,
    rows=EQ_ROWS,
    sources_text=EQ_SOURCES,
    first_col_width=64,
    source_height=340,
)

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement (raw USD figures, converted at build time)
# ---------------------------------------------------------------
PROFIT_BEFORE_TAX = {"FY2026": 621.1, "FY2025": 483.6, "FY2024": 535.6, "FY2023": 340.3, "FY2022": 180.8, "FY2021": 333.1,
                     "FY2020": 219.6, "FY2019": 388.3, "FY2018": 297.2, "FY2017": 230.7, "FY2016": 140.1,
                     "FY2015": 152.4, "FY2014": 144.0, "FY2013": 122.7}
IMPAIRMENT_LOSS = {"FY2026": 20.7, "FY2025": 28.3, "FY2024": 27.2, "FY2023": 47.7, "FY2022": 95.8, "FY2021": 8.6,
                   "FY2020": 200.3, "FY2019": 13.1, "FY2018": 36.9, "FY2017": 35.6, "FY2016": 72.6,
                   "FY2015": 36.0, "FY2014": 11.8, "FY2013": 29.2}
LOSS_ON_DISPOSAL = {"FY2026": -43.1, "FY2025": 83.7}
# FY2013-FY2016 only: a distinct "Impairment loss written off" adjustment line not seen from FY2017 onward.
IMPAIRMENT_WRITTEN_OFF = {"FY2016": -21.9, "FY2015": -30.2, "FY2014": -122.9, "FY2013": -28.4}
UNREALISED_FX = {"FY2026": -1140.2, "FY2025": -239.2, "FY2024": -161.3, "FY2023": -1076.0, "FY2022": -1121.7, "FY2021": 1698.8,
                 "FY2020": 4.4, "FY2019": -64.2, "FY2018": -19.2, "FY2017": 29.1, "FY2016": -22.4,
                 "FY2015": -7.4, "FY2014": 5.9, "FY2013": -2.5}
DEPRECIATION = {"FY2026": 66.7, "FY2025": 62.1, "FY2024": 55.6, "FY2023": 51.9, "FY2022": 42.7, "FY2021": 40.8,
                "FY2020": 33.6, "FY2019": 19.9, "FY2018": 16.8, "FY2017": 16.0, "FY2016": 13.5,
                "FY2015": 12.1, "FY2014": 10.4, "FY2013": 9.4}
CHG_LOANS_BANKS = {"FY2026": -3760.6, "FY2025": -35.0, "FY2024": -276.4, "FY2023": 736.4, "FY2022": -197.8, "FY2021": 8.9,
                   "FY2020": -891.4, "FY2019": -428.6, "FY2018": 489.2, "FY2017": -12.1, "FY2016": -496.9,
                   "FY2015": 319.4, "FY2014": 64.0, "FY2013": 964.0}
CHG_LOANS_CUSTOMERS = {"FY2026": 5335.0, "FY2025": -1292.4, "FY2024": -321.5, "FY2023": 2255.5, "FY2022": 856.4, "FY2021": 1943.4,
                       "FY2020": -1404.4, "FY2019": -1030.5, "FY2018": -5462.0, "FY2017": 565.6, "FY2016": -4023.4,
                       "FY2015": -246.1, "FY2014": -297.5, "FY2013": -345.3}
CHG_REVERSE_REPO = {"FY2026": -16423.8, "FY2025": -15373.7, "FY2024": -443.5, "FY2023": -69.0, "FY2022": 534.8, "FY2021": -230.2,
                    "FY2020": 290.9, "FY2019": -459.8}
CHG_DERIVATIVES = {"FY2026": -271.2, "FY2025": 358.0, "FY2024": -139.5, "FY2023": -100.5, "FY2022": -80.9, "FY2021": 123.5,
                   "FY2020": -25.2, "FY2019": -178.1, "FY2018": 109.7, "FY2017": 26.9, "FY2016": 61.8,
                   "FY2015": -128.3, "FY2014": 50.7, "FY2013": -101.7}
CHG_OTHER_ASSETS = {"FY2026": -128.9, "FY2025": -698.8, "FY2024": 162.5, "FY2023": -214.0, "FY2022": -200.7, "FY2021": 341.6,
                    "FY2020": -402.6, "FY2019": 269.2, "FY2018": -45.7, "FY2017": 2.3, "FY2016": 63.7,
                    "FY2015": -83.1, "FY2014": -42.5, "FY2013": -46.0}
CHG_DEPOSITS_BANKS = {"FY2026": -8242.5, "FY2025": 7630.1, "FY2024": -4082.8, "FY2023": -1387.4, "FY2022": 2550.6, "FY2021": -1854.8,
                      "FY2020": 1468.5, "FY2019": -2723.0, "FY2018": 14891.0, "FY2017": -10941.9, "FY2016": 7094.3,
                      "FY2015": -225.0, "FY2014": -2197.6, "FY2013": 8050.1}
CHG_CUSTOMER_ACCOUNTS = {"FY2026": 5714.7, "FY2025": -149.1, "FY2024": 1157.2, "FY2023": -1085.1, "FY2022": -2565.1, "FY2021": -5329.7,
                         "FY2020": 9455.9, "FY2019": -4995.4, "FY2018": 6270.4, "FY2017": 8908.0, "FY2016": 361.6,
                         "FY2015": -176.9, "FY2014": 2709.0, "FY2013": -216.8}
# FY2013-FY2016 only: a distinct "Changes in income tax" line (separate from "Taxes paid") in these years' own presentation.
CHG_INCOME_TAX = {"FY2016": -1.8, "FY2015": -18.4, "FY2014": 16.9, "FY2013": -5.3}
CHG_OTHER_LIABILITIES = {"FY2026": 803.4, "FY2025": 145.4, "FY2024": 99.4, "FY2023": 245.9, "FY2022": 107.6, "FY2021": -324.4,
                         "FY2020": 601.1, "FY2019": -894.9, "FY2018": -33.4, "FY2017": 92.1, "FY2016": 14.0,
                         "FY2015": -16.6, "FY2014": 13.4, "FY2013": -14.1}
CHG_TRADING_ASSETS = {"FY2026": -652.1, "FY2025": -1497.7}
CHG_TRADING_LIABILITIES = {"FY2026": 340.5, "FY2025": 294.3}
CHG_REPO_BORROWING = {"FY2026": 8559.9, "FY2025": 12669.1}
TAXES_PAID = {"FY2026": -127.1, "FY2025": -130.3, "FY2024": -122.8, "FY2023": -91.6, "FY2022": -92.1, "FY2021": -50.5,
              "FY2020": -150.3, "FY2019": -92.2, "FY2018": -69.7, "FY2017": -54.4}
NET_OPERATING = {"FY2026": -9327.5, "FY2025": 2338.4, "FY2024": -3510.3, "FY2023": -350.7, "FY2022": 110.4, "FY2021": -3290.9,
                 "FY2020": 9400.4, "FY2019": -10176.2, "FY2018": 16481.2, "FY2017": -1102.1, "FY2016": 3255.2,
                 "FY2015": -412.1, "FY2014": 365.6, "FY2013": 8415.3}

PURCHASE_SECURITIES = {"FY2026": -6614.9, "FY2025": -3186.0, "FY2024": -2849.6, "FY2023": -1025.2, "FY2022": -1669.1, "FY2021": -1137.0,
                       "FY2020": -1136.1, "FY2019": -1144.5, "FY2018": -821.4, "FY2017": -878.0, "FY2016": -762.0,
                       "FY2015": -950.2, "FY2014": -936.2, "FY2013": -585.0}
PROCEEDS_SECURITIES = {"FY2026": 3170.2, "FY2025": 3107.4, "FY2024": 3217.3, "FY2023": 992.4, "FY2022": 1145.9, "FY2021": 1269.1,
                       "FY2020": 922.1, "FY2019": 1458.1, "FY2018": 542.1, "FY2017": 1178.4, "FY2016": 860.0,
                       "FY2015": 1014.5, "FY2014": 425.4, "FY2013": 526.4}
PURCHASE_INTANGIBLES = {"FY2026": -73.0, "FY2025": -65.7, "FY2024": -34.5, "FY2023": -24.5, "FY2022": -21.0, "FY2021": -20.9,
                        "FY2020": -22.4, "FY2019": -12.5, "FY2018": -15.9, "FY2017": -9.6, "FY2016": -10.3,
                        "FY2015": -4.4, "FY2014": -5.0, "FY2013": -2.1}
PROCEEDS_INTANGIBLES = {"FY2026": 0.4, "FY2021": 0.2}
PURCHASE_PPE = {"FY2026": -12.0, "FY2025": -6.6, "FY2024": -24.0, "FY2023": -37.1, "FY2022": -64.1, "FY2021": -199.1,
                "FY2020": -4.1, "FY2019": -10.8, "FY2018": -17.9, "FY2017": -5.7, "FY2016": -15.8,
                "FY2015": -2.9, "FY2014": -0.2, "FY2013": -4.8}
PROCEEDS_PPE = {"FY2026": 0.4, "FY2025": 0.5, "FY2021": 15.1, "FY2020": 6.0, "FY2019": 7.2, "FY2016": 1.6}
NET_INVESTING = {"FY2026": -3528.9, "FY2025": -150.4, "FY2024": 309.2, "FY2023": -94.4, "FY2022": -608.3, "FY2021": -72.6,
                 "FY2020": -234.5, "FY2019": 297.5, "FY2018": -313.1, "FY2017": 285.1, "FY2016": 73.5,
                 "FY2015": 57.0, "FY2014": -516.0, "FY2013": -65.5}

LEASE_PAYMENTS = {"FY2026": -17.8, "FY2025": -17.2, "FY2024": -8.3, "FY2023": -5.3, "FY2022": -18.9, "FY2021": -19.0, "FY2020": -10.6}
PROCEEDS_DEBT_SECURITIES = {"FY2026": 99.4, "FY2025": 1012.0, "FY2024": 901.9, "FY2023": 1048.7, "FY2022": 976.0, "FY2021": 853.6,
                            "FY2019": 13.1, "FY2018": 4045.3, "FY2017": 3519.1, "FY2016": 4098.5,
                            "FY2015": 2378.4, "FY2014": 2375.7, "FY2013": 2240.0}
REPAYMENT_DEBT_SECURITIES = {"FY2026": -1012.0, "FY2025": -901.9, "FY2024": -1048.7, "FY2023": -976.0, "FY2022": -853.6, "FY2021": 0,
                             "FY2020": -13.1, "FY2018": -3730.0, "FY2017": -3887.6, "FY2016": -2378.4,
                             "FY2015": -2375.7, "FY2014": -2240.0, "FY2013": -3323.7}
# FY2014 only: redemption of subordinated debt and a further ordinary share issue (on top of FY2013's own).
REPAYMENT_SUB_DEBT = {"FY2014": -800.0}
# FY2013 and FY2014 both saw a USD 800.0m ordinary share capital injection (see the Statement of Changes in
# Equity sheet) - the FY2014 injection was a further one, on top of FY2013's.
NET_ISSUE_SHARES = {"FY2014": 800.0, "FY2013": 800.0}
NET_FINANCING = {"FY2026": -930.4, "FY2025": 92.9, "FY2024": -155.1, "FY2023": 67.4, "FY2022": 103.5, "FY2021": 834.6,
                 "FY2020": -23.7, "FY2019": -4032.2, "FY2018": 315.3, "FY2017": -368.5, "FY2016": 1720.1,
                 "FY2015": 2.7, "FY2014": 135.7, "FY2013": -283.7}

NET_CHANGE = {"FY2026": -13786.8, "FY2025": 2280.9, "FY2024": -3356.2, "FY2023": -377.7, "FY2022": -394.4, "FY2021": -2528.9,
              "FY2020": 9142.2, "FY2019": -13910.9, "FY2018": 16483.4, "FY2017": -1185.5, "FY2016": 5048.8,
              "FY2015": -352.4, "FY2014": -14.7, "FY2013": 8066.1}
FX_EFFECT = {"FY2026": 1143.3, "FY2025": 214.3, "FY2024": 159.5, "FY2023": 1020.9, "FY2022": 1157.1, "FY2021": -1824.8}
CASH_BEGIN = {"FY2026": 25294.0, "FY2025": 22798.8, "FY2024": 25995.5, "FY2023": 25352.3, "FY2022": 24589.6, "FY2021": 28943.3,
              "FY2020": 19801.1, "FY2019": 33712.0, "FY2018": 20710.1, "FY2017": 21895.6, "FY2016": 16846.8,
              "FY2015": 17199.2, "FY2014": 17213.9, "FY2013": 9147.8}
CASH_END = {"FY2026": 12650.5, "FY2025": 25294.0, "FY2024": 22798.8, "FY2023": 25995.5, "FY2022": 25352.3, "FY2021": 24589.6,
            "FY2020": 28943.3, "FY2019": 19801.1, "FY2018": 37193.5, "FY2017": 20710.1, "FY2016": 21895.6,
            "FY2015": 16846.8, "FY2014": 17199.2, "FY2013": 17213.9}

# Reconciling line: with stocks at spot and flows at average, opening + net
# change (avg) + FX effect (avg) will not exactly equal closing (spot) in
# GBP terms - see FX_NOTE. This line absorbs that rate-differential exactly.
cash_begin_gbp = gbp_spot_prior(CASH_BEGIN)
cash_end_gbp = gbp_spot(CASH_END)
net_change_gbp = gbp_avg(NET_CHANGE)
fx_effect_gbp = gbp_avg(FX_EFFECT)
GBP_TRANSLATION_EFFECT = {
    # FY2014-FY2020 disclose no separate "exchange differences" line (NET_CHANGE alone bridges
    # opening/closing exactly in USD for those years) - fx_effect_gbp.get(y, 0) handles the absent key.
    y: round(cash_end_gbp[y] - cash_begin_gbp[y] - net_change_gbp[y] - fx_effect_gbp.get(y, 0), 1)
    for y in YEARS
}

rows = [
    ("SECTION", "Reconciliation of profit before tax to net cash flows from operating activities", {}),
    ("DATA", "Profit for the year before tax", gbp_avg(PROFIT_BEFORE_TAX)),
    ("DATA", "Net impairment loss on financial assets", gbp_avg(IMPAIRMENT_LOSS)),
    ("DATA", "Net losses from disposal of financial assets at amortised cost", gbp_avg(LOSS_ON_DISPOSAL)),
    ("DATA", "Unrealised exchange movements on non operating assets and liabilities", gbp_avg(UNREALISED_FX)),
    ("DATA", "Impairment loss written off (FY2013-FY2016 only)", gbp_avg(IMPAIRMENT_WRITTEN_OFF)),
    ("DATA", "Depreciation and amortisation", gbp_avg(DEPRECIATION)),
    ("SECTION", "Changes in operating assets and liabilities", {}),
    ("DATA", "Changes in loans and advances to banks", gbp_avg(CHG_LOANS_BANKS)),
    ("DATA", "Changes in loans and advances to customers", gbp_avg(CHG_LOANS_CUSTOMERS)),
    ("DATA", "Changes in reverse repurchase agreements", gbp_avg(CHG_REVERSE_REPO)),
    ("DATA", "Changes in derivative financial instruments", gbp_avg(CHG_DERIVATIVES)),
    ("DATA", "Changes in other assets", gbp_avg(CHG_OTHER_ASSETS)),
    ("DATA", "Changes in deposits by banks", gbp_avg(CHG_DEPOSITS_BANKS)),
    ("DATA", "Changes in customer accounts", gbp_avg(CHG_CUSTOMER_ACCOUNTS)),
    ("DATA", "Changes in other liabilities", gbp_avg(CHG_OTHER_LIABILITIES)),
    ("DATA", "Net decrease/(increase) in trading portfolio assets", gbp_avg(CHG_TRADING_ASSETS)),
    ("DATA", "Net increase in trading portfolio liabilities", gbp_avg(CHG_TRADING_LIABILITIES)),
    ("DATA", "Net increase in repurchase agreements and other similar secured borrowing", gbp_avg(CHG_REPO_BORROWING)),
    ("DATA", "Changes in income tax (FY2013-FY2016 only - see 'Taxes paid' for other years)", gbp_avg(CHG_INCOME_TAX)),
    ("DATA", "Taxes paid", gbp_avg(TAXES_PAID)),
    ("TOTAL", "Net cash from/(used in) operating activities", gbp_avg(NET_OPERATING)),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Purchase of investment securities", gbp_avg(PURCHASE_SECURITIES)),
    ("DATA", "Proceeds from sale or redemption of investment securities", gbp_avg(PROCEEDS_SECURITIES)),
    ("DATA", "Purchase of intangible assets", gbp_avg(PURCHASE_INTANGIBLES)),
    ("DATA", "Proceeds from the sale of intangible assets", gbp_avg(PROCEEDS_INTANGIBLES)),
    ("DATA", "Purchase of property and equipment", gbp_avg(PURCHASE_PPE)),
    ("DATA", "Proceeds from sale of property and equipment", gbp_avg(PROCEEDS_PPE)),
    ("TOTAL", "Net cash from/(used in) investing activities", gbp_avg(NET_INVESTING)),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Payment of lease liabilities", gbp_avg(LEASE_PAYMENTS)),
    ("DATA", "Proceeds from issue of debt securities", gbp_avg(PROCEEDS_DEBT_SECURITIES)),
    ("DATA", "Repayment of debt securities", gbp_avg(REPAYMENT_DEBT_SECURITIES)),
    ("DATA", "Repayment and cancellation of subordinated debt (FY2014 only)", gbp_avg(REPAYMENT_SUB_DEBT)),
    ("DATA", "Net issue of shares (FY2013-FY2014 only)", gbp_avg(NET_ISSUE_SHARES)),
    ("TOTAL", "Net cash from/(used in) financing activities", gbp_avg(NET_FINANCING)),
    ("TOTAL", "Net increase/(decrease) in cash and cash equivalents", net_change_gbp),
    ("DATA", "Exchange differences in respect of cash and cash equivalents (USD)", fx_effect_gbp),
    ("DATA", "Effect of GBP/USD translation (£ conversion artefact - see FX note)", GBP_TRANSLATION_EFFECT),
    ("DATA", "Cash and cash equivalents at start of the year", cash_begin_gbp),
    ("TOTAL", "Cash and cash equivalents at 31 March", cash_end_gbp),
]

bw.add_cash_flow_sheet(
    title="SMBC Bank International plc — Consolidated Cash Flow Statement",
    subtitle="£m, converted from USD - see source note at bottom for FX methodology and rates used.",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=76,
    source_height=340,
    unit_suffix=" (£m, conv. from USD)",
    years=YEARS,
)

# ---------------------------------------------------------------
# Sheet: Asset Quality (raw USD figures, converted at build time - spot rate, stocks)
# ---------------------------------------------------------------
AQ_STAGE1_GROSS = {"FY2026": 66680.5, "FY2025": 64247.5, "FY2024": 43096.3, "FY2023": 44409.4, "FY2022": 47598.7, "FY2021": 46288.7,
                    "FY2020": 20731.7, "FY2019": 20467.0}
AQ_STAGE2_GROSS = {"FY2026": 962.6, "FY2025": 1233.3, "FY2024": 1440.7, "FY2023": 3404.7, "FY2022": 2385.5, "FY2021": 3097.8,
                    "FY2020": 2123.1, "FY2019": 977.5}
AQ_STAGE3_GROSS = {"FY2026": 107.5, "FY2025": 164.5, "FY2024": 241.5, "FY2023": 396.7, "FY2022": 492.6, "FY2021": 526.5,
                    "FY2020": 124.6, "FY2019": 132.2}
AQ_TOTAL_GROSS = {"FY2026": 67750.6, "FY2025": 65645.3, "FY2024": 44778.5, "FY2023": 48210.8, "FY2022": 50476.8, "FY2021": 49913.0,
                   "FY2020": 22979.4, "FY2019": 21576.7}
AQ_STAGE1_IMPAIRMENT = {"FY2026": 26.1, "FY2025": 19.1, "FY2024": 14.3, "FY2023": 19.3, "FY2022": 67.3, "FY2021": 34.6,
                         "FY2020": 41.5, "FY2019": 20.4}
AQ_STAGE2_IMPAIRMENT = {"FY2026": 147.5, "FY2025": 157.3, "FY2024": 158.3, "FY2023": 211.3, "FY2022": 136.7, "FY2021": 108.2,
                         "FY2020": 164.6, "FY2019": 24.0}
AQ_STAGE3_IMPAIRMENT = {"FY2026": 19.5, "FY2025": 28.0, "FY2024": 96.0, "FY2023": 22.5, "FY2022": 45.8, "FY2021": 56.2,
                         "FY2020": 56.1, "FY2019": 51.8}
AQ_TOTAL_IMPAIRMENT = {"FY2026": 193.1, "FY2025": 204.4, "FY2024": 268.6, "FY2023": 253.1, "FY2022": 249.8, "FY2021": 199.0,
                        "FY2020": 262.2, "FY2019": 96.2}

AQ_STAGE3_PCT = {y: f"{100 * AQ_STAGE3_GROSS[y] / AQ_TOTAL_GROSS[y]:.2f}%" for y in AQ_TOTAL_GROSS}
AQ_COVERAGE_PCT = {y: f"{100 * AQ_TOTAL_IMPAIRMENT[y] / AQ_TOTAL_GROSS[y]:.2f}%" for y in AQ_TOTAL_GROSS}

# ---------------------------------------------------------------
# Legacy IAS 39 basis (FY2014-FY2018) - SMBC BI adopted IFRS 9's 3-stage ECL model only on 1 April 2018, so
# FY2014-FY2018's own Annual Reports disclose credit quality on the old "incurred loss" basis instead: gross loans
# and advances to customers by internal grading (Normal / requiring caution 7A+7B / Substandard-and-below 7R,8-10,
# the latter recognised as "Default" under CRD IV per each year's own Pillar 3 disclosure), and a Specific/
# Collective impairment provision roll-forward (Note 18) rather than a stage-by-stage ECL allowance. Not
# comparable to the IFRS 9 section above - shown in its own clearly-labelled section instead of being blended in.
LEGACY_NORMAL = {"FY2018": 19952.1, "FY2017": 14468.8, "FY2016": 14812.2, "FY2015": 11052.1, "FY2014": 11035.2}
LEGACY_CAUTION = {"FY2018": 187.2, "FY2017": 324.2, "FY2016": 603.9, "FY2015": 459.5, "FY2014": 285.4}
LEGACY_DEFAULT = {"FY2018": 142.5, "FY2017": 169.0, "FY2016": 155.2, "FY2015": 78.2, "FY2014": 30.9}
LEGACY_TOTAL_GROSS = {"FY2018": 20281.8, "FY2017": 14962.0, "FY2016": 15571.3, "FY2015": 11589.8, "FY2014": 11351.5}
LEGACY_SPECIFIC_PROVISION = {"FY2018": 110.5, "FY2017": 87.4, "FY2016": 108.3, "FY2015": 87.4, "FY2014": 96.7}
LEGACY_COLLECTIVE_PROVISION = {"FY2018": 46.0, "FY2017": 39.7, "FY2016": 58.0, "FY2015": 37.9, "FY2014": 45.0}
LEGACY_TOTAL_PROVISION = {"FY2018": 156.5, "FY2017": 127.1, "FY2016": 166.3, "FY2015": 125.3, "FY2014": 141.7}

LEGACY_DEFAULT_PCT = {y: f"{100 * LEGACY_DEFAULT[y] / LEGACY_TOTAL_GROSS[y]:.2f}%" for y in LEGACY_TOTAL_GROSS}
LEGACY_COVERAGE_PCT = {y: f"{100 * LEGACY_TOTAL_PROVISION[y] / LEGACY_TOTAL_GROSS[y]:.2f}%" for y in LEGACY_TOTAL_GROSS}

AQ_SOURCES = (
    "Sources - SMBC Bank International plc's own IFRS 9 gross exposure and impairment allowance roll-forward for "
    "financial assets at amortised cost, converted from USD to £m (see FX conversion note below):\n"
    f"FY2026: SMBC BI Annual report and financial statements, year ended 31 March 2026 (Companies House "
    f"filing, scanned/image-only - read by OCR at 250 dpi), p.81 (Note 4, Financial risk management - "
    f"movement in impairment provisions, financial assets at amortised cost) - {AR2026_URL}. Added "
    f"2026-09-15. Both FY2026 roll-forwards reconcile exactly from their own opening balances, and "
    f"those opening balances reproduce this workbook's existing FY2025 closing figures (gross "
    f"64,247.5 / 1,233.3 / 164.5 / 65,645.3; allowance 19.1 / 157.3 / 28.0 / 204.4) exactly.\n"
    f"FY2025: SMBC BI Annual report and financial statements, year ended 31 March 2025, p.87 (Note 4, Financial "
    f"risk management) - {AR2025_URL}\n"
    f"FY2024: SMBC BI Annual report and financial statements, year ended 31 March 2024, p.106 (Note 4, Financial "
    f"risk management) - {AR2024_URL}\n"
    f"FY2023: SMBC BI Annual report and financial statements, year ended 31 March 2023, p.111 (Note 4, Financial "
    f"risk management) - {AR2023_URL}\n"
    f"FY2022: SMBC BI Annual report and financial statements, year ended 31 March 2022, p.108 (Note 4, Financial "
    f"risk management) - {AR2022_URL}\n"
    f"FY2021: SMBC BI Annual report & financial statements, year ended 31 March 2021, p.95 (Note 4, Financial risk "
    f"management) - {AR2021_URL}\n"
    f"FY2020: Sumitomo Mitsui Banking Corporation Europe Limited Annual report & financial statements, year ended "
    f"31 March 2020, p.64 ('Credit quality and stage per class of financial asset') - {AR2020_URL}\n"
    f"FY2019: as above, year ended 31 March 2019, p.73 ('Credit quality and stage per class of financial asset') - {AR2019_URL}\n"
    "Each year's own report was used for its own 'Balance at end of year' column (not a restated comparative); "
    "every year's own closing balance was cross-checked against its appearance as the opening balance in the "
    "following year's report and matched exactly, EXCEPT one figure: AR2022's own text extraction of the FY2022 "
    "'Balance at end of year' Total gross exposure prints as USD 49,598.7m, which does not foot (47,598.7 + "
    "2,385.5 + 492.6 = 50,476.8) and does not match AR2023's own FY2022 opening balance of USD 50,476.8m exactly - "
    "the figure used here (USD 50,476.8m, £38,350.4m converted) is the cross-validated, footing figure, not the "
    "garbled PDF-extracted one. SCOPE NOTE: FY2025's disclosure explicitly states these balances 'relate to loans and "
    "advances to banks and customers and reverse repurchase agreements' - every other year's disclosure states "
    "the narrower 'loans and advances to banks and customers' only (no reverse repos) - a real scope widening "
    "from the October 2024 securities-business transfer (see entity note), not a presentation error. FY2019/FY2020 "
    "figures above are for 'Loans and advances to customers at amortised cost' only, matching every other year's "
    "own basis (no reverse repos existed for this bank yet in those years). 'Stage 3 as % of gross' and 'Coverage "
    "ratio' are derived credit-quality proxies (not Pillar 3-defined ratios).\n\n"
    "LEGACY IAS 39 BASIS (FY2014-FY2018): SMBC BI adopted IFRS 9 (the 3-stage ECL model the section above is built "
    "around) only on 1 April 2018 - FY2014-FY2018's own Annual Reports therefore report credit quality on an "
    "entirely different, non-comparable IAS 39 'incurred loss' basis, shown in the separate section below instead:\n"
    f"FY2018: Sumitomo Mitsui Banking Corporation Europe Limited Annual report & financial statements, year ended "
    f"31 March 2018, p.45 ('Credit quality of counterparty per class of financial assets') and p.65 (Note 18, "
    f"Impairment provisions) - {AR2018_URL}\n"
    f"FY2017: as above, year ended 31 March 2017, p.36 and Note 18 - {AR2017_URL}\n"
    f"FY2016: as above, year ended 31 March 2016, p.33 and Note 18 - {AR2016_URL}\n"
    f"FY2015: as above, year ended 31 March 2015, p.33 and Note 18 - {AR2015_URL}\n"
    f"FY2014: as above, year ended 31 March 2014, p.30 and Note 18 - {AR2014_URL}\n"
    "'Normal borrowers' (internal grades 1-6), 'Borrowers requiring caution' (grades 7A+7B, combined here), and "
    "'Substandard borrowers and below' (grades 7R, 8-10) are the Bank's own internal obligor grading tiers for "
    "loans and advances to customers - not a stage model, but 'Substandard and below' is the closest available "
    "proxy to Stage 3/credit-impaired, since the Bank's own Pillar 3 disclosures describe 7R/J7R through 8-10/J10 "
    "as meeting the regulatory 'Default' definition. Every year's own closing gross/grading figures were cross-"
    "checked against their appearance as the comparative column in the following year's report and matched "
    "exactly in every case (FY2018 vs FY2019's own report is the one exception - see IFRS 9 transition note below). "
    "'Specific'/'Collective' impairment provisions are Note 18's own roll-forward categories (individually assessed "
    "vs incurred-but-not-identified portfolio provisions) - the pre-IFRS 9 equivalent of the Stage 3/'Stage 1+2' "
    "split above, but not directly comparable to it (different recognition trigger and measurement basis). "
    "'Default as % of gross loans' and 'Coverage ratio' on this section are derived legacy-basis proxies, not "
    "directly comparable to the IFRS 9 section's 'Stage 3 as % of gross'/'Coverage ratio' rows above.\n\n"
    "IFRS 9 TRANSITION NOTE: FY2019's own report separately discloses an 'as at 1 April 2018' IFRS 9 transition-"
    "date restatement of FY2018's closing position (Stage 1/2/3 gross USD 19,313.9m/964.5m/271.5m, ECL allowance "
    "USD 16.7m/14.3m/110.4m for loans and advances to customers at amortised cost) - this is a retrospective IFRS 9 "
    "recasting of the FY2018 balance, not what FY2018's own Annual Report itself reported (which used the Specific/"
    "Collective basis shown in the legacy section), so it is not used as this workbook's FY2018 column; it is "
    "recorded here for reference only, in case a future ticket wants an IFRS-9-consistent FY2018 comparative.\n\n"
    + ENTITY_NOTE + "\n\n" + FX_NOTE
)

AQ_ROWS = [
    ("SECTION", "Gross exposure by IFRS 9 stage - financial assets at amortised cost", {}),
    ("DATA", "Stage 1: subject to 12-month ECL", gbp_spot(AQ_STAGE1_GROSS)),
    ("DATA", "Stage 2: subject to lifetime ECL, not credit-impaired", gbp_spot(AQ_STAGE2_GROSS)),
    ("DATA", "Stage 3: subject to lifetime ECL, credit-impaired", gbp_spot(AQ_STAGE3_GROSS)),
    ("TOTAL", "Total gross exposure", gbp_spot(AQ_TOTAL_GROSS)),
    ("SECTION", "Impairment allowance by IFRS 9 stage", {}),
    ("DATA", "Stage 1: subject to 12-month ECL", gbp_spot(AQ_STAGE1_IMPAIRMENT)),
    ("DATA", "Stage 2: subject to lifetime ECL, not credit-impaired", gbp_spot(AQ_STAGE2_IMPAIRMENT)),
    ("DATA", "Stage 3: subject to lifetime ECL, credit-impaired", gbp_spot(AQ_STAGE3_IMPAIRMENT)),
    ("TOTAL", "Total impairment allowance", gbp_spot(AQ_TOTAL_IMPAIRMENT)),
    ("DATA", "Stage 3 as % of gross exposure (derived)", AQ_STAGE3_PCT),
    ("DATA", "Coverage ratio (derived)", AQ_COVERAGE_PCT),
    ("SECTION", "Legacy IAS 39 basis (FY2014-FY2018 only, NOT comparable to IFRS 9 stages above) - gross loans "
                "and advances to customers by internal grading", {}),
    ("DATA", "Normal borrowers (grades 1-6)", gbp_spot(LEGACY_NORMAL)),
    ("DATA", "Borrowers requiring caution (grades 7A/7B)", gbp_spot(LEGACY_CAUTION)),
    ("DATA", "Substandard borrowers and below / Default (grades 7R, 8-10)", gbp_spot(LEGACY_DEFAULT)),
    ("TOTAL", "Total gross loans and advances to customers", gbp_spot(LEGACY_TOTAL_GROSS)),
    ("SECTION", "Legacy IAS 39 basis - impairment provisions (Note 18 roll-forward)", {}),
    ("DATA", "Specific provisions", gbp_spot(LEGACY_SPECIFIC_PROVISION)),
    ("DATA", "Collective provisions", gbp_spot(LEGACY_COLLECTIVE_PROVISION)),
    ("TOTAL", "Total impairment provisions", gbp_spot(LEGACY_TOTAL_PROVISION)),
    ("DATA", "Default as % of gross loans (derived, legacy-basis proxy for Stage 3)", LEGACY_DEFAULT_PCT),
    ("DATA", "Coverage ratio (derived, legacy basis)", LEGACY_COVERAGE_PCT),
]

bw.add_asset_quality_sheet(
    title="SMBC Bank International plc — Asset Quality",
    subtitle="£m, converted from USD - IFRS 9 stage breakdown (FY2019-FY2025) and legacy IAS 39 basis (FY2014-FY2018) - see source note for FX methodology.",
    rows=AQ_ROWS,
    sources_text=AQ_SOURCES,
    first_col_width=68,
    source_height=340,
    unit_suffix=" (£m, conv. from USD)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
CET1_CAPITAL = {"FY2026": 6168, "FY2025": 5786, "FY2024": 5477, "FY2023": 5083, "FY2022": 4887, "FY2021": 4787.9,
                "FY2020": 4583.3, "FY2019": 4320.3, "FY2018": 4036.1, "FY2017": 3817.2, "FY2016": 3685.2,
                "FY2015": 3607.9, "FY2014": 3472.5}
TIER1_CAPITAL = dict(CET1_CAPITAL)   # identical every year - no AT1 instruments
TOTAL_CAPITAL = dict(CET1_CAPITAL)   # identical every year - no Tier 2 instruments either
TOTAL_RWA = {"FY2026": 29411, "FY2025": 33891, "FY2024": 28122, "FY2023": 28579, "FY2022": 29941, "FY2021": 28662.1,
             "FY2020": 28958.3, "FY2019": 23357.1, "FY2018": 24087.4, "FY2017": 18277.5, "FY2016": 20041.1,
             "FY2015": 14520.4, "FY2014": 15027.4}
LEV_EXPOSURE = {"FY2026": 73939, "FY2025": 57267, "FY2024": 37072, "FY2023": 36713, "FY2022": 39509, "FY2021": 62531.4,
                "FY2020": 67858.7, "FY2019": 56691.0, "FY2018": 70312.4, "FY2017": 45662.0, "FY2016": 51919.0,
                "FY2015": 37242.9, "FY2014": 43594.0}
# LCR: not disclosed in SMBC BI's own FY2014 report (pre-dates the EU LCR requirement, phased in from Oct 2015);
# FY2015's figure is sourced from the FY2016 report's own comparative column (FY2015's own report pre-dates the
# standard KM1-style disclosure template - see p3_sources()).
LCR_HQLA = {"FY2026": 29498, "FY2025": 25359, "FY2024": 25071, "FY2023": 27770, "FY2022": 27160, "FY2021": 25266.0,
            "FY2020": 25678.8, "FY2019": 20726.6, "FY2018": 35672.0, "FY2017": 18351.6, "FY2016": 20815.8,
            "FY2015": 15643.7}
LCR_OUTFLOWS = {"FY2026": 19053, "FY2025": 15835, "FY2024": 16110, "FY2023": 19094, "FY2022": 20036, "FY2021": 17426.3,
                "FY2020": 20351.9, "FY2019": 14661.3, "FY2018": 26101.6, "FY2017": 14024.0, "FY2016": 21388.4,
                "FY2015": 13585.4}
# NSFR: first appears in SMBC BI's own disclosures with the FY2018 report (showing FY2018 and FY2017); not
# disclosed at all for FY2014-FY2016.
NSFR_ASF = {"FY2026": 25902, "FY2025": 22673, "FY2024": 23986, "FY2023": 23984, "FY2022": 23643, "FY2021": 27000.0,
            "FY2020": 23740.4, "FY2019": 21494.1, "FY2018": 20366.0, "FY2017": 13875.3}
NSFR_RSF = {"FY2026": 19511, "FY2025": 17827, "FY2024": 16912, "FY2023": 16839, "FY2022": 17713, "FY2021": 19923.0,
            "FY2020": 22064.3, "FY2019": 19450.2, "FY2018": 19797.9, "FY2017": 14438.4}

RATIO_PAGES = {"FY2026": "4-5", "FY2025": "5-6", "FY2024": "5-6", "FY2023": "7-8", "FY2022": "6-7", "FY2021": "6",
               "FY2020": "6", "FY2019": "6", "FY2018": "6", "FY2017": "6", "FY2016": "6",
               "FY2015": "24", "FY2014": "31"}


def metric(name, unit, rows_data, note=None):
    bw.add_metric_sheet(name, f"SMBC BI basis, {unit}" if unit else "SMBC BI basis",
                         rows_data, p3_sources(RATIO_PAGES), note=note,
                         first_col_width=46, source_height=130)


metric("CET1 Capital", "£m (conv. from USD)", [("Common Equity Tier 1 (CET1) capital", gbp_spot(CET1_CAPITAL))])

metric("CET1 Ratio", "% of RWA", [
    ("Common Equity Tier 1 (CET1) ratio", {"FY2026": "21.0%", "FY2025": "17.1%", "FY2024": "19.5%", "FY2023": "17.8%", "FY2022": "16.3%", "FY2021": "16.7%",
                                            "FY2020": "15.8%", "FY2019": "18.5%", "FY2018": "16.8%", "FY2017": "20.9%", "FY2016": "18.4%",
                                            "FY2015": "24.8%", "FY2014": "22.9%"}),
])

metric("Tier 1 Capital", "£m (conv. from USD)", [("Tier 1 capital", gbp_spot(TIER1_CAPITAL))],
       note="Equal to CET1 capital in every year shown - SMBC BI holds no Additional Tier 1 (AT1) instruments.")

metric("Tier 1 Ratio", "% of RWA", [
    ("Tier 1 ratio", {"FY2026": "21.0%", "FY2025": "17.1%", "FY2024": "19.5%", "FY2023": "17.8%", "FY2022": "16.3%", "FY2021": "16.7%",
                      "FY2020": "15.8%", "FY2019": "18.5%", "FY2018": "16.8%", "FY2017": "20.9%", "FY2016": "18.4%",
                      "FY2015": "24.8%", "FY2014": "22.9%"}),
])

metric("Total Capital", "£m (conv. from USD)", [("Total capital", gbp_spot(TOTAL_CAPITAL))],
       note="Equal to CET1/Tier 1 capital in every year shown - SMBC BI holds no Tier 2 instruments either.")

metric("Total Capital Ratio", "% of RWA", [
    ("Total capital ratio", {"FY2026": "21.0%", "FY2025": "17.1%", "FY2024": "19.5%", "FY2023": "17.8%", "FY2022": "16.3%", "FY2021": "16.7%",
                             "FY2020": "15.8%", "FY2019": "18.5%", "FY2018": "16.8%", "FY2017": "20.9%", "FY2016": "18.4%",
                             "FY2015": "24.8%", "FY2014": "22.9%"}),
])

metric("Total RWAs", "£m (conv. from USD)", [("Total risk weighted exposure amount", gbp_spot(TOTAL_RWA))])

# ---------------------------------------------------------------
# Sheet: RWA Breakdown (raw USD figures, converted at build time - spot rate, stocks)
# ---------------------------------------------------------------
RWA_CREDIT_RISK = {"FY2026": 20790, "FY2025": 27889, "FY2024": 24153, "FY2023": 24625, "FY2022": 26391, "FY2021": 25576,
                    "FY2020": 27032.5, "FY2019": 21730.0, "FY2018": 22348.8, "FY2017": 16868.8, "FY2016": 18636.3,
                    "FY2015": 13472.5, "FY2014": 14048.1}
# CCR is not separately broken out in SMBC BI's own Pillar 3 disclosures until the CRR2-era OV1 template first
# appears in FY2021 - for FY2014-FY2020 it is embedded within the single "credit risk" capital requirement figure
# (RWA_CREDIT_RISK above), which is why RWA_CCR has no FY2014-FY2020 keys (blank, not zero) - see RWA_SOURCES.
RWA_CCR = {"FY2026": 2163, "FY2025": 1841, "FY2024": 1759, "FY2023": 1742, "FY2022": 1303, "FY2021": 750}
RWA_MARKET_RISK = {"FY2026": 3412, "FY2025": 1818, "FY2024": 195, "FY2023": 466, "FY2022": 610, "FY2021": 723,
                    "FY2020": 372.5, "FY2019": 198.8, "FY2018": 426.3, "FY2017": 172.5, "FY2016": 216.3,
                    "FY2015": 176.3, "FY2014": 210.9}
RWA_OPERATIONAL_RISK = {"FY2026": 2796, "FY2025": 2343, "FY2024": 2016, "FY2023": 1745, "FY2022": 1637, "FY2021": 1613,
                         "FY2020": 1552.5, "FY2019": 1427.5, "FY2018": 1312.5, "FY2017": 1236.3, "FY2016": 1188.8,
                         "FY2015": 871.3, "FY2014": 768.4}
RWA_MEMO_BELOW_THRESHOLD = {"FY2026": 46, "FY2025": 99, "FY2024": 117, "FY2023": 65, "FY2022": 80, "FY2021": 52}

RWA_SOURCES = (
    "Sources - SMBC Bank International plc's own Basel III Pillar 3 Disclosures, Table OV1 - Overview of risk "
    "weighted exposure amounts, converted from USD to £m (see FX conversion note below):\n"
    f"FY2026: Table 4.1 OV1, p.9 - {P3_2026_URL}\n"
    f"FY2025: Table 4.1 OV1, p.9 - {P3_2025_URL}\n"
    f"FY2024: Table 5 OV1, p.9 - {P3_2024_URL}\n"
    f"FY2023: Table 5 OV1, p.11 - {P3_2023_URL}\n"
    f"FY2022: Table 5 OV1, p.10 - {P3_2022_URL}\n"
    f"FY2021: Table 5 OV1, p.10 (FY2021's own column of the FY2022 Pillar 3 report - no standalone OV1 table is "
    f"published in the March 2021 interim disclosure itself) - {P3_2022_URL}\n"
    f"FY2020: Sections 9.3/9.4 Pillar 1 overview & Capital adequacy ratio & capital requirements, pp.34-35 - {P3_2020_URL}\n"
    f"FY2019: Section 9 Capital Adequacy, pp.6-7 - {P3_2019_URL}\n"
    f"FY2018: Section 9 Capital Adequacy, pp.6-7 - {P3_2018_URL}\n"
    f"FY2017: Section 9 Capital Adequacy, p.6 - {P3_2017_URL}\n"
    f"FY2016: Section 9.3/9.4 Capital Adequacy, pp.6-7 - {P3_2016_URL}\n"
    f"FY2015: Sections 9.1-9.3 Capital Adequacy, pp.24-25 - {P3_2015_URL}\n"
    f"FY2014: Sections 9.1-9.4 Capital Adequacy, pp.30-31 - {P3_2014_URL}\n"
    "Each year's own figure was cross-checked against its appearance as the comparative column in the following "
    "year's report and matched exactly in every case. FY2024 and FY2023 each have a genuine £1m/USD1m rounding "
    "gap between the sum of the four category rows and the Total (each line independently rounded to the nearest "
    "USD million in the source table itself) - not a data error; FY2025, FY2022 and FY2021 sum exactly. 'Memo: "
    "amounts below thresholds for deduction' is an information-only line excluded from the Total per the source "
    "template's own footnote, not summed into RWAs. Settlement risk (FY2025 only, USD 0.1m) and 'exposures to a "
    "CCP'/large exposures sub-lines (nil or immaterial in every year) are omitted as separate rows for brevity.\n\n"
    "FY2026 FOOTING GAP (added 2026-09-15): FY2026 is the one year where the source OV1 table does NOT foot. "
    "Its disclosed category rows - Credit risk excluding CCR USD 20,790m, CCR USD 2,163m, settlement risk USD "
    "0.5m, market risk USD 3,412m and operational risk USD 2,796m - sum to USD 29,161.5m against a disclosed "
    "Total of USD 29,411m, a gap of USD 249.5m (0.8% of the Total). This is not a rounding artefact and not a "
    "transcription error: every individual row in the source table ties exactly to its own 8% own-funds "
    "requirement (20,790 x 8% = 1,663; 2,163 x 8% = 173; 3,412 x 8% = 273; 2,796 x 8% = 224), as does the "
    "Total (29,411 x 8% = 2,353), and the own-funds column shows the same USD 20m gap that USD 249.5m implies "
    "at 12.5x. The published table contains no securitisation or other row that would bridge it. Per this "
    "workbook's standing convention the disclosed Total is used for the TOTAL row and the gap is left visible "
    "rather than plugged into any category. The FY2025 comparative column of the same FY2026 table reproduces "
    "this workbook's existing FY2025 figures exactly and does foot.\n\n"
    "FY2014-FY2020 METHODOLOGY: none of these years' Pillar 3 disclosures contain a CRR2-style OV1 template (that "
    "first appears with FY2021's disclosure) - instead each year discloses capital REQUIREMENTS by risk category "
    "(Section 9, 'Capital adequacy ratio & capital requirements' or equivalent). RWA-by-category for these years is "
    "therefore derived as capital requirement x 12.5 (the inverse of the standard 8% minimum capital ratio), cross- "
    "checked against each year's own disclosed Total RWA - small (0.1-0.8 £m/USDm, well under 1%) footing gaps are "
    "a rounding artefact of each underlying capital-requirement line being independently rounded in the source "
    "table, not a data error, consistent with the same pattern seen in FY2023/FY2024. Counterparty credit risk "
    "(CCR) is not separately broken out in any of these years' capital-requirement tables and is embedded within "
    "the single credit risk figure used for RWA_CREDIT_RISK - RWA_CCR is therefore left blank (not zero) for "
    "FY2014-FY2020, and the 'Memo: amounts below thresholds' line is likewise not disclosed pre-FY2021 and left "
    "blank. FY2014 is a special case: its own report's Section 9.1 'Total Credit Risk Capital Required' "
    "(USD 1,140.748k) includes a Credit Valuation Adjustment (CVA) component that its own Section 9.4 capital-"
    "requirement bridge ('8% of credit risk-weighted assets', USD 1,123.848k) excludes - the Section 9.4 bridge "
    "figure is used here because it is the one that reconciles exactly (together with Market and Operational risk) "
    "to FY2014's own disclosed Total capital requirements (USD 1,202.190k) and hence to TOTAL_RWA; using the "
    "Section 9.1 figure instead would overstate credit risk RWA by roughly USD 210m with no corresponding change "
    "to the Total. FY2015-FY2020 do not exhibit this discrepancy (their own CVA lines already reconcile within the "
    "single credit risk figure).\n\n"
    + ENTITY_NOTE + "\n\n" + FX_NOTE
)

RWA_ROWS = [
    ("DATA", "Credit risk (excluding CCR)", gbp_spot(RWA_CREDIT_RISK)),
    ("DATA", "Counterparty credit risk (CCR)", gbp_spot(RWA_CCR)),
    ("DATA", "Position, foreign exchange and commodities risks (market risk)", gbp_spot(RWA_MARKET_RISK)),
    ("DATA", "Operational risk", gbp_spot(RWA_OPERATIONAL_RISK)),
    ("TOTAL", "Total risk weighted exposure amount", gbp_spot(TOTAL_RWA)),
    ("DATA", "Memo: amounts below thresholds for deduction (not summed into Total)", gbp_spot(RWA_MEMO_BELOW_THRESHOLD)),
]

bw.add_rwa_breakdown_sheet(
    title="SMBC Bank International plc — RWA Breakdown",
    subtitle="£m, converted from USD - UK OV1 Overview of risk weighted exposure amounts - see source note for FX methodology.",
    rows=RWA_ROWS,
    sources_text=RWA_SOURCES,
    first_col_width=66,
    source_height=340,
    unit_suffix=" (£m, conv. from USD)",
)

metric("Leverage Ratio", "£m (conv. from USD) / %", [
    ("Total exposure measure excluding claims on central banks", gbp_spot(LEV_EXPOSURE)),
    ("Leverage ratio excluding claims on central banks (%)", {"FY2026": "8.3%", "FY2025": "10.1%", "FY2024": "14.8%", "FY2023": "13.8%", "FY2022": "12.4%", "FY2021": "7.7%",
                                                               "FY2020": "6.8%", "FY2019": "7.6%", "FY2018": "5.8%", "FY2017": "8.4%", "FY2016": "7.1%",
                                                               "FY2015": "9.7%", "FY2014": "7.7%"}),
    ("Leverage ratio including claims on central banks (%)", {"FY2026": "7.2%", "FY2025": "7.0%", "FY2024": "9.2%", "FY2023": "8.2%"}),
], note="FY2021 and FY2022 disclosed a single Basel III leverage ratio (7.7% / 12.4%) that does NOT exclude central "
        "bank claims - the 'excluding claims on central banks' UK framework was introduced only from the FY2022 "
        "report onward per that report's own commentary ('this was primarily due to the exclusion of qualifying "
        "claims on central banks from the leverage ratio exposures under the UK leverage ratio framework'). FY2021's "
        "and FY2022's figures are shown on the 'excluding' row for continuity, but are not on a like-for-like basis "
        "with FY2023 onward; no 'including claims on central banks' variant is separately disclosed for those two "
        "years. FY2014-FY2020 all predate the UK framework entirely and disclose only a single (CRR, pre-Brexit) "
        "'end of quarter leverage ratio' with no central-bank-claims carve-out at all - shown on the 'excluding' row "
        "for continuity but not like-for-like with any other year. FY2014 and FY2015 also separately disclose a "
        "'leverage ratio (average of the monthly leverage ratios over the quarter)' variant (7.7%/9.1% and 9.7%/9.1% "
        "respectively) not shown here, to keep this row consistent with the 'end of quarter' basis used everywhere "
        "else in the workbook.")

metric("LCR", "£m (conv. from USD) / %", [
    ("Total high quality liquid assets (HQLA), weighted value (average)", gbp_spot(LCR_HQLA)),
    ("Total net cash outflows (adjusted value)", gbp_spot(LCR_OUTFLOWS)),
    ("Liquidity coverage ratio (%)", {"FY2026": "154.8%", "FY2025": "160.1%", "FY2024": "155.6%", "FY2023": "145.4%", "FY2022": "136%", "FY2021": "145.0%",
                                      "FY2020": "126.2%", "FY2019": "141.4%", "FY2018": "133.4%", "FY2017": "125.5%", "FY2016": "97.3%",
                                      "FY2015": "115.2%"}),
], note="FY2014 predates the EU LCR requirement (phased in for UK banks from October 2015) and is not disclosed - "
        "left blank rather than estimated.")

metric("NSFR", "£m (conv. from USD) / %", [
    ("Total available stable funding", gbp_spot(NSFR_ASF)),
    ("Total required stable funding", gbp_spot(NSFR_RSF)),
    ("NSFR ratio (%)", {"FY2026": "132.8%", "FY2025": "127.2%", "FY2024": "141.8%", "FY2023": "142.4%", "FY2022": "133.5%", "FY2021": "135.5%",
                        "FY2020": "107.6%", "FY2019": "110.5%", "FY2018": "102.9%", "FY2017": "96.1%"}),
], note="NSFR first appears in SMBC BI's own Pillar 3 disclosures with the FY2018 report (showing FY2018 and its "
        "FY2017 comparative); not disclosed at all for FY2014-FY2016 - left blank rather than estimated.")

bw.add_not_disclosed_metric_sheets(
    ["MREL Ratio"],
    p3_sources(RATIO_PAGES),
    per_note={"MREL Ratio": "No MREL disclosure of any kind (numeric or qualitative) appears in any of the 12 "
                             "years' Pillar 3 disclosures (FY2014-FY2026) - SMBC BI does not appear to be subject "
                             "to a disclosed MREL requirement."},
)

# ---------------------------------------------------------------
# Interim Pillar 3 disclosures
# ---------------------------------------------------------------
# SMBC BI's financial year ends in March.  The official EMEA archive provides
# entity-level KM1 disclosures for June, September and December 2022-2025;
# March is the annual reporting point already represented by the metric sheets
# above.  Values below remain in SMBC BI's native USD millions because the
# interim source documents do not provide a defensible common GBP conversion
# basis for the three month-end dates.  Annual sheets retain their established
# GBP conversion methodology.
INTERIM_PERIODS = [
    ("2025 Q4", "Q4", "SMBC-BI-Pillar-3-Dec-25-v3.pdf", "Table 1: KM1, PDF p.5",
     "https://www.smbcgroup.com/emea/getmedia/0d5f0926-6436-48ef-a708-377fa7898591/SMBC-BI-Pillar-3-Dec-25-v3.pdf"),
    ("2025 Q3", "Q3", "SMBC-BI-Pillar-3-Sept-25.pdf", "Table 2.1: KM1, PDF p.5",
     "https://www.smbcgroup.com/emea/getmedia/bd6c0013-d139-4ba1-913c-96bbd44efe1f/SMBC-BI-Pillar-3-Sept-25.pdf"),
    ("2025 H1", "H1", "SMBC-BI-Pillar-3-June-25.pdf", "Table 1: KM1, PDF p.5",
     "https://www.smbcgroup.com/emea/getmedia/97fab1b7-9060-4cfe-93c7-09d3172181ac/SMBC-BI-Pillar-3-June-25.pdf"),
    ("2024 Q4", "Q4", "Pillar-3-Interim-Disclosure-December-2024-(SMBC-BI).pdf", "Table 1: KM1, PDF p.5",
     "https://www.smbcgroup.com/emea/getmedia/478b7c2d-76e0-4c07-b727-b00757a4636d/Pillar-3-Interim-Disclosure-December-2024-(SMBC-BI).pdf"),
    ("2024 Q3", "Q3", "Pillar-3-Interim-Disclosure-September-2024-(SMBC-BI).pdf", "Table 1: KM1, PDF p.5",
     "https://www.smbcgroup.com/emea/getmedia/7c046ae7-c39b-4e3a-83b6-789e9c0d305e/Pillar-3-Interim-Disclosure-September-2024-(SMBC-BI).pdf"),
    ("2024 H1", "H1", "Pillar-3-Interim-Disclosure-June-2024-(SMBC-BI).pdf", "Table 1: KM1, PDF p.5",
     "https://www.smbcgroup.com/emea/getmedia/5808b03a-874f-4d90-a062-10d94d98c9d8/Pillar-3-Interim-Disclosure-June-2024-(SMBC-BI).pdf"),
    ("2023 Q4", "Q4", "Pillar-3-Interim-Disclosure-December-2023-(SMBC-BI).pdf", "Table 1: KM1, PDF p.5",
     "https://www.smbcgroup.com/emea/getmedia/8c626609-cec1-44a5-b08b-227189f7e287/Pillar-3-Interim-Disclosure-December-2023-(SMBC-BI).pdf"),
    ("2023 Q3", "Q3", "Pillar-3-Interim-Disclosure-September-2023-(SMBC-BI).pdf", "Table 1: KM1, PDF p.4",
     "https://www.smbcgroup.com/emea/getmedia/e2329270-9c6b-4707-be71-48a96b030b7b/Pillar-3-Interim-Disclosure-September-2023-(SMBC-BI).pdf"),
    ("2023 H1", "H1", "Pillar-3-Interim-Disclosure-June-2023-(SMBC-BI).pdf", "Table 1: KM1, PDF p.5",
     "https://www.smbcgroup.com/emea/getmedia/db3289f7-2020-4cfe-835c-4b0ef5eac4aa/Pillar-3-Interim-Disclosure-June-2023-(SMBC-BI).pdf"),
    ("2022 Q4", "Q4", "Pillar-3-Interim-Disclosure-December-2022-(SMBC-BI).pdf", "Table 1: KM1, PDF p.5",
     "https://www.smbcgroup.com/emea/getmedia/ee8d7d6b-5d17-4d82-9bd8-d52369fa4e45/Pillar-3-Interim-Disclosure-December-2022-(SMBC-BI).pdf"),
    ("2022 Q3", "Q3", "Pillar-3-Interim-Disclosure-September-2022-(SMBC-BI).pdf", "Table 1: KM1, PDF p.4",
     "https://www.smbcgroup.com/emea/getmedia/cd804340-56b8-4410-8bab-2b2f733729cd/Pillar-3-Interim-Disclosure-September-2022-(SMBC-BI).pdf"),
    ("2022 H1", "H1", "Pillar-3-Interim-Disclosure-June-2022-(SMBC-BI).pdf", "Table 1: KM1, PDF p.5",
     "https://www.smbcgroup.com/emea/getmedia/4490ceb5-1ff3-4cfb-84ac-93a8049d8cb5/Pillar-3-Interim-Disclosure-June-2022-(SMBC-BI).pdf"),
]

# Most-recent-first and aligned with INTERIM_PERIODS above.  All amount rows
# are USDm; ratios are percentage points as reported.
INTERIM_VALUES = {
    "CET1 Capital": [5761, 5771, 5780, 5450, 5465, 5469, 5077, 5084, 5077, 4878, 4871, 4864],
    "Tier 1 Capital": [5761, 5771, 5780, 5450, 5465, 5469, 5077, 5084, 5077, 4878, 4871, 4864],
    "Total Capital": [5761, 5771, 5780, 5450, 5465, 5469, 5077, 5084, 5077, 4878, 4871, 4864],
    "Total RWAs": [34723, 32117, 34299, 32113, 30156, 28591, 31432, 29061, 29791, 28657, 27759, 28233],
    "CET1 Ratio": ["16.6%", "18.0%", "16.9%", "17.0%", "18.1%", "19.1%", "16.2%", "17.5%", "17.0%", "17.0%", "17.5%", "17.2%"],
    "Tier 1 Ratio": ["16.6%", "18.0%", "16.9%", "17.0%", "18.1%", "19.1%", "16.2%", "17.5%", "17.0%", "17.0%", "17.5%", "17.2%"],
    "Total Capital Ratio": ["16.6%", "18.0%", "16.9%", "17.0%", "18.1%", "19.1%", "16.2%", "17.5%", "17.0%", "17.0%", "17.5%", "17.2%"],
    "Leverage Exposure": [74964, 64993, 63790, 59429, 40131, 36189, 42439, 37292, 36456, 38261, 42903, 38634],
    "Leverage Ratio": ["7.7%", "8.9%", "9.1%", "9.2%", "13.6%", "15.1%", "12.0%", "13.6%", "13.9%", "12.7%", "11.4%", "12.6%"],
    "LCR HQLA": [28993, 27479, 26296, 24939, 25369, 25342, 26810, 25074, 22986, 28599, 26812, 27846],
    "LCR Net Outflows": [19099, 18026, 16850, 15384, 15651, 15855, 16971, 16237, 15301, 19175, 16934, 19730],
    "LCR Ratio": ["151.8%", "152.4%", "156.1%", "162.1%", "162.1%", "159.8%", "158.0%", "154.4%", "150.2%", "149.1%", "158.3%", "141.1%"],
    "NSFR ASF": [26054, 24586, 23735, 22805, 23060, 23516, 23890, 23965, 23210, 24228, 24965, 22865],
    "NSFR RSF": [20317, 19844, 19020, 16987, 16693, 16735, 16939, 16870, 16613, 17256, 16274, 17191],
    "NSFR Ratio": ["128.2%", "123.9%", "124.8%", "134.3%", "138.1%", "140.5%", "141.0%", "142.1%", "139.7%", "140.4%", "153.4%", "133.0%"],
}

interim_headers = ["Period", "Disclosure type", "Metric", "Value", "Unit", "Basis", "Source document", "Page / table"]
interim_rows = []
interim_hyperlinks = {}
for metric_name, values in INTERIM_VALUES.items():
    unit = "%" if "Ratio" in metric_name else "USDm"
    if metric_name in {"Leverage Exposure", "LCR HQLA", "LCR Net Outflows", "NSFR ASF", "NSFR RSF"}:
        unit = "USDm"
    for idx, (period, disclosure_type, document, page, url) in enumerate(INTERIM_PERIODS):
        interim_rows.append((period, disclosure_type, metric_name, values[idx], unit,
                             "SMBC Bank International plc entity-level; native USD reporting",
                             document, page))
        interim_hyperlinks[(len(interim_rows) - 1, 6)] = url

bw.add_wide_interim_sheet(
    "Interim Pillar 3",
    headers=interim_headers,
    rows=interim_rows,
    title="SMBC Bank International plc — Interim Pillar 3",
    subtitle="Entity-level KM1 observations for non-annual quarter ends; amounts are native USDm and ratios are as reported.",
    note="The March year-end observations remain on the annual metric sheets. The official archive provides June, September and December disclosures for 2022-2025. Direct source-document hyperlinks are attached to every row. Interim amounts are intentionally not converted to GBP because a common, documented month-end conversion series is not part of the source methodology used for the annual workbook.",
    widths=[14, 16, 24, 14, 10, 48, 58, 25],
    hyperlink_cells=interim_hyperlinks,
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", gbp_spot(BS_TOTAL_ASSETS)),
        ("Loans and advances to customers", gbp_spot(BS_LOANS_CUSTOMERS)),
        ("Customer accounts", gbp_spot(BS_CUSTOMER_ACCOUNTS)),
        ("Total equity", gbp_spot(BS_TOTAL_EQUITY)),
    ],
    balance_sheet_unit="£m (conv. from USD)",
    income_statement_totals=[
        ("Operating income", gbp_avg(IS_OPERATING_INCOME)),
        ("Net operating expenses", gbp_avg(IS_NET_OPERATING_EXPENSES)),
        ("Profit for the year", gbp_avg(IS_PROFIT_FOR_YEAR)),
    ],
    income_statement_unit="£m (conv. from USD)",
    equity_changes_totals=[
        ("Opening equity", {"FY2025": 4417.2, "FY2024": 4197.2, "FY2023": 3757.9, "FY2022": 3471.0, "FY2021": 3690.5,
                            "FY2020": 3383.0, "FY2019": 2947.9, "FY2018": 3122.0, "FY2017": 2609.1, "FY2016": 2453.5,
                            "FY2015": 2114.6, "FY2014": 1728.8}),
        ("Total comprehensive income for the year", {"FY2025": 271.3, "FY2024": 310.3, "FY2023": 201.9, "FY2022": 115.8, "FY2021": 160.1,
                                                     "FY2020": 133.1, "FY2019": 207.1, "FY2018": 161.7, "FY2017": 117.6, "FY2016": 72.3,
                                                     "FY2015": 72.8, "FY2014": 63.3}),
        ("Other equity movements, net", {"FY2025": -98.0, "FY2024": -90.3, "FY2023": 237.4, "FY2022": 171.1, "FY2021": -379.6,
                                         "FY2020": 174.4, "FY2019": 228.0, "FY2018": -346.9, "FY2017": 395.3, "FY2016": 83.3,
                                         "FY2015": 266.1, "FY2014": 322.5}),
        ("Closing equity", gbp_spot(BS_TOTAL_EQUITY)),
    ],
    equity_changes_unit="£m (conv. from USD)",
    cash_flow_totals=[
        ("Net cash from/(used in) operating activities", gbp_avg(NET_OPERATING)),
        ("Net cash from/(used in) investing activities", gbp_avg(NET_INVESTING)),
        ("Net cash from/(used in) financing activities", gbp_avg(NET_FINANCING)),
        ("Cash and cash equivalents at 31 March", cash_end_gbp),
    ],
    cash_flow_unit="£m (conv. from USD)",
    ratios=[
        ("CET1 Ratio", {"FY2026": "21.0%", "FY2025": "17.1%", "FY2024": "19.5%", "FY2023": "17.8%", "FY2022": "16.3%", "FY2021": "16.7%",
                        "FY2020": "15.8%", "FY2019": "18.5%", "FY2018": "16.8%", "FY2017": "20.9%", "FY2016": "18.4%",
                        "FY2015": "24.8%", "FY2014": "22.9%"}),
        ("Tier 1 Ratio", {"FY2026": "21.0%", "FY2025": "17.1%", "FY2024": "19.5%", "FY2023": "17.8%", "FY2022": "16.3%", "FY2021": "16.7%",
                          "FY2020": "15.8%", "FY2019": "18.5%", "FY2018": "16.8%", "FY2017": "20.9%", "FY2016": "18.4%",
                          "FY2015": "24.8%", "FY2014": "22.9%"}),
        ("Total Capital Ratio", {"FY2026": "21.0%", "FY2025": "17.1%", "FY2024": "19.5%", "FY2023": "17.8%", "FY2022": "16.3%", "FY2021": "16.7%",
                                 "FY2020": "15.8%", "FY2019": "18.5%", "FY2018": "16.8%", "FY2017": "20.9%", "FY2016": "18.4%",
                                 "FY2015": "24.8%", "FY2014": "22.9%"}),
        ("Leverage Ratio", {"FY2026": "8.3%", "FY2025": "10.1%", "FY2024": "14.8%", "FY2023": "13.8%", "FY2022": "12.4%", "FY2021": "7.7%",
                            "FY2020": "6.8%", "FY2019": "7.6%", "FY2018": "5.8%", "FY2017": "8.4%", "FY2016": "7.1%",
                            "FY2015": "9.7%", "FY2014": "7.7%"}),
        ("LCR", {"FY2026": "154.8%", "FY2025": "160.1%", "FY2024": "155.6%", "FY2023": "145.4%", "FY2022": "136%", "FY2021": "145.0%",
                 "FY2020": "126.2%", "FY2019": "141.4%", "FY2018": "133.4%", "FY2017": "125.5%", "FY2016": "97.3%",
                 "FY2015": "115.2%"}),
        ("NSFR", {"FY2026": "132.8%", "FY2025": "127.2%", "FY2024": "141.8%", "FY2023": "142.4%", "FY2022": "133.5%", "FY2021": "135.5%",
                  "FY2020": "107.6%", "FY2019": "110.5%", "FY2018": "102.9%", "FY2017": "96.1%"}),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing. ALL £ figures in this "
         "workbook are converted from SMBC Bank International plc's native USD reporting - see the Cash Flow "
         "Statement sheet's source note for the full FX methodology and exact rates used. Ratios (%) are shown "
         "exactly as reported in USD and were not converted.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/SMBC FINANCIALS.xlsx")
