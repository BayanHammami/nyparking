import os


class Config(object):
    DEBUG = True
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'secret'
    SSQLALCHEMY_DATABASE_URI = 'postgresql://demodata:password@demodata.c3ctvtncfc4b.ap-southeast-2.rds.amazonaws.com:5432/demodata'


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True