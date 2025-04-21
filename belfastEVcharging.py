import os
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
from cartopy.feature import ShapelyFeature
import cartopy.crs as ccrs
import cartopy.mpl.geoaxes as cgeoaxes
import contextily as cx 

# Import Data
substations = gpd.read_file(os.path.abspath('Data/belfastSubstations.shp')) # Import NIE substation data from the Data folder within Repository
EVcharging = gpd.read_file(os.path.abspath('Data/evChargingStations_Belfast.shp')) # Import EV Charging Station data from same folder

# Reproject Data for analysis and compatility with basemap
substations_wm = substations.to_crs(epsg=3857) # Convert data from Irish Grid to Web Mercator
EVcharging_wm = EVcharging.to_crs(epsg=3857) # Convert data from Irish Grid to Web Mercator

# Create 200m buffer around substations
buffer = substations_wm.buffer(200) # Create buffer
buffer_gdf = gpd.GeoDataFrame(geometry=buffer, crs="EPSG:3857") # Convert the GeoSeries created by the buffer method to a GeoDataFrame

# Create a map reference system to project data
map_crs = ccrs.Mercator() # Creates a standard coordinate system for the map figure to match the data and basemap

# Create Figure 
fig = plt.figure(figsize=(10, 10)) # Create a figure of 10 inches x 10 inches
ax = plt.axes(projection=map_crs) # Creates an axis in EPSG 3857 Web Mercator

# Set Extent of Figure
ax.set_xlim(buffer_gdf.total_bounds[[0, 2]])
ax.set_ylim(buffer_gdf.total_bounds[[1, 3]])

# Add Basemap to Figure
cx.add_basemap(ax, source=cx.providers.OpenStreetMap.Mapnik) # Add basemap to figure 

# Add Buffer to Figure 
buffer_feature = ShapelyFeature(substations_wm.geometry, map_crs, edgecolor="lightsalmon", facecolor="lightsalmon") # Create a buffer map feature and set symbology 
ax.add_feature(buffer_feature) # Add buffers to figure

# Add Substations to Figure
substations_feature = ax.plot(substations_wm.geometry.x, substations_wm.geometry.y, 's', color="dodgerblue", ms=3, label="NIE Substations") # Add subtations to figure

# Add EV Charging Stations to Figure 
EVcharging_feature = ax.plot(EVcharging_wm.geometry.x, EVcharging_wm.geometry.y, 'o', color="limegreen", ms=4, label="EV Charging Points") # add charging stations to figure

# Create a scale
# Adopted from Mapping with Cartopy Exercise within https://github.com/iamdonovan/egm722
def scale_bar(ax: cgeoaxes.GeoAxes, length=1, location=(0.92, 0.95)): # Set location of bar within map figure 
    x0, x1, y0, y1 = ax.get_extent() # Retreive current extent of axis - to be defined by data
    sbx = x0 + (x1 - x0) * location[0] # Correct x coorinate of scale bar
    sby = y0 + (y1 - y0) * location[1] # Correct y coordinate of scale bar

    ax.plot([sbx, sbx-length*1000], [sby, sby], color='k', linewidth=4, transform=ax.projection) # Plot black line with thickness of 4
    ax.plot([sbx-(length/2)*1000, sbx-length*1000], [sby, sby], color='w', linewidth=2, transform=ax.projection) # Plot thinner white line

    ax.text(sbx, sby-(length/4)*1000, f"{length}km", ha='center', transform=ax.projection, fontsize=6) # Add label to right of scale bar
    ax.text(sbx-(length/2)*1000, sby-(length/4)*1000, f"{int(length/2)}km", ha='center', transform=ax.projection, fontsize=6) # Add halfway label
    ax.text(sbx-length*1000, sby-(length/4*1000), '0km', ha='center', transform=ax.projection, fontsize=6) # Add label to left of scale bar

    return ax

# Create patches for the legend
def map_legend(ax: cgeoaxes.GeoAxes):
    buffer_patch = mpatches.Patch(color="lightsalmon", label="200m Buffer") # Create legend patch for Buffer polygon data
    substations_marker = mlines.Line2D([], [], color='dodgerblue', marker='s', linestyle='None',
markersize=8, label="Substations") # Create legend patch for Substation point data
    charging_marker = mlines.Line2D([], [], color='limegreen', marker='o', linestyle='None',
markersize=8, label="EV Charging Points") # Create a legend patch for EV Charging point data
    
    ax.legend(handles=[buffer_patch, substations_marker, charging_marker], loc='lower left', fontsize=8, frameon=True) # Determines position and style of legend

# Add map elements 
ax.gridlines(draw_labels=False) # Add gridlines to figure 
scale_bar(ax) # Add scale to figure
map_legend(ax) # Add legend to figure
ax.set_title("EV Charging Stations in relation to Substations in Belfast", fontsize=14, pad=20) # Add title to figure

# Export Map 
fig.savefig('belfastChargers_python.jpeg', dpi =300) # Export map as JPEG
