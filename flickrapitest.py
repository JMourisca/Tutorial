#!flaskenv/bin/python


import webbrowser

import flickrapi
from pip._vendor.distlib.compat import raw_input

FLICKR_API_KEY = u"fe3681102a2a672c27a559f9d0e54a04"
FLICKR_API_SECRET = u"fa9cb0cb9cf4a297"
FLICKR_MY_ID = "99717691@N00"

photo_set_test = u"72157653893025093"

flickr = flickrapi.FlickrAPI(FLICKR_API_KEY, FLICKR_API_SECRET, format="parsed-json")
photosfromset = flickr.photosets.getPhotos(user_id=FLICKR_MY_ID, photoset_id=photo_set_test)

print(photosfromset)

#photos = flickr.photos.search(user_id=FLICKR_MY_ID, per_page="10")
#sets = flickr.photosets.getList(user_id=FLICKR_MY_ID)
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
# print("--- ALBUNS --")
# for set in sets["photosets"]["photoset"]:
#     title = set["title"]["_content"]
#     id = set["id"]
#     count_views = set["count_views"]
#     print("%s - %s - %s" % (title, count_views, id))
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