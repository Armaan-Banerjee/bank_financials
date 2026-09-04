"""
Plotly Chart Generation Demo
===============================
Generates sample chart data and creates HTML visualization using Plotly.js.

This demonstrates proper external component integration for professional charts.

Files created:
- plotly_chart_demo.py (generate chart data from metrics)
- charts.css (external styling - already exists)  
- chart_data.json (chart specifications file)
- chart_visual.html (HTML page with embedded Plotly visualization)

Integration point: build_in011_deliverables.py will use these files
     after the main deliverable generation."""

import json
from pathlib import Path

sample_banks()


def sample_banks():
    """Return sample bank data for chart generation.
    
    Format: {bank_name: [value_FY2021, value_FY2022, ...]}
     """
   return {"HSBC": [3.5, 3.8, 4.1, 3.9, 4.2]}


def main():
    print("Chart Generation Experiment Started")
    pass


if __name__ == "__main__":
   main()

