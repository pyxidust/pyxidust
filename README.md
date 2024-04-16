# Pyxidust
Geoprocessing/lidar/project tools for ArcGIS PRO.
<br>

# Dependencies
Python 3.11+ with Pandas package, Microsoft Windows 10+, ArcGIS PRO 3.0+
<br>

# GP (Geoprocessing) Module
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
Converts X/Y data in a .csv file to ArcGIS features and removes duplicate 
coordinate pairs.
```py
# csv_to_features(input_file, output_features, projection, event_data)
from pyxidust.gp import csv_to_features
csv_to_features(input_file=r'\\.csv', output_features=r'\\.shp',
    projection=r'\\.prj', event_data='event_1')
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
Exports each row of a multipart feature class.
```py
# explode_geometry(dataset, gdb)
from pyxidust.gp import explode_geometry
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
from pyxidust.gp import move_elements
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
from pyxidust.gp import place_anno
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
from pyxidust.gp import plot_csv
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
from pyxidust.gp import plot_excel
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
from pyxidust.gp import print_info
project = arcpy.mp.ArcGISProject(r'\\.aprx')
print_info(pro_obj=project)
```
<br>

### **Print Layers Function**
Prints the properties of all layers in a map in an ArcGIS PRO project.
```py
# print_layers(pro_obj, map_name)
import arcpy
from pyxidust.gp import print_layers
project = arcpy.mp.ArcGISProject(r'\\.aprx')
print_layers(pro_obj=project, map_name='Map')
```
<br>

### **Remove Layers Function**
Removes layers from a map in an ArcGIS PRO project.
```py
# remove_layers(pro_obj, map_obj, layers)
import arcpy
from pyxidust.gp import remove_layers
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
from pyxidust.gp import set_default
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
from pyxidust.gp import turn_off
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
from pyxidust.gp import zoom_to
project = arcpy.mp.ArcGISProject(r'\\.aprx')
zoom_to(pro_obj=project, map_name='Map', lay_name='Layout', fra_name='Map Frame',
    lyr_idx=0, adjust=1.1)
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
- pyxidust.gp.move_elements
- pyxidust.gp.remove_layers

### Deprecated:
- The 'Utils' module has been removed

### Migrated:
- pyxidust.arc.create_index >> pyxidust.projects.create_index
- pyxidust.arc.get_metadata >> pyxidust.projects.get_metadata
- pyxidust.arc.set_default >> pyxidust.projects.set_default
- pyxidust.arc.turn_off >> pyxidust.gp.visible_layers
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
