from flask import request
from flask import Blueprint, jsonify, request
from flask_restful import Resource, marshal, fields, reqparse

from .marshal_fields import request_marshal
from services import RequestService


parser = reqparse.RequestParser()
parser.add_argument('r_id', type=int, required=True)
parser.add_argument('data', type=dict, required=True)
parser.add_argument('status', type=str, required=True)
parser.add_argument('type', type=str, required=True)
parser.add_argument('user_id', type=int, required=True)

class RequestResource(Resource):
    @staticmethod
    def get(r_id):
        item = RequestService.get_request(r_id).first()
        return marshal(item, request_marshal), 200

    @staticmethod
    def put(r_id):
        item = RequestService.get_request(r_id).first()
        if not item:
            return {'message': 'Request not found'}, 404
        args = parser.parse_args()
        args["r_id"] = r_id
        RequestService.update_request(args)

    @staticmethod
    def delete(r_id):
        item = RequestService.get_request(r_id).first()
        if not item:
            return {'message': 'Request not found'}, 404
        message = RequestService.delete_request(r_id)
        return message

    @staticmethod
    def patch(r_id):
        item = RequestService.get_request(r_id).first()
        if not item:
            return {'message': 'Request not found'}, 404
        data = request.get_json()
        data["r_id"] = r_id
        RequestService.update_request(data)

class RequestListResource(Resource):
    @staticmethod
    def get():
        items = RequestService.get_all()
        return marshal(items, request_marshal), 200
    @staticmethod
    def post():
        args = parser.parse_args()
        item = RequestService.create_request(args)
        return marshal(item, request_marshal), 201