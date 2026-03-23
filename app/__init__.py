from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://root:root@localhost/cinemadb?charset=utf8mb4'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config['SECRET_KEY'] = 'suhtiwnetseveytneewtadyreveeyppahswt'

db = SQLAlchemy(app)

login = LoginManager()
login.init_app(app)