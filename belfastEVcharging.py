import os
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
from cartopy.feature import ShapelyFeature
import cartopy.crs as ccrs
import cartopy.mpl.geoaxes as cgeoaxes
import contextily as cx 

# Import data
substations = gpd.read_file(os.path.abspath('Data/belfastSubstations.shp')) # Import NIE substation data from the Data folder within Repository
EVcharging = gpd.read_file(os.path.abspath('Data/evChargingStations_Belfast.shp')) # Import EV Charging Station data from same folder

# Reproject data for analysis and compatility with basemap
substations_wm = substations.to_crs(epsg=3857) # Convert data from Irish Grid to Web Mercator
EVcharging_wm = EVcharging.to_crs(epsg=3857) # Convert data from Irish Grid to Web Mercator

# Create 200m buffer around substations
buffer = substations_wm.buffer(200) # Create buffer of 200m - units derived from substation_wm 
buffer_gdf = gpd.GeoDataFrame(geometry=buffer) # Convert the GeoSeries created by the buffer method to a GeoDataFrame
buffer_gdf.set_crs(epsg=3857, inplace=True) # Sets GDF to EPSG 3857

#Classify charging points as inside or outside the 200m buffer
within_buffer = [] # Create an empty list to store inside or outside values 

for point in EVcharging_wm.geometry: # Loop through all points within named dataset
    is_within = buffer_gdf.intersects(point).any() # Check if point intersects buffer
    within_buffer.append(is_within) # Append true/false results to list 

EVcharging_wm["within_buffer"] = within_buffer # Adds list as column to dataset

# Create an Inside and Outside GeoDataFrame
EV_inside = EVcharging_wm[EVcharging_wm["within_buffer"]] # Create a GDF for points within the buffer - True values
EV_outside = EVcharging_wm[~EVcharging_wm["within_buffer"]] # Create a GDF for points outside the buffer - False values

# Create a map reference system to project data
map_crs = ccrs.Mercator() # Creates a standard coordinate system for the map figure to match the data and basemap

# Create figure 
fig = plt.figure(figsize=(10, 10)) # Create a figure of 10 inches x 10 inches
ax = plt.axes(projection=map_crs) # Creates an axis in EPSG 3857 Web Mercator

# Set extent of figure
ax.set_xlim(buffer_gdf.total_bounds[[0, 2]]) # Sets extent to match total bounds of buffer_gdf - x coordinate
ax.set_ylim(buffer_gdf.total_bounds[[1, 3]]) # Sets extent to match total bounds of buffer_gdf - y coordinate

# Add Basemap to figure
cx.add_basemap(ax, source=cx.providers.OpenStreetMap.Mapnik) # Add basemap to figure 

# Add Buffer to figure 
buffer_feature = ShapelyFeature(
    buffer_gdf['geometry'],# Define geometry
    map_crs, # Define CRS
    edgecolor="lightsalmon", # Set edge colour
    facecolor="lightsalmon" # Set face colour
)  

ax.add_feature(buffer_feature) # Add buffers to figure

# Add Substations to figure
substations_feature = ax.plot(
    substations_wm.geometry.x, # Define x coordinates
    substations_wm.geometry.y, # Define y coordinates
    's', # Set marker style to square
    color="dodgerblue", # Set marker colour
    ms=3, # Set marker size
    label="NIE Substations" # Add label 
)  

# Add EV Charging Stations to figure 
EVcharging_inside_feature = ax.plot(
    EV_inside.geometry.x, # Define x coordinates
    EV_inside.geometry.y, # Define y coordinates
    'o', # Set marker style to circle
    color="limegreen",  # Set marker colour
    ms=4, # Set marker size
    label="EV Charging Points inside Buffer" # Add label
) 

EVcharging_outside_feature = ax.plot(
    EV_outside.geometry.x, # Define x coordinates
    EV_outside.geometry.y,  # Define y coordinates
    'o', # Set marker style to circle
    color="red",  # Set marker colour
    ms=4, # Set marker size
    label="EV Charging Points outside Buffer" # Add label
) 

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
    buffer_patch = mpatches.Patch( # Add patch to legend for buffer polygon data
        color="lightsalmon", # Set colour to lightsalmon to match data
        label="200m Buffer" # Add label to patch
    ) 
    
    substations_marker = mlines.Line2D( # Add patch to legend for substation point data
        [], [], # Empty placeholder for x,y coordinates - not required in legend
        color="dodgerblue", # Set colour to dodgerble 
        marker="s", # Set marker style to square
        linestyle="None", # Set line style to none (point data)
        markersize=7, # Set marker size
        label="Substations" # Add label to patch 
    ) 
    
    EV_inside_marker = mlines.Line2D( # Add patch to legend for EV points inside buffer
        [], [], # Empty placeholder for x,y coordinates
        color="limegreen", # Set colour to limegreen 
        marker="o", # Set marker style to circle
        linestyle="None", # Set linestyle to none
        markersize=7, # Set marker size
        label="EV Charging Points inside the 200m buffer" # Add label to patch
    ) 
    
    EV_outside_marker = mlines.Line2D( # Add patch to legend for EV points outside buffer
        [], [], # Empty placeholder for x,y coordinates
        color="red", # Set colour to red
        marker="o", # Set marker style to circle
        linestyle="None", # Set linestyle to none
        markersize=7, # Set marker size
        label="EV Charging Points outside the 200m buffer" # Add label to patch
    ) 
    
    ax.legend(handles=[buffer_patch, substations_marker, EV_inside_marker, EV_outside_marker], loc='lower left', fontsize=8, frameon=True) # Set position and style of legend - lower left corner of figure

# Add summary text 
inside_count = len(EV_inside) # Store count of how many charging points are inside the buffer 
outside_count = len(EV_outside) # Store count of how many charging points are outside the buffer

summary_text = f"Charging points inside buffer: {inside_count} \nCharging points outside buffer: {outside_count}" # Create summary text showing count of points inside and outside buffer 

ax.text( # Add summary text to map
    0.98, # x coordinate relative to axes
    0.02, # y coordinate relative to axes
    summary_text, # String to display
    transform=ax.transAxes, # Set axes coorindates
    fontsize=10, # Set font size
    verticalalignment="bottom", # Align text from bottom edge
    horizontalalignment="right", # Align text from right edge
    bbox=dict(facecolor="white", # Set background colour of bounding box
              edgecolor="grey", # Set edge colour of bounding box
              boxstyle="round", # Round box corners
              pad=0.4) # Set padding inside box
    ) 

# Add map elements 
ax.gridlines(draw_labels=False) # Add gridlines to figure with labelling turned off
scale_bar(ax) # Add scale to figure
map_legend(ax) # Add legend to figure
ax.set_title("EV Charging Stations in relation to Substations in Belfast", fontsize=14, pad=20) # Add title to figure

# Export Map 
fig.savefig('belfastChargers.jpeg', dpi =300) # Export map as JPEG to EV_Analysis folder
