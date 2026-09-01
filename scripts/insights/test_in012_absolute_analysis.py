import unittest

from in012_absolute_analysis import (
    classify_amount_unit,
    normalize_amount_observation,
    scale_adjusted_ratio,
    assign_size_bands,
    analyze_absolute_metrics,
)


def row(**overrides):
    value = {
        "frn": "1",
        "bank": "Bank 1",
        "sheet": "Total RWAs",
        "row_label": "Total risk-weighted assets",
        "year": "FY2024",
        "value_raw": "1,000",
        "value_numeric": "1000",
        "is_numeric": "1",
        "unit": "",
        "basis_note": "Entity basis, £'000.",
        "reporting_basis": "entity",
        "source_note": "Annual report",
    }
    value.update(overrides)
    return value


class AbsoluteAnalysisTests(unittest.TestCase):
    def test_units_are_classified_from_explicit_text(self):
        self.assertEqual(classify_amount_unit("Entity basis, £'000."), "GBP_thousand")
        self.assertEqual(classify_amount_unit("Consolidated basis, £m."), "GBP_million")
        self.assertEqual(classify_amount_unit("Source note only."), None)

    def test_observation_keeps_unknown_unit_unknown(self):
        normalized = normalize_amount_observation(row(basis_note="Source note only."))
        self.assertIsNone(normalized["amount_unit"])
        self.assertEqual(normalized["value_status"], "numeric")

    def test_scale_adjusted_ratio_requires_same_unit_and_basis(self):
        capital = normalize_amount_observation(row(sheet="CET1 Capital", value_numeric="200"))
        rwa = normalize_amount_observation(row(value_numeric="1000"))
        self.assertEqual(scale_adjusted_ratio(capital, rwa), 20.0)
        self.assertIsNone(scale_adjusted_ratio(capital, dict(rwa, amount_unit="GBP_million")))

    def test_size_bands_are_deterministic_and_rank_based(self):
        bands = assign_size_bands({"1": 100.0, "2": 200.0, "3": 300.0})
        self.assertEqual(bands, {"1": "small", "2": "medium", "3": "large"})

    def test_analysis_keeps_latest_metadata_and_cohort_boundaries(self):
        observations = [
            normalize_amount_observation(row(frn="1", sheet="CET1 Capital", year="FY2023", value_numeric="100")),
            normalize_amount_observation(row(frn="1", sheet="CET1 Capital", year="FY2024", value_numeric="120")),
            normalize_amount_observation(row(frn="2", sheet="CET1 Capital", year="FY2024", value_numeric="900", basis_note="Consolidated basis, £m.")),
        ]
        result = analyze_absolute_metrics(observations, {"CET1 Capital": "CET1 Capital"})["CET1 Capital"]
        self.assertEqual(result["latest"]["values"], {"1": 120.0, "2": 900.0})
        self.assertEqual(result["latest"]["years"]["1"], 2024)
        self.assertEqual(result["latest"]["metadata"]["2"]["amount_unit"], "GBP_million")
        self.assertEqual(len(result["size_cohorts"]), 2)

    def test_scale_adjusted_output_reports_coverage(self):
        observations = [
            normalize_amount_observation(row(frn="1", sheet="CET1 Capital", year="FY2024", value_numeric="200")),
            normalize_amount_observation(row(frn="1", sheet="Total RWAs", year="FY2024", value_numeric="1000")),
        ]
        result = analyze_absolute_metrics(observations, {"CET1 Capital": "CET1 Capital", "Total RWAs": "Total RWAs"})
        self.assertEqual(result["CET1 Capital"]["scale_adjusted"], {"1": {2024: 20.0}})
        self.assertEqual(result["CET1 Capital"]["scale_adjusted_coverage"]["observations"], 1)

    def test_trends_exclude_a_bank_when_unit_or_basis_changes(self):
        observations = [
            normalize_amount_observation(row(frn="1", sheet="CET1 Capital", year="FY2023", value_numeric="100")),
            normalize_amount_observation(row(frn="1", sheet="CET1 Capital", year="FY2024", value_numeric="100", basis_note="Consolidated basis, £m.")),
        ]
        result = analyze_absolute_metrics(observations, {"CET1 Capital": "CET1 Capital"})["CET1 Capital"]
        self.assertEqual(result["coverage"]["banks"], 0)
        self.assertEqual(result["coverage"]["unstable_unit_or_basis_banks"], 1)

    def test_small_cohorts_are_explicitly_not_size_banded(self):
        observations = [
            normalize_amount_observation(row(frn="1", sheet="CET1 Capital", value_numeric="100")),
            normalize_amount_observation(row(frn="2", sheet="CET1 Capital", value_numeric="200")),
        ]
        result = analyze_absolute_metrics(observations, {"CET1 Capital": "CET1 Capital"})["CET1 Capital"]
        self.assertEqual(result["size_bands"], {})
        self.assertEqual(result["size_cohorts"][0]["status"], "insufficient_cohort")


if __name__ == "__main__":
    unittest.main()
