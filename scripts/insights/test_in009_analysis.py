import unittest

from in009_analysis import (
    classify_reporting_basis,
    normalize_observation,
    comparable_observations,
    build_metric_series,
    pairwise_trend,
    detect_outliers,
    render_quality_report,
)


def row(**overrides):
    value = {
        "frn": "123",
        "bank": "Example Bank",
        "sheet": "CET1 Ratio",
        "row_label": "CET1 ratio",
        "year": "FY2024*",
        "value_raw": "15.2%",
        "value_numeric": "15.2",
        "is_numeric": "1",
        "basis_note": "Entity-level basis, £'000. See source note.",
        "reporting_basis": "",
        "restatement_note": "",
        "source_note": "Annual report, p. 10",
    }
    value.update(overrides)
    return value


class NormalizationTests(unittest.TestCase):
    def test_period_keeps_year_and_marks_footnote_variant(self):
        normalized = normalize_observation(row())
        self.assertEqual(normalized["fiscal_year"], 2024)
        self.assertEqual(normalized["period_key"], "FY2024*")
        self.assertTrue(normalized["period_qualified"])

    def test_short_period_is_not_annual_eligible(self):
        normalized = normalize_observation(row(year="FY2023 (15m)"))
        self.assertEqual(normalized["period_length_months"], 15)
        self.assertFalse(normalized["annual_eligible"])

    def test_explicit_basis_note_is_classified(self):
        self.assertEqual(
            classify_reporting_basis("Consolidated Group basis, £m."),
            "consolidated_group",
        )
        self.assertEqual(
            classify_reporting_basis("Bank Company-only basis, £m."),
            "entity",
        )

    def test_unknown_basis_is_not_guessed(self):
        self.assertIsNone(classify_reporting_basis("£m. See source note."))
        normalized = normalize_observation(row(basis_note="£m. See source note."))
        self.assertIsNone(normalized["reporting_basis"])

    def test_sentinel_percentage_is_classified_without_becoming_missing(self):
        normalized = normalize_observation(row(value_raw="999999%", value_numeric="999999"))
        self.assertEqual(normalized["value_status"], "special_numeric")
        self.assertEqual(normalized["value_numeric"], "999999")

    def test_strict_comparability_excludes_unknown_basis(self):
        observations = [
            normalize_observation(row(frn="1", reporting_basis="entity", year="FY2024")),
            normalize_observation(row(frn="2", reporting_basis="", basis_note="", year="FY2024")),
            normalize_observation(row(frn="3", reporting_basis="entity", year="FY2023")),
        ]
        selected = comparable_observations(observations, mode="strict", fiscal_year=2024)
        self.assertEqual([item["frn"] for item in selected], ["1"])

    def test_strict_comparability_uses_one_common_basis(self):
        observations = [
            normalize_observation(row(frn="1", reporting_basis="entity", basis_note="", year="FY2024")),
            normalize_observation(row(frn="2", reporting_basis="consolidated_group", basis_note="", year="FY2024")),
            normalize_observation(row(frn="3", reporting_basis="entity", basis_note="", year="FY2024")),
        ]
        selected = comparable_observations(observations, mode="strict", fiscal_year=2024)
        self.assertEqual([item["frn"] for item in selected], ["1", "3"])

    def test_metric_series_selects_one_numeric_observation_per_entity_year(self):
        observations = [
            normalize_observation(row(frn="1", row_label="CET1 ratio", year="FY2024", value_numeric="15")),
            normalize_observation(row(frn="1", row_label="Common Equity Tier 1 (CET1) ratio", year="FY2024", value_numeric="15.1")),
            normalize_observation(row(frn="1", row_label="CET1 ratio", year="FY2023", value_numeric="14")),
        ]
        series = build_metric_series(observations, "CET1 Ratio")
        self.assertEqual(series, {"1": {2023: 14.0, 2024: 15.0}})

    def test_metric_series_fills_years_when_source_label_changes(self):
        observations = [
            normalize_observation(row(frn="1", row_label="CET1 ratio", year="FY2023", value_numeric="14")),
            normalize_observation(row(frn="1", row_label="Common Equity Tier 1 ratio", year="FY2024", value_numeric="15")),
        ]
        self.assertEqual(build_metric_series(observations, "CET1 Ratio"), {"1": {2023: 14.0, 2024: 15.0}})

    def test_metric_series_prefers_percentage_row_over_absolute_amount_row(self):
        # Regression for a real bug: Barclays Bank PLC's "Leverage Ratio" sheet
        # carries both the true ratio ("UK leverage ratio (%)" = 5.8%) and a
        # supporting absolute amount ("Tier 1 (T1) capital used in leverage
        # calculation (£m)" = 56465). Neither label is in `_label_rank`'s
        # curated dict, and "Tier 1..." sorts alphabetically before "UK
        # leverage ratio (%)", so the old selection logic picked the £m
        # figure and the deliverable reported it as "56465%".
        observations = [
            normalize_observation(row(
                frn="1", sheet="Leverage Ratio",
                row_label="Tier 1 (T1) capital used in leverage calculation (£m)",
                year="FY2024", value_raw="56465", value_numeric="56465",
            )),
            normalize_observation(row(
                frn="1", sheet="Leverage Ratio",
                row_label="UK leverage ratio (%)",
                year="FY2024", value_raw="5.8%", value_numeric="5.8",
            )),
        ]
        series = build_metric_series(observations, "Leverage Ratio")
        self.assertEqual(series, {"1": {2024: 5.8}})

    def test_metric_series_prefers_documented_excluding_variant_over_including_variant(self):
        observations = [
            normalize_observation(row(
                frn="1", sheet="Leverage Ratio",
                row_label="Leverage ratio including claims on central banks (%)",
                year="FY2021", value_raw="4.1%", value_numeric="4.1",
            )),
            normalize_observation(row(
                frn="1", sheet="Leverage Ratio",
                row_label="Leverage ratio excluding claims on central banks (%)",
                year="FY2021", value_raw="5.6%", value_numeric="5.6",
            )),
        ]
        self.assertEqual(build_metric_series(observations, "Leverage Ratio"), {"1": {2021: 5.6}})

    def test_metric_series_excludes_year_with_no_disclosed_percentage_on_ratio_sheet(self):
        # Regression: when a percentage-only sheet (Leverage Ratio, LCR, NSFR,
        # MREL Ratio, CET1/Tier 1/Total Capital Ratio) has no percentage row
        # disclosed for a given bank/year - only a supporting absolute-amount
        # row - that year must be treated as missing, not filled in with the
        # absolute figure as if it were the ratio.
        observations = [
            normalize_observation(row(
                frn="1", sheet="MREL Ratio",
                row_label="MREL-eligible senior non-preferred debt issued (£m)",
                year="FY2023", value_raw="200", value_numeric="200",
            )),
            normalize_observation(row(
                frn="1", sheet="MREL Ratio",
                row_label="Total MREL ratio (% of RWA)",
                year="FY2024", value_raw="23.6%", value_numeric="23.6",
            )),
        ]
        series = build_metric_series(observations, "MREL Ratio")
        self.assertEqual(series, {"1": {2024: 23.6}})

    def test_metric_series_on_absolute_only_sheet_is_unaffected(self):
        # CET1 Capital and similar absolute sheets never carry a "%" row -
        # the percentage-preference guard must not exclude their genuine
        # £m/£'000 observations.
        observations = [
            normalize_observation(row(
                frn="1", sheet="CET1 Capital", row_label="Common Equity Tier 1 (CET1) capital",
                year="FY2024", value_raw="564.579", value_numeric="564.579",
            )),
        ]
        series = build_metric_series(observations, "CET1 Capital")
        self.assertEqual(series, {"1": {2024: 564.579}})

    def test_pairwise_trend_reports_down_up_same_and_long_run(self):
        series = {"1": {2021: 10, 2022: 9, 2025: 12}, "2": {2021: 10, 2022: 11, 2025: 10}}
        self.assertEqual(pairwise_trend(series, 2021, 2022), {"down": 1, "up": 1, "same": 0, "n": 2})
        self.assertEqual(pairwise_trend(series, 2021, 2025)["n"], 2)

    def test_pairwise_trend_works_for_available_years_without_hardcoded_window(self):
        self.assertEqual(pairwise_trend({"1": {2020: 1, 2021: 2}}, 2020, 2021)["up"], 1)

    def test_metric_series_and_pairwise_trend_handle_two_banks_of_different_window_lengths(self):
        """The historical-depth (HD-series) extension effort gave some real
        banks a 10-year window (FY2016-FY2025) against most banks' standard 5
        (FY2021-FY2025). Existing tests here only ever use one FRN, or two
        FRNs sharing identical years - neither exercises build_metric_series
        grouping two genuinely different-length windows into independent
        per-FRN series, nor pairwise_trend being asked about an older year
        pair that only the long-window bank has on file."""
        observations = [
            normalize_observation(row(frn="1", row_label="CET1 ratio", year=f"FY{year}", value_numeric=str(10 + i)))
            for i, year in enumerate(range(2016, 2026))  # long-window bank: 10 years, values 10..19
        ] + [
            normalize_observation(row(frn="2", row_label="CET1 ratio", year=f"FY{year}", value_numeric=str(20 + i)))
            for i, year in enumerate(range(2021, 2026))  # short-window bank: 5 years, values 20..24
        ]
        series = build_metric_series(observations, "CET1 Ratio")
        self.assertEqual(series["1"], {2016 + i: 10.0 + i for i in range(10)})
        self.assertEqual(series["2"], {2021 + i: 20.0 + i for i in range(5)})

        # FY2016->FY2017 pair: only the long-window bank has both years.
        old_pair = pairwise_trend(series, 2016, 2017)
        self.assertEqual(old_pair["n"], 1)
        self.assertEqual(old_pair["up"], 1)

        # FY2021->FY2022 pair: both banks have both years.
        shared_pair = pairwise_trend(series, 2021, 2022)
        self.assertEqual(shared_pair["n"], 2)
        self.assertEqual(shared_pair["up"], 2)

    def test_outlier_has_explainable_level_and_movement_reasons(self):
        observations = []
        for frn, value in (("1", 10), ("2", 11), ("3", 12), ("4", 100)):
            observations.append(normalize_observation(row(frn=frn, year="FY2024", value_numeric=str(value))))
        observations += [
            normalize_observation(row(frn="4", year="FY2023", value_numeric="10")),
        ]
        outliers = detect_outliers(observations, metric="CET1 Ratio")
        flagged = next(item for item in outliers if item["frn"] == "4")
        self.assertTrue(flagged["reasons"])
        self.assertTrue(any("level" in reason or "movement" in reason for reason in flagged["reasons"]))
        self.assertIn("comparability_status", flagged)

    def test_quality_report_is_deterministic_and_includes_coverage(self):
        payload = {
            "metadata": {"source": "test.db", "metrics": ["CET1 Ratio"]},
            "coverage": {"CET1 Ratio": {
                "broad": {"observations": 2, "banks": 1, "years": [2024]},
                "strict": {"observations": 1, "banks": 1, "years": [2024]},
            }},
            "outliers": {"broad": [], "strict": []},
        }
        report = render_quality_report(payload)
        self.assertIn("| CET1 Ratio | strict | 1 | 1 | 2024 |", report)
        self.assertEqual(report, render_quality_report(payload))


if __name__ == "__main__":
    unittest.main()
