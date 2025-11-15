from flask_restful import Api
from flask import Blueprint

from .auth_resources import auth_bp
from .apt_resources import AppointmentResource, AppointmentListResource, PatientAppointmentsResource, DoctorAppointmentsResource
from .trt_resource import TreatmentResource, TreatmentListResource, PatientTreatmentResource, DoctorTreatmentResource
from .user_resources import UserResource, UserListResource, DoctorResource, approve_user
from .dct_aval_resources import DoctorAvailabilityResource, DoctorAvailabilityListResource
from .rqt_resources import RequestResource, RequestListResource

api_bp = Blueprint('api', __name__, url_prefix='/api')
api = Api(api_bp)

api.add_resource(AppointmentListResource, '/appointments')
api.add_resource(AppointmentResource, '/appointments/<int:ap_id>')
api.add_resource(PatientAppointmentsResource, '/appointments/patient/<int:patient_id>')
api.add_resource(DoctorAppointmentsResource, '/appointments/doctor/<int:doctor_id>')

api.add_resource(TreatmentListResource, '/treatments')
api.add_resource(TreatmentResource, '/treatment/<int:t_id>')

api.add_resource(UserListResource, '/users')
api.add_resource(UserResource, '/user/<int:user_id>')

api.add_resource(DoctorAvailabilityListResource, '/doctoravailability')
api.add_resource(DoctorAvailabilityResource, '/doctoravailability/<int:doc_id>')

api.add_resource(RequestListResource, '/requests')
api.add_resource(RequestResource, '/requests/<int:request_id>')

api_bp.add_url_rule("/user/<int:user_id>/approve", view_func=approve_user, methods=['PATCH'])