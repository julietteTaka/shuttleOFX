#!/usr/bin/python

import ConfigParser

from flask import (
	Flask,
    make_response,
    request,
    jsonify,
    abort
)

import logging
import multiprocessing
import Bundle
import atexit

config =  ConfigParser.RawConfigParser()
config.read( "/etc/shuttleofx/analyser.cfg" )

tmpRenderingPath = config.get('APP_ANALYSER', 'workingTmpDir')

g_app = Flask(__name__)

# Pool for analysing jobs 
g_pool = multiprocessing.Pool(processes=4)
g_sharedBundleDatas = {}
g_enablePool = True

# Manager to share analysing information
g_manager = multiprocessing.Manager()

@g_app.route('/', methods=['GET'])
def index():
    return "ShuttleOFX Analyser service"

@g_app.route('/bundle/<bundleId>', methods=['POST'])
def analyseBundle(bundleId):
    '''
    Apply a pool of process to analyse bundles asynchronously.
    '''

    bundleBin = request.data
    bundleExt = request.headers.get('Content-Type')

    if bundleId in g_sharedBundleDatas:
        logging.warning("Bundle %(bundleId)s already exists. It will be overridden." % {"bundleId":bundleId})

    datas = g_sharedBundleDatas[bundleId] = g_manager.dict()

    datas['status'] = "waiting"
    datas['analyse'] = "waiting"
    datas['extraction'] = "waiting"
    datas['datas'] = None

    logging.warning("analyseBundle %(bundleId)s : %(datas)s." % {"bundleId":bundleId, "datas":datas})

    if g_enablePool:
        g_pool.apply(Bundle.launchAnalyse, args=[datas, bundleExt, bundleBin, bundleId])
    else:
        Bundle.launchAnalyse(datas, bundleExt, bundleBin, bundleId)

    return jsonify(**datas)

@g_app.route('/bundle/<bundleId>', methods=['GET'])
def getStatus(bundleId):
    '''
    Return the analyse status.
    '''
    if bundleId not in g_sharedBundleDatas:
        logging.error("The id " + bundleId + " doesn't exist")
        abort(make_response("The id " + bundleId + " doesn't exist", 404))

    return jsonify(**g_sharedBundleDatas[bundleId])

@atexit.register
def quit():
    '''
    Close processes and quit pool at exit.
    '''
    g_pool.close()
    g_pool.terminate()
    g_pool.join()

if __name__ == '__main__':
    g_app.run(host="0.0.0.0",port=5004, debug=True)