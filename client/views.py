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


from client import app




@app.route('/')
@app.route('/index')
# @login_required
def index():
    return render_template('index.html')



