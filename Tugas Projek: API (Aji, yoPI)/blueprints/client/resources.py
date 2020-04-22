import json
from flask import Blueprint
from flask_restful import Api, reqparse, Resource, marshal
from .model import Client
from . import *
from blueprints import db, app, internal_required
from sqlalchemy import desc
import hashlib, uuid

bp_client = Blueprint('client', __name__)
api = Api(bp_client)

class ClientResource(Resource):

    # @internal_required
    def get(self, id):
        qry = Client.query.get(id)
        if qry is not None:
            return marshal(qry, Client.response_fields), 200, {
                'Content-Type': 'application/json'}
        return {'status': 'NOT_FOUND'}, 404

    # @internal_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('client_key', location='json', required=True)
        parser.add_argument('client_secret', location='json', required=True)
        parser.add_argument('status', location='json', type = bool)
        
        data = parser.parse_args()
        
        salt = uuid.uuid4().hex
        encode = ('%s%s' % (data['client_secret'], salt)).encode('utf-8')
        hash_pass = hashlib.sha512(encode).hexdigest()
        
        client = Client(data['client_key'], hash_pass, data['status'], salt)
        db.session.add(client)
        db.session.commit()
        
        app.logger.debug('DEBUG :%s', client)
                
        return marshal(client, Client.response_fields), 200,  {'Content-Type': 'application/json'}

    # @internal_required
    def put(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('client_key', location='json', required=True)
        parser.add_argument('client_secret', location='json', required=True)
        parser.add_argument('status', location='json')
        parser.add_argument('salt', location='json')
        
        data = parser.parse_args()
        qry = Client.query.get(id)
        if qry is None:
            return {'status': 'NOT_FOUND'}, 404
        
        salt = uuid.uuid4().hex
        encode = ('%s%s' % (data['client_secret'], salt)).encode('utf-8')
        hash_pass = hashlib.sha512(encode).hexdigest()
        
        qry.client_key = data['client_key']
        qry.client_secret = hash_pass
        qry.status = data['status']
        qry.salt = salt
        db.session.commit()
        
        return marshal(qry, Client.response_fields), 200
    
    # @internal_required
    def delete(self, id):
        qry = Client.query.get(id)
        if qry is None:
            return {'status': 'NOT_FOUND'}, 404
        
        db.session.delete(qry)
        db.session.commit() 
        



class ClientList(Resource):
    
    def __init__(self):
        pass
    
    # @internal_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=25)
        parser.add_argument('client_key', location='args', help='invalid status', type=str)
        parser.add_argument('orderby', location='args', help='invalid orderby value', choices=('client_key', 'status'))
        parser.add_argument('sort', location='args', help='invalid sort value', choices=('desc', 'asc'))
        parser.add_argument('status', location='args', choices=('true', 'false', 'True', 'False'))

        args = parser.parse_args()
        
        offset = (args['p'] * args['rp'] - args['rp'])
        qry = Client.query
        
        if args['client_key'] is not None:
            qry = qry.filter_by(client_key=args['client_key'])
        
        if args['orderby'] is not None:
            if args ['orderby'] == 'client_key':
                if args['sort'] == 'desc':
                    qry = qry.order_by(desc(Client.client_key))
                else:
                    qry = qry.order_by(Client.client_key)
                    
        rows = []
        for row in qry.limit(args['rp']).offset(offset).all():
            rows.append(marshal(row, Client.response_fields))
            
        return rows, 200
 ###Routes
api.add_resource(ClientList, '', '/list')
api.add_resource(ClientResource, '', '/<id>')