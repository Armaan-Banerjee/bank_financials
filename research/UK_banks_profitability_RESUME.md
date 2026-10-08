# Profitability (ROE/ROA) work — cold-resume state, 2026-10-08 ~20:10 BST

Written because the session is near its usage limit. Everything needed to pick
this up with no memory of the conversation is here.

## What exists and how to rebuild it

```bash
S=/private/tmp/claude-501/-Users-armaan-code-katalysis/20f20984-c24d-413e-b487-68c0d0793341/scratchpad
/usr/bin/python3 research/build_profitability_table.py    $S/prof.json
/usr/bin/python3 research/build_profitability_workbook.py $S/prof.json $S/thebanks_eu.jsonl \
    "research/UK_banks_profitability_$(date +%Y-%m-%d)"
```

- `research/build_profitability_table.py` — extracts profit after tax, profit
  before tax, total comprehensive income, total equity, total assets from all
  145 `banks/*.xlsx`. Writes JSON. **Reads workbooks; writes none.**
- `research/build_profitability_workbook.py` — assembles the CSV + XLSX.
- `research/UK_banks_profitability_2026-10-08.{csv,xlsx}` — the deliverable.
  11 sheets: Read me, ROE, ROE year-end, ROA, Detail, Definition resolver,
  Vs thebanks.eu, Period and entity flags, Ratio caveats, Vs prior research,
  Gaps, Unmatched inputs.
- `$S/thebanks_eu.jsonl` — 50 aggregator figures, all FY2024. **If the
  scratchpad is gone this is lost**; re-collecting means WebSearch with
  `allowed_domains:["thebanks.eu"]` (the site itself is behind a Cloudflare
  CAPTCHA — do NOT attempt to bypass it).

**No bank workbook has been modified by any of this work.** The 23 modified
files in `banks/` are from the earlier ICBC and GA-025 tasks.

## Coverage as built

145 banks x FY2021-FY2025 = 725 bank-years. ROA 708, ROE year-end 703, ROE
average-equity 648. 144/145 banks matched; only CITIBANK UK fails (no separate
equity line in its balance sheet — genuine, known).

## User decisions already applied

1. **ROE caveats excluded** from the ROE sheets (9 bank-years, near-zero or
   sign-changing equity). Kept on the Ratio caveats sheet with the equity base.
2. **ROA extremes are flagged, NOT excluded** — total assets never crosses
   zero, so those ratios are well-defined, just huge for pre-operational banks.

## Where the analysis got to

54 divergences against the two outside sources, classified automatically by the
**Definition resolver** sheet: 12 RESOLVED, 13 explained by their own measure
label, 14 within 0.5pp, **14 genuine leads**.

**CLOSED — Al Rayan, all four years.** The prior research file's "ROE" is struck
on profit BEFORE tax: FY2025 23,587/225,238 = 10.47 (they say 10.47); FY2024
23,469/205,806 = 11.40 (11.40); FY2022 20,797/162,313 = 12.81 (12.82); FY2021
6.26 (6.26). Nothing wrong on either side; the label omits "before tax".

Also auto-resolved: Lloyds (total comprehensive income / average equity = 7.13
vs their 7.11), Monzo (pre-tax / closing equity), Metro FY2024, Bank of Ceylon,
Charter Court, HSBC Bank plc, Starling's ROA (TCI / assets = 1.68 vs 1.69).

**Known limit:** RoTE and any tangible-equity measure CANNOT be tested, because
intangibles are not extracted. Metro's -23.00 RoTE and Shawbrook's Underlying
RoTE are "explained by label" only — the arithmetic has not been reproduced.

## The 14 open leads

UNITED TRUST BANK (FY2021-FY2024, incl. the +20.74pp thebanks.eu case),
COUTTS (FY2024, FY2025), ALDERMORE (FY2022, FY2023, FY2025), NORTHERN BANK
(FY2024), STARLING (FY2024), AIB GROUP UK (FY2024, 0.62pp).

Established and worth not re-deriving:
- **United Trust**: their ROA nearly agrees (1.79 vs 1.68) while ROE is ~2x, so
  the difference is the EQUITY denominator (~GBP 172m implied against our
  362,862). Note FY2020 equity was 174,036 — a stale denominator is a candidate.
- **Northern Bank**: the AT1 theory is DISPROVED. Their leverage multiple
  (ROE/ROA = 15.00) nearly matches ours (15.45); excluding the GBP 226,526k AT1
  would give ROE 23.30 and a multiple of 20.4. Both their denominators are
  11-13% below ours; cause unknown. Also: the research file's 19.8 and
  thebanks.eu's 19.80 are the SAME source, not two.
- **Starling**: 31 March year-end, so an outside "2024" is ambiguous.

## Three subagents were running when this was written

Each was told to checkpoint after every figure and to keep a cold-resume file:
- United Trust Bank -> `$S/utb_roe.jsonl`, `$S/utb_roe_RESUME.md`
- Coutts / Aldermore / Lloyds -> `$S/coutts_aldermore_lloyds.jsonl` + `_RESUME.md`
- Al Rayan / Northern / Starling -> `$S/alrayan_northern_starling.jsonl` + `_RESUME.md`

**If they did not report, check those files before re-dispatching** — and note
Al Rayan is already closed, so that agent's remaining value is Northern and
Starling only.

## Standing rules these outputs obey

Never back-solve. Three sources (computed / prior research / aggregator) stay in
three columns and are never merged or averaged. Group and parent figures are not
the UK entity's. A missing input leaves an EMPTY cell, never a zero. Period and
entity anomalies live only in the column header, so they are reproduced verbatim
on the Period and entity flags sheet.

## Known defects fixed in the extractor (do not reintroduce)

1. Matching only `profit|surplus` dropped **every loss-making bank**.
2. Taking the first row with a year in it locked onto the SUBTITLE (Recognise
   Bank's opens "FY2025-FY2026 ..."), treating column 0 as data. Header
   detection now scores candidates and never accepts column 0. In another
   layout this would mis-assign figures to the wrong year SILENTLY.
3. Rank ties must break on year coverage: Bank Sepah has both "Total assets"
   and "Total assets (FY2026 presentation)", and the latter cost all five years.

---

# UPDATE ~20:45 BST — all three subagents KILLED by the session limit (resets 22:10)

The per-figure checkpointing instruction was sent ~15 minutes before the kill and
it worked: all three left verified findings on disk. **Do not re-dispatch from
scratch** — read `$S/utb_roe.jsonl`, `$S/coutts_aldermore_lloyds.jsonl` +
`_RESUME.md`, `$S/alrayan_northern_starling.jsonl` + `_RESUME.md` first.

## CLOSED against primary documents

**AL RAYAN — confirmed by the bank's own words, not just arithmetic.** AR2024
printed p.9 KPI table publishes "Return on equity 11.40%" and states the
definition outright: *the ratio of profit for the year BEFORE TAX to AVERAGE
equity*. That is the bank's own figure, and the prior desk research simply
copied it. 23,469/205,806 = 11.404%. The offset from our 8.61% is exactly the
tax charge over average equity (5,752/205,806 = 2.795pp). FY2024 inputs verified
digit-for-digit at 300 dpi. FY2025 KPI table reads 10.47% with the same wording.

**LLOYDS BANK — fully explained, and MY EARLIER AUTO-RESOLUTION WAS WRONG.**
The Definition resolver matched it as "total comprehensive income / average
equity = 7.13 vs their 7.11" — that was a COINCIDENCE. The real cause, verified
on 300 dpi images of the ARA 2024: thebanks.eu mixes bases within one ratio.
Numerator = GROUP consolidated profit 3,486 (printed p.75). Denominators =
BANK-only unconsolidated figures from printed p.145: assets 430,252 (2023
419,441), equity 51,688 — and its 2023 equity comparative is the Bank-only
SHAREHOLDERS' equity 46,348, a different definition again. Both reproduce
exactly: 3,486/avg(430,252;419,441) = 0.8205%; 3,486/avg(51,688;46,348) =
7.1117%. Our figures are right; theirs is a cross-basis artefact.
**LESSON: the resolver can produce a spurious match. A combination that
reproduces a figure to 0.02pp is a HYPOTHESIS, not a finding, until a document
confirms it.** Lloyds Bank plc publishes no ROE/RoTE/ROA at all (full-text
search of ARA 2024 and 2025); only Lloyds Banking Group plc does.

**COUTTS — entity mismatch.** The 21.7% is NatWest Group's PRIVATE BANKING &
WEALTH MANAGEMENT SEGMENT RoE for FY2025, not the Coutts & Company legal
entity. Coutts' own ARA 2025 prints "Return on Equity (RoE) 17.3%", close to
our computed 17.03%. (OCR only — still needs 300 dpi verification and the
footnote definition.)

**ALDERMORE — entity mismatch.** The 7.7% is ALDERMORE GROUP PLC consolidated
for y/e 30 June 2025 (group PBT 193.5, PAT 141.1), not Aldermore Bank plc solo
(PBT 220.7, PAT 163.2). Confirmed at press-release level; AR page and definition
still to pull.

**UNITED TRUST BANK — the prior desk research has its YEARS TRANSPOSED.** UTB
publishes its own ROE every year: FY2021 20.2%, FY2022 21.7%, FY2023 23.9%,
FY2024 20.1%, FY2025 14.1%, defined as average equity NET OF THE COUPON ON
CONTINGENT CONVERTIBLE SECURITIES. The research file's "FY2023 = 20.20" is
UTB's published FY2021, and its "FY2021 = 23.90" is the published FY2023. Our
computed FY2023 (23.48) sits against published 23.9 and our FY2021 (19.16)
against published 20.2 — both consistent once the CCS coupon deduction is
allowed for.

## STILL OPEN

**UTB FY2024, thebanks.eu 40.59% — unresolved, and two hypotheses are now DEAD.**
Their ROA 1.79% is reproduced as profit / AVERAGE assets (65,772/3,676,714 =
1.789%), and their stated total-asset growth of 13.75% matches UTB Limited's
entity assets EXACTLY (3,913,260/3,440,168), so they are on the right entity
with the right numerator. But 65,772/0.4059 implies equity of 162,040, which
matches nothing: not UTB Ltd equity (362,862 = share capital 10,350 + premium
25,680 + AT1 16,851 + retained 309,981), not ex-AT1 (346,011), and NOT the
group — UTB Partners Plc consolidated total capital and reserves is 365,019.
**The group hypothesis is disproved.**

**NORTHERN BANK FY2024 — our inputs are CONFIRMED digit-for-digit** at 300 dpi
(Northern Bank Limited, company R0000568, unconsolidated balance sheet, printed
p.129; profit 165,495, equity 943,995/929,341, assets 14,474,391, AT1 226,526,
TCI 169,665). Their 19.80/1.32 still unexplained.

**STARLING FY2024** — not reached.

## DEFECT FOUND INCIDENTALLY IN A DELIVERED WORKBOOK — needs a decision

`banks/ALDERMORE FINANCIALS.xlsx`, Balance Sheet, **FY2025 "Total liabilities"
reads 17,050.8 but should be 19,103.6**. Verified two independent ways: the
liability line items sum to 19,103.6, and total assets minus total equity
(20,618.2 - 1,514.6) is also 19,103.6. FY2024 (18,823.7) and FY2023 (17,832.7)
both tie exactly, so it is the FY2025 cell alone — a 2,052.8 transcription slip.
The "Total liabilities and equity" row is correct at 20,618.2.
**Not fixed**: fixing means editing the build script, rebuilding and running all
four checks, and the user commits. Nothing in the ROE work depends on it (ROE
and ROA use profit, equity and assets, none of which is affected).
Hint as to origin, NOT a conclusion: the FY2025 "Customers' accounts" line is
17,047.6 — only 3.2 away from the 17,050.8 in the total cell, which suggests the
transcription landed on or near the wrong row. The document settles it, not this.
The script's own long series makes the figure implausible on its face too: it has
liabilities FALLING 1,772.9 (18,823.7 -> 17,050.8) in a year when assets ROSE
422.7 (20,195.5 -> 20,618.2). Cell: `scripts/build_aldermore.py:440`.

**Check-axis gap this exposes:** `verify_workbook.py` reconciles DATA blocks to
TOTAL rows on the CASH FLOW sheet only. It never sums the Balance Sheet or P&L,
so a wrong subtotal there passes silently — as this one has. Aldermore's verifier
output is "1/4 DATA-block checks passed" purely on cash-flow rounding noise and
says nothing about the balance sheet. Worth a GA- ticket.
