# Pyxidust: geoprocessing/lidar/project tools for ESRI ArcGIS PRO software
# Copyright (C) 2024  Gabriel Peck  pyxidust@pm.me
###############################################################################

def add_map(directory, filename, option, quantity, template=None):
    """Adds new .aprx files to an existing project directory and increments the
    existing serial numbers. If the clone option is selected users can choose
    any .aprx file in the directory as a template and the last .aprx file in
    the directory will determine the last used serial number. This
    functionality acts as a guard to prevent users from overwriting existing
    files.
    -----------
    PARAMETERS:
    -----------
    directory: str
        path to a project folder
    filename: str
        name and extension of an .aprx file in the directory
    option: str
        clone - replicate the .aprx file in 'filename' to produce a similar map
        scratch - create a new .aprx file with default layers per a template
    quantity: str
        enter a value of '1' to create one .aprx file; enter a value greater
        than '1' to create a series of .aprx files; several hundred maps can
        be created at once, or more if your project requires it
    template: str
        desired orientation and map size for new .aprx layouts; sizes match the
        templates in 'pyxidust/templates/newproject/templates'
    ------
    USAGE:
    ------
    from pyxidust.config import PROJECTS
    # if option == 'clone' no template argument is provided
    add_map(directory=f'{PROJECTS}\\20232179_GPSPoints',
        filename='20232179-0003_GPSPoints.aprx', option='clone', quantity='3')
    # if option == 'scratch' provide only one template size
    add_map(directory=f'{PROJECTS}\\20232179_GPSPoints',
        filename='20232179-0002_GPSPoints.aprx', option='scratch', 
        quantity='99', template='L_08x11')
    """
    
    import os
    import shutil
    import arcpy

    from pyxidust.projects import new_serial
    from pyxidust.config import LAYOUTS
    
    # filter directory and return filename of 'bottom' .aprx file
    aprx = (([i for i in os.listdir(directory) if i.endswith('.aprx')]).pop())

    # get last-used serial number in directory from 'bottom' .aprx file
    serial_name_last, _ = aprx.replace('.aprx', '').split('_')
    _, serial_last = serial_name_last[:3], serial_name_last[3:]

    # get project details and layout element name
    serial_name, title = filename.replace('.aprx', '').split('_')
    _, serial_old = serial_name[:3], serial_name[3:]
    
    def _create_project():
        
        size = (f'{template}.aprx')
        aprx_old = os.path.join(directory, filename)
        aprx_new = (f'{serial_new}_{title}.aprx')
        source = aprx_old if option == 'clone' else rf'{LAYOUTS}\\{size}.aprx'
        destination = (rf'{directory}\\{aprx_new}')
        
        shutil.copy(source, destination)
        project = arcpy.mp.ArcGISProject(destination)
        project_new = (f'{serial_new}_{title}')
        
        if option == 'clone':
            project_old = (f'{serial_old}_{title}')
            map_ = project.listMaps(project_old)[0]
            layout = project.listLayouts(project_old)[0]
            map_.name = project_new
            layout.name = project_new
            for element in layout.listElements('TEXT_ELEMENT', '*'):
                if element.text == serial_old:
                    element.text = serial_new
        
        if option == 'scratch':
            map_ = project.listMaps('Map')[0]
            layout = project.listLayouts('Layout')[0]
            map_.name = project_new
            layout.name = project_new
            for element in layout.listElements('TEXT_ELEMENT', '*'):
                if element.text == 'SERIAL_NUMBER':
                    element.text = serial_new
        
        project.save()
    
    # create new projects via incrementing serial numbers;
    # start with last used serial in project directory
    serial_new = new_serial(serial_last)

    for _ in range(0, int(quantity)):
        _create_project()
        serial_new = new_serial(serial_new)

###############################################################################

def archive_project():
    """Moves projects from previous year to archive folder."""

    import os
    import shutil
    from pyxidust.config import ARCHIVE, PROJECTS, YEAR

    for root, dirs, files in os.walk(PROJECTS):
        for dir_ in dirs:
            if dir_.startswith(YEAR):
                pass
            else:
                print(f'Moving folder to archive:\n{dir_}')
                shutil.copytree(dir_, ARCHIVE)
                shutil.rmtree(dir_, ignore_errors=False)

###############################################################################

def create_folder(folder_name, map_name, template):
    """Creates folder structure and clones pro project template."""

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
    """Joins file metadata (name/path/modified) with layers/layouts/maps via a
    global ID for each .aprx file in the specified directory.
    -----------
    PARAMETERS:
    -----------
    directory: path
        path to a directory containing files with an .aprx extension
    ------
    USAGE:
    ------
    from pyxidust.gp import create_index
    create_index(directory=r'\\folder')
    """
    
    import arcpy
    import pandas

    from pandas import merge, read_csv
    from pyxidust.projects import get_metadata

    # create new lists for each project chunk
    # when using outside of function scope
    map_frames = []
    map_layers = []
    map_layouts = []
    
    # get file name/path/modified
    get_metadata('.aprx', directory)
    # read file metadata into pandas dataframe ('df')
    df = read_csv(filepath_or_buffer=rf'{directory}\\Catalog.csv')
    # create list of ArcGIS PRO project objects
    projects = [arcpy.mp.ArcGISProject(i) for i in df['FILE_PATH']]
    
    # return tuples with ID/project object
    for identifier, project in enumerate(projects, start=1):

        maps = project.listMaps()
        layouts = project.listLayouts()

        # get/write ID/attributes to list
        for _maps in maps:
            layers = _maps.listLayers()
            map_text = str(identifier) + '|' + _maps.name
            map_frames.append(map_text)
            for layer in layers:
                layer_text = str(identifier) + '|' + layer.name
                map_layers.append(layer_text)

        for layout in layouts:
            layout_text = str(identifier) + '|' + layout.name
            map_layouts.append(layout_text)

    # write field names/attributes to newlines
    with open(rf'{directory}\\Maps.csv', 'w+') as file:
        file.write('ID|MAP_NAME\n')
        for s in map_frames:
            file.write('%s\n' % s)

    with open(rf'{directory}\\Layers.csv', 'w+') as file:
        file.write('ID|LAYER_NAME\n')
        for s in map_layers:
            file.write('%s\n' % s)

    with open(rf'{directory}\\Layouts.csv', 'w+') as file:
        file.write('ID|LAYOUT_NAME\n')
        for s in map_layouts:
            file.write('%s\n' % s)
    
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
    """Deletes .aprx file and associated data for workflows that do not require
    a pro project.
    -----------
    PARAMETERS:
    -----------
    directory: str
        path to a folder containing a pro project structure
    ------
    USAGE:
    ------
    delete_project(directory=r'\\')
    """
    
    import os
    import shutil

    for root, folders, files in os.walk(directory):
        for folder in folders:
            if folder == '.backups' or folder == 'Index' or folder == 'GpMessages':
                shutil.rmtree(os.path.join(root, folder))
        for file in files:
            if file.ednswith('.aprx'):
                os.remove(os.path.join(root, file))

###############################################################################

def get_metadata(extension, directory):
    """Crawls a directory and returns metadata per a certain file extension.
    -----------
    PARAMETERS:
    -----------
    extension: str
        file extension to search for in the directory
    directory: path
        path to a directory containing files of a certain extension
    ------
    USAGE:
    ------
    from pyxidust.gp import get_metadata
    get_metadata(extension='.jpg', directory=r'\\folder')
    """
    
    import datetime
    import os
    import pandas
    
    name = []
    path = []
    time = []
    
    catalog = (f'{directory}\\Catalog.csv')

    # loop through directory returning the fully qualified path name to a file
    # filtered by its extension
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(extension):
                # get full path of file
                location = os.path.join(root, file)
                # write file path to list
                path.append(location)
                # write file name to list
                name.append(file)
                # get UNIX time in seconds elapsed
                unix_time = os.path.getmtime(location)
                # convert UNIX time to UTC time
                utc_time = datetime.datetime.utcfromtimestamp(unix_time)
                # write UTC time to list
                time.append(utc_time)
                # read name list into data frame
                df1 = pandas.DataFrame(name, columns=['FILE_NAME'])
                # read path list into data frame
                df2 = pandas.DataFrame(path, columns=['FILE_PATH'])
                # read time list into data frame
                df3 = pandas.DataFrame(time, columns=['LAST_MODIFIED'])
                # combine data frames 1-3
                df4 = pandas.concat([df1, df2, df3], axis='columns')
                # shift index to start at one during initial crawl
                # increment this index anytime you change file type
                # or directory location to maintain a global ID
                df4.index += 1
                # set global 'ID' field name
                df4.index.name = 'ID'
                # write output to file
                df5 = df4.to_csv(catalog)

###############################################################################

def get_serial():
    """Read/increment counter and return a serial number."""

    from pyxidust.config import SERIALS, YEAR

    with open(SERIALS, 'r') as file:
        serial = (f'{YEAR}{str(int(file.read()) + 1)}')

    with open(SERIALS, 'w+') as file:
        file.write(serial)

    return serial

###############################################################################

def import_map(pro_obj, mxd, serial_file, serial_number=None):
    """Converts a layout in a .mxd file to the ArcGIS PRO format and assigns
    a serial number to the new map/layout.
    -----------
    PARAMETERS:
    -----------
    pro_obj:
        ArcGIS project object
    mxd: path
        Fully-qualified/raw file path to a .mxd file
    serial_file: path
        Fully-qualified/raw file path to a .txt file containing one-line of
        text representing a base serial number in format 'YYYYRRRR' where
        'YYYY' is the four-digit year and 'RRRR' is the global ID.
    serial_number: str
        Serial number in format 'YYYYRRRR' or 'YYYYRRRR-CCCC' where 'YYYY' is
        the four-digit year, 'RRRR' is the global ID, and 'CCCC' is a counter
        for multiple records belonging to the same project. If serial_number
        is equal to None, a new serial number will be generated using the base
        number in the .txt file. Supports '-0000' counter values up to 9999. At
        9999, a new serial number will be generated using a '-0001' suffix.
    ------
    USAGE:
    ------
    import arcpy
    project_ = arcpy.mp.ArcGISProject(r'\\.aprx')
    import_map(pro_obj=project_, mxd=r'\\.mxd', serial_file=r'\\.txt',
        serial_number='20201234-0001')
    """

    import arcpy
    from pyxidust.projects import new_serial

    # choose serial number format
    if serial_number == None:
        serial_new = new_serial(serial_file)
    else:
        serial_new = new_serial(serial_file, serial_number)

    # close open items
    _project = pro_obj
    _project.closeViews()

    # get existing maps/layouts
    maps_old = _project.listMaps()
    layouts_old = _project.listLayouts()

    # new map.name == .mxd dataframe name
    # new layout.name == .mxd filename
    _project.importDocument(document_path=mxd)
    _project.save()

    # get total maps/layouts
    maps_total = _project.listMaps()
    layouts_total = _project.listLayouts()

    # get/rename new map objects
    for _map in maps_total:
        if _map not in maps_old:
            _map.name = serial_new

    # get/rename new layout objects
    for _layout in layouts_total:
        if _layout not in layouts_old:
            _layout.name = serial_new

    _project.save()

###############################################################################

def log_project(description, name, serial):
    """Writes project information to the catalog."""

    import getpass, time
    from pyxidust.config import CATALOG

    map_serial = (f'{serial}-0001')
    folder_name = (f'{serial}_{name}')
    map_name = (f'{map_serial}_{name}.aprx')

    creator = getpass.getuser()
    modified = time.localtime()
    stamp = time.strftime('%m/%d/%y,%H:%M:%S', modified)

    entry = (f'\n{serial},{name},{description},{creator},{stamp}')

    with open(CATALOG, 'a') as file:
        file.write(entry)

    return folder_name, map_name, map_serial

###############################################################################

def memory_swap(project):
    """Deletes an existing ArcGIS PRO project object and returns a replacement.
    Acts as a file lock workaround and alternative to project.saveACopy().
    -----------
    PARAMETERS:
    -----------
    project:
        ArcGIS project object
    ------
    USAGE:
    ------
    import arcpy
    from pyxidust.arc import memory_swap
    project_ = arcpy.mp.ArcGISProject(r'\\')
    project = memory_swap(project=project_)
    """
    
    import arcpy

    project_path = project.filePath
    del project

    new_project = arcpy.mp.ArcGISProject(project_path)
    return new_project

###############################################################################

def message_window(option, title, message):
    """Lightweight wrapper for Tkinter error messages."""

    import tkinter as tk
    from tkinter import messagebox

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

    root = tk.Tk()
    root.withdraw()
    error(title, message)

###############################################################################

def name_elements(directory, map_name, map_serial, name):
    """Updates map element names with project information."""

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
    
    return project

###############################################################################

# @new_project
# *args, **kwargs = function(description, name, template, workflow)
def new_project(function):
    import functools
    @functools.wraps(function)
    # keywords fed to wrapper can be accessed in wrapper scope;
    # args/kwargs feed keywords from function call into function scope
    def wrapper(description, name, template, *args, **kwargs):
        """Creates a new ArcGIS PRO project and workspace. Relevant project
        information is written to a catalog. A unique identifier cascades
        through all parts of the process. Use this decorator to wrap a
        geoprocessing pipeline to fully automate a workflow, or use it
        as a standalone project creation tool."""
        # wrapper scope -------------------------------------------------------
        from sys import exit
        from pyxidust.projects import archive_project, create_folder
        from pyxidust.projects import get_serial, log_project
        from pyxidust.projects import name_elements, message_window
        from pyxidust.projects import validate_project
        # check folder age |> validate user arguments
        archive_project()
        # validation |> pass/exit program |> get serial number
        error = validate_project(description, name, template)
        if error != None:
            message_window(option='showerror', title='ERROR:', message=error)
            restart = (f"'Check user input arguments and try again'")
            message_window(option='showerror', title='ERROR:', message=restart)
            exit()
        if error == None:
            # get_serial() |> log_project()
            serial = get_serial()
            #...
            folder_name, map_name, map_serial = log_project(description, name,
                serial)
            #...
            directory = create_folder(folder_name, map_name, template)
            #...
            project = name_elements(directory, map_name, map_serial, name)
        # function scope ------------------------------------------------------
        if error == None:
            result = function(*args, **kwargs)
        # wrapper scope -------------------------------------------------------
        # if error == None:
        #     ...

###############################################################################

def new_serial(serial=None):
    """With systems that implement a serial number for record ID, compares user
    input to a .txt file containing a base serial number and increments the
    user input accordingly.
    -----------
    PARAMETERS:
    -----------
    serial: str
        Serial number in format 'YYYYRRRR' or 'YYYYRRRR-CCCC' where 'YYYY' is
        the four-digit year, 'RRRR' is the global ID, and 'CCCC' is a counter
        for multiple records belonging to the same project. If serial_number
        is equal to None, a new serial number will be generated using the base
        number in the .txt file. Supports '-0000' counter values up to 9999. At
        9999, a new serial number will be generated using a '-0001' suffix.
    ------
    USAGE:
    ------
    from pyxidust.projects import new_serial
    # pull a new serial number
    new_serial()
    # increment an existing serial number
    new_serial(serial='20231234-0001')
    """

    from pyxidust.projects import get_serial, message_window, validate_serial
    
    # pull new serial number
    if serial == None:
        serial_new = (f'{get_serial()}-0001')

    # validate user input
    if serial != None:
        validate_serial(string=serial)

    # increment base serial number
    if serial != None and len(serial) == 8:
        serial_new = (f'{serial}-0001')

    # increment '-' serial number
    elif serial != None and len(serial) == 13:
        base, suffix = serial.split('-')
        suffix_int = (int(suffix)) + 1
        suffix_new = str(suffix_int).zfill(4)
        if suffix_int > 9999:
            serial_new = (f'{get_serial()}-0001')
        else:
            serial_new = (f'{base}-{suffix_new}')

    return serial_new

###############################################################################

def set_default(pro_obj, home, gdb, toolbox):
    """Updates home folder/default geodatabase/toolbox in an ArcGIS PRO
    project.
    -----------
    PARAMETERS:
    -----------
    pro_obj:
        ArcGIS project object
    home: path
        path to a new home folder for the PRO project
    gdb: path
        path to a new default geodatabase for the PRO project
    toolbox: path
        path to a new default toolbox for the PRO project
    ------
    USAGE:
    ------
    import arcpy
    from pyxidust.projects import set_default
    project_ = arcpy.mp.ArcGISProject(r'\\.aprx')
    set_default(pro_obj=project_, home=r'\\folder', gdb=r'\\.gdb',
        toolbox=r'\\.tbx')
    """
    
    import arcpy
    
    _project = pro_obj

    _project.homeFolder = home
    _project.defaultGeodatabase = gdb
    _project.defaultToolbox = toolbox

    _project.save()

###############################################################################

def validate_project(description, name, template):
    """Performs data validation of user arguments."""

    from string import punctuation as SPECIAL
    from pyxidust.config import SIZES

    if any(i.isnumeric() for i in description):
        error = (f'Description does not accept numbers.')
    elif any(i in SPECIAL for i in description):
        error = (f'Description does not accept special characters.')
    elif len(description) > 50:
        error = (f'Description must be 50 characters or less.')
    
    elif any(i.isspace() for i in name):
        error = (f'Name does not accept spaces.')
    elif any(i in SPECIAL for i in name):
        error = (f'Name does not accept special characters.')
    elif len(name) > 15:
        error = (f'Name must be 15 characters or less.')

    elif template not in SIZES:
        error = (f'Invalid template size for {template}')

    return error

###############################################################################

def validate_serial(string):
    """Enforces population of numeric characters in a serial number.
    -----------
    PARAMETERS:
    -----------
    string: str
        serial number in format 'YYYYRRRR' or 'YYYYRRRR-CCCC' where 'YYYY' is
        the four-digit year, 'RRRR' is the global ID, and 'CCCC' is a counter
        for multiple records belonging to the same project.
    ------
    USAGE:
    ------
    from pyxidust.utils import validate_serial
    validate_serial(string='20201234-0001')
    """

    from pyxidust.gui import launch_message

    def _check_numeric(value):
        """Standard character validation."""
        if any(i.isalpha() for i in value):
            error_message = (f'Serial number must not contain letters')
            launch_message('showinfo', 'ERROR:', error_message)
        elif any(i.isspace() for i in value):
            error_message = (f'Serial number cannot have spaces')
            launch_message('showinfo', 'ERROR:', error_message)
        elif any(i in SPECIAL for i in value):
            error_message = (f'Serial number cannot have special characters')
            launch_message('showinfo', 'ERROR:', error_message)
        else:
            pass

    def _format_error():
        """Error handling if user inputs serial # in wrong format."""
        error_message = (f'Serial # format is 00000000 or 00000000-0000')
        launch_message(option='showinfo', title='ERROR', message=error_message)

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
