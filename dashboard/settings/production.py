from __future__ import absolute_import, unicode_literals

from .base import *

DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '9oy(88fy6$p6m!2jx^xf&j5)gw2xim(s%qvz*s+7ps^-equlst'

try:
    from .local import *
except ImportError:
    pass

# ZIE WEB HOSTING DOCUMENTATIE VOOR MEER INFO OVER ONDERSTAANDE SETTINGS


# Parse database configuration from $DATABASE_URL
import dj_database_url
DATABASES['default'] =  dj_database_url.parse(default='postgres://aysszcrjtglpno:cFm8Ufnl2klOV1o92rnDW-pV8s@ec2-54-247-185-241.eu-west-1.compute.amazonaws.com:5432/d7d26hc0g6p94k')

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

# WhiteNoise is de aanbevolen package voor static files in Heroku
STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

# COMPRESS

COMPRESS_ENABLED = True

COMPRESS_OFFLINE = True
COMPRESS_CSS_FILTERS = [
    'compressor.filters.css_default.CssAbsoluteFilter',
    'compressor.filters.cssmin.CSSMinFilter',
]
COMPRESS_CSS_HASHING_METHOD = 'content'