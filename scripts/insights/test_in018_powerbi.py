import os
import tempfile
import unittest

import build_insights_db
from in018_powerbi import _period_id, build_powerbi_model, semantic_contract


class In018PowerBiTests(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.db = os.path.join(self.tmpdir.name, "model.db")
        conn = build_insights_db.connect(self.db)
        rows = []
        for frn in (1, 2):
            rows.append({"bank": f"BANK{frn}", "canonical_bank": f"Bank {frn}", "source_filename_bank": f"BANK{frn}",
                         "source_workbook": f"BANK{frn}.xlsx", "frn": str(frn), "workbook_kind": "full",
                         "sheet": "CET1 Ratio", "row_label": "CET1 ratio", "year": "FY2025",
                         "value_raw": str(frn * 10), "value_numeric": str(frn * 10), "is_numeric": "1",
                         "basis_note": "entity", "unit": "%", "reporting_basis": "entity",
                         "restatement_note": "", "source_note": "Annual report"})
        build_insights_db.write_banks_and_metrics(conn, rows, metrics_source="test")
        conn.close()

    def tearDown(self):
        self.tmpdir.cleanup()

    def test_fact_has_one_row_per_source_observation_and_dimensions_are_unique(self):
        model = build_powerbi_model(self.db)
        self.assertEqual(len(model["tables"]["fact_observation"]), 2)
        self.assertEqual(len(model["tables"]["dim_bank"]), 2)
        self.assertEqual(len(model["tables"]["dim_metric"]), 1)
        fact = model["tables"]["fact_observation"][0]
        self.assertEqual(fact["quality_id"], "numeric")
        self.assertEqual(fact["period_id"], "FY2025")
        self.assertEqual(fact["source_id"], "bank1_xlsx")

    def test_contract_exposes_relationships_measures_and_rules(self):
        contract = semantic_contract()
        self.assertIn("Comparable N", contract["measures"])
        self.assertGreaterEqual(len(contract["relationships"]), 7)
        self.assertTrue(any("unit_id" in rule for rule in contract["authoring_rules"]))

    def test_period_id_preserves_qualified_reporting_periods(self):
        ordinary = {"fiscal_year": 2023, "year": "FY2023"}
        fifteen_month = {"fiscal_year": 2023, "year": "FY2023 (15m)"}
        fifteen_month_spelled = {"fiscal_year": 2023, "year": "FY2023 (15mo)"}
        self.assertEqual(_period_id(ordinary), "FY2023")
        self.assertNotEqual(_period_id(fifteen_month), _period_id(fifteen_month_spelled))
        self.assertNotEqual(_period_id(ordinary), _period_id(fifteen_month))


if __name__ == "__main__":
    unittest.main()
