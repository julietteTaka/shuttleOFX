#!/usr/bin/python
from flask import Flask, jsonify
import ConfigParser, requests, json

from server import app


configParser =  ConfigParser.RawConfigParser()
configParser.read('configuration.conf')

version = "0.0.1"



@app.route('/demo/<string:pluginId>', methods=['GET'])
def getDemo(pluginId):
    json_data= open('server/plugin.json')
    data = json.load(json_data)
    json_data.close()
    return jsonify(**data)




