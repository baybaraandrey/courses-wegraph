from datetime import timedelta
from pathlib import Path

import dj_database_url

import environ

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent.parent
APPS_DIR = BASE_DIR / 'courses'
env = environ.Env()

DOCKER = env.bool('DOCKER', default=False)
READ_DOTENV_FILE = env.bool('DJANGO_READ_DOTENV_FILE', default=True)
if READ_DOTENV_FILE or not DOCKER:
    env.read_env(str(BASE_DIR / '.env'))


DEBUG = env.bool('DJANGO_DEBUG', default=False)
SECRET_KEY = env.str(
    'DJANGO_SECRET_KEY',
    'i$(+4doe&44d_x$!a=%*2#6b=*5zubct*8c@%nrjxt@23)_xlw',
)
if not DOCKER:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'data.db',
        }
    }
else:
    POSTGRES_PASSWORD = env.str('POSTGRES_PASSWORD')
    POSTGRES_USER = env.str('POSTGRES_USER')
    POSTGRES_DB = env.str('POSTGRES_DB')
    POSTGRES_HOST = env.str('POSTGRES_HOST')
    POSTGRES_PORT = env.str('POSTGRES_PORT')

    DATABASE_URL = 'postgres://{user}:{passwd}@{host}:{port}/{db}'.format(
        user=POSTGRES_USER,
        passwd=POSTGRES_PASSWORD,
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
        db=POSTGRES_DB,
    )
    DATABASES = {
        'default': dj_database_url.parse(DATABASE_URL),
    }

ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS', default=['*'] if DEBUG else [])
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]
CORS_ALLOW_CREDENTIALS = False
CORS_ORIGIN_ALLOW_ALL = True

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
]
THIRD_PARTY_APPS = [
    'rest_framework',
    'django_filters',
    'drf_yasg',
    'django_extensions',
    'phonenumber_field',
]
AUTH_APPS = [

]

LOCAL_APPS = [
    'courses.core.apps.CoreConfig',
    'courses.users.apps.UsersConfig',
    'courses.hls.apps.HlsConfig',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS + AUTH_APPS

MIDDLEWARE = [
    'courses.core.middlewares.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [str(APPS_DIR / 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',  # noqa: E501
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',  # noqa: E501
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',  # noqa: E501
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',  # noqa: E501
    },
]

AUTH_USER_MODEL = 'users.User'
LOGIN_URL = '/admin/login'
ADMIN_URL = '^admin/'
SITE_ID = env.int('DJANGO_SITE_ID', 1)

# REST Framework
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS':
    'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 100,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
}
JWT_SECRET_KEY = env('DJANGO_JWT_SECRET_KEY')
JWT_ACCESS_TOKEN_LIFETIME = env.int(
    'DJANGO_JWT_ACCESS_TOKEN_LIFETIME', 5)  # default 5 minutes
JWT_REFRESH_TOKEN_LIFETIME = env.int(
    'DJANGO_JWT_REFRESH_TOKEN_LIFETIME', 1440)  # default 1 day
JWT_RECOVERY_PASSWORD_TOKEN_LIFETIME = env.int(
    'DJANGO_JWT_RECOVERY_PASSWORD_TOKEN_LIFETIME', 5)  # default 5 minutes
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=JWT_ACCESS_TOKEN_LIFETIME),
    'REFRESH_TOKEN_LIFETIME': timedelta(minutes=JWT_REFRESH_TOKEN_LIFETIME),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': JWT_SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'uid',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATICFILES_DIRS = [
    APPS_DIR / 'static',
]

STATIC_ROOT = str(BASE_DIR / '.static')
STATIC_URL = '/static/'


MEDIA_ROOT = str(BASE_DIR / '.media')
MEDIA_URL = '/media/'

# Temporarily in this place for test purposes
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

RECOVERY_PASSWORD_REDIRECT_URL = env.str(
    var='RECOVERY_PASSWORD_REDIRECT_URL',
    default='http://localhost:8000/',
)
