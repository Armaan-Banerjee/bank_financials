import unittest

from in040_risk_metrics import (
    _bare_label,
    _select_labeled_rows,
    loan_concentration_quality,
    rwa_density,
    leverage,
    income_volatility,
)


def obs(frn, sheet, row_label, year, value, bank="Bank"):
    return {
        "frn": frn,
        "bank": bank,
        "sheet": sheet,
        "row_label": row_label,
        "fiscal_year": year,
        "annual_eligible": True,
        "value_status": "numeric",
        "value_numeric": value,
        "value_raw": str(value),
    }


class BareLabelTests(unittest.TestCase):
    def test_strips_section_prefix(self):
        self.assertEqual(_bare_label("Assets - Derivative financial instruments"), "Derivative financial instruments")

    def test_no_prefix_is_unchanged(self):
        self.assertEqual(_bare_label("Total assets"), "Total assets")


class SelectLabeledRowsTests(unittest.TestCase):
    def test_picks_shortest_bare_label_on_tie(self):
        import re
        rows = [
            obs(1, "Balance Sheet", "Equity - Total equity", 2024, 100),
            obs(1, "Balance Sheet", "Capital and reserves - Total equity attributable to owners", 2024, 90),
        ]
        selected, ambiguous = _select_labeled_rows(rows, "Balance Sheet", re.compile(r"total equity", re.I))
        self.assertEqual(selected[(1, 2024)]["value_numeric"], 100)
        self.assertEqual(ambiguous, 0)

    def test_excludes_matching_exclude_pattern(self):
        import re
        rows = [obs(1, "RWA Breakdown", "Credit risk - Total Credit Risk-Weighted Assets (CRWA)", 2024, 500)]
        selected, _ = _select_labeled_rows(rows, "RWA Breakdown", re.compile(r"total.*rwa", re.I), re.compile(r"of which|total", re.I))
        self.assertEqual(selected, {})


class LoanConcentrationQualityTests(unittest.TestCase):
    def test_groups_stage_balances_by_category(self):
        rows = [
            obs(1, "Asset Quality", "Loans and advances to customers - Stage 1", 2024, 900),
            obs(1, "Asset Quality", "Loans and advances to customers - Stage 2", 2024, 80),
            obs(1, "Asset Quality", "Placements with banks - Stage 1", 2024, 200),
        ]
        result = loan_concentration_quality(rows)
        self.assertEqual(result["stage_balances"][1][2024]["Loans and advances to customers"]["stage_1"], 900)
        self.assertEqual(result["stage_balances"][1][2024]["Placements with banks"]["stage_1"], 200)
        self.assertEqual(result["coverage"]["banks_with_stage_data"], 1)

    def test_stage_with_no_prefix_falls_back_to_total(self):
        rows = [obs(1, "Asset Quality", "Stage 3", 2024, 5)]
        result = loan_concentration_quality(rows)
        self.assertEqual(result["stage_balances"][1][2024]["Total"]["stage_3"], 5)

    def test_coverage_and_npl_ratio_rows_captured(self):
        rows = [obs(1, "Asset Quality", "Stage 3 coverage ratio", 2024, 45.2)]
        result = loan_concentration_quality(rows)
        self.assertEqual(result["coverage_and_npl_ratios"][1][0]["value"], 45.2)

    def test_stage_basis_wording_does_not_fragment_the_category(self):
        # Unity Trust discloses "Gross carrying amount by IFRS 9 stage -
        # Stage 1 (12 month ECL)" / "- Stage 2 (Lifetime ECL - SICR)" / "-
        # Stage 3 (Lifetime ECL - credit impaired)" - the ECL-basis wording
        # differs per stage BY DEFINITION, so naively keeping it as part of
        # the category produced three different category strings for what
        # is really one metric, and the internal " - " inside "(Lifetime
        # ECL - SICR)" mangled the Stage 2 case into an unrelated fragment
        # ("...- -"). Found via a 2026-09-04 user report that a bank's own
        # worksheet clearly had this data when the comparison page claimed
        # it didn't.
        rows = [
            obs(1, "Asset Quality", "Gross carrying amount by IFRS 9 stage - Stage 1 (12 month ECL)", 2024, 900),
            obs(1, "Asset Quality", "Gross carrying amount by IFRS 9 stage - Stage 2 (Lifetime ECL - SICR)", 2024, 40),
            obs(1, "Asset Quality", "Gross carrying amount by IFRS 9 stage - Stage 3 (Lifetime ECL - credit impaired)", 2024, 5),
        ]
        result = loan_concentration_quality(rows)
        cats = result["stage_balances"][1][2024]
        self.assertEqual(list(cats.keys()), ["Gross carrying amount by IFRS 9 stage"])
        self.assertEqual(
            cats["Gross carrying amount by IFRS 9 stage"],
            {"stage_1": 900, "stage_2": 40, "stage_3": 5},
        )

    def test_stage_marker_removed_without_mangling_a_hyphenated_descriptor(self):
        # HSBC UK Bank's shape: the stage marker sits in its own segment,
        # separate from a genuine (non-boilerplate) descriptor that itself
        # contains " - ". The descriptor must survive intact.
        rows = [obs(1, "Asset Quality", "Loans - by IFRS 9 stage - Stage 1 - gross carrying amount", 2024, 500)]
        result = loan_concentration_quality(rows)
        self.assertEqual(result["stage_balances"][1][2024]["Loans - by IFRS 9 stage - gross carrying amount"]["stage_1"], 500)

    def test_stage_basis_wording_with_trailing_text_still_strips_fully(self):
        # British Arab Commercial Bank's Stage 3 parenthetical is "(lifetime
        # ECL, credit-impaired / default)" - the trailing "/ default" isn't
        # part of any fixed suffix vocabulary, so it used to survive
        # stripping while Stage 1/2's parenthetical stripped cleanly,
        # leaving Stage 3 with a different category string and vanishing
        # from the primary chart entirely (found via a 2026-09-04 user
        # report that BACB's chart looked narrower than others').
        rows = [
            obs(1, "Asset Quality", "Loans, by IFRS 9 stage (gross exposure) - Stage 1 (12-month ECL)", 2024, 270),
            obs(1, "Asset Quality", "Loans, by IFRS 9 stage (gross exposure) - Stage 2 (lifetime ECL, not credit-impaired)", 2024, 36),
            obs(1, "Asset Quality", "Loans, by IFRS 9 stage (gross exposure) - Stage 3 (lifetime ECL, credit-impaired / default)", 2024, 9),
        ]
        result = loan_concentration_quality(rows)
        cats = result["stage_balances"][1][2024]
        self.assertEqual(len(cats), 1)
        (only_cat,) = cats.values()
        self.assertEqual(only_cat, {"stage_1": 270, "stage_2": 36, "stage_3": 9})

    def test_stage_default_synonym_does_not_fragment_the_category(self):
        # FirstBank UK labels its Stage 3 row "Stage 3 / Default (Lifetime
        # ECL, credit-impaired)" - after "Stage 3" and its trailing
        # parenthetical are stripped, a dangling "/ Default" fragment used
        # to survive, giving Stage 3 a different category string than
        # Stage 1/2 and dropping it from the primary chart (found via a
        # 2026-09-04 user report that FirstBank UK's chart looked narrower
        # than others').
        rows = [
            obs(1, "Asset Quality", "Gross carrying amount by IFRS 9 stage - Stage 1 (12-month ECL)", 2024, 550),
            obs(1, "Asset Quality", "Gross carrying amount by IFRS 9 stage - Stage 2 (Lifetime ECL, not credit-impaired)", 2024, 2),
            obs(1, "Asset Quality", "Gross carrying amount by IFRS 9 stage - Stage 3 / Default (Lifetime ECL, credit-impaired)", 2024, 32),
        ]
        result = loan_concentration_quality(rows)
        cats = result["stage_balances"][1][2024]
        self.assertEqual(len(cats), 1)
        (only_cat,) = cats.values()
        self.assertEqual(only_cat, {"stage_1": 550, "stage_2": 2, "stage_3": 32})

    def test_stage_scope_footnote_on_one_stage_does_not_fragment_the_category(self):
        # Barclays Bank UK PLC attaches a scope footnote only to its Stage 3
        # row - "Stage 3 (incl. POCI where separately disclosed)" - with no
        # equivalent wording on Stage 1/2. Left in, it fragments Stage 3 into
        # its own category apart from Stage 1/2, so Stage 3 balances vanish
        # from the shared chart.
        rows = [
            obs(1, "Asset Quality", "Gross exposure by IFRS 9 stage - Stage 1", 2024, 500),
            obs(1, "Asset Quality", "Gross exposure by IFRS 9 stage - Stage 2", 2024, 50),
            obs(1, "Asset Quality", "Gross exposure by IFRS 9 stage - Stage 3 (incl. POCI where separately disclosed)", 2024, 8),
        ]
        result = loan_concentration_quality(rows)
        cats = result["stage_balances"][1][2024]
        self.assertEqual(len(cats), 1)
        (only_cat,) = cats.values()
        self.assertEqual(only_cat, {"stage_1": 500, "stage_2": 50, "stage_3": 8})


class RwaDensityTests(unittest.TestCase):
    def test_rwa_to_assets_uses_pillar3_total_rwas_not_breakdown_total(self):
        rows = [
            obs(1, "Total RWAs", "Total RWAs", 2024, 1000),
            obs(1, "Balance Sheet", "Assets - Total assets", 2024, 10000),
        ]
        result = rwa_density(rows)
        self.assertEqual(result["rwa_to_assets_pct"][1][2024], 10.0)

    def test_category_breakdown_excludes_total_and_of_which_rows(self):
        rows = [
            obs(1, "Total RWAs", "Total RWAs", 2024, 1000),
            obs(1, "RWA Breakdown", "Credit risk", 2024, 800),
            obs(1, "RWA Breakdown", "Credit risk - Of which: standardised approach", 2024, 300),
            obs(1, "RWA Breakdown", "Total RWA", 2024, 1000),
        ]
        result = rwa_density(rows)
        labels = [row["label"] for row in result["rwa_category_composition"]["1:2024"]]
        self.assertEqual(labels, ["Credit risk"])
        self.assertEqual(result["rwa_category_composition"]["1:2024"][0]["pct_of_total_rwa"], 80.0)

    def test_category_breakdown_excludes_cross_sheet_unit_mismatch(self):
        # Total RWAs (Pillar 3 metric sheet) carries no per-row unit; a bank
        # whose Total RWAs sheet is £m while its RWA Breakdown is £'000 (e.g.
        # ABC International Bank) produces category percentages ~1000x too
        # large. A whole bank-year whose categories sum wildly over 100%
        # must be dropped rather than published as a broken chart.
        rows = [
            obs(1, "Total RWAs", "Total RWAs", 2024, 1.0),
            obs(1, "RWA Breakdown", "Credit risk", 2024, 800),
            obs(1, "RWA Breakdown", "Operational risk", 2024, 200),
        ]
        result = rwa_density(rows)
        self.assertNotIn("1:2024", result["rwa_category_composition"])
        self.assertEqual(result["coverage"]["implausible_rwa_category_sum_skipped"], 1)

    def test_category_breakdown_recovers_total_labeled_rows_when_thats_all_there_is(self):
        # Bank of the Philippine Islands (Europe) names its only level of RWA
        # disaggregation "Total Credit/Market/Operational Risk-Weighted
        # Assets" - the blanket "total" exclusion would otherwise strip every
        # row, leaving zero categories despite real per-risk-type data. The
        # true grand total ("Total Risk Exposure Amount") is identified by
        # internal self-consistency (its value equals the sum of the other
        # candidates), not by proximity to the separate Total RWAs sheet -
        # that sheet can disagree with RWA Breakdown's own internal total by
        # a few percent without the row selection being wrong.
        rows = [
            obs(1, "Total RWAs", "Total RWAs", 2024, 150420),
            obs(1, "RWA Breakdown", "Total Credit Risk-Weighted Assets (CRWA)", 2024, 150420),
            obs(1, "RWA Breakdown", "Total Market Risk-Weighted Assets (MRWA)", 2024, 6330),
            obs(1, "RWA Breakdown", "Total Operational Risk-Weighted Assets (ORWA)", 2024, 4703),
            obs(1, "RWA Breakdown", "Total Risk Exposure Amount", 2024, 161453),
        ]
        result = rwa_density(rows)
        labels = {row["label"] for row in result["rwa_category_composition"]["1:2024"]}
        self.assertEqual(
            labels,
            {
                "Total Credit Risk-Weighted Assets (CRWA)",
                "Total Market Risk-Weighted Assets (MRWA)",
                "Total Operational Risk-Weighted Assets (ORWA)",
            },
        )

    def test_category_breakdown_leaves_layered_structure_alone(self):
        # C. Hoare & Co discloses genuine finer-grained exposure-class rows
        # alongside redundant "Total X risk" subtotals. The primary filter
        # already yields real categories here, so the total-labeled-rows
        # fallback must not fire and must not add the subtotal back in.
        rows = [
            obs(1, "Total RWAs", "Total RWAs", 2024, 1000),
            obs(1, "RWA Breakdown", "Institutions", 2024, 100),
            obs(1, "RWA Breakdown", "Corporates", 2024, 200),
            obs(1, "RWA Breakdown", "Total credit risk", 2024, 300),
        ]
        result = rwa_density(rows)
        labels = {row["label"] for row in result["rwa_category_composition"]["1:2024"]}
        self.assertEqual(labels, {"Institutions", "Corporates"})

    def test_category_breakdown_recovers_a_total_labeled_row_alongside_real_categories(self):
        # Unity Trust: "Operational risk" and "Credit Valuation Adjustment"
        # survive the primary filter untouched, but its only credit-risk
        # figure is named "Total credit risk" and gets excluded alongside
        # the real grand total "Total RWA" - unlike the layered C. Hoare &
        # Co case above, credit risk here isn't already covered by any
        # other accepted category, so it must be added back rather than
        # dropped as a redundant subtotal.
        rows = [
            obs(1, "Total RWAs", "Total RWAs", 2024, 1065248),
            obs(1, "RWA Breakdown", "Operational risk", 2024, 180965),
            obs(1, "RWA Breakdown", "Credit Valuation Adjustment", 2024, 633),
            obs(1, "RWA Breakdown", "Total credit risk", 2024, 883650),
            obs(1, "RWA Breakdown", "Total RWA", 2024, 1065248),
        ]
        result = rwa_density(rows)
        labels = {row["label"] for row in result["rwa_category_composition"]["1:2024"]}
        self.assertEqual(labels, {"Operational risk", "Credit Valuation Adjustment", "Total credit risk"})


class LeverageTests(unittest.TestCase):
    def test_equity_to_assets_and_reported_ratio_reported_side_by_side(self):
        rows = [
            obs(1, "Balance Sheet", "Assets - Total assets", 2024, 1000),
            obs(1, "Balance Sheet", "Equity - Total equity", 2024, 80),
            {**obs(1, "Leverage Ratio", "UK leverage ratio", 2024, 7.5), "unit": "%", "value_raw": "7.5%"},
        ]
        result = leverage(rows)
        self.assertEqual(result["equity_to_assets_pct"][1][2024], 8.0)
        self.assertEqual(result["leverage_ratio_reported_pct"][1][2024], 7.5)
        self.assertEqual(result["coverage"]["banks_with_both"], 1)


class IncomeVolatilityTests(unittest.TestCase):
    def test_prefers_bare_profit_for_year_over_attributable_variant(self):
        rows = [
            obs(1, "Profit & Loss", "Operating expenses - Profit for the year", 2024, 50),
        ]
        result = income_volatility(rows)
        self.assertEqual(result["profit_or_loss_for_year"][1][2024], 50)
        self.assertEqual(result["labels_used"][1][2024], "Operating expenses - Profit for the year")

    def test_excludes_comprehensive_and_discontinued_variants(self):
        rows = [obs(1, "Profit & Loss", "Total comprehensive income for the year", 2024, 999)]
        result = income_volatility(rows)
        self.assertEqual(result["profit_or_loss_for_year"], {})

    def test_falls_back_to_attributable_variant_when_no_bare_line_exists(self):
        # Unity Trust has no minority interest at all, so its ONLY
        # disclosed headline line is "Profit for the year attributable to
        # shareholders" - the hard "attributable" exclusion used to leave
        # this bank-year with no profit figure whatsoever, despite one
        # being clearly disclosed (found via a 2026-09-04 user report).
        rows = [obs(1, "Profit & Loss", "Profit for the year attributable to shareholders", 2024, 40789)]
        result = income_volatility(rows)
        self.assertEqual(result["profit_or_loss_for_year"][1][2024], 40789)

    def test_prefers_bare_line_over_attributable_variant_when_both_exist(self):
        # A bank with genuine minority interest discloses both a group-
        # level headline AND an NCI-split "attributable" line - the group
        # figure must still win, not the fallback.
        rows = [
            obs(1, "Profit & Loss", "Profit for the year", 2024, 100),
            obs(1, "Profit & Loss", "Profit for the year attributable to owners of the parent", 2024, 80),
        ]
        result = income_volatility(rows)
        self.assertEqual(result["profit_or_loss_for_year"][1][2024], 100)

    def test_computes_yoy_change_and_volatility(self):
        rows = [
            obs(1, "Profit & Loss", "Profit for the year", 2022, 100),
            obs(1, "Profit & Loss", "Profit for the year", 2023, 150),
            obs(1, "Profit & Loss", "Profit for the year", 2024, 120),
        ]
        result = income_volatility(rows)
        self.assertEqual(result["yoy_change_pct"][1][2023], 50.0)
        self.assertEqual(result["yoy_change_pct"][1][2024], -20.0)
        self.assertIn(1, result["volatility_stdev_of_yoy_pct"])


if __name__ == "__main__":
    unittest.main()
