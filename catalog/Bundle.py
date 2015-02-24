

class Bundle:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.description = ""

    def setDescription(self, description):
        self.description = description

    def printBundle():
        print "Bundle :"
        print "id:", self.id
        print "name:", self.name
        print "description:", self.description
