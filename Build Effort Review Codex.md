# Build Effort Review Codex

WF-019 execution record for the Codex session on 2026-08-28. This is a
separate report from `Build Effort Review.md`; no shared tracker, tooling, or
existing-bank files were modified.

## Scope

Five banks were processed in parallel, using the five most recent available
financial years (FY2021-FY2025):

| Bank | Result | Workbook | Notes |
|---|---|---|---|
| OneSavings Bank Plc | Built | `banks/ONESAVINGS FINANCIALS.xlsx` | Cash flow is Company-only; Pillar 3 is OSB Group consolidated. Companies House filings required OCR. FY2021 NSFR components and FY2021-FY2023 MREL ratios remain blank where not disclosed. |
| Oxbury Bank PLC | Built | `banks/OXBURY FINANCIALS.xlsx` | Cash flow uses Company columns. FY2022 cash flow is presented using the restated comparative from the FY2023 report; dedicated Pillar 3 data was found for FY2022-FY2023, with other years using disclosed annual-report KPIs where available. |
| Paragon Bank Plc | Built | `banks/PARAGON FINANCIALS.xlsx` | Statutory cash flow uses the Bank entity. Regulatory metrics use the applicable Paragon Banking Group/Pillar 3 basis. FY2025 Pillar 3 access and MREL gaps are documented. |
| Perenna Bank PLC | Built | `banks/PERENNA FINANCIALS.xlsx` | FY2021-FY2023 cash flow is Company-only; FY2024-FY2025 is consolidated Group basis. All five Companies House filings required OCR. Only explicitly disclosed CET1 and leverage KPIs are populated. |
| Persia International Bank Plc | Built | `banks/PERSIA INTERNATIONAL BANK FINANCIALS.xlsx` | EUR source figures converted to GBP using disclosed rates. Later Pillar 3 metrics are unavailable; sanctions, ownership, risk weighting, and the FY2021 opening-rate limitation are documented. |

## Validation

All five build scripts passed Python compilation. Each generated workbook was
reopened with `openpyxl` and checked for the standard 13-sheet order, two
Overview charts, and source-citation cells.

`verify_workbook.py` confirmed 13 sheets and two charts in every workbook.
Its automated cash-flow block results were:

- OneSavings: 3/4 blocks passed.
- Oxbury: 3/4 blocks passed.
- Paragon: 3/4 blocks passed.
- Perenna: 3/4 blocks passed.
- Persia: 0/1 compact block passed.

The ordinary 3/4 warnings are the verifier's known limitation around the
opening-cash/net-change/closing-cash tail, not failures in the operating,
investing, or financing blocks. Persia's warning is amplified by its compact
FX-converted presentation and the deliberately blank FY2021 opening value;
the worker manually reconciled FY2022-FY2025 after the translation adjustment.

## Research and effort notes

The five workers ran concurrently. Exact per-worker duration and token
metadata were not exposed to this parent session, so no invented timing or
token estimates are recorded here. Research used official Companies House,
bank investor-relations/report archives, official Pillar 3 documents where
available, the existing `scripts/pdf_tools.py` workflow for scanned PDFs, and
`scripts/verify_workbook.py`.

The main recurring patterns were entity-versus-group basis changes, sparse or
missing Pillar 3 disclosures, OCR-dependent Companies House filings, and
source-reported cash-flow restatements. These were retained as notes and
explicit blanks rather than filled by inference.

## Proposed shared-file edits (not applied)

After user approval, the following tracker-only edits can be made:

1. In `wayfinder/tickets/WF-019.md`, mark all five bank progress checkboxes as
   complete and append a dated session-log entry recording five builds.
2. In `wayfinder/map.md`, append the normal Batch 19 completion summary once
   the user confirms the ticket should be closed.
3. Leave WF-019/WF-020 status fields unchanged because the user stated that the
   other model will update statuses.

No edits are proposed to `scripts/bank_workbook.py`, existing bank scripts or
workbooks, `Build Effort Review.md`, or any other shared tooling.

---

## WF-020 execution record

WF-020 was processed in parallel on 2026-08-28. All five banks were built as
full workbooks:

| Bank | Result | Coverage and notable treatment |
|---|---|---|
| Punjab National Bank (International) Limited | Built | FY2022-FY2026, the five latest available years; entity-level USD accounts converted to GBP, with full Pillar 3 metrics and an explicit MREL gap. |
| QIB (UK) Plc | Built | FY2021-FY2025, entity-only GBP basis; official Pillar 3 metrics and FY2023/FY2024 subtotal discrepancies documented. |
| Rathbones Investment Management Limited | Built | FY2021-FY2025, entity-level GBP accounts; entity-level Pillar 3 metrics remain undisclosed rather than substituting group figures. |
| RBC Europe Limited | Built | FY2021-FY2025, October year-end and entity-level GBP basis; FY2021 LCR/NSFR are explicitly undisclosed. |
| RCI Bank UK Limited | Built | FY2020-FY2024, the five latest available years because FY2025 accounts were not filed; consolidated Group basis, with all five scanned filings OCR-processed. |

The five scripts were compiled and rerun successfully in the parent workspace.
Each workbook was confirmed to contain the standard 13 sheets and two Overview
charts. The generic verifier reported 0/1, 3/4, 3/4, 1/3, and 3/5 detailed
cash-flow block passes respectively for Punjab National Bank International,
QIB, Rathbones, RBC Europe, and RCI. These raw counts include the verifier's
known false positives: compact FX/translation rows, separately presented
exchange-rate effects, tax subtotals, and the opening/closing cash tail.
Worker-level independent checks confirmed the underlying operating, investing,
financing, subtotal, cash-chain, FX, chart, and workbook-integrity checks for
each bank, with the source-specific discrepancies retained in workbook notes.

No shared tracker, tooling, existing bank, or shared effort-review file was
modified. Proposed tracker changes are:

1. Mark all five banks complete and append a dated WF-020 session-log entry in
   `wayfinder/tickets/WF-020.md`.
2. Mark WF-020 `closed` and WF-021 `open` after the user confirms the queue may
   advance.
3. Add the Batch 20 summary to the existing Decisions section and update the
   WF-020/WF-021 rows in `wayfinder/map.md`.

---

## WF-021 execution record

WF-021 was processed in parallel. Four banks were built and one was
self-skipped on documented structural grounds:

| Bank | Result | Coverage and notable treatment |
|---|---|---|
| Recognise Bank Limited | Built | FY2022-FY2026, standalone Company basis; CAML liquidation and resulting basis change documented. |
| Redwood Bank Limited | Built | FY2021-FY2025, Company-only basis; FY2021/FY2022 OCR and a comparative-column reclassification documented. |
| Reliance Bank Limited | Built | FY2022-FY2026; entity-level GBP cash flows, 2023 restatement and small source arithmetic differences documented. |
| Revolut Bank UK Ltd | Skipped | No FY2021 accounts, FRS 101 IAS 7 cash-flow exemption, and no standalone entity-level Pillar 3 dataset; Group figures were not substituted. |
| Santander Financial Services plc | Built | FY2021-FY2025, standalone Company basis; standalone capital-ratio/RWA gaps retained and SFS capital/liquidity figures used where disclosed. |

The four build scripts were compiled and rerun successfully in the parent
workspace. Each generated workbook has the standard 13-sheet order and two
Overview charts. Santander's initial out-of-order metric tabs were caught by
the parent integration check, corrected in its own build script, rebuilt, and
rechecked. Generic verifier warnings were independently reviewed as known
tail-chain, subtotal, exchange-rate, or source-presentation limitations; the
workers' independent subtotal and cash-chain checks passed for each built bank.

No shared tooling, existing bank, or shared effort-review file was modified.
The proposed shared edits are:

1. Mark Recognise, Redwood, Reliance, and Santander complete and Revolut
   skipped in `wayfinder/tickets/WF-021.md`, with a dated session-log entry.
2. Mark WF-021 `closed` and WF-022 `open`.
3. Add the Batch 21 summary and update the WF-021/WF-022 rows in
   `wayfinder/map.md`.

### Revolut reassessment

At the user's request, Revolut Bank UK was reassessed using the shorter
FY2022-FY2025 timeframe. The missing FY2021 filing is not the deciding blocker:
FY2022 had no trading/cash-flow statement, FY2023-FY2025 explicitly claim the
FRS 101 exemption from IAS 7, and no standalone UK-entity Pillar 3 dataset was
found. The available Group disclosures cannot responsibly be substituted for
the UK entity. Revolut therefore remains a documented self-skip, with no script
or workbook created.

---

## WF-022 execution record

WF-022 was processed in parallel on 2026-08-28. Four banks were built and one
was self-skipped on documented entity/source-availability grounds:

| Bank | Result | Coverage and notable treatment |
|---|---|---|
| Schroder & Co. Limited | Built | FY2021-FY2025, standalone Company basis in GBP'000; all five Companies House accounts required OCR; standalone Pillar 3 metrics were not publicly disclosed. |
| Secure Trust Bank plc | Built | FY2021-FY2025, consolidated Group basis; FY2021 comparative restatement retained; LCR, NSFR, and MREL were not publicly disclosed. |
| Shawbrook Bank Limited | Built | FY2021-FY2025, Company cash-flow basis; bank-specific regulatory metrics through FY2024, with FY2025 left blank where only Group Pillar 3 information was available. |
| Standard Chartered Bank | Skipped | The exact PRA/FRN entity was verified, but only a recent Bank-level half-year report was located; PLC group reports and Pillar 3 disclosures were not substituted for the requested standalone five-year dataset. |
| State Bank of India (UK) Limited | Pillar 3-only | FY2021-FY2025 standalone UK entity; official disclosures support capital, RWA, leverage, LCR, and NSFR metrics; the FY2025 accounts claim the FRS 102 cash-flow exemption. |

The four generated scripts were compiled and rerun successfully in the parent
workspace. All four workbooks contain the standard 13-sheet order. Schroder,
Secure Trust, and Shawbrook contain two Overview charts; the SBI UK
Pillar-3-only workbook contains one chart because it has no cash-flow dataset.
The generic verifier reported 3/4 cash-flow blocks for each of Schroder, Secure
Trust, and Shawbrook, with the known opening/closing cash-tail warning. SBI UK
has 0/0 cash-flow blocks, as expected. Worker-level independent reconciliations,
source checks, and XLSX integrity checks passed.

No shared tracker, tooling, existing bank, or shared effort-review file was
modified. Proposed shared edits are:

1. Mark Schroder, Secure Trust, Shawbrook, and State Bank of India (UK)
   complete, and Standard Chartered skipped, with a dated session-log entry
   in `wayfinder/tickets/WF-022.md`.
2. Mark WF-022 `closed` and WF-023 `open`.
3. Add the Batch 22 summary and update the WF-022/WF-023 rows in
   `wayfinder/map.md`.

## Retrospective timing note

Exact worker timings and token counts were not exposed by the agent interface
for the earlier batches. Filesystem timestamps provide only approximate lower
bounds for the parallel build/output phase:

| Batch | Approximate observable window | Interpretation |
|---|---:|---|
| WF-019 | at least 14 minutes | First builder file at 22:00:45; generated workbooks at 22:14:57. |
| WF-020 | at least 12 minutes | First builder file at 22:24:03; generated workbooks at 22:36:31. |
| WF-021 | at least 6 minutes | First builder file at 22:45:40; final generated workbook at 22:52:00. |
| WF-022 | at least 6 minutes | First builder file at 23:01:34; final generated workbook at 23:06:53; parent validation completed shortly afterward. |

These are not full elapsed worker durations and should not be treated as
precise effort measurements. No retrospective token estimate is available.

## Timing capture for future batches

For each future batch, record only the total wall-clock duration from agent
dispatch to final parent integration. Capture the dispatch timestamp and the
final integration timestamp, then report their difference; do not record
individual rebuild, compilation, or verification timings as effort measures.
Record token usage only when the platform returns an authoritative usage field;
otherwise mark it unavailable rather than estimating it.

## WF-023 execution record

WF-023 was processed in parallel on 2026-08-28. Both banks were built:

| Bank | Result | Coverage and notable treatment |
|---|---|---|
| StreamBank PLC | Built | FY2021, FY2023 (15-month transition period), FY2024, and FY2025. FY2022 is intentionally absent because the accounting period was extended to March 2023. |
| Weatherbys Bank Limited | Built | FY2021-FY2025, consolidated Weatherbys Banking Group basis; FY2025 Pillar 3 metrics remain blank where no official disclosure was available. |

Both workers confirmed the legal entity, FRN, and source availability. Each
generated workbook has the standard 13-sheet order and two Overview charts.
Independent cash-flow bridges and XLSX integrity checks passed. The generic
verifier reported 3/4 blocks for StreamBank and 3/5 for Weatherbys; the
remaining warnings are the known opening/closing cash-tail and intermediate
subtotal patterns, not independent reconciliation failures.

StreamBank's worker reported 3m51s from its own start/completion timestamps.
The total batch wall-clock duration from agent dispatch through final parent
integration was not captured consistently enough to report retrospectively.
Individual rebuild, compilation, and verification timings are intentionally
not retained as effort measures.

No authoritative token-usage metadata was exposed by either worker or the
parent tool interface. Token usage is therefore recorded as unavailable, with
no estimate substituted.

## Semi-annual Pillar 3 expansion — existing banks

On 2026-08-29, the existing-workbook semi-annual group was processed in
parallel: Aldermore Bank, The Co-operative Bank, Investec Bank, Paragon Bank,
and Secure Trust Bank. The approximate total wall-clock duration from agent
dispatch to final parent integration was 9 minutes. Individual rebuild,
compilation, and verification timings are intentionally not retained as effort
measures. Authoritative token usage was unavailable.

Each workbook gained a 14th `Interim Pillar 3` sheet, with annual sheets and
two Overview charts preserved. The sourced observation counts were: Aldermore
48, Co-operative Bank 19, Investec 88, Paragon 50, and Secure Trust 37.
Historical or entity-basis gaps were recorded explicitly where applicable.
Metro Bank is listed in the cadence research but had no existing workbook and
was not included in this pass.

## Interim Pillar 3 expansion — existing quarterly banks

On 2026-08-29, the remaining quarterly-reporting banks with existing
workbooks were processed in parallel: RBC Europe Limited and SMBC Bank
International plc. The approximate total wall-clock duration from agent
dispatch to final parent integration was 10 minutes. Individual rebuild,
compilation, and verification timings are intentionally not retained as effort
measures. Authoritative token usage was unavailable.

RBC Europe gained 97 interim observations covering April 2021–July 2025, each
with an official source hyperlink. SMBC Bank International gained 180 interim
observations covering 12 June/September/December periods from 2022–2025, each
with an official source hyperlink. Both workbooks retained their annual sheets
and two Overview charts; the standard verifier confirmed 14 sheets and the
expected interim-table structures. Existing cash-flow reconciliation warnings
remain unrelated to these additions.

No shared tracker, tooling, existing bank, or shared effort-review file was
modified. Proposed shared edits are:

1. Mark StreamBank PLC and Weatherbys Bank Limited complete and append the
   dated session-log entry in `wayfinder/tickets/WF-023.md`.
2. Mark WF-023 `closed` in its frontmatter.
3. Add the Batch 23 summary to `wayfinder/map.md`; this is the final ticket, so
no WF-024 should be opened.

## WF-018 interim expansion

On 2026-08-29, the three WF-018 banks with defensible entity-level interim
Pillar 3 evidence were expanded from 13 to 14 sheets in parallel:

| Bank | Interim coverage |
|---|---|
| National Westminster Bank plc | 108 observations across 12 quarterly periods from March 2022 to September 2025; liquidity metrics excluded where only UK DoLSub data was available. |
| NatWest Markets plc | 137 observations across 13 quarter-end periods from September 2021 through September 2025. |
| Nomura Bank International plc | 45 observations across September 2021–2025, including explicit later non-disclosure entries where standalone Pillar 3 tables were unavailable. |

All three retained their annual sheets and existing Overview charts. The
approximate total end-to-end parent duration from agent dispatch to final
integration was 17 minutes. Individual rebuild, compilation, and verification
timings are intentionally not retained as effort measures. Authoritative token
usage was unavailable from the agent interface.

## WF-016 execution record

WF-016 was claimed and processed in parallel on 2026-08-29. All five banks
were built and validated:

| Bank | Result | Workbook shape / note |
|---|---|---|
| Lloyds Bank plc | Built | 14 sheets; 159 interim observations across 2021 Q1/H1/Q3 and 2022–2025 Q1/H1/Q3. |
| Marks and Spencer Financial Services plc | Built | 13 sheets; interim Pillar 3 is reported through HSBC UK consolidated disclosures, not standalone entity data. |
| Melli Bank plc | Built | 13 sheets; no defensible public interim series; FY2025 regulatory data unavailable. |
| Methodist Chapel Aid Limited | Built | 13 sheets; annual Pillar 3 policy and no defensible interim series. |
| Metro Bank plc | Built | 14 sheets; 35 entity-level interim observations; later Holdings Group data excluded. |

The approximate total parent wall-clock duration from agent dispatch at 11:29
BST to final integration at 11:40 BST was 11 minutes. Individual rebuild,
compilation, and verification timings are intentionally not retained as effort
measures. Authoritative token usage was unavailable from the agent interface.

## WF-017 execution record

WF-017 was claimed and processed in parallel on 2026-08-29. All five banks
were built and validated:

| Bank | Result | Coverage / note |
|---|---|---|
| Mizuho International plc | Built | FY2021–FY2025 annual workbook; annual-only Pillar 3 archive. |
| Monument Bank Limited | Built | FY2021–FY2024 populated; FY2025 accounts unavailable and left blank. |
| Morgan Stanley Bank International Limited | Built | FY2021–FY2025 standalone data; group-level interim evidence excluded. |
| National Bank of Egypt (UK) Limited | Built | FY2021–FY2025 annual workbook; annual-only Pillar 3 evidence. |
| National Bank of Kuwait (International) plc | Built | FY2021–FY2025 Pillar-3-only workbook; FRS 101 cash-flow exemption. |

The approximate total parent wall-clock duration from agent dispatch at 11:13
BST to final integration at 11:31 BST was 18 minutes. Individual rebuild,
compilation, and verification timings are intentionally not retained as effort
measures. Authoritative token usage was unavailable from the agent interface.

## WF-018 execution record

WF-018 was claimed and processed in parallel on 2026-08-29. All five banks
were built and validated:

| Bank | Result | Coverage / note |
|---|---|---|
| National Westminster Bank plc | Built | FY2021–FY2025 annual workbook; quarterly Pillar 3 follow-up remains separate. |
| NatWest Markets plc | Built | FY2021–FY2025 annual workbook; entity confirmed distinct from RBS plc; interim follow-up remains. |
| Nomura Bank International plc | Built | FY2021–FY2025 annual workbook; September/group interim reporting noted for follow-up. |
| Northern Bank Limited | Built | FY2021–FY2025 annual workbook; entity confirmed as Companies House R0000568. |
| OakNorth Bank plc | Built | FY2021–FY2025 annual workbook; annual-only archive, so no interim follow-up. |

The approximate total parent wall-clock duration from agent dispatch at 10:53
BST to final integration at 11:03 BST was 10 minutes. Individual rebuild,
compilation, and verification timings are intentionally not retained as effort
measures. Authoritative token usage was unavailable from the agent interface;
no estimate was substituted.

## Wide interim-layout conversion

On 2026-08-29, all 13 eligible 14-sheet workbooks were converted from the
long-form interim table to a wide matrix with metrics as rows and filing
periods as columns. The shared workbook helper and verifier were extended
backward-compatibly; all original observations, value hyperlinks, and source
registers were preserved. The approximate end-to-end duration was 30 minutes,
including parent integration and final validation. Authoritative token usage
was unavailable.

## WF-024 execution record

WF-024 was dispatched in parallel on 2026-08-29 to reassess five previously
skipped banks whose official disclosure availability had improved. All five
were built as 13-sheet Pillar-3-only workbooks:

| Bank | Result | Coverage / note |
|---|---|---|
| GB Bank Limited | Built | FY2021–FY2025 solo Pillar 3; shortened FY2024 and a 2023 RWA inconsistency documented. |
| J.P. Morgan Europe Limited | Built | FY2023–FY2025 standalone JPMEL data; FY2021–FY2022 not separately disclosed. |
| ICICI Bank UK Plc | Built | FY2021–FY2025 standalone UK KM1 data; early unavailable comparatives left blank. |
| United Trust Bank Limited | Built | FY2021–FY2025 consolidated UTB Partners basis, explicitly labelled. |
| TD Bank Europe Limited | Built | FY2021–FY2025; FY2021 basis transition and 2025 NSFR source discrepancy documented. |

All five builder scripts compiled and rebuilt successfully. Parent validation
confirmed 13 sheets in the expected order and 0/0 cash-flow blocks for each,
as expected for Pillar-3-only workbooks. Each has one Overview chart because no
cash-flow series exists. Targeted checks confirmed the documented regulatory
scope, ratio/detail consistency, and source-note coverage. The approximate
end-to-end duration from dispatch at 12:10:14 BST to final validation at
12:16:33 BST was 6 minutes 19 seconds. Individual build or verification times
are not recorded. Authoritative token usage was unavailable.

## WF-025 execution record

WF-025 was dispatched in parallel on 2026-08-29 to revisit five previously
skipped banks whose source availability had improved:

| Bank | Result | Coverage / note |
|---|---|---|
| Citibank UK Limited | Built | FY2021–FY2023 standalone Pillar 3; FY2024–FY2025 standalone reports were not located. |
| Union Bancaire Privée (UK) Limited | Built | FY2021–FY2024 Pillar 3 on the UK Consolidation Group basis; FY2025 gap documented. |
| Philippine National Bank (Europe) Plc | Built | FY2024–FY2025 standalone Pillar 3; earlier quantitative coverage not defensible. |
| Standard Chartered Bank | Built | FY2021–FY2025 standalone Bank accounts; standalone regulatory metrics left undisclosed. |
| THIS BANK LIMITED | Built | FY2021–FY2025 full annual workbook; LCR/NSFR tab-order issue caught and corrected. |

All five builders compiled and rebuilt successfully. Parent validation confirmed
13 sheets for each workbook, correct structure, and the expected one Overview
chart for the three Pillar-3-only workbooks. Standard Chartered's cash-flow
reconciliations passed independently; its remaining generic verifier warning is
the known opening-cash/FX/closing-cash tail limitation. THIS BANK's independent
cash-flow checks passed after its sheet-order correction. The approximate total
end-to-end duration from dispatch at 12:17:39 BST through final validation at
12:25:38 BST was 7 minutes 59 seconds. Individual rebuild and verification
durations are not recorded. Authoritative token usage was unavailable.

## Later revisit execution record

On 2026-08-29, three later revisit candidates were processed sequentially in
the agreed order:

| Bank | Result | Coverage / note |
|---|---|---|
| Afin Bank Limited | Built | New FY2024-only workbook; its first Pillar 3 disclosure explicitly provides no prior-period comparatives. The unusual 999999% LCR is retained and documented. |
| J.P. Morgan Securities plc | Expanded | Existing Pillar-3-only workbook expanded from FY2024–FY2025 capital data to FY2021–FY2025 capital, RWA, leverage and LCR data, plus NSFR from FY2022 onward. MREL remains unavailable. |
| Goldman Sachs International Bank | Expanded | Existing workbook expanded with GSIB-specific FY2021–FY2025 capital, ratios, RWA, leverage, LCR and NSFR recovered from official GSG UK Pillar 3 tables. MREL remains unavailable. |

All three workbooks retain 13 sheets in the standard order. Afin's parent-side
verification reports one bank-specific opening-cash/closing-cash tail warning;
J.P. Morgan Securities has the expected single-chart Pillar-3-only result; and
Goldman's existing cash-flow tail warning remains. No shared helpers or the
historical tickets were modified. The measured Afin agent run was approximately
4 minutes 43 seconds (12:39:11–12:43:54 BST), and the Goldman investigation plus
implementation ran approximately 10 minutes 04 seconds in total
(12:52:18–13:02:22 BST). The JPM agent did not capture a reliable start/end
window; parent rebuild and verification completed successfully. Individual
rebuild and verification durations are not recorded. Authoritative token usage
was unavailable from the agent interface.

## FirstBank and EFG discrepancy resolution

The 2026-08-29 source review resolved the two financial follow-ups identified
in the final audit:

- **FirstBank UK:** no financial value was changed. The FY2022 RWA difference
  is a GBP-to-USD restatement by FirstBank, not conflicting USD data. The
  FirstBank builder now records the original £1,019,070k amount, the restated
  $1,230,686k amount, the implied conversion, and the GBP/USD volatility caveat.
- **EFG Private Bank:** the workbook now follows the originally published
  FY2022 vintage, changing net change in cash from £(65,618)k to £(60,778)k.
  The later £4,840k term-deposit reclassification remains documented in the
  source note rather than being mixed into the original-year column.

Both builders compiled and both workbooks rebuilt successfully. The remaining
verifier warnings are existing bank-specific cash-flow-tail limitations; no
new structural issue was introduced.

## Final-audit citation remediation

Following the read-only final audit, the citation and source-link issues were
fixed without changing financial values or disclosure scope:

| Area | Result |
|---|---|
| Bank of Africa UK | Added official source citations to the MREL not-disclosed note. |
| ICICI Bank UK | Added the official FY2025 financial-statements URL to the cash-flow exemption note. |
| M&S Financial Services | Added the five direct Companies House annual-report URLs to each non-disclosed metric citation block. |
| Metro Bank | Added `n/a` to the explanatory interim row's Unit field and replaced early source-register titles with the official H1 2022 Pillar 3 URL, which contains both comparative periods. |
| RBC Europe and Secure Trust | Corrected the shared wide-interim helper so `hyperlink_cells` is applied; all populated interim values now link to official sources. |

Validation confirmed the affected workbooks rebuild successfully. RBC Europe had
97/97 populated interim cells linked and Secure Trust had 37/37. The helper was
also regression-checked against a 13-sheet Barclays workbook. All 13 current
interim workbooks have source hyperlinks, and all 128 current 13-sheet
workbooks retain their expected structure. No financial discrepancy work was
included in this pass.

## IN-004 execution record

On 2026-08-29, IN-004 was started and completed through the first full analysis
pass. The end-to-end agent window, including the normalized-data scan, script
creation, document update, and final validation, was approximately 6 minutes
(roughly 17:29–17:35 BST). Individual rebuild/verification durations were not
recorded, as requested. Authoritative token usage was unavailable from the
agent interface.

The subsequent IN-004 selection-hardening pass took approximately 6 minutes
end-to-end, including exception-report generation, rule changes, rerun and
tests. Individual rebuild/verification durations were not recorded;
authoritative token usage was unavailable.

## IN-005f execution record

On 2026-08-29, independent trend metric selectors, arbitrary year-range inputs,
and total-RWA series were implemented and validated in approximately 7 minutes
end-to-end. Individual rebuild/verification durations were not recorded;
authoritative token usage was unavailable.

## IN-005 prototype execution record

On 2026-08-29, the initial single-file HTML prototype was generated and
validated in approximately 6 minutes end-to-end. Individual rebuild/verification
durations were not recorded; authoritative token usage was unavailable.

## IN-005a / IN-005b execution record

On 2026-08-29, visual refinement and selectable trend controls were implemented
and validated in approximately 8 minutes end-to-end. Individual rebuild/
verification durations were not recorded; authoritative token usage was
unavailable. Subagent delegation was attempted but unavailable because the
active-agent thread limit had been reached.

## IN-005c execution record

On 2026-08-29, the parent-group drill-down was implemented and validated in
approximately 5 minutes end-to-end. Individual rebuild/verification durations
were not recorded; authoritative token usage was unavailable.

## IN-005g execution record

On 2026-08-29, the trend-count layout, peer-group terminology, and metric
definitions were updated and validated in approximately 5 minutes end-to-end.
Individual rebuild/verification durations were not recorded; authoritative
token usage was unavailable.

## IN-005i execution record

On 2026-08-29, peer-list toggling, metric-guide layout, chart spacing, and
dual parent-group metrics were implemented and validated in approximately 4
minutes end-to-end. Individual rebuild/verification durations were not
recorded; authoritative token usage was unavailable.

## IN-005j execution record

On 2026-08-29, duplicated Key Takeaways content was replaced with quantified
RWA, capital-ratio, and operating-cash-flow trends in approximately 3 minutes
end-to-end. Individual rebuild/verification durations were not recorded;
authoritative token usage was unavailable.

## IN-006 execution record

On 2026-08-29, the final HTML Artifact and fixed PDF companion were generated,
validated, and documented in approximately 12 minutes end-to-end, including
the format-decision grilling round. Individual rebuild/verification durations
were not recorded; authoritative token usage was unavailable.

## Pipeline test execution record

On 2026-08-29, unit, integration, and end-to-end coverage for IN-007/IN-008
was expanded and run in approximately 8 minutes end-to-end. The suite reached
31 passing tests and included a real 145-workbook extraction into a temporary
database. Individual rebuild/verification durations were not recorded;
authoritative token usage was unavailable.

## Clean-layout revalidation record

On 2026-08-29, the relocated insights pipeline was re-mapped and revalidated
in approximately 5 minutes end-to-end. The ordered real refresh completed,
the full suite reached 34 passing tests, all Python files compiled, and all
145 bank workbooks completed the generic verifier without a process failure.
Individual rebuild/verification durations were not recorded; authoritative
token usage was unavailable.

## Additional test coverage record

On 2026-08-29, output-safety, PDF pagination, refresh artifact-preservation,
and database rollback tests were added and validated in approximately 4 minutes
end-to-end. The insights suite reached 122 passing tests. Individual rebuild/
verification durations were not recorded; authoritative token usage was
unavailable.
