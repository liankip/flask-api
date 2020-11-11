from flask import jsonify, Blueprint, abort
from flask_restful import Api, Resource, fields, marshal, marshal_with, reqparse

import models

message_fields = {
    'id': fields.Integer,
    'content': fields.String,
    'published_at': fields.String
}


def get_or_abort(id):
    try:
        msg = models.Message.get_by_id(id)
    except models.Message.DoesNotExist:
        abort(404)
    else:
        return msg


class MessageList(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'content',
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

    def get(self):

        # Get data from model
        messages = [marshal(message, message_fields)
                    for message in models.Message.select()]

        # Print json
        return jsonify({'messages': messages})

    def post(self):

        # Get input
        args = self.reqparse.parse_args()

        # Input data to model
        message = models.Message.create(**args)

        # return true if success
        return marshal(message, message_fields)


class Message(Resource):
    @marshal_with(message_fields)
    def get(self, id):
        return get_or_abort(id)


# Register
messages_api = Blueprint('resources.messages', __name__)
api = Api(messages_api)

# Route
api.add_resource(MessageList, '/messages', endpoint='messages')
api.add_resource(Message, '/message/<int:id>', endpoint='message')
