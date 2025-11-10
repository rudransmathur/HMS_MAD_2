from application.model import Treatment
from application.database import db
from services.service_errors import ServiceError
from datetime import datetime


class TreatmentService:
    @staticmethod
    def get_all():
        return Treatment.query.all()

    @staticmethod
    def get_treatment(t_id):
        item = Treatment.query.filter_by(t_id=t_id)
        if not item:
            raise ServiceError("not Found")
        return item

    @staticmethod
    def delete_treatment(t_id):
        item = Treatment.query.filter_by(t_id=t_id).first()
        if not item:
            raise ServiceError("not Found")
        db.session.delete(item)
        db.session.commit()
        return {"message": "deleted item {}".format(t_id)}

    @staticmethod
    def update_treatment(data):
        item = Treatment.query.filter_by(t_id=data['t_id']).first()
        if not item:
            raise ServiceError("not Found")

        for key in data:
            if data[key] is not None:  # Only update non-None values
                setattr(item, key, data[key])

        db.session.commit()
        return item

    @staticmethod
    def create_treatment(data):
        item = Treatment.query.filter_by(t_id=data.get('t_id')).first()
        if item:
            raise ServiceError("Already Exists")

        item = Treatment(**data)
        db.session.add(item)
        db.session.commit()
        return item