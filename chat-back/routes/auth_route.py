from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from app import db
from models.users import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    phone_number = data.get('phone_number')
    email = data.get('email')
    password = data.get('password')
    
    if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
        return jsonify({"msg": "Username or email already exists"}), 400
    
    new_user = User(username=username, phone_number=phone_number, email=email)
    new_user.set_password(password)
    
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({"msg": "User registered successfully"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username_or_email = data.get('username_or_email')
    password = data.get('password')
    
    user = User.query.filter((User.username==username_or_email) | (User.email==username_or_email)).first()
    print(user.username,"",user.password_hash)
    print(user.check_pass(password))
    
    if user and user.check_pass(password):
        access_token = create_access_token(identity={'username': user.username, 'email': user.email})
        return jsonify(access_token=access_token, user={'username': user.username, 'email': user.email}), 200
    else:
        return jsonify({"msg": "Bad username or password"}), 401
