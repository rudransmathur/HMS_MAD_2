from flask_restful import fields

appointment_marshal = {
    "patient_id": fields.Integer,
    "doctor_id": fields.Integer,
    "appointment_date": fields.String(attribute="appointment_date"),  # Will be converted from date object to string
    "appointment_time": fields.String(attribute="appointment_time"),
    "status": fields.String,
    "reason": fields.String,
    "created_date": fields.DateTime(dt_format='iso8601')
}

treatment_marshal = {
    "appointment_id": fields.Integer,
    "patient_id": fields.Integer,
    "doctor_id": fields.Integer,
    "diagnosis": fields.String,
    "prescription": fields.String,
    "notes": fields.String,
    "created_date": fields.DateTime(attribute="treatment_date", dt_format='iso8601')
}