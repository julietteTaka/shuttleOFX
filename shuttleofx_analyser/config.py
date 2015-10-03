#!/usr/bin/python

import ConfigParser

from flask import (
    Flask,
    make_response,
    request,
    jsonify,
    abort
)

import multiprocessing


currentFileDir = os.path.dirname(os.path.abspath(__file__))

config =  ConfigParser.RawConfigParser()
config.read(os.path.join(currentFileDir, 'analyser.cfg'))

tmpRenderingPath = config.get('APP_ANALYSER', 'workingTmpDir')

g_app = Flask(__name__)

# Pool for analysing jobs 
g_pool = multiprocessing.Pool(processes=4)
g_sharedBundleDatas = {}
g_enablePool = True

# Manager to share analysing information
g_manager = multiprocessing.Manager()