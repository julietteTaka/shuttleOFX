from pyTuttle import tuttle
import logging
import json

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

def getPluginProperties(plugin):
  logging.info('Analyzing plugin for ' + plugin.getRawIdentifier())

  pluginProperties = {
    'id': plugin.getIdentifier(),
    'uri': "/plugins/"+ plugin.getIdentifier(),
    'version': {
      'major': plugin.getVersionMajor(),
      'minor': plugin.getVersionMinor()
    },
    'tags': [],
    'bundleID': "",
    'thumbnailPath': "",
    'iconPath': "",
    'lastAccess': 0,
    'rate': 0,
    'presets': [],
    'defaultImagePaths': [""],
    'sampleImagePaths': [""],
  }


  try:
    node = tuttle.createNode(plugin.getIdentifier())
  except Exception as e:
    logging.error("Error in node creation: " + str(e))
    return pluginProperties

  # plugin properties
  pluginProperties["properties"] = getDictOfProperties(node.getProperties())

  # list all properties on parameters of the node
  params = []
  for parameters in node.getParamSet().getParams():
    params.append(getDictOfProperties(parameters.getProperties()))
  pluginProperties["parameters"] = params

  # list all properties on Clips
  clips = []
  for clip in node.getClipImageSet().getClips():
      clips.append(getDictOfProperties(clip.getProperties()))
  pluginProperties["clips"] = clips

  return pluginProperties