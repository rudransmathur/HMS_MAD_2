from application import Request
from application import db
from .service_errors import ServiceError
from datetime import datetime

class RequestService:
    @staticmethod
    def get_all():
        return Request.query.all()

    @staticmethod
    def get_request(r_id):
        item = Request.query.filter_by(r_id=r_id)
        if not item:
            raise ServiceError("not Found")
        return item

    @staticmethod
    def delete_request(r_id):
        item = Request.query.filter_by(r_id=r_id).first()
        if not item:
            raise ServiceError("not Found")
        db.session.delete(item)
        db.session.commit()
        return {"message": "deleted item {}".format(r_id)}

    @staticmethod
    def update_request(data):
        item = Request.query.filter_by(r_id=data['r_id']).first()
        if not item:
            raise ServiceError("not Found")

        for key in data:
            if data[key] is not None:  # Only update non-None values
                setattr(item, key, data[key])

        db.session.commit()
        return item

    @staticmethod
    def create_request(data):
        item = Request.query.filter_by(r_id=data.get('r_id')).first()
        if item:
            raise ServiceError("Already Exists")
        item = Request(**data)
        db.session.add(item)
        db.session.commit()
        return item