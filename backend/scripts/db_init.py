from app import app
from application.database import db
from flask_security.datastore import SQLAlchemyUserDatastore
from flask_security.utils import hash_password

from application.database import db
from application.model import Role

with app.app_context():
    db.drop_all()
    db.create_all()
    print('Created Database')
    datastore : SQLAlchemyUserDatastore = app.datastore

    admin_role = datastore.find_or_create_role('admin', description='Administrator')
    patient_role = datastore.find_or_create_role('Patient', description='Patient')
    doctors_role = datastore.find_or_create_role('Doctors', description='Doctors')
    db.session.add(admin_role)
    db.session.add(patient_role)
    db.session.add(doctors_role)
    db.session.commit()
    print('Created Roles')

    if not datastore.find_user(username='admin'):
        datastore.create_user(username='admin', email='@gmail.com', password=hash_password('admin'))
    db.session.commit()
    print('Created Admin')

    admin = datastore.find_user(username='admin')
    admin_role = datastore.find_role('admin')

    datastore.add_role_to_user(admin, admin_role)
    db.session.commit()
    print('Created User-Role')