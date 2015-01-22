from flask import Flask, request, abort, send_file, render_template, jsonify, json
import ConfigParser, requests, tarfile, uuid, os

app = Flask(__name__)

configParser =  ConfigParser.RawConfigParser()
configParser.read('client/configuration.conf')
version = "0.0.1"

analyzeRootUri = configParser.get("APP_CLIENT", "analyzeRootUri")
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

@app.route('/demo/')
def displayIndex():
    renderGraph = {"graph":"graph"}
    return render_template('base.html', renderGraph=renderGraph)

@app.route('/plugins/')
def getPlugins():
    resp = requests.get(analyzeRootUri+"/plugins/")
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