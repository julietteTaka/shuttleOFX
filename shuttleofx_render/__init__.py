#!/usr/bin/python

import os
import pymongo
import ConfigParser
from flask import Flask

g_app = Flask(__name__)

config =  ConfigParser.RawConfigParser()
config.read('/etc/shuttleofx/render.cfg')

# mongoDB initialization
client = pymongo.MongoClient(config.get('MONGODB', 'hostname'), config.getint('MONGODB', 'port'))
db = client.__getattr__(config.get('MONGODB', 'dbName'))
resourceTable = db.__getattr__(config.get('MONGODB', 'resourceTable'))

renderDirectory = config.get('RENDERED_FILES', 'renderedFilesDirectory')
if not os.path.exists(renderDirectory):
    os.makedirs(renderDirectory)

resourcesPath = config.get('RESOURCES', 'resourcesDirectory')
if not os.path.exists(resourcesPath):
    os.makedirs(resourcesPath)

pluginsStorage = config.get('APP_RENDER', 'pluginsStorage')
catalogRootUri = config.get('APP_RENDER', 'catalogRootUri')


globalOfxPluginPath = config.get("OFX_PATH", "globalOfxPluginPath")

import shuttleofx_render.views