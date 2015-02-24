

class Bundle:
    def __init__(self, bundleId, name):
        self.bundleId = bundleId
        self.name = name
        self.description = ""

    def setDescription(self, description):
        self.description = description

    def printBundle():
        print "Bundle :"
        print "bundleId:", self.bundleId
        print "name:", self.name
        print "description:", self.description
