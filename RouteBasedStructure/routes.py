from flask import Blueprint, jsonify, request
from controllers import *
from middleware import *

auth_route = Blueprint('auth', __name__)

@auth_route.route('/signup', methods=['POST'])
@validate_params(['username', 'password'])
def signup_route():
    result, status_code = signup()
    return jsonify({'message': result}), status_code

@validate_params(['username', 'password'])
@auth_route.route('/login', methods=['POST'])
def login_route():
    result, status_code = login()
    return jsonify(result), status_code

@auth_route.route('/home', methods=['GET'])
@jwt_required()
def home_route():
    result, status_code = home()
    return jsonify(result), status_code

# auth_routes.add_url_rule('/signup', view_func=signup, methods=['POST'])      
# auth_routes.add_url_rule('/login', view_func=login, methods=['POST'])
# auth_routes.add_url_rule('/home', view_func=home, methods=['GET'])