import decimal
import json

from app import app, lm, db, oid, babel
from app.emails import follower_notification
from app.forms import LoginForm, EditForm, CategoryForm, SubCategoryForm, SearchAlbum
from app.models import User, Category, Subcategory
from app.flickr_models import Photoset, Photo
from config import PHOTOSETS_PER_PAGE, LANGUAGES
from datetime import datetime
from flask import render_template, flash, redirect, g, url_for, session, request, jsonify, Response
from flask.ext.babel import gettext
from flask.ext.login import login_user, logout_user, current_user, login_required
from flask_triangle import triangle
from slugify import slugify

"""
    g = global. Is setup by Flask as a place to store and share data during the life of a request.
"""

__author__ = 'juliana'


# URLS
@app.route('/')
@app.route('/index')
@app.route('/index/<int:page>')
@login_required
def index(page=1):
    user = g.user
    photosets = Photoset.query.order_by(Photoset.date_create.desc()).paginate(page, PHOTOSETS_PER_PAGE, False)
    total_views = sum([int(i.count_views) for i in photosets.items])
    total_photos = sum([int(i.photos) for i in photosets.items])
    form = CategoryForm()
    form_sub = SubCategoryForm()
    categories = user.categories.all()

    return render_template('index.html',
                           title='Home',
                           user=user,
                           form=form,
                           form_sub=form_sub,
                           categories=categories,
                           photosets=photosets,
                           total_views=total_views,
                           total_photos=total_photos,
                           page=page,
                           total=10)

@app.route("/category", methods=["POST"])
@login_required
def category():
    form = CategoryForm()
    if form.validate_on_submit():
        category_slug = slugify(form.category.data)
        category = Category(category=form.category.data,
                            timestamp=datetime.utcnow(),
                            author=g.user,
                            category_slug=category_slug)
        db.session.add(category)
        db.session.commit()
        flash("Category created!")
    else:
        flash("Nothing happened.")
    return redirect(url_for("index"))

@app.route("/category/<int:category_id>/subcategory", methods=["POST"])
@login_required
def subcategory(category_id):
    form_sub = SubCategoryForm()
    if form_sub.validate_on_submit():
        subcategory_slug = slugify(form_sub.subcategory.data)
        subcategory = Subcategory(subcategory=form_sub.subcategory.data,
                            timestamp=datetime.utcnow(),
                            category_id=category_id,
                            subcategory_slug=subcategory_slug)
        db.session.add(subcategory)
        db.session.commit()
        flash("Subcategory created!")
    else:
        flash_errors(form_sub)

    return redirect(url_for("index"))

@app.route("/add_photo/<int:subcategory_id>", methods=["GET", "POST"])
@login_required
def add_photo(subcategory_id):
    subcategory = Subcategory.query.filter_by(id=subcategory_id).first()
    category = subcategory.category
    form = SearchAlbum()
    albums = None
    if form.validate_on_submit():
        query = form.query.data
        albums = Photoset.query.filter(Photoset.title.like("%"+query+"%")).all()

    return render_template("add_photo.html",
                           subcategory=subcategory,
                           category=category,
                           form=form,
                           albums=albums)

@app.route("/subcategory/<int:subcategory_id>", methods=["DELETE"])
@login_required
def delete_subcategory(subcategory_id):
    user = g.user
    s = Subcategory.query.filter_by(id = subcategory_id).first()
    deleted = False
    if s == None:
        msg = "Subcategory doesn't exist."
    else:
        deleted, msg = s.delete(user.id)

    response = {"status": 200, "result": str(deleted), "msg": msg}
    return jsonify(response)

@app.route("/category/<int:category_id>", methods=["DELETE"])
@login_required
def delete_category(category_id):
    user = g.user
    s = Category.query.filter_by(id = category_id).first()
    deleted = False
    if s == None:
        msg = "Category doesn't exist."
    else:
        deleted, msg = s.delete(user.id)

    response = {"status": 200, "result": str(deleted), "msg": msg}
    return jsonify(response)

@app.route("/album/<photosetid>")
@app.route("/album/<photosetid>/<int:page>")
@login_required
def album(photosetid, page=1):
    photos = Photo.query.filter_by(photoset_id=photosetid).paginate(page, PHOTOSETS_PER_PAGE, False)
    total = int(photos.total/PHOTOSETS_PER_PAGE)

    return render_template("flickr_album.html", photos=photos, total=total, page=page, photosetid=photosetid)

def alchemyencoder(obj):
    """JSON encoder function for SQLAlchemy special classes."""
    if isinstance(obj, datetime.date):
        return obj.isoformat()
    elif isinstance(obj, decimal.Decimal):
        return float(obj)

@app.route("/login", methods=['GET', 'POST'])
@oid.loginhandler
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for("index"))

    form = LoginForm()

    if form.validate_on_submit():
        session["remember_me"] = form.remember_me.data
        return oid.try_login(form.openid.data, ask_for=["nickname", "email"])

    return render_template("login.html", title="Sign In", form=form, providers=app.config["OPENID_PROVIDERS"])

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))

@app.route("/user/<nickname>")
@app.route("/user/<nickname>/<int:page>")
@login_required
def user(nickname, page=1):
    user = User.query.filter_by(nickname=nickname).first()

    if user == None:
        flash(gettext("User %s not found") % nickname)
        return redirect(url_for("index"))

    posts = user.posts.paginate(page, POSTS_PER_PAGE, False)

    return render_template("user.html", user=user, posts=posts)

@app.route("/edit", methods=["GET", "POST"])
@login_required
def edit():
    form = EditForm(g.user.nickname)
    if form.validate_on_submit():
        g.user.nickname = form.nickname.data
        g.user.about_me = form.about_me.data
        g.user.name = form.name.data
        db.session.add(g.user)
        db.session.commit()
        flash(gettext("Your changes have been saved."), "success")
        return redirect(url_for("edit"))
    else:
        form.nickname.data = g.user.nickname
        form.about_me.data = g.user.about_me
        form.name.data = g.user.name

    return render_template("edit.html", form=form)

@app.route("/follow/<nickname>")
@login_required
def follow(nickname):
    user = User.query.filter_by(nickname=nickname).first()
    if user is None:
        flash("User %s not found." % nickname)

    if user == g.user:
        flash("You can't follow yourself")

    u = g.user.follow(user)

    if u is None:
        flash("Cannot follow %s." % nickname)
        return redirect(url_for("user", nickname=nickname))

    db.session.add(u)
    db.session.commit()

    flash("You are now following %s" % nickname)
    follower_notification(user, g.user)
    return redirect(url_for("user", nickname=nickname))

@app.route("/unfollow/<nickname>")
@login_required
def unfollow(nickname):
    user = User.query.filter_by(nickname=nickname).first()

    if user is None:
        flash("User %s not found." % nickname)

    if user == g.user:
        flash("You can't unfollow yourself")

    u = g.user.unfollow(user)

    if u is None:
        flash("Cannot unfollow %s." % nickname)
        return redirect(url_for("user", nickname=nickname))

    db.session.add(u)
    db.session.commit()

    flash("You are unfollowd %s" % nickname)
    return redirect(url_for("user", nickname=nickname))

# Handle stuff
@app.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated:
        g.user.last_seen = datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()
    g.locale = get_locale()

@app.errorhandler(404)
def not_found_error(error):
    return render_template("404.html"), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template("500.html"), 500

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@oid.after_login
def after_login(resp):
    # resp contains information returned by the OpenID provider

    if resp.email is None or resp.email == "":
        flash("Invalid login. Please try again.")
        return redirect(url_for("login"))

    user = User.query.filter_by(email=resp.email).first()

    if user is None:
        nickname = resp.nickname

        if nickname is None or nickname == "":
            nickname = resp.email.split("@")[0]

        nickname = User.make_valid_nickname(nickname)
        nickname = User.make_unique_nickname(nickname)
        user = User(nickname=nickname, email=resp.email)
        db.session.add(user)
        db.session.commit()

        db.session.add(user.follow(user))
        db.session.commit()

    remember_me = False

    if "remember_me" in session:
        remember_me = session["remember_me"]
        session.pop("remember_me", None)

    login_user(user, remember=remember_me)

    return redirect(request.args.get("next") or url_for("index"))

@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(LANGUAGES.keys())

def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ))