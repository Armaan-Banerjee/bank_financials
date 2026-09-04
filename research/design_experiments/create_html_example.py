"""
Create demonstration HTML with Plotly integration
===============================================
This script generates a sample chart visualization file that demonstrates 
how to integrate external CSS and Plotly.js into the deliverable.

Integration point: build_in011_deliverables.py will be updated to use these files.
"""

import json
from pathlib import Path

def main():
     print("=== Creating Demonstration Files ===")
     
    # 1. Create chart_data.json (data source)
    data = {
        "version": 1,
        "metric": "CET1 Ratio",
        "description": "UK Banks Analysis FY2021-FY2025",
        "data": [
            {"x": [2021, 2022, 2023, 2024, 2025], "y": [3.5, 3.8, 4.1, 3.9, 4.2], "name": "HSBC"}
        ]
    }
    Path("chart_data.json").write_text(json.dumps(data))
    print("✓ Created chart_data.json")

    # 2. Create HTML template with Plotly integration
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CET1 Ratio Analysis</title>
     
     <!-- External CSS loading -->
     <link href="/Users/armaan/code/katalysis/research/design_experiments/charts.css" rel="stylesheet">
     
     <!-- Plotly.js library loaded from CDN -->
     <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
</head>
<body class="financial-report">

<div style="max-width: 1366px; margin: auto; padding: 24px;">

<!-- Section 1: Title -->
<section style="border-radius: 8px; background-color: #faf9f5; padding: 20px; margin-bottom: 20px;">
   <h1>CET1 Ratio Analysis: UK Banks (FY2021-2025)</h1>
</section>

<!-- Controls -->
<select id="year-filter" style="display: inline-block; padding: 12px 16px; border-radius: 4px; background-color: #fff;">
   <option value="2021-2025">All Years (FY2021-FY2025)</option>
</select>

<!-- Main Chart -->
<div id="chart-container" style="background-color: white; border-radius: 8px; padding: 24px; box-shadow: 0 2px 8px rgba(0,0,0,0.06);">
   <h2>Interactive CET1 Performance Chart</h2>
   
   <!-- Hover over chart to see bank details -->
   Hover over bars to view detailed information

</div>

<!-- Legend -->
<div style="display: flex; gap: 16px; margin-bottom: 20px;">
   <span>CET1 (%)</span>
   <span style="color: #657982">Higher = better risk buffering</span>
</div>


<!-- Data provenance -->
<div style="background-color: rgba(0,0,0,0.03); padding: 15px; margin-bottom: 20px;">
   <em>Data Source: UK Financial Services Authority reports and regulatory filings</em>
</div>

<!-- Download button -->
<button style="padding: 12px 24px; background-color: #195b8f; color: white; border: none; border-radius: 4px; cursor: pointer;">
   Export as PNG
</button>

<!-- Footer -->
<div style="margin-top: 30px; padding: 15px; background-color: #f5f5f5; border-radius: 8px;">
   <strong class="version-info">Analysis Version: 2.0 | Generated: %(timestamp)s</strong>
   <br>Data provenance: UK Financial Services Authority reports and regulatory filings
</div>

</div>

<!-- Chart generation script -->
<script type="text/javascript">
var data = {{JSON.parse('''[{"x": [2021, 2022, 2023, 2024, 2025], "y": [3.5, 3.8, 4.1, 3.9, 4.2], "name": "HSDB Bank Plc", "marker": {"size: 10}}']}'')}};
plotly.newPlot('chart-container', data);
</script>

</body>
</html>"""

Path("charts.html").write_text(html_content)
print("✓ Created charts.html with Plotly integration")

    # Summary
print("\nFiles created for demo:")
files = ["chart_data.json", "charts.css", "charts.html"]
for f in files:
    path = Path(f)
    print(f'  - {f} ({path.name})')

if __name__ == "__main__":
   main()
    
