# Scheduled Jobs & Notification System

This document describes the backend scheduled jobs and notification system for the hospital management application.

## Overview

The application includes an automated daily reminder system that sends appointment reminders to patients the morning of their scheduled appointment. Reminders can be sent via:

- **Email** - Via SMTP (Gmail, SendGrid, etc.)
- **SMS** - Via Twilio
- **Google Chat** - Via webhook integration

## Architecture

### Components

1. **APScheduler** - Handles scheduling and running background jobs
2. **NotificationService** - Sends reminders via different channels
3. **ScheduledJobs** - Defines the actual job logic
4. **ReminderResource** - REST API endpoint for manual trigger testing

### File Structure

```
backend/
  services/
    notification_service.py    # Sends reminders via email/SMS/Google Chat
    scheduled_jobs.py          # Scheduler setup and job definitions
  resources/
    reminder_resources.py      # API endpoint for manual trigger
```

## Setup Instructions

### 1. Install Dependencies

The required packages have been added to `requirements.txt`:
- `APScheduler==3.10.4` - For background job scheduling
- `requests==2.31.0` - For HTTP requests (webhooks, Twilio API)

Install dependencies:
```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Copy `.env.example` to `.env` and configure the following:

#### Email Configuration (for email reminders)
```env
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_app_password
```

For Gmail, use an [App Password](https://myaccount.google.com/apppasswords) instead of your regular password.

#### SMS Configuration (for SMS reminders via Twilio)
```env
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=+1234567890
```

Get your Twilio credentials from https://console.twilio.com/

#### Google Chat Configuration
```env
GOOGLE_CHAT_WEBHOOK_URL=https://chat.googleapis.com/v1/spaces/xxx/messages?key=xxx&token=xxx
```

See [Google Chat Webhooks](https://developers.google.com/chat/how-tos/webhooks) for setup.

### 3. Database Schema Update (if needed)

If you want to store patient contact preferences or Google Chat webhook URLs per patient, add these fields to the `Patient` model:

```python
class Patient(db.Model):
    # ... existing fields ...
    
    # Notification preferences
    phone_for_sms = db.Column(db.String(20), nullable=True)
    google_chat_webhook = db.Column(db.String(500), nullable=True)
    notification_channels = db.Column(db.String(100), default='email')  # 'email,sms,google_chat'
```

## How It Works

### Daily Reminder Job

The job runs daily at **8:00 AM** (configurable via `REMINDER_SCHEDULE_TIME` in `.env`):

1. Query all appointments scheduled for **today**
2. For each appointment:
   - Retrieve patient information
   - Determine notification channels (email, SMS, Google Chat)
   - Send reminder message via each channel
3. Log results (sent, failed, errors)

### Flow Diagram

```
APScheduler (8 AM daily)
    ↓
send_daily_appointment_reminders()
    ↓
Get today's appointments
    ↓
For each appointment:
    - Get patient details
    - Determine channels
    - Send notification via each channel
    ↓
Log results
```

## API Endpoints

### Manually Trigger Reminders

**Endpoint:** `POST /api/reminders/trigger`

**Authentication:** Required (login_required)

**Description:** Manually trigger the daily appointment reminder job. Useful for testing.

**Response:**
```json
{
  "status": "success",
  "message": "Daily reminder job completed",
  "total": 5,
  "sent": 5,
  "failed": 0
}
```

**Example:**
```bash
curl -X POST http://localhost:5000/api/reminders/trigger \
  -H "Authorization: Bearer <token>" \
  -H "Authentication-Token: <token>"
```

## Notification Templates

### Email Reminder
```
Subject: Appointment Reminder - [DATE] at [TIME]

Dear [PATIENT_NAME],

You have an appointment with Dr. [DOCTOR_NAME] on [DATE] at [TIME].
Please arrive 10 minutes early.

Thank you,
Hospital Management System
```

### SMS Reminder
```
Hi [PATIENT_NAME], reminder: You have an appointment with Dr. [DOCTOR_NAME] 
today at [TIME]. Please arrive 10 minutes early. Thank you!
```

### Google Chat Reminder
```
📋 Appointment Reminder for [PATIENT_NAME]

👨‍⚕️ Doctor: Dr. [DOCTOR_NAME]
📅 Date: [DATE]
🕐 Time: [TIME]

Please arrive 10 minutes early.
```

## Testing & Troubleshooting

### Test Manually

1. Create an appointment for today in the database
2. Call the trigger endpoint:
   ```bash
   curl -X POST http://localhost:5000/api/reminders/trigger
   ```
3. Check the logs for success/failure messages

### Check Logs

The application logs all reminder activity. Look for log entries starting with:
- `[EMAIL REMINDER]` - Email sent
- `[SMS]` - SMS sent
- `[GOOGLE_CHAT]` - Google Chat sent
- `Error sending reminder` - Failures

### Common Issues

**Issue:** Scheduler not starting
- **Solution:** Ensure APScheduler is installed: `pip install APScheduler`
- **Check logs:** Look for "Scheduler initialized successfully"

**Issue:** Emails not being sent
- **Solution:** Verify SMTP credentials in `.env`. Test with: 
  ```python
  from services.notification_service import NotificationService
  NotificationService.send_email_reminder('test@example.com', 'Patient', 'Doctor', '2025-12-01', '09:00')
  ```

**Issue:** SMS not being sent
- **Solution:** Verify Twilio credentials. Ensure `TWILIO_PHONE_NUMBER` is in E.164 format: `+1234567890`

**Issue:** Google Chat webhook not working
- **Solution:** Test webhook URL manually:
  ```bash
  curl -X POST https://chat.googleapis.com/v1/spaces/xxx/messages?key=xxx&token=xxx \
    -H "Content-Type: application/json" \
    -d '{"text":"Test message"}'
  ```

## Production Considerations

1. **Use a persistent job store** - Replace the in-memory scheduler with a database-backed store for production
2. **Error handling** - Implement retry logic for failed reminders
3. **Timezone support** - Set `TZ` environment variable to match your timezone
4. **Rate limiting** - Add delays between sending reminders to avoid overwhelming the service
5. **Logging** - Use a proper logging service (Sentry, DataDog, etc.) for monitoring
6. **Database transactions** - Wrap reminder job in transactions to handle database failures

### Production Scheduler Setup

For production, use a job store to persist scheduler state:

```python
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore

jobstores = {
    'default': SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')
}
scheduler = BackgroundScheduler(jobstores=jobstores)
```

## Customization

### Change Reminder Time

Edit `backend/services/scheduled_jobs.py`:
```python
scheduler.add_job(
    func=send_daily_appointment_reminders,
    trigger=CronTrigger(hour=9, minute=30),  # 9:30 AM daily
    ...
)
```

### Add New Notification Channel

1. Add method to `NotificationService`:
   ```python
   @staticmethod
   def send_slack_reminder(webhook_url, patient_name, doctor_name, ...):
       # Implementation
   ```

2. Update `send_reminder()` method to include new channel

3. Update patient model to store Slack webhook URL (optional)

### Filter Appointments

Currently sends to all appointments on a given day. To filter:

```python
# In scheduled_jobs.py
appointments_today = Appointment.query.filter(
    Appointment.appointment_date == today,
    Appointment.status == 'Confirmed'  # Only confirmed appointments
).all()
```

## API Reference

### NotificationService

#### send_email_reminder(recipient_email, patient_name, doctor_name, appointment_date, appointment_time)
- **Returns:** `bool` - Success/failure status
- **Description:** Send email reminder via SMTP

#### send_sms_reminder(phone, patient_name, doctor_name, appointment_date, appointment_time)
- **Returns:** `bool` - Success/failure status
- **Description:** Send SMS reminder via Twilio

#### send_google_chat_reminder(webhook_url, patient_name, doctor_name, appointment_date, appointment_time)
- **Returns:** `bool` - Success/failure status
- **Description:** Send Google Chat message via webhook

#### send_reminder(patient, appointment, channels=['email'])
- **Returns:** `dict` - Status of each channel {'email': True/False, 'sms': True/False, ...}
- **Description:** Send reminders via configured channels for a patient-appointment pair

### ScheduledJobs

#### send_daily_appointment_reminders()
- **Returns:** `dict` - Job result with status and counts
- **Description:** Main scheduled job that sends all daily reminders

#### init_scheduler(app)
- **Description:** Initialize APScheduler in Flask app context

## Future Enhancements

1. **Two-way communication** - Allow patients to confirm/reschedule via SMS reply
2. **Notification history** - Track sent reminders in database
3. **Patient preferences** - Let patients choose notification channels
4. **Multi-language support** - Send reminders in patient's preferred language
5. **Follow-up reminders** - Send reminders 24 hours and 1 hour before appointment
6. **Appointment confirmation** - Ask patients to confirm attendance before appointment
