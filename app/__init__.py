import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.openid import OpenID
from config import basedir #, ADMINS, MAIL_SERVER, MAIL_PORT, MAIL_USERNAME, MAIL_PASSWORD, MAIL_REQUIRE_SSL
from flask.ext.mail import Mail
from .momentjs import MomentJs

app = Flask(__name__)
app.config.from_object('config')
app.jinja_env.globals["momentjs"] = MomentJs

db = SQLAlchemy(app)

lm = LoginManager()
lm.init_app(app)
lm.login_view = "login"

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
    # from logging.handlers import SMTPHandler
    # credentials = None
    # if MAIL_USERNAME or MAIL_PASSWORD:
    #     credentials = (MAIL_USERNAME, MAIL_PASSWORD)
    #
    # mail_handler = SMTPHandler((MAIL_SERVER, MAIL_PORT), "no-reply@gmail.com", ADMINS, "microblog failure",
    #                            credentials, secure=True)
    # mail_handler.setLevel(logging.ERROR)
    # app.logger.addHandler(mail_handler)

from app import views, models