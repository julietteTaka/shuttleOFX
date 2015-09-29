#!/usr/bin/python

import ConfigParser

from flask_oauthlib.client import OAuth

import os
import json
import requests
from functools import wraps
from flask import (
    Flask,
    request,
    jsonify,
    render_template,
    abort,
    Response,
    redirect,
    url_for,
    session
)
import logging

config =  ConfigParser.ConfigParser()
config.read('/etc/shuttleofx/client.cfg')

g_app = Flask(__name__)

g_app.config['GOOGLE_ID'] = config.get('OAUTH_CONFIG', 'googleId')
g_app.config['GOOGLE_SECRET'] = config.get('OAUTH_CONFIG', 'googleSecret')
g_app.debug = True
g_app.secret_key = 'development'

oauth = OAuth(g_app)

google = oauth.remote_app(
    'google',
    consumer_key=g_app.config.get('GOOGLE_ID'),
    consumer_secret=g_app.config.get('GOOGLE_SECRET'),
    request_token_params={
        'scope': 'https://www.googleapis.com/auth/userinfo.profile'
    },
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
)

def get_resource_as_string(name, charset='utf-8'):
    with g_app.open_resource(name) as f:
        return f.read().decode(charset)

g_app.jinja_env.globals['get_resource_as_string'] = get_resource_as_string

catalogRootUri = config.get("APP_CLIENT", "catalogRootUri")
renderRootUri  = config.get("APP_CLIENT", "renderRootUri")

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


@g_app.route("/plugin/search/")
def searchPlugins():
    user = None
    if 'google_token' in session:
        user = google.get('userinfo').data

    resp = requests.get(catalogRootUri+"/plugin", params=request.args)

    return render_template('plugins.html', dico=resp.json(), user=user)


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
    if resp.status_code != 200:
        abort(resp.status_code)
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
    resp = requests.get(catalogRootUri+"/plugin/"+str(pluginId))
    if resp.status_code != 200:
        abort(resp.status_code)
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
        return render_template("upload.html", user=user.data, uploaded=None)
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
    logging.warning('login start')
    res = google.authorize(callback=url_for('authorized', _external=True))
    logging.warning('login end')
    return res


@g_app.route('/logout')
def logout():
    session.pop('google_token', None)
    redirectTarget = request.values.get('next') or request.referrer
    return redirect( redirectTarget )


@g_app.route('/login/authorized')
def authorized():
    logging.warning('login/authorized start')
    resp = google.authorized_response()
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )

    session['google_token'] = (resp['access_token'], '')
    # user = google.get('userinfo')

    aa = {(k, v) for (k, v) in request.args.iteritems()}
    logging.warning('login/authorized request.args:', str(aa))

    redirectTarget = request.values.get('next') or request.referrer or url_for('getPlugins')
    if redirectTarget == None:
        logging.warning('login/authorized redirectTarget is None')

    logging.warning('login/authorized before redirect')
    res = redirect( redirectTarget )
    logging.warning('login/authorized end')
    return res


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

if __name__ == '__main__':
    g_app.run(host="0.0.0.0",port=5000,debug=True)