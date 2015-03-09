from pyTuttle import tuttle
import logging
import time
import ConfigParser

configParser =  ConfigParser.RawConfigParser()
configParser.read('render.cfg')

globalOfxPluginPath = configParser.get("OFX_PATH", "globalOfxPluginPath")


class ProgressHandle(tuttle.IProgressHandle):
    def __init__(self, renderSharedInfo):
        super(ProgressHandle, self).__init__()
        self.renderSharedInfo = renderSharedInfo

    def beginSequence(self):
        """Called before the beginning of the process
        """

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

def configLocalPluginPath(ofxPluginPath):
    tuttle.core().getPluginCache().addDirectoryToPath(ofxPluginPath)
    pluginCache = tuttle.core().getPluginCache()
    tuttle.core().preload(False)

def loadGraph(scene, outputFilename):
    tuttleGraph = tuttle.Graph()
    status = 1
    try:
        nodes = []
        for node in scene['nodes']:
            tuttleNode = tuttleGraph.createNode(str(node['plugin']))
            for parameter in node['parameters']:
                param = tuttleNode.getParam(str(parameter["id"]))

                if type(parameter["value"]) == unicode:
                    parameter["value"] = str(parameter["value"])

                param.setValue(parameter["value"])
            nodes.append(tuttleNode)

        for connection in scene['connections']:
            # TODO: replace src/dst with from/to.
            tuttleGraph.connect([
                nodes[connection['src']['id']],
                nodes[connection['dst']['id']],
                ])

        # TODO: what is the right way to retrieve the output node.
        outputNode = nodes[-1]
        # TODO:
        # if outputNode.getProperties().getProperty("OfxPropContextWriter").getValue():
        outputFilenameParameter = outputNode.getParam("filename")
        outputFilenameParameter.setValue( outputFilename )

        return tuttleGraph

    except Exception as e:
        logging.error("error in the graph " + str(e))


def computeGraph(renderSharedInfo, newRender, outputFilename):
    try:
        renderSharedInfo['startDate'] = time.time()

        #TODO set the right plugin path
        configLocalPluginPath(globalOfxPluginPath)

        renderSharedInfo['status'] = 1
        tuttleGraph = loadGraph(newRender['scene'], outputFilename)

        cOptions = newRender['scene']['options'];
        renderSharedInfo['status'] = 2

        computeOptions = tuttle.ComputeOptions()
        
        for option in cOptions:

            if "TimeRange" in option['id']:
                begin = option['values']['begin']
                end = option['values']['end']
                step = option['values']['step']
                computeOptions.setTimeRange(begin, end, step)

            if "RenderScale" in option['id']:
                x = option['values']['x']
                y = option['values']['y']
                computeOptions.setRenderScale(x, y)

        ## Create handle and set it in ComputeOptions
        progressHandle = ProgressHandle(renderSharedInfo)
        computeOptions.setProgressHandle(progressHandle)

        tuttleGraph.compute(computeOptions)

        renderSharedInfo['status'] = 3

    except Exception as e:
        renderSharedInfo['status'] = -1
        logging.error("Error in render: " + str(e))
