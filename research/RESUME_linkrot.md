# Link-rot repair checkpoint — started 2026-09-15

Task: two banks whose already-cited Pillar 3 URLs have gone dead. Principle applied:
when a live URL dies, cite a Wayback `id_` snapshot rather than deleting the citation;
keep the original URL too, labelled as the dead original.

Every replacement URL below was verified by downloading it and checking the `%PDF`
magic bytes (not just HTTP 200 — soft-404s returning 200 with HTML have been hit
repeatedly).

## Status

- [x] Kingdom Bank — `scripts/build_kingdom_bank.py` — DONE, rebuilt, 18 sheets
- [ ] Methodist Chapel Aid — `scripts/build_methodist_chapel_aid.py`

## 1. Kingdom Bank Limited (FRN 400972)

### URL verification (2026-09-15)

Live originals, all confirmed HTTP 404 today:

- `https://www.kingdom.bank/wp-content/uploads/2021/03/5ee1ea4628eaae3b944cb122_Pillar-3-Disclosures-approved-14-May-2020.pdf` → 404
- `https://www.kingdom.bank/wp-content/uploads/2021/07/Pillar-3-Disclosures-approved-3-June-2021-v2.pdf` → 404
- `https://www.kingdom.bank/wp-content/uploads/2022/06/Pillar-3-Disclosures-2021-approved-9-June-2022-clean-v2.pdf` → 404

Wayback `id_` replacements, all retrieved with `%PDF-` magic bytes:

| Edition | Snapshot | Bytes | Pages |
|---|---|---|---|
| FY2019 (approved 14 May 2020) | `https://web.archive.org/web/20230321070013id_/https://www.kingdom.bank/wp-content/uploads/2021/03/5ee1ea4628eaae3b944cb122_Pillar-3-Disclosures-approved-14-May-2020.pdf` | 834,124 | 21 |
| FY2020 (approved 3 Jun 2021) | `https://web.archive.org/web/20240701022732id_/https://www.kingdom.bank/wp-content/uploads/2021/07/Pillar-3-Disclosures-approved-3-June-2021-v2.pdf` | 345,689 | 24 |
| FY2021 (approved 9 Jun 2022) — NEW | `https://web.archive.org/web/20240617063554id_/https://www.kingdom.bank/wp-content/uploads/2022/06/Pillar-3-Disclosures-2021-approved-9-June-2022-clean-v2.pdf` | 399,602 | 25 |

FY2024 Annual Report (live, `%PDF-`, 81pp):
`https://www.kingdom.bank/wp-content/uploads/KBL-Statutory-Accounts-2024.pdf`

FY2022 / FY2023 Pillar 3: no retrievable copy (Wayback capture is a bot-check page,
or never archived). To be recorded as such.

### DONE — what changed in `scripts/build_kingdom_bank.py`

Rebuilt with `python3 scripts/build_kingdom_bank.py`; 18 sheets confirmed.

**Major correction.** The script previously asserted (in `NOT_DISCLOSED_NOTE`) that the
bank's "Pillar 3 practice lapsed after the FY2015 edition" and that no standalone Pillar 3
document existed for any reported year. That was WRONG. Kingdom Bank published Pillar 3
disclosures for FY2019–FY2023. The earlier search missed them because it enumerated the
live WordPress media library and a 2017 capture of `/about-us/pillar-3-disclosure/`; the
FY2019–FY2023 documents live under `/wp-content/uploads/` and every one of those URLs has
since 404'd, so live-site enumeration returned a true but misleading "nothing there now".
A CDX sweep filtered on `pillar` surfaced them.

**New data filled (regulatory basis, from the recovered documents):**

| Sheet | New rows |
|---|---|
| CET1 Capital | FY2021 6,892; FY2020 6,594; FY2019 £5.7m; FY2020 pre-deduction 6,759 / deduction −165 |
| CET1 Ratio | FY2021 16.97%; FY2020 16.64% |
| Tier 1 Capital / Tier 1 Ratio | same values (KM1 prints rows 1=2 and 5=6, so equality is now *stated*, not inferred) |
| Total Capital | FY2021 7,653; FY2020 7,448 (T2 854); FY2019 £6.7m |
| **Total Capital Ratio** | was "Not publicly disclosed" → FY2021 18.84%; FY2020 18.79% |
| **Total RWAs** | was "Not publicly disclosed" → FY2021 40,617; FY2020 39,632 |
| **RWA Breakdown** | was "Not publicly disclosed" → full UK OV1 + FY2021 SA class detail + FY2020/FY2019 CRR Art 112 detail + own-funds-requirement block |
| Leverage Ratio | FY2021 10.40%, FY2020 10.35% (excl. central bank claims) + exposure measure 66,250 / 63,697 |
| LCR | FY2021 1,382.23%, FY2020 998.00% (12-mo avg) + HQLA/inflow/outflow components |
| **NSFR** | was "Not publicly disclosed" → FY2021 160.67%; FY2020 151.57% (bank's own estimates) |
| MREL Ratio | unchanged — genuinely undisclosed in every year |

**Validation gate applied — nothing overwritten.** The Pillar 3 series and the Annual
Report KPI series disagree, so both are carried on separate labelled rows:
- CET1 Ratio FY2020: KPI 17.13% vs Pillar 3 16.64% (49bp)
- LCR FY2021: KPI 1,475.9% vs Pillar 3 1,382.23% (94pp); FY2020: 1,304.6% vs 998.00% (307pp)
- Leverage FY2021: 9.03% (total exposure) vs 10.40% (excl. central banks) — different measures
- Credit-risk RWA at 31 Dec 2020: 35,488 (FY2020 edition) vs 35,487 (FY2021 edition's
  comparative) — £1k difference, both rows kept
- *Control that passed:* leverage FY2020 9.37% / FY2019 9.40% / FY2018 10.10% in the Pillar 3
  documents match the KPI table exactly; CET1 ratio FY2021 16.97% matches to the basis point.

**LCR average check (the trap this project keeps hitting).** KM1's caption claims a 12-month
average. Verified it really is one from the components in the same table: 8,840 / 640 = 1,382%
(FY2021) and 6,580 / 659 = 998% (FY2020), both reproducing the printed ratio.

**FY2019 precision.** That edition prints £m to 1 d.p.; its figures are carried in £'000 at
that precision (5,700 = "£5.7m as printed") and every row label and note says so.

**Not back-solved:** FY2021 Tier 2 is left blank (KM1 prints total capital and Tier 1 but no
T2 line — 7,653 − 6,892 was deliberately not computed). No total RWA is shown for FY2019
(neither the FY2019 nor FY2020 edition states one).

**SDDT recorded.** Rule 3.1, FRN 400972, waiver ref A00009930P.pdf, start 20/02/2025, no end
date — verified firsthand from the BoE consolidated waivers CSV, not from memory. Year-end is
31 December, so **only FY2025 is structurally exempt**; FY2024 and earlier predate the
modification and are recorded as ordinary non-disclosure. The FY2024 AR's own words are
quoted verbatim in the note (p.13 "The Bank has submitted a modification by consent to join
the SDDT regime"; p.27 "Due to the SDDT regime the Pillar 3 disclosure document will not be
required in future years").

**Source typo reproduced and flagged, not silently fixed:** the FY2021 edition's narrative
says £3,249k was the Pillar 1 requirement "as at 31 December 2020"; the table header and the
FY2020 edition's own £3,171k establish it is the 2021 figure.

## 2. Methodist Chapel Aid — in progress
