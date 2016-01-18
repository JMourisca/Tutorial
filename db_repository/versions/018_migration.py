from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
image = Table('image', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('name', VARCHAR(length=200)),
    Column('flickr_id', VARCHAR(length=50)),
    Column('tags', VARCHAR(length=500)),
    Column('count_views', INTEGER),
    Column('url_sq', VARCHAR(length=200)),
    Column('url_t', VARCHAR(length=200)),
    Column('url_m', VARCHAR(length=200)),
    Column('url_s', VARCHAR(length=200)),
    Column('url_o', VARCHAR(length=200)),
    Column('photoset_id', VARCHAR(length=50)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['image'].drop()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['image'].create()
