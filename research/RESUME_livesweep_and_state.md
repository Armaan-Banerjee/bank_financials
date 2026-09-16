# Live sweep results + session state at the 2am cut

Written 2026-09-16 ~02:0x, immediately after a session limit (resets **6am**
Europe/London) killed four agents mid-flight. Nothing below has been applied to
any build script. This is the only copy of the peer's sweep results.

---

## 1. LIVE SWEEP — complete, 1,191 URLs, full download + last-page test on each

### The headline answer
**ZERO truncations on the live web.** Not one row at exactly 1,048,576 bytes
anywhere in 1,191 live URLs. So the 1 MiB defect is purely a **Wayback capture
artifact**, not a live-web phenomenon. Established by checking the byte count of
every row, not by an empty results section.

The 95 files whose last page carries no text run from 176 KB to 24.8 MB (largest
a 50-page HKMA report) — image back-covers and scanned documents, the predicted
false-positive class, none of them truncation.

### Verdict counts
| Count | Verdict |
|---|---|
| 1,039 | OK_PDF |
| +5 | alive but initially misreported (TLS, see §4) → **1,044 serving real PDFs** |
| 95 | no text on last page (image back-cover / scanned) — **not** truncation |
| 27 | honest 404/410 → **only 7 actionable**, see §3 |
| 16 | blocked 403 (+1 unreachable) = **17 UNKNOWN**, never "dead" |
| 8 | soft-404s, all demoted as catch-alls |

---

## 2. SOFT-404 DETECTOR — an honest zero

**Zero published-then-removed leads across the entire live corpus.** All 8
soft-404s were demoted by the body-identity guard:
- `eabplc.com` ×4 — byte-identical 95,415 B bodies
- `qib-uk.com` ×4 — byte-identical 247 B bodies, **status 200** (the F5 WAF page;
  any status-only check reads it as success)

The WordPress attachment mechanism did not appear in this corpus. **Without the
guard, all 8 would have been shipped as published-then-removed leads and all 8
would have been false.** The detector is sound and found nothing here — a real
result for it, not a failure.

---

## 3. LINK ROT — ZERO GENUINELY NEW (corrected 2026-09-16, ~06:0x)

**All 27 honest 404s are deliberately-documented dead originals. There is no new
link rot anywhere in the corpus, and NO ACTION IS REQUIRED HERE.**

20 were recognised immediately, because their constant names say so
(`P3_2019_DEAD`, `P3_FY2020_DEAD_URL`, `P3_2021_OLD_URL`, `P3_DEAD_URL_NOTE`):
FirstBank ×6, Kingdom ×4, Methodist ×5, Rathbones, Redwood, TSB, UBA, UTB.

~~The seven new ones are all Shawbrook, cited from plain literals with no
dead-marker.~~ **WRONG — withdrawn.** The remaining seven are Shawbrook and they
are documented too, just in a shape the dead-marker filter did not recognise.
`scripts/build_shawbrook.py:34-41` holds them in a dict named **`P3_DEAD`**,
under the comment *"Dead originals, retained for provenance - do NOT delete"*,
with a `LINK_PROVENANCE` block rendering each DEAD→LIVE substitution into the
workbook. The live replacements were **already in `P3` (lines 24-28)** before
this sweep ran; the peer's seven recommended swaps were all already applied.

**The filter's blind spot, worth fixing before it is re-run:** it matched
dead-markers in the NAME OF A SCALAR CONSTANT, so it missed a **dict named
`P3_DEAD` keyed by year**, where the marker sits on the container and the
entries are plain string literals. Check the enclosing assignment target, not
just the immediate one.

Verified directly before this correction was written: `cc5dq5j0/pillar-3-2014.pdf`
200/2,077,440/`e2f9d46c…`, `vypjeoat/pillar-3-2018.pdf` 200/1,500,212/`3bdffb59…`,
`yhdl0kcs/pillar-3-2019.pdf` 200/4,059,311/`0b1615e7…`, and the old
`kfnfg0oe/shawbrook-pillar-3-disclosures-2018.pdf` an honest 404.

**One real improvement still outstanding**: `yhdl0kcs/pillar-3-2019.pdf` has
served **two distinct CDX digests**, so that citation should be pinned to md5
`0b1615e7c61eee2da3ee0f3bb2a1beea`, which the script does not yet record.

`/media/<hash>/` paths are Umbraco-style and cannot be permuted — the same wall
as Aldermore — but that never came into play here.

---

## 4. TLS FAILURES MISREAD AS LINK ROT — 5 LIVE DOCUMENTS NEARLY LOST

Six URLs came back "ARCHIVE_UNAVAILABLE". All six were **TLS failures**
(curl rc=60 / rc=35), not link rot. Retried with `-k`:

- **banksepah.co.uk ×5 — ALL ALIVE**: 200 `application/pdf`, 31–32 pages each
  (Pillar 3 at 31 March 2021, 2022, 2023, 2024, 2025)
- persiabank.co.uk ×1 — still unreachable even with `-k`; **BLOCKED/unknown, not dead**

The peer's note on this is worth preserving verbatim in spirit: the fix was
*already written in their own notes* ("an expired TLS certificate is not link rot,
retry with -k, e.g. banksepah.co.uk") and the verifier simply did not pass the
flag. **"I have written this down" is not the same as "the tool does this."**

---

## 5. ASK 3(b) CONTEXT RE-ANALYSIS — 17 of 103 flagged, most false positives

Re-ran all 107 assertions capturing previous sentence, following sentence and
containing heading (no re-fetch needed). **The flag is a REVIEW marker, not a
verdict.**

**Genuinely off-topic (remuneration, not capital):**
- Vanquis FY2021 (the disproof, see `project_pillar3_transcription_traps`)
- **FCE Bank FY2018/FY2019/FY2020** — "the RemCo reviewed and approved the bank's
  Pillar 3 disclosures **regarding remuneration**, which were published to the
  bank's website"

**False flags (the capital document, flagged only on a word):**
- Crown Agents ×4 — "PRA Pillar 3 **capital adequacy** disclosure requirements…
  including remuneration"
- OakNorth FY2020 — "the Pillar 3 disclosures, **including** disclosures on
  remuneration policy"
- Charity Bank FY2023 — flagged because "Climate risk" is the NEXT heading
- Co-op FY2014 — flagged on "Task Force" (EDTF)

**Ambiguous, needs a human read:**
- Hampshire Trust FY2016/FY2017/FY2020 and Zopa FY2023 — "Information on the
  Bank's Remuneration Code is set out in the Pillar 3 disclosures and will be
  published on our website". Remuneration-framed, but each still asserts a
  Pillar 3 document is published.

**86 of 103 carry no off-topic context at all** — the PUBLISHED set is in better
shape than the Vanquis case suggested.

### NEW CATEGORY — Pillar 3 EMBEDDED IN THE ANNUAL REPORT
FCE Bank FY2018 and FY2019 also say: *"This **chapter** contains the remaining
Pillar 3 disclosures required by Part Eight of the CRR not already disclosed
elsewhere"*. **FCE embeds its capital Pillar 3 inside the annual report** rather
than publishing a separate document.

That is neither "published separately" nor "not disclosed". A search for a
standalone FCE Pillar 3 PDF **would fail forever** while the disclosures sit in a
document this project already holds. Worth checking for at other banks.

Peer's files: `live_report_final.txt`, `ar_context.jsonl`,
`research/cited_urls_v2.tsv` (+ README), `research/nd_targets.json`,
`research/nd_classified.json`, `research/nd_targets_README.md`.

---

## 6. AGENTS KILLED AT THE 2am LIMIT — resume points

All four have checkpoint files; **re-read them and reconcile against `git diff`
before continuing**, since the user commits mid-session.

| Agent | Last words | Checkpoint |
|---|---|---|
| Corpus-wide arithmetic tie-out | "Confirmed: two defects in NatWest's FY2020 column. Let me locate and fix the build script." | `research/RESUME_tieout_sweep.md` |
| Comparative-column backfill | "Now making the Monzo edits." | `research/RESUME_comparative_sweep.md` |
| OneSavings solo LCR | "Now let me write the checkpoint file…" (barely started) | `research/RESUME_onesavings_solo_lcr.md` |
| Hoare + BNY Mellon | "Now the MREL note and the Overview copies." | `research/RESUME_hoare_bny.md` |

---

## 7. OUTSTANDING — needs the user

1. **Cater Allen** — four `RWA_CALC` values are capital ÷ CET1 ratio. Recommend withdraw.
2. **Kuwait Finance House** — Total RWAs back-solved (Own Funds ÷ Total Capital ratio). Recommend withdraw.
3. **Persia FY2015 ratios** (68.94% / 47.92%) — proven to use a credit-only denominator, so overstated (~64.4% / ~44.8%). Withdraw or leave flagged; **not** recompute. *(Unaffected by the FX fix — ratios are scale-invariant, zero percentage cells moved.)*
4. **"Declared group basis"** — Vanquis, OneSavings, ClearBank (FY2023+) and Arbuthnot's Pillar 3 sheets carry openly-labelled parent-group figures. Withdrawing them is a project-wide editorial call with coverage-denominator and `insights.db` consequences.
5. **Corpus OCR** — 577 of 1,127 documents unread, 50 banks entirely unread. Not the cheap job first reported.
6. **MREL reclassification (372 bank-years)** — needs a rule mapping BoE resolution-entity status to UK subsidiaries. Does **not** move the coverage % (MREL already excluded); it is a deliverable-quality fix.

## 8. ~~MUST RUN WHEN AGENTS FINISH~~ — DONE 2026-09-16 06:42

`python3 scripts/insights/refresh_all.py` ran clean: all 22 steps, 145 banks,
122,526 metric rows, 302 deliverable pages regenerated.

**A trap found on the way in, worth keeping.** Step 1 (`extract_metrics.py`)
reads the **workbooks**, not the build scripts — so a corrected script whose
workbook was never rebuilt feeds STALE figures into a refresh that reports
success. Four scripts were in exactly that state, and they are precisely the
four agents killed at the 2am limit, each leaving a complete edit that had never
been built:

| script | workbook was behind by | agent |
|---|---|---|
| `build_monzo.py` | 200.4 h | comparative-column backfill |
| `build_onesavings.py` | 200.3 h | OneSavings solo LCR |
| `build_bny_mellon.py` | 5.3 h | Hoare + BNY Mellon |
| `build_national_westminster_bank.py` | 0.8 h | corpus tie-out sweep |

All four were checked for truncated edits (every script in the repo parses; no
conflict markers; no note-constant defined-but-never-referenced), then rebuilt,
and only then was the refresh run. **Always compare each build script's mtime
against its own workbook before refreshing.**

Verified in the refreshed DB rather than trusting the exit code: Persia FY2025
total assets **129,947.7** (the FX fix), NatWest FY2020 loans **238,366** and
customer deposits **255,290** (the tie-out agent's two corrections).

Pre-existing and NOT touched: `AR_2022_URL` in `build_onesavings.py:14` is
defined and never referenced (committed 2026-09-08, not agent residue) — wiring
it into a citation without establishing that it is the right source would be
inventing provenance.

## 9. OPEN DEFECTS, ticketed not fixed
- **JP Morgan Securities** — RWA Breakdown in US$'000 while Total RWAs is converted; the two sheets don't foot, by exactly the FX rate. Both labelled, neither warns.
- **ABC International** FY2023 differs by £3.566m between sheets while the subtitle claims all years match within rounding.
- **Metro** MREL wrong FY2022–FY2024 (documents print 17.7%, 22.0%, 23.0%; sheet says "Not disclosed").
- **Aldermore** RWA Breakdown headers read "(£'000)" while data and subtitle are £m.
- **Reliance** Total Capital Ratio FY2023 25.5% / FY2022 19.7% are derived (declared as such on the sheet), appearing in no document.
- **Overview note row height** hardcoded at 45 in `bank_workbook.py`; GIB's note is ~3,700 chars and displays clipped. Fixing touches all 145 banks.
- **`_labels` dict keyed on row caption** collapses duplicate captions (balance sheets carry "Derivative financial instruments" twice) — live in 3 scripts using the post-hoc pattern.
