from flask import Flask, jsonify, request, abort, send_file

import ConfigParser , psycopg2 , requests , uuid , json , sys

from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import func

pathToCommon = "../common"
sys.path.append(pathToCommon)

import models
from models import Bundle, Plugin, Clip, Property, Parameter

configParser =  ConfigParser.RawConfigParser()
configParser.read('configuration.conf')

dbUser = configParser.get("DB_CONFIG", "dbUser")
dbMdp = configParser.get("DB_CONFIG", "dbMdp")
dbUrl = configParser.get("DB_CONFIG", "dbUrl")
dbName = configParser.get("DB_CONFIG", "dbName")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://"+dbUser+":"+dbMdp+"@"+dbUrl+"/"+dbName
db = SQLAlchemy(app)

#urlAnalyser = configParser.get("APP_PLUGIN", "analyzeRootUri")
urlAnalyser = configParser.get("APP_PLUGIN", "analyzeFake")


def declareBundle(userId, companyId, name, description, architecture):
    b = Bundle()
    b.userId = userId
    b.companyId = companyId
    b.name = companyId
    b.description = description
    b.architecture = architecture
    return b


@app.route("/bundle", methods = ['POST'])
def insertMetaData():

    if not 'userId' in request.get_json():
        abort(404)

    userId = request.get_json()['userId']
    companyId = request.get_json()['companyId']
    name = request.get_json()['name']
    description = request.get_json()['description']
    architecture = request.get_json()['architecture']

    b = declareBundle(userId, companyId, name, description, architecture) 

    db.session.add(b)
    db.session.commit()

    data = {}
    data["uriBundle"] = "/bundle/"+str(b.bundleId)
    data["uriArchive"] = "/bundle/"+str(b.bundleId)+"/archive"
    myBundle = Bundle.query.filter_by(bundleId=b.bundleId)
    data["b"] = Bundle.serialize_list(myBundle)

    print data
    return jsonify(**data)


@app.route("/bundle/<bundleId>/archive", methods = ['POST'])
def createBundleArchive(bundleId):
    print request.headers
    print request.headers['content-type']

    fileName = str(bundleId)

    mappingExtension = { 'application/zip': "zip", "application/gzip": "tar.gz"}

    if request.headers['content-type'] not in mappingExtension:
        abort(400)

    extension = mappingExtension[ request.headers['content-type'] ]

    try:
        f = open('upload/'+bundleId+'.'+extension, 'w')
        f.write(request.data)
        f.close()
    except:
        abort(400)

    data = {}
    data["uriAnalyse"] = "/bundle/"+str(bundleId)+"/analyse"
    return jsonify(**data)

@app.route("/bundle/<bundleId>/analyse", methods = ['POST'])
def analyseBundle(bundleId):

    #Need to find a trick to get dynamicly the extension
    #Right now, the analyser  works with tar.gz only

    headers = {'content-type': 'application/x-gzip'}
    r = requests.post(urlAnalyser+"/analyzeBundle/", data=open('upload/'+bundleId+'.tar.gz', 'r').read(), headers=headers)
    
    pluginsOffset = Plugin.query.count()
    
    pluginsIds = []

    bundleData = json.loads(r.text)

    for i, plugin in enumerate(bundleData["plugins"]) :
        
        '''
        Fill myBundle with the pluginsIds ->stock in an array pluginsOffset + i 
        Create Plugins object from the datas and add them -> same trick to get the good values for clips and Parameter's id
        Create Parameter and clips
        Create properties
        '''
        #Potentially these values are increased after a plugin is added in the DB
        clipOffset = Clip.query.count()
        parameterOffset = Parameter.query.count()

        clipsIds = []
        paramIds = []
        pluginsIds.append(i + pluginsOffset)

        p = Plugin()
        p.bundleId = bundleId

        p.bundleId = bundleId
        p.pluginUid = plugin['id']
        p.version = [plugin['version']['major'], plugin['version']['minor']]
        
        p.defautImagePath = plugin['defaultImagePaths']
        p.sampleImagePath = plugin['sampleImagePaths']
        
        p.presets = json.dumps(plugin['presets'])
        p.rate = 0
        p.tags = plugin['tags']

        p.name = 'noName'
        p.description = 'no description yet'
        p.shortDescription = ''

        p.properties = json.dumps(plugin['properties'])
       
        for prop in plugin['properties'] : 
            
            if prop['name'] == "OfxPropShortLabel" :
                p.name = prop['value'][0]
            
            if prop['name'] == 'OfxPropPluginDescription' :
                p.description = prop['value'][0]
            
            if prop['name'] == 'OfxPropPluginShortDescription' :
                p.shortDescription = prop['value'][0]
            else : 
                prop['value'][0] = p.description


        if len(plugin['clips']) > 0 :

            for z in range(clipOffset, clipOffset+len(plugin['clips'])) : 
                clipsIds.append(z+1)

            for j, clip in enumerate(plugin['clips']) : 
                c = Clip()
                for propObj in clip : 
                    propertyClip = Property(j+clipOffset+1, True)

                    if 'name' in propObj :
                        propertyClip.name = propObj['name']

                    if 'type' in propObj : 
                        propertyClip.paramType = propObj['type']

                    if 'value' in propObj : 
                        propertyClip.value = propObj['value']

                    if 'readOnly' in propObj : 
                        propertyClip.readOnly = propObj['readOnly']
                    db.session.add(propertyClip)
                db.session.add(c)


        if len(plugin['parameters']) > 0 :

            for v in range(parameterOffset, parameterOffset+len(plugin['parameters'])) : 
                paramIds.append(v+1)

            for j, param in enumerate(plugin['parameters']) : 
                pa = Parameter()
                for propObj in param : 
                    propertyParam = Property(j+parameterOffset+1, False)
                    if 'name' in propObj :
                        propertyParam.name = propObj['name']

                    if 'type' in propObj : 
                        propertyParam.paramType = propObj['type']

                    if 'value' in propObj : 
                        propertyParam.value = propObj['value']

                    if 'readOnly' in propObj : 
                        propertyParam.readOnly = propObj['readOnly']
                    db.session.add(propertyParam)
                db.session.add(pa)

        p.clip = clipsIds
        p.parameters = paramIds
        db.session.add(p)
        db.session.commit()
    myBundle = Bundle.query.filter_by(bundleId=bundleId).first()
    myBundle.plugins = pluginsIds
    myBundle.uploaded = True
    
    db.session.commit()

    data = {}
    data["bundleId"] = str(bundleId)
    return jsonify(**data)


@app.route('/bundle', methods=['GET'])
def getBundles():
    bundles = Bundle.query.all()
    return json.dumps(Bundle.serialize_list(bundles))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002 ,debug=True)
    db.create_all()

