# Pyxidust: geoprocessing/lidar/project tools for ESRI ArcGIS PRO software
# Copyright (C) 2024  Gabriel Peck  pyxidust@pm.me
###############################################################################

def add_data(pro_obj, map_name, option, layers=None, lyr_idx=None, gdb=None):
    """Adds data to a map in an ArcGIS PRO project.
    -----------
    PARAMETERS:
    -----------
    pro_obj:
        ArcGIS project object
    map_name: str
        map name as it appears in the catalog pane (default is 'Map')
    option/description/layers/lyr_idx/gdb:
        '1' - description:
                add one layer from disk to an indexed position in the TOC
            layers:
                path to a shapefile or feature class on disk
            layer index:
                integer layer index value above intended placement;
                use 0 for top, or 1, 2, ... to position above layer in TOC
            gdb:
                None
        '2' - description:
                add multiple layers to the top of the TOC
            layers:
                list of feature class names in the gdb
            layer index:
                None
            gdb:
                path to a geodatabase
        '3' - description:
                add all feature classes from a gdb to the top of the TOC
            layers:
                None
            layer index:
                None
            gdb:
                path to a geodatabase
        '4' - description:
                add a layer file from disk to the top of the TOC
            layers:
                path to a layer file on disk
            layer index:
                None
            gdb:
                None
        '5' - description:
                add a layer file from disk to an indexed group layer
            layers:
                path to a layer file on disk
            layer index:
                integer layer index value of existing group layer
            gdb:
                None
    ------
    USAGE:
    ------
    import arcpy
    project = arcpy.mp.ArcGISProject(r'.aprx')
    # add layer to top of table of contents
    add_data(pro_obj=project, map_name='Map', option='1',
        layers=r'Shapefile.shp', lyr_idx=0, gdb=None)
    # nest layer within table of contents
    add_data(pro_obj=project, map_name='Map', option='1',
        layers=r'Shapefile.shp', lyr_idx=3, gdb=None)
    # add multiple layers to top of table of contents
    add_data(pro_obj=project, map_name='Map', option='2',
        layers=['Points', 'Polygons'], lyr_idx=None, gdb=r'GDB.gdb')
    # add all feature classes from gdb to top of table of contents
    add_data(pro_obj=project, map_name='Map', option='3', layers=None, 
        lyr_idx=None, gdb=r'GDB.gdb')
    # add layer file from disk to top of table of contents
    add_data(pro_obj=project, map_name='Map', option='4',
        layers=r'LayerFile.lyrx', lyr_idx=0, gdb=None)
    # add layer file from disk to indexed group layer in table of contents
    add_data(pro_obj=project, map_name='Map', option='5',
        layers=r'LayerFile.lyrx', lyr_idx=0, gdb=None)
    """

    import os
    import arcpy

    _project = pro_obj
    _map = _project.listMaps(map_name)[0]

    # enable core arc methods
    def _set_environment():
        environment = gdb if gdb != None else os.getcwd()
        os.chdir(environment)
        arcpy.env.workspace = os.getcwd()
        arcpy.env.addOutputsToMap = True
    
    def _move_layer():
        new_layer = _map.listLayers()[0]
        ref_layer = _map.listLayers()[lyr_idx]
        _map.moveLayer(reference_layer=ref_layer, move_layer=new_layer,
            insert_position='BEFORE')
    
    if option == '1':
        _map.addDataFromPath(layers)
        if lyr_idx != 0:
            _move_layer()
    
    if option == '2':
        for layer in layers:
            _map.addDataFromPath(rf'{gdb}\\{layer}')
    
    if option == '3':
        _set_environment()
        for fc in arcpy.ListFeatureClasses():
            _map.addDataFromPath(rf'{gdb}\\{fc}')
    
    if option == '4':
        # layer file on disk
        layer_file = arcpy.mp.LayerFile(layers)
        # expose with listLayers to use addLayer
        for layer in layer_file.listLayers():
            _map.addLayer(add_layer_or_layerfile=layer,
                add_position='TOP')
    
    if option == '5':
        _set_environment()
        # group layer must exist
        group_layer = _map.listLayers()[lyr_idx]
        layer_file = arcpy.mp.LayerFile(layers)
        _map.addLayerToGroup(target_group_layer=group_layer,
            add_layer_or_layerfile=layer_file)
    
    _project.save()

###############################################################################

def change_source(pro_obj, dataset, layer, option, old_source, new_source):
    """Changes source of map layers in an ArcGIS PRO project.
    -----------
    PARAMETERS:
    -----------
    pro_obj:
        ArcGIS project object
    dataset: str
        layer name as it appears in the catalog pane table of contents
    layer:
        ArcGIS layer object
    option/old_source/new_source:
        '1' - old_source: str
                  path to a geodatabase for the existing data source
              new_source: str
                  path to a geodatabase for the new data source
    ------
    USAGE:
    ------
    import arcpy
    from pyxidust.gp import change_source
    project_ = arcpy.mp.ArcGISProject(r'\\.aprx')
    map_ = project_.listMaps('Map')[0]
    # [index position of layer in TOC]
    layer_ = map_.listLayers('Points')[3]
    change_source(project=project_, dataset='Points', layer=layer_,
        option='1', old_source=r'\\Old.gdb', new_source=r'\\New.gdb')
    """

    import arcpy
    
    _project = pro_obj

    if option == '1':
        source = {'dataset': dataset, 'workspace_factory': 'File Geodatabase',
                  'connection_info': {'database': old_source}}
        new = {'dataset': dataset, 'workspace_factory': 'File Geodatabase',
                  'connection_info': {'database': new_source}}
        layer.updateConnectionProperties(source, new, True, False, True)

    _project.save()

###############################################################################

def clear_gdb(gdb):
    """Removes all feature classes, rasters, and tables from a geodatabase.
    -----------
    PARAMETERS:
    -----------
    gdb: str
        path to a geodatabase
    ------
    USAGE:
    ------
    clear_gdb(gdb=r'GDB.gdb')
    """

    import arcpy
    from arcpy.management import Delete

    arcpy.env.workspace = gdb

    features = arcpy.ListFeatureClasses()
    rasters = arcpy.ListRasters()
    tables = arcpy.ListTables()
    contents = features + rasters + tables

    Delete(in_data=contents)

###############################################################################

def csv_to_features(input_file, output_features, crs, event_data):
    """Converts X/Y data in a .csv file to ArcGIS features and removes
    duplicate coordinate pairs.
    -----------
    PARAMETERS:
    -----------
    input_file: str
        path to a .csv file containing coordinate pairs; expected field format
        is 'id','x','y'
    output_features: str
        path to a shapefile, feature class, etc. that will store the output
        data
    crs: str
        path to an ArcGIS projection file of the desired output coordinate
        reference system
    event_data: path
        output path to temporary event data; this parameter is exposed to
        resolve memory conflicts between functions that make internal calls to
        MakeXYEventLayer; suggested naming convention for successive calls is
        XYEvent_CSVToFeatures where 'CSVToFeatures' is the name of the function being
        called
    ------
    USAGE:
    ------
    csv_to_features(input_file=r'\\.csv', output_features=r'\\Points.shp',
        crs=r'\\.prj', event_data='XYEvent_XYEvent_CSVToFeatures')
    """

    import arcpy
    from arcpy.management import CopyFeatures, DeleteIdentical
    from arcpy.management import MakeXYEventLayer

    MakeXYEventLayer(table=input_file, in_x_field='x', in_y_field='y',
        out_layer=event_data, spatial_reference=crs)
    plot_csv_features = CopyFeatures(in_features=event_data,
        out_feature_class=output_features)

    # remove duplicate coordinate pairs for coincident polygons
    DeleteIdentical(in_dataset=output_features, fields=['Shape', 'x', 'y'])

###############################################################################

def csv_to_gdb(csv, gdb, table):
    """Converts a .csv file to a geodatabase table.
    -----------
    PARAMETERS:
    -----------
    csv: path
        path to a .csv file
    gdb: path
        path to an ArcGIS geodatabase (workspace)
    table: str
        name of the geodatabase output table
    ------
    USAGE:
    ------
    from pyxidust.gp import csv_to_gdb
    csv_to_gdb(csv=r'\\.csv', gdb=r'\\.gdb', table='Output')
    """

    from arcpy.conversion import TableToTable

    TableToTable(csv, gdb, table)

###############################################################################

def cubic_volume(original, current, gdb, polygons):
    """Calculates volume in cubic yards using a cut/fill operation on two input
    rasters with the same cell size and coordinate system.
    -----------
    PARAMETERS:
    -----------
    original: path
        Fully-qualified/raw file path to a GRID of the original surface
    current: path
        Fully-qualified/raw file path to a GRID of the current surface
    gdb: path
        Fully-qualified/raw path to an ArcGIS geodatabase to store the results
    polygons: str
        Polygon feature class in the geodatabase to set boundaries of cut/fill
    ------
    USAGE:
    ------
    from pyxidust import *
    from pyxidust.gp import cubic_volume
    cubic_volume(original=r'\\', current=r'\\', gdb=r'\\.gdb', polygons='poly')
    """

    import arcpy
    from arcpy.analysis import Statistics
    from arcpy.conversion import FeatureClassToFeatureClass
    from arcpy.da import SearchCursor, UpdateCursor
    from arcpy.ddd import CutFill
    from arcpy.management import AddField, CalculateField, DeleteField, Merge
    from arcpy.sa import ExtractByMask

    # full path to input polygons
    boundaries = (f'{gdb}\\{polygons}')

    # enable list methods
    arcpy.env.workspace = gdb    
    arcpy.CheckOutExtension('SPATIAL')
    arcpy.CheckOutExtension('3D')

    # links polygons via filename
    suffixes = []
    # dict for suffix:sum values
    sum_values = {}

    # letter iterator to workaround
    # numerals in filenames limitation
    counter=get_suffix(string='')
    # geometry token SHAPE@ accesses polygon objects
    with SearchCursor(boundaries, ['SHAPE@']) as cursor:
        # loop polygon objects
        for row in cursor:
            # letter per iteration
            letter = next(counter)
            # store per iteration
            suffixes.append(letter)
            # unique letter per filename
            shapefile = (f'input_{letter}')
            # create a feature class for each row of the polygons
            FeatureClassToFeatureClass(in_features=row, out_path=gdb,
                out_name=shapefile)
    
    # create new iterator for loop
    raster_iterator = iter(suffixes)
    # get previous output with wild_card='input*'
    for fc in arcpy.ListFeatureClasses('input*'):
        try:
            # try/catch to handle stop iteration
            raster_suffix = next(raster_iterator)
            raster = (f'{gdb}\\cf_{raster_suffix}')
            # create subset rasters for original/current data within polygons
            before_clip = ExtractByMask(in_raster=original, in_mask_data=fc)
            after_clip = ExtractByMask(in_raster=current, in_mask_data=fc)
            # cut/fill produces AREA field in sq ft and VOLUME in cubic feet
            CutFill(in_before_surface=before_clip, in_after_surface=after_clip,
                out_raster=raster)
        except StopIteration:
            pass
    
    # create new iterator for loop
    stats_iterator = iter(suffixes)
    # get previous output with wild_card='cf*'
    for fc in arcpy.ListRasters('cf*'):
        try:
            # try/catch to handle stop iteration
            stats_suffix = next(stats_iterator)
            stats = (f'{gdb}\\stats_{stats_suffix}')
            # calculate cubic volume per raster
            CalculateField(in_table=fc, field='VOL_CUB_YDS',
                expression="!VOLUME!/27", expression_type='PYTHON3',
                field_type='DOUBLE')
            # calculate cubic volume sum per raster
            Statistics(in_table=fc, out_table=stats,
                statistics_fields=[['VOL_CUB_YDS', 'SUM']])
        except StopIteration:
            pass

    # create new iterator for loop
    search_iterator = iter(suffixes)
    # get previous output with wild_card='stats*'
    for fc in arcpy.ListTables('stats*'):
        # access field values and store in dict
        with SearchCursor(fc, ['SUM_VOL_CUB_YDS']) as cursor:
            # loop stats tables
            for row in cursor:
                # drop decimal values
                value = round(row[0])
                # get string value; drop negative
                sum_value = (str(value)).replace('-', '')
                search_suffix = next(search_iterator)
                sum_values.update({search_suffix: sum_value})
    
    # get previous output with wild_card='input*'
    for fc in arcpy.ListFeatureClasses('input*'):
        # get filename suffixes
        name_suffix = fc.split('_')
        # extract value from tuple
        loop_value = name_suffix[1]
        # add new field to calculate labels
        AddField(in_table=fc, field_name='LABEL2', field_type='TEXT',
            field_length=256)
        # add new field to store labels
        AddField(in_table=fc, field_name='LABEL', field_type='TEXT',
            field_length=256)
        # write volumes from stats to polygons
        with UpdateCursor(fc, ['LABEL']) as cursor:
            # loop stats tables
            for row in cursor:
                # link datasets through suffix
                for key, value in sum_values.items():
                    if key == loop_value:
                        # carryover value from raster
                        CalculateField(in_table=fc, field='LABEL2',
                            expression=value, expression_type='PYTHON3')
                        # calculate again to add 'CY'
                        CalculateField(in_table=fc, field='LABEL',
                            expression="!LABEL2! + ' CY'",
                            expression_type='PYTHON3')
                        # drop unwanted 'LABEL2' field from table
                        DeleteField(in_table=fc, drop_field='LABEL2')
    
    # get input polygon filenames and merge into final result
    datasets = [fc for fc in arcpy.ListFeatureClasses('input*')]
    results = (f'{gdb}\\CubicVolume')
    Merge(inputs=datasets, output=results)
    
    # check-in licenses
    arcpy.CheckInExtension('SPATIAL')
    arcpy.CheckInExtension('3D')

###############################################################################

def excel_to_gdb(workbook, gdb, table, sheet=None):
    """Converts a Microsoft Excel workbook sheet to an ArcGIS geodatabase table.
    -----------
    PARAMETERS:
    -----------
    workbook: path
        path to a Microsoft Excel workbook in .xlsx format
    gdb: path
        path to an ArcGIS geodatabase (workspace)
    table: str
        name of the geodatabase output table
    sheet: str
        workbook sheet name; used if the sheet to be converted to table is not
        the first sheet in the workbook
    ------
    USAGE:
    ------
    from pyxidust.gp import excel_to_gdb
    excel_to_gdb(workbook=r'\\.xlsx', gdb=r'\\.gdb', table='Output',
        sheet='Sheet 1')
    """

    import os
    from arcpy.conversion import TableToTable
    from pandas import DataFrame, read_excel

    csv_excel = (rf'{os.getcwd()}\\excel_to_gdb.csv')
    
    if sheet != None:
        df = DataFrame(read_excel(workbook, sheet_name=sheet,
            engine='openpyxl'))
        df.to_csv(csv_excel)
        TableToTable(csv_excel, gdb, table)

    else:
        df = DataFrame(read_excel(workbook, engine='openpyxl'))
        df.to_csv(csv_excel)
        TableToTable(csv_excel, gdb, table)

    os.remove(csv_excel)

###############################################################################

def explode_geometry(dataset, gdb):
    """Exports each row of a multipart feature class.
    -----------
    PARAMETERS:
    -----------
    dataset: str
        Name of the feature class to explode as it appears in the catalog pane
        in ArcGIS PRO; feature class must be in the root of the .gdb
    gdb: path
        Fully-qualified/raw folder path to a geodatabase
    ------
    USAGE:
    ------
    from pyxidust.gp import explode_geometry
    explode_geometry(dataset='Polygons', gdb=r'\\.gdb')
    """

    import arcpy
    from arcpy import AddFieldDelimiters as Delimiter
    from arcpy.analysis import Select
    from arcpy.da import SearchCursor

    # construct feature class path
    fc = (rf'{gdb}\\{dataset}')
    # get feature class properties
    fields = arcpy.Describe(fc).OIDFieldName
    # infinite generator
    counter = get_suffix(string='')
    # loop rows in feature class
    with SearchCursor(fc, fields) as cursor:
        for row in cursor:
            # get unique letters for each row
            letter = next(counter)
            # construct filename/path for exports
            explode = (rf'{gdb}\\Explode_{letter}')
            # SQL 'where' clause
            clause = '{0} = {1}'.format(Delimiter(fc, fields), row[0])
            # get/export rows
            Select(fc, explode, clause)

###############################################################################

def features_to_csv(input_features, output_file, option, gdb=None):
    """Converts point/polygon features to a .csv file.
    -----------
    PARAMETERS:
    -----------
    input_features: str
        path to ArcGIS point/polygon features
    output_file: str
        path to an output .csv file to store coordinate data
    option: str
        'point' - input features are point geometry
        'polygon' - input features are polygon geometry
    gdb: path
        full path to a geodatabase if option == 'point'
    ------
    USAGE:
    ------
    features_to_csv(input_features=r'Shapefile.shp',
        output_file=r'CSV.csv', option='polygon')
    """

    import json
    import os
    import arcpy
    import pandas

    from arcpy.conversion import FeaturesToJSON
    from arcpy.stats import ExportXYv
    from pandas import json_normalize, read_csv

    json_temp = (rf'{os.getcwd()}\\features_to_csv.json')
    csv_temp = (rf'{os.getcwd()}\\features_to_csv.csv')

    arcpy.env.overwriteOutput = True

    if option == 'point':
        os.chdir(gdb)
        arcpy.env.workspace = os.getcwd()
        ExportXYv(Input_Feature_Class=input_features,
            Value_Field=['id', 'x', 'y'], Delimiter='COMMA',
            Output_ASCII_File=csv_temp,
            Add_Field_Names_to_Output='ADD_FIELD_NAMES')
        df_csv = read_csv(filepath_or_buffer=csv_temp, sep=',')
        df_clean = df_csv.loc[:, ['id', 'x', 'y']]
        df_clean.to_csv(path_or_buf=output_file, index=False)
        os.remove(csv_temp)

    if option == 'polygon':
        FeaturesToJSON(in_features=input_features,
            out_json_file=json_temp, format_json='FORMATTED')
        with open(json_temp, 'r') as file:
            json_file = json.load(file)
        os.remove(json_temp)
        df_flat = json_normalize(data=json_file, record_path='features',
            meta=['geometry', 'rings'], errors='ignore')
        GEO = 'geometry.rings'
        df_clean = df_flat[GEO]
        df_exploded = df_clean.explode(GEO).explode(GEO)
        json_csv = df_exploded.to_csv(path_or_buf=json_temp, index=False)
        with open(json_temp, 'r') as file:
            text = file.read().replace('[', '').replace(']', '')
            text = text.replace('"', '').replace(',geometry.rings', '')
            text = text.replace(' ', '')
        with open(output_file, 'w+') as file:
            file.write('id,x,y')
            file.writelines(text)
        os.remove(json_temp)

###############################################################################

def get_suffix(string):
    """Infinite generator that yields unique letter combinations for file
    operations that do not support numbers.
    -----------
    PARAMETERS:
    -----------
    string: str
        Base string that will have a unique letter combination appended;
        yields a unique filename combination with each iteration; include
        an underbar for readability if desired
        (A, B, ..., _AA, _BB, ...)
    ------
    USAGE:
    ------
    from pyxidust.gp import get_suffix
    generator = get_suffix(string='filename_')
    next(generator) -> 'filename_A'
    next(generator) -> 'filename_B'
    """

    from string import ascii_uppercase as UPPER

    loops = 1
    while loops > 0:
        for letter in UPPER:
            text = (f'{string}{letter * loops}')
            yield text
            if letter.startswith('Z'):
                loops += 1

###############################################################################

def image_to_features(image, classes, identifier, query, crs, directory,
    area=None):
    """Clips a georeferenced raster to a new extent based on parameters and
    outputs the new clipped raster and polygon features.
    -----------
    PARAMETERS:
    -----------
    image: str
        path to a georeferenced image that has been registered with the 'update
        georeferencing' option applied; do not 'rectify' the image afterwards
        as it blows out the RGB color values from the original image
    classes: str
        number of raster cell groups for the Iso Cluster Unsupervised
        Classification tool; function can be run multiple times to produce the
        desired results by tweaking this value combined with the query parameter
    identifier: str
        value will be appended to the end of all file names to tie results
        together from multiple function calls
    query: str
        valid SQL 'where clause' that acts as a threshold in the Extract By
        Attributes tool to limit the amount of features that will be processed
        in the second part of the function; can also be used to clean data of
        undesired values
    crs: str
        path to an ArcGIS projection file of the desired output coordinate
        reference system
    directory: str
        path to an output folder to store the function results
    area: str
        valid SQL 'where clause' that acts as a threshold in the Select tool
        to remove small polygons produced by rasterization/analysis which are
        not part of the data
    --------
    RETURNS:
    --------
    image
        clipped image within the mask
    ------
    USAGE:
    ------
    from pyxidust.gp import image_to_features
    clip = image_to_features(image='\\Image.tif', classes='4', identifier='A',
        query='VALUE = 1 OR VALUE = 2', crs='\\.prj', directory='\\Folder',
        area='AREA >= 100')
    # for sequential function calls feed the returned 'clip' as the image value
    clip_2 = image_to_features(image=clip, classes='6', identifier='B',
        query='VALUE = 3', crs='\\.prj', directory='\\Folder',
        area='AREA >= 100')
    """

    import arcpy
    from arcpy.analysis import Select
    from arcpy.conversion import RasterToPolygon
    from arcpy.management import CalculateGeometryAttributes
    from arcpy.sa import ExtractByAttributes, ExtractByMask
    from arcpy.sa import IsoClusterUnsupervisedClassification

    arcpy.env.overwriteOutput = True
    arcpy.env.outputCoordinateSystem = crs
    arcpy.CheckOutExtension('SPATIAL')

    classes = int(classes)

    # create raster for all polygons in image per classes
    boundary = IsoClusterUnsupervisedClassification(image, classes)
    boundary.save(rf'{directory}\\boundary_{identifier}')

    # retain only desired values per SQL query
    extract = ExtractByAttributes(boundary, query)
    extract.save(rf'{directory}\\extract_{identifier}')

    # convert extracted raster to polygons for use as mask
    mask = (rf'{directory}\\mask_{identifier}')
    RasterToPolygon(extract, mask, 'SIMPLIFY', '', 'SINGLE_OUTER_PART')

    # use area query to remove small polygons
    if area != None:
        CalculateGeometryAttributes(in_features=mask,
            geometry_property='AREA AREA', area_unit='SQUARE_FEET_US')
        clean = (rf'{directory}\\clean_{identifier}')
        Select(mask, clean, area)

    # clip image using outer boundary as mask
    extract = ExtractByMask(image, clean)
    clip = (rf'{directory}\\clip_{identifier.lower()}')
    extract.save(clip)

    arcpy.CheckInExtension('SPATIAL')

    return clip

###############################################################################

def move_elements(pro_obj, lay_obj, ele_type, wildcard):
    """Moves a selected set of elements off a layout in an ArcGIS PRO project.
    -----------
    PARAMETERS:
    -----------
    pro_obj:
        ArcGIS project object
    lay_obj:
        ArcGIS layout object
    ele_type: str
        type of layout element to move; options are:
        GRAPHIC_ELEMENT, LEGEND_ELEMENT, MAPFRAME_ELEMENT,
        MAPSURROUND_ELEMENT, PICTURE_ELEMENT, TEXT_ELEMENT
    wildcard: str
        text value used to restrict the search in the provided ele_type;
        use '*...' or '...*' to search for elements with a certain name
    ------
    USAGE:
    ------
    project = arcpy.mp.ArcGISProject(r'.aprx')
    layout = project.listLayouts('Map')[0]
    move_elements(pro_obj=project, lay_obj=layout,
        ele_type=GRAPHIC_ELEMENT, wildcard='*Info')
    """

    import arcpy

    project = pro_obj
    layout = lay_obj

    for element in layout.listElements(ele_type, wildcard):
        element.elementPositionX = -abs(100000.00)
        element.elementPositionY = -abs(100000.00)

    project.save()

###############################################################################

def place_anno(pro_obj, map_name, lay_name, fra_name, lyr_idx, adjust, gdb,
    suffix, lyr_name=None):
    """Sets reference scale from a layer in an ArcGIS PRO project and creates
    annotation feature classes for all layers with visible labels.
    -----------
    PARAMETERS:
    -----------
    pro_obj:
        ArcGIS project object
    map_name: str
        Map name as it appears in the catalog pane (default is 'Map')
    lay_name: str
        Layout name as it appears in the catalog pane (default is 'Layout')
    fra_name: str
        Frame name as it appears in the layout TOC (default is 'Map Frame')
    lyr_idx: int
        Index position of a layer in the map TOC layer stack (0, 1, ...)
    adjust: float
        value used to fine-tune layout scale; value will be multiplied by the
        map frame camera scale; use a value less than 1 to decrease scale and a
        value more than 1 to increase scale (0.7, 1.2)
    gdb: path
        output geodatabase for the annotation features
    suffix: str
        letter added to all new annotation feature class names
    lyr_name: str
        layer name as it appears in the table of contents (TOC); if a value
        is provided for this argument only the named layer will have
        annotations created
    --------
    RETURNS:
    --------
    _extent:
        ArcGIS extent object
    scale:
        ArcGIS environment/map/camera scale used as conversion scale for anno
    ------
    USAGE:
    ------
    import arcpy
    project_ = arcpy.mp.ArcGISProject(r'\\.aprx')
    # returns extent, scale; unpack or call without variables
    extent,scale = place_anno(pro_obj=project_, map_name='Map',
        lay_name='Layout', fra_name='Map Frame', lyr_idx=0, adjust=1.1,
        gdb=r'\\.gdb', suffix='A')
    """

    import arcpy
    from arcpy.cartography import ConvertLabelsToAnnotation
    
    _project = pro_obj
    _map = _project.listMaps(map_name)[0]
    _layout = _project.listLayouts(lay_name)[0]
    _frame = _layout.listElements('MAPFRAME_ELEMENT', fra_name)[0]
    _layer = _map.listLayers()[lyr_idx]
    
    _extent = _frame.getLayerExtent(_layer, True)
    _frame.camera.setExtent(_extent)
    _frame.camera.scale *= adjust
    arcpy.env.referenceScale = _frame.camera.scale
    _map.referenceScale = arcpy.env.referenceScale
    scale = _map.referenceScale

    _project.save()
    
    if lyr_name == None:
        ConvertLabelsToAnnotation(input_map=_map, conversion_scale=scale,
            output_geodatabase=gdb, anno_suffix=suffix, extent=_extent,
            generate_unplaced='GENERATE_UNPLACED')
    
    if lyr_name != None:
        ConvertLabelsToAnnotation(input_map=_map, conversion_scale=scale,
            output_geodatabase=gdb, anno_suffix=suffix, extent=_extent,
            generate_unplaced='GENERATE_UNPLACED', which_layers='SINGLE_LAYER',
            single_layer=lyr_name)
    
    return _extent, scale

###############################################################################

def plot_csv(pro_obj, map_name, csv, crs, output, event_data, x_name, y_name,
    z_name=None):
    """Converts X/Y/Z coordinates in a .csv file to a shapefile and adds it to
    a map in an ArcGIS PRO project.
    -----------
    PARAMETERS:
    -----------
    pro_obj:
        ArcGIS project object
    map_name: str
        Map name as it appears in the catalog pane (default is 'Map')
    csv: path
        Fully-qualified/raw file path to a .csv file containing X/Y data
    crs: path
        Fully-qualified/raw file path to an ArcGIS projection file of the
        desired output coordinate reference system
    output: path
        Fully-qualified/raw file path to the desired output shapefile
    event_data: path
        output path to temporary event data; this parameter is exposed to
        resolve memory conflicts between functions that make internal calls to
        MakeXYEventLayer; suggested naming convention for successive calls is
        XYEvent_CSVPlot where 'CSVPlot' is the name of the function being
        called
    x_name: str
        Name of field containing X coordinates to import
    y_name: str
        Name of field containing Y coordinates to import
    z_name: str
        Name of field containing Z coordinates to import
    ------
    USAGE:
    ------
    import arcpy
    from pyxidust.gp import plot_csv
    project_ = arcpy.mp.ArcGISProject(r'\\.aprx')
    # z-values are optional
    plot_csv(pro_obj=project_, map_name='Map', csv=r'\\.csv', crs=r'\\.prj',
        output=r'\\.shp', event_data='XYEvent_CSV_Plot', x_name='X', y_name='Y',
        z_name=None='Z')
    """

    import os
    import random
    import arcpy
    from string import ascii_uppercase as LETTERS
    
    letter = random.choice(LETTERS)
    plot = (f'Plot_{letter}')
    
    _project = pro_obj
    _map = _project.listMaps(map_name)[0]
    
    if z_name != None:
        arcpy.management.MakeXYEventLayer(table=csv, in_x_field=x_name,
            in_y_field=y_name, out_layer=event_data,
            spatial_reference=crs, in_z_field=z_name)
    if z_name == None:
        arcpy.management.MakeXYEventLayer(table=csv, in_x_field=x_name,
            in_y_field=y_name, out_layer=event_data,
            spatial_reference=crs)

    # arcobjects results object
    csv_plot = arcpy.management.CopyFeatures(in_features=event_data,
        out_feature_class=output)
    features_csv = arcpy.management.MakeFeatureLayer(in_features=csv_plot,
        out_layer=plot)
    
    # arcpy.mp layer object
    _layer = features_csv.getOutput(0)
    _map.addLayer(_layer)

    _project.save()

###############################################################################

def plot_excel(workbook, pro_obj, map_name, crs, shapefile, event_data, x_name,
    y_name, z_name=None, sheet=None):
    """Converts X/Y/Z coordinates in a spreadsheet workbook to a shapefile and
    adds it to a map in an ArcGIS PRO project.
    -----------
    PARAMETERS:
    -----------
    workbook: path
        path to a spreadsheet workbook in xls/xlsx/xlsm/xlsb/odf/ods/odt format
    pro_obj:
        ArcGIS project object
    map_name: str
        Map name as it appears in the catalog pane (default is 'Map')
    crs: path
        Fully-qualified/raw file path to an ArcGIS projection file of the
        desired output coordinate reference system
    shapefile: path
        Fully-qualified/raw file path to the desired output shapefile
    event_data: path
        output path to temporary event data; this parameter is exposed to
        resolve memory conflicts between functions that make internal calls to
        MakeXYEventLayer; suggested naming convention for successive calls is
        XYEvent_PlotExcel where 'PlotExcel' is the name of the function being
        called
    x_name: str
        Name of field containing X coordinates to import
    y_name: str
        Name of field containing Y coordinates to import
    z_name: str
        Name of field containing Z coordinates to import
    sheet: str
        individual spreadsheet name; used if the sheet to be converted is not
        the first sheet in the workbook
    ------
    USAGE:
    ------
    import arcpy
    from pyxidust.gp import plot_excel
    project_ = arcpy.mp.ArcGISProject(r'\\.aprx')
    # z-values and sheet name are optional
    plot_excel(workbook=r'\\.xlsx', pro_obj=project_, map_name='Map',
        crs=r'\\.prj', shapefile=r'\\.shp', event_data='XYEvent_PlotExcel', 
        x_name='X', y_name='Y', z_name='Z',
        sheet='Sheet1')
    """
    
    import os
    from pandas import DataFrame, read_excel

    plot_excel = (rf'{os.getcwd()}\\excel_plot.csv')
    
    if sheet == None and z_name == None:
        df = DataFrame(read_excel(workbook, engine='openpyxl'))
        df.to_csv(plot_excel)
        plot_csv(pro_obj=pro_obj, map_name=map_name, csv=plot_excel, crs=crs,
            output=shapefile, event_data=event_data, x_name=x_name,
            y_name=y_name)

    elif sheet != None and z_name == None:
        df = DataFrame(read_excel(workbook, sheet_name=sheet,
            engine='openpyxl'))
        df.to_csv(plot_excel)
        plot_csv(pro_obj=pro_obj, map_name=map_name, csv=plot_excel, crs=crs,
            output=shapefile, event_data=event_data, x_name=x_name,
            y_name=y_name)

    elif sheet == None and z_name != None:
        df = DataFrame(read_excel(workbook, engine='openpyxl'))
        df.to_csv(plot_excel)
        plot_csv(pro_obj=pro_obj, map_name=map_name, csv=plot_excel, crs=crs,
            output=shapefile, event_data=event_data, x_name=x_name,
            y_name=y_name, z_name=z_name)

    elif sheet != None and z_name != None:
        df = DataFrame(read_excel(workbook, sheet_name=sheet,
            engine='openpyxl'))
        df.to_csv(plot_excel)
        plot_csv(pro_obj=pro_obj, map_name=map_name, csv=plot_excel, crs=crs,
            output=shapefile, event_data=event_data, x_name=x_name,
            y_name=y_name, z_name=z_name)

    os.remove(plot_excel)

###############################################################################

def print_info(pro_obj):
    """Prints map/layout/layer names and data sources in an ArcGIS PRO project.
    Useful for troublesome projects that will not open due to memory issues.
    -----------
    PARAMETERS:
    -----------
    pro_obj:
        ArcGIS project object
    ------
    USAGE:
    ------
    import arcpy
    project_ = arcpy.mp.ArcGISProject(r'\\.aprx')
    print_info(pro_obj=project_)
    """
    
    import arcpy
    
    _project = pro_obj

    print(f'Layout names: {[i.name for i in _project.listLayouts()]}\n')
    
    for _id, _map in enumerate(_project.listMaps(), start=1):
        for _layer in _map.listLayers():
            if _layer.isFeatureLayer:
                print(f'Map #{_id} ({_map.name})')
                print(f'{_layer.name} layer source: {_layer.dataSource}')
                
###############################################################################

def print_layers(pro_obj, map_name):
    """Prints the properties of all layers in a map in an ArcGIS PRO project.
    -----------
    PARAMETERS:
    -----------
    pro_obj:
        ArcGIS project object
    map_name: str
        Map name as it appears in the catalog pane (default is 'Map')
    ------
    USAGE:
    ------
    import arcpy
    project_ = arcpy.mp.ArcGISProject(r'\\.aprx')
    print_layers(pro_obj=project_, map_name='Map')
    """
    
    import arcpy
    
    _project = pro_obj
    _map = _project.listMaps(map_name)[0]
    _layers = _map.listLayers()
    
    for _layer in _layers:

        if _layer.isGroupLayer == False:
            print(f'\n{"_"*79}\n\n')
            
            try:
                if _layer.supports('NAME'):
                    print(f'Layer name: {_layer.name}')
            except Exception as e:
                print(e)
                
            try:
                if _layer.supports('LONGNAME'):
                    print(f'Group name: {_layer.longName}')
            except Exception as e:
                print(e)
                
            try:
                if _layer.is3DLayer:
                    print(f'3D layer = True')
            except Exception as e:
                print(e)
                
            try:
                if _layer.isWebLayer:
                    print(f'Web layer = True')
            except Exception as e:
                print(e)

            try:
                if _layer.isSceneLayer:
                    print(f'Scene layer = True')
            except Exception as e:
                print(e)

            try:
                if _layer.isTimeEnabled:
                    print(f'Time enabled = True')
            except Exception as e:
                print(e)

            try:
                if _layer.isRasterLayer:
                    print(f'Raster layer = True')
            except Exception as e:
                print(e)

            try:
                if _layer.isBasemapLayer:
                    print(f'Basemap layer = True')
            except Exception as e:
                print(e)

            try:
                if _layer.isFeatureLayer:
                    print(f'Feature layer = True')
            except Exception as e:
                print(e)

            try:
                if _layer.isBroken:
                    print(f'Broken data source = True')
            except Exception as e:
                print(e)

            try:
                if _layer.supports('VISIBLE'):
                    print(f'Visible = {_layer.visible}')
            except Exception as e:
                print(e)

            try:
                if _layer.isNetworkAnalystLayer:
                    print(f'Network analyst layer = True')
            except Exception as e:
                print(e)

            try:
                if _layer.isNetworkDatasetLayer:
                    print(f'Network dataset layer = True')
            except Exception as e:
                print(e)

            try:
                if _layer.supports('SHOWLABELS'):
                    print(f'Labels on = {_layer.showLabels}')
            except Exception as e:
                print(e)

            print(f'\n{"_"*79}\n\n')
            
            try:
                if _layer.supports('TIME'):
                    print(f'Time: {_layer.time}')
            except Exception as e:
                print(e)
            
            try:
                if _layer.supports('CONTRAST'):
                    print(f'Contrast: {_layer.contrast}')
            except Exception as e:
                print(e)
            
            try:
                if _layer.supports('BRIGHTNESS'):
                    print(f'Brightness: {_layer.brightness}')
            except Exception as e:
                print(e)
            
            try:
                if _layer.supports('TRANSPARENCY'):
                    print(f'Transparency: {_layer.transparency}')
            except Exception as e:
                print(e)

            try:
                if _layer.supports('MINTHRESHOLD'):
                    print(f'Min display scale: {_layer.minThreshold}')
            except Exception as e:
                print(e)

            try:
                if _layer.supports('MAXTHRESHOLD'):
                    print(f'Max display scale: {_layer.maxThreshold}')
            except Exception as e:
                print(e)

            try:
                if _layer.supports('DEFINITIONQUERY'):
                    print(f'Query: {_layer.definitionQuery}')
            except Exception as e:
                print(e)

            print(f'\n{"_"*79}\n\n')

            try:
                if _layer.supports('URI'):
                    print(f'Universal resource indicator: {_layer.URI}')
            except Exception as e:
                print(e)
                
            try:
                if _layer.supports('DATASOURCE'):
                    print(f'Source: {_layer.dataSource}')
            except Exception as e:
                print(e)

            try:
                if _layer.supports('CONNECTIONPROPERTIES'):
                    print(f'Connection: {_layer.connectionProperties}')
            except Exception as e:
                print(e)

            try:
                if _layer.supports('METADATA'):
                    print(f'\n{"_"*79}\n\n')
                    meta = _layer.metadata
                    print(f'Metadata title: {meta.title}')
                    print(f'Metadata description: {meta.description}')
            except Exception as e:
                print(e)

###############################################################################

def remove_layers(pro_obj, map_obj, layers):
    """Removes layers from a map in an ArcGIS PRO project.
    -----------
    PARAMETERS:
    -----------
    pro_obj:
        ArcGIS project object
    map_obj:
        ArcGIS map object
    layers: set
        Layer names in the table of contents to remove from the map
    ------
    USAGE:
    ------
    import arcpy
    project = arcpy.mp.ArcGISProject(path)
    map_ = project.listMaps('Map')[0]
    remove_layers(pro_obj=project, map_obj=map_, layers={'Hydro', 'Points'})
    """

    import arcpy

    _project = pro_obj
    _map = map_obj

    for layer in _map.listLayers():
        if layer.isFeatureLayer:
            if layer.name in layers:
                _layer = _map.listLayers(layer.name)[0]
                _map.removeLayer(_layer)

    _project.save()

###############################################################################

def visible_layers(pro_obj, map_name, lyr_idx, option=None):
    """Turns on/off layers in a map in an ArcGIS PRO project if the layer index
    position is found in the input list.
    -----------
    PARAMETERS:
    -----------
    pro_obj:
        ArcGIS project object
    map_name: str
        Map name as it appears in the catalog pane (default is 'Map')
    lyr_idx: list
        List of integers representing index positions of layers in the map
        table of contents layer stack to turn off
    option: str
        if option == 'on' layers that are off in the map will be visible;
        if option == 'off' layers that are on in the map will not be visible
    ------
    USAGE:
    ------
    import arcpy
    project_ = arcpy.mp.ArcGISProject(r'\\.aprx')
    visible_layers(pro_obj=project_, map_name='Map', lyr_idx=[0,1,2])
    """

    import arcpy

    _project = pro_obj
    _map = _project.listMaps(map_name)[0]

    for element in lyr_idx:
        index = int(element)
        _layer = _map.listLayers()[index]
        if _layer.isFeatureLayer:
            if option == 'on':
                _layer.visible = True
            else:
                _layer.visible = False

    _project.save()

###############################################################################

def zoom_to(pro_obj, map_name, lay_name, fra_name, lyr_idx, adjust):
    """Sets reference scale from a layer in an ArcGIS PRO project and zooms the
    layout to the layer extent.
    -----------
    PARAMETERS:
    -----------
    pro_obj:
        ArcGIS project object
    map_name: str
        Map name as it appears in the catalog pane (default is 'Map')
    lay_name: str
        Layout name as it appears in the catalog pane (default is 'Layout')
    fra_name: str
        Frame name as it appears in the layout TOC (default is 'Map Frame')
    lyr_idx: int
        Index position of a layer in the map TOC layer stack (0, 1, ...)
    adjust: float
        value used to fine-tune layout scale; value will be multiplied by the
        map frame camera scale; use a value less than 1 to decrease scale and a
        value more than 1 to increase scale (0.7, 1.2)
    ------
    USAGE:
    ------
    import arcpy
    project_ = arcpy.mp.ArcGISProject(r'\\.aprx')
    zoom_to(pro_obj=project_, map_name='Map', lay_name='Layout',
        fra_name='Map Frame', lyr_idx=0, adjust=1.1)
    """
    
    import arcpy
    
    _project = pro_obj
    _map = _project.listMaps(map_name)[0]
    _layout = _project.listLayouts(lay_name)[0]
    _frame = _layout.listElements('MAPFRAME_ELEMENT', fra_name)[0]
    _layer = _map.listLayers()[lyr_idx]
    
    _extent = _frame.getLayerExtent(_layer, True)
    _frame.camera.setExtent(_extent)
    _frame.camera.scale *= adjust
    arcpy.env.referenceScale = _frame.camera.scale
    _map.referenceScale = arcpy.env.referenceScale
    scale = _map.referenceScale

    _project.save()
    
    return _extent, scale
