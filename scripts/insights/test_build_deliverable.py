import sqlite3
import unittest

from build_deliverable import curate_equity_composition, curate_equity_waterfall, curate_liability_composition


def _row(label, **components):
    return {"label": label, "values": components}


def _balance_sheet_conn(rows):
    """rows: list of (row_label, year, value_numeric, unit) tuples for one
    frn (always 1 here) - the minimal shape curate_liability_composition/
    curate_equity_composition read via a plain annual_metrics SELECT."""
    conn = sqlite3.connect(":memory:")
    conn.execute(
        "CREATE TABLE annual_metrics (frn TEXT, sheet TEXT, row_label TEXT, year TEXT, "
        "value_numeric REAL, unit TEXT)"
    )
    conn.executemany(
        "INSERT INTO annual_metrics (frn, sheet, row_label, year, value_numeric, unit) VALUES (1, 'Balance Sheet', ?, ?, ?, ?)",
        rows,
    )
    conn.commit()
    return conn


class LiabilityCompositionTests(unittest.TestCase):
    def test_deposits_from_customers_word_order_is_matched(self):
        """Reproduces both Barclays entities' real Balance Sheet wording -
        "Deposits at amortised cost from customers"/"...from banks" puts
        "customer"/"bank" AFTER "deposit", not before it. Before this fix
        neither _CUSTOMER_DEPOSITS_RE nor _BANK_DEPOSITS_RE matched this
        order at all, silently showing 0% for both categories on a bank
        whose largest liability line IS customer deposits."""
        conn = _balance_sheet_conn([
            ("Liabilities - Deposits at amortised cost from customers", "FY2025", 244666.0, "£m"),
            ("Liabilities - Deposits at amortised cost from banks", "FY2025", 125.0, "£m"),
            ("Liabilities - Subordinated liabilities", "FY2025", 14049.0, "£m"),
            ("Liabilities - Total liabilities", "FY2025", 282546.0, "£m"),
        ])
        out = curate_liability_composition(conn, 1)
        self.assertGreater(out["2025"]["customer_deposits_pct"], 80)
        self.assertGreater(out["2025"]["bank_deposits_pct"], 0)

    def test_asset_side_deposits_with_banks_is_not_counted_as_a_bank_deposit(self):
        """The word-order fix above loosens "bank deposit" matching to a
        wildcard ("deposits?.*banks?"), which could otherwise cross onto an
        ASSET-side row using the same two words in the opposite sense - a
        bank's own money placed with other banks (an asset) rather than
        money other banks placed with it (a liability). Confirms the
        in_liabilities_section() guard keeps this out of the liability
        tally."""
        conn = _balance_sheet_conn([
            ("Assets - Deposits with banks", "FY2025", 999.0, "£m"),
            ("Liabilities - Deposits at amortised cost from customers", "FY2025", 244666.0, "£m"),
            ("Liabilities - Total liabilities", "FY2025", 282546.0, "£m"),
        ])
        out = curate_liability_composition(conn, 1)
        self.assertEqual(out["2025"]["bank_deposits_pct"], 0.0)


class EquityCompositionTests(unittest.TestCase):
    def test_blended_other_reserves_label_is_not_counted_as_retained_earnings(self):
        """A handful of build scripts fold retained earnings together with
        a pension/FX/fair-value reserve under one blended label when a
        bank's own accounts don't split them - e.g. "Other reserves
        (retained earnings + pension reserve...)". That label contains the
        substring "retained earnings" and must NOT be counted as pure
        retained earnings - it stays unclassified and folds into the
        residual "other" bucket instead."""
        conn = _balance_sheet_conn([
            ("Equity - Share capital", "FY2025", 100.0, "£m"),
            ("Equity - Other reserves (retained earnings + pension reserve)", "FY2025", 50.0, "£m"),
            ("Equity - Total equity", "FY2025", 150.0, "£m"),
        ])
        out = curate_equity_composition(conn, 1)
        self.assertEqual(out["2025"]["retained_earnings_pct"], 0.0)
        self.assertAlmostEqual(out["2025"]["other_pct"], 33.33, places=1)

    def test_negative_unclassified_reserves_are_not_clamped_to_zero(self):
        """Reproduces NatWest Markets' real FY2025 Balance Sheet: share
        capital + retained earnings alone already exceed Total equity,
        because unclassified reserves (cash flow hedging, FX translation)
        are genuinely NEGATIVE that year. Unlike the asset/liability
        composition curators (whose named categories can't be negative by
        construction), equity's residual must be allowed to go negative
        too, or the three legs would silently sum to >100% with no
        visible explanation."""
        conn = _balance_sheet_conn([
            ("Equity - Called-up share capital", "FY2025", 400.0, "£m"),
            ("Equity - Share premium account", "FY2025", 1946.0, "£m"),
            ("Equity - Paid-in equity", "FY2025", 1192.0, "£m"),
            ("Equity - Retained earnings", "FY2025", 3537.0, "£m"),
            ("Equity - Cash flow hedging reserve", "FY2025", -97.0, "£m"),
            ("Equity - Foreign exchange reserve", "FY2025", -117.0, "£m"),
            ("Equity - Total equity", "FY2025", 6880.0, "£m"),
        ])
        out = curate_equity_composition(conn, 1)
        self.assertLess(out["2025"]["other_pct"], 0)
        total_pct = out["2025"]["share_capital_pct"] + out["2025"]["retained_earnings_pct"] + out["2025"]["other_pct"]
        self.assertAlmostEqual(total_pct, 100.0, places=1)

    def test_net_assets_outside_equity_section_is_not_mistaken_for_total_equity(self):
        """"Net assets" is a generic enough phrase (and _TOTAL_EQUITY_RE
        matches it exactly, as some smaller banks use it in place of
        "Total equity") that, without a section guard, an unrelated
        Assets-section row using the same exact wording would be wrongly
        picked up as the equity total. Confirms in_equity_section() keeps
        this scoped to the Equity section."""
        conn = _balance_sheet_conn([
            ("Assets - Net assets", "FY2025", 5.0, "£m"),
            ("Equity - Share capital", "FY2025", 100.0, "£m"),
            ("Equity - Total equity", "FY2025", 100.0, "£m"),
        ])
        out = curate_equity_composition(conn, 1)
        self.assertEqual(out["2025"]["total"], 100.0 * 1_000_000)  # "£m" is scaled to actual £ by scaled()


class CurateEquityWaterfallTests(unittest.TestCase):
    """A restatement/reclassification checkpoint (e.g. Monzo's real FY2020
    "Restated balance as at 1 March 2020": +12,536 Other reserves, -12,536
    Retained losses, Total equity unchanged) creates a checkpoint-to-
    checkpoint segment whose only movement row nets to exactly zero on the
    grand total. Before the 2026-09-06 fix, this still emitted a segment
    with an empty bars list - a visually blank second "FY2020" chart row
    with no bars and no visible reason for its own existence (a 2026-09-06
    user report on Monzo's chart; the equivalent 111 other empty segments
    across ~30 real banks were confirmed the same way)."""

    def test_a_net_zero_restatement_checkpoint_produces_no_empty_segment(self):
        by_order = {
            1: _row("Balance as at 28 February 2019", **{"Retained losses": "-85640", "Total equity": "115670"}),
            2: _row("Loss for the year (FY2020)", **{"Retained losses": "-113816", "Total equity": "-113816"}),
            3: _row("Shares issued", **{"Share premium": "112993", "Total equity": "112993"}),
            4: _row(
                "Balance as at 1 March 2020 (as previously reported)",
                **{"Retained losses": "-199436", "Share premium": "112993", "Total equity": "129004"},
            ),
            5: _row(
                "Prior year adjustments",
                **{"Retained losses": "-12536", "Other reserves": "12536", "Total equity": "0"},
            ),
            6: _row(
                "Restated balance as at 1 March 2020",
                **{"Retained losses": "-211972", "Other reserves": "12536", "Share premium": "112993", "Total equity": "129004"},
            ),
        }
        components = ["Retained losses", "Total equity", "Share premium", "Other reserves"]
        segments = curate_equity_waterfall(by_order, components)

        years_2020 = [s for s in segments if s["year"] == "2020"]
        self.assertEqual(len(years_2020), 1, "a net-zero restatement checkpoint must not add a second FY2020 row")
        self.assertGreater(len(years_2020[0]["bars"]), 0)
        self.assertEqual(years_2020[0]["opening"], 115670.0)
        self.assertEqual(years_2020[0]["closing"], 129004.0)

    def test_a_genuine_reconciling_gap_still_emits_its_own_segment(self):
        """A real gap between one year's closing and the next year's
        opening with no explaining movement row (verified against
        ClearBank's real FY2023/FY2024 figures) must still surface as its
        own segment carrying a "reconciling" bar - the empty-segment fix
        must not also swallow a genuine, non-zero unexplained difference."""
        by_order = {
            1: _row("Balance as at 31 December 2023", **{"Total equity": "100"}),
            2: _row("Balance as at 31 December 2024", **{"Total equity": "150"}),
        }
        components = ["Total equity"]
        segments = curate_equity_waterfall(by_order, components)

        self.assertEqual(len(segments), 1)
        self.assertEqual(segments[0]["year"], "2024")
        buckets = [b["bucket"] for b in segments[0]["bars"]]
        self.assertEqual(buckets, ["reconciling"])
        self.assertEqual(segments[0]["bars"][0]["value"], 50.0)

    def test_a_normal_year_with_real_movements_is_unaffected(self):
        by_order = {
            1: _row("Balance as at 31 December 2023", **{"Retained losses": "0", "Total equity": "100"}),
            2: _row("Profit for the year", **{"Retained losses": "20", "Total equity": "20"}),
            3: _row("Balance as at 31 December 2024", **{"Retained losses": "20", "Total equity": "120"}),
        }
        components = ["Retained losses", "Total equity"]
        segments = curate_equity_waterfall(by_order, components)

        self.assertEqual(len(segments), 1)
        self.assertEqual(segments[0]["opening"], 100.0)
        self.assertEqual(segments[0]["closing"], 120.0)
        self.assertGreater(len(segments[0]["bars"]), 0)

    def test_an_untagged_zero_movement_checkpoint_folds_into_its_neighbour(self):
        """The 2026-09-06 fix above only merges a net-zero checkpoint when
        it trails a genuinely FY-tagged segment. A bank whose movement rows
        never carry an explicit "(FYNNNN)" tag at all (verified against
        Hampshire Trust Bank and ICBC (London) - an IFRS 9 transition
        adjustment applied on the same "1 January" date as the prior
        year's closing) never reaches that merge, so the same-value
        "opening balance" checkpoint used to survive as its own blank
        chart row, and collided with the restated checkpoint that
        immediately followed it on the same date - producing a
        "Jan 2018 (i)"/"Jan 2018 (ii)" pair instead of one real segment."""
        by_order = {
            1: _row("Balance at 31 December 2017", **{"Retained earnings": "100", "Total equity": "100"}),
            2: _row("Balance at 1 January 2018", **{"Retained earnings": "100", "Total equity": "100"}),
            3: _row("Adjustment on initial application of IFRS 9", **{"Retained earnings": "5", "Total equity": "5"}),
            4: _row("Restated balance at 1 January 2018", **{"Retained earnings": "105", "Total equity": "105"}),
            5: _row("Profit for the year", **{"Retained earnings": "20", "Total equity": "20"}),
            6: _row("Balance at 31 December 2018", **{"Retained earnings": "125", "Total equity": "125"}),
        }
        components = ["Retained earnings", "Total equity"]
        segments = curate_equity_waterfall(by_order, components)

        jan_2018 = [s for s in segments if s["year"].startswith("Jan 2018")]
        self.assertEqual(len(jan_2018), 1, "the empty carried-forward checkpoint must not survive as its own row")
        self.assertEqual(jan_2018[0]["year"], "Jan 2018")
        self.assertEqual(jan_2018[0]["opening"], 100.0)
        self.assertEqual(jan_2018[0]["closing"], 105.0)
        self.assertGreater(len(jan_2018[0]["bars"]), 0)

    def test_two_real_same_date_checkpoints_get_their_own_qualifier_not_a_bare_ordinal(self):
        """When two checkpoints genuinely share the same disclosed date and
        BOTH carry real movements (Clydesdale Bank's "Group basis"/
        "restated to Bank-solo basis" entity split; Paragon's "as
        originally reported"/"as restated" pair), the empty-segment fold
        above correctly leaves both in place since neither is empty - the
        collision is real and must be labelled with each checkpoint's own
        disclosed qualifier, not an opaque "(i)"/"(ii)" ordinal."""
        by_order = {
            1: _row("At 30 September 2023 (FY2023 closing)", **{"Total equity": "1000"}),
            2: _row("Profit for the year", **{"Total equity": "50"}),
            3: _row("At 30 September 2024 (FY2024 closing, as originally reported)", **{"Total equity": "1050"}),
            4: _row("Restatement (Note 44)", **{"Total equity": "-20"}),
            5: _row("At 30 September 2024 (FY2024 closing, as restated)", **{"Total equity": "1030"}),
        }
        components = ["Total equity"]
        segments = curate_equity_waterfall(by_order, components)

        sep_2024 = [s for s in segments if s["year"].startswith("Sep 2024")]
        self.assertEqual(len(sep_2024), 2)
        self.assertEqual({s["year"] for s in sep_2024}, {
            "Sep 2024 (as originally reported)", "Sep 2024 (as restated)",
        })


if __name__ == "__main__":
    unittest.main()
