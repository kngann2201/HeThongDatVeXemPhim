from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_babel import Babel
import cloudinary

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://root:root@localhost/cinemadb?charset=utf8mb4'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config['SECRET_KEY'] = 'suhtiwnetseveytneewtadyreveeyppahswt'
app.config['BABEL_DEFAULT_LOCALE'] = 'vi'

db = SQLAlchemy(app)
babel = Babel(app)

login = LoginManager()
login.init_app(app)

cloudinary.config(
  cloud_name = "dimiharka",
  api_key = "333172498898523",
  api_secret = "7CtvguA8K-0A92T5Zp3BkiB_440",
  secure = True
)