from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
application = Flask(__name__)
application.config['SQLALCHEMY_DATABASE_URI']='sqlite:///market.db' #used so that Flask application can reconize db and see where it is located
application.config['SECRET_KEY']='405ac523f3d41649ef3cfb2b'

db=SQLAlchemy(application)               #URI stands for Uniform Resource Identifier
bcrypt=Bcrypt(application)

login_manager=LoginManager(application)
login_manager.login_view='login_page'
login_manager.login_message_category='info'
from market import routes
