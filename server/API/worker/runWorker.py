from pyTuttle import tuttle
from flask import Flask, jsonify, request, abort, send_file
from logging.handlers import RotatingFileHandler
import tempfile
import uuid
import io
import logging
import os

#class
import renderScene

app = Flask(__name__)
renders = []

currentAppDir = os.path.dirname(__file__)
tmpRenderingPath = os.path.join(currentAppDir, "tmp")
if not os.path.exists(tmpRenderingPath):
  os.mkdir(tmpRenderingPath)

'''
sendGraphExample = {
    "nodes": [
        {
            "id": 0,
            "plugin": "tuttle.text",
           "parameters" : [
                {
                    "id":"color",
                    "value":[1,0,1,1]
                },
                {
                    "id":"text",
                    "value": "HEY CECI EST UN SUPER PROJET"
                },
                {
                    "id":"italic",
                    "value": true
                },
                {
                    "id":"textSize",
                    "value": 80
                }
           ]
        },
        {
            "id": 1,
            "plugin": "tuttle.pngwriter",
           "parameters" : []
        }
    ],
    "connections": [
        {"src": {"id": 0}, "dst": {"id": 1}}
    ]
}
'''

# send graph informations, nodes and connections
@app.route('/render', methods=['POST'])
def newRender():
    datas = request.json
    userID = "jonhDoe"

    tmpFile = tempfile.mkstemp(prefix='tuttle_', suffix="_"+userID+".png", dir=tmpRenderingPath)
    renderID = str(uuid.uuid1())

    render = {
    "id" : renderID,
    "scene" : datas,
    "resources": [
        "/render/"+str(renderID)+"/resources/"+os.path.basename(tmpFile[1])
    ]}

    app.logger.debug("new resource id is " + os.path.basename(tmpFile[1]))
    renders.append( render )

    r = renderScene.RenderScene()
    r.setPluginPaths("")
    r.loadGraph(render, outputFilename=tmpFile[1])
    r.computeGraph()
    
    return jsonify(renderID=renderID) #is it useful to return the json instead of the renderid?

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
def updateRequest(renderID):
    if renderID not in renders:
        app.logger.error('id '+renderID+" doesn't exists")
        abort(404)
    for key, value in request.json["update"].items():
        renders[renderID][key] = value


# return all renders in json format
@app.route('/render', methods=['GET'])
def getRenders():
    totalRenders = {"renders": renders}
    return jsonify(**totalRenders)


# get a render by id in json format
@app.route('/render/<renderID>', methods=['GET'])
def getRenderById(renderID):
    if renderID not in renders:
        jsonify(render=None)
        app.logging.error('id '+renderID+" doesn't exists")
        abort(404)
    return jsonify(render=renders[renderID])

@app.route('/render/<renderId>/resources/<resourceId>', methods=['GET'])
def resource(renderId, resourceId):
    if os.path.isfile('tmp/' + resourceId):
        return send_file('tmp/' + resourceId, mimetype='image/png')
    else:
        logging.error('tmp/' + resourceId + " doesn't exists")
        abort(404)


# delete a render from the render array
@app.route('/render/<renderID>', methods=['DELETE'])
def deleteRenderById(renderID):
    print renders
    print renders["id"]
    if renderID not in renders:
        app.logger.error('id '+renderID+" doesn't exists")
        abort(400)
    del renders[renderID]


if __name__ == "__main__":
    app.run(debug=True)
    handler = RotatingFileHandler('/tmp/apiMethods.log', backupCount=1)
    handler.setLevel(logging.DEBUG)
    app.logger.addHandler(handler)