import requests
from flask import Blueprint
from flask_restful import Api, reqparse, Resource
from blueprints.face.resources import FaceDetector
import datetime

bp_music = Blueprint('music', __name__)
api = Api(bp_music)


class MusicSpotify(Resource):
    spo_oauth = 'BQA84iijblSwQ-zhA_1I70ToqrSGeShbXm1b137EQ6fWYa1z1DX99JP49bm_Dpt-s0g9gU9y3IeRYv74QVnxnrmrrehGLQdzw0YBP_85OkqRiz3vXD0obFDqcrTULof1VpEGk2ecj55sTNWGj3wMw3u1IE9UUyuJpDMSI-THgRCn74eHXV549J8UEwBmLEMKzx5ndJARr1Drwf_fdFWGpcshl7WGARVDijG-2aYJE7mBpns1lFziTUp5XE_2OvTpINnZG7p2ZSrE59X6N1-iPqfYN4Ynajyojw'
    spo_host = 'https://api.spotify.com/v1/search'

    payload = {}
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': 'Bearer %s' % (spo_oauth)
    }

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