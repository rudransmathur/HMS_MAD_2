from flask_restful import Api
from flask import Blueprint

from .auth_resources import auth_bp
from .apt_resources import AppointmentResource, AppointmentListResource
from .trt_resource import TreatmentResource, TreatmentListResource

api_bp = Blueprint('api', __name__, url_prefix='/api')
api = Api(api_bp)

api.add_resource(AppointmentListResource, '/appointments')
api.add_resource(AppointmentResource, '/appointments/<ap_id>')
api.add_resource(TreatmentListResource, '/treatments')
api.add_resource(TreatmentResource, '/treatments/<t_id>')