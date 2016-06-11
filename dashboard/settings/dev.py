from __future__ import absolute_import, unicode_literals

from .base import *



# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '9oy(88fy6$p6m!2jx^xf&j5)gw2xim(s%qvz*s+7ps^-equlst'


EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


try:
    from .local import *
except ImportError:
    pass
