"""Builds the production client deliverable: a static multi-page site
(comparison.html, banks.html, bank-<slug>.html, workbook-<slug>.html) at
`deliverable/` in the repo root, covering all 145 banks.

Migrated from the IN-042 prototype (see wayfinder/insights/tickets/IN-051.md
for the migration decisions) - same "institutional ledger" design, now the
real deliverable rather than a throwaway mockup. Reads every metric straight
from `research/insights.db` at generation time via in040_risk_metrics.py's
and in041_spend_metrics.py's payload builders, called in-process rather than
through their cached JSON snapshots (research/in040_risk_metrics.json and
in041_spend_metrics.json still get written by those scripts for other
consumers, but this build never depends on them staying fresh). Also pulls
Weatherbys' Pillar 3 credit-risk-exposure-by-class breakdown directly from
the database, since Weatherbys discloses no IFRS 9 stage split at all (per
IN-039's finding) and IN-040's stage-only extraction has nothing to show for
it - see IN-042's ticket Resolution for why this substitute view was chosen
over dropping the bank.

Run: python3 scripts/insights/build_deliverable.py
Then open deliverable/comparison.html directly in a browser. Wired into
refresh_all.py's default sequence.
"""

import argparse
import json
import re
import shutil
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "deliverable"
DB_PATH = ROOT / "research" / "insights.db"

sys.path.insert(0, str(ROOT / "scripts" / "insights"))
from in012_absolute_analysis import classify_amount_unit  # noqa: E402
from in040_risk_metrics import build_in040_payload  # noqa: E402
from in041_spend_metrics import build_in041_payload  # noqa: E402
from build_workbook_viewer import render_workbook_viewer  # noqa: E402

# "Profit or loss for the year" headline-figure selector. Deliberately two
# separate co-occurring patterns rather than one combined regex requiring
# "profit"/"loss" to sit immediately before the suffix -
# in040_risk_metrics.py's _PROFIT_LOSS_RE requires exactly that adjacency
# ((profit|loss)\s+for\s+the\s+year), which fails on the very common
# "Profit/(loss) for the year" and "(Loss)/profit for the year" slash-
# parenthesis formats (the word right before "for" is ")", not "profit" or
# "loss"). Requiring only that both fragments appear anywhere in the label
# - guarded by the same exclude list - catches those formats plus
# Birmingham Bank's "Loss for the financial year" and Barclays Bank PLC's
# standalone "Profit after tax" (no "for the year" at all), all three of
# which this batch's real data hit and a stricter regex silently dropped.
# "surplus|deficit" added for Methodist Chapel Aid (IN-042e), a mutual/
# charity whose accounts use that vocabulary instead of "profit"/"loss"
# throughout - isolated to that one bank in the full 145-bank label survey,
# low collision risk.
_PROFIT_LOSS_RE = re.compile(r"profit|loss|surplus|deficit", re.I)
_PROFIT_LOSS_SUFFIX_RE = re.compile(r"for\s+the\s+(financial\s+)?(year|period)|after\s+tax", re.I)
_PROFIT_LOSS_EXCLUDE_RE = re.compile(r"discontinued|comprehensive|before tax|before taxation", re.I)
# "attributable"/"minority"/"non-controlling" used to be hard-excluded
# alongside the above, to avoid picking a parent-only or NCI-split figure
# over a bank's real group-level headline when BOTH exist. But several
# banks with no minority interest at all (Unity Trust) disclose ONLY
# "Profit for the year attributable to shareholders" - there, that line
# IS the headline, not an NCI split, and the hard exclusion left the whole
# bank-year with no profit figure despite one being clearly disclosed
# (found via a 2026-09-04 user report). Keep these as a soft/fallback
# exclusion instead - used only when nothing else in the year matched.
_PROFIT_LOSS_SOFT_EXCLUDE_RE = re.compile(r"attributable|minority|non-controlling", re.I)

# Same unit-normalization convention as in041_spend_metrics.py's
# _UNIT_MULTIPLIER: absolute P&L figures are reported in whatever unit each
# bank's filing uses (£'000 for most, £m for Barclays Bank UK) - scale every
# absolute figure to actual GBP at the point it's read.
UNIT_MULTIPLIER = {"GBP_thousand": 1_000, "GBP_million": 1_000_000, "GBP_unit": 1}


def scaled(value, unit):
    # None (rather than a 1x default) for a unit that isn't a recognized GBP
    # variant - a bank reporting in USD (Standard Chartered Bank, $m) or with
    # no unit metadata at all must not have its absolute figures silently
    # treated as GBP; every caller drops the row when this returns None
    # rather than propagate it into further arithmetic.
    mult = UNIT_MULTIPLIER.get(classify_amount_unit(unit or ""))
    return None if mult is None else value * mult

CAPITAL_METRICS = ["cash_pct_of_assets", "loans_pct_of_assets", "treasury_investments_pct_of_assets"]
COST_METRICS = [
    "cost_to_income_pct", "revenue", "total_operating_expense",
    "personnel_expense", "other_operating_expense",
]

# Widened from the original 4 stress-test banks to ~20 for IN-042's "how does
# this look at scale" check - a deliberately mixed set (big-4 retail,
# challenger/digital, specialist lender, private bank, wholesale/markets,
# international) rather than another 16 similar banks, so the comparison
# grids and per-bank color palette get genuinely exercised before the full
# 145-bank rollout. Still not all 145 - that's IN-043's real build.
BANKS = {
    "Monzo": "730427",
    "Barclays Bank UK": "759676",
    "Weatherbys": "204571",
    "Gulf International Bank UK": "124772",
    "Starling Bank": "730166",
    "HSBC UK Bank": "765112",
    "Lloyds Bank": "119278",
    "Santander UK": "106054",
    "TSB Bank": "191240",
    "Metro Bank": "488982",
    "Atom Bank": "661960",
    "Aldermore Bank": "204503",
    "Shawbrook Bank": "204574",
    "Secure Trust Bank": "204550",
    "Investec Bank": "172330",
    "C. Hoare & Co": "122093",
    "Standard Chartered Bank": "114276",
    "NatWest Markets": "121882",
    "Vanquis Bank": "221156",
    "Clydesdale Bank": "121873",
    # IN-042b batch: alphabetical A-B slice of the remaining 125 banks.
    "ABC International Bank": "149025",
    "Access Bank UK": "478415",
    "Afin Bank": "1004742",
    "AIB Group UK": "122088",
    "Allica": "821851",
    "Alpha Bank London": "135327",
    "Alrayan Bank": "229148",
    "Arab Bank Europe": "446951",
    "Arbuthnot Latham": "143336",
    "Bank Mandiri Europe": "204424",
    "Bank of Africa UK": "454750",
    "Bank of Beirut UK": "219523",
    "Bank of Ceylon UK": "514744",
    "Bank of China UK": "467410",
    "Bank of Ireland UK": "512956",
    "Bank of Scotland": "169628",
    "Bank of the Philippine Islands Europe": "455378",
    "Bank Saderat": "204488",
    "Bank Sepah International": "208019",
    "Barclays Bank": "122702",
    # IN-042c batch: alphabetical B-C slice of the remaining 105 banks.
    "Birmingham Bank": "204478",
    "BLME": "464292",
    "BNY Mellon International": "183100",
    "British Arab Commercial Bank": "204564",
    "Brown Shipley": "124548",
    "Caf Bank": "204451",
    "Cambridge and Counties Bank": "579415",
    "Castle Trust Capital": "541910",
    "Cater Allen": "178737",
    "Charity Bank": "207701",
    "Charter Court Financial Services": "494549",
    "Chetwood": "740551",
    "Citibank UK": "805574",
    "Clearbank": "754568",
    "Close Brothers": "124750",
    "Co-operative Bank": "121885",
    "Coutts": "122287",
    "Credit Suisse International": "146702",
    "Credit Suisse UK": "124269",
    "Crown Agents Bank": "204456",
    # IN-042d batch: alphabetical C-H slice of the remaining 85 banks.
    "Cynergy Bank": "575105",
    "DB UK Bank": "140848",
    "DF Capital Bank": "848291",
    "EFG Private Bank": "144036",
    "FCE Bank": "204469",
    "FCMB UK": "502704",
    "Fidbank UK": "400712",
    "Firstbank UK": "216772",
    "Gatehouse Bank": "475346",
    "GB Bank": "850286",
    "Ghana International Bank": "204471",
    "Goldman Sachs International Bank": "124659",
    "Griffin Bank": "970920",
    "Guaranty Trust Bank UK": "466611",
    "Habib Bank Zurich": "627671",
    "Hampden & Co": "606934",
    "Hampshire Trust Bank": "204601",
    "Handelsbanken": "806852",
    "Havin Bank": "204481",
    "HBL Bank UK": "188585",
    # IN-042e batch: alphabetical H-M slice of the remaining 65 banks.
    "HSBC Bank": "114216",
    "HSBC Innovation Bank": "543146",
    "ICBC (London)": "222030",
    "ICBC Standard Bank": "124823",
    "ICICI Bank UK": "223268",
    "iFAST Global Bank": "716167",
    "Itau BBA International": "575225",
    "Jordan International Bank": "183722",
    "JP Morgan Europe": "124579",
    "JP Morgan Securities": "155240",
    "Julian Hodge Bank": "204439",
    "KEXIM Bank UK": "204490",
    "Kingdom Bank": "400972",
    "Kroo Bank": "953772",
    "Kuwait Finance House": "131818",
    "LHV": "993767",
    "Lloyds Bank Corporate Markets": "763256",
    "Marks and Spencer Financial Services": "151427",
    "Melli Bank": "207380",
    "Methodist Chapel Aid": "204508",
    # IN-042f batch: alphabetical M-R slice of the remaining 45 banks.
    "Mizuho International": "119256",
    "Monument Bank": "849724",
    "Morgan Stanley Bank International": "195430",
    "National Bank of Egypt UK": "204520",
    "National Bank of Kuwait International": "171532",
    "National Westminster Bank": "121878",
    "Nomura Bank International": "204419",
    "Northern Bank": "122261",
    "OakNorth Bank": "629564",
    "Onesavings": "530504",
    "Oxbury": "834822",
    "Paragon": "604551",
    "Perenna": "956138",
    "Persia International Bank": "208020",
    "Philippine National Bank Europe": "204532",
    "Punjab National Bank International": "459701",
    "QIB UK": "466577",
    "Rathbones Investment Management": "116316",
    "RBC Europe": "124543",
    "RBS": "114724",
    # IN-042g batch: alphabetical R-U slice of the remaining 25 banks.
    "RCI Bank UK": "815220",
    "Recognise Bank": "849404",
    "Redwood Bank": "755924",
    "Reliance Bank": "204537",
    "Santander Financial Services": "146003",
    "Schroder": "144206",
    "SMBC": "223304",
    "State Bank of India UK": "757156",
    "Streambank": "954876",
    "Tandem": "204479",
    "TD Bank Europe": "165556",
    "The Bank of London Group": "930379",
    "This Bank": "832786",
    "Triodos": "817008",
    "Turkish Bank UK": "204566",
    "UBA UK": "695048",
    "Union Bancaire Privee UK": "119250",
    "Union Bank of India UK": "601551",
    "United National": "207381",
    "United Trust Bank": "204463",
    # IN-042h batch: final alphabetical U-Z slice, completing all 145 banks.
    "Unity Trust": "204570",
    "Vida": "738741",
    "Zempler": "671140",
    "Zenith": "451720",
    "Zopa": "800542",
}


def slugify(name):
    return re.sub(r"^-+|-+$", "", re.sub(r"[^a-z0-9]+", "-", name.lower()))


_RATIO_KEYWORDS = ["ratio", "coverage", "share", "of which"]


def is_ratio_category(name):
    # "ecl"/"impairment"/"allowance" used to be blanket keywords here too,
    # but all three name genuine BALANCE amounts at least as often as
    # ratios ("ECL allowance", "impairment provision", "loss allowance" are
    # money, not a percentage) - the blanket match was silently dropping
    # every such category across most banks with real IFRS 9 stage data,
    # not just an edge case (Unity Trust's, Secure Trust Bank's, and ~140
    # other category strings, found via a 2026-09-04 user report that a
    # bank's own worksheet clearly had this data when the comparison page
    # claimed it didn't). "%" / "/" plus "ratio"/"coverage"/"share"/"of
    # which" catch every real ratio label already found in the dataset;
    # removing the three broad keywords cost no genuine ratio exclusion
    # when checked against the full 145-bank category set.
    #
    # Whole-string keyword matching is right for most real category shapes
    # (e.g. "Coverage ratio - Stage 3" needs its PARENT segment's
    # "Coverage ratio" to be seen, since the descriptor after the stage
    # marker can be a bare qualifier with no keyword of its own) - but one
    # specific parent-header shape coordinates multiple concept types under
    # one heading ("IFRS 9 stage split AND coverage, portfolio-total
    # level"), so a real gross-balance row nested under it (" - gross
    # carrying amount") false-positives on "coverage" even though this row
    # isn't a coverage ratio. Narrowly re-check using only the segments
    # after a header matching that "X and coverage" shape, rather than
    # dropping every parent header.
    if "%" in name or "/" in name:
        return True
    n = name.lower()
    if not any(k in n for k in _RATIO_KEYWORDS):
        return False
    segments = name.split(" - ")
    if len(segments) > 1 and re.search(r"\band\s+coverage\b", segments[0], re.I):
        tail = " - ".join(segments[1:])
        tn = tail.lower()
        return "%" in tail or "/" in tail or any(k in tn for k in _RATIO_KEYWORDS)
    return True


def normalize_pnl_year(year):
    # Profit & Loss years carry entity suffixes for Monzo's group restructure
    # ("FY2024 (MBHG)*") that the rest of this prototype's data doesn't - strip
    # down to the bare 4-digit year so it lines up with rwa_to_assets_pct etc.
    m = re.match(r"(\d{4})", year.replace("FY", ""))
    return m.group(1) if m else year.replace("FY", "")


def canonical_income_category(item):
    l = item.lower()
    if l.startswith("other"):
        return None
    if "net interest income" in l:
        return "Net interest income"
    if "net fee and commission income" in l:
        return "Net fee and commission income"
    if "net trading income" in l or "net investment income" in l:
        return "Trading & investment income"
    return None


def is_other_income(item):
    l = item.lower()
    return "other operating income" in l or l == "other income" or "rent receivable" in l or "other interest income" in l


PILLAR3_SHEETS = ["CET1 Ratio", "Tier 1 Ratio", "Total Capital Ratio", "Leverage Ratio", "LCR", "NSFR", "MREL Ratio"]


def _pillar3_rank(label):
    # Some banks (Monzo, Barclays Bank UK) disclose more than one leverage-
    # ratio variant per year as the KM1 template basis changed over time
    # (CRR "including claims on central banks" retired FY2022) - prefer the
    # basis excluding central-bank claims (the current standard), falling
    # back to whatever's actually disclosed for a given year.
    l = label.lower()
    if "excluding claims on central banks" in l:
        return 0
    if "including claims on central banks" in l:
        return 2
    if "km1 format" in l:
        return 3
    return 1


def curate_pillar3(conn, frn):
    """One ratio row per (sheet, year): CET1/Tier1/Total Capital/Leverage
    ratios, LCR, NSFR, MREL ratio. Each Pillar 3 sheet also carries its own
    absolute numerator/denominator rows (e.g. Leverage Ratio's "Leverage
    exposure measure", LCR's "Total high-quality liquid assets", MREL
    Ratio's "Total MREL resources") under wildly inconsistent labels across
    banks - a label-substring exclude list chased one variant at a time and
    still missed "Leverage exposure measure" (no "total" prefix) for NatWest
    Markets, producing a 100,000%+ chart scale. value_raw carries the '%'
    for every genuine ratio disclosure regardless of label wording, so
    filter on that instead of guessing at label phrasing."""
    out = {}
    for sheet in PILLAR3_SHEETS:
        rows = conn.execute(
            "SELECT row_label, year, value_numeric, value_raw FROM annual_metrics "
            "WHERE frn=? AND sheet=? AND value_numeric IS NOT NULL",
            (frn, sheet),
        ).fetchall()
        by_year = {}
        for row_label, year, value, value_raw in rows:
            if not value_raw or "%" not in value_raw:
                continue
            item = row_label.split(" - ", 1)[1] if " - " in row_label else row_label
            y = normalize_pnl_year(year)
            current = by_year.get(y)
            if current is None or _pillar3_rank(item) < _pillar3_rank(current[0]):
                by_year[y] = (item, value)
        out[sheet] = {y: v for y, (_, v) in by_year.items()}
    return out


def canonical_cashflow_category(item):
    l = item.lower()
    if "end of" in l:
        return None
    if "net" in l and ("increase" in l or "decrease" in l) and "cash and cash equivalents" in l:
        return "Net change in cash"
    if "operat" in l:
        return "Operating activities"
    if "invest" in l:
        return "Investing activities"
    if "financ" in l:
        return "Financing activities"
    return None


def curate_cashflow(conn, frn):
    """Operating / investing / financing / net-change cash flow per year,
    from the raw Cash Flow Statement sheet - row labels vary bank to bank
    ("Cash from operations" vs "Net cash from operating activities") so
    matched by keyword rather than a fixed schema, same convention as the
    Profit & Loss extraction above."""
    rows = conn.execute(
        "SELECT row_label, year, value_numeric, unit FROM annual_metrics "
        "WHERE frn=? AND sheet='Cash Flow Statement' AND value_numeric IS NOT NULL",
        (frn,),
    ).fetchall()
    by_year = {}
    for row_label, year, value, unit in rows:
        scaled_value = scaled(value, unit)
        if scaled_value is None:
            continue
        item = row_label.split(" - ", 1)[1] if " - " in row_label else row_label
        cat = canonical_cashflow_category(item)
        if cat:
            by_year.setdefault(normalize_pnl_year(year), {})[cat] = scaled_value
    return by_year


def curate_equity_changes(conn, frn):
    """Statement of Changes in Equity, straight off the `equity_changes`
    table - a chronological roll-forward (movement rows x equity-component
    columns), not the year-column shape every other sheet here uses, so it's
    pivoted into {components: [...], rows: [{label, values: {component: raw}}]}
    for a plain table render rather than forced into a chart. Component
    order follows first-seen order across `row_order` (the sheet's own
    oldest-to-newest read order), matching how the column appears in the
    source workbook - never re-sorted alphabetically."""
    rows = conn.execute(
        "SELECT movement_label, component, value_raw, row_order FROM equity_changes "
        "WHERE frn=? ORDER BY row_order",
        (frn,),
    ).fetchall()
    components = []
    seen = set()
    by_order = {}
    for movement_label, component, value_raw, row_order in rows:
        if component not in seen:
            seen.add(component)
            components.append(component)
        entry = by_order.setdefault(row_order, {"label": movement_label, "values": {}})
        entry["values"][component] = value_raw
    ordered_rows = [by_order[k] for k in sorted(by_order)]
    return {"components": components, "rows": ordered_rows}


def curate_income_pnl(conn, frn):
    """Net interest / net fee / trading / other income mix + profit for the
    year, from the raw Profit & Loss sheet. Row labels are heterogeneous
    across banks (real disclosures, not a shared schema) - e.g. some banks
    only disclose gross interest/fee income and expense with no explicit
    "Net ..." line for a given year (Monzo's FY2025 filing), so net income is
    computed from the gross pair as a fallback when the net line is absent.
    """
    rows = conn.execute(
        "SELECT row_label, year, value_numeric, unit FROM annual_metrics "
        "WHERE frn=? AND sheet='Profit & Loss' AND value_numeric IS NOT NULL",
        (frn,),
    ).fetchall()

    by_year_raw = {}  # year -> {item: value}, value already scaled to actual GBP
    for row_label, year, value, unit in rows:
        scaled_value = scaled(value, unit)
        if scaled_value is None:
            continue
        item = row_label.split(" - ", 1)[1] if " - " in row_label else row_label
        by_year_raw.setdefault(normalize_pnl_year(year), {})[item] = scaled_value

    breakdown = {}
    profit_for_year = {}
    for year, items in by_year_raw.items():
        cats = {}
        soft_excluded_candidates = []
        for item, value in items.items():
            l = item.lower()
            # A bank in a loss year reports "Loss for the financial year",
            # not "Profit ..." (Birmingham Bank, IN-042c) - checking only
            # "profit" silently dropped every loss-making bank-year's
            # headline figure. But a broad "profit OR loss" + "for the
            # year" match also sweeps in OCI/comprehensive-income lines
            # ("Total comprehensive income/(loss) for the year") which
            # contain "loss" too - reuse in040_risk_metrics.py's proven
            # _PROFIT_LOSS_RE/_PROFIT_LOSS_EXCLUDE_RE pair instead of a
            # bespoke heuristic here.
            #
            # A blanket "comprehensive" exclusion over-corrects, though:
            # several small banks with zero OCI items disclose one combined
            # line, "Profit/(loss) for the year and total comprehensive
            # income/(loss)" (Hampden & Co, Havin Bank, Charity Bank,
            # IN-042d) - a genuine headline figure, not a pure-OCI line.
            # Distinguish by word order: a pure OCI line always leads with
            # "comprehensive" ("Total comprehensive income for the year"
            # - "comprehensive" is the first substantive word), while the
            # combined headline always leads with "profit"/"loss" itself
            # ("(Loss)/profit and total comprehensive income for the
            # financial year", "Profit/(loss) for the year and total
            # comprehensive income" - "profit"/"loss" is the first
            # substantive word regardless of where "comprehensive" or the
            # suffix match land relative to EACH OTHER, which is why
            # comparing against the suffix match's position (IN-042d's
            # first attempt) still missed Kingdom Bank's phrasing, where
            # "comprehensive" sits before the suffix even in a genuine
            # combined line). Compare against the profit/loss match's own
            # position instead - only exclude when "comprehensive" appears
            # before the first "profit"/"loss" token.
            pl_match = _PROFIT_LOSS_RE.search(l)
            suffix_match = _PROFIT_LOSS_SUFFIX_RE.search(l)
            comprehensive_idx = l.find("comprehensive")
            comprehensive_leads = pl_match and comprehensive_idx != -1 and comprehensive_idx < pl_match.start()
            other_exclude = _PROFIT_LOSS_EXCLUDE_RE.search(re.sub(r"comprehensive", "", l))
            if pl_match and suffix_match and not comprehensive_leads and not other_exclude:
                if _PROFIT_LOSS_SOFT_EXCLUDE_RE.search(l):
                    soft_excluded_candidates.append(value)
                else:
                    profit_for_year[year] = value
                continue
            cat = canonical_income_category(item)
            if cat:
                cats[cat] = cats.get(cat, 0) + value
            elif is_other_income(item):
                cats["Other income"] = cats.get("Other income", 0) + value

        if year not in profit_for_year and soft_excluded_candidates:
            profit_for_year[year] = soft_excluded_candidates[0]

        if "Net interest income" not in cats:
            income = sum(v for k, v in items.items() if not k.lower().startswith("other")
                         and any(p in k.lower() for p in ["interest income", "interest receivable", "interest and similar income"]))
            expense = sum(v for k, v in items.items()
                          if any(p in k.lower() for p in ["interest expense", "interest payable", "interest and similar expense"]))
            if income:
                cats["Net interest income"] = income + expense
        if "Net fee and commission income" not in cats:
            income = sum(v for k, v in items.items()
                         if any(p in k.lower() for p in ["fee and commission income", "fees and commissions receivable"]))
            expense = sum(v for k, v in items.items()
                          if any(p in k.lower() for p in ["fee and commission expense", "fees and commissions payable"]))
            if income:
                cats["Net fee and commission income"] = income + expense

        if cats:
            breakdown[year] = cats
    return breakdown, profit_for_year


def curate():
    d = build_in040_payload(DB_PATH)
    out = {}
    for label, frn in BANKS.items():
        stage = d["loan_concentration_quality"]["stage_balances"].get(frn, {})
        per_year = {}
        for year, cats in stage.items():
            balance_cats = {k: v for k, v in cats.items() if not is_ratio_category(k)}
            if balance_cats:
                per_year[year] = balance_cats
        entry = {
            "frn": frn,
            "coverage_npl": d["loan_concentration_quality"]["coverage_and_npl_ratios"].get(frn, []),
            "rwa_to_assets_pct": d["rwa_density"]["rwa_to_assets_pct"].get(frn, {}),
        }
        entry["loan_composition"] = (
            {"kind": "stage", "years": per_year} if per_year else {"kind": "none", "years": {}}
        )
        cat = {}
        for key, rows in d["rwa_density"]["rwa_category_composition"].items():
            f, y = key.split(":")
            if f == frn:
                cat[y] = rows
        entry["rwa_category_composition"] = cat
        out[label] = entry

    # Balance Sheet / P&L derived metrics (IN-041) - "where is this bank
    # making money": capital_deployment is a Balance Sheet asset mix,
    # cost_base is a P&L cost structure. Reshape from metric-keyed to
    # year-keyed per bank, matching the loan_composition/rwa shapes above.
    spend = build_in041_payload(DB_PATH)
    for label, frn in BANKS.items():
        cap_years = {}
        for m in CAPITAL_METRICS:
            for y, v in (spend["capital_deployment"][m].get(frn) or {}).items():
                cap_years.setdefault(y, {})[m] = v
        cost_years = {}
        for m in COST_METRICS:
            for y, v in (spend["cost_base"][m].get(frn) or {}).items():
                cost_years.setdefault(y, {})[m] = v
        out[label]["capital_deployment"] = cap_years
        out[label]["cost_base"] = cost_years

    conn = sqlite3.connect(DB_PATH)
    for label, frn in BANKS.items():
        income_breakdown, profit_for_year = curate_income_pnl(conn, frn)
        out[label]["income_breakdown"] = income_breakdown
        out[label]["profit_for_year"] = profit_for_year
        out[label]["pillar3"] = curate_pillar3(conn, frn)
        out[label]["cash_flow"] = curate_cashflow(conn, frn)
        out[label]["equity_changes"] = curate_equity_changes(conn, frn)
        source_workbook = conn.execute(
            "SELECT source_workbook FROM banks WHERE frn=?", (frn,)
        ).fetchone()
        out[label]["source_workbook"] = source_workbook[0] if source_workbook else None

    # IN-041's revenue selector requires an explicit "Total operating
    # income"/"Total income"/"Net operating income" row, so a year with none
    # of those (Monzo's FY2025 filing) has no cost_to_income_pct even though
    # the underlying income lines exist - the income_breakdown just computed
    # above (which does have a same-basis fallback for exactly this case)
    # can fill that gap, so the trend doesn't just stop at the newest year.
    for label in BANKS:
        cost_years = out[label]["cost_base"]
        for year, cats in out[label]["income_breakdown"].items():
            entry = cost_years.setdefault(year, {})
            if entry.get("revenue") is not None:
                continue
            synth_revenue = sum(cats.values())
            total_opex = entry.get("total_operating_expense")
            if synth_revenue > 0:
                entry["revenue"] = synth_revenue
                entry["revenue_is_synthesized"] = True
                if total_opex is not None and entry.get("cost_to_income_pct") is None:
                    entry["cost_to_income_pct"] = round(abs(total_opex) / synth_revenue * 100, 2)

    # Weatherbys discloses no IFRS 9 stage split - substitute its real Pillar 3
    # credit-risk exposure-by-class breakdown instead of leaving it empty.
    rows = conn.execute(
        """
        SELECT row_label, year, value_numeric FROM annual_metrics m
        JOIN banks b ON b.frn = m.frn
        WHERE b.canonical_name LIKE '%Weatherbys%' AND m.sheet = 'Asset Quality'
          AND row_label LIKE 'Regulatory credit risk exposure%'
          AND row_label NOT LIKE '%Total regulatory%'
          AND value_numeric IS NOT NULL
        ORDER BY year, row_label
        """
    ).fetchall()
    exposure_years = {}
    for lbl, year, val in rows:
        cat = lbl.split(" - ", 1)[1]
        y = year.replace("FY", "")
        exposure_years.setdefault(y, {})[cat] = val
    out["Weatherbys"]["loan_composition"] = {"kind": "exposure_class", "years": exposure_years}
    conn.close()
    return out


HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{title}</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Source+Serif+4:opsz,wght@8..60,500;8..60,600;8..60,700&family=IBM+Plex+Sans:wght@400;500;600&display=swap">
<link rel="stylesheet" href="deliverable_shared.css">
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.4/dist/chart.umd.min.js"></script>
</head>
<body>

<aside class="sidebar">
  <div class="brand">Credit risk<span class="sub">loan concentration &amp; RWA density</span></div>
  <div>
    <div class="nav-label">View</div>
    <div class="nav-pills" id="sidebar-nav"></div>
  </div>
  <div class="bank-search-wrap" id="bank-search-wrap"></div>
  <div class="sidebar-note">Search returns instantly across all 145 banks; the sidebar never grows past this size regardless of how many banks are covered — the full list lives on its own page instead.</div>
  <div class="sidebar-foot">Katalysis · UK bank Pillar 3 deliverable</div>
</aside>

<main>
  <div class="page-head">
    {back_link}
    <h1>{h1}</h1>
    <div class="sub" id="page-sub">{sub_fallback}</div>
  </div>
  <div id="app">{body}</div>
  {todo_note}
</main>
"""

TODO_NOTE = ''


def write_comparison(data, banks_index):
    html = HEAD.format(
        title="Credit risk — comparison",
        back_link="",
        h1="Credit risk",
        sub_fallback="",
        body="",
        todo_note=TODO_NOTE,
    )
    html += f"""
<script id="data" type="application/json">{json.dumps(data)}</script>
<script id="banks-index" type="application/json">{json.dumps(banks_index)}</script>
<script src="deliverable_shared.js"></script>
<script>
const DATA = JSON.parse(document.getElementById('data').textContent);
const BANKS_INDEX = JSON.parse(document.getElementById('banks-index').textContent);
renderSidebar('comparison', BANKS_INDEX);
renderComparisonPage(DATA, Object.keys(DATA));
</script>
</body>
</html>
"""
    (OUT_DIR / "comparison.html").write_text(html)


def write_banks_directory(data, banks_index):
    rows_html = ""
    for b in banks_index:
        bd = data[b["name"]]
        profit_years = sorted(bd.get("profit_for_year", {}).items())
        latest_profit_year, latest_profit = profit_years[-1] if profit_years else (None, None)
        if latest_profit is not None:
            sign = "-" if latest_profit < 0 else ""
            color = "var(--red)" if latest_profit < 0 else "var(--green)"
            profit_cell = f'<span style="color:{color}">{sign}£{abs(round(latest_profit)):,}</span> <span style="color:var(--ink-faint);font-size:11px;">FY{latest_profit_year}</span>'
        else:
            profit_cell = "—"
        comp = bd["loan_composition"]
        basis = {"stage": "IFRS 9 stage", "exposure_class": "exposure class", "none": "not disclosed"}[comp["kind"]]
        years_count = len(comp["years"])
        rows_html += f"""<tr>
      <td><a href="bank-{b['slug']}.html">{b['name']}</a></td>
      <td class="num">{profit_cell}</td>
      <td><span class="basis-tag">{basis}</span></td>
      <td class="num">{years_count}</td>
      <td><a href="bank-{b['slug']}.html">View profile</a></td>
    </tr>"""

    body = f"""<div class="block" style="margin-top:8px;">
    <div class="card" style="padding:0;">
      <table class="bank-table">
        <thead><tr>
          <th>Bank</th><th>Profit or loss (latest)</th><th>Loan concentration basis</th><th>Years of data</th><th></th>
        </tr></thead>
        <tbody>{rows_html}</tbody>
      </table>
    </div>
  </div>"""

    html = HEAD.format(
        title="Credit risk — banks",
        back_link='<a class="back" href="comparison.html">← Comparison</a>',
        h1="Banks",
        sub_fallback=f"All {len(banks_index)} banks with credit-risk data in this prototype — click through for the full profile. At 145 banks this is the same table, just longer; the sidebar search is the fast path to a specific bank from anywhere.",
        body=body,
        todo_note="",
    )
    html += """
<script src="deliverable_shared.js"></script>
<script id="banks-index" type="application/json">""" + json.dumps(banks_index) + """</script>
<script>
const BANKS_INDEX = JSON.parse(document.getElementById('banks-index').textContent);
renderSidebar('banks', BANKS_INDEX);
</script>
</body>
</html>
"""
    (OUT_DIR / "banks.html").write_text(html)


def write_bank_page(bank_name, bank_data, banks_index):
    slug = slugify(bank_name)
    html = HEAD.format(
        title=f"{bank_name} — credit risk",
        back_link='<a class="back" href="banks.html">← All banks</a>',
        h1=bank_name,
        sub_fallback="",
        body="",
        todo_note=TODO_NOTE,
    )
    html += f"""
<script id="bank-data" type="application/json">{json.dumps(bank_data)}</script>
<script id="banks-index" type="application/json">{json.dumps(banks_index)}</script>
<script src="deliverable_shared.js"></script>
<script>
const BANK_DATA = JSON.parse(document.getElementById('bank-data').textContent);
const BANKS_INDEX = JSON.parse(document.getElementById('banks-index').textContent);
renderSidebar(null, BANKS_INDEX);
renderDrilldownPage({bank_name!r}, BANK_DATA);
</script>
</body>
</html>
"""
    (OUT_DIR / f"bank-{slug}.html").write_text(html)


def write_workbook_viewer(bank_name, bank_data):
    source_workbook = bank_data.get("source_workbook")
    if not source_workbook:
        return
    xlsx_path = ROOT / "banks" / source_workbook
    if not xlsx_path.exists():
        return
    html = render_workbook_viewer(xlsx_path, title=f"{bank_name} — workbook")
    (OUT_DIR / f"workbook-{slugify(bank_name)}.html").write_text(html)


def main():
    global DB_PATH, OUT_DIR
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", default=DB_PATH, help="SQLite source-of-truth database")
    parser.add_argument("--out", default=OUT_DIR, help="output directory for the built site")
    args = parser.parse_args()
    DB_PATH = Path(args.db)
    OUT_DIR = Path(args.out)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    # Pages link to these by bare relative filename (one <link>/<script> tag
    # per page, no bundler), so the built assets need to live in OUT_DIR
    # alongside the generated HTML, not just their scripts/insights/ source.
    shutil.copy(ROOT / "scripts" / "insights" / "deliverable_shared.css", OUT_DIR / "deliverable_shared.css")
    shutil.copy(ROOT / "scripts" / "insights" / "deliverable_shared.js", OUT_DIR / "deliverable_shared.js")
    data = curate()
    banks_index = [{"name": name, "slug": slugify(name)} for name in data]
    write_comparison(data, banks_index)
    write_banks_directory(data, banks_index)
    for name, bank_data in data.items():
        write_bank_page(name, bank_data, banks_index)
        write_workbook_viewer(name, bank_data)
    print(f"Wrote comparison.html, banks.html, {len(data)} bank-<slug>.html, and {len(data)} workbook-<slug>.html pages to {OUT_DIR}")


if __name__ == "__main__":
    main()
