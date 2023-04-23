"""Flask configuration."""
from os import environ, path

import web.exts

basedir = path.abspath(path.dirname(__file__))


class Config:
    """Base config."""
    DEBUG = True
    SECRET_KEY = environ.get('SECRET_KEY', default="MATP")
    SESSION_COOKIE_NAME = environ.get('SESSION_COOKIE_NAME', "MATP")
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'
    SQLALCHEMY_DATABASE_URI = web.exts.SQLALCHEMY_DATABASE_URI


class ProdConfig(Config):
    FLASK_ENV = 'production'
    DEBUG = False
    TESTING = False
    DATABASE_URI = environ.get('PROD_DATABASE_URI')


class DevConfig(Config):
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = True
    DATABASE_URI = environ.get('DEV_DATABASE_URI')
