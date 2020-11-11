from flask import jsonify, Blueprint, abort
from flask_restful import Api, Resource, fields, marshal, marshal_with, reqparse
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token, get_jwt_identity)

import models

articles_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'description': fields.String,
    'published_at': fields.String
}


def get_or_abort(id):
    try:
        msg = models.Article.get_by_id(id)
    except models.Article.DoesNotExist:
        abort(404)
    else:
        return msg


def validate_owner(msg):
    current_user = get_jwt_identity()
    user = models.User.select().where(models.User.email == current_user).get()

    if msg.user_id == user:
        return True
    else:
        abort(403)


class ArticleBase(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'title',
            required=True,
            help='input is empty',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'description',
            required=True,
            help='input is empty',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'published_at',
            required=True,
            help='input is empty',
            location=['form', 'json']
        )
        super().__init__()


class ArticleList(ArticleBase):

    def get(self):

        # Get data from model
        articles = [marshal(article, articles_fields)
                    for article in models.Article.select()]

        # Print json
        return jsonify({'articles': articles})

    @jwt_required
    def post(self):

        # Get input
        args = self.reqparse.parse_args()
        current_user = get_jwt_identity()
        user = models.User.select().where(models.User.email == current_user).get()

        # Input data to model
        article = models.Article.create(
            title=args.get('title'),
            description=args.get('description'),
            user_id=user
        )

        # return true if success
        return marshal(article, articles_fields)


class Article(ArticleBase):
    @marshal_with(articles_fields)
    def get(self, id):
        return get_or_abort(id)

    @jwt_required
    def put(self, id):
        args = self.reqparse.parse_args()

        msg = get_or_abort(id)

        if validate_owner(msg):
            article = models.Article.update(title=args.get('title'), description=args.get(
                'description')).where(models.Article.id == id).execute()
            return 'update success'

    @jwt_required
    def delete(self, id):
        args = self.reqparse.parse_args()

        msg = get_or_abort(id)

        if validate_owner(msg):
            article = models.Article.delete().where(models.Article.id == id).execute()
            return 'delete success'


# Register
articles_api = Blueprint('resources.articles', __name__)
api = Api(articles_api)

# Route
api.add_resource(ArticleList, '/articles', endpoint='articles')
api.add_resource(Article, '/article/<int:id>', endpoint='article')
