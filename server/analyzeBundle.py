#!/usr/bin/python
from flask import Flask, jsonify,request, abort
from pyTuttle import tuttle
from ofxPlugins import analyze
import logging, uuid, ConfigParser, requests, tarfile, os, multiprocessing, tempfile, shutil
from multiprocessing import Process
from logging.handlers import RotatingFileHandler

app = Flask(__name__, static_folder='', static_url_path='')
configParser =  ConfigParser.RawConfigParser()
configParser.read('ofxPlugins/configuration.conf')

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
    tempFilePath = "tmp/" + uid + ".tar.gz"

    f = open(tempFilePath, 'w')
    f.write(bundleBin)
    f.close()

    if tarfile.is_tarfile(tempFilePath):
        tar = tarfile.open(tempFilePath, "r")
        tar.extractall("tmp/" + uid)

        result_queue = multiprocessing.Queue()

        process = Process(target=analyzeFromPath, args=("tmp/" + uid, result_queue))
        process.start()
        analyzedBundle = result_queue.get()
        process.join()

        tar.close()
    else:
        app.logger.error(tempFilePath + " doesn't exists")
        abort(404)

    os.remove(tempFilePath)
    shutil.rmtree("tmp/" + uid)

    return analyzedBundle


def getPlugins():
    global plugins

    pluginsDescription = {'plugins':[], 'total': len(plugins)}

    for plugin in plugins:
        pluginsDescription['plugins'].append(analyze.getPluginProperties(plugin))

    headers = {
        'content-type': 'application/json',
        'mimetype': 'application/json'
    }

    plugins = ()
    return jsonify(**pluginsDescription)


if __name__ == '__main__':
    app.run(host=configParser.get("APP_PLUGIN", "host"), port=configParser.getint("APP_PLUGIN", "port"), debug=True)
    handler = RotatingFileHandler('/tmp/analyzer.log', backupCount=1)
    handler.setLevel(logging.DEBUG)
    app.logger.addHandler(handler)