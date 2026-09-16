#!/usr/bin/env python3
"""Render the tie-out sweep JSON into the ranked Markdown table.

Usage:
    python3 scripts/insights/tieout_check.py --out research/tieout_sweep.json
    python3 scripts/insights/tieout_report.py --in research/tieout_sweep.json
"""

import argparse
import collections
import json


def fmt(x):
    if x is None:
        return ""
    return f"{x:,.1f}".rstrip("0").rstrip(".") if abs(x) < 1e12 else f"{x:,.0f}"


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--in", dest="inp", default="research/tieout_sweep.json")
    ap.add_argument("--top", type=int, default=80)
    args = ap.parse_args()

    D = json.load(open(args.inp))
    R = D["checks"]
    counts = collections.Counter(r["status"] for r in R)

    def sigs(status):
        s = collections.defaultdict(list)
        for r in R:
            if r["status"] == status:
                s[(r["bank"], r["sheet"], r["label"])].append(r)
        return s

    mm = sigs("MISMATCH")
    su = sigs("STRUCTURE_UNCLEAR")

    out = []
    out.append("## Status counts (bank / sheet / year / total-row checks)\n")
    out.append("| status | checks |")
    out.append("|---|---:|")
    for k, v in counts.most_common():
        out.append(f"| {k} | {v:,} |")
    out.append(f"| **total** | **{len(R):,}** |")
    out.append("")

    def table(sig, title, limit):
        rows = []
        for k, v in sig.items():
            w = max(v, key=lambda r: r["pct"] or 0)
            a = max(v, key=lambda r: abs(r["residual"] or 0))
            rows.append((w, a, len(v)))
        rows.sort(key=lambda t: -(t[0]["pct"] or 0))
        out.append(f"### {title} — {len(rows)} signatures, ranked by worst-year %\n")
        out.append(
            "| % | abs residual | yrs | bank | sheet | worst year | TOTAL row "
            "| total | sum of DATA | blanks |"
        )
        out.append("|---:|---:|---:|---|---|---|---|---:|---:|---:|")
        for w, a, n in rows[:limit]:
            out.append(
                f"| {w['pct']:.2f}% | {fmt(abs(a['residual'] or 0))} | {n} | "
                f"{w['bank']} | {w['sheet']} | {w['year']} | {w['label'][:70]} | "
                f"{fmt(w['total'])} | {fmt(w['sum'])} | {w.get('n_blank', '')} |"
            )
        out.append("")
        return rows

    table(mm, "MISMATCH — no sane composition fits", limit=args.top)
    table(su, "STRUCTURE_UNCLEAR — needs a human read", limit=30)

    print("\n".join(out))


if __name__ == "__main__":
    main()
