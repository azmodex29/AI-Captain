import jwt
from datetime import datetime, timedelta
from flask import current_app, request, jsonify
from functools import wraps
from app.models.user import User

def generate_token(user_id):
    """Generates a JWT token for a user."""
    payload = {
        'exp': datetime.utcnow() + timedelta(days=1),
        'iat': datetime.utcnow(),
        'sub': user_id
    }
    return jwt.encode(
        payload,
        current_app.config.get('SECRET_KEY'),
        algorithm='HS256'
    )

def token_required(f):
    """Decorator to protect routes with JWT."""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith("Bearer "):
                token = auth_header.split(" ")[1]
            else:
                token = auth_header

        if not token:
            return jsonify({'message': 'Token is missing', 'status': 'error'}), 401

        try:
            data = jwt.decode(token, current_app.config.get('SECRET_KEY'), algorithms=["HS256"])
            current_user = User.query.filter_by(id=data['sub']).first()
            if not current_user:
                return jsonify({'message': 'Invalid token user', 'status': 'error'}), 401
        except Exception as e:
            current_app.logger.error(f"JWT Error: {str(e)}")
            return jsonify({'message': f'Token is invalid or expired: {str(e)}', 'status': 'error'}), 401

        return f(current_user, *args, **kwargs)

    return decorated
