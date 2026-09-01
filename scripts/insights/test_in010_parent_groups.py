import unittest

from in009_analysis import normalize_observation
from in010_parent_groups import analyze_parent_groups


def observation(frn, year, value, basis="entity"):
    return normalize_observation({
        "frn": str(frn),
        "bank": f"Bank {frn}",
        "sheet": "CET1 Ratio",
        "row_label": "CET1 ratio",
        "year": f"FY{year}",
        "value_raw": f"{value}%",
        "value_numeric": str(value),
        "is_numeric": "1",
        "basis_note": "",
        "reporting_basis": basis,
        "source_note": f"Source {year}",
    })


class ParentGroupAnalysisTests(unittest.TestCase):
    def test_latest_level_reports_dispersion_and_values(self):
        rows = [observation(1, 2023, 10), observation(1, 2024, 12), observation(2, 2024, 18)]
        groups = {"1": ("Bank 1", "Group A", "confirmed"), "2": ("Bank 2", "Group A", "confirmed")}
        result = analyze_parent_groups(rows, groups, metrics={"CET1 Ratio": "CET1 Ratio"})
        level = result["CET1 Ratio"]["strict"][0]["latest_level"]
        self.assertEqual(level["status"], "comparable")
        self.assertEqual(level["year"], 2024)
        self.assertEqual(level["values"], {"1": 12.0, "2": 18.0})
        self.assertEqual(level["range"], 6.0)

    def test_trend_agreement_reports_direction_and_share(self):
        rows = [observation(1, 2023, 10), observation(1, 2024, 12), observation(2, 2023, 10), observation(2, 2024, 9)]
        groups = {"1": ("Bank 1", "Group A", "confirmed"), "2": ("Bank 2", "Group A", "confirmed")}
        result = analyze_parent_groups(rows, groups, metrics={"CET1 Ratio": "CET1 Ratio"})
        trend = result["CET1 Ratio"]["strict"][0]["trends"][0]
        self.assertEqual(trend["n"], 2)
        self.assertEqual(trend["direction"], "mixed")
        self.assertEqual(trend["agreement"], 0.5)

    def test_basis_mismatch_is_not_called_comparable(self):
        rows = [observation(1, 2024, 12, "entity"), observation(2, 2024, 18, "consolidated_group")]
        groups = {"1": ("Bank 1", "Group A", "confirmed"), "2": ("Bank 2", "Group A", "confirmed")}
        result = analyze_parent_groups(rows, groups, metrics={"CET1 Ratio": "CET1 Ratio"})
        self.assertEqual(result["CET1 Ratio"]["strict"][0]["latest_level"]["status"], "insufficient")

    def test_single_member_group_is_retained_as_insufficient(self):
        rows = [observation(1, 2024, 12)]
        groups = {"1": ("Bank 1", "Solo Group", "confirmed")}
        result = analyze_parent_groups(rows, groups, metrics={"CET1 Ratio": "CET1 Ratio"})
        group = result["CET1 Ratio"]["strict"][0]
        self.assertEqual(group["member_count"], 1)
        self.assertEqual(group["latest_level"]["status"], "insufficient")


if __name__ == "__main__":
    unittest.main()
