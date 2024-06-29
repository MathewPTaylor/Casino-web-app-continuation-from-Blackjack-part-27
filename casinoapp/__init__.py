from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_socketio import SocketIO


app = Flask(__name__)
app.config['SECRET_KEY'] = "suckyourmumontuesdays"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///site.db"
app.config['TEMPLATES_AUTO_RELOAD'] = True

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login' # name of the function for the login route
login_manager.login_message_category = 'danger'

socketio = SocketIO(app, cors_allowed_origins="*")

from casinoapp import routes


# Initialising Casino tables and games
'''
Games to initialise:
1. Blackjack
2. Different types of poker
3. slots
4. roulette
'''
