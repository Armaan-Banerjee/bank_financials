# Profitability sheet — 145-bank rollout reconnaissance (2026-10-26)

Monzo's pilot sheet works. This records what a corpus-wide rollout has to
solve, measured rather than assumed, BEFORE any of the 144 other scripts is
touched.

## 1. Row labels vary; the repo already solved this

Resolving "profit after tax", "total equity", "total assets" by a hand-written
regex found equity in 119/145 and profit in only 66/145. That is a measure of
my regex, not of the corpus.

`research/build_profitability_table.py` already carries mature, rank-ordered
pattern tables (`PROFIT_PATTERNS`/`PROFIT_EXCLUDE`, `EQUITY_PATTERNS`,
`ASSET_PATTERNS`) that resolved all 145, with the reasoning written down —
losses are first-class, "before tax" is excluded outright, "total
comprehensive income" deliberately is NOT. **The rollout must call that code,
not restate it.** `_detail_rows` in `BankWorkbook` already holds every
statement sheet's rows by normalised label, so the sheet can derive with no
per-script data at all — one call line per build script.

## 2. The FX problem, and why source inspection cannot settle it

29 workbooks involve a non-GBP currency. The convention
(`project_fx_conversion_convention`) is **stocks at year-end SPOT, flows at
that year's AVERAGE**. Where a script applies it to the primary statements,
the balance sheet is converted at spot and the P&L at average — so a ratio
struck across them **does not cancel its unit**. Both sides are labelled
£'000, so nothing on the page shows it.

I wrote a detector that looked for `stock()` on the balance-sheet rows and
`flow()` on the P&L rows. **It was wrong in both directions** and must not be
trusted:

| bank | detector said | actually |
|---|---|---|
| Credit Suisse International | MIXED RATE | raw literals both sides — **fine** |
| Gulf International Bank UK | needs checking | raw US$ both sides — **fine** |
| J.P. Morgan Securities | MIXED RATE | `Total equity` IS `stock()`-wrapped — **confirm the P&L** |
| Goldman Sachs International Bank | MIXED RATE | label format differs; **unverified** |
| 6 others | "cancels" | **false negative** — their row lists are named `bs_rows`/`pl_rows`/etc., so the block was never found at all |

The failure mode is the documented one: a hand-rolled classifier over source
text, trusted without a positive control. Scripts name their row lists
differently, `stock(`/`flow(` appear on unrelated rows inside the same block,
and a missing match reads as a clean bill of health.

**Consequence for the design:** unit-consistency cannot be proven
mechanically from the scripts. The sheet must therefore compute only where
the two sheets' own recorded unit strings match, and every FX bank must be
settled **one at a time by reading its script**, recorded in an explicit
table in the manner of `OVERVIEW_SPEC` — explicit, not inferred, for exactly
the reason that table gives.

## 3. This is not only a rollout problem — it is live in the deliverable

`research/UK_banks_profitability_2026-10-22.{csv,xlsx}` computes ROE/ROA from
these same workbook rows, so wherever a bank's statements are converted on
mixed bases, **the deliverable's ratio already carries the error**. It
publishes ratios for all four banks above. For a bank whose numerator is at
the average rate and denominator at spot, the figure is wrong by the
spot/average spread — FY2025 is 1.3448 vs 1.3193, about **1.9% relative**:
Credit Suisse International's FY2025 3.27% would be ~3.33% struck
consistently. Small, systematic, and invisible to every existing check axis.

This is a finding about work already delivered, not a blocker the rollout
introduced. It needs settling on its own terms.

## 4. What the per-bank note cannot be

Monzo's note carries facts that are Monzo's alone: the `publishes_none`
evidence, the MBHG/MBL reporting-entity break, the structural FY2018 blank,
and the thebanks.eu FY2024 disagreement. None of that generalises.

**75 of 145 banks publish a return of their own**, and those published
figures are not interchangeable: Secure Trust prints four different
return-on-equity measures, BACB's "return on initial invested capital" is not
ROE at all, Weatherbys' is struck pre-tax and its definition changed between
editions. 399 records in `published_returns.jsonl` carry each bank's own
measure, definition, entity and verification state — the own-published row
and its caveat must be driven from that store per bank, not written once.

## Recommended shape

1. `add_profitability_sheet()` in `bank_workbook.py`, deriving from
   `_detail_rows`, calling the research module's pattern tables.
2. Own-published row and caveats driven from `published_returns.jsonl`.
3. An explicit FX table; compute only on matched units, otherwise print the
   reason — "a ratio cancels its unit only if both sides share it; skip
   rather than coerce".
4. A dry-run audit reporting, per bank, what resolved and what did not,
   reviewed BEFORE any workbook is written.
5. Positive control per bank against the research deliverable for
   FY2021-FY2025, as the Monzo pilot had (20 agree / 0 differ).
