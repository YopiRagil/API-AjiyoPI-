from blueprints import db
from flask_restful import fields
from sqlalchemy import func
from sqlalchemy.sql.expression import text

from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref

class Clients(db.Model):
    __tablename__ = "clients"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    client_key = db.Column(db.String(30), unique=True, nullable=False)
    client_secret = db.Column(db.String(255), nullable=True)
    status = db.Column(db.Integer, nullable=True, default=0)
    salt = db.Column(db.String(255))
    users = db.relationship('Users', backref='clients', lazy=True, uselist=False)

    response_fields ={
        'id': fields.Integer,
        'client_key': fields.String,
        'client_secret': fields.String,
        'status': fields.Integer
    }

    jwt_claims_fields ={
        'id': fields.Integer,
        'client_key': fields.String,
        'status': fields.Integer
    }

    def __init__(self, client_key, hash, status, salt):
        self.client_key = client_key
        self.client_secret = hash
        self.status = status
        self.salt = salt

    def __repr__(self):
        return '<Client %r>'% self.id