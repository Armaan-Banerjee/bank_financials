# CLAUDE.md

Shared coding rules for both models are in
[CODING_STANDARDS.md](CODING_STANDARDS.md). Read that file before modifying
scripts, databases, exports, or analytical deliverables.

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

Not a software project — a data project. It produces one Excel workbook per UK
PRA-authorised bank, each summarizing five years of financial data sourced from
public Annual Reports and Pillar 3 disclosures. The source list of banks to cover
is `Banks List 2608.xlsx` in the repo root. Finished workbooks live in `banks/`,
named `<BANK> FINANCIALS.xlsx`. There is no git repo here and no dependency
manifest — `openpyxl` is expected to already be installed against `/usr/bin/python3`.

## Commands

Each bank has its own build script; there is no shared entrypoint or test suite.

```bash
python3 scripts/build_barclays.py   # regenerates banks/BARCLAYS FINANCIALS.xlsx
python3 scripts/build_monzo.py
python3 scripts/build_chetwood.py
python3 scripts/build_starling.py
python3 scripts/build_tsb.py
python3 scripts/build_bank_of_london.py
```

Each script hardcodes its own output path via `bw.save(...)` at the bottom, so
running a script always regenerates that one bank's workbook in `banks/`.
There's no way to "run just one sheet" — rerun the whole script.

## Architecture

`scripts/bank_workbook.py` is the shared library all build scripts import
(`from bank_workbook import BankWorkbook`). It defines the `BankWorkbook` class
and the standard workbook shape, enforced the same way for every bank:

- **`Cash Flow Statement`** sheet: full statement, one column per year
  (most-recent-first), rows tagged `SECTION` (divider), `DATA` (line item), or
  `TOTAL` (bolded subtotal).
- One sheet per **Pillar 3 key metric** — the fixed list in
  `PILLAR3_SHEET_NAMES` (CET1 Capital, CET1 Ratio, Tier 1 Capital, Tier 1 Ratio,
  Total Capital, Total Capital Ratio, Total RWAs, Leverage Ratio, LCR, NSFR,
  MREL Ratio) — 12 sheets total per workbook.
- Every sheet ends in a single merged, wrapped **source-citation cell**, not a
  per-row citation column. Citation text always names the exact document, page,
  and table, plus the source URL.
- `header_color` is varied per bank (hex, no `#`) so workbooks are visually
  distinguishable at a glance.

A build script (e.g. `scripts/build_barclays.py`) is a flat, linear data file:
define `YEARS`, define source URL constants and `*_sources()` helper functions
that build citation strings, construct one `BankWorkbook`, call
`add_cash_flow_sheet(...)` once, then call a local `metric(...)` wrapper around
`add_metric_sheet(...)` once per Pillar 3 metric, and finally `bw.save(...)`.
When a metric genuinely isn't disclosed for a bank at all,
`add_not_disclosed_metric_sheets(...)` fills it with a single "Not publicly
disclosed" row instead of a bespoke `metric(...)` call.

Figures are transcribed by hand from primary sources into each script — there's
no API or scraper. Missing years are left as blank dict keys rather than zeros.
Numbers vs. strings are both valid cell values in `rows_data`/`rows` (e.g.
`"82.94%"` or `"Not publicly disclosed"` are written as-is).

## Workflow notes for adding a new bank

- Before sourcing documents, do preliminary research first: confirm the entity
  match against `Banks List 2608.xlsx`, check Companies House filing history,
  and check Pillar 3 archive availability (including Wayback Machine if the
  bank's own site is unreliable). Proactively flag gaps or ambiguities to the
  user before building rather than silently guessing or dropping data.
- One or two source-document workarounds for a bank (an OCR pass, a
  Wayback-archived report, substituting a near-identical legal entity) are
  normal and worth doing. If structural blockers keep stacking on the *same*
  bank (scanned/non-text filings, a source site blocking automated fetches,
  missing years, an entity that legally has no cash flow statement at all —
  e.g. FRS 102's reduced-disclosure exemption for wholly-owned subsidiaries),
  stop and offer the user the option to skip that bank rather than continuing
  to solve around each new blocker.
- New build scripts follow the existing ones' structure exactly (see
  `scripts/build_barclays.py` as the reference implementation) — same
  `metric()` wrapper pattern, same citation-string conventions, same
  `bw.save("/Users/armaan/code/katalysis/banks/<BANK> FINANCIALS.xlsx")` call
  at the end.

## Insights pipeline

Once workbooks exist in `banks/`, a second system in `scripts/insights/`
normalizes them into a SQLite database, clusters banks into peer groups,
extends a cross-bank trend analysis, and builds a client deliverable. It's
a separate, actively-maintained codebase from the one-off `build_<bank>.py`
scripts above — see `scripts/insights/README.md` for how it fits together,
`CODING_STANDARDS.md` for the rules it follows, and
`wayfinder/insights/map.md` for why it exists and what's been decided.
Refresh it with `python3 scripts/insights/refresh_all.py`, never by running
its scripts individually out of order.
