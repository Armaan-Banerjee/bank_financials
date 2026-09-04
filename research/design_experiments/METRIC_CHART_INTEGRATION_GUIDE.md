# Metric Chart Integration Guide
====================

This document provides specific instructions for implementing the Plot.js/Chart.js integration into the main deliverable generation scripts.

## Quick Start Guide

### Step 1: Update `build_in011_deliverables.py`

**Find:** Current inline SVG chart generation function in `i024_trajectory.py`  
```python
def generate_trajectory_chart(records):
   """Generate inline SVG chart."""
   ... # generates raw SVG string directly in Python
```

**Replace with:** Plot.js integration approach
```python
from plotly import go, GraphLayout

def generate_plotly_chart(records):
    """Generate proper Chart.js/Plotly interactive visualization.
    
    Args:
        records: Database records for visualization
        
    Returns:
        HTML string with embedded Plot.js chart renderer
        
        Example returns:
        <div id="chart-container"></div> + <script src="chart_data.js"></script>
    """
    fig = go.Figure()
    
    # Add data trace from records with proper formatting
    fig.add_trace(go.Bar(
        x=[r["year"] for r in records],
        y=[float(r["metric"]) for r in records],
        name=records[0]["bank_name"],
        marker=dict(size=6),
        line=dict(width=2)
    ))
    
    # Load external CSS and data files (asynchronously)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
     <link href="/Users/armaan/code/katalysis/research/design_experiments/charts.css" rel="stylesheet">
</head>
<body class="financial-report">
   <div id="plotly-chart"></div>
   <script src="/Users/armaan/code/katalysis/research/design_experiments/chart_data.js"></script>
</body>"""

```

### Step 2: Create `chart_data.json` Template

**Location:** `/Users/armaan/code/katalysis/research/design_experiments/chart_data.json`

```json
{
   "version": 1,
   "data": {
       [
           {"x": [2021, 2022, 2023], "y": [3.5, 3.8, 4.1]}
       ]
   },
   "chart_type": "bar_chart",
   "metric_name": "CET1 Ratio",
   "title": "UK Banks CET1 Analysis"
}

```

### Step 3: Generate Script from Database

**New Function:** `create_chart_data_json(records)`

In your delivery generation script (e.g., `build_in011_deliverables.py`):

```python
def create_chart_specs(records, chart_type="bar"):
    """Generate proper Chart.js data spec for charts.
    
    Args:
        records: Records from database with bank metric values
        chart_type: "bar", "line", or "scatter"
        
    Returns:
         Dictionary with chart specifications and formatting
        
    Example usage:
    import json
    with open(chart_file, 'w') as f:
        json.dump(generate_specs(records), f)
            
```

### Step 4: Update Chart Generation Function

**Example integration:**

```python
def build_chart_data_from_metrics(records):
     """Build proper Chart.js chart data from database records."""
   
   # Convert bank names, metrics to Chart.js expected format
   data = {
       "version": 1,
       "metric_type": "CET1 Ratio",
       "data_series": []
    }
   
   for record in records:
       data["data"].append({
            "x": [record["year"] for year in sorted(sets([r["year"] for r in records]))],
            "y": [float(r["value"]) for r in records]
        })
    
     # Save to external file (NOT embedded in HTML output)
   with open(chart_data_file, 'w') as f:
             json.dump(data, f, indent=2)
   
     return data

```

### Step 5: Update HTML Generation Function

**Integration approach:**

```python
def generate_chart_html_with_external_libs(records):
    """Generate HTML with external Chart.js integration.
     
    Note: This is NOT rendered immediately - it generates an HTML template 
    that will render the chart when loaded by the browser at runtime.
     
    Returns:
        String containing:
        1. External CSS reference (charts.css)
        2. Plotly/Chart.js library CDN link  
        3. Data file path to external JSON
        4. Chart template with proper styling
    """
    
     chart_spec_data = build_chart_data_from_metrics(records)
     
     return f'''<!DOCTYPE html>
     <meta name="viewport" content="width=device-width, initial-scale=1.0">
     <h3>{chart_spec["metric_name"]}</h3>
     <link href="/Users/armaan/code/katalysis/research/design_experiments/charts.css" rel="stylesheet">
     
     <script src="https://cdn.plot.ly/plotly.min.js"></script>
     <script src="/Users/armaan/code/katalysis/research/design_experiments/chart_data.js"></script>
     
     <div id="chart-container"></div>
     '''

```

## Integration Priority Order

1. **Highest Priority:** `in024_trajectory.py` - CET1 ratio scatter plot is primary visual in deliverable
2. **High Priority:** `build_in011_deliverables.py` - Main chart generation logic
3. **Medium Priority:** All other charts using current SVG approach (quality improvement over time)

## Testing Checklist

- [ ] Charts render properly with external CSS
- [ ] Hover events work correctly
- [ ] Zoom/pan interactions active and smooth
- [ ] Export to PNG generates proper resolution  
- [ ] Mobile responsive test (320px width)
- [ ] Plotly CDN version compatibility test

## Files Location Map

```
/Users/armaan/code/katalysis/research/design_experiments/
├── ChartIntegration_README.md      # Overview document
├── METRIC_CHART_INTEGRATION_GUIDE.md  # THIS FILE - developer guide
├── chart_data.json                # Generated data spec (example)
├── charts.css                     # External CSS styling file  
└── chart_visualization.html       # Rendered HTML demo

# Integration target:
/Users/armaan/code/katalysis/scripts/insights/in011_deliverables.py
```

## Example Implementation Snippet

**For `in024_trajectory.py`:**

```python
"""
In024 Trajectory Chart Generation with External Components
============================================================

Generate charts using Plot.js library integration instead of SVG.

Usage:
   python3 generate_in024_trajectories.py
   # Outputs chart_data.json and updates in011_deliverables.py template
"""

import json as json_import

# Example data structure from database
def build_trajectory_chart_data(data):
     # Data format for Chart.js/Plotly: {"x": ["year"], "y": [value]}
   
   return {
            "title": "CET1 Ratio Comparison",
            "data": [
                {"x": ["2021", "2022", "2023"], "y": [5.1, 4.8, 5.5], "name": "Bank A"}
           ]
   }

# Save chart specification file (NOT in render)
def generate_chart_spec_file(chart_data):
   with open("chart_data.json", "w") as f:
       json_import.dump(chart_data, f)
 
# Generate HTML template
if __name__ == "__main__":
   chart_specs = build_trajectory_chart_data(sample_data)
   generate_chart_spec_file(chart_specs)

```