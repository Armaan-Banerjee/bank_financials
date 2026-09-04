import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]  # most recent first, calendar year-end
YEAR_LABEL = {y: y for y in YEARS}

# Bank of England GBP/USD rates via poundsterlinglive.com's published archive,
# reusing the exact table already established for Zenith Bank UK (same 31
# December calendar year-end, so identical rate set applies).
FX_SPOT = {
    "FY2020": 1.3661,  # 31 Dec 2020 - only used for FY2021's opening cash balance
    "FY2021": 1.3521,  # 31 Dec 2021
    "FY2022": 1.2097,  # 30 Dec 2022 (31st was a Saturday)
    "FY2023": 1.2732,  # 29 Dec 2023 (31st was a Sunday)
    "FY2024": 1.2515,  # 31 Dec 2024
    "FY2025": 1.3448,  # 31 Dec 2025
}
FX_AVG = {
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
    "at the AVERAGE rate over that fiscal year. Rates used (£1 = $X): 31 Dec 2020 spot 1.3661 (FY2021 opening "
    "cash only); FY2021 spot 1.3521 / average 1.3752; FY2022 spot 1.2097 / average 1.2362; FY2023 spot 1.2732 / "
    "average 1.2439; FY2024 spot 1.2515 / average 1.2782; FY2025 spot 1.3448 / average 1.3193 - same table "
    "already established for Zenith Bank UK (identical 31 December year-end). Converting stocks and flows at "
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
    + ENTITY_NOTE + "\n\n" + FX_METHOD_NOTE
)


def p3_sources():
    return (
        "Sources - Credit Suisse International capital/RWA basis: the FY2025 Annual Report's own 'Key "
        "Performance Indicators' table (p.6), which discloses Risk Weighted Assets, Tier 1 capital, and Tier 1 "
        "capital ratio for all 5 years (2021-2025) as at each year-end - "
        f"{AR_URLS['FY2025']}. This report explicitly states 'Pillar 3 disclosures required under the Capital "
        "Requirements Regulation (CRR) can be found separately at http://www.ubs.com' - a standalone CSI Pillar "
        "3 document was not locatable this session (the UBS regulatory-disclosures URL pattern returned 404, "
        "and the session's WebSearch quota was already exhausted by parallel forks) - revisit if this bank is "
        "ever rebuilt. Converted from USD to GBP using the same FX methodology as the Cash Flow Statement sheet "
        "(SPOT rate at each year-end); % ratios shown exactly as disclosed, not converted.\n" + FX_METHOD_NOTE
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
    + ENTITY_NOTE + "\n\n" + FX_METHOD_NOTE + "\n\n"
    "PRESENTATION NOTE: s.408 Companies Act 2006 exemption means no separate Bank-only income statement is "
    "published (Group figures used for P&L throughout, consistent with the Balance Sheet and Equity statement). "
    "FY2024/FY2025's income statement separates 'Discontinued Operations' from continuing operations; FY2021-23 "
    "have no such split (whole-entity basis) - both presentations reproduced as reported, not forced onto one "
    "basis. A small (~£0.7m-£1.5m) rounding gap exists between the P&L's own 'Total comprehensive income/(loss)' "
    "and the Equity statement's own total for the same year in 3 of 5 years (FY2024/FY2022/FY2021) - this "
    "originates as a <=$1m rounding artifact already present in CSI's own USD-million source tables, amplified "
    "slightly by FX conversion; both sheets show each source table's own figure rather than forcing one to match "
    "the other."
)

# ---------------------------------------------------------------
# Balance Sheet (Consolidated Statement of Financial Position)
# ---------------------------------------------------------------
BS_ROWS_USD = [
    ("SECTION", "Assets", None),
    ("DATA", "Cash and due from banks", {"FY2025":362,"FY2024":1858,"FY2023":3627,"FY2022":4149,"FY2021":1484}),
    ("DATA", "Interest-bearing deposits with banks", {"FY2025":525,"FY2024":3961,"FY2023":8319,"FY2022":12085,"FY2021":13284}),
    ("DATA", "Securities purchased under resale agreements", {"FY2025":4439,"FY2024":533,"FY2023":1304,"FY2022":10527,"FY2021":8902}),
    ("DATA", "Trading financial assets at fair value through P&L", {"FY2025":8,"FY2024":22624,"FY2023":63309,"FY2022":107973,"FY2021":143718}),
    ("DATA", "Non-trading financial assets at fair value through P&L", {"FY2024":14200,"FY2023":24588,"FY2022":22831,"FY2021":38226}),
    ("DATA", "Loans and advances", {"FY2025":7,"FY2024":2548,"FY2023":3411,"FY2022":2973,"FY2021":2968}),
    ("DATA", "Investment property", {"FY2021":14}),
    ("DATA", "Current tax assets", {"FY2025":107,"FY2024":194,"FY2023":121,"FY2022":110,"FY2021":67}),
    ("DATA", "Deferred tax assets", {"FY2021":284}),
    ("DATA", "Other assets", {"FY2025":202,"FY2024":5416,"FY2023":17629,"FY2022":21744,"FY2021":34666}),
    ("DATA", "Property and equipment", {"FY2024":9,"FY2023":27,"FY2022":372,"FY2021":407}),
    ("DATA", "Intangible assets", {"FY2024":31,"FY2023":83,"FY2022":482,"FY2021":495}),
    ("TOTAL", "Total assets", {"FY2025":5650,"FY2024":51374,"FY2023":122418,"FY2022":183246,"FY2021":244515}),
    ("SECTION", "Liabilities", None),
    ("DATA", "Due to banks", {"FY2025":5,"FY2024":18,"FY2023":31,"FY2022":266,"FY2021":218}),
    ("DATA", "Securities sold under repurchase agreements", {"FY2025":443,"FY2024":26,"FY2023":358,"FY2022":2924,"FY2021":3371}),
    ("DATA", "Trading financial liabilities at fair value through P&L", {"FY2025":8,"FY2024":22129,"FY2023":60519,"FY2022":93397,"FY2021":122054}),
    ("DATA", "Financial liabilities designated at fair value through P&L", {"FY2025":1,"FY2024":2565,"FY2023":16050,"FY2022":27169,"FY2021":35012}),
    ("DATA", "Borrowings", {"FY2025":2002,"FY2024":7387,"FY2023":12622,"FY2022":6025,"FY2021":1470}),
    ("DATA", "Current tax liabilities", {"FY2024":3,"FY2023":3,"FY2022":3,"FY2021":13}),
    ("DATA", "Deferred tax liabilities", {"FY2024":37,"FY2023":59}),
    ("DATA", "Other liabilities", {"FY2025":118,"FY2024":6007,"FY2023":9025,"FY2022":16675,"FY2021":23584}),
    ("DATA", "Provisions", {"FY2025":58,"FY2024":116,"FY2023":168,"FY2022":45,"FY2021":313}),
    ("DATA", "Debt in issuance", {"FY2024":5456,"FY2023":8108,"FY2022":18309,"FY2021":40224}),
    ("DATA", "Lease liabilities", {"FY2024":291,"FY2023":512,"FY2022":529,"FY2021":627}),
    ("TOTAL", "Total liabilities", {"FY2025":2635,"FY2024":44035,"FY2023":107455,"FY2022":165342,"FY2021":226886}),
    ("SECTION", "Shareholders' equity", None),
    ("DATA", "Share capital", {"FY2025":1,"FY2024":1368,"FY2023":7267,"FY2022":11366,"FY2021":11366}),
    ("DATA", "Capital contribution", {"FY2025":904,"FY2024":917,"FY2023":887,"FY2022":887,"FY2021":887}),
    ("DATA", "Other equity instruments", {"FY2023":1200,"FY2022":1200}),
    ("DATA", "Retained earnings", {"FY2025":2110,"FY2024":5611,"FY2023":6058,"FY2022":4852,"FY2021":5536}),
    ("DATA", "Accumulated other comprehensive income", {"FY2024":-557,"FY2023":-449,"FY2022":-401,"FY2021":-160}),
    ("TOTAL", "Total shareholders' equity", {"FY2025":3015,"FY2024":7339,"FY2023":14963,"FY2022":17904,"FY2021":17629}),
    ("TOTAL", "Total liabilities and shareholders' equity", {"FY2025":5650,"FY2024":51374,"FY2023":122418,"FY2022":183246,"FY2021":244515}),
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
    ("DATA", "Interest income", {"FY2025":507,"FY2024":1581,"FY2023":2976,"FY2022":1628,"FY2021":428}),
    ("DATA", "Interest expense", {"FY2025":-295,"FY2024":-1004,"FY2023":-2532,"FY2022":-1670,"FY2021":-491}),
    ("TOTAL", "Net interest income/(expense)", {"FY2025":212,"FY2024":577,"FY2023":444,"FY2022":-42,"FY2021":-63}),
    ("DATA", "Commission and fee income", {"FY2025":1,"FY2024":1,"FY2023":139,"FY2022":425,"FY2021":428}),
    ("DATA", "Allowance for credit losses", {"FY2023":-68,"FY2022":158,"FY2021":-4530}),
    ("DATA", "Net gains from financial assets/liabilities at FVTPL", {"FY2025":47,"FY2024":109,"FY2023":796,"FY2022":1603,"FY2021":1761}),
    ("DATA", "Other revenues", {"FY2025":1,"FY2024":46,"FY2023":102,"FY2022":184,"FY2021":253}),
    ("TOTAL", "Net revenues", {"FY2025":261,"FY2024":733,"FY2023":1413,"FY2022":2328,"FY2021":-2151}),
    ("SECTION", "Operating expenses", None),
    ("DATA", "Compensation and benefits", {"FY2023":-642,"FY2022":-551,"FY2021":-729}),
    ("DATA", "General, administrative and trading expenses", {"FY2025":-18,"FY2024":-20,"FY2023":-2460,"FY2022":-2061,"FY2021":-2489}),
    ("DATA", "Restructuring expenses", {"FY2023":-47,"FY2022":-47,"FY2021":-17}),
    ("TOTAL", "Total operating expenses", {"FY2025":-18,"FY2024":-20,"FY2023":-3149,"FY2022":-2659,"FY2021":-3235}),
    ("TOTAL", "Profit/(loss) before tax from continuing operations", {"FY2025":243,"FY2024":713,"FY2023":-1736,"FY2022":-331,"FY2021":-5386}),
    ("DATA", "Income tax (expense)/benefit", {"FY2025":-68,"FY2024":-92,"FY2023":-57,"FY2022":-354,"FY2021":43}),
    ("TOTAL", "Profit/(loss) after tax from continuing operations", {"FY2025":175,"FY2024":621,"FY2023":-1793,"FY2022":-685,"FY2021":-5343}),
    ("SECTION", "Discontinued operations (FY2024/FY2025 presentation only - see note)", None),
    ("DATA", "Loss before tax from discontinued operations", {"FY2025":-397,"FY2024":-773}),
    ("DATA", "Income tax (expense)/benefit from discontinued operations", {"FY2025":-2,"FY2024":65}),
    ("TOTAL", "Loss after tax from discontinued operations", {"FY2025":-399,"FY2024":-708}),
    ("TOTAL", "Profit/(loss) for the year", {"FY2025":-224,"FY2024":-87,"FY2023":-1793,"FY2022":-685,"FY2021":-5343}),
    ("SECTION", "Other comprehensive income/(loss)", None),
    ("DATA", "Other comprehensive income/(loss) for the period, net of tax", {"FY2025":-5,"FY2024":-108,"FY2023":-48,"FY2022":-241,"FY2021":-33}),
    ("TOTAL", "Total comprehensive income/(loss) for the year", {"FY2025":-229,"FY2024":-195,"FY2023":-1841,"FY2022":-926,"FY2021":-5376}),
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
EQUITY_HEADERS = ["Share capital", "Capital contribution", "Other equity instruments", "Retained earnings", "AOCI", "Total"]
EQUITY_ROWS_USD = [
    ("TOTAL", "At 1 January 2021", [11366,887,0,10881,-127,23007], "spot", "FY2020"),
    ("DATA", "Net loss for the year (FY2021)", [None,None,None,-5343,None,-5343], "avg", "FY2021"),
    ("DATA", "Realised gain/(loss) on designated FL reclassed to retained earnings (FY2021)", [None,None,None,-2,2,0], "avg", "FY2021"),
    ("DATA", "Unrealised gain on designated FL relating to credit risk (FY2021)", [None,None,None,None,10,10], "avg", "FY2021"),
    ("DATA", "Cash flow hedges - effective portion of changes in fair value (FY2021)", [None,None,None,None,-45,-45], "avg", "FY2021"),
    ("DATA", "Related tax on cash flow hedges (FY2021)", [None,None,None,None,9,9], "avg", "FY2021"),
    ("DATA", "Remeasurement of defined benefit pension assets (FY2021)", [None,None,None,None,-29,-29], "avg", "FY2021"),
    ("DATA", "Related tax on remeasurement of defined benefit pension assets (FY2021)", [None,None,None,None,20,20], "avg", "FY2021"),
    ("TOTAL", "Total comprehensive loss for the year (FY2021)", [None,None,None,-5345,-33,-5378], "avg", "FY2021"),
    ("DATA", "FX translation effect on equity, net (FY2021)", [None,None,None,None,None,None], "plug", "FY2021"),
    ("TOTAL", "At 31 December 2021", [11366,887,0,5536,-160,17629], "spot", "FY2021"),

    ("DATA", "Net loss for the year (FY2022)", [None,None,None,-685,None,-685], "avg", "FY2022"),
    ("DATA", "Realised gain/(loss) on designated FL reclassed to retained earnings (FY2022)", [None,None,None,1,-1,0], "avg", "FY2022"),
    ("DATA", "Unrealised gain on designated FL relating to credit risk (FY2022)", [None,None,None,None,31,31], "avg", "FY2022"),
    ("DATA", "Related tax on unrealised gain (FY2022)", [None,None,None,None,-3,-3], "avg", "FY2022"),
    ("DATA", "Cash flow hedges - effective portion of changes in fair value (FY2022)", [None,None,None,None,3,3], "avg", "FY2022"),
    ("DATA", "Related tax on cash flow hedges (FY2022)", [None,None,None,None,-3,-3], "avg", "FY2022"),
    ("DATA", "Remeasurement of defined benefit pension assets (FY2022)", [None,None,None,None,-358,-358], "avg", "FY2022"),
    ("DATA", "Related tax on remeasurement of defined benefit pension assets (FY2022)", [None,None,None,None,90,90], "avg", "FY2022"),
    ("TOTAL", "Total comprehensive loss for the year (FY2022)", [None,None,None,-684,-241,-925], "avg", "FY2022"),
    ("DATA", "Additional Tier 1 Capital issuance (FY2022)", [None,None,1200,None,None,1200], "avg", "FY2022"),
    ("DATA", "FX translation effect on equity, net (FY2022)", [None,None,None,None,None,None], "plug", "FY2022"),
    ("TOTAL", "At 31 December 2022", [11366,887,1200,4852,-401,17904], "spot", "FY2022"),

    ("DATA", "Net loss for the year (FY2023)", [None,None,None,-1793,None,-1793], "avg", "FY2023"),
    ("DATA", "Unrealised loss on designated FL relating to credit risk (FY2023)", [None,None,None,None,-23,-23], "avg", "FY2023"),
    ("DATA", "Related tax on unrealised loss (FY2023)", [None,None,None,None,3,3], "avg", "FY2023"),
    ("DATA", "Cash flow hedges - effective portion of changes in fair value (FY2023)", [None,None,None,None,12,12], "avg", "FY2023"),
    ("DATA", "Remeasurement of defined benefit pension assets (FY2023)", [None,None,None,None,-56,-56], "avg", "FY2023"),
    ("DATA", "Related tax on remeasurement of defined benefit pension assets (FY2023)", [None,None,None,None,16,16], "avg", "FY2023"),
    ("TOTAL", "Total comprehensive loss for the year (FY2023)", [None,None,None,-1793,-48,-1841], "avg", "FY2023"),
    ("DATA", "Capital reduction (FY2023)", [-4099,None,None,4099,None,0], "avg", "FY2023"),
    ("DATA", "Dividend payment (FY2023)", [None,None,None,-1100,None,-1100], "avg", "FY2023"),
    ("DATA", "FX translation effect on equity, net (FY2023)", [None,None,None,None,None,None], "plug", "FY2023"),
    ("TOTAL", "At 31 December 2023", [7267,887,1200,6058,-449,14963], "spot", "FY2023"),

    ("DATA", "Net loss for the year (FY2024)", [None,None,None,-87,None,-87], "avg", "FY2024"),
    ("DATA", "Realised gain/(loss) on designated FL reclassed to retained earnings (FY2024)", [None,None,None,-1,1,0], "avg", "FY2024"),
    ("DATA", "Unrealised gain on designated FL relating to credit risk (FY2024)", [None,None,None,None,3,3], "avg", "FY2024"),
    ("DATA", "Cash flow hedges - effective portion of changes in fair value (FY2024)", [None,None,None,None,-3,-3], "avg", "FY2024"),
    ("DATA", "Remeasurement of defined benefit pension assets (FY2024)", [None,None,None,None,-152,-152], "avg", "FY2024"),
    ("DATA", "Related tax on remeasurement of defined benefit pension assets (FY2024)", [None,None,None,None,43,43], "avg", "FY2024"),
    ("TOTAL", "Total comprehensive loss for the year (FY2024)", [None,None,None,-88,-108,-196], "avg", "FY2024"),
    ("DATA", "Capital reduction (FY2024)", [-5899,None,None,None,None,-5899], "avg", "FY2024"),
    ("DATA", "Additional Tier 1 capital repatriation (FY2024)", [None,None,-1200,None,None,-1200], "avg", "FY2024"),
    ("DATA", "Interest payment on Additional Tier 1 capital (FY2024)", [None,None,None,-466,None,-466], "avg", "FY2024"),
    ("DATA", "Related tax on interest payment on Additional Tier 1 capital (FY2024)", [None,None,None,107,None,107], "avg", "FY2024"),
    ("DATA", "Gain on transfer of business to UBS Group entities (FY2024)", [None,30,None,None,None,30], "avg", "FY2024"),
    ("DATA", "FX translation effect on equity, net (FY2024)", [None,None,None,None,None,None], "plug", "FY2024"),
    ("TOTAL", "At 31 December 2024", [1368,917,0,5611,-557,7339], "spot", "FY2024"),

    ("DATA", "Net loss for the year (FY2025)", [None,None,None,-224,None,-224], "avg", "FY2025"),
    ("DATA", "Remeasurement of defined benefit pension assets (FY2025)", [None,None,None,None,-7,-7], "avg", "FY2025"),
    ("DATA", "Related tax on remeasurement of defined benefit pension assets (FY2025)", [None,None,None,None,2,2], "avg", "FY2025"),
    ("TOTAL", "Total comprehensive loss for the year (FY2025)", [None,None,None,-224,-5,-229], "avg", "FY2025"),
    ("DATA", "Capital reduction (FY2025)", [-1367,None,None,None,None,-1367], "avg", "FY2025"),
    ("DATA", "Loss on transfer of leases to UBS Group entities (FY2025)", [None,-13,None,None,None,-13], "avg", "FY2025"),
    ("DATA", "Dividend payment (FY2025)", [None,None,None,-2400,None,-2400], "avg", "FY2025"),
    ("DATA", "Pension asset transfer to UBS Group entities, as dividend (FY2025)", [None,None,None,-437,None,-437], "avg", "FY2025"),
    ("DATA", "Tax on pension asset transfer to UBS Group entities (FY2025)", [None,None,None,122,None,122], "avg", "FY2025"),
    ("DATA", "AOCI on pension transferred to reserves, net of tax (FY2025)", [None,None,None,-562,562,0], "avg", "FY2025"),
    ("DATA", "FX translation effect on equity, net (FY2025)", [None,None,None,None,None,None], "plug", "FY2025"),
    ("TOTAL", "At 31 December 2025", [1,904,0,2110,0,3015], "spot", "FY2025"),
]
# FX translation plug values (£m) - computed as: closing (spot) - opening (spot, prior year-end) -
# sum of that year's movements (average rate). Not hardcoded blind; independently derived and
# cross-checked to make each year's roll-forward tie exactly - see map.md's Notes for the method.
FX_PLUG_GBP = {"FY2021": 107.6, "FY2022": 1539.7, "FY2023": -683.7, "FY2024": 76.5, "FY2025": -344.7}

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
NET_OPERATING_USD = {"FY2025": 7865, "FY2024": 8673, "FY2023": 11387, "FY2022": 21276, "FY2021": -14340}
NET_INVESTING_USD = {"FY2025": 4, "FY2024": 1, "FY2023": -26, "FY2022": -165, "FY2021": -180}
NET_FINANCING_USD = {"FY2025": -9493, "FY2024": -10409, "FY2023": -11749, "FY2022": -18419, "FY2021": 10043}
OPENING_CASH_USD = {"FY2025": 1840, "FY2024": 3596, "FY2023": 3883, "FY2022": 5792, "FY2021": 5792}
OPENING_CASH_RATE_YEAR = {"FY2025": "FY2024", "FY2024": "FY2023", "FY2023": "FY2022", "FY2022": "FY2021", "FY2021": "FY2020"}
CLOSING_CASH_USD = {"FY2025": 357, "FY2024": 1840, "FY2023": 3596, "FY2022": 3883, "FY2021": 5792}

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
    "dominated by trading/derivative exposures, not a traditional retail/commercial loan book.\n\n" + ENTITY_NOTE
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


TIER1_USD = {"FY2025": 3014, "FY2024": 6883, "FY2023": 13889, "FY2022": 15809, "FY2021": 15022}
TIER1_RATIO = {"FY2025": "146.9%", "FY2024": "62.9%", "FY2023": "40.0%", "FY2022": "26.0%", "FY2021": "24.0%"}
RWA_USD = {"FY2025": 2052, "FY2024": 10951, "FY2023": 34698, "FY2022": 60646, "FY2021": 62643}

tier1_gbp = {y: stock(v, y) for y, v in TIER1_USD.items()}
rwa_gbp = {y: stock(v, y) for y, v in RWA_USD.items()}

AT1_NOTE = (
    "CET1 is NOT separately disclosed anywhere in the source - only a combined 'Tier 1 capital' figure and "
    "ratio are given. The Statement of Changes in Equity shows Additional Tier 1 (AT1) instruments of $1,200m "
    "outstanding at 31 Dec 2022 and 31 Dec 2023 only (issued during FY2022, repatriated during FY2024) - so "
    "CET1 = Tier 1 for FY2021/FY2024/FY2025 (confirmed zero AT1 those years), but CET1 < Tier 1 for FY2022/"
    "FY2023 by an unknown regulatory-capital amount (the $1,200m accounting carrying value of the AT1 "
    "instrument itself isn't necessarily identical to its CRR-recognised capital amount) - left blank rather "
    "than guessed for those two years."
)

metric(
    "CET1 Capital", "£m (conv. from USD) - see note",
    [("Common Equity Tier 1 (CET1) capital", {y: tier1_gbp[y] for y in ["FY2025", "FY2024", "FY2021"]})],
    note=AT1_NOTE,
)
metric(
    "CET1 Ratio", "% - see note",
    [("CET1 Ratio", {y: TIER1_RATIO[y] for y in ["FY2025", "FY2024", "FY2021"]})],
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
bw.add_not_disclosed_metric_sheets(
    ["Total Capital", "Total Capital Ratio"],
    p3_sources(),
    per_note={
        "Total Capital": "Not publicly disclosed - only Tier 1 capital is given in the source; no Tier 2 "
                          "instrument or Total Capital figure/ratio appears anywhere in the 5 Annual Reports "
                          "reviewed, and the standalone Pillar 3 document (referenced at ubs.com) was not "
                          "locatable this session.",
        "Total Capital Ratio": "Not publicly disclosed - see Total Capital sheet note.",
    },
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

RWA_BD_USD = {
    "Credit risk (excluding CCR)": {"FY2025": 266, "FY2024": 810, "FY2023": 4338, "FY2022": 7086, "FY2021": 7424},
    "Counterparty credit risk (CCR)": {"FY2025": 21, "FY2024": 3558, "FY2023": 14628, "FY2022": 24912, "FY2021": 23717},
    "Settlement risk": {"FY2025": 1, "FY2024": 0, "FY2023": 19, "FY2022": 55, "FY2021": 100},
    "Securitisation exposures in the non-trading book": {"FY2025": 0, "FY2024": 0, "FY2023": 26, "FY2022": 0, "FY2021": 67},
    "Position, foreign exchange and commodities risks (Market risk)": {"FY2025": 82, "FY2024": 3706, "FY2023": 9711, "FY2022": 17116, "FY2021": 22546},
    "Large exposures": {"FY2025": 0, "FY2024": 0, "FY2023": 2210, "FY2022": 6970, "FY2021": 4240},
    "Operational risk": {"FY2025": 1682, "FY2024": 2877, "FY2023": 3767, "FY2022": 4507, "FY2021": 4550},
    "Amounts below thresholds for deduction (subject to 250% risk weight) - memo, already included above, not additive to Total": {
        "FY2025": 0, "FY2024": 96, "FY2023": 96, "FY2022": 407, "FY2021": 864},
}
rwa_bd_gbp = {label: {y: stock(v, y) for y, v in yrs.items()} for label, yrs in RWA_BD_USD.items()}

rwa_breakdown_rows = [
    ("SECTION", "RWA by risk category (OV1 template)", {}),
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
    ("TOTAL", "Total RWAs", rwa_gbp),
]
bw.add_rwa_breakdown_sheet(
    title="Credit Suisse International — RWA Breakdown",
    subtitle="Pillar 3 UK OV1 template, £m (conv. from USD). Ties exactly to the Total RWAs sheet for all 5 years.",
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
        "Converted from USD to GBP using the same FX methodology as the Cash Flow Statement sheet (SPOT rate "
        "at each year-end).\n" + FX_METHOD_NOTE
    ),
    first_col_width=90,
    source_height=260,
)

bw.add_not_disclosed_metric_sheets(
    ["Leverage Ratio", "LCR", "NSFR", "MREL Ratio"],
    p3_sources(),
    per_note={m: "Not publicly disclosed in the Annual Report itself. A standalone CSI Pillar 3 document is "
                 "explicitly referenced (at ubs.com) but was not locatable this session (404 on the guessed URL "
                 "pattern; WebSearch quota already exhausted) - revisit if this bank is ever rebuilt."
              for m in ["Leverage Ratio", "LCR", "NSFR", "MREL Ratio"]},
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bs_by_label = {label: values for _, label, values in balance_sheet_rows}
is_by_label = {label: values for _, label, values in income_statement_rows}

OPENING_EQUITY_GBP = {"FY2021":16841.4,"FY2022":13038.2,"FY2023":14800.4,"FY2024":11752.3,"FY2025":5864.2}
CLOSING_EQUITY_GBP = {"FY2021":13038.2,"FY2022":14800.4,"FY2023":11752.3,"FY2024":5864.2,"FY2025":2242.0}
TOTAL_COMPREHENSIVE_GBP = {"FY2021":-3910.7,"FY2022":-748.3,"FY2023":-1480.0,"FY2024":-153.3,"FY2025":-173.6}
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
