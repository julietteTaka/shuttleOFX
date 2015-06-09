#!/usr/bin/env python
from flask import Flask, request, jsonify, send_file, abort, Response
from bson import json_util, ObjectId
import os
import uuid
import json
import atexit
import pymongo
import logging
import tempfile
import ConfigParser
import multiprocessing

import renderScene

configParser =  ConfigParser.RawConfigParser()
configParser.read('render.cfg')

g_app = Flask(__name__, static_folder='', static_url_path='')

# list of all computing renders
g_renders = {}
g_rendersSharedInfo = {}

# Pool for rendering jobs
# processes=None => os.cpu_count()
g_pool = multiprocessing.Pool(processes=4)
g_enablePool = False

# Manager to share rendering information
g_manager = multiprocessing.Manager()

# mongoDB initialization
client = pymongo.MongoClient(configParser.get('MONGODB', 'hostname'), configParser.getint('MONGODB', 'port'))
db = client.__getattr__(configParser.get('MONGODB', 'dbName'))
resourceTable = db.__getattr__(configParser.get('MONGODB', 'resourceTable'))


currentAppDir = os.path.dirname(os.path.abspath(__file__))

renderDirectory = os.path.join(currentAppDir, configParser.get('RENDERED_FILES', 'renderedFilesDirectory'))
if not os.path.exists(renderDirectory):
    os.makedirs(renderDirectory)

resourcesPath = os.path.join(currentAppDir, configParser.get('RESOURCES', 'resourcesDirectory'))
if not os.path.exists(resourcesPath):
    os.makedirs(resourcesPath)


# TODO: replace multiprocessing with https://github.com/celery/billiard to have timeouts in the Pool.

# TODO atexit:
# g_pool.terminate()
# g_pool.join()

def mongodoc_jsonify(*args, **kwargs):
    return Response(json.dumps(args[0], default=json_util.default), mimetype='application/json')

def remapPath(datas):
    '''
    Replace PATTERNS with real filepaths.
    '''
    outputResources = []
    for node in datas['nodes']:
        for parameter in node['parameters']:
            logging.warning('param: %s %s', parameter['id'], parameter['value'])
            if isinstance(parameter['value'], (str, unicode)):

                if '{RESOURCES_DIR}' in parameter['value']:
                    parameter['value'] = parameter['value'].replace('{RESOURCES_DIR}', resourcesPath)

                if '{UNIQUE_OUTPUT_FILE}' in parameter['value']:
                    prefix, suffix = parameter['value'].split('{UNIQUE_OUTPUT_FILE}')
                    _, tmpFilepath = tempfile.mkstemp(prefix=prefix, suffix=suffix, dir=renderDirectory)
                    outputResources.append(os.path.basename(tmpFilepath))
                    parameter['value'] = tmpFilepath

    return outputResources


@g_app.route('/render', methods=['POST'])
def newRender():
    '''
    Create a new render and return graph informations.
    '''
    global g_renders, g_pool

    datas = request.json
    renderID = str(uuid.uuid1())

    outputResources = remapPath(datas)

    newRender = {}
    newRender['id'] = renderID
    # TODO: return a list of output resources in case of several writers.
    newRender['outputFilename'] = outputResources[0]
    newRender['scene'] = datas
    g_renders[renderID] = newRender

    g_app.logger.debug('new resource is ' + newRender['outputFilename'])

    renderSharedInfo = g_manager.dict()
    renderSharedInfo['status'] = 0
    g_rendersSharedInfo[renderID] = renderSharedInfo

    if g_enablePool:
        g_pool.apply(renderScene.computeGraph, args=[renderSharedInfo, newRender])
    else:
        renderScene.computeGraph(renderSharedInfo, newRender)
    
    return jsonify(render=newRender)


@g_app.route('/progress/<renderID>', methods=['GET'])
def getProgress(renderID):
    '''
    Return render progress.
    '''
    return str(g_rendersSharedInfo[renderID]['status'])


@g_app.route('/render', methods=['GET'])
def getRenders():
    '''
        Returns all renders in JSON format
    '''
    totalRenders = {"renders": g_rendersSharedInfo}
    return jsonify(**totalRenders)


@g_app.route('/render/<renderID>', methods=['GET'])
def getRenderById(renderID):
    '''
    Get a render by id in json format.
    '''

    for key, render in g_renders.iteritems():
        if renderID == key:
            return jsonify(render=render)
    g_app.logger.error('id '+ renderID +" doesn't exists")
    abort(404)


@g_app.route('/render/<renderId>/resource/<resourceId>', methods=['GET'])
def resource(renderId, resourceId):
    '''
    Returns file resource by renderId and resourceId.
    '''
    if not os.path.isfile( os.path.join(renderDirectory, resourceId) ):
        logging.error(renderDirectory + resourceId + " doesn't exists")
        aboirt(404)

    return send_file( os.path.join(renderDirectory, resourceId) )

@g_app.route('/render/<renderID>', methods=['DELETE'])
def deleteRenderById(renderID):
    '''
    Delete a render from the render array.
    TODO: needed?
    TODO: kill the corresponding process?
    '''
    if renderID not in g_renders:
        g_app.logger.error('id '+renderID+" doesn't exists")
        abort(400)
    del g_renders[renderID]


@g_app.route('/resource', methods=['POST'])
def addResource():
    '''
    Upload resource file on the database
    '''
    if not 'file' in request.files:
        abort(404)

    mimetype = request.files['file'].content_type

    if not mimetype:
        g_app.logger.error("Invalide resource.")
        abort(404)

    uid = resourceTable.insert({
        "mimetype" : mimetype,
        "size" : request.content_length,
        "name" : request.files['file'].filename})

    imgFile = os.path.join(resourcesPath, str(uid))
    file = request.files['file']
    file.save(imgFile)
    
    resource = resourceTable.find_one({ "_id" : ObjectId(uid)})
    return mongodoc_jsonify(resource)


@g_app.route('/resource/<resourceId>', methods=['GET'])
def getResource(resourceId):
    '''
    Returns resource file.
    '''
    resource = os.path.join(resourcesPath, resourceId)

    if os.path.isfile(resource):
        return send_file(resource)
    else:
        g_app.logger.error("can't find " + resource)
        abort(404)

@g_app.route('/resource/', methods=['GET'])
def getResourcesDict():
    '''
    Returns all resources files from db.
    '''
    count = int(request.args.get('count', 10))
    skip = int(request.args.get('skip', 0))
    resources = resourceTable.find().limit(count).skip(skip)
    return mongodoc_jsonify({"resources":[ result for result in resources ]})

@g_app.route('/upload', methods=['GET'])
def uploadPage():
    return """<!DOCTYPE html>
      <html lang="en">
      <head>
      </head>
      <body>
        <div class="container">
          <div class="header">
            <h3 class="text-muted">UPLOAD A RESOURCE</h3>
          </div>
          <hr/>
          <div>
            <form action="/resource" method="POST" enctype="multipart/form-data">
              <input type="file" name="file">
              <br/><br/>
              <input type="submit" value="Upload">
            </form>
          </div>
        </div>
      </body>
      </html>"""

@atexit.register
def cleanPool():
    '''
    Close processes and quit pool at exit.
    '''
    g_pool.close()
    g_pool.terminate()
    g_pool.join()

if __name__ == "__main__":
    g_app.run(host=configParser.get("APP_RENDER", "host"), port=configParser.getint("APP_RENDER", "port"), debug=True)
