from os import abort
from flask import request, jsonify
from models import User
from middleware import jwt_required, create_access_token, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from middleware import validate_params, perform_login_validation
import logging

#salt = bcrypt.gensalt()

# Set up logging configuration
logging.basicConfig(level=logging.DEBUG)

def signup():
    username = request.json.get('username')
    password = request.json.get('password')

    if not username or not password:
        return 'Missing username or password', 400

    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return 'Username already exists', 409

    hashed_password = generate_password_hash(password, method='sha256')
    #hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    new_user = User(username=username, password=hashed_password)
    new_user.save()

    return 'User created successfully', 201

def login():
    username = request.json.get('username')
    password = request.json.get('password')

    if not username or not password:
        abort(400, 'Missing username or password')

    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password, password):
    #if not user or not bcrypt.checkpw(password.encode('utf-8'), user.password):
        #logging.debug("Received username: %s", username)
        #logging.debug("Received password: %s", password)
        #logging.debug("Received user password: %s", user.password)
        #logging.debug("Invalid username or password")
        #return {'message': 'Incorrect username or password'}, 409
        abort(409, 'Username already exists')

    access_token = create_access_token(identity=user.id)
    return {'access_token': access_token}, 200

def home():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    return {'message': f'Welcome, {user.username}!'}, 200
