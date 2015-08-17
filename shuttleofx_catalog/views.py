import os
import json
import logging
import requests

from time import sleep
from bson import json_util, ObjectId
from flask import jsonify, Response, request, abort, make_response


from Bundle import Bundle
from Plugin import Plugin

import shuttleofx_catalog as catalog

def mongodoc_jsonify(*args, **kwargs):
    return Response(json.dumps(args[0], default=json_util.default), mimetype='application/json')

@catalog.g_app.route("/")
def index():
    return "ShuttleOFX Catalog service"

@catalog.g_app.route("/bundle", methods=["POST"])
def newBundle():
    bundleName = request.get_json().get('bundleName', None)
    bundleDescription = request.get_json().get('bundleDescription', None)
    userId = request.get_json().get('userId', None)
    companyId = request.get_json().get('companyId', None)

    bundleId = catalog.bundleTable.count()

    if  bundleId == None or bundleName == None or userId == None:
        logging.error("bundleName, bundleId or userId is undefined")
        abort(make_response("bundleName, bundleId or userId is undefined", 404))

    bundle = Bundle(bundleId, bundleName, userId)
    bundle.companyId = companyId
    bundle.description = bundleDescription

    catalog.bundleTable.insert(bundle.__dict__)

    requestResult = catalog.bundleTable.find_one({"bundleId": bundleId})
    return mongodoc_jsonify(requestResult)

@catalog.g_app.route("/bundle")
def getBundles():
    count = int(request.args.get('count', 20))
    skip = int(request.args.get('skip', 0))
    bundle = catalog.bundleTable.find().limit(count).skip(skip)
    return mongodoc_jsonify({"bundles":[ result for result in bundle ]})

@catalog.g_app.route("/bundle/<int:bundleId>")
def getBundle(bundleId):
    bundle = catalog.bundleTable.find_one({"bundleId": bundleId})
    if bundle == None:
        logging.error("No matching bundle has been found")
        abort(make_response("No matching bundle has been found", 404))
    return mongodoc_jsonify(bundle)


@catalog.g_app.route('/bundle/<int:bundleId>/archive', methods=['POST', 'PUT'])
def uploadArchive(bundleId):
    bundle = catalog.bundleTable.find_one({"bundleId": bundleId})

    if bundle is None:
        logging.error("No matching bundle has been found")
        abort(make_response("No matching bundle has been found", 400))

    # mappingExtension = {
    #    "application/zip": ".zip",
    #    "application/gzip": ".tar.gz"
    # }

    # if request.headers['content-type'] not in mappingExtension:
    #     catalog.g_app.logger.error("Format is not supported : " + str(request.headers['content-type']))
    #     abort(400)

    #extension = mappingExtension[ request.headers['content-type'] ]
    extension = ".tar.gz"

    archivePath = os.path.join(catalog.bundleRootPath, str(bundleId) + extension)

    try:
        file = request.files['file']
        file.save(archivePath)
    except Exception, err:
        logging.error(err)
        abort(400)

    bundle["archivePath"] = archivePath
    catalog.bundleTable.update({'_id': bundle['_id']}, bundle)
    return mongodoc_jsonify(bundle)


@catalog.g_app.route('/bundle/<int:bundleId>/analyse', methods=['POST'])
def analyseBundle(bundleId):
    bundle = catalog.bundleTable.find_one({"bundleId": bundleId})

    if bundle == None:
        logging.error("No matching bundle has been found")
        abort(make_response("No matching bundle has been found", 400))

    if bundle["archivePath"] == None: 
        logging.error("The bundle as no directory path")
        abort(make_response("The bundle as no directory path", 400))

    headers = {'content-type': 'application/gzip'}
    analyseReturn = requests.post(
        catalog.uriAnalyser+"/bundle/"+str(bundleId),
        data=open(bundle["archivePath"], 'r').read(),
        headers=headers).json()

    # logging.error("analyzeBundle analyseReturn: " + str(analyseReturn))

    pluginIdOffset = catalog.pluginTable.count()

    while 1:
        analyseReturn = requests.get(catalog.uriAnalyser+"/bundle/"+str(bundleId)).json()

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
        catalog.pluginTable.insert(currentPlugin.__dict__)

    return mongodoc_jsonify(bundle)

@catalog.g_app.route("/bundle/<int:bundleId>", methods=["DELETE"])
def deleteBundle(bundleId):
    bundle = catalog.bundleTable.find_one({"bundleId": bundleId})
    if bundle == None:
        abort(404)

    for pluginId in bundle.plugins:
        deleteStatus = catalog.pluginTable.remove({"pluginId":pluginId})
        if deleteStatus['n'] == 0:
            abort(404)

    deleteStatus = catalog.bundleTable.remove({"bundleId":bundleId})

    if deleteStatus['n'] == 0:
        abort(404)

    return jsonify(**deleteStatus)

@catalog.g_app.route("/bundle/<int:bundleId>/plugin", methods=['POST'])
def newPlugin(bundleId):
    pluginId = request.get_json().get('pluginId', None)
    pluginName = request.get_json().get('name', None)

    if pluginId == None or pluginName == None:
        abort(404)

    plugin = Plugin(pluginId, bundleId, pluginName)
    
    catalog.pluginTable.insert(plugin.__dict__)

    requestResult = catalog.pluginTable.find_one({"pluginId": pluginId})
    return mongodoc_jsonify(requestResult)


@catalog.g_app.route("/bundle/<int:bundleId>/plugin")
def getPlugins(bundleId):
    count = int(request.args.get('count', 20))
    skip = int(request.args.get('skip', 0))
    plugin = catalog.pluginTable.find({"bundleId":bundleId}).limit(count).skip(skip)
    return mongodoc_jsonify({"plugins":[ result for result in plugin ]})

@catalog.g_app.route("/plugin")
def getAllPlugins():
    #Text search
    keyWord = request.args.get('keyWord', None)
    
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

    count = int(request.args.get('count', 20))
    skip = int(request.args.get('skip', 0))


    if keyWord != None :
        return textSearchPlugin(keyWord, count)

    else :
        plugin = catalog.pluginTable.find().sort('name' , alphaSort).limit(count).skip(skip)
        return mongodoc_jsonify({"plugins":[ result for result in plugin ]})


def textSearchPlugin(keyWord, count):
    #To Do Tags
    plugin = catalog.pluginTable.find({"rawIdentifier":keyWord})
    return mongodoc_jsonify({"plugins":[ result for result in plugin ]})


@catalog.g_app.route("/bundle/<int:bundleId>/plugin/<int:pluginId>")
@catalog.g_app.route("/plugin/<int:pluginId>")
def getPlugin(pluginId, bundleId=None):
    plugin = catalog.pluginTable.find_one({"pluginId": pluginId})
    if plugin == None:
        abort(404)

    return mongodoc_jsonify(plugin)


@catalog.g_app.route("/bundle/<rawIdentifier>/bundle", methods=['GET'])
def getBundleByPluginId(rawIdentifier):
    '''
    Returns the bundleid of a plugin using its pluginId.
    '''
    bundleId = catalog.pluginTable.find_one({'rawIdentifier':rawIdentifier}, {"bundleId":1, "_id":0})

    if bundleId is None:
        logging.error("plugin "+rawIdentifier+" doesn't exists")
        abort(make_response("plugin "+rawIdentifier+" doesn't exists", 404))
        
    return mongodoc_jsonify(bundleId)


@catalog.g_app.route('/resources', methods=['POST'])
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

    uid = catalog.resourceTable.insert({ 
        "mimetype" : mimetype,
        "size" : size,
        "name" : name})

    img = request.data


    imgFile = os.path.join(catalog.resourcesPath, str(uid))
    file = request.files['file']
    file.save(imgFile)

    resource = catalog.resourceTable.find_one({ "_id" : ObjectId(uid)})
    return mongodoc_jsonify(resource)

@catalog.g_app.route('/resources', methods=['GET'])
def getResources():
    '''
    Returns resource file from db.
    '''

    count = int(request.args.get('count', 10))
    skip = int(request.args.get('skip', 0))
    resources = catalog.resourceTable.find().limit(count).skip(skip)
    return mongodoc_jsonify({"resources":[ result for result in resources ]})

@catalog.g_app.route('/resources/<resourceId>', methods=['GET'])
def getResourceById(resourceId):
    '''
    Returns resource datas from db.
    '''
    resourceData = catalog.resourceTable.find_one({ "_id" : ObjectId(resourceId)})

    if resourceData == None:
        abort(404)
    return mongodoc_jsonify(resourceData)


@catalog.g_app.route('/resources/<resourceId>/data', methods=['GET'])
def getResourceData(resourceId):
    '''
     Returns the resource.
    '''

    resourceData = catalog.resourceTable.find_one({ "_id" : ObjectId(resourceId)})
    if not resourceData:
        abort(404)

    filePath = os.path.join (catalog.resourcesPath, resourceId)

    if not os.path.isfile(filePath):
        abort(404)

    resource = open(filePath)
    return Response(resource.read(), mimetype=resourceData['mimetype'])


@catalog.g_app.route("/plugin/<int:pluginId>/images", methods= ['POST'])
def addImageToPlugin(pluginId):
    if "ressourceId" not in request.get_json() :
        abort(404)

    imageId = request.get_json()["ressourceId"]

    plugin = catalog.pluginTable.find_one({"pluginId": pluginId})
    if plugin == None:
        abort(404)

    catalog.pluginTable.update({"pluginId" : pluginId}, { '$addToSet' : {"sampleImagesPath" : imageId} }, upsert=True)
    plugin = catalog.pluginTable.find_one({"pluginId": pluginId})
    
    return mongodoc_jsonify(plugin)

#TO DO : Tags
catalog.pluginTable.ensure_index([
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
