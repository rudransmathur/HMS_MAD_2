from flask import request
from flask import Blueprint, jsonify, request
from flask_restful import Resource, marshal, fields, reqparse

from .marshal_fields import treatment_marshal
from services import TreatmentService


parser = reqparse.RequestParser()
parser.add_argument('appointment_id', type=int, required=True)
parser.add_argument('patient_id', type=int, required=True)
parser.add_argument('doctor_id', type=int, required=True)
parser.add_argument('diagnosis', type=str, required=True)
parser.add_argument('prescription', type=str, required=True)
parser.add_argument('notes', type=str, required=True)

class TreatmentResource(Resource):
    @staticmethod
    def get(t_id):
        item = TreatmentService.get_treatment(t_id).first()
        return marshal(item, treatment_marshal), 200

    @staticmethod
    def put(t_id):
        item = TreatmentService.get_treatment(t_id).first()
        if not item:
            return {'message': 'Treatment not found'}, 404
        args = parser.parse_args()
        args["t_id"] = t_id
        TreatmentService.update_treatment(args)

    @staticmethod
    def delete(t_id):
        item = TreatmentService.get_treatment(t_id).first()
        if not item:
            return {'message': 'Treatment not found'}, 404
        message = TreatmentService.delete_treatment(t_id)
        return message

    @staticmethod
    def patch(t_id):
        item = TreatmentService.get_treatment(t_id).first()
        if not item:
            return {'message': 'Treatment not found'}, 404
        data = request.get_json()
        data["t_id"] = t_id
        TreatmentService.update_treatment(data)

class TreatmentListResource(Resource):
    @staticmethod
    def get():
        items = TreatmentService.get_all()
        return marshal(items, treatment_marshal), 200
    @staticmethod
    def post():
        args = parser.parse_args()
        item = TreatmentService.create_treatment(args)
        return marshal(item, treatment_marshal), 201