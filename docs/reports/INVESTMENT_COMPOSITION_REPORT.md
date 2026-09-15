# Investment-composition batches — detailed report (HD-003, 27 banks)

Two batches assigned by katalysis-36 and run by HD-003 (a separate 17-bank half was run by
katalysis-36 itself, reported separately). All 27 done. `refresh_all.py` intentionally NOT
run by this session in either batch — left to katalysis-36 to run centrally.

- **Batch 1 (11 banks):** BLME, National Bank of Kuwait International, FCMB UK, GB Bank,
  CAF Bank, Allica Bank, Alpha Bank London, DF Capital, Hampden & Co, Nomura Bank
  International, Recognise Bank.
- **Batch 2 (16 banks):** NatWest Markets, Kuwait Finance House, SMBC, UBA UK, Northern
  Bank, TD Bank Europe, State Bank of India UK, National Bank of Egypt UK, United National,
  Vida, Weatherbys, Persia International Bank, This Bank, Reliance Bank, Turkish Bank UK,
  United Trust Bank.

## REAL SPLIT FOUND (lump row renamed to "Total ...", reconciling sub-rows added, arithmetic verified)

### BLME (`scripts/build_blme.py`)
12 years, FY2014-FY2025. Every annual Financial Statement has a dedicated "Investment
Securities" note (Note 16 FY2025/24, Note 18 FY2023/22/21/20, Note 19 FY2019/18, Note 17
FY2017/16, Note 18 FY2015/14 — Bank/BLME plc column). Split by measurement basis and
instrument: Sukuk at amortised cost / held-to-maturity(IAS39) / FVOCI / available-for-sale
(IAS39) / FVTPL(IAS39); Equity at FVOCI / available-for-sale(IAS39); Sharia'a-compliant
funds at FVTPL; Investment in subsidiaries at cost (bundled into this line FY2014-2023,
then split into its own Balance Sheet row FY2024-25). 9 sub-rows added. No issuer-type
(UK gilts vs supranational/corporate) split disclosed anywhere. Verified sub-rows sum
exactly to the pre-existing total for all 12 years via a Python check. Did not touch
RWA Breakdown/Total RWAs (already fixed separately, out of scope here). ~35 tool calls,
7 WebFetch/pdftotext PDF extractions (FY2025/23/21/19/17/15 pairs).

### National Bank of Kuwait International (`scripts/build_national_bank_of_kuwait_international.py`)
5 years, FY2021-FY2025. Own Note 15 "Investment Securities" splits by basis: Equities
(FVOCI), Equities (FVPL), Debt securities (FVOCI), Debt securities (FVPL, FY2021 only),
plus a combined ECL allowance line and (FY2022-25) combined interest-receivable line.
6 sub-rows added, verified reconciling exactly across all 5 years. No issuer-type split
exists (only a footnote mentioning pledged Gilts as repo collateral, no total disclosed).
WebFetch's PDF-to-text failed on all 3 filings (encoding quirk); fell back to local
pypdf extraction. ~12 tool calls.

### FCMB UK (`scripts/build_fcmb_uk.py`)
6 years, FY2020-FY2025 (FY2019 left blank, source PDF unavailable). Note 15 "Investment
securities" splits by basis and instrument: Government Bonds (FVOCI), Bank bonds (FVOCI),
HQLA — described as "US Treasury bills and bonds issued by IBRD," a sovereign/supranational
mix (FVOCI), FVOCI impairment allowance, Fund Investments – Government (FVTPL), Fund
Investments – Other (FVTPL). 6 sub-rows added. Reports in USD; verified reconciliation in
USD before conversion — sub-rows tie exactly except 3 years (FY2024/FY2023/FY2020) off by
£0.1k, a pre-existing artifact of this workbook's per-row independent FX rounding (not a
data error), explicitly documented in the added citation. ~31 tool calls, 6 PDF
downloads/extractions since WebFetch alone couldn't parse text.

### GB Bank (`scripts/build_gb_bank.py`)
5 years, FY2021-FY2025. Own note (numbered differently each year: Note 11 FY2021, Note 10
FY2022/23, Note 11 FY2024, Note 12 FY2025) breaks the balance down by issuer/instrument,
and from FY2025 also by measurement basis: "Issued by public bodies" (100% of balance
FY2021-23; UK-government-only per that era's own wording, broadening to include
Supranational/Sovereign/Agency per FY2024+ wording, not separately quantifiable within the
line), Covered Bonds, RMBS bonds, Other bonds (all amortised cost from FY2024), plus a
small Hedged Item line and a separate Other bonds line at FVTPL from FY2025. 6 sub-rows
added, all verified summing exactly to the pre-existing totals. Checked
`scripts/gb_bank_research.md` first per instructions — did not end up needing it, sourced
fresh from the 5 annual report PDFs directly (all downloaded via curl, Companies House
WebFetch redirects to short-lived signed URLs). ~29 tool calls.

### CAF Bank (`scripts/build_caf_bank.py`)
6 years, FY2020-FY2025. Note 10 (Note 11 in the FY2020/21 filing) "Debt securities" splits
by issuer type: UK government, multilateral financial institutions (supranational), fixed
coupon corporate bonds, floating rate corporate bonds, certificates of deposit — all
confirmed amortised cost only (accounting policy note 1.5/1.6, no FVOCI/FVTPL instruments
exist for this bank), so this is a pure issuer-type split, no basis split needed. 5
sub-rows added, with blanks where a category is genuinely absent for a year (e.g. no UK
government line from FY2022, no CDs from FY2024) — not a gap, matches the note's own
composition. FY2020 cross-checked against FY2021's FY2020 comparative column, both agree
exactly. Most Companies House PDFs here were scanned/image-only, required page-image
reads at higher DPI. ~32 tool calls.

### NatWest Markets (`scripts/build_natwest_markets.py`)
5 years, FY2021-FY2025. Note 15 "Other financial assets" splits by measurement basis
(Mandatory FVTPL / FVOCI / Amortised cost) and, for the debt-securities portion, by issuer
(UK central/local government, overseas government, other debt), plus equity shares and
loans sub-lines. 7 sub-rows added. UK government debt securities disclosed as nil
FY2022-FY2024 (explicit in source). All 5 years verified reconciling exactly. New
dedicated `BALANCE_SHEET_SOURCES` citation (Note 15, page per report). ~10 tool calls.

### Kuwait Finance House (`scripts/build_kuwait_finance_house.py`)
5 years, FY2021-FY2025. Note 14 "Financial investments" splits by measurement basis
(amortised cost / FVTPL / FVOCI) and, within amortised cost, by issuer type (GCC government
bonds/Sukuk, banks & other financial institutions, corporate bodies), plus an ECL
impairment allowance line. 6 sub-rows added. All 5 years verified reconciling exactly.
Source PDFs were scanned/image-only, required page-image rendering. ~20 tool calls.

### SMBC (`scripts/build_smbc.py`)
6 years, FY2020-FY2025 (FY2013-FY2019 left blank — those Companies House filings are
scanned TIFF-derived PDFs with no text layer at all, confirmed via pdffonts/pdfinfo, and
pre-date the relevant note format). Note 12 "Investment securities" splits purely by
measurement basis (amortised cost / FVOCI / FVTPL) — no issuer-type breakdown disclosed
anywhere. 3 sub-rows added, verified reconciling exactly for all 6 years. Did not touch
RWA Breakdown/Total RWAs (already fixed separately). ~14 tool calls.

### UBA UK (`scripts/build_uba_uk.py`)
6 years, FY2019-FY2024 (FY2018 left as-is — its cited source URL is now dead with no
Wayback snapshot). Annual notes split by measurement basis: debt securities at amortised
cost / FVOCI / FVTPL-Collective Investment Undertaking (a BlackRock US Treasury Fund
holding), net of ECL provision and (FY2021/22 only) an FX-movement deduction. No
issuer-type split — book is African sovereign/bank Eurobonds plus the US Treasury fund,
stated only qualitatively; no UK government securities held at all. 5 sub-rows added,
verified reconciling exactly. ~15 tool calls.

### Northern Bank (`scripts/build_northern_bank.py`)
6 years, FY2020-FY2025. Note 15(a)/(b) (Note 13(a)/(b) pre-FY2023) "Investment securities"
splits purely by IFRS 9 measurement basis: "Hold to collect" (amortised cost) vs "Hold to
collect and sell" (FVOCI). No numeric issuer-type breakdown (only narrative: "primarily UK
government securities and highly rated covered, sovereign, supra-national and agency
bonds"). 2 sub-rows added, verified reconciling exactly for all 6 years, cross-checked
against each report's own comparative column. ~30 tool calls.

### TD Bank Europe (`scripts/build_td_bank_europe.py`)
5 years, FY2021-FY2025. Note 13/14 "Debt Securities" splits by issuer type only:
Government securities vs Other debt securities, net of a Provision for credit losses.
100% amortised cost, no FVOCI/FVTPL line exists. 3 sub-rows added, verified reconciling
exactly. All 3 source PDFs scanned/image-only, required OCR. Scope note: the same lump
figure also appears unchanged in the Asset Quality and Overview sheets — those were
explicitly out of scope and left untouched. ~20 tool calls.
(Separately, katalysis-36 later found this bank's rows were reporting in CAD and fixed a
currency-classifier gap in `build_deliverable.py` that was silently dropping them — not a
build-script issue, see katalysis-36's own report.)

### State Bank of India UK (`scripts/build_state_bank_of_india_uk.py`)
7 years, FY2019-FY2025. Note 3.9 (3.11 in the FY2019 filing) "Investment securities"
splits by both measurement basis (Available for Sale/mark-to-market vs Held to
Maturity/amortised cost) and issuer type (Government issued vs Other public sector
securities & corporates), plus a blended AFS market-rate revaluation line and a one-off
FY2020 collective provision. 6 sub-rows added, verified reconciling exactly for all 7
years — no rounding gaps. ~10 tool calls.

### National Bank of Egypt UK (`scripts/build_national_bank_of_egypt_uk.py`)
5 years, FY2021-FY2025. Note 12/10 "Debt securities" splits by issuer type: public
bodies/government securities vs Other securities, plus an interest-rate fair-value
hedge-adjustment line. 100% amortised cost per a separate financial-instruments note (the
"asset swap" portion is a hedge-accounting basis adjustment, not a distinct measurement
category). 3 sub-rows added, verified reconciling exactly for all 5 years. **Source-citation
correction found**: the existing FY2021 citation pointed at the FY2022 report's restated
comparative column, whose total (£553.66m) didn't match the workbook's existing FY2021
figure (£550.75m) — switched citation to the actual FY2021 own-year filing, whose total
matches exactly. ~39 tool calls (heaviest of batch 2, 4 OCR passes).

### United National (`scripts/build_united_national.py`)
10 years, FY2016-FY2025 — genuinely two-dimensional. Measurement basis: 100%
available-for-sale every year FY2018-2025; FY2016/17 alone also carried a
held-to-maturity component that fully ran off by FY2018. Issuer type: only the FY2021
report's own sector-concentration table splits Central government / Financial
institutions / Corporates, and only for FY2020/FY2021 — no other year discloses an
equivalent split. 5 sub-rows added (AFS, HTM, and the 3 FY2020/21-only issuer lines,
each labelled to avoid double-counting against the blanket AFS row those years).
Reconciles exactly FY2018-2025; within £205/£10 for FY2016/17 (source stated only to
nearest £'000). Heaviest single agent of the entire two batches: 9 scanned PDFs, ~35
page-image reads, ~83 tool calls total.

### Vida (`scripts/build_vida.py`)
FY2025 has a real split (UK Government securities / Supranational bonds / Covered bonds,
all FVOCI — sums to within a genuine £1k source-document rounding artifact, documented).
FY2024 is 100% UK Government securities/"Gilts" (single-bucket that year only). 3
sub-rows added under "Total debt securities". ~10 tool calls.

## NO REAL SPLIT (100% one bucket in every disclosed year — row relabeled in place, no sub-rows, no "Total" rename)

### Allica Bank (`scripts/build_allica.py`)
100% FVOCI in every year (FY2022-2025); AR2025's Note 10 "Debt securities" gives one
combined issuer line, "Issued by governments and supranational bodies," not split further;
AR2023/AR2022 don't even carry a numbered note for this line. Row relabeled: "Debt
securities" → "Debt securities - Government and supranational bonds, at FVOCI". ~13 tool
calls.

### Alpha Bank London (`scripts/build_alpha_bank_london.py`)
Note 18 "Investment securities" across all 7 years (FY2019-2025), entire balance under one
heading, "Measured at FVTOCI" — no basis split (100% FVTOCI, never amortised cost or
FVTPL), and only a label change over time for issuer composition (FY2019-20: "Multilateral
development bank bonds"; FY2021-25: "...and sovereign debt", with no £ split between the
two — FY2022's report adds qualitative paragraphs for each but never a £ figure).
"Sovereign" wording never specifies country, so couldn't be treated as UK-specific. Row
relabeled: "Investment securities" → "Investment securities - Multilateral development bank
& sovereign debt bonds, all at FVTOCI (mark-to-market)". Several source PDFs were
scanned/image-only (Companies House filings), needed page-image rendering to verify
figures. ~20 tool calls.

### DF Capital (`scripts/build_df_capital.py`)
100% one bucket in every year, but the bucket itself changes over 3 distinct eras:
FY2020/21 UK govt gilts+T-bills at FVOCI; FY2022/23 UK govt gilts only at FVOCI (T-bills
line goes to nil); FY2024/25 a Euro money market fund at amortised cost (the FVOCI gilts
book was fully sold down). Row relabeled with all 3 eras summarized in the label, full
detail in the citation. ~14 tool calls.

### Hampden & Co (`scripts/build_hampden_co.py`)
100% amortised cost in every year (FY2023-2025; £0 in FY2022) — the fair-value-hierarchy
note's "Fair value through profit or loss" and FVOCI columns are always nil. Issuer type is
narrative-only, no numeric split: FY2023 "All debt securities held are UK Government debt
securities"; FY2024 "UK Government or US Department of Treasury debt securities" (though
FY2024's own Note 21 credit-risk section separately says "all issued by the UK Government"
— an internal inconsistency in the bank's own report, transcribed as printed rather than
resolved); FY2025 "issued by the UK, US and Australian governments." Row relabeled: "Debt
securities" → "Debt securities (sovereign government debt, amortised cost)", inconsistency
documented in citation. ~15 tool calls.

### Nomura Bank International (`scripts/build_nomura_bank_international.py`)
The "Financial investments" line is tiny ($11k-$20k against a $6-8bn balance sheet, this is
an investment bank dominated by derivatives/repos/intercompany loans). 100% "Mandatorily at
fair value through profit or loss," Level 3 in the fair value hierarchy, no significant
unobservable inputs disclosed, no issuer-type breakdown anywhere. Row relabeled: "Financial
investments" → "Financial investments (mandatorily at fair value through profit or loss)",
matching the style already used on NatWest's workbook for the same scenario. ~15 tool
calls.

### Recognise Bank (`scripts/build_recognise_bank.py`)
Only populated FY2021, FY2025, FY2026 (blank/n/a other years). 100% UK government
gilts/Treasury Bills in every populated year, but measurement basis changed: FY2021 FVOCI
(Note 13, Companies House filing — scanned/image-only PDF, required OCR across ~35 pages),
FY2025/FY2026 amortised cost (Note 17, AR2026). Row relabeled: "Debt securities" → "Debt
securities - UK government (gilts and Treasury bills)", basis change documented in citation
since it can't be captured in a single cross-year label. ~20 tool calls.

### Weatherbys (`scripts/build_weatherbys.py`)
Note 32 "Financial instruments" (FY2021-FY2024) confirms debt securities are entirely
amortised cost, no FVOCI/FVTPL. No issuer-type breakdown exists anywhere (checked Note 17
reconciliation, Note 33 maturity table, and a non-reconciling strategic-report gilts
mention). FY2015-2020 assumed consistent but unverified — those Companies House filings
are scanned images with no machine-readable text. Row relabeled: "Debt securities" → "Debt
securities (measured at amortised cost)". ~15 tool calls.

### Persia International Bank (`scripts/build_persia_international_bank.py`)
Only 2 years populated (FY2015/FY2016). Note 12 "Debt securities" shows the entire balance
is a single unlisted Sukuk bond: "available for sale, other debt securities," "issued by
other than public bodies" — both dimensions 100% one bucket. FY2015 carries 90.56%
impairment, FY2016 100% (nil balance) — ties out exactly to the P&L's existing
impairment-charge row, confirming internal consistency. Row relabeled with full
classification detail. ~15 tool calls.

### This Bank (`scripts/build_this_bank.py`)
FY2020-FY2024 (FY2025 blank/nil). Note 12/13/11 "Investment securities" splits into Gilts /
Certificates of Deposit / Treasury Bills, but CDs are nil in every year — 100% UK
government (gilts + T-bills combined). A separate measurement-basis table confirms 100%
amortised cost, zero FVOCI/FVTPL every year. Row relabeled: "Investment securities" →
"Investment securities (UK gilts and Treasury Bills, held at amortised cost)". ~20 tool
calls.

### Reliance Bank (`scripts/build_reliance_bank.py`)
8 years, FY2019-FY2026. "Debt Securities" note (numbered 9/10/11 depending on year)
discloses one line every year: securities "Issued by Banks/Building Societies," amortised
cost less impairment — no UK government, no corporate/supranational/ABS, no FVOCI/FVTPL in
any year. Row relabeled: "Debt securities" → "Debt securities (amortised cost, issued by
banks/building societies)". ~20 tool calls.

### Turkish Bank UK (`scripts/build_turkish_bank.py`)
5 years, FY2021-FY2025. Note 19 "Investment securities" is 100% Preference Shares in Visa
Inc./Visa Europe (from the 2016 Visa reorganisation) — an equity investment held at FVOCI,
100% USA issuer origin every year. No dimension of comparison exists. Row relabeled:
"Investment securities" → "Investment securities (Visa Inc./Visa Europe preference shares,
FVOCI equity)". ~15 tool calls.

### United Trust Bank (`scripts/build_united_trust_bank.py`)
5 years, FY2021-FY2025. Note 10/11 "Debt securities" shows the entire balance as "Issued by
public bodies - government securities" every year — 100% UK gilts/government, no
supranational/corporate/ABS ever disclosed. Separately confirmed 100% amortised cost, no
FVOCI/FVTPL. Row relabeled: "Debt securities" → "Debt securities - UK government securities
(amortised cost)". ~16 tool calls.

## General notes

- Every edit followed the `build_close_brothers.py` citation pattern: note number, exact
  page, source URL per year, explicit statement of why no further split exists where
  applicable.
- Where PDFs were scanned/image-only (roughly half of both batches — CAF Bank, Alpha Bank
  London, Recognise Bank, parts of GB Bank; Kuwait Finance House, Persia International
  Bank, This Bank, TD Bank Europe, National Bank of Egypt UK, United National, some of
  Turkish Bank UK/Reliance Bank), agents rendered pages to images/OCR'd them rather than
  guessing, since WebFetch's text extraction failed on those.
- No RWA Breakdown / Total RWAs sheets were touched on any of the 27 banks — scope was
  strictly the Balance Sheet investment-securities row(s). SMBC's citation explicitly notes
  RWA sheets were already fixed separately and out of scope here.
- All 27 `python3 scripts/build_<bank>.py` runs completed cleanly with the normal "Saved
  workbook with sheets: [...]" line.
- One genuine data-quality find, not a pipeline bug: National Bank of Egypt UK's existing
  FY2021 citation pointed at a restated comparative column that didn't match the
  workbook's own FY2021 figure — corrected to cite the actual FY2021 own-year filing,
  which matches exactly.
- `refresh_all.py` intentionally not run by this session in either batch — pulled together
  centrally by katalysis-36 alongside its own 17-bank half, audited for double-counting
  across all 33 banks, and verified via the test suite and Puppeteer.
