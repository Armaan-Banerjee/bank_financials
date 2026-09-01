---
label: wayfinder:map
title: "Bank financials data-collection map"
---

## Destination

Every one of the 148 banks in `Banks List 2608.xlsx` has been attempted — a full
workbook, a Pillar-3-only workbook, or a documented structural skip — with
`Build Effort Review.md` (time/token tracking + difficulty ranking) and
`~/.claude/projects/-Users-armaan-code-katalysis/memory/project_bank_financials_workbooks.md`
kept current after every batch. WF-024 and WF-025 are authorised revisit tickets
for skips whose source availability has materially improved; after WF-025 closes,
this map's current bank-build queue is done.

Statistics/insights work (cross-bank trend analysis, PowerBI-style integration) is
explicitly a *separate* future map — see "Not yet specified" below. Don't pull it
into this map's tickets.

## Notes

- **WF-007-009's and WF-010-012's batched-reporting instructions (both given
  2026-08-28) are both fulfilled** — all six tickets closed, one combined
  summary sent for each trio. Per-batch check-ins are the default from
  WF-013 onward unless the user asks for another quiet stretch.
- **Concurrent session note (2026-08-29): a separate model/session is working
  WF-019 through WF-023 in parallel with this session's WF-013-018.** If you
  see banks/scripts appear on disk for that range that this session's tickets
  didn't dispatch, that's expected — don't re-dispatch or "fix" them here.
  Verify against the ticket's own bank list before assuming disk state is
  stale or wrong.
- **Standing constraint, stated twice by the user (2026-08-28): do not
  redeploy any tooling fix across already-built banks.** Only fix a script
  when a bug is found while legitimately working that specific bank/ticket —
  never run a bulk "fix all banks" pass without explicit future permission.
  This applies to `bank_workbook.py`/`bank_scaffold.py` changes and to any
  script-level fix pattern alike.
- **A known sandbox-side bug: Wayback-archived PDF fetches truncate at
  ~1MB (1,048,576 bytes)**, first hit at Gulf International Bank UK, then
  HBL Bank UK and Ghana International Bank (WF-010-012). It looks like a
  normal fetch failure but isn't source-side — the fix is a manual chunked
  range-request download (with retries), not a plain re-fetch or `qpdf`/
  `fitz` xref repair (which only sometimes recovers a truncated file).
  Mention this upfront in future fork prompts for any bank sourcing Pillar 3
  or filings via Wayback, so the fork reaches for the chunked-download
  workaround immediately instead of losing several minutes rediscovering it.
  Confirmed (2026-08-28 diagnostic pass) this bug, not forgotten efficiency
  rules or stalling, explains most of WF-010-012's above-average build times
  — those tickets just happened to pull several fully-scanned-filing banks
  back to back, which forces `pdf_tools.py render`-heavy page-by-page
  transcription regardless of how efficient the fork is.
- **Check what's actually on disk before resuming or re-dispatching after a
  session-limit cutoff — every case is different.** Across WF-006/007/009,
  the same-looking cutoff produced four genuinely different situations: (1)
  nothing written at all (re-dispatch fresh), (2) a complete, correct script
  that was simply never executed (just run it, no fork needed), (3) a fix
  already applied to the script but the workbook never rebuilt (just rebuild
  it, no fork needed), (4) a real half-applied fix or a genuine unfound bug
  (needs a dedicated fix fork). A cutoff fork's own last message is a hint,
  not a verdict — always check `banks/`/`scripts/` and re-run
  `verify_workbook.py` before deciding which of these four situations you're
  actually in.

- **This map carries execution, not just decisions.** Every ticket (`wayfinder:task`)
  is a batch of up to 5 banks to actually build or skip — the deliverable is the
  workbook(s) themselves, not a design decision. This is a deliberate override of
  wayfinder's plan-only default (see the skill's "Plan, don't do" section).
- **Tracker**: no git repo and no issue tracker exist for this project, so this map
  uses a **local-markdown tracker**: this file plus one file per ticket under
  `wayfinder/tickets/WF-NNN.md`. Each ticket's YAML frontmatter carries `status`
  (`blocked` / `open` / `in-progress` / `closed`) and `blocked_by` (the prior
  ticket's id, or `null`). Tickets are chained strictly in order — WF-002 is
  `blocked` until WF-001 is `closed`, and so on — so the frontier is always exactly
  the lowest-numbered ticket that isn't `closed`.
- **Claiming**: a session starting a ticket sets its `status: in-progress`. There's
  no separate assignee field — this is a single-operator project, so "not closed"
  is enough signal that a ticket still needs work.
- **Partial completion is expected and fine.** If a session runs low on its 5-hour
  usage budget mid-ticket, it does NOT close the ticket or spin up a replacement.
  It appends a dated entry to the ticket's "Session log" section recording exactly
  which banks got done and which didn't, leaves `status: open` (or `in-progress`),
  and stops. The next session opens that same ticket and continues — this is the
  whole point of the map: no work gets silently lost to a session cutoff.
- **Session cadence is manual.** No cloud/cron automation — investigated and
  deliberately deferred (see Decisions so far). Start a new session, say "work the
  next wayfinder ticket," and it resumes correctly from the ticket files alone.
- **Research is folded into each build**, not a separate phase — confirm entity
  match against `Banks List 2608.xlsx`, check Companies House + Pillar 3 archive
  availability (incl. Wayback Machine), then build or self-skip in the same pass.
  Self-skipping on a clear structural blocker is pre-authorized; flag genuine
  entity-identity ambiguity rather than guessing.
- Every ticket follows the same process already established across the first 36
  banks: `CLAUDE.md`'s "Workflow notes for adding a new bank", `scripts/bank_workbook.py`,
  `scripts/build_barclays.py` as the reference script, `scripts/verify_workbook.py`
  before closing a ticket.
- **Efficiency**: tell each fork to WebFetch the bank's own site and Companies
  House directly before reaching for WebSearch, use `pdf_tools.py scan` before
  assuming OCR is needed, check a later year's comparative column before
  searching for a missing standalone document, and reuse an existing FX rate
  table (e.g. from `build_zenith.py`/`build_arab_bank_europe.py`) rather than
  re-deriving one for a currency already used elsewhere. Confirmed working as of
  WF-004 (WebSearch calls dropped to 0-1 per fork). Note: the WebSearch quota
  (200) is shared across the whole session, not per-fork, so it can still
  exhaust partway through a 5-fork batch even with the directive.
- **A fork can stall** (a stream issue, distinct from hitting the session's
  usage limit — the notification says "no progress for Ns" rather than "hit
  your session limit"). Don't restart it from scratch: `SendMessage` to its
  `agentId` telling it exactly what it was doing when it stalled and to
  continue — this resumes it from its own transcript with all research already
  done intact. Confirmed working on WF-005 (2 of 5 forks stalled, both resumed
  cleanly). The resumed fork's reported duration will include the stall time,
  so treat it as inflated when logging to `Build Effort Review.md`.
- **Tell a stream stall apart from a session-limit termination** — they look
  similar (a fork notification with `status: failed`) but need opposite
  handling. A stall's summary reads "no progress for Ns" and its `result`
  field still has real content (the fork's last message before it froze) —
  `SendMessage` to resume it, per the note above. A session-limit termination's
  summary reads "hit your session limit" and its `result` is typically empty
  or cut off mid-sentence with no transcript to resume from — confirmed on
  WF-006 (all 5 forks killed this way at once). For that case: verify nothing
  was actually written to `banks/`/`scripts/` for the affected bank(s) (it
  usually wasn't — research happens before any file write), then wait for the
  limit to reset and re-dispatch those banks as fresh forks, not a `SendMessage`
  resume.
- **A fork's last message before a session-limit cutoff can overstate its real
  progress** — confirmed on WF-007: one fork's final message claimed "building
  now with full cash flow + not-disclosed Pillar 3," but the script it left
  behind was still the unfilled scaffold template. Always check what's
  actually on disk (`banks/`, `scripts/`) rather than trusting the cutoff
  message's framing before deciding whether to resume or re-dispatch fresh.
  Conversely, a script can exist with real data but never have been executed
  (no matching file in `banks/`) — try running it before assuming it needs
  redoing; it may just need `python3 scripts/build_X.py` to finish the job.
- **Periodic sanity-check audits are worth repeating**, not just doing once at
  the end. The first one (after WF-004) found 2 real data errors and 2 cosmetic
  structural issues across 47 workbooks — see the Decisions-so-far entry above
  for the method (a full `verify_workbook.py` run, pre-computed output handed
  to 4 parallel audit forks rather than each one re-running the tool).
- Historical pacing reference (21 tracked full builds): mean **11m 37s / 508,657
  tokens** per bank; self-skips are much cheaper (~1–5 min). A 5-bank ticket can
  therefore run well past one session's budget on its own — expect most tickets to
  span 2+ sessions, and treat that as normal, not a problem to fix.

## Decisions so far

<!-- Append one line per closed ticket: `- [Batch NN](tickets/WF-NNN.md) — a/b built, c/b skipped (gist)` -->

- [Batch 16](tickets/WF-016.md) — 5/5 built, 0/5 skipped (Lloyds and Metro
  received interim sheets; Marks and Spencer Financial Services, Melli Bank,
  and Methodist Chapel Aid were annual-only at entity level).

- [Batch 17](tickets/WF-017.md) — 5/5 built, 0/5 skipped (Mizuho, Monument,
  Morgan Stanley Bank International, National Bank of Egypt UK, and National
  Bank of Kuwait International; annual/entity-basis gaps documented).

- [Batch 18](tickets/WF-018.md) — 5/5 built, 0/5 skipped (National Westminster
  Bank, NatWest Markets, Nomura Bank International, Northern Bank, and OakNorth;
  quarterly/interim follow-up remains for the relevant entities).

- [Batch 20](tickets/WF-020.md) — 5/5 built, 0/5 skipped (Punjab National Bank
  International, QIB, Rathbones, RBC Europe, and RCI Bank UK; documented OCR,
  entity/group, disclosure, restatement, and FX limitations).

- [Batch 21](tickets/WF-021.md) — 4/5 built, 1/5 skipped (Recognise, Redwood,
  Reliance, Santander Financial Services built; Revolut skipped after confirming
  the FRS 101 cash-flow exemption and no standalone UK Pillar 3 dataset).

- [Batch 22](tickets/WF-022.md) — 4/5 built, 1/5 skipped (Schroder, Secure
  Trust, Shawbrook, and State Bank of India (UK) built; Standard Chartered
  skipped because the required standalone five-year source set was unavailable).

- [Batch 23](tickets/WF-023.md) — 2/2 built (StreamBank and Weatherbys; StreamBank
  has a documented 15-month transition period with no separate FY2022).

- [Batch 24](tickets/WF-024.md) — 5/5 built as Pillar-3-only workbooks (GB Bank,
  J.P. Morgan Europe, ICICI Bank UK, United Trust Bank, and TD Bank Europe);
  basis transitions and source discrepancies are documented.

- [Batch 25](tickets/WF-025.md) — 5/5 completed: Citibank UK, UBP UK, and
  Philippine National Bank Europe received Pillar-3-only workbooks; Standard
  Chartered Bank and THIS BANK received full annual workbooks.

- [Charting this map](map.md) — destination, tracker design, batching, and
  partial-completion protocol settled via `/wayfinder` + `/grilling` on 2026-08-26/27.
  Cloud/cron automation for session start was investigated and deferred (needs a
  GitHub repo this project doesn't have; manual cadence chosen instead for now).
- [Batch 01](tickets/WF-001.md) — 4/5 built (3 full: AIB Group UK, Aldermore,
  Allica; 1 Pillar-3-only: ABC International Bank), 1/5 self-skipped (Afin Bank,
  authorised Oct 2024, too young). New patterns: AIB's group→solo exemption switch
  mid-window, ABC's consolidated/solo Pillar-3 basis break.
- [Batch 02](tickets/WF-002.md) — 5/5 built (Alpha Bank London, ALRAYAN Bank, Arab
  Bank Europe, Arbuthnot Latham, Atom Bank), 0 skipped. Arab Bank Europe is the
  first EUR-reporting workbook in the series (4/5 years, thin Pillar 3, a real
  unreconciled €380m cash-bridge gap flagged not forced). Atom Bank is a third
  variant of the "exemption kicks in partway through the window" pattern.
- [Batch 03](tickets/WF-003.md) — 4/5 built (3 full: Bank of Africa UK, Bank of
  Beirut UK, Bank of Ceylon UK; 1 Pillar-3-only, FX-converted: Bank Mandiri
  Europe), 1/5 self-skipped (Bank Of Baroda UK — double blocker: permanent
  exemption + zero quantitative Pillar 3 data, unlike BNY Mellon's rich-data
  precedent). Bank of Africa UK is now the longest single build in the whole
  series (25m 29s) — a genuine multi-statement restatement, corroborated by an
  auditor's note referencing a regulatory investigation.
- [Batch 04](tickets/WF-004.md) — 5/5 built (Bank of China UK, BLME, Bank of
  Scotland — full; Bank of the Philippine Islands Europe — Pillar-3-only), 0
  skipped. Forks given an explicit efficiency directive this round (reuse
  tooling, WebFetch before WebSearch); WebSearch usage dropped to 0-1 calls per
  fork. Bank Saderat is the second EUR-reporting workbook and reflects an
  unfolding situation — UK sanctions hit it from 29 Sept 2025, materially
  affecting FY2025 figures. Bank of the Philippine Islands Europe introduced a
  new pattern: a mid-series GBP→USD currency switch.
- [Project-wide sanity-check audit](../Build%20Effort%20Review.md) (2026-08-27,
  between Batch 04 and Batch 05) — full `verify_workbook.py` run across all 47
  then-built workbooks plus a 4-fork deep audit of every flagged mismatch. Found
  and fixed: scrambled Pillar 3 sheet order in Bank Mandiri Europe/Bank Saderat
  (cosmetic, rebuilt), a real FY2026 transcription error in Starling
  (£185,354k → £183,334k), and 5 Company-vs-Group column mixups in Chetwood's
  FY2023/FY2024 cash flow. Everything else in all 47 workbooks confirmed either
  already-documented or a known checker false-positive. Worth repeating this
  audit periodically (e.g. every ~5 batches) rather than only at the end.
- [Batch 05](tickets/WF-005.md) — 5/5 built (Bank Sepah International, Barclays
  Bank Plc, Birmingham Bank, British Arab Commercial Bank, Brown Shipley), 0
  skipped. Barclays Bank Plc is a distinct entity from the already-built
  Barclays Bank UK PLC (non-ring-fenced vs. ring-fenced) — separate filename
  used, no collision. Two forks stalled on a stream issue mid-task and were
  resumed via SendMessage rather than restarted from scratch; their reported
  durations in `Build Effort Review.md` include the stall time.
- [Bank of Ireland UK styling fix](../scripts/build_bank_of_ireland.py)
  (2026-08-27) — the sanity-check audit's third finding: three running-subtotal
  rows were tagged `DATA` instead of `TOTAL`, so they weren't bold like every
  other bank's subtotals. Fixed by re-tagging, rebuilt. Figures were always
  correct — purely a styling/checker-false-positive fix.
- [Batch 06](tickets/WF-006.md) — 5/5 built (C. Hoare & Co., CAF Bank,
  Cambridge & Counties Bank, Castle Trust Capital, Cater Allen), 0 skipped.
  First ticket to hit a **session-limit termination** (distinct from the WF-005
  stream-stall case) — all 5 forks were killed mid-research with no resumable
  transcript, confirmed nothing was salvageable, and were re-dispatched fresh
  after the limit reset; see the Notes entry below on telling the two apart.
  Cater Allen introduced a new pattern: the cash-flow exemption applies only to
  the *final* year of the window (mirror image of Tandem/AIB/Atom's "kicks in
  partway" pattern). Two reusable-tooling bugs found and fixed:
  `bank_scaffold.py`'s color picker had a hardcoded single-color fallback once
  its palette was exhausted (now generates further unique colors), and
  `bank_workbook.py`'s `add_overview_sheet()` docstring now documents that
  `ratios=[]` is invalid (use empty-`{}`-valued entries instead).

- [Tooling fixes](../scripts/bank_workbook.py) (2026-08-28, at the user's
  request, deliberately not redeployed across already-built banks) —
  `bank_workbook.py`'s `add_overview_sheet()` now properly supports
  `ratios=[]` (mirrors `cash_flow_totals=[]`), regression-tested against all 6
  affected banks. Found and fixed a third scrambled-sheet-order instance
  (Brown Shipley) while doing so — all 57 banks built at that point confirmed
  on the standard sheet order.
- [Batch 07](tickets/WF-007.md) — 5/5 built (Charter Court Financial Services,
  ClearBank, Close Brothers, Coutts & Company), 1/5 self-skipped (Citibank UK
  — double blocker, same pattern as Bank Of Baroda UK). Hit a session-limit
  termination mid-batch (4 of 5 forks killed); recovery found one fork's
  script was an unfilled scaffold despite claiming progress (re-dispatched),
  one had real data but was never executed (ran cleanly on retry), and one
  had a real-looking reconciliation gap that turned out to be a misdiagnosis —
  an unbolded-subtotal checker false-positive (third instance of that bug
  class), not an actual data error. See the Notes entry on distinguishing a
  fork's own claimed progress from what it actually wrote to disk.

- [Batch 08](tickets/WF-008.md) — 5/5 built (Credit Suisse UK, Credit Suisse
  International, Crown Agents Bank, Cynergy Bank — full; DB UK Bank —
  Pillar-3-only), 0 skipped, no interruptions. Both Credit Suisse entities
  confirmed active and separately-reporting post the 2023 UBS rescue (not
  merged), but with real disclosed turmoil: a Part VII transfer at Credit
  Suisse UK, an explicit controlled wind-down (assets down 97.7%) at Credit
  Suisse International.

- [Batch 09](tickets/WF-009.md) — 5/5 built (DF Capital Bank, EFG Private
  Bank, FCE Bank, FCMB UK, FidBank UK), 0 skipped. A second session-limit
  termination hit this ticket too (4 of 5 forks killed); recovery found one
  case each of: a fix applied to the script but never rebuilt (no fork
  needed), a false alarm (interrupted fork had actually finished correctly),
  and two real bugs needing dedicated fix forks. FidBank UK's fix included a
  third recurrence of the known FX opening-balance spot-rate bug (after
  Zenith Bank UK and Union Bank of India UK) — worth treating as a
  standing checklist item on every FX-converted bank now, not just a one-off.

- [Batch 10](tickets/WF-010.md) — 4/5 built (FirstBank UK, Gatehouse Bank,
  Ghana International Bank, Goldman Sachs International Bank), 1 self-skipped
  (GB Bank Limited). First fully clean batch since WF-008 — no interruptions.
  GB Bank Limited's skip is a new flavor: an access-tooling stack (scanned
  filings + site 403 + in-session Wayback failure + exhausted WebSearch), not
  a legal exemption — worth revisiting with fresh tool budget. Goldman Sachs
  International Bank has a documented, recoverable Pillar 3 gap (8 of 11
  metrics live only in the parent's consolidated disclosure, unreachable this
  session). FirstBank UK is the first FX bank to need a brand-new rate derived
  from scratch rather than reusing the shared table.

- [Batch 11](tickets/WF-011.md) — 5/5 built (Griffin Bank, Guaranty Trust Bank
  UK, Gulf International Bank UK, Habib Bank Zurich, Hampden & Co), 0 skipped.
  A third session-limit termination hit mid-batch (4 of 5 forks killed,
  Griffin Bank had already finished); 3 of the 4 interrupted banks had nothing
  on disk and needed full fresh rebuilds, the fourth (Hampden & Co) had a
  genuine half-applied edit — a real sourced line item removed mid-fix and
  never restored — recovered by a dedicated fix fork. Also: a sandbox-level
  PDF fetch truncation (Gulf International Bank UK, worked around via
  qpdf/fitz repair) and a Nigerian-subsidiary bank breaking the expected FX
  pattern by reporting in GBP (Guaranty Trust Bank UK) — both new, one-off
  wrinkles rather than recurring patterns so far.

- [Batch 12](tickets/WF-012.md) — 5/5 built (Hampshire Trust Bank, Havin Bank,
  HBL Bank UK, HSBC Bank plc, HSBC Innovation Bank), 0 skipped. A fourth
  session-limit termination hit mid-batch (3 of 5 forks killed, HBL Bank UK
  and HSBC Innovation Bank had already finished); all 3 interrupted banks had
  nothing on disk and rebuilt cleanly, no false alarms or half-applied edits
  this round. HSBC Bank plc hit a genuine Companies House DNS-level outage,
  worked around via HSBC's own investor-relations site. Havin Bank's fork
  independently confirmed the Wayback Machine outage some WF-010 banks hit is
  a real Internet Archive-side outage, not session-specific.

- [Batch 19](tickets/WF-019.md) — 5/5 built, 0/5 skipped (OneSavings, Oxbury,
  Paragon, Perenna, and Persia International Bank; documented group/entity,
  disclosure, OCR, restatement, and FX limitations).

- [Batch 13](tickets/WF-013.md) — 5/5 built (HSBC UK Bank Plc, ICBC (London)
  plc, ICBC Standard Bank Plc, IFAST Global Bank, Investec Bank PLC), 0
  skipped. A fifth session-limit termination hit mid-batch (4 of 5 forks
  killed, ICBC Standard Bank Plc had already finished); all 4 interrupted
  banks had nothing on disk and rebuilt cleanly. HSBC UK Bank Plc and ICBC
  Standard Bank Plc were both unusually clean (0 WebSearch calls, everything
  on the bank's own site). Investec Bank PLC needed the heaviest OCR-
  equivalent transcription of the batch (all 5 Companies House filings fully
  scanned, ~35 pages read manually) and has a documented Pillar 3 access gap
  (LCR/NSFR/MREL only exist in a standalone Group-level report this session
  couldn't reach). ICBC (London) plc nearly self-skipped before finding the
  bank's correct domain. Note: a separate concurrent session ran WF-019
  through WF-023 in parallel — see the Notes entry above.

- [Batch 14](tickets/WF-014.md) — 4/5 built (2 full: Itau BBA International,
  Jordan International Bank; 2 Pillar-3-only: J.P. Morgan Securities, Julian
  Hodge Bank), 1/5 self-skipped (J.P. Morgan Europe Limited — double blocker,
  same pattern as Bank Of Baroda UK/Citibank UK/ICICI Bank UK). No
  interruptions this batch. J.P. Morgan Securities plc has a genuine,
  documented Pillar 3 access gap (only 2/5 years recovered — Companies House
  filing history and the Wayback Machine both unreachable this session) worth
  a revisit with fresh tool budget, not treated as a permanent gap.

- [Batch 15](tickets/WF-015.md) — 5/5 built (4 full: Kingdom Bank, Kroo Bank,
  Kuwait Finance House, Lloyds Bank Corporate Markets; 1 Pillar-3-only: KEXIM
  Bank UK), 0 skipped. A sixth session-limit termination hit mid-batch (4 of
  5 forks killed, Kroo Bank had already finished); all 4 interrupted banks
  had nothing on disk and rebuilt cleanly. Kuwait Finance House introduced a
  new pattern: a genuine mid-series conventional-to-Islamic banking
  terminology switch following its 2024 conversion (formerly Ahli United
  Bank UK). Kingdom Bank's obvious domain guess was an unrelated parked page
  (real site: kingdom.bank) — a new variant of the "site blocks fetches"
  failure mode. KEXIM Bank UK has a real, still-open Pillar 3 access gap
  (domain dead-ends + Wayback 429s) worth a revisit. This closes out this
  session's run (WF-013 through WF-015) — WF-016 through WF-025 were closed
  by a separate concurrent session; see the Notes entry above.

## Not yet specified

- The statistics/insights/PowerBI-integration map: destination, whether it targets
  real PowerBI (data export) or an in-house insights format (e.g. more artifacts
  like `Cross-Bank Trends Analysis.md`), and whether the ad hoc metrics-extraction
  script written for that first cross-bank analysis gets promoted into `scripts/`.
  Not sharp enough to ticket yet — chart a new map for it once WF-023 closes.
- Whether the "5 banks per ticket" batch size should change once more real-session
  data comes in on how many banks a single 5-hour budget actually gets through
  (nothing to decide yet — revisit after a few batches close).

## Out of scope

- Cloud/cron automation of session starts (RemoteTrigger routine hitting a GitHub
  repo at a fixed time) — considered directly, explicitly deferred in favor of
  manual session starts. Would require `git init` + a GitHub remote for this
  currently git-free project; revisit only if manual cadence turns out to be a
  real bottleneck.
- Promoting the cross-bank metrics-extraction script into a permanent `scripts/`
  tool — belongs to the future statistics map, not this one.

## Ticket index

| Ticket | Banks | Status |
|---|---|---|
| [WF-001](tickets/WF-001.md) | ABC International Bank Plc … ALLICA BANK LIMITED | closed |
| [WF-002](tickets/WF-002.md) | Alpha Bank London Limited … Atom Bank PLC | closed |
| [WF-003](tickets/WF-003.md) | Bank Mandiri (Europe) Limited … BANK OF CEYLON (UK) LIMITED | closed |
| [WF-004](tickets/WF-004.md) | BANK OF CHINA (UK) LIMITED … Bank Saderat Plc | closed |
| [WF-005](tickets/WF-005.md) | Bank Sepah International Plc … BROWN SHIPLEY & CO. LIMITED | closed |
| [WF-006](tickets/WF-006.md) | C. HOARE & CO. … Cater Allen Limited | closed |
| [WF-007](tickets/WF-007.md) | Charter Court Financial Services Limited … Coutts & Company | closed |
| [WF-008](tickets/WF-008.md) | Credit Suisse (UK) Limited … DB UK Bank Limited | closed |
| [WF-009](tickets/WF-009.md) | DF Capital Bank Limited … FidBank UK Limited | closed |
| [WF-010](tickets/WF-010.md) | FirstBank UK Limited … Goldman Sachs International Bank | closed |
| [WF-011](tickets/WF-011.md) | Griffin Bank Ltd … HAMPDEN & CO PLC | closed |
| [WF-012](tickets/WF-012.md) | Hampshire Trust Bank Plc … HSBC INNOVATION BANK LIMITED | closed |
| [WF-013](tickets/WF-013.md) | HSBC UK Bank Plc … Investec Bank PLC | closed |
| [WF-014](tickets/WF-014.md) | Itau BBA International PLC … Julian Hodge Bank Limited | closed |
| [WF-015](tickets/WF-015.md) | KEXIM BANK (UK) LIMITED … Lloyds Bank Corporate Markets Plc | closed |
| [WF-016](tickets/WF-016.md) | Lloyds Bank PLC … Metro Bank PLC | closed |
| [WF-017](tickets/WF-017.md) | Mizuho International plc … National Bank of Kuwait (International) Plc | closed |
| [WF-018](tickets/WF-018.md) | NATIONAL WESTMINSTER BANK PUBLIC LIMITED COMPANY … OakNorth Bank plc | closed |
| [WF-019](tickets/WF-019.md) | OneSavings Bank Plc … Persia International Bank Plc | closed |
| [WF-020](tickets/WF-020.md) | Punjab National Bank (International) Limited … RCI Bank UK Limited | closed |
| [WF-021](tickets/WF-021.md) | RECOGNISE BANK LIMITED … Santander Financial Services plc | closed |
| [WF-022](tickets/WF-022.md) | SCHRODER & CO. LIMITED … State Bank Of India (UK) Limited | closed |
| [WF-023](tickets/WF-023.md) | StreamBank PLC … Weatherbys Bank Limited | closed |
| [WF-024](tickets/WF-024.md) | GB Bank Limited … TD Bank Europe Limited | closed |
| [WF-025](tickets/WF-025.md) | Citibank UK Limited … THIS BANK LIMITED | closed |

This table is bookkeeping only, kept in sync manually — a ticket's frontmatter
`status` field is the source of truth if the two ever disagree.
