# from app import db
from flask_restful import fields
from sqlalchemy.sql import func
from datetime import datetime
from blueprints import db
from sqlalchemy.sql.expression import text
from blueprints.client.model import Client
from sqlalchemy import Integer, ForeignKey, String, Column


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    client_id = db.Column(db.Integer, ForeignKey(Client.id), unique=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    age = db.Column(db.Integer, nullable=True, default=20)
    sex = db.Column(db.String(10), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())
    # deleted_at = db.Column(db.DateTime, server_default=text('0'))
    
    
    response_fields = {
        'id' : fields.Integer,
        'name' : fields.String,
        'age' : fields.Integer,
        'sex' : fields.String,
        'client_id' : fields.Integer
    }
    
    def __init__(self, name, age, sex, client_id):
        self.name = name
        self.age = age
        self.sex =sex
        self.client_id = client_id
        
        
    def __repr__(self):
        return '<User %s>' % self.id