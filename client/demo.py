from flask import Flask, request, jsonify
from flask import render_template, jsonify, json

import ConfigParser
import requests

from client import app

def get_resource_as_string(name, charset='utf-8'):
    with app.open_resource(name) as f:
        return f.read().decode(charset)

app.jinja_env.globals['get_resource_as_string'] = get_resource_as_string

configParser =  ConfigParser.RawConfigParser()
configParser.read('client/configuration.conf')
version = "0.0.1"

analyzeRootUri = configParser.get("APP_CLIENT", "analyzeRootUri")


@app.route('/demo')
def getDemos(pluginId = "tuttle.convolution"):
    resp = requests.get(analyzeRootUri+"/demo/"+pluginId)
    return render_template('demo.html', plugin=resp.json())


@app.route('/demo/<pluginId>', methods=['GET'])
def getDemo(pluginId):
    resp = requests.get(analyzeRootUri+"/demo/"+pluginId)
    return render_template('demo.html', plugin=resp.json())