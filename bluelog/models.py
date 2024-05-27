from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash

from bluelog.extensions import db

from flask_login import UserMixin

# 数据库模型设计
# 文章，评论，用户，分类

# 管理员模型 还不知道干啥的，随便写点
class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30))
    password_hash = db.Column(db.String(128))
    name = db.Column(db.String(30))
    about = db.Column(db.Text)

    # 除了创建单独的set_password()方法设置密码，还可通过创建只读属性来实现
    # @property
    # def password(self):
    #     raise AttributeError(u'该属性不可读')
    #
    # @password.setter
    # def password(self, password):
    #     self.password_hash = generate_password_hash(password)


    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)


# 分类模型
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)

    posts = db.relationship('Post', back_populates='category')


# 文章模型
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30))
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    # 一个分类有多个文章
    category_id = db.Column(db.Integer, db.ForeignKey('category.id')) # 设立外键
    category = db.relationship('Category', back_populates='posts')  # ???back_populates具体啥用来着

    comments = db.relationship('Comment', back_populates='post')

# 评论模型
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(30))
    body = db.Column(db.Text)
    timestamp= db.Column(db.DateTime, default=datetime.utcnow())
    # 一个文章有多个评论
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    post = db.relationship('Post', back_populates='comments')
    # 每个评论可以有多个回复，每个回复也是个评论 # ???邻近列表关系
    replied = db.relationship('Comment', back_populates='replies', remote_side=[id])# remote_side
    replied_id = db.Column(db.Integer, db.ForeignKey('comment.id'))
    replies = db.relationship('Comment', back_populates='replied', cascade='all')# cascade
    # 是否给管理员过目过
    reviewed = db.Column(db.Boolean, default=False)



