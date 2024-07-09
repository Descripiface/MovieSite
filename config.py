import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Configuration(object):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = 'movie film'
    SQLALCHEMY_POOL_PRE_PING = True
    #
    POSTS_PER_PAGE = 36

    # ####Flask Sequrity
    SECURITY_PASSWORD_SALT = 'salt'
    SECURITY_PASSWORD_HASH = 'bcrypt'