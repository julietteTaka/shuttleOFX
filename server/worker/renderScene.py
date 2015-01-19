from pyTuttle import tuttle
import logging
import time


class RenderScene:
    def __init__(self):
        self.nodes = []
        self.tuttleGraph = tuttle.Graph()
        self.globalOfxPluginPath = "/home/juliette/Programmation_compilation/webOpenOFX/TuttleOFX/install/" #install path ?
        self.graph = None


    def setPluginPaths(self, ofxPluginPath):

        tuttle.core().getPluginCache().addDirectoryToPath(self.globalOfxPluginPath)
        tuttle.core().getPluginCache().addDirectoryToPath(ofxPluginPath)
        pluginCache = tuttle.core().getPluginCache()
        tuttle.core().preload()


    def loadGraph(self, graphToLoad, outputFilename):
        pythonType =  None
        self.graph = graphToLoad
        try:
            for node in graphToLoad['scene']['nodes']:
                tuttleNode =  self.tuttleGraph.createNode(str(node['plugin']))
                for parameter in node['parameters']:
                    param = tuttleNode.getParam(str(parameter["id"]))

                    if type(parameter["value"]) == unicode:
                        parameter["value"] = str(parameter["value"])

                    param.setValue( parameter["value"])
                self.nodes.append(tuttleNode)

            for connection in graphToLoad['scene']['connections']:
                 self.tuttleGraph.connect( [ self.nodes[connection['src']['id']],  self.nodes[connection['dst']['id']]] )

            outputFilenameParameter = self.nodes[len(self.nodes)-1].getParam("filename")
            outputFilenameParameter.setValue( outputFilename )

        except Exception as e:
            logging.error("error in the graph " + str(e))

    def computeGraph(self):
        try:
            self.graph["startDate"] = time.time()
            self.tuttleGraph.compute(self.nodes[len(self.nodes)-1] )
        except Exception as e:
                logging.error("Error in render: " + str(e))