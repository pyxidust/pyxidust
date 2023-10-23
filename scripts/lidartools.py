# pyxidust library lidartools script
# Gabriel Peck 2023 (MIT license)

"""The lidartools script uses functions from the pyxidust.lidar module to
create a suite of lidar datasets from raw .las files. Users can comment-out
functions that are not needed at the end of this script, or run all the lidar
tools to create a lidar catalog that can be archived year-to-year as new data
is acquired.

Prerequisites:

1. Copy/paste the 'pyxidust/templates/lidar' folder to a local SSD drive; set
the fully-qualified/raw path to the that folder as the output_folder variable
below

2. Copy/paste the .las files that will be processed into the new lidar folder's
'LAS' subdirectory

3. Set the coordinate system (crs) and arcpy environments in the global configs
below

4. If running the 3D buildings code, the following are needed:

    a. Digitize building footprints to constrain the 3D patch analysis:
    ...Lidar\\Buildings\\Buildings.gdb\\BuildingsCurrent
    b. Digitize a mask boundary to limit the analysis extent:
    ...Lidar\\Buildings\\Buildings.gdb\\Region
"""

###############################################################################

import arcpy
from pyxidust import lidar

###############################################################################
# GLOBAL CONFIGS:
###############################################################################

# copy/paste the lidar template folder to
# desired location and set here...
output_folder = r''

# coordinate system for all output; path to
# an ArcGIS .prj file on disk
crs = r''

# universal cellsize for all output
arcpy.env.cellSize = 0.55

# distribute cpu processing power for tasks
# that honor parallel processing; 10-core
# cpu using 9 cores in this example
arcpy.env.parallelProcessingFactor = '90%'

# build pyramids by default for all output
arcpy.env.pyramid = 'PYRAMIDS'

###############################################################################

# lasd dataset is the base for further analysis
lidar.lasd(output_folder, crs)

###############################################################################

# function calls to process lidar data;
# comment-out tools that are not needed;
# dem or dsm-derived data cannot process
# without a dem or dsm function call

# DEM-derived data
lidar.dem(output_folder)
print('DEM has executed')
lidar.mean(output_folder)
print('Mean has executed')
lidar.contours(output_folder)
print('Contours have executed')

# DEM-derived data
lidar.aspect(output_folder)
print('Aspect executed successfully')
lidar.buildings(output_folder)
print('Buildings have executed')
lidar.dem_shade(output_folder)
print('DEM hillshade executed successfully')
lidar.dem_terrain(output_folder)
print('DEM terrain executed successfully')
lidar.slope(output_folder)
print('Slope executed successfully')

# DSM-derived data
lidar.dsm(output_folder)
print('DSM executed successfully')
lidar.dsm_shade(output_folder)
print('DSM hillshade executed successfully')
lidar.dsm_terrain(output_folder)
print('DSM terrain executed successfully')
lidar.ranged(output_folder)
print('Range executed successfully')

# LAS-derived data
lidar.intensity(output_folder)
print('Intensity executed successfully')

# metadata
lidar.metadata(output_folder)
print('Metadata executed successfully')

print('Lidar tools suite has completed successfully.')
end = input('Press the <ENTER> key to exit.')
