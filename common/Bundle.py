import uuid
from datetime import datetime

from flask import Flask
import psycopg2

from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID, ARRAY, JSON


app = Flask(__name__)

# ADD
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://webopenfx:tuttle@localhost:5432/webopenfx_db"

db = SQLAlchemy(app)

print "lol"
class Bundle(db.Model):
#class Bundle(object):
    '''
    This the representation of a Bundle.
    '''

    __tablename__ = 'bundle'
    '''
    Representation of a Bundle in the DB
    '''
    idB = db.Column(db.Integer, autoincrement = True, primary_key = True)
    bundleId = db.Column(UUID, nullable = False, unique=True)
    userId = db.relationship('User', backref='bundle', lazy='dynamic', uselist=False )
    companyId = db.relationship('Company', backref='bundle', lazy='dynamic', uselist=False )
    #companyId = db.Column(db.Integer, db.ForeignKey('company.id'))
    name = db.Column(db.String, nullable = False)
    description = db.Column(db.String(250))
    uploadDate = db.Column(db.DateTime, nullable = False)
    shared = db.Column(db.Boolean, nullable = False)
    contributors = db.Column(ARRAY(db.Integer))
    architecture = db.Column(ARRAY(db.String), nullable=False)
    plugins = db.Column(ARRAY(db.String), nullable=False)
    uploaded = db.Column(db.Boolean, nullable=False)

    def __init__(self):
        '''
        Constructor for a Bundle
        '''
        super(Bundle, self).__init__()
        self.bundleId = str(uuid.uuid1())
        self.uploadDate = datetime.now()
        self.shared = False
        self.uploaded = False



class User(db.Model):
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
