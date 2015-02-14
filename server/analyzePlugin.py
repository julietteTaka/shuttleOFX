from pyTuttle import tuttle
from server import plugin
from flask import jsonify
import logging
import json
import uuid

# logging.basicConfig(filename='/tmp/analyze.log',level=logging.DEBUG)

class pointer:
    def __init__(self, p):
        self.p = p

propTypeToPythonType = {
    tuttle.ePropTypeDouble: float,
    tuttle.ePropTypeInt: int,
    tuttle.ePropTypeNone: None,
    tuttle.ePropTypePointer: str,
    tuttle.ePropTypeString: str,
}

def getDictOfProperty(prop):

    pythonType = propTypeToPythonType[prop.getType()]

    return {
        "name": prop.getName(),
        "readOnly": prop.getPluginReadOnly(),
        "type": prop.getType(),
        "modifiedBy": prop.getModifiedBy(),
        "value": [pythonType(v) for v in prop.getStringValue().split(', ')]
    }

def getDictOfProperties(props):
    properties = []
    for p in props:
        properties.append(getDictOfProperty(p))
    return properties

def getPluginProperties(pluginToAnalyse):
    logging.info('Analyzing plugin for ' + str(pluginToAnalyse.getRawIdentifier()))
    pluginObject = plugin.Plugin()

    pluginObject.id = str(uuid.uuid1())
    pluginObject.uri = "/plugins/" + str(pluginToAnalyse.getIdentifier())
    pluginObject.rawIdentifier = str(pluginToAnalyse.getIdentifier())
    pluginObject.version = {
        'major': pluginToAnalyse.getVersionMajor(),
        'minor': pluginToAnalyse.getVersionMinor()
    }
    
    try:
        node = tuttle.createNode(pluginToAnalyse.getIdentifier())
    except Exception as e:
        logging.error("Error in node creation: " + str(e))
        return (pluginObject.__dict__)

    # plugin properties
    pluginObject.properties = getDictOfProperties(node.getProperties())

    # list all properties on parameters of the node
    params = []
    for parameters in node.getParamSet().getParams():
        params.append(getDictOfProperties(parameters.getProperties()))
    pluginObject.parameters = params

    # list all properties on Clips
    clips = []
    for clip in node.getClipImageSet().getClips():
        clips.append(getDictOfProperties(clip.getProperties()))
    pluginObject.clips = clips
    
    return (pluginObject.__dict__)

