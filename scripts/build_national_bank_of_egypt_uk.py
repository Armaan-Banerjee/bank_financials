import os
import sys
sys.path.insert(0, os.path.dirname(__file__))
from bank_workbook import BankWorkbook

YEARS = ["FY2025", "FY2024", "FY2023", "FY2022", "FY2021"]

AR = {
    "FY2025": "https://find-and-update.company-information.service.gov.uk/company/02743734/filing-history/MzU0MDExNTA0NGFkaXF6a2N4/document?format=pdf&download=0",
    "FY2024": "https://find-and-update.company-information.service.gov.uk/company/02743734/filing-history/MzQ2Mjk2OTExMGFkaXF6a2N4/document?format=pdf&download=0",
    "FY2023": "https://find-and-update.company-information.service.gov.uk/company/02743734/filing-history/MzQxOTgxMTA0NmFkaXF6a2N4/document?format=pdf&download=0",
    "FY2022": "https://find-and-update.company-information.service.gov.uk/company/02743734/filing-history/MzM5NDYwNDY2OGFkaXF6a2N4/document?format=pdf&download=0",
    "FY2021": "https://find-and-update.company-information.service.gov.uk/company/02743734/filing-history/MzM1MTQyMDQxMmFkaXF6a2N4/document?format=pdf&download=0",
}
P3 = {
    "FY2024": "https://www.nbeuk.com/wp-content/uploads/2025/04/Pillar-3-Disclosures-31st-December-2024.pdf",
    "FY2023": "https://www.nbeuk.com/wp-content/uploads/2024/09/Pillar-3-Disclosures-31st-December-2023-FINAL.pdf",
    "FY2022": "https://www.nbeuk.com/wp-content/uploads/2023/10/NBE-UK-Pillar-3-31-December-2022-approved.pdf",
    "FY2021": "https://www.nbeuk.com/wp-content/uploads/2023/05/Pillar-3-31-December-2021-approved.pdf",
}

ENTITY = (
    "ENTITY NOTE: National Bank of Egypt (UK) Limited (Companies House 02743734, FRN 204520, LEI "
    "2TV5CTDU7ZDMT8HL5F58) matches Banks List 2608.xlsx and Companies House. It is a UK-incorporated, "
    "wholly owned subsidiary of National Bank of Egypt. The accounts contain a full entity-level cash-flow "
    "statement. The annual reports and Pillar 3 documents are image-only or mixed scans for the older years; "
    "figures were OCR'd and checked against the following year's comparative columns where available. "
    "Pillar 3 is annual: no defensible entity-level interim disclosure was located, so this is a 13-sheet workbook."
)

def sources(kind):
    if kind == "cash":
        return ("Sources - National Bank of Egypt (UK) Limited entity-level Cash Flow Statement, £:\n" +
                "\n".join(f"{y}: Companies House Annual Report for {y[2:]}, Cash Flow Statement - {AR[y]}" for y in YEARS) +
                "\n\nFY2021/FY2022 are condensed cash-flow presentations in the filed accounts; the reported subtotals and opening/closing cash chain are preserved.\n\n"
                "CORRECTION (2026-08-29 correctness sweep): the original transcription omitted a real, separately-disclosed "
                "'Effect of foreign exchange rate changes' line that sits between the opening and closing cash balances in the "
                "FY2023, FY2024, and FY2025 filings' own Cash Flow Statements (FY2025 Annual Report p.41; FY2023 Annual Report p.39, "
                "restated FY2022 comparative). Without it, the opening + net change chain did not tie to the printed closing balance "
                "for those 3 years (confirmed by re-reading each source page directly): FY2023 -18,919,972; FY2024 +3,491,832; FY2025 "
                "-15,465,348. Added as its own line; the chain now reconciles exactly for FY2023-FY2025. FY2021/FY2022 needed no change "
                "- their condensed presentation already embeds this effect within operating activities, and the chain already tied.\n\n"
                + ENTITY)
    return ("Sources - National Bank of Egypt (UK) Limited entity-level Pillar 3 / regulatory capital disclosures, £000 unless stated:\n" +
            "\n".join(f"{y}: annual Pillar 3 disclosure, UK KM1 / capital adequacy table - {P3[y]}" for y in ["FY2021", "FY2022", "FY2023", "FY2024"]) +
            "\nFY2025: no 2025 Pillar 3 disclosure located as of this build; values left blank rather than estimated.\n\n" + ENTITY)

bw = BankWorkbook("National Bank of Egypt (UK) Limited", YEARS, header_color="7B2D26")

rows = [
    ("SECTION", "Operating activities", {}),
    ("TOTAL", "Net cash generated/(used) from operating activities", {"FY2025":101280910,"FY2024":-44497653,"FY2023":-110688337,"FY2022":-91172027,"FY2021":5256681}),
    ("SECTION", "Investing activities", {}),
    ("TOTAL", "Net cash generated/(used) from investing activities", {"FY2025":-122997984,"FY2024":21089132,"FY2023":-16905485,"FY2022":83292813,"FY2021":-5782456}),
    ("SECTION", "Financing activities", {}),
    ("TOTAL", "Net cash generated/(used) in financing activities", {"FY2025":27813180,"FY2024":-2299886,"FY2023":-4776099,"FY2022":-2491694,"FY2021":0}),
    ("TOTAL", "Net decrease/(increase) in cash and cash equivalents", {"FY2025":6096106,"FY2024":-25708407,"FY2023":-132369921,"FY2022":-10370908,"FY2021":-525775}),
    ("DATA", "Cash and cash equivalents at the beginning of year", {"FY2025":286126277,"FY2024":308342852,"FY2023":459632745,"FY2022":53727035,"FY2021":54252810}),
    ("DATA", "Effect of foreign exchange rate changes", {"FY2025":-15465348,"FY2024":3491832,"FY2023":-18919972}),
    ("TOTAL", "Cash and cash equivalents at the end of year", {"FY2025":276757036,"FY2024":286126277,"FY2023":308342852,"FY2022":43356127,"FY2021":53727035}),
]
bw.add_cash_flow_sheet("National Bank of Egypt (UK) Limited — Cash Flow Statement", "Entity-level basis, £", rows, sources("cash"), first_col_width=65, source_height=190, unit_suffix=" (£)")

def metric(name, unit, label, data, note=None):
    bw.add_metric_sheet(name, unit, [(label, data)], sources("p3"), note=note, first_col_width=48, source_height=170)

metric("CET1 Capital", "£000", "CET1 / Tier 1 capital", {"FY2024":170750,"FY2023":166857,"FY2022":160206,"FY2021":154505}, "FY2021–FY2022 source tables report Tier 1 capital; no AT1 instruments are disclosed, so it is used as CET1. FY2025 not disclosed.")
metric("CET1 Ratio", "%", "CET1 ratio", {"FY2024":"16.31%","FY2023":"17.3%","FY2022":"16.8%"}, "FY2021 standalone CET1 ratio was not separately stated and is left blank rather than substituting the reported leverage ratio.")
metric("Tier 1 Capital", "£000", "Tier 1 capital", {"FY2024":170750,"FY2023":166857,"FY2022":160206,"FY2021":154505})
metric("Tier 1 Ratio", "%", "Tier 1 ratio", {"FY2024":"16.31%","FY2023":"17.3%","FY2022":"16.8%"}, "FY2021 standalone Tier 1 ratio was not separately stated; the reported 12.47% leverage ratio is kept only on the Leverage Ratio sheet.")
metric("Total Capital", "£000", "Total capital resources", {"FY2024":201853,"FY2023":197905,"FY2022":195475,"FY2021":187789})
metric("Total Capital Ratio", "%", "Total capital ratio / capital adequacy ratio", {"FY2024":"19.28%","FY2023":"20.6%","FY2022":"20.54%","FY2021":"15.15%"}, "The older reports label this capital adequacy/total capital ratio and use their stated regulatory denominator; values are not recalculated.")
metric("Total RWAs", "£000", "Total risk-weighted exposure amount / RWA", {"FY2024":1047061,"FY2023":962119,"FY2022":906134,"FY2021":779381})
metric("Leverage Ratio", "%", "Leverage ratio", {"FY2024":"11.6%","FY2023":"12.1%","FY2022":"11.65%","FY2021":"12.47%"})
metric("LCR", "%", "Liquidity coverage ratio (average)", {"FY2024":"418%","FY2023":"387%","FY2022":"296%"}, "FY2021 average LCR was not quantified in the located disclosure; FY2025 has no Pillar 3 edition.")
metric("NSFR", "%", "Net stable funding ratio (average)", {"FY2024":"194%","FY2023":"176%","FY2022":"135%"}, "FY2021 NSFR was not quantified in the located disclosure; FY2025 has no Pillar 3 edition.")
bw.add_not_disclosed_metric_sheets(["MREL Ratio"], sources("p3"), per_note={"MREL Ratio": "No MREL ratio was disclosed in the located annual Pillar 3 documents."})

bw.add_overview_sheet(
    cash_flow_totals=[
        ("Net cash generated/(used) from operating activities", {"FY2025":101280910,"FY2024":-44497653,"FY2023":-110688337,"FY2022":-91172027,"FY2021":5256681}),
        ("Net cash generated/(used) from investing activities", {"FY2025":-122997984,"FY2024":21089132,"FY2023":-16905485,"FY2022":83292813,"FY2021":-5782456}),
        ("Net cash generated/(used) in financing activities", {"FY2025":27813180,"FY2024":-2299886,"FY2023":-4776099,"FY2022":-2491694,"FY2021":0}),
        ("Cash and cash equivalents at end of year", {"FY2025":276757036,"FY2024":286126277,"FY2023":308342852,"FY2022":43356127,"FY2021":53727035}),
    ], cash_flow_unit="£", ratios=[
        ("CET1 Ratio", {"FY2024":"16.31%","FY2023":"17.3%","FY2022":"16.8%"}),
        ("Total Capital Ratio", {"FY2024":"19.28%","FY2023":"20.6%","FY2022":"20.54%","FY2021":"15.15%"}),
        ("Leverage Ratio", {"FY2024":"11.6%","FY2023":"12.1%","FY2022":"11.65%","FY2021":"12.47%"}),
        ("LCR", {"FY2024":"418%","FY2023":"387%","FY2022":"296%"}),
    ], note=ENTITY)
bw.save("/Users/armaan/code/katalysis/banks/NATIONAL BANK OF EGYPT UK FINANCIALS.xlsx")
print("Saved.")
