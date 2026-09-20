import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021", "FY2020", "FY2019", "FY2018", "FY2017"]
YEAR_LABEL = {y: y for y in YEARS}

AR2025_URL = "https://clear.bank/uploads/assets/ClearBank-Annual-Report-2025.pdf"
AR2023_URL = "https://clear.bank/uploads/assets/ClearBank-Annual-Report-and-Accounts-2023.pdf"
AR2022_URL = "https://clear.bank/uploads/assets/ClearBank-Annual-Report-and-Accounts_2022.pdf"
AR2021_URL = "https://clear.bank/uploads/assets/ClearBank-Annual-Report-2021.pdf"
AR2020_URL = "https://clear.bank/uploads/assets/ClearBank-Annual-Report-2020.pdf"
AR2019_URL = "https://clear.bank/uploads/assets/ClearBank-Annual-Report-2019.pdf"
AR2018_URL = "https://clear.bank/uploads/assets/ClearBank-Annual-Report-2018.pdf"
AR2017_URL = "https://clear.bank/uploads/assets/ClearBank-Annual-Report-2017.pdf"
AR2016_URL = "https://clear.bank/uploads/assets/ClearBank-Annual-Report-2016.pdf"
P3_2025_URL = "https://clear.bank/uploads/assets/ClearBank-Pillar-3-2025.pdf"
# ClearBank's own published filename misspells "Disclosure" as "Discolsure".
P3_2024_URL = "https://clear.bank/uploads/assets/ClearBank-Pillar-3-Discolsure-2024.pdf"
P3_2023_URL = "https://clear.bank/uploads/assets/ClearBank-Pillar-3-Disclosure-2023.pdf"
P3_2022_URL = "https://clear.bank/uploads/assets/ClearBank-Pillar-3-2022.pdf"
P3_2021_URL = "https://clear.bank/uploads/assets/ClearBank-Pillar-3-disclosure-2021.pdf"
P3_2020_URL = "https://clear.bank/uploads/assets/Clear.Bank-Pillar-3-disclosure-2020.pdf"
P3_2019_URL = "https://clear.bank/uploads/assets/ClearBank-Pillar-3-disclosure-2019.pdf"
P3_2018_URL = "https://clear.bank/uploads/assets/ClearBank-Pillar-3-disclosure-2018.pdf"
P3_2017_URL = "https://clear.bank/uploads/assets/ClearBank-Pillar-3-disclosure-2017.pdf"
P3_2016_URL = "https://clear.bank/uploads/assets/ClearBank-Pillar-3-disclosure-2016.pdf"
CBGH_FY2023_URL = "https://find-and-update.company-information.service.gov.uk/company/14254435/filing-history/MzQyMTUzMzg4NGFkaXF6a2N4/document?format=pdf&download=0"

# ---------------------------------------------------------------
# HD-019 FLOOR VERIFICATION (do not delete - this is why YEARS stops at FY2017)
# ---------------------------------------------------------------
# HD-019 originally labelled ClearBank's floor as "FY2015" purely from GLEIF's
# entity-creation-year signal (incorporated 17 Aug 2015). That is NOT the real
# floor. Independently verified against ClearBank's own primary documents:
#   - ClearBank Limited (co. 09736376) was incorporated 17 August 2015.
#   - Its first Annual Report covers a 16-MONTH STUB PERIOD, 17 Aug 2015 to
#     31 Dec 2016 - not a discrete "FY2015" or "FY2016" - and this stub period
#     is entirely PRE-OPERATIONAL: "Customer accounts" and "Loans and advances
#     to customers" are both exactly nil at 31 Dec 2016 (ClearBank Limited
#     2016 Annual Report, Company/Consolidated Statement of Financial
#     Position, p.23 - AR2016_URL). The bank's own Directors' Report for that
#     period states activity was "in line with the ongoing development of IT
#     infrastructure in support of the Bank's proposed launch during 2017."
#   - ClearBank's banking licence was approved by the PRA/FCA in December
#     2016 (ClearBank Limited 2016 Annual Report, Strategic Report, p.9 -
#     AR2016_URL), after which it entered a regulatory "mobilisation" period
#     with no customer-facing activity.
#   - ClearBank's own FY2017 Annual Report states plainly: "As the bank
#     opened to customers in October 2017 subsequent trading for the rest of
#     the year was limited to initial onboarding through November and
#     December... the directors do not consider a full suite of financial and
#     non-financial KPI's to be relevant for the 2017 Annual Report" (AR2017,
#     p.9 - AR2017_URL). FY2017 is the first year with any non-zero customer
#     deposits ("Amounts due to customers" of £1,601k at 31 Dec 2017, vs. nil
#     at 31 Dec 2016) and any income at all (£49k total income vs. £nil).
# This is the same shape of gating event HD-001 found for Barclays Bank UK
# PLC (a real licensing/operational-start event delaying the usable floor
# past the GLEIF entity-creation date) - just for ClearBank the event is
# "banking licence granted Dec 2016 + mobilisation, then genuine customer
# onboarding from Oct 2017" rather than ring-fencing. CONFIRMED FLOOR:
# FY2017 (the first year with real, if tiny, customer-facing banking
# activity) - NOT FY2015 and NOT the FY2016 stub period, which predates any
# customer accounts, any lending, and any income whatsoever.

ENTITY_NOTE = (
    "ClearBank Limited (FRN 754568, company 09736376), a UK clearing/embedded-banking "
    "infrastructure bank. Group basis throughout. Does NOT "
    "take the FRS 101/102 cash-flow-statement exemption - full Consolidated Statement of Cash "
    "Flows every year.\n"
    "WHICH GROUP (corrected 2026-09-16, entity-basis sweep): 'Group' does NOT mean the same "
    "thing across this workbook, and the earlier wording here - 'the Group is essentially the "
    "Bank plus dormant/minor subsidiaries' - is only true up to FY2022. FY2017-FY2022: the "
    "Group is ClearBank Limited and its own subsidiaries, i.e. the workbook entity's own "
    "consolidation. FY2023 onward it is a DIFFERENT legal entity's consolidation: ClearBank "
    "Group Holdings Limited (company 14254435), which received formal PRA approval as a bank "
    "holding company in Q4 2023 and consolidates BOTH ClearBank Limited and ClearBank Europe "
    "N.V., a separately and fully regulated Netherlands bank that sits alongside (not inside) "
    "ClearBank Limited. Primary sources: ClearBank Pillar 3 Disclosure 2023, 'Scope of "
    "consolidation' - 'The Group comprises of ClearBank Group Holdings Limited, a regulated "
    "financial holding company, and its 100% owned and controlled subsidiaries, ClearBank "
    "Limited (the \"UK Bank\", a fully regulated UK bank) and ClearBank Europe N.V. ClearBank "
    "Limited is currently the only material subsidiary within the Group... Any reference to "
    "comparative metrics are for the required disclosures relating to the material subsidiary, "
    "ClearBank Limited only' (" + P3_2023_URL + "); and ClearBank Pillar 3 Disclosure 2025, "
    "same section, which repeats the three-entity composition with no materiality carve-out "
    "(" + P3_2025_URL + "). So FY2023's comparatives are Bank-only but its own-year figures "
    "are CBGH-consolidated, and FY2024/FY2025 are CBGH-consolidated outright. See the "
    "ENTITY-CHANGE NOTE on the Statement of Changes in Equity sheet for the same boundary on "
    "the statement sheets, which is already documented there.\n"
    "FY2022's own figures (from the FY2022 Annual Report itself) are used here rather than "
    "FY2023's report's restated FY2022 comparative (Note 32 of the FY2023 report flags a "
    "restatement, e.g. profit for the year after tax 6,818 as originally reported vs. 10,760 "
    "restated, and net cash from operating activities 413,627 vs. 416,088 restated) - each "
    "year's own originally-published figures are used throughout this workbook, per project "
    "convention.\n"
    "A genuine, small, undocumented cross-vintage gap exists between FY2023's own closing cash "
    "balance (£6,256,126k) and FY2024's own opening balance per the FY2025 Annual Report's "
    "comparative (£6,258,123k) - a ~£1,997k difference with no explanation found in either "
    "source; both figures are shown exactly as each report states them, not force-reconciled.\n"
    "\"Foreign currency differences\" appears twice with different values in the FY2025/FY2024 "
    "presentation - once within the non-cash adjustments (a small figure) and again within the "
    "working-capital-changes section (a much larger figure driven by FX movement on customer "
    "deposit balances) - both are genuine distinct line items in the source, not a duplicate.\n"
    "FY2020's own \"Operating cash flows before changes in working capital\" subtotal ((20,248)) "
    "does not equal the sum of its own component adjustment lines as disclosed (which sum to "
    "(20,032), a £216k difference) - a genuine, unexplained arithmetic inconsistency within "
    "ClearBank's own FY2020 Annual Report and Accounts, reproduced exactly as published rather "
    "than force-reconciled."
)

CASH_FLOW_SOURCES = (
    "Sources - all figures are ClearBank Limited's own Consolidated Statement of Cash Flows:\n"
    "FY2025/FY2024: ClearBank Annual Report and Accounts 2025, p.71 - " + AR2025_URL + "\n"
    "FY2023: ClearBank Annual Report and Accounts 2023, p.73 - " + AR2023_URL + "\n"
    "FY2022: ClearBank Annual Report and Accounts 2022, p.43 (own originally-published figures, "
    "not FY2023's restated comparative) - " + AR2022_URL + "\n"
    "FY2021: ClearBank Annual Report and Accounts 2021, p.66 - " + AR2021_URL + "\n"
    "FY2020: ClearBank Annual Report and Accounts 2020, p.70 - " + AR2020_URL + "\n"
    "FY2019: ClearBank Annual Report and Accounts 2019, p.71 - " + AR2019_URL + "\n"
    "FY2018: ClearBank Limited 2018 Annual Report, p.59 - " + AR2018_URL + "\n"
    "FY2017: ClearBank Limited 2017 Annual Report, p.52 (own-year figures; cross-checked against "
    "AR2018's own FY2017 comparative column, which matches exactly, so no restatement between "
    "vintages for this year) - " + AR2017_URL + "\n\n"
    + ENTITY_NOTE
)


def p3_sources():
    return (
        "Sources - ClearBank Group Pillar 3 Key Metrics table:\n"
        "REPORTING ENTITY (see the 'WHICH GROUP' note on the Cash Flow Statement sheet): "
        "FY2017-FY2022 these metrics are ClearBank Limited's own consolidation; FY2023-FY2025 "
        "they are ClearBank Group Holdings Limited's consolidation (company 14254435), which "
        "also includes ClearBank Europe N.V. There is no ClearBank-Limited-only Pillar 3 "
        "publication for FY2023 onward, so these are group-basis figures in an entity-level "
        "workbook and are NOT a like-for-like continuation of the FY2017-FY2022 series.\n"
        "FY2025: ClearBank Pillar 3 Disclosure 2025, 'Key metrics' table, p.15 - " + P3_2025_URL + "\n"
        "FY2024: ClearBank Pillar 3 Disclosure 2024, 'Key metrics' table, p.13 - " + P3_2024_URL + " "
        "(located 2026-09-16; the file is published under a misspelt name, 'ClearBank-Pillar-3-Discolsure-"
        "2024.pdf', which is why earlier passes cited the FY2025 edition's comparative column instead. Every "
        "FY2024 figure is identical in the two, so no value changed - but the citation now points at FY2024's "
        "own edition, as this project requires.)\n"
        "FY2023: ClearBank Pillar 3 Disclosure 2023, p.5-6 - " + P3_2023_URL + "\n"
        "FY2022/FY2021: ClearBank Pillar 3 Disclosure 2022, p.4-5 (FY2021 as the FY2022 "
        "document's own comparative column, cross-checked against ClearBank Pillar 3 Disclosure "
        "2021's own Table 1/Table 2 - CET1 140%/£36,739k there vs. 139.70%/£37m here, consistent "
        "to rounding) - " + P3_2022_URL + " and " + P3_2021_URL + "\n"
        "FY2020: mostly ClearBank Annual Report and Accounts 2020's own \"Robust capital, liquidity "
        "and balance sheet\" financial review narrative (CET1 ratio, LCR, NSFR) and Note 22 Capital "
        "management (CET1 capital £29,952k) - " + AR2020_URL + "; UK Leverage Ratio (30%) and Total "
        "RWA (£26.2m) are NOT disclosed anywhere in AR2020 itself and are instead taken from "
        "ClearBank Pillar 3 disclosure 2021's own FY2020 comparative column (Table 1 and the COREP "
        "own-funds template) - " + P3_2021_URL + "\n"
        "FY2019: ClearBank Annual Report and Accounts 2019, financial review KPI table and Note 21 "
        "Capital management - " + AR2019_URL + "\n"
        "FY2018: ClearBank Limited 2018 Annual Report, financial review KPI table and capital/"
        "leverage notes - " + AR2018_URL + "\n"
        "FY2017: ClearBank Limited 2017 Annual Report, p.9 KPI table and p.19 capital/leverage "
        "notes - " + AR2017_URL + "\n\n"
        "PRE-2021 DISCLOSURE FORMAT NOTE, CORRECTED 2026-09-16. This note previously read 'ClearBank did "
        "not publish a standalone Pillar 3 document for FY2017-FY2020'. That is FALSE and is retracted. "
        "ClearBank has published a standalone Pillar 3 disclosure every year since FY2016, and all of them "
        "are live on clear.bank today - they are listed in the site's own sitemap under /pillar-3-disclosure "
        "but are not all linked from the visible page, which is why earlier passes missed them:\n"
        "  FY2020 - " + P3_2020_URL + "\n"
        "  FY2019 - " + P3_2019_URL + "\n"
        "  FY2018 - " + P3_2018_URL + "\n"
        "  FY2017 - " + P3_2017_URL + "\n"
        "  FY2016 - " + P3_2016_URL + "\n"
        "Each was downloaded and read on 2026-09-16 (HTTP 200, application/pdf, %PDF magic bytes, real text "
        "layers). What IS true, and is the substantive point the old note was reaching for, is that none of "
        "those editions uses the KM1 template or anything like it: each has a bespoke 'Summary Analysis' "
        "section with 'Table 1: Capital and leverage ratios' and 'Table 2: Own funds'. The FY2020 edition's "
        "Table 1 gives CET1/Tier 1/Total 114%, CRD leverage 3%, UK leverage 30%, and its Table 2 gives CET1 "
        "capital of £29,952k - which is what this workbook already carries for FY2020, so no figure changes. "
        "The FY2019 edition prints CET1 capital of £17,460k where this workbook carries £17,461k from "
        "AR2019; the £1k difference is left as each source printed it. Re-sourcing FY2016-FY2019 from these "
        "documents rather than from the Annual Reports is a real improvement left for a later pass - it is "
        "logged here rather than done, because the KM1 rollout ticket that found them covers the KM1 sheet "
        "and the latest edition, not a re-sourcing of nine-year-old columns.\n"
        "FY2017-FY2019's CET1/leverage ratios are disclosed only to whole-percent precision in "
        "the source (e.g. \"53%\", \"88%\"); FY2020's are disclosed to 1 decimal place via the "
        "FY2021 Pillar 3 document's comparative column. No Basel II/CET1-terminology issue arises "
        "for any of these years (all post-date the 2014 CRD IV/CET1 introduction).\n"
        "CET1 = Tier 1 = Total Capital every year (no AT1/Tier 2 instruments). No MREL ratio is "
        "disclosed in any Pillar 3 document or Annual Report reviewed (FY2017-FY2025); the FY2018-FY2021 "
        "Pillar 3 documents state the Bank is not required to hold additional capital for MREL - see the "
        "MREL Ratio sheet (corrected 2026-09-19, GA-020).\n"
        "LEVERAGE RATIO BASIS NOTE: FY2021's own Pillar 3 document (Table 1) discloses two "
        "different leverage figures with materially different values - a \"CRD leverage ratio\" "
        "of 1% and a \"UK leverage ratio\" of 39%, reflecting genuinely different exposure-measure "
        "definitions, not a typo. The 38.79% figure used here for FY2021 (from the FY2022 "
        "document's comparative, \"excluding claims on central banks\" basis) matches the UK "
        "leverage ratio figure, consistent with the basis used FY2022 onward. FY2017-FY2020's "
        "leverage ratios are each year's own disclosed \"UK Leverage Ratio\" (84%/74%/21%/30%), "
        "which pre-date the \"excluding claims on central banks\" wording introduced later - shown "
        "as originally disclosed each year, not adjusted for comparability."
    )


bw = BankWorkbook(bank_name="ClearBank Limited", years=YEARS, year_label=YEAR_LABEL, header_color="E47F85")

# ---------------------------------------------------------------
# Statements sources / notes
# ---------------------------------------------------------------
STATEMENTS_ENTITY_NOTE = (
    "ENTITY-CHANGE NOTE (corrected on follow-up review against ClearBank Group Holdings "
    "Limited's own FY2023 Companies House filing, company 14254435): FY2021-FY2023 figures "
    "are ClearBank Limited's own statements (Companies House 09736376). FY2024/FY2025 "
    "figures are instead from the Annual Report and Accounts 2025, whose auditor's report "
    "and Statement of Financial Position are addressed to \"ClearBank Group Holdings "
    "Limited\" - a NEW intermediate holding entity (incorporated 25 July 2022) inserted "
    "above ClearBank Limited DURING FY2023, not between FY2023 and FY2024 as an earlier "
    "pass of this workbook stated. Per that entity's own first Group accounts (period ended "
    "31 December 2023, filed at Companies House 18 May 2024 - " + CBGH_FY2023_URL + "), its "
    "inaugural subsidiary ClearBank Europe N.V. was incorporated 6 March 2023; it acquired "
    "100% of ClearBank Limited on 8 December 2023 as a Business Combination Under Common "
    "Control, with ClearBank Limited's results consolidated from 1 May 2023 (the day after "
    "common control was established, 30 April 2023). \"CB Growth Holdings Limited\" (named "
    "in AR2023's own equity note 3, and confirmed in ClearBank Group Holdings Limited's own "
    "Note 1.4 as \"its parent\") is a GENUINELY SEPARATE, higher entity in the group chain - "
    "not an earlier name for ClearBank Group Holdings Limited (no Companies House "
    "previous-names record exists for company 14254435, and its own filing history shows no "
    "rename). The corrected chain, top to bottom, is: CB Growth Holdings Limited -> "
    "ClearBank Group Holdings Limited (14254435) -> ClearBank Limited. This is a genuine "
    "change of reporting entity, not a presentation choice: the Statement of Changes in "
    "Equity's FY2024 opening balance (£196,497k) does not equal FY2023's own closing balance "
    "(£129,526k) below, and the two entities' equity bases are not directly comparable, so no "
    "plug/bridging row is used across that boundary in this sheet. However, a genuine bridge "
    "DOES exist and is now cited for traceability: ClearBank Group Holdings Limited's own "
    "stub-period Consolidated statement of changes in equity (in the filing above) runs from "
    "£(812)k total equity at 1 March 2023 (its own first reporting date) to exactly £196,497k "
    "at 31 December 2023 - i.e. this workbook's existing FY2024 opening figure is that "
    "entity's own closing balance for its first, ~10-month accounting period, built mostly "
    "from a £179,405k share capital issuance (the mechanism for the ClearBank Limited "
    "acquisition) rather than organic trading profit. This bridging period is not added as "
    "its own column here since it doesn't align with this workbook's FY-year grid, but the "
    "£196,497k figure is now independently verified against its true source rather than only "
    "appearing as an unexplained opening balance. Balance Sheet and P&L totals for each year "
    "are still internally consistent (assets = liabilities + equity; income - expenses = "
    "profit/loss) since each is a same-entity, same-year snapshot - only the cross-year "
    "equity roll-forward is affected. FY2023's own Statement of Financial Position/"
    "Comprehensive Income are Company-only (ClearBank Limited did not publish Consolidated "
    "statements that year - see the Company vs Consolidated presentation note below); "
    "FY2021/FY2022/FY2024/FY2025 are Consolidated. Per project convention, each year's own "
    "originally-published figures are used throughout (FY2022's own AR2022 Consolidated "
    "figures, not AR2023's restated comparative - see CASH_FLOW_SOURCES' existing "
    "ENTITY_NOTE for the same convention applied to Cash Flow)."
)

PRESENTATION_NOTE = (
    "PRESENTATION NOTE: FY2021's own Statement of Comprehensive Income discloses only Net "
    "interest income and Net fee income (no separate Interest income/expense or Fee "
    "income/expense split) - per AR2022's own footnote, \"In 2021, only net interest income "
    "and net fee income were presented without splitting for gross amounts.\" FY2023's own "
    "Statement of Comprehensive Income additionally has an \"Expenses recharged\" line "
    "(income, not cost) not present in any other year, resulting in a positive \"Operating "
    "profit\" that year rather than the \"Operating loss\" label used elsewhere - both "
    "reproduced as reported. Balance Sheet: \"Loans and advances to banks\" (an interbank "
    "placement, not a customer loan) appears as its own line FY2021-FY2023 only - dropped "
    "from FY2024/FY2025's presentation (folded into Cash and cash equivalents per the "
    "Group's own accounting policy note). \"Due from UK tax authorities\" (FY2022/FY2023) "
    "and \"Current tax asset\" (FY2024/FY2025) are the same concept under different labels; "
    "FY2021 has neither line. Equity: \"Share-based payment reserve\" (FY2021/FY2022) was "
    "replaced by \"Capital contribution reserve\" from FY2023 onward (see the entity-change "
    "note above); \"Treasury shares\" and \"Translation reserve\" are absent from FY2023's "
    "Company-only presentation, present in every other year's Consolidated presentation.\n"
    "FY2017-FY2020 presentation: \"Amounts due to customers\" (FY2017 label) and \"Customer "
    "deposits\" (FY2018-FY2020 label) are the same concept under different labels - ClearBank "
    "opened to customers in October 2017, so FY2017's figure (£1,601k) reflects barely two "
    "months of customer-facing activity. \"Right-of-use assets\"/\"Lease obligations\" first "
    "appear in FY2019 (adoption of IFRS 16, replacing IAS 17 - see the Group's own Note 3.1) - "
    "absent FY2017/FY2018. \"Translation reserve\" first appears in FY2019 (a small foreign "
    "currency translation difference of £33k) - absent FY2017/FY2018, which had no foreign "
    "operations giving rise to translation differences. \"Deferred income\" first appears in "
    "FY2019 - absent FY2017/FY2018. FY2017's Statement of Comprehensive Income shows no "
    "Interest expense line (Net interest income was not yet split into gross Interest "
    "income/expense until FY2019) and no Impairments line (first appears FY2019)."
)

STATEMENTS_SOURCES = (
    "Sources - ClearBank's own Statement of Comprehensive Income / Statement of Financial "
    "Position / Statement of Changes in Equity, transcribed from each year's own report:\n"
    "FY2025/FY2024: Consolidated statements, ClearBank Group Holdings Limited Annual Report "
    "and Accounts 2025, pp.68-70 - " + AR2025_URL + "\n"
    "FY2023: Company statements (no Consolidated statements published that year), ClearBank "
    "Annual Report and Accounts 2023, pp.69-72 - " + AR2023_URL + "\n"
    "FY2022: Consolidated statements, own originally-published figures (not FY2023's "
    "restated comparative - see Note 32 of the FY2023 report), ClearBank Annual Report and "
    "Accounts 2022, pp.80-83 - " + AR2022_URL + "\n"
    "FY2021: Consolidated statements, ClearBank Limited Annual Report and Accounts 2021, "
    "pp.60-63 - " + AR2021_URL + "\n"
    "FY2020: Consolidated statements, ClearBank Limited Annual Report and Accounts 2020, "
    "pp.66-70 - " + AR2020_URL + "\n"
    "FY2019: Consolidated statements, ClearBank Limited Annual Report and Accounts 2019, "
    "pp.66-71 - " + AR2019_URL + "\n"
    "FY2018: Consolidated statements, ClearBank Limited 2018 Annual Report, pp.54-58 - " + AR2018_URL + "\n"
    "FY2017: Consolidated statements, ClearBank Limited 2017 Annual Report, pp.46-52 (own-year "
    "figures; cross-checked against AR2018's own FY2017 comparative column, which matches "
    "exactly - no restatement between vintages for this year) - " + AR2017_URL + "\n\n"
    "FLOOR VERIFICATION NOTE (HD-019): ClearBank Limited was incorporated 17 August 2015, but "
    "its first Annual Report covers a 16-month pre-operational stub period (17 Aug 2015 - 31 "
    "Dec 2016) with nil customer accounts, nil lending, and nil income throughout - see the "
    "HD-019 FLOOR VERIFICATION comment block near the top of this script for the full evidence "
    "trail. FY2017 (the first year with any customer deposits or income at all, following the "
    "bank's actual opening to customers in October 2017) is the confirmed, independently "
    "verified floor for this workbook - not FY2015/FY2016.\n\n"
    + STATEMENTS_ENTITY_NOTE + "\n\n" + PRESENTATION_NOTE
)

RWA_SOURCES = (
    "Sources - ClearBank Group Pillar 3 \"Overview of RWA\"/\"Overview of risk weighted "
    "exposure amounts\" table:\n"
    "FY2025/FY2024: ClearBank Pillar 3 Disclosure 2025, p.18 - " + P3_2025_URL + "\n"
    "FY2023: ClearBank Pillar 3 Disclosure 2023, p.11 (ClearBank Group column) - " + P3_2023_URL + "\n"
    "FY2022: ClearBank Pillar 3 disclosure 2022, p.15 (own originally-published figures, not "
    "FY2023's restated comparative - see note below) - " + P3_2022_URL + "\n"
    "FY2021: ClearBank Pillar 3 disclosure 2022, p.15 (FY2021 comparative column) - " + P3_2022_URL + "\n"
    "FY2020: derived from ClearBank Pillar 3 disclosure 2021's own FY2020 comparative column - "
    "Total RWA £26.2m (COREP own-funds template, line 60) and Operational risk Pillar 1 capital "
    "requirement £0.7m (implying Operational RWA = £0.7m / 8% = £8.75m by definition); Credit "
    "risk RWA (£17.45m) is the residual (Total - Operational), not itself a directly-disclosed "
    "single line item - " + P3_2021_URL + "\n"
    "FY2019: Credit risk RWA (£15,664k) is ClearBank's own explicitly-disclosed \"credit risk "
    "exposure by asset and exposure class\" table (ClearBank Annual Report and Accounts 2019, "
    "financial review section) - " + AR2019_URL + ". No operational-risk RWA or Total RWA figure "
    "is disclosed anywhere in the FY2019 Annual Report, so Operational risk and Total RWAs are "
    "left blank for FY2019 rather than estimated.\n"
    "FY2018: Credit risk RWA (£9,184k) is ClearBank's own explicitly-disclosed credit risk "
    "exposure table (ClearBank Limited 2018 Annual Report, p.22) - " + AR2018_URL + ". Same gap "
    "as FY2019: no operational-risk RWA or Total RWA disclosed, left blank.\n"
    "FY2017: Credit risk RWA (£2,366k) is ClearBank's own explicitly-disclosed credit risk "
    "exposure table (ClearBank Limited 2017 Annual Report, p.19) - " + AR2017_URL + ". Same gap: "
    "no operational-risk RWA or Total RWA disclosed, left blank.\n\n"
    "Only two risk categories are disclosed in any year: Credit risk (excluding CCR, "
    "Standardised Approach) and Operational risk (Basic Indicator Approach) - no market risk, "
    "CCR, or CVA charge in any year (consistent with a clearing/embedded-banking bank with no "
    "trading book).\n"
    "FY2024's Total here (£212m = £34m + £178m) is £1m higher than the FY2024 figure on this "
    "workbook's own Total RWAs sheet (£211m) - an immaterial rounding artifact in ClearBank's "
    "own Pillar 3 table, reproduced as disclosed rather than force-matched.\n"
    "RESTATEMENT NOTE: ClearBank's own FY2022 Pillar 3 disclosure (2022 edition) states "
    "Operational risk RWA of £22m (Total £38m), matching this workbook's existing Total RWAs "
    "sheet. The FY2023 Pillar 3 disclosure's own FY2022 comparative column instead shows "
    "Operational risk RWA of £55m (Total £71m) - a large restatement between Pillar 3 "
    "vintages with no explanation given. Per project convention, FY2022's own "
    "originally-published figures (£16m credit / £22m operational / £38m total) are used "
    "here, not the later restated comparative."
)

ASSET_QUALITY_SOURCES = (
    "Sources - ClearBank's own \"Credit risk\" and \"Impairment of financial assets\" notes "
    "(Note 21/2.6), read in full for all 9 years:\n"
    "FY2025/FY2024: ClearBank Group Holdings Limited Annual Report and Accounts 2025, pp.77,88 "
    "- " + AR2025_URL + "\n"
    "FY2023: ClearBank Annual Report and Accounts 2023, credit risk/impairment notes - " + AR2023_URL + "\n"
    "FY2022/FY2021: ClearBank Annual Report and Accounts 2022, credit risk/impairment notes - " + AR2022_URL + "\n"
    "FY2020: ClearBank Annual Report and Accounts 2020, credit risk section - " + AR2020_URL + "\n"
    "FY2019: ClearBank Annual Report and Accounts 2019, credit risk section - " + AR2019_URL + "\n"
    "FY2018: ClearBank Limited 2018 Annual Report, credit risk section - " + AR2018_URL + "\n"
    "FY2017: ClearBank Limited 2017 Annual Report, p.19 (\"Currently, the bank has not started "
    "lending to customers and hence has no direct credit exposure\") - " + AR2017_URL + "\n\n"
    "GENUINE STRUCTURAL FINDING, NOT A DATA GAP: ClearBank does not lend to customers at "
    "all. Its own FY2025 Annual Report states plainly: \"The Group does not provide any "
    "credit facilities which are not fully collateralised to its customers and is therefore "
    "not exposed to associated credit risks\" and \"the Group's trade receivables and hence "
    "ECL are immaterial, with no further ECL-related disclosures considered necessary by "
    "management.\" This wording (or its equivalent) recurs across all 9 years reviewed "
    "(FY2017-FY2019: \"the bank has not started lending to customers and hence has no direct "
    "credit exposure\"). "
    "There is therefore no customer loan book, no IFRS 9 stage split, and no loss allowance "
    "of any kind recognised in any year - ClearBank's only credit exposure is to its treasury "
    "counterparties (predominantly the Bank of England) and to collateral it holds FROM "
    "clients (an asset-side benefit, not a risk), both deemed low/immaterial risk by the "
    "Group's own policy. \"Loans and advances to banks\" on the Balance Sheet (FY2021-FY2023 "
    "only, see Presentation Note on the Balance Sheet sheet) is an interbank treasury "
    "placement, not customer lending."
)


# ---------------------------------------------------------------
# Sheet: Balance Sheet
# ---------------------------------------------------------------
bs_rows = [
    ("SECTION", "Assets", {}),
    ("DATA", "Cash and cash equivalents",
     {"FY2025": 17956976, "FY2024": 10961293, "FY2023": 6256126, "FY2022": 3125862, "FY2021": 2720797,
      "FY2020": 1013224, "FY2019": 526594, "FY2018": 62527, "FY2017": 27062}),
    ("DATA", "Loans and advances to banks",
     {"FY2023": 19525, "FY2022": 9156, "FY2021": 5962}),
    ("DATA", "Collateral placed",
     {"FY2025": 509, "FY2024": 1368, "FY2023": 1352, "FY2022": 433, "FY2021": 406,
      "FY2020": 370, "FY2019": 364, "FY2018": 364, "FY2017": 315}),
    ("DATA", "Receivables",
     {"FY2025": 17296, "FY2024": 10408, "FY2023": 9768, "FY2022": 6212, "FY2021": 4478,
      "FY2020": 4565, "FY2019": 3900, "FY2018": 1487, "FY2017": 1176}),
    ("DATA", "Current tax asset / due from UK tax authorities",
     {"FY2025": 1563, "FY2024": 753, "FY2023": 3542, "FY2022": 4363}),
    ("DATA", "Right-of-use asset",
     {"FY2025": 549, "FY2024": 2111, "FY2023": 952, "FY2022": 2677, "FY2021": 510,
      "FY2020": 2180, "FY2019": 4530}),
    ("DATA", "Property, plant and equipment",
     {"FY2025": 0, "FY2024": 34, "FY2023": 97, "FY2022": 566, "FY2021": 451,
      "FY2020": 673, "FY2019": 351, "FY2018": 819, "FY2017": 1082}),
    ("DATA", "Intangible assets",
     {"FY2025": 51683, "FY2024": 52670, "FY2023": 41806, "FY2022": 29184, "FY2021": 27479,
      "FY2020": 22475, "FY2019": 18751, "FY2018": 13924, "FY2017": 6728}),
    ("DATA", "Deferred tax asset",
     {"FY2025": 39779, "FY2024": 35426, "FY2023": 33682, "FY2022": 25956, "FY2021": 12525,
      "FY2020": 9484, "FY2019": 8335, "FY2018": 8335, "FY2017": 3652}),
    ("TOTAL", "Total assets",
     {"FY2025": 18068355, "FY2024": 11064063, "FY2023": 6366850, "FY2022": 3204409, "FY2021": 2772608,
      "FY2020": 1052971, "FY2019": 562825, "FY2018": 87456, "FY2017": 40015}),
    ("SECTION", "Liabilities", {}),
    ("DATA", "Customer deposits",
     {"FY2025": 17826803, "FY2024": 10818568, "FY2023": 6147363, "FY2022": 2982259, "FY2021": 2644756,
      "FY2020": 925890, "FY2019": 457981, "FY2018": 44145, "FY2017": 1601}),
    ("DATA", "Other payables",
     {"FY2025": 27067, "FY2024": 20708, "FY2023": 82372, "FY2022": 109307, "FY2021": 9897,
      "FY2020": 6591, "FY2019": 8570, "FY2018": 6403, "FY2017": 4367}),
    ("DATA", "Lease obligations",
     {"FY2025": 1256, "FY2024": 2219, "FY2023": 1003, "FY2022": 2789, "FY2021": 509,
      "FY2020": 2483, "FY2019": 4520}),
    ("DATA", "Deferred income",
     {"FY2025": 390, "FY2024": 277, "FY2023": 6444, "FY2022": 22742, "FY2021": 45229,
      "FY2020": 59760, "FY2019": 51512}),
    ("DATA", "Current tax liability", {"FY2023": 142}),
    ("TOTAL", "Total liabilities",
     {"FY2025": 17855516, "FY2024": 10841772, "FY2023": 6237324, "FY2022": 3117097, "FY2021": 2700391,
      "FY2020": 994724, "FY2019": 522583, "FY2018": 50548, "FY2017": 5968}),
    ("SECTION", "Equity", {}),
    ("DATA", "Called up share capital", {"FY2025": 2, "FY2024": 2}),
    ("DATA", "Share premium",
     {"FY2025": 224403, "FY2024": 224403, "FY2023": 203445, "FY2022": 192349, "FY2021": 191816,
      "FY2020": 157316, "FY2019": 113204, "FY2018": 78329, "FY2017": 53458}),
    ("DATA", "Treasury shares",
     {"FY2022": -204, "FY2021": -204, "FY2020": -204, "FY2019": -204, "FY2018": -204, "FY2017": -204}),
    ("DATA", "Capital contribution reserve", {"FY2025": 11942, "FY2024": 9188, "FY2023": 26805}),
    ("DATA", "Share-based payment reserve",
     {"FY2022": 24933, "FY2021": 17190, "FY2020": 9519, "FY2019": 5723, "FY2018": 3301, "FY2017": 467}),
    ("DATA", "Retained earnings/(losses)",
     {"FY2025": -24512, "FY2024": -10518, "FY2023": -100724, "FY2022": -129650, "FY2021": -136468,
      "FY2020": -108268, "FY2019": -78472, "FY2018": -44518, "FY2017": -19674}),
    ("DATA", "Translation reserve",
     {"FY2025": 1004, "FY2024": -784, "FY2022": -116, "FY2021": -117, "FY2020": -116, "FY2019": -9}),
    ("TOTAL", "Total equity",
     {"FY2025": 212839, "FY2024": 222291, "FY2023": 129526, "FY2022": 87312, "FY2021": 72217,
      "FY2020": 58247, "FY2019": 40242, "FY2018": 36908, "FY2017": 34047}),
    ("TOTAL", "Total liabilities and equity",
     {"FY2025": 18068355, "FY2024": 11064063, "FY2023": 6366850, "FY2022": 3204409, "FY2021": 2772608,
      "FY2020": 1052971, "FY2019": 562825, "FY2018": 87456, "FY2017": 40015}),
]

bw.add_balance_sheet_sheet(
    title="ClearBank — Consolidated Statement of Financial Position",
    subtitle="£'000. FY2023 is Company-only (no Consolidated statements published that year). See source note at bottom.",
    rows=bs_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=54,
    source_height=380,
)

# ---------------------------------------------------------------
# Sheet: Profit & Loss
# ---------------------------------------------------------------
pl_rows = [
    ("SECTION", "Income", {}),
    ("DATA", "Interest income",
     {"FY2025": 625779, "FY2024": 425289, "FY2023": 243956, "FY2022": 43774,
      "FY2020": 900, "FY2019": 1664, "FY2018": 178, "FY2017": 46}),
    ("DATA", "Interest expense",
     {"FY2025": -554816, "FY2024": -358179, "FY2023": -162042, "FY2022": -9911, "FY2019": -567}),
    ("TOTAL", "Net interest income",
     {"FY2025": 70963, "FY2024": 67110, "FY2023": 81914, "FY2022": 33863, "FY2021": 1842,
      "FY2020": 900, "FY2019": 1097, "FY2018": 178, "FY2017": 46}),
    ("DATA", "Fee income",
     {"FY2025": 66183, "FY2024": 47141, "FY2023": 31390, "FY2022": 25455}),
    ("DATA", "Fee expenses",
     {"FY2025": -5268, "FY2024": -2952, "FY2023": -2620, "FY2022": -1047}),
    ("TOTAL", "Net fee income",
     {"FY2025": 60915, "FY2024": 44189, "FY2023": 28770, "FY2022": 24408, "FY2021": 18614,
      "FY2020": 8785, "FY2019": 3441, "FY2018": 660, "FY2017": 3}),
    ("DATA", "Other income",
     {"FY2025": 806, "FY2024": 787, "FY2023": 663, "FY2022": 13, "FY2021": 938,
      "FY2020": 933, "FY2019": 780}),
    ("TOTAL", "Total income",
     {"FY2025": 132684, "FY2024": 112086, "FY2023": 111347, "FY2022": 58284, "FY2021": 21394,
      "FY2020": 10618, "FY2019": 5318, "FY2018": 838, "FY2017": 49}),
    ("SECTION", "Operating expenses", {}),
    ("DATA", "Staff costs",
     {"FY2025": -78740, "FY2024": -67335, "FY2023": -55318, "FY2022": -40095, "FY2021": -27719,
      "FY2020": -20995, "FY2019": -16573, "FY2018": -14439, "FY2017": -7377}),
    ("DATA", "Depreciation",
     {"FY2025": -2265, "FY2024": -1693, "FY2023": -2212, "FY2022": -1334, "FY2021": -2145,
      "FY2020": -3432, "FY2019": -2891, "FY2018": -620, "FY2017": -490}),
    ("DATA", "Amortisation of intangibles",
     {"FY2025": -15706, "FY2024": -11643, "FY2023": -8869, "FY2022": -7824, "FY2021": -5791,
      "FY2020": -3750, "FY2019": -2914, "FY2018": -1745, "FY2017": -334}),
    ("DATA", "Impairment",
     {"FY2025": -936, "FY2024": -1584, "FY2023": -268, "FY2022": -675, "FY2021": -337,
      "FY2020": -549, "FY2019": -1032}),
    ("DATA", "Other operating expenses",
     {"FY2025": -51287, "FY2024": -39780, "FY2023": -39116, "FY2022": -27710, "FY2021": -16447,
      "FY2020": -12557, "FY2019": -15682, "FY2018": -13567, "FY2017": -9396}),
    ("TOTAL", "Operating expenses",
     {"FY2025": -148934, "FY2024": -122035, "FY2023": -105783, "FY2022": -77638, "FY2021": -52439,
      "FY2020": -41283, "FY2019": -39092, "FY2018": -30371, "FY2017": -17597}),
    ("DATA", "Expenses recharged", {"FY2023": 13054, "FY2022": 8587}),
    ("TOTAL", "Operating profit/(loss)",
     {"FY2025": -16250, "FY2024": -9949, "FY2023": 18618, "FY2022": -10767, "FY2021": -31045,
      "FY2020": -30665, "FY2019": -33774, "FY2018": -29533, "FY2017": -17548}),
    ("DATA", "Other gains/(losses)",
     {"FY2025": -354, "FY2024": -165, "FY2023": -111, "FY2022": -181, "FY2021": 5,
      "FY2020": 3, "FY2019": 4, "FY2018": 6}),
    ("DATA", "Finance costs",
     {"FY2025": -106, "FY2024": -130, "FY2023": -78, "FY2022": -55, "FY2021": -34,
      "FY2020": -115, "FY2019": -73, "FY2017": -3}),
    ("TOTAL", "Profit/(loss) for the year before taxation",
     {"FY2025": -16710, "FY2024": -10244, "FY2023": 18429, "FY2022": -11003, "FY2021": -31074,
      "FY2020": -30777, "FY2019": -33843, "FY2018": -29527, "FY2017": -17551}),
    ("DATA", "Taxation",
     {"FY2025": 945, "FY2024": -74, "FY2023": 3967, "FY2022": 17821, "FY2021": 2874,
      "FY2020": 981, "FY2019": -153, "FY2018": 4683, "FY2017": 3652}),
    ("TOTAL", "Profit/(loss) for the year after taxation",
     {"FY2025": -15765, "FY2024": -10318, "FY2023": 22396, "FY2022": 6818, "FY2021": -28200,
      "FY2020": -29796, "FY2019": -33996, "FY2018": -24844, "FY2017": -13899}),
    ("SECTION", "Other comprehensive income/(loss)", {}),
    ("DATA", "Foreign currency translation differences",
     {"FY2025": 1788, "FY2024": -767, "FY2022": 1, "FY2021": -1, "FY2020": -107, "FY2019": 33}),
    ("TOTAL", "Total comprehensive income/(loss) for the year",
     {"FY2025": -13977, "FY2024": -11085, "FY2023": 22396, "FY2022": 6819, "FY2021": -28201,
      "FY2020": -29903, "FY2019": -33963, "FY2018": -24844, "FY2017": -13899}),
]

bw.add_income_statement_sheet(
    title="ClearBank — Consolidated Statement of Comprehensive Income",
    subtitle="£'000. FY2023 is Company-only (no Consolidated statements published that year). See source note at bottom.",
    rows=pl_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=54,
    source_height=380,
)

# ---------------------------------------------------------------
# Sheet: Statement of Changes in Equity
# ---------------------------------------------------------------
EQ_HEADERS = ["Share capital", "Share premium", "Treasury shares", "Share-based payment reserve",
              "Capital contribution reserve", "Retained earnings/(losses)", "Translation reserve",
              "Total equity"]

eq_rows = [
    ("TOTAL", "At 1 January 2017", (None, 25254, None, None, None, -5775, None, 19479)),
    ("DATA", "Loss for the year (FY2017)", (None, None, None, None, None, -13899, None, -13899)),
    ("DATA", "Issue of share capital (FY2017)", (None, 28204, None, None, None, None, None, 28204)),
    ("DATA", "Own shares acquired (FY2017)", (None, None, -204, None, None, None, None, -204)),
    ("DATA", "Share-based payments (FY2017)", (None, None, None, 467, None, None, None, 467)),
    ("TOTAL", "At 31 December 2017", (None, 53458, -204, 467, None, -19674, None, 34047)),
    ("DATA", "Loss for the year (FY2018)", (None, None, None, None, None, -24844, None, -24844)),
    ("DATA", "Issue of share capital (FY2018)", (None, 24871, None, None, None, None, None, 24871)),
    ("DATA", "Share-based payments (FY2018)", (None, None, None, 2834, None, None, None, 2834)),
    ("TOTAL", "At 31 December 2018", (None, 78329, -204, 3301, None, -44518, None, 36908)),
    ("DATA", "Loss for the year (FY2019)", (None, None, None, None, None, -33996, None, -33996)),
    ("DATA", "Other comprehensive income (FY2019)", (None, None, None, None, None, None, 33, 33)),
    ("DATA", "Issue of share capital (FY2019)", (None, 34875, None, None, None, None, None, 34875)),
    ("DATA", "Share-based payments (FY2019)", (None, None, None, 2422, None, None, None, 2422)),
    ("DATA", "Other movements (FY2019, reserve transfer)", (None, None, None, None, None, 42, -42, None)),
    ("TOTAL", "At 31 December 2019", (None, 113204, -204, 5723, None, -78472, -9, 40242)),
    ("DATA", "Loss for the year (FY2020)", (None, None, None, None, None, -29796, None, -29796)),
    ("DATA", "Other comprehensive loss (FY2020)", (None, None, None, None, None, None, -107, -107)),
    ("DATA", "Issue of share capital (FY2020)", (None, 44112, None, None, None, None, None, 44112)),
    ("DATA", "Share-based payments (FY2020)", (None, None, None, 3796, None, None, None, 3796)),
    ("TOTAL", "At 31 December 2020 (= At 1 January 2021)", (None, 157316, -204, 9519, None, -108268, -116, 58247)),
    ("DATA", "Loss for the year (FY2021)", (None, None, None, None, None, -28200, None, -28200)),
    ("DATA", "Other comprehensive loss (FY2021)", (None, None, None, None, None, None, -1, -1)),
    ("DATA", "Issue of share capital (FY2021)", (None, 34500, None, None, None, None, None, 34500)),
    ("DATA", "Share-based payments (FY2021)", (None, None, None, 7671, None, None, None, 7671)),
    ("TOTAL", "At 31 December 2021", (None, 191816, -204, 17190, None, -136468, -117, 72217)),
    ("DATA", "Profit for the year (FY2022)", (None, None, None, None, None, 6818, None, 6818)),
    ("DATA", "Other comprehensive income (FY2022)", (None, None, None, None, None, None, 1, 1)),
    ("DATA", "Issue of share capital (FY2022)", (None, 533, None, None, None, None, None, 533)),
    ("DATA", "Share-based payments (FY2022)", (None, None, None, 7743, None, None, None, 7743)),
    ("TOTAL", "At 31 December 2022", (None, 192349, -204, 24933, None, -129650, -116, 87312)),
    ("DATA", "Note: FY2023's own report is Company-only - Treasury shares/Translation reserve "
             "columns are not disclosed that year (see Presentation Note); the FY2022 closing "
             "balance it re-presents (£87,312k Total) matches the Consolidated total above exactly.",
     (None, None, None, None, None, None, None, None)),
    ("DATA", "Profit for the year (FY2023)", (None, None, None, None, None, 22396, None, 22396)),
    ("DATA", "Issue of share capital (FY2023)", (None, 11300, None, None, None, None, None, 11300)),
    ("DATA", "Share-based payments and reserve transfer (FY2023)",
     (None, None, None, -21408, 26805, 1332, None, 6729)),
    ("DATA", "Tax on share-based payments (FY2023)", (None, None, None, None, None, 1789, None, 1789)),
    ("TOTAL", "At 31 December 2023", (None, 203445, None, None, 26805, -100724, None, 129526)),
    ("DATA", "ENTITY-CHANGE NOTE: a new intermediate parent, ClearBank Group Holdings Limited, "
             "was inserted above ClearBank Limited during FY2023 (business combination under "
             "common control, consolidated from 1 May 2023 - see Sources below) - the FY2024 "
             "opening balance is that new entity's own closing balance for its first reporting "
             "period (to 31 Dec 2023), not a continuation of the row above.",
     (None, None, None, None, None, None, None, None)),
    ("TOTAL", "At 1 January 2024", (2, 189403, None, None, 3511, 3598, -17, 196497)),
    ("DATA", "Loss for the year (FY2024)", (None, None, None, None, None, -10318, None, -10318)),
    ("DATA", "Other comprehensive loss (FY2024)", (None, None, None, None, None, None, -767, -767)),
    ("DATA", "Issue of share capital (FY2024)", (None, 35000, None, None, None, None, None, 35000)),
    ("DATA", "Share-based payments (FY2024)", (None, None, None, None, 5677, 76, None, 5753)),
    ("DATA", "Tax on share-based payments (FY2024)", (None, None, None, None, None, -3874, None, -3874)),
    ("TOTAL", "At 31 December 2024", (2, 224403, None, None, 9188, -10518, -784, 222291)),
    ("DATA", "Loss for the year (FY2025)", (None, None, None, None, None, -15765, None, -15765)),
    ("DATA", "Other comprehensive income (FY2025)", (None, None, None, None, None, None, 1788, 1788)),
    ("DATA", "Share-based payments (FY2025)", (None, None, None, None, 2754, -1187, None, 1567)),
    ("DATA", "Tax on share-based payments (FY2025)", (None, None, None, None, None, 2958, None, 2958)),
    ("TOTAL", "At 31 December 2025", (2, 224403, None, None, 11942, -24512, 1004, 212839)),
]

bw.add_equity_changes_sheet(
    title="ClearBank — Statement of Changes in Equity",
    subtitle="£'000, chronological. Contains a genuine entity-basis break at FY2023/FY2024 - see the notes rows and source note.",
    headers=EQ_HEADERS,
    rows=eq_rows,
    sources_text=STATEMENTS_SOURCES,
    first_col_width=52,
    source_height=380,
)

# ---------------------------------------------------------------
# Sheet: Cash Flow Statement
# ---------------------------------------------------------------
rows = [
    ("SECTION", "Operating activities", {}),
    ("DATA", "Profit/(loss) for the year after tax",
     {"FY2025": -15765, "FY2024": -10318, "FY2023": 22396, "FY2022": 6818, "FY2021": -28200,
      "FY2020": -29796, "FY2019": -33996, "FY2018": -24844, "FY2017": -13899}),
    ("DATA", "Depreciation of property, plant and equipment",
     {"FY2025": 63, "FY2024": 68, "FY2023": 510, "FY2022": 304, "FY2021": 475,
      "FY2020": 462, "FY2019": 651, "FY2018": 620, "FY2017": 490}),
    ("DATA", "(Profit)/loss on disposals of property, plant and equipment",
     {"FY2022": -13, "FY2021": 15, "FY2020": 26, "FY2019": 79, "FY2018": 5}),
    ("DATA", "Impairment of property, plant and equipment", {"FY2020": 9}),
    ("DATA", "Depreciation of right-of-use assets",
     {"FY2025": 2202, "FY2024": 1624, "FY2023": 1702, "FY2022": 1030, "FY2021": 1670,
      "FY2020": 2969, "FY2019": 2240}),
    ("DATA", "Amortisation of intangible assets",
     {"FY2025": 15706, "FY2024": 11643, "FY2023": 8869, "FY2022": 7824, "FY2021": 5791,
      "FY2020": 3723, "FY2019": 2939, "FY2018": 1745, "FY2017": 334}),
    ("DATA", "Impairment of intangible assets",
     {"FY2025": 936, "FY2024": 1584, "FY2023": 246, "FY2022": 676, "FY2021": 337,
      "FY2020": 549, "FY2019": 1032}),
    ("DATA", "Share-based payment expense",
     {"FY2025": 1567, "FY2024": 5753, "FY2023": 6729, "FY2022": 7743, "FY2021": 7671,
      "FY2020": 3796, "FY2019": 2422, "FY2018": 2834, "FY2017": 467}),
    ("DATA", "Recognition of right-of-use assets", {"FY2021": 34, "FY2020": 110, "FY2019": -570}),
    ("DATA", "Costs of share issue / raising finance (included in professional fees)", {"FY2017": 92}),
    ("DATA", "Tax benefit/(charge)",
     {"FY2025": -945, "FY2024": 74, "FY2023": -3967, "FY2022": -17794, "FY2021": -2874,
      "FY2020": -981, "FY2019": 153, "FY2018": -4683, "FY2017": -3652}),
    ("DATA", "Finance costs", {"FY2022": 34, "FY2021": 10, "FY2020": 108}),
    ("DATA", "Net interest income",
     {"FY2025": -70963, "FY2024": -67110, "FY2023": -81914, "FY2022": -33863, "FY2021": -1842,
      "FY2020": -900, "FY2019": -1097}),
    ("DATA", "Other income", {"FY2025": -798, "FY2024": -678, "FY2023": -380}),
    ("DATA", "Foreign currency differences (non-cash items)",
     {"FY2025": 30, "FY2024": 18, "FY2023": 43, "FY2022": 1, "FY2021": -1,
      "FY2020": -107, "FY2019": 33}),
    ("TOTAL", "Operating cash flows before changes in working capital",
     {"FY2025": -67967, "FY2024": -57342, "FY2023": -45766, "FY2022": -27240, "FY2021": -16914,
      "FY2020": -20248, "FY2019": -26114, "FY2018": -24323, "FY2017": -16168}),
    ("DATA", "Increase/(decrease) in collateral",
     {"FY2025": 859, "FY2024": -16, "FY2023": -919, "FY2022": -27, "FY2021": -36,
      "FY2020": -6, "FY2018": -49, "FY2017": -315}),
    ("DATA", "(Increase)/decrease in loans and advances to banks",
     {"FY2024": 19525, "FY2023": -10369, "FY2022": -3194, "FY2021": -5962}),
    ("DATA", "Increase in receivables",
     {"FY2025": -6288, "FY2024": -1877, "FY2023": -3547, "FY2022": -1734, "FY2021": -294,
      "FY2020": -842, "FY2019": -2565, "FY2018": -311, "FY2017": -689}),
    ("DATA", "Increase/(decrease) in payables",
     {"FY2025": 6359, "FY2024": 46, "FY2023": -26935, "FY2022": 99410, "FY2021": 3306,
      "FY2020": -2143, "FY2019": 1942, "FY2018": 1620, "FY2017": 1920}),
    ("DATA", "Increase/(decrease) in deferred income",
     {"FY2025": 113, "FY2024": -6167, "FY2023": -16298, "FY2022": -24954, "FY2021": -17307,
      "FY2020": 8045, "FY2019": 51512}),
    ("DATA", "Increase in customer deposits/amounts due to customers",
     {"FY2025": 7006677, "FY2024": 4654971, "FY2023": 3152204, "FY2022": 335213, "FY2021": 1718866,
      "FY2020": 467909, "FY2019": 413836, "FY2018": 42544, "FY2017": 1601}),
    ("DATA", "Foreign currency differences (working capital)",
     {"FY2025": 5979, "FY2024": -3846}),
    ("TOTAL", "Cash generated by/from operations",
     {"FY2025": 6945732, "FY2024": 4605294, "FY2023": 3048370, "FY2022": 377474, "FY2021": 1681659,
      "FY2020": 452715, "FY2019": 438611}),
    ("DATA", "Interest received",
     {"FY2025": 625779, "FY2024": 425289, "FY2023": 243957, "FY2022": 43774, "FY2021": 2056,
      "FY2020": 909, "FY2019": 1096}),
    ("DATA", "Interest paid",
     {"FY2025": -553258, "FY2024": -341945, "FY2023": -149139, "FY2022": -7621}),
    ("DATA", "Tax (paid)/received", {"FY2025": -1062, "FY2024": 2134, "FY2023": -640}),
    ("TOTAL", "Net cash generated from operating activities",
     {"FY2025": 7017191, "FY2024": 4690772, "FY2023": 3142548, "FY2022": 413627, "FY2021": 1683715,
      "FY2020": 453624, "FY2019": 439707, "FY2018": 19481, "FY2017": -13651}),
    ("SECTION", "Investing activities", {}),
    ("DATA", "Purchase of property, plant and equipment",
     {"FY2025": -29, "FY2024": -5, "FY2023": -41, "FY2022": -408, "FY2021": -268,
      "FY2020": -800, "FY2019": -262, "FY2018": -320, "FY2017": -640}),
    ("DATA", "Purchase of intangible assets",
     {"FY2025": -15655, "FY2024": -24091, "FY2023": -21737, "FY2022": -7736, "FY2021": -8356,
      "FY2020": -7648, "FY2019": -8573, "FY2018": -8567, "FY2017": -5030}),
    ("TOTAL", "Net cash used in investing activities",
     {"FY2025": -15684, "FY2024": -24096, "FY2023": -21778, "FY2022": -8144, "FY2021": -8624,
      "FY2020": -8448, "FY2019": -8835, "FY2018": -8887, "FY2017": -5670}),
    ("SECTION", "Financing activities", {}),
    ("DATA", "Proceeds from issue of Ordinary Shares",
     {"FY2024": 35000, "FY2023": 11300, "FY2022": 533, "FY2021": 34500,
      "FY2020": 44112, "FY2019": 34875, "FY2018": 24871, "FY2017": 28000}),
    ("DATA", "Direct costs paid for lease acquisition", {"FY2025": -24}),
    ("DATA", "Cost of raising finance", {"FY2017": -92}),
    ("DATA", "Principal paid on lease liabilities",
     {"FY2025": -1579, "FY2024": -1567, "FY2023": -1763, "FY2022": -917, "FY2021": -1974,
      "FY2020": -2650, "FY2019": -1607}),
    ("DATA", "Interest paid on lease liabilities", {"FY2021": -34, "FY2019": -73}),
    ("TOTAL", "Net cash generated from/(used in) financing activities",
     {"FY2025": -1603, "FY2024": 33433, "FY2023": 9537, "FY2022": -384, "FY2021": 32492,
      "FY2020": 41462, "FY2019": 33195, "FY2018": 24871, "FY2017": 27908}),
    ("TOTAL", "Net increase in cash and cash equivalents",
     {"FY2025": 6999904, "FY2024": 4700109, "FY2023": 3130307, "FY2022": 405099, "FY2021": 1707583,
      "FY2020": 486638, "FY2019": 464067, "FY2018": 35465, "FY2017": 8587}),
    ("DATA", "Cash and cash equivalents at the beginning of the year",
     {"FY2025": 10961293, "FY2024": 6258123, "FY2023": 3125862, "FY2022": 2720797, "FY2021": 1013224,
      "FY2020": 526594, "FY2019": 62527, "FY2018": 27062, "FY2017": 18475}),
    ("DATA", "Effect of foreign exchange rate changes",
     {"FY2025": -4221, "FY2024": 3061, "FY2023": -43, "FY2022": -34, "FY2021": -10, "FY2020": -8}),
    ("TOTAL", "Cash and cash equivalents at the end of the year",
     {"FY2025": 17956976, "FY2024": 10961293, "FY2023": 6256126, "FY2022": 3125862, "FY2021": 2720797,
      "FY2020": 1013224, "FY2019": 526594, "FY2018": 62527, "FY2017": 27062}),
]

bw.add_cash_flow_sheet(
    title="ClearBank Limited — Consolidated Cash Flow Statement",
    subtitle="Group basis, £'000. See source note at bottom.",
    rows=rows,
    sources_text=CASH_FLOW_SOURCES,
    first_col_width=78,
    source_height=280,
    unit_suffix=" (£'000)",
)

# ---------------------------------------------------------------
# Sheet: Asset Quality
# ---------------------------------------------------------------
aq_rows = [
    ("SECTION", "Loan book", {}),
    ("DATA", "Customer loans and advances",
     {"FY2025": 0, "FY2024": 0, "FY2023": 0, "FY2022": 0, "FY2021": 0,
      "FY2020": 0, "FY2019": 0, "FY2018": 0, "FY2017": 0}),
    ("DATA", "Loss allowance on customer loans",
     {"FY2025": 0, "FY2024": 0, "FY2023": 0, "FY2022": 0, "FY2021": 0,
      "FY2020": 0, "FY2019": 0, "FY2018": 0, "FY2017": 0}),
    ("SECTION", "Interbank treasury placements ('Loans and advances to banks')", {}),
    ("DATA", "Carrying amount",
     {"FY2023": 19525, "FY2022": 9156, "FY2021": 5962}),
    ("DATA", "Loss allowance recognised", {"FY2023": 0, "FY2022": 0, "FY2021": 0}),
]

bw.add_asset_quality_sheet(
    title="ClearBank — Asset Quality / Credit Risk Disclosures",
    subtitle="£'000. ClearBank does not lend to customers - see the structural finding in the source note below.",
    rows=aq_rows,
    sources_text=ASSET_QUALITY_SOURCES,
    first_col_width=64,
    source_height=280,
)

# ---------------------------------------------------------------
# Pillar 3 metric sheets
# ---------------------------------------------------------------
def metric(name, unit, rows_data, note=None):
    bw.add_metric_sheet(name, unit, rows_data, p3_sources(), note=note, first_col_width=44, source_height=190)


CET1_CAPITAL = {"FY2025": 132, "FY2024": 141, "FY2023": 126, "FY2022": 33, "FY2021": 36.7,
                "FY2020": 29.952, "FY2019": 17.461, "FY2018": 17.890, "FY2017": 23.681}
CET1_RATIO = {"FY2025": "49.75%", "FY2024": "67.02%", "FY2023": "77.45%", "FY2022": "87.66%", "FY2021": "139.70%",
              "FY2020": "114.20%", "FY2019": "88%", "FY2018": "35%", "FY2017": "53%"}
RWA = {"FY2025": 266, "FY2024": 211, "FY2023": 163, "FY2022": 38, "FY2021": 26, "FY2020": 26.2}
LEVERAGE = {"FY2025": "20.05%", "FY2024": "26.07%", "FY2023": "43.51%", "FY2022": "13.87%", "FY2021": "38.79%",
            "FY2020": "30%", "FY2019": "21%", "FY2018": "74%", "FY2017": "84%"}
LCR = {"FY2025": "396.85%", "FY2024": "381.88%", "FY2023": "445.36%", "FY2022": "297.05%", "FY2021": "185.94%",
       "FY2020": "186%", "FY2019": "127%", "FY2018": "237%", "FY2017": "3718%"}
NSFR = {"FY2025": "20366.50%", "FY2024": "15959.22%", "FY2023": "10153.88%", "FY2022": "5429.15%", "FY2021": "11701.32%",
        "FY2020": "3298%", "FY2019": "324%", "FY2018": "432%", "FY2017": "878%"}

# ---------------------------------------------------------------
# KM1 Key Metrics - ClearBank's own published table, reproduced as printed.
#
# ClearBank prints the KM1 template WITHOUT its row numbers and under a plain
# "Key metrics" heading; the string "KM1" appears nowhere in any edition. It
# is still the template - the rows, their order and the section headings are
# the UK KM1's line for line - it is simply abridged: the rows ClearBank has
# nothing to report against (UK 7b/7c, UK 8a, UK 9a, 10, UK 10a, 14a-14e) are
# not printed at all rather than printed empty. Only the rows the bank
# actually printed are shown here; a row it never printed is not the same as
# a row we failed to find, so this note says which.
#
# WHICH EDITIONS CARRY IT. FY2022 is the first. Confirmed positively, not by
# a text search coming up empty: the FY2016-FY2021 editions were each
# downloaded and read on 2026-09-16, and every one uses a bespoke "Summary
# Analysis" section ("Table 1: Capital and leverage ratios", "Table 2: Own
# funds") that reports CET1/Tier 1/Total as PERCENTAGES only, plus two
# different leverage ratios ("CRD" and "UK"). Those pages were also checked
# for an image-only table - pdfimages finds nothing on them but cover art -
# so the absence is real. FY2021 IS shown below, from the FY2022 edition's
# own comparative column, which is the first time ClearBank presented that
# year in template shape (same treatment as Allica's FY2021).
#
# ENTITY. The column header changes entity mid-series, and the table says so:
# the FY2022 edition heads its columns "31 Dec 2022 / 31 Dec 2021" with the
# narrative referring to "the Bank" (ClearBank Limited's own consolidation),
# while the FY2023 edition heads its single column "ClearBank Group / 31 Dec
# 2023" (ClearBank Group Holdings Limited, company 14254435, which also
# includes ClearBank Europe N.V.). FY2023-FY2025 are therefore group-basis
# and are NOT a like-for-like continuation of FY2021/FY2022. This matches the
# entity note already carried on every other Pillar 3 sheet here.
#
# TWO INTERNAL INCONSISTENCIES IN CLEARBANK'S OWN PRINTING, both recorded and
# neither reconciled - see the source note.
# ---------------------------------------------------------------
km1_rows = [
    ("SECTION", "Available own funds (£m)", {}),
    ("DATA", "Common Equity Tier 1 ('CET 1') capital (£m)",
     {"FY2025": 132, "FY2024": 141, "FY2023": 126, "FY2022": 33, "FY2021": 37}),
    ("DATA", "Tier 1 capital (£m)",
     {"FY2025": 132, "FY2024": 141, "FY2023": 126, "FY2022": 33, "FY2021": 37}),
    ("DATA", "Total capital (£m)",
     {"FY2025": 132, "FY2024": 141, "FY2023": 126, "FY2022": 33, "FY2021": 37}),
    ("SECTION", "Risk-weighted assets ('RWA') (£m)", {}),
    ("DATA", "Total risk-weighted exposure amount (£m)",
     {"FY2025": 266, "FY2024": 211, "FY2023": 163, "FY2022": 38, "FY2021": 26}),
    ("SECTION", "Capital ratios (% of RWA)", {}),
    ("DATA", "Common Equity Tier 1 ratio (%)",
     {"FY2025": "49.75%", "FY2024": "67.02%", "FY2023": "77.45%", "FY2022": "87.66%", "FY2021": "139.70%"}),
    ("DATA", "Tier 1 ratio (%)",
     {"FY2025": "49.75%", "FY2024": "67.02%", "FY2023": "77.45%", "FY2022": "87.66%", "FY2021": "139.70%"}),
    ("DATA", "Total Capital ratio (%)",
     {"FY2025": "49.75%", "FY2024": "67.02%", "FY2023": "77.45%", "FY2022": "87.66%", "FY2021": "139.70%"}),
    ("SECTION", "Additional own funds requirements based on SREP (% of RWA)", {}),
    ("DATA", "Additional CET1 SREP requirements (%)",
     {"FY2025": "7.38%", "FY2024": "9.89%", "FY2023": "0.00%", "FY2022": "0.00%", "FY2021": "0.00%"}),
    ("DATA", "Total SREP own funds requirements (%)",
     {"FY2025": "13.12%", "FY2024": "17.58%", "FY2023": "0.00%", "FY2022": "0.00%", "FY2021": "0.00%"}),
    ("SECTION", "Combined buffer requirements (% of RWA)", {}),
    ("DATA", "Capital conservation buffer (%)",
     {"FY2025": "2.50%", "FY2024": "2.50%", "FY2023": "2.50%", "FY2022": "0.00%", "FY2021": "0.00%"}),
    ("DATA", "Institution specific countercyclical capital buffer (%)",
     {"FY2025": "2.00%", "FY2024": "2.00%", "FY2023": "2.00%", "FY2022": "1.00%", "FY2021": "0.00%"}),
    ("DATA", "Combined buffer requirement (%)",
     {"FY2025": "4.50%", "FY2024": "4.50%", "FY2023": "4.50%", "FY2022": "1.00%", "FY2021": "0.00%"}),
    ("DATA", "Overall capital requirements (%)",
     {"FY2025": "17.62%", "FY2024": "22.08%", "FY2023": "22.11%", "FY2022": "17.49%", "FY2021": "21.77%"}),
    ("DATA", "CET1 available after meeting the total SREP own funds requirements (%)",
     {"FY2025": "36.63%", "FY2024": "49.44%", "FY2023": "77.26%", "FY2022": "79.45%", "FY2021": "83.83%"}),
    ("SECTION", "Leverage ratio", {}),
    ("DATA", "Total exposure measure excluding claims on central banks (£m)",
     {"FY2025": 658, "FY2024": 542, "FY2023": 289, "FY2022": 241, "FY2021": 94}),
    ("DATA", "Leverage ratio excluding claims on central banks (%)",
     {"FY2025": "20.05%", "FY2024": "26.07%", "FY2023": "43.51%", "FY2022": "13.87%", "FY2021": "38.79%"}),
    ("SECTION", "Liquidity Coverage Ratio ('LCR')", {}),
    ("DATA", "Total high-quality liquid assets ('HQLA') (Weighted value-average) (£m)",
     {"FY2025": 17909, "FY2024": 10914, "FY2023": 6187, "FY2022": 3081, "FY2021": 2719}),
    ("DATA", "Cash outflows - Total weighted value (£m)",
     {"FY2025": 4521, "FY2024": 2873, "FY2023": 1398, "FY2022": 1053, "FY2021": 1462}),
    ("DATA", "Cash inflows - Total weighted value (£m)",
     {"FY2025": 9, "FY2024": 15, "FY2023": 9, "FY2022": 16, "FY2021": 0}),
    ("DATA", "Total net outflows (adjusted value) (£m)",
     {"FY2025": 4513, "FY2024": 2858, "FY2023": 1389, "FY2022": 1037, "FY2021": 1462}),
    ("DATA", "Liquidity coverage ratio (%)",
     {"FY2025": "396.85%", "FY2024": "381.88%", "FY2023": "445.36%", "FY2022": "297.05%", "FY2021": "185.94%"}),
    ("SECTION", "Net Stable Funding Ratio ('NSFR')", {}),
    ("DATA", "Total available stable funding (£m)",
     {"FY2025": 14804, "FY2024": 8718, "FY2023": 5032, "FY2022": 2062, "FY2021": 1190}),
    ("DATA", "Total required stable funding (£m)",
     {"FY2025": 72, "FY2024": 55, "FY2023": 50, "FY2022": 38, "FY2021": 10}),
    ("DATA", "NSFR ratio (%)",
     {"FY2025": "20366.50%", "FY2024": "15959.22%", "FY2023": "10,153.88%", "FY2022": "5429.15%", "FY2021": "11701.32%"}),
]

KM1_SOURCES = (
    "Sources - ClearBank's own published key-metrics table, reproduced as printed. Each column is transcribed "
    "from the edition in which that year is the reporting year, except FY2021 (see below).\n"
    "FY2025: ClearBank Pillar 3 Disclosure 2025, 'Key metrics' table, p.15 - " + P3_2025_URL + "\n"
    "FY2024: ClearBank Pillar 3 Disclosure 2024, 'Key metrics' table, p.13 - " + P3_2024_URL + "\n"
    "FY2023: ClearBank Pillar 3 Disclosure 2023, 'Key metrics' / 'Key metrics continued', pp.4-5 - "
    + P3_2023_URL + "\n"
    "FY2022: ClearBank Pillar 3 disclosure 2022, 'Key metrics', pp.4-5 - " + P3_2022_URL + "\n"
    "FY2021: the FY2022 edition's own '31 Dec 2021' comparative column, same table - " + P3_2022_URL + ". "
    "FY2021's OWN edition has no key-metrics table to transcribe (see below), so this is the first time "
    "ClearBank presented that year in template shape.\n\n"
    "NO TEMPLATE BEFORE FY2022 - A POSITIVE FINDING, NOT A FAILED SEARCH. Every ClearBank Pillar 3 edition "
    "from FY2016 to FY2021 was downloaded and read on 2026-09-16 (all live on clear.bank, all HTTP 200 / "
    "application/pdf / %PDF, all with real text layers). Each uses a bespoke 'Summary Analysis' section - "
    "'Table 1: Capital and leverage ratios' (CET1 / Tier 1 / Total regulatory capital as PERCENTAGES only, "
    "plus a 'CRD leverage ratio' and a 'UK leverage ratio' side by side) and 'Table 2: Own funds' (the "
    "equity-to-CET1 build-up in £'000). That is a different disclosure from KM1, not an earlier version of "
    "it, so those years are blank on this sheet and their figures live on the single-metric sheets instead. "
    "Those pages were additionally checked for an image-only table (pdfimages) after a sister bank was found "
    "publishing its KM1 as a bitmap: ClearBank's pre-FY2022 editions contain only cover art and photography, "
    "no table images.\n\n"
    "UNNUMBERED AND ABRIDGED. ClearBank never writes 'KM1' and never prints the template's row numbers; the "
    "heading is simply 'Key metrics'. The rows it does print are the UK KM1's rows, in the template's order, "
    "under the template's own section headings. The rows it does NOT print anywhere - UK 7b, UK 7c, UK 8a, "
    "UK 9a, 10, UK 10a and 14a-14e - are omitted here too rather than shown empty, because ClearBank omits "
    "them from the table itself; that is a statement about ClearBank's disclosure, and it is recorded here "
    "rather than represented as blank cells that could be mistaken for a gap in this workbook.\n\n"
    "ENTITY CHANGES MID-SERIES, AND THE TABLE HEADER SAYS SO. The FY2022 edition heads its columns '31 Dec "
    "2022 / 31 Dec 2021' and its narrative speaks of 'the Bank' - ClearBank Limited's own consolidation. The "
    "FY2023 edition heads its single column 'ClearBank Group / 31 Dec 2023', and FY2024/FY2025 continue on "
    "that basis: ClearBank Group Holdings Limited (company 14254435), which also consolidates ClearBank "
    "Europe N.V. FY2023-FY2025 are therefore group-basis figures in an entity-level workbook and are NOT a "
    "like-for-like continuation of the FY2021/FY2022 columns. Same caveat as the other Pillar 3 sheets.\n\n"
    "TWO INCONSISTENCIES IN CLEARBANK'S OWN PRINTING, recorded and not reconciled:\n"
    "• FY2023 total risk-weighted exposure amount is 163 in the FY2023 edition and 162 in the FY2024 "
    "edition's FY2023 comparative. The 163 shown here is FY2023's own edition.\n"
    "• The FY2025 edition prints FY2024 total RWEA as 211 on its Key metrics table and 212 on its 'Overview "
    "of risk weighted exposure amounts' table, two pages apart in the same document. This sheet shows 211 "
    "(the key-metrics figure); the RWA Breakdown sheet shows 212, its own table's total. Both are as "
    "published.\n\n"
    "FY2023 SREP ROWS LOOK WRONG IN THE SOURCE, AND ARE REPRODUCED ANYWAY. The FY2023 edition prints "
    "'Additional CET1 SREP requirements 0.00%' and 'Total SREP own funds requirements 0.00%' - a total SREP "
    "own funds requirement of zero is not possible (the Pillar 1 minimum alone is 8%), and the same edition's "
    "own 'Overall capital requirements' row prints 22.11%. The FY2024 edition's FY2023 comparative instead "
    "prints 9.91% and 17.61% for those two rows, and 59.84% rather than 77.26% for 'CET1 available after "
    "meeting the total SREP own funds requirements'. Under this project's rule that each year comes from its "
    "own edition, the FY2023 column here carries the FY2023 edition's figures; the FY2024 edition's restated "
    "comparatives are recorded in this note so nothing is lost. The FY2022 edition prints 0.00% for those "
    "rows in both its columns, and a 0.00% capital conservation buffer, which is likewise as published.\n\n"
    "TWO PRINTED PRECISIONS FOR THE SAME FY2021 QUANTITY, ON THIS SHEET AND ON THE CET1/TIER 1/TOTAL "
    "CAPITAL SHEETS - not an error in either "
    "place. This sheet shows 37 for FY2021 because that is what the FY2022 edition's comparative column "
    "prints: ClearBank rounds the whole key-metrics table to whole £m. The CET1 Capital / Tier 1 Capital / "
    "Total Capital sheets show 36.7, because those sheets take FY2021 from FY2021's OWN Pillar 3 edition, "
    "whose 'Table 2: Own funds' gives the figure to the pound (£36,739k). Same quantity, two precisions, two "
    "documents. Both are left as published rather than re-rounded in either direction, because rounding "
    "36,739 to '37' is ClearBank's "
    "act, not this workbook's, and re-deriving '36.7' onto a reproduction sheet would print a number the "
    "key-metrics table never contained.\n\n"
    "PRINTED PRECISION AND LABELS ARE AS EACH EDITION HAS THEM. The FY2023 edition prints the NSFR ratio "
    "with a thousands separator ('10,153.88%') where the others do not; the FY2025/FY2024 editions caption "
    "the LCR row 'Total net outflows (adjusted value)' where the FY2023/FY2022 editions caption it 'Total "
    "net cash outflows (adjusted value)', and capitalise 'Total Capital ratio' where the earlier ones write "
    "'Total capital ratio'. The most recent edition's wording is used for the row label and the variants are "
    "recorded here.\n\n"
    "LATEST-EDITION CHECK, 2026-09-16: taken from clear.bank's own sitemap rather than from the URLs "
    "previously cited here, because the visible /pillar-3-disclosure page does not link every file. The "
    "newest documents published are the Pillar 3 Disclosure 2025 and the Annual Report and Accounts 2025; "
    "there is no FY2026 edition of either, which is expected for a 31 December year-end "
    "(ClearBank-Annual-Report-2026.pdf returns an honest 404 while the 2025 file serves 22.2 MB of PDF). "
    "Checked, none newer. The same sweep turned up the previously-uncited FY2024 Pillar 3 and the FY2016-"
    "FY2020 Pillar 3 documents - see the correction on the other Pillar 3 sheets."
)

bw.add_km1_sheet(
    title="ClearBank — KM1 Key Metrics",
    subtitle="ClearBank's own published key-metrics table, reproduced in its row order, labels and printed "
             "precision. ClearBank prints the UK KM1 template unnumbered, headed simply 'Key metrics', and "
             "abridged to the rows it reports against. Amounts in £m, ratios as printed. FY2021/FY2022 are "
             "ClearBank Limited's consolidation; FY2023-FY2025 are ClearBank Group Holdings Limited's. FY2020 "
             "and earlier are blank - those editions use a different disclosure format entirely, not an "
             "earlier KM1. See source note below.",
    rows=km1_rows,
    sources_text=KM1_SOURCES,
    first_col_width=70,
    source_height=520,
)

metric("CET1 Capital", "£m", [("Common Equity Tier 1 (CET1) capital", CET1_CAPITAL)])
metric("CET1 Ratio", "% of RWA", [("Common Equity Tier 1 ratio", CET1_RATIO)])
metric("Tier 1 Capital", "£m (= CET1 capital; no AT1 instruments)", [("Tier 1 capital", CET1_CAPITAL)])
metric("Tier 1 Ratio", "% of RWA", [("Tier 1 ratio", CET1_RATIO)])
metric("Total Capital", "£m (= CET1 capital; no Tier 2 instruments)", [("Total capital", CET1_CAPITAL)])
metric("Total Capital Ratio", "% of RWA", [("Total capital ratio", CET1_RATIO)])
metric("Total RWAs", "£m", [("Total risk-weighted exposure amount", RWA)])

# ---------------------------------------------------------------
# Sheet: RWA Breakdown
# ---------------------------------------------------------------
rwa_rows = [
    ("SECTION", "RWA by risk category", {}),
    ("DATA", "Credit risk (excluding CCR), standardised approach",
     {"FY2025": 45000, "FY2024": 34000, "FY2023": 36000, "FY2022": 16000, "FY2021": 17000,
      "FY2020": 17450, "FY2019": 15664, "FY2018": 9184, "FY2017": 2366}),
    ("DATA", "Operational risk, basic indicator approach",
     {"FY2025": 221000, "FY2024": 178000, "FY2023": 127000, "FY2022": 22000, "FY2021": 9000,
      "FY2020": 8750}),
    ("TOTAL", "Total RWAs",
     {"FY2025": 266000, "FY2024": 212000, "FY2023": 163000, "FY2022": 38000, "FY2021": 26000,
      "FY2020": 26200}),
]

bw.add_rwa_breakdown_sheet(
    title="ClearBank — RWA Breakdown",
    subtitle="£'000 (source tables are in £m; converted x1000 for unit consistency with other sheets). See source note at bottom.",
    rows=rwa_rows,
    sources_text=RWA_SOURCES,
    first_col_width=54,
    source_height=340,
)
metric("Leverage Ratio", "%",
       [("Leverage ratio excluding claims on central banks", LEVERAGE)],
       note="FY2021 figure is on the \"UK leverage ratio\" basis (39% as originally disclosed in "
            "ClearBank's own FY2021 Pillar 3 document), consistent with the \"excluding claims on "
            "central banks\" basis used FY2022 onward - see the LEVERAGE RATIO BASIS NOTE in this "
            "sheet's source citation for the very different \"CRD leverage ratio\" (1%) also "
            "disclosed for FY2021 on a different exposure-measure definition.")
metric("LCR", "%", [("Liquidity Coverage Ratio", LCR)])
metric("NSFR", "%", [("Net Stable Funding Ratio", NSFR)],
       note="Extreme values (5,000%-20,000%+) are genuine, not a transcription error - ClearBank's "
            "clearing-bank business model holds very large customer deposit balances relative to a "
            "small lending book, so required stable funding is tiny relative to available stable "
            "funding.")

# GA-020 (2026-09-19) evidenced statement texts, per year.
_CB_MREL_NA = ("Not applicable – this year's Pillar 3 MREL section: ClearBank 'has been informed by the PRA that we "
               "are not currently required to hold any additional capital in respect of MREL'")
_CB_MREL_NP = ("Not published – no MREL figure or reference in this year's Pillar 3 or annual report "
               "(full-text search 2026-09-19)")
CB_MREL = {
    "FY2025": _CB_MREL_NP, "FY2023": _CB_MREL_NP, "FY2022": _CB_MREL_NP,
    "FY2024": ("Not published – no MREL figure; FY2024 Pillar 3 (PDF p.8) says only that the 2024 Resolution "
               "Communication left resolution strategy and MREL unchanged for 2025"),
    "FY2021": ("Not applicable – FY2021 Pillar 3 MREL section (PDF p.11): 'Currently, ClearBank is not required to "
               "hold any additional capital in respect of MREL'"),
    "FY2020": _CB_MREL_NA, "FY2019": _CB_MREL_NA, "FY2018": _CB_MREL_NA,
    "FY2017": ("Not published – no MREL figure; FY2017 Pillar 3 says only that MREL applied from 1 Jan 2016, fully "
               "phased in by 1 Jan 2022"),
}
bw.add_not_disclosed_metric_sheets(
    ["MREL Ratio"],
    p3_sources(),
    statements={"MREL Ratio": CB_MREL},
    per_note={"MREL Ratio": "CORRECTED 2026-09-19 (GA-020). This note previously said no qualitative MREL statement "
                             "appears in any Pillar 3 or Annual Report. That was wrong: the Pillar 3 documents carry an "
                             "MREL section in FY2017 (phase-in dates only), FY2018 (PDF p.10), FY2019 (p.10), FY2020 "
                             "(p.10) and FY2021 (p.11) - the last four stating that ClearBank has been informed by the "
                             "PRA that it is not currently required to hold any additional capital in respect of MREL - "
                             "and FY2024 (p.8) notes that the 2024 Resolution Communication left its resolution strategy "
                             "and MREL unchanged for 2025. No MREL ratio or requirement figure is published in any year "
                             "and none is derived. FY2022, FY2023 and FY2025 Pillar 3 documents and every Annual Report "
                             "FY2016-FY2025 available return zero hits for 'MREL' (full-text search 2026-09-19)."},
)

# ---------------------------------------------------------------
# Overview sheet
# ---------------------------------------------------------------
bw.add_overview_sheet(
    balance_sheet_totals=[
        ("Total assets",
         {"FY2025": 18068355, "FY2024": 11064063, "FY2023": 6366850, "FY2022": 3204409, "FY2021": 2772608,
          "FY2020": 1052971, "FY2019": 562825, "FY2018": 87456, "FY2017": 40015}),
        ("Customer deposits",
         {"FY2025": 17826803, "FY2024": 10818568, "FY2023": 6147363, "FY2022": 2982259, "FY2021": 2644756,
          "FY2020": 925890, "FY2019": 457981, "FY2018": 44145, "FY2017": 1601}),
        ("Total equity",
         {"FY2025": 212839, "FY2024": 222291, "FY2023": 129526, "FY2022": 87312, "FY2021": 72217,
          "FY2020": 58247, "FY2019": 40242, "FY2018": 36908, "FY2017": 34047}),
    ],
    balance_sheet_unit="£'000",
    income_statement_totals=[
        ("Total income",
         {"FY2025": 132684, "FY2024": 112086, "FY2023": 111347, "FY2022": 58284, "FY2021": 21394,
          "FY2020": 10618, "FY2019": 5318, "FY2018": 838, "FY2017": 49}),
        ("Operating expenses",
         {"FY2025": -148934, "FY2024": -122035, "FY2023": -105783, "FY2022": -77638, "FY2021": -52439,
          "FY2020": -41283, "FY2019": -39092, "FY2018": -30371, "FY2017": -17597}),
        ("Profit/(loss) for the year after taxation",
         {"FY2025": -15765, "FY2024": -10318, "FY2023": 22396, "FY2022": 6818, "FY2021": -28200,
          "FY2020": -29796, "FY2019": -33996, "FY2018": -24844, "FY2017": -13899}),
    ],
    income_statement_unit="£'000",
    equity_changes_totals=[
        ("Opening equity",
         {"FY2025": 222291, "FY2024": 196497, "FY2023": 87312, "FY2022": 72217, "FY2021": 58247,
          "FY2020": 40242, "FY2019": 36908, "FY2018": 34047, "FY2017": 19479}),
        ("Total comprehensive income/(loss) for the year",
         {"FY2025": -13977, "FY2024": -11085, "FY2023": 22396, "FY2022": 6819, "FY2021": -28201,
          "FY2020": -29903, "FY2019": -33963, "FY2018": -24844, "FY2017": -13899}),
        ("Other equity movements, net",
         {"FY2025": 4525, "FY2024": 36879, "FY2023": 19818, "FY2022": 8276, "FY2021": 42171,
          "FY2020": 47908, "FY2019": 37297, "FY2018": 27705, "FY2017": 28467}),
        ("Closing equity",
         {"FY2025": 212839, "FY2024": 222291, "FY2023": 129526, "FY2022": 87312, "FY2021": 72217,
          "FY2020": 58247, "FY2019": 40242, "FY2018": 36908, "FY2017": 34047}),
    ],
    equity_changes_unit="£'000",
    cash_flow_totals=[
        ("Net cash from operating activities",
         {"FY2025": 7017191, "FY2024": 4690772, "FY2023": 3142548, "FY2022": 413627, "FY2021": 1683715,
          "FY2020": 453624, "FY2019": 439707, "FY2018": 19481, "FY2017": -13651}),
        ("Net cash used in investing activities",
         {"FY2025": -15684, "FY2024": -24096, "FY2023": -21778, "FY2022": -8144, "FY2021": -8624,
          "FY2020": -8448, "FY2019": -8835, "FY2018": -8887, "FY2017": -5670}),
        ("Net cash from/(used in) financing activities",
         {"FY2025": -1603, "FY2024": 33433, "FY2023": 9537, "FY2022": -384, "FY2021": 32492,
          "FY2020": 41462, "FY2019": 33195, "FY2018": 24871, "FY2017": 27908}),
        ("Cash and cash equivalents at end of year",
         {"FY2025": 17956976, "FY2024": 10961293, "FY2023": 6256126, "FY2022": 3125862, "FY2021": 2720797,
          "FY2020": 1013224, "FY2019": 526594, "FY2018": 62527, "FY2017": 27062}),
    ],
    cash_flow_unit="£'000",
    ratios=[
        ("CET1 Ratio", CET1_RATIO),
        ("Leverage Ratio", LEVERAGE),
        ("LCR", LCR),
    ],
    note="Figures are duplicated from the detail sheets for at-a-glance trend viewing; see each sheet's own "
         "source citation for the underlying document/page. Statement of Changes in Equity Summary: FY2024's "
         "Opening equity is a new ultimate parent entity's own balance (ClearBank Group Holdings Limited, "
         "inserted above ClearBank Limited during FY2024), not a continuation of FY2023's Closing equity - "
         "see the Statement of Changes in Equity sheet for the full entity-change note. NSFR omitted from this chart (values in the "
         "thousands of percent would flatten every other series) - see the NSFR sheet directly. "
         "HD-019: this workbook's year range now extends back to FY2017, ClearBank's independently-verified "
         "floor (first year with any customer deposits/income, following the bank's actual opening to "
         "customers in October 2017) - not FY2015, which an earlier ticket-generation pass had assumed "
         "purely from the entity's GLEIF incorporation date. See the HD-019 FLOOR VERIFICATION comment "
         "block near the top of build_clearbank.py and the Balance Sheet sheet's Sources note for the "
         "full evidence trail.",
)

bw.save("/Users/armaan/code/katalysis/banks/CLEARBANK FINANCIALS.xlsx")
