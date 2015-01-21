#!/usr/bin/python
from client import app
import ConfigParser

configParser =  ConfigParser.RawConfigParser()
configParser.read('client/configuration.conf')

app.run(host=configParser.get("APP_CLIENT", "host"), port=configParser.getint("APP_CLIENT", "port"), debug=True)
