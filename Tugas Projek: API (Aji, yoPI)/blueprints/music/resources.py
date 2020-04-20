import requests
from flask import Blueprint
from flask_restful import Api, reqparse, Resource
from blueprints.face.resources import FaceDetector
import datetime
from blueprints import internal_required

bp_music = Blueprint('music', __name__)
api = Api(bp_music)


class MusicSpotify(Resource):
    spo_oauth = 'BQCloWs4ZCHY6tdZZbpx8RcyDmuas6btW5MLtmv4B5ccEutryCywrwI0kT3c2_oBd7tveuG-9SP_TfEEnW6o1oNj4JD0MRUu7WbFMmD_CrpO0AVqHA_Gk2xNp4PRDNQVqHV4l1wz5MIx5fAdQ1V1Aq-5g6eBWmCzO34m-2C8nZzJmZTMiN-ZsSQHjzGs6LiSB5chDZ7euafOnAa6dMLjYnMY6bzcivsKoNhTegB4iAugYDSq7aBAZFDeIQTvkWAlE6c0yk3Xfi6DblevzCcpZtP4hfquRg'
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
        parser.add_argument('type', location='args', default=None)
        args = parser.parse_args()

        rq = requests.get(self.spo_host, params={"q": str(years)+" hits", "type": args['type'], "limit": 1}, headers=self.headers, data=self.payload)
        result = rq.json()
        name = result['playlists']['items'][0]['name']
        link = result['playlists']['items'][0]['external_urls']['spotify']
        output = {'name': name, 'link': link}

        return output, 200

api.add_resource(MusicSpotify, '')