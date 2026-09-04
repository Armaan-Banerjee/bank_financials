"""
Builds and maintains the insights project's SQLite database,
research/insights.db - the source of truth for this data (decided
2026-08-29, see wayfinder/insights/tickets/IN-008.md).

Originally built for IN-007 as a one-off CSV/markdown -> DB import. IN-008
inverted the refresh path: scripts/extract_metrics.py now writes the
banks/annual_metrics tables DIRECTLY (calling write_banks_and_metrics()
below with its in-memory rows, no CSV round-trip), and
scripts/export_parent_group_tables.py writes the parent_group_lookup/edges
tables directly from freshly-researched data before splicing the rendered
tables back into research/bank_parent_groups.md. This file keeps a
standalone CLI (`python3 scripts/build_insights_db.py`) that rebuilds the
WHOLE database from the current research/bank_metrics.csv and
research/bank_parent_groups.md - useful for disaster recovery (the DB file
was deleted or corrupted) or for verifying the DB matches those exports,
but it is no longer the primary way the database gets written day to day.

IMPORTANT: only ever modifies research/insights.db. Never modifies bank
workbooks, research/bank_metrics.csv, or research/bank_parent_groups.md.

Usage:
    python3 scripts/build_insights_db.py                  # full rebuild from CSV+markdown
    python3 scripts/build_insights_db.py --db research/insights.db

Schema
------
banks(frn INTEGER PRIMARY KEY, canonical_name, filename_bank_name,
      source_workbook, workbook_kind, basis_note)

annual_metrics(id INTEGER PRIMARY KEY, frn INTEGER REFERENCES banks(frn),
      sheet, row_label, year, value_raw, value_numeric REAL NULL,
      is_numeric INTEGER,
      UNIQUE(frn, sheet, row_label, year))
      -- id is a plain autoincrement-by-insertion-order rowid; exporters
      -- that want to reproduce the original extraction order should
      -- ORDER BY id.

parent_group_lookup(frn INTEGER PRIMARY KEY REFERENCES banks(frn),
      bank_name, immediate_parent, ultimate_group, status_caveat, evidence)

parent_group_edges(id INTEGER PRIMARY KEY, from_node, edge_type, to_node,
      effective_note, source, from_frn INTEGER NULL REFERENCES banks(frn),
      to_frn INTEGER NULL REFERENCES banks(frn))
      -- from_frn/to_frn are a best-effort resolution when an edge endpoint's
      -- name matches a built bank exactly; NULL when the endpoint is a
      -- parent/holding entity that isn't itself one of the 145 built banks.

equity_changes(id INTEGER PRIMARY KEY, frn INTEGER REFERENCES banks(frn),
      sheet, movement_label, component, value_raw, value_numeric REAL NULL,
      is_numeric INTEGER, row_order INTEGER)
      -- Statement of Changes in Equity (added 2026-09-04, IN-039) - a
      -- chronological roll-forward, not the year-column shape
      -- annual_metrics assumes, so it gets its own table. row_order
      -- preserves the sheet's own oldest-to-newest read order; never
      -- re-sort by it implicitly (e.g. alphabetically on movement_label).

refresh_metadata(id INTEGER PRIMARY KEY CHECK (id = 1),
      metrics_built_at, metrics_source, banks_count, annual_metrics_count,
      equity_changes_count, parent_group_built_at, parent_group_lookup_count,
      parent_group_edges_count)
      -- one row, columns updated independently by whichever half (metrics
      -- vs. parent-group) last refreshed - the two halves are written by
      -- different scripts on different schedules, so this must not force
      -- both to be present before either can record its own refresh.
"""

import argparse
import csv
import json
import os
import re
import sqlite3
from datetime import datetime, timezone

REPO_ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
DEFAULT_CSV = os.path.join(REPO_ROOT, "research", "bank_metrics.csv")
DEFAULT_SCHEMA_JSON = DEFAULT_CSV + ".schema.json"
DEFAULT_MARKDOWN = os.path.join(REPO_ROOT, "research", "bank_parent_groups.md")
DEFAULT_DB = os.path.join(REPO_ROOT, "research", "insights.db")

BANKS_METRICS_SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS banks (
    frn INTEGER PRIMARY KEY,
    canonical_name TEXT NOT NULL,
    filename_bank_name TEXT NOT NULL,
    source_workbook TEXT NOT NULL,
    workbook_kind TEXT NOT NULL,
    basis_note TEXT
);

CREATE TABLE IF NOT EXISTS annual_metrics (
    id INTEGER PRIMARY KEY,
    frn INTEGER NOT NULL REFERENCES banks(frn),
    sheet TEXT NOT NULL,
    row_label TEXT NOT NULL,
    year TEXT NOT NULL,
    value_raw TEXT,
    value_numeric REAL,
    is_numeric INTEGER NOT NULL,
    unit TEXT,
    reporting_basis TEXT,
    restatement_note TEXT,
    source_note TEXT,
    UNIQUE(frn, sheet, row_label, year)
);
CREATE INDEX IF NOT EXISTS idx_annual_metrics_frn ON annual_metrics(frn);
CREATE INDEX IF NOT EXISTS idx_annual_metrics_sheet ON annual_metrics(sheet);
"""

EQUITY_CHANGES_SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS equity_changes (
    id INTEGER PRIMARY KEY,
    frn INTEGER NOT NULL REFERENCES banks(frn),
    sheet TEXT NOT NULL,
    movement_label TEXT NOT NULL,
    component TEXT NOT NULL,
    value_raw TEXT,
    value_numeric REAL,
    is_numeric INTEGER NOT NULL,
    row_order INTEGER NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_equity_changes_frn ON equity_changes(frn);
"""
# Statement of Changes in Equity (added by the ST- wayfinder rollout,
# 2026-09-04, see wayfinder/insights/tickets/IN-039.md) doesn't fit
# annual_metrics's year-keyed shape - it's a chronological roll-forward,
# equity-component columns x movement rows, not year columns - so it gets
# its own table rather than forcing `year` to hold a movement label.
# `row_order` preserves the sheet's own oldest-to-newest read order;
# consumers must not re-sort this the way annual_metrics rows can be.

PARENT_GROUP_SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS parent_group_lookup (
    frn INTEGER PRIMARY KEY REFERENCES banks(frn),
    bank_name TEXT NOT NULL,
    immediate_parent TEXT,
    ultimate_group TEXT,
    status_caveat TEXT,
    evidence TEXT,
    sort_order INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS parent_group_edges (
    id INTEGER PRIMARY KEY,
    from_node TEXT NOT NULL,
    edge_type TEXT NOT NULL,
    to_node TEXT NOT NULL,
    effective_note TEXT,
    source TEXT,
    from_frn INTEGER REFERENCES banks(frn),
    to_frn INTEGER REFERENCES banks(frn),
    effective_from TEXT,
    effective_to TEXT
);
"""

REFRESH_METADATA_SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS refresh_metadata (
    id INTEGER PRIMARY KEY CHECK (id = 1),
    metrics_built_at TEXT,
    metrics_source TEXT,
    banks_count INTEGER,
    annual_metrics_count INTEGER,
    parent_group_built_at TEXT,
    parent_group_lookup_count INTEGER,
    parent_group_edges_count INTEGER
);
"""

INTERIM_SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS interim_observations (
    id INTEGER PRIMARY KEY,
    frn INTEGER NOT NULL REFERENCES banks(frn),
    source_workbook TEXT NOT NULL,
    source_sheet TEXT NOT NULL,
    source_cell TEXT NOT NULL,
    row_label_raw TEXT NOT NULL,
    metric_key TEXT,
    normalization_status TEXT NOT NULL,
    unit_raw TEXT,
    basis_raw TEXT,
    reporting_basis TEXT,
    period_label_raw TEXT NOT NULL,
    period_type TEXT NOT NULL,
    period_end_date TEXT,
    period_precision TEXT,
    period_end_year INTEGER,
    period_end_month INTEGER,
    period_sequence INTEGER,
    period_length_months INTEGER,
    annual_status TEXT NOT NULL,
    value_raw TEXT,
    value_numeric REAL,
    is_numeric INTEGER NOT NULL,
    sheet_note TEXT
);
CREATE INDEX IF NOT EXISTS idx_interim_observations_frn ON interim_observations(frn);
CREATE INDEX IF NOT EXISTS idx_interim_observations_period ON interim_observations(period_label_raw);

CREATE TABLE IF NOT EXISTS interim_source_register (
    id INTEGER PRIMARY KEY,
    frn INTEGER NOT NULL REFERENCES banks(frn),
    source_workbook TEXT NOT NULL,
    source_sheet TEXT NOT NULL,
    registry_row INTEGER NOT NULL,
    period_label_raw TEXT,
    disclosure_type_raw TEXT,
    source_document_raw TEXT,
    source_locator_raw TEXT,
    source_url TEXT,
    mapping_scope TEXT NOT NULL
);
"""


def connect(db_path):
    """Opens (creating if needed) the database and ensures all tables
    exist. Does NOT drop anything - callers that need a clean slate for a
    specific table group call the relevant create_*_tables() below.

    Deliberately does NOT enable `PRAGMA foreign_keys` - banks/annual_metrics
    and parent_group_lookup/edges are refreshed independently by different
    scripts on different schedules (see the module docstring), so there's a
    legitimate transient state where one side is rebuilt before the other
    catches up. Referential integrity is checked explicitly in validate()
    instead of relying on SQLite to enforce it at write time."""
    conn = sqlite3.connect(db_path)
    conn.executescript(BANKS_METRICS_SCHEMA_SQL)
    conn.executescript(EQUITY_CHANGES_SCHEMA_SQL)
    conn.executescript(PARENT_GROUP_SCHEMA_SQL)
    conn.executescript(REFRESH_METADATA_SCHEMA_SQL)
    conn.executescript(INTERIM_SCHEMA_SQL)
    conn.execute("INSERT OR IGNORE INTO refresh_metadata (id) VALUES (1)")
    _migrate_add_columns(conn)
    conn.commit()
    return conn


# Schema-completeness columns added after the original IN-007/IN-008 tables
# were already in production use (see wayfinder/insights/ item 5). `CREATE
# TABLE IF NOT EXISTS` above is a no-op against a database file that already
# has the table under the OLD column set, so new columns need an explicit,
# idempotent ALTER TABLE migration here - this is what "preserve current
# data during migration" means in practice: existing rows are never
# touched, they just gain new NULL-valued columns.
_COLUMN_MIGRATIONS = [
    ("annual_metrics", "unit", "TEXT"),
    ("annual_metrics", "reporting_basis", "TEXT"),
    ("annual_metrics", "restatement_note", "TEXT"),
    ("annual_metrics", "source_note", "TEXT"),
    ("parent_group_edges", "effective_from", "TEXT"),
    ("parent_group_edges", "effective_to", "TEXT"),
    ("refresh_metadata", "equity_changes_count", "INTEGER"),
]


def _migrate_add_columns(conn):
    for table, column, coltype in _COLUMN_MIGRATIONS:
        existing = {row[1] for row in conn.execute(f"PRAGMA table_info({table})")}
        if column not in existing:
            conn.execute(f"ALTER TABLE {table} ADD COLUMN {column} {coltype}")


def create_banks_and_metrics_tables(conn):
    """Clears ONLY banks/annual_metrics (tables are created if missing,
    then emptied) - leaves parent_group_lookup/edges/refresh_metadata's
    other columns untouched, since those are owned by a different refresh
    cycle. Uses DELETE rather than DROP+CREATE: with foreign_keys=ON,
    parent_group_lookup/edges reference banks(frn), and SQLite refuses to
    DROP a table that another table's FK still points at even when both
    are empty - DELETE avoids that entirely and is just as clean for a
    full-table refresh."""
    conn.executescript(BANKS_METRICS_SCHEMA_SQL)
    conn.execute("DELETE FROM annual_metrics")
    conn.execute("DELETE FROM banks")


def write_banks_and_metrics(conn, rows, metrics_source):
    """Writes banks + annual_metrics from `rows` - a list of dicts shaped
    exactly like scripts/extract_metrics.py's in-memory `all_rows` (the
    same rows it also writes to CSV), post-deduplication. Recreates the
    two tables from scratch (this IS the authoritative write path now, not
    an import of something else) and updates refresh_metadata's
    metrics_* columns only.

    `metrics_source` is a short human string recorded in refresh_metadata
    for provenance (e.g. "scripts/extract_metrics.py direct write" or
    "scripts/build_insights_db.py CSV import").
    """
    try:
        create_banks_and_metrics_tables(conn)

        banks_by_frn = {}
        for r in rows:
            frn = r["frn"]
            if frn in (None, ""):
                raise ValueError(
                    f"Row with no FRN found (bank={r.get('bank')!r}) - every row "
                    f"must carry an FRN; this indicates a regression in FRN coverage."
                )
            frn = int(frn)
            if frn not in banks_by_frn:
                banks_by_frn[frn] = {
                    "frn": frn,
                    "canonical_name": r["canonical_bank"],
                    "filename_bank_name": r["source_filename_bank"],
                    "source_workbook": r["source_workbook"],
                    "workbook_kind": r["workbook_kind"],
                    "basis_note": r["basis_note"] or None,
                }

        conn.executemany(
            "INSERT INTO banks (frn, canonical_name, filename_bank_name, "
            "source_workbook, workbook_kind, basis_note) VALUES "
            "(:frn, :canonical_name, :filename_bank_name, :source_workbook, "
            ":workbook_kind, :basis_note)",
            list(banks_by_frn.values()),
        )

        # unit/reporting_basis/restatement_note/source_note (schema-completeness
        # columns, see _COLUMN_MIGRATIONS) are read via .get() - optional on the
        # input row dicts so existing callers/tests that don't supply them keep
        # working unchanged, and simply get NULL for these columns, never an
        # error or a fabricated value.
        metric_rows = [
            {
                "frn": int(r["frn"]),
                "sheet": r["sheet"],
                "row_label": r["row_label"],
                "year": r["year"],
                "value_raw": (r["value_raw"] if r["value_raw"] not in (None, "") else None),
                "value_numeric": (float(r["value_numeric"]) if r["value_numeric"] not in (None, "") else None),
                "is_numeric": int(r["is_numeric"]),
                "unit": r.get("unit") or None,
                "reporting_basis": r.get("reporting_basis") or None,
                "restatement_note": r.get("restatement_note") or None,
                "source_note": r.get("source_note") or None,
            }
            for r in rows
        ]
        conn.executemany(
            "INSERT INTO annual_metrics (frn, sheet, row_label, year, "
            "value_raw, value_numeric, is_numeric, unit, reporting_basis, "
            "restatement_note, source_note) VALUES "
            "(:frn, :sheet, :row_label, :year, :value_raw, :value_numeric, :is_numeric, "
            ":unit, :reporting_basis, :restatement_note, :source_note)",
            metric_rows,
        )

        conn.execute(
            "UPDATE refresh_metadata SET metrics_built_at = ?, metrics_source = ?, "
            "banks_count = ?, annual_metrics_count = ? WHERE id = 1",
            (datetime.now(timezone.utc).isoformat(), metrics_source,
             len(banks_by_frn), len(metric_rows)),
        )
        conn.commit()
        return len(banks_by_frn), len(metric_rows)
    except Exception:
        # DELETE + INSERT happens in one transaction. Preserve the previous
        # source-of-truth snapshot if validation or an insert fails midway.
        conn.rollback()
        raise


def write_equity_changes(conn, rows):
    """Replace the equity_changes table from `rows` - dicts shaped like
    extract_metrics.py's `_equity_row()` output. Independently refreshable
    (DELETE + INSERT, like write_interim_observations below) rather than
    tied to write_banks_and_metrics's own transaction, since a caller could
    conceivably refresh one without the other - but every row's frn must
    already exist in banks (see extract_metrics.py's frn-drop filter before
    calling this), so call this AFTER write_banks_and_metrics in the same
    refresh run."""
    conn.execute("DELETE FROM equity_changes")
    conn.executemany(
        "INSERT INTO equity_changes (frn, sheet, movement_label, component, "
        "value_raw, value_numeric, is_numeric, row_order) VALUES "
        "(:frn, :sheet, :movement_label, :component, :value_raw, "
        ":value_numeric, :is_numeric, :row_order)",
        [
            {
                "frn": int(r["frn"]),
                "sheet": r["sheet"],
                "movement_label": r["movement_label"],
                "component": r["component"],
                "value_raw": (r["value_raw"] if r["value_raw"] not in (None, "") else None),
                "value_numeric": (float(r["value_numeric"]) if r["value_numeric"] not in (None, "") else None),
                "is_numeric": int(r["is_numeric"]),
                "row_order": int(r["row_order"]),
            }
            for r in rows
        ],
    )
    conn.execute(
        "UPDATE refresh_metadata SET equity_changes_count = ? WHERE id = 1",
        (len(rows),),
    )
    conn.commit()
    return len(rows)


def write_interim_observations(conn, observations, source_register):
    """Replace the independently refreshable interim observation domain."""
    conn.execute("DELETE FROM interim_source_register")
    conn.execute("DELETE FROM interim_observations")
    conn.executemany("""
        INSERT INTO interim_observations (
            frn, source_workbook, source_sheet, source_cell, row_label_raw,
            metric_key, normalization_status, unit_raw, basis_raw,
            reporting_basis, period_label_raw, period_type, period_end_date,
            period_precision, period_end_year, period_end_month, period_sequence,
            period_length_months, annual_status, value_raw, value_numeric,
            is_numeric, sheet_note
        ) VALUES (
            :frn, :source_workbook, :source_sheet, :source_cell, :row_label_raw,
            :metric_key, :normalization_status, :unit_raw, :basis_raw,
            :reporting_basis, :period_label_raw, :period_type, :period_end_date,
            :period_precision, :period_end_year, :period_end_month, :period_sequence,
            :period_length_months, :annual_status, :value_raw, :value_numeric,
            :is_numeric, :sheet_note
        )
    """, observations)
    conn.executemany("""
        INSERT INTO interim_source_register (
            frn, source_workbook, source_sheet, registry_row, period_label_raw,
            disclosure_type_raw, source_document_raw, source_locator_raw,
            source_url, mapping_scope
        ) VALUES (
            :frn, :source_workbook, :source_sheet, :registry_row, :period_label_raw,
            :disclosure_type_raw, :source_document_raw, :source_locator_raw,
            :source_url, :mapping_scope
        )
    """, source_register)
    conn.commit()
    return len(observations), len(source_register)


METRICS_CSV_FIELDNAMES = [
    "bank", "canonical_bank", "source_filename_bank", "source_workbook",
    "frn", "workbook_kind", "sheet", "row_label", "year",
    "value_raw", "value_numeric", "is_numeric", "basis_note",
    "unit", "reporting_basis", "restatement_note", "source_note",
]

_METRICS_CSV_STRING_COLUMNS = (
    "value_raw", "basis_note", "unit", "reporting_basis", "restatement_note", "source_note",
)


def export_metrics_csv(conn, out_path):
    """Exports annual_metrics JOIN banks back into IN-001's original CSV
    column shape - the mechanism that makes the database the source of
    truth rather than the CSV: this is a read FROM the database, not a
    re-derivation from workbooks. ORDER BY m.id reproduces the original
    per-bank/per-sheet extraction order (annual_metrics.id is a plain
    insertion-order rowid)."""
    import csv as _csv
    cur = conn.execute("""
        SELECT b.filename_bank_name AS bank,
               b.canonical_name AS canonical_bank,
               b.filename_bank_name AS source_filename_bank,
               b.source_workbook AS source_workbook,
               b.frn AS frn,
               b.workbook_kind AS workbook_kind,
               m.sheet AS sheet,
               m.row_label AS row_label,
               m.year AS year,
               m.value_raw AS value_raw,
               m.value_numeric AS value_numeric,
               m.is_numeric AS is_numeric,
               b.basis_note AS basis_note,
               m.unit AS unit,
               m.reporting_basis AS reporting_basis,
               m.restatement_note AS restatement_note,
               m.source_note AS source_note
        FROM annual_metrics m JOIN banks b ON b.frn = m.frn
        ORDER BY m.id
    """)
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    n = 0
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = _csv.DictWriter(f, fieldnames=METRICS_CSV_FIELDNAMES)
        writer.writeheader()
        for row in cur:
            d = dict(zip(METRICS_CSV_FIELDNAMES, row))
            for key in _METRICS_CSV_STRING_COLUMNS:
                d[key] = d[key] if d[key] is not None else ""
            d["value_numeric"] = d["value_numeric"] if d["value_numeric"] is not None else ""
            d["is_numeric"] = str(d["is_numeric"])
            writer.writerow(d)
            n += 1
    return n


def load_csv_rows(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def load_rows_from_db(path):
    """Return annual metric rows in the same string-shaped form as the
    generated CSV export, for consumers that should read the source of truth
    directly rather than making a CSV round-trip."""
    conn = sqlite3.connect(path)
    try:
        rows = []
        cur = conn.execute("""
            SELECT b.filename_bank_name AS bank,
                   b.canonical_name AS canonical_bank,
                   b.filename_bank_name AS source_filename_bank,
                   b.source_workbook AS source_workbook,
                   b.frn AS frn,
                   b.workbook_kind AS workbook_kind,
                   m.sheet AS sheet,
                   m.row_label AS row_label,
                   m.year AS year,
                   m.value_raw AS value_raw,
                   m.value_numeric AS value_numeric,
                   m.is_numeric AS is_numeric,
                   b.basis_note AS basis_note,
                   m.unit AS unit,
                   m.reporting_basis AS reporting_basis,
                   m.restatement_note AS restatement_note,
                   m.source_note AS source_note
            FROM annual_metrics m JOIN banks b ON b.frn = m.frn
            ORDER BY m.id
        """)
        columns = [description[0] for description in cur.description]
        for record in cur:
            row = dict(zip(columns, record))
            for key in ("frn", "is_numeric"):
                row[key] = str(row[key])
            for key in ("value_raw", "value_numeric", "basis_note", "unit",
                        "reporting_basis", "restatement_note", "source_note"):
                if row[key] is None:
                    row[key] = ""
                elif key == "value_numeric":
                    row[key] = str(row[key])
            rows.append(row)
        return rows
    finally:
        conn.close()


def load_groups_from_db(path):
    """Returns {frn_str: (bank_name, ultimate_group, status_caveat)} from
    parent_group_lookup - the DB-sourced equivalent of
    scripts/analyze_trends.py's load_groups() (which parses the markdown
    directly). Shared here, per CODING_STANDARDS.md, so every consumer
    (analyze_trends.py, review_trend_selection.py, and any future one) reads
    parent-group data the same way rather than each re-parsing the markdown
    or re-writing this query."""
    conn = sqlite3.connect(path)
    try:
        groups = {}
        for frn, bank_name, ultimate_group, status_caveat in conn.execute(
            "SELECT frn, bank_name, ultimate_group, status_caveat FROM parent_group_lookup "
            "ORDER BY sort_order"
        ):
            groups[str(frn)] = (bank_name, ultimate_group, status_caveat)
        return groups
    finally:
        conn.close()


def multi_entity_groups(groups, min_size=2):
    """`groups` is the {frn: (bank_name, ultimate_group, status_caveat)}
    shape load_groups()/load_groups_from_db() both return. Returns a list
    of (group_name, [(frn, bank_name), ...]) for every ultimate_group with
    at least `min_size` members, sorted by descending size then name - the
    same grouping analyze_trends.py's own main() already computes for its
    report, factored out here so deliverable generators (build_in005_prototype.py,
    build_in006_pdf.py) read it live instead of hardcoding the result, per
    CODING_STANDARDS.md.

    FRN is included alongside each bank_name deliberately: parent_group_lookup's
    bank_name (e.g. "Santander UK", "National Westminster Bank") and
    bank_clusters.csv's filename-derived name (e.g. "SANTANDER",
    "NATIONAL WESTMINSTER BANK PLC") are two different, both-legitimate
    naming conventions for the same entity - a consumer that needs to join
    group membership back to cluster/metric data must do it by FRN, not by
    fuzzy name matching, or it will silently drop members whose two names
    happen to differ (confirmed happening for exactly Santander UK and
    National Westminster Bank while building this)."""
    by_group = {}
    for frn, (bank_name, group, caveat) in groups.items():
        by_group.setdefault(group, []).append((frn, bank_name))
    multi = [(group, members) for group, members in by_group.items() if len(members) >= min_size]
    multi.sort(key=lambda item: (-len(item[1]), item[0]))
    return multi


def load_cluster_rows(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def cluster_size_summary(cluster_rows):
    """Returns ({cluster_id: size}, insufficient_count) from
    research/bank_clusters.csv-shaped rows. Used to report peer-group
    sizes without hardcoding them - see validate_cluster_inputs() for the
    staleness guard that should normally run before this."""
    sizes = {}
    insufficient = 0
    for row in cluster_rows:
        if row["insufficient_data"] == "1":
            insufficient += 1
            continue
        cid = row["cluster_id"]
        sizes[cid] = sizes.get(cid, 0) + 1
    return sizes, insufficient


def validate_cluster_inputs(db_path, cluster_rows, cluster_path, centroids_path=None):
    """Rejects obviously stale or mismatched derived cluster outputs before
    a deliverable generator embeds them. Checks: (1) the cluster CSV's FRN
    set matches the database's bank FRN set exactly (catches a cluster
    output computed against a different/older bank list); (2) if
    `centroids_path` is given, that file exists; (3) neither the cluster
    CSV nor (if given) the centroids CSV is older than the database's last
    metrics refresh (catches "database was refreshed, cluster_banks.py
    wasn't rerun yet"). Originally build_in005_prototype.py-only; moved
    here so build_in006_pdf.py gets the same protection rather than a
    second, drifting copy of this logic."""
    conn = sqlite3.connect(db_path)
    try:
        db_frns = {str(row[0]) for row in conn.execute("SELECT frn FROM banks")}
        metrics_built_at = conn.execute(
            "SELECT metrics_built_at FROM refresh_metadata WHERE id = 1"
        ).fetchone()[0]
    finally:
        conn.close()
    cluster_frns = {str(row["frn"]) for row in cluster_rows}
    if cluster_frns != db_frns:
        raise ValueError(
            "cluster output FRNs do not match the database; rerun "
            "scripts/cluster_banks.py before generating the deliverable"
        )
    if centroids_path is not None and not os.path.exists(centroids_path):
        raise FileNotFoundError(f"Missing cluster centroid output: {centroids_path}")
    if metrics_built_at:
        built_at = datetime.fromisoformat(metrics_built_at).astimezone(timezone.utc).timestamp()
        stale = os.path.getmtime(cluster_path) + 2 < built_at
        if centroids_path is not None:
            stale = stale or os.path.getmtime(centroids_path) + 2 < built_at
        if stale:
            raise ValueError(
                "cluster outputs are older than the database metrics refresh; "
                "rerun scripts/cluster_banks.py before generating the deliverable"
            )


def load_markdown_lookup_and_edges(path):
    """Parses IN-002's two tables: the bank-level lookup (with an FRN
    column) and the typed edge list. Both are plain markdown pipe tables -
    parsed by splitting on '|', same approach already used and proven
    correct in scripts/analyze_trends.py's load_groups()."""
    lookup_rows = []
    edge_rows = []
    section = None
    with open(path, encoding="utf-8") as f:
        for line in f:
            stripped = line.strip()
            if stripped.startswith("## Bank-level lookup"):
                section = "lookup"
                continue
            if stripped.startswith("## Typed edge list"):
                section = "edges"
                continue
            if stripped.startswith("## ") and section in ("lookup", "edges"):
                section = None
                continue
            if not stripped.startswith("|") or stripped.startswith("|---"):
                continue
            parts = [p.strip() for p in stripped.strip("|").split("|")]
            if section == "lookup":
                if parts[0] in ("Bank/legal entity",) or not parts[1].isdigit():
                    continue
                if len(parts) < 6:
                    continue
                lookup_rows.append({
                    "frn": int(parts[1]),
                    "bank_name": parts[0],
                    "immediate_parent": parts[2],
                    "ultimate_group": parts[3],
                    "status_caveat": parts[4],
                    "evidence": parts[5],
                })
            elif section == "edges":
                if parts[0] in ("from",):
                    continue
                if len(parts) < 5:
                    continue
                edge_rows.append({
                    "from_node": parts[0],
                    "edge_type": parts[1],
                    "to_node": parts[2],
                    "effective_note": parts[3],
                    "source": parts[4],
                })
    return lookup_rows, edge_rows


_EFFECTIVE_FROM_RE = re.compile(r"\bfrom (\d{4}(?:-\d{2}(?:-\d{2})?)?)", re.I)


def _parse_effective_from(effective_note):
    """Best-effort structured date extraction from the free-text
    effective_note (e.g. "from 2023-05-19; prior no-parent state retained"
    -> "2023-05-19"). Conservative on purpose: only a clearly-labelled
    "from <date>" phrase is extracted; anything else (a bare year in a
    sentence, a JV percentage, "current") is left NULL rather than guessed,
    per the same discipline used throughout this project - see
    CODING_STANDARDS.md's missing-data rules."""
    if not effective_note:
        return None
    match = _EFFECTIVE_FROM_RE.search(effective_note)
    return match.group(1) if match else None


def write_parent_group(conn, lookup_rows, edge_rows):
    """Writes parent_group_lookup + parent_group_edges from already-parsed
    row lists. Requires banks to already be populated (raises a clear
    error naming the fix otherwise) - every lookup row's FRN must resolve
    to a known bank, no crosswalk permitted."""
    known_frns = {row[0] for row in conn.execute("SELECT frn FROM banks")}
    if not known_frns:
        raise RuntimeError(
            "banks table is empty - run scripts/extract_metrics.py first "
            "(it writes banks/annual_metrics) before writing parent-group data."
        )
    skipped_lookup = [lr for lr in lookup_rows if lr["frn"] not in known_frns]
    if skipped_lookup:
        raise ValueError(
            f"{len(skipped_lookup)} parent_group_lookup rows have an FRN not "
            f"present in banks: {[lr['frn'] for lr in skipped_lookup]}"
        )

    conn.executescript("""
        DROP TABLE IF EXISTS parent_group_edges;
        DROP TABLE IF EXISTS parent_group_lookup;
    """)
    conn.executescript(PARENT_GROUP_SCHEMA_SQL)

    # sort_order preserves the exact row order from the source markdown file
    # (NOT re-derived by sorting bank_name in SQL) - the file's order isn't
    # guaranteed to be strict case-insensitive alphabetical everywhere, and
    # re-sorting risked a subtly different (if plausible-looking) order on
    # export - see scripts/export_parent_group_tables.py.
    lookup_rows_with_order = [{**lr, "sort_order": i} for i, lr in enumerate(lookup_rows)]
    conn.executemany(
        "INSERT INTO parent_group_lookup (frn, bank_name, immediate_parent, "
        "ultimate_group, status_caveat, evidence, sort_order) VALUES "
        "(:frn, :bank_name, :immediate_parent, :ultimate_group, :status_caveat, :evidence, :sort_order)",
        lookup_rows_with_order,
    )

    name_to_frn = {lr["bank_name"]: lr["frn"] for lr in lookup_rows}
    edge_insert_rows = [
        {
            **e,
            "from_frn": name_to_frn.get(e["from_node"]),
            "to_frn": name_to_frn.get(e["to_node"]),
            "effective_from": _parse_effective_from(e["effective_note"]),
            # No current edge's effective_note encodes an end date (every
            # historical change so far reads as "current as of X", not
            # "X until Y") - column exists for when one does, deliberately
            # left NULL rather than guessed.
            "effective_to": None,
        }
        for e in edge_rows
    ]
    conn.executemany(
        "INSERT INTO parent_group_edges (from_node, edge_type, to_node, "
        "effective_note, source, from_frn, to_frn, effective_from, effective_to) VALUES "
        "(:from_node, :edge_type, :to_node, :effective_note, :source, :from_frn, :to_frn, "
        ":effective_from, :effective_to)",
        edge_insert_rows,
    )

    conn.execute(
        "UPDATE refresh_metadata SET parent_group_built_at = ?, "
        "parent_group_lookup_count = ?, parent_group_edges_count = ? WHERE id = 1",
        (datetime.now(timezone.utc).isoformat(), len(lookup_rows), len(edge_rows)),
    )
    conn.commit()
    return len(lookup_rows), len(edge_rows)


def validate(conn, expected_banks=145, expected_metric_rows=None):
    """Prints validation results; raises on any hard failure."""
    cur = conn.cursor()

    n_banks = cur.execute("SELECT COUNT(*) FROM banks").fetchone()[0]
    n_distinct_frn = cur.execute("SELECT COUNT(DISTINCT frn) FROM banks").fetchone()[0]
    print(f"banks: {n_banks} rows, {n_distinct_frn} distinct FRNs")
    if n_banks != expected_banks or n_distinct_frn != expected_banks:
        raise AssertionError(f"Expected {expected_banks} banks with unique FRNs, got {n_banks}/{n_distinct_frn}")

    n_metrics = cur.execute("SELECT COUNT(*) FROM annual_metrics").fetchone()[0]
    print(f"annual_metrics: {n_metrics} rows")
    if expected_metric_rows is not None and n_metrics != expected_metric_rows:
        raise AssertionError(
            f"annual_metrics row count ({n_metrics}) does not match expected ({expected_metric_rows})"
        )

    n_dup = cur.execute(
        "SELECT COUNT(*) FROM (SELECT frn, sheet, row_label, year, COUNT(*) c "
        "FROM annual_metrics GROUP BY frn, sheet, row_label, year HAVING c > 1)"
    ).fetchone()[0]
    print(f"duplicate (frn, sheet, row_label, year) keys: {n_dup}")
    if n_dup != 0:
        raise AssertionError(f"{n_dup} duplicate identity keys found in annual_metrics")

    n_orphan_metrics = cur.execute(
        "SELECT COUNT(*) FROM annual_metrics WHERE frn NOT IN (SELECT frn FROM banks)"
    ).fetchone()[0]
    print(f"annual_metrics rows with no matching bank: {n_orphan_metrics}")
    if n_orphan_metrics != 0:
        raise AssertionError(f"{n_orphan_metrics} annual_metrics rows reference an unknown FRN")

    n_equity = cur.execute("SELECT COUNT(*) FROM equity_changes").fetchone()[0]
    n_orphan_equity = cur.execute(
        "SELECT COUNT(*) FROM equity_changes WHERE frn NOT IN (SELECT frn FROM banks)"
    ).fetchone()[0]
    print(f"equity_changes: {n_equity} rows, {n_orphan_equity} with no matching bank")
    if n_orphan_equity != 0:
        raise AssertionError(f"{n_orphan_equity} equity_changes rows reference an unknown FRN")

    n_lookup = cur.execute("SELECT COUNT(*) FROM parent_group_lookup").fetchone()[0]
    n_lookup_joined = cur.execute(
        "SELECT COUNT(*) FROM parent_group_lookup pgl JOIN banks b ON b.frn = pgl.frn"
    ).fetchone()[0]
    print(f"parent_group_lookup: {n_lookup} rows, {n_lookup_joined} join cleanly to banks by FRN")
    if n_lookup and (n_lookup != expected_banks or n_lookup_joined != expected_banks):
        raise AssertionError(
            f"Expected all {expected_banks} parent_group_lookup rows to join to banks by "
            f"FRN with no crosswalk needed; got {n_lookup} rows, {n_lookup_joined} joined"
        )

    n_edges = cur.execute("SELECT COUNT(*) FROM parent_group_edges").fetchone()[0]
    n_edges_resolved_from = cur.execute(
        "SELECT COUNT(*) FROM parent_group_edges WHERE from_frn IS NOT NULL"
    ).fetchone()[0]
    n_edges_resolved_to = cur.execute(
        "SELECT COUNT(*) FROM parent_group_edges WHERE to_frn IS NOT NULL"
    ).fetchone()[0]
    print(f"parent_group_edges: {n_edges} rows ({n_edges_resolved_from} from_frn resolved, "
          f"{n_edges_resolved_to} to_frn resolved - unresolved endpoints are parent/holding "
          f"entities that aren't themselves one of the {expected_banks} built banks, expected)")

    n_missing_value = cur.execute(
        "SELECT COUNT(*) FROM annual_metrics WHERE value_raw IS NULL AND value_numeric IS NOT NULL"
    ).fetchone()[0]
    print(f"rows with NULL value_raw but non-NULL value_numeric (should be 0): {n_missing_value}")
    if n_missing_value != 0:
        raise AssertionError("Found value_numeric populated on a row with NULL value_raw - a missing value must never look numeric")

    print("\nAll validation checks passed.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", default=DEFAULT_DB)
    parser.add_argument("--csv", default=DEFAULT_CSV)
    parser.add_argument("--schema-json", default=DEFAULT_SCHEMA_JSON)
    parser.add_argument("--markdown", default=DEFAULT_MARKDOWN)
    args = parser.parse_args()

    print(f"Full rebuild of {args.db} from {args.csv} and {args.markdown} ...")
    csv_rows = load_csv_rows(args.csv)
    with open(args.schema_json, encoding="utf-8") as f:
        csv_schema = json.load(f)
    lookup_rows, edge_rows = load_markdown_lookup_and_edges(args.markdown)

    conn = connect(args.db)
    try:
        write_banks_and_metrics(conn, csv_rows, metrics_source=f"{__file__} CSV import")
        write_parent_group(conn, lookup_rows, edge_rows)
    except Exception:
        conn.close()
        raise
    print(f"Wrote {args.db}\n")
    validate(conn, expected_metric_rows=csv_schema.get("row_count"))
    conn.close()


if __name__ == "__main__":
    main()
