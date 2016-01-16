from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
category = Table('category', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('category', String(length=100)),
    Column('category_slug', String(length=100)),
    Column('timestamp', DateTime),
    Column('user_id', Integer),
)

subcategory = Table('subcategory', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('subcategory', String(length=100)),
    Column('subcategory_slug', String(length=100)),
    Column('timestamp', DateTime),
    Column('category_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['category'].create()
    post_meta.tables['subcategory'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['category'].drop()
    post_meta.tables['subcategory'].drop()
