"""
Regression tests for scripts/extract_metrics.py (wayfinder/insights/ ticket
IN-001). Run with:

    python3 scripts/test_extract_metrics.py

No pytest dependency - plain unittest (stdlib) so it runs in this project's
bare-Python environment (no sklearn/scipy/pytest installed, confirmed while
building IN-001/IN-003).

Covers, per the follow-up spec that added canonical_bank/source_workbook/
identity-key deduplication/schema versioning to this tool:
  - sibling-entity disambiguation (Barclays/HSBC) - uses the REAL workbooks
    in banks/, since these are the exact regression case that was found and
    fixed while building extract_metrics.py in the first place; skipped
    gracefully if banks/ isn't present rather than failing the whole suite.
  - duplicate identical totals collapse to one row
  - conflicting duplicates raise a clear, informative error
  - percentage-string parsing
  - missing values stay genuinely missing (never coerced to 0)

Synthetic fixtures are built with the real BankWorkbook class from
bank_workbook.py (not hand-rolled openpyxl), so they exercise the exact
styling/structure conventions (bold TOTAL rows, header row position, etc.)
every real bank build script also goes through - not a simplified stand-in.
"""

import csv
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(__file__))
# bank_workbook.py lives in scripts/, one level up from scripts/insights/.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from bank_workbook import BankWorkbook
from extract_metrics import (
    deduplicate,
    get_entity_title,
    load_bank_list,
    match_frn,
    parse_numeric,
    process_workbook,
)

import openpyxl
import sqlite3

import build_insights_db

BANKS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "banks")


class PercentAndMissingValueParsing(unittest.TestCase):
    """Percentage parsing and missing-value handling - the two column-level
    behaviours the spec asked to be covered, tested directly against
    parse_numeric() (no workbook needed)."""

    def test_percent_string_parses_to_float(self):
        self.assertEqual(parse_numeric("14.5%"), 14.5)
        self.assertEqual(parse_numeric("-2.3%"), -2.3)
        self.assertEqual(parse_numeric("1,234.5%"), 1234.5)

    def test_plain_number_passes_through(self):
        self.assertEqual(parse_numeric(1286.5), 1286.5)
        self.assertEqual(parse_numeric(-40.2), -40.2)

    def test_non_numeric_string_is_missing_not_zero(self):
        self.assertIsNone(parse_numeric("Not publicly disclosed"))

    def test_none_is_missing_not_zero(self):
        self.assertIsNone(parse_numeric(None))


class DeduplicationBehaviour(unittest.TestCase):
    """Exercises deduplicate() directly with hand-built row dicts - the
    identity-key dedup logic itself, independent of any workbook."""

    def _row(self, frn, bank, sheet, label, year, value_raw):
        return {
            "bank": bank, "canonical_bank": bank, "source_filename_bank": bank,
            "source_workbook": f"{bank} FINANCIALS.xlsx", "frn": frn,
            "workbook_kind": "full", "sheet": sheet, "row_label": label,
            "year": year, "value_raw": value_raw,
            "value_numeric": value_raw if isinstance(value_raw, float) else "",
            "is_numeric": "1" if isinstance(value_raw, float) else "0",
            "basis_note": "",
        }

    def test_identical_duplicate_collapses_to_one_row(self):
        rows = [
            self._row(111, "TESTBANK", "Cash Flow Statement",
                      "Cash and cash equivalents at end of year", "FY2025", 1286.5),
            self._row(111, "TESTBANK", "Cash Flow Statement",
                      "Cash and cash equivalents at end of year", "FY2025", 1286.5),
        ]
        deduped, n_dup_groups, fallback = deduplicate(rows)
        self.assertEqual(len(deduped), 1)
        self.assertEqual(n_dup_groups, 1)
        self.assertEqual(fallback, set())

    def test_conflicting_duplicate_raises_with_useful_detail(self):
        rows = [
            self._row(222, "TESTBANK2", "Cash Flow Statement",
                      "Cash and cash equivalents at end of year", "FY2025", 100.0),
            self._row(222, "TESTBANK2", "Cash Flow Statement",
                      "Cash and cash equivalents at end of year", "FY2025", 999.0),
        ]
        with self.assertRaises(ValueError) as ctx:
            deduplicate(rows)
        msg = str(ctx.exception)
        self.assertIn("222", msg)
        self.assertIn("Cash Flow Statement", msg)
        self.assertIn("Cash and cash equivalents at end of year", msg)
        self.assertIn("FY2025", msg)

    def test_duplicate_agreeing_on_value_but_disagreeing_on_unit_raises(self):
        # Regression: two rows sharing an identity key that agree on
        # value_raw but disagree on unit/reporting_basis used to collapse
        # silently to group[0] - exactly the field class already responsible
        # for three confirmed pipeline bugs (wrong unit/basis attribution).
        rows = [
            {**self._row(333, "TESTBANK3", "Leverage Ratio", "UK leverage ratio", "FY2025", 5.2),
             "unit": "%", "reporting_basis": "entity"},
            {**self._row(333, "TESTBANK3", "Leverage Ratio", "UK leverage ratio", "FY2025", 5.2),
             "unit": "", "reporting_basis": "consolidated_group"},
        ]
        with self.assertRaises(ValueError) as ctx:
            deduplicate(rows)
        msg = str(ctx.exception)
        self.assertIn("333", msg)
        self.assertIn("unit", msg)

    def test_identity_key_is_frn_not_bank(self):
        # Two rows with the SAME frn but DIFFERENT `bank` (simulating a
        # filename rename) must still be treated as the same identity and
        # deduplicated together, per the "use FRN not filename" spec.
        rows = [
            self._row(333, "OLD FILENAME", "LCR", "Liquidity coverage ratio", "FY2024", "150.0%"),
            self._row(333, "NEW FILENAME", "LCR", "Liquidity coverage ratio", "FY2024", "150.0%"),
        ]
        deduped, n_dup_groups, fallback = deduplicate(rows)
        self.assertEqual(len(deduped), 1)
        self.assertEqual(n_dup_groups, 1)

    def test_missing_frn_falls_back_to_bank_and_is_logged(self):
        rows = [
            self._row("", "UNMATCHED BANK", "LCR", "Liquidity coverage ratio", "FY2024", "100.0%"),
        ]
        deduped, n_dup_groups, fallback = deduplicate(rows)
        self.assertEqual(len(deduped), 1)
        self.assertIn("UNMATCHED BANK", fallback)


class SiblingEntityDisambiguation(unittest.TestCase):
    """The exact regression class this tool was built to catch: two banks
    with near-identical filenames that are legally distinct entities. Uses
    the real Barclays/HSBC workbooks already in banks/ - these ARE the
    original repro case, not a stand-in for it."""

    @classmethod
    def setUpClass(cls):
        cls.have_fixtures = os.path.isdir(BANKS_DIR)

    def test_barclays_siblings_resolve_to_different_frns(self):
        path_a = os.path.join(BANKS_DIR, "BARCLAYS FINANCIALS.xlsx")
        path_b = os.path.join(BANKS_DIR, "BARCLAYS BANK PLC FINANCIALS.xlsx")
        if not (os.path.exists(path_a) and os.path.exists(path_b)):
            self.skipTest("banks/BARCLAYS* fixtures not present")
        bank_list = load_bank_list()
        _, frn_a, _, _, _, _, _ = process_workbook(path_a, bank_list)
        _, frn_b, _, _, _, _, _ = process_workbook(path_b, bank_list)
        self.assertIsNotNone(frn_a)
        self.assertIsNotNone(frn_b)
        self.assertNotEqual(frn_a, frn_b, "Barclays Bank UK and Barclays Bank PLC must not collide")

    def test_hsbc_siblings_resolve_to_different_frns(self):
        path_a = os.path.join(BANKS_DIR, "HSBC BANK PLC FINANCIALS.xlsx")
        path_b = os.path.join(BANKS_DIR, "HSBC UK BANK PLC FINANCIALS.xlsx")
        if not (os.path.exists(path_a) and os.path.exists(path_b)):
            self.skipTest("banks/HSBC* fixtures not present")
        bank_list = load_bank_list()
        _, frn_a, _, _, _, _, _ = process_workbook(path_a, bank_list)
        _, frn_b, _, _, _, _, _ = process_workbook(path_b, bank_list)
        self.assertIsNotNone(frn_a)
        self.assertIsNotNone(frn_b)
        self.assertNotEqual(frn_a, frn_b, "HSBC Bank plc and HSBC UK Bank plc must not collide")

    def test_entity_title_disambiguates_before_frn_matching(self):
        # Lower-level check: the sheet-title entity name (not the filename)
        # is what get_entity_title() must return, since that's the whole
        # fix - filename alone can't tell these entities apart.
        path_a = os.path.join(BANKS_DIR, "BARCLAYS FINANCIALS.xlsx")
        path_b = os.path.join(BANKS_DIR, "BARCLAYS BANK PLC FINANCIALS.xlsx")
        if not (os.path.exists(path_a) and os.path.exists(path_b)):
            self.skipTest("banks/BARCLAYS* fixtures not present")
        wb_a = openpyxl.load_workbook(path_a, read_only=True)
        wb_b = openpyxl.load_workbook(path_b, read_only=True)
        title_a = get_entity_title(wb_a)
        title_b = get_entity_title(wb_b)
        self.assertNotEqual(title_a, title_b)
        self.assertIn("UK", title_a)
        self.assertNotIn("UK", title_b)


class SyntheticWorkbookExtraction(unittest.TestCase):
    """Builds small throwaway workbooks with the real BankWorkbook class in
    a temp dir, so the duplicate-total and missing-value cases are tested
    end-to-end through process_workbook() too, not just deduplicate()."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp(prefix="extract_metrics_test_")
        self.bank_list = []  # deliberately empty: these fake banks aren't in
        # Banks List 2608.xlsx, so frn will be None - not the focus here.

    def tearDown(self):
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def _build(self, bank_name, cf_rows):
        bw = BankWorkbook(bank_name=bank_name, years=["FY2025", "FY2024"], header_color="336699")
        bw.add_cash_flow_sheet(
            title=f"{bank_name} — Cash Flow Statement",
            subtitle="Test fixture",
            rows=cf_rows,
            sources_text="Test fixture - not a real source.",
        )
        path = os.path.join(self.tmpdir, f"{bank_name} FINANCIALS.xlsx")
        bw.save(path)
        return path

    def test_duplicate_total_rows_in_one_workbook_are_identical_and_collapse(self):
        rows = [
            ("TOTAL", "Cash and cash equivalents at end of year",
             {"FY2025": 500.0, "FY2024": 400.0}),
            ("TOTAL", "Cash and cash equivalents at end of year comprise (restated)",
             {"FY2025": 500.0, "FY2024": 400.0}),
        ]
        # Give both TOTAL rows the SAME label to reproduce the real pattern
        # (Allica's "Cash and cash equivalents at end of year" appearing
        # twice, both bold, both identical) rather than two different labels.
        rows[1] = ("TOTAL", "Cash and cash equivalents at end of year", rows[1][2])
        path = self._build("DUPTESTBANK", rows)
        _, _, _, _, _, extracted_rows, _ = process_workbook(path, self.bank_list)
        deduped, n_dup_groups, _ = deduplicate(extracted_rows)
        self.assertEqual(n_dup_groups, 2)  # one group per year (FY2025, FY2024)
        self.assertEqual(len(deduped), 2)  # collapsed to 1 row per year

    def test_metric_sheet_note_and_source_are_captured(self):
        bw = BankWorkbook(bank_name="NOTETESTBANK", years=["FY2025", "FY2024"], header_color="336699")
        bw.add_metric_sheet(
            "CET1 Ratio", "% of RWA",
            [("Common Equity Tier 1 (CET1) ratio", {"FY2025": "14.5%", "FY2024": "13.9%"})],
            sources_text="Test source citation - CET1 Ratio Report 2025, p.1.",
            note="FY2024 restated from 13.2% following a methodology change.",
        )
        path = os.path.join(self.tmpdir, "NOTETESTBANK FINANCIALS.xlsx")
        bw.save(path)
        _, _, _, _, _, extracted_rows, _ = process_workbook(path, self.bank_list)
        self.assertEqual(len(extracted_rows), 2)
        for row in extracted_rows:
            self.assertEqual(row["restatement_note"], "FY2024 restated from 13.2% following a methodology change.")
            self.assertIn("Test source citation", row["source_note"])
            self.assertEqual(row["unit"], "")  # ratio sheets don't get a separate unit
            self.assertEqual(row["reporting_basis"], "")  # deliberately not populated yet

    def test_cash_flow_unit_suffix_is_captured(self):
        rows = [("TOTAL", "Net cash from operating activities", {"FY2025": 100.0, "FY2024": 90.0})]
        bw = BankWorkbook(bank_name="UNITTESTBANK", years=["FY2025", "FY2024"], header_color="336699")
        bw.add_cash_flow_sheet(
            title="UNITTESTBANK — Cash Flow Statement", subtitle="Test fixture",
            rows=rows, sources_text="Test fixture.", unit_suffix=" (£m)",
        )
        path = os.path.join(self.tmpdir, "UNITTESTBANK FINANCIALS.xlsx")
        bw.save(path)
        _, _, _, _, _, extracted_rows, _ = process_workbook(path, self.bank_list)
        self.assertEqual(len(extracted_rows), 2)
        for row in extracted_rows:
            self.assertEqual(row["unit"], "£m")
            self.assertEqual(row["restatement_note"], "")  # no Note:/Note-equivalent convention for CF
            self.assertIn("Test fixture", row["source_note"])

    def test_missing_year_stays_missing_not_zero(self):
        rows = [
            ("TOTAL", "Net cash from operating activities",
             {"FY2025": 100.0}),  # FY2024 deliberately omitted
        ]
        path = self._build("MISSINGYEARBANK", rows)
        _, _, _, _, _, extracted_rows, _ = process_workbook(path, self.bank_list)
        fy2024_rows = [r for r in extracted_rows if r["year"] == "FY2024"]
        self.assertEqual(len(fy2024_rows), 1)
        self.assertEqual(fy2024_rows[0]["value_raw"], "")
        self.assertEqual(fy2024_rows[0]["is_numeric"], "0")
        fy2025_rows = [r for r in extracted_rows if r["year"] == "FY2025"]
        self.assertEqual(fy2025_rows[0]["value_numeric"], 100.0)


class DatabaseRoundTrip(unittest.TestCase):
    """IN-008: extract_metrics.py now writes to the database first and
    exports the CSV FROM it (not independently). These tests exercise that
    round trip directly - in-memory rows -> DB -> exported CSV -> re-parsed
    - without touching the real research/insights.db, using a throwaway
    temp-file database instead."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp(prefix="db_roundtrip_test_")
        self.db_path = os.path.join(self.tmpdir, "test.db")
        self.csv_path = os.path.join(self.tmpdir, "test.csv")

    def tearDown(self):
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def _row(self, frn, bank, sheet, label, year, value_raw, value_numeric, is_numeric):
        return {
            "bank": bank, "canonical_bank": f"{bank} Canonical Ltd",
            "source_filename_bank": bank, "source_workbook": f"{bank} FINANCIALS.xlsx",
            "frn": frn, "workbook_kind": "full", "sheet": sheet, "row_label": label,
            "year": year, "value_raw": value_raw, "value_numeric": value_numeric,
            "is_numeric": is_numeric, "basis_note": "Test basis note",
        }

    def test_round_trip_preserves_values_including_missing(self):
        rows = [
            self._row(111, "ALPHA", "CET1 Ratio", "CET1 ratio", "FY2025", "14.5%", 14.5, "1"),
            self._row(111, "ALPHA", "CET1 Ratio", "CET1 ratio", "FY2024", "", "", "0"),  # missing
            self._row(222, "BETA", "LCR", "LCR", "FY2025", "Not publicly disclosed", "", "0"),
        ]
        conn = build_insights_db.connect(self.db_path)
        n_banks, n_metrics = build_insights_db.write_banks_and_metrics(conn, rows, metrics_source="test")
        self.assertEqual(n_banks, 2)
        self.assertEqual(n_metrics, 3)
        n_exported = build_insights_db.export_metrics_csv(conn, self.csv_path)
        conn.close()
        self.assertEqual(n_exported, 3)

        with open(self.csv_path, newline="", encoding="utf-8") as f:
            exported = list(csv.DictReader(f))
        by_year = {r["year"]: r for r in exported if r["bank"] == "ALPHA"}
        self.assertEqual(by_year["FY2025"]["value_raw"], "14.5%")
        self.assertEqual(by_year["FY2025"]["value_numeric"], "14.5")
        self.assertEqual(by_year["FY2025"]["is_numeric"], "1")
        # the missing year must round-trip as genuinely blank, never "0" or "0.0"
        self.assertEqual(by_year["FY2024"]["value_raw"], "")
        self.assertEqual(by_year["FY2024"]["value_numeric"], "")
        self.assertEqual(by_year["FY2024"]["is_numeric"], "0")

    def test_sibling_entities_stay_distinct_through_the_round_trip(self):
        rows = [
            self._row(759676, "BARCLAYS", "CET1 Ratio", "CET1 ratio", "FY2025", "14.5%", 14.5, "1"),
            self._row(122702, "BARCLAYS BANK PLC", "CET1 Ratio", "CET1 ratio", "FY2025", "13.1%", 13.1, "1"),
        ]
        conn = build_insights_db.connect(self.db_path)
        build_insights_db.write_banks_and_metrics(conn, rows, metrics_source="test")
        banks = {r[0]: r[1] for r in conn.execute("SELECT frn, filename_bank_name FROM banks")}
        conn.close()
        self.assertEqual(banks, {759676: "BARCLAYS", 122702: "BARCLAYS BANK PLC"})

    def test_refreshing_metrics_does_not_touch_existing_parent_group_tables(self):
        # This is the specific safety property IN-008 depends on: extract_
        # metrics.py must be able to refresh banks/annual_metrics without
        # wiping out IN-002's already-written parent-group data.
        conn = build_insights_db.connect(self.db_path)
        build_insights_db.write_banks_and_metrics(
            conn, [self._row(111, "ALPHA", "CET1 Ratio", "CET1 ratio", "FY2025", "14.5%", 14.5, "1")],
            metrics_source="test",
        )
        build_insights_db.write_parent_group(
            conn,
            lookup_rows=[{"frn": 111, "bank_name": "ALPHA", "immediate_parent": "Parent Co",
                          "ultimate_group": "Parent Group", "status_caveat": "confirmed", "evidence": "test"}],
            edge_rows=[],
        )
        conn.close()

        # Re-run write_banks_and_metrics (simulating a refresh) - the same FRN
        # is still present, so parent_group_lookup should still join cleanly.
        conn = build_insights_db.connect(self.db_path)
        build_insights_db.write_banks_and_metrics(
            conn, [self._row(111, "ALPHA", "CET1 Ratio", "CET1 ratio", "FY2025", "14.7%", 14.7, "1")],
            metrics_source="test refresh",
        )
        n_lookup = conn.execute("SELECT COUNT(*) FROM parent_group_lookup").fetchone()[0]
        joined = conn.execute(
            "SELECT COUNT(*) FROM parent_group_lookup pgl JOIN banks b ON b.frn = pgl.frn"
        ).fetchone()[0]
        updated_value = conn.execute(
            "SELECT value_raw FROM annual_metrics WHERE frn = 111"
        ).fetchone()[0]
        conn.close()
        self.assertEqual(n_lookup, 1, "parent_group_lookup must survive a banks/annual_metrics refresh")
        self.assertEqual(joined, 1)
        self.assertEqual(updated_value, "14.7%", "the refreshed value should be the new one, not stale")

    def test_conflicting_duplicate_in_db_write_raises(self):
        # write_banks_and_metrics relies on deduplicate() having already run
        # (extract_metrics.py's main() calls it first) - this test confirms
        # the DB layer doesn't silently swallow a UNIQUE constraint violation
        # if that invariant is ever broken upstream.
        rows = [
            self._row(111, "ALPHA", "CET1 Ratio", "CET1 ratio", "FY2025", "14.5%", 14.5, "1"),
            self._row(111, "ALPHA", "CET1 Ratio", "CET1 ratio", "FY2025", "99.9%", 99.9, "1"),
        ]
        conn = build_insights_db.connect(self.db_path)
        with self.assertRaises(sqlite3.IntegrityError):
            build_insights_db.write_banks_and_metrics(conn, rows, metrics_source="test")
        conn.close()

    def test_db_loader_preserves_metadata_columns(self):
        row = self._row(111, "ALPHA", "Cash Flow Statement", "Operating cash flow",
                        "FY2025", "100", 100.0, "1")
        row.update({
            "unit": "£m",
            "reporting_basis": "entity",
            "restatement_note": "FY2024 comparative restated",
            "source_note": "Annual Report 2025, p. 42",
        })
        conn = build_insights_db.connect(self.db_path)
        build_insights_db.write_banks_and_metrics(conn, [row], metrics_source="test")
        loaded = build_insights_db.load_rows_from_db(self.db_path)[0]
        conn.close()
        for key in ("unit", "reporting_basis", "restatement_note", "source_note"):
            self.assertEqual(loaded[key], row[key])

    def test_write_parent_group_populates_effective_from(self):
        # Covers item 5's structured effective_from/effective_to columns -
        # conservative "from <date>" extraction, never a guess.
        conn = build_insights_db.connect(self.db_path)
        build_insights_db.write_banks_and_metrics(
            conn, [self._row(111, "ALPHA", "CET1 Ratio", "CET1 ratio", "FY2025", "14.5%", 14.5, "1")],
            metrics_source="test",
        )
        build_insights_db.write_parent_group(
            conn,
            lookup_rows=[{"frn": 111, "bank_name": "ALPHA", "immediate_parent": "Parent Co",
                          "ultimate_group": "Parent Group", "status_caveat": "confirmed", "evidence": "test"}],
            edge_rows=[
                {"from_node": "ALPHA", "edge_type": "owned_by", "to_node": "Parent Co",
                 "effective_note": "from 2023-05-19", "source": "CH"},
                {"from_node": "ALPHA", "edge_type": "regulatory_consolidated_into", "to_node": "UK DoLSub",
                 "effective_note": "liquidity scope", "source": "AR"},
            ],
        )
        rows = conn.execute(
            "SELECT effective_note, effective_from, effective_to FROM parent_group_edges ORDER BY id"
        ).fetchall()
        conn.close()
        self.assertEqual(rows[0], ("from 2023-05-19", "2023-05-19", None))
        self.assertEqual(rows[1], ("liquidity scope", None, None))  # no "from <date>" phrase - left NULL, not guessed

    def test_load_groups_from_db_matches_load_rows_from_db_shape(self):
        # Covers the shared loader added for IN-008 item 3
        # (scripts/analyze_trends.py, scripts/review_trend_selection.py) -
        # load_groups_from_db() must return the same {frn_str: (bank_name,
        # ultimate_group, status_caveat)} shape analyze_trends.load_groups()
        # produces from markdown, keyed by the same string FRN load_rows_from_db
        # uses, so a consumer can join the two without type mismatches.
        conn = build_insights_db.connect(self.db_path)
        build_insights_db.write_banks_and_metrics(
            conn, [self._row(111, "ALPHA", "CET1 Ratio", "CET1 ratio", "FY2025", "14.5%", 14.5, "1")],
            metrics_source="test",
        )
        build_insights_db.write_parent_group(
            conn,
            lookup_rows=[{"frn": 111, "bank_name": "ALPHA", "immediate_parent": "Parent Co",
                          "ultimate_group": "Parent Group", "status_caveat": "confirmed", "evidence": "test"}],
            edge_rows=[],
        )
        conn.close()

        groups = build_insights_db.load_groups_from_db(self.db_path)
        metrics_rows = build_insights_db.load_rows_from_db(self.db_path)
        self.assertEqual(groups, {"111": ("ALPHA", "Parent Group", "confirmed")})
        # the FRN key type must match load_rows_from_db's string FRNs exactly
        self.assertEqual(set(groups.keys()), {r["frn"] for r in metrics_rows})

    def test_multi_entity_groups_returns_frn_alongside_bank_name(self):
        # Regression test for a real bug found while building the
        # deliverable-generator fixes: parent_group_lookup.bank_name
        # ("Santander UK") and a cluster CSV's filename-derived name
        # ("SANTANDER") are two different, both-legitimate spellings for
        # the same entity. A first version of the deliverable code joined
        # group membership back to cluster data by normalized NAME and
        # silently dropped members whose spelling differed between the two
        # sources. multi_entity_groups() must return FRN alongside each
        # bank_name specifically so a consumer can join by the stable key
        # instead - this test would have caught that regression.
        groups = {
            "111": ("Santander UK", "Banco Santander S.A.", "confirmed"),
            "222": ("Santander Financial Services", "Banco Santander S.A.", "confirmed"),
            "333": ("Solo Bank", "Solo Bank", "confirmed"),  # single-entity - excluded
        }
        multi = build_insights_db.multi_entity_groups(groups)
        self.assertEqual(len(multi), 1)
        group_name, members = multi[0]
        self.assertEqual(group_name, "Banco Santander S.A.")
        self.assertEqual(set(members), {("111", "Santander UK"), ("222", "Santander Financial Services")})

    def test_multi_entity_groups_excludes_below_min_size(self):
        groups = {"111": ("Alpha", "Solo Group", "confirmed")}
        self.assertEqual(build_insights_db.multi_entity_groups(groups), [])

    def test_cluster_size_summary(self):
        rows = [
            {"cluster_id": "0", "insufficient_data": "0"},
            {"cluster_id": "0", "insufficient_data": "0"},
            {"cluster_id": "1", "insufficient_data": "0"},
            {"cluster_id": "", "insufficient_data": "1"},
        ]
        sizes, insufficient = build_insights_db.cluster_size_summary(rows)
        self.assertEqual(sizes, {"0": 2, "1": 1})
        self.assertEqual(insufficient, 1)


class CorruptWorkbookErrorContinuation(unittest.TestCase):
    """main()'s per-workbook try/except (catch, log, continue) had no test
    at all - only ever exercised against the real banks/ directory, which
    is always clean by construction, so this path had literally never run
    in any test. Uses the new --banks-dir override (added alongside this
    test, for exactly this reason) to point at a small fixture directory
    with one genuinely corrupt file and one good one."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp(prefix="corrupt_workbook_test_")
        self.banks_dir = os.path.join(self.tmpdir, "banks")
        os.makedirs(self.banks_dir)
        self.db_path = os.path.join(self.tmpdir, "test.db")
        self.out_path = os.path.join(self.tmpdir, "test.csv")

        # a genuinely corrupt "workbook" - not a valid zip/xlsx at all
        with open(os.path.join(self.banks_dir, "CORRUPT FINANCIALS.xlsx"), "wb") as f:
            f.write(b"this is not a real xlsx file, just plain bytes\x00\x01\x02")

        # A real, valid, minimal workbook alongside it - named after a real
        # Banks List 2608.xlsx entity so it resolves an FRN successfully,
        # isolating this test to the corrupt-FILE path specifically (an
        # unmatched-FRN row is a separate, already-hard-required failure
        # mode in write_banks_and_metrics(), not what's being tested here).
        bw = BankWorkbook(bank_name="ABC International Bank Plc", years=["FY2025"], header_color="336699")
        bw.add_cash_flow_sheet(
            title="ABC International Bank Plc — Cash Flow Statement", subtitle="Test fixture",
            rows=[("TOTAL", "Net cash from operating activities", {"FY2025": 100.0})],
            sources_text="Test fixture.",
        )
        bw.save(os.path.join(self.banks_dir, "ABC INTERNATIONAL BANK FINANCIALS.xlsx"))

    def tearDown(self):
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_process_workbook_raises_on_a_corrupt_file(self):
        # confirms the failure really is an exception (caught by main()'s
        # try/except), not a silent wrong/empty result that main() would
        # then mistake for "nothing to warn about."
        bank_list = []
        with self.assertRaises(Exception):
            process_workbook(os.path.join(self.banks_dir, "CORRUPT FINANCIALS.xlsx"), bank_list)

    def test_main_continues_past_the_corrupt_file_and_still_processes_the_good_one(self):
        script = os.path.join(os.path.dirname(__file__), "extract_metrics.py")
        result = subprocess.run(
            [sys.executable, script, "--banks-dir", self.banks_dir,
             "--db", self.db_path, "--out", self.out_path],
            capture_output=True, text=True,
        )
        # main() records the error and continues - it must NOT crash with
        # a nonzero exit or an unhandled traceback.
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("failed to process", result.stderr)
        self.assertIn("CORRUPT FINANCIALS.xlsx", result.stderr)
        self.assertIn("Workbooks that failed to process (1)", result.stdout)

        # and the good bank's data still made it through end to end
        conn = sqlite3.connect(self.db_path)
        banks = [row[0] for row in conn.execute("SELECT filename_bank_name FROM banks")]
        conn.close()
        self.assertEqual(banks, ["ABC INTERNATIONAL BANK"])


class PartialExtractionFailureDetection(unittest.TestCase):
    """Regression for a real bug: extract_metrics.py's main() used to call
    `_db.validate(conn, expected_banks=n_banks, ...)` - checking the count it
    JUST WROTE against itself, which always trivially passes even when a
    workbook silently contributed no row (e.g. two workbooks resolving to
    the same FRN, which write_banks_and_metrics() collapses to one `banks`
    row with no exception and no entry in `errors`). The fix passes a true
    independent expected count (`len(paths) - len(errors)`, the number of
    workbooks that did NOT throw) instead. This test exercises the
    write_banks_and_metrics()+validate() combination directly with two
    distinct-source rows that collapse to the same FRN - the exact
    "no exception raised, but fewer banks than workbooks" scenario the old
    code couldn't detect."""

    def _row(self, frn, bank, source_workbook, sheet="Cash Flow Statement",
              label="Net cash from operating activities", year="FY2025", value=100.0):
        return {
            "bank": bank, "canonical_bank": bank, "source_filename_bank": bank,
            "source_workbook": source_workbook, "frn": frn, "workbook_kind": "full",
            "sheet": sheet, "row_label": label, "year": year, "value_raw": str(value),
            "value_numeric": value, "is_numeric": "1", "basis_note": "",
            "unit": "", "reporting_basis": "", "restatement_note": "", "source_note": "",
        }

    def test_two_workbooks_colliding_on_one_frn_is_caught_by_the_independent_expected_count(self):
        import build_insights_db as _db
        # Two DIFFERENT source workbooks, same FRN - simulates a matching
        # collision write_banks_and_metrics() silently resolves to one row.
        rows = [
            self._row("111", "BANK ONE", "BANK ONE FINANCIALS.xlsx", year="FY2024"),
            self._row("111", "BANK TWO", "BANK TWO FINANCIALS.xlsx", year="FY2025"),
        ]
        with tempfile.TemporaryDirectory() as directory:
            db_path = os.path.join(directory, "test.db")
            conn = _db.connect(db_path)
            n_banks, n_metrics = _db.write_banks_and_metrics(conn, rows, metrics_source="test")
            self.assertEqual(n_banks, 1)  # collapsed - the silent-failure symptom

            # OLD (buggy) behaviour: checking the count against itself always
            # "passes", even though 2 source workbooks only produced 1 bank.
            _db.validate(conn, expected_banks=n_banks, expected_metric_rows=n_metrics)

            # NEW (fixed) behaviour: a true independent expectation (2 source
            # workbooks, 0 caught errors) correctly detects the collision.
            with self.assertRaises(AssertionError):
                _db.validate(conn, expected_banks=2, expected_metric_rows=n_metrics)
            conn.close()


if __name__ == "__main__":
    unittest.main(verbosity=2)
