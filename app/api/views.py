import json

from app import bp, app
from app.flickr_models import Photo
from flask.ext.login import login_required
from flask import Response

@app.route("/api/album/<photosetid>/photos")
@login_required
def album_photos(photosetid):
    photos = Photo.query.filter_by(photoset_id=photosetid).all()
    photos_dict = dict()
    photos_arr = []
    for photo in photos:
        item = dict((col, getattr(photo, col)) for col in photo.__table__.columns.keys())
        photos_arr.append(item.copy())
    photos_dict["data"] = photos_arr
    return Response(json.dumps(photos_arr), mimetype='application/json')