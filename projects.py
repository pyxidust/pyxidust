# pyxidust library projects module
# Gabriel Peck 2023 (MIT license)

###############################################################################

# -------------
# MODULE INDEX:
# -------------

# decorators:
# pyxidust.projects.new_project()

# helper functions (not intended to be called by user)
# pyxidust.projects.archive_project()
# pyxidust.projects.create_folder()
# pyxidust.projects.get_serial()
# pyxidust.projects.log_project()
# pyxidust.projects.name_elements()
# pyxidust.projects.tk_message()
# pyxidust.projects.validate_project()

# standalone functions (callable by user)
# pyxidust.projects.clone_project()
# pyxidust.projects.delete_project()
# pyxidust.projects.import_map()

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
        import sys
        from pyxidust.projects import archive_project, create_folder, get_serial
        from pyxidust.projects import log_project, name_elements, tk_message
        from pyxidust.projects import validate_project
        # check folder age |> validate user arguments
        archive_project()
        # validation |> pass/exit program |> get serial number
        error = validate_project(description, name, template)
        if error != None:
            tk_message(option='showerror', title='ERROR:', message=error)
            sys.exit()
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
        result = function(*args, **kwargs)
        # wrapper scope -------------------------------------------------------
        
        #...

############################### HELPER FUNCTIONS ##############################

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

def get_serial():
    """Read/increment counter and return a serial number."""

    from pyxidust.config import SERIALS, YEAR

    with open(SERIALS, 'r') as file:
        serial = (f'{YEAR}{str(int(file.read()) + 1)}')

    with open(SERIALS, 'w+') as file:
        file.write(serial)

    return serial

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

def tk_message(option, title, message):
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

def validate_project(description, name, template):
    """Performs data validation of user arguments."""

    from string import punctuation as SPECIAL
    from pyxidust.config import LAYOUTS

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

    elif template not in LAYOUTS:
        error = (f'Invalid template size for {template}')

    return error

############################# STANDALONE FUNCTIONS ############################

# FUNCTIONALITY NOT AVAILABLE IN ARCGIS PRO
# def clone_project(old_project, new_project):
#     """Reproduces an ArcGIS PRO project. Useful when the contents of a project
#     are needed for further work, but the project will not open due to memory
#     limitations (large project with many maps/layouts/layers).
#     -----------
#     PARAMETERS:
#     -----------
#     old_project:
#         ArcGIS project object that will not open or is unresponsive
#     new_project:
#         ArcGIS project object to replace the old_project
#     ------
#     USAGE:
#     ------
#     import arcpy
#     project_old = arcpy.mp.ArcGISProject(path)
#     project_new = arcpy.mp.ArcGISProject(path)
#     clone_project(old_project=project_old, new_project=project_new)
#     """

#     import arcpy
#     from pyxidust.arc import add_data

#     project = old_project
#     layouts = project.listLayouts()
#     layer_names = []
#     info = {}
    
#     # assign unique id to each group of maps/layouts/layers
#     for identifier, layout in enumerate(layouts):
#         # get map name tied to a certain layout
#         mapframe = layout.listElements('MAPFRAME_ELEMENT')[0]
#         map_name = mapframe.map.name
#         # get layer objects
#         map_ = project.listMaps(map_name)[0]
#         layers = map_.listLayers()
#         # position of layers from top (0) to bottom
#         layer_order = 0
#         # filter layers and append position/name/source
#         for layer in layers:
#             if layer.isFeatureLayer == True or layer.isRasterLayer == True:
#                 layer_names.append((layer_order, layer.name, layer.dataSource))
#             # next layer
#             layer_order += 1
#         # write info to project dictionary
#         info[identifier] = (map_name, layout.name, layer_names)

#     # recreate old project
#     project = new_project

#     # unpack/loop project info
#     for identifier, (map_name, layout_name, layers) in info.items():
#         # create new map in new project
#         project.createMap(name=map_name, map_type='MAP')
#         # create new layout in new project
#         ...
#         # unpack/loop layer info
#         for layer_order, layer_name, layer_source in layers:
#             # add data from disk
#             add_data(pro_obj=project, map_name=map_name, option='1',
#                 layers=layer_source, lyr_idx=layer_order, gdb=None)

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
            if folder == '.backups' or folder == 'Index':
                shutil.rmtree(os.path.join(root, folder))
        for file in files:
            if file.ednswith('.aprx'):
                os.remove(os.path.join(root, file))

# NEEDS TESTED IN ARCGIS PRO 3.1
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
    from pyxidust.utils import new_serial

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
