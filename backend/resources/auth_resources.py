from flask import Blueprint, jsonify, request
from flask_security import verify_password, hash_password
from datetime import datetime
from flask_login import login_user, login_required

from flask import current_app
from application import User, Patient, Doctor, DoctorAvailability, db
from flask_login import login_user
from application import cache
from services import RequestService

auth_bp = Blueprint("auth", __name__, url_prefix='/api/auth')

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json(force=True)

    username = data['username']
    password = data['password']

    if not username or not password:
        return jsonify({"message": "Please provide username and password"}), 400

    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"message": "User does not exist"}), 404
    if not verify_password(password, user.password):
        return jsonify({"message":"Invalid Password"}), 400
    if not user.active:
        return jsonify({"message":"User is flagged"})

    login_user(user, remember=True)

    user_role = user.roles[0].name if user.roles else None

    return jsonify({
        "id": user.user_id,
        "name": user.username,
        "fullname": user.fullname,
        "phone": user.phone,
        "email": user.email,
        "role": user_role,
        "token": user.get_auth_token()
    }), 200

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    role = data['role']
    username = data['username']
    fullname = data['fullname']
    phone = data['phone']
    email = data['email']
    password = data['password']

    active = True

    exists = User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first()
    if exists:
        return jsonify({"message": "User already exists"}), 400
    if role not in ["Doctor", "Patient"]:
        return jsonify({"message": "Invalid info"}), 400
    if not (username and fullname and phone and email and password):
        return jsonify({"message": "Enter Values in fields"}), 400
    if role == "Doctor":
        active = False

    try:
        datastore = current_app.datastore

        user = datastore.create_user(username=username,
                                     fullname=fullname,
                                     phone=phone,
                                     email=email,
                                     password=hash_password(password),
                                     active=active)
        user = User.query.filter_by(username=username).first()
    except Exception as e:
        return jsonify({"message": f"SignUp error: {e}"}), 500
    try:
        if role=="Patient":
            dob = data["dob"]
            # Convert dob string (YYYY-MM-DD) to Python date object
            if isinstance(dob, str):
                dob = datetime.strptime(dob, '%Y-%m-%d').date()

            gender = data["gender"]
            emergency_contact = data["emergency_contact"]
            blood_group = data.get("blood_group", "")
            medical_history = data.get("medical_history", "")

            item = Patient(patient_id = user.user_id, dob = dob, gender = gender,
                           emergency_contact = emergency_contact, blood_group = blood_group,
                           medical_history = medical_history)
            db.session.add(item)
            db.session.commit()
        else:
            department_name = data["department_name"]
            qualification = data["qualification"]
            experience_years = data["experience_years"]
            specialization = data["specialization"]
            consultation_fee = data["consultation_fee"]
            availabilities = data["availabilities"]

            item = Doctor(doctor_id = user.user_id, department_name = department_name,
                          qualification = qualification, experience_years = experience_years,
                          specialization = specialization, consultation_fee = consultation_fee)

            db.session.add(item)
            db.session.commit()

            for i in availabilities:
                days_of_week = {"Monday":0, "Tuesday":1, "Wednesday":2, "Thursday":3,
                                "Friday":4, "Saturday":5, "Sunday":6}
                # Convert time strings (HH:MM) to Python time objects
                start_time = i['start']
                end_time = i['end']
                if isinstance(start_time, str):
                    start_time = datetime.strptime(start_time, '%H:%M').time()
                if isinstance(end_time, str):
                    end_time = datetime.strptime(end_time, '%H:%M').time()

                item_d = DoctorAvailability(doctor_id = user.user_id, day_of_week = days_of_week[i['day']],
                                            start_time = start_time, end_time = end_time)
                db.session.add(item_d)
                db.session.commit()
            
            req = {"data": data, "status": "created", "type": "put", "user_id": user.user_id}
            RequestService.create_request(req)
            
            cache.delete("user_get")

            role_obj = datastore.find_role(role)
            datastore.add_role_to_user(user, role_obj)
            db.session.commit()
            
            return {"message":f"request created, wait for admin approval"}, 200

        role_obj = datastore.find_role(role)
        datastore.add_role_to_user(user, role_obj)

        db.session.commit()

        cache.delete("user_get")
        return jsonify({"id": user.user_id,
                        "username": user.username,
                        "fullname": user.fullname,
                        "phone": user.phone,
                        "email": user.email,
                        "role": role,
                        "active": active}), 200
    except Exception as e:
        return jsonify({"message": e}), 500