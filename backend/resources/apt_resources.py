from flask import request
from flask import Blueprint, jsonify, request
from flask_restful import Resource, marshal, fields, reqparse
from application import cache

from .marshal_fields import appointment_marshal
from services import AppointmentService, ServiceError


parser = reqparse.RequestParser()
parser.add_argument('patient_id', type=int, required=True)
parser.add_argument('doctor_id', type=int, required=True)
parser.add_argument('appointment_date', type=str, required=True)
parser.add_argument('appointment_time', type=str, required=True)
parser.add_argument('status', type=str, required=True)
parser.add_argument('reason', type=str, required=True)


class AppointmentResource(Resource):
    @staticmethod

    @cache.memoize()
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
        cache.delete_memoized(AppointmentResource.get, AppointmentResource, id)
        AppointmentService.update_appointment(args)

    @staticmethod
    def delete(ap_id):
        item = AppointmentService.get_appointment(ap_id).first()
        if not item:
            return {'message': 'Appointment not found'}, 404
        message = AppointmentService.delete_appointment(ap_id)
        cache.delete_memoized(AppointmentResource.get, AppointmentResource, id)
        return message

    @staticmethod
    def patch(ap_id):
        item = AppointmentService.get_appointment(ap_id).first()
        if not item:
            return {'message': 'Appointment not found'}, 404
        data = request.get_json()
        data["ap_id"] = ap_id
        cache.delete_memoized(AppointmentResource.get, AppointmentResource, id)
        AppointmentService.update_appointment(data)


class AppointmentListResource(Resource):
    @cache.cached(key_prefix="product_get")
    def get(self):
        items = AppointmentService.get_all()
        return marshal(items, appointment_marshal), 200

    def post(self):
        args = parser.parse_args()
        item = AppointmentService.create_appointment(args)
        cache.delete()
        return marshal(item, appointment_marshal), 201


class PatientAppointmentsResource(Resource):
    @staticmethod
    def get(patient_id):
        try:
            items = AppointmentService.get_appointments_by_patient(patient_id)
            return marshal(items, appointment_marshal), 200
        except ServiceError as e:
            return {"message": e.message}, 404


class DoctorAppointmentsResource(Resource):
    @staticmethod
    def get(doctor_id):
        items = AppointmentService.get_appointments_by_doctor(doctor_id)
        return marshal(items, appointment_marshal), 200