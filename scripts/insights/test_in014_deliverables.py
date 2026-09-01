import unittest

from in011_deliverables import render_html_analysis, render_pdf_analysis_lines


def payload():
    return {
        "in009": {"metadata": {"metrics": []}, "coverage": {}, "outliers": {"broad": [], "strict": []}},
        "in010": {"parent_groups": {}},
        "in012": {"absolute_metrics": {
            "CET1 Capital": {
                "coverage": {"observations": 10, "known_unit_banks": 4, "unknown_unit_observations": 2, "banks": 4},
                "trends": [{"start_year": 2023, "end_year": 2024, "up": 3, "down": 1, "n": 4}],
                "size_cohorts": [{"amount_unit": "GBP_million", "reporting_basis": "entity", "count": 4, "status": "comparable"}],
                "scale_adjusted_coverage": {"banks": 3, "exclusions": {"unknown_unit": 2}},
            },
        }},
    }


class AbsoluteDeliverableTests(unittest.TestCase):
    def test_html_has_visual_and_accessible_table(self):
        rendered = render_html_analysis(payload())
        self.assertIn("Absolute capital and RWA analysis", rendered)
        self.assertIn('role="img"', rendered)
        self.assertIn("Known-unit banks", rendered)
        self.assertIn("GBP_million", rendered)
        self.assertIn("Scale exclusions", rendered)
        self.assertEqual(rendered.count('class="card wide analysis-collapsible"'), 3)
        self.assertNotIn('class="analysis-collapsible" open', rendered)
        self.assertIn("What this shows:", rendered)
        self.assertIn("A larger amount does not by itself mean a stronger capital position", rendered)

    def test_pdf_has_executive_absolute_summary(self):
        rendered = "\n".join(render_pdf_analysis_lines(payload()))
        self.assertIn("Absolute capital/RWA analysis", rendered)
        self.assertIn("CET1 Capital", rendered)
        self.assertIn("scale-adjusted banks", rendered)
        self.assertIn("unknown_unit: 2", rendered)


if __name__ == "__main__":
    unittest.main()
