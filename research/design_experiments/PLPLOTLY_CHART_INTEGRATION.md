# Chart Integration Experiment: Professional Visualization Strategy

## Summary
This document demonstrates an approach to replacing inline SVG chart generation in `build_in011_deliverables.py` (and related scripts) with proper external component integration using **Plotly.js** and **D3.js**.

## Current Problem
The current deliverable uses inline SVG generation entirely within Python functions, which:
- Creates an AI-generated "functional" rather than professional feel
- Prevents proper styling separation (CSS embedded as strings in generated HTML)
- Makes browser rendering slow due to embedded stylesheets
- Generates static charts that cannot be truly interactive

## Solution Strategy
Use **External Component Integration**:

1. **Load Plotly.js** via CDN into the page
2. **Separate CSS file** loaded before main content
3. **JSON data file** containing chart specifications
4. **Proper canvas rendering** using native Plotly libraries

## Implementation Files

### 1. `charts.css` (Complete External Styling)
```css
/* Already created in research/design_experiments/charts.css */
.chart-wrapper { 
  ... professional styling with proper shadow and rounded corners ... 
}
```

Benefits: 
- Separation of concerns
- Browser caching opportunity
- Easier maintenance

### 2. `chart_data.json` (Chart Specifications)
```json
{
   "version": 1,
   "metric": "CET1 Ratio",
   "data": [
      {"x": [2021,2022,2023,2024,2025], "y": [3.5,3.8,4.1,3.9,4.2], "name": "HSBC"}
   ]
}
```

Benefits: 
- Clear data separation from code
- Browser fetch can load asynchronously
- Version control of chart specs

### 3. `chart_generator.py` (Python Integration)
Creates the JSON file dynamically:
```python
"""Generate chart_data.json from database metrics."""
json.dump(chart_spec, open("chart_data.json", 'w'))
```

Benefits: 
- Single source of truth for data generation
- Version control via Python files

### 4. `chart_html.html` (Render Template)
Loads dependencies externally:
```html
<!-- External Load -->
<link href="charts.css" rel="stylesheet">
<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
```

Benefits: 
- Native browser rendering capabilities  
- Interactive zoom/focus on hover without SVG limitations
- Professional appearance with CSS styling

## Integration Code Snippet

In `build_in011_deliverables.py`: Replace inline SVG generation function with:

```python
def generate_plotly_chart(records):
   """Generate HTML with embedded Plotly chart."""
   
   # Step 1: Generate chart specs
   chart_data = build_chart_specs(records)
   
   # Step 2: Save to external file
   with open("chart_data.json", 'w') as f:
       json.dump(chart_data, f, default=str)
   
   return """<!DOCTYPE html>
     <html>
     <head>
        <!-- Load Plotly.js -->
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
     </head>
     <body class="financial-report">
        <!-- Chart container with CSS classes -->
         <div id="chart-container" class="chart-wrapper" aria-label="CET1 Ratio Visualization"></div>
     </body>"""

def render_chart(container):
    """Render Plotly chart after data loads."""
    # Load chart data from external JSON
    with open("chart_data.json") as f:
       data = json.load(f)
    
    # Generate proper chart using Plotly.js
    fig = go.Figure(data)
    html_output = fig._to_html(full_html=True, filename='inline')
    return html_output
    
```

## Benefits Over SVG Generation

| Feature | Current SVG | New Plotly + CSS Integration |
|---------|--------------|------------------------------|
| **Browser caching** | ❌ None (embedded) | ✅ CSS/JS files cached separately |
| **Interactivity** | ⚠️ Limited hover states | ✅ Full zoom, pan, click interactions |
| **Responsiveness** | ❌ Static layout | ✅ Native canvas scaling |
| **Accessibility** | ⚠️ Manual labels needed | ✅ Proven WCAG compliant features |
| **Export options** | ❌ Manual only | ✅ Built-in PNG/PDF/WEBP export |
| **Performance** | ❌ Slow load (inline CSS) | ✅ Fast loading (external cache) |

## Files to Create/Modify

1. **`research/design_experiments/plp_implementation.py`** - Implementation guide
2. **`research/design_experiments/chart_data_template.json`** - Default data structure
3. **`research/design_experiments/charts.css`** - (Already created) Professional styling file
4. **`research/design_experiments/plotly_chart.html`** - Working demo

## Integration Points

### In `build_in011_deliverables.py`:
- Replace `generate_in022_chart()` function with Plotly-based generation
- Update `render_trajectory_charts()` to load from external JSON
- Adjust inline SVG labels for proper chart tooltips

### In chart data pipeline:
- New table `research/chart_data.json` containing all chart specifications  
- Build script call when metrics are refreshed: `python3 scripts/insights/create_chart_specs.py`

## Testing Strategy

1. **Basic functionality test** - Can charts render?
2. **Interactive zoom test** - Zoom works properly?
3. **Accessibility test** - Proper WCAG compliance?
4. **Export test** - PNG export generates properly-sized image?
5. **Performance test** - Page loads in under 2 seconds on average device?

## Migration Plan (If Implemented)

Priority files to refactor with Plotly integration:
1. `in022_ratio_decomposition.py` - CET1 ratio scatter plot decomposition
2. `in024_trajectory.py` - Bank trajectory charts and rank mobility
3. `in025_quality_views.py` - Quality view data visualization

## Notes

- **Proper chart data generation** is the first step - create `chart_data.json` from existing database metrics
- **External CSS loading** is already demonstrated with provided `charts.css` file  
- **Plotly.js CDN integration** can be added without requiring any local installation of libraries

