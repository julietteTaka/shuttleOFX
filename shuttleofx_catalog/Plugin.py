

class Plugin(object):
    def __init__(self, pluginId, bundleId):
        self.pluginId = pluginId
        self.bundleId = bundleId
        self.label = ""
        self.shortLabel = ""
        self.description = ""
        self.shortDescription = ""
        self.version = [0, 0]
        self.details = None
        self.tags = []
        self.presets = None
        self.rate = 0
        self.defautImagePath = None
        self.sampleImagesPath = []
        self.parameters = []
        self.properties = {}
        self.clip = []
        self.rawIdentifier = None
        self.comments.user = ""
        self.comments.content = ""

    def setDescription(self, description):
        self.description = description

    def addPluginDetails(self, details):
        self.details = details

    def setRating(self, val):
        self.rate = val

    def getRating(self):
        return self.rate

    def addSampleImages(self, paths):
        if isinstance(paths, str):
            self.sampleImagesPath.append(paths)

        if isinstance(paths, list):
            for path in paths:
                self.sampleImagesPath.append(path)

    def getPropValueFromKeys(self, keys, default=None):
        """
        Return a non empty value with multiple fallback keys.
        """
        for key in keys:
            if key in self.properties:
                value = self.properties[key]['value']
                if value:
                    return value
        return default

    def printBundle(self):
        print "Plugin :"
        print "pluginId:", self.pluginId
        print "bundleId:", self.bundleId
        print "description:", self.description
        print "shortDescription:", self.shortDescription
        print "version:", self.version
        print "details:", self.details
        print "tags:", self.tags
        print "presets:", self.presets
        print "rate:", self.rate
        print "defautImagePath:", self.defautImagePath
        print "sampleImagesPath:", self.sampleImagesPath
        print "comments", self.comments
