# Pyxidust: geoprocessing/lidar/project tools for ESRI ArcGIS PRO software
# Copyright (C) 2024  Gabriel Peck  pyxidust@pm.me
###############################################################################

import os
import time

# get year to construct serials
YEAR = int(time.strftime('%Y', time.localtime()))

# get working folder path; all references are built from ROOT
ROOT = os.path.normpath(os.getcwd())

###############################################################################
# FOLDER PATHS:
###############################################################################

ARCHIVE = (f'{ROOT}\\archive')
PROJECTS = (f'{ROOT}\\projects')
TEMPLATES = (f'{ROOT}\\templates')
LAYOUTS = (f'{ROOT}\\templates\\newproject\\templates')

###############################################################################
# FILE PATHS:
###############################################################################

CATALOG = (f'{ROOT}\\files\\catalog.csv')
SERIALS = (f'{ROOT}\\files\\serials.txt')

###############################################################################
# CONSTANTS:
###############################################################################

# default files/folders created by ArcGIS PRO new projects
DEFAULT_FILES = ['.aprx', '.temp', '.tmp']
DEFAULT_FOLDERS = ['.', 'Index', 'GPMessages', 'Raster']

# pyramid steps for terrains
LEVELS = '2.5 1200; 5 2500; 7 5000; 15 10000; 20 24000; 25 62500; 30 100000'

# template sizes for layouts
SIZES = {'P_08x11', 'P_11x17', 'P_18x24', 'P_24x36', 'P_36x48', 'L_08x11',
        'L_11x17', 'L_18x24', 'L_24x36', 'L_36x48'}
