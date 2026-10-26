#!/usr/bin/env /usr/bin/python3
"""Assemble the UK bank profitability deliverable (CSV + Excel).

Consumes:
  - the extraction from build_profitability_table.py (JSON)
  - research/UK_banks_ROE_research.xlsx   (prior desk research, mostly 2024)
  - research/UK_Banks_Key_Metrics.xlsx    (a template; every data cell is n/d)
  - scratchpad/thebanks_eu.jsonl          (aggregator figures, optional)

Writes research/UK_banks_profitability_<date>.{csv,xlsx}. It writes NOTHING to
banks/ - the delivered workbooks are untouched by design.

  - research/profitability/published_returns.jsonl  (what the BANKS publish)

The organising rule: FOUR SOURCES, FOUR COLUMNS, NEVER MERGED. A figure we
computed from a bank's own transcribed statements, a figure the BANK ITSELF
publishes, a figure a desk-research file recorded, and a figure an aggregator
publishes are different claims about the world. Averaging them, or letting one
silently fill in for another, would destroy the only thing that makes a
disagreement visible.

The fourth source is the bank's own report, added 2026-10-10 on the user's
instruction. It is the most authoritative of the four and the LEAST
comparable: a bank's published return is struck on that bank's own
definition, so the figures cannot be ranked against each other or against
ours without reading each definition. It therefore gets its own sheet rather
than a column in the computed grid, and every figure carries its definition,
its entity, and whether it has been verified at 300 dpi or is still an OCR
lead.
"""
import csv
import datetime
import json
import os
import re
import sys

import openpyxl
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]
# A year-column header that says more than "FY20XX" after its unit is stripped:
# a period length, a stub/transition, an entity code, or a footnote marker.
PERIOD_RISK = re.compile(r"\d+\s*m(o|onth)?s?\b|stub|transition|pro[- ]?forma|[\u2020\u2021*]|\([A-Z]{2,6}\)")
TODAY = datetime.date.today().isoformat()
HDR = PatternFill("solid", start_color="1F3A5F", end_color="1F3A5F")
HDRF = Font(color="FFFFFF", bold=True)
NOTE = Font(italic=True, size=9, color="444444")


def load_published(path):
    """{(bank, FY): (value, measure_label)} from the prior ROE research file."""
    out = {}
    if not os.path.exists(path):
        return out
    wb = openpyxl.load_workbook(path, read_only=True)
    ws = wb["ROE research"] if "ROE research" in wb.sheetnames else wb[wb.sheetnames[0]]
    rows = list(ws.iter_rows(values_only=True))
    hdr = [str(c or "").strip() for c in rows[0]]
    ycol = {j: h for j, h in enumerate(hdr) if re.fullmatch(r"\d{4}", h)}
    for row in rows[1:]:
        bank = str(row[0] or "").strip()
        if not bank:
            continue
        for j, y in ycol.items():
            try:
                v = float(str(row[j]).replace("%", "").strip())
            except (TypeError, ValueError):
                continue
            meas = str(row[j + 1] or "").strip() if j + 1 < len(row) else ""
            out[(bank, "FY" + y)] = (v, meas)
    wb.close()
    return out


def load_own_published(path):
    """{(bank, FY): [record]} - returns the BANK ITSELF publishes.

    A fourth source, and the one the user asked for on 2026-10-10: "we should
    try and use the report from the banks themselves where possible". It is
    kept strictly apart from `load_published` above, which despite its name
    reads the prior DESK RESEARCH file - third-party figures of unknown
    derivation, and demonstrably not always right (its United Trust Bank
    years are transposed against UTB's own published series).

    These records are NOT comparable with our computed column and are never
    merged into it. A bank's own return is struck on the bank's own
    definition, and those differ: Al Rayan's "Return on equity" is profit
    BEFORE tax over average equity, United Trust's is net of the coupon on
    contingent convertible securities. The definition travels with the figure
    for exactly that reason, and a record whose `verification` is "ocr_lead"
    is a lead, not a finding.
    """
    out = {}
    if not os.path.exists(path):
        return out
    for line in open(path):
        line = line.strip()
        if not line:
            continue
        rec = json.loads(line)
        if "_schema" in rec or rec.get("excluded") or rec.get("publishes_none"):
            continue
        if rec.get("bank") and rec.get("year"):
            out.setdefault((rec["bank"], rec["year"]), []).append(rec)
    return out


def load_own_published_all(path):
    """Every record including exclusions and publishes-none, for its own sheet."""
    out = []
    if not os.path.exists(path):
        return out
    for line in open(path):
        line = line.strip()
        if line:
            rec = json.loads(line)
            if "_schema" not in rec:
                out.append(rec)
    return out


# Aggregator names that match no project bank. Each alias is settled by the
# ENTITY the aggregator file itself states, not by name similarity - which
# matters most for the two that look ambiguous and are not: the file records
# "NOT NatWest Group plc" and "NOT Santander UK Group Holdings", so NATWEST is
# the ring-fenced National Westminster Bank Plc and SANTANDER UK is Santander
# UK plc (company 02294747), distinct from Santander Financial Services plc.
# Without these five, those banks' values were silently dropped: the loader
# found no matching bank and said nothing.
AGG_ALIASES = {
    "HAMPSHIRE TRUST": "HAMPSHIRE TRUST BANK",
    "HSBC UK BANK": "HSBC UK BANK PLC",
    "NATWEST": "NATIONAL WESTMINSTER BANK PLC",
    "OAKNORTH": "OAKNORTH BANK",
    "SANTANDER UK": "SANTANDER",
}

# Verification states in descending strength. All of these are thebanks.eu, so
# they belong in ONE column - but they are not equally evidenced, and the
# state has to travel with the value or the column asserts a uniformity it
# does not have. A `wayback_snapshot` has a replay URL and a 14-digit
# timestamp; an `archive_search_indexed` record has neither and must never be
# described as a verified capture.
AGG_PRECEDENCE = ["wayback_snapshot", "thebanks_profile", "search_indexed",
                  "archive_search_indexed", "search_snippet"]


def _agg_rank(verification):
    try:
        return AGG_PRECEDENCE.index(verification)
    except ValueError:
        return len(AGG_PRECEDENCE)


def _agg_year(raw):
    y = str(raw or "").strip()
    if y.startswith("FY"):
        return y
    return "FY" + y if re.fullmatch(r"\d{4}", y) else ""


def _agg_value(raw):
    try:
        return float(str(raw).replace("%", "").replace(",", "").strip())
    except (TypeError, ValueError):
        return None


def load_aggregator(paths):
    """{(bank, FY, metric): {...}} merged from every thebanks.eu file.

    Three files carry the same source in two different record shapes: the
    original collection is one record per metric (`metric` + `value`), while
    the full collection and the Wayback extraction are one record per
    bank-year carrying `roe_pct` and `roa_pct`. Both shapes are normalised
    here rather than in two places.

    Where two files give a value for the same (bank, year, metric), the
    STRONGER verification wins and a numeric disagreement is recorded on the
    surviving row - never silently dropped. thebanks.eu restates, so two
    snapshots of one bank-year can legitimately differ, and which one you are
    looking at is exactly what a reader needs to know.
    """
    out = {}
    if isinstance(paths, str):
        paths = [paths]
    for path in paths:
        if not path or not os.path.exists(path):
            continue
        label = os.path.basename(path)
        for line in open(path, encoding="utf-8"):
            line = line.strip()
            if not line:
                continue
            try:
                r = json.loads(line)
            except ValueError:
                continue
            if r.get("done") or not r.get("bank"):
                continue
            bank = AGG_ALIASES.get(r["bank"].strip().upper(), r["bank"].strip().upper())
            year = _agg_year(r.get("year"))
            if not year:
                continue
            url = r.get("archive_url") or r.get("source_url") or r.get("url") or ""
            verification = r.get("verification") or "search_snippet"
            # shape A: one record per metric; shape B: roe_pct / roa_pct
            found = []
            if r.get("value") not in (None, ""):
                found.append((str(r.get("metric", "ROE")).upper(), r["value"]))
            for key, metric in (("roe_pct", "ROE"), ("roa_pct", "ROA")):
                if r.get(key) not in (None, ""):
                    found.append((metric, r[key]))
            for metric, raw in found:
                v = _agg_value(raw)
                if v is None:
                    continue
                key = (bank, year, metric)
                new = {"value": v, "url": url, "verification": verification,
                       "source": label, "disagreement": None}
                old = out.get(key)
                if old is None:
                    out[key] = new
                    continue
                clash = (None if abs(old["value"] - v) < 1e-9 else
                         "%s says %s%%, %s says %s%%"
                         % (old["source"], old["value"], label, v))
                if _agg_rank(verification) < _agg_rank(old["verification"]):
                    new["disagreement"] = clash or old["disagreement"]
                    out[key] = new
                elif clash:
                    old["disagreement"] = old["disagreement"] or clash
    return out


def sheet(wb, name, headers, rows, widths, note=None):
    ws = wb.create_sheet(name)
    ws.append(headers)
    for c in range(1, len(headers) + 1):
        ws.cell(row=1, column=c).fill = HDR
        ws.cell(row=1, column=c).font = HDRF
        ws.cell(row=1, column=c).alignment = Alignment(wrap_text=True, vertical="center")
    for r in rows:
        ws.append(r)
    for i, w in enumerate(widths, start=1):
        ws.column_dimensions[get_column_letter(i)].width = w
    ws.freeze_panes = "B2"
    if note:
        r = ws.max_row + 2
        ws.cell(row=r, column=1, value=note).font = NOTE
        ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=max(4, len(headers)))
        ws.cell(row=r, column=1).alignment = Alignment(wrap_text=True, vertical="top")
        ws.row_dimensions[r].height = 120
    return ws


def main(extract_json, agg_path, outbase, *extra_agg):
    d = json.load(open(extract_json))
    rows = d["rows"]
    pub = load_published("research/UK_banks_ROE_research.xlsx")
    own = load_own_published("research/profitability/published_returns.jsonl")
    own_all = load_own_published_all("research/profitability/published_returns.jsonl")
    # Every thebanks.eu file we hold, not just the one named on the command
    # line. Until 2026-10-22 only `agg_path` was read, so the column carried
    # 20 bank-years while 179 sat on disk: the full exact-entity collection
    # and the Wayback extraction reached no column at all, and FY2022/FY2023
    # showed as having no aggregator coverage when in fact we had 36
    # bank-years of it. Extra paths may still be passed on the command line
    # and are read in addition to these.
    agg_paths = [agg_path]
    agg_paths += [os.path.join("research", "profitability", "thebanks_eu", n)
                  for n in ("thebanks_eu_returns_with_archives.jsonl",
                            "wayback_returns.jsonl")]
    agg_paths += list(extra_agg)
    for p in agg_paths:
        print("  aggregator source: %s%s"
              % (p, "" if os.path.exists(p) else "   [ABSENT, skipped]"))
    agg = load_aggregator(agg_paths)
    banks = sorted({r["bank"] for r in rows})
    idx = {(r["bank"], r["year"]): r for r in rows}

    # ---- long-format CSV: one row per bank-year, every source side by side
    # Column 4 is the HEADLINE ROA and is now struck on AVERAGE assets (user,
    # 2026-10-10: the denominator is the average, for ROA as well as ROE). The
    # year-end variant is appended rather than inserted, because the rows
    # below are built and read positionally and an insert would silently
    # reassign every column after it.
    # `desk_research_*` was called `published_*` until 2026-10-10. The rename
    # is the point of the user's decision, not cosmetic: that column holds
    # THIRD-PARTY desk research, and calling it "published" invited exactly
    # the confusion that let its transposed United Trust Bank years stand.
    # What the BANK itself publishes is `own_published_*`, at the end.
    cols = ["bank", "year", "roe_pct_avg_equity", "roe_pct_year_end",
            "roa_pct_avg_assets",
            "profit_after_tax", "total_equity", "total_assets", "equity_prior_year",
            "unit", "profit_row_label", "equity_row_label", "assets_row_label",
            "desk_research_roe_pct", "desk_research_roe_measure",
            "aggregator_roe_pct", "aggregator_roa_pct", "aggregator_url",
            "delta_computed_minus_desk_research_pp", "gap_reason", "roe_caveat",
            "period_or_entity_flag", "pl_year_label",
            "roa_pct_year_end", "assets_prior_year",
            "own_published_value", "own_published_measure",
            "own_published_definition", "own_published_verification",
            "own_published_source",
            # Appended 2026-10-22. New columns go at the END: the sheet builders
            # below address out_rows POSITIONALLY (r[4], r[15], r[16], r[17],
            # r[20] among others), so inserting a column anywhere earlier
            # silently rewires every one of them.
            "aggregator_verification", "aggregator_source",
            "aggregator_disagreement"]
    out_rows = []
    for b in banks:
        for y in YEARS:
            r = idx[(b, y)]
            p = pub.get((b, y), (None, ""))
            ar = agg.get((b, y, "ROE")) or {}
            aa = agg.get((b, y, "ROA")) or {}
            delta = (round(r["roe_avg_equity"] - p[0], 2)
                     if r["roe_avg_equity"] is not None and p[0] is not None else None)
            # A missing year next to a longer-than-12-month column is not a gap
            # at all: the bank changed its year-end and that year has no
            # separate reporting period. Clydesdale is the case here - its
            # 18-month FY2025 absorbs FY2024 - and calling it a gap would send
            # someone hunting for a document that cannot exist.
            # Only the year IMMEDIATELY before the long column is absorbed by
            # it. Griffin's 15-month FY2023 reaches back into FY2022 and no
            # further - its FY2021 is missing because the bank was not yet
            # licensed, which is a different fact and must not be relabelled.
            nxt = idx.get((b, "FY" + str(int(y[2:]) + 1)), {})
            nlab = nxt.get("pl_year_label") or ""
            absorbed = (r.get("pl_year_label") is None and bool(nlab)
                        and re.search(r"\(\s*\d+\s*m", nlab, re.I) is not None)
            reason = ""
            # The year-end variant is the right test for "is an INPUT missing":
            # the average additionally needs a prior-year balance sheet, and its
            # absence in a bank's oldest reported year is not a gap to chase.
            if r["roa_year_end"] is None:
                if absorbed:
                    reason = ("no such reporting period - an adjacent column covers more than "
                              "12 months, so this year was never reported separately. NOT a gap "
                              "to chase; see Period and entity flags.")
                elif r["profit_after_tax"] is None and r["total_assets"] is None:
                    reason = "no statement figures for this year in the workbook"
                elif r["total_assets"] is None:
                    reason = "total assets not matched"
                else:
                    reason = "profit after tax not matched"
            elif r["roe_avg_equity"] is None and r["roe_year_end"] is not None:
                reason = "average-equity basis needs the prior year; year-end basis given"
            # A ratio whose denominator sits near zero is arithmetic noise, not
            # a return: Afin Bank's equity crosses from +46,830 to -35,786, so
            # its average equity is 5,522 and the ROE prints as -7,361%. The
            # figure is kept - suppressing a computed value would be the same
            # sin as back-solving one - but it is labelled, because an
            # unlabelled -7,361% in a column of single digits misleads at a
            # glance and will poison any mean or chart built off this file.
            # The column header is the only place a non-12-month period or an
            # entity switch is recorded, and the year key "FY2025" hides both.
            # A return ratio divides a PERIOD figure (profit) by a POINT-IN-TIME
            # one (equity, assets), so an 18-month numerator inflates it by half
            # again - and Clydesdale, Griffin and StreamBank each have one
            # inside this window.
            pflag = ""
            lab = r.get("pl_year_label") or r.get("bs_year_label") or ""
            rest = re.sub(r"\s*\([^()]*\)\s*$", "", lab).replace(y, "", 1).strip()
            if rest and PERIOD_RISK.search(rest):
                if re.search(r"\d+\s*m", rest, re.I):
                    pflag = ("NOT a 12-month period: %s. Profit covers this period while equity "
                             "and assets are point-in-time, so the ratio is not comparable to "
                             "the bank's other years or to other banks." % rest)
                else:
                    pflag = ("reporting entity or basis differs for this column: %s - check it "
                             "is the same entity as the adjacent years before comparing" % rest)
            cav = ""
            eq, pe = r["total_equity"], r["equity_prior_year"]
            if r["roe_avg_equity"] is not None and eq is not None and pe is not None:
                avg = (eq + pe) / 2.0
                if (eq < 0) != (pe < 0):
                    cav = ("equity changed sign between the two year-ends - the average-equity "
                           "denominator passes through zero and the ratio is not interpretable")
                elif eq < 0:
                    cav = "negative equity in both years - sign of the ratio is not meaningful"
                elif r["profit_after_tax"] and abs(avg) < 0.1 * abs(r["profit_after_tax"]):
                    cav = "average equity is small relative to profit - ratio is unstable"
                elif abs(r["roe_avg_equity"]) > 100:
                    cav = "magnitude over 100% - check the equity base before quoting"
            o = own.get((b, y), [])
            # Several measures can coexist for one bank-year (a ROE and a
            # RoTE). They are joined rather than one being chosen, because
            # picking one would hide that the bank published both.
            ov = " | ".join(str(x.get("value")) for x in o) or None
            om = " | ".join(str(x.get("measure")) for x in o) or None
            od = " | ".join(str(x.get("definition") or "(none stated)") for x in o) or None
            oves = " | ".join(str(x.get("verification")) for x in o) or None
            osrc = " | ".join(str(x.get("source")) for x in o) or None
            out_rows.append([b, y, r["roe_avg_equity"], r["roe_year_end"],
                             r["roa_avg_assets"],
                             r["profit_after_tax"], r["total_equity"], r["total_assets"],
                             r["equity_prior_year"], r["unit"], r["profit_row"],
                             r["equity_row"], r["assets_row"], p[0], p[1],
                             ar.get("value"), aa.get("value"),
                             ar.get("url") or aa.get("url") or "",
                             delta, reason, cav,
                             pflag, lab,
                             r["roa_year_end"], r["assets_prior_year"],
                             ov, om, od, oves, osrc,
                             ar.get("verification") or aa.get("verification"),
                             ar.get("source") or aa.get("source"),
                             ar.get("disagreement") or aa.get("disagreement")])
    with open(outbase + ".csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(cols)
        w.writerows(out_rows)

    # ---- Excel
    wb = openpyxl.Workbook()
    wb.remove(wb.active)

    cov = {y: (sum(1 for b in banks if idx[(b, y)]["roe_avg_equity"] is not None),
               sum(1 for b in banks if idx[(b, y)]["roa_avg_assets"] is not None)) for y in YEARS}
    readme = [
        ["UK bank profitability - ROE and ROA", ""],
        ["Built", TODAY],
        ["Banks", len(banks)],
        ["Years", ", ".join(reversed(YEARS))],
        ["", ""],
        ["WHAT THIS IS", "ROE and ROA for the UK bank corpus, COMPUTED from the figures already "
         "transcribed and verified in banks/*.xlsx - each bank's own Profit & Loss and Balance "
         "Sheet. No workbook was modified to produce this."],
        ["THE ONE RULE", "Three sources, three columns, never merged. A figure we computed, a "
         "figure the prior desk research recorded, and a figure an aggregator publishes are "
         "different claims. They sit side by side so a disagreement stays visible; none is "
         "averaged into another and none silently fills in for another."],
        ["ROE BASIS", "Two bases are given and they are NOT interchangeable. 'avg equity' = "
         "profit after tax / average of opening and closing equity - the standard definition, "
         "and the one that reproduces published ROE best. 'year end' = profit / closing equity, "
         "which needs no prior year and so covers more bank-years. Pick one and stay on it; "
         "mixing them within a series is the mixed-basis trap."],
        ["WHAT IS NOT HERE", "Nothing is back-solved and nothing is derived from a ratio. Every "
         "value is profit / equity or profit / assets using figures printed in the bank's own "
         "accounts. Where an input is missing the cell is EMPTY and the Gaps sheet says why."],
        ["ENTITY", "Every computed figure is on the UK entity perimeter, because the workbooks "
         "it is computed from already are. This matters: UK_Banks_Key_Metrics.xlsx caveat 4 "
         "states its figures for Lloyds, NatWest, Barclays, HSBC and Santander are GROUP "
         "figures, which is contrary to this project's entity rule - so nothing was imported "
         "from it. (It is in any case a populated template: every data cell reads 'n/d'.)"],
        ["", ""],
        ["COVERAGE", "year / ROE (avg equity) / ROA, out of %d banks" % len(banks)],
    ] + [["  " + y, "ROE %d    ROA %d" % cov[y]] for y in YEARS]
    ws = sheet(wb, "Read me", ["Field", "Value"], readme, [26, 118])
    for row in ws.iter_rows(min_row=2, max_col=2):
        row[1].alignment = Alignment(wrap_text=True, vertical="top")

    # ROE values with a denominator problem are EXCLUDED from the headline ROE
    # sheets (user decision, 2026-10-08) rather than printed beside ordinary
    # ones. They are not deleted: the figure, its equity base and the reason
    # stay on the ROE caveats sheet and in the Detail sheet, so the file still
    # says what was found and why it is not shown here.
    excluded = {(r[0], r[1]) for r in out_rows if r[20]}
    for metric, key, label in [("ROE", "roe_avg_equity", "Return on equity, % (profit after tax / AVERAGE equity)"),
                               ("ROE year-end", "roe_year_end", "Return on equity, % (profit after tax / closing equity)"),
                               ("ROA", "roa_avg_assets", "Return on assets, % (profit after tax / AVERAGE total assets)"),
                               ("ROA year-end", "roa_year_end", "Return on assets, % (profit after tax / closing total assets)")]:
        drop = excluded if key.startswith("roe") else set()
        body = [[b] + [None if (b, y) in drop else idx[(b, y)][key] for y in YEARS]
                for b in banks]
        sheet(wb, metric, ["Bank"] + list(YEARS), body, [34] + [12] * len(YEARS),
              note=label + ". Computed from each bank's own transcribed Profit & Loss and "
              "Balance Sheet. An empty cell means an input was missing - see the Gaps sheet "
              "for which one and why; it never means zero.")

    # `sheet()` zips widths against columns, so a short list simply leaves the
    # remaining columns at Excel's default. Widths for the three aggregator
    # provenance columns are given explicitly because `aggregator_disagreement`
    # holds a sentence.
    sheet(wb, "Detail", cols, out_rows,
          [30, 9] + [13] * 3 + [15] * 4 + [16] + [34] * 3 + [13, 18, 13, 13, 30, 14, 42, 50, 60, 24]
          + [22, 40, 24, 26, 60, 22, 34, 54])

    # ---- Definition resolver.
    # A divergence is far more useful explained than merely reported. Most
    # published "ROE" figures that disagree with ours are not errors on either
    # side: they are struck on a different numerator (profit BEFORE tax, or
    # total comprehensive income) or a different denominator (closing rather
    # than average equity), and the label rarely says so. This tests every
    # combination against each outside figure and names the one that
    # reproduces it. Nothing here changes a computed value.
    res = []
    for b in banks:
        for y in YEARS:
            r = idx[(b, y)]
            eq, pe = r["total_equity"], r["equity_prior_year"]
            avg = (eq + pe) / 2.0 if (eq is not None and pe is not None) else None
            nums = [("profit after tax", r["profit_after_tax"]),
                    ("profit BEFORE tax", r.get("profit_before_tax")),
                    ("total comprehensive income", r.get("total_comprehensive_income"))]
            dens = [("average equity", avg), ("closing equity", eq)]
            for src, val, metric in [("prior desk research", pub.get((b, y), (None, ""))[0], "ROE"),
                                     ("thebanks.eu", (agg.get((b, y, "ROE")) or {}).get("value"), "ROE"),
                                     ("thebanks.eu", (agg.get((b, y, "ROA")) or {}).get("value"), "ROA")]:
                if val is None:
                    continue
                hits = []
                if metric == "ROE":
                    for nn, nv in nums:
                        for dn, dv in dens:
                            if nv is not None and dv:
                                got = 100.0 * nv / dv
                                if abs(got - val) <= 0.1:
                                    hits.append("%s / %s = %.2f" % (nn, dn, got))
                else:
                    for nn, nv in nums:
                        if nv is not None and r["total_assets"]:
                            got = 100.0 * nv / r["total_assets"]
                            if abs(got - val) <= 0.05:
                                hits.append("%s / total assets = %.2f" % (nn, got))
                ours = r["roe_avg_equity"] if metric == "ROE" else r["roa_avg_assets"]
                if ours is None or abs(ours - val) < (0.1 if metric == "ROE" else 0.05):
                    continue  # already agrees on our own definition
                delta = round(val - ours, 2) if ours is not None else None
                meas = (pub.get((b, y), (None, ""))[1] or "").strip()
                if hits:
                    verdict = ("RESOLVED - a different definition, not a disagreement about "
                               "any underlying figure")
                elif src == "prior desk research" and meas and meas.upper() not in (
                        "ROE", "REPORTED ROE"):
                    verdict = ("EXPLAINED BY LABEL - their figure is %s, a different metric. "
                               "RoTE and tangible-equity measures cannot be tested here "
                               "because intangibles are not extracted." % meas)
                elif delta is not None and abs(delta) <= 0.5:
                    verdict = ("within 0.5pp - consistent with rounding or a minor "
                               "presentation difference; not worth a document read")
                else:
                    verdict = "LEAD - material and unexplained; needs the bank's own accounts"
                res.append([b, y, metric, src, val, ours, delta,
                            hits[0] if hits else "", verdict])
    res.sort(key=lambda x: (0 if x[8].startswith("LEAD") else
                            1 if x[8].startswith("RESOLVED") else
                            2 if x[8].startswith("EXPLAINED") else 3,
                            -abs(x[6] or 0)))
    sheet(wb, "Definition resolver",
          ["Bank", "Year", "Metric", "Outside source", "Their value", "Our computed value",
           "Delta (pp)", "What reproduces their figure", "Verdict"],
          res, [26, 8, 7, 20, 11, 13, 10, 46, 46],
          note="Read this before treating any divergence as an error. A published 'ROE' is "
               "often struck on profit BEFORE tax, or on total comprehensive income, or on "
               "closing rather than average equity - and the label almost never says which. "
               "Where a combination reproduces the outside figure to within 0.1pp (0.05pp for "
               "ROA) it is named here, and the divergence is a DEFINITIONAL difference, not a "
               "disagreement about any underlying number. Al Rayan is the clearest case: its "
               "three published values reproduce exactly on profit before tax in all three "
               "years. Rows marked unresolved are the ones that still need a document read - "
               "they are the real leads.")

    tb = [r for r in out_rows if r[15] is not None and r[2] is not None]
    tb_rows = []
    for r in tb:
        d_roe = round(r[2] - r[15], 2)
        d_roa = round(r[4] - r[16], 2) if (r[4] is not None and r[16] is not None) else None
        # Which side of the ratio moved tells you where to look. Both ratios
        # shifting by a similar factor points at the NUMERATOR (a different
        # profit figure); ROE moving while ROA holds points at the EQUITY
        # DENOMINATOR. That narrows a document read from "check everything" to
        # one line of one statement.
        diag = ""
        if abs(d_roe) >= 1.0:
            if d_roa is not None and abs(d_roa) < 0.25 * abs(r[16] or 1):
                diag = ("ROA agrees but ROE does not - the difference is in the EQUITY "
                        "denominator, not the profit figure. Check what they counted as equity "
                        "(AT1 and other equity instruments are the usual cause).")
            elif d_roa is not None:
                diag = ("both ratios move in the same direction by a similar factor - the "
                        "difference is in the PROFIT numerator or the entity, not the "
                        "denominator.")
            else:
                diag = "no ROA to compare, so the side of the ratio that differs is unknown."
        tb_rows.append([r[0], r[1], r[2], r[15], d_roe, r[4], r[16], d_roa, diag,
                        r[30], r[32] or "", r[17]])
    tb_rows.sort(key=lambda x: -abs(x[4]))
    sheet(wb, "Vs thebanks.eu",
          ["Bank", "Year", "Computed ROE (avg equity)", "thebanks.eu ROE", "Delta (pp)",
           "Computed ROA", "thebanks.eu ROA", "Delta (pp)", "Where the difference is",
           "How that figure is evidenced", "Snapshots disagree", "URL"],
          tb_rows, [28, 8, 16, 13, 10, 12, 13, 10, 62, 22, 44, 34],
          note="thebanks.eu is an AGGREGATOR: every figure here is what that site says, never "
               "a bank-published figure. The site itself sits behind a Cloudflare challenge "
               "that was NOT bypassed; these figures come from its public search index, its "
               "exact-entity profiles, and Wayback captures of those profiles. "
               "THIS SHEET WAS REBUILT 2026-10-22 and an earlier version of this note said "
               "'every figure it carries is FY2024 - it cannot fill an earlier year'. That is "
               "no longer true and was only ever true of the first 20-bank file: the column now "
               "also covers FY2022 and FY2023, chiefly from Wayback captures, and FY2024 runs "
               "to 141 banks rather than 20. "
               "'How that figure is evidenced' is load-bearing and the four states are NOT "
               "equally strong: a wayback_snapshot has a replay URL and a 14-digit timestamp; "
               "a thebanks_profile or search_indexed record was read from the live site or its "
               "index; an archive_search_indexed record has NEITHER a snapshot URL nor a "
               "timestamp and must never be described as a verified capture. Where two sources "
               "cover one bank-year the stronger evidence is shown and any numeric "
               "disagreement is named in its own column rather than hidden. "
               "Its value is as an INDEPENDENT check, and on that it is reassuring: most of "
               "this sample agrees with our computed figure to 0.00pp, which also tells us the "
               "site computes profit / AVERAGE equity, the same basis. Nothing here was copied "
               "into our own columns. Period caveats: Starling and Monzo have non-December year "
               "ends, so a bare '2024' may not be our FY2024; NBK International's figures are "
               "USD; and thebanks.eu LAGS, so a capture's own date is not its reporting period "
               "- the year stated on the page is used, never the capture date.")

    pf = [r for r in out_rows if r[21]]
    sheet(wb, "Period and entity flags",
          ["Bank", "Year", "Column header as printed", "ROE", "ROA", "Why it needs care"],
          [[r[0], r[1], r[22], r[2], r[4], r[21]] for r in pf], [30, 9, 28, 12, 10, 72],
          note="A return ratio divides a PERIOD figure (profit) by a POINT-IN-TIME figure "
               "(equity, assets). That only works when the period is a normal 12-month year "
               "and the entity is unchanged. These columns are neither, and the year key alone "
               "does not show it - the information exists ONLY in the column header, which is "
               "why it is reproduced here verbatim. Clydesdale's FY2025 is an 18-month "
               "transition period (so the bank has no FY2024 period at all, and its apparent "
               "FY2024 gap is not a gap); Griffin's and StreamBank's FY2023 are 15 months; "
               "Monzo's FY2024 onward report a different entity (MBHG) from FY2023 and earlier "
               "(MBL). Treat every ratio listed here as non-comparable until checked.")

    cavs = [[r[0], r[1], "ROE", "EXCLUDED from the ROE sheets", r[2], r[6], r[8], r[20]]
            for r in out_rows if r[20]]
    # ROA gets a different treatment on purpose. Its denominator, total assets,
    # is always positive and never crosses zero, so every ROA here is a
    # well-defined, correctly-signed number - it is merely huge, because a
    # pre-operational bank burns cash against almost no balance sheet. That is
    # a true fact about the bank, not an artefact of the arithmetic, so these
    # are FLAGGED and kept rather than excluded.
    cavs += [[r[0], r[1], "ROA", "shown, flagged only", r[4], r[7], None,
              "magnitude over 25%% - the bank was pre-operational or barely trading "
              "(assets %s against profit %s), so the ratio is well-defined but not "
              "comparable with an established bank" % (r[7], r[5])]
             for r in out_rows if r[4] is not None and abs(r[4]) > 25]
    sheet(wb, "Ratio caveats", ["Bank", "Year", "Metric", "Treatment", "Computed value",
                                "Denominator", "Prior-year equity",
                                "Why the figure needs reading with care"],
          cavs, [28, 8, 8, 26, 13, 16, 16, 62],
          note="These ROE values are EXCLUDED from the ROE and ROE year-end sheets, where their "
               "cells are left empty. They are arithmetically correct but each has a "
               "denominator problem that makes the percentage meaningless on its own - almost "
               "always a young bank whose equity is near zero or crossing it, so the ratio "
               "measures the smallness of the equity base rather than any return. They are kept "
               "here, with the equity base that produced them, because deleting a computed "
               "figure without trace would leave no way to tell an excluded value from one that "
               "was never computed. ROA is treated differently and deliberately so - see the "
               "Treatment column. Total assets is always positive and never crosses zero, so "
               "every ROA is well-defined and correctly signed; a figure like Afin Bank's "
               "-2,794% in FY2022 reports a real fact (a GBP 406,520 loss against a GBP 14,552 "
               "balance sheet), not an arithmetic artefact. Those stay visible and are only "
               "flagged. Both groups are overwhelmingly young banks before they began trading.")

    comp = [r for r in out_rows if r[13] is not None and r[2] is not None]
    comp.sort(key=lambda r: -abs(r[18]))
    # ---- what the BANKS THEMSELVES publish (user decision, 2026-10-10)
    # Deliberately NOT a bank x year grid like the computed sheets. A grid
    # would line these up under one column heading and so assert they are one
    # measure, which is the one thing that is not true of them: each is struck
    # on its own bank's definition. One row per published figure, with the
    # definition and the verification state beside it.
    own_rows = []
    for rec in sorted(own_all, key=lambda x: (x.get("bank") or "", x.get("year") or "")):
        def flags(r):
            if r.get("excluded") or r.get("publishes_none"):
                return ("", "")
            oe = "own edition" if r.get("own_edition") else "LATER EDITION'S COMPARATIVE"
            cw = ("YES - same definition as ours"
                  if r.get("comparable_with_computed")
                  else "no - different definition")
            return (oe, cw)

        oe, cw = flags(rec)
        if rec.get("publishes_none"):
            own_rows.append([rec.get("bank"), rec.get("year"), "(publishes none)",
                             None, None, rec.get("verification"), oe, cw,
                             rec.get("finding"), rec.get("entity"),
                             rec.get("source") or ""])
            continue
        own_rows.append([
            rec.get("bank"), rec.get("year"),
            ("EXCLUDED - " + (rec.get("measure") or "")) if rec.get("excluded")
            else rec.get("measure"),
            rec.get("value"),
            rec.get("definition") or "(no definition stated in the document)",
            rec.get("verification"), oe, cw,
            rec.get("finding") or rec.get("differs_from_computed") or rec.get("note") or "",
            rec.get("entity"), rec.get("source") or ""])
    sheet(wb, "Own published returns",
          ["Bank", "Year", "Measure as the bank labels it", "Value as printed",
           "The bank's own stated definition", "Verification", "Own edition?",
           "Comparable with our computed ROE?",
           "What it tells us / how it differs from ours", "Entity", "Source"],
          own_rows, [26, 9, 26, 13, 44, 13, 26, 30, 60, 34, 52],
          note="THE BANK'S OWN FIGURE, and not comparable with the computed ROE/ROA sheets. "
               "Each is struck on its own bank's definition and those genuinely differ - Al "
               "Rayan's 'Return on equity' is profit BEFORE tax over average equity, United "
               "Trust's is net of the coupon on contingent convertible securities. That is why "
               "the definition travels with the figure and why these are never merged into the "
               "computed columns. READ THE VERIFICATION COLUMN: 'ocr_lead' means the figure was "
               "read off a text layer or a low-resolution contact sheet and has NOT been "
               "confirmed on a 300 dpi render, which is this project's standard - it is a lead, "
               "not a finding. 'EXCLUDED' rows are outside figures identified as belonging to a "
               "DIFFERENT entity (usually a group rather than the bank in this workbook's "
               "perimeter) and are recorded so nobody re-derives them. A '(publishes none)' row "
               "is a positive finding: that bank publishes no return at all, so the computed "
               "figure is the only one there is.")

    sheet(wb, "Vs prior research",
          ["Bank", "Year", "Computed ROE (avg equity)", "Prior research value",
           "Measure as labelled there", "Delta (pp)"],
          [[r[0], r[1], r[2], r[13], r[14], r[18]] for r in comp],
          [30, 9, 16, 14, 22, 11],
          note="Sorted by absolute delta. READ THE AGREEMENT CAREFULLY - it is partly "
               "circular. The prior research file's values appear to have been computed the "
               "same way (profit / average equity) by an aggregator, so close agreement "
               "confirms our transcriptions match that aggregator; it does NOT independently "
               "confirm either against the bank's own published ROE. The large deltas are the "
               "informative part, and most are explained by the Measure column: RoTE, ROAE and "
               "PBT ROE are different metrics, not disagreements about the same one.")

    gaps = [r for r in out_rows if r[19]]
    sheet(wb, "Gaps", ["Bank", "Year", "What is missing", "ROE year-end (if available)"],
          [[r[0], r[1], r[19], r[3]] for r in gaps], [30, 9, 60, 16],
          note="Most of these are STRUCTURAL, not failures of reach: the bank did not exist or "
               "was not yet licensed in that year, or its accounts for the newest year are not "
               "filed yet. An aggregator cannot fill a year a bank never reported. The rows "
               "worth chasing are those where a year is missing in the MIDDLE of an otherwise "
               "complete series.")

    unm = d.get("unmatched", [])
    sheet(wb, "Unmatched inputs",
          ["Bank", "Missing input", "Note"],
          [[u["bank"], ", ".join(u["missing"]), ""] for u in unm], [30, 20, 70],
          note="Banks where a required statement row could not be matched by label. These are "
               "listed rather than dropped, because a silent drop is indistinguishable from a "
               "bank that genuinely does not disclose the line.")

    wb.save(outbase + ".xlsx")
    print(f"wrote {outbase}.csv and {outbase}.xlsx")
    print(f"  {len(banks)} banks x {len(YEARS)} years = {len(out_rows)} rows")
    print(f"  vs prior research: {len(comp)} comparable pairs")
    print(f"  gaps: {len(gaps)}   unmatched-input banks: {len(unm)}")
    print(f"  aggregator values merged: {len(agg)}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3], *sys.argv[4:])
