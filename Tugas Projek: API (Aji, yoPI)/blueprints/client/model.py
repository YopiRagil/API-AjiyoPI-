# from app import db
from flask_restful import fields
from sqlalchemy.sql import func
from datetime import datetime
from blueprints import db
from sqlalchemy.sql.expression import text

class Client(db.Model):
    __tablename__ = "client"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    client_key = db.Column(db.String(30), unique=True, nullable=False)
    client_secret = db.Column(db.String(1000))
    status = db.Column(db.Integer, default=0)
    salt = db.Column(db.String(255))
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())
    # deleted_at = db.Column(db.DateTime, server_default=text('0'))
    
    response_fields = {
        'id' : fields.Integer,
        'client_key' : fields.String,
        'client_secret' : fields.String,
        'status' : fields.Boolean(),
        'salt' : fields.String
    }
    
    jwt_calims_fields = {
        'id' : fields.Integer,
        'client_key' : fields.String,
        'status' : fields.Boolean,
        'salt' : fields.String
    }
    
    def __init__(self, client_key, client_secret, status, salt):
        self.client_key = client_key
        self.client_secret = client_secret
        self.status =status
        self.salt = salt
        
        
    def __repr__(self):
        return '<Client %s>' % self.id