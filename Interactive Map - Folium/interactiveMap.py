import os
import geopandas as gpd
import cartopy.crs as ccrs
import folium

# Import Data
substations = gdp.read_file(os.path.abspath("Data/belfastSubstations.shp")) # Import substations data from Data folder within repository
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

# Create Folium map
m = buffer.explore(color="lightsalmon", # Create folium map with buffer GDF added in lightsalmon colour
                   popup=False, # Popups disabled
                   legend=True) # Legend enabled 

# Add additional data
substations_wm.explore(m=m, # Add to existing folium map
                       marker_type="marker", # Represented by pin marker
                       color="dodgerblue", # Colour set to blue
                       popup=True, # Popups enabled
                       legend=True) # Legend enabled
EV_inside.explore(m=m, # Add to existing folium map
                  icon=folium.Icon(color="limegreen", icon="car"), # Represented by pin marker with car icon in green
                  popup=True, # Popup enabled
                  legend=True) # Legend enabled.
EV_outside.explore(m=m, # Add to existing folium map
                   icon=folium.Icon(color="red", icon="car"), # Represented by pin marker with car icon in red
                   popup=True, # Popup enabled
                   legend=True) # Legend enabled 

m.save("EVcharging_Belfast.html")