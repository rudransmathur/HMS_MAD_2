import os
import requests
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class NotificationService:
    @staticmethod
    def send_email_reminder(recipient_email, patient_name, doctor_name, appointment_date, appointment_time):
        try:
            logger.info(f"[EMAIL REMINDER] To: {recipient_email}")
            logger.info(f"Subject: Appointment Reminder - {appointment_date} at {appointment_time}")
            logger.info(f"Dear {patient_name}, you have an appointment with Dr. {doctor_name} on {appointment_date} at {appointment_time}")
            return True
        except Exception as e:
            logger.error(f"Failed to send reminder: {e}")
            return False

    @staticmethod
    def send_reminder(patient, appointment):
        try:
            doctor_name = appointment.doctor.user.fullname
            appointment_date = str(appointment.appointment_date)
            appointment_time = str(appointment.appointment_time)
            result = NotificationService.send_email_reminder(
                patient.user.email,
                patient.user.fullname,
                doctor_name,
                appointment_date,
                appointment_time
                )
            
            return result
            
        except Exception as e:
            logger.error(f"Error sending reminder: {e}")
            return {'error': str(e)}
