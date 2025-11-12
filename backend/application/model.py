from application.database import db
from flask_security import auth_required, UserMixin, RoleMixin
import datetime

roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.user_id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.role_id'))
)

class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    role_id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    description = db.Column(db.String, nullable=False)

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    fullname = db.Column(db.String(100))
    phone = db.Column(db.Integer())
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))

    fs_uniquifier = db.Column(db.String, unique=True, nullable=False)
    active = db.Column(db.Boolean(), default=True)

    patient_profile = db.relationship('Patient', back_populates='user', uselist=False, cascade='all, delete-orphan')
    doctor_profile = db.relationship('Doctor', back_populates='user', uselist=False, cascade='all, delete-orphan')
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))

class Patient(db.Model):
    __tablename__ = 'patient'
    patient_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), primary_key=True)
    dob = db.Column(db.Date)
    gender = db.Column(db.String(10))
    blood_group = db.Column(db.String(15))
    emergency_contact = db.Column(db.Integer())
    medical_history = db.Column(db.Text)

    user = db.relationship('User', back_populates='patient_profile', uselist=False)

    @property
    def age(self):
        today = datetime.date.today()
        years = today.year - self.dob.year
        if today.month < self.dob.month and today.day < self.dob.day:
            years -= 1
        return years

class Doctor(db.Model):
    __tablename__ = 'doctor'
    doctor_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), primary_key=True)
    department_name = db.Column(db.String, nullable=False)
    qualification = db.Column(db.String(200)) # MBBS MD DO DDS etc
    experience_years = db.Column(db.Integer)
    specialization = db.Column(db.String(100))
    consultation_fee = db.Column(db.Float)
    is_active = db.Column(db.Boolean, default=True)

    user = db.relationship('User', back_populates='doctor_profile', uselist=False)

class DoctorAvailability(db.Model):
    __tablename__ = 'doctor_availability'
    dav_id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    day_of_week = db.Column(db.Integer, nullable=False)  # 0=Mon ... 6=Sun
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)

    doctor = db.relationship('User', backref=db.backref('availabilities', lazy=True, cascade='all, delete-orphan'))

class Request(db.Model):
    __tablename__ = 'request'
    r_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    data = db.Column(db.JSON())
    status = db.Column(db.Enum("approved", "rejected", "created"))
    type = db.Column(db.String(20))

    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))

    user = db.relationship('User', backref=db.backref('requests', lazy=True))


class Appointment(db.Model):
    __tablename__ = 'appointment'
    ap_id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.patient_id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.doctor_id'), nullable=False)
    appointment_date = db.Column(db.Date, nullable=False)
    appointment_time = db.Column(db.Time, nullable=False)
    status = db.Column(db.String(20), default='Pending')
    reason = db.Column(db.Text)
    created_date = db.Column(db.DateTime, default=db.func.now())

    __table_args__ = (
        db.UniqueConstraint(
            'doctor_id', 'appointment_date', 'appointment_time',
            name='unique_doctor_datetime'
        ),
    )

    patient = db.relationship('Patient', foreign_keys=[patient_id])
    doctor = db.relationship('Doctor', foreign_keys=[doctor_id])

class Treatment(db.Model):
    __tablename__ = 'treatment'
    t_id = db.Column(db.Integer, primary_key=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointment.ap_id'))
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.patient_id'))
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.doctor_id'))
    diagnosis = db.Column(db.Text)
    prescription = db.Column(db.Text)
    notes = db.Column(db.Text)
    treatment_date = db.Column(db.DateTime, default=db.func.now())

    appointment = db.relationship('Appointment')
    patient = db.relationship('Patient', foreign_keys=[patient_id])
    doctor = db.relationship('Doctor', foreign_keys=[doctor_id])

class UserSession(db.Model):
    __tablename__ = 'user_session'
    session_id = db.Column(db.String(255), primary_key=True)  # Store session or token
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    last_active = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    session_data = db.Column(db.Text)  # For storing serialized info (JSON or similar)
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.Text)

class SystemLog(db.Model):
    __tablename__ = 'system_log'
    log_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=True)
    event_type = db.Column(db.String(32))
    event_desc = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.Text)

class BackgroundJob(db.Model):
    __tablename__ = 'background_job'
    job_id = db.Column(db.String(64), primary_key=True)
    task_name = db.Column(db.String(128))
    status = db.Column(db.String(32))  # 'PENDING', 'STARTED', 'SUCCESS', 'FAILURE'
    enqueued_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    started_at = db.Column(db.DateTime, nullable=True)
    finished_at = db.Column(db.DateTime, nullable=True)
    result = db.Column(db.Text, nullable=True)
    error = db.Column(db.Text, nullable=True)
    retries = db.Column(db.Integer, default=0)