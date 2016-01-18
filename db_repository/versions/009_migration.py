from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
image = Table('image', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=200)),
    Column('flickr_id', String(length=50)),
    Column('tags', String(length=500)),
    Column('count_views', Integer),
    Column('url_sq', String(length=200)),
    Column('url_t', String(length=200)),
    Column('url_m', String(length=200)),
    Column('url_s', String(length=200)),
    Column('url_o', String(length=200)),
    Column('photoset_id', String(length=50)),
)

image_count = Table('image_count', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('count_view', Integer),
    Column('image_id', Integer),
    Column('timestamp', DateTime),
)

images_subcat = Table('images_subcat', post_meta,
    Column('subcategory_id', Integer),
    Column('image_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['image'].create()
    post_meta.tables['image_count'].create()
    post_meta.tables['images_subcat'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['image'].drop()
    post_meta.tables['image_count'].drop()
    post_meta.tables['images_subcat'].drop()
