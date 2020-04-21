import json
from flask import Blueprint, Flask, request, Blueprint
from flask_restful import Api, reqparse, Resource, marshal
from .model import User
from . import *
from blueprints import db, app, internal_required
from sqlalchemy import desc
import hashlib, uuid


bp_user = Blueprint('user', __name__)
api = Api(bp_user)

class UserResource(Resource):
    
    @internal_required
    def get(self, id):
        qry = User.query.get(id)
        if qry is not None:
            return marshal(qry, User.response_fields), 200, {
                'Content-Type': 'application/json'}
        return {'status': 'NOT_FOUND'}, 404

    @internal_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', location='json', required=True)
        parser.add_argument('age', location='json', type=int, required=True)
        parser.add_argument('sex', location='json')
        parser.add_argument('client_id', location='json', type=int, required=True)
        args = parser.parse_args()
        user = User(args['name'], args['age'], args['sex'], args['client_id'])
        try:
            db.session.add(user)
            db.session.commit()
            
            
            return marshal (user, User.response_fields), 200,  {'Content-Type': 'application/json'}
        except Exception as e:
            print (e)

    @internal_required
    def put(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('id', location='json', type=int, required=True)
        parser.add_argument('name', location='json', required=True)
        parser.add_argument('age', location='json', type=int, required=True)
        parser.add_argument('sex', location='json')
        parser.add_argument('client_id', location='json', type=int, required=True)
        
        args = parser.parse_args()
        qry = User.query.get(id)
        if qry is None:
            return {'status': 'NOT_FOUND'}, 404
        
        qry.name = args['name']
        qry.age = args['age']
        qry.sex = args['sex']
        qry.client_id = args['client_id']
        db.session.commit()
        
        return marshal(qry, User.response_fields), 200
        
    @internal_required
    def delete(self, id):
        qry = User.query.get(id)
        if qry is None:
            return {'status': 'NOT_FOUND'}, 404
        
        db.session.delete(qry)
        db.session.commit() 
        

class UserList(Resource):
    
    def __init__(self):
        pass
    
    @internal_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=25)
        parser.add_argument('sex', location='args', help='invalid status', choices=('male', 'female'))
        parser.add_argument('age', location='args', help='invalid status', type=int)
        parser.add_argument('client_id', location='args', help='invalid status', type=int)
        parser.add_argument('orderby', location='args', help='invalid orderby value', choices=('age', 'client_id'))
        parser.add_argument('sort', location='args', help='invalid sort value', choices=('desc', 'asc'))

        args = parser.parse_args()
        
        offset = (args['p'] * args['rp'] - args['rp'])
        qry = User.query
    
        if args['sex'] is not None:
            qry = qry.filter_by(sex=args['sex'])
        
        if args['orderby'] is not None:
            if args ['orderby'] == 'age':
                if args['sort'] == 'desc':
                    qry = qry.order_by(desc(User.age))
                else:
                    qry = qry.order_by(User.age)
            elif args ['orderby'] =='client_id':
                if args['sort'] == 'desc':
                    qry = qry.order_by(desc(User.sex))
                else:
                    qry = qry.order_by(User.sex)
                    
        rows = []
        for row in qry.limit(args['rp']).offset(offset).all():
            rows.append(marshal(row, User.response_fields))
            
        return rows, 200
 ###Routes
api.add_resource(UserList, '', '/list')
api.add_resource(UserResource, '', '/<id>')