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
every bank's Pillar 3 credit-risk-exposure-by-class breakdown directly from
the database, as a per-bank-page-only substitute for any bank with no IFRS 9
stage split disclosed at all (Weatherbys was the first found, per IN-039's
finding, but this isn't special-cased to Weatherbys - see curate()'s final
loop) - see IN-042's ticket Resolution for why this substitute view was
chosen over dropping such a bank.

Run: python3 scripts/insights/build_deliverable.py
Then open deliverable/comparison.html directly in a browser. Wired into
refresh_all.py's default sequence.
"""

import argparse
import csv
import json
import re
import shutil
import sqlite3
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "deliverable"
DB_PATH = ROOT / "research" / "insights.db"
LOGOS_DIR = ROOT / "scripts" / "insights" / "assets" / "logos"
CLUSTERS_CSV = ROOT / "research" / "bank_clusters.csv"
CLUSTERS_SWEEP_CSV = ROOT / "research" / "bank_clusters_sweep.csv"

sys.path.insert(0, str(ROOT / "scripts" / "insights"))
sys.path.insert(0, str(ROOT / "scripts"))
from bank_workbook import PILLAR3_SHEET_NAMES  # noqa: E402
from in012_absolute_analysis import classify_amount_unit  # noqa: E402
from in040_risk_metrics import build_in040_payload  # noqa: E402
from in041_spend_metrics import (  # noqa: E402
    build_in041_payload, _LOANS_RE, _OF_WHICH_RE, _TREASURY_RE, _TREASURY_EXCLUDE_RE,
    _CASH_RE, _CASH_EXCLUDE_RE,
)
from in024_trajectory import build_in024_payload  # noqa: E402
from in021_headroom_trajectory import build_headroom_payload  # noqa: E402
from in010_parent_groups import build_in010_payload  # noqa: E402
from in009_analysis import CORE_METRICS, detect_outliers  # noqa: E402
from analysis_queries import AnalysisQueries  # noqa: E402
from build_workbook_viewer import render_workbook_viewer  # noqa: E402
from statement_row_selection import in_assets_section, own_label  # noqa: E402

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

# Hand-curated business-model tag for the "how does this bank make money"
# view (business-model.html). No existing data in this repo (Banks List
# 2608.xlsx, bank_parent_groups.md, bank_clusters.csv's k-means clustering -
# which is built purely from Pillar 3 capital/liquidity ratios) hints at
# business model, so this is a manual classification, reviewed by the user
# before being treated as authoritative - expect corrections.
#
# "digital": app-first/branchless neobanks and direct digital lenders with
# no branch network, judged on channel and origin, not size or age.
# "other": banks whose core revenue is fee/markets/wealth-driven rather than
# a classic loan book - private/wealth banks, trading/markets desks, asset
# managers - genuinely a different shape of business, not a compromise
# between the other two. Everything else defaults to "traditional"
# (branch-based retail/commercial banks, and the many specialist, wholesale,
# and foreign-subsidiary lenders whose balance sheet is still fundamentally
# loan-and-interest-driven even without a branch network) - matches this
# project's own observation that the vast majority of the 145 banks here
# are traditional, not that "other" is some large leftover bucket.
_DIGITAL_BANKS = {
    "Monzo", "Starling Bank", "Atom Bank", "Chetwood", "Tandem", "Zopa",
    "Kroo Bank", "GB Bank", "Griffin Bank", "Recognise Bank", "Redwood Bank",
    "Perenna", "Oxbury", "Allica", "Zempler", "Clearbank", "Monument Bank",
    "LHV", "Cynergy Bank", "DF Capital Bank", "Streambank", "This Bank",
    "iFAST Global Bank", "Gatehouse Bank",
}
_OTHER_BUSINESS_MODEL_BANKS = {
    "Rathbones Investment Management", "Schroder", "NatWest Markets",
    "JP Morgan Securities", "Goldman Sachs International Bank",
    "ICBC Standard Bank", "Coutts", "Investec Bank", "Brown Shipley",
    "Arbuthnot Latham", "Weatherbys", "Hampden & Co", "C. Hoare & Co",
}
BANK_TYPE = {
    name: (
        "digital" if name in _DIGITAL_BANKS else
        "other" if name in _OTHER_BUSINESS_MODEL_BANKS else
        "traditional"
    )
    for name in BANKS
}


def slugify(name):
    return re.sub(r"^-+|-+$", "", re.sub(r"[^a-z0-9]+", "-", name.lower()))


def load_logo_registry(path=LOGOS_DIR / "manifest.json"):
    """Load the source-tracked, canonical-slug logo registry.

    A verified entry must point to a local SVG and retain its official-source
    provenance. An unresolved entry has no asset and deliberately renders the
    neutral initials fallback instead of a guessed brand mark.
    """
    registry = json.loads(path.read_text())
    if not isinstance(registry, dict):
        raise ValueError("Logo manifest must be an object keyed by canonical slug")
    for slug, entry in registry.items():
        if slug != slugify(slug) or not isinstance(entry, dict):
            raise ValueError(f"Invalid logo manifest entry: {slug!r}")
        status = entry.get("status")
        asset = entry.get("asset")
        if status not in {"verified", "unresolved"}:
            raise ValueError(f"Logo {slug!r} must have status verified or unresolved")
        if status == "verified":
            required = ("asset", "source_url", "retrieved_on", "source_context", "use_note")
            if any(not entry.get(field) for field in required):
                raise ValueError(f"Verified logo {slug!r} is missing provenance")
            if not isinstance(asset, str) or Path(asset).name != asset or not asset.endswith(".svg"):
                raise ValueError(f"Verified logo {slug!r} must name one local SVG")
            if not (LOGOS_DIR / asset).is_file():
                raise ValueError(f"Verified logo {slug!r} asset is missing: {asset}")
        elif asset is not None:
            raise ValueError(f"Unresolved logo {slug!r} cannot name an asset")
    return registry


LOGO_REGISTRY = load_logo_registry()


def bank_initials(bank_name):
    words = re.findall(r"[A-Za-z0-9]+", bank_name)
    return "".join(word[0].upper() for word in words[:2]) or "?"


def render_bank_heading(bank_name):
    """Render an identity lockup only for banks deliberately in the registry."""
    entry = LOGO_REGISTRY.get(slugify(bank_name))
    if entry is None:
        return bank_name
    monogram = bank_initials(bank_name)
    image = ""
    if entry["status"] == "verified":
        image = (
            f'<img src="assets/logos/{entry["asset"]}" alt="" '
            f'onload="this.previousElementSibling.hidden=true" onerror="this.hidden=true">'
        )
    return (
        f'<span class="bank-identity"><span class="bank-logo" aria-hidden="true">'
        f'<span class="bank-monogram">{monogram}</span>{image}</span><span>{bank_name}</span></span>'
    )


_RATIO_KEYWORDS = ["ratio", "coverage", "share"]
# "of which" used to be a blanket keyword here too, on the theory that a
# stage-loan category retaining that structural IN-039 label prefix was
# always a sub-ratio breakout. But "of which" is also a genuine structural
# prefix that survives on real BALANCE categories (FidBank UK's "...of
# which: Stage 1 and Stage 2 impairment allowance", NatWest Markets' "of
# which: individual"/"of which: collective" provision splits) - this only
# sees category-name text, not the row's own value, so it can't tell those
# apart from a genuinely ratio-valued "of which" category (Morgan Stanley
# Bank International's "...Of which: Stage 1 (IFRS 9...)" with value_raw
# "100%"). loan_concentration_quality() in in040_risk_metrics.py now
# excludes genuine percentage rows (value_raw containing "%") before they
# ever reach this filter, so that distinction is already made upstream on
# the actual value rather than guessed from the label here.
# A bare "/" is otherwise a strong ratio signal ("allowance / gross loans"),
# but this dataset also uses "/" in note references ("Note 11/12") and
# short-form fiscal-year ranges ("FY2024/23", "FY2022/21") - neither is a
# ratio. Left unstripped, that false-positived Bank Sepah International's
# "...by IFRS 9 stage (Note 11/12" and Citibank UK's "Stage split
# (FY2024/23... FY2022/21...) - gross exposure"/"- ECL allowance" categories
# as ratios, dropping their only real Stage 1/2/3 balance data entirely and
# leaving both banks looking like they had none (found via a 2026-09-04
# systematic survey of banks with no detected stage data). Strip digit-to-
# digit slashes (with optional surrounding spaces) before checking for a
# ratio-indicating "/" - a genuine ratio's slash separates two named
# concepts ("Stage 3 gross / Total gross"), never two bare numbers.
_DIGIT_SLASH_RE = re.compile(r"\d\s*/\s*\d")
# A slash inside a parenthetical is often part of an explanatory footnote
# ("IAS 39/UK GAAP total provision") rather than a genuine ratio ("X /
# Y") - Julian Hodge Bank's Stage 1/2/3 impairment-provision category
# carries a disclosure-scope parenthetical explaining when IFRS 9 was
# adopted, and "IAS 39/UK GAAP" inside it tripped the ratio-slash check,
# wrongly dropping a real balance category (found via a 2026-09-07
# systematic audit of the one-off empty-note messages). Strip parenthetical
# content before the slash check; a genuine ratio's defining "X / Y" is
# never itself parenthesised in this dataset.
_PAREN_RE = re.compile(r"\([^)]*\)")


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
    if "%" in name or "/" in _DIGIT_SLASH_RE.sub("", _PAREN_RE.sub("", name)):
        return True
    n = name.lower()
    if not any(k in n for k in _RATIO_KEYWORDS):
        return False
    segments = name.split(" - ")
    if len(segments) > 1 and re.search(r"\band\s+coverage\b", segments[0], re.I):
        tail = " - ".join(segments[1:])
        tn = tail.lower()
        return "%" in tail or "/" in _DIGIT_SLASH_RE.sub("", _PAREN_RE.sub("", tail)) or any(k in tn for k in _RATIO_KEYWORDS)
    return True


def normalize_pnl_year(year):
    # Profit & Loss years carry entity suffixes for Monzo's group restructure
    # ("FY2024 (MBHG)*") that the rest of this prototype's data doesn't - strip
    # down to the bare 4-digit year so it lines up with rwa_to_assets_pct etc.
    m = re.match(r"(\d{4})", year.replace("FY", ""))
    return m.group(1) if m else year.replace("FY", "")


# Genuine phrasing variety found across banks' own P&L labels for what is
# structurally the same net fee/commission line ("Net fee income" - HSBC UK
# Bank; "Net fees and commissions income"; "Net fee & commission income";
# the swing-order "Net fees and commission (expense)/income") or net
# interest line ("Net interest and similar income") - a literal substring
# match on only the single most common phrasing ("net fee and commission
# income") silently dropped these banks' fee/interest data entirely, found
# via a 2026-09-07 user request for a fee-vs-loan-reliance comparison where
# HSBC UK Bank (a MAJOR bank whose data is clearly present, just differently
# worded) was one of 69 banks missing from the result. Deliberately does
# NOT match a blended line that mixes the other side in - "Net fee,
# commission and other operating income" (some banks' FY2015-FY2018 filings
# sum fees into a broader other-income subtotal) or "Net interest and fee
# income" - counting either as a pure fee or pure interest figure would
# misattribute one category's revenue to the other and distort the ratio;
# a bank-year with only a blended disclosure has no clean split available,
# so it's correctly left uncategorized rather than forced.
_NET_FEE_LINE_RE = re.compile(
    r"net\s+fees?\s*(?:(?:and|&)\s*commissions?)?\s*(?:\(expense\)/income|\(income\)/expense|income|expense)\b", re.I
)
_NET_INTEREST_LINE_RE = re.compile(
    r"net\s+interest\s*(?:and\s+similar\s+)?(?:income|expense)\b", re.I
)


def canonical_income_category(item):
    l = item.lower()
    if l.startswith("other"):
        return None
    # A bank whose net fee/interest position is negative for the year
    # discloses its own headline line as "... expense", not "... income"
    # (Atom Bank's "Net fee and commission expense" - it pays out more in
    # card/processing fees than it earns; found via a 2026-09-07 user
    # request for a fee-vs-loan-reliance view, where this line's absence
    # silently dropped Atom Bank - a digital bank whose negative fee
    # contribution is itself a genuine, telling data point, not a gap - from
    # the whole comparison). Same category, just the net-negative case of
    # the same line, matched by the same regex as the income case.
    if _NET_INTEREST_LINE_RE.search(l) and "fee" not in l:
        return "Net interest income"
    if _NET_FEE_LINE_RE.search(l) and "interest" not in l and "other operating" not in l:
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


_TOTAL_ASSETS_RE = re.compile(r"total assets$", re.I)


def curate_total_assets(conn, frn):
    """Total assets per year, scaled to actual GBP (2026-09-05 follow-up:
    a group overview page's balance-sheet contribution chart needs each
    member's own absolute total assets, not just the % ratios curate()
    otherwise carries). Every bank in this project has a Balance Sheet
    sheet with a "Total assets" row (unlike the Pillar 3 sheets, where
    some entities have none at all), but units and basis vary member to
    member - non-GBP units are dropped via scaled(), same convention as
    every other absolute-£ figure in this build."""
    rows = conn.execute(
        "SELECT row_label, year, value_numeric, unit FROM annual_metrics "
        "WHERE frn=? AND sheet='Balance Sheet' AND value_numeric IS NOT NULL",
        (frn,),
    ).fetchall()
    out = {}
    for row_label, year, value, unit in rows:
        item = row_label.split(" - ", 1)[1] if " - " in row_label else row_label
        if not _TOTAL_ASSETS_RE.search(item):
            continue
        amount = scaled(value, unit)
        if amount is None:
            continue
        out[normalize_pnl_year(year)] = amount
    return out


def _latest_of(series):
    """Most recent non-None value in a {year: value} series - shared by
    curate_business_model and curate_investment_composition_records, both of
    which capture the same handful of scatter-view y-axis candidates
    (total_assets, cost_to_income_pct, leverage_ratio_pct, rwa_to_assets_pct)
    each at its OWN latest available year, independent of whichever year the
    page's primary metric lands on."""
    years = sorted((y for y, v in series.items() if v is not None), reverse=True)
    return series[years[0]] if years else None


def _scatter_y_axis_fields(data, conn, label, frn):
    bd = data[label]
    return {
        "total_assets": _latest_of(curate_total_assets(conn, frn)),
        "cost_to_income_pct": _latest_of({y: v.get("cost_to_income_pct") for y, v in bd.get("cost_base", {}).items()}),
        "leverage_ratio_pct": _latest_of(bd.get("leverage", {}).get("leverage_ratio_reported_pct", {})),
        "rwa_to_assets_pct": _latest_of(bd.get("rwa_to_assets_pct", {})),
    }


def curate_business_model(data, conn):
    """"How does this bank make money" view (business-model.html, user
    request 2026-09-07): fee income as a share of total income (fee / (fee
    + net interest), NOT fee per unit of assets - a mix question, not an
    intensity one), latest year with both lines disclosed, tagged with the
    hand-curated BANK_TYPE. Reuses income_breakdown/cost_base/leverage/
    rwa_to_assets_pct already computed in curate() rather than re-deriving
    them, and curate_total_assets() for a size figure - the same
    already-established per-bank fields every other page draws from.

    Requires BOTH legs non-negative, not just a positive total. A "share of
    income" ratio is only bounded in the intuitive [0, 100] range when both
    components are non-negative contributions to income - a bank whose net
    interest position is itself an expense that year (funding cost exceeds
    interest earned) can otherwise produce a nonsense >100% "fee share"
    (fee=122.7m, interest=-77.3m -> 270%) or a negative one (fee=-2m,
    interest=412.5m -> -0.5%), neither of which means what the chart's axis
    label says. Skipping to the next year first (rather than clipping the
    negative leg to zero) prefers a genuinely comparable earlier year over a
    silently distorted one, only falling out of the loop with no result when
    no year has both legs non-negative.

    A handful of y-axis candidates are captured alongside fee_share_pct for
    the scatter variant (total_assets, cost_to_income_pct,
    leverage_ratio_reported_pct, rwa_to_assets_pct) - each taken at its OWN
    latest available year independently, not forced onto fee_share_pct's
    year, since requiring all four to align on one year would silently drop
    banks that report a metric in a different year than their income
    breakdown."""
    records = []
    for label, frn in BANKS.items():
        bd = data[label]
        income_years = sorted(bd.get("income_breakdown", {}), reverse=True)
        fee_share_pct, fee_share_year = None, None
        for y in income_years:
            cats = bd["income_breakdown"][y]
            fee, interest = cats.get("Net fee and commission income"), cats.get("Net interest income")
            if fee is None or interest is None:
                continue
            if fee < 0 or interest < 0:
                continue
            total = fee + interest
            if total <= 0:
                continue
            fee_share_pct, fee_share_year = round(fee / total * 100, 1), y
            break
        if fee_share_pct is None:
            continue

        records.append({
            "bank": label, "frn": frn, "bank_type": BANK_TYPE.get(label, "traditional"),
            "fee_share_pct": fee_share_pct, "fee_share_year": fee_share_year,
            **_scatter_y_axis_fields(data, conn, label, frn),
        })
    return records


# investments.html (user request, 2026-09-07, following business-model.html):
# what kind of investments banks make. A survey of all 164 Balance Sheet
# investment/securities-related row labels across the 145 banks found that
# most DON'T name an asset class (government vs corporate bonds vs
# equities) at all - that level of detail lives in note-level sub-tables
# that weren't transcribed (see CLAUDE.md: hand-transcribed from primary
# sources, no scraper) - so a true asset-class breakdown isn't available
# without a new extraction pass. Two things ARE well-supported by what's
# already extracted, agreed with the user as the two views to build:
#   1. Measurement basis: amortised cost/"hold to collect" vs FVOCI+FVTPL+
#      trading/"mark to market" - a genuinely different but related
#      question (how exposed is this bank's investment book to short-term
#      valuation swings), ~30 banks have at least one leg disclosed.
#   2. Government/sovereign vs other investment securities - a coarser cut
#      at the original asset-class question, only 11 banks disclose an
#      explicit government/treasury/gilt/sovereign line separately from a
#      generic "other" investment-securities line.
# Both exclude: investments in subsidiaries/associates/joint ventures (an
# equity stake in group structure, not a markets portfolio position) and
# repo/securities-financing lines (collateralized funding/lending, not a
# portfolio holding) - confirmed with the user. Investment property is
# DELIBERATELY NOT excluded - IAS 40 "Investment property" is itself the
# accounting term for property held for rental income/capital appreciation
# as distinct from IAS 16 owner-occupied premises (a different line,
# "Property, plant and equipment"/"Premises"), so a bank's own use of that
# exact label is already the verification the user asked for. It simply
# doesn't carry a measurement-basis or government/other split of its own
# (property uses IAS 40's separate cost-model/fair-value-model choice, not
# the amortised-cost/FVOCI/FVTPL scheme for financial instruments), so it
# naturally doesn't appear in either view below rather than needing a
# special-case exclusion.
_INVESTMENT_EXCLUDE_RE = re.compile(
    r"subsidiar|associat|joint venture|participating interest|group (?:entit|undertaking)|"
    r"repurchase agreement|securities (?:borrowed|lent|loaned|financing)|cash collateral on securities|"
    r"loans? and advances|derivative|non.financial|revaluation reserve|fair value reserve|"
    r"\bin issue\b|of which|\btotal\b",
    re.I,
)
_INVESTMENT_SHAPE_RE = re.compile(
    r"investment securit|financial investment|debt securit|financial assets?\b|treasury (?:bill|asset|investment)|"
    r"government (?:bond|securit)|sovereign debt|\bgilt|government and other securit",
    re.I,
)
_AMORTISED_COST_RE = re.compile(r"amortised cost|held.to.maturity", re.I)
_MARK_TO_MARKET_RE = re.compile(
    # fvt?o?ci/fvt?pl covers both the common "FVOCI"/"FVTPL" abbreviations
    # AND the "FVTOCI"/"FVTIS" variant used by a handful of banks (Bank of
    # Beirut UK, Gatehouse Bank, Alpha Bank London, etc - "fair value
    # through other comprehensive income"/"fair value through income
    # statement", the same concepts, different abbreviation convention) -
    # found via Gatehouse's Balance Sheet already having genuine FVTOCI/
    # FVTIS rows that this regex was silently dropping entirely.
    r"fvt?o?ci|fvt?pl|fvtis|fair value through (?:other comprehensive income|profit (?:or|and) loss|income statement)|"
    r"available.for.sale|\btrading\b",
    re.I,
)
_GOVERNMENT_INVESTMENT_RE = re.compile(r"government bond|treasury bill|sovereign debt|\bgilt|government securit", re.I)
# "Government AND OTHER securities" is itself a blended line (some banks'
# own wording) - counting it as pure government would overstate the
# government share, so it's deliberately excluded from BOTH the government
# and the "other" bucket rather than guessed into either.
_GOVERNMENT_BLENDED_RE = re.compile(r"government and other securit", re.I)

# scaled() (used everywhere else in this file) deliberately returns None for
# a non-GBP unit, since an absolute £ figure genuinely can't mix currencies.
# curate_investment_composition only ever computes a WITHIN-BANK % share
# (one bucket's amount / that same bank's total investment-book amount, same
# year, same reporting currency throughout) - the currency itself cancels
# out of that ratio, so requiring GBP here was needlessly excluding every
# USD/EUR-reporting bank (ICBC (London), SMBC, Kuwait Finance House, several
# foreign-parented subsidiaries) even though their composition split is
# perfectly readable in their own currency. Only the scale word (thousand /
# million / unit) matters for summing sibling rows correctly. CAD was added
# after TD Bank Europe (a CAD-reporting subsidiary) was found to have every
# one of its otherwise clean, reconciling investment-securities rows
# silently dropped by classify_amount_unit() never recognizing "CAD'000".
_ANY_CURRENCY_SCALE_MULTIPLIER = {
    "GBP_thousand": 1_000, "GBP_million": 1_000_000, "GBP_unit": 1,
    "USD_thousand": 1_000, "USD_million": 1_000_000, "USD_unit": 1,
    "EUR_thousand": 1_000, "EUR_million": 1_000_000, "EUR_unit": 1,
    "CAD_thousand": 1_000, "CAD_million": 1_000_000, "CAD_unit": 1,
}


def _scaled_for_ratio(value, unit):
    mult = _ANY_CURRENCY_SCALE_MULTIPLIER.get(classify_amount_unit(unit or ""))
    return None if mult is None else value * mult


def curate_investment_composition(conn, frn):
    """Two investment-book composition breakdowns for one bank, latest year
    each has usable data: measurement basis (amortised cost vs mark to
    market) and government vs other investment securities. Sums ALL
    matching sibling rows per (year, bucket) rather than picking one best
    row - unlike select_labeled_rows's single-winner selection, several
    banks genuinely disclose multiple FVOCI/FVTPL sub-lines in the same
    year (e.g. Santander UK's "Other financial assets at FVTPL" alongside
    "Financial assets at FVOCI") that would be silently undercounted by a
    single pick."""
    rows = conn.execute(
        "SELECT row_label, year, value_numeric, unit FROM annual_metrics "
        "WHERE frn=? AND sheet='Balance Sheet' AND value_numeric IS NOT NULL",
        (frn,),
    ).fetchall()

    basis_by_year = defaultdict(lambda: {"amortised_cost": 0.0, "mark_to_market": 0.0})
    govt_by_year = defaultdict(lambda: {"government": 0.0, "other": 0.0})
    for row_label, year, value, unit in rows:
        if not in_assets_section(row_label):
            continue
        item = own_label(row_label)
        if _INVESTMENT_EXCLUDE_RE.search(item) or not _INVESTMENT_SHAPE_RE.search(item):
            continue
        amount = _scaled_for_ratio(value, unit)
        if amount is None or amount < 0:
            continue
        y = normalize_pnl_year(year)
        if _AMORTISED_COST_RE.search(item):
            basis_by_year[y]["amortised_cost"] += amount
        elif _MARK_TO_MARKET_RE.search(item):
            basis_by_year[y]["mark_to_market"] += amount
        if _GOVERNMENT_BLENDED_RE.search(item):
            continue
        if _GOVERNMENT_INVESTMENT_RE.search(item):
            govt_by_year[y]["government"] += amount
        else:
            govt_by_year[y]["other"] += amount

    def _latest_composition(by_year, require_positive_keys=()):
        # require_positive_keys guards against a false "split": e.g. every
        # bank without an explicit government/sovereign line falls entirely
        # into "other" once matched at all, which isn't a disclosed split -
        # it's the absence of one, so government_vs_other only counts as
        # data when the government leg is actually non-zero for that year.
        for y in sorted(by_year, reverse=True):
            legs = by_year[y]
            total = sum(legs.values())
            if total > 0 and all(legs[k] > 0 for k in require_positive_keys):
                return {"year": y, **{k: round(v / total * 100, 1) for k, v in legs.items()}}
        return None

    return {
        "measurement_basis": _latest_composition(basis_by_year),
        "government_vs_other": _latest_composition(govt_by_year, require_positive_keys=("government",)),
    }


def curate_investment_composition_records(data, conn):
    """records list for investments.html, one entry per bank that has usable
    data in EITHER composition view - a bank with only a government/other
    split and no measurement-basis split (or vice versa) still gets a
    record, since the two views are rendered as independent charts each
    filtering to banks with data for that view specifically. Also carries
    the same scatter y-axis candidates as curate_business_model, for the
    scatter view alongside the primary 100%-stacked bar."""
    records = []
    for label, frn in BANKS.items():
        comp = curate_investment_composition(conn, frn)
        if comp["measurement_basis"] is None and comp["government_vs_other"] is None:
            continue
        records.append({
            "bank": label, "frn": frn, "bank_type": BANK_TYPE.get(label, "traditional"),
            **comp, **_scatter_y_axis_fields(data, conn, label, frn),
        })
    return records


def curate_asset_composition_absolute(conn, frn):
    """Loans / treasury investments / cash, in £, alongside Total assets -
    the SAME categories and label-matching regexes as in041_spend_metrics's
    capital_deployment() (imported, not re-derived, so this can't silently
    drift from the % figures curate() already carries per bank), but kept
    as an absolute amount rather than only a %. Needed for the 2026-09-05
    follow-up ("for the entire parent, how much of its assets are customer
    loans") - %'s can't be summed across members into one parent-group
    figure, but £ amounts can, so this is what group_asset_composition
    below is built from."""
    rows = conn.execute(
        "SELECT row_label, year, value_numeric, unit FROM annual_metrics "
        "WHERE frn=? AND sheet='Balance Sheet' AND value_numeric IS NOT NULL",
        (frn,),
    ).fetchall()
    totals, cats = {}, {}
    for row_label, year, value, unit in rows:
        if not row_label.startswith("Assets - "):
            continue
        item = row_label.split(" - ", 1)[1]
        amount = scaled(value, unit)
        if amount is None:
            continue
        y = normalize_pnl_year(year)
        if _TOTAL_ASSETS_RE.search(item):
            totals[y] = amount
        elif _OF_WHICH_RE.search(item):
            continue
        elif _LOANS_RE.search(item):
            cats.setdefault(y, {})["loans"] = amount
        elif _TREASURY_RE.search(item) and not _TREASURY_EXCLUDE_RE.search(item):
            cats.setdefault(y, {})["treasury"] = amount
        elif _CASH_RE.search(item) and not _CASH_EXCLUDE_RE.search(item):
            cats.setdefault(y, {})["cash"] = amount
    out = {}
    for y, total in totals.items():
        if not total:
            continue
        c = cats.get(y, {})
        out[y] = {"total": total, "loans": c.get("loans", 0), "treasury": c.get("treasury", 0), "cash": c.get("cash", 0)}
    return out


_TOTAL_LIABILITIES_RE = re.compile(r"total liabilities$", re.I)
# Balance Sheet liability labels are as heterogeneous as everywhere else in
# this hand-transcribed dataset - "Customer deposits" vs "Customer accounts"
# vs "Deposits by customers" vs "Client accounts" for the exact same concept
# across the 17 group-member banks this was built against (2026-09-05
# follow-up: "show what those assets are... as well as liabilities").
# Deliberately coarse (3 named buckets + a remainder), same spirit as
# capital_deployment's cash/loans/treasury/other - a finer split would need
# per-bank label review this feature doesn't warrant.
_CUSTOMER_DEPOSITS_RE = re.compile(r"customer (deposit|account)|deposits? by customer|client account", re.I)
_BANK_DEPOSITS_RE = re.compile(r"bank deposit|deposits? (by|from) bank|due to bank|deposits from .*undertaking", re.I)
_WHOLESALE_FUNDING_RE = re.compile(r"debt securities in issue|debt in issuance|notes in circulation|long.?term debt|subordinated", re.I)


def curate_liability_composition(conn, frn):
    """Total liabilities split into customer deposits / bank deposits /
    wholesale funding (debt securities in issue + subordinated liabilities)
    / other, as a % of total liabilities per year - the liabilities-side
    counterpart to capital_deployment's asset mix, built fresh here since
    curate() never needed a liability breakdown before this."""
    rows = conn.execute(
        "SELECT row_label, year, value_numeric, unit FROM annual_metrics "
        "WHERE frn=? AND sheet='Balance Sheet' AND value_numeric IS NOT NULL",
        (frn,),
    ).fetchall()
    totals, by_year = {}, {}
    for row_label, year, value, unit in rows:
        item = row_label.split(" - ", 1)[1] if " - " in row_label else row_label
        amount = scaled(value, unit)
        if amount is None:
            continue
        y = normalize_pnl_year(year)
        if _TOTAL_LIABILITIES_RE.search(item):
            totals[y] = amount
            continue
        if _CUSTOMER_DEPOSITS_RE.search(item):
            cat = "customer_deposits"
        elif _BANK_DEPOSITS_RE.search(item):
            cat = "bank_deposits"
        elif _WHOLESALE_FUNDING_RE.search(item):
            cat = "wholesale_funding"
        else:
            continue
        year_cats = by_year.setdefault(y, {})
        year_cats[cat] = year_cats.get(cat, 0) + amount
    out = {}
    for y, total in totals.items():
        if not total:
            continue
        cats = by_year.get(y, {})
        known = sum(cats.values())
        other = max(0, total - known)
        out[y] = {
            "customer_deposits_pct": round(cats.get("customer_deposits", 0) / total * 100, 2),
            "bank_deposits_pct": round(cats.get("bank_deposits", 0) / total * 100, 2),
            "wholesale_funding_pct": round(cats.get("wholesale_funding", 0) / total * 100, 2),
            "other_pct": round(other / total * 100, 2),
            # Raw £ alongside the %'s (2026-09-05 follow-up: a parent-group
            # composition sums amounts across members, which a % can't do).
            "total": total, "customer_deposits": cats.get("customer_deposits", 0),
            "bank_deposits": cats.get("bank_deposits", 0), "wholesale_funding": cats.get("wholesale_funding", 0),
            "other": other,
        }
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


EQUITY_BALANCE_ROW_RE = re.compile(r"\bbalance\b", re.I)

# Component names that mean "the grand total of equity for this row" across
# the 145 banks' own freeform column headers (verified against every
# distinct component in `equity_changes` - 0 banks fall outside this list).
# Deliberately an explicit safelist, not a generic "total ..." regex: several
# real column headers ("Total retained earnings", "Total share capital",
# "Total comprehensive income") say "total" but name a sub-item, not the
# grand total, and a loose regex would silently misclassify those as the
# whole-equity figure.
_GRAND_TOTAL_COMPONENTS = {
    "total", "total equity", "total attributable to owners",
    "total attributable to shareholders", "total shareholder funds",
    "total shareholder's equity", "total shareholder's funds",
    "total shareholders' equity", "total shareholders' funds",
    "parent company shareholders' equity", "shareholder's equity excl. nci",
}


def _normalize_component(name):
    return re.sub(r"\s+", " ", name.replace("’", "'").strip().lower())


def _is_grand_total_component(name):
    return _normalize_component(name) in _GRAND_TOTAL_COMPONENTS


# Movement-row bucketing for the equity waterfall. Order matters - each
# label is tested top-to-bottom and the first match wins, since some
# patterns are traps for each other (e.g. "Total comprehensive income for
# the year" must not fall through to the generic profit/loss bucket).
_EQUITY_BUCKET_PATTERNS = [
    ("total_comprehensive", re.compile(r"total comprehensive", re.I)),
    ("prior_year_adjustment", re.compile(r"prior year adjustment|\brestat", re.I)),
    ("dividend", re.compile(r"dividend", re.I)),
    ("share_based_payments", re.compile(r"share.based payment", re.I)),
    ("share_capital", re.compile(
        r"shares? (issu|option|warrant)|issu(e|ance) of share|proceeds from (issue of )?shares?|"
        r"share capital|new shares issued|bonus share|exercise of option|cost of issuance|"
        r"share issue costs", re.I)),
    ("oci", re.compile(
        r"other comprehensive|\btranslation\b|actuarial|revaluation|\bhedg|fvoci|"
        r"available.for.sale|afs reserve|fair value (movement|reserve)", re.I)),
    ("profit_loss", re.compile(r"\b(profit|loss)\b", re.I)),
]
_EQUITY_BUCKET_LABEL = {
    "total_comprehensive": "Profit & other comprehensive income",
    "profit_loss": "Profit/(loss) for the year",
    "oci": "Other comprehensive income/(loss)",
    "dividend": "Dividends",
    "share_capital": "Share capital movements",
    "share_based_payments": "Share-based payments",
    "prior_year_adjustment": "Prior year adjustments",
    "other": "Other movements",
}
_EQUITY_BUCKET_ORDER = [
    "total_comprehensive", "profit_loss", "oci", "dividend", "share_capital",
    "share_based_payments", "prior_year_adjustment", "other",
]


def _bucket_equity_movement(label):
    for bucket, pattern in _EQUITY_BUCKET_PATTERNS:
        if pattern.search(label):
            return bucket
    return "other"


def _extract_year(label):
    years = re.findall(r"(19\d{2}|20\d{2})", label)
    return years[-1] if years else None


_FY_TAG_RE = re.compile(r"\(FY(\d{4})[,)]")


def _extract_fy_tag_year(label):
    """A movement row's OWN fiscal year, from the standard "(FYNNNN)" or
    "(FYNNNN, ...)" tagging convention used throughout these rows (e.g.
    "Profit for the year (FY2013)", or Credit Suisse UK's own "Total
    comprehensive income for the year (FY2019, as originally reported)") -
    stricter than `_extract_year`'s bare "any 4-digit number in the label"
    search, and deliberately requiring "FYNNNN" to be followed by "," or
    ")" (not any word boundary): Bank of Africa UK's own "Impact of
    correction of errors (FY2018 Annual Report restatement)" names the
    filing the correction was DISCLOSED in, not the fiscal year the
    correction itself belongs to - a looser `\\b` boundary wrongly tagged
    it as a "FY2018" movement and collided with the real FY2018 segment.
    Restatement/
    reclassification bridge rows (e.g. "Reclassification (per FY2014
    accounts' own FY2013 restated comparative - see FY2013 RESTATEMENT
    NOTE)") mention several years in free prose WITHOUT "FY" starting the
    parenthetical, so they still correctly don't match; `_extract_year` on
    them picks up whichever year happens to be the LAST 4-digit match,
    which is not necessarily the segment's real year and previously
    collided with a genuinely different same-year segment (verified
    against Union Bancaire Privee UK's FY2013->FY2014 and FY2014->FY2015
    restatement bridges, and separately against Credit Suisse UK's own
    FY2019/FY2020 qualifier-tagged rows)."""
    m = _FY_TAG_RE.search(label)
    return m.group(1) if m else None


_MONTH_YEAR_RE = re.compile(
    r"\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+(\d{4})\b", re.I
)


def _extract_month_year(label):
    """A checkpoint's own "Mon YYYY" (e.g. "At 28 February 1998" ->
    "Feb 1998") - used to disambiguate archival, pre-cutoff segments that
    land in the same calendar year (e.g. Union Bancaire Privee UK's own
    28 Feb 1998 and 31 Dec 1998 balance dates) without resorting to a bare
    "(i)"/"(ii)" suffix."""
    m = _MONTH_YEAR_RE.search(label)
    return f"{m.group(1)[:3].capitalize()} {m.group(2)}" if m else None


_PAREN_RE = re.compile(r"\([^)]*\)")
_CHECKPOINT_RE = re.compile(
    r"^(unaudited |restated |audited )*((opening|closing) )?balance\b|^at\s+\d|^as\s+at\s+\d|^total$",
    re.I,
)


def _is_balance_checkpoint(label):
    """A real point-in-time balance row (segment boundary for the
    waterfall/mix-by-year), not just any row that happens to mention
    "balance" in passing. `EQUITY_BALANCE_ROW_RE` (bare \\bbalance\\b) is
    right for the table's cosmetic bold-row styling but wrong here: real
    movement rows sometimes reference "balance" inside a parenthetical
    aside ("IFRS 17 transition restatement (change in opening balance, see
    source note)"), which `\\bbalance\\b` alone would misread as a
    checkpoint and silently corrupt the segment split. Stripping
    parentheticals first and requiring "balance"/"at <year>" to be the
    label's own leading subject filters those out."""
    stripped = _PAREN_RE.sub("", label).strip()
    return bool(_CHECKPOINT_RE.search(stripped))


def curate_equity_waterfall(rows_by_order, components):
    """Per-fiscal-year waterfall bars (opening balance -> movements ->
    closing balance) derived from the same chronological roll-forward the
    table view uses. Segments are the spans between consecutive "balance"
    rows.

    Real filings sometimes disclose a same-year subtotal line - not just
    "Total comprehensive income/(loss) for the year" (profit + OCI) but
    also bespoke ones like "Total contributions by and distributions to
    owners" (capital contributions + an asset-disposal reclass + dividends,
    all in one row, verified against Arbuthnot Latham's real 2021 data) -
    that re-states the sum of several immediately preceding leaf rows.
    Bucketing every row independently double-counts those: the subtotal
    AND its constituents both land in the total. Rather than hardcode every
    subtotal phrasing, a wrapper row is detected structurally: its own
    value exactly matches the running sum of the pending (not yet
    absorbed) leaf rows since the last checkpoint or wrapper, in which case
    those leaves are replaced by one bar carrying the wrapper row's own
    label/bucket. This makes opening + sum(bars) == closing exact by
    construction for the common cases, self-verified per segment rather
    than assumed - see the balance-check note in `curate_equity_changes`'s
    caller for how residual mismatches (nested/partial subtotals a flat
    single-pass can't unwind) are surfaced rather than silently swallowed.
    """
    grand_total_component = next(
        (c for c in components if _is_grand_total_component(c)), None
    )
    if grand_total_component is None:
        return []

    order_keys = sorted(rows_by_order)
    balance_positions = [
        i for i, k in enumerate(order_keys)
        if _is_balance_checkpoint(rows_by_order[k]["label"])
        and rows_by_order[k]["values"].get(grand_total_component) not in (None, "")
    ]

    # Pass 1: one raw (opening, closing, movement_keys) pair per adjacent
    # checkpoint, plus whichever "(FYNNNN)" tag its own movement rows carry
    # (see `_extract_fy_tag_year`) - before any merging.
    raw_pairs = []
    for seg_i in range(len(balance_positions) - 1):
        start_pos = balance_positions[seg_i]
        end_pos = balance_positions[seg_i + 1]
        opening_key = order_keys[start_pos]
        closing_key = order_keys[end_pos]
        movement_keys = order_keys[start_pos + 1:end_pos]
        tag_year = None
        for k in movement_keys:
            tag_year = _extract_fy_tag_year(rows_by_order[k]["label"])
            if tag_year:
                break
        raw_pairs.append({
            "opening_key": opening_key, "closing_key": closing_key,
            "movement_keys": movement_keys, "tag_year": tag_year,
        })

    # Pass 2: merge untagged pairs so every emitted row is either a real,
    # uniquely-labelled fiscal year or one honest multi-year "no data"
    # range - never a same-year duplicate or an odd non-year label
    # (verified against Union Bancaire Privee UK and Aldermore Bank, both
    # of whose roll-forwards mix genuine multi-year gaps with short,
    # same/adjacent-year untagged pairs). An untagged pair - whether it's a
    # pure balance-to-balance gap with no disclosed detail at all, or a
    # bridging row like "Reclassification (per FY2014 accounts' own
    # FY2013 restated comparative...)" or Aldermore's "As at 1 January
    # 2014" GAAP-transition balance - is chained together with any
    # adjacent untagged pairs (`carry`). At the next real tagged fiscal
    # year (or the end of the roll-forward), that accumulated run either:
    #  - spans more than one calendar year (its own opening's year to its
    #    own closing's year): a genuine multi-year undisclosed gap (e.g.
    #    Union Bancaire Privee UK's 1997-2012 span, or a stub-period chain
    #    that adds up to one) - kept as its own row, named the range it
    #    covers, never folded into a real year's numbers; or
    #  - spans one calendar year or less: too short to be its own honest
    #    row and would only collide with (or misname) the fiscal year
    #    right next to it - folded forward into that year's own bars
    #    instead (its balance delta, if any, surfaces there as a
    #    "Reconciling difference" bar rather than a same-year duplicate
    #    row).
    # A carry that DOES clear the >1-year bar is emitted as one row PER
    # checkpoint pair, not one row for the whole run: the "full available
    # history" toggle on the per-bank page (mirroring the same toggle on
    # the capital-deployment/income-mix charts) is only useful if the
    # archival years are actually there to reveal - bundling e.g. Union
    # Bancaire Privee UK's four 1997-2012 checkpoints into a single
    # "1997-2012" bar would leave nothing for it to show.
    groups = []
    carry = []

    def carry_span_years():
        if not carry:
            return None
        opening_year = _extract_year(rows_by_order[carry[0]["opening_key"]]["label"])
        closing_year = _extract_year(rows_by_order[carry[-1]["closing_key"]]["label"])
        if opening_year and closing_year:
            return int(closing_year) - int(opening_year)
        return None

    for pair in raw_pairs:
        if pair["tag_year"]:
            span = carry_span_years()
            if span is not None and span > 1:
                for p in carry:
                    groups.append(("gap", [p]))
                carry = []
            groups.append(("tagged", carry + [pair]))
            carry = []
        else:
            carry.append(pair)
    if carry:
        # A TRAILING untagged run (nothing left after it to merge forward
        # into) needs the same "too short to be its own row" treatment,
        # just folded backward instead - found via Monzo's real FY2020
        # "Prior year adjustments" checkpoint (Retained losses/Other
        # reserves reclass, Total equity net-zero), which sits AFTER its
        # own fiscal year's tagged movement row with nothing tagged
        # following it, so the forward-merge branch above never sees it and
        # it fell straight through to a standalone (near-empty) "gap"
        # segment - the same spurious-segment shape the fold-forward branch
        # already prevents in the mirror-image case.
        span = carry_span_years()
        if span is not None and span <= 1 and groups and groups[-1][0] == "tagged":
            kind, group = groups[-1]
            groups[-1] = (kind, group + carry)
        else:
            for p in carry:
                groups.append(("gap", [p]))

    segments = []
    for kind, group in groups:
        opening_key = group[0]["opening_key"]
        closing_key = group[-1]["closing_key"]
        try:
            opening = float(str(rows_by_order[opening_key]["values"][grand_total_component]).replace(",", ""))
            closing = float(str(rows_by_order[closing_key]["values"][grand_total_component]).replace(",", ""))
        except (TypeError, ValueError):
            continue

        movement_keys = [k for pair in group for k in pair["movement_keys"]]
        emitted = []  # [(bucket, value)] in emission order, subtotal-collapsed
        pending = []  # [(bucket, value)] leaf rows not yet absorbed by a subtotal
        running_base = opening  # opening + every already-emitted bar's value
        for k in movement_keys:
            row = rows_by_order[k]
            raw = row["values"].get(grand_total_component)
            if raw in (None, ""):
                continue
            try:
                value = float(str(raw).replace(",", ""))
            except (TypeError, ValueError):
                continue
            pending_sum = sum(v for _, v in pending)
            if abs(running_base + pending_sum - value) <= 1.0:
                # An absolute mid-year checkpoint disguised as a movement row
                # (e.g. Gatehouse Bank's "Subtotal after other comprehensive
                # income (FY2021)": restates opening + leaves-so-far as one
                # running total, not a new delta). Its pending leaves are
                # real movements and are kept; the checkpoint row itself
                # carries no new information, so it's dropped rather than
                # emitted as a bar.
                emitted.extend(pending)
                running_base += pending_sum
                pending = []
                continue
            bucket = _bucket_equity_movement(row["label"])
            if pending and abs(pending_sum - value) <= 1.0:
                emitted.append((bucket, value))  # wrapper row replaces its leaves
                running_base += value
                pending = []
            else:
                pending.append((bucket, value))
        emitted.extend(pending)

        bucket_totals = defaultdict(float)
        for bucket, value in emitted:
            bucket_totals[bucket] += value
        bars = [
            {"bucket": b, "label": _EQUITY_BUCKET_LABEL[b], "value": bucket_totals[b]}
            for b in _EQUITY_BUCKET_ORDER if bucket_totals[b] != 0
        ]
        # A handful of banks' own source filings have a real gap between one
        # year's closing balance and the next year's opening balance with no
        # movement row explaining it (verified against ClearBank's FY2023/
        # FY2024 figures - a genuine transcription/source-document gap, not
        # a bucketing bug: row order jumps straight from one balance to the
        # next). Rather than silently drop the gap (a waterfall that doesn't
        # foot) or chase every such per-bank quirk, name it honestly.
        gap = closing - (opening + sum(b["value"] for b in bars))
        if abs(gap) > 1.0:
            bars.append({"bucket": "reconciling", "label": "Reconciling difference (source data gap)", "value": gap})

        tag_year = next((p["tag_year"] for p in group if p["tag_year"]), None)
        opening_year = _extract_year(rows_by_order[opening_key]["label"])
        closing_year = _extract_year(rows_by_order[closing_key]["label"])
        if tag_year:
            # A real, disclosed fiscal year - use its own "(FYNNNN)" tag
            # rather than either checkpoint's calendar label, which several
            # banks (verified against Union Bancaire Privee UK) print as the
            # FOLLOWING year's "At 1 January <year+1>" opening balance
            # rather than a same-year "At 31 December <year>" closing row.
            year = tag_year
        elif opening_year and closing_year and int(closing_year) - int(opening_year) > 1:
            # A single checkpoint pair spanning more than one calendar year
            # with no interior movement rows at all (e.g. Union Bancaire
            # Privee UK's own 1999->2013 pair) - name it as the range it
            # actually covers.
            year = f"{opening_year}–{int(closing_year) - 1}"
        else:
            year = closing_year or opening_year or None
        end_year = int(tag_year or closing_year or opening_year) if (tag_year or closing_year or opening_year) else None
        # `start_year` matters separately from `end_year` for the "full
        # available history" toggle: a multi-year range segment's CLOSING
        # edge can be recent even though it covers mostly archival years
        # (Union Bancaire Privee UK's own "1999-2012" gap closes right at
        # 2013) - filtering the default view by `start_year` keeps that
        # kind of segment out of the recent view too, not just its
        # standalone archival siblings.
        start_year = int(tag_year or opening_year or closing_year) if (tag_year or opening_year or closing_year) else None
        segments.append({
            "year": year, "start_year": start_year, "end_year": end_year, "opening": opening, "closing": closing,
            "bars": bars, "_kind": kind, "_opening_key": opening_key, "_closing_key": closing_key,
        })

    # Archival "gap" segments (checkpoints with no disclosed movement detail
    # at all - see the "one row PER checkpoint pair" note above) can land on
    # the same bare year as a sibling gap segment (verified against Union
    # Bancaire Privee UK's own 28 Feb 1998 and 31 Dec 1998 balance dates,
    # both "1998"). Real fiscal-year segments are already guaranteed unique
    # by their own "(FYNNNN)" tag, so only gap segments need this pass:
    # first try each one's own precise "Mon YYYY" checkpoint date, and fall
    # back to a bare "(i)"/"(ii)" suffix only if that still collides.
    gap_year_counts = defaultdict(int)
    for seg in segments:
        if seg["_kind"] == "gap" and seg["year"]:
            gap_year_counts[seg["year"]] += 1
    if any(c > 1 for c in gap_year_counts.values()):
        for seg in segments:
            if seg["_kind"] == "gap" and seg["year"] and gap_year_counts[seg["year"]] > 1:
                month_year = _extract_month_year(rows_by_order[seg["_closing_key"]]["label"])
                if month_year:
                    seg["year"] = month_year

    # Final safety net: whatever the cause (two same-year "(FYNNNN)" tagged
    # segments from a restated/"as originally reported" pair of movements,
    # or a gap segment the month-date upgrade above couldn't disambiguate),
    # NO segment should ever reach the chart with a label some other
    # segment already has - fall back to a bare "(i)"/"(ii)" suffix, in
    # chronological order, for any label still shared by more than one
    # segment at this point.
    label_counts = defaultdict(int)
    for seg in segments:
        if seg["year"]:
            label_counts[seg["year"]] += 1
    label_seen = defaultdict(int)
    for seg in segments:
        if seg["year"] and label_counts[seg["year"]] > 1:
            label_seen[seg["year"]] += 1
            seg["year"] = f"{seg['year']} ({'i' * label_seen[seg['year']]})"

    for i, seg in enumerate(segments):
        if not seg["year"]:
            seg["year"] = f"Segment {i + 1}"
        del seg["_kind"], seg["_opening_key"], seg["_closing_key"]
    return segments


def curate_equity_mix_by_year(rows_by_order, components):
    """One equity-composition snapshot per fiscal year (all components
    except the grand total), taken from each year's closing "balance" row -
    when a year has more than one (an originally-reported balance later
    corrected by a restated balance), the last one in row order wins, since
    corrections are transcribed immediately after what they correct.
    Excludes every component recognized as a grand total, not just the one
    `curate_equity_waterfall` picks - some banks (HSBC Bank Plc verified)
    disclose two ("Total shareholders' equity" excl. NCI and "Total equity"
    incl. NCI); leaving the unpicked one in would double-count as a phantom
    stacked-bar segment on top of the real components, which already sum to
    the total on their own."""
    grand_total_components = {c for c in components if _is_grand_total_component(c)}
    mix_by_year = {}
    for k in sorted(rows_by_order):
        row = rows_by_order[k]
        if not _is_balance_checkpoint(row["label"]):
            continue
        year = _extract_year(row["label"])
        if not year:
            continue
        snapshot = {}
        for c in components:
            if c in grand_total_components:
                continue
            raw = row["values"].get(c)
            if raw in (None, ""):
                continue
            try:
                snapshot[c] = float(str(raw).replace(",", ""))
            except (TypeError, ValueError):
                continue
        if snapshot:
            mix_by_year[year] = snapshot
    return mix_by_year


def curate_equity_changes(conn, frn):
    """Statement of Changes in Equity, straight off the `equity_changes`
    table - a chronological roll-forward (movement rows x equity-component
    columns), not the year-column shape every other sheet here uses, so it's
    pivoted into {components: [...], rows: [{label, values: {component: raw}}]}
    for the plain table render, plus a derived `waterfall` (IN-044) and
    `mix_by_year` (IN-044) for the two chart views. Component order follows
    first-seen order across `row_order` (the sheet's own oldest-to-newest
    read order), matching how the column appears in the source workbook -
    never re-sorted alphabetically."""
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
    return {
        "components": components,
        "rows": ordered_rows,
        "waterfall": curate_equity_waterfall(by_order, components),
        "mix_by_year": curate_equity_mix_by_year(by_order, components),
    }


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


def curate_comparison_trends():
    """IN-052: the two old-dashboard sections with no equivalent anywhere in
    `deliverable/` (no page there has a time dimension at all) - persistent
    trajectories/rank mobility and regulatory headroom trajectory - migrated
    onto comparison.html only (not every per-bank page, unlike curate()'s
    payload), since both are inherently cross-bank comparisons. Condensed
    from in024/in021's full payloads (which carry per-change-pair scoring,
    reporting-basis notes, and rank-mobility panels not needed to draw a
    chart or table) - the full in024 payload alone is ~1.25MB of JSON;
    trimmed to just what the client-side chart/table need."""
    # Trimmed to FY2021-FY2025 - the full payload spans FY2020-FY2026, but
    # FY2020 and FY2026 are each only sparsely disclosed (a handful of
    # banks), so showing them stretched every chart's x-axis wider than the
    # RWA density chart right next to it for little real data (per user
    # request, 2026-09-05).
    TRAJECTORY_YEARS = list(range(2021, 2026))
    raw24 = build_in024_payload(DB_PATH)
    trajectories = {"years": TRAJECTORY_YEARS, "minimum_changes": raw24["metadata"]["minimum_changes"], "metrics": {}}
    for metric, records in raw24["trajectories"].items():
        trajectories["metrics"][metric] = [
            {"frn": r["frn"], "bank": r["bank"],
             "points": [{"year": p["year"], "value": p["value"]} for p in r["years"] if p["year"] in TRAJECTORY_YEARS]}
            for r in records if any(p["value"] is not None for p in r["years"] if p["year"] in TRAJECTORY_YEARS)
        ]

    raw21 = build_headroom_payload(DB_PATH)
    headroom = [
        {
            "frn": r["frn"], "bank": r["bank"], "metric": r["metric"], "latest_year": r["latest_year"],
            "current_value": r["current_value"], "regulatory_floor": r["regulatory_floor"],
            "current_headroom": r["current_headroom"], "trend_direction": r["trend_direction"],
            "trend_change": r["trend_change"], "status": r["status"],
        }
        for r in raw21["records"]
    ]
    return {"trajectories": trajectories, "headroom": headroom}


def curate_comparison_efficiency(data):
    """IN-045: cost-to-income and profit/(loss) both broadly improved
    through FY2023, then reversed - reuses `data`'s already-curated
    cost_base (IN-041) and income_volatility (IN-040) rather than
    re-deriving either. Vetted the same way as the pre-existing 4 findings
    in `Cross-Bank Trends Analysis.md`: an exact down/up count per window,
    not an estimate - see that file's own new entry for the coverage
    caveats (both series are a real-but-partial minority of the 145 banks,
    comparable to the existing LCR finding's n=73)."""
    windows = [("2021", "2022"), ("2022", "2023"), ("2023", "2024"), ("2024", "2025")]
    cost_series = {label: entry["cost_base"] for label, entry in data.items() if entry.get("cost_base")}
    profit_yoy = {
        label: {str(y): v for y, v in entry["income_volatility"]["yoy_change_pct"].items()}
        for label, entry in data.items() if entry.get("income_volatility", {}).get("yoy_change_pct")
    }

    def counts(y1, y2, series_map, get_value):
        down = up = 0
        for s in series_map.values():
            v1, v2 = get_value(s, y1), get_value(s, y2)
            if v1 is None or v2 is None:
                continue
            if v2 < v1:
                down += 1
            elif v2 > v1:
                up += 1
        return down, up

    cost_to_income_pct_worsening = []
    profit_pct_declining = []
    n_cost, n_profit = [], []
    for y1, y2 in windows:
        d, u = counts(y1, y2, cost_series, lambda s, y: s.get(y, {}).get("cost_to_income_pct"))
        n_cost.append(d + u)
        cost_to_income_pct_worsening.append(round(u / (d + u) * 100, 1) if (d + u) else None)
        # profit_yoy is keyed by the LATER year of the pair already (IN-040's
        # own convention: yoy_change_pct["2022"] is the FY2021->FY2022 move)
        d2 = sum(1 for s in profit_yoy.values() if s.get(y2) is not None and s[y2] < 0)
        u2 = sum(1 for s in profit_yoy.values() if s.get(y2) is not None and s[y2] >= 0)
        n_profit.append(d2 + u2)
        profit_pct_declining.append(round(d2 / (d2 + u2) * 100, 1) if (d2 + u2) else None)

    return {
        "windows": [f"FY{y1}→FY{y2}" for y1, y2 in windows],
        "cost_to_income_pct_worsening": cost_to_income_pct_worsening,
        "profit_pct_declining": profit_pct_declining,
        "n_cost": n_cost,
        "n_profit": n_profit,
    }


def curate_comparison_bubbles(data, parent_groups):
    """Three Gapminder-style bubble charts (user request, 2026-09-05): the
    first pairing (RWA density vs. CET1 Ratio) was grilled and picked by
    the user over two alternatives; the user then asked for the other two
    to be added as well, so all three ship together. All three share the
    same bubble size (Total assets - balance-sheet scale, the conventional
    bank-size proxy, near-universal coverage per curate_total_assets's own
    docstring - rather than revenue, closer to Gapminder's own "population"
    size role than a P&L figure) and the same color convention (parent
    group where the bank is one of >=2 comparable members per
    curate_comparison_parent_groups, standalone banks neutral):
      - risk_vs_capital: RWA density (X) vs. CET1 Ratio (Y) - the
        project's own "risk-taking" lens.
      - efficiency_vs_capital: Cost-to-income ratio (X) vs. CET1 Ratio (Y)
        - "efficiency vs. strength".
      - leverage_vs_liquidity: Leverage Ratio (X) vs. LCR (Y) - the two
        core Basel resilience pillars.

    A year-scrubber (FY2021-FY2025, the same trimmed window
    curate_comparison_trends() uses) steps through snapshots client-side
    for each - the point of a Gapminder-style chart is watching bubbles
    move, not one static year.

    Source dicts disagree on year-key type (rwa_to_assets_pct's keys are
    the raw DB fiscal_year, int, per in040_risk_metrics.py; pillar3's and
    cost_base's are string, via normalize_pnl_year/AnalysisQueries) - every
    source is cast to str here before lookup, the same class of silent
    int/str key-mismatch bug already found and fixed twice this session
    (cost_base, income_volatility), not repeated a third time."""
    conn = sqlite3.connect(DB_PATH)
    bank_to_group = {
        m["bank"]: group
        for group, meta in parent_groups["group_meta"].items()
        for m in meta["members"]
    }
    assets_by_bank = {
        bank: {str(k): v for k, v in curate_total_assets(conn, entry["frn"]).items()}
        for bank, entry in data.items()
    }
    conn.close()

    def series(entry, source):
        kind, key = source
        if kind == "top":
            raw = entry.get(key) or {}
        elif kind == "pillar3":
            raw = (entry.get("pillar3") or {}).get(key) or {}
        elif kind == "cost_base":
            raw = {y: v.get(key) for y, v in (entry.get("cost_base") or {}).items() if v.get(key) is not None}
        else:
            raise ValueError(kind)
        return {str(k): v for k, v in raw.items()}

    years = [str(y) for y in range(2021, 2026)]

    def build(x_source, y_source):
        points_by_year = {y: [] for y in years}
        for bank, entry in data.items():
            xs = series(entry, x_source)
            ys = series(entry, y_source)
            assets = assets_by_bank[bank]
            for y in years:
                x, yv = xs.get(y), ys.get(y)
                if x is None or yv is None:
                    continue
                points_by_year[y].append({
                    "bank": bank, "x": x, "y": yv,
                    "assets": assets.get(y), "group": bank_to_group.get(bank),
                })
        covered = [y for y in years if points_by_year[y]]
        return {"years": covered, "points_by_year": {y: points_by_year[y] for y in covered}}

    return {
        "risk_vs_capital": build(("top", "rwa_to_assets_pct"), ("pillar3", "CET1 Ratio")),
        "efficiency_vs_capital": build(("cost_base", "cost_to_income_pct"), ("pillar3", "CET1 Ratio")),
        "leverage_vs_liquidity": build(("pillar3", "Leverage Ratio"), ("pillar3", "LCR")),
    }


CLUSTER_DIMS = [
    "CET1 Ratio", "Tier 1 Ratio", "Total Capital Ratio",
    "Leverage Ratio", "LCR", "NSFR", "MREL Ratio",
]


def curate_comparison_clusters():
    """Statistical peer-cluster PCA projection (user request, 2026-09-05,
    following the wayfinder/insights/prototype/cluster_bubble_prototype.html
    prototype the user reacted to, preferring the PCA variant over a raw
    2-dimension scatter since a handful of outlier banks on any single
    ratio squash everyone else into an unreadable clump). Projects
    scripts/insights/cluster_banks.py's existing k-means fit
    (research/bank_clusters.csv) onto its own top-2 principal components,
    computed here in Python with numpy (mirroring cluster_banks.py's own
    median/IQR robust-standardize + winsorize-at-4 method exactly, since
    the CSV's *_value columns are already median-imputed but NOT
    standardized) rather than re-implementing the prototype's from-scratch
    JS eigensolver in production - numpy is already a dependency here via
    cluster_banks.py, so there's no reason for production code to hand-roll
    Jacobi eigendecomposition the way the throwaway prototype did.

    PC1/PC2 loadings ship alongside the projected points (not just the
    projection) so deliverable_shared.js can build its plain-language
    explainer dynamically from the real loadings - the same approach the
    prototype used, so the explanation stays accurate if this data changes
    on a future rebuild rather than drifting out of sync with hand-written
    prose. Eigenvector sign is mathematically arbitrary, so the explainer
    text must describe which dimensions move together/oppositely, never
    which absolute direction on screen is "higher" - see the prototype's
    describeLoadings() for the convention this mirrors."""
    if not CLUSTERS_CSV.exists():
        return None
    with open(CLUSTERS_CSV, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    with open(CLUSTERS_SWEEP_CSV, newline="", encoding="utf-8") as f:
        sweep_rows = list(csv.DictReader(f))

    included = [r for r in rows if r["insufficient_data"] == "0"]
    n_excluded = len(rows) - len(included)
    if not included:
        return None

    X = np.array([[float(r[f"{d}_value"]) for d in CLUSTER_DIMS] for r in included])
    col_median = np.median(X, axis=0)
    q75, q25 = np.percentile(X, [75, 25], axis=0)
    col_iqr = q75 - q25
    col_iqr[col_iqr == 0] = 1.0
    X_std = np.clip((X - col_median) / col_iqr, -4.0, 4.0)

    cov = np.cov(X_std, rowvar=False)
    eigvals, eigvecs = np.linalg.eigh(cov)
    order = np.argsort(-eigvals)
    eigvals, eigvecs = eigvals[order], eigvecs[:, order]
    total_var = float(eigvals.sum())
    pc1_loadings, pc2_loadings = eigvecs[:, 0], eigvecs[:, 1]
    projected = X_std @ eigvecs[:, :2]

    banks = []
    for row, (pc1_v, pc2_v) in zip(included, projected):
        n_imputed = sum(1 for d in CLUSTER_DIMS if row[f"{d}_imputed"] == "1")
        banks.append({
            "bank": row["bank"], "frn": row["frn"],
            "cluster_id": int(row["cluster_id"]), "cluster_label": row["cluster_label"],
            "pc1": round(float(pc1_v), 4), "pc2": round(float(pc2_v), 4),
            "n_imputed": n_imputed,
        })

    best_sweep = max(sweep_rows, key=lambda r: float(r["silhouette"]))
    cluster_ids = sorted({b["cluster_id"] for b in banks})
    cluster_labels = {cid: next(b["cluster_label"] for b in banks if b["cluster_id"] == cid) for cid in cluster_ids}

    return {
        "dims": CLUSTER_DIMS,
        "banks": banks,
        "cluster_ids": cluster_ids,
        "cluster_labels": cluster_labels,
        "n_included": len(included),
        "n_excluded": n_excluded,
        "best_k": int(best_sweep["k"]),
        "silhouette": round(float(best_sweep["silhouette"]), 4),
        "pca": {
            "var_explained_1": round(eigvals[0] / total_var * 100, 2),
            "var_explained_2": round(eigvals[1] / total_var * 100, 2),
            "pc1_loadings": [round(float(v), 4) for v in pc1_loadings],
            "pc2_loadings": [round(float(v), 4) for v in pc2_loadings],
        },
    }


def curate_comparison_outliers():
    """"Most extreme" section (user request, 2026-09-05): reuses
    in009_analysis.py's existing detect_outliers() - percentile-bound,
    robust z-score, YoY-movement, and special-disclosure flags on each
    bank's latest value per core metric - rather than new statistical work.
    A standalone section, not folded into Capital/liquidity/RWA, since it's
    screening/detail material like the headroom table, not a capital-ratio
    visual."""
    observations = AnalysisQueries(DB_PATH).observations()
    records = []
    for metric, sheet in CORE_METRICS.items():
        for item in detect_outliers(observations, metric, sheet):
            records.append({
                "frn": item["frn"], "bank": item["bank"], "metric": item["metric"],
                "fiscal_year": item["fiscal_year"], "value": item["value"], "reasons": item["reasons"],
            })
    return records


def curate_comparison_parent_groups(data):
    """Reintroduces the old dashboard's parent-group dispersion/trend-
    agreement analysis (in010_parent_groups.py) as its own comparison.html
    section (user request, 2026-09-05). Condensed to groups with >=2
    comparable members - a single-entity "group" has nothing to compare,
    and most of the 134 curated groups are single-entity.

    Also carries each group's member roster and an aggregate "Total P&L"
    headline (follow-up user request, 2026-09-05: click a group -> its own
    overview page, and keep headline figures like total P&L visible in the
    comparison table too). Total P&L sums member profit_for_year figures
    ONLY for years every member discloses - the conservative choice the
    user picked over summing whichever members happen to have a given
    year, since a 2-of-3-member year would otherwise look like a real
    decline against a 3-of-3 year."""
    groups_map = AnalysisQueries(DB_PATH).groups()  # frn -> (bank, group, caveat)
    frn_to_display = {bd["frn"]: name for name, bd in data.items()}

    by_group_members = defaultdict(list)
    for frn, (bank, group, caveat) in groups_map.items():
        display = frn_to_display.get(frn)
        if display:  # only entities in our curated 145-bank set have a page to link to
            by_group_members[group].append({"frn": frn, "bank": display, "caveat": caveat})

    conn = sqlite3.connect(DB_PATH)
    group_meta = {}
    for group, members in by_group_members.items():
        if len(members) < 2:
            continue
        member_pnls = [data[m["bank"]].get("profit_for_year", {}) for m in members]
        common_years = set.intersection(*(set(p) for p in member_pnls)) if member_pnls else set()
        total_pnl = {y: sum(p[y] for p in member_pnls) for y in sorted(common_years)}
        # Per-member total assets (2026-09-05 follow-up: the group overview
        # page charts how each member contributes to the group's combined
        # balance sheet) - kept per-bank rather than summed like total_pnl,
        # since the chart needs each member's own line/segment, not a total.
        member_total_assets = {m["bank"]: curate_total_assets(conn, m["frn"]) for m in members}
        # Same "every member or it doesn't count" convention as total_pnl
        # above, for the same reason - a year where a USD-reporting member
        # (e.g. J.P. Morgan Securities) drops out must not silently read as
        # the whole group's combined total assets.
        common_asset_years = set.intersection(*(set(a) for a in member_total_assets.values())) if member_total_assets else set()
        total_assets_by_year = {y: sum(a[y] for a in member_total_assets.values()) for y in sorted(common_asset_years)}
        # What those assets/liabilities actually ARE (2026-09-05 follow-up),
        # per member rather than summed - a % composition can't be added
        # across banks the way an absolute total can. capital_deployment is
        # already computed for every BANKS entry by curate() above, so it's
        # just referenced here, not recomputed; liability_composition has
        # no existing equivalent, so it's built fresh per member.
        member_capital_deployment = {m["bank"]: data[m["bank"]].get("capital_deployment", {}) for m in members}
        member_liability_composition = {m["bank"]: curate_liability_composition(conn, m["frn"]) for m in members}
        # "For the entire parent, how much of its assets are customer
        # loans" (2026-09-05 follow-up): combine members' own absolute £
        # asset/liability amounts into one parent-group composition -
        # summing %'s directly would be wrong (they're not weighted by
        # each member's size), so this sums the underlying £ first and
        # only takes a % of the combined total at the end. Same "every
        # member or it doesn't count" convention as total_pnl/total_assets.
        member_asset_composition_abs = {m["bank"]: curate_asset_composition_absolute(conn, m["frn"]) for m in members}
        common_bs_years = set.intersection(*(set(a) for a in member_asset_composition_abs.values())) if member_asset_composition_abs else set()
        group_asset_composition = {}
        for y in sorted(common_bs_years):
            total = sum(v[y]["total"] for v in member_asset_composition_abs.values())
            if not total:
                continue
            loans = sum(v[y]["loans"] for v in member_asset_composition_abs.values())
            treasury = sum(v[y]["treasury"] for v in member_asset_composition_abs.values())
            cash = sum(v[y]["cash"] for v in member_asset_composition_abs.values())
            other = max(0, total - (loans + treasury + cash))
            group_asset_composition[y] = {
                "cash_pct_of_assets": round(cash / total * 100, 2),
                "loans_pct_of_assets": round(loans / total * 100, 2),
                "treasury_investments_pct_of_assets": round(treasury / total * 100, 2),
                "other": round(other / total * 100, 2),
            }
        common_liab_years = set.intersection(*(set(a) for a in member_liability_composition.values())) if member_liability_composition else set()
        group_liability_composition = {}
        for y in sorted(common_liab_years):
            total = sum(v[y]["total"] for v in member_liability_composition.values())
            if not total:
                continue
            cd = sum(v[y]["customer_deposits"] for v in member_liability_composition.values())
            bd = sum(v[y]["bank_deposits"] for v in member_liability_composition.values())
            wf = sum(v[y]["wholesale_funding"] for v in member_liability_composition.values())
            other = max(0, total - (cd + bd + wf))
            group_liability_composition[y] = {
                "customer_deposits_pct": round(cd / total * 100, 2),
                "bank_deposits_pct": round(bd / total * 100, 2),
                "wholesale_funding_pct": round(wf / total * 100, 2),
                "other_pct": round(other / total * 100, 2),
            }
        # "Where the banking group overall made its profit and loss"
        # (2026-09-05 follow-up): sum each income category across members,
        # same "every member or it doesn't count" convention as total_pnl -
        # a year where only some members disclose an income mix must not
        # read as the whole group's income composition for that year.
        member_incomes = [data[m["bank"]].get("income_breakdown", {}) for m in members]
        common_income_years = set.intersection(*(set(i) for i in member_incomes)) if member_incomes else set()
        total_income_breakdown = {}
        for y in sorted(common_income_years):
            cats = {}
            for income in member_incomes:
                for cat, value in income[y].items():
                    cats[cat] = cats.get(cat, 0) + value
            total_income_breakdown[y] = cats
        group_meta[group] = {
            "members": members, "total_pnl_by_year": total_pnl,
            "member_total_assets": member_total_assets, "total_assets_by_year": total_assets_by_year,
            "member_capital_deployment": member_capital_deployment,
            "member_liability_composition": member_liability_composition,
            "group_asset_composition": group_asset_composition,
            "group_liability_composition": group_liability_composition,
            "total_income_breakdown_by_year": total_income_breakdown,
        }
    conn.close()

    raw = build_in010_payload(DB_PATH)
    metrics = {}
    for metric, entries in raw["parent_groups"].items():
        rows = []
        for g in entries["broad"]:
            level = g["latest_level"]
            if g["member_count"] < 2 or level.get("status") != "comparable":
                continue
            rows.append({
                "group": g["group"], "member_count": g["member_count"], "year": level["year"],
                "min": level["min"], "max": level["max"], "median": level["median"], "range": level["range"],
                # Per-member values (2026-09-05 follow-up: the group overview
                # page charts each member's own contribution, not just the
                # group's aggregate median) - remapped from frn to this
                # build's curated display name, same bridge as group_meta's
                # member roster above.
                "values": {frn_to_display.get(frn, frn): v for frn, v in level["values"].items() if frn in frn_to_display},
                "trends": g["trends"],
            })
        if rows:
            metrics[metric] = rows
    return {"metrics": metrics, "group_meta": group_meta}


# Hand-researched ultimate/resolution-group-level figures (2026-09-05
# follow-up on the "Reported only at the parent-group level" section:
# "likely disclosed only at ultimate parent, potentially we look up the
# figures if the ultimate parent discloses them" - then, once MREL was
# done, "try the same for LCR and NSFR... instead of a sibling member
# substitute, perhaps we try search in the ultimate parent as well, and
# see if that can get a better picture for the whole group"). Each entry
# is that ultimate/holding parent's own disclosed ratio, sourced fresh
# against the group's own public Pillar 3 disclosures - not inferred, not
# carried over from an unrelated regulatory regime. For LCR/NSFR this is
# consulted even where a sibling-member substitute already exists (see
# curate_group_level_metrics below): the group's own consolidated LCR/NSFR
# is a genuinely better answer than one non-resolution-entity subsidiary's
# solo ratio standing in for the whole group. Keyed by our group name,
# then by PILLAR3_SHEET_NAMES sheet name.
ULTIMATE_PARENT_METRICS = {
    "Lloyds Banking Group": {
        "MREL Ratio": {
            "entity": "Lloyds Banking Group plc",
            "values": {"2024": 32.2, "2025": 32.2},
            "citation": "Lloyds Banking Group plc 2025 Year-End Pillar 3 Disclosures (17 Feb 2026), Table KM2 'Key Metrics - TLAC requirements', p.7: 'TLAC as a percentage of RWA' for the consolidated position of Lloyds Banking Group plc (the resolution entity), covering Lloyds Bank plc, Bank of Scotland plc and Lloyds Bank Corporate Markets plc.",
        },
        "LCR": {
            "entity": "Lloyds Banking Group plc",
            "values": {"2024": 146.0, "2025": 145.0},
            "citation": "Lloyds Banking Group plc 2025 Year-End Pillar 3 Disclosures (17 Feb 2026), Table LIQ1 'Liquidity coverage ratio (LCR)', p.113: average LCR (12-month basis) for the consolidated Group was 145% at 31 December 2025 (146% at 31 December 2024).",
        },
        "NSFR": {
            "entity": "Lloyds Banking Group plc",
            "values": {"2024": 129.0, "2025": 124.0},
            "citation": "Lloyds Banking Group plc 2025 Year-End Pillar 3 Disclosures (17 Feb 2026), Table LIQ2 'Net stable funding ratio', p.115: average NSFR (4-quarter basis) for the consolidated Group was 124% at 31 December 2025 (129% at 31 December 2024).",
        },
    },
    "Banco Santander S.A.": {
        "MREL Ratio": {
            "entity": "Santander UK Group Holdings plc",
            "values": {"2025": 36.1},
            "citation": "Santander UK Group Holdings plc Annual Consolidated Regulatory and Market Disclosures (ACRMD) 2025, p.6, Table KM2 'Key metrics - MREL': Total Own Funds and Eligible Liabilities as at 31 December 2025 were 36.1% of RWA (also recorded in Santander UK's own workbook source note).",
        },
        "LCR": {
            "entity": "Santander UK Group Holdings plc",
            "values": {"2025": 160.0},
            "citation": "Santander UK Group Holdings plc ACRMD 2025, p.15, Table LIQ1 'Liquidity Coverage Ratio': HoldCo Group's 12-month average LCR was 160% at 31 December 2025.",
        },
        "NSFR": {
            "entity": "Santander UK Group Holdings plc",
            "values": {"2025": 135.0},
            "citation": "Santander UK Group Holdings plc ACRMD 2025, p.17, Template UK LIQ2 'Net Stable Funding Ratio': HoldCo Group's NSFR was 135% at 31 December 2025.",
        },
    },
    "HSBC group": {
        "MREL Ratio": {
            "entity": "HSBC Holdings plc (European resolution group)",
            "values": {"2024": 36.8, "2025": 35.5},
            "citation": "HSBC Holdings plc Pillar 3 Disclosures at 31 December 2025, Table 20.i 'Key metrics of the European resolution group (KM2)', p.30: 'TLAC as a percentage of RWA' for the European resolution group (HSBC Bank plc, HSBC UK Bank plc, HSBC Continental Europe as material entities).",
        },
        "LCR": {
            "entity": "HSBC Holdings plc",
            "values": {"2025": 137.0},
            "citation": "HSBC Holdings plc Pillar 3 Disclosures at 31 December 2025, Table 14 'Liquidity coverage ratio (UK LIQ1)', p.23: average LCR (12-month basis) for the HSBC Group was 137% at 31 December 2025.",
        },
        "NSFR": {
            "entity": "HSBC Holdings plc",
            "values": {"2025": 143.0},
            "citation": "HSBC Holdings plc Pillar 3 Disclosures at 31 December 2025, Table 15 'Net stable funding ratio (UK LIQ2)', p.24: average NSFR (4-quarter basis) for the HSBC Group was 143% at 31 December 2025.",
        },
    },
    "NatWest group": {
        "LCR": {
            "entity": "NatWest Group plc",
            "values": {"2024": 151.0, "2025": 147.0},
            "citation": "NatWest Group plc Annual Results 2025 (13 Feb 2026), Key metrics table, p.9: average Liquidity Coverage Ratio for the Group was 147% at 31 December 2025 (151% at 31 December 2024).",
        },
        "NSFR": {
            "entity": "NatWest Group plc",
            "values": {"2024": 137.0, "2025": 135.0},
            "citation": "NatWest Group plc Annual Results 2025 (13 Feb 2026), Key metrics table, p.9: average Net Stable Funding Ratio for the Group was 135% at 31 December 2025 (137% at 31 December 2024).",
        },
    },
    # JPMorgan Chase group: researched, not found. J.P. Morgan Europe
    # Limited / J.P. Morgan Securities plc are non-ring-fenced UK
    # subsidiaries of a US G-SIB resolved via the US Single Point of Entry
    # strategy - TLAC/MREL is set and disclosed at JPMorgan Chase & Co.
    # (the US resolution entity), not as a standalone UK MREL ratio. The
    # Bank of England's own "External MRELs 2025" list covers only firms
    # whose resolution entity is incorporated in the UK, which excludes
    # both JPM UK entities. No genuine UK-scoped figure exists to cite, so
    # this group is deliberately left out rather than guessed at.
}


def curate_group_level_metrics(data, group_meta):
    """Surfaces Pillar 3 metrics a member doesn't disclose solo because
    it's only reported at the parent-group level (2026-09-05 user request:
    "some of the missing data was attributed to being parent group level
    only" - this project's own disclosure notes already recorded exactly
    that as each bank was built. E.g. Bank of Scotland's own restatement_
    note for LCR/NSFR/MREL Ratio literally reads "disclosed only at the
    wider Lloyds Banking Group plc consolidated level, which is out of
    scope for this entity-level workbook"). Where a sibling member of the
    SAME group discloses that metric on its own Group-consolidated basis,
    that figure is surfaced as the de facto group-level number; where no
    member has one at all (MREL Ratio - set only at each group's ultimate
    holding company, itself not one of Katalysis's 145 workbooks), the gap
    is reported too rather than silently dropped."""
    conn = sqlite3.connect(DB_PATH)
    out = {}
    for group, meta in group_meta.items():
        frns = [m["frn"] for m in meta["members"]]
        frn_to_bank = {m["frn"]: m["bank"] for m in meta["members"]}
        placeholders = ",".join("?" * len(frns))
        group_result = {}
        for sheet in PILLAR3_SHEET_NAMES:
            rows = conn.execute(
                f"SELECT frn, restatement_note FROM annual_metrics "
                f"WHERE sheet=? AND frn IN ({placeholders}) AND is_numeric=0 AND restatement_note IS NOT NULL "
                f"AND (restatement_note LIKE '%group%' OR restatement_note LIKE '%entity level%' OR restatement_note LIKE '%this level%')",
                [sheet] + frns,
            ).fetchall()
            note_by_frn = {}
            for frn, note in rows:
                note_by_frn.setdefault(str(frn), note)
            if not note_by_frn:
                continue
            substitute = None
            for m in meta["members"]:
                if m["frn"] in note_by_frn:
                    continue
                series = data.get(m["bank"], {}).get("pillar3", {}).get(sheet, {})
                if series:
                    substitute = {"bank": m["bank"], "values": series}
                    break
            # Consulted regardless of whether a sibling-member substitute
            # exists: for LCR/NSFR the group's own consolidated ratio is a
            # genuinely better "whole group" answer than one non-resolution
            # -entity subsidiary's solo figure standing in for the group.
            ultimate_parent = ULTIMATE_PARENT_METRICS.get(group, {}).get(sheet)
            group_result[sheet] = {
                "flagged": [{"bank": frn_to_bank[frn], "note": note} for frn, note in note_by_frn.items()],
                "substitute": substitute,
                "ultimate_parent": ultimate_parent,
            }
        if group_result:
            out[group] = group_result
    conn.close()
    return out


def curate():
    d = build_in040_payload(DB_PATH)
    # IN-021's screening records (also used cross-bank by
    # curate_comparison_trends()) - grouped by frn once here so every bank's
    # own page can show "how far above the regulatory minimum is this bank,
    # per metric" without re-querying the DB per bank (user request,
    # 2026-09-05: bring headroom onto the per-bank pages, not just the
    # cross-bank comparison table).
    headroom_by_frn = defaultdict(list)
    for r in build_headroom_payload(DB_PATH)["records"]:
        headroom_by_frn[r["frn"]].append({
            "metric": r["metric"], "latest_year": r["latest_year"],
            "current_value": r["current_value"], "regulatory_floor": r["regulatory_floor"],
            "current_headroom": r["current_headroom"], "trend_direction": r["trend_direction"],
            "trend_change": r["trend_change"], "status": r["status"],
        })
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
        entry["leverage"] = {
            "equity_to_assets_pct": d["leverage"]["equity_to_assets_pct"].get(frn, {}),
            "leverage_ratio_reported_pct": d["leverage"]["leverage_ratio_reported_pct"].get(frn, {}),
        }
        entry["income_volatility"] = {
            "yoy_change_pct": d["income_volatility"]["yoy_change_pct"].get(frn, {}),
            "volatility_stdev_of_yoy_pct": d["income_volatility"]["volatility_stdev_of_yoy_pct"].get(frn),
        }
        entry["headroom"] = headroom_by_frn.get(frn, [])
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
                # IN-041's own years are ints; the revenue-fallback loop below
                # keys by normalize_pnl_year()'s strings - normalizing to str
                # here up front avoids each Python dict silently holding both
                # an int and a str key for the same year (e.g. 2024 and
                # "2024"), which look like one key in the browser's JSON but
                # are two distinct entries in Python: json.dumps happily
                # emits both as duplicate "2024" keys and JSON.parse then
                # keeps only the later one, silently discarding this real
                # cost/revenue data in favour of the fallback's incomplete
                # (categories-only) synthesized revenue for that year -
                # verified against the real database: 112 of 145 banks,
                # 524 bank-years were losing their cost_to_income_pct/
                # personnel_expense/other_operating_expense this way before
                # this fix.
                cost_years.setdefault(str(y), {})[m] = v
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

    # A bank with no IFRS 9 stage split at all (Weatherbys was the first
    # found, but this applies to any such bank, not just Weatherbys) often
    # still discloses SOME other Pillar 3 credit-risk breakdown - a
    # different, product-level concentration view worth showing on its own
    # per-bank page rather than leaving the bank with nothing. Deliberately
    # per-bank page only: the comparison page's "Loan concentration &
    # quality" section stays IFRS 9 stage-only (see renderComparisonPage's
    # `kind === 'stage'` filter in deliverable_shared.js) since exposure
    # class isn't the same signal and mixing the two into one cross-bank
    # comparison would be misleading.
    #
    # This is a hand-transcribed, no-shared-schema dataset (see CLAUDE.md) -
    # surveyed the 42 banks with no stage data (2026-09-05) and, aside from
    # Weatherbys, found the label wording is essentially unique per bank
    # (e.g. "Loan book by risk of financial loss", "Credit quality analysis
    # (Note 22)" - one bank each, no shared pattern worth generalizing a
    # regex over without risking a false match against an unrelated
    # maturity/geography/product breakdown). Two more DID turn out to share
    # Weatherbys' underlying concept closely enough to add here, each
    # verified against its own real figures before being added:
    # - Morgan Stanley Bank International: "Exposure to credit risk by
    #   class, subject to ECL (external counterparties only)" - the 4
    #   category rows sum exactly to its own "Total gross credit exposure"
    #   row in every year (e.g. FY2021: 20144+124091+0+22811=167046),
    #   confirming they're a clean, exhaustive category split.
    # - Mizuho International: "Credit risk exposures by credit quality step
    #   (standardised approach), net of CRM" - mixes real per-step exposure
    #   amounts ("Credit quality step 1-6", "Unrated") with ratio/RWA/memo
    #   rows ("Credit risk RWA density...", "Credit risk RWAs (excluding
    #   CCR)", "Memo: Total gross credit exposure...", "Total net credit
    #   exposure") that are NOT exposure-amount categories - the exclude
    #   pattern below drops all of those by keyword, keeping only the
    #   genuine per-step amounts.
    #
    # Followed up (2026-09-04) by checking all 40 remaining "none" banks'
    # full row-label lists, not just prefixes - most are still genuinely
    # unique disclosures (maturity/geography/product-only splits, plain
    # gross/net/allowance rollforwards) with no category structure worth
    # generalizing over. Four more DID turn out to be genuine, exhaustive
    # category splits, each confirmed by checking its categories sum
    # exactly to its own disclosed total in every year with data:
    # - ICICI Bank UK: "Loans and advances to customers, by credit risk
    #   category" - Neither past due nor impaired + Past due not impaired +
    #   Impaired, net of "Impairment & collective allowances", ties exactly
    #   to "Total loans and advances to customers (net)" (e.g. FY2021:
    #   1465451+40536+55208-39057=1522138).
    # - Tandem: "Credit Quality Analysis" - Neither past due nor impaired +
    #   Past due but not impaired + Total gross impaired loans ties exactly
    #   to "Total gross amount due" (e.g. FY2021: 423400+13074+8443=444917).
    #   Note "Total gross impaired loans" is itself a category here despite
    #   the word "Total" in its name - the exclude regex below only drops
    #   the real totalling row ("Total gross amount due"), not this one.
    # - State Bank of India UK: "Loan book by risk of financial loss
    #   (Pillar 3 credit risk exposures)" - 6 categories (Neither past due
    #   beyond 90 days nor impaired, Past due beyond 90 days but not
    #   impaired, Impaired, Pipeline loans, Repossessions, Unutilised
    #   overdraft commitments) tie exactly to "Total maximum exposure of
    #   loans and advances to customers" (e.g. FY2021:
    #   1142.58+0+4.61+86.83+0+8.51=1242.53).
    # - United National: "Loans and advances to customers by impairment
    #   status (FRS 102 basis - not IFRS 9 stage 1/2/3)" - Impaired loans +
    #   Non-impaired loans ties exactly to "Gross loans and advances to
    #   customers" (e.g. FY2022: 8027926+631590077=639618003). The "not
    #   IFRS 9 stage 1/2/3" parenthetical is deliberate on the bank's part
    #   (FRS 102, not IFRS 9) - correctly NOT a stage-detection miss.
    _EXPOSURE_CLASS_PATTERNS = (
        ("Regulatory credit risk exposure%", re.compile(r"total regulatory", re.I)),
        ("Exposure to credit risk by class%", re.compile(r"\btotal\b", re.I)),
        ("Credit risk exposures by credit quality step%", re.compile(r"total|memo|rwa|density|%", re.I)),
        ("Loans and advances to customers, by credit risk category%", re.compile(r"total|ratio|allowance", re.I)),
        # SQLite LIKE is case-insensitive, so a bare "Credit Quality
        # Analysis%" also matches Kroo Bank's differently-shaped "Credit
        # quality analysis (FY2023/FY2022, Note 22 Risk Management)" label
        # (sparse, non-exhaustive, not a candidate) - requiring the literal
        # " - " right after "Analysis" matches only Tandem's exact prefix,
        # which has no parenthetical before its dash.
        ("Credit Quality Analysis - %", re.compile(r"total gross amount due", re.I)),
        ("Loan book by risk of financial loss%", re.compile(r"total maximum exposure", re.I)),
        (
            "Loans and advances to customers by impairment status%",
            re.compile(r"provision|fair value|unamortised|gross loans and advances to customers|net loans and advances to customers", re.I),
        ),
    )
    for label, frn in BANKS.items():
        if out[label]["loan_composition"]["kind"] != "none":
            continue
        for like_pattern, exclude_re in _EXPOSURE_CLASS_PATTERNS:
            rows = conn.execute(
                """
                SELECT row_label, year, value_numeric FROM annual_metrics
                WHERE frn=? AND sheet = 'Asset Quality'
                  AND row_label LIKE ? AND value_numeric IS NOT NULL
                ORDER BY year, row_label
                """,
                (frn, like_pattern),
            ).fetchall()
            rows = [r for r in rows if not exclude_re.search(r[0])]
            if not rows:
                continue
            exposure_years = {}
            for lbl, year, val in rows:
                cat = lbl.split(" - ", 1)[1]
                y = year.replace("FY", "")
                exposure_years.setdefault(y, {})[cat] = val
            out[label]["loan_composition"] = {"kind": "exposure_class", "years": exposure_years}
            break
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
<script src="chart.umd.min.js"></script>
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


def write_comparison(data, banks_index, parent_groups):
    html = HEAD.format(
        title="Credit risk — comparison",
        back_link="",
        h1="Credit risk",
        sub_fallback="",
        body="",
        todo_note=TODO_NOTE,
    )
    trends = curate_comparison_trends()
    outliers = curate_comparison_outliers()
    efficiency = curate_comparison_efficiency(data)
    bubbles = curate_comparison_bubbles(data, parent_groups)
    clusters = curate_comparison_clusters()
    html += f"""
<script id="data" type="application/json">{json.dumps(data)}</script>
<script id="banks-index" type="application/json">{json.dumps(banks_index)}</script>
<script id="trends-data" type="application/json">{json.dumps(trends)}</script>
<script id="outliers-data" type="application/json">{json.dumps(outliers)}</script>
<script id="parent-groups-data" type="application/json">{json.dumps(parent_groups)}</script>
<script id="efficiency-data" type="application/json">{json.dumps(efficiency)}</script>
<script id="bubbles-data" type="application/json">{json.dumps(bubbles)}</script>
<script id="clusters-data" type="application/json">{json.dumps(clusters)}</script>
<script src="deliverable_shared.js"></script>
<script>
const DATA = JSON.parse(document.getElementById('data').textContent);
const BANKS_INDEX = JSON.parse(document.getElementById('banks-index').textContent);
const TRENDS = JSON.parse(document.getElementById('trends-data').textContent);
const OUTLIERS = JSON.parse(document.getElementById('outliers-data').textContent);
const PARENT_GROUPS = JSON.parse(document.getElementById('parent-groups-data').textContent);
const EFFICIENCY = JSON.parse(document.getElementById('efficiency-data').textContent);
const BUBBLES = JSON.parse(document.getElementById('bubbles-data').textContent);
const CLUSTERS = JSON.parse(document.getElementById('clusters-data').textContent);
renderSidebar('comparison', BANKS_INDEX);
renderComparisonPage(DATA, Object.keys(DATA), TRENDS, OUTLIERS, PARENT_GROUPS, EFFICIENCY, BUBBLES, CLUSTERS);
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
        # Span of available history (max year - min year + 1), not a count of
        # years with actual data points - a bank with disclosures in 2015,
        # 2019 and 2022 has 8 years of history available, not 3. Both bounds
        # come straight from the real year keys already resolved via SQL
        # against annual_metrics further up curate() (the stage_balances and
        # _EXPOSURE_CLASS_PATTERNS queries), so this stays a deterministic
        # min/max over real data, not a judgment call.
        comp_years = [int(y) for y in comp["years"]]
        history_span = (max(comp_years) - min(comp_years) + 1) if comp_years else 0
        rows_html += f"""<tr>
      <td><a href="bank-{b['slug']}.html">{b['name']}</a></td>
      <td class="num">{profit_cell}</td>
      <td><span class="basis-tag">{basis}</span></td>
      <td class="num">{history_span}</td>
      <td><a href="bank-{b['slug']}.html">View profile</a></td>
    </tr>"""

    body = f"""<div class="block" style="margin-top:8px;">
    <div class="card" style="padding:0;">
      <table class="bank-table">
        <thead><tr>
          <th>Bank</th><th>Profit or loss (latest)</th><th>Loan concentration basis</th><th>History available (yrs)</th><th></th>
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


def write_business_model_page(records, banks_index):
    html = HEAD.format(
        title="Credit risk — business model",
        back_link='<a class="back" href="comparison.html">← Comparison</a>',
        h1="Business model",
        sub_fallback=(
            "How each bank makes money: fee income as a share of total income (fee + net interest), "
            "latest year disclosed, grouped by a hand-curated digital / traditional / other tag — "
            "reviewed, not machine-derived, so treat borderline cases as a starting point."
        ),
        body="",
        todo_note="",
    )
    html += """
<script id="business-model-data" type="application/json">""" + json.dumps(records) + """</script>
<script id="banks-index" type="application/json">""" + json.dumps(banks_index) + """</script>
<script src="deliverable_shared.js"></script>
<script>
const BUSINESS_MODEL_DATA = JSON.parse(document.getElementById('business-model-data').textContent);
const BANKS_INDEX = JSON.parse(document.getElementById('banks-index').textContent);
renderSidebar('business-model', BANKS_INDEX);
renderBusinessModelPage(BUSINESS_MODEL_DATA);
</script>
</body>
</html>
"""
    (OUT_DIR / "business-model.html").write_text(html)


def write_investments_page(records, banks_index):
    html = HEAD.format(
        title="Credit risk — investments",
        back_link='<a class="back" href="comparison.html">← Comparison</a>',
        h1="Investment book composition",
        sub_fallback=(
            "What kind of investments banks hold on their balance sheets, latest year disclosed. "
            "Two independent cuts: measurement basis (amortised cost / “hold to collect” vs "
            "fair-value-through-P&L or OCI / “mark to market”), and government/sovereign vs other "
            "investment securities. Excludes investments in subsidiaries, associates and joint ventures, "
            "and repo/securities-financing lines — those aren't markets portfolio positions. Coverage is "
            "thin (most banks don't disclose this split at the level this project's source documents capture), "
            "so absence from a chart means “not disclosed separately”, not “zero”."
        ),
        body="",
        todo_note="",
    )
    html += """
<script id="investments-data" type="application/json">""" + json.dumps(records) + """</script>
<script id="banks-index" type="application/json">""" + json.dumps(banks_index) + """</script>
<script src="deliverable_shared.js"></script>
<script>
const INVESTMENTS_DATA = JSON.parse(document.getElementById('investments-data').textContent);
const BANKS_INDEX = JSON.parse(document.getElementById('banks-index').textContent);
renderSidebar('investments', BANKS_INDEX);
renderInvestmentsPage(INVESTMENTS_DATA);
</script>
</body>
</html>
"""
    (OUT_DIR / "investments.html").write_text(html)


def write_bank_page(bank_name, bank_data, banks_index):
    slug = slugify(bank_name)
    html = HEAD.format(
        title=f"{bank_name} — credit risk",
        back_link='<a class="back" href="banks.html">← All banks</a>',
        h1=render_bank_heading(bank_name),
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


def write_group_page(group, group_meta, group_metrics, group_level_metrics, banks_index):
    """One page per multi-member parent group (user request, 2026-09-05:
    click a group in comparison.html's Parent groupings table -> an
    overview page for that group), modeled on write_bank_page()."""
    slug = slugify(group)
    html = HEAD.format(
        title=f"{group} — credit risk",
        back_link='<a class="back" href="comparison.html">← Comparison</a>',
        h1=group,
        sub_fallback="",
        body="",
        todo_note=TODO_NOTE,
    )
    group_payload = {
        "group": group, "meta": group_meta, "metrics": group_metrics,
        "group_level_metrics": group_level_metrics,
    }
    html += f"""
<script id="group-data" type="application/json">{json.dumps(group_payload)}</script>
<script id="banks-index" type="application/json">{json.dumps(banks_index)}</script>
<script src="deliverable_shared.js"></script>
<script>
const GROUP_DATA = JSON.parse(document.getElementById('group-data').textContent);
const BANKS_INDEX = JSON.parse(document.getElementById('banks-index').textContent);
renderSidebar(null, BANKS_INDEX);
renderGroupPage(GROUP_DATA, BANKS_INDEX);
</script>
</body>
</html>
"""
    (OUT_DIR / f"group-{slug}.html").write_text(html)


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
    if LOGOS_DIR.exists():
        shutil.copytree(LOGOS_DIR, OUT_DIR / "assets" / "logos", dirs_exist_ok=True)
    # IN-052: the old dashboard (IN-036) deliberately vendored Chart.js
    # locally so the deliverable has zero CDN dependency and works offline;
    # IN-051's migration silently reintroduced a jsdelivr CDN <script> tag.
    # Reconciled onto the same vendored bundle everywhere, not just the
    # trajectories section being migrated in this pass.
    shutil.copy(ROOT / "vendor" / "chartjs" / "chart.umd.min.js", OUT_DIR / "chart.umd.min.js")
    data = curate()
    banks_index = [{"name": name, "slug": slugify(name)} for name in data]
    parent_groups = curate_comparison_parent_groups(data)
    write_comparison(data, banks_index, parent_groups)
    write_banks_directory(data, banks_index)
    business_model_conn = sqlite3.connect(DB_PATH)
    write_business_model_page(curate_business_model(data, business_model_conn), banks_index)
    write_investments_page(curate_investment_composition_records(data, business_model_conn), banks_index)
    business_model_conn.close()
    for name, bank_data in data.items():
        write_bank_page(name, bank_data, banks_index)
        write_workbook_viewer(name, bank_data)
    group_level_metrics = curate_group_level_metrics(data, parent_groups["group_meta"])
    for group, group_meta in parent_groups["group_meta"].items():
        group_metrics = {
            metric: [r for r in rows if r["group"] == group]
            for metric, rows in parent_groups["metrics"].items()
        }
        group_metrics = {metric: rows for metric, rows in group_metrics.items() if rows}
        write_group_page(group, group_meta, group_metrics, group_level_metrics.get(group, {}), banks_index)
    print(f"Wrote comparison.html, banks.html, {len(data)} bank-<slug>.html, {len(data)} workbook-<slug>.html, "
          f"and {len(parent_groups['group_meta'])} group-<slug>.html pages to {OUT_DIR}")


if __name__ == "__main__":
    main()
