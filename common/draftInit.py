import uuid
from datetime import datetime

from flask import Flask
import psycopg2

from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID, ARRAY, JSON

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://webopenfx:tuttle@localhost:5432/webopenfx_db"

db = SQLAlchemy(app)


'''
Note that this is a work in progress version : 
- When there is relations between tables, they need (for know) to be declared in the same file
- I will work on a cleaner strucure once the plugins are recorded in the db
- Also, to make the relations work, we need to have different columns names. Prefixing with the table name isn't enough
'''


class Bundle(db.Model):
    '''
    This the representation of a Bundle.
    '''

    __tablename__ = 'bundle'
    '''
    Representation of a Bundle in the DB
    '''
    idB = db.Column(db.Integer, autoincrement = True, primary_key = True)
    bundleId = db.Column(UUID, nullable = False, unique=True)
    #userId = db.relationship('User', lazy='dynamic', uselist=False )
    # Will change when authentification will be implemented
    userId = db.Column(db.Integer, nullable = False)
    companyId = db.relationship('Company', backref='bundle', lazy='dynamic', uselist=False )
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
    company = db.Column(ARRAY(db.Integer), nullable = False)
    #Will change when identification will be implemented
    bundle = db.Column(ARRAY(db.Integer), nullable = False)
    #bundle = db.Column(db.Integer, db.ForeignKey('bundle.idB'),nullable = False)


class Company(db.Model):
    '''
    This is the representation of a Company
    '''

    __tablename__ = 'company'
    '''
    Representation of a Company in db
    '''
    idC = db.Column(db.Integer, autoincrement = True, primary_key = True)
    name = db.Column(db.String, nullable = False)
    bundle = db.Column(db.Integer, db.ForeignKey('bundle.idB'),nullable = False)


class Plugin(db.Model):

    '''
    This is the representation as an object and as seen from the DB perspective
    '''

    __tablename__ = 'plugin'
    '''
    Representation of a Plugin in the DB
    '''
    idPl = db.Column(db.Integer, primary_key=True)
    # The pluginID isn't generated in the Class but some other instance, hence the primary key type
    bundleId = db.Column(db.String)
    pluginId = db.Column(UUID, unique=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String(250), nullable=False)
    shortDescription = db.Column(db.String(250), nullable=False)
    version = db.Column(db.String(250), nullable=False)
    # These colomn might become Custom Types, until then, we stock it as JSON
    clip = db.Column(JSON)
    parameters = db.Column(JSON, nullable=False)
    properties = db.Column(JSON, nullable=False)
    tags = db.Column(JSON)
    presets = db.Column(JSON)
    rate = db.Column(db.Integer)
    defautImagePath = db.Column(ARRAY(db.String), nullable=False)
    # Can be empty this it is for user's personnal image sample
    sampleImagePath = db.Column(ARRAY(db.String))


class property(db.Model):
    '''
    '''
    __tablename__ = "property"
    idPr = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String)
    paramType = db.Column(db.Integer)
    value = db.Column(ARRAY(db.String))
    readOnly = db.Column(db.Boolean)
    idParameter = db.Column(db.Integer, db.ForeignKey('parameter.idPa'))
    idClip = db.Column(db.Integer, db.ForeignKey('clip.idCl'))

    def __init__(self):
        idProperty = -1
        idClip = -1


class Clip(db.Model):
    '''
    Clip
    '''
    __tablename__ = "clip"
    idCl = db.Column(db.Integer, primary_key = True)
    idProp = db.relationship('Property', backref = 'clip', lazy = 'dynamic', uselist = False)


class Parameter(db.Model):
    '''
    Parameter
    '''
    __tablename__ = "parameter"
    idPa = db.Column(db.Integer, primary_key = True)
    idProp = db.relationship('Property', backref = 'parameter', lazy = 'dynamic', uselist = False)


db.create_all()
