
from flask import (
    make_response,
    request,
    jsonify,
    abort
)

import config
import logging
import multiprocessing
import Bundle
import atexit

# Pool for analysing jobs 
config.g_pool = multiprocessing.Pool(processes=4)
g_sharedBundleDatas = {}
g_enablePool = True

# Manager to share analysing information
g_manager = multiprocessing.Manager()

@config.g_app.route('/', methods=['GET'])
def index():
    return "ShuttleOFX Analyser service"

@config.g_app.route('/bundle/<bundleId>', methods=['POST'])
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
        config.g_pool.apply(Bundle.launchAnalyse, args=[datas, bundleExt, bundleBin, bundleId])
    else:
        Bundle.launchAnalyse(datas, bundleExt, bundleBin, bundleId)

    return jsonify(**datas)

@config.g_app.route('/bundle/<bundleId>', methods=['GET'])
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
    config.g_pool.close()
    config.g_pool.terminate()
    config.g_pool.join()

if __name__ == '__main__':
    config.g_app.run(host="0.0.0.0",port=5004, debug=True)