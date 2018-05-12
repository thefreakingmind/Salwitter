from flask import Flask
from flask_mysqldb import MySQL
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_restful import Resource, Api
app = Flask(__name__)
app.secret_key='Salman'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://k7gv49rbg20sdwxe:kqbe1xiyv0akj9gm@ocvwlym0zv3tcn68.cbetxkdyhwsb.us-east-1.rds.amazonaws.com/fh0pj3ghv5w81npg'

api = Api(app)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager= LoginManager(app)
login_manager.login_view = 'info'


from Blog import routes
