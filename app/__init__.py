from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_babel import Babel
import cloudinary
from flask_mail import Mail
from dotenv import load_dotenv
import os


load_dotenv()
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
    "DATABASE_URL",
    "mysql+pymysql://root:root@localhost/cinemadb?charset=utf8mb4"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config['SECRET_KEY'] = 'suhtiwnetseveytneewtadyreveeyppahswt'

app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT') or 2525)
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS') == 'True'
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = (os.getenv('MAIL_SENDER_NAME', 'Cinema Admin'), os.getenv('MAIL_USERNAME'))

db = SQLAlchemy(app)
login = LoginManager(app)
babel = Babel(app)
mail = Mail()
mail.init_app(app)

# cloudinary.config(cloud_name='dkzxdp1gi',
#                   api_key='889343733763378',
#                   api_secret='AfqkwYpSy0i8oRU4XN4bRC-5qIg')

app.config["VNPAY_TMN_CODE"] = "SZM44ELG"
app.config["VNPAY_HASH_SECRET"] = "EMMTSPAWQ3UEWNT9UFMKI32HSLX34238"


cloudinary.config(
  cloud_name = "dimiharka",
  api_key = "333172498898523",
  api_secret = "7CtvguA8K-0A92T5Zp3BkiB_440",
  secure = True
)




