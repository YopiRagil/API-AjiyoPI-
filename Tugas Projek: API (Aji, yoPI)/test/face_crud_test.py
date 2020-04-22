import json
from . import app, client, cache, create_token, init_database
from unittest import mock
from unittest.mock import patch
import requests, os, io
from io import BytesIO, StringIO

class TestFaceCrud():

    def mocked_requests_post(*args, **kwargs):
        class MockResponse:
            def __init__(self, json_data, status_code):
                self.json_data = json_data
                self.status_code = status_code
            
            def json(self):
                return self.json_data

        if len(args) > 0:
            if args[0] == app.config['MUSIK']:
                return MockResponse(
                                    {
                                        "Successful": true,
                                        "PeopleWithAge": [
                                            {
                                            "FaceLocation": 
                                                    {
                                                    "LeftX": 7,
                                                    "TopY": 20,
                                                    "RightX": 165,
                                                    "BottomY": 179
                                                    },
                                            "AgeClassificationConfidence": 0.9,
                                            "AgeClass": "25-32",
                                            "Age": 25.089151382446289
                                            }
                                        ],
                                        "PeopleIdentified": 1
                                    }
                                    , 200)

        else:
            return MockResponse(None, 404)
        
    @mock.patch('requests.post', side_effect=mocked_requests_post)
    def test_check_face(self, post_mock, client):
        token = create_token()
        dirname = '/home/alta18/Pictures/'
        file_path = os.path.join(os.path.dirname(__file__), '/home/alta18/Pictures','rb')
        with open('/home/alta18/Pictures/3-Me.png', 'rb') as picture: 
            sIO = BytesIO(picture.read())
        data = {"picture": (sIO, "/home/alta18/Pictures/3-Me.png")}

        res = client.post('/face', 
                        data = data,
                        headers={'Authorization': 'Bearer ' + token}, 
                        # files =data['picture'],
                        content_type='multipart/form-data')
        
        # res = client.post('/face', 
        #                     headers={'Authorization': 'Bearer ' + token},
        #                     data = payload, 
        #                     files = [('imageFile', open('/home/alta18/Pictures/3-Me.png','rb'))],
        #                     content_type='multipart/form-data'
        #                 )

        
        res_json = json.loads(res.data)
        assert res.status_code == 200
        






# res = client.post('/face', 
#             headers={'Apikey': self.key}, 
#             data = payload, 
#             files = [('imageFile', open('/home/alta18/Pictures/3-Alul.png','rb'))])


# file_path = os.path.join(os.path.dirname(__file__), 'test_emailbulk.csv')

#     print(file_path)

#     with open(file_path, 'rb') as log:
#         sIO = BytesIO(log.read())

#     data = {
#         'bulkemail': (sIO, "test_emailbulk.csv"),
#         'description': 'BULK DESCRIPTION',
#         'job_name': 'BULK TEST'
#             }

#     content_type='multipart/form-data'

