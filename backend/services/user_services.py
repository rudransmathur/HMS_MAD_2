from application import User, Patient, Doctor, DoctorAvailability
from application import db
from .service_errors import ServiceError
from datetime import datetime

class UserService:
    @staticmethod
    def get_all():
        return User.query.all()

    @staticmethod
    def get_all_doctors():
        return Doctor.query.all()

    @staticmethod
    def get_doctors():
        return Doctor.query.all()

    @staticmethod
    def get_user(user_id):
        item = User.query.filter_by(user_id=user_id)
        if not item:
            raise ServiceError("not Found")
        return item

    @staticmethod
    def delete_user(user_id):
        
        item = User.query.filter_by(user_id=user_id).first()
        if not item:
            raise ServiceError("not Found")
        
        # Delete related DoctorAvailability records if doctor profile exists
        if item.doctor_profile:
            DoctorAvailability.query.filter_by(doctor_id=user_id).delete()
        
        # Delete related Doctor profile if exists
        if item.doctor_profile:
            db.session.delete(item.doctor_profile)
        
        # Delete related Patient profile if exists
        if item.patient_profile:
            db.session.delete(item.patient_profile)
        
        # Now delete the User
        db.session.delete(item)
        db.session.commit()
        return {"message": "deleted item {}".format(user_id)}

    @staticmethod
    def update_user(data):
        item = User.query.filter_by(user_id=data['user_id']).first()
        if not item:
            raise ServiceError("not Found")

        for key in data:
            if data[key] is not None:  # Only update non-None values
                setattr(item, key, data[key])
        db.session.commit()

    @staticmethod
    def create_user(data):
        item = User.query.filter_by(user_id=data.get('user_id')).first()
        if item:
            raise ServiceError("Already Exists")

        item = User(**data)
        db.session.add(item)
        db.session.commit()
        return item