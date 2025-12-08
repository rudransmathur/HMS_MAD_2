from datetime import date, datetime, timedelta
from io import StringIO
import csv
from flask import render_template_string
from celery import shared_task

from application import Appointment, Treatment, Doctor
from .notify import send_email

@shared_task
def monthly_doctor_report():
    prev_month = date.today().month -1
    prev_month_name = date.today().replace(month=prev_month).strftime("%B")

    doctors = Doctor.query.filter(Doctor.is_active == True).all()
    for doc in doctors:
        appts = Appointment.query.filter(
            Appointment.doctor_id == doc.doctor_id,
            Appointment.appointment_date >= f"2025-{prev_month}-01",
            Appointment.appointment_date <= f"2025-{prev_month}-31"
        ).all()

        treatments = Treatment.query.filter(
            Treatment.doctor_id == doc.doctor_id,
            Treatment.treatment_date >= f"2025-{prev_month}-01",
            Treatment.treatment_date <= f"2025-{prev_month}-31"
        ).all()

        html_template = """
        <h2>Monthly Activity Report for Dr. {{ doctor.fullname }}</h2>
        <p>Month: {{prev_month_name}} </p>
        <h3>Appointments ({{ appts|length }})</h3>
        <table border="1" cellpadding="4" cellspacing="0">
            <tr><th>Patient</th><th>Date</th><th>Time</th><th>Status</th><th>Reason</th></tr>
            {% for a in appts %}
            <tr>
                <td>{{ a.patient.fullname }}</td>
                <td>{{ a.appointment_date }}</td>
                <td>{{ a.appointment_time }}</td>
                <td>{{ a.status }}</td>
                <td>{{ a.reason }}</td>
            </tr>
            {% endfor %}
        </table>

        <h3>Treatments ({{ treatments|length }})</h3>
        <table border="1" cellpadding="4" cellspacing="0">
            <tr><th>Patient</th><th>Date</th><th>Diagnosis</th><th>Prescription</th><th>Notes</th></tr>
            {% for t in treatments %}
            <tr>
                <td>{{ t.patient.fullname }}</td>
                <td>{{ t.treatment_date }}</td>
                <td>{{ t.diagnosis }}</td>
                <td>{{ t.prescription }}</td>
                <td>{{ t.notes }}</td>
            </tr>
            {% endfor %}
        </table>
        """

        body = render_template_string(html_template,
                                        doctor=doc,
                                        appts=appts,
                                        treatments=treatments,
                                        month=prev_month_name)

        send_email([doc.user.email],
                    f"Monthly Activity Report — {prev_month_name}",
                    body)

@shared_task
def export_treatments_csv(patient_id):
    treatments = Treatment.query.filter(Treatment.patient_id == patient_id).order_by(Treatment.treatment_date.asc()).all()
    si = StringIO()
    writer = csv.writer(si)
    writer.writerow(['Patient Name', 'Doctor Name', 'Appointment Date', 'Diagnosis', 'Prescription', 'Notes', 'Treatment Date'])
    for t in treatments:
        patient_name = t.patient.user.fullname
        doctor_name = t.doctor.user.fullname
        appt_date = t.appointment.appointment_date
        writer.writerow([patient_name, doctor_name, appt_date, t.diagnosis, t.prescription, t.notes, t.treatment_date])
    csv_bytes = si.getvalue().encode('utf-8')
    send_email([t.patient.user.email],
                "Your Treatment History Export",
                "<p>Please find your treatment history CSV attached.</p>",
                attachments=[(f"treatment_history_{patient_id}.csv", csv_bytes, 'text/csv')])
