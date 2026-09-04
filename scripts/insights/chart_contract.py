"""Small, serialisable contracts shared by chart renderers.

Analysis modules remain responsible for statistics and filtering. This module
only normalises already-computed observations into a renderer-neutral shape so
HTML, PDF, and a future Chart.js adapter can consume the same inputs.
"""

from math import isfinite
from pathlib import Path


SCHEMA_VERSION = 1
LOCAL_CHART_RUNTIME_VERSION = "0.1.0"
CHARTJS_VERSION = "4.5.0"
CHARTJS_BUNDLE = Path(__file__).resolve().parents[2] / "vendor" / "chartjs" / "chart.umd.min.js"


def load_chartjs_bundle():
    """Load the pinned local Chart.js UMD bundle for the single-file output."""
    if not CHARTJS_BUNDLE.is_file():
        raise FileNotFoundError(f"missing pinned Chart.js bundle: {CHARTJS_BUNDLE}")
    return CHARTJS_BUNDLE.read_text(encoding="utf-8")


LOCAL_CHART_RUNTIME = r'''/* Katalysis Charts 0.1.0 — Chart.js adapter and lifecycle wrapper. */
(function(global){
  const mounted=new Map();
  const palette=["#1f5f8b","#b94c42","#2f8f9d","#b87916","#6d597a","#4f772d","#577590","#bc6c25"];
  const destroy=element=>{if(!element)return;const chart=mounted.get(element);if(chart){chart.destroy();if(chart.canvas)chart.canvas.remove()}mounted.delete(element);element.removeAttribute("data-chart-runtime")};
  const mount=(element,spec)=>{if(!element||!spec||typeof global.Chart!=="function")return null;destroy(element);const canvas=document.createElement("canvas");canvas.setAttribute("role","img");canvas.setAttribute("aria-label",spec.accessibility?.aria_label||spec.title||"Chart");element.prepend(canvas);const x=spec.dimensions.x,y=spec.dimensions.y;const chart=new global.Chart(canvas,{type:"line",data:{datasets:spec.series.map((series,index)=>({label:series.label,data:series.points.filter(point=>point.y!==null),borderColor:palette[index%palette.length],backgroundColor:palette[index%palette.length],pointRadius:1.8,pointHoverRadius:4,borderWidth:1.25,tension:0,spanGaps:false,parsing:false}))},options:{responsive:true,maintainAspectRatio:false,animation:false,interaction:{mode:"nearest",intersect:false},plugins:{legend:{position:"bottom",labels:{usePointStyle:true,boxWidth:7,filter:(item,data)=>!data.datasets[item.datasetIndex].hidden}},title:{display:true,text:spec.title},tooltip:{callbacks:{title:items=>{const point=items[0]?.raw;return point?`${x.labels?.[point.x]||`FY${point.x}`}`:""},label:item=>`${item.dataset.label}: ${item.raw.y} ${y.unit||""}`}}},scales:{x:{type:"linear",min:x.values[0],max:x.values[x.values.length-1],title:{display:true,text:x.label},ticks:{stepSize:1,callback:value=>x.labels?.[value]||`FY${value}`}},y:{title:{display:true,text:y.label},min:y.domain[0],max:y.domain[1],reverse:y.unit==="rank"}}}});element.dataset.chartRuntime="chartjs-4.5.0";element.setAttribute("data-chart-id",String(spec.id||""));element.querySelectorAll("svg").forEach(svg=>{svg.setAttribute("aria-hidden","true");svg.style.display="none"});const resetButton=element.parentElement?.querySelector('.in024-reset-zoom[data-chart="'+spec.id+'"]');if(resetButton)resetButton.addEventListener("click",()=>reset(element));mounted.set(element,chart);return chart};
  const observe=(root=document)=>root.querySelectorAll("[data-chart-contract]").forEach(element=>{try{mount(element,JSON.parse(element.dataset.chartContract))}catch(error){element.dataset.chartRuntimeError="invalid-chart-contract";element.setAttribute("title","Chart data is unavailable");}});
  const reset=element=>{const chart=mounted.get(element);if(!chart)return;const spec=JSON.parse(element.dataset.chartContract),x=spec.dimensions.x,y=spec.dimensions.y;chart.options.scales.x.min=x.values[0];chart.options.scales.x.max=x.values[x.values.length-1];chart.options.scales.y.min=y.domain[0];chart.options.scales.y.max=y.domain[1];chart.reset();chart.update("none")};
  const fitYAxis=(chart,spec)=>{const values=chart.data.datasets.filter(dataset=>!dataset.hidden).flatMap(dataset=>dataset.data.map(point=>point.y));if(!values.length)return;const low=Math.min(...values),high=Math.max(...values),padding=(high-low)*.08||.5;chart.options.scales.y.min=spec.dimensions.y.unit==="rank"?spec.dimensions.y.domain[0]:low-padding;chart.options.scales.y.max=spec.dimensions.y.unit==="rank"?spec.dimensions.y.domain[1]:high+padding};
  const refresh=()=>{const active=new Set([...document.querySelectorAll(".in024-shared-bank-toggle:checked")].map(item=>item.value));document.querySelectorAll("[data-chart-contract]").forEach(element=>{const chart=mounted.get(element);if(chart){chart.data.datasets.forEach(dataset=>{dataset.hidden=!active.has(dataset.label)});fitYAxis(chart,JSON.parse(element.dataset.chartContract));chart.update("none")}})};
  global.KatalysisCharts={version:"0.1.0",chartjsVersion:"4.5.0",mount,observe,destroy,reset,refresh};
  document.addEventListener("change",event=>{if(event.target.matches?.(".in024-shared-bank-toggle"))refresh()});
  global.addEventListener("wheel",event=>{const element=event.target.closest?.("[data-chart-contract]");const chart=element&&mounted.get(element);if(!chart)return;event.preventDefault();const spec=JSON.parse(element.dataset.chartContract),x=chart.scales.x,originalMin=spec.dimensions.x.values[0],originalMax=spec.dimensions.x.values.at(-1),originalRange=originalMax-originalMin,currentRange=x.max-x.min,factor=event.deltaY>0?1.2:.8,nextRange=Math.max(1,Math.min(originalRange,currentRange*factor)),rect=chart.canvas.getBoundingClientRect(),pointer=x.getValueForPixel(event.clientX-rect.left),centre=Math.max(x.min,Math.min(x.max,pointer)),fraction=currentRange?Math.max(0,Math.min(1,(centre-x.min)/currentRange)):.5,nextMin=Math.max(originalMin,Math.min(originalMax-nextRange,centre-nextRange*fraction)),nextMax=nextMin+nextRange,values=chart.data.datasets.filter(dataset=>!dataset.hidden).flatMap(dataset=>dataset.data.filter(point=>point.x>=nextMin&&point.x<=nextMax).map(point=>point.y));if(values.length){const low=Math.min(...values),high=Math.max(...values),padding=(high-low)*.08||.5;chart.options.scales.y.min=spec.dimensions.y.unit==="rank"?spec.dimensions.y.domain[0]:low-padding;chart.options.scales.y.max=spec.dimensions.y.unit==="rank"?spec.dimensions.y.domain[1]:high+padding}chart.options.scales.x.min=nextMin;chart.options.scales.x.max=nextMax;chart.update("none")},{passive:false});
})(window);'''


def _number(value):
    if value is None:
        return None
    number = float(value)
    return number if isfinite(number) else None


def _domain(values):
    numeric = [value for value in values if value is not None]
    if not numeric:
        return [0.0, 1.0]
    low, high = min(numeric), max(numeric)
    if low == high:
        padding = max(abs(low) * 0.05, 1.0)
    else:
        padding = (high - low) * 0.05
    return [low - padding, high + padding]


def build_line_chart_spec(chart_id, title, unit, records, years, description=None):
    """Return a deterministic line-chart specification from trajectory rows.

    ``records`` is the existing IN-024 shape: each row has ``bank`` and a
    ``years`` list containing ``year`` and ``value``. Missing values are
    retained as nulls so renderers can break lines instead of implying zero.
    """
    clean_years = sorted({int(year) for year in years})
    series = []
    for record in sorted(records, key=lambda item: str(item["bank"]).casefold()):
        by_year = {int(point["year"]): _number(point.get("value"))
                   for point in record.get("years", [])}
        series.append({
            "id": str(record["bank"]),
            "label": str(record["bank"]),
            "points": [{"x": year, "y": by_year.get(year)} for year in clean_years],
        })
    values = [point["y"] for item in series for point in item["points"]]
    return {
        "schema_version": SCHEMA_VERSION,
        "id": str(chart_id),
        "title": str(title),
        "dimensions": {
            "x": {"field": "x", "label": "Fiscal year", "values": clean_years},
            "y": {"field": "y", "label": str(unit), "unit": str(unit), "domain": _domain(values)},
        },
        "series": series,
        "accessibility": {
            "role": "img",
            "aria_label": description or f"{title} by fiscal year",
            "table_columns": ["Bank", "Fiscal year", str(unit)],
        },
    }


def build_rank_chart_spec(chart_id, title, records, start_label, end_label, n):
    """Build a two-point Chart.js line spec for a fixed-panel rank chart."""
    series = [{"id": str(record.get("bank", record["frn"])),
               "label": str(record.get("bank", record["frn"])),
               "points": [{"x": 0, "y": int(record["start_rank"])},
                          {"x": 1, "y": int(record["end_rank"])}]}
              for record in sorted(records, key=lambda item: str(item.get("bank", item["frn"])).casefold())]
    return {"schema_version": SCHEMA_VERSION, "id": str(chart_id), "title": str(title),
            "dimensions": {"x": {"field": "x", "label": "Panel year", "values": [0, 1],
                                   "labels": [str(start_label), str(end_label)]},
                           "y": {"field": "y", "label": "Rank (1 = highest)", "unit": "rank",
                                 "domain": [1, max(2, int(n))]}},
            "series": series,
            "accessibility": {"role": "img", "aria_label": f"{title} rank mobility",
                               "table_columns": ["Bank", str(start_label), str(end_label)]}}


def validate_chart_spec(spec):
    """Raise ``ValueError`` when a chart contract is incomplete or malformed."""
    required = {"schema_version", "id", "title", "dimensions", "series", "accessibility"}
    missing = required - set(spec)
    if missing:
        raise ValueError(f"chart spec missing keys: {sorted(missing)}")
    if spec["schema_version"] != SCHEMA_VERSION:
        raise ValueError(f"unsupported chart schema: {spec['schema_version']}")
    x_values = spec["dimensions"]["x"]["values"]
    if x_values != sorted(set(x_values)):
        raise ValueError("chart x values must be sorted and unique")
    low, high = spec["dimensions"]["y"]["domain"]
    if not low < high:
        raise ValueError("chart y domain must have positive width")
    for series in spec["series"]:
        if len(series["points"]) != len(x_values):
            raise ValueError(f"series {series['id']!r} does not cover every x value")
        if any(point["x"] != x for point, x in zip(series["points"], x_values)):
            raise ValueError(f"series {series['id']!r} has inconsistent x values")
    return spec
