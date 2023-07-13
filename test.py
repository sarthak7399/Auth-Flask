from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from os import path
import re
from functools import wraps     #The wraps function is used to preserve the original function's metadata

app = Flask(__name__)    #A Flask app object is created with the name app. 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'   #The SQLALCHEMY_DATABASE_URI configuration is set to connect to an SQLite database named database.db.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False    #The SQLALCHEMY_TRACK_MODIFICATIONS configuration is set to False to disable tracking modifications by SQLAlchemy. 
app.config['JWT_SECRET_KEY'] = 'BIHUJFegdsal'   # Change this to your preferred secret key

db = SQLAlchemy(app)
jwt = JWTManager(app)

def protected_route(func):          #The route will now require authentication before it can be accessed.
    @wraps(func)
    @jwt_required()
    def wrapper(*args, **kwargs):
        current_user_id = get_jwt_identity()        # Perform additional actions with the current_user_id if needed
        return func(*args, **kwargs)
    return wrapper

def validate_params(required_params):       #To ensure that JSON input is in well structured format 
    def decorator(func):
        @wraps(func)        #ensures the decorated function retains its original name and docstring.
        def wrapper(*args, **kwargs):
            if not request.is_json:
                return jsonify({'message': 'Invalid JSON payload'}), 400

            for param in required_params:
                if param not in request.json:
                    return jsonify({'message': f'Missing parameter: {param}'}), 400

            return func(*args, **kwargs)        #If all the parameters are present in the JSON payload
        return wrapper
    return decorator

regexuser='^[a-zA-Z0-9]+$'
def perform_login_validation(username):     #To ensure some basic validation parameters for entries 
    if not username.strip():
        return {'message': 'Internal server error'}, 500
    if len(username) < 3 or len(username) > 20:
        return {'message': 'Internal server error'}, 500
    if not re.match(regexuser, username):
        return {'message': 'Internal server error'}, 500
    return None

def validate_login_paramstype(func):        #Decorator function that takes up the logic from perform_login_validation function to be implemented anywhere
    @wraps(func)
    def wrapper(*args, **kwargs):
        username = request.json.get('username')
        validation_result = perform_login_validation(username)
        if validation_result:
            return jsonify(validation_result)
        return func(*args, **kwargs)
    return wrapper


class User(db.Model):  #The User class is defined as a subclass of db.Model, representing a user entity in the database. It has columns for id, username, and password. 
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __init__(self, username, password):     #The __init__ method is used to set the initial values of the username and password attributes.
        self.username = username
        self.password = password

@app.route('/signup', methods=['POST'])
@validate_params(['username', 'password'])
@validate_login_paramstype
def signup():
    username = request.json.get('username')
    password = request.json.get('password')

    if not username or not password:
        return jsonify({'message': 'Missing username or password'}), 400    # 400 (Bad Request)

    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({'message': 'Username already exists'}), 409     #  409 (Conflict)

    hashed_password = generate_password_hash(password)
    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User created successfully'}), 201   #   201 (Created).

@app.route('/login', methods=['POST'])
@validate_params(['username', 'password'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')      

    if not username or not password:
        return jsonify({'message': 'Missing username or password'}), 400

    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({'message': 'Invalid username or password'}), 401

    access_token = create_access_token(identity=user.id)
    return jsonify({'access_token': access_token}), 200


@app.route('/home', methods=['GET'])
@jwt_required()
@protected_route
def home():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    return jsonify({'message': f'Welcome, {user.username}!'}), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)