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

cloudinary.config(cloud_name=os.getenv('cloudinary_cloud_name'),
                  api_key=os.getenv('cloudinary_api_key'),
                  api_secret=os.getenv('cloudinary_api_secret'))

app.config["VNPAY_TMN_CODE"] = os.getenv('VNPAY_TMN_CODE')
app.config["VNPAY_HASH_SECRET"] = os.getenv('VNPAY_HASH_SECRET')





