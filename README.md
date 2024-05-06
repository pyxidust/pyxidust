# Pyxidust
Geoprocessing/lidar/project tools for ArcGIS PRO.
<br>
<br>

# Dependencies
Python 3.11+ with Pandas package, Microsoft Windows 10+, ArcGIS PRO 3.0+
<br>
<br>

# Geoprocessing Module
### **Add Data Function**
Adds data to a map in an ArcGIS PRO project.
```py
# add_data(project, map_name, option, layers=None, layer_index=None, gdb=None)
import arcpy
from pyxidust.gp import add_data
project = arcpy.mp.ArcGISProject(r'\\.aprx')

# option 1: add shapefile to an indexed position in the table of contents
add_data(project=project, map_name='Map', option=1, layers=r'\\.shp',
    layer_index=3)

# option 2: add one/multiple feature classes to top of table of contents
add_data(project=project, map_name='Map', option=2,
    layers=['Points', 'Polygons'], gdb=r'\\.gdb')

# option 3: add all feature classes from gdb to top of table of contents
add_data(project=project, map_name='Map', option=3, gdb=r'\\.gdb')

# option 4: add layer file to top of table of contents
add_data(project=project, map_name='Map', option=4, layers=r'\\.lyrx')

# option 5: add layer file to indexed group layer in table of contents
add_data(project=project, map_name='Map', option=5, layers=r'\\.lyrx',
    layer_index=0)
```
<br>

### **Change Source Function**
Changes source of map layers in an ArcGIS PRO project.
```py
# change_source(project, dataset, layer, option, old_source, new_source)
import arcpy
from pyxidust.gp import change_source
project = arcpy.mp.ArcGISProject(r'\\.aprx')
map_ = project.listMaps('Map')[0]

# [3] == index position of layer in TOC
layer = map_.listLayers('Points')[3]

# option 1: change dataset source from one GDB to another GDB
change_source(project=project, dataset='Points', layer=layer, option=1,
    old_source=r'\\.gdb', new_source=r'\\.gdb')
```
<br>

### **Clear GDB Function**
Removes all feature classes/rasters/tables from a geodatabase.
```py
# clear_gdb(gdb)
from pyxidust.gp import clear_gdb
clear_gdb(gdb=r'\\.gdb')
```
<br>

### **CSV To Features Function**
Converts X/Y data in a .csv file to features.
```py
# csv_to_features(input_file, output_features, projection, event_data)
from pyxidust.gp import csv_to_features
csv_to_features(input_file=r'\\.csv', output_features=r'\\.shp',
    projection=r'\\.prj', event_data=r'\\event_1')
```
<br>

### **CSV To GDB Function**
Converts a .csv file to a geodatabase table.
```py
# csv_to_gdb(csv, gdb, table)
from pyxidust.gp import csv_to_gdb
csv_to_gdb(csv=r'\\.csv', gdb=r'\\.gdb', table='Output')
```
<br>

### **Cubic Volume Function**
Calculates change in volume between two rasters.
```py
# cubic_volume(original, current, gdb, polygons)
from pyxidust.gp import cubic_volume
cubic_volume(original=r'\\', current=r'\\', gdb=r'\\.gdb', polygons='Poly')
```
<br>

### **Excel To GDB Function**
Converts an Excel workbook sheet to an ArcGIS geodatabase table.
```py
# excel_to_gdb(workbook, gdb, table, sheet=None)
from pyxidust.gp import excel_to_gdb
excel_to_gdb(workbook=r'\\.xlsx', gdb=r'\\.gdb', table='Output',
    sheet='Sheet 1')
```
<br>

### **Explode Geometry Function**
Exports new features for each row in a multipart feature class.
```py
# explode_geometry(dataset, gdb)
from pyxidust.gp import explode_geometry
explode_geometry(dataset='Polygons', gdb=r'\\.gdb')
```
<br>

### **Features To CSV Function**
Extracts coordinate pairs from point/polygon features.
```py
# features_to_csv(input_features, output_file, option, gdb=None)
from pyxidust.gp import features_to_csv

# point input features
features_to_csv(input_features=r'\\', output_file=r'\\.csv',
    option='point', gdb=r'\\.gdb')

# polygon input features
features_to_csv(input_features=r'\\.shp', output_file=r'\\.csv',
    option='polygon')
```
<br>

### **Get Suffix Function**
Appends a unique letter combination to the string per each iteration.
```py
# get_suffix(string)
from pyxidust.gp import get_suffix

# create generator to yield values
generator = get_suffix(string='filename_')
next(generator) -> 'filename_A'
next(generator) -> 'filename_B'
```
<br>

### **Image To Features Function**
Extracts polygon features from a georeferenced image.
```py
# image_to_features(image, classes, identifier, query, projection, directory, area=None)
from pyxidust.gp import image_to_features

# example with 4 distinct colors/polygons in the input image
clip_1 = image_to_features(image='\\.tif', classes='4', identifier='A',
    query='VALUE = 1 OR VALUE = 2', projection='\\.prj', directory='\\',
    area='AREA >= 100')

# when classes > 1 feed the returned 'clip' to the image value
clip_2 = image_to_features(image=clip_1, classes='6', identifier='B',
    query='VALUE = 3', projection='\\.prj', directory='\\',
    area='AREA >= 100')
```
<br>

### **Increment Field Function**
Adds a sequential range of numbers to an existing field in a dataset.
```py
# increment_field(dataset, field_name, field_type, counter)
from pyxidust.gp import increment_field
increment_field(dataset=r'\\.shp', field_name='ID', field_type='text',
    counter=1)
```
<br>

### **Layout Scale Function**
Adjusts the layout scale to the extent of a layer.
```py
# layout_scale(project, map_name, layout_name, frame_name, layer_index, adjust)
import arcpy
from pyxidust.gp import layout_scale
project = arcpy.mp.ArcGISProject(r'\\.aprx')

# set layout extent to layer[1]
extent, scale = layout_scale(project=project, map_name='Map',
    layout_name='Layout', frame_name='Map Frame', layer_index=1,
    adjust=1.0)

# set layout extent to layer[3] and fine-tune scale
extent, scale = layout_scale(project=project, map_name='Map',
    layout_name='Layout', frame_name='Map Frame', layer_index=3,
    adjust=0.9)
```
<br>

### **Match Values Function**
Updates a text field value if a match is found in the field map.
```py
# match_values(dataset, key_field, field_map, update_field, update_value)
from pyxidust.gp import match_values
search_values = ['21', '44', '3', '87', '35', '77', '92']

# populate 'MATCH' with 'Y' when 'ID' values are found in the search values
match_values(dataset=r'\\.shp', key_field=['ID'], field_map=search_values,
    update_field=['MATCH'], update_value='Y')
```
<br>

### **Move Elements Function**
Removes elements from a layout in an ArcGIS PRO project.
```py
# move_elements(project, layout, element, wildcard)
import arcpy
from pyxidust.gp import move_elements
project = arcpy.mp.ArcGISProject(r'\\.aprx')
layout = project.listLayouts('Layout')[0]

# remove all graphic elements with names that end in 'Info'
move_elements(project=project, layout=layout, element='GRAPHIC_ELEMENT',
    wildcard='*Info')
```
<br>

### **Place Anno Function**
Creates annotation feature classes from all layers with visible labels.
```py
# place_anno(project, map_name, layout_name, frame_name, layer_index, adjust, gdb, suffix, layer_name=None)
import arcpy
from pyxidust.gp import place_anno
project = arcpy.mp.ArcGISProject(r'\\.aprx')

# create annotation for all visible layers
extent, scale = place_anno(project=project, map_name='Map',
    layout_name='Layout', frame_name='Map Frame', layer_index=1,
    adjust=1.0, gdb=r'\\.gdb', suffix='A')

# create annotation for 'Points' layer only and fine-tune scale
extent, scale = place_anno(project=project, map_name='Map',
    layout_name='Layout', frame_name='Map Frame', layer_index=3,
    adjust=0.9, gdb=r'\\.gdb', suffix='B', layer_name='Points')
```
<br>

### **Plot CSV Function**
Converts X/Y/Z coordinates in a .csv file to a shapefile.
```py
# plot_csv(project, map_name, csv, projection, shapefile, event_data, x_name, y_name, z_name=None)
import arcpy
from pyxidust.gp import plot_csv
project = arcpy.mp.ArcGISProject(r'\\.aprx')

# output shapefile is added to map
plot_csv(project=project, map_name='Map', csv=r'\\.csv', projection=r'\\.prj',
    shapefile=r'\\.shp', event_data=r'\\event_2', x_name='X', y_name='Y',
    z_name='Z')
```
<br>

### **Plot Excel Function**
Converts X/Y/Z coordinates in an Excel workbook to a shapefile.
```py
# plot_excel(workbook, project, map_name, projection, shapefile, event_data, x_name, y_name, z_name=None, sheet=None)
import arcpy
from pyxidust.gp import plot_excel
project = arcpy.mp.ArcGISProject(r'\\.aprx')

# using the first workbook sheet and Z values
plot_excel(workbook=r'\\.xlsx', project=project, map_name='Map',
    projection=r'\\.prj', shapefile=r'\\.shp', event_data=r'\\event_3',
    x_name='X', y_name='Y', z_name='Z')

# using the third workbook sheet without Z values
plot_excel(workbook=r'\\.xlsx', project=project, map_name='Map',
    projection=r'\\.prj', shapefile=r'\\.shp', event_data=r'\\event_3',
    x_name='X', y_name='Y', sheet='Sheet 3')
```
<br>

### **Print Info Function**
Prints map/layout/layer names and data sources in an ArcGIS PRO project.
```py
# print_info(project)
import arcpy
from pyxidust.gp import print_info
project = arcpy.mp.ArcGISProject(r'\\.aprx')

# useful for projects that will not open due to memory limitations
print_info(project=project)
```
<br>

### **Print Layers Function**
Prints all layer properties in an ArcGIS PRO project.
```py
# print_layers(project, map_name)
import arcpy
from pyxidust.gp import print_layers
project = arcpy.mp.ArcGISProject(r'\\.aprx')
print_layers(project=project, map_name='Map')
```
<br>

### **Remove Layers Function**
Removes layers from a map in an ArcGIS PRO project.
```py
# remove_layers(project, map_, layers)
import arcpy
from pyxidust.gp import remove_layers
project = arcpy.mp.ArcGISProject(r'\\.aprx')
map_ = project.listMaps('Map')[0]
remove_layers(project=project, map_=map_, layers={'Points', 'Polygons'})
```
<br>

### **Visible Layers Function**
Turns on/off layers in an ArcGIS PRO project.
```py
# visible_layers(project, map_name, layer_index, option)
import arcpy
from pyxidust.gp import visible_layers
project = arcpy.mp.ArcGISProject(r'\\.aprx')

# turn on one layer
visible_layers(project=project, map_name='Map', layer_index=[2],
    option='on')

# turn off multiple layers
visible_layers(project=project, map_name='Map', layer_index=[3, 4, 5],
    option='off')
```
<br>

# Lidar Module
### ...

# Projects Module
### **Add Map Function**
Creates new .aprx files in an existing project directory via incremental serial numbers. Each new .aprx file contains a new map/layout which serve as
variations of the base project. For example, users may create 10 copies of an 
existing map via the 'clone' option to produce a suite of layouts with minor 
variations (such as a property boundary overlayed on historical imagery over a 
40-year period). The 'scratch' option will produce a certain quantity of
basemaps from the 'SIZES' in the .config module to be used as standalone maps
for a large project (such as utility layouts per each city block). The highest 
serial number found in the filename of an existing .aprx file in the directory 
acts as the base for all operations.
```py
# add_map(directory, option, quantity, filename=None, template=None)
from pyxidust.config import PROJECTS
from pyxidust.gp import add_map

# add three new .aprx files using a default template
add_map(directory=rf'{PROJECTS}\\20240001_GPSPoints', option='scratch',
    quantity=3, template='L_08x11')

# clone one .aprx file many times to create a suite of layouts
add_map(directory=rf'{PROJECTS}\\20240001_GPSPoints', option='clone',
    quantity=99, filename='20240001-0005_GPSPoints.aprx')
```
<br>

### **Archive Project Function**
Moves project folders from previous year to archive folder. Called by the new 
project decorator.
<br>
<br>

### **Change Element Name Function**
Updates the text property of one layout element.
```py
# change_element_name(project, map_name, layout_name, element, old_name, new_name)
import arcpy
from pyxidust.projects import change_element_name
project = arcpy.mp.ArcGISProject(r'\\.aprx')

# update the 'Draft' text to read 'Revised Draft'
change_element_name(project=project, map_name='Map', layout_name='Layout',
    element='TEXT_ELEMENT', old_name='Draft', new_name='Revised Draft')
```
<br>

### **Create Folder Function**
Creates a new project directory and clones the appropriate template. Called by 
the new project decorator.
<br>
<br>

### **Create Index Function**
Joins file metadata (name/path/modified) with layer/layout/map names via a
global ID for each .aprx file in the specified directory.
```py
# create_index(directory)
from pyxidust.projects import create_index
create_index(directory=r'\\')
```
<br>

### **Delete Project Function**
Deletes files/folders generated by ArcGIS PRO for workflows that do not require
a project.
```py
# delete_project(directory)
from pyxidust.projects import delete_project
delete_project(directory=r'\\')
```
<br>

### **Get Metadata Function**
Returns name/path/modified per a certain file extension in a directory.
```py
# get_metadata(extension, directory)
from pyxidust.projects import get_metadata
get_metadata(extension='.aprx', directory=r'\\')
```
<br>

### **Function**

```py
# 
```
<br>

### **Function**

```py
# 
```
<br>

### **Function**

```py
# 
```
<br>

### **Function**

```py
# 
```
<br>

### **Function**

```py
# 
```
<br>

### **Function**

```py
# 
```
<br>

### **Function**

```py
# 
```
<br>

### **Function**

```py
# 
```
<br>

### **Function**

```py
# 
```
<br>

### **Function**

```py
# 
```
<br>

### **Function**

```py
# 
```
<br>

# Changelog
Pyxidust version 0.0.1 was released on November 10th, 2022 under a M.I.T.
license which has since been updated to GPL3.

## **0.2.0** (date):
### Added:
- The 'Lidar' and 'Projects' modules have been added
- pyxidust.gp.add_data
- pyxidust.gp.change_source
- pyxidust.gp.clear_gdb
- pyxidust.gp.csv_to_features
- pyxidust.gp.explode_geometry
- pyxidust.gp.features_to_csv
- pyxidust.gp.increment_field
- pyxidust.gp.match_values
- pyxidust.gp.move_elements
- pyxidust.gp.remove_layers

### Deprecated:
- The 'Utils' module has been removed

### Migrated:
- pyxidust.arc.create_index >> pyxidust.projects.create_index
- pyxidust.arc.get_metadata >> pyxidust.projects.get_metadata
- pyxidust.arc.set_default >> pyxidust.projects.set_default
- pyxidust.arc.turn_off >> pyxidust.gp.visible_layers
- pyxidust.arc.zoom_to >> pyxidust.gp.layout_scale
- pyxidust.utils.get_letters >> pyxidust.gp.get_suffix
- pyxidust.utils.get_metadata >> pyxidust.gp.get_metadata
- pyxidust.utils.tk_message >> pyxidust.projects.message_window

### Renamed:
- The 'Arc' module has been renamed 'GP'

<br>

## **0.1.0** (1/23/2023):
### Added:
- pyxidust.arc.create_index
- pyxidust.arc.csv_to_gdb
- pyxidust.arc.cubic_volume
- pyxidust.arc.excel_to_gdb
- pyxidust.arc.image_to_features
- pyxidust.arc.place_anno
- pyxidust.arc.plot_csv
- pyxidust.arc.plot_excel
- pyxidust.arc.print_info
- pyxidust.arc.print_layers
- pyxidust.arc.set_default
- pyxidust.arc.turn_off
- pyxidust.arc.zoom_to
- pyxidust.utils.get_metadata

### Renamed:
- pyxidust.utils.file_rename >> change_name

<br>

## **0.0.1** (11/10/2022):
- Initial release and birth of Pyxidust!

<br>
