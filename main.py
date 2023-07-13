from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from app.routes import auth_routes

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'BIHUJFegdsal'

db = SQLAlchemy(app)
jwt = JWTManager(app)


app.register_blueprint(auth_routes)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
