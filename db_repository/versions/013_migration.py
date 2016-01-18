from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
photoset = Table('photoset', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('primary', VARCHAR(length=100)),
    Column('date_update', DATETIME),
    Column('set_id', VARCHAR(length=100)),
    Column('can_comment', INTEGER),
    Column('farm', INTEGER),
    Column('description', VARCHAR(length=500)),
    Column('date_create', DATETIME),
    Column('secret', VARCHAR),
    Column('needs_interstitial', INTEGER),
    Column('title', VARCHAR(length=200)),
    Column('videos', INTEGER),
    Column('count_views', INTEGER),
    Column('photos', INTEGER),
    Column('visibility_can_see_set', INTEGER),
    Column('url_o', VARCHAR(length=300)),
    Column('url_m', VARCHAR(length=300)),
    Column('url_s', VARCHAR(length=300)),
    Column('url_t', VARCHAR(length=300)),
    Column('url_sq', VARCHAR(length=300)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['photoset'].columns['set_id'].drop()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['photoset'].columns['set_id'].create()
