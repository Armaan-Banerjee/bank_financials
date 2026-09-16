# RESUME — C. Hoare & Co. and BNY Mellon "published-then-lost" Pillar 3 leads

Session started 2026-09-16. Lead type: a bank's own annual report asserting that
its Pillar 3 disclosures **were published on its website** for a year where this
project holds no document.

---

## 1. C. HOARE & CO. (company 00240822, FRN 122093) — y/e 31 MARCH

### What the assertion's sentence actually pointed at

The recurring sentence ends in a colon, so the colon was chased in all eight
annual reports held (FY2019-FY2026). Result: **the colon is nearly always
followed by the bare domain, not a path.**

| AR | text after the colon |
|----|----------------------|
| FY2019 (Financial Report 2019) | `www.hoaresbank.co.uk` |
| FY2020 (Annual Report and Accounts for 2020) | `www.hoaresbank.co.uk` |
| FY2021 (CHC_Cons_Accounts21) | `www.hoaresbank.co.uk` |
| FY2022 (Annual Report 2022) | `www.hoaresbank.co.uk` |
| FY2023 (Financial Report 2023) | `www.hoaresbank.co.uk/financial-reports` (2 of 3 occurrences; the Note 31 occurrence still says bare domain) |
| FY2024 (Financial Report 2024) | `www.hoaresbank.co.uk/financial-reports` |
| FY2025 (Financial Report 2025) | `www.hoaresbank.co.uk/financial-reports` |
| FY2026 (Financial Report 2026) | n/a — records the SDDT approval (Dec 2025) and that the bank "no longer prepares Pillar III disclosures" |

So the colon yielded **one** useful string — the `/financial-reports` index path,
first appearing in the FY2023 report. That index is what unlocked the run.

### Routes tried

| Route | Result |
|-------|--------|
| `/financial-reports` live index, `curl` + `grep href` | **HIT** — lists 2 Pillar 3 editions the build script did not hold (2022, 2024), plus annual accounts back to 2008 |
| Wayback CDX, `url=hoaresbank.co.uk&matchType=domain`, filter `.pdf`, then grep `pillar` | **HIT** — 2010, 2011, 2012, **2018**, **2019**, 2021, 2022, 2023 editions |
| Wayback CDX on `sites/default/files/styles/*` (the pre-Drupal-migration path) | enumerated; **no 2020 or 2017 edition present** |
| Direct-fetch `sites/default/files/styles/{2016,2017,2020,2021} Pillar 3 Disclosures.pdf`, live AND Wayback | all honest **404** (live `404 text/html 81,222 B`; Wayback `404 text/html 4,718 B`) |
| Negative controls in `/files/2021-05/`, `/files/2022-07/`, `/files/2024-06/`, `sites/default/files/styles/` | every one returns an honest **404** — this host does NOT soft-404 |

### Documents found (every one cover-dated, not filename-dated)

| Edition | URL | Pages | Cover |
|---------|-----|-------|-------|
| FY2019 | Wayback `20190923044126id_/https://www.hoaresbank.co.uk/sites/default/files/styles/2019%20Pillar%203%20Disclosures.pdf` (live path now 404) | 54 | "C. Hoare & Co. / Capital and Risk Management / Pillar 3 Disclosures / **Year ended 31 March 2019**" |
| FY2018 | Wayback `20210506235636id_/…/2018%20Pillar%203%20Disclosures.pdf` | 53 | "**Year ended 31 March 2018**" — outside this workbook's year range, recorded only |
| FY2022 | `https://www.hoaresbank.co.uk/files/2022-07/2022_Pillar_3_Disclosures_0.pdf` | 29 | "**Year ended 31 March 2022**" |
| FY2024 | `https://www.hoaresbank.co.uk/files/2024-06/Pillar_3_Disclosure_2024.pdf` | 24 | "**Year ended 31 March 2024**" |

All four: HTTP 200, `application/pdf`, `%PDF` magic verified, none at the
1,048,576-byte truncation size, last page carries text.

### Enumerated absence

**FY2020 Pillar 3 (y/e 31 March 2020): ENUMERATED AND ABSENT.** The live
`/financial-reports` index, the Wayback CDX domain sweep, the CDX sweep of the
pre-migration `sites/default/files/styles/` directory, and direct-fetch of the
exact filename pattern that DOES work for 2018 and 2019 all return nothing /
honest 404s. Note the bank migrated to Drupal in 2021 and back-loaded legacy
documents into `/files/2021-05/` and `/files/2021-06/` — those batches include
*Financial Report 2019* and *Annual Report and Accounts for 2020* but **no
Pillar 3 of any vintage**, which is why the 2018/2019 editions survive only at
the old pre-migration path and 2020 survives nowhere. FY2020 figures are
nonetheless fully covered by the FY2021 edition's comparative column, so this
absence costs the workbook nothing.

**FY2019 LCR and NSFR: disclosed qualitatively only.** The FY2019 edition's
section 11 says "The bank exceeds its regulatory requirements for the LCR ratio"
and carries no KM1/LIQ1 template and no numeric LCR or NSFR. Not a retrieval
failure — the number was never published. Left blank, not estimated.

**FY2019 MREL: absent.** No MREL row, and no qualitative MREL statement, anywhere
in the 54-page FY2019 edition (`grep -i "MREL|minimum requirement for own funds|bail-in"` → nil).

### Cells filled / corrected in `scripts/build_c_hoare.py`

Done — see the script. Summary:
- FY2019 filled on CET1 Capital, CET1 Ratio, Tier 1 Capital, Tier 1 Ratio,
  Total Capital, Total Capital Ratio, Total RWAs, Leverage Ratio, RWA Breakdown.
- **Leverage basis break corrected.** FY2019/FY2020/FY2021 were on the
  including-central-bank-claims CRD IV basis and were sitting on a row labelled
  "excluding claims on central banks". Split onto their own row.
- **`Equity exposures` row added to RWA Breakdown** — it was missing entirely,
  so FY2021/FY2020 credit-risk rows did not sum to their own printed total.
- FY2021 LCR (357%) recovered from the FY2022 edition's comparative column.
- FY2024 CET1/Total capital repointed to the FY2024 own-year edition.

---

## 2. BNY MELLON — The Bank of New York Mellon (International) Limited

(in progress — see below)
