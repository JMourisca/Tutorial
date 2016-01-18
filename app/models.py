import re
from hashlib import md5
from app import db

"""
This is an auxiliary table for a many-to-many relationship, that's why it doesn't belong to a class.
"""
followers = db.Table("followers",
                     db.Column("follower_id", db.Integer, db.ForeignKey("user.id")),
                     db.Column("followed_id", db.Integer, db.ForeignKey("user.id"))
            )

images = db.Table("images_subcat",
                  db.Column("subcategory_id", db.Integer, db.ForeignKey("subcategory.id")),
                  db.Column("image_id", db.Integer, db.ForeignKey("image.id"))
                  )

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    nickname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    """
        one-to-many relationship is normally defined on the 'one' side. Here we can get the list of a user's post
        with user.posts.
        The first argument is the "many" class of the relationship.
        The backref defines a field that will be added to the objects of the "many"class: post.author returns the
        User instance that created the post.
    """
    posts = db.relationship("Post", backref="author", lazy="dynamic")
    categories = db.relationship("Category", backref="author", lazy="dynamic")
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime)
    """
        - 'User' is the right side entity that is in this relationship (the left side entity is the parent class).
            Since we are defining a self-referential relationship we use the same class on both sides.
        - secondary indicates the association table that is used for this relationship.
        - primaryjoin indicates the condition that links the left side entity (the follower user) with the association
            table. Note that because the followers table is not a model there is a slightly odd syntax required to get
            to the field name.
        - secondaryjoin indicates the condition that links the right side entity (the followed user) with the
            association table.
        - backref defines how this relationship will be accessed from the right side entity. We said that for a given
            user the query named followed returns all the right side users that have the target user on the left side.
            The back reference will be called followers and will return all the left side users that are linked to the
            target user in the right side. The additional lazy argument indicates the execution mode for this query.
            A mode of dynamic sets up the query to not run until specifically requested. This is useful for performance
            reasons, and also because we will be able to take this query and modify it before it executes. More about
            this later.
        - lazy is similar to the parameter of the same name in the backref, but this one applies to the regular query instead of the back reference.
    """
    followed = db.relationship("User",
                               secondary=followers,
                               primaryjoin=(followers.c.follower_id == id),
                               secondaryjoin=(followers.c.followed_id == id),
                               backref=db.backref("followers", lazy="dynamic"),
                               lazy="dynamic")

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    @staticmethod
    def make_unique_nickname(nickname):
        if User.query.filter_by(nickname=nickname).first() is None:
            return nickname

        version = 2
        new_nickname = nickname + str(version)
        while True:
            new_nickname = nickname + str(version)
            if User.query.filter_by(nickname=new_nickname).first() is None:
                break
            version += 1
        return new_nickname

    @staticmethod
    def make_valid_nickname(nickname):
        return re.sub("[^a-zA-Z0-9_\.]", "", nickname)

    def get_id(self):
        return str(self.id)

    def avatar(self, size):
        return 'http://www.gravatar.com/avatar/%s?d=mm&s=%d' % (md5(self.email.encode('utf-8')).hexdigest(), size)

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)
            return self

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)
            return self

    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0

    def followed_posts(self):
        return Post.query.join(
            followers,
                (followers.c.followed_id == Post.user_id)
        ).filter(followers.c.follower_id == self.id).order_by(Post.timestamp.desc())

    def __repr__(self):
        name = self.name
        if self.name == None:
            name = self.nickname

        return "<User %r>" % (name)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    language = db.Column(db.String(5))

    def __repr__(self):
        return "<Post %r>" % (self.body)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(100))
    category_slug = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    subcategories = db.relationship("Subcategory", backref="category", lazy="dynamic")

    def delete(self, id):
        if self.author.id != id or self.subcategories.count() > 0:
            if self.author.id != id:
                msg = "Cannot delete another user's information."

            if self.subcategories.count() > 0:
                msg = "This Category is not empty."

            return False, msg

        db.session.delete(self)
        db.session.commit()
        return True, "Deleted"

    def __repr__(self):
        return "<Category %s>" % self.category

class Subcategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subcategory = db.Column(db.String(100))
    subcategory_slug = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"))

    def delete(self, id):
        if self.category.author.id != id:
            return False, "Cannot delete another user's information."
        db.session.delete(self)
        db.session.commit()
        return True, "Deleted"

    def __repr__(self):
        return "<Subcategory %s>" % self.subcategory

class ImageCount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    count_view = db.Column(db.Integer)
    image_id = db.Column(db.Integer, db.ForeignKey("image.id"))
    timestamp = db.Column(db.DateTime)

