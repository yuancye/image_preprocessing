
# config.py

import os

from utils.registerClass import RegisterDir

# Define the base directory of the project
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

register = RegisterDir()

# first layer folder
DATA_DIR = register.create(BASE_DIR, 'data') # Folder for data files
LOGS_DIR = register.create(BASE_DIR, 'logs')  # Folder for log files
# RESULTS_DIR = register.create(BASE_DIR, 'results')  # Folder for result files
META_DIR = register.create(BASE_DIR, 'metadata') # Folder for metadata files
# VIA_DIR = register.create(BASE_DIR, 'via_project_raw')  # Folder for via files
SEG_DIR = register.create(BASE_DIR, 'segmentation')

#2nd layer under data
images = register.create(DATA_DIR, 'images')

#2nd layer under segmentation
sam = register.create(SEG_DIR, 'sam')
detectrons = register.create(SEG_DIR, 'detectrons')
via = register.create(SEG_DIR, 'via_project_raw')
lvis = register.create(SEG_DIR, 'lvis')



