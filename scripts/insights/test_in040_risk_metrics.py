import unittest

from in040_risk_metrics import (
    _bare_label,
    _currency_and_scale,
    _normalized_ratio_pct,
    _select_labeled_rows,
    loan_concentration_quality,
    rwa_density,
    leverage,
    income_volatility,
)


def obs(frn, sheet, row_label, year, value, bank="Bank", row_kind=None, unit=None):
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
        "row_kind": row_kind,
        "unit": unit,
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

    def test_coverage_and_npl_catalogue_still_picks_up_section_only_matches(self):
        # Unlike select_labeled_rows's single-winner selection, this
        # catalogue deliberately wants every row filed under a coverage/
        # NPL-themed SECTION even when the row's own text doesn't repeat
        # "coverage"/"NPL" (e.g. a stage-level breakdown row under a
        # "Coverage ratios (as disclosed)" section).
        rows = [obs(1, "Asset Quality", "Coverage ratios (as disclosed) - Stage 3 as a % of gross core loans", 2024, 45.2)]
        result = loan_concentration_quality(rows)
        self.assertEqual(result["coverage_and_npl_ratios"][1][0]["value"], 45.2)

    def test_excludes_a_provision_charge_row_that_only_matches_via_section_title(self):
        # National Bank of Egypt UK's Asset Quality sheet has a SECTION
        # named "Bad and doubtful debt provision movement and
        # non-performing loans" - an absolute-£ P&L charge/release row
        # beneath it ("Net (release)/charge of provisions for bad and
        # doubtful debts") got swept into this ratio/balance catalogue
        # purely via the section title mentioning "non-performing loans",
        # even though the row itself is neither a ratio nor an NPL balance.
        rows = [obs(1, "Asset Quality", "Bad and doubtful debt provision movement and non-performing loans - "
                     "Net (release)/charge of provisions for bad and doubtful debts", 2024, -443787.0)]
        result = loan_concentration_quality(rows)
        self.assertEqual(result["coverage_and_npl_ratios"], {})

    def test_recognizes_coverage_phrasing_without_the_literal_word_ratio(self):
        # HSBC UK Bank's own wording is "ECL coverage - overall (total
        # allowance / total gross)" - no adjacent "ratio" - and National
        # Westminster Bank's is "... - Stage 1 coverage". A regex requiring
        # the exact phrase "coverage ratio" missed both, along with 30+
        # other banks' equally genuine but differently-worded coverage
        # disclosures (found via a puppeteer sweep of the live deliverable).
        rows = [
            obs(1, "Asset Quality", "Derived ratios - ECL coverage - overall (total allowance / total gross)", 2024, 12.3),
            obs(2, "Asset Quality", "ECL provision coverage (ECL provisions / loans) - Stage 1 coverage", 2024, 4.5),
            obs(3, "Asset Quality", "Key ratios (as disclosed) - Credit loss reserve ratio, Stage 1 (%)", 2024, 1.1),
            obs(4, "Asset Quality", "Key ratios (as disclosed) - Proportion of loans in Stage 3 (%)", 2024, 2.2),
        ]
        result = loan_concentration_quality(rows)
        for frn in (1, 2, 3, 4):
            self.assertEqual(len(result["coverage_and_npl_ratios"][frn]), 1)

    def test_excludes_non_ratio_rows_that_only_match_via_an_impairment_and_coverage_section(self):
        # Tandem's own SECTION is literally named "Impairment and Coverage"
        # and contains two genuine ratios alongside three unrelated rows -
        # a hedge-accounting fair value adjustment, a bare net loans balance
        # (not a ratio), and a bare provision balance/charge with no ratio
        # qualifier - all three matched only via the section title.
        rows = [
            obs(1, "Asset Quality", "Impairment and Coverage - Coverage ratio (provision / impaired loans)", 2024, 55.0),
            obs(1, "Asset Quality", "Impairment and Coverage - NPL ratio (impaired loans / gross loans)", 2024, 3.0),
            obs(1, "Asset Quality", "Impairment and Coverage - Fair value adjustments (hedge accounting)", 2024, -2238.0),
            obs(1, "Asset Quality", "Impairment and Coverage - Net Loans and Advances to Customers", 2024, 436845.0),
            obs(1, "Asset Quality", "Impairment and Coverage - Provision for impairment", 2024, -5834.0),
        ]
        result = loan_concentration_quality(rows)
        values = {r["value"] for r in result["coverage_and_npl_ratios"][1]}
        self.assertEqual(values, {55.0, 3.0})

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

    def test_pre_ifrs9_equivalence_wording_is_not_treated_as_a_real_stage(self):
        # TSB Bank's FY2014-2017 pre-IFRS 9 IAS 39 "Impaired loans" total is
        # captioned "... broadly equivalent to Stage 3 above" - a
        # cross-reference to a DIFFERENT (incompatible) classification
        # basis, not a genuine IFRS 9 Stage 3 row. Naively matching "Stage
        # 3" here fabricated a spurious stage_3-only bar for years that
        # have no real stage split at all (IFRS 9 wasn't adopted until
        # FY2018), found via a 2026-09-07 user report that TSB's
        # loan-concentration chart looked odd before 2018.
        rows = [obs(1, "Asset Quality", "Impaired loans (IAS 39 basis, pre-IFRS 9 - broadly equivalent to Stage 3 above)", 2016, 140)]
        result = loan_concentration_quality(rows)
        self.assertEqual(result["stage_balances"], {})

    def test_explicit_stage_equivalence_disclaimer_is_not_treated_as_a_real_stage(self):
        # British Arab Commercial Bank's pre-IFRS 9 impairment-provision rows
        # are captioned "... not a Stage 1/2/3 equivalent, see note" -
        # explicitly disclaiming any stage mapping, yet the literal digits
        # would still satisfy the bare stage regex.
        rows = [obs(1, "Asset Quality", "Impairment provision (IAS 39 individual/collective model - not a Stage 1/2/3 equivalent, see note) - Total impairment provision", 2016, -48803)]
        result = loan_concentration_quality(rows)
        self.assertEqual(result["stage_balances"], {})

    def test_genuine_stage_marker_survives_alongside_unrelated_equivalence_wording(self):
        # A label can legitimately use "equivalent" in an unrelated sense
        # elsewhere while still carrying a real trailing "Stage N" marker -
        # the exclusion must not blanket-suppress every "equivalent" label.
        rows = [obs(1, "Asset Quality", "IFRS 9 stage-level exposure - no equivalent balance-level stage table found in prior years - Stage 1 gross exposure", 2025, 100)]
        result = loan_concentration_quality(rows)
        cats = result["stage_balances"][1][2025]
        self.assertEqual(len(cats), 1)
        (only_cat,) = cats.values()
        self.assertEqual(only_cat, {"stage_1": 100})


class CurrencyAndScaleTests(unittest.TestCase):
    def test_parses_currency_and_thousand_scale(self):
        self.assertEqual(_currency_and_scale("£'000"), ("GBP", 1000.0))

    def test_parses_currency_and_million_scale(self):
        self.assertEqual(_currency_and_scale("£m"), ("GBP", 1_000_000.0))

    def test_parses_currency_and_billion_scale(self):
        self.assertEqual(_currency_and_scale("£bn"), ("GBP", 1_000_000_000.0))

    def test_recognizes_usd_and_conversion_annotation(self):
        self.assertEqual(_currency_and_scale("£m, conv. from USD"), ("GBP", 1_000_000.0))

    def test_bare_unit_defaults_to_scale_one(self):
        self.assertEqual(_currency_and_scale("£"), ("GBP", 1.0))

    def test_missing_unit_returns_none_currency(self):
        self.assertEqual(_currency_and_scale(None), (None, 1.0))
        self.assertEqual(_currency_and_scale(""), (None, 1.0))

    def test_percent_unit_has_no_recognizable_currency(self):
        self.assertEqual(_currency_and_scale("%"), (None, 1.0))

    def test_recognizes_spelled_out_million(self):
        # ICICI Bank UK's own Total RWAs unit is "USD million" - "m" isn't
        # its own token there, it's the start of the word "million".
        self.assertEqual(_currency_and_scale("USD million"), ("USD", 1_000_000.0))

    def test_recognizes_mm_as_millions_abbreviation(self):
        # TD Bank Europe's own unit is "CAD MM" - a standard finance
        # abbreviation for millions, not matched by a single "m" pattern.
        self.assertEqual(_currency_and_scale("CAD MM"), ("CAD", 1_000_000.0))


class NormalizedRatioPctTests(unittest.TestCase):
    def test_rescales_a_millions_over_thousands_mismatch(self):
        num = {"value_numeric": 1.0, "unit": "£m"}
        den = {"value_numeric": 1000.0, "unit": "£'000"}
        self.assertEqual(_normalized_ratio_pct(num, den), 100.0)

    def test_returns_none_when_either_side_has_no_unit(self):
        num = {"value_numeric": 1.0, "unit": "£m"}
        den = {"value_numeric": 1000.0, "unit": None}
        self.assertIsNone(_normalized_ratio_pct(num, den))

    def test_returns_none_across_a_recognizable_currency_mismatch(self):
        num = {"value_numeric": 1.0, "unit": "$m"}
        den = {"value_numeric": 1000.0, "unit": "£'000"}
        self.assertIsNone(_normalized_ratio_pct(num, den))


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

    def test_category_breakdown_excludes_cross_sheet_unit_mismatch_when_unit_unknown(self):
        # When neither side's `unit` was captured at all (the general
        # fallback case - e.g. an older extraction, or a genuinely blank
        # unit cell), there's nothing to normalize against, so a bank-year
        # whose categories sum wildly over 100% is still dropped rather
        # than published as a broken chart - the pre-2026-09-07 behavior,
        # kept as the safety net for whatever this normalization can't fix.
        rows = [
            obs(1, "Total RWAs", "Total RWAs", 2024, 1.0),
            obs(1, "RWA Breakdown", "Credit risk", 2024, 800),
            obs(1, "RWA Breakdown", "Operational risk", 2024, 200),
        ]
        result = rwa_density(rows)
        self.assertNotIn("1:2024", result["rwa_category_composition"])
        self.assertEqual(result["coverage"]["implausible_rwa_category_sum_skipped"], 1)

    def test_category_breakdown_normalizes_a_known_cross_sheet_scale_mismatch(self):
        # ABC International Bank: Total RWAs sheet in £m, RWA Breakdown in
        # £'000 - both units are now captured (extract_metrics.py, fixed
        # 2026-09-07), so this is no longer a guess: 1.0 (£m) == 1000 (£'000
        # unit), so Credit risk 800/1000*100 = 80%, not 80,000%.
        rows = [
            obs(1, "Total RWAs", "Total RWAs", 2024, 1.0, unit="£m"),
            obs(1, "RWA Breakdown", "Credit risk", 2024, 800, unit="£'000"),
            obs(1, "RWA Breakdown", "Operational risk", 2024, 200, unit="£'000"),
        ]
        result = rwa_density(rows)
        rows_out = {r["label"]: r["pct_of_total_rwa"] for r in result["rwa_category_composition"]["1:2024"]}
        self.assertEqual(rows_out["Credit risk"], 80.0)
        self.assertEqual(rows_out["Operational risk"], 20.0)

    def test_rwa_to_assets_normalizes_a_known_cross_sheet_scale_mismatch(self):
        # Credit Suisse UK's real shape: Total RWAs disclosed in £m, its
        # Balance Sheet in £'000 - raw division gives ~0.04%, which the
        # plausibility guard correctly rejected as implausible before this
        # sheet's own unit was captured; now normalized to the real ~37%.
        rows = [
            obs(1, "Total RWAs", "Total RWAs", 2024, 1340, unit="£m"),
            obs(1, "Balance Sheet", "Assets - Total assets", 2024, 3579171, unit="£'000"),
        ]
        result = rwa_density(rows)
        self.assertEqual(result["rwa_to_assets_pct"][1][2024], round(1340 * 1000 / 3579171 * 100, 2))

    def test_rwa_to_assets_does_not_guess_across_a_genuine_currency_mismatch(self):
        # A bank whose Total RWAs and Balance Sheet are captured in
        # genuinely different currencies (not just different scales of the
        # same currency) must not be silently normalized as if they were -
        # falls back to the raw ratio + plausibility guard instead.
        rows = [
            obs(1, "Total RWAs", "Total RWAs", 2024, 1.0, unit="$m"),
            obs(1, "Balance Sheet", "Assets - Total assets", 2024, 3579171, unit="£'000"),
        ]
        result = rwa_density(rows)
        self.assertEqual(result["rwa_to_assets_pct"], {})

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
            obs(1, "Profit & Loss", "Operating expenses - Profit for the year", 2024, 50, row_kind="TOTAL"),
        ]
        result = income_volatility(rows)
        self.assertEqual(result["profit_or_loss_for_year"][1][2024], 50)
        self.assertEqual(result["labels_used"][1][2024], "Operating expenses - Profit for the year")

    def test_excludes_comprehensive_and_discontinued_variants(self):
        rows = [obs(1, "Profit & Loss", "Total comprehensive income for the year", 2024, 999, row_kind="TOTAL")]
        result = income_volatility(rows)
        self.assertEqual(result["profit_or_loss_for_year"], {})

    def test_falls_back_to_attributable_variant_when_no_bare_line_exists(self):
        # Unity Trust has no minority interest at all, so its ONLY
        # disclosed headline line is "Profit for the year attributable to
        # shareholders" - the hard "attributable" exclusion used to leave
        # this bank-year with no profit figure whatsoever, despite one
        # being clearly disclosed (found via a 2026-09-04 user report).
        rows = [obs(1, "Profit & Loss", "Profit for the year attributable to shareholders", 2024, 40789, row_kind="TOTAL")]
        result = income_volatility(rows)
        self.assertEqual(result["profit_or_loss_for_year"][1][2024], 40789)

    def test_prefers_bare_line_over_attributable_variant_when_both_exist(self):
        # A bank with genuine minority interest discloses both a group-
        # level headline AND an NCI-split "attributable" line - the group
        # figure must still win, not the fallback.
        rows = [
            obs(1, "Profit & Loss", "Profit for the year", 2024, 100, row_kind="TOTAL"),
            obs(1, "Profit & Loss", "Profit for the year attributable to owners of the parent", 2024, 80, row_kind="TOTAL"),
        ]
        result = income_volatility(rows)
        self.assertEqual(result["profit_or_loss_for_year"][1][2024], 100)

    def test_computes_yoy_change_and_volatility(self):
        rows = [
            obs(1, "Profit & Loss", "Profit for the year", 2022, 100, row_kind="TOTAL"),
            obs(1, "Profit & Loss", "Profit for the year", 2023, 150, row_kind="TOTAL"),
            obs(1, "Profit & Loss", "Profit for the year", 2024, 120, row_kind="TOTAL"),
        ]
        result = income_volatility(rows)
        self.assertEqual(result["yoy_change_pct"][1][2023], 50.0)
        self.assertEqual(result["yoy_change_pct"][1][2024], -20.0)
        self.assertIn(1, result["volatility_stdev_of_yoy_pct"])

    def test_excludes_data_row_that_merely_mentions_profit_for_the_year(self):
        # Co-operative Bank's HD-078 FY1972-1980 block has a DATA row
        # "Operating profit/Profit for the year (Group, before exceptional
        # items)" that is explicitly NOT the bank's real headline figure
        # (a section note says the genuine row is deliberately left blank
        # for these years) - only a TOTAL row can be the real headline.
        rows = [
            obs(1, "Profit & Loss", "HD-078: Group P&L (Group basis, not Bank Company-only) - "
                "Operating profit/Profit for the year (Group, before exceptional items)", 1980, 5.422,
                row_kind="DATA"),
        ]
        result = income_volatility(rows)
        self.assertEqual(result["profit_or_loss_for_year"], {})

    # NOTE: a SECTION label that itself contains " - " breaks own_label()'s
    # "split on the first ' - '" boundary heuristic - everything after that
    # internal dash, including the SECTION's own explanatory prose rather
    # than the row's own text, gets treated as "own text". This was the
    # actual root cause of the Co-operative Bank HD-078 leak (fixed by
    # rewriting that SECTION's prose to avoid an internal " - ", in
    # build_coop_bank.py). require_own_match does NOT fully close this
    # general class - it only prevents pollution via the FIRST " - "
    # segment (the true section/label boundary in the common case). A
    # SECTION whose own prose contains a second " - " ahead of a trigger
    # phrase can still slip past it. Production data is swept for this
    # specific shape by test_statement_row_selection.py's
    # SectionProseAudit, which scans every live SECTION label for exactly
    # this risk rather than relying on catching each instance by hand.


if __name__ == "__main__":
    unittest.main()
