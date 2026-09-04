import unittest

from chart_contract import build_line_chart_spec, validate_chart_spec


class ChartContract(unittest.TestCase):
    def test_line_spec_preserves_missing_values_and_metadata(self):
        spec = build_line_chart_spec(
            "cet1", "CET1 ratio", "percentage points", [
                {"bank": "Zulu", "years": [{"year": 2022, "value": 12}, {"year": 2023, "value": None}]},
                {"bank": "Alpha", "years": [{"year": 2022, "value": 8}, {"year": 2023, "value": 9}]},
            ], [2023, 2022], "CET1 trajectories",
        )
        validate_chart_spec(spec)
        self.assertEqual(spec["dimensions"]["x"]["values"], [2022, 2023])
        self.assertEqual([item["id"] for item in spec["series"]], ["Alpha", "Zulu"])
        self.assertIsNone(spec["series"][1]["points"][1]["y"])
        self.assertEqual(spec["accessibility"]["table_columns"], ["Bank", "Fiscal year", "percentage points"])

    def test_invalid_series_shape_is_rejected(self):
        with self.assertRaises(ValueError):
            validate_chart_spec({"schema_version": 1, "id": "bad", "title": "Bad",
                                 "dimensions": {"x": {"values": [2022, 2021]}, "y": {"domain": [0, 1]}},
                                 "series": [], "accessibility": {}})


if __name__ == "__main__":
    unittest.main()
