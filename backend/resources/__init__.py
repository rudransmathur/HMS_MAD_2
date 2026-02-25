from flask_restful import Api
from flask import Blueprint

from .auth_resources import auth_bp
from .apt_resources import AppointmentResource, AppointmentListResource, PatientAppointmentsResource, DoctorAppointmentsResource
from .trt_resource import TreatmentResource, TreatmentListResource, PatientTreatmentResource, DoctorTreatmentResource
from .user_resources import UserResource, UserListResource, DoctorResource, PatientResource, activate_user, deactivate_user
from .dct_aval_resources import AllAvailabilityListResource, DoctorAvailabilityListResource, DoctorAvailabilityResource
from .rqt_resources import RequestResource, RequestListResource

api_bp = Blueprint('api', __name__, url_prefix='/api')
api = Api(api_bp)

api.add_resource(AppointmentListResource, '/appointments')
api.add_resource(AppointmentResource, '/appointments/<int:ap_id>')
api.add_resource(PatientAppointmentsResource, '/appointments/patient/<int:patient_id>')
api.add_resource(DoctorAppointmentsResource, '/appointments/doctor/<int:doctor_id>')

api.add_resource(TreatmentListResource, '/treatments')
api.add_resource(TreatmentResource, '/treatment/<int:t_id>')
api.add_resource(DoctorTreatmentResource, '/treatment/doctor/<int:doctor_id>')
api.add_resource(PatientTreatmentResource, '/treatment/patient/<int:patient_id>')

api.add_resource(UserListResource, '/users')
api.add_resource(UserResource, '/user/<int:user_id>')
api.add_resource(DoctorResource, '/doctors')
api.add_resource(PatientResource, '/patients')

api.add_resource(AllAvailabilityListResource, '/allavailability')
api.add_resource(DoctorAvailabilityListResource, '/allavailability/<int:doc_id>')
api.add_resource(DoctorAvailabilityResource, '/doctoravailability/<int:dav_id>')

api.add_resource(RequestListResource, '/requests')
api.add_resource(RequestResource, '/requests/<int:r_id>')

api_bp.add_url_rule("/user/<int:user_id>/activate", view_func=activate_user, methods=['PATCH'])
api_bp.add_url_rule("/user/<int:user_id>/deactivate", view_func=deactivate_user, methods=['PATCH'])