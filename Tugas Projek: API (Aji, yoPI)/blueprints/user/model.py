from blueprints import db
from flask_restful import fields
from sqlalchemy import func
from sqlalchemy.sql.expression import text
from datetime import datetime

from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref

class Users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=True)
    sex = db.Column(db.String(50), nullable=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'))

    response_fields ={
        'id': fields.Integer,
        'name': fields.String,
        'age': fields.Integer,
        'sex': fields.String,
        'client_id': fields.Integer
    }

    def __init__(self, name, age, sex):
        self.name = name
        self.age = age
        self.sex = sex
        self.client_id = client_id

    def __repr__(self):
        return '<Client %r>'% self.id