from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity, JWTManager, exceptions
from functools import wraps
from flask import request, jsonify
import re

jwt = JWTManager()

def protected_route(func):
    @wraps(func)
    @jwt_required()
    def wrapper(*args, **kwargs):
        try:
            current_user_id = get_jwt_identity()
            return func(*args, **kwargs)
        except Exception as e:
            return jsonify({'message': 'Internal Server error', 'error': str(e), "status code": 500})
    return wrapper

def validate_params(required_params):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                if not request.is_json:
                    return jsonify({'message': 'Invalid JSON payload'}), 400

                for param in required_params:
                    if param not in request.json:
                        return jsonify({'message': f'Missing parameter: {param}'}), 400

                return func(*args, **kwargs)
            except Exception as e:
                return jsonify({'message': 'Internal Server error', 'error': str(e), "status code": 500})

        return wrapper

    return decorator


regexuser = '^[a-zA-Z0-9]+$'

def perform_login_validation(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            username = request.json.get('username')
            if not username.strip():
                return jsonify({'message': 'Internal server error'}), 500
            if len(username) < 3 or len(username) > 20:
                return jsonify({'message': 'Internal server error'}), 500
            if not re.match(regexuser, username):
                return jsonify({'message': 'Internal server error'}), 500

            return func(*args, **kwargs)
        except Exception as e:
                return jsonify({'message': 'Internal Server error', 'error': str(e), "status code": 500})

    return wrapper

def password_validation(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            password = request.json.get('password')

            if password==" ":
                return {'error': 'Password cannot be blank', "status code": 400}
            if len(password) < 3:
                return {'error': 'Password must be at least 3 characters long', "status code": 400}

            return func(*args, **kwargs)
        except Exception as e:
                return jsonify({'message': 'Internal Server error', 'error': str(e), "status code": 500})

    return wrapper