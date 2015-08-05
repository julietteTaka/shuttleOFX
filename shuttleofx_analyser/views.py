
import shuttleofx_analyser as analyser

from flask import (
    make_response,
    request,
    jsonify,
    abort
)

import logging
import multiprocessing
import Bundle
import atexit

# Pool for analysing jobs 
g_pool = multiprocessing.Pool(processes=4)
g_sharedBundleDatas = {}
g_enablePool = True

# Manager to share analysing information
g_manager = multiprocessing.Manager()

@analyser.g_app.route('/', methods=['GET'])
def index():
    return "ShuttleOFX Analyser service"

@analyser.g_app.route('/bundle/<bundleId>', methods=['POST'])
def analyseBundle(bundleId):
    '''
    Apply a pool of process to analyse bundles asynchronously.
    '''
    global g_sharedBundleDatas, g_pool, g_enablePool

    bundleBin = request.data
    bundleExt = request.headers.get('Content-Type')

    if bundleId in g_sharedBundleDatas:
        logging.warning('Bundle {bundleId} already exists. It will be overridden.'.format(bundleId=bundleId))

    datas = g_sharedBundleDatas[bundleId] = g_manager.dict()

    datas['status'] = "waiting"
    datas['analyse'] = "waiting"
    datas['extraction'] = "waiting"
    datas['datas'] = None

    logging.warning('analyseBundle {bundleId}: {datas}'.format(bundleId=bundleId, datas=datas))

    if g_enablePool:
        g_pool.apply(Bundle.launchAnalyse, args=[datas, bundleExt, bundleBin, bundleId])
    else:
        Bundle.launchAnalyse(datas, bundleExt, bundleBin, bundleId)

    return jsonify(**datas)

@analyser.g_app.route('/bundle/<bundleId>', methods=['GET'])
def getStatus(bundleId):
    '''
    Return the analyse status.
    '''
    global g_sharedBundleDatas
    if bundleId not in g_sharedBundleDatas:
        logging.error("the id"  + bundleId + "doesn't exist")
        abort(make_response("the id"  + bundleId + "doesn't exist", 404))

    return jsonify(**g_sharedBundleDatas[bundleId])

@atexit.register
def quit():
    '''
    Close processes and quit pool at exit.
    '''
    global g_pool
    g_pool.close()
    g_pool.terminate()
    g_pool.join()