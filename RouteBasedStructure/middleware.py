from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity, JWTManager
from functools import wraps
from flask import request, jsonify
import re

jwt = JWTManager()

def protected_route(func):
    @wraps(func)
    @jwt_required()
    def wrapper(*args, **kwargs):
        current_user_id = get_jwt_identity()
        return func(*args, **kwargs)

    return wrapper

def validate_params(required_params):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not request.is_json:
                return jsonify({'message': 'Invalid JSON payload'}), 400

            for param in required_params:
                if param not in request.json:
                    return jsonify({'message': f'Missing parameter: {param}'}), 400

            return func(*args, **kwargs)

        return wrapper

    return decorator


regexuser = '^[a-zA-Z0-9]+$'

def perform_login_validation(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        username = request.json.get('username')
        if not username.strip():
            return jsonify({'message': 'Internal server error'}), 500
        if len(username) < 3 or len(username) > 20:
            return jsonify({'message': 'Internal server error'}), 500
        if not re.match(regexuser, username):
            return jsonify({'message': 'Internal server error'}), 500

        return func(*args, **kwargs)
    return wrapper
