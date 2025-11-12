from argon2 import hash_password
from flask import Blueprint, jsonify, request
from flask_security import verify_password, hash_password

from flask import current_app
from application import User, db
from flask_login import login_user

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

    # create a server-side session (session cookie) so @login_required works
    login_user(user)

    return jsonify({
        "id": user.user_id,
        "name": user.username,
        "fullname": user.fullname,
        "phone": user.phone,
        "email": user.email,
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
    if not (role in ["Doctor","Patient"] or username or fullname or phone or email or password):
        return jsonify({"message": "Invalid info"}), 400
    if role == "Doctor":
        active = False

    datastore = current_app.datastore

    user = datastore.create_user(username=username,
                                 fullname=fullname,
                                 phone=phone,
                                 email=email,
                                 password=hash_password(password),
                                 active=active)
    db.session.commit()
    user = User.query.filter_by(username=username).first()
    role = datastore.find_role(role)
    datastore.add_role_to_user(user, role)

    db.session.commit()

    return jsonify({"id": user.user_id,
                    "username": user.username,
                    "fullname": user.fullname,
                    "phone": user.phone,
                    "email": user.email,
                    "active": active}), 200