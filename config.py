# pyxidust library configurations
# Gabriel Peck 2023 (MIT license)

import os
import time

# from string import punctuation as SPECIAL
# from string import ascii_lowercase as LOWER
# from string import ascii_uppercase as UPPER

# get year to construct serials
current_time = time.localtime()
YEAR = int(time.strftime('%Y', current_time))

# get working folder path; all references are built from ROOT
ROOT = os.path.normpath(os.getcwd())

# folder paths
ARCHIVE = (f'{ROOT}\\archive')
PROJECTS = (f'{ROOT}\\projects')
TEMPLATES = (f'{ROOT}\\templates')

# file paths
CATALOG = (f'{ROOT}\\files\\catalog.csv')
SERIALS = (f'{ROOT}\\files\\serials.txt')

# constants
LAYOUTS = {'P_08x11', 'P_11x17', 'P_18x24', 'P_24x36', 'P_36x48', 'L_08x11',
             'L_11x17', 'L_18x24', 'L_24x36', 'L_36x48'}
