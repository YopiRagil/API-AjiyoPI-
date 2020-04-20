#app.py
from flask import Flask, request
import json, config, os
from flask_migrate import Migrate, MigrateCommand
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_jwt_extended import JWTManager, verify_jwt_in_request, get_jwt_claims
from datetime import timedelta
from functools import wraps

app = Flask(__name__)
# app.config['APP_DEBUG'] = True

# app.config['JWT_SECRET_KEY'] = 'apaajaboleh'
# app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)

jwt = JWTManager(app)
def internal_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if claims['status'] == False:
            return {'status':'FORBIDEN', 'message':'Internal Only!'}, 403
        else:
            return fn(*args, **kwargs)
    return wrapper

if os.environ.get('FLASK_NEW', 'Production') == "Production":
    app.config.from_object(config.ProductionConfig)
else:
    app.config.from_object(config.DevelopmentConfig)

db = SQLAlchemy (app)
migrate = Migrate (app, db)
manager = Manager (app)
manager.add_command('db', MigrateCommand)

@app.after_request
def after_request(response):
    try:
        requestData = request.get_json()
    except Exception as e:
        requestData = request.args.to_dict()
    if response.status_code == 200:
        app.logger.warning("REQUEST_LOG\t%s",
            json.dumps({
                'method' : request.method,
                'code' : response.status,
                'url' :request.full_path,
                'request':requestData,
                'response':json.loads(response.data.decode('utf-8'))
            })
        )
    else:
        app.logger.error("REQUEST_LOG\t%s",
            json.dumps({
                'method': request.method,
                'code': response.status,
                'uri': request.full_path,
                'request': requestData,
                'response': json.loads(response.data.decode('utf-8'))
            })
        )
    return response

from blueprints.face.resources import bp_face
from blueprints.music.resources import bp_music
from blueprints.client.resources import bp_client
from blueprints.user.resources import bp_user
from blueprints.auth import bp_auth

app.register_blueprint(bp_face, url_prefix='/face')
app.register_blueprint(bp_music, url_prefix='/music')
app.register_blueprint(bp_client, url_prefix='/client')
app.register_blueprint(bp_user, url_prefix='/user')
app.register_blueprint(bp_auth, url_prefix='/auth')

db.create_all()