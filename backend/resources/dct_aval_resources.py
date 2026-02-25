from flask import request
from flask import Blueprint, jsonify, request
from flask_restful import Resource, marshal, fields, reqparse
from datetime import datetime

from .marshal_fields import availability_marshal
from services import DoctorAvailabilityService


parser = reqparse.RequestParser()
parser.add_argument('dav_id', type=int)
parser.add_argument('doctor_id', type=int, required=True)
parser.add_argument('date', type=str, required=True)
parser.add_argument('start_time', type=str, required=True)
parser.add_argument('end_time', type=str, required=True)

class DoctorAvailabilityResource(Resource):
    @staticmethod
    def get(dav_id):
        item = DoctorAvailabilityService.get_availability(dav_id).first()
        return marshal(item, availability_marshal), 200

    @staticmethod
    def put(dav_id):
        item = DoctorAvailabilityService.get_availability(dav_id).first()
        if not item:
            return {'message': 'Doctor Availability not found'}, 404
        args = parser.parse_args()
        args['date'] = datetime.strptime(args['date'], "%Y-%m-%d").date()
        args["dav_id"] = dav_id
        DoctorAvailabilityService.update_availability(args)

    @staticmethod
    def delete(dav_id):
        item = DoctorAvailabilityService.get_availability(dav_id).first()
        if not item:
            return {'message': 'Doctor Availability not found'}, 404
        message = DoctorAvailabilityService.delete_availability(dav_id)
        return message

    @staticmethod
    def patch(dav_id):
        item = DoctorAvailabilityService.get_availability(dav_id).first()
        if not item:
            return {'message': 'Doctor Availability not found'}, 404
        data = request.get_json()
        data["dav_id"] = dav_id
        DoctorAvailabilityService.update_availability(data)

class AllAvailabilityListResource(Resource):
    @staticmethod
    def get():
        items = DoctorAvailabilityService.get_all()
        return marshal(items, availability_marshal), 200
    @staticmethod
    def post():
        args = parser.parse_args()
        args['date'] = datetime.strptime(args['date'], "%Y-%m-%d").date()
        args['start_time'] = datetime.strptime(args['start_time'], "%H:%M:%S").time()
        args['end_time'] = datetime.strptime(args['end_time'], "%H:%M:%S").time()
        item = DoctorAvailabilityService.create_availability(args)
        return marshal(item, availability_marshal), 201

class DoctorAvailabilityListResource(Resource):
    @staticmethod
    def get(doc_id):
        items = DoctorAvailabilityService.get_doctors_availabilities(doc_id)
        return marshal(items, availability_marshal), 200