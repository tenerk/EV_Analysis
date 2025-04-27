# Interactive Map (Folium)

This script creates an interactive map of EV charging points and NIE substations in Belfast using the `folium` library and GeoPandas' `.explore()` function. It visualises:

- 200 m buffer zones around substations (light salmon polygons)
- NIE substations (blue circular markers)
- EV charging points inside the buffer zones (green point markers)
- EV charging points outsidethe buffer zones (red point markers)
Created as assignment for EGM722. Designed to produce a mapping output showing the proximity of EV Charging stations to sub stations utilising Open Data. 
---

## Folder Purpose

This folder contains a python script (.py) and Jupyter Notebook (.ipynb) that generates an interactive map. It complements the static Cartopy map in the main belfastEVcharging.py script

---

## Data Access

The notebook reads spatial data from the shared `/Data/` directory located one folder level up from this folder.
