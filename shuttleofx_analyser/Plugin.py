from pyTuttle import tuttle
import logging

propTypeToPythonType = {
    tuttle.ePropTypeDouble: float,
    tuttle.ePropTypeInt: int,
    tuttle.ePropTypeNone: None,
    tuttle.ePropTypePointer: str,
    tuttle.ePropTypeString: str,
}

class Plugin(object):
    def __init__(self, pluginToAnalyse):
        self.rawIdentifier = None
        self.name = None
        self.version = {}
        self.clips = []
        self.parameters = []
        self.properties = []
        self.initFromPlugin(pluginToAnalyse)

    def getDictOfProperty(self, prop):

        pythonType = propTypeToPythonType[prop.getType()]
        
        # Convert SWIG binding list in python
        valuesCPP = prop.getValues()
        values = []
        if prop.getType() != tuttle.ePropTypePointer and prop.getType() != tuttle.ePropTypeNone:
            values = [valuesCPP[i] for i in range(valuesCPP.size())]

        value = values[0] if values else None

        return {
            "name": prop.getName(),
            "readOnly": prop.getPluginReadOnly(),
            "type": prop.getType(),
            "modifiedBy": prop.getModifiedBy(),
            "value": value,  # TODO: rename propValue
            "propValues": values,
        }

    def getDictOfProperties(self, props):
        properties = []
        for p in props:
            properties.append(self.getDictOfProperty(p))
        return properties

    def initFromPlugin(self, pluginToAnalyse):
        logging.info('Analysing plugin for ' + str(pluginToAnalyse.getRawIdentifier()))

        self.uri = "/plugins/" + str(pluginToAnalyse.getIdentifier())
        self.rawIdentifier = str(pluginToAnalyse.getIdentifier())
        self.version = {
            'major': pluginToAnalyse.getVersionMajor(),
            'minor': pluginToAnalyse.getVersionMinor()
        }
        
        try:
            node = tuttle.createNode(pluginToAnalyse.getIdentifier())
        except Exception as e:
            logging.error("Error in node creation: " + str(e))
            return (self.__dict__)

        # plugin properties
        self.properties = self.getDictOfProperties(node.getProperties())

        # list all properties on parameters of the node
        params = []
        for parameters in node.getParamSet().getParams():
            params.append(self.getDictOfProperties(parameters.getProperties()))
        self.parameters = params

        # list all properties on Clips
        clips = []
        for clip in node.getClipImageSet().getClips():
            clips.append(self.getDictOfProperties(clip.getProperties()))
        self.clips = clips
