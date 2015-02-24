import uuid
from datetime import datetime

from flask import Flask
import psycopg2

from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID, ARRAY, JSON
from sqlalchemy.schema import ForeignKey 


app = Flask(__name__)

# ADD
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://webopenfx:tuttle@localhost:5432/webopenfx_db"

db = SQLAlchemy(app)


class User(db.Model):
#class Bundle(object):
    '''
    This the representation of a User.
    '''

    __tablename__ = 'user'
    '''
    Representation of a User in the DB
    '''
    idU = db.Column(db.Integer, autoincrement = True, primary_key = True)
    name = db.Column(db.String, nullable = False)
    firstname = db.Column(db.String, nullable = False)
    mail = db.Column(db.String, nullable = False)
    company = db.Column(ARRAY(db.String), nullable = False)
    #bundle = db.Column(ARRAY(db.Integer), nullable = False)
    bundle = db.Column(db.Integer, db.ForeignKey('bundle.idB'),nullable = False)

    def __init__(self):
        '''
        Constructor for a User
        '''
        super(Bundle, self).__init__()
        

db.create_all()
