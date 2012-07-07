#Local settings for djolio project.

import os
ROOTDIR = os.path.realpath(os.path.dirname(__file__)) + '/'
STATIC_HOST = ''
STATIC_DIR = ''
TEMPLATES_DIR = ROOTDIR + 'templates/'
UPLOADEDFILES_HOST = STATIC_HOST + 'upload/'
UPLOADEDFILES_DIR = STATIC_DIR + 'upload/'

DB_ENGINE = ''
DB_NAME = ''
DB_USER = ''
DB_PASSWORD = ''
DB_HOST = ''
DB_PORT = ''

#Defines if the system is in Dev mode or in production
DEBUG_BOOLEAN = True
