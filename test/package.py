# pyxidust library full unit test
# Gabriel Peck 2023 (MIT license)

###############################################################################
# ARC MODULE:
###############################################################################

from pyxidust import arc

# -----------------------------------------------------------------------------
# add_data(pro_obj, map_name, option, layers=None, lyr_idx=None, gdb=None)
arc.add_data(pro_obj, map_name, option, layers=None, lyr_idx=None, gdb=None)
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# change_source(project, dataset, layer, option, old_source, new_source)
arc.change_source(pro_obj, dataset, layer, option, old_source, new_source)
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# clear_gdb(gdb)
arc.clear_gdb(gdb)
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# create_index(directory)
arc.create_index(directory)
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# csv_to_features(input_file, output_features, crs)
arc.csv_to_features(input_file, output_features, crs)
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# csv_to_gdb(csv, gdb, table)
arc.csv_to_gdb(csv, gdb, table)
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# cubic_volume(original, current, gdb, polygons)
arc.cubic_volume(original, current, gdb, polygons)
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# excel_to_gdb(workbook, gdb, table, sheet=None)
arc.excel_to_gdb(workbook, gdb, table, sheet=None)
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# explode_geometry(dataset, gdb)
arc.explode_geometry(dataset, gdb)
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# features_to_csv(input_features, output_file, option)
arc.features_to_csv(input_features, output_file, option)
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# move_elements(pro_obj, lay_obj, ele_type, wildcard)
arc.move_elements(pro_obj, lay_obj, ele_type, wildcard)
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# place_anno(pro_obj, map_name, lay_name, fra_name, lyr_idx, adjust, gdb,
#     suffix, lyr_name=None)
arc.place_anno(pro_obj, map_name, lay_name, fra_name, lyr_idx, adjust, gdb,
    suffix, lyr_name=None)
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# plot_csv(pro_obj, map_name, csv, crs, output, x_name, y_name, z_name=None)
arc.plot_csv(pro_obj, map_name, csv, crs, output, x_name, y_name, z_name=None)
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# plot_excel(workbook, pro_obj, map_name, crs, output, x_name, y_name,
#         z_name=None, sheet=None)
arc.plot_excel(workbook, pro_obj, map_name, crs, output, x_name, y_name,
        z_name=None, sheet=None)
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# print_info(pro_obj)
arc.print_info(pro_obj)
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# print_layers(pro_obj, map_name)
arc.print_layers(pro_obj, map_name)
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# remove_layers(pro_obj, map_obj, layers)
arc.remove_layers(pro_obj, map_obj, layers)
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# set_default(pro_obj, home, gdb, toolbox)
arc.set_default(pro_obj, home, gdb, toolbox)
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# turn_off(pro_obj, map_name, lyr_idx)
arc.turn_off(pro_obj, map_name, lyr_idx)
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# zoom_to(pro_obj, map_name, lay_name, fra_name, lyr_idx, adjust)
arc.zoom_to(pro_obj, map_name, lay_name, fra_name, lyr_idx, adjust)
# -----------------------------------------------------------------------------

###############################################################################
# LIDAR MODULE:
###############################################################################

# run the lidartools script at 'pyxidust/scripts/lidartools.py'

###############################################################################
# PROJECTS MODULE:
###############################################################################

from pyxidust import projects
from pyxidust.projects import new_project

@new_project
def unit_test(...):
    # do stuff


# -----------------------------------------------------------------------------
# unit_test(...)
unit_test(...)
# -----------------------------------------------------------------------------

# pyxidust.projects.clone_project()
# pyxidust.projects.delete_project()
# pyxidust.projects.import_map()

###############################################################################
# UTILS MODULE:
###############################################################################

from pyxidust import utils

# -----------------------------------------------------------------------------
# change_name(extension, directory, serial_file)
utils.change_name(extension, directory, serial_file)
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# clear_folder(directory, option)
utils.clear_folder(directory, option)
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# collapse_path(path)
utils.collapse_path(path)
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# file_parse(option, read_file, write_file=None, find_chars=None,
#     replace_chars=None, split_chars=None)
utils.file_parse('1','text.txt')
utils.file_parse('2','text.txt',split_chars=',')
utils.file_parse('3','text.txt')
utils.file_parse('4','text.txt',find_chars='s',replace_chars='#',split_chars=',')
utils.file_parse('5','text.txt',find_chars='s',replace_chars='#')
utils.file_parse('6','text.txt',write_file='output.txt',split_chars=',')
utils.file_parse('7','text.txt',write_file='output.txt')
utils.file_parse('8','text.txt',write_file='output.txt',find_chars='s',
    replace_chars='#',split_chars=',')
utils.file_parse('9','text.txt',write_file='output.txt',find_chars='s',
    replace_chars='#')
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# get_letters(string)
utils.get_letters(string)
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# get_metadata(extension, directory)
utils.get_metadata(extension, directory)
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# get_numbers(string)
utils.get_numbers(string)
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# get_time(option)
utils.get_time(option)
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# join_csv(directory, join_file)
utils.join_csv(directory, join_file)
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# new_serial(serial_file, serial_number=None)
utils.new_serial(serial_file, serial_number=None)
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# session_args(*args, **kwargs)
utils.session_args(*args, **kwargs)
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# session_in(session_data)
utils.session_in(session_data)
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# session_out(arguments, session_data)
utils.session_out(arguments, session_data)
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# trim_scale(csv_in, csv_out, columns, index, scale)
utils.trim_scale(csv_in, csv_out, columns, index, scale)
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# validate_serial(string)
utils.validate_serial(string)
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# validate_string(length, option, text)
utils.validate_string(length, option, text)
# -----------------------------------------------------------------------------

print('Unit test has executed successfully')
end = input('Press any key to exit')
