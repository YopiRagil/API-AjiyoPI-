import json
from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from blueprints import db
from sqlalchemy import desc
import hashlib, uuid
from blueprints import internal_required

from .model import Users

bp_user = Blueprint('user', __name__)
api = Api(bp_user)


class UsersResource(Resource):
    
    def get(self, id=None):
        qry = Users.query.get(id)

        if qry is not None:
            return marshal(qry, Users.response_fields), 200, {'Content-Type': 'application/json'}
        return {'status': 'NOT_FOUND'}, 404, {'Content-Type': 'application/json'}

    def post(self):
        parser = reqparse.RequestParser()
        # parser.add_argument('id', location='json', type=int, required=True)
        parser.add_argument('name', location='json', required=True)
        parser.add_argument('age', location='json', type=int)
        parser.add_argument('sex', location='json')
        args = parser.parse_args()

        result = Users(args['name'], args['age'], args['sex'])

        db.session.add(result)
        db.session.commit()

        return marshal(result, Users.response_fields), 200, {'Content-Type': 'application/json'}

    def put(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('id', location='json', type=int, required=True)
        parser.add_argument('name', location='json', required=True)
        parser.add_argument('age', location='json', type=int)
        parser.add_argument('sex', location='json')
        args = parser.parse_args()

        qry = Users.query.get(id)
        if qry is None:
            return {'status': 'NOT_FOUND'}, 404, {'Content-Type': 'application/json'}

        qry.name = args['name']
        qry.age = args['age']
        qry.sex = args['sex']
        db.session.commit()

        return marshal(qry, Users.response_fields), 200, {'Content-Type': 'application/json'}
        
    def delete(self, id):
        qry = Users.query.get(id)
        if qry is None:
            return {'status': 'NOT_FOUND'}, 404, {'Content-Type': 'application/json'}

        db.session.delete(qry)
        db.session.commit()
        return {"status": "Deleted"}, 200, {'Content-Type': 'application/json'}


class UserList(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=25)
        parser.add_argument('orderby', location='args', help='invalid status', choices=(
            'name',
            'age',
            'sex'
        ))
        parser.add_argument('sort', location='args', help='invalid status', choices=('asc', 'desc'))
        
        args = parser.parse_args()

        offset = (args['p'] * args['rp']) - args['rp']

        qry = Users.query

        if args['orderby'] is not None:
            if args['orderby'] == 'name':
                if args['sort'] == 'desc':
                    qry = qry.order_by(desc(Users.name))
                else:
                    qry = qry.order_by(Users.name)
            elif args['orderby'] == 'age':
                if args['sort'] == 'desc':
                    qry = qry.order_by(desc(Users.age))
                else:
                    qry = qry.order_by(Users.age)
            elif args['orderby'] == 'sex':
                if args['sort'] == 'desc':
                    qry = qry.order_by(desc(Users.sex))
                else:
                    qry = qry.order_by(Users.sex)

        rows = []
        for row in qry.limit(args['rp']).offset(offset).all():
            rows.append(marshal(row, Users.response_fields))

        return rows, 200, {'Content-Type': 'application/json'}

api.add_resource(UserList, '', '/list')
api.add_resource(UsersResource, '', '/<id>')