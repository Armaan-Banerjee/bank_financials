import unittest

from in016_distribution import _exact_cohort, distribution_for_metric, percentile_rank, summarize


def observation(frn, value, basis="entity"):
    return {"frn": str(frn), "sheet": "CET1 Ratio", "row_label": "CET1 ratio",
            "year": "FY2025", "value_raw": f"{value}%", "value_numeric": str(value),
            "is_numeric": "1", "basis_note": basis, "reporting_basis": basis,
            "annual_eligible": True, "fiscal_year": 2025, "period_key": "FY2025",
            "value_status": "numeric"}


class In016DistributionTests(unittest.TestCase):
    def test_percentile_rank_uses_midrank_for_ties(self):
        self.assertEqual(percentile_rank(20, [10, 20, 20, 30]), 50.0)

    def test_summary_contains_robust_spread_and_small_sample_status(self):
        result = summarize([10, 20, 30, 40, 50, 60, 70, 80])
        self.assertEqual(result["n"], 8)
        self.assertEqual(result["median"], 45)
        self.assertEqual(result["q1"], 27.5)
        self.assertEqual(result["q3"], 62.5)
        self.assertEqual(result["iqr"], 35)
        self.assertEqual(result["status"], "small_n")

    def test_distribution_requires_common_basis_in_strict_mode(self):
        rows = [observation(index, index * 10, "entity" if index < 5 else "consolidated_group") for index in range(1, 9)]
        result = distribution_for_metric(rows, "CET1 Ratio", "CET1 Ratio", mode="strict", fiscal_year=2025)
        self.assertEqual(result["summary"]["status"], "ambiguous_basis")

    def test_distribution_retains_bank_level_rank_and_robust_score(self):
        rows = [observation(index, value) for index, value in enumerate((10, 20, 30, 40, 50, 60, 70, 80), start=1)]
        result = distribution_for_metric(rows, "CET1 Ratio", "CET1 Ratio", mode="strict", fiscal_year=2025)
        self.assertEqual(result["summary"]["status"], "small_n")
        self.assertEqual(result["observations"][0]["percentile_rank"], 6.25)
        self.assertIsNone(result["observations"][0]["robust_z"])

    def test_explicit_basis_does_not_get_replaced_by_modal_basis(self):
        rows = [observation(index, index * 10, "entity") for index in range(1, 9)]
        rows.append(observation(99, 99, "consolidated_group"))
        result = distribution_for_metric(rows, "CET1 Ratio", "CET1 Ratio", mode="strict", fiscal_year=2025, reporting_basis="consolidated_group")
        self.assertEqual(result["summary"]["n"], 1)
        self.assertEqual(result["summary"]["status"], "insufficient_cohort")

    def test_distribution_uses_canonical_choice_between_valid_percentage_variants(self):
        rows = [
            observation(1, 4.1),
            {**observation(1, 5.6),
             "row_label": "Leverage ratio excluding claims on central banks (%)"},
        ]
        rows[0]["sheet"] = "Leverage Ratio"
        rows[1]["sheet"] = "Leverage Ratio"
        rows[0]["row_label"] = "Leverage ratio including claims on central banks (%)"
        result = distribution_for_metric(rows, "Leverage Ratio", "Leverage Ratio", mode="broad", fiscal_year=2025)
        self.assertEqual([row["value_numeric"] for row in result["observations"]], ["5.6"])

    def test_absolute_cohort_uses_one_row_definition_across_years(self):
        rows = []
        for year, cet1, tier2, total in ((2021, 7451, 761, 8212), (2022, 9353, 700, 10053), (2023, 9876, 700, 10576)):
            for label, value in (
                ("Shareholders' funds (Core Equity Tier 1)", cet1),
                ("Subordinated liabilities (Tier 2)", tier2),
                ("Total regulatory capital (CET1 + Tier 2)", total),
            ):
                rows.append({"frn": "kingdom", "sheet": "Total Capital", "fiscal_year": year,
                             "annual_eligible": True, "value_status": "numeric", "value_numeric": value,
                             "value_raw": str(value), "row_label": label, "reporting_basis": "entity",
                             "amount_unit": "GBP_thousands", "period_key": f"FY{year}"})
        selected = [
            _exact_cohort(rows, "Total Capital", year, "entity", amount=True, unit="GBP_thousands")[0]
            for year in (2021, 2022, 2023)
        ]
        self.assertEqual(
            [row["row_label"] for row in selected],
            ["Shareholders' funds (Core Equity Tier 1)"] * 3,
        )


if __name__ == "__main__":
    unittest.main()
