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
  - **METHOD NOTE (2026-09-16):** "2014–2018 same pattern" above was an INFERENCE from the 2010–2013
    filenames, written into a list that otherwise read as verified. It happened to be right, but it
    should not have been stated that way.
  - **VERIFIED 2026-09-16** after katalysis-36 reported this directory as a catch-all soft-404 serving
    text/html. It is not, from this client. All seven tested return `200 application/pdf`, `%PDF`, with
    DISTINCT md5s and sizes — 2010 299,440 B / 27 pp "as at 31 October 2010"; 2014 351,821 B / 23 pp
    "as at 31 October 2014"; 2016 774,618 B / 34 pp; 2018 876,285 B / 37 pp (2011/2012/2013 also
    application/pdf, distinct md5s). Identical bodies are the soft-404 tell and they are absent here.
    Two clients disagree about this host; do not repoint citations until that is resolved.
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

### Batch 7 — update ~21:55 by system clock (PARTIAL 2a SENT ~22:00)
- **Sent in 2a:**
  - ABE: 3 id_ URLs, using Pillar3.pdf at the CITED timestamp 20240714131343 (35pp, intact).
  - FirstBank 6 (incl. 2020 20231206074745id_ 36pp, Dec-2022 20240219211830id_ 39pp, Dec-2023 20240527034030id_ 33pp, Dec-2024-1 20251203042809id_ 39pp).
  - UTB 20250913035253id_ (13pp); TSB 2015 20221214093332id_ (37pp).
  - Itaú and PNB 2017/2019 fallbacks.
  - No exact-URL capture: PNB 2015, 2016 and storage; Starling 2019; QIB 4.
  - The AIB CH reversal, the negatives that hold, Hodge info and the Melli CH statements.
- **Still owed in 2b:**
  - The 80 id_ conversions (lr_res_stage5.jsonl).
  - Stage-3 rows still pending: FCE 2008, Vanquis 2017, SMBC ×2, UBL 2018. FCE 2016/2010/2006 are already OK in id_ form.
  - ABE domain CDX and the md5 of 20240714 vs 20250505 (lr_res_stage6.jsonl).
  - Melli Wayback results.
- **Background jobs:** stage5.sh (task bclpvsv9r), then stage6.sh (task bn90w0ght), which waits for stage 5.
- **~22:05: ALL 8 remaining stage-3 priority rows now have a working id_ form** (lr_res_stage5.jsonl), at the same timestamp as cited:
  - FCE 2016 AR 167pp, 2010 AR 129pp, 2006 AR 100pp, 2008 AR 140pp
  - Vanquis pfg_pillar_3_report-2017 28pp (20220703024108id_)
  - SMBC pillar3-31-03-15 39pp (20240527065243id_), smbce-pillar3-2020 60pp (20240527071545id_)
  - UBL pillar-iii-disclosure-2018 63pp (20250804031750id_)
  - So no stage-3 citation is left without a working form. Those 8 had only been failing on archive connection timeouts.
- **More live negative re-checks (~22:10). All HOLD:**
  - Turkish Bank FY2025: /reports/ newest is "Pillar 3 Disclosure 2024" (the 2026/02 PILLAR-3-DISCLOSURE.pdf). The WP media search for "pillar" returns only that one item.
  - UBI UK FY2026: /disclosures/financial-reports lists Pillar 3 editions 31-03-2015 through Final_Pillar_3_Disclosure-31-03-2025 and nothing for 2026. My href filter found no 2026 accounts PDF path either, although the script says the page lists "Financial Accounts 31-03-2026".
  - Griffin: griffin.com/legal and /regulatory-information are 404. The cms.griffin.com Strapi upload API returns 502, so it can't be used. The script's negative stands on its own evidence, and this check was inconclusive.
- **Stage 5 slowed at row 10 (~22:10):**
  - Row 10 is Zenith 2014, 20160826052010id_. No curl of mine is running, so the verifier is in its backoff and the archive is throttling again. Leave it alone; don't add archive load.
  - A curl from ANOTHER session (relative path eab_pillar3.pdf, a different UA) was fetching the ABE Pillar3.pdf capture at the same time. That is probably the peer acting on partial 2a. Archive throttling is shared across sessions, so slow rows now are not evidence of absence.
  - UBI UK: the script cites only the unionbankofindiauk.co.uk index page, with no PDFs, so there is nothing to link-rot-check.
### Batch 7 — stages 5/6 COMPLETE (~22:05–22:20)
- **id_ verification: 84 rows, 81 OK_PDF, 3 TRUNCATED_1MiB.**
  - **DO NOT convert these three to id_** — the id_ capture is truncated at exactly 1,048,576 bytes, while the cited bare/viewer form still works:
    - build_bank_of_africa_uk.py 20220519120942 BMCE___Pillar_III_VF___31122017.pdf
    - build_gulf_international_bank_uk.py 20220518000354 2020-GIBUK-Pillar-3_Final.pdf
    - build_gulf_international_bank_uk.py 20230329132856 2021-GIBUK-Pillar-3_Final.pdf
  - Stage 7 is looking for untruncated alternative captures for those three.
  - The 2 credit_suisse year-only `/web/2024id_/` rows BOTH resolve fine: 2021 edition 85pp, 2022 edition 71pp, covers "Credit Suisse International / Basel III / <year> Pillar 3".
- **ABE Pillar3.pdf edition question RESOLVED.** The cited capture 20240714131343id_ and the newest 20250505164839id_ have the SAME md5 (f79e76794db045a963b40fde1da8ebea), 35pp, 3,074,106 bytes. Same document, so there was no edition risk after all — but the CDX digest list does show TWO distinct versions at that URL: 20240713003435 (1,036,749 WARC bytes, a different digest) and 20240714131343. Keep citing 20240714131343.
- **ABE older Pillar 3 editions EXIST in the archive**, at a different path from the one the script probed (`/files/PDFs/`, not `/downloads/`). All 200 application/pdf:
  - 2012 `3.4 - EAB 2012 Pillar Three.pdf` 20161108212856; 2013 20161108212844; 2014 (CRDIV) 20161108192950; 2015 20161108212906
  - 2016 `Pillar 3/EAB 2016 Pillar 3 - CRDIV_FINAL.pdf` 20220707074618; 2017 20210918014857; 2018 `Pillar 3/Pillar III Disclosure 2018.pdf` 20210918014555
  - 2019 20210918015853; 2020 20210918020429; plus 2009 and a v13 from 2010
  - The workbook covers FY2021–FY2024, so these are out of range today, but they matter for any year extension. arabbankeurope.com has NO archived Pillar 3 captures at all.
- **Melli — what it ever published (both verified id_, entity confirmed "Registered number 4152338"):**
  - FY2014: https://web.archive.org/web/20170407223115id_/http://mellibank.com/PDFs/Melli%20Bank%20P3%20Disclosures%20as%20at%2031%20December%202014%20FINAL.pdf (16pp, "As at 31st December 2014")
  - FY2016: https://web.archive.org/web/20190405190315id_/http://mellibank.com/File/DownloadReportFiles?filename=Melli%20Bank%20-%20Pillar%203%20%20Disclosures%202016%20-%20Final.pdf (23pp, "As at 31st December 2016")
  - Also archived on the old domain: mellibank.co.uk 20160221234533 (the same FY2014 document, 159,723 bytes).
  - The mellibank.com CDX from 2019 shows ARs 2002–2008 and 2016 plus compliance PDFs, and NO Pillar 3 later than the FY2016 edition. Captures from May 2026 exist for compliance files, so the domain was still being crawled — the absence of a FY2023 edition is not simply "nothing was captured". Stage 7 checks the /reports page listings.
- **Stage 6 covers — all 13 replacements confirm entity and period:** FirstBank "FBN Bank (UK) Limited"/"FirstBank UK Limited" Pillar 3 as at 31 Dec 2019/2020/2021/2022/2023/2024; UTB "UTB Partners Plc ... as at 31 December 2024"; TSB "TSB Banking Group plc Significant Subsidiary Disclosures"; PNB "Philippine National Bank (Europe) Plc"; ABE AR "31 December 2024".

### Batch 7 — stage 7 results + PARTIAL 2b SENT (~01:00)
- **PARTIAL 2b sent:** the full per-script id_ conversion list (81 OK), the 3 do-not-convert rows, the ABE md5 resolution, the ABE 2012–2020 finds, and the Melli answer.
- **BOA UK is solved LIVE, not by archive** (better than converting):
  - FY2017 → https://www.bankofafricaunitedkingdom.co.uk/pdfs/finances/BMCE___Pillar_III_VF___31122017.pdf (32pp, "2017 PILLAR III DISCLOSURES", reg 5321714)
  - FY2015 → https://www.bankofafricaunitedkingdom.co.uk/pdfs/finances/BMCE___Pillar_3_disclosures____2015.pdf (5pp, "BMCE BANK INTERNATIONAL plc ... FOR THE YEAR 2015")
  - The site moved these from /assets/<n>/ to /pdfs/finances/. The Wayback path /assets/0/BMCE___Pillar_3_disclosures____2017.pdf is a 404 capture, so /assets/239/ was the only archived 2017 copy.
- **GIB UK 2020/2021: only ONE 200 capture exists for each** (20220518000354 and 20230329132856), so there is no alternative timestamp to switch to. gibam.com now 404s on the 2020, 2021 AND 2022 asset paths and has no disclosures index page, so live is not an option either.
  - Stage 8 is testing whether the CITED bare form plays back complete, or is truncated like the id_ form. If the bare form is complete, leave those two citations exactly as they are.
- **Melli /reports page captures run 2017 → 17 May 2026** (17 captures). Stage 9 reads the 2026, 2025, 2023 and 2021 listings to test the FY2023 "on the website" statement.
  - The mellibank.com DownloadReportFiles CDX lists ARs 2002–2008 and 2016 plus the FY2016 Pillar 3 — and NO Pillar 3 after FY2016.

### Batch 7 — PRIORITY: GIB UK has no working form (~01:10, sent to peer)
- **build_gulf_international_bank_uk.py FY2020 and FY2021 Pillar 3 are UNUSABLE in every form.**
  - bare (cited), if_ AND id_ all return exactly 1,048,576 bytes with no pdfinfo page count. md5 edfe2438dbff06fdc617e6a38efb6059 (2020) and 32d6206989581714144f61ffc6982ab5 (2021), identical across the three forms, so the CAPTURE is truncated, not the playback.
  - Only ONE 200 capture exists per URL (20220518000354, 20230329132856); every other capture of those paths is a 404.
  - Live: gibam.com 404s on the 2020, 2021 and 2022 asset paths, no disclosures index page; gibuk.com does not resolve; gib.com is 403 to BOTH curl and WebFetch = BLOCKED, not a negative.
  - Stage 10 sweeps gib.com/gibam.com for a differently-named copy.
  - **Lesson:** a %PDF magic-byte check cannot see a truncation 1 MiB into the file. Only the full download plus a pdfinfo page count catches it. That is why stages 5/6/8 downloaded in full.
- **Melli /reports page, ALL captures (Sept 2021, Apr 2023, Jun 2023, Jun 2025, Feb 2026, May 2026):**
  - "Financial Statements and Pillar 3 Disclosures are available on request."
  - So the site said "on request" throughout, and the FY2023 AR's "available on the Bank's website" is NOT corroborated by any capture. No Pillar 3 later than FY2016 is archived on the domain, and captures continue into May 2026, so this is not a crawl gap.
  - Melli's only public Pillar 3 documents remain FY2014 and FY2016 (both verified id_, sent in 2b).

- **Stage 10 (archive sweep for a usable GIB UK copy) — NOTHING FOUND, and a trap to avoid:**
  - gibam.com holds exactly three GIBUK Pillar 3 assets ever: 2020-GIBUK-Pillar-3_Final.pdf, 2021-GIBUK-Pillar-3_Final.pdf (both the truncated captures) and 2022-GIBUK-Pillar-3-disclosures_VF.pdf (fine, 33pp). No differently-named GIB UK edition exists on the domain.
  - gib.com has MANY Pillar 3 PDFs, but they are all OTHER ENTITIES: Gulf International Bank B.S.C. (the Bahrain parent), the KSA entity (/ksa/) and the Abu Dhabi branch. **ENTITY-BASIS RULE: none of these may be substituted for GIB UK's own disclosure.** Flagged to the peer so they are not mistaken for candidates.
  - So GIB UK FY2020/FY2021 currently have NO retrievable Pillar 3 source in any form.

### Batch 7 — GIB UK: the "unrecoverable" verdict below is WITHDRAWN (corrected 2026-09-16, see SUPERSEDED note)
- **Every route tried and exhausted for FY2020/FY2021:**
  - Wayback: one 200 capture each; bare/if_/id_ all return the same 1,048,576 truncated bytes (md5-identical per year).
  - **PDF repair fails:** qpdf "can't find startxref" (the truncation removed the xref table at the file's end); Ghostscript rebuilt only a 2,431-byte single BLANK page from both. No page content survives, not even page 1.
  - Live gibam.com: 404 on 2020/2021/2022 asset paths; /regulatory-information, /literature-library, /important-information all 404.
  - **NEW HOST (does not help):** documents moved to CDN gib-am.files.svdcdn.com. The live Policies and Governance page (gibam.com/insights/policies-and-governance) lists only the 2024 Pillar 3. The CDN has 2023 + 2024 only; ~10 permutations for 2020/2021/2022 404; a Wayback sweep of the CDN host returns only those two files.
  - Memento aggregator, Common Crawl CC-MAIN-2023-50, archive.today: nothing. Web search: 2022/2023/2024 only.
  - gib.com responds 200 to browser headers (the earlier 403 was a WRONG PATH, so gib.com is reachable, not blocked). All its Pillar 3 PDFs are GIB B.S.C. (Bahrain parent), /ksa/ or the Abu Dhabi branch — **ENTITY-BASIS RULE: never substitutable.** Flagged to the peer because they look like hits.
  - Route left for the PEER (a read, not retrieval): the FY2022 edition is retrievable (20240223164517id_, 33pp) and FY2023 is live on the CDN; if FY2022 carries a FY2021 comparative, FY2021 is sourceable. FY2020 has no such route.
- **Defect class bounded (answering the peer's question):** of the 84 archive citations verified by FULL download + page count, exactly 3 failed — BOA UK 2017, GIB UK 2020, GIB UK 2021 — and BOA was rescued live.
- **SUPERSEDED 2026-09-16 — the unretrievable set is EMPTY.** All three truncated captures were recovered
  in full by `gs -o fixed.pdf -sDEVICE=pdfwrite <truncated>`: GIB UK FY2020 → 795,035 B / 38 pp, GIB UK
  FY2021 → 697,523 B / 30 pp, BOA UK 2017 → 981,636 B / 32 pp (cover "Company Registration N°5321714",
  the UK entity). Reproduced byte-for-byte against katalysis-36's independent run.
  **Why the earlier verdict was wrong:** my gs invocation carried `-dPDFSTOPONERROR=false`, which on
  gs 10.07.1 causes "Unrecoverable error, exit code 1" and a 2,423-byte blank page. Run bare it rebuilds
  all 38. The flag added to make gs MORE tolerant is what made it fail, so the "evidence" of
  unrecoverability was produced by my own command line, not by the document. Truncation removes the xref
  INDEX at the file's end; the page objects before it are intact, and gs rebuilds by scanning objects.
  Treat any 1 MiB capture as recoverable until a bare repair actually fails.
  - **Stated limit:** the ~1,035 LIVE citations were header-checked (first 2 KB) only, which proves a PDF is served, not that it is COMPLETE. Offered the peer a bounded full-download sweep of those 1,035 if they want that closed.
- **"Posted to the website" class (peer ask 3):** confirmed instances are Melli FY2017–FY2019 ("have been posted", only FY2016 survives) and Hampden FY2016/FY2017 (script note already records the AR wording). A repo grep only finds cases someone already quoted, so I offered (a) derive the candidate list from the repo (free) and (b) fetch+grep those ARs (bounded sweep).

### Ask 3 — "posted to the website" sweep (peer-requested, started ~01:45)
- **(a) DONE, and my first answer was wrong.** The grep heuristic said 17 scripts; an AST parse of all 145 says **78 scripts / 487 bank-years**.
  - Method: parse each script's YEARS, every `{year: "Not publicly disclosed"}` dict, every `add_not_disclosed_metric_sheets` call (whole sheets × all years), and every year-specific AR/CH constant. A bank-year qualifies when BOTH hold for the same year.
  - Machine-readable: `scratchpad/nd_targets.json` (script → year → {metrics, doc constant}).
  - Biggest: FCE 20yrs (FY2006–FY2025), ICICI 19, UBP 17, NatWest 14, SMBC 14, BACB 13, BLME/ICBC/Morgan Stanley 12.
  - The first list's top entries all survive, so nothing dispatched on it was wasted — the parse just found ~60 more scripts and pins the YEARS rather than the bank.
- **(b) scope widened on the peer's instruction, and they are right:** the "Not publicly disclosed" filter finds where WE failed, not where the BANK asserted publication. The Melli shape (cells filled from the AR, so nothing looks missing) is invisible to it by construction. So (b) sweeps EVERY cited AR.
  - `ar_extract.py` → **948 distinct documents** across 140 scripts (467 Companies House, 481 other hosts). List: `scratchpad/ar_fetch_list.json`.
  - `ar_grep.py` fetches, pdftotext's, and records a Pillar 3 mention within ~300 chars of an assertion, BOTH directions:
    - PUBLISHED = "posted to / published on / available on the … website" → a document existed and was public
    - ON_REQUEST = "available/provided on request" → the bank asserts NON-publication (an answer, not a gap)
  - Verdicts kept distinct so a failure never reads as silence: ASSERTION / NO_ASSERTION / SCANNED_NO_TEXT / NOT_PDF / ERROR.
  - **SCANNED_NO_TEXT matters:** most CH filings are image-only = "not yet read", NOT "no assertion". Melli's whole AR set was this shape and needed OCR.
  - Per the peer's Melli point: where both the AR and the archived disclosures page can be checked, report any CONFLICT as the finding rather than picking a side.
- Order: Zenith, BLME, CAF Bank, Turkish Bank, Metro → rest of the original 17 → everything else. Then the 1,035-row live full-download sweep (third).

- **LBCM 2021 interim negative HOLDS (~22:15):**
  - Eight 2021 Q1/HY/Q3 permutations 404. They cover the 2022+ folder patterns q1/, q2/, q3/ and half-year/, plus flat 2021/ with "pillar3" and "pillar-3".
  - Control: 2021/2021-lbcm-fy-pillar3.pdf serves %PDF (556KB).
- **Access Bank UK WP media API:** curl gets a Cloudflare 403 challenge and WebFetch gets a 403 too, so it is BLOCKED on both clients. Inconclusive; the negative still rests on the script's CDX evidence.
- **Melli live site (~22:15):** mellibank.com and www.mellibank.com resolve (62.232.194.164), but TCP connections time out on ports 80 and 443. www.mellibank.co.uk times out too. The site is effectively offline, which fits the Sept 2025 sanctions designation, so Wayback is the only route for any FY2023 website edition.
- **Wayback fallback results so far** (lr_fix_out2.jsonl). Each is a verified id_ capture: %PDF, page count, and not 1 MiB-truncated.
  - eabplc AR2022 `202304_EABAnnualReport_v7_144ppi.pdf` → 20240714135652id_ (98pp). This is the same timestamp the script already cites.
  - eabplc AR2024 `202502_EABAnnualReport_v3.pdf` → 20250805183352id_ (100pp). Same timestamp as cited.
  - eabplc `Pillar3.pdf`:
    - lr_fix chose the NEWEST capture, 20250505164839 (35pp). **Do not send that one.**
    - The script cites 20240714131343 (the FY2022 edition). An undated filename can hold different editions at different captures (the Metro trap).
    - Stage 5 verifies the 20240714131343id_ capture and lists its CDX digest history.
  - Itaú 2021/2022/2023 (BLOCKED live): id_ captures 20230502062443 (54pp), 20230502054346 (67pp) and 20240812211731 (62pp). These are fallbacks only; the live URLs stay cited.
  - FirstBank `FBNUK-Pillar-3-Dec-19-FINAL-Published_v3.pdf` → 20200918094410id_ (27pp). `FBNUK-Pillar-3-Disclosures_-2021.pdf` → 20240718195901id_ (39pp).
- **Stage-3 retry** (lr_res_stage3b.jsonl): 19 of the 27 are now OK. 8 still hit archive connection timeouts:
  - FCE 2016 AR, 2010 AR, 2006 AR, 2008 AR
  - Vanquis pfg 2017
  - SMBC pillar3-31-03-15 and smbce-pillar3-2020
  - UBL if_ 2018
  - Their id_ forms are first in the stage-5 queue (lr_stage5.json → lr_res_stage5.jsonl, lr_idverify.py, sequential with backoff).
- **Negative re-checks on live hosts** (no archive), 2026-09-15 ~22:30. Every negative below HOLDS:
  - BOA UK: finances.html newest is Pillar3-Disclosures-2024; three 2025 permutations 404 (2024 control 206 PDF).
  - Saderat: Basel_Disclosures.htm newest is 2023; 2024/2025 permutations 404 (2023 control PDF).
  - Nomura NEH 310325/310326: 404 under both public/ and login/ (310324 control PDF).
  - FidBank 2025: three permutations 404 (2024 control PDF).
  - UBP UK: the P3 page lists SGKH 31 Dec 2022/2023/2024 only.
  - Weatherbys: the annual-reporting page newest P3 is 2024. A 2026/06 upload exists, but it is the gender pay gap report, not a P3. The WP REST route is absent.
  - Arbuthnot FY2025 annual P3: five permutations 404.
  - Hodge FY2024/FY2025: the WP media API (terms pillar, pillar-3, disclosure, hodge) shows no P3 upload after 2024-07. Note that /regulatory-disclosures/ is now a plain **404**, where it used to be a 403.
  - Access Bank UK: the WP media API gets a Cloudflare 403 challenge, so this could not be re-checked (the negative rests on the existing CDX evidence).
- **REVERSAL, access-type:** AIB Group (UK) p.l.c. FY2021 Annual Financial Report.
  - The script says it "could not be fetched" (aibgb.co.uk 403) and uses the FY2022 AR's comparatives.
  - It IS on Companies House: NI018800, filed 11 Mar 2022, "Group of companies' accounts made up to 31 December 2021".
    https://find-and-update.company-information.service.gov.uk/company/NI018800/filing-history/MzMzMjQ0MDUyOWFkaXF6a2N4/document?format=pdf&download=0
    %PDF, 168pp, scanned. OCR cover: "AIB Group (UK) p.l.c. Annual Financial Report for the year ended 31 December 2021, Company number: NI018800".
  - aib.ie /annualreport/2021/ permutations all 404.
- **Hodge (info):** live copies of every old Pillar 3 are at `hodgebank.co.uk/wp-content/uploads/2024/07/`. These could replace the Wayback citations, but the Wayback id_ citations are already fine.
  - jhb-pillar3-2012 ("as at 31 October 2012", 21pp), -2013 (23pp), -2014 (23pp), -2015 (23pp), -2016 (34pp), -2017 (34pp), -2018 (37pp), Pillar-3-Disclosure-FY19-FINAL (36pp).
  - FY2012/FY2013 Pillar 3s exist live, although the script's P3 sheets start at FY2014/FY2016 (Basel II years).
- **Melli (Companies House, all 13 ARs FY2013–FY2025 OCR'd; statement in the Directors' report):**
  - FY2013: "will be posted to the Bank's website, www.mellibank.com after the agreement of the capital planning buffer with the PRA".
  - FY2014 and FY2015: "will be posted to the Bank's website".
  - FY2016–FY2019: "have been posted to the Bank's website, www.mellibank.com".
  - FY2020, FY2021 and FY2022: "available on request from the Bank".
  - **FY2023: "The Pillar 3 disclosure is available on the Bank's website (www.mellibank.com)".**
  - FY2024 and FY2025: "available on request". FY2025 also records the 29 Sept 2025 sanctions designation.
  - Accounts doc ids: FY2013 MzEwMzI2NjE3MmFkaXF6a2N4, FY2017 MzIwODMyMzYxMGFkaXF6a2N4, FY2018 MzIzNzg1NzI1MmFkaXF6a2N4, FY2019 MzI2ODMyMjYyMWFkaXF6a2N4, FY2020 MzMwNjA2MDkzMGFkaXF6a2N4 (others listed earlier).
  - Stage 5 runs a mellibank.com CDX from 2019 to test the FY2023 website claim, and verifies the FY2014/FY2016 P3 captures.

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

## Ask 3(b) — "what the BANK says about Pillar 3 publication" (2026-09-16)

Method: fetch every cited Annual Report / CH filing, extract text, and record assertions where the SAME
SENTENCE mentions Pillar 3 and asserts either publication or availability-on-request. Both directions are
findings. Sentence-scoped after a ±320-char window produced false positives by stitching table cells.

**Verdicts:** ASSERTION / NO_ASSERTION / SCANNED_NO_TEXT / NOT_PDF.
`SCANNED_NO_TEXT` means NOT YET READ. It must never be counted as "the bank said nothing" — Melli's
Pillar 3 statement sat in a scanned AR, and that case is why this sweep exists.

### A BUG IN MY OWN EXTRACTOR (found 2026-09-16, before reporting it as a repo defect)
`ar_extract.py`'s `str_of()` resolved string literals but returned `""` for an `ast.Name` and silently
dropped f-string `FormattedValue` nodes. Two consequences:
- It **invented 17 addresses** present in no build script — `.../company//filing-history/...` (empty
  company number) and `.../web/<ts>id_/` with no target. These fetched as NOT_PDF and looked exactly like
  a defect class of malformed citations in the repo. **They are not.** The scripts are correct:
  `build_marks_and_spencer_financial_services.py` uses `f".../company/{COMPANY_NO}/..."` with
  `COMPANY_NO = "01772585"`; `build_arab_bank_europe.py` uses `"...id_/" + ORIG_AR2022_URL`.
- It **missed 196 real documents** — mostly CH filing-history URLs whose company number is a variable.
  Corrected extraction (`ar_extract2.py`): **1,127 URLs, not 948**. The first pass therefore covered ~83%
  of the corpus; a second pass covers the remainder.
Fixed by building a module-level symbol table and resolving Names/FormattedValues against it.
**This is the same error shape as the gs verdict: reporting an artifact of my own tooling as a property
of the source.** Verified against the scripts before sending this time.

### Not defects, checked and cleared
- `sbiuk.statebank` — resolves (103.68.221.40), serves a 920,392-byte `%PDF`. `.statebank` is a real gTLD.
- SBI annual report — a 13.4 MB PDF that outran my timeout; alive.
- Lloyds `CH_URL` (`/company/00002065`) — a legitimate CH landing page used inside a citation string.
- Shawbrook's CH entries are URL + prose in one string; a citation format, not a broken address.

### Truncation rule REFINED
Exactly 1,048,576 bytes is a **signature, not proof**. Julian Hodge's FY2018 AR capture is exactly 1 MiB
and fully intact — 86 pages, last page carrying real text ending naturally on "38 Ultimate parent
undertaking". The decisive test is **whether the LAST page carries text**, since truncation removes the
END of a file. Page 1 proves nothing. Guard against linearized PDFs: their page-count hint table sits at
the file's START, so a truncated one can still report a full page count.

### hodgebank.co.uk is PATH-DEPENDENT
A nonexistent filename under `/wp-content/uploads/2024/07/` returns an honest 548-byte 404, but
`/wp-content/uploads/2020/02/FINAL-Julian-Hodge-Bank-Limited-FY18.pdf` returns 200 `text/html` at 108,306
bytes. A negative control proves the behaviour of the directory it was run in and nothing about any other
path on that host. That FY2018 AR is genuinely gone live, so citing the Wayback `id_` capture is correct.

### Interim results (868 of 1,127 documents)
PUBLISHED 61 · ON_REQUEST 1 · NO_ASSERTION 244 · SCANNED_NO_TEXT 270 · NOT_PDF 47.
Representative verbatim hits:
- C. Hoare & Co, FY2019-FY2023 (five consecutive years): "A fuller description of the bank's principal
  risks can be found in the bank's Pillar 3 disclosures, which is unaudited, and is available on the
  bank's website:"
- BNY Mellon FY2023/FY2025: "The Pillar 3 disclosures for the Company are published on BNY's website at
  https://www.bny.com/corporate/global/en/investor-relations/regulatory-filings.html."
- Arbuthnot Latham FY2017: "Our Pillar III disclosures for the year ended 31 December 2017 are published
  as a separate document on the Group website under Investor Relations."
Reporting via `ar_report.py`, which filters v1 artifacts and prints the unread denominator per bank.

### Ask 3(b) COMPLETE — 1,127 documents (2026-09-16)
`SCANNED_NO_TEXT 577 · NO_ASSERTION 391 · NOT_PDF 70 · ASSERTION 89`
(103 PUBLISHED sentences, 4 ON_REQUEST, across 30 banks). Report: `ar_report_final.txt`.

**THE OCR SHAPE I REPORTED EARLIER WAS WRONG AND IS CORRECTED HERE.** From the partial 250-document
pass I said 79 unread, "concentrated", "six banks entirely unread", and framed the decision as
"OCR six banks' CH filings". At full coverage it is **577 of 1,127 unread (51%)**, with **101 banks
holding at least one unread document and 50 banks ENTIRELY unread**. The earlier framing was drawn
from a partial pass running at 83% corpus coverage and should not be used.

**The sweep is blind to the case it exists to detect.** `melli_bank` is 5/5 entirely unread. Melli is
the bank whose Pillar 3 statement sat in a scanned Directors' report and started this line of work.
So is `gulf_international_bank_uk` (5/5) and `bank_of_africa_uk` (10/10). This is the
`nd_targets_README.md` caveat — "it cannot see the case that matters most" — confirmed on live data.

#### GROUP-LEVEL ASSERTIONS — a contamination risk, not a lead (24 across 10 banks)
An assertion naming a GROUP/parent document cannot source a UK-subsidiary workbook. Flagged banks:
arbuthnot_latham, clearbank, hsbc_bank_plc, hsbc_uk_bank_plc, onesavings, secure_trust (9 hits
FY2017-FY2023), shawbrook, vanquis. Verbatim examples:
- Secure Trust FY2017: "Pillar 3 disclosures for the Group for the year ended 31 December 2017 are
  published as a separate document on the Group's website."
- OneSavings FY2019/FY2022: "The Group's Pillar 3 disclosures can be found on the Group's website."
- Shawbrook FY2021: "Additional disclosures can be found in the Shawbrook Group plc Pillar 3
  Disclosures, which is available on the website detailed above."

#### VANQUIS — ~~a STRUCTURAL finding that moves the coverage denominator~~ **DISPROVEN 2026-09-16**
FY2021 AR, verbatim: "As a result, with effect from 31 December 2020 the Company's individual
disclosures have been aggregated into the consolidated Group Pillar 3 disclosures, which can be found
on the Group's corporate website (www.providentfinancial.com)."
~~Vanquis Bank's OWN Pillar 3 therefore ceased to exist from 31 Dec 2020, so FY2021+ cells are
"Not applicable" rather than "Not publicly disclosed".~~
**THAT READING WAS WRONG.** The sentence sits under the **Remuneration Committee** heading and its
subject is the CRD V **Remuneration Code** disclosure statement, not the capital Pillar 3. The two
preceding sentences settle it: *"Until 31 December 2019, the Company was required **as part of the
code** to publish an annual disclosure statement on an individual basis… Following the application of
the CRD V Remuneration Code on the Group on a consolidated basis, the contents of the remuneration
disclosure are required to reflect the policy and aggregated remuneration on a consolidated Group
basis."*
Corroborated independently by katalysis-36: Wayback CDX on vanquis.co.uk shows **every** "individual"
Pillar III document the Bank self-published (2010, 2011, 2012, 2016, 2017, 2018) is a Remuneration
Code disclosure and never a capital one — so there was no capital disclosure to cease and no
FY2020/FY2021 boundary. Every Provident/VBG edition FY2014–FY2025 was read end to end: none contains a
Vanquis Bank Limited solo capital section. Zero cells re-marked; `build_vanquis.py` contains zero
"Not publicly disclosed" cells, so the instructed re-marking had no target.
**WHY I GOT IT WRONG — the limit of sentence-scoping.** Sentence-scoped matching was the right fix for
the ±320-char window that stitched table cells into false positives, but it introduced the opposite
failure: *a sentence that is unambiguous alone can be about something else entirely in its paragraph.*
Fixed in `ar_context.py`, which keeps matching sentence-scoped but captures the previous sentence, the
next sentence and the containing heading. Had that existed, the Remuneration Committee heading would
have made this self-evident.

#### SELF-CATCH: the Shawbrook Pillar 3 URLs I supplied in batch 7 are GROUP-basis
`shawbrook-pillar-3-disclosures-2025.pdf` cover: "Shawbrook Group plc Company No: 07240248", section 2
"Disclosures for Shawbrook Group plc (the 'Group')" — 120 mentions of "Shawbrook Group plc" against 3
of "Shawbrook Bank Limited". FY2021: 72 vs 37. FY2019: 46 vs 6.
The workbook's own AR citations are Companies House **00388466 = Shawbrook Bank Limited**; the Pillar 3
documents are **07240248 = Shawbrook Group plc**. Different entities.
NOT overclaimed: the FY2021 edition mentions the Bank 37 times and may carry a Bank-only section, so
the live question is whether each transcribed figure came from a solo table or the Group consolidated
one. But on their face these are Group-basis documents cited in a Bank-basis workbook — the same defect
being fixed in Arbuthnot Latham, in files I supplied. Flagged to katalysis-36; repo edits are theirs.

### Live full-download sweep — LAUNCHED 2026-09-16
Target rebuilt with the FIXED resolver (`all_urls.py`), because the old extractor's dropped `ast.Name`
and f-string `FormattedValue` nodes would have biased this list the same way they biased 3(b):
**2,207 distinct cited URLs across 145 scripts — 2,020 live, 187 archive, 1,191 live PDFs** once
Companies House is excluded (those 667 were covered by 3(b)). The figure we had both been using was
1,035, so the live target set is ~15% larger, same root cause.

**`lr_idverify.py` truncation logic REWRITTEN and validated on known answers before use.**
The old line was `TRUNCATED_1MiB if len(data) == 1048576` — the rule disproved earlier today. It now
applies the last-page test and only reaches for bare `gs` when the tools actually fail:
| document | verdict | detail |
|---|---|---|
| GIB FY2020 truncated capture | `RECOVERED_BY_GS` | rebuilt to 38 pp / 795,035 B, tail 2,699 chars |
| Hodge FY2018, exactly 1,048,576 B | `OK_PDF_1MiB_INTACT` | 86 pp, tail 933 chars |
| Hodge 2016, ordinary live PDF | `OK_PDF` | 34 pp |
The middle row is the regression test: the OLD rule would have condemned that intact 86-page document.
A truncated *linearized* PDF reports a full page count but returns an empty tail, so it lands as
`TAIL_EMPTY_CHECK` rather than passing silently as OK_PDF.

### Shawbrook — RESOLVED IN THE PEER'S FAVOUR (my flag was a hint, not evidence)
katalysis-36's agent had already examined all seven FY2014–FY2020 editions. Every figure comes from
**"Appendix 1: Disclosures for Shawbrook Bank Limited"** — the Article 13 CRR reduced disclosure of the
Bank itself, the significant-subsidiary exception this project recognises. Appendix 1 is present in the
2014–2018 and 2020 editions; FY2019 lacks it, which is exactly why the script already sources FY2019
from the 2020 edition.
**THE PROOF IS A DIVERGENCE, NOT AN ASSERTION:** the 2018 edition prints Group leverage 9.2% (2017:
9.4%) against Bank 9.2% (2017: **9.5%**), and the workbook carries **9.5%**. In the one year the two
bases disagree, the workbook demonstrably follows the Bank's. That is stronger than any mention count.
STILL OPEN, and it is the INVERSE error: my 120-vs-3 count was on the FY2025 edition, FY2021 was
72-vs-37, so the Appendix 1 practice may have LAPSED after FY2021 — in which case FY2021+ figures would
be Group-basis. Not that the old editions were misread, but that the old practice was assumed to
continue. Peer has dispatched on it.

### Method worth reusing: THE DIVERGENCE TEST
Where two candidate bases exist (Group vs Bank, parent vs UK subsidiary), do not argue from cover pages
or mention counts. **Find a year in which the two bases print DIFFERENT numbers, then check which one
the sheet followed.** It converts an unanswerable "which document did this come from" into a decisive
one-cell comparison.

### Caveat carried from the peer, worth keeping visible
A correct citation proves nothing about the figures. Gatehouse's FY2017 column had dropped a
"Due from financial institutions" line worth 27.5% of total assets while being fully and correctly
cited. Everything in this file verifies whether the SOURCE is right; that is a different audit from
whether the figure was read off it correctly, and the two should not be reported as one.

### C. Hoare & Co — RESOLVED (2026-09-16). 31 MARCH year-end.
Index: https://www.hoaresbank.co.uk/financial-reports (also lists ARs back to 2008).
LIVE, all verified 200 `application/pdf` + `%PDF` + page count + cover:
  /files/2021-10/CHC_2021_Pillar_3_Disclosures.pdf   42 pp
  /files/2022-07/2022_Pillar_3_Disclosures_0.pdf     29 pp   "Year ended 31 March 2022"
  /files/2023-07/Pillar_3_Disclosure_2023.pdf        28 pp
  /files/2024-06/Pillar_3_Disclosure_2024.pdf        24 pp
  /files/2025-07/Pillar_3_Disclosure_2025.pdf        17 pp
RECOVERED FROM ARCHIVE (older editions live under a DIFFERENT path, `/sites/default/files/styles/`):
  FY2019 — 957,075 B, 54 pp, "Year ended 31 March 2019", md5 659284c2947bfc979b9cf1f3f2b9efed, tail 1,546 chars
    https://web.archive.org/web/20190923044126id_/https://www.hoaresbank.co.uk/sites/default/files/styles/2019%20Pillar%203%20Disclosures.pdf
  2018  — 791,429 B, 53 pp, "Year ended 31 March 2018", md5 a8593688d6d14fcafd0b1d1a54cc2f1f, tail 751 chars
    https://web.archive.org/web/20210506235636id_/https://www.hoaresbank.co.uk/sites/default/files/styles/2018%20Pillar%203%20Disclosures.pdf
Entity basis clean: covers and running heads read "C. Hoare & Co." throughout, no group wording.
**FY2020 is GENUINELY ABSENT** — no capture at any timestamp under any path family, live site 404s.
Asserted in the AR, unretrievable by any route. Recorded as ABSENT, not BLOCKED: CDX answered 200
throughout, so this is a real negative rather than the Archive being unavailable.
Dated published-then-removed example: the 2018 file is 200 at 20210506235636 and 404 at 20240627025610.
**Year mapping deliberately NOT done here** — the period is printed on each cover; which column it
belongs in is a repo decision (katalysis-36's side).
METHOD NOTE: my first probes permuted filenames under `/files/` and returned eight identical 404s. The
documents were under `/sites/default/files/styles/`. I never questioned the DIRECTORY — the same error
as Hodge's untested fifth directory, committed two hours after writing that lesson down.

### RETRACTION — CDX `length` is NOT the file size
I suggested the Hoare 2022/2023 URLs might hold multiple editions because captures showed different CDX
lengths. **That inference was unsound and is withdrawn.** CDX `length` is the WARC record length
(compressed): CDX reported 749,337 for the 2019 file whose actual size is 957,075 bytes. Differing
lengths prove nothing about differing content. Use `collapse=digest` (computed on content) and confirm
by fetching `id_` bytes and comparing md5. The live 2022/2023 URLs remain verified-live; only the
multiple-editions suspicion is withdrawn.

## LIVE FULL-DOWNLOAD SWEEP — COMPLETE (2026-09-16), 1,191 URLs
Method: full download + `pdfinfo` + **last-page test** on every URL. Report: `live_report_final.txt`.

| verdict | n |
|---|---|
| OK_PDF | 1,039 (+5 recovered, see TLS) |
| no text on last page (image back-cover / scanned) | 95 |
| honest 404/410 | 27 (only 7 actionable) |
| blocked 403 / unreachable | 17 — UNKNOWN, never "dead" |
| soft-404 catch-alls | 8 |

### ZERO TRUNCATIONS — the question the sweep was commissioned to answer
**Not one row at exactly 1,048,576 bytes in 1,191 live URLs.** The 1 MiB defect is purely a Wayback
CAPTURE artifact, not a live-web phenomenon. Established by checking every row's byte count, not by
observing an empty section. The 95 empty-tail files run 176 KB – 24.8 MB: image back-covers, not
truncation.

### The soft-404 published-then-removed detector: an honest NEGATIVE
Zero leads. All 8 soft-404s were demoted by the body-identity guard — eabplc.com ×4 (identical
95,415 B bodies) and qib-uk.com ×4 (identical **247 B** bodies at status **200** — the F5 WAF page).
Without the guard these would have been reported as 8 published-then-removed leads, all false.

### Link rot: ALL 27 of 27 are DOCUMENTED dead originals. THERE IS NO NEW LINK ROT IN THE CORPUS.
**Corrected 2026-09-16 (katalysis-36 caught this; my first report said "20 documented, 7 genuinely new").**
Every one of the 27 honest 404s is a deliberately-retained provenance record with a live or archived
replacement already cited alongside it. The citation estate has **zero** undocumented breakage — a
stronger statement than the one I originally sent.

**Why I got it wrong three times in a row, each time by widening a regex instead of opening the file.**
A dead-marker can sit in at least three places, and I only ever checked one at a time:
1. **On the constant** — `P3_2019_DEAD`, `P3_FY2020_DEAD_URL`, `P3_2021_OLD_URL`. My filter caught these.
2. **On the CONTAINER** — Shawbrook's seven live at `build_shawbrook.py:24-28` (`P3`) with the seven dead
   at `:34-41` in a dict named **`P3_DEAD`**, under "Dead originals, retained for provenance - do NOT
   delete", plus a `LINK_PROVENANCE` block rendering each substitution into the workbook. The entries are
   plain literals; the marker is on the dict. I reported them as unmarked.
3. **In a FILE-HEADER COMMENT far from the literal** — FirstBank ×6 named `ORIG_P3_<year>_URL`
   (`build_firstbank_uk.py:62-67`), documented by a comment at **lines 26-30** ("ALL SIX ... are DEAD ...
   preserved below as ORIG_P3_*"), each paired with a Wayback `P3_<year>_URL` and a `P3_DEAD_URL_NOTE`
   written into the workbook. My container-aware rerun STILL missed these: "ORIG" was not in my marker
   vocabulary and my comment scan looked only 4 lines back.

**The lesson is not a better regex.** Marker vocabulary, marker location and marker distance are all
unbounded; each fix found the previous shape and missed the next. katalysis-36 caught instance 2 by
opening the file before editing — the only reason any of tonight's ten instances were caught.

### A defect in my own verifier, caught before reporting
Six rows returned `ARCHIVE_UNAVAILABLE`. All six were TLS failures (curl rc=60/35), not link rot.
Retried with `-k`: **banksepah.co.uk ×5 are ALL ALIVE** (200 `application/pdf`, 31–32 pp, Pillar 3 at
31 March 2021–2025); persiabank.co.uk remains unreachable and is recorded BLOCKED, not dead.
Five live documents would have been reported unavailable. **The fix was already in my own notes**
("an expired TLS certificate is not link rot, retry with -k, e.g. banksepah.co.uk") and the verifier
simply never passed the flag. Recording a lesson is not the same as wiring it into the tool.

### Ask 3(b) context re-analysis (katalysis-36's suggestion)
Re-ran all 107 assertions capturing previous sentence, next sentence and containing heading, from
cache — no re-fetch. **17 of 103 PUBLISHED flagged as review items, NOT verdicts:**
- Genuinely off-topic: Vanquis FY2021 (disproven) + FCE Bank FY2018/19/20 ("Pillar 3 disclosures
  **regarding remuneration**").
- False flags: Crown Agents ×4 ("PRA Pillar 3 **Capital Adequacy** disclosure requirements… including
  remuneration"), OakNorth FY2020 ("**including** disclosures on remuneration policy"), Charity Bank
  (flagged on the *next* heading "Climate risk"), Co-op FY2014 (flagged on "Task Force"/EDTF).
- Ambiguous: Hampshire Trust ×3, Zopa FY2023 — remuneration-framed but each still asserts publication.
**86 of 103 carry no off-topic context**, so the PUBLISHED set is sounder than Vanquis implied.
**NEW CATEGORY:** FCE Bank FY2018/FY2019 — "This **chapter** contains the remaining Pillar 3
disclosures required by Part Eight of the CRR". FCE embeds its capital Pillar 3 INSIDE the annual
report. Neither "published separately" nor "not disclosed"; a hunt for a standalone FCE PDF would fail
forever while the disclosures sit in a document already held.

## SHAWBROOK — RESOLVED (2026-09-16). The documents were never gone; the filenames were.
The seven dead citations have **live replacements on shawbrook.co.uk**. No Wayback copy, no Companies
House fallback, no recovery of any kind is required. `build_shawbrook.py` cites **two filename families**
and already cites the live one for every affected year — the dead family is a redundant alias.

| FY | dead (cited, 404) | LIVE replacement `/media/…` | bytes | pp | md5 |
|---|---|---|---|---|---|
| 2014 | qsxpg41l/shawbrook-pillar-3-disclosures-2014.pdf | `cc5dq5j0/pillar-3-2014.pdf` | 2,077,440 | 48 | e2f9d46c…4b35 |
| 2015 | wdvhqxsn/…-2015.pdf | `4galhsik/pillar-3-2015.pdf` | 757,619 | 42 | 46546a4d…0ded |
| 2016 | 1lhngswy/…-2016.pdf | `koignkmo/pillar-3-2016.pdf` | 2,897,173 | 57 | 97892dec…9b03 |
| 2017 | 3lifgtxe/…-2017.pdf | `3wefl2tu/pillar-3-2017.pdf` | 5,384,148 | 55 | 19e94882…6a1c |
| 2018 | kfnfg0oe/…-2018.pdf | `vypjeoat/pillar-3-2018.pdf` | 1,500,212 | 50 | 3bdffb59…0c6 |
| 2019 | 2azlz2vz/…-2019.pdf | `yhdl0kcs/pillar-3-2019.pdf` | 4,059,311 | 44 | 0b1615e7…1bea |
| 2020 | xexpjjkq/…-2020.pdf | `zlibpqlt/pillar-3-2020.pdf` | 3,052,414 | 61 | ef44fc79…ab86 |

All seven: status 200, `application/pdf`, `%PDF` magic, and md5 **identical to the copies I had already
verified page-by-page**. Of the 26 Shawbrook URLs the script cites, exactly **7 are dead and 19 live**;
the seven sit in one contiguous dict at **`scripts/build_shawbrook.py:35-41`**. No cell or citation
changed here — mapping and counts only.

**Caveat:** CDX shows `yhdl0kcs/pillar-3-2019.pdf` has served **two distinct digests** (AFAXAWHT…,
HIRIVCFH…). Pin that citation to md5 `0b1615e7c61eee2da3ee0f3bb2a1beea`, not to the URL alone.

### Appendix 1 is in ALL SEVEN editions — the "FY2019 lacks it" note is withdrawn
Every edition FY2014–FY2020 carries "Appendix 1: Disclosures for Shawbrook Bank Limited / In accordance
with Article 13 of the CRR … the significant subsidiary of the Group", each naming **PRA FRN 204574
exactly once**. FY2019 has it **nine times**, including a leverage ratio common disclosure.

**The divergence test re-confirmed from the complete 2018 file** — two distinct entity blocks:
Group T1 640.4 / exposure 6,986.6 → 9.2% (2017: **9.4%**); Bank T1 639.4 / exposure 6,987.0 → 9.2%
(2017: **9.5%**). AT1 differs (124.0 vs 125.0), so these are genuinely two entities. Workbook carries
**9.5% = Bank basis**. FY2019 is *not* a divergence year (8.6% on both bases); Bank T1 719.4 vs Group
721.2 (2019), Bank 788.8 vs Group 790.3 (2020).

### Three matcher artifacts nearly cost real documents — the night's recurring class, again
1. `Appendix 1: 0` on the 2016 file: it prints "APPENDIX 1 **:**" (space before colon) and its text layer
   is **line-fragmented**, so `appendix\s*1` matches the whole text but NEVER line-by-line. Two of my own
   Python runs disagreed with each other — the tell. **Normalise whitespace before counting anything.**
2. The 2015 appendix is "SHAWBROOK BANK **LTD**"; searching "Limited" under-reports it. (BNYMIL again.)
3. **"This edition lacks the appendix" and "my copy is truncated" look identical** — an appendix sits at
   the END (2019 lists it at p.31 of 44) and a 1 MiB cut removes exactly that. Almost certainly what
   produced the FY2019 claim. Apply the last-page test before concluding a practice lapsed.

**My own correction:** I described 2014/2016/2018 as "truncated, partially recovered by gs". The live site
serves all three **complete**; the truncation was purely a Wayback capture artifact. Tool reach reported as
a property of the world — ninth instance tonight.

## FCE-CLASS HUNT — an honest NEGATIVE (2026-09-16). Detector: `scratchpad/fce_pattern.py`
katalysis-36 asked whether other banks embed their capital Pillar 3 INSIDE another document, as FCE does.
Such a bank is invisible to a filename hunt and looks identical to one that never disclosed.

**The discriminator that worked: "Part Eight of the CRR"** — that IS the capital Pillar 3 requirement,
whereas remuneration flows from CRD/the Remuneration Code and climate from TCFD. All 18 candidates it
returned are genuinely about the capital disclosure; **zero remuneration false positives.** Worth reusing.
FCE carries BOTH a remuneration Pillar 3 mention and an embedded capital chapter, so filtering remuneration
documents out wholesale would have discarded the document that defined the class.

| corpus | n |
|---|---|
| searchable (text layer) | **482** |
| **scanned, no text — NEVER SEARCHED** | **653 (58%)** |
| no cached file | 9 |
| candidates | 18, across 2 banks |

- **FCE Bank** — 6 docs FY2015–FY2020, 3 with explicit embedded phrasing ("This chapter contains the
  remaining Pillar 3 disclosures required by Part Eight of the CRR"), all carrying CET1/leverage/RWA/LCR/
  own-funds tables. The known case, confirmed.
- **Clydesdale — NOT the class, lead closed.** 12 docs, **zero** embedded phrasing, 10 of 12 explicitly
  reference a separate Pillar 3, and `build_clydesdale.py` cites standalone Pillar 3 reports through
  `cb-2026-pillar-3-report.pdf` with **zero open gaps**. Its Part Eight mentions are routine
  cross-references. (FY2025/FY2026 appeared to lack the separate-Pillar-3 reference; that was my phrasing
  regex missing it, not a change in practice — a fourth matcher artifact, caught before it became a claim.)

**RESULT: zero new instances of the FCE class among the 482 searchable documents.** That is NOT the same
claim as "no other bank does this". **653 documents were never searched** because they have no text layer,
and the OCR job over them remains the user's call. The detector is re-runnable against them if that job
ever happens. Stating this as "no other bank embeds its Pillar 3" would be instance eleven.

**Reproducing the detector** — `scratchpad/fce_pattern.py` is in a SESSION-SCOPED scratchpad and will not
survive this session; it was not among the artifacts I was asked to write into `research/`, so I have not
copied it here. It is three regexes over `pdftotext -layout` output, whitespace-normalised first:
```python
PART8    = r"Part\s+(Eight|8|VIII)\b[^.]{0,60}\bCRR\b|\bCRR\b[^.]{0,40}Part\s+(Eight|8|VIII)\b"   # the discriminator
EMBEDDED = r"(this|the)\s+(chapter|section|report|document|annual\s+report)\s+(contains|sets?\s+out|includes?)[^.]{0,90}?Pillar\s*3"
SEPARATE = r"Pillar\s*3[^.]{0,90}?(web\s?site|www\.|separate\s+document|published\s+separately)"   # demotes a hit
```
Report PART8 and EMBEDDED separately, probe each candidate for CET1/leverage/RWA/LCR/own-funds tables, and
treat `SEPARATE` as demoting — a bank with a standalone Pillar 3 is not this class whatever it cross-references.
Say it to me if you want it as a `research/` artifact and I will add it.

## READER-SIDE URL AUDIT — verified independently (2026-09-16). 52 → 37 → **one real rot**
katalysis-36's reframing is right and is the structural lesson of the night: **"is this citation broken for
a reader?" is a property of `banks/*.xlsx`, not of `scripts/*.py`.** My 1,191-URL sweep was source-side, so
any URL built by concatenation or f-string that only materialises in a rendered cell was invisible to it.
They asked me to check their extraction rather than trust it. Doing so reduced the gap.

**My independent extraction: 145 workbooks, 20k+ occurrences, 2,033 distinct reader URLs** (their 2,034
included the bare `https://` fragment they flagged). **Reader-only = 37, not 52.**

| the 52 | n | outcome |
|---|---|---|
| genuine reader-only URLs | **37** | tested — see below |
| **extractor truncation artifacts** | **12** | ALL LIVE once reconstructed |
| templates, never citations | 3 | `<YEAR>`, `<timestamp>`, `<the` |

**THE TRUNCATION CAUSE — both our regexes shared it.** Excluding `)` and `,` from the URL character class
cuts any citation containing them. Testing the cut forms returns 404s that are artifacts, not rot:
- SMBC ×7 `...Annual-Report-and-Financial-Statements-2023-(SMBC-BI` → all **200 `application/pdf`**
- Union Bank of India ×3 `..._(Final`, `..._(2020-21`, `..._(2020` → all **200 `application/pdf`**
- TSB FY2014 — true URL ends **`TSB-Pillar-3-2014,0.pdf`** (a COMMA) → **200, 1,078,676 B**
**Fix:** match to whitespace, then trim trailing punctuation and only UNBALANCED closing parens.

**The 37 real reader-only URLs, all liveness-tested:** Companies House filing-history ×13 live PDFs;
Secure Trust ×9 live PDFs; web.archive ×4 live; Hoare 2022/2024 live; Reliance ×2, Jordan, UBI-2026 live.
`habibbank.com`, `gtbankuk.com`, `monument.co` return live **HTML index pages** — legitimate non-PDF
citations, not failures. Two 404s are **already documented with live fallbacks cited alongside**: TSB
FY2015 (cited to `web/20221214093332id_/`, 200 PDF) and Hoare FY2019 (cited to `web/20190923044126id_/`,
200 PDF, 957,075 B) — the Hoare workbook even records its own negative control in prose.

### The single genuine rot in the entire reader-facing estate
`vanquis.co.uk/media/1394744/crr-2018-remuneration-code-pillar-iii-disclosure-final-min.pdf`
**301 → `https://www.vanquis.com/` (homepage).** curl -L reported 403; that was the WAF masking a redirect,
and a second client (WebFetch) exposed it — the two-client rule earning its place again.
**Replacement verified:** `https://web.archive.org/web/20190923204636id_/<original>` → 200
`application/pdf`, 53,960 B, md5 `450a3447b5ba97766fa9525791eb0d9e`, **2 pp**, cover "Vanquis Bank Limited /
Capital Requirements Regulation (CRR) Pillar III & 2018 Remuneration Code Disclosure", last page carries
text (last-page test passes). The cover independently corroborates the earlier finding: Vanquis's
self-published "Pillar III" is a **Remuneration Code** document, never a capital one.

**FIXED by katalysis-36 (2026-09-16), verified in the rendered workbook, not just the script.** House
convention applied to `scripts/build_vanquis.py`: `ORIG_P3_REMUN_2018_URL` retains the dead original,
`P3_REMUN_2018_URL` is the Wayback `id_` form, and `P3_REMUN_2018_DEAD_NOTE` RENDERS into the workbook.
Both citing cells in `banks/VANQUIS FINANCIALS.xlsx` now carry the live archived URL, the named original and
the dead-marker. Their own catch en route is the lesson repeating: the note was defined but never
referenced, so the first rebuild produced a working link with **no record that the original had died** —
found by checking the rendered output rather than the source. Same principle that opened this thread,
turned on their own edit.

**CITATION ESTATE CLOSED: one genuine rot in 2,033 reader-facing URLs, now fixed.** The other 36
reader-only URLs are verified live or documented-with-fallback.

### CORRECTION to my own live sweep — persiabank is NOT unreachable
I recorded persiabank as BLOCKED/unreachable. **It is alive over `http://`**: 200 `application/pdf`,
1,382,251 B, byte-size matching its archived `id_` copy exactly. `https://` fails on the TLS handshake
(`curl_rc=35`). I classified the PROTOCOL as the HOST — the same family as the banksepah `-k` catch, and
the second TLS-shaped false negative of the night. Five archived persiabank captures are also live PDFs.

**A bug in my own sweep, found while checking this:** the loop reused `/tmp/v.bin` without truncating it,
so a failed fetch reported the PREVIOUS URL's byte count (persiabank https showed "81,222 bytes" having
downloaded nothing). `rm -f` the target before every fetch — better, a fresh `mktemp` path per URL, which
cannot race or be skipped on an early `continue`. A verifier that reports stale bytes on failure
manufactures evidence.

### `build_onesavings.py:14` `AR_2022_URL` — verified, and NO ACTION IS CORRECT
katalysis-36 flagged this unreferenced constant and deliberately declined to wire it. That call is right on
two independent grounds, both now established rather than assumed:
1. **It is the wrong entity.** The URL is live (200 `application/pdf`, 6,488,702 B, **260 pp**) but its cover
   reads "Annual Report and Accounts 2022 / **OSB Group** is a leading specialist mortgage lender" —
   `osbg-ara-2022.pdf` is the GROUP report. Every other AR citation in that script names **OneSavings Bank
   plc**, and Companies House **07312896 is ONESAVINGS BANK PLC** (confirmed from the register, not inferred).
   Wiring it would have crossed the entity boundary — the Arbuthnot FY2017 class.
2. **There is no hole to fill.** FY2022 is already sourced at `:43-44` from the entity's FY2023 accounts,
   "p.89 (**Company column**; FY2022 comparative)" — the Company column, not the Group one, which is the
   entity-basis rule applied correctly.
Note the script's Pillar 3 sheets separately and openly declare "OSB Group plc consolidated Pillar 3 basis",
the known **declared group basis** class — so group sourcing there is a labelled scoping decision, not
contamination. Leave the constant flagged and unreferenced; removing it is an editorial call for the user.

---

## KM1 SOURCE SURVEY — DELIVERED 2026-09-16

`research/km1_inventory.jsonl` (785 rows, one per distinct URL, 114 banks) plus
`research/km1_inventory_README.md`. Candidates and row inventories only — no figure transcribed.

**335 KM1_PRESENT of 732 readable documents (46%).** Columns captured for 311 of 335 (93%).
86 of 114 banks have at least one KM1 edition.

### The detector was wrong six times before it was right, and every fix was the same error class

Anchoring on the wrong table, reported under a confident verdict. A wrong anchor is **invisible in
its own output** — a foreign table still yields perfectly plausible dates.

1. **v5 header_block returned mid-table body rows** — anchored on the first `UK 7a` token, which sits
   mid-table, not on the column-header line.
2. **Dedup destroyed the multi-entity case** — Monzo's `2024 2024 2023` collapsed to two columns.
   Repeated years are often different ENTITIES. Also collapsed every quarterly filer's genuine
   five-column T..T-4 set to two.
3. **160-char truncation** ate the payload: `l.rstrip()[:160]` keeps LEADING padding and discards
   content, so a wide KM1's date row past column 160 rendered as blank lines.
4. **The anchor never applied the KM1_UK_ROWS restriction the VERDICT had applied since v2.** ICBC
   London anchored on a bare `UK 4a`; OSB Group on `UK 9b Redemption price` (capital-instruments
   template — KM1 has 9a, never 9b).
5. **A generic numbered-row tier found CC1 and contents pages** — Provident and Metro reported CC1's
   columns; three documents anchored on `1 Introduction 1`. A label test cannot separate these,
   because a contents page LISTS every label there is. **Figures** separate them.
6. **A title anchor's header is BELOW it, not above.** Scanning upward from ICBC's
   `UK KM1 - Key metric template` found the running page header and emitted the "column"
   `3 Disclosures 2024` — page furniture reported as a reporting date.

Two of my own guards were also matcher zeros: `(Common Equity|Available own)` without `re.I` missed
NatWest's `Common equity`, and `\d{1,2}\s+\w+\s+20\d\d` matched "Pillar **3 Disclosures 2024**".

**A presence claim the detector cannot point at is now a candidate, not a finding**
(`KM1_CANDIDATE_UNLOCATED`, 42 rows).

### Independent validation

The KM1-004 session hand-transcribed Allica and Alrayan. Allica is an Article 433b disclosure headed
"Key metrics" in which the string "KM1" never appears — this detector catches it on `UK 7a/7b/7c/7d`,
FY2022–FY2025 `KM1_PRESENT`, FY2020 `NO_KM1_FOUND`, matching their transcription. My `uk_rows` field
also independently reproduced their row-set drift finding (`8a/9a/10a` present FY2022–23, gone
FY2024–25).

### The "no Pillar 3" question, answered carefully

28 banks have no `KM1_PRESENT` in any cited edition — but only **12** are pure `NO_KM1_FOUND` with no
candidates and no fetch problems. `national_bank_of_egypt_uk` is 7 blocked + 2 scanned + 1 readable:
effectively **unsurveyed**, and would be fabricated as "Not applicable" by anyone reading the list
naively.

**SDDT does not rescue this.** 10 of 28 hold a PRA Rule 3.1 waiver, but every start date is 2024–2026,
so date-fitted it explains at most the latest edition year. And it is not a predictor: Secure Trust,
C. Hoare, Cambridge & Counties and Monument all hold Rule 3.1 waivers **and** print full KM1 tables.

### KM1-003 reconnaissance (not started; ticket untouched)

- **ALDERMORE** — live index carries THREE uncited editions: FY2020 `/media/axcpvnoo/`, FY2021
  `/media/ahbpvlih/`, FY2023 `/media/ynohqczi/`. Newest is FY2026, already cited. Checked 2026-09-16.
  Its KM1 is **six columns, Group a/b/c + Bank a/b/c** — the entity-basis rule applies inside one table.
- **AIB GROUP UK** — zero cited Pillar 3 PDFs. `aibgb.co.uk`/`aibni.co.uk` return 403 "Access Denied"
  to two independent clients: **BLOCKED, not dead**. The Irish parent publishes
  `AIB-Group-plc-Q1-2026-Pillar-3-Disclosures.pdf` on a page that names the UK subsidiary zero times —
  a **decoy** under the entity-basis rule.
- **ACCESS BANK UK** — its 403 is `cf-mitigated: challenge`, `server: cloudflare`. A JS interstitial,
  **not** an access denial.
- **ICBC LONDON** — KM1 denominated in **USD**, not sterling.

### Session limit

WebSearch budget exhausted (200/200). Step-1 latest-edition checks now run via curl against index
pages — which worked for Aldermore but fails silently on blocked hosts. A bank whose index cannot be
reached is reported BLOCKED, never guessed.
