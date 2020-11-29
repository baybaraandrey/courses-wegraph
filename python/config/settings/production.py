from .base import *  # noqa: F403, F401
from .base import env


SECRET_KEY = env('DJANGO_SECRET_KEY')
ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS', default=['localhost'])

# mailgun integration
MAILGUN_BASE_URL = env.str(
    'DJANGO_MAILGUN_BASE_URL',
    default='https://api.mailgun.net/v3',
)
MAILGUN_API_KEY = env.str('DJANGO_MAILGUN_API_KEY')
MAILGUN_DOMAIN_NAME = env.str('DJANGO_MAILGUN_DOMAIN_NAME')
MAILGUN_FROM = env.str('DJANGO_MAILGUN_FROM')
