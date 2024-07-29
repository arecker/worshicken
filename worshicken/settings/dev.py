# flake8: noqa

from .common import *

SECRET_KEY = 'not-a-secure-key-just-for-dev-relax'

DEBUG = True

ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'tmp/db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = []

EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"

EMAIL_FILE_PATH = BASE_DIR / 'tmp/emails'

MEDIA_ROOT = BASE_DIR / 'tmp/uploads'
