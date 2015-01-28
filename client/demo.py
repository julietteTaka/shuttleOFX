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
current_render = ""
_id = 0



@app.route('/demo')
@app.route('/demo/<pluginId>', methods=['GET'])
def displayIndex(pluginId = None):

    if pluginId == None:
        pluginId = "tuttle.colorwheel"

    # json_data= open('server/plugin.json')
    # data = json.load(json_data)
    # json_data.close()
    # return render_template('demo.html', plugin=data)

    resp = requests.get(analyzeRootUri+"/plugins/"+pluginId)
    return render_template('demo.html', plugin=resp.json())



@app.route('/resource/<resourceName>', methods=['GET'])
def resource(resourceName):
    resp = requests.get(renderRootUri + "/render/" + current_render['render']['id'] + "/resources/" + resourceName )
    return Response(resp.content, mimetype="image/png", content_type='image/png')


@app.route('/render', methods=['POST'])
def render():
    global current_render

    data = request.data

    # print data

    headers = {
        'Content-Type': 'application/json; charset=utf-8',
        'Accept-Encoding': 'gzip, deflate'
    }

    req = requests.post(renderRootUri + "/render", data=data, headers=headers)
    current_render = req.json()
    # print req.text
    return jsonify(**req.json())



# @app.route('/render/<int:renderId>/resources/<resourceId>', methods=['GET'])
# def getRenderResource(renderId, resourceId):
#     req = requests.get(renderRootUri+"/render/"+str(renderId)+"/resources/"+resourceId)
#     return Response(req.content, mimetype="image/jpeg")


# @app.route('/resource/<path:path>', methods=['GET'])
# def resource(path):
#   return app.send_static_file('resources/' + path)

