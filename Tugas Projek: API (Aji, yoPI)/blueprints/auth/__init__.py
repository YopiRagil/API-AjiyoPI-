from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal
import hashlib, uuid
from blueprints import internal_required
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, get_jwt_claims

from ..client.model import Clients

bp_auth = Blueprint('auth', __name__)
api = Api(bp_auth)

class CreateTokenResource(Resource):
    
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('client_key', location='args', required=True)
        parser.add_argument('client_secret', location='args', required=True)
        args = parser.parse_args()

        qry_client = Clients.query.filter_by(client_key=args['client_key']).first()
        
        if qry_client is not None:
            client_salt = qry_client.salt
            encoded = ('%s%s' % (args['client_secret'], client_salt)).encode('utf-8')
            hash_pass = hashlib.sha512(encoded).hexdigest()
            if hash_pass == qry_client.client_secret:
                if args['client_key'] == 'internal' and args['client_secret'] == 'th1s1s1nt3n4lcl13nt':
                    ClientData = marshal(qry_client, Clients.jwt_claims_fields)
                    ClientData['status'] = 'True'
                    token = create_access_token(identity=args['client_key'], user_claims=ClientData)
                    return {'token': token}, 200
                else:
                    ClientData = marshal(qry_client, Clients.jwt_claims_fields)
                    ClientData['status'] = 'False'
                    token = create_access_token(identity=args['client_key'], user_claims=ClientData)
                    return {'token': token}, 200
            else:
                return 'not_found', 404    
        else:
            return 'not_found', 404

    # @jwt_required
    @internal_required
    def post(self):
        claims = get_jwt_claims()
        return {'claims': claims}, 200


class RefreshTokenResource(Resource):
    
    # @jwt_required
    @internal_required
    def post(self):
        current_user = get_jwt_identity()
        claims = get_jwt_claims()
        token = create_access_token(identity=current_user, user_claims=claims)
        return {'token': token}, 200

api.add_resource(CreateTokenResource, '')
api.add_resource(RefreshTokenResource, '/refresh')