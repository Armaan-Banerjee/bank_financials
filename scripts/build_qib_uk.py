import os
import sys
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]
YEAR_LABEL = {y: y for y in YEARS}
CH = "https://find-and-update.company-information.service.gov.uk/company/04656003/filing-history"
AR = {"FY2025": CH+"/MzUyNzI4MTM5OGFkaXF6a2N4/document?format=pdf&download=0", "FY2024": CH+"/MzQ2NzkwMzQ0MmFkaXF6a2N4/document?format=pdf&download=0", "FY2023": CH+"/MzQyNDU4NzQ0OGFkaXF6a2N4/document?format=pdf&download=0", "FY2022": CH+"/MzM4MDQ4MTUzN2FkaXF6a2N4/document?format=pdf&download=0", "FY2021": CH+"/MzMzOTk2ODIxNmFkaXF6a2N4/document?format=pdf&download=0"}
P3 = {"FY2025": "https://www.qib-uk.com/-/media/project/uk/files/finance-reports/pillar-3-disclosure-document--2025-approved.pdf", "FY2024": "https://www.qib-uk.com/-/media/project/uk/files/finance-reports/pillar-3-disclosure-document-31-december-2024.pdf", "FY2023": "https://www.qib-uk.com/-/media/project/uk/files/finance-reports/pillar-3-disclosure-document-31-december-2023.pdf", "FY2022": "https://www.qib-uk.com/-/media/project/uk/files/finance-reports/pillar-3-disclosure-document-2023.pdf", "FY2021": "https://www.qib-uk.com/-/media/project/uk/files/finance-reports/pillar-3-disclosure-document-2023.pdf"}

ENTITY = ("ENTITY NOTE: QIB (UK) plc (Companies House 04656003, FRN 466577) is the UK bank subsidiary of Qatar Islamic Bank S.A.Q. The Bank states that it had no active subsidiaries or joint ventures at 31 December 2023 and does not prepare group accounts; these are entity-only GBP accounts. Companies House shows the entity Active with accounts filed through FY2025.")
CASH_SOURCES = ("Sources - QIB (UK) plc's own entity Statement of Cash Flows, converted from £ to £m (divide by 1,000,000 and round to 2 decimals):\n" + "\n".join(f"{y}: Annual Report, p.{p} - {AR[y]}" for y,p in {"FY2025":24,"FY2024":25,"FY2023":24,"FY2022":25,"FY2021":22}.items()) + "\nFY2025/FY2024 reports label the FY2024 comparative restated and FY2023 labels the FY2022 comparative restated. Each year's own report column is used here, preserving the project convention and avoiding blended reclassifications. FY2024 and FY2023 each contain a source presentation difference between the printed operating line items and the printed operating subtotal; explicit reconciliation rows preserve both.\n\n" + ENTITY)
def p3_sources():
    return ("Sources - QIB (UK) plc's own Pillar 3 disclosures, UK KM1 Key Metrics template (amounts in £'000; ratios as reported):\n" + "\n".join(f"{y}: {('FY2022 comparative column of FY2022 disclosure' if y=='FY2021' else 'own-year disclosure')}, pp.6-7 - {P3[y]}" for y in YEARS) + "\nMREL is not disclosed in the reviewed QIB UK Pillar 3 documents.\n\n" + ENTITY)
def m(d): return {y: round(v/1_000_000, 2) for y,v in d.items()}

bw = BankWorkbook(bank_name="QIB (UK) plc", years=YEARS, year_label=YEAR_LABEL, header_color="0B4F6C")

STATEMENTS_SOURCES = (
    "Sources - QIB (UK) plc's own entity Statement of Financial Position / Statement of Comprehensive "
    "Income / Statement of Changes in Equity, converted from £ to £m (divide by 1,000,000, round to 3 "
    "decimals):\n"
    "FY2025/FY2024 (own): Annual Report and Accounts 2025, pp.21-23 - " + AR["FY2025"] + "\n"
    "FY2023 (own): Annual Report and Accounts 2023, pp.20-22 - " + AR["FY2023"] + "\n"
    "FY2022 (own): Annual Report and Accounts 2022, pp.21-23 - " + AR["FY2022"] + "\n"
    "FY2021 (own): Annual Report and Accounts 2021, pp.18-20 - " + AR["FY2021"] + "\n\n"
    + ENTITY + "\n\n"
    "RESTATEMENT NOTE: each year's own originally-published Balance Sheet figures are used throughout "
    "(project convention), not later restated comparatives. FY2024's Balance Sheet was later restated in "
    "AR2025 (Cash and balances with banks 82,316,418 vs FY2024's own 27,223,411; Financial assets at "
    "amortised cost 137,810,920 vs FY2024's own 192,903,927) - Note 2g attributes this to a reclassification "
    "of the Alternative Liquidity Facility from 'Financial assets at amortised cost' into 'Cash and balances "
    "with banks'; Total assets/equity are unaffected. FY2022's Balance Sheet was similarly restated in "
    "AR2023 (Financing arrangements 783,073,152 vs FY2022's own 777,848,982; Financial assets at amortised "
    "cost 150,714,519 vs FY2022's own 149,784,049; Other assets 950,771 vs FY2022's own 7,105,411) - a "
    "reclassification across three asset lines, net-zero on Total assets. Both are genuine, Bank-disclosed "
    "reclassifications, not transcription errors.\n\n"
    "PRESENTATION NOTE: the Balance Sheet's 'Fair value adjustment for portfolio hedged risk' line and "
    "'Deferred tax liability' line only appear from FY2024 onward (FY2021-FY2023 instead carry a 'Deferred "
    "tax asset' line - a genuine sign flip in the Bank's net deferred tax position, not an omission). The "
    "P&L's 'Net gain/(loss) on financial assets at fair value' / 'at amortised cost' lines and the 'FV loss "
    "on investment property' line each appear only in some years, reflecting genuine year-on-year changes "
    "in what the Bank's own income statement discloses as a separate line - blank cells indicate a line "
    "not disclosed that year, not a zero."
)

bs_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and balances with banks", m({"FY2025": 132462261, "FY2024": 27223411, "FY2023": 49246616, "FY2022": 59103924, "FY2021": 56338957})),
    ("DATA", "Financing arrangements", m({"FY2025": 954683460, "FY2024": 884059958, "FY2023": 826875369, "FY2022": 777848982, "FY2021": 726026105})),
    ("DATA", "Financial assets at amortised cost", m({"FY2025": 141472045, "FY2024": 192903927, "FY2023": 172313444, "FY2022": 149784049, "FY2021": 81553810})),
    ("DATA", "Derivative financial instruments", m({"FY2025": 1122065, "FY2024": 1597563, "FY2023": 617042, "FY2022": 989055, "FY2021": 1429382})),
    ("DATA", "Fair value adjustment for portfolio hedged risk", m({"FY2025": -1031227, "FY2024": -898730})),
    ("DATA", "Property and equipment", m({"FY2025": 15289209, "FY2024": 12810372, "FY2023": 12674423, "FY2022": 14126933, "FY2021": 12995170})),
    ("DATA", "Intangible assets", m({"FY2025": 384806, "FY2023": 23300, "FY2022": 72221, "FY2021": 231069})),
    ("DATA", "Investment property", m({"FY2025": 3100000, "FY2024": 6225000, "FY2023": 6225000, "FY2022": 7665000, "FY2021": 10240000})),
    ("DATA", "Other assets", m({"FY2025": 2766848, "FY2024": 1527850, "FY2023": 1003932, "FY2022": 7105411, "FY2021": 4124393})),
    ("DATA", "Deferred tax asset", m({"FY2023": 1500052, "FY2022": 2212189, "FY2021": 1792307})),
    ("TOTAL", "Total assets", m({"FY2025": 1250249467, "FY2024": 1125449351, "FY2023": 1070479178, "FY2022": 1018907764, "FY2021": 894731193})),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Due to banks", m({"FY2025": 108416644, "FY2024": 83641722, "FY2023": 103985098, "FY2022": 105266168, "FY2021": 120257356})),
    ("DATA", "Due to customers", m({"FY2025": 969400662, "FY2024": 886390965, "FY2023": 827374599, "FY2022": 780208856, "FY2021": 657768467})),
    ("DATA", "Other liabilities", m({"FY2025": 31877296, "FY2024": 27424980, "FY2023": 23695160, "FY2022": 29976993, "FY2021": 22889306})),
    ("DATA", "Derivative financial instruments", m({"FY2025": 1646782, "FY2024": 593378, "FY2023": 816802, "FY2022": 1345231, "FY2021": 1289353})),
    ("DATA", "Deferred tax liability", m({"FY2025": 163967, "FY2024": 163136})),
    ("DATA", "Subordinated Wakala", m({"FY2025": 14097755, "FY2024": 14133099, "FY2023": 14166072, "FY2022": 13700000, "FY2021": 13700000})),
    ("TOTAL", "Total liabilities", m({"FY2025": 1125603106, "FY2024": 1012347280, "FY2023": 970037731, "FY2022": 930497248, "FY2021": 815904482})),
    ("SECTION", "Equity", {}),
    ("DATA", "Share capital", m({"FY2025": 60864221, "FY2024": 60864221, "FY2023": 60864221, "FY2022": 60864221, "FY2021": 60864221})),
    ("DATA", "Cash flow hedge reserve", m({"FY2025": -470073, "FY2024": -206240, "FY2023": -283405, "FY2022": -309566, "FY2021": -202208})),
    ("DATA", "Retained earnings", m({"FY2025": 64252213, "FY2024": 52444090, "FY2023": 39860631, "FY2022": 27855861, "FY2021": 18164698})),
    ("TOTAL", "Total equity", m({"FY2025": 124646361, "FY2024": 113102071, "FY2023": 100441447, "FY2022": 88410516, "FY2021": 78826711})),
    ("TOTAL", "Total liabilities and equity", m({"FY2025": 1250249467, "FY2024": 1125449351, "FY2023": 1070479178, "FY2022": 1018907764, "FY2021": 894731193})),
]
bw.add_balance_sheet_sheet(
    title="QIB (UK) plc — Balance Sheet",
    subtitle="Entity basis, £m, converted from the Bank's reported £ amounts; FY2021-FY2025. Each year's "
              "own originally-published figures are used - see RESTATEMENT NOTE at bottom.",
    rows=bs_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=66,
    source_height=380,
    unit_suffix=" (£m)",
)

pl_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Income from financing activities", m({"FY2025": 65547275, "FY2024": 69270359, "FY2023": 60989079, "FY2022": 31605685, "FY2021": 21439036})),
    ("DATA", "Income from investing activities", m({"FY2025": 7726355, "FY2024": 6228539, "FY2023": 4899705, "FY2022": 2535344, "FY2021": 1622287})),
    ("DATA", "Returns to banks and customers", m({"FY2025": -45712749, "FY2024": -47998896, "FY2023": -37367914, "FY2022": -14860836, "FY2021": -7938424})),
    ("TOTAL", "Net income from financing and investing activities", m({"FY2025": 27560881, "FY2024": 27500002, "FY2023": 28520870, "FY2022": 19280193, "FY2021": 15122899})),
    ("DATA", "Fees and commissions income", m({"FY2025": 2489591, "FY2024": 2208209, "FY2023": 1823107, "FY2022": 1842222, "FY2021": 1611384})),
    ("DATA", "Fees and commissions expense", m({"FY2025": -719061, "FY2024": -633508, "FY2023": -667574, "FY2022": -556172, "FY2021": -491526})),
    ("TOTAL", "Net fees and commissions income", m({"FY2025": 1770530, "FY2024": 1574701, "FY2023": 1155533, "FY2022": 1286050, "FY2021": 1119858})),
    ("DATA", "Net gain/(loss) on financial assets at fair value", m({"FY2025": -323866, "FY2024": 28013})),
    ("DATA", "Net gain/(loss) on financial assets at amortised cost", m({"FY2025": 103987, "FY2024": 25681, "FY2021": 25475})),
    ("DATA", "Net gain/(loss) on financial assets at FVPL", m({"FY2021": 95289})),
    ("DATA", "Gain/(loss) on foreign exchange", m({"FY2025": 330256, "FY2024": 198849, "FY2023": 251062, "FY2022": 248560, "FY2021": 83629})),
    ("DATA", "Other income", m({"FY2025": 120181, "FY2024": 477869, "FY2023": 172981, "FY2022": 124170, "FY2021": 91934})),
    ("DATA", "FV loss on investment property", m({"FY2023": -1440000, "FY2022": -905000})),
    ("TOTAL", "Total operating income", m({"FY2025": 29561969, "FY2024": 29805115, "FY2023": 28660446, "FY2022": 20033973, "FY2021": 16539084})),
    ("SECTION", "Expenses", {}),
    ("DATA", "Personnel expenses", m({"FY2025": -7814270, "FY2024": -7645092, "FY2023": -7169597, "FY2022": -6410143, "FY2021": -5758494})),
    ("DATA", "Depreciation and amortisation", m({"FY2025": -376722, "FY2024": -569224, "FY2023": -608256, "FY2022": -692789, "FY2021": -695265})),
    ("DATA", "Other expenses", m({"FY2025": -3944957, "FY2024": -3334767, "FY2023": -2857395, "FY2022": -2558521, "FY2021": -2192538})),
    ("TOTAL", "Total operating expenses", m({"FY2025": -12135949, "FY2024": -11549083, "FY2023": -10635248, "FY2022": -9661453, "FY2021": -8646297})),
    ("TOTAL", "Profit/(loss) before provisions for impairment", m({"FY2025": 17426020, "FY2024": 18256032, "FY2023": 18025198, "FY2022": 10372520, "FY2021": 7892787})),
    ("DATA", "Credit (loss)/reversal expense on financial assets", m({"FY2025": -1650686, "FY2024": -735091, "FY2023": -1048140, "FY2022": 638445, "FY2021": -661700})),
    ("DATA", "Impairment on building", m({"FY2023": -945738})),
    ("TOTAL", "Profit/(loss) before taxation", m({"FY2025": 15775334, "FY2024": 17520941, "FY2023": 16031320, "FY2022": 11010965, "FY2021": 7231087})),
    ("DATA", "Taxation", m({"FY2025": -4043683, "FY2024": -4918191, "FY2023": -4081371, "FY2022": -1318592, "FY2021": -375560})),
    ("TOTAL", "Profit/(loss) for the year", m({"FY2025": 11731651, "FY2024": 12602750, "FY2023": 11949949, "FY2022": 9692373, "FY2021": 6855527})),
    ("SECTION", "Other comprehensive income", {}),
    ("DATA", "Change in fair value of cash flow hedge", m({"FY2025": -263833, "FY2024": 77165, "FY2023": 26161, "FY2022": -107358, "FY2021": 81691})),
    ("TOTAL", "Total comprehensive profit/(loss) for the year", m({"FY2025": 11467818, "FY2024": 12679915, "FY2023": 11976110, "FY2022": 9585015, "FY2021": 6937218})),
]
bw.add_income_statement_sheet(
    title="QIB (UK) plc — Profit & Loss",
    subtitle="Entity basis, £m, converted from the Bank's reported £ amounts; FY2021-FY2025. Each year's "
              "own originally-published figures are used - see PRESENTATION NOTE at bottom.",
    rows=pl_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=66,
    source_height=380,
    unit_suffix=" (£m)",
)

equity_headers = ["Share Capital", "Cash Flow Hedge", "Retained Earnings", "Total"]
equity_rows = [
    ("DATA", "At 1 January 2021 (FY2021 opening)", (60.864, -0.284, 11.353, 71.933)),
    ("DATA", "Changes in FV of cash flow hedge", (None, 0.082, None, 0.082)),
    ("DATA", "Movement in deferred tax relating to change in tax rate", (None, None, -0.044, -0.044)),
    ("DATA", "Profit for the year", (None, None, 6.856, 6.856)),
    ("TOTAL", "At 31 December 2021", (60.864, -0.202, 18.165, 78.827)),
    ("DATA", "Changes in FV of cash flow hedge", (None, -0.107, None, -0.107)),
    ("DATA", "Movement in deferred tax relating to change in tax rate", (None, None, -0.001, -0.001)),
    ("DATA", "Profit for the year", (None, None, 9.692, 9.692)),
    ("TOTAL", "At 31 December 2022", (60.864, -0.310, 27.856, 88.411)),
    ("DATA", "Changes in FV of cash flow hedge", (None, 0.026, None, 0.026)),
    ("DATA", "Movement in deferred tax relating to recognition or change in tax rate", (None, None, 0.055, 0.055)),
    ("DATA", "Profit for the year", (None, None, 11.950, 11.950)),
    ("TOTAL", "At 31 December 2023", (60.864, -0.283, 39.861, 100.441)),
    ("DATA", "Changes in FV of cash flow hedge", (None, 0.077, None, 0.077)),
    ("DATA", "Movement in deferred tax relating to recognition or change in tax rate", (None, None, -0.019, -0.019)),
    ("DATA", "Profit for the year", (None, None, 12.603, 12.603)),
    ("TOTAL", "At 31 December 2024", (60.864, -0.206, 52.444, 113.102)),
    ("DATA", "Changes in FV of cash flow hedge", (None, -0.264, None, -0.264)),
    ("DATA", "Movement in deferred tax on cash flow hedge", (None, None, 0.076, 0.076)),
    ("DATA", "Profit for the year", (None, None, 11.732, 11.732)),
    ("TOTAL", "At 31 December 2025", (60.864, -0.470, 64.252, 124.646)),
]
bw.add_equity_changes_sheet(
    title="QIB (UK) plc — Statement of Changes in Equity",
    subtitle="Chronological roll-forward oldest to newest, entity basis, £m. Equity reconciliation ladder "
              "confirmed: every year's own closing balance ties exactly to both the next year's own opening "
              "balance and that year's own Balance Sheet Total equity - zero plug rows needed anywhere "
              "across all 5 years. The deferred-tax movement row's label changes across years (the Bank's "
              "own wording); all years' rows represent the same underlying deferred tax adjustment on the "
              "cash flow hedge reserve/retained earnings.",
    headers=equity_headers,
    rows=equity_rows,
    sources_text=STATEMENTS_SOURCES,
)

rows = [
 ("SECTION", "Operating activities", {}),
 ("DATA", "Profit for the year", m({"FY2025":11731651,"FY2024":12602750,"FY2023":11949949,"FY2022":9692373,"FY2021":6855527})),
 ("DATA", "Depreciation", m({"FY2025":365521,"FY2024":545924,"FY2023":559334,"FY2022":533941,"FY2021":559611})),
 ("DATA", "Amortisation", m({"FY2025":11201,"FY2024":23300,"FY2023":48921,"FY2022":158848,"FY2021":135654})),
 ("DATA", "Taxation", m({"FY2025":4043683,"FY2024":4918194,"FY2023":4081371,"FY2022":1318592,"FY2021":375560})),
 ("DATA", "Fair value / impairment adjustments", m({"FY2025":1783183,"FY2024":898730,"FY2023":2383878,"FY2022":1490529,"FY2021":760690})),
 ("DATA", "Increase/(decrease) in financing arrangements", m({"FY2025":-72273531,"FY2024":-57921880,"FY2023":-44846764,"FY2022":-51177541,"FY2021":-133182070})),
 ("DATA", "Stage 3 ECL recoveries", m({"FY2024":0,"FY2023":-3750,"FY2022":-1223974,"FY2021":-3700})),
 ("DATA", "Increase/(decrease) in other assets", m({"FY2025":-1238998,"FY2024":-523919,"FY2023":-53161,"FY2022":-2981020,"FY2021":-183119})),
 ("DATA", "Increase/(decrease) in amounts due to banks", m({"FY2025":24774922,"FY2024":-20343376,"FY2023":-2185645,"FY2022":-14991188,"FY2021":-5075581})),
 ("DATA", "Increase/(decrease) in amounts due to customers", m({"FY2025":83009697,"FY2024":59016367,"FY2023":41134935,"FY2022":122440389,"FY2021":162594916})),
 ("DATA", "Increase/(decrease) in other liabilities", m({"FY2025":539841,"FY2024":458933,"FY2023":-2293547,"FY2022":5356669,"FY2021":3613140})),
 ("DATA", "Increase/(decrease) in financial assets at amortised cost", m({"FY2025":-3660555,"FY2024":-20589713,"FY2023":-21599498,"FY2022":-68236950,"FY2021":-14259831})),
 ("DATA", "Increase/(decrease) in derivative financial instruments", m({"FY2025":1265068,"FY2024":-1126779,"FY2023":-130255,"FY2022":388846,"FY2021":-5152783})),
 ("DATA", "Source operating subtotal reconciliation (see source note)", m({"FY2024":735088,"FY2023":1050000})),
 ("TOTAL", "Net cash inflow/(outflow) from operating activities", m({"FY2025":50351683,"FY2024":-21306381,"FY2023":-9904232,"FY2022":2769514,"FY2021":17038014})),
 ("SECTION", "Investing activities", {}),
 ("DATA", "Purchase of property, plant and equipment", m({"FY2025":-65532,"FY2024":-685282,"FY2023":-54715,"FY2022":-4369,"FY2021":-37762})),
 ("DATA", "Purchase of intangible assets", m({"FY2025":-103738,"FY2021":-116000})),
 ("TOTAL", "Net cash outflow from investing activities", m({"FY2025":-169270,"FY2024":-685282,"FY2023":-54715,"FY2022":-4369,"FY2021":-153762})),
 ("SECTION", "Financing activities", {}),
 ("DATA", "Repayment/(increase) of subordinated Wakala", m({"FY2025":-35344,"FY2024":-32973,"FY2023":100909,"FY2021":-2250000})),
 ("TOTAL", "Net cash (outflow)/inflow from financing activities", m({"FY2025":-35344,"FY2024":-32973,"FY2023":100909,"FY2022":0,"FY2021":-2250000})),
 ("TOTAL", "Net increase/(decrease) in cash and cash equivalents", m({"FY2025":50147069,"FY2024":-22024636,"FY2023":-9858038,"FY2022":2765145,"FY2021":14634252})),
 ("DATA", "Cash and cash equivalents at start of year", m({"FY2025":82318198,"FY2024":49249786,"FY2023":59107824,"FY2022":56342679,"FY2021":41708427})),
 ("TOTAL", "Cash and cash equivalents at end of year", m({"FY2025":132465267,"FY2024":27225150,"FY2023":49249786,"FY2022":59107824,"FY2021":56342679})),
]
bw.add_cash_flow_sheet(title="QIB (UK) plc — Statement of Cash Flows", subtitle="Entity basis, £m, converted from the Bank's reported £ amounts; FY2021-FY2025.", rows=rows, sources_text=CASH_SOURCES, first_col_width=66, source_height=280, unit_suffix=" (£m)")

ASSET_QUALITY_SOURCES = (
    "Sources - QIB (UK) plc's own Annual Report, 'ECL breakdown' / 'Credit Quality' IFRS 9 stage 1/2/3 "
    "table for Financing Arrangements (Murabaha financing):\n"
    "FY2025 (own): Annual Report and Accounts 2025, p.55 - " + AR["FY2025"] + "\n"
    "FY2024 (own): Annual Report and Accounts 2024, p.56 - " + AR["FY2024"] + "\n"
    "FY2023 (own): Annual Report and Accounts 2023, p.54 - " + AR["FY2023"] + "\n"
    "FY2022 (own): Annual Report and Accounts 2022, p.55 - " + AR["FY2022"] + "\n"
    "FY2021 (own): Annual Report and Accounts 2021, p.51 - " + AR["FY2021"] + "\n\n"
    + ENTITY + "\n\n"
    "DATA QUALITY FLAG: the Bank's own note states these are the 'maximum credit exposure, including "
    "accrued profit' - for FY2021/FY2022 this note's own Total financing arrangements net figure "
    "(728,703,868 / 783,073,152) does NOT tie to that same year's own Balance Sheet 'Financing "
    "arrangements' line (726,026,105 / 777,848,982) - a genuine internal inconsistency within each of "
    "those two Annual Reports (the accrued-profit basis difference the note itself flags), not a "
    "transcription error here. From FY2023 onward this note's total ties exactly to the Balance Sheet."
)
asset_quality_rows = [
    ("SECTION", "Financing arrangements (Murabaha financing), gross carrying amount by IFRS 9 stage", {}),
    ("DATA", "Stage 1", m({"FY2025": 849001016, "FY2024": 768728253, "FY2023": 768684249, "FY2022": 761510966, "FY2021": 719077654})),
    ("DATA", "Stage 2", m({"FY2025": 94122611, "FY2024": 109923252, "FY2023": 60853408, "FY2022": 23168677, "FY2021": 5856639})),
    ("DATA", "Stage 3", m({"FY2025": 16609442, "FY2024": 8808032, "FY2023": 0, "FY2022": 7500, "FY2021": 7810910})),
    ("TOTAL", "Total gross carrying amount", m({"FY2025": 959733069, "FY2024": 887459537, "FY2023": 829537657, "FY2022": 784687143, "FY2021": 732745203})),
    ("SECTION", "ECL allowance by IFRS 9 stage", {}),
    ("DATA", "Stage 1", m({"FY2025": -832670, "FY2024": -933355, "FY2023": -1079806, "FY2022": -890540, "FY2021": -746630})),
    ("DATA", "Stage 2", m({"FY2025": -553439, "FY2024": -2455724, "FY2023": -1582482, "FY2022": -715951, "FY2021": -281223})),
    ("DATA", "Stage 3", m({"FY2025": -3663500, "FY2024": -10500, "FY2023": 0, "FY2022": -7500, "FY2021": -3013482})),
    ("TOTAL", "Total ECL allowance", m({"FY2025": -5049609, "FY2024": -3399579, "FY2023": -2662288, "FY2022": -1613991, "FY2021": -4041335})),
    ("TOTAL", "Net financing arrangements (per this note)", m({"FY2025": 954683460, "FY2024": 884059958, "FY2023": 826875369, "FY2022": 783073152, "FY2021": 728703868})),
    ("SECTION", "Asset quality ratios (derived)", {}),
    ("DATA", "Stage 3 as % of total gross carrying amount (NPL ratio)",
     {"FY2025": "1.73%", "FY2024": "0.99%", "FY2023": "0.00%", "FY2022": "0.00%", "FY2021": "1.07%"}),
    ("DATA", "Total ECL allowance as % of total gross carrying amount (coverage)",
     {"FY2025": "0.53%", "FY2024": "0.38%", "FY2023": "0.32%", "FY2022": "0.21%", "FY2021": "0.55%"}),
]
bw.add_asset_quality_sheet(
    title="QIB (UK) plc — Asset Quality",
    subtitle="Financing arrangements (Murabaha financing), IFRS 9 stage 1/2/3 gross carrying amount and "
              "ECL allowance. Entity basis, £m. See DATA QUALITY FLAG at bottom for FY2021/FY2022's own "
              "internal note-vs-Balance Sheet basis difference.",
    rows=asset_quality_rows,
    sources_text=ASSET_QUALITY_SOURCES,
    first_col_width=76,
    source_height=340,
    unit_suffix=" (£m)",
)

def metric(name, unit, data, note=None): bw.add_metric_sheet(name, unit, data, p3_sources(), note=note, first_col_width=50, source_height=220)
cap={"FY2025":124.259,"FY2024":113.099,"FY2023":98.878,"FY2022":86.739,"FY2021":78.028}; total={"FY2025":137.959,"FY2024":126.799,"FY2023":112.578,"FY2022":96.585,"FY2021":91.081}; rwa={"FY2025":693.154,"FY2024":601.928,"FY2023":543.184,"FY2022":499.121,"FY2021":462.020}
ratios={"CET1 Ratio":{"FY2025":"17.93%","FY2024":"18.79%","FY2023":"18.20%","FY2022":"17.38%","FY2021":"16.89%"},"Total Capital Ratio":{"FY2025":"19.90%","FY2024":"21.07%","FY2023":"20.73%","FY2022":"19.35%","FY2021":"19.71%"},"Leverage Ratio":{"FY2025":"10.67%","FY2024":"10.53%","FY2023":"9.61%","FY2022":"8.50%","FY2021":"8.75%"},"LCR":{"FY2025":"345.59%","FY2024":"322.05%","FY2023":"1153.62%","FY2022":"1236.14%","FY2021":"555.60%"},"NSFR":{"FY2025":"127.95%","FY2024":"128.20%","FY2023":"130.56%","FY2022":"129.18%","FY2021":"119.68%"}}
metric("CET1 Capital","£m",[("Common Equity Tier 1 (CET1) capital",cap)]); metric("CET1 Ratio","% of RWA",[("Common Equity Tier 1 ratio",ratios["CET1 Ratio"])]); metric("Tier 1 Capital","£m",[("Tier 1 capital",cap)],"KM1 reports Tier 1 equal to CET1; no AT1 capital is reported."); metric("Tier 1 Ratio","% of RWA",[("Tier 1 ratio",ratios["CET1 Ratio"])]); metric("Total Capital","£m",[("Total capital",total)]); metric("Total Capital Ratio","% of RWA",[("Total capital ratio",ratios["Total Capital Ratio"])]); metric("Total RWAs","£m",[("Total risk-weighted exposure amount",rwa)])

rwa_breakdown_rows = [
    ("DATA", "Credit risk (excluding CCR)", {"FY2025": 634.742, "FY2024": 548.789, "FY2023": 500.902, "FY2022": 465.681, "FY2021": 432.383}),
    ("DATA", "Counterparty credit risk (CCR, including CVA)", {"FY2025": 3.345, "FY2024": 4.023, "FY2023": 1.390, "FY2022": 1.852, "FY2021": 2.166}),
    ("DATA", "Position, foreign exchange and commodities risk (market risk)", {"FY2025": 0.049, "FY2024": 0.053, "FY2023": 0.122, "FY2022": 0.044, "FY2021": 0.031}),
    ("DATA", "Operational risk", {"FY2025": 55.017, "FY2024": 49.062, "FY2023": 40.771, "FY2022": 31.545, "FY2021": 27.440}),
    ("TOTAL", "Total risk-weighted exposure amount", {"FY2025": 693.154, "FY2024": 601.927, "FY2023": 543.185, "FY2022": 499.122, "FY2021": 462.020}),
]
bw.add_rwa_breakdown_sheet(
    title="QIB (UK) plc — RWA Breakdown",
    subtitle="Pillar 3 UK OV1 template (top-level risk-type categories), £m.",
    rows=rwa_breakdown_rows,
    sources_text=p3_sources() + (
        "\n\nRWA BREAKDOWN: sourced from Template UK OV1 - Overview of risk weighted exposure amounts "
        "(p.7 of each year's own Pillar 3 document). Each year's own OV1 table gives that year's own column "
        "plus the prior year's comparative column; FY2021's figures are read from the FY2022 Pillar 3 "
        "document's own comparative column (its own standalone OV1 table not being available this session). "
        "This sheet's totals (693.154 / 601.927 / 543.185 / 499.122 / 462.020) are within £1k of the "
        "pre-existing Total RWAs sheet's figures (693.154 / 601.928 / 543.184 / 499.121 / 462.020) - an "
        "immaterial rounding difference between the two Pillar 3 tables, not an error."
    ),
    first_col_width=64,
    source_height=220,
    unit_suffix=" (£m)",
)

metric("Leverage Ratio","%",[("Leverage ratio excluding claims on central banks",ratios["Leverage Ratio"])]); metric("LCR","%",[("Liquidity coverage ratio",ratios["LCR"])]); metric("NSFR","%",[("Net stable funding ratio",ratios["NSFR"])]); metric("MREL Ratio","%",[("MREL ratio",{y:"Not publicly disclosed" for y in YEARS})],"No MREL ratio or requirement is disclosed in the reviewed QIB UK Pillar 3 documents.")

bs_totals = {r[1]: r[2] for r in bs_rows}
pl_totals = {r[1]: r[2] for r in pl_rows}
bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", bs_totals["Total assets"]),
        ("Financing arrangements", bs_totals["Financing arrangements"]),
        ("Due to customers", bs_totals["Due to customers"]),
        ("Total equity", bs_totals["Total equity"]),
    ],
    balance_sheet_unit="£m",
    income_statement_totals=[
        ("Total operating income", pl_totals["Total operating income"]),
        ("Total operating expenses", pl_totals["Total operating expenses"]),
        ("Profit/(loss) for the year", pl_totals["Profit/(loss) for the year"]),
    ],
    income_statement_unit="£m",
    equity_changes_totals=[
        ("Opening equity", {"FY2025": 113.102, "FY2024": 100.441, "FY2023": 88.411, "FY2022": 78.827, "FY2021": 71.933}),
        ("Profit for the year", {"FY2025": 11.732, "FY2024": 12.603, "FY2023": 11.950, "FY2022": 9.692, "FY2021": 6.856}),
        ("Other equity movements, net", {"FY2025": -0.188, "FY2024": 0.058, "FY2023": 0.081, "FY2022": -0.108, "FY2021": 0.038}),
        ("Closing equity", {"FY2025": 124.646, "FY2024": 113.102, "FY2023": 100.441, "FY2022": 88.411, "FY2021": 78.827}),
    ],
    equity_changes_unit="£m",
    cash_flow_totals=[("Net cash inflow/(outflow) from operating activities",rows[15][2]),("Net cash outflow from investing activities",rows[18][2]),("Net cash (outflow)/inflow from financing activities",rows[21][2]),("Cash and cash equivalents at end of year",rows[24][2])],
    cash_flow_unit="£m",
    ratios=list(ratios.items()),
    note="Figures are duplicated from detail sheets; see each detail sheet's source citation.",
)
bw.save("/Users/armaan/code/katalysis/banks/QIB UK FINANCIALS.xlsx")
