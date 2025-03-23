from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from flask_mail import Mail
# from flask_bcrypt import Bcrypt
# from flask_wtf import FlaskForm,CSRFProtect

app=Flask(__name__)

app.config['SECRET_KEY'] = '8ea2a86e42689205dde0ba81f31138b6'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///civengine.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


from project import routes