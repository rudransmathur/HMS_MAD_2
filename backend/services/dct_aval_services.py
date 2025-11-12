from application import DoctorAvailability
from application import db
from .service_errors import ServiceError
from datetime import datetime


class DoctorAvailabilityService:
    @staticmethod
    def get_all():
        return DoctorAvailability.query.all()

    @staticmethod
    def get_availability(dav_id):
        item = DoctorAvailability.query.filter_by(dav_id=dav_id)
        if not item:
            raise ServiceError("not Found")
        return item

    @staticmethod
    def delete_availability(dav_id):
        item = DoctorAvailability.query.filter_by(dav_id=dav_id).first()
        if not item:
            raise ServiceError("not Found")
        db.session.delete(item)
        db.session.commit()
        return {"message": "deleted item {}".format(dav_id)}

    @staticmethod
    def update_availability(data):
        item = DoctorAvailability.query.filter_by(dav_id=data['dav_id']).first()
        if not item:
            raise ServiceError("not Found")

        if 'start_time' in data and data['start_time']:
            data['start_time'] = datetime.strptime(data['start_time'], '%H:%M:%S').time()

        if 'end_time' in data and data['end_time']:
            data['end_time'] = datetime.strptime(data['end_time'], '%H:%M:%S').time()

        for key in data:
            if data[key] is not None:  # Only update non-None values
                setattr(item, key, data[key])

        db.session.commit()
        return item

    @staticmethod
    def create_availability(data):
        item = DoctorAvailability.query.filter_by(dav_id=data.get('dav_id')).first()
        if item:
            raise ServiceError("Already Exists")

        item = DoctorAvailability(**data)
        db.session.add(item)
        db.session.commit()
        return item