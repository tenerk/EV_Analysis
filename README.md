# EV_Analysis
This script creates a JPEG mapping output of EV charging points and NIE substations in Belfast using the `matplotlib` library and `cartopy`. It visualises:

- 200 m buffer zones around substations (light salmon polygons)
- NIE substations (blue square markers)
- EV charging points inside the buffer zones (green circle)
- EV charging points outsidethe buffer zones (red circles)
- Open Street Map basemap
Created as assignment for EGM722. Designed to produce a mapping output showing the proximity of EV Charging stations to sub stations utilising Open Data. 
---

## Folder Purpose

This folder contains a python script (.py) and Jupyter Notebook (.ipynb) that generates a JPEG map.

---

## Data Access

The notebook reads spatial data from the shared `/Data/` directory located one folder level up from this folder.

## Additional Resources

Within the `/Interactive Map - Folium folder within the repository/`, there is a Python Script and Jupyter Notebook provided to transform the static output into an interactive HTML link using `folium`. No additional data is required and the environment.yml file is consistent. 
