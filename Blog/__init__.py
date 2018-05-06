from flask import Flask
from flask_mysqldb import MySQL
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
app = Flask(__name__)
app.secret_key='Salman'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:mpasas12@localhost/Salwitter'


db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager= LoginManager(app)
login_manager.login_view = 'info'


from Blog import routes
