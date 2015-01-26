from flask import Flask, request, abort, send_file, render_template, jsonify, json, Response
import ConfigParser, requests, tarfile, uuid, os

app = Flask(__name__)

configParser =  ConfigParser.RawConfigParser()
configParser.read('client/configuration.conf')
version = "0.0.1"

analyzeRootUri = configParser.get("APP_CLIENT", "analyzeRootUri")
renderRootUri = configParser.get("APP_CLIENT", "renderRootUri")
current_render = ""
_id = 0

@app.route('/demo/')
def displayIndex():
    return render_template('base.html')

@app.route('/plugins/', methods=['GET'])
def getPlugins():
    resp = requests.get(analyzeRootUri+"/plugins/")
    return resp.text

@app.route('/demo/<resourceName>', methods=['GET'])
def resource(resourceName):
    resp = requests.get(renderRootUri + "/render/" + current_render['render']['id'] + "/resources/" + resourceName )
    return Response(resp.content, mimetype="image/png", content_type='image/png')

@app.route('/render/', methods=['POST'])
def render():
    global current_render
    headers = {
        'content-type': 'application/json'
    }
    resp = requests.post(renderRootUri + "/render", data=request.get_json(), headers=headers)
    current_render = resp.json()
    return resp.text

@app.route('/stats/', methods=['GET'])
def getStatus():
    resp = requests.get(renderRootUri+"/stats/")
    return resp.text

@app.route('/bundles/', methods=['GET', 'POST'])
def sendBundle():
    bundleDirPath = "Blur-1.0.ofx.bundle" #sample dir path

    prefix = "client_bundle_"
    uid = str(uuid.uuid4())[:8]

    completeFileName = prefix + uid + ".tar.gz"
    tar = tarfile.open(completeFileName, "w")

    for root, dirs, files in os.walk(bundleDirPath):
        for file in files:
            tar.add(os.path.join(root, file))

    headers = {
        'content-type': 'application/x-gzip'
    }
    archive = {completeFileName: open(completeFileName, 'r')}
    resp = requests.post(analyzeRootUri+"/analyzeBundle/", data=open(completeFileName, 'r'), headers=headers)

    os.remove(completeFileName)
    return resp.text


if __name__ == "__main__":
    app.run(host=configParser.get("APP_CLIENT", "host"), port=configParser.getint("APP_CLIENT", "port"), debug=True)