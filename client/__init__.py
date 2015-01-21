from flask import Flask
app = Flask(__name__)

import client.plugins
import client.upload
