from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager 
from flask_wtf.csrf import CSRFProtect
from swe_project.config import databse_uri,configkey

app = Flask(__name__)
app.config['SECRET_KEY'] = configkey
app.config['SQLALCHEMY_DATABASE_URI']=databse_uri
db=SQLAlchemy(app)
login_manager=LoginManager(app) 
login_manager.login_view = 'login'
login_manager.login_message_category = 'info' 

csrf = CSRFProtect(app)
from swe_project import routes
