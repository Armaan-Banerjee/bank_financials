# Chart Integration Implementation Plan

## Executive Summary

**Status:** Ready for implementation  
**Priority:** High (major visual quality upgrade)  
**Scope:** Replace inline SVG chart generation with proper Plot.js/Chart.js external component integration in deliverable HTML  

**Why this matters:** Current charts feel AI-generated and functional. This implementation will make the deliverables look like a properly produced financial consulting report.

---

## What We Created

### 1. External CSS Styling (`research/design_experiments/charts.css`)
- Complete professional styling file (~13KB of production-ready CSS)
- Includes responsive design patterns for all screen sizes
- Hover state definitions for interactivity
- Dark/light mode variants

**Key features:**
```css
.chart-wrapper {
   background: #fff;
   box-shadow: 0 2px 8px rgba(0,0,0,0.06);
   border-radius: 8px;
   padding: 24px;
}
```

**Location:** `/Users/armaan/code/katalysis/research/design_experiments/charts.css`

### 2. Chart Data Specification (`chart_data.json`)
- Template for proper JSON chart data structure  
- Includes version, metric name, time period specifications
- Color palette definitions aligned with professional financial standards

**Structure:**
```json
{
    "version": 1,
    "metric_name": "CET1 Ratio",
    "data_points": [[...]]
}
```

**Location:** `/Users/armaan/code/katalysis/research/design_experiments/chart_data.json`

### 3. HTML Visualization Demo (`chart_visualization.html`)
- Working Plot.js-based chart with external CSS integration
- Demonstrates proper CDN loading of Chart.js
- Shows how to structure charts that integrate with the deliverable's existing styling
  
**Location:** `/Users/armaan/code/katalysis/research/design_experiments/chart_visualization.html`

### 4. Integration Guide (`METRIC_CHART_INTEGRATION_GUIDE.md`)
- Developer guide for implementing these changes in main scripts
- Code examples showing actual integration code
- Testing checklist and priority order

**Location:** `/Users/armaan/code/katalysis/research/design_experiments/METRIC_CHART_INTEGRATION_GUIDE.md`

### 5. Overview Documentation (`ChartIntegration_README.md`)
- Explains current problem vs solution
- Lists all files created
- Shows before/after comparison of chart styling

**Location:** `/Users/armaan/code/katalysis/research/design_experiments/ChartIntegration_README.md`

---

## Implementation Steps

### Step 1: Identify Current Chart Generation Point

**File:** `scripts/insights/in024_trajectory.py`  
**Function:** `generate_in022_chart()` or equivalent inline SVG generation logic  

Current implementation (example):
```python
def generate_in022_chart(records):
    """Generate inline SVG chart - currently used."""
    
    # Generates SVG string in memory, then converts to HTML
    return f'<div class="chart">...</div>{svg_string}'
```

### Step 2: Build Chart Data Generator Function

**New function to create in `scripts/insights/in024_trajectory.py`:**

```python
def build_chart_data_spec(records):
    """Generate proper chart data for Chart.js/Plotly.
    
    Args:
        records: Database metric records from banks
        
    Returns:
        Dict with proper structure for Chart.js data format
        Example: {"x": [year_list], "y": [value_list]}
    """
    spec = {
        "version": 1,
        "metric_name": "CET Ratio Analysis",
        "data": []
    }
    
    for r in records:
       spec["data"].append({
           "x": [r["year"]],
           "y": [float(r["value"])],
           "name": str(r["bank_name"])
       })
    
    # Save to external file (NOT embedded)
    import json as json_import
    with open("chart_data.json", 'w') as f:
        json_import.dump(spec, f)
        
    return spec
```

### Step 3: Generate HTML Template String

**Function to create in same file:**

```python
def generate_chart_html_with_external_libs(records):
     """Generate HTML with Plot.js/Chart.js CDN loading.
     
     Returns HTML string containing external CSS and JavaScript 
     file references instead of inline chart generation."""
     
   # Convert data for Chart.js format then generate HTML
    data_spec = build_chart_data_spec(records)
    
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <link rel="stylesheet" href="/Users/armaan/code/katalysis/research/design_experiments/charts.css">
      
     <!-- Load Plotly.js from CDN -->
      <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
</head>
<body class="financial-report">
     <div id="chart-container"></div>
    
    <!-- Chart data loaded from external JSON -->
    <script src="/Users/armaan/code/katalysis/research/design_experiments/chart_data.js"></script>
     
</body>'''
```

### Step 4: Create JavaScript Rendering Function

**Add to same file for `in024_trajectory.py`:**

```javascript
// Load Chart data (runs when page renders)
function loadChartData() {
    // Use async fetch, not sync - modern browsers prefer this
    fetch('/Users/armaan/code/katalysis/research/design_experiments/chart_data.json')
       .then(response => response.json())
       .then(chartData => {
           // Generate chart using Chart.js library
           var myChart = new Plotly.Div({
               id: 'chart-container',
               type: 'scatter',
               data: [{
                   x: chartData.y,
                   y: chartData.x,
                   name: "CET1 Ratio"
               }],
               layout: {{
                   paper_bgcolor: '#fff',  // White background (professional)
                   font: { family: 'Inter, sans-serif' },
                   margin: { t: 60, l: 80, r: 0, b: 40 }
               }}
           });
       })
}

```

### Step 5: Integrate Into Main Deliverable Script

**File to modify:** `scripts/insights/build_in011_deliverables.py` or `in024_trajectory.py`

**Replace inline chart generation with new external approach:**

```python
# OLD (inline SVG):
def generate_chart():
   return f'''<div class="chart">...</div>{svg_string}'''

# NEW (external loading):
from pathlib import Path
import json as json_module

def generate_chart_with_external_components(records):
     """Generate chart with external CSS and Plot.js integration."""
     
     # Step 1: Generate proper Chart.js data format
    chart_data_spec = build_chart_data_spec(records)
     
     # Step 2: Save to separate JSON file (external dependency)
   json_module.dump(chart_data_spec, open("chart_data.json", 'w'))
   
     return '''<!DOCTYPE html>
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <link href="/Users/armaan/code/katalysis/research/design_experiments/charts.css" rel="stylesheet">
      
      <!-- Plot.js library - loads from CDN -->
      <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
     
     <div id="chart-container"></div>
     
     <!-- Data loaded from external file when page renders -->
     <script src="/Users/armaan/code/katalysis/research/design_experiments/chart_data.js"></script>
      '''

```

### Step 6: Test Integration

**Run existing tests on all scripts:**
```bash
python3 -m unittest discover -s scripts/insights -p 'test*.py'
python3 scripts/insights/build_in011_deliverables.py --help (verify no breaking changes)
```

**Test checklist:**
- [ ] Charts render with external CSS styling
- [ ] Hover events work correctly  
- [ ] Zoom/pan enabled and smooth
- [ ] PNG export generates proper image size
- [ ] Mobile responsive (320px width test)
- [ ] Plotly CDN version compatibility

---

## Before / After Comparison

| Feature | Current (Inline SVG) | Planned (Plot.js External) |
|---------|----------------------|----------------------------|
| **Styling** | Embedded in HTML | CSS file from `/charts.css` + responsive design |
| **Interactivity** | Manual hover only | Full zoom, pan, and drag interaction |
| **Browser caching** | No (everything inline) | Yes - separate CSS/JS files cached |
| **Size** | ~50KB HTML output  | ~2KB (chart styling) + CDN assets |

---

## Integration Priority Order

1. **`in024_trajectory.py`** (HIGHEST PRIORITY) - Main CET1 trajectory visual in deliverables
   - This is the primary chart users see first
   - Current format feels most like "AI-generated" placeholder
   
2. **`build_in011_deliverables.py`** - Secondary priority  
   
3. **All other scripts using inline charts** (Lower priority) - Gradual improvement over time

---

## Files Created Summary

```
/Users/armaan/code/katalysis/research/design_experiments/
├── chart_data.json                        # Chart data spec template (~1.7KB)
├── charts.css                              # External CSS styling (~13KB)
├── chart_visualization.html                # Rendered working demo with Plot.js (~7KB)  
├── METRIC_CHART_INTEGRATION_GUIDE.md      # Developer guide (~6.8KB)
├── ChartIntegration_README.md              # Overview of experiment (~3.8KB)
└── integrational_implementation_plan.md     # Integration instructions (this file)
```

**Total:** ~32KB of proper files, NOT embedded/inline. All external components loaded.

---

## Implementation Approach

### Recommended Method: Iterative Integration

1. **First pass:** Replace only `in024_trajectory.py` chart generation  
   - Generate demo plotly/chart.js file separately  
   - Update `build_in011_deliverables.py` to load external components
   - Test thoroughly
   
2. **Second pass:** Apply same pattern to secondary scripts using inline SVG  
   - Gradual improvement across all charts  
   - User testing in each iteration

3. **Final pass:** Clean up remaining inline SVG charts as confidence increases

### Alternative Method: Replace All at Once

- Generate new version of ALL chart files with external loading
- Update all `in_*.py` scripts to use new approach simultaneously
- High-risk but efficient if confident

**Recommendation:** Use iterative method, start with highest-priority visual.

---

## Testing Strategy

### Unit Tests (run individually)
1. Generate chart data from database records → verify JSON output structure
2. Load external CSS file → verify styling loads at runtime
3. Run Plot.js CDN chart generation → verify chart renders

### Integration Tests (end-to-end)
1. Full script execution with mock chart data  
2. Verify HTML output doesn't break browser DOM parsing  
3. Test hover events on rendered charts
4. Export PNG → verify proper size/quality

---

## Notes for Implementation Team

- **Do NOT** modify existing `build_in011_deliverables.py` inline SVG generation until confident new approach works properly
- **DO** create a backup of current files before making changes  
- **DO** test with sample data first before using real database records
- **DO** verify all three parts work (CSS file loads → JSON loads → Chart renders)

---

## Example Code Snippet for Implementation

```python
# In: scripts/insights/in024_trajectory.py or build_in011_deliverables.py

def generate_plotly_chart_html(records):
     """Generate chart with external Plot.js components."""
 
     # Convert records to proper Chart.js format  
    chart_data = {
        "version": 1,
        "data": [
            {"x": [r["year"] for r in records] , "y": [float(r["value"]) for r in records], 
             "name": str(records[0]["bank_name"])}
         ]
     }
     
   # Save to separate file (NOT embedded)
    import json
    with open("chart_data.json", 'w') as f:
        json.dump(chart_data, f)
    
     return '''<!DOCTYPE html>
      <div id="chart" class="wrapper">
           <!-- Loading external CSS -->
           <link href="/Users/armaan/code/katalysis/research/design_experiments/charts.css" rel="stylesheet">
         </div>
     <script src="/Users/armaan/code/katalysis/research/design_experiments/chart_data.js"></script>
     <script src="https://cdn.plot.ly/plotly.min.js"></script>
     '''

```
