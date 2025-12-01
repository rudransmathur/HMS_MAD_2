import logging
from datetime import date
from application import db, Appointment, Patient
from services.notification_service import NotificationService

logger = logging.getLogger(__name__)


def send_daily_appointment_reminders():
    try:
        logger.info("=== Starting daily appointment reminder job ===")
        
        appointments_today = Appointment.query.filter(Appointment.appointment_date == date.today()).all()
        
        if not appointments_today:
            logger.info(f"No appointments scheduled for {date.today()}")
            return {"status": "success", "message": "No appointments to remind", "count": 0}
        
        logger.info(f"Found {len(appointments_today)} appointments for {date.today()}")
        
        reminder_count = 0
        failed_count = 0
        
        # Send reminders for each appointment
        for appointment in appointments_today:
            try:
                patient = Patient.query.filter_by(patient_id=appointment.patient_id).first()

                results = NotificationService.send_reminder(appointment.patient, appointment)
                
                if results.get('error'):
                    logger.error(results['error'])
                    failed_count += 1
                else:
                    logger.info(f"Reminder sent for appointment {appointment.ap_id}: {results}")
                    reminder_count += 1
                    
            except Exception as e:
                logger.error(f"Error : {e}")
                failed_count += 1
        
        logger.info(f"=== Daily reminder job completed: {reminder_count} sent, {failed_count} failed ===")
        
        return {
            "status": "success",
            "message": "Daily reminder job completed",
            "total": len(appointments_today),
            "sent": reminder_count,
            "failed": failed_count
        }
        
    except Exception as e:
        logger.error(f"Fatal error in daily reminder job: {e}", exc_info=True)
        return {"status": "error", "message": str(e)}


def init_scheduler(app):
    """
    Initialize APScheduler and register scheduled jobs.
    
    Args:
        app: Flask application instance
    """
    from apscheduler.schedulers.background import BackgroundScheduler
    from apscheduler.triggers.cron import CronTrigger
    
    try:
        scheduler = BackgroundScheduler()
        
        # Schedule daily reminder job at 8 AM every day
        scheduler.add_job(
            func=send_daily_appointment_reminders,
            trigger=CronTrigger(hour=8, minute=0),  # 8:00 AM daily
            id='daily_appointment_reminders',
            name='Daily Appointment Reminders',
            replace_existing=True
        )
        
        scheduler.start()
        logger.info("Scheduler initialized successfully")
        logger.info("Scheduled jobs:")
        for job in scheduler.get_jobs():
            logger.info(f"  - {job.name}: {job.trigger}")
        
        # Gracefully shutdown scheduler when app closes
        def shutdown_scheduler():
            if scheduler.running:
                scheduler.shutdown()
                logger.info("Scheduler shut down")
        
        app.config['SCHEDULER'] = scheduler
        
    except Exception as e:
        logger.error(f"Failed to initialize scheduler: {e}", exc_info=True)
