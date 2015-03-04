
import os
import json
import pymongo
import requests
import ConfigParser

from bson import json_util
from flask import Flask, jsonify, Response, request, abort

from Bundle import Bundle
from Plugin import Plugin

app = Flask(__name__)

currentDir = os.path.dirname(os.path.realpath(__file__))

config = ConfigParser.ConfigParser()
config.read('catalog.cfg')

client = pymongo.MongoClient(config.get('MONGODB', 'hostname'), config.getint('MONGODB', 'port'))
db = client.__getattr__(config.get('MONGODB', 'dbName'))
bundleTable = db.__getattr__(config.get('MONGODB', 'bundleTable'))
pluginTable = db.__getattr__(config.get('MONGODB', 'pluginTable'))

uriAnalyser = config.get('ANALYSER', 'uri')

bundleRootPath = config.get('CATALOG', 'bundleStore')
if not os.path.exists(bundleRootPath):
    os.makedirs(bundleRootPath)

@app.route("/")
def index():
    return "test catalog with mongodb"


def mongodoc_jsonify(*args, **kwargs):
    return Response(json.dumps(args[0], default=json_util.default), mimetype='application/json')

@app.route("/bundle", methods=["POST"])
def newBundle():
    bundleName = request.get_json().get('name', None)
    userId = request.get_json().get('userId', None)
    companyId = request.get_json().get('companyId', None)

    bundleId = bundleTable.count()+1

    if  bundleId == None or bundleName == None or userId == None:
        abort(404)

    bundle = Bundle(bundleId, bundleName, userId)
    
    bundleTable.insert(bundle.__dict__)

    requestResult = bundleTable.find_one({"bundleId": bundleId})
    return mongodoc_jsonify(requestResult)

@app.route("/bundle")
def getBundles():
    count = int(request.args.get('count', 10))
    skip = int(request.args.get('skip', 0))
    requestResult = bundleTable.find().limit(count).skip(skip)
    return mongodoc_jsonify({"bundles":[ result for result in requestResult ]})

@app.route("/bundle/<int:bundleId>")
def getBundle(bundleId):
    requestResult = bundleTable.find_one({"bundleId": bundleId})
    if requestResult == None:
        abort(404)
    return mongodoc_jsonify(requestResult)


@app.route('/bundle/<int:bundleId>/archive', methods=['POST'])
def uploadArchive(bundleId):
    #change var name to bundle
    requestResult = bundleTable.find_one({"bundleId": bundleId})

    if requestResult == None:
        abort(400)

    mappingExtension = {
        "application/zip": ".zip",
        "application/gzip": ".tar.gz"
    }

    if request.headers['content-type'] not in mappingExtension:
        abort(400)

    extension = mappingExtension[ request.headers['content-type'] ]

    archivePath = os.path.join("bundle", str(bundleId) + extension)

    try:
        f = open( archivePath, 'w')
        f.write(request.data)
        f.close()
    except Exception, err:
        app.logger.error(err)
        abort(400)

    requestResult["archivePath"] = archivePath
    bundleTable.update({'_id': requestResult['_id']}, requestResult)
    return mongodoc_jsonify(requestResult)


@app.route('/bundle/<int:bundleId>/analyse', methods=['POST'])
def analyseBundle(bundleId):
    bundle = bundleTable.find_one({"bundleId": bundleId})

    if bundle == None:
        abort(400)

    #We must also check and abort if the bundle as no path

    headers = {'content-type': 'application/x-gzip'}
    anylseReturn = requests.post(uriAnalyser+"/bundle/"+str(bundleId), data=open(bundle["archivePath"], 'r').read(), headers=headers)

    pluginIdOffset = pluginTable.count()
    bundleData = anylseReturn.json()

    ofxPropList = {"OfxPropShortLabel", "OfxPropLongLabel"}

    for index, plugin in enumerate(bundleData['datas']['plugins']) :
        pluginId = pluginIdOffset + index
        currentPlugin = Plugin(pluginId, bundleId)
        currentPlugin.clips = plugin['clips']
        currentPlugin.parameters = plugin['parameters']
        currentPlugin.properties = plugin['properties']
        currentPlugin.rawIdentifier = plugin['rawIdentifier']
        currentPlugin.uri = plugin['uri']
        currentPlugin.version = plugin['version']

        for prop in plugin['properties']:
            name = prop['name']
            if name in ofxPropList :
                value = prop['value']

                if name == "OfxPropShortLabel":
                    currentPlugin.shortName = value

                if name == "OfxPropLongLabel":
                    currentPlugin.name = value

        pluginTable.insert(currentPlugin.__dict__)

    return mongodoc_jsonify(bundle)

@app.route("/bundle/<int:bundleId>", methods=["DELETE"])
def deleteBundle(bundleId):
    requestResult = bundleTable.find_one({"bundleId": bundleId})
    if requestResult == None:
        abort(404)

    for plugin in requestResult.plugins:
        deleteStatus = pluginTable.remove({"pluginId":pluginId})
        if deleteStatus['n'] == 0:
            abort(404)

    deleteStatus = bundleTable.remove({"bundleId":bundleId})

    if deleteStatus['n'] == 0:
        abort(404)

    return jsonify(**deleteStatus)

@app.route("/bundle/<int:bundleId>/plugin", methods=['POST'])
def newPlugin(bundleId):
    pluginId = request.get_json().get('pluginId', None)
    pluginName = request.get_json().get('name', None)

    if pluginId == None or pluginName == None:
        abort(404)

    plugin = Plugin(pluginId, bundleId, pluginName)
    
    pluginTable.insert(plugin.__dict__)

    requestResult = pluginTable.find_one({"pluginId": pluginId})
    return mongodoc_jsonify(requestResult)


@app.route("/bundle/<int:bundleId>/plugin")
def getPlugins(bundleId):
    count = int(request.args.get('count', 10))
    skip = int(request.args.get('skip', 0))
    requestResult = pluginTable.find({"bundleId":bundleId}).limit(count).skip(skip)
    return mongodoc_jsonify({"plugins":[ result for result in requestResult ]})

@app.route("/plugin")
def getAllPlugins():
    count = int(request.args.get('count', 10))
    skip = int(request.args.get('skip', 0))
    requestResult = pluginTable.find().limit(count).skip(skip)
    return mongodoc_jsonify({"plugins":[ result for result in requestResult ]})

@app.route("/bundle/<int:bundleId>/plugin/<pluginId>")
@app.route("/plugin/<pluginId>")
def getPlugin(bundleId):
    requestResult = pluginTable.find_one({"pluginId": pluginId})
    if requestResult == None:
        abort(404)

    return mongodoc_jsonify(requestResult)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002 ,debug=True)

