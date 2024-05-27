from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms import TextAreaField
from wtforms.validators import DataRequired, Length, ValidationError


# 登录表单
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(1,20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(8,128)])
    remember = BooleanField('Remember me')
    submit = SubmitField('Log in')



from flask_ckeditor import CKEditorField
from wtforms import SelectField

from bluelog.models import Category


# 文章表单
class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(1,30)])
    category = SelectField('Category', coerce=int, default=1)
    body = CKEditorField('Body',validators=[DataRequired()])
    submit = SubmitField()

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.category.choices = [(category.id, category.name)
                                 for category in Category.query.order_by(Category.name).all()]


# 分类表单
class CategoryForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(1,30)])
    submit = SubmitField()

    def validate_name(self, field):
        if Category.query.filter_by(name=field.data).first():
            raise ValidationError('Name already in use.')


# 评论表单
class CommentForm(FlaskForm):
    author = StringField('Name', validators=[DataRequired(), Length(1,30)])
    body = TextAreaField('Comment', validators=[DataRequired()])
    submit = SubmitField()
