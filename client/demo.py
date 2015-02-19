from flask import Flask, request, render_template, json, jsonify
from flask import abort, send_file, Response

import ConfigParser, json, requests, uuid, os


from client import app


def get_resource_as_string(name, charset='utf-8'):
    with app.open_resource(name) as f:
        return f.read().decode(charset)

app.jinja_env.globals['get_resource_as_string'] = get_resource_as_string

configParser =  ConfigParser.RawConfigParser()
configParser.read('client/configuration.conf')
version = "0.0.1"

analyzeRootUri = configParser.get("APP_CLIENT", "analyzeRootUri")
renderRootUri = configParser.get("APP_CLIENT", "renderRootUri")

# @app.route('/demo')

@app.route('/demo/<pluginId>')
def displayIndex(pluginId):

    # json_data= open('server/plugin.json')
    # data = json.load(json_data)
    # json_data.close()
    # return render_template('demo.html', plugin=data)

    resp = requests.get(analyzeRootUri+"/plugins/"+pluginId)
    return render_template('demo.html', plugin=resp.json())

@app.route('/render', methods=['POST'])
def render():
    headers = {
        'Content-Type': 'application/json; charset=utf-8',
        'Accept-Encoding': 'gzip, deflate'
    }
    req = requests.post(renderRootUri + "/render", data=request.data, headers=headers)
    return jsonify(**req.json())


@app.route('/render/<int:renderId>', methods=['GET'])
def getRenderStatus(renderId):
    req = requests.get(renderRootUri+"/render/"+str(renderId))
    return jsonify(**req.json())


@app.route('/render/<int:renderId>/resources/<resourceId>', methods=['GET'])
def getRenderResource(renderId, resourceId):
    req = requests.get(renderRootUri+"/render/"+str(renderId)+"/resources/"+resourceId)
    return Response(req.content, mimetype="image/jpeg")


@app.route('/resource/<path:path>', methods=['GET'])
def resource(path):
  return app.send_static_file('resources/' + path)

