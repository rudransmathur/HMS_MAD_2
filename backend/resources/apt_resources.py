from flask import request
from flask import Blueprint, jsonify, request
from flask_restful import Resource, marshal, fields, reqparse

appointment_marshal = {
    "patient_id": fields.Integer,
    "doctor_id": fields.Integer,
    "appointment_date": fields.String(attribute="appointment_date"),  # Will be converted from date object to string
    "appointment_time": fields.String(attribute="appointment_time"),
    "status": fields.String,
    "reason": fields.String,
    "created_date": fields.DateTime(dt_format='iso8601')
}

parser = reqparse.RequestParser()
parser.add_argument('patient_id', type=int)
parser.add_argument('doctor_id', type=int)
parser.add_argument('appointment_date', type=str)
parser.add_argument('appointment_time', type=str)
parser.add_argument('status', type=str)
parser.add_argument('reason', type=str)
parser.add_argument('created_date')

from services.apt_services import AppointmentService

class AppointmentResource(Resource):
    def get(self, ap_id):
        item = AppointmentService.get_appointment(ap_id).first()
        return marshal(item, appointment_marshal), 200

    def put(self, ap_id):
        item = AppointmentService.get_appointment(ap_id).first()
        if not item:
            return {'message': 'Appointment not found'}, 404
        args = parser.parse_args()
        args["ap_id"] = ap_id
        AppointmentService.update_appointment(args)

    def delete(self, ap_id):
        item = AppointmentService.get_appointment(ap_id).first()
        if not item:
            return {'message': 'Appointment not found'}, 404
        item = AppointmentService.delete_appointment(ap_id)
        return marshal(item, appointment_marshal), 200

    def patch(self, ap_id):
        item = AppointmentService.get_appointment(ap_id).first()
        if not item:
            return {'message': 'Appointment not found'}, 404
        data = request.get_json()
        data["ap_id"] = ap_id
        AppointmentService.update_appointment(data)


class AppointmentListResource(Resource):
    def get(self):
        items = AppointmentService.get_all()
        return marshal(items, appointment_marshal), 200
    def post(self):
        args = parser.parse_args()
        item = AppointmentService.create_appointment(args)
        return marshal(item, appointment_marshal), 201