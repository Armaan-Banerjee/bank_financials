# Profitability sheet rollout — COMPLETE (2026-10-26)

All steps below are closed. Kept as the record of what was done and why.

Written so a session that is killed mid-rollout can resume without re-deriving
anything. Update it as steps close; do not delete it until the rollout is done.

## What exists now (all on disk, all verified)

- **`scripts/profitability_rows.py`** — the shared row resolver, extracted
  verbatim from `research/build_profitability_table.py`. The research extract
  was regenerated after the move and is **byte-identical** (`cmp` passed), so
  the move changed no figure.
- **`scripts/profitability_fx_basis.py`** — the audited FX basis table.
  **29 banks: 16 fully mixed, 2 partly mixed (FIRSTBANK UK FY2019–FY2021,
  ZENITH FY2014–FY2025), 11 clean.** Plus `ENTITY_MISMATCH` (2) and
  `OTHER_FINDINGS` (4). Keyed on the **workbook key** (filename minus
  " FINANCIALS.xlsx"), the same identifier `published_returns.jsonl` uses.
  It was first keyed on each bank's display `bank_name` and **26 of the 29
  then matched nothing** — the display name is not an identifier.
- **`scripts/bank_workbook.py`** — `add_profitability_sheet()`, plus module
  helpers `_read_published_returns`, `_profitability_note`,
  `_profitability_sources`, `_widest_spread`, and the constants
  `PROFITABILITY_SHEET_NAME`, `REFUSED_MIXED_BASIS`. Also `_sheet_units`,
  recorded in `_add_statement_sheet`.
- **`scripts/build_monzo.py`** — rewired onto the library call. Its hand-built
  pilot grid and the library-built grid are **identical cell for cell**
  (positive control passed). Monzo keeps two bank-specific paragraphs as
  `extra_note`: the MBHG/MBL reporting-entity break and the thebanks.eu FY2024
  disagreement.
- **`scripts/verify_workbook.py`** — `has_profitability` derived from the sheet
  list, never asserted, so workbooks without the sheet still verify.

## Dry run, all 145 banks, real library call, nothing written

Harness: `dryrun2.py` in the session scratchpad (re-creatable — it stubs
`BankWorkbook.save`, runs each build script with `runpy`, then calls
`add_profitability_sheet(key)` on the captured workbook).

**144/145 build a sheet. 1 raises: CITIBANK UK.**
Across the 144: **3,958 computed per-cent cells, 648 "Not computed"
refusals, 784 "Not published", 1,174 blank.**

CITIBANK UK's own Statement of Financial Position prints **no total-equity
line** — it presents equity inside Total liabilities, which its own ENTITY
NOTE states. Its Statement of Changes in Equity still closes to a published
total every year (FY2019 362,624; FY2020 404,330; FY2021 378,126 £'000).
Handled by the guarded `equity_series` / `equity_series_source` override:
the override raises without provenance, and the provenance is printed in the
sheet's source cell.

## Design decisions already settled (do not relitigate)

1. **The FX verdict is looked up, never inferred.** Three detection routes
   were tried and all three fail — see the file header. In particular the
   "unit says conv." shortcut catches only **13 of the 18** contaminated
   banks: BANK MANDIRI EUROPE, CREDIT SUISSE INTERNATIONAL, FCMB UK,
   GOLDMAN SACHS INTERNATIONAL BANK and JP MORGAN SECURITIES print a plain
   unit and would have computed silently on two different rates.
2. **A contaminated year is refused, not caveated** (user's choice,
   2026-10-26: "Refuse to compute, state why"). The cell says
   `"Not computed"` — short, because a data cell is ~21 chars and Excel clips;
   the reason is a paragraph in the note, which auto-fits.
3. **Entity mismatch refuses too** (KUWAIT FINANCE HOUSE, STANDARD CHARTERED
   BANK): the units cancel perfectly and the ratio still divides GROUP profit
   by a SOLO balance sheet. No unit test can see this.
4. **The own-published rows print only own-edition figures.** 166 of 325
   measure records are a later edition's comparative; those go in the note,
   never in the year's cell.
5. **The note is generated, not hand-written per bank** — 145 hand-written
   notes drift from the figures beside them.
6. **Placement**: after `Asset Quality`, BEFORE `KM1 Key Metrics`. The
   KM1→CET1 Capital adjacency is locked.

## Steps completed

- [x] **Non-12-month periods** settled. Three subagents audited the 30
      candidate scripts; every cited line was then checked against the script
      itself. **19 bank-years across 18 banks**, recorded in
      `NON_ANNUAL_PERIODS`. Eleven of the 30 candidates have no affected
      column, mostly because the irregular period sits below the workbook's
      floor and was deliberately excluded from the year grid. The **year label
      finds only 2 of the 19** (Aldermore alone encodes it), so that is not a
      detector either. User's decision: **print the ratio, state the period** —
      it is exact arithmetic on two published figures and only the
      interpretation is wrong, and annualising would invent a figure the bank
      never published. Two cases run the OTHER way and are flagged as
      understatements: Handelsbanken FY2018 (one month of trading against a
      full balance sheet) and Triodos FY2019 (eight months). KINGDOM BANK
      FY2004 is excluded from the table because that column has no profit and
      loss at all, so there is no numerator to distort.
- [x] Call inserted into all 144 remaining scripts. Monzo FY2024 gained the
      13-month note it had been missing — the audit caught that gap in the
      hand-written pilot note.
- [x] All 145 rebuilt, 0 failures. **All six axes clean**:
      `verify_workbook` 0 shape complaints across 145; `check_builds_current`
      clean; `check_overview_ties` **A=2 / B=0 / C=0 at reach 14,648** (exact
      baseline); `check_cell_fit` 0 clipped; `check_ratio_ties` unchanged
      population. Sheet sits at index 6 in all 145, between Asset Quality and
      KM1, verified.
      **`audit_gaps.py` enumerates a fixed sheet list that does not include
      `Profitability`, and that file is untouched by standing constraint — so
      the census does not see this sheet, and no Profitability count here is a
      census figure.**
- [x] **Positive control**: workbook sheets vs the research extract —
      **2,352 cells agree exactly, 0 regressions.** Separately, 16 cells where
      the workbook computes and the extract is blank: the extract's window
      starts FY2021 so it has no opening balance for that year, while the
      workbook carries FY2020. A window limit, not a defect.
- [x] **Deliverable fixed.** `research/UK_banks_profitability_2026-10-26.xlsx`
      cut as a new dated edition (each edition is kept; 10-22 left in place and
      marked superseded in the README). The table builder now IMPORTS the
      basis verdict instead of gating on `units_agree`. Measured two
      independent ways, both agreeing: **20 banks, 96 bank-years, 384 cells
      now read `Not computed`, of which 360 printed a number in the 2026-10-22
      edition.** My earlier estimate from the unit string — 15 banks / 73
      bank-years / 284 cells — under-counted by 5 banks and 76 cells.
- [x] Memory updated: new `project_profitability_sheet_rollout`, and
      `project_fx_conversion_convention` corrected (the J.P. Morgan Securities
      claim was stale from 2026-10-09, and the `stock()`-only heuristic is
      unsound — five different helper-naming schemes, plus one bank that
      converts with no helper at all).

## Still open (not part of this rollout)

- NATIONAL BANK OF KUWAIT INTERNATIONAL changes presentation currency
  USD→GBP at FY2023/FY2024 with an empty `unit_suffix`, so no column header
  carries a currency marker. Each year's ratio is sound; comparing levels
  across that boundary is not, and nothing on the sheet warns.
- PERSIA INTERNATIONAL BANK FY2015/FY2016 labelling defects: the Balance Sheet
  passes raw EUR through while its header claims GBP, and the P&L subtitle's
  claim that those years are "EUR '000 shown" is false for that sheet.
- BANK SEPAH INTERNATIONAL has two total-assets rows; a lookup on the plain
  label silently drops FY2026.
- [ ] Carried over, unrelated to this rollout: ARAB BANK EUROPE FY2025 remains
      a lead; RCI BANK UK FY2025 opex moved −298,114 → −433,225; whether
      ROE/ROA should land in the insights deliverable.

## Retraction recorded

Earlier this session I reported CREDIT SUISSE INTERNATIONAL and GULF
INTERNATIONAL BANK UK as "CANCELS". **Both are MIXED RATE.** The grep-based
detector read their row literals, and both scripts apply the stock/flow
wrappers in a comprehension over the whole row list, so the literal looks raw.
