from flask import Flask, request
from flask_restful import Resource, Api

import models

# Register resources
# from resources.messages import messages_api
from resources.articles import articles_api
from resources.users import users_api

from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token, get_jwt_identity, get_raw_jwt)

app = Flask(__name__)

# access token
app.config['SECRET_KEY'] = 'randomString_superSecret1928390123'
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

jwt = JWTManager(app)

# app.register_blueprint(messages_api, url_prefix='/api/v2')
app.register_blueprint(articles_api, url_prefix='/api/v2')
app.register_blueprint(users_api, url_prefix='/api/v2')

# logout
blacklist = set()


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return jti in blacklist


@app.route('/api/v2/user/logout')
@jwt_required
def logout():
    jti = get_raw_jwt()['jti']
    blacklist.add(jti)
    return 'logout successs'


if __name__ == '__main__':
    models.initialize()
    app.run(debug=True)
