import requests
from flask import Blueprint
from flask_restful import Api, reqparse, Resource
from blueprints.face.resources import FaceDetector
import datetime
from blueprints import app, internal_required

bp_music = Blueprint('music', __name__)
api = Api(bp_music)

class MusicSpotify(Resource):
    spo_oauth = app.config['KEY_MUSIK']
    spo_host = app.config['MUSIK']
    
    payload = {}
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': 'Bearer %s' % (spo_oauth)
    }

    @internal_required
    def get(self):
        FaceDetector()
        umur = FaceDetector().post()
        years = (datetime.date.today().year)-umur
    
        parser = reqparse.RequestParser()
        parser.add_argument('q', location='args', default=None)
        parser.add_argument('type', location='args', default=None)
        parser.add_argument('limit', location='args', default=None)
        args = parser.parse_args()

        rq = requests.get(self.spo_host, params={"q": years, "type": args['type'], "limit": args['limit']}, headers=self.headers, data=self.payload)
        result = rq.json()
        name = result['playlists']['items'][0]['name']
        link = result['playlists']['items'][0]['external_urls']['spotify']
        output = {'name': name, 'link': link}

        return output, 200

api.add_resource(MusicSpotify, '')

