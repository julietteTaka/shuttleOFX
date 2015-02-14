#!/usr/bin/python
from flask import Flask, jsonify,request, abort
from pyTuttle import tuttle
from server import analyzePlugin, plugin
import logging, uuid, ConfigParser, requests, tarfile, os, multiprocessing, tempfile, shutil, os
from multiprocessing import Process
from logging.handlers import RotatingFileHandler

from server import app

configParser =  ConfigParser.RawConfigParser()
configParser.read('server/configuration.conf')

# print os.getcwd()

handler = RotatingFileHandler('/tmp/analyzer.log', backupCount=1)
handler.setLevel(logging.DEBUG)
app.logger.addHandler(handler)

plugins = ()

def analyzeFromPath(bundlePath, queue):
    global plugins

    customOfxPluginPath = bundlePath
    pluginCache = tuttle.core().getPluginCache()

    pluginCache.addDirectoryToPath(customOfxPluginPath)
    tuttle.core().preload(False)

    plugins = pluginCache.getPlugins()

    pluginsDescription = getPlugins()

    pluginCache.clearPaths()
    plugins = ()

    queue.put(pluginsDescription)


@app.route('/analyzeBundle/', methods=['POST'])
def analyzeBundle():
    bundleBin = request.data

    uid = str(uuid.uuid1())
    tempFilePath = "server/tmp/" + uid + ".tar.gz"

    f = open(tempFilePath, 'w')
    f.write(bundleBin)
    f.close()

    if tarfile.is_tarfile(tempFilePath):
        tar = tarfile.open(tempFilePath, "r")
        tar.extractall("server/tmp/" + uid)

        result_queue = multiprocessing.Queue()

        process = Process(target=analyzeFromPath, args=("server/tmp/" + uid, result_queue))
        process.start()
        analyzedBundle = result_queue.get()
        process.join()

        tar.close()
    else:
        app.logger.error(tempFilePath + " doesn't exists")
        abort(404)

    os.remove(tempFilePath)
    shutil.rmtree("server/tmp/" + uid)

    return analyzedBundle


@app.route('/plugins/', methods=['GET'])
def getPlugins():
    globalOfxPluginPath = configParser.get("OFX_PATH", "globalOfxPluginPath")

    customOfxPluginPath = globalOfxPluginPath

    pluginCache = tuttle.core().getPluginCache()

    pluginCache.addDirectoryToPath(customOfxPluginPath)
    tuttle.core().preload(False)

    plugins = pluginCache.getPlugins()

    pluginsDescription = {'plugins':[], 'total': 0}
    for plugin in plugins:
        pluginsDescription['plugins'].append(analyzePlugin.getPluginProperties(plugin))

    headers = {
        'content-type': 'application/json'
    }
    return jsonify(**pluginsDescription)


@app.route('/plugins/<string:pluginId>', methods=['GET'])
def getPlugin(pluginId):
    globalOfxPluginPath = configParser.get("OFX_PATH", "globalOfxPluginPath")

    customOfxPluginPath = globalOfxPluginPath
    
    pluginCache = tuttle.core().getPluginCache()

    pluginCache.addDirectoryToPath(customOfxPluginPath)
    tuttle.core().preload(False)


    plugin = pluginCache.getPluginById(str(pluginId))
    pluginDescription = analyzePlugin.getPluginProperties(plugin)
    return jsonify(**pluginDescription)



def getPlugins():
    global plugins

    pluginsDescription = {'plugins':[], 'total': len(plugins)}

    for plugin in plugins:
        pluginsDescription['plugins'].append(analyzePlugin.getPluginProperties(plugin))

    headers = {
        'content-type': 'application/json',
        'mimetype': 'application/json'
    }

    plugins = ()
    return jsonify(**pluginsDescription)