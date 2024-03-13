
# GP (Geoprocessing) Module
### **Add Data Function**
Adds data to a map in an ArcGIS PRO project.
```py
# add_data(pro_obj, map_name, option, layers=None, lyr_idx=None, gdb=None)
import arcpy
from pyxidust.gp import add_data
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
from pyxidust.gp import change_source
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
from pyxidust.gp import clear_gdb
clear_gdb(gdb=r'GDB.gdb')
```
<br>

### **Create Index Function**
Joins file metadata (name/path/modified) with layers/layouts/maps via a global ID for each .aprx file in the specified directory.
```py
# create_index(directory)
from pyxidust.gp import create_index
create_index(directory=r'\\folder')
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
from pyxidust.gp import cubic_volume
cubic_volume(original=r'\\', current=r'\\', gdb=r'\\.gdb', polygons='poly')
```
<br>

### **Excel To GDB Function**
Converts a Microsoft Excel workbook sheet to an ArcGIS geodatabase table.
```py
# excel_to_gdb(workbook, gdb, table, sheet=None)
from pyxidust.gp import excel_to_gdb
excel_to_gdb(workbook=r'\\.xlsx', gdb=r'\\.gdb', table='Output', sheet='Sheet 1')
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
