
import shuttleofx_analyser
from shuttleofx_render import globalOfxPluginPath, pluginsStorage, catalogRootUri
from pyTuttle import tuttle

import requests
import logging
import json
import time
import os

class ProgressHandle(tuttle.IProgressHandle):
    def __init__(self, renderSharedInfo):
        super(ProgressHandle, self).__init__()
        self.renderSharedInfo = renderSharedInfo

    def beginSequence(self):
        """Called before the beginning of the process
        """
        pass

    def setupAtTime(self):
        """Called when setting up an image
        """
        pass

    def processAtTime(self):
        """Called before processing an image
        """
        self.renderSharedInfo["status"] = 99

    def endSequence(self):
        """Called at the end of the process
        """
        pass

def configLocalPluginPath(ofxPluginPaths):
    tuttle.core().getPluginCache().addDirectoryToPath(globalOfxPluginPath)

    for ofxPluginPath in ofxPluginPaths:
        tuttle.core().getPluginCache().addDirectoryToPath(ofxPluginPath)
    pluginCache = tuttle.core().getPluginCache()
    tuttle.core().preload(False)
    logging.debug('Number of Plugins:' + str(len(pluginCache.getPlugins())))

def loadGraph(scene):
    tuttleGraph = tuttle.Graph()

    nodes = []
    for node in scene['nodes']:
        tuttleNode = tuttleGraph.createNode(str(node['plugin']))
        for parameter in node['parameters']:
            param = tuttleNode.getParam(str(parameter["id"]))

            # Remap unicode to str. TODO: check if it's still needed.
            if isinstance(parameter["value"], unicode):
                parameter["value"] = str(parameter["value"])

            param.setValue(parameter["value"])
        nodes.append(tuttleNode)

    for connection in scene['connections']:
        # TODO: replace src/dst with from/to.
        tuttleGraph.connect([
            nodes[connection['src']['id']],
            nodes[connection['dst']['id']],
            ])
    return tuttleGraph


def computeGraph(renderSharedInfo, newRender):
    try:
        renderSharedInfo['startDate'] = time.time()
        scene = newRender['scene']

        bundleIds = []
        nodes = []
        for node in scene['nodes']:
            if 'plugin' in node:

                resp = requests.get(catalogRootUri+"/bundle/" + node['plugin']+ '/bundle')
                resp = resp.json()
                bundleIds.append(resp['bundleId'])
            else:
                logging.error("Error while searching the plugin "+node['plugin'])

        bundlePaths = [os.path.join(shuttleofx_analyser.tmpRenderingPath, str(bundleId)) for bundleId in bundleIds]
        configLocalPluginPath(bundlePaths)

        renderSharedInfo['status'] = 1
        tuttleGraph = loadGraph(scene)

        renderSharedInfo['status'] = 2
        tuttleComputeOptions = tuttle.ComputeOptions()

        if 'options' in newRender['scene']:
            for option in newRender['scene']['options']:

                if "TimeRange" in option['id']:
                    begin = option['values']['begin']
                    end = option['values']['end']
                    step = option['values']['step']
                    tuttleComputeOptions.setTimeRange(begin, end, step)

                if "RenderScale" in option['id']:
                    x = option['values']['x']
                    y = option['values']['y']
                    tuttleComputeOptions.setRenderScale(x, y)

        ## Create handle and set it in ComputeOptions
        progressHandle = ProgressHandle(renderSharedInfo)
        tuttleComputeOptions.setProgressHandle(progressHandle)

        tuttleGraph.compute(tuttleComputeOptions)

        renderSharedInfo['status'] = 3

    except:
        renderSharedInfo['status'] = -1
        raise
