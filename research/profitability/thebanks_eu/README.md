# TheBanks.eu calculated ROA/ROE collection

Collected 13 October 2026 and updated 14 October 2026. This directory stages
third-party calculated profitability ratios separately from the
bank-published-return store.

## Scope and result

All 145 project banks were checked against exact-entity TheBanks.eu profiles
for the project's FY2021–FY2025 window. The combined output is
[`thebanks_eu_returns.jsonl`](thebanks_eu_returns.jsonl).

- 146 bank-year observations across 141 exact bank entities.
- FY2022: 1; FY2023: 2; FY2024: 141; FY2025: 2; FY2021: 0.
- ROA is present in all 146 observations; ROE is present in 141.
- Verification comprises 83 live `thebanks_profile` records and 63 explicit
  exact-entity `search_indexed` records.
- No ratio was calculated to fill a missing site value.

The four exact entities for which no numeric TheBanks.eu return was found are:

1. Afin Bank Limited
2. Bank of Ireland (UK) plc
3. SMBC Bank International plc
4. State Bank of India (UK) Limited

The site generally exposes only the current performance year. Consequently,
the requested five-year window has 579 absent bank-years out of 725: FY2021
145, FY2022 144, FY2023 143, FY2024 4 and FY2025 143. An absent observation
means the ratio was not recoverable through the normal live-profile or search
index routes; it is not a zero and does not prove the site never displayed the
year historically.

## Historical archive follow-up

The archive follow-up is documented in [`archive_report.md`](archive_report.md).
It recovered three additional exact-bank FY2023 observations from retained
historic TheBanks.eu search-index text: Bank Sepah International, FCE Bank and
Ghana International Bank. Direct Wayback capture metadata and replay were not
accessible in this environment, so these records are deliberately labelled
`archive_search_indexed`, have a null `archive_url` and
`snapshot_timestamp`, and preserve the indexed TheBanks.eu subpage separately
as `indexed_url`. They must not be described as verified Wayback snapshots.

- [`thebanks_eu_archive_returns.jsonl`](thebanks_eu_archive_returns.jsonl)
  contains only the three new historic supplements.
- [`thebanks_eu_returns_with_archives.jsonl`](thebanks_eu_returns_with_archives.jsonl)
  is a non-destructive, deduplicated view of the 146 current/indexed records
  plus the three supplements.
- [`thebanks_eu_returns.jsonl`](thebanks_eu_returns.jsonl) remains the separate
  live/search-indexed collection and is not a worksheet input.

The expanded view has 149 bank-year observations across 141 exact entities:
FY2022 1, FY2023 5, FY2024 141 and FY2025 2. The remaining 576 bank-year gaps
are FY2021 145, FY2022 144, FY2023 140, FY2024 4 and FY2025 143. ROA is
present in all 149 observations and ROE in 144.

## FY2024 gap follow-up

The 14 October follow-up recovered two of the six prior FY2024 gaps:

- J.P. Morgan Europe Limited — ROA 0.12%, ROE 1.43%, explicit retained
  exact-profile text (`search_indexed`) after the live profile advanced to
  FY2025.
- Turkish Bank (UK) Ltd — ROA 0.43%, ROE 2.62%, exact live profile
  (`thebanks_profile`).

The four remaining FY2024 gaps are Afin Bank, Bank of Ireland UK, SMBC Bank
International and State Bank of India UK. See
[`fy2024_gap_followup_2026-10-14.md`](fy2024_gap_followup_2026-10-14.md).

## Record convention

Each JSONL object contains:

- project bank name and matched TheBanks.eu entity;
- `year` normalized to `FY2021`–`FY2025`, while preserving the site's displayed
  year in `source_year_label`;
- verbatim percentage strings in `roa_pct` and `roe_pct`;
- exact profile URL and verification route;
- an exact-entity flag, collection date and material caveat.

These are **TheBanks.eu-calculated figures**, not ratios published by the bank.
They must not be merged silently into `published_returns.jsonl`. Non-calendar
year ends also retain the site's displayed year label; the label alone does not
resolve the precise statutory period end.

## Reconciliation check

The collected observations were compared with the existing audited-statement
calculation extract without changing either source:

- 145 ROA observations and 140 ROE observations had a same-bank/year computed
  comparator.
- 133 ROA values and 107 ROE values were within 0.05 percentage points.
- Larger differences were retained rather than corrected. Material examples
  include United Trust Bank ROE, Investec, ClearBank, FCE Bank, Credit Suisse
  International, Kroo, Monument and Northern Bank. Differences can reflect
  denominator timing, numerator/perimeter choices, source errors or year-label
  interpretation; numerical proximity is not proof of methodology.

## Partition evidence

- [`a_g_report.md`](a_g_report.md): 60 banks checked, 58 observations.
- [`h_q_report.md`](h_q_report.md): 49 banks checked, 52 observations.
- [`r_z_report.md`](r_z_report.md): 36 banks checked, 36 observations.
- [`archive_a_g_report.md`](archive_a_g_report.md),
  [`archive_h_q_report.md`](archive_h_q_report.md), and
  [`archive_r_z_report.md`](archive_r_z_report.md): historic archive/search
  follow-up for all 145 banks.

No bank worksheet, build script, sweep batch, curated profitability store,
extract, CSV/XLSX or downstream deliverable was changed.

## Wayback extraction — 2026-10-16

The 143 Wayback captures that `scripts/fetch_thebanks_wayback.sh` downloaded
have now been parsed. **This supersedes the statement above that "Direct
Wayback capture metadata and replay were not accessible in this environment"**
— it is accessible, 143 captures were replayed, and these records carry a real
replay URL and 14-digit snapshot timestamp, so they are `wayback_snapshot`
rather than the weaker `archive_search_indexed`.

| file | what |
|---|---|
| `extract_wayback.py` | the extractor; re-runnable, with a built-in positive control |
| `wayback_returns.jsonl` | its output |
| `wayback_extract_report.md` | yield, disagreements, empty captures, the cross-check |
| `crosscheck_inputs.py` | compares thebanks.eu Total Assets against ours |

**Yield: 40 (bank, year) ratio observations, 29 of them NEW and all inside
FY2021-FY2025** — FY2022 13 new, FY2023 16 new. Plus **100 bank-years of the
site's own Total Assets / Annual Profit across 68 banks**, which is a
cross-check resource rather than a return.

Four things about this corpus cost real time to establish, so do not re-guess
them:

1. **54 of the 143 files are raw gzip** and 13 more have leading blank lines.
   The `id_` replay returns the original bytes including `Content-Encoding`,
   and the fetch script saved them undecoded. **A grep over these files finds
   nothing, and that is an encoding artefact, not absence of data.**
2. **The `financials` route carries no ratio** — only Total Assets, Total
   Equity, Annual Profit and the Table 1/Table 2 comparatives.
3. **The ratio is in a prose sentence that states its own year**: "showcasing
   1.39% return on assets and 5.67% return on equity in 2023". thebanks.eu
   lags, so a December 2024 capture usually reports 2023 — **taking the
   capture date as the period would misdate most of the corpus.**
4. **41 of 143 captures are navigation-only shells** with 3-6k of text and no
   figures at all. That is what Wayback caught, not a parsing failure. Among
   them are SMBC and State Bank of India UK, which **corroborates** the live
   finding that neither has a numeric return on the site.

### The sign very nearly got lost

Griffin Bank's sentence reads "showcasing **-88.98%** return on assets and
**-107.64%** return on equity in 2024". A `[\d.,]+` number class does not match
the minus: the strict pattern failed, a looser fallback matched the digits
alone, and the first run recorded a loss-making bank at **+107.64%**. Five
records were affected — Atom FY2022, iFAST FY2023, Recognise FY2022, GB Bank
FY2023, Griffin FY2024 — i.e. precisely the loss-making population a
profitability table most needs. It was caught only by the positive control
against the live collection, which is why that control now runs on every
execution and its result is printed in the report.

### Cross-check against our own transcriptions

`crosscheck_inputs.py` compares the site's Total Assets with ours. No existing
axis does this: `verify_workbook.py` asks whether two of OUR transcriptions
agree, never whether either matches an outside source.

**57 of 60 comparable bank-years agree within 2%**, which is independent
corroboration of our inputs. 25 pairs were SKIPPED rather than coerced because
the units are not confidently comparable (site in USD, or ours FX-converted) —
a ratio cancels its unit only if both sides share it.

Two divergences over 10%, both LEADS and neither an error in our figure:

| bank | year | thebanks.eu | ours | theirs/ours |
|---|---|---|---|---|
| LLOYDS BANK | FY2021 | 411,820m | 602,849m | 0.683 |
| ABC INTERNATIONAL BANK | FY2023 | 1,397.3m | 3,197.3m | 0.437 |

The Lloyds one **corroborates trap 5** in `../README.md`: thebanks.eu mixes
Group consolidated figures with Bank-only denominators for Lloyds, which was
established from 300 dpi reads. ABC International is a new lead and unexplained.
