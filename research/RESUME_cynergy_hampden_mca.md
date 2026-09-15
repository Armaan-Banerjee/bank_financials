# Resume checkpoint — Cynergy / Hampden / Methodist Chapel Aid

Started 2026-09-15. Update after each bank, not at the end.

---

## 1. CYNERGY BANK PLC — `scripts/build_cynergy_bank.py`

### Contentful enumeration (THE key result)

Command run 2026-09-15:

```
curl -sL https://www.cynergybank.co.uk/strong-and-prudent-management \
  | grep -o 'assets\.ctfassets\.net[^"'"'"' ]*' | sort -u
```

Full output (15 assets, space `xzmqg68ot16t`):

| Asset | Doc |
|---|---|
| `1vXCr68vBHhYVYZK6AXrFy/d6276c26bf68de097c5c3a2605356ad5/gender-pay-gap-report-2020.pdf` | GPG 2020 |
| `2l0o6Ki3Jh8F4ZRJDZLmY8/93d723e3ba41d7f866b4000d09702b05/gender-pay-gap-report-2017.pdf` | GPG 2017 |
| `2v6FmkY7vFJwKVYPsdkTkg/2c74d882695a4854e99edf9a78ac6b00/cynergy-bank-pillar-3-2021.pdf` | **P3 FY2021** |
| `3m32VZMQssjUtTQ5Qbee2i/650adad10a21eb80683613a032bb9428/gender-pay-gap-report-2018-docx.pdf` | GPG 2018 |
| `3qKJzsAiu3dGAA2EQBSzPo/bbb85f662bef802d29fb7144d087c761/cynergy-bank-2022-pillar-3-disclosures.pdf` | **P3 FY2022** |
| `4bBxZIPpOo5bbLcKHWYEUm/fcd9cdd11b86ea543870c4278d798a22/Cynergy_Bank_Gender_Pay_Gap_Report_2023-Final.pdf` | GPG 2023 |
| `4pIQEYRVfpbybsjGR5dSSg/c079e7a7976ab21b64ee0d11d7ff3305/gender-pay-gap-report-2022.pdf` | GPG 2022 |
| `5lTzyJuIg2zRrc7GGyH6Gv/6eb39217d6164e649f946b7aed50a0cb/Cynergy_Bank_Pillar_3_Disclosures_2023.pdf` | **P3 FY2023** |
| `5VXZDjR2zbmfVLacUjaf8c/.../FSCS_..._2025.pdf` | FSCS sheet |
| `6cr6h8Swx5thOBkCOc8Z2Q/e3b2a8d44a4d8015fa09c6806662144b/pillar-3-disclosures-2018.pdf` | **P3 FY2018** |
| `6QU51x2uOfJrvTvWQXqjBb/8c8355dd5958036c3ca36b844b5d2f3e/gender-pay-gap-report-2019.pdf` | GPG 2019 |
| `6UrOmWW2bF1uUTP86Lupt7/a760004278eda1c2d8508479499a3200/pillar-3-disclosures-2020.pdf` | **P3 FY2020** |
| `7szQ9puHAozWh6f8VVeSUq/b3f0c659a7773d61f0ef2e51c1025d1e/Gender_Pay_Gap_Report_Final_2026.pdf` | GPG 2026 |
| `7xhQZUsoPzNA5JIdWVpMKl/c393ea48db3ae4dbd6e74f51926a8cff/pillar-3-disclosures-2019.pdf` | **P3 FY2019** |
| `ucwNaCvmz2BIQddjoIpoN/edc29ba1199dde15898c03d0753f9e21/Gender_Pay_Gap_Report_2024_Final.pdf` | GPG 2024 |

**CONCLUSION: Cynergy publishes Pillar 3 for FY2018–FY2023 ONLY. There is no
FY2024 and no FY2025 Pillar 3 disclosure.** This is an *enumerated* negative,
not a failed search: the page is current (it carries a Gender Pay Gap report
dated 2026), so the absence is meaningful.

Note the hash segment differs from the URLs in RESUME_SESSION.md for the FY2021
and FY2023 files (Contentful re-publishes change the hash); both old and new
hashes resolve.

### THE BIG CORRECTION

`build_cynergy_bank.py` contained two long, confident notes concluding that the
**FY2023 Pillar 3 did not exist / could not be reached**, the second describing
itself as a "maximum-effort sweep" over "four independent routes, all negative".
**That was wrong.** The FY2023 Pillar 3 is live:
`https://assets.ctfassets.net/xzmqg68ot16t/5lTzyJuIg2zRrc7GGyH6Gv/6eb39217d6164e649f946b7aed50a0cb/Cynergy_Bank_Pillar_3_Disclosures_2023.pdf`

Why the earlier routes all missed it (reusable failure mode):
1. It is linked from **exactly one page**, `/strong-and-prudent-management`.
   The earlier passes enumerated `/about-us/company-performance` and
   `/document-library`, which genuinely don't list it. Each negative was
   individually accurate and collectively wrong.
2. The claim "the Contentful space exposes exactly 15 PDFs, every one an Annual
   Report" was an artefact of enumerating *one rendered page*. A Contentful
   space is not enumerable from any single page: company-performance's asset set
   is 15 Annual Reports; strong-and-prudent-management's is a *different* 15
   assets containing six Pillar 3 editions.
3. Wayback CDX of cynergybank.co.uk could never have found it — the FY2023
   edition never lived on the old `/media/` tree, only on assets.ctfassets.net.

### Entity check — PASSES
- FY2023 P3 cover/intro names **"Cynergy Bank Limited, PRA firm reference
  number 575105"**.
- AR2024 and AR2025 both give **company number 04728421**; AR2025 p.3690: "Cynergy
  Bank plc is a public limited company registered in England and Wales (company
  number 04728421)". AR2024 uses the same number.
- Same company number + same FRN ⇒ same legal entity, re-registered Limited→plc.
  The annual reports and the Pillar 3 are usable together.

### Figures written (all from the 2023 Pillar 3, UK KM1 p.7 / UK OV1 p.8 / CC1 p.9)
| Sheet | FY2023 |
|---|---|
| CET1 Ratio | 14.69% |
| Tier 1 Ratio | 14.69% |
| Total Capital Ratio | 15.41% |
| Total RWAs | 2,084,246 |
| Leverage Ratio | 6.96% (exposure measure 4,398,669) |
| LCR | 304.44% |
| NSFR | 148.67% |
| RWA Breakdown | credit 1,905,000 (of which securitisations 13,000), CCR 0, operational 179,000, total 2,084,000 |

Overview sheet updated to match (it is a separate copy).

### Validation gate — PASSED
2023 edition's FY2022 comparative reproduces the workbook exactly on capital,
RWA, ratios and leverage: CET1 287,447 / Tier 1 287,447 / Total capital 287,447 /
RWA 1,822,159 / CET1 15.78% / TCR 15.78% / leverage 7.40%. CC1 also confirms the
FY2023 capital amounts already held (306,251 / 321,251). **Nothing overwritten.**

### TRAP FOUND — FY2022 liquidity restatement, NOT reconciled
2023 edition's FY2022 comparative disagrees with the 2022 edition on liquidity
**only**: LCR 249.66% vs 315.98%; NSFR 144.09% vs 149.48%. Components restated
too (HQLA 525,228 vs 602,317; net outflows 212,745 vs 190,621; ASF 3,546,316 vs
3,721,028). **Not** the average-vs-point-in-time trap — both editions label the
HQLA input "Weighted value - average". Genuine inter-edition restatement.
FY2022 keeps its own edition's 315.98% / 149.48%; both documented on the sheets.

### FY2024/FY2025
Stay blank. Enumerated structural absence (SDDT Rule 3.1, approved 17 Jan 2025 —
already evidenced in the script from both ARs and the PRA waivers register), now
backed by the Contentful enumeration above rather than by a failed search.

### Also fixed
7 occurrences of literal `%%` inside plain/f-strings in this script, which
rendered as "13.59%%" in the workbook's source notes. Other build scripts use a
single `%`.

### Status
- [x] Enumeration done
- [x] Entity check (Plc vs Limited) — same company 04728421, same FRN 575105
- [x] Figures written and workbook rebuilt (18 sheets)

---

## 2. HAMPDEN & CO PLC — `scripts/build_hampden_co.py` — DONE

### Rename recorded in the script (was the explicit ask)
Added a large header block above the P3 URL constants. Key content:
- hampdenandco.com → **www.hampdenbank.com**. The old domain is a redirect shell
  (all three old P3 URLs 301 through and resolve 200), but it is NOT the live
  host and gets no new Wayback captures — do not conclude anything from a CDX
  sweep of it.
- Live indexes: `https://www.hampdenbank.com/investors` (primary) and
  `https://www.hampdenbank.com/about-us/shareholder-information`.
- Two interchangeable live document hosts:
  `https://www.hampdenbank.com/content/hampden/content/<file>` and
  `https://cdn.craft.cloud/019db931-.../assets/content/hampden/content/<file>`.
- The P3 URL constants for 2019/2021/2022 were repointed from hampdenandco.com
  to the live hampdenbank.com host via a new `P3_HOST` constant.

### FY2024/FY2025 Pillar 3 — enumerated negative CONFIRMED (re-run independently)
1. Scraped every PDF href from `/investors`: 16 documents — ARs 2017-2025 (2025
   in two variants), 2 Articles of Association, AGM pack, privacy notice, Jun-26
   factsheet, and **exactly one Pillar 3 (2023)**.
2. `/about-us/shareholder-information` scrape returns the identical single P3
   href — the two pages agree, neither is stale.
3. 10 FY2024/FY2025 filename candidates × 2 live hosts = 20 requests, **all 404
   with an identical 9-byte body**; control request for the 2023 edition on both
   hosts returned a real 426,753-byte PDF each. So the 404s are real, not a block.
4. Re-read both ARs full-text: **no RWA, no leverage, no LCR, no NSFR, no GBP
   capital amount anywhere.** Note 31 is narrative in both. Only capital figure
   in either is the KPI Total capital ratio: 17% (FY2025), 17% (FY2024) — already
   in the workbook. **Nothing new to fill from the annual reports.**

Backed by the already-documented PRA **Rule 3.1** SDDT modification, FRN 606934,
start **25/04/2024**, no end date, against a 31 December year-end.

### INCIDENTAL TRAP worth carrying to other banks
The 2019, 2021 and 2022 P3 editions still serve **HTTP 200 from both live hosts
even though neither index page links them any more.** Absence from an index page
is therefore NOT evidence of withdrawal at this bank. That is exactly why the
FY2024/FY2025 negative rests on the 404s + the Rule 3.1 date test, not the index.

### Cells actually changed
- **NSFR FY2016-FY2021 → "Not applicable"** (6 cells, detail sheet + Overview).
  Structural: UK had no NSFR requirement or disclosure template before
  1 Jan 2022 (PRA PS17/21 / PS22/21). Standing rule 7 — previously blank, so
  indistinguishable from an unresearched gap and re-chased every pass.
- Deliberately NOT marked "Not applicable": FY2024/FY2025. The metric applied in
  both years; only the *duty to publish* was removed by SDDT. That is a real
  disclosure limitation and must keep counting as a gap.
- **Overview LCR row split into two rows.** It was one row spanning FY2018-FY2023,
  silently merging 12-month-average (FY2022/23, UK KM1) with point-in-time
  (FY2018-21). The detail sheet always kept them apart; the Overview did not.
  Same defect as the Zenith Overview correction in RESUME_SESSION §8.

### Status
- [x] Rename recorded; URL constants repointed
- [x] FY2024/FY2025 enumerated negative re-confirmed 4 ways
- [x] ARs mined — genuinely nothing further to fill
- [x] NSFR structural cells marked; Overview LCR basis split
- [x] Rebuilt, 18 sheets

---

## 3. METHODIST CHAPEL AID — `scripts/build_methodist_chapel_aid.py` — DONE

### Wayback CDX enumeration (the only method that works here)
Permutation is hopeless — a different filename style every single year:
`pillar3disclosures2019.pdf`, `pillar3disclosures2020.pdf`,
`2021-pillar-3-disclosures.pdf`, `pillar3disclosures2022.pdf`, then the Umbraco
opaque-key form `/media/ngqlqg5o/pillar-3-disclosures-2023.pdf`.

CDX over the whole domain returned **160 distinct URLs**, of which **6 are
Pillar 3 URLs covering 5 editions**: FY2019, FY2020, FY2021, FY2022 (twice — old
`/sitefiles/` path and post-migration `/media/` path), FY2023. **Nothing later.**
Archive is current for this domain (newest captures June 2026), so the negative
is meaningful.

Live-site scrape (all 11 pages from sitemap.xml): 5 PDFs — AR 2025, country-by-
country 2025, FSCS leaflet, privacy notice, brochure. No Pillar 3.
**But per the standing rule this page canNOT prove absence** — MCA has never
linked its Pillar 3 docs there even in years they existed. Weight rests on CDX +
the SDDT Rule 3.1 date test (effective 11 April 2024, already in the script).

### FY2024/FY2025 — nothing fillable from the annual reports
Both ARs downloaded and read. Both are purely qualitative: Total Capital
Requirement 17.72% of RWAs (a *requirement*, not an outturn), CET1 risk appetite
"at least 35% of RWAs" (a target floor), LCR policy "at least 200%" (a floor),
and Note 24's "actual regulatory capital ... remained above that required"
naming no amount. No KM1 table, no RWA, no leverage, no outturn ratio.
**Nothing transcribed. Nothing back-solved.**

### REAL BUG FOUND AND FIXED — LCR/NSFR basis mixing
The LCR row was labelled "Average liquidity coverage ratio" but held:
- FY2023 835% — genuinely the 12-month average ✓
- FY2022 833% — actually the **KM1 year-end point-in-time**; the FY2022
  document's own stated average is **827%**
- FY2021 603% — also a KM1 year-end comparative

Same defect on NSFR: FY2023 182% (average) vs FY2022 192% (year-end; the FY2022
document's own average is **194%**) and FY2021 184% (year-end).

Fixed by splitting both sheets into two labelled rows. **New cells transcribed:**
LCR average FY2022 **827%**; LCR year-end FY2023 **970%**; NSFR average FY2022
**194%**; NSFR year-end FY2023 **174%**. Overview updated the same way, and an
NSFR row added to the Overview for the first time.

### SOURCE QUIRK recorded, not "corrected"
In both the FY2022 and FY2023 editions the KM1 HQLA input row is captioned
"(Weighted value - average)", yet the ratio KM1 states is demonstrably the
**year-end** figure — it reproduces the 31-December column of that same
document's quarterly table exactly (FY2023 KM1 970% = its 31-Dec-23 column;
FY2022 KM1 833% = its 31-Dec-22 column), while the separately-stated average is a
different number (835% / 827%). The caption is wrong in the source. Rows are
labelled for what the figures demonstrably are; the caption is left as published.

### Other changes
- NSFR FY2016–FY2020 → "Not applicable" (structural, PRA PS17/21). FY2021
  deliberately NOT marked so — a figure *was* published for it (FY2022 KM1
  comparative), and a disclosed figure outranks the structural argument.
- FY2024/FY2025 left blank, not "Not applicable" — SDDT removed the *duty to
  publish*, not the metric. Same call as Hampden.
- The FY2023 P3 citation in `p3_sources()` pointed at a live URL that now 404s
  with no fallback; added the Wayback snapshot (RWA_BREAKDOWN_SOURCES already
  had it, p3_sources did not).

### NOT TOUCHED, as instructed
The **£48k discrepancy** is intact: FY2021 category total 26,321 (FY2021 doc) vs
26,369 (FY2022 doc's KM1 comparative for the same date). Total RWAs FY2021
verified still 26,369 in the rebuilt workbook.

### Status
- [x] CDX enumeration run and recorded
- [x] FY2024/FY2025 ARs mined — genuinely nothing to fill
- [x] LCR/NSFR basis bug fixed, 4 new cells transcribed
- [x] NSFR structural cells marked
- [x] Rebuilt, 18 sheets

---

## Cross-bank lessons from this batch
1. **A single rendered page is not an asset space.** Cynergy's false negative came
   from enumerating one page's Contentful assets and calling it "the whole asset
   set". Different pages on the same site expose different asset sets.
2. **Scrape every index page a site has, not the obvious one.** Cynergy's P3s live
   only on `/strong-and-prudent-management`; MCA's live on none of its pages.
3. **Absence from an index ≠ withdrawn.** Hampden still serves its 2019/2021/2022
   P3s with HTTP 200 from both live hosts though nothing links them.
4. **Always run a positive control alongside 404 sweeps** — a known-good URL on
   the same host, same request shape. Used at Hampden; it is what turns "all
   404" into evidence.
5. **"Average" captions on UK KM1 liquidity rows are not trustworthy.** MCA's KM1
   says average and prints point-in-time. Check against the document's own
   quarterly table before mapping a figure to an averaged series.
