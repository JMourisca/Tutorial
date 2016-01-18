from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
photo = Table('photo', post_meta,
    Column('id', BigInteger, primary_key=True, nullable=False),
    Column('photoset_id', BigInteger),
    Column('title', String(length=200)),
    Column('isfamily', Integer),
    Column('ispublic', Integer),
    Column('tags', String(length=1000)),
    Column('views', Integer),
    Column('farm', Integer),
    Column('secret', String(length=20)),
    Column('height_o', Integer),
    Column('height_m', Integer),
    Column('height_s', Integer),
    Column('height_t', Integer),
    Column('height_sq', Integer),
    Column('width_o', Integer),
    Column('width_m', Integer),
    Column('width_s', Integer),
    Column('width_t', Integer),
    Column('width_sq', Integer),
    Column('url_o', String(length=300)),
    Column('url_m', String(length=300)),
    Column('url_s', String(length=300)),
    Column('url_t', String(length=300)),
    Column('url_sq', String(length=300)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['photo'].columns['photoset_id'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['photo'].columns['photoset_id'].drop()
