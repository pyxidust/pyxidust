# Pyxidust
### Geoprocessing/lidar/project tools for ArcGIS PRO.
<br>

# Dependencies
Python 3.11+, MS Windows, ArcGIS PRO 3.0+, Pandas package
<br>

# Arc Module
### **Add Data Function**
Adds data to a map in an ArcGIS PRO project.
```py
# add_data(pro_obj, map_name, option, layers=None, lyr_idx=None, gdb=None)
import arcpy
from pyxidust.arc import add_data
project = arcpy.mp.ArcGISProject(r'.aprx')
add_data(pro_obj=project, map_name='Map', option='1',
        layers=r'Shapefile.shp', lyr_idx=0, gdb=None)
```
<br>

### **Change Source Function**
Changes source of map layers in an ArcGIS PRO project.
```py
# change_source(project, dataset, layer, option, old_source, new_source)
import arcpy
from pyxidust.arc import change_source
project_ = arcpy.mp.ArcGISProject(r'\\.aprx')
map_ = project_.listMaps('Map')[0]
layer_ = map_.listLayers('Points')[3]
change_source(project=project_, dataset='Points', layer=layer_,
    option='1', old_source=r'\\Old.gdb', new_source=r'\\New.gdb')
```
<br>

### **Clear GDB Function**
Removes all feature classes, rasters, and tables from a geodatabase.
```py
# clear_gdb(gdb)
from pyxidust.arc import clear_gdb
clear_gdb(gdb=r'GDB.gdb')
```
<br>

### **Create Index Function**
Joins file metadata (name/path/modified) with layers/layouts/maps via a global ID for each .aprx file in the specified directory.
```py
# create_index(directory)
from pyxidust.arc import create_index
create_index(directory=r'\\folder')
```
<br>

### **CSV To GDB Function**
Converts a .csv file to a geodatabase table.
```py
# csv_to_gdb(csv, gdb, table)
from pyxidust.arc import csv_to_gdb
csv_to_gdb(csv=r'\\.csv', gdb=r'\\.gdb', table='Output')
```
<br>

### **CSV To Features Function**
Converts X/Y data in a .csv file to ArcGIS features and removes duplicate
coordinate pairs.
```py
# csv_to_features(input_file, output_features)
csv_to_features(input_file=r'\\.csv', output_features=r'\\Points.shp')
```
<br>

### **Cubic Volume Function**
Calculates volume in cubic yards using a cut/fill operation on two input
rasters with the same cell size and coordinate system.
```py
# cubic_volume(original, current, gdb, polygons)
from pyxidust import *
from pyxidust.arc import cubic_volume
cubic_volume(original=r'\\', current=r'\\', gdb=r'\\.gdb', polygons='poly')
```
<br>

### **Excel To GDB Function**
Converts a Microsoft Excel workbook sheet to an ArcGIS geodatabase table.
```py
# excel_to_gdb(workbook, gdb, table, sheet=None)
from pyxidust.arc import excel_to_gdb
excel_to_gdb(workbook=r'\\.xlsx', gdb=r'\\.gdb', table='Output', sheet='Sheet 1')
```
<br>

### **Explode Geometry Function**
Exports each row of a multipart feature class.
```py
# explode_geometry(dataset, gdb)
from pyxidust.arc import explode_geometry
explode_geometry(dataset='Polygons', gdb=r'\\.gdb')
```
<br>

### **Features To CSV Function**
Converts point/polygon features to a .csv file.
```py
# features_to_csv(input_features, output_file, option)
features_to_csv(input_features=r'Shapefile.shp',
        output_file=r'CSV.csv', option='polygon')
```
<br>

### **Image To Features Function**

```py
# sig
...
```
<br>

### **Move Elements Function**
Moves a selected set of elements off a layout in an ArcGIS PRO project.
```py
# move_elements(pro_obj, lay_obj, ele_type, wildcard)
import arcpy
from pyxidust.arc import move_elements
project = arcpy.mp.ArcGISProject(r'.aprx')
layout = project.listLayouts('Map')[0]
move_elements(pro_obj=project, lay_obj=layout,
    ele_type=GRAPHIC_ELEMENT, wildcard='*Info')
```
<br>

### **Place Anno Function**
Sets reference scale from a layer in an ArcGIS PRO project and creates
annotation feature classes for all layers with visible labels.
```py
# place_anno(pro_obj, map_name, lay_name, fra_name, lyr_idx, adjust, gdb, suffix, lyr_name=None)
import arcpy
from pyxidust.arc import place_anno
project = arcpy.mp.ArcGISProject(r'\\.aprx')

# returns extent, scale; unpack or call without variables
extent, scale = place_anno(pro_obj=project, map_name='Map', lay_name='Layout',
    fra_name='Map Frame', lyr_idx=0, adjust=1.1, gdb=r'\\.gdb', suffix='A')
```
<br>

### **Plot CSV Function**
Converts X/Y/Z coordinates in a .csv file to a shapefile and adds it to
a map in an ArcGIS PRO project.
```py
# plot_csv(pro_obj, map_name, csv, crs, output, x_name, y_name, z_name=None)
import arcpy
from pyxidust.arc import plot_csv
project_ = arcpy.mp.ArcGISProject(r'\\.aprx')
# z-values are optional
plot_csv(pro_obj=project_, map_name='Map', csv=r'\\.csv', crs=r'\\.prj',
    output=r'\\.shp', x_name='X', y_name='Y', z_name='Z')
```
<br>

### **Plot Excel Function**
Converts X/Y/Z coordinates in a spreadsheet workbook to a shapefile and
adds it to a map in an ArcGIS PRO project.
```py
# plot_excel(workbook, pro_obj, map_name, crs, output, x_name, y_name, z_name=None, sheet=None)
import arcpy
from pyxidust.arc import plot_excel
project_ = arcpy.mp.ArcGISProject(r'\\.aprx')
# z-values and sheet name are optional
plot_excel(workbook=r'\\.xlsx', pro_obj=project_, map_name='Map', crs=r'\\.prj',
    output=r'\\.shp', x_name='X', y_name='Y', z_name='Z', sheet='Sheet1')
```
<br>

### **Print Info Function**
Prints map/layout/layer names and data sources in an ArcGIS PRO project.
Useful for troublesome projects that will not open due to memory issues.
```py
# print_info(pro_obj)
import arcpy
from pyxidust.arc import print_info
project = arcpy.mp.ArcGISProject(r'\\.aprx')
print_info(pro_obj=project)
```
<br>

### **Print Layers Function**
Prints the properties of all layers in a map in an ArcGIS PRO project.
```py
# print_layers(pro_obj, map_name)
import arcpy
from pyxidust.arc import print_layers
project = arcpy.mp.ArcGISProject(r'\\.aprx')
print_layers(pro_obj=project, map_name='Map')
```
<br>

### **Remove Layers Function**
Removes layers from a map in an ArcGIS PRO project.
```py
# remove_layers(pro_obj, map_obj, layers)
import arcpy
from pyxidust.arc import remove_layers
project = arcpy.mp.ArcGISProject(path)
map_ = project.listMaps('Map')[0]
remove_layers(pro_obj=project, map_obj=map_, layers={'Hydro', 'Points'})
```
<br>

### **Set Default Function**
Updates home folder/default geodatabase/toolbox in an ArcGIS PRO project.
```py
# set_default(pro_obj, home, gdb, toolbox)
import arcpy
from pyxidust.arc import set_default
project = arcpy.mp.ArcGISProject(r'\\.aprx')
set_default(pro_obj=project, home=r'\\folder', gdb=r'\\.gdb',
    toolbox=r'\\.tbx')
```
<br>

### **Turn Off Function**
Turns off layers in a map in an ArcGIS PRO project if the layer index
position is found in the input list.
```py
# turn_off(pro_obj, map_name, lyr_idx)
import arcpy
from pyxidust.arc import turn_off
project = arcpy.mp.ArcGISProject(r'\\.aprx')
turn_off(pro_obj=project, map_name='Map', lyr_idx=[0,1,2])
```
<br>

### **Zoom To Function**
Sets reference scale from a layer in an ArcGIS PRO project and zooms the
layout to the layer extent.
```py
# zoom_to(pro_obj, map_name, lay_name, fra_name, lyr_idx, adjust)
import arcpy
from pyxidust.arc import zoom_to
project = arcpy.mp.ArcGISProject(r'\\.aprx')
zoom_to(pro_obj=project, map_name='Map', lay_name='Layout', fra_name='Map Frame',
    lyr_idx=0, adjust=1.1)
```
<br>

# Lidar Module
The lidartools.py script in the pyxidust/scripts folder runs all functions
in the lidar module as a suite of tools. Copy/paste the lidar template folder
into the desired location and set all configs in the 'global configs' section
at the top of the script.

# Projects Module
### **Delete Project Function**
Deletes .aprx file and associated data for workflows that do not require a
pro project.
```py
# delete_project(directory)
delete_project(directory=r'\\')
```
<br>

### **New Project Decorator**
Creates a new ArcGIS PRO project and workspace. Relevant project
information is written to a catalog. A unique identifier cascades
through all parts of the process. Use this decorator to wrap a
geoprocessing pipeline to fully automate a workflow, or use it
as a standalone project creation tool.
```py
# *args, **kwargs = function(description, name, template)
import arcpy
results = geoprocessing_pipeline(description=, name=, template=)
```
<br>

# Utils Module
### **Change Name Function**
Renames files in a folder via incremental serial numbers per a certain
file extension.
```py
# change_name(extension, directory, serials)
from pyxidust.utils import change_name
change_name(extension='.jpg', directory=r'\\folder', serials=r'\\Serials.txt')
```
<br>

### **Clear Folder Function**
Removes all files or files/folders in a directory.
```py
# clear_folder(directory, option)
clear_folder(directory=r'\\', option='all')
```
<br>

### **Collapse Path Function**
Corrects the placement of slashes in WindowsOS network paths.
```py
# collapse_path(path)
collapse_path(path=r'\\Network_Drive\\Folder')
```
<br>

### **File Parse Function**
Swiss Army knife for reading/writing files.
```py
# file_parse(option, read_file, write_file=None, find_chars=None, replace_chars=None, split_chars=None)
file_parse('8','text.txt',write_file='output.txt',find_chars='s', replace_chars='#',split_chars=',')
```
<br>

### **Get Letters Function**
Infinite generator that yields unique letter combinations for file
operations that do not support numbers.
```py
# get_letters(string)
from pyxidust.utils import get_letters
generator = get_letters(string='filename_')
next(generator) -> 'filename_A'
next(generator) -> 'filename_B'
```
<br>

### **Get Metadata Function**
Crawls a directory and returns metadata per a certain file extension.
```py
# get_metadata(extension, directory)
from pyxidust.utils import get_metadata
get_metadata(extension='.jpg', directory=r'\\folder')
```
<br>

### **Get Numbers Function**
Infinite generator that yields unique number combinations for file
operations that do not support letters.
```py
# get_numbers(string)
from pyxidust.utils import get_numbers
generator = get_numbers(string='filename_')
next(generator) -> 'filename_1'
next(generator) -> 'filename_2'
```
<br>

### **Get Time Function**
Get current timestamp and convert to desired type and format.
```py
# get_time(option)
get_time(option='1')
```
<br>

### **Join CSV Function**
Reads multiple .csv files from a directory and joins them based on a
```py
# join_csv(directory, join_file)
get_metadata('.mxd', r'\\folder')
join_csv(r'\\folder1', r'\\folder2\\.csv')
```
<br>

### **New Serial Function**
With systems that implement a serial number for record ID, compares user
input to a .txt file containing a base serial number and increments the
user input accordingly.
```py
# new_serial(serial_file, serial_number=None)
from pyxidust.utils import new_serial
new_serial(serial_file=r'\\.txt', serial_number='20231234-0001')
```
<br>

### **Session Args Function**
Creates a dictionary of arguments.
```py
# session_args(*args, **kwargs)
args = session_args(name, number, ...)
session_out(arguments=args, session_data=r'.csv')
```
<br>

### **Session In Function**
Reads results from previous session and returns as a tuple.
```py
# session_in(session_data)
name, number = session_in(session_data=r'.csv')
```
<br>

### **Session Out Function**
Writes function results to bytes for use by next session.
```py
# session_out(arguments, session_data)
args = session_args(name, number, ...)
session_out(arguments=args, session_data=r'.csv')
```
<br>

### **Trim Scale Function**
Drops decimal places in floating point values to specified scale.
```py
# trim_scale(csv_in, csv_out, columns, index, scale)
trim_scale(csv_in=r'.csv', csv_out=r'.csv', columns=['x','y'], index='id', scale=2)
```
<br>

### **Validate Serial Function**
Enforces population of numeric characters in a serial number.
```py
# validate_serial(string)
from pyxidust.utils import validate_serial
validate_serial(string='20201234-0001')
```
<br>

### **Validate String Function**
Enforces length and character type standards in a string.
Spaces and special characters are not permitted.
```py
# validate_string(length, option, text)
validate_string(length='3', option='alpha', text='abc9')
```
<br>

# Change Log
**0.2.0** (date):
- Added the following functions to the 'Arc' module:
add_data, change_source, clear_gdb, csv_to_features, explode_geometry,
features_to_csv, move_elements, remove_layers

- Added the 'Lidar' module

- Added the 'Projects' module

- Added the following functions to the 'Utils' module:
clear_folder, collapse_path, file_parse, get_letters, get_numbers, get_time,
join_csv, new_serial, session_args, session_in, session_out, trim_scale,
validate_serial, validate_string
<br>

**0.1.2** (1/23/2023):
- Corrected build information to make compatible with Windows
<br>

**0.1.1** (1/23/2023):
- Corrected build information to make compatible with Windows
<br>

**0.1.0** (1/23/2023):
- Added the 'Arc' module with the following functions:
create_index, csv_to_gdb, cubic_volume, excel_to_gdb, image_to_features,
place_anno, plot_csv, plot_excel, print_info, print_layers, set_default,
turn_off, zoom_to

- Added the get_metadata function to the 'Utils' module

- The file_rename function in the 'Utils' module has become the change_name
function with the same arguments

**0.0.1** (11/10/2022):
- Initial release and birth of Pyxidust!
<br>
