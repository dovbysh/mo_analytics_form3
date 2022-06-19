import configparser
import os

from app import app
from flask_login import LoginManager, UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Table, create_engine

# from users_mgt import db, User as base
# from users_mgt import db_config

db_config = configparser.ConfigParser()
db_config.read('db_config.txt')

server = app.server
# config
server.config.update(
    SECRET_KEY=os.urandom(12),
    SQLALCHEMY_DATABASE_URI=db_config.get('database', 'con'),
    SQLALCHEMY_TRACK_MODIFICATIONS=False
)

engine = create_engine(db_config.get('database', 'con'))
db = SQLAlchemy()
db.init_app(server)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))

base = User
# Setup the LoginManager for the server
login_manager = LoginManager()
login_manager.init_app(server)
login_manager.login_view = '/login'


# Create User class with UserMixin
# class User_log(UserMixin, base):
#     pass


# callback to reload the user object
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))