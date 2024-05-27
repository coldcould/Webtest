import os
# from dotenv import load_dotenv, find_dotenv

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
# load_dotenv(find_dotenv())

class BaseConfig(object):
    # ???这个是干嘛来着
    SECRET_KEY = os.getenv('SECRET_KEY')

    # ???数据库是否追踪，有点忘了， 再看一遍
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # ??? Mail服务，先省略了
    MAIL_SERVER = os.getenv('MAIL_SERVER')

    BLUELOG_POST_PER_PAGE = 10
    BLUELOG_COMMENT_PER_PAGE = 15
    BLUELOG_MANAGE_POST_PER_PAGE = 15

class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data-dev.db')

class TestingConfig(BaseConfig):
    TESTING = True
    WTF_CSRF_ENALED = False
    # ??? 什么意思
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL',
                                        'sqlite:///' + os.path.join(basedir, 'data.db'))

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}