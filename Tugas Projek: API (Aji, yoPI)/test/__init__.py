#pytest --cov-report html --cov=blueprints test/  ==>utk run test
import pytest
import json
import logging
from flask import Flask, request, json
from blueprints import app, db
from app import cache
from blueprints.user.model import User
from blueprints.client.model import Client
import uuid, hashlib

def call_client(request):
    client = app.test_client()
    return client

@pytest.fixture 
def client(request):
    return call_client(request)

@pytest.fixture
def init_database():
    db.drop_all()
    db.create_all()
    
    salt = uuid.uuid4().hex
    encode = ('%s%s' % ('password', salt)).encode('utf-8')
    hash_pass = hashlib.sha512(encode).hexdigest()
    
    client = Client(client_key="yopi", client_secret=hash_pass, status=1, salt=salt)
    clientnonInternal = Client(client_key="ragil", client_secret=hash_pass, status=0, salt=salt)
    db.session.add(client)
    db.session.add(clientnonInternal)
    db.session.commit()

    user=User(client_id=1, name="Little Joni", age=23, sex="male")
    db.session.add(user)
    db.session.commit()

    yield db
    db.drop_all()
        
def create_token():
    ## prepare request
    token = cache.get('test-token')
    if token is None:    
        data={
            'client_key':'yopi',
            'client_secret':'password',
        }
        #do request
        req = call_client(request)
        res = req.get('/auth', query_string=data)
        
        res_json =json.loads(res.data)
        logging.warning('RESULT:%s', res_json)
        
        assert res.status_code == 200
        
        cache.set('test-token', res_json['token'], timeout=60)
        
        return res_json ['token']
    
    else:
        return token
        
def create_token_nonin():
    ## prepare request
    token = cache.get('test-token-nonin')
    if token is None:    
        data={
            'client_key':'ragil',
            'client_secret':'password',
        }

        req = call_client(request)
        res = req.get('/auth', query_string=data)

        
        res_json =json.loads(res.data)
        logging.warning('RESULT:%s', res_json)
        
        assert res.status_code == 200
        
        cache.set('test-token-nonin', res_json['token'], timeout=60)
        
        return res_json ['token']
    
    else:
        return token
    

    

