import dj_database_url
import django_heroku

from livelobby.settings.base import *  # NOQA

DEBUG = False

DATABASES = {
    'default': dj_database_url.config()
}

# Activate Django-Heroku.
django_heroku.settings(locals())
