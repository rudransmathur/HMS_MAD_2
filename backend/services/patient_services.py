from application.model import User, Patient
from application.database import db
from .service_errors import ServiceError
from datetime import datetime

class PatientService:
    @staticmethod
    def get_all():
        return User.query.filter(User.patient_profile != None).all()

    @staticmethod
    def get_patient(patient_id):
        item = Patient.query.filter_by(patient_id=patient_id).first()
        if not item:
            raise ServiceError("Patient not found")
        return item

    @staticmethod
    def delete_patient(patient_id):
        item = Patient.query.filter_by(patient_id=patient_id).first()
        if not item:
            raise ServiceError("Patient not found")
        db.session.delete(item)
        db.session.commit()
        return {"message": f"deleted patient {patient_id}"}

    @staticmethod
    def update_patient(patient_id, data):
        """Update patient profile with given data"""
        from datetime import datetime, date
        
        item = Patient.query.filter_by(patient_id=patient_id).first()
        if not item:
            raise ServiceError("Patient not found")

        for key in data:
            if data[key] is not None:  # Only update non-None values
                # Convert dob string to date object if present
                if key == 'dob' and isinstance(data[key], str):
                    data[key] = datetime.strptime(data[key], '%Y-%m-%d').date()
                setattr(item, key, data[key])

        db.session.commit()
        return item

    @staticmethod
    def create_patient(patient_id, data):
        """Create a new patient profile"""
        from datetime import datetime, date
        
        item = Patient.query.filter_by(patient_id=patient_id).first()
        if item:
            raise ServiceError("Patient profile already exists")

        data['patient_id'] = patient_id
        
        # Convert dob string to date object if present
        if 'dob' in data and isinstance(data['dob'], str):
            data['dob'] = datetime.strptime(data['dob'], '%Y-%m-%d').date()
        
        item = Patient(**data)
        db.session.add(item)
        db.session.commit()
        return item
