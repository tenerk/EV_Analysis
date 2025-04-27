import os
import geopandas as gpd
import cartopy.crs as ccrs
import folium

# Import Data
substations = gpd.read_file("../Data/belfastSubstations.shp") # Import substations data from Data folder within repository
EVcharging = gpd.read_file("..Data/evChargingStations_Belfast.shp") # Import EV Charging Station data from same folder

# Reproject data for analysis and compatility with .buffer
substations_wm = substations.to_crs(epsg=3857) # Convert data from Irish Grid to Web Mercator
EVcharging_wm = EVcharging.to_crs(epsg=3857) # Convert data from Irish Grid to Web Mercator

# Create 200m buffer around substations
buffer = substations_wm.buffer(200) # Create buffer of 200m - units derived from substation_wm 
buffer_gdf = gpd.GeoDataFrame(geometry=buffer) # Convert the GeoSeries created by the buffer method to a GeoDataFrame
buffer_gdf.set_crs(epsg=3857, inplace=True) # Sets GDF to EPSG:3857

#Classify charging points as inside or outside the 200m buffer
within_buffer = [] # Create an empty list to store inside or outside values 

for point in EVcharging_wm.geometry: # Loop through all points within named dataset
    is_within = buffer_gdf.intersects(point).any() # Check if point intersects buffer
    within_buffer.append(is_within) # Append true/false results to list 

EVcharging_wm["within_buffer"] = within_buffer # Adds list as column to dataset

# Create an Inside and Outside GeoDataFrame
EV_inside = EVcharging_wm[EVcharging_wm["within_buffer"]] # Create a GDF for points within the buffer - True values
EV_outside = EVcharging_wm[~EVcharging_wm["within_buffer"]] # Create a GDF for points outside the buffer - False values

# Reproject data for use in folium 
buffer_f = buffer_gdf.to_crs(epsg=4326) # Reproject buffer data to EPSG:4326
substations_f = substations_wm.to_crs(epsg=4326) # Reproject substation data to EPSG:4326
EVinside_f = EV_inside.to_crs(epsg=4326) # Reproject EV points inside buffer to EPSG:4326
EVoutside_f = EV_outside.to_crs(epsg=4326) # Reproject EV points outside buffer to EPSG:4326

# Create Folium map
m = buffer_f.explore(color="lightsalmon", # Create folium map with buffer GDF added in lightsalmon colour
                   popup=False, # Popups disabled
                   legend=True) # Legend enabled 

# Add additional data
substations_f.explore(m=m, # Add to existing folium map
                       marker_type="circle_marker", # Represented by small circle
                       color="dodgerblue", # Colour set to blue
                       popup=True, # Popups enabled
                       legend=True) # Legend enabled
EVinside_f.explore(m=m, # Add to existing folium map
                  marker_type="marker", # Represented by pin marker with car icon in green
                   color="limegreen", # Colour set to green
                  popup=True, # Popup enabled
                  legend=True) # Legend enabled.
EVoutside_f.explore(m=m, # Add to existing folium map
                   marker_type="marker", # Represented by pin marker with car icon in red
                    color="red", # Colour set to red
                   popup=True, # Popup enabled
                   legend=True) # Legend enabled 

m.save("EVcharging_Belfast.html") # Save map as HTML link