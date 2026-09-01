import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]
YEAR_LABEL = {y: y for y in YEARS}
AR_URL = {
    "FY2025": "https://find-and-update.company-information.service.gov.uk/company/00995939/filing-history/MzUxNjA1NTA3MGFkaXF6a2N4/document?format=pdf&download=0",
    "FY2024": "https://find-and-update.company-information.service.gov.uk/company/00995939/filing-history/MzQ3MTY0MzU5OWFkaXF6a2N4/document?format=pdf&download=0",
    "FY2023": "https://find-and-update.company-information.service.gov.uk/company/00995939/filing-history/MzQxNjYxMzY5MmFkaXF6a2N4/document?format=pdf&download=0",
    "FY2022": "https://find-and-update.company-information.service.gov.uk/company/00995939/filing-history/MzM3Mzk1MDQ0MWFkaXF6a2N4/document?format=pdf&download=0",
    "FY2021": "https://find-and-update.company-information.service.gov.uk/company/00995939/filing-history/MzMzNjkyMjU2MGFkaXF6a2N4/document?format=pdf&download=0",
}
P3_URL = {
    "FY2025": "https://www.rbc.com/regulatory-information/_assets-custom/pdf/Pillar-III/rbcel-pillar-3-oct-25-final.pdf",
    "FY2024": "https://www.rbc.com/regulatory-information/_assets-custom/pdf/Pillar-III/rbcel-pillar-3-oct-24-final.pdf",
    "FY2023": "https://www.rbc.com/regulatory-information/_assets-custom/pdf/Pillar-III/RBCEL-Pillar-3-Oct-23_Final_v2.pdf",
    "FY2022": "https://www.rbc.com/regulatory-information/_assets-custom/pdf/Pillar-III/RBCEL-Annual-Pillar-3-2022.pdf",
    "FY2021": "https://www.rbc.com/regulatory-information/_assets-custom/pdf/Pillar-III/RBCEL-Annual-Pillar-3-2021.pdf",
}
ENTITY_NOTE = ("RBC Europe Limited (company 00995939, FRN 124543) is a UK authorised bank and wholly owned "
               "subsidiary of Royal Bank of Canada. The financial statements and cash flows are the Company's own "
               "entity-level figures in GBP, with October 31 year-end. The Pillar 3 disclosures are also RBC Europe "
               "Limited (RBCEL) Company-level disclosures, not consolidated Royal Bank of Canada group figures.")
CASH_FLOW_SOURCES = (
    "Sources - RBC Europe Limited's own Statement of Cash Flows, £'000 (all five filings were image-only scans; "
    "OCR'd with tesseract and cross-checked against rendered pages):\n"
    f"FY2025/FY2024: Full accounts made up to 31 October 2025, p.41 - {AR_URL['FY2025']}\n"
    f"FY2024/FY2023: Full accounts made up to 31 October 2024, p.39 - {AR_URL['FY2024']}\n"
    f"FY2023/FY2022: Full accounts made up to 31 October 2023, p.36 - {AR_URL['FY2023']}\n"
    f"FY2022/FY2021: Full accounts made up to 31 October 2022, p.34; FY2021 is the restated comparative - {AR_URL['FY2022']}\n"
    "The 2022 accounts label the FY2021 comparative as restated following an error; that restated comparative is used.\n" + ENTITY_NOTE)
def p3_sources():
    return ("Sources - RBC Europe Limited annual Pillar III disclosures, UK KM1 Key Metrics (Company basis), "
            "p.11 of the 2025/2024 disclosures, p.12 of 2023, p.13 of 2022, and FY2021 own-funds/leverage tables pp.16/21.\n" +
            "\n".join(f"{y}: {P3_URL[y]}" for y in YEARS) + "\n" + ENTITY_NOTE)

bw = BankWorkbook(bank_name="RBC Europe Limited", years=YEARS, year_label=YEAR_LABEL, header_color="0B4F6C")
rows = [
    ("SECTION", "Cash flows from operating activities", {}),
    ("TOTAL", "Net cash (outflow)/inflow from operating activities", {"FY2025": -2827725, "FY2024": -4638153, "FY2023": -1165304, "FY2022": 5441607, "FY2021": 3898171}),
    ("SECTION", "Cash flows from investing activities", {}),
    ("TOTAL", "Net cash from investing activities", {"FY2025": -1153173, "FY2024": 0, "FY2023": 0, "FY2022": 0, "FY2021": 0}),
    ("SECTION", "Cash flows from financing activities", {}),
    ("DATA", "Interest on subordinated liabilities", {"FY2025": -16674, "FY2024": -5638, "FY2023": -4890, "FY2022": -1637, "FY2021": -1354}),
    ("DATA", "Dividends on other equity", {"FY2025": -27672, "FY2024": -31277, "FY2023": -30127, "FY2022": -17648, "FY2021": -12927}),
    ("DATA", "Issue of subordinated liabilities", {"FY2025": 209396}),
    ("DATA", "Issue of common shares", {"FY2025": 1550000}),
    ("TOTAL", "Net cash inflow/(outflow) from financing activities", {"FY2025": 1715050, "FY2024": -36915, "FY2023": -35017, "FY2022": -19285, "FY2021": -14281}),
    ("DATA", "Effect of exchange rate changes on cash and due from banks (added to reach closing cash)", {"FY2025": 344323, "FY2024": -217052, "FY2023": -46137, "FY2022": 0, "FY2021": 0}),
    ("TOTAL", "Net decrease/increase in cash and cash equivalents before exchange-rate effect", {"FY2025": -2265848, "FY2024": -4675068, "FY2023": -1200321, "FY2022": 5422322, "FY2021": 3883890}),
    ("DATA", "Cash and cash equivalents at the beginning of the financial year", {"FY2025": 4455652, "FY2024": 9347772, "FY2023": 10594230, "FY2022": 5171908, "FY2021": 1288018}),
    ("TOTAL", "Cash and cash equivalents at end of year", {"FY2025": 2534127, "FY2024": 4455652, "FY2023": 9347772, "FY2022": 10594230, "FY2021": 5171908}),
]
bw.add_cash_flow_sheet(title="RBC Europe Limited — Statement of Cash Flows", subtitle="RBC Europe Limited own entity basis, £'000; source net-change line is before separately reported exchange-rate effect", rows=rows, sources_text=CASH_FLOW_SOURCES + "\nRECONCILIATION NOTE: In each year, the source's reported net decrease/increase equals operating + investing + financing cash flows before the separately presented exchange-rate effect. Closing cash equals opening cash + that net-change line + the exchange-rate effect.", first_col_width=66, source_height=230, unit_suffix=" (£'000)")
def metric(name, unit, rows_data, note=None):
    bw.add_metric_sheet(name, unit, rows_data, p3_sources(), note=note, first_col_width=52, source_height=150)


INTERIM_SOURCES = {
    "2021 H1": "https://www.rbc.com/regulatory-information/_assets-custom/pdf/Pillar-III/2021-Interim-Pillar-III-Disclosure.pdf",
    "2022 H1": "https://www.rbc.com/regulatory-information/_assets-custom/pdf/Pillar-III/2022-Interim-Pillar-III-Disclosure.pdf",
    "2023 Q1": "https://www.rbc.com/regulatory-information/_assets-custom/pdf/Pillar-III/RBCEL-Jan-2023-Pillar3-Disclosures.pdf",
    "2023 H1": "https://www.rbc.com/regulatory-information/_assets-custom/pdf/Pillar-III/RBCEL-April-2023-Semi-Annual-Pillar3-Disclosures.pdf",
    "2023 Q3": "https://www.rbc.com/regulatory-information/_assets-custom/pdf/Pillar-III/RBCEL-July2023-Pillar3-Disclosures.pdf",
    "2024 Q1": "https://www.rbc.com/regulatory-information/_assets-custom/pdf/Pillar-III/RBCEL-Pillar-3-Jan-24.pdf",
    "2024 H1": "https://www.rbc.com/regulatory-information/_assets-custom/pdf/Pillar-III/RBCEL-Pillar-3-Apr-24.pdf",
    "2024 Q3": "https://www.rbc.com/regulatory-information/_assets-custom/pdf/Pillar-III/2024-Q3-Pillar-III-Diclosure.pdf",
    "2025 Q1": "https://www.rbc.com/regulatory-information/_assets-custom/pdf/Pillar-III/2025-q1-pillar-iii-disclosure.pdf",
    "2025 H1": "https://www.rbc.com/regulatory-information/_assets-custom/pdf/Pillar-III/2025-semi-annual-pillar-iii-disclosure.pdf",
    "2025 Q3": "https://www.rbc.com/regulatory-information/_assets-custom/pdf/Pillar-III/2025-Q3-Pillar-III-Disclosure.pdf",
}


def add_interim_pillar3_sheet():
    """Add entity-level RBCEL interim observations from official disclosures."""
    headers = ["Period", "Disclosure type", "Metric", "Value", "Unit", "Basis", "Source document", "Page / table"]
    rows = []

    def add(period, disclosure_type, metric_name, value, unit, basis, page):
        rows.append((period, disclosure_type, metric_name, value, unit, basis,
                     f"RBC Europe Limited {period} Pillar III disclosure", page))

    # The 2021 and 2022 reports use the transitional/CRR-era presentation;
    # values below are the headline figures reported in their own tables.
    add("Apr-21", "Semi-annual", "Common Equity Tier 1 (CET1) capital", 1257, "£m", "Company / transitional own-funds table", "p.4, Table 2")
    add("Apr-21", "Semi-annual", "Tier 1 capital", 1557, "£m", "Company / transitional own-funds table", "p.4, Table 2")
    add("Apr-21", "Semi-annual", "Total capital", 1629, "£m", "Company / transitional own-funds table", "p.4, Table 2")
    add("Apr-21", "Semi-annual", "Total risk-weighted exposures", 8642, "£m", "Company / transitional own-funds table", "p.4, Table 2")
    add("Apr-21", "Semi-annual", "Common Equity Tier 1 ratio", "14.5%", "%", "Company / transitional own-funds table", "p.4, Table 2")
    add("Apr-21", "Semi-annual", "Tier 1 ratio", "18.0%", "%", "Company / transitional own-funds table", "p.4, Table 2")
    add("Apr-21", "Semi-annual", "Total capital ratio", "18.9%", "%", "Company / transitional own-funds table", "p.4, Table 2")
    add("Apr-21", "Semi-annual", "Total leverage ratio exposure", 47141, "£m", "Company / CRR leverage ratio disclosure", "p.5, Table 3")
    add("Apr-21", "Semi-annual", "Leverage ratio", "3.30%", "%", "Company / CRR leverage ratio disclosure", "p.5, Table 3")

    add("Apr-22", "Semi-annual", "Common Equity Tier 1 (CET1) capital", 1344, "£m", "Company / UK KM1", "p.4, Table 1")
    add("Apr-22", "Semi-annual", "Tier 1 capital", 1644, "£m", "Company / UK KM1", "p.4, Table 1")
    add("Apr-22", "Semi-annual", "Total capital", 1724, "£m", "Company / UK KM1", "p.4, Table 1")
    add("Apr-22", "Semi-annual", "Total risk-weighted exposure amount", 9759, "£m", "Company / UK KM1", "p.4, Table 1")
    add("Apr-22", "Semi-annual", "Common Equity Tier 1 ratio", "13.77%", "%", "Company / UK KM1", "p.4, Table 1")
    add("Apr-22", "Semi-annual", "Tier 1 ratio", "16.85%", "%", "Company / UK KM1", "p.4, Table 1")
    add("Apr-22", "Semi-annual", "Total capital ratio", "17.66%", "%", "Company / UK KM1", "p.4, Table 1")
    add("Apr-22", "Semi-annual", "Leverage ratio total exposure measure", 45175, "£m", "Company / UK leverage ratio key metrics", "p.4, Table 2")
    add("Apr-22", "Semi-annual", "Leverage ratio", "3.63%", "%", "Company / UK leverage ratio key metrics", "p.4, Table 2")
    add("Apr-22", "Semi-annual", "Total high-quality liquid assets (HQLA), weighted value-average", 8757, "£m", "Company / UK liquidity key metrics", "p.5, Table 3")
    add("Apr-22", "Semi-annual", "Total net cash outflows, adjusted value", 6881, "£m", "Company / UK liquidity key metrics", "p.5, Table 3")
    add("Apr-22", "Semi-annual", "Liquidity coverage ratio", "127%", "%", "Company / UK liquidity key metrics", "p.5, Table 3")
    add("Apr-22", "Semi-annual", "Total available stable funding", 16464, "£m", "Company / UK liquidity key metrics", "p.5, Table 3")
    add("Apr-22", "Semi-annual", "Total required stable funding", 16249, "£m", "Company / UK liquidity key metrics", "p.5, Table 3")
    add("Apr-22", "Semi-annual", "NSFR ratio", "101%", "%", "Company / UK liquidity key metrics", "p.5, Table 3")

    # From 2023 onward the semi-annual reports use the UK KM1 template;
    # quarterly reports publish only the leverage section.
    h1_metrics = {
        "Apr-23": ("2023 H1", 1362, 1662, 1742, 9222, "14.77%", "18.02%", "18.89%", 42658, "3.90%", 11968, 9515, "126%", 18196, 15752, "116%", "p.2, UK KM1"),
        "Apr-24": ("2024 H1", 1423, 1723, 1803, 10873, "13.09%", "15.85%", "16.85%", 42706, "4.03%", 11174, 8891, "126%", 17116, 14616, "117%", "p.2, UK KM1"),
        "Apr-25": ("2025 H1", 1810, 2110, 2185, 12120, "14.94%", "17.41%", "18.03%", 42018, "5.02%", 11462, 8198, "140%", 18113, 15959, "114%", "p.2, UK KM1"),
    }
    for period, (source_period, cet1, tier1, total, rwa, cet1r, tier1r, totalr, lev_exp, levr, hqla, net_out, lcr, asf, rsf, nsfr, page) in h1_metrics.items():
        for name, value, unit in [
            ("Common Equity Tier 1 (CET1) capital", cet1, "£m"), ("Tier 1 capital", tier1, "£m"),
            ("Total capital", total, "£m"), ("Total risk-weighted exposure amount", rwa, "£m"),
            ("Common Equity Tier 1 ratio", cet1r, "%"), ("Tier 1 ratio", tier1r, "%"),
            ("Total capital ratio", totalr, "%"), ("Leverage ratio total exposure measure excluding claims on central banks", lev_exp, "£m"),
            ("Leverage ratio excluding claims on central banks", levr, "%"),
            ("Total high-quality liquid assets (HQLA), weighted value-average", hqla, "£m"),
            ("Total net cash outflows, adjusted value", net_out, "£m"), ("Liquidity coverage ratio", lcr, "%"),
            ("Total available stable funding", asf, "£m"), ("Total required stable funding", rsf, "£m"),
            ("NSFR ratio", nsfr, "%"),
        ]:
            add(period, "Semi-annual", name, value, unit, "Company / UK KM1", page)

    quarterly = {
        "Jan-23": ("2023 Q1", "4.13%", "3.36%", "0.08%", 50486, 41191, "p.2"),
        "Jul-23": ("2023 Q3", "4.38%", "3.46%", "0.30%", 48617, 39003, "p.2"),
        "Jan-24": ("2024 Q1", "4.24%", "3.59%", "0.28%", 48253, 40359, "p.2"),
        "Jul-24": ("2024 Q3", "4.25%", "3.63%", "0.34%", 46331, 41636, "p.2"),
        "Jan-25": ("2025 Q1", "4.91%", "4.24%", "0.32%", 45272, None, "p.2"),
        "Jul-25": ("2025 Q3", "4.60%", "4.24%", "0.33%", 44665, None, "p.2"),
    }
    for period, (source_period, excl, incl, buffer, avg_incl, avg_excl, page) in quarterly.items():
        add(period, "Quarterly", "Leverage ratio excluding claims on central banks", excl, "%", "Company / leverage ratio disclosure", page)
        add(period, "Quarterly", "Leverage ratio including claims on central banks", incl, "%", "Company / leverage ratio disclosure", page)
        add(period, "Quarterly", "Leverage ratio buffer", buffer, "%", "Company / leverage ratio disclosure", page)
        add(period, "Quarterly", "Average exposure measure including claims on central banks", avg_incl, "£m", "Company / leverage ratio disclosure", page)
        if avg_excl is not None:
            add(period, "Quarterly", "Average exposure measure excluding claims on central banks", avg_excl, "£m", "Company / leverage ratio disclosure", page)

    source_period = {
        "Apr-21": "2021 H1", "Apr-22": "2022 H1",
        "Jan-23": "2023 Q1", "Apr-23": "2023 H1", "Jul-23": "2023 Q3",
        "Jan-24": "2024 Q1", "Apr-24": "2024 H1", "Jul-24": "2024 Q3",
        "Jan-25": "2025 Q1", "Apr-25": "2025 H1", "Jul-25": "2025 Q3",
    }
    hyperlinks = {
        (i, 6): INTERIM_SOURCES[source_period[rows[i][0]]]
        for i in range(len(rows))
    }
    bw.add_wide_interim_sheet(
        "Interim Pillar 3", headers, rows,
        title="RBC Europe Limited — Interim Pillar 3",
        subtitle="Entity-level interim observations from official RBC Europe Limited disclosures, April 2021 to July 2025",
        note="Annual Pillar 3 disclosures remain in the existing annual metric sheets. Quarterly RBCEL reports are limited disclosures focused on leverage; semi-annual reports provide the broader UK KM1 and liquidity metrics shown here. All amounts are £m unless stated otherwise.",
        widths=[16, 16, 58, 16, 12, 38, 48, 18],
        hyperlink_cells=hyperlinks,
    )


CET1 = {"FY2025": 1773, "FY2024": 1454, "FY2023": 1439, "FY2022": 1377, "FY2021": 1348}
T1 = {"FY2025": 2072, "FY2024": 1754, "FY2023": 1738, "FY2022": 1677, "FY2021": 1649}
TC = {"FY2025": 2358, "FY2024": 1832, "FY2023": 1821, "FY2022": 1764, "FY2021": 1721}
RWA = {"FY2025": 12834, "FY2024": 12049, "FY2023": 9579, "FY2022": 8911, "FY2021": 8961}
CET1R = {"FY2025": "13.81%", "FY2024": "12.07%", "FY2023": "15.02%", "FY2022": "15.46%", "FY2021": "15.05%"}
T1R = {"FY2025": "16.15%", "FY2024": "14.56%", "FY2023": "18.15%", "FY2022": "18.82%", "FY2021": "18.40%"}
TCR = {"FY2025": "18.37%", "FY2024": "15.20%", "FY2023": "19.01%", "FY2022": "19.80%", "FY2021": "19.21%"}
metric("CET1 Capital", "£m", [("Common Equity Tier 1 (CET1) capital", CET1)])
metric("CET1 Ratio", "% of RWA", [("Common Equity Tier 1 (CET1) ratio", CET1R)])
metric("Tier 1 Capital", "£m", [("Tier 1 capital", T1)])
metric("Tier 1 Ratio", "% of RWA", [("Tier 1 ratio", T1R)])
metric("Total Capital", "£m", [("Total capital", TC)])
metric("Total Capital Ratio", "% of RWA", [("Total capital ratio", TCR)])
metric("Total RWAs", "£m", [("Total risk-weighted exposure amount", RWA)])
metric("Leverage Ratio", "£m / %", [("Total exposure measure excluding claims on central banks", {"FY2025": 45993, "FY2024": 42872, "FY2023": 40693, "FY2022": 40753}), ("Leverage ratio excluding claims on central banks (%)", {"FY2025": "4.51%", "FY2024": "4.09%", "FY2023": "4.27%", "FY2022": "4.12%"}), ("Total leverage ratio exposure (FY2021 disclosure)", {"FY2021": 46925}), ("Leverage ratio (FY2021 disclosure)", {"FY2021": "3.51%"})], note="FY2021 uses the older CRR leverage table (total exposure £46,924.653m; ratio 3.51%). From FY2022, KM1 reports the excluding-central-bank basis; the FY2022 report shows FY2021 as N/A under that revised presentation.")
metric("LCR", "£m / %", [("Total high-quality liquid assets (HQLA), weighted value (average)", {"FY2025": 12642, "FY2024": 10688, "FY2023": 11490, "FY2022": 10868}), ("Total net cash outflows, adjusted value", {"FY2025": 9632, "FY2024": 8036, "FY2023": 9031, "FY2022": 8696}), ("Liquidity coverage ratio (%)", {"FY2025": "132%", "FY2024": "134%", "FY2023": "127%", "FY2022": "125%", "FY2021": "Not publicly disclosed"})], note="The FY2021 standalone Pillar 3 disclosure contains no LCR table or headline ratio.")
metric("NSFR", "£m / %", [("Total available stable funding", {"FY2025": 18791, "FY2024": 17010, "FY2023": 16879, "FY2022": 18964}), ("Total required stable funding", {"FY2025": 16780, "FY2024": 15158, "FY2023": 13654, "FY2022": 17081}), ("NSFR ratio (%)", {"FY2025": "112%", "FY2024": "112%", "FY2023": "124%", "FY2022": "111%", "FY2021": "Not publicly disclosed"})], note="The FY2021 standalone Pillar 3 disclosure contains no NSFR table or headline ratio.")
metric("MREL Ratio", "£m / %", [("MREL ratio", {y: "Not publicly disclosed" for y in YEARS})], note="No numeric MREL ratio was identified in the five annual RBCEL Pillar 3 disclosures reviewed.")
add_interim_pillar3_sheet()
bw.add_overview_sheet(cash_flow_totals=[("Net cash (outflow)/inflow from operating activities", {"FY2025": -2827725, "FY2024": -4638153, "FY2023": -1165304, "FY2022": 5441607, "FY2021": 3898171}), ("Net cash from investing activities", {"FY2025": -1153173, "FY2024": 0, "FY2023": 0, "FY2022": 0, "FY2021": 0}), ("Net cash inflow/(outflow) from financing activities", {"FY2025": 1715050, "FY2024": -36915, "FY2023": -35017, "FY2022": -19285, "FY2021": -14281}), ("Cash and cash equivalents at end of year", {"FY2025": 2534127, "FY2024": 4455652, "FY2023": 9347772, "FY2022": 10594230, "FY2021": 5171908})], cash_flow_unit="£'000", ratios=[("CET1 Ratio", CET1R), ("Tier 1 Ratio", T1R), ("Total Capital Ratio", TCR), ("Leverage Ratio", {"FY2025": "4.51%", "FY2024": "4.09%", "FY2023": "4.27%", "FY2022": "4.12%", "FY2021": "3.51%"}), ("LCR", {"FY2025": "132%", "FY2024": "134%", "FY2023": "127%", "FY2022": "125%"}), ("NSFR", {"FY2025": "112%", "FY2024": "112%", "FY2023": "124%", "FY2022": "111%"})], note="Figures are duplicated from the detail sheets; see those sheets for source pages, basis notes, and disclosure gaps.")
bw.save("/Users/armaan/code/katalysis/banks/RBC EUROPE FINANCIALS.xlsx")
