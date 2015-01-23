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

urlAnalyser = configParser.get("APP_PLUGIN", "analyzeRootUri")


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
    myBundle = Bundle.query.filter_by(bundleId=bundleId)

    #Need to find a trick to get dynamicly the extension
    #Right now, the analyser  works with tar.gz only

    headers = {'content-type': 'application/x-gzip'}
    r = requests.post(urlAnalyser+"/analyzeBundle/", data=open('upload/'+bundleId+'.tar.gz', 'r').read(), headers=headers)
    
    pluginsOffset = Plugin.query.count()
    print pluginsOffset
    pluginsIds = []

    bundleData = json.loads(r.text)
    
    for i, plugin in enumerate(bundleData["plugins"]) :
        '''
        Fill myBundle with the pluginsIds ->stock in an array pluginsOffset + i 
        Create Plugins object from the datas and add them -> same trick to get the good values for clips and Parameter's id
        Create Parameter and clips
        Create properties
        '''
        print i , plugin['id']

    '''
    At the end of the loop -> session.commit() !
    '''
    return "Analysing the awesome"


@app.route('/bundle', methods=['GET'])
def getBundles():
    bundles = Bundle.query.all()
    return json.dumps(Bundle.serialize_list(bundles))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002 ,debug=True)
    db.create_all()

