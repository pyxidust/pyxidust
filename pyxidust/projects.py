# Pyxidust: geoprocessing/lidar/project tools for ESRI ArcGIS PRO software
# Copyright (C) 2024  Gabriel Peck  pyxidust@pm.me
"""Project management/documentation and user coordination tools."""
###############################################################################

def add_map(directory, option, quantity, filename=None, template=None):
    """Creates new .aprx files in an existing project directory via incremental
    serial numbers. Each new .aprx file contains a new map/layout which serve
    as variations of the base project. For example, users may create 10 copies
    of an existing map via the 'clone' option to produce a suite of layouts
    with minor variations (such as a property boundary overlayed on historical
    imagery over a 40-year period). The 'scratch' option will produce a certain
    quantity of basemaps from the 'SIZES' in the .config module to be used as
    standalone maps for a large project (such as utility layouts per each city
    block). The highest serial number found in the filename of an existing
    .aprx file in the directory acts as the base for all operations.
    ---------------------------------------------------------------------------
    PARAMETERS:
    ---------------------------------------------------------------------------
    directory: str
        path to an existing project folder
    option: str
        clone - replicate the .aprx file in 'filename' to produce a similar map
        scratch - create a new .aprx file with default layers per a template
    quantity: int
        number of new .aprx files to create via 'clone' or 'scratch'
    filename: str
        existing project to use as a template if option is 'clone'
    template: str
        desired orientation and map size for new .aprx layouts found in the
        'SIZES' symbol in the .config module
    ---------------------------------------------------------------------------
    USAGE:
    ---------------------------------------------------------------------------
    from pyxidust.config import PROJECTS
    from pyxidust.gp import add_map
    # add three new .aprx files using a default template
    add_map(directory=rf'{PROJECTS}\\20240001_GPSPoints', option='scratch',
        quantity=3, template='L_08x11')
    # clone one .aprx file many times to create a suite of layouts
    add_map(directory=rf'{PROJECTS}\\20240001_GPSPoints', option='clone',
        quantity=99, filename='20240001-0005_GPSPoints.aprx')
    """

    import os
    import shutil
    import arcpy
    from pyxidust.config import PROJECT

    # get last-used/cloned serial number/title
    aprx = (([i for i in os.listdir(directory) if i.endswith('.aprx')]).pop())
    serial_base, title = aprx.replace('.aprx', '').split('_')

    if option == 'clone':
        key, title = filename.replace('.aprx', '').split('_')

    def _create_project():
        """Creates/configures a new project per each iteration."""

        path = os.path.join(directory, filename)
        source = path if option == 'clone' else rf'{PROJECT}\\{template}.aprx'
        destination = rf'{directory}\\{serial}_{title}.aprx'
        shutil.copy(source, destination)
        project = arcpy.mp.ArcGISProject(destination)

        if option == 'clone':
            clone = f'{key}_{title}'
            map_, layout = change_element_name(project=project, map_name=clone,
                layout_name=clone, element='TEXT_ELEMENT', old_name=key,
                new_name=serial)

        if option == 'scratch':
            map_, layout = change_element_name(project=project, map_name='Map',
                layout_name='Layout', element='TEXT_ELEMENT',
                old_name='SERIAL', new_name=serial)

        map_.name = f'{serial}_{title}'
        layout.name = f'{serial}_{title}'

        project.save()

    serial = new_serial(serial_base)
    for _ in range(0, quantity):
        _create_project()
        serial = new_serial(serial)

###############################################################################

def archive_project():
    """Moves project folders from previous year to archive folder. Called by
    the new project decorator.
    """

    import os
    import shutil
    from pyxidust.config import ARCHIVE, PROJECTS, YEAR

    for root, folders, files in os.walk(PROJECTS):
        for folder in folders:
            if folder.startswith(YEAR):
                pass
            else:
                print(f'Moving folder to archive:\n{folder}\n')
                shutil.copytree(folder, ARCHIVE)
                shutil.rmtree(folder, ignore_errors=False)

###############################################################################

def change_element_name(project, map_name, layout_name, element, old_name,
    new_name):
    """Updates the text property of one layout element.
    ---------------------------------------------------------------------------
    PARAMETERS:
    ---------------------------------------------------------------------------
    project:
        ArcGIS project object
    map_name: str
        map name as it appears in the catalog pane
    layout_name: str
        layout name as it appears in the catalog pane
    element: str
        type of layout element to rename: GRAPHIC_ELEMENT, LEGEND_ELEMENT,
        MAPFRAME_ELEMENT, MAPSURROUND_ELEMENT, PICTURE_ELEMENT, TEXT_ELEMENT
    old_name: str
        existing element name
    new_name: str
        new element name
    ---------------------------------------------------------------------------
    RETURNS:
    ---------------------------------------------------------------------------
    map_:
        ArcGIS map object
    layout:
        ArcGIS layout object
    ---------------------------------------------------------------------------
    USAGE:
    ---------------------------------------------------------------------------
    import arcpy
    from pyxidust.projects import change_element_name
    project = arcpy.mp.ArcGISProject(r'\\.aprx')
    # update the 'Draft' text to read 'Revised Draft'
    change_element_name(project=project, map_name='Map', layout_name='Layout',
        element='TEXT_ELEMENT', old_name='Draft', new_name='Revised Draft')
    """

    import arcpy

    map_ = project.listMaps(map_name)[0]
    layout = project.listLayouts(layout_name)[0]
    for item in layout.listElements(element, old_name):
        item.text = new_name

    project.save()

    return map_, layout

###############################################################################

def create_folder(folder_name, map_name, template):
    """Creates a new project directory and clones the appropriate template.
    Called by the new project decorator.
    """

    import os
    import shutil
    from pyxidust.config import PROJECTS, TEMPLATES

    directory = (f'{PROJECTS}\\{folder_name}')
    source = (f'{TEMPLATES}\\{template}.aprx')
    destination = (f'{directory}\\{map_name}')
    os.mkdir(directory)
    shutil.copy(source, destination)

    return directory

###############################################################################

def create_index(directory):
    """Joins file metadata (name/path/modified) with layer/layout/map names via
    a global ID for each .aprx file in the specified directory.
    ---------------------------------------------------------------------------
    PARAMETERS:
    ---------------------------------------------------------------------------
    directory: str
        path to a root project folder
    ---------------------------------------------------------------------------
    USAGE:
    ---------------------------------------------------------------------------
    from pyxidust.projects import create_index
    create_index(directory=r'\\')
    """

    import arcpy
    import pandas
    from pandas import merge, read_csv

    map_frames = []
    map_layers = []
    map_layouts = []

    # get/read metadata/create projects
    get_metadata('.aprx', directory)
    df = read_csv(filepath_or_buffer=rf'{directory}\\Catalog.csv')
    projects = [arcpy.mp.ArcGISProject(i) for i in df['FILE_PATH']]

    # use ID/project object to get/write ID/attributes to list
    for identifier, project in enumerate(projects, start=1):
        for map_ in project.listMaps():
            map_frames.append(f'{str(identifier)}|{map_.name}')
            for layer in map_.listLayers():
                map_layers.append(f'{str(identifier)}|{layer.name}')
        for layout in project.listLayouts():
            map_layouts.append(f'{str(identifier)}|{layout.name}')

    # write field names/attributes to newlines
    with open(rf'{directory}\\Maps.csv', 'w+') as file:
        map_index = '\n'.join(map_frames)
        file.write(f'ID|MAP_NAME\n{map_index}')

    with open(rf'{directory}\\Layers.csv', 'w+') as file:
        layer_index = '\n'.join(map_layers)
        file.write(f'ID|LAYER_NAME\n{layer_index}')

    with open(rf'{directory}\\Layouts.csv', 'w+') as file:
        layout_index = '\n'.join(map_layouts)
        file.write(f'ID|LAYOUT_NAME\n{layout_index}')

    # read-in structured newlines to perform merge assigning the global
    # ID to the index values of the dataframes
    df_info = read_csv(filepath_or_buffer=rf'{directory}\\Catalog.csv',
        sep=',', index_col='ID')
    df_layers = read_csv(filepath_or_buffer=rf'{directory}\\Layers.csv',
        sep='|', index_col='ID')
    df_layouts = read_csv(filepath_or_buffer=rf'{directory}\\Layouts.csv',
        sep='|', index_col='ID')
    df_maps = read_csv(filepath_or_buffer=rf'{directory}\\Maps.csv',
        sep='|', index_col='ID')

    # join file metadata to ArcGIS attributes and write to csv; output files
    # can be imported as separate sheets into an Excel notebook to create a
    # finished product; Excel does not support the number of rows created when
    # joining as one table with many-to-many relationships
    layers_merge = merge(left=df_layers, right=df_info, how='left', on=None,
        left_on='ID', right_on='ID')
    layers_merge.to_csv(path_or_buf=rf'{directory}\\LayersJoined.csv', sep='|')
    layouts_merge = merge(left=df_layouts, right=df_info, how='left', on=None,
        left_on='ID', right_on='ID')
    layouts_merge.to_csv(path_or_buf=rf'{directory}\\LayoutsJoined.csv',
        sep='|')
    maps_merge = merge(left=df_maps, right=df_info, how='left', on=None,
        left_on='ID', right_on='ID')
    maps_merge.to_csv(path_or_buf=rf'{directory}\\MapsJoined.csv', sep='|')

###############################################################################

def delete_project(directory):
    """Deletes files/folders generated by ArcGIS PRO for workflows that do not
    require a project.
    ---------------------------------------------------------------------------
    PARAMETERS:
    ---------------------------------------------------------------------------
    directory: str
        path to a folder containing a pro project structure
    ---------------------------------------------------------------------------
    USAGE:
    ---------------------------------------------------------------------------
    from pyxidust.projects import delete_project
    delete_project(directory=r'\\')
    """

    import os
    import shutil
    from pyxidust.config import DEFAULT_FILES, DEFAULT_FOLDERS

    for root, folders, files in os.walk(directory):
        for folder in folders:
            for item in DEFAULT_FOLDERS:
                if folder.startswith(item) or folder.endswith(item):
                    shutil.rmtree(os.path.join(root, folder))
        for file in files:
            for item in DEFAULT_FILES:
                if file.startswith(item) or file.endswith(item):
                    os.remove(os.path.join(root, file))

###############################################################################

def get_metadata(extension, directory):
    """Returns name/path/modified per a certain file extension in a directory.
    ---------------------------------------------------------------------------
    PARAMETERS:
    ---------------------------------------------------------------------------
    extension: str
        file extension to search for
    directory: str
        path to a folder to search in
    ---------------------------------------------------------------------------
    USAGE:
    ---------------------------------------------------------------------------
    from pyxidust.projects import get_metadata
    get_metadata(extension='.aprx', directory=r'\\')
    """

    import datetime
    import os
    import pandas
    from pandas import concat, DataFrame

    name = []
    path = []
    time = []

    for root, folders, files in os.walk(directory):
        for file in files:
            if file.endswith(extension):
                location = os.path.join(root, file)
                path.append(location)
                name.append(file)
                unix_time = os.path.getmtime(location)
                utc_time = datetime.datetime.utcfromtimestamp(unix_time)
                time.append(utc_time)
                df1 = DataFrame(data=name, columns=['FILE_NAME'])
                df2 = DataFrame(data=path, columns=['FILE_PATH'])
                df3 = DataFrame(data=time, columns=['LAST_MODIFIED'])
                df4 = concat(objs=[df1, df2, df3], axis='columns')
                df4.index += 1
                df4.index.name = 'ID'
                df5 = df4.to_csv(path_or_buf=rf'{directory}\\Catalog.csv')

###############################################################################

def get_serial():
    """Returns an incremented serial number from a file. Called by the new
    project decorator."""

    from pyxidust.config import SERIALS, YEAR

    with open(SERIALS, 'r') as file:
        serial = (f'{YEAR}{str(int(file.read()) + 1)}')
    with open(SERIALS, 'w+') as file:
        file.write(serial)

    return serial

###############################################################################

def import_map(project, mxd, serial_number=None):
    """Converts a layout in a .mxd file to the ArcGIS PRO format and assigns
    a serial number to the new map/layout.
    ---------------------------------------------------------------------------
    PARAMETERS:
    ---------------------------------------------------------------------------
    project:
        ArcGIS project object
    mxd: path
        Fully-qualified/raw file path to a .mxd file
    serial_number: str
        Serial number in format 'YYYYRRRR' or 'YYYYRRRR-CCCC' where 'YYYY' is
        the four-digit year, 'RRRR' is the global ID, and 'CCCC' is a counter
        for multiple records belonging to the same project. If serial_number
        is equal to None, a new serial number will be generated using the base
        number in the .txt file. Supports '-0000' counter values up to 9999. At
        9999, a new serial number will be generated using a '-0001' suffix.
    ---------------------------------------------------------------------------
    USAGE:
    ---------------------------------------------------------------------------
    import arcpy
    project_ = arcpy.mp.ArcGISProject(r'\\.aprx')
    import_map(project=project_, mxd=r'\\.mxd', serial_number='20201234-0001')
    """

    import arcpy

    # choose serial number format
    if serial_number is None:
        serial_new = new_serial()
    else:
        serial_new = new_serial(serial_number)    

    # close open items/get existing maps/layouts
    project.closeViews()
    maps_old = project.listMaps()
    layouts_old = project.listLayouts()

    # new map.name == .mxd dataframe name
    # new layout.name == .mxd filename
    project.importDocument(document_path=mxd)
    project.save()

    # get total maps/layouts
    maps_total = project.listMaps()
    layouts_total = project.listLayouts()

    # get/rename new map objects   
    for map_ in maps_total:
        if map_ not in maps_old:
            map_.name = serial_new

    # get/rename new layout objects
    for layout in layouts_total:
        if layout not in layouts_old:
            layout.name = serial_new

    project.save()

###############################################################################

def log_project(description, name, serial):
    """Writes project information to the catalog. Called by
    the new project decorator."""

    import getpass
    import time
    from pyxidust.config import CATALOG

    map_serial = (f'{serial}-0001')
    folder_name = (f'{serial}_{name}')
    map_name = (f'{map_serial}_{name}.aprx')
    creator = getpass.getuser()
    stamp = time.strftime('%m/%d/%y,%H:%M:%S', time.localtime())

    with open(CATALOG, 'a') as file:
        file.write(f'\n{serial},{name},{description},{creator},{stamp}')

    return folder_name, map_name, map_serial

###############################################################################

def memory_swap(project):
    """Deletes an existing ArcGIS PRO project object and returns a replacement.
    Acts as a file lock workaround and alternative to project.saveACopy().
    ---------------------------------------------------------------------------
    PARAMETERS:
    ---------------------------------------------------------------------------
    project:
        ArcGIS project object
    ---------------------------------------------------------------------------
    USAGE:
    ---------------------------------------------------------------------------
    import arcpy
    from pyxidust.arc import memory_swap
    project_ = arcpy.mp.ArcGISProject(r'\\')
    project = memory_swap(project=project_)
    """
    
    import arcpy

    project_path = project.filePath
    del project
    project_new = arcpy.mp.ArcGISProject(project_path)
    return project_new

###############################################################################

def message_window(option, title, message):
    """Wrapper for Tkinter error messages."""

    from tkinter import messagebox, Tk

    options = {
        'askokcancel': messagebox.askokcancel,
        'askquestion': messagebox.askquestion,
        'askretrycancel': messagebox.askretrycancel,
        'askyesno': messagebox.askyesno,
        'showerror': messagebox.showerror,
        'showinfo': messagebox.showinfo,
        'showwarning': messagebox.showwarning
    }

    for key, value in options.items():
        if option == key:
            error = value

    root = Tk()
    root.withdraw()
    error(title, message)

###############################################################################

def name_elements(directory, map_name, map_serial, name):
    """Updates map element names with project information. Called by
    the new project decorator."""

    import arcpy

    project = arcpy.mp.ArcGISProject(f'{directory}\\{map_name}')
    map_ = project.listMaps('Map')[0]
    layout = project.listLayouts('Layout')[0]

    for element in layout.listElements('TEXT_ELEMENT', '*'):
        if element.text == 'SERIAL_NUMBER':
            element.text = map_serial
        if element.text == 'TITLE':
            element.text = name

    if map_.name == 'Map':
        map_.name = map_serial
    if layout.name == 'Layout':
        layout.name = map_serial

    project.save()

###############################################################################

# @new_project
def new_project(function):
    import functools
    @functools.wraps(function)
    def wrapper(description, name, template, *args, **kwargs):
        """Creates a new ArcGIS PRO project and workspace. Relevant project
        information is written to a catalog. A unique identifier cascades
        through all parts of the process. Use this decorator to wrap a
        geoprocessing pipeline to fully automate a workflow, or use it
        as a standalone project creation tool.
        -----------------------------------------------------------------------
        PARAMETERS:
        -----------------------------------------------------------------------
        description: str
            project purpose written to catalog entry
        name: str
            project title used in file/folder name
        template: str
            desired orientation and map size for new project layout
        -----------------------------------------------------------------------
        USAGE:
        -----------------------------------------------------------------------
        # *args, **kwargs = function(description, name, template)
        processed_data, results_value = geoprocessing_pipeline(
            description, name, template, data_in, values)
        """

        # wrapper scope
        archive_project()
        validate_project(description, name, template)
        serial = get_serial()
        folder_name, map_name, map_serial = log_project(description,
            name, serial)
        directory = create_folder(folder_name, map_name, template)
        name_elements(directory, map_name, map_serial, name)

        # function scope
        result = function(*args, **kwargs)

        return result

    return wrapper

###############################################################################

def new_serial(serial=None):
    """With systems that implement a serial number for record ID, compares user
    input to a .txt file containing a base serial number and increments the
    user input accordingly.
    ---------------------------------------------------------------------------
    PARAMETERS:
    ---------------------------------------------------------------------------
    serial: str
        Serial number in format 'YYYYRRRR' or 'YYYYRRRR-CCCC' where 'YYYY' is
        the four-digit year, 'RRRR' is the global ID, and 'CCCC' is a counter
        for multiple records belonging to the same project. If serial_number
        is equal to None, a new serial number will be generated using the base
        number in the .txt file. Supports '-0000' counter values up to 9999. At
        9999, a new serial number will be generated using a '-0001' suffix.
    ---------------------------------------------------------------------------
    USAGE:
    ---------------------------------------------------------------------------
    from pyxidust.projects import new_serial
    # pull a new serial number
    new_serial()
    # increment an existing serial number
    new_serial(serial='20231234-0001')
    """

    # pull new serial number
    if serial is None:
        serial_new = (f'{get_serial()}-0001')

    # use existing serial number
    if serial is not None:
        validate_serial(string=serial)
        # increment base serial number
        if len(serial) == 8:
            serial_new = (f'{serial}-0001')
        # increment '-' serial number
        elif len(serial) == 13:
            base, suffix = serial.split('-')
            suffix_int = (int(suffix)) + 1
            suffix_new = str(suffix_int).zfill(4)
            if suffix_int > 9999:
                serial_new = (f'{get_serial()}-0001')
            else:
                serial_new = (f'{base}-{suffix_new}')

    return serial_new

###############################################################################

def set_default(project, home, gdb, toolbox):
    """Updates home folder/default geodatabase/toolbox in an ArcGIS PRO
    project.
    ---------------------------------------------------------------------------
    PARAMETERS:
    ---------------------------------------------------------------------------
    project:
        ArcGIS project object
    home: path
        path to a new home folder for the PRO project
    gdb: path
        path to a new default geodatabase for the PRO project
    toolbox: path
        path to a new default toolbox for the PRO project
    ---------------------------------------------------------------------------
    USAGE:
    ---------------------------------------------------------------------------
    import arcpy
    from pyxidust.projects import set_default
    project_ = arcpy.mp.ArcGISProject(r'\\.aprx')
    set_default(project=project_, home=r'\\folder', gdb=r'\\.gdb',
        toolbox=r'\\.tbx')
    """
    
    import arcpy

    project.homeFolder = home
    project.defaultGeodatabase = gdb
    project.defaultToolbox = toolbox

    project.save()

###############################################################################

def validate_project(description, name, template):
    """Performs data validation of user arguments. Called by
    the new project decorator."""

    from sys import exit
    from string import punctuation as SPECIAL
    from pyxidust.config import SIZES

    if any(i.isnumeric() for i in description):
        error = 'Description does not accept numbers.'
    elif any(i in SPECIAL for i in description):
        error = 'Description does not accept special characters.'
    elif len(description) > 50:
        error = 'Description must be 50 characters or less.'

    elif any(i.isspace() for i in name):
        error = 'Name does not accept spaces.'
    elif any(i in SPECIAL for i in name):
        error = 'Name does not accept special characters.'
    elif len(name) > 15:
        error = 'Name must be 15 characters or less.'

    elif template not in SIZES:
        error = (f'Invalid template size for {template}')

    if error is not None:
        message_window(option='showerror', title='ERROR:', message=error)
        restart = "'Check user input arguments and try again'"
        message_window(option='showerror', title='ERROR:', message=restart)
        exit()

###############################################################################

def validate_serial(string):
    """Enforces population of numeric characters in a serial number.
    ---------------------------------------------------------------------------
    PARAMETERS:
    ---------------------------------------------------------------------------
    string: str
        serial number in format 'YYYYRRRR' or 'YYYYRRRR-CCCC' where 'YYYY' is
        the four-digit year, 'RRRR' is the global ID, and 'CCCC' is a counter
        for multiple records belonging to the same project.
    ---------------------------------------------------------------------------
    USAGE:
    ---------------------------------------------------------------------------
    from pyxidust.utils import validate_serial
    validate_serial(string='20201234-0001')
    """

    from string import punctuation as SPECIAL

    def _check_numeric(value):
        """Standard character validation."""
        if any(i.isalpha() for i in value):
            error_message = 'Serial number must not contain letters'
            message_window('showinfo', 'ERROR:', error_message)
        elif any(i.isspace() for i in value):
            error_message = 'Serial number cannot have spaces'
            message_window('showinfo', 'ERROR:', error_message)
        elif any(i in SPECIAL for i in value):
            error_message = 'Serial number cannot have special characters'
            message_window('showinfo', 'ERROR:', error_message)
        else:
            pass

    def _format_error():
        """Error handling if user inputs serial # in wrong format."""
        error_message = 'Serial # format is 00000000 or 00000000-0000'
        message_window(option='showinfo', title='ERROR', message=error_message)

    # base serial
    if len(string) == 8:
        base = string
        _check_numeric(value=base)

    # base/counter serial
    elif len(string) == 13 and string.count('-') == 1 and string[8] == '-':
        base, suffix = string.split('-')
        _check_numeric(value=base)
        _check_numeric(value=suffix)

    # all other cases
    else:
        _format_error()
