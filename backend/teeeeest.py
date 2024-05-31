import os

shapefile_path = 'C:/Users/PC/Desktop/Final_year_project/fyp_is/backend/maps/animalpoints.shp'

os.chmod(shapefile_path, 0o644)

if os.access(shapefile_path, os.R_OK | os.W_OK):
    print("Shapefile has read and write permissions.")
else:
    print("Shapefile does not have read and write permissions.")