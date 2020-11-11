from flask import jsonify, Blueprint, abort
from flask_restful import Api, Resource, fields, marshal, marshal_with, reqparse
from hashlib import md5
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token, get_jwt_identity)

import models

user_fields = {
    'email': fields.String,
    'access_token': fields.String
}


class UserBase(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'email',
            required=True,
            help='input is empty',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'password',
            required=True,
            help='input is empty',
            location=['form', 'json']
        )
        super().__init__()


class UserList(UserBase):

    def post(self):

        # Get input
        args = self.reqparse.parse_args()

        email = args.get('email')
        password = args.get('password')
        try:
            models.User.select().where(models.User.email == email).get()
        except models.User.DoesNotExist:
            user = models.User.create(
                email=email,
                password=md5(password.encode('utf-8')).hexdigest()
            )

            # Send Token
            access_token = create_access_token(identity=email)
            user.access_token = access_token
            return marshal(user, user_fields)
        else:
            raise Exception('email exist')

    @jwt_required
    def get(self):
        return {'message': 'protection'}


class User(UserBase):

    def post(self):
        # Get input
        args = self.reqparse.parse_args()

        email = args.get('email')
        password = args.get('password')
        try:
            hashPass = md5(password.encode('utf-8')).hexdigest()
            user = models.User.get(
                (models.User.email == email) & (models.User.password == hashPass))
        except models.User.DoesNotExist:
            return {'messages': 'user or password is wrong!'}
        else:
            access_token = create_access_token(identity=email)
            return {'messages': 'signin success', 'access_token': access_token}


# Register
users_api = Blueprint('resources.users', __name__)
api = Api(users_api)

# Route
api.add_resource(UserList, '/user/signup', endpoint='user/signup')
api.add_resource(User, '/user/signin', endpoint='user/signin')
