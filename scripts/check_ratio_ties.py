#!/usr/bin/env python3
"""Free check nobody performs: does a printed capital RATIO tie to the printed
CAPITAL and RWA on the same workbook's other sheets, for the same year?

verify_workbook.py cross-checks KM1 against the metric sheets (agreement, not
correctness) and reconciles DATA->TOTAL blocks. It never divides one
single-metric sheet by another. audit_gaps.py counts cells. So a ratio that
contradicts its own numerator and denominator passes everything.

REPORTS LEADS, NOT VERDICTS. A break can be (a) a transcription error, (b) the
bank printing an inconsistent set, (c) a scale/currency mismatch between the
two sheets, (d) a ratio struck on a different denominator (transitional vs
fully-loaded, or a different entity). Only the documents separate them.

KNOWN LIMITATION, stated so nobody reads past it: `firstvals` takes the FIRST
non-empty cell in each year column, which assumes the sheet's first data row
carries the figure. That holds for the single-metric sheets this scans, but a
sheet whose first row is a caption or a "not disclosed" statement will be read
wrong or skipped. The `skipped` count in the summary is part of the result -
a run that skips heavily is reporting its own reach, not a clean corpus.

Worked example of a REAL break that is nobody's error (Bank of Africa UK
FY2019, 2026-09-18): the source's own "Capital management" table prints Own
funds 81,016 - which ties exactly to Tier 1 65,965 + subordinated debt 15,051 -
while its printed 17.36% solvency ratio is struck on Required capital 69,046 +
Surplus capital 12,506 = 81,552. Both figures are correctly transcribed and the
document disagrees with itself. That case is DOCUMENTED in the sheet note, not
resolved by picking a side, and it is the treatment any break here should
default to until a document says otherwise.
"""
import glob, os, re, sys, openpyxl

PAIRS = [("CET1 Capital","CET1 Ratio"),("Tier 1 Capital","Tier 1 Ratio"),
         ("Total Capital","Total Capital Ratio")]
RWA = "Total RWAs"
THRESH = float(sys.argv[1]) if len(sys.argv)>1 else 0.10   # percentage points

def firstvals(ws):
    """year -> first non-empty cell in that year's column."""
    hdr=[c.value for c in ws[3]]
    cols={}
    for i,h in enumerate(hdr):
        if i==0 or not h: continue
        m=re.findall(r"FY(\d{4})", str(h))
        if m: cols[m[-1]]=i
    out={}
    for y,ci in cols.items():
        for r in ws.iter_rows(min_row=4,values_only=True):
            if ci<len(r) and r[ci] not in (None,""):
                out[y]=r[ci]; break
    return out

def num(v):
    if isinstance(v,(int,float)): return float(v)
    if isinstance(v,str):
        s=v.strip().replace(",","").replace("%","").replace("£","").replace("$","")
        try: return float(s)
        except ValueError: return None
    return None

rows=[]; skipped=0; banks=0
for p in sorted(glob.glob("banks/*FINANCIALS.xlsx")):
    bank=os.path.basename(p).replace(" FINANCIALS.xlsx","")
    try: wb=openpyxl.load_workbook(p,read_only=True,data_only=True)
    except Exception: continue
    banks+=1
    if RWA not in wb.sheetnames: wb.close(); continue
    rwa=firstvals(wb[RWA])
    for cap_s,rat_s in PAIRS:
        if cap_s not in wb.sheetnames or rat_s not in wb.sheetnames: continue
        cap=firstvals(wb[cap_s]); rat=firstvals(wb[rat_s])
        for y in sorted(set(cap)&set(rat)&set(rwa),reverse=True):
            c,r,w = num(cap[y]), num(rat[y]), num(rwa[y])
            if None in (c,r,w) or w==0 or r is None:
                skipped+=1; continue
            comp = c/w*100
            if not (0.01 < comp/max(r,1e-9) < 100):   # gross scale mismatch
                skipped+=1; continue
            d=abs(comp-r)
            if d>THRESH:
                rows.append((d,bank,y,cap_s,c,w,comp,r))
    wb.close()

rows.sort(reverse=True)
print(f"scanned {banks} workbooks; {len(rows)} ratio(s) break by >{THRESH}pp; "
      f"{skipped} comparisons skipped (missing/unparseable/scale-mismatch)\n")
print(f"{'break':>7}  {'bank':<34} {'year':<6} {'sheet':<16} {'capital':>12} {'RWA':>12} {'computed':>9} {'printed':>8}")
for d,bank,y,sh,c,w,comp,r in rows:
    print(f"{d:6.2f}pp  {bank:<34} FY{y}   {sh:<16} {c:12,.0f} {w:12,.0f} {comp:8.2f}% {r:7.2f}%")
