import requests
from flask import Blueprint
from flask_restful import Api, reqparse, Resource
from blueprints.face.resources import FaceDetector
import datetime

bp_music = Blueprint('music', __name__)
api = Api(bp_music)


class MusicSpotify(Resource):
    spo_oauth = 'BQAe9Pka9yG6XS2EQJs_8vartMC6J8SR78WMx8SY5-HcYG4i63n4tUt3R4jxj_bupPbK7DQmfHg5yjjLt0S4vubEKaCn6afPoJcl9xHuZ_UVHbxQBR7hpQdzMvIvtI-5TLyUkXRDj6MzfABu81dEBWoyA2PxytJelO4C89M-QGRBEEUrKkKz3_svtyCPa3cViY-U6trjxIZSvj-zVY4fOWiJp2FNBXn1QVtkxEICP5xQG_lADv_K9F_zH36ywaZuBxsVYZQHooikHoVoq9L6BM91VE55yQ'
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