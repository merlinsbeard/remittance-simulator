from .base import *
import environ

root = environ.Path(__file__) -3
env = environ.Env()
environ.Env.read_env(root.path('local.env')())

DEBUG = True


INSTALLED_APPS += [
    'partner',
    'rest_framework',
    'raven.contrib.django.raven_compat',
]
ALLOWED_HOSTS = ['*']

# DATABASE CONFIG
DATABASES = {
        'default': env.db(),
}

STATIC_ROOT = os.path.join(BASE_DIR, "static")

import os
import raven

RAVEN_CONFIG = {
    'dsn': env('SENTRY'),
    # If you are using git, you can also automatically configure
    # the
    # release based on the git info.
    #'release': raven.fetch_git_sha(os.path.dirname(os.pardir)),
}
