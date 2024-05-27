import os

from flask import Flask, render_template
from flask_login import current_user
from flask_wtf.csrf import CSRFError

from bluelog.models import Category, Admin, Comment
from bluelog.settings import config
from bluelog.blueprints.admin import admin_bp
from bluelog.blueprints.auth import auth_bp
from bluelog.blueprints.blog import blog_bp
from bluelog.extensions import db, moment, bootstrap, login_manager, csrf


# p0 用工厂函数创建应用示例
def create_app(config_name=None):
    # config用于区分生产和开发环境
    if config_name == None:
        # ???这边的getenv是否是在.env中查找FLASK_ENV的值
        config_name = os.getenv('FLASK_ENV')

    app = Flask('bluelog')
    app.config.from_object(config[config_name])

    register_blueprints(app)
    register_extensions(app)
    register_commands(app)
    register_template_context(app)
    register_errors(app)

    return app


# p1 注册蓝本
def register_blueprints(app):
    app.register_blueprint(blog_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(auth_bp, url_prefix='/auth')

# 扩展加入实例
def register_extensions(app):
    db.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)


import click
# 注册到app上
def register_commands(app):
    @app.cli.command()
    @click.option('--drop', is_flag=True, help='Init Database')
    def initdb(drop):
        if drop:
            db.drop_all()
            db.create_all()
        else:
            db.create_all()


    @app.cli.command()
    @click.option('--category', default=10, help='Quantity of categories, default is 10.')
    @click.option('--post', default=50, help='Quantity of posts, default is 50.')
    @click.option('--comment', default=500, help='Quantity of posts, default is 500.')
    def forge(category, post, comment):
        """Generates the fake categories, posts, and comments """
        from bluelog.fakes import fake_categories,fake_posts,fake_admin,fake_comments

        db.drop_all()
        db.create_all()

        click.echo('生成用户')
        fake_admin()

        click.echo('生成分类')
        fake_categories(category)

        click.echo('生成文章')
        fake_posts(post)

        click.echo('生成评论')
        fake_comments(comment)

        click.echo('成功')


    # 创建管理员账户命令
    @app.cli.command()
    @click.option('--username', prompt=True, help='The username used to login.')
    @click.option('--password', prompt=True, hide_input=True,
                    confirmation_prompt=True, help='The password used to login.')
    def init(username, password):
        """Building Bluelog, just for you"""

        click.echo('Initializing the database...')
        db.create_all()

        admin = Admin.query.first()
        if admin:   # 如果数据库中已经有管理员记录就更新用户名和密码
            click.echo('The administrator already exists, updating...')
            admin.username = username
            admin.set_password(password)
        else:   # 否则创建新的管理员
            click.echo('Creating the temporary administrator account...')
            admin = Admin(
                username=username,
                name='Admin',
                about='Anything about you.',
            )
            admin.set_password(password)
            db.session.add(admin)

        category = Category.query.first()
        if category is None:
            click.echo('Creating the default category...')
            category = Category(name='Default')
            db.session.add(category)

        db.session.commit()
        click.echo('Done.')





# 处理模板上下文 ??这个是干嘛的
def register_template_context(app):
    @app.context_processor
    def make_template_context():
        categories = Category.query.order_by(Category.name).all()
        if current_user.is_authenticated:
            unread_comments = Comment.query.filter_by(reviewed=False).count()
        else:
            unread_comments = None
        return dict(categories=categories, unread_comments=unread_comments)


def register_errors(app):
    @app.errorhandler(CSRFError)
    def handle_csrf_error(e):
        return render_template('400.html', description=e.description), 400
