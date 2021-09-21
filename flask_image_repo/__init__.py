from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)

app.config['SECRET_KEY'] = '4f8db49c809f010b2271025d1dda4655'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_man = LoginManager(app)
login_man.login_view = 'login'
login_man.login_message_category = 'info'

from flask_image_repo import routes