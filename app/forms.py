from flask.ext.babel import gettext
from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, TextAreaField, HiddenField
from wtforms.validators import DataRequired, Length
from app.models import User

class LoginForm(Form):
    openid = StringField("openid", validators=[DataRequired()])
    remember_me = BooleanField("remember_me", default=False)

class EditForm(Form):
    name = StringField("name", validators=[DataRequired()])
    nickname = StringField("nickname", validators=[DataRequired()])
    about_me = TextAreaField("about_me", validators=[Length(min=0, max=140)])

    def __init__(self, original_nickname, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.original_nickname = original_nickname

    def validate(self):
        if not Form.validate(self):
            return False

        if self.nickname.data == self.original_nickname:
            return True

        if self.nickname.data != User.make_valid_nickname(self.nickname.data):
            self.nickname.errors.append(gettext("This nickname has invalid characters. Please try again."))
            return False

        user = User.query.filter_by(nickname=self.nickname.data).first()
        if user != None:
            self.nickname.errors.append("This nickname is already in use. Please choose another.")
            return False

        return True

class PostForm(Form):
    post = StringField("post", validators=[DataRequired()])

class CategoryForm(Form):
    category = StringField("category", validators=[DataRequired()])

class SubCategoryForm(Form):
    subcategory = StringField("subcategory", validators=[DataRequired()])

class SearchAlbum(Form):
    query = StringField("query", validators=[DataRequired()])