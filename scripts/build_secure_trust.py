import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook


YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]
AR_URLS = {
    "FY2025": "https://www.securetrustbank.com/investor-relations/document-library/reports-and-accounts-2025-final-483796420288",
    "FY2024": "https://www.securetrustbank.com/investor-relations/document-library/reports-and-accounts-2024-final",
    "FY2023": "https://www.securetrustbank.com/investor-relations/document-library/reports-and-accounts-2023-final",
    "FY2022": "https://www.securetrustbank.com/investor-relations/document-library/reports-and-accounts-2022-final",
    "FY2021": "https://www.securetrustbank.com/investor-relations/document-library/reports-and-accounts-2021-final",
}
P3_URLS = {
    y: f"https://www.securetrustbank.com/investor-relations/document-library/pillar-3-disclosure-{y[-4:]}-final"
    for y in YEARS
}
INTERIM_URLS = {
    "H1 2025": "https://www.securetrustbank.com/investor-relations/document-library/pillar-3-disclosure-2025-interim",
    "H1 2024": "https://www.securetrustbank.com/investor-relations/document-library/pillar-3-disclosure-2024-interim",
    "H1 2023": "https://www.securetrustbank.com/investor-relations/document-library/pillar-3-disclosure-2023-interim",
    "H1 2022": "https://www.securetrustbank.com/investor-relations/document-library/pillar-3-disclosure-2022-interim",
}

ENTITY_NOTE = (
    "ENTITY / BASIS NOTE: Secure Trust Bank Public Limited Company (Companies House 00541132; FRN 204550; "
    "LEI 213800CXIBLC2TMIGI76) is the exact legal entity in the supplied bank list and the PRA register. "
    "The cash-flow statement uses the consolidated Group column, matching the Group-basis Pillar 3 disclosures; "
    "the annual reports also contain Company statements, but Company cash flows are not substituted. Secure Trust "
    "Bank PLC is the current legal name. FY2021 is taken from the restated comparative column in the FY2022 report, "
    "which restates prior-year cash and cash equivalents from £303.0m to £306.7m. Figures are £million as reported."
)

CASH_SOURCES = "Sources - Secure Trust Bank PLC consolidated Group cash flows, £million:\n" + "\n".join(
    f"{y}: Secure Trust Bank PLC Annual Report & Accounts {y[-4:]}, consolidated statement of cash flows, "
    f"pp. { {'FY2025': '149', 'FY2024': '133', 'FY2023': '119', 'FY2022': '125', 'FY2021': '125'}[y] } - {AR_URLS[y]}"
    for y in YEARS
) + "\n\n" + ENTITY_NOTE

P3_SOURCES = "Sources - Secure Trust Bank PLC Group regulatory disclosures:\n" + "\n".join(
    f"{y}: Secure Trust Bank PLC Pillar 3 disclosure for the year ended 31 December {y[-4:]}, Key metrics table, "
    f"p. 5 (2021 p. 4) - {P3_URLS[y]}"
    for y in YEARS
) + "\n\n" + ENTITY_NOTE + " Regulatory figures are Group figures and are not substituted into Company cash flows."

bw = BankWorkbook("Secure Trust Bank Public Limited Company", YEARS, header_color="1F4E79")

rows = [
    ("SECTION", "Cash flows from operating activities", {}),
    ("DATA", "Profit for the year", {"FY2025": 17.6, "FY2024": 19.7, "FY2023": 24.3, "FY2022": 33.7, "FY2021": 45.6}),
    ("DATA", "Income tax expense", {"FY2025": 9.9, "FY2024": 9.5, "FY2023": 9.1, "FY2022": 10.3, "FY2021": 10.4}),
    ("DATA", "Depreciation of property, plant and equipment", {"FY2025": .8, "FY2024": 1.0, "FY2023": .9, "FY2022": 1.2, "FY2021": 1.3}),
    ("DATA", "Depreciation of right-of-use assets", {"FY2025": 1.1, "FY2024": 1.0, "FY2023": .7, "FY2022": .7, "FY2021": .7}),
    ("DATA", "Amortisation of intangible assets", {"FY2025": 1.2, "FY2024": 1.4, "FY2023": 1.2, "FY2022": 1.4, "FY2021": 1.5}),
    ("DATA", "Loss/(gain) on disposals and modifications", {"FY2024": 0.0, "FY2023": .2, "FY2022": -7.5, "FY2021": -.5}),
    ("DATA", "Impairment charge on loans and advances", {"FY2025": 58.0, "FY2024": 61.9, "FY2023": 43.2, "FY2022": 39.0, "FY2021": 4.5}),
    ("DATA", "Share-based compensation", {"FY2025": 2.0, "FY2024": 2.3, "FY2023": 1.1, "FY2022": 2.0, "FY2021": 1.0}),
    ("DATA", "Provisions for liabilities and charges", {"FY2025": 21.7, "FY2024": 9.8, "FY2023": 8.5}),
    ("DATA", "Other non-cash items included in profit before tax", {"FY2025": .2, "FY2024": -.6, "FY2023": -.8, "FY2022": 1.0, "FY2021": .4}),
    ("DATA", "Loans and advances to customers", {"FY2025": -159.0, "FY2024": -354.8, "FY2023": -439.0, "FY2022": -497.1, "FY2021": -238.4}),
    ("DATA", "Loans and advances to banks and central banks", {"FY2025": -5.1, "FY2024": 5.0, "FY2023": -1.3, "FY2022": .6, "FY2021": -1.9}),
    ("DATA", "Other assets", {"FY2025": 2.8, "FY2024": 1.4, "FY2023": .4, "FY2022": -1.5, "FY2021": 6.0}),
    ("DATA", "Deposits from customers", {"FY2025": 264.7, "FY2024": 373.1, "FY2023": 357.2, "FY2022": 411.4, "FY2021": 110.7}),
    ("DATA", "Provisions for liabilities and charges utilisation", {"FY2025": -7.6, "FY2024": -4.7, "FY2023": -4.7, "FY2022": -1.1, "FY2021": -.7}),
    ("DATA", "Other liabilities", {"FY2025": 60.7, "FY2024": -5.5, "FY2023": -37.8, "FY2022": 45.6, "FY2021": -24.4}),
    ("DATA", "Income tax paid", {"FY2025": -12.0, "FY2024": -8.8, "FY2023": -8.6, "FY2022": -7.0, "FY2021": -12.6}),
    ("TOTAL", "Net cash inflow/(outflow) from operating activities", {"FY2025": 257.0, "FY2024": 111.7, "FY2023": -45.4, "FY2022": 32.7, "FY2021": -96.4}),
    ("SECTION", "Cash flows from investing activities", {}),
    ("DATA", "Consideration on sale of loan books", {"FY2023": 0.0, "FY2022": 81.9, "FY2021": 60.4}),
    ("DATA", "Sale of investment property", {"FY2022": 3.3}),
    ("DATA", "Maturity and sales of debt securities", {"FY2022": 80.0, "FY2021": 90.0}),
    ("DATA", "Purchase of debt securities", {"FY2022": -80.0, "FY2021": -90.0}),
    ("DATA", "Purchase of property, plant and equipment and intangible assets", {"FY2025": -1.6, "FY2024": -1.0, "FY2023": -2.7, "FY2022": -2.7, "FY2021": -1.3}),
    ("DATA", "Purchase of investment property", {"FY2025": -1.1}),
    ("DATA", "Purchase of debt securities", {"FY2025": -1.0}),
    ("DATA", "Sale of property, plant and equipment", {"FY2025": 1.9}),
    ("TOTAL", "Net cash inflow/(outflow) from investing activities", {"FY2025": -1.8, "FY2024": -1.0, "FY2023": -2.7, "FY2022": 82.5, "FY2021": 59.1}),
    ("SECTION", "Cash flows from financing activities", {}),
    ("DATA", "Issue of subordinated debt", {"FY2023": 70.0}),
    ("DATA", "Redemption of subordinated debt", {"FY2023": -28.8}),
    ("DATA", "Drawdown/(repayment) of amounts due to banks", {"FY2025": -1.7, "FY2024": .8, "FY2023": -.9, "FY2022": 7.0, "FY2021": 114.4}),
    ("DATA", "Drawdown of sale and repurchase agreements", {"FY2025": 250.0, "FY2024": 125.0}),
    ("DATA", "Repayment of sale and repurchase agreements", {"FY2025": -175.0}),
    ("DATA", "Repayment of Term Funding Scheme", {"FY2025": -230.0, "FY2024": -160.0}),
    ("DATA", "Purchase of own shares", {"FY2025": -.2, "FY2024": -1.4, "FY2023": -1.2, "FY2022": -.3}),
    ("DATA", "Issue of shares", {"FY2025": .2, "FY2024": .2, "FY2023": 1.7}),
    ("DATA", "Dividends paid", {"FY2025": -6.4, "FY2024": -5.2, "FY2023": -8.4, "FY2022": -10.7, "FY2021": -11.9}),
    ("DATA", "Repayment of lease liabilities", {"FY2025": -1.3, "FY2024": -1.4, "FY2023": -.9, "FY2022": -1.0, "FY2021": -.9}),
    ("DATA", "Issue of ordinary shares", {"FY2021": 0.0}),
    ("TOTAL", "Net cash (outflow)/inflow from financing activities", {"FY2025": -164.4, "FY2024": -42.0, "FY2023": 31.5, "FY2022": -5.0, "FY2021": 101.6}),
    ("TOTAL", "Net increase/(decrease) in cash and cash equivalents", {"FY2025": 90.8, "FY2024": 68.7, "FY2023": -16.6, "FY2022": 110.2, "FY2021": 64.3}),
    ("DATA", "Cash and cash equivalents at 1 January", {"FY2025": 469.0, "FY2024": 400.3, "FY2023": 416.9, "FY2022": 306.7, "FY2021": 242.4}),
    ("TOTAL", "Cash and cash equivalents at 31 December", {"FY2025": 559.8, "FY2024": 469.0, "FY2023": 400.3, "FY2022": 416.9, "FY2021": 306.7}),
]

bw.add_cash_flow_sheet(
    "Secure Trust Bank PLC - Group Cash Flow Statement",
    "Consolidated Group basis, £million; FY2021 uses the restated comparative presented in the FY2022 report.",
    rows, CASH_SOURCES, first_col_width=68, source_height=250, unit_suffix=" (£m)",
)

def metric(name, unit, data, note=None):
    bw.add_metric_sheet(name, unit, data, P3_SOURCES, note=note, first_col_width=52, source_height=230)

metric("CET1 Capital", "£m", [("Common Equity Tier 1 capital", {"FY2025": 364.8, "FY2024": 351.4, "FY2023": 337.9, "FY2022": 327.4, "FY2021": 303.6})])
metric("CET1 Ratio", "% of RWEA", [("CET1 ratio", {"FY2025": "12.9%", "FY2024": "12.3%", "FY2023": "12.7%", "FY2022": "14.0%", "FY2021": "14.5%"})])
metric("Tier 1 Capital", "£m", [("Tier 1 capital", {"FY2025": 364.8, "FY2024": 351.4, "FY2023": 337.9, "FY2022": 327.4, "FY2021": 303.6})])
metric("Tier 1 Ratio", "% of RWEA", [("Tier 1 ratio", {"FY2025": "12.9%", "FY2024": "12.3%", "FY2023": "12.7%", "FY2022": "14.0%", "FY2021": "14.5%"})])
metric("Total Capital", "£m", [("Total capital", {"FY2025": 428.4, "FY2024": 415.7, "FY2023": 397.6, "FY2022": 377.3, "FY2021": 350.6})])
metric("Total Capital Ratio", "% of RWEA", [("Total capital ratio", {"FY2025": "15.2%", "FY2024": "14.6%", "FY2023": "15.0%", "FY2022": "16.2%", "FY2021": "16.8%"})])
metric("Total RWAs", "£m", [("Total RWEAs", {"FY2025": 2827.5, "FY2024": 2855.7, "FY2023": 2653.4, "FY2022": 2335.0, "FY2021": 2087.4})])
metric("Leverage Ratio", "%", [("Leverage ratio excluding claims on central banks", {"FY2025": "9.4%", "FY2024": "9.5%", "FY2023": "9.7%", "FY2022": "10.7%", "FY2021": "10.3%"})])
metric("LCR", "%", [("Liquidity Coverage Ratio", {"FY2025": "190.4%", "FY2024": "219.6%", "FY2023": "208.0%", "FY2022": "270.1%", "FY2021": "Not publicly disclosed"})], "The 2021 Pillar 3 key-metrics table does not disclose an LCR figure; no annual-report proxy is substituted.")
metric("NSFR", "%", [("Net Stable Funding Ratio", {"FY2025": "Not publicly disclosed", "FY2024": "Not publicly disclosed", "FY2023": "143.6%", "FY2022": "152.8%", "FY2021": "Not publicly disclosed"})])
metric("MREL Ratio", "%", [("MREL ratio", {y: "Not publicly disclosed" for y in YEARS})], "No quantitative MREL ratio was located in the reviewed annual reports or Pillar 3 disclosures.")

INTERIM_VALUES = {
    "H1 2025": {
        "CET1 capital": (367.1, "£m"),
        "Tier 1 capital": (367.1, "£m"),
        "Total capital": (432.7, "£m"),
        "Total RWEAs": (2916.8, "£m"),
        "CET1 ratio": ("12.6%", "% of RWEA"),
        "Tier 1 ratio": ("12.6%", "% of RWEA"),
        "Total capital ratio": ("14.8%", "% of RWEA"),
        "Leverage ratio excluding claims on central banks": ("9.3%", "%"),
        "Liquidity Coverage Ratio": ("193.5%", "%"),
    },
    "H1 2024": {
        "CET1 capital": (348.2, "£m"),
        "Tier 1 capital": (348.2, "£m"),
        "Total capital": (409.7, "£m"),
        "Total RWEAs": (2735.3, "£m"),
        "CET1 ratio": ("12.7%", "% of RWEA"),
        "Tier 1 ratio": ("12.7%", "% of RWEA"),
        "Total capital ratio": ("15.0%", "% of RWEA"),
        "Leverage ratio excluding claims on central banks": ("9.9%", "%"),
        "Liquidity Coverage Ratio": ("216.3%", "%"),
    },
    "H1 2023": {
        "CET1 capital": (326.8, "£m"),
        "Tier 1 capital": (326.8, "£m"),
        "Total capital": (383.5, "£m"),
        "Total RWEAs": (2518.5, "£m"),
        "CET1 ratio": ("13.0%", "% of RWEA"),
        "Tier 1 ratio": ("13.0%", "% of RWEA"),
        "Total capital ratio": ("15.2%", "% of RWEA"),
        "Leverage ratio excluding claims on central banks": ("10.1%", "%"),
        "Liquidity Coverage Ratio": ("217.0%", "%"),
        "NSFR ratio": ("150.9%", "%"),
    },
    "H1 2022": {
        "CET1 capital": (313.8, "£m"),
        "Tier 1 capital": (313.8, "£m"),
        "Total capital": (363.6, "£m"),
        "Total RWEAs": (2237.1, "£m"),
        "CET1 ratio": ("14.0%", "% of RWEA"),
        "Tier 1 ratio": ("14.0%", "% of RWEA"),
        "Total capital ratio": ("16.3%", "% of RWEA"),
        "Leverage ratio excluding claims on central banks": ("10.6%", "%"),
        "Liquidity Coverage Ratio": ("363.0%", "%"),
    },
}

INTERIM_PAGE_TABLE = {
    "H1 2025": "PDF p. 5, UK KM1 / IFRS 9-FL",
    "H1 2024": "PDF p. 5, UK KM1 / IFRS 9-FL",
    "H1 2023": "PDF p. 5, UK KM1",
    "H1 2022": "PDF p. 3, UK KM1",
}

interim_rows = []
interim_links = {}
for period, metrics in INTERIM_VALUES.items():
    for metric_name, (value, unit) in metrics.items():
        interim_rows.append(
            (period, "Interim Pillar 3", metric_name, value, unit, "Group", period, INTERIM_PAGE_TABLE[period])
        )
        interim_links[(len(interim_rows) - 1, 6)] = INTERIM_URLS[period]

bw.add_wide_interim_sheet(
    "Interim Pillar 3",
    headers=["Period", "Disclosure type", "Metric", "Value", "Unit", "Basis", "Source document", "Page / table"],
    rows=interim_rows,
    subtitle="Secure Trust Bank PLC Group basis; H1 observations from official interim UK KM1 disclosures.",
    note=(
        "Coverage: H1 2022 through H1 2025, covering the four official interim disclosures located. "
        "Each disclosure states that Secure Trust Bank PLC and its subsidiaries (the Group) are covered and "
        "that Pillar 3 disclosures are issued every six months. No separate H1 2021 Pillar 3 disclosure was "
        "located in the official archive; no 2021 interim values are inferred from annual or comparative data. "
        "NSFR was not disclosed in the H1 2022, H1 2024, or H1 2025 KM1 tables; those gaps are omitted rather "
        "than represented as zero. H1 2023 NSFR is reported. All source-document cells link to the official "
        "Secure Trust Bank document-library page for the relevant disclosure."
    ),
    widths=[14, 20, 46, 14, 16, 14, 42, 30],
    hyperlink_cells=interim_links,
)

bw.add_overview_sheet(
    cash_flow_totals=[
        ("Net cash from/(used in) operating activities", {"FY2025": 257.0, "FY2024": 111.7, "FY2023": -45.4, "FY2022": 32.7, "FY2021": -96.4}),
        ("Net cash from/(used in) investing activities", {"FY2025": -1.8, "FY2024": -1.0, "FY2023": -2.7, "FY2022": 82.5, "FY2021": 59.1}),
        ("Net cash from/(used in) financing activities", {"FY2025": -164.4, "FY2024": -42.0, "FY2023": 31.5, "FY2022": -5.0, "FY2021": 101.6}),
        ("Cash and cash equivalents at end of year", {"FY2025": 559.8, "FY2024": 469.0, "FY2023": 400.3, "FY2022": 416.9, "FY2021": 306.7}),
    ], cash_flow_unit="£m",
    ratios=[
        ("CET1 Ratio", {"FY2025": "12.9%", "FY2024": "12.3%", "FY2023": "12.7%", "FY2022": "14.0%", "FY2021": "14.5%"}),
        ("Total Capital Ratio", {"FY2025": "15.2%", "FY2024": "14.6%", "FY2023": "15.0%", "FY2022": "16.2%", "FY2021": "16.8%"}),
        ("Leverage Ratio", {"FY2025": "9.4%", "FY2024": "9.5%", "FY2023": "9.7%", "FY2022": "10.7%", "FY2021": "10.3%"}),
        ("LCR", {"FY2025": "190.4%", "FY2024": "219.6%", "FY2023": "208.0%", "FY2022": "270.1%"}),
        ("NSFR", {"FY2023": "143.6%", "FY2022": "152.8%"}),
    ],
    note="Group cash flows and Group Pillar 3 metrics are deliberately kept on their respective disclosed bases. FY2021 cash uses the FY2022 restated comparative; blank regulatory cells mean not disclosed, not zero.",
)

bw.save("/Users/armaan/code/katalysis/banks/SECURE TRUST BANK FINANCIALS.xlsx")
