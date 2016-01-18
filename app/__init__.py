import os
import datetime
from flask import Flask, Blueprint
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.openid import OpenID
from flask.ext.babel import Babel, lazy_gettext
from flask.json import JSONEncoder
from config import basedir
from flask.ext.mail import Mail
from .momentjs import MomentJs
from flask_triangle import Triangle

class CustomJSONEncoder(JSONEncoder):
    """This class adds support for lazy translation texts to Flask's
    JSON encoder. This is necessary when flashing translated texts."""
    def default(self, obj):
        from speaklater import is_lazy_string
        if is_lazy_string(obj):
            return str(obj)  # python 3
        return super(CustomJSONEncoder, self).default(obj)

def from_timestamp(timestamp, format):
    return datetime.datetime.fromtimestamp(
        float(timestamp)
    ).strftime(format)

app = Flask(__name__)
app.config.from_object('config')
app.jinja_env.globals["momentjs"] = MomentJs
app.jinja_env.globals["from_timestamp"] = from_timestamp
app.jinja_env.add_extension('jinja2.ext.do')
app.json_encoder = CustomJSONEncoder

bp = Blueprint("api", __name__)
app.register_blueprint(bp, url_prefix="/api/")

Triangle(app)

babel = Babel(app)

db = SQLAlchemy(app)

lm = LoginManager()
lm.init_app(app)
lm.login_view = "login"
lm.login_message = lazy_gettext('Please log in to access this page.')

mail = Mail(app)

oid = OpenID(app, os.path.join(basedir, 'tmp'))

if not app.debug:
    import logging
    from logging.handlers import RotatingFileHandler

    file_handler = RotatingFileHandler("tmp/microblog.log", "a", 1*1024*1024, 10)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('microblog startup')

from app import views, models, flickr_models
from app.api import views