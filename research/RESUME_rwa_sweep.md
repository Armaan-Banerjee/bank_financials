# RWA sweep — Total RWAs sheet vs RWA Breakdown TOTAL divergences

Started 2026-09-15. Task: for 10 flagged bank-years, go to the primary source and
decide which of three outcomes applies (defect real / gap legitimate / breakdown wrong),
then write the conclusion into the build script.

Status legend: TODO / IN PROGRESS / DONE

| Bank | Year | Status | Outcome |
|---|---|---|---|
| Hampshire Trust Bank | FY2016 | DONE | 2 - documented, figure unchanged (credit-only proven, no total ever published) |
| Hampshire Trust Bank | FY2017 | DONE | 2 - same |
| KEXIM Bank (UK) | FY2024 | DONE | 2 - genuine Note 28 vs Pillar 3 basis difference, re-verified by OCR |
| Paragon Bank | FY2022 | DONE | 3 - breakdown (OV1) is the inflated one; Total RWAs sheet right; kept per own-edition rule |
| BNY Mellon (International) | FY2016 | DONE | 2 - Solo vs Consolidated, both printed side by side |
| BNY Mellon (International) | FY2017 | DONE | 2 - same |
| BNY Mellon (International) | FY2018 | DONE | 2 - same |
| Bank of Ceylon (UK) | FY2018 | DONE | 1 confirmed, NOT renumbered (no document states a total) |
| Bank of Ceylon (UK) | FY2019 | DONE | **1 - CORRECTED 23,604 -> 28,513** |
| Bank of Ceylon (UK) | FY2021 | DONE | **1 - CORRECTED 24,509 -> 29,052** |

Also corrected as a by-product: Bank of Ceylon FY2020 RWA Breakdown rows replaced derived
(/8%) values with the transcribed RWA column (34,473 / 187 / 4,188 / 38,848), which removes a
spurious 9k gap against the Total RWAs sheet.

Unit/currency work: `research/RWA_UNIT_CONSISTENCY.md` (7 banks; all internally correct in
their own declared unit; nothing converted).

## Log

### Hampshire Trust Bank — FY2016 & FY2017 — RESOLVED (documented, figure NOT changed)

Sources read (primary, downloaded and read directly):
- P3 2017 (https://www.htb.co.uk/htbcontent/uploads/2019/08/Hampshire-Trust-Bank-HTB-2017-Pillar-3-Disclosures-1.pdf)
  - p.4 "Summary of key ratios": `Risk weighted assets (£000) 529,157 (2016: 430,807)`
  - p.12 s4.2 credit-risk exposure-class table: RWAs column **foots to exactly 529,157**
    (Corporate 42,100 + Sec. by mortgages 67,276 + High risk 264,058 + Retail 142,500 +
     Defaults 6,229 + Central govts 0 + Institutions 2,233 + Other 4,763 = 529,157;
     Pillar 1 capital column 42,333).
  - p.13 "Capital resources requirement – Pillar 1": Credit risk 42,333 / Operational risk 3,136
    (2016: 34,464 / 1,189). Operational risk RWA = 3,136/0.08 = 39,200 (2016: 14,863).
  - p.11 Total regulatory capital 113,435. p.13 prints total capital ratio **21%**.
    113,435/529,157 = 21.44% -> 21%.  113,435/568,357 = 19.96% -> 20%.
    So HTB's own printed ratio uses the CREDIT-ONLY denominator.
- P3 2018 — DECISIVE structural proof: the same summary line prints
  `Risk weighted assets 687,497 (2017: 529,157)` while the COREP template row 010
  `Total risk exposure amount` on the same document reads **746,201**, and the COREP
  CET1 ratio is 16.31% (=121,690/746,201). Difference 746,201-687,497 = 58,704
  ~= operational risk RWA (4,677/0.08 = 58,463).
- AR 2017 p. (key-metrics table, line "Risk weighted assets (“RWA”) 529,157 430,807")
  and AR 2016 (430,807 / 157,455) repeat the same credit-only figures.

CONCLUSION: HTB's own headline "Risk weighted assets" line excluded operational risk RWA
in FY2016-FY2018 (proven by FY2018's COREP total sitting beside it). So the Total RWAs
sheet's FY2016/FY2017 values ARE credit-only. BUT no document HTB has ever published
states a FY2016 or FY2017 total risk exposure amount; the only candidate (445,663 /
568,363) is credit + (operational requirement / 8%), i.e. arithmetic. Under the
no-derivation rule the transcribed figure stays. Both sheets annotated as a resolved,
do-not-re-flag divergence, and the FY2017->FY2018 basis break is flagged.

Outcome: **2 (gap explained, figures unchanged)**, with the underlying credit-only
nature of the source line now proven rather than inferred.

### KEXIM Bank (UK) — FY2024 — RESOLVED (documented, figures NOT changed)

Primary source re-read: FY2025 Companies House filing (image-only scan; OCR'd page 88 of 88
via pdftoppm -r 200 + tesseract). The capital risk management note prints:
  `Capital, leverage and Risk Weighted Assets ('RWA')   Limit  2025   2024`
  `CET1 ratio 4.5  20.5%  20.9% / T1 6 20.5% 20.9% / Total capital 8 20.5% 20.9%`
  `Leverage ratio 5 16.9% 16.1%`
  `RWA (£)  517,644,568   488,424,781`
So the Total RWAs sheet's 488,424,781 is correctly transcribed from the statutory Note 28.
The RWA Breakdown sheet is the Bank's standalone Pillar 3 basis (492,924,960 for FY2024,
categories footing exactly). The bank publishes two different RWA figures for the same
year-end on two different bases and explains neither; Note 28's RWA is LOWER than Pillar 3's
while its ratio is ALSO lower, which is only possible if capital differs too - independent
confirmation of a real basis difference, not a subtotal error.
Both sheets already carried the basis note; added an explicit do-not-re-flag paragraph and
put the basis note on the Total RWAs sheet as well (it was only on the breakdown).

Outcome: **2 (gap legitimate, nothing changed)**.

### Paragon Bank — FY2022 — RESOLVED (documented, figures NOT changed)

Primary source: Paragon Banking Group PLC Pillar III Disclosures 30 September 2022
(Wayback: https://web.archive.org/web/20240830044143/https://www.paragonbankinggroup.co.uk/resources/paragon-group/documents/reports-presentations/2022/pbg_2022_pillar_iii_disclosures)

Inside that ONE document:
- UK OV1 row 29 "Total" = **7,645.8**  (row 1 credit risk excl CCR 6,763.3; row 6 CCR 249.9;
  row 23 operational 633.1)
- UK KM1 row 4 "Total risk-weighted exposure amount" = **7,515.0**
- own-funds template row 60 "Total risk exposure amount" = **7,515.0**
- IFRS 9 transitional template row 7 "Total risk-weighted assets" = **7,515.0**
- leverage section "Total risk exposure amount (£m)" = **7,515.0**

So 7,515.0 (what the Total RWAs sheet holds) is corroborated 4x; the OV1 total is the lone
outlier. Paragon's own printed FY2022 CET1 ratio 16.3% confirms it (1,221.8/7,515.0=16.26%;
vs OV1 it would be 16.0%).

Cause identified: the FY2023 edition's restated FY2022 credit-risk figure (6,632.5) is lower
than the originally-published 6,763.3 by exactly 130.8 — which is exactly OV1 row 7 "CCR - of
which the standardised approach" (130.8) — and 7,645.8 - 7,515.0 = 130.8 exactly. i.e. the
FY2022 OV1 double-counted the standardised CCR amount inside its credit-risk line. The FY2022
OV1 is sloppy elsewhere too (its own rows 1 vs 2 disagree for the 30 Sept 21 column,
6,186.1 vs 6,247.1; its CCR "of which" rows sum to 256.9 vs a printed 249.9).

This is the OPPOSITE of the Redwood/GHIB pattern — the Total RWAs sheet holds the complete
figure and the breakdown holds the inflated one. Per the standing restatement rule, each year
keeps its own contemporaneous edition, so nothing was renumbered; both sheets now carry the
finding.

Outcome: **3 (breakdown is the wrong one) — diagnosed and documented, deliberately not
renumbered because of the own-edition restatement rule.**

### Bank of New York Mellon (International) — FY2016/FY2017/FY2018 — RESOLVED (documented, figures NOT changed)

Primary sources: BNYMIL Pillar 3 Disclosures 2016 / 2017 / 2018 (bnymellon.com dam URLs in script).
Each prints BOTH RWA totals side by side in a two-column "Consolidated | Solo" table:
- FY2016 Own Funds table: `Total risk-weighted assets (RWA)  793  1,290  765  680`
  (793 Consolidated 2016, 765 Solo 2016)
- FY2017: `Total risk-weighted assets (RWA)  936  793  881  765`
- FY2018: `Total risk-weighted assets ('RWA')  1,233  936  1,211  881`
And the reason the breakdown exists on only one basis is stated in the documents themselves
(FY2018 p., repeated FY2017): "There is no material difference in the risk profile between
solo and consolidated and therefore Capital Requirements and Credit Risk Adjustments
information is only shown at the consolidated level."

Basis confirmed by the ratio sheets: CET1 412/765 = 53.9% (FY2016 doc prints Solo 53.9%,
Consolidated 51.9%); 448/881 = 50.8%; 618/1,211 = 51.0%. So Total RWAs + ratio sheets are all
Solo; the breakdown is Consolidated for FY2016-FY2019.

Entity-basis check: "Consolidated" is BNYMIL's OWN consolidation (FY2018 "Basis of
consolidation" table lists the Luxembourg Branch, BNY Trust Company Limited, BNY Mellon Trust
& Depositary (UK) Limited), NOT the parent group — so no rule-2 violation.

Changes: added do-not-re-flag paragraphs to both sheets' notes; corrected the RWA Breakdown
sheet subtitle, which wrongly read "Entity-level basis, £m." with no mention that FY2016-FY2019
are on the Consolidated basis.

Outcome: **2 (gap legitimate, nothing changed)** for all three years.

### Bank of Ceylon (UK) — FY2018 / FY2019 / FY2021 — DEFECT CONFIRMED (Redwood/GHIB pattern)

Primary sources (all downloaded and read directly from bankofceylon.co.uk):
BOCUK_Pillar 3 Disclosures 31 December 2018 / 2019 / 2020 / 2021.pdf

**FY2021 — s5.4 OWN FUNDS REQUIREMENT prints an RWA column, and its own rows are:**
```
Credit and Counterparty Credit Risk (exposure-class subtotal)   RWA 24,509   cap req 1,961
Market Risk                                                     RWA    302   cap req    24
Operational Risk Basic Indicator Approach                       RWA  4,241   cap req   339
Total Pillar 1 Requirement                                      RWA 29,052   cap req 2,324
Own funds                                                                         13,424
```
So **29,052 is PRINTED in the Bank's own RWA column** — a transcribed figure, not a derivation.
And 24,509 is printed in that same table as the credit-and-CCR subtotal. Section 4.1's
"Risk Weighted Assets 24,509" is therefore the credit subtotal.
(s4.1 also claims "The total for Risk Weighted Assets is the amount reported in the Bank's
regulatory returns" — a claim its own s5.4 contradicts.)
NOTE: BOC's printed FY2021 ratios use the credit-only denominator (CET1 13,424/24,509 = 54.77%
= the printed 54.8%), so unlike Redwood the ratio does NOT disprove the total here — the
same-document s5.4 RWA column does.

**FY2020 — same table, printed RWA column: credit 34,473 / market 187 / operational 4,188 /
Total Pillar 1 Requirement 38,848.** s4.1 prints RWA 38,848. So from FY2020 the s4.1 line IS
the full total — pattern confirmed as the script already said. ALSO: the workbook's FY2020
breakdown rows were DERIVED (34,463/188/4,188 = 38,839) when the document prints them
directly (34,473/187/4,188 = 38,848). Replaced derived with transcribed.

**FY2019 — the FY2019 document has NO RWA column at all** (s5.3/s5.4 are capital-requirement
only: credit 1,888 + market 7 + operational 335 = Total Pillar 1 Requirement 2,230). Its KM1
prints `Total RWAs 23,604` with `CET1 57.5%`, and 13,569/23,604 = 57.49%, so the FY2019
edition's own ratio agrees with the credit-only figure.
BUT the **FY2020 edition's s4.1 restates FY2019: `Risk Weighted Assets  38,848  28,513`** —
a directly-printed FY2019 total. (Consistent: the FY2020 edition also restates FY2019's
Pillar 1 requirement to 2,281 = credit 1,888 + market 77 + operational 316.)
This is exactly the GHIB precedent — corrected total transcribed from the following year's
edition. FY2019 -> **28,513**.

**FY2018 — the printed ratio DISPROVES the printed total, Redwood-style:**
FY2018 KM1 prints `CET1 capital 13,393`, `Total RWAs 24,492`, `CET1 ratio 46.9%`.
13,393 / 24,492 = **54.7%**, NOT 46.9%.  13,393 / 28,538 = **46.93% -> 46.9%** exactly.
(28,538 = that document's own Total Pillar 1 Requirement 2,283 / 8%.)
Cross-check that the KM1 line is normally a full total: the same table's FY2017 column reads
RWA 36,385 / CET1 36.5%, and 13,263/36,385 = 36.45% -> 36.5%, i.e. FY2017 is internally
consistent. FY2018 is where the line switched to credit-only (1,959/0.08 = 24,488 ~ 24,492).
BUT no BOC document anywhere prints a FY2018 total RWA figure — the FY2019 edition's
comparative repeats 24,492, and neither FY2018 nor FY2019 has an RWA column. 28,538 would be
a derivation, so under the no-derivation rule FY2018 is NOT renumbered; it is kept, flagged,
and the evidence recorded.

Outcome: **1 (defect real)** for FY2019 and FY2021 — corrected with transcribed figures.
**1-confirmed-but-no-transcribable-replacement** for FY2018 — kept and flagged.

---

## Extra check requested: other banks with mixed units WITHIN one sheet (the NBE §8b defect)

Scanned all 145 built workbooks programmatically for the National-Bank-of-Egypt signature —
one year's column on a Balance Sheet / P&L sitting ~1000x below the rest of the same row.

Two passes:
1. Any row on any sheet where one year is 300-4000x below the median of its other years:
   202 hits, essentially all genuine (a new bank's ramp-up years, or a cash-flow movement line
   that happens to be near zero in one year).
2. Narrowed to `Total assets` / `Total liabilities` / `Total equity and liabilities` /
   `Total income` rows with an adjacent-year jump of >=50x, which is the signature that
   separates a scale error from a startup ramp:
   - AFIN Bank FY2022 -> FY2023 x93  (licensed 2023 - genuine)
   - Atom Bank FY2016 -> FY2017 x67  (launched 2016 - genuine)
   - Kroo FY2022 -> FY2023 x262      (ramp - genuine)
   - Oxbury FY2020 -> FY2021 x183    (licensed 2021 - genuine)
   - StreamBank FY2021 -> FY2023 x113 (licensed 2023 - genuine)
   - The Bank of London FY2022 -> FY2023 x111 (launched 2022 - genuine)
   - **National Bank of Egypt (UK) FY2017 -> FY2021 x843** - the already-known §8b defect,
     and the ONLY hit that is an established bank rather than a start-up ramp.

**Conclusion: no additional mixed-units-within-one-sheet defect found.** NBE remains the
single instance, and it was left untouched as instructed.
