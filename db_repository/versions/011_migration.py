from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
photoset = Table('photoset', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('primary', String(length=100)),
    Column('date_update', DateTime),
    Column('set_id', String(length=100)),
    Column('can_comment', Integer),
    Column('farm', Integer),
    Column('description', String(length=500)),
    Column('date_create', DateTime),
    Column('secret', String),
    Column('needs_interstitial', Integer),
    Column('title', String(length=200)),
    Column('videos', Integer),
    Column('count_views', Integer),
    Column('photos', Integer),
    Column('visibility_can_see_set', Integer),
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
    post_meta.tables['photoset'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['photoset'].drop()
