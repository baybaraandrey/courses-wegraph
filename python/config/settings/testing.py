from .base import *  # noqa: F403, F401

DEBUG = False
TEMPLATE_DEBUG = False
DEBUG_LOGGING = False

# for sorl:
THUMBNAIL_DEBUG = False


# this guy makes the tests run very very fast
PASSWORD_HASHERS = ('django.contrib.auth.hashers.MD5PasswordHasher',)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',  # noqa: F405
        'TEST': {},
    },
}
