import json
from . import app, client, cache, create_token, create_token_nonin, init_database


class TestClientCrud():
    def test_client_list_get(self, client, init_database):
        token = create_token()
        res = client.get('/client',
                         headers={'Authorization': 'Bearer ' + token},
                         content_type = 'application/json')
        
        res_json = json.loads(res.data)
        assert res.status_code == 200
        
    def test_client_list_get_params(self, client, init_database):
        token = create_token()
        res = client.get('/client',
                         headers={'Authorization': 'Bearer ' + token},
                         query_string={'status':0},
                         content_type = 'application/json')
        
        res_json = json.loads(res.data)
        assert res.status_code == 200
        
    def test_client_list_get_orderby_status_desc(self, client, init_database):
        token = create_token()
        res = client.get('/client',
                         headers={'Authorization': 'Bearer ' + token},
                         query_string={'client_key':'yopi','orderby':'client_key', 'sort': 'desc'},
                         content_type = 'application/json')
        
        res_json = json.loads(res.data)
        assert res.status_code == 200
        
    def test_client_list_get_orderby_status_asc(self, client, init_database):
        token = create_token()
        res = client.get('/client',
                         headers={'Authorization': 'Bearer ' + token},
                         query_string={'client_key':'yopi','orderby':'client_key', 'sort': 'asc'},
                         content_type = 'application/json')
        
        res_json = json.loads(res.data)
        assert res.status_code == 200    
    
        
    
    def test_client_list_get_nonin(self, client, init_database):
        token = create_token_nonin()
        res = client.get('/client',
                         headers={'Authorization': 'Bearer ' + token},
                         content_type = 'application/json')
        
        res_json = json.loads(res.data)
        assert res.status_code == 403
        
    def test_client_get_byid(self, client, init_database):
        token = create_token()
        res = client.get('/client/1',
                         headers={'Authorization': 'Bearer ' + token},
                         content_type = 'application/json')
        
        res_json = json.loads(res.data)
        assert res.status_code == 200
        
    def test_client_get_byid_fail(self, client, init_database):
        token = create_token()
        res = client.get('/client/3',
                         headers={'Authorization': 'Bearer ' + token},
                         content_type = 'application/json')
        
        res_json = json.loads(res.data)
        assert res.status_code == 404
        
    def test_client_post(self, client, init_database):
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
        assert res.status_code == 200
        
    def test_client_put(self, client, init_database):
        token = create_token()
        data={
            "client_key": "babebo",
            "client_secret": "yes",
            "status": 0
            }
        res = client.put('/client/1',
                        data=json.dumps(data),
                        headers={'Authorization': 'Bearer ' + token},
                        content_type = 'application/json')
        
        res_json = json.loads(res.data)
        assert res.status_code == 200
        
    def test_client_put_fail(self, client, init_database):
        token = create_token()
        data={
            "client_key": "babebo",
            "client_secret": "yes",
            "status": 0
            }
        res = client.put('/client/6',
                        data=json.dumps(data),
                        headers={'Authorization': 'Bearer ' + token},
                        content_type = 'application/json')
        
        res_json = json.loads(res.data)
        assert res.status_code == 404
        
    def test_client_delete_fail(self, client, init_database):
        token = create_token()
        res = client.delete('/client/9',
                         headers={'Authorization': 'Bearer ' + token},
                         content_type = 'application/json')
        
        res_json = json.loads(res.data)
        assert res.status_code == 404
    
    def test_client_delete(self, client, init_database):
        token = create_token()
        res = client.delete('/client/1',
                         headers={'Authorization': 'Bearer ' + token},
                         content_type = 'application/json')
        
        res_json = json.loads(res.data)
        assert res.status_code == 200
        
        
        
        
        

   
        