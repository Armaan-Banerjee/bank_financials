"""Shared read-only analysis interface over the insights SQLite database.

The public seam deliberately returns the normalized row/group shapes already
used by the analysis modules.  Database access and period/value filtering live
here so callers do not each grow their own SQL and normalization rules.
"""

import os
import sqlite3

import build_insights_db
from in009_analysis import normalize_observation, normalize_period


class AnalysisQueries:
    """Read-only adapter for common analysis inputs.

    ``db_path`` is the only required configuration. Each method opens a
    short-lived read connection through the existing database loader, returns
    deterministic results, and does not mutate the database.
    """

    def __init__(self, db_path):
        self.db_path = os.fspath(db_path)

    def observations(self, sheet=None, annual_only=False, numeric_only=False):
        """Return normalized observations, optionally filtered by policy."""
        rows = [normalize_observation(row) for row in build_insights_db.load_rows_from_db(self.db_path)]
        if sheet is not None:
            rows = [row for row in rows if row.get("sheet") == sheet]
        if annual_only:
            rows = [row for row in rows if row.get("annual_eligible")]
        if numeric_only:
            rows = [row for row in rows if row.get("value_status") in ("numeric", "special_numeric")]
        return rows

    def annual_observations(self, sheet=None, numeric_only=False):
        """Return normalized annual observations through the shared seam."""
        return self.observations(sheet=sheet, annual_only=True, numeric_only=numeric_only)

    def groups(self):
        """Return the canonical ``{frn: (name, group, caveat)}`` mapping."""
        return build_insights_db.load_groups_from_db(self.db_path)

    def interim_observations(self, numeric_only=False):
        """Return period-aware interim facts; annual rows never enter here."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            rows = [dict(row) for row in conn.execute(
                "SELECT * FROM interim_observations ORDER BY id"
            )]
        finally:
            conn.close()
        if numeric_only:
            rows = [row for row in rows if row["is_numeric"]]
        return rows

    def interim_coverage(self):
        """Return deterministic coverage by period type and metric status."""
        rows = self.interim_observations()
        from collections import Counter
        conn = sqlite3.connect(self.db_path)
        try:
            register_rows = conn.execute("SELECT COUNT(*) FROM interim_source_register").fetchone()[0]
        finally:
            conn.close()
        return {
            "banks": len({row["frn"] for row in rows}),
            "observations": len(rows),
            "numeric_observations": sum(bool(row["is_numeric"]) for row in rows),
            "period_types": dict(sorted(Counter(row["period_type"] for row in rows).items())),
            "source_register_rows": register_rows,
        }

    def annual_integrity(self):
        """Return structural checks shared by quality consumers."""
        conn = sqlite3.connect(self.db_path)
        try:
            orphan_count = conn.execute(
                "SELECT COUNT(*) FROM annual_metrics m "
                "LEFT JOIN banks b ON b.frn=m.frn WHERE b.frn IS NULL"
            ).fetchone()[0]
            duplicate_count = conn.execute(
                "SELECT COUNT(*) FROM (SELECT frn,sheet,row_label,year,COUNT(*) c "
                "FROM annual_metrics GROUP BY frn,sheet,row_label,year HAVING c>1)"
            ).fetchone()[0]
            tables = {row[0] for row in conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            )}
        finally:
            conn.close()
        return {"tables": tables, "orphan_rows": orphan_count,
                "identity_duplicates": duplicate_count}

    def refresh_metadata(self):
        """Return the current refresh metadata row, if present."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            row = conn.execute(
                "SELECT metrics_built_at, metrics_source, banks_count, "
                "annual_metrics_count, parent_group_built_at "
                "FROM refresh_metadata WHERE id=1"
            ).fetchone()
        finally:
            conn.close()
        return dict(row) if row else {}

    def latest_interim_snapshot(self, numeric_only=False):
        """Return the latest observation per bank/metric/unit/basis.

        Ordering uses explicit end dates when available; otherwise the raw
        period label is parsed (via `normalize_period`, the same parser
        `in009_analysis.py` uses for quarter/half/point-in-time labels) into
        a comparable ISO period-end date. A bare lexical comparison of
        `period_label_raw` was tried before this and is wrong for real
        interim label formats - e.g. "December 2023" sorts lexically after
        "November 2024" ('D' > 'N') and would pick the chronologically
        earlier snapshot as "latest". Only genuinely unparseable labels fall
        back to lexical comparison as a last resort.
        """
        rows = self.interim_observations(numeric_only=numeric_only)
        latest = {}
        for row in rows:
            key = (row["frn"], row["metric_key"], row["unit_raw"], row["reporting_basis"])
            period_end = row["period_end_date"] or normalize_period(row["period_label_raw"]).get("period_end") or ""
            order = (period_end, row["period_label_raw"])
            if key not in latest or order > latest[key][0]:
                latest[key] = (order, row)
        return [item[1] for item in sorted(latest.values(), key=lambda item: (item[1]["frn"], item[1]["metric_key"] or "", item[1]["period_label_raw"]))]

    def year_to_date_observations(self, numeric_only=False):
        """Return period facts suitable for YTD-aware callers.

        Capital, RWA, ratio, and liquidity observations are snapshots and are
        deliberately not summed. Callers receive only observations whose
        source declares a duration, with the original duration retained.
        """
        return [row for row in self.interim_observations(numeric_only=numeric_only)
                if row["period_length_months"] is not None]

    def multi_entity_groups(self, min_size=2):
        """Return deterministic parent groups with at least ``min_size`` members."""
        return build_insights_db.multi_entity_groups(self.groups(), min_size=min_size)


def load_analysis_inputs(db_path):
    """Convenience adapter for callers needing both normalized inputs."""
    queries = AnalysisQueries(db_path)
    return {"observations": queries.observations(), "groups": queries.groups()}
