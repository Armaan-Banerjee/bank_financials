import unittest

from in041_spend_metrics import cost_base, capital_deployment


def obs(frn, sheet, row_label, year, value, bank="Bank", unit="£", row_kind=None):
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
        "unit": unit,
        "row_kind": row_kind,
    }


class CostBaseTests(unittest.TestCase):
    def test_selects_personnel_other_opex_and_total_opex(self):
        rows = [
            obs(1, "Profit & Loss", "Operating expenses - Personnel expenses", 2024, -50, row_kind="DATA"),
            obs(1, "Profit & Loss", "Operating expenses - Other operating expenses", 2024, -30, row_kind="DATA"),
            obs(1, "Profit & Loss", "Operating expenses - Total operating expenses", 2024, -80, row_kind="TOTAL"),
            obs(1, "Profit & Loss", "Income - Total operating income", 2024, 200, row_kind="TOTAL"),
        ]
        result = cost_base(rows)
        self.assertEqual(result["personnel_expense"][1][2024], -50)
        self.assertEqual(result["other_operating_expense"][1][2024], -30)
        self.assertEqual(result["total_operating_expense"][1][2024], -80)
        self.assertEqual(result["revenue"][1][2024], 200)
        self.assertEqual(result["cost_to_income_pct"][1][2024], 40.0)
        self.assertEqual(result["personnel_expense_pct_of_revenue"][1][2024], 25.0)

    def test_includes_total_opex_before_impairment_variant(self):
        # UBI UK/Arab Bank Europe/HBL Bank UK/Close Brothers each label their
        # genuine, complete opex TOTAL row "... before impairment/provisions/
        # amortisation" - excluding credit losses and one-off items from
        # opex is the standard cost-to-income convention, so this must be
        # INCLUDED, not rejected merely for containing "before ".
        rows = [obs(1, "Profit & Loss", "Income - Total operating expenses before impairment losses", 2024, -80, row_kind="TOTAL")]
        result = cost_base(rows)
        self.assertEqual(result["total_operating_expense"][1][2024], -80)

    def test_excludes_revenue_row_describing_expenses_as_before(self):
        # LHV/Persia International Bank's revenue TOTAL row is "Net operating
        # income (... BEFORE operating expenses ...)" - the phrase "operating
        # expense" in its own descriptive text must not get it mistaken for
        # the opex total itself.
        rows = [obs(1, "Profit & Loss", "Income - Net operating income (FY2024's own subtotal, BEFORE operating expenses)", 2024, 200, row_kind="TOTAL")]
        result = cost_base(rows)
        self.assertEqual(result["total_operating_expense"], {})

    def test_prefers_total_operating_income_over_net_operating_income(self):
        rows = [
            obs(1, "Profit & Loss", "Income - Total operating income", 2024, 200, row_kind="TOTAL"),
            obs(1, "Profit & Loss", "Income - Net Operating Income", 2024, 150, row_kind="TOTAL"),
        ]
        result = cost_base(rows)
        self.assertEqual(result["revenue"][1][2024], 200)

    def test_keeps_total_income_under_other_income_section(self):
        # UBP's source workbook uses "Other operating income" as the
        # section heading.  The residual line of that name is not revenue,
        # but its section must not suppress the reported total beneath it.
        rows = [
            obs(1, "Profit & Loss", "Other operating income - Total operating income", 2012, 200, row_kind="TOTAL"),
            obs(1, "Profit & Loss", "Operating expenses - Total operating expenses", 2012, -80, row_kind="TOTAL"),
        ]
        result = cost_base(rows)
        self.assertEqual(result["revenue"][1][2012], 200)
        self.assertEqual(result["cost_to_income_pct"][1][2012], 40.0)

    def test_excludes_opex_total_that_only_matches_via_section_prefix(self):
        # Punjab National Bank International places "Profit/(loss) before
        # tax" inside a SECTION literally named "Operating expenses"
        # (alongside the genuine "Total operating expenses" TOTAL row) - the
        # resulting full label matches _TOTAL_OPEX_RE purely because of the
        # section name, not the row's own text, and must not be selected
        # over (or instead of) the real opex total.
        rows = [
            obs(1, "Profit & Loss", "Operating expenses - Total operating expenses", 2024, -80, row_kind="TOTAL"),
            obs(1, "Profit & Loss", "Operating expenses - Profit/(loss) before tax", 2024, 120, row_kind="TOTAL"),
            obs(1, "Profit & Loss", "Income - Total operating income", 2024, 200, row_kind="TOTAL"),
        ]
        result = cost_base(rows)
        self.assertEqual(result["total_operating_expense"][1][2024], -80)

    def test_prefers_total_operating_income_with_descriptive_suffix_over_net(self):
        # HSBC Bank Plc's own revenue TOTAL row is "Total operating income
        # (IFRS 4 presentation, pre-FY2023)" - the descriptive suffix must
        # not stop it beating a shorter but non-gross "Net operating income"
        # (post credit-loss-charge) row on the tie-break.
        rows = [
            obs(1, "Profit & Loss", "Income - Total operating income (IFRS 4 presentation, pre-FY2023)", 2024, 200, row_kind="TOTAL"),
            obs(1, "Profit & Loss", "Income - Net operating income", 2024, 150, row_kind="TOTAL"),
        ]
        result = cost_base(rows)
        self.assertEqual(result["revenue"][1][2024], 200)

    def test_non_gbp_absolute_figure_excluded_not_mislabeled(self):
        # A bank reporting in USD (e.g. Standard Chartered Bank, $m) must
        # not have its absolute figures silently treated as GBP - excluded
        # from the £-denominated series rather than mislabeled, but the
        # cost_to_income_pct RATIO still computes fine since both sides
        # share the same (unconverted) currency.
        rows = [
            obs(1, "Profit & Loss", "Operating expenses - Total operating expenses", 2024, -80, unit="$m", row_kind="TOTAL"),
            obs(1, "Profit & Loss", "Income - Total operating income", 2024, 200, unit="$m", row_kind="TOTAL"),
        ]
        result = cost_base(rows)
        self.assertEqual(result["total_operating_expense"], {1: {2024: None}})
        self.assertEqual(result["revenue"], {1: {2024: None}})
        self.assertEqual(result["cost_to_income_pct"][1][2024], 40.0)


class CapitalDeploymentTests(unittest.TestCase):
    def test_computes_asset_mix_as_pct_of_total_assets(self):
        rows = [
            obs(1, "Balance Sheet", "Assets - Total assets", 2024, 1000),
            obs(1, "Balance Sheet", "Assets - Loans and advances to customers", 2024, 600),
            obs(1, "Balance Sheet", "Assets - Investment securities", 2024, 250),
            obs(1, "Balance Sheet", "Assets - Cash and cash equivalents", 2024, 150),
        ]
        result = capital_deployment(rows)
        self.assertEqual(result["loans_pct_of_assets"][1][2024], 60.0)
        self.assertEqual(result["treasury_investments_pct_of_assets"][1][2024], 25.0)
        self.assertEqual(result["cash_pct_of_assets"][1][2024], 15.0)
        self.assertEqual(result["coverage"]["banks_with_all_three"], 1)

    def test_excludes_liability_side_debt_securities_in_issue(self):
        rows = [
            obs(1, "Balance Sheet", "Assets - Total assets", 2024, 1000),
            obs(1, "Balance Sheet", "Liabilities - Debt securities in issue", 2024, 400),
        ]
        result = capital_deployment(rows)
        self.assertEqual(result["treasury_investments_pct_of_assets"], {})

    def test_excludes_restricted_cash_sub_line(self):
        rows = [
            obs(1, "Balance Sheet", "Assets - Total assets", 2024, 1000),
            obs(1, "Balance Sheet", "Non-current assets - Restricted cash and cash equivalents", 2024, 50),
        ]
        result = capital_deployment(rows)
        self.assertEqual(result["cash_pct_of_assets"], {})

    def test_matches_cash_row_with_comma_and_other_before_balances(self):
        # Cater Allen's own Balance Sheet row is "Cash, and other balances at
        # central banks" - the comma plus "other" between "Cash" and
        # "balances" made the tighter "cash and (cash equivalents|balances)"
        # pattern miss it entirely, silently dropping its cash figure and
        # leaving its capital-deployment chart looking empty (found via a
        # 2026-09-04 user report).
        rows = [
            obs(1, "Balance Sheet", "Assets - Total assets", 2024, 1000),
            obs(1, "Balance Sheet", "Assets - Cash, and other balances at central banks", 2024, 400),
        ]
        result = capital_deployment(rows)
        self.assertEqual(result["cash_pct_of_assets"][1][2024], 40.0)

    def test_matches_loans_to_customers_without_and_advances(self):
        # Coutts labels its own row "Loans to customers - amortised cost" -
        # without "and advances" - which the exact-phrase-only pattern
        # missed entirely.
        rows = [
            obs(1, "Balance Sheet", "Assets - Total assets", 2024, 1000),
            obs(1, "Balance Sheet", "Assets - Loans to customers - amortised cost", 2024, 500),
        ]
        result = capital_deployment(rows)
        self.assertEqual(result["loans_pct_of_assets"][1][2024], 50.0)


if __name__ == "__main__":
    unittest.main()
