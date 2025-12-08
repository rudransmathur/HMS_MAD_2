from datetime import date
from celery import shared_task

from application import Appointment
from .notify import send_email

@shared_task
def daily_reminder():
    today = date.today()
    appts = Appointment.query.filter(Appointment.appointment_date == today)\
                                .filter(Appointment.status != 'Cancelled').all()
    for ap in appts:
        patient = ap.patient
        msg = f"Hi {patient.user.fullname}, you have an appointment with Dr. {ap.doctor.user.fullname} today at {ap.appointment_time}. Please be on time."

        send_email([patient.user.email], "Appointment Reminder", msg)