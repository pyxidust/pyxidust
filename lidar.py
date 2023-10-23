# pyxidust library lidar module
# Gabriel Peck 2023 (MIT license)

###############################################################################

# -------------
# MODULE INDEX:
# -------------

# pyxidust.lidar.aspect()
# pyxidust.lidar.buildings()
# pyxidust.lidar.contours()
# pyxidust.lidar.dem()
# pyxidust.lidar.dem_shade()
# pyxidust.lidar.dem_terrain()
# pyxidust.lidar.dsm()
# pyxidust.lidar.dsm_shade()
# pyxidust.lidar.dsm_terrain()
# pyxidust.lidar.intensity()
# pyxidust.lidar.lasd()
# pyxidust.lidar.mean()
# pyxidust.lidar.metadata()
# pyxidust.lidar.ranged()
# pyxidust.lidar.slope()

###############################################################################

def aspect(output_folder):
    """Creates a high-resolution aspect raster from a digital elevation model.
    """

    import arcpy

    dem = (f'{output_folder}\\DEM\\dem.tif')

    arcpy.CheckOutExtension('SPATIAL')
    aspect = arcpy.sa.SurfaceParameters(dem, 'ASPECT')
    aspect.save(f'{output_folder}\\Aspect\\aspect.tif')
    arcpy.CheckInExtension('SPATIAL')

def buildings(output_folder):
    """Creates 3D building patches from raw .las files.
    """

    import arcpy

    buildings_db = (f'{output_folder}\\Buildings\\Buildings.gdb')
    bdactive = (f'{buildings_db}\\BuildingsCurrent')
    bdpatch = (f'{buildings_db}\\Buildings3D')
    bdregion = (f'{buildings_db}\\Region')
    dem = (f'{output_folder}\\DEM\\dem.tif')
    lasd = (f'{output_folder}\\LASD\\Working.lasd')

    arcpy.CheckOutExtension('3D')
    arcpy.ddd.ClassifiyLasBuilding(lasd, 1, 1, '', 'MAXOF', bdregion)
    arcpy.ddd.LasBuildingMultipatch(lasd, bdactive, dem, bdpatch, '', '')
    arcpy.CheckInExtension('3D')

def contours(output_folder):
    """Creates a set of contour lines from a mean surface.
    """

    import arcpy

    contours_db = (f'{output_folder}\\Contours\\Contours.gdb')
    contours_five = (f'{contours_db}\\Contours5ft')
    contours_ten = (f'{contours_db}\\Contours10ft')
    contours_twenty = (f'{contours_db}\\Contours20ft')
    mean = (f'{output_folder}\\Mean\\mean.tif')

    arcpy.CheckOutExtension('SPATIAL')
    arcpy.sa.Contour(mean, contours_five, 5, 530)
    arcpy.sa.Contour(mean, contours_ten, 10, 530)
    arcpy.sa.Contour(mean, contours_twenty, 20, 530)
    arcpy.CheckInExtension('SPATIAL')

def dem(output_folder):
    """Creates a high-resolution digital elevation model from raw .las files.
    """

    import arcpy

    dem = (f'{output_folder}\\DEM\\dem.tif')
    lasd = (f'{output_folder}\\LASD\\Working.lasd')

    arcpy.management.MakeLasDatasetLayer(lasd, 'TODEM', class_code = 2)
    arcpy.conversion.LasDatasetToRaster('TODEM', dem, 'ELEVATION',
        'TRIANGULATION NATURAL_NEIGHBOR WINDOW_SIZE MAXIMUM 0',
        'FLOAT', 'OBSERVATIONS', 50000)

def dem_shade(output_folder):
    """Creates a high-resolution hillshade raster from a digital elevation
    model.
    """

    import arcpy

    dem = (f'{output_folder}\\DEM\\dem.tif')

    hillshade_dem = arcpy.ia.Hillshade(dem, '', '', 3, 'DEGREE', '', '', '', 1)
    hillshade_dem.save(f'{output_folder}\\HillshadeDEM\\hillshadedem.tif')

def dem_terrain(output_folder):
    """Creates a medium-resolution terrain model from raw .las files.
    """

    import arcpy

    las = (f'{output_folder}\\LAS')
    terraindem_db = (f'{output_folder}\\TerrainDEM\\TerrainDEM.gdb')
    multidem = (f'{terraindem_db}\\TDEM\\Multi')
    terraindem = (f'{terraindem_db}\\TDEM\\Terrain_DEM')
    terraindem_fd = (f'{terraindem_db}\\TDEM')

    arcpy.CheckOutExtension('3D')
    arcpy.ddd.LASToMultipoint(las, multidem, 1.31, 2, 'ANY_RETURNS', '',
        HARN83, 'las', 1, 'NO_RECURSION')
    arcpy.ddd.CreateTerrain(terraindem, 'Terrain_DEM', 1.31, 100000, '',
        'WINDOWSIZE', 'ZMEAN', 'NONE', 1)
    arcpy.ddd.AddTerrainPyramidLevel(terraindem, 'WINDOWSIZE', LEVELS)

    try:
        arcpy.ddd.AddFeatureClassToTerrain(terraindem, [multidem, 'Shape',
            'Mass_Points', 1, 0, 0, True, False, 'Multi_embed', '<None>',
            False])
    except:
        pass
    try:
        arcpy.ddd.AddFeatureClassToTerrain(terraindem, [multidem, 'Shape',
            'Mass_Points', 1, 0, 0, True, False, 'Multi_embed', '<None>',
            False])
    except:
        pass
    finally:
        arcpy.ddd.BuildTerrain(terraindem, '')

    arcpy.CheckInExtension('3D')

def dsm(output_folder):
    """Creates a high-resolution digital surface model from raw .las files.
    """

    import arcpy

    dsm = (f'{output_folder}\\DSM\\dsm.tif')
    lasd = (f'{output_folder}\\LASD\\Working.lasd')

    arcpy.management.MakeLasDatasetLayer(lasd, 'TODSM', 1)
    arcpy.conversion.LasDatasetToRaster('TODSM', dsm, 'ELEVATION',
        'BINNING MAXIMUM NATURAL_NEIGHBOR', 'FLOAT', 'OBSERVATIONS', 50000)

def dsm_shade(output_folder):
    """Creates a high-resolution hillshade raster from a digital surface
    model.
    """

    import arcpy

    dsm = (f'{output_folder}\\DSM\\dsm.tif')

    hillshade_dsm = arcpy.ia.Hillshade(dsm, '', '', 3, 'DEGREE', '', '', '', 1)
    hillshade_dsm.save(f'{output_folder}\\HillshadeDSM\\hillshadedsm.tif')

def dsm_terrain(output_folder):
    """Creates a medium-resolution terrain model from raw .las files.
    """

    import arcpy

    las = (f'{output_folder}\\LAS')
    terraindsm_db = (f'{output_folder}\\TerrainDSM\\TerrainDSM.gdb')
    multidsm = (f'{terraindsm_db}\\TDSM\\Multi')        
    terraindsm = (f'{terraindsm_db}\\TDSM\\Terrain_DSM')
    terraindsm_fd = (f'{terraindsm_db}\\TDSM')

    arcpy.CheckOutExtension('3D')
    arcpy.ddd.LASToMultipoint(las, multidsm, 1.31, '', 1, '', HARN83,
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
    try:
        arcpy.ddd.AddFeatureClassToTerrain(terraindsm, [multidsm, 'Shape',
            'Mass_Points', 1, 0, 0, True, False, 'Multi_embed', '<None>',
            False])
    except:
        pass
    finally:
        arcpy.ddd.BuildTerrain(terraindsm, '')

    arcpy.CheckInExtension('3D')

def intensity(output_folder):
    """Creates a high-resolution intensity raster from raw .las files.
    """

    import arcpy

    intensity = (f'{output_folder}\\Intensity\\intensity.tif')
    lasd = (f'{output_folder}\\LASD\\Working.lasd')

    arcpy.management.MakeLasDatasetLayer(lasd, 'TOINTENSITY')
    arcpy.conversion.LasDatasetToRaster('TOINTENSITY', intensity,
        'INTENSITY', 'BINNING AVERAGE LINEAR', 'INT', 'OBSERVATIONS',
        50000)

def lasd(output_folder, crs):
    """Creates a LASD dataset for further lidar processing.
    -----------
    PARAMETERS:
    -----------
    crs: str
        path to an ArcGIS projection file of the desired output coordinate
        reference system
    """
    
    import arcpy
    
    las = (f'{output_folder}\\LAS')
    lasd = (f'{output_folder}\\LASD\\Working.lasd')
    
    arcpy.management.CreateLasDataset(las, lasd, 'NO_RECURSION', '', crs,
        'COMPUTE_STATS', 'ABSOLUTE_PATHS', 'NO_FILES')

def mean(output_folder):
    """Creates a mean elevation surface from raw .las files.
    """

    import arcpy

    dem = (f'{output_folder}\\DEM\\dem.tif')

    arcpy.CheckOutExtension('SPATIAL')
    mean = arcpy.sa.FocalStatistics(dem, '', 'MEAN')
    mean.save(f'{output_folder}\\Mean\\mean.tif')
    arcpy.CheckInExtension('SPATIAL')

def metadata(output_folder):
    """Overwrites previous year with current year in all .xml files.
    """

    import arcpy
    import glob
    import os
    from arcpy import metadata as md
    from pyxidust.utils import get_time

    terraindem_db = (f'{output_folder}\\TerrainDEM\\TerrainDEM.gdb')
    terraindsm_db = (f'{output_folder}\\TerrainDSM\\TerrainDSM.gdb')
    buildings_db = (f'{output_folder}\\Buildings\\Buildings.gdb')
    contours_db = (f'{output_folder}\\Contours\\Contours.gdb')

    hillshadedem = (f'{output_folder}\\HillshadeDEM\\hillshadedem.tif')
    hillshadedsm = (f'{output_folder}\\HillshadeDSM\\hillshadedsm.tif')
    intensity = (f'{output_folder}\\Intensity\\intensity.tif')
    terraindem = (f'{terraindem_db}\\TDEM\\Terrain_DEM')
    terraindsm = (f'{terraindsm_db}\\TDSM\\Terrain_DSM')
    contours_twenty = (f'{contours_db}\\Contours20ft')
    aspect = (f'{output_folder}\\Aspect\\aspect.tif')
    range_r = (f'{output_folder}\\Range\\range.tif')
    contours_five = (f'{contours_db}\\Contours5ft')
    contours_ten = (f'{contours_db}\\Contours10ft')
    slope = (f'{output_folder}\\Slope\\slope.tif')    
    mean = (f'{output_folder}\\Mean\\mean.tif')
    bdpatch = (f'{buildings_db}\\Buildings3D')
    dem = (f'{output_folder}\\DEM\\dem.tif')
    dsm = (f'{output_folder}\\DSM\\dsm.tif')

    meta = (f'{output_folder}\\Metadata\\')
    contourstwenty_meta = (f'{meta}Contours20ft.xml')
    hillshadedem_meta = (f'{meta}Hillsahdedem.xml')
    hillshadedsm_meta = (f'{meta}Hillshadedsm.xml')    
    contoursfive_meta = (f'{meta}Contours5ft.xml')
    contoursten_meta = (f'{meta}Contours10ft.xml')    
    buildings_meta = (f'{meta}Buildings3D.xml')
    terraindem_meta = (f'{meta}TerrainDEM.xml')
    terraindsm_meta = (f'{meta}TerrainDSM.xml')
    intensity_meta = (f'{meta}Intensity.xml')
    aspect_meta = (f'{meta}Aspect.xml')
    range_meta = (f'{meta}Range.xml')
    slope_meta = (f'{meta}Slope.xml')
    mean_meta = (f'{meta}Mean.xml')    
    dem_meta = (f'{meta}DEM.xml')
    dsm_meta = (f'{meta}DSM.xml')
    
    new year, previous_year = get_time(option='1')

    os.chdir(meta)
    for file in glob.glob('*.xml'):
        with open(file, 'r') as xml:
            text = xml.read().replace(previous_year, new_year)
        with open(file, 'w+') as xml:
            xml.write(text)

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

def ranged(output_folder):
    """Creates a high-resolution range raster from a digital surface
    model.
    """

    import arcpy

    dsm = (f'{output_folder}\\DSM\\dsm.tif')

    arcpy.CheckOutExtension('SPATIAL')
    ranged = arcpy.sa.FocalStatistics(dsm, '', 'RANGE')
    ranged.save(f'{output_folder}\\Range\\range.tif')
    arcpy.CheckInExtension('SPATIAL')

def slope(output_folder):
    """Creates a high-resolution slope raster from a digital elevation model.
    """

    import arcpy

    mean = (f'{output_folder}\\Mean\\mean.tif')

    arcpy.CheckOutExtension('SPATIAL')
    slope = arcpy.sa.SurfaceParameters(mean, 'SLOPE')
    slope.save(f'{output_folder}\\Slope\\slope.tif')
    arcpy.CheckInExtension('SPATIAL')
