import os
import pymongo
import ConfigParser
import multiprocessing

from flask import Flask, request, jsonify, send_file, abort, Response, make_response
from bson import json_util, ObjectId


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

cacheMaxSize = config.getint('CACHE', 'maxSize')
cleanCacheInterval = config.getfloat('CACHE', 'interval')

# list of all computing renders
g_renders = {}
g_rendersSharedInfo = {}

# Pool for rendering jobs
# processes=None => os.cpu_count()
g_pool = multiprocessing.Pool(processes=4)
g_enablePool = False

# Manager to share rendering information
g_manager = multiprocessing.Manager()


config.read('/etc/shuttleofx/catalog.cfg')
catalogResourcesPath = config.get('RESOURCES', 'resourcesDirectory')
catalogResourceTable = db.__getattr__(config.get('MONGODB', 'resourceTable'))
