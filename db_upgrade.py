#!flaskenv/bin/python
from migrate.versioning import api
from config import SQLALCHEMY_MIGRATE_REPO
from config import SQLALCHEMY_DATABASE_URI

api.upgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
print("DB upgraded. Current database version: " + str(v))