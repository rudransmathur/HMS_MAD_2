from flask import request, jsonify
from flask_restful import Resource
from services.scheduled_jobs import send_daily_appointment_reminders
from flask_security import login_required
import logging

logger = logging.getLogger(__name__)


class ReminderResource(Resource):
    """
    API endpoint to manually trigger appointment reminders.
    Useful for testing and manual reminder sending.
    """
    
    @login_required
    @staticmethod
    def post():
        """
        POST /api/reminders/trigger
        Manually trigger the daily appointment reminder job.
        Admin only.
        """
        try:
            result = send_daily_appointment_reminders()
            return result, 200
        except Exception as e:
            logger.error(f"Error triggering reminders: {e}")
            return {'message': str(e), 'status': 'error'}, 500
