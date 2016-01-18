import flickrapi
from app import db
from config import FLICKR_API_KEY, FLICKR_API_SECRET, FLICKR_MY_ID, PHOTOS_PER_PAGE

class Photoset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    primary = db.Column(db.String(100))
    date_update = db.Column(db.DateTime)
    can_comment = db.Column(db.Integer)
    farm = db.Column(db.Integer)
    description = db.Column(db.String(500))
    date_create = db.Column(db.DateTime)
    secret = db.Column(db.String)
    needs_interstitial = db.Column(db.Integer)
    title = db.Column(db.String(200))
    videos = db.Column(db.Integer)
    count_views = db.Column(db.Integer)
    photos = db.Column(db.Integer)
    visibility_can_see_set = db.Column(db.Integer)
    url_o = db.Column(db.String(300))
    url_m = db.Column(db.String(300))
    url_s = db.Column(db.String(300))
    url_t = db.Column(db.String(300))
    url_sq = db.Column(db.String(300))
    images = db.relationship("Photo", backref="photoset", lazy="dynamic")

    def as_dict(self):
       return {c.title: getattr(self, c.title) for c in self.__table__.columns}

    def __repr__(self):
        return "<Flickr Photoset - %s>" % (self.title)

class Photo(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    photoset_id = db.Column(db.Integer, db.ForeignKey("photoset.id"))
    title = db.Column(db.String(200))
    isfamily = db.Column(db.Integer)
    ispublic = db.Column(db.Integer)
    tags = db.Column(db.String(1000))
    views = db.Column(db.Integer)
    farm = db.Column(db.Integer)
    secret = db.Column(db.String(20))
    height_o = db.Column(db.Integer)
    height_m = db.Column(db.Integer)
    height_s = db.Column(db.Integer)
    height_t = db.Column(db.Integer)
    height_sq = db.Column(db.Integer)
    width_o = db.Column(db.Integer)
    width_m = db.Column(db.Integer)
    width_s = db.Column(db.Integer)
    width_t = db.Column(db.Integer)
    width_sq = db.Column(db.Integer)
    url_o = db.Column(db.String(300))
    url_m = db.Column(db.String(300))
    url_s = db.Column(db.String(300))
    url_t = db.Column(db.String(300))
    url_sq = db.Column(db.String(300))

    def as_dict(self):
       return {c.title: getattr(self, c.title) for c in self.__table__.columns}

    def __repr__(self):
        return "<Flickr Photo - %s>" % (self.title)

class Flickr():
    flickr = flickrapi.FlickrAPI(FLICKR_API_KEY, FLICKR_API_SECRET, format="parsed-json")

    def photosets(self):
        return self.flickr.photosets.getList(user_id=FLICKR_MY_ID, per_page=5, page=1)

    def photos(self, photosetid, page=1, per_page=PHOTOS_PER_PAGE):
        return self.flickr.photosets.getPhotos(user_id=FLICKR_MY_ID,
                                               photoset_id=photosetid,
                                               per_page=per_page,
                                               page=page,
                                               extras="url_t,url_sq,url_s,url_m,url_o,views,path_alias,tags")

    def __repr__(self):
        return "<Flickr %r>" % ("Nurdagniriel")