import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

# Entity was named "Belmont Green Finance Limited" (trading as Vida/Vida
# Homeloans) through FY2023, renamed "Vida Bank Limited" on receiving its PRA
# banking licence 19 Nov 2024. FY2022 cash flow was recorded here as "a genuine
# gap" until 2026-09-18; it was not one - see FY2022_FOUND_NOTE.
# Pillar 3 only exists from FY2024 (first year as a bank).
# Extended back to FY2018 (confirmed historical floor per HD-057): FY2018-
# FY2020 the entity was "Belmont Green Finance Limited", a specialist
# mortgage lender regulated only by the FCA (not yet PRA-authorised, no
# banking licence) - see ENTITY_NOTE for detail on what that means for each
# sheet type.
YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021", "FY2020", "FY2019", "FY2018"]  # most recent first
YEAR_LABEL = {y: y for y in YEARS}

AR2025_URL = "https://www.vidabank.co.uk/media/pkmnxlqg/annual-report-and-accounts-2025-company.pdf"
AR2024_URL = "https://www.vidabank.co.uk/media/emghy4z2/annual-report-and-accounts-2024-company.pdf"
AR2023_URL = "https://www.vidabank.co.uk/media/zhoj0swe/annual-report-and-accounts-2023.pdf"
AR2021_URL = "https://www.vidabank.co.uk/media/p3wau0ms/annual-report-and-accounts-2021.pdf"

# FY2022 Annual Report (Belmont Green Finance Limited) - Companies House only.
# No copy is published on vidabank.co.uk's media library, which is why earlier
# passes never opened it; the Companies House copy is an IMAGE-ONLY SCAN
# (go-tiff2pdf / CCITT G4, 303 dpi, 164 pages, zero-character text layer), so a
# text search of it returns nothing whatever it contains. Read here via full-
# document OCR (ocrmypdf --force-ocr, tesseract 5.5.3) and confirmed against a
# 300 dpi render of the page itself.
AR2022_URL = "https://find-and-update.company-information.service.gov.uk/company/09837692/filing-history/MzM4Nzk2MDY5OWFkaXF6a2N4/document?format=pdf&download=0"

# FY2018-FY2020 Annual Reports (Belmont Green Finance Limited) - sourced from
# Companies House filing history (company number 09837692), re-verified this
# session directly from the filed PDFs rather than assumed from an earlier scan.
AR2018_URL = "https://find-and-update.company-information.service.gov.uk/company/09837692/filing-history/MzIzMzYzMjc1OWFkaXF6a2N4/document?format=pdf&download=0"
AR2019_URL = "https://find-and-update.company-information.service.gov.uk/company/09837692/filing-history/MzI4NjAzOTYwNWFkaXF6a2N4/document?format=pdf&download=0"
AR2020_URL = "https://find-and-update.company-information.service.gov.uk/company/09837692/filing-history/MzMwNjUyMjA5MmFkaXF6a2N4/document?format=pdf&download=0"

P3_2025_URL = "https://www.vidabank.co.uk/media/od2lpxc0/vghl-pillar-3-report-2025-final.pdf"
P3_2024_URL = "https://www.vidabank.co.uk/media/mucbqgwi/vghl-pillar-3-report-2024-final.pdf"

ENTITY_NOTE = (
    "ENTITY NOTE: the company (FRN 738741, Companies House 09837692) was named 'Belmont Green Finance Limited' "
    "(trading as Vida / Vida Homeloans) through its FY2023 Annual Report, and was renamed 'Vida Bank Limited' after "
    "receiving its PRA banking licence on 19 November 2024. This workbook uses 'Vida Bank Limited' throughout since "
    "that is its current name. Pre-authorisation (FY2018-FY2023), the business was funded mainly through mortgage "
    "securitisation (numerous 'Tower Bridge Funding' special-purpose vehicles) and warehouse facilities rather than "
    "retail deposits; the FY2023 Annual Report's own commentary describes the business as still 'preparing for the "
    "banking licence'. FY2018-FY2020 the company was regulated only by the FCA (mortgage lending/administration "
    "permissions) - not the PRA - and had no banking licence and no deposit-taking business at all; its own FY2019 "
    "and FY2020 Annual Reports both still describe the banking licence application as in progress/delayed. "
    "Cash flow figures below are on the Company's own (non-consolidated/solo) basis in every populated year - this "
    "is the only basis for which a full three-part cash flow statement (operating/investing/financing) could be "
    "found in every report; the Consolidated (Group) statement of financial position was reported each year from "
    "FY2019 onwards. (CORRECTED 2026-09-18: this note previously said the FY2022 AND FY2023 Annual Reports print "
    "only a partial Group operating-activities reconciliation and no full Group cash flow statement. That is true "
    "of the FY2023 report; it is NOT true of the FY2022 report, which prints a full three-part CONSOLIDATED "
    "Statement of Cash Flows on printed p.117 AND a full three-part COMPANY statement on printed p.161. The claim "
    "had been generalised from the one report that was actually opened - see FY2022_FOUND_NOTE.) FY2018's own "
    "Annual Report only presented Company-"
    "only financial statements (no Group/consolidated accounts were filed for FY2018); Group consolidated accounts "
    "for Belmont Green Finance Limited first appear in the FY2019 Annual Report, which also restates FY2018's "
    "Company-basis Balance Sheet, Cash Flow Statement and Statement of Changes in Equity figures - see "
    "FY2018_RESTATEMENT_NOTE below for why this workbook uses those restated figures rather than the originally-"
    "filed FY2018 Annual Report's own (much smaller) figures."
)

FY2018_RESTATEMENT_NOTE = (
    "FY2018 RESTATEMENT NOTE: Belmont Green Finance Limited's own, originally-filed FY2018 Annual Report "
    f"({AR2018_URL}) reported total Company assets of only £132,973k, Loans to customers of just £450k (almost "
    "all mortgage exposure sat in warehouse/securitisation special-purpose vehicles, recognised via 'Other "
    "receivables' subordinated loan notes rather than on the Company's own balance sheet), and a full three-part "
    "Company cash flow statement with operating activities of £(45,851)k / financing activities of £44,782k. The "
    "subsequent FY2019 Annual Report's Note 28(d) explains that this presentation was reassessed: 'following a "
    "thorough analysis and in accordance with IFRS9, it has been established that BGFL retains substantial risks "
    "and rewards' of the securitised mortgage assets, so the FY2019 Annual Report's own restated FY2018 comparative "
    "brings the securitised loan book onto the Company's balance sheet (Loans to customers restated to £1,197,862k) "
    "with an offsetting 'Deemed loan due to Group undertakings' liability, and correspondingly grosses up the FY2018 "
    "Company cash flow statement's operating and financing activities (to £(763,195)k and £762,125k respectively) "
    "with no change to the net cash movement or cash balances. This workbook uses the FY2019 Annual Report's "
    "restated FY2018 figures throughout the Balance Sheet, Cash Flow Statement and Statement of Changes in Equity "
    "sheets, for consistency with FY2019 onwards' presentation (which uses the same 'Deemed loan due to Group "
    "undertakings' convention) - not the originally-filed FY2018 Annual Report's figures, which are noted here for "
    "transparency rather than blended in."
)

FY2022_FOUND_NOTE = (
    "FY2022 (FILLED 2026-09-18 - IT WAS NEVER A GAP IN THE DISCLOSURE, ONLY IN OUR READING). This sheet previously "
    "carried a note saying 'neither the FY2022 nor FY2023 Annual Report presents a full three-part Company cash "
    "flow statement for FY2022', with the FY2023 report cited as the document checked. Only the FY2023 report had "
    "in fact been checked. Belmont Green Finance Limited's OWN FY2022 Annual Report prints a complete three-part "
    "Company cash flow statement - operating, investing and financing, with opening and closing cash - on printed "
    "p.161, presented under the running head 'Notes to the Company Financial Statements (continued)' rather than "
    "under a title of its own, which is why a heading search for 'Company Statement of Cash Flows' finds nothing "
    "in it. (The same report also prints a full CONSOLIDATED Statement of Cash Flows on printed p.117, so the "
    "Group-basis claim was wrong for FY2022 too.) The reason it had not been read is a sourcing one, not a "
    "disclosure one: vidabank.co.uk's media library carries the 2021, 2023, 2024 and 2025 reports but not 2022, "
    f"and the Companies House copy ({AR2022_URL}) is an image-only scan with a zero-character text layer, so any "
    "text search of it returns nothing regardless of content. It was read by OCRing all 164 pages and then "
    "confirming the figures against a 300 dpi render of p.161 itself.\n"
    "BASIS: Company (non-consolidated), identical to every other populated year here. The same page's 2021 "
    "comparative column reproduces this workbook's existing FY2021 column cell for cell (operating (179,449); PPE "
    "(190); software (1,567); investing (1,757); shares issued 8,300; deemed loans 169,705; leases (1,407); "
    "financing 176,598; net (4,608); opening 18,108; closing 13,500), which confirms both the basis and the "
    "transcription.\n"
    "TWO DIVERGENCES ARE REPRODUCED RATHER THAN RECONCILED, both verified on the page image:\n"
    "(1) The Bank's own FY2022 financing subtotal does not foot. Its three financing lines are nil, (31,392) and "
    "(1,365), which sum to (32,757), but the printed 'Net cash (utilised)/generated by financing activities' reads "
    "(32,755) - a £2k break in the BANK's own arithmetic. The printed (32,755) is the odd figure out: the printed "
    "net increase of 1,419 equals 35,347 - 1,171 - 32,757 and ties exactly to the printed cash balances "
    "(13,500 -> 14,919), whereas the printed subtotal would give 1,421. Both the components and the subtotal are "
    "transcribed exactly as printed; nothing has been adjusted to make the column foot.\n"
    "(2) 'Proceeds from shares issued' is printed as a DASH for FY2022 and is carried here as a literal '-'. A "
    "dash is the Bank stating nil, which is a different statement from a blank cell (no such line) and from a "
    "typed zero; it is kept as printed. The workbook's block-reconciliation check still reads the column and "
    "reports divergence (1) as a financing-block break of exactly £2k (-32,757 summed vs -32,755 printed), which "
    "is the intended outcome: the disagreement is the Bank's, and it stays visible.\n"
    "FY2022/FY2023 BOUNDARY: FY2022's own report closes cash at 14,919 while the FY2023 column (taken from the "
    "FY2024 report's comparative) opens at 14,920 - a £1k cross-edition difference, left as each edition printed "
    "it. The FY2022 Annual Report's own Company loss of £(25,453)k was also later restated; this workbook's "
    "Statement of Changes in Equity already carries the restated FY2022 figures from the FY2023 report and "
    "documents that boundary separately. The cash flow column here is FY2022's own edition throughout."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are Vida Bank Limited's own Company (non-consolidated) cash flow statement, £'000:\n"
    f"FY2025: Vida Bank Limited Annual Report and Accounts 2025 (Company), p.55 (Statement of Cash Flows) - "
    f"{AR2025_URL}\n"
    f"FY2024: Vida Bank Limited Annual Report and Accounts 2024 (Company), p.73 (Statement of Cash Flows) - "
    f"{AR2024_URL}\n"
    f"FY2023: taken from Vida Bank Limited's FY2024 Annual Report's own FY2023 comparative column (p.73, same "
    f"document as above) - Belmont Green Finance Limited's own FY2023 Annual Report does not present a comparable "
    f"Company-basis statement (see ENTITY_NOTE/FY2022_FOUND_NOTE).\n"
    f"FY2022: Belmont Green Finance Limited Annual Report and Accounts 2022, printed p.161 / PDF p.161 (the "
    f"Company cash flow statement, printed under the running head 'Notes to the Company Financial Statements "
    f"(continued)'; the operating-activities reconciliation behind it is Note 34 on printed p.164) - {AR2022_URL} "
    f"(Companies House copy, image-only scan, read by OCR and confirmed against a 300 dpi page render - see "
    f"FY2022_FOUND_NOTE).\n"
    f"FY2021: Belmont Green Finance Limited (Vida) Annual Report and Accounts 2021, p.150 (Company Statement of "
    f"Cash Flows) - {AR2021_URL}\n"
    f"FY2020: Belmont Green Finance Limited Annual Report and Accounts 2020 (Company Statement of Cash Flows) - "
    f"{AR2020_URL}\n"
    f"FY2019: Belmont Green Finance Limited Annual Report and Accounts 2019 (Company Statement of Cash Flows, "
    f"Note 35-37 breakdown) - {AR2019_URL}\n"
    f"FY2018: taken from the FY2019 Annual Report's own restated FY2018 comparative column (same document/notes as "
    f"above) - see FY2018_RESTATEMENT_NOTE for why the restated figures are used in place of Belmont Green's "
    f"originally-filed FY2018 Annual Report ({AR2018_URL}).\n\n"
    + ENTITY_NOTE + "\n\n" + FY2022_FOUND_NOTE + "\n\n" + FY2018_RESTATEMENT_NOTE
)


def p3_sources():
    return (
        "Sources - Vida Group Holdings Limited/plc Pillar 3 disclosures (Table 3.1 KM1 - Key Metrics; the smallest "
        "regulatory group Vida Bank Limited is consolidated into - no Vida-Bank-Limited-only Pillar 3 disclosure is "
        "separately published):\n"
        f"FY2025: Vida Group Holdings plc Pillar 3 Disclosures 2025, p.5 (3.1 Key Metrics / Table KM1) - {P3_2025_URL}\n"
        f"FY2024: Vida Group Holdings Limited Pillar 3 Disclosures 2024, p.5 (3.1 Key Metrics / Table KM1) - {P3_2024_URL}\n"
        "BASIS DETERMINATION, made 2026-09-15 by reading section 1.3 'Scope' of both reports directly (they are "
        "word-for-word identical on this point). Verbatim: 'VGHL is a financial holding company and it is a CRR "
        "consolidation entity. This Pillar 3 report is prepared on a consolidated basis. Vida Bank Limited (\"VBL\") "
        "is the principal regulated subsidiary of the Group. The same basis of consolidation is used for the "
        "preparation of the Group's Annual Report and Accounts as is used for regulatory reporting.' Section 1.2 "
        "'Basis of Disclosure' adds, equally verbatim: 'Regulatory ratios are presented on a Group-basis only.' "
        "Three consequences follow, and they are why the figures above are kept rather than demoted to memo rows. "
        "(1) VGHL is not an incidental parent that merely happens to contain the bank - it is the CRR CONSOLIDATION "
        "ENTITY, i.e. the level at which the PRA actually sets and measures Vida's regulatory capital requirement, "
        "with VBL as the principal regulated subsidiary. This is the smallest regulatory group VBL belongs to. "
        "(2) No VBL-solo ratio exists to prefer over it: 'Group-basis only' is the publisher's own statement that "
        "the solo figures are not disclosed anywhere, so the choice is between the consolidated figure and nothing "
        "at all - not between a group figure and a suppressed entity figure. (3) The Group and the Annual Report "
        "use the same basis of consolidation, so these ratios are reconcilable to the accounts in this workbook "
        "rather than sitting on an unrelated perimeter. Accordingly every Pillar 3 sheet in this workbook carries "
        "the subtitle 'Vida Group Holdings basis' so the reader is never shown a consolidated ratio labelled as an "
        "entity one - the project rule this workbook observes is that group figures are never SUBSTITUTED for "
        "entity figures unlabelled, which is a different thing from refusing to report the only regulatory ratio "
        "that exists. Note also that both reports are reduced-scope Article 433b disclosures ('small and non-"
        "complex institution', UK CRR Article 4(145)), which is why the metric set here is narrower than a large "
        "bank's - it is a permitted reduction, not an omission.\n"
        "No Pillar 3 disclosure exists for FY2018-FY2023: Pillar 3 only applies once PRA-authorised as a deposit-"
        "taker, which happened 19 November 2024 (see ENTITY_NOTE on the Cash Flow Statement sheet). FY2018-FY2020 "
        "the company was FCA-regulated only (not PRA-authorised at all, no banking licence); its FY2019 and FY2020 "
        "Annual Reports confirm the banking licence application was still in progress/delayed those years.\n"
        "RE-VERIFIED 2026-09-12 (disclosure audit): the pre-authorisation gap is STRUCTURAL, independently "
        "confirmed against the Companies House register rather than the workbook's own prior claim. Company "
        "09837692 was incorporated 22 October 2015 and traded as 'Belmont Green Finance Ltd' (22 Oct 2015 - 10 Jun "
        "2019) and then 'Belmont Green Finance Limited' (10 Jun 2019 - 25 Nov 2024), only taking the name 'Vida "
        "Bank Limited' on 25 November 2024 - six days after the 19 November 2024 PRA authorisation. No Pillar 3 "
        "obligation can therefore exist for FY2018-FY2023, so those years are blank by regulation, not by omission.\n"
        "SDDT - EXPLICIT NEGATIVE, recorded 2026-09-15 (cross-bank SDDT date-fit pass) so that a future pass does "
        "not wrongly apply the Small Domestic Deposit Taker exemption to this workbook's gap years. Vida DOES "
        "hold the SDDT opt-in, but it is far too recent to explain anything here. The Bank of England "
        "consolidated list of waivers and modifications granted to PRA-authorised firms (downloaded 2026-09-15, "
        "https://www.bankofengland.co.uk/-/media/boe/files/prudential-regulation/authorisations/"
        "waivers-and-modifications-of-rules/consolidated-waivers-pra-firms.csv) carries three SDDT rows for FRN "
        "738741, 'Vida Bank Limited': (a) 'Modification by Consent - PRA Rulebook - CRR Firms - Rule 3.1 of the "
        "SDDT Regime - General Application Part', sub rule 'Ru 3.1', waiver ref 'A00011924P.pdf', START DATE "
        "03/04/2026, no end date; plus two eligibility-criteria modifications under sub rules 'Ru 1.2' and 'Ru "
        "2.1(9)', both ref 'A00010069P.pdf', start 25/03/2026, end 25/03/2029. Only row (a) matters: Rule 3.1 is "
        "the actual opt-in that removes the Pillar 3 disclosure obligation, whereas rules 1.2 and 2.1(9) merely "
        "modify eligibility CRITERIA (2.1(9) waives the 'any parent undertaking of the firm is a UK undertaking' "
        "test) and are not themselves evidence of any disclosure exemption.\n"
        "DATE FIT - IT DOES NOT FIT. Vida's accounting reference date is 31 DECEMBER, confirmed at Companies "
        "House (company 09837692, an unbroken run of accounts to 31 December from 2019 to 2025). The outstanding "
        "Pillar 3 gap years are FY2021, FY2022 and FY2023, which ended 31 December 2021, 2022 and 2023 "
        "respectively. The Rule 3.1 modification began 3 APRIL 2026 - between two and four and a half years "
        "AFTER every one of those year-ends, and after the FY2025 year-end too. A modification cannot explain a "
        "gap that predates it, so the SDDT regime explains NONE of the FY2021-FY2023 blanks.\n"
        "Those gaps already have a different and fully sufficient explanation, set out immediately above, and it "
        "is left exactly as it stands: the entity was not PRA-authorised as a deposit-taker until 19 November "
        "2024, so no Pillar 3 obligation existed in any of those years. That is a structural pre-authorisation "
        "absence, not an exemption. The register finding changes no cell in this workbook. Its only forward-"
        "looking value is that from 3 April 2026 Vida is an SDDT, so Pillar 3 documents of the kind used for "
        "FY2024 and FY2025 should not be expected for FY2026 onward. Note finally that this is the SDDT "
        "DISCLOSURE exemption, which is in force now - not the separate SDDT CAPITAL regime that begins 1 "
        "January 2027; the two are easy to conflate and must not be."
    )


bw = BankWorkbook(bank_name="Vida Bank Limited", years=YEARS, year_label=YEAR_LABEL, header_color="6E2C00")

STATEMENTS_ENTITY_NOTE = (
    "Balance Sheet / Statement of Changes in Equity are on Vida Bank Limited's own Company (non-consolidated) "
    "basis in every year, matching the Cash Flow Statement sheet's basis (see its own ENTITY_NOTE). Profit & Loss "
    "is on the Company basis for FY2025/FY2024 only (Vida's own Company Statement of Comprehensive Income exists "
    "for those two years); for FY2023/FY2022/FY2021/FY2020/FY2019, the Company took the section 408 Companies Act "
    "2006 exemption and published no separate Company income statement (only a one-line narrative profit/loss-"
    "after-tax figure, which ties to the equity ladder's own movement for that year), so the Group/Consolidated "
    "income statement is shown instead for those years. FY2018's own Annual Report did present a Company income "
    "statement, but it is not used here either, for consistency with every other pre-2024 year's Group-basis "
    "figures (see INCOME_STATEMENT_SOURCES for detail) - a genuine basis difference, not forced to a single basis."
)

BALANCE_SHEET_SOURCES = (
    "Sources - Vida Bank Limited's own Company (non-consolidated) Statement of Financial Position, £'000:\n"
    f"FY2025: Vida Bank Limited Annual Report and Accounts 2025 (Company), p.53 - {AR2025_URL}\n"
    f"FY2024: Vida Bank Limited Annual Report and Accounts 2024 (Company), p.71 - {AR2024_URL}\n"
    f"FY2023: Belmont Green Finance Limited Annual Report and Accounts 2023, p.185 (Company Statement of "
    f"Financial Position) - {AR2023_URL}\n"
    f"FY2022: taken from the FY2023 Annual Report's own restated FY2022 comparative column (same document/page "
    f"as above). Belmont Green's own FY2022 Annual Report has since been located and read (2026-09-18, see the "
    f"Cash Flow Statement sheet's FY2022_FOUND_NOTE); its own Company Statement of Financial Position is on "
    f"printed p.159 and its figures were superseded by the FY2023 report's restatement, so the restated "
    f"comparative is retained here deliberately rather than for want of the original.\n"
    f"FY2021: Belmont Green Finance Limited Annual Report and Accounts 2021, p.149 (Company Statement of "
    f"Financial Position) - {AR2021_URL}\n"
    f"FY2020: Belmont Green Finance Limited Annual Report and Accounts 2020, Company Statement of Financial "
    f"Position - {AR2020_URL}\n"
    f"FY2019: Belmont Green Finance Limited Annual Report and Accounts 2019, Company Statement of Financial "
    f"Position - {AR2019_URL}\n"
    f"FY2018: taken from the FY2019 Annual Report's own restated FY2018 comparative column (same document as "
    f"above) - see FY2018_RESTATEMENT_NOTE (on the Cash Flow Statement sheet's source note) for why the restated "
    f"figures are used in place of Belmont Green's originally-filed FY2018 Annual Report ({AR2018_URL}).\n\n"
    "DEBT SECURITIES BREAKDOWN: the 'Debt securities - ...' sub-rows below the headline 'Total debt securities' "
    "line are transcribed from each year's own Note 15 'Debt securities'. All debt securities are held at "
    "fair value through other comprehensive income (FVOCI) in both years - Note 11 'Financial instruments' "
    "(FY2025 AR, pp.75-76) shows the full £819,770k FY2025 balance and £34,135k FY2024 balance classified "
    "entirely as FVOCI, with nothing at amortised cost or FVTPL - so no measurement-basis split applies. "
    "Note 15 does split by issuer type:\n"
    f"FY2025: UK Government securities £537,441k, Supranational bonds £167,080k, Covered bonds £115,248k - "
    f"Note 15, p.81 - {AR2025_URL}. These three lines sum to £819,769k against the note's own stated total "
    f"of £819,770k - a £1k rounding difference present in the source document itself, not a transcription "
    f"error (the UK Government securities sub-row above is left at the source's own £537,441k rather than "
    f"plugged to force an exact tie-out).\n"
    f"FY2024: 100% UK Government securities (labelled 'Gilts' in this year's own note) - Note 15, p.102 - "
    f"{AR2024_URL}. No issuer-type split applies for FY2024 since the full £34,135k balance is one category.\n\n"
    + STATEMENTS_ENTITY_NOTE
)

INCOME_STATEMENT_SOURCES = (
    "Sources - £'000. FY2025/FY2024: Vida Bank Limited's own Company Statement of Comprehensive Income. "
    "FY2023-FY2018: Group/Consolidated Statement of Profit and Loss and Other Comprehensive Income "
    "(Company P&L exempted under s.408 in every one of these years - FY2018's own Annual Report is the sole "
    "exception, which did present a Company income statement, but it is not used here for consistency with "
    "every other year's Group-basis figures; see ENTITY_NOTE below):\n"
    f"FY2025: Vida Bank Limited Annual Report and Accounts 2025 (Company), p.52 - {AR2025_URL}\n"
    f"FY2024: Vida Bank Limited Annual Report and Accounts 2025 (Company), p.52, FY2024 comparative column - "
    f"{AR2025_URL}\n"
    f"FY2023: Belmont Green Finance Limited Annual Report and Accounts 2023, p.143 (Consolidated Statement of "
    f"Profit and Loss and Other Comprehensive Income) - {AR2023_URL}\n"
    f"FY2022: taken from the FY2023 Annual Report's own FY2022 comparative column (same document/page as above).\n"
    f"FY2021: Belmont Green Finance Limited Annual Report and Accounts 2021, p.109 (Consolidated Statement of "
    f"Comprehensive Income) - {AR2021_URL}\n"
    f"FY2020: Belmont Green Finance Limited Annual Report and Accounts 2020, Consolidated Statement of "
    f"Comprehensive Income - {AR2020_URL}\n"
    f"FY2019: Belmont Green Finance Limited Annual Report and Accounts 2019, Consolidated Statement of "
    f"Comprehensive Income - {AR2019_URL}\n"
    f"FY2018: taken from the FY2019 Annual Report's own FY2018 comparative column (same document as above) - "
    f"Belmont Green's originally-filed FY2018 Annual Report did present a Company-basis income statement, but "
    f"it is not used here (see basis note above).\n\n"
    "FY2019's own Annual Report has an internal, unreconciled ~£80k discrepancy between the Loss for the year it "
    "reports on this Consolidated Statement of Comprehensive Income (£(31,164)k) and the Loss for the year used "
    "on this workbook's own Statement of Changes in Equity and Cash Flow Statement sheets (£(31,084)k, per the "
    "same Annual Report's own Statement of Changes in Equity and cash flow note) - both figures are reproduced "
    "exactly as printed on their respective source statements rather than forced to agree.\n\n"
    "Presentation notes (not silently reconciled): FY2021's Group statement labels its operating-income subtotal "
    "\"Total income\" rather than FY2022-25's \"Net operating income\" - same position in the statement, different "
    "label, reproduced as printed. FY2025's own Statement of Comprehensive Income prints its final row as \"Total "
    "other comprehensive profit\" with a value of 12,699 - this is actually the year's Total comprehensive income "
    "(Profit after tax 13,097 less the 3 OCI items above it, -21-98-279=-398, gives exactly 12,699); the source's "
    "own row label is internally inconsistent (a subtotal, not \"other\" comprehensive income), so this row is "
    "relabelled \"Total comprehensive income for the year, net of tax\" here to match the other 4 years' own "
    "correctly-labelled totals - the £'000 value itself is reproduced exactly as printed, unchanged.\n\n"
    + STATEMENTS_ENTITY_NOTE
)

EQUITY_SOURCES = (
    "Sources - Vida Bank Limited's own Company (non-consolidated) Statement of Changes in Equity, £'000:\n"
    f"FY2021 boundary (1 Jan 2021 opening, FY2021 movements, 31 Dec 2021 closing): Belmont Green Finance Limited "
    f"Annual Report and Accounts 2021, p.150 - {AR2021_URL}\n"
    f"FY2022 boundary: Belmont Green Finance Limited Annual Report and Accounts 2023, p.184 (FY2022 comparative "
    f"rows) - {AR2023_URL}\n"
    f"FY2023 boundary: same document, p.184 - {AR2023_URL}\n"
    f"FY2024 boundary: Vida Bank Limited Annual Report and Accounts 2024, p.72 - {AR2024_URL}\n"
    f"FY2025 boundary: Vida Bank Limited Annual Report and Accounts 2025 (Company), p.54 - {AR2025_URL}\n"
    f"FY2018 boundary (1 Jan 2018 opening, FY2018 movements, 31 Dec 2018 closing): taken from the FY2019 Annual "
    f"Report's own restated FY2018 comparative rows (Company Statement of Changes in Equity) - {AR2019_URL}\n"
    f"FY2019 boundary: same FY2019 Annual Report, Company Statement of Changes in Equity - {AR2019_URL}\n"
    f"FY2020 boundary: Belmont Green Finance Limited Annual Report and Accounts 2020, Company Statement of "
    f"Changes in Equity - {AR2020_URL}\n\n"
    "Discrepancy flagged, not forced to tie: the FY2024 Annual Report's own opening balance at 1 January 2024 "
    "(share capital 204,463 / total equity 122,070) differs by £1k from the FY2023 Annual Report's own closing "
    "balance at 31 December 2023 (share capital 204,462 / total equity 122,069) - a genuine £1k rounding artefact "
    "between the two source documents, each reproduced exactly as its own report states. A similar £1k share-"
    "capital rounding artefact exists between the FY2020 Annual Report's own opening 1 January 2020 row (share "
    "capital 168,312) and the FY2019 Annual Report's own closing 31 December 2019 row (share capital 168,313), "
    "again reproduced exactly as each report states.\n\n"
    "Larger, unreconciled discrepancy flagged (not forced to tie): the FY2019 Annual Report's own 'Balance as at 1 "
    "January 2019' row (129,641 / (29,547) / 100,015) does not internally sum (129,641 - 29,547 = 100,094, not "
    "100,015 as printed) and its own 'At 31 December 2019' row (168,313 / (53,240) / 114,993) likewise differs by "
    "£80k from this workbook's own Balance Sheet sheet, which uses the same Annual Report's Company Statement of "
    "Financial Position total shareholders' equity of £115,073k for 31 December 2019 - both sets of figures are "
    "reproduced exactly as printed on their own source statement rather than corrected or blended.\n\n"
    "The FY2025 Statement of Changes in Equity's own \"Total comprehensive income\" subtotal row is omitted from "
    "this ladder: it prints running balances (not that year's movement) in its Retained earnings and Total "
    "columns - see the Profit & Loss sheet's own source note for the same issue on that sheet. Every individual "
    "movement row above it (Profit for the year, Deferred tax on Gilts, Fair value through OCI reserve, Amounts "
    "deferred to cash flow hedge reserve) is reproduced in full and the ladder ties exactly without it.\n\n"
    + STATEMENTS_ENTITY_NOTE
)

ASSET_QUALITY_SOURCES = (
    "Sources - Vida Bank Limited's own IFRS 9 stage disclosure (Note 13/14, \"Expected credit losses\"), £'000, "
    "on a Group/Consolidated basis (the only basis at which this note is disclosed in every source document; "
    "gross/net loan totals below therefore don't tie exactly to the Balance Sheet sheet's Company-basis \"Loans "
    "to customers\" line - a genuine basis difference, documented not blended):\n"
    f"FY2025/FY2024: Vida Bank Limited Annual Report and Accounts 2025, p.79-81 (Note 14, Expected credit "
    f"losses) - {AR2025_URL}\n"
    f"FY2023/FY2022: Belmont Green Finance Limited Annual Report and Accounts 2023, p.168-169 (Note 14, Expected "
    f"credit losses) - {AR2023_URL}\n"
    f"FY2021: Belmont Green Finance Limited Annual Report and Accounts 2021, p.132-133 (Note 13, Expected credit "
    f"losses) - {AR2021_URL}\n"
    f"FY2020/FY2019: Belmont Green Finance Limited Annual Report and Accounts 2020, Note 13 (Expected credit "
    f"losses) and Note 23 (Risk management - loans to customers by IFRS 9 stage, Low/High risk sub-bucketed within "
    f"Stage 1/Stage 2, summed here into the single Stage 1/Stage 2 rows used throughout this sheet) - {AR2020_URL}\n"
    f"FY2018: Belmont Green Finance Limited Annual Report and Accounts 2019, FY2018 comparative column of the "
    f"same Note 23-equivalent risk management table (Low/High risk sub-buckets summed the same way) - "
    f"{AR2019_URL}. Belmont Green's own originally-filed FY2018 Annual Report does not disclose an IFRS 9 stage "
    f"split at all (only £450k of loans sat on the Company balance sheet that year - see FY2018_RESTATEMENT_NOTE "
    f"on the Cash Flow Statement sheet), so the FY2019 Annual Report's restated comparative is the only source for "
    f"FY2018 on this sheet.\n\n"
    "NPL ratio = Stage 3 gross balance / Total gross balance. Coverage ratio = Stage 3 impairment provision / "
    "Stage 3 gross balance. Both derived, not separately disclosed by the Bank."
)


def rwa_not_disclosed_note():
    return (
        "No UK OV1 (RWA-by-risk-category) template, or equivalent RWA breakdown table, exists in either Pillar 3 "
        "Disclosures document (2025 or 2024) checked this session - both are short (9-page) documents covering "
        "only the KM1 Key Metrics table already used on the other Pillar 3 sheets. Confirmed non-disclosure, not "
        "an access gap. No Pillar 3 disclosure exists at all for FY2018-FY2023 (see ENTITY_NOTE on the Cash Flow "
        "Statement sheet)."
    )


# ---------------------------------------------------------------
# Sheet: Balance Sheet
# ---------------------------------------------------------------
bs_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and cash equivalents", {"FY2025": 254874, "FY2024": 143485, "FY2023": 17161, "FY2022": 14919, "FY2021": 13500, "FY2020": 18109, "FY2019": 4079, "FY2018": 5680}),
    ("DATA", "Total debt securities", {"FY2025": 819770, "FY2024": 34135}),
    ("DATA", "Debt securities - UK Government securities (FVOCI)", {"FY2025": 537441, "FY2024": 34135}),
    ("DATA", "Debt securities - Supranational bonds (FVOCI)", {"FY2025": 167080}),
    ("DATA", "Debt securities - Covered bonds (FVOCI)", {"FY2025": 115248}),
    ("DATA", "Loans to customers", {"FY2025": 2301831, "FY2024": 1866006, "FY2023": 1712271, "FY2022": 1761996, "FY2021": 1811577, "FY2020": 1635572, "FY2019": 1599800, "FY2018": 1197862}),
    ("DATA", "Derivative financial instruments", {"FY2025": 10198, "FY2024": 2123, "FY2022": 731}),
    ("DATA", "Other receivables", {"FY2025": 71715, "FY2024": 16412, "FY2023": 34000, "FY2022": 13982, "FY2021": 11399, "FY2020": 15207, "FY2019": 21901, "FY2018": 25813}),
    ("DATA", "Deferred taxation asset", {"FY2025": 15299, "FY2024": 13565, "FY2023": 13565, "FY2022": 13565, "FY2021": 12975, "FY2020": 11602, "FY2019": 10283, "FY2018": 6007}),
    ("DATA", "Investment in subsidiaries", {"FY2020": 9000, "FY2019": 9000, "FY2018": 9000}),
    ("DATA", "Property, plant and equipment", {"FY2025": 1343, "FY2024": 1551, "FY2023": 401, "FY2022": 965, "FY2021": 2407, "FY2020": 3795, "FY2019": 5334, "FY2018": 1249}),
    ("DATA", "Intangible assets", {"FY2025": 1316, "FY2024": 2190, "FY2023": 2704, "FY2022": 2837, "FY2021": 2408, "FY2020": 1117, "FY2019": 317, "FY2018": 261}),
    ("DATA", "Corporation tax", {"FY2022": 25}),
    ("TOTAL", "Total assets", {"FY2025": 3476346, "FY2024": 2079467, "FY2023": 1780102, "FY2022": 1809020, "FY2021": 1854266, "FY2020": 1694401, "FY2019": 1650714, "FY2018": 1245872}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Retail deposits", {"FY2025": 2425702, "FY2024": 173113}),
    ("DATA", "Amounts owed to credit institutions", {"FY2025": 40345, "FY2024": 74254, "FY2023": 44437, "FY2022": 15188, "FY2021": 15336}),
    ("DATA", "Deemed loan due to Group undertakings", {"FY2025": 767720, "FY2024": 1659540, "FY2023": 1544083, "FY2022": 1606178, "FY2021": 1690865, "FY2020": 1521161, "FY2019": 1484952, "FY2018": 1108999}),
    ("DATA", "Derivative financial liabilities", {"FY2025": 19403, "FY2024": 184, "FY2023": 4727}),
    ("DATA", "Other liabilities", {"FY2025": 44269, "FY2024": 7067, "FY2023": 64722, "FY2022": 56584, "FY2021": 21050, "FY2020": 48390, "FY2019": 50689, "FY2018": 36696}),
    ("DATA", "Provisions", {"FY2023": 64, "FY2022": 64, "FY2021": 374, "FY2020": 604}),
    ("DATA", "Corporation tax", {"FY2025": 1128, "FY2024": 229}),
    ("TOTAL", "Total liabilities", {"FY2025": 3298567, "FY2024": 1914387, "FY2023": 1658033, "FY2022": 1678014, "FY2021": 1727625, "FY2020": 1570155, "FY2019": 1535641, "FY2018": 1145695}),
    ("SECTION", "Shareholders' equity", {}),
    ("DATA", "Called up share capital", {"FY2025": 36156, "FY2024": 241039, "FY2023": 204462, "FY2022": 204462, "FY2021": 204462, "FY2020": 196162, "FY2019": 168313, "FY2018": 129642}),
    ("DATA", "Other reserves", {"FY2025": -398}),
    ("DATA", "Retained profit/(losses)", {"FY2025": 142021, "FY2024": -75959, "FY2023": -82393, "FY2022": -73456, "FY2021": -77821, "FY2020": -71916, "FY2019": -53240, "FY2018": -29464}),
    ("TOTAL", "Total shareholders' equity", {"FY2025": 177779, "FY2024": 165080, "FY2023": 122069, "FY2022": 131006, "FY2021": 126641, "FY2020": 124246, "FY2019": 115073, "FY2018": 100178}),
    ("TOTAL", "Total liabilities and equity", {"FY2025": 3476346, "FY2024": 2079467, "FY2023": 1780102, "FY2022": 1809020, "FY2021": 1854266, "FY2020": 1694401, "FY2019": 1650714, "FY2018": 1245872}),
]

bw.add_balance_sheet_sheet(
    title="Vida Bank Limited — Company Statement of Financial Position",
    subtitle="Company (non-consolidated) basis, £'000.",
    rows=bs_rows,
    sources_text=BALANCE_SHEET_SOURCES,
    first_col_width=60,
    source_height=180,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Sheet: Profit & Loss
# ---------------------------------------------------------------
pl_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest income and similar income", {"FY2025": 171518, "FY2024": 121718, "FY2023": 144373, "FY2022": 99941, "FY2021": 68551, "FY2020": 61142, "FY2019": 49649, "FY2018": 42042}),
    ("DATA", "Interest expense and similar charges", {"FY2025": -124229, "FY2024": -87898, "FY2023": -110660, "FY2022": -57037, "FY2021": -34046, "FY2020": -37205, "FY2019": -47030, "FY2018": -24573}),
    ("TOTAL", "Net interest income", {"FY2025": 47289, "FY2024": 33820, "FY2023": 33713, "FY2022": 42904, "FY2021": 34505, "FY2020": 23937, "FY2019": 2619, "FY2018": 17469}),
    ("DATA", "Other operating income/(expense)", {"FY2025": 7035, "FY2024": 1158, "FY2023": 920, "FY2022": -6174, "FY2021": 987, "FY2020": 779}),
    ("DATA", "Net fair value gain/(loss) on financial instruments", {"FY2025": 3331, "FY2024": 6045, "FY2023": 3903, "FY2022": -706, "FY2021": -1404, "FY2020": -50, "FY2019": -3900, "FY2018": -473}),
    ("TOTAL", "Net operating income", {"FY2025": 57655, "FY2024": 41023, "FY2023": 38536, "FY2022": 36024, "FY2021": 34088, "FY2020": 24666, "FY2019": -1281, "FY2018": 16996}),
    ("TOTAL", "Administrative expenses", {"FY2025": -42450, "FY2024": -34231, "FY2023": -32438, "FY2022": -35502, "FY2021": -30932, "FY2020": -28043, "FY2019": -31642, "FY2018": -25132}),
    ("TOTAL", "Operating profit before impairment", {"FY2025": 15205, "FY2024": 6792, "FY2023": 6098, "FY2022": 522, "FY2021": 3156, "FY2020": -3377, "FY2019": -32923, "FY2018": -8136}),
    ("DATA", "Provisions", {"FY2023": 0, "FY2022": 310, "FY2021": 223, "FY2020": -350}),
    ("DATA", "Impairment (losses)/releases", {"FY2025": -2736, "FY2024": -128, "FY2023": -55, "FY2022": 543, "FY2021": -725, "FY2020": -3371, "FY2019": -2402, "FY2018": -1105}),
    ("TOTAL", "Profit before taxation", {"FY2025": 12469, "FY2024": 6664, "FY2023": 6043, "FY2022": 1375, "FY2021": 2654, "FY2020": -7098, "FY2019": -35325, "FY2018": -9241}),
    ("DATA", "Tax credit/(charge) for the year", {"FY2025": 628, "FY2024": -230, "FY2023": 25, "FY2022": 609, "FY2021": 2005, "FY2020": 762, "FY2019": 4161, "FY2018": 222}),
    ("TOTAL", "Profit for the year", {"FY2025": 13097, "FY2024": 6434, "FY2023": 6068, "FY2022": 1984, "FY2021": 4659, "FY2020": -6336, "FY2019": -31164, "FY2018": -9019}),
    ("SECTION", "Other comprehensive income", {}),
    ("DATA", "Cash flow hedge reserve (losses)/gains", {"FY2025": -21, "FY2024": 0, "FY2023": -10468, "FY2022": 16864, "FY2021": 0}),
    ("DATA", "Tax on items in other comprehensive income", {"FY2025": -98}),
    ("DATA", "Fair value through OCI reserve", {"FY2025": -279}),
    ("TOTAL", "Total comprehensive income/(loss) for the year, net of tax", {"FY2025": 12699, "FY2024": 6434, "FY2023": -4400, "FY2022": 18848, "FY2021": 4659, "FY2020": -6336, "FY2019": -31164, "FY2018": -9019}),
]

bw.add_income_statement_sheet(
    title="Vida Bank Limited — Statement of Comprehensive Income",
    subtitle="FY2025/FY2024: Company basis. FY2023-FY2018: Group/Consolidated basis (Company P&L exempted under s.408 in every year except FY2018's own Annual Report, not used here for consistency - see source note). £'000.",
    rows=pl_rows,
    sources_text=INCOME_STATEMENT_SOURCES,
    first_col_width=64,
    source_height=260,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Sheet: Statement of Changes in Equity
# ---------------------------------------------------------------
equity_headers = ["Called up share capital", "Retained earnings", "Other reserves", "Total"]
equity_rows = [
    ("TOTAL", "Balance at 1 January 2018", (84860, -28014, None, 56846)),
    ("DATA", "Share issuance", (44782, None, None, 44782)),
    ("DATA", "Loss for the year (restated)", (None, -1451, None, -1451)),
    ("TOTAL", "Balance at 31 December 2018", (129642, -29464, None, 100177)),
    ("DATA", "Adjustment on initial application of IFRS 16", (None, -162, None, -162)),
    ("TOTAL", "Balance at 1 January 2019 (per FY2019 Annual Report - see source note)", (129641, -29547, None, 100015)),
    ("DATA", "Share issuance", (38671, None, None, 38671)),
    ("DATA", "Loss for the year", (None, -23693, None, -23693)),
    ("TOTAL", "Balance at 31 December 2019 (per FY2019 Annual Report - see source note)", (168313, -53240, None, 114993)),
    ("TOTAL", "Balance at 1 January 2020 (per FY2020 Annual Report - see source note)", (168312, -53240, None, 115072)),
    ("DATA", "Share issuance", (27850, None, None, 27850)),
    ("DATA", "Loss for the year", (None, -18676, None, -18676)),
    ("TOTAL", "Balance at 31 December 2020", (196162, -71916, None, 124246)),
    ("TOTAL", "Balance at 1 January 2021", (196162, -71916, None, 124246)),
    ("DATA", "Share issuance", (8300, None, None, 8300)),
    ("DATA", "Loss for the year", (None, -5905, None, -5905)),
    ("TOTAL", "Balance at 31 December 2021", (204462, -77821, None, 126641)),
    ("DATA", "Profit for the year", (None, 4365, None, 4365)),
    ("TOTAL", "Balance at 31 December 2022", (204462, -73456, None, 131006)),
    ("DATA", "Loss for the year", (None, -8937, None, -8937)),
    ("TOTAL", "Balance at 31 December 2023", (204462, -82393, None, 122069)),
    ("TOTAL", "Balance at 1 January 2024 (per FY2024 Annual Report - see source note)", (204463, -82393, None, 122070)),
    ("DATA", "Profit for the year", (None, 6434, None, 6434)),
    ("DATA", "Share issuance", (36576, None, None, 36576)),
    ("TOTAL", "Balance at 31 December 2024", (241039, -75959, None, 165080)),
    ("DATA", "Profit for the year", (None, 13097, None, 13097)),
    ("DATA", "Deferred tax on Gilts", (None, None, -98, -98)),
    ("DATA", "Fair value through OCI reserve", (None, None, -279, -279)),
    ("DATA", "Amounts deferred to cash flow hedge reserve, net of tax", (None, None, -21, -21)),
    ("DATA", "Share capital reallocation", (-204883, 204883, None, 0)),
    ("TOTAL", "Balance at 31 December 2025", (36156, 142021, -398, 177779)),
]

bw.add_equity_changes_sheet(
    title="Vida Bank Limited — Company Statement of Changes in Equity",
    subtitle="Company (non-consolidated) basis, £'000. Chronological, oldest to newest.",
    headers=equity_headers,
    rows=equity_rows,
    sources_text=EQUITY_SOURCES,
    first_col_width=56,
    source_height=260,
)

# ---------------------------------------------------------------
# Sheet 1: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Operating activities", {}),
    ("TOTAL", "Net cash flows from/(used in) operating activities", {"FY2025": 1766849, "FY2024": 70662, "FY2023": 65493, "FY2022": 35347, "FY2021": -179449, "FY2020": -47723, "FY2019": -423882, "FY2018": -763195}),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Purchase of property, plant and equipment", {"FY2025": -92, "FY2024": -57, "FY2023": -24, "FY2022": -131, "FY2021": -190, "FY2020": -119, "FY2019": -4537, "FY2018": -1319}),
    ("DATA", "Expenditure on software development", {"FY2025": -12, "FY2024": -351, "FY2023": -674, "FY2022": -1040, "FY2021": -1567, "FY2020": -994, "FY2019": -311, "FY2018": 0}),
    ("TOTAL", "Net cash flows from/(used in) investing activities", {"FY2025": -104, "FY2024": -408, "FY2023": -698, "FY2022": -1171, "FY2021": -1757, "FY2020": -1113, "FY2019": -4848, "FY2018": -1319}),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Proceeds from shares issued", {"FY2022": "-", "FY2021": 8300, "FY2020": 27850, "FY2019": 38671, "FY2018": 44782}),
    ("DATA", "Movement of deemed loans due to Group undertakings", {"FY2025": -904243, "FY2024": 115457, "FY2023": -62096, "FY2022": -31392, "FY2021": 169705, "FY2020": 36209, "FY2019": 392814, "FY2018": 723148}),
    ("DATA", "Loan to/from subsidiary undertakings", {"FY2019": -4356, "FY2018": -5804}),
    ("DATA", "Repayment of loans", {"FY2024": -25000}),
    ("DATA", "Issuance of Tier 2 subordinated liabilities", {"FY2025": 35000}),
    ("DATA", "Repayment of lease liabilities", {"FY2025": -479, "FY2024": -225, "FY2023": -446, "FY2022": -1365, "FY2021": -1407, "FY2020": -1194}),
    ("DATA", "Movement in debt securities", {"FY2025": -785634, "FY2024": -34135}),
    ("DATA", "Other movements", {"FY2025": 0, "FY2024": -27, "FY2023": -12}),
    ("TOTAL", "Net cash flows (used in)/generated from financing activities", {"FY2025": -1655356, "FY2024": 56070, "FY2023": -62554, "FY2022": -32755, "FY2021": 176598, "FY2020": 62865, "FY2019": 427129, "FY2018": 762126}),
    ("TOTAL", "Net increase/(decrease) in cash and cash equivalents", {"FY2025": 111389, "FY2024": 126324, "FY2023": 2241, "FY2022": 1419, "FY2021": -4608, "FY2020": 14029, "FY2019": -1601, "FY2018": -2389}),
    ("DATA", "Cash and cash equivalents at the beginning of the year", {"FY2025": 143485, "FY2024": 17161, "FY2023": 14920, "FY2022": 13500, "FY2021": 18108, "FY2020": 4079, "FY2019": 5680, "FY2018": 8069}),
    ("TOTAL", "Cash and cash equivalents at the end of the year", {"FY2025": 254874, "FY2024": 143485, "FY2023": 17161, "FY2022": 14919, "FY2021": 13500, "FY2020": 18108, "FY2019": 4079, "FY2018": 5680}),
]

bw.add_cash_flow_sheet(
    title="Vida Bank Limited — Company Cash Flow Statement",
    subtitle="Company (non-consolidated) basis, £'000. Every year FY2018-FY2025 is populated; see the source "
              "note for FY2022's own two documented divergences and the FY2018 restatement.",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=68,
    source_height=280,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Sheet: Asset Quality
# ---------------------------------------------------------------
aq_rows = [
    ("SECTION", "Gross loans to customers by IFRS 9 stage", {}),
    ("DATA", "Stage 1 (performing)", {"FY2025": 1915462, "FY2024": 1463371, "FY2023": 1254493, "FY2022": 1041635, "FY2021": 1124656, "FY2020": 1150485, "FY2019": 1411656, "FY2018": 1080264}),
    ("DATA", "Stage 2 (underperforming)", {"FY2025": 321347, "FY2024": 330053, "FY2023": 392712, "FY2022": 662983, "FY2021": 643597, "FY2020": 455349, "FY2019": 184957, "FY2018": 109901}),
    ("DATA", "Stage 3 (non-performing)", {"FY2025": 65403, "FY2024": 63782, "FY2023": 51849, "FY2022": 45129, "FY2021": 44090, "FY2020": 35694, "FY2019": 7654, "FY2018": 2354}),
    ("TOTAL", "Total gross loans to customers", {"FY2025": 2302212, "FY2024": 1857206, "FY2023": 1699054, "FY2022": 1749747, "FY2021": 1812343, "FY2020": 1641528, "FY2019": 1604267, "FY2018": 1192519}),
    ("SECTION", "Impairment provision (ECL) by IFRS 9 stage", {}),
    ("DATA", "Stage 1 provision", {"FY2025": 1671, "FY2024": 1053, "FY2023": 1105, "FY2022": 647, "FY2021": 1217, "FY2020": 898, "FY2019": 661, "FY2018": 549}),
    ("DATA", "Stage 2 provision", {"FY2025": 1555, "FY2024": 1341, "FY2023": 1885, "FY2022": 3443, "FY2021": 3889, "FY2020": 3834, "FY2019": 1550, "FY2018": 966}),
    ("DATA", "Stage 3 provision", {"FY2025": 3865, "FY2024": 2480, "FY2023": 2599, "FY2022": 1835, "FY2021": 2541, "FY2020": 2739, "FY2019": 1889, "FY2018": 183}),
    ("TOTAL", "Total impairment provision", {"FY2025": 7091, "FY2024": 4874, "FY2023": 5589, "FY2022": 5925, "FY2021": 7647, "FY2020": 7471, "FY2019": 4100, "FY2018": 1698}),
    ("SECTION", "Derived ratios", {}),
    ("DATA", "NPL ratio (Stage 3 / Total gross loans)", {"FY2025": "2.84%", "FY2024": "3.43%", "FY2023": "3.05%", "FY2022": "2.58%", "FY2021": "2.43%", "FY2020": "2.17%", "FY2019": "0.48%", "FY2018": "0.20%"}),
    ("DATA", "Stage 3 coverage ratio (Stage 3 provision / Stage 3 gross)", {"FY2025": "5.91%", "FY2024": "3.89%", "FY2023": "5.01%", "FY2022": "4.07%", "FY2021": "5.77%", "FY2020": "7.67%", "FY2019": "24.68%", "FY2018": "7.77%"}),
]

bw.add_asset_quality_sheet(
    title="Vida Bank Limited — Asset Quality",
    subtitle="Group/Consolidated basis (see source note), £'000.",
    rows=aq_rows,
    sources_text=ASSET_QUALITY_SOURCES,
    first_col_width=64,
    source_height=200,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
# FY2018-FY2023 predate the 19 November 2024 banking licence, so no Pillar 3 metric
# can ever exist for them. They were left blank until 2026-09-15, which made them
# indistinguishable from years nobody had researched yet - a cross-bank coverage audit
# counted all 30 of them as chaseable gaps. Marking them explicitly matches what the
# RWA Breakdown sheet on this same workbook already does, and build_afin_bank.py's
# handling of the identical situation.
PRE_LICENCE_YEARS = ["FY2023", "FY2022", "FY2021", "FY2020", "FY2019", "FY2018"]


def metric(name, unit, rows_data, note=None):
    rows_data = [(label, {**{y: "Not applicable" for y in PRE_LICENCE_YEARS}, **values})
                 for label, values in rows_data]
    bw.add_metric_sheet(name, f"Vida Group Holdings basis, {unit}" if unit else "Vida Group Holdings basis",
                         rows_data, p3_sources(), note=note, first_col_width=48, source_height=130)


# ---------------------------------------------------------------
# Sheet: KM1 Key Metrics (must be added BEFORE the first metric sheet so it
# lands immediately after Asset Quality and immediately before CET1 Capital)
# ---------------------------------------------------------------
P3_HY2026_URL = "https://www.vidabank.co.uk/media/g1vnsxxu/pillar-3-disclosures-30-june-2026.pdf"

KM1_SOURCES = (
    "Sources - Vida's own published UK KM1 'Key metrics' table, reproduced whole in the bank's own row order, "
    "row labels and printed precision. Entity/basis: Vida Group Holdings Limited (FY2024 edition) / Vida Group "
    "Holdings plc (FY2025 edition) CONSOLIDATED - the CRR consolidation entity, with Vida Bank Limited as its "
    "principal regulated subsidiary. Both editions state 'Regulatory ratios are presented on a Group-basis "
    "only', so no Vida-Bank-Limited-solo KM1 exists to prefer; this is the same basis every other Pillar 3 "
    "sheet in this workbook uses (see the metric sheets' own BASIS DETERMINATION note).\n"
    f"FY2025: Vida Group Holdings Limited Pillar 3 Disclosures 31 December 2025, section 3.1 'Key Metrics', "
    f"PRINTED PAGE 5 (the page's own footer reads '5|Page') - {P3_2025_URL}\n"
    f"FY2024: Vida Group Holdings Limited Pillar 3 Disclosures 31 December 2024, section 3.1 'Key Metrics', "
    f"PRINTED PAGE 5 (footer '5|Page') - {P3_2024_URL}\n"
    "Each year is taken from its OWN edition. The FY2025 edition also prints a 31 Dec 2024 comparative column "
    "and it agrees with the FY2024 edition digit-for-digit on every one of the 23 rows, so nothing here depends "
    "on which edition a FY2024 figure came from.\n\n"
    "COLUMN ORDER: both editions print the OLDER year on the LEFT (the FY2025 edition's header block reads "
    "'31 Dec 2024   31 Dec 2025'). This sheet keeps the workbook's standard most-recent-first column order, "
    "which reorders columns but not rows - no row, label, figure or precision is altered.\n\n"
    "THE TABLE IS UNNUMBERED, AND IT IS STILL THE TEMPLATE. Vida prints no template row numbers at all (no "
    "'1', no 'UK 7a'), but the table carries the UK KM1 row set in template order - available own funds, "
    "risk-weighted exposure amount, the three capital ratios, the additional own-funds (SREP) requirement, the "
    "combined buffer build-up, leverage, LCR and NSFR - and the bank's own sentence above it names it: 'The key "
    "metrics table (KM1) covering capital, leverage and liquidity is set out below.' Both editions are reduced-"
    "scope Article 433b disclosures ('small and non-complex institution', UK CRR Article 4(145)), and both say "
    "'Specific rows and columns in the tables prescribed by the PRA have been omitted where these are not "
    "applicable to the Group' - so the shorter row set is a permitted reduction of the prescribed template, not "
    "a different table and not an omission.\n\n"
    "NO MISSING-VALUE GLYPHS: neither edition prints a dash, an 'n/a' or a zero anywhere in this table. Every "
    "row the bank printed carries a figure in every column it printed.\n\n"
    "UNITS: the bank declares £'000 on its own block captions ('Available own funds (£’000)', 'Risk-weighted "
    "exposure (£’000)') and again on most individual rows. Each amount row below carries its own '(£'000)' so "
    "the unit never has to be inferred from how far a lookup walks. The bank's own table mixes a typewriter "
    "apostrophe and a typographic one for the same unit within a single page; the typewriter form is used "
    "throughout here, which is a glyph choice in an annotation and changes no wording and no figure.\n\n"
    "FY2018-FY2023 ARE BLANK BECAUSE NO PILLAR 3 DISCLOSURE OF ANY KIND EXISTS FOR THEM, on any basis, in any "
    "edition. The entity was not PRA-authorised as a deposit-taker until 19 November 2024, so no Pillar 3 "
    "obligation could attach to any earlier year; FY2018-FY2020 it was FCA-regulated only. FY2024 is the first "
    "year for which any Pillar 3 document exists, and no later edition prints a pre-FY2024 comparative that "
    "could fill those columns. This is a structural pre-authorisation absence, not an exemption - see the "
    "ENTITY_NOTE on the Cash Flow Statement sheet and the SDDT date-fit note on the metric sheets, which "
    "records that Vida's Rule 3.1 SDDT modification began 3 April 2026 and therefore explains none of these "
    "blanks.\n\n"
    "LATEST-EDITION CHECK, 2026-09-17: checked Vida's own site (www.vidabank.co.uk -> About Vida Bank -> "
    "Investors -> Debt Investors), not a cached citation list. The newest ANNUAL Pillar 3 is the 31 December "
    "2025 edition used above, and the newest Annual Report is the 2025 Annual Report and Accounts already used "
    "throughout this workbook - so no year is missing. The site additionally carries an INTERIM Pillar 3 as at "
    f"30 June 2026 ({P3_HY2026_URL}), published alongside a 30 June 2026 Interim Report. It falls outside this "
    "workbook's financial years (Vida's year-end is 31 December) and so adds no column, but its 31 Dec 2025 "
    "comparative was read as an independent second transcription of the whole FY2025 column.\n\n"
    "WHAT THAT SECOND OPINION FOUND - RECORDED, NOT RECONCILED. The interim edition reproduces the FY2025 "
    "capital and leverage block exactly: CET1 168,319, Tier 1 168,319, Total capital 202,429, RWEA 1,105,780, "
    "ratios 15.2% / 15.2% / 18.3%, leverage exposure 3,440,332 and leverage ratio 4.9%. It differs in two "
    "places, both of which are the interim edition changing how it MEASURES a row rather than correcting a "
    "figure, so the FY2025 column below stays exactly as Vida's own FY2025 edition printed it. (1) The SREP "
    "block is presented differently: the FY2025 edition prints one combined 'Additional own funds requirements "
    "(%)' of 1.2% and a 9.2% total, while the interim edition splits the same requirement into 'Additional "
    "CET1 SREP requirements 0.66% / Additional AT1 SREP requirements 0.22% / Additional T2 SREP requirements "
    "0.30%' with a 9.18% total - the components sum to 1.18%, i.e. the same requirement shown to two decimals "
    "instead of one. (2) The LIQUIDITY rows are on a different averaging window. The interim edition footnotes "
    "its LCR as 'the simple average of month end observations over the preceding 12 months' and its NSFR as "
    "'the simple average of quarter end observations over the preceding 4 quarter ends', and on that basis "
    "restates 31 Dec 2025 to HQLA 612,552 / outflows 330,304 / inflows 101,370 / net outflows 252,077 / LCR "
    "528%, and NSFR 2,327,088 / 1,646,865 / 142%, against the 1,073,005 / 747,252 / 77,815 / 669,438 / 163% "
    "and 2,377,496 / 1,719,626 / 138% that the FY2025 annual edition printed for the same date. Two printings "
    "of one date on two bases is a documented divergence, not a transcription error in either; each year's own "
    "edition governs its own column."
)

km1_rows = [
    ("SECTION", "Available own funds (£'000)", {}),
    ("DATA", "Common Equity Tier 1 (CET1) capital (£'000)", {"FY2025": 168319, "FY2024": 160316}),
    ("DATA", "Tier 1 capital (£'000)", {"FY2025": 168319, "FY2024": 160316}),
    ("DATA", "Total capital (£'000)", {"FY2025": 202429, "FY2024": 160316}),
    ("SECTION", "Risk-weighted exposure (£'000)", {}),
    ("DATA", "Total risk-weighted exposure amount (£'000)", {"FY2025": 1105780, "FY2024": 986809}),
    ("SECTION", "Capital ratios", {}),
    ("DATA", "Common Equity Tier 1 ratio (%)", {"FY2025": "15.2%", "FY2024": "16.2%"}),
    ("DATA", "Tier 1 ratio (%)", {"FY2025": "15.2%", "FY2024": "16.2%"}),
    ("DATA", "Total capital ratio (%)", {"FY2025": "18.3%", "FY2024": "16.2%"}),
    ("SECTION", "Additional own funds requirements", {}),
    ("DATA", "Additional own funds requirements (%)", {"FY2025": "1.2%", "FY2024": "1.2%"}),
    ("DATA", "Total own funds requirements (%)", {"FY2025": "9.2%", "FY2024": "9.2%"}),
    ("SECTION", "Combined buffer requirement", {}),
    ("DATA", "Capital conservation buffer (%)", {"FY2025": "2.5%", "FY2024": "2.5%"}),
    ("DATA", "Institution specific countercyclical capital buffer (%)", {"FY2025": "1.9%", "FY2024": "1.9%"}),
    ("DATA", "Combined buffer requirement (%)", {"FY2025": "4.4%", "FY2024": "4.4%"}),
    ("DATA", "Overall capital requirements (%)", {"FY2025": "13.6%", "FY2024": "13.6%"}),
    ("SECTION", "Leverage ratio", {}),
    ("DATA", "Total exposure measure excluding claims on central banks (£'000)", {"FY2025": 3440332, "FY2024": 2331835}),
    ("DATA", "Leverage ratio excluding claims on central banks (%)", {"FY2025": "4.9%", "FY2024": "6.9%"}),
    ("SECTION", "Liquidity coverage ratio", {}),
    ("DATA", "Total high-quality liquid assets (HQLA) (weighted value - average) (£'000)", {"FY2025": 1073005, "FY2024": 167705}),
    ("DATA", "Cash outflows - total weighted value (£'000)", {"FY2025": 747252, "FY2024": 64182}),
    ("DATA", "Cash inflows - total weighted value (£'000)", {"FY2025": 77815, "FY2024": 205580}),
    ("DATA", "Total net cash outflows (adjusted value) (£'000)", {"FY2025": 669438, "FY2024": 16046}),
    ("DATA", "Liquidity coverage ratio (%)", {"FY2025": "163%", "FY2024": "1,045%"}),
    ("SECTION", "Net stable funding ratio", {}),
    ("DATA", "Total available stable funding (£'000)", {"FY2025": 2377496, "FY2024": 2016146}),
    ("DATA", "Total required stable funding (£'000)", {"FY2025": 1719626, "FY2024": 1830180}),
    ("DATA", "Net stable funding ratio (%)", {"FY2025": "138%", "FY2024": "110%"}),
]

bw.add_km1_sheet(
    title="Vida Bank Limited — KM1 Key Metrics",
    subtitle="Vida Group Holdings (CRR consolidation entity) basis - the bank's own published UK KM1 table, "
             "reproduced whole in its own row order, labels and precision. The bank prints no template row "
             "numbers; amounts £'000, ratios as printed. FY2018-FY2023 are blank because no Pillar 3 "
             "disclosure of any kind exists for them (pre-authorisation) - see source note.",
    rows=km1_rows,
    sources_text=KM1_SOURCES,
    first_col_width=72,
    source_height=560,
    years=YEARS,
)

metric("CET1 Capital", "£'000", [("Common Equity Tier 1 (CET1) capital", {"FY2025": 168319, "FY2024": 160316})])
metric("CET1 Ratio", "% of RWA", [("Common Equity Tier 1 (CET1) ratio", {"FY2025": "15.2%", "FY2024": "16.2%"})])
metric("Tier 1 Capital", "£'000", [("Tier 1 capital", {"FY2025": 168319, "FY2024": 160316})],
       note="Equal to CET1 capital in both years - Vida has no Additional Tier 1 (AT1) instruments.")
metric("Tier 1 Ratio", "% of RWA", [("Tier 1 ratio", {"FY2025": "15.2%", "FY2024": "16.2%"})])
metric("Total Capital", "£'000", [("Total capital", {"FY2025": 202429, "FY2024": 160316})],
       note="FY2025 total capital exceeds Tier 1 capital because the Group issued £35m of qualifying Tier 2 capital "
            "during the year to support planned balance sheet expansion; FY2024 had no Tier 2 capital.")
metric("Total Capital Ratio", "% of RWA", [("Total capital ratio", {"FY2025": "18.3%", "FY2024": "16.2%"})])
metric("Total RWAs", "£'000", [("Total risk-weighted exposure amount", {"FY2025": 1105780, "FY2024": 986809})])
bw.add_rwa_breakdown_sheet(
    title="Vida Bank Limited — RWA Breakdown",
    subtitle="Vida Group Holdings (Group/consolidated) basis, £'000. Table (OV1) - RWEAs by risk type, as "
             "disclosed. FY2018-FY2023: no Pillar 3 disclosure exists at all (see ENTITY_NOTE).",
    rows=[
        ("DATA", "Credit risk (excluding CCR)", {"FY2025": 936924, "FY2024": 766886}),
        ("DATA", "Counterparty credit risk (CCR), of which credit valuation adjustment (CVA)", {"FY2025": 83044, "FY2024": 155027}),
        ("DATA", "Securitisation exposures in the non-trading book (after the cap)", {"FY2025": 6391, "FY2024": 0}),
        ("DATA", "Operational risk", {"FY2025": 79420, "FY2024": 64896}),
        ("TOTAL", "Total risk weighted exposure amount (Table OV1)", {"FY2025": 1105779, "FY2024": 986809}),
        ("SECTION", "Not applicable - entity was not a PRA-authorised bank", {}),
        ("DATA", "Not applicable (no banking licence held in these years)", {
            "FY2023": "Not applicable",
            "FY2022": "Not applicable",
            "FY2021": "Not applicable",
            "FY2020": "Not applicable",
            "FY2019": "Not applicable",
            "FY2018": "Not applicable",
        }),
    ],
    sources_text=(
        "Sources - Vida Group Holdings Limited/plc Pillar 3 disclosures, Table (OV1) 'RWEAs and total own funds "
        "requirements by risk type', £'000, as disclosed (DIRECTLY DISCLOSED, not derived):\n"
        f"FY2025 & FY2024: Vida Group Holdings plc Pillar 3 Disclosures 2025, section 3.2 'Risk-Weighted "
        f"Exposures', Table (OV1), p.6 - {P3_2025_URL}. FY2024's category rows sum exactly to that table's own "
        f"stated Total (986,809), matching the Total RWAs sheet's FY2024 figure exactly. FY2025's category rows "
        f"sum to 1,105,779 - £1k below the table's own stated Total (1,105,780) and the Total RWAs sheet's own "
        f"FY2025 figure - a one £'000 rounding artifact in the source table itself (each row independently "
        f"rounded to the nearest £'000 before summing), not a transcription error here; the TOTAL row above "
        f"shows the reconciling sum of the category rows, not the source's stated Total, per this project's "
        f"convention of the category breakdown always ticking to its own components.\n\n"
        "This table was not identified in an earlier review of these documents (which found only the KM1 Key "
        "Metrics table used on the other Pillar 3 sheets) - a 2026-09-08 re-check located it in section 3.2 of "
        "the FY2025 report (which also carries the FY2024 comparative column, so the standalone FY2024 report "
        "did not need separately re-checking for this sheet).\n\n"
        "FY2018-FY2023: no Pillar 3 disclosure exists at all for any year before FY2024 (Pillar 3 only applies "
        "once the entity holds a banking licence, obtained 19 November 2024) - see ENTITY_NOTE on the Cash Flow "
        "Statement sheet.\n\n"
        "2026-09-15: those pre-licence years are now marked explicitly as 'Not applicable' in the rows above, "
        "rather than being left as empty cells. They were previously blank, which made them indistinguishable "
        "from a bank that simply has not been researched yet - an audit of RWA Breakdown coverage counted them "
        "as open, chaseable gaps when in fact no document can ever exist for them. This follows the same "
        "convention already used in build_afin_bank.py for the identical situation. Corroborating evidence for "
        "the licence date: Companies House (company 09837692) shows the entity's first full bank accounts made "
        "up to 31 December 2024, and FY2024 is the first year for which any Pillar 3 disclosure of any kind "
        "exists."
    ),
    first_col_width=68,
    source_height=200,
    unit_suffix=" (£'000)",
)
metric(
    "Leverage Ratio", "£'000 / %",
    [
        ("Total exposure measure excluding claims on central banks", {"FY2025": 3440332, "FY2024": 2331835}),
        ("Leverage ratio excluding claims on central banks (%)", {"FY2025": "4.9%", "FY2024": "6.9%"}),
    ],
)
metric(
    "LCR", "£'000 / %",
    [
        ("Total high-quality liquid assets (HQLA), weighted value (average)", {"FY2025": 1073005, "FY2024": 167705}),
        ("Total net cash outflows, adjusted value", {"FY2025": 669438, "FY2024": 16046}),
        ("Liquidity Coverage Ratio (%)", {"FY2025": "163%", "FY2024": "1,045%"}),
    ],
    note="FY2024's very high LCR (1,045%) reflects a build-up of liquid assets immediately following PRA "
         "authorisation on 19 November 2024, per the Group's own Pillar 3 commentary.",
)
metric(
    "NSFR", "£'000 / %",
    [
        ("Total available stable funding", {"FY2025": 2377496, "FY2024": 2016146}),
        ("Total required stable funding", {"FY2025": 1719626, "FY2024": 1830180}),
        ("Net Stable Funding Ratio (%)", {"FY2025": "138%", "FY2024": "110%"}),
    ],
)
metric("MREL Ratio", None,
       [("MREL ratio", {y: "Not disclosed" for y in YEARS if y not in PRE_LICENCE_YEARS})],
       note="FY2025/FY2024: no MREL disclosure (numeric or qualitative) found in either Pillar 3 report - Vida is a "
            "small, recently-authorised bank and does not appear to be within scope of an MREL-above-minimum-capital "
            "requirement based on its own disclosures. FY2018-FY2023 read 'Not applicable' rather than 'Not "
            "disclosed' because the entity held no banking licence in those years, so no MREL requirement could "
            "attach to it in the first place - the two are different findings and were previously conflated here.")

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets", {"FY2025": 3476346, "FY2024": 2079467, "FY2023": 1780102, "FY2022": 1809020, "FY2021": 1854266, "FY2020": 1694401, "FY2019": 1650714, "FY2018": 1245872}),
        ("Loans to customers", {"FY2025": 2301831, "FY2024": 1866006, "FY2023": 1712271, "FY2022": 1761996, "FY2021": 1811577, "FY2020": 1635572, "FY2019": 1599800, "FY2018": 1197862}),
        ("Retail deposits", {"FY2025": 2425702, "FY2024": 173113}),
        ("Total shareholders' equity", {"FY2025": 177779, "FY2024": 165080, "FY2023": 122069, "FY2022": 131006, "FY2021": 126641, "FY2020": 124246, "FY2019": 115073, "FY2018": 100178}),
    ],
    balance_sheet_unit="£'000",
    income_statement_totals=[
        ("Net operating income", {"FY2025": 57655, "FY2024": 41023, "FY2023": 38536, "FY2022": 36024, "FY2021": 34088, "FY2020": 24666, "FY2019": -1281, "FY2018": 16996}),
        ("Administrative expenses", {"FY2025": -42450, "FY2024": -34231, "FY2023": -32438, "FY2022": -35502, "FY2021": -30932, "FY2020": -28043, "FY2019": -31642, "FY2018": -25132}),
        ("Profit for the year", {"FY2025": 13097, "FY2024": 6434, "FY2023": 6068, "FY2022": 1984, "FY2021": 4659, "FY2020": -6336, "FY2019": -31164, "FY2018": -9019}),
    ],
    income_statement_unit="£'000",
    equity_changes_totals=[
        ("Opening equity", {"FY2025": 165080, "FY2024": 122070, "FY2023": 131006, "FY2022": 126641, "FY2021": 124246, "FY2020": 115072, "FY2019": 100015, "FY2018": 56846}),
        ("Total comprehensive income/(loss) for the year", {"FY2025": 12699, "FY2024": 6434, "FY2023": -8937, "FY2022": 4365, "FY2021": -5905, "FY2020": -18676, "FY2019": -23693, "FY2018": -1451}),
        ("Other equity movements, net", {"FY2025": 0, "FY2024": 36576, "FY2023": 0, "FY2022": 0, "FY2021": 8300, "FY2020": 27850, "FY2019": 38671, "FY2018": 44782}),
        ("Closing equity", {"FY2025": 177779, "FY2024": 165080, "FY2023": 122069, "FY2022": 131006, "FY2021": 126641, "FY2020": 124246, "FY2019": 114993, "FY2018": 100177}),
    ],
    equity_changes_unit="£'000",
    cash_flow_totals=[
        ("Net cash from/(used in) operating activities", {"FY2025": 1766849, "FY2024": 70662, "FY2023": 65493, "FY2021": -179449, "FY2020": -47723, "FY2019": -423882, "FY2018": -763195}),
        ("Net cash from/(used in) investing activities", {"FY2025": -104, "FY2024": -408, "FY2023": -698, "FY2021": -1757, "FY2020": -1113, "FY2019": -4848, "FY2018": -1319}),
        ("Net cash from/(used in) financing activities", {"FY2025": -1655356, "FY2024": 56070, "FY2023": -62554, "FY2021": 176598, "FY2020": 62865, "FY2019": 427129, "FY2018": 762126}),
        ("Cash and cash equivalents at end of year", {"FY2025": 254874, "FY2024": 143485, "FY2023": 17161, "FY2021": 13500, "FY2020": 18108, "FY2019": 4079, "FY2018": 5680}),
    ],
    cash_flow_unit="£'000",
    ratios=[
        ("CET1 Ratio", {"FY2025": "15.2%", "FY2024": "16.2%"}),
        ("Tier 1 Ratio", {"FY2025": "15.2%", "FY2024": "16.2%"}),
        ("Total Capital Ratio", {"FY2025": "18.3%", "FY2024": "16.2%"}),
        ("Leverage Ratio", {"FY2025": "4.9%", "FY2024": "6.9%"}),
        ("LCR", {"FY2025": "163%", "FY2024": "1,045%"}),
        ("NSFR", {"FY2025": "138%", "FY2024": "110%"}),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own source "
         "citation for the underlying document/page. FY2022 cash flow and FY2018-FY2023 Pillar 3 are blank - Vida "
         "only became a PRA-authorised bank on 19 November 2024 (no Pillar 3 exists before then; FY2018-FY2020 the "
         "entity was regulated only by the FCA, with no banking licence application even complete until later), and "
         "FY2022's own Annual Report doesn't present a full cash flow statement on a basis comparable to other "
         "years - see the Cash Flow Statement sheet's source note for details. The Balance Sheet/Equity/Cash Flow "
         "sheets and the Income Statement/Asset Quality sheets are on different bases (Company vs Group) in most "
         "pre-2024 years - see each sheet's own source note.",
)

# ---------------------------------------------------------------
bw.save("/Users/armaan/code/katalysis/banks/VIDA FINANCIALS.xlsx")
