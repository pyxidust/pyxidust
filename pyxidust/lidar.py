# Pyxidust: geoprocessing/lidar/project tools for ESRI ArcGIS PRO software
# Copyright (C) 2024  Gabriel Peck  pyxidust@pm.me
"""..."""
###############################################################################

def aspect(output_folder):
    """Creates a high-resolution aspect raster from a digital elevation model.
    """

    import arcpy

    dem = (rf'{output_folder}\\DEM\\dem.tif')
    arcpy.CheckOutExtension('SPATIAL')
    aspect = arcpy.sa.SurfaceParameters(dem, 'ASPECT')
    aspect.save(rf'{output_folder}\\Aspect\\aspect.tif')
    arcpy.CheckInExtension('SPATIAL')

###############################################################################

def buildings(output_folder):
    """Creates 3D building patches from raw .las files.
    """

    import arcpy

    buildings_db = (rf'{output_folder}\\Buildings\\Buildings.gdb')
    bdactive = (rf'{buildings_db}\\BuildingsCurrent')
    bdpatch = (rf'{buildings_db}\\Buildings3D')
    bdregion = (rf'{buildings_db}\\Region')
    dem = (rf'{output_folder}\\DEM\\dem.tif')
    lasd = (rf'{output_folder}\\LASD\\Working.lasd')

    arcpy.CheckOutExtension('3D')
    arcpy.ddd.ClassifiyLasBuilding(lasd, 1, 1, '', 'MAXOF', bdregion)
    arcpy.ddd.LasBuildingMultipatch(lasd, bdactive, dem, bdpatch,
        'LAYER_FILTERED_POINTS', '0.5 Feet')
    arcpy.CheckInExtension('3D')

###############################################################################

def contours(output_folder, base_contour):
    """Creates a set of contour lines from a mean surface.
    ---------------------------------------------------------------------------
    PARAMETERS:
    ---------------------------------------------------------------------------
    base_contour: int
        base elevation contour value in feet; no contours will be created at
        elevations below the given threshold
    """

    import arcpy

    contours_db = (rf'{output_folder}\\Contours\\Contours.gdb')
    contours_five = (rf'{contours_db}\\Contours5ft')
    contours_ten = (rf'{contours_db}\\Contours10ft')
    contours_twenty = (rf'{contours_db}\\Contours20ft')
    mean = (rf'{output_folder}\\Mean\\mean.tif')

    arcpy.CheckOutExtension('SPATIAL')
    arcpy.sa.Contour(mean, contours_five, 5, base_contour)
    arcpy.sa.Contour(mean, contours_ten, 10, base_contour)
    arcpy.sa.Contour(mean, contours_twenty, 20, base_contour)
    arcpy.CheckInExtension('SPATIAL')

###############################################################################

def dem(output_folder):
    """Creates a high-resolution digital elevation model from raw .las files.
    """

    import arcpy

    dem = (rf'{output_folder}\\DEM\\dem.tif')
    lasd = (rf'{output_folder}\\LASD\\Working.lasd')
    arcpy.management.MakeLasDatasetLayer(lasd, 'TODEM', class_code = 2)
    arcpy.conversion.LasDatasetToRaster('TODEM', dem, 'ELEVATION',
        'TRIANGULATION NATURAL_NEIGHBOR WINDOW_SIZE MAXIMUM 0',
        'FLOAT', 'OBSERVATIONS', 50000)

###############################################################################

def dem_shade(output_folder):
    """Creates a high-resolution hillshade raster from a digital elevation
    model.
    """

    import arcpy

    dem = (rf'{output_folder}\\DEM\\dem.tif')
    hillshade_dem = arcpy.ia.Hillshade(dem, '', '', 3, 'DEGREE', '', '', '', 1)
    hillshade_dem.save(rf'{output_folder}\\HillshadeDEM\\hillshadedem.tif')

###############################################################################

def dem_terrain(output_folder, projection):
    """Creates a medium-resolution terrain model from raw .las files.
    ---------------------------------------------------------------------------
    PARAMETERS:
    ---------------------------------------------------------------------------
    projection: str
        path to a ArcGIS projection file used in the LAS To Multipoint tool
    """

    import arcpy
    from pyxidust.config import LEVELS
    
    las = (rf'{output_folder}\\LAS')
    terraindem_db = (rf'{output_folder}\\TerrainDEM\\TerrainDEM.gdb')
    multidem = (rf'{terraindem_db}\\TDEM\\Multi')
    terraindem = (rf'{terraindem_db}\\TDEM\\Terrain_DEM')
    terraindem_fd = (rf'{terraindem_db}\\TDEM')

    arcpy.CheckOutExtension('3D')
    arcpy.ddd.LASToMultipoint(las, multidem, 1.31, 2, 'ANY_RETURNS', '',
        projection, 'las', 1, 'NO_RECURSION')
    arcpy.ddd.CreateTerrain(terraindem_fd, 'Terrain_DEM', 1.31, 100000, '',
        'WINDOWSIZE', 'ZMEAN', 'NONE', 1)
    arcpy.ddd.AddTerrainPyramidLevel(terraindem, 'WINDOWSIZE', LEVELS)

    try:
        arcpy.ddd.AddFeatureClassToTerrain(terraindem, [multidem, 'Shape',
            'Mass_Points', 1, 0, 0, True, False, 'Multi_embed', '<None>',
            False])
    except:
        pass

    # workaround for bug in PRO; remove when resolved in future version
    try:
        arcpy.ddd.AddFeatureClassToTerrain(terraindem, [multidem, 'Shape',
            'Mass_Points', 1, 0, 0, True, False, 'Multi_embed', '<None>',
            False])
    except:
        pass

    finally:
        arcpy.ddd.BuildTerrain(terraindem, '')

    arcpy.CheckInExtension('3D')

###############################################################################

def dsm(output_folder):
    """Creates a high-resolution digital surface model from raw .las files.
    """

    import arcpy

    dsm = (rf'{output_folder}\\DSM\\dsm.tif')
    lasd = (rf'{output_folder}\\LASD\\Working.lasd')
    arcpy.management.MakeLasDatasetLayer(lasd, 'TODSM', 1)
    arcpy.conversion.LasDatasetToRaster('TODSM', dsm, 'ELEVATION',
        'BINNING MAXIMUM NATURAL_NEIGHBOR', 'FLOAT', 'OBSERVATIONS', 50000)

###############################################################################

def dsm_shade(output_folder):
    """Creates a high-resolution hillshade raster from a digital surface
    model.
    """

    import arcpy

    dsm = (rf'{output_folder}\\DSM\\dsm.tif')
    hillshade_dsm = arcpy.ia.Hillshade(dsm, '', '', 3, 'DEGREE', '', '', '', 1)
    hillshade_dsm.save(rf'{output_folder}\\HillshadeDSM\\hillshadedsm.tif')

###############################################################################

def dsm_terrain(output_folder, projection):
    """Creates a medium-resolution terrain model from raw .las files.
    ---------------------------------------------------------------------------
    PARAMETERS:
    ---------------------------------------------------------------------------
    projection: str
        path to a ArcGIS projection file used in the LAS To Multipoint tool
    """

    import arcpy
    from pyxidust.config import LEVELS

    las = (rf'{output_folder}\\LAS')
    terraindsm_db = (rf'{output_folder}\\TerrainDSM\\TerrainDSM.gdb')
    multidsm = (rf'{terraindsm_db}\\TDSM\\Multi')        
    terraindsm = (rf'{terraindsm_db}\\TDSM\\Terrain_DSM')
    terraindsm_fd = (rf'{terraindsm_db}\\TDSM')

    arcpy.CheckOutExtension('3D')
    arcpy.ddd.LASToMultipoint(las, multidsm, 1.31, '', 1, '', projection,
        'las', 1, 'NO_RECURSION')
    arcpy.ddd.CreateTerrain(terraindsm_fd, 'Terrain_DSM', 1.31, 100000, '',
        'WINDOWSIZE', 'ZMAX', 'NONE', 1)
    arcpy.ddd.AddTerrainPyramidLevel(terraindsm, 'WINDOWSIZE', LEVELS)

    try:
        arcpy.ddd.AddFeatureClassToTerrain(terraindsm, [multidsm, 'Shape',
            'Mass_Points', 1, 0, 0, True, False, 'Multi_embed', '<None>',
            False])
    except:
        pass

    # workaround for bug in PRO; remove when resolved in future version
    try:
        arcpy.ddd.AddFeatureClassToTerrain(terraindsm, [multidsm, 'Shape',
            'Mass_Points', 1, 0, 0, True, False, 'Multi_embed', '<None>',
            False])
    except:
        pass

    finally:
        arcpy.ddd.BuildTerrain(terraindsm, '')

    arcpy.CheckInExtension('3D')

###############################################################################

def intensity(output_folder):
    """Creates a high-resolution intensity raster from raw .las files.
    """

    import arcpy

    intensity = (rf'{output_folder}\\Intensity\\intensity.tif')
    lasd = (rf'{output_folder}\\LASD\\Working.lasd')
    arcpy.management.MakeLasDatasetLayer(lasd, 'TOINTENSITY')
    arcpy.conversion.LasDatasetToRaster('TOINTENSITY', intensity, 'INTENSITY',
        'BINNING AVERAGE LINEAR', 'INT', 'OBSERVATIONS', 50000)

###############################################################################

def lasd(output_folder, projection):
    """Creates a LASD dataset for further lidar processing.
    ---------------------------------------------------------------------------
    PARAMETERS:
    ---------------------------------------------------------------------------
    projection: str
        path to an ArcGIS projection file of the desired output coordinate
        reference system
    """
    
    import arcpy
    
    las = (rf'{output_folder}\\LAS')
    lasd = (rf'{output_folder}\\LASD\\Working.lasd')
    arcpy.management.CreateLasDataset(las, lasd, 'NO_RECURSION', '',
        projection, 'COMPUTE_STATS', 'ABSOLUTE_PATHS', 'NO_FILES')

###############################################################################

def mean(output_folder):
    """Creates a mean elevation surface from raw .las files.
    """

    import arcpy

    dem = (rf'{output_folder}\\DEM\\dem.tif')
    arcpy.CheckOutExtension('SPATIAL')
    mean = arcpy.sa.FocalStatistics(dem, '', 'MEAN')
    mean.save(rf'{output_folder}\\Mean\\mean.tif')
    arcpy.CheckInExtension('SPATIAL')

###############################################################################

def metadata(output_folder):
    """Overwrites previous year with current year in all .xml files.
    """

    import glob
    import os
    import time
    from arcpy import metadata as md

    terraindem_db = (rf'{output_folder}\\TerrainDEM\\TerrainDEM.gdb')
    terraindsm_db = (rf'{output_folder}\\TerrainDSM\\TerrainDSM.gdb')
    buildings_db = (rf'{output_folder}\\Buildings\\Buildings.gdb')
    contours_db = (rf'{output_folder}\\Contours\\Contours.gdb')

    hillshadedem = (rf'{output_folder}\\HillshadeDEM\\hillshadedem.tif')
    hillshadedsm = (rf'{output_folder}\\HillshadeDSM\\hillshadedsm.tif')
    intensity = (rf'{output_folder}\\Intensity\\intensity.tif')
    terraindem = (rf'{terraindem_db}\\TDEM\\Terrain_DEM')
    terraindsm = (rf'{terraindsm_db}\\TDSM\\Terrain_DSM')
    contours_twenty = (rf'{contours_db}\\Contours20ft')
    aspect = (rf'{output_folder}\\Aspect\\aspect.tif')
    range_r = (rf'{output_folder}\\Range\\range.tif')
    contours_five = (rf'{contours_db}\\Contours5ft')
    contours_ten = (rf'{contours_db}\\Contours10ft')
    slope = (rf'{output_folder}\\Slope\\slope.tif')    
    mean = (rf'{output_folder}\\Mean\\mean.tif')
    bdpatch = (rf'{buildings_db}\\Buildings3D')
    dem = (rf'{output_folder}\\DEM\\dem.tif')
    dsm = (rf'{output_folder}\\DSM\\dsm.tif')
    
    # add tree canopy height/density datasets here
    ...

    meta = (rf'{output_folder}\\Metadata')
    contourstwenty_meta = (rf'{meta}\\Contours20ft.xml')
    hillshadedem_meta = (rf'{meta}\\Hillsahdedem.xml')
    hillshadedsm_meta = (rf'{meta}\\Hillshadedsm.xml')    
    contoursfive_meta = (rf'{meta}\\Contours5ft.xml')
    contoursten_meta = (rf'{meta}\\Contours10ft.xml')    
    buildings_meta = (rf'{meta}\\Buildings3D.xml')
    terraindem_meta = (rf'{meta}\\TerrainDEM.xml')
    terraindsm_meta = (rf'{meta}\\TerrainDSM.xml')
    intensity_meta = (rf'{meta}\\Intensity.xml')
    aspect_meta = (rf'{meta}\\Aspect.xml')
    range_meta = (rf'{meta}\\Range.xml')
    slope_meta = (rf'{meta}\\Slope.xml')
    mean_meta = (rf'{meta}\\Mean.xml')    
    dem_meta = (rf'{meta}\\DEM.xml')
    dsm_meta = (rf'{meta}\\DSM.xml')

    # add tree canopy height/density xml here
    ...

    timestamp = int(time.strftime('%Y', time.localtime()))
    (new_year, previous_year) = str(timestamp - 1), str(timestamp - 2)

    os.chdir(meta)

    for file in glob.glob('*.xml'):
        with open(file, 'r') as xml:
            text = xml.read().replace(previous_year, new_year)
        with open(file, 'w+') as xml:
            xml.write(text)
    
    # add symbols from above to lookup below
    ...

    datasets = {aspect: aspect_meta, bdpatch: buildings_meta,
        contours_five: contoursfive_meta, contours_ten: contoursten_meta,
        contours_twenty: contourstwenty_meta, dem: dem_meta,
        dsm: dsm_meta, hillshadedem: hillshadedem_meta,
        hillshadedsm: hillshadedsm_meta, intensity: intensity_meta,
        mean: mean_meta, range_r: range_meta, slope: slope_meta,
        terraindem: terraindem_meta, terraindsm: terraindsm_meta}

    for key, value in datasets.items():
        dataset = md.Metadata(key)
        dataset.importMetadata(value, 'FGDC_CSDGM')
        dataset.save()

###############################################################################

def ranged(output_folder):
    """Creates a high-resolution range raster from a digital surface
    model.
    """

    import arcpy

    dsm = (rf'{output_folder}\\DSM\\dsm.tif')
    arcpy.CheckOutExtension('SPATIAL')
    ranged = arcpy.sa.FocalStatistics(dsm, '', 'RANGE')
    ranged.save(rf'{output_folder}\\Range\\range.tif')
    arcpy.CheckInExtension('SPATIAL')

###############################################################################

def slope(output_folder):
    """Creates a high-resolution slope raster from a digital elevation model.
    """

    import arcpy

    mean = (rf'{output_folder}\\Mean\\mean.tif')
    arcpy.CheckOutExtension('SPATIAL')
    slope = arcpy.sa.SurfaceParameters(mean, 'SLOPE')
    slope.save(rf'{output_folder}\\Slope\\slope.tif')
    arcpy.CheckInExtension('SPATIAL')

###############################################################################

def tree_canopy(output_folder, projection):
    """Creates high-resolution tree canopy density and hieght rasters from
    raw .las data captured with leaf-on conditions.
    ---------------------------------------------------------------------------
    PARAMETERS:
    ---------------------------------------------------------------------------
    projection: str
        path to a ArcGIS projection file used in the LAS To Multipoint tool
    """

    import arcpy
    from arcpy.conversion import LasDatasetToRaster
    from arcpy.management import CreateLasDataset, LasPointStatsAsRaster
    from arcpy.management import MakeLasDatasetLayer
    from arcpy.sa import Con, Divide, Float, IsNull, Minus, Plus

    canopy = rf'{output_folder}\\Canopy'
    # input leaf-on .las files
    leaf_on = rf'{canopy}\\LAS'

    dem = rf'{canopy}\\DEM\\dem.tif'
    dem_con = rf'{canopy}\\DEMCon\\demcon.tif'
    dem_null = rf'{canopy}\\DEMNull\\demnull.tif'
    dem_stats = rf'{canopy}\\DEMStats\\demstats.tif'
    density = rf'{canopy}\\Density\\density.tif'
    dsm = rf'{canopy}\\DSM\\dsm.tif'
    dsm_con = rf'{canopy}\\DSMCon\\dsmcon.tif'
    dsm_null = rf'{canopy}\\DSMNull\\dsmnull.tif'
    dsm_stats = rf'{canopy}\\DSMStats\\dsmstats.tif'
    float_ = rf'{canopy}\\Float\\float.tif'
    height = rf'{canopy}\\Height\\height.tif'
    lasd = rf'{canopy}\\LASD\\Working.lasd'
    plus = rf'{canopy}\\Plus\\plus.tif'

    arcpy.CheckOutExtension("SPATIAL")

    # base data
    CreateLasDataset(leaf_on, lasd, "NO_RECURSION", "", projection,
        "COMPUTE_STATS", "ABSOLUTE_PATHS", "NO_FILES")

    # dem workflow
    MakeLasDatasetLayer(lasd, "TODEM", class_code=2)
    LasDatasetToRaster("TODEM", dem, "ELEVATION",
        "TRIANGULATION NATURAL_NEIGHBOR WINDOW_SIZE MAXIMUM 0", "FLOAT",
        "OBSERVATIONS", 50000)
    LasPointStatsAsRaster("TODEM", dem_stats, "POINT_COUNT", "CELLSIZE", 5.25)
    dem_null_raster = IsNull(dem_stats)
    dem_null_raster.save(dem_null)
    dem_con_raster = Con(dem_null, 0, dem_stats)
    dem_con_raster.save(dem_con)

    # dsm workflow
    MakeLasDatasetLayer(lasd, "TODSM", 1)
    LasDatasetToRaster("TODSM", dsm, "ELEVATION",
        "BINNING MAXIMUM NATURAL_NEIGHBOR", "FLOAT", "OBSERVATIONS", 50000)
    LasPointStatsAsRaster("TODSM", dsm_stats, "POINT_COUNT", "CELLSIZE", 5.25)
    dsm_null_raster = IsNull(dsm_stats)
    dsm_null_raster.save(dsm_null)
    dsm_con_raster = Con(dsm_null, 0, dsm_stats)
    dsm_con_raster.save(dsm_con)

    # math operations
    plus_raster - Plus(dsm_con, dem_con)
    plus_raster.save(plus)
    plus_float_raster = Float(plus)
    plus_float_raster.save(float_)
    divide_raster = Divide(dsm_con, float_)
    divide_raster.save(density)

    # get canopy height
    height_raster = Minus(dsm, dem)
    height_raster.save(height)

    arcpy.CheckInExtension("SPATIAL")

###############################################################################
