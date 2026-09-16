#!/usr/bin/env python3
"""Corpus-wide arithmetic tie-out audit of the statement sheets.

For every bank workbook in banks/, every statement-shaped sheet (Balance
Sheet, Profit & Loss, Cash Flow Statement, Asset Quality, RWA Breakdown) and
every year column, check that each TOTAL-tagged row equals the sum of the
DATA-tagged rows it subtotals.

Row kinds are recovered from the saved workbook exactly as
``bank_workbook._add_statement_sheet`` writes them:

    SECTION -> bold in column 1 only, no values
    TOTAL   -> bold in every column
    DATA    -> not bold

Because a naive "sum every DATA row since the last divider" rule produces
spurious gaps wherever a statement nests its subtotals, each TOTAL is tested
against several candidate compositions and is only reported as a mismatch
when none of them fits:

    A  DATA rows since the last boundary (SECTION divider or TOTAL row)
    B  DATA rows since the last SECTION divider, ignoring nested TOTALs
    C  the last preceding TOTAL, plus the DATA rows after it
       (e.g. Total equity = Equity attributable to owners + NCI)
    D  any small subset of the preceding TOTAL rows, optionally plus the
       DATA rows since the last boundary (e.g. Total equity and liabilities
       = Total liabilities + Total equity)

Sign conventions differ between statements (a source may print expenses as
positive numbers under a negative total), so a candidate that fits after
negating the sum is recorded as a sign-convention tie rather than a defect.

"Of which" rows are subsets of the line above and are never added in.

Usage:
    python3 scripts/insights/tieout_check.py --out research/tieout_sweep.json
"""

import argparse
import glob
import json
import os
import re
import sys
from itertools import combinations

import openpyxl

STATEMENT_SHEETS = [
    "Balance Sheet",
    "Profit & Loss",
    "Cash Flow Statement",
    "Asset Quality",
    "RWA Breakdown",
]

# Rows that are a SUBSET of the line above them and must never be summed in.
OF_WHICH_RE = re.compile(
    r"^\s*[-–—•]?\s*(of\s+which|o/w|thereof|which:|whereof|comprising|"
    r"including|includes)\b",
    re.I,
)

# Rows that are a memo/ratio annotation rather than a component of the total.
MEMO_RE = re.compile(
    r"^\s*[-–—•]?\s*(memo(randum)?\b|ratio\b|coverage ratio|npl ratio|"
    r"cost[- ]to[- ]income)",
    re.I,
)

# A DATA row that announces itself as a subtotal of the rows around it.
TOTALISH_RE = re.compile(r"^\s*total\b", re.I)

HEADER_ROW = 3
FIRST_DATA_ROW = 4


def _num(v):
    """Return a float for a numeric cell, else None. String ratio cells
    ("13.55%") and text ("Not publicly disclosed") are not components."""
    if isinstance(v, bool):
        return None
    if isinstance(v, (int, float)):
        return float(v)
    return None


def read_sheet(ws):
    """Return (years, rows) where rows is a list of dicts with kind/label/values."""
    ncols = ws.max_column
    years = []
    for c in range(2, ncols + 1):
        h = ws.cell(HEADER_ROW, c).value
        if h is None:
            break
        years.append((c, str(h)))

    rows = []
    for r in range(FIRST_DATA_ROW, ws.max_row + 1):
        label = ws.cell(r, 1).value
        if label is None:
            continue
        label = str(label)
        # the merged source-citation cell is the last row; it is long prose
        if label.lstrip().lower().startswith("source") or len(label) > 300:
            continue
        bold1 = bool(ws.cell(r, 1).font and ws.cell(r, 1).font.bold)
        bold2 = bool(ws.cell(r, 2).font and ws.cell(r, 2).font.bold)
        vals = {}
        raw = {}
        for c, y in years:
            v = ws.cell(r, c).value
            raw[y] = v
            n = _num(v)
            if n is not None:
                vals[y] = n
        if bold1 and bold2:
            kind = "TOTAL"
        elif bold1:
            kind = "SECTION"
        else:
            kind = "DATA"
        # A bold-col-1-only row that nonetheless carries values is a section
        # divider in name only; treat it as DATA so its figures are not lost.
        if kind == "SECTION" and vals:
            kind = "DATA"
        rows.append(
            {
                "row": r,
                "kind": kind,
                "label": label,
                "values": vals,
                "raw": raw,
                "of_which": bool(OF_WHICH_RE.match(label)),
                "memo": bool(MEMO_RE.match(label)),
                "child": False,
                "has_children": False,
            }
        )
    mark_breakdown_children(rows)
    return [y for _, y in years], rows


def _run_ties(rows, parent, idxs, require=2):
    """True if the DATA rows at idxs sum to rows[parent] in every year where
    the parent and all of them carry a figure.

    `require` is the minimum number of such years. Demanding two guards
    against a coincidental single-year match between sparse rows, which is
    how a genuine peer line item gets wrongly written off as a breakdown."""
    hits = 0
    for year, pv in rows[parent]["values"].items():
        # A breakdown row that is blank in a given year simply does not apply
        # that year (a line the source introduced or dropped mid-series).
        # Requiring every row to be populated in every year would mean one
        # permanently-blank line - BNY Mellon carries an all-blank "Treasury"
        # investment-securities row - defeats the whole match.
        present = [j for j in idxs if year in rows[j]["values"]]
        if len(present) < 2:
            continue
        s = sum(rows[j]["values"][year] for j in present)
        if abs(pv - s) > max(1.0, 0.5 * len(present) + 0.5, abs(pv) * 0.0005):
            return False
        hits += 1
    return hits >= require


def mark_breakdown_children(rows):
    """Flag DATA rows that are the itemised breakdown of another DATA row,
    so a section sum counts the parent once instead of parent + components.

    This is the NBE shape: a breakdown block carrying both its category rows
    and its own total, all tagged DATA. Detected arithmetically - a
    contiguous run of DATA rows that sums to the DATA row immediately before
    or immediately after it, in every year the two share - rather than by
    label, so it catches breakdowns whose parent is not called "Total ...".
    """
    n = len(rows)

    def run_from(start, direction):
        """Contiguous DATA row indexes moving `direction` from `start`."""
        out = []
        j = start
        while 0 <= j < n and rows[j]["kind"] == "DATA" and not rows[j]["child"]:
            if not rows[j]["of_which"] and not rows[j]["memo"]:
                out.append(j)
            j += direction
        return out

    for i in range(n):
        if rows[i]["kind"] != "DATA" or rows[i]["child"] or not rows[i]["values"]:
            continue
        # children immediately after the parent
        # A one-row "breakdown" is only meaningful where the parent announces
        # itself as a total ("Total debt securities" over a single
        # undisclosed-split line); otherwise a lone equal neighbour is noise.
        totalish = bool(TOTALISH_RE.match(rows[i]["label"]))
        floor = 1 if totalish else 2
        require = 1 if totalish else 2

        def longest_tie(run):
            for L in range(len(run), floor - 1, -1):
                if _run_ties(rows, i, run[:L], require):
                    return run[:L]
            return None

        # A parent can carry MORE THAN ONE breakdown of itself, stacked -
        # a presentation that changed mid-series leaves both eras' splits on
        # the sheet (Monzo's "Total treasury investments" is itemised BOTH by
        # measurement basis and by issuer; United National's "Total debt
        # securities" by AFS/HTM for the recent years and by counterparty
        # type for FY2021). Marking only the first one double-counts the
        # rest into Total assets, so keep consuming the run.
        remainder = run_from(i + 1, 1)
        marked = False
        while len(remainder) >= floor:
            hit = longest_tie(remainder)
            if not hit:
                break
            for j in hit:
                rows[j]["child"] = True
            marked = True
            remainder = remainder[len(hit):]
        if not marked:
            before = list(reversed(run_from(i - 1, -1)))
            for L in range(len(before), floor - 1, -1):
                if _run_ties(rows, i, before[-L:], require):
                    for j in before[-L:]:
                        rows[j]["child"] = True
                    break

    # A subtotal printed ABOVE its own components: a TOTAL row whose figure is
    # the sum of the contiguous DATA run that FOLLOWS it (Griffin Bank prints
    # "Total debt securities" above its two FVTPL lines). Only the forward
    # direction is considered - the rows BEFORE a TOTAL are its ordinary
    # components, and marking those as children would empty every section.
    for i in range(n):
        if rows[i]["kind"] != "TOTAL" or not rows[i]["values"]:
            continue
        run = []
        j = i + 1
        while j < n and rows[j]["kind"] == "DATA" and not rows[j]["child"]:
            if not rows[j]["of_which"] and not rows[j]["memo"]:
                run.append(j)
            j += 1
        for L in range(len(run), 1, -1):
            if _run_ties(rows, i, run[:L], require=1):
                for j in run[:L]:
                    rows[j]["child"] = True
                rows[i]["has_children"] = True
                break


NET_RE = re.compile(r"\bnet\b|\bcarrying\b|\bless\b|-\s*total", re.I)


def candidates(rows, i, year):
    """Yield (name, components) candidate compositions for the TOTAL at index
    i, most-structural first. `components` is a list of (row_index, sign)."""
    # walk back for boundaries
    last_section = None
    last_total = None
    for j in range(i - 1, -1, -1):
        if rows[j]["kind"] == "TOTAL" and last_total is None:
            last_total = j
        if rows[j]["kind"] == "SECTION" and last_section is None:
            last_section = j
        if last_total is not None and last_section is not None:
            break
    boundary = max(x for x in (last_section, last_total, -1) if x is not None)

    def data_between(lo, hi):
        return [
            j
            for j in range(lo + 1, hi)
            if rows[j]["kind"] == "DATA"
            and not rows[j]["of_which"]
            and not rows[j]["memo"]
            and not rows[j]["child"]
            and year in rows[j]["values"]
        ]

    def blanks_between(lo, hi):
        """DATA rows in the span that carry NO figure for this year - the
        difference between "this total is wrong" and "this column is
        sparse"."""
        return sum(
            1
            for j in range(lo + 1, hi)
            if rows[j]["kind"] == "DATA"
            and not rows[j]["of_which"]
            and not rows[j]["memo"]
            and not rows[j]["child"]
            and year not in rows[j]["values"]
        )

    def plus(idxs):
        return [(j, 1) for j in idxs]

    # G: this TOTAL is printed ABOVE its own components, so they are the
    # marked child run that FOLLOWS it, not anything behind it.
    if rows[i].get("has_children"):
        g = []
        j = i + 1
        while j < len(rows) and rows[j]["kind"] == "DATA" and rows[j]["child"]:
            if year in rows[j]["values"]:
                g.append(j)
            j += 1
        if g:
            yield "G", plus(g)

    a = data_between(boundary, i)
    candidates.blanks = blanks_between(boundary, i)
    yield "A", plus(a)

    sec = last_section if last_section is not None else -1
    b = data_between(sec, i)
    yield "B", plus(b)

    # C: roll a preceding subtotal forward. Only when there are real DATA
    # rows after it - otherwise an empty section (a year where the ECL stage
    # rows are blank) would silently "compose" its total out of the previous
    # section's total, which is how a 31,000% phantom gap gets generated.
    if last_total is not None and year in rows[last_total]["values"]:
        tail_c = data_between(last_total, i)
        if tail_c:
            yield "C", plus([last_total] + tail_c)

    # D: subsets of preceding TOTAL rows in this sheet (grand totals)
    prior_totals = [
        j for j in range(0, i) if rows[j]["kind"] == "TOTAL" and year in rows[j]["values"]
    ]
    prior_totals = prior_totals[-6:]
    tail = data_between(boundary, i)
    for k in (1, 2, 3, 4):
        for combo in combinations(prior_totals, k):
            yield "D", plus(list(combo) + tail)
            # ...and without the trailing DATA rows: a cash flow statement
            # routinely prints the FX-effect line BETWEEN the financing
            # subtotal and the net-movement line without including it there
            # (RBC Europe), so the net movement is the section nets alone.
            if tail:
                yield "D", plus(list(combo))

    # F: the flat read since the last SECTION divider, but with a nested
    # subtotal counted ONCE as a unit rather than expanded into its own
    # components (Griffin Bank: Total assets = cash + Total debt securities
    # + receivables + intangibles + PPE, where Total debt securities is
    # itself a TOTAL row sitting above its own two DATA lines).
    f = [
        j
        for j in range(sec + 1, i)
        if not rows[j]["child"]
        and not rows[j]["of_which"]
        and not rows[j]["memo"]
        and year in rows[j]["values"]
        and rows[j]["kind"] in ("DATA", "TOTAL")
    ]
    if f and f != a and f != b:
        yield "F", plus(f)

    # H: the components sit ABOVE their subtotal but are only PART of the
    # span since the last boundary - a mid-section subtotal (Chetwood's
    # "Investment in debt securities - total" closes the two debt-securities
    # lines directly above it, not the whole asset block).
    for k in range(len(a) - 1, 1, -1):
        yield "H", plus(a[-k:])

    # E: DIFFERENCES, not sums. "Net carrying amount" / "Net loans and
    # advances" / "Net lending assets" rows on the Asset Quality sheet are
    # gross MINUS the ECL total; "Net fee and commission income" is income
    # minus expense. Summing them is guaranteed to miss by ~100%.
    for x, y2 in combinations(prior_totals, 2):
        yield "E", [(y2, 1), (x, -1)]
        yield "E", [(x, 1), (y2, -1)]
        # ...less the intervening DATA rows (Methodist Chapel Aid's
        # "Net Assets" = Total Assets - Total Liabilities - Deferred tax,
        # where the deferred-tax provision sits in its own little section)
        if tail:
            yield "E", [(y2, 1), (x, -1)] + [(j, -1) for j in tail]
            yield "E", [(x, 1), (y2, -1)] + [(j, -1) for j in tail]
    if len(a) >= 2:
        yield "E", [(a[0], 1)] + [(j, -1) for j in a[1:]]
        yield "E", plus(a[:-1]) + [(a[-1], -1)]
    if len(b) >= 2 and b != a:
        yield "E", [(b[0], 1)] + [(j, -1) for j in b[1:]]


def tolerance(total, n):
    """Rounding tolerance: half a unit per summed row, floor 1.0, plus a
    0.05% relative allowance for sources printed in a coarser unit."""
    return max(1.0, 0.5 * n + 0.5, abs(total) * 0.0005)


def demote_leaf_totals(rows, years):
    """Un-tag TOTAL rows that are really bolded leaf line items.

    A source sometimes emphasises an ordinary line (FCE Bank's "Operating
    expenses" sits between "Allowance for ECL" and "Profit before tax" and is
    a peer of both, not their subtotal). Left tagged TOTAL it produces a
    guaranteed false positive AND breaks the subtotal below it. The tell is
    that it never has more than one candidate component and never ties in any
    year. Returns the list of demoted row labels."""
    demoted = []
    for i, row in enumerate(rows):
        if row["kind"] != "TOTAL":
            continue
        ties = False
        max_comp = 0
        for year in years:
            if year not in row["values"]:
                continue
            for name, comps in candidates(rows, i, year):
                if not comps:
                    continue
                if name in ("A", "B", "C"):
                    max_comp = max(max_comp, len(comps))
                total = sum(sg * rows[j]["values"][year] for j, sg in comps)
                tol = tolerance(row["values"][year], len(comps))
                if (abs(row["values"][year] - total) <= tol
                        or abs(row["values"][year] + total) <= tol):
                    ties = True
                    break
            if ties:
                break
        # A subtotal printed ABOVE its own components has nothing to
        # subtotal behind it; demoting it would double-count it AND its
        # components into the section total below.
        if row.get("has_children"):
            continue
        if not ties and max_comp <= 1:
            row["kind"] = "DATA"
            row["leaf_total"] = True
            demoted.append(row["label"])
    return demoted


def check_workbook(path):
    wb = openpyxl.load_workbook(path, data_only=True)
    bank = os.path.basename(path).replace(" FINANCIALS.xlsx", "")
    results = []
    leaf_notes = []
    for sheet in STATEMENT_SHEETS:
        if sheet not in wb.sheetnames:
            continue
        ws = wb[sheet]
        unit = str(ws.cell(2, 1).value or "")
        years, rows = read_sheet(ws)
        for lbl in demote_leaf_totals(rows, years):
            leaf_notes.append({"bank": bank, "sheet": sheet, "label": lbl})
        for i, row in enumerate(rows):
            if row["kind"] != "TOTAL":
                continue
            for year in years:
                if year not in row["values"]:
                    continue
                total = row["values"][year]
                n_blank = 0
                structural = []  # non-empty A/B/C, for the fallback residual
                fit = None
                for name, comps in candidates(rows, i, year):
                    if name == "A":
                        n_blank = candidates.blanks
                    if not comps:
                        continue
                    s = sum(sg * rows[j]["values"][year] for j, sg in comps)
                    resid = total - s
                    tol = tolerance(total, len(comps))
                    if name in ("A", "B", "C"):
                        structural.append((name, comps, s, resid))
                    if abs(resid) <= tol:
                        fit = (name, comps, s, resid, False)
                        break
                    # A whole-section sign flip (a source printing expenses
                    # positive under a negative total) is a presentation
                    # convention, not a defect - but only for the plain-sum
                    # candidates. E already explores signs explicitly, so
                    # accepting a flip there would fit almost anything.
                    if name != "E" and abs(total + s) <= tol:
                        fit = (name, comps, s, total + s, True)
                        break
                if fit is None and not structural:
                    # a TOTAL with nothing above it to subtotal (a lone
                    # headline figure under a divider, or a grand total whose
                    # own components are on another sheet)
                    results.append(
                        {
                            "bank": bank,
                            "sheet": sheet,
                            "unit": unit,
                            "year": year,
                            "row": row["row"],
                            "label": row["label"],
                            "total": total,
                            "sum": None,
                            "residual": None,
                            "pct": None,
                            "candidate": None,
                            "n_comp": 0,
                            "n_blank": n_blank,
                            "components": [],
                            "status": "NO_COMPONENTS",
                        }
                    )
                    continue
                if fit is not None:
                    name, comps, s, resid, signed = fit
                    status = "TIES" if not signed else "TIES_SIGN"
                    if name != "A":
                        status = "TIES_NESTED" if not signed else "TIES_NESTED_SIGN"
                    if abs(resid) > 1e-9 and status == "TIES":
                        status = "TIES_ROUNDING"
                else:
                    # report the most charitable STRUCTURAL reading: a residual
                    # that survives every sane composition is the real finding
                    name, comps, s, resid = min(
                        structural, key=lambda e: abs(e[3])
                    )
                    # A residual larger than the total itself, or a sum of the
                    # opposite sign, means the composition this checker chose
                    # is almost certainly not the one the statement intends.
                    # That is a question for a human, not a figure defect.
                    opposite = s * total < 0 and abs(s) > 1 and abs(total) > 1
                    if opposite or (total and abs(resid) / abs(total) > 1.0):
                        status = "STRUCTURE_UNCLEAR"
                    else:
                        status = "MISMATCH"
                results.append(
                    {
                        "bank": bank,
                        "sheet": sheet,
                        "unit": unit,
                        "year": year,
                        "row": row["row"],
                        "label": row["label"],
                        "total": total,
                        "sum": s,
                        "residual": resid,
                        "pct": (abs(resid) / abs(total) * 100.0) if total else None,
                        "candidate": name,
                        "n_comp": len(comps),
                        "n_blank": n_blank,
                        "components": [
                            ("" if sg > 0 else "-") + rows[j]["label"]
                            for j, sg in comps
                        ],
                        "status": status,
                    }
                )
    wb.close()
    return results, leaf_notes


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--banks-dir", default="banks")
    ap.add_argument("--out", default="research/tieout_sweep.json")
    ap.add_argument("--only", help="substring filter on workbook filename")
    args = ap.parse_args()

    paths = sorted(glob.glob(os.path.join(args.banks_dir, "*.xlsx")))
    paths = [p for p in paths if not os.path.basename(p).startswith("~$")]
    if args.only:
        paths = [p for p in paths if args.only.lower() in os.path.basename(p).lower()]

    all_results = []
    all_leaves = []
    for p in paths:
        try:
            res, leaves = check_workbook(p)
            all_results.extend(res)
            all_leaves.extend(leaves)
        except Exception as e:  # noqa: BLE001
            print(f"ERROR {p}: {e}", file=sys.stderr)
    tmp = args.out + ".tmp"
    with open(tmp, "w") as fh:
        json.dump({"checks": all_results, "leaf_totals": all_leaves}, fh, indent=1)
    os.replace(tmp, args.out)

    from collections import Counter

    c = Counter(r["status"] for r in all_results)
    print(f"workbooks: {len(paths)}  checks: {len(all_results)}  "
          f"bolded-leaf TOTALs demoted: {len(all_leaves)}")
    for k, v in c.most_common():
        print(f"  {k:20s} {v}")
    print(f"written: {args.out}")


if __name__ == "__main__":
    main()
