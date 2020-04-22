from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal

from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, get_jwt_claims
from ..client.model import Client
import hashlib, uuid
from blueprints import internal_required

bp_auth = Blueprint('auth', __name__)
api = Api (bp_auth)

class CreateTokenResource(Resource):
    
    def get(self):
        ##create token
        parser = reqparse.RequestParser()
        parser.add_argument('client_key', location='args', required=True)
        parser.add_argument('client_secret', location='args', required=True)
        args = parser.parse_args()
        
        qry = Client.query.filter_by(client_key=args['client_key']).first()
        encode = ('%s%s' % (args['client_secret'], qry.salt)).encode('utf-8')
        hash_pass = hashlib.sha512(encode).hexdigest()
        if qry.client_secret == hash_pass:
            qry = marshal(qry, Client.jwt_calims_fields)
            token = create_access_token(identity=args['client_key'], user_claims=qry)
            return {'token':token}, 200

        else:
            return {'status': 'PASWORD SALAH BOSS'}, 404

    @jwt_required
    def post(self):
        claims = get_jwt_claims()
        return {'claims': claims}, 200
    
class RefreshTokenResource(Resource):
    @jwt_required
    @internal_required
    def post(self):
        current_user = get_jwt_identity()
        token = create_access_token(identity = current_user)
        return {'token':token}, 200

api.add_resource(CreateTokenResource, '')
api.add_resource(RefreshTokenResource,'/refresh')