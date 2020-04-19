import requests
from flask import Blueprint
from flask_restful import Api, reqparse, Resource

bp_music = Blueprint('music', __name__)
api = Api(bp_music)


class MusicSpotify(Resource):
    spo_oauth = 'BQARKonULVnee2iqnIduDt67I0Bht-7NDqNizh4hYBRfUbns-27j4mdyaPJR9QgAo87VZ2aJvribuVVy4OLccCxvrXGoQnGbHZ7DrxKYiD1ZVGKeC3ZSXe_8hTV866bEjHJAsTtNGZERjx2VHGAfPlLNXlrbFhHzx-2ACbtm5JY8RijEVc8qg-P1mXQ7AWvVQItKE3BhyufjFMTlCNrhAvmcuk7TN96F3w0z-NscJgux1PFmY-WErXoaPj6DhNxSoAcz4GK7uBtHpn02mdgGZxyofUhQtg'
    spo_host = 'https://api.spotify.com/v1/search'

    payload = {}
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': 'Bearer %s' % (spo_oauth)
    }

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('q', location='args', default=None)
        parser.add_argument('type', location='args', default=None)
        parser.add_argument('limit', location='args', default=None)
        args = parser.parse_args()

        rq = requests.get(self.spo_host, params={"q": args['q'], "type": args['type'], "limit": args['limit']}, headers=self.headers, data=self.payload)
        result = rq.json()
        name = result['playlists']['items'][0]['name']
        link = result['playlists']['items'][0]['external_urls']['spotify']
        output = {'name': name, 'link': link}

        return output, 200

api.add_resource(MusicSpotify, '')