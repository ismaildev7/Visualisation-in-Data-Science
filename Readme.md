# Visualisation in Data Science 2025/2026 — Second Chance Project
 
**Dataset:** Earthquakes (USGS, 2000–2023)
**Author:** Muhammad Ismail (2505039)
**Course:** Visualisation in Data Science (VDS2526), UHasselt
**Instructor:** Iñigo Bermejo
 
---
 
## Overview
 
This project designs and implements a set of interactive visualisations for the
USGS global earthquake catalogue (~600,000 earthquakes recorded worldwide between
January 2000 and February 2023). The goal is to explore **where** earthquakes
occur, **how** seismic activity has changed over time, and **how depth relates to
magnitude** across different tectonic regions.
 
The work follows the full visualisation design pipeline taught in the course:
exploratory data analysis → guiding questions → task operationalisation →
storyboarding → diverge/emerge sketching → final design → implementation.
 
---
 
## Guiding questions
 
1. **Where** do earthquakes occur, and how does location relate to their depth and magnitude?
2. **How** has earthquake activity evolved over time — are strong earthquakes becoming more or less frequent?
3. **What** is the relationship between depth and magnitude, and how does it differ across regions?
---
 
## Visualisations
 
| # | File | Description |
|---|------|-------------|
| 1 | `visualisations/viz1_map_explorer.html` | Animated world map (M ≥ 4.5). Size = magnitude, colour = depth. Year slider + play button, hover tooltips. |
| 2 | `visualisations/viz2_temporal_dashboard.html` | Stacked area chart of events per year by magnitude class, linked to a per-year calendar heatmap (overview + detail). |
| 3 | `visualisations/viz3_depth_magnitude.html` | Depth vs magnitude scatter with marginal histograms and a region dropdown (subduction vs shallow regions). |
| 4 | `visualisations/viz4_small_multiples.html` | Three juxtaposed maps split by depth class, showing deep events cluster only along subduction arcs. |
 
All four are standalone, self-contained HTML files (Plotly embedded inline) —
open them directly in any modern browser, no server or internet connection required.
 
---
 
## Key findings
 
- Earthquakes trace the global plate-boundary network, most densely along the Pacific "Ring of Fire".
- Total recorded activity grows over time, but the frequency of **strong** (M ≥ 6) earthquakes stays flat — the growth reflects improved detection of small events, not increased seismicity.
- Most earthquakes are shallow (< 70 km); a distinct deep-focus population at 500–600 km exists **only** in subduction zones such as Tonga, Chile, Indonesia, and Japan.
---
 
## Repository structure
 
```
.
├── README.md                      # this file
├── code/
│   └── build_visualisations.py    # single reproducible build script
├── visualisations/                # the 4 interactive HTML outputs
│   ├── viz1_map_explorer.html
│   ├── viz2_temporal_dashboard.html
│   ├── viz3_depth_magnitude.html
│   └── viz4_small_multiples.html
├── data/
│   └── README.md                  # data source note (CSV not committed — see below)
├── sketches/                      # diverge & emerge design sketches (pen & paper)
└── report/
    └── VDS2526_SecondChance_Earthquakes_Report.pdf
```
 
---
 
## Data
 
The dataset (`earthquakes-2000-01-01-2023-02-12.csv`, ~110 MB) is **not committed**
to this repository because it exceeds GitHub's 100 MB file-size limit.
 
- **Source:** USGS Earthquake Catalog — https://earthquake.usgs.gov/
- Place the CSV at `data/earthquakes-2000-01-01-2023-02-12.csv` before running the build script.
---
 
## Reproducing the visualisations
 
**Requirements:** Python 3.9+, with `pandas`, `numpy`, and `plotly`.
 
```bash
pip install pandas numpy plotly
cd code
python build_visualisations.py ../data/earthquakes-2000-01-01-2023-02-12.csv
```
 
This regenerates all four HTML files. The script performs the shared data
preparation (filtering to earthquakes, deriving year/month/day, extracting region
from the place string, depth clipping, and depth/magnitude class binning) and
writes each visualisation as a self-contained HTML file.
 
---
 
## Video walkthrough
 
A screen-capture video explaining the four visualisations is linked in the report
(Part 4) and available here: https://youtu.be/jze-uiDBvzQ
 
---
 
## Tools
 
Python · pandas · NumPy · Plotly