import sqlite3
import tempfile
import unittest
from pathlib import Path

from inspect_db_polars import _identifier, _query, _schema, _tables


class InspectDbHelpers(unittest.TestCase):
    def test_table_discovery_and_schema_are_deterministic(self):
        with tempfile.TemporaryDirectory() as directory:
            connection = sqlite3.connect(Path(directory) / "test.db")
            connection.execute("CREATE TABLE zeta (id INTEGER PRIMARY KEY, label TEXT)")
            connection.execute("CREATE TABLE alpha (value REAL)")
            self.assertEqual(_tables(connection), ["alpha", "zeta"])
            self.assertEqual(_schema(connection, "zeta")[0][1:3], ("id", "INTEGER"))
            connection.close()

    def test_identifier_and_preview_query_are_safe_and_explicit(self):
        self.assertEqual(_identifier("annual_metrics"), '"annual_metrics"')
        with self.assertRaises(ValueError):
            _identifier("annual_metrics; DROP TABLE banks")
        with self.assertRaises(ValueError):
            _identifier("")
        query, parameters = _query("banks", "frn = 123", 10)
        self.assertIn('SELECT * FROM "banks" WHERE frn = 123 LIMIT ?', query)
        self.assertEqual(parameters, (10,))


if __name__ == "__main__":
    unittest.main()
