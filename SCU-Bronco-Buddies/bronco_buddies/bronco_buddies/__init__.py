import os
from flask import Flask 
from flask_sqlalchemy import SQLAlchemy #orm to run queries
from flask_bcrypt import Bcrypt 
from flask_login import LoginManager
from flask_mail import Mail
# from flask_socketio import SocketIO

app = Flask(__name__) # set app variable to an instance of the flask class
app.config['SECRET_KEY']='a27adadd2e3e4bb099e737cd7c3257e4' # create secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///BroncoBuddies.db' # chose your database

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login' # to redirect users to login if they haven't already 
login_manager.login_message_category = 'info' # for alert to login 
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USER_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')
mail = Mail(app)

from bronco_buddies import routes 