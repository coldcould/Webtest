import random

from faker import Faker
from sqlalchemy.exc import IntegrityError

from bluelog.extensions import db
from bluelog.models import Category, Post, Comment, Admin

def fake_admin():
    admin = Admin(
        username='admin',
        name='Skybabies',
        about='Um, 1, I am SkyBaby, had a fun time as a member of CHAM...',
        password_hash='admin',
    )
    db.session.add(admin)
    db.session.commit()

faker = Faker()

def fake_categories(count=10):
    category = Category(name='Default')
    db.session.add(category)

    for i in range(count):
        category = Category(name=faker.name())
        db.session.add(category)
        try:
            db.session.commit()
        except IntegrityError: # ??? rollback() IntergrityError什么意思
            db.session.rollback()

def fake_posts(count=50):
    for i in range(count):
        post = Post(
            title = faker.sentence(),
            body = faker.text(2000),
            timestamp = faker.date_time_this_year(),
            category = Category.query.get(random.randint(1, Category.query.count()))
        )
        db.session.add(post)
    db.session.commit()

def fake_comments(count=500):
    for i in range(count):
        comment = Comment(
            author=faker.name(),
            body=faker.text(150),
            timestamp=faker.date_time_this_year(),
            post=Post.query.get(random.randint(1, Post.query.count()))
        )
        db.session.add(comment)
    db.session.commit()
    for i in range(count):
        comment = Comment(
            author=faker.name(),
            body=faker.text(150),
            timestamp=faker.date_time_this_year(),
            post=Post.query.get(random.randint(1, Post.query.count())),
            replied=Comment.query.get(random.randint(1, Comment.query.count()))
        )
        db.session.add(comment)
    db.session.commit()

