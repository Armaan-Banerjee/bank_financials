# Chart Integration Experiment: Professional Visualization Strategy

## Summary

This demonstrates an approach to replacing inline SVG chart generation in the Python scripts with proper external component integration using Plot.js and D3.js.

## Current Situation

- Deliverable HTML uses **inline SVG generation** entirely within Python
- Creates AI-generated "functional" feel, not professional appearance
- CSS is embedded as strings in generated HTML - poor caching/optimization
- Charts lack proper interactive zoom/pan functionality

## Solution: External Component Integration

Use **three separate files** loaded at runtime:

1. `charts.css` - Professional external styling (already created)
2. `chart_data.json` - Chart specifications and bank data  
3. `plotly_chart.html` - Rendering HTML with Plot.js library (to create)

## Files Created

### charts.css (Existent)
- Complete external CSS with professional color palette
- Responsive design patterns for different screen sizes
- Hover state definitions for all chart elements
- Dark/light mode variants

**Example styling:**
```css
.chart-wrapper {
    background: #fff;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    border-radius: 8px;
    padding: 24px;
}
```

### chart_data.json (Generated)
- Contains all chart data with proper structure for Plotly/CSV integration
- Example format:
```json
{
   "version": 1,
   "metric": "CET1 Ratio",
   "data": [
      {"x": [2021, 2022, 2023, 2024, 2025], "y": [3.5, 3.8, 4.1, 3.9, 4.2], "name": "Bank"}
   ]
}
```

### plotly_chart.html (To create)
- Loads Plot.js from CDN: `<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>`
- Uses external CSS file via `<link href="charts.css" rel="stylesheet">`
- JavaScript generation of data-driven charts with interactive features
- Proper hover states, dropdowns, and export functionality

## Integration Code Example

```python
def build_chart_html(records):
    """Generate HTML with proper Chart.js/Plotly integration.
    
    Args:
        records: Database records to visualize
    
    Returns:
         String containing external references to chart files + data
    """
    
    # Step 1: Generate chart data (similar to in022_ratio_decomposition)
    chart_data = generate_chart_specs(records)
     
    # Step 2: Save data as separate JSON file
   with open("chart_data.json", 'w') as f:
        json.dump(chart_data, f, indent=2)
    
     return """<!DOCTYPE html>
 <html>
 <head>
    <!-- Plotly library loaded from CDN -->
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
 </head>
 <body class="financial-report">
    <!-- Chart container with external styling -->
    <div id="chart" class="chart-wrapper"></div>
   
   <script src="chart_data.js"></script>
 </body>"""

```

## Benefits

| Feature | Current SVG | New Plotly Integration |
|---------|--------------|------------------------|
| Browser caching | ❌ (everything inline) | ✅ Separate CSS/JS files |
| Interactivity | ⚠️ Limited hover | ✅ Full zoom, pan, drag |
| Accessibility | ❌ Needs manual labels | ✅ Built-in WCAG compliance |
| Responsive | ❌ No scaling | ✅ Native canvas |
| Export options | ❌ Manual only | ✅ PNG/PDF/WEBP built-in |

## Migration Priority Order

1. **in024_trajectory.py** - CET1 ratio scatter plot (highest priority)
2. **in025_quality_views.py** - Quality visualization data  
3. **build_in011_deliverables.py** - Main chart rendering logic
4. **all others** - Future updates to trend charts

## Testing Checklist

- [ ] Charts render properly in browser (Chrome/Firefox/Safari)
- [ ] Zoom works without flickering
- [ ] Export to PNG generates proper resolution image
- [ ] CSS styling loads correctly
- [ ] Data loading from separate JSON file works
- [ ] Mobile responsive test pass (works on 320px width)
