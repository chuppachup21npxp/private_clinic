from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote
from flask_login import LoginManager
from flask_babelex import Babel
import cloudinary

app = Flask(__name__)
app.secret_key = '$#&*&%$(*&^(*^*&%^%$#^%&^%*&56547648764%$#^%$&^'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:%s@localhost/sql_clinic?charset=utf8mb4' % quote('phuc12345')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True

db = SQLAlchemy(app=app)
login = LoginManager(app=app)
babel = Babel(app=app)
cloudinary.config(cloud_name='dtoo1xp8u', api_key='388565515118322', api_secret='g0iVZWuqPCVkg0dMysDvciafQOQ')

@babel.localeselector
def load_locale():
    return "vi"
