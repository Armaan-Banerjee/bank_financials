"""
Tests for scripts/build_insights_db.py's safety-critical functions that had
no dedicated coverage: validate()'s FAILURE paths (only the happy path was
previously exercised, via the live pipeline), validate_cluster_inputs()'s
staleness/mismatch rejection (previously only verified manually in-session),
the idempotent _migrate_add_columns() schema migration (previously only
verified manually against a real pre-migration database backup), and
_parse_effective_from()'s regex edge cases.
"""

import csv
import os
import shutil
import sqlite3
import sys
import tempfile
import time
import unittest

sys.path.insert(0, os.path.dirname(__file__))
import build_insights_db as db


def make_valid_db(path, n_banks=2):
    """A minimal DB that passes validate() cleanly, for corrupting one
    property at a time in the tests below."""
    conn = db.connect(path)
    rows = []
    for i in range(n_banks):
        frn = 100 + i
        rows.append({
            "bank": f"BANK{i}", "canonical_bank": f"Bank {i} Ltd",
            "source_filename_bank": f"BANK{i}", "source_workbook": f"BANK{i} FINANCIALS.xlsx",
            "frn": frn, "workbook_kind": "full", "sheet": "CET1 Ratio",
            "row_label": "CET1 ratio", "year": "FY2025", "value_raw": "14.5%",
            "value_numeric": 14.5, "is_numeric": "1", "basis_note": "",
        })
    db.write_banks_and_metrics(conn, rows, metrics_source="test")
    return conn


class ValidateCatchesCorruption(unittest.TestCase):
    """validate()'s whole job is catching corruption before it's reported
    as a successful refresh - these are the failure paths, previously
    entirely untested (only the "all checks passed" happy path was)."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp(prefix="validate_test_")
        self.db_path = os.path.join(self.tmpdir, "test.db")

    def tearDown(self):
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_happy_path_passes(self):
        conn = make_valid_db(self.db_path)
        db.validate(conn, expected_banks=2)  # must not raise
        conn.close()

    def test_wrong_bank_count_raises(self):
        conn = make_valid_db(self.db_path, n_banks=2)
        with self.assertRaises(AssertionError):
            db.validate(conn, expected_banks=145)
        conn.close()

    def test_the_unique_constraint_itself_blocks_a_duplicate_insert(self):
        # The first line of defense: confirm write_banks_and_metrics'
        # UNIQUE(frn, sheet, row_label, year) constraint actually blocks a
        # duplicate insert at the SQL level, before validate() would ever
        # need to catch one.
        conn = make_valid_db(self.db_path)
        with self.assertRaises(sqlite3.IntegrityError):
            conn.execute(
                "INSERT INTO annual_metrics (frn, sheet, row_label, year, value_raw, "
                "value_numeric, is_numeric) SELECT frn, sheet, row_label, year, "
                "value_raw, value_numeric, is_numeric FROM annual_metrics LIMIT 1"
            )
        conn.close()

    def test_duplicate_identity_key_raises(self):
        # validate()'s duplicate check is a second, independent line of
        # defense - it must catch a duplicate even if something upstream
        # (a future schema change, a bulk-load path that doesn't go
        # through write_banks_and_metrics) ever bypasses the UNIQUE
        # constraint. Reproduced here with a hand-built table that
        # deliberately omits that constraint, to isolate this specific
        # check from the constraint that would otherwise always catch it
        # first in production use.
        conn = sqlite3.connect(self.db_path)
        conn.executescript("""
            CREATE TABLE banks (frn INTEGER PRIMARY KEY, canonical_name TEXT,
                filename_bank_name TEXT, source_workbook TEXT, workbook_kind TEXT, basis_note TEXT);
            CREATE TABLE annual_metrics (id INTEGER PRIMARY KEY, frn INTEGER,
                sheet TEXT, row_label TEXT, year TEXT, value_raw TEXT,
                value_numeric REAL, is_numeric INTEGER);
            CREATE TABLE parent_group_lookup (frn INTEGER PRIMARY KEY, bank_name TEXT,
                immediate_parent TEXT, ultimate_group TEXT, status_caveat TEXT, evidence TEXT);
            CREATE TABLE parent_group_edges (id INTEGER PRIMARY KEY, from_node TEXT,
                edge_type TEXT, to_node TEXT, effective_note TEXT, source TEXT,
                from_frn INTEGER, to_frn INTEGER);
        """)
        conn.execute("INSERT INTO banks VALUES (100, 'Bank Zero', 'BANK0', 'BANK0 FINANCIALS.xlsx', 'full', '')")
        for _ in range(2):
            conn.execute(
                "INSERT INTO annual_metrics (frn, sheet, row_label, year, value_raw, "
                "value_numeric, is_numeric) VALUES (100, 'CET1 Ratio', 'CET1 ratio', 'FY2025', '14.5%', 14.5, 1)"
            )
        conn.commit()
        with self.assertRaises(AssertionError):
            db.validate(conn, expected_banks=1)
        conn.close()

    def test_orphaned_metric_row_raises(self):
        conn = make_valid_db(self.db_path)
        conn.execute(
            "INSERT INTO annual_metrics (frn, sheet, row_label, year, value_raw, "
            "value_numeric, is_numeric) VALUES (999999, 'CET1 Ratio', 'CET1 ratio', "
            "'FY2025', '10%', 10.0, 1)"
        )
        conn.commit()
        with self.assertRaises(AssertionError):
            db.validate(conn, expected_banks=2)
        conn.close()

    def test_wrong_metric_row_count_raises(self):
        conn = make_valid_db(self.db_path)
        with self.assertRaises(AssertionError):
            db.validate(conn, expected_banks=2, expected_metric_rows=999)
        conn.close()

    def test_value_numeric_without_value_raw_raises(self):
        # A missing value must never look numeric - this is the specific
        # invariant CODING_STANDARDS.md's missing-data rule depends on.
        conn = make_valid_db(self.db_path)
        conn.execute("UPDATE annual_metrics SET value_raw = NULL WHERE value_numeric IS NOT NULL")
        conn.commit()
        with self.assertRaises(AssertionError):
            db.validate(conn, expected_banks=2)
        conn.close()

    def test_parent_group_lookup_not_joining_all_banks_raises(self):
        conn = make_valid_db(self.db_path, n_banks=2)
        db.write_parent_group(
            conn,
            lookup_rows=[{"frn": 100, "bank_name": "BANK0", "immediate_parent": "P",
                          "ultimate_group": "G", "status_caveat": "confirmed", "evidence": "test"}],
            edge_rows=[],
        )
        # only 1 of 2 banks has a lookup row - validate() expects ALL banks
        # to be covered once parent_group_lookup is non-empty
        with self.assertRaises(AssertionError):
            db.validate(conn, expected_banks=2)
        conn.close()

    def test_empty_parent_group_lookup_does_not_raise(self):
        # Metrics can be refreshed before parent-group data exists at all
        # (independent refresh domains) - validate() must not treat a
        # completely-empty parent_group_lookup as an error.
        conn = make_valid_db(self.db_path, n_banks=2)
        db.validate(conn, expected_banks=2)  # must not raise
        conn.close()

    def test_failed_refresh_rolls_back_and_preserves_previous_snapshot(self):
        conn = make_valid_db(self.db_path, n_banks=2)
        before = conn.execute(
            "SELECT frn, canonical_name FROM banks ORDER BY frn"
        ).fetchall()
        bad_rows = [{
            "bank": "BROKEN", "canonical_bank": "Broken Ltd",
            "source_filename_bank": "BROKEN", "source_workbook": "BROKEN.xlsx",
            "frn": None, "workbook_kind": "full", "sheet": "CET1 Ratio",
            "row_label": "CET1 ratio", "year": "FY2025", "value_raw": "1%",
            "value_numeric": 1.0, "is_numeric": "1", "basis_note": "",
        }]
        with self.assertRaises(ValueError):
            db.write_banks_and_metrics(conn, bad_rows, metrics_source="broken refresh")
        after = conn.execute(
            "SELECT frn, canonical_name FROM banks ORDER BY frn"
        ).fetchall()
        self.assertEqual(after, before)
        self.assertEqual(conn.execute("SELECT COUNT(*) FROM annual_metrics").fetchone()[0], 2)
        conn.close()


class EquityChangesWriteAndValidate(unittest.TestCase):
    """IN-039: equity_changes is a genuinely different-shaped table
    (chronological roll-forward, not year-keyed) written independently of
    write_banks_and_metrics - covers the write path, refresh_metadata's
    new equity_changes_count column, and validate()'s orphan-FRN check."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp(prefix="equity_changes_test_")
        self.db_path = os.path.join(self.tmpdir, "test.db")

    def tearDown(self):
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def _equity_rows(self, frn):
        return [
            {"frn": frn, "sheet": "Statement of Changes in Equity",
             "movement_label": "Balance as at 1 January 2024", "component": "Share capital",
             "value_raw": 100.0, "value_numeric": 100.0, "is_numeric": "1", "row_order": 0},
            {"frn": frn, "sheet": "Statement of Changes in Equity",
             "movement_label": "Balance as at 1 January 2024", "component": "Retained earnings",
             "value_raw": 50.0, "value_numeric": 50.0, "is_numeric": "1", "row_order": 0},
            {"frn": frn, "sheet": "Statement of Changes in Equity",
             "movement_label": "Profit for the year", "component": "Retained earnings",
             "value_raw": 20.0, "value_numeric": 20.0, "is_numeric": "1", "row_order": 1},
        ]

    def test_write_equity_changes_round_trips_and_updates_refresh_metadata(self):
        conn = make_valid_db(self.db_path)  # writes bank frn=100
        n = db.write_equity_changes(conn, self._equity_rows(100))
        self.assertEqual(n, 3)

        rows = conn.execute(
            "SELECT movement_label, component, value_numeric, row_order "
            "FROM equity_changes ORDER BY row_order, component"
        ).fetchall()
        self.assertEqual(rows, [
            ("Balance as at 1 January 2024", "Retained earnings", 50.0, 0),
            ("Balance as at 1 January 2024", "Share capital", 100.0, 0),
            ("Profit for the year", "Retained earnings", 20.0, 1),
        ])

        count = conn.execute("SELECT equity_changes_count FROM refresh_metadata WHERE id = 1").fetchone()[0]
        self.assertEqual(count, 3)
        conn.close()

    def test_write_equity_changes_replaces_not_appends(self):
        conn = make_valid_db(self.db_path)
        db.write_equity_changes(conn, self._equity_rows(100))
        db.write_equity_changes(conn, self._equity_rows(100)[:1])  # a re-refresh with fewer rows
        n = conn.execute("SELECT COUNT(*) FROM equity_changes").fetchone()[0]
        self.assertEqual(n, 1)  # old rows deleted, not accumulated
        conn.close()

    def test_validate_catches_orphaned_equity_changes_row(self):
        conn = make_valid_db(self.db_path)  # only frn=100,101 exist in banks
        db.write_equity_changes(conn, self._equity_rows(999))  # unknown frn
        with self.assertRaises(AssertionError):
            db.validate(conn, expected_banks=2)
        conn.close()

    def test_migration_adds_equity_changes_table_and_refresh_metadata_column(self):
        # A pre-IN-039 database has no equity_changes table at all, and
        # refresh_metadata (if it already existed) has no
        # equity_changes_count column - connect() must add both without
        # touching existing data, same guarantee as MigrateAddColumns below.
        conn = sqlite3.connect(self.db_path)
        conn.executescript("""
            CREATE TABLE banks (
                frn INTEGER PRIMARY KEY, canonical_name TEXT NOT NULL,
                filename_bank_name TEXT NOT NULL, source_workbook TEXT NOT NULL,
                workbook_kind TEXT NOT NULL, basis_note TEXT
            );
            CREATE TABLE refresh_metadata (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                metrics_built_at TEXT, metrics_source TEXT,
                banks_count INTEGER, annual_metrics_count INTEGER
            );
        """)
        conn.execute("INSERT INTO banks VALUES (100, 'Bank Zero Ltd', 'BANK0', 'BANK0 FINANCIALS.xlsx', 'full', NULL)")
        conn.execute("INSERT INTO refresh_metadata (id, banks_count) VALUES (1, 1)")
        conn.commit()
        conn.close()

        conn = db.connect(self.db_path)
        tables = {row[0] for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        self.assertIn("equity_changes", tables)
        columns = {row[1] for row in conn.execute("PRAGMA table_info(refresh_metadata)")}
        self.assertIn("equity_changes_count", columns)
        # pre-existing refresh_metadata row untouched
        banks_count = conn.execute("SELECT banks_count FROM refresh_metadata WHERE id = 1").fetchone()[0]
        self.assertEqual(banks_count, 1)
        conn.close()


class ValidateClusterInputs(unittest.TestCase):
    """validate_cluster_inputs() is the staleness/FRN-mismatch guard both
    deliverable generators call before embedding cluster data - verified
    manually in-session twice while building it, never as an automated test."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp(prefix="validate_cluster_test_")
        self.db_path = os.path.join(self.tmpdir, "test.db")
        self.cluster_path = os.path.join(self.tmpdir, "clusters.csv")
        self.centroids_path = os.path.join(self.tmpdir, "centroids.csv")

        conn = make_valid_db(self.db_path, n_banks=2)
        conn.close()
        with open(self.cluster_path, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["frn", "bank", "cluster_id"])
            w.writerow(["100", "BANK0", "0"])
            w.writerow(["101", "BANK1", "0"])
        with open(self.centroids_path, "w") as f:
            f.write("cluster_id,cluster_size\n0,2\n")

    def tearDown(self):
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def _cluster_rows(self):
        with open(self.cluster_path, newline="") as f:
            return list(csv.DictReader(f))

    def test_matching_fresh_inputs_pass(self):
        db.validate_cluster_inputs(self.db_path, self._cluster_rows(), self.cluster_path, self.centroids_path)

    def test_mismatched_frn_set_raises(self):
        with open(self.cluster_path, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["frn", "bank", "cluster_id"])
            w.writerow(["100", "BANK0", "0"])
            w.writerow(["999999", "GHOST BANK", "0"])  # not in the DB
        with self.assertRaises(ValueError):
            db.validate_cluster_inputs(self.db_path, self._cluster_rows(), self.cluster_path, self.centroids_path)

    def test_missing_centroids_file_raises(self):
        os.remove(self.centroids_path)
        with self.assertRaises(FileNotFoundError):
            db.validate_cluster_inputs(self.db_path, self._cluster_rows(), self.cluster_path, self.centroids_path)

    def test_no_centroids_path_skips_that_check(self):
        # build_in006_pdf.py doesn't use centroids at all - confirm the
        # centroids checks are skipped, not silently required, when None.
        os.remove(self.centroids_path)
        db.validate_cluster_inputs(self.db_path, self._cluster_rows(), self.cluster_path, centroids_path=None)

    def test_stale_cluster_output_raises(self):
        conn = sqlite3.connect(self.db_path)
        conn.execute("UPDATE refresh_metadata SET metrics_built_at = ? WHERE id = 1",
                     (time.strftime("%Y-%m-%dT%H:%M:%S+00:00", time.gmtime(time.time() + 3600)),))
        conn.commit()
        conn.close()
        with self.assertRaises(ValueError):
            db.validate_cluster_inputs(self.db_path, self._cluster_rows(), self.cluster_path, self.centroids_path)


class MigrateAddColumns(unittest.TestCase):
    """The idempotent ALTER-TABLE migration that adds unit/reporting_basis/
    restatement_note/source_note/effective_from/effective_to onto an
    EXISTING database with the old schema - "preserve current data during
    migration" is the whole point, verified here against a database that
    genuinely predates those columns, not just a freshly-created one where
    CREATE TABLE IF NOT EXISTS would already include them."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp(prefix="migration_test_")
        self.db_path = os.path.join(self.tmpdir, "old_schema.db")

    def tearDown(self):
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def _build_old_schema_db(self):
        """Hand-builds a database with the ORIGINAL (pre-item-5) schema -
        no unit/reporting_basis/restatement_note/source_note/effective_from/
        effective_to columns at all - with real data in it."""
        conn = sqlite3.connect(self.db_path)
        conn.executescript("""
            CREATE TABLE banks (
                frn INTEGER PRIMARY KEY, canonical_name TEXT NOT NULL,
                filename_bank_name TEXT NOT NULL, source_workbook TEXT NOT NULL,
                workbook_kind TEXT NOT NULL, basis_note TEXT
            );
            CREATE TABLE annual_metrics (
                id INTEGER PRIMARY KEY, frn INTEGER NOT NULL REFERENCES banks(frn),
                sheet TEXT NOT NULL, row_label TEXT NOT NULL, year TEXT NOT NULL,
                value_raw TEXT, value_numeric REAL, is_numeric INTEGER NOT NULL,
                UNIQUE(frn, sheet, row_label, year)
            );
            CREATE TABLE parent_group_edges (
                id INTEGER PRIMARY KEY, from_node TEXT NOT NULL, edge_type TEXT NOT NULL,
                to_node TEXT NOT NULL, effective_note TEXT, source TEXT,
                from_frn INTEGER REFERENCES banks(frn), to_frn INTEGER REFERENCES banks(frn)
            );
        """)
        conn.execute("INSERT INTO banks VALUES (100, 'Bank Zero Ltd', 'BANK0', 'BANK0 FINANCIALS.xlsx', 'full', 'test basis')")
        conn.execute(
            "INSERT INTO annual_metrics (frn, sheet, row_label, year, value_raw, value_numeric, is_numeric) "
            "VALUES (100, 'CET1 Ratio', 'CET1 ratio', 'FY2025', '14.5%', 14.5, 1)"
        )
        conn.execute(
            "INSERT INTO parent_group_edges (from_node, edge_type, to_node, effective_note, source) "
            "VALUES ('BANK0', 'owned_by', 'Parent Co', 'from 2023-05-19', 'CH')"
        )
        conn.commit()
        conn.close()

    def test_migration_preserves_existing_data_and_adds_columns(self):
        self._build_old_schema_db()
        pre_columns = {"id", "frn", "sheet", "row_label", "year", "value_raw", "value_numeric", "is_numeric"}

        conn = db.connect(self.db_path)  # this triggers _migrate_add_columns()

        post_columns = {row[1] for row in conn.execute("PRAGMA table_info(annual_metrics)")}
        self.assertTrue(pre_columns.issubset(post_columns))
        for new_col in ("unit", "reporting_basis", "restatement_note", "source_note"):
            self.assertIn(new_col, post_columns)

        edge_columns = {row[1] for row in conn.execute("PRAGMA table_info(parent_group_edges)")}
        for new_col in ("effective_from", "effective_to"):
            self.assertIn(new_col, edge_columns)

        # the existing row's original data must be untouched
        row = conn.execute(
            "SELECT frn, sheet, row_label, year, value_raw, value_numeric, is_numeric, unit "
            "FROM annual_metrics WHERE frn = 100"
        ).fetchone()
        self.assertEqual(row, (100, "CET1 Ratio", "CET1 ratio", "FY2025", "14.5%", 14.5, 1, None))

        bank_row = conn.execute("SELECT frn, canonical_name, basis_note FROM banks WHERE frn = 100").fetchone()
        self.assertEqual(bank_row, (100, "Bank Zero Ltd", "test basis"))

        edge_row = conn.execute(
            "SELECT from_node, effective_note, effective_from FROM parent_group_edges"
        ).fetchone()
        self.assertEqual(edge_row, ("BANK0", "from 2023-05-19", None))  # not backfilled by migration alone
        conn.close()

    def test_migration_is_idempotent(self):
        self._build_old_schema_db()
        conn1 = db.connect(self.db_path)
        conn1.close()
        # second connect() on an already-migrated DB must not error
        conn2 = db.connect(self.db_path)
        columns = {row[1] for row in conn2.execute("PRAGMA table_info(annual_metrics)")}
        self.assertIn("unit", columns)
        conn2.close()


class ParseEffectiveFrom(unittest.TestCase):
    """_parse_effective_from()'s conservative "from <date>" regex - only
    ever exercised via write_parent_group() integration tests before, with
    one matching and one non-matching case. These are the edge cases."""

    def test_full_iso_date(self):
        self.assertEqual(db._parse_effective_from("from 2023-05-19"), "2023-05-19")

    def test_year_and_month_only(self):
        self.assertEqual(db._parse_effective_from("from 2024-07"), "2024-07")

    def test_year_only(self):
        self.assertEqual(db._parse_effective_from("from 2024 conversion"), "2024")

    def test_case_insensitive(self):
        self.assertEqual(db._parse_effective_from("From 2023-05-19"), "2023-05-19")
        self.assertEqual(db._parse_effective_from("FROM 2023-05-19"), "2023-05-19")

    def test_embedded_mid_sentence(self):
        self.assertEqual(
            db._parse_effective_from("60% JV from 2021-04-20; prior structure retained"),
            "2021-04-20",
        )

    def test_no_from_phrase_returns_none(self):
        self.assertIsNone(db._parse_effective_from("liquidity scope"))
        self.assertIsNone(db._parse_effective_from("60% JV"))
        self.assertIsNone(db._parse_effective_from("current"))

    def test_none_input_returns_none(self):
        self.assertIsNone(db._parse_effective_from(None))

    def test_empty_string_returns_none(self):
        self.assertIsNone(db._parse_effective_from(""))

    def test_bare_year_without_from_is_not_matched(self):
        # deliberately conservative - a bare year mentioned in prose isn't
        # an effective-date claim, only an explicit "from <date>" is.
        self.assertIsNone(db._parse_effective_from("acquired in 2023, integrated by 2024"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
