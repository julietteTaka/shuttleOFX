

class Plugin:
    def __init__(self, pluginId, bundleId):
        self.pluginId = pluginId
        self.bundleId = bundleId
        self.name = None
        self.shortName = None
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
        self.properties = []
        self.clip = []
        self.uri= None
        self.rawIdentifier = None

    def setDescription(self, description):
        self.description = description

    def addPluginDetails(self, details):
        self.details = details

    def updateRating(self, val):
        self.rate += val

    def addSampleImages(sefl, paths):
        for path in paths :
            self.sampleImagesPath.append(path)

    def printBundle():
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
