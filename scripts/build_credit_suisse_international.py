import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021",
         "FY2020", "FY2019", "FY2018", "FY2017", "FY2016", "FY2015"]  # most recent first, calendar year-end
YEAR_LABEL = {y: y for y in YEARS}

# Bank of England GBP/USD rates via poundsterlinglive.com's published archive,
# reusing the exact table already established for Zenith Bank UK (same 31
# December calendar year-end, so identical rate set applies). FY2014-FY2019
# rates (added for HD-020's FY2015-FY2020 extension) independently sourced
# from poundsterlinglive.com's historical Bank-of-England-spot pages and
# annual-average pages (not reused from any other bank's table).
FX_SPOT = {
    "FY2014": 1.5608,  # 31 Dec 2014 - only used for FY2015's opening cash balance
    "FY2015": 1.4819,  # 31 Dec 2015
    "FY2016": 1.2303,  # 30 Dec 2016 (31st was a Saturday)
    "FY2017": 1.3510,  # 29 Dec 2017 (30th/31st were a weekend)
    "FY2018": 1.2769,  # 31 Dec 2018
    "FY2019": 1.3210,  # 31 Dec 2019
    "FY2020": 1.3661,  # 31 Dec 2020
    "FY2021": 1.3521,  # 31 Dec 2021
    "FY2022": 1.2097,  # 30 Dec 2022 (31st was a Saturday)
    "FY2023": 1.2732,  # 29 Dec 2023 (31st was a Sunday)
    "FY2024": 1.2515,  # 31 Dec 2024
    "FY2025": 1.3448,  # 31 Dec 2025
}
FX_AVG = {
    "FY2015": 1.5283,
    "FY2016": 1.3550,
    "FY2017": 1.2885,
    "FY2018": 1.3347,
    "FY2019": 1.2765,
    "FY2020": 1.2837,
    "FY2021": 1.3752,
    "FY2022": 1.2362,
    "FY2023": 1.2439,
    "FY2024": 1.2782,
    "FY2025": 1.3193,
}


def flow(usd_m, year):
    """Flow figures (cash flow statement lines) - converted at the year's AVERAGE rate."""
    return round(usd_m / FX_AVG[year], 1)


def stock(usd_m, year):
    """Point-in-time figures (balances, capital, RWA) - converted at that year-end's SPOT rate."""
    return round(usd_m / FX_SPOT[year], 1)


AR_URLS = {
    "FY2025": "https://find-and-update.company-information.service.gov.uk/company/02500199/filing-history/MzUxNDA4Njk0M2FkaXF6a2N4/document?format=pdf&download=0",
    "FY2023": "https://find-and-update.company-information.service.gov.uk/company/02500199/filing-history/MzQxNzkxNzIxNWFkaXF6a2N4/document?format=pdf&download=0",
    "FY2021": "https://find-and-update.company-information.service.gov.uk/company/02500199/filing-history/MzMzMjg3NzIzMGFkaXF6a2N4/document?format=pdf&download=0",
    # Added for HD-020 (FY2015-FY2020 extension) - re-scanned and downloaded
    # directly from Companies House filing history (category=accounts,
    # pages 4-6), confirmed as real scanned Annual Report PDFs (go-tiff2pdf
    # producer - image-only, OCR'd this session to locate statement pages).
    "FY2020": "https://find-and-update.company-information.service.gov.uk/company/02500199/filing-history/MzMwMTQ3Mjk3N2FkaXF6a2N4/document?format=pdf&download=0",
    "FY2019": "https://find-and-update.company-information.service.gov.uk/company/02500199/filing-history/MzI2MTMzMDczMmFkaXF6a2N4/document?format=pdf&download=0",
    "FY2018": "https://find-and-update.company-information.service.gov.uk/company/02500199/filing-history/MzIzMTA0NjM5NGFkaXF6a2N4/document?format=pdf&download=0",
    "FY2017": "https://find-and-update.company-information.service.gov.uk/company/02500199/filing-history/MzIwMjIxNDAzMWFkaXF6a2N4/document?format=pdf&download=0",
    "FY2016": "https://find-and-update.company-information.service.gov.uk/company/02500199/filing-history/MzE3NTQ0MjEyNWFkaXF6a2N4/document?format=pdf&download=0",
    "FY2015": "https://find-and-update.company-information.service.gov.uk/company/02500199/filing-history/MzE0NTU0ODE5NWFkaXF6a2N4/document?format=pdf&download=0",
}

# Credit Suisse International's own standalone Pillar 3 disclosures for
# FY2015-FY2020, sourced from Credit Suisse's pre-UBS-migration website via
# the Wayback Machine (credit-suisse.com was reorganised/migrated after the
# 2023 UBS acquisition - these older documents are no longer live at their
# original credit-suisse.com URLs, confirmed via a CDX API re-scan this
# session). Real PDF text layers (not scanned), independently confirmed by
# extracting and reading each one.
CSI_P3_2025_URL = ("https://www.ubs.com/global/en/collections/credit-suisse/investment-bank/regulatory-directory/"
                    "international/_jcr_content/root/contentarea/mainpar/toplevelgrid_840462106/col_1/accordion/"
                    "accordionsplit/linklistnewlook/link_copy_copy_20862_2004292923.958213743.file/"
                    "PS9jb250ZW50L2RhbS9hc3NldHMvZ2xvYmFsL2VuL2NvbGxlY3Rpb25zL2NyZWRpdC1zdWlzc2UvZG9jdW1lbnRzL2ludGVy"
                    "bmF0aW9uYWwtZG9jdW1lbnRzL2NzaS1waWxsYXItMjAyNS1kaXNjbG9zdXJlLXY2LnBkZg==/"
                    "csi-pillar-2025-disclosure-v6.pdf")
CSI_P3_2024_URL = ("https://www.ubs.com/global/en/collections/credit-suisse/investment-bank/regulatory-directory/"
                    "international/_jcr_content/root/contentarea/mainpar/toplevelgrid_840462106/col_1/accordion/"
                    "accordionsplit/linklistnewlook/link_copy_copy_20862.0656872784.file/"
                    "PS9jb250ZW50L2RhbS9hc3NldHMvY2MvaW52ZXN0b3ItcmVsYXRpb25zL2NvbXBsZW1lbnRhcnktZmluYW5jaWFsLWluZm9y"
                    "bWF0aW9uL2FyY2hpdmUvMjAyNC8yMDI0LWNzaS1waWxsYXItMy1kaXNjbG9zdXJlcy5wZGY=/"
                    "2024-csi-pillar-3-disclosures.pdf")
CSI_P3_2023_URL = ("https://www.ubs.com/global/en/investor-relations/complementary-financial-information/"
                    "disclosure-legal-entities/archive-credit-suisse/_jcr_content/root/contentarea/mainpar/"
                    "toplevelgrid_1145414446/col_1/accordionbox/accordionsplit_485894160/table.0884404004.file/"
                    "dGFibGVUZXh0PS9jb250ZW50L2RhbS9hc3NldHMvY2MvaW52ZXN0b3ItcmVsYXRpb25zL2NvbXBsZW1lbnRhcnktZmluYW5j"
                    "aWFsLWluZm9ybWF0aW9uL2FyY2hpdmUvMjAyMy8yMDIzLWNzaS1waWxsYXItMy1kaXNjbG9zdXJlcy5wZGY=/"
                    "2023-csi-pillar-3-disclosures.pdf")
CSI_P3_2022_URL = ("https://www.ubs.com/global/en/investor-relations/complementary-financial-information/"
                    "disclosure-legal-entities/archive-credit-suisse/_jcr_content/root/contentarea/mainpar/"
                    "toplevelgrid_1145414446/col_1/accordionbox/accordionsplit_1343042181/innergrid/col_1/"
                    "table.0589413556.file/dGFibGVUZXh0PS9jb250ZW50L2RhbS9hc3NldHMvY2MvaW52ZXN0b3ItcmVsYXRpb25zL2Nv"
                    "bXBsZW1lbnRhcnktZmluYW5jaWFsLWluZm9ybWF0aW9uL2FyY2hpdmUvMjAyMi9jc2ktcGlsbGFyLTMtZGlzY2xvc3VyZXMt"
                    "MjAyMi5wZGY=/csi-pillar-3-disclosures-2022.pdf")

P3_URLS = {
    # FY2021/FY2022 located 2026-09-12: the same pre-migration credit-suisse.com
    # path as FY2015-FY2020 below still serves these two years via Wayback, which
    # an earlier session's "not locatable" conclusion had missed.
    "FY2022": "https://web.archive.org/web/2024id_/https://www.credit-suisse.com/media/assets/corporate/docs/about-us/investor-relations/regulatory-disclosures/csi-pillar-3-disclosures-2022.pdf",
    "FY2021": "https://web.archive.org/web/2024id_/https://www.credit-suisse.com/media/assets/corporate/docs/about-us/investor-relations/regulatory-disclosures/csi-pillar-3-disclosures-2021.pdf",
    "FY2020": "https://web.archive.org/web/20210627075334if_/https://www.credit-suisse.com/media/assets/corporate/docs/about-us/investor-relations/regulatory-disclosures/csi-pillar-3-disclosures-2020.pdf",
    "FY2019": "https://web.archive.org/web/20210627075339if_/https://www.credit-suisse.com/media/assets/corporate/docs/about-us/investor-relations/regulatory-disclosures/csi-pillar-3-disclosures-2019.pdf",
    "FY2018": "https://web.archive.org/web/20210627075317if_/https://www.credit-suisse.com/media/assets/corporate/docs/about-us/investor-relations/regulatory-disclosures/csi-pillar-3-disclosures-2018.pdf",
    "FY2017": "https://web.archive.org/web/20210627075328if_/https://www.credit-suisse.com/media/assets/about-us/docs/investor-relations/financial-regulatory-disclosures/regulatory-disclosures/regulatory-disclosures-subsidiaries/csi-pillar-3-disclosures-2017.pdf",
    "FY2016": "https://web.archive.org/web/20170629113020if_/https://www.credit-suisse.com/media/assets/corporate/docs/about-us/investor-relations/regulatory-disclosures/csi-pillar-3-disclosures-2016.pdf",
    "FY2015": "https://web.archive.org/web/20210627075342if_/https://www.credit-suisse.com/media/assets/corporate/docs/about-us/investor-relations/regulatory-disclosures/csi-pillar-3-disclosures-2015.pdf",
}

ENTITY_NOTE = (
    "Credit Suisse International (CSI, company 02500199, FRN 146702) is the UK derivatives/structured-products "
    "trading entity within the former Credit Suisse group - a DISTINCT legal entity from 'Credit Suisse (UK) "
    "Limited' (the deposit-taking bank, built separately in this same batch). Following Credit Suisse's 2023 "
    "collapse and rescue by UBS Group AG, CSI remains an active, separately-reporting UK entity (registered "
    "office moved to UBS's 5 Broadgate address 2 Jan 2026) but is in an explicit, disclosed CONTROLLED WIND-DOWN: "
    "its own FY2025 KPI table states 'Profitability and Risk Weighted Assets (RWA) are reviewed to ensure a "
    "controlled wind-down in a capital efficient manner.' Total assets collapsed from $244.5bn (FY2021) to "
    "$5.65bn (FY2025) - a 97.7% reduction - as client business was progressively transferred to other UBS Group "
    "entities via Part VII transfers. FY2025 also separately reports a $(397)m pre-tax loss from Discontinued "
    "Operations, on top of continuing operations. All figures are converted from CSI's reporting currency (USD) "
    "to GBP using the Bank of England's published GBP/USD spot rate (point-in-time/balance figures) or average "
    "rate over the fiscal year (flow figures) - see the FX conversion methodology note below. All %-ratios are "
    "shown exactly as disclosed, not converted (dimensionless)."
)

FX_METHOD_NOTE = (
    "FX conversion: point-in-time figures (cash balances, Tier 1 capital, RWA) converted at the Bank of England "
    "GBP/USD SPOT rate as at each fiscal year-end; flow figures (every cash flow statement line item) converted "
    "at the AVERAGE rate over that fiscal year. Rates used (£1 = $X): 31 Dec 2014 spot 1.5608 (FY2015 opening "
    "cash only); FY2015 spot 1.4819 / average 1.5283; FY2016 spot 1.2303 / average 1.3550; FY2017 spot 1.3510 / "
    "average 1.2885; FY2018 spot 1.2769 / average 1.3347; FY2019 spot 1.3210 / average 1.2765; FY2020 spot "
    "1.3661 / average 1.2837; FY2021 spot 1.3521 / average 1.3752; FY2022 spot 1.2097 / average 1.2362; FY2023 "
    "spot 1.2732 / average 1.2439; FY2024 spot 1.2515 / average 1.2782; FY2025 spot 1.3448 / average 1.3193. "
    "FY2021-FY2025 rates reuse the table already established for Zenith Bank UK (identical 31 December year-end); "
    "FY2014-FY2019 rates were independently sourced this session from poundsterlinglive.com's Bank-of-England-spot "
    "and annual-average history pages for HD-020's FY2015-FY2020 extension. Converting stocks and flows at "
    "different rates means the statement doesn't tie in GBP by itself - an 'Effect of GBP/USD translation' line "
    "is included, computed programmatically as the balancing figure (never hardcoded), labelled clearly as a "
    "translation artefact with no bearing on CSI's actual results."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are Credit Suisse International's own Consolidated Statement of Cash Flows (Group "
    "and Bank basis - identical for this entity in every year checked), converted from USD to GBP (see FX note "
    "below):\n"
    f"FY2025/FY2024: Annual Report for the Year Ended 31 December 2025, p.46 (filed at Companies House "
    f"12 Apr 2026) - {AR_URLS['FY2025']}\n"
    f"FY2023/FY2022: Annual Report for the Year Ended 31 December 2023, p.47 (filed 20 Apr 2024) - "
    f"{AR_URLS['FY2023']}\n"
    f"FY2021: Annual Report for the Year Ended 31 December 2021, p.55 (filed 16 Mar 2022) - {AR_URLS['FY2021']}\n"
    f"FY2020: Annual Report for the Year Ended 31 December 2020, p.66 (filed 26 May 2021) - {AR_URLS['FY2020']}\n"
    f"FY2019: Annual Report for the Year Ended 31 December 2019, p.53 (filed 8 Apr 2020) - {AR_URLS['FY2019']}\n"
    f"FY2018: Annual Report for the Year Ended 31 December 2018, p.45 (filed 2 Apr 2019) - {AR_URLS['FY2018']}\n"
    f"FY2017: Annual Report for the Year Ended 31 December 2017, p.39 (filed 10 Apr 2018) - {AR_URLS['FY2017']}\n"
    f"FY2016: Annual Report for the Year Ended 31 December 2016, p.31 (filed 10 May 2017) - {AR_URLS['FY2016']}\n"
    f"FY2015: Annual Report for the Year Ended 31 December 2015, p.21 (filed 8 Apr 2016) - {AR_URLS['FY2015']}\n"
    + ENTITY_NOTE + "\n\n" + FX_METHOD_NOTE
)


def p3_sources():
    return (
        "Sources - Credit Suisse International capital/RWA basis: the FY2025 Annual Report's own 'Key "
        "Performance Indicators' table (p.6), which discloses Risk Weighted Assets, Tier 1 capital, and Tier 1 "
        "capital ratio for all 5 years (2021-2025) as at each year-end - "
        f"{AR_URLS['FY2025']}. This report explicitly states 'Pillar 3 disclosures required under the Capital "
        "Requirements Regulation (CRR) can be found separately at http://www.ubs.com'. Converted from USD to "
        "GBP using the same FX methodology as the Cash Flow Statement sheet (SPOT rate at each year-end); "
        "% ratios shown exactly as disclosed, not converted.\n\n"
        "FY2021-FY2024 PILLAR 3 DOCUMENTS RECOVERED (2026-09-12): an earlier session concluded the standalone "
        "CSi Pillar 3 document 'was not locatable' for FY2021-FY2025 and left Total Capital, Total Capital "
        "Ratio, Leverage Ratio, LCR and NSFR blank on that basis. That conclusion was wrong for four of those "
        "five years. CSi publishes a full KM1 key-metrics template every year, recovered as follows:\n"
        f"FY2024: KM1, p.5 - UBS-hosted '2024-csi-pillar-3-disclosures.pdf' (the same document already cited on "
        f"the RWA Breakdown sheet for its OV1 table), retrieved via web.archive.org - {CSI_P3_2024_URL}\n"
        f"FY2023: KM1, p.5 - UBS-hosted '2023-csi-pillar-3-disclosures.pdf', likewise already cited on the RWA "
        f"Breakdown sheet, retrieved via web.archive.org - {CSI_P3_2023_URL}\n"
        f"FY2022: KM1, p.5 - Credit Suisse International Pillar 3 Disclosures 2022, retrieved via "
        f"web.archive.org from the pre-migration credit-suisse.com pattern - {P3_URLS['FY2022']}\n"
        f"FY2021: capital composition/'Capital ratios' tables, p.4-5, plus the leverage-ratio (LRCom, p.9) and "
        f"LCR (p.11) tables - Credit Suisse International Pillar 3 Disclosures 2021, same pre-migration pattern "
        f"via web.archive.org - {P3_URLS['FY2021']}\n"
        "Each recovered year's figures were cross-checked against the following year's own KM1 comparative "
        "column and agree exactly (FY2021 CET1/Tier 1 $15,022m, Total capital $15,027m, Total RWA $62,643m all "
        "confirmed in both FY2021's and FY2022's own documents).\n"
        "FY2022/FY2023 CET1 GAP CLOSED (2026-09-15): the same three KM1 templates also carry the separate CET1 "
        "amount and CET1 ratio lines that the CET1 Capital / CET1 Ratio sheets previously left blank for these "
        "two years (see those sheets' own note for the figures, the two-document cross-check and the FY2022 "
        "restated-vs-originally-published ratio point). The FY2024 and FY2023 UBS-hosted documents both return "
        "HTTP 403 to scripted requests against ubs.com from this environment; both were retrieved instead "
        "through the Wayback Machine's id_ replay of those exact UBS URLs "
        "(https://web.archive.org/web/2025id_/<the UBS URL below>), and the FY2022 document from the "
        "pre-migration credit-suisse.com URL already listed here. All three are genuine PDFs (0.8-2.6MB), not "
        "soft-404 HTML.\n"
        "FY2025 NOW OBTAINED (2026-09-15) - the access block is resolved. ubs.com returns HTTP 403 to scripted "
        "requests from this environment and the Wayback Machine has no capture, so the PDF was downloaded "
        "manually in an ordinary browser and transcribed from the local copy. Source: Credit Suisse "
        "International Pillar 3 Disclosures 2025, 'KM1 - Key metrics template', p.6 (Total capital, Total "
        "capital ratio, Leverage ratio, LCR, NSFR; CET1/Tier 1/Total RWA on the same table confirm the figures "
        "already carried here from the Annual Report's KPI table). That document's own 2024 comparative column "
        "reproduces every FY2024 figure already on these sheets exactly (CET1/Tier 1/Total capital $6,883m, "
        "Total RWA $10,951m, ratios 62.86%, leverage 21.16%, LCR 363.29%, NSFR 214.78%), confirming an "
        "unbroken basis across the two years. Its 'Own Funds' section (p.7) states 'CSi has no AT1 capital or "
        "Tier 2 capital instruments', so CET1 = Tier 1 = Total capital = $3,014m for FY2025 as disclosed, not "
        "inferred. The live URL, fetchable in an ordinary browser, is:\n"
        f"{CSI_P3_2025_URL}\n\n"
        "FY2015-FY2020 (added for HD-020): CSI's own standalone Pillar 3 disclosure PDFs (real text layers, not "
        "scanned), each headed 'Capital management' and each containing its own capital composition/capital "
        "ratios table plus (from FY2017 onward) an 'OV1 - Overview of RWA' breakdown table. These are no longer "
        "hosted live at credit-suisse.com following the 2023 UBS acquisition/site migration (confirmed via a "
        "Wayback Machine CDX API re-scan this session) - retrieved via web.archive.org:\n"
        f"FY2020: Credit Suisse International Pillar 3 Disclosures 2020, p.5 (capital)/p.7 (RWA) - {P3_URLS['FY2020']}\n"
        f"FY2019: Credit Suisse International Pillar 3 Disclosures 2019, p.5 (capital)/p.6 (RWA) - {P3_URLS['FY2019']}\n"
        f"FY2018: Credit Suisse International Pillar 3 Disclosures 2018, p.5 (capital)/p.6 (RWA) - {P3_URLS['FY2018']}\n"
        f"FY2017: Credit Suisse International Pillar 3 Disclosures 2017, p.6 (capital)/p.8 (RWA) - {P3_URLS['FY2017']}\n"
        f"FY2016: Credit Suisse International Pillar 3 Disclosures 2016, p.5 (capital)/p.7 (RWA, Basel II/III-era "
        f"template - see RWA Breakdown sheet's own note) - {P3_URLS['FY2016']}\n"
        f"FY2015: Credit Suisse International Pillar 3 Disclosures 2015, p.5 (capital)/p.7 (RWA, Basel II/III-era "
        f"template) - {P3_URLS['FY2015']}\n"
        "BASEL II/III-ERA CAVEAT: FY2015-FY2016's Pillar 3 disclosures pre-date the CRR II 'OV1' RWA-breakdown "
        "template used from FY2017 onward - they report RWA under three broader buckets ('Total credit and "
        "counterparty credit risk' including CVA, 'Total market risk', 'Total other risks' covering default-fund "
        "contributions/operational risk/large exposures) rather than the 8-line OV1 categories. CET1 is not a "
        "distinct concept in any of FY2015-FY2020's disclosures either (CSI had no Additional Tier 1 instruments "
        "in this window, so CET1 = Tier 1 throughout - stated explicitly in each year's own document).\n"
        + FX_METHOD_NOTE
    )


bw = BankWorkbook(bank_name="Credit Suisse International", years=YEARS, year_label=YEAR_LABEL, header_color="50B633")

STATEMENTS_SOURCES_NOTE = (
    "Sources - Credit Suisse International's own Consolidated Statement of Financial Position / Consolidated "
    "Statement of Income / Consolidated Statement of Changes in Equity (Group basis throughout, converted from "
    "USD to GBP - see FX note below), each year's own originally-published figures (not a later year's restated "
    "comparative):\n"
    f"FY2025: Annual Report for the Year Ended 31 December 2025, pp.43-45 - {AR_URLS['FY2025']}\n"
    f"FY2024: FY2025 Annual Report's own FY2024 comparative column (restated to exclude discontinued operations "
    f"- FY2024's own standalone Annual Report was not sourced this session), pp.43-45 - {AR_URLS['FY2025']}\n"
    f"FY2023: Annual Report for the Year Ended 31 December 2023, pp.42-45 - {AR_URLS['FY2023']}\n"
    f"FY2022: FY2023 Annual Report's own FY2022 comparative column, pp.42-45 - {AR_URLS['FY2023']}\n"
    f"FY2021: Annual Report for the Year Ended 31 December 2021, pp.50-53 - {AR_URLS['FY2021']}\n"
    f"FY2020: Annual Report for the Year Ended 31 December 2020, pp.61-65 - {AR_URLS['FY2020']}\n"
    f"FY2019: Annual Report for the Year Ended 31 December 2019, pp.48-52 - {AR_URLS['FY2019']}\n"
    f"FY2018: Annual Report for the Year Ended 31 December 2018, pp.41-44 - {AR_URLS['FY2018']}\n"
    f"FY2017: Annual Report for the Year Ended 31 December 2017, pp.34-38 - {AR_URLS['FY2017']}\n"
    f"FY2016: Annual Report for the Year Ended 31 December 2016, pp.26-30 - {AR_URLS['FY2016']}\n"
    f"FY2015: Annual Report for the Year Ended 31 December 2015, pp.16-20 - {AR_URLS['FY2015']}\n"
    + ENTITY_NOTE + "\n\n" + FX_METHOD_NOTE + "\n\n"
    "PRESENTATION NOTE: s.408 Companies Act 2006 exemption means no separate Bank-only income statement is "
    "published (Group figures used for P&L throughout, consistent with the Balance Sheet and Equity statement). "
    "FY2024/FY2025's income statement separates 'Discontinued Operations' from continuing operations, as do "
    "FY2019/FY2020 (each showing its own year's discontinued-operations split, driven by different disposals); "
    "FY2015/FY2018/FY2021-23 have no such split (whole-entity basis); FY2016/FY2017 show a continuing/"
    "discontinued split but with nil or small discontinued-operations figures - each year's own presentation is "
    "reproduced as reported, not forced onto one basis. A small (~£0.7m-£1.5m) rounding gap exists between the "
    "P&L's own 'Total comprehensive income/(loss)' and the Equity statement's own total for the same year in "
    "several years (FY2024/FY2022/FY2021) - this originates as a <=$1m rounding artifact already present in "
    "CSI's own USD-million source tables, amplified slightly by FX conversion; both sheets show each source "
    "table's own figure rather than forcing one to match the other.\n\n"
    "BALANCE SHEET LINE-ITEM RELABELLING ACROSS YEARS (same underlying items, renamed by CSI over time - not a "
    "definitional change): 'Deposits' (FY2015-2019) = 'Due to banks' (FY2020+); 'Short term borrowings' "
    "(FY2015-2017) = 'Borrowings' (FY2018+); 'Long term debt' (FY2015-2017) = 'Debt in issuance' (FY2018+); "
    "'Other loans and receivables' (FY2015-2017) then 'Net loans' (FY2018-2019) = 'Loans and advances' (FY2020+); "
    "'Financial assets designated at fair value through profit or loss' (FY2015-2017, pre-IFRS 9) = 'Non-trading "
    "financial assets [mandatorily] at fair value through P&L' (FY2018+, post-IFRS 9 adoption 1 Jan 2018) - shown "
    "on the same row in each case, per each year's own renaming note in its Annual Report. 'Share premium' "
    "(a distinct row, FY2015-2020) was reclassified in full to retained earnings during FY2020 (see the "
    "Statement of Changes in Equity sheet) and does not exist as a separate balance from FY2021 onward. 'Assets "
    "held for sale' / 'Liabilities held for sale' are discontinued-operations classification lines that appear "
    "only in the specific years CSI disclosed a held-for-sale disposal group (FY2016/FY2017/FY2019/FY2020) - "
    "left blank, not zero, in years with no such disclosure. 'Lease liabilities' is disclosed as its own line "
    "only from FY2020 onward (IFRS 16 adopted 1 Jan 2019, but FY2019's own Balance Sheet still embeds lease "
    "liabilities within 'Debt in issuance' per that year's own presentation - only FY2020's own report first "
    "breaks it out as a separate line, per FY2020's own explanatory footnote)."
)

# ---------------------------------------------------------------
# Balance Sheet (Consolidated Statement of Financial Position)
# ---------------------------------------------------------------
BS_ROWS_USD = [
    ("SECTION", "Assets", None),
    ("DATA", "Cash and due from banks", {"FY2025":362,"FY2024":1858,"FY2023":3627,"FY2022":4149,"FY2021":1484,
     "FY2020":6225,"FY2019":4438,"FY2018":2229,"FY2017":4971,"FY2016":5490,"FY2015":13163}),
    ("DATA", "Interest-bearing deposits with banks", {"FY2025":525,"FY2024":3961,"FY2023":8319,"FY2022":12085,"FY2021":13284,
     "FY2020":14486,"FY2019":12205,"FY2018":17859,"FY2017":4187,"FY2016":9647,"FY2015":59}),
    ("DATA", "Securities purchased under resale agreements", {"FY2025":4439,"FY2024":533,"FY2023":1304,"FY2022":10527,"FY2021":8902,
     "FY2020":4559,"FY2019":6145,"FY2018":10487,"FY2017":17052,"FY2016":9467,"FY2015":30073}),
    ("DATA", "Trading financial assets at fair value through P&L", {"FY2025":8,"FY2024":22624,"FY2023":63309,"FY2022":107973,"FY2021":143718,
     "FY2020":188620,"FY2019":148443,"FY2018":148674,"FY2017":174555,"FY2016":242427,"FY2015":295229}),
    ("DATA", "Non-trading financial assets at fair value through P&L", {"FY2024":14200,"FY2023":24588,"FY2022":22831,"FY2021":38226,
     "FY2020":25516,"FY2019":22294,"FY2018":17659,"FY2017":11130,"FY2016":20406,"FY2015":12078}),
    ("DATA", "Loans and advances", {"FY2025":7,"FY2024":2548,"FY2023":3411,"FY2022":2973,"FY2021":2968,
     "FY2020":3151,"FY2019":3103,"FY2018":3512,"FY2017":3331,"FY2016":3316,"FY2015":3495}),
    ("DATA", "Other investments", {"FY2015":26}),
    ("DATA", "Investment property", {"FY2021":14,"FY2020":15,"FY2019":17,"FY2018":18,"FY2017":131,"FY2016":169,"FY2015":303}),
    ("DATA", "Current tax assets", {"FY2025":107,"FY2024":194,"FY2023":121,"FY2022":110,"FY2021":67,
     "FY2020":39,"FY2019":51,"FY2018":21,"FY2017":5,"FY2016":52,"FY2015":46}),
    ("DATA", "Deferred tax assets", {"FY2021":284,"FY2020":199,"FY2019":196,"FY2018":330,"FY2017":349,"FY2016":338,"FY2015":337}),
    ("DATA", "Other assets", {"FY2025":202,"FY2024":5416,"FY2023":17629,"FY2022":21744,"FY2021":34666,
     "FY2020":44566,"FY2019":35231,"FY2018":30254,"FY2017":32957,"FY2016":36700,"FY2015":45610}),
    ("DATA", "Property and equipment", {"FY2024":9,"FY2023":27,"FY2022":372,"FY2021":407,
     "FY2020":451,"FY2019":535,"FY2018":234,"FY2017":157,"FY2016":193,"FY2015":196}),
    ("DATA", "Intangible assets", {"FY2024":31,"FY2023":83,"FY2022":482,"FY2021":495,
     "FY2020":485,"FY2019":489,"FY2018":476,"FY2017":454,"FY2016":404,"FY2015":374}),
    ("DATA", "Assets held for sale", {"FY2020":1934,"FY2019":531,"FY2017":161,"FY2016":3772}),
    ("TOTAL", "Total assets", {"FY2025":5650,"FY2024":51374,"FY2023":122418,"FY2022":183246,"FY2021":244515,
     "FY2020":290246,"FY2019":233678,"FY2018":231753,"FY2017":249440,"FY2016":332381,"FY2015":400989}),
    ("SECTION", "Liabilities", None),
    ("DATA", "Due to banks", {"FY2025":5,"FY2024":18,"FY2023":31,"FY2022":266,"FY2021":218,
     "FY2020":433,"FY2019":435,"FY2018":1028,"FY2017":188,"FY2016":457,"FY2015":564}),
    ("DATA", "Securities sold under repurchase agreements", {"FY2025":443,"FY2024":26,"FY2023":358,"FY2022":2924,"FY2021":3371,
     "FY2020":4783,"FY2019":3155,"FY2018":2391,"FY2017":7193,"FY2016":2821,"FY2015":5737}),
    ("DATA", "Trading financial liabilities at fair value through P&L", {"FY2025":8,"FY2024":22129,"FY2023":60519,"FY2022":93397,"FY2021":122054,
     "FY2020":164364,"FY2019":133536,"FY2018":126414,"FY2017":149505,"FY2016":211639,"FY2015":270767}),
    ("DATA", "Financial liabilities designated at fair value through P&L", {"FY2025":1,"FY2024":2565,"FY2023":16050,"FY2022":27169,"FY2021":35012,
     "FY2020":29788,"FY2019":21115,"FY2018":24164,"FY2017":22899,"FY2016":24689,"FY2015":22509}),
    ("DATA", "Borrowings", {"FY2025":2002,"FY2024":7387,"FY2023":12622,"FY2022":6025,"FY2021":1470,
     "FY2020":2436,"FY2019":14116,"FY2018":19555,"FY2017":5940,"FY2016":2667,"FY2015":21066}),
    ("DATA", "Current tax liabilities", {"FY2024":3,"FY2023":3,"FY2022":3,"FY2021":13,
     "FY2020":4,"FY2019":38,"FY2018":51,"FY2017":91,"FY2016":0}),
    ("DATA", "Deferred tax liabilities", {"FY2024":37,"FY2023":59}),
    ("DATA", "Other liabilities", {"FY2025":118,"FY2024":6007,"FY2023":9025,"FY2022":16675,"FY2021":23584,
     "FY2020":32418,"FY2019":23320,"FY2018":23339,"FY2017":24176,"FY2016":31426,"FY2015":30822}),
    ("DATA", "Provisions", {"FY2025":58,"FY2024":116,"FY2023":168,"FY2022":45,"FY2021":313,
     "FY2020":4,"FY2019":22,"FY2018":5,"FY2017":6,"FY2016":27,"FY2015":33}),
    ("DATA", "Debt in issuance", {"FY2024":5456,"FY2023":8108,"FY2022":18309,"FY2021":40224,
     "FY2020":31597,"FY2019":14724,"FY2018":12146,"FY2017":16847,"FY2016":32140,"FY2015":26587}),
    ("DATA", "Lease liabilities", {"FY2024":291,"FY2023":512,"FY2022":529,"FY2021":627,"FY2020":705}),
    ("DATA", "Liabilities held for sale", {"FY2020":707,"FY2019":431,"FY2017":117,"FY2016":3807}),
    ("TOTAL", "Total liabilities", {"FY2025":2635,"FY2024":44035,"FY2023":107455,"FY2022":165342,"FY2021":226886,
     "FY2020":267239,"FY2019":210892,"FY2018":209093,"FY2017":226962,"FY2016":309673,"FY2015":378085}),
    ("SECTION", "Shareholders' equity", None),
    ("DATA", "Share capital", {"FY2025":1,"FY2024":1368,"FY2023":7267,"FY2022":11366,"FY2021":11366,
     "FY2020":11366,"FY2019":11366,"FY2018":12366,"FY2017":12366,"FY2016":12366,"FY2015":12366}),
    ("DATA", "Share premium", {"FY2020":0,"FY2019":12704,"FY2018":12704,"FY2017":12704,"FY2016":12704,"FY2015":12704}),
    ("DATA", "Capital contribution", {"FY2025":904,"FY2024":917,"FY2023":887,"FY2022":887,"FY2021":887,
     "FY2020":887,"FY2019":875}),
    ("DATA", "Other equity instruments", {"FY2023":1200,"FY2022":1200}),
    ("DATA", "Retained earnings", {"FY2025":2110,"FY2024":5611,"FY2023":6058,"FY2022":4852,"FY2021":5536,
     "FY2020":10881,"FY2019":-2030,"FY2018":-2381,"FY2017":-2592,"FY2016":-2360,"FY2015":-2164}),
    ("DATA", "Accumulated other comprehensive income", {"FY2024":-557,"FY2023":-449,"FY2022":-401,"FY2021":-160,
     "FY2020":-127,"FY2019":-129,"FY2018":-29,"FY2017":0,"FY2016":-2,"FY2015":-2}),
    ("TOTAL", "Total shareholders' equity", {"FY2025":3015,"FY2024":7339,"FY2023":14963,"FY2022":17904,"FY2021":17629,
     "FY2020":23007,"FY2019":22786,"FY2018":22660,"FY2017":22478,"FY2016":22708,"FY2015":22904}),
    ("TOTAL", "Total liabilities and shareholders' equity", {"FY2025":5650,"FY2024":51374,"FY2023":122418,"FY2022":183246,"FY2021":244515,
     "FY2020":290246,"FY2019":233678,"FY2018":231753,"FY2017":249440,"FY2016":332381,"FY2015":400989}),
]
balance_sheet_rows = [
    (kind, label, ({} if values is None else {y: stock(v, y) for y, v in values.items()}))
    for kind, label, values in BS_ROWS_USD
]

bw.add_balance_sheet_sheet(
    title="Credit Suisse International — Consolidated Statement of Financial Position",
    subtitle="£m, converted from USD - Group basis - see source note at bottom for FX methodology and rates used.",
    rows=balance_sheet_rows,
    sources_text=STATEMENTS_SOURCES_NOTE,
    first_col_width=90,
    source_height=340,
    unit_suffix=" (£m, conv. from USD)",
)

# ---------------------------------------------------------------
# Profit & Loss (Consolidated Statement of Income / Comprehensive Income)
# ---------------------------------------------------------------
PL_ROWS_USD = [
    ("SECTION", "Income", None),
    ("DATA", "Interest income", {"FY2025":507,"FY2024":1581,"FY2023":2976,"FY2022":1628,"FY2021":428,
     "FY2020":497,"FY2019":1273,"FY2018":1446,"FY2017":818,"FY2016":662,"FY2015":535}),
    ("DATA", "Interest expense", {"FY2025":-295,"FY2024":-1004,"FY2023":-2532,"FY2022":-1670,"FY2021":-491,
     "FY2020":-487,"FY2019":-1111,"FY2018":-1175,"FY2017":-848,"FY2016":-822,"FY2015":-475}),
    ("TOTAL", "Net interest income/(expense)", {"FY2025":212,"FY2024":577,"FY2023":444,"FY2022":-42,"FY2021":-63,
     "FY2020":10,"FY2019":162,"FY2018":271,"FY2017":-30,"FY2016":-160,"FY2015":60}),
    ("DATA", "Commission and fee income", {"FY2025":1,"FY2024":1,"FY2023":139,"FY2022":425,"FY2021":428,
     "FY2020":363,"FY2019":336,"FY2018":598,"FY2017":524,"FY2016":381,"FY2015":216}),
    ("DATA", "Allowance for credit losses", {"FY2023":-68,"FY2022":158,"FY2021":-4530,
     "FY2020":-17,"FY2019":-4,"FY2018":-8,"FY2017":-5,"FY2016":-2,"FY2015":3}),
    ("DATA", "Net gains from financial assets/liabilities at FVTPL", {"FY2025":47,"FY2024":109,"FY2023":796,"FY2022":1603,"FY2021":1761,
     "FY2020":1715,"FY2019":1271,"FY2018":1097,"FY2017":1054,"FY2016":1532,"FY2015":2003}),
    ("DATA", "Other revenues", {"FY2025":1,"FY2024":46,"FY2023":102,"FY2022":184,"FY2021":253,
     "FY2020":241,"FY2019":154,"FY2018":239,"FY2017":-180,"FY2016":-367,"FY2015":-340}),
    ("TOTAL", "Net revenues", {"FY2025":261,"FY2024":733,"FY2023":1413,"FY2022":2328,"FY2021":-2151,
     "FY2020":2312,"FY2019":1919,"FY2018":2197,"FY2017":1363,"FY2016":1384,"FY2015":1942}),
    ("SECTION", "Operating expenses", None),
    ("DATA", "Compensation and benefits", {"FY2023":-642,"FY2022":-551,"FY2021":-729,
     "FY2020":-841,"FY2019":-796,"FY2018":-604,"FY2017":-672,"FY2016":-636,"FY2015":-572}),
    ("DATA", "General, administrative and trading expenses", {"FY2025":-18,"FY2024":-20,"FY2023":-2460,"FY2022":-2061,"FY2021":-2489,
     "FY2020":-1272,"FY2019":-986,"FY2018":-1423,"FY2017":-840,"FY2016":-938,"FY2015":-1305}),
    ("DATA", "Restructuring expenses", {"FY2023":-47,"FY2022":-47,"FY2021":-17,
     "FY2020":-8,"FY2019":0,"FY2018":-96,"FY2017":-31,"FY2016":-140,"FY2015":-117}),
    ("TOTAL", "Total operating expenses", {"FY2025":-18,"FY2024":-20,"FY2023":-3149,"FY2022":-2659,"FY2021":-3235,
     "FY2020":-2121,"FY2019":-1782,"FY2018":-2123,"FY2017":-1543,"FY2016":-1714,"FY2015":-1994}),
    ("TOTAL", "Profit/(loss) before tax from continuing operations", {"FY2025":243,"FY2024":713,"FY2023":-1736,"FY2022":-331,"FY2021":-5386,
     "FY2020":191,"FY2019":137,"FY2018":74,"FY2017":-180,"FY2016":-330,"FY2015":-52}),
    ("DATA", "Income tax (expense)/benefit", {"FY2025":-68,"FY2024":-92,"FY2023":-57,"FY2022":-354,"FY2021":43,
     "FY2020":12,"FY2019":158,"FY2018":-15,"FY2017":-82,"FY2016":2,"FY2015":-66}),
    ("TOTAL", "Profit/(loss) after tax from continuing operations", {"FY2025":175,"FY2024":621,"FY2023":-1793,"FY2022":-685,"FY2021":-5343,
     "FY2020":203,"FY2019":295,"FY2018":59,"FY2017":-262,"FY2016":-328,"FY2015":-118}),
    ("SECTION", "Discontinued operations (each year's own presentation - see note; FY2015/FY2018/FY2021-23 have none)", None),
    ("DATA", "Loss before tax from discontinued operations", {"FY2025":-397,"FY2024":-773,
     "FY2020":10,"FY2019":53,"FY2017":0,"FY2016":132}),
    ("DATA", "Income tax (expense)/benefit from discontinued operations", {"FY2025":-2,"FY2024":65,
     "FY2020":-2,"FY2019":-12,"FY2017":0,"FY2016":0}),
    ("TOTAL", "Loss after tax from discontinued operations", {"FY2025":-399,"FY2024":-708,
     "FY2020":8,"FY2019":41,"FY2017":0,"FY2016":132}),
    ("TOTAL", "Profit/(loss) for the year", {"FY2025":-224,"FY2024":-87,"FY2023":-1793,"FY2022":-685,"FY2021":-5343,
     "FY2020":211,"FY2019":336,"FY2018":59,"FY2017":-262,"FY2016":-196,"FY2015":-118}),
    ("SECTION", "Other comprehensive income/(loss)", None),
    ("DATA", "Other comprehensive income/(loss) for the period, net of tax", {"FY2025":-5,"FY2024":-108,"FY2023":-48,"FY2022":-241,"FY2021":-33,
     "FY2020":2,"FY2019":-100,"FY2018":-11,"FY2017":2,"FY2016":0,"FY2015":2}),
    ("TOTAL", "Total comprehensive income/(loss) for the year", {"FY2025":-229,"FY2024":-195,"FY2023":-1841,"FY2022":-926,"FY2021":-5376,
     "FY2020":213,"FY2019":236,"FY2018":48,"FY2017":-260,"FY2016":-196,"FY2015":-116}),
]
income_statement_rows = [
    (kind, label, ({} if values is None else {y: flow(v, y) for y, v in values.items()}))
    for kind, label, values in PL_ROWS_USD
]

bw.add_income_statement_sheet(
    title="Credit Suisse International — Consolidated Statement of Income",
    subtitle="£m, converted from USD - Group basis - see source note at bottom for FX methodology and rates used.",
    rows=income_statement_rows,
    sources_text=STATEMENTS_SOURCES_NOTE,
    first_col_width=90,
    source_height=340,
    unit_suffix=" (£m, conv. from USD)",
)

# ---------------------------------------------------------------
# Statement of Changes in Equity - built year-by-year per the map's
# per-year reconciliation ladder: each TOTAL "At 31 December YYYY" row
# below was checked to tie to (a) its own component's Balance Sheet
# figure above and (b) the following year's own opening row, in USD,
# before conversion. A "FX translation effect" plug row (Total column
# only, computed as the balancing figure - same treatment as this
# entity's own Cash Flow FX plug and the precedent set by
# build_bank_mandiri_europe.py / build_bank_saderat.py) makes each
# year's roll-forward tie exactly in GBP too, since opening/movement/
# closing are converted at 3 different point-in-time rates.
# ---------------------------------------------------------------
EQUITY_HEADERS = ["Share capital", "Share premium", "Capital contribution", "Other equity instruments", "Retained earnings", "AOCI", "Total"]
EQUITY_ROWS_USD = [
    # --- FY2015-FY2020 added for HD-020 ---
    ("TOTAL", "At 1 January 2015", [13108,12699,None,None,-1774,-4,24029], "spot", "FY2014"),
    ("DATA", "Loss for the year (FY2015)", [None,None,None,None,-118,None,-118], "avg", "FY2015"),
    ("DATA", "Foreign exchange translation differences (FY2015)", [None,None,None,None,None,-2,-2], "avg", "FY2015"),
    ("DATA", "Cash flow hedges - reclassified to profit or loss (FY2015)", [None,None,None,None,None,4,4], "avg", "FY2015"),
    ("TOTAL", "Total comprehensive loss for the year (FY2015)", [None,None,None,None,-118,2,-116], "avg", "FY2015"),
    ("DATA", "Issue of ordinary shares (FY2015)", [8,5,None,None,None,None,13], "avg", "FY2015"),
    ("DATA", "Capital reduction of ordinary shares (FY2015)", [-750,None,None,None,None,None,-750], "avg", "FY2015"),
    ("DATA", "Decrease in retained earnings due to purchase of business from a common control entity (FY2015)", [None,None,None,None,-272,None,-272], "avg", "FY2015"),
    ("DATA", "FX translation effect on equity, net (FY2015)", [None,None,None,None,None,None,None], "plug", "FY2015"),
    ("TOTAL", "At 31 December 2015", [12366,12704,None,None,-2164,-2,22904], "spot", "FY2015"),

    ("DATA", "Loss for the year (FY2016)", [None,None,None,None,-196,None,-196], "avg", "FY2016"),
    ("TOTAL", "Total comprehensive loss for the year (FY2016)", [None,None,None,None,-196,None,-196], "avg", "FY2016"),
    ("DATA", "FX translation effect on equity, net (FY2016)", [None,None,None,None,None,None,None], "plug", "FY2016"),
    ("TOTAL", "At 31 December 2016", [12366,12704,None,None,-2360,-2,22708], "spot", "FY2016"),

    ("DATA", "Loss for the year (FY2017)", [None,None,None,None,-262,None,-262], "avg", "FY2017"),
    ("DATA", "Foreign exchange translation differences (FY2017)", [None,None,None,None,None,2,2], "avg", "FY2017"),
    ("TOTAL", "Total comprehensive loss for the year (FY2017)", [None,None,None,None,-262,2,-260], "avg", "FY2017"),
    ("DATA", "Additional paid in capital (FY2017)", [None,None,None,None,30,None,30], "avg", "FY2017"),
    ("DATA", "FX translation effect on equity, net (FY2017)", [None,None,None,None,None,None,None], "plug", "FY2017"),
    ("TOTAL", "At 31 December 2017", [12366,12704,None,None,-2592,0,22478], "spot", "FY2017"),

    ("DATA", "Prior period restatement of retained earnings (per FY2018 AR Note 49 - not in FY2017's own report)", [None,None,None,None,137,None,137], "spot", "FY2017"),
    ("DATA", "Adjustment on initial application of IFRS 15, net of tax (FY2018)", [None,None,None,None,-10,None,-10], "spot", "FY2017"),
    ("DATA", "Adjustment on initial application of IFRS 9, net of tax (FY2018)", [None,None,None,None,25,-18,7], "spot", "FY2017"),
    ("DATA", "Net profit for the period (FY2018)", [None,None,None,None,59,None,59], "avg", "FY2018"),
    ("DATA", "Gains on designated financial liabilities relating to credit risk (FY2018)", [None,None,None,None,None,1,1], "avg", "FY2018"),
    ("DATA", "Cash flow hedges - effective portion of changes in fair value (FY2018)", [None,None,None,None,None,-12,-12], "avg", "FY2018"),
    ("TOTAL", "Total comprehensive gain for the period (FY2018)", [None,None,None,None,59,-11,48], "avg", "FY2018"),
    ("DATA", "FX translation effect on equity, net (FY2018)", [None,None,None,None,None,None,None], "plug", "FY2018"),
    ("TOTAL", "At 31 December 2018", [12366,12704,None,None,-2381,-29,22660], "spot", "FY2018"),

    ("DATA", "Adjustment on initial application of IFRS 16, net of tax (FY2019)", [None,None,None,None,21,None,21], "spot", "FY2018"),
    ("DATA", "Net profit for the year (FY2019)", [None,None,None,None,336,None,336], "avg", "FY2019"),
    ("DATA", "Realised gain/(loss) on designated FL reclassed to retained earnings (FY2019)", [None,None,None,None,-8,8,0], "avg", "FY2019"),
    ("DATA", "Related tax on Realised losses relating to credit risk on designated FL (FY2019)", [None,None,None,None,2,None,2], "avg", "FY2019"),
    ("DATA", "Unrealised loss on designated FL relating to credit risk (FY2019)", [None,None,None,None,None,-13,-13], "avg", "FY2019"),
    ("DATA", "Cash flow hedges - effective portion of changes in fair value (FY2019)", [None,None,None,None,None,21,21], "avg", "FY2019"),
    ("DATA", "Transfer UK Pension Fund from CSS(E)L (FY2019)", [None,None,1165,None,None,None,1165], "avg", "FY2019"),
    ("DATA", "Related tax on transfer UK Pension Fund from CSS(E)L (FY2019)", [None,None,-291,None,None,None,-291], "avg", "FY2019"),
    ("DATA", "Remeasurement of defined benefit pension assets (FY2019)", [None,None,None,None,None,-154,-154], "avg", "FY2019"),
    ("DATA", "Related tax on remeasurement of defined benefit pension assets (FY2019)", [None,None,None,None,None,38,38], "avg", "FY2019"),
    ("DATA", "Gain on loan sale to CSD (FY2019)", [None,None,None,None,2,None,2], "avg", "FY2019"),
    ("DATA", "Related tax on gain on loan sale to CSD (FY2019)", [None,None,None,None,-1,None,-1], "avg", "FY2019"),
    ("TOTAL", "Total comprehensive gain for the period (FY2019)", [None,None,875,None,330,-100,1105], "avg", "FY2019"),
    ("DATA", "Capital reduction of ordinary shares (FY2019)", [-1000,None,None,None,None,None,-1000], "avg", "FY2019"),
    ("DATA", "FX translation effect on equity, net (FY2019)", [None,None,None,None,None,None,None], "plug", "FY2019"),
    ("TOTAL", "At 31 December 2019", [11366,12704,875,None,-2030,-129,22786], "spot", "FY2019"),

    ("DATA", "Net profit for the year (FY2020)", [None,None,None,None,211,None,211], "avg", "FY2020"),
    ("DATA", "Realised gain/(loss) on designated FL reclassed to retained earnings (FY2020)", [None,None,None,None,-4,4,0], "avg", "FY2020"),
    ("DATA", "Related tax on Realised losses relating to credit risk on designated FL (FY2020)", [None,None,None,None,1,None,1], "avg", "FY2020"),
    ("DATA", "Unrealised loss on designated FL relating to credit risk (FY2020)", [None,None,None,None,None,-6,-6], "avg", "FY2020"),
    ("DATA", "Cash flow hedges - effective portion of changes in fair value (FY2020)", [None,None,None,None,None,24,24], "avg", "FY2020"),
    ("DATA", "Related tax on Cash flow hedges - effective portion of changes in fair value (FY2020)", [None,None,None,None,None,-6,-6], "avg", "FY2020"),
    ("DATA", "Gain on business transfer to other CS entities (FY2020)", [None,None,9,None,None,None,9], "avg", "FY2020"),
    ("DATA", "Remeasurement of defined benefit pension assets (FY2020)", [None,None,None,None,None,-24,-24], "avg", "FY2020"),
    ("DATA", "Related tax on remeasurement of defined benefit pension assets (FY2020)", [None,None,None,None,None,10,10], "avg", "FY2020"),
    ("DATA", "Gain on loan sale to CSD (FY2020)", [None,None,None,None,4,None,4], "avg", "FY2020"),
    ("DATA", "Related tax on gain on loan sale to CSD (FY2020)", [None,None,None,None,-1,None,-1], "avg", "FY2020"),
    ("DATA", "Related taxes on initial application of IFRS16 due to tax rate changes (FY2020)", [None,None,None,None,-1,None,-1], "avg", "FY2020"),
    ("TOTAL", "Total comprehensive gain for the period (FY2020)", [None,None,12,None,207,2,221], "avg", "FY2020"),
    ("DATA", "Share premium reclassification to retained earnings (FY2020)", [None,-12704,None,None,12704,None,0], "avg", "FY2020"),
    ("TOTAL", "At 31 December 2020", [11366,0,887,0,10881,-127,23007], "spot", "FY2020"),
    # --- FY2021-FY2025 (existing) ---
    ("DATA", "Net loss for the year (FY2021)", [None,None,None,None,-5343,None,-5343], "avg", "FY2021"),
    ("DATA", "Realised gain/(loss) on designated FL reclassed to retained earnings (FY2021)", [None,None,None,None,-2,2,0], "avg", "FY2021"),
    ("DATA", "Unrealised gain on designated FL relating to credit risk (FY2021)", [None,None,None,None,None,10,10], "avg", "FY2021"),
    ("DATA", "Cash flow hedges - effective portion of changes in fair value (FY2021)", [None,None,None,None,None,-45,-45], "avg", "FY2021"),
    ("DATA", "Related tax on cash flow hedges (FY2021)", [None,None,None,None,None,9,9], "avg", "FY2021"),
    ("DATA", "Remeasurement of defined benefit pension assets (FY2021)", [None,None,None,None,None,-29,-29], "avg", "FY2021"),
    ("DATA", "Related tax on remeasurement of defined benefit pension assets (FY2021)", [None,None,None,None,None,20,20], "avg", "FY2021"),
    ("TOTAL", "Total comprehensive loss for the year (FY2021)", [None,None,None,None,-5345,-33,-5378], "avg", "FY2021"),
    ("DATA", "FX translation effect on equity, net (FY2021)", [None,None,None,None,None,None,None], "plug", "FY2021"),
    ("TOTAL", "At 31 December 2021", [11366,None,887,0,5536,-160,17629], "spot", "FY2021"),

    ("DATA", "Net loss for the year (FY2022)", [None,None,None,None,-685,None,-685], "avg", "FY2022"),
    ("DATA", "Realised gain/(loss) on designated FL reclassed to retained earnings (FY2022)", [None,None,None,None,1,-1,0], "avg", "FY2022"),
    ("DATA", "Unrealised gain on designated FL relating to credit risk (FY2022)", [None,None,None,None,None,31,31], "avg", "FY2022"),
    ("DATA", "Related tax on unrealised gain (FY2022)", [None,None,None,None,None,-3,-3], "avg", "FY2022"),
    ("DATA", "Cash flow hedges - effective portion of changes in fair value (FY2022)", [None,None,None,None,None,3,3], "avg", "FY2022"),
    ("DATA", "Related tax on cash flow hedges (FY2022)", [None,None,None,None,None,-3,-3], "avg", "FY2022"),
    ("DATA", "Remeasurement of defined benefit pension assets (FY2022)", [None,None,None,None,None,-358,-358], "avg", "FY2022"),
    ("DATA", "Related tax on remeasurement of defined benefit pension assets (FY2022)", [None,None,None,None,None,90,90], "avg", "FY2022"),
    ("TOTAL", "Total comprehensive loss for the year (FY2022)", [None,None,None,None,-684,-241,-925], "avg", "FY2022"),
    ("DATA", "Additional Tier 1 Capital issuance (FY2022)", [None,None,None,1200,None,None,1200], "avg", "FY2022"),
    ("DATA", "FX translation effect on equity, net (FY2022)", [None,None,None,None,None,None,None], "plug", "FY2022"),
    ("TOTAL", "At 31 December 2022", [11366,None,887,1200,4852,-401,17904], "spot", "FY2022"),

    ("DATA", "Net loss for the year (FY2023)", [None,None,None,None,-1793,None,-1793], "avg", "FY2023"),
    ("DATA", "Unrealised loss on designated FL relating to credit risk (FY2023)", [None,None,None,None,None,-23,-23], "avg", "FY2023"),
    ("DATA", "Related tax on unrealised loss (FY2023)", [None,None,None,None,None,3,3], "avg", "FY2023"),
    ("DATA", "Cash flow hedges - effective portion of changes in fair value (FY2023)", [None,None,None,None,None,12,12], "avg", "FY2023"),
    ("DATA", "Remeasurement of defined benefit pension assets (FY2023)", [None,None,None,None,None,-56,-56], "avg", "FY2023"),
    ("DATA", "Related tax on remeasurement of defined benefit pension assets (FY2023)", [None,None,None,None,None,16,16], "avg", "FY2023"),
    ("TOTAL", "Total comprehensive loss for the year (FY2023)", [None,None,None,None,-1793,-48,-1841], "avg", "FY2023"),
    ("DATA", "Capital reduction (FY2023)", [-4099,None,None,None,4099,None,0], "avg", "FY2023"),
    ("DATA", "Dividend payment (FY2023)", [None,None,None,None,-1100,None,-1100], "avg", "FY2023"),
    ("DATA", "FX translation effect on equity, net (FY2023)", [None,None,None,None,None,None,None], "plug", "FY2023"),
    ("TOTAL", "At 31 December 2023", [7267,None,887,1200,6058,-449,14963], "spot", "FY2023"),

    ("DATA", "Net loss for the year (FY2024)", [None,None,None,None,-87,None,-87], "avg", "FY2024"),
    ("DATA", "Realised gain/(loss) on designated FL reclassed to retained earnings (FY2024)", [None,None,None,None,-1,1,0], "avg", "FY2024"),
    ("DATA", "Unrealised gain on designated FL relating to credit risk (FY2024)", [None,None,None,None,None,3,3], "avg", "FY2024"),
    ("DATA", "Cash flow hedges - effective portion of changes in fair value (FY2024)", [None,None,None,None,None,-3,-3], "avg", "FY2024"),
    ("DATA", "Remeasurement of defined benefit pension assets (FY2024)", [None,None,None,None,None,-152,-152], "avg", "FY2024"),
    ("DATA", "Related tax on remeasurement of defined benefit pension assets (FY2024)", [None,None,None,None,None,43,43], "avg", "FY2024"),
    ("TOTAL", "Total comprehensive loss for the year (FY2024)", [None,None,None,None,-88,-108,-196], "avg", "FY2024"),
    ("DATA", "Capital reduction (FY2024)", [-5899,None,None,None,None,None,-5899], "avg", "FY2024"),
    ("DATA", "Additional Tier 1 capital repatriation (FY2024)", [None,None,None,-1200,None,None,-1200], "avg", "FY2024"),
    ("DATA", "Interest payment on Additional Tier 1 capital (FY2024)", [None,None,None,None,-466,None,-466], "avg", "FY2024"),
    ("DATA", "Related tax on interest payment on Additional Tier 1 capital (FY2024)", [None,None,None,None,107,None,107], "avg", "FY2024"),
    ("DATA", "Gain on transfer of business to UBS Group entities (FY2024)", [None,None,30,None,None,None,30], "avg", "FY2024"),
    ("DATA", "FX translation effect on equity, net (FY2024)", [None,None,None,None,None,None,None], "plug", "FY2024"),
    ("TOTAL", "At 31 December 2024", [1368,None,917,0,5611,-557,7339], "spot", "FY2024"),

    ("DATA", "Net loss for the year (FY2025)", [None,None,None,None,-224,None,-224], "avg", "FY2025"),
    ("DATA", "Remeasurement of defined benefit pension assets (FY2025)", [None,None,None,None,None,-7,-7], "avg", "FY2025"),
    ("DATA", "Related tax on remeasurement of defined benefit pension assets (FY2025)", [None,None,None,None,None,2,2], "avg", "FY2025"),
    ("TOTAL", "Total comprehensive loss for the year (FY2025)", [None,None,None,None,-224,-5,-229], "avg", "FY2025"),
    ("DATA", "Capital reduction (FY2025)", [-1367,None,None,None,None,None,-1367], "avg", "FY2025"),
    ("DATA", "Loss on transfer of leases to UBS Group entities (FY2025)", [None,None,-13,None,None,None,-13], "avg", "FY2025"),
    ("DATA", "Dividend payment (FY2025)", [None,None,None,None,-2400,None,-2400], "avg", "FY2025"),
    ("DATA", "Pension asset transfer to UBS Group entities, as dividend (FY2025)", [None,None,None,None,-437,None,-437], "avg", "FY2025"),
    ("DATA", "Tax on pension asset transfer to UBS Group entities (FY2025)", [None,None,None,None,122,None,122], "avg", "FY2025"),
    ("DATA", "AOCI on pension transferred to reserves, net of tax (FY2025)", [None,None,None,None,-562,562,0], "avg", "FY2025"),
    ("DATA", "FX translation effect on equity, net (FY2025)", [None,None,None,None,None,None,None], "plug", "FY2025"),
    ("TOTAL", "At 31 December 2025", [1,None,904,0,2110,0,3015], "spot", "FY2025"),
]
# FX translation plug values (£m) - computed as: closing (spot) - opening (spot, prior year-end) -
# sum of that year's movements (average rate). Not hardcoded blind; independently derived and
# cross-checked to make each year's roll-forward tie exactly - see map.md's Notes for the method.
FX_PLUG_GBP = {
    "FY2021": 107.6, "FY2022": 1539.7, "FY2023": -683.7, "FY2024": 76.5, "FY2025": -344.7,
    # Added for HD-020 (FY2015-FY2020) - derived the same way: closing (spot) minus
    # opening (spot, prior year-end) minus that year's movements (average rate).
    "FY2015": 796.6, "FY2016": 3146.1, "FY2017": -1640.7, "FY2018": 972.9,
    "FY2019": -595.8, "FY2020": -579.8,
}

equity_changes_rows = []
for kind, label, vals, rtype, ry in EQUITY_ROWS_USD:
    if rtype == "plug":
        row_vals = [None] * (len(EQUITY_HEADERS) - 1) + [FX_PLUG_GBP[ry]]
    else:
        rate = FX_SPOT[ry] if rtype == "spot" else FX_AVG[ry]
        row_vals = [None if v is None else round(v / rate, 1) for v in vals]
    equity_changes_rows.append((kind, label, row_vals))

EQUITY_SOURCES = (
    STATEMENTS_SOURCES_NOTE + "\n\n"
    "FX METHODOLOGY FOR THIS SHEET: opening balances converted at the prior year-end's spot rate, movement "
    "lines at that year's average rate, closing balances at that year-end's spot rate - the same convention "
    "used throughout this workbook. Converting stocks and flows at 3 different rates within one year means the "
    "roll-forward doesn't tie exactly in GBP even though it ties exactly in USD (independently verified against "
    "each year's own source table before conversion) - an explicit 'FX translation effect on equity, net' row "
    "(Total column only, computed as the balancing figure) is included each year, same treatment as this "
    "entity's own Cash Flow Statement's 'Effect of GBP/USD translation' line."
)

bw.add_equity_changes_sheet(
    title="Credit Suisse International — Consolidated Statement of Changes in Equity",
    subtitle="£m, converted from USD - Group basis - chronological, oldest to newest. See source note for FX methodology.",
    headers=EQUITY_HEADERS,
    rows=equity_changes_rows,
    sources_text=EQUITY_SOURCES,
    first_col_width=56,
    source_height=340,
)

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
NET_OPERATING_USD = {"FY2025": 7865, "FY2024": 8673, "FY2023": 11387, "FY2022": 21276, "FY2021": -14340,
                      "FY2020": -13750, "FY2019": 2371, "FY2018": 1236, "FY2017": 16294, "FY2016": -3837, "FY2015": -1683}
NET_INVESTING_USD = {"FY2025": 4, "FY2024": 1, "FY2023": -26, "FY2022": -165, "FY2021": -180,
                      "FY2020": -137, "FY2019": -241, "FY2018": -82, "FY2017": -152, "FY2016": -191, "FY2015": -472}
NET_FINANCING_USD = {"FY2025": -9493, "FY2024": -10409, "FY2023": -11749, "FY2022": -18419, "FY2021": 10043,
                      "FY2020": 15493, "FY2019": 685, "FY2018": -4658, "FY2017": -16392, "FY2016": 6016, "FY2015": 1798}
OPENING_CASH_USD = {"FY2025": 1840, "FY2024": 3596, "FY2023": 3883, "FY2022": 5792, "FY2021": 5792,
                     "FY2020": 4003, "FY2019": 1201, "FY2018": 4783, "FY2017": 5033, "FY2016": 12692, "FY2015": 13049}
OPENING_CASH_RATE_YEAR = {"FY2025": "FY2024", "FY2024": "FY2023", "FY2023": "FY2022", "FY2022": "FY2021", "FY2021": "FY2020",
                           "FY2020": "FY2019", "FY2019": "FY2018", "FY2018": "FY2017", "FY2017": "FY2016", "FY2016": "FY2015", "FY2015": "FY2014"}
CLOSING_CASH_USD = {"FY2025": 357, "FY2024": 1840, "FY2023": 3596, "FY2022": 3883, "FY2021": 5792,
                     "FY2020": 5792, "FY2019": 4003, "FY2018": 1201, "FY2017": 4783, "FY2016": 5033, "FY2015": 12692}

net_operating = {y: flow(v, y) for y, v in NET_OPERATING_USD.items()}
net_investing = {y: flow(v, y) for y, v in NET_INVESTING_USD.items()}
net_financing = {y: flow(v, y) for y, v in NET_FINANCING_USD.items()}
opening_cash = {y: stock(v, OPENING_CASH_RATE_YEAR[y]) for y, v in OPENING_CASH_USD.items()}
closing_cash = {y: stock(v, y) for y, v in CLOSING_CASH_USD.items()}
net_change = {y: round(net_operating[y] + net_investing[y] + net_financing[y], 1) for y in YEARS}
fx_plug = {y: round((closing_cash[y] - opening_cash[y]) - net_change[y], 1) for y in YEARS}

rows = [
    ("SECTION", "Operating activities", {}),
    ("TOTAL", "Net cash generated from/(used in) operating activities", net_operating),
    ("SECTION", "Investing activities", {}),
    ("TOTAL", "Net cash generated from/(used in) investing activities", net_investing),
    ("SECTION", "Financing activities", {}),
    ("TOTAL", "Net cash generated from/(used in) financing activities", net_financing),
    ("TOTAL", "Net change in cash and cash equivalents (before FX translation)", net_change),
    ("DATA", "Effect of GBP/USD translation (see FX methodology note - not a real cash flow)", fx_plug),
    ("DATA", "Cash and cash equivalents at beginning of period", opening_cash),
    ("TOTAL", "Cash and cash equivalents at end of period", closing_cash),
]

bw.add_cash_flow_sheet(
    title="Credit Suisse International — Consolidated Cash Flow Statement",
    subtitle="£m, converted from USD - see source note at bottom for FX methodology and rates used.",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=90,
    source_height=320,
    unit_suffix=" (£m, conv. from USD)",
)

# ---------------------------------------------------------------
# Asset Quality
# ---------------------------------------------------------------
# Note 6 "Allowance for Credit Losses" in the FY2025 Annual Report explicitly
# states "Quantitative and qualitative disclosure is not provided ... as
# there is Nil amount to report" - a narrative-only note with no IFRS 9
# stage-split table in any year's format checked, consistent with this
# entity's near-zero customer loan book ($7m-$3,411m, mostly derivatives/
# trading exposures rather than a traditional loan book). Confirmed via
# reading Note 6, not assumed.
asset_quality_rows = [
    ("DATA", "Not publicly disclosed - no IFRS 9 stage-split or credit-quality table for the loan book is "
             "published in any year's Annual Report (Note 6 'Allowance for Credit Losses' is narrative-only, "
             "confirmed by reading) - see source note.", {}),
]
ASSET_QUALITY_SOURCES = (
    "Sources - Credit Suisse International's own Note 6 'Allowance for Credit Losses' (FY2025 Annual Report, "
    f"p.60) - {AR_URLS['FY2025']} - explicitly states no quantitative disclosure is provided as there is a Nil "
    "amount to report, and describes only a narrative USD 0.6m provision release during FY2025 following asset "
    "transfers out of the CSi group. No stage-split or credit-quality-by-rating table for the loan book (Note "
    "18 'Loans and Advances') was found in this or the FY2023/FY2021 Annual Reports checked - CSI's Loans and "
    "advances line (see Balance Sheet sheet) is a small, mostly-collapsing component of a balance sheet "
    "dominated by trading/derivative exposures, not a traditional retail/commercial loan book.\n\n"
    "FY2015-FY2020 (checked for HD-020): the FY2018/FY2019/FY2020 Annual Reports (post-IFRS 9 adoption 1 Jan "
    "2018) DO publish an IFRS 9 stage-1/2/3 ECL roll-forward table (e.g. FY2020 Annual Report p.117-118) - but "
    "only for 'Financial guarantees', 'Interest-bearing deposits with banks' and 'Other assets', never for a "
    "'Loans and advances' line itself, consistent with this entity having no traditional loan book to stage-"
    "split. FY2015-FY2017 (pre-IFRS 9, incurred-loss model under IAS 39) show only a single aggregate 'Release "
    "of/(Additional) provision for credit losses' P&L line (see Profit & Loss sheet) with no stage or "
    "credit-quality-by-rating breakdown at all. No year in this window publishes the loan-book stage-split this "
    "sheet is asking for.\n\n" + ENTITY_NOTE
)
bw.add_asset_quality_sheet(
    title="Credit Suisse International — Asset Quality",
    subtitle="See source note - no quantitative credit-quality disclosure is published for this entity's loan book.",
    rows=asset_quality_rows,
    sources_text=ASSET_QUALITY_SOURCES,
    first_col_width=90,
    source_height=260,
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, note=None):
    bw.add_metric_sheet(name, unit, rows_data, p3_sources(), note=note, first_col_width=56, source_height=190)


TIER1_USD = {"FY2025": 3014, "FY2024": 6883, "FY2023": 13889, "FY2022": 15809, "FY2021": 15022,
             "FY2020": 20520, "FY2019": 20359, "FY2018": 21270, "FY2017": 21080, "FY2016": 21023, "FY2015": 21236}
TIER1_RATIO = {"FY2025": "146.9%", "FY2024": "62.9%", "FY2023": "40.0%", "FY2022": "26.0%", "FY2021": "24.0%",
               "FY2020": "19.3%", "FY2019": "26.4%", "FY2018": "20.5%", "FY2017": "20%", "FY2016": "16.6%", "FY2015": "13.0%"}
RWA_USD = {"FY2025": 2052, "FY2024": 10951, "FY2023": 34698, "FY2022": 60646, "FY2021": 62643,
           "FY2020": 106476, "FY2019": 77110, "FY2018": 103983, "FY2017": 104871, "FY2016": 126723, "FY2015": 163722}
TOTAL_CAPITAL_USD = {"FY2025": 3014, "FY2024": 6883, "FY2023": 13889, "FY2022": 15812, "FY2021": 15027,
                     "FY2020": 20536, "FY2019": 20372, "FY2018": 22267, "FY2017": 23715, "FY2016": 26741, "FY2015": 28956}
TOTAL_CAPITAL_RATIO = {"FY2025": "146.90%", "FY2024": "62.86%", "FY2023": "40.03%", "FY2022": "26.07%", "FY2021": "23.99%",
                       "FY2020": "19.3%", "FY2019": "26.4%", "FY2018": "21.4%", "FY2017": "23%", "FY2016": "21.1%", "FY2015": "17.7%"}
LEVERAGE_RATIO = {"FY2025": "53.08%", "FY2024": "21.16%", "FY2023": "17.78%", "FY2022": "12.51%", "FY2021": "7.47%",
                  "FY2020": "9.9%", "FY2019": "11.9%", "FY2018": "11.8%", "FY2017": "11.7%", "FY2016": "9.2%", "FY2015": "7.6%"}
LCR_RATIO = {"FY2025": "341.45%", "FY2024": "363.29%", "FY2023": "280.3%", "FY2022": "150.4%", "FY2021": "152.7%",
             "FY2020": "224%", "FY2019": "229%", "FY2018": "199%", "FY2017": "237%"}
# NSFR only became a disclosed KM1 line for CSi from FY2022 - the FY2022
# report's own KM1 shows "-" in its FY2021 comparative column, and FY2021's
# own report never states an NSFR figure (the term appears only in narrative
# risk-management text). FY2015-FY2020 likewise pre-date its disclosure.
NSFR_RATIO = {"FY2025": "384.98%", "FY2024": "214.78%", "FY2023": "125.6%", "FY2022": "127.5%"}

tier1_gbp = {y: stock(v, y) for y, v in TIER1_USD.items()}
rwa_gbp = {y: stock(v, y) for y, v in RWA_USD.items()}

# FY2022/FY2023 are the only two years in which CSi's CET1 differs from its
# Tier 1 capital (the $1,200m AT1 instrument was outstanding at both those
# year-ends). Both years' CET1 amount and CET1 ratio ARE separately printed on
# CSi's own Pillar 3 KM1 template - recovered 2026-09-15, see CET1_GAP_NOTE.
CET1_USD = {"FY2023": 12689, "FY2022": 14609}
CET1_RATIO = {"FY2023": "36.57%", "FY2022": "24.09%"}

CET1_GAP_NOTE = (
    "FY2022/FY2023 CET1 FILLED 2026-09-15 (was blank): CSi's own KM1 key-metrics template DOES print a "
    "separate 'Common Equity Tier 1 (CET1) capital' amount and 'Common Equity Tier 1 ratio (%)' line in every "
    "year, including the two years in which CET1 differs from Tier 1 - an earlier session's note (kept below) "
    "wrongly stated CET1 was 'NOT separately disclosed anywhere in the FY2021-FY2025 source', which was true "
    "only of the Annual Report's KPI table, not of the Pillar 3 documents. Both years were confirmed from TWO "
    "independent documents that agree exactly on the amounts: CSi Pillar 3 Disclosures 2023 (KM1, p.5; Q4 2023 "
    "CET1 $12,689m / 36.57% and its own Q4 2022 comparative CET1 $14,609m / 24.09%) and CSi Pillar 3 "
    "Disclosures 2024 (KM1, p.5; its 2023 comparative column repeats $12,689m / 36.57%) and CSi Pillar 3 "
    "Disclosures 2022 (KM1, p.5; own-year 2022 CET1 $14,609m). Each year's Tier 1 less CET1 is exactly $1,200m, "
    "matching the AT1 instrument's carrying value in the Statement of Changes in Equity.\n"
    "FY2022 RATIO BASIS: the FY2022 document's own originally-published CET1 ratio is 24.02%, computed against "
    "that document's own then-current Total RWA of $60,818m; the FY2023 document restates FY2022 RWA to "
    "$60,646m and the CET1 ratio to 24.09%. This workbook already carries the RESTATED $60,646m on its Total "
    "RWAs sheet and the restated 26.07% on its Total Capital Ratio sheet, so the restated 24.09% is used here "
    "too, keeping the sheet internally consistent (14,609/60,646 = 24.09%); the originally-published 24.02% is "
    "recorded here rather than silently dropped."
)

AT1_NOTE = (
    CET1_GAP_NOTE + "\n\n"
    "AT1 BACKGROUND (original note, retained): the Annual Report's own KPI table gives only a combined 'Tier 1 "
    "capital' figure and ratio. The Statement of Changes in Equity shows Additional Tier 1 (AT1) instruments of "
    "$1,200m outstanding at 31 Dec 2022 and 31 Dec 2023 only (issued during FY2022, repatriated during FY2024) - "
    "so CET1 = Tier 1 for FY2021/FY2024/FY2025 (confirmed zero AT1 those years), while CET1 < Tier 1 for FY2022/"
    "FY2023. FY2015-FY2020 (added for HD-020): each year's own standalone Pillar 3 "
    "disclosure states explicitly 'CSi has no AT1 capital' (or shows a combined 'Tier 1 (and CET1) capital' "
    "line, same treatment) - CSI held no Additional Tier 1 instruments at all in this window, so CET1 = Tier 1 "
    "exactly for all of FY2015-FY2020, not estimated."
)

cet1_gbp = dict(tier1_gbp)
for _y, _v in CET1_USD.items():
    cet1_gbp[_y] = stock(_v, _y)

metric(
    "CET1 Capital", "£m (conv. from USD) - see note",
    [("Common Equity Tier 1 (CET1) capital", {y: cet1_gbp[y] for y in
        ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021", "FY2020", "FY2019", "FY2018", "FY2017", "FY2016", "FY2015"]})],
    note=AT1_NOTE,
)
metric(
    "CET1 Ratio", "% - see note",
    [("CET1 Ratio", {y: CET1_RATIO.get(y, TIER1_RATIO[y]) for y in
        ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021", "FY2020", "FY2019", "FY2018", "FY2017", "FY2016", "FY2015"]})],
    note=AT1_NOTE,
)
metric(
    "Tier 1 Capital", "£m (conv. from USD)",
    [("Tier 1 capital", tier1_gbp)],
)
metric(
    "Tier 1 Ratio", "%",
    [("Tier 1 capital ratio", TIER1_RATIO)],
)
total_capital_gbp = {y: stock(v, y) for y, v in TOTAL_CAPITAL_USD.items()}
metric(
    "Total Capital", "£m (conv. from USD) - see note",
    [("Total capital", total_capital_gbp)],
    note="FY2021-FY2024 added 2026-09-12: a prior session's claim that the standalone Pillar 3 document was "
         "'not locatable' for these years was WRONG - CSi's own Pillar 3 KM1 template publishes Total capital "
         "('own funds') every year. FY2021/FY2022 recovered from the pre-migration credit-suisse.com URL "
         "pattern via Wayback; FY2023/FY2024 from the UBS-hosted documents already cited on the RWA Breakdown "
         "sheet (which had used them for OV1 data while these capital sheets still claimed they didn't exist). "
         "FY2025 added 2026-09-15 from that same KM1 template (p.6), obtained by manual browser download "
         "after ubs.com blocked scripted access - see this sheet's source note. FY2015-FY2020 (HD-020): "
         "each year's own standalone Pillar 3 disclosure, located via Wayback Machine.",
)
metric(
    "Total Capital Ratio", "% - see note",
    [("Total Capital Ratio", TOTAL_CAPITAL_RATIO)],
    note="FY2021-FY2024 added 2026-09-12 from CSi's own Pillar 3 KM1 template - see Total Capital sheet note "
         "for how the documents were recovered. FY2025 added 2026-09-15 from that document's KM1 (p.6). "
         "NOTE on FY2022: CSi restated its "
         "own FY2022 Total RWA between reports (FY2022's own report states $60,818m; the FY2023 report's "
         "FY2022 comparative states $60,646m). This workbook's Total RWAs sheet already carries the restated "
         "$60,646m, so the FY2022 ratio shown here is the FY2023 report's 26.07% (= 15,812/60,646) rather than "
         "the FY2022 report's own 26.00% (= 15,812/60,818), keeping capital / RWA / ratio internally consistent "
         "across the three sheets. FY2015-FY2020 sourced from each year's own standalone Pillar 3 disclosure.",
)
metric(
    "Total RWAs", "£m (conv. from USD)",
    [("Risk Weighted Assets", rwa_gbp)],
)

# RWA Breakdown - the FY2025 Annual Report's KPI table only gives the single
# aggregate Total RWAs figure already used above, but CSI's own standalone
# Pillar 3 document (explicitly referenced in the Annual Report at ubs.com,
# see p3_sources()) DOES publish a full OV1 category breakdown for every
# year - a revisit found it under UBS's post-migration URL pattern
# (ubs.com/.../regulatory-directory/international/... for FY2024/FY2025;
# the pre-migration ubs.com/.../archive-credit-suisse/... pattern still
# serves FY2021-FY2023). "Amounts below the thresholds for deduction" is
# explicitly labelled "(For information)" in CSI's own OV1 table in every
# year - a memo item already folded into Credit risk above, not additive to
# Total - reproduced here as a memo row for the same reason. All 5 years'
# additive category rows sum to that year's own disclosed Total RWAs figure
# (cross-checked in USD before conversion), which also ties exactly to the
# Total RWAs sheet.

RWA_BD_USD = {
    "Credit risk (excluding CCR)": {"FY2025": 266, "FY2024": 810, "FY2023": 4338, "FY2022": 7086, "FY2021": 7424,
                                     "FY2020": 6630, "FY2019": 9620, "FY2018": 5870, "FY2017": 7638},
    "Counterparty credit risk (CCR)": {"FY2025": 21, "FY2024": 3558, "FY2023": 14628, "FY2022": 24912, "FY2021": 23717,
                                        "FY2020": 42127, "FY2019": 40493, "FY2018": 58517, "FY2017": 62136},
    "Settlement risk": {"FY2025": 1, "FY2024": 0, "FY2023": 19, "FY2022": 55, "FY2021": 100,
                         "FY2020": 70, "FY2019": 72, "FY2018": 0, "FY2017": 7},
    "Securitisation exposures in the non-trading book": {"FY2025": 0, "FY2024": 0, "FY2023": 26, "FY2022": 0, "FY2021": 67,
                                                           "FY2020": 66, "FY2019": 69, "FY2018": 1, "FY2017": 797},
    "Position, foreign exchange and commodities risks (Market risk)": {"FY2025": 82, "FY2024": 3706, "FY2023": 9711, "FY2022": 17116, "FY2021": 22546,
                                                                         "FY2020": 24456, "FY2019": 15371, "FY2018": 21592, "FY2017": 21710},
    "Large exposures": {"FY2025": 0, "FY2024": 0, "FY2023": 2210, "FY2022": 6970, "FY2021": 4240,
                         "FY2020": 23853, "FY2019": 7563, "FY2018": 14191, "FY2017": 9044},
    "Operational risk": {"FY2025": 1682, "FY2024": 2877, "FY2023": 3767, "FY2022": 4507, "FY2021": 4550,
                          "FY2020": 3773, "FY2019": 3181, "FY2018": 2875, "FY2017": 2669},
    "Amounts below thresholds for deduction (subject to 250% risk weight) - memo, already included above, not additive to Total": {
        "FY2025": 0, "FY2024": 96, "FY2023": 96, "FY2022": 407, "FY2021": 864,
        "FY2020": 683, "FY2019": 741, "FY2018": 937, "FY2017": 870},
}
rwa_bd_gbp = {label: {y: stock(v, y) for y, v in yrs.items()} for label, yrs in RWA_BD_USD.items()}

# FY2015-FY2016 pre-date the OV1 template - CSI's own Pillar 3 disclosures for
# those years use the older Basel II/III-era 3-category RWA table (Total
# credit and counterparty risk / Total market risk / Total other risks), which
# doesn't map cleanly onto the 8-line OV1 categories above. Per HD-020's
# instruction to flag this as a caveat rather than force a mapping, these two
# years are carried as a SEPARATE set of rows using their own disclosed
# category names, populated only for FY2015/FY2016 (blank for all OV1-era
# years). Each year's components sum to that year's own disclosed Total RWAs
# figure (cross-checked in USD): FY2016 = 87452+24441+14830 = 126723;
# FY2015 = 109129+28840+25753 = 163722. Both tie exactly to the Total RWAs sheet.
RWA_BD_OLD_USD = {
    "Total credit and counterparty risk (incl. CVA/settlement)": {"FY2016": 87452, "FY2015": 109129},
    "Total market risk": {"FY2016": 24441, "FY2015": 28840},
    "Total other risks (incl. operational risk, large exposures - trading book, default fund contributions)": {
        "FY2016": 14830, "FY2015": 25753},
}
rwa_bd_old_gbp = {label: {y: stock(v, y) for y, v in yrs.items()} for label, yrs in RWA_BD_OLD_USD.items()}

rwa_breakdown_rows = [
    ("SECTION", "RWA by risk category (OV1 template, FY2017-FY2025)", {}),
    ("DATA", "Credit risk (excluding CCR)", rwa_bd_gbp["Credit risk (excluding CCR)"]),
    ("DATA", "Counterparty credit risk (CCR)", rwa_bd_gbp["Counterparty credit risk (CCR)"]),
    ("DATA", "Settlement risk", rwa_bd_gbp["Settlement risk"]),
    ("DATA", "Securitisation exposures in the non-trading book",
     rwa_bd_gbp["Securitisation exposures in the non-trading book"]),
    ("DATA", "Position, foreign exchange and commodities risks (Market risk)",
     rwa_bd_gbp["Position, foreign exchange and commodities risks (Market risk)"]),
    ("DATA", "Large exposures", rwa_bd_gbp["Large exposures"]),
    ("DATA", "Operational risk", rwa_bd_gbp["Operational risk"]),
    ("DATA", "Amounts below thresholds for deduction (subject to 250% risk weight) - memo, already included "
             "above, not additive to Total",
     rwa_bd_gbp["Amounts below thresholds for deduction (subject to 250% risk weight) - memo, already included "
                "above, not additive to Total"]),
    ("SECTION", "RWA by risk category (pre-OV1 Basel II/III-era format, FY2015-FY2016 - see caveat in source note)", {}),
    ("DATA", "Total credit and counterparty risk (incl. CVA/settlement)",
     rwa_bd_old_gbp["Total credit and counterparty risk (incl. CVA/settlement)"]),
    ("DATA", "Total market risk", rwa_bd_old_gbp["Total market risk"]),
    ("DATA", "Total other risks (incl. operational risk, large exposures - trading book, default fund contributions)",
     rwa_bd_old_gbp["Total other risks (incl. operational risk, large exposures - trading book, default fund contributions)"]),
    ("TOTAL", "Total RWAs", rwa_gbp),
]
bw.add_rwa_breakdown_sheet(
    title="Credit Suisse International — RWA Breakdown",
    subtitle="Pillar 3 disclosures, £m (conv. from USD). Ties exactly to the Total RWAs sheet for 10 of 11 years - "
             "see FY2020 reconciliation note below.",
    rows=rwa_breakdown_rows,
    sources_text=(
        "Sources - Credit Suisse International's own standalone Pillar 3 disclosures, table 'OV1 - Overview of "
        "risk weighted exposure amounts' (found on ubs.com, per the Annual Report's own cross-reference - see "
        "p3_sources note on other Pillar 3 sheets for why this wasn't located in an earlier session):\n"
        f"FY2025: Credit Suisse International Pillar 3 Risk Disclosures 2025, p.10 - {CSI_P3_2025_URL}\n"
        f"FY2024: Basel III 2024 Pillar 3 Disclosures, p.11 - {CSI_P3_2024_URL}\n"
        f"FY2023: Basel III 2023 Pillar 3 Disclosures, p.10 - {CSI_P3_2023_URL}\n"
        f"FY2022: Basel III 2023 Pillar 3 Disclosures' 2022 comparative column, p.10 - {CSI_P3_2023_URL} "
        "(used instead of the 2022 disclosures' own-year column because the 2023 document's footnote states "
        "'2022 RWA numbers have been restated to align with Dec'22 COREP final submission numbers' - this "
        "restated figure is what ties to the Total RWAs sheet's FY2022 figure)\n"
        f"FY2021: Basel III 2022 Pillar 3 Disclosures' 2021 comparative column, p.10 - {CSI_P3_2022_URL}\n\n"
        "FY2015-FY2020 (added for HD-020) - CSI's own standalone Pillar 3 disclosures, located via Wayback "
        "Machine (no longer hosted live at credit-suisse.com following the 2023 UBS acquisition/site migration - "
        "see p3_sources note on other Pillar 3 sheets for the full URL list and page references):\n"
        "FY2020: csi-pillar-3-disclosures-2020.pdf, OV1 table\n"
        "FY2019: csi-pillar-3-disclosures-2019.pdf, OV1 table\n"
        "FY2018: csi-pillar-3-disclosures-2018.pdf, OV1 table\n"
        "FY2017: csi-pillar-3-disclosures-2017.pdf, OV1 table\n"
        "FY2016: csi-pillar-3-disclosures-2016.pdf, own-format RWA table (pre-OV1)\n"
        "FY2015: csi-pillar-3-disclosures-2015.pdf, own-format RWA table (pre-OV1)\n\n"
        "FY2020 RECONCILIATION NOTE: the FY2020 Pillar 3 document's own OV1 table sums to $101,658m, which does "
        "NOT match the same document's capital-composition table Total RWA figure of $106,476m used on the Total "
        "RWAs/CET1 Ratio/Tier 1 Ratio/Total Capital Ratio sheets (a $4,818m gap, cause not stated in the source). "
        "Per this workbook's existing precedent for the FY2022 RWA restatement above, the capital-composition "
        "table's figure is treated as authoritative for the ratio sheets, while this Breakdown sheet reproduces "
        "the OV1 table's own component figures as-disclosed (which is why the FY2020 column of this sheet's "
        "OV1 rows sums to $101,658m rather than to the $106,476m Total RWAs row above it - a genuine internal "
        "inconsistency in CSI's own FY2020 disclosure, not a transcription error here).\n\n"
        "BASEL II/III-ERA CAVEAT (FY2015-FY2016): these two years' own Pillar 3 disclosures use an older "
        "3-category RWA table (Total credit and counterparty risk / Total market risk / Total other risks) that "
        "pre-dates the OV1 template introduced under CRR/Basel III Pillar 3 rules - the categories don't map "
        "cleanly onto the 8 OV1 rows above, so they're shown as their own separate section using their own "
        "disclosed category names rather than force-fit into the newer template. Both years' components sum "
        "exactly to that year's own Total RWAs figure.\n\n"
        "Converted from USD to GBP using the same FX methodology as the Cash Flow Statement sheet (SPOT rate "
        "at each year-end).\n" + FX_METHOD_NOTE
    ),
    first_col_width=90,
    source_height=340,
    unit_suffix=" (£m, conv. from USD)",
)

metric(
    "Leverage Ratio", "% - see note",
    [("Leverage Ratio", LEVERAGE_RATIO)],
    note="FY2021-FY2024 added 2026-09-12 from the 'Leverage ratio' line of CSi's own Pillar 3 KM1 template - "
         "the prior 'not locatable' claim was wrong (see Total Capital sheet note). The Annual Report itself "
         "still doesn't carry a leverage ratio; these come from the Pillar 3 documents. FY2025 added "
         "2026-09-15 from that same KM1 line (p.6). FY2015-FY2020 (HD-020) sourced from each year's own "
         "standalone Pillar 3 disclosure.",
)
metric(
    "LCR", "% - see note",
    [("Liquidity Coverage Ratio", LCR_RATIO)],
    note="FY2021-FY2024 added 2026-09-12 from the 'Liquidity coverage ratio (%)' line of CSi's own Pillar 3 "
         "KM1 template - the prior 'not locatable' claim was wrong (see Total Capital sheet note). Each is the "
         "12-month-average LCR as that year's KM1 states it. FY2021's figure (152.7%) is taken from the FY2022 "
         "report's own FY2021 comparative column; FY2021's own report presents the same metric only as four "
         "quarterly averages (Q4 2021: 153%), so the comparative is the like-for-like annual figure. FY2025 "
         "added 2026-09-15 from that same KM1 line (p.6). FY2015-FY2016 genuinely pre-date the LCR's phased-in "
         "UK application. FY2017-FY2020 "
         "sourced from each year's own standalone Pillar 3 disclosure (located via Wayback Machine).",
)
metric(
    "NSFR", "% - see note",
    [("Net Stable Funding Ratio", NSFR_RATIO)],
    note="FY2022-FY2024 added 2026-09-12 from the 'NSFR ratio (%)' line of CSi's own Pillar 3 KM1 template - "
         "the prior blanket 'not disclosed for any year' claim was wrong for these three years (see Total "
         "Capital sheet note for how the documents were recovered). FY2021 and earlier are a genuine "
         "non-disclosure rather than an access gap: the FY2022 report's own KM1 prints '-' in its FY2021 NSFR "
         "comparative column, and FY2021's own report mentions the NSFR only in narrative risk-management text "
         "with no figure. FY2025 added 2026-09-15 from that same KM1 line (p.6) - see this sheet's source note.",
)
bw.add_not_disclosed_metric_sheets(
    ["MREL Ratio"],
    p3_sources(),
    per_note={"MREL Ratio": "Not publicly disclosed for any year FY2015-FY2025, and not expected to be: CSi is "
                            "not a UK resolution entity, so no entity-level MREL requirement applies to it. "
                            "Re-checked 2026-09-12 against the recovered FY2021-FY2024 Pillar 3 documents - the "
                            "term appears in none of them, nor in any Annual Report."},
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bs_by_label = {label: values for _, label, values in balance_sheet_rows}
is_by_label = {label: values for _, label, values in income_statement_rows}

OPENING_EQUITY_GBP = {"FY2021":16841.4,"FY2022":13038.2,"FY2023":14800.4,"FY2024":11752.3,"FY2025":5864.2,
                      # FY2015-FY2020 added for HD-020 - derived from BS_ROWS_USD's "Total shareholders'
                      # equity" row (prior year's closing balance) converted at that year-end's SPOT rate;
                      # FY2015's opening uses the FY2014 Annual Report's own "At 1 January 2015" balance
                      # ($24,029m) converted at the FY2014 spot rate (1.5608) since FY2014 isn't itself a
                      # sheet in this workbook. FY2020's closing (16,841.4) ties to FY2021's existing
                      # opening figure above to within GBP 2.3 (rounding), confirming the chain is correct.
                      "FY2020":17249.1,"FY2019":17746.1,"FY2018":16638.0,"FY2017":18457.3,"FY2016":15455.8,
                      "FY2015":15395.3}
CLOSING_EQUITY_GBP = {"FY2021":13038.2,"FY2022":14800.4,"FY2023":11752.3,"FY2024":5864.2,"FY2025":2242.0,
                      "FY2020":16841.4,"FY2019":17249.1,"FY2018":17746.1,"FY2017":16638.0,"FY2016":18457.3,
                      "FY2015":15455.8}
TOTAL_COMPREHENSIVE_GBP = {"FY2021":-3910.7,"FY2022":-748.3,"FY2023":-1480.0,"FY2024":-153.3,"FY2025":-173.6,
                           "FY2020":172.2,"FY2019":865.6,"FY2018":36.0,"FY2017":-201.8,"FY2016":-144.6,
                           "FY2015":-75.9}
OTHER_EQUITY_MOVEMENTS_GBP = {
    y: round(CLOSING_EQUITY_GBP[y] - OPENING_EQUITY_GBP[y] - TOTAL_COMPREHENSIVE_GBP[y], 1) for y in YEARS
}

bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", bs_by_label["Total assets"]),
        ("Loans and advances", bs_by_label["Loans and advances"]),
        ("Borrowings", bs_by_label["Borrowings"]),
        ("Total shareholders' equity", bs_by_label["Total shareholders' equity"]),
    ],
    balance_sheet_unit="£m (conv. from USD)",
    income_statement_totals=[
        ("Net revenues", is_by_label["Net revenues"]),
        ("Total operating expenses", is_by_label["Total operating expenses"]),
        ("Profit/(loss) for the year", is_by_label["Profit/(loss) for the year"]),
    ],
    income_statement_unit="£m (conv. from USD)",
    equity_changes_totals=[
        ("Opening equity", OPENING_EQUITY_GBP),
        ("Total comprehensive income/(loss) for the year", TOTAL_COMPREHENSIVE_GBP),
        ("Other equity movements, net", OTHER_EQUITY_MOVEMENTS_GBP),
        ("Closing equity", CLOSING_EQUITY_GBP),
    ],
    equity_changes_unit="£m (conv. from USD)",
    cash_flow_totals=[
        ("Net cash generated from/(used in) operating activities", net_operating),
        ("Net cash generated from/(used in) investing activities", net_investing),
        ("Net cash generated from/(used in) financing activities", net_financing),
        ("Cash and cash equivalents at end of period", closing_cash),
    ],
    cash_flow_unit="£m (conv. from USD)",
    ratios=[
        ("Tier 1 Ratio", TIER1_RATIO),
    ],
    note="CSI is in an explicit, disclosed controlled wind-down following the 2023 Credit Suisse/UBS "
         "combination - total assets fell 97.7% from FY2021 to FY2025. Figures converted from USD to GBP; see "
         "the Cash Flow Statement sheet's source note for the full FX methodology. Figures are duplicated from "
         "the detail sheets for at-a-glance trend viewing; see each sheet's own source citation for the "
         "underlying document/page.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/CREDIT SUISSE INTERNATIONAL FINANCIALS.xlsx")
