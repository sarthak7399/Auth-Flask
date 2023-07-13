from flask import Blueprint, jsonify
from controllers import signup, login, home

auth_routes = Blueprint('auth', __name__)

auth_routes.add_url_rule('/signup', view_func=signup, methods=['POST'])      
auth_routes.add_url_rule('/login', view_func=login, methods=['POST'])
auth_routes.add_url_rule('/home', view_func=home, methods=['GET'])