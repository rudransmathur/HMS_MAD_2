from application.model import Doctor
from application.database import db
from .service_errors import ServiceError
from datetime import datetime

class DoctorService:
    @staticmethod
    def get_all():
        return Doctor.query.all()

    @staticmethod
    def get_doctor(doctor_id):
        item = Doctor.query.filter_by(doctor_id=doctor_id).first()
        if not item:
            raise ServiceError("Doctor not found")
        return item

    @staticmethod
    def delete_doctor(doctor_id):
        from application.model import DoctorAvailability
        
        item = Doctor.query.filter_by(doctor_id=doctor_id).first()
        if not item:
            raise ServiceError("Doctor not found")
        
        # Delete related DoctorAvailability records first (cascade)
        DoctorAvailability.query.filter_by(doctor_id=doctor_id).delete()
        
        db.session.delete(item)
        db.session.commit()
        return {"message": f"deleted doctor {doctor_id}"}

    @staticmethod
    def update_doctor(doctor_id, data):
        """Update doctor profile with given data"""
        item = Doctor.query.filter_by(doctor_id=doctor_id).first()
        if not item:
            raise ServiceError("Doctor not found")

        for key in data:
            if data[key] is not None:  # Only update non-None values
                setattr(item, key, data[key])

        db.session.commit()
        return item

    @staticmethod
    def create_doctor(doctor_id, data):
        """Create a new doctor profile"""
        item = Doctor.query.filter_by(doctor_id=doctor_id).first()
        if item:
            raise ServiceError("Doctor profile already exists")

        data['doctor_id'] = doctor_id
        item = Doctor(**data)
        db.session.add(item)
        db.session.commit()
        return item
