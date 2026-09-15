# RESUME — peer WebSearch discovery (batch 4 checkpoint)

Written 2026-09-15 by the discovery session (WebSearch/WebFetch only) working for
katalysis-36. Nothing in this file has been downloaded, transcribed or validated —
every URL below is a *discovery lead* for the retrieval side to verify. No build
scripts or other repo files were touched.

Conventions: FY = the bank's own financial year label. "ENUMERATED NEGATIVE" = the
bank's own index page was fetched and the year is absent from it. "UNVERIFIED" =
came from a search-engine summary and was not seen on a fetched page.

---

## Batch 4 — status per target

### 1. Nomura Bank International plc (31 Mar year-end) — PARTIAL, promising
- **Key finding:** the *Nomura Europe Holdings plc (NEHS) Group* Pillar 3 covers "the
  Group as well as three material subsidiaries: Nomura International Plc (NIP),
  Nomura Bank International Plc (NBI) and Nomura Financial Products Europe GmbH
  (NFPE)" (snippet from the 31 Mar 2021 annual edition). This looks like the
  UK-CRR large/material-subsidiary section with NBI's own figures — **verify the
  table is NBI entity-level before using** (entity-basis rule).
- NEHS Pillar 3 editions indexed (note two path prefixes, `/portal/site/login/` and
  `/portal/site/public/`):
  - FY2017 annual: https://www.nomuranow.com/portal/site/login/en-gb/resources/upload/Nomura-Europe-Holdings-plc-Pillar-3-Disclosures-310317.pdf
  - FY2018 annual: https://www.nomuranow.com/portal/site/login/en-gb/resources/upload/Nomura-Europe-Holdings-plc-Pillar-3-Disclosures-310318.pdf
  - FY2019 annual: https://www.nomuranow.com/portal/site/login/en-gb/resources/upload/Nomura-Europe-Holdings-plc-Pillar-3-Disclosures-310319.pdf
  - FY2021 annual: https://www.nomuranow.com/portal/site/login/en-gb/resources/upload/nomura-europe-holdings-plc-annual-pillar-3-disclosures-310321.pdf
  - FY2024 annual: https://www.nomuranow.com/portal/site/public/en-gb/resources/upload/nomura-europe-holdings-plc-annual-pillar-3-disclosures-310324.pdf
  - Q 30 Jun 2019: https://www.nomuranow.com/portal/site/login/en-gb/resources/upload/Nomura-Europe-Holdings-plc-Quarterly-Pillar-3-Disclosures-300619.pdf
  - H1 30 Sep 2021: https://www.nomuranow.com/portal/site/login/en-gb/resources/upload/nomura-europe-holdings-plc-semi-annual-pillar-3-disclosures-300921.pdf
  - H1 30 Sep 2023: https://www.nomuranow.com/portal/site/public/en-gb/resources/upload/nomura-europe-holdings-plc-semi-annual-pillar-3-disclosures-300923.pdf
  - Q 31 Dec 2023: https://www.nomuranow.com/portal/site/public/en-gb/resources/upload/Nomura-Europe-Holdings-plc-Group-Quarterly-Pillar-3-Disclosures-311223.pdf
  - Q 31 Dec 2024: https://www.nomuranow.com/portal/site/public/en-gb/resources/upload/Nomura-Europe-Holdings-plc-Group-Quarterly-Pillar-3-Disclosures-311224.pdf
  - Undated: https://www.nomuranow.com/portal/site/login/en-gb/resources/upload/Nomura-Europe-Holdings-plc-Pillar-3-Disclosures.pdf
- **Filename tests (direct fetch, pattern
  `nomura-europe-holdings-plc-annual-pillar-3-disclosures-3103YY.pdf`):**
  - FY2022 RESOLVES (91pp, cover "Nomura Europe Holdings plc Group, Annual Pillar 3
    Disclosures 31st March 2022"): https://www.nomuranow.com/portal/site/public/en-gb/resources/upload/nomura-europe-holdings-plc-annual-pillar-3-disclosures-310322.pdf
  - FY2023 RESOLVES (cover "… 31st March 2023"): https://www.nomuranow.com/portal/site/public/en-gb/resources/upload/nomura-europe-holdings-plc-annual-pillar-3-disclosures-310323.pdf
  - 404: `/login/` 310322 and 310323; both prefixes for 310325 and 310326.
- **SOURCED NEGATIVE for NBI, FY2022 and FY2023 (read p.5 "Scope of Application"
  of both PDFs):**
  - FY2022: "NBI and NFPE were previously considered 'significant subsidiaries' and
    previously disclosed. However, along with the other regulated subsidiaries, they
    are not considered to be large subsidiaries as at 31st March 2022 and are
    therefore not disclosed in this document."
  - FY2023: the regulated subsidiaries including NBI "are not considered to be large
    subsidiaries as at 31st March 2023 and are therefore not disclosed in this document."
  - The TOC templates in both are for "the Group" and "NIP" only.
  - FY2024 (310324, read p.5): same wording, "not considered to be large subsidiaries
    as at 31st March 2024 and are therefore not disclosed". TOC is Group + NIP only.
    → SOURCED NEGATIVE for NBI FY2024 as well.
  - So the NEHS annex route gives NBI figures only up to FY2021.
- **FY2021 NEHS (310321) DOES carry NBI entity-level own funds (verified by reading):**
  - Scope p.1: "NBI disclosures have been made for article 437 (Own Funds) with no
    other disclosures relevant to significant subsidiary requirements".
  - Tables:
    - p.7 "CC1: Composition of Regulatory Capital" has Group / NIP / **NBI** / NFPE
      columns (Mar-21, $m), including CET1, Total Capital, CET1 Ratio and Total Capital
      ratio rows; footnote 6 says Tier 1 ratio = CET1 ratio.
    - p.9 "LI1: Reconciliation of NBI Own Funds".
  - No NBI RWA, leverage or LCR table (Art 437 only).
- **NBI's own annual reports (solo entity, Co. reg. 1981122) — URLs resolve:**
  - FY2023: https://www.nomuranow.com/portal/site/public/en-gb/resources/upload/NBI-Annual-Report-310323.pdf
  - FY2024: https://www.nomuranow.com/portal/site/public/en-gb/resources/upload/NBI-Annual-Report-310324.pdf
  - FY2025: https://www.nomuranow.com/portal/site/public/en-gb/resources/upload/NBI-Annual-Report-310325.pdf
  - FY2026: https://www.nomuranow.com/portal/site/public/en-gb/resources/upload/NBI-Annual-Report-310326.pdf
  - Their strategic reports (pp.1–7) give no capital ratios, only P&L, assets and
    shareholders' funds.
  - They say NBI "has minimum capital adequacy requirements imposed on it on a
    standalone basis by the PRA".
  - **Capital note (read via pdftotext):** "CAPITAL MANAGEMENT POLICY / UK Regulatory
    Capital" — note 16 in FY2022/FY2023, note 15 in FY2025 (p.79) / FY2026 (p.84).
    - Gives ONLY "Tier 1 capital" and "Total capital resources" ($'000, current year +
      prior-year comparative), and says "The Bank does not currently maintain Tier 2 capital".
    - No CET1 line, no ratios, no RWAs.
    - FY2026 footnote: "Tier 1 capital is not subject to audit". The FY2025 AR covers
      31 Mar 2024 as its comparative.
    - FY2022 AR also resolves: https://www.nomuranow.com/portal/site/public/en-gb/resources/upload/NBI-Annual-Report-310322.pdf
    - **katalysis-36 ruling:** Total capital = Tier 1 (no T2 stated), but CET1 is NOT
      inferred (no document rules out AT1). CET1 stays blank FY2022–FY2026 with a note.
- **Pattern worth reusing:** "was a significant subsidiary, then ceased to be one" explains
  a parent-annex series simply stopping (the NEHS FY2022 wording).
- **Don't spend:** Wayback for NEHS FY2025/26 (agreed with katalysis-36).
- NBI own docs: annual reports
  https://www.nomuranow.com/portal/site/public/en-gb/resources/upload/NBI-Annual-Report-310324.pdf ,
  `...-310323.pdf` (public), `...-310321.pdf` (under /login/); interim
  https://www.nomuranow.com/portal/site/public/en-gb/resources/upload/NBI-Interim-Report-Sep2023.pdf
- Do NOT use: Nomura Holdings Inc. (Japan) Basel disclosures on nomuraholdings.com
  (Japanese group consolidated); Nomura Bank (Luxembourg) S.A. Pillar 3 (different entity).

### 2. Bank of Ceylon (UK) — LCR/NSFR FY2022, FY2023 — NEGATIVE
- Off-domain name searches found no copy of a 2022 or 2023 Pillar 3.
- Own index (fetched in batch 2) https://bankofceylon.co.uk/financial-statements/
  lists Pillar 3 for 2018–2021 and 2024–2025 only → ENUMERATED NEGATIVE for 2022/2023.
- Fallback only: FS 2022 https://bankofceylon.co.uk/downloads/corporate/BOCUK_Financial_statements_2022.pdf ,
  FS 2023 https://bankofceylon.co.uk/downloads/corporate/BOCUK_Financial_statements_2023.pdf
- Do NOT use: Bank of Ceylon (Sri Lanka parent) annual report capital-adequacy pages.

### 3. Secure Trust Bank PLC — FY2017–FY2019 — RESOLVED (found, index enumerated)
- Full index = the paginated results page (5 pages, `?start=0,6,12,18,24`):
  https://www.securetrustbank.com/investor-relations/investors/results-reports-and-presentations/financial-results
  Annual Pillar 3 is listed for **every year FY2015–FY2025**; nothing before FY2015
  (the `?start=24` page covers 2011–2014 results with no Pillar 3 items).
- **Slug trap:** 2017–2019 use `-annual`, not `-final` (the `-final` permutations 404).
  - FY2019: https://www.securetrustbank.com/investor-relations/document-library/pillar-3-disclosure-2019-annual
  - FY2018: https://www.securetrustbank.com/investor-relations/document-library/pillar-3-disclosure-2018-annual
  - FY2017: https://www.securetrustbank.com/investor-relations/document-library/pillar-3-disclosure-2017-annual
  - FY2016: https://www.securetrustbank.com/investor-relations/document-library/pillar-3-disclosure-2016-annual
  - FY2015: https://www.securetrustbank.com/investor-relations/document-library/pillar-3-disclosure-2015-annual
  - FY2020/2021/2022: `.../pillar-3-disclosure-YYYY-final`; FY2023–2025 also `-final`.
  - Quarterlies: `.../pillar-3-disclosure-2017-q1|q2|q3`, `2018-q1|q2|q3`, `2019-q1|q2|q3`;
    interims `2022-interim` … `2026-interim`.
- The document-library slugs are HTML landing pages; the PDF link is inside each.

### 4. Paragon Bank PLC — FY2017–FY2020 — ENTITY-BASIS NEGATIVE (probably)
- Only **Paragon Banking Group PLC** Pillar III found; search snippet: disclosures
  "cover the Group as a whole on a consolidated basis". Parent-group basis → not
  Paragon Bank PLC's own figures unless a solo annex exists (not verified).
- URLs (30 Sep year-end), for checking for a solo annex:
  - FY2017: https://www.paragonbankinggroup.co.uk/resources/paragon-group/documents/reports-presentations/2017/paragonbankinggroup_iii_report_2017
  - FY2018: https://www.paragonbank.co.uk/resources/paragonbank/documents/savings/2018-remuneration-code-pillar-iii-disclosure
  - FY2019: https://www.paragonbank.co.uk/resources/paragongroup/documents/reportspresentations/2019/pillar-iii-document
  - FY2020: https://www.paragonbankinggroup.co.uk/resources/paragon-group/documents/reports-presentations/2021/pbg_2020_pillar_iii_disclosures
  - FY2021: https://www.paragonbankinggroup.co.uk/paragongrouprefresh_viewer/resources/paragon-group/documents/reports-presentations/2022/pbg_2021_pillar_iii_disclosures
  - FY2024 (on FCA NSM): https://data.fca.org.uk/artefacts/NSM/Portal/NI-000111546/NI-000111546.pdf
  - HY 31 Mar 2022: https://www.paragonbankinggroup.co.uk/resources/paragon-group/documents/corporate-governance/half-year-pillar-iii
  - HY 31 Mar 2023: https://www.paragonbankinggroup.co.uk/resources/paragon-group/documents/reports-presentations/2023/paragonbankinggroup_hy_pillar-3_2023
- **Method note:** FCA National Storage Mechanism (data.fca.org.uk/artefacts/NSM/…)
  hosts Pillar 3 PDFs for listed issuers — another off-domain source.

### 5. Recognise Bank Limited — FY2018–FY2020 — NEGATIVE (pre-disclosure era)
- Investors index https://recognisebank.co.uk/investors/ (per search summary) lists
  Pillar 3 2023–2025 and annual reports 2022–2025 only.
  - Pillar 3 March 2023: https://www.recognisebank.co.uk/wp-content/uploads/2024/03/Pillar-3-disclosures-March-2023-RBL.pdf
  - Pillar 3 March 2024: https://recognisebank.co.uk/wp-content/uploads/Pillar-3-disclosure-March-2024-RBL.pdf
  - Pillar 3 March 2025: https://recognisebank.co.uk/wp-content/uploads/Pillar-3-disclosure-March-2025.pdf
  - AR 2023: https://recognisebank.co.uk/wp-content/uploads/2023/10/230821-Recognise-Bank-2023-Annual-Report-WEB.pdf
  - AR 2022: https://recognisebank.co.uk/wp-content/uploads/2023/10/2022-Annual-Report-Recognise-Bank-Limited.pdf
- **ENUMERATED NEGATIVE for FY2018–FY2020** — the investors page was fetched: Pillar 3
  listed for 2023, 2024, 2025, 2026 only; annual reports 2022–2026 only.
  - NEW, Pillar 3 March 2026: https://recognisebank.co.uk/wp-content/uploads/Pillar-3-disclosure-March-2026-RBL-v1.1-To-BAC-updated_-1-1.pdf
  - AR 2026: https://recognisebank.co.uk/wp-content/uploads/274107-Recognise-Bank-Annual-Report-WEB.pdf ;
    AR 2025: https://recognisebank.co.uk/wp-content/uploads/271817-Recognise-Bank-Annual-Report-WEB.pdf ;
    AR 2024: https://recognisebank.co.uk/wp-content/uploads/2024-Annual-Report-Accounts.pdf
  - The Pillar 3s are labelled "March YYYY", so check the year-end/label mapping.

### 6. FY2009–FY2013 era (optional) — Aldermore, Metro, Vanquis, ICICI UK
- **Aldermore:** found Aldermore Bank Plc editions
  - FY2009: https://www.aldermore.co.uk/media/b4scou3l/pillar_3_disclosure_2009_0.pdf
  - FY2010: https://www.aldermore.co.uk/media/yfik2u2e/pillar_3_disclosure_2010_0.pdf
  - FY2012: https://www.aldermore.co.uk/media/n0lnuva4/pillar_3_disclosure_2012_0.pdf
  - (FY2014 https://www.aldermore.co.uk/media/2vlludj0/aldermore-pillar-3-disclosures-2014.pdf and
    FY2015 https://www.aldermore.co.uk/media/ot5axgnp/pillar-3-disclosure-dec-2015.pdf are
    **Aldermore Group PLC** — group basis from 2014)
  - FY2011, FY2013: not found. Umbraco `/media/<hash>/` paths can't be permuted.
    Old investor-site file of unknown year: https://www.investors.aldermore.co.uk/system/files/uploads/financialdocs/pillar_3_disclosures.pdf
- **Metro Bank:** ENUMERATED NEGATIVE for FY2009–FY2013. IR page
  https://www.metrobankonline.co.uk/investor-relations/ lists Pillar 3 for 2016, 2017,
  2018, 2020–2025 (+H1s). Nothing before 2016.
  Earliest: https://www.metrobankonline.co.uk/globalassets/legal-information/pillar-3-disclosure-2016.pdf
  - **FY2019: FOUND although it's missing from the index** (live, verified `%PDF`, 54 pp, "Pillar 3 2019",
    METRO BANK PLC, 31 December 2019):
    https://www.metrobankonline.co.uk/globalassets/documents/investor_documents/metro-bank-pillar-3-2019.pdf
  - Nine guessed paths built from the neighbouring years' patterns all 404'd (same size as a control path).
    Only a web search found the real name. This is a live case of the caveat below.

**Caveat (from katalysis-36, 2026-09-15):** absence from an index is not proof of non-existence.
- Hampden still serves its 2019/2021/2022 Pillar 3 files, which no index links.
- Cynergy FY2023 is linked from only one page.
- An index negative for a year inside an unbroken run is PROVISIONAL until a direct fetch of plausible
  paths AND a name search both fail. A run that simply stops at the end is good evidence.
- **Vanquis Bank Limited:** ENUMERATED NEGATIVE (solo). https://www.vanquis.com/investors/results-reports-presentations/
  lists Pillar 3 only from 2021, and every edition is Provident Financial plc /
  Vanquis Banking Group (group basis). Search snippet: Provident Financial group
  published Pillar III in April 2012 (group — not usable for Vanquis Bank Ltd).
- **ICICI Bank UK PLC:** full index at https://www.icicibank.co.uk/personal/basel-disclosures
  (31 Mar year-end). All paths are relative to https://www.icicibank.co.uk
  - Basel II FY2013-14: /content/dam/icicibank/icici-assets/uk/disclosures2013-14.pdf
  - Basel II FY2012-13: /content/dam/icicibank/icici-assets/uk/disclosures2012-13.pdf
  - Basel II "2011-2012": /content/dam/icicibank/icici-assets/uk/basel2_disclosures_March31_11.pdf
    — **label/filename mismatch** (filename says March 2011); check the period inside.
  - Basel II "2010-2011": /content/dam/icicibank/icici-assets/uk/basel2_disclosures_FY10_11.pdf
  - Basel II FY2009-10: /content/dam/icicibank/icici-assets/uk/basel2_disclosures_FY09_10.pdf
  - Basel II FY2008-09: /content/dam/icicibank/icici-assets/uk/Basel_II_p3_Disclosure_Statement.pdf
  - Basel II FY2007-08: /content/dam/icicibank/icici-assets/uk/basel2_disclosures_FY2008.pdf
  - Also "Capital Resources disclosures" HTML pages for 31 Mar 2010–2019, e.g.
    /personal/basel_capital_resource_popup_march2013 (2010: /personal/basel_capital_resource_popup)
  - Basel III FY2014-15 → FY2025-26 also listed; FY2025-26:
    /content/dam/icicibank-revamp/uk/doc/basel-pillar-3-disclosures-FY2026.pdf

### 7. FY2009–FY2013 era (optional) — Zenith, PNBIL, Julian Hodge, Clydesdale
- **Zenith Bank (UK):** ENUMERATED NEGATIVE on the current page.
  https://www.zenith-bank.co.uk/pillar-3/ lists only 2021–2025
  (/media/2228/31dec21-pillar-3.pdf … /media/2290/pillar-3-zbuk-31dec25.pdf).
  Older editions only via Wayback, if at all. Do NOT use zenithbank.com (Nigerian parent).
- **Punjab National Bank (International):** not found for FY2009–FY2013. Earliest
  indexed is FY2016 (31 Mar 2016), which says Basel III disclosure was adopted
  w.e.f. 01.01.2014:
  https://www.pnbint.com/PNBIL/pdf/Financial_Reports/Pillar%20III%20disclosures%2031%2003%202016_Revised.pdf
  Also FY2018, FY2022, FY2024 under the same /PNBIL/pdf/Financial_Reports/ path.
  The index page on pnbint.com was not located. Do NOT use pnb.bank.in (Indian parent).
- **Julian Hodge Bank:** full index at https://hodgebank.co.uk/hodge/financial-information/
  lists Pillar 3 2010–2023 (31 Oct year-end to FY2019, then 30 Sep):
  - 2010: https://hodgebank.co.uk/wp-content/uploads/2024/07/jhb-pillar3-2010.pdf
  - 2011: https://hodgebank.co.uk/wp-content/uploads/2024/07/jhb-pillar3-2011.pdf
  - 2012: https://hodgebank.co.uk/wp-content/uploads/2024/07/jhb-pillar3-2012.pdf
  - 2013: https://hodgebank.co.uk/wp-content/uploads/2024/07/jhb-pillar3-2013.pdf
  - (2014–2018 same pattern; 2019 Pillar-3-Disclosure-FY19-FINAL.pdf; 2020 2.-JHB-Pillar-III.pdf;
    2021 Hodge-Pillar-3-Document-2020_2021.pdf; 2022 Hodge-pillar-3-19.06.23.pdf;
    2023 Hodge-pillar-3-11.03.24.pdf — all under /wp-content/uploads/2024/07/)
  - ENUMERATED NEGATIVE: FY2009, and also **FY2024 and FY2025** (ARs for those years
    are listed but no Pillar 3).
- **Clydesdale Bank PLC:** SOURCED NEGATIVE (parent basis) for FY2009–FY2013. The NAB
  Sept 2013 Pillar 3 says Clydesdale "relies on references to comparable National
  Australia Bank Limited consolidated disclosure to satisfy its Pillar 3 disclosure
  obligations": https://www.nab.com.au/content/dam/nabrwd/documents/reports/financial/pillar-3-report-september-2013.pdf

---

## Batch 5 — status (complete except the Bank of Ceylon Wayback pass)

**Verification:** every batch-5 PDF URL below was checked with `curl -r 0-4` → `%PDF` + application/pdf.
- nbeuk.com returns **403 text/html to bare curl** (bot block), but the PDFs download fine (200, application/pdf,
  `%PDF`) with a browser User-Agent + Referer https://www.nbeuk.com/about-us/ . Use those headers.
- The Persia website works over http only.

### Index pages (item 5)
- **National Bank of Egypt (UK):** ENUMERATED.
  - Index: https://www.nbeuk.com/about-us/ (the homepage has no Pillar 3 link; the documents sit on About Us).
  - Pillar 3 listed 2017–2025; financial reports 2011–2025; NO Pillar 3 for 2011–2016.
  - **Year-end label trap:** 2017–2020 Pillar 3 filenames are dated 30 June
    (Pillar_3_30062020_FINAL.pdf, Pillar-3-as-at-30062019-FINAL.pdf, Draft_Pillar_3-30062017_30112017.pdf);
    2021+ are 31 December. Check which FY each maps to.
  - All under https://www.nbeuk.com/wp-content/uploads/ :
    - 2025: 2026/04/NBEUK-Pillar-3-Disclosures-31st-December-2025.pdf
    - 2024: 2025/04/Pillar-3-Disclosures-31st-December-2024.pdf
    - 2023: 2024/09/Pillar-3-Disclosures-31st-December-2023-FINAL.pdf
    - 2022: 2023/10/NBE-UK-Pillar-3-31-December-2022-approved.pdf
    - 2021: 2023/05/Pillar-3-31-December-2021-approved.pdf
    - 2020: 2021/02/Pillar_3_30062020_FINAL.pdf
    - 2019: 2023/01/Pillar-3-as-at-30062019-FINAL.pdf
    - 2018: 2021/02/2018_Basel_ll_Pillar_3_Disclosure.pdf
    - 2017: 2021/02/Draft_Pillar_3-30062017_30112017.pdf ("Draft" in the filename)
- **United National Bank (United Bank UK / UBL UK):** ENUMERATED.
  - Index: https://www.ubluk.com/footer-pages/annual-reports/
  - Pillar 3 2016–2024 listed; **2025 missing** (the 2025 statutory accounts ARE listed).
  - Paths relative to https://www.ubluk.com :
    - 2024: /media/sr5puvji/unb-2024-pillar3-approved-finalplusamended.pdf
    - 2023: /media/lupbssja/annual-report-unb-2023-pillar3-final-approved.pdf
    - 2022: /media/2unkh0m2/pillar-iii-disclosure-2022.pdf
    - 2021: /media/pqqda2ng/pillar-iii-disclosure-2021.pdf
    - 2020: /media/xq1lvuuj/pillar-iii-disclosure-2020.pdf
    - 2019: /media/sqgdszjz/pillar-iii-disclosure-2019.pdf
    - 2018: /media/5avboizc/pillar-iii-disclosure-2018.pdf
    - 2017: /media/o0bp44wd/pillar-iii-disclosure-2017.pdf
    - 2016: /media/sp5brt0v/pillar-iii-disclosure-2016.pdf
  - ARs 2016–2025 under /media/…; 2025 is /media/405naqby/ye2025-statutory-accounts-final-23apr2026_signed.pdf
  - Do NOT confuse with United Bank for Africa (UK) (ubauk.com).
- **Habib Bank Zurich plc (UK):** ENUMERATED, complete 2016–2025.
  - The FULL index is https://habibbank.com/gb/about-us/ . The /gb/financial-information/ page
    is STALE (stops at 2022).
  - Pillar 3 2016–2025 and ARs 2016–2025, no gaps. Paths under https://habibbank.com/gb/wp-content/uploads/sites/7/ :
    - P3 2025: 2026/09/Pillar-3-Disclosures-2025.pdf
    - P3 2024: 2025/08/Pillar-3-Disclosure-2024.pdf
    - P3 2023: 2024/10/UK-Pillar-3-Disclosure-2023.pdf (filename differs; the guesses under 2024/07 404)
    - P3 2016–2022: 2024/05/Pillar-3-Disclosures-YYYY.pdf
    - AR 2025: 2026/09/Annual-Report-2025.pdf
    - AR 2024: 2025/08/HBZ-UK-Annual-Report-2024.pdf
    - AR 2023: 2024/07/HBZ-UK-Annual-Report-2023.pdf
    - AR 2016–2022: 2024/05/Annual-Report-YYYY.pdf
  - Nothing before 2016 is listed.
  - Do NOT confuse with HBL Bank UK (hblbankuk.com).
- **Ghana International Bank plc:** NO enumerating index.
  - https://www.ghanabank.co.uk/about-us/ (fetched with curl) links only the LATEST set: AR 2024, AR 2025,
    summary FS 2025, 5-year financials 2025 and P3 2024. It is not a history, so it can't give enumerated negatives.
  - The 2025 Pillar 3 is not yet posted (AR 2025 is, Apr 2026).
  - ghanabank.co.uk fails TLS verification for WebFetch ("unable to verify the first certificate"); curl works.
  - Found by search, under https://www.ghanabank.co.uk/app/uploads/ :
    - 2024: 2025/11/GHIB-2024-Pillar-3-Disclosures.pdf
    - 2023: 2024/11/GHIB-2023-Pillar-3-Disclosures.pdf
    - 2022: 2023/09/GHIB-2022-Pillar-3-Disclosures.pdf
    - 2020: 2021/06/Pillar-3-Disclosures-2020.pdf
    - 2019: 2020/11/GHIB-2019-Pillar-3-Disclosures_FINAL_publish-on-website.pdf
  - 2021: 2022/10/GHIB-2021-Pillar-3-Disclosures.pdf (found by search) → 2019–2024 continuous.
  - Also AR 2022: 2023/03/GHIB-Annual-Report-and-Financial-Statements-2022-.pdf
  - Also summary FS 2023: 2024/04/Summary-Financial-Statements-2023.pdf

### Persia International Bank (item 3) — NOT wound down
- Companies House 04218020 shows it **Active**, with full accounts filed to 31 Mar 2022, 2023, 2024
  and 2025 (the 2025 accounts were filed 2 Sep 2025, 82 pp).
  https://find-and-update.company-information.service.gov.uk/company/04218020/filing-history
  - So "ceased operating" is NOT available as an explanation.
  - Accounts PDFs, prefix https://find-and-update.company-information.service.gov.uk :
    - FY2025: /company/04218020/filing-history/MzQ3OTMzNTI0NWFkaXF6a2N4/document?format=pdf&download=0
    - FY2024: /company/04218020/filing-history/MzQzMzA4NzcwMWFkaXF6a2N4/document?format=pdf&download=0
    - FY2023: /company/04218020/filing-history/MzM4OTExNTc1NmFkaXF6a2N4/document?format=pdf&download=0
    - FY2022: /company/04218020/filing-history/MzM1NTU5ODQzNmFkaXF6a2N4/document?format=pdf&download=0
    - FY2021: /company/04218020/filing-history/MzMxMTg0NDU2NWFkaXF6a2N4/document?format=pdf&download=0
- **Website index ENUMERATED** via plain **http** (https resets the connection):
  http://www.persiabank.co.uk/
  - The ONLY Pillar 3 linked is http://www.persiabank.co.uk/Pillar%203%202021%20v3.pdf
    ("PILLAR 3 DISCLOSURE (INCLUSIVE OF LCR DISCLOSURE) 31 MARCH 2021", 28 pp).
  - Other documents: annual reports pib_report_2003–2010.pdf only; sanctions/EU notices; GDPR; Wolfsberg 2025.
  - → ENUMERATED NEGATIVE for Pillar 3 FY2022–FY2025 on its own site. The 31 Mar 2018 edition katalysis-36
    holds is no longer linked.
- **Status evidence (not a wind-down, but material):**
  http://www.persiabank.co.uk/Important%20Notice%20About%20Sanctions%20Website%2006102025%20Final.pdf
  - "Persia International Bank PLC has been made subject to financial sanctions by the UK Government and
    the European Union as of 29 September 2025", operating under OFSI General Licence INT/2025/7345464.
  - It still says it complies with PRA/FCA obligations, so it is still authorised, under sanctions.
- **SOURCED ANSWER for FY2023–FY2025 (accounts, OCR'd with tesseract, "Pillar 3 Disclosures" paragraph, p.8
  of the directors' report):**
  - FY2022 accounts (y/e 31 Mar 2022): "Pillar 3 disclosures are made separately and are published on the
    Bank's web site" (yet the site now links only the 2021 edition).
  - FY2023, FY2024 and FY2025 accounts: "Pillar 3 disclosures are made separately and can be made available
    on request."
  - → From FY2023 the bank stopped publishing Pillar 3 publicly; it is available on request only
    (the same shape as Havin). This is a sourced "not publicly disclosed" for FY2023–25.
  - FY2022: the accounts claim it was published, but it is not on the site now. Treat as published-then-removed
    (the Wayback check is pending because the Internet Archive was offline).
- Also in the accounts (FY2025 p.17): "The Tier 1 Capital ratios are still robust" — no figure on that page.
  - The FY2025 auditor's report (p.24) has "Material uncertainty related to going concern"
    (OFAC sanctions); the FY2022 one (p.19) does too.

### Bank of Ceylon (UK) (item 4)
- **Mid-run gap re-checked by direct fetch (per the index caveat) — still NEGATIVE, now firmer:**
  - The index uses one uniform name: `/downloads/corporate/BOCUK_Pillar%203%20Disclosures%2031%20December%20YYYY.pdf`
    (2018–2021 and 2024–2025). The 2021 file is a positive control: 200, `%PDF`.
  - Eight 2022/2023 candidates (the exact pattern, underscores, "Disclosure" singular, no date) all return a real 404:
    548-byte text/html, byte-identical to a made-up control path. The site gives genuine 404s, not soft-404s.
  - Financial statements 2022 and 2023 are live (scanned, OCR'd); 2024 and 2025 have a text layer:
    - FS2022 audit committee "KEY AREAS OF FOCUS DURING 2022": "Approved the Pillar 3 disclosures as 31 December 2021."
    - FS2023's equivalent section (p.25) has no Pillar 3 line, and neither do FS2024 or FS2025, even though the 2024/2025
      editions exist. So the missing approval line is NOT evidence either way.
  - No LCR or NSFR figure in FS2022, FS2023 or FS2024 (only a mention of holding US Treasuries "in accordance with LCR requirements").
- **Capital figures available from the solo FS, if wanted for other cells (entity = Bank of Ceylon (UK) Ltd):**
  - FS2023 p.8: CET1 capital, CET1 ratio 43% (2022: 44%), total capital, total capital ratio 46% (2022: 48%),
    with 2022 comparatives.
    https://bankofceylon.co.uk/downloads/corporate/BOCUK_Financial_statements_2023.pdf
  - **Conflict:** FS2022 note 28 (p.60) gives 31 Dec 2022 "regulatory CET1 capital after adjusting for transitional
    relief under IFRS9" as GBP 13,958,648, but the FS2023 comparative for 2022 is GBP 12,852,280.
    Different basis or restated; don't reconcile by derivation.
  - **Label trap, FS2024:** "The CET1 total capital ratio at the end of 2024 was 24% (2023 46%) see note 32".
    The 46% matches FS2023's TOTAL capital ratio, not its 43% CET1.
- Wayback pass NOT done:
  - WebFetch is blocked from web.archive.org.
  - curl on 2026-09-15 got "Internet Archive: Temporarily Offline".
  - Retry later with:
  `curl 'http://web.archive.org/cdx/search/cdx?url=bankofceylon.co.uk/downloads/*&fl=original,timestamp&collapse=urlkey'`

### Julian Hodge FY2024/25 (item 6) — CLOSED
- Off-domain search found nothing; the only 2024 "Pillar III" hit was hblbankuk.com (a different bank).

### Aldermore FY2011/13 (item 2) — no change, still not found.

## Batch 6 — status (in progress, 2026-09-15)

Rules in force: a mid-run gap closes only when a direct fetch AND a name search both fail. Recent-year
negatives carry the date they were established.

### Metro Bank (item 5, priority)
- Index (re-scraped): annual Pillar 3 2016, 2017, 2018, 2020–2025; H1 editions 2022–2026.
- **FY2015: FOUND by direct fetch, NOT on the index** (verified: `%PDF`, 21 pp, "Pillar 3 Disclosure 31st December 2015",
  with 31 Dec 2014 comparatives):
  https://www.metrobankonline.co.uk/globalassets/legal-information/pillar-3-disclosure-2015.pdf
  (the same folder and pattern as the 2016 edition).
- FY2019: found earlier (metro-bank-pillar-3-2019.pdf), also missing from the index.
- 2011–2014: 12 candidates in legal-information/ (…-disclosure-YYYY, …-disclosures-YYYY,
  metro-bank-pillar-3-disclosure-YYYY) all 404 at ~68,730 bytes, the same as a control path.
- H1 2019–2021: 8 candidates across the three folders all 404. H1 Pillar 3 probably only started in 2022 (CRR2).

### Zenith Bank (UK) (item 2)
- The index https://www.zenith-bank.co.uk/pillar-3/ (re-scraped) still shows 2021–2025 only.
- **Two DIFFERENT FY2023 files exist:**
  - Indexed "final": /media/2260/pillar-3-31dec23-final.pdf (456,587 B, 25 pp, marked "External").
  - Unindexed: /media/2254/31dec23-zbuk-pillar-3-disclosures.pdf (1,044,040 B, 25 pp, different md5).
  - Both have the cover "ZENITH BANK (UK) LIMITED PILLAR 3 DISCLOSURES FOR THE YEAR ENDED 31 DECEMBER 2023".
    Compare the figures; use the final.
- Name search for pre-2021: only the Nigerian parent (zenithbank.com / digital.zenithbank.com) — NOT usable.

### Julian Hodge (item 1)
- The index still stops at the FY2023 Pillar 3 (Hodge-pillar-3-11.03.24.pdf). The FY2024 and FY2025 ARs ARE listed:
  /wp-content/uploads/2025/02/Hodge-annual-report-21.02.25.pdf and /2026/02/Hodge-AR-28.01.26.pdf
- Name search (2nd pass, different wording) found nothing. ARs FY2023–25 contain no Pillar 3 statement.
- File names are date-stamped (e.g. 11.03.24), so a direct fetch can't be permuted.
- **PRA register: Rule 3.1 start 18/02/2025** (plus Ru 1.2 & 2.1(9) from 11/02/2025).
  - FY2025 (y/e 30 Sep 2025) → within the SDDT disclosure exemption.
  - FY2024 (y/e 30 Sep 2024) → NOT covered, so an ordinary negative.

### GHIB pre-2019 (item 6) — NEGATIVE
- `GHIB-2018-Pillar-3-Disclosures.pdf` under /app/uploads/2019/01 … /2019/12 plus a variant: all 404 at 52,403 B
  (same as a control).
- Two name searches found nothing before 2019.
- About-us re-checked 2026-09-15: still no 2025 Pillar 3 (AR 2025 is posted).
- PRA register: no SDDT rows.

### NBE UK 2011–2016 (item 7)
- Eight candidates in /wp-content/uploads/2021/02/ (2016_/2015_Basel_ll_Pillar_3_Disclosure.pdf,
  Pillar_3_30062016_FINAL.pdf, …) all 404 at 90,391 B (same as a control). The 2018 positive control is a real PDF.
- **But the index is PARTIAL for early years:** FS 30 June 2014 (text layer) says "Further details of the Company's
  risk management policies, procedures and exposures, in compliance with the Pillar 3 requirements of the Capital
  Requirements Directive, are published on the Company's website, www.nbeuk.com."
  → FY2014 Pillar 3 existed but wasn't migrated to the current site. Year-end was 30 June through at least 2016.

### Wayback CDX results (the archive was intermittently offline; empty results were re-run with status codes)
- **NBE UK — pre-2017 editions RECOVERED from Wayback.** The live old paths 404 at 90,391 B (removed); use id_ URLs.
  All are verified `%PDF`, with cover periods read (OCR where scanned):
  - FY2010 "Basel II, Pillar 3 disclosures for the year ended 30th June 2010" (20 pp, scanned):
    https://web.archive.org/web/20110419125423id_/http://www.nbeuk.com:80/eng/pdf/financial/pillar_3_20100630.pdf
  - FY2013 "…year ended 30th June 2013", with 30 June 2012 comparatives (22 pp, text layer):
    https://web.archive.org/web/20160824045329id_/http://www.nbeuk.com:80/eng/pdf/mak16139-Pillar_3.pdf
  - FY2015 "…year ended 30th June 2015" (21 pp, scanned):
    https://web.archive.org/web/20160622053404id_/http://nbeuk.com/Pillar3-30062015.pdf
  - FY2016: only a 404 capture of `FINAL-Pillar%203-30062016.login.php`, so the file probably existed; not recovered.
  - FY2011, FY2012, FY2014: no "pillar" capture (FS2014 says published).
- **Bank of Ceylon (UK) — Wayback pass DONE → 2022/2023 closed.**
  - Captures exist for the 2018, 2019, 2020, 2021 and 2024 files, none for 2022/2023.
  - The live site gives genuine 404s. katalysis-36 confirmed this independently: byte-identical 146-byte 404s, same md5.
  - Bonus, FY2013: "Capital & Risk Management Pillar 3 Disclosures 31st December 2013", Co. reg. 06736473 (15 pp):
    https://web.archive.org/web/20150813084438id_/http://www.bankofceylon.co.uk:80/documents/corporate/BOCUK_Pillar_3_2013.pdf
- **Julian Hodge — FY2024 closed.** 28 captures cover every edition 2010–FY2023 at their original upload paths
  (2019/01 … 2024/03) plus the 2024/07 re-uploads. The newest capture is 2025-08, and no FY2024 or FY2025 Pillar 3
  was ever captured.
- **UBL UK:** CDX shows older /media/1081…1368 paths (the same years, earlier uploads) plus
  **/media/vsvfbmui/pillar260825.pdf** (live, `%PDF`, 65 pp). It's "UBL UK Pillar 3 Disclosures Year ended
  31 December 2024" — a SECOND FY2024 version (26/08/25), not a 2025 edition. See the comparison below.
- **Castle Trust — CORRECT live URLs.** The old /docs/default-source/ paths now serve the homepage (the whole site is
  a catch-all, ~258 KB). Files are live under https://www.castletrust.co.uk/wp-content/uploads/ :
  - FY2025: fy-30_sept-2025-ctb-pillar-3-disclosures.pdf (underscore)
  - FY2024: fy-30_sept-2024-ctb-pillar-3-disclosures.pdf (underscore)
  - FY2023: fy-30-sept-2023-ctb-pillar-3-disclosures.pdf (hyphen; the underscore variant soft-404s)
  - FY2022: fy-30-sept-2022-ctb-pillar-3-disclosures.pdf
  - Wayback copies of FY2020–FY2024 exist at the old /docs/default-source/{may-21,apr-22,mar-23,mar-24,mar-25}/ paths.
  - **Entity flag:** the FY2023 and FY2025 covers say "Castle Trust Bank … Registered No: 12161224", the
    Castle Trust Holdings number, not Castle Trust Capital PLC. This is a sub-consolidation basis for the
    peer or user to decide.
- Metro, Zenith, GHIB, Persia and Aldermore CDX: **not done — the Internet Archive returned 503 "Temporarily Offline"**.
- **UBL FY2024 — two versions, numerically IDENTICAL.**
  - Indexed unb-2024-pillar3-approved-finalplusamended.pdf (created 1 Jul) and unindexed pillar260825.pdf (created 26 Aug)
    are both 65 pp, and all 245 numeric tokens match. A re-upload; either is safe.
  - UBL FY2025 is still absent as of 2026-09-15.
- **Castle Trust — live /wp-content/uploads/ also has FY2021 and FY2020** (fy-30-sept-2021-…, fy-30-sept-2020-…, both `%PDF`).
  - So FY2020–FY2025 are all live.
  - Every edition checked (FY2022, FY2024, FY2025) is headed "Registered No: 12161224" and names Castle Trust Holdings
    Limited, with Castle Trust Capital plc as the authorised firm. Entity-basis decision needed.

### Vanquis Bank Limited solo (item 3)
- There is no solo Pillar 3 from 2020.
  - The Provident Financial plc Pillar 3 2020 and 2021 editions (group) are live at https://www.vanquis.com/wp-content/uploads/2025/05/10-05-21_Pillar-3-regulatory-capital-disclosures.pdf
    and …/Provident_Financial_plc_Pillar_3_Disclosures_2021.pdf . Their only "solo" mentions are CCA/leverage template captions.
  - vanquisbankinggroup.com now redirects to https://www.vanquis.com/investors/results-reports-presentations/
- **Solo AR capital figures (entity = Vanquis Bank Limited, Co. 2558509):**
  - AR 2021 (https://www.vanquis.com/wp-content/uploads/2025/05/Vanquis_Bank_Ltd_31_12_2021_Signed.pdf):
    "regulatory capital, on a verified basis, of £381m (2020: £407m), equating to a total CET1 ratio of 32.1% (2020: 33.4%)".
    **Label trap:** "total CET1 ratio" is ambiguous.
  - AR 2025 (https://www.vanquis.com/wp-content/uploads/2026/03/VBL-stats-2025-FINAL-Fully-Signed.pdf, 88 pp):
    "regulatory capital of £385m (2024: £303m), equating to a total capital ratio of 25.9% (2024: 26.4%)".
    Also: "In December 2025, the Company issued £60m of AT1", so CET1 ≠ Tier 1 from FY2025.
  - Also listed: "2-Apr-2025-Vanquis-Bank-Limited-Full-year-results-for-the-year-ended-31-December-2024.pdf" (same folder).
- **Lead:** AR 2021 says "with effect from 31 December 2020 the Company's individual disclosures have been aggregated into
  the consolidated Group Pillar 3 disclosures" (in the remuneration context). Solo disclosures of some kind existed before 2020.

### Other recent re-checks (2026-09-15)
- Persia http index unchanged (still only Pillar 3 2021). Melli: mellibank.com / .co.uk still do not respond.

## Batch 6 — Wayback CDX round 2 (archive back up, 2026-09-15). Every URL below is `%PDF`-checked, with the cover read.

### Metro Bank (item 5)
- **FY2010 (WB):** https://web.archive.org/web/20120717023649id_/https://www.metrobankonline.co.uk/Global/NEW%20WEBSITE%20FILES/Pillar%203%20Disclosures%202010%2031%20December.pdf
  — 18 pp, "METRO BANK PLC Pillar 3 Disclosures 31st December 2010".
- **FY2011 (WB):** https://web.archive.org/web/20130625053953id_/https://www.metrobankonline.co.uk/Global/Legal%20Information/Pillar%203%20Disclosure%20-%202011.pdf — 18 pp.
- **FY2012: CLOSED, not retrievable.**
  - A CDX prefix scan of /Global/ has no 2012 Pillar 3.
  - The name search ("31st December 2012") is negative. Live paths 404.
- **FY2013 (WB):** https://web.archive.org/web/20140915151355id_/https://www.metrobankonline.co.uk/Global/Legal%20Information/Pillar%203%20Disclosure.pdf — 20 pp.
- **FY2014 (WB):** SAME original URL, capture 20151230210842:
  https://web.archive.org/web/20151230210842id_/https://www.metrobankonline.co.uk/Global/Legal%20Information/Pillar%203%20Disclosure.pdf — 21 pp, "31st December 2014".
  **Trap:** one undated filename holds different editions per capture, so always cite the timestamped id_ URL.
- **FY2015:** live (found earlier).
- **Live and `%PDF`-checked:**
  - FY2016: /globalassets/legal-information/pillar-3-disclosure-2016.pdf
  - FY2017: /globalassets/documents/investor_documents/metro-bank-2017-pillar-3-disclosure.pdf
  - FY2018: /globalassets/documents/investor_documents/pillar-3-disclosure-2018.pdf (byte-identical to /globalassets/legal-information/pillar_3_2018.pdf)
  - FY2019 (known)
  - FY2020: /globalassets/investor-relations/metro-bank-plc-pillar-3-2020.pdf
  - FY2021: /globalassets/documents/customer_documents/intermediaries/metro-bank-pillar-3-disclosure-2021.pdf
  - FY2022: /globalassets/documents/customer_documents/business-and-commercial/pillar-3-disclosure-2022.pdf
  - FY2023: /globalassets/pillar-3-disclosure-2023.pdf (byte-identical to …/personal/2023-pillar-3-disclosure-of-metro-bank-holdings-plc.pdf)
  - FY2024: /globalassets/pillar-3-2024.pdf
  - FY2025: /globalassets/documents/investor_documents/pillar-3---2025-final.pdf
  - H1 2022: …/business-and-commercial/pillar-3-disclosure---h1-2022.pdf
  - H1 2023: …/personal/pillar-3-disclosure-h1-2023.pdf
  - H1 2024: …/intermediaries/pillar-3-disclosure-h1-2024.pdf
  - H1 2025: /globalassets/h1-2025-pillar-3-final.pdf
  - H1 2026: /globalassets/documents/investor_documents/metro-bank-pillar-3-30-june-2026.pdf
  - All sit under https://www.metrobankonline.co.uk
- **ENTITY FLAG:** the FY2023 and FY2025 covers read "Metro Bank Holdings PLC" (the new holdco); FY2010–2014 read "METRO BANK PLC".

### Zenith Bank (UK) (item 2)
- **FY2008 (WB):** https://web.archive.org/web/20090424153904id_/http://www.zenith-bank.co.uk:80/documents/ZBL_Pillar_3_Disclosure_Document.pdf
  - 9 pp, "PILLAR 3 DISCLOSURES FOR THE YEAR ENDING 31 DECEMBER 2008". It says "Reviewed December 2008", i.e. before the year end, so check the data date.
- **FY2011 (WB):** https://web.archive.org/web/20130616222348id_/http://www.zenith-bank.co.uk:80/docs/ZBL_Pillar_3_Disclosure_Document_2011.pdf — 17 pp.
- **FY2014 (WB):** https://web.archive.org/web/20160826052010id_/http://www.zenith-bank.co.uk/uploads/ZBL_Pillar_3_Disclosure_Document_2014.pdf — 19 pp.
- **FY2015 (WB):** https://web.archive.org/web/20161128044735id_/http://www.zenith-bank.co.uk/uploads/ZBL_Pillar_3_Disclosure_Document_2015.pdf — 18 pp.
- **FY2016 and FY2019: published, but no retrievable copy.**
  - The archived /pillar-3 index lists them: 2018-04 → uploads/ZBL_Pillar_3_Disclosure_Document_2016.pdf; 2019-02 → /media/1013/zbl_pillar_3_disclosure_document_2016.pdf; 2021-01 and 2021-09 → /media/2177/zenith-bank-uk-limited-pillar-3-disclosure-2019.pdf.
  - Live paths 404, and CDX has no capture of the PDFs.
- **FY2017, FY2018, FY2020: index evidence of NON-posting.** The index showed only the latest edition:
  - it still showed FY2016 in Feb 2019;
  - it still showed FY2019 in Sep 2021.
  - A caveat: no captures exist between 2019-02-15 and 2021-01-27.
- FY2009/2010/2012/2013: no capture.
- Zenith statutory accounts 2009–2024 are all in CDX, useful for capital notes.

### Aldermore (batch 5 leftovers)
- **FY2011 (WB):** https://web.archive.org/web/20230810043035id_/https://www.investors.aldermore.co.uk/system/files/uploads/financialdocs/pillar_3_disclosure_2011_0.pdf
  - 23 pp, "Aldermore Bank Plc Pillar 3 Disclosures December 31 2011". Same md5 as the 2012 capture of aldermore.co.uk/media/54859/aldermore_pillar_3_-_31-12-2011.pdf.
- **FY2013 (WB):** https://web.archive.org/web/20230811224731id_/https://www.investors.aldermore.co.uk/system/files/uploads/financialdocs/pillar_3_disclosure_2013_0.pdf — 22 pp, Aldermore Bank PLC.
- **Entity:** FY2011 and FY2013 are Aldermore Bank PLC. "pillar_3_disclosures.pdf" (WB 20230810043041) is Aldermore GROUP PLC, 31 Dec 2016.
- investors.aldermore.co.uk is now a soft-404 (HTML, 242,659 B).

### Persia International Bank — pre-2021 (bonus; y/e 31 March)
- **FY2016 (WB):** https://web.archive.org/web/20161024202355id_/http://www.persiabank.co.uk/Pillar%203%20Disclosure%20as%20at%2031%20March%202016.pdf — 21 pp.
- **FY2018 (WB):** https://web.archive.org/web/20180902131909id_/http://www.persiabank.co.uk/Pillar%203%20Disclosure%20as%20at%2031_03_2018%20(final).pdf — 27 pp.
- **FY2020 (WB):** https://web.archive.org/web/20220125010012id_/http://www.persiabank.co.uk/Pillar%203%202020%20v7.pdf — 28 pp, "31 MARCH 2020".
  - The v6 capture (20211207051625) is TRUNCATED at exactly 1,048,576 B, so don't use it.
- **FY2015 (WB):** https://web.archive.org/web/20160316221826id_/http://www.persiabank.co.uk/Pillar3_disclosures_March%202015.pdf
  - 18 pp, scanned. The OCR cover reads "PERSIA INTERNATIONAL BANK PLC LONDON Pillar 3 disclosures 31 March 2015".
  - Basel II basis; it "forms part of the Annual Report and Financial Statements 31 March 2015".
- FY2017, FY2019: no capture.

### GHIB pre-2019 — CLOSED
- A full `mimetype:application/pdf` CDX of ghanabank.co.uk has no Pillar 3 before the FY2019 edition (uploaded 2020/11).
- There are no PDF captures at all between 2005 and 2020, so this is "not retrievable" rather than proof it was never published.

### Vanquis solo — CLOSED
- The vanquisbankinggroup.com CDX shows group Pillar 3s only: PF plc 2009–2021, VBG 2022–2023, plus H1 2023/24.
- PF plc Pillar 3 2019 §9 says the "separate, standalone document … on www.vanquisbank.co.uk" is the **Remuneration Code** Pillar 3.
  The AR 2021 "individual disclosures aggregated" line is in that remuneration context.
- There was never a solo capital Pillar 3. The group 2019 edition has divisional exposures only, with no solo capital table.

### Recent-year re-check (established 2026-09-15)
- **GTBank UK — FY2023 negative REVERSED; FY2025 FOUND.**
  - FY2023: https://gtbank-uk.files.svdcdn.com/production/general/GTBank-UK-Pillar-3-2023.pdf (26 pp, 31 Dec 2023).
    A second copy, …/GTBUK-Pillar-3-2023.pdf (27 pp), has identical figures; only page refs differ.
  - FY2025: https://gtbank-uk.files.svdcdn.com/production/general/GTBank-UK-Pillar-3-Disclosure-2025.pdf (26 pp, "For Period Ended 31st December 2025", created 23 Jul 2026).
- **NBKI FY2023 — still negative.**
  - The nbk.com "Pillar III Report Year 2023/2024" (jcr:6ed10da3…, jcr:7ba4c7e4…) are **NBK France SA**. DO NOT USE.
  - Bonus FY2014 NBKI (1 page): https://www.nbk.com/dam/jcr:a00ed21f-7439-433a-a8e3-46fb7f495fa9/NBK-(International)-PLC-Pillar-3-Disclosures-2014.pdf
- **Kingdom Bank — LINK ROT: every previously cited Pillar 3 URL now 404s live** (2021/03, 2021/07, 2023/04, 2024/05).
  - Wayback copies:
    - FY2019 (approved 14 May 2020): https://web.archive.org/web/20230321070013id_/https://www.kingdom.bank/wp-content/uploads/2021/03/5ee1ea4628eaae3b944cb122_Pillar-3-Disclosures-approved-14-May-2020.pdf
    - FY2020 (approved 3 Jun 2021): https://web.archive.org/web/20240701022732id_/https://www.kingdom.bank/wp-content/uploads/2021/07/Pillar-3-Disclosures-approved-3-June-2021-v2.pdf
    - **FY2021 (approved 9 Jun 2022; never in our earlier list):** https://web.archive.org/web/20240617063554id_/https://www.kingdom.bank/wp-content/uploads/2022/06/Pillar-3-Disclosures-2021-approved-9-June-2022-clean-v2.pdf
  - FY2022/FY2023: CLOSED, not retrievable.
    - Wayback 2023/04 serves only a "One moment, please…" bot page, and 2024/05 was never archived.
    - Live /about/oversight/ links only KBL-Statutory-Accounts-2025.pdf.
  - Register: Rule 3.1 from 20/02/2025.
  - KBL-Statutory-Accounts-2024.pdf (live; y/e 31 Dec 2024) says: "The Bank has submitted a modification by consent
    to join the SDDT regime … [under] the SDDT regime the Pillar 3 disclosure document will not be required in future years."
- **Methodist Chapel Aid — LINK ROT.** /media/ngqlqg5o/ (2023) and /media/honer1yl/ (2022) now 404, and the index links no Pillar 3.
  - Live: FY2022 at https://www.mcafundingforchurches.co.uk/siteFiles/resources/pdf/Pillar3disclosures2022.pdf
  - Wayback:
    - FY2019: https://web.archive.org/web/20200930032441id_/http://mcafundingforchurches.co.uk/sitefiles/resources/pdf/pillar3disclosures2019.pdf
    - FY2020: https://web.archive.org/web/20210515024743id_/https://www.mcafundingforchurches.co.uk/sitefiles/resources/pdf/pillar3disclosures2020.pdf
    - FY2021: https://web.archive.org/web/20220625084136id_/https://www.mcafundingforchurches.co.uk/sitefiles/resources/pdf/2021-pillar-3-disclosures.pdf
    - FY2023: https://web.archive.org/web/20250407005711id_/https://www.mcafundingforchurches.co.uk/media/ngqlqg5o/pillar-3-disclosures-2023.pdf
  - **Register: Rule 3.1 from 11/04/2024**, so FY2024/FY2025 are consistent with the SDDT exemption.
    Index captures from Apr 2025, Sep 2025 and Jan 2026 list the AR and CBCR 2024 but no Pillar 3.
- **Reliance:** the WP media library (`/wp-json/wp/v2/media?search=pillar` and `=disclosure`) holds FY2020 (x2), FY2021, FY2022 and FY2023 (31 Mar) only.
  Register Rule 3.1 from 05/04/2024, 5 days after the FY2024 y/e, so the FY2024 disclosure would fall due after the opt-in. Peer to rule.
- **Hampden:** FY2024/25 negative.
  - 6 name patterns × 2 hosts all 404, and CDX has none.
  - The 2023 "_2024-07-10-095416_sxcs.pdf" path is byte-identical to the indexed one.
  - Register Rule 3.1 from 25/04/2024.
- **Griffin:** /reports lists only the FY2023 Pillar 3, CDX has none, and the name search is negative. Register Rule 3.1 from 05/03/2024.
- **Cynergy:** the page still lists 2018–2023. Asset version hashes changed for 2021/2023, but old and new URLs are byte-identical. Register Rule 3.1 from 17/01/2025.
- **StreamBank FY2026:** every candidate returns the catch-all soft-404 (25,989 B HTML), and CDX has none.
- **UBI UK:** the index now lists /Portals/0/pdf/Final_Pillar_3_Disclosure-31-03-2025.pdf (FY2025). FY2026 is still absent.
- **Afin FY2025:** the media library holds only the FY2024 edition (posted Sep 2025). The register has criteria rows only, so not exempt; perishable.
- **Turkish Bank FY2025:** the media library holds only the Feb 2026 upload (31 Dec 2024).
- **Castle Trust:** /wp-content/uploads/2025/05/Pillar-3-Document.pdf is a byte-identical copy of FY2024.
- **Arab Bank Europe:** the important-information page has a new 202602_EABAnnualReport_v9.pdf but no Pillar 3.

### ICICI Bank UK PLC (item 4) — CLOSED, complete run (2026-09-15)
- The live index at https://www.icicibank.co.uk/personal/basel-disclosures lists 19 annual editions, FY2008 to FY2026 (y/e 31 March).
  Every one is `%PDF`, and I read the period on each cover. No gaps. All paths are under https://www.icicibank.co.uk/content/dam/icicibank/icici-assets/uk/ unless noted:
  - FY2008 basel2_disclosures_FY2008.pdf
  - FY2009 Basel_II_p3_Disclosure_Statement.pdf
  - FY2010 basel2_disclosures_FY09_10.pdf
  - FY2011 basel2_disclosures_FY10_11.pdf
  - **FY2012 basel2_disclosures_March31_11.pdf.** FILENAME TRAP: the content reads "ended March 31, 2012", despite the "_11" name.
  - FY2013 disclosures2012-13.pdf
  - FY2014 disclosures2013-14.pdf
  - FY2015 basel3-disclosures-FY14-15.pdf
  - FY2016 basel3-disclosures-FY15-16.pdf
  - FY2017 basel3-disclosures-FY16-17.pdf
  - FY2018 basel3-disclosures-FY17-18.pdf
  - FY2019 ICICI_Bank_UK_Pillar3_disclosures_FY2018-19.pdf
  - FY2020 ICICI_Bank_UK_Pillar3_disclosures_FY2019-20.pdf
  - FY2021 ICICI-Bank-UK-Plc-Pillar3-disclosures-FY2020-21.pdf
  - FY2022 ICICI-Bank-UK-Plc-Pillar3-disclosures-FY2021-22.pdf
  - FY2023 icici-bank-uk-plc-pillar-3-disclosures-FY2022-23.pdf
  - FY2024 at a different folder: https://www.icicibank.co.uk/content/dam/icicibank/india/managed-assets/docs/pdf/basel-pillar-3-disclosures-FY2023-24.pdf
  - FY2025 basel-pillar-3-disclosures-FY2024-25.pdf
  - FY2026 at a different folder: https://www.icicibank.co.uk/content/dam/icicibank-revamp/uk/doc/basel-pillar-3-disclosures-FY2026.pdf
- FY2008–FY2014 are 10–21 pp Basel II documents.
- The Wayback CDX (icicibank.co.uk, PDF filter) holds only the same files under older paths (/pdf/Basal_Disclosures/, /managed-assets/docs/). Nothing is missing from the index.

## Batch 7 — link-rot sweep of every cited PDF (started 2026-09-15 ~21:20)
- **Input:** the peer's snapshot, research/cited_urls.tsv (columns url, kind, scripts). 1,134 rows = 1,035 live + 99 wayback. File mtime 21:18.
  Do NOT re-extract from scripts; five agents are editing them.
- **Scratchpad:** checker lr_check.py; stage inputs lr_stage*.json; results lr_res_stage*.jsonl, one JSON per URL.
- **Checker:** curl with browser UA + Referer + Accept, reading the first 2 KB. Hosts run in parallel, one fetch at a time per host.
- **Classes:** OK_PDF (body starts %PDF), SOFT404? (2xx but not a PDF), DEAD (404/410), BLOCKED? (401/403/429/503/5xx-CDN), SERVER_ERR, ERROR.
  **BLOCKED is never DEAD** without independent confirmation; nbeuk.com's 403 was a WAF.
- **Stages:**
  - 1 = 583 small-host live PDFs (highest yield)
  - 2 = 452 big-host live PDFs (21 hosts; run last, rate-limit risk)
  - 3 = 99 wayback rows
- **Deliverable per failure:** script(s), dead original (kept on record), and a verified Wayback id_ replacement or "no capture".
  Retrieval check only; no figure checking.
- **Status:** stages 1 and 3 running.

### Batch 7 partial results (checked ~21:25–21:50)
- **Stage 1 (583 small-host PDFs):** 540 OK_PDF, 18 DEAD, 11 BLOCKED?, 8 SOFT404?, 6 ERROR.
- **Stage 2 (452 big-host):** 451 OK_PDF, 1 DEAD. The big hosts are essentially clean.
  - The one DEAD: tsb.co.uk /investors/results-and-reports/TSB-Significant-Subsidiary-Disclosures-2015.pdf (build_tsb.py).
- **Stage 3 (99 wayback):** in progress. The first 15 ERRORs were archive connection timeouts on my side, so they get re-run; they are not dead snapshots.
- **Shawbrook (build_shawbrook.py): 7 DEAD, all RELOCATED live** on /about-us/investors/results-centre/.
  All replacements are `%PDF`, and the year/entity was read from each cover:
  - …/media/qsxpg41l/shawbrook-pillar-3-disclosures-2014.pdf → https://www.shawbrook.co.uk/media/cc5dq5j0/pillar-3-2014.pdf (Group plc, 31 Dec 2014)
  - …/wdvhqxsn/…-2015.pdf → https://www.shawbrook.co.uk/media/4galhsik/pillar-3-2015.pdf (Group plc)
  - …/1lhngswy/…-2016.pdf → https://www.shawbrook.co.uk/media/koignkmo/pillar-3-2016.pdf (Group plc)
  - …/3lifgtxe/…-2017.pdf → https://www.shawbrook.co.uk/media/3wefl2tu/pillar-3-2017.pdf (Group plc + App. 1 Shawbrook Bank Ltd)
  - …/kfnfg0oe/…-2018.pdf → https://www.shawbrook.co.uk/media/vypjeoat/pillar-3-2018.pdf (App. 1 Shawbrook Bank Ltd)
  - …/2azlz2vz/…-2019.pdf → https://www.shawbrook.co.uk/media/yhdl0kcs/pillar-3-2019.pdf (31 Dec 2019)
  - …/xexpjjkq/…-2020.pdf → https://www.shawbrook.co.uk/media/zlibpqlt/pillar-3-2020.pdf (Group plc, 31 Dec 2020)
  - Also live: 2012/2013 (Shawbrook Bank Limited) and 2021–2025, plus an H1 2026 Pillar 3.
- **Bank Sepah (5 URLs):** the PDFs are present, but the site's TLS certificate has EXPIRED (curl error 60). Live file OK; a browser will warn.
- **Persia 2021 v3:** the https:// form gives a connection reset, but the **http://** form serves the PDF. Cite http.
- **QIB UK (4 annual reports):** "Request Rejected" (F5 WAF) with 247-byte HTML. This is BLOCKED, not soft-404.
- **eabplc.com (4 URLs, build_arab_bank_europe.py):** a genuine soft-404 serving the "Home - Arab Bank Europe" page.
  - These include Pillar3EAB_PLC_2024.pdf and Pillar3.pdf, which are STILL cited.
- **FirstBank UK (6 Pillar 3s, build_firstbank_uk.py):** all DEAD. The site now links only ARs 2024/2025, and the WP media search is empty.
- **UTB:** FY2024 Pillar 3 DEAD; the site now lists only 2025. The WP REST API is restricted.
- **Redwood** 2021 getmedia URL, **Rathbones** 2024 Pillar 3 and **UBA UK** AR 2018 are DEAD; replacements being searched.
- **BLOCKED? (403 even with alternate headers):** pnb.com.ph (5), itau.com.br (3), alphabanklondon.co.uk (2), starlingbank.com (1).
  Being confirmed with a second client (WebFetch), plus a Wayback fallback.

### Batch 7 — update ~22:05 (partial 1 SENT to peer)
- **Additional live replacements (verified):**
  - **Rathbones** 2024 → https://www.rathbones.com/sites/main/files/results_and_presentations/files/31_december_2024_pillar_3_disclosures.pdf
  - **UBA UK** AR 2018: same path on the new domain → https://www.ubauk.com/wp-content/uploads/sites/29/2019/07/UBA-UK-Ltd-Report-and-Accounts-31-Dec-2018.pdf
  - **Redwood** 2021 → https://redwoodbank.co.uk/media/u5sb3ky5/redwood-pillar-3-2021-1.pdf (Kentico /getmedia/ → Umbraco /media/ migration)
  - **Alpha Bank London:**
    - The 2019 FS URL is truly DEAD (WebFetch 404) → https://www.alphabanklondon.co.uk/sites/default/files/2025-10/ABL%20Financial%20Statements%202019.pdf
      (72 pp, 31 Dec 2019; fetched via WebFetch because curl gets a WAF 403).
    - The 2020 FS URL is FINE (WebFetch gets the PDF).
- **BLOCKED (curl ×2 header sets + WebFetch all refused):** PNB 5, Itaú 3, Starling 1, QIB 4.
- **Stage 3:** 72 OK. The 27 connection timeouts are being re-run (lr_res_stage3b.jsonl).
  Forms: 19 id_, 65 bare /web/<ts>/, 15 if_. The non-id_ rows still serve raw %PDF.
- **Queued Wayback fallback** (lr_fix_out2.jsonl; the script now separates ARCHIVE_UNAVAILABLE from NO_CAPTURE):
  FirstBank UK 6, UTB 2024, eabplc 4, TSB 2015, plus the BLOCKED rows.
- **Lesson:** web.archive.org throttled me when stage 3 and ad-hoc CDX queries ran concurrently, and the connections timed out.
  An earlier lr_fix version would have recorded those failures as "no capture". It was killed and patched.

### Recent-year re-checks (2026-09-15)
- UBL UK: annual-reports page still has no 2025 Pillar 3. PRA register: no SDDT row.
- Castle Trust Capital PLC: PRA Rule 3.1 start 06/01/2026 → covers FY2026 (y/e 30 Sep 2026), not FY2025.
- Melli Bank: mellibank.com is still unreachable (no response on http or https).

## Searched and found nothing (don't repeat)
- Bank of Ceylon (UK) Pillar 3 2022/2023, off-domain (name + "Liquidity Coverage Ratio").
- Nomura NEHS annual editions 310325 / 310326: search found nothing, and a direct fetch
  under both prefixes returns 404. (310322 and 310323 now RESOLVED but exclude NBI — see section 1.)
- Nomura Bank International plc own Pillar 3 / "CET1 ratio" / "own funds".
- (Secure Trust Bank 2017–2019 — now FOUND, see section 3; `-final` slug guesses 404.)
- Paragon Bank PLC "individual basis" / "solo" Pillar III.
- Recognise Bank / "Recognise Financial Services" Pillar 3 before 2023.
- Aldermore 2011 / 2013 by filename and by investor-archive search.
- Metro Bank 2012/2013; Vanquis Bank 2011–2013; Zenith Bank (UK) 2011–2013;
  PNBIL 2010–2014; Clydesdale 2011–2013 (see notes above for why each is closed).

## Mid-way when the checkpoint was requested
- (Done after checkpoint: Secure Trust resolved via its paginated results index;
  Recognise enumerated via its investors page — see sections 3 and 5.)
- Nomura: FY2022 and FY2023 NEHS editions are resolved and are SOURCED NEGATIVE for NBI
  (see section 1).
  - Still open: whether the FY2024 edition likewise excludes NBI, and whether NBI's own
    annual reports carry capital ratios (a solo-basis fallback).
- Still open — Aldermore FY2011/FY2013 (optional era); no index page located.

---

## Earlier batches — revisions / corrections
- **Batch 3:** nothing revised since it was sent. Open caveats restated:
  - Turkish Bank (UK): the only Pillar 3 on its index is labelled "2024" but was
    uploaded Feb 2026 (/wp-content/uploads/2026/02/PILLAR-3-DISCLOSURE.pdf) — check
    the period date inside.
  - CAF Bank FY2025: the bank's own page claims SDDT exemption. Per katalysis-36's
    method note, only a PRA **Rule 3.1** modification removes the obligation —
    confirm against the PRA waivers register before closing the cell. Same for
    StreamBank FY2026 (its FY2025 Pillar 3 says it was confirmed in the SDDT regime
    from Jan 2025).
  - Cynergy: Pillar 3 links on /strong-and-prudent-management are JS-rendered — curl
    and grep for `assets.ctfassets.net/xzmqg68ot16t` to enumerate years.
  - Arab Bank Europe: /important-information/ lists "Pillar III Disclosures" but the
    href wasn't captured — grep the raw HTML.
  - **CORRECTION (reported by katalysis-36):** the batch-3 Arab Bank Europe URLs `Pillar3EAB_PLC_2024.pdf`
    and `Pillar3EABplc2023.pdf` are SOFT-404s.
    - They return HTTP 200 with Content-Type text/html: identical 95,415-byte bodies that are the homepage.
    - Wayback CDX over eabplc.com shows the Pillar 3 series 2009–2020, then FY2022; there is NO FY2021,
      FY2023 or FY2024 capture → enumerated-absent.
- **Standing check from batch 5 on:** every URL reported is verified to start with the `%PDF` magic bytes
  (curl range 0-4) and to have a PDF Content-Type. A status code alone is not enough, and identical byte
  counts across URLs mean a catch-all handler.
- **Batch 2:** Castle Trust FY2023 URL
  (castletrust.co.uk/docs/default-source/financial-statements/mar-24/fy-30-sept-2023-ctb-pillar-3-disclosures.pdf)
  — **SOFT-404 per a curl check on 2026-09-15:** HTTP 200 but text/html, 258,831 bytes, not a PDF.
  (WebFetch had failed on castletrust.co.uk's malformed headers.)
- **Corrections reported by katalysis-36 (2026-09-15):**
  - Oxbury: the batch-3 "one Pillar 3 on oxbury.com/annual-reports/" was a snapshot. A same-day re-fetch shows
    2023 + Dec 2024 + Dec 2025 at /media/3yknkp3i/ and /media/yqqdu010/ (~30 cells filled).
    → Recent-year negatives are perishable; date them.
  - Turkish Bank (UK): the Pillar 3 is 31 Dec 2024. The "2025" came from an unfilled board-approval placeholder
    ("approved … on xx 2025"). The comparative column is mislabelled T-4 instead of T-1.
  - CAF Bank: PRA Rule 3.1 starts 08/08/2025, after FY2025's 30 Apr 2025 year-end → FY2025 is NOT exempt; FY2026+ is.
  - StreamBank: Rule 3.1 starts 04/05/2024, but it still published a full FY2025 Pillar 3 → FY2026 not recorded as exempt.
  - Cynergy: the FY2023 Pillar 3 restates FY2022 LCR/NSFR (249.66%/144.09% vs 315.98%/149.48% in the FY2022
    edition) → assume restatement; keep both. The FY2022 Castle
  Trust Pillar 3 is headed "Registered No: 12161224" = Castle Trust Holdings Ltd.
- **Reported back by katalysis-36:** Kingdom Bank's three wp-content URLs now 404, and a
  CDX sweep found no captures, so those years are unrecoverable. The NBK file named
  "Pillar III Disclosures 2023.pdf" is NBK France SA (EUR), not NBK International.
  Havin's decoded index lists Pillar 3 only to 2019 (the rest are "available upon request").
