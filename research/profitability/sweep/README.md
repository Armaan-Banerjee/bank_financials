# sweep/ — the 140-bank published-returns sweep

**STATUS 2026-10-15: ALL SEVEN BATCHES COMPLETE AND MERGED.** 140 banks,
379 raw records; batch record counts 64, 50, 42, 59, 53, 47 and 64.

Collection finished 2026-10-13. The merge into the curated store ran
2026-10-15 via `../merge_sweep.py` (199 records added, store 156 → **355
records across 138 banks**), and the deliverable was rebuilt as
`research/UK_banks_profitability_2026-10-15.{csv,xlsx}`.

**The merge is now a tool, not an action.** The 2026-10-11 hand-merge of
batches 1-3 could not be re-run, so the 12-13 October retry corrections
(Metro Bank's RoTE series, Turkish Bank UK's five ROE years, five
`publishes_none` findings) never reached the store and 7 banks sat outside it
for two days; `merge_sweep.py` picked all 16 of those records up on its first
run. It is idempotent and defaults to a dry run, so re-running it after any
batch correction is the normal way to pick that correction up.

The 12–13 October cache-first and primary-source retries closed all 29
formerly unresolved records. The final uploaded-report pass closed
Co-operative Bank, Monument Bank and Goldman Sachs International Bank as
verified exact-report non-disclosures and recovered Philippine National Bank
Europe ROA of -3.5% / 0.1% for FY2025/24. Metro Bank PLC is resolved with its exact
bank-consolidated RoTE series of 5% / (22)% / 7% for FY2025/24/23, and Tandem
Bank Limited is closed as a verified exact-report non-disclosure. Arab Bank
Europe remains settled at the collection level with six exact values/formulas
from the search-indexed text of its own reports, retained conservatively as
`ocr_lead` until the pages can be rendered. The batch files therefore retain
40 `ocr_lead` records: 34 in batch 4 and six in batch 7. Those OCR leads may
not be silently promoted during a later merge.

Combined quality audit of all 379 raw records: `300dpi` 336,
`press_release` 3, `ocr_lead` 40 and null/unresolved 0. The provisional
population is deliberately retained in the batch files and documented in the
corresponding `batch_N_RESUME.md` and dated `unresolved_retry_*` reports
files; it is not eligible for silent promotion.

**Finding, recomputed over the whole merged store on 2026-10-15** (it read
"23 distinct measure labels across 32 banks" while the sweep was one wave in,
and that partial figure stood in this file for four days):

**66 distinct measure labels across 283 published figures, and only 42 of
those 283 are `comparable_with_computed`** — 15%. Seven spellings of "return
on equity" alone ("Return on Equity", "Return on equity", "Return on Equity
(RoE)", "Pre-tax return on equity", "Adjusted return on equity", "Return on
average equity", "Return on average equity - Profit / (loss) before
taxation"), and those are different measures, not just different casing.

That is why this store is one row per published figure with its definition
attached, and never a bank x year grid: a grid would assert these 66 labels
are one measure, and 85% of the figures in it are struck on a definition that
is NOT ours. **72 banks publish at least one return; 70 publish none.**

Full context, method and dispatch brief: `../RESUME_2026-10-10.md`.

| file | what |
|---|---|
| `worklist.json` | all 145 banks, `status` done/todo, candidate URLs |
| `batch_N.json` | 20 banks each (N=1..7), the dispatch input |
| `batch_N.jsonl` | **the output** — append one record per bank-year, checkpointing after EVERY bank |
| `batch_N_RESUME.md` | per-batch source log, verification state and cold-resume handoff |

5 banks are already `done` and excluded from the batches: ALRAYAN BANK,
UNITED TRUST BANK, COUTTS, LLOYDS BANK, ACCESS BANK UK. Their verified
records are in `../published_returns.jsonl`.

## Merge history

| date | what | store after |
|---|---|---|
| 2026-10-11 | batches 1-3, by hand | 156 records / 59 banks |
| 2026-10-15 | all seven batches via `../merge_sweep.py --apply` | **355 records / 138 banks** |

The 2026-10-11 line was recorded here as "157 records across 60 banks". That
count included the store's `_schema` header line, which is a schema note and
not a record — the file held 156 records across 59 banks. Count with a parser
that skips the header; `merge_sweep.py` prints the figure on every run.

**The evidence filter is `merge_sweep.py`, not a convention to re-apply by
hand.** It is a whitelist — only `300dpi` and `press_release` merge, an
unrecognised verification state is refused and named rather than inherited —
de-duplicates on `(bank, year, measure)`, and never overwrites a record
already in the store, because a batch correction to a curated record is a
hand decision.

**Still quarantined after the merge: the 40 `ocr_lead` records.** They stay in
the batch files and are reported by name on every `merge_sweep.py` run. 7
banks are therefore in the sweep but have no store record at all — **Arab Bank
Europe, Bank of Africa UK, British Arab Commercial Bank, EFG Private Bank,
Ghana International Bank, ICBC (London), Secure Trust Bank** — and that is
the honest coverage gap, not a silence. Promoting one means rendering its
cited page at 300 dpi and reading it; the store is `300dpi` 351 /
`press_release` 4 / `ocr_lead` **0**, and the 2026-10-10 backlog clearance
holds only as long as that stays true.
