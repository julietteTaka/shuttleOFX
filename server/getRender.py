from flask import Flask, jsonify, request, send_file, abort
import os, uuid, time, random, ConfigParser

app = Flask(__name__, static_folder='', static_url_path='')

configParser =  ConfigParser.RawConfigParser()
configParser.read('worker/configuration.conf')

listImg = {}
renderList = {}



@app.route('/render/', methods=['POST'])
def render():

    scene = request.get_json()
    uid = str(uuid.uuid1())
    outputId = random.choice(listImg.keys())

    newRender = {}
    newRender['id'] = uid
    newRender['outputFile'] = outputId
    newRender['scene'] = scene
    renderList['outputListId'] = ["sample"]

    response = jsonify(**newRender)

    time.sleep(2)

    return response



@app.route('/resources/', methods=['GET'])
def getResourcesDict():
    ret = {"files" : listImg }
    return jsonify(**ret)


@app.route('/resources/<resourceId>', methods=['GET'])
def resource(resourceId):
    print resourceId
    print listImg
    

    if os.path.isfile("resources/"+resourceId):
        return send_file("resources/"+resourceId)
    abort(404)
    return

@app.route('/resources/', methods=['POST'])
def addResource():
    global listImg

    uid = str(uuid.uuid1())
    img = request.data

    ext = request.headers.get("Content-Type").split('/')[1]

    imgFile = "/resources/" + uid + "." + ext

    f = open("resources/" + uid + "." + ext, 'w')
    f.write(img)
    f.close()

    objectId = {'id': uid,
                'uri': imgFile
    }

    listImg[uid] = imgFile

    return jsonify(**objectId)

def getAllResources():
    for image in os.listdir(os.getcwd() + "/resources"):
        _id = str(uuid.uuid4())
        listImg[_id] = "/resources/" + str(image)

if __name__ == "__main__":
    getAllResources()
    app.run(host=configParser.get("APP_RENDER", "host"), port=configParser.getint("APP_RENDER", "port"), debug=True)
