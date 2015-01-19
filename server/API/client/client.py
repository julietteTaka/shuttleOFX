from flask import Flask, request, abort, send_file, render_template, jsonify, json
import ConfigParser, requests

app = Flask(__name__)

configParser =  ConfigParser.RawConfigParser()
configParser.read('client/configuration.conf')
version = "0.0.1"

analyzeRootUri = configParser.get("APP_CLIENT", "analyzeRootUri")

@app.route('/')
def displayIndex():
    return render_template('form.html')

@app.route('/plugins/', methods=['GET', 'POST'])
def getPlugins():
    resp = requests.get(analyzeRootUri+"/plugins/")
    return resp.text

if __name__ == "__main__":
    app.run(host=configParser.get("APP_CLIENT", "host"), port=configParser.getint("APP_CLIENT", "port"), debug=True)