#!/usr/bin/python

import os
import pymongo
import ConfigParser
from flask import Flask

config = ConfigParser.ConfigParser()
config.read('/etc/shuttleofx/catalog.cfg')

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

import shuttleofx_catalog.views
