from flask import Blueprint, jsonify, request
from controllers import *
from middleware import *

auth_route = Blueprint('auth', __name__)

@auth_route.route('/signup', methods=['POST'])
@validate_params(['username', 'password'])
@password_validation
def signup_route():
    try:
        result, status_code = signup()
        return jsonify({'message': result,  'status': status_code})
    except Exception as e:
        return jsonify({'message': 'Internal Server error', 'error': str(e), "status code": 500})

@validate_params(['username', 'password'])
@password_validation
@auth_route.route('/login', methods=['POST'])
def login_route():
    try:
        result, status_code = login()
        return jsonify(result), status_code
    except Exception as e:
        return jsonify({'message': 'Internal Server error', 'error': str(e), "status code": 500})

@auth_route.route('/home', methods=['GET'])
@jwt_required()
@protected_route
def home_route():
    try:
        result, status_code = home()
        return jsonify(result), status_code
    except Exception as e:
        return jsonify({'message': 'Internal Server error', 'error': str(e), "status code": 500})
    
@auth_route.route('/ask', methods=['GET'])
@jwt_required()
@protected_route
def ask_route():
    try:
        result, status_code = ask()
        return jsonify({'message': result,  'status_code': status_code})
    except Exception as e:
        return jsonify({'message': 'Internal Server error', 'error': str(e), "status code": 500})

# auth_routes.add_url_rule('/signup', view_func=signup, methods=['POST'])      
# auth_routes.add_url_rule('/login', view_func=login, methods=['POST'])
# auth_routes.add_url_rule('/home', view_func=home, methods=['GET'])
# auth_routes.add_url_rule('/ask', view_func=home, methods=['GET'])