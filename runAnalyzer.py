#!/usr/bin/python
from server import app
import ConfigParser

configParser =  ConfigParser.RawConfigParser()
configParser.read('server/configuration.conf')

app.run(host=configParser.get("APP_ANALYZER", "host"), port=configParser.getint("APP_ANALYZER", "port"), debug=True)
