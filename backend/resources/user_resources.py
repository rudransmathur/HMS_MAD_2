from flask import request
from flask import Blueprint, jsonify, request
from flask_restful import Resource, marshal, fields, reqparse
from flask_security import current_user
from flask_security.decorators import login_required, roles_required

from .marshal_fields import user_marshal, patient_marshal, doctor_marshal
from services import UserService, RequestService

# Base user parser (required fields)
parser = reqparse.RequestParser()
parser.add_argument('username', type=str)
parser.add_argument('fullname', type=str)
parser.add_argument('phone', type=int)
parser.add_argument('email', type=str)
parser.add_argument('active', type=bool)

# Patient data parser (user + patient fields)
patient_parser = reqparse.RequestParser()
patient_parser.add_argument('username', type=str)
patient_parser.add_argument('fullname', type=str)
patient_parser.add_argument('phone', type=int)
patient_parser.add_argument('email', type=str)
patient_parser.add_argument('active', type=bool)
# Patient-specific fields
patient_parser.add_argument('dob', type=str)
patient_parser.add_argument('gender', type=str)
patient_parser.add_argument('blood_group', type=str)
patient_parser.add_argument('emergency_contact', type=int)
patient_parser.add_argument('medical_history', type=str)

# Doctor data parser (user + doctor fields)
doctor_parser = reqparse.RequestParser()
doctor_parser.add_argument('username', type=str)
doctor_parser.add_argument('fullname', type=str)
doctor_parser.add_argument('phone', type=int)
doctor_parser.add_argument('email', type=str)
doctor_parser.add_argument('active', type=bool)
# Doctor-specific fields
doctor_parser.add_argument('department_name', type=int)
doctor_parser.add_argument('qualification', type=str)
doctor_parser.add_argument('experience_years', type=int)
doctor_parser.add_argument('specialization', type=str)
doctor_parser.add_argument('consultation_fee', type=float)
doctor_parser.add_argument('is_active', type=bool)


def get_appropriate_marshal(user_item):
    if user_item.patient_profile:
        return patient_marshal
    elif user_item.doctor_profile:
        return doctor_marshal
    else:
        return user_marshal


class UserResource(Resource):
    # By Admin for any userid and Patient for any doctorid
    @login_required
    def get(self, user_id):
        # Use service layer to fetch user and role-specific profiles
        item = UserService.get_user(user_id).first()
        if not item:
            return {'message': 'User not found'}, 404


        # Authorization checks
        if not (current_user.has_role("admin") or 
                (current_user.has_role("Patient") and item.has_role("Doctor")) or 
                current_user.user_id == item.user_id):
            return {'message': 'You are not authorized to perform this action'}, 401

        # If user has patient profile, validate via PatientService and return patient marshal
        if item.patient_profile:
            # import here to avoid circular imports at module load
            from services import PatientService
            from services.service_errors import ServiceError
            try:
                # Ensure the patient record exists and is valid
                PatientService.get_patient(user_id)
            except ServiceError:
                return {'message': 'Patient profile not found'}, 404

            return marshal(item, patient_marshal), 200

        # If user has doctor profile, validate via DoctorService and return doctor marshal
        if item.doctor_profile:
            from services import DoctorService
            from services.service_errors import ServiceError
            try:
                DoctorService.get_doctor(user_id)
            except ServiceError:
                return {'message': 'Doctor profile not found'}, 404

            return marshal(item, doctor_marshal), 200

        # Fallback: regular user marshal
        return marshal(item, user_marshal), 200

    # Only admin can do for doctors and patient can do for themselves.
    # Doctors will send request to admin for a change
    @login_required
    def put(self, user_id):
        item = UserService.get_user(user_id).first()
        if not item:
            return {'message': 'User not found'}, 404
        
        if current_user.has_role("Doctor") and current_user.user_id == user_id:
            req = {"data": request.get_json(), "status": "created", "type": "put", "user_id": user_id}
            RequestService.create_request(req)
            return {"message":f"request created, wait for admin approval"}, 200

        # Parse appropriate arguments based on user role
        if item.patient_profile:
            args = patient_parser.parse_args()
        elif item.doctor_profile:
            args = doctor_parser.parse_args()
        else:
            args = parser.parse_args()
        
        args["user_id"] = user_id

        if ((current_user.has_role("admin") and item.has_role("Doctor")) or
        current_user.user_id == user_id):
            # Handle profile-specific fields separately and use service-layer updates
            if item.patient_profile:
                patient_data = {k: v for k, v in args.items() if k in ['dob', 'gender', 'blood_group', 'emergency_contact', 'medical_history']}
                user_data = {k: v for k, v in args.items() if k not in patient_data}
                if user_data:
                    UserService.update_user(user_data)
                if patient_data:
                    from services import PatientService
                    PatientService.update_patient(user_id, patient_data)

                # Refresh the user and return patient marshal
                refreshed = UserService.get_user(user_id).first()
                return marshal(refreshed, patient_marshal), 200

            elif item.doctor_profile:
                doctor_data = {k: v for k, v in args.items() if k in ['department_name', 'qualification', 'experience_years', 'specialization', 'consultation_fee', 'is_active']}
                user_data = {k: v for k, v in args.items() if k not in doctor_data}
                if user_data:
                    UserService.update_user(user_data)
                if doctor_data:
                    from services import DoctorService
                    DoctorService.update_doctor(user_id, doctor_data)

                refreshed = UserService.get_user(user_id).first()
                return marshal(refreshed, doctor_marshal), 200

            else:
                UserService.update_user(args)
                refreshed = UserService.get_user(user_id).first()
                return marshal(refreshed, user_marshal), 200

        return {'message': 'You are not authorized to edit'}, 401

    # Authorization:
    # - Doctor: any delete request (self or other) → creates a delete request
    # - Admin: can delete any doctor except themselves
    # - Patient: can only delete themselves
    @login_required
    def delete(self, user_id):
        item = UserService.get_user(user_id).first()
        if not item:
            return {'message': 'User not found'}, 404
        # Doctors must create a delete request
        if current_user.has_role("Doctor") and current_user.user_id == user_id:
            req = {"data": "delete_request", "status": "created", "type": "delete", "user_id": user_id}
            RequestService.create_request(req)
            return {"message": f"request created for deletion, wait for admin approval"}, 200

        # Admin role: can delete any doctor except themselves
        if current_user.has_role("admin"):
            if current_user.user_id == user_id:
                return {'message': 'You cannot delete your own admin profile'}, 403
            if not item.has_role("Doctor"):
                return {'message': 'Admin can only delete doctor profiles'}, 403

            # UserService.delete_user handles all cascade deletions
            message = UserService.delete_user(user_id)
            return message, 200

        # Patient role: can only delete themselves
        if current_user.has_role("Patient"):
            if current_user.user_id != user_id:
                return {'message': 'Patient can only delete their own profile'}, 403

            # UserService.delete_user handles all cascade deletions
            message = UserService.delete_user(user_id)
            return message, 200

        return {'message': 'You are not authorized to delete'}, 401

    # Only admin can do for doctors and patient can do for themselves.
    # Doctors will send request to admin for a change
    @login_required
    def patch(self, user_id):
        data = request.get_json()
        data["user_id"] = user_id
        
        item = UserService.get_user(user_id).first()
        if not item:
            return {'message': 'User not found'}, 404

        if current_user.has_role("Doctor") and current_user.user_id == user_id:
            req = {"data": data, "status": "created", "type": "patch", "user_id": user_id}
            RequestService.create_request(req)
            return {"message":f"request created, wait for admin approval"}, 200

        if ((current_user.has_role("admin") and item.has_role("Doctor")) or
                current_user.user_id == user_id):
            # Handle profile-specific fields separately and use service-layer updates
            if item.patient_profile:
                patient_data = {k: v for k, v in data.items() if k in ['dob', 'gender', 'blood_group', 'emergency_contact', 'medical_history']}
                user_data = {k: v for k, v in data.items() if k not in patient_data}
                if user_data:
                    UserService.update_user(user_data)
                if patient_data:
                    from services import PatientService
                    PatientService.update_patient(user_id, patient_data)

                refreshed = UserService.get_user(user_id).first()
                return marshal(refreshed, patient_marshal), 200

            elif item.doctor_profile:
                doctor_data = {k: v for k, v in data.items() if k in ['department_name', 'qualification', 'experience_years', 'specialization', 'consultation_fee', 'is_active']}
                user_data = {k: v for k, v in data.items() if k not in doctor_data}
                if user_data:
                    UserService.update_user(user_data)
                if doctor_data:
                    from services import DoctorService
                    DoctorService.update_doctor(user_id, doctor_data)

                refreshed = UserService.get_user(user_id).first()
                return marshal(refreshed, doctor_marshal), 200

            else:
                UserService.update_user(data)
                refreshed = UserService.get_user(user_id).first()
                return marshal(refreshed, user_marshal), 200

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
