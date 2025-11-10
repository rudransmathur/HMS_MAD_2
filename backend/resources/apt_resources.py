from flask import request
from flask import Blueprint, jsonify, request
from flask_restful import Resource, marshal, fields, reqparse

from .marshal_fields import appointment_marshal
from services.apt_services import AppointmentService


parser = reqparse.RequestParser()
parser.add_argument('patient_id', type=int)
parser.add_argument('doctor_id', type=int)
parser.add_argument('appointment_date', type=str)
parser.add_argument('appointment_time', type=str)
parser.add_argument('status', type=str)
parser.add_argument('reason', type=str)

class AppointmentResource(Resource):
    @staticmethod
    def get(ap_id):
        item = AppointmentService.get_appointment(ap_id).first()
        return marshal(item, appointment_marshal), 200

    @staticmethod
    def put(ap_id):
        item = AppointmentService.get_appointment(ap_id).first()
        if not item:
            return {'message': 'Appointment not found'}, 404
        args = parser.parse_args()
        args["ap_id"] = ap_id
        AppointmentService.update_appointment(args)

    @staticmethod
    def delete(ap_id):
        item = AppointmentService.get_appointment(ap_id).first()
        if not item:
            return {'message': 'Appointment not found'}, 404
        message = AppointmentService.delete_appointment(ap_id)
        return message

    @staticmethod
    def patch(ap_id):
        item = AppointmentService.get_appointment(ap_id).first()
        if not item:
            return {'message': 'Appointment not found'}, 404
        data = request.get_json()
        data["ap_id"] = ap_id
        AppointmentService.update_appointment(data)


class AppointmentListResource(Resource):
    @staticmethod
    def get():
        items = AppointmentService.get_all()
        return marshal(items, appointment_marshal), 200
    @staticmethod
    def post():
        args = parser.parse_args()
        item = AppointmentService.create_appointment(args)
        return marshal(item, appointment_marshal), 201