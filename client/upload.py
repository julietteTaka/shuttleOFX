from flask import (
    Flask,
    abort,
    request,
    render_template,
    send_from_directory,
    redirect,
    url_for,
    jsonify
)
from werkzeug import secure_filename
import os

basedir = os.path.abspath(os.path.dirname(__file__))



# app = Flask(__name__)


from client import app



UPLOAD_FOLDER = 'upload/'

app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp4', 'avi'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']



@app.route('/upload')
def upld():
    return render_template('upload.html', uploaded=None)


# @app.route('/uploaded')
# def uplded():
#     return render_template('configureUpload.html')


@app.route('/upload', methods=['POST'])
def upldfile():
    if request.method == 'POST':

        print basedir

        saved_files_urls = []
        for f in request.files.getlist('file[]'):
            if f and allowed_file(f.filename):
                filename = secure_filename(f.filename)

                print f

                updir = os.path.join(basedir, UPLOAD_FOLDER)
                f.save(os.path.join(updir, filename))
                file_size = os.path.getsize(os.path.join(updir, filename))
                saved_files_urls.append(url_for('uploaded_file', filename=filename))
        #return jsonify(name=filename, size=file_size)

    return render_template('upload.html', uploaded="true")




@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)






