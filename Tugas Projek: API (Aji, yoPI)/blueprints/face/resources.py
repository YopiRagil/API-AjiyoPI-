from flask import Blueprint
from flask_restful import Api, reqparse, Resource
from flask_jwt_extended import jwt_required
from blueprints import app, internal_required
import requests, os
from werkzeug.datastructures import FileStorage


bp_face = Blueprint('face', __name__)
api = Api(bp_face)
class FaceDetector(Resource):
    url = app.config['FACE']
    key = app.config['KEY_FACE']

    @internal_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('picture', type=FileStorage, location='files', required=True)        
        args = parser.parse_args()
        header = {'Apikey': self.key}
        payload = {}        
        res = requests.post(self.url, headers=header, data = payload, files = [('imageFile', args['picture'])]).json()    
        val= res['PeopleWithAge'][0]['Age']
        return int(val)
api.add_resource(FaceDetector, '')