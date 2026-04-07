from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_babel import Babel
import cloudinary

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://root:root@localhost/cinemadb?charset=utf8mb4'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config['SECRET_KEY'] = 'suhtiwnetseveytneewtadyreveeyppahswt'

# cloudinary.config(cloud_name='dkzxdp1gi',
#                   api_key='889343733763378',
#                   api_secret='AfqkwYpSy0i8oRU4XN4bRC-5qIg')

app.config["VNPAY_TMN_CODE"] = "SZM44ELG"
app.config["VNPAY_HASH_SECRET"] = "EMMTSPAWQ3UEWNT9UFMKI32HSLX34238"

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