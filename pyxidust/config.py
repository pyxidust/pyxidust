# Pyxidust: geoprocessing/lidar/project tools for ESRI ArcGIS PRO software
# Copyright (C) 2024  Gabriel Peck  pyxidust@pm.me
"""..."""
###############################################################################

import os
import time

# base for serial numbers
YEAR = int(time.strftime('%Y', time.localtime()))

# core folder structure
ROOT = rf'{os.path.normpath(os.getcwd())}\\pyxidust\\pyxidust'

###############################################################################
# FOLDER PATHS:
###############################################################################

# core folders
ARCHIVE = f'{ROOT}\\archive'
METADATA = f'{ROOT}\\metadata'
MISC = f'{ROOT}\\misc'
PROJECTS = f'{ROOT}\\projects'
SCRIPTS = f'{ROOT}\\scripts'
TEMPLATES = f'{ROOT}\\templates'
TEST = f'{ROOT}\\test'

# template folders
LIDAR = f'{TEMPLATES}\\lidar'
PROJECT = f'{TEMPLATES}\\project'

###############################################################################
# FILE PATHS:
###############################################################################

CATALOG = f'{MISC}\\catalog.csv'
SERIALS = f'{MISC}\\serials.txt'

###############################################################################
# MISC:
###############################################################################

# default files/folders created by ArcGIS PRO new projects
DEFAULT_FILES = ['.aprx', '.temp', '.tmp']
DEFAULT_FOLDERS = ['.', 'Index', 'GPMessages', 'Raster']

# pyramid steps for terrains
LEVELS = '2.5 1200; 5 2500; 7 5000; 15 10000; 20 24000; 25 62500; 30 100000'

# template sizes for layouts
SIZES = {'P_08x11', 'P_11x17', 'P_18x24', 'P_24x36', 'P_36x48', 'L_08x11',
        'L_11x17', 'L_18x24', 'L_24x36', 'L_36x48'}
