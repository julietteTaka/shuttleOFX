
import os
import json
import requests
from functools import wraps
from flask import (
    request,
    jsonify,
    render_template,
    abort,
    Response,
    redirect,
    url_for,
    session
)

from shuttleofx_client import g_app, google, catalogRootUri, renderRootUri

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not 'google_token' in session:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

@g_app.route('/')
def index():
    if 'google_token' in session:
        user = google.get('userinfo').data
        return render_template("index.html", user=user)
    return render_template("index.html")

@g_app.route('/plugin')
def getPlugins():
    user = None
    if 'google_token' in session:
        user = google.get('userinfo').data
    try:
        resp = requests.get(catalogRootUri+"/plugin", params=request.args)
    except:
        return render_template('plugins.html', dico=None, user=user)

    return render_template('plugins.html', dico=resp.json(), user=user)

@g_app.route("/plugin/search")
def searchPlugins():
    req = requests.get(catalogRootUri+"/plugin", params=request.args)
    if req.status_code != 200:
        abort(req.status_code)
    return jsonify(**req.json())

@g_app.route("/plugin/count")
def countPlugins():
    req = requests.get(catalogRootUri+"/plugin", params=request.args)
    if req.status_code != 200:
        abort(req.status_code)
    return jsonify(**req.json())


@g_app.route('/plugin/<pluginId>')
def getPlugin(pluginId):
    user = None
    if 'google_token' in session:
        user = google.get('userinfo').data
    resp = requests.get(catalogRootUri+"/plugin/"+pluginId)
    return render_template('plugin.html', plugin=resp.json(), user=user)

@g_app.route('/plugin/<pluginId>/image/<imageId>')
def getSampleImagesForPlugin(pluginId, imageId):
    req = requests.get(catalogRootUri + "/resources/" + str(imageId) + "/data")
    return Response(req.content, mimetype=req.headers["content-type"])

@g_app.route('/editor')
@g_app.route('/editor/<pluginId>')
def renderPageWithPlugin(pluginId = 0):
    user = None
    if 'google_token' in session:
        user = google.get('userinfo').data
    resp = requests.get(catalogRootUri+"/plugin/"+pluginId)
    previewGallery = requests.get(renderRootUri + '/resource/').json()
    return render_template('editor.html', plugin=resp.json(), user=user, resources=previewGallery)

@g_app.route('/render', methods=['POST'])
def render():
    headers = {
        'Content-Type': 'application/json; charset=utf-8',
        'Accept-Encoding': 'gzip, deflate'
    }
    req = requests.post(renderRootUri + "/render", data=request.data, headers=headers)
    return jsonify(**req.json())

@g_app.route('/render/<int:renderId>', methods=['GET'])
def getRenderStatus(renderId):
    req = requests.get(renderRootUri+"/render/"+str(renderId))
    return jsonify(**req.json())

@g_app.route('/render/<renderId>/resource/<resourceId>', methods=['GET'])
def getRenderResource(renderId, resourceId):
    req = requests.get(renderRootUri+"/render/"+str(renderId)+"/resource/"+resourceId)
    return Response(req.content, mimetype="image/jpeg")


@g_app.route('/resource/<resourceId>', methods=['GET'])
def getResourceById(resourceId):
    req = requests.get(renderRootUri+"/resource/"+resourceId)
    return Response(req.content, mimetype="image/png")

@g_app.route('/resource', methods=['GET'])
def getResources() :
    req = requests.get(renderRootUri + '/resource/')
    if req.status_code != 200:
        abort(req.status_code)
    return jsonify(**req.json())

@g_app.route('/upload')
@login_required
def upload():
    if 'google_token' in session:
        user = google.get('userinfo')
        return render_template("upload.html", user=user.data, uploaded= None)
    return redirect(url_for('login'))

@g_app.route('/bundle')
def getBundles() :
    req = requests.get(catalogRootUri + '/bundle', headers=request.headers)
    if req.status_code != 200:
        abort(req.status_code)
    return jsonify(**req.json())

@g_app.route('/bundle', methods=['POST'])
def newBundle() :
    header = {'content-type' : 'application/json'}
    req = requests.post(catalogRootUri + '/bundle', data=json.dumps(request.form), headers=header)
    if req.status_code != 200:
        abort(req.status_code)
    return jsonify(**req.json())

@g_app.route('/bundle/<bundleId>/archive', methods=['POST'])
def uploadArchive(bundleId):
    filename = request.files['file'].filename
    file = request.files['file']

    file.save("/tmp/" + filename)
    multiple_files = [('file', (filename, open("/tmp/" + filename, 'rb'), 'application/gzip'))]

    req = requests.post(catalogRootUri + '/bundle/' + bundleId + '/archive', files = multiple_files)
    if req.status_code != 200:
        abort(req.status_code)
    os.remove("/tmp/" + filename)
    return jsonify(**req.json())

@g_app.route('/bundle/<bundleId>/analyse', methods=['POST'])
def analyseBundle(bundleId):
    req = requests.post(catalogRootUri + '/bundle/' + bundleId + '/analyse', data=request.data, headers=request.headers)
    if req.status_code != 200:
        abort(req.status_code)
    return req.json()

@g_app.route('/login')
def login():
    return google.authorize(callback=url_for('authorized', _external=True))


@g_app.route('/logout')
def logout():
    session.pop('google_token', None)
    redirectTarget = None
    for target in request.values.get('next'), request.referrer:
        if target != None:
            redirectTarget = target
    return redirect( redirectTarget )


@g_app.route('/login/authorized')
def authorized():
    resp = google.authorized_response()
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )

    session['google_token'] = (resp['access_token'], '')
    user = google.get('userinfo')

    redirectTarget = None
    for target in request.values.get('next'), request.referrer:
        if target != None:
            redirectTarget = target
    return redirect( redirectTarget )


@g_app.route("/plugin/<int:pluginId>/resource", methods=['POST'])
def addPluginResource(pluginId):
    filename = request.files['file'].filename
    file = request.files['file']
    file.save("/tmp/" + filename)

    multiple_files = [('file', (filename, open("/tmp/"+filename, 'rb'), 'application/gzip'))]

    req = requests.post(catalogRootUri + "/resources", files = multiple_files)

    return jsonify(**req.json())

@g_app.route("/plugin/<int:pluginId>/images", methods=['POST'])
def addImageToPlugin(pluginId):
    req = requests.post(catalogRootUri + "/plugin/" + str(pluginId) + "/images", data=request.data, headers=request.headers)
    return jsonify(**req.json())

@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')

