from flask import Blueprint, jsonify, request
from app import db
from app.models.user import User
from app.core.security import generate_token

bp = Blueprint('auth', __name__)

@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"message": "Missing email or password", "status": "error"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"message": "User already exists", "status": "error"}), 400

    new_user = User(email=email)
    new_user.set_password(password)
    
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully", "status": "success"}), 201

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()

    if user and user.check_password(password):
        token = generate_token(user.id)
        return jsonify({
            "message": "Login successful",
            "token": token,
            "status": "success"
        }), 200

    return jsonify({"message": "Invalid credentials", "status": "error"}), 401
