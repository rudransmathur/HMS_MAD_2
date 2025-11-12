from flask import request
from flask import Blueprint, jsonify, request
from flask_restful import Resource, marshal, fields, reqparse
from flask_security import current_user
from flask_security.decorators import login_required, roles_required

from .marshal_fields import user_marshal
from services import UserService, RequestService

parser = reqparse.RequestParser()
parser.add_argument('username', type=str, required=True)
parser.add_argument('fullname', type=str, required=True)
parser.add_argument('phone', type=int, required=True)
parser.add_argument('email', type=str, required=True)
parser.add_argument('active', type=bool, required=True)

class UserResource(Resource):
    # By Admin for any userid and Patient for any doctorid
    def get(self, user_id):
        item = UserService.get_user(user_id).first()
        if not item:
            return {'message': 'User not found'}, 404
        if current_user.has_role("admin"):
            return marshal(item, user_marshal), 200
        if current_user.has_role("Patient") and item.has_role("Doctor"):
            return marshal(item, user_marshal), 200
        if current_user.user_id == item.user_id:
            return marshal(item, user_marshal), 200
        return {'message': 'You are not authorized to perform this action'}, 401

    # Only admin can do for doctors and patient can do for themselves.
    # Doctors will send request to admin for a change
    def put(self, user_id):
        args = parser.parse_args()
        args["user_id"] = user_id

        if current_user.has_role("Doctor") and current_user.user_id == user_id:
            req = {"data": args, "status": "created", "type": "put", "user_id": user_id}
            RequestService.create_request(req)
            return {"message":f"request created for {args}, wait for admin apporval"}, 200

        item = UserService.get_user(user_id).first()
        if not item:
            return {'message': 'User not found'}, 404

        if (current_user.has_role("Patient") and current_user.user_id == user_id) or (current_user.has_role("admin") and item.has_role("Doctor")):
            UserService.update_user(args)
            return{"message": f"Updated id {user_id} with fields {args}"}, 200

        return {'message': 'You are not authorized to edit'}, 401

    # Only admin can do for doctors and patient can do for themselves.
    # Doctors will send request to admin for a change
    def delete(self, user_id):

        if current_user.has_role("Doctor") and current_user.user_id == user_id:
            req = {"data": "args", "status": "created", "type": "delete", "user_id": user_id}
            RequestService.create_request(req)
            return {"message":f"request created for {user_id}, wait for admin apporval"}, 200

        item = UserService.get_user(user_id).first()
        if not item:
            return {'message': 'User not found'}, 404

        if (current_user.has_role("Patient") and current_user.user_id == user_id) or (current_user.has_role("admin") and item.has_role("Doctor")):
            message = UserService.delete_user(user_id)
            return {"message": f"Deleted id {user_id} with fields {args}"}, 200

        return {'message': 'You are not authorized to delete'}, 401

    # Only admin can do for doctors and patient can do for themselves.
    # Doctors will send request to admin for a change
    def patch(self, user_id):
        data = request.get_json()
        data["user_id"] = user_id

        if current_user.has_role("Doctor") and current_user.user_id == user_id:
            req = {"data": data, "status": "created", "type": "put", "user_id": user_id}
            RequestService.create_request(req)
            return {"message":f"request created for {data}, wait for admin apporval"}, 200

        item = UserService.get_user(user_id).first()
        if not item:
            return {'message': 'User not found'}, 404

        if (current_user.has_role("Patient") and current_user.user_id == user_id) or (current_user.has_role("admin") and item.has_role("Doctor")):
            UserService.update_user(data)
            return {"message": f"Updated id {user_id} with fields {data}"}, 200

        return {'message': 'You are not authorized to edit'}, 401

class UserListResource(Resource):
    @staticmethod
    @roles_required("admin")
    def get():
        # only by admin
        items = UserService.get_all()
        return marshal(items, user_marshal), 200


def approve_user(user_id):
    user = UserService.update_user({"active": True, "user_id": user_id})
    return {"message": f"Updated id {user_id}"}, 200
