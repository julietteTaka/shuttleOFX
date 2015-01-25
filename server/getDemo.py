#!/usr/bin/python
from flask import Flask, jsonify
import ConfigParser, requests, json


app = Flask(__name__, static_folder='', static_url_path='')

configParser =  ConfigParser.RawConfigParser()
configParser.read('configuration.conf')

version = "0.0.1"



@app.route('/demo/<string:pluginId>', methods=['GET'])
def getDemo(pluginId):
    json_data= open('plugin.json')
    data = json.load(json_data)
    json_data.close()
    return jsonify(**data)



if __name__ == '__main__':
    app.run(host=configParser.get("APP_PLUGIN", "host"), port=configParser.getint("APP_PLUGIN", "port"), debug=True)



