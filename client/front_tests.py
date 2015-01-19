from flask import Flask
from flask import render_template



# app = Flask(__name__)


from client import app


def get_resource_as_string(name, charset='utf-8'):
    with app.open_resource(name) as f:
        return f.read().decode(charset)

app.jinja_env.globals['get_resource_as_string'] = get_resource_as_string


dico = {
    # clef:valeur
    "plugins" : [
        {
            "id" : "colorwheel",
            "name" : "Color Wheel",
            "version" : "2.0",
            "author" : "Armand Biteau",
            "parameters" : [
                {
                    "id" : "MinColor",
                    "name" : "Min Color",
                    "type" : "int"
                },
                 {
                    "id" : "MaxColor",
                    "name" : "Max Color",
                    "type" : "int"

                }

            ]
        },
        {
            "id" : "crop",
            "name" : "Image croper",
            "version" : "3.2",
            "author" : "Hugo Garrido",
            "parameters" : [
                {
                    "id" : "wid",
                    "name" : "Width",
                    "type" : "int"

                },
                 {
                    "id" : "hei",
                    "name" : "Height",
                    "type" : "int"

                }

            ]
        },
        {
            "id" : "opacity",
            "name" : "Opacity",
            "version" : "1.2",
            "author" : "Juliette Belin",
            "parameters" : [
                {
                    "id" : "intensity",
                    "name" : "Intensity",
                    "type" : "int"

                },
                 {
                    "id" : "imgIn",
                    "name" : "Image In",
                    "type" : "int"
                    
                }

            ]
        },
        {
            "id" : "text",
            "name" : "Text decorator",
            "version" : "1.2",
            "author" : "Armand Biteau",
            "parameters" : [
                {
                    "id" : "wid",
                    "name" : "Width",
                    "type" : "int"

                },
                 {
                    "id" : "hei",
                    "name" : "Height",
                    "type" : "int"

                }

            ]
        },
        {
            "id" : "rgba",
            "name" : "Convert to rgba",
            "version" : "1.4",
            "author" : "Armand Biteau",
            "parameters" : [
                {
                    "id" : "wid",
                    "name" : "Width",
                    "type" : "int"

                },
                 {
                    "id" : "hei",
                    "name" : "Height",
                    "type" : "int"

                }

            ]
        },
        {
            "id" : "rgb",
            "name" : "Convert to rgb",
            "version" : "3.8.1",
            "author" : "Armand Biteau",
            "parameters" : [
                {
                    "id" : "wid",
                    "name" : "Width",
                    "type" : "int"

                },
                 {
                    "id" : "hei",
                    "name" : "Height",
                    "type" : "int"

                }

            ]
        }
    ]
}

@app.route('/plugins')
def getPlugins(pluginName=None):
    return render_template('plugins.html', dico=dico)


@app.route('/plugins/<pluginName>')
def Plugin(pluginName=None):
    newdico = dict(dico)
    newdico["currentPlugin"] = pluginName
    return render_template('plugin.html', dico=newdico)




