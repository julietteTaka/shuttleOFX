#!/usr/bin/python
import logging
from flask import Flask, jsonify
from pyTuttle import tuttle
from pluginsModule import runPlugin

app = Flask(__name__, static_folder='', static_url_path='')

version = "0.0.1"

globalOfxPluginPath = "/home/juliette/Programmation_compilation/webOpenOFX/TuttleOFX/install/" #install path ?
tuttle.core().getPluginCache().addDirectoryToPath(globalOfxPluginPath)

tuttle.core().preload(False)
pluginCache = tuttle.core().getPluginCache()
plugins = pluginCache.getPlugins()

@app.route('/', methods=['GET'])
def index():
  index = "<html><head><title>WebOpenFX - Catalog</title></head><body><h1><center>WebOpenFX - Catalog</center></h1><br/><br/><ul><li>version: " + str(version) + "</li></ul></body>"
  return index


@app.route('/plugins', methods=['GET'])
def getPlugins():
  pluginsDescription = {'plugins':[], 'total': len(plugins)}
  for plugin in plugins:
    pluginsDescription['plugins'].append(runPlugin.getPluginProperties(plugin))

  return jsonify(**pluginsDescription)

@app.route('/plugins/<string:pluginId>', methods=['GET'])
def getPlugin(pluginId):
  plugin = pluginCache.getPluginById(str(pluginId))
  pluginDescription = runPlugin.getPluginProperties(plugin)
  return jsonify(**pluginDescription)

if __name__ == '__main__':
  # logging.getLogger().setLevel(10)
  app.run(host='0.0.0.0', port=5010, debug=True)