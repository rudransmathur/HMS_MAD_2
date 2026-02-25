# scripts/seed_db.py
"""
Database seeder for the medical appointment app.

Usage:
    python scripts/seed_db.py

This script expects:
 - A Flask app factory named `create_app` in application (or a Flask app instance `app`).
 - application.database.db to be the SQLAlchemy db object.
 - models to be importable as `from models import Role, User, Patient, Doctor, DoctorAvailability, Appointment, Treatment, UserSession, SystemLog, BackgroundJob`
 - flask-security's hash_password available.

Adjust imports at top if your app layout differs.
"""

import random
import uuid
import datetime
from faker import Faker
from faker_food import FoodProvider
from sqlalchemy.exc import IntegrityError


from app import create_app
app, _ = create_app()

# database and models
from application.extension import db
from flask_security.utils import hash_password

# Import models as defined in your code base (the names used in your prompt)
from application.model import (
    Role,
    User,
    Patient,
    Doctor,
    DoctorAvailability,
    Appointment,
    Treatment,
    UserSession,
    SystemLog,
    BackgroundJob,
)

# -------------------------------------------------------------------

fake = Faker()
fake.add_provider(FoodProvider)

# small helpers
def make_phone_int():
    # create a 10-digit integer phone number (no leading zeros)
    s = ''.join([str(random.randint(6 if i == 0 else 0, 9)) for i in range(10)])
    return int(s)

def random_time_between(hour_start=9, hour_end=17):
    h = random.randint(hour_start, hour_end - 1)
    m = random.choice([0, 15, 30, 45])
    return datetime.time(h, m, 0)

def create_fs_uniquifier():
    return uuid.uuid4().hex

def safe_commit():
    try:
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        raise

def seed(app):
    with app.app_context():
        print("Starting DB seed...")

        # ---- ensure tables exist (optional) ----
        # If you prefer to run migrations separately, you can comment this out.
        db.drop_all()
        db.create_all()

        # Remove existing seed data *careful* — here we only check for existing roles to avoid duplicates.
        # Create roles
        role_names = [
            ("admin", "Administrator with full privileges"),
            ("Doctor", "Doctor role"),
            ("Patient", "Patient role"),
        ]
        roles_map = {}
        for name, desc in role_names:
            role = db.session.query(Role).filter_by(name=name).first()
            if not role:
                role = Role(name=name, description=desc)
                db.session.add(role)
                print(f"Added role: {name}")
            else:
                print(f"Role already exists: {name}")
            roles_map[name] = role
        safe_commit()

        # Create admin user (single)
        admin_user = db.session.query(User).filter_by(username='admin').first()
        if not admin_user:
            admin_user = User(
                username='admin',
                fullname='System Administrator',
                phone=make_phone_int(),
                email='admin@gmail.com',
                password=hash_password('admin'),
                fs_uniquifier=create_fs_uniquifier(),
                active=True
            )
            # associate role
            admin_user.roles.append(roles_map['admin'])
            db.session.add(admin_user)
            safe_commit()
            print("Created admin user: admin@gmail.com / username=admin")
        else:
            print("Admin user already exists, skipping creation.")

        # Create doctors
        NUM_DOCTORS = 10
        doctor_users = []
        department_ids = [1,2,3,4,5,6]  # since Doctor.department_name is Integer in model
        qualifications = ["MBBS", "MD", "DO", "MBBS MS", "MBBS MD"]
        specializations = [
            "General Medicine", "Cardiology", "Dermatology", "Pediatrics",
            "Orthopedics", "ENT", "Ophthalmology", "Psychiatry", "Gynecology", "Neurology"
        ]

        print(f"Seeding {NUM_DOCTORS} doctors...")
        for i in range(NUM_DOCTORS):
            username = f"doctor{i+1}"
            email = f"doctor{i+1}@example.com"
            # avoid duplicates
            if db.session.query(User).filter_by(username=username).first():
                print(f"User {username} already exists, skipping.")
                continue

            user = User(
                username=username,
                fullname=fake.name(),
                phone=make_phone_int(),
                email=email,
                password=hash_password("password"),  # default password for seeded doctors
                fs_uniquifier=create_fs_uniquifier(),
                active=True,
            )
            user.roles.append(roles_map['Doctor'])
            db.session.add(user)
            db.session.flush()  # get user.user_id for FK relations

            doc = Doctor(
                doctor_id=user.user_id,
                department_name=random.choice(department_ids),
                qualification=random.choice(qualifications),
                experience_years=random.randint(1, 30),
                specialization=random.choice(specializations),
                consultation_fee=round(random.uniform(15, 100), 2),
                is_active=True,
            )
            db.session.add(doc)
            doctor_users.append(user)
        safe_commit()
        print(f"Created {len(doctor_users)} doctor users.")

        # # Create doctor availabilities (2-4 slots per doctor)
        # print("Seeding doctor availabilities...")
        # for doc_user in doctor_users:
        #     # each doctor: 3 random days with morning/afternoon times
        #     days = random.sample(range(0, 7), k=3)
        #     for d in days:
        #         start = random_time_between(9, 15)
        #         end = (datetime.datetime.combine(datetime.date.today(), start) + datetime.timedelta(hours=2)).time()
        #         availability = DoctorAvailability(
        #             doctor_id=doc_user.user_id,
        #             day_of_week=d,
        #             start_time=start,
        #             end_time=end
        #         )
        #         db.session.add(availability)
        # safe_commit()
        # print("Doctor availabilities created.")

        # Create patients
        NUM_PATIENTS = 50
        patient_users = []
        print(f"Seeding {NUM_PATIENTS} patients...")
        for i in range(NUM_PATIENTS):
            username = f"patient{i+1}"
            email = f"patient{i+1}@example.com"
            if db.session.query(User).filter_by(username=username).first():
                continue
            user = User(
                username=username,
                fullname=fake.name(),
                phone=make_phone_int(),
                email=email,
                password=hash_password("password"),
                fs_uniquifier=create_fs_uniquifier(),
                active=True
            )
            user.roles.append(roles_map['Patient'])
            db.session.add(user)
            db.session.flush()

            # patient dob between 0 and 90 years
            dob = fake.date_of_birth(minimum_age=1, maximum_age=90)
            patient = Patient(
                patient_id=user.user_id,
                dob=dob,
                gender=random.choice(["Male", "Female", "Other"]),
                blood_group=random.choice(["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]),
                emergency_contact=make_phone_int(),
                medical_history=fake.sentence(nb_words=12)
            )
            db.session.add(patient)
            patient_users.append(user)
        safe_commit()
        print(f"Created {len(patient_users)} patients.")

        # Create appointments - create some realistic appointments (past & future)
        print("Seeding appointments and treatments...")
        appointments_created = 0
        treatments_created = 0
        # For each patient, schedule 0-3 appointments with random doctors
        appointment_date_base = datetime.date.today()
        for p_user in patient_users:
            num_ap = random.randint(0, 3)
            # get patient id
            patient_obj = db.session.query(Patient).filter_by(patient_id=p_user.user_id).first()
            if not patient_obj:
                continue
            chosen_doctors = random.sample(doctor_users, k=min(len(doctor_users), max(1, num_ap)))
            # schedule appointments on random days upcoming/past within +/-30 days
            for j in range(num_ap):
                doc_user = chosen_doctors[j % len(chosen_doctors)]
                # appointment date
                delta_days = random.randint(-30, 30)
                ap_date = appointment_date_base + datetime.timedelta(days=delta_days)
                ap_time = random_time_between(9, 16)
                # create appointment if unique constraint not violated
                ap = Appointment(
                    patient_id=patient_obj.patient_id,
                    doctor_id=doc_user.user_id,
                    appointment_date=ap_date,
                    appointment_time=ap_time,
                    status=random.choice(["Pending", "Confirmed", "Completed", "Cancelled"]),
                    reason=fake.sentence(nb_words=8),
                )
                db.session.add(ap)
                try:
                    db.session.flush()
                except IntegrityError:
                    db.session.rollback()
                    # skip conflicting slot
                    continue
                appointments_created += 1

                # For some appointments, create treatments (if appointment in past or completed)
                if ap.status in ("Completed",) or ap_date < datetime.date.today() and random.random() < 0.6:
                    treat = Treatment(
                        appointment_id=ap.ap_id,
                        patient_id=patient_obj.patient_id,
                        doctor_id=doc_user.user_id,
                        diagnosis=fake.sentence(nb_words=6),
                        prescription=fake.sentence(nb_words=10),
                        notes=fake.paragraph(nb_sentences=2),
                        treatment_date=datetime.datetime.combine(ap_date, ap_time)
                    )
                    db.session.add(treat)
                    treatments_created += 1
        safe_commit()
        print(f"Appointments created: {appointments_created}, Treatments created: {treatments_created}")

        # create a few user sessions (for admin and some doctors)
        print("Seeding user sessions & logs & background jobs...")
        sess_admin = UserSession(
            session_id=uuid.uuid4().hex,
            user_id=admin_user.user_id,
            session_data='{"logged_in": true}',
            ip_address="127.0.0.1",
            user_agent="Seeder/1.0",
            created_at=datetime.datetime.utcnow(),
            last_active=datetime.datetime.utcnow()
        )
        db.session.add(sess_admin)
        for du in doctor_users[:3]:
            s = UserSession(
                session_id=uuid.uuid4().hex,
                user_id=du.user_id,
                session_data='{"logged_in": true}',
                ip_address=fake.ipv4(),
                user_agent=fake.user_agent(),
                created_at=datetime.datetime.utcnow(),
                last_active=datetime.datetime.utcnow()
            )
            db.session.add(s)
        safe_commit()

        # System logs
        log = SystemLog(
            user_id=admin_user.user_id,
            event_type="SEED",
            event_desc="Database seeded with test data",
            ip_address="127.0.0.1",
            user_agent="Seeder/1.0"
        )
        db.session.add(log)
        safe_commit()

        # Background job example
        job = BackgroundJob(
            job_id=uuid.uuid4().hex[:32],
            task_name="initial_email_send",
            status="SUCCESS",
            enqueued_at=datetime.datetime.utcnow() - datetime.timedelta(minutes=15),
            started_at=datetime.datetime.utcnow() - datetime.timedelta(minutes=14),
            finished_at=datetime.datetime.utcnow() - datetime.timedelta(minutes=13),
            result="Sent 1 admin email",
            retries=0
        )
        db.session.add(job)
        safe_commit()

        # Final counts
        total_users = db.session.query(User).count()
        total_doctors = db.session.query(Doctor).count()
        total_patients = db.session.query(Patient).count()
        total_appointments = db.session.query(Appointment).count()
        total_treatments = db.session.query(Treatment).count()

        print("Seeding complete.")
        print(f"Users: {total_users}, Doctors: {total_doctors}, Patients: {total_patients}")
        print(f"Appointments: {total_appointments}, Treatments: {total_treatments}")

if __name__ == "__main__":
    seed(app)
