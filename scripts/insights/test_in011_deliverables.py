import unittest

from in011_deliverables import render_html_analysis, render_pdf_analysis_lines


def payload():
    return {
        "in009": {
            "metadata": {"metrics": ["CET1 Ratio"]},
            "coverage": {
                "CET1 Ratio": {
                    "broad": {"banks": 10, "observations": 40, "years": [2023, 2024], "exclusions": {}},
                    "strict": {"banks": 6, "observations": 20, "years": [2023, 2024], "exclusions": {"unknown_basis": 20}},
                }
            },
            "outliers": {"broad": [{"metric": "CET1 Ratio", "frn": "1", "bank": "Alpha", "fiscal_year": 2024, "value": 55.0, "reasons": ["level above 95th percentile"], "comparability_status": "broad-only"}], "strict": []},
        },
        "in010": {
            "parent_groups": {"CET1 Ratio": {"strict": [{"group": "Group A", "member_count": 2, "latest_level": {"status": "comparable", "year": 2024, "range": 4.0, "n": 2}, "trends": [{"start_year": 2023, "end_year": 2024, "direction": "mixed", "agreement": 0.5, "n": 2}]}]}}
        },
    }


class DeliverableAdapterTests(unittest.TestCase):
    def test_html_contains_shared_coverage_outliers_and_group_sections(self):
        rendered = render_html_analysis(payload())
        self.assertIn("Strict versus broad coverage", rendered)
        self.assertIn("Outlier investigation", rendered)
        self.assertIn("Alpha", rendered)
        self.assertIn("Group A", rendered)
        self.assertIn("how many banks can be compared", rendered)
        self.assertIn("An outlier is a review prompt", rendered)
        self.assertIn("separately regulated entities", rendered)

    def test_analysis_sections_are_collapsed_by_default(self):
        rendered = render_html_analysis(payload())
        self.assertIn("<summary>Strict versus broad coverage</summary>", rendered)
        self.assertIn("<summary>Outlier investigation</summary>", rendered)
        self.assertNotIn("<details open", rendered)

    def test_pdf_lines_contain_same_evidence_in_concise_form(self):
        rendered = "\n".join(render_pdf_analysis_lines(payload()))
        self.assertIn("Core-ratio coverage", rendered)
        self.assertIn("Alpha", rendered)
        self.assertIn("Group A", rendered)
        self.assertIn("strict", rendered)

    def test_html_omits_parent_dispersion_when_every_group_is_insufficient(self):
        data = payload()
        data["in010"] = {"parent_groups": {"CET1 Ratio": {"strict": [
            {"group": "Group A", "latest_level": {"status": "insufficient"}, "trends": []}
        ]}}}
        rendered = render_html_analysis(data)
        self.assertNotIn("Parent-group dispersion and agreement", rendered)


if __name__ == "__main__":
    unittest.main()
