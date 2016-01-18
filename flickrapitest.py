#!flaskenv/bin/python

import sys
import datetime
import flickrapi
from app import db
from app.models import Flickr
from app.flickr_models import Photoset, Photo

to_update = sys.argv

FLICKR_API_KEY = u"fe3681102a2a672c27a559f9d0e54a04"
FLICKR_API_SECRET = u"fa9cb0cb9cf4a297"
FLICKR_MY_ID = "99717691@N00"


if "photoset" in to_update:
    flickr = flickrapi.FlickrAPI(FLICKR_API_KEY, FLICKR_API_SECRET, format="parsed-json")
    sets = flickr.photosets.getList(user_id=FLICKR_MY_ID, primary_photo_extras="license, date_upload, date_taken, owner_name, "
                                                                           "icon_server, original_format, last_update, geo, "
                                                                           "tags, machine_tags, o_dims, views, media, path_alias, "
                                                                        "url_sq, url_t, url_s, url_m, url_o")
    print("--- ALBUNS --")
    for set in sets["photosets"]["photoset"]:
        id = set["id"]
        photoset = Photoset.query.filter_by(id=id).first()
        if photoset == None:
            print("It will insert a new set %s" % id)
            photoset = Photoset(id=int(id))
            db.session.add(photoset)
            db.session.commit()

            photoset = Photoset.query.filter_by(id=id).first()
        else:
            print("It will update the exsisting set %s" % id)

        photoset.title = set["title"]["_content"]
        photoset.count_views = set["count_views"]
        photoset.primary = set["primary"]
        photoset.date_create = datetime.datetime.fromtimestamp(float(set["date_create"]))
        photoset.date_update = datetime.datetime.fromtimestamp(float(set["date_update"]))
        photoset.can_comment = int(set["can_comment"])
        photoset.farm = int(set["farm"])
        photoset.description = set["description"]["_content"]
        photoset.secret = set["secret"]
        photoset.needs_interstitial = set["needs_interstitial"]
        photoset.videos = set["videos"]
        photoset.photos = set["photos"]
        photoset.visibility_can_see_set = set["visibility_can_see_set"]
        photoset.url_o = set["primary_photo_extras"]["url_o"]
        photoset.url_m = set["primary_photo_extras"]["url_m"]
        photoset.url_s = set["primary_photo_extras"]["url_s"]
        photoset.url_t = set["primary_photo_extras"]["url_t"]
        photoset.url_sq = set["primary_photo_extras"]["url_sq"]
        db.session.commit()

if "photos" in to_update:
    photosets = Photoset.query.all()

    for photoset in photosets:
        photoset = photoset.id
        flickr = Flickr()
        photos = flickr.photos(photoset, 1, 500)
        for fl_photo in photos["photoset"]["photo"]:
            id = fl_photo["id"]
            photo = Photo.query.filter_by(id=id).first()
            if photo == None:
                print("It will insert a new photo %s" % id)
                photo = Photo(id=int(id))
                db.session.add(photo)
                db.session.commit()

                photo = Photo.query.filter_by(id=id).first()
            else:
                print("It will update the exsisting set %s" % id)

            photo.photoset_id = photoset
            photo.title = fl_photo["title"]
            photo.isfamily = fl_photo["isfamily"]
            photo.ispublic = fl_photo["ispublic"]
            photo.tags = fl_photo["tags"]
            photo.views = int(fl_photo["views"])
            photo.farm = fl_photo["farm"]
            photo.secret = fl_photo["secret"]
            photo.height_o = fl_photo["height_o"]
            photo.height_m = fl_photo["height_m"]
            photo.height_s = fl_photo["height_s"]
            photo.height_t = fl_photo["height_t"]
            photo.height_sq = fl_photo["height_sq"]
            photo.width_o = fl_photo["width_o"]
            photo.width_m = fl_photo["width_m"]
            photo.width_s = fl_photo["width_s"]
            photo.width_t = fl_photo["width_t"]
            photo.width_sq = fl_photo["width_sq"]
            photo.url_o = fl_photo["url_o"]
            photo.url_m = fl_photo["url_m"]
            photo.url_s = fl_photo["url_s"]
            photo.url_t = fl_photo["url_t"]
            photo.url_sq = fl_photo["url_sq"]
            db.session.commit()



#
# print('Step 1: authenticate')
#
# # Only do this if we don't have a valid token already
# if not flickr.token_valid(perms='read'):
#
#     # Get a request token
#     flickr.get_request_token(oauth_callback='oob')
#
#     # Open a browser at the authentication URL. Do this however
#     # you want, as long as the user visits that URL.
#     authorize_url = flickr.auth_url(perms='read')
#     webbrowser.open_new_tab(authorize_url)
#
#     # Get the verifier code from the user. Do this however you
#     # want, as long as the user gives the application the code.
#     verifier = str(raw_input('Verifier code: '))
#
#     # Trade the request token for an access token
#     flickr.get_access_token(verifier)
#
# print('Step 2: use Flickr')
# resp = flickr.photos.getInfo(photo_id='23457070664')
# print(resp)
#
#
# print("--- Details of first album --")
# first_album = sets['photosets']['photoset'][0]
# print(first_album)

# flickr = flickrapi.FlickrAPI(FLICKR_API_KEY, FLICKR_API_SECRET, format="etree")
# random_photo_set = "72157653893025093"
# for photo in flickr.walk_set(random_photo_set):
#     photo_title = photo.get("title")
#     photo_id = photo.get("id")
#     short_url = flickr.shorturl.url(photo_id)
#     print("%s - %s - url: %s" % (photo_title, photo_id, short_url))