import os
import pymongo
import ConfigParser
from flask import Flask, jsonify, Response, request, abort, make_response


currentFileDir = os.path.dirname(os.path.abspath(__file__))

config = ConfigParser.ConfigParser()
config.read(os.path.join(currentFileDir, 'catalog.cfg'))

client = pymongo.MongoClient(config.get('MONGODB', 'hostname'), config.getint('MONGODB', 'port'))
db = client.__getattr__(config.get('MONGODB', 'dbName'))
bundleTable = db.__getattr__(config.get('MONGODB', 'bundleTable'))
pluginTable = db.__getattr__(config.get('MONGODB', 'pluginTable'))
resourceTable = db.__getattr__(config.get('MONGODB', 'resourceTable'))

uriAnalyser = config.get('ANALYSER', 'uri')

resourcesPath = config.get('RESOURCES', 'resourcesDirectory')
if not os.path.exists(resourcesPath):
    os.makedirs(resourcesPath)

bundleRootPath = config.get('CATALOG', 'bundleStore')
if not os.path.exists(bundleRootPath):
    os.makedirs(bundleRootPath)

g_app = Flask(__name__)