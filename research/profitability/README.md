# Profitability (ROE / ROA)

## How to rebuild

```bash
/usr/bin/python3 research/build_profitability_table.py research/profitability/extract_$(date +%Y-%m-%d).json
/usr/bin/python3 research/build_profitability_workbook.py \
    research/profitability/extract_$(date +%Y-%m-%d).json \
    research/profitability/agent_findings/thebanks_eu.jsonl \
    "research/UK_banks_profitability_$(date +%Y-%m-%d)"
```

The command is unchanged, but **since 2026-10-22 the build also reads
`thebanks_eu/thebanks_eu_returns_with_archives.jsonl` and
`thebanks_eu/wayback_returns.jsonl` automatically**, and prints every
aggregator source it opened. Until then only the file named on the command
line was read, so the aggregator column carried 20 bank-years while 178 sat
on disk. Extra aggregator files can still be passed as additional arguments.

`build_profitability_table.py` reads `banks/*.xlsx` and **writes no workbook**.
Nothing in this directory ever modifies a delivered bank workbook.

Current deliverable: `research/UK_banks_profitability_2026-10-22.{csv,xlsx}`,
14 sheets, 145 banks x FY2021-FY2025 = 725 bank-years.

**What changed on 2026-10-22, and what deliberately did not.** Every collected
aggregator source is now wired in: the column went **20 → 178 bank-years**,
FY2022 and FY2023 are no longer empty, FY2024 runs to 141 banks, and five
banks that were lost to a name mismatch (Hampshire Trust, HSBC UK, National
Westminster, OakNorth, Santander) are present. Three columns were APPENDED —
`aggregator_verification`, `aggregator_source`, `aggregator_disagreement` —
because the four evidence states behind those values are not equally strong
and the state has to travel with the figure. **No computed, own-published or
desk-research value changed**: the regenerated extract is byte-identical to
the previous one, and a column-by-column diff of the CSV shows the only
changed pre-existing columns are the three aggregator ones.

**Promoting a lead is its own tool, and it is not optional.** An `ocr_lead`
is a figure located in a text layer that NOBODY HAS SEEN, so `merge_sweep.py`
quarantines it. `promote_leads.py --fetch` fetches each cited document, proves
it is a PDF by its magic bytes, renders the cited page at 300 dpi and reports
what to look at; a human or vision-capable model then reads the render and the
confirmed records are merged like any batch.

```bash
/usr/bin/python3 research/profitability/promote_leads.py --fetch --outdir <scratch>
```

Run on 2026-10-22 against the 40 quarantined leads (9 banks): 33 confirmed,
**9 records found that no lead held**, **2 refuted**, 2 still leads, 1
excluded — 44 merged. Store **355 → 399 records, 138 → 145 banks**; the
deliverable's own-published column **181 → 205 bank-years across 75 banks**,
every cell `300dpi` or `press_release`. Full account, including the two cases
where the lead was materially wrong (EFG's measure is over AUM, not assets;
Hampshire Trust publishes a Bank column the lead missed entirely), is in
`lead_promotion_2026-10-22.md`. The original leads STAY quarantined in batches
1-7 on purpose: where the render disagreed with the lead, that disagreement is
the finding.

**Merging the sweep into the store is a third step, and it is a tool:**

```bash
/usr/bin/python3 research/profitability/merge_sweep.py          # dry run
/usr/bin/python3 research/profitability/merge_sweep.py --apply  # write
```

Run it after ANY correction to a `sweep/batch_*.jsonl`, then rebuild. It is
idempotent, so running it when nothing has changed is free and reports
"nothing to add". The 2026-10-11 merge was done by hand and could not be
re-run, which is exactly how 16 corrected records from the 12-13 October
retry rounds — Metro Bank's RoTE series among them — sat outside the store
for two days.

**The extract is a positive control, so re-run it rather than reusing one.**
On 2026-10-15 `extract_2026-10-15.json` came out byte-identical to
`extract_2026-10-11.json`, which is what confirmed that merging 199 published
records changed nothing on the computed side — the two must stay independent.

## Current frontier (2026-10-11)

The first three published-return sweep batches are complete at the bank level:
**60/60 banks, 157 raw records**. Of those, **140 new records met the curated
store's evidence threshold** (`300dpi` or an explicit official
`press_release`) and were merged into `published_returns.jsonl`. Combined with
the earlier work, the curated store now contains **156 records across 59
banks: 154 verified at 300 dpi and 2 official press-release exclusions**.

The remaining **17 provisional records** stay only in the batch JSONL files:
8 `ocr_lead` figures in batch 3 and 9 null-verification/unresolved records
across batches 1-3. They are leads, not findings, and are deliberately absent
from the client workbook. See the three `batch_N_RESUME.md` files for the exact
banks and source obstacles.

Next corpus work is batches 4-7 (80 banks), followed by clearing the remaining
verification backlog where primary documents become renderable.

## The two user decisions this directory is built around (2026-10-10)

**1. The denominator is the AVERAGE.** For ROA as well as ROE. The headline
columns are `roe_pct_avg_equity` and `roa_pct_avg_assets`.

The year-end variants are KEPT, in their own columns and their own sheets, for
two reasons that are not about preference. A bank's oldest reported year has no
prior-year balance sheet, so year-end is the only figure available there —
which is the whole of the coverage difference (ROE 648 average vs 703 year-end;
ROA 653 vs 708). And an outside figure that reproduces on one basis and not the
other is how a divergence gets **explained** rather than merely reported:
thebanks.eu's United Trust ROA of 1.79% reproduces on average assets (1.789%)
and not on year-end (1.681%), which is what identified their basis.

**2. Use the bank's own published figure where there is one.**
`published_returns.jsonl` is that store, and the deliverable's **Own published
returns** sheet is where it surfaces.

## Why the bank's own figure gets its own sheet and not a column

Because it is the most authoritative source and the least comparable one. A
published return is struck on that bank's own definition, and those genuinely
differ:

- **Al Rayan** — "Return on equity" is *profit for the year BEFORE TAX over
  average equity*, stated outright in its KPI table. Its 11.40% for FY2024 and
  our 8.61% differ by exactly the tax charge over average equity (2.795pp).
  Neither is wrong; the label omits "before tax".
- **United Trust Bank** — "Return on Equity is calculated net of the coupon
  paid on contingent convertible securities", on average equity.

So these figures cannot be ranked against each other or against ours without
reading each definition, and a grid would assert they are one measure. One row
per published figure, with its definition, its entity and its verification
state beside it.

Three record kinds, all of them findings:

| kind | meaning |
|---|---|
| a figure | the bank publishes this, on this definition |
| `publishes_none` | the bank publishes **no** return at all — so the computed figure is the only one there is. A positive finding, not a failed search. Lloyds Bank plc is one: full-text search of its 2024 and 2025 ARAs returns zero genuine hits, and returns KPIs are published only by Lloyds Banking **Group** plc, a different perimeter. |
| `excluded` | an outside figure identified as belonging to a **different entity**, recorded so nobody re-derives it. Aldermore's 7.7% is Aldermore Group plc consolidated, not Aldermore Bank plc solo. Coutts' 21.7% is NatWest Group's Private Banking & Wealth Management *segment*. |

**`verification` is load-bearing.** `300dpi` means confirmed on a render at
this project's standard resolution. `ocr_lead` means read off a text layer or a
low-resolution contact sheet and **not** confirmed — a lead, not a finding, and
it must not be presented as one. `press_release` means exactly that.

**The OCR backlog was cleared on 2026-10-10: every figure in the store is now
`300dpi`, and each is taken from its own year's edition except where
`own_edition` says otherwise.** Nine figures were verified in that pass, and it
produced three things the leads did not have:

- **Coutts' footnote (1), previously unread, turns out to state OUR
  definition**: *"RoE is calculated using annual profit for the period divided
  by the average owner's equity, which at 31 December 2025 was £1.5 billion
  (2024 — £1.5 billion)."* That makes Coutts the one bank so far whose
  published figure IS directly comparable with the computed column — 17.3%
  against our 17.03%, where 259/0.173 implies £1,497m against their stated
  "£1.5 billion", so the residual is denominator precision and the composition
  of "owner's equity", not a difference of basis. The store carries a
  `comparable_with_computed` flag for exactly this.
- **Al Rayan's definition is now the bank's own words, not an inference.** The
  FY2025 KPI table states the basis in a column of its own: *"The ratio of
  profit for the year (before tax) to average equity, expressed as a
  percentage."*
- **A year nobody had recorded**: United Trust FY2019 = 16.2%, printed as the
  FY2020 edition's comparative. Outside the FY2021–FY2025 window, so it does
  not reach the deliverable's grid, but it is in the store.

All six United Trust years were confirmed from **their own editions**, not from
one page of comparatives — the own-edition rule applies to a published ratio
exactly as it does to a transcribed figure. The footnote wording is identical
in all six, and the page itself names "UNITED TRUST BANK LIMITED", which is
what rules out the group.

## Four sources, four columns, never merged

Computed / the bank's own / prior desk research / aggregator. These are
different claims about the world and averaging them, or letting one silently
fill in for another, destroys the only thing that makes a disagreement visible.

**`desk_research_*` was called `published_*` until 2026-10-10.** That rename is
substantive. The column holds third-party desk research of unknown derivation,
and calling it "published" invited exactly the confusion that let its
**transposed United Trust Bank years** stand: its "FY2023 = 20.20" is UTB's own
published FY2021, and its "FY2021 = 23.90" is the published FY2023.

## Traps already paid for — do not reintroduce

1. **Matching only `profit|surplus` dropped every loss-making bank** — Afin,
   Chetwood, Kroo, Monument, Oxbury, Griffin, The Bank of London, This Bank.
   That is precisely the population a profitability table most needs to show. A
   loss is a valid numerator and a negative return is a real figure.
2. **Taking the first row containing a year locked onto the SUBTITLE.**
   Recognise Bank's opens "FY2025-FY2026 ...", so column 0 (the label column)
   was treated as data. Header detection now SCORES candidates and never
   accepts column 0. In a different layout this would have mis-assigned figures
   to the wrong year **silently**.
3. **Rank ties must break on year coverage.** Bank Sepah prints both "Total
   assets" and "Total assets (FY2026 presentation)"; the latter canonicalises
   identically and holds one figure, and taking it cost all five ROA years.
4. **A ratio cancels its unit only if both sides share it** — reported, never
   silently divided through. Related and live: **JP Morgan Securities reports in
   USD**, and its script converts stock figures at spot and flow figures at
   average. The 2026-10-08 extract predates that conversion and read JPMS in
   **USD**, so the 2026-10-08 deliverable is wrong for that bank; the
   2026-10-10 extract is correct. Re-running the extract after any FX change is
   not optional.
5. **A combination that reproduces an outside figure to 0.02pp is a
   HYPOTHESIS, not a finding, until a document confirms it.** The Definition
   resolver matched Lloyds as "total comprehensive income / average equity =
   7.13 vs their 7.11" and that was a **coincidence**. The real cause, verified
   on 300 dpi images: thebanks.eu mixes bases within one ratio — Group
   consolidated profit (3,486) over Bank-only unconsolidated denominators, and
   its 2023 equity comparative is Bank-only *shareholders'* equity, a third
   definition. Both reproduce exactly. Ours are right; theirs is a cross-basis
   artefact.

## Known limits

- **RoTE and any tangible-equity measure cannot be tested** — intangibles are
  not extracted. Metro's -23.00 RoTE and Shawbrook's Underlying RoTE are
  "explained by label" only; the arithmetic has not been reproduced.
- **CITIBANK UK** is the one bank with an unmatched input: its balance sheet
  carries no separate equity line. Genuine and known.
- **Starling has a 31 March year-end**, so an outside figure labelled "2024" is
  ambiguous as to period.

## Open leads

**UTB FY2024, thebanks.eu 40.59%** — unresolved, and three hypotheses are now
dead. Their ROA 1.79% reproduces as profit / average assets, and their stated
total-asset growth of 13.75% matches UTB **Limited**'s entity assets exactly
(3,913,260/3,440,168), so they are on the right entity with the right
numerator. But 65,772/0.4059 implies equity of 162,040, which matches nothing:
not UTB Ltd equity (362,862), not ex-AT1 (346,011), and **not the group** — UTB
Partners Plc consolidated total capital and reserves is 365,019.

**UTB's own published FY2024 ROE is 20.1%** (verified 300 dpi, 2026-10-10),
which settles that the bank does not recognise 40.59% on any basis it states.

Narrowed on 2026-10-10 against UTB's full equity series — FY2020 174,036,
FY2021 195,632, FY2022 239,109, FY2023 299,799, FY2024 362,862: the implied
162,040 lies **below every year in the window**, and below the FY2020 figure
by 12.0k. So if it is a UTB Ltd equity figure at all it is **FY2019 or
earlier** — a denominator at least five years stale against a FY2024
numerator. It is also not the ex-AT1 FY2020 base (157,185). The remaining
candidate worth one check is UTB's FY2019 total capital and reserves, which
this workbook does not carry; an average of FY2019 and FY2020 equal to 162,040
would imply FY2019 = 150,044. **That is an arithmetic observation, not a
hypothesis with evidence behind it** — see trap 5 above.

**NORTHERN BANK FY2024** — our inputs are confirmed digit-for-digit at 300 dpi
(company R0000568, unconsolidated, printed p.129: profit 165,495, equity
943,995/929,341, assets 14,474,391, AT1 226,526). Their 19.80/1.32 is still
unexplained, and the AT1 theory is **disproved**: their leverage multiple
(ROE/ROA = 15.00) nearly matches ours (15.45), while excluding the AT1 would
give a multiple of 20.4. Also: the desk-research 19.8 and thebanks.eu's 19.80
are the SAME source, not two.

**COLLECTED. The sweep is done** — all 140 remaining banks, finished
2026-10-13 and merged 2026-10-15. The store holds **355 records across 138
banks**: 283 published figures, 70 `publishes_none`, 2 `excluded`;
verification `300dpi` 351 / `press_release` 4 / `ocr_lead` 0.

Two results worth carrying forward, because both overturn something this file
previously assumed:

- **"Most small banks do not" was wrong.** 72 banks publish at least one
  return against 70 that publish none — an even split, not a long tail of
  silence.
- **66 distinct measure labels across 283 figures, and only 42 are
  `comparable_with_computed`** (15%). Seven spellings of "return on equity"
  alone, and they are different measures rather than different casing. The
  one-row-per-figure design is now backed by the full corpus.

**7 banks have no store record at all**, and this is the honest gap: Arab
Bank Europe, Bank of Africa UK, British Arab Commercial Bank, EFG Private
Bank, Ghana International Bank, ICBC (London), Secure Trust Bank. Their 40
records sit quarantined in the batch files as `ocr_lead` — read off
search-indexed text, never rendered. Promoting one means rendering its cited
page at 300 dpi and reading it.

Aldermore Bank plc solo remains the nearest open case on definitions — only
the group figure is identified, at press-release level, so its own annual
report page and definition are still to pull.

**Navigation recipe for the sweep**, worked out on the United Trust reports and
worth reusing: these filings are scans with **no text layer at all**
(`pdftotext` returns zero bytes), so grepping finds nothing and it is easy to
mistake that for "the bank publishes none". Render candidate pages at 150 dpi,
OCR them with `tesseract` purely to locate the KPI page, then render that one
page at 300 dpi and read it. The KPI page sat at PDF page 3 or 4 in all six
editions. OCR for navigation, images for the figure — never the other way
round.

## Check-axis gap this work exposed

`verify_workbook.py` reconciles DATA blocks to TOTAL rows on the **Cash Flow
sheet only**. It never sums the Balance Sheet or P&L, so a wrong subtotal there
passes silently — as Aldermore's FY2025 Total liabilities did (17,050.8 against
a printed 19,103.6, an eye-skip to the adjacent Customers' accounts line at
17,047.6). That one was found here incidentally and **has since been corrected**
in `scripts/build_aldermore.py`, with the correction documented in the sheet's
source note. The axis gap itself is still open and worth a GA- ticket.

## Files

| file | what it is |
|---|---|
| `published_returns.jsonl` | **curated**: what the banks themselves publish. 355 records / 138 banks. Line 1 is a `_schema` note, NOT a record — a count that includes it is one too high, which is how "157 records across 60 banks" got into `sweep/README.md` for a file holding 156 across 59. Append-only; `merge_sweep.py` is the only thing that should append. |
| `coverage_ceiling.py` / `coverage_ceiling_<date>.md` | **what we can actually get**, per year, per source — as opposed to what is wired into the deliverable. The two diverge sharply: the aggregator column carries 20 bank-years while 179 are on disk. Also names the 14 bank-years NO source can reach. |
| `gap_report.py` / `gaps_<date>.md` | the inverse view: what is missing from the deliverable, each gap classified by cause so the structural ones are not mistaken for chaseable ones. |
| `merge_sweep.py` | the merge tool: sweep batches → curated store. Dry run by default, `--apply` to write, idempotent, and it backs the store up to `.bak` before writing. Encodes the evidence filter (only `300dpi`/`press_release` merge; `ocr_lead` is quarantined and named; an unrecognised state is refused, not inherited) so the filter is code rather than a convention a later session has to guess at. |
| `verification_2026-10-10.md` | the 300 dpi pass that cleared the OCR backlog: every page cited, the three findings it produced, and the scan-navigation recipe. Renders are deliberately not committed — the citation is the record. |
| `extract_2026-10-10.json` | the extraction feeding the current deliverable |
| `agent_findings/` | raw per-figure checkpoints from the 2026-10-08 subagents, kept as provenance. **These were recovered from the scratchpad on 2026-10-10** — they were the only copy of primary-source-verified work and were sitting in `/private/tmp`. |
| `agent_findings/thebanks_eu.jsonl` | 50 aggregator figures, all FY2024. Re-collecting means WebSearch with `allowed_domains:["thebanks.eu"]` — **the site itself is behind a Cloudflare CAPTCHA and must not be bypassed.** |
| `thebanks_eu/thebanks_eu_returns.jsonl` | Exhaustive exact-entity TheBanks.eu refresh for all 145 project banks over the FY2021–FY2025 request window: 146 recoverable bank-year observations across 141 banks. Kept separate from bank-published returns; see `thebanks_eu/README.md`. |
| `thebanks_eu/thebanks_eu_archive_returns.jsonl` | Three new FY2023 exact-bank records recovered from retained historic TheBanks.eu search-index text during the archive pass. These are explicitly not represented as replayed Wayback snapshots; see `thebanks_eu/archive_report.md`. |
| `thebanks_eu/thebanks_eu_returns_with_archives.jsonl` | Non-destructive deduplicated view of the 146 live/indexed records plus the 3 historic supplements: 149 bank-years across 141 exact entities. Not a worksheet input unless explicitly adopted later. |
| `UK_banks_profitability_RESUME.md` | the 2026-10-08 cold-resume handoff. Historical; its "Aldermore not fixed" section is **stale** — that defect was corrected on 2026-10-08. |
