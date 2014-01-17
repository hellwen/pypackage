class Config(object):
    SECRET_KEY = '\xb5\xc8\xfb\x18\xba\xc7*\x03\xbe\x91{\xfd\xe0L\x9f\xe3\\\xb3\xb1P\xac\xab\x061'

    ACCEPT_LANGUAGES = ['en', 'zh']
    BABEL_DEFAULT_LOCALE = 'zh'
    BABEL_DEFAULT_TIMEZONE = 'Asia/Shanghai'

    PER_PAGE = 20

class DevConfig(Config):
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = 'sqlite:///pypackage.db'
    SQLALCHEMY_ECHO = True

    UPLOADS_DEFAULT_DEST = '/static/'
    UPLOADS_DEFAULT_URL = '/static'
    STATIC_URL_ROOT = '/static'

    CACHE_TYPE = "simple"
    CACHE_DEFAULT_TIMEOUT = 300

    USE_LOCAL_COMMENT = True # if false, to include comment.html

    DEBUG_LOG = 'logs/debug.log'
    ERROR_LOG = 'logs/error.log'

    ADMINS = ('yourname@domain.com',)

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_DEBUG = DEBUG
    MAIL_USERNAME = 'username'
    MAIL_PASSWORD = 'password'
    DEFAULT_MAIL_SENDER = 'yourname@domain.com'

class PrdConfig(Config):

    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://pypackage@127.0.0.1/pypackage_db'
    SQLALCHEMY_ECHO = True

    UPLOADS_DEFAULT_DEST = '/static/'
    UPLOADS_DEFAULT_URL = '/static'
    STATIC_URL_ROOT = '/static'

    CACHE_TYPE = "simple"
    CACHE_DEFAULT_TIMEOUT = 300

    USE_LOCAL_COMMENT = True # if false, to include comment.html

    DEBUG_LOG = 'logs/debug.log'
    ERROR_LOG = 'logs/error.log'

