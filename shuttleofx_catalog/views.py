import os
import json
import logging
import requests
import re

from time import sleep
from bson import json_util, ObjectId
from flask import jsonify, Response, request, abort, make_response

import config

from Bundle import Bundle
from Plugin import Plugin


def mongodoc_jsonify(*args, **kwargs):
    return Response(json.dumps(args[0], default=json_util.default), mimetype='application/json')

@config.g_app.route("/")
def index():
    return "ShuttleOFX Catalog service"

@config.g_app.route("/bundle", methods=["POST"])
def newBundle():
    bundleName = request.get_json().get('bundleName', None)
    bundleDescription = request.get_json().get('bundleDescription', None)
    userId = request.get_json().get('userId', None)
    companyId = request.get_json().get('companyId', None)

    bundleId = config.bundleTable.count()

    if  bundleId == None or bundleName == None or userId == None:
        logging.error("bundleName, bundleId or userId is undefined")
        abort(make_response("bundleName, bundleId or userId is undefined", 404))

    bundle = Bundle(bundleId, bundleName, userId)
    bundle.companyId = companyId
    bundle.description = bundleDescription

    config.bundleTable.insert(bundle.__dict__)

    requestResult = config.bundleTable.find_one({"bundleId": bundleId})
    return mongodoc_jsonify(requestResult)

@config.g_app.route("/bundle")
def getBundles():
    count = int(request.args.get('count', 20))
    skip = int(request.args.get('skip', 0))
    bundle = config.bundleTable.find().limit(count).skip(skip)
    return mongodoc_jsonify({"bundles":[ result for result in bundle ]})

@config.g_app.route("/bundle/<int:bundleId>")
def getBundle(bundleId):
    bundle = config.bundleTable.find_one({"bundleId": bundleId})
    if bundle == None:
        logging.error("No matching bundle has been found")
        abort(make_response("No matching bundle has been found", 404))
    return mongodoc_jsonify(bundle)


@config.g_app.route('/bundle/<int:bundleId>/archive', methods=['POST', 'PUT'])
def uploadArchive(bundleId):
    bundle = config.bundleTable.find_one({"bundleId": bundleId})

    if bundle is None:
        logging.error("No matching bundle has been found")
        abort(make_response("No matching bundle has been found", 400))

    # mappingExtension = {
    #    "application/zip": ".zip",
    #    "application/gzip": ".tar.gz"
    # }

    # if request.headers['content-type'] not in mappingExtension:
    #     config.g_app.logger.error("Format is not supported : " + str(request.headers['content-type']))
    #     abort(400)

    #extension = mappingExtension[ request.headers['content-type'] ]
    extension = ".tar.gz"

    archivePath = os.path.join(config.bundleRootPath, str(bundleId) + extension)

    try:
        file = request.files['file']
        file.save(archivePath)
    except Exception, err:
        logging.error(err)
        abort(400)

    bundle["archivePath"] = archivePath
    config.bundleTable.update({'_id': bundle['_id']}, bundle)
    return mongodoc_jsonify(bundle)


@config.g_app.route('/bundle/<int:bundleId>/analyse', methods=['POST'])
def analyseBundle(bundleId):
    bundle = config.bundleTable.find_one({"bundleId": bundleId})

    if bundle == None:
        logging.error("No matching bundle has been found")
        abort(make_response("No matching bundle has been found", 400))

    if bundle["archivePath"] == None: 
        logging.error("The bundle as no directory path")
        abort(make_response("The bundle as no directory path", 400))

    headers = {'content-type': 'application/gzip'}
    analyseReturn = requests.post(
        config.uriAnalyser+"/bundle/"+str(bundleId),
        data=open(bundle["archivePath"], 'r').read(),
        headers=headers).json()

    # logging.error("analyzeBundle analyseReturn: " + str(analyseReturn))

    pluginIdOffset = config.pluginTable.count()

    while 1:
        analyseReturn = requests.get(config.uriAnalyser+"/bundle/"+str(bundleId)).json()

        if analyseReturn['status'] == "done":
            bundleData = analyseReturn['datas']
            break
        sleep(1)

    for index, plugin in enumerate(bundleData['plugins']) :
        pluginId = pluginIdOffset + index
        
        currentPlugin = Plugin(pluginId, bundleId)
        currentPlugin.clips = plugin['clips']
        currentPlugin.parameters = plugin['parameters']
        currentPlugin.properties = plugin['properties']
        currentPlugin.rawIdentifier = plugin['rawIdentifier']
        currentPlugin.version = plugin['version']

        # Gets Label/ShortLabel and ensures a non-empty value.
        currentPlugin.label = currentPlugin.getPropValueFromKeys(
            ('OfxPropLabel', 'OfxPropShortLabel', 'OfxPropLongLabel'),
            currentPlugin.rawIdentifier)
        currentPlugin.shortLabel = currentPlugin.getPropValueFromKeys(
            ('OfxPropShortLabel', 'OfxPropLongLabel'),
            currentPlugin.label)

        bundle['plugins'].append(pluginId)
        config.pluginTable.insert(currentPlugin.__dict__)
    return mongodoc_jsonify(bundle)


@config.g_app.route("/bundle/<int:bundleId>", methods=["DELETE"])
def deleteBundle(bundleId):
    bundle = config.bundleTable.find_one({"bundleId": bundleId})
    if bundle == None:
        abort(404)

    for pluginId in bundle.plugins:
        deleteStatus = config.pluginTable.remove({"pluginId":pluginId})
        if deleteStatus['n'] == 0:
            abort(404)

    deleteStatus = config.bundleTable.remove({"bundleId":bundleId})

    if deleteStatus['n'] == 0:
        abort(404)

    return jsonify(**deleteStatus)

@config.g_app.route("/bundle/<int:bundleId>/plugin", methods=['POST'])
def newPlugin(bundleId):
    pluginId = request.get_json().get('pluginId', None)
    pluginName = request.get_json().get('name', None)

    if pluginId == None or pluginName == None:
        abort(404)

    plugin = Plugin(pluginId, bundleId, pluginName)
    
    config.pluginTable.insert(plugin.__dict__)

    requestResult = config.pluginTable.find_one({"pluginId": pluginId})
    return mongodoc_jsonify(requestResult)


@config.g_app.route("/bundle/<int:bundleId>/plugin")
def getPlugins(bundleId):
    count = int(request.args.get('count', 20))
    skip = int(request.args.get('skip', 0))
    plugin = config.pluginTable.find({"bundleId":bundleId}).limit(count).skip(skip)
    return mongodoc_jsonify({"plugins":[ result for result in plugin ]})

@config.g_app.route("/plugin")
def getAllPlugins():
    #Text search
    keyWord = request.args.get('search', None)
    
    #Alphabetical sorting
    alphaSort = request.args.get('alphaSort', None)

    if alphaSort != None :
        if alphaSort != 'asc' and alphaSort != 'desc' :
            alphaSort = None
        else : 
            if alphaSort == 'asc' :
                alphaSort = 1
            if alphaSort == 'desc' :
                alphaSort = -1

    count = request.args.get('count', None)
    if count:
        count = int(count)
    skip = request.args.get('skip', None)
    if skip:
        skip = int(skip)

    if keyWord:
        logging.info("search: " + keyWord)
        searchRegex = re.compile(".*{search}.*".format(search=keyWord.replace("*", ".*")))
        searchKeys = ["label", "rawIdentifier", "shortDescription", "description", "properties.OfxPropPluginDescription.value"]
        cursor = config.pluginTable.find(
            {"$or":  # Search on multiple keys
                [{searchKey: searchRegex} for searchKey in searchKeys]
            })
    else:
        cursor = config.pluginTable.find()

    sortedCursor = cursor.sort("label", alphaSort)
    if count and skip:
        # logging.info("pagination -- count: " + str(count) + ", skip: " + str(skip))
        filteredCursor = sortedCursor.limit(count).skip(skip)
    else:
        filteredCursor = sortedCursor

    plugins = [ result for result in filteredCursor ]

    # logging.warning("getAllPlugins: " + str([ p["rawIdentifier"] for p in plugins ]))

    return mongodoc_jsonify({"plugins": plugins})


@config.g_app.route("/bundle/<int:bundleId>/plugin/<int:pluginId>")
@config.g_app.route("/plugin/<int:pluginId>")
def getPlugin(pluginId, bundleId=None):
    plugin = config.pluginTable.find_one({"pluginId": pluginId})
    if plugin == None:
        abort(404)

    return mongodoc_jsonify(plugin)


@config.g_app.route("/bundle/<rawIdentifier>/bundle", methods=['GET'])
def getBundleByPluginId(rawIdentifier):
    '''
    Returns the bundleid of a plugin using its pluginId.
    '''
    bundleId = config.pluginTable.find_one({'rawIdentifier':rawIdentifier}, {"bundleId":1, "_id":0})

    if bundleId is None:
        logging.error("plugin "+rawIdentifier+" doesn't exists")
        abort(make_response("plugin "+rawIdentifier+" doesn't exists", 404))
        
    return mongodoc_jsonify(bundleId)


@config.g_app.route('/resources', methods=['POST'])
def addResource():
    '''
    Upload resource file on the database
    '''

    mimetype = request.mimetype
    name = ""
    size = request.content_length

    if not mimetype:
        logging.error("Invalide resource.")
        abort(make_response("Invalide resource.", 400))

    uid = config.resourceTable.insert({ 
        "mimetype" : mimetype,
        "size" : size,
        "name" : name})

    img = request.data


    imgFile = os.path.join(config.resourcesPath, str(uid))
    file = request.files['file']
    file.save(imgFile)

    resource = config.resourceTable.find_one({ "_id" : ObjectId(uid)})
    return mongodoc_jsonify(resource)

@config.g_app.route('/resources', methods=['GET'])
def getResources():
    '''
    Returns resource file from db.
    '''

    count = int(request.args.get('count', 10))
    skip = int(request.args.get('skip', 0))
    resources = config.resourceTable.find().limit(count).skip(skip)
    return mongodoc_jsonify({"resources":[ result for result in resources ]})

@config.g_app.route('/resources/<resourceId>', methods=['GET'])
def getResourceById(resourceId):
    '''
    Returns resource datas from db.
    '''
    resourceData = config.resourceTable.find_one({ "_id" : ObjectId(resourceId)})

    if resourceData == None:
        abort(404)
    return mongodoc_jsonify(resourceData)


@config.g_app.route('/resources/<resourceId>/data', methods=['GET'])
def getResourceData(resourceId):
    '''
     Returns the resource.
    '''

    resourceData = config.resourceTable.find_one({ "_id" : ObjectId(resourceId)})
    if not resourceData:
        abort(404)

    filePath = os.path.join (config.resourcesPath, resourceId)

    if not os.path.isfile(filePath):
        abort(404)

    resource = open(filePath)
    return Response(resource.read(), mimetype=resourceData['mimetype'])


@config.g_app.route("/plugin/<int:pluginId>/images", methods= ['POST'])
def addImageToPlugin(pluginId):
    if "ressourceId" not in request.get_json() :
        abort(404)

    imageId = request.get_json()["ressourceId"]

    plugin = config.pluginTable.find_one({"pluginId": pluginId})
    if plugin == None:
        abort(404)

    config.pluginTable.update({"pluginId" : pluginId}, { '$addToSet' : {"sampleImagesPath" : imageId} }, upsert=True)
    plugin = config.pluginTable.find_one({"pluginId": pluginId})
    
    return mongodoc_jsonify(plugin)

#TO DO : Tags
config.pluginTable.ensure_index([
        ('name', 'text'),
        ('description', 'text'),
        ('shortDescription', 'text'),
    ],
    name = "search_index",
    weights={
        'name':100,
        'description':20,
        'shortDescription':60
    }
)

if __name__ == '__main__':
    config.g_app.run(host="0.0.0.0",port=5002,debug=True)