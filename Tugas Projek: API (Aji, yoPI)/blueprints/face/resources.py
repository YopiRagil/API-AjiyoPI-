from flask import Blueprint
from flask_restful import Api, reqparse, Resource
from flask_jwt_extended import jwt_required
from blueprints import app
import requests

bp_face = Blueprint('face', __name__)
api = Api(bp_face)
class FaceDetector(Resource):
    url = "https://api.cloudmersive.com/image/face/detect-age"
    key = '8a0dc979-c5d3-439e-b183-b945a61de2ba'
    file = [('imageFile', open('/home/alta18/Pictures/6-Ajay.png','rb'))]
    def post(self):
        header = {'Apikey': self.key}
        payload = {}
        # file = [(('imageFile', open('/path/to/file','rb')))]
        

        res = requests.request("POST", self.url, headers=header, data = payload, files = self.file).json()
        val= res['PeopleWithAge'][0]['Age']
        return {'age':(int(val))}

api.add_resource(FaceDetector, '')