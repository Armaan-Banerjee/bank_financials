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

    def test_html_renders_risk_composition_section(self):
        data = payload()
        data["in040"] = {
            "metadata": {"banks": {"1": "Alpha", "2": "Beta"}},
            "loan_concentration_quality": {
                "stage_balances": {
                    "1": {2024: {"Loans and advances to customers": {"stage_1": 700, "stage_2": 200, "stage_3": 100}}},
                    "2": {2024: {"Placements with banks": {"stage_1": 500, "stage_2": 0, "stage_3": 0}}},
                },
                "coverage_and_npl_ratios": {"1": [{"year": 2024, "label": "NPL ratio", "value": 10.0, "value_raw": "10.0%"}]},
                "coverage": {"banks_with_stage_data": 2, "banks_with_coverage_or_npl_disclosure": 1},
            },
            "rwa_density": {
                "rwa_to_assets_pct": {"1": {2024: 45.0}, "2": {2024: 10.0}},
                "rwa_category_composition": {
                    "1:2024": [{"label": "Credit risk", "value": 90, "pct_of_total_rwa": 90.0}],
                },
                "coverage": {"bank_years_with_rwa_to_assets": 2, "bank_years_with_category_breakdown": 1},
            },
        }
        rendered = render_html_analysis(data)
        self.assertIn("Loan concentration, asset quality, and RWA density", rendered)
        self.assertIn("Alpha", rendered)
        self.assertIn("Beta", rendered)
        self.assertIn("Placements with banks", rendered)
        self.assertIn("Credit risk (90.0%)", rendered)
        self.assertIn("10.0%", rendered)

    def test_pdf_lines_include_risk_composition_summary(self):
        data = payload()
        data["in040"] = {
            "metadata": {"banks": {"1": "Alpha"}},
            "loan_concentration_quality": {
                "stage_balances": {"1": {2024: {"Loans": {"stage_1": 90, "stage_2": 10, "stage_3": 0}}}},
                "coverage_and_npl_ratios": {},
                "coverage": {"banks_with_stage_data": 1, "banks_with_coverage_or_npl_disclosure": 0},
            },
            "rwa_density": {
                "rwa_to_assets_pct": {"1": {2024: 35.5}},
                "rwa_category_composition": {},
                "coverage": {"bank_years_with_rwa_to_assets": 1, "bank_years_with_category_breakdown": 0},
            },
        }
        rendered = "\n".join(render_pdf_analysis_lines(data))
        self.assertIn("Loan concentration, asset quality, and RWA density", rendered)
        self.assertIn("Alpha | FY2024 | RWA/assets=35.5%", rendered)


if __name__ == "__main__":
    unittest.main()
