from pyTuttle import tuttle
from flask import Flask, jsonify, request, abort, Response, send_file
from logging.handlers import RotatingFileHandler
import tempfile, ConfigParser, uuid, io, logging, os

#class
import renderScene

configParser =  ConfigParser.RawConfigParser()
configParser.read('configuration.conf')

app = Flask(__name__)
renders = []

currentAppDir = os.path.dirname(__file__)
tmpRenderingPath = os.path.join(currentAppDir, "render")
if not os.path.exists(tmpRenderingPath):
  os.mkdir(tmpRenderingPath)

r = renderScene.RenderScene()

# send graph informations, nodes and connections
@app.route('/render', methods=['POST'])
def newRender():
    global r
    datas = request.json
    userID = "johnDoe"
    renderID = str(uuid.uuid1())

    tmpFile = tempfile.mkstemp(prefix='tuttle_', suffix="_"+userID+".png", dir=tmpRenderingPath)
    resourcePath = os.path.basename(tmpFile[1])

    newRender = {}
    newRender['id'] = renderID
    newRender['outputFile'] = resourcePath
    newRender['scene'] = datas

    app.logger.debug("new resource is " + resourcePath)
    renders.append( newRender )

    r = renderScene.RenderScene()
    r.setPluginPaths("")
    r.loadGraph(newRender, outputFilename=tmpFile[1])
    r.computeGraph()
    
    return jsonify(render=newRender)

'''
 update graph informations
 data example 
{
    "update": {
        "progress": 2,
        "last_request_time": 1421079769.27,
        "priority": 1
    }
}
'''

@app.route('/render/<renderID>', methods=['PUT'])
def updateRequest(renderPath):
    for render in renders:
        if renderID not in render:
            app.logger.error('id '+renderID+" doesn't exists")
            abort(404)
    for key, value in request.json["update"].items():
        renders[renderID][key] = value

# return compute status
@app.route('/stats/', methods=['GET'])
def getStatus():
    global r
    return str(r.getStatus())


# return all renders in json format
@app.route('/render', methods=['GET'])
def getRenders():
    totalRenders = {"renders": renders}
    return jsonify(**totalRenders)


# get a render by id in json format
@app.route('/render/<renderID>', methods=['GET'])
def getRenderById(renderID):
    global renders

    for render in renders:
        if renderID == render['id']:
            return jsonify(render=render)
    jsonify(render=None)
    app.logger.error('id '+ renderID +" doesn't exists")
    abort(404)


@app.route('/render/<renderId>/resources/<resourceId>', methods=['GET'])
def resource(renderId, resourceId):
    if os.path.isfile(tmpRenderingPath + "/" + resourceId):
        return send_file( tmpRenderingPath + "/" + resourceId )
    else:
        logging.error(tmpRenderingPath + resourceId + " doesn't exists")
        abort(404)


# delete a render from the render array
@app.route('/render/<renderID>', methods=['DELETE'])
def deleteRenderById(renderID):
    if renderID not in renders:
        app.logger.error('id '+renderID+" doesn't exists")
        abort(400)
    del renders[renderID]


if __name__ == "__main__":
    app.run(host=configParser.get("APP_RENDER", "host"), port=configParser.getint("APP_RENDER", "port"), debug=True)

    handler = RotatingFileHandler('/tmp/worker.log', backupCount=1)
    handler.setLevel(logging.DEBUG)
    app.logger.addHandler(handler)