from application import Appointment
from application import db
from .service_errors import ServiceError
from datetime import datetime

class AppointmentService:
    @staticmethod
    def get_all():
        return Appointment.query.all()
    
    @staticmethod
    def get_appointments_by_patient(patient_id):
        items = Appointment.query.filter_by(patient_id=patient_id).all()
        return items

    @staticmethod
    def get_appointments_by_doctor(doctor_id):
        items = Appointment.query.filter_by(doctor_id=doctor_id).all()
        return items

    @staticmethod
    def get_appointment(ap_id):
        item=Appointment.query.filter_by(ap_id=ap_id)
        if not item:
            raise ServiceError("not Found")
        return item

    @staticmethod
    def delete_appointment(ap_id):
        item=Appointment.query.filter_by(ap_id=ap_id).first()
        if not item:
            raise ServiceError("not Found")
        db.session.delete(item)
        db.session.commit()
        return {"message": "deleted item {}".format(ap_id)}

    @staticmethod
    def update_appointment(data):
        item = Appointment.query.filter_by(ap_id=data['ap_id']).first()
        if not item:
            raise ServiceError("not Found")
        
        if 'appointment_date' in data and data['appointment_date']:
            data['appointment_date'] = datetime.strptime(data['appointment_date'], '%Y-%m-%d').date()

        if 'appointment_time' in data and data['appointment_time']:
            data['appointment_time'] = datetime.strptime(data['appointment_time'], '%H:%M:%S').time()

        for key in data:
            if data[key] is not None:
                setattr(item, key, data[key])
        
        db.session.commit()
        return item

    @staticmethod
    def create_appointment(data):
        if 'appointment_date' in data and data['appointment_date']:
            from datetime import datetime
            try:
                data['appointment_date'] = datetime.strptime(data['appointment_date'], '%Y-%m-%d').date()
            except ValueError:
                raise ServiceError("Invalid date format. Use YYYY-MM-DD")

        if 'appointment_time' in data and data['appointment_time']:
            from datetime import datetime
            try:
                data['appointment_time'] = datetime.strptime(data['appointment_time'], '%H:%M:%S').time()
            except ValueError:
                try:
                    data['appointment_time'] = datetime.strptime(data['appointment_time'], '%H:%M').time()
                except ValueError:
                    raise ServiceError("Invalid time format. Use HH:MM:SS or HH:MM")
        
        item = Appointment.query.filter_by(ap_id=data.get('ap_id')).first()
        if item:
            raise ServiceError("Already Exists")
        
        item = Appointment(**data)
        db.session.add(item)
        db.session.commit()
        return item