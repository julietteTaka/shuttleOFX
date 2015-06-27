#!/usr/bin/python

import ConfigParser
from flask import Flask

config =  ConfigParser.RawConfigParser()
config.read( "/etc/shuttleofx/analyser.cfg" )

tmpRenderingPath = config.get('APP_ANALYSER', 'workingTmpDir')

g_app = Flask(__name__)

import shuttleofx_analyser.views
