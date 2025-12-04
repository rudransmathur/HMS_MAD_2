from flask_restful import fields

appointment_marshal = {
    "ap_id": fields.Integer,
    "patient_id": fields.Integer,
    "doctor_id": fields.Integer,
    "patient_name": fields.String(attribute="patient.user.fullname"),
    "doctor_name": fields.String(attribute="doctor.user.fullname"),
    "appointment_date": fields.String(attribute="appointment_date"),
    "appointment_time": fields.String(attribute="appointment_time"),
    "status": fields.String,
    "reason": fields.String,
    "created_date": fields.DateTime(dt_format='iso8601')
}

treatment_marshal = {
    "t_id": fields.Integer,
    "appointment_id": fields.Integer,
    "patient_id": fields.Integer,
    "doctor_id": fields.Integer,
    "patient_name": fields.String(attribute="patient.user.fullname"),
    "doctor_name": fields.String(attribute="doctor.user.fullname"),
    "diagnosis": fields.String,
    "prescription": fields.String,
    "notes": fields.String,
    "created_date": fields.DateTime(attribute="treatment_date", dt_format='iso8601')
}

user_marshal = {
    "user_id": fields.Integer,
    "username": fields.String,
    "fullname": fields.String,
    "phone": fields.Integer,
    "email": fields.String,
    "active": fields.Boolean
}

patient_marshal = {
    "user_id": fields.Integer,
    "username": fields.String,
    "fullname": fields.String,
    "phone": fields.Integer,
    "email": fields.String,
    "active": fields.Boolean,
    "patient_id": fields.Integer(attribute="patient_profile.patient_id"),
    "dob": fields.String(attribute="patient_profile.dob"),
    "gender": fields.String(attribute="patient_profile.gender"),
    "blood_group": fields.String(attribute="patient_profile.blood_group"),
    "emergency_contact": fields.Integer(attribute="patient_profile.emergency_contact"),
    "medical_history": fields.String(attribute="patient_profile.medical_history"),
    "age": fields.Integer(attribute="patient_profile.age")
}

doctor_marshal = {
    "user_id": fields.Integer,
    "username": fields.String,
    "fullname": fields.String,
    "phone": fields.Integer,
    "email": fields.String,
    "active": fields.Boolean,
    "doctor_id": fields.Integer(attribute="doctor_profile.doctor_id"),
    "department_name": fields.String(attribute="doctor_profile.department_name"),
    "qualification": fields.String(attribute="doctor_profile.qualification"),
    "experience_years": fields.Integer(attribute="doctor_profile.experience_years"),
    "specialization": fields.String(attribute="doctor_profile.specialization"),
    "consultation_fee": fields.Float(attribute="doctor_profile.consultation_fee"),
    "is_active": fields.Boolean(attribute="doctor_profile.is_active")
}

availability_marshal = {
    "dav_id": fields.Integer,
    "doctor_id": fields.Integer,
    "day_of_week": fields.Integer,
    "start_time": fields.String(attribute="start_time"),
    "end_time": fields.String(attribute="end_time")
}

request_marshal = {
    "r_id": fields.Integer,
    "data": fields.Raw,
    "status": fields.String,
    "type": fields.String,
    "user_id": fields.Integer,
    "username": fields.String(attribute="user.username"),
    "fullname": fields.String(attribute="user.fullname")
}