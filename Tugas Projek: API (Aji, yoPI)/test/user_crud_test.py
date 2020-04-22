import json
from . import app, client, cache, create_token, create_token_nonin, init_database
       
class TestUserCrud():
    id_user = 0
    def test_user_list(self, client, init_database):
        token = create_token()
        res = client.get(
                        '/user', 
                        headers={'Authorization':'Bearer ' + token}, 
                        content_type='application/json'
                        )
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_user_id_invalid(self, client, init_database):
        token = create_token()
        res = client.get(
                        '/user/10', 
                        headers={'Authorization':'Bearer ' + token}, 
                        content_type='application/json'
                        )
        res_json = json.loads(res.data)
        assert res.status_code == 404

    def test_user_put_fail(self, client, init_database):
        token = create_token()
        data = {
                "name": "Jane",
                "age": 20,
                "sex": "Female",
                "client_id": 2
                }
        res = client.put('/user/', 
                        data=json.dumps(data),
                        headers={'Authorization': 'Bearer ' + token},
                        content_type='application/json'
                        )
        res_json = json.loads(res.data)
        assert res.status_code == 404

    def test_user_put(self, client, init_database):
        token = create_token()
        
        data={
            "client_key": "ajay",
            "client_secret": "ntap",
            "status": 0
            }
        res = client.post('/client',
                        data=json.dumps(data),
                        headers={'Authorization': 'Bearer ' + token},
                        content_type = 'application/json')
        res_json = json.loads(res.data)
        
        
        dataput = {
                "name": "Jane",
                "age": 20,
                "sex": "male",
                "client_id": res_json['id']
                }
        resput = client.put('/user/1', 
                        data=json.dumps(dataput),
                        headers={'Authorization': 'Bearer ' + token},
                        content_type='application/json'
                        )
        res_json = json.loads(resput.data)
        assert res.status_code == 200

    def test_user_post(self, client, init_database):
        token = create_token()
        
        data = {
                "name": "dodi",
                "age": 25,
                "sex": "Male",
                "client_id": 2
                }
        res = client.post(
                        '/user', 
                        json = data,
                        headers={'Authorization': 'Bearer ' + token},
                        content_type='application/json'
                        )
        res_json = json.loads(res.data)
        assert res.status_code == 200
        self.id_user = res_json['id']
        
    def test_user_post_fail(self, client, init_database):
        token = create_token()
        data = {
                "name": "dodi",
                "age": 25,
                "sex": "Male",
                "client_id": 1
                }
        res = client.post(
                        '/user', 
                        json = data,
                        headers={'Authorization': 'Bearer ' + token},
                        content_type='application/json'
                        )
        res_json = json.loads(res.data)
        assert res.status_code == 403

    def test_user_id(self, client, init_database):
        token = create_token()
        res = client.get(
                        '/user/1', 
                        headers={'Authorization':'Bearer ' + token}, 
                        content_type='application/json'
                        )
        res_json = json.loads(res.data)
        assert res.status_code == 200
        
    

    def test_user_delete(self, client, init_database):
        token = create_token()
        res = client.delete('/user/1', 
                            headers={'Authorization':'Bearer ' + token}, 
                            content_type='application/json'
                            )
        res_json = json.loads(res.data)
        assert res.status_code == 200
    
    def test_user_delete_fail(self, client, init_database):
        token = create_token()
        res = client.delete(
                            '/user/10', 
                            headers={'Authorization':'Bearer ' + token}, 
                            content_type='application/json'
                            )
        res_json = json.loads(res.data)
        assert res.status_code == 404

    def test_get_filterby(self, client, init_database):
        token = create_token()
        res = client.get('/user', 
                        query_string={
                                    "orderby": "age",
                                    "sort": "desc"
                                    },
                        headers={'Authorization':'Bearer ' + token}
                        )
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_get_filterby2(self, client, init_database):
        token = create_token()
        res = client.get(
                        '/user', 
                        query_string={
                            "orderby": "client_id",
                            "sort": "desc"
                        },
                        headers={'Authorization':'Bearer ' + token}
                        )
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_get_filterby3(self, client, init_database):
        token = create_token()
        res = client.get('/user', 
                        query_string={
                                    "orderby": "age",
                                    "sort": "asc"
                                    },
                        headers={'Authorization':'Bearer ' + token}
                        )
        res_json = json.loads(res.data)
        assert res.status_code == 200
        
    def test_get_filterby4(self, client, init_database):
        token = create_token()
        res = client.get(
                        '/user', 
                        query_string={
                            "orderby": "client_id",
                            "sort": "asc"
                        },
                        headers={'Authorization':'Bearer ' + token}
                        )
        res_json = json.loads(res.data)
        assert res.status_code == 200
    
    def test_get_filterby5(self, client, init_database):
        token = create_token()
        res = client.get(
                        '/user', 
                        query_string={
                            "sex": "male",
                        },
                        headers={'Authorization':'Bearer ' + token}
                        )
        res_json = json.loads(res.data)
        assert res.status_code == 200
