# Pyxidust
### Geoprocessing/lidar/project tools for ArcGIS PRO.
<br>

# Dependencies
Python 3.11+, MS Windows, ArcGIS PRO 3.0+, Pandas package
<br>

# Change Log
**0.2.0** (date):
- The 'Arc' module has been renamed 'GP' for geoprocessing and the following
functions added:
add_data, change_source, clear_gdb, csv_to_features, explode_geometry,
features_to_csv, move_elements, remove_layers

- pyxidust.arc.turn_off has been renamed to visible_layers

- pyxidust.arc.create_index has been migrated to pyxidust.projects.create_index
- pyxidust.arc.get_metadata has been migrated to pyxidust.projects.get_metadata
- pyxidust.arc.set_default has been migrated to pyxidust.projects.set_default
- pyxidust.utils.get_letters has been migrated to pyxidust.gp.get_suffix;
- pyxidust.utils.get_metadata has been migrated to pyxidust.gp.get_metadata
- pyxidust.utils.tk_message has been migrated to pyxidust.projects.message_window

- Added the 'Lidar' module

- Added the 'Projects' module

- Deprecated the 'Utils' module

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
