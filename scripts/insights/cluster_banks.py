"""
Statistical clustering of UK banks into peer groups, from research/insights.db
(the source of truth, per IN-008) or, if pointed at one explicitly, an
IN-001 CSV export. Built for wayfinder/insights/ ticket IN-003 - see that
ticket and wayfinder/insights/map.md for the destination this serves.

NumPy is the only third-party dependency; no sklearn/scipy is required.
The k-means and silhouette implementations below are small NumPy
implementations, not a simplification of the method itself.

Usage:
    python3 scripts/cluster_banks.py
    python3 scripts/cluster_banks.py --db research/insights.db --out research/bank_clusters.csv
    python3 scripts/cluster_banks.py --in research/bank_metrics.csv  # CSV fallback, e.g. no DB available
    python3 scripts/cluster_banks.py --exclude-mrel --out research/bank_clusters_no_mrel.csv

Method (see IN-003's Progress notes for the full write-up and coverage
numbers that motivated these choices):
  - Clusters on the 7 Pillar 3 RATIO sheets only (CET1 Ratio, Tier 1 Ratio,
    Total Capital Ratio, Leverage Ratio, LCR, NSFR, MREL Ratio) - these are
    dimensionless percentages, so they're comparable across banks regardless
    of currency or reporting-unit differences that Total RWAs/absolute
    capital amounts would drag in unresolved. Consolidation-basis
    differences (solo vs. Group) are NOT corrected for - a real limitation,
    documented rather than silently fixed.
  - Per bank per ratio sheet, some workbooks carry more than one row (e.g. a
    "including central bank claims" and "excluding" Leverage Ratio pair).
    The row with the most numeric-valued years is used as that bank's series
    for the sheet - a deterministic, re-runnable rule rather than a manual
    per-bank pick.
  - Each bank's feature value per dimension is its most recent disclosed
    year for that series - a snapshot, not a multi-year average - since
    banks cover different year windows and this ticket's scope is peer
    grouping, not trend-fitting (that's IN-004).
  - A missing/non-numeric ratio is treated as genuine non-disclosure, per
    the user's guidance, not as zero or as disqualifying. Banks with fewer
    than MIN_DIMENSIONS populated ratios are excluded from the fit (listed
    separately as "insufficient data" rather than forced into a cluster on
    mostly-imputed values); banks that clear the threshold have their
    remaining missing dimensions median-imputed, flagged per-cell in the
    output so a downstream consumer can tell a real value from a filled one.
  - MREL is included in the primary run at the user's direction, despite
    sparse coverage. Use --exclude-mrel for a sensitivity run; the script
    reports the selected dimensions and coverage in either mode.
"""

import argparse
import csv
import os
import re
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
from analysis_queries import AnalysisQueries

RATIO_SHEETS = [
    "CET1 Ratio",
    "Tier 1 Ratio",
    "Total Capital Ratio",
    "Leverage Ratio",
    "LCR",
    "NSFR",
    "MREL Ratio",
]

MIN_DIMENSIONS = 4  # documented threshold; applies to whichever dimensions are selected

DEFAULT_DB = os.path.join(os.path.dirname(__file__), "..", "..", "research", "insights.db")
DEFAULT_IN = os.path.join(os.path.dirname(__file__), "..", "..", "research", "bank_metrics.csv")
DEFAULT_OUT = os.path.join(os.path.dirname(__file__), "..", "..", "research", "bank_clusters.csv")

_YEAR_RE = re.compile(r"(\d{4})")


def year_sort_key(year):
    m = _YEAR_RE.search(year or "")
    return int(m.group(1)) if m else -1


def load_rows(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


# Database-backed runs use the shared AnalysisQueries adapter. It returns the
# same superset of fields this module needs while keeping the DB seam in one
# place; the explicit CSV option remains available for comparisons/fallbacks.


def build_feature_matrix(rows, ratio_sheets=None):
    """Returns banks, FRNs, values, selected years, and coverage counts."""
    ratio_sheets = ratio_sheets or RATIO_SHEETS
    # bank -> sheet -> row_label -> list of (year, value_numeric, is_numeric, value_raw)
    by_bank_sheet_label = {}
    bank_frn = {}
    for r in rows:
        if r["sheet"] not in ratio_sheets:
            continue
        bank = r["bank"]
        bank_frn[bank] = r["frn"]
        key = (bank, r["sheet"], r["row_label"])
        by_bank_sheet_label.setdefault(key, []).append(
            (r["year"], r["value_numeric"], r["is_numeric"], r["value_raw"])
        )

    banks = sorted(bank_frn.keys())
    bank_idx = {b: i for i, b in enumerate(banks)}
    matrix = np.full((len(banks), len(ratio_sheets)), np.nan)
    latest_years = np.full((len(banks), len(ratio_sheets)), "", dtype=object)

    # group by (bank, sheet) to pick the most-numeric-populated row_label
    by_bank_sheet = {}
    for (bank, sheet, label), series in by_bank_sheet_label.items():
        by_bank_sheet.setdefault((bank, sheet), []).append((label, series))

    for (bank, sheet), label_series_list in by_bank_sheet.items():
        def numeric_count(series):
            return sum(1 for _, _, is_num, _ in series if is_num == "1")

        def is_percent_row(series):
            # A ratio sheet can carry a sibling row of absolute exposure/
            # buffer amounts (e.g. Leverage Ratio's "total exposure measure"
            # row alongside its "%" row) - these are on wildly different
            # scales and must never be picked as the clustering feature.
            # Prefer any row where a disclosed value is written as "12.3%".
            return any("%" in (v_raw or "") for _, _, _, v_raw in series)

        percent_rows = [ls for ls in label_series_list if is_percent_row(ls[1])]
        candidates = percent_rows if percent_rows else label_series_list
        candidates.sort(key=lambda ls: -numeric_count(ls[1]))
        _, best_series = candidates[0]
        numeric_points = [(y, float(v)) for y, v, is_num, _ in best_series if is_num == "1"]
        if not numeric_points:
            continue
        numeric_points.sort(key=lambda yv: -year_sort_key(yv[0]))
        latest_value = numeric_points[0][1]
        dimension = ratio_sheets.index(sheet)
        matrix[bank_idx[bank], dimension] = latest_value
        latest_years[bank_idx[bank], dimension] = numeric_points[0][0]

    coverage = {sheet: int(np.sum(~np.isnan(matrix[:, i]))) for i, sheet in enumerate(ratio_sheets)}
    return banks, [bank_frn[b] for b in banks], matrix, latest_years, coverage


def kmeans(X, k, n_init=15, max_iter=200, seed=0):
    rng = np.random.default_rng(seed)
    n = X.shape[0]
    best = None
    for init in range(n_init):
        idx = rng.choice(n, size=k, replace=False)
        centers = X[idx].copy()
        labels = None
        for _ in range(max_iter):
            dists = ((X[:, None, :] - centers[None, :, :]) ** 2).sum(axis=2)
            new_labels = dists.argmin(axis=1)
            new_centers = np.array([
                X[new_labels == j].mean(axis=0) if np.any(new_labels == j) else centers[j]
                for j in range(k)
            ])
            if labels is not None and np.array_equal(new_labels, labels):
                labels = new_labels
                centers = new_centers
                break
            labels, centers = new_labels, new_centers
        dists = ((X[:, None, :] - centers[None, :, :]) ** 2).sum(axis=2)
        inertia = dists[np.arange(n), labels].sum()
        if best is None or inertia < best[0]:
            best = (inertia, labels, centers)
    return best  # (inertia, labels, centers)


def silhouette_score(X, labels):
    n = X.shape[0]
    dist = np.sqrt(((X[:, None, :] - X[None, :, :]) ** 2).sum(axis=2))
    unique_labels = np.unique(labels)
    scores = np.zeros(n)
    for i in range(n):
        same = (labels == labels[i])
        same[i] = False
        if not same.any():
            continue
        a = dist[i, same].mean()
        b_candidates = []
        for lbl in unique_labels:
            if lbl == labels[i]:
                continue
            mask = labels == lbl
            if mask.any():
                b_candidates.append(dist[i, mask].mean())
        if not b_candidates:
            continue
        b = min(b_candidates)
        denom = max(a, b)
        scores[i] = (b - a) / denom if denom > 0 else 0.0
    return float(scores.mean())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", dest="db_path", default=DEFAULT_DB,
                        help="SQLite database to read from (source of truth, per IN-008); "
                             "default research/insights.db")
    parser.add_argument("--in", dest="in_path", default=None,
                        help="read from this CSV instead of --db (e.g. for comparing "
                             "against an older export, or if the DB isn't available)")
    parser.add_argument("--out", dest="out_path", default=DEFAULT_OUT)
    parser.add_argument("--k-min", type=int, default=2)
    parser.add_argument("--k-max", type=int, default=8)
    parser.add_argument(
        "--exclude-mrel", action="store_true",
        help="sensitivity run excluding sparse MREL Ratio (primary run includes it)",
    )
    parser.add_argument("--centroids-out", default=None,
                        help="optional centroids CSV; defaults beside --out")
    parser.add_argument("--sweep-out", default=None,
                        help="optional k-sweep CSV; defaults beside --out")
    args = parser.parse_args()
    if args.centroids_out is None:
        root, ext = os.path.splitext(args.out_path)
        args.centroids_out = root + "_centroids.csv"
    if args.sweep_out is None:
        root, ext = os.path.splitext(args.out_path)
        args.sweep_out = root + "_sweep.csv"

    if args.in_path:
        rows = load_rows(args.in_path)
        print(f"Loaded {len(rows)} rows from CSV: {args.in_path}")
    else:
        rows = AnalysisQueries(args.db_path).observations()
        print(f"Loaded {len(rows)} rows from database: {args.db_path}")
    ratio_sheets = [s for s in RATIO_SHEETS if not args.exclude_mrel or s != "MREL Ratio"]
    banks, frns, matrix, latest_years, coverage = build_feature_matrix(rows, ratio_sheets)

    print(f"=== Per-dimension bank coverage (of {len(banks)}; MREL included={not args.exclude_mrel}) ===")
    for sheet in ratio_sheets:
        print(f"  {sheet:22s} {coverage[sheet]:3d} banks with a latest numeric value")

    n_dims_present = (~np.isnan(matrix)).sum(axis=1)
    min_dimensions = min(MIN_DIMENSIONS, len(ratio_sheets))
    include_mask = n_dims_present >= min_dimensions
    n_included = int(include_mask.sum())
    n_excluded = len(banks) - n_included
    print(f"\n{n_included} banks have >= {min_dimensions}/{len(ratio_sheets)} dimensions populated and are included in the fit.")
    print(f"{n_excluded} banks fall below that threshold and are reported as 'insufficient data', not clustered.")

    X_included = matrix[include_mask].copy()
    imputed_mask = np.isnan(X_included)
    col_medians = np.nanmedian(X_included, axis=0)
    for j in range(X_included.shape[1]):
        X_included[imputed_mask[:, j], j] = col_medians[j]

    # Robust (median/IQR) rather than mean/std standardization: several ratio
    # sheets carry known genuine extreme outliers for atypical small-balance-
    # sheet or correspondent-banking business models (e.g. Chetwood's LCR,
    # BNY Mellon's capital ratios - both already flagged as "noise, not
    # signal" in Cross-Bank Trends Analysis.md's first-pass analysis). A
    # mean/std z-score lets a handful of those dominate the whole fit and
    # collapses everyone else together; median/IQR is far less sensitive to
    # them, so the fit differentiates the ~90% of banks with unremarkable
    # ratios instead of just isolating the already-known outliers.
    col_median = np.median(X_included, axis=0)
    q75, q25 = np.percentile(X_included, [75, 25], axis=0)
    col_iqr = q75 - q25
    col_iqr[col_iqr == 0] = 1.0
    X_std = (X_included - col_median) / col_iqr
    # Winsorize (clip) after standardizing: a couple of known extreme
    # sentinel-like disclosures (e.g. Afin Bank's documented 999999% LCR -
    # see Build Effort Review Codex.md) are orders of magnitude beyond
    # everyone else even in robust-scaled units, and Euclidean k-means would
    # otherwise isolate exactly those 1-2 banks as their own cluster at
    # every k, crowding out any real peer-group structure among the other
    # ~110 banks. Clipping keeps them recognizably "extreme" in the fit
    # without letting a single cell's scale dominate every distance
    # computation. WINSOR_CLIP is a judgment call, not a derived constant -
    # documented here so it's easy to revisit.
    WINSOR_CLIP = 4.0
    X_std = np.clip(X_std, -WINSOR_CLIP, WINSOR_CLIP)
    col_mean, col_std = col_median, col_iqr  # reused below to invert back to original units

    print("\n=== k sweep (silhouette score, higher is better) ===")
    results = {}
    k_max = min(args.k_max, n_included - 1)
    if k_max < args.k_min:
        raise ValueError(
            f"Not enough banks passed the coverage threshold to try any k in "
            f"[{args.k_min}, {args.k_max}]: only {n_included} banks included, "
            f"so the largest triable k is {k_max}. Lower --k-min or include "
            f"more banks rather than letting this silently crash on an empty "
            f"results dict."
        )
    for k in range(args.k_min, k_max + 1):
        inertia, labels, centers = kmeans(X_std, k)
        sil = silhouette_score(X_std, labels)
        results[k] = (inertia, labels, centers, sil)
        print(f"  k={k}: silhouette={sil:.4f}  inertia={inertia:.2f}")

    best_k = max(results, key=lambda k: results[k][3])
    inertia, labels, centers_std, sil = results[best_k]
    print(f"\nChosen k={best_k} (highest silhouette score, {sil:.4f})")

    centers_original = centers_std * col_std + col_mean

    print("\n=== Cluster centroids (original % units) ===")
    cluster_sizes = [int((labels == j).sum()) for j in range(best_k)]
    for j in range(best_k):
        print(f"  Cluster {j} (n={cluster_sizes[j]}): " +
              ", ".join(f"{ratio_sheets[d]}={centers_original[j, d]:.1f}" for d in range(len(ratio_sheets))))

    # Reference point is the unweighted mean OF THE CLUSTER CENTROIDS, not of
    # the raw per-bank data. A per-bank median/mean is skewed by within-
    # cluster distribution shape (this dataset's ratio dimensions are
    # right-skewed even after winsorizing extreme sentinel values), which on
    # an earlier pass produced identical "high X / high Y" labels for both
    # clusters in a 2-cluster fit even though one was clearly higher than
    # the other - comparing each centroid to the average *centroid* fixes
    # that, since it's a genuinely relative comparison across clusters.
    # Which 2 dimensions to name is picked in STANDARDIZED (robust-scaled)
    # units, not original % units - LCR/NSFR run in the hundreds of percent
    # while capital ratios run in the tens, so picking by raw-unit deviation
    # would just always surface LCR/NSFR regardless of which dimension
    # actually separates the clusters more meaningfully in relative terms.
    centroid_reference = centers_original.mean(axis=0)
    std_reference = centers_std.mean(axis=0)
    cluster_labels_text = {}
    for j in range(best_k):
        deviations = centers_original[j] - centroid_reference
        std_deviations = centers_std[j] - std_reference
        order = np.argsort(-np.abs(std_deviations))
        top2 = order[:2]
        parts = []
        for d in top2:
            direction = "high" if deviations[d] > 0 else "low"
            parts.append(f"{direction} {ratio_sheets[d]}")
        cluster_labels_text[j] = " / ".join(parts)

    os.makedirs(os.path.dirname(args.centroids_out) or ".", exist_ok=True)
    with open(args.centroids_out, "w", newline="", encoding="utf-8") as f:
        centroid_fields = ["cluster_id", "cluster_label", "cluster_size"] + ratio_sheets
        writer = csv.DictWriter(f, fieldnames=centroid_fields)
        writer.writeheader()
        for j in range(best_k):
            out = {
                "cluster_id": j,
                "cluster_label": cluster_labels_text[j],
                "cluster_size": int((labels == j).sum()),
            }
            out.update({sheet: round(float(centers_original[j, d]), 4)
                        for d, sheet in enumerate(ratio_sheets)})
            writer.writerow(out)

    os.makedirs(os.path.dirname(args.sweep_out) or ".", exist_ok=True)
    with open(args.sweep_out, "w", newline="", encoding="utf-8") as f:
        sweep_fields = ["k", "inertia", "silhouette", "cluster_sizes"]
        writer = csv.DictWriter(f, fieldnames=sweep_fields)
        writer.writeheader()
        for k in sorted(results):
            sweep_inertia, sweep_labels, _, sweep_sil = results[k]
            sizes = ";".join(str(int((sweep_labels == j).sum())) for j in range(k))
            writer.writerow({"k": k, "inertia": round(float(sweep_inertia), 6),
                             "silhouette": round(float(sweep_sil), 6),
                             "cluster_sizes": sizes})

    os.makedirs(os.path.dirname(args.out_path), exist_ok=True)
    fieldnames = ["bank", "frn", "cluster_id", "cluster_label", "insufficient_data"] + \
        [f"{s}_value" for s in ratio_sheets] + [f"{s}_year" for s in ratio_sheets] + \
        [f"{s}_imputed" for s in ratio_sheets]
    with open(args.out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        included_indices = np.where(include_mask)[0]
        for row_i, bank_i in enumerate(included_indices):
            out = {
                "bank": banks[bank_i],
                "frn": frns[bank_i],
                "cluster_id": int(labels[row_i]),
                "cluster_label": cluster_labels_text[int(labels[row_i])],
                "insufficient_data": "0",
            }
            for d, sheet in enumerate(ratio_sheets):
                out[f"{sheet}_value"] = round(float(X_included[row_i, d]), 4)
                out[f"{sheet}_year"] = latest_years[bank_i, d]
                out[f"{sheet}_imputed"] = "1" if imputed_mask[row_i, d] else "0"
            writer.writerow(out)
        for bank_i in np.where(~include_mask)[0]:
            out = {
                "bank": banks[bank_i],
                "frn": frns[bank_i],
                "cluster_id": "",
                "cluster_label": "insufficient data",
                "insufficient_data": "1",
            }
            for d, sheet in enumerate(ratio_sheets):
                v = matrix[bank_i, d]
                out[f"{sheet}_value"] = "" if np.isnan(v) else round(float(v), 4)
                out[f"{sheet}_year"] = latest_years[bank_i, d]
                out[f"{sheet}_imputed"] = "0"
            writer.writerow(out)

    print(f"\nWrote {len(banks)} bank rows ({n_included} clustered, {n_excluded} insufficient-data) to {args.out_path}")
    print(f"Wrote cluster centroids to {args.centroids_out}")
    print(f"Wrote k-sweep results to {args.sweep_out}")
    print("\nCluster labels (auto-generated from top-2 deviating dimensions - a starting point for IN-005, not final client-facing naming):")
    for j in range(best_k):
        print(f"  Cluster {j}: {cluster_labels_text[j]}")


if __name__ == "__main__":
    main()
