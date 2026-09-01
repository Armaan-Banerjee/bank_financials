"""
Tests for scripts/export_parent_group_tables.py's markdown table-splicing
logic - previously only exercised against the real, well-formed
bank_parent_groups.md (via manual verification and test_pipeline.py's
idempotence/prose-preservation check). These specifically target malformed
input: a missing section header, a missing table header, and confirm the
splice fails loudly rather than silently corrupting the file.
"""

import os
import shutil
import sqlite3
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(__file__))

import build_insights_db as db
from export_parent_group_tables import (
    EDGES_SECTION_HEADER,
    EDGES_TABLE_HEADER,
    LOOKUP_SECTION_HEADER,
    LOOKUP_TABLE_HEADER,
    _find_table_block,
    splice,
)

WELL_FORMED_MARKDOWN = f"""# Test doc

## Conventions

Hand-authored prose that must never be touched.

{LOOKUP_SECTION_HEADER}

{LOOKUP_TABLE_HEADER}
|---|---:|---|---|---|---|
| Old Bank | 999 | Old Parent | Old Group | old | old |

{EDGES_SECTION_HEADER}

More hand-authored prose here too.

{EDGES_TABLE_HEADER}
|---|---|---|---|---|
| Old Bank | owned_by | Old Parent | old note | old source |

## Quality and follow-up

Final hand-authored section, also untouched.
"""


class FindTableBlock(unittest.TestCase):
    def test_missing_section_header_raises_value_error(self):
        lines = ["# doc", "no matching section here"]
        with self.assertRaises(ValueError) as ctx:
            _find_table_block(lines, LOOKUP_SECTION_HEADER, LOOKUP_TABLE_HEADER)
        self.assertIn(LOOKUP_SECTION_HEADER, str(ctx.exception))

    def test_missing_table_header_after_correct_section_raises_value_error(self):
        lines = [LOOKUP_SECTION_HEADER, "", "some prose but no table header follows"]
        with self.assertRaises(ValueError) as ctx:
            _find_table_block(lines, LOOKUP_SECTION_HEADER, LOOKUP_TABLE_HEADER)
        self.assertIn(LOOKUP_TABLE_HEADER, str(ctx.exception))

    def test_finds_correct_block_boundaries_in_well_formed_input(self):
        lines = WELL_FORMED_MARKDOWN.split("\n")
        start, end = _find_table_block(lines, LOOKUP_SECTION_HEADER, LOOKUP_TABLE_HEADER)
        self.assertEqual(lines[start], LOOKUP_TABLE_HEADER)
        # end_idx is exclusive and lands on the first blank line after the data rows
        self.assertEqual(lines[end].strip(), "")

    def test_table_header_belonging_to_a_different_section_is_not_matched(self):
        # a table header text that happens to appear BEFORE the requested
        # section must not be picked up - _find_table_block only searches
        # from section_idx onward.
        lines = [EDGES_TABLE_HEADER, "", LOOKUP_SECTION_HEADER, "", "no lookup table header here"]
        with self.assertRaises(ValueError):
            _find_table_block(lines, LOOKUP_SECTION_HEADER, LOOKUP_TABLE_HEADER)


class SpliceEndToEnd(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp(prefix="splice_test_")
        self.md_path = os.path.join(self.tmpdir, "test.md")
        self.db_path = os.path.join(self.tmpdir, "test.db")
        with open(self.md_path, "w", encoding="utf-8") as f:
            f.write(WELL_FORMED_MARKDOWN)

        conn = db.connect(self.db_path)
        db.write_banks_and_metrics(
            conn,
            [{"bank": "NEWBANK", "canonical_bank": "New Bank Ltd", "source_filename_bank": "NEWBANK",
              "source_workbook": "NEWBANK FINANCIALS.xlsx", "frn": 111, "workbook_kind": "full",
              "sheet": "CET1 Ratio", "row_label": "CET1 ratio", "year": "FY2025",
              "value_raw": "14.5%", "value_numeric": 14.5, "is_numeric": "1", "basis_note": ""}],
            metrics_source="test",
        )
        db.write_parent_group(
            conn,
            lookup_rows=[{"frn": 111, "bank_name": "New Bank", "immediate_parent": "New Parent",
                          "ultimate_group": "New Group", "status_caveat": "confirmed", "evidence": "test"}],
            edge_rows=[{"from_node": "New Bank", "edge_type": "owned_by", "to_node": "New Parent",
                        "effective_note": "from 2025-01-01", "source": "CH"}],
        )
        self.conn = conn

    def tearDown(self):
        self.conn.close()
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_tables_are_replaced_and_prose_is_preserved_exactly(self):
        new_content, n_lookup, n_edges = splice(self.md_path, self.conn)
        self.assertEqual(n_lookup, 1)
        self.assertEqual(n_edges, 1)

        # new data replaces old
        self.assertIn("New Bank", new_content)
        self.assertNotIn("Old Bank", new_content)
        self.assertNotIn("999", new_content)  # old FRN gone

        # hand-authored prose survives byte-for-byte
        self.assertIn("Hand-authored prose that must never be touched.", new_content)
        self.assertIn("More hand-authored prose here too.", new_content)
        self.assertIn("Final hand-authored section, also untouched.", new_content)
        self.assertIn("## Conventions", new_content)
        self.assertIn("## Quality and follow-up", new_content)

    def test_splice_raises_cleanly_on_a_markdown_missing_a_required_section(self):
        broken_path = os.path.join(self.tmpdir, "broken.md")
        with open(broken_path, "w", encoding="utf-8") as f:
            f.write("# Just a title, no sections at all\n")
        with self.assertRaises(ValueError):
            splice(broken_path, self.conn)


if __name__ == "__main__":
    unittest.main(verbosity=2)
